#!/usr/bin/env python3
"""effect.py's reading with the chain rule's split beside it: per carried component, how far its three values would
move with every outside-cause wake removed (the rule as written, effect.py's `out`), with only the wakes whose own
wakeup row names the outside waker removed (`direct`: the inherited wakes put back), and with the unplaced python3
wakers added (`up`) — each against the value's 95 % half-width.

  python3 -I effect_split.py <census.json> [<census.json> ...] > effect.json

A census file is effect.py's form; each component may also hold `split`: {"direct": {"n", "run"}, "inherited":
{"n", "run"}} over its outside-cause wakes (a component without it is read as all direct).
"""

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from effect import values  # noqa: E402
sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
from meas.stability import stability, ratio_stability  # noqa: E402


def direct_only(reps):
    """The repeats with each component's `outside` class cut to its direct wakes."""
    out = copy.deepcopy(reps)
    for res in out.values():
        for c in res.values():
            o = c["classes"].get("outside")
            if o is not None and "split" in c:
                c["classes"]["outside"] = dict(c["split"]["direct"])
    return out


def shifts(reps, comp, drop):
    base, new = values(reps, comp, ()), values(reps, comp, drop)
    out = {}
    for name, ia, ib in (("rate", 0, None), ("gap", 1, 2), ("run", 3, 2)):
        if name == "rate":
            a = stability(base[0], keep_zero=True)
            va, vb = sum(base[0].values()) / len(base[0]), sum(new[0].values()) / len(new[0])
        else:
            a = ratio_stability(base[ia], base[ib])
            if not sum(base[ib].values()):
                continue
            va = sum(base[ia].values()) / sum(base[ib].values())
            vb = sum(new[ia].values()) / max(sum(new[ib].values()), 1)
        if not va:
            continue
        out[f"{name}_value"], out[f"{name}_hw"], out[f"{name}_shift"] = va, a["half_width"], (vb - va) / va
    return out


def main():
    rows = []
    for path in sys.argv[1:]:
        for entry, e in json.load(open(path)).items():
            if e.get("field") in ("cycle", "input_run") or e.get("kind") == "batch":
                continue
            reps = e["repeats"]
            dreps = direct_only(reps)
            for comp in sorted({c for res in reps.values() for c in res}):
                cs = [res[comp] for res in reps.values() if comp in res]
                line = {"entry": entry, "campaign": e["campaign"], "phase": e["phase"], "component": comp,
                        "k": len(cs), "wakes": sum(c["n"] for c in cs),
                        "outside": sum(c["classes"].get("outside", {}).get("n", 0) for c in cs),
                        "direct": sum(c.get("split", {}).get("direct", {}).get("n",
                                      c["classes"].get("outside", {}).get("n", 0)) for c in cs),
                        "harness_python": sum(c["classes"].get("harness-python", {}).get("n", 0) for c in cs),
                        "stimulus": sum(c["classes"].get("stimulus", {}).get("n", 0) for c in cs),
                        "per_repeat_outside": [c["classes"].get("outside", {}).get("n", 0) for c in cs]}
                for tag, rr, drop in (("out", reps, ("outside",)), ("direct", dreps, ("outside",)),
                                      ("up", reps, ("outside", "harness-python"))):
                    for k, v in shifts(rr, comp, drop).items():
                        if k.endswith("_shift"):
                            line[f"{k}_{tag}"] = v
                        else:
                            line[k] = v
                rows.append(line)
    json.dump(rows, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
