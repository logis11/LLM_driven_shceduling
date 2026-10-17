"""By when a file's batch job ends on one lane under every work-conserving policy (end_bound.py; 9.10 D78, D162)."""
import end_bound


def _artifact():
    # an editor woken at 1, 3 and 9 ms for 2 ms each, and a job arriving at 2 ms: 4 ms of CPU, a 1 ms block
    editor = {"op": "arrive", "id": "editor", "t": 0,
              "program": [{"op": "WAIT", "channel": "timer:editor"}, {"op": "RUN", "us": 2000}] * 3}
    job = {"op": "arrive", "id": "bulk", "t": 2000,
           "program": [{"op": "RUN", "us": 3000}, {"op": "SLEEP", "us": 1000}, {"op": "RUN", "us": 1000}, {"op": "EXIT"}]}
    wakes = [{"op": "wake", "channel": "timer:editor", "target": "editor", "t": t} for t in (1000, 3000, 9000)]
    return {"events": [editor, job, *wakes]}


def test_the_bound_is_the_arrival_the_job_and_the_other_tasks_cpu_after_it():
    r = end_bound.end_bound(_artifact(), "bulk")
    assert (r["a"], r["C"], r["S"], r["others_after"]) == (2000, 4000, 1000, 4000)
    assert r["bound"] == 11000


def test_the_backlog_at_the_arrival_counts_a_run_released_before_it():
    # the editor's run released at 1 ms still holds 1 ms of the lane at the job's arrival
    assert end_bound.end_bound(_artifact(), "bulk")["B"] == 1000


def test_the_fixed_point_counts_only_what_is_released_before_it():
    # 2 + 4 + 1 + 1 (the backlog) = 8 ms; the 3 ms wake's 2 ms makes 10 ms, and the 9 ms wake's 2 ms 12 ms
    assert end_bound.end_bound(_artifact(), "bulk")["fixed_point"] == 12000
