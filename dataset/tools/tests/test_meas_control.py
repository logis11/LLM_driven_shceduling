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
                f"xdotool key --clearmodifiers {key}; sleep 2; if xdotool search --onlyvisible --name '{title}' > /dev/null; "
                f"then echo dialog-still-up; ") in pre, app
        # run #616: GIMP's first prelude kept its dialog through the pointer path, which an explicit focus answered in
        # run #614 — the focus is the second stage, taken only while the dialog is still up (the focus's own run #614
        # left the reopened Writer document without the keyboard, so it is never the first)
        assert (f"xdotool search --onlyvisible --name '{title}' windowfocus --sync key --clearmodifiers {key}; sleep 2; "
                f"xdotool search --onlyvisible --name '{title}' > /dev/null && echo dialog-still-up-after-focus; fi; fi") in pre, app
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


# ---- analysis: the shared core (analysis plan, task 1) ----------------------------------------------------------

def _snap(t, procs):
    """procs: {pid: [(tid, comm, start, run_ns, vol, invol)]}"""
    return {"t_mono": t, "procs": [{"pid": pid, "cmd": f"app{pid}", "cgroup": "/", "tasks": [
        {"tid": tid, "comm": comm, "start_ticks": st, "run_ns": run, "wait_ns": 0, "slices": 0, "vol": vol, "invol": inv}
        for tid, comm, st, run, vol, inv in ts]} for pid, ts in procs.items()]}


def test_the_deltas_count_only_threads_alive_at_both_edges():
    from meas import control
    before = _snap(100.0, {10: [(10, "main", 1, 1_000_000, 10, 1), (11, "worker", 2, 0, 0, 0), (12, "old", 3, 5, 5, 0)]})
    after = _snap(160.0, {10: [(10, "main", 1, 4_000_000, 40, 3), (11, "worker", 2, 2_000_000, 20, 0),
                               (12, "new", 99, 7, 2, 0), (13, "born", 50, 9, 9, 9)]})
    deltas, span = control.thread_deltas(before, after)
    assert span == 60.0
    # 12 is a new thread under a reused tid (another start time), 13 was born within the run: neither counts (decision 10)
    assert sorted(k[1] for k in deltas) == [10, 11]
    assert deltas[(10, 10, 1)] == {"pid": 10, "comm": "main", "run_ns": 3_000_000, "vol": 30, "invol": 2}


def test_threads_group_by_the_family_s_key_and_values_are_per_wake():
    from meas import control
    deltas = {(10, 10, 1): {"pid": 10, "comm": "main", "run_ns": 3_000_000, "vol": 30, "invol": 2},
              (10, 11, 2): {"pid": 10, "comm": "worker", "run_ns": 2_000_000, "vol": 20, "invol": 0},
              (10, 12, 3): {"pid": 10, "comm": "worker", "run_ns": 1_000_000, "vol": 30, "invol": 1},
              (20, 20, 4): {"pid": 20, "comm": "harness", "run_ns": 9, "vol": 9, "invol": 9}}
    g = control.group(deltas, lambda pid, comm: None if comm == "harness" else comm)
    assert g == {"main": {"run_ns": 3_000_000, "vol": 30, "invol": 2, "threads": 1},
                 "worker": {"run_ns": 3_000_000, "vol": 50, "invol": 1, "threads": 2}}
    # decision 8: the run mean is CPU over voluntary switches, the wake rate voluntary switches over the span
    assert control.rate_and_run(g["worker"], 50.0) == (1.0, 0.06)
    assert control.rate_and_run({"run_ns": 5, "vol": 0, "invol": 0, "threads": 1}, 50.0) == (0.0, None)


def test_the_reading_is_the_d36_check_with_the_two_orders_beside_it():
    from meas import control
    from meas.background.pool import check
    pairs = {1: ("traced untraced", 10.0, 9.7), 2: ("untraced traced", 10.0, 9.8), 3: ("traced untraced", 12.0, 11.7),
             4: ("untraced traced", 11.0, 10.8), 5: ("traced untraced", 10.0, 9.75), 6: ("untraced traced", 10.0, 0.0)}
    out = control.read(pairs)
    ratios = {1: 0.97, 2: 0.98, 3: 0.975, 4: 0.9818, 5: 0.975, 6: None}   # job 6's untraced side is zero: no ratio
    assert {k: out["per_repeat"][k] for k in ratios} == ratios
    # the pooled medians take every job's value, job 6's zero included
    assert out["a"] == 10.0 and out["b"] == 9.775
    ref = check(10.0, 9.775, ratios)
    assert out["reading"] == ref["reading"] == "difference" and out["interval"] == ref["interval"]
    assert out["ratio"] == ref["ratio"] == 0.9775
    assert out["n"] == 5
    assert out["order_means"] == {"traced untraced": round((0.97 + 0.975 + 0.975) / 3, 4),
                                  "untraced traced": round((0.98 + 0.9818) / 2, 4)}


