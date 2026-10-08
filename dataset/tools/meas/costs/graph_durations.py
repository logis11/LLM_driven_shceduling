#!/usr/bin/env python3
"""Per-call durations of one function from an ftrace function_graph trace (9.12 kernel-cost campaign,
research-slice changelog D31).

With `set_ftrace_filter` and `set_graph_function` both naming the one function, a call is a leaf line,
  ` 3)   0.581 us    |  pick_next_task_fair();`
its duration printed by the tracer, preceded by a marker above 10 µs (`+`, `!`, `#`, `*`, `@`, `$`), or an
opening and a closing line (`durations`). The duration
is the tracer's entry-to-return time, so it holds the part of the tracer's own cost that falls between its two
timestamps; the campaign's calibration pass (`__x64_sys_getpid`) measures that part on the same machine.

    graph_durations.py <trace> <function>   → JSON on stdout: n and the duration statistics in ns
"""

import json
import re
import statistics
import sys


def durations(path, func):
    """A call printed as a leaf line, or as an opening `func() {` line and, at depth 1, the next closing `}` line
    carrying the duration (the tracer splits a call when another entry lands in the buffer between its two
    halves)."""
    leaf = re.compile(r"\)\s*[+!#*@$]?\s*([0-9]+\.[0-9]+) us\s*\|\s*" + re.escape(func) + r"\(\);")
    opening = re.compile(r"\|\s*" + re.escape(func) + r"\(\) \{")
    closing = re.compile(r"\)\s*[+!#*@$]?\s*([0-9]+\.[0-9]+) us\s*\|\s*\}")
    out, open_call = [], False
    with open(path, errors="replace") as handle:
        for line in handle:
            m = leaf.search(line)
            if m:
                out.append(float(m.group(1)) * 1000.0)
                open_call = False
            elif opening.search(line):
                open_call = True
            elif open_call:
                m = closing.search(line)
                if m:
                    out.append(float(m.group(1)) * 1000.0)
                    open_call = False
    return out


def summary(ns):
    if not ns:
        return {"n": 0}
    s = sorted(ns)
    q = lambda p: s[min(len(s) - 1, int(p * len(s)))]
    return {"n": len(s), "mean_ns": round(statistics.fmean(s), 2), "median_ns": round(statistics.median(s), 2),
            "p10_ns": q(0.10), "p90_ns": q(0.90), "p99_ns": q(0.99), "p999_ns": q(0.999),
            "min_ns": s[0], "max_ns": s[-1], "sum_ns": round(sum(s), 1)}


if __name__ == "__main__":
    json.dump(summary(durations(sys.argv[1], sys.argv[2])), sys.stdout)
    print()
