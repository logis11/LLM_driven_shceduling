"""Compile the gaming files in memory and report each game-chain member's RUN
value, the chain's per-frame sum and longest stage, and the periodic tasks'
TIMER periods. Read-only. Usage: python3 chain_scan.py <repo-root> <file-id>..."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "dataset" / "tools"))
from wlc import Library, Timeline, compile_timeline  # noqa: E402

lib = Library(root / "dataset" / "archetypes.yaml")
wanted = set(sys.argv[2:])


def runs(prog, acc):
    for s in prog:
        if s["op"] == "RUN":
            acc.append(s)
        elif s["op"] == "LOOP":
            runs(s["body"], acc)
    return acc


def timers(prog, acc):
    for s in prog:
        if s["op"] == "TIMER":
            acc.append(s)
        elif s["op"] == "LOOP":
            timers(s["body"], acc)
    return acc


for path in sorted((root / "dataset" / "timelines").glob("**/*.timeline.yaml")):
    fid = path.name.replace(".timeline.yaml", "")
    if fid not in wanted:
        continue
    tl = Timeline(path, lib)
    canonical, report = compile_timeline(tl, lib, "single")
    print(f"=== {fid}  T_end={canonical.get('meta', {}).get('t_end', canonical.get('t_end'))}")
    chain = []
    for ev in canonical["events"]:
        if ev["op"] != "arrive":
            continue
        tid = ev["id"]
        rs = runs(ev["program"], [])
        ts = timers(ev["program"], [])
        if tid.startswith("game") or ts:
            rv = [r.get("us", r.get("value_us", r.get("dist"))) for r in rs]
            tv = [t.get("period_us", t.get("us", t.get("period"))) for t in ts]
            print(f"  {tid:14s} {ev['name']:16s} arrive={ev.get('t', ev.get('arrive'))} RUN={rv} TIMER={tv}")
            if tid.startswith("game"):
                for r in rs:
                    v = r.get("us", r.get("value_us"))
                    if isinstance(v, (int, float)):
                        chain.append((tid, v))
    if chain:
        total = sum(v for _, v in chain)
        longest = max(chain, key=lambda x: x[1])
        second = sorted((v for _, v in chain), reverse=True)[1] if len(chain) > 1 else None
        print(f"  chain members {len(chain)}: per-frame RUN sum {total:.0f} us; longest {longest[0]} {longest[1]:.0f} us; second {second}")
