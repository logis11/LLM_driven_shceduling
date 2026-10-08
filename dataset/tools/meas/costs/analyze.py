#!/usr/bin/env python3
"""One kernel-cost repeat's values (9.12 campaign, research-slice changelog D31), from the outputs costs/run.sh
writes into <out>:

- `pingpong.txt`: the pair's ns per round trip and context switches per round trip (`ctxt_delta` / n), the self
  pipe's ns per write+read pair, each the mean over the repeat's runs; the direct switch estimate
  (pair − 2 × self) / 2, Li, Ding & Shen's subtraction: a round trip holds two switches and, over both processes,
  two writes and two reads.
- `perf-bench-pipe.txt`: µs per operation (one round trip), the mean over the runs.
- `lat_ctx.txt`: lmbench's per-switch time and its measured overhead at each process size.
- `trace.<function>.<load>.json`: the per-call durations (graph_durations.py).
- `perfstat.idle.<w>.csv`, `schedstat.idle.<w>.{start,end}`, `idle.txt`: per CPU, context switches and schedule()
  calls per second over each idle window, then the mean over the windows.

    analyze.py <out>   → JSON on stdout
"""

import glob
import json
import os
import re
import statistics
import sys


def kv(line):
    return dict(p.split("=", 1) for p in line.split() if "=" in p)


def pingpong(out):
    pair, self_ = [], []
    for line in open(os.path.join(out, "pingpong.txt"), errors="replace"):
        d = kv(line)
        if d.get("mode") == "pair" and d.get("child_status") == "0":
            pair.append((float(d["ns_per_round_trip"]), int(d["ctxt_delta"]) / int(d["n"])))
        elif d.get("mode") == "self":
            self_.append(float(d["ns_per_pair"]))
    res = {"pair_runs": len(pair), "self_runs": len(self_)}
    if pair:
        res["pair_ns_per_round_trip"] = statistics.fmean(p[0] for p in pair)
        res["pair_switches_per_round_trip"] = statistics.fmean(p[1] for p in pair)
        res["pair_ns_per_round_trip_runs"] = [p[0] for p in pair]
    if self_:
        res["self_ns_per_pair"] = statistics.fmean(self_)
        res["self_ns_per_pair_runs"] = self_
    if pair and self_:
        res["switch_ns_direct"] = (res["pair_ns_per_round_trip"] - 2 * res["self_ns_per_pair"]) / 2
        res["switch_ns_half_round_trip"] = res["pair_ns_per_round_trip"] / 2
    return res


def perf_bench(out):
    runs = [float(m.group(1)) for m in re.finditer(r"([0-9.]+) usecs/op", open(os.path.join(out, "perf-bench-pipe.txt"), errors="replace").read())]
    return {"perf_pipe_us_per_op": statistics.fmean(runs) if runs else None, "perf_pipe_runs": runs}


def lat_ctx(out):
    res, size = {}, None
    path = os.path.join(out, "lat_ctx.txt")
    if not os.path.exists(path):
        return res
    for line in open(path, errors="replace"):
        line = line.strip().strip('"')
        m = re.match(r"## -s (\d+)", line)
        if m:
            size = m.group(1)
            continue
        m = re.match(r"size=(\d+)k ovr=([0-9.]+)", line)
        if m:
            res[f"lat_ctx_ovr_us_{size}k"] = float(m.group(2))
            continue
        m = re.match(r"^2 ([0-9.]+)$", line)
        if m and size is not None:
            res[f"lat_ctx_us_{size}k"] = float(m.group(1))
    return res


def load_line(path):
    """The pingpong line of a load's output: ns per round trip (pair) or per call (getpid), and n."""
    if not os.path.exists(path):
        return None
    for line in open(path, errors="replace"):
        d = kv(line)
        if d.get("mode") == "pair" and d.get("child_status") == "0":
            return {"ns": float(d["ns_per_round_trip"]), "n": int(d["n"])}
        if d.get("mode") == "getpid":
            return {"ns": float(d["ns_per_call"]), "n": int(d["n"])}
    return None


