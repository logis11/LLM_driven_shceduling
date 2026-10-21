#!/usr/bin/env python3
"""9.7's SteamCMD phase (`game-download`, and `game-download-idle`, which shares its tables; `meas-ci:background:2026-09-19`,
phase `steam-fresh-shaped`) traced and recomputed as the 9.10 background section recomputes the Tracker index and the
Déjà Dup backup (census_bg910.py): each pooled repeat read as `meas/background/analyze.analyze_phase` reads it (the
launched root, the phase's tree by the fork rows, SteamCMD's own binary's processes, the measured CPU's rows,
`thread_wakes`), every wake of the program's threads traced by `chain_roots.RootTracer` (census_core's rules and
classes; the fork rows give the processes born in the phase), and the batch loop's two tables — the program's runs
between voluntary blocks and the block after each — recomputed with the outside-cause wakes' segments taken out of the
rows: every outside-cause wake (the rule as written) and only those whose own wakeup row names the outside waker
(direct.py's reading; the inherited put back), the time they ran left to the program's other threads or idle.

The phase holds tens of millions of rows on the harness CPUs, so only the measured CPU's timehist rows are kept
(census_background.segments_on) and only the wakeup rows to the tree, the processes born in the phase, pid 1 and the
relays (census_background.one's filter). Each repeat's zip is extracted (the phase's files only) into its own folder.

Per repeat it writes the tally (classes, labels, the direct/inherited split, the outside-cause wakes), the roots
(chain_roots.runs), the check against census_core.Tracer on the first 200,000 wakes, the tables' sums and counts per
reading, and the tables' samples per reading (`<out dir>/steamcmd-r<k>.npz`: run_<reading>, block_<reading>, in µs),
from which effect_steamcmd.py builds the pooled quantile tables the archetype carries.

  python3 -I census_steamcmd.py <steamcmd-pooled.json> <zip dir> <extract dir> --out <out.json> [--only k,k,...]
"""

import collections
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
import census_background as cbk  # noqa: E402
import census_bg910 as b910  # noqa: E402
from meas.background import analyze as bg  # noqa: E402
from meas.build import shapes  # noqa: E402
import numpy as np  # noqa: E402

PHASE = "steam-fresh-shaped"
MEMBERS = ("report.json", "report.kv", "spec.json", "edges.jsonl", f"taskstats.{PHASE}.tsv",
           f"perf.{PHASE}.timehist.txt.gz", f"perf.{PHASE}.wakeups.txt.gz", f"perf.{PHASE}.forks.txt.gz")


def extract(zip_path, dest):
    """The phase's files of one repeat's zip into dest/<its folder>; the folder."""
    z = zipfile.ZipFile(zip_path)
    folder = None
    for n in z.namelist():
        parts = n.split("/")
        if len(parts) == 2 and parts[1] in MEMBERS and ".." not in parts:
            folder = parts[0]
            out = os.path.join(dest, parts[0], parts[1])
            if not os.path.exists(out) or os.path.getsize(out) != z.getinfo(n).file_size:
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with z.open(n) as src, open(out, "wb") as dst:
                    while True:
                        b = src.read(1 << 22)
                        if not b:
                            break
                        dst.write(b)
    return os.path.join(dest, folder)


def tables(prog_rows, span):
    """analyze_phase's batch tables, in µs, as arrays: the program's runs between voluntary blocks (per thread,
    concatenated) and the block after each voluntary block (the program-level gap from where the run's thread went to
    sleep), with the CPU total."""
    prog_rows = sorted(prog_rows, key=lambda s: s.t_in)
    by_tid = collections.defaultdict(list)
    for s in prog_rows:
        by_tid[s.tid].append(s)
    runs = np.fromiter((x * 1000.0 for rs in by_tid.values() for x in shapes.runs_between_blocks(rs)), dtype=np.float64)
    blocks = np.fromiter((ms * 1000.0 for ms in shapes.blocks_after_runs(prog_rows, span[0], span[1])), dtype=np.float64)
    return runs, blocks, sum(s.run for s in prog_rows) * 1000.0


