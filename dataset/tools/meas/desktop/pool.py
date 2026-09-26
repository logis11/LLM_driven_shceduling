#!/usr/bin/env python3
"""Pool the repeats of the 9.8 desktop campaign and evaluate the stability rule (changelog D13; method §5, §6).

  pool.py <artifacts-dir> <out.json> [--md results.md] [--cpu-model TEXT] [--tag TAG]

Structured on `background/pool.py`, whose `find_runs`, module-level list and `render` are the shape a new family
needs; `campaign/pool.py`'s discovery and per-app pooling live inside its `main()` with nothing to reuse. The
component selection is imported from `campaign/pool.py` all the same, so the coverage cut and the residual are
computed exactly as they were for `web-browser`, the other half of the same application.

Three reasons a repeat does not enter the pool:
  - the machine gate stopped it (another CPU model), as in every campaign of this phase;
  - its mode is `probe`: the long-phase probe is never a repeat (method §1);
  - for `chrome-hidden`, intensive throttling did not engage. That is knowable only from the trace, which is why
    it is gated here and not in `run.sh` (decision 9): a renderer past the grace wakes about once a minute, so a
    steady phase whose renderers wake far faster measured an unthrottled page and describes nothing the entry
    claims.
"""

import argparse
import glob
import json
import os
import re
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.desktop import analyze  # noqa: E402
from meas.campaign.analyze import pct  # noqa: E402
from meas.stability import stability, ratio_stability, ratio_repeats_needed, TOLERANCE  # noqa: E402
from meas.distribution import circular_gaps  # noqa: E402


def _campaign_pool():
    """`campaign/pool.py` imports its sibling with a flat `from analyze import ...`, so it picks up whatever is
    bound to `analyze` — `meas/build/analyze.py` or `meas/analyze.py` in a process that imported one first. The
    repo's idiom for reaching it is to unbind the name across the import (tests/test_meas.py)."""
    import importlib
    saved = sys.modules.pop("analyze", None)
    try:
        return importlib.import_module("meas.campaign.pool")
    finally:
        if saved is not None:
            sys.modules["analyze"] = saved


_cp = _campaign_pool()
# the coverage cut and the residual exactly as `web-browser` — the other half of the same application — was pooled
QUANTILE_PROBS, select_components = _cp.QUANTILE_PROBS, _cp.select_components

APPS = ("chrome-hidden", "chrome-visible", "element", "steam")
NAME = re.compile(r"^meas-desktop-(chrome-hidden|chrome-visible|element|steam)-r(\d+)-(dry|probe|full)$")
POOLED_MODES = ("dry", "full")          # `probe` is parsed so it can be reported, never pooled

# the phase each entry reads. The visible entry reads the no-timer phase where that phase yields enough and the
# timer phase otherwise (method §2 subject 3, §9); until the probe settles it, both are pooled and the entry's
# choice is recorded at the fold-in.
CARRIED = {"chrome-hidden": ("steady",),
           "chrome-visible": ("steady-notimer", "steady-timer"),
           "element": ("idle",),
           "steam": ("shown",)}

# the list: every value the fold-in carries (method §6 item 1) — per carried component of the carried phase and for
# the residual, its wake rate by its per-repeat values, its gap mean and run mean as the pooled tables carry them
# (count-weighted over the repeats), as campaign/pool.py tests 9.5's entries. Thread counts are carried as their
# observed range and are deliberately absent.
LIST_FIELDS = (("wakes_per_s", "wakes/s"), ("gap_ms", "gap mean (ms)"), ("run_ms", "run mean (ms)"))

# changelog D17, the rule's exception (measurement-campaign workflow; 9.6 D29): run times move together across every
# thread of a repeat — a per-runner speed on one CPU model — while wake rates hold within about 1 %. For these
# subjects every run mean, the residual's included, is carried over at least five repeats with its half-width and
# range instead of the tolerance. Steam joins them by D18: its shown-against-minimised comparison (D5) is stated on
# the wake-rate ratio, and the CPU-share ratio is reported with its spread with no effect resting on it, so no
# reported effect rests on its run times either.
EXCEPTED_RUN_MEANS = ("chrome-hidden", "chrome-visible", "element", "steam")

