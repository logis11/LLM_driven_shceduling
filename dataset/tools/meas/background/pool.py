#!/usr/bin/env python3
"""Pool the 9.7 background campaign's repeats into the tables the archetypes take
(method §5; changelog D13–D15) and render them as results.md.

pool.py <artifacts-dir> <out.json> [--md results.md] [--cpu-model TEXT] [--tag TAG]

<artifacts-dir> holds one folder per (program, repeat) named
meas-background-<app>-r<k>-<mode> (as uploaded), at any depth, so the runs of
one campaign can be downloaded side by side into one folder each. A job the
machine gate stopped (report.json gate=wrong-machine), one the network gate stopped (gate=no-vf) and, with --cpu-model, a
repeat measured on another CPU model are listed, not pooled. Per program and
phase: every repeat is analysed (analyze.analyze_phase) once, the result and its samples cached beside the
repeat (pool-cache/, keyed by the analysis code), and the samples of all
repeats are pooled — one table at a time — into the quantile table (p1 … p99.9; µs, bytes for bytes per
wake), over all the program's threads and per thread (comm#rank), with the
per-repeat mean as the spread (§5 "Distribution form", §9 D19). Then: the
shared stability rule (stability.py) on the list — every table the fold-in
carries, each by its per-repeat mean (D19): the tolerance the larger of 5 % and
1 µs for times, 5 % for bytes per wake, over at least five repeats (D18); per
value the repeat count at which the present spread would hold, whose largest is,
in probe mode, the first batch (D14 (3)); the two checks (D15) and the
comparisons (D8, D6, D10, D12) as ratios of pooled medians with the per-repeat
spread, a difference within ± TOLERANCE reported as not resolved (D14 (2)); and
what §5 "Also reported" lists — the set check (D7), the D11 robustness line,
the achieved download rate, the cached fraction of every warm phase.
"""

import argparse
import glob
import hashlib
import json
import os
import re
import statistics
import sys

import numpy as np

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.background import analyze  # noqa: E402
from meas.stability import stability, TOLERANCE, T975  # noqa: E402
from meas.distribution import quantile_table  # noqa: E402
pct, QUANTILE_PROBS = analyze.pct, analyze.QUANTILE_PROBS

NAME = re.compile(r"^meas-background-(borg|7z|steamcmd)-r(\d+)-(dry|probe|full)$")
PHASES = {"borg": ("borg-first-warm", "borg-repeat-warm", "borg-first-cold", "borg-repeat-cold"),
          "7z": ("7z-mmt8-warm", "7z-mmt1-warm", "7z-mmt8-cold"),
          "steamcmd": ("steam-fresh-shaped", "steam-fresh-untraced", "steam-fresh-unshaped", "steam-update-shaped")}
# D19 (the shared stability rule): the list — every table the fold-in carries, each tested by its per-repeat mean. D29
# (9.6 D21, D22, D25): each archetype compiles as cpu-batch's batch loop, so it carries the program's runs between
# voluntary blocks, pooled over its threads, and the block after each run — the program-level off-CPU time, zero when
# another thread runs on; the per-wake tables of D19's first list are reported, not carried
LIST = {app: [(ph, "batch_run_us", "run between voluntary blocks (µs)"), (ph, "batch_block_us", "block per run (µs)")]
        for app, ph in (("borg", "borg-first-warm"), ("7z", "7z-mmt8-warm"), ("steamcmd", "steam-fresh-shaped"))}
# D14 (1): the headline medians, pooled over all the program's threads — read by the comparisons (results only)
HEADLINE = {"borg": [("borg-first-warm", "run_us", "run per wake (µs)"), ("borg-first-warm", "wait_us", "wait per wake (µs)")],
            "7z": [("7z-mmt8-warm", "run_us", "run per wake (µs)"), ("7z-mmt8-warm", "wait_us", "wait per wake (µs)")],
            "steamcmd": [("steam-fresh-shaped", "run_us", "run per wake (µs)"), ("steam-fresh-shaped", "network_us", "network wait (µs)"),
                         ("steam-fresh-shaped", "bytes_per_wake", "bytes per wake")]}
