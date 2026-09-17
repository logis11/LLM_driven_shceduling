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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "campaign"))
from analyze import pct, TASK  # noqa: E402

Seg = namedtuple("Seg", "t_in t_wake t_end run comm tid pid state cpu")

# timehist --state: time [cpu] comm[tid/pid] wait sch_delay run state
ROW = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)(?:\s+(\S+))?\s*$")
WAKE = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+awakened:\s+(.*?)\s*$")
FORK = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_fork:\s+comm=(.*?)\s+pid=(\d+)\s+child_comm=(.*?)\s+child_pid=(\d+)")
EXIT = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_exit:\s+comm=(.*?)\s+pid=(\d+)")

# comms on the measured CPU that are never part of a phase's tree: kernel threads and the runner's own agent
OUTSIDE_PREFIX = ("kworker/", "ksoftirqd/", "migration/", "rcu_", "cpuhp/", "idle_inject/", "kcompactd", "kswapd",
                  "jbd2/", "xfsaild", "swapper", "watchdog", "irq/", "khugepaged", "ext4-", "blkcg", "kthreadd")
OUTSIDE_COMMS = {"Runner.Listener", "Runner.Worker", "dotnet", "containerd", "dockerd", "containerd-shim", "provjobd",
                 "perf", "taskstats_liste", "sudo", "taskset", "systemd", "systemd-journal", "systemd-udevd",
                 "snapd", "cron", "rsyslogd", "walinuxagent", "python3-walinux", "hv_kvp_daemon", "chronyd",
                 "multipathd", "dbus-daemon", "polkitd", "networkd-dispat", "systemd-resolve", "systemd-network",
                 "sshd", "mono", "node", "Hosted Compute", "sleep", "gzip", "grep", "date", "tee", "sed"}
PHASE_ROOT = {"build-j8-warm": "make", "build-j8-cold": "make", "build-j1-warm": "make", "dkms": "dkms",
              "clamscan": "clamscan", "ffmpeg": "ffmpeg", "handbrake": "HandBrakeCLI", "train": "python3",
              "tracker": "dbus-run-sessio"}
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


# ---- the tree --------------------------------------------------------------

def build_tree(phase, segs, forks, ts_rows, meas_cpu):
    """Return (root_tid, tree_tids, tid2pid, role_of_pid, parent_of_pid, outside_by_comm).

    The root is the earliest thread on the measured CPU whose comm (at any row) is the phase's program and whose
    parent, per the fork rows, never ran on the measured CPU; the tree is every descendant by the fork rows plus
    the root. Roles: comm at exit (taskstats tgid row, else the last comm seen in perf's exit row or a segment)."""
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
    cpu_tids = {s.tid for s in on_cpu}
    root_comm = PHASE_ROOT.get(phase, phase.split("-")[0])
    root = None
    for s in on_cpu:
        if s.comm == root_comm and parent.get(s.tid) not in cpu_tids:
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
    role = {}
    for r in ts_rows:
        if r["type"] == "tgid":
            role[r["id"]] = r["comm"]
    for t in tree:
        pid = tid2pid.get(t, t)
        role.setdefault(pid, last_comm.get(t, "?"))
    parent_pid = {}
    for t in tree:
        pid = tid2pid.get(t, t)
        p = parent.get(t)
        if p is not None and pid == t:   # a process (its main thread): parent process = the forking thread's pid
            parent_pid[pid] = tid2pid.get(p, p)
    for r in ts_rows:
        if r["type"] == "tgid" and r["id"] in tree and r["id"] not in parent_pid:
            parent_pid[r["id"]] = r["ppid"]
    out_by_comm = defaultdict(lambda: [0, 0.0])
    for s in on_cpu:
        if s.tid not in tree:
            out_by_comm[s.comm][0] += 1; out_by_comm[s.comm][1] += s.run
    return root, tree, tid2pid, role, parent_pid, {k: {"rows": v[0], "run_ms": round(v[1], 3)} for k, v in out_by_comm.items()}


