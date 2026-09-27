"""The untraced control's collection tooling (`_dev/docs/spec/jioh/task-9.5-untraced-control.md`)."""

import importlib.util
import pathlib
import re

MEAS = pathlib.Path(__file__).resolve().parents[1] / "meas"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


snapshot = _load("snapshot_for_control", MEAS / "probe" / "snapshot.py")


def _stat(pid, comm, ppid, start):
    # fields 3 on: state, ppid, eight zeros, utime, stime, six zeros, starttime (field 22)
    rest = ["S", str(ppid)] + ["0"] * 9 + ["7", "3"] + ["0"] * 6 + [str(start), "0"]
    return f"{pid} ({comm}) " + " ".join(rest) + "\n"


def _process(root, pid, comm, cmd, cgroup, tasks, ppid=1):
    """A fake /proc/<pid>: `tasks` maps tid -> (comm, start, run_ns, wait_ns, slices, vol, invol)."""
    d = root / str(pid)
    (d / "task").mkdir(parents=True)
    (d / "cmdline").write_text(cmd.replace(" ", "\0") + "\0")
    (d / "comm").write_text(comm + "\n")
    (d / "cgroup").write_text(f"0::{cgroup}\n")
    (d / "stat").write_text(_stat(pid, comm, ppid, tasks[pid][1]))
    for tid, (tcomm, start, run, wait, slices, vol, invol) in tasks.items():
        t = d / "task" / str(tid)
        t.mkdir()
        (t / "stat").write_text(_stat(tid, tcomm, ppid, start))
        if run is not None:
            (t / "schedstat").write_text(f"{run} {wait} {slices}\n")
        (t / "status").write_text(f"Name:\t{tcomm}\nvoluntary_ctxt_switches:\t{vol}\nnonvoluntary_ctxt_switches:\t{invol}\n")


def _fake_proc(root):
    _process(root, 100, "soffice.bin", "/usr/lib/libreoffice/program/soffice.bin --norestore /tmp/doc/large.odt",
             "/user.slice/user-1001.slice/session-3.scope",
             {100: ("soffice.bin", 5000, 123456789, 1000, 42, 30, 12), 101: ("gmain", 5001, 2000, 10, 3, 2, 1)})
    _process(root, 120, "oosplash", "/usr/lib/libreoffice/program/oosplash", "/user.slice",
             {120: ("oosplash", 4990, 900, 0, 1, 1, 0), 121: ("gone", 4991, None, None, None, 0, 0)}, ppid=100)
    _process(root, 200, "bash", "bash", "/user.slice", {200: ("bash", 10, 5, 0, 1, 1, 0)})


def test_the_snapshot_reads_each_threads_runtime_and_switches(tmp_path, monkeypatch):
    # decision 9: each thread's CPU from task/<tid>/schedstat (ns), its switches from task/<tid>/status, and its
    # start time, which tells a reused tid from the thread it replaced
    _fake_proc(tmp_path)
    monkeypatch.setattr(snapshot, "PROC", str(tmp_path))
    snap = snapshot.snapshot("soffice", None)
    procs = {p["pid"]: p for p in snap["procs"]}
    assert sorted(procs) == [100, 120]                         # the matching root and its descendant, not bash
    assert procs[100]["cgroup"] == "/user.slice/user-1001.slice/session-3.scope"
    tasks = {t["tid"]: t for t in procs[100]["tasks"]}
    assert tasks[100] == {"tid": 100, "comm": "soffice.bin", "start_ticks": 5000, "run_ns": 123456789,
                          "wait_ns": 1000, "slices": 42, "vol": 30, "invol": 12}
    assert tasks[101]["comm"] == "gmain" and tasks[101]["run_ns"] == 2000


def test_a_thread_that_left_mid_read_is_skipped(tmp_path, monkeypatch):
    _fake_proc(tmp_path)
    monkeypatch.setattr(snapshot, "PROC", str(tmp_path))
    procs = {p["pid"]: p for p in snapshot.snapshot("soffice", None)["procs"]}
    assert [t["tid"] for t in procs[120]["tasks"]] == [120]    # 121's schedstat is gone


def test_the_tree_totals_are_kept(tmp_path, monkeypatch):
    _fake_proc(tmp_path)
    monkeypatch.setattr(snapshot, "PROC", str(tmp_path))
    snap = snapshot.snapshot("soffice", None)
    assert snap["n_procs"] == 2 and snap["n_threads"] == 4
    assert snap["vol_switches"] == 30 + 2 + 1 + 0 and snap["nonvol_switches"] == 12 + 1


def _src(*p):
    return MEAS.joinpath(*p).read_text()


def _body(src, fn):
    m = re.search(rf"^{fn}\(\) \{{(.*?)^\}}", src, re.S | re.M)
    assert m, f"no function {fn}()"
    return m.group(1)


def _arm(src, app):
    m = re.search(rf"^    {re.escape(app)}\)\n(.*?);;\n", src, re.S | re.M)
    assert m, f"no appdef arm {app}"
    return m.group(1)


