#!/usr/bin/env python3
"""Run the variant deriver + coverage-grid generator over dataset/timelines.

Usage: derive.py [--check] [--repo ROOT]
  --check   re-derive and fail on drift against the committed derived
            timelines and coverage grid (CI gate; writes nothing)
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from wlc import deriver, grid  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])
    timelines = root / "dataset" / "timelines"

    errors = deriver.run(timelines, check=args.check)
    errors += grid.write(timelines, root / "dataset" / "coverage-grid.json",
                         check=args.check)
    if errors:
        print(f"{len(errors)} error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    coverage = grid.build_grid(timelines)
    print(("verified" if args.check else "derived") +
          f" — {coverage['segments_total']} segments on the grid")
    print(grid.render(coverage))
    return 0


if __name__ == "__main__":
    sys.exit(main())
