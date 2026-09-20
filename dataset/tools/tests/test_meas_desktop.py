"""Constructed cases for the 9.8 desktop campaign tools (changelog D13)."""

import json
import re

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
    assert arm[0] == var[0], f"chrome arm {arm[0]} != chrome-hidden/chrome-visible {var[0]}"
    assert "--no-sandbox" in arm[0], "the flag is kept and stated (D13 corrects D12's claim that it is avoided)"


def test_the_page_times_out_of_a_nesting_level_and_does_no_work_per_wake(repo_root):
    # D13 / decision 7: setInterval, not a one-shot setTimeout — intensive throttling applies only to timers with
    # a high nesting level — and a callback that increments a counter and returns, so the entries are floors.
    page = (repo_root / "dataset" / "tools" / "meas" / "probe" / "idle-page.html").read_text()
    assert "setInterval(" in page and "setTimeout(" not in page
    body = re.search(r"setInterval\(function \(\) \{(.*?)\}", page, re.S).group(1)
    assert body.strip() == "n++;", f"the callback must do nothing but count, found {body.strip()!r}"


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
    assert ph["threads"]["chrome"]["wakes_per_s"] == round(2 / ph["span_s"], 2)
    assert ph["threads"]["chrome"]["run_ms"]["sum"] == 4.0
    assert set(ph["threads"]["chrome"]) == {"threads", "wakes_per_s", "cpu_share", "gap_ms", "run_ms"}


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