# results only: (a, b, what) — the headline medians side by side
COMPARISONS = {"borg": [("borg-first-warm", "borg-first-cold", "warm against cold, first backup (D8)"),
                        ("borg-repeat-warm", "borg-repeat-cold", "warm against cold, repeat backup (D8)"),
                        ("borg-first-warm", "borg-repeat-warm", "first against repeat backup (D6)")],
               "7z": [("7z-mmt8-warm", "7z-mmt8-cold", "warm against cold (D8)")],
               "steamcmd": [("steam-fresh-shaped", "steam-fresh-unshaped", "shaped against unshaped (D10)"),
                            ("steam-fresh-shaped", "steam-update-shaped", "fresh install against update (D12)")]}
# D18 (9.6 D23, D24): the tolerance is the larger of TOLERANCE × mean and the trace's 1 µs for times — bytes per wake,
# a count of whole bytes, has no floor — and the rule holds only over at least five same-machine repeats
ABS_FLOOR_US = 1.0
MIN_REPEATS = 5
SAMPLE_KEYS = ("run_us", "wait_us", "disk_us", "uninterruptible_us", "network_us", "sleep_us", "runnable_us", "bytes_per_wake", "batch_run_us", "batch_block_us")
APPLIED_MBPS, NETWORK_TABLE_MBPS = 121.0, 128.9   # D11: the applied rate; the network table's byte-weighted median


def pct_sorted(v, q):
    """analyze.pct on an already sorted array, the same arithmetic on the same doubles."""
    n = len(v)
    if not n:
        return None
    k = (n - 1) * q
    lo, hi = int(k), min(int(k) + 1, n - 1)
    a, b = float(v[lo]), float(v[hi])
    return round(a + (b - a) * (k - lo), 3)


def pooled(by_repeat):
    """by_repeat: repeat -> float64 array of one table's samples. Each array is sorted once, the pooled one once."""
    reps = sorted((r, np.asarray(vs, dtype=np.float64)) for r, vs in by_repeat.items())
    allv = np.sort(np.concatenate([vs for _r, vs in reps])) if reps else np.empty(0)
    out = {"n": int(len(allv)), "q": [round(pct_sorted(allv, q), 1) for q in QUANTILE_PROBS] if len(allv) else None,
           "p50": round(pct_sorted(allv, .5), 1) if len(allv) else None,
           "table": quantile_table(allv) if len(allv) else None}
    del allv
    out["repeat_p50"] = {r: (round(pct_sorted(np.sort(vs), .5), 1) if len(vs) else None) for r, vs in reps}
    out["repeat_mean"] = {r: (round(statistics.fmean(vs.tolist()), 4) if len(vs) else None) for r, vs in reps}
    out["repeat_n"] = {r: int(len(vs)) for r, vs in reps}
    return out


# ---- per-repeat analysis, cached --------------------------------------------------
CACHE_VERSION = 1


def code_hash():
    """The analysis code a cached result was made by: a change to it makes every cache stale."""
    h = hashlib.sha256(str(CACHE_VERSION).encode())
    for m in (analyze, analyze.nettrace, analyze._build, analyze.shapes, sys.modules["meas.stability"]):
        h.update(open(m.__file__, "rb").read())
    return h.hexdigest()[:16]


def cached_phase(d, ph, meas_cpu, edges, kv, code):
    """analyze_phase for one repeat's phase, from pool-cache/ when the same code made it. The samples leave the
    result: they are kept per thread as float64 arrays in <phase>.npz — the program's "all" samples are the
    concatenation of its threads', so only the threads' are stored."""
    cdir = os.path.join(d, "pool-cache")
    meta_p, npz_p = os.path.join(cdir, f"{ph}.json"), os.path.join(cdir, f"{ph}.npz")
    if os.path.exists(meta_p):
        m = json.load(open(meta_p))
        if m.get("code") == code and m.get("meas_cpu") == meas_cpu and ("missing" in m["result"] or os.path.exists(npz_p)):
            r = m["result"]
            if "missing" not in r:
                r["_npz"] = npz_p
            return r
    r = analyze.analyze_phase(d, ph, meas_cpu, edges, kv)
    os.makedirs(cdir, exist_ok=True)
    if "missing" not in r:
        smp = r.pop("_samples")
        r["_threads"] = list(smp["threads"])
        arrays = {f"t{i}__{s}": np.asarray(smp["threads"][t][s], dtype=np.float64)
                  for i, t in enumerate(r["_threads"]) for s in SAMPLE_KEYS}
        del smp
        np.savez(npz_p + ".tmp.npz", **arrays)
        os.replace(npz_p + ".tmp.npz", npz_p)
        del arrays
    json.dump({"code": code, "meas_cpu": meas_cpu, "result": r}, open(meta_p + ".tmp", "w"))
    os.replace(meta_p + ".tmp", meta_p)
    r = json.load(open(meta_p))["result"]   # the same JSON form a cached read gives
    if "missing" not in r:
        r["_npz"] = npz_p
    return r


