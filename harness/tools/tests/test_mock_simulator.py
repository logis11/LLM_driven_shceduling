"""The mock simulator (8.5 spec, decisions 17–19): the unit-run generator on a
hand workload and over the whole coreset, the replay of the fixture traces,
and the command."""

import gzip
import json
import subprocess
import sys

import pytest

from conftest import FIXTURES, REPO, TOOLS
from harness.grader import read_driver_table
from harness.primitives import compute
from harness.reader import read_config_schedule, read_run_file, read_trace
from harness.records import build
from mocks import daemon, simulator
from mocks.simulator import MockSimulatorError

BUILD = REPO / "dataset" / "build" / "coreset-single"
PRIOR = REPO / "daemon" / "driver-table" / "prior.yaml"
BOOT = REPO / "harness" / "boot-defaults" / "ostep.json"
SCRIPT = TOOLS / "tests" / "mocks" / "mock_simulator.py"

needs_build = pytest.mark.skipif(not BUILD.exists(), reason="compiled coreset absent")

MLFQ = {"algorithm": "MLFQ",
        "params": {"num_queues": 3, "timeslice_us": 10000, "timeslice_growth": 2,
                   "boost_interval_us": 100000},
        "batch_bandwidth_cap": None}
EDF = {"algorithm": "EDF", "params": {"residual_timeslice_us": 10000}, "batch_bandwidth_cap": 0.3}
FIFO = {"algorithm": "FIFO", "params": {}, "batch_bandwidth_cap": 0.5}

TINY = {
    "meta": {"id": "tiny"},
    "ground_truth": [],
    "events": [
        {"op": "arrive", "t": 0, "id": "editor", "name": "code", "depart": 1000,
         "program": [{"op": "WAIT", "channel": "input:editor"}, {"op": "RUN", "us": 10}]},
        {"op": "arrive", "t": 0, "id": "game.chain.1", "name": "game.exe", "depart": 1000,
         "program": [{"op": "LOOP", "count": "unbounded", "body": [
             {"op": "TIMER", "period_us": 300}, {"op": "RUN", "us": 5},
             {"op": "WAKE", "target": "game.chain.2"}]}]},
        {"op": "arrive", "t": 0, "id": "game.chain.2", "name": "game.exe", "depart": 1000,
         "program": [{"op": "LOOP", "count": "unbounded", "body": [
             {"op": "WAIT", "channel": "chain:2"}, {"op": "RUN", "us": 5}]}]},
        {"op": "arrive", "t": 100, "id": "batch", "name": "python3",
         "program": [{"op": "RUN", "us": 50}, {"op": "EXIT"}]},
        {"op": "arrive", "t": 200, "id": "build", "name": "make", "fork_cap": 2,
         "program": [{"op": "RUN", "us": 1}, {"op": "FORK"}, {"op": "RUN", "us": 1},
                     {"op": "FORK"}, {"op": "EXIT"}],
         "spawn_table": [{"id": "build.c1", "name": "cc1",
                          "program": [{"op": "RUN", "us": 3}, {"op": "EXIT"}]},
                         {"id": "build.c2", "name": "cc1",
                          "program": [{"op": "RUN", "us": 3}, {"op": "EXIT"}]}]},
        {"op": "wake", "t": 500, "channel": "input:editor", "target": "editor"},
        {"op": "wake", "t": 500, "channel": "input:editor", "target": "editor"},
        {"op": "wake", "t": 700, "channel": "input:editor", "target": "editor"},
    ],
}

SCHEDULE = {"workload_id": "tiny", "condition": "oracle", "schedule": [
    {"t_us": 0, "config": MLFQ, "provenance": "fallback"},
    {"t_us": 0, "config": EDF, "provenance": "unmodified"},
    {"t_us": 400, "config": FIFO, "provenance": "unmodified"},
    {"t_us": 1000, "config": FIFO, "provenance": "unmodified"},     # at T_end: ignored
]}


