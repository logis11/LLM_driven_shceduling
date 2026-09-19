#!/usr/bin/env python3
"""The steady phase's slice profile (9.5 changelog D34, D35): the process tree's CPU (ms per second) and wakes per
second in consecutive slices of the idle phase (the play phase for the playback runs), from the phase's start.

slices.py <run-dir>... [--phase idle|play] [--s 10] [--exclude-roles renderer]

Each <run-dir> is one run's artifact folder (run.sh output), a campaign repeat or a long-phase probe. Slices start at
the phase's first timehist row over all tasks (perf record's start, about 1 s before any driver). A segment's run
counts in the slice of its schedule-in; a wake is a segment the wake rule keeps (analyze.merge_resumes). One line per
run, then the mean over the runs. Used to show launch work in a phase (`campaign/launch-work.md`), to read a long-phase
probe (D35, D42) and, in the loop's validity step, the steady phase of every new repeat where a settle applies.
"""

import argparse
import os
import statistics
import sys

try:   # imported as meas.campaign.slices: the sibling module, never another `analyze` already loaded
    from .analyze import analyze_run
except ImportError:   # run as a script
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from analyze import analyze_run  # noqa: E402


def profile(run_dir, phase=None, slice_s=10.0, exclude_roles=()):
    """(phase, [CPU ms/s per slice], [wakes/s per slice]); the phase is idle, else play, unless named."""
    _, raw = analyze_run(run_dir, exclude_roles=exclude_roles)
    phases = raw["phases"]
    phase = phase or ("idle" if "idle" in phases else "play")
    p = phases[phase]
    n = max(1, int(p["span"] // slice_s))
    cpu, wakes = [0.0] * n, [0] * n
    for r in p["segments"]:
        i = int((r.t_in - p["t0"]) // slice_s)
        if 0 <= i < n:
            cpu[i] += r.run
    for r in p["rows"]:
        i = int((r.t_in - p["t0"]) // slice_s)
        if 0 <= i < n:
            wakes[i] += 1
    return phase, [round(c / slice_s, 1) for c in cpu], [round(w / slice_s, 1) for w in wakes]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--phase", default=None)
    ap.add_argument("--s", type=float, default=10.0, help="slice length in seconds")
    ap.add_argument("--exclude-roles", default="", help="process roles left out of the tree (D14: renderer for chrome)")
    args = ap.parse_args()
    roles = tuple(x for x in args.exclude_roles.split(",") if x)
    cpus, wakes = [], []
    for d in args.runs:
        phase, c, w = profile(d, args.phase, args.s, roles)
        cpus.append(c); wakes.append(w)
        print(f"{os.path.basename(os.path.normpath(d))} {phase}, CPU ms/s per {args.s:g} s slice: {' '.join(f'{x:g}' for x in c)}")
        print(f"{' ' * len(os.path.basename(os.path.normpath(d)))} {phase}, wakes/s: {' '.join(f'{x:g}' for x in w)}")
    if len(cpus) > 1:
        n = min(len(c) for c in cpus)
        print(f"mean over {len(cpus)} runs, CPU ms/s: {' '.join(f'{statistics.fmean(c[i] for c in cpus):.1f}' for i in range(n))}")
        print(f"mean over {len(cpus)} runs, wakes/s: {' '.join(f'{statistics.fmean(w[i] for w in wakes):.1f}' for i in range(n))}")


if __name__ == "__main__":
    main()
