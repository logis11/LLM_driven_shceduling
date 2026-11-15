"""10.4 decisions 12–13: the full run's cost projected from the cold smoke, and whether the cost is carried.

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/project.py --smoke runs/cold-smoke \
        --free-gb FREE [--stages runs/smoke-rerun] [--budget-hours 80] [--machine harness/runner.yaml]

`--stages` names the experiment whose `stage-times.csv` gives the end stages, the smoke's own when left out — the
rerun's, its traces from the execution cache, when the end stages changed after the cold smoke (decision 14); the
runs are always the cold smoke's.

The upper projection (decision 12): for each file, its slowest measured run of any condition stands for every one of
its runs in the full run, and its largest run for their bytes. The wall projection is the longer of the two pools —
the runs on files under `heavy_mb` over `workers` processes, the rest over `heavy_workers` — each pool's run-seconds
divided by its processes, never less than its longest run, plus the smoke's end stages scaled by the run count. The
full run is counted cold: every run executed, all its bytes new. The disk projection adds the experiment's own files
(decision 12 as restated 2026-11-15), from the `--stages` experiment's: `aggregates.csv` by its rows, each full run's
rows its smoke counterpart's (the same run, seed 1 for a drawing run's every seed), the other files by the run
count. The mean projection, each file's mean run in place of its slowest and largest, is printed beside it. The cost
is carried (decision 13) when the upper wall projection is at most the budget and the upper disk projection at most
the free space measured at the smoke's start.

Run from the repository root; writes projection.json beside this file."""
import argparse
import collections
import csv
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import runner  # noqa: E402

SPEC = REPO / "harness" / "experiments" / "rq0-gate.yaml"


def project(per_file, full_counts, heavy, machine, end_seconds, smoke_runs, pick, experiment_bytes):
    pools = {"light": [0.0, 0.0, machine.workers], "heavy": [0.0, 0.0, max(1, machine.heavy_workers)]}
    runs_bytes = 0
    for wid, n in full_counts.items():
        seconds, size = pick(per_file[wid])
        pool = pools["heavy" if heavy[wid] else "light"]
        pool[0] += seconds * n
        pool[1] = max(pool[1], seconds)
        runs_bytes += size * n
    walls = {name: max(total / procs, longest) for name, (total, longest, procs) in pools.items()}
    total_runs = sum(full_counts.values())
    end = end_seconds * total_runs / smoke_runs
    wall = max(walls.values()) + end
    return {"wall_hours": round(wall / 3600, 2), "pools_hours": {k: round(v / 3600, 2) for k, v in walls.items()},
            "end_stages_hours": round(end / 3600, 2), "runs_gb": round(runs_bytes / 1e9, 1),
            "experiment_files_gb": round(experiment_bytes / 1e9, 1),
            "disk_gb": round((runs_bytes + experiment_bytes) / 1e9, 1)}


def experiment_files(stages, full, smoke_runs, full_runs):
    """The full run's own files, from the `stages` experiment's: aggregates.csv by its rows — each full run's rows
    its smoke counterpart's, seed 1 for a drawing run — the others by the run count."""
    rows = collections.Counter()
    with open(stages / "aggregates.csv", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            rows[tuple(r[:6])] += 1
    smoke_rows = sum(rows.values())
    full_rows = 0
    for run in full:
        key = (run.workload_id, run.condition, run.table, "1" if run.seed else "", run.boot_default, run.telemetry)
        if key not in rows:
            sys.exit(f"no smoke counterpart of {run.identity()}")
        full_rows += rows[key]
    agg_bytes = (stages / "aggregates.csv").stat().st_size
    other = sum(p.stat().st_size for p in stages.iterdir() if p.is_file() and p.name != "aggregates.csv")
    return {"smoke_aggregate_rows": smoke_rows, "full_aggregate_rows": full_rows,
            "aggregates_bytes": round(agg_bytes * full_rows / smoke_rows),
            "other_bytes": round(other * full_runs / smoke_runs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", required=True, help="the smoke's experiment directory")
    ap.add_argument("--free-gb", type=float, required=True, help="free space measured at the smoke's start, GB")
    ap.add_argument("--stages", default=None, help="the experiment directory whose stage-times.csv gives the end stages")
    ap.add_argument("--budget-hours", type=float, default=80.0)
    ap.add_argument("--machine", default=str(REPO / "harness" / "runner.yaml"))
    args = ap.parse_args()
    smoke = pathlib.Path(args.smoke)
    stages = pathlib.Path(args.stages) if args.stages else smoke
    machine = runner.load_machine(args.machine, REPO)

    per_file = collections.defaultdict(list)
    with open(smoke / "run-times.csv", newline="") as f:
        for r in csv.DictReader(f):
            per_file[r["workload_id"]].append((float(r["seconds"]), int(r["bytes"])))
    smoke_runs = sum(len(v) for v in per_file.values())
    with open(stages / "stage-times.csv", newline="") as f:
        end_seconds = sum(float(r["seconds"]) for r in csv.DictReader(f) if r["stage"] != "runs")

    full = runner.expand(SPEC, machine, REPO)
    full_counts = collections.Counter(r.workload_id for r in full)
    heavy = {r.workload_id: runner.is_heavy(r, machine) for r in full}
    missing = sorted(set(full_counts) - set(per_file))
    if missing:
        sys.exit(f"no smoke run of {missing}: the projection reads every file")

    files = experiment_files(stages, full, smoke_runs, len(full))
    experiment_bytes = files["aggregates_bytes"] + files["other_bytes"]
    upper = project(per_file, full_counts, heavy, machine, end_seconds, smoke_runs,
                    lambda runs: (max(s for s, _ in runs), max(b for _, b in runs)), experiment_bytes)
    mean = project(per_file, full_counts, heavy, machine, end_seconds, smoke_runs,
                   lambda runs: (sum(s for s, _ in runs) / len(runs), sum(b for _, b in runs) / len(runs)),
                   experiment_bytes)
    carried = upper["wall_hours"] <= args.budget_hours and upper["disk_gb"] <= args.free_gb
    top = sorted(((max(s for s, _ in per_file[w]) * n, w) for w, n in full_counts.items()), reverse=True)[:10]
    doc = {"smoke": str(smoke.resolve().relative_to(REPO)) if smoke.resolve().is_relative_to(REPO) else str(smoke),
           "stages": str(stages), "smoke_runs": smoke_runs, "full_runs": len(full),
           "machine": {"workers": machine.workers, "heavy_workers": machine.heavy_workers,
                       "heavy_mb": machine.heavy_mb},
           "budget_hours": args.budget_hours, "free_gb_at_start": args.free_gb,
           "experiment_files": files, "upper": upper, "mean": mean,
           "carried": carried, "over": [k for k, over in (("wall", upper["wall_hours"] > args.budget_hours),
                                                          ("disk", upper["disk_gb"] > args.free_gb)) if over],
           "largest_files_upper_run_hours": [{"workload_id": w, "hours": round(h / 3600, 2),
                                              "runs": full_counts[w]} for h, w in top]}
    (pathlib.Path(__file__).parent / "projection.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps(doc, indent=1))


if __name__ == "__main__":
    main()
