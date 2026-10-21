#!/usr/bin/env python3
"""The Kdenlive export's wakes census_core keeps as `unknown` (9.10, `meas-ci:background:2026-10-03c`, phase
`kdenlive-export`): each repeat read as census_bg910.py reads it (the renderer's tree from the earliest process that
executed kdenlive_render, the measured CPU's rows, `thread_wakes`), every wake of the tree traced by
`chain_roots.RootTracer`, and the unknown ones listed with how their cause reached them, the row it was read from and
their time from the renderer's first wake; and the export's three carried values (the run between voluntary blocks,
the block per run, the CPU total; census_bg910.batch_values) recomputed with the unknown wakes' segments taken out —
all of them, and only those whose own wakeup row names the application (`how` direct) — as a reading of what classing
the application `outside` would do.

  python3 -I kdenlive_unknown.py <out.json> <repeat dir> [<repeat dir> ...]
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
import census_bg910 as b910  # noqa: E402
from meas.background import analyze as bg  # noqa: E402

PHASE = "kdenlive-export"


def one(D):
    rep = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(rep.get("pin.load_cpu", 3))
    base = os.path.join(D, f"perf.{PHASE}")
    segs, wakeups = bg.load_segments(base + ".timehist.txt.gz"), bg.load_wakeups(base + ".wakeups.txt.gz")
    forks, _exits = bg.load_forks(base + ".forks.txt.gz")
    exec_rows = bg.load_exec_rows(base + ".forks.txt.gz")
    root, tree, tid2pid, last_comm, _o = bg.phase_tree("kdenlive", segs, forks, meas_cpu,
                                                       bg.launched_root("kdenlive", exec_rows))
    pids = sorted({tid2pid.get(t, t) for t in tree})
    rows = [s for s in segs if s.cpu == meas_cpu and s.tid in tree]
    per_wakes, _iv, _m = bg.thread_wakes(rows, wakeups)
    wakes = sorted((w for ws in per_wakes.values() for w in ws), key=lambda w: w.t_in)
    born = {c for _t, _p, _pc, c, _cc in forks}
    wr = cc.load_wakeup_rows(base + ".wakeups.txt.gz")
    tr = cr.RootTracer(wr, set(pids), cc.by_tid(wakes), born=born)
    traced = tr.trace(wakes)
    t0 = wakes[0].t_in
    # the processes behind the root rows' wakers: the wakeup rows name a thread and its process
    comm_of = collections.defaultdict(set)
    for t, wc, wt, wp, *_x in wr:
        if wp is not None:
            comm_of[wp].add(wc)
    unk = [(w, lab, how, r) for w, cls, lab, how, r, _h, _d in traced if cls == "unknown"]
    total = sum(w.run for w in wakes)
    by_root = collections.defaultdict(lambda: {"wakes": 0, "run_ms": 0.0, "how": collections.Counter(),
                                               "threads": collections.Counter()})
    for w, lab, how, r in unk:
        key = f"{r[2]}[{r[3]}] -> {r[0]} at {r[1] - t0:.4f} s" if r else lab
        g = by_root[key]
        g["wakes"] += 1
        g["run_ms"] += w.run
        g["how"][how] += 1
        g["threads"][w.comm] += 1
    prog_rows = [s for s in rows if tid2pid.get(s.tid, s.tid) in set(pids)]
    span = (min(s.t_in for s in prog_rows), max(s.t_end for s in prog_rows))
    index = b910.wake_of_segment(per_wakes)
    values = {"base": b910.batch_values(prog_rows, tid2pid, span, None)}
    for tag, pick in (("unknown", lambda x: True), ("unknown_direct", lambda x: x[2] == "direct")):
        gone = [x[0] for x in unk if pick(x)]
        values[tag] = b910.batch_values(b910.drop_segments(prog_rows, gone, index), tid2pid, span, None)
        values[tag]["removed"] = len(gone)
    return {"repeat": rep.get("repeat"), "dir": D, "root_pid": root, "wakes": len(wakes), "run_ms": total,
            "values": values,
            "unknown": len(unk), "unknown_run_ms": sum(w.run for w, *_x in unk),
            "last_unknown_s": max((w.t_in - t0 for w, *_x in unk), default=None),
            "render_span_s": wakes[-1].t_end - t0,
            "largest_unknown_run": max(((w.comm, round(w.run, 3), round(w.t_in - t0, 4)) for w, *_x in unk),
                                       key=lambda x: x[1], default=None),
            "by_root": {k: {"wakes": g["wakes"], "run_ms": round(g["run_ms"], 3), "how": dict(g["how"]),
                            "threads": dict(g["threads"])} for k, g in by_root.items()},
            "root_waker_process_comms": {str(r[3]): sorted(comm_of.get(r[3], ())) for _w, _l, _h, r in unk if r}}


def main():
    out_path, dirs = sys.argv[1], sys.argv[2:]
    result = json.load(open(out_path)) if os.path.exists(out_path) else {}
    for D in dirs:
        r = one(D)
        result[str(r["repeat"])] = r
        print(f"r{r['repeat']}: {r['unknown']} unknown, {r['unknown_run_ms']:.1f} ms of {r['run_ms']:.1f}; "
              f"last at {r['last_unknown_s']:.3f} s; roots {list(r['by_root'])}", flush=True)
        json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
