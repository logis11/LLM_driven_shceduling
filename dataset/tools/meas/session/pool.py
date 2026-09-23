#!/usr/bin/env python3
"""Pool the repeats of the 9.9 session campaign and evaluate the stability rule (changelog D8–D14; method §5, §6).

  pool.py <artifacts-dir> <out.json> [--md results.md] [--cpu-model TEXT] [--tag TAG]

Structured on `desktop/pool.py`; the coverage cut, the residual and the tables are `campaign/pool.py`'s, imported.
One subject, `session`, carries four entries — GNOME Shell, the PipeWire stack, `systemd`, `dbus-daemon` — each
pooled on its own components (`<instance>/<comm>`), its own 95 % cut and its own residual (method §5: no pooling
across entries or instances).

Reasons a repeat does not enter the pool:
  - the machine gate stopped it, or the run stopped it at the steady edge (`not-idle`) or earlier;
  - its mode is `probe`: the long-phase probe is never a repeat (method §1);
  - user-space work other than the four entries' — a pinned unit's other process included — took more than
    `FOREIGN_CPU_SHARE_BOUND` of the measured CPU during `steady` (D12, D15, amended by D20).
"""

import argparse
import glob
import json
import os
import re
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.session import analyze  # noqa: E402
from meas.stability import stability, TOLERANCE  # noqa: E402
from meas.desktop.pool import _campaign_pool, repeat_order  # noqa: E402

_cp = _campaign_pool()
select_components = _cp.select_components

APPS = ("session",)
NAME = re.compile(r"^meas-session-(session)-r(\d+)-(dry|probe|full)$")
POOLED_MODES = ("dry", "full")          # `probe` is parsed so it can be reported, never pooled
CARRIED = "steady"
LIST_FIELDS = (("wakes_per_s", "wakes/s"), ("gap_ms", "gap mean (ms)"), ("run_ms", "run mean (ms)"))
ABS_FLOOR_MS = 0.001        # the trace's resolution, as campaign/pool.py uses

# D20: the gate is a bound on how much of the measured CPU foreign user-space work took, not an absolute. Both
# managers' `init.scope` are on the measured CPU because both managers are entries, so every process the system
# starts is forked there and no placement can move it: the 2026-09-23 probes found no window of 600 s or more
# without some. The bound is a share of the steady phase's wall time, set from the unpolled probes and written
# into method §5 before the first batch. `None` until then: no repeat is pooled without it.
FOREIGN_CPU_SHARE_BOUND = None
MIN_REPEATS = 5             # method §6 item 3


def find_runs(root, cpu_model):
    """As `desktop/pool.py`: every repeat obtained is pooled; an index that landed more than once is keyed
    `<index>@<run id>` per landing."""
    runs, gated, other, probes = {}, [], [], []
    for d in sorted(glob.glob(os.path.join(root, "**", "meas-session-*"), recursive=True)):
        m = NAME.match(os.path.basename(d))
        if not m or not os.path.exists(os.path.join(d, "report.json")):
            continue
        app, k, mode = m.group(1), int(m.group(2)), m.group(3)
        rpt = json.load(open(os.path.join(d, "report.json")))
        rel = os.path.relpath(d, root)
        if mode not in POOLED_MODES:
            probes.append({"app": app, "repeat": k, "mode": mode, "path": rel})
            continue
        if rpt.get("gate") != "open":
            gated.append({"app": app, "repeat": k, "gate": rpt.get("gate"),
                          "cpu_model": rpt.get("machine.model"), "path": rel})
            continue
        spec_p = os.path.join(d, "spec.json")
        spec = json.load(open(spec_p)) if os.path.exists(spec_p) else {}
        model = spec.get("cpu_model") or ""
        if cpu_model and cpu_model not in model:
            other.append({"app": app, "repeat": k, "cpu_model": model, "path": rel})
            continue
        run_id = str((spec.get("github_run") or {}).get("GITHUB_RUN_ID") or os.path.basename(os.path.dirname(d)))
        runs.setdefault(app, {}).setdefault(k, []).append((run_id, {"dir": d, "mode": mode, "report": rpt, "spec": spec}))
    keyed = {}
    for app, by_k in runs.items():
        for k, landings in by_k.items():
            for run_id, info in landings:
                keyed.setdefault(app, {})[k if len(landings) == 1 else f"{k}@{run_id}"] = info
    return keyed, gated, other, probes


