#!/usr/bin/env python3
"""One run's trace read against the batch-class rule and the cap, and its input latency recomputed.

    python3 cap_check.py <workload_id> [--run 'oracle~focus'] [--task editor]

Three checks, from the trace and the compiled workload alone:

1. The parks. Every `x_cap_park` that parks a task finds it in the batch class — rule B1, CPU since its last
   voluntary block at least the running config's slice, and not periodic (rule B2) — while a task that is not in
   the batch class and not of the idle class is runnable (the batch-class memo, `docs/memos/2026-09-09-batch-
   class-rule-for-the-simulator.md` §3 and §7 item 3); and no parked task runs before it is given back.
2. The ceiling. Over the capped config intervals, the CPU delivered to tasks while they are in the batch class,
   counted only while a non-batch task is runnable, is at most the cap times that time plus the bucket's depth,
   one slice (`simulator/memo/memo_261020.md` Part F, the token bucket of rate cap and depth one slice).
3. The scored term. The task's `input_latency` rows recomputed by the metrics doc's §6.12 rule — the k-th
   keystroke served by the k-th input WAIT's `ready` line, from the wake to that service's start — against the
   run's `records.csv.gz`, and their P99 by the harness's own percentile.

Writes `cap-check-<workload_id>.json` beside this script, or `--out`."""
import argparse
import csv
import gzip
import json
import pathlib
import sys
from collections import defaultdict
from fractions import Fraction

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import aggregates  # noqa: E402

SHARE_DEN = 10000


def periodic_tasks(programs):
    """Rule B2: every task with a TIMER, and every task reachable from one through WAKE targets."""
    seeds = {t for t, prog in programs.items() if any(p["op"] == "TIMER" for p in prog)}
    out, todo = set(), list(seeds)
    while todo:
        t = todo.pop()
        if t in out:
            continue
        out.add(t)
        todo += [p["target"] for p in programs.get(t, []) if p["op"] == "WAKE" and p.get("target")]
    return out


