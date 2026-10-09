import json, sys
from collections import Counter
def load(p): return json.load(open(p))
def summarize(c):
    wakes = Counter(e["channel"].split(":")[0] + ":" + e["target"] for e in c["events"] if e["op"] == "wake")
    inputs = {e["target"]: [] for e in c["events"] if e["op"]=="wake" and e["channel"].startswith("input:")}
    for e in c["events"]:
        if e["op"]=="wake" and e["channel"].startswith("input:"): inputs[e["target"]].append(e["t"])
    def runs(prog):
        s = 0
        for st in prog:
            if st["op"]=="RUN": s += st["us"]
            elif st["op"]=="LOOP": s += runs(st.get("body", []))
        return s
    demand = {e["id"]: runs(e["program"]) for e in c["events"] if e["op"]=="arrive"}
    nops = {e["id"]: len(e["program"]) for e in c["events"] if e["op"]=="arrive"}
    return wakes, inputs, demand, nops
for f in sys.argv[1:]:
    a, b = load(f"dataset/build/coreset-single/{f}.workload.json"), load(f"dataset/build/coreset-single/{f}@replay.workload.json")
    wa, ia, da, na = summarize(a); wb, ib, db, nb = summarize(b)
    print(f"== {f}: base vs replay")
    for k in sorted(set(wa)|set(wb)): print(f"   wakes {k:22s} {wa.get(k,0):7d} -> {wb.get(k,0):7d}")
    for k in sorted(set(da)|set(db)): print(f"   demand {k:21s} {da.get(k,0)/1e6:9.3f} s -> {db.get(k,0)/1e6:9.3f} s   ops {na.get(k)} -> {nb.get(k)}")
    print("   input wakes identical:", ia == ib, "| meta identical but id:", {k:v for k,v in a['meta'].items() if k!='id'} == {k:v for k,v in b['meta'].items() if k!='id'})
