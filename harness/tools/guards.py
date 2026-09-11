#!/usr/bin/env python3
"""guards: a run set (manifest) + the aggregates file → the guards CSV (sub-task 8.3).

    guards.py --manifest MANIFEST.json --out GUARDS.csv
              [--spec harness/guards/guard-spec.yaml] [--scoring-spec harness/scoring/scoring-spec.yaml]

The manifest is JSON: {"aggregates": "<aggregates csv>", "scoring_spec": "<optional path>",
"runs": [{"workload_id", "condition", "table", "seed", "boot_default", "records",
"schedule", "log", "workload", "rerun_trace", "guard_messages": [...]}, …]} — identity plus
the paths each run's guards read; a missing path is a missing input and that guard fails.
The runner (8.6) writes it. Every run gets one row per guard. Exit 2 when any guard failed."""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import aggregates as agg  # noqa: E402
from harness import scoring  # noqa: E402
from harness.guards import COLUMNS, SPEC_PATH, GuardError, Run, evaluate, load_spec  # noqa: E402
from harness.outputs import read_csv, write_csv  # noqa: E402

_PATHS = ("records", "schedule", "log", "workload", "rerun_trace")


def runs_from_manifest(doc):
    runs = []
    for i, r in enumerate(doc.get("runs") or []):
        try:
            paths = {k: (pathlib.Path(r[k]) if r.get(k) else None) for k in _PATHS}
            runs.append(Run(workload_id=r["workload_id"], condition=r["condition"],
                            table=str(r.get("table", "")), seed=str(r.get("seed", "")),
                            boot_default=str(r.get("boot_default", "")),
                            guard_messages=r.get("guard_messages"), **paths))
        except KeyError as exc:
            raise GuardError(f"manifest run {i}: missing {exc}") from None
    if not runs:
        raise GuardError("manifest lists no runs")
    if runs[0].records is None or any(x.records is None for x in runs):
        raise GuardError("every manifest run names its records file")
    return runs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--spec", default=str(SPEC_PATH))
    ap.add_argument("--scoring-spec", default=None, dest="scoring_spec",
                    help="overrides the manifest's; default the committed scoring spec")
    args = ap.parse_args()
    with open(args.manifest, "r", encoding="utf-8") as f:
        doc = json.load(f)
    spec = load_spec(args.spec)
    scoring_path = args.scoring_spec or doc.get("scoring_spec") or str(scoring.SPEC_PATH)
    scoring_spec = scoring.load_spec(scoring_path)
    try:
        runs = runs_from_manifest(doc)
        if not doc.get("aggregates"):
            raise GuardError("manifest names no aggregates file")
        aggregates = read_csv(doc["aggregates"], agg.COLUMNS)
        rows = evaluate(runs, spec, aggregates, scoring_spec)
    except (GuardError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    write_csv(rows, COLUMNS, args.out)
    n = {k: sum(1 for r in rows if r["result"] == k) for k in ("pass", "fail", "not_applicable")}
    print(f"wrote {len(rows)} rows to {args.out}: {n['pass']} pass, {n['fail']} fail, "
          f"{n['not_applicable']} not_applicable")
    return 2 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
