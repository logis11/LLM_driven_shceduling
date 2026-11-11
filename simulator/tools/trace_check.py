#!/usr/bin/env python3
"""The §7 integration gate's sanity checks on one trace (steps/README.md §7 item 4; TODO 1.3).

    sim W.workload.json [S.json] | python3 simulator/tools/trace_check.py W.workload.json
    python3 simulator/tools/trace_check.py W.workload.json trace.jsonl[.gz]

Reads the trace as a stream (c6-dual's is 48 million lines) and checks, against the workload:

1. no event out of order — `t` never decreases from one line to the next;
2. delivered CPU <= elapsed — one lane: a run_start only on a free lane, a run_end only by the
   holder, so the occupancies never overlap, and their sum is at most the last line's t;
3. every completed task's RUN demand delivered — a task that ends with `task_end(exit)` received,
   over its occupancies, exactly the RUN total of its program (LOOP counts expanded). A task with
   a `wake_drop` line is counted apart: a dropped timer wake's RUN is passed with no work
   (conformance (j)), so its delivered CPU is its program's total minus those RUNs, which the
   trace does not name;
4. segment-bound tasks gone at their depart — a task with a pinned `depart` has its task_end at
   or before it, `reason: depart` exactly at it unless it exited first;
5. nothing of a task after its task_end, and at most one task_end per task.

Prints one line, `ok` or the failures (the first few of each), and exits 0 or 1.
"""
import collections
import gzip
import json
import re
import sys


def demand_of(program):
    """The RUN total of a program, LOOP counts expanded. None for an unbounded LOOP."""
    total = 0
    for op in program:
        kind = op["op"]
        if kind == "RUN":
            total += op["us"]
        elif kind == "LOOP":
            body = demand_of(op["body"])
            if body is None or op["count"] == "unbounded":
                return None
            total += body * op["count"]
    return total


def events_of(workload_path):
    """The workload's events one at a time. json.load of c6-dual (187 MB, millions of wake events)
    builds Python objects many times the file's size and took this machine down (2026-11-11), so the
    text is decoded event by event and each is dropped once the caller is done with it."""
    with open(workload_path) as f:
        text = f.read()
    dec = json.JSONDecoder()
    m = re.search(r'"events"\s*:\s*\[', text)
    if not m:
        raise SystemExit(f"no events array in {workload_path}")
    i = m.end()
    while True:
        while text[i] in " \t\r\n,":
            i += 1
        if text[i] == "]":
            return
        e, i = dec.raw_decode(text, i)
        yield e


def tasks_of(workload_path):
    """task id → (demand or None, depart or None), spawn-table children included."""
    out = {}
    for e in events_of(workload_path):
        if e["op"] != "arrive":
            continue
        out[e["id"]] = (demand_of(e["program"]), e.get("depart"))
        for c in e.get("spawn_table", []):
            out[c["id"]] = (demand_of(c["program"]), None)
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    tasks = tasks_of(sys.argv[1])
    src = sys.argv[2] if len(sys.argv) > 2 else None
    stream = (gzip.open(src, "rt") if src.endswith(".gz") else open(src)) if src else sys.stdin

    class Fails(collections.defaultdict):
        """A count and the first three messages per kind — a systematic failure on a 48-million-line
        trace must not keep millions of strings (it took this machine down once, 2026-11-11)."""
        def __init__(self):
            super().__init__(list)
            self.n = collections.Counter()

        def add(self, kind, msg):
            self.n[kind] += 1
            if len(self[kind]) < 3:
                self[kind].append(msg)

    fails = Fails()
    last_t = 0
    holder, since = None, 0
    busy = 0
    cpu = collections.Counter()
    ended = {}                      # task → (t, reason)
    dropped = set()
    n = 0
    for line in stream:
        n += 1
        e = json.loads(line)
        kind = e["event"]
        if kind == "meta":
            continue
        t = e["t"]
        if t < last_t:
            fails.add("order", f"line {n}: t {t} after {last_t}")
        last_t = max(last_t, t)
        task = e.get("task")
        if task is not None and task in ended and kind != "x_mlfq_boost":
            fails.add("after-end", f"line {n}: {kind} of {task} after its task_end at {ended[task][0]}")
        if kind == "run_start":
            if holder is not None:
                fails.add("lane", f"line {n}: run_start of {task} while {holder} holds the lane")
            holder, since = task, t
        elif kind == "run_end":
            if holder != task:
                fails.add("lane", f"line {n}: run_end of {task}, the holder is {holder}")
            else:
                cpu[task] += t - since
                busy += t - since
                holder = None
        elif kind == "task_end":
            if task in ended:
                fails.add("task-end", f"line {n}: a second task_end of {task}")
            ended[task] = (t, e["reason"])
            if holder == task:
                fails.add("lane", f"line {n}: task_end of {task} while it holds the lane")
        elif kind == "wake_drop":
            dropped.add(task)
    if holder is not None:              # an occupancy still open at the last line
        busy += last_t - since
        cpu[holder] += last_t - since

    if busy > last_t:
        fails.add("cpu>elapsed", f"busy {busy} > elapsed {last_t}")
    completed = skipped = 0
    for task, (t, reason) in ended.items():
        demand, depart = tasks.get(task, (None, None))
        if task not in tasks:
            fails.add("unknown", f"{task} is in no arrive or spawn table")
            continue
        if reason == "exit":
            if task in dropped:
                skipped += 1
                if demand is not None and cpu[task] > demand:
                    fails.add("demand", f"{task}: delivered {cpu[task]} > demand {demand}")
            elif demand is not None:
                completed += 1
                if cpu[task] != demand:
                    fails.add("demand", f"{task}: delivered {cpu[task]}, demand {demand}")
        if depart is not None:
            if t > depart:
                fails.add("depart", f"{task}: task_end at {t} after its depart {depart}")
            elif reason == "depart" and t != depart:
                fails.add("depart", f"{task}: task_end(depart) at {t}, depart {depart}")
    for task, (demand, depart) in tasks.items():
        if depart is not None and task not in ended:
            fails.add("depart", f"{task}: no task_end, depart {depart}")

    summary = f"lines {n} busy {busy} elapsed {last_t} completed-checked {completed} with-drops {skipped}"
    if not fails:
        print("ok  " + summary)
        return 0
    print("FAIL " + summary + "  " + "; ".join(f"{k} {fails.n[k]}: {v}" for k, v in sorted(fails.items())))
    return 1


if __name__ == "__main__":
    sys.exit(main())
