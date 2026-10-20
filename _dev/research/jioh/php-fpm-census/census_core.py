#!/usr/bin/env python3
"""The php-fpm census's shared core: each measured wake of a carried component traced to its cause through the
trace's wakeup rows, as `dataset/tools/meas/session/causes.py` traces the session entries' wakes (9.9 D27; method §5),
adapted to a campaign whose subject is one application's process tree and which records no process census.

What is reused unchanged: `causes.load_wakeup_rows` (the wakeup rows, waker and wakee), `causes.JOBS` (the scheduled
jobs, named by the programs their process tree ran) and the rules of `Causes.cause`:
  - a wakeup row whose waker is the idle task (`swapper`) is a timer or an interrupt: the thread's own;
  - a waker that is a thread of the measured tree passes on the cause of the wake it was running in;
  - a wake that follows a switch-out in D continues the wake before it (where the campaign recorded the state);
  - another dataset entry acting on its own — pid 1 or a `dbus-daemon` — is a desktop program's activity, and
    its wake is traced on through its own wakeup rows (in the session campaign those were entry threads);
  - a process born inside the phase is traced up its creator rows to pid 1, cron or anacron and named as a job.

What differs, and why:
  - no census of cgroups: a waker outside the tree is classed by its command name (`COMMS`) and, for a process born
    inside the phase, by its ancestry. Every package named in `COMMS` was looked up in the Ubuntu 24.04.5.1 desktop
    manifest (SHA-256 6c200933…f8ff, the copy under _dev/research/jioh/task-9.10-scenarios-timelines/sources/S2-01).
  - a born-inside process is recognised by the fork rows where the campaign records them (9.6, 9.7), else by its
    pid: above the pid of `perf-exec`, the tracer's own child at the trace's start (pids are handed out in increasing
    order and a runner never wraps them within a job).
  - a relay's (pid 1, dbus-daemon) current wake is the last wakeup row to that thread at or before the moment it
    acted; an `rcu_*` kernel thread's row there is a resume after an RCU wait and is stepped over, as the D rule does.
  - FOLLOW_UP (WirePlumber's 100.2 ms timer) names no application thread; no follow-up delay is applied.
  - a tree thread's first row, when the thread was created inside the phase by the harness, is the measured
    program's launch (a batch job's start by run.sh): `own`, labelled `launch`. Without it every wake of a batch
    tree, whose chains run back through its own threads to the start, would trace to the harness that started it.
  - the measured campaigns stand a few programs in for the desktop around the application: the X server (Xvfb), the
    window manager (openbox, 9.8), and the scripted peers that stand for the network's other end (the Matrix
    homeserver, Synapse, 9.8; the SMTP peer and the local page servers, 9.5). Their wakes are classed `stand-in`,
    counted apart from `outside`.

  - in a phase with a driver (an operation's, or the input replay's), a driver process started inside the phase
    wakes the tree with the phase's stimulus — the operation's trigger, the replayed input: `stimulus`.

Classes: own · kernel · desktop · stand-in · stimulus · outside · unknown. `outside` is what D27, D32 and D37 take out of a
session component: a package the manifest does not hold, a runner-only service, or the harness (the runner's agent,
the workflow's steps and loops, run.sh, the tracer and the input driver under them).
"""

import bisect
import collections
import os
import re
import sys

TOOLS = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/tools"
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.session.causes import JOBS, load_wakeup_rows  # noqa: E402

EPS = 2e-6

KTHREAD = re.compile(r"^(kworker/|ksoftirqd/|migration/|rcu_|rcuc/|rcuog/|rcuop/|cpuhp/|idle_inject/|irq/|kthreadd$|"
                     r"khugepaged$|kcompactd|kswapd|watchdog/|jbd2/|writeback|scsi_|kauditd$|hv_balloon|hv_vmbus|"
                     r"hv_pri_chan|hv_sub_chan|kblockd|oom_reaper|khungtaskd|psimon|ext4-rsv|kintegrityd|ksmd|"
                     r"pool_workqueue|kdevtmpfs|netns|inet_frag|kstrp|zswap|xenbus|card\d|ttm|nvme|ipv6_addrconf|"
                     r"mm_percpu_wq|blkcg_punt|tpm_dev|edac|devfreq|kthrotld|acpi_thermal|charger_manager|cryptd|"
                     r"ecryptfs|kaluad|ata_sff|md$|md_bitmap|raid5|dm_|kmpath|kpsmoused|vfio|scsi_eh|kmemleak|"
                     r"krfcommd|bluetooth|hci|nfit|pkt|iscsi|led_workqueue|ksgxd|slub_flushwq|events|kstrp|kerneloops$)")
