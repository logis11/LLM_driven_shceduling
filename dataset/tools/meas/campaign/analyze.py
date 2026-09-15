#!/usr/bin/env python3
"""Analyse one campaign run directory (run.sh output) into per-thread wake
and run distributions per phase and, for the driven phase, per-input run.

analyze.py <run-dir> [--w-ms 5] [--cap-ms 0] [--json out.json]

Reads report.json, snap.<phase>.{before,after}.json (the application's pid
set), perf.<phase>.timehist.txt[.gz] and, if present, replay.jsonl. A
timehist row is the end of one run of a thread: sched-in = time − run,
wake = sched-in − sch delay. Rows are kept when the pid in `comm[tid/pid]`
(or `comm[pid]`) belongs to the application's process tree.

Per phase and per thread comm: wakes per second, gap between consecutive
sched-ins (p50, p90, p99, ms), run per sched-in (p50, p90, p99, ms), CPU
share. Driven phase, per replayed input event i with send time s_i: (a)
first-wake rule — the first application wake in [s_i, s_i + W] and the run
of that sched-in; (b) window rule — total application run in
[s_i, min(s_{i+1}, s_i + cap)) with the idle phase's CPU rate over the same
span subtracted; (c) waker rule — from perf.<phase>.wakeups.txt.gz (rows
`time [cpu] waker[tid/pid] ... awakened: wakee[tid/pid]`), the application
wakes whose waker is the X server (comm Xvfb), which is how replayed input
reaches the application, and the run of those schedule-ins per input
window. All three are reported; the method chooses (9.5 changelog).
"""

import argparse
import gzip
import json
import os
import re
import statistics

from collections import namedtuple
Row = namedtuple("Row", "t_in t_wake t_end run comm tid pid")  # compact: one tuple per schedule row

# comms of the measurement harness itself: the snapshot roots the tree at run.sh, whose children include these
HARNESS_COMMS = {"bash", "sh", "sleep", "setsid", "Xvfb", "perf", "python3", "xdotool", "gzip", "sudo", "tee", "sed",
                 "grep", "import", "convert", "date", "xwd", "wc", "cat", "kill", "sort", "awk", "run.sh", "phase.sh"}

ROW = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*$")
TASK = re.compile(r"^(.*)\[(\d+)(?:/(\d+))?\]$")


