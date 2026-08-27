#!/usr/bin/env python3
"""1 s /proc state sampler (task-2.6 spec §1) — the slow sidecar.

Emits one JSONL line per sample: epoch-µs timestamp, loadavg, and per-process
{pid, ppid, comm, state, utime, stime, threads, starttime} from /proc/<pid>/stat.
With --ctxt, also voluntary/nonvoluntary context-switch counters from
/proc/<pid>/status (wakeup-rate estimation for the GUI workflow).

Linux-only; runs until SIGINT/SIGTERM. Structural/shape claims only —
absolutes carry the runner spec (building-plan §7).
"""

import argparse
import json
import os
import signal
import sys
import time

RUNNING = True


def _stop(_sig, _frm):
    global RUNNING
    RUNNING = False


def read_stat(pid):
    with open(f"/proc/{pid}/stat", "rb") as handle:
        raw = handle.read().decode("ascii", "replace")
    left, _, right = raw.partition("(")
    comm, _, rest = right.rpartition(")")
    fields = rest.split()
    return {
        "pid": int(left.strip()),
        "comm": comm,
        "state": fields[0],
        "ppid": int(fields[1]),
        "utime": int(fields[11]),
        "stime": int(fields[12]),
        "threads": int(fields[17]),
        "starttime": int(fields[19]),
    }


def read_ctxt(pid):
    volun = nonvol = None
    with open(f"/proc/{pid}/status", "rb") as handle:
        for line in handle:
            if line.startswith(b"voluntary_ctxt_switches:"):
                volun = int(line.split()[1])
            elif line.startswith(b"nonvoluntary_ctxt_switches:"):
                nonvol = int(line.split()[1])
    return volun, nonvol


def sample(with_ctxt):
    procs = []
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            record = read_stat(entry)
            if with_ctxt:
                record["vctxt"], record["nvctxt"] = read_ctxt(entry)
            procs.append(record)
        except (OSError, IndexError, ValueError):
            continue  # process vanished mid-read
    return {
        "t": time.time_ns() // 1000,
        "load": list(os.getloadavg()),
        "procs": procs,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--out", required=True)
    parser.add_argument("--ctxt", action="store_true")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    with open(args.out, "a", buffering=1) as out:
        while RUNNING:
            started = time.monotonic()
            out.write(json.dumps(sample(args.ctxt),
                                 separators=(",", ":")) + "\n")
            remaining = args.interval - (time.monotonic() - started)
            if remaining > 0:
                time.sleep(remaining)
    return 0


if __name__ == "__main__":
    sys.exit(main())