# changelog D21, 9.5 D57's exception: a component whose rate varies between sessions is carried with its half-widths
# over at least five repeats, its three values together. Extended by D21 to the visible renderer's ThreadPoolForeg,
# whose spread is in part within a run (about six wakes per renderer per phase) — both spreads and that limitation
# are stated in the entry's scope (D20 holds the measurement).
# changelog D24: the hidden renderer's Chrome_ChildIOT, a separate component once all 14 landings are pooled — ±17.7 %
# within a run against ±76.9 % between runs, 9.5 D57 as written, as D21 found for the visible renderer's
SESSION_SPREAD = {"chrome-hidden": ("Chrome_ChildIOT",
                                    # changelog D26: carried once the rates are one renderer's and exact
                                    "Compositor", "PerfettoTrace", "ThreadPoolServi"),
                  "chrome-visible": ("Chrome_ChildIOT", "ThreadPoolForeg", "PerfettoTrace")}
# changelog D26: the Steam client's steamwebhelper and ThreadPoolForeg, carried between sessions under D23, hold the
# rule over merged wake times; steamwebhelper's run mean stays carried, under D18

# changelog D27: a sparse component — one that wakes a few times per renderer per phase (hidden residual, MemoryInfra
# alone, 1.2–3.4 wakes; visible residual, four comms, 3.6–5.5) — is carried with its half-widths over at least five
# repeats, its three values together, and its count stated. Its spread is the count's own: a 600 s window of the
# long-phase probe catches 0–2 of its wakes, so the within-run test cannot place the spread and 9.5 D57 does not
# apply (D26 re-read the residuals under D21 and D24 and found neither placed). The residuals were carried between
# sessions from D21 to D26.
SPARSE = {"chrome-hidden": ("residual",), "chrome-visible": ("residual",)}

# results only: (a, b, what) — the two comparisons the slice reports (method §6 item 2)
COMPARISONS = {"chrome-hidden": [], "chrome-visible": [("steady-timer", "steady-notimer", "timer against no timer")],
               "element": [("idle", "traffic", "idle against scripted traffic (D11; feeds no archetype)")],
               "steam": [("shown", "minimised", "shown against minimised (D5)")]}

ABS_FLOOR_MS = 0.001        # the trace's resolution, as campaign/pool.py uses
MIN_REPEATS = 5             # method §6 item 3
THROTTLED_WAKES_PER_S_MAX = 0.5   # a renderer past the grace wakes ~1/min; 0.5/s is thirty times that


def qtable(values):
    if not values:
        return None
    v = sorted(values)
    return [round(pct(v, q), 4) for q in QUANTILE_PROBS]


def repeat_order(k):
    """Sort key for a repeat: its index, then the run of one landing of an index that landed more than once."""
    i, _, run = str(k).partition("@")
    return int(i), run


def find_runs(root, cpu_model):
    """Every repeat obtained is pooled (campaign workflow: "Every same-machine repeat obtained is pooled and
    reported"). A repeat is keyed by its index; when an index landed more than once — a retry relaunched while an
    earlier launch of it was still queued — every landing of it is keyed `<index>@<run id>`, never the latest alone."""
    runs, gated, other, probes = {}, [], [], []
    for d in sorted(glob.glob(os.path.join(root, "**", "meas-desktop-*"), recursive=True)):
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