def jobs_of(tree, tid2pid, role, parent_pid, forks, exits, ts_by_pid):
    """make jobs (D2): a non-make child process of a make process, with its subtree; fork and last-exit times."""
    children = defaultdict(list)
    for pid, pp in parent_pid.items():
        children[pp].append(pid)
    fork_t = {c: t for t, _p, _pc, c, _cc in forks}
    def exit_t(pid):
        if pid in exits:
            return exits[pid][0]
        r = ts_by_pid.get(pid)
        return None if r is None else r["_t_exit"]
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
            jobs.append({"root": c, "make": m, "members": members, "roles": sorted(role.get(x, "?") for x in members),
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

def role_shapes(tree, tid2pid, role, segs, wakeups, meas_cpu, ts_by_pid):
    """Per role: wakes (run per wake), off-CPU intervals after each wake by kind, per-process CPU and delays."""
    rows = [s for s in segs if s.tid in tree and s.cpu == meas_cpu]
    wakes, merged = merge_resumes(rows, wakeups)
    by_tid = defaultdict(list)
    for w in wakes:
        by_tid[w.tid].append(w)
    per_role = defaultdict(lambda: {"run_ms": [], "off_D_ms": [], "off_S_ms": [], "off_R_ms": [], "wakes": 0, "threads": set(),
                                    "procs": set(), "cpu_us": [], "blkio_ns": [], "blkio_count": [], "cpu_delay_ns": [],
                                    "etime_us": [], "nvcsw": [], "nivcsw": [], "perf_run_ms_by_pid": defaultdict(float)})
    for tid, ws in by_tid.items():
        pid = tid2pid.get(tid, tid)
        r = per_role[role.get(pid, "?")]
        r["threads"].add(tid); r["procs"].add(pid); r["wakes"] += len(ws)
        for a, b in zip(ws, ws[1:]):
            r["run_ms"].append(a.run)
            off = (b.t_wake - a.t_end) * 1000.0   # from the previous wake's last sched-out to the wakeup
            kind = "off_D_ms" if a.state.startswith("D") else "off_S_ms" if a.state.startswith("S") else "off_R_ms"
            r[kind].append(max(off, 0.0))
        r["run_ms"].append(ws[-1].run)
        r["perf_run_ms_by_pid"][pid] += sum(w.run for w in ws)
    for pid in set(tid2pid.get(t, t) for t in tree):
        t = ts_by_pid.get(pid)
        if t is None:
            continue
        r = per_role[role.get(pid, "?")]
        r["procs"].add(pid)
        r["cpu_us"].append(t["utime_us"] + t["stime_us"]); r["blkio_ns"].append(t["blkio_delay_ns"]); r["blkio_count"].append(t["blkio_count"])
        r["cpu_delay_ns"].append(t["cpu_delay_ns"]); r["etime_us"].append(t["etime_us"]); r["nvcsw"].append(t["nvcsw"]); r["nivcsw"].append(t["nivcsw"])
    out = {}
    for name, r in per_role.items():
        cross = []
        for pid, ms in r["perf_run_ms_by_pid"].items():
            t = ts_by_pid.get(pid)
            if t is not None and (t["utime_us"] + t["stime_us"]) > 0:
                cross.append(ms * 1000.0 / (t["utime_us"] + t["stime_us"]))
        out[name] = {"processes": len(r["procs"]), "threads": len(r["threads"]), "wakes": r["wakes"],
                     "run_per_wake_ms": dist(r["run_ms"]),
                     "off_after_D_ms": dist(r["off_D_ms"]), "off_after_S_ms": dist(r["off_S_ms"]), "off_after_R_ms": dist(r["off_R_ms"]),
                     "cpu_per_process_us": dist(r["cpu_us"]), "etime_per_process_us": dist(r["etime_us"]),
                     "blkio_delay_per_process_ns": dist(r["blkio_ns"]), "blkio_count_per_process": dist(r["blkio_count"]),
                     "cpu_delay_per_process_ns": dist(r["cpu_delay_ns"]),
                     "nvcsw_per_process": dist(r["nvcsw"]), "nivcsw_per_process": dist(r["nivcsw"]),
                     "perf_over_taskstats_cpu": dist(cross)}
    return out, merged, len(rows), len(wakes)


def dispatch(tree, tid2pid, role, segs, forks, meas_cpu, ts_by_pid):
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
        t = ts_by_pid.get(tid2pid.get(tid, tid))
        if t is not None and fts:
            cross.append((t["utime_us"] + t["stime_us"]) / len(fts) / 1000.0)
    return {"per_dispatch_ms": dist(per_dispatch), "makes": len(forks_by), "forks": sum(len(v) for v in forks_by.values()),
            "cpu_per_fork_ms_by_make": dist(cross)}


def batch(tree, tid2pid, role, segs, wakeups, meas_cpu, ts_by_pid, span_s):
    """The batch programs: saturation, thread share, wait shares over the tree."""
    rows = [s for s in segs if s.tid in tree and s.cpu == meas_cpu]
    run_by_tid = defaultdict(float)
    for s in rows:
        run_by_tid[s.tid] += s.run
    total_run_ms = sum(run_by_tid.values())
    dominant = max(run_by_tid.values()) if run_by_tid else 0.0
    cpu_us = sum(t["utime_us"] + t["stime_us"] for pid, t in ts_by_pid.items() if pid in set(tid2pid.get(x, x) for x in tree))
    blkio = sum(t["blkio_delay_ns"] for pid, t in ts_by_pid.items() if pid in set(tid2pid.get(x, x) for x in tree))
    return {"perf_run_ms": round(total_run_ms, 1), "phase_span_s": round(span_s, 2),
            "saturation_perf": round(total_run_ms / 1000.0 / span_s, 4) if span_s else None,
            "taskstats_cpu_s": round(cpu_us / 1e6, 3), "saturation_taskstats": round(cpu_us / 1e6 / span_s, 4) if span_s else None,
            "threads_with_runs": len(run_by_tid), "dominant_thread_share": round(dominant / total_run_ms, 4) if total_run_ms else None,
            "blkio_delay_s": round(blkio / 1e9, 4)}


# ---- driver ----------------------------------------------------------------

def analyze_phase(D, phase, meas_cpu, edges):
    base = os.path.join(D, f"perf.{phase}")
    th, wk, fk, ts = base + ".timehist.txt.gz", base + ".wakeups.txt.gz", base + ".forks.txt.gz", os.path.join(D, f"taskstats.{phase}.tsv")
    if not all(os.path.exists(p) for p in (th, wk, fk, ts)):
        return {"missing": [p for p in (th, wk, fk, ts) if not os.path.exists(p)]}
    segs = load_segments(th); wakeups = load_wakeups(wk); forks, exits = load_forks(fk); ts_rows, trailer = load_taskstats(ts)
    # taskstats exit time on the perf clock: recv_mono_ns is CLOCK_MONOTONIC, as is perf's -k CLOCK_MONOTONIC
    ts_by_pid = {}
    for r in ts_rows:
        if r["type"] == "tgid":
            r["_t_exit"] = r["recv_mono_ns"] / 1e9
            ts_by_pid[r["id"]] = r
    root, tree, tid2pid, role, parent_pid, out_by_comm = build_tree(phase, segs, forks, ts_rows, meas_cpu)
    e = edges.get(phase, {})
    span_s = (e["end"] - e["start"]) / 1e9 if "start" in e and "end" in e else (segs[-1].t_end - segs[0].t_in if segs else 0.0)
    res = {"root_tid": root, "root_comm": role.get(tid2pid.get(root, root)) if root is not None else None,
           "tree_threads": len(tree), "tree_processes": len(set(tid2pid.get(t, t) for t in tree)),
           "taskstats_rows": len(ts_rows), "taskstats_trailer": trailer, "fork_rows": len(forks), "exit_rows": len(exits),
           "phase_span_s": round(span_s, 2),
           "outside_on_measured_cpu": dict(sorted(out_by_comm.items(), key=lambda kv: -kv[1]["run_ms"])[:25])}
    roles, merged, n_rows, n_wakes = role_shapes(tree, tid2pid, role, segs, wakeups, meas_cpu, ts_by_pid)
    res["segments_in_tree"] = n_rows; res["wakes_in_tree"] = n_wakes; res["resumes_merged"] = merged
    res["roles"] = dict(sorted(roles.items(), key=lambda kv: -(kv[1]["cpu_per_process_us"].get("sum") or 0)))
    role_counts = defaultdict(int)
    for pid in set(tid2pid.get(t, t) for t in tree):
        role_counts[role.get(pid, "?")] += 1
    res["processes_by_role"] = dict(sorted(role_counts.items(), key=lambda kv: -kv[1]))
    if PHASE_ROOT.get(phase) in ("make", "dkms"):
        jobs, makes = jobs_of(tree, tid2pid, role, parent_pid, forks, exits, ts_by_pid)
        shapes = defaultdict(int)
        for j in jobs:
            shapes[" ".join(j["roles"])] += 1
        res["jobs"] = {"count": len(jobs), "makes": len(makes), "concurrency": concurrency(jobs),
                       "members_per_job": dist([len(j["members"]) for j in jobs]),
                       "job_lifetime_ms": dist([(j["end"] - j["start"]) * 1000.0 for j in jobs if j["start"] is not None and j["end"] is not None]),
                       "shapes": dict(sorted(shapes.items(), key=lambda kv: -kv[1])[:20])}
        res["dispatch"] = dispatch(tree, tid2pid, role, segs, forks, meas_cpu, ts_by_pid)
    else:
        res["batch"] = batch(tree, tid2pid, role, segs, wakeups, meas_cpu, ts_by_pid, span_s)
    return res


def load_edges(D):
    edges = defaultdict(dict)
    p = os.path.join(D, "edges.jsonl")
    if os.path.exists(p):
        for line in open(p):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            edges[e["phase"]][e["edge"]] = e["mono_ns"]
    return edges


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir"); ap.add_argument("--phase", action="append")
    ap.add_argument("--json"); ap.add_argument("--meas-cpu", type=int)
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
        json.dump(out, open(args.json, "w"), indent=1)
    for ph, r in out["phases"].items():
        if "missing" in r:
            print(f"{ph}: missing {r['missing']}"); continue
        print(f"{ph}: root {r['root_comm']}[{r['root_tid']}] tree {r['tree_processes']} procs / {r['tree_threads']} threads, "
              f"span {r['phase_span_s']} s, segments {r['segments_in_tree']} wakes {r['wakes_in_tree']} merged {r['resumes_merged']}, "
              f"taskstats rows {r['taskstats_rows']} enobufs {r['taskstats_trailer'].get('enobufs')}")
        for name, rr in list(r["roles"].items())[:12]:
            c = rr["cpu_per_process_us"]
            print(f"  {name:16s} procs {rr['processes']:5d} wakes {rr['wakes']:7d} run/wake p50 {rr['run_per_wake_ms'].get('p50')} ms "
                  f"cpu/proc p50 {c.get('p50')} us  blkio/proc p50 {rr['blkio_delay_per_process_ns'].get('p50')} ns  perf/ts {rr['perf_over_taskstats_cpu'].get('p50')}")
        if "jobs" in r:
            j = r["jobs"]
            print(f"  jobs {j['count']} makes {j['makes']} concurrency max {j['concurrency']['max']} mean {j['concurrency']['mean_busy']} "
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
