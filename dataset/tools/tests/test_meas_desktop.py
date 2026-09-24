"""Constructed cases for the 9.8 desktop campaign tools (changelog D13)."""

import json
import os
import re

import pytest

from meas.desktop import analyze, pool

CHROME_ARM = re.compile(r'^\s*LAUNCH="(google-chrome [^"]*)"', re.M)
CHROME_VAR = re.compile(r'^\s*CHROME="(google-chrome [^"]*)"', re.M)


def flags_of(cmd):
    """The leading run of --flags, which is what the three Chrome arms must share; the URLs after them differ."""
    out = []
    for tok in cmd.split()[1:]:
        if not tok.startswith("--"):
            break
        out.append(tok)
    return out


def test_the_three_chrome_arms_launch_with_identical_flags(repo_root):
    # D13: web-browser carries Chrome's tree minus its renderers (9.5 D14) and the two renderer entries carry the
    # renderers, so the halves of one application must be the same program launched the same way. The arms restate
    # the flags rather than share a variable, because extracting one would edit an arm 9.5 is still running
    # repeats through — so the identity is asserted here instead of being structural.
    src = (repo_root / "dataset" / "tools" / "meas" / "probe" / "appdefs.sh").read_text()
    arm = [flags_of(m) for m in CHROME_ARM.findall(src) if "/tmp/page.html" in m]
    var = [flags_of(m) for m in CHROME_VAR.findall(src)]
    assert len(arm) == 1, "expected exactly one `chrome` arm LAUNCH naming /tmp/page.html"
    assert len(var) == 1, "expected exactly one CHROME= shared by chrome-hidden and chrome-visible"
    # identical but for one stated flag: the spare renderer is not created, because it hosts no page and cannot
    # be told from a real one afterwards. The difference is asserted exactly, not merely allowed.
    assert var[0][:len(arm[0])] == arm[0], f"chrome arm {arm[0]} is not a prefix of {var[0]}"
    assert var[0][len(arm[0]):] == ["--disable-features=SpareRendererForSitePerProcess"], \
        f"the renderer arms may differ by that one flag only, found {var[0][len(arm[0]):]}"
    assert "--no-sandbox" in arm[0], "the flag is kept and stated (D13 corrects D12's claim that it is avoided)"


def test_the_measured_timer_is_an_interval_that_does_no_work_per_wake(repo_root):
    # D13 / decision 7: setInterval, not a one-shot setTimeout — intensive throttling applies only to timers
    # with a high nesting level — and a callback that increments a counter and returns, so the entries are
    # floors. The only other timer is the one-shot that walks the page's step plan.
    page = (repo_root / "dataset" / "tools" / "meas" / "probe" / "idle-page.html").read_text()
    assert page.count("setInterval(") == 1
    body = re.search(r"setInterval\(function \(\) \{(.*?)\}", page, re.S).group(1)
    assert body.strip() == "n++;", f"the callback must do nothing but count, found {body.strip()!r}"
    for call in re.findall(r"setTimeout\(([^,]+),", page):
        assert call.strip() == "step", f"the only one-shot timer walks the plan, found setTimeout({call})"


def _run_dir(tmp_path, app, phase, procs, rows, wakeups=""):
    (tmp_path / "report.json").write_text(json.dumps(
        {"app": app, "repeat": 1, "mode": "full", "gate": "open",
         "settings.origins": "3", "renderers.observed": "4"}))
    for s in ("before", "after"):
        (tmp_path / f"snap.{phase}.{s}.json").write_text(json.dumps({"procs": procs}))
    (tmp_path / f"perf.{phase}.timehist.txt").write_text(rows)
    (tmp_path / f"perf.{phase}.wakeups.txt").write_text(wakeups)
    (tmp_path / "edges.jsonl").write_text(json.dumps({"phase": phase, "edge": "start", "mono_ns": 0}) + "\n")
    return tmp_path