def one(D, npz_path):
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
    born = {c for _t, _p, _pc, c, _cc in forks}
    keep = {tid2pid.get(t, t) for t in tree} | born | {1}
    wakeup_rows = sorted((w for w in cc.iter_wakeup_rows(base + ".wakeups.txt.gz")
                          if w[6] in keep or w[4] in cc.RELAY_COMMS), key=lambda w: w[0])
    wakeups = {}
    for w in wakeup_rows:
        wakeups.setdefault(w[5], []).append(w[0])
    per_wakes, _iv, _m = bg.thread_wakes(rows, wakeups)
    del wakeups
    all_wakes = sorted((w for ws in per_wakes.values() for w in ws), key=lambda w: w.t_in)
    tr = cr.RootTracer(wakeup_rows, set(pids), cc.by_tid(all_wakes), born=born)
    prog_wakes = [w for w in all_wakes if tid2pid.get(w.tid, w.tid) in prog]
    traced = tr.trace(prog_wakes)
    check_n = cr.check(tr, prog_wakes[:200000])
    del tr, wakeup_rows, all_wakes     # the tracing's memory freed before the tables are rebuilt
    res = b910.tally(traced, lambda w: "steamcmd")
    prog_rows = [s for s in rows if tid2pid.get(s.tid, s.tid) in prog]
    span = (min(s.t_in for s in prog_rows), max(s.t_end for s in prog_rows))
    index = b910.wake_of_segment(per_wakes)
    vals, arrays = {}, {}
    for tag, pick in (("base", None), ("rule", lambda x: x[1] == "outside"),
                      ("direct", lambda x: x[1] == "outside" and x[6]),
                      ("how_direct", lambda x: x[1] == "outside" and x[3] == "direct")):
        gone = [x[0] for x in traced if pick(x)] if pick else []
        kept = b910.drop_segments(prog_rows, gone, index) if gone else prog_rows
        runs, blocks, cpu = tables(kept, span)
        vals[tag] = {"removed": len(gone), "removed_run_ms": sum(w.run for w in gone),
                     "removed_busy_ms": sum((w.t_end - w.t_wake) * 1000.0 for w in gone),
                     "run_sum": float(runs.sum()), "run_n": int(runs.size), "block_sum": float(blocks.sum()),
                     "block_n": int(blocks.size), "block_nonzero": int((blocks > 0).sum()), "cpu_us": cpu}
        if tag != "how_direct":
            arrays[f"run_{tag}"], arrays[f"block_{tag}"] = runs, blocks
    np.savez_compressed(npz_path, **arrays)
    return {"repeat": rep.get("repeat"), "dir": D, "values": vals, "tally": res, "roots": cr.runs(traced, top=8),
            "check_differ": check_n, "check_wakes": min(len(prog_wakes), 200000), "tree_threads": len(tree),
            "program_pids": len(prog), "program_wakes": len(prog_wakes), "span_s": span[1] - span[0]}


def main():
    pooled_path, zip_dir, ext_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    out_path = sys.argv[sys.argv.index("--out") + 1]
    only = None
    if "--only" in sys.argv:
        only = {s for s in sys.argv[sys.argv.index("--only") + 1].split(",")}
    e = json.load(open(pooled_path))["runs"]["steamcmd"]
    run_ids = {str(k): str(v) for k, v in (e.get("run_id") or {}).items()}
    result = json.load(open(out_path)) if os.path.exists(out_path) else {}
    sec = result.setdefault("game-download", {"campaign": "meas-ci:background:2026-09-19", "phase": PHASE,
                                              "job": "steamcmd", "kind": "batch", "reading": "census_core",
                                              "repeats": {}})
    for k in e["repeats"]:
        key = str(k)
        if key in sec["repeats"] or (only and key not in only):
            continue
        D = extract(os.path.join(zip_dir, f"meas-background-steamcmd-r{k}-full.zip"), ext_dir)
        spec = json.load(open(os.path.join(D, "spec.json")))
        run = str((spec.get("github_run") or {}).get("GITHUB_RUN_ID") or "")
        if run_ids.get(key) and run != run_ids[key]:
            raise SystemExit(f"r{k}: run id {run} against the pooled record's {run_ids[key]}")
        r = one(D, os.path.join(os.path.dirname(os.path.abspath(out_path)), f"steamcmd-r{k}.npz"))
        r["run_id"] = run
        result = json.load(open(out_path)) if os.path.exists(out_path) else result
        sec = result.setdefault("game-download", sec)
        sec["repeats"][key] = r
        c = r["tally"].get("steamcmd", {})
        v = r["values"]
        print(f"r{k}: {c.get('n')} wakes, outside {c.get('classes', {}).get('outside', {}).get('n', 0)} "
              f"(direct {c.get('split', {}).get('direct', {}).get('n', 0)}), check differs {r['check_differ']}; "
              f"block mean {v['base']['block_sum'] / v['base']['block_n']:.4f} -> rule "
              f"{v['rule']['block_sum'] / v['rule']['block_n']:.4f}, direct {v['direct']['block_sum'] / v['direct']['block_n']:.4f}",
              flush=True)
        json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
