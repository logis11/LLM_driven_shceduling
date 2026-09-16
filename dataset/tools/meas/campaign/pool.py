#!/usr/bin/env python3
"""Pool a campaign's downloaded artifacts into per-run distributions with
across-repeat spread (9.5 method §6–§7).

pool.py <artifacts-dir> <out.json> [--w-ms 5] [--cap-ms 0]

<artifacts-dir> holds one folder per (app, repeat) named
meas-<family>-<app>-r<k>-<mode> (as uploaded). For each app: every repeat is
analysed (analyze.analyze_run); per phase and per thread comm the gap and run
samples of all repeats are pooled (p50, p90, p99, n) and the per-repeat p50
is listed as the spread; per-input samples likewise for the three rules.
"""

import argparse
import glob
import json
import os
import re
import sys
from array import array

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import analyze_run, pct  # noqa: E402

NAME = re.compile(r"^meas-(interactive|playback)-(.+)-r(\d+)-(dry|full)$")


QUANTILE_PROBS = (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999)
COVERAGE = 0.95  # D16: components in descending wake rate until this share of idle wakes; the rest pooled as one residual


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
            "repeat_p50": [pct(vs, .5) for vs in samples_by_repeat], "repeat_n": [len(vs) for vs in samples_by_repeat]}


def select_components(comms, spans, reps):
    """D16: comms in descending mean wake rate until COVERAGE of the wakes; the remaining comms merged
    into one residual component whose gaps are those of their merged wake times."""
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
    return chosen, residual, {"coverage": COVERAGE, "covered_share": round(cum / total, 4) if total else None,
                              "total_wakes_per_s": round(total, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--w-ms", type=float, default=5.0); ap.add_argument("--cap-ms", type=float, default=0.0)
    ap.add_argument("--exclude-roles", default="", help="comma-separated process roles left out of the tree (D14: renderer for chrome)")
    args = ap.parse_args()
    exclude_roles = tuple(x for x in args.exclude_roles.split(",") if x)
    runs = {}
    for d in sorted(glob.glob(os.path.join(args.artifacts, "meas-*"))):
        m = NAME.match(os.path.basename(d))
        if not m or not os.path.exists(os.path.join(d, "report.json")):
            continue
        fam, app, rep, mode = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        runs.setdefault(app, {"family": fam, "mode": mode, "repeats": {}})["repeats"][rep] = d
    out = {"w_ms": args.w_ms, "cap_ms": args.cap_ms, "exclude_roles": list(exclude_roles), "runs": {}}
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
                    by_tid.setdefault((row.comm, row.tid), []).append((row.t_in, row.run))
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
                 "version": results[reps[0]].get("version"), "phases": {}}
        for phase in ("idle", "driven", "driven-alt", "play", "op"):
            if not all(phase in raws[r]["phases"] for r in reps):
                continue
            ph = {"roles": {r: results[r]["phases"][phase]["roles"] for r in reps},
                  "span_s": [round(raws[r]["phases"][phase]["span"], 1) for r in reps],
                  "cpu_share": [results[r]["phases"][phase]["cpu_share"] for r in reps],
                  "wakes_per_s": [results[r]["phases"][phase]["wakes_per_s"] for r in reps],
                  "threads": {}}
            comms = {}
            for r in reps:
                for comm, cc in raws[r]["phases"][phase]["comms"].items():
                    c = comms.setdefault(comm, {"gaps": {}, "runs": {}, "t_in": {}, "wakes": {}, "threads": {}})
                    c["gaps"][r] = cc["gaps"]; c["runs"][r] = cc["runs"]; c["t_in"][r] = cc["t_in"]
                    c["wakes"][r] = cc["wakes"]; c["threads"][r] = cc["threads"]
            spans = {r: raws[r]["phases"][phase]["span"] for r in reps}
            chosen, residual, cov = select_components(comms, spans, reps)
            ph["components"] = {"selected": chosen, "residual": residual, **cov}
            for comm, c in sorted(comms.items(), key=lambda kv: -sum(sum(v) for v in kv[1]["runs"].values())):
                spans = {r: raws[r]["phases"][phase]["span"] for r in reps}
                ph["threads"][comm] = {
                    "threads": [c["threads"].get(r, 0) for r in reps],
                    "wakes_per_s": [round(c["wakes"].get(r, 0) / spans[r], 2) for r in reps],
                    "cpu_share": [round(sum(c["runs"].get(r, [])) / 1000 / spans[r], 4) for r in reps],
                    "gap_ms": summary([c["gaps"].get(r, []) for r in reps]),
                    "run_ms": summary([c["runs"].get(r, []) for r in reps])}
            if phase == "op" and all(raws[r]["phases"][phase].get("operation") for r in reps):
                ops = {r: raws[r]["phases"][phase]["operation"] for r in reps}
                ph["operation"] = {"name": ops[reps[0]]["name"],
                                   "n_ok": [ops[r]["n_ok"] for r in reps], "n_failed": [ops[r]["n_failed"] for r in reps],
                                   "duration_ms": summary([ops[r]["durations_ms"] for r in reps])}
            if phase in ("driven", "driven-alt") and all(raws[r]["phases"][phase].get("per_input") for r in reps):
                pi = {r: raws[r]["phases"][phase]["per_input"] for r in reps}
                ph["per_input"] = {
                    "events": [len(pi[r]["win_run"]) for r in reps],
                    "first_wake": {"attributed_share": [round(len(pi[r]["first_lat"]) / max(len(pi[r]["win_run"]), 1), 3) for r in reps],
                                   "latency_ms": summary([pi[r]["first_lat"] for r in reps]),
                                   "run_ms": summary([pi[r]["first_run"] for r in reps])},
                    "window": {"len_ms": summary([pi[r]["win_len"] for r in reps]),
                               "run_ms": summary([pi[r]["win_run"] for r in reps]),
                               "run_ms_minus_idle": summary([pi[r]["win_run_corr"] for r in reps])},
                    "waker": {"x_wakes_per_input": summary([pi[r]["xw_count"] for r in reps]),
                              "first_x_wake_latency_ms": summary([pi[r]["xw_lat"] for r in reps]),
                              "run_ms": summary([pi[r]["xw_run"] for r in reps])}}
            entry["phases"][phase] = ph
        out["runs"][app] = entry
        print(f"== {app} ({info['family']}, {info['mode']}, repeats {reps}, {entry['version']})")
        for phase, ph in entry["phases"].items():
            print(f"   {phase}: span {ph['span_s']} cpu {ph['cpu_share']} wakes/s {ph['wakes_per_s']}")
            if "operation" in ph:
                o = ph["operation"]
                print(f"     operation {o['name']}: ok {o['n_ok']} failed {o['n_failed']}; duration p50/p90/p99 {o['duration_ms']['p50']}/{o['duration_ms']['p90']}/{o['duration_ms']['p99']} ms ({o['duration_ms']['repeat_p50']})")
            print(f"     roles r{reps[0]}: {ph['roles'][reps[0]]}")
            for comm, c in list(ph["threads"].items())[:5]:
                print(f"     {comm:16s} thr {c['threads']} wakes/s {c['wakes_per_s']} gap p50 {c['gap_ms']['p50']} ({c['gap_ms']['repeat_p50']}) run p50/p90/p99 {c['run_ms']['p50']}/{c['run_ms']['p90']}/{c['run_ms']['p99']}")
            if "per_input" in ph:
                p = ph["per_input"]
                print(f"     per input: events {p['events']}; first-wake share {p['first_wake']['attributed_share']} run p50 {p['first_wake']['run_ms']['p50']}; window run p50/p90 {p['window']['run_ms']['p50']}/{p['window']['run_ms']['p90']} net {p['window']['run_ms_minus_idle']['p50']}; waker run p50/p90/p99 {p['waker']['run_ms']['p50']}/{p['waker']['run_ms']['p90']}/{p['waker']['run_ms']['p99']} ({p['waker']['run_ms']['repeat_p50']})")
    json.dump(out, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
