#!/usr/bin/env python3
"""evaluate: the RQ0 gate evaluator — a per-experiment spec and the harness's four
output files → the report and its rendering (sub-task 8.7).

    evaluate.py --spec EXPERIMENT.yaml --aggregates A.csv --scores S.csv --guards G.csv --grades R.csv
                --out-report REPORT.json --out-render REPORT.md [--root REPO]

Pins in the spec resolve against `--root` (default: the repository). A pin
mismatch, an incomplete run set, or an unregistered type is a refusal: exit 1,
nothing written. Otherwise both files are written and the exit code follows the
verdict: 0 on pass, 2 on fail or invalid."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.evaluator import GateError, evaluate, render, validate_report, write_report  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--aggregates", required=True)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--guards", required=True)
    ap.add_argument("--grades", required=True)
    ap.add_argument("--out-report", required=True, dest="out_report")
    ap.add_argument("--out-render", required=True, dest="out_render")
    ap.add_argument("--root", default=str(REPO))
    args = ap.parse_args()
    try:
        report = evaluate(args.spec, args.aggregates, args.scores, args.guards, args.grades, args.root)
        validate_report(report)
    except (GateError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    write_report(report, args.out_report)
    pathlib.Path(args.out_render).write_text(render(report), encoding="utf-8")
    d = report["verdict_detail"]
    print(f"verdict: {report['verdict']} — {d['met']} of {d['judging']} judging files met the criterion "
          f"(K = {d['k']}); wrote {args.out_report} and {args.out_render}")
    return 0 if report["verdict"] == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
