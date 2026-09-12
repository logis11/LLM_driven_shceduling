#!/usr/bin/env python3
"""smoke: the full pipeline on the mocks over the compiled coreset (sub-task 8.6,
decisions 7–8) — a throwaway experiment spec generated from the files as they
are, run through `run.py`'s path, and discarded.

    smoke.py [--machine harness/runner.example.yaml] [--files N] [--root REPO]

`--files N` limits the judging set to the first N scored files (the test suite
uses a handful; the make target runs them all). The smoke checks the plumbing,
not the mocks' verdict, which is `invalid` by construction (c6-dual's oracle runs
on fallback and the spec exempts nothing): exit 0 once a report was written,
1 when a run failed or the spec was refused. The verdict is printed."""
import argparse
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.evaluator import GateError  # noqa: E402
from harness.runner import RunError, load_machine, run_experiment, write_smoke_spec  # noqa: E402
from run import report_result  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--machine", default=str(REPO / "harness" / "runner.example.yaml"))
    ap.add_argument("--files", type=int, default=None)
    ap.add_argument("--root", default=str(REPO))
    args = ap.parse_args()
    try:
        machine = load_machine(args.machine, args.root)
        with tempfile.TemporaryDirectory() as tmp:
            spec = write_smoke_spec(pathlib.Path(tmp) / "smoke.yaml", machine, args.root, files=args.files)
            print(f"smoke spec: {len(spec.read_text().splitlines())} lines, discarded after the run")
            result = run_experiment(spec, machine, args.root)
    except (GateError, RunError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    code = report_result(result)
    return 1 if code == 1 else 0            # a report was written: the plumbing held


if __name__ == "__main__":
    sys.exit(main())
