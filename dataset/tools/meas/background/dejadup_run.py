#!/usr/bin/env python3
"""dejadup_run.py <out dir> -- <session command...> — the incremental phase's driver (9.10 D112, D118), run on the
harness CPUs.

Starts the session command — run.sh's: the user's session bus on the measured CPU, the keyring unlocked and
deja-dup-monitor started in it (dejadup-session.sh monitor) — in a session of its own, so it outlives the phase until
run.sh stops it. Waits for the deja-dup the monitor starts, after its 120 s wait, as `chrt --idle 0 ionice -c3
deja-dup --backup --auto` (S2-62 BackupInterface.vala:39, CommonUtils.vala:107–131); reads its arguments, parent,
scheduling policy, I/O class and CPU affinity once it runs deja-dup — its parent as /proc shows it is recorded, not
checked: the perf fork rows carry the lineage from the monitor — and returns at its exit, the job's end. Writes
run.json: the steps' times (CLOCK_MONOTONIC and wall, ns), the process's readings, notes. Exit status: 0 the backup
ran and deja-dup exited; 2 no deja-dup within 900 s; 3 deja-dup still running at the cap.
"""

import json
import os
import subprocess
import sys
import time

PROGRAM = "deja-dup"
APPEAR_S = 900
CAP_S = 4 * 3600


def stamp():
    return {"mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}


def pids_named(name):
    return [int(p) for p in subprocess.run(["pgrep", "-x", name], capture_output=True, text=True).stdout.split()]


def read(path):
    try:
        return open(path, "rb").read()
    except OSError:
        return b""


def out_of(*cmd):
    return subprocess.run(list(cmd), capture_output=True, text=True).stdout.strip()


def main():
    a = sys.argv[1:]
    out, cmd = a[0], a[a.index("--") + 1:]
    rec = {"steps": {}, "notes": [], "session": cmd}

    def done(rc):
        rec["rc"] = rc
        json.dump(rec, open(os.path.join(out, "run.json"), "w"), indent=1)
        sys.exit(rc)

    before = set(pids_named(PROGRAM))
    rec["before"] = sorted(before)
    rec["steps"]["session"] = stamp()
    subprocess.Popen(cmd, stdout=open(os.path.join(out, "dejadup.session.log"), "w"), stderr=subprocess.STDOUT,
                     stdin=subprocess.DEVNULL, start_new_session=True)
    pid, end = None, time.monotonic() + APPEAR_S
    while pid is None and time.monotonic() < end:
        new = [p for p in pids_named(PROGRAM) if p not in before]
        if new:
            pid = new[0]
        else:
            time.sleep(0.05)
    rec["steps"]["seen"] = stamp()
    if pid is None:
        rec["notes"].append(f"no {PROGRAM} within {APPEAR_S} s of the session's start")
        done(2)
    rec["pid"] = pid
    rec["argv"] = [x.decode(errors="replace") for x in read(f"/proc/{pid}/cmdline").split(b"\0") if x]
    stat = read(f"/proc/{pid}/stat").decode(errors="replace")
    ppid = stat.rsplit(")", 1)[-1].split()[1] if ")" in stat else ""
    rec["ppid"] = ppid
    rec["parent_comm"] = read(f"/proc/{ppid}/comm").decode(errors="replace").strip() if ppid else ""
    rec["policy"] = out_of("chrt", "-p", str(pid))
    rec["io_class"] = out_of("ionice", "-p", str(pid))
    rec["affinity"] = out_of("taskset", "-pc", str(pid))
    rec["comm"] = read(f"/proc/{pid}/comm").decode(errors="replace").strip()
    end = time.monotonic() + CAP_S
    while os.path.exists(f"/proc/{pid}") and time.monotonic() < end:
        time.sleep(0.1)
    rec["steps"]["gone"] = stamp()
    if os.path.exists(f"/proc/{pid}"):
        rec["notes"].append(f"{PROGRAM} still running after {CAP_S} s")
        done(3)
    done(0)


if __name__ == "__main__":
    main()