def samples_of(A, t, s):
    """One repeat's samples of table s: of thread t, or of all the program's threads when t is None."""
    with np.load(A["_npz"]) as z:
        if t is None:
            parts = [z[f"t{i}__{s}"] for i in range(len(A["_threads"]))]
            return np.concatenate(parts) if parts else np.empty(0)
        if t not in A["_threads"]:
            return np.empty(0)
        return z[f"t{A['_threads'].index(t)}__{s}"]


def _analyse_one(job):
    d, ph, meas_cpu, code = job
    cached_phase(d, ph, meas_cpu, analyze.load_edges(d), kvfile(os.path.join(d, "report.kv")), code)
    return d, ph


def median_of(d):
    v = [x for x in d.values() if x is not None]
    return statistics.median(v) if v else None


def floor_of(key):
    return None if key == "bytes_per_wake" else ABS_FLOOR_US


def value_stability(key, values_by_repeat):
    return stability(values_by_repeat, floor_of(key), MIN_REPEATS)


def first_batch(values, abs_floor=None, min_k=None):
    """The repeats one value needs (D14 (3) with D18, D19): the smallest repeat count, at least min_k, at which the
    95 % half-width of the across-repeat mean, at the spread of the given repeats, is within the tolerance — the larger
    of TOLERANCE × mean and abs_floor (t multiplier; normal beyond the table)."""
    v = [x for x in values if x]
    if len(v) < 2:
        return None
    m, sd = statistics.fmean(v), statistics.stdev(v)
    bound = max(TOLERANCE * m, abs_floor or 0.0)
    for k in range(max(2, min_k or 2), 201):
        t = T975.get(k, 1.96 if k > max(T975) else None)
        if t is not None and t * sd / k ** 0.5 <= bound:
            return k
    return None


def criterion(app, entry):
    """D19: the shared stability rule on every table of the list, each by its per-repeat mean, with the repeat count at
    which its present spread would hold."""
    crit = {}
    for ph, key, label in LIST[app]:
        P = entry["phases"].get(ph, {})
        if P.get("missing") or key not in P.get("all", {}):
            continue
        vals = P["all"][key]["repeat_mean"]
        crit[f"{ph} {label}"] = {**value_stability(key, vals), "needed": first_batch(list(vals.values()), floor_of(key), MIN_REPEATS)}
    return crit


def compare(a, b):
    """b against a: the ratio, and the reading under D14 (2)."""
    if a in (None, 0) or b is None:
        return {"a": a, "b": b, "ratio": None, "reading": None}
    r = b / a
    return {"a": a, "b": b, "ratio": round(r, 4), "reading": "not resolved" if abs(r - 1) <= TOLERANCE else "difference"}


def ratio_by_repeat(num, den):
    return {r: (round(num[r] / den[r], 4) if num.get(r) and den.get(r) else None) for r in sorted(set(num) & set(den))}


def kvfile(path):
    try:
        return dict(line.rstrip("\n").split("=", 1) for line in open(path) if "=" in line)
    except OSError:
        return {}


