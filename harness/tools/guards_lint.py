#!/usr/bin/env python3
"""guards_lint: the guard spec against its schema, the code's registry, and the
dataset's C2 variant recipe (sub-task 8.3 spec, decision 2).

    guards_lint.py [--spec harness/guards/guard-spec.yaml] [--recipes dataset/timelines/coreset]

Exit 1 on any error."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.guards import SCHEMA_PATH, SPEC_PATH, lint_spec, load_spec  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", default=str(SPEC_PATH))
    ap.add_argument("--schema", default=str(SCHEMA_PATH))
    ap.add_argument("--recipes", default=str(REPO / "dataset" / "timelines" / "coreset"))
    args = ap.parse_args()
    errors = lint_spec(args.spec, args.schema, args.recipes)
    try:
        spec = load_spec(args.spec)
        print(f"guard spec {spec.get('version')}: {len(spec.get('guards') or [])} guards, "
              f"{len(spec.get('pairs') or [])} C2 pairs")
    except Exception:                                  # the lint already reported it
        pass
    for e in errors:
        print(f"  {e}")
    print("lint clean" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
