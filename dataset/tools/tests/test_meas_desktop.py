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
    # D13: the renderer-only view keeps what an exclude_roles=("renderer",) filter would drop, so the same code
    # computes the components of every Chrome measurement. The browser process and the GPU
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


def test_each_subject_s_build_is_read_from_the_key_its_job_records():
    # 9.5 D69 in 9.8 D31's census: Chrome records `version`, Element `element.version`, the Steam client `steam.buildid`
    assert pool.build_of("chrome-hidden", {"version": "Google Chrome 153.0.8010.52"}) == "Google Chrome 153.0.8010.52"
    assert pool.build_of("element", {"element.version": "1.12.28", "version": None}) == "Element 1.12.28"
    assert pool.build_of("steam", {"steam.buildid": "1788652215"}) == "Steam client build 1788652215"
    assert pool.build_of("steam", {}) is None


def test_a_shaped_phase_is_invalid_when_its_shaper_did_not_install_or_carried_too_little(repo_root):
    # 9.7 D27: every phase run under shape_on records its shaper installed, and its bytes through ifb0 are at least 90 %
    # of the bytes received; before, a phase whose shaper failed recorded no bytes and no rule read it
    pr = _pool_runs(repo_root)
    ok = {"shape.steam-fresh-shaped": "1", "shape.steam-fresh-shaped.through_ifb_bytes": "950",
          "net.steam-fresh-shaped.rx_bytes": "1000", "shape.steam-fresh-unshaped": "0"}
    assert pr.shaping_notes(ok) == []
    assert pr.shaping_notes({**ok, "shape.steam-fresh-untraced": "0"}) == ["steam-fresh-untraced not shaped: the shaper did not install"]
    assert pr.shaping_notes({**ok, "shape.steam-fresh-shaped.through_ifb_bytes": "800"}) == [
        "steam-fresh-shaped not shaped: 800 B through ifb0 of 1000 B received"]


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


def _table(means, n=10):
    """A pooled table's per-repeat fields, each repeat holding n samples."""
    return {"repeat_mean": list(means), "repeat_n": [n] * len(means)}


