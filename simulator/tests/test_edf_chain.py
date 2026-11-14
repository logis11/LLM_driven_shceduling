#!/usr/bin/env python3
"""Conformance item (f) of the RQ0 gate spec (harness/experiments/rq0-gate.yaml,
`simulator-conformance`), black-box on the binary: the frame chain's woken stages in EDF's deadline
class with the frame's deadline (docs/recognition-vocabulary.md §2, 2026-10-06).

    python3 simulator/tests/test_edf_chain.py [path/to/sim]      # default simulator/src/sim

One frame under EDF, the cap null. The head's TIMER (period 30 ms) opens the frame at 0, so the
frame's deadline is 30 000 µs. The head runs 1 ms and WAKEs stage s1, which runs 4 ms and WAKEs
s2, which runs 12 ms. `bulk`, with no TIMER, arrives beside the head with more work than the frame
holds: EDF's residual class.

(1) The deadline class: from the head's block to s2's end the lane goes head → s1 → s2, and `bulk`
    first runs after s2 has ended — a residual task never runs while a deadline-class task is
    runnable.
(2) The frame's deadline, pinned to the µs by a probe: a periodic task that arrives while a stage
    holds the lane, its own deadline set by its period. EDF preempts the holder only for an earlier
    deadline, a tie does not preempt (the fixed executor rule), so a probe due at 29 999 µs must
    take the lane from the stage at once and a probe due at 30 000 µs must not. Done for s1
    (probe at 3 000 µs) and for s2 (probe at 10 000 µs), four runs.
"""
import sys

import blackbox as bb

FRAME = 30_000
DEPART = 29_000


def workload(probe=None):
    head = [{"op": "LOOP", "count": "unbounded", "body": [
        {"op": "TIMER", "period_us": FRAME}, {"op": "RUN", "us": 1_000}, {"op": "WAKE", "target": "s1"}]}]
    s1 = [{"op": "LOOP", "count": "unbounded", "body": [
        {"op": "WAIT", "channel": "chain:s1"}, {"op": "RUN", "us": 4_000}, {"op": "WAKE", "target": "s2"}]}]
    s2 = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "WAIT", "channel": "chain:s2"}, {"op": "RUN", "us": 12_000}]}]
    ev = [{"op": "arrive", "t": 0, "id": i, "name": i, "depart": DEPART, "program": p}
          for i, p in (("head", head), ("s1", s1), ("s2", s2))]
    ev.append({"op": "arrive", "t": 0, "id": "bulk", "name": "bulk", "depart": DEPART,
               "program": [{"op": "RUN", "us": 1_000_000}, {"op": "EXIT"}]})
    if probe:
        at, period = probe
        ev.append({"op": "arrive", "t": at, "id": "probe", "name": "probe", "depart": DEPART,
                   "program": [{"op": "TIMER", "period_us": period}, {"op": "RUN", "us": 2_000}, {"op": "EXIT"}]})
    return ev


def holder_at(trace, t):
    """The task holding the lane just after µs t, or None."""
    for task, s, e, _ in bb.occupancies(trace):
        if s <= t < e:
            return task
    return None


def test_deadline_class(sim):
    tr = bb.run(sim, "edf-chain", workload(), [bb.entry("EDF")])
    occ = bb.occupancies(tr)
    order = [task for task, s, e, _ in occ if e <= 17_000]
    assert order == ["head", "s1", "s2"], f"the lane before s2's end went {order}, not head → s1 → s2"
    s2_end = next(e for task, s, e, _ in occ if task == "s2")
    bulk_first = next((s for task, s, e, _ in occ if task == "bulk"), None)
    assert bulk_first is not None and bulk_first >= s2_end, (
        f"the residual task ran at {bulk_first} µs, before s2 ended at {s2_end} µs")
    return f"head → s1 → s2 to {s2_end} µs, the residual task first at {bulk_first} µs"


def probe(sim, stage, at):
    """The probe due one µs before the frame's deadline preempts `stage` at `at`; due at it, it does not."""
    early = bb.run(sim, f"edf-probe-{stage}-early", workload((at, FRAME - at - 1)), [bb.entry("EDF")])
    assert holder_at(early, at) == "probe", (
        f"a probe due at {FRAME - 1} µs did not take the lane from {stage} at {at} µs "
        f"(holder {holder_at(early, at)!r}): {stage}'s deadline is not after {FRAME - 1}")
    cut = [e for e in early if e["event"] == "run_end" and e["task"] == stage and e["t"] == at]
    assert cut and cut[0]["reason"] == "preempt", f"{stage} was not preempted at {at} µs by the earlier deadline"
    tie = bb.run(sim, f"edf-probe-{stage}-tie", workload((at, FRAME - at)), [bb.entry("EDF")])
    assert holder_at(tie, at) == stage, (
        f"a probe due at {FRAME} µs took the lane from {stage} at {at} µs: {stage}'s deadline is not "
        f"{FRAME} µs, the frame's (a tie does not preempt)")
    return f"{stage}: preempted by a probe due at {FRAME - 1} µs, kept the lane against one due at {FRAME} µs"


def test_frame_deadline(sim):
    return "; ".join([probe(sim, "s1", 3_000), probe(sim, "s2", 10_000)])


if __name__ == "__main__":
    sys.exit(bb.main([("f-class", test_deadline_class), ("f-deadline", test_frame_deadline)], sys.argv))
