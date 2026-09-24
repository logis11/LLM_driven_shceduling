#!/usr/bin/env python3
"""What caused each wake of an entry thread, and which wakes leave the component (changelog D27; method §5).

Every wake is traced to a cause through the trace itself, never through a time window:
  - its wakeup row names the waker: a thread, or `swapper` for a wakeup raised on an idle CPU — a timer or an
    interrupt, the thread's own;
  - a waker that is an entry's thread passes on the cause of the wake it was running in; a wake that follows a
    block inside the kernel (a switch-out in D: pid 1 waiting for an RCU grace period) continues the wake before it
    and carries its cause, as a resume after preemption does;
  - a waker the census never saw, a process born and gone inside the phase, is traced up the fork rows — a new
    task's first wakeup row names its creator as the waker — to a process the census places in a unit, or to the
    scheduler that launched it (pid 1, cron or anacron): a job, named by the programs its process tree ran or by
    cron's own CMD line in the journal;
  - a thread's idle-CPU wake at its component's fixed delay after its previous wake follows that wake's cause
    (FOLLOW_UP).

The cause is classed against Ubuntu 24.04's desktop package manifest (`ubuntu-24.04.5.1-desktop-amd64.manifest`,
releases.ubuntu.com, read 2026-09-24, SHA-256 6c200933618b2e382e7732b69b247aa5f63ed6600d8ee730d57b02ec74e4f8ff):
  own      the entry's own threads and timers              kept
  kernel   kernel threads                                  kept
  desktop  a desktop package's unit, or its job whose schedule recurs within the phase   kept
  outside  a package the manifest does not hold, or the harness                          leaves, stated
  event    a desktop job bound to a clock time (D23's form)                               leaves, stated
  unknown  a cause the trace does not resolve                                             kept, stated
"""

import bisect
import os
import re

from meas.campaign.analyze import TASK, WAKE, open_text

EPS = 2e-6            # timehist and the wakeup rows print whole microseconds

# Units whose processes wake the entries, by the package that ships them. Every package was checked against the
# manifest above; "outside" marks one it does not hold.
UNITS = {
    "systemd-oomd.service": ("systemd-oomd", "desktop"),
    "systemd-logind.service": ("systemd", "desktop"),
    "systemd-resolved.service": ("systemd-resolved", "desktop"),
    "systemd-journald.service": ("systemd", "desktop"),
    # kept by the package rule and stated: a stock desktop runs NetworkManager (network-manager is in the
    # manifest), and whether systemd-networkd also runs there is unverified
    "systemd-networkd.service": ("systemd", "desktop"),
    "systemd-udevd.service": ("udev", "desktop"),
    "udisks2.service": ("udisks2", "desktop"),
    "cron.service": ("cron", "desktop"),
    "evolution-calendar-factory.service": ("evolution-data-server", "desktop"),
    # anacron runs its daily jobs once a boot, after fixed delays: a clock event, not a recurring job
    "anacron.service": ("anacron", "event"),
    "php8.3-fpm.service": ("php8.3-fpm", "outside"),
    # the runner's agent, which runs the workflow's steps and through them run.sh and perf: the harness
    "hosted-compute-agent.service": ("the harness", "outside"),
}
UNIT_PREFIXES = (("app-gnome-org.gnome.Evolution\\x2dalarm\\x2dnotify-", ("evolution-data-server", "desktop")),)

# Scheduled jobs, named by any program their process tree ran (systemd names a unit's process `(<unit>)` before its
# exec, truncated to 15 characters) or by a fragment of cron's CMD line. A desktop job is kept only when its
# schedule recurs within the 1800 s phase — sysstat's collector, every 10 minutes (met 3 times in each of the 24
# repeats); every other desktop job is bound to a clock time (daily, weekly, twice a day, once a boot) and is an
# event. Checked in order: the summary before the collector.
JOBS = (
    ("sysstat-summary", ("(sa2)", "sa2", "sar.sysstat"), "sysstat", "event"),
    # sysstat's cron file: `debian-sa1 60 2` once a day at 23:59, `debian-sa1 1 1` every 10 minutes
    ("sysstat-daily-sample", ("debian-sa1 60 2",), "sysstat", "event"),
    ("sysstat-collect", ("(sa1)", "sa1", "sadc", "debian-sa1"), "sysstat", "desktop"),
    ("phpsessionclean", ("(ionclean)", "sessionclean", "phpquery", "/usr/lib/php/sessionclean"), "php-common",
     "outside"),
    ("podman", ("(podman)", "podman"), "podman", "outside"),
    ("sphinxsearch", ("indexer", "sphinxsearch"), "sphinxsearch", "outside"),
    ("dpkg-db-backup", ("(b-backup)", "dpkg-db-backup"), "dpkg", "event"),
    ("logrotate", ("(ogrotate)", "logrotate"), "logrotate", "event"),
    ("man-db", ("(mandb)", "mandb"), "man-db", "event"),
    ("fstrim", ("(fstrim)", "fstrim"), "util-linux", "event"),
    ("motd-news", ("(otd-news)", "50-motd-news"), "base-files", "event"),
    ("cron.hourly", ("/etc/cron.hourly",), "cron", "event"),
    ("anacron", ("0anacron", "/etc/cron.daily", "/etc/cron.weekly", "/etc/cron.monthly"), "anacron", "event"),
    # pid 1's own helper processes (asynchronous close, recursive removal): systemd's work, not a job's
    ("systemd helper", ("(sd-close)", "(sd-rmrf)", "(sd-sync)", "(sd-exec-strv)"), "systemd", "desktop"),
)

