"""9.5's adapter for the untraced control (_dev/docs/spec/jioh/task-9.5-untraced-control.md).

A control job's values, each a (traced, untraced) pair, at the grouping each carried value has (decision 7): the
components a carried phase selected and its residual, keyed as campaign/pool.py keys them — the process role with the
thread's comm (analyze.component_name), a Gecko pool's `#<n>` stripped (pool.component_key), the harness's comms and
the software rasteriser dropped as analyze.load_rows drops them, the roles the pool excluded dropped; and over the whole
tree, the typing entries' per-input run, the play phase's CPU share and the operation's duration.
"""

import json
import os
import statistics
import sys

from meas import control
from meas.campaign import analyze


def _campaign_pool():
    """campaign/pool.py imports its sibling with a flat `from analyze import ...`; the repo's idiom (desktop/pool.py)
    unbinds that name across the import."""
    import importlib
    saved = sys.modules.pop("analyze", None)
    try:
        return importlib.import_module("meas.campaign.pool")
    finally:
        if saved is not None:
            sys.modules["analyze"] = saved


_cp = _campaign_pool()
RUNS = ("traced", "untraced")


def _snaps(D, name):
    load = lambda edge: json.load(open(os.path.join(D, f"snap.{name}.{edge}.json")))
    return load("before"), load("after")


def _run_name(phase, run):
    return phase if run == "traced" else f"{phase}-untraced"


def keyer(D, app, name, exclude_roles):
    """key(pid, comm) for one run's snapshots: the pool's component name, or None for a thread the pool leaves out."""
    roles = analyze.pid_roles(D, name)

    def key(pid, comm):
        if comm in analyze.HARNESS_COMMS or comm.startswith("llvmpipe-"):
            return None
        role = roles.get(pid, "main")
        if role in exclude_roles:
            return None
        return analyze.component_name(role, _cp.component_key(app, comm))
    return key


def carried_components(app, phase, ph):
    """The components the fold-in carries for a phase (fold_in.components_block): the selected ones with a gap table,
    and `residual` when it has one; the driven phase's only for the pointer-loop entries, whose focus components they
    are — a typing entry carries its driven phase as the per-input run."""
    if phase == "driven" and app not in _cp.FOCUS_COMPONENTS:
        return []
    sel = ph.get("components") or {}
    out = [c for c in sel.get("selected", []) if ((ph.get("threads") or {}).get(c, {}).get("gap_ms") or {}).get("table")]
    if (sel.get("residual") or {}).get("gap_ms", {}).get("table"):
        out.append("residual")
    return out


def _tree(D, app, name, exclude_roles):
    before, after = _snaps(D, name)
    deltas, span = control.thread_deltas(before, after)
    g = control.group(deltas, keyer(D, app, name, exclude_roles))
    return g, span


def _ops_mean(D, run):
    path = os.path.join(D, "ops.jsonl" if run == "traced" else "ops-untraced.jsonl")
    if not os.path.exists(path):
        return None
    ms = [(r["done_us"] - r["trigger_us"]) / 1000 for r in map(json.loads, filter(str.strip, open(path))) if r.get("rc") == 0]
    return round(statistics.fmean(ms), 3) if ms else None


def job_values(D, app, carried):
    """(order, {value name: (traced, untraced)}) for one control job; `carried` is the app's pooled entry with the
    pool's `exclude_roles`."""
    report = json.load(open(os.path.join(D, "report.json")))
    excl = set(carried.get("exclude_roles") or ())
    vals, idle_rate = {}, {}
    per = {run: {} for run in RUNS}
    for phase in ("idle", "driven", "op", "play"):
        ph = carried["phases"].get(phase)
        if ph is None or not os.path.exists(os.path.join(D, f"snap.{_run_name(phase, 'traced')}.before.json")):
            continue
        comps = carried_components(app, phase, ph)
        for run in RUNS:
            g, span = _tree(D, app, _run_name(phase, run), excl)
            tree = sum(c["run_ns"] for c in g.values())
            per[run][phase] = (g, span, tree)
            if phase == "idle":
                idle_rate[run] = tree / span if span else None
        for comp in comps:
            pick = {}
            for run in RUNS:
                g, span, _ = per[run][phase]
                if comp == "residual":
                    rest = [c for k, c in g.items() if k not in comps]
                    c = {k: sum(x[k] for x in rest) for k in ("run_ns", "vol", "invol", "threads")}
                else:
                    c = g.get(comp)
                pick[run] = control.rate_and_run(c, span) if c else (None, None)
            vals[f"{phase} {comp} wakes/s"] = (pick["traced"][0], pick["untraced"][0])
            vals[f"{phase} {comp} run mean (ms)"] = (pick["traced"][1], pick["untraced"][1])
        if phase == "driven" and "per_input" in ph and app not in _cp.FOCUS_COMPONENTS:
            sent = {"traced": report.get("replay.sent"), "untraced": report.get("replay_untraced.sent")}
            pair = []
            for run in RUNS:
                _, span, tree = per[run]["driven"]
                n = int(sent[run] or 0)
                rate = idle_rate.get(run)
                pair.append(round((tree - rate * span) / 1e6 / n, 6) if n and rate is not None else None)
            vals["driven per-input run (ms)"] = tuple(pair)
        if phase == "play":
            vals["play CPU share"] = tuple(round(per[run]["play"][2] / 1e9 / per[run]["play"][1], 6) for run in RUNS)
        if phase == "op" and "operation" in ph:
            vals["op operation duration mean (ms)"] = (_ops_mean(D, "traced"), _ops_mean(D, "untraced"))
    return report.get("control.order"), vals


def shares(D, app, carried):
    """{"<phase> <component>": control.shares' record} over the traced runs' wake rows as the pool reads them
    (analyze.analyze_run, the pool's roles excluded): the threads not alive at both edges (decision 10), and the heavy
    event a component's value leaves out (HEAVY_EVENTS, 9.5 D64; decision 22)."""
    _, raw = analyze.analyze_run(D, exclude_roles=carried.get("exclude_roles") or ())
    out = {}
    for phase, r in raw["phases"].items():
        ph = carried["phases"].get(phase)
        comps = carried_components(app, phase, ph) if ph else []
        if not comps:
            continue
        before, after = _snaps(D, phase)
        roles = r["roles"]
        key = lambda row: analyze.component_name(roles.get(row.pid, "main"), _cp.component_key(app, row.comm))
        spec = _cp.HEAVY_EVENTS.get((app, phase))
        left = (lambda row: row.comm == spec[0] and row.run >= spec[1]) if spec else None
        for comp, rec in control.shares(r["rows"], key, comps, control.alive(before, after), left).items():
            out[f"{phase} {comp}"] = rec
    return out
