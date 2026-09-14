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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import analyze_run, pct  # noqa: E402

NAME = re.compile(r"^meas-(interactive|playback)-(.+)-r(\d+)-(dry|full)$")


def summary(samples_by_repeat):
    pooled = [v for vs in samples_by_repeat for v in vs]
    return {"n": len(pooled), "p50": pct(pooled, .5), "p90": pct(pooled, .9), "p99": pct(pooled, .99),
            "repeat_p50": [pct(vs, .5) for vs in samples_by_repeat], "repeat_n": [len(vs) for vs in samples_by_repeat]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--w-ms", type=float, default=5.0); ap.add_argument("--cap-ms", type=float, default=0.0)
    args = ap.parse_args()
    runs = {}
    for d in sorted(glob.glob(os.path.join(args.artifacts, "meas-*"))):
        m = NAME.match(os.path.basename(d))
        if not m or not os.path.exists(os.path.join(d, "report.json")):
            continue
        fam, app, rep, mode = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        runs.setdefault(app, {"family": fam, "mode": mode, "repeats": {}})["repeats"][rep] = d
    out = {"w_ms": args.w_ms, "cap_ms": args.cap_ms, "runs": {}}
    for app, info in runs.items():
        reps = sorted(info["repeats"])
        results, raws = {}, {}
        for r in reps:
            results[r], raws[r] = analyze_run(info["repeats"][r], args.w_ms, args.cap_ms)
        entry = {"family": info["family"], "mode": info["mode"], "repeats": reps,
                 "version": results[reps[0]].get("version"), "phases": {}}
        for phase in ("idle", "driven", "play"):
            if not all(phase in raws[r]["phases"] for r in reps):
                continue
            ph = {"roles": {r: results[r]["phases"][phase]["roles"] for r in reps},
                  "span_s": [round(raws[r]["phases"][phase]["span"], 1) for r in reps],
                  "cpu_share": [results[r]["phases"][phase]["cpu_share"] for r in reps],
                  "wakes_per_s": [results[r]["phases"][phase]["wakes_per_s"] for r in reps],
                  "threads": {}}
            comms = {}
            for r in reps:
                by_tid = {}
                for row in raws[r]["phases"][phase]["rows"]:
                    by_tid.setdefault((row["comm"], row["tid"]), []).append(row)
                for (comm, tid), rows in by_tid.items():
                    rows.sort(key=lambda x: x["t_in"])
                    c = comms.setdefault(comm, {"gaps": {}, "runs": {}, "wakes": {}, "threads": {}})
                    c["gaps"].setdefault(r, []).extend((b["t_in"] - a["t_in"]) * 1000 for a, b in zip(rows, rows[1:]))
                    c["runs"].setdefault(r, []).extend(x["run"] for x in rows)
                    c["wakes"][r] = c["wakes"].get(r, 0) + len(rows)
                    c["threads"][r] = c["threads"].get(r, 0) + 1
            for comm, c in sorted(comms.items(), key=lambda kv: -sum(sum(v) for v in kv[1]["runs"].values())):
                spans = {r: raws[r]["phases"][phase]["span"] for r in reps}
                ph["threads"][comm] = {
                    "threads": [c["threads"].get(r, 0) for r in reps],
                    "wakes_per_s": [round(c["wakes"].get(r, 0) / spans[r], 2) for r in reps],
                    "cpu_share": [round(sum(c["runs"].get(r, [])) / 1000 / spans[r], 4) for r in reps],
                    "gap_ms": summary([c["gaps"].get(r, []) for r in reps]),
                    "run_ms": summary([c["runs"].get(r, []) for r in reps])}
            if phase == "driven" and all("per_input" in raws[r]["phases"][phase] for r in reps):
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
            print(f"     roles r{reps[0]}: {ph['roles'][reps[0]]}")
            for comm, c in list(ph["threads"].items())[:5]:
                print(f"     {comm:16s} thr {c['threads']} wakes/s {c['wakes_per_s']} gap p50 {c['gap_ms']['p50']} ({c['gap_ms']['repeat_p50']}) run p50/p90/p99 {c['run_ms']['p50']}/{c['run_ms']['p90']}/{c['run_ms']['p99']}")
            if "per_input" in ph:
                p = ph["per_input"]
                print(f"     per input: events {p['events']}; first-wake share {p['first_wake']['attributed_share']} run p50 {p['first_wake']['run_ms']['p50']}; window run p50/p90 {p['window']['run_ms']['p50']}/{p['window']['run_ms']['p90']} net {p['window']['run_ms_minus_idle']['p50']}; waker run p50/p90/p99 {p['waker']['run_ms']['p50']}/{p['waker']['run_ms']['p90']}/{p['waker']['run_ms']['p99']} ({p['waker']['run_ms']['repeat_p50']})")
    json.dump(out, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
