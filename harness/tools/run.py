#!/usr/bin/env python3
"""run: the runner — a per-experiment spec and a machine configuration → every
run of the matrix invoked through the invocation contract (twice, cached), the
records, aggregates, scores, guards, grades, and the report (sub-task 8.6).

    run.py --spec EXPERIMENT.yaml --machine MACHINE.yaml [--root REPO]

Outputs land under the machine configuration's runs directory, one directory
per experiment, workload, and run. Exit 1 when any run failed (the failed runs
are named, nothing is scored) or the spec is refused; otherwise the exit code
follows the verdict: 0 on pass, 2 on fail or invalid."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.evaluator import GateError  # noqa: E402
from harness.runner import RunError, load_machine, run_experiment  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def report_result(result, out=sys.stdout):
    if result.failed:
        print(f"{len(result.failed)} run(s) failed; nothing scored:", file=sys.stderr)
        for f in result.failed:
            print(f"  {f.run}: {f.reason}", file=sys.stderr)
        return 1
    d = result.report["verdict_detail"]
    print(f"verdict: {result.report['verdict']} — {d['met']} of {d['judging']} judging files met the "
          f"criterion (K = {d['k']}); {result.executed} invocation(s) executed, {result.cached} from the cache; "
          f"report in {result.experiment_dir / 'report.json'}", file=out)
    return 0 if result.report["verdict"] == "pass" else 2


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--machine", required=True)
    ap.add_argument("--root", default=str(REPO))
    args = ap.parse_args()
    try:
        machine = load_machine(args.machine, args.root)
        result = run_experiment(args.spec, machine, args.root)
    except (GateError, RunError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return report_result(result)


if __name__ == "__main__":
    sys.exit(main())
