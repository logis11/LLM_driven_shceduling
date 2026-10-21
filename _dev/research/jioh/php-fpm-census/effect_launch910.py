#!/usr/bin/env python3
"""How far each launch phase's stream would move without its outside-cause wakes (census_launch910.py's output).

  python3 -I effect_launch910.py <launch.json> > effect-launch.json

A launch phase is carried as each pooled repeat's stream, as observed (9.10 D136: each repeat's wakes replayed, no
distribution, no stability rule), so the shift is read per repeat — its wakes and its CPU without the outside-cause
wakes, against them — and over the repeats' means, against the ±5 % tolerance and against the spread of the
per-repeat values (their 95 % half-width by meas/stability.stability: a reading of the repeats, not a carried
half-width). Three removals: every outside-cause wake (the rule as written, `out`); only those whose own wakeup row
names the outside waker (`direct`, the inherited put back); and the context reading's (`ctx`: the phase wakes traced
with the tree's wakes before the exec as their predecessors). Also the first 10 s slice's CPU, where a launch's work
falls. `renderer-hidden`'s twelve streams are summed per repeat, with the largest single stream's shift beside it.
"""

import json
import statistics
import sys

sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
from meas.stability import stability  # noqa: E402


def main():
    d = json.load(open(sys.argv[1]))
    rows = []
    for sec, e in d.items():
        reps = sorted(e["repeats"], key=int)
        per = {}
        stream_max = {"out_wakes": 0.0, "out_cpu": 0.0}
        for k in reps:
            res = e["repeats"][k]
            n = sum(c["n"] for c in res.values())
            run = sum(c["run"] for c in res.values())
            o = sum(c["classes"].get("outside", {}).get("n", 0) for c in res.values())
            orun = sum(c["classes"].get("outside", {}).get("run", 0.0) for c in res.values())
            dn = sum(c["split"]["direct"]["n"] for c in res.values())
            drun = sum(c["split"]["direct"]["run"] for c in res.values())
            cx = e["context"][k]["classes"].get("outside", {"n": 0, "run": 0.0})
            per[k] = {"n": n, "cpu": run, "out": o, "out_run": orun, "direct": dn, "direct_run": drun,
                      "ctx": cx["n"], "ctx_run": cx["run"], "first10": e["first10"][k]}
            for c in res.values():
                if c["n"]:
                    stream_max["out_wakes"] = max(stream_max["out_wakes"], c["classes"].get("outside", {}).get("n", 0) / c["n"])
                if c["run"]:
                    stream_max["out_cpu"] = max(stream_max["out_cpu"], c["classes"].get("outside", {}).get("run", 0.0) / c["run"])
        line = {"entry": sec.split(" ", 1)[1], "campaign": e["campaign"], "k": len(reps),
                "wakes": sum(p["n"] for p in per.values()), "outside": sum(p["out"] for p in per.values()),
                "direct": sum(p["direct"] for p in per.values()), "ctx": sum(p["ctx"] for p in per.values()),
                "per_repeat_outside": [per[k]["out"] for k in reps],
                "streams": len(next(iter(e["repeats"].values()))), "stream_max": stream_max}
        for v, base in (("wakes", "n"), ("cpu", "cpu")):
            vals = {k: per[k][base] for k in reps}
            line[f"{v}_mean"] = statistics.fmean(vals.values())
            line[f"{v}_spread"] = stability(vals, keep_zero=True)["half_width"]
            for tag, key in (("out", "out" if v == "wakes" else "out_run"),
                             ("direct", "direct" if v == "wakes" else "direct_run"),
                             ("ctx", "ctx" if v == "wakes" else "ctx_run")):
                shifts = {k: -per[k][key] / per[k][base] for k in reps}
                line[f"{v}_shift_{tag}"] = -sum(per[k][key] for k in reps) / sum(per[k][base] for k in reps)
                line[f"{v}_shift_{tag}_per_repeat"] = [round(shifts[k], 6) for k in reps]
        f10 = {k: per[k]["first10"] for k in reps}
        line["first10_shift_out_per_repeat"] = [round(-f10[k]["outside_ms"] / f10[k]["cpu_ms"], 6) if f10[k]["cpu_ms"]
                                                else 0.0 for k in reps]
        line["first10_shift_direct_per_repeat"] = [round(-f10[k]["direct_ms"] / f10[k]["cpu_ms"], 6) if f10[k]["cpu_ms"]
                                                   else 0.0 for k in reps]
        rows.append(line)
    json.dump(rows, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
