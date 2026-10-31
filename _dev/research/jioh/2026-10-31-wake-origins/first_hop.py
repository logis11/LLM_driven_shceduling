"""first_hop.py REPO OUT.json RUN_DIR... — each application wake (analyze.py's wake definition: a schedule-in
with a wakeup event since the thread's previous wake) classified by its waker, per run, phase and component.

waker classes: x (Xvfb/Xorg), idle (swapper: the wakeup ran in interrupt context on an idle CPU), tree (a thread
of the application's own process tree), kernel (kworker, ksoftirqd, rcu, irq/ and other kernel threads), other
(any other process). For `tree` wakes, `tree_same_cpu` counts those whose wakeup ran on the CPU the wakee last
ran on (where a timer armed by the wakee fires)."""
import bisect, collections, gzip, importlib.util, json, os, re, sys

repo, out_path, phases, run_dirs = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4:]
spec = importlib.util.spec_from_file_location("analyze", os.path.join(repo, "dataset/tools/meas/campaign/analyze.py"))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)

ROW = A.ROW; TASK = A.TASK; WAKE = A.WAKE
KERNEL = re.compile(r"^(kworker|ksoftirqd|rcu|migration|irq/|kthreadd|watchdog|cpuhp|kcompactd|khugepaged|jbd2|kswapd|scsi_|nvme|systemd-journal)")

def cls(wcomm, wpid, tree):
    if wcomm in ("Xvfb", "Xorg"): return "x"
    if wcomm.startswith("swapper"): return "idle"
    if wpid in tree: return "tree"
    if KERNEL.match(wcomm): return "kernel"
    return "other"

def cpu_rows(path, tree):
    """tid -> sorted [(t_in, cpu)] of every schedule-in of the tree's threads."""
    out = collections.defaultdict(list)
    with A.open_text(path) as h:
        for line in h:
            m = ROW.match(line)
            if not m: continue
            t, cpu, task, _, _, run, _ = m.groups()
            tm = TASK.match(task.strip())
            if not tm: continue
            a, b = int(tm.group(2)), tm.group(3)
            tid, pid = (a, int(b)) if b else (a, a)
            if pid in tree:
                out[tid].append((float(t) - float(run) / 1000, int(cpu)))
    for v in out.values(): v.sort()
    return out

def wakeups(path, tree):
    """wakee tid -> sorted [(t, cpu, waker comm, waker pid)]."""
    out = collections.defaultdict(list)
    with A.open_text(path) as h:
        for line in h:
            m = WAKE.match(line)
            if not m: continue
            t, cpu, waker, wakee = m.groups()
            km = TASK.match(wakee.strip())
            if not km: continue
            kpid = int(km.group(3)) if km.group(3) else int(km.group(2))
            if kpid not in tree: continue
            wm = TASK.match(waker.strip())
            wcomm = wm.group(1) if wm else waker.strip()
            wpid = (int(wm.group(3)) if wm.group(3) else int(wm.group(2))) if wm else -1
            out[int(km.group(2))].append((float(t), int(cpu), wcomm, wpid))
    for v in out.values(): v.sort()
    return out

result = []
for D in run_dirs:
    report = json.load(open(os.path.join(D, "report.json")))
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
        allw = A.load_all_wakeups(wk, tree)
        by_state = report.get("app") in A.STATE_WAKE_APPS and any(r.state for r in segs)
        rows, _ = A.merge_resumes(segs, allw, None, by_state)
        W = wakeups(wk, tree); C = cpu_rows(th, tree)
        prev_in = {}
        comp = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
        wakers = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
        for r in rows:
            key = A.component_name(roles.get(r.pid, "main"), r.comm)
            p = prev_in.get(r.tid); prev_in[r.tid] = r.t_in
            evs = W.get(r.tid, [])
            ts = [e[0] for e in evs]
            hi = bisect.bisect_right(ts, r.t_in + A.EPS)
            lo = bisect.bisect_right(ts, p) if p is not None else 0
            wname = "none"
            if hi > lo:
                t, cpu, wcomm, wpid = evs[hi - 1]
                c = cls(wcomm, wpid, tree)
                wname = (A.component_name(roles.get(wpid, "main"), wcomm) if c == "tree" else wcomm)
                if c == "tree":
                    cr = C.get(r.tid, []); k = bisect.bisect_left(cr, (r.t_in - A.EPS, -1)) - 1
                    if k >= 0 and cr[k][1] == cpu: c = "tree_same_cpu"
            else:
                c = "none"   # a state-decided wake with no wakeup event, or the thread's first segment
            comp[key][c][0] += 1; comp[key][c][1] += r.run
            wakers[key][wname][0] += 1; wakers[key][wname][1] += r.run
        result.append({"run": D, "app": report.get("app"), "repeat": report.get("repeat"), "phase": phase,
                       "span_s": t1 - t0,
                       "components": {k: {c: v for c, v in d.items()} for k, d in comp.items()},
                       "wakers": {k: dict(sorted(d.items(), key=lambda kv: -kv[1][0])[:12]) for k, d in wakers.items()}})
json.dump(result, open(out_path, "w"), indent=1)
print("runs", len(result))
