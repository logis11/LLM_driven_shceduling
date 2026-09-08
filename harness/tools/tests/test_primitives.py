"""Primitives on synthetic event lists — the edge rules the fixtures do not
isolate (docs/harness/metrics.md §4, §6)."""

import pytest

from harness.primitives import compute
from harness.reader import RunFile, TaskInfo


def task(id, name="x", arrive=0, depart=None, demand=None, period=None, targets=()):
    return TaskInfo(id=id, name=name, arrive=arrive, depart=depart, demand=demand,
                    period_us=period, wake_targets=list(targets))


def runfile(t_end, tasks, chains=(), wakes=None):
    return RunFile(workload_id="w", t_end=t_end,
                   tasks={t.id: t for t in tasks}, chains=[list(c) for c in chains],
                   wakes=wakes or {})


def rows_of(result, metric, entity=None):
    return [r for r in result.rows if r["metric"] == metric
            and (entity is None or r["entity"] == entity)]


def test_ready_without_run_start_before_t_end_is_dropped():
    run = runfile(1000, [task("a")])
    events = [
        {"event": "task_arrive", "t": 0, "task": "a", "source": "file"},
        {"event": "ready", "t": 0, "task": "a", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "a"},
        {"event": "run_end", "t": 10, "task": "a", "reason": "block", "blocked_on": "wait"},
        {"event": "ready", "t": 900, "task": "a", "cause": "wake"},
        {"event": "run_start", "t": 1500, "task": "a"},          # past T_end
        {"event": "run_end", "t": 1600, "task": "a", "reason": "exit"},
        {"event": "task_end", "t": 1600, "task": "a", "reason": "exit"},
    ]
    r = compute(run, events)
    assert [(x["t"], x["value"]) for x in rows_of(r, "ready_wait", "a")] == [(0, 0)]
    assert rows_of(r, "completed", "a")[0]["value"] == 0      # exit past T_end
    assert rows_of(r, "turnaround", "a") == []
    assert rows_of(r, "cpu_delivered", "a")[0]["value"] == 10


def test_occupancy_open_at_t_end_is_clipped_and_preempts_counted():
    run = runfile(100, [task("h", demand=500)])
    events = [
        {"event": "task_arrive", "t": 0, "task": "h", "source": "file"},
        {"event": "ready", "t": 0, "task": "h", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "h"},
        {"event": "run_end", "t": 30, "task": "h", "reason": "preempt"},
        {"event": "run_start", "t": 40, "task": "h"},
        {"event": "run_end", "t": 250, "task": "h", "reason": "preempt"},   # after T_end
    ]
    r = compute(run, events)
    assert rows_of(r, "cpu_delivered", "h")[0]["value"] == 30 + (100 - 40)
    assert rows_of(r, "preempt_count", "h")[0]["value"] == 1
    assert rows_of(r, "demand", "h")[0] == {"entity": "h", "metric": "demand",
                                            "t": 100, "value": 500}
    assert rows_of(r, "busy", "lane")[0]["value"] == 90


def test_spawned_child_turnaround_from_its_spawn_arrival():
    run = runfile(10000, [task("build", demand=200),
                          task("build.c1", arrive=None, demand=500)])
    events = [
        {"event": "task_arrive", "t": 0, "task": "build", "source": "file"},
        {"event": "ready", "t": 0, "task": "build", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "build"},
        {"event": "run_end", "t": 100, "task": "build", "reason": "block", "blocked_on": "fork_slot"},
        {"event": "task_arrive", "t": 100, "task": "build.c1", "source": "spawn", "parent": "build"},
        {"event": "ready", "t": 100, "task": "build.c1", "cause": "arrive"},
        {"event": "run_start", "t": 100, "task": "build.c1"},
        {"event": "run_end", "t": 600, "task": "build.c1", "reason": "exit"},
        {"event": "task_end", "t": 600, "task": "build.c1", "reason": "exit"},
    ]
    r = compute(run, events)
    assert rows_of(r, "turnaround", "build.c1")[0] == {"entity": "build.c1", "metric": "turnaround",
                                                       "t": 600, "value": 500}
    assert rows_of(r, "completed", "build.c1")[0] == {"entity": "build.c1", "metric": "completed",
                                                      "t": 600, "value": 1}
    assert rows_of(r, "demand", "build.c1")[0]["value"] == 500


