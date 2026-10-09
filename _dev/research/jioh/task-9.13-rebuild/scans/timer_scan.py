"""Scan the compiled single-lane coreset: which tasks carry TIMER, and what
their first executed instruction is (descending LOOP heads). Also count wake
events. Read-only; compiles in memory via wlc."""
import pathlib
import sys
from collections import Counter

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "dataset" / "tools"))
from wlc import Library, Timeline, compile_timeline  # noqa: E402

lib = Library(root / "dataset" / "archetypes.yaml")


def first_exec(prog):
    while prog:
        step = prog[0]
        if step["op"] == "LOOP":
            prog = step["body"]
            continue
        return step["op"]
    return None


def has_timer(prog):
    for s in prog:
        if s["op"] == "TIMER":
            return True
        if s["op"] == "LOOP" and has_timer(s["body"]):
            return True
    return False


timer_tasks = 0
literal_first = Counter()
violations = []
wake_events = 0
arrive_events = 0
spawned = 0
timer_entries = Counter()
for path in sorted((root / "dataset" / "timelines").glob("**/*.timeline.yaml")):
    tl = Timeline(path, lib)
    canonical, report = compile_timeline(tl, lib, "single")
    for ev in canonical["events"]:
        if ev["op"] == "wake":
            wake_events += 1
            continue
        arrive_events += 1
        tasks = [(ev["id"], ev["name"], ev["program"], "top")]
        for s in ev.get("spawn_table", []) or []:
            spawned += 1
            tasks.append((s["id"], s["name"], s["program"], "spawn"))
        for tid, name, prog, kind in tasks:
            if not has_timer(prog):
                continue
            timer_tasks += 1
            literal_first[prog[0]["op"]] += 1
            timer_entries[name] += 1
            fe = first_exec(prog)
            if fe != "TIMER":
                violations.append((tl.id, tid, name, kind, fe, prog[0]["op"]))

print(f"timelines compiled; arrive events {arrive_events}, spawned tasks {spawned}, wake events {wake_events}")
print(f"tasks carrying TIMER: {timer_tasks}; literal first op distribution: {dict(literal_first)}")
print(f"TIMER tasks by name: {dict(timer_entries)}")
print(f"first-executed-not-TIMER: {len(violations)}")
for v in violations[:40]:
    print("  ", v)