def slice_of(config):
    a, p = config["algorithm"], config.get("params") or {}
    if a == "EDF":
        return p["residual_timeslice_us"]
    if a == "FIFO":
        return 10000
    return p["timeslice_us"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workload_id")
    ap.add_argument("--run", default="oracle~focus")
    ap.add_argument("--task", default="editor")
    ap.add_argument("--runs-dir", default=str(REPO / "runs" / "rq0-gate"))
    ap.add_argument("--build-dir", default=str(REPO / "dataset" / "build" / "coreset-single"))
    ap.add_argument("--out", default=None, help="the result's path (default cap-check-<workload_id>.json here)")
    args = ap.parse_args()
    run_dir = pathlib.Path(args.runs_dir) / args.workload_id / args.run
    w = json.load(open(pathlib.Path(args.build_dir) / f"{args.workload_id}.workload.json"))
    arrive = {e["id"]: e for e in w["events"] if e["op"] == "arrive"}
    programs = {k: e["program"] for k, e in arrive.items()}
    for s in w.get("spawn") or []:
        programs[s["id"]] = s["program"]
    periodic = periodic_tasks(programs)
    idle = {k for k, e in arrive.items() if e.get("declared_class") == "idle"}
    idle |= {s["id"] for s in (w.get("spawn") or []) if s.get("declared_class") == "idle"}
    sched = json.load(open(run_dir / "schedule.json"))["schedule"]
    t_end = max(f["t_end"] for f in w["focus"])

    # config in force at t: the last entry at or before t (entries at one instant apply in order)
    entries = [(s["t_us"], s["config"]) for s in sched]

    def config_at(t):
        cfg = None
        for at, c in entries:
            if at <= t:
                cfg = c
        return cfg

    burst = defaultdict(int)          # B1 counter, settled at run_end
    runnable, parked = set(), set()
    running, start = None, 0
    park_checks = {"parks": 0, "parked_task_batch": 0, "nonbatch_runnable": 0, "violations": []}
    ran_while_parked = []
    capped_time = Fraction(0)
    in_class_capped = Fraction(0)
    cap_allow = Fraction(0)
    min_allow = Fraction(0)
    last_t = 0
    lines = []

    def is_batch(task, t):
        if task in periodic:
            return False
        b = burst[task] + (t - start if task == running else 0)
        return b >= slice_of(config_at(t))

    def advance(t):
        """Account [last_t, t]: the runnable set and the bursts of the waiting tasks are constant over it."""
        nonlocal capped_time, in_class_capped, last_t, cap_allow, min_allow
        if t <= last_t:
            last_t = max(last_t, t)
            return
        cfg = config_at(last_t)
        cap = cfg.get("batch_bandwidth_cap")
        if cap is not None:
            sl = slice_of(cfg)
            others_nonbatch = any(x != running and x not in idle and not is_batch(x, last_t) for x in runnable)
            run_nonbatch = running is not None and running not in idle and running in periodic
            b0 = burst[running] + (last_t - start) if running is not None else 0
            # split the interval at the running task's B1 crossing
            cut = last_t + max(0, sl - b0) if running is not None and running not in periodic else t
            for a, b in ((last_t, min(cut, t)), (max(cut, last_t), t)):
                if b <= a:
                    continue
                run_batch = running is not None and running not in periodic and (b0 + (a - last_t)) >= sl
                capped = others_nonbatch or (running is not None and not run_batch and running not in idle) \
                    or run_nonbatch
                if capped:
                    capped_time += b - a
                    cap_allow += Fraction(b - a) * Fraction(round(cap * SHARE_DEN), SHARE_DEN)
                    if run_batch:
                        in_class_capped += b - a
                        cap_allow -= b - a
                    cap_allow = min(cap_allow, sl)
                    min_allow = min(min_allow, cap_allow)
        last_t = t

    with gzip.open(run_dir / "trace.jsonl.gz", "rt") as f:
        for raw in f:
            e = json.loads(raw)
            ev, t, task = e["event"], e.get("t", 0), e.get("task")
            lines.append(e)
            if t > t_end:
                break
            advance(t)
            if ev == "task_arrive":
                pass
            elif ev == "ready":
                runnable.add(task)
            elif ev == "run_start":
                if task in parked:
                    ran_while_parked.append(t)
                running, start = task, t
            elif ev == "run_end":
                burst[task] += t - start
                running = None
            elif ev == "x_block":
                runnable.discard(task)
                burst[task] = 0
            elif ev == "task_end":
                runnable.discard(task)
            elif ev == "x_cap_park":
                if e["in"]:
                    park_checks["parks"] += 1
                    ok_batch = is_batch(task, t)
                    ok_other = any(x != task and x not in idle and not is_batch(x, t) for x in runnable)
                    park_checks["parked_task_batch"] += int(ok_batch)
                    park_checks["nonbatch_runnable"] += int(ok_other)
                    if not (ok_batch and ok_other) and len(park_checks["violations"]) < 10:
                        park_checks["violations"].append({"t": t, "task": task, "batch": ok_batch,
                                                          "nonbatch_runnable": ok_other})
                    parked.add(task)
                else:
                    parked.discard(task)
    advance(t_end)

    # 3. input latency (metrics doc §6.12), by walking the task's program through its ready lines
    task = args.task
    wakes = defaultdict(list)
    for e in w["events"]:
        if e["op"] == "wake" and e["target"] == task:
            wakes[e["channel"]].append(e["t"])
    dropped = defaultdict(list)
    for e in lines:
        if e["event"] == "wake_drop" and e["task"] == task:
            dropped[e["channel"]].append(e["t"])
    fate = {}                                            # (channel, k) -> 'd' for a dropped timer wake
    for ch, ts in dropped.items():
        pool = list(wakes[ch])
        used = set()
        for td in ts:
            k = next(i for i, x in enumerate(pool) if x == td and i not in used)
            used.add(k)
            fate[(ch, k)] = "d"
    ready = [e["t"] for e in lines if e["event"] == "ready" and e["task"] == task and e.get("cause") == "wake"]
    occupancy = []                                       # the task's [run_start, run_end) intervals
    s0 = None
    task_end = None
    for e in lines:
        if e.get("task") != task:
            continue
        if e["event"] == "run_start":
            s0 = e["t"]
        elif e["event"] == "run_end":
            occupancy.append((s0, e["t"]))
            s0 = None
        elif e["event"] == "task_end":
            task_end = e["t"]
    starts = sorted(a for a, _ in occupancy)

    def service_start(r):
        for a, b in occupancy:
            if a <= r < b or (a == r):
                return r
        nxt = next((a for a in starts if a >= r), None)
        return nxt

    k_by_ch = defaultdict(int)
    ri = 0
    mine = []
    for p in programs[task]:
        if p["op"] != "WAIT":
            continue
        ch = p["channel"]
        k = k_by_ch[ch]
        k_by_ch[ch] += 1
        if fate.get((ch, k)) == "d":
            continue
        if ri >= len(ready):
            if ch.startswith("input:") and k < len(wakes[ch]) and wakes[ch][k] < min(task_end or t_end, t_end):
                mine.append((wakes[ch][k], min(task_end or t_end, t_end) - wakes[ch][k], 1))
            continue
        r = ready[ri]
        ri += 1
        if ch.startswith("input:"):
            st = service_start(r)
            wk = wakes[ch][k]
            if st is None or st > t_end:
                mine.append((wk, min(task_end or t_end, t_end) - wk, 1))
            else:
                mine.append((wk, st - wk, 0))
    rec = []
    with gzip.open(run_dir / "records.csv.gz", "rt") as f:
        for r in csv.DictReader(f):
            if r["entity"] == task and r["metric"] == "input_latency":
                rec.append((int(r["t"]), int(r["value"]), int(r["censored"] or 0)))
    rec.sort()
    mine.sort()
    vals = [v for _, v, _ in rec]
    out = {
        "workload_id": args.workload_id, "run": args.run,
        "periodic": sorted(periodic), "idle": sorted(idle),
        "parks": park_checks, "parked_task_ran": len(ran_while_parked),
        "ceiling": {"capped_us": float(capped_time), "in_class_us": float(in_class_capped),
                    "share": float(in_class_capped / capped_time) if capped_time else None,
                    "bound_us": float(capped_time * Fraction(round(
                        (config_at(0).get("batch_bandwidth_cap") or 0) * SHARE_DEN), SHARE_DEN)),
                    "replayed_min_allow_us": float(min_allow)},
        "input_latency": {"rows_recomputed": len(mine), "rows_recorded": len(rec), "equal": mine == rec,
                          "first_difference": next(({"mine": a, "recorded": b} for a, b in zip(mine, rec)
                                                    if a != b), None),
                          "p99_us": float(aggregates.percentile(vals, 99)) if vals else None,
                          "p50_us": float(aggregates.percentile(vals, 50)) if vals else None},
    }
    sl = slice_of(config_at(0))
    out["ceiling"]["bound_us"] += sl
    out["ceiling"]["within"] = out["ceiling"]["in_class_us"] <= out["ceiling"]["bound_us"]
    out["ok"] = (park_checks["parks"] == park_checks["parked_task_batch"] == park_checks["nonbatch_runnable"]
                 and not ran_while_parked and out["ceiling"]["within"] and out["input_latency"]["equal"])
    path = pathlib.Path(args.out) if args.out else pathlib.Path(__file__).parent / f"cap-check-{args.workload_id}.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