# ---- analysis: 9.5's adapter (analysis plan, task 2) ------------------------------------------------------------

def _write_job(d, order, sides):
    """A control artifact in miniature: sides[run] = {phase: (t0, t1, {pid: (cmd, [(tid, comm, run0, run1, vol0, vol1)])})}"""
    import json as _j
    d.mkdir(parents=True)
    rep = {"app": "chrome", "control.order": order, "replay.sent": "100", "replay_untraced.sent": "80"}
    (d / "report.json").write_text(_j.dumps(rep))
    for run, phases in sides.items():
        for phase, (t0, t1, procs) in phases.items():
            name = phase if run == "traced" else f"{phase}-untraced"
            for edge, t, i in (("before", t0, 0), ("after", t1, 1)):
                snap = {"t_mono": t, "procs": [{"pid": pid, "cmd": cmd, "cgroup": "/", "tasks": [
                    {"tid": tid, "comm": comm, "start_ticks": tid, "run_ns": (r0, r1)[i], "wait_ns": 0, "slices": 0,
                     "vol": (v0, v1)[i], "invol": 0} for tid, comm, r0, r1, v0, v1 in ts]} for pid, (cmd, ts) in procs.items()]}
                (d / f"snap.{name}.{edge}.json").write_text(_j.dumps(snap))
    for log, durs in (("ops.jsonl", (400, 500, 900)), ("ops-untraced.jsonl", (380, 470))):
        rows = [{"op": "page-load", "i": i, "trigger_us": 1_000_000 * i, "done_us": 1_000_000 * i + 1000 * ms, "rc": 0}
                for i, ms in enumerate(durs)]
        rows.append({"op": "page-load", "i": 9, "trigger_us": 0, "done_us": 99_000_000, "rc": 3})    # a failed op is left out
        (d / log).write_text("".join(_j.dumps(r) + "\n" for r in rows))


MAIN, GPU = "/opt/google/chrome/chrome --user-data-dir=/tmp/chrome-data", "/opt/google/chrome/chrome --type=gpu-process"


def _job_sides(scale):
    procs = lambda k: {1: (MAIN, [(1, "chrome", 0, int(4e6 * k), 0, 40), (2, "Chrome_IOThread", 0, int(1e6 * k), 0, 20),
                                  (3, "llvmpipe-0", 0, 10**9, 0, 999), (4, "xdotool", 0, 10**9, 0, 999)]),
                       2: (GPU, [(5, "VizCompositorTh", 0, int(2e6 * k), 0, 10)]),
                       3: ("/opt/google/chrome/chrome --type=renderer", [(6, "Compositor", 0, 10**9, 0, 999)])}
    return {"idle": (0.0, 100.0, procs(scale)), "driven": (200.0, 300.0, procs(3 * scale)), "op": (400.0, 500.0, procs(2 * scale))}


CARRIED_95 = {"exclude_roles": ["renderer"], "phases": {
    "idle": {"components": {"selected": ["chrome", "gpu/VizCompositorTh"], "residual": {"gap_ms": {"table": [1]}}},
             "threads": {"chrome": {"gap_ms": {"table": [1]}}, "gpu/VizCompositorTh": {"gap_ms": {"table": [1]}}}},
    "driven": {"components": {"selected": ["chrome"], "residual": None}, "threads": {"chrome": {"gap_ms": {"table": [1]}}},
               "per_input": {}},
    "op": {"components": {"selected": ["chrome"], "residual": {"gap_ms": {"table": [1]}}},
           "threads": {"chrome": {"gap_ms": {"table": [1]}}}, "operation": {}}}}


def test_the_campaign_adapter_keys_threads_as_the_pool_keys_components(tmp_path):
    from meas.campaign import control as c95
    _write_job(tmp_path / "job", "traced untraced", {"traced": _job_sides(1.0), "untraced": _job_sides(0.9)})
    order, vals = c95.job_values(str(tmp_path / "job"), "chrome", CARRIED_95)
    assert order == "traced untraced"
    # idle: the selected components and the residual (Chrome_IOThread); llvmpipe and the harness's xdotool dropped as the
    # pool drops them, the renderer role excluded as chrome's pool excludes it
    assert vals["idle chrome wakes/s"] == (0.4, 0.4) and vals["idle chrome run mean (ms)"] == (0.1, 0.09)
    assert vals["idle gpu/VizCompositorTh run mean (ms)"] == (0.2, 0.18)
    assert vals["idle residual run mean (ms)"] == (0.05, 0.045)
    assert not any("renderer" in k or "llvmpipe" in k or "xdotool" in k for k in vals)
    # the typing entries' driven phase carries the per-input run over the tree, not components (chrome is not a
    # pointer-loop app): (tree CPU − the same side's idle CPU rate × span) / inputs that side sent
    assert "driven chrome wakes/s" not in vals
    t, u = vals["driven per-input run (ms)"]
    assert round(t, 6) == round((21e6 - 7e6) / 1e6 / 100, 6) and round(u, 6) == round((18.9e6 - 6.3e6) / 1e6 / 80, 6)
    # the operation: its duration over the rc-0 operations of each side's own log
    assert vals["op operation duration mean (ms)"] == (600.0, 425.0)
    assert vals["op chrome run mean (ms)"] == (0.2, 0.18) and "op residual wakes/s" in vals