MODE_MAP = 'case "$MODE_ARG" in control) CONTROL=1; MODE=full ;; control-dry) CONTROL=1; MODE=dry ;; esac'
ORDER = re.compile(r'if \[ \$\(\(REPEAT % 2\)\) -eq 1 \]; then ORDER="traced untraced"; else ORDER="untraced traced"; fi')


def test_every_family_maps_the_control_modes_onto_its_own(repo_root):
    # a control job runs full's lengths (`control`) or dry's (`control-dry`); its artifact keeps the mode it was
    # launched with, which no campaign pool takes (decision 15)
    for fam in ("campaign", "desktop", "session"):
        src = _src(fam, "run.sh")
        assert MODE_MAP in src, fam
        assert 'rec mode "$MODE_ARG"' in src and 'rec control "$CONTROL"' in src, fam
        assert ORDER.search(src), f"{fam}: decision 5, odd jobs traced first, even jobs untraced first"
        assert "rec sysctl.sched_schedstats" in src, f"{fam}: decision 9, the switch recorded in each job"


def test_the_untraced_run_is_the_traced_run_without_perf(repo_root):
    # decision 1: the same snapshots, driver and length, and no perf
    for fam in ("campaign", "desktop", "session"):
        quiet = _body(_src(fam, "run.sh"), "quiet")
        assert "perf" not in quiet, fam
        pair = _body(_src(fam, "run.sh"), "pair")
        assert "for run in $ORDER" in pair and 'phase "$name"' in pair and 'quiet "$name-untraced"' in pair, fam
    q95 = _body(_src("campaign", "run.sh"), "quiet")
    assert q95.index('snap "$PAT" "" "$name.before"') < q95.index('sleep "$secs" &') < q95.index('snap "$PAT" "" "$name.after"')
    assert 'phase_summary "$name"' in q95 and 'phase_summary "$name"' in _body(_src("campaign", "run.sh"), "phase")


def test_the_campaign_control_pairs_every_carried_phase(repo_root):
    src = _src("campaign", "run.sh")
    ctl = _body(src, "control_phases")
    assert 'pair idle "$IDLE" no_driver' in ctl and 'pair play "$PLAY" no_driver' in ctl         # decision 3
    assert 'pair driven "$((DRIVEN + 5))" stream_driver prelude' in ctl
    assert 'pair driven "$((DRIVEN + 5))" pointer_loop prelude' in ctl
    assert 'pair op "$((OPS + 5))" op_run_driver' in ctl
    assert "driven-alt" not in ctl and "aalto" not in ctl       # the 136M phase is carried by no archetype
    # decision 6: idle, then driven, then the operation — both idle runs before any input
    assert ctl.index("pair idle") < ctl.index("pair driven") < ctl.index("pair op")
    assert re.search(r'if \[ "\$CONTROL" = 1 \]; then\n\s*control_phases\nelse\n', src)


def test_the_prelude_runs_before_each_driven_run(repo_root):
    # decision 4: the same prelude before each of the two driven runs, the window re-read after it
    src = _src("campaign", "run.sh")
    loop = _body(src, "pair").split("for run in $ORDER")[1]
    assert loop.index('ctrl_prelude "$name.$run"') < loop.index('phase "$name"')
    assert loop.index('ctrl_prelude "$name.$run"') < loop.index('quiet "$name-untraced"')
    pre = _body(src, "ctrl_prelude")
    assert 'bash -c "$CTRLPRELUDE"' in pre and 'wait_window "$CLASS"' in pre and 'screenshot "after-ctrlprelude-$1"' in pre
    assert 'CTRLPRELUDE="${CTRLPRELUDE:-$ALTPRELUDE}"' in src


def test_each_run_writes_its_own_driver_log(repo_root):
    src = _src("campaign", "run.sh")
    assert "replay-untraced.jsonl" in _body(src, "stream_driver")
    assert "ops-untraced.jsonl" in _body(src, "op_run_driver") and "OPS_OUT=" in _body(src, "op_run_driver")
    assert "${OPS_OUT:-$OUT/ops.jsonl}" in _body(_src("probe", "appdefs.sh"), "op_driver")
    assert 'DRV="$(pointer_loop)"' in src              # the campaign's pointer loop and the control's are one


def test_the_three_new_preludes_are_defined(repo_root):
    appdefs = _src("probe", "appdefs.sh")
    assert 'OP=""; ALTPRELUDE=""; CTRLPRELUDE=""' in appdefs
    for app in ("soffice", "gimp", "kdenlive"):
        assert "CTRLPRELUDE=" in _arm(appdefs, app), app
    assert "/tmp/doc/large.odt" in _arm(appdefs, "soffice").split("CTRLPRELUDE=")[1]
    assert '<Actions>/file/file-revert' in _arm(appdefs, "gimp")
    assert '<Action name="file_revert" shortcut="Ctrl+Shift+F8"/>' in _arm(appdefs, "kdenlive")


