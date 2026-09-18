#!/usr/bin/env python3
"""Pool the 9.6 build campaign's repeats into the per-role tables the archetypes
take (method §5; changelog D8) and render them as results.md.

pool.py <artifacts-dir> <out.json> [--md results.md]

<artifacts-dir> holds one folder per repeat named meas-build-r<k>-<mode>. Every
repeat is analysed (analyze.analyze_phase with samples); per phase and per role
the samples of all repeats are pooled into the D17 quantile table (µs; block-I/O
delay in ns) with the per-repeat p50 as the spread; job counts, concurrency,
dispatch, the batch programs' saturation table, the -j1 against -j8 per-role
CPU ratio (D4) and the DKMS chain shapes (D6) are listed per repeat.
"""

import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import analyze_phase, load_edges, pct, QUANTILE_PROBS  # noqa: E402

NAME = re.compile(r"^meas-build-r(\d+)-(dry|full)$")
BUILD_PHASES = ("build-j8-warm", "build-j8-cold", "build-j1-warm", "dkms")
BATCH_PHASES = ("clamscan", "ffmpeg", "handbrake", "train", "tracker")
ROLE_SAMPLES = (("run_ms", 1000.0, "run_per_wake_us"), ("off_D_ms", 1000.0, "off_after_D_us"), ("off_S_ms", 1000.0, "off_after_S_us"),
                ("off_R_ms", 1000.0, "off_after_R_us"), ("cpu_us", 1.0, "cpu_per_process_us"), ("blkio_ns", 1.0, "blkio_per_process_ns"),
                ("etime_us", 1.0, "etime_per_process_us"), ("wakes_by_pid", 1.0, "wakes_per_process"))


def qtable(values):
    if not values:
        return None
    v = sorted(values)
    return [round(pct(v, q), 1) for q in QUANTILE_PROBS]


def pooled(samples_by_repeat, scale=1.0):
    vals = {r: [x * scale for x in vs] for r, vs in samples_by_repeat.items()}
    allv = [x for vs in vals.values() for x in vs]
    return {"n": len(allv), "q": qtable(allv), "p50": round(pct(sorted(allv), .5), 1) if allv else None,
            "repeat_p50": {r: (round(pct(sorted(vs), .5), 1) if vs else None) for r, vs in sorted(vals.items())},
            "repeat_n": {r: len(vs) for r, vs in sorted(vals.items())}}


# ---- same-machine repeats and the stability criterion (changelog D10; method §8, 2026-09-18) ----------------
T975 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262}
TOLERANCE, REPEAT_CAP = 0.05, 8
CRITERION_ROLES = ("cc1", "as", "gcc", "sh", "fixdep", "rm")   # the object job's roles; plus the dispatch median


