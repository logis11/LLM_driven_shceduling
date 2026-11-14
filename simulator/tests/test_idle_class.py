#!/usr/bin/env python3
"""Conformance item (e) of the RQ0 gate spec (harness/experiments/rq0-gate.yaml,
`simulator-conformance`), black-box on the binary: the strict idle class, an idle task running only
when no other-class task is runnable and preempted at once when one wakes, under every algorithm
(docs/memos/2026-10-08-declared-scheduling-class.md §2).

    python3 simulator/tests/test_idle_class.py [path/to/sim]      # default simulator/src/sim

One workload, run under MLFQ, FIFO, EDF and LOTTERY with the cap null:

- `idler`, declared idle, arrives first with more work than the window holds, so it is runnable
  throughout and holds the lane whenever the algorithm alone would give it;
- `ui`, a normal task woken every 10 ms for 3 ms — a wake comes while the idler holds the lane;
- `hog`, a normal task that sleeps 300 ms and then runs 200 ms, a batch-class stretch with no wake
  in it.

Asserted under each algorithm: no occupancy of the idler overlaps a span over which a normal task
is runnable (from the ready line that makes it runnable to the run_end that blocks or ends it); the
idler leaves the lane at the very µs of each wake that comes while it holds it, with
run_end(preempt) — at least one such wake, or the test proves nothing; and the lane is busy over
the whole window, the idler taking every gap (the band is below the algorithm, not a hole in it).
"""
import sys

import blackbox as bb

END = 1_000_000
PERIOD, BURST = 10_000, 3_000


def workload():
    ui = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "WAIT", "channel": "input:ui"}, {"op": "RUN", "us": BURST}]}]
    return ([{"op": "arrive", "t": 0, "id": "idler", "name": "idler", "depart": END, "declared_class": "idle",
              "program": [{"op": "RUN", "us": 5 * END}, {"op": "EXIT"}]},
             {"op": "arrive", "t": 0, "id": "ui", "name": "ui", "depart": END, "program": ui},
             {"op": "arrive", "t": 0, "id": "hog", "name": "hog", "depart": END,
              "program": [{"op": "SLEEP", "us": 300_000}, {"op": "RUN", "us": 200_000}, {"op": "EXIT"}]}]
            + [{"op": "wake", "t": t, "channel": "input:ui", "target": "ui"} for t in range(5_000, END, PERIOD)])


def check(sim, algorithm):
    tr = bb.run(sim, f"idle-{algorithm.lower()}", workload(), [bb.entry(algorithm)])
    occ = bb.occupancies(tr)
    idle_occ = [(s, e, why) for task, s, e, why in occ if task == "idler"]
    spans = [(task, a, b) for task in ("ui", "hog") for a, b in bb.runnable_intervals(tr, task)]
    overlap = [(task, a, b, s, e) for task, a, b in spans for s, e, _ in idle_occ if max(a, s) < min(b, e)]
    assert not overlap, (f"{algorithm}: the idler held the lane while a normal task was runnable — "
                         f"(task, runnable from, to, idler from, to) {overlap[:3]}")
    wakes = [e["t"] for e in tr if e["event"] == "ready" and e["task"] == "ui"]
    at_wake = [(s, e, why) for s, e, why in idle_occ if e in wakes and s < e]
    assert at_wake, f"{algorithm}: no wake came while the idler held the lane — the preemption is not exercised"
    late = [(s, e, why) for s, e, why in at_wake if why != "preempt"]
    assert not late, f"{algorithm}: the idler left the lane at a wake other than by preemption: {late[:3]}"
    busy = sum(e - s for _task, s, e, _ in occ)
    assert busy == END, f"{algorithm}: the lane was free for {END - busy} µs with the idler runnable throughout"
    hog_cpu = bb.cpu(tr, "hog")
    assert hog_cpu == 200_000, f"{algorithm}: the hog received {hog_cpu} µs of its 200 000"
    return f"{algorithm} idler preempted at {len(at_wake)} wakes, {bb.cpu(tr, 'idler')} µs in the gaps"


def test_strict_idle_class(sim):
    done, failed = [], []
    for a in bb.ALGORITHMS:               # every algorithm judged, so a failure names each one it holds in
        try:
            done.append(check(sim, a))
        except AssertionError as e:
            failed.append(str(e))
    assert not failed, " | ".join(failed)
    return "; ".join(done)


if __name__ == "__main__":
    sys.exit(bb.main([("e", test_strict_idle_class)], sys.argv))
