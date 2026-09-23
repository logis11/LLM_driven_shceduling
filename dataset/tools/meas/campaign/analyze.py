#!/usr/bin/env python3
"""Analyse one campaign run directory (run.sh output) into per-thread wake
and run distributions per phase and, for the driven phase, per-input run.

analyze.py <run-dir> [--w-ms 5] [--cap-ms 0] [--json out.json]

Reads report.json, snap.<phase>.{before,after}.json (the application's pid
set), perf.<phase>.timehist.txt[.gz], perf.<phase>.wakeups.txt[.gz] and, if
present, replay.jsonl. A timehist row is one schedule-in of a thread and the
run that followed it (a *segment*): sched-in = time − run, wake = sched-in −
sch delay. Rows are kept when the pid in `comm[tid/pid]` (or `comm[pid]`)
belongs to the application's process tree.

Wake definition (9.5 follow-ups spec, decision 4): a segment is a *wake* only
when a wakeup event for that thread (the wakeups file, `perf sched timehist
-w`) lies after the schedule-in of the wake it would continue and at or before
this schedule-in (9.7 D21). A segment with no such event is a resume after
preemption: its run is added to the preceding wake's run and the preempted
time is neither run nor gap. Where timehist carries the switch-out state
(`--state`, 9.5 D39), the row is checked against it per comm (`wake_check`);
for `thunderbird-send` the state decides and the row is the check (9.5 D40,
`wake_definition: state`).
Wake rates, gap and run distributions are computed over wakes; the per-input
window rule (b) sums segments, so it is unaffected. Without a wakeups file
every segment counts as a wake (`wake_definition: row`).

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
Row = namedtuple("Row", "t_in t_wake t_end run comm tid pid state", defaults=("",))  # compact: one tuple per schedule row

# comms of the measurement harness itself: the snapshot roots the tree at run.sh, whose children include these
HARNESS_COMMS = {"bash", "sh", "sleep", "setsid", "Xvfb", "perf", "python3", "xdotool", "gzip", "sudo", "tee", "sed",
                 "grep", "import", "convert", "date", "xwd", "wc", "cat", "kill", "sort", "awk", "run.sh", "phase.sh", "curl", "pgrep",
                 "taskset"}

# timehist [--state]: time [cpu] comm[tid/pid] wait sch_delay run [state] — the state column from 9.5 D39 on
ROW = re.compile(r"^\s*(\d+\.\d+)\s+\[(\d+)\]\s+(.*?)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)(?:\s+(\S+))?\s*$")
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


def load_rows(path, pids, comm_rx=None):
    """Rows of the application's threads, plus the capture window (first, last) over all tasks.

    comm_rx (the appdef's RX, recorded as `rx` in report.json) admits rows of pids the snapshots never saw —
    transient children of the tree such as Kdenlive's kdenlive_render, which lives only during a preview
    render (spec decisions 8–9); their pids are returned as the third element for the caller to record."""
    rows = []
    extra = set()
    rx = re.compile(comm_rx) if comm_rx else None
    t_min, t_max = None, None
    with open_text(path) as handle:
        for line in handle:
            m = ROW.match(line)
            if not m:
                continue
            t, cpu, task, wait, delay, run, state = m.groups()
            tf = float(t)
            t_min = tf if t_min is None or tf < t_min else t_min
            t_max = tf if t_max is None or tf > t_max else t_max
            tm = TASK.match(task.strip())
            if not tm:
                continue
            comm, a, b = tm.group(1), int(tm.group(2)), tm.group(3)
            tid, pid = (a, int(b)) if b else (a, a)
            if comm in HARNESS_COMMS or comm.startswith("llvmpipe-"):
                continue  # harness processes share the tree; llvmpipe-* is the runner's software rasteriser (D15)
            if pid not in pids:
                if rx and rx.search(comm):
                    extra.add(pid)
                else:
                    continue
            t, delay, run = float(t), float(delay), float(run)
            rows.append(Row(t - run / 1000.0, t - run / 1000.0 - delay / 1000.0, t, run, comm, tid, pid, state or ""))
    rows.sort(key=lambda r: r.t_in)
    return rows, (t_min or 0.0, t_max or 0.0), sorted(extra)


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


def load_all_wakeups(path, pids):
    """tid -> sorted wakeup times, for every wakee thread of the application's tree (any waker)."""
    out = {}
    with open_text(path) as handle:
        for line in handle:
            m = WAKE.match(line)
            if not m:
                continue
            t, _, _, wakee = m.groups()
            km = TASK.match(wakee.strip())
            if not km:
                continue
            kpid = int(km.group(3)) if km.group(3) else int(km.group(2))
            if kpid in pids:
                out.setdefault(int(km.group(2)), []).append(float(t))
    for v in out.values():
        v.sort()
    return out


EPS = 1e-6  # timehist prints microseconds
# 9.5 D40: the send campaign starts with the switch-out state recorded, so the state decides its wakes (9.7 D21), the
# row its check; the current campaign's repeats keep the row (D39)
STATE_WAKE_APPS = {"thunderbird-send"}


def merge_resumes(rows, wakeups_by_tid, check=None, by_state=False):
    """Fold resume-after-preemption segments into the wake they continue.

    rows: segments sorted by t_in. A segment is a wake when a wakeup event for its
    tid falls after the schedule-in of the wake it would continue and at or before
    this t_in: sched_waking fires only for a thread already in a sleep state
    (kernel try_to_wake_up: after ttwu_state_match) and can precede the sleeper's
    own switch-out by microseconds, so a row inside the thread's last run wakes
    the sleep that follows (9.7 changelog D21: the window from the switch-out
    missed those); the first segment of a thread in the capture is always a wake.
    The row decides for the whole 9.5 campaign, whose early repeats carry no
    switch-out state (9.5 D39); with by_state (9.5 D40), a recorded switch-out
    state decides instead — a sleep state (any but R) a wake, R a resume — and
    the row decides only where no state was recorded. check (a dict), if given,
    collects per comm the gaps whose preceding segment carries a state (`gaps`)
    and those where the row disagrees with it: a sleep state but no row
    (`slept_without_row`), R with a row (`preempted_with_row`). Returns (wakes
    sorted by t_in, number of segments merged)."""
    import bisect
    last = {}      # tid -> index into out of that thread's current wake
    out = []
    merged = 0
    for r in rows:
        i = last.get(r.tid)
        if i is None:
            out.append(r); last[r.tid] = len(out) - 1
            continue
        prev = out[i]
        wk = wakeups_by_tid.get(r.tid, [])
        k = bisect.bisect_right(wk, prev.t_in)
        row = k < len(wk) and wk[k] <= r.t_in + EPS
        slept = prev.state[:1] != "R" if prev.state else None
        woken = slept if by_state and slept is not None else row
        if check is not None and slept is not None:
            c = check.setdefault(prev.comm, {"gaps": 0, "slept_without_row": 0, "preempted_with_row": 0})
            c["gaps"] += 1
            if slept != row:
                c["slept_without_row" if slept else "preempted_with_row"] += 1
        if woken:
            out.append(r); last[r.tid] = len(out) - 1
        else:
            out[i] = prev._replace(run=prev.run + r.run, t_end=r.t_end, state=r.state)
            merged += 1
    out.sort(key=lambda r: r.t_in)
    return out, merged


def operation_windows(rows, ops):
    """Cut the op phase (spec decisions 8–9): rows whose schedule-in falls in a successful operation's
    [trigger, done) window are `inside` (the operation's components), the rest `outside`; durations in ms
    of the successful operations (rc 0), which the archetype carries as the operation's duration table."""
    import bisect
    ok = [(o["trigger_us"] / 1e6, o["done_us"] / 1e6) for o in ops if o.get("rc") == 0 and o.get("trigger_us") and o.get("done_us")]
    ok.sort()
    starts = [a for a, _ in ok]
    inside, outside = [], []
    for r in rows:
        k = bisect.bisect_right(starts, r.t_in) - 1
        if k >= 0 and r.t_in < ok[k][1]:
            inside.append(r)
        else:
            outside.append(r)
    return {"durations_ms": [round((b - a) * 1000, 3) for a, b in ok], "n_ok": len(ok),
            "n_failed": sum(1 for o in ops if o.get("rc") != 0), "inside": inside, "outside": outside,
            "name": ops[0]["op"] if ops else None}


def pid_roles(D, phase):
    """pid -> role from the snapshots' command lines: main | renderer | gpu | utility | zygote | other; for the op
    phase also from the per-operation process lists in ops.jsonl (transient processes the snapshots never see)."""
    roles = {}
    if phase == "op" and os.path.exists(os.path.join(D, "ops.jsonl")):
        for line in open(os.path.join(D, "ops.jsonl")):
            if not line.strip():
                continue
            for pid, kind in (json.loads(line).get("procs") or {}).items():
                roles.setdefault(int(pid), {"renderer": "renderer", "gpu-process": "gpu", "utility": "utility",
                                            "zygote": "zygote", "broker": "zygote", "main": "main"}.get(kind, "other"))
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


def component_name(role, comm):
    """D67: a component is identified by its process role and comm together — one comm can name a thread of several
    processes (chrome's Chrome_ChildIOT runs in the GPU process and in each utility process), and pooling their gaps
    into one bucket mixes a thread waking thousands of times with threads waking once or twice. The role is dropped
    from the name of a single-process tree's components, whose every thread carries role `main`."""
    return comm if role == "main" else f"{role}/{comm}"


def per_thread(rows, span_s, roles=None):
    """roles (pid -> role) qualifies each component by the role of the process its thread runs in (D67). The callers
    that already separate their rows per process — the desktop and session slices' entries — pass none and keep
    plain comm names."""
    out = {}
    by_tid = {}
    for r in rows:
        key = component_name(roles.get(r.pid, "main"), r.comm) if roles else r.comm
        by_tid.setdefault((key, r.tid), []).append(r)
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


def analyze_run(D, w_ms=5.0, cap_ms=0.0, waker="^Xvfb$|^Xorg$", wake_def="wakeup", exclude_roles=()):
    """Return (result, raw): result as printed/dumped by the CLI; raw = per-phase wakes, segments and per-input lists for pooling.
    exclude_roles: process roles (pid_roles) whose rows leave the tree — D14: Chrome's renderer processes belong to
    renderer-hidden and renderer-visible (9.8 D2), so the web-browser archetype is pooled with exclude_roles=("renderer",)."""
    class A: pass
    args = A(); args.run_dir = D; args.w_ms = w_ms; args.cap_ms = cap_ms; args.waker = waker; args.json = None
    args.wake_def = wake_def; args.exclude_roles = set(exclude_roles)
    return _analyze(args)


def _analyze(args):
    D = args.run_dir
    raw = {"phases": {}}
    report = json.load(open(os.path.join(D, "report.json")))
    result = {"app": report.get("app"), "repeat": report.get("repeat"), "mode": report.get("mode"),
              "version": report.get("version"), "phases": {}}
    idle_rate = None
    for phase in ("idle", "driven", "driven-alt", "play", "op"):
        th = next((p for p in (f"perf.{phase}.timehist.txt.gz", f"perf.{phase}.timehist.txt") if os.path.exists(os.path.join(D, p))), None)
        if not th:
            continue
        pids = set()
        for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
            p = os.path.join(D, snap)
            if os.path.exists(p):
                pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
        segments, (t0, t1), extra_pids = load_rows(os.path.join(D, th), pids, report.get("rx") if phase == "op" else None)
        # the tree's wakeup rows include the transient children load_rows admitted (Kdenlive's kdenlive_render): without
        # them every sleep of those threads found no row and was folded as a resume (9.5 D41)
        tree = pids | set(extra_pids)
        span = max(t1 - t0, 1e-6)
        roles = pid_roles(D, phase)
        excluded = getattr(args, "exclude_roles", set())
        if excluded:  # D14: rows of processes another archetype owns leave the tree (web-browser: renderers)
            segments = [r for r in segments if roles.get(r.pid, "main") not in excluded]
        total_run_s = sum(r.run for r in segments) / 1000
        wk_path = next((p for p in (f"perf.{phase}.wakeups.txt.gz", f"perf.{phase}.wakeups.txt") if os.path.exists(os.path.join(D, p))), None)
        wake_def = getattr(args, "wake_def", "wakeup")
        check = {}
        if wk_path and wake_def == "wakeup":
            by_state = report.get("app") in STATE_WAKE_APPS and any(r.state for r in segments)
            rows, merged = merge_resumes(segments, load_all_wakeups(os.path.join(D, wk_path), tree), check, by_state)
            wake_def = "state" if by_state else wake_def
        else:
            rows, merged, wake_def = segments, 0, "row"
        ph = {"pids": sorted(pids), "transient_pids": {p: sorted({r.comm for r in segments if r.pid == p}) for p in extra_pids},
              "rows": len(rows), "segments": len(segments), "resumes_merged": merged,
              "wake_definition": wake_def, "span_s": round(span, 2),
              "wake_check": check or None,   # the row against the switch-out state, where recorded (D39)
              "cpu_share": round(total_run_s / span, 4), "wakes_per_s": round(len(rows) / span, 2),
              "roles": per_role(rows, roles, span), "threads": per_thread(rows, span, roles)}
        if phase == "idle":
            idle_rate = total_run_s / span
        xwakes = load_wakeups(os.path.join(D, wk_path), tree, args.waker) if wk_path else []
        if xwakes:
            ph["x_wakes_per_s"] = round(len(xwakes) / span, 2)
            ph["x_wakes_by_comm"] = {c: n for c, n in sorted(((c, sum(1 for w in xwakes if w[1] == c)) for c in {w[1] for w in xwakes}), key=lambda kv: -kv[1])[:8]}
        replay = {"driven": "replay.jsonl", "driven-alt": "replay-alt.jsonl"}.get(phase)
        if phase == "op" and os.path.exists(os.path.join(D, "ops.jsonl")):
            ops = [json.loads(l) for l in open(os.path.join(D, "ops.jsonl")) if l.strip()]
            ow = operation_windows(rows, ops)
            in_span = sum(d for d in ow["durations_ms"]) / 1000 or 1e-6
            ph["operation"] = {"name": ow["name"], "n_ok": ow["n_ok"], "n_failed": ow["n_failed"],
                               "duration_ms": dist(ow["durations_ms"]),
                               "inside": {"wakes": len(ow["inside"]), "span_s": round(in_span, 2),
                                          "wakes_per_s": round(len(ow["inside"]) / in_span, 2),
                                          "cpu_share": round(sum(r.run for r in ow["inside"]) / 1000 / in_span, 4),
                                          "threads": per_thread(ow["inside"], in_span, roles)},
                               "outside_wakes_per_s": round(len(ow["outside"]) / (span - in_span), 2) if span > in_span else None}
            raw["phases"][phase] = {"rows": rows, "segments": segments, "span": span, "t0": t0, "idle_rate": idle_rate, "roles": roles,
                                    "operation": ow}
            result["phases"][phase] = ph
            continue
        if replay and os.path.exists(os.path.join(D, replay)):
            sent = [json.loads(l) for l in open(os.path.join(D, replay)) if l.strip()]
            s_times = [e["sent_us"] / 1e6 for e in sent]
            s_kinds = [e.get("kind", "key") for e in sent]
            wakes = [r.t_wake for r in rows]
            t_in = [r.t_in for r in segments]  # rule (b) sums segments: CPU time in the window, however it was split
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
                run_sum = sum(r.run for r in segments[a:b])
                win_run.append(run_sum); win_len.append((end - s) * 1000); win_wakes.append(b - a)
                if idle_rate is not None:
                    # D13: the input's work is the window's run net of the idle rate, bounded below by zero —
                    # a window quieter than the idle rate carries no input work (negative values are not physical)
                    win_run_corr.append(max(0.0, run_sum - idle_rate * (end - s) * 1000))
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
        raw["phases"][phase] = {"rows": rows, "segments": segments, "span": span, "t0": t0, "idle_rate": idle_rate, "roles": roles}
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
    ap.add_argument("--exclude-roles", dest="exclude_roles", default="", type=lambda v: set(x for x in v.split(",") if x),
                    help="process roles whose rows leave the tree, e.g. renderer (D14, web-browser)")
    ap.add_argument("--wake-def", dest="wake_def", choices=("wakeup", "row"), default="wakeup",
                    help="wakeup: a wake needs a wakeup event (default); row: every timehist row is a wake (the D1-D20 analysis)")
    args = ap.parse_args()
    result, _ = _analyze(args)
    if args.json:
        json.dump(result, open(args.json, "w"), indent=1)
    for phase, ph in result["phases"].items():
        print(f"== {result['app']} r{result['repeat']} {phase}: span {ph['span_s']} s, wakes {ph['rows']} of {ph['segments']} segments ({ph['wake_definition']}, {ph['resumes_merged']} resumes merged), cpu share {ph['cpu_share']}, wakes/s {ph['wakes_per_s']}")
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
