#!/usr/bin/env python3
"""Conformance item (d) of the RQ0 gate spec (harness/experiments/rq0-gate.yaml,
`simulator-conformance`), black-box on the binary: batch_bandwidth_cap read and applied as a
work-conserving ceiling on the behavioural batch class (docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md;
the token bucket, simulator/memo/memo_261020.md F1). Which tasks are batch-class is
`test_batch_class.py`'s; this test is the ceiling's.

    python3 simulator/tests/test_cap_ceiling.py [path/to/sim]      # default simulator/src/sim

(1) The ceiling. A `hog` that never blocks (batch-class one slice in) arrives first beside
    `frame`, a periodic task whose every job takes its whole period, so a non-batch task is
    runnable throughout the window of 2 s. Under MLFQ, FIFO and LOTTERY, the hog's share of the
    window is at most the cap plus three slices over the window (the slice before it enters the
    class, the bucket's depth of one slice, one grant's overrun — memo_261020 F1, F4), at cap
    0.05 and at cap 0.2. With the cap null the hog's share is above the 0.05 ceiling's bound, so
    that cap binds; and the value is read: under MLFQ and LOTTERY the hog's share at cap 0.2 is
    above the 0.05 bound too. Under FIFO a capped hog, once preempted, does not get the lane back
    from a periodic task that never blocks, so FIFO shows the ceiling and not the value. EDF is
    left out: the periodic task is in its deadline class and takes the lane whatever the cap says.
(2) Work-conserving. The hog alone, cap 0.05, under all four algorithms: it is never parked and the
    lane is busy for the whole window — no non-batch task is runnable, so nothing is capped.
"""
import sys

import blackbox as bb

WINDOW = 2_000_000
TOL = 3 * bb.SLICE / WINDOW


def ceiling_workload():
    frame = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "TIMER", "period_us": 10_000}, {"op": "RUN", "us": 10_000}]}]
    return [{"op": "arrive", "t": 0, "id": "hog", "name": "hog", "depart": WINDOW,
             "program": [{"op": "RUN", "us": 10 * WINDOW}, {"op": "EXIT"}]},
            {"op": "arrive", "t": 0, "id": "frame", "name": "frame", "depart": WINDOW, "program": frame}]


def share(sim, algorithm, cap):
    tr = bb.run(sim, f"cap-{algorithm.lower()}-{cap}", ceiling_workload(), [bb.entry(algorithm, cap)])
    return bb.cpu(tr, "hog") / WINDOW


def test_ceiling(sim):
    out, failed = [], []
    for a in ("MLFQ", "FIFO", "LOTTERY"):
        got = {cap: share(sim, a, cap) for cap in (None, 0.05, 0.2)}
        for cap in (0.05, 0.2):
            if got[cap] > cap + TOL:
                failed.append(f"{a}: at cap {cap} the batch-class hog took {got[cap]:.4f} of the lane")
        if got[None] <= 0.05 + TOL:
            failed.append(f"{a}: uncapped the hog takes {got[None]:.4f}, within the 0.05 bound — the case shows no ceiling")
        if a != "FIFO" and got[0.2] <= 0.05 + TOL:
            failed.append(f"{a}: at cap 0.2 the hog takes {got[0.2]:.4f}, within the 0.05 bound — the value is not read")
        out.append(f"{a} uncapped {got[None]:.4f}, cap 0.05 → {got[0.05]:.4f}, cap 0.2 → {got[0.2]:.4f}")
    assert not failed, " | ".join(failed)
    return "; ".join(out) + f" (bound: cap + {TOL:.4f})"


def test_work_conserving(sim):
    failed, out = [], []
    ev = [{"op": "arrive", "t": 0, "id": "hog", "name": "hog", "depart": WINDOW,
           "program": [{"op": "RUN", "us": 10 * WINDOW}, {"op": "EXIT"}]}]
    for a in bb.ALGORITHMS:
        tr = bb.run(sim, f"cap-alone-{a.lower()}", ev, [bb.entry(a, 0.05)])
        busy = bb.cpu(tr, "hog")
        if bb.parks(tr, "hog") or busy != WINDOW:
            failed.append(f"{a}: alone under cap 0.05 the hog was parked {len(bb.parks(tr, 'hog'))}x and ran {busy} of {WINDOW} µs")
        out.append(a)
    assert not failed, " | ".join(failed)
    return f"alone under cap 0.05 the hog holds the whole window, never parked ({', '.join(out)})"


if __name__ == "__main__":
    sys.exit(bb.main([("d-ceiling", test_ceiling), ("d-work-conserving", test_work_conserving)], sys.argv))
