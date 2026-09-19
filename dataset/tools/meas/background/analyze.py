#!/usr/bin/env python3
"""Analyse one run directory of the 9.7 background campaign (run.sh output) by the
rules fixed in the method before the run (campaign/method.md §5; changelog D13,
D15).

analyze.py <run-dir> [--phase NAME ...] [--json out.json] [--samples]

Per phase: the process tree rooted at the phase's command on the measured CPU
(fork rows from perf script), the program's processes by the file they executed
(exec rows; borg, 7z, SteamCMD's own binary rather than its shell wrappers),
and for every thread of those processes: its wakes (a timehist row is a
segment; a segment is a wake when a wakeup row for the thread lies between its
previous schedule-out and this schedule-in, else a resume merged into the
preceding wake — 9.5 D21), the run of each wake, and the off-CPU interval after
each wake, classified (§5 "Shape"):
  disk — the schedule-out state is uninterruptible and the kernel's
    sched_stat_iowait row for the thread lies between its schedule-out and its
    next schedule-in: the sleep was spent waiting on I/O (method §9, the
    dry-run entry); in records without schedstats, the earlier reading — the
    process's block-I/O delay (taskstats) equal to its uninterruptible time
    within TOLERANCE — with the process's coverage kept as the cross-check;
  uninterruptible — uninterruptible, not so marked;
  network — by the matching rule on the `perf trace` rows (nettrace.py), in the
    traced SteamCMD phases;
  sleep — otherwise, interruptible;
  runnable — a runnable wait (neither).
Bytes per wake: after each network wait, the bytes the thread's socket
receives return from the next schedule-in until it next leaves the CPU into a
network wait. The transfer rate: the socket receives' payload from the first
receive that returns data to the last, per second of that span, beside the wire
bytes through the shaper. Per process: the CPU total as the sum of its perf run segments on
the measured CPU, with taskstats' CPU beside it (9.6 method, dry-run-2
amendment (a)). Every thread's quantiles are kept separately (D13), keyed
`comm#rank` (rank by CPU among the program's threads of that comm), and pooled
over all the program's threads. Rows on the measured CPU outside the tree are
counted by comm, never folded in.
"""

import argparse
import gzip
import json
import os
import re
import statistics
import sys
from bisect import bisect_left
from collections import defaultdict

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.build import analyze as _build   # noqa: E402  9.6's loaders and wake rule
from meas.background import nettrace  # noqa: E402
from meas.stability import TOLERANCE  # noqa: E402
load_segments, load_wakeups, load_forks = _build.load_segments, _build.load_wakeups, _build.load_forks
load_taskstats, process_records, merge_resumes = _build.load_taskstats, _build.process_records, _build.merge_resumes
load_edges, outside, pct, dist, QUANTILE_PROBS = _build.load_edges, _build.outside, _build.pct, _build.dist, _build.QUANTILE_PROBS

IOWAIT = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_stat_iowait:\s+comm=.*?\s+pid=(\d+)\s+delay=(\d+)")
EXEC = re.compile(r"^\s*(\d+\.\d+):\s+sched:sched_process_exec:\s+filename=(.*?)\s+pid=(\d+)\s+old_pid=(\d+)")
ROOT_COMMS = {"borg": ("borg",), "7z": ("7z", "7zz"), "steamcmd": ("steamcmd",)}
CLASSES = ("disk", "uninterruptible", "network", "sleep", "runnable")


def job_of(phase):
    for job, prefix in (("borg", "borg"), ("7z", "7z"), ("steamcmd", "steam")):
        if phase.startswith(prefix):
            return job
    return None


def is_program(job, filename, comm):
    """The program's own processes: borg's (a Python script, executed as /usr/bin/borg), 7-Zip's, and SteamCMD's
    binary — not /usr/games/steamcmd or steamcmd.sh, the shell wrappers that start it. Without an exec row, by comm."""
    if filename:
        base = filename.rsplit("/", 1)[-1]
        if job == "borg":
            return base == "borg"
        if job == "7z":
            return base in ("7z", "7zz")
        if job == "steamcmd":
            return base == "steamcmd" and not filename.startswith("/usr/games/")
        return False
    return comm in ROOT_COMMS.get(job, ())


