#!/usr/bin/env python3
"""The SteamCMD blocks the removal lengthens most: one repeat read as census_steamcmd.py reads it, the program's
segments with the outside-cause wakes census_steamcmd.py recorded (`gone`) taken out, and every block of the rebuilt
table longer than the base table's longest listed with its place in the phase, the removed wakes inside it (their
threads, runs, causes and root rows) and the base table's blocks over the same span.

  python3 -I steamcmd_blocks.py <steamcmd.json> <repeat> <extract dir> [--direct]
"""

import bisect
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import census_background as cbk  # noqa: E402
import census_bg910 as b910  # noqa: E402
from meas.background import analyze as bg  # noqa: E402
from meas.build import shapes  # noqa: E402

PHASE = "steam-fresh-shaped"


def blocks_with_place(rows, span):
    """(t_end of the voluntary block's run, block ms) for each voluntary block, as shapes.blocks_after_runs reads them."""
    rows = sorted(rows, key=lambda s: s.t_in)
    vol = [s for s in rows if s.state[:1] in shapes.VOLUNTARY]
    return list(zip((s.t_end for s in vol), shapes.blocks_after_runs(rows, span[0], span[1]), (s for s in vol)))


def main():
    data, k, ext = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    direct = "--direct" in sys.argv
    r = data["game-download"]["repeats"][k]
    D = r["dir"]
    rep = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(rep.get("pin.load_cpu", 3))
    base = os.path.join(D, f"perf.{PHASE}")
    fk = base + ".forks.txt.gz"
    segs = cbk.segments_on(base + ".timehist.txt.gz", meas_cpu)
    forks, _ = bg.load_forks(fk)
    exec_rows = bg.load_exec_rows(fk)
    execs = {pid: f for _t, pid, f in exec_rows}
    recs = bg.process_records(bg.load_taskstats(os.path.join(D, f"taskstats.{PHASE}.tsv"))[0])
    root, tree, tid2pid, last_comm, _o = bg.phase_tree("steamcmd", segs, forks, meas_cpu,
                                                       bg.launched_root("steamcmd", exec_rows))
    pids = sorted({tid2pid.get(t, t) for t in tree})
    role = {pid: (recs[pid]["comm"] if pid in recs else last_comm.get(pid, "?")) for pid in pids}
    prog = {p for p in pids if bg.is_program("steamcmd", execs.get(p), role.get(p))}
    rows = [s for s in segs if s.cpu == meas_cpu and s.tid in tree]
    del segs
    tids = set(tree)
    wakeups = collections.defaultdict(list)
    for w in cc.iter_wakeup_rows(base + ".wakeups.txt.gz"):
        if w[5] in tids:
            wakeups[w[5]].append(w[0])
    for v in wakeups.values():
        v.sort()
    per_wakes, _iv, _m = bg.thread_wakes(rows, wakeups)
    prog_rows = sorted((s for s in rows if tid2pid.get(s.tid, s.tid) in prog), key=lambda s: s.t_in)
    span = (prog_rows[0].t_in, max(s.t_end for s in prog_rows))
    gone_rec = [g for g in r["tally"]["steamcmd"]["gone"] if g[4] == "outside" and (g[7] or not direct)]
    key = {(g[2], round(g[0], 6)) for g in gone_rec}
    gone = [w for ws in per_wakes.values() for w in ws if (w.tid, round(w.t_in, 6)) in key]
    kept = b910.drop_segments(prog_rows, gone, b910.wake_of_segment(per_wakes))
    b0 = blocks_with_place(prog_rows, span)
    b1 = blocks_with_place(kept, span)
    longest = max(ms for _t, ms, _s in b0)
    t0 = span[0]
    print(f"repeat {k}: {len(gone)} wakes removed ({'direct' if direct else 'rule as written'}); base longest block "
          f"{longest * 1000:.0f} µs; phase {span[1] - span[0]:.1f} s")
    gone_t = sorted(gone_rec, key=lambda g: g[0])
    gt = [g[0] for g in gone_t]
    for t, ms, s in b1:
        if ms <= longest:
            continue
        a, b = bisect.bisect_left(gt, t - 1e-6), bisect.bisect_right(gt, t + ms / 1000 + 1e-6)
        inside = gone_t[a:b]
        base_in = [(round(t2 - t0, 4), round(ms2 * 1000)) for t2, ms2, _s in b0 if t - 1e-6 <= t2 <= t + ms / 1000 and ms2 > 0]
        busy_base = sum(x.run for x in prog_rows if t <= x.t_in <= t + ms / 1000)
        print(f"  block of {ms * 1000:.0f} µs from {t - t0:.4f} s after the program's first row, after {s.comm}[{s.tid}] "
              f"went to sleep ({s.state}); {len(inside)} removed wakes inside, {sum(g[3] for g in inside):.3f} ms of run; "
              f"base program run inside {busy_base:.3f} ms; base blocks inside {base_in[:12]}")
        for g in inside[:12]:
            print(f"     {g[0] - t0:.6f} {g[1]}[{g[2]}] run {g[3]} ms — {g[5]} via {g[6]}, direct {g[7]}, root {g[8]}")
        roots = collections.Counter(g[8] for g in inside)
        print(f"     roots: {dict(roots.most_common(5))}; threads: {dict(collections.Counter(g[1] for g in inside))}")


if __name__ == "__main__":
    main()
