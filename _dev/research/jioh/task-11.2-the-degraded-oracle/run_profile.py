#!/usr/bin/env python3
"""A run's shape from its trace, beside another run of the same file: CPU per task inside the window, each task's
bursts (CPU between voluntary blocks — rule B1's counter at each block), and where the cap's parks fall.

    python3 run_profile.py <workload_id> [--runs 'fixed~focus' 'oracle~focus'] [--top 6] [--bins 10]

Prints JSON; reads `runs/rq0-gate/<workload_id>/<run>/trace.jsonl.gz` and the compiled workload's window."""
import argparse
import gzip
import json
import pathlib
from collections import Counter, defaultdict

REPO = pathlib.Path(__file__).resolve().parents[4]


def profile(trace, t_end, bins):
    cpu, burst, bursts, parks = Counter(), Counter(), defaultdict(list), defaultdict(Counter)
    running, start = None, 0
    with gzip.open(trace, "rt") as f:
        for raw in f:
            e = json.loads(raw)
            t, ev, task = e.get("t", 0), e["event"], e.get("task")
            if t > t_end:
                break
            if ev == "run_start":
                running, start = task, t
            elif ev == "run_end":
                cpu[task] += t - start
                burst[task] += t - start
                running = None
            elif ev == "x_block":
                bursts[task].append(burst[task])
                burst[task] = 0
            elif ev == "x_cap_park" and e["in"]:
                parks[task][min(bins - 1, t * bins // t_end)] += 1
    if running is not None:
        cpu[running] += t_end - start
    return cpu, bursts, parks


def pct(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(len(v) * p / 100))] if v else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workload_id")
    ap.add_argument("--runs", nargs="+", default=["fixed~focus", "oracle~focus"])
    ap.add_argument("--runs-dir", default=str(REPO / "runs" / "rq0-gate"))
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--bins", type=int, default=10)
    args = ap.parse_args()
    w = json.load(open(REPO / "dataset" / "build" / "coreset-single" / f"{args.workload_id}.workload.json"))
    t_end = max(f["t_end"] for f in w["focus"])
    out = {"workload_id": args.workload_id, "t_end": t_end, "runs": {}}
    for run in args.runs:
        cpu, bursts, parks = profile(pathlib.Path(args.runs_dir) / args.workload_id / run / "trace.jsonl.gz",
                                     t_end, args.bins)
        top = [t for t, _ in cpu.most_common(args.top)]
        out["runs"][run] = {
            "cpu_us": {t: cpu[t] for t in top}, "cpu_us_all": sum(cpu.values()), "tasks": len(cpu),
            "bursts": {t: {"n": len(bursts[t]), "p50": pct(bursts[t], 50), "p90": pct(bursts[t], 90),
                           "max": max(bursts[t]) if bursts[t] else None} for t in top},
            "parks_by_tenth": {t: [parks[t][i] for i in range(args.bins)] for t in parks if sum(parks[t].values()) >=
                               max(1, sum(sum(c.values()) for c in parks.values()) // 50)},
        }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