def load_exec_rows(path):
    """Exec rows in the forks file, in time order: (t, pid, filename)."""
    out = []
    with _build.open_text(path) as handle:
        for line in handle:
            m = EXEC.match(line)
            if m:
                out.append((float(m.group(1)), int(m.group(3)), m.group(2)))
    out.sort()
    return out


def load_execs(path):
    """pid -> the last file it executed."""
    return {pid: f for _t, pid, f in load_exec_rows(path)}


def launched_root(job, exec_rows):
    """The process phase.sh launched: the earliest one that executed taskset and then the job's command (borg, 7z, or
    /usr/games/steamcmd, which becomes a bash running steamcmd.sh before it starts SteamCMD's binary)."""
    last = {}
    for _t, pid, f in exec_rows:
        if last.get(pid, "").rsplit("/", 1)[-1] == "taskset" and f.rsplit("/", 1)[-1] in ROOT_COMMS.get(job, ()):
            return pid
        last[pid] = f
    return None


def load_exec_classes(path):
    """filename -> ELF32 | ELF64 | script | missing (run.sh, execs.<phase>.tsv)."""
    out = {}
    if os.path.exists(path):
        for line in open(path):
            name, _, cls = line.rstrip("\n").rpartition("\t")
            if name:
                out[name] = cls
    return out


def read_kv(path):
    try:
        return dict(line.rstrip("\n").split("=", 1) for line in open(path) if "=" in line)
    except OSError:
        return {}


# ---- the tree -----------------------------------------------------------------

def phase_tree(job, segs, forks, meas_cpu, root=None):
    """(root tid, tree tids, tid -> pid, last comm per tid, outside rows by comm). The root is the process phase.sh
    launched (launched_root) when the exec rows name it, else the earliest thread on the measured CPU whose comm is the
    job's program; the tree is it and every descendant by the fork rows (which carry threads as well as processes)."""
    on_cpu = [s for s in segs if s.cpu == meas_cpu]
    children = defaultdict(list)
    for _t, p, _pc, c, _cc in forks:
        children[p].append(c)
    tid2pid, last_comm = {}, {}
    for s in segs:
        tid2pid[s.tid] = s.pid
        last_comm[s.tid] = s.comm
    if root is None:
        root = next((s.tid for s in on_cpu if s.comm in ROOT_COMMS.get(job, ())), None)
    if root is None:
        root = next((s.tid for s in on_cpu if not outside(s.comm)), None)
    tree, stack = set(), ([root] if root is not None else [])
    while stack:
        t = stack.pop()
        if t not in tree:
            tree.add(t)
            stack.extend(children.get(t, ()))
    out_by_comm = defaultdict(lambda: [0, 0.0])
    for s in on_cpu:
        if s.tid not in tree:
            out_by_comm[s.comm][0] += 1
            out_by_comm[s.comm][1] += s.run
    return root, tree, tid2pid, last_comm, {k: {"rows": v[0], "run_ms": round(v[1], 3)} for k, v in out_by_comm.items()}


# ---- wakes and intervals ---------------------------------------------------------

def thread_wakes(rows, wakeups, check=None):
    """Per thread: wakes (sorted) and the intervals between consecutive wakes as dicts
    {tid, t0 (schedule-out), t1 (wakeup), us, state, next_in, next_end}. check: the wake rule's disagreements of row
    and state (merge_resumes)."""
    wakes, merged = merge_resumes(sorted(rows, key=lambda r: r.t_in), wakeups, check)
    per = defaultdict(list)
    for w in wakes:
        per[w.tid].append(w)
    intervals = {}
    for tid, ws in per.items():
        iv = []
        for a, b in zip(ws, ws[1:]):
            iv.append({"tid": tid, "t0": a.t_end, "t1": b.t_wake, "us": max(b.t_wake - a.t_end, 0.0) * 1e6,
                       "state": a.state, "next_in": b.t_in, "next_end": b.t_end})
        intervals[tid] = iv
    return per, intervals, merged


