#!/usr/bin/env python3
"""The reading of 9.10's upgrade probe (9.10 changelog D165–D167; method
_dev/research/jioh/task-9.10-scenarios-timelines/campaign/session-upgrade/method.md §6).

  upgrade_probe.py <run-dir> [--json out.json]

One recording holds three windows on the trace's clock (`edges.mono.jsonl`): the blanked session (`pre`), the
upgrade unit started through pid 1 (`job`), the session after it (`post`). Two readings:

  - new processes: every process that runs in the recording and is none of these — in the census taken before the
    recording, in the job's tree, the harness's, a kernel thread — with its name, its execs, the window it first runs
    in, and its parent chain up to its first ancestor in that census; and every process a later census holds that
    the first does not;
  - the entries' work: per 9.9 instance (census.py's ENTRIES), the CPU and the runs in each window, each as a rate.

The job's tree is every process pid 1 forks inside `job` that executes apt-helper or apt.systemd.daily (the unit's
ExecStartPre and ExecStart), and its descendants; the harness is the run's shell (`harness.pid` in report.kv) and its
descendants. The trace's rows are 9.9's (`analyze.load_trace`), its fork and exit rows 9.6's (`build.analyze`), its
exec rows the background family's.
"""

import argparse
import json
import os
import re
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.build.analyze import load_forks  # noqa: E402
from meas.session.analyze import KTHREAD_NAME, load_trace  # noqa: E402

EXEC = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_exec:\s+filename=(.*?)\s+pid=(\d+)\s+old_pid=(\d+)")
JOB_EXECS = ("apt-helper", "apt.systemd.daily")   # the unit's ExecStartPre and ExecStart
WINDOWS = ("pre", "job", "post")
NAME = "upgrade-probe"


def first(D, *names):
    return next((os.path.join(D, n) for n in names if os.path.exists(os.path.join(D, n))), None)


def read_kv(D):
    kv = {}
    p = os.path.join(D, "report.kv")
    if os.path.exists(p):
        for line in open(p):
            k, sep, v = line.rstrip("\n").partition("=")
            if sep:
                kv[k] = v
    return kv


def windows(D):
    """window -> (start s, end s) on CLOCK_MONOTONIC, from edges.mono.jsonl."""
    out = {}
    for line in open(os.path.join(D, "edges.mono.jsonl")):
        if line.strip():
            e = json.loads(line)
            out.setdefault(e["phase"], [None, None])[0 if e["edge"] == "start" else 1] = e["mono_ns"] / 1e9
    return {w: tuple(v) for w, v in out.items()}


def load_execs(path):
    """[(t, pid, filename)] in time order."""
    out = []
    with (__import__("gzip").open(path, "rt") if path.endswith(".gz") else open(path)) as handle:
        for line in handle:
            m = EXEC.match(line)
            if m:
                out.append((float(m.group(1)), int(m.group(3)), m.group(2)))
    return sorted(out)


