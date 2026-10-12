#!/usr/bin/env python3
"""Generate the generated layer and compile it, one manifest per set (9.19 spec).

Usage: generate.py [--check] [--sets NAME,…] [--jobs N] [--repo ROOT]
  --check   regenerate and recompile in memory and fail if any set's committed
            manifest would change (an independent verification; the gate
            compares the manifest the build wrote with the committed one —
            check_build.py; 9.22)
  --jobs N  worker processes, one cell each (default: the CPU count)
  --sets    the named sets only (their manifests alone are written)

The cells come from `dataset/grids.yaml` over the sixteen C1 timelines (`gen.cells`); each becomes a timeline under
`dataset/generated/<set>/` (not committed; `gen.compose`), compiled like any other timeline — the schema, the lints,
the compile report beside the artifact — into `dataset/build/<set>-<mode>/`. The set's manifest,
`dataset/build.<set>.manifest.json`, pins the compile's inputs plus the definition, the generator and the C1
timelines by content, every artifact and report by hash, the demand per file, and under `grid` each file's
coordinates and split (decisions 4–6). The compile mirrors `compile.compile_one` over a different root so the core
compiler and the core set's manifest stay as they are (spec invariant).
"""

import argparse
import concurrent.futures
import json
import os
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import compile as compile_tool  # noqa: E402
from gen import c1_sets, cells, lint_grids, load_definition, modes_of  # noqa: E402
from gen.compose import timeline_bytes  # noqa: E402
from wlc import Timeline, TimelineError, compile_timeline  # noqa: E402
from wlc.compiler import MODES, canonical_bytes  # noqa: E402
from wlc.linter import lint_bound_sources, lint_canonical  # noqa: E402

sha256 = compile_tool.sha256


def generated_dir(root):
    return pathlib.Path(root) / "dataset" / "generated"


def manifest_path(root, set_name):
    return pathlib.Path(root) / "dataset" / f"build.{set_name}.manifest.json"


def generator_inputs(root):
    """The files the generation reads besides the compile's inputs: the definition, the generator, the C1 timelines."""
    dataset = pathlib.Path(root) / "dataset"
    files = [dataset / "grids.yaml", dataset / "tools" / "generate.py"]
    files += sorted((dataset / "tools" / "gen").glob("*.py"))
    files += sorted((dataset / "timelines" / "coreset").glob("c1-*.timeline.yaml"))
    return files


def write_timelines(root, defn, by_set):
    """Writes every cell's timeline under generated/<set>/, removes stale ones; returns {set: [(cell, path)]}."""
    sets = c1_sets(pathlib.Path(root) / "dataset" / "timelines" / "coreset")
    out = {}
    for set_name, set_cells in by_set.items():
        directory = generated_dir(root) / set_name
        directory.mkdir(parents=True, exist_ok=True)
        wanted = set()
        out[set_name] = []
        for cell in set_cells:
            path = directory / f"{cell['id']}.timeline.yaml"
            data = timeline_bytes(cell, sets, defn)
            if not path.is_file() or path.read_bytes() != data:
                path.write_bytes(data)
            wanted.add(path.name)
            out[set_name].append((cell, path))
        for stale in directory.glob("*.timeline.yaml"):
            if stale.name not in wanted:
                stale.unlink()
    return out


def compile_generated_one(root, set_name, path):
    """One generated timeline in every mode — `compile.compile_one` over the generated root."""
    root, path = pathlib.Path(root), pathlib.Path(path)
    library, schema = compile_tool._tools(root)
    rel_path = path.relative_to(root).as_posix()
    try:
        timeline = Timeline(path, library)
    except TimelineError as err:
        return [str(err)], []
    errors, built = [], []
    for mode in MODES:
        canonical, report = compile_timeline(timeline, library, mode, rel_path=rel_path)
        errors.extend(lint_canonical(canonical, schema, report=report, mode=mode, name=f"{timeline.id}[{mode}]"))
        out = f"{set_name}-{mode}/{timeline.id}.workload.json"
        demand = {"utilization": round(report["utilization"], 4),
                  "demand_class": report["demand_class"],
                  "segments": [{"index": seg["index"], "t_start_us": seg["t_start_us"],
                                "t_end_us": seg["t_end_us"], "utilization": round(seg["utilization"], 4)}
                               for seg in report["per_segment"]]}
        built.append((out, canonical_bytes(canonical), demand, report, timeline.id, mode))
    return errors, built


