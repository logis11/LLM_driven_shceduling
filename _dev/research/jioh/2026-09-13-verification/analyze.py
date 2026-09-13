import json, glob, os, sys, statistics as st, collections, math, pathlib
REPO = pathlib.Path("/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling")
sys.path.insert(0, str(REPO / "dataset/tools"))
from wlc import Library, Timeline, compile_timeline  # noqa
from wlc.compiler import canonical_bytes  # noqa

BUILD = REPO / "dataset/build"
TL = REPO / "dataset/timelines/coreset"
SLICES = [500, 750, 900, 1000, 1200, 2000, 3000, 5000, 10000, 20000, 100000]


def flat(prog):
    for s in prog:
        if s["op"] == "LOOP":
            yield from flat(s["body"])
        else:
            yield s


def section(t):
    print("\n" + "#" * 8, t)


lib = Library(REPO / "dataset/archetypes.yaml")
reports, files = {}, {}
section("1 recompile in-process: byte identity with build + per-task demand")
mismatch = 0
for path in sorted(TL.glob("*.timeline.yaml")):
    tl = Timeline(path, lib)
    for mode in ("single", "native"):
        canon, rep = compile_timeline(tl, lib, mode, rel_path=path.relative_to(REPO).as_posix())
        on_disk = (BUILD / f"coreset-{mode}" / f"{tl.id}.workload.json").read_bytes()
        if canonical_bytes(canon) != on_disk:
            mismatch += 1
            print("MISMATCH", tl.id, mode)
        reports[(tl.id, mode)] = rep
        files[(tl.id, mode)] = canon
print("files compiled:", len(reports), "byte mismatches vs build:", mismatch)


def per_task_share(fid, mode="single"):
    r = reports[(fid, mode)]
    d = r["duration_us"]
    groups = collections.OrderedDict()
    for tid, us in r["per_task"].items():
        key = tid
        for pat in (".tail.", ".chain.", "renderers.", "webhelper.", "daemons."):
            if pat in tid:
                key = tid.split(pat)[0] + pat + "*"
        groups[key] = groups.get(key, 0) + us
    return {k: round(v / d, 4) for k, v in groups.items()}, round(r["utilization"], 4)


section("2 demand breakdown (single) per file, lanes over file duration")
for fid in sorted({k[0] for k in reports}):
    shares, u = per_task_share(fid)
    un, _ = per_task_share(fid, "native")
    print(f"{fid}: total single={u} native={round(reports[(fid,'native')]['utilization'],4)} :: {shares}")

section("3 chains: sum of stage RUNs, frame slack, longest stage, compositor")
for (fid, mode), canon in sorted(files.items()):
    arr = [e for e in canon["events"] if e["op"] == "arrive"]
    chain = [e for e in arr if ".chain." in e["id"]]
    if not chain:
        continue
    prefixes = sorted({e["id"].split(".chain.")[0] for e in chain})
    for p in prefixes:
        members = [e for e in chain if e["id"].startswith(p + ".chain.")]
        runs = {int(e["id"].rsplit(".", 1)[1]): [s["us"] for s in flat(e["program"]) if s["op"] == "RUN"][0] for e in members}
        period = [s["period_us"] for s in flat(members[0]["program"]) if s["op"] == "TIMER"]
        head = [e for e in members if e["id"].endswith(".chain.1")][0]
        period = [s["period_us"] for s in flat(head["program"]) if s["op"] == "TIMER"][0]
        total = sum(runs.values())
        longest = max(runs.values())
        comp = [e for e in arr if e["id"] == "compositor"]
        comp_s = ""
        if comp:
            cr = [s["us"] for s in flat(comp[0]["program"]) if s["op"] == "RUN"][0]
            comp_s = f" compositor RUN={cr}; chain+compositor per frame={total+cr} ({(total+cr)/period:.3f} lanes) slack={period-total-cr}"
        print(f"{fid}[{mode}] {p}: stages={len(runs)} sum={total} period={period} frame_slack={period-total} "
              f"longest=chain.{max(runs,key=runs.get)}={longest} second={sorted(runs.values())[-2]} min={min(runs.values())}{comp_s}")

section("4 interactive bursts vs slices (fraction of bursts < slice; CPU beyond the slice)")
INTERACTIVE = {}
for (fid, mode), canon in sorted(files.items()):
    if mode != "single":
        continue
    for e in canon["events"]:
        if e["op"] != "arrive" or e["program"] and e["program"][0]["op"] == "LOOP":
            continue
        ops = e["program"]
        if not any(s["op"] == "WAIT" and s.get("channel", "").startswith("input:") for s in ops):
            continue
        runs = [s["us"] for s in ops if s["op"] == "RUN"]
        if not runs:
            print(f"{fid} {e['id']} ({e['name']}): no bursts (never focused)")
            continue
        INTERACTIVE[(fid, e["id"])] = runs
        row = []
        for sl in (2000, 10000, 20000, 100000):
            below = sum(r < sl for r in runs) / len(runs)
            beyond = sum(max(0, r - sl) for r in runs) / sum(runs)
            row.append(f"<{sl//1000}ms {below:.1%} (cpu past slice {beyond:.1%})")
        q = sorted(runs)
        p10 = q[int(0.1 * len(q))]
        print(f"{fid} {e['id']} ({e['name']}): n={len(runs)} median={st.median(runs):.0f} p10={p10} mean={st.mean(runs):.0f} max={max(runs)} | " + "; ".join(row))

