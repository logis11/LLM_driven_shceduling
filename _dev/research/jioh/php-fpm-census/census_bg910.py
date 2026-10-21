#!/usr/bin/env python3
"""9.10's background campaigns: the unattended upgrade (`package-upgrade`, `meas-ci:background:2026-10-01`), the DKMS
module build (`module-build-orchestrator`, `module-compiler-child`, 2026-10-02), the Tracker index (`file-indexer`,
2026-10-02b), the MNIST training run (`cpu-batch`'s `python3`, 2026-10-03), the HandBrakeCLI transcode
(`video-transcoder`, 2026-10-03b), the Kdenlive export (`cpu-batch`'s `kdenlive_render`, 2026-10-03c) and the Déjà Dup
incremental backup (`incremental-backup`, 2026-10-04). Each pooled repeat is read as
`meas/background/analyze.analyze_phase` reads it for its job — the launched root, the phase's tree by the fork rows,
the program's processes, the measured CPU's rows, `thread_wakes`; the Tracker job's window; the Déjà Dup job's end at
deja-dup's exit; the DKMS build's hook run and `modbuild`'s readings — and every wake of the program's threads is
traced by `chain_roots.RootTracer` (census_core's rules and classes; the fork rows give the processes born in the
phase).

The carried values are CPU sums and the batch loop's two tables (the program's runs between voluntary blocks, the
block after each), or for the DKMS build the spawn form's tables (each job kind's CPU per member and structural step,
make's dispatch run, the serial tail's runs and blocks, the carried CPU total). Besides the census tally, each repeat's
values are recomputed with the outside-cause wakes' segments taken out of the rows the values are read from — every
outside-cause wake (the rule as written), and only those whose own wakeup row names the outside waker (the inherited
ones put back) — the time they ran left to the program's other threads or idle.

  python3 -I census_bg910.py <job> <pooled.json> <extracted release dir> --out <out.json> [--session-by-package] [--warm]

--session-by-package: a second reading for a job run under a session bus of its own (the Tracker index and the Déjà
Dup backup: the harness's `dbus-run-session` in the chroot, each campaign's method §1 and §3). census_core names a
process born in the phase after its long-lived ancestor, and the session's services — gvfs's daemons and volume
monitors, GNOME Online Accounts' daemons, the desktop portals, dconf, the keyring, Déjà Dup's monitor — descend from
the harness's shell, so the rule classes them `outside` (the harness). With the option a process whose own executable
(or, without an exec row of its own, its nearest creator's) is one of SESSION_EXECS is classed by that executable's
package, each looked up in the desktop manifest (all `desktop`); every other rule as before.

<job>: upgrade | dkms | tracker | mnist | handbrake | kdenlive | dejadup. The repeats are the pooled record's, each
matched to its folder by index and, where an index landed more than once, by run id. The output is written after each
repeat and a repeat already in it is skipped.

--warm: every wake of the phase's tree traced first, in time order, before the program's. census_core's tracing
memoizes each wake's cause, and a chain cut at its depth limit (25 hops) is memoized as `unknown: chain too deep` at
every wake along it; traced in time order, each wake finds the wakes before it already resolved. The rules are
unchanged; only the order in which wakes are first traced.
"""

import bisect
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
from meas.background import analyze as bg  # noqa: E402
from meas.background import modbuild  # noqa: E402
from meas.build import shapes  # noqa: E402

PHASE = {"upgrade": "upgrade-install", "dkms": "dkms-install", "tracker": "tracker-index", "mnist": "mnist-train",
         "handbrake": "handbrake-transcode", "kdenlive": "kdenlive-export", "dejadup": "dejadup-incremental"}
ENTRY = {"upgrade": "package-upgrade", "dkms": "module-build-orchestrator + module-compiler-child",
         "tracker": "file-indexer", "mnist": "cpu-batch (python3)", "handbrake": "video-transcoder",
         "kdenlive": "cpu-batch (kdenlive_render)", "dejadup": "incremental-backup"}
