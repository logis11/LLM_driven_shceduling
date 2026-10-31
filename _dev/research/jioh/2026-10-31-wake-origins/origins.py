"""origins.py REPO OUT.json PHASES RUN_DIR — each application wake (analyze.py's wake definition) by the origin
of its wake chain: walking the wakeup events in time order, a wake by a thread of the application's tree takes the
origin of that thread's own last wake; otherwise the origin is the waker: timer (swapper — the wakeup ran in
interrupt context on an idle CPU), x (the X server where its own wakes are not in the capture), irq (a kernel thread:
kworker, ksoftirqd, ...), ext (any other process), unknown (a tree thread not yet woken inside the capture). The X
server relays as a tree thread does, its origin its own last wake's, whether or not the snapshots hold it; a harness
process (xdotool, the driver) and the driver's channel into the application (GIMP's Script-Fu server) are the origin
input. The walk is analyze.py's (`load_origins`, `origins_at`)."""
import collections, importlib.util, json, os, sys
repo, out_path, phases, D = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4]
spec = importlib.util.spec_from_file_location("analyze", os.path.join(repo, "dataset/tools/meas/campaign/analyze.py"))
A = importlib.util.module_from_spec(spec); spec.loader.exec_module(A)
report = json.load(open(os.path.join(D, "report.json")))
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
    origins = A.load_origins(wk, tree)   # analyze.py's chain walk, the X server walked whatever the snapshots hold
    comp = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
    for r, c in zip(rows, A.origins_at(rows, origins)):
        key = A.component_name(roles.get(r.pid, "main"), r.comm)
        c = c or "none"
        comp[key][c][0] += 1; comp[key][c][1] += r.run
    result.append({"run": D, "app": report.get("app"), "repeat": report.get("repeat"), "phase": phase,
                   "span_s": t1 - t0, "components": {k: dict(d) for k, d in comp.items()}})
json.dump(result, open(out_path, "w"))