# ---- analysis: 9.8's and 9.9's adapters (analysis plan, task 3) -------------------------------------------------

REND = "/opt/google/chrome/chrome --type=renderer --enable-features=x"


def _write_desktop_job(d, app, phase, order, procs_by_run, renderers_tsv=None):
    """procs_by_run[run] = (t0, t1, {pid: (cmd, [(tid, comm, run0, run1, vol0, vol1)])})"""
    import json as _j
    d.mkdir(parents=True)
    (d / "report.json").write_text(_j.dumps({"app": app, "control.order": order}))
    if renderers_tsv:
        (d / "renderers.tsv").write_text(renderers_tsv)
    for run, (t0, t1, procs) in procs_by_run.items():
        name = phase if run == "traced" else f"{phase}-untraced"
        for edge, t, i in (("before", t0, 0), ("after", t1, 1)):
            snap = {"t_mono": t, "procs": [{"pid": pid, "cmd": v[0], "cgroup": v[2] if len(v) > 2 else "/", "tasks": [
                {"tid": tid, "comm": comm, "start_ticks": tid, "run_ns": (r0, r1)[i], "wait_ns": 0, "slices": 0,
                 "vol": (v0, v1)[i], "invol": 0} for tid, comm, r0, r1, v0, v1 in v[1]]} for pid, v in procs.items()]}
            (d / f"snap.{name}.{edge}.json").write_text(_j.dumps(snap))


def test_the_desktop_adapter_reads_a_renderer_component_per_renderer(tmp_path):
    from meas.desktop import control as c98
    def procs(k):
        return (0.0, 100.0, {
            1: ("/opt/google/chrome/chrome --user-data-dir=/tmp/chrome-data", [(1, "chrome", 0, 10**9, 0, 999)]),
            # the control tab: the busiest renderer, dropped (desktop/analyze.drop_control_tab)
            10: (REND, [(10, "chrome", 0, 10**8, 0, 5000), (11, "HangWatcher", 0, 10**6, 0, 100)]),
            20: (REND, [(20, "chrome", 0, int(2e6 * k), 0, 20), (21, "HangWatcher", 0, int(1e6 * k), 0, 10),
                        (22, "Compositor", 0, int(3e5 * k), 0, 3)]),
            30: (REND, [(30, "chrome", 0, int(4e6 * k), 0, 40)]),           # no HangWatcher: counts at zero in the mean
            40: (REND, [(40, "chrome", 0, 10**7, 0, 900)]),                  # an extension process: not a page's renderer
        })
    tsv = "10\tchrome --type=renderer\n20\tchrome --type=renderer\n30\tchrome --type=renderer\n40\tchrome --type=renderer --extension-process\n"
    _write_desktop_job(tmp_path / "job", "chrome-hidden", "steady", "untraced traced",
                       {"traced": procs(1.0), "untraced": procs(0.5)}, tsv)
    carried = {"phases": {"steady": {"components": {"selected": ["chrome", "HangWatcher"], "residual": {"x": 1}}}}}
    order, vals = c98.job_values(str(tmp_path / "job"), "chrome-hidden", carried)
    assert order == "untraced traced"
    # renderers 20 and 30 only: rate the mean over them, run mean their pooled CPU over their pooled wakes
    assert vals["steady chrome wakes/s"] == (0.3, 0.3)
    assert vals["steady chrome run mean (ms)"] == (0.1, 0.05)
    assert vals["steady HangWatcher wakes/s"] == (0.05, 0.05) and vals["steady HangWatcher run mean (ms)"] == (0.1, 0.05)
    assert vals["steady residual wakes/s"] == (0.015, 0.015) and vals["steady residual run mean (ms)"] == (0.1, 0.05)


