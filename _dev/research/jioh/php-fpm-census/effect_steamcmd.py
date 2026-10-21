#!/usr/bin/env python3
"""census_steamcmd.py's output read against the pooled record and the archetype: the check (the run and block means
reconstructed from the census's own reading against `steamcmd-pooled.json`'s, the quantile tables against
`dataset/archetypes.yaml`'s `steamcmd_run` and `steamcmd_block`), the outside-cause wakes by cause group
(effect_bg910.py's groups), the classes, and every carried value recomputed — the run mean and the block mean as the
pool's stability rule reads them (Σ / Σ n over the repeats, `ratio_stability`), the CPU total, and the two quantile
tables (p1 … p99.9, min, max, the eleven interval means; `meas/distribution.quantile_table` over the pooled samples) —
under the rule as written, direct.py's reading (the inherited put back) and chain_roots' own direct (`how` direct).

  python3 -I effect_steamcmd.py <steamcmd.json> <steamcmd-pooled.json> > effect-steamcmd.json   (--md: the tables)
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools")
import numpy as np  # noqa: E402
import yaml  # noqa: E402
from meas.distribution import quantile_table  # noqa: E402
from meas.stability import ratio_stability, stability  # noqa: E402
from effect_bg910 import GROUPS, group  # noqa: E402

ARCH = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/archetypes.yaml"
READINGS = ("rule", "direct", "how_direct")


def main():
    data, pooled = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    e = data["game-download"]
    R = e["repeats"]
    keys = sorted(R, key=int)
    q = pooled["runs"]["steamcmd"]["stability"]["quantities"]
    arch = yaml.safe_load(open(ARCH))["archetypes"]["game-download"]["params"]
    out = {"k": len(R), "repeats": keys}
    # census: classes, causes, split, check
    cl, c, how = collections.Counter(), collections.Counter(), collections.Counter()
    n = o = d = 0
    for k in keys:
        t = R[k]["tally"]["steamcmd"]
        n += t["n"]
        for x, v in t["classes"].items():
            cl[x] += v["n"]
        for lab, x in t["labels"].items():
            if lab.startswith("outside: "):
                c[group(lab[len("outside: "):])] += x
        how.update(t["how"])
        o += t["classes"].get("outside", {}).get("n", 0)
        d += t["split"]["direct"]["n"]
    out["census"] = {"wakes": n, "outside": o, "direct": d, "how": dict(how),
                     "classes": dict(cl), "by_cause": {g: c.get(g, 0) for g, _ in GROUPS},
                     "other": {g: x for g, x in c.items() if g.startswith("other: ")},
                     "check_differ": sum(R[k]["check_differ"] for k in keys),
                     "check_wakes": sum(R[k]["check_wakes"] for k in keys),
                     "per_repeat_outside": [R[k]["tally"]["steamcmd"]["classes"].get("outside", {}).get("n", 0) for k in keys],
                     "roots": sorted((dict(g, repeat=k) for k in keys for g in R[k]["roots"]["largest"]),
                                     key=lambda g: -g["wakes"])[:10],
                     "inherited_by_roots": sum(R[k]["roots"]["inherited"] for k in keys)}
    # the means
    V = {tag: [R[k]["values"][tag] for k in keys] for tag in ("base",) + READINGS}
    vals = {}
    for name, s_key, n_key, label in (("run", "run_sum", "run_n", "steam-fresh-shaped run between voluntary blocks (µs)"),
                                      ("block", "block_sum", "block_n", "steam-fresh-shaped block per run (µs)")):
        Q = q[label]
        line = {"pooled_mean": Q["mean"], "pooled_half_width": Q["half_width"]}
        for tag in ("base",) + READINGS:
            sums = {k: x[s_key] for k, x in zip(keys, V[tag])}
            cnts = {k: x[n_key] for k, x in zip(keys, V[tag])}
            st = ratio_stability(sums, cnts, 1.0, 5)   # background/pool.py: ABS_FLOOR_US 1.0, MIN_REPEATS 5
            m = sum(sums.values()) / sum(cnts.values())
            line[tag] = {"mean": m, "half_width": st["half_width"], "half_width_abs": st["half_width_abs"],
                         "passes": st["passes"]}
        base = line["base"]["mean"]
        line["check"] = (base - Q["mean"]) / Q["mean"]
        for tag in READINGS:
            line[tag]["shift"] = (line[tag]["mean"] - base) / base
        line["per_repeat_base"] = {k: x[s_key] / x[n_key] for k, x in zip(keys, V["base"])}
        line["per_repeat_rule_shift"] = {k: (y[s_key] / y[n_key]) / (x[s_key] / x[n_key]) - 1
                                         for k, x, y in zip(keys, V["base"], V["rule"])}
        vals[name] = line
    cpu = {tag: {k: x["cpu_us"] for k, x in zip(keys, V[tag])} for tag in ("base",) + READINGS}
    st = stability(cpu["base"], None, 5)
    vals["cpu"] = {"base_mean": sum(cpu["base"].values()) / len(keys), "half_width": st["half_width"],
                   **{tag: {"shift": sum(cpu[tag].values()) / sum(cpu["base"].values()) - 1} for tag in READINGS}}
    vals["removed"] = {tag: {"n": sum(x["removed"] for x in V[tag]), "run_ms": sum(x["removed_run_ms"] for x in V[tag]),
                             "busy_ms": sum(x["removed_busy_ms"] for x in V[tag])} for tag in READINGS}
    vals["block_sum_ms"] = {tag: sum(x["block_sum"] for x in V[tag]) / 1000.0 for tag in ("base",) + READINGS}
    vals["block_n"] = {tag: sum(x["block_n"] for x in V[tag]) for tag in ("base",) + READINGS}
    vals["share_runs_followed_by_a_block"] = {
        tag: [min(x["block_nonzero"] / x["block_n"] for x in V[tag]), max(x["block_nonzero"] / x["block_n"] for x in V[tag])]
        for tag in ("base",) + READINGS}
    out["values"] = vals
    # the quantile tables over the pooled samples
    tabs = {}
    out_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
    for name, field in (("run", "steamcmd_run"), ("block", "steamcmd_block")):
        tabs[name] = {"archetype": {x: arch[field][x] for x in ("p", "min", "max", "means")}}
        for tag in ("base", "rule", "direct"):
            arr = np.concatenate([np.load(os.path.join(out_dir, f"steamcmd-r{k}.npz"))[f"{name}_{tag}"] for k in keys])
            t = quantile_table(arr)
            del arr
            tabs[name][tag] = {"p": [round(x, 3) for x in t["p"]], "min": round(t["min"], 3), "max": round(t["max"], 3),
                               "means": [round(x, 3) for x in t["means"]]}
    out["tables"] = tabs
    if "--md" in sys.argv:
        render(out)
    else:
        json.dump(out, sys.stdout, indent=1)


def render(out):
    c = out["census"]
    print(f"k {out['k']}; wakes {c['wakes']}, outside {c['outside']} (direct, direct.py's reading: {c['direct']}); "
          f"how {c['how']}; check differs {c['check_differ']} of {c['check_wakes']}")
    print("classes", c["classes"])
    print("by cause", c["by_cause"], c["other"])
    v = out["values"]
    for name in ("run", "block"):
        L = v[name]
        print(f"{name}: pooled {L['pooled_mean']} ±{100 * L['pooled_half_width']:.2f} %; reconstructed "
              f"{L['base']['mean']:.4f} (check {100 * L['check']:+.4f} %, hw {L['base']['half_width']}, abs {L['base']['half_width_abs']})")
        for tag in READINGS:
            print(f"   {tag}: {L[tag]['mean']:.4f} shift {100 * L[tag]['shift']:+.3f} % (hw {L[tag]['half_width']}, abs "
                  f"{L[tag]['half_width_abs']}, passes {L[tag]['passes']})")
        rs = L["per_repeat_rule_shift"]
        print(f"   per repeat rule shift {100 * min(rs.values()):+.3f} … {100 * max(rs.values()):+.3f} %")
    print("cpu", v["cpu"])
    print("removed", v["removed"])
    print("block sum (ms)", v["block_sum_ms"], "block n", v["block_n"])
    print("share followed by a block", v["share_runs_followed_by_a_block"])
    for name, t in out["tables"].items():
        print(name)
        for tag, x in t.items():
            print(f"   {tag:9s} p {x['p']} min {x['min']} max {x['max']}")
            print(f"   {'':9s} means {x['means']}")
    for g in c["roots"][:8]:
        print("root", g)


if __name__ == "__main__":
    main()