def census(D, label):
    p = os.path.join(D, f"census.{label}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def window_of(t, wins):
    return next((w for w in WINDOWS if w in wins and wins[w][0] is not None and wins[w][0] <= t < (wins[w][1] or t + 1)),
                "outside")


def tree(forks, rows_pid):
    """child process -> (fork time, parent process). A fork row's child is a new process unless the trace shows it as
    a thread of another process (its rows carry a pid other than its tid)."""
    parent = {}
    for t, ptid, _pcomm, ctid, _ccomm in forks:
        if rows_pid.get(ctid, ctid) != ctid:
            continue                                    # a thread
        parent.setdefault(ctid, (t, rows_pid.get(ptid, ptid)))
    return parent


def descendants(roots, parent):
    kids = {}
    for c, (_t, p) in parent.items():
        kids.setdefault(p, []).append(c)
    out, todo = set(), list(roots)
    while todo:
        x = todo.pop()
        if x in out:
            continue
        out.add(x)
        todo.extend(kids.get(x, ()))
    return out


def chain(pid, parent, known, limit=32):
    """The parent chain from `pid` up to its first ancestor in `known` (pid -> census record), that ancestor last."""
    out, x = [], pid
    for _ in range(limit):
        if x not in parent:
            return out, None
        x = parent[x][1]
        if x in known:
            return out, x
        out.append(x)
    return out, None


def read(D):
    kv = read_kv(D)
    wins = windows(D)
    rows_cpu, span = load_trace(first(D, f"perf.{NAME}.timehist.txt.gz", f"perf.{NAME}.timehist.txt"))
    forks_path = first(D, f"perf.{NAME}.forks.txt.gz", f"perf.{NAME}.forks.txt")
    forks, exits = load_forks(forks_path)
    execs = load_execs(forks_path)
    rows = [r for r, _cpu in rows_cpu]
    rows_pid = {r.tid: r.pid for r in rows}

    before = census(D, "probe.start") or {"procs": [], "instances": {}, "kthreads": []}
    known = {p["pid"]: p for p in before["procs"]}
    kthreads = set(before.get("kthreads") or [])
    parent = tree(forks, rows_pid)
    execs_of = {}
    for t, pid, f in execs:
        execs_of.setdefault(pid, []).append(f)
    comm_of = {}
    for r in rows:
        comm_of.setdefault(r.pid, r.comm)
    for _t, _ptid, _pcomm, ctid, ccomm in forks:
        comm_of.setdefault(ctid, ccomm)

    # the job's tree: pid 1's children inside `job` that execute the unit's commands, and their descendants
    j0, j1 = wins.get("job", (None, None))
    roots = [c for c, (t, p) in parent.items()
             if p == 1 and j0 is not None and j0 <= t <= (j1 or t)
             and any(f.rsplit("/", 1)[-1] in JOB_EXECS for f in execs_of.get(c, ()))]
    job = descendants(roots, parent)
    harness_pid = int(kv["harness.pid"]) if kv.get("harness.pid", "").isdigit() else None
    harness = descendants([harness_pid], parent) if harness_pid else set()
    # the harness's processes already in the census: those whose census parents lead to its shell
    for pid in known:
        x, seen = pid, set()
        while x in known and x not in seen and x != harness_pid:
            seen.add(x)
            x = known[x]["ppid"]
        if harness_pid and x == harness_pid:
            harness.add(pid)

    # every process that runs in the recording, outside the census, the job, the harness and the kernel
    first_run, cpu = {}, {}
    for r in rows:
        first_run.setdefault(r.pid, r.t_in)
        cpu[r.pid] = cpu.get(r.pid, 0.0) + r.run
    new = []
    for pid in sorted(first_run, key=first_run.get):
        if pid in known or pid in job or pid in harness or pid in kthreads or pid == harness_pid:
            continue
        comm = comm_of.get(pid, "")
        if KTHREAD_NAME.match(comm) or (pid in parent and parent[pid][1] == 2):
            continue
        up, anc = chain(pid, parent, known)
        if anc is not None and anc in harness:
            continue
        a = known.get(anc) or {}
        new.append({"pid": pid, "comm": comm, "execs": execs_of.get(pid, []), "window": window_of(first_run[pid], wins),
                    "first_s_from_job": round(first_run[pid] - j0, 3) if j0 is not None else None,
                    "cpu_ms": round(cpu[pid], 3), "chain": [{"pid": x, "comm": comm_of.get(x, "")} for x in up],
                    "ancestor": {"pid": anc, "comm": a.get("comm"), "cgroup": a.get("cgroup"), "cmd": a.get("cmd")}
                    if anc is not None else None})

    # every process a later census holds that the first does not, outside the job and the harness
    later = []
    for label in ("job.start", "job.end", "probe.end"):
        c = census(D, label)
        for p in (c or {}).get("procs", []):
            if p["pid"] in known or p["pid"] in job or p["pid"] in harness or p.get("kthread"):
                continue
            if any(x["pid"] == p["pid"] for x in later):
                continue
            later.append({"census": label, "pid": p["pid"], "comm": p["comm"], "cmd": p["cmd"], "cgroup": p["cgroup"],
                          "ppid": p["ppid"]})

    # the entries' work per window: CPU and runs of every thread of each instance's processes
    entries = {}
    for e, by_i in (before.get("instances") or {}).items():
        for i, pids in by_i.items():
            ps = set(pids)
            out = {}
            for w in WINDOWS:
                if w not in wins or None in wins[w]:
                    continue
                a, b = wins[w]
                sel = [r for r in rows if r.pid in ps and a <= r.t_end < b]
                ms = sum(r.run for r in sel)
                out[w] = {"s": round(b - a, 3), "cpu_ms": round(ms, 3), "runs": len(sel),
                          "cpu_ms_per_s": round(ms / (b - a), 4) if b > a else None,
                          "runs_per_s": round(len(sel) / (b - a), 4) if b > a else None}
            entries.setdefault(e, {})[i] = {"pids": sorted(ps), **out}

    job_rows = [r for r in rows if r.pid in job]
    return {
        "windows": {w: {"start": v[0], "end": v[1]} for w, v in wins.items()},
        "trace_span": span,
        "job": {"roots": [{"pid": r, "execs": execs_of.get(r, [])} for r in roots], "processes": len(job),
                "cpu_ms": round(sum(r.run for r in job_rows), 3),
                "comms": sorted({r.comm for r in job_rows})},
        "harness": {"pid": harness_pid, "processes": len(harness)},
        "new_processes": new,
        "new_in_later_census": later,
        "entries": entries,
        "unit": {k: kv.get(k) for k in ("upgrade.unit.result", "upgrade.unit.status", "upgrade.uu.all_installed",
                                        "upgrade.reboot_required", "upgrade.glibc.not_at_new")},
    }


def summary(r):
    out = [f"job: {len(r['job']['roots'])} roots, {r['job']['processes']} processes, {r['job']['cpu_ms'] / 1000:.3f} s CPU"]
    out.append(f"unit: {r['unit']}")
    out.append(f"new processes outside the census, the job and the harness: {len(r['new_processes'])}")
    for n in r["new_processes"]:
        anc = n["ancestor"] or {}
        out.append(f"  {n['window']:<7} {n['comm']:<16} pid {n['pid']:<7} {n['cpu_ms']:9.3f} ms  "
                   f"{' '.join(n['execs'][-1:]) or '-'}  <- {' <- '.join(x['comm'] for x in n['chain']) or '.'} "
                   f"<- {anc.get('comm')} [{anc.get('cgroup')}]")
    out.append(f"new in a later census: {len(r['new_in_later_census'])}")
    for n in r["new_in_later_census"]:
        out.append(f"  {n['census']:<10} {n['comm']:<16} pid {n['pid']:<7} {n['cgroup']}  {n['cmd'][:80]}")
    out.append("entries (cpu ms/s, runs/s): " + "  ".join(WINDOWS))
    for e, by_i in r["entries"].items():
        for i, v in by_i.items():
            cells = "  ".join(f"{v[w]['cpu_ms_per_s']}/{v[w]['runs_per_s']}" if w in v else "-" for w in WINDOWS)
            out.append(f"  {e}/{i}: {cells}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--json")
    a = ap.parse_args()
    r = read(a.run_dir)
    if a.json:
        json.dump(r, open(a.json, "w"), indent=1)
    print(summary(r))


if __name__ == "__main__":
    main()