def _write(tmp_path, doc, name):
    p = tmp_path / name
    p.write_text(json.dumps(doc))
    return p


def _lines(tmp_path, doc=TINY, schedule=SCHEDULE):
    out = tmp_path / "trace.jsonl"
    simulator.generate(_write(tmp_path, doc, "w.json"), _write(tmp_path, schedule, "s.json"), out)
    return out, [json.loads(l) for l in out.read_text().splitlines()]


def _of(lines, task, event):
    return [l for l in lines if l.get("task") == task and l["event"] == event]


# ------------------------------------------------------------ the generator

def test_header_and_config_lines(tmp_path):
    out, lines = _lines(tmp_path)
    assert lines[0] == {"event": "meta", "workload_id": "tiny", "condition": "oracle",
                        "sim": simulator.SIM, "schedule_entries": 4}
    applied = [l for l in lines if l["event"] == "config_applied"]
    assert applied == [
        {"event": "config_applied", "t": 0, "index": 0, "algorithm": "MLFQ", "provenance": "fallback"},
        {"event": "config_applied", "t": 0, "index": 1, "algorithm": "EDF", "provenance": "unmodified"},
        {"event": "config_applied", "t": 400, "index": 2, "algorithm": "FIFO", "provenance": "unmodified"},
    ]
    assert [l["t"] for l in lines[1:]] == sorted(l["t"] for l in lines[1:])
    trace = read_trace(out)
    assert sum(1 for _ in trace) == len(lines) - 1


def test_one_unit_run_per_stimulus(tmp_path):
    _, lines = _lines(tmp_path)
    # segment-bound editor: arrival, two queued wakes at one instant, one wake, the depart
    assert [(l["t"], l["cause"]) for l in _of(lines, "editor", "ready")] == \
        [(0, "arrive"), (500, "wake"), (500, "wake"), (700, "wake")]
    assert [l["t"] for l in _of(lines, "editor", "run_start")] == [0, 500, 700]
    assert [(l["t"], l["reason"], l["blocked_on"]) for l in _of(lines, "editor", "run_end")] == \
        [(1, "block", "wait"), (501, "block", "wait"), (701, "block", "wait")]
    assert _of(lines, "editor", "task_end") == [{"event": "task_end", "t": 1000, "task": "editor",
                                                 "reason": "depart"}]
    # finite batch task: exits after its first run
    assert _of(lines, "batch", "task_arrive") == [{"event": "task_arrive", "t": 100, "task": "batch",
                                                   "source": "file"}]
    assert _of(lines, "batch", "run_end") == [{"event": "run_end", "t": 101, "task": "batch",
                                               "reason": "exit"}]
    assert _of(lines, "batch", "task_end") == [{"event": "task_end", "t": 101, "task": "batch",
                                                "reason": "exit"}]
    # periodic head: ticks on its grid before the depart, met deadlines
    assert [(l["t"], l["cause"]) for l in _of(lines, "game.chain.1", "ready")] == \
        [(0, "arrive"), (0, "timer_tick"), (300, "timer_tick"), (600, "timer_tick"), (900, "timer_tick")]
    assert [l["t"] for l in _of(lines, "game.chain.1", "run_start")] == [0, 300, 600, 900]
    assert [(l["t"], l["reason"], l["blocked_on"]) for l in _of(lines, "game.chain.1", "run_end")] == \
        [(1, "block", "timer"), (301, "block", "timer"), (601, "block", "timer"), (901, "block", "timer")]
    assert _of(lines, "game.chain.1", "deadline") == [
        {"event": "deadline", "t": t + 1, "task": "game.chain.1", "due": t + 300, "met": True,
         "slack_us": 299} for t in (0, 300, 600, 900)]
    # chain stage: woken at each tick
    assert [(l["t"], l["cause"]) for l in _of(lines, "game.chain.2", "ready")] == \
        [(0, "arrive"), (0, "wake"), (300, "wake"), (600, "wake"), (900, "wake")]
    assert _of(lines, "game.chain.2", "deadline") == []
    # orchestrator and children: children arrive with the parent, every one exits
    assert _of(lines, "build.c1", "task_arrive") == [{"event": "task_arrive", "t": 200,
                                                      "task": "build.c1", "source": "spawn",
                                                      "parent": "build"}]
    for tid in ("build", "build.c1", "build.c2"):
        assert [l["t"] for l in _of(lines, tid, "task_end")] == [201]
    assert not any(l["event"] == "run_end" and l["reason"] == "preempt" for l in lines)


