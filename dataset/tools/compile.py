#!/usr/bin/env python3
"""Compile every timeline to canonical form and write the build manifest.

Usage: compile.py [--check] [--repo ROOT]
  --check   recompile and fail if dataset/build.manifest.json would change
            (CI determinism / drift gate; writes nothing)
"""

import argparse
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from wlc import Library, Timeline, TimelineError, compile_timeline  # noqa: E402
from wlc.compiler import MODES, canonical_bytes  # noqa: E402
from wlc.linter import lint_canonical, load_schema  # noqa: E402


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def discover(timelines_dir):
    return sorted(timelines_dir.glob("**/*.timeline.yaml"))


def artifact_set(timelines_dir, path):
    relative = path.relative_to(timelines_dir)
    return relative.parts[0] if len(relative.parts) > 1 else "adhoc"


def build_all(root):
    """Returns (manifest_dict, artifacts {relpath: bytes}, errors, reports)."""
    dataset = root / "dataset"
    library = Library(dataset / "archetypes.yaml")
    schema = load_schema(dataset / "schema" / "workload.schema.json")
    timelines_dir = dataset / "timelines"

    artifacts, errors, reports = {}, [], []
    for path in discover(timelines_dir):
        rel_path = path.relative_to(root).as_posix()
        try:
            timeline = Timeline(path, library)
        except TimelineError as err:
            errors.append(str(err))
            continue
        for mode in MODES:
            canonical, report = compile_timeline(timeline, library, mode,
                                                 rel_path=rel_path)
            errors.extend(lint_canonical(
                canonical, schema, report=report, mode=mode,
                name=f"{timeline.id}[{mode}]"))
            out = (f"{artifact_set(timelines_dir, path)}-{mode}/"
                   f"{timeline.id}.workload.json")
            artifacts[out] = canonical_bytes(canonical)
            reports.append((timeline.id, mode, report))

    manifest = {
        "inputs": {
            "dataset/archetypes.yaml":
                sha256((dataset / "archetypes.yaml").read_bytes()),
            "dataset/schema/workload.schema.json":
                sha256((dataset / "schema" / "workload.schema.json").read_bytes()),
        },
        "artifacts": {rel: sha256(data)
                      for rel, data in sorted(artifacts.items())},
    }
    return manifest, artifacts, errors, reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])

    manifest, artifacts, errors, reports = build_all(root)
    for timeline_id, mode, report in reports:
        print(f"  {timeline_id}[{mode}]: demand {report['utilization']:.2f} "
              f"({report['demand_class']})")
    if errors:
        print(f"{len(errors)} error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1

    manifest_path = root / "dataset" / "build.manifest.json"
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True)
                      + "\n").encode()
    if args.check:
        if not manifest_path.exists():
            print("no committed manifest to check against", file=sys.stderr)
            return 1
        if manifest_path.read_bytes() != manifest_bytes:
            print("build.manifest.json drift: recompiled artifacts do not "
                  "match the committed manifest", file=sys.stderr)
            return 1
        print(f"manifest verified ({len(artifacts)} artifacts)")
        return 0

    build_dir = root / "dataset" / "build"
    for rel, data in artifacts.items():
        out_path = build_dir / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(data)
    manifest_path.write_bytes(manifest_bytes)
    print(f"wrote {len(artifacts)} artifacts + manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
