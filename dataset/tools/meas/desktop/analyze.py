#!/usr/bin/env python3
"""Per-phase analysis of a 9.8 desktop run (changelog D13; method §5).

The component layer is imported, not copied. `campaign/analyze.py` computes the components of every other
Chrome measurement in this dataset, and the two renderer entries here are the other half of the archetype it
computed for `web-browser`: that archetype was pooled with `exclude_roles=("renderer",)` (9.5 D14) and these
entries keep the renderers and drop the rest. Computing the two halves with different code would put a montage
inside one application through the analysis rather than through the measurement.

What is NOT reused is `analyze_run`, whose phase loop is fixed to 9.5's names — `idle`, `driven`, `driven-alt`,
`play`, `op` — and would skip every phase this slice records. Phase discovery is local, as
`background/analyze.py`'s is.

  analyze.py <run-dir> [--json out.json] [--phase NAME ...]
"""

import argparse
import json
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import (   # noqa: E402  — the component layer, one definition for both halves
    load_all_wakeups, load_rows, merge_resumes, per_role, per_thread, pid_roles,
)

# the renderer-only view: the inverse of the filter that pools `web-browser`. pid_roles returns exactly these
# six values, so naming the five that go is equivalent to keeping the one that stays, and it stays honest if a
# future Chromium adds a role — an unrecognised role arrives as "other" and is dropped.
KEEP_ROLE = "renderer"
RENDERER_APPS = ("chrome-hidden", "chrome-visible")


def phases_in(D):
    """Every phase with a timehist, in the order the run recorded them (edges.jsonl), else alphabetical."""
    have = set()
    for f in os.listdir(D):
        if f.startswith("perf.") and ".timehist.txt" in f:
            have.add(f.split(".")[1])
    order = []
    p = os.path.join(D, "edges.jsonl")
    if os.path.exists(p):
        for line in open(p):
            if not line.strip():
                continue
            name = json.loads(line).get("phase")
            if name in have and name not in order:
                order.append(name)
    return order + sorted(have - set(order))


def analyze_phase(D, phase, app):
    th = next((f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
               if os.path.exists(os.path.join(D, f"perf.{phase}.timehist.txt{s}"))), None)
    if not th:
        return {"missing": True}
    pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p):
            pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
    segments, (t0, t1), extra = load_rows(os.path.join(D, th), pids)
    span = max(t1 - t0, 1e-6)
    roles = pid_roles(D, phase)

    wk = os.path.join(D, f"perf.{phase}.wakeups.txt.gz")
    if not os.path.exists(wk):
        wk = os.path.join(D, f"perf.{phase}.wakeups.txt")
    wakeups = load_all_wakeups(wk, pids | set(extra)) if os.path.exists(wk) else {}
    segments, merged = merge_resumes(segments, wakeups)

    out = {"span_s": round(span, 3), "rows": len(segments), "resumes_merged": merged,
           "roles": per_role(segments, roles, span),
           "renderer_pids": sorted(p for p, r in roles.items() if r == KEEP_ROLE)}
    if app in RENDERER_APPS:
        kept = [r for r in segments if roles.get(r.pid, "main") == KEEP_ROLE]
        out["role_filter"] = f"kept {KEEP_ROLE} only"
    else:
        kept = segments
        out["role_filter"] = "none"
    out["wakes_per_s"] = round(len(kept) / span, 3)
    out["cpu_share"] = round(sum(r.run for r in kept) / 1000 / span, 5)
    out["threads"] = per_thread(kept, span)
    out["per_pid_wakes_per_s"] = {str(p): round(sum(1 for r in kept if r.pid == p) / span, 3)
                                  for p in sorted({r.pid for r in kept})}
    return out


def analyze_run_dir(D, only=()):
    report = json.load(open(os.path.join(D, "report.json")))
    app = report.get("app")
    res = {"run_dir": D, "app": app, "repeat": report.get("repeat"), "mode": report.get("mode"),
           "gate": report.get("gate"), "renderers_observed": report.get("renderers.observed"),
           "origins": report.get("settings.origins"), "timer_ms": report.get("settings.timer_ms"),
           "phases": {}}
    for phase in phases_in(D):
        if only and phase not in only:
            continue
        res["phases"][phase] = analyze_phase(D, phase, app)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--phase", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    res = analyze_run_dir(a.run_dir, tuple(a.phase))
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    for name, ph in res["phases"].items():
        if ph.get("missing"):
            print(f"{name}: missing")
            continue
        print(f"{name}: span {ph['span_s']}s  wakes/s {ph['wakes_per_s']}  cpu_share {ph['cpu_share']}  "
              f"comms {len(ph['threads'])}  renderers {len(ph['renderer_pids'])}")


if __name__ == "__main__":
    main()
