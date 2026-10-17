#!/usr/bin/env python3
"""Every thread's scheduling class over a run (9.11 D4): policy, real-time
priority and nice from /proc/<pid>/task/<tid>/stat, one row when a thread is
first seen and one each time any of the three changes.

usage: classes.py <out.tsv> <interval_s>

Runs until SIGTERM or SIGINT. Fields of proc_pid_stat(5), counted from 1:
nice is 19, rt_priority 40, policy 41 (0 NORMAL, 1 FIFO, 2 RR, 3 BATCH,
5 IDLE, 6 DEADLINE, 7 EXT). comm sits in parentheses and may hold spaces, so
the fields after it are read from the last ')'.
"""

import os
import signal
import sys
import time

STOP = False


def stop(*_):
    global STOP
    STOP = True


def stat_fields(path):
    try:
        with open(path) as handle:
            raw = handle.read()
    except OSError:
        return None
    left, right = raw.find("("), raw.rfind(")")
    if left < 0 or right < 0:
        return None
    rest = raw[right + 2:].split()
    if len(rest) < 39:
        return None
    # rest[0] is field 3 (state): field n is rest[n - 3]
    return raw[left + 1:right], int(rest[1]), int(rest[16]), int(rest[37]), int(rest[38])


def cmdline(pid):
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as handle:
            raw = handle.read().replace(b"\0", b" ").decode(errors="replace")
            for ch in "\t\r\n":                 # one TSV field: an argument's tabs and newlines become spaces
                raw = raw.replace(ch, " ")
            return raw.strip()[:200]
    except OSError:
        return ""


def main():
    out, interval = sys.argv[1], float(sys.argv[2])
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    seen = {}
    with open(out, "w", buffering=1) as log:
        log.write("t_mono_s\tpid\ttid\tppid\tproc_comm\tcomm\tpolicy\trt_priority\tnice\tevent\tcmdline\n")
        while not STOP:
            now = time.monotonic()
            for pid in os.listdir("/proc"):
                if not pid.isdigit():
                    continue
                leader = stat_fields(f"/proc/{pid}/stat")
                if leader is None:
                    continue
                try:
                    tids = os.listdir(f"/proc/{pid}/task")
                except OSError:
                    continue
                for tid in tids:
                    fields = stat_fields(f"/proc/{pid}/task/{tid}/stat")
                    if fields is None:
                        continue
                    comm, _, nice, rtprio, policy = fields
                    key = (int(pid), int(tid))
                    state = (comm, policy, rtprio, nice)
                    old = seen.get(key)
                    if old == state:
                        continue
                    seen[key] = state
                    event = "new" if old is None else "change"
                    cmd = cmdline(pid) if old is None and pid == tid else ""
                    log.write(f"{now:.3f}\t{pid}\t{tid}\t{leader[1]}\t{leader[0]}\t{comm}\t{policy}\t{rtprio}\t{nice}\t{event}\t{cmd}\n")
            time.sleep(interval)
    return 0


if __name__ == "__main__":
    sys.exit(main())
