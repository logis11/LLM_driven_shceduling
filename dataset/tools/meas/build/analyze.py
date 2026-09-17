#!/usr/bin/env python3
"""Analyse one run directory of the 9.6 build campaign (run.sh output) by the
rules fixed in the method before the run (campaign/method.md §4–§5; changelog
D2, D8).

analyze.py <run-dir> [--phase NAME ...] [--json out.json] [--text out.md]

Per phase: the process tree rooted at the phase's command on the measured CPU
(fork rows from perf script; comms at exit from taskstats), the roles (comm at
exit), the make jobs (a non-make child of a make and its subtree), the
concurrency of live jobs, per-role wakes (a timehist row is a segment; a
segment is a wake when a wakeup row for the thread lies between its previous
schedule-out and this schedule-in, else a resume merged into the preceding
wake — 9.5 follow-ups decision 4), the off-CPU interval after each wake by the
sched-out state (D = disk-wait candidate, S = sleep, R = runnable), per-process
CPU totals and block-I/O delay from taskstats, make's per-dispatch run between
consecutive forks, job counts, the batch programs' saturation, thread share and
wait shares, and the per-process cross-check of perf run against taskstats
CPU. Rows on the measured CPU outside the tree (the runner's agent, kernel
threads) are counted and listed by comm, never folded in.
"""

import argparse
import bisect
import gzip
import json
import os
import re
import statistics
import sys
from collections import defaultdict, namedtuple

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("campaign_analyze", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campaign", "analyze.py"))
_campaign_analyze = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_campaign_analyze)
pct, TASK = _campaign_analyze.pct, _campaign_analyze.TASK   # the 9.5 analyzer's percentile and `comm[tid/pid]` parser

Seg = namedtuple("Seg", "t_in t_wake t_end run comm tid pid state cpu")

# timehist --state: time [cpu] comm[tid/pid] wait sch_delay run state
ROW = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)(?:\s+(\S+))?\s*$")
WAKE = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+awakened:\s+(.*?)\s*$")
FORK = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_fork:\s+comm=(.*?)\s+pid=(\d+)\s+child_comm=(.*?)\s+child_pid=(\d+)")
EXIT = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_exit:\s+comm=(.*?)\s+pid=(\d+)")

# comms on the measured CPU that are never part of a phase's tree: kernel threads and the runner's own agent
OUTSIDE_PREFIX = ("kworker/", "ksoftirqd/", "migration/", "rcu_", "cpuhp/", "idle_inject/", "kcompactd", "kswapd",
                  "jbd2/", "xfsaild", "swapper", "watchdog", "irq/", "khugepaged", "ext4-", "blkcg", "kthreadd")
OUTSIDE_PREFIX = OUTSIDE_PREFIX + (".NET", "provjobd", "Hosted Compute")
OUTSIDE_COMMS = {"Runner.Listener", "Runner.Worker", "dotnet", "containerd", "dockerd", "containerd-shim", "provjobd",
                 "perf", "taskstats_liste", "sudo", "taskset", "systemd", "systemd-journal", "systemd-udevd",
                 "snapd", "cron", "rsyslogd", "walinuxagent", "python3-walinux", "hv_kvp_daemon", "chronyd",
                 "multipathd", "dbus-daemon", "polkitd", "networkd-dispat", "systemd-resolve", "systemd-network",
                 "sshd", "mono", "node", "Hosted Compute", "sleep", "gzip", "grep", "date", "tee", "sed"}
PHASE_ROOT = {"build-j8-warm": "make", "build-j8-cold": "make", "build-j1-warm": "make", "dkms": "dkms",
              "clamscan": "clamscan", "ffmpeg": "ffmpeg", "handbrake": "HandBrakeCLI", "train": "python3",
              "tracker": "dbus-run-sessio"}
# the batch program inside each batch phase's tree (D7): its processes carry the saturation and wait figures; the
# rest of the tree (a session bus, the poll loop) is reported beside them
BATCH_PROGRAM = {"clamscan": ("clamscan",), "ffmpeg": ("ffmpeg",), "handbrake": ("HandBrakeCLI",), "train": ("python3",),
                 "tracker": ("tracker-miner-f", "tracker-extract")}   # the miner and the extractor it activates are one indexing job
QUANTILE_PROBS = (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999)
EPS = 1e-6


