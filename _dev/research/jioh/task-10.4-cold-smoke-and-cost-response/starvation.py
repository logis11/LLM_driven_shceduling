"""10.4 decisions 16–17: the starvation readings on the cold smoke.

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/starvation.py --smoke runs/cold-smoke [--workers N]

1. The guard table of every condition on the judging files: per condition and guard, the runs that pass, fail and
   are not applicable, every failed row named; a failed `starvation_floor` there reopens the executor's
   starvation net.
2. `simulator/tools/wait_check.py` on every run's trace: the guard's own reading (the longest wait a `run_start`
   ended after a `ready` line) and the three it cannot read — a wait still open at the end, a wait after a
   preemption ended by a `run_start`, one after a preemption still open. On a judging file, under any condition,
   one of those three over 30 s reopens the starvation net before the full run, past 15 s reopens the question
   with 인경민; on any other file it is recorded with its run.
3. Every run that fails `starvation_floor`, on any file, beside the five `oracle` runs named before the smoke
   (`simulator/memo/memo_261111.md` Part L).
4. The availability of every reporting line in the smoke's report (10.3 decision 8): each count, agreement or
   difference a line gives, available or not, with the failed runs a line names. Expected since the starvation
   net's decision session of 2026-11-15: the 100 ms boot default's sensitivity count, and the two chain-scale
   lines, `chain-x1.2` and `chain-x1.4`, on the four chain-scaled files' `oracle` and `random` runs'
   `starvation_floor`, and no other line.

A judging file's failed `starvation_floor` or unread wait under `ostep-slice-100000us` is the 100 ms point's own
(the same session) and is listed apart from what reopens.

Run from the repository root; writes starvation.json beside this file and prints its summary."""
import argparse
import collections
import concurrent.futures
import csv
import gzip
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
sys.path.insert(0, str(REPO / "simulator" / "tools"))
from harness import evaluator, manifests  # noqa: E402
import wait_check  # noqa: E402

SPEC = REPO / "harness" / "experiments" / "rq0-gate.yaml"
NET_US, QUESTION_US = 30_000_000, 15_000_000
NAMED_ORACLE = ("c3-evening", "c2-p2a@chain-x1.2", "c2-p2a@chain-x1.4", "c2-p2b@chain-x1.2", "c2-p2b@chain-x1.4")
# The starvation net's decision session of 2026-11-15: the 100 ms point's failures are the point's own; a run that
# holds EDF over the frame chain fails on the five files, oracle always, random on a seed that draws it.
SETTLED_BOOT_DEFAULT = "ostep-slice-100000us"
EXPECTED_UNAVAILABLE = ["sensitivity ostep-slice-100000us", "variant_set chain-x1.2", "variant_set chain-x1.4"]
EXPECTED_FAILED = sorted((w, c, "starvation_floor") for w in NAMED_ORACLE[1:] for c in ("oracle", "random"))


def availability(report):
    """Every count, agreement or difference a reporting line gives, and whether it is available."""
    out = []
    for line in report["lines"]:
        t = line["type"]
        if "available" in line:
            label = t + (f" {line['name']}" if "name" in line else "")
            out.append({"line": label, "available": line["available"],
                        "failed": [(r["workload_id"], r["condition"], r["guard"]) for r in line.get("failed", [])]})
        for r in line.get("rows", []):
            if "met" in r and "verdict" in r:            # a count per boot default, band table, g, latency floor
                key = next((r[k] for k in ("boot_default", "table", "g", "latency_floor_us") if k in r), "")
                out.append({"line": f"{t} {key or '(primary)'}", "available": r.get("available", r["verdict"] is not None),
                            "failed": []})
    return out


def run_name(r):
    return (f"{r['workload_id']}/{r['condition']}" + (f"-{r['seed']}" if r["seed"] else "")
            + (f"+{r['boot_default']}" if r["boot_default"] else "")
            + (f"@{r['table'].partition('@')[2]}" if "@" in r["table"] else "") + f"~{r['telemetry']}")