def renderer_residual(rest, comms, spans, by_rep, cov):
    """The residual of ONE renderer (changelog D19). `select_components` merges the residual comms' wake times over
    everything it is given, which for a renderer entry is every measured renderer at once: its rate came out N times
    a renderer's and its gaps interleaved N processes, where the selected components are one renderer's with the
    renderers pooled as samples (D14). Here the residual comms are merged within each renderer, gaps are taken
    within each renderer, and the renderers pooled as samples: the rate is the mean over the renderers measured,
    and the gap and run tables are over every renderer's samples together. A residual without two wakes in some
    repeat is reported as sporadic and not carried, as D43 has it."""
    reps = sorted(by_rep, key=repeat_order)
    gaps_by_rep, runs_by_rep, rate_by_rep, share_by_rep, threads_by_rep = [], [], [], [], []
    for k in reps:
        n = by_rep[k].get("renderers_measured") or 1
        by_pid = {pid: [] for pid in by_rep[k].get("measured_renderer_pids") or []}
        for c in rest:
            for pid, ts in (comms[c]["t_in_by_pid"].get(k) or {}).items():
                by_pid.setdefault(pid, []).extend(ts)
        t0 = by_rep[k]["t0"]
        # merged within each renderer, every renderer measured laid end to end and wrapped round (a renderer the
        # residual never woke in adds its time), so the gaps imply the per-renderer rate
        gaps = [g * 1000 for g in circular_gaps([(ts, t0, t0 + spans[k]) for ts in by_pid.values()])]
        runs = [x for c in rest for x in comms[c]["runs"].get(k, [])]
        wakes = sum(len(ts) for ts in by_pid.values())
        gaps_by_rep.append(gaps); runs_by_rep.append(runs)
        rate_by_rep.append(wakes / spans[k] / n)
        share_by_rep.append(round(sum(runs) / 1000 / spans[k] / n, 6))
        threads_by_rep.append(sum(comms[c]["threads"].get(k, 0) for c in rest))
    residual = {"comms": rest, "threads": threads_by_rep, "wakes_per_s": rate_by_rep, "cpu_share": share_by_rep,
                "gap_ms": _cp.summary(gaps_by_rep), "run_ms": _cp.summary(runs_by_rep), "per_renderer": True}
    if not all(n >= 2 for n in (sum(len(ts) for c in rest for ts in (comms[c]["t_in_by_pid"].get(k) or {}).values())
                                for k in reps)):
        cov.setdefault("sporadic", []).append({"comm": "residual", "comms": rest,
                                               "repeats": [k for k, w in zip(reps, rate_by_rep) if w]})
        return None
    return residual


def throttling_check(app, res):
    """chrome-hidden only: did intensive throttling engage in the carried phase? Returns (ok, wakes_per_s).

    The control tab is excluded. It carries the same timer and, being the selected tab, stays visible to Blink
    and is never throttled (method §2 subject 1) — it is the reference the run identifies the throttled
    renderers against, at 55x the next. `per_pid_wakes_per_s` is computed before it is dropped, so reading the
    raw map here tested the one renderer that cannot pass, and rejected every repeat whose renderers did
    throttle.
    """
    if app != "chrome-hidden":
        return True, None
    ph = res["phases"].get(CARRIED[app][0]) or {}
    per_pid = dict(ph.get("per_pid_wakes_per_s") or {})
    control = (ph.get("control_tab") or {}).get("dropped")
    if control is not None:
        per_pid.pop(str(control), None)
    if not per_pid:
        return False, None
    worst = max(per_pid.values())
    return worst <= THROTTLED_WAKES_PER_S_MAX, worst