TAG = {"upgrade": "meas-ci:background:2026-10-01", "dkms": "meas-ci:background:2026-10-02",
       "tracker": "meas-ci:background:2026-10-02b", "mnist": "meas-ci:background:2026-10-03",
       "handbrake": "meas-ci:background:2026-10-03b", "kdenlive": "meas-ci:background:2026-10-03c",
       "dejadup": "meas-ci:background:2026-10-04"}
# --session-by-package: executable -> package, each package held by the Ubuntu 24.04.5.1 desktop manifest (SHA-256
# 6c200933…f8ff); the executables' packages by name, the packages' file lists not read
SESSION_EXECS = {"dbus-daemon": "dbus-daemon", "gvfsd": "gvfs-daemons", "gvfsd-fuse": "gvfs-fuse",
                 "gvfs-udisks2-volume-monitor": "gvfs-daemons", "gvfs-mtp-volume-monitor": "gvfs-backends",
                 "gvfs-gphoto2-volume-monitor": "gvfs-backends", "gvfs-goa-volume-monitor": "gvfs-backends",
                 "gvfs-afc-volume-monitor": "gvfs-backends", "goa-daemon": "gnome-online-accounts",
                 "goa-identity-service": "gnome-online-accounts", "fusermount3": "fuse3", "gsettings": "libglib2.0-bin",
                 "gvfsd-metadata": "gvfs-daemons", "xdg-desktop-portal": "xdg-desktop-portal",
                 "xdg-document-portal": "xdg-desktop-portal", "xdg-permission-store": "xdg-desktop-portal",
                 "xdg-desktop-portal-gtk": "xdg-desktop-portal-gtk", "dconf-service": "dconf-service",
                 "gnome-keyring-daemon": "gnome-keyring", "deja-dup-monitor": "deja-dup", "gpg-agent": "gpg-agent"}


class SessionTracer(cr.RootTracer):
    """RootTracer with the job's session services classed by their own executable's package (--session-by-package)."""

    def __init__(self, *a, execs=None, **k):
        super().__init__(*a, **k)
        self.execs = execs or {}

    def process(self, pid, comm):
        p, hops = pid, 0
        while self.execs.get(p) is None and p in self.parent and hops < 40:
            p, hops = self.parent[p], hops + 1
        ex = self.execs.get(p)
        if ex in SESSION_EXECS:
            return "desktop", f"{SESSION_EXECS[ex]} ({ex}, the job's session)"
        return super().process(pid, comm)


DIRNAME = re.compile(r"^meas-background-([a-z0-9-]+)-r(\d+)-full(?:-(\d+))?$")


def find_dirs(root, job, pooled):
    """{pooled repeat key: folder}: every folder holding a report.json whose own name or whose parent's is the job's
    `-full` folder; matched by index, and by run id for an index the pooled record keys `<index>@<run id>` or lists
    with a run id among several landings."""
    e = list(pooled["runs"].values())[0]
    want = {str(k): str((e.get("run_id") or {}).get(str(k)) or "") for k in e["repeats"]}
    found = collections.defaultdict(list)
    for rp in glob.glob(os.path.join(root, "**", "report.json"), recursive=True):
        d = os.path.dirname(rp)
        m = DIRNAME.match(os.path.basename(d)) or DIRNAME.match(os.path.basename(os.path.dirname(d)))
        if not m or m.group(1) != job:
            continue
        spec = json.load(open(os.path.join(d, "spec.json"))) if os.path.exists(os.path.join(d, "spec.json")) else {}
        run = str((spec.get("github_run") or {}).get("GITHUB_RUN_ID") or m.group(3) or "")
        found[int(m.group(2))].append((run, d))
    out = {}
    for key, run in want.items():
        k = int(key.split("@")[0])
        cands = found.get(k, [])
        if "@" in key:
            run = key.split("@")[1]
        if len(cands) > 1 or "@" in key:
            cands = [c for c in cands if c[0] == run]
        if len(cands) != 1:
            raise SystemExit(f"{job} {key}: {len(cands)} folders match (run {run})")
        out[key] = cands[0][1]
    return out