def stability(values_by_repeat):
    """The 95 % confidence half-width of the across-repeat mean of one carried median, relative to the mean
    (t multiplier, k − 1 degrees of freedom), and the largest shift of the mean when any one repeat is dropped."""
    import statistics
    v = [x for x in values_by_repeat.values() if x]
    k = len(v)
    if k < 2:
        return {"k": k, "mean": v[0] if v else None, "cv": None, "half_width": None, "leave_one_out": None, "passes": False}
    m, sd = statistics.fmean(v), statistics.stdev(v)
    hw = T975.get(k, 2.2) * sd / (k ** 0.5) / m
    loo = max(abs(statistics.fmean(v[:i] + v[i + 1:]) - m) / m for i in range(k))
    return {"k": k, "mean": round(m, 1), "cv": round(sd / m, 4), "half_width": round(hw, 4), "leave_one_out": round(loo, 4),
            "passes": hw <= TOLERANCE}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts"); ap.add_argument("out"); ap.add_argument("--md")
    ap.add_argument("--cpu-model", default="", help="pool only repeats whose CPU model contains this text (D10); others are the cross-machine check")
    args = ap.parse_args()
    runs, gated = {}, {}
    for d in sorted(glob.glob(os.path.join(args.artifacts, "meas-build-*"))):
        m = NAME.match(os.path.basename(d))
        if m and os.path.exists(os.path.join(d, "report.json")):
            rpt = json.load(open(os.path.join(d, "report.json")))
            if rpt.get("gate") == "wrong-machine":   # stopped by the machine gate before any measurement
                gated[int(m.group(1))] = rpt.get("machine.model")
                continue
            runs[int(m.group(1))] = (d, m.group(2))
    if not runs:
        print("no repeats found", file=sys.stderr); return 1
    reps = sorted(runs)
    per = {}       # repeat -> phase -> analysis
    for r in reps:
        d, mode = runs[r]
        report = json.load(open(os.path.join(d, "report.json")))
        meas_cpu = int(report.get("pin.load_cpu", 3))
        edges = load_edges(d)
        per[r] = {"mode": mode, "cpu_model": (json.load(open(os.path.join(d, "spec.json"))).get("cpu_model") if os.path.exists(os.path.join(d, "spec.json")) else None),
                  "phases": {ph: analyze_phase(d, ph, meas_cpu, edges) for ph in BUILD_PHASES + BATCH_PHASES}}
    all_reps = reps
    other = [r for r in all_reps if args.cpu_model and args.cpu_model not in (per[r]["cpu_model"] or "")]
    reps = [r for r in all_reps if r not in other]
    out = {"repeats": reps, "machine": args.cpu_model or None, "other_machine_repeats": other, "gated_out": gated,
           "mode": {r: per[r]["mode"] for r in all_reps}, "cpu_model": {r: per[r]["cpu_model"] for r in all_reps}, "phases": {}}
    for ph in BUILD_PHASES + BATCH_PHASES:
        have = [r for r in reps if "missing" not in per[r]["phases"][ph]]
        if not have:
            out["phases"][ph] = {"missing": True}; continue
        P = {"repeats": have, "cmd_wall_s": {r: per[r]["phases"][ph]["cmd_wall_s"] for r in have},
             "tree_processes": {r: per[r]["phases"][ph]["tree_processes"] for r in have},
             "wakes_in_tree": {r: per[r]["phases"][ph]["wakes_in_tree"] for r in have},
             "resumes_merged": {r: per[r]["phases"][ph]["resumes_merged"] for r in have},
             "taskstats_enobufs": {r: per[r]["phases"][ph]["taskstats_trailer"].get("enobufs") for r in have},
             "roles": {}}
        roles = sorted({n for r in have for n in per[r]["phases"][ph]["_samples"]["roles"]},
                       key=lambda n: -sum(sum(per[r]["phases"][ph]["_samples"]["roles"].get(n, {}).get("cpu_us", [])) for r in have))
        for n in roles:
            R = {"processes": {r: per[r]["phases"][ph]["roles"].get(n, {}).get("processes", 0) for r in have},
                 "perf_over_taskstats_cpu_p50": {r: per[r]["phases"][ph]["roles"].get(n, {}).get("perf_over_taskstats_cpu", {}).get("p50") for r in have},
                 "blkio_invalid_threads": {r: per[r]["phases"][ph]["roles"].get(n, {}).get("blkio_invalid_threads", 0) for r in have}}
            for key, scale, name in ROLE_SAMPLES:
                R[name] = pooled({r: per[r]["phases"][ph]["_samples"]["roles"].get(n, {}).get(key, []) for r in have}, scale)
            P["roles"][n] = R
        if ph in ("build-j8-warm", "build-j8-cold", "build-j1-warm", "dkms"):
            P["jobs"] = {r: {k: v for k, v in per[r]["phases"][ph]["jobs"].items() if k != "shapes"} for r in have}
            P["job_shapes"] = {r: per[r]["phases"][ph]["jobs"]["shapes"] for r in have}
            P["dispatch"] = {"per_dispatch_us": pooled({r: per[r]["phases"][ph]["dispatch"]["_samples"]["per_dispatch_ms"] for r in have}, 1000.0),
                             "cpu_per_fork_us_by_make": pooled({r: per[r]["phases"][ph]["dispatch"]["_samples"]["cpu_per_fork_ms_by_make"] for r in have}, 1000.0),
                             "forks": {r: per[r]["phases"][ph]["dispatch"]["forks"] for r in have},
                             "makes": {r: per[r]["phases"][ph]["dispatch"]["makes"] for r in have}}
        else:
            P["batch"] = {r: per[r]["phases"][ph]["batch"] for r in have}
        out["phases"][ph] = P
    # D4 invariance check: per role, cpu-per-process pooled median at -j1 over -j8 warm, per repeat and pooled
    chk = {}
    w, o = out["phases"].get("build-j8-warm", {}), out["phases"].get("build-j1-warm", {})
    for n in ("cc1", "as", "gcc", "sh", "fixdep", "rm", "make", "ld", "cc1 (probe)", "sh (probe)"):
        a, b = w.get("roles", {}).get(n), o.get("roles", {}).get(n)
        if a and b and a["cpu_per_process_us"]["p50"] and b["cpu_per_process_us"]["p50"]:
            chk[n] = {"j1_over_j8_pooled_p50": round(b["cpu_per_process_us"]["p50"] / a["cpu_per_process_us"]["p50"], 3),
                      "per_repeat": {r: (round(b["cpu_per_process_us"]["repeat_p50"][r] / a["cpu_per_process_us"]["repeat_p50"][r], 3)
                                        if a["cpu_per_process_us"]["repeat_p50"].get(r) and b["cpu_per_process_us"]["repeat_p50"].get(r) else None)
                                     for r in reps}}
    out["j1_check"] = chk
    # the stability criterion on the warm -j8 phase's carried medians, and the other machine's repeats as a ratio
    crit, cross = {}, {}
    w = out["phases"].get("build-j8-warm", {})
    for n in CRITERION_ROLES:
        if n in w.get("roles", {}):
            crit[n + " CPU per process"] = stability(w["roles"][n]["cpu_per_process_us"]["repeat_p50"])
    if "dispatch" in w:
        crit["make dispatch"] = stability(w["dispatch"]["per_dispatch_us"]["repeat_p50"])
    for r in other:
        a = per[r]["phases"].get("build-j8-warm", {})
        if "missing" in a:
            continue
        row = {}
        for n in CRITERION_ROLES:
            p50 = a["roles"].get(n, {}).get("cpu_per_process_us", {}).get("p50")
            ref = crit.get(n + " CPU per process", {}).get("mean")
            if p50 and ref:
                row[n] = round(p50 / ref, 3)
        ref = crit.get("make dispatch", {}).get("mean")
        if ref and a.get("dispatch", {}).get("per_dispatch_ms", {}).get("p50"):
            row["make dispatch"] = round(a["dispatch"]["per_dispatch_ms"]["p50"] * 1000.0 / ref, 3)
        row["build wall s"] = a.get("cmd_wall_s")
        cross[r] = {"cpu_model": per[r]["cpu_model"], "ratio_to_same_machine_mean": row}
    out["stability"] = {"tolerance": TOLERANCE, "repeat_cap": REPEAT_CAP, "quantities": crit,
                        "passes": bool(crit) and all(c["passes"] for c in crit.values())}
    out["cross_machine"] = cross
    json.dump(out, open(args.out, "w"), indent=1)
    if args.md:
        open(args.md, "w").write(render(out))
    print(f"pooled {len(reps)} repeat(s) -> {args.out}")
    return 0


