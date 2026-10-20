#!/usr/bin/env python3
"""9.8's desktop campaign (`meas-ci:desktop:2026-09-20`): `chat-client` (element, idle phase) and `game-client`
(steam, shown phase). Each repeat's carried phase is read as `meas/desktop/analyze.py` reads it (its kept rows, the
heavy event out), every wake traced by census_core.

  python3 -I census_desktop.py <extracted-release-dir> <out.json>
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
from meas.desktop import analyze as da  # noqa: E402
from meas.desktop import pool as dp  # noqa: E402
from meas.campaign.analyze import load_rows, load_all_wakeups, merge_resumes  # noqa: E402
import yaml  # noqa: E402

ENTRY = {"element": "chat-client", "steam": "game-client"}
ARCH = os.path.join(os.path.dirname(cc.TOOLS), "archetypes.yaml")


def carried_comms(entry):
    a = yaml.safe_load(open(ARCH))["archetypes"][entry]
    return [c["comm"] for c in a["params"]["components"] if c["comm"] != "residual"]


def tally(classified, comps, span):
    out = {}
    for r, cls, lab in classified:
        name = r.comm if r.comm in comps else "residual"
        c = out.setdefault(name, {"n": 0, "run": 0.0, "span": span, "classes": {}, "labels": {}, "gone": []})
        c["n"] += 1
        c["run"] += r.run
        k = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
        k["n"] += 1
        k["run"] += r.run
        if cls not in ("own",):
            c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
        if cls in ("outside", "harness-python"):
            c["gone"].append([round(r.t_in, 6), r.tid, round(r.run, 3), cls, lab])
    return out


def main():
    root, out_path = sys.argv[1], sys.argv[2]
    runs, _gated, _other, _probes = dp.find_runs(root, "")
    result = {}
    for app, entry in ENTRY.items():
        phase = dp.CARRIED[app][0]
        comps = carried_comms(entry)
        for k in sorted(runs.get(app, {}), key=dp.repeat_order):
            D = runs[app][k]["dir"]
            ph = da.analyze_phase(D, phase, app, keep_rows=True)
            kept, span = ph["_rows"], ph["span_s"]
            # every merged wake of the tree, as analyze_phase computed them before keeping
            pids = set()
            for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
                p = os.path.join(D, snap)
                if os.path.exists(p):
                    pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
            segs, _w, extra = load_rows(os.path.join(D, f"perf.{phase}.timehist.txt.gz"), pids)
            wk = os.path.join(D, f"perf.{phase}.wakeups.txt.gz")
            merged, _ = merge_resumes(segs, load_all_wakeups(wk, pids | set(extra)))
            peers = {}
            sp = cc.read_pid(os.path.join(D, "synapse.pid"))
            if sp:
                peers[sp] = "Synapse, the Matrix homeserver (the scripted peer)"
            tr = cc.Tracer(cc.load_wakeup_rows(wk), pids | set(extra), cc.by_tid(merged), peers)
            res = tally(tr.classify(kept), comps, span)
            result.setdefault(entry, {"campaign": "meas-ci:desktop:2026-09-20", "phase": phase, "app": app,
                                      "repeats": {}})["repeats"][str(k)] = res
            o = sum(c["classes"].get("outside", {}).get("n", 0) for c in res.values())
            print(f"{entry} r{k}: {sum(c['n'] for c in res.values())} wakes, outside {o}", flush=True)
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
