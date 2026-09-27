"""9.8's adapter for the untraced control (_dev/docs/spec/jioh/task-9.5-untraced-control.md).

A control job's (traced, untraced) values for the subject's carried phase, keyed as desktop/analyze.py keys them. A
renderer subject's component is a thread comm of ONE page renderer, the renderers present pooled as samples of it
(analyze.renderer_components): its wake rate the mean over the renderers — one where the thread never woke counts at
zero — and its run mean the renderers' pooled CPU over their pooled wakes; a page renderer is a --type=renderer process
not listed as an extension or WebUI renderer in renderers.tsv (analyze.page_renderers), alive at both edges; the hidden
subject's control tab, the busiest renderer, is dropped (analyze.drop_control_tab, here by its switches). The other
subjects' components are thread comms over the tree.
"""

import json
import os
import statistics

from meas import control
from meas.campaign import analyze as a95
from meas.desktop import analyze as a98

CARRIED = {"chrome-hidden": "steady", "chrome-visible": "steady-notimer", "element": "idle", "steam": "shown"}
RUNS = ("traced", "untraced")
ZERO = {"run_ns": 0, "vol": 0, "invol": 0, "threads": 0}


def _kept(deltas):
    return {k: d for k, d in deltas.items() if d["comm"] not in a95.HARNESS_COMMS and not d["comm"].startswith("llvmpipe-")}


def _renderers(D, app, name, deltas):
    roles, page = a95.pid_roles(D, name), a98.page_renderers(D)
    pids = {k[0] for k in deltas if k[0] == k[1] and roles.get(k[0]) == a98.KEEP_ROLE and (page is None or k[0] in page)}
    if app == "chrome-hidden" and len(pids) >= 2:
        busy = {p: sum(d["vol"] + d["invol"] for k, d in deltas.items() if k[0] == p) for p in pids}
        pids.discard(max(busy, key=busy.get))
    return {p: control.group({k: d for k, d in deltas.items() if k[0] == p}, lambda pid, comm: comm) for p in pids}


def _pick(g, comp, selected):
    if comp != "residual":
        return g.get(comp) or ZERO
    rest = [c for k, c in g.items() if k not in selected]
    return {k: sum(x[k] for x in rest) for k in ZERO}


def job_values(D, app, carried):
    """(order, {value name: (traced, untraced)}) for one control job; `carried` is the subject's pooled entry."""
    report = json.load(open(os.path.join(D, "report.json")))
    phase = CARRIED[app]
    comps = (carried["phases"][phase].get("components") or {})
    selected = list(comps.get("selected") or [])
    names = selected + (["residual"] if comps.get("residual") else [])
    per = {}
    for run in RUNS:
        name = phase if run == "traced" else f"{phase}-untraced"
        load = lambda edge: json.load(open(os.path.join(D, f"snap.{name}.{edge}.json")))
        deltas, span = control.thread_deltas(load("before"), load("after"))
        deltas = _kept(deltas)
        per[run] = ((_renderers(D, app, name, deltas) if app in a98.RENDERER_APPS
                     else control.group(deltas, lambda pid, comm: comm)), span)
    vals = {}
    for comp in names:
        pair = {}
        for run in RUNS:
            data, span = per[run]
            if app in a98.RENDERER_APPS:
                cs = [_pick(g, comp, selected) for g in data.values()]
                vol, cpu = sum(c["vol"] for c in cs), sum(c["run_ns"] for c in cs)
                pair[run] = ((round(statistics.fmean(c["vol"] / span for c in cs), 4) if cs and span else None),
                             (round(cpu / vol / 1e6, 6) if vol else None))
            else:
                pair[run] = control.rate_and_run(_pick(data, comp, selected), span)
        vals[f"{phase} {comp} wakes/s"] = (pair["traced"][0], pair["untraced"][0])
        vals[f"{phase} {comp} run mean (ms)"] = (pair["traced"][1], pair["untraced"][1])
    return report.get("control.order"), vals
