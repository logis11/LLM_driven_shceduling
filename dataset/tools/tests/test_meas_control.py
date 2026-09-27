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