def pool_entry(name, by_rep):
    """by_rep: {k -> the entry's phase record}. The components, the residual and the tables, as desktop/pool.py
    builds them for a non-renderer subject."""
    reps = sorted(by_rep, key=repeat_order)
    comms, spans = {}, {}
    for k in reps:
        e = by_rep[k]
        spans[k] = e["span_s"]
        for comm, c in e["threads"].items():
            slot = comms.setdefault(comm, {"gaps": {}, "runs": {}, "t_in": {}, "wakes": {}, "threads": {}})
            slot["wakes"][k] = int(round(c["wakes_per_s"] * e["span_s"]))
            slot["threads"][k] = c["threads"]
            sm = (e.get("_samples") or {}).get(comm) or {}
            slot["gaps"][k], slot["runs"][k], slot["t_in"][k] = sm.get("gaps", []), sm.get("runs", []), sm.get("t_in", [])
    chosen, residual, cov = select_components(comms, spans, reps)
    at = lambda comm, f: [by_rep[k]["threads"][comm][f] for k in reps if comm in by_rep[k]["threads"]]
    return {
        "repeats": reps,
        "span_s": [spans[k] for k in reps],
        "wakes_per_s": [by_rep[k]["wakes_per_s"] for k in reps],
        "cpu_share": [by_rep[k]["cpu_share"] for k in reps],
        "instances": {k: by_rep[k]["instances"] for k in reps},
        "threads": {comm: {f: at(comm, f) for f in ("threads", "wakes_per_s", "gap_ms", "run_ms")}
                    for comm in sorted({c for k in reps for c in by_rep[k]["threads"]})},
        "components": {"selected": chosen, "residual": residual, **cov},
        "tables": {c: {"gap_ms": _cp.summary([comms[c]["gaps"].get(k, []) for k in reps]),
                       "run_ms": _cp.summary([comms[c]["runs"].get(k, []) for k in reps])} for c in chosen},
    }


def criterion(pooled):
    """Method §6 item 1: per entry, per carried component and the residual, the wake rate, gap mean and run mean,
    each by its per-repeat mean; the standing tolerance, no exception invoked in advance."""
    out = {}
    for name, ph in pooled.items():
        comps = [(c, ph["threads"][c]) for c in ph["components"]["selected"] if c in ph["threads"]]
        residual = ph["components"].get("residual")
        if not comps and not residual:     # an entry with nothing to carry cannot pass the rule
            out[f"{name} (no components)"] = {"k": len(ph["repeats"]), "mean": None, "half_width": None, "passes": False}
            continue
        for comm, c in comps + ([("residual", residual)] if residual else []):
            for field, label in LIST_FIELDS:
                if field == "wakes_per_s":
                    vals, floor = c.get("wakes_per_s") or [], None
                elif comm == "residual":
                    vals, floor = (c.get(field) or {}).get("repeat_mean") or [], ABS_FLOOR_MS
                else:
                    vals, floor = [x.get("mean") if x else None for x in c.get(field) or []], ABS_FLOOR_MS
                if not vals:
                    continue
                out[f"{name} {comm} {label}"] = {**stability(vals, floor, MIN_REPEATS, keep_zero=True),
                                                 "needed": _cp.repeats_needed(vals, floor)}
    return {"tolerance": TOLERANCE, "abs_floor_ms": ABS_FLOOR_MS, "min_repeats": MIN_REPEATS, "quantities": out,
            "passes": bool(out) and all(c["passes"] for c in out.values())}