def _job(args):
    return compile_generated_one(*args)


def build_set(root, set_name, placed, jobs=None):
    """Returns (manifest, artifacts {relpath: bytes}, errors, reports) for one set."""
    root = pathlib.Path(root)
    jobs = min(jobs or compile_tool.default_jobs(), max(1, len(placed)))
    args = [(root, set_name, path) for _, path in placed]
    if jobs == 1:
        results = [_job(a) for a in args]
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pool:
            results = list(pool.map(_job, args, chunksize=8))
    artifacts, demand, errors, reports, report_of, grid = {}, {}, [], [], {}, {}
    for (cell, _), (cell_errors, built) in zip(placed, results):
        errors.extend(cell_errors)
        for out, data, entry, report, timeline_id, mode in built:
            artifacts[out] = data
            demand[out] = entry
            reports.append((timeline_id, mode, report))
            report_of[out] = report
            coords = dict(cell["grid"])
            if "split" in cell:
                coords["split"] = cell["split"]
            grid[out] = coords
    reports.sort(key=lambda r: (r[0], r[1]))
    inputs = compile_tool.input_files(root) + generator_inputs(root)
    manifest = {
        "inputs": {p.relative_to(root).as_posix(): sha256(p.read_bytes()) for p in sorted(set(inputs))},
        "artifacts": {rel: sha256(data) for rel, data in sorted(artifacts.items())},
        "demand": {rel: demand[rel] for rel in sorted(demand)},
        "reports": {compile_tool.report_path(rel): sha256(compile_tool.report_bytes(report))
                    for rel, report in sorted(report_of.items())},
        "grid": {rel: grid[rel] for rel in sorted(grid)},
    }
    return manifest, artifacts, errors, reports


def manifest_bytes(manifest):
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--jobs", type=int, default=None)
    parser.add_argument("--sets", default=None)
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])
    dataset = root / "dataset"

    registry = yaml.safe_load((dataset / "sources.yaml").read_text())["sources"]
    errors = lint_grids(dataset / "grids.yaml", registry)
    if errors:
        print(f"{len(errors)} grid definition error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    defn = load_definition(dataset / "grids.yaml")
    timelines = dataset / "timelines" / "coreset"
    by_set = cells(defn, modes_of(timelines), c1_sets(timelines))
    if args.sets:
        only = args.sets.split(",")
        unknown = sorted(set(only) - set(by_set))
        if unknown:
            print(f"unknown sets {unknown}; the definition names {sorted(by_set)}", file=sys.stderr)
            return 1
        by_set = {name: by_set[name] for name in only}
    placed = write_timelines(root, defn, by_set)

    status = 0
    for set_name, set_placed in placed.items():
        errors = []
        for _, path in set_placed:
            errors.extend(lint_bound_sources(path, registry))
        manifest, artifacts, build_errors, reports = build_set(root, set_name, set_placed, jobs=args.jobs)
        errors.extend(build_errors)
        if errors:
            print(f"{set_name}: {len(errors)} error(s):", file=sys.stderr)
            for message in errors[:50]:
                print(f"  - {message}", file=sys.stderr)
            status = 1
            continue
        data = manifest_bytes(manifest)
        target = manifest_path(root, set_name)
        if args.check:
            if not target.is_file():
                print(f"{target.name}: no committed manifest to check against", file=sys.stderr)
                status = 1
            elif target.read_bytes() != data:
                print(f"{target.name} drift: the regenerated set does not match the committed manifest",
                      file=sys.stderr)
                status = 1
            else:
                print(f"{set_name}: manifest verified ({len(artifacts)} artifacts)")
            continue
        build_dir = dataset / "build"
        for rel, bytes_ in artifacts.items():
            out = build_dir / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(bytes_)
        for timeline_id, mode, report in reports:
            rel = f"{set_name}-{mode}/{timeline_id}.workload.json"
            (build_dir / compile_tool.report_path(rel)).write_bytes(compile_tool.report_bytes(report))
        target.write_bytes(data)
        print(f"{set_name}: wrote {len(artifacts)} artifacts + reports + manifest")
    return status


if __name__ == "__main__":
    sys.exit(main())