# A thread that arms a timer on being woken: its next wake, raised on an idle CPU this long after the wake that armed
# it, follows that wake's cause. WirePlumber's worker thread: 100.2 ms — 4316 of the workflow loop's 4320 wakes of it
# over the 24 repeats are followed by one at 100.17–100.25 ms (1st–99th percentile), and wakes from other causes by
# one at a median 100.20 ms.
FOLLOW_UP = {("pipewire", "wireplumber", "gmain"): (0.1002, 0.001)}

KEPT = ("own", "kernel", "desktop", "unknown")
CRON_CMD = re.compile(r"^\[\s*([\d.]+)\]\s+\S+\s+CRON\[(\d+)\]:\s+\((\S+)\)\s+CMD\s+\((.*)\)\s*$")


def unit_of(cgroup):
    for p in reversed([p for p in (cgroup or "").split("/") if p]):
        if p.endswith((".service", ".scope")):
            return p
    return "/"


def load_wakeup_rows(path):
    """Every wakeup row as (t, waker comm, waker tid, waker pid, wakee comm, wakee tid, wakee pid), in time order;
    a wakeup raised on an idle CPU has no waker thread (tid and pid None)."""
    out = []
    with open_text(path) as handle:
        for line in handle:
            m = WAKE.match(line)
            if not m:
                continue
            t, _cpu, waker, wakee = m.groups()
            km = TASK.match(wakee.strip())
            if not km:
                continue
            wm = TASK.match(waker.strip())
            wtid = int(wm.group(2)) if wm else None
            wpid = (int(wm.group(3)) if wm.group(3) else wtid) if wm else None
            ktid = int(km.group(2))
            kpid = int(km.group(3)) if km.group(3) else ktid
            out.append((float(t), (wm.group(1) if wm else waker.strip()).strip(), wtid, wpid,
                        km.group(1).strip(), ktid, kpid))
    out.sort(key=lambda w: w[0])
    return out


def cron_commands(path):
    """pid -> the command cron logged for it (`CRON[pid]: (user) CMD (...)`), from the followed journal."""
    out = {}
    if not path or not os.path.exists(path):
        return out
    for line in open(path, errors="replace"):
        m = CRON_CMD.match(line.rstrip("\n"))
        if m:
            out[int(m.group(2))] = m.group(4)
    return out


