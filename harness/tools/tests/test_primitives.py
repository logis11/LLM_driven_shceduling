"""Primitives on synthetic event lists — the edge rules the fixtures do not
isolate (docs/harness/metrics.md §4, §6)."""

import pytest

from harness.primitives import compute
from harness.reader import ConfigSchedule, RunFile, ScheduleEntry, TaskInfo


def task(id, name="x", arrive=0, depart=None, demand=None, period=None, targets=()):
    return TaskInfo(id=id, name=name, arrive=arrive, depart=depart, demand=demand,
                    period_us=period, wake_targets=list(targets))


def runfile(t_end, tasks, chains=(), wakes=None):
    return RunFile(workload_id="w", t_end=t_end,
                   tasks={t.id: t for t in tasks}, chains=[list(c) for c in chains],
                   wakes=wakes or {})


def schedule(*entries):
    """entries: (index, algorithm, params) — t_us and provenance do not matter here."""
    return ConfigSchedule(workload_id="w", condition="llm_full", entries=[
        ScheduleEntry(index=i, t_us=0, algorithm=alg, params=dict(params),
                      batch_bandwidth_cap=None, provenance="unmodified")
        for (i, alg, params) in entries])


MLFQ_BOOT = {"num_queues": 3, "timeslice_us": 2000, "timeslice_growth": 2,
             "boost_interval_us": 100000}


def cfg(t, index, algorithm):
    return {"event": "config_applied", "t": t, "index": index, "algorithm": algorithm,
            "provenance": "unmodified"}


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


# ------------------------------------------------------------ switch_window
# docs/harness/metrics.md §6.9 — one row per config_applied whose algorithm differs
# from the previous entry's; into MLFQ the window runs until the last hog has
# received W_single of CPU since t_apply (lane time, read from occupancies);
# 0 otherwise.

