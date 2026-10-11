#!/usr/bin/env python3
"""Compile every timeline to canonical form and write the build manifest.

Usage: compile.py [--check] [--repo ROOT]
  --check   recompile and fail if dataset/build.manifest.json would change
            (CI determinism / drift gate; writes nothing)

Every artifact is written with its compile report beside it (`<id>.report.json`);
the manifest pins both, and its `inputs` pin by content everything the compile
reads besides the timelines: the library, the schema, the compiler's sources and
the stimulus and replay streams (9.18 spec, decisions 5 and 8).
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


def report_path(artifact_rel):
    """The compile report's path beside its artifact: `<set>-<mode>/<id>.report.json`."""
    assert artifact_rel.endswith(".workload.json"), artifact_rel
    return artifact_rel[:-len(".workload.json")] + ".report.json"


def report_bytes(report):
    """The byte form of a compile report the manifest hashes (9.18 spec, decision 8)."""
    return (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()


def input_files(root):
    """The files the compile reads besides the timelines, pinned by content in the manifest's `inputs` (9.18 spec,
    decision 5): the library, the schema, the compiler's sources, the stimulus and replay streams."""
    dataset = root / "dataset"
    files = [dataset / "archetypes.yaml", dataset / "schema" / "workload.schema.json",
             dataset / "tools" / "compile.py"]
    files += sorted((dataset / "tools" / "wlc").glob("*.py"))
    files += sorted((dataset / "stimulus").glob("*.jsonl"))
    files += sorted((dataset / "replay").glob("*.json.gz"))
    return files


def build_all(root):
    """Returns (manifest_dict, artifacts {relpath: bytes}, errors, reports)."""
    dataset = root / "dataset"
    library = Library(dataset / "archetypes.yaml")
    schema = load_schema(dataset / "schema" / "workload.schema.json")
    timelines_dir = dataset / "timelines"

    artifacts, demand, errors, reports, report_of = {}, {}, [], [], {}
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
            demand[out] = {"utilization": round(report["utilization"], 4),
                           "demand_class": report["demand_class"],
                           "segments": [{"index": seg["index"], "t_start_us": seg["t_start_us"],
                                         "t_end_us": seg["t_end_us"],
                                         "utilization": round(seg["utilization"], 4)}
                                        for seg in report["per_segment"]]}
            reports.append((timeline.id, mode, report))
            report_of[out] = report

    manifest = {
        "inputs": {path.relative_to(root).as_posix(): sha256(path.read_bytes()) for path in input_files(root)},
        "artifacts": {rel: sha256(data)
                      for rel, data in sorted(artifacts.items())},
        "demand": {rel: demand[rel] for rel in sorted(demand)},
        "reports": {rel: sha256(report_bytes(report)) for rel, report in sorted(report_of.items())},
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
    for timeline_id, mode, report in reports:
        rel = next(r for r in artifacts if r.endswith(f"-{mode}/{timeline_id}.workload.json"))
        (build_dir / report_path(rel)).write_bytes(report_bytes(report))
    manifest_path.write_bytes(manifest_bytes)
    print(f"wrote {len(artifacts)} artifacts + reports + manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