def wake_of_segment(per_wakes):
    """tid -> (sorted wake starts, wakes): a segment belongs to the wake whose start is the last at or before it."""
    return {tid: ([w.t_in for w in ws], ws) for tid, ws in per_wakes.items()}


def drop_segments(segs, gone_wakes, index):
    """The segments less those of the given wakes (every segment a wake merged)."""
    gone = {(w.tid, w.t_in) for w in gone_wakes}
    if not gone:
        return segs
    tids = {t for t, _ in gone}
    out = []
    for s in segs:
        if s.tid in tids:
            starts, ws = index[s.tid]
            i = bisect.bisect_right(starts, s.t_in + 1e-9) - 1
            if i >= 0 and (s.tid, ws[i].t_in) in gone and s.t_in <= ws[i].t_end + 1e-9:
                continue
        out.append(s)
    return out


def batch_values(prog_rows, tid2pid, b_span, trk):
    """The batch loop's two tables and the CPU total, as analyze_phase computes them: (Σ run, n runs, Σ block,
    n blocks, CPU µs), all in µs."""
    prog_rows = sorted(prog_rows, key=lambda s: s.t_in)
    by_tid = collections.defaultdict(list)
    for s in prog_rows:
        by_tid[s.tid].append(s)
    runs = [x * 1000.0 for rs in by_tid.values() for x in shapes.runs_between_blocks(rs)]
    blocks = []
    if prog_rows:
        b_start, b_end = b_span
        vol = [s for s in prog_rows if s.state[:1] in shapes.VOLUNTARY]
        init_abs = (trk["start"] + trk["initializing_s"]) if trk and trk.get("initializing_s") is not None else None
        for s, ms in zip(vol, shapes.blocks_after_runs(prog_rows, b_start, b_end)):
            if init_abs is not None and s.t_end < init_abs <= s.t_end + ms / 1000.0 + 0.1 and ms >= 1000.0:
                continue      # 9.10 D71: the Tracker job's initial sleep is the task's arrival, not a block
            blocks.append(ms * 1000.0)
    return {"run_sum": sum(runs), "run_n": len(runs), "block_sum": sum(blocks), "block_n": len(blocks),
            "cpu_us": sum(s.run for s in prog_rows) * 1000.0}


def mb_values(mb_samples, cpu_ms):
    """The DKMS build's carried tables as (Σ, n) in µs, and the carried CPU total."""
    out = {f"step:{k}": [sum(v) * 1000.0, len(v)] for k, v in mb_samples["steps"].items()}
    for k in ("dispatch_ms", "tail_run_ms", "tail_block_ms"):
        v = mb_samples[k]
        out[k[:-3]] = [sum(v) * 1000.0, len(v)]
    out["carried_cpu_us"] = [cpu_ms["carried"] * 1000.0, 1]
    return out


def tally(traced, cat_of):
    out = {}
    for w, cls, lab, how, root, hops, direct in traced:
        c = out.setdefault(cat_of(w), {"n": 0, "run": 0.0, "classes": {}, "labels": {}, "how": {},
                                       "split": {"direct": {"n": 0, "run": 0.0}, "inherited": {"n": 0, "run": 0.0}},
                                       "gone": []})
        c["n"] += 1
        c["run"] += w.run
        x = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
        x["n"] += 1
        x["run"] += w.run
        if cls != "own":
            c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
        if cls == "outside":
            c["how"][how] = c["how"].get(how, 0) + 1
            s = c["split"]["direct" if direct else "inherited"]
            s["n"] += 1
            s["run"] += w.run
        if cls in ("outside", "harness-python"):
            c["gone"].append([round(w.t_in, 6), w.comm, w.tid, round(w.run, 3), cls, lab, how, bool(direct),
                              f"{root[2]}[{root[3]}]@{root[1]:.6f}" if root else None])
    return out


