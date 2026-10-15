#!/usr/bin/env python3
"""Compile every timeline to canonical form and write the build manifest.

Usage: compile.py [--check] [--jobs N] [--repo ROOT]
  --check   recompile and fail if dataset/build.manifest.json would change
            (an independent verification; the gate compares the manifest the
            build wrote with the committed one — check_build.py; 9.22)
  --jobs N  worker processes, one timeline each (default: the CPU count)

Every artifact is written with its compile report beside it (`<id>.report.json`);
the manifest pins both, and its `inputs` pin by content everything the compile
reads besides the timelines: the library, the schema, the compiler's sources and
the stimulus and replay streams (9.18 spec, decisions 5 and 8).
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
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
    decision 5): the library, the schema, the compiler's sources, the stimulus, launch and replay streams (the launch
    streams 9.23 B1)."""
    dataset = root / "dataset"
    files = [dataset / "archetypes.yaml", dataset / "schema" / "workload.schema.json",
             dataset / "tools" / "compile.py"]
    files += sorted((dataset / "tools" / "wlc").glob("*.py"))
    files += sorted((dataset / "stimulus").glob("*.jsonl"))
    files += sorted((dataset / "launch").glob("*.json.gz"))
    files += sorted((dataset / "replay").glob("*.json.gz"))
    return files


_PER_PROCESS = {}   # root -> (library, schema), loaded once per worker process


def _tools(root):
    if root not in _PER_PROCESS:
        dataset = root / "dataset"
        _PER_PROCESS[root] = (Library(dataset / "archetypes.yaml"),
                              load_schema(dataset / "schema" / "workload.schema.json"))
    return _PER_PROCESS[root]


def compile_one(root, path):
    """One timeline in every mode: (errors, [(out, artifact bytes, demand entry, report, timeline id, mode)]).
    Pure in its inputs, so the timelines compile in parallel (9.22) and in any order; the manifest sorts."""
    root, path = pathlib.Path(root), pathlib.Path(path)
    library, schema = _tools(root)
    timelines_dir = root / "dataset" / "timelines"
    rel_path = path.relative_to(root).as_posix()
    try:
        timeline = Timeline(path, library)
    except TimelineError as err:
        return [str(err)], []
    errors, built = [], []
    for mode in MODES:
        canonical, report = compile_timeline(timeline, library, mode, rel_path=rel_path)
        errors.extend(lint_canonical(canonical, schema, report=report, mode=mode,
                                     name=f"{timeline.id}[{mode}]"))
        out = f"{artifact_set(timelines_dir, path)}-{mode}/{timeline.id}.workload.json"
        demand = {"utilization": round(report["utilization"], 4),
                  "demand_class": report["demand_class"],
                  "segments": [{"index": seg["index"], "t_start_us": seg["t_start_us"],
                                "t_end_us": seg["t_end_us"],
                                "utilization": round(seg["utilization"], 4)}
                               for seg in report["per_segment"]]}
        built.append((out, canonical_bytes(canonical), demand, report, timeline.id, mode))
    return errors, built


def default_jobs():
    return max(1, os.cpu_count() or 1)


def build_all(root, jobs=None):
    """Returns (manifest_dict, artifacts {relpath: bytes}, errors, reports). The timelines compile in `jobs`
    worker processes (9.22); the results are the same in any order."""
    root = pathlib.Path(root)
    timelines_dir = root / "dataset" / "timelines"
    paths = discover(timelines_dir)
    jobs = min(jobs or default_jobs(), max(1, len(paths)))

    artifacts, demand, errors, reports, report_of = {}, {}, [], [], {}
    if jobs == 1:
        results = [compile_one(root, path) for path in paths]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pool:
            results = list(pool.map(compile_one, [root] * len(paths), paths))
    for path_errors, built in results:
        errors.extend(path_errors)
        for out, data, entry, report, timeline_id, mode in built:
            artifacts[out] = data
            demand[out] = entry
            reports.append((timeline_id, mode, report))
            report_of[out] = report
    reports.sort(key=lambda r: (r[0], r[1]))

    manifest = {
        "inputs": {path.relative_to(root).as_posix(): sha256(path.read_bytes()) for path in input_files(root)},
        "artifacts": {rel: sha256(data)
                      for rel, data in sorted(artifacts.items())},
        "demand": {rel: demand[rel] for rel in sorted(demand)},
        "reports": {report_path(rel): sha256(report_bytes(report)) for rel, report in sorted(report_of.items())},
    }
    return manifest, artifacts, errors, reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--jobs", type=int, default=None)
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])

    manifest, artifacts, errors, reports = build_all(root, jobs=args.jobs)
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
