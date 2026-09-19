#!/usr/bin/env python3
"""Pool a campaign's downloaded artifacts into per-run distributions with
across-repeat spread (9.5 method §6–§7).

pool.py <artifacts-dir> <out.json> [--w-ms 5] [--cap-ms 0] [--cpu-model TEXT]

<artifacts-dir> holds one folder per (app, repeat) named
meas-<family>-<app>-r<k>-<mode> (as uploaded), at any depth, so the runs of one
campaign can be downloaded side by side into one folder each. A job the machine
gate stopped (report.json gate=wrong-machine) and, with --cpu-model, a repeat
measured on another CPU model are listed, not pooled (changelog D26). For each
app: every repeat is analysed (analyze.analyze_run); per phase and per thread
comm the gap and run samples of all repeats are pooled (p50, p90, p99, n) and
the per-repeat p50 is listed as the spread; per-input samples likewise for the
three rules; every value the fold-in carries, each table by its per-repeat
mean, is checked against the shared stability criterion
(dataset/tools/meas/stability.py; changelog D29, D30).
"""

import argparse
import glob
import json
import os
import re
import statistics
import sys
from array import array

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import analyze_run, pct  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stability import stability, TOLERANCE, T975  # noqa: E402

NAME = re.compile(r"^meas-(interactive|playback)-(.+)-r(\d+)-(dry|full)$")


QUANTILE_PROBS = (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999)
COVERAGE = 0.95  # D16: components in descending wake rate until this share of idle wakes; the rest pooled as one residual
# D26: the headline per application; under D30 the playback CPU share stays on the list beside every carried table
HEADLINE = {"soffice": "input_run", "code": "input_run", "thunderbird": "input_run", "thunderbird-send": "input_run",
            "chrome": "op_duration", "gimp": "op_duration", "kdenlive": "op_duration",
            "mpv-video": "play_cpu_share", "mpv-audio": "play_cpu_share", "webrtc": "play_cpu_share"}
# D26: SWELL-KW's Outlook conditions (c2, c3) hold 4 761 s of recorded time — eight windows, the eighth 561 s
WINDOW_LIMIT = {"thunderbird": 8, "thunderbird-send": 8}   # D31: the re-observation reads the same Outlook windows
ABS_FLOOR_MS = 0.001  # the trace's resolution: perf sched timehist times in whole microseconds (D30; 9.6 D23)
MIN_REPEATS = 5       # kalibera-ismm13 §11 (D29; 9.6 D24)
FOCUS_COMPONENTS = {"gimp", "kdenlive"}  # fold_in.py's pointer-loop archetypes carry the driven phase as focus_components
# D38: a component keyed by the thread's name with a trailing " #<n>" removed — Gecko names a pool's threads
# "<pool> #<n>", n counting up per spawn (nsThreadPoolNaming::GetNextThreadName), so each pool is one component
POOL_SUFFIX_APPS = {"thunderbird-send"}
POOL_SUFFIX = re.compile(r" #\d+$")


def component_key(app, comm):
    return POOL_SUFFIX.sub("", comm) if app in POOL_SUFFIX_APPS else comm


def repeats_needed(values, abs_floor=None):
    """The smallest repeat count, at least MIN_REPEATS, at which the 95 % half-width at the spread of the given
    repeats is within the tolerance (stability()'s t multipliers); None past 200."""
    v = [x for x in values if x is not None]
    if len(v) < 2:
        return None
    m, sd = statistics.fmean(v), statistics.stdev(v)
    bound = max(TOLERANCE * m, abs_floor or 0.0)
    for k in range(MIN_REPEATS, 201):
        if T975.get(k, T975[20]) * sd / k ** 0.5 <= bound:
            return k
    return None


