"""The untraced control's shared core (_dev/docs/spec/jioh/task-9.5-untraced-control.md).

Each control job runs a carried phase as a traced run and an untraced run, snapshotting the application's threads at
each run's edges (probe/snapshot.py: every thread's schedstat runtime, switches and start time). Here: the per-thread
deltas over one run (decision 10: the threads alive at both edges), grouped by a family's key into components, a
component's wake rate and run mean per wake (decision 8), and a value's per-job ratios read as 9.7 D36 reads a check
(decisions 11, 12) — `check` of background/pool.py, with the two order groups' means beside it. The family adapters
(campaign/, desktop/, session/ control.py) supply the key and the carried components.
"""

import statistics

from meas.background.pool import check, ratio_by_repeat


def thread_deltas(before, after):
    """({(pid, tid, start_ticks): {pid, comm, run_ns, vol, invol}}, span_s) over the threads present at both edges; a
    tid reused within the run carries another start time, so the thread it names is not the one before."""
    first = {(p["pid"], t["tid"], t["start_ticks"]): t for p in before["procs"] for t in p.get("tasks", [])}
    out = {}
    for p in after["procs"]:
        for t in p.get("tasks", []):
            k = (p["pid"], t["tid"], t["start_ticks"])
            if k in first:
                a = first[k]
                out[k] = {"pid": p["pid"], "comm": t["comm"], "run_ns": t["run_ns"] - a["run_ns"],
                          "vol": t["vol"] - a["vol"], "invol": t["invol"] - a["invol"]}
    return out, after["t_mono"] - before["t_mono"]


def group(deltas, key):
    """{component: {run_ns, vol, invol, threads}}; key(pid, comm) names a thread's component, None drops it."""
    out = {}
    for d in deltas.values():
        c = key(d["pid"], d["comm"])
        if c is None:
            continue
        g = out.setdefault(c, {"run_ns": 0, "vol": 0, "invol": 0, "threads": 0})
        g["run_ns"] += d["run_ns"]; g["vol"] += d["vol"]; g["invol"] += d["invol"]; g["threads"] += 1
    return out


def rate_and_run(g, span_s):
    """(wakes per second, run mean in ms or None): voluntary switches over the span, CPU over voluntary switches."""
    rate = g["vol"] / span_s if span_s else None
    return (round(rate, 4) if rate is not None else None,
            round(g["run_ns"] / g["vol"] / 1e6, 6) if g["vol"] else None)


def read(pairs):
    """pairs {job: (order, traced, untraced)} -> check()'s reading of the per-job ratios untraced / traced (the
    pooled medians over every job's value beside it), plus the two order groups' mean ratios and the ratio count."""
    traced = {j: t for j, (_, t, _) in pairs.items() if t is not None}
    untraced = {j: u for j, (_, _, u) in pairs.items() if u is not None}
    ratios = ratio_by_repeat(untraced, traced)
    a = statistics.median(traced.values()) if traced else None
    b = statistics.median(untraced.values()) if untraced else None
    out = check(a, b, ratios)
    by_order = {}
    for j, (order, _, _) in pairs.items():
        if ratios.get(j) is not None:
            by_order.setdefault(order, []).append(ratios[j])
    out["order_means"] = {o: round(statistics.fmean(v), 4) for o, v in sorted(by_order.items())}
    out["n"] = sum(1 for v in ratios.values() if v is not None)
    return out


def alive(before, after):
    """{(pid, tid)} of the threads present at both edges of a run — the same thread, by its start time."""
    first = {(p["pid"], t["tid"], t["start_ticks"]) for p in before["procs"] for t in p.get("tasks", [])}
    return {(pid, tid) for p in after["procs"] for t in p.get("tasks", [])
            for pid, tid in [(p["pid"], t["tid"])] if (pid, tid, t["start_ticks"]) in first}


def shares(rows, key, comps, alive_ids, left=None):
    """{component: {"exited": (cpu share, wake share), "left": (cpu share, wake share) | None}} over a traced run's
    wake rows: `exited` the rows of threads not alive at both edges (decision 10), `left` the rows a rule read from the
    trace leaves out of the carried value (decision 22). key(row) names a row's component, None drops it; `residual`
    takes every kept row outside the other components."""
    named = [(key(r), r) for r in rows]
    out = {}
    for comp in comps:
        mine = [r for k, r in named if k is not None and (k == comp if comp != "residual" else k not in comps)]
        out[comp] = {"exited": _share(mine, lambda r: (r.pid, r.tid) not in alive_ids),
                     "left": _share(mine, left) if left else None}
    return out


def _share(rows, pred):
    cpu = sum(r.run for r in rows)
    hit = [r for r in rows if pred(r)]
    return (round(sum(r.run for r in hit) / cpu, 4) if cpu else None, round(len(hit) / len(rows), 4) if rows else None)


def workload(carried, ctl):
    """Decision 17, in the form of 9.5 D69 and D80: each carried value of the control's traced-run pool placed in the
    carried pool's per-repeat spread — z = (control mean − carried mean) / (carried cv × carried mean) — over the
    stability blocks' quantities, with the values found in one pool only listed."""
    a = (carried.get("stability") or {}).get("quantities") or {}
    b = (ctl.get("stability") or {}).get("quantities") or {}
    z = {}
    for name in sorted(a.keys() & b.keys()):
        m, cv = a[name].get("mean"), a[name].get("cv")
        if m and cv and b[name].get("mean") is not None:
            z[name] = round((b[name]["mean"] - m) / (cv * m), 2)
    return {"z": z, "only_carried": sorted(a.keys() - b.keys()), "only_control": sorted(b.keys() - a.keys()),
            "max_abs_z": max((abs(v) for v in z.values()), default=None)}
