#!/usr/bin/env python3
"""The system-call rows of the 9.7 campaign's `perf trace` (method §4) decoded for the network-wait rule and bytes per
wake (method §5; changelog D13 (vi)–(vii)).

run.sh records `perf trace record` — the raw_syscalls enter and exit events, CLOCK_MONOTONIC, the measured CPU — with a
kernel filter on the call numbers of FILTER_IDS, and converts the data with `perf script` into rows

    <pid>/<tid> <time>: raw_syscalls:sys_enter: NR <nr> (<a0>, <a1>, <a2>, <a3>, <a4>, <a5>)
    <pid>/<tid> <time>: raw_syscalls:sys_exit: NR <nr> = <ret>

The numbers are decoded here, per process, with the table of the process's own ABI: SteamCMD is a 32-bit program
(changelog D4), and a 32-bit process on the 64-bit kernel enters its calls with the i386 numbers — where, besides the
direct socket calls, a C library may reach the socket layer through `socketcall` (a sub-call number in the first
argument, the rest behind a pointer). FILTER_IDS is the union of both tables' numbers for the method's calls: the
receive and send calls, the poll-family waits, `socket`, `connect`, `close`.

`python3 nettrace.py filter` prints the kernel filter expression run.sh passes to the recording.
"""

import bisect
import gzip
import re
import sys
from collections import defaultdict, namedtuple

# the method §4 call list, by ABI (arch/x86/entry/syscalls/syscall_64.tbl and syscall_32.tbl)
X64 = {0: "read", 1: "write", 3: "close", 7: "poll", 19: "readv", 20: "writev", 23: "select", 41: "socket", 42: "connect",
       44: "sendto", 45: "recvfrom", 46: "sendmsg", 47: "recvmsg", 232: "epoll_wait", 270: "pselect6", 271: "ppoll",
       281: "epoll_pwait", 299: "recvmmsg", 441: "epoll_pwait2"}
I386 = {3: "read", 4: "write", 6: "close", 82: "select", 102: "socketcall", 142: "_newselect", 145: "readv", 146: "writev",
        168: "poll", 256: "epoll_wait", 308: "pselect6", 309: "ppoll", 319: "epoll_pwait", 337: "recvmmsg", 359: "socket",
        362: "connect", 369: "sendto", 370: "sendmsg", 371: "recvfrom", 372: "recvmsg", 413: "pselect6_time64",
        414: "ppoll_time64", 417: "recvmmsg_time64", 441: "epoll_pwait2"}
# socketcall's first argument (include/uapi/linux/net.h); the descriptor is behind the pointer and is not recorded
SOCKETCALL = {1: "socket", 3: "connect", 9: "send", 10: "recv", 11: "sendto", 12: "recvfrom", 16: "sendmsg",
              17: "recvmsg", 19: "recvmmsg", 20: "sendmmsg"}
FILTER_IDS = sorted(set(X64) | set(I386))

RECV = {"recv", "recvfrom", "recvmsg", "recvmmsg", "recvmmsg_time64"}
SEND = {"send", "sendto", "sendmsg", "sendmmsg"}
READ = {"read", "readv"}
WRITE = {"write", "writev"}
POLL = {"poll", "ppoll", "ppoll_time64", "select", "_newselect", "pselect6", "pselect6_time64", "epoll_wait",
        "epoll_pwait", "epoll_pwait2"}
MSG_COUNT = {"recvmmsg", "recvmmsg_time64", "sendmmsg"}   # return a message count, not bytes
EPS = 1e-6

# kind: recv | send (socket), fread | fwrite (any other descriptor), poll, socket, connect, close
Call = namedtuple("Call", "t_enter t_exit pid tid name fd ret kind nbytes")

ROW = re.compile(r"^\s*(?:\S.*?\s+)?(\d+)/(\d+)\s+(?:\[\d+\]\s+)?(\d+\.\d+):\s+raw_syscalls:sys_(enter|exit):\s+"
                 r"NR\s+(-?\d+)\s+(?:\(([^)]*)\)|=\s+(-?\d+))")


def filter_expr():
    return " || ".join(f"id == {n}" for n in FILTER_IDS)


def open_text(path):
    return gzip.open(path, "rt") if path.endswith(".gz") else open(path)


def load_rows(path):
    """Raw rows: (t, pid, tid, 'enter'|'exit', nr, args tuple or None, ret or None)."""
    rows = []
    with open_text(path) as handle:
        for line in handle:
            m = ROW.match(line)
            if not m:
                continue
            pid, tid, t, kind, nr, args, ret = m.groups()
            a = tuple(int(x.strip(), 16) for x in args.split(",")) if args is not None else None
            rows.append((float(t), int(pid), int(tid), kind, int(nr), a, int(ret) if ret is not None else None))
    rows.sort(key=lambda r: r[0])
    return rows