def test_the_session_adapter_keys_threads_by_instance(tmp_path):
    import json as _j
    from meas.session import control as c99
    U = "/user.slice/user-1002.slice/user@1002.service"
    def procs(k):
        return (0.0, 1800.0, {
            1: ("/sbin/init", [(1, "systemd", 0, int(9e6 * k), 0, 90)], "/init.scope"),
            400: ("@dbus-daemon --system", [(400, "dbus-daemon", 0, int(1e6 * k), 0, 10)], "/meas.slice/dbus.service"),
            520: ("/usr/bin/gnome-shell", [(520, "gnome-shell", 0, int(5e7 * k), 0, 500), (521, "gmain", 0, int(2e6 * k), 0, 40)],
                  f"{U}/session.slice/org.gnome.Shell@wayland.service"),
            900: ("/usr/sbin/cron", [(900, "cron", 0, 10**9, 0, 999)], "/system.slice/cron.service"),
        })
    _write_desktop_job(tmp_path / "job", "session", "steady", "traced untraced",
                       {"traced": procs(1.0), "untraced": procs(0.8)})
    for name in ("steady", "steady-untraced"):
        (tmp_path / "job" / f"census.{name}.start.json").write_text(_j.dumps({"uid": 1002}))
    carried = {"phases": {"steady": {"entries": {
        "systemd": {"components": {"selected": ["pid1/systemd"]}},
        "dbus-daemon": {"components": {"selected": ["system-bus/dbus-daemon"]}},
        "gnome-shell": {"components": {"selected": ["gnome-shell/gnome-shell", "gnome-shell/gmain"]}}}}}}
    order, vals = c99.job_values(str(tmp_path / "job"), carried)
    assert vals["systemd pid1/systemd wakes/s"] == (0.05, 0.05)
    assert vals["systemd pid1/systemd run mean (ms)"] == (0.1, 0.08)
    assert vals["gnome-shell gnome-shell/gmain run mean (ms)"] == (0.05, 0.04)
    assert vals["dbus-daemon system-bus/dbus-daemon run mean (ms)"] == (0.1, 0.08)
    assert not any("cron" in k for k in vals)


# ---- analysis: the shares of decisions 10 and 22 (analysis plan, task 4) ----------------------------------------

def test_the_shares_are_read_over_the_traced_run_s_wake_rows():
    from collections import namedtuple
    from meas import control
    R = namedtuple("R", "pid tid comm run")
    rows = [R(1, 1, "main", 4.0), R(1, 1, "main", 4.0), R(1, 2, "worker", 1.0), R(1, 3, "worker", 3.0),
            R(1, 9, "MemoryInfra", 50.0), R(1, 9, "MemoryInfra", 2.0), R(7, 7, "xdotool", 99.0)]
    alive = {(1, 1), (1, 2), (1, 9)}                      # tid 3 started or exited within the run
    key = lambda r: None if r.comm == "xdotool" else r.comm
    out = control.shares(rows, key, ["main", "MemoryInfra", "residual"], alive,
                         left=lambda r: r.comm == "MemoryInfra" and r.run >= 30.0)
    # decision 10: the residual (both worker threads) holds 3 of its 4 ms and 1 of its 2 wakes in the thread that left
    assert out["residual"]["exited"] == (0.75, 0.5)
    assert out["main"]["exited"] == (0.0, 0.0)
    # decision 22: MemoryInfra's heavy pass (50 of its 52 ms, 1 of 2 wakes) is what the carried value leaves out
    assert out["MemoryInfra"]["left"] == (round(50 / 52, 4), 0.5)
    assert out["main"]["left"] == (0.0, 0.0)
    assert control.shares(rows, key, ["main"], alive)["main"]["left"] is None     # no rule for this value


# ---- analysis: the operation windows' share of decision 23 (analysis plan, task 7) --------------------------------

def test_the_share_inside_the_operation_windows_is_read_beside_the_others():
    from collections import namedtuple
    from meas import control
    R = namedtuple("R", "pid tid comm run")
    rows = [R(1, 1, "main", 4.0), R(1, 1, "main", 1.0), R(1, 2, "worker", 3.0)]
    alive = {(1, 1), (1, 2)}
    out = control.shares(rows, lambda r: r.comm, ["main", "residual"], alive, inside=lambda r: r.run >= 3.0)
    assert out["main"]["inside"] == (0.8, 0.5)
    assert out["residual"]["inside"] == (1.0, 1.0)
    assert control.shares(rows, lambda r: r.comm, ["main"], alive)["main"]["inside"] is None   # a phase without an operation


def test_the_op_phase_s_inside_rows_are_the_ones_the_pool_reads():
    from collections import namedtuple
    from meas.campaign import analyze
    from meas.campaign import control as cc
    R = namedtuple("R", "pid tid comm run t_in")
    rows = [R(1, 1, "main", 1.0, 0.5), R(1, 1, "main", 2.0, 1.2), R(1, 1, "main", 4.0, 2.0), R(1, 1, "main", 8.0, 3.4)]
    ops = [{"op": "page-load", "trigger_us": 1_000_000, "done_us": 2_000_000, "rc": 0},
           {"op": "page-load", "trigger_us": 3_000_000, "done_us": 3_500_000, "rc": 1}]
    rule = cc.inside_rule(analyze.operation_windows(rows, ops))
    # a successful operation's [trigger, done) window only: the row at done and the failed operation's row are outside
    assert [rule(r) for r in rows] == [False, True, False, False]


