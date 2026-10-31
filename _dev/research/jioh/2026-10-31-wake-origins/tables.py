"""tables.py JSON... — per app and phase, per component: wakes/s, CPU share, and the shares by wake-chain origin."""
import collections, json, sys
tot = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0])))
spans = collections.defaultdict(float); reps = collections.defaultdict(set)
for f in sys.argv[1:]:
    for r in json.load(open(f)):
        key = (r["app"], r["phase"]); spans[key] += r["span_s"]; reps[key].add(r["repeat"])
        for comp, d in r["components"].items():
            for c, (n, cpu) in d.items():
                t = tot[key][comp][c]; t[0] += n; t[1] += cpu
CL = ["timer", "input", "x", "ext", "irq", "unknown", "none"]
for key in sorted(tot):
    comps = tot[key]; app_cpu = sum(v[1] for d in comps.values() for v in d.values())
    allw = collections.defaultdict(lambda: [0, 0.0])
    for d in comps.values():
        for c, v in d.items(): allw[c][0] += v[0]; allw[c][1] += v[1]
    n_all = sum(v[0] for v in allw.values())
    print(f"\n## {key[0]} {key[1]}: {len(reps[key])} repeats, app CPU share {app_cpu/1000/spans[key]:.3f}; whole tree " +
          ", ".join(f"{c} {allw[c][0]/n_all:.2f}/{allw[c][1]/app_cpu:.2f}" for c in CL if c in allw))
    print("| component | wakes/s | CPU share of app | " + " | ".join(CL) + " |")
    print("|---|---|---|" + "---|" * len(CL))
    for comp, d in sorted(comps.items(), key=lambda kv: -sum(v[1] for v in kv[1].values()))[:10]:
        n = sum(v[0] for v in d.values()); cpu = sum(v[1] for v in d.values())
        if cpu / app_cpu < 0.01 and n / spans[key] < 5: continue
        cells = [f"{d[c][0]/n:.2f}/{d[c][1]/cpu if cpu else 0:.2f}" if c in d else "" for c in CL]
        print(f"| {comp} | {n/spans[key]:.1f} | {cpu/app_cpu:.2f} | " + " | ".join(cells) + " |")
