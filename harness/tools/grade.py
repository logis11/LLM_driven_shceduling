#!/usr/bin/env python3
"""grade: recognition logs + ground truth (+ the driver table) → recognition
records CSVs and one grades CSV (sub-task 8.4).

    grade.py --manifest MANIFEST.json --out-grades GRADES.csv [--out-records DIR]
             [--seed N] [--repetitions N]

The manifest is JSON: {"driver_table": "<path>", "bootstrap": {"seed": N,
"repetitions": N}, "runs": [{"workload_id", "condition", "table", "seed",
"boot_default", "log", "workload", "driver_table"?}, …]}. Each run is one
recognition log; a run may name its own `driver_table`, otherwise the top-level
one is used. The runner (8.6) writes it.

Layer-1 numbers are pooled across workloads, so the whole run set is graded in
one invocation: the cluster bootstrap resamples files and the paired comparisons
need both conditions present. Consistency messages go to stderr — the oracle not
being perfect on a graded point is one — and the exit code is 2 when any fired.
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import grader, records  # noqa: E402
from harness.grader import COLUMNS, Bootstrap, GradeError, Run, compute_grades, grade_log  # noqa: E402
from harness.outputs import write_csv  # noqa: E402


def runs_from_manifest(doc):
    table = doc.get("driver_table")
    out = []
    for i, r in enumerate(doc.get("runs") or []):
        try:
            own = r.get("driver_table", table)
            out.append(Run(workload_id=r["workload_id"], condition=r["condition"],
                           table=str(r.get("table", "")), seed=str(r.get("seed", "")),
                           boot_default=str(r.get("boot_default", "")),
                           log=pathlib.Path(r["log"]), workload=pathlib.Path(r["workload"]),
                           table_path=pathlib.Path(own) if own else None))
        except KeyError as exc:
            raise GradeError(f"manifest run {i}: missing {exc}") from None
    if not out:
        raise GradeError("manifest lists no runs")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out-grades", required=True, dest="out_grades")
    ap.add_argument("--out-records", default=None, dest="out_records",
                    help="directory for one recognition records CSV per run")
    ap.add_argument("--seed", type=int, default=None, help="overrides the manifest's")
    ap.add_argument("--repetitions", type=int, default=None, help="overrides the manifest's")
    args = ap.parse_args()

    with open(args.manifest, "r", encoding="utf-8") as f:
        doc = json.load(f)
    boot = doc.get("bootstrap") or {}
    bootstrap = Bootstrap(seed=args.seed if args.seed is not None
                          else int(boot.get("seed", grader.BOOTSTRAP_SEED)),
                          repetitions=args.repetitions if args.repetitions is not None
                          else int(boot.get("repetitions", grader.BOOTSTRAP_REPETITIONS)))
    try:
        runs = runs_from_manifest(doc)
        rows, messages = [], []
        out_dir = pathlib.Path(args.out_records) if args.out_records else None
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
        for run in runs:
            run_rows, run_messages = grade_log(run)
            records.validate_rows(run_rows)
            rows.extend(run_rows)
            messages.extend(run_messages)
            if out_dir is not None:
                records.write_csv(run_rows, out_dir / f"{run.condition}--{run.workload_id}.csv")
        grades = compute_grades(rows, bootstrap=bootstrap)
    except (GradeError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    write_csv(grades, COLUMNS, args.out_grades)
    for m in messages:
        print(f"consistency: {m}", file=sys.stderr)
    print(f"graded {len(rows)} recognition rows from {len(runs)} run(s); "
          f"wrote {len(grades)} rows to {args.out_grades}")
    return 2 if messages else 0


if __name__ == "__main__":
    sys.exit(main())