def disk_accounting(intervals, tid2pid, recs):
    """pid -> {d_state_ns, blkio_ns, coverage, accounted}: the process's uninterruptible off-CPU time against its
    block-I/O delay; accounted when they agree within TOLERANCE."""
    d_ns = defaultdict(float)
    for tid, iv in intervals.items():
        for x in iv:
            if x["state"].startswith("D"):
                d_ns[tid2pid.get(tid, tid)] += x["us"] * 1000.0
    out = {}
    for pid, d in d_ns.items():
        blk = (recs.get(pid) or {}).get("blkio_ns")
        cov = (blk / d) if (blk is not None and d > 0) else None
        out[pid] = {"d_state_ns": round(d), "blkio_ns": blk, "coverage": round(cov, 4) if cov is not None else None,
                    "accounted": cov is not None and abs(cov - 1.0) <= TOLERANCE}
    return out


def parse_iowait(lines):
    """tid -> sorted times of its sched_stat_iowait rows (perf script -F time,event,trace)."""
    out = defaultdict(list)
    for line in lines:
        m = IOWAIT.match(line)
        if m:
            out[int(m.group(2))].append(float(m.group(1)))
    for v in out.values():
        v.sort()
    return dict(out)


def iowait_marked(times, t0, t_in):
    """Whether a row lies between the schedule-out and the next schedule-in."""
    i = bisect_left(times, t0)
    return i < len(times) and times[i] <= t_in


def classify(intervals, tid2pid, disk, calls_by_tid=None, iowait=None):
    """Label every interval (in place) with its class and, for network waits, how the rule matched. iowait (tid ->
    sched_stat_iowait times): an uninterruptible wait is disk when its own row marks it; None: the process-level
    reading (records without schedstats)."""
    how = defaultdict(int)
    for tid, iv in intervals.items():
        tc = calls_by_tid.get(tid) if calls_by_tid else None
        pid = tid2pid.get(tid, tid)
        for x in iv:
            st = x["state"]
            if st.startswith("D") and (iowait_marked(iowait.get(tid, ()), x["t0"], x["next_in"]) if iowait is not None
                                       else disk.get(pid, {}).get("accounted")):
                x["class"] = "disk"
                continue
            if st.startswith("R"):
                x["class"] = "runnable"
                continue
            if tc is not None:
                ok, h = tc.network_wait(x["t0"], x["t1"], x["next_end"])
                how[h] += 1
                if ok:
                    x["class"], x["how"] = "network", h
                    continue
            x["class"] = "uninterruptible" if st.startswith("D") else "sleep"
    return dict(how)


def transfer_rate(calls, wire_bytes=None):
    """The download's rate while data flows (method §9, the dry-run entry): the bytes the socket receives return, per
    second from the first receive that returns data, and the median of those per-second rates weighted by their bytes
    (D11's statistic), so the seconds of the login connection's trickle weigh by what they carry; beside it the wire
    bytes through the shaper over the payload."""
    rx = sorted((c.t_exit, c.nbytes) for c in calls if c.kind == "recv" and c.nbytes and c.nbytes > 0)
    if len(rx) < 2 or rx[-1][0] <= rx[0][0]:
        return None
    t0 = rx[0][0]
    bins = [0] * (int(rx[-1][0] - t0) + 1)
    for t, n in rx:
        bins[int(t - t0)] += n
    total, acc = sum(bins), 0
    for b in sorted(bins):
        acc += b
        if acc * 2 >= total:
            break
    out = {"payload_bytes": total, "per_second_mbps": [round(x * 8 / 1e6, 1) for x in bins],
           "per_second_mbps_byte_weighted_median": round(b * 8 / 1e6, 1)}
    if wire_bytes:
        out["wire_over_payload"] = round(wire_bytes / total, 4)
    return out


