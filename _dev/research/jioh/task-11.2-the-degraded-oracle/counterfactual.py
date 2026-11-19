#!/usr/bin/env python3
"""A counterfactual run: one RQ0 run's config schedule with a knob moved, run on the pinned simulator, its records
and aggregates built by the harness as the runner builds them, and the case's term read beside the base run's.

    python3 counterfactual.py <workload_id> <name> --set INDEX.FIELD=VALUE [--set …] [--base-run 'oracle~focus']
        --entity editor --metric input_latency --aggregate p99 [--cause …] [--channel …]

FIELD is `batch_bandwidth_cap`, `algorithm` or `params.<name>` of the schedule's entry INDEX; VALUE is JSON.
The run goes to `counterfactual/<workload_id>/<name>/` beside this script — `schedule.json`, `trace.jsonl.gz`,
`records.csv.gz`, `aggregates.csv`, `result.json`. The term is the aggregate row the scores file reads for it,
beside the post hoc `scores.csv`'s oracle value; the trace's hash beside the base run's, which a run with
nothing moved reproduces."""
import argparse
import copy
import csv
import gzip
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import aggregates as agg, evaluator, records, scoring  # noqa: E402

SPEC = REPO / "harness" / "experiments" / "rq0-gate.yaml"
SIM = REPO / "simulator" / "src" / "sim"
BUILD = REPO / "dataset" / "build" / "coreset-single"
RUNS = REPO / "runs" / "rq0-gate"
KEY = ("entity", "metric", "aggregate", "cause", "channel", "window_start_us", "window_end_us")


def term_rows(aggs, want):
    return [a for a in aggs if all(str(a.get(k, "")) == want.get(k, "") for k in KEY)]


def build(workload, run_dir, spec, wid, table):
    rows, messages = records.build(workload, run_dir / "trace.jsonl", table=table, seed="",
                                   schedule_path=run_dir / "schedule.json", boot_default="", telemetry="focus")
    records.write_csv(rows, run_dir / "records.csv.gz")
    aggs = agg.compute_aggregates(rows, scoring.windows_from_spec(spec, wid), scoring.interactive_from_spec(spec, wid))
    return aggs, messages


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("workload_id")
    ap.add_argument("name")
    ap.add_argument("--set", action="append", default=[], dest="sets")
    ap.add_argument("--base-run", default="oracle~focus")
    ap.add_argument("--table", default="prior")
    for k in ("entity", "metric", "aggregate", "cause", "channel", "window_start_us", "window_end_us"):
        ap.add_argument(f"--{k.replace('_', '-')}", dest=k, default="")
    args = ap.parse_args()
    wid = args.workload_id
    want = {k: getattr(args, k) for k in KEY}
    pins = evaluator.load_spec(SPEC)["pins"]
    spec = scoring.load_spec(REPO / pins["scoring_spec"]["path"])
    workload = BUILD / f"{wid}.workload.json"
    base_dir = RUNS / wid / args.base_run
    out = pathlib.Path(__file__).parent / "counterfactual" / wid / args.name
    out.mkdir(parents=True, exist_ok=True)

    sched = json.load(open(base_dir / "schedule.json"))
    moved = copy.deepcopy(sched)
    for s in args.sets:
        lhs, value = s.split("=", 1)
        idx, field = lhs.split(".", 1)
        cfg = moved["schedule"][int(idx)]["config"]
        if field.startswith("params."):
            cfg.setdefault("params", {})[field.split(".", 1)[1]] = json.loads(value)
        else:
            cfg[field] = json.loads(value)
    (out / "schedule.json").write_text(json.dumps(moved, indent=1) + "\n")

    trace = out / "trace.jsonl"
    with open(out / "simulator.stderr.log", "w") as err:
        subprocess.run([str(SIM), "--workload", str(workload), "--schedule", str(out / "schedule.json"),
                        "--out-trace", str(trace)], check=True, stderr=err)
    aggs, messages = build(workload, out, spec, wid, args.table)
    with gzip.open(out / "trace.jsonl.gz", "wb") as g, open(trace, "rb") as f:
        shutil.copyfileobj(f, g)
    trace.unlink()
    with open(out / "aggregates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(aggs[0].keys()))
        w.writeheader()
        w.writerows(aggs)

    # the trace against the base run's own: a run with nothing moved must reproduce it byte for byte
    import hashlib
    with gzip.open(out / "trace.jsonl.gz", "rb") as f:
        trace_sha = hashlib.sha256(f.read()).hexdigest()
    base_sha = (base_dir / "trace.rerun.sha256").read_text().split()[0]
    cf_term = term_rows(aggs, want)
    scored = None
    with open(RUNS / "post-hoc" / "scores.csv", newline="") as f:
        for r in csv.DictReader(f):
            if (r["workload_id"] == wid and r["level"] == "term" and r["condition"] == "oracle"
                    and r["table"] == args.table and not r["boot_default"]
                    and all(r[k] == want[k] for k in KEY)):
                scored = r["value_oracle"]
    result = {"workload_id": wid, "name": args.name, "sets": args.sets, "term": want,
              "scored_oracle": scored, "trace_sha256": trace_sha, "base_trace_rerun_sha256": base_sha,
              "trace_equal_base": trace_sha == base_sha,
              "counterfactual": [a["value"] for a in cf_term], "records_messages": messages}
    if scored is not None and len(cf_term) == 1:
        result["moved_by"] = float(cf_term[0]["value"]) - float(scored)
    (out / "result.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
