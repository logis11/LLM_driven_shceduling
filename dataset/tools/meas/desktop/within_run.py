#!/usr/bin/env python3
"""Does a component's rate vary within one run, or between runs (changelog D20; 9.5 D57)?

9.5 D57 carries a component whose rate varies between sessions rather than within a run with its half-widths,
and places the spread by sliding a window along one long run: if the rate barely moves inside a run while it moves
a lot across repeats, the spread is the application's between sessions, not the phase's placement. This does the
same for a renderer entry: over the long-phase probe's steady phase, a window of the campaign's phase length slides
in steps, and each position's rate is taken per renderer — the comms named merged within each renderer, the
renderers averaged — as the pool computes one renderer's residual (D19).

  within_run.py <probe-run-dir> <phase> <analysis.json> <window-s> <step-s> <comm>[,<comm>...]
  within_run.py --tree <probe-run-dir> <phase> <window-s> <step-s> <skip-s> <comm>[,<comm>...]

--tree does the same for a subject that is one process tree (the Steam client), reporting at each position the
comms' wake rate and their gap mean.
"""
import json
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import load_rows       # noqa: E402
from meas.desktop.wake_alignment import measured_pids  # noqa: E402


def rates(run_dir, phase, analysis, window_s, step_s, comms):
    res = json.load(open(analysis))["phases"][phase]
    th = next(f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
              if os.path.exists(os.path.join(run_dir, f"perf.{phase}.timehist.txt{s}")))
    pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        pids |= {p["pid"] for p in json.load(open(os.path.join(run_dir, snap)))["procs"]}
    segments, (t0, t1), _ = load_rows(os.path.join(run_dir, th), pids)
    keep = measured_pids(res)
    times = [r.t_in - t0 for r in segments if r.pid in keep and r.comm in comms]
    out, start = [], 0.0
    while start + window_s <= (t1 - t0) + 1e-6:
        n = sum(1 for t in times if start <= t < start + window_s)
        out.append(n / window_s / len(keep))
        start += step_s
    return out


def tree_windows(run_dir, phase, window_s, step_s, comms, skip_s=0.0):
    """For a subject that is one process tree (the Steam client, the chat client): at each window position, the
    comms' wake rate and their gap mean — gaps taken within each thread, as the pool's per-thread gap is."""
    th = next(f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
              if os.path.exists(os.path.join(run_dir, f"perf.{phase}.timehist.txt{s}")))
    pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        pids |= {p["pid"] for p in json.load(open(os.path.join(run_dir, snap)))["procs"]}
    segments, (t0, t1), _ = load_rows(os.path.join(run_dir, th), pids)
    rows = sorted(((r.tid, r.t_in - t0) for r in segments if r.comm in comms), key=lambda x: x[1])
    out, start = [], skip_s
    while start + window_s <= (t1 - t0) + 1e-6:
        by_tid = {}
        for tid, t in rows:
            if start <= t < start + window_s:
                by_tid.setdefault(tid, []).append(t)
        gaps = [(b - a) * 1000 for ts in by_tid.values() for a, b in zip(ts, ts[1:])]
        out.append((sum(len(ts) for ts in by_tid.values()) / window_s, sum(gaps) / len(gaps) if gaps else None))
        start += step_s
    return out


def spread(v):
    m = sum(v) / len(v)
    return f"{min(v):.4f}–{max(v):.4f} (mean {m:.4f}, ±{(max(v) - min(v)) / 2 / m * 100:.1f}% of the mean)"


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "--tree":
        # within_run.py --tree <run-dir> <phase> <window-s> <step-s> <skip-s> <comm>[,<comm>...]
        d, ph, w, st, sk, cs = sys.argv[2:8]
        v = tree_windows(d, ph, float(w), float(st), set(cs.split(",")), float(sk))
        print(f"{cs}: {len(v)} positions of {w}s from {sk}s — wake rate {spread([a for a, _ in v])}; "
              f"gap mean (ms) {spread([g for _, g in v if g])}")
        raise SystemExit(0)
    if len(sys.argv) < 7:
        raise SystemExit(__doc__)
    d, ph, an, w, st, cs = sys.argv[1:7]
    v = rates(d, ph, an, float(w), float(st), set(cs.split(",")))
    print(f"{cs}: {len(v)} positions of {w}s, per-renderer rate {spread(v)}")