def bytes_per_wake(intervals, calls_by_tid):
    """Per thread: after each network wait, the bytes its socket receives return from the next schedule-in until it
    next leaves the CPU into a network wait (or the phase ends). Returns (samples by tid, windows with a receive whose
    byte count is unknown)."""
    out, unknown = defaultdict(list), 0
    for tid, iv in intervals.items():
        tc = calls_by_tid.get(tid)
        nets = [x for x in iv if x.get("class") == "network"]
        if tc is None or not nets:
            continue
        for k, x in enumerate(nets):
            end = nets[k + 1]["t0"] if k + 1 < len(nets) else float("inf")
            got, unk = tc.received(x["next_in"], end)
            out[tid].append(got)
            unknown += bool(unk)
    return out, unknown


# ---- one phase -------------------------------------------------------------------

def analyze_phase(D, phase, meas_cpu, edges, kv=None):
    base = os.path.join(D, f"perf.{phase}")
    th, wk, fk, ts = base + ".timehist.txt.gz", base + ".wakeups.txt.gz", base + ".forks.txt.gz", os.path.join(D, f"taskstats.{phase}.tsv")
    if not all(os.path.exists(p) for p in (th, wk, fk, ts)):
        return {"missing": [os.path.basename(p) for p in (th, wk, fk, ts) if not os.path.exists(p)]}
    kv = kv if kv is not None else read_kv(os.path.join(D, "report.kv"))
    job = job_of(phase)
    segs, wakeups = load_segments(th), load_wakeups(wk)
    forks, _exits = load_forks(fk)
    exec_rows = load_exec_rows(fk)
    execs = {pid: f for _t, pid, f in exec_rows}
    ts_rows, trailer = load_taskstats(ts)
    recs = process_records(ts_rows)
    root, tree, tid2pid, last_comm, out_by_comm = phase_tree(job, segs, forks, meas_cpu, launched_root(job, exec_rows))
    pids = sorted({tid2pid.get(t, t) for t in tree})
    role = {pid: (recs[pid]["comm"] if pid in recs else last_comm.get(pid, "?")) for pid in pids}
    prog = [p for p in pids if is_program(job, execs.get(p), role.get(p))]
    prog_set = set(prog)
    rows = [s for s in segs if s.cpu == meas_cpu and s.tid in tree]
    wake_check = {}
    per_wakes, intervals, merged = thread_wakes(rows, wakeups, wake_check)
    disk = disk_accounting(intervals, tid2pid, recs)
    iowait = None
    if str(kv.get("sysctl.sched_schedstats")) == "1":   # the sched_stat_iowait rows sit in the forks file (run.sh)
        with gzip.open(fk, "rt") as handle:
            iowait = parse_iowait(handle)

    # the socket rows of a traced SteamCMD phase
    calls_by_tid, net = None, None
    tr = os.path.join(D, f"trace.{phase}.txt.gz")
    if job == "steamcmd" and os.path.exists(tr):
        classes = load_exec_classes(os.path.join(D, f"execs.{phase}.tsv"))
        compat = [p for p in prog if classes.get(execs.get(p)) == "ELF32"]
        assumed = False
        if not compat and not classes:   # no record of the binary's class: SteamCMD is a 32-bit program (D4)
            compat, assumed = list(prog), True
        raw = nettrace.load_rows(tr)
        pairs, unpaired = nettrace.pair(raw)
        calls, unknown = nettrace.decode(pairs, compat)
        calls = [c for c in calls if c.tid in tree]
        calls_by_tid = {tid: nettrace.ThreadCalls(cs) for tid, cs in nettrace.by_tid(calls).items()}
        kinds = defaultdict(int)
        for c in calls:
            kinds[c.name + ":" + c.kind] += 1
        net = {"trace_rows": len(raw), "calls_in_tree": len(calls), "unpaired": unpaired, "unknown_numbers": unknown,
               "compat_pids": compat, "compat_assumed": assumed, "calls_by_name_kind": dict(sorted(kinds.items())),
               "transfer": transfer_rate([c for c in calls if tid2pid.get(c.tid, c.tid) in prog_set],
                                         int(kv.get(f"shape.{phase}.through_ifb_bytes") or 0) or None)}
    prog_intervals = {t: iv for t, iv in intervals.items() if tid2pid.get(t, t) in prog_set}
    how = classify(prog_intervals, tid2pid, disk, calls_by_tid, iowait)
    bpw, bpw_unknown = bytes_per_wake(prog_intervals, calls_by_tid) if calls_by_tid else ({}, 0)
    if net is not None:
        net["network_rule"] = how
        net["bytes_windows_with_unknown_count"] = bpw_unknown

    # per thread of the program, keyed comm#rank
    run_by_tid = {tid: sum(w.run for w in ws) for tid, ws in per_wakes.items() if tid2pid.get(tid, tid) in prog_set}
    ranked = defaultdict(list)
    for tid in sorted(run_by_tid, key=lambda t: -run_by_tid[t]):
        ranked[last_comm.get(tid, "?")].append(tid)
    key_of = {tid: f"{comm}#{i + 1}" for comm, tids in ranked.items() for i, tid in enumerate(tids)}
    samples = {"all": {k: [] for k in ("run_us", "wait_us", "bytes_per_wake") + tuple(c + "_us" for c in CLASSES)}, "threads": {}}
    threads = {}
    for tid in sorted(run_by_tid, key=lambda t: -run_by_tid[t]):
        s = {"run_us": [w.run * 1000.0 for w in per_wakes[tid]], "wait_us": [x["us"] for x in prog_intervals.get(tid, [])],
             "bytes_per_wake": list(bpw.get(tid, []))}
        for c in CLASSES:
            s[c + "_us"] = [x["us"] for x in prog_intervals.get(tid, []) if x.get("class") == c]
        samples["threads"][key_of[tid]] = s
        for k, v in s.items():
            samples["all"][k].extend(v)
        threads[key_of[tid]] = {"tid": tid, "pid": tid2pid.get(tid, tid), "wakes": len(per_wakes[tid]),
                                "cpu_us": round(run_by_tid[tid] * 1000.0, 1),
                                **{k: dist(v) for k, v in s.items()}}

    # per process: CPU twice (perf segments on the measured CPU; taskstats)
    perf_cpu = defaultdict(float)
    for tid, ws in per_wakes.items():
        perf_cpu[tid2pid.get(tid, tid)] += sum(w.run for w in ws) * 1000.0
    procs = []
    for pid in pids:
        r = recs.get(pid, {})
        ts_us = r["cpu_ns"] / 1000.0 if r else None
        procs.append({"pid": pid, "role": role.get(pid), "exec": execs.get(pid), "program": pid in prog_set,
                      "threads": r.get("threads"), "perf_cpu_us": round(perf_cpu.get(pid, 0.0), 1),
                      "taskstats_cpu_us": round(ts_us, 1) if ts_us is not None else None,
                      "perf_over_taskstats": round(perf_cpu.get(pid, 0.0) / ts_us, 4) if ts_us else None,
                      "blkio_ns": r.get("blkio_ns"), "etime_us": r.get("etime_us"), "disk": disk.get(pid)})
    e = edges.get(phase, {})
    span_s = (e["end"] - e["start"]) / 1e9 if "start" in e and "end" in e else None
    prog_cpu = sum(p["perf_cpu_us"] for p in procs if p["program"])
    prog_ts = sum(p["taskstats_cpu_us"] or 0.0 for p in procs if p["program"])
    res = {"job": job, "root_tid": root, "root_comm": last_comm.get(root) if root is not None else None,
           "tree_processes": len(pids), "tree_threads": len(tree), "program_pids": prog,
           "program_exec": sorted({execs.get(p) for p in prog if execs.get(p)}),
           "cmd_wall_s": round(e["cmd_wall_s"], 3) if e.get("cmd_wall_s") is not None else None, "rc": e.get("rc"),
           "phase_span_s": round(span_s, 3) if span_s else None,
           "segments_in_tree": len(rows), "resumes_merged": merged, "wake_rule_row_disagrees": wake_check,
           "disk_rule": "per-wait (sched_stat_iowait)" if iowait is not None else "process total (taskstats)",
           "iowait_rows_in_tree": sum(len(v) for t, v in (iowait or {}).items() if t in tree),
           "taskstats_rows": len(ts_rows), "taskstats_trailer": trailer,
           "program_cpu_us": round(prog_cpu, 1), "program_taskstats_cpu_us": round(prog_ts, 1),
           "all": {k: dist(v) for k, v in samples["all"].items()}, "threads": threads, "processes": procs,
           "outside_on_measured_cpu": dict(sorted(out_by_comm.items(), key=lambda kv_: -kv_[1]["run_ms"])[:25]),
           "_samples": samples}
    cf = kv.get(f"cache.{phase}.fraction")
    if cf not in (None, ""):
        res["cached_fraction"] = float(cf)
    if net is not None:
        rx = kv.get(f"net.{phase}.rx_bytes")
        if rx not in (None, ""):
            net["rx_bytes"] = int(rx)
            if res["cmd_wall_s"]:
                net["achieved_mbps_counters"] = round(int(rx) * 8 / res["cmd_wall_s"] / 1e6, 2)
        res["network"] = net
    elif job == "steamcmd":
        rx = kv.get(f"net.{phase}.rx_bytes")
        if rx not in (None, "") and res["cmd_wall_s"]:
            res["network"] = {"rx_bytes": int(rx), "achieved_mbps_counters": round(int(rx) * 8 / res["cmd_wall_s"] / 1e6, 2)}
    return res