def test_the_page_carries_the_operation_windows_share_only_for_an_archetype_with_an_operation():
    from meas import control_report
    recs = [{"exited": (0.0, 0.0), "left": None, "inside": (0.9, 0.8)},
            {"exited": (0.0, 0.0), "left": None, "inside": (0.7, 0.6)}]
    assert control_report._mean_shares(recs) == {"exited cpu": {"mean": 0.0, "max": 0.0}, "exited wakes": {"mean": 0.0, "max": 0.0},
                                                 "inside cpu": {"mean": 0.8, "max": 0.9}, "inside wakes": {"mean": 0.7, "max": 0.8}}
    value = {"a": 1.0, "b": 0.9, "ratio": 0.9, "per_repeat_mean": 0.9, "interval": [0.8, 1.0], "reading": "not resolved",
             "order_means": {}, "n": 6}
    rep = {"app": "chrome", "jobs": 6, "orders": {}, "builds": {}, "intervals": 2, "chance": 0.1, "differences": [],
           "values": {"idle chrome wakes/s": value, "op chrome wakes/s": value},
           "shares": {"idle chrome": control_report._mean_shares([{"exited": (0.0, 0.0), "left": None}]),
                      "op chrome": control_report._mean_shares(recs)}}
    lines = control_report.render({"family": "campaign", "archetypes": {"web-browser": rep}}).splitlines()
    assert next(l for l in lines if l.startswith("| value |")).endswith("| in the operation windows (CPU, wakes) |")
    assert next(l for l in lines if l.startswith("| op chrome wakes/s")).endswith("| 0.8, 0.7 |")
    assert next(l for l in lines if l.startswith("| idle chrome wakes/s")).endswith("| — |")
    rep["shares"] = {"idle chrome": rep["shares"]["idle chrome"]}
    del rep["values"]["op chrome wakes/s"]
    assert "operation windows" not in control_report.render({"family": "campaign", "archetypes": {"web-browser": rep}})


# ---- analysis: a copy left out of the control's pool (9.5 D66) ---------------------------------------------------

def test_the_report_reads_no_copy_the_pool_left_out(tmp_path):
    import json as _j
    from meas import control_report
    rep = _j.dumps({"gate": "open", "machine.model": "AMD EPYC 7763 64-Core Processor"})
    kept = tmp_path / "playback-mpv-video-from620" / "36300400332" / "meas-playback-mpv-video-r2-control"
    left = tmp_path / "playback-mpv-video-from620-excluded" / "36300802358" / "meas-playback-mpv-video-r2-control"
    for d in (kept, left):
        d.mkdir(parents=True)
        (d / "report.json").write_text(rep)
    assert control_report.find_jobs("campaign", str(tmp_path)) == {"mpv-video": {2: str(kept)}}


def test_the_page_names_each_copy_left_out_of_the_control_s_pool(tmp_path):
    from meas import control_report
    jobs = {}
    for k in range(1, 7):
        d = tmp_path / f"meas-interactive-chrome-r{k}-control"
        _write_job(d, "traced untraced" if k % 2 else "untraced traced", {"traced": _job_sides(1.0), "untraced": _job_sides(0.95)})
        jobs[k] = str(d)
    why = "D66: window 2 measured twice; the original launch's copy is kept"
    ctl = {"runs": {"chrome": {"excluded_repeats": {"2@36300802358": why}}}}
    rep = control_report.app_reports("campaign", "chrome", jobs, CARRIED_95, with_shares=False, control_pool=ctl)["web-browser"]
    assert rep["left_out"] == {"2@36300802358": why}
    assert rep["notes"] == control_report.control_notes(rep)   # the record carries the notes' reading for the fold-in
    md = control_report.render({"family": "campaign", "archetypes": {"web-browser": rep}})
    assert f"- left out of the control's pool: 2@36300802358 — {why}" in md.splitlines()


# ---- analysis: the workload check (analysis plan, task 5) --------------------------------------------------------

def test_a_control_artifact_is_pooled_only_under_the_control_flag(tmp_path):
    import json as _j
    import sys as _s
    from meas.desktop import pool as p98
    from meas.session import pool as p99
    saved = _s.modules.pop("analyze", None)
    try:
        import importlib
        p95 = importlib.import_module("meas.campaign.pool")
    finally:
        if saved is not None:
            _s.modules["analyze"] = saved
    # decision 15: a campaign pool never takes a control artifact; the control's traced runs pool apart
    assert p95.pooled_mode("full", False) and not p95.pooled_mode("control", False)
    assert p95.pooled_mode("control", True) and not p95.pooled_mode("full", True)
    assert p95.NAME.match("meas-interactive-chrome-r3-control")
    for fam, mod, app in (("desktop", p98, "steam"), ("session", p99, "session")):
        for k, mode in ((1, "control"), (2, "full")):
            d = tmp_path / fam / f"meas-{fam}-{app}-r{k}-{mode}"
            d.mkdir(parents=True)
            (d / "report.json").write_text(_j.dumps({"gate": "open"}))
            (d / "spec.json").write_text(_j.dumps({"cpu_model": "AMD EPYC 7763 64-Core Processor"}))
        runs, _, _, probes = mod.find_runs(str(tmp_path / fam), "EPYC 7763", modes=("control",))
        assert list(runs[app]) == [1] and [p["mode"] for p in probes] == ["full"], fam
        runs, _, _, probes = mod.find_runs(str(tmp_path / fam), "EPYC 7763")
        assert list(runs[app]) == [2] and [p["mode"] for p in probes] == ["control"], fam