def pct(values, q):
    if not values:
        return None
    v = sorted(values)
    k = (len(v) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return round(v[lo] + (v[hi] - v[lo]) * (k - lo), 3)


def dist(values):
    return {"n": len(values), "p50": pct(values, .5), "p90": pct(values, .9), "p99": pct(values, .99),
            "mean": round(statistics.fmean(values), 3) if values else None, "sum": round(sum(values), 3)}


def open_text(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def load_rows(path, pids):
    """Rows of the application's threads, plus the capture window (first, last) over all tasks."""
    rows = []
    t_min, t_max = None, None
    with open_text(path) as handle:
        for line in handle:
            m = ROW.match(line)
            if not m:
                continue
            t, cpu, task, wait, delay, run = m.groups()
            tf = float(t)
            t_min = tf if t_min is None or tf < t_min else t_min
            t_max = tf if t_max is None or tf > t_max else t_max
            tm = TASK.match(task.strip())
            if not tm:
                continue
            comm, a, b = tm.group(1), int(tm.group(2)), tm.group(3)
            tid, pid = (a, int(b)) if b else (a, a)
            if pid not in pids or comm in HARNESS_COMMS or comm.startswith("llvmpipe-"):
                continue  # harness processes share the tree; llvmpipe-* is the runner's software rasteriser (D15)
            t, delay, run = float(t), float(delay), float(run)
            rows.append(Row(t - run / 1000.0, t - run / 1000.0 - delay / 1000.0, t, run, comm, tid, pid))
    rows.sort(key=lambda r: r.t_in)
    return rows, (t_min or 0.0, t_max or 0.0)


WAKE = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+awakened:\s+(.*?)\s*$")


def load_wakeups(path, pids, waker_rx):
    """Return sorted wake times of application threads woken by a waker matching waker_rx."""
    out = []
    with open_text(path) as handle:
        for line in handle:
            m = WAKE.match(line)
            if not m:
                continue
            t, _, waker, wakee = m.groups()
            wm, km = TASK.match(waker.strip()), TASK.match(wakee.strip())
            if not km:
                continue
            kpid = int(km.group(3)) if km.group(3) else int(km.group(2))
            if kpid not in pids:
                continue
            wcomm = wm.group(1) if wm else waker.strip()
            if re.search(waker_rx, wcomm):
                out.append((float(t), km.group(1), int(km.group(2))))
    out.sort()
    return out


def pid_roles(D, phase):
    """pid -> role from the snapshots' command lines: main | renderer | gpu | utility | zygote | other."""
    roles = {}
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json", "snap.launch.json"):
        p = os.path.join(D, snap)
        if not os.path.exists(p):
            continue
        for pr in json.load(open(p))["procs"]:
            cmd = pr.get("cmd", "")
            if "--type=renderer" in cmd:
                role = "renderer"
            elif "--type=gpu-process" in cmd:
                role = "gpu"
            elif "--type=utility" in cmd:
                role = "utility"
            elif "--type=zygote" in cmd or "--type=broker" in cmd:
                role = "zygote"
            elif "--type=" in cmd:
                role = "other"
            else:
                role = "main"
            roles.setdefault(pr["pid"], role)
    return roles


def per_role(rows, roles, span_s):
    out = {}
    for r in rows:
        role = roles.get(r.pid, "main")
        c = out.setdefault(role, {"pids": set(), "wakes": 0, "run": 0.0})
        c["pids"].add(r.pid); c["wakes"] += 1; c["run"] += r.run
    return {role: {"pids": len(c["pids"]), "wakes_per_s": round(c["wakes"] / span_s, 2), "cpu_share": round(c["run"] / 1000 / span_s, 4)}
            for role, c in sorted(out.items(), key=lambda kv: -kv[1]["run"])}


def per_thread(rows, span_s):
    out = {}
    by_tid = {}
    for r in rows:
        by_tid.setdefault((r.comm, r.tid), []).append(r)
    by_comm = {}
    for (comm, tid), rs in by_tid.items():
        gaps = [(b.t_in - a.t_in) * 1000 for a, b in zip(rs, rs[1:])]
        by_comm.setdefault(comm, {"threads": 0, "wakes": 0, "gaps": [], "runs": []})
        c = by_comm[comm]
        c["threads"] += 1; c["wakes"] += len(rs); c["gaps"] += gaps; c["runs"] += [r.run for r in rs]
    for comm, c in sorted(by_comm.items(), key=lambda kv: -sum(kv[1]["runs"])):
        out[comm] = {"threads": c["threads"], "wakes_per_s": round(c["wakes"] / span_s, 2),
                     "cpu_share": round(sum(c["runs"]) / 1000 / span_s, 4),
                     "gap_ms": dist(c["gaps"]), "run_ms": dist(c["runs"])}
    return out


def phase_span(rows):
    return (rows[0].t_in, rows[-1].t_end) if rows else (0, 0)


def analyze_run(D, w_ms=5.0, cap_ms=0.0, waker="^Xvfb$|^Xorg$"):
    """Return (result, raw): result as printed/dumped by the CLI; raw = per-phase rows and per-input lists for pooling."""
    class A: pass
    args = A(); args.run_dir = D; args.w_ms = w_ms; args.cap_ms = cap_ms; args.waker = waker; args.json = None
    return _analyze(args)


def _analyze(args):
    D = args.run_dir
    raw = {"phases": {}}
    report = json.load(open(os.path.join(D, "report.json")))
    result = {"app": report.get("app"), "repeat": report.get("repeat"), "mode": report.get("mode"),
              "version": report.get("version"), "phases": {}}
    idle_rate = None
    for phase in ("idle", "driven", "play"):
        th = next((p for p in (f"perf.{phase}.timehist.txt.gz", f"perf.{phase}.timehist.txt") if os.path.exists(os.path.join(D, p))), None)
        if not th:
            continue
        pids = set()
        for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
            p = os.path.join(D, snap)
            if os.path.exists(p):
                pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
        rows, (t0, t1) = load_rows(os.path.join(D, th), pids)
        span = max(t1 - t0, 1e-6)
        total_run_s = sum(r.run for r in rows) / 1000
        roles = pid_roles(D, phase)
        ph = {"pids": sorted(pids), "rows": len(rows), "span_s": round(span, 2),
              "cpu_share": round(total_run_s / span, 4), "wakes_per_s": round(len(rows) / span, 2),
              "roles": per_role(rows, roles, span), "threads": per_thread(rows, span)}
        if phase == "idle":
            idle_rate = total_run_s / span
        wk_path = next((p for p in (f"perf.{phase}.wakeups.txt.gz", f"perf.{phase}.wakeups.txt") if os.path.exists(os.path.join(D, p))), None)
        xwakes = load_wakeups(os.path.join(D, wk_path), pids, args.waker) if wk_path else []
        if xwakes:
            ph["x_wakes_per_s"] = round(len(xwakes) / span, 2)
            ph["x_wakes_by_comm"] = {c: n for c, n in sorted(((c, sum(1 for w in xwakes if w[1] == c)) for c in {w[1] for w in xwakes}), key=lambda kv: -kv[1])[:8]}
        if phase == "driven" and os.path.exists(os.path.join(D, "replay.jsonl")):
            sent = [json.loads(l) for l in open(os.path.join(D, "replay.jsonl")) if l.strip()]
            s_times = [e["sent_us"] / 1e6 for e in sent]
            s_kinds = [e.get("kind", "key") for e in sent]
            wakes = [r.t_wake for r in rows]
            t_in = [r.t_in for r in rows]
            import bisect
            first_lat, first_run, win_run, win_len, win_wakes, win_run_corr = [], [], [], [], [], []
            xw_times = [w[0] for w in xwakes]
            # index rows by (tid, t_wake) to find the schedule-in that followed an X wake
            by_tid = {}
            for r in rows:
                by_tid.setdefault(r.tid, []).append(r)
            by_tid_tin = {tid: [r.t_in for r in rs] for tid, rs in by_tid.items()}
            xw_run, xw_count, xw_lat = [], [], []
            for i, s in enumerate(s_times):
                if s < t0 or s > t1:
                    continue
                nxt = s_times[i + 1] if i + 1 < len(s_times) else t1
                end = min(nxt, t1, s + args.cap_ms / 1000 if args.cap_ms > 0 else nxt)
                j = bisect.bisect_left(wakes, s)
                if j < len(wakes) and wakes[j] - s <= args.w_ms / 1000:
                    first_lat.append((wakes[j] - s) * 1000); first_run.append(rows[j].run)
                a, b = bisect.bisect_left(t_in, s), bisect.bisect_left(t_in, end)
                run_sum = sum(r.run for r in rows[a:b])
                win_run.append(run_sum); win_len.append((end - s) * 1000); win_wakes.append(b - a)
                if idle_rate is not None:
                    win_run_corr.append(run_sum - idle_rate * (end - s) * 1000)
                if xwakes:
                    xa, xb = bisect.bisect_left(xw_times, s), bisect.bisect_left(xw_times, end)
                    xw_count.append(xb - xa)
                    run_x = 0.0
                    for (tw, comm, tid) in xwakes[xa:xb]:
                        rs = by_tid.get(tid, [])
                        k = bisect.bisect_left(by_tid_tin.get(tid, []), tw)
                        if k < len(rs) and rs[k].t_in - tw < 0.05:
                            run_x += rs[k].run
                    xw_run.append(run_x)
                    if xb > xa:
                        xw_lat.append((xw_times[xa] - s) * 1000)
            ph["per_input"] = {"events_in_phase": len(win_run), "kinds": {k: s_kinds.count(k) for k in set(s_kinds)},
                               "first_wake": {"attributed_share": round(len(first_lat) / max(len(win_run), 1), 3),
                                              "latency_ms": dist(first_lat), "run_ms": dist(first_run)},
                               "window": {"len_ms": dist(win_len), "wakes": dist(win_wakes), "run_ms": dist(win_run),
                                          "run_ms_minus_idle": dist(win_run_corr) if win_run_corr else None,
                                          "idle_rate_ms_per_ms": round(idle_rate, 5) if idle_rate is not None else None},
                               "waker": {"x_wakes_per_input": dist(xw_count), "first_x_wake_latency_ms": dist(xw_lat),
                                         "run_ms": dist(xw_run)} if xwakes else None}
        result["phases"][phase] = ph
        raw["phases"][phase] = {"rows": rows, "span": span, "idle_rate": idle_rate, "roles": roles}
        if "per_input" in ph:
            raw["phases"][phase]["per_input"] = {"first_lat": first_lat, "first_run": first_run, "win_run": win_run,
                                                 "win_len": win_len, "win_wakes": win_wakes, "win_run_corr": win_run_corr,
                                                 "xw_run": xw_run, "xw_count": xw_count, "xw_lat": xw_lat}
    return result, raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir"); ap.add_argument("--w-ms", type=float, default=5.0)
    ap.add_argument("--cap-ms", type=float, default=0.0); ap.add_argument("--json", default=None)
    ap.add_argument("--waker", default="^Xvfb$|^Xorg$")
    args = ap.parse_args()
    result, _ = _analyze(args)
    if args.json:
        json.dump(result, open(args.json, "w"), indent=1)
    for phase, ph in result["phases"].items():
        print(f"== {result['app']} r{result['repeat']} {phase}: span {ph['span_s']} s, rows {ph['rows']}, cpu share {ph['cpu_share']}, wakes/s {ph['wakes_per_s']}")
        print(f"   roles: {ph['roles']}")
        for comm, c in list(ph["threads"].items())[:8]:
            print(f"   {comm:16s} thr {c['threads']:3d} wakes/s {c['wakes_per_s']:8.2f} cpu {c['cpu_share']:.4f} gap p50/p90 {c['gap_ms']['p50']}/{c['gap_ms']['p90']} run p50/p90/p99 {c['run_ms']['p50']}/{c['run_ms']['p90']}/{c['run_ms']['p99']}")
        if "per_input" in ph:
            pi = ph["per_input"]
            print(f"   per input: events {pi['events_in_phase']} {pi['kinds']}; first-wake attributed {pi['first_wake']['attributed_share']}, latency p50 {pi['first_wake']['latency_ms']['p50']}, run p50 {pi['first_wake']['run_ms']['p50']}; window run p50/p90 {pi['window']['run_ms']['p50']}/{pi['window']['run_ms']['p90']} minus idle p50 {pi['window']['run_ms_minus_idle']['p50'] if pi['window']['run_ms_minus_idle'] else None}")
            if pi.get("waker"):
                w = pi["waker"]
                print(f"   waker rule: X wakes per input p50/p90 {w['x_wakes_per_input']['p50']}/{w['x_wakes_per_input']['p90']}, first X wake latency p50/p90 {w['first_x_wake_latency_ms']['p50']}/{w['first_x_wake_latency_ms']['p90']} ms, run p50/p90/p99 {w['run_ms']['p50']}/{w['run_ms']['p90']}/{w['run_ms']['p99']} ms")
        if ph.get("x_wakes_by_comm"):
            print(f"   X-woken: {ph['x_wakes_per_s']}/s {ph['x_wakes_by_comm']}")


if __name__ == "__main__":
    main()
