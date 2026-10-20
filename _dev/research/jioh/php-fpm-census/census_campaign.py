#!/usr/bin/env python3
"""9.5's interactive and playback campaigns: each pooled repeat read as `meas/campaign/pool.py` reads it
(`analyze_run` at the pool's settings, the operation's windows, the heavy events split off, the components keyed by
role and comm), every wake traced by census_core.

  python3 -I census_campaign.py <app> <campaign tag> <pool json> <out.json> <extracted dir> [<extracted dir> ...]

Sections per app (`SECTIONS`): the phase each carried table is read from and the archetype field that carries it.
`components`, `focus_components` and an operation's `components` are tallied per carried component (the rest as
`residual`); `cycle` (the playback entries' period and cycle_run) and `input_run` (the per-input windows) are tallied
over the whole tree, their effect read from the run the outside-cause wakes add.
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
sys.path.insert(0, os.path.join(cc.TOOLS, "meas", "campaign"))
from analyze import analyze_run, component_name, HARNESS_COMMS  # noqa: E402
import pool as cp  # noqa: E402
import yaml  # noqa: E402

ARCH = os.path.join(os.path.dirname(cc.TOOLS), "archetypes.yaml")
SECTIONS = {
    "soffice": ("office-writer", {"idle": "components", "driven": "input_run"}),
    "code": ("code-editor", {"idle": "components", "driven": "input_run"}),
    "thunderbird-send@meas-ci:interactive:2026-09-19": ("mail-client", {"idle": "components"}),
    "thunderbird-send@meas-ci:interactive:2026-09-27": ("mail-client", {"op": "operations.send.components",
                                                                       "driven": "input_run"}),
    "chrome": ("web-browser", {"idle": "components", "op": "operations.page-load.components", "driven": "input_run"}),
    "gimp": ("image-editor", {"driven": "focus_components", "op": "operations.unsharp-mask.components"}),
    "kdenlive": ("video-editor", {"driven": "focus_components", "op": "operations.preview-render.components"}),
    "mpv-video": ("video-player", {"play": "cycle"}),
    "mpv-audio": ("audio-player", {"play": "cycle"}),
    "webrtc": ("video-call", {"play": "cycle"}),
}
NAME = re.compile(r"^meas-(interactive|playback)-(.+)-r(\d+)-(full|dry|idle)$")


def carried(entry, field):
    if field in ("cycle", "input_run"):
        return None
    node = yaml.safe_load(open(ARCH))["archetypes"][entry]["params"]
    for part in field.split("."):
        node = node[part]
    return [c["comm"] for c in node if c["comm"] != "residual"]


def tally(classified, name_of, span):
    out = {}
    for r, cls, lab in classified:
        name = name_of(r)
        c = out.setdefault(name, {"n": 0, "run": 0.0, "span": span, "classes": {}, "labels": {}, "gone": []})
        c["n"] += 1
        c["run"] += r.run
        k = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
        k["n"] += 1
        k["run"] += r.run
        if cls != "own":
            c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
        if cls in ("outside", "harness-python"):
            c["gone"].append([round(r.t_in, 6), r.comm, r.tid, round(r.run, 3), cls, lab])
    return out


def main():
    key, tag, pool_json, out_path, roots = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
    app = key.split("@")[0]
    entry, sections = SECTIONS.get(f"{app}@{tag}") or SECTIONS[app]
    reps = json.load(open(pool_json))["runs"][app]["repeats"]
    dirs = {}
    for root in roots:
        for d in sorted(glob.glob(os.path.join(root, "**", "meas-*"), recursive=True)):
            m = NAME.match(os.path.basename(d))
            if not m or m.group(2) != app or "-excluded" in d or not os.path.exists(os.path.join(d, "report.json")):
                continue
            k = int(m.group(3))
            if k in dirs:
                raise SystemExit(f"{app} r{k}: two folders {dirs[k]} {d}")
            dirs[k] = d
    missing = [k for k in reps if k not in dirs]
    if missing:
        print(f"{app}: pooled repeats without a folder here: {missing}", flush=True)
    result = {}
    for k in reps:
        if k not in dirs:
            continue
        D = dirs[k]
        res, raw = analyze_run(D, 5.0, 0.0, idle_from_s=cp.IDLE_FROM_S.get(app, 0.0))
        for phase, field in sections.items():
            pd = raw["phases"].get(phase)
            if pd is None:
                continue
            ph = res["phases"][phase]
            snap_pids = set()
            for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
                p = os.path.join(D, snap)
                if os.path.exists(p):
                    snap_pids |= {pr["pid"] for pr in json.load(open(p))["procs"]
                                  if pr.get("comm") not in HARNESS_COMMS and not pr.get("comm", "").startswith("llvmpipe-")}
            tree = snap_pids | {int(p) for p in ph.get("transient_pids", {})} | {r.pid for r in pd["segments"]}
            wk = os.path.join(D, f"perf.{phase}.wakeups.txt.gz")
            tr = cc.Tracer(cc.load_wakeup_rows(wk), tree, cc.by_tid(pd["rows"]),
                           drivers=("python3", "xdotool") if phase in ("op", "driven") else ())
            roles = pd.get("roles") or {}
            op = pd.get("operation")
            comps = carried(entry, field)
            if field in ("cycle", "input_run"):
                rows, span = pd["rows"], pd["span"]
                name_of = lambda r: "tree"
            else:
                rows = op["inside"] if op else pd["rows"]
                span = (sum(op["durations_ms"]) / 1000 or 1e-6) if op else pd["span"]
                rows, events = cp.split_events(app, phase, rows)
                heavy = [r for r in (op["inside"] if op else pd["rows"]) if r not in set(rows)] if events else []

                def name_of(r, comps=comps):
                    n = component_name(roles.get(r.pid, "main"), cp.component_key(app, r.comm))
                    return n if n in comps else "residual"
            t = tally(tr.classify(rows), name_of, span)
            if field not in ("cycle", "input_run") and events:
                t.update({f"event {k2}": v for k2, v in tally(tr.classify(heavy), lambda r: r.comm, span).items()})
            if field in ("cycle", "input_run"):
                t["tree"]["segments_run"] = sum(s.run for s in pd["segments"])
            sec = result.setdefault(f"{entry} {phase}", {"campaign": tag, "phase": phase, "field": field, "app": app,
                                                         "repeats": {}})
            sec["repeats"][str(k)] = t
            o = sum(c["classes"].get("outside", {}).get("n", 0) for c in t.values())
            print(f"{entry} {phase} r{k}: {sum(c['n'] for c in t.values())} wakes, outside {o}", flush=True)
        del raw
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
