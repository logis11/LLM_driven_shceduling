#!/usr/bin/env python3
"""9.10's Kdenlive idle campaign (`meas-ci:interactive:2026-10-05`): `video-editor`'s idle components, each pooled
repeat read as `meas/campaign/pool.py` reads it (`analyze_run` at the pool's settings, the idle phase after the 240 s
settle, the components keyed by role and comm), every wake traced by chain_roots (census_core's rules) — as
census_campaign.py reads 9.5's idle phases.

  python3 -I census_idle910.py <pool-kdenlive.json> <release x dir> <out.json>

The repeat folders are `meas-interactive-kdenlive-r<k>-idle-<run id>`, the run id the pooled record's.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
import tally910 as t9  # noqa: E402
sys.path.insert(0, os.path.join(cc.TOOLS, "meas", "campaign"))
from analyze import analyze_run, component_name, HARNESS_COMMS  # noqa: E402
import pool as cp  # noqa: E402
import yaml  # noqa: E402

ARCH = os.path.join(os.path.dirname(cc.TOOLS), "archetypes.yaml")
APP, ENTRY, PHASE, TAG = "kdenlive", "video-editor", "idle", "meas-ci:interactive:2026-10-05"


def main():
    pool_json, root, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    pj = json.load(open(pool_json))
    run = pj["runs"][APP]
    comps = [c["comm"] for c in yaml.safe_load(open(ARCH))["archetypes"][ENTRY]["params"]["components"]
             if c["comm"] != "residual"]
    result = {ENTRY: {"campaign": TAG, "phase": PHASE, "field": "components", "app": APP, "repeats": {},
                      "runs": {}, "check": {}}}
    sec = result[ENTRY]
    for k in run["repeats"]:
        D = os.path.join(root, f"meas-interactive-{APP}-r{k}-idle-{run['run_id'][str(k)]}")
        res, raw = analyze_run(D, pj["w_ms"], pj["cap_ms"], idle_from_s=cp.IDLE_FROM_S.get(APP, 0.0))
        pd, ph = raw["phases"][PHASE], res["phases"][PHASE]
        snap_pids = set()
        for snap in (f"snap.{PHASE}.before.json", f"snap.{PHASE}.after.json"):
            p = os.path.join(D, snap)
            if os.path.exists(p):
                snap_pids |= {pr["pid"] for pr in json.load(open(p))["procs"]
                              if pr.get("comm") not in HARNESS_COMMS and not pr.get("comm", "").startswith("llvmpipe-")}
        tree = snap_pids | {int(p) for p in ph.get("transient_pids", {})} | {r.pid for r in pd["segments"]}
        tr = t9.PeerTracer(cc.load_wakeup_rows(os.path.join(D, f"perf.{PHASE}.wakeups.txt.gz")), tree,
                           cc.by_tid(pd["rows"]), servers=t9.servers_of(D))
        rows, events = cp.split_events(APP, PHASE, pd["rows"])
        roles = pd.get("roles") or {}

        def name_of(r):
            n = component_name(roles.get(r.pid, "main"), cp.component_key(APP, r.comm))
            return n if n in comps else "residual"
        traced = tr.trace(rows)
        sec["repeats"][str(k)] = t9.tally(traced, name_of, lambda _n: pd["span"])
        sec["runs"][str(k)] = cr.runs(traced, 5)
        if k == run["repeats"][0]:
            sec["check"][str(k)] = cr.check(tr, rows)
        o = sum(c["classes"].get("outside", {}).get("n", 0) for c in sec["repeats"][str(k)].values())
        print(f"{ENTRY} {PHASE} r{k}: {len(rows)} wakes, outside {o}, events {events is not None}", flush=True)
        del raw
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