def test_same_instant_order_is_config_arrivals_then_the_rest(tmp_path):
    _, lines = _lines(tmp_path)
    at0 = [l["event"] for l in lines if l.get("t") == 0]
    assert at0[:2] == ["config_applied", "config_applied"]
    assert at0[2:5] == ["task_arrive"] * 3
    # a run closing at t precedes a run opening at t (the 500 µs wake follows no run, so use 1)
    doc = json.loads(json.dumps(TINY))
    doc["events"].append({"op": "wake", "t": 1, "channel": "input:editor", "target": "editor"})
    _, lines = _lines(tmp_path, doc)
    at1 = [l["event"] for l in lines if l.get("task") == "editor" and l["t"] == 1]
    assert at1 == ["run_end", "ready", "run_start"]


def test_records_build_is_consistent_on_the_hand_workload(tmp_path):
    out, _ = _lines(tmp_path)
    rows, messages = build(tmp_path / "w.json", out, schedule_path=tmp_path / "s.json")
    assert messages == []
    by = {(r["entity"], r["metric"], r["t"]): r for r in rows}
    assert by[("lane", "busy", 1000)]["value"] == 3 + 4 + 4 + 1 + 1 + 2
    assert [by[("game.chain.1", "job", t)]["value"] for t in (0, 300, 600, 900)] == [1, 1, 1, 1]
    assert by[("batch", "completed", 101)]["value"] == 1
    assert by[("batch", "turnaround", 101)]["value"] == 1
    assert by[("build", "turnaround", 201)]["value"] == 1
    assert [r["value"] for r in rows if r["metric"] == "config_interval"] == [0, 400, 600]
    switches = [r for r in rows if r["metric"] == "switch_window"]
    assert [(r["index"], r["value"], r["hogs"]) for r in switches] == [(1, 0, 0), (2, 0, 0)]
    assert all(r["value"] == 0 for r in rows if r["metric"] == "ready_wait")