def phases_in(D):
    return [f[len("taskstats."):-len(".tsv")] for f in sorted(os.listdir(D))
            if f.startswith("taskstats.") and f.endswith(".tsv") and "smoke" not in f]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir"); ap.add_argument("--phase", action="append")
    ap.add_argument("--json"); ap.add_argument("--meas-cpu", type=int)
    ap.add_argument("--samples", action="store_true", help="keep the raw sample arrays in the JSON (for pooling)")
    args = ap.parse_args()
    D = args.run_dir
    report = json.load(open(os.path.join(D, "report.json"))) if os.path.exists(os.path.join(D, "report.json")) else {}
    meas_cpu = args.meas_cpu if args.meas_cpu is not None else int(report.get("pin.load_cpu", 3))
    edges, kv = load_edges(D), read_kv(os.path.join(D, "report.kv"))
    out = {"run_dir": D, "app": report.get("app"), "mode": report.get("mode"), "repeat": report.get("repeat"),
           "meas_cpu": meas_cpu, "phases": {}}
    for ph in args.phase or phases_in(D):
        out["phases"][ph] = analyze_phase(D, ph, meas_cpu, edges, kv)
    if args.json:
        if not args.samples:
            for r in out["phases"].values():
                r.pop("_samples", None)
        json.dump(out, open(args.json, "w"), indent=1)
    for ph, r in out["phases"].items():
        if "missing" in r:
            print(f"{ph}: missing {r['missing']}")
            continue
        a = r["all"]
        print(f"{ph}: root {r['root_comm']}[{r['root_tid']}] tree {r['tree_processes']} procs / {r['tree_threads']} threads; "
              f"program {r['program_pids']} {r['program_exec']}; cmd {r['cmd_wall_s']} s rc {r['rc']}; "
              f"CPU perf {r['program_cpu_us'] / 1e6:.3f} s taskstats {r['program_taskstats_cpu_us'] / 1e6:.3f} s; "
              f"run/wake p50 {a['run_us'].get('p50')} µs wait p50 {a['wait_us'].get('p50')} µs "
              + " ".join(f"{c} n {a[c + '_us']['n']}" for c in CLASSES)
              + (f"; cached {r['cached_fraction']}" if "cached_fraction" in r else ""))
        if "network" in r:
            print(f"  network {json.dumps({k: v for k, v in r['network'].items() if k != 'calls_by_name_kind'})}")
        for p in r["processes"]:
            if p["disk"] or p["program"]:
                print(f"  {p['role']}[{p['pid']}] {p['exec']} perf/ts {p['perf_over_taskstats']} disk {p['disk']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