class Causes:
    """Trace each entry wake to its cause. `wakes`: the entry threads' wakes, one row per wake (resumes merged), in
    time order; `rows_cpu`: every task row of the trace; `procs`: pid -> census process (both censuses);
    `inst`: entry -> instance -> pids; `kthreads`: the census's kernel threads."""

    def __init__(self, wakes, wakeup_rows, rows_cpu, procs, inst, kthreads, kthread_name, cron_cmds):
        self.procs, self.kthreads, self.kthread_name, self.cron_cmds = procs, kthreads, kthread_name, cron_cmds
        self.entry_of = {pid: (e, i) for e, by in inst.items() for i, pids in by.items() for pid in pids}
        self.by_tid = {}
        for w in wakes:
            self.by_tid.setdefault(w.tid, []).append(w)
        self.starts = {tid: [w.t_in for w in ws] for tid, ws in self.by_tid.items()}
        self.rows_to = {}                     # entry tid -> [(t, waker comm, waker tid, waker pid)]
        self.parent, self.comms, seen = {}, {}, set()
        for t, wc, wt, wp, kc, kt, kp in wakeup_rows:
            if kp in self.entry_of:
                self.rows_to.setdefault(kt, []).append((t, wc, wt, wp))
            if wp is not None and not wc.startswith(":"):
                self.comms.setdefault(wp, set()).add(wc)
            if not kc.startswith(":"):
                self.comms.setdefault(kp, set()).add(kc)
            if kt not in seen and kp not in procs and wp is not None and wp != kp:
                self.parent.setdefault(kp, wp)    # a new task's first row: its creator woke it
            seen.add(kt)
        for r, _cpu in rows_cpu:
            if not r.comm.startswith(":"):
                self.comms.setdefault(r.pid, set()).add(r.comm)
        self.row_t = {tid: [x[0] for x in rs] for tid, rs in self.rows_to.items()}
        self.kids = {}
        for ch, pa in self.parent.items():
            self.kids.setdefault(pa, set()).add(ch)
        self.schedulers = {1} | {p for p, c in procs.items() if c.get("comm") in ("cron", "anacron")
                                 and unit_of(c.get("cgroup")) in ("cron.service", "anacron.service")}
        self.memo = {}

    # -- the waker's side -------------------------------------------------------------------------------------
    def classify_unit(self, unit):
        if unit == "/":
            return "kernel", "kernel (root cgroup)"
        if unit in UNITS:
            pkg, cls = UNITS[unit]
            return cls, f"{unit} ({pkg})"
        for prefix, (pkg, cls) in UNIT_PREFIXES:
            if unit.startswith(prefix):
                return cls, f"{unit} ({pkg})"
        return "unknown", f"unit {unit}"

    def job(self, root, scheduler):
        """A job by the programs its tree ran (exact names) or by cron's CMD line (a fragment of it)."""
        names, cmds, st = set(), [], [root]
        while st:
            p = st.pop()
            names |= self.comms.get(p, set())
            if p in self.cron_cmds:
                cmds.append(self.cron_cmds[p])
            st.extend(self.kids.get(p, ()))
        for name, marks, pkg, cls in JOBS:
            if any(n == m for n in names for m in marks) or any(m in c for c in cmds for m in marks):
                return cls, f"job {name} ({pkg})"
        who = "pid 1" if scheduler == 1 else unit_of(self.procs[scheduler].get("cgroup"))
        return "unknown", f"job launched by {who}: {' '.join(cmds + sorted(names))[:80]}"

    def process(self, pid, comm):
        if pid in self.kthreads or self.kthread_name.search(comm or ""):
            return "kernel", f"kernel thread {comm}"
        p, hops = pid, 0
        while p not in self.procs and hops < 30:
            pa = self.parent.get(p)
            if pa is None:
                return "unknown", f"unresolved process {comm}"
            if pa in self.schedulers:
                return self.job(p, pa)
            p, hops = pa, hops + 1
        if p not in self.procs:
            return "unknown", f"unresolved process {comm}"
        return self.classify_unit(unit_of(self.procs[p].get("cgroup")))

    # -- the wakee's side -------------------------------------------------------------------------------------
    def wake_at(self, tid, t):
        """The wake of an entry thread running at time t (the last one begun by then)."""
        i = bisect.bisect_right(self.starts.get(tid, []), t + EPS) - 1
        return (tid, i) if i >= 0 else None

    def cause(self, key, depth=0):
        """(class, label) of wake `key` = (tid, index into that thread's wakes)."""
        if key in self.memo:
            return self.memo[key]
        if depth > 12:
            return "unknown", "chain too deep"
        self.memo[key] = ("unknown", "cycle")
        tid, i = key
        w = self.by_tid[tid][i]
        prev = self.by_tid[tid][i - 1] if i > 0 else None
        if prev is not None and prev.state[:1] == "D":
            res = self.cause((tid, i - 1), depth + 1)     # continues the wake the kernel block interrupted
            self.memo[key] = res
            return res
        rows, ts = self.rows_to.get(tid, []), self.row_t.get(tid, [])
        j = bisect.bisect_right(ts, w.t_in + EPS) - 1
        if j < 0 or (prev is not None and ts[j] <= prev.t_in):
            res = ("unknown", "no wakeup row")
        else:
            t, wc, wt, wp = rows[j]
            if wp is None:
                res = ("own", "idle CPU (timer or interrupt)")
                e, inst = self.entry_of[w.pid]
                fu = FOLLOW_UP.get((e, inst, w.comm))
                if fu and prev is not None:
                    k = bisect.bisect_right(ts, prev.t_in + EPS) - 1
                    if k >= 0 and (i < 2 or ts[k] > self.by_tid[tid][i - 2].t_in) and abs(t - ts[k] - fu[0]) <= fu[1]:
                        res = self.cause((tid, i - 1), depth + 1)
            elif wp in self.entry_of:
                at = self.wake_at(wt, t)
                if at is None:
                    res = ("unknown", "entry waker with no wake")
                else:
                    cls, lab = self.cause(at, depth + 1)
                    we, wi = self.entry_of[wp]
                    if cls != "own":
                        res = (cls, lab)
                    elif we == self.entry_of[w.pid][0]:
                        res = ("own", f"own thread {wi}/{wc}")
                    else:     # another entry acting on its own: a desktop program's activity
                        res = ("desktop", f"entry {we} ({wi}/{wc}) on its own")
            else:
                res = self.process(wp, wc)
        self.memo[key] = res
        return res

    def split(self, rows):
        """(rows the component keeps, {class: {label: count}} for every row, [(t_in, class, label)] of the rows that
        leave)."""
        idx = {}
        for tid, ws in self.by_tid.items():
            for i, w in enumerate(ws):
                idx[(tid, w.t_in)] = i
        keep, tally, gone = [], {}, []
        for r in rows:
            i = idx.get((r.tid, r.t_in))
            cls, lab = self.cause((r.tid, i)) if i is not None else ("unknown", "not a traced wake")
            tally.setdefault(cls, {}).setdefault(lab, 0)
            tally[cls][lab] += 1
            (keep.append(r) if cls in KEPT else gone.append((r.t_in, cls, lab)))
        return keep, tally, gone