def pair(rows):
    """Enter and exit rows paired per thread: (t_enter, t_exit, pid, tid, nr, args, ret). An exit without its enter (the
    call began before the recording) and an enter without its exit (the recording stopped inside it) are counted."""
    pending, out, unpaired = {}, [], {"exit_without_enter": 0, "enter_without_exit": 0}
    for t, pid, tid, kind, nr, args, ret in rows:
        if kind == "enter":
            if tid in pending:
                unpaired["enter_without_exit"] += 1
            pending[tid] = (t, pid, nr, args)
        else:
            p = pending.pop(tid, None)
            if p is None or p[2] != nr:
                unpaired["exit_without_enter"] += 1
                continue
            out.append((p[0], t, pid, tid, nr, p[3], ret))
    unpaired["enter_without_exit"] += len(pending)
    out.sort(key=lambda c: c[0])
    return out, unpaired


def decode(pairs, compat_pids=()):
    """Calls with names and kinds. `compat_pids`: processes that run a 32-bit program (i386 table). A descriptor is a
    socket from the `socket` call that returned it, or once a socket-only call (connect, the receive and send calls)
    names it, until its `close`; `read`/`readv`/`write`/`writev` are socket receives and sends on a socket descriptor
    and file reads and writes on any other. Returns (calls sorted by entry, per-process counts of unknown numbers)."""
    compat = set(compat_pids)
    sockets = defaultdict(set)
    unknown = defaultdict(int)
    out = []
    for t0, t1, pid, tid, nr, args, ret in pairs:
        name = (I386 if pid in compat else X64).get(nr)
        if name is None:
            unknown[pid] += 1
            continue
        fd = args[0] if args else None
        if name == "socketcall":
            name = SOCKETCALL.get(args[0] if args else -1)
            fd = None
            if name is None:
                continue
        socks = sockets[pid]
        if name == "socket":
            kind = "socket"
            if ret is not None and ret >= 0:
                socks.add(ret)
        elif name == "connect":
            kind = "connect"
            if fd is not None:
                socks.add(fd)
        elif name == "close":
            kind = "close"
            socks.discard(fd)
        elif name in RECV or name in SEND:
            kind = "recv" if name in RECV else "send"
            if fd is not None:
                socks.add(fd)
        elif name in READ:
            kind = "recv" if fd in socks else "fread"
        elif name in WRITE:
            kind = "send" if fd in socks else "fwrite"
        elif name in POLL:
            kind = "poll"
        else:
            continue
        nbytes = ret if kind == "recv" and ret is not None and ret > 0 and name not in MSG_COUNT else None
        out.append(Call(t0, t1, pid, tid, name, fd, ret, kind, nbytes))
    return out, dict(unknown)


def by_tid(calls):
    d = defaultdict(list)
    for c in calls:
        d[c.tid].append(c)
    return d


class ThreadCalls:
    """One thread's calls, indexed by entry and by exit."""

    def __init__(self, calls):
        self.calls = sorted(calls, key=lambda c: c.t_enter)
        self.enters = [c.t_enter for c in self.calls]
        self.by_exit = sorted(self.calls, key=lambda c: c.t_exit)
        self.exits = [c.t_exit for c in self.by_exit]

    def spanning(self, t0, t1):
        """The call the thread slept inside: entered by the schedule-out t0, returned at or after the wakeup t1."""
        i = bisect.bisect_right(self.enters, t0 + EPS) - 1
        if i >= 0 and self.calls[i].t_exit >= t1 - EPS:
            return self.calls[i]
        return None

    def network_wait(self, t0, t1, t_bound):
        """Method §5, network wait: the interval (t0 schedule-out, t1 wakeup) ended with data arriving on a socket —
        the first receive call returning after the interval that returns data is on a socket, with no file read or
        write between; when the thread slept inside a poll-family call spanning the interval, that call returned a
        ready descriptor and such a receive follows it. The search ends at t_bound, the end of the wake that follows
        the interval: the data that ended the wait is read in the wake it caused, so the receive returns inside it.
        Returns (is_network, how) — how: 'recv' (the receive the thread slept in), 'poll', 'after' (a receive after
        the wakeup, the thread having slept in no recorded call), or the reason it is not."""
        span = self.spanning(t0, t1)
        if span is not None and span.kind == "poll":
            if span.ret is None or span.ret <= 0:
                return False, "poll-no-ready"
            start, how = span.t_exit + EPS, "poll"
        else:
            start, how = t1 - EPS, ("recv" if span is not None and span.kind == "recv" else "after")
        for k in range(bisect.bisect_left(self.exits, start), len(self.by_exit)):   # by index: a slice copies the tail
            c = self.by_exit[k]
            if c.t_exit > t_bound + EPS:
                break
            if c is span and how == "poll":
                continue
            if c.kind in ("fread", "fwrite"):
                return False, "file-io-first"
            if c.kind == "recv" and c.ret is not None and c.ret > 0:
                return True, how if c is span or how == "poll" else "after"
        return False, "no-receive"

    def received(self, t_from, t_to):
        """Bytes returned by the thread's socket receives whose return lies in [t_from, t_to); and the number of
        data-returning receives whose byte count is unknown (a message count)."""
        i, j = bisect.bisect_left(self.exits, t_from), bisect.bisect_left(self.exits, t_to)
        got, unknown = 0, 0
        for c in self.by_exit[i:j]:
            if c.kind == "recv" and c.ret is not None and c.ret > 0:
                if c.nbytes is None:
                    unknown += 1
                else:
                    got += c.nbytes
        return got, unknown


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "filter":
        print(filter_expr())
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