def test_the_workload_check_places_each_control_value_in_the_carried_spread():
    from meas import control
    carried = {"stability": {"quantities": {"idle a wakes/s": {"k": 20, "mean": 10.0, "cv": 0.05},
                                            "idle b run mean (ms)": {"k": 20, "mean": 2.0, "cv": 0.1},
                                            "idle gone wakes/s": {"k": 20, "mean": 1.0, "cv": 0.2}}}}
    ctl = {"stability": {"quantities": {"idle a wakes/s": {"k": 6, "mean": 10.25, "cv": 0.04},
                                        "idle b run mean (ms)": {"k": 6, "mean": 1.7, "cv": 0.1},
                                        "idle new wakes/s": {"k": 6, "mean": 3.0, "cv": 0.1}}}}
    out = control.workload(carried, ctl)
    # z: the control's mean less the carried mean, over the carried per-repeat spread (cv × mean) — 9.5 D69's form
    assert out["z"] == {"idle a wakes/s": 0.5, "idle b run mean (ms)": -1.5}
    assert out["only_carried"] == ["idle gone wakes/s"] and out["only_control"] == ["idle new wakes/s"]
    assert out["max_abs_z"] == 1.5


# ---- analysis: the report (analysis plan, task 6) ----------------------------------------------------------------

def test_the_report_reads_every_value_over_the_jobs_and_counts_the_intervals(tmp_path):
    from meas import control_report
    jobs = {}
    for k in range(1, 7):
        order = "traced untraced" if k % 2 else "untraced traced"
        d = tmp_path / f"meas-interactive-chrome-r{k}-control"
        _write_job(d, order, {"traced": _job_sides(1.0), "untraced": _job_sides(0.9 + 0.01 * k)})
        jobs[k] = str(d)
    rep = control_report.app_reports("campaign", "chrome", jobs, CARRIED_95, with_shares=False)["web-browser"]
    assert rep["archetype"] == "web-browser" and rep["jobs"] == 6 and rep["orders"] == {"traced untraced": 3, "untraced traced": 3}
    v = rep["values"]["idle chrome run mean (ms)"]
    assert v["n"] == 6 and v["reading"] == "difference" and v["interval"][1] < 1
    # decision 12: how many intervals were read, and how many differences a 95 % level gives by chance alone
    assert rep["intervals"] == sum(1 for x in rep["values"].values() if x.get("interval")) and rep["chance"] == round(0.05 * rep["intervals"], 1)
    md = control_report.render({"family": "campaign", "archetypes": {"web-browser": rep}})
    assert "## web-browser (`chrome`)" in md and "idle chrome run mean (ms)" in md
    assert f"{rep['intervals']} intervals read" in md and "chance alone" in md


# ---- the notes' reading (fold-in plan, task 1) --------------------------------------------------------------------

def _diff(mean, lo, hi):
    return {"per_repeat_mean": mean, "interval": [lo, hi], "reading": "difference"}


def test_the_notes_read_the_counts_then_each_difference_by_phase_and_component(monkeypatch):
    from meas import control_report
    values = {"idle gpu/Chrome_ChildIOT run mean (ms)": _diff(0.8634, 0.8497, 0.8772),
              "idle gpu/VizCompositorTh run mean (ms)": _diff(0.9537, 0.9291, 0.9783),
              "idle gpu/VizCompositorTh wakes/s": _diff(0.9767, 0.96, 0.9933),
              "op Chrome_IOThread wakes/s": _diff(1.0368, 1.014, 1.0597),
              "op chrome run mean (ms)": _diff(0.9634, 0.9333, 0.9934),
              "op operation duration mean (ms)": _diff(0.99, 0.98, 0.995),
              "op residual wakes/s": {"per_repeat_mean": 0.99, "interval": [0.97, 1.01], "reading": "not resolved"}}
    rep = {"archetype": "web-browser", "app": "chrome", "jobs": 6, "intervals": 32, "chance": 1.6, "values": values,
           "differences": sorted(n for n, v in values.items() if v["reading"] == "difference")}
    monkeypatch.setitem(control_report.NOTES_STATED, "web-browser", "A stated line.")
    assert control_report.control_notes(rep) == (
        "Untraced control (the 9.5 untraced-control spec): six jobs each ran every carried phase twice, traced under "
        "`perf sched record` and untraced, read by the 95 % interval of the per-job ratios, untraced over traced; "
        "32 intervals read, about 1.6 differences by chance alone. Perf's effect on the carried values, which stay the "
        "traced ones — idle phase: `gpu/Chrome_ChildIOT` run mean 0.863 (0.850–0.877), `gpu/VizCompositorTh` run mean "
        "0.954 (0.929–0.978) and wake rate 0.977 (0.960–0.993); operation phase, over the whole phase: "
        "`Chrome_IOThread` wake rate 1.037 (1.014–1.060), `chrome` run mean 0.963 (0.933–0.993), the operation's "
        "duration mean 0.990 (0.980–0.995). A stated line.")


