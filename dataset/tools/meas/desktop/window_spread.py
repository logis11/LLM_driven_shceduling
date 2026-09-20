#!/usr/bin/env python3
"""Size a steady phase from a long-phase probe (changelog D15; method §3, §9).

For each candidate phase length L, the probe's steady phase is cut into non-overlapping windows of L and each
window's mean taken — the quantity one repeat would contribute. The spread across those windows is the part of
the across-repeat variance the phase length itself controls; it is a lower bound on that variance, since a real
repeat also redraws the runner. `hw@5rep` is the 95 % t half-width a five-repeat batch of such windows would
show (t = 2.776 at 4 degrees of freedom), in percent of the mean, against the 5 % tolerance of the stability
rule. A figure taken over fewer than three windows is a weak estimate of a standard deviation and is reported
with its window count for that reason.

This is what set the 2026-09-20 phase lengths: 600 s everywhere, a 900 s launch-settle for the Steam client
whose shown phase steps down at 900 s, and a 630 s grace-settle for the hidden renderer, which was still
settling for the first 300 s of what the probe recorded as steady.

  window_spread.py <analysis.json> <phase> [drop-seconds]

<analysis.json> is `desktop/analyze.py --json` output; [drop-seconds] cuts that many seconds off the front of
the phase first, which is how a settle is sized.
"""
import json
import statistics
import sys

T95_4DF = 2.776        # 95 % two-sided t, 4 degrees of freedom: a five-repeat batch


def windows(vals, slice_s, length_s):
    k = int(length_s // slice_s)
    if not k or len(vals) < k:
        return []
    return [statistics.mean(vals[i:i + k]) for i in range(0, len(vals) - k + 1, k)]


def spread(vals, slice_s, length_s, repeats=5):
    w = windows(vals, slice_s, length_s)
    if len(w) < 2:
        return None
    mean, sd = statistics.mean(w), statistics.stdev(w)
    if not mean:
        return None
    return {"windows": len(w), "mean": mean, "sd_pct": sd / mean * 100,
            "half_width_pct": T95_4DF * sd / (repeats ** 0.5) / mean * 100}


def report(path, phase, drop_s=0, lengths=(120, 300, 375, 500, 600, 900)):
    ph = json.load(open(path))["phases"][phase]
    sl = ph["slices"]["slice_s"]
    vals = ph["slices"]["wakes_per_s"][int(drop_s // sl):]
    head = f"{phase}" + (f", first {drop_s}s dropped" if drop_s else "")
    per = ph.get("wakes_per_s_per_renderer")
    print(f"{head}: {ph['wakes_per_s']:.3f} wakes/s over {ph['span_s']:.0f}s"
          + (f", {per:.4f} per renderer, N={ph.get('renderers_measured')}" if per else ""))
    print(f"  {'length':>8}  {'windows':>7}  {'mean':>9}  {'sd':>6}  {'hw@5rep':>8}")
    for L in lengths:
        r = spread(vals, sl, L)
        if r:
            print(f"  {L:>7}s  {r['windows']:>7}  {r['mean']:>9.3f}  {r['sd_pct']:>5.1f}%  {r['half_width_pct']:>7.1f}%")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    report(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 0)