section("5 finite IO-shaped jobs: B1 batch-class exposure per slice, wall time, completion vs file end")
for (fid, mode), canon in sorted(files.items()):
    if mode != "single":
        continue
    dur = reports[(fid, mode)]["duration_us"]
    segs = canon["ground_truth"]
    for e in canon["events"]:
        if e["op"] != "arrive":
            continue
        ops = e["program"]
        if not ops or ops[0]["op"] == "LOOP" or not any(s["op"] == "SLEEP" for s in ops):
            continue
        runs = [s["us"] for s in ops if s["op"] == "RUN"]
        sleeps = [s["us"] for s in ops if s["op"] == "SLEEP"]
        wall = sum(runs) + sum(sleeps)
        # uncontended delivered CPU by file end
        t, cpu = e["t"], 0
        finish = None
        for s in ops:
            if s["op"] == "RUN":
                take = min(s["us"], max(0, dur - t))
                cpu += take
                t += s["us"]
            elif s["op"] == "SLEEP":
                t += s["us"]
            elif s["op"] == "EXIT":
                finish = t
        seg_end = max(g["t_end"] for g in segs if g["t_start"] <= e["t"] < g["t_end"])
        print(f"{fid} {e['id']} ({e['name']}): arrive={e['t']/1e6:.0f}s chunks={len(runs)} RUN sum={sum(runs)/1e6:.3f}s med={st.median(runs):.0f} mean={st.mean(runs):.0f} max={max(runs)} "
              f"SLEEP med={st.median(sleeps):.0f} mean={st.mean(sleeps):.0f} duty={sum(runs)/wall:.3f} "
              f"uncontended finish={finish/1e6:.1f}s vs segment end {seg_end/1e6:.0f}s / file end {dur/1e6:.0f}s; "
              f"uncontended CPU by file end={cpu/1e6:.3f}s ({cpu/sum(runs):.1%} of total_work; {cpu/dur:.4f} lanes vs static {sum(runs)/dur:.4f})")
        for sl in SLICES:
            n_hit = sum(r >= sl for r in runs)
            cpu_b = sum(max(0, r - sl) for r in runs)
            print(f"    slice {sl:>6}: chunks reaching a full slice {n_hit}/{len(runs)} ({n_hit/len(runs):.1%}); CPU in batch class {cpu_b/sum(runs):.2%}")

section("6 periodic / sleep loops: wineserver, daemons, electron — wakes inside lifetime")
for (fid, mode), canon in sorted(files.items()):
    if mode != "single":
        continue
    for e in canon["events"]:
        if e["op"] != "arrive" or e["name"] not in ("wineserver",):
            continue
        body = e["program"][0]["body"]
        sl = [s["us"] for s in body if s["op"] == "SLEEP"][0]
        run = [s["us"] for s in body if s["op"] == "RUN"][0]
        life = e["depart"] - e["t"]
        wakes = life // (sl + run)
        print(f"{fid} {e['id']}: SLEEP={sl} RUN={run} lifetime={life} -> completed wake-runs in lifetime={wakes} (first RUN at t={e['t']+sl})")

section("7 c3-creation: external wakes of video-editor after 240 s")
c = files[("c3-creation", "single")]
w = [x["t"] for x in c["events"] if x["op"] == "wake" and x["target"] == "video-editor"]
print("video-editor wakes: first", min(w), "last", max(w), "count", len(w), "after 240s:", sum(t >= 240e6 for t in w))
w = [x["t"] for x in c["events"] if x["op"] == "wake" and x["target"] == "photo-editor"]
print("photo-editor wakes: last", max(w))

section("8 C2 P1 event identity apart from name")
a = files[("c2-p1a", "single")]; b = files[("c2-p1b", "single")]
def strip(c):
    ev = json.loads(json.dumps(c["events"]))
    for x in ev:
        x.pop("name", None)
    return ev
print("p1 events identical apart from names:", strip(a) == strip(b))
print("p1 name diffs:", [(x["id"], x["name"], y["name"]) for x, y in zip(a["events"], b["events"]) if x.get("name") != y.get("name")])
for p in ("p2", "p3"):
    a = files[(f"c2-{p}a", "single")]; b = files[(f"c2-{p}b", "single")]
    print(p, "events identical apart from names:", strip(a) == strip(b))
