import json, glob, os, sys, pathlib
REPO = pathlib.Path("/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling")
sys.path.insert(0, str(REPO / "dataset/tools"))
from wlc import Library, Timeline, compile_timeline
lib = Library(REPO / "dataset/archetypes.yaml")
def flat(p):
    for s in p:
        if s["op"]=="LOOP": yield from flat(s["body"])
        else: yield s
def alone_cpu(e, T):
    """CPU the task could receive by T if it were alone on the lane (upper bound)."""
    p = e["program"]; t = e["t"]
    if p and p[0]["op"] == "LOOP":
        return None  # periodic: static estimate already RUN/period*lifetime
    if "spawn_table" in e:
        cpu = sum(s["us"] for s in p if s["op"]=="RUN") + sum(s["us"] for c in e["spawn_table"] for s in c["program"] if s["op"]=="RUN")
        return min(cpu, T - t)
    if any(s["op"]=="WAIT" and s.get("channel","").startswith("input:") for s in p):
        return None  # interactive: bursts gated by wakes, estimate = sum of bursts
    cpu = 0
    for s in p:
        if t >= T: break
        if s["op"]=="RUN":
            cpu += min(s["us"], T - t); t += s["us"]
        elif s["op"]=="SLEEP":
            t += s["us"]
    return cpu
rows=[]
for path in sorted((REPO/"dataset/timelines/coreset").glob("*.timeline.yaml")):
    tl = Timeline(path, lib)
    canon, rep = compile_timeline(tl, lib, "single")
    T = rep["duration_us"]
    arr = {e["id"]: e for e in canon["events"] if e["op"]=="arrive"}
    total = 0; notes=[]
    for tid, d in rep["per_task"].items():
        a = alone_cpu(arr[tid], T) if tid in arr else None
        if a is not None and a < d:
            notes.append(f"{tid}: static {d/1e6:.2f}s -> alone-deliverable {a/1e6:.2f}s")
            total += a
        else:
            total += d
    rows.append((tl.id, rep["demand_class"], rep["utilization"], total/T, notes))
for fid, cls, u, ud, notes in rows:
    flag = ""
    if cls == "oversubscribed" and not (1.0 <= ud <= 1.5): flag = "  <-- leaves [1.00,1.50] once undeliverable work is removed"
    print(f"{fid:14s} {cls:14s} static={u:.3f} deliverable-bound={ud:.3f}{flag}")
    for n in notes: print("      ", n)
