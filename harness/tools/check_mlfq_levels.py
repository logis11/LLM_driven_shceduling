#!/usr/bin/env python3
"""check_mlfq_levels: does each switch window cover its hogs' last demotion?

    check_mlfq_levels.py --run RUN.json --trace TRACE.jsonl[.gz] [--schedule CONFIG-SCHEDULE.json]

Ground truth for the `switch_window` primitive (memo 2026-09-08 §4). The
simulator emits `x_mlfq_level` {t, task, from, to} on every MLFQ demotion and
boost; the harness ignores those lines by the `x_` rule, so this tool — beside
the harness, not inside it — reads them itself. For every switch into MLFQ it
takes the hogs the primitive counted and checks that each hog's last demotion
after t_apply (the run of demotions before its next boost, or down to the
bottom queue) lies inside [t_apply, t_apply + value]. Exit 1 if any does not:
a systematic miss is the evidence for proposing a field in the closed set.
Without the schedule a switch into MLFQ cannot be sized; the guard is printed
and the exit code is 2."""
import argparse
import gzip
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.primitives import compute  # noqa: E402
from harness.reader import read_config_schedule, read_run_file, read_trace  # noqa: E402


def level_lines(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    out = []
    with opener(path, "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("event") == "x_mlfq_level":
                out.append((int(obj["t"]), obj["task"], int(obj["from"]), int(obj["to"])))
    out.sort(key=lambda x: x[0])
    return out


def last_demotion(lines, task, t_apply, bottom):
    """t of the last demotion in the run that starts after t_apply and ends at
    the next boost or at the bottom queue; None if no demotion follows."""
    last = None
    for (t, tid, frm, to) in lines:
        if tid != task or t <= t_apply:
            continue
        if to < frm:                      # a boost ends the run
            break
        if to > frm:
            last = t
            if to == bottom:
                break
    return last


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--trace", required=True)
    ap.add_argument("--schedule", default=None)
    args = ap.parse_args()

    run = read_run_file(args.run)
    schedule = read_config_schedule(args.schedule) if args.schedule else None
    result = compute(run, read_trace(args.trace), schedule)
    into_mlfq = [s for s in result.switches if s.algorithm == "MLFQ"]
    if not into_mlfq:
        omitted = [g for g in result.guards if "switch_window row omitted" in g]
        if omitted:
            for g in omitted:
                print(f"guard: {g}")
            return 2
        print("no switch into MLFQ; nothing to check")
        return 0
    lines = level_lines(args.trace)
    if not lines:
        print(f"{len(into_mlfq)} switch(es) into MLFQ but no x_mlfq_level lines in the trace; "
              "nothing to check")
        return 0

    misses = 0
    for sw in into_mlfq:
        entry = schedule.entry(sw.index)
        bottom = int(entry.params["num_queues"]) - 1
        until = sw.t + sw.value
        print(f"switch index {sw.index} at {sw.t} (MLFQ, {len(sw.hogs)} hog(s), "
              f"window {sw.value} -> until {until})")
        if not sw.hogs:
            print("  no hogs; nothing to cover")
            continue
        for hog in sw.hogs:
            t_last = last_demotion(lines, hog, sw.t, bottom)
            if t_last is None:
                misses += 1
                print(f"  hog {hog}: no demotion after {sw.t} -> not covered")
            elif t_last <= until:
                print(f"  hog {hog}: last demotion {t_last} -> covered")
            else:
                misses += 1
                print(f"  hog {hog}: last demotion {t_last} -> not covered "
                      f"({t_last - until} past the window)")
    print("all covered" if not misses else f"{misses} hog window(s) not covered")
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
