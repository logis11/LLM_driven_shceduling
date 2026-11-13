#!/usr/bin/env python3
"""Every task's waits for the lane on one trace, the ones the harness's starvation guard cannot read
among them (2026-11-13; simulator/memo/memo_261111.md Part L).

    sim W.workload.json [S.json] | python3 simulator/tools/wait_check.py W.workload.json
    python3 simulator/tools/wait_check.py W.workload.json trace.jsonl[.gz] [--floor 30000000] [--json]

The guard `starvation_floor` reads each task's longest `ready_wait` (harness/guards/guard-spec.yaml),
and a `ready_wait` row runs from a `ready` line to the task's next `run_start` (docs/harness/metrics.md
§6.1). Its grounding is wider: sched_ext's watchdog acts when a runnable task waits past its timeout.
Two waits of a runnable task have no row, and this tool reads them off the trace, up to T_end, the
latest time the workload writes:

  kind     `ready`   — from a `ready` line outside the task's own occupancy;
           `preempt` — from a `run_end(reason = preempt)`: no `ready` line, so no row;
  ending   `done`    — a `run_start` ended it (for `ready`, this is the guard's own reading);
           `open`    — T_end or the task's own end came first: no `run_start`, so no row.

A wait is dropped when the task blocks without the lane (`x_block`: a TIMER reached straight after a
TIMER, or a zero-work primitive). Prints one line and exits 1 when any wait of any kind is over the
floor, 0 otherwise; `--json` prints the record instead.
"""
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trace_check import events_of  # noqa: E402

FLOOR = 30_000_000   # the guard spec's starvation_floor, µs


def t_end_of(workload_path):
    end = 0
    for e in events_of(workload_path):
        end = max(end, int(e["t"]), int(e.get("depart") or 0))
    return end


def waits(lines, t_end, floor=FLOOR):
    """`lines`: the trace's lines as bytes. Returns the record of the docstring's four readings."""
    since = {"ready": {}, "preempt": {}}                 # kind -> task -> the time its wait began
    done = {"ready": (0, ""), "preempt": (0, "")}        # the longest wait a run_start ended
    opened = []                                          # (kind, task, since, until, how)
    running = None
    for line in lines:
        if line[10:13] not in (b"rea", b"run", b"tas", b"x_b"):
            continue
        q = line.split(b'"')
        ev = q[3]
        if ev == b"task_arrive":
            continue
        t = int(q[6][1:-1])
        if t > t_end:
            break
        task = q[9].decode()
        if ev == b"ready":
            if task != running:
                since["ready"].setdefault(task, t)
        elif ev == b"run_start":
            for kind in ("ready", "preempt"):
                a = since[kind].pop(task, None)
                if a is not None and t - a > done[kind][0]:
                    done[kind] = (t - a, task)
            running = task
        elif ev == b"run_end":
            running = None
            if q[13] == b"preempt":
                since["preempt"][task] = t
        elif ev == b"x_block":
            since["ready"].pop(task, None); since["preempt"].pop(task, None)
        elif ev == b"task_end":
            for kind in ("ready", "preempt"):
                a = since[kind].pop(task, None)
                if a is not None:
                    opened.append((kind, task, a, t, "task_end/" + q[13].decode()))
    for kind in ("ready", "preempt"):
        for task, a in since[kind].items():
            opened.append((kind, task, a, t_end, "T_end"))
    longest = {"ready": (0, "", ""), "preempt": (0, "", "")}
    for kind, task, a, u, how in opened:
        if u - a > longest[kind][0]:
            longest[kind] = (u - a, task, how)
    over = sorted(((u - a, kind, task, a, how) for kind, task, a, u, how in opened if u - a > floor), reverse=True)
    return {"t_end": t_end, "floor": floor,
            "ready_done": list(done["ready"]), "preempt_done": list(done["preempt"]),
            "ready_open": list(longest["ready"]), "preempt_open": list(longest["preempt"]),
            "open_over_floor": [list(x) for x in over[:40]], "open_over_floor_count": len(over)}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    floor = int(sys.argv[sys.argv.index("--floor") + 1]) if "--floor" in sys.argv else FLOOR
    if "--floor" in sys.argv:
        args = [a for a in args if a != str(floor)]
    src = args[1] if len(args) > 1 else None
    stream = (gzip.open(src, "rb") if src.endswith(".gz") else open(src, "rb")) if src else sys.stdin.buffer
    r = waits(stream, t_end_of(args[0]), floor)
    if "--json" in sys.argv:
        print(json.dumps(r))
    else:
        s = lambda us: f"{us / 1e6:.2f}s"
        worst = max(r["ready_done"][0], r["preempt_done"][0], r["ready_open"][0], r["preempt_open"][0])
        print(f"{'over' if worst > floor else 'ok'}  T_end {s(r['t_end'])}  "
              f"ready done {s(r['ready_done'][0])} {r['ready_done'][1]} (the guard's reading) | "
              f"ready open {s(r['ready_open'][0])} {r['ready_open'][1]} | "
              f"preempt done {s(r['preempt_done'][0])} {r['preempt_done'][1]} | "
              f"preempt open {s(r['preempt_open'][0])} {r['preempt_open'][1]}")
    worst = max(r["ready_done"][0], r["preempt_done"][0], r["ready_open"][0], r["preempt_open"][0])
    return 1 if worst > floor else 0


if __name__ == "__main__":
    sys.exit(main())
