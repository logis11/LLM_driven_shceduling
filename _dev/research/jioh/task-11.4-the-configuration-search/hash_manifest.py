#!/usr/bin/env python3
"""The search's hash manifest: one line per run of the configuration search, its trace's hash and its records' hash,
so that the committed report can be held against a regeneration of the runs once their traces are deleted (11.4 spec,
decision 15: every run reproducible from the search spec on the pinned simulator).

    python3 _dev/research/jioh/task-11.4-the-configuration-search/hash_manifest.py
            [--search-dir runs/rq0-config-search] [--out harness/experiments/rq0-config-search/runs.sha256.csv]

For each run directory `<workload>/<condition>@<point>~<telemetry>` under the search's runs directory:

  trace_sha256    the SHA-256 of the trace as the simulator wrote it, uncompressed — read from the run's
                  `trace.rerun.sha256`, the hash the runner kept of the second invocation's trace after holding it
                  equal to the first's, the one stored as `trace.jsonl.gz`;
  records_sha256  the SHA-256 of the run's records, uncompressed — `records.csv.gz` read through gzip.

The rows are sorted by workload and point. The same columns as 10.5's manifest of the RQ0 run
(`_dev/research/jioh/task-10.5-the-rq0-run/hash_manifest.py`), the table column the point's id. Run from the repository
root. It reads no report or reading."""
import argparse
import concurrent.futures
import csv
import gzip
import hashlib
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
COLUMNS = ("workload_id", "condition", "point", "telemetry", "trace_sha256", "records_sha256")


def hashes(run_dir):
    run_dir = pathlib.Path(run_dir)
    condition, rest = run_dir.name.split("@", 1)
    point, telemetry = rest.split("~", 1)
    h = hashlib.sha256()
    with gzip.open(run_dir / "records.csv.gz", "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    trace = (run_dir / "trace.rerun.sha256").read_text().split()[0]
    return {"workload_id": run_dir.parent.name, "condition": condition, "point": point, "telemetry": telemetry,
            "trace_sha256": trace, "records_sha256": h.hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--search-dir", default="runs/rq0-config-search")
    ap.add_argument("--out", default="harness/experiments/rq0-config-search/runs.sha256.csv")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    search, out = (REPO / args.search_dir).resolve(), (REPO / args.out).resolve()
    runs = sorted(str(p) for p in search.glob("*/*@*~*") if (p / "trace.rerun.sha256").is_file())
    t0, rows = time.time(), []
    with concurrent.futures.ProcessPoolExecutor(args.workers) as pool:
        for k, row in enumerate(pool.map(hashes, runs, chunksize=8), 1):
            rows.append(row)
            if k % 1000 == 0:
                print(f"  {k}/{len(runs)} runs, {time.time() - t0:.0f} s", file=sys.stderr, flush=True)
    rows.sort(key=lambda r: tuple(r[k] for k in COLUMNS[:4]))
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(COLUMNS), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} runs → {out} ({out.stat().st_size} bytes), {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
