#!/usr/bin/env python3
"""How far each carried component value would move if its outside-cause wakes were removed, against its spread.

  python3 -I effect.py <census.json> [<census.json> ...] > effect.json

A census file: {entry: {"campaign", "phase", "repeats": {k: {component: {"n", "run", "span", "classes": {class:
{"n", "run"}}}}}}}. Per component, the three values the stability rule tests, read as the pools read them
(meas/stability.py): the wake rate by its per-repeat values; the gap mean as the carried table carries it, the wake
times wrapped round the phase, so Σspan / Σn over the repeats; the run mean Σrun / Σn — each with its 95 % half-width
(`stability`, `ratio_stability`). Removing a wake lowers n (and the run sum by its run): the shift is the value without
the outside-cause wakes against the value with them. `harness-python` (a python3 waker the trace cannot place between
a harness driver and a scripted peer) is counted with `outside` in the upper bound and stated apart.
"""

import json
import sys

sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
from meas.stability import stability, ratio_stability  # noqa: E402

GONE = ("outside",)
GONE_UPPER = ("outside", "harness-python")


def values(reps, comp, drop):
    rate, spans, ns, runs = {}, {}, {}, {}
    for k, res in reps.items():
        c = res.get(comp)
        if c is None:
            continue
        o = sum(c["classes"].get(x, {}).get("n", 0) for x in drop)
        orun = sum(c["classes"].get(x, {}).get("run", 0.0) for x in drop)
        n = c["n"] - o
        rate[k] = n / c["span"]
        spans[k], ns[k], runs[k] = c["span"] * 1000.0, n, c["run"] - orun
    return rate, spans, ns, runs


def main():
    rows = []
    for path in sys.argv[1:]:
        for entry, e in json.load(open(path)).items():
            if e.get("field") in ("cycle", "input_run") or entry in ("file-archiver", "game-download") \
                    or entry.startswith("compiler-child"):
                continue    # CPU sums over the tree: effect_extra.py
            reps = e["repeats"]
            comps = sorted({c for res in reps.values() for c in res})
            for comp in comps:
                base = values(reps, comp, ())
                k = len(base[0])
                gone = {kk: sum(res[comp]["classes"].get(x, {}).get("n", 0) for x in GONE)
                        for kk, res in reps.items() if comp in res}
                upper = {kk: sum(res[comp]["classes"].get(x, {}).get("n", 0) for x in GONE_UPPER)
                         for kk, res in reps.items() if comp in res}
                total = sum(base[2].values())
                line = {"entry": entry.split()[0], "campaign": e["campaign"], "phase": e["phase"], "component": comp, "k": k,
                        "wakes": total, "outside": sum(gone.values()), "outside_upper": sum(upper.values()),
                        "per_repeat_outside": [gone[x] for x in reps if x in gone],
                        "per_repeat_upper": [upper[x] for x in reps if x in upper]}
                for tag, drop in (("out", GONE), ("up", GONE_UPPER)):
                    new = values(reps, comp, drop)
                    for name, a, b in (("rate", stability(base[0], keep_zero=True), stability(new[0], keep_zero=True)),
                                       ("gap", ratio_stability(base[1], base[2]), ratio_stability(new[1], new[2])),
                                       ("run", ratio_stability(base[3], base[2]), ratio_stability(new[3], new[2]))):
                        if a["mean"] in (None, 0) or b["mean"] is None:
                            continue
                        # the shift from unrounded values
                        if name == "rate":
                            va = sum(base[0].values()) / len(base[0]); vb = sum(new[0].values()) / len(new[0])
                        elif name == "gap":
                            va = sum(base[1].values()) / sum(base[2].values()); vb = sum(new[1].values()) / max(sum(new[2].values()), 1)
                        else:
                            va = sum(base[3].values()) / sum(base[2].values()); vb = sum(new[3].values()) / max(sum(new[2].values()), 1)
                        line[f"{name}_value"] = va
                        line[f"{name}_hw"] = a["half_width"]
                        line[f"{name}_shift_{tag}"] = (vb - va) / va
                rows.append(line)
    json.dump(rows, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