def find_runs(root, cpu_model):
    runs, gated, other = {}, [], []
    for d in sorted(glob.glob(os.path.join(root, "**", "meas-background-*"), recursive=True)):
        m = NAME.match(os.path.basename(d))
        if not m or not os.path.exists(os.path.join(d, "report.json")):
            continue
        app, k, mode = m.group(1), int(m.group(2)), m.group(3)
        rpt = json.load(open(os.path.join(d, "report.json")))
        if rpt.get("gate") in ("wrong-machine", "no-vf"):
            gated.append({"app": app, "repeat": k, "cpu_model": rpt.get("machine.model"), "path": os.path.relpath(d, root)})
            continue
        spec = json.load(open(os.path.join(d, "spec.json"))) if os.path.exists(os.path.join(d, "spec.json")) else {}
        model = spec.get("cpu_model") or ""
        if cpu_model and cpu_model not in model:
            other.append({"app": app, "repeat": k, "cpu_model": model, "path": os.path.relpath(d, root)})
            continue
        runs.setdefault(app, {})[k] = {"dir": d, "mode": mode, "report": rpt, "spec": spec}
    return runs, gated, other


def pool_app(app, reps, jobs=1):
    ks = sorted(reps)
    code = code_hash()
    if jobs > 1:   # fill the cache first, several phases at a time; the pooling below then reads it
        import multiprocessing
        todo = [(reps[k]["dir"], ph, int(reps[k]["report"].get("pin.load_cpu", 3)), code)
                for k in ks for ph in analyze.phases_in(reps[k]["dir"])]
        with multiprocessing.get_context("spawn").Pool(jobs, maxtasksperchild=1) as mp:
            for d, ph in mp.imap_unordered(_analyse_one, todo):
                print(f"   analysed {os.path.basename(d)} {ph}", file=sys.stderr, flush=True)
    per = {}
    for k in ks:
        d = reps[k]["dir"]
        kv = kvfile(os.path.join(d, "report.kv"))
        meas_cpu = int(reps[k]["report"].get("pin.load_cpu", 3))
        edges = analyze.load_edges(d)
        phases = [p for p in analyze.phases_in(d)]
        per[k] = {"kv": kv, "phases": {ph: cached_phase(d, ph, meas_cpu, edges, kv, code) for ph in phases}}
    spec = {k: reps[k]["spec"] for k in ks}
    entry = {"repeats": ks, "mode": {k: reps[k]["mode"] for k in ks},
             "cpu_model": {k: spec[k].get("cpu_model") for k in ks},
             "kernel": {k: ((spec[k].get("uname") or "").split() + [None, None, None])[2] for k in ks},
             "run_id": {k: (spec[k].get("github_run") or {}).get("GITHUB_RUN_ID") for k in ks},
             "versions": {k: {x: per[k]["kv"].get(x) for x in ("borg.version", "7z.version", "zpaq.version", "steamcmd.version",
                                                              "steam.app", "steam.buildid", "perf.version", "kernel")
                             if per[k]["kv"].get(x)} for k in ks},
             "phases": {}}
    all_phases = [p for p in PHASES[app] if any(p in per[k]["phases"] for k in ks)]
    all_phases += sorted({p for k in ks for p in per[k]["phases"]} - set(all_phases))
    for ph in all_phases:
        have = [k for k in ks if ph in per[k]["phases"] and "missing" not in per[k]["phases"][ph]]
        if not have:
            entry["phases"][ph] = {"missing": True}
            continue
        A = {k: per[k]["phases"][ph] for k in have}
        P = {"repeats": have, "cmd_wall_s": {k: A[k]["cmd_wall_s"] for k in have}, "rc": {k: A[k]["rc"] for k in have},
             "program_cpu_us": {k: A[k]["program_cpu_us"] for k in have},
             "program_taskstats_cpu_us": {k: A[k]["program_taskstats_cpu_us"] for k in have},
             "resumes_merged": {k: A[k]["resumes_merged"] for k in have},
             "taskstats_enobufs": {k: A[k]["taskstats_trailer"].get("enobufs") for k in have},
             "all": {s: pooled({k: samples_of(A[k], None, s) for k in have}) for s in SAMPLE_KEYS},
             "threads": {},
             "processes": {k: [{x: p[x] for x in ("pid", "role", "exec", "threads", "perf_cpu_us", "taskstats_cpu_us",
                                                  "perf_over_taskstats", "disk")} for p in A[k]["processes"] if p["program"] or p["disk"]]
                           for k in have},
             "outside_on_measured_cpu": {k: dict(list(A[k]["outside_on_measured_cpu"].items())[:5]) for k in have}}
        if any("cached_fraction" in A[k] for k in have):
            P["cached_fraction"] = {k: A[k].get("cached_fraction") for k in have}
        if any("network" in A[k] for k in have):
            P["network"] = {k: A[k].get("network") for k in have}
        keys = sorted({t for k in have for t in A[k]["_threads"]},
                      key=lambda t: -sum(A[k]["threads"].get(t, {}).get("cpu_us", 0) for k in have))
        for t in keys:
            P["threads"][t] = {"cpu_us": {k: A[k]["threads"].get(t, {}).get("cpu_us") for k in have},
                               **{s: pooled({k: samples_of(A[k], t, s) for k in have}) for s in SAMPLE_KEYS}}
        entry["phases"][ph] = P
    # D19: the shared stability rule on the list; in probe mode the first batch it sets (D14 (3))
    crit = criterion(app, entry)
    fb = {q: c["needed"] for q, c in crit.items()}
    entry["stability"] = {"tolerance": TOLERANCE, "abs_floor_us": ABS_FLOOR_US, "min_repeats": MIN_REPEATS, "quantities": crit,
                          "passes": bool(crit) and all(c["passes"] for c in crit.values())}
    entry["first_batch"] = {"by_quantity": fb, "count": max(fb.values()) if fb and all(fb.values()) else None}
    entry["checks"] = checks(app, entry, per)
    entry["comparisons"] = comparisons(app, entry)
    entry["also"] = also(app, entry, per)
    return entry