def test_no_demand_row_for_unbounded_program():
    run = runfile(100, [task("v", demand=None, period=50)], chains=[["v"]])
    events = [
        {"event": "task_arrive", "t": 0, "task": "v", "source": "file"},
        {"event": "ready", "t": 0, "task": "v", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "v"},
        {"event": "ready", "t": 0, "task": "v", "cause": "timer_tick"},
        {"event": "run_end", "t": 10, "task": "v", "reason": "block", "blocked_on": "timer"},
        {"event": "deadline", "t": 10, "task": "v", "due": 50, "met": True, "slack_us": 40},
    ]
    r = compute(run, events)
    assert rows_of(r, "demand", "v") == []
    assert rows_of(r, "job", "v") == [{"entity": "v", "metric": "job", "t": 0, "value": 10,
                                       "period_us": 50}]
    assert r.guards == []


def test_lost_wake_trips_the_chain_guard():
    # head ticks twice, the tail only runs once: iteration count != tick count
    run = runfile(200, [task("h", period=100, targets=["t"]), task("t")], chains=[["h", "t"]])
    events = [
        {"event": "task_arrive", "t": 0, "task": "h", "source": "file"},
        {"event": "task_arrive", "t": 0, "task": "t", "source": "file"},
        {"event": "ready", "t": 0, "task": "h", "cause": "arrive"},
        {"event": "ready", "t": 0, "task": "t", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "h"},
        {"event": "ready", "t": 0, "task": "h", "cause": "timer_tick"},
        {"event": "run_end", "t": 5, "task": "h", "reason": "block", "blocked_on": "timer"},
        {"event": "run_start", "t": 5, "task": "t"},
        {"event": "ready", "t": 5, "task": "t", "cause": "wake"},
        {"event": "run_end", "t": 20, "task": "t", "reason": "block", "blocked_on": "wait"},
        {"event": "ready", "t": 100, "task": "h", "cause": "timer_tick"},
        {"event": "run_start", "t": 100, "task": "h"},
        {"event": "run_end", "t": 105, "task": "h", "reason": "block", "blocked_on": "timer"},
        # the wake to t is lost: no ready(wake), no second iteration
    ]
    r = compute(run, events)
    assert [x["value"] for x in rows_of(r, "job", "h")] == [20]
    assert any("h" in g and "tick" in g for g in r.guards)


def test_deadline_disagreement_on_single_stage_is_a_guard():
    run = runfile(100, [task("v", period=50)], chains=[["v"]])
    events = [
        {"event": "task_arrive", "t": 0, "task": "v", "source": "file"},
        {"event": "ready", "t": 0, "task": "v", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "v"},
        {"event": "ready", "t": 0, "task": "v", "cause": "timer_tick"},
        {"event": "run_end", "t": 10, "task": "v", "reason": "block", "blocked_on": "timer"},
        {"event": "deadline", "t": 12, "task": "v", "due": 50, "met": True, "slack_us": 38},
    ]
    r = compute(run, events)
    assert rows_of(r, "job", "v")[0]["value"] == 10
    assert any("deadline" in g for g in r.guards)


def test_config_interval_ignores_entries_at_or_after_t_end():
    run = runfile(100, [])
    events = [
        {"event": "config_applied", "t": 0, "index": 0, "algorithm": "MLFQ", "provenance": "fallback"},
        {"event": "config_applied", "t": 40, "index": 1, "algorithm": "EDF", "provenance": "held"},
        {"event": "config_applied", "t": 100, "index": 2, "algorithm": "FIFO", "provenance": "unmodified"},
    ]
    r = compute(run, events)
    assert [(x["t"], x["value"], x["provenance"], x["algorithm"], x["index"])
            for x in rows_of(r, "config_interval")] == [(0, 40, "fallback", "MLFQ", 0),
                                                        (40, 60, "held", "EDF", 1)]


def test_stimulus_count_guard_against_run_file_wakes():
    run = runfile(100, [task("e")], wakes={"e": 2})
    events = [
        {"event": "task_arrive", "t": 0, "task": "e", "source": "file"},
        {"event": "ready", "t": 0, "task": "e", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "e"},
        {"event": "run_end", "t": 0, "task": "e", "reason": "block", "blocked_on": "wait"},
        {"event": "ready", "t": 10, "task": "e", "cause": "wake"},
        {"event": "run_start", "t": 10, "task": "e"},
        {"event": "run_end", "t": 12, "task": "e", "reason": "block", "blocked_on": "wait"},
        # the second keystroke never produced a ready line
    ]
    r = compute(run, events)
    assert any("e" in g and "wake" in g for g in r.guards)