def pool_app(app, reps):
    """reps: {k -> info}. Returns the entry, plus the repeats left out for not throttling."""
    entry = {"family": "desktop", "repeats": [], "mode": None, "cpu_model": {}, "kernel": {}, "run_id": {},
             "version": {}, "origins": {}, "renderers": {}, "phases": {}, "not_throttled": []}
    per_phase = {}
    for k in sorted(reps, key=repeat_order):
        info = reps[k]
        res = analyze.analyze_run_dir(info["dir"])
        ok, worst = throttling_check(app, res)
        if not ok:
            entry["not_throttled"].append({"repeat": k, "worst_renderer_wakes_per_s": worst,
                                           "limit": THROTTLED_WAKES_PER_S_MAX})
            continue
        entry["repeats"].append(k)
        entry["mode"] = info["mode"]
        entry["cpu_model"][k] = info["spec"].get("cpu_model")
        entry["kernel"][k] = info["report"].get("kernel")
        entry["run_id"][k] = (info["spec"].get("github_run") or {}).get("GITHUB_RUN_ID")
        entry["version"][k] = info["report"].get("version")
        entry["origins"][k] = info["report"].get("settings.origins")
        entry["renderers"][k] = info["report"].get("renderers.observed")
        for name, ph in res["phases"].items():
            if ph.get("missing"):
                continue
            per_phase.setdefault(name, {})[k] = ph

    for name, by_rep in per_phase.items():
        comms, spans, wps = {}, {}, {}
        for k, ph in by_rep.items():
            spans[k] = ph["span_s"]
            wps[k] = ph["wakes_per_s"]
            for comm, c in ph["threads"].items():
                slot = comms.setdefault(comm, {"gaps": {}, "runs": {}, "t_in": {}, "t_in_by_pid": {}, "wakes": {},
                                               "count": {}, "threads": {}})
                sm = (ph.get("_samples") or {}).get(comm) or {}
                # the exact count, never a rate rounded and multiplied back (9.9 D24's correction, applied here too);
                # for a renderer entry the count of ONE renderer — the mean over every renderer measured (D14)
                slot["wakes"][k] = len(sm.get("runs") or []) / ((ph.get("renderers_measured") or 1)
                                                                 if app in analyze.RENDERER_APPS else 1)
                slot["count"][k] = len(sm.get("runs") or [])   # across the renderers measured: what 9.5 D43 reads
                # per-renderer components carry a thread count per renderer; the selector wants one number
                t = c["threads"]
                slot["threads"][k] = (max(t) if isinstance(t, list) and t else 0) if isinstance(t, list) else t
                slot["gaps"][k] = sm.get("gaps", [])
                slot["runs"][k] = sm.get("runs", [])
                slot["t_in"][k] = sm.get("t_in", [])
                slot["t_in_by_pid"][k] = sm.get("t_in_by_pid", {})
        chosen, residual, cov = select_components(comms, spans, sorted(by_rep, key=repeat_order),
                                                  {k: [(ph["t0"], ph["t0"] + ph["span_s"])] for k, ph in by_rep.items()})
        if app in analyze.RENDERER_APPS and residual:
            residual = renderer_residual(residual["comms"], comms, spans, by_rep, cov)
        entry["phases"][name] = {
            "repeats": sorted(by_rep, key=repeat_order),
            "span_s": [by_rep[k]["span_s"] for k in sorted(by_rep, key=repeat_order)],
            "wakes_per_s": [wps[k] for k in sorted(by_rep, key=repeat_order)],
            "wakes_per_s_per_renderer": [by_rep[k].get("wakes_per_s_per_renderer") for k in sorted(by_rep, key=repeat_order)],
            "renderers_measured": [by_rep[k].get("renderers_measured") for k in sorted(by_rep, key=repeat_order)],
            "cpu_share": [by_rep[k]["cpu_share"] for k in sorted(by_rep, key=repeat_order)],
            "threads": {comm: {
                "threads": [by_rep[k]["threads"][comm]["threads"] for k in sorted(by_rep, key=repeat_order) if comm in by_rep[k]["threads"]],
                "renderers": [by_rep[k]["threads"][comm].get("renderers") for k in sorted(by_rep, key=repeat_order) if comm in by_rep[k]["threads"]],
                "wakes_per_s": [by_rep[k]["threads"][comm]["wakes_per_s"] for k in sorted(by_rep, key=repeat_order) if comm in by_rep[k]["threads"]],
                "wakes_per_s_per_renderer": [by_rep[k]["threads"][comm].get("wakes_per_s_per_renderer")
                                             for k in sorted(by_rep, key=repeat_order) if comm in by_rep[k]["threads"]],
                "gap_ms": [by_rep[k]["threads"][comm]["gap_ms"] for k in sorted(by_rep, key=repeat_order) if comm in by_rep[k]["threads"]],
                "run_ms": [by_rep[k]["threads"][comm]["run_ms"] for k in sorted(by_rep, key=repeat_order) if comm in by_rep[k]["threads"]],
            } for comm in sorted({c for k in by_rep for c in by_rep[k]["threads"]})},
            "control_tab": {k: by_rep[k].get("control_tab") for k in sorted(by_rep, key=repeat_order)},
            "components": {"selected": chosen, "residual": residual, **cov},
            # each selected component's pooled gap and run tables, every repeat's samples together — what the fold-in
            # carries (D10), built with the summary `campaign/pool.py` builds 9.5's tables with
            "tables": {c: {"gap_ms": _cp.summary([comms[c]["gaps"].get(k, []) for k in sorted(by_rep, key=repeat_order)]),
                           "run_ms": _cp.summary([comms[c]["runs"].get(k, []) for k in sorted(by_rep, key=repeat_order)])}
                       for c in chosen},
            "renderer_pids": {k: by_rep[k].get("renderer_pids") for k in sorted(by_rep, key=repeat_order)},
        }
    # the population the entry is pooled from (D14 hands to 9.13 that each entry's scope states it): the renderers
    # measured in the carried phase, after the browser's own renderers, part-phase renderers and the control tab are
    # dropped — `renderers` above is the raw `--type=renderer` count the job observed, which includes all of those
    carried = entry["phases"].get(CARRIED[app][0]) or {}
    entry["renderers_measured"] = dict(zip(carried.get("repeats", []), carried.get("renderers_measured", [])))
    entry["stability"] = criterion(app, entry)
    return entry