def test_the_notes_state_when_no_difference_is_found_and_read_a_session_entry_s_components():
    from meas import control_report
    rep = {"archetype": "audio-server", "app": "session", "jobs": 6, "intervals": 2, "chance": 0.1, "differences": [],
           "values": {"pipewire wireplumber/gmain wakes/s": {"per_repeat_mean": 1.0, "interval": [0.9, 1.1]}}}
    assert control_report.control_notes(rep).endswith("; 2 intervals read, about 0.1 differences by chance alone, none found.")
    rep["differences"] = ["gnome-shell gnome-shell/JS Helper run mean (ms)"]
    rep["values"]["gnome-shell gnome-shell/JS Helper run mean (ms)"] = _diff(0.864, 0.8414, 0.8865)
    assert control_report.control_notes(rep).endswith(
        "— steady phase: `gnome-shell/JS Helper` run mean 0.864 (0.841–0.886).")


def test_the_page_carries_the_lines_stated_for_an_archetype(monkeypatch):
    from meas import control_report
    monkeypatch.setitem(control_report.NOTES_STATED, "chat-client", "Stated in the notes.")
    monkeypatch.setitem(control_report.PAGE_STATED, "chat-client", "Stated on the page only.")
    rep = {"app": "element", "jobs": 6, "orders": {}, "builds": {}, "intervals": 0, "chance": 0.0, "differences": [],
           "values": {}, "shares": {}}
    md = control_report.render({"family": "desktop", "archetypes": {"chat-client": rep}}).splitlines()
    assert "Stated in the notes." in md and "Stated on the page only." in md


# ---- the fold-ins carry the reading (fold-in plan, task 2) --------------------------------------------------------

def _control_record(tmp_path, notes):
    import json as _j
    p = tmp_path / "control.json"
    p.write_text(_j.dumps({"archetypes": {a: {"notes": n} for a, n in notes.items()}}))
    return p


def _only_notes_gain(plain, read, archetype, reading):
    """`read` is `plain` with `reading` appended to `archetype`'s modeling_notes and nothing else changed."""
    import yaml
    a = yaml.safe_load("archetypes:\n" + plain)["archetypes"]
    b = yaml.safe_load("archetypes:\n" + read)["archetypes"]
    assert b[archetype]["modeling_notes"] == a[archetype]["modeling_notes"] + " " + reading
    b[archetype]["modeling_notes"] = a[archetype]["modeling_notes"]
    assert a == b


def test_the_9_5_fold_in_appends_each_archetype_s_reading_to_its_notes(repo_root, tmp_path):
    import shutil
    import subprocess
    import sys
    from test_meas import IDLE_POOL_95, POOLS_95, TAGS_95
    campaign = repo_root / "_dev" / "research" / "jioh" / "task-9.5-interactive-typing" / "campaign"
    (tmp_path / "pools").mkdir()
    for sub, app in POOLS_95:
        shutil.copy(campaign / sub / f"pool-{app}.json", tmp_path / "pools")
    idle = campaign / IDLE_POOL_95[0] / f"pool-{IDLE_POOL_95[1]}.json"
    run = lambda out, *extra: subprocess.run(
        [sys.executable, str(repo_root / "dataset" / "tools" / "meas" / "campaign" / "fold_in.py"), str(tmp_path / "pools"),
         str(out), *TAGS_95, "--idle-from", f"{IDLE_POOL_95[1]}={idle}", *extra], check=True, capture_output=True)
    run(tmp_path / "plain.yaml")
    run(tmp_path / "read.yaml", "--control", str(_control_record(tmp_path, {"audio-player": "Untraced control: one."})))
    _only_notes_gain((tmp_path / "plain.yaml").read_text(), (tmp_path / "read.yaml").read_text(), "audio-player",
                     "Untraced control: one.")