def one(job, D, by_package=False, warm=False):
    phase = PHASE[job]
    rep = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(rep.get("pin.load_cpu", 3))
    kv, edges = bg.read_kv(os.path.join(D, "report.kv")), bg.load_edges(D)
    base = os.path.join(D, f"perf.{phase}")
    th, wk, fk, ts = base + ".timehist.txt.gz", base + ".wakeups.txt.gz", base + ".forks.txt.gz", \
        os.path.join(D, f"taskstats.{phase}.tsv")
    segs, wakeups = bg.load_segments(th), bg.load_wakeups(wk)
    forks, exits = bg.load_forks(fk)
    exec_rows = bg.load_exec_rows(fk)
    execs = {pid: f for _t, pid, f in exec_rows}
    recs = bg.process_records(bg.load_taskstats(ts)[0])
    root, tree, tid2pid, last_comm, _out = bg.phase_tree(job, segs, forks, meas_cpu, bg.launched_root(job, exec_rows))
    pids = sorted({tid2pid.get(t, t) for t in tree})
    role = {pid: (recs[pid]["comm"] if pid in recs else last_comm.get(pid, "?")) for pid in pids}
    hooks = None
    if job == "dkms":
        subs = bg.hook_subtrees(exec_rows, forks)
        hook_tids = set().union(*(seen for _f, seen in subs.values())) & tree if subs else set()
        prog = sorted({tid2pid.get(t, t) for t in hook_tids})
        hooks = {r: {"hook": f, "tids": seen & tree} for r, (f, seen) in subs.items()}
    else:
        prog = [p for p in pids if bg.is_program(job, execs.get(p), role.get(p))]
    prog_set = set(prog)
    rows = [s for s in segs if s.cpu == meas_cpu and s.tid in tree]
    if job == "dejadup":
        ends = [s.t_end for s in segs if tid2pid.get(s.tid, s.tid) == root]
        if ends:
            end = max(ends)     # analyze_phase's max(ends), taken once
            rows = [s for s in rows if s.t_in < end]
    trk = None
    if job == "tracker":
        trk, rows = bg.tracker_window(D, phase, edges, exec_rows, root, rows, execs, tid2pid)
    per_wakes, _iv, _merged = bg.thread_wakes(rows, wakeups)
    all_wakes = sorted((w for ws in per_wakes.values() for w in ws), key=lambda w: w.t_in)
    born = {c for _t, _p, _pc, c, _cc in forks}
    wakeup_rows = cc.load_wakeup_rows(wk)
    if by_package:
        tr = SessionTracer(wakeup_rows, set(pids), cc.by_tid(all_wakes), born=born,
                           execs={pid: f.rsplit("/", 1)[-1] for _t, pid, f in exec_rows})
    else:
        tr = cr.RootTracer(wakeup_rows, set(pids), cc.by_tid(all_wakes), born=born)
    index = wake_of_segment(per_wakes)
    if warm:   # every tree wake in time order first: both tracings memoize from the phase's start
        tr.classify(all_wakes)
        tr.trace(all_wakes)

    if job != "dkms":
        prog_wakes = [w for w in all_wakes if tid2pid.get(w.tid, w.tid) in prog_set]
        traced = tr.trace(prog_wakes)
        res = tally(traced, lambda w: job)
        prog_rows = [s for s in rows if tid2pid.get(s.tid, s.tid) in prog_set]
        span = (min(s.t_in for s in prog_rows), max(s.t_end for s in prog_rows)) if prog_rows else (0, 0)
        vals = {"base": batch_values(prog_rows, tid2pid, span, trk)}
        for tag, pick in (("rule", lambda x: x[1] == "outside"), ("direct", lambda x: x[1] == "outside" and x[6])):
            gone = [x[0] for x in traced if pick(x)]
            vals[tag] = batch_values(drop_segments(prog_rows, gone, index), tid2pid, span, trk)
            vals[tag]["removed"] = len(gone)
        check_n = cr.check(tr, prog_wakes[:200000])
        out = {"repeat": rep.get("repeat"), "dir": D, "values": vals, "tally": res,
               "roots": cr.runs(traced, top=8), "check_differ": check_n, "check_wakes": min(len(prog_wakes), 200000),
               "tree_threads": len(tree), "program_pids": len(prog)}
        return out

    # the DKMS build: the hook run that built the module, read as analyze_phase reads it
    build_root = max(hooks, key=lambda r_: sum(s_.run for s_ in rows if s_.tid in hooks[r_]["tids"]))
    htids = hooks[build_root]["tids"]
    h_tid2pid, h_role, h_parent = modbuild.hook_run(htids, segs, forks, recs, last_comm)
    h_jobs = modbuild.jobs_of(htids, h_tid2pid, h_role, h_parent, forks, exits, recs)

    def read(sg):
        r = modbuild.readings(h_jobs, htids, h_tid2pid, h_role, h_parent, sg, forks, exits, recs, meas_cpu)
        return mb_values(r["_samples"], r["cpu_ms"]), r
    base_vals, base_r = read(segs)
    # each wake of the build hook's threads by what it is carried as: a job kind's member role, make, the tail, or
    # the hook run's unmodelled rest; and every other hook run apart
    kids = collections.defaultdict(list)
    for c, p in h_parent.items():
        kids[p].append(c)
    kind_of_pid = {}
    for j in h_jobs:
        k = modbuild.kind_of(j, h_role, kids)
        for x in j["members"]:
            kind_of_pid[x] = k
    make_pids = {h_tid2pid.get(t, t) for t in htids if h_role.get(h_tid2pid.get(t, t)) == "make"}
    t_last = base_r["tail"]["start_s"]

    def cat(w):
        if w.tid not in htids:
            return "other hook runs"
        pid = h_tid2pid.get(w.tid, w.tid)
        if pid in kind_of_pid:
            k = kind_of_pid[pid]
            return f"job {k} {modbuild.role_of(h_role.get(pid, '?'))}" if k else "unmodelled job"
        if pid in make_pids:
            return "make"
        if t_last is not None and w.t_in >= t_last:
            return "tail"
        return "unmodelled"
    prog_wakes = [w for w in all_wakes if tid2pid.get(w.tid, w.tid) in prog_set]
    traced = tr.trace(prog_wakes)
    vals = {"base": base_vals}
    for tag, pick in (("rule", lambda x: x[1] == "outside"), ("direct", lambda x: x[1] == "outside" and x[6])):
        gone = [x[0] for x in traced if pick(x) and x[0].tid in htids]
        vals[tag] = read(drop_segments(segs, gone, index))[0] if gone else base_vals
        vals[tag + "_removed"] = len(gone)
    return {"repeat": rep.get("repeat"), "dir": D, "values": vals, "tally": tally(traced, cat),
            "roots": cr.runs([x for x in traced if x[0].tid in htids], top=8),
            "check_differ": cr.check(tr, prog_wakes[:200000]), "check_wakes": min(len(prog_wakes), 200000),
            "tree_threads": len(tree), "program_pids": len(prog), "hook": hooks[build_root]["hook"],
            "cpu_ms": base_r["cpu_ms"]}


def main():
    job, pooled_path, root = sys.argv[1], sys.argv[2], sys.argv[3]
    out_path = sys.argv[sys.argv.index("--out") + 1]
    pooled = json.load(open(pooled_path))
    by_package = "--session-by-package" in sys.argv
    warm = "--warm" in sys.argv
    dirs = find_dirs(root, job, pooled)
    result = json.load(open(out_path)) if os.path.exists(out_path) else {}
    name = ENTRY[job] + (" (session by package)" if by_package else "") + (" (traced in time order)" if warm else "")
    sec = result.setdefault(name, {"campaign": TAG[job], "phase": PHASE[job], "job": job, "kind": "batch",
                                   "reading": ("session by package" if by_package else "census_core")
                                   + (", traced in time order" if warm else ""),
                                   "repeats": {}})
    for key, D in dirs.items():
        if key in sec["repeats"]:
            continue
        r = one(job, D, by_package, warm)
        sec["repeats"][key] = r
        o = sum(c["classes"].get("outside", {}).get("n", 0) for c in r["tally"].values())
        n = sum(c["n"] for c in r["tally"].values())
        print(f"{name} r{key}: {n} wakes, outside {o}, check differs {r['check_differ']}", flush=True)
        json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
