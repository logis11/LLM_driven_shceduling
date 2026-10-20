#!/usr/bin/env python3
"""9.6's compile campaign (`meas-ci:build:2026-09-18`): the warm `make -j8` phase every carried build value is read
from (`compiler-child`'s per-member steps, `build-orchestrator`'s dispatch run). The tree and its wakes as
`meas/build/analyze.py` reads them (`build_tree`, the measured CPU's segments, `merge_resumes`); every wake traced by
census_core. Tallied per role (the object job's six members, make, the rest as `other`): the carried values are CPU
sums (a member's CPU per structural step, make's run between forks), so the effect is read from the run the
outside-cause wakes carry.

  python3 -I census_build.py <extracted-release-dir> <out.json>
"""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
from meas.build import analyze as ba  # noqa: E402

PHASE = "build-j8-warm"
ROLES = ("cc1", "as", "gcc", "sh", "fixdep", "rm", "make")
REPEATS = (4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)   # the 14 measured repeats (release notes)


def main():
    root, out_path = sys.argv[1], sys.argv[2]
    result = {"compiler-child + build-orchestrator": {"campaign": "meas-ci:build:2026-09-18", "phase": PHASE,
                                                      "repeats": {}}}
    for d in sorted(glob.glob(os.path.join(root, "**", "meas-build-r*-full"), recursive=True)):
        rep = json.load(open(os.path.join(d, "report.json")))
        k = int(rep.get("repeat"))
        if k not in REPEATS or rep.get("gate") != "open":
            continue
        meas_cpu = int(rep.get("pin.load_cpu", 3))
        base = os.path.join(d, f"perf.{PHASE}")
        segs = ba.load_segments(base + ".timehist.txt.gz")
        wakeups = ba.load_wakeups(base + ".wakeups.txt.gz")
        forks, _exits = ba.load_forks(base + ".forks.txt.gz")
        recs = ba.process_records(ba.load_taskstats(os.path.join(d, f"taskstats.{PHASE}.tsv"))[0])
        _root, tree, tid2pid, role, _pp, _out = ba.build_tree(PHASE, segs, forks, recs, meas_cpu)
        rows = [s for s in segs if s.tid in tree and s.cpu == meas_cpu]
        wakes, _ = ba.merge_resumes(rows, wakeups)
        del segs
        pids = {tid2pid.get(t, t) for t in tree}
        tr = cc.Tracer(cc.load_wakeup_rows(base + ".wakeups.txt.gz"), pids, cc.by_tid(wakes),
                       born={c for _t, _p, _pc, c, _cc in forks})
        span = sum(w.run for w in wakes) / 1000.0
        t = {}
        for w, cls, lab in tr.classify(wakes):
            r = role.get(tid2pid.get(w.tid, w.tid), "?")
            name = r if r in ROLES else "other"
            c = t.setdefault(name, {"n": 0, "run": 0.0, "span": span, "classes": {}, "labels": {}, "gone": []})
            c["n"] += 1
            c["run"] += w.run
            x = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
            x["n"] += 1
            x["run"] += w.run
            if cls != "own":
                c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
            if cls in ("outside", "harness-python"):
                c["gone"].append([round(w.t_in, 6), w.comm, w.tid, round(w.run, 3), cls, lab])
        result["compiler-child + build-orchestrator"]["repeats"][str(k)] = t
        o = sum(c["classes"].get("outside", {}).get("n", 0) for c in t.values())
        print(f"build r{k}: {len(wakes)} wakes, outside {o}", flush=True)
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
