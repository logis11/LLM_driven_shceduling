"""first_hop_tables.py JSON... — per app and phase, per component: wakes and CPU summed over repeats, the shares by waker class."""
import collections, json, sys
tot = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0])))
spans = collections.defaultdict(float); reps = collections.defaultdict(set)
for f in sys.argv[1:]:
    for r in json.load(open(f)):
        key = (r["app"], r["phase"]); spans[key] += r["span_s"]; reps[key].add(r["repeat"])
        for comp, d in r["components"].items():
            for c, (n, cpu) in d.items():
                t = tot[key][comp][c]; t[0] += n; t[1] += cpu
CL = ["x", "tree", "tree_same_cpu", "idle", "kernel", "other", "none"]
for key in sorted(tot):
    comps = tot[key]; app_cpu = sum(v[1] for d in comps.values() for v in d.values())
    print(f"\n## {key[0]} {key[1]}: {len(reps[key])} repeats, {spans[key]:.0f} s, app CPU share {app_cpu/1000/spans[key]:.3f}")
    print("| component | wakes/s | CPU share of app | " + " | ".join(f"{c} wakes/CPU" for c in CL) + " |")
    print("|---|---|---|" + "---|" * len(CL))
    for comp, d in sorted(comps.items(), key=lambda kv: -sum(v[1] for v in kv[1].values()))[:8]:
        n = sum(v[0] for v in d.values()); cpu = sum(v[1] for v in d.values())
        if cpu / app_cpu < 0.005 and n / spans[key] < 5: continue
        cells = [f"{d[c][0]/n:.2f}/{d[c][1]/cpu if cpu else 0:.2f}" if c in d else "" for c in CL]
        print(f"| {comp} | {n/spans[key]:.1f} | {cpu/app_cpu:.2f} | " + " | ".join(cells) + " |")

# the wakers of each component, summed over repeats
wk = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0])))
for f in sys.argv[1:]:
    for r in json.load(open(f)):
        key = (r["app"], r["phase"])
        for comp, d in (r.get("wakers") or {}).items():
            for w, (n, cpu) in d.items():
                t = wk[key][comp][w]; t[0] += n; t[1] += cpu
print("\n# Wakers")
for key in sorted(wk):
    comps = tot[key]; app_cpu = sum(v[1] for d in comps.values() for v in d.values())
    print(f"\n## {key[0]} {key[1]}")
    for comp, d in sorted(comps.items(), key=lambda kv: -sum(v[1] for v in kv[1].values()))[:8]:
        n = sum(v[0] for v in d.values()); cpu = sum(v[1] for v in d.values())
        if cpu / app_cpu < 0.005 and n / spans[key] < 5: continue
        top = sorted(wk[key][comp].items(), key=lambda kv: -kv[1][0])[:5]
        print(f"- {comp} ({n/spans[key]:.1f}/s, {cpu/app_cpu:.2f} of CPU): " + "; ".join(f"{w} {v[0]/n:.2f}/{v[1]/cpu if cpu else 0:.2f}" for w, v in top))