def test_only_renderer_processes_reach_the_components_of_a_renderer_subject(tmp_path):
    # D13: the renderer-only view is the inverse of the exclude_roles=("renderer",) filter that pooled
    # web-browser, so the same code computes both halves of one application. The browser process and the GPU
    # process are in the trace and must not be in the entry.
    procs = [{"pid": 100, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --user-data-dir=/tmp/chrome-data"},
             {"pid": 200, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=renderer --lang=en"},
             {"pid": 300, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=gpu-process"}]
    rows = ("   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
            "   1.000000 [0003]  chrome[100/100]    0.000      0.001      5.000      S\n"
            "   2.000000 [0003]  chrome[201/200]    0.000      0.001      1.000      S\n"
            "   3.000000 [0003]  chrome[201/200]    0.000      0.001      3.000      S\n"
            "   4.000000 [0003]  chrome[301/300]    0.000      0.001      9.000      S\n"
            "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    # one wakeup per renderer schedule-in, each at or before that row's schedule-in — the timehist time column is
    # the switch-out, so a row's t_in is time minus run. Without them the second row follows an S with no wakeup
    # since, which the wake rule folds into the first as a resume (method §5).
    wakeups = ("   1.990000 [0001]  x[9]  awakened: chrome[201/200]\n"
               "   2.990000 [0001]  x[9]  awakened: chrome[201/200]\n")
    d = _run_dir(tmp_path, "chrome-hidden", "steady", procs, rows, wakeups)
    ph = analyze.analyze_run_dir(str(d))["phases"]["steady"]
    assert ph["role_filter"] == "kept renderer only"
    assert ph["renderer_pids"] == [200]
    assert ph["resumes_merged"] == 0
    # two wakes of the renderer only: the browser's 5 ms and the GPU's 9 ms are out
    assert ph["threads"]["chrome"]["wakes_per_s"] == pytest.approx(2 / ph["span_s"], rel=1e-4)
    assert ph["threads"]["chrome"]["run_ms"]["sum"] == 4.0
    # method §5's shape, plus what tells the reader how many renderers the one archetype was pooled from
    assert {"threads", "wakes_per_s", "cpu_share", "gap_ms", "run_ms"} <= set(ph["threads"]["chrome"])
    assert ph["threads"]["chrome"]["renderers"] == 1
    assert ph["renderers_measured"] == 1 and ph["wakes_per_s_per_renderer"] == ph["wakes_per_s"]


def test_every_process_reaches_the_components_of_a_non_renderer_subject(tmp_path):
    # the role filter is the renderer subjects' alone: Element and Steam carry their whole tree
    procs = [{"pid": 100, "comm": "element", "cmd": "/usr/bin/element-desktop"},
             {"pid": 300, "comm": "element", "cmd": "/usr/bin/element-desktop --type=gpu-process"}]
    rows = ("   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
            "   1.000000 [0003]  element[100/100]    0.000      0.001      5.000      S\n"
            "   4.000000 [0003]  element[301/300]    0.000      0.001      9.000      S\n"
            "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    d = _run_dir(tmp_path, "element", "idle", procs, rows)
    ph = analyze.analyze_run_dir(str(d))["phases"]["idle"]
    assert ph["role_filter"] == "none"
    assert ph["threads"]["element"]["run_ms"]["sum"] == 14.0


def test_a_probe_artifact_is_named_but_never_pooled():
    # method §1: the long-phase probe runs in this family as a mode, and is never a repeat
    assert pool.NAME.match("meas-desktop-chrome-hidden-r3-full").groups() == ("chrome-hidden", "3", "full")
    assert pool.NAME.match("meas-desktop-element-r2-dry").groups() == ("element", "2", "dry")
    assert pool.NAME.match("meas-desktop-steam-r1-probe").group(3) == "probe"
    assert "probe" not in pool.POOLED_MODES
    assert pool.NAME.match("meas-interactive-code-r1-full") is None


def test_a_hidden_repeat_whose_renderers_never_throttled_is_left_out():
    # decision 9: throttling engagement is knowable only from the trace, so it is gated in the pool. A renderer
    # past the grace wakes about once a minute; one waking many times a second measured an unthrottled page.
    throttled = {"phases": {"steady": {"per_pid_wakes_per_s": {"200": 0.017, "201": 0.017}}}}
    unthrottled = {"phases": {"steady": {"per_pid_wakes_per_s": {"200": 0.017, "201": 9.8}}}}
    assert pool.throttling_check("chrome-hidden", throttled)[0] is True
    ok, worst = pool.throttling_check("chrome-hidden", unthrottled)
    assert ok is False and worst == 9.8
    # the visible subject is not throttled by design, so the check does not apply to it
    assert pool.throttling_check("chrome-visible", unthrottled)[0] is True


def test_the_control_tab_does_not_decide_the_throttling_check():
    # The control tab is never throttled — that is what it is for (method §2 subject 1), and
    # `per_pid_wakes_per_s` is computed before it is dropped. Reading it here rejected every repeat whose
    # renderers had throttled: the 2026-09-20 probe gated at the control's 10.193 wakes/s while the worst
    # measured renderer was 0.184.
    probe = {"phases": {"steady": {"per_pid_wakes_per_s": {"3494": 10.193, "3501": 0.182, "3508": 0.184},
                                   "control_tab": {"dropped": 3494, "wakes_per_s": 10.193,
                                                   "ratio_to_next": 55.26}}}}
    ok, worst = pool.throttling_check("chrome-hidden", probe)
    assert ok is True and worst == 0.184
    # a measured renderer that never throttled is still caught, with the control tab out of the way
    hot = {"phases": {"steady": {"per_pid_wakes_per_s": {"3494": 10.193, "3501": 0.182, "3508": 9.8},
                                 "control_tab": {"dropped": 3494}}}}
    ok, worst = pool.throttling_check("chrome-hidden", hot)
    assert ok is False and worst == 9.8
    # no control tab identified — nothing to exclude, and a phase holding only one is not a measurement
    only = {"phases": {"steady": {"per_pid_wakes_per_s": {"3494": 10.193},
                                  "control_tab": {"dropped": 3494}}}}
    assert pool.throttling_check("chrome-hidden", only) == (False, None)


def _loop_dirs(tmp_path, rows):
    """rows: {repeat -> report.kv dict}; every repeat gates open on the campaign's machine."""
    dirs = {}
    for k, kvs in rows.items():
        p = tmp_path / f"r{k}"
        p.mkdir(parents=True)
        (p / "report.json").write_text(json.dumps(
            {"gate": "open", "machine.model": "AMD EPYC 7763 64-Core Processor"}))
        (p / "report.kv").write_text("".join(f"{a}={b}\n" for a, b in kvs.items()))
        dirs[k] = str(p)
    return dirs


def _pool_runs(repo_root):
    """loop/pool_runs.py imports its sibling registry as a flat `common`, so its directory goes on the path."""
    import importlib
    import sys
    d = str(repo_root / "dataset" / "tools" / "meas" / "loop")
    if d not in sys.path:
        sys.path.insert(0, d)
    return importlib.import_module("pool_runs")


def test_the_desktop_validity_arm_reads_the_loop_s_checks(tmp_path, repo_root):
    # D13: the loop's per-repeat line for this family — the renderer count against the minimum the job wanted,
    # the page server, Element's session, and one origin count across the repeats that are repeats
    pool_runs = _pool_runs(repo_root)
    base = {"app": "chrome-hidden", "mode": "full", "renderers.wanted_min": "13",
            "renderers.observed": "13", "page.server": "200", "settings.origins": "12"}
    dirs = _loop_dirs(tmp_path / "chrome", {
        1: dict(base),
        2: dict(base, **{"renderers.observed": "9"}),
        3: dict(base, **{"mode": "probe", "settings.origins": "8"}),
    })
    # repeat 2 alone: the probe is never a repeat, so its smaller N stays out of the cross-repeat comparison
    assert pool_runs.validity("desktop", dirs, {"repeats": [1, 2, 3], "phases": {}}) == 1


def test_an_element_repeat_without_a_session_is_flagged(tmp_path, repo_root):
    # D7/D13: the idle phase the archetype reads is the /sync long poll, which no signed-out client holds, so a
    # repeat whose session never reached the homeserver measured a login screen
    pool_runs = _pool_runs(repo_root)
    dirs = _loop_dirs(tmp_path / "element", {
        1: {"app": "element", "mode": "full", "matrix.sync_rows": "0"},
        2: {"app": "element", "mode": "full", "matrix.sync_rows": "412"},
    })
    assert pool_runs.validity("desktop", dirs, {"repeats": [1, 2], "phases": {}}) == 1


def test_the_renderer_subjects_drive_no_input(repo_root):
    # the dry run of 2026-09-20 showed why: run.sh retyped a URL into each window through the omnibox, and
    # without a window manager xdotool windowactivate does not move X input focus, so all three navigations
    # landed on one window and two renderers kept their timers through the phase that was meant to have none.
    # The page now walks its own plan and the run synchronises on what each window reports.
    src = (repo_root / "dataset" / "tools" / "meas" / "desktop" / "run.sh").read_text()
    body = re.search(r"^chrome_subject\(\) \{(.*?)^\}", src, re.S | re.M).group(1)
    for forbidden in ("xdotool type", "xdotool key", "windowactivate", "navigate"):
        assert forbidden not in body, f"the renderer subjects must drive no input, found {forbidden!r}"
    wait = re.search(r"^wait_for_step\(\) \{(.*?)^\}", src, re.S | re.M).group(1)
    assert "getwindowname" in window_steps_body(src), "the step is read back per window, without focus"
    assert "rec " in wait and "seq 1" in wait, "the wait polls and records what it saw"


def window_steps_body(src):
    return re.search(r"^window_steps\(\) \{(.*?)^\}", src, re.S | re.M).group(1)


def test_the_archetype_carries_one_renderer_not_the_sum_of_n(tmp_path):
    # the job measures N renderers only so a throttled entry yields enough wakes to read (method §9). Every
    # renderer's main thread is named `chrome`, so per_thread over the whole tree returns the SUM over N, which
    # is not what the archetype describes. Two renderers, one wake each, must read as one renderer's rate.
    procs = [{"pid": p, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=renderer"} for p in (200, 300)]
    rows = ("   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
            "   1.000000 [0003]  chrome[201/200]    0.000      0.001      2.000      S\n"
            "   2.000000 [0003]  chrome[301/300]    0.000      0.001      2.000      S\n"
            "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    d = _run_dir(tmp_path, "chrome-visible", "steady-timer", procs, rows)
    ph = analyze.analyze_run_dir(str(d))["phases"]["steady-timer"]
    assert ph["renderers_measured"] == 2
    assert ph["wakes_per_s"] == round(2 / ph["span_s"], 3)                      # the set
    assert ph["wakes_per_s_per_renderer"] == round(ph["wakes_per_s"] / 2, 4)    # what the entry carries
    assert ph["threads"]["chrome"]["renderers"] == 2
    assert ph["threads"]["chrome"]["wakes_per_s"] == pytest.approx(1 / ph["span_s"], rel=1e-4)


def test_the_hidden_subject_drops_its_control_tab(tmp_path):
    # the control tab is the selected tab, so it stays visible to Blink and is never throttled: it is the single
    # fastest renderer, and the ratio to the next is recorded so the pool can see the identification was clean
    procs = [{"pid": p, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=renderer"} for p in (200, 300)]
    rows = ["   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"]
    for i in range(6):     # the control tab, unthrottled
        rows.append(f"   {1.0 + i:.6f} [0003]  chrome[201/200]    0.000      0.001      1.000      S\n")
    rows.append("   9.000000 [0003]  chrome[301/300]    0.000      0.001      1.000      S\n")
    rows.append("  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    # a wakeup at or before each schedule-in, else the wake rule folds the run of rows into one (method §5)
    wakeups = "".join(f"   {0.99 + i:.6f} [0001]  x[9]  awakened: chrome[201/200]\n" for i in range(6))
    d = _run_dir(tmp_path, "chrome-hidden", "steady", procs, "".join(rows), wakeups)
    ph = analyze.analyze_run_dir(str(d))["phases"]["steady"]
    assert ph["control_tab"]["dropped"] == 200
    assert ph["control_tab"]["ratio_to_next"] == 6.0
    assert ph["renderers_measured"] == 1
    assert list(ph["threads"]["chrome"]["wakes_per_s_per_renderer"]) == [pytest.approx(1 / ph["span_s"], rel=1e-4)]


def test_the_slice_profile_reads_a_phase_in_ten_second_slices(tmp_path):
    # method §3: the long-phase probe's steady phase is read per 10 s slice, which is what tells launch work
    # from behaviour that recurs (9.5 D35, D42). campaign/slices.py cannot do it for this family — it goes
    # through campaign.analyze_run, whose phase loop is fixed to 9.5's names and raises KeyError on ours.
    procs = [{"pid": 200, "comm": "element", "cmd": "/usr/bin/element-desktop"}]
    rows = ["   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"]
    for t in (1.0, 2.0, 3.0):            # three wakes in the first slice
        rows.append(f"   {t:.6f} [0003]  element[201/200]    0.000      0.001      2.000      S\n")
    rows.append("  25.000000 [0003]  element[201/200]    0.000      0.001      4.000      S\n")   # third slice
    rows.append("  30.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    wakeups = "".join(f"   {t - 0.01:.6f} [0001]  x[9]  awakened: element[201/200]\n"
                      for t in (1.0, 2.0, 3.0, 25.0))
    d = _run_dir(tmp_path, "element", "idle", procs, "".join(rows), wakeups)
    sl = analyze.analyze_run_dir(str(d))["phases"]["idle"]["slices"]
    assert sl["slice_s"] == 10.0
    assert len(sl["wakes_per_s"]) == 3
    assert sl["wakes_per_s"][0] == 0.3 and sl["wakes_per_s"][1] == 0.0 and sl["wakes_per_s"][2] == 0.1
    assert sl["cpu_ms_per_s"][0] == 0.6 and sl["cpu_ms_per_s"][2] == 0.4


def _entry(threads, residual=None, phase="idle"):
    return {"phases": {phase: {"threads": threads,
                               "components": {"selected": sorted(threads), "residual": residual}}}}


def _comp(rate, gap, run):
    return {"wakes_per_s": list(rate), "gap_ms": [{"mean": g} for g in gap], "run_ms": [{"mean": r} for r in run]}


def test_the_stability_rule_tests_each_carried_component_and_the_residual():
    # method §6 item 1 lists every value per component, and the residual's. The earlier criterion averaged the
    # components' gap means into one number: a steady component and a wild one could pass together, and the
    # residual was never tested. On the 2026-09-20 first batch it passed `element` with 6 of 15 values failing.
    steady = _comp([4.0] * 5, [250.0] * 5, [0.05] * 5)
    wild = _comp([4.0] * 5, [100.0, 400.0, 100.0, 400.0, 250.0], [0.05] * 5)
    res = {"wakes_per_s": [0.4] * 5, "gap_ms": {"repeat_mean": [2000.0] * 5},
           "run_ms": {"repeat_mean": [0.02, 0.02, 0.09, 0.02, 0.02]}}
    crit = pool.criterion("element", _entry({"a": steady, "b": wild}, res))
    q = crit["quantities"]
    assert q["idle a gap mean (ms)"]["passes"] is True
    assert q["idle b gap mean (ms)"]["passes"] is False
    assert q["idle residual run mean (ms)"]["passes"] is False
    assert "idle residual wakes/s" in q and crit["passes"] is False
    # every value carries the repeat count its present spread would need
    assert all("needed" in v for v in q.values())
    # all steady -> the entry holds
    ok = pool.criterion("element", _entry({"a": steady}, {**res, "run_ms": {"repeat_mean": [0.02] * 5}}))
    assert ok["passes"] is True


def test_run_means_carry_under_the_machine_spread_exception():
    # changelog D17, D18: run times move together across a repeat's threads, a per-runner speed. A run mean is
    # carried over five repeats with its half-width — for Steam too, once D5 is stated on the wake-rate ratio.
    wide_run = _comp([4.0] * 5, [250.0] * 5, [0.068, 0.047, 0.049, 0.065, 0.062])
    for app, phase in (("element", "idle"), ("steam", "shown"), ("chrome-hidden", "steady")):
        q = pool.criterion(app, _entry({"a": wide_run}, phase=phase))
        c = q["quantities"][f"{phase} a run mean (ms)"]
        assert c["passes"] is False and c["excepted"] is True and c["carried"] is True and q["passes"] is True
    # but not with fewer than five repeats behind it
    short = _comp([4.0] * 4, [250.0] * 4, [0.068, 0.047, 0.049, 0.065])
    assert pool.criterion("steam", _entry({"a": short}, phase="shown"))["passes"] is False
    # the exception never reaches a wake rate or a gap
    wide_gap = _comp([4.0] * 5, [100.0, 400.0, 100.0, 400.0, 250.0], [0.05] * 5)
    q = pool.criterion("element", _entry({"a": wide_gap}))
    assert q["quantities"]["idle a gap mean (ms)"]["carried"] is False and q["passes"] is False


def test_a_renderer_residual_describes_one_renderer_not_n_merged():
    # changelog D19: the residual merged every measured renderer's wakes, so its rate was N times a renderer's and
    # its gaps interleaved N processes. Two renderers, each waking every 100 s on one residual thread, offset by
    # 50 s: one renderer's residual wakes at 0.01/s with 100 s gaps, not 0.02/s with 50 s gaps.
    ts = {1: [0.0, 100.0, 200.0, 300.0], 2: [50.0, 150.0, 250.0, 350.0]}
    comms = {"Quiet": {"t_in_by_pid": {1: ts, 2: ts}, "runs": {1: [0.02] * 8, 2: [0.02] * 8},
                       "threads": {1: 2, 2: 2}}}
    by_rep = {k: {"renderers_measured": 2, "measured_renderer_pids": [1, 2], "t0": 0.0} for k in (1, 2)}
    res = pool.renderer_residual(["Quiet"], comms, {1: 400.0, 2: 400.0}, by_rep, {})
    assert res["wakes_per_s"] == [pytest.approx(0.01), pytest.approx(0.01)]
    assert res["gap_ms"]["repeat_mean"] == [100000.0, 100000.0]
    # a repeat where the residual wakes fewer than twice in every renderer is sporadic, not carried (D43)
    thin = {"Quiet": {"t_in_by_pid": {1: ts, 2: {1: [5.0]}}, "runs": {1: [0.02] * 8, 2: [0.02]},
                      "threads": {1: 2, 2: 1}}}
    cov = {}
    assert pool.renderer_residual(["Quiet"], thin, {1: 400.0, 2: 400.0}, by_rep, cov) is None
    assert cov["sporadic"][0]["comm"] == "residual"


def test_the_renderer_quiet_threads_carry_with_their_half_widths():
    # changelog D21: 9.5 D57's between-sessions exception, for the named quiet threads of the renderer entries — all
    # three of their values together, over at least five repeats — and for nothing else
    wild = _comp([0.0, 0.01, 0.005, 0.01, 0.002], [300000.0, 100000.0, 150000.0, 100000.0, 250000.0], [0.03] * 5)
    q = pool.criterion("chrome-visible", _entry({"Chrome_ChildIOT": wild}, phase="steady-notimer"))
    assert all(c["session_spread"] and c["carried"] for c in q["quantities"].values()) and q["passes"] is True
    q = pool.criterion("chrome-hidden", _entry({"Chrome_ChildIOT": wild}, phase="steady"))   # D24
    assert all(c["session_spread"] and c["carried"] for c in q["quantities"].values()) and q["passes"] is True
    q = pool.criterion("chrome-visible", _entry({"chrome": wild}, phase="steady-notimer"))
    assert q["passes"] is False                        # the main thread is not excepted
    q = pool.criterion("element", _entry({"Chrome_ChildIOT": wild}))
    assert q["passes"] is False                        # nor is any other subject's thread of the same name


def test_an_interrupted_artifact_download_leaves_nothing_behind_and_does_not_block_the_next(tmp_path, repo_root,
                                                                                          monkeypatch):
    # 2026-09-21: an extraction cut off at 41 of 43 files left a folder without report.json, and every later
    # download refused it with "file exists", so the pool could never be read again
    import subprocess
    _pool_runs(repo_root)
    import common
    dest = tmp_path / "run" / "meas-desktop-element-r15-full"
    dest.mkdir(parents=True)
    (dest / "after-credentials.png").write_text("partial")          # the leftover of the interrupted attempt

    def gh_fails(cmd, **kw):
        out = cmd[cmd.index("-D") + 1]
        with open(os.path.join(out, "half.png"), "w") as f:
            f.write("x")
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(common.subprocess, "run", gh_fails)
    with pytest.raises(subprocess.CalledProcessError):
        common.download(1, "meas-desktop-element-r15-full", str(dest))
    assert not dest.exists() and not (tmp_path / "run" / "meas-desktop-element-r15-full.partial").exists()

    def gh_ok(cmd, **kw):
        out = cmd[cmd.index("-D") + 1]
        for f in ("report.json", "after-credentials.png"):
            with open(os.path.join(out, f), "w") as fh:
                fh.write("{}")
    monkeypatch.setattr(common.subprocess, "run", gh_ok)
    assert common.download(1, "meas-desktop-element-r15-full", str(dest)) == str(dest)
    assert (dest / "report.json").exists()


def test_the_steam_client_components_carried_between_sessions():
    # changelog D23: steamwebhelper's and ThreadPoolForeg's gap means carried with their half-widths under 9.5 D57
    wild = _comp([70.0] * 5, [29.0, 29.0, 42.0, 29.0, 41.0], [0.05] * 5)
    q = pool.criterion("steam", _entry({"steamwebhelper": wild}, phase="shown"))
    assert q["quantities"]["shown steamwebhelper gap mean (ms)"]["carried"] is True and q["passes"] is True
    assert pool.criterion("steam", _entry({"steam": wild}, phase="shown"))["passes"] is False


def test_every_landing_of_an_index_that_landed_twice_is_pooled(tmp_path):
    # campaign workflow: every same-machine repeat obtained is pooled. A retry relaunched while an earlier launch of
    # the same index was queued lands twice (9.8: chrome-hidden repeat 10 four times); keying by index alone kept
    # the latest landing and dropped the rest without a word
    for run, k in (("111", 1), ("222", 2), ("333", 2)):
        d = tmp_path / run / f"meas-desktop-element-r{k}-full"
        d.mkdir(parents=True)
        (d / "report.json").write_text(json.dumps({"gate": "open"}))
        (d / "spec.json").write_text(json.dumps({"cpu_model": "AMD EPYC 7763", "github_run": {"GITHUB_RUN_ID": run}}))
    runs, _, _, _ = pool.find_runs(str(tmp_path), "EPYC 7763")
    assert sorted(runs["element"], key=pool.repeat_order) == [1, "2@222", "2@333"]


def test_each_selected_component_carries_its_pooled_tables(tmp_path):
    # D10: the entries carry a gap and a run quantile table per component; the pool builds them from every
    # repeat's samples together
    procs = [{"pid": 100, "comm": "element", "cmd": "/usr/bin/element-desktop"}]
    rows = ("   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
            + "".join(f"   {t:.6f} [0003]  element[100/100]    0.000      0.001      1.000      S\n" for t in (1, 2, 3, 4, 5))
            + "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    wakeups = "".join(f"   {t - 0.01:.6f} [0001]  x[9]  awakened: element[100/100]\n" for t in (1, 2, 3, 4, 5))
    reps = {}
    for k in (1, 2):
        d = tmp_path / f"r{k}"
        d.mkdir()
        _run_dir(d, "element", "idle", procs, rows, wakeups)
        reps[k] = {"dir": str(d), "mode": "full", "report": {}, "spec": {}}
    e = pool.pool_app("element", reps)
    t = e["phases"]["idle"]["tables"]
    assert set(t) == set(e["phases"]["idle"]["components"]["selected"]) and t
    assert all(v["gap_ms"]["q"] and v["run_ms"]["q"] for v in t.values())


def test_a_renderer_entry_counts_its_coverage_per_renderer(tmp_path):
    # the fidelity fix: a renderer entry's rates and coverage are ONE renderer's (the mean over those measured), not
    # the total over the N renderers
    procs = [{"pid": p, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=renderer"} for p in (200, 300)]
    times = {(201, 200, "chrome"): (1.0, 2.0, 3.0), (202, 200, "Quiet"): (5.0,),
             (301, 300, "chrome"): (1.5, 2.5, 3.5), (302, 300, "Quiet"): (6.0,)}
    rows = "   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
    rows += "".join(f"   {t + 0.001:.6f} [0003]  {c}[{tid}/{pid}]    0.000      0.001      1.000      S\n"
                    for (tid, pid, c), ts in times.items() for t in ts)
    rows += "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n"
    wakeups = "".join(f"   {t - 0.01:.6f} [0001]  x[9]  awakened: {c}[{tid}/{pid}]\n"
                      for (tid, pid, c), ts in times.items() for t in ts)
    reps = {}
    for k in range(1, 3):
        d = tmp_path / f"r{k}"
        d.mkdir()
        _run_dir(d, "chrome-visible", "steady-notimer", procs, rows, wakeups)
        reps[k] = {"dir": str(d), "mode": "full", "report": {}, "spec": {}}
    comps = pool.pool_app("chrome-visible", reps)["phases"]["steady-notimer"]["components"]
    assert comps["total_wakes_per_s"] == pytest.approx(4 / 10.0, rel=1e-3)   # one renderer: 3 + 1 wakes in 10 s


def test_a_renderer_thread_that_wakes_twice_across_the_renderers_is_carried(tmp_path):
    # the fidelity fix, 인지오's decision: a renderer entry carries a thread that wakes at least twice across the
    # renderers measured in every repeat — once in each of two renderers — though one renderer wakes it once
    procs = [{"pid": p, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=renderer"} for p in (200, 300)]
    times = {(201, 200, "chrome"): (1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8), (202, 200, "Quiet"): (5.0,),
             (301, 300, "chrome"): (1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9), (302, 300, "Quiet"): (6.0,)}
    rows = "   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
    rows += "".join(f"   {t + 0.001:.6f} [0003]  {c}[{tid}/{pid}]    0.000      0.001      1.000      S\n"
                    for (tid, pid, c), ts in times.items() for t in ts)
    rows += "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n"
    wakeups = "".join(f"   {t - 0.01:.6f} [0001]  x[9]  awakened: {c}[{tid}/{pid}]\n"
                      for (tid, pid, c), ts in times.items() for t in ts)
    reps = {}
    for k in range(1, 3):
        d = tmp_path / f"r{k}"
        d.mkdir()
        _run_dir(d, "chrome-visible", "steady-notimer", procs, rows, wakeups)
        reps[k] = {"dir": str(d), "mode": "full", "report": {}, "spec": {}}
    comps = pool.pool_app("chrome-visible", reps)["phases"]["steady-notimer"]["components"]
    assert comps["selected"] == ["chrome", "Quiet"]