def criterion(app, entry):
    """The list of method §6 item 1 over the carried phase: for every selected component and for the residual, its
    wake rate by its per-repeat values, its gap mean and run mean as its pooled tables carry them — count-weighted
    over the repeats, the half-width the ratio estimator's (`campaign/pool.py`'s `table_pairs`) — the list
    `campaign/pool.py` tests for 9.5's entries.

    An earlier version tested three numbers per phase — the per-renderer wake rate and the unweighted means of the
    components' gap and run means. That average gave a component waking a handful of times a phase the weight of
    one waking every ten seconds, let a failing component sit behind stable ones, and left the residual untested:
    on the first batch it passed `element`, where 6 of its 15 per-component values fail.

    For the renderer entries every rate here is already per renderer — components are computed per renderer
    process and pooled as its samples (changelog D14) — so nothing is divided by N.
    """
    out = {}
    phase = CARRIED[app][0]
    ph = entry["phases"].get(phase)
    if ph:
        comps = [(c, ph["threads"][c]) for c in ph["components"]["selected"] if c in ph["threads"]]
        residual = ph["components"].get("residual")
        for comm, c in comps + ([("residual", residual)] if residual else []):
            for field, label in LIST_FIELDS:
                if field == "wakes_per_s":
                    vals = c.get("wakes_per_s") or []
                    if not vals:
                        continue
                    c_ = {**stability(vals, None, MIN_REPEATS, keep_zero=True), "needed": _cp.repeats_needed(vals)}
                else:
                    table = (c if comm == "residual" else (ph.get("tables") or {}).get(comm) or {}).get(field)
                    if not table:
                        continue
                    sums, counts = _cp.table_pairs(table)
                    c_ = {**ratio_stability(sums, counts, ABS_FLOOR_MS, MIN_REPEATS),
                          "needed": ratio_repeats_needed(sums, counts, ABS_FLOOR_MS, MIN_REPEATS)}
                c_["excepted"] = field == "run_ms" and app in EXCEPTED_RUN_MEANS          # D17
                c_["session_spread"] = comm in SESSION_SPREAD.get(app, ())                 # D21
                c_["sparse"] = comm in SPARSE.get(app, ())                                 # D27
                c_["carried"] = c_["passes"] or ((c_["excepted"] or c_["session_spread"] or c_["sparse"])
                                                 and c_["k"] >= MIN_REPEATS)
                out[f"{phase} {comm} {label}"] = c_
    passes = bool(out) and all(c["carried"] for c in out.values())
    return {"tolerance": TOLERANCE, "abs_floor_ms": ABS_FLOOR_MS, "min_repeats": MIN_REPEATS,
            "quantities": out, "passes": passes}


