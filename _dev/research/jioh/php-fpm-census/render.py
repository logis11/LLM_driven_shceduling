#!/usr/bin/env python3
"""The record's two value tables from the census outputs: every carried component (effect.py's rows, direct.py's
split) and every CPU-sum value (effect_extra.py's rows).

  python3 -I render.py <effect-components.json> <effect-extra.json> <out dir holding direct-*.json>
"""
import glob
import json
import os
import sys

rows = json.load(open(sys.argv[1]))
extra = json.load(open(sys.argv[2]))
direct = {}
for f in glob.glob(os.path.join(sys.argv[3], "direct-*.json")):
    for sec, v in json.load(open(f)).items():
        for comp, r in v.items():
            direct[(sec.split()[0], sec.split()[1] if " " in sec else None, comp)] = r["direct"]

pc = lambda x: f"{100 * x:+.3f} %"
hw = lambda x: "—" if x is None else f"±{100 * x:.2f} %"
print("| entry | phase | component | k | wakes | outside (direct) | per repeat, min–max | wake rate: shift / half-width | gap mean | run mean |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    if r["component"].startswith("event "):
        continue
    ph = r["phase"]
    d = direct.get((r["entry"], ph, r["component"]), direct.get((r["entry"], None, r["component"]), 0 if not r["outside"] else "?"))
    pr = r["per_repeat_outside"]
    cells = []
    for v in ("rate", "gap", "run"):
        s, h = r.get(f"{v}_shift_out"), r.get(f"{v}_hw")
        mark = " **beyond**" if s is not None and h is not None and abs(s) > h else ""
        cells.append("—" if s is None else f"{pc(s)} / {hw(h)}{mark}")
    print(f"| {r['entry']} | {ph} | `{r['component']}` | {r['k']} | {r['wakes']} | {r['outside']} ({d}) | "
          f"{min(pr)}–{max(pr)} | " + " | ".join(cells) + " |")
print()
print("| entry / section | value | k | wakes | outside | outside run share | value's half-width | bound on the shift |")
print("|---|---|---|---|---|---|---|---|")
for r in extra:
    if "field" in r:
        print(f"| {r['section']} | {r['value']} | {r['k']} | {r['wakes']} | {r['outside']} | "
              f"{100 * r['outside_run_ms'] / r['tree_run_ms']:.3f} % of the tree's run | ±{100 * r['half_width']:.2f} % | "
              f"{pc(r['shift_bound'])} |")
    elif "program" in r:
        print(f"| {r['section']} ({r['program']}) | runs between blocks, block per run | {r['k']} | {r['wakes']} | "
              f"{r['outside']} | {100 * (r['run_share'] or 0):.3f} % | see text | ≤ {100 * (r['count_share'] or 0):.3f} % of the runs |")
    else:
        print(f"| {r['section']} (`{r['role']}`) | member steps / dispatch run | {r['k']} | {r['wakes']} | {r['outside']} | "
              f"{100 * (r['run_share'] or 0):.3f} % | see text | 0 |")
