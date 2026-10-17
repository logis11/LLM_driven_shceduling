#!/usr/bin/env python3
"""scoring_lint: the scoring spec against its schema, the compiled coreset, and
the dataset's variant recipes (Phase 6 spec, decision 15); the generated-layer
rule's entries against each generated set's compiled files (9.21 decision 1),
one manifest per set `dataset/grids.yaml` names.

    scoring_lint.py [--spec harness/scoring/scoring-spec.yaml]
                    [--build dataset/build/coreset-single] [--recipes dataset/timelines/coreset]
                    [--grids dataset/grids.yaml | --no-generated]

Exit 1 on any error."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import yaml  # noqa: E402

from harness import manifests  # noqa: E402
from harness.scoring import SCHEMA_PATH, SPEC_PATH, generated_entries, lint_generated, lint_spec, load_spec  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]


def generated_manifests(grids_path):
    """One committed manifest per set the grid definition names, beside it."""
    grids_path = pathlib.Path(grids_path)
    if not grids_path.is_file():
        return []
    sets = (yaml.safe_load(grids_path.read_text()) or {}).get("sets") or {}
    return [grids_path.parent / f"build.{name}.manifest.json" for name in sets]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", default=str(SPEC_PATH))
    ap.add_argument("--schema", default=str(SCHEMA_PATH))
    ap.add_argument("--build", default=str(REPO / "dataset" / "build" / "coreset-single"))
    ap.add_argument("--recipes", default=str(REPO / "dataset" / "timelines" / "coreset"))
    ap.add_argument("--grids", default=str(REPO / "dataset" / "grids.yaml"))
    ap.add_argument("--no-generated", action="store_true", help="skip the generated-layer rule's lint")
    args = ap.parse_args()
    errors = lint_spec(args.spec, args.schema, args.build, args.recipes)
    spec = None
    try:
        spec = load_spec(args.spec)
        files = spec.get("files", {}) if isinstance(spec, dict) else {}
        n_terms = sum(len(f.get("terms") or []) for f in files.values() if isinstance(f, dict))
        print(f"scoring spec: {len(files)} files, {n_terms} terms")
    except Exception:                                  # the lint already reported it
        pass
    if not errors and not args.no_generated and isinstance(spec, dict):
        for manifest_path in generated_manifests(args.grids):
            set_errors = lint_generated(spec, manifest_path)
            errors.extend(set_errors)
            if not set_errors:
                entries = generated_entries(spec, manifests.load(manifest_path))
                n_terms = sum(len(e["terms"]) for e in entries.values())
                print(f"generated {manifest_path.name[len('build.'):-len('.manifest.json')]}: "
                      f"{len(entries)} files with terms, {n_terms} terms by the rule")
    for e in errors:
        print(f"  {e}")
    print("lint clean" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
