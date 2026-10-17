"""Demand-window state of the current single-lane set, from the compile
reports alone (no schema validation). Read-only, in memory."""
import pathlib
import sys
import time

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "dataset" / "tools"))
from wlc import Library, Timeline, compile_timeline  # noqa: E402
from wlc.estimate import check_window  # noqa: E402

t0 = time.time()
lib = Library(root / "dataset" / "archetypes.yaml")
rows, violations = [], []
for path in sorted((root / "dataset" / "timelines").glob("**/*.timeline.yaml")):
    tl = Timeline(path, lib)
    _, report = compile_timeline(tl, lib, "single")
    rows.append((tl.id, report["utilization"], report["demand_class"]))
    v = check_window(report, "single")
    if v:
        violations.append((tl.id, report["utilization"], report["demand_class"]))
print(f"compiled {len(rows)} single-lane files in {time.time()-t0:.0f} s")
print(f"window violations: {len(violations)}")
for wid, u, c in violations:
    print(f"  {wid:14s} demand {u:.2f} ({c})")
print("demand classes:", {c: sum(1 for r in rows if r[2] == c) for c in sorted({r[2] for r in rows})})
