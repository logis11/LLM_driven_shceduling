"""Coverage-grid generator (task-2.4 spec §2).

Counts segments on the mode × familiarity grid across all core timelines.
A segment's tier comes from its `familiarity:` annotation when present;
otherwise it defaults to the highest (most opaque) tier among the names of
the tasks alive in it. The generated artifact is committed and re-derived
in CI — the paper's dataset-design table cannot drift from the files.
"""

import json
import pathlib

import yaml

from .units import parse_us

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


def build_grid(timelines_dir):
    grid, files = {}, {}
    for path in sorted(pathlib.Path(timelines_dir).glob(
            "**/*.timeline.yaml")):
        data = yaml.safe_load(path.read_text())
        rows = []
        for segment in data["segments"]:
            tier = segment_tier(segment, data["tasks"])
            key = f"{segment['mode']}|t{tier}"
            grid[key] = grid.get(key, 0) + 1
            rows.append({"mode": segment["mode"], "tier": tier,
                         "scenario": segment.get("scenario", [])})
        files[data["meta"]["id"]] = rows
    modes = sorted({k.split("|")[0] for k in grid})
    table = {mode: {f"t{t}": grid.get(f"{mode}|t{t}", 0) for t in range(1, 6)}
             for mode in modes}
    return {"segments_total": sum(grid.values()), "grid": table,
            "per_file": files}


def render(coverage):
    lines = ["mode            t1  t2  t3  t4  t5"]
    for mode, tiers in coverage["grid"].items():
        lines.append(f"{mode:<14}" + "".join(
            f"{tiers[f't{t}']:>4}" for t in range(1, 6)))
    lines.append(f"total segments: {coverage['segments_total']}")
    return "\n".join(lines)


def write(timelines_dir, out_path, check=False):
    coverage = build_grid(timelines_dir)
    content = (json.dumps(coverage, indent=2, sort_keys=True) + "\n").encode()
    out_path = pathlib.Path(out_path)
    if check:
        if not out_path.exists() or out_path.read_bytes() != content:
            return ["coverage-grid.json differs from the timelines "
                    "(grid drift)"]
        return []
    out_path.write_bytes(content)
    return []
