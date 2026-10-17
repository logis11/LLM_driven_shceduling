"""Ad-hoc checks cited in the report: query points and constant-answer baselines, familiarity
annotations, compiler-child burst exposure at 10 ms, C2 gaming per-frame load, last-tick arithmetic."""
import json, glob, collections
R = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single/"
def L(f): return json.load(open(R + f + ".workload.json"))
def arr(d): return {e["id"]: e for e in d["events"] if e["op"] == "arrive"}

# 1. query points (telemetry changes at arrivals and pinned departs) and baselines
tot = term = amb = graded = pcm = 0; files = set(); truths = []; modes = []
for p in sorted(glob.glob(R + "*.json")):
    d = json.load(open(p)); fid = d["meta"]["id"]; times = set()
    for e in d["events"]:
        if e["op"] == "arrive":
            times.add(e["t"])
            if "depart" in e: times.add(e["depart"])
    for t in sorted(times):
        tot += 1
        seg = [g for g in d["ground_truth"] if g["t_start"] <= t < g["t_end"]]
        if not seg: term += 1; continue
        g = seg[0]
        if g["mode"] == "ambiguous": amb += 1; continue
        graded += 1; files.add(fid); pcm += bool(g["attributes"].get("pre_committed_miss"))
        truths.append(g["attributes"]["background_wanted"]); modes.append(g["mode"])
c = collections.Counter(modes)
print(f"1. query points {tot}, terminal {term}, ambiguous {amb}, graded {graded} in {len(files)} files, on pre_committed_miss {pcm}; "
      f"constant true {sum(truths)/len(truths):.3f}; majority mode {c.most_common(1)} {c.most_common(1)[0][1]/len(modes):.3f}")
# 2. familiarity annotations
print("2. familiarity:", [(json.load(open(p))["meta"]["id"], g["familiarity"]) for p in sorted(glob.glob(R+"*.json")) for g in json.load(open(p))["ground_truth"] if "familiarity" in g])
# 3. compiler children vs a 10 ms slice
for f in ("c1-compile", "c7-compile", "c3-workday", "c6-dual"):
    b = arr(L(f))["build"]; ch = b["spawn_table"]
    runs = [s["us"] for c_ in ch for s in c_["program"] if s["op"] == "RUN"]
    reach = sum(any(s["op"] == "RUN" and s["us"] >= 10000 for s in c_["program"]) for c_ in ch)
    q2 = sum(any(s["op"] == "RUN" and s["us"] >= 30000 for s in c_["program"]) for c_ in ch)
    print(f"3. {f}: {len(ch)} children; with a RUN >= 10 ms: {reach}; with a RUN >= 30 ms: {q2}; CPU past the first 10 ms of a RUN: {100*sum(max(0,r-10000) for r in runs)/sum(runs):.1f}%")
# 4. C2 gaming per-frame load and the last tick before T_end
for f, T in (("c2-p2a", 120_000_000), ("c1-gaming", 60_000_000), ("c7-gaming", 60_000_000)):
    a = arr(L(f))
    chain = sum([s["us"] for s in e["program"][0]["body"] if s["op"] == "RUN"][0] for k, e in a.items() if ".chain." in k)
    def lanes(e):
        b = e["program"][0]["body"]; r = [s["us"] for s in b if s["op"] == "RUN"][0]; s_ = [s["us"] for s in b if s["op"] == "SLEEP"][0]
        return r / (r + s_)
    tails = sum(lanes(e) for k, e in a.items() if ".tail." in k)
    comp = [s["us"] for s in a["compositor"]["program"][0]["body"] if s["op"] == "RUN"][0] if "compositor" in a else 0
    last_k = (T - 1) // 16667; last_tick = last_k * 16667
    print(f"4. {f}: chain {chain} us/frame, tails {tails:.4f} lanes = {tails*16667:.0f} us/frame, compositor {comp}; "
          f"ticks consumed by T_end: {last_k+1}; last tick {last_tick}; T_end - last tick = {T-last_tick} us vs chain work {chain}")
