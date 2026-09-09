#!/usr/bin/env python3
"""scoring_lint: the scoring spec against its schema, the compiled coreset, and
the dataset's variant recipes (Phase 6 spec, decision 15).

    scoring_lint.py [--spec harness/scoring/scoring-spec.yaml]
                    [--build dataset/build/coreset-single] [--recipes dataset/timelines/coreset]

Exit 1 on any error."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.scoring import SCHEMA_PATH, SPEC_PATH, lint_spec, load_spec  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", default=str(SPEC_PATH))
    ap.add_argument("--schema", default=str(SCHEMA_PATH))
    ap.add_argument("--build", default=str(REPO / "dataset" / "build" / "coreset-single"))
    ap.add_argument("--recipes", default=str(REPO / "dataset" / "timelines" / "coreset"))
    args = ap.parse_args()
    errors = lint_spec(args.spec, args.schema, args.build, args.recipes)
    try:
        spec = load_spec(args.spec)
        files = spec.get("files", {}) if isinstance(spec, dict) else {}
        n_terms = sum(len(f.get("terms") or []) for f in files.values() if isinstance(f, dict))
        print(f"scoring spec: {len(files)} files, {n_terms} terms")
    except Exception:                                  # the lint already reported it
        pass
    for e in errors:
        print(f"  {e}")
    print("lint clean" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