def test_the_9_8_and_9_9_fold_ins_append_each_archetype_s_reading_to_its_notes(repo_root, tmp_path):
    import sys
    from meas.desktop import fold_in as f98
    from meas.session import fold_in as f99
    results = repo_root / "_dev" / "research" / "jioh"
    for mod, slice_, archetype in ((f98, "task-9.8-browser-comms", "renderer-hidden"),
                                   (f99, "task-9.9-daemons-session", "compositor-shell")):
        pooled = results / slice_ / "campaign" / "results" / "pooled.json"
        ctl = _control_record(tmp_path, {archetype: "Untraced control: one."})
        outs = {}
        for name, extra in (("plain", []), ("read", ["--control", str(ctl)])):
            outs[name] = tmp_path / f"{mod.__name__}-{name}.yaml"
            argv, sys.argv = sys.argv, ["fold_in.py", str(pooled), str(outs[name]), *extra]
            try:
                mod.main()
            finally:
                sys.argv = argv
        _only_notes_gain(outs["plain"].read_text(), outs["read"].read_text(), archetype, "Untraced control: one.")


def test_the_build_census_reads_each_subject_s_own_version_key():
    from meas import control_report
    # the chat client's job records Element's build under its own key, the renderers' under `version` (decision 16)
    element = {1: {"element.version": "1.12.29", "synapse.version": "1.161.0+noble1"}, 2: {"element.version": "1.12.29"}}
    assert control_report._census("desktop", "chat-client", element) == {"Element 1.12.29": [1, 2]}
    steam = {k: {"steam.buildid": "1788652215", "steam.package": "steam-installer 1:1.0.0.79~ds-2"} for k in (1, 2)}
    assert control_report._census("desktop", "game-client", steam) == {"Steam client build 1788652215": [1, 2]}
    chrome = {1: {"version": "Google Chrome 153.0.8010.52 "}}
    assert control_report._census("desktop", "renderer-hidden", chrome) == {"Google Chrome 153.0.8010.52": [1]}


def test_the_report_names_the_archetypes_the_fold_ins_name(repo_root):
    import re as _re
    from meas import control_report
    src = (repo_root / "dataset" / "tools" / "meas" / "campaign" / "fold_in.py").read_text()
    body = src[src.index("ARCHETYPES = {"):src.index("\n}\n", src.index("ARCHETYPES = {"))]
    folded = {app: aid for aid, app in _re.findall(r'^    "([a-z-]+)": \("([a-z0-9-]+)",', body, _re.M)}
    assert control_report.ARCH_95 == folded


def test_a_play_entry_is_read_over_the_tree_only():
    # the play entries carry a period and the tree's whole CPU per cycle (fold_in, D74/D75), no components: the first
    # landed control jobs (playback #620) listed the play phase's per-thread tables, which no archetype carries
    from meas.campaign import control as c95
    ph = {"components": {"selected": ["ao", "mpv"], "residual": {"gap_ms": {"table": [1]}}},
          "threads": {"ao": {"gap_ms": {"table": [1]}}, "mpv": {"gap_ms": {"table": [1]}}}, "cycle": {}}
    assert c95.carried_components("mpv-audio", "play", ph) == []


def test_a_control_job_s_validity_names_what_would_leave_it_out(tmp_path):
    import json as _j
    from meas import control_report
    _write_job(tmp_path / "ok", "traced untraced", {"traced": _job_sides(1.0), "untraced": _job_sides(0.9)})
    rep = _j.loads((tmp_path / "ok" / "report.json").read_text())
    rep.update({"gate": "open", "replay.sent": "100", "replay_untraced.sent": "100", "ctrlprelude.driven.traced.rc": "0",
                "ctrlprelude.driven.untraced.rc": "0", "ops.count": "3", "ops.rc0": "3", "ops_untraced.count": "3", "ops_untraced.rc0": "2"})
    (tmp_path / "ok" / "report.json").write_text(_j.dumps(rep))
    (tmp_path / "ok" / "ctrlprelude.driven.traced.log").write_text("revert-query\n")
    (tmp_path / "ok" / "ctrlprelude.driven.untraced.log").write_text("revert-query\ndialog-still-up\n")
    assert control_report.validity(str(tmp_path / "ok")) == ["op-untraced: 1 of 3 operations failed"]
    rep.update({"replay_untraced.sent": "90", "ctrlprelude.driven.traced.rc": "1"})
    (tmp_path / "ok" / "report.json").write_text(_j.dumps(rep))
    (tmp_path / "ok" / "ctrlprelude.driven.traced.log").write_text("revert-query\ndialog-still-up\ndialog-still-up-after-focus\n")
    (tmp_path / "ok" / "snap.op-untraced.after.json").unlink()
    probs = control_report.validity(str(tmp_path / "ok"))
    assert "driven: the two runs replayed 100 and 90 events" in probs
    assert "prelude driven.traced: rc 1" in probs and "prelude driven.traced: its dialog stayed up" in probs
    assert "op-untraced: a snapshot is missing" in probs
