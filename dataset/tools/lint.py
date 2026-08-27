#!/usr/bin/env python3
"""Dataset linter CLI — repo lints, timeline lints, in-memory compile lints.

Usage: lint.py [--freeze] [--repo ROOT]
  --freeze   reject meas-pending source tags (schema-freeze gate)
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from wlc import Library, Timeline, TimelineError, compile_timeline  # noqa: E402
from wlc.compiler import MODES  # noqa: E402
from wlc.linter import lint_canonical, lint_repo, load_schema  # noqa: E402


def run(root, freeze=False):
    dataset = root / "dataset"
    errors = lint_repo(dataset / "archetypes.yaml", dataset / "sources.yaml",
                       root / "docs" / "references.md", freeze=freeze)
    library = Library(dataset / "archetypes.yaml")
    schema = load_schema(dataset / "schema" / "workload.schema.json")
    for path in sorted((dataset / "timelines").glob("**/*.timeline.yaml")):
        try:
            timeline = Timeline(path, library)
        except TimelineError as err:
            errors.append(str(err))
            continue
        for mode in MODES:
            canonical, report = compile_timeline(timeline, library, mode)
            errors.extend(lint_canonical(canonical, schema, report=report,
                                         mode=mode,
                                         name=f"{timeline.id}[{mode}]"))
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