def criterion(app, entry):
    """D30: every value the fold-in carries against the shared rule, each carried table by its per-repeat mean
    (georges-oopsla07 §4.2, kalibera-ismm13 §9.3) — tolerance the larger of 5 % of the mean and 1 µs for times, 5 % for
    rates and shares, at least five repeats (D29). Per carried component (the idle or play phase; the driven phase of
    the pointer-loop runs; the operation's), its wake rate, gap mean and run mean; the input-run mean under SWELL-KW and
    under the 136M check; the operation duration mean; the play-phase CPU share (D26's headline for playback)."""
    ph, crit = entry["phases"], {}

    def add(name, values, floor):
        crit[name] = {**stability(values, floor, MIN_REPEATS, keep_zero=True), "needed": repeats_needed(values, floor)}

    name, values = headline(app, entry)
    if name == "play CPU share":
        add("play CPU share", values, None)
    carried = ["idle" if "idle" in ph else "play"] + (["driven"] if app in FOCUS_COMPONENTS else []) \
        + (["op"] if ph.get("op", {}).get("operation") else [])
    for p in carried:
        if p not in ph:
            continue
        sel = ph[p]["components"]
        comps = [(c, ph[p]["threads"][c]) for c in sel["selected"] if ph[p]["threads"][c]["gap_ms"]["q"] is not None]
        if sel["residual"] and sel["residual"]["gap_ms"]["q"]:
            comps.append(("residual", sel["residual"]))
        for comm, c in comps:
            add(f"{p} {comm} wakes/s", c["wakes_per_s"], None)
            add(f"{p} {comm} gap mean (ms)", c["gap_ms"]["repeat_mean"], ABS_FLOOR_MS)
            add(f"{p} {comm} run mean (ms)", c["run_ms"]["repeat_mean"], ABS_FLOOR_MS)
    for p, label in (("driven", "SWELL-KW"), ("driven-alt", "136M")):
        if "per_input" in ph.get(p, {}):
            add(f"input_run mean, {label} (ms)", ph[p]["per_input"]["window"]["run_ms_minus_idle"]["repeat_mean"], ABS_FLOOR_MS)
    if ph.get("op", {}).get("operation"):
        add("operation duration mean (ms)", ph["op"]["operation"]["duration_ms"]["repeat_mean"], ABS_FLOOR_MS)
    return crit


def headline(app, entry):
    kind = HEADLINE.get(app)
    ph = entry["phases"]
    if kind == "input_run" and "per_input" in ph.get("driven", {}):
        return "input_run p50 (ms)", ph["driven"]["per_input"]["window"]["run_ms_minus_idle"]["repeat_p50"]
    if kind == "op_duration" and "operation" in ph.get("op", {}):
        return "operation duration p50 (ms)", ph["op"]["operation"]["duration_ms"]["repeat_p50"]
    if kind == "play_cpu_share" and "play" in ph:
        return "play CPU share", ph["play"]["cpu_share"]
    return None, None


def qtable(values):
    """The D17 quantile table (ms, 3 decimals) of a pooled sample."""
    if not values:
        return None
    v = sorted(values)
    return [pct(v, q) for q in QUANTILE_PROBS]


def summary(samples_by_repeat):
    pooled = [v for vs in samples_by_repeat for v in vs]
    return {"n": len(pooled), "p50": pct(pooled, .5), "p90": pct(pooled, .9), "p99": pct(pooled, .99),
            "q": qtable(pooled),
            "repeat_p50": [pct(vs, .5) for vs in samples_by_repeat], "repeat_n": [len(vs) for vs in samples_by_repeat],
            "repeat_mean": [round(statistics.fmean(vs), 4) if vs else None for vs in samples_by_repeat]}


