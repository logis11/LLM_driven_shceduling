#!/usr/bin/env python3
"""A census file's causes summed over the repeats, per section and component: the classes, then every label that is
not the component's own, most frequent first.

  python3 -I labels.py <census.json> [--top N]
"""
import collections
import json
import sys

d = json.load(open(sys.argv[1]))
top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 40
for sec, v in d.items():
    lab, cls = collections.Counter(), collections.Counter()
    for res in v["repeats"].values():
        for comp, c in res.items():
            for l, n in c["labels"].items():
                lab[(comp, l)] += n
            for cl, x in c["classes"].items():
                cls[cl] += x["n"]
    print(f"== {sec} ({v['campaign']}, {len(v['repeats'])} repeats): {dict(cls)}")
    for (comp, l), n in sorted(lab.items(), key=lambda kv: -kv[1])[:top]:
        print(f"   {n:7d}  {comp} | {l}")
