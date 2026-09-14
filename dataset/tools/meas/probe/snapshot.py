#!/usr/bin/env python3
"""Snapshot one process tree's CPU, threads and context switches from /proc.

probe tooling for the 9.5 campaign (research-slice D3): prints one JSON
object for the process whose comm or cmdline matches PATTERN, summed over
its threads and its descendants. Read twice around a phase to get deltas.
"""

import json
import os
import re
import sys
import time

CLK = os.sysconf("SC_CLK_TCK")


def read(path):
    try:
        with open(path) as handle:
            return handle.read()
    except OSError:
        return ""


def pids():
    return [int(p) for p in os.listdir("/proc") if p.isdigit()]


def cmdline(pid):
    return read(f"/proc/{pid}/cmdline").replace("\0", " ").strip()


def stat_fields(path):
    raw = read(path)
    if not raw:
        return None
    close = raw.rfind(")")
    comm = raw[raw.find("(") + 1:close]
    rest = raw[close + 2:].split()
    return comm, rest


def parent(pid):
    fields = stat_fields(f"/proc/{pid}/stat")
    return int(fields[1][1]) if fields else None


def matching_roots(pattern):
    rx = re.compile(pattern)
    return [p for p in pids() if rx.search(cmdline(p)) or rx.search(
        read(f"/proc/{p}/comm").strip())]


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
    for line in read(f"/proc/{pid}/task/{tid}/status").splitlines():
        if line.startswith("voluntary_ctxt_switches"):
            vol = int(line.split()[1])
        elif line.startswith("nonvoluntary_ctxt_switches"):
            nonvol = int(line.split()[1])
    return vol, nonvol


def main():
    pattern = sys.argv[1]
    exclude = re.compile(sys.argv[2]) if len(sys.argv) > 2 else None
    roots = [p for p in matching_roots(pattern)
             if p != os.getpid() and not (exclude and exclude.search(cmdline(p)))]
    procs = descendants(roots)
    out = {"t_mono": time.monotonic(), "pattern": pattern, "roots": roots,
           "n_procs": len(procs), "n_threads": 0, "cpu_s": 0.0,
           "vol_switches": 0, "nonvol_switches": 0, "procs": []}
    for p in procs:
        fields = stat_fields(f"/proc/{p}/stat")
        if not fields:
            continue
        comm, rest = fields
        cpu = (int(rest[11]) + int(rest[12])) / CLK
        tids = [int(t) for t in os.listdir(f"/proc/{p}/task")] if os.path.isdir(f"/proc/{p}/task") else []
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
                             "cpu_s": cpu, "cmd": cmdline(p)[:120]})
    print(json.dumps(out))


if __name__ == "__main__":
    main()
