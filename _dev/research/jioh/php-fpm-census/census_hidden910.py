#!/usr/bin/env python3
"""9.10's hidden-renderer campaign (`meas-ci:desktop:2026-10-05b`): `renderer-hidden`'s steady phase, each repeat read
as `meas/desktop/analyze.py` reads it (the page renderers by `renderers.tsv`, part-phase renderers and the control tab
dropped, every measured renderer a sample of ONE renderer), every wake traced by chain_roots (census_core's rules) —
as census_desktop.py reads 9.8's phases.

  python3 -I census_hidden910.py <release x dir> <out.json>

The components are one renderer's: a component's count is over the renderers measured and its span is the phase's
times the renderers measured, so effect.py's rate (n / span) is the per-renderer rate the pool carries and its gap
mean (Σspan / Σn) the gap mean of the renderers laid end to end and wrapped round. The residual is every comm the
pool did not select (`ThreadPoolServi`, `MemoryInfra`).
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
import tally910 as t9  # noqa: E402
from meas.desktop import analyze as da  # noqa: E402
from meas.campaign.analyze import load_rows, load_all_wakeups, merge_resumes  # noqa: E402
import yaml  # noqa: E402

ARCH = os.path.join(os.path.dirname(cc.TOOLS), "archetypes.yaml")
APP, ENTRY, PHASE, TAG = "chrome-hidden", "renderer-hidden", "steady", "meas-ci:desktop:2026-10-05b"
DIR = re.compile(r"^meas-desktop-chrome-hidden-r(\d+)-full-(\d+)$")


def main():
    root, out_path = sys.argv[1], sys.argv[2]
    comps = [c["comm"] for c in yaml.safe_load(open(ARCH))["archetypes"][ENTRY]["params"]["components"]
             if c["comm"] != "residual"]
    sec = {"campaign": TAG, "phase": PHASE, "app": APP, "repeats": {}, "runs": {}, "check": {}, "renderers": {}}
    dirs = sorted(((int(DIR.match(os.path.basename(d)).group(1)), d) for d in glob.glob(os.path.join(root, "*"))
                   if DIR.match(os.path.basename(d))))
    for k, D in dirs:
        ph = da.analyze_phase(D, PHASE, APP, keep_rows=True)
        kept, n_rend = ph["_rows"], ph["renderers_measured"]
        span = ph["span_s"]
        pids = set()
        for snap in (f"snap.{PHASE}.before.json", f"snap.{PHASE}.after.json"):
            p = os.path.join(D, snap)
            if os.path.exists(p):
                pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
        segs, _w, extra = load_rows(os.path.join(D, f"perf.{PHASE}.timehist.txt.gz"), pids)
        wk = os.path.join(D, f"perf.{PHASE}.wakeups.txt.gz")
        merged, _ = merge_resumes(segs, load_all_wakeups(wk, pids | set(extra)))
        tr = t9.PeerTracer(cc.load_wakeup_rows(wk), pids | set(extra), cc.by_tid(merged), servers=t9.servers_of(D))
        traced = tr.trace(kept)
        sec["repeats"][str(k)] = t9.tally(traced, lambda r: r.comm if r.comm in comps else "residual",
                                          lambda _n: span * n_rend)
        sec["runs"][str(k)] = cr.runs(traced, 5)
        sec["renderers"][str(k)] = {"measured": n_rend, "span_s": span, "control_tab": ph.get("control_tab")}
        if not sec["check"]:
            sec["check"][str(k)] = cr.check(tr, kept)
        o = sum(c["classes"].get("outside", {}).get("n", 0) for c in sec["repeats"][str(k)].values())
        print(f"{ENTRY} r{k}: {len(kept)} wakes over {n_rend} renderers, outside {o}", flush=True)
    json.dump({ENTRY: sec}, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
