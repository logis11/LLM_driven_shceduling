#!/usr/bin/env python3
"""run: the runner — a per-experiment spec and a machine configuration → every
run of the matrix invoked through the invocation contract (twice, cached), the
records, aggregates, scores, guards, grades, and the report (sub-task 8.6).

    run.py --spec EXPERIMENT.yaml --machine MACHINE.yaml [--workers N] [--quiet] [--root REPO]

Outputs land under the machine configuration's runs directory, one directory
per experiment, workload, and run. `--workers` overrides the configuration's
number of runs at once; one line per finished run goes to stderr unless
`--quiet`. Exit 1 when any run failed (the failed runs
are named, nothing is scored) or the spec is refused; otherwise the exit code
follows the verdict: 0 on pass, 2 on fail or invalid."""
import argparse
import dataclasses
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
          f"{result.results_cached} run(s) of records from the results cache; "
          f"report in {result.experiment_dir / 'report.json'}", file=out)
    return 0 if result.report["verdict"] == "pass" else 2


def print_progress(done, total, run, out, err=sys.stderr):
    """One line per finished run: how far, which run, and whether its records were built or served."""
    if "failure" in out:
        what = "FAILED: " + out["failure"]
    else:
        what = f"{'records from the cache' if out['results_cached'] else 'built'} in {out['seconds']:.0f} s"
    print(f"[{done}/{total}] {run.workload_id}/{run.name} {what}", file=err, flush=True)


def with_workers(machine, workers):
    return machine if workers is None else dataclasses.replace(machine, workers=workers)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--machine", required=True)
    ap.add_argument("--workers", type=int, default=None, help="runs at once (overrides the machine configuration)")
    ap.add_argument("--quiet", action="store_true", help="no line per finished run")
    ap.add_argument("--root", default=str(REPO))
    args = ap.parse_args()
    try:
        machine = with_workers(load_machine(args.machine, args.root), args.workers)
        result = run_experiment(args.spec, machine, args.root, progress=None if args.quiet else print_progress)
    except (GateError, RunError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return report_result(result)


if __name__ == "__main__":
    sys.exit(main())
