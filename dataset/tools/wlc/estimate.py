"""Static demand record (task-2.3 spec §7; 9.14 decision 4).

The estimate itself is computed exactly during synthesis (compiler.py
accumulates each task's CPU demand in context). This module turns it into the
manifest's demand record: the file's utilization over its whole length and,
per ground-truth segment, the utilization inside the segment, each task's
demand spread uniformly over its lifetime (its arrival to its pinned depart or
the file's end).

The demand window of the earlier policy — a single-lane file of demand class
`oversubscribed` had to land in [1.00, 1.50] — retired as a gate on 2026-10-09
(9.14 decision 4): every file's demand is a measured fact the manifest reports
and the pair review reads per contended segment; no build fails on it.
"""


def per_segment(builds, segments, duration_us):
    """One record per ground-truth segment: its bounds and the utilization
    inside it, each build's demand spread uniformly over its lifetime."""
    out = []
    for i, seg in enumerate(segments):
        s0, s1 = int(seg["t_start"]), int(seg["t_end"])
        total = 0.0
        for b in builds:
            a = int(b.arrive)
            d = int(b.depart) if b.depart is not None else int(duration_us)
            life = d - a
            if life <= 0:
                continue
            overlap = max(0, min(d, s1) - max(a, s0))
            if overlap:
                total += b.demand_us * overlap / life
        out.append({"index": i, "t_start_us": s0, "t_end_us": s1,
                    "utilization": total / (s1 - s0)})
    return out
