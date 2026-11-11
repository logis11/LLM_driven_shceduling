#!/usr/bin/env python3
"""The batch-class rule's two unit tests (docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md
§7 item 6), black-box on the binary.

    python3 simulator/tests/test_batch_class.py [path/to/sim]      # default simulator/src/sim

The class itself is not in the trace, but the cap shows it: under a `batch_bandwidth_cap` the
executor parks only batch-class tasks, each park an `x_cap_park` line with `in: true` naming the
task (stage V). So "never batch-class" reads as "never parked while the cap bites", and a positive
control in each test, a task that is batch-class, must be parked, or the test proves nothing.

(a) A task running 1 ms then sleeping 5.7 ms in a loop is never batch-class, however long it runs
    (B1: its CPU since its last voluntary block never reaches a slice). Positive control: a hog.
(b) A TIMER head waking a two-stage chain whose stages run longer than a slice is never
    batch-class (B2: reachable from a TIMER through WAKE targets). A plain task with the same bursts
    is batch-class a slice into each burst and non-batch again after it blocks: each of its parks
    comes at least one slice (10 ms, the boot slice; the memo's "2 ms" predates it, boot-default
    memo §5) after the start of its burst. Run under FIFO: the cap bites only while a non-batch task
    is runnable, and under MLFQ the chain takes the lane whenever it is, so the plain task's batch
    stretches never overlap it and the positive control would not fire (it did not, 2026-11-11).
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLICE = 10000
MLFQ = {"num_queues": 3, "timeslice_us": SLICE, "timeslice_growth": 2, "boost_interval_us": 100000}


def run(sim, name, events, cap=0.05, algorithm="MLFQ"):
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, "w.json"); s = os.path.join(d, "s.json"); t = os.path.join(d, "t.jsonl")
        json.dump({"meta": {"id": name}, "ground_truth": {}, "events": events}, open(w, "w"))
        json.dump({"workload_id": name, "condition": "fixed", "schedule": [
            {"t_us": 0, "config": {"algorithm": algorithm, "params": MLFQ if algorithm == "MLFQ" else {},
                                   "batch_bandwidth_cap": cap},
             "provenance": "fallback"}]}, open(s, "w"))
        subprocess.run([sim, "--workload", w, "--schedule", s, "--out-trace", t], check=True,
                       stderr=subprocess.DEVNULL)
        return [json.loads(l) for l in open(t)]


def poke(end):
    """A short non-batch task woken every 3 ms (200 us, then a WAIT). It is runnable whenever a
    batch-class task holds the lane, so the cap bites on every batch stretch, whoever holds it —
    without it a test can pass because nothing was runnable, not because the class was right (the
    first draft of (b) passed with B2 switched off, 2026-11-11)."""
    prog = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "WAIT", "channel": "input:poke"}, {"op": "RUN", "us": 200}]}]
    return ([{"op": "arrive", "t": 0, "id": "poke", "name": "poke", "depart": end, "program": prog}]
            + [{"op": "wake", "t": t, "channel": "input:poke", "target": "poke"} for t in range(1500, end, 3000)])


def parks(trace, task):
    return [e["t"] for e in trace if e["event"] == "x_cap_park" and e["task"] == task and e["in"]]


def test_a(sim):
    loop = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "RUN", "us": 1000}, {"op": "SLEEP", "us": 5700}]}]
    ev = [{"op": "arrive", "t": 0, "id": "sleeper", "name": "s", "depart": 5_000_000, "program": loop},
          {"op": "arrive", "t": 0, "id": "hog", "name": "h", "program": [{"op": "RUN", "us": 3_000_000}, {"op": "EXIT"}]}] + poke(5_000_000)
    tr = run(sim, "batch-a", ev)
    assert parks(tr, "hog"), "positive control: the hog is never parked — the cap did not bite"
    assert not parks(tr, "sleeper"), f"the 1 ms / 5.7 ms sleeper was parked at {parks(tr, 'sleeper')[:3]}"
    return f"hog parked {len(parks(tr, 'hog'))}x, sleeper 0x"


def test_b(sim):
    head = [{"op": "LOOP", "count": "unbounded", "body": [
        {"op": "TIMER", "period_us": 50000}, {"op": "RUN", "us": 1000}, {"op": "WAKE", "target": "s1"}]}]
    s1 = [{"op": "LOOP", "count": "unbounded", "body": [
        {"op": "WAIT", "channel": "chain:s1"}, {"op": "RUN", "us": 15000}, {"op": "WAKE", "target": "s2"}]}]
    s2 = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "WAIT", "channel": "chain:s2"}, {"op": "RUN", "us": 15000}]}]
    plain = [{"op": "LOOP", "count": "unbounded", "body": [{"op": "WAIT", "channel": "input:plain"}, {"op": "RUN", "us": 15000}]}]
    end = 3_000_000
    ev = [{"op": "arrive", "t": 0, "id": i, "name": i, "depart": end, "program": p}
          for i, p in (("head", head), ("s1", s1), ("s2", s2), ("plain", plain))]
    ev += [{"op": "wake", "t": t, "channel": "input:plain", "target": "plain"} for t in range(48000, end, 50000)]
    ev += poke(end)
    # the plain burst opens 2 ms before each tick, so its batch stretch (10-15 ms in) overlaps the head
    # and the chain waiting, runnable and non-batch: the cap bites there and only there
    tr = run(sim, "batch-b", ev, algorithm="FIFO")
    for stage in ("head", "s1", "s2"):
        assert not parks(tr, stage), f"chain member {stage} was parked at {parks(tr, stage)[:3]}"
    pk = parks(tr, "plain")
    assert pk, "positive control: the plain task is never parked — the cap did not bite"
    # its CPU since its last ready(wake) at each park: at least one slice
    cpu, since, early = 0, None, []
    for e in tr:
        if e.get("task") != "plain":
            continue
        if e["event"] == "ready" and e["cause"] == "wake":
            cpu = 0
        elif e["event"] == "run_start":
            since = e["t"]
        elif e["event"] == "run_end" and since is not None:
            cpu += e["t"] - since; since = None
        elif e["event"] == "x_cap_park" and e["in"]:
            got = cpu + (e["t"] - since if since is not None else 0)
            if got < SLICE:
                early.append((e["t"], got))
    assert not early, f"the plain task parked before a slice into its burst: {early[:3]}"
    return f"plain parked {len(pk)}x, each >= {SLICE} us into its burst; chain 0x"


def main():
    sim = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "simulator", "src", "sim")
    ok = True
    for name, t in (("a", test_a), ("b", test_b)):
        try:
            print(f"test {name}: ok — {t(sim)}")
        except AssertionError as e:
            ok = False
            print(f"test {name}: FAIL — {e}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
