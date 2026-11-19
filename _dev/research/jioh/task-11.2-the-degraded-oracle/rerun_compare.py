#!/usr/bin/env python3
"""The rerun against the RQ0 run (the 11.2 spec, decisions 6 and 7).

    python3 rerun_compare.py [--rerun runs/rq0-gate-rerun] [--run runs/rq0-gate] [--workers 4]

Decision 6: every run of the rerun, its trace read line by line against the RQ0 run's with the header line — the
version stamp — left out, and its records with their `sim` column left out; a judging file's runs change when any
of them differs. Decision 7: the rerun's term rows at the primary boot default under the primary table on which
the oracle is worse than fixed by the floor or more (`oracle_worse`), against the RQ0 run's post hoc reading's
(`runs/rq0-gate/post-hoc/scores.csv`): a new case is one the rerun shows and the RQ0 run did not, a vanished one
the reverse. Writes `rerun-compare.json` beside this script."""
import argparse
import csv
import gzip
import itertools
import json
import pathlib
import sys
from multiprocessing import Pool

REPO = pathlib.Path(__file__).resolve().parents[4]
TERM = ("entity", "metric", "aggregate", "cause", "channel", "window_start_us", "window_end_us")


def same_trace(a, b):
    with gzip.open(a, "rt") as x, gzip.open(b, "rt") as y:
        next(x, None)
        next(y, None)
        n = 0
        for p, q in itertools.zip_longest(x, y):
            n += 1
            if p != q:
                return False, n + 1
    return True, None


def records_rows(path):
    with gzip.open(path, "rt", newline="") as f:
        r = csv.DictReader(f)
        cols = [c for c in r.fieldnames if c != "sim"]
        return [tuple(row[c] for c in cols) for row in r]


def one(job):
    rerun_dir, run_dir, wid, name = job
    a, b = run_dir / wid / name, rerun_dir / wid / name
    if not b.is_dir():
        return {"workload_id": wid, "run": name, "missing": True}
    t_same, line = same_trace(a / "trace.jsonl.gz", b / "trace.jsonl.gz")
    r_same = records_rows(a / "records.csv.gz") == records_rows(b / "records.csv.gz")
    return {"workload_id": wid, "run": name, "trace_same": t_same, "first_differing_line": line, "records_same": r_same}


def marked(scores, judging):
    out = set()
    with open(scores, newline="") as f:
        for r in csv.DictReader(f):
            if (r["level"] == "term" and r["condition"] == "oracle" and r["table"] == "prior" and not r["boot_default"]
                    and r["workload_id"] in judging and r["oracle_worse"] == "1"):
                out.add((r["workload_id"],) + tuple(r[k] for k in TERM))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--rerun", default=str(REPO / "runs" / "rq0-gate-rerun"))
    ap.add_argument("--run", default=str(REPO / "runs" / "rq0-gate"))
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    rerun_dir, run_dir = pathlib.Path(args.rerun), pathlib.Path(args.run)
    judging = sorted(d.name for d in rerun_dir.iterdir() if d.is_dir())
    jobs = [(rerun_dir, run_dir, w, r.name) for w in judging for r in sorted((rerun_dir / w).iterdir()) if r.is_dir()]
    with Pool(args.workers) as pool:
        rows = pool.map(one, jobs, chunksize=4)
    files = {}
    for r in rows:
        f = files.setdefault(r["workload_id"], {"runs": 0, "changed": []})
        f["runs"] += 1
        if r.get("missing") or not (r["trace_same"] and r["records_same"]):
            f["changed"].append(r["run"])
    before = marked(run_dir / "post-hoc" / "scores.csv", set(judging))
    after = marked(rerun_dir / "scores.csv", set(judging))
    out = {"runs": len(rows), "files": len(files),
           "changed_files": sorted(w for w, f in files.items() if f["changed"]),
           "per_file": {w: {"runs": f["runs"], "changed": len(f["changed"]),
                            "changed_conditions": sorted({c.split("~")[0].split("-")[0] for c in f["changed"]})}
                        for w, f in sorted(files.items())},
           "cases_at_primary": {"rq0_run": len(before), "rerun": len(after),
                                "new": [list(k) for k in sorted(after - before)],
                                "vanished": [list(k) for k in sorted(before - after)]}}
    (pathlib.Path(__file__).parent / "rerun-compare.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "per_file"}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
