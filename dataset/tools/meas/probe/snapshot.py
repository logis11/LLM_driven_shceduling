#!/usr/bin/env python3
"""Snapshot one process tree's CPU, threads and context switches from /proc.

probe tooling for the 9.5 campaign (research-slice D3): prints one JSON
object for the process whose comm or cmdline matches PATTERN, summed over
its threads and its descendants. Read twice around a phase to get deltas.
Each process also carries its cgroup and, per thread, the counters the
untraced control reads (`_dev/docs/spec/jioh/task-9.5-untraced-control.md`,
decision 9): the runtime, run-queue wait and slice count of
task/<tid>/schedstat, the voluntary and involuntary switches of
task/<tid>/status, and the start time of task/<tid>/stat.
"""

import json
import os
import re
import sys
import time

CLK = os.sysconf("SC_CLK_TCK")
PROC = "/proc"


def read(path):
    try:
        with open(path) as handle:
            return handle.read()
    except OSError:
        return ""


def pids():
    return [int(p) for p in os.listdir(PROC) if p.isdigit()]


def cmdline(pid):
    return read(f"{PROC}/{pid}/cmdline").replace("\0", " ").strip()


def stat_fields(path):
    raw = read(path)
    if not raw:
        return None
    close = raw.rfind(")")
    comm = raw[raw.find("(") + 1:close]
    rest = raw[close + 2:].split()
    return comm, rest


def parent(pid):
    fields = stat_fields(f"{PROC}/{pid}/stat")
    return int(fields[1][1]) if fields else None


def matching_roots(pattern):
    rx = re.compile(pattern)
    return [p for p in pids() if rx.search(cmdline(p)) or rx.search(
        read(f"{PROC}/{p}/comm").strip())]


def descendants(roots):
    roots = set(roots)
    found = set(roots)
    changed = True
    while changed:
        changed = False
        for p in pids():
            if p in found:
                continue
            par = parent(p)
            if par in found:
                found.add(p)
                changed = True
    return sorted(found)


def switches(pid, tid):
    vol = nonvol = 0
    for line in read(f"{PROC}/{pid}/task/{tid}/status").splitlines():
        if line.startswith("voluntary_ctxt_switches"):
            vol = int(line.split()[1])
        elif line.startswith("nonvoluntary_ctxt_switches"):
            nonvol = int(line.split()[1])
    return vol, nonvol


def cgroup(pid):
    """The process's cgroup v2 path (the `0::` line)."""
    return next((ln[3:] for ln in read(f"{PROC}/{pid}/cgroup").splitlines() if ln.startswith("0::")), "")


def task_counters(pid, tid):
    """One thread's counters, or None when it left mid-read: run_ns, wait_ns and slices are task/<tid>/schedstat's
    three fields (fs/proc/base.c proc_pid_schedstat: se.sum_exec_runtime, sched_info.run_delay, sched_info.pcount),
    vol and invol the switches of task/<tid>/status, start_ticks field 22 of task/<tid>/stat."""
    sched = read(f"{PROC}/{pid}/task/{tid}/schedstat").split()
    fields = stat_fields(f"{PROC}/{pid}/task/{tid}/stat")
    if len(sched) < 3 or not fields:
        return None
    comm, rest = fields
    vol, nonvol = switches(pid, tid)
    return {"tid": int(tid), "comm": comm, "start_ticks": int(rest[19]), "run_ns": int(sched[0]),
            "wait_ns": int(sched[1]), "slices": int(sched[2]), "vol": vol, "invol": nonvol}


def snapshot(pattern, exclude=None):
    exclude = re.compile(exclude) if exclude else None
    roots = [p for p in matching_roots(pattern)
             if p != os.getpid() and not (exclude and exclude.search(cmdline(p)))]
    procs = descendants(roots)
    out = {"t_mono": time.monotonic(), "pattern": pattern, "roots": roots,
           "n_procs": len(procs), "n_threads": 0, "cpu_s": 0.0,
           "vol_switches": 0, "nonvol_switches": 0, "procs": []}
    for p in procs:
        fields = stat_fields(f"{PROC}/{p}/stat")
        if not fields:
            continue
        comm, rest = fields
        cpu = (int(rest[11]) + int(rest[12])) / CLK
        tids = [int(t) for t in os.listdir(f"{PROC}/{p}/task")] if os.path.isdir(f"{PROC}/{p}/task") else []
        vol = nonvol = 0
        for t in tids:
            v, n = switches(p, t)
            vol += v
            nonvol += n
        out["n_threads"] += len(tids)
        out["cpu_s"] += cpu
        out["vol_switches"] += vol
        out["nonvol_switches"] += nonvol
        out["procs"].append({"pid": p, "comm": comm, "threads": len(tids),
                             "cpu_s": cpu, "cmd": cmdline(p)[:120], "cgroup": cgroup(p),
                             "tasks": [c for c in (task_counters(p, t) for t in sorted(tids)) if c]})
    return out


def main():
    print(json.dumps(snapshot(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)))


if __name__ == "__main__":
    main()