def _entry(threads, residual=None, phase="idle"):
    # the pooled tables the rule reads beside the per-repeat thread records, ten samples a repeat
    tables = {c: {f: _table([x["mean"] for x in t[f]]) for f in ("gap_ms", "run_ms")} for c, t in threads.items()}
    if residual:
        residual = {k: ({**v, "repeat_n": [10] * len(v["repeat_mean"])} if isinstance(v, dict) and "repeat_n" not in v
                        else v) for k, v in residual.items()}
    return {"phases": {phase: {"threads": threads, "tables": tables,
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


def test_the_rule_reads_a_components_mean_as_its_pooled_table_carries_it():
    # the carried gap and run tables pool every repeat's samples, so their means are count-weighted: a repeat whose
    # run mean is ten times the others' but which holds one wake of 4001 moves the carried mean to 0.0501 ms and
    # holds within ±0.8 %, where its per-repeat means, 0.05 four times and 0.5, would read ±178 %
    entry = _entry({"a": _comp([4.0] * 5, [250.0] * 5, [0.05, 0.05, 0.05, 0.05, 0.50])})
    entry["phases"]["idle"]["tables"]["a"]["run_ms"]["repeat_n"] = [1000, 1000, 1000, 1000, 1]
    c = pool.criterion("element", entry)["quantities"]["idle a run mean (ms)"]
    assert c["mean"] == pytest.approx(200.5 / 4001, abs=1e-4) and c["half_width"] < 0.01 and c["passes"] is True


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


def test_the_renderer_residuals_carry_as_sparse_components():
    # changelog D27: a renderer's residual wakes a few times per renderer per phase (hidden: `MemoryInfra` alone,
    # 1.2–3.4 wakes; visible: four comms, 3.6–5.5), a count whose spread is the count's own — the within-run test
    # cannot place it, so 9.5 D57 does not apply. It is carried with its half-widths and its count, its three
    # values together, over at least five repeats, and is no longer a between-sessions component.
    res = {"wakes_per_s": [0.0031, 0.0057, 0.0021, 0.0050, 0.0029],
           "gap_ms": {"repeat_mean": [320000.0, 175000.0, 480000.0, 200000.0, 345000.0]},
           "run_ms": {"repeat_mean": [0.15, 0.26, 0.17, 0.19, 0.20]}}
    steady = _comp([4.0] * 5, [250.0] * 5, [0.05] * 5)
    for app, phase in (("chrome-hidden", "steady"), ("chrome-visible", "steady-notimer")):
        q = pool.criterion(app, _entry({"HangWatcher": steady}, res, phase=phase))
        for label in ("wakes/s", "gap mean (ms)", "run mean (ms)"):
            c = q["quantities"][f"{phase} residual {label}"]
            assert c["passes"] is False and c["sparse"] is True and c["session_spread"] is False
            assert c["carried"] is True
        assert q["passes"] is True
    # not with fewer than five repeats behind it
    short = {k: (v[:4] if k == "wakes_per_s" else {"repeat_mean": v["repeat_mean"][:4]}) for k, v in res.items()}
    steady4 = _comp([4.0] * 4, [250.0] * 4, [0.05] * 4)
    assert pool.criterion("chrome-hidden", _entry({"HangWatcher": steady4}, short, phase="steady"))["passes"] is False
    # no other subject's residual is sparse, and no named renderer thread is
    q = pool.criterion("element", _entry({"HangWatcher": steady}, res))
    assert q["quantities"]["idle residual wakes/s"]["sparse"] is False and q["passes"] is False
    q = pool.criterion("chrome-hidden", _entry({"Chrome_ChildIOT": _comp(res["wakes_per_s"], [250.0] * 5,
                                                                          [0.03] * 5)}, phase="steady"))
    c = q["quantities"]["steady Chrome_ChildIOT wakes/s"]
    assert c["sparse"] is False and c["session_spread"] is True


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


def test_the_steam_clients_http_burst_leaves_its_component_as_a_stated_event(tmp_path):
    # changelog D33, 9.5 D64: CHTTPClientThre's runs of 1 ms or more leave the component and are stated beside it, in
    # seconds into the phase; its other runs are the component. D30's between-sessions carry is withdrawn with it.
    procs = [{"pid": 100, "comm": "steam", "cmd": "/home/runner/.local/share/Steam/ubuntu12_32/steam"}]
    rows = ("   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
            "   1.000000 [0003]  CHTTPClientThre[101/100]    0.000      0.001      0.015      S\n"
            "   2.000000 [0003]  CHTTPClientThre[101/100]    0.000      0.001      20.000      S\n"
            "   2.100000 [0003]  CHTTPClientThre[101/100]    0.000      0.001      5.000      S\n"
            "   3.000000 [0003]  CHTTPClientThre[101/100]    0.000      0.001      0.017      S\n"
            "  10.000100 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    # one wakeup before each schedule-in (a row's t_in is its time minus its run), so each row is a wake of its own
    wakeups = "".join(f"   {t:.6f} [0001]  x[9]  awakened: CHTTPClientThre[101/100]\n" for t in (0.99, 1.97, 2.09, 2.99))
    for phase in ("shown", "minimised"):   # both sides of D5's comparison read the same way
        (tmp_path / phase).mkdir()
        d = _run_dir(tmp_path / phase, "steam", phase, procs, rows, wakeups)
        ph = analyze.analyze_run_dir(str(d))["phases"][phase]
        assert round(ph["threads"]["CHTTPClientThre"]["run_ms"]["sum"], 3) == 0.032
        assert [run for _, run in ph["events"]] == [20.0, 5.0]
        assert all(0 <= t <= ph["span_s"] for t, _ in ph["events"])
    assert "steam" not in pool.SESSION_SPREAD


def test_the_game_client_carries_the_http_burst_as_a_heavy_event(repo_root, tmp_path):
    # changelog D33: the fold-in emits the event as 9.5's web-browser carries its MemoryInfra pass — the runs' table,
    # count, span and rate — and the scope states it where D30's two modes stood
    import sys
    from meas.desktop import fold_in
    out = tmp_path / "fold.yaml"
    pooled = repo_root / "_dev" / "research" / "jioh" / "task-9.8-browser-comms" / "campaign" / "results" / "pooled.json"
    argv, sys.argv = sys.argv, ["fold_in.py", str(pooled), str(out)]
    try:
        fold_in.main()
    finally:
        sys.argv = argv
    import yaml
    entry = yaml.safe_load("archetypes:\n" + out.read_text())["archetypes"]["game-client"]
    ev = entry["params"]["heavy_events"]
    assert [e["comm"] for e in ev] == ["CHTTPClientThre"] and ev[0]["run_floor_ms"] == 1 and ev[0]["count"] == 62
    assert abs(ev[0]["rate_per_s"] - 62 / ev[0]["span_s"]) < 1e-6 and "gap" not in ev[0]
    scope = entry["validation_stats"]["scope"]
    assert "A rare event within a run (9.5 D64; D33): `CHTTPClientThre`'s runs of 1 ms or more" in scope
    assert "in 4 of the repeats (4, 5, 6, 12)" in scope and "two modes" not in scope


def test_the_build_census_orders_repeats_keyed_by_landing():
    # 9.5 D69 in 9.8: an index that landed more than once is keyed "<index>@<run id>" (D24); the census counts every
    # landing and orders by the index
    census = pool._cp.build_census({"1": "Chrome 152", "10@35585759158": "Chrome 152", "10@35586632429": "Chrome 152",
                                    "12": "Chrome 153", "2": "Chrome 152"})
    assert census == "Chrome 152 (4 repeats), Chrome 153 (1: 12)"


def test_the_fold_in_regenerates_the_library_s_entries_from_the_pooled_record(repo_root, tmp_path):
    # the entries in archetypes.yaml are fold_in.py's output on the committed pooled record, byte for byte, with the
    # untraced control's reading in their notes (the 9.5 untraced-control spec, decision 20)
    import sys
    from meas.desktop import fold_in
    campaign = repo_root / "_dev" / "research" / "jioh" / "task-9.8-browser-comms" / "campaign"
    pooled, control = campaign / "results" / "pooled.json", campaign / "results-control" / "control.json"
    out = tmp_path / "fold.yaml"
    argv, sys.argv = sys.argv, ["fold_in.py", str(pooled), str(out), "--control", str(control)]
    try:
        fold_in.main()
    finally:
        sys.argv = argv
    fragment = out.read_text().rstrip("\n")
    entries = fragment[fragment.index("\n  renderer-hidden:\n"):]   # the library holds the entries, not the fold's header
    assert entries in (repo_root / "dataset" / "archetypes.yaml").read_text()
    for app in fold_in.FOLDED:
        assert f"\n  {fold_in.IDS[app]}:\n" in fragment
    assert "\n  renderer-visible:\n" not in fragment   # 9.10 D16: bound nowhere, out of the library


def test_the_renderer_scopes_state_the_chrome_builds_they_pool(repo_root, tmp_path):
    # 9.5 D69: Google's repository serves only its current Chrome, so the build is recorded per repeat and the census
    # stated in the observed line; the hidden renderer's added repeats (D31) ran 153
    import sys
    from meas.desktop import fold_in
    out = tmp_path / "fold.yaml"
    pooled = repo_root / "_dev" / "research" / "jioh" / "task-9.8-browser-comms" / "campaign" / "results" / "pooled.json"
    argv, sys.argv = sys.argv, ["fold_in.py", str(pooled), str(out)]
    try:
        fold_in.main()
    finally:
        sys.argv = argv
    import yaml
    doc = yaml.safe_load("archetypes:\n" + out.read_text())["archetypes"]
    hidden = doc["renderer-hidden"]["validation_stats"]["scope"]
    assert ("Google Chrome 152.0.7977.82 (14 repeats), Google Chrome 153.0.8010.52 (5: 12, 13, 14, 15, 16), "
            "launched as web-browser was") in hidden


def test_the_run_means_excepted_for_the_runner_s_speed_state_their_share_of_the_phase_s_cpu(repo_root, tmp_path):
    # D37: the workflow asks a value whose spread follows the machine to state the share of the job's time it holds
    # (9.6 D29); each excepted run mean's runs over the phase's, the heavy event's runs counted in the phase
    import sys
    from meas.desktop import fold_in
    out = tmp_path / "fold.yaml"
    pooled = repo_root / "_dev" / "research" / "jioh" / "task-9.8-browser-comms" / "campaign" / "results" / "pooled.json"
    argv, sys.argv = sys.argv, ["fold_in.py", str(pooled), str(out)]
    try:
        fold_in.main()
    finally:
        sys.argv = argv
    import yaml
    doc = yaml.safe_load("archetypes:\n" + out.read_text())["archetypes"]
    assert ("`VizCompositorTh` run mean 0.0818 ms ±5.6 % (0.066–0.089 ms). Their runs hold 32.4 %, 25.3 %, 16.8 % and "
            "5.7 % of the phase's CPU, 80.2 % together (D37).") in doc["game-client"]["validation_stats"]["scope"]
    for aid in ("renderer-hidden", "chat-client"):
        assert "Their runs hold" not in doc[aid]["validation_stats"]["scope"], aid


def test_the_renderer_mode_reads_the_probe_past_a_skip(tmp_path):
    # D38: D20, D24 and D26 read the hidden probe past its first 300 s; the renderer mode takes the skip `--tree` has
    from meas.desktop import within_run
    procs = [{"pid": 200, "comm": "chrome", "cmd": "/opt/google/chrome/chrome --type=renderer --lang=en"}]
    row = lambda t: f"{t:11.6f} [0003]  Chrome_ChildIOT[201/200]    0.000      0.001      0.010      S\n"
    rows = ("   0.000010 [0000]  perf[50]    0.000      0.000      0.010      R\n"
            + "".join(row(10.0 + i * 0.1) for i in range(100))       # a launch burst in the first 300 s
            + "".join(row(305.0 + i * 10.0) for i in range(70))      # then one wake every 10 s
            + "1000.500000 [0000]  perf[50]    0.000      0.000      0.010      R\n")
    d = _run_dir(tmp_path, "chrome-hidden", "steady", procs, rows)
    an = tmp_path / "analysis.json"
    an.write_text(json.dumps({"phases": {"steady": {"renderer_pids": [200]}}}))
    v = within_run.rates(str(d), "steady", str(an), 600.0, 100.0, {"Chrome_ChildIOT"}, skip_s=300.0)
    assert v == [pytest.approx(0.1), pytest.approx(0.1)]   # two positions from 300 s, the burst left out
    assert len(within_run.rates(str(d), "steady", str(an), 600.0, 100.0, {"Chrome_ChildIOT"})) == 5


def test_the_steam_client_carries_no_other_component_between_sessions():
    # changelog D26: over merged wake times steamwebhelper's and ThreadPoolForeg's gap means hold the rule, so of D23's
    # two components carried between sessions only steamwebhelper's run mean stays carried, under D18
    wild_gap = _comp([70.0] * 5, [29.0, 29.0, 42.0, 29.0, 41.0], [0.05] * 5)
    q = pool.criterion("steam", _entry({"steamwebhelper": wild_gap}, phase="shown"))
    assert q["quantities"]["shown steamwebhelper gap mean (ms)"]["carried"] is False and q["passes"] is False
    wide_run = _comp([70.0] * 5, [29.0] * 5, [0.068, 0.047, 0.049, 0.065, 0.062])
    c = pool.criterion("steam", _entry({"steamwebhelper": wide_run}, phase="shown"))["quantities"]
    run = c["shown steamwebhelper run mean (ms)"]
    assert run["excepted"] is True and run["session_spread"] is False and run["carried"] is True


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


# ---- 9.10 D126–D129: the tab set whose renderers are counted ----------------------------------------------------

from meas.desktop import tabs  # noqa: E402


def test_the_tab_subject_s_two_launches_differ_by_the_spare_flag_alone(repo_root):
    # D128: the spare-off launch is the renderer subjects' CHROME, the spare-on launch the same with that one flag
    # taken off — the `chrome` arm's flags, which test_the_three_chrome_arms_launch_with_identical_flags ties to it
    src = (repo_root / "dataset" / "tools" / "meas" / "probe" / "appdefs.sh").read_text()
    off = re.search(r'^\s*LAUNCH_OFF="\$CHROME (\S+)"', src, re.M)
    on = re.search(r'^\s*LAUNCH_ON="\$\{CHROME% --disable-features=SpareRendererForSitePerProcess\} (\S+)"', src, re.M)
    assert off and on, "expected LAUNCH_OFF from $CHROME and LAUNCH_ON from $CHROME less the spare flag"
    assert off.group(1) == on.group(1), "the two launches open the same tabs"
    assert off.group(1).startswith("http://127.0.0.1:$PORT/idle-page.html?$PAGEQ$URLS")


def test_the_tab_set_is_five_tabs_in_every_mode(repo_root):
    # D15: the page in use and four others; a dry run shortens the phases, never the tab set
    src = (repo_root / "dataset" / "tools" / "meas" / "desktop" / "run.sh").read_text()
    assert re.search(r"^TAB_ORIGINS=4\b", src, re.M)
    dry = re.search(r'^if \[ "\$MODE" = dry \]; then\n(.*?)\n', src, re.M).group(1)
    assert "TAB_ORIGINS" not in dry
    body = re.search(r"^tabs_subject\(\) \{(.*?)^\}", src, re.S | re.M).group(1)
    assert 'MEAS_ORIGINS="$TAB_ORIGINS"' in body


def test_the_listing_reads_a_renderer_s_role_as_the_renderer_analysis_does():
    base = ["/opt/google/chrome/chrome", "--type=renderer", "--user-data-dir=/tmp/chrome-data"]
    assert tabs.role_of(base) == ("renderer", "plain")
    assert tabs.role_of(base + ["--top-chrome-webui"]) == ("renderer", "webui")
    assert tabs.role_of(base + ["--extension-process"]) == ("renderer", "extension")
    assert tabs.role_of(["/opt/google/chrome/chrome", "--type=gpu-process"]) == ("gpu-process", "")
    assert tabs.role_of(["/opt/google/chrome/chrome", "--user-data-dir=/tmp/chrome-data"]) == ("browser", "")
    assert {f for f, _ in tabs.OWN} == set(analyze.NOT_PAGE_RENDERER)


def test_the_listing_reads_proc_and_leaves_out_what_does_not_hold_the_pattern(tmp_path):
    def proc(pid, ppid, argv, threads=7, start=100, ut=3, st=2):
        d = tmp_path / str(pid)
        d.mkdir()
        (d / "cmdline").write_bytes(b"\0".join(a.encode() for a in argv) + b"\0")
        f = ["S", ppid] + [0] * 9 + [ut, st] + [0] * 4 + [threads, 0, start] + [0] * 30   # fields 3, 4, 5–13, 14–15, 16–19, 20–22
        (d / "stat").write_text(f"{pid} (chrome) " + " ".join(str(x) for x in f))
    proc(10, 1, ["/opt/google/chrome/chrome", "--user-data-dir=/tmp/chrome-data"])
    proc(11, 10, ["/opt/google/chrome/chrome", "--type=renderer", "--user-data-dir=/tmp/chrome-data",
                  "--renderer-client-id=6"], threads=12, start=150)
    proc(12, 1, ["/usr/bin/python3", "-m", "http.server"])
    # a renamed child: Chrome rewrites its title, and the cmdline is one string with the arguments joined by spaces
    proc(13, 10, ["/opt/google/chrome/chrome --type=renderer --top-chrome-webui --user-data-dir=/tmp/chrome-data"])
    got = tabs.listing("chrome-data", proc=str(tmp_path))
    assert [p[0] for p in got] == [10, 11, 13]
    assert tabs.role_of(got[2][2]) == ("renderer", "webui")
    assert got[1][1:2] == (10,) and got[1][3:] == (150, 12, 5)
    row = list(tabs.rows("off", "steady", 0, got, 2_000_000_000))[1]
    assert row == ("off", "steady", "2.0", 11, 10, "renderer", "plain", "6", 150, 12, 5)


def _tabs_rows(arm, phase, t, plain, webui=1, extension=0, first_pid=100):
    out, pid = [], first_pid
    for role, n in (("plain", plain), ("webui", webui), ("extension", extension)):
        for _ in range(n):
            out.append(dict(zip(tabs.COLUMNS, (arm, phase, str(t), str(pid), "1", "renderer", role, "", "0", "1", "0"))))
            pid += 1
    out.append(dict(zip(tabs.COLUMNS, (arm, phase, str(t), "1", "0", "browser", "", "", "0", "1", "0"))))
    return out


def test_the_summary_reads_the_spare_as_the_two_launches_difference():
    # D127, D128: the spare-off launch's plain renderers are pages, the page in use one of them; what the spare-on
    # launch holds beyond them is the spare. Extension renderers that leave before the steady phase are recorded.
    rs = []
    for t in (10.0, 20.0):
        rs += _tabs_rows("off", "launch-settle", t, plain=5, extension=2)
        rs += _tabs_rows("on", "launch-settle", t, plain=6, extension=2, first_pid=200)
    for t in (650.0, 660.0, 1250.0):
        rs += _tabs_rows("off", "steady", t, plain=5)
        rs += _tabs_rows("on", "steady", t, plain=6, first_pid=200)
    k = tabs.summary(rs)
    assert k["tabs.hidden"] == 4 and k["tabs.spare"] == 1
    assert k["tabs.off.steady.plain_pids_stable"] == 1 and k["tabs.on.steady.plain_pids_stable"] == 1
    assert k["tabs.off.launch-settle.extension_max"] == 2 and k["tabs.off.steady.extension_max"] == 0
    assert k["tabs.off.steady.webui_max"] == 1 and k["tabs.off.plain_reached_s"] == 10.0


def test_a_steady_phase_whose_count_moves_carries_no_count():
    rs = _tabs_rows("off", "steady", 650.0, plain=5) + _tabs_rows("off", "steady", 660.0, plain=4)
    k = tabs.summary(rs)
    assert "tabs.hidden" not in k and k["tabs.off.steady.plain_min"] == 4 and k["tabs.off.steady.plain_max"] == 5


def test_the_tab_count_holds_only_when_every_repeat_has_one_count():
    def rep(hidden, spare):
        return {"mode": "full", "spec": {}, "report": {"tabs.hidden": hidden, "tabs.spare": spare}}
    e = tabs.pool({k: rep("4", "1") for k in range(1, 6)})
    assert e["hidden"] == ["4"] and e["spare"] == ["1"]
    assert e["stability"]["passes"] and e["stability"]["half_width"] == 0
    assert not tabs.pool({k: rep("4", "1") for k in range(1, 5)})["stability"]["passes"], "five repeats at least"
    e = tabs.pool({**{k: rep("4", "1") for k in range(1, 5)}, 5: rep("4", "0")})
    assert not e["stability"]["passes"] and e["stability"]["half_width"] is None and e["spare"] == ["0", "1"]
    assert "| 5 |" in "\n".join(tabs.render("chrome-tabs", e))