def test_generation_is_byte_identical_across_reruns(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    a, _ = _lines(tmp_path / "a")
    b, _ = _lines(tmp_path / "b")
    assert a.read_bytes() == b.read_bytes()


def test_gzip_when_the_output_path_says_so(tmp_path):
    out = tmp_path / "trace.jsonl.gz"
    simulator.generate(_write(tmp_path, TINY, "w.json"), _write(tmp_path, SCHEDULE, "s.json"), out)
    with gzip.open(out, "rt") as f:
        assert json.loads(f.readline())["event"] == "meta"
    assert sum(1 for _ in read_trace(out)) > 0


def test_contract_invalid_input_is_refused(tmp_path):
    w = _write(tmp_path, TINY, "w.json")
    no_boot = json.loads(json.dumps(SCHEDULE))
    no_boot["schedule"] = no_boot["schedule"][2:]
    with pytest.raises(MockSimulatorError, match="t_us"):
        simulator.generate(w, _write(tmp_path, no_boot, "s1.json"), tmp_path / "t1.jsonl")
    other = json.loads(json.dumps(SCHEDULE))
    other["workload_id"] = "elsewhere"
    with pytest.raises(MockSimulatorError, match="workload_id"):
        simulator.generate(w, _write(tmp_path, other, "s2.json"), tmp_path / "t2.jsonl")
    assert not (tmp_path / "t1.jsonl").exists() and not (tmp_path / "t2.jsonl").exists()


@needs_build
def test_every_coreset_file_flows_through_records_with_no_message(tmp_path):
    table = read_driver_table(PRIOR)
    boot = json.loads(BOOT.read_text())
    files = sorted(BUILD.glob("*.workload.json"))
    assert len(files) == 50
    for path in files:
        doc = json.loads(path.read_text())
        wid = doc["meta"]["id"]
        for condition in ("fixed", "oracle"):
            schedule, _ = daemon.run(doc, condition, table, boot)
            sp = _write(tmp_path, schedule, f"{wid}-{condition}.json")
            out = tmp_path / f"{wid}-{condition}.trace.jsonl"
            simulator.generate(path, sp, out)
            run = read_run_file(path)
            result = compute(run, read_trace(out), read_config_schedule(sp))
            assert result.guards == [], (wid, condition, result.guards)     # tick_count
            busy = next(r["value"] for r in result.rows
                        if r["entity"] == "lane" and r["metric"] == "busy")
            assert 0 < busy <= run.t_end, (wid, condition, busy, run.t_end)  # utilisation_sanity


# ------------------------------------------------------------------ replay

def _fixture_schedule(d, tmp_path):
    if (d / "config-schedule.json").exists():
        return d / "config-schedule.json"
    run = read_run_file(d / "run.json")
    return _write(tmp_path, {"workload_id": run.workload_id, "condition": "fixed",
                             "schedule": [{"t_us": 0, "config": MLFQ, "provenance": "fallback"}]},
                  f"{d.name}-schedule.json")


def test_replay_returns_each_fixture_trace_byte_for_byte(tmp_path):
    pairs = sorted(p for p in FIXTURES.iterdir() if (p / "trace.jsonl").exists())
    assert len(pairs) == 6
    for d in pairs:
        out = tmp_path / f"{d.name}.jsonl"
        simulator.generate(d / "run.json", _fixture_schedule(d, tmp_path), out,
                           replay=d / "trace.jsonl")
        assert out.read_bytes() == (d / "trace.jsonl").read_bytes(), d.name


def test_replay_refuses_a_trace_of_another_workload(tmp_path):
    d = FIXTURES / "mock-switch"
    with pytest.raises(MockSimulatorError, match="workload_id"):
        simulator.generate(d / "run.json", _fixture_schedule(d, tmp_path), tmp_path / "t.jsonl",
                           replay=FIXTURES / "mock-office" / "trace.jsonl")
    assert not (tmp_path / "t.jsonl").exists()


# ------------------------------------------------------------- the command

def test_cli_generates_and_replays_silently(tmp_path):
    w = _write(tmp_path, TINY, "w.json")
    s = _write(tmp_path, SCHEDULE, "s.json")
    proc = subprocess.run([sys.executable, str(SCRIPT), "--workload", str(w), "--schedule", str(s),
                           "--out-trace", str(tmp_path / "t.jsonl")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "" and (tmp_path / "t.jsonl").exists()
    d = FIXTURES / "mock-switch"
    proc = subprocess.run([sys.executable, str(SCRIPT), "--replay", str(d / "trace.jsonl"),
                           "--workload", str(d / "run.json"),
                           "--schedule", str(d / "config-schedule.json"),
                           "--out-trace", str(tmp_path / "r.jsonl")], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert (tmp_path / "r.jsonl").read_bytes() == (d / "trace.jsonl").read_bytes()


def test_cli_refuses_a_missing_flag_and_bad_input(tmp_path):
    w = _write(tmp_path, TINY, "w.json")
    s = _write(tmp_path, SCHEDULE, "s.json")
    for argv in (["--workload", str(w), "--out-trace", str(tmp_path / "t.jsonl")],
                 ["--workload", str(w), "--schedule", str(tmp_path / "missing.json"),
                  "--out-trace", str(tmp_path / "t.jsonl")]):
        proc = subprocess.run([sys.executable, str(SCRIPT)] + argv, capture_output=True, text=True)
        assert proc.returncode != 0 and proc.stdout == ""
        assert not (tmp_path / "t.jsonl").exists()
