#!/usr/bin/env python3
"""Dataset linter CLI — the checks before a compile: repo lints, timeline lints and the grid definition's.

The canonical lints run inside the compile, on every artifact as it is built
(compile.py, variants.py); a `lint` pass repeats none of it (9.22 spec, decision 2).

Usage: lint.py [--freeze] [--repo ROOT]
  --freeze   reject meas-pending source tags (schema-freeze gate)
"""

import argparse
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from wlc import Library, Timeline, TimelineError  # noqa: E402
from gen import lint_grids  # noqa: E402
from wlc.linter import lint_bound_sources, lint_repo  # noqa: E402


def run(root, freeze=False):
    dataset = root / "dataset"
    errors = lint_repo(dataset / "archetypes.yaml", dataset / "sources.yaml",
                       root / "docs" / "references.md", freeze=freeze)
    library = Library(dataset / "archetypes.yaml")
    registry = yaml.safe_load((dataset / "sources.yaml").read_text())["sources"]
    for path in sorted((dataset / "timelines").glob("**/*.timeline.yaml")):
        errors.extend(lint_bound_sources(path, registry))   # 9.18: every bound value tagged or labelled
        try:
            Timeline(path, library)
        except TimelineError as err:
            errors.append(str(err))
    errors.extend(lint_grids(dataset / "grids.yaml", registry))   # 9.19: the generated layer's definition and its interval sources
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])
    errors = run(root, freeze=args.freeze)
    if errors:
        print(f"{len(errors)} lint error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    print("lint clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
