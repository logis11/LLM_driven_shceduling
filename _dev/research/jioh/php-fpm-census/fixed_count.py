#!/usr/bin/env python3
"""The second check on the outside-cause counts: a component whose wake count is the same in (nearly) every repeat
wakes on its own fixed timer, so a wake the trace attributes to an outside cause in a repeat that still holds the
usual count is one of the timer's own wakes named after the task the interrupt found running — had the outside
cause added it, that repeat would hold one more. Per component with an outside-cause wake: the modal per-repeat count,
the share of repeats at it, and the outside-cause wakes that fall in repeats at the modal count.

  python3 -I fixed_count.py <census.json> [<census.json> ...]
"""
import collections
import json
import sys

for path in sys.argv[1:]:
    for sec, e in json.load(open(path)).items():
        comps = sorted({c for r in e["repeats"].values() for c in r})
        for comp in comps:
            cs = {k: r[comp] for k, r in e["repeats"].items() if comp in r}
            o = {k: c["classes"].get("outside", {}).get("n", 0) for k, c in cs.items()}
            if not sum(o.values()) or len(cs) < 5:
                continue
            ns = collections.Counter(c["n"] for c in cs.values())
            mode, at = ns.most_common(1)[0]
            if at / len(cs) < 0.5:
                continue
            in_mode = sum(o[k] for k, c in cs.items() if c["n"] == mode)
            print(f"{sec} | {comp}: {at}/{len(cs)} repeats at {mode} wakes; outside-cause wakes {sum(o.values())}, "
                  f"{in_mode} of them in repeats at the modal count")
