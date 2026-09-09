"""The `x_mlfq_level` check tool (memo 2026-09-08 §4, ground truth): for every
switch into MLFQ, does the switch window cover the last demotion of each hog?
The tool lives beside the harness and reads the `x_` lines the reader skips."""

import json
import subprocess
import sys

from conftest import TOOLS


def run_tool(d, trace):
    cmd = [sys.executable, str(TOOLS / "check_mlfq_levels.py"),
           "--run", str(d / "run.json"), "--trace", str(trace)]
    if (d / "config-schedule.json").exists():
        cmd += ["--schedule", str(d / "config-schedule.json")]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_mock_switch_window_covers_the_hogs_last_demotion(fixture_dir):
    # lane-time window [40600, 53100]: the hog's 1→2 demotion at 53100 is its edge
    d = fixture_dir("mock-switch")
    p = run_tool(d, d / "trace.jsonl")
    assert p.returncode == 0, p.stdout + p.stderr
    assert "index 2" in p.stdout and "hog" in p.stdout and "53100" in p.stdout
    assert "not covered" not in p.stdout and "all covered" in p.stdout


def test_a_demotion_past_the_window_is_reported(fixture_dir, tmp_path):
    # a simulator whose hog reaches the bottom later than its CPU accounting says
    d = fixture_dir("mock-switch")
    lines = (d / "trace.jsonl").read_text().splitlines()
    out = []
    for line in lines:
        obj = json.loads(line)
        if obj.get("event") == "x_mlfq_level" and obj["t"] == 53100:
            obj["t"] = 55000                       # still before the 60600 boost line
        out.append(json.dumps(obj, separators=(",", ":")))
    trace = tmp_path / "trace.jsonl"
    trace.write_text("\n".join(out) + "\n")
    p = run_tool(d, trace)
    assert p.returncode == 1, p.stdout + p.stderr
    assert "55000" in p.stdout and "not covered" in p.stdout


def test_trace_without_a_switch_into_mlfq_has_nothing_to_check(fixture_dir):
    d = fixture_dir("mock-p1a")             # MLFQ → MLFQ only, no schedule needed
    p = run_tool(d, d / "trace.jsonl")
    assert p.returncode == 0
    assert "no switch into MLFQ" in p.stdout


def test_switch_into_mlfq_without_a_schedule_exits_2(fixture_dir, tmp_path):
    d = fixture_dir("mock-switch")
    p = subprocess.run([sys.executable, str(TOOLS / "check_mlfq_levels.py"),
                        "--run", str(d / "run.json"), "--trace", str(d / "trace.jsonl")],
                       capture_output=True, text=True)
    assert p.returncode == 2
    assert "no config schedule given" in p.stdout