def check(entry):
    with gzip.open(entry["trace"], "rb") as f:
        r = wait_check.waits(f, wait_check.t_end_of(entry["workload"]))
    return {"run": run_name(entry), "workload_id": entry["workload_id"], "condition": entry["condition"],
            "boot_default": entry["boot_default"], "guard_reading_us": r["ready_done"][0], "guard_reading_task": r["ready_done"][1],
            "ready_open_us": r["ready_open"][0], "ready_open_task": r["ready_open"][1],
            "preempt_done_us": r["preempt_done"][0], "preempt_done_task": r["preempt_done"][1],
            "preempt_open_us": r["preempt_open"][0], "preempt_open_task": r["preempt_open"][1],
            "open_over_floor_count": r["open_over_floor_count"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    smoke = pathlib.Path(args.smoke)
    spec, _paths, _axes = manifests.expand(evaluator.load_spec(SPEC), REPO)
    judging = set(spec["files"]["judging"])

    # 1. the guard table on the judging files
    table = collections.defaultdict(collections.Counter)
    failed_judging, starvation_fails = [], []
    with open(smoke / "guards.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["guard"] == "starvation_floor" and r["result"] == "fail":
                starvation_fails.append({"run": run_name(r), "value_us": r["value"], "reason": r["reason"],
                                         "judging": r["workload_id"] in judging, "boot_default": r["boot_default"]})
            if r["workload_id"] not in judging:
                continue
            table[(r["condition"] + (f"@{r['table'].partition('@')[2]}" if "@" in r["table"] else ""),
                   r["guard"])][r["result"]] += 1
            if r["result"] == "fail":
                failed_judging.append({"run": run_name(r), "guard": r["guard"], "reason": r["reason"]})

    # 2. the wait check on every trace
    runs = json.loads((smoke / "guards-manifest.json").read_text())["runs"]
    with concurrent.futures.ProcessPoolExecutor(args.workers) as pool:
        waits = sorted(pool.map(check, runs, chunksize=4), key=lambda w: w["run"])
    unread = ("ready_open", "preempt_done", "preempt_open")
    findings = []
    for w in waits:
        for kind in unread:
            us = w[f"{kind}_us"]
            if us <= QUESTION_US:
                continue
            on_judging = w["workload_id"] in judging
            leads_to = ("reopens the starvation net" if us > NET_US else "reopens the question with 인경민") \
                if on_judging else "recorded with its run"
            if on_judging and w["boot_default"] == SETTLED_BOOT_DEFAULT:
                leads_to = "the 100 ms point's, settled 2026-11-15"
            findings.append({"run": w["run"], "kind": kind, "wait_us": us, "task": w[f"{kind}_task"],
                             "judging": on_judging, "boot_default": w["boot_default"], "leads_to": leads_to})

    # 4. every line's availability in the smoke's report
    lines = availability(json.loads((smoke / "report.json").read_text()))
    unavailable = [l for l in lines if not l["available"]]
    failed_named = sorted({f for l in unavailable for f in l["failed"]})
    as_expected = ([l["line"] for l in unavailable] == EXPECTED_UNAVAILABLE
                   and all(f in EXPECTED_FAILED for f in failed_named) and failed_named != [])

    reopened = [f for f in starvation_fails + findings
                if f["judging"] and f["boot_default"] != SETTLED_BOOT_DEFAULT]
    settled = [f for f in starvation_fails + findings
               if f["judging"] and f["boot_default"] == SETTLED_BOOT_DEFAULT]
    doc = {"smoke": str(smoke), "runs": len(waits), "judging_files": sorted(judging),
           "guard_table_judging": [{"condition": c, "guard": g, **dict(n)} for (c, g), n in sorted(table.items())],
           "failed_on_judging": failed_judging,
           "starvation_floor_fails": starvation_fails,
           "named_oracle_runs": {name: [f for f in starvation_fails if f["run"].startswith(f"{name}/oracle")]
                                 for name in NAMED_ORACLE},
           "unread_waits_past_15s": findings,
           "line_availability": lines, "unavailable_lines": unavailable,
           "unavailable_as_expected": as_expected, "expected_unavailable": EXPECTED_UNAVAILABLE,
           "reopens": bool(reopened), "reopened_by": reopened, "settled": settled,
           "waits": waits}
    (pathlib.Path(__file__).parent / "starvation.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(f"{len(waits)} runs; {len(failed_judging)} failed guard rows on the judging files; "
          f"{len(starvation_fails)} starvation_floor fails ({sum(f['judging'] for f in starvation_fails)} on judging); "
          f"{len(findings)} unread waits past 15 s ({sum(f['judging'] for f in findings)} on judging); "
          f"{'REOPENS' if reopened else 'nothing reopened'}; {len(settled)} on judging under the settled 100 ms point")
    print(f"{len(lines)} line readings; unavailable: {[l['line'] for l in unavailable] or 'none'} "
          f"({'as expected' if as_expected else 'NOT as expected: ' + ', '.join(EXPECTED_UNAVAILABLE) + ' expected'})")
    for l in unavailable:
        for f in l["failed"]:
            print(f"  {l['line']}: {f[2]} on {f[0]} · {f[1]}")
    for f in starvation_fails:
        print(f"  starvation_floor fail: {f['run']} {f['reason']}")
    for f in findings:
        print(f"  {f['kind']} {f['wait_us'] / 1e6:.1f} s {f['run']} task {f['task']}: {f['leads_to']}")


if __name__ == "__main__":
    main()