def checks(app, entry, per):
    """D15: (a) 7z at one thread against eight — CPU per byte, per-wake run and wait; (b) SteamCMD untraced against
    traced — the program's CPU total from exit accounting and the download's duration."""
    ph = entry["phases"]
    out = {}
    if app == "7z":
        a, b = ph.get("7z-mmt8-warm", {}), ph.get("7z-mmt1-warm", {})
        if a and b and not a.get("missing") and not b.get("missing"):
            nb = {k: int(per[k]["kv"].get("set.bytes") or 0) or None for k in entry["repeats"]}
            cpb_a = {k: (v / nb[k] if v and nb.get(k) else None) for k, v in a["program_cpu_us"].items()}
            cpb_b = {k: (v / nb[k] if v and nb.get(k) else None) for k, v in b["program_cpu_us"].items()}
            out["mmt1 against mmt8: CPU per byte"] = {**compare(median_of(cpb_a), median_of(cpb_b)), "per_repeat": ratio_by_repeat(cpb_b, cpb_a)}
            for key, label in (("run_us", "run per wake"), ("wait_us", "wait per wake")):
                out[f"mmt1 against mmt8: {label}"] = {**compare(a["all"][key]["p50"], b["all"][key]["p50"]),
                                                      "per_repeat": ratio_by_repeat(b["all"][key]["repeat_p50"], a["all"][key]["repeat_p50"])}
    if app == "steamcmd":
        a, b = ph.get("steam-fresh-shaped", {}), ph.get("steam-fresh-untraced", {})
        if a and b and not a.get("missing") and not b.get("missing"):
            for key, label in (("program_taskstats_cpu_us", "CPU total (exit accounting)"), ("cmd_wall_s", "download duration")):
                out[f"untraced against traced: {label}"] = {**compare(median_of(a[key]), median_of(b[key])),
                                                           "per_repeat": ratio_by_repeat(b[key], a[key])}
    return out