def _switch_events():
    """FIFO in force; at 1000 a switch into MLFQ lands. Alive at 1000: `a` (running,
    its occupancy ends in a preempt), `b` (pending, first occupancy ends in a
    preempt), `e` (pending, first occupancy ends in a block), `gone` (ended before).
    `late` arrives after the switch and is never counted."""
    return [
        cfg(0, 0, "MLFQ"), cfg(10, 1, "FIFO"),
        {"event": "task_arrive", "t": 0, "task": "gone", "source": "file"},
        {"event": "ready", "t": 0, "task": "gone", "cause": "arrive"},
        {"event": "run_start", "t": 0, "task": "gone"},
        {"event": "run_end", "t": 50, "task": "gone", "reason": "exit"},
        {"event": "task_end", "t": 50, "task": "gone", "reason": "exit"},
        {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
        {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
        {"event": "run_start", "t": 100, "task": "a"},
        {"event": "task_arrive", "t": 200, "task": "b", "source": "file"},
        {"event": "ready", "t": 200, "task": "b", "cause": "arrive"},
        {"event": "task_arrive", "t": 300, "task": "e", "source": "file"},
        {"event": "ready", "t": 300, "task": "e", "cause": "arrive"},
        cfg(1000, 2, "MLFQ"),
        {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"},
        {"event": "run_start", "t": 2000, "task": "b"},
        {"event": "run_end", "t": 3000, "task": "b", "reason": "preempt"},
        {"event": "run_start", "t": 3000, "task": "e"},
        {"event": "run_end", "t": 3200, "task": "e", "reason": "block", "blocked_on": "wait"},
        {"event": "task_arrive", "t": 3200, "task": "late", "source": "file"},
        {"event": "ready", "t": 3200, "task": "late", "cause": "arrive"},
        {"event": "run_start", "t": 3200, "task": "late"},
        {"event": "run_end", "t": 4200, "task": "late", "reason": "preempt"},
        {"event": "run_start", "t": 4200, "task": "a"},
        {"event": "run_end", "t": 10200, "task": "a", "reason": "preempt"},
        {"event": "run_start", "t": 10200, "task": "b"},
        {"event": "run_end", "t": 16200, "task": "b", "reason": "block", "blocked_on": "wait"},
    ]


def test_switch_into_mlfq_window_ends_when_the_last_hog_has_w_single_of_cpu():
    run = runfile(20000, [task("gone"), task("a", arrive=100), task("b", arrive=200),
                          task("e", arrive=300), task("late", arrive=3200)])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "FIFO", {}),
                     (2, "MLFQ", {"num_queues": 4, "timeslice_us": 1000,
                                  "timeslice_growth": 2, "boost_interval_us": 50000}))
    r = compute(run, _switch_events(), sched)
    sw = rows_of(r, "switch_window")
    # W_single = 1000 · (1 + 2 + 4) = 7000. Since t_apply = 1000:
    #   a: [1000,2000] 1000 + [4200,10200] 6000 → reaches 7000 at 10200
    #   b: [2000,3000] 1000 + [10200,16200] 6000 → reaches 7000 at 16200  (last hog)
    # window [1000, 16200] → value 15200
    assert sw == [
        {"entity": "schedule", "metric": "switch_window", "t": 10, "value": 0,
         "algorithm": "FIFO", "index": 1, "hogs": 0},          # into FIFO: only `gone` is alive at 10, and it exits
        {"entity": "schedule", "metric": "switch_window", "t": 1000, "value": 15200,
         "algorithm": "MLFQ", "index": 2, "hogs": 2},
    ]
    assert r.guards == []


def test_hog_that_never_receives_w_single_clips_the_window_at_t_end_with_a_guard():
    run = runfile(5000, [task("a", arrive=100)])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "FIFO", {}), (2, "MLFQ", MLFQ_BOOT))  # W = 6000
    events = [cfg(0, 0, "MLFQ"), cfg(10, 1, "FIFO"),
              {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
              {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
              {"event": "run_start", "t": 100, "task": "a"},
              cfg(1000, 2, "MLFQ"),
              {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"},
              {"event": "run_start", "t": 2500, "task": "a"}]          # open at T_end: 1000 + 2500 < 6000
    r = compute(run, events, sched)
    assert [x["value"] for x in rows_of(r, "switch_window")] == [0, 4000]   # clipped: 5000 − 1000
    assert any("a" in g and "W_single" in g and "T_end" in g for g in r.guards)


def test_window_is_clipped_at_the_next_algorithm_switch():
    run = runfile(20000, [task("a", arrive=100)])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "FIFO", {}), (2, "MLFQ", MLFQ_BOOT),
                     (3, "EDF", {"residual_timeslice_us": 2000}))
    events = [cfg(0, 0, "MLFQ"), cfg(10, 1, "FIFO"),
              {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
              {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
              {"event": "run_start", "t": 100, "task": "a"},
              cfg(1000, 2, "MLFQ"),
              {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"},
              {"event": "run_start", "t": 2500, "task": "a"},
              cfg(4000, 3, "EDF"),                                    # before a has its 6000
              {"event": "run_end", "t": 9000, "task": "a", "reason": "block", "blocked_on": "wait"}]
    r = compute(run, events, sched)
    assert [(x["t"], x["value"]) for x in rows_of(r, "switch_window")] == [(10, 0), (1000, 3000), (4000, 0)]
    assert any("a" in g and "index 3" in g for g in r.guards)


def test_w_single_rounds_down_to_whole_microseconds():
    run = runfile(10000, [task("a", arrive=100)])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "FIFO", {}),
                     (2, "MLFQ", {"num_queues": 3, "timeslice_us": 1001,
                                  "timeslice_growth": 1.5, "boost_interval_us": 50000}))
    events = [cfg(0, 0, "MLFQ"), cfg(10, 1, "FIFO"),
              {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
              {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
              {"event": "run_start", "t": 100, "task": "a"},
              cfg(1000, 2, "MLFQ"),
              {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"},
              {"event": "run_start", "t": 2500, "task": "a"},
              {"event": "run_end", "t": 6000, "task": "a", "reason": "block", "blocked_on": "wait"}]
    r = compute(run, events, sched)
    # W_single = 1001 · (1 + 1.5) = 2502.5 → 2502; a has 1000 by 2000, the rest at 2500 + 1502 = 4002
    assert [x["value"] for x in rows_of(r, "switch_window")] == [0, 3002]
    assert r.guards == []


def test_same_algorithm_entry_is_not_a_switch():
    run = runfile(10000, [task("a", arrive=100)])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "MLFQ", MLFQ_BOOT))
    events = [cfg(0, 0, "MLFQ"),
              {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
              {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
              {"event": "run_start", "t": 100, "task": "a"},
              cfg(1000, 1, "MLFQ"),
              {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"}]
    r = compute(run, events, sched)
    assert rows_of(r, "switch_window") == []
    assert len(rows_of(r, "config_interval")) == 2


def test_switch_at_or_after_t_end_is_ignored():
    run = runfile(1000, [])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "EDF", {"residual_timeslice_us": 2000}))
    r = compute(run, [cfg(0, 0, "MLFQ"), cfg(1000, 1, "EDF")], sched)
    assert rows_of(r, "switch_window") == []


def test_hog_whose_first_run_end_is_past_t_end_is_not_counted():
    run = runfile(1500, [task("a", arrive=100)])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "FIFO", {}), (2, "MLFQ", MLFQ_BOOT))
    events = [cfg(0, 0, "MLFQ"), cfg(10, 1, "FIFO"),
              {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
              {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
              {"event": "run_start", "t": 100, "task": "a"},
              cfg(1000, 2, "MLFQ"),
              {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"}]   # past T_end
    r = compute(run, events, sched)
    assert [(x["value"], x["hogs"]) for x in rows_of(r, "switch_window")] == [(0, 0), (0, 0)]


def test_switch_into_mlfq_without_a_schedule_is_a_guard_and_no_row():
    run = runfile(10000, [task("a", arrive=100)])
    events = [cfg(0, 0, "MLFQ"), cfg(10, 1, "FIFO"),
              {"event": "task_arrive", "t": 100, "task": "a", "source": "file"},
              {"event": "ready", "t": 100, "task": "a", "cause": "arrive"},
              {"event": "run_start", "t": 100, "task": "a"},
              cfg(1000, 2, "MLFQ"),
              {"event": "run_end", "t": 2000, "task": "a", "reason": "preempt"}]
    r = compute(run, events)                      # no schedule
    sw = rows_of(r, "switch_window")
    assert [(x["t"], x["algorithm"], x["value"]) for x in sw] == [(10, "FIFO", 0)]
    assert any("schedule" in g and "index 2" in g for g in r.guards)


def test_schedule_disagreeing_with_the_trace_is_a_guard():
    run = runfile(10000, [])
    sched = schedule((0, "MLFQ", MLFQ_BOOT), (1, "FIFO", {}))
    r = compute(run, [cfg(0, 0, "MLFQ"), cfg(10, 1, "EDF")], sched)
    assert any("index 1" in g and "EDF" in g and "FIFO" in g for g in r.guards)
    r = compute(run, [cfg(0, 0, "MLFQ"), cfg(10, 3, "EDF")], sched)
    assert any("index 3" in g for g in r.guards)
