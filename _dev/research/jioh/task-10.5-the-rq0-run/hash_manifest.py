#!/usr/bin/env python3
"""The hash manifest (10.5 spec, decision 13): one line per run of a finished experiment, its trace's hash and its
records' hash, so that the committed report can be held against a regeneration of the run's outputs.

    python3 _dev/research/jioh/task-10.5-the-rq0-run/hash_manifest.py [--experiment-dir runs/rq0-gate]
                                                                      [--out harness/experiments/rq0-gate/runs.sha256.csv]

For each run of the experiment's `guards-manifest.json`, in identity order:

  trace_sha256    the SHA-256 of the trace as the simulator wrote it, uncompressed — read from the run's
                  `trace.rerun.sha256`, the hash the runner kept of the second invocation's trace after holding it
                  equal to the first's, the one stored as `trace.jsonl.gz`;
  records_sha256  the SHA-256 of the run's records, uncompressed — `records.csv.gz` read through gzip.

Run from the repository root. It reads no report, score or verdict."""
import argparse
import concurrent.futures
import csv
import gzip
import hashlib
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
IDENTITY = ("workload_id", "condition", "table", "seed", "boot_default", "telemetry")


def hashes(entry):
    h = hashlib.sha256()
    with gzip.open(entry["records"], "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    trace = pathlib.Path(entry["rerun_trace"]).read_text().split()[0]
    return {**{k: entry[k] for k in IDENTITY}, "trace_sha256": trace, "records_sha256": h.hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--experiment-dir", default="runs/rq0-gate")
    ap.add_argument("--out", default="harness/experiments/rq0-gate/runs.sha256.csv")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    exp, out = (REPO / args.experiment_dir).resolve(), (REPO / args.out).resolve()
    runs = json.loads((exp / "guards-manifest.json").read_text())["runs"]
    t0, rows = time.time(), []
    with concurrent.futures.ProcessPoolExecutor(args.workers) as pool:
        for k, row in enumerate(pool.map(hashes, runs, chunksize=8), 1):
            rows.append(row)
            if k % 1000 == 0:
                print(f"  {k}/{len(runs)} runs, {time.time() - t0:.0f} s", file=sys.stderr, flush=True)
    rows.sort(key=lambda r: tuple(r[k] for k in IDENTITY))
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(IDENTITY) + ["trace_sha256", "records_sha256"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} runs → {out} ({out.stat().st_size} bytes), {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
