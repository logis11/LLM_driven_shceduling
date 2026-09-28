#!/usr/bin/env python3
"""The untraced control's operation passes read by operation (9.5 D87). Each control job runs the operation phase
twice and traces one pass, the first or the second (`control.order`); the traced pass's rows inside its operations,
as the pool reads them, are read as `meas/windows.py` reads a carried operation phase — in time windows and one by
one — and pooled over the jobs that traced the same pass. The threads a stated line names (`control_report.
NOTES_STATED`) are read under their own names, every other row as `other`. Per job, each named thread's wakes in the
pass's first operations one by one, and its wake rate over the rest.

control_passes.py <artifacts> <out.json> [--md PAGE] [--app APP]...
"""

import argparse
import json
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas import windows  # noqa: E402

# the threads the web-browser and mail-client lines name
STATED = {"chrome": ("utility/ThreadPoolForeg",), "thunderbird-send": ("Socket Thread", "TaskCon~ller")}
FIRST = 3               # the operations read one by one per job; the rest read as one rate


def pass_of(order):
    return {"traced untraced": "first", "untraced traced": "second"}[order]


def first_and_rest(by_op, name, first=FIRST):
    """One job's by-operation reading: the name's wakes in each of its first operations, and its wake rate over the
    rest of the operations' time."""
    n, w, secs = by_op
    head = [w.get(k, {}).get(name, [0, 0.0])[0] for k in range(min(first, n))]
    wakes = sum(w.get(k, {}).get(name, [0, 0.0])[0] for k in range(first, n))
    s = sum(secs.get(k, 0.0) for k in range(first, n))
    return head, (wakes / s if s else None)


def job_reading(D, app, pooled, names):
    """The traced pass of one control job: (by time, by operation, window s), rows named as the pool names them."""
    from meas import burstiness as b
    from meas.campaign.analyze import analyze_run, component_name
    cp = b._campaign_pool_module()
    _, raw = analyze_run(D, pooled.get("w_ms", 5.0), pooled.get("cap_ms", 0.0),
                         exclude_roles=tuple(pooled.get("exclude_roles") or ()))
    pd = raw["phases"]["op"]
    rows, _ = cp.split_events(app, "op", pd["operation"]["inside"])
    named = []
    for r in rows:
        name = component_name(pd["roles"].get(r.pid, "main"), cp.component_key(app, r.comm))
        named.append((name if name in names else "other", r.t_in, r.run))
    win = windows.window_of(pd["span"])
    return windows.read_ops(named, pd["operation"]["windows"], pd["t0"], pd["span"], win) + (win,)


def entries(root, apps=()):
    from meas import control_report as cr
    jobs, lib, out = cr.find_jobs("campaign", root), windows._library(), {}
    for app, names in STATED.items():
        if apps and app not in apps:
            continue
        arch = cr.ARCH_95[app]
        (op_name, _), = lib[arch]["params"]["operations"].items()
        pooled = json.load(open(os.path.join(cr.POOL_95[app], f"pool-{app}.json")))
        by = {"first": [], "second": []}
        for k, D in sorted(jobs[app].items(), key=lambda kv: int(str(kv[0]).split("@")[0])):
            order = json.load(open(os.path.join(D, "report.json")))["control.order"]
            by[pass_of(order)].append((k, *job_reading(D, app, pooled, names)))
            print(f"{app} control r{k}", file=sys.stderr)
        e = {"archetype": arch, "app": app, "operation": op_name, "stated": list(names), "passes": {}}
        for p, js in by.items():
            if not js:
                continue
            ent = windows.pool([t for _, t, _, _ in js], js[0][3])
            ent["by_operation"] = windows.pool([o for _, _, o, _ in js], None)
            ent["jobs"] = {str(k): {name: dict(zip(("first", "rest_wakes_per_s"), first_and_rest(o, name))) for name in names}
                           for k, _, o, _ in js}
            e["passes"][p] = ent
        out[arch] = e
    return out


def render(record):
    lines = ["# The untraced control's operation passes, by operation", ""]
    for arch, e in record["archetypes"].items():
        lines += [f"## {arch} (`{e['app']}`, the `{e['operation']}` operation's two passes)", "",
                  "Each control job traces one of its two passes; the traced pass's rows inside the operations, pooled "
                  "over the jobs that traced it. " + ", ".join(f"`{n}`" for n in e["stated"])
                  + " read under their own names, every other thread as `other`.", ""]
        for p, ent in e["passes"].items():
            n = ent["by_operation"]["windows"]
            size = -(-n // windows.BLOCKS)
            per = ("Per thread: each {0}'s wake rate over the thread's mean over the {0}s, each {0}'s run mean (ms), its "
                   "share of the pass's CPU, and the CPU its {0}s hold above its median {0} as a share of the pass's CPU.")
            jobs = sorted(ent["jobs"], key=lambda k: int(k.split("@")[0]))
            lines += [f"### The {p} pass traced ({'job' if len(jobs) == 1 else 'jobs'} {', '.join(jobs)})", "",
                      f"{ent['windows']} whole windows of {ent['win_s']:g} s, each holding the operations triggered in "
                      "it, read over their time. " + per.format("window"), ""] + windows._table(ent, "window") + [
                      "", f"By operation, in blocks of {size} ({n} operations a pass{windows._remainder(n, size)}), each "
                      "block read over its operations' time. " + per.format("block"), ""] + windows._table(
                      windows.blocks(ent["by_operation"], size), "block") + [""]
            for name in e["stated"]:
                lines += [f"`{name}` per job: its wakes in each of the pass's first {FIRST} operations, and its wake "
                          f"rate over the rest (/s).", "", "| job | wakes in operations 1–3 | wakes/s after |",
                          "|---|---|---|"]
                for k in jobs:
                    j = ent["jobs"][k][name]
                    lines.append(f"| {k} | " + " · ".join(str(x) for x in j["first"]) + " | "
                                 f"{windows._f(j['rest_wakes_per_s'], 1)} |")
                lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--md")
    ap.add_argument("--app", action="append", default=[])
    a = ap.parse_args()
    record = {"archetypes": entries(a.artifacts, tuple(a.app))}
    json.dump(record, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(record))


if __name__ == "__main__":
    main()