# kerneloops is a userspace daemon in Ubuntu (desktop manifest), listed under COMMS before KTHREAD is consulted

# command name -> (package, class). A prefix match on the entries ending in '*'. Checked against the desktop manifest:
# "outside" marks a package the manifest does not hold, a runner-only service (D32, D37), or the harness.
COMMS = {
    # the four D27 names
    "php-fpm8.3": ("php8.3-fpm", "outside"),
    "php-fpm*": ("php8.3-fpm", "outside"),
    "sessionclean": ("php-common (PHP's session cleanup)", "outside"),
    "php8.3": ("php-common (PHP's session cleanup)", "outside"),
    "phpquery": ("php-common (PHP's session cleanup)", "outside"),
    "(ionclean)": ("php-common (PHP's session cleanup)", "outside"),
    "podman": ("podman", "outside"), "(podman)": ("podman", "outside"), "conmon": ("podman", "outside"),
    "crun": ("podman", "outside"), "catatonit": ("podman", "outside"), "netavark": ("podman", "outside"),
    "aardvark-dns": ("podman", "outside"), "rootlessport": ("podman", "outside"),
    "indexer": ("sphinxsearch", "outside"), "searchd": ("sphinxsearch", "outside"),
    # the harness: the runner's agent, its provisioner, the workflow's steps and loops, run.sh, the tracer, drivers
    ".NET*": ("the harness (runner agent, .NET)", "outside"),
    "Runner.Worker": ("the harness (runner agent)", "outside"),
    "Runner.Listener": ("the harness (runner agent)", "outside"),
    "provjobd*": ("the harness (runner provisioner)", "outside"),
    "hosted-compute-*": ("the harness (runner agent)", "outside"),
    "perf": ("the harness (tracer)", "outside"), "perf-exec": ("the harness (tracer)", "outside"),
    "xdotool": ("the harness (input driver)", "outside"),
    "bash": ("the harness (workflow step / run.sh)", "outside"), "sh": ("the harness (workflow step / run.sh)", "outside"),
    "sleep": ("the harness (workflow loop)", "outside"), "run.sh": ("the harness (run.sh)", "outside"),
    "phase.sh": ("the harness (run.sh)", "outside"), "timeout": ("the harness (run.sh)", "outside"),
    "sudo": ("the harness (run.sh)", "outside"), "gzip": ("the harness (run.sh)", "outside"),
    "tee": ("the harness (run.sh)", "outside"), "taskset": ("the harness (run.sh)", "outside"),
    "setsid": ("the harness (run.sh)", "outside"), "xwd": ("the harness (run.sh)", "outside"),
    "import": ("the harness (run.sh)", "outside"), "convert": ("the harness (run.sh)", "outside"),
    "pgrep": ("the harness (run.sh)", "outside"), "curl": ("the harness (run.sh)", "outside"),
    "grep": ("the harness (run.sh)", "outside"), "cat": ("the harness (run.sh)", "outside"),
    "kill": ("the harness (run.sh)", "outside"), "date": ("the harness (run.sh)", "outside"),
    "xprop": ("the harness (run.sh)", "outside"), "wmctrl": ("the harness (run.sh)", "outside"),
    "xwininfo": ("the harness (run.sh)", "outside"),
    "python3": ("python3 (a harness driver, the snapshot, or a scripted peer)", "harness-python"),
    "python": ("python (a harness driver or a scripted peer)", "harness-python"),
    # the measured campaigns' stand-ins for the desktop around the application
    "Xvfb": ("xvfb (the X server's stand-in; xserver-xorg-core and xwayland are in the manifest)", "stand-in"),
    "openbox": ("openbox (the window manager's stand-in)", "stand-in"),
    # runner-only services: packages the desktop manifest does not hold, or a unit a stock desktop leaves inactive
    "hv_kvp_daemon": ("hyperv-daemons (Azure VM)", "outside"), "hv_vss_daemon": ("hyperv-daemons (Azure VM)", "outside"),
    "hv_fcopy_daemon": ("hyperv-daemons (Azure VM)", "outside"),
    "multipathd": ("multipath-tools", "outside"),
    "containerd*": ("containerd", "outside"), "dockerd": ("docker.io", "outside"), "docker-proxy": ("docker.io", "outside"),
    "runc": ("runc", "outside"),
    "chronyd": ("chrony", "outside"), "haveged": ("haveged", "outside"), "waagent": ("walinuxagent", "outside"),
    "irqbalance": ("irqbalance", "outside"),
    "systemd-network": ("systemd (systemd-networkd, D37)", "outside"),
    "freshclam": ("clamav-freshclam", "outside"),
    "mono": ("mono (runner image)", "outside"),
    # desktop packages (in the manifest)
    "systemd-journal": ("systemd", "desktop"), "systemd-logind": ("systemd", "desktop"),
    "systemd-resolve": ("systemd-resolved", "desktop"), "systemd-udevd": ("udev", "desktop"),
    "systemd-oomd": ("systemd-oomd", "desktop"), "systemd-timesyn": ("systemd-timesyncd", "desktop"),
    "systemd-userwor": ("systemd", "desktop"), "systemd-userdbd": ("systemd", "desktop"),
    "(sd-close)": ("systemd", "desktop"), "(sd-rmrf)": ("systemd", "desktop"),
    "udisksd": ("udisks2", "desktop"), "NetworkManager": ("network-manager", "desktop"),
    "cron": ("cron", "desktop"), "rsyslogd": ("rsyslog", "desktop"), "in:imuxsock": ("rsyslog", "desktop"),
    "in:imklog": ("rsyslog", "desktop"), "rs:main Q:Reg": ("rsyslog", "desktop"),
    "snapd": ("snapd", "desktop"), "packagekitd": ("packagekit", "desktop"), "polkitd": ("polkitd", "desktop"),
    "accounts-daemon": ("accountsservice", "desktop"), "ModemManager": ("modemmanager", "desktop"),
    "avahi-daemon": ("avahi-daemon", "desktop"), "cupsd": ("cups-daemon", "desktop"),
    "unattended-upgr": ("unattended-upgrades", "desktop"), "package-data-do": ("update-notifier-common", "desktop"),
    "lsb_release": ("lsb-release", "desktop"), "kerneloops": ("kerneloops", "desktop"),
    "pipewire": ("pipewire", "desktop"), "wireplumber": ("wireplumber", "desktop"),
    "pipewire-pulse": ("pipewire-pulse", "desktop"), "dconf-service": ("dconf-service", "desktop"),
    "gvfsd": ("gvfs", "desktop"), "xdg-desktop-por": ("xdg-desktop-portal", "desktop"),
    "xdg-document-po": ("xdg-desktop-portal", "desktop"), "xdg-permission-": ("xdg-desktop-portal", "desktop"),
    "at-spi-bus-laun": ("at-spi2-core", "desktop"), "at-spi2-registr": ("at-spi2-core", "desktop"),
    "gnome-keyring-d": ("gnome-keyring", "desktop"), "snap": ("snapd", "desktop"), "snap-confine": ("snapd", "desktop"),
    "snap-update-ns": ("snapd", "desktop"), "update-notifier": ("update-notifier", "desktop"),
    "apt-get": ("apt", "desktop"), "apt": ("apt", "desktop"), "dpkg": ("dpkg", "desktop"),
    "rtkit-daemon": ("rtkit", "desktop"), "upowerd": ("upower", "desktop"), "thermald": ("thermald", "desktop"),
    "power-profiles-": ("power-profiles-daemon", "desktop"), "switcheroo-cont": ("switcheroo-control", "desktop"),
    "fwupd": ("fwupd", "desktop"), "colord": ("colord", "desktop"), "wpa_supplicant": ("wpasupplicant", "desktop"),
    "agetty": ("util-linux", "desktop"), "atd": ("at (runner image)", "outside"),
}
# relays: other dataset entries (pid 1, the buses); their own wake is traced on, and if it is their own, desktop
RELAY_COMMS = ("dbus-daemon", "systemd")


