#!/usr/bin/env python3
"""experiment_lint: a per-experiment spec against its schema, the compiled files,
the pinned scoring spec's terms, the guard registry, the registries of criterion
and reporting-line types, and the pins' bytes (sub-task 8.7).

    experiment_lint.py [--spec EXPERIMENT.yaml] [--build dataset/build/coreset-single] [--root REPO]

Without --spec, every spec under harness/experiments/ is linted. Exit 1 on any error.

An executed spec — one whose run record is committed beside it, `<experiment>/runs.sha256.csv` — is linted the
same way but for its pins: they name the tree its run read, so a pin the working tree no longer matches is printed
as a note, not an error (the harness changelog, 2026-11-20)."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.evaluator import EXPERIMENTS, SPEC_SCHEMA, lint_spec, load_spec  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def run_record(spec_path, spec):
    """The committed record of the spec's run, `<the spec's directory>/<experiment>/runs.sha256.csv`, or None."""
    path = pathlib.Path(spec_path).parent / str((spec or {}).get("experiment")) / "runs.sha256.csv"
    return path if path.is_file() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--spec", default=None)
    ap.add_argument("--schema", default=str(SPEC_SCHEMA))
    ap.add_argument("--build", default=str(REPO / "dataset" / "build" / "coreset-single"))
    ap.add_argument("--root", default=str(REPO))
    args = ap.parse_args()
    specs = [pathlib.Path(args.spec)] if args.spec else sorted(EXPERIMENTS.glob("*.yaml"))
    if not specs:
        print("no experiment specs under harness/experiments/")
        return 0
    total = 0
    for spec_path in specs:
        errors = lint_spec(spec_path, args.schema, args.build, args.root)
        record = None
        try:
            spec = load_spec(spec_path)
            record = run_record(spec_path, spec)
            files = spec.get("files") or {}
            print(f"{spec_path.name}: experiment {spec.get('experiment')}, {len(spec.get('conditions') or [])} "
                  f"conditions, {len(files.get('judging') or [])} judging + {len(files.get('reporting') or [])} "
                  f"reporting files, criterion {(spec.get('criterion') or {}).get('type')}"
                  + (f"; executed, its run recorded in {record.parent.name}/{record.name}" if record else ""))
        except Exception:                              # the lint already reported it
            pass
        notes = [e for e in errors if record and e.startswith("pins/")]
        errors = [e for e in errors if e not in notes]
        for e in errors:
            print(f"  {e}")
        for n in notes:
            print(f"  note: {n} — the pin names the tree the run read")
        total += len(errors)
    print("lint clean" if not total else f"{total} error(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
