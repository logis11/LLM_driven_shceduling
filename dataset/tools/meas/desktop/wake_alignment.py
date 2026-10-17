#!/usr/bin/env python3
"""Do the throttled renderers' wakes coincide across processes (changelog D15; method §9)?

Method §9 leaves this open before the first batch: alignment is documented within a page, and the budget pool
allows a lower alignment when there has been no recent wake, but whether the grids coincide *across* renderer
processes — so that N renderers wake together rather than independently — is not established by the sources
read, and it bears on both pooling and what the scheduler sees.

The measured renderers' wake times are binned, and the bins are counted by how many distinct renderers woke in
each. The same count is taken over draws that keep every renderer's own wake count and place its wakes
uniformly over the phase, which is what independence looks like. Clustering shows as bins holding many
renderers where the independent draws hold none.

On the 2026-09-20 probe this was decisive: every one of the twelve renderers woke together in 243 bins of 1 s
and 32 bins of 10 ms, against none at either width under independence.

  wake_alignment.py <run-dir> <phase> <analysis.json> [bin-seconds]
"""
import json
import os
import random
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import load_rows        # noqa: E402

DRAWS = 20


def measured_pids(res_phase):
    """The renderers the entry is pooled from: the browser's own renderers and the control tab are not it."""
    pids = set(res_phase["renderer_pids"]) - set(res_phase.get("renderers_not_page") or [])
    pids.discard((res_phase.get("control_tab") or {}).get("dropped"))
    return pids


def occupancy(by_pid, bin_s, n_bins):
    seen = {}
    for pid, times in by_pid.items():
        for t in times:
            seen.setdefault(int(t // bin_s), set()).add(pid)
    hist = {}
    for bucket in seen.values():
        hist[len(bucket)] = hist.get(len(bucket), 0) + 1
    return hist


def main(run_dir, phase, analysis, bin_s=1.0, seed=9):
    res = json.load(open(analysis))["phases"][phase]
    th = next(f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
              if os.path.exists(os.path.join(run_dir, f"perf.{phase}.timehist.txt{s}")))
    pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        pids |= {p["pid"] for p in json.load(open(os.path.join(run_dir, snap)))["procs"]}
    segments, (t0, t1), _ = load_rows(os.path.join(run_dir, th), pids)
    span = t1 - t0
    keep = measured_pids(res)
    by_pid = {}
    for r in segments:
        if r.pid in keep:
            by_pid.setdefault(r.pid, []).append(r.t_in - t0)

    n_bins = int(span // bin_s) + 1
    observed = occupancy(by_pid, bin_s, n_bins)
    random.seed(seed)
    independent = {}
    for _ in range(DRAWS):
        drawn = {pid: [random.random() * span for _ in ts] for pid, ts in by_pid.items()}
        for k, v in occupancy(drawn, bin_s, n_bins).items():
            independent[k] = independent.get(k, 0) + v / DRAWS

    print(f"{len(keep)} renderers, {sum(len(v) for v in by_pid.values())} wakes, "
          f"{span:.0f}s, {bin_s}s bins")
    print(f"  {'renderers per bin':>18}  {'observed':>9}  {'independent':>12}")
    for k in sorted(set(observed) | set(independent)):
        print(f"  {k:>18}  {observed.get(k, 0):>9}  {independent.get(k, 0):>12.1f}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 1.0)
