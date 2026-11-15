#!/usr/bin/env python3
"""The blind reading (10.5 spec, decisions 4 and 5): what is read of a finished RQ0 run before its report is
opened. It reads `guards.csv`, `guards-manifest.json` and the runs' traces; it does not read `report.json`,
`report.md`, `scores.csv`, the runner's verdict line or its exit code.

    python3 _dev/research/jioh/task-10.5-the-rq0-run/blind_reading.py [--experiment-dir runs/rq0-gate] [--workers 6]

1. The guard table on the runs the criterion reads — on each judging file, the primary boot default's `fixed`
   run, the `oracle` run and every `random` seed, under the pinned driver table. A failed guard there that no
   exemption of the RQ0 gate spec covers makes the verdict `invalid` (the 8.7 spec's decision 9).
2. The longest-wait line's reopen condition (the RQ0 gate spec's `sensitivity-lines` statement and its
   `longest_wait` line): a judging file's run whose longest `ready_wait` — the `starvation_floor` guard's value —
   is past the line's `reopen_us`, under every boot default but the ones the line leaves out.
3. `simulator/tools/wait_check.py` on every run's trace, for the waits the guard cannot read — one still open at
   the end, one after a preemption, ended or open. On a run the criterion reads, such a wait over 30 s is handled
   as a failed `starvation_floor` is; past 15 s it reopens the executor-net question with 인경민; on any other
   run it is recorded with the run.

The reading is clear when 1 finds no failure, 2 no run, and 3 no wait past 15 s on a run the criterion reads.
Every failed guard row outside the criterion's runs is counted and listed, exempt or not, for the record.

Run from the repository root. Writes, into the record folder (`run/` beside this file), `blind-reading.json`
and `waits.csv` (every run's four wait readings), and prints the summary."""
import argparse
import collections
import concurrent.futures
import csv
import gzip
import json
import pathlib
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "harness" / "tools"))
sys.path.insert(0, str(REPO / "simulator" / "tools"))
from harness import evaluator, manifests  # noqa: E402
import wait_check  # noqa: E402

NET_US, QUESTION_US = 30_000_000, 15_000_000
UNREAD = ("ready_open", "preempt_done", "preempt_open")
KINDS = ("ready_done",) + UNREAD


def run_name(r):
    return (f"{r['workload_id']}/{r['condition']}" + (f"-{r['seed']}" if r["seed"] else "")
            + (f"+{r['boot_default']}" if r["boot_default"] else "")
            + (f"@{r['table'].partition('@')[2]}" if "@" in r["table"] else "") + f"~{r['telemetry']}")


