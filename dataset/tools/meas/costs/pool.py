#!/usr/bin/env python3
"""Pool the 9.12 costs campaign (research-slice changelog D31; method
_dev/research/jioh/task-9.12-related-work-prose/campaign/method.md).

Finds every repeat under <root> (report.json with family `costs`), keeps the gate-open repeats on the named CPU
model, one per (run id, job, repeat), reads each one's values on the method's list and evaluates the workflow's
stability rule on each by its per-repeat values (stability.stability, at least five repeats). Prints a table and
writes pooled.json beside it when --out is given.

    pool.py <root> --cpu-model "EPYC 7763" [--out <dir>]
"""

import argparse
import glob
import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from stability import TOLERANCE, stability, t975  # noqa: E402

LOADS = ("pingpong", "messaging", "sleep")


def kernel_values(d):
    c = json.load(open(os.path.join(d, "costs.json")))
    v = {k: c.get(k) for k in ("pair_ns_per_round_trip", "self_ns_per_pair", "switch_ns_direct",
                               "perf_pipe_us_per_op", "lat_ctx_us_0k", "lat_ctx_us_16k", "lat_ctx_us_64k")}
    tr = c.get("traces", {})
    for f in ("pick_next_task_fair", "pick_task_fair"):
        for load in LOADS:
            t = tr.get(f"{f}.{load}") or {}
            v[f"{f}.{load}.median_ns"] = t.get("median_ns")
            v[f"{f}.{load}.mean_ns"] = t.get("mean_ns")
            if load == "pingpong":
                v[f"{f}.{load}.tracer_ns_per_call"] = t.get("tracer_ns_per_call")
    t = tr.get("sched_balance_newidle.sleep") or {}
    v["sched_balance_newidle.sleep.mean_ns"] = t.get("mean_ns")
    t = tr.get("__task_pid_nr_ns.getpid") or {}
    v["__task_pid_nr_ns.getpid.median_ns"] = t.get("median_ns")
    v["__task_pid_nr_ns.getpid.tracer_ns_per_call"] = t.get("tracer_ns_per_call")
    idle = c.get("idle_mean", {})
    cpu = str(c.get("measured_cpu", 3))
    cs, sc = idle.get("cs_per_s", {}), idle.get("schedule_per_s", {})
    v["idle.cs_per_s.measured_cpu"] = cs.get(cpu)
    v["idle.cs_per_s.all_cpus"] = sum(cs.values()) if cs else None
    v["idle.schedule_per_s.measured_cpu"] = sc.get(cpu)
    return v


def llm_values(d, report):
    v = {}
    for path in sorted(glob.glob(os.path.join(d, "requests.*.jsonl"))):
        model = os.path.basename(path)[len("requests."):-len(".jsonl")]
        rows = [json.loads(x) for x in open(path) if x.strip()]
        reqs = [r for r in rows if r.get("kind") == "request" and r.get("label") != "warmup"]
        for schema in ("system", "full"):
            rs = [r for r in reqs if r["schema"] == schema and r.get("timings")]
            if not rs:
                continue
            v[f"{model}.{schema}.wall_ms"] = statistics.fmean(r["wall_ms"] for r in rs)
            v[f"{model}.{schema}.prompt_ms"] = statistics.fmean(r["timings"]["prompt_ms"] for r in rs)
            v[f"{model}.{schema}.predicted_ms"] = statistics.fmean(r["timings"]["predicted_ms"] for r in rs)
            v[f"{model}.{schema}.predicted_n"] = statistics.fmean(r["timings"]["predicted_n"] for r in rs)
            v[f"{model}.{schema}.prompt_n"] = statistics.fmean(r["timings"]["prompt_n"] for r in rs)
            v[f"{model}.{schema}.parses"] = sum(1 for r in rs if r.get("parses")) / len(rs)
        load = report.get(f"server.{model}.load_ms")
        v[f"{model}.load_ms"] = float(load) if load else None
        bench = os.path.join(d, f"bench.{model}.json")
        try:
            for b in json.load(open(bench)):
                if b.get("n_prompt") and not b.get("n_gen"):
                    v[f"{model}.bench.pp{b['n_prompt']}_tps"] = b.get("avg_ts")
                elif b.get("n_gen") and not b.get("n_prompt"):
                    v[f"{model}.bench.tg{b['n_gen']}_tps"] = b.get("avg_ts")
        except (OSError, ValueError):
            pass
    return v


def needed(vals):
    """The first repeat count at which the present spread would hold the rule (the pools' projection)."""
    v = [x for x in vals if x]
    if len(v) < 2:
        return None
    m, sd = statistics.fmean(v), statistics.stdev(v)
    if m == 0:
        return None
    for k in range(5, 1000):
        if t975(k) * sd / math.sqrt(k) <= TOLERANCE * abs(m):
            return k
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--cpu-model", default="EPYC 7763")
    ap.add_argument("--out")
    a = ap.parse_args()
    repeats = {"kernel": {}, "llm": {}}
    others = []
    for rep in sorted(glob.glob(os.path.join(a.root, "**", "report.json"), recursive=True)):
        d = os.path.dirname(rep)
        r = json.load(open(rep))
        if r.get("family") != "costs" or r.get("mode") != "full":
            continue
        try:
            run = json.load(open(os.path.join(d, "spec.json")))["github_run"]["GITHUB_RUN_ID"]
        except (OSError, ValueError, KeyError, TypeError):
            run = "?"
        key = f"{r.get('repeat')}@{run}"
        if r.get("gate") != "open" or a.cpu_model not in r.get("machine.model", ""):
            others.append({"job": r.get("job"), "repeat": key, "gate": r.get("gate"), "model": r.get("machine.model")})
            continue
        job = r.get("job")
        if key in repeats[job]:
            continue
        vals = kernel_values(d) if job == "kernel" else llm_values(d, r)
        repeats[job][key] = {"values": vals, "kernel": r.get("kernel"), "model": r.get("machine.model")}
    pooled = {"cpu_model": a.cpu_model, "others": others, "jobs": {}}
    for job, reps in repeats.items():
        names = sorted({n for x in reps.values() for n in x["values"]})
        rows = {}
        for n in names:
            per = {k: x["values"].get(n) for k, x in reps.items()}
            s = stability(per, min_k=5)
            vs = [x for x in per.values() if x]
            s.update({"min": min(vs) if vs else None, "max": max(vs) if vs else None, "needed": needed(per.values()),
                      "per_repeat": per})
            rows[n] = s
        pooled["jobs"][job] = {"repeats": sorted(reps), "kernels": sorted({x["kernel"] for x in reps.values()}),
                               "values": rows}
        print(f"\n== {job}: {len(reps)} repeats on the {a.cpu_model} ({', '.join(sorted(reps))})")
        print(f"{'value':52} {'k':>3} {'mean':>12} {'min':>12} {'max':>12} {'±%':>7} {'need':>5} pass")
        for n, s in rows.items():
            hw = f"{100 * s['half_width']:.2f}" if s.get("half_width") is not None else "-"
            fmt = lambda x: f"{x:.3f}" if isinstance(x, (int, float)) else "-"
            print(f"{n:52} {s['k']:>3} {fmt(s['mean']):>12} {fmt(s['min']):>12} {fmt(s['max']):>12} {hw:>7} "
                  f"{str(s['needed']):>5} {'yes' if s['passes'] else 'no'}")
    print(f"\nnot pooled (gate or model): {len(others)}")
    for o in others:
        print(f"  {o['job']} {o['repeat']} {o['gate']} {o['model']}")
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        json.dump(pooled, open(os.path.join(a.out, "pooled.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
