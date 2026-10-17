"""Compiled single-lane coreset: total canonical bytes, the five largest files,
and per-file wake-event counts for the five largest. Read-only, in memory."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "dataset" / "tools"))
from wlc import Library, Timeline, compile_timeline  # noqa: E402
from wlc.compiler import canonical_bytes  # noqa: E402

lib = Library(root / "dataset" / "archetypes.yaml")
rows = []
for path in sorted((root / "dataset" / "timelines").glob("**/*.timeline.yaml")):
    tl = Timeline(path, lib)
    canonical, _ = compile_timeline(tl, lib, "single")
    wakes = sum(1 for e in canonical["events"] if e["op"] == "wake")
    rows.append((len(canonical_bytes(canonical)), wakes, tl.id))
total = sum(r[0] for r in rows)
print(f"files {len(rows)}; total single-lane bytes {total:,} ({total/1e6:.1f} MB); wakes {sum(r[1] for r in rows):,}")
for size, wakes, wid in sorted(rows, reverse=True)[:8]:
    print(f"  {wid:14s} {size/1e6:7.1f} MB  wakes {wakes:,}")
