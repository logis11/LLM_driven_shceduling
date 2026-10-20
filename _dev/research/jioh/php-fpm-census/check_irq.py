#!/usr/bin/env python3
"""A plausibility check on the outside-cause counts: a wakeup row names the task that was running when the wakeup
was raised, and a wakeup raised from interrupt context — a timer migrated off the idle measured CPU, a network
receive — names whichever task the interrupt found running. If the measured tree's wakes "raised" by runner
processes that share no channel with it are such interrupt-context rows, each process's count follows the CPU time it
ran on the other CPUs, and the rows per CPU-second are about the same for every one of them.

Per repeat of the desktop campaign's carried phases: for every waker outside the tree (the idle task excluded), the
tree wakeup rows it raised and its run time on the CPUs other than the measured one, then the rows per CPU-second.

  python3 -I check_irq.py <phase> <measured cpu> <repeat dir> [<repeat dir> ...]   (summed over the repeats)
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
from meas.campaign.analyze import ROW, TASK, open_text  # noqa: E402


def one(D, phase, meas, run, rows):
    pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p):
            pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
    t0 = t1 = None
    with open_text(os.path.join(D, f"perf.{phase}.timehist.txt.gz")) as h:
        for line in h:
            m = ROW.match(line)
            if not m:
                continue
            t, cpu, task, _w, _d, r, _s = m.groups()
            t0 = float(t) if t0 is None else t0
            t1 = float(t)
            tm = TASK.match(task.strip())
            if not tm or int(cpu) == meas:
                continue
            run[tm.group(1)] += float(r) / 1000.0
    for t, wc, wt, wp, kc, kt, kp in cc.load_wakeup_rows(os.path.join(D, f"perf.{phase}.wakeups.txt.gz")):
        if kp in pids and wp is not None and wp not in pids:
            rows[wc] += 1
    return t1 - t0


def main():
    phase, meas, dirs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    run, rows = collections.Counter(), collections.Counter()
    span = sum(one(D, phase, meas, run, rows) for D in dirs)
    print(f"{phase}, {len(dirs)} repeats, {span:.0f} s; wakers outside the tree: rows into the tree, CPU-s on the other CPUs")
    for c, n in rows.most_common(25):
        print(f"  {c:20s} {n:6d} rows  {run.get(c, 0):8.2f} CPU-s  {n / run[c] if run.get(c) else float('nan'):8.2f} rows/CPU-s"
              f"  [{cc.comm_class(c)[1]}]")


if __name__ == "__main__":
    main()