def fmt_q(q):
    return " / ".join("–" if x is None else (f"{x:.0f}" if x >= 100 else f"{x:.1f}") for x in q) if q else "–"


def render(out):
    reps = out["repeats"]
    L = [f"# 9.6 build campaign — pooled results", "",
         f"Repeats {reps}; mode {out['mode']}; CPU model per repeat {out['cpu_model']}. Quantile tables are p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 / p99.9; "
         f"times in µs unless stated; the spread is the per-repeat p50. Rules: method §5.", ""]
    for ph, P in out["phases"].items():
        if P.get("missing"):
            L += [f"## {ph}", "", "missing", ""]; continue
        L += [f"## {ph}", "", f"command wall s {P['cmd_wall_s']}; tree processes {P['tree_processes']}; wakes {P['wakes_in_tree']}; resumes merged {P['resumes_merged']}; ENOBUFS {P['taskstats_enobufs']}", ""]
        if "jobs" in P:
            for r, j in P["jobs"].items():
                L.append(f"- repeat {r}: jobs {j['count']} {j['kinds']} (compile {j['compile_jobs']}; cc1 {j['cc1_processes']}), makes {j['makes']}; live jobs max {j['concurrency']['max']} mean {j['concurrency']['mean_busy']}; "
                         f"live compile jobs max {j['compile_concurrency']['max']} mean {j['compile_concurrency']['mean_busy']}; live cc1 max {j['cc1_concurrency']['max']} mean {j['cc1_concurrency']['mean_busy']}; "
                         f"members/job p50 {j['members_per_job'].get('p50')}; compile-job lifetime p50 {j['compile_job_lifetime_ms'].get('p50')} ms")
            d = P["dispatch"]
            L += ["", f"dispatch (make's run between consecutive forks, µs): {fmt_q(d['per_dispatch_us']['q'])} (n {d['per_dispatch_us']['n']}; spread {d['per_dispatch_us']['repeat_p50']}); "
                  f"cross-check CPU per fork by make: p50 {d['cpu_per_fork_us_by_make']['p50']} (spread {d['cpu_per_fork_us_by_make']['repeat_p50']}); forks {d['forks']}", ""]
            L += ["job shapes (roles per job, top 8 of repeat " + str(reps[0]) + "):", ""]
            for shape, n in list(P["job_shapes"][reps[0]].items())[:8]:
                L.append(f"- {n} × `{shape}`")
            L.append("")
        L += ["| role | procs | wakes/proc p50 | run per wake | off after D (disk) | off after S (sleep) | CPU per process | blkio per process (ns) | perf/ts p50 |", "|---|---|---|---|---|---|---|---|---|"]
        for n, R in list(P["roles"].items())[:14]:
            L.append(f"| `{n}` | {sum(R['processes'].values())} | {R['wakes_per_process']['p50']} | {fmt_q(R['run_per_wake_us']['q'])} | {fmt_q(R['off_after_D_us']['q'])} (n {R['off_after_D_us']['n']}) | "
                     f"{fmt_q(R['off_after_S_us']['q'])} (n {R['off_after_S_us']['n']}) | {fmt_q(R['cpu_per_process_us']['q'])} | {fmt_q(R['blkio_per_process_ns']['q'])} | {R['perf_over_taskstats_cpu_p50']} |")
        L.append("")
        if "batch" in P:
            L += ["| repeat | program | procs | threads | lifetime s | saturation (taskstats / perf) | dominant thread | top-5 thread shares | blkio s (share) | off after S s | off after D s | invalid blkio threads |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
            for r, b in P["batch"].items():
                L.append(f"| {r} | `{b['program']}` | {b['processes']} | {b['threads_with_runs']} | {b['lifetime_s']} | {b['saturation']} / {b['saturation_perf']} | {b['dominant_thread_share']} | {b['thread_cpu_share_top5']} | "
                         f"{b['blkio_delay_s']} ({b['blkio_share_of_lifetime']}) | {b['off_cpu_after_S_s']} | {b['off_cpu_after_D_s']} | {b['blkio_invalid_threads']} |")
            L.append("")
    st = out.get("stability")
    if st:
        L += ["## Same-machine repeats and the stability criterion (D10)", "",
              f"Pooled machine: {out.get('machine') or 'any'}; pooled repeats {reps}; other-machine repeats {out.get('other_machine_repeats')}; stopped by the machine gate {out.get('gated_out')}. "
              f"Criterion: the 95 % confidence half-width of the across-repeat mean of each carried median is at most {st['tolerance']:.0%} (cap {st['repeat_cap']} repeats). "
              f"**{'Holds' if st['passes'] else 'Does not hold yet'}.**", "",
              "| quantity | repeats | mean (µs) | spread (cv) | 95 % half-width | leave-one-out | passes |", "|---|---|---|---|---|---|---|"]
        for q, c in st["quantities"].items():
            L.append(f"| {q} | {c['k']} | {c['mean']} | {c['cv']:.1%} | ±{c['half_width']:.1%} | {c['leave_one_out']:.1%} | {'yes' if c['passes'] else 'no'} |")
        L.append("")
        for r, x in out.get("cross_machine", {}).items():
            L.append(f"- cross-machine check, repeat {r} ({x['cpu_model']}): ratio to the same-machine mean {x['ratio_to_same_machine_mean']} — written into scope as a ratio, applied to no value (9.5 follow-ups decision 13)")
        L.append("")
    L += ["## -j1 against -j8 (D4 invariance check): CPU per process, pooled p50 ratio", ""]
    for n, c in out["j1_check"].items():
        L.append(f"- `{n}`: {c['j1_over_j8_pooled_p50']} (per repeat {c['per_repeat']})")
    L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    sys.exit(main())
