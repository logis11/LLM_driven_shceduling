#!/usr/bin/env python3
"""The post hoc scores against the RQ0 run's own, row by row (11.1 spec, decision 1).

    python3 scores_check.py [--run runs/rq0-gate/scores.csv] [--post-hoc runs/rq0-gate/post-hoc/scores.csv]

Rows are matched on their identity and term columns. A row is marked when it reads an oracle worse than fixed —
`oracle_worse` 1 on a term row, `n_oracle_worse` above 0 on a file row. Every unmarked row must equal the run's in
every column the run's file has; the counts go to `scores-check.json` beside this script."""
import argparse
import csv
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
KEY = ["workload_id", "condition", "table", "seed", "boot_default", "telemetry", "level", "entity", "metric",
       "aggregate", "cause", "channel", "window_start_us", "window_end_us"]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, {tuple(row[k] for k in KEY): row for row in r}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", default=str(REPO / "runs" / "rq0-gate" / "scores.csv"))
    ap.add_argument("--post-hoc", dest="post_hoc", default=str(REPO / "runs" / "rq0-gate" / "post-hoc" / "scores.csv"))
    args = ap.parse_args()
    run_cols, run = load(args.run)
    new_cols, new = load(args.post_hoc)
    out = {"run_rows": len(run), "post_hoc_rows": len(new), "same_rows": run.keys() == new.keys(),
           "added_columns": [c for c in new_cols if c not in run_cols],
           "dropped_columns": [c for c in run_cols if c not in new_cols],
           "marked": {"term": 0, "file": 0}, "marked_changed": 0, "unmarked": 0, "unmarked_changed": 0}
    for k, n in new.items():
        o = run.get(k)
        if o is None:
            continue
        marked = n["oracle_worse"] == "1" if n["level"] == "term" else n["n_oracle_worse"] not in ("", "0")
        changed = any(o[c] != n[c] for c in run_cols)
        if marked:
            out["marked"][n["level"]] += 1
            out["marked_changed"] += int(changed)
        else:
            out["unmarked"] += 1
            out["unmarked_changed"] += int(changed)
    out["ok"] = (out["same_rows"] and not out["dropped_columns"] and out["unmarked_changed"] == 0)
    (pathlib.Path(__file__).parent / "scores-check.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
