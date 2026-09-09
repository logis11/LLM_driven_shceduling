"""Trace reader and run-file reader, checked against the four mock pairs
(docs/harness/metrics.md §3; data-contracts §9 for the trace, §4 for the
run-file view)."""

import gzip
import json

import pytest

from conftest import MOCKS
from harness.reader import (RESERVED_ENTITIES, RunFileError, ScheduleError,
                            TraceError, read_config_schedule, read_run_file,
                            read_trace)


# ------------------------------------------------------------------ trace

EXPECTED_HEADER = {
    "mock-office": ("mock-office", "fixed", 1),
    "mock-media": ("mock-media", "oracle", 2),
    "mock-p1a": ("mock-p1a", "llm_vocab", 2),
    "mock-chain": ("mock-chain", "oracle", 2),
    "mock-switch": ("mock-switch", "llm_algo", 3),
}


@pytest.mark.parametrize("mock", MOCKS)
def test_header_is_captured(fixture_dir, mock):
    trace = read_trace(fixture_dir(mock) / "trace.jsonl")
    wid, cond, entries = EXPECTED_HEADER[mock]
    assert trace.meta.workload_id == wid
    assert trace.meta.condition == cond
    assert trace.meta.sim == "mock@0"
    assert trace.meta.schedule_entries == entries


def test_events_are_yielded_in_order_with_counts(fixture_dir):
    events = list(read_trace(fixture_dir("mock-media") / "trace.jsonl"))
    kinds = [e["event"] for e in events]
    assert "meta" not in kinds                      # the header is not an event
    assert kinds.count("config_applied") == 2
    assert kinds.count("task_arrive") == 3
    assert kinds.count("task_end") == 3
    assert kinds.count("ready") == 11
    assert kinds.count("deadline") == 8
    times = [e["t"] for e in events]
    assert times == sorted(times)


def test_gzip_and_plain_read_identically(fixture_dir, tmp_path):
    plain = fixture_dir("mock-chain") / "trace.jsonl"
    gz = tmp_path / "trace.jsonl.gz"
    with gzip.open(gz, "wb") as f:
        f.write(plain.read_bytes())
    assert list(read_trace(gz)) == list(read_trace(plain))
    assert read_trace(gz).meta == read_trace(plain).meta


def test_x_prefixed_lines_are_ignored(fixture_dir, tmp_path):
    src = (fixture_dir("mock-office") / "trace.jsonl").read_text().splitlines()
    src.insert(3, json.dumps({"event": "x_mlfq_boost", "t": 0, "queue": 2}))
    src.insert(9, json.dumps({"event": "x_debug", "anything": [1, 2]}))
    p = tmp_path / "trace.jsonl"
    p.write_text("\n".join(src) + "\n")
    assert list(read_trace(p)) == list(read_trace(fixture_dir("mock-office") / "trace.jsonl"))


def test_sha256_is_of_the_file_bytes(fixture_dir):
    import hashlib
    p = fixture_dir("mock-p1a") / "trace.jsonl"
    assert read_trace(p).sha256 == hashlib.sha256(p.read_bytes()).hexdigest()


def _write(tmp_path, lines):
    p = tmp_path / "trace.jsonl"
    p.write_text("\n".join(json.dumps(l) for l in lines) + "\n")
    return p


HEADER = {"event": "meta", "workload_id": "w", "condition": "fixed",
          "sim": "mock@0", "schedule_entries": 1}


def test_missing_header_is_refused(tmp_path):
    p = _write(tmp_path, [{"event": "config_applied", "t": 0, "index": 0,
                           "algorithm": "MLFQ", "provenance": "fallback"}])
    with pytest.raises(TraceError, match="line 1"):
        read_trace(p)


def test_unknown_event_type_is_refused(tmp_path):
    p = _write(tmp_path, [HEADER, {"event": "context_switch", "t": 5, "task": "a"}])
    with pytest.raises(TraceError, match="line 2"):
        list(read_trace(p))


def test_missing_required_field_is_refused(tmp_path):
    p = _write(tmp_path, [HEADER, {"event": "ready", "t": 5, "task": "a"}])  # no cause
    with pytest.raises(TraceError, match="cause"):
        list(read_trace(p))


def test_bad_enum_value_is_refused(tmp_path):
    p = _write(tmp_path, [HEADER, {"event": "run_end", "t": 5, "task": "a",
                                   "reason": "killed"}])
    with pytest.raises(TraceError, match="reason"):
        list(read_trace(p))


def test_out_of_order_line_is_refused(tmp_path):
    p = _write(tmp_path, [HEADER,
                          {"event": "task_arrive", "t": 10, "task": "a", "source": "file"},
                          {"event": "ready", "t": 9, "task": "a", "cause": "arrive"}])
    with pytest.raises(TraceError, match="line 3"):
        list(read_trace(p))


def test_reserved_task_id_in_trace_is_refused(tmp_path):
    p = _write(tmp_path, [HEADER, {"event": "task_arrive", "t": 0, "task": "lane",
                                   "source": "file"}])
    with pytest.raises(TraceError, match="reserved"):
        list(read_trace(p))


# --------------------------------------------------------------- run file

EXPECTED_T_END = {"mock-office": 60000, "mock-media": 95000,
                  "mock-p1a": 120000, "mock-chain": 50000,
    "mock-switch": 100000,
}


@pytest.mark.parametrize("mock", MOCKS)
def test_t_end_is_the_largest_pinned_time(fixture_dir, mock):
    run = read_run_file(fixture_dir(mock) / "run.json")
    assert run.workload_id == mock
    assert run.t_end == EXPECTED_T_END[mock]


