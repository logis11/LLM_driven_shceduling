#!/usr/bin/env python3
"""effect.py's rows as a Markdown table: per component its wakes, the outside-cause wakes (the upper bound with the
unplaced python3 wakers in brackets), and each value's shift against its 95 % half-width.

  python3 -I table.py <effect.json> [--all]   (without --all, the components with an outside-cause wake)
"""
import json
import sys

rows = json.load(open(sys.argv[1]))
show_all = "--all" in sys.argv
pc = lambda x: "—" if x is None else f"{100 * x:+.3f} %"
hw = lambda x: "—" if x is None else f"±{100 * x:.1f} %"
print("| entry | phase | component | k | wakes | outside (upper) | per repeat | wake rate shift / hw | gap mean shift / hw | run mean shift / hw |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    if not show_all and not r["outside_upper"]:
        continue
    pr = ",".join(str(x) for x in r["per_repeat_outside"])
    up = f" ({r['outside_upper']})" if r["outside_upper"] != r["outside"] else ""
    cells = []
    for v in ("rate", "gap", "run"):
        if f"{v}_shift_out" not in r:
            cells.append("—"); continue
        s = pc(r[f"{v}_shift_out"])
        if r.get(f"{v}_shift_up") is not None and abs(r[f"{v}_shift_up"] - r[f"{v}_shift_out"]) > 5e-6:
            s += f" ({pc(r[f'{v}_shift_up'])})"
        cells.append(f"{s} / {hw(r.get(f'{v}_hw'))}")
    print(f"| {r['entry']} | {r['phase']} | {r['component']} | {r['k']} | {r['wakes']} | {r['outside']}{up} | {pr} | " + " | ".join(cells) + " |")
