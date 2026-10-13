"""The generated layer's coverage tables (9.21 spec, decision 4) beside the core set's grid.

`wlc.grid` counts the core set's segments per driver-table cell over `dataset/timelines/`. The generated timelines
are not committed, so their tables are derived from the committed manifests alone: the generator records each
file's segment labels — mode, `background_wanted`, tier, `pre_committed_miss` — under the manifest's `grid` section
(`gen.compose.grid_record`), and `build_generated_grid` counts them into the same 32 cells, one table per set, with
the set's file count and segment total. `write` puts the core grid and the generated tables into one artifact,
`dataset/coverage-grid.json`, drift-checked by the gate; the tables need no build and read the same in every CI
step. No empty-cell rule applies to them: each set's enumeration is asserted by the generator's tests, and every C1
task set is the `true` side of its mode, so the generated layer fills the sixteen `true` cells alone.

This module lives beside the generator, not in `wlc`, because the core set's manifest pins `wlc/*.py` by content:
the core set's artifacts and manifest do not move when a generated-layer table changes.
"""

import json
import pathlib

from wlc.grid import MISS_KEY, MODES, TIERS, GridError, build_grid, cell_name, _new_cell


def set_name_of(manifest_path):
    """`dataset/build.<set>.manifest.json` -> `<set>`."""
    name = pathlib.Path(manifest_path).name
    return name[len("build."):-len(".manifest.json")]


def build_generated_grid(manifest_paths):
    """{set: table} over the committed generated manifests: per set, the 32 cells with their tier, segment and
    pre-committed-miss counts read from each file's recorded segment labels, the file count and the segment total.
    A missing manifest, or one without the labels (it predates the record), is a `GridError`."""
    out = {}
    for path in manifest_paths:
        path = pathlib.Path(path)
        set_name = set_name_of(path)
        if not path.is_file():
            raise GridError(f"{path.name}: no manifest — run `make generated` first (the set's manifest is the "
                            "coverage table's input)")
        manifest = json.loads(path.read_text())
        cells = {(m, w): _new_cell(m, w) for m in MODES for w in (True, False)}
        total = 0
        grid = manifest.get("grid") or {}
        for rel in sorted(grid):
            record = grid[rel]
            if "segments" not in record:
                raise GridError(f"{path.name}: {rel} records no segment labels — the manifest predates the "
                                "9.21 record; run `make generated`")
            for index, seg in enumerate(record["segments"]):
                mode = seg["mode"]
                if mode not in MODES:
                    raise GridError(f"{path.name}: {rel} segment {index}: mode {mode!r} is not on the menu")
                cell = cells[(mode, bool(seg["background_wanted"]))]
                cell["tiers"][f"t{int(seg['tier'])}"] += 1
                cell["segments"] += 1
                cell[MISS_KEY] += int(bool(seg.get(MISS_KEY, False)))
                total += 1
        out[set_name] = {"files": len(grid), "segments_total": total, "cells": list(cells.values())}
    return out


def render_generated(generated):
    """The generated tables as text, the instanced cells of each set."""
    lines = []
    for set_name, table in sorted(generated.items()):
        lines.append("")
        lines.append(f"generated {set_name}: {table['files']} files, {table['segments_total']} segments")
        lines.append(f"{'cell':<18}" + "".join(f"{t:>4}" for t in TIERS) + f"{'segs':>6}{'miss':>6}")
        for cell in table["cells"]:
            if cell["segments"]:
                counts = "".join(f"{cell['tiers'][t]:>4}" for t in TIERS)
                lines.append(f"{cell_name(cell['mode'], cell['background_wanted']):<18}{counts}"
                             f"{cell['segments']:>6}{cell[MISS_KEY]:>6}")
    return "\n".join(lines)


def build(timelines_dir, manifest_paths):
    """The whole coverage artifact: the core set's grid plus `generated`, one table per manifest."""
    coverage = build_grid(timelines_dir)
    coverage["generated"] = build_generated_grid(manifest_paths)
    return coverage


def write(timelines_dir, manifest_paths, out_path, check=False):
    """Writes the artifact, or with `check` compares it with the committed one and writes nothing. Error strings."""
    try:
        coverage = build(timelines_dir, manifest_paths)
    except GridError as error:
        return [str(error)]
    content = (json.dumps(coverage, indent=2, sort_keys=True) + "\n").encode()
    out_path = pathlib.Path(out_path)
    if check:
        if not out_path.exists() or out_path.read_bytes() != content:
            return ["coverage-grid.json differs from the timelines and the generated manifests (grid drift)"]
        return []
    out_path.write_bytes(content)
    return []