def test_chain_topology_follows_wake_targets(fixture_dir):
    run = read_run_file(fixture_dir("mock-chain") / "run.json")
    assert run.chains == [["input", "engine", "display"]]
    media = read_run_file(fixture_dir("mock-media") / "run.json")
    assert sorted(media.chains) == [["music"], ["video"]]
    for mock in ("mock-office", "mock-p1a"):
        assert read_run_file(fixture_dir(mock) / "run.json").chains == []


def test_periods_are_read_for_chain_heads(fixture_dir):
    run = read_run_file(fixture_dir("mock-media") / "run.json")
    assert run.tasks["video"].period_us == 16667
    assert run.tasks["music"].period_us == 50000
    chain = read_run_file(fixture_dir("mock-chain") / "run.json")
    assert chain.tasks["input"].period_us == 16667
    assert chain.tasks["engine"].period_us is None


def test_demand_is_finite_run_total_or_absent(fixture_dir):
    office = read_run_file(fixture_dir("mock-office") / "run.json")
    assert office.tasks["writer"].demand == 16000
    assert office.tasks["browser"].demand == 0
    media = read_run_file(fixture_dir("mock-media") / "run.json")
    assert media.tasks["video"].demand is None          # unbounded LOOP
    assert media.tasks["scan"].demand == 31000
    p1a = read_run_file(fixture_dir("mock-p1a") / "run.json")
    assert p1a.tasks["hog"].demand == 90000


def test_wake_events_are_counted_per_target(fixture_dir):
    run = read_run_file(fixture_dir("mock-p1a") / "run.json")
    assert run.wakes == {"editor": 4}


def test_spawn_table_children_are_tasks_with_demand(tmp_path):
    run_file = {"workload_id": "w", "events": [
        {"op": "arrive", "t": 0, "id": "build", "name": "make", "fork_cap": 2,
         "program": [{"op": "RUN", "us": 100}, {"op": "FORK"},
                     {"op": "RUN", "us": 100}, {"op": "FORK"},
                     {"op": "WAIT", "channel": "children:build"}, {"op": "EXIT"}],
         "spawn_table": [
             {"id": "build.c1", "name": "cc1",
              "program": [{"op": "RUN", "us": 500}, {"op": "EXIT"}]},
             {"id": "build.c2", "name": "cc1",
              "program": [{"op": "RUN", "us": 700}, {"op": "SLEEP", "us": 10},
                          {"op": "RUN", "us": 5}, {"op": "EXIT"}]}]},
        {"op": "arrive", "t": 0, "id": "editor", "name": "code", "depart": 5000,
         "program": [{"op": "LOOP", "count": 3,
                      "body": [{"op": "WAIT", "channel": "input:editor"},
                               {"op": "RUN", "us": 40}]}]},
        {"op": "wake", "t": 1000, "channel": "input:editor", "target": "editor"},
    ]}
    p = tmp_path / "run.json"
    p.write_text(json.dumps(run_file))
    run = read_run_file(p)
    assert run.t_end == 5000
    assert run.tasks["build"].demand == 200
    assert run.tasks["build.c1"].demand == 500
    assert run.tasks["build.c1"].arrive is None      # a spawn-table child has no pinned arrival
    assert run.tasks["build.c2"].demand == 705
    assert run.tasks["editor"].demand == 120                 # bounded LOOP
    assert run.tasks["build"].arrive == 0


def test_reserved_task_id_in_run_file_is_refused(tmp_path):
    for name in RESERVED_ENTITIES:
        p = tmp_path / f"{name}.json"
        p.write_text(json.dumps({"workload_id": "w", "events": [
            {"op": "arrive", "t": 0, "id": name, "name": "x", "program": [{"op": "EXIT"}]}]}))
        with pytest.raises(RunFileError, match="reserved"):
            read_run_file(p)


# --------------------------------------------------------- config schedule

def test_config_schedule_entries_are_read_by_index(fixture_dir):
    sched = read_config_schedule(fixture_dir("mock-switch") / "config-schedule.json")
    assert sched.workload_id == "mock-switch"
    assert sched.condition == "llm_algo"
    assert [e.index for e in sched.entries] == [0, 1, 2]
    assert [e.algorithm for e in sched.entries] == ["MLFQ", "FIFO", "MLFQ"]
    assert [e.t_us for e in sched.entries] == [0, 10600, 40600]
    assert sched.entries[2].params == {"num_queues": 3, "timeslice_us": 2000,
                                       "timeslice_growth": 2, "boost_interval_us": 20000}
    assert sched.entries[1].params == {}
    assert sched.entries[1].batch_bandwidth_cap == 0.15
    assert sched.entries[0].provenance == "fallback"
    assert sched.entry(2).algorithm == "MLFQ"
    assert sched.entry(7) is None


def test_config_schedule_refuses_a_malformed_file(tmp_path):
    bad = tmp_path / "s.json"
    bad.write_text(json.dumps({"workload_id": "w", "condition": "fixed"}))
    with pytest.raises(ScheduleError, match="schedule"):
        read_config_schedule(bad)
    bad.write_text(json.dumps({"workload_id": "w", "condition": "fixed",
                               "schedule": [{"t_us": 0, "provenance": "fallback"}]}))
    with pytest.raises(ScheduleError, match="config"):
        read_config_schedule(bad)
    bad.write_text(json.dumps({"workload_id": "w", "condition": "fixed",
                               "schedule": [{"t_us": 0, "provenance": "fallback",
                                             "config": {"algorithm": "RR", "params": {}}}]}))
    with pytest.raises(ScheduleError, match="algorithm"):
        read_config_schedule(bad)