def check(entry):
    with gzip.open(entry["trace"], "rb") as f:
        r = wait_check.waits(f, wait_check.t_end_of(entry["workload"]))
    out = {k: entry[k] for k in ("workload_id", "condition", "table", "seed", "boot_default", "telemetry")}
    for kind in KINDS:
        out[f"{kind}_us"], out[f"{kind}_task"] = r[kind][0], r[kind][1]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--experiment-dir", default="runs/rq0-gate")
    ap.add_argument("--spec", default="harness/experiments/rq0-gate.yaml")
    ap.add_argument("--record", default=str(HERE / "run"))
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    exp, record = (REPO / args.experiment_dir).resolve(), (REPO / args.record).resolve()
    record.mkdir(parents=True, exist_ok=True)
    spec, _paths, _axes = manifests.expand(evaluator.load_spec(REPO / args.spec), REPO)
    judging = set(spec["files"]["judging"])
    wait_line = next(line for line in spec["reporting_lines"] if line["type"] == "longest_wait")
    reopen_us = int(wait_line["reopen_us"])
    left_out = set(wait_line.get("reopen_excluded_boot_defaults", []))

    def criterion_run(r):
        return r["workload_id"] in judging and r["boot_default"] == "" and "@" not in r["table"]

    # 1 and 2: the guard table
    criterion_table = collections.defaultdict(collections.Counter)
    invalidating, reopening, other_failed = [], [], []
    criterion_runs = set()
    with open(exp / "guards.csv", newline="") as f:
        for r in csv.DictReader(f):
            on_criterion = criterion_run(r)
            if on_criterion:
                criterion_runs.add(run_name(r))
                criterion_table[(r["condition"], r["guard"])][r["result"]] += 1
            if r["result"] == "fail":
                reason = evaluator._exempt(spec, r)
                row = {"run": run_name(r), "guard": r["guard"], "value": r["value"], "threshold": r["threshold"],
                       "reason": r["reason"], "exempt": reason is not None}
                if on_criterion and reason is None:
                    invalidating.append(row)
                else:
                    other_failed.append({**row, "criterion_run": on_criterion, "judging": r["workload_id"] in judging})
            if (r["guard"] == "starvation_floor" and r["value"] and r["workload_id"] in judging
                    and r["boot_default"] not in left_out and float(r["value"]) > reopen_us):
                reopening.append({"run": run_name(r), "longest_ready_wait_us": float(r["value"]),
                                  "criterion_run": on_criterion})

    # 3: the wait check on every trace
    runs = json.loads((exp / "guards-manifest.json").read_text())["runs"]
    t0, waits = time.time(), []
    with concurrent.futures.ProcessPoolExecutor(args.workers) as pool:
        for k, w in enumerate(pool.map(check, runs, chunksize=4), 1):
            waits.append(w)
            if k % 1000 == 0:
                print(f"  wait check: {k}/{len(runs)} traces, {time.time() - t0:.0f} s", file=sys.stderr, flush=True)
    waits.sort(key=run_name)
    with open(record / "waits.csv", "w", newline="") as f:
        out = csv.DictWriter(f, fieldnames=list(waits[0]), lineterminator="\n")
        out.writeheader()
        out.writerows(waits)
    unread = []
    for w in waits:
        on_criterion = criterion_run(w)
        for kind in UNREAD:
            us = w[f"{kind}_us"]
            if us <= QUESTION_US:
                continue
            if on_criterion:
                leads_to = ("handled as a failed starvation_floor" if us > NET_US
                            else "reopens the executor-net question with 인경민")
            else:
                leads_to = "recorded with its run"
            unread.append({"run": run_name(w), "kind": kind, "wait_us": us, "task": w[f"{kind}_task"],
                           "criterion_run": on_criterion, "judging": w["workload_id"] in judging,
                           "leads_to": leads_to})
    unread_criterion = [u for u in unread if u["criterion_run"]]

    clear = not invalidating and not reopening and not unread_criterion
    other_counts = collections.Counter((o["guard"], "exempt" if o["exempt"] else "not exempt") for o in other_failed)
    doc = {"experiment_dir": str(exp), "read": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "runs": len(runs),
           "criterion_runs": len(criterion_runs), "clear": clear,
           "guard_table_criterion_runs": [{"condition": c, "guard": g, **dict(n)}
                                          for (c, g), n in sorted(criterion_table.items())],
           "invalidating": invalidating,
           "reopen_us": reopen_us, "reopen_left_out": sorted(left_out), "reopening": reopening,
           "unread_waits_past_15s": unread,
           "other_failed_guard_rows": {"counts": [{"guard": g, "exempt": e, "rows": n}
                                                  for (g, e), n in sorted(other_counts.items())],
                                       "rows": other_failed},
           "wait_check_seconds": round(time.time() - t0, 1)}
    (record / "blind-reading.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")

    print(f"{len(runs)} runs, {len(criterion_runs)} the criterion reads; "
          f"{'CLEAR' if clear else 'NOT CLEAR'}: {len(invalidating)} invalidating guard failure(s), "
          f"{len(reopening)} run(s) past the reopen point, {len(unread_criterion)} unread wait(s) past 15 s on the "
          f"criterion's runs; {len(unread) - len(unread_criterion)} unread wait(s) past 15 s on other runs, "
          f"{len(other_failed)} failed guard row(s) outside the criterion's runs or exempt")
    for row in invalidating:
        print(f"  INVALIDATING {row['guard']} on {row['run']}: {row['reason']}")
    for row in reopening:
        print(f"  REOPENS {row['run']}: longest ready_wait {row['longest_ready_wait_us'] / 1e6:.1f} s")
    for u in unread:
        print(f"  {u['kind']} {u['wait_us'] / 1e6:.1f} s {u['run']} task {u['task']}: {u['leads_to']}")
    for (g, e), n in sorted(other_counts.items()):
        print(f"  outside the criterion's runs or exempt: {g}, {e}: {n} row(s)")
    return 0 if clear else 1


if __name__ == "__main__":
    sys.exit(main())
