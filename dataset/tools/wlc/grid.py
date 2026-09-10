"""Coverage-grid generator (task-2.4 spec §2; Phase 7 spec, decisions 1, 11).

Counts segments per driver-table cell — mode × background_wanted, the 32
rows of the driver table — across the five familiarity-tier columns, over
all core timelines. A segment's tier comes from its `familiarity:`
annotation when present; otherwise it defaults to the highest (most opaque)
tier among the names of the tasks alive in it. Segments whose mode is not
on the recognizer's menu (`ambiguous`) are reported outside the grid.
A segment annotated `pre_committed_miss: true` (recognition-vocabulary §1)
counts in its cell like any other and is marked, so the table shows which
cells are instanced but recognition-limited.

An empty cell is a coverage error (`coverage_errors`). The generated
artifact is committed and re-derived in CI — the paper's dataset-design
table cannot drift from the files. The empty-cell check is reported by
`derive.py` on every run and made fatal by its `--require-coverage` flag,
which the Makefile's `check` target adopts once the coreset is meant to
satisfy it (Phase 7, 7.3).
"""

import json
import pathlib

import yaml

from .units import parse_us

# The recognizer's closed menu, in recognition-vocabulary §1 order.
MODES = ("browsing", "office", "mail", "dev", "photo", "meeting", "gaming",
         "media", "video-edit", "compile", "ml-train", "render", "transcode",
         "indexing", "backup", "idle")
TIERS = ("t1", "t2", "t3", "t4", "t5")
MISS_KEY = "pre_committed_miss"

# Default name→tier lookup (C5 ladder, building-plan §3). Tiers 4–5 exist
# only via explicit annotation or invented names listed here by authoring.
NAME_TIERS = {
    1: {"firefox", "blender", "chrome", "code", "make", "steam", "discord",
        "thunderbird", "spotify", "gimp", "kdenlive", "ffmpeg", "mpv",
        "python3", "rsync", "tar", "xz", "7z", "borg", "rclone", "zoom",
        "slack", "vlc", "game.exe", "transmission-daemon", "clamscan",
        "evince", "darktable", "ollama"},
    2: {"soffice.bin", "gamescope", "wineserver", "steamwebhelper",
        "HandBrakeCLI", "freshclam", "gnome-shell", "Xorg", "pipewire",
        "systemd", "dbus-daemon"},
    3: {"tracker-miner-fs-3", "cc1", "baloo_file", "updatedb", "ld", "cc1plus"},
}
_TIER_BY_NAME = {name: tier for tier, names in NAME_TIERS.items()
                 for name in names}


class GridError(Exception):
    """A segment the grid cannot place: a menu mode without the attribute,
    or a mode neither on the menu nor `ambiguous`."""


def cell_name(mode, wanted):
    return f"{mode}/{str(wanted).lower()}"


def segment_tier(segment, tasks):
    if "familiarity" in segment:
        return segment["familiarity"]
    t_start, t_end = parse_us(segment["from"]), parse_us(segment["to"])
    tiers = []
    for task in tasks:
        arrive = parse_us(task["arrive"])
        depart = parse_us(task["depart"]) if "depart" in task else None
        if arrive < t_end and (depart is None or depart > t_start):
            tiers.append(_TIER_BY_NAME.get(task["name"], 5))
            # an orchestrator's spawned children are recognizer-visible
            # processes too (e.g. make's cc1) — count their bound name
            child = (task.get("bind") or {}).get("child_name")
            if child:
                tiers.append(_TIER_BY_NAME.get(child, 5))
    return max(tiers, default=1)


def _new_cell(mode, wanted):
    return {"mode": mode, "background_wanted": wanted,
            "tiers": {t: 0 for t in TIERS}, "segments": 0, MISS_KEY: 0}


def build_grid(timelines_dir):
    cells = {(m, w): _new_cell(m, w) for m in MODES for w in (True, False)}
    outside, files, total = [], {}, 0
    for path in sorted(pathlib.Path(timelines_dir).glob(
            "**/*.timeline.yaml")):
        data = yaml.safe_load(path.read_text())
        wid = data["meta"]["id"]
        rows = []
        for index, segment in enumerate(data["segments"]):
            total += 1
            mode = segment["mode"]
            attributes = segment.get("attributes") or {}
            tier = segment_tier(segment, data["tasks"])
            row = {"mode": mode, "tier": tier,
                   "scenario": segment.get("scenario", [])}
            if mode == "ambiguous":
                outside.append({"file": wid, "segment": index, "mode": mode,
                                "tier": tier})
            elif mode not in MODES:
                raise GridError(f"{wid} segment {index}: mode {mode!r} is "
                                "neither on the menu nor 'ambiguous'")
            else:
                if "background_wanted" not in attributes:
                    raise GridError(f"{wid} segment {index}: a menu-mode "
                                    "segment needs background_wanted")
                wanted = bool(attributes["background_wanted"])
                miss = bool(attributes.get(MISS_KEY, False))
                cell = cells[(mode, wanted)]
                cell["tiers"][f"t{tier}"] += 1
                cell["segments"] += 1
                cell[MISS_KEY] += miss
                row["background_wanted"] = wanted
                if miss:
                    row[MISS_KEY] = True
            rows.append(row)
        files[wid] = rows
    cell_list = list(cells.values())
    empty = sorted(cell_name(c["mode"], c["background_wanted"])
                   for c in cell_list if c["segments"] == 0)
    return {"segments_total": total, "cells": cell_list,
            "empty_cells": empty, "outside": outside, "per_file": files}


def coverage_errors(coverage):
    """The all-cells requirement (Phase 7 spec, decision 11): one error
    naming every empty cell, or none."""
    empty = coverage["empty_cells"]
    if not empty:
        return []
    return [f"coverage: {len(empty)} empty driver-table cell(s) — "
            + ", ".join(empty)]


def render(coverage):
    lines = [f"{'cell':<18}" + "".join(f"{t:>4}" for t in TIERS)
             + f"{'segs':>6}{'miss':>6}"]
    for cell in coverage["cells"]:
        name = cell_name(cell["mode"], cell["background_wanted"])
        if cell["segments"]:
            counts = "".join(f"{cell['tiers'][t]:>4}" for t in TIERS)
            lines.append(f"{name:<18}{counts}{cell['segments']:>6}"
                         f"{cell[MISS_KEY]:>6}")
        else:
            lines.append(f"{name:<18}" + f"{'-':>4}" * len(TIERS)
                         + f"{0:>6}{0:>6}   (empty)")
    for entry in coverage["outside"]:
        lines.append(f"outside the grid: {entry['mode']} ×1 "
                     f"({entry['file']}, tier {entry['tier']})")
    on_grid = sum(c["segments"] for c in coverage["cells"])
    lines.append(f"total segments: {coverage['segments_total']} "
                 f"({on_grid} on the grid, {len(coverage['outside'])} outside)")
    empty = coverage["empty_cells"]
    lines.append(f"empty cells: {len(empty)}"
                 + (" — " + ", ".join(empty) if empty else ""))
    return "\n".join(lines)


def write(timelines_dir, out_path, check=False):
    try:
        coverage = build_grid(timelines_dir)
    except GridError as error:
        return [str(error)]
    content = (json.dumps(coverage, indent=2, sort_keys=True) + "\n").encode()
    out_path = pathlib.Path(out_path)
    if check:
        if not out_path.exists() or out_path.read_bytes() != content:
            return ["coverage-grid.json differs from the timelines "
                    "(grid drift)"]
        return []
    out_path.write_bytes(content)
    return []
