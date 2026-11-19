#!/usr/bin/env python3
"""A simulator stage against the RQ0 run's own traces: every file of the run under its fixed and oracle config
schedules, run again on the given binary, the new trace read line by line against the run's, the header line
(which names the simulator's version) left out.

    python3 stage_regression.py --sim simulator/src/sim [--runs 'fixed~focus' 'oracle~focus'] [--workers 4]
        [--out stage-regression-<name>.json]

Writes the per-run result — identical, or the count of differing lines and the first one — beside this script."""
import argparse
import gzip
import itertools
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from multiprocessing import Pool

REPO = pathlib.Path(__file__).resolve().parents[4]
RUNS = REPO / "runs" / "rq0-gate"
BUILD = REPO / "dataset" / "build"


def one(job):
    sim, wid, run = job
    run_dir = RUNS / wid / run
    workload = next(BUILD.glob(f"*/{wid}.workload.json"))
    with tempfile.TemporaryDirectory() as d:
        out = pathlib.Path(d) / "trace.jsonl"
        p = subprocess.run([sim, "--workload", str(workload), "--schedule", str(run_dir / "schedule.json"),
                            "--out-trace", str(out)], stderr=subprocess.PIPE, text=True)
        if p.returncode != 0:
            return {"workload_id": wid, "run": run, "exit": p.returncode, "stderr": p.stderr[-400:]}
        n, diff, first = 0, 0, None
        with gzip.open(run_dir / "trace.jsonl.gz", "rt") as old, open(out) as new:
            next(old, None)
            next(new, None)
            for a, b in itertools.zip_longest(old, new):
                n += 1
                if a != b:
                    diff += 1
                    if first is None:
                        first = {"line": n + 1, "run": (a or "").strip()[:200], "new": (b or "").strip()[:200]}
    return {"workload_id": wid, "run": run, "exit": 0, "lines": n, "differing": diff, "first": first}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--sim", required=True)
    ap.add_argument("--runs", nargs="+", default=["fixed~focus", "oracle~focus"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    sim = str(pathlib.Path(args.sim).resolve())
    wids = sorted(d.name for d in RUNS.iterdir() if (d / "fixed~focus").is_dir())
    jobs = [(sim, w, r) for w in wids for r in args.runs if (RUNS / w / r).is_dir()]
    with Pool(args.workers) as pool:
        rows = sorted(pool.map(one, jobs, chunksize=1), key=lambda r: (r["workload_id"], r["run"]))
    summary = {}
    for r in args.runs:
        mine = [x for x in rows if x["run"] == r]
        summary[r] = {"runs": len(mine), "identical": sum(1 for x in mine if x["exit"] == 0 and x["differing"] == 0),
                      "differing": [x["workload_id"] for x in mine if x["exit"] == 0 and x["differing"]],
                      "failed": [x["workload_id"] for x in mine if x["exit"] != 0]}
    out = {"sim": args.sim, "summary": summary, "rows": rows}
    pathlib.Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.exit(main())
