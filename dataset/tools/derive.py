#!/usr/bin/env python3
"""Run the variant deriver + coverage-grid generator over dataset/timelines, the generated layer's coverage tables
over its committed manifests (9.21 decision 4).

Usage: derive.py [--check] [--require-coverage] [--repo ROOT]
  --check             re-derive and fail on drift against the committed
                      derived timelines and coverage grid (CI gate; writes
                      nothing)
  --require-coverage  fail when any driver-table cell has no segment (the
                      all-32-cells requirement, Phase 7 spec decision 11).
                      The empty-cell report prints on every run regardless;
                      the Makefile's check target adopts the flag once the
                      coreset is meant to satisfy it (7.3).
"""

import argparse
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from gen import coverage  # noqa: E402
from wlc import deriver, grid  # noqa: E402


def generated_manifests(root):
    """One committed manifest per set the grid definition names: `dataset/build.<set>.manifest.json`."""
    grids = root / "dataset" / "grids.yaml"
    if not grids.is_file():
        return []
    sets = (yaml.safe_load(grids.read_text()) or {}).get("sets") or {}
    return [root / "dataset" / f"build.{name}.manifest.json" for name in sets]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--require-coverage", action="store_true")
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])
    timelines = root / "dataset" / "timelines"

    errors = deriver.run(timelines, check=args.check)
    errors += coverage.write(timelines, generated_manifests(root), root / "dataset" / "coverage-grid.json",
                             check=args.check)
    if args.require_coverage and not errors:
        errors += grid.coverage_errors(grid.build_grid(timelines))
    if errors:
        print(f"{len(errors)} error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    table = coverage.build(timelines, generated_manifests(root))
    print(("verified" if args.check else "derived") +
          f" — {table['segments_total']} segments on the grid")
    print(grid.render(table) + coverage.render_generated(table["generated"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
