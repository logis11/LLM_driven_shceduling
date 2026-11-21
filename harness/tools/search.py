#!/usr/bin/env python3
"""search: the configuration search — a search spec and a machine configuration → the boot default's and the
row's points run and checked against the corrected runs, every point of the grid on every file the spec names, the
reading, and the report (the RQ0 gate spec's statement `failure-procedure`; sub-task 11.4).

    search.py --spec experiments/rq0-config-search.yaml --machine MACHINE.yaml [--workers N] [--heavy-workers N]
              [--quiet] [--root REPO] [--checks-only | --read-only] [--out-dir DIR]

Outputs land under the machine configuration's runs directory, in `<search>/`: the points' tables, one directory
per file and point, `checks.json`, then `aggregates.csv.gz`, `guards.csv`, `waits.csv`, `points.csv`,
`run-times.csv`, `report.json` and `report.md`. `--checks-only` stops after decision 10's checks; `--read-only`
reads the report again from `points.csv` and `checks.json`, running nothing. `--out-dir` also writes the report and
its rendering there (the committed copy beside the spec). One line per finished run goes to stderr unless `--quiet`.
Exit 1 when the spec is refused, a run failed or a check did not reproduce its run; otherwise 0."""
import argparse
import dataclasses
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.runner import RunError, load_machine  # noqa: E402
from harness.search import SearchError, read, render, search, write_report  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def print_progress(done, total, run, out, err=sys.stderr):
    if "failure" in out:
        what = "FAILED: " + out["failure"]
    else:
        what = f"{'records from the cache' if out['results_cached'] else 'built'} in {out['seconds']:.0f} s"
    print(f"[{done}/{total}] {run.workload_id}/{run.name} {what}", file=err, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--spec", required=True)
    ap.add_argument("--machine", required=True)
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--heavy-workers", type=int, default=None)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--root", default=str(REPO))
    ap.add_argument("--checks-only", action="store_true")
    ap.add_argument("--read-only", action="store_true")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()
    try:
        machine = load_machine(args.machine, args.root)
        if args.workers is not None:
            machine = dataclasses.replace(machine, workers=args.workers)
        if args.heavy_workers is not None:
            machine = dataclasses.replace(machine, heavy_workers=args.heavy_workers)
        from harness.search import load_spec
        exp_dir = machine.runs_dir / load_spec(args.spec)["search"]
        if args.read_only:
            report = read(args.spec, exp_dir, args.root, machine.build_dir, machine.boot_defaults_dir)
        else:
            result = search(args.spec, machine, args.root, progress=None if args.quiet else print_progress,
                            only_checks=args.checks_only)
            for c in result.checks:
                print(f"check {c['workload_id']} {c['check']}: {'reproduced' if c['reproduced'] else 'NOT reproduced'}",
                      file=sys.stderr)
            if result.failed:
                print(f"{len(result.failed)} run(s) failed:", file=sys.stderr)
                for f in result.failed:
                    print(f"  {f}", file=sys.stderr)
            if result.stopped:
                print(f"stopped: {result.stopped}", file=sys.stderr)
                return 1
            if result.report is None:
                return 0
            report = result.report
    except (SearchError, RunError, OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for d in [exp_dir] + ([pathlib.Path(args.out_dir)] if args.out_dir else []):
        d.mkdir(parents=True, exist_ok=True)
        write_report(report, d / "report.json")
        (d / "report.md").write_text(render(report), encoding="utf-8")
    r = report["route"]
    print(f"route: {r['route']} — files at finding 3: {', '.join(r['files_at_3']) or 'none'}; report in "
          f"{exp_dir / 'report.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