def select_components(comms, spans, reps):
    """D16: comms in descending mean wake rate until COVERAGE of the wakes; the remaining comms merged
    into one residual component whose gaps are those of their merged wake times. D43: a component, the residual
    included, whose gap and run means are missing in any repeat is listed under `sporadic`, not carried."""
    rate = {c: sum(cc["wakes"].get(r, 0) / spans[r] for r in reps) / len(reps) for c, cc in comms.items()}
    total = sum(rate.values())
    order = sorted(comms, key=lambda c: -rate[c])
    chosen, cum = [], 0.0
    for c in order:
        if total and cum / total >= COVERAGE:
            break
        chosen.append(c); cum += rate[c]
    rest = [c for c in order if c not in chosen]
    residual = None
    if rest:
        gaps_by_rep, runs_by_rep, wakes_by_rep, threads_by_rep = [], [], [], []
        for r in reps:
            times = sorted(t for c in rest for t in comms[c]["t_in"].get(r, []))
            gaps_by_rep.append([(b - a) * 1000 for a, b in zip(times, times[1:])])
            runs_by_rep.append([x for c in rest for x in comms[c]["runs"].get(r, [])])
            wakes_by_rep.append(len(times)); threads_by_rep.append(sum(comms[c]["threads"].get(r, 0) for c in rest))
        residual = {"comms": rest, "threads": threads_by_rep,
                    "wakes_per_s": [round(wakes_by_rep[i] / spans[r], 3) for i, r in enumerate(reps)],
                    "cpu_share": [round(sum(runs_by_rep[i]) / 1000 / spans[r], 5) for i, r in enumerate(reps)],
                    "gap_ms": summary(gaps_by_rep), "run_ms": summary(runs_by_rep)}
    # D43: a component — the residual as a whole included — is carried only if its gap and run means exist in every
    # repeat (it wakes at least twice in each repeat's phase): the rule tests each value by its per-repeat mean
    # (kalibera-ismm13 §9.3), and D16's components are periodic; the rest is reported as sporadic, not carried
    sporadic = []
    for c in [c for c in chosen if not all(len(comms[c]["gaps"].get(r, [])) for r in reps)]:
        chosen.remove(c)
        sporadic.append({"comm": c, "repeats": [r for r in reps if comms[c]["wakes"].get(r, 0)], "wakes_per_s": round(rate[c], 4)})
    if residual and not all(residual["gap_ms"]["repeat_n"]):
        sporadic.append({"comm": "residual", "comms": rest, "repeats": [r for r, w in zip(reps, residual["wakes_per_s"]) if w],
                         "wakes_per_s": round(sum(rate[c] for c in rest), 4)})
        residual = None
    cum = sum(rate[c] for c in chosen)
    return chosen, residual, {"coverage": COVERAGE, "covered_share": round(cum / total, 4) if total else None,
                              "total_wakes_per_s": round(total, 3), "sporadic": sporadic}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--w-ms", type=float, default=5.0); ap.add_argument("--cap-ms", type=float, default=0.0)
    ap.add_argument("--exclude-roles", default="", help="comma-separated process roles left out of the tree (D14: renderer for chrome)")
    ap.add_argument("--cpu-model", default="", help="pool only repeats whose CPU model contains this text (D26)")
    args = ap.parse_args()
    exclude_roles = tuple(x for x in args.exclude_roles.split(",") if x)
    runs, gated, other = {}, [], []
    for d in sorted(glob.glob(os.path.join(args.artifacts, "**", "meas-*"), recursive=True)):
        m = NAME.match(os.path.basename(d))
        if not m or not os.path.exists(os.path.join(d, "report.json")):
            continue
        fam, app, rep, mode = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        spec = json.load(open(os.path.join(d, "spec.json"))) if os.path.exists(os.path.join(d, "spec.json")) else {}
        model = spec.get("cpu_model") or ""
        if json.load(open(os.path.join(d, "report.json"))).get("gate") == "wrong-machine":
            gated.append({"app": app, "repeat": rep, "cpu_model": model, "path": os.path.relpath(d, args.artifacts)})
            continue
        if args.cpu_model and args.cpu_model not in model:
            other.append({"app": app, "repeat": rep, "cpu_model": model, "path": os.path.relpath(d, args.artifacts)})
            continue
        info = runs.setdefault(app, {"family": fam, "mode": mode, "repeats": {}, "cpu_model": {}, "kernel": {}, "run_id": {}})
        if rep in info["repeats"]:
            raise SystemExit(f"{app} repeat {rep}: two measured artifacts ({info['repeats'][rep]}, {d})")
        info["repeats"][rep] = d
        info["cpu_model"][rep] = model
        info["run_id"][rep] = (spec.get("github_run") or {}).get("GITHUB_RUN_ID")  # D27: a campaign spans runs
        info["kernel"][rep] = (spec.get("uname") or "").split()[2] if len((spec.get("uname") or "").split()) > 2 else None
    out = {"w_ms": args.w_ms, "cap_ms": args.cap_ms, "exclude_roles": list(exclude_roles), "machine": args.cpu_model or None,
           "gated_out": gated, "other_machine": other, "runs": {}}
    for app, info in runs.items():
        reps = sorted(info["repeats"])
        results, raws = {}, {}
        for r in reps:
            results[r], raw = analyze_run(info["repeats"][r], args.w_ms, args.cap_ms, exclude_roles=exclude_roles)
            # keep only compact samples per phase: per-comm gaps/runs/wakes/threads, span, per-input lists
            slim = {"phases": {}}
            for phase, pd in raw["phases"].items():
                comms = {}
                by_tid = {}
                # the op phase pools the operation's components, i.e. the rows inside the [trigger, done) windows,
                # over the summed window span; its duration samples travel beside them (spec decisions 8–9)
                op = pd.get("operation")
                phase_rows = op["inside"] if op else pd["rows"]
                phase_span = (sum(op["durations_ms"]) / 1000 or 1e-6) if op else pd["span"]
                for row in phase_rows:
                    by_tid.setdefault((component_key(app, row.comm), row.tid), []).append((row.t_in, row.run))
                for (comm, tid), rs in by_tid.items():
                    c = comms.setdefault(comm, {"gaps": array("d"), "runs": array("d"), "t_in": array("d"), "wakes": 0, "threads": 0})
                    c["gaps"].extend((b[0] - a[0]) * 1000 for a, b in zip(rs, rs[1:]))
                    c["runs"].extend(x[1] for x in rs)
                    c["t_in"].extend(x[0] for x in rs)
                    c["wakes"] += len(rs); c["threads"] += 1
                slim["phases"][phase] = {"span": phase_span, "comms": comms, "per_input": pd.get("per_input"),
                                         "operation": {"name": op["name"], "durations_ms": op["durations_ms"],
                                                       "n_ok": op["n_ok"], "n_failed": op["n_failed"]} if op else None}
            raws[r] = slim
            del raw
        entry = {"family": info["family"], "mode": info["mode"], "repeats": reps,
                 "cpu_model": {r: info["cpu_model"][r] for r in reps}, "kernel": {r: info["kernel"][r] for r in reps},
                 "run_id": {r: info["run_id"][r] for r in reps},
                 "version": results[reps[0]].get("version"), "phases": {}}
        for phase in ("idle", "driven", "driven-alt", "play", "op"):
            # D32: each phase over the repeats that have it — a repeat past the recording's end runs the idle phase alone
            preps = [r for r in reps if phase in raws[r]["phases"]]
            if not preps:
                continue
            ph = {"roles": {r: results[r]["phases"][phase]["roles"] for r in preps},
                  "span_s": [round(raws[r]["phases"][phase]["span"], 1) for r in preps],
                  "cpu_share": [results[r]["phases"][phase]["cpu_share"] for r in preps],
                  "wakes_per_s": [results[r]["phases"][phase]["wakes_per_s"] for r in preps],
                  "threads": {}}
            comms = {}
            for r in preps:
                for comm, cc in raws[r]["phases"][phase]["comms"].items():
                    c = comms.setdefault(comm, {"gaps": {}, "runs": {}, "t_in": {}, "wakes": {}, "threads": {}})
                    c["gaps"][r] = cc["gaps"]; c["runs"][r] = cc["runs"]; c["t_in"][r] = cc["t_in"]
                    c["wakes"][r] = cc["wakes"]; c["threads"][r] = cc["threads"]
            spans = {r: raws[r]["phases"][phase]["span"] for r in preps}
            chosen, residual, cov = select_components(comms, spans, preps)
            ph["components"] = {"selected": chosen, "residual": residual, **cov}
            for comm, c in sorted(comms.items(), key=lambda kv: -sum(sum(v) for v in kv[1]["runs"].values())):
                spans = {r: raws[r]["phases"][phase]["span"] for r in preps}
                ph["threads"][comm] = {
                    "threads": [c["threads"].get(r, 0) for r in preps],
                    "wakes_per_s": [round(c["wakes"].get(r, 0) / spans[r], 2) for r in preps],
                    "cpu_share": [round(sum(c["runs"].get(r, [])) / 1000 / spans[r], 4) for r in preps],
                    "gap_ms": summary([c["gaps"].get(r, []) for r in preps]),
                    "run_ms": summary([c["runs"].get(r, []) for r in preps])}
            if phase == "op" and all(raws[r]["phases"][phase].get("operation") for r in preps):
                ops = {r: raws[r]["phases"][phase]["operation"] for r in preps}
                ph["operation"] = {"name": ops[preps[0]]["name"],
                                   "n_ok": [ops[r]["n_ok"] for r in preps], "n_failed": [ops[r]["n_failed"] for r in preps],
                                   "duration_ms": summary([ops[r]["durations_ms"] for r in preps])}
            if phase in ("driven", "driven-alt") and all(raws[r]["phases"][phase].get("per_input") for r in preps):
                pi = {r: raws[r]["phases"][phase]["per_input"] for r in preps}
                ph["per_input"] = {
                    "events": [len(pi[r]["win_run"]) for r in preps],
                    "first_wake": {"attributed_share": [round(len(pi[r]["first_lat"]) / max(len(pi[r]["win_run"]), 1), 3) for r in preps],
                                   "latency_ms": summary([pi[r]["first_lat"] for r in preps]),
                                   "run_ms": summary([pi[r]["first_run"] for r in preps])},
                    "window": {"len_ms": summary([pi[r]["win_len"] for r in preps]),
                               "run_ms": summary([pi[r]["win_run"] for r in preps]),
                               "run_ms_minus_idle": summary([pi[r]["win_run_corr"] for r in preps])},
                    "waker": {"x_wakes_per_input": summary([pi[r]["xw_count"] for r in preps]),
                              "first_x_wake_latency_ms": summary([pi[r]["xw_lat"] for r in preps]),
                              "run_ms": summary([pi[r]["xw_run"] for r in preps])}}
            checks = {r: results[r]["phases"][phase].get("wake_check") for r in preps}
            if any(checks.values()):   # D39: the wakeup row against the switch-out state, repeats that record it
                ph["wake_check"] = {r: v for r, v in checks.items() if v}
            if preps != reps:
                ph["repeats"] = preps   # the phase's lists run over these repeats, not the entry's
            entry["phases"][phase] = ph
        crit = criterion(app, entry)
        needed = [c["needed"] for c in crit.values()]
        entry["stability"] = {"tolerance": TOLERANCE, "abs_floor_ms": ABS_FLOOR_MS, "min_repeats": MIN_REPEATS,
                              "window_limit": WINDOW_LIMIT.get(app), "quantities": crit,
                              "passes": bool(crit) and all(c["passes"] for c in crit.values()),
                              "needed": None if not needed or None in needed else max(needed)}
        out["runs"][app] = entry
        print(f"== {app} ({info['family']}, {info['mode']}, repeats {reps}, {entry['version']}; CPU {sorted(set(entry['cpu_model'].values()))})")
        st = entry["stability"]
        fails = [q for q, c in crit.items() if not c["passes"]]
        print(f"   stability: {len(crit)} quantities over {len(reps)} repeats, {len(fails)} out of tolerance; repeats needed at "
              f"this spread {st['needed'] or 'over 200'} — {'holds' if st['passes'] else 'does not hold yet'}")
        for q in fails:
            c = crit[q]
            hw = "—" if c["half_width"] is None else f"±{c['half_width']:.1%}"
            print(f"     {q}: mean {c['mean']}, half-width {hw}, needed {c['needed']}")
        for phase, ph in entry["phases"].items():
            preps = ph.get("repeats", reps)
            print(f"   {phase}{f' (repeats {preps})' if preps != reps else ''}: span {ph['span_s']} cpu {ph['cpu_share']} wakes/s {ph['wakes_per_s']}")
            if "wake_check" in ph:
                tot = {k: sum(c[k] for v in ph["wake_check"].values() for c in v.values())
                       for k in ("gaps", "slept_without_row", "preempted_with_row")}
                print(f"     wake check (repeats {sorted(ph['wake_check'])}): {tot['gaps']} gaps with a state; row disagrees: "
                      f"{tot['slept_without_row']} slept without a row, {tot['preempted_with_row']} preempted with a row")
            if "operation" in ph:
                o = ph["operation"]
                print(f"     operation {o['name']}: ok {o['n_ok']} failed {o['n_failed']}; duration p50/p90/p99 {o['duration_ms']['p50']}/{o['duration_ms']['p90']}/{o['duration_ms']['p99']} ms ({o['duration_ms']['repeat_p50']})")
            print(f"     roles r{preps[0]}: {ph['roles'][preps[0]]}")
            for sp in ph["components"].get("sporadic", []):
                print(f"     sporadic, not carried (D43): {sp['comm']}{' ' + str(sp['comms']) if 'comms' in sp else ''}, "
                      f"wakes in repeats {sp['repeats']}, {sp['wakes_per_s']} wakes/s")
            for comm, c in list(ph["threads"].items())[:5]:
                print(f"     {comm:16s} thr {c['threads']} wakes/s {c['wakes_per_s']} gap p50 {c['gap_ms']['p50']} ({c['gap_ms']['repeat_p50']}) run p50/p90/p99 {c['run_ms']['p50']}/{c['run_ms']['p90']}/{c['run_ms']['p99']}")
            if "per_input" in ph:
                p = ph["per_input"]
                print(f"     per input: events {p['events']}; first-wake share {p['first_wake']['attributed_share']} run p50 {p['first_wake']['run_ms']['p50']}; window run p50/p90 {p['window']['run_ms']['p50']}/{p['window']['run_ms']['p90']} net {p['window']['run_ms_minus_idle']['p50']}; waker run p50/p90/p99 {p['waker']['run_ms']['p50']}/{p['waker']['run_ms']['p90']}/{p['waker']['run_ms']['p99']} ({p['waker']['run_ms']['repeat_p50']})")
    for g in gated:
        print(f"   gated out: {g['app']} r{g['repeat']} ({g['cpu_model']}) {g['path']}")
    for o in other:
        print(f"   other machine, not pooled: {o['app']} r{o['repeat']} ({o['cpu_model']}) {o['path']}")
    json.dump(out, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
