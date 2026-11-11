#!/usr/bin/env python3
"""Demand is conserved across config switches (memo_261010 Part D2) — black-box on the binary.

    python3 simulator/tests/test_switch_demand.py [path/to/sim]      # default simulator/src/sim

Three finite tasks with RUNs longer than any slice, a sleeper and a periodic task, under a schedule
that walks every algorithm and back, entries landing mid-RUN, during a drain (out of MLFQ, EDF and
LOTTERY a switch waits for the lane — U3, and since AB a RUN's end inside an occupancy), and a
same-algorithm entry with a smaller slice (U2). Every task that exits must have received exactly
its program's RUN total, and the trace must pass every check of tools/trace_check.py. The cap is
on in two entries, so a park can also fall across a switch.
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CHECK = os.path.join(ROOT, "simulator", "tools", "trace_check.py")


def mlfq(slice_us):
    return {"algorithm": "MLFQ", "params": {"num_queues": 3, "timeslice_us": slice_us, "timeslice_growth": 2,
                                            "boost_interval_us": 100000}}


SCHEDULE = [   # (t_us, config, cap)
    (0, mlfq(10000), None),
    (7300, {"algorithm": "FIFO", "params": {}}, None),                       # out of MLFQ: drains
    (19100, {"algorithm": "EDF", "params": {"residual_timeslice_us": 7000}}, 0.2),   # out of FIFO: at once
    (41700, {"algorithm": "LOTTERY", "params": {"timeslice_us": 5000, "batch_share": 0.3}}, None),  # drains
    (66600, mlfq(4000), 0.05),                                                # out of LOTTERY: drains
    (70000, mlfq(2000), 0.05),                                                # same algorithm (U2)
    (93300, {"algorithm": "FIFO", "params": {}}, None),
    (120000, mlfq(10000), None),
]


def main():
    sim = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "simulator", "src", "sim")
    run = lambda *us: [{"op": "RUN", "us": u} for u in us]
    ev = [
        {"op": "arrive", "t": 0, "id": "a", "name": "a", "program": run(23000, 17000, 9000) + [{"op": "EXIT"}]},
        {"op": "arrive", "t": 500, "id": "b", "name": "b", "program": run(41000) + [{"op": "SLEEP", "us": 3000}] + run(12000) + [{"op": "EXIT"}]},
        {"op": "arrive", "t": 900, "id": "c", "name": "c", "program": run(5000, 5000, 5000, 5000, 5000, 5000) + [{"op": "EXIT"}]},
        {"op": "arrive", "t": 0, "id": "p", "name": "p", "depart": 200000, "program": [
            {"op": "LOOP", "count": "unbounded", "body": [{"op": "TIMER", "period_us": 16667}, {"op": "RUN", "us": 2500}]}]},
    ]
    with tempfile.TemporaryDirectory() as d:
        w, s, t = (os.path.join(d, n) for n in ("w.json", "s.json", "t.jsonl"))
        json.dump({"meta": {"id": "switch-demand"}, "ground_truth": {}, "events": ev}, open(w, "w"))
        json.dump({"workload_id": "switch-demand", "condition": "fixed", "schedule": [
            {"t_us": at, "config": dict(c, batch_bandwidth_cap=cap), "provenance": "unmodified" if k else "fallback"}
            for k, (at, c, cap) in enumerate(SCHEDULE)]}, open(s, "w"))
        subprocess.run([sim, "--workload", w, "--schedule", s, "--out-trace", t], check=True, stderr=subprocess.DEVNULL)
        lines = [json.loads(l) for l in open(t)]
        applied = [e["index"] for e in lines if e["event"] == "config_applied"]
        ended = {e["task"] for e in lines if e["event"] == "task_end" and e["reason"] == "exit"}
        r = subprocess.run([sys.executable, CHECK, w, t], capture_output=True, text=True)
    ok = r.returncode == 0 and applied == list(range(len(SCHEDULE))) and ended == {"a", "b", "c"}
    print(("ok" if ok else "FAIL") + f" — entries applied {applied}, exited {sorted(ended)}; trace_check: {r.stdout.strip()}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