def test_a_prelude_answers_only_the_dialog_it_raised(repo_root):
    # the dry runs of 2026-09-27: with no window manager, keys go to the window under the pointer, so Writer's Alt+D
    # and GIMP's Return missed their dialogs (runs #612, #613); focusing the dialog explicitly then left the reopened
    # Writer document without the keyboard (run #614). The pointer now sits at the window's centre, where the dialog
    # opens, and each prelude answers a confirmation only when that dialog is up, by its title — Writer's "Save
    # Document?" (querysavedialog.ui, discard button "Do_n't Save"), GIMP's "Revert Image" (file-commands.c),
    # Kdenlive's "Revert to last saved version" (projectmanager.cpp, asked only of a modified project) — and says so
    # if it is still up after
    appdefs = _src("probe", "appdefs.sh")
    for app, title, key in (("soffice", "^Save Document", "alt+n"), ("gimp", "^Revert Image", "Return"),
                            ("kdenlive", "^Revert to last saved version", "Return")):
        pre = _arm(appdefs, app).split("CTRLPRELUDE=")[1]
        assert f"if xdotool search --onlyvisible --name '{title}' > /dev/null; then" in pre, app
        # run #615: a key sent the moment the dialog maps, the pointer still, did not reach it — the pointer is nudged
        # across it and the dialog given a second first
        assert (f"xdotool mousemove_relative 1 1; sleep 0.3; xdotool mousemove_relative -- -1 -1; sleep 1; "
                f"xdotool key --clearmodifiers {key}; sleep 2; xdotool search --onlyvisible --name '{title}' > /dev/null && echo dialog-still-up") in pre, app
        assert "windowfocus" not in pre, app
    assert "alt+d" not in _arm(appdefs, "soffice")
    # run #615: the document reopened after the dialog took no keys until clicked — a click at the pointer, on the
    # first page's running text, before Ctrl+End puts the caret at the end in both preludes
    sof = _arm(appdefs, "soffice").split("CTRLPRELUDE=")[1]
    assert sof.index("sleep 30; xdotool click 1; sleep 1; xdotool key --clearmodifiers ctrl+End") > sof.index("soffice --norestore")
    pre = _body(_src("campaign", "run.sh"), "ctrl_prelude")
    assert pre.index("getwindowgeometry --shell") < pre.index("xdotool mousemove") < pre.index('bash -c "$CTRLPRELUDE"')


def test_the_interactive_workflow_holds_the_longest_control_job(repo_root):
    # web-browser's control job: 420 s settle + 2 × 600 + 2 × 605 + 2 × 605 s of phases, about 68 minutes
    wf = (repo_root / ".github" / "workflows" / "meas-interactive.yml").read_text()
    assert "timeout-minutes: 150" in wf


def test_the_desktop_control_pairs_each_subject_s_carried_phase_alone(repo_root):
    # decision 3: renderer-hidden `steady`, renderer-visible `steady-notimer`, chat-client `idle`, game-client `shown`
    src = _src("desktop", "run.sh")
    chrome = _body(src, "chrome_subject")
    assert 'if [ "$CONTROL" = 1 ]; then pair steady "$STEADY"; else phase steady "$STEADY" ""; fi' in chrome
    assert 'if [ "$CONTROL" = 1 ]; then pair steady-notimer "$STEADY"; else phase steady-notimer "$STEADY" ""; fi' in chrome
    # the timer phase is carried by no archetype: its time kept, unmeasured, so the pages switch off on schedule
    assert re.search(r'if \[ "\$CONTROL" = 1 \]; then edge timer-wait start; sleep "\$STEADY"; edge timer-wait end\n'
                     r'\s*else phase steady-timer "\$STEADY" ""; fi', chrome)
    element = src[src.index("  element)\n"):src.index("  steam)\n")]
    assert 'pair idle "$STEADY"' in element and element.index("pair idle") < element.index("phase traffic")
    assert re.search(r'if \[ "\$CONTROL" = 1 \]; then pair idle "\$STEADY".*?\n\s*else\n', element, re.S)
    steam = src[src.index("  steam)\n"):src.index("  *) rec error")]
    assert re.search(r'if \[ "\$CONTROL" = 1 \]; then pair shown "\$STEADY".*?\n\s*else\n', steam, re.S)
    quiet = _body(src, "quiet")
    assert quiet.index('edge "$name" start') < quiet.index('snap "$PAT" "" "$name.before"') < quiet.index('sleep "$secs" &')
    assert quiet.index('snap "$PAT" "" "$name.after"') < quiet.index('edge "$name" end')


def test_the_session_control_pairs_the_steady_phase_with_a_snapshot_at_each_edge(repo_root):
    src = _src("session", "run.sh")
    assert 'if [ "$CONTROL" = 1 ]; then pair steady "$STEADY"; else phase steady "$STEADY"; fi' in src
    assert "sys_snap() { sudo python3 \"$MEAS/probe/snapshot.py\" '.'" in src
    for fn in ("phase", "quiet"):
        body = _body(src, fn)
        # the snapshot sits between the census and the recorded edge, on both sides: /proc only, outside the run
        assert body.index('census "$name.start"') < body.index('sys_snap "$name.before"') < body.index('edge "$name" start'), fn
        assert body.index('edge "$name" end') < body.index('sys_snap "$name.after"') < body.index('census "$name.end"'), fn