def comparisons(app, entry):
    ph = entry["phases"]
    out = {}
    for pa, pb, what in COMPARISONS[app]:
        a, b = ph.get(pa, {}), ph.get(pb, {})
        if not a or not b or a.get("missing") or b.get("missing"):
            continue
        rows = {}
        for _h, key, label in HEADLINE[app]:
            if a["all"][key]["n"] and b["all"][key]["n"]:
                rows[label] = {**compare(a["all"][key]["p50"], b["all"][key]["p50"]),
                               "per_repeat": ratio_by_repeat(b["all"][key]["repeat_p50"], a["all"][key]["repeat_p50"])}
        rows["CPU total (perf)"] = {**compare(median_of(a["program_cpu_us"]), median_of(b["program_cpu_us"])),
                                    "per_repeat": ratio_by_repeat(b["program_cpu_us"], a["program_cpu_us"])}
        rows["duration"] = {**compare(median_of(a["cmd_wall_s"]), median_of(b["cmd_wall_s"])),
                            "per_repeat": ratio_by_repeat(b["cmd_wall_s"], a["cmd_wall_s"])}
        out[f"{what}: {pb} against {pa}"] = rows
    return out


def achieved(net):
    t = (net or {}).get("transfer") or {}
    return {"per_second_byte_weighted_median": t.get("per_second_mbps_byte_weighted_median"),
            "wire_over_payload": t.get("wire_over_payload"), "over_command": (net or {}).get("achieved_mbps_counters")}


def also(app, entry, per):
    out = {}
    ks = entry["repeats"]
    if app in ("borg", "7z"):
        out["set_check"] = {k: {x[len("set."):]: per[k]["kv"].get(x) for x in per[k]["kv"] if x.startswith("set.")} for k in ks}
    if app == "steamcmd":
        out["d11_robustness"] = {"applied_mbps": APPLIED_MBPS, "network_table_byte_weighted_median_mbps": NETWORK_TABLE_MBPS,
                                 "difference": round(NETWORK_TABLE_MBPS / APPLIED_MBPS - 1, 4)}
        # the rate while data flows (the payload's per-second rates, their byte-weighted median; traced phases), and over the
        # whole command from the interface counters (every phase; login and commit included)
        out["achieved_mbps"] = {ph: {k: achieved((P.get("network") or {}).get(k)) for k in P["repeats"]}
                                for ph, P in entry["phases"].items() if not P.get("missing")}
        out["shaping"] = {k: {x: per[k]["kv"].get(x) for x in per[k]["kv"] if x.startswith(("tc.", "shape."))} for k in ks}
    cached = {ph: P["cached_fraction"] for ph, P in entry["phases"].items() if not P.get("missing") and "cached_fraction" in P}
    if cached:
        out["cached_fraction"] = cached
    return out


# ---- results.md ---------------------------------------------------------------------

def fmt_q(q):
    return " / ".join("–" if x is None else (f"{x:.0f}" if abs(x) >= 100 else f"{x:.1f}") for x in q) if q else "–"