def traces(out):
    """Per traced pass, the durations; where the load is the ping-pong or the getpid loop, its cost per round trip
    or call traced and untraced, and the tracer's whole cost per traced call: the difference over the calls per
    round trip (the trace's count over the load's n)."""
    res = {}
    untraced = {"pingpong": load_line(os.path.join(out, "untraced.pingpong.load.txt")),
                "getpid": load_line(os.path.join(out, "untraced.getpid.load.txt"))}
    for path in sorted(glob.glob(os.path.join(out, "trace.*.json"))):
        name = os.path.basename(path)[len("trace."):-len(".json")]
        try:
            res[name] = json.load(open(path))
        except ValueError:
            res[name] = None
            continue
        label = name.rsplit(".", 1)[1]
        traced = load_line(os.path.join(out, f"trace.{name}.load.txt"))
        base = untraced.get(label)
        if traced and base and res[name].get("n"):
            calls = res[name]["n"] / traced["n"]
            res[name].update({"load_ns_traced": traced["ns"], "load_ns_untraced": base["ns"], "calls_per_load_unit": calls,
                              "tracer_ns_per_call": (traced["ns"] - base["ns"]) / calls if calls else None})
    return res


def schedstat(path):
    cpus = {}
    for line in open(path, errors="replace"):
        parts = line.split()
        if parts and re.fullmatch(r"cpu\d+", parts[0]) and len(parts) >= 10:
            cpus[int(parts[0][3:])] = {"sched_count": int(parts[3]), "sched_goidle": int(parts[4]),
                                       "ttwu_count": int(parts[5])}
    return cpus


def idle(out):
    windows = []
    spans = {}
    for line in open(os.path.join(out, "idle.txt"), errors="replace"):
        d = kv(line)
        spans[d["window"]] = (int(d["t1_us"]) - int(d["t0_us"])) / 1e6
    for w, secs in sorted(spans.items()):
        row = {"window": int(w), "seconds": secs, "cs_per_s": {}, "schedule_per_s": {}, "goidle_per_s": {}}
        csv = os.path.join(out, f"perfstat.idle.{w}.csv")
        if os.path.exists(csv):
            for line in open(csv, errors="replace"):
                parts = line.strip().split(",")
                if len(parts) > 3 and parts[0].startswith("CPU") and parts[3].startswith("context-switches"):
                    try:
                        row["cs_per_s"][int(parts[0][3:])] = int(parts[1]) / secs
                    except ValueError:
                        pass
        a, b = os.path.join(out, f"schedstat.idle.{w}.start"), os.path.join(out, f"schedstat.idle.{w}.end")
        if os.path.exists(a) and os.path.exists(b):
            s0, s1 = schedstat(a), schedstat(b)
            for cpu in s1:
                if cpu in s0:
                    row["schedule_per_s"][cpu] = (s1[cpu]["sched_count"] - s0[cpu]["sched_count"]) / secs
                    row["goidle_per_s"][cpu] = (s1[cpu]["sched_goidle"] - s0[cpu]["sched_goidle"]) / secs
        windows.append(row)
    mean = {}
    for key in ("cs_per_s", "schedule_per_s", "goidle_per_s"):
        cpus = sorted({c for r in windows for c in r[key]})
        mean[key] = {c: statistics.fmean(r[key][c] for r in windows if c in r[key]) for c in cpus}
    return {"idle_windows": windows, "idle_mean": mean}


def main(out):
    report = json.load(open(os.path.join(out, "report.json"))) if os.path.exists(os.path.join(out, "report.json")) else {}
    res = {"measured_cpu": int(os.environ.get("MEAS_CPU", report.get("pin.load_cpu", "3")))}
    for part in (pingpong, perf_bench, lat_ctx):
        try:
            res.update(part(out))
        except OSError as err:
            res[part.__name__ + "_error"] = str(err)
    res["traces"] = traces(out)
    try:
        res.update(idle(out))
    except OSError as err:
        res["idle_error"] = str(err)
    json.dump(res, sys.stdout, indent=1, sort_keys=True)
    print()


if __name__ == "__main__":
    main(sys.argv[1])
