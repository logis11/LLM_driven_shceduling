"""Score records: records files (+ the scoring spec) → an aggregates CSV and a scores CSV.

    python3 tools/score.py --records RUN1.csv RUN2.csv … --out-aggregates a.csv --out-scores s.csv
    python3 tools/score.py --records DIR …                (every *.csv under DIR, recursively)

Every run's aggregates (metrics doc §8) are written whether a term scores them
or not; the scores file carries one row per term per run and one per run for
the file's weighted score (metrics doc §9; harness/scoring/scoring-spec.yaml).
A run whose workload has no scoring entry still gets its aggregates.
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness import aggregates as agg  # noqa: E402
from harness import records, scorer, scoring  # noqa: E402
from harness.outputs import write_csv  # noqa: E402


def windows_from_spec(spec, workload_id):
    """{(entity, metric): [(start_us, end_us), …]} named by the workload's terms."""
    out = {}
    entry = spec["files"].get(workload_id)
    if not entry:
        return out
    for term in entry["terms"]:
        w = term.get("window")
        if w:
            out.setdefault((term["entity"], term["metric"]), []).append((w["start_us"], w["end_us"]))
    return out


def interactive_from_spec(spec, workload_id):
    """The entities of the workload's `ready_wait` terms — the interactive tasks the excess aggregates measure."""
    entry = spec["files"].get(workload_id)
    if not entry:
        return ()
    return tuple(dict.fromkeys(t["entity"] for t in entry["terms"] if t["metric"] == "ready_wait"))


def collect(paths):
    files = []
    for p in paths:
        p = pathlib.Path(p)
        files.extend(sorted(p.rglob("*.csv")) if p.is_dir() else [p])
    return files


def aggregate_files(files, spec):
    rows = []
    for f in files:
        run_rows = records.read_csv(f)
        if not run_rows:
            continue
        wid = run_rows[0]["workload_id"]
        rows.extend(agg.compute_aggregates(run_rows, windows_from_spec(spec, wid), interactive_from_spec(spec, wid)))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True, help="records CSVs, or directories of them")
    ap.add_argument("--spec", default=str(scoring.SPEC_PATH))
    ap.add_argument("--out-aggregates", required=True)
    ap.add_argument("--out-scores", required=True)
    args = ap.parse_args()
    spec = scoring.load_spec(args.spec)
    agg_rows = aggregate_files(collect(args.records), spec)
    write_csv(agg_rows, agg.COLUMNS, args.out_aggregates)
    try:
        term_rows, file_rows = scorer.score(agg_rows, spec)
    except scorer.ScoringError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    write_csv(term_rows + file_rows, scorer.COLUMNS, args.out_scores)
    print(f"wrote {len(agg_rows)} aggregate rows to {args.out_aggregates}; "
          f"{len(term_rows)} term rows and {len(file_rows)} file rows to {args.out_scores}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
