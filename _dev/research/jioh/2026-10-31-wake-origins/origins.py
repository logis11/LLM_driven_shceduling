"""origins.py REPO OUT.json PHASES RUN_DIR — each application wake (analyze.py's wake definition) by the origin
of its wake chain: walking the wakeup events in time order, a wake by a thread of the application's tree takes the
origin of that thread's own last wake; otherwise the origin is the waker: timer (swapper — the wakeup ran in
interrupt context on an idle CPU), x (Xvfb/Xorg), irq (a kernel thread: kworker, ksoftirqd, ...), ext (any other
process), unknown (a tree thread not yet woken inside the capture). The X server relays as a tree thread does, its
origin its own last wake's; a harness process (xdotool, the driver) and the driver's channel into the
application (GIMP's Script-Fu server) are the origin input."""
import bisect, collections, importlib.util, json, os, re, sys
repo, out_path, phases, D = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4]
spec = importlib.util.spec_from_file_location("analyze", os.path.join(repo, "dataset/tools/meas/campaign/analyze.py"))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
KERNEL = re.compile(r"^(kworker|ksoftirqd|rcu|migration|irq/|kthreadd|watchdog|cpuhp|kcompactd|khugepaged|jbd2|kswapd|scsi_|nvme)")
report = json.load(open(os.path.join(D, "report.json")))
DRIVER = {"script-fu"}   # the measurement driver's channel into GIMP: unsharp mask runs through the Script-Fu server
result = []
for phase in phases:
    th = os.path.join(D, f"perf.{phase}.timehist.txt.gz"); wk = os.path.join(D, f"perf.{phase}.wakeups.txt.gz")
    if not (os.path.exists(th) and os.path.exists(wk)): continue
    pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p): pids |= {pr["pid"] for pr in json.load(open(p))["procs"]}
    segs, (t0, t1), extra = A.load_rows(th, pids, report.get("rx") if phase == "op" else None)
    tree = pids | set(extra)
    roles = A.pid_roles(D, phase)
    by_state = report.get("app") in A.STATE_WAKE_APPS and any(r.state for r in segs)
    rows, _ = A.merge_resumes(segs, A.load_all_wakeups(wk, tree), None, by_state)
    evs = []
    for line in A.open_text(wk):
        m = A.WAKE.match(line)
        if not m: continue
        t, cpu, waker, wakee = m.groups()
        km = A.TASK.match(wakee.strip())
        if not km: continue
        kpid = int(km.group(3)) if km.group(3) else int(km.group(2))
        if kpid not in tree: continue
        wm = A.TASK.match(waker.strip())
        wcomm = wm.group(1) if wm else waker.strip()
        wtid = int(wm.group(2)) if wm else -1
        wpid = (int(wm.group(3)) if wm.group(3) else wtid) if wm else -1
        evs.append((float(t), int(km.group(2)), wcomm, wtid, wpid))
    evs.sort()
    cause = {}; ev_by_tid = collections.defaultdict(list)
    for t, ktid, wcomm, wtid, wpid in evs:
        if wcomm in ("Xvfb", "Xorg"): c = cause.get(wtid, "x")     # the X server relays: its own last wake's origin
        elif wcomm in A.HARNESS_COMMS or wcomm in DRIVER: c = "input"                 # the measurement's input replay (xdotool) and driver
        elif wpid in tree: c = cause.get(wtid, "unknown")
        elif wcomm.startswith("swapper"): c = "timer"
        elif KERNEL.match(wcomm): c = "irq"
        else: c = "ext"
        cause[ktid] = c; ev_by_tid[ktid].append((t, c))
    prev = {}; comp = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
    for r in rows:
        key = A.component_name(roles.get(r.pid, "main"), r.comm)
        p = prev.get(r.tid); prev[r.tid] = r.t_in
        ev = ev_by_tid.get(r.tid, []); ts = [e[0] for e in ev]
        hi = bisect.bisect_right(ts, r.t_in + A.EPS); lo = bisect.bisect_right(ts, p) if p is not None else 0
        c = ev[hi - 1][1] if hi > lo else "none"
        comp[key][c][0] += 1; comp[key][c][1] += r.run
    result.append({"run": D, "app": report.get("app"), "repeat": report.get("repeat"), "phase": phase,
                   "span_s": t1 - t0, "components": {k: dict(d) for k, d in comp.items()}})
json.dump(result, open(out_path, "w"))