def open_text(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def qtable(values):
    if not values:
        return None
    v = sorted(values)
    return [round(pct(v, q), 3) for q in QUANTILE_PROBS]


def dist(values):
    if not values:
        return {"n": 0}
    return {"n": len(values), "p50": round(pct(values, .5), 3), "p90": round(pct(values, .9), 3),
            "p99": round(pct(values, .99), 3), "mean": round(statistics.fmean(values), 3),
            "sum": round(sum(values), 3), "q": qtable(values)}


def outside(comm):
    return comm in OUTSIDE_COMMS or comm.startswith(OUTSIDE_PREFIX)


# ---- loading -------------------------------------------------------------

def load_segments(path):
    """All timehist rows as segments (times in s, run/delay in ms), every CPU."""
    segs = []
    with open_text(path) as handle:
        for line in handle:
            m = ROW.match(line)
            if not m:
                continue
            t, cpu, task, _wait, delay, run, state = m.groups()
            tm = TASK.match(task.strip())
            if not tm:
                continue
            comm, a, b = tm.group(1), int(tm.group(2)), tm.group(3)
            tid, pid = (a, int(b)) if b else (a, a)
            t, delay, run = float(t), float(delay), float(run)
            segs.append(Seg(t - run / 1000.0, t - run / 1000.0 - delay / 1000.0, t, run, comm, tid, pid, state or "", int(cpu)))
    segs.sort(key=lambda s: s.t_in)
    return segs


def load_wakeups(path):
    """tid -> sorted wakeup times (any waker, any CPU)."""
    out = defaultdict(list)
    with open_text(path) as handle:
        for line in handle:
            m = WAKE.match(line)
            if not m:
                continue
            t, _, _, wakee = m.groups()
            km = TASK.match(wakee.strip())
            if km:
                out[int(km.group(2))].append(float(t))
    for v in out.values():
        v.sort()
    return out


def load_forks(path):
    """(forks: list of (t, parent_tid, parent_comm, child_tid, child_comm)), (exits: tid -> (t, comm))."""
    forks, exits = [], {}
    with open_text(path) as handle:
        for line in handle:
            m = FORK.match(line)
            if m:
                forks.append((float(m.group(1)), int(m.group(3)), m.group(2), int(m.group(5)), m.group(4)))
                continue
            m = EXIT.match(line)
            if m:
                exits[int(m.group(3))] = (float(m.group(1)), m.group(2))
    forks.sort()
    return forks, exits


def load_taskstats(path):
    """Rows of the listener file: list of dicts (numbers as int), plus the trailer counters."""
    rows, trailer, header = [], {}, None
    with open(path) as handle:
        for line in handle:
            if line.startswith("#"):
                for kv in line[1:].split():
                    k, _, v = kv.partition("=")
                    if v.lstrip("-").isdigit():
                        trailer[k] = int(v)
                continue
            parts = line.rstrip("\n").split("\t")
            if header is None:
                header = parts
                continue
            if len(parts) != len(header):
                continue
            row = {}
            for k, v in zip(header, parts):
                row[k] = int(v) if v.lstrip("-").isdigit() else v
            rows.append(row)
    return rows, trailer


def process_records(ts_rows):
    """Per process (tgid) from the listener rows. The kernel sends a per-thread row for every exiting thread and,
    for a thread group that ever had more than one thread, a per-tgid row of sums at the last exit (comm and pid
    empty in it). A process's identity, parent, lifetime and exit time come from its main thread's row (id == tgid),
    its CPU from the tgid sums when present. CPU is `cpu_run_virtual_total` (the scheduler's sum_exec_runtime, ns);
    `utime + stime` (tick-sampled, ms resolution) is kept beside it. A thread's block-I/O delay larger than its
    lifetime is a wait whose start was never stamped (dry run 1: a HandBrake thread at the machine's uptime) and is
    rejected and counted."""
    by_tgid = defaultdict(list)
    tgid_rows = {}
    for r in ts_rows:
        if r["type"] == "tgid":
            tgid_rows[r["id"]] = r
        else:
            by_tgid[r["tgid"] or r["id"]].append(r)
    recs = {}
    for tgid, rows in by_tgid.items():
        main = next((r for r in rows if r["id"] == tgid), None) or rows[0]
        agg = tgid_rows.get(tgid)
        valid = [r for r in rows if r["blkio_delay_ns"] <= r["etime_us"] * 1000]
        invalid = len(rows) - len(valid)
        cpu_ns = agg["run_virtual_ns"] if agg else sum(r["run_virtual_ns"] for r in rows)
        rec = {"pid": tgid, "comm": main["comm"], "ppid": main["ppid"], "etime_us": main["etime_us"],
               "t_exit": max(r["recv_mono_ns"] for r in rows) / 1e9,
               "threads": len(rows), "cpu_ns": cpu_ns, "utime_stime_us": (agg["utime_us"] + agg["stime_us"]) if agg else sum(r["utime_us"] + r["stime_us"] for r in rows),
               "cpu_delay_ns": agg["cpu_delay_ns"] if agg else sum(r["cpu_delay_ns"] for r in rows),
               "blkio_ns": sum(r["blkio_delay_ns"] for r in valid), "blkio_count": sum(r["blkio_count"] for r in valid),
               "blkio_invalid_threads": invalid, "nvcsw": sum(r["nvcsw"] for r in rows), "nivcsw": sum(r["nivcsw"] for r in rows),
               "thread_cpu_ns": {r["id"]: r["run_virtual_ns"] for r in rows}, "exitcode": main["exitcode"]}
        recs[tgid] = rec
    return recs


# ---- the tree --------------------------------------------------------------

def build_tree(phase, segs, forks, recs, meas_cpu):
    """Return (root_tid, tree_tids, tid2pid, role_of_pid, parent_of_pid, outside_by_comm).

    The root is the earliest thread on the measured CPU whose comm is the phase's program (`taskset` execs it, so it
    is the first of its name there; sudo and dbus-run-session wrappers run pinned too and are its parents); the tree
    is every descendant by the fork rows plus the root. Roles: comm at exit (the process record), else the last comm
    seen in a segment."""
    on_cpu = [s for s in segs if s.cpu == meas_cpu]
    children = defaultdict(list)
    parent = {}
    for _, p, _pc, c, _cc in forks:
        children[p].append(c); parent[c] = p
    tid2pid = {}
    last_comm = {}
    for s in segs:
        tid2pid[s.tid] = s.pid
        last_comm[s.tid] = s.comm
    root_comm = PHASE_ROOT.get(phase, phase.split("-")[0])
    root = None
    for s in on_cpu:
        if s.comm == root_comm:
            root = s.tid; break
    if root is None:   # fall back: the earliest non-outside thread on the measured CPU
        for s in on_cpu:
            if not outside(s.comm):
                root = s.tid; break
    tree = set()
    stack = [root] if root is not None else []
    while stack:
        t = stack.pop()
        if t in tree:
            continue
        tree.add(t); stack.extend(children.get(t, ()))
    # exit comm per pid from taskstats (tgid rows), else perf's exit row, else last segment comm
    role = {pid: r["comm"] for pid, r in recs.items()}
    for t in tree:
        pid = tid2pid.get(t, t)
        role.setdefault(pid, last_comm.get(t, "?"))
    parent_pid = {}
    for t in tree:
        pid = tid2pid.get(t, t)
        p = parent.get(t)
        if p is not None and pid == t:   # a process (its main thread): parent process = the forking thread's pid
            parent_pid[pid] = tid2pid.get(p, p)
    for pid, r in recs.items():
        if pid in tree and pid not in parent_pid:
            parent_pid[pid] = r["ppid"]
    out_by_comm = defaultdict(lambda: [0, 0.0])
    for s in on_cpu:
        if s.tid not in tree:
            out_by_comm[s.comm][0] += 1; out_by_comm[s.comm][1] += s.run
    return root, tree, tid2pid, role, parent_pid, {k: {"rows": v[0], "run_ms": round(v[1], 3)} for k, v in out_by_comm.items()}


JOB_KINDS = (("object", ("fixdep",)), ("link", ("ld", "collect2", "ld.bfd", "ld.lld")), ("archive", ("ar",)),
             ("probe", ("cc1", "cc1plus", "gcc", "gcc-13", "as", "cpp")))


def job_kind(roles):
    """kbuild's object recipes run `fixdep` after the compiler (Kbuild.include cmd_and_fixdep); its compiler probes
    (`try-run`, `cc-option`, `as-instr`) never do. A job with fixdep is an object compile; with a linker and no fixdep
    a link; with `ar` a per-directory archive (cmd_ar_builtin); with a compiler and none of those a compiler probe;
    anything else (mkdir, a bare shell, pahole-flags.sh) a helper. Only probe members carry the "(probe)" role suffix."""
    for kind, marks in JOB_KINDS:
        if any(m in roles for m in marks):
            return kind
    return "helper"


def jobs_of(tree, tid2pid, role, parent_pid, forks, exits, recs):
    """make jobs (D2): a non-make child process of a make process, with its subtree; fork and last-exit times."""
    children = defaultdict(list)
    for pid, pp in parent_pid.items():
        children[pp].append(pid)
    fork_t = {c: t for t, _p, _pc, c, _cc in forks}
    def exit_t(pid):
        if pid in exits:
            return exits[pid][0]
        r = recs.get(pid)
        return None if r is None else r["t_exit"]
    makes = {pid for pid in set(tid2pid.get(t, t) for t in tree) if role.get(pid) == "make"}
    jobs = []
    for m in makes:
        for c in children.get(m, ()):
            if role.get(c) == "make":
                continue
            members, stack = [], [c]
            while stack:
                x = stack.pop(); members.append(x); stack.extend(children.get(x, ()))
            starts = [fork_t[x] for x in members if x in fork_t]
            ends = [e for e in (exit_t(x) for x in members) if e is not None]
            rs = sorted(role.get(x, "?") for x in members)
            jobs.append({"root": c, "make": m, "members": members, "roles": rs, "kind": job_kind(rs),
                         "start": min(starts) if starts else None, "end": max(ends) if ends else None})
    jobs.sort(key=lambda j: (j["start"] is None, j["start"]))
    return jobs, makes


def concurrency(jobs):
    """Live jobs over time: (max, mean over the busy span, histogram of live count by time share)."""
    ev = []
    for j in jobs:
        if j["start"] is not None and j["end"] is not None:
            ev.append((j["start"], 1)); ev.append((j["end"], -1))
    ev.sort()
    live, t_prev, mx, share = 0, None, 0, defaultdict(float)
    for t, d in ev:
        if t_prev is not None and live > 0:
            share[live] += t - t_prev
        live += d; mx = max(mx, live); t_prev = t
    total = sum(share.values()) or 1.0
    mean = sum(k * v for k, v in share.items()) / total
    return {"max": mx, "mean_busy": round(mean, 2), "time_share": {str(k): round(v / total, 3) for k, v in sorted(share.items())}}


def merge_resumes(rows, wakeups_by_tid):
    """Fold resume-after-preemption segments into the wake they continue (9.5 follow-ups decision 4), carrying the
    last segment's sched-out state so the off-CPU interval after the wake is classified by how the wake ended.
    rows: segments sorted by t_in. Returns (wakes sorted by t_in, number of segments merged)."""
    last, out, merged = {}, [], 0
    for r in rows:
        i = last.get(r.tid)
        if i is None:
            out.append(r); last[r.tid] = len(out) - 1
            continue
        prev = out[i]
        wk = wakeups_by_tid.get(r.tid, [])
        k = bisect.bisect_right(wk, prev.t_end - EPS)
        if k < len(wk) and wk[k] <= r.t_in + EPS:
            out.append(r); last[r.tid] = len(out) - 1
        else:
            out[i] = prev._replace(run=prev.run + r.run, t_end=r.t_end, state=r.state)
            merged += 1
    out.sort(key=lambda r: r.t_in)
    return out, merged


# ---- per role -------------------------------------------------------------

def role_shapes(tree, tid2pid, role, segs, wakeups, meas_cpu, recs):
    """Per role: wakes (run per wake), off-CPU intervals after each wake by kind, per-process CPU and delays."""
    rows = [s for s in segs if s.tid in tree and s.cpu == meas_cpu]
    wakes, merged = merge_resumes(rows, wakeups)
    by_tid = defaultdict(list)
    for w in wakes:
        by_tid[w.tid].append(w)
    per_role = defaultdict(lambda: {"run_ms": [], "off_D_ms": [], "off_S_ms": [], "off_R_ms": [], "wakes": 0, "threads": set(),
                                    "procs": set(), "cpu_us": [], "ts_cpu_us": [], "tick_cpu_us": [], "blkio_ns": [], "blkio_count": [], "cpu_delay_ns": [],
                                    "etime_us": [], "nvcsw": [], "nivcsw": [], "perf_run_ms_by_pid": defaultdict(float),
                                    "wakes_by_pid": defaultdict(int), "blkio_invalid": 0})
    for tid, ws in by_tid.items():
        pid = tid2pid.get(tid, tid)
        r = per_role[role.get(pid, "?")]
        r["threads"].add(tid); r["procs"].add(pid); r["wakes"] += len(ws); r["wakes_by_pid"][pid] += len(ws)
        for a, b in zip(ws, ws[1:]):
            r["run_ms"].append(a.run)
            off = (b.t_wake - a.t_end) * 1000.0   # from the previous wake's last sched-out to the wakeup
            kind = "off_D_ms" if a.state.startswith("D") else "off_S_ms" if a.state.startswith("S") else "off_R_ms"
            r[kind].append(max(off, 0.0))
        r["run_ms"].append(ws[-1].run)
        r["perf_run_ms_by_pid"][pid] += sum(w.run for w in ws)
    for pid in set(tid2pid.get(t, t) for t in tree):
        t = recs.get(pid)
        if t is None:
            continue
        r = per_role[role.get(pid, "?")]
        r["procs"].add(pid)
        r["ts_cpu_us"].append(t["cpu_ns"] / 1000.0); r["tick_cpu_us"].append(t["utime_stime_us"])
        r["blkio_ns"].append(t["blkio_ns"]); r["blkio_count"].append(t["blkio_count"]); r["blkio_invalid"] += t["blkio_invalid_threads"]
        r["cpu_delay_ns"].append(t["cpu_delay_ns"]); r["etime_us"].append(t["etime_us"]); r["nvcsw"].append(t["nvcsw"]); r["nivcsw"].append(t["nivcsw"])
    out = {}
    samples = {}
    for name, r in per_role.items():
        # the process's CPU is the sum of its perf segments on the measured CPU: taskstats stamps its record early in
        # the exit path, before the teardown (~0.5 ms), which is most of a sub-millisecond process (dry run 2)
        r["cpu_us"] = [ms * 1000.0 for ms in r["perf_run_ms_by_pid"].values()]
        samples[name] = {"run_ms": r["run_ms"], "off_D_ms": r["off_D_ms"], "off_S_ms": r["off_S_ms"], "off_R_ms": r["off_R_ms"],
                         "cpu_us": r["cpu_us"], "blkio_ns": r["blkio_ns"], "etime_us": r["etime_us"], "wakes_by_pid": list(r["wakes_by_pid"].values())}
        cross = []
        for pid, ms in r["perf_run_ms_by_pid"].items():
            t = recs.get(pid)
            if t is not None and t["cpu_ns"] > 0:
                cross.append(ms * 1e6 / t["cpu_ns"])
        out[name] = {"processes": len(r["procs"]), "threads": len(r["threads"]), "wakes": r["wakes"],
                     "wakes_per_process": dist(list(r["wakes_by_pid"].values())),
                     "run_per_wake_ms": dist(r["run_ms"]),
                     "off_after_D_ms": dist(r["off_D_ms"]), "off_after_S_ms": dist(r["off_S_ms"]), "off_after_R_ms": dist(r["off_R_ms"]),
                     "cpu_per_process_us": dist(r["cpu_us"]), "taskstats_cpu_per_process_us": dist(r["ts_cpu_us"]),
                     "tick_cpu_per_process_us": dist(r["tick_cpu_us"]),
                     "etime_per_process_us": dist(r["etime_us"]),
                     "blkio_delay_per_process_ns": dist(r["blkio_ns"]), "blkio_count_per_process": dist(r["blkio_count"]),
                     "blkio_invalid_threads": r["blkio_invalid"],
                     "cpu_delay_per_process_ns": dist(r["cpu_delay_ns"]),
                     "nvcsw_per_process": dist(r["nvcsw"]), "nivcsw_per_process": dist(r["nivcsw"]),
                     "perf_over_taskstats_cpu": dist(cross)}
    return out, merged, len(rows), len(wakes), samples


def dispatch(tree, tid2pid, role, segs, forks, meas_cpu, recs):
    """make's per-dispatch run: for each make thread, the run of its segments between consecutive forks it issued."""
    make_tids = [t for t in tree if role.get(tid2pid.get(t, t)) == "make"]
    forks_by = defaultdict(list)
    for t, p, _pc, _c, _cc in forks:
        if p in make_tids:
            forks_by[p].append(t)
    seg_by = defaultdict(list)
    for s in segs:
        if s.tid in forks_by and s.cpu == meas_cpu:
            seg_by[s.tid].append(s)
    per_dispatch, cross = [], []
    for tid, fts in forks_by.items():
        fts.sort()
        ss = sorted(seg_by.get(tid, []), key=lambda s: s.t_in)
        ends = [s.t_end for s in ss]
        for a, b in zip(fts, fts[1:]):
            i, j = bisect.bisect_right(ends, a), bisect.bisect_right(ends, b)
            per_dispatch.append(sum(s.run for s in ss[i:j]))
        t = recs.get(tid2pid.get(tid, tid))
        if t is not None and fts:
            cross.append(t["cpu_ns"] / len(fts) / 1e6)
    return {"per_dispatch_ms": dist(per_dispatch), "makes": len(forks_by), "forks": sum(len(v) for v in forks_by.values()),
            "cpu_per_fork_ms_by_make": dist(cross), "_samples": {"per_dispatch_ms": per_dispatch, "cpu_per_fork_ms_by_make": cross}}


def batch(phase, tree, tid2pid, role, segs, wakeups, meas_cpu, recs, cmd_wall_s):
    """The batch program's processes (BATCH_PROGRAM): saturation = CPU over the program's own lifetime, the dominant
    thread's share, disk and sleep shares; the rest of the tree is reported beside it."""
    prog = BATCH_PROGRAM.get(phase)
    pids = set(tid2pid.get(x, x) for x in tree)
    prog_pids = {p for p in pids if role.get(p) in prog} if prog else pids
    prog_tids = {t for t in tree if tid2pid.get(t, t) in prog_pids}
    rows = [s for s in segs if s.tid in prog_tids and s.cpu == meas_cpu]
    run_by_tid = defaultdict(float)
    for s in rows:
        run_by_tid[s.tid] += s.run
    total_run_ms = sum(run_by_tid.values())
    dominant = max(run_by_tid.values()) if run_by_tid else 0.0
    prog_recs = [recs[p] for p in prog_pids if p in recs]
    cpu_ns = sum(r["cpu_ns"] for r in prog_recs)
    life_s = max((r["etime_us"] for r in prog_recs), default=0) / 1e6
    blkio = sum(r["blkio_ns"] for r in prog_recs)
    off = defaultdict(float)
    wakes, _ = merge_resumes(rows, wakeups)
    by_tid = defaultdict(list)
    for w in wakes:
        by_tid[w.tid].append(w)
    for ws in by_tid.values():
        for a, b in zip(ws, ws[1:]):
            kind = "D" if a.state.startswith("D") else "S" if a.state.startswith("S") else "R"
            off[kind] += max((b.t_wake - a.t_end) * 1000.0, 0.0)
    other = sorted({role.get(p, "?") for p in pids - prog_pids})
    return {"program": " + ".join(prog) if prog else None, "processes": len(prog_pids), "threads_with_runs": len(run_by_tid),
            "lifetime_s": round(life_s, 3), "cmd_wall_s": round(cmd_wall_s, 2) if cmd_wall_s else None,
            "perf_run_s": round(total_run_ms / 1000.0, 3), "taskstats_cpu_s": round(cpu_ns / 1e9, 3),
            "saturation": round(cpu_ns / 1e9 / life_s, 4) if life_s else None,
            "saturation_perf": round(total_run_ms / 1000.0 / life_s, 4) if life_s else None,
            "dominant_thread_share": round(dominant / total_run_ms, 4) if total_run_ms else None,
            "thread_cpu_share_top5": sorted((round(v / total_run_ms, 4) for v in run_by_tid.values()), reverse=True)[:5] if total_run_ms else [],
            "blkio_delay_s": round(blkio / 1e9, 4), "blkio_share_of_lifetime": round(blkio / 1e9 / life_s, 4) if life_s else None,
            "off_cpu_after_D_s": round(off["D"] / 1000.0, 3), "off_cpu_after_S_s": round(off["S"] / 1000.0, 3), "off_cpu_after_R_s": round(off["R"] / 1000.0, 3),
            "blkio_invalid_threads": sum(r["blkio_invalid_threads"] for r in prog_recs),
            "other_roles_in_tree": other}


# ---- driver ----------------------------------------------------------------

def analyze_phase(D, phase, meas_cpu, edges):
    base = os.path.join(D, f"perf.{phase}")
    th, wk, fk, ts = base + ".timehist.txt.gz", base + ".wakeups.txt.gz", base + ".forks.txt.gz", os.path.join(D, f"taskstats.{phase}.tsv")
    if not all(os.path.exists(p) for p in (th, wk, fk, ts)):
        return {"missing": [p for p in (th, wk, fk, ts) if not os.path.exists(p)]}
    segs = load_segments(th); wakeups = load_wakeups(wk); forks, exits = load_forks(fk); ts_rows, trailer = load_taskstats(ts)
    # taskstats receive time is CLOCK_MONOTONIC, as is perf's -k CLOCK_MONOTONIC
    recs = process_records(ts_rows)
    root, tree, tid2pid, role, parent_pid, out_by_comm = build_tree(phase, segs, forks, recs, meas_cpu)
    e = edges.get(phase, {})
    span_s = (e["end"] - e["start"]) / 1e9 if "start" in e and "end" in e else (segs[-1].t_end - segs[0].t_in if segs else 0.0)
    cmd_wall_s = e.get("cmd_wall_s")
    res = {"root_tid": root, "root_comm": role.get(tid2pid.get(root, root)) if root is not None else None,
           "tree_threads": len(tree), "tree_processes": len(set(tid2pid.get(t, t) for t in tree)),
           "taskstats_rows": len(ts_rows), "taskstats_processes": len(recs), "taskstats_trailer": trailer,
           "fork_rows": len(forks), "exit_rows": len(exits),
           "phase_span_s": round(span_s, 2), "cmd_wall_s": round(cmd_wall_s, 2) if cmd_wall_s else None,
           "outside_on_measured_cpu": dict(sorted(out_by_comm.items(), key=lambda kv: -kv[1]["run_ms"])[:25])}
    jobs, makes = (jobs_of(tree, tid2pid, role, parent_pid, forks, exits, recs) if PHASE_ROOT.get(phase) in ("make", "dkms") else ([], set()))
    role_key = dict(role)   # roles keyed by comm and job kind: members of probe jobs carry " (probe)"
    for j in jobs:
        if j["kind"] == "probe":
            for x in j["members"]:
                role_key[x] = role.get(x, "?") + " (probe)"
    roles, merged, n_rows, n_wakes, samples = role_shapes(tree, tid2pid, role_key, segs, wakeups, meas_cpu, recs)
    res["_samples"] = {"roles": samples}
    res["segments_in_tree"] = n_rows; res["wakes_in_tree"] = n_wakes; res["resumes_merged"] = merged
    res["roles"] = dict(sorted(roles.items(), key=lambda kv: -(kv[1]["cpu_per_process_us"].get("sum") or 0)))
    role_counts = defaultdict(int)
    for pid in set(tid2pid.get(t, t) for t in tree):
        role_counts[role_key.get(pid, "?")] += 1
    res["processes_by_role"] = dict(sorted(role_counts.items(), key=lambda kv: -kv[1]))
    if PHASE_ROOT.get(phase) in ("make", "dkms"):
        shapes = defaultdict(int)
        kinds = defaultdict(int)
        for j in jobs:
            shapes[j["kind"] + ": " + " ".join(j["roles"])] += 1; kinds[j["kind"]] += 1
        compile_jobs = [j for j in jobs if j["kind"] == "object" and any(r in ("cc1", "cc1plus") for r in j["roles"])]
        fork_t = {c: t for t, _p, _pc, c, _cc in forks}
        cc1_live = [{"start": fork_t.get(pid), "end": recs[pid]["t_exit"]} for pid in recs
                    if recs[pid]["comm"] in ("cc1", "cc1plus") and pid in tree and fork_t.get(pid) is not None]
        res["jobs"] = {"count": len(jobs), "kinds": dict(kinds), "makes": len(makes), "concurrency": concurrency(jobs),
                       "compile_jobs": len(compile_jobs), "compile_concurrency": concurrency(compile_jobs),
                       "cc1_processes": len(cc1_live), "cc1_concurrency": concurrency(cc1_live),
                       "compile_job_lifetime_ms": dist([(j["end"] - j["start"]) * 1000.0 for j in compile_jobs if j["start"] is not None and j["end"] is not None]),
                       "members_per_job": dist([len(j["members"]) for j in jobs]),
                       "job_lifetime_ms": dist([(j["end"] - j["start"]) * 1000.0 for j in jobs if j["start"] is not None and j["end"] is not None]),
                       "shapes": dict(sorted(shapes.items(), key=lambda kv: -kv[1])[:20])}
        res["dispatch"] = dispatch(tree, tid2pid, role, segs, forks, meas_cpu, recs)
    else:
        res["batch"] = batch(phase, tree, tid2pid, role, segs, wakeups, meas_cpu, recs, cmd_wall_s)
    return res


def load_edges(D):
    """Phase edges on the monotonic clock (edges.jsonl) plus the command's own wall time (phases.jsonl)."""
    edges = defaultdict(dict)
    p = os.path.join(D, "edges.jsonl")
    if os.path.exists(p):
        for line in open(p):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            edges[e["phase"]][e["edge"]] = e["mono_ns"]
    p = os.path.join(D, "phases.jsonl")
    if os.path.exists(p):
        for line in open(p):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            edges[e["phase"]]["cmd_wall_s"] = (e["end_us"] - e["start_us"]) / 1e6
            edges[e["phase"]]["rc"] = e["rc"]
    return edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir"); ap.add_argument("--phase", action="append")
    ap.add_argument("--json"); ap.add_argument("--meas-cpu", type=int)
    ap.add_argument("--samples", action="store_true", help="keep the raw per-role sample arrays in the JSON (for pooling)")
    args = ap.parse_args()
    D = args.run_dir
    report = json.load(open(os.path.join(D, "report.json"))) if os.path.exists(os.path.join(D, "report.json")) else {}
    meas_cpu = args.meas_cpu if args.meas_cpu is not None else int(report.get("pin.load_cpu", 3))
    phases = args.phase or [os.path.basename(p)[len("taskstats."):-len(".tsv")] for p in sorted(
        os.path.join(D, f) for f in os.listdir(D) if f.startswith("taskstats.") and f.endswith(".tsv") and "smoke" not in f)]
    edges = load_edges(D)
    out = {"run_dir": D, "meas_cpu": meas_cpu, "mode": report.get("mode"), "repeat": report.get("repeat"),
           "cpu_model": None, "phases": {}}
    spec = os.path.join(D, "spec.json")
    if os.path.exists(spec):
        out["cpu_model"] = json.load(open(spec)).get("cpu_model")
    for ph in phases:
        out["phases"][ph] = analyze_phase(D, ph, meas_cpu, edges)
    if args.json:
        if not args.samples:
            for r in out["phases"].values():
                r.pop("_samples", None)
                if "dispatch" in r:
                    r["dispatch"].pop("_samples", None)
        json.dump(out, open(args.json, "w"), indent=1)
    for ph, r in out["phases"].items():
        if "missing" in r:
            print(f"{ph}: missing {r['missing']}"); continue
        print(f"{ph}: root {r['root_comm']}[{r['root_tid']}] tree {r['tree_processes']} procs / {r['tree_threads']} threads, "
              f"cmd {r['cmd_wall_s']} s (edges {r['phase_span_s']} s), segments {r['segments_in_tree']} wakes {r['wakes_in_tree']} merged {r['resumes_merged']}, "
              f"taskstats rows {r['taskstats_rows']} enobufs {r['taskstats_trailer'].get('enobufs')}")
        for name, rr in list(r["roles"].items())[:12]:
            c = rr["cpu_per_process_us"]
            print(f"  {name:16s} procs {rr['processes']:5d} wakes {rr['wakes']:7d} (per proc p50 {rr['wakes_per_process'].get('p50')}) run/wake p50 {rr['run_per_wake_ms'].get('p50')} ms "
                  f"cpu/proc p50 {c.get('p50')} us  blkio/proc p50 {rr['blkio_delay_per_process_ns'].get('p50')} ns  perf/ts p50 {rr['perf_over_taskstats_cpu'].get('p50')}")
        if "jobs" in r:
            j = r["jobs"]
            print(f"  jobs {j['count']} {j['kinds']} (compile {j['compile_jobs']}, live max {j['compile_concurrency']['max']} mean {j['compile_concurrency']['mean_busy']}; cc1 {j['cc1_processes']} live max {j['cc1_concurrency']['max']} mean {j['cc1_concurrency']['mean_busy']}) makes {j['makes']} concurrency max {j['concurrency']['max']} mean {j['concurrency']['mean_busy']} "
                  f"members/job p50 {j['members_per_job'].get('p50')}; dispatch p50 {r['dispatch']['per_dispatch_ms'].get('p50')} ms over {r['dispatch']['forks']} forks")
            for shape, n in list(j["shapes"].items())[:6]:
                print(f"    {n:6d} × {shape}")
        if "batch" in r:
            print(f"  batch {r['batch']}")
        top = list(r["outside_on_measured_cpu"].items())[:5]
        print(f"  outside the tree on the measured CPU: {top}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