def pool_app(app, reps):
    entry = {"family": "session", "repeats": [], "mode": None, "cpu_model": {}, "kernel": {}, "run_id": {},
             "versions": {}, "foreign_user": [], "foreign": {}, "display_servers": {}, "in_unit_other": {},
             "phases": {}}
    by_entry = {}
    for k in sorted(reps, key=repeat_order):
        info = reps[k]
        res = analyze.analyze_run_dir(info["dir"], (CARRIED,))
        ph = res["phases"].get(CARRIED) or {}
        if ph.get("missing"):
            continue
        f = ph["foreign"]
        entry["foreign"][k] = {x: {"schedule_ins": f[x]["schedule_ins"], "cpu_ms": f[x]["cpu_ms"]} for x in f}
        # D12, D15, D20: user space outside the entries, the pinned units' other processes included, gates a
        # repeat when it took more than the bound of the measured CPU over the phase
        ins = f["user"]["schedule_ins"] + f["in_unit_other"]["schedule_ins"]
        share = (f["user"]["cpu_ms"] + f["in_unit_other"]["cpu_ms"]) / 1000.0 / max(ph["span_s"], 1e-9)
        entry["foreign"][k]["share_of_phase"] = share
        if FOREIGN_CPU_SHARE_BOUND is None or share > FOREIGN_CPU_SHARE_BOUND:
            entry["foreign_user"].append({
                "repeat": k, "schedule_ins": ins, "share_of_phase": share, "bound": FOREIGN_CPU_SHARE_BOUND,
                "why": "no bound set (D20): none is pooled until method §5 states one"
                       if FOREIGN_CPU_SHARE_BOUND is None else "over the bound",
                "by_comm": {**f["user"]["by_comm"], **f["in_unit_other"]["by_comm"]}})
            continue
        entry["repeats"].append(k)
        entry["mode"] = info["mode"]
        entry["cpu_model"][k] = info["spec"].get("cpu_model")
        entry["kernel"][k] = info["report"].get("kernel")
        entry["run_id"][k] = (info["spec"].get("github_run") or {}).get("GITHUB_RUN_ID")
        entry["versions"][k] = {x[len("version."):]: v for x, v in info["report"].items() if x.startswith("version.")}
        entry["display_servers"][k] = ph["display_servers"]
        entry["in_unit_other"][k] = ph["in_unit_other"]
        for name, e in ph["entries"].items():
            by_entry.setdefault(name, {})[k] = e
    pooled = {name: pool_entry(name, by_rep) for name, by_rep in by_entry.items()}
    entry["phases"][CARRIED] = {"entries": pooled}
    entry["stability"] = criterion(pooled)
    return entry


def render(out):
    L = [f"# 9.9 session campaign — pooled results ({out.get('tag') or 'untagged'})", "",
         f"Machine: {out.get('machine')}. `probe` jobs are never repeats.", ""]
    for app, e in sorted(out["runs"].items()):
        L += [f"Repeats: {e['repeats']}  ·  mode {e['mode']}", ""]
        if e["foreign_user"]:
            L += [f"Left out, user-space work on the measured CPU over the bound "
                  f"{FOREIGN_CPU_SHARE_BOUND} (D12, D20): "
                  + ", ".join(f"r{x['repeat']} {x['share_of_phase'] * 100:.4f}% ({x['why']})"
                              for x in e["foreign_user"]), ""]
        kern = {k: v["kernel"]["schedule_ins"] for k, v in e["foreign"].items()}
        L += [f"Kernel-thread schedule-ins on the measured CPU per repeat (D14, reported): {kern}", ""]
        for name, ph in e["phases"][CARRIED]["entries"].items():
            c = ph["components"]
            L += [f"## {name}", "", f"Components {c['selected']} cover {c['covered_share']} of "
                  f"{c['total_wakes_per_s']} wakes/s; residual {bool(c['residual'])}; sporadic {c['sporadic']}", ""]
        L += ["| quantity | k | mean | half-width | passes |", "|---|---|---|---|---|"]
        for name, c in e["stability"]["quantities"].items():
            hw = f"{c['half_width']:.1%}" if c.get("half_width") is not None else "—"
            L.append(f"| {name} | {c['k']} | {c['mean']} | ±{hw} | {'yes' if c['passes'] else 'no'} |")
        L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts")
    ap.add_argument("out")
    ap.add_argument("--md")
    ap.add_argument("--cpu-model", default="")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    runs, gated, other, probes = find_runs(a.artifacts, a.cpu_model)
    if not runs:
        print("no repeats found", file=sys.stderr)
        raise SystemExit(1)
    out = {"tag": a.tag, "machine": a.cpu_model or None, "gated_out": gated, "other_machine": other,
           "probe_jobs": probes, "runs": {}}
    for app, reps in sorted(runs.items()):
        entry = pool_app(app, reps)
        out["runs"][app] = entry
        st = entry["stability"]
        print(f"== {app}: repeats {entry['repeats']}  stability {'passes' if st['passes'] else 'does not hold'}"
              f"  left out (foreign work) {len(entry['foreign_user'])}")
    json.dump(out, open(a.out, "w"), indent=1, default=list)
    if a.md:
        open(a.md, "w").write(render(out))


if __name__ == "__main__":
    main()
