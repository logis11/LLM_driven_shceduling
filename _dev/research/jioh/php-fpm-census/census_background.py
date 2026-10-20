#!/usr/bin/env python3
"""9.7's background campaign (`meas-ci:background:2026-09-19`): `file-archiver` (7-Zip, phase `7z-mmt8-warm`) and
`game-download` / `game-download-idle` (SteamCMD, phase `steam-fresh-shaped`). Each pooled repeat's tree, program
processes and wakes as `meas/background/analyze.py` reads them (`phase_tree` from the launched root, `is_program`,
the measured CPU's rows, `thread_wakes`); every wake of the program's threads traced by census_core. The carried
tables are the program's runs between voluntary blocks and the block after each (CPU sums and off-CPU spans), so the
effect is read from the outside-cause wakes' count against the runs and from the run they carry.

  python3 -I census_background.py <job> <repeat dir> [<repeat dir> ...] --out <out.json>
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
from meas.background import analyze as bg  # noqa: E402
from meas.build import shapes  # noqa: E402
from meas.build import analyze as ba  # noqa: E402

PHASE = {"7z": "7z-mmt8-warm", "steamcmd": "steam-fresh-shaped"}
ENTRY = {"7z": "file-archiver", "steamcmd": "game-download"}


def segments_on(path, cpu):
    """`meas/build/analyze.load_segments` restricted to the measured CPU's rows (the program is pinned there; the
    other CPUs' rows are never part of its tree's wakes, and a SteamCMD phase holds tens of millions of them)."""
    segs = []
    with ba.open_text(path) as handle:
        for line in handle:
            m = ba.ROW.match(line)
            if not m or int(m.group(2)) != cpu:
                continue
            t, c, task, _wait, delay, run, state = m.groups()
            tm = ba.TASK.match(task.strip())
            if not tm:
                continue
            comm, a, b = tm.group(1), int(tm.group(2)), tm.group(3)
            tid, pid = (a, int(b)) if b else (a, a)
            t, delay, run = float(t), float(delay), float(run)
            segs.append(ba.Seg(t - run / 1000.0, t - run / 1000.0 - delay / 1000.0, t, run, comm, tid, pid, state or "",
                               int(c)))
    segs.sort(key=lambda s: s.t_in)
    return segs


def one(job, D):
    phase = PHASE[job]
    rep = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(rep.get("pin.load_cpu", 3))
    base = os.path.join(D, f"perf.{phase}")
    fk = base + ".forks.txt.gz"
    segs = segments_on(base + ".timehist.txt.gz", meas_cpu)
    forks, _ = bg.load_forks(fk)
    exec_rows = bg.load_exec_rows(fk)
    execs = {pid: f for _t, pid, f in exec_rows}
    recs = bg.process_records(bg.load_taskstats(os.path.join(D, f"taskstats.{phase}.tsv"))[0])
    root, tree, tid2pid, last_comm, _o = bg.phase_tree(job, segs, forks, meas_cpu, bg.launched_root(job, exec_rows))
    pids = sorted({tid2pid.get(t, t) for t in tree})
    role = {pid: (recs[pid]["comm"] if pid in recs else last_comm.get(pid, "?")) for pid in pids}
    prog = {p for p in pids if bg.is_program(job, execs.get(p), role.get(p))}
    rows = [s for s in segs if s.cpu == meas_cpu and s.tid in tree]
    del segs
    born = {c for _t, _p, _pc, c, _cc in forks}
    keep = {tid2pid.get(t, t) for t in tree} | born | {1}
    wakeup_rows = sorted((w for w in cc.iter_wakeup_rows(base + ".wakeups.txt.gz")
                          if w[6] in keep or w[4] in cc.RELAY_COMMS), key=lambda w: w[0])
    wakeups = {}
    for w in wakeup_rows:     # bg.load_wakeups over the rows kept: every tree thread's wakeup times
        wakeups.setdefault(w[5], []).append(w[0])
    per_wakes, _iv, _m = bg.thread_wakes(rows, wakeups)
    wakes = sorted((w for ws in per_wakes.values() for w in ws), key=lambda w: w.t_in)
    tr = cc.Tracer(wakeup_rows, set(pids), cc.by_tid(wakes), born=born)
    prog_rows = [s for s in rows if tid2pid.get(s.tid, s.tid) in prog]
    n_runs = sum(len(shapes.runs_between_blocks([s for s in prog_rows if s.tid == t])) for t in {s.tid for s in prog_rows})
    t = {}
    for w, cls, lab in tr.classify([w for w in wakes if tid2pid.get(w.tid, w.tid) in prog]):
        c = t.setdefault(job, {"n": 0, "run": 0.0, "span": 1.0, "batch_runs": n_runs, "classes": {}, "labels": {},
                               "gone": []})
        c["n"] += 1
        c["run"] += w.run
        x = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
        x["n"] += 1
        x["run"] += w.run
        if cls != "own":
            c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
        if cls in ("outside", "harness-python"):
            c["gone"].append([round(w.t_in, 6), w.comm, w.tid, round(w.run, 3), cls, lab, w.state])
    return int(rep.get("repeat")), t


def main():
    job = sys.argv[1]
    i = sys.argv.index("--out")
    dirs, out_path = sys.argv[2:i], sys.argv[i + 1]
    result = json.load(open(out_path)) if os.path.exists(out_path) else {}
    sec = result.setdefault(ENTRY[job], {"campaign": "meas-ci:background:2026-09-19", "phase": PHASE[job], "repeats": {}})
    for D in dirs:
        k, t = one(job, D)
        sec["repeats"][str(k)] = t
        c = t.get(job, {})
        print(f"{ENTRY[job]} r{k}: {c.get('n')} wakes, outside {c.get('classes', {}).get('outside', {}).get('n', 0)}",
              flush=True)
        json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