def render(out):
    L = [f"# 9.7 background campaign — pooled results{' (' + out['tag'] + ')' if out.get('tag') else ''}", "",
         f"Machine {out.get('machine') or 'any'}; stopped by the machine gate {len(out['gated_out'])}; other-model repeats "
         f"{len(out['other_machine'])}. Quantile tables are p1 / p5 / p10 / p25 / p50 / p75 / p90 / p95 / p99 / p99.9, times in µs, "
         f"bytes per wake in bytes; the spread is the per-repeat mean. Rules: method §5 and §9.", ""]
    for app, E in out["runs"].items():
        L += [f"## {app}", "", f"Repeats {E['repeats']}; mode {E['mode']}; CPU {E['cpu_model']}; kernel {E['kernel']}; runs {E['run_id']}.", ""]
        for k, v in E["versions"].items():
            L.append(f"- repeat {k}: {v}")
        L.append("")
        for ph, P in E["phases"].items():
            if P.get("missing"):
                L += [f"### {ph}", "", "missing", ""]
                continue
            L += [f"### {ph}", "",
                  f"command s {P['cmd_wall_s']}; rc {P['rc']}; program CPU µs (perf) {P['program_cpu_us']}; (taskstats) {P['program_taskstats_cpu_us']}; "
                  f"resumes merged {P['resumes_merged']}; ENOBUFS {P['taskstats_enobufs']}"
                  + (f"; cached fraction {P['cached_fraction']}" if "cached_fraction" in P else ""), "",
                  "| threads | quantity | n | quantiles | spread (per-repeat mean) |", "|---|---|---|---|---|"]
            for s in SAMPLE_KEYS:
                x = P["all"][s]
                if x["n"]:
                    L.append(f"| all | {s} | {x['n']} | {fmt_q(x['q'])} | {x['repeat_mean']} |")
            for t, T in list(P["threads"].items())[:12]:
                for s in ("run_us", "wait_us", "disk_us", "network_us", "bytes_per_wake"):
                    x = T[s]
                    if x["n"]:
                        L.append(f"| `{t}` | {s} | {x['n']} | {fmt_q(x['q'])} | {x['repeat_mean']} |")
            L.append("")
            for k, procs in P["processes"].items():
                for p in procs:
                    L.append(f"- repeat {k}: `{p['role']}` [{p['pid']}] {p['exec']} threads {p['threads']}; perf/taskstats CPU {p['perf_over_taskstats']}; disk {p['disk']}")
            if "network" in P:
                for k, n in P["network"].items():
                    if n:
                        L.append(f"- repeat {k} network: " + json.dumps({x: n[x] for x in n if x not in ("calls_by_name_kind",)}))
            L.append("")
        st = E["stability"]
        L += ["### Stability rule (D18, D19)", "", f"**{'Holds' if st['passes'] else 'Does not hold yet'}** (each table on the list by "
              f"its per-repeat mean; tolerance the larger of {st['tolerance']:.0%} and {st['abs_floor_us']:g} µs for times, at least "
              f"{st['min_repeats']} repeats). Repeats needed at the spread of these repeats: {E['first_batch']['count'] or 'over 200'}.", "",
              "| quantity | repeats | mean | cv | 95 % half-width | leave-one-out | needed at this spread | passes |",
              "|---|---|---|---|---|---|---|---|"]
        for q, c in st["quantities"].items():
            hw = "–" if c["half_width"] is None else f"±{c['half_width']:.1%}"
            cv = "–" if c["cv"] is None else f"{c['cv']:.1%}"
            lo = "–" if c["leave_one_out"] is None else f"{c['leave_one_out']:.1%}"
            L.append(f"| {q} | {c['k']} | {c['mean']} | {cv} | {hw} | {lo} | {c['needed'] or 'over 200'} | {'yes' if c['passes'] else 'no'} |")
        L.append("")
        if E["checks"]:
            L += ["### Checks (D15)", ""]
            for q, c in E["checks"].items():
                L.append(f"- {q}: {c['ratio']} — {c['reading']} (per repeat {c['per_repeat']})")
            L.append("")
        if E["comparisons"]:
            L += ["### Comparisons (results only)", ""]
            for what, rows in E["comparisons"].items():
                L.append(f"- {what}: " + "; ".join(f"{q} {c['ratio']} ({c['reading']})" for q, c in rows.items()))
            L.append("")
        if E["also"]:
            L += ["### Also reported", ""]
            for q, v in E["also"].items():
                L.append(f"- {q}: {v}")
            L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts"); ap.add_argument("out"); ap.add_argument("--md")
    ap.add_argument("--cpu-model", default="", help="pool only repeats whose CPU model contains this text")
    ap.add_argument("--tag", default="", help="the campaign tag, meas-ci:background:<launch date of the first batch>")
    ap.add_argument("--jobs", type=int, default=1, help="phases analysed at a time when the cache is filled")
    args = ap.parse_args()
    runs, gated, other = find_runs(args.artifacts, args.cpu_model)
    if not runs:
        print("no repeats found", file=sys.stderr)
        return 1
    out = {"tag": args.tag or None, "machine": args.cpu_model or None, "gated_out": gated, "other_machine": other, "runs": {}}
    for app in ("borg", "7z", "steamcmd"):
        if app in runs:
            out["runs"][app] = E = pool_app(app, runs[app], args.jobs)
            st = E["stability"]
            print(f"== {app}: repeats {E['repeats']}; stability {'holds' if st['passes'] else 'does not hold yet'}; first batch {E['first_batch']['count']}")
            for q, c in st["quantities"].items():
                print(f"   {q}: k {c['k']} mean {c['mean']} half-width {c['half_width']} needed {c['needed']}")
    json.dump(out, open(args.out, "w"), indent=1)
    if args.md:
        open(args.md, "w").write(render(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