def comparisons(app, entry):
    out = []
    for a, b, what in COMPARISONS.get(app, []):
        pa, pb = entry["phases"].get(a), entry["phases"].get(b)
        if not pa or not pb:
            continue
        # for the renderer entries the comparison is between one renderer's rates, not between the sums over N
        key = "wakes_per_s_per_renderer" if app in ("chrome-hidden", "chrome-visible") else "wakes_per_s"
        va = [x for x in pa.get(key) or [] if x is not None]
        vb = [x for x in pb.get(key) or [] if x is not None]
        ma = statistics.fmean(va) if va else None
        mb = statistics.fmean(vb) if vb else None
        ratio = (ma / mb) if (ma and mb) else None
        # CPU share beside the rate: D5 asks whether the helper's behaviour changes when the window is hidden,
        # and the dry run moved share 2.6x while the rate moved 1.25x — the rate alone understates it
        ca = [x for x in pa.get("cpu_share") or [] if x is not None]
        cb = [x for x in pb.get("cpu_share") or [] if x is not None]
        sa = statistics.fmean(ca) if ca else None
        sb = statistics.fmean(cb) if cb else None
        cpu_ratio = (sa / sb) if (sa and sb) else None
        # method §6 item 2: a difference under 10 % is reported as not resolved at this tolerance, not as an effect
        def read(r):
            return None if not r else ("not resolved" if 0.9 < r < 1.1 else "difference")
        out.append({"a": a, "b": b, "what": what, "a_wakes_per_s": ma, "b_wakes_per_s": mb,
                    "ratio": round(ratio, 3) if ratio else None, "reading": read(ratio),
                    "a_cpu_share": sa, "b_cpu_share": sb,
                    "cpu_share_ratio": round(cpu_ratio, 3) if cpu_ratio else None,
                    "cpu_share_reading": read(cpu_ratio)})
    return out


def render(out):
    L = [f"# 9.8 desktop campaign — pooled results ({out.get('tag') or 'untagged'})", "",
         f"Machine: {out.get('machine')}. Repeats pooled per subject; `probe` jobs are never repeats.", ""]
    for app, e in sorted(out["runs"].items()):
        pop = (f"renderers measured {e['renderers_measured']} (observed {e['renderers']})"
               if any(e.get("renderers_measured", {}).values()) else "")
        L += [f"## {app}", "", f"Repeats: {e['repeats']}  ·  mode {e['mode']}" + (f"  ·  {pop}" if pop else ""), ""]
        if e["not_throttled"]:
            L += [f"Left out, intensive throttling did not engage: {e['not_throttled']}", ""]
        L += ["| quantity | k | mean | half-width | passes |", "|---|---|---|---|---|"]
        for name, c in e["stability"]["quantities"].items():
            hw = f"{c['half_width']:.1%}" if c.get("half_width") is not None else "—"
            L.append(f"| {name} | {c['k']} | {c['mean']} | ±{hw} | {'yes' if c['passes'] else 'no'} |")
        L.append("")
        if e.get("comparisons"):
            L += ["| comparison | wakes/s a | wakes/s b | ratio | reading | cpu share a | cpu share b | ratio | reading |",
                  "|---|---|---|---|---|---|---|---|---|"]
            for c in e["comparisons"]:
                L.append(f"| {c['what']} | {c['a_wakes_per_s']} | {c['b_wakes_per_s']} | {c['ratio']} | {c['reading']} "
                         f"| {c['a_cpu_share']} | {c['b_cpu_share']} | {c['cpu_share_ratio']} | {c['cpu_share_reading']} |")
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
        entry["comparisons"] = comparisons(app, entry)
        out["runs"][app] = entry
        st = entry["stability"]
        print(f"== {app}: repeats {entry['repeats']}  stability {'passes' if st['passes'] else 'does not hold'}"
              f"  left out (not throttled) {len(entry['not_throttled'])}")
    json.dump(out, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(out))


if __name__ == "__main__":
    main()