def iter_wakeup_rows(path):
    """`causes.load_wakeup_rows`, one row at a time and unsorted: a caller that keeps only some rows (a SteamCMD
    phase holds tens of millions) filters before it sorts."""
    from meas.campaign.analyze import TASK, WAKE, open_text
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
            yield (float(t), (wm.group(1) if wm else waker.strip()).strip(), wtid, wpid,
                   km.group(1).strip(), ktid, kpid)


def comm_class(comm):
    if comm in COMMS:
        return COMMS[comm]
    for k, v in COMMS.items():
        if k.endswith("*") and comm.startswith(k[:-1]):
            return v
    if KTHREAD.search(comm or ""):
        return ("kernel", "kernel")
    return (comm, "unknown")


class Tracer:
    """`wakeup_rows`: causes.load_wakeup_rows over the phase. `tree`: the measured tree's pids. `wakes_by_tid`: the
    tree's merged wakes (campaign.analyze Row: t_in, run, comm, tid, pid, state), in time order, per thread — every
    wake of the phase, not only the carried ones, so each wake's predecessor is the one the analysis saw.
    `peers`: {pid: label} of scripted peers known by their pid file."""

    def __init__(self, wakeup_rows, tree, wakes_by_tid, peers=None, born=None, drivers=()):
        self.tree, self.peers, self.drivers = set(tree), dict(peers or {}), tuple(drivers)
        self.wakes = wakes_by_tid
        self.starts = {tid: [w.t_in for w in ws] for tid, ws in wakes_by_tid.items()}
        self.rows_to = collections.defaultdict(list)
        self.comms = collections.defaultdict(set)
        threshold = None
        for t, wc, wt, wp, kc, kt, kp in wakeup_rows:
            if threshold is None and kc == "perf-exec":
                threshold = kp
        self.threshold = threshold if threshold is not None else 10 ** 9
        # tids created inside the phase: the fork rows where the campaign records them (9.6, 9.7), else every tid above
        # perf-exec's
        self.born = (lambda x: x in born) if born is not None else (lambda x: x > self.threshold)
        self.parent, seen = {}, set()
        for t, wc, wt, wp, kc, kt, kp in wakeup_rows:
            if kp in self.tree or kp == 1 or kc in RELAY_COMMS:   # the threads a chain is followed through
                self.rows_to[kt].append((t, wc, wt, wp))
            if wp is not None and not wc.startswith(":"):
                self.comms[wp].add(wc)
            if not kc.startswith(":"):
                self.comms[kp].add(kc)
            if kt not in seen and self.born(kp) and kt == kp and wp is not None and wp != kp:
                self.parent.setdefault(kp, wp)
            seen.add(kt)
        self.row_t = {tid: [x[0] for x in rs] for tid, rs in self.rows_to.items()}
        self.kids = collections.defaultdict(set)
        for ch, pa in self.parent.items():
            self.kids[pa].add(ch)
        self.memo = {}

    # -- a waker outside the tree --------------------------------------------------------------------------------
    def job(self, root, scheduler_comm):
        names, st = set(), [root]
        while st:
            p = st.pop()
            names |= self.comms.get(p, set())
            st.extend(self.kids.get(p, ()))
        for name, marks, pkg, cls in JOBS:
            if any(n == m for n in names for m in marks):
                return cls, f"job {name} ({pkg})"
        for n in sorted(names):
            pkg, cls = comm_class(n)
            if cls == "outside":
                return "outside", f"job of {pkg} ({n})"
        return "unknown", f"job launched by {scheduler_comm}: {' '.join(sorted(names))[:80]}"

    def process(self, pid, comm):
        if pid in self.peers:
            return "stand-in", self.peers[pid]
        if comm in self.drivers and self.born(pid):
            # the phase's own driver — the operation driver of an `op` phase, the replay driver of a driven phase —
            # started inside the phase: its wakes are the operation's trigger or the input, the phase's stimulus
            return "stimulus", f"the phase's driver ({comm}, started in the phase)"
        # a process born inside the phase: up its creators to a scheduler (a job) or to a long-lived ancestor
        chain, p, hops = [], pid, 0
        while p in self.parent and hops < 40:
            pa = self.parent[p]
            pa_comms = self.comms.get(pa, set())
            if pa == 1 or pa_comms & {"cron", "anacron"}:
                return self.job(p, "pid 1" if pa == 1 else "cron")
            chain.append(pa)
            p, hops = pa, hops + 1
        if p != pid:   # the long-lived ancestor names the cause: the harness's shell, a service
            for c in sorted(self.comms.get(p, set())):
                pkg, cls = comm_class(c)
                if cls in ("outside", "desktop", "stand-in", "harness-python"):
                    return cls, f"{pkg} (via {c}[{p}])"
            if p in self.peers:
                return "stand-in", self.peers[p]
        pkg, cls = comm_class(comm)
        if cls == "kernel":
            return "kernel", f"kernel thread {comm}"
        return cls, pkg

    # -- the chain ---------------------------------------------------------------------------------------------
    def row_before(self, tid, t, after=None):
        ts = self.row_t.get(tid, [])
        j = bisect.bisect_right(ts, t + EPS) - 1
        if j < 0 or (after is not None and ts[j] <= after):
            return None
        return j

    def cause_row(self, tid, j, depth):
        """The cause of row j to thread tid."""
        key = ("row", tid, j)
        if key in self.memo:
            return self.memo[key]
        if depth > 25:
            return "unknown", "chain too deep"
        self.memo[key] = ("unknown", "cycle")
        t, wc, wt, wp = self.rows_to[tid][j]
        if wp is None:
            res = ("own", "idle CPU (timer or interrupt)")
        elif wp in self.tree:
            res = self.cause_tree_thread_at(wt, t, depth + 1)
            if res[0] == "own":
                res = ("own", "own thread")
        elif wp == 1 or wc in RELAY_COMMS:
            k = self.row_before(wt, t)
            while k is not None and k > 0 and self.rows_to[wt][k][1].startswith("rcu_"):
                k -= 1     # a resume after an RCU wait continues the wake before it
            if k is None:
                res = ("desktop", f"{wc} on its own (no earlier row)")
            else:
                res = self.cause_row(wt, k, depth + 1)
                if res[0] in ("own", "kernel"):
                    res = ("desktop", f"{wc}{'[1]' if wp == 1 else ''} on its own")
        else:
            res = self.process(wp, wc)
            if j == 0 and self.born(tid) and res[0] == "outside" and res[1].startswith("the harness"):
                # the measured program's own launch: its first row, raised by the harness that started it, is the
                # subject's arrival, not a wake the harness adds to it (a chain through the tree ends here)
                res = ("own", f"launch, by {res[1]}")
        self.memo[key] = res
        return res

    def cause_tree_thread_at(self, tid, t, depth):
        """The cause of the wake a tree thread was running in at time t."""
        ws = self.starts.get(tid)
        if ws:
            i = bisect.bisect_right(ws, t + EPS) - 1
            if i >= 0:
                return self.cause_wake(tid, i, depth)
        j = self.row_before(tid, t)
        if j is None:
            return "own", "tree thread, no earlier row"
        return self.cause_row(tid, j, depth)

    def cause_wake(self, tid, i, depth=0):
        key = ("wake", tid, i)
        if key in self.memo:
            return self.memo[key]
        if depth > 25:
            return "unknown", "chain too deep"
        self.memo[key] = ("unknown", "cycle")
        ws = self.wakes[tid]
        w = ws[i]
        prev = ws[i - 1] if i > 0 else None
        if prev is not None and (getattr(prev, "state", "") or "")[:1] == "D":
            res = self.cause_wake(tid, i - 1, depth + 1)
        else:
            j = self.row_before(tid, w.t_in, prev.t_in if prev is not None else None)
            res = ("unknown", "no wakeup row") if j is None else self.cause_row(tid, j, depth + 1)
        self.memo[key] = res
        return res

    def classify(self, rows):
        """[(row, class, label)] for the given wakes (each one of `wakes_by_tid`)."""
        idx = {(tid, w.t_in): i for tid, ws in self.wakes.items() for i, w in enumerate(ws)}
        out = []
        for r in rows:
            i = idx.get((r.tid, r.t_in))
            cls, lab = self.cause_wake(r.tid, i) if i is not None else ("unknown", "not a traced wake")
            out.append((r, cls, lab))
        return out


def by_tid(rows):
    d = collections.defaultdict(list)
    for r in sorted(rows, key=lambda r: r.t_in):
        d[r.tid].append(r)
    return d


def read_pid(path):
    try:
        return int(open(path).read().strip())
    except (OSError, ValueError):
        return None
