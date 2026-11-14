"""The per-switch excess's boost-window check (harness changelog, 2026-11-14): every run of the first cold smoke
whose results the cache holds and whose aggregates carry a per-switch excess, its results built again from its
trace with the harness as it stands — records, records messages, aggregates and graded queries — and compared
exactly with the ones the harness before the change built and cached.

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/excess_check.py --smoke runs/cold-smoke \
        --cache runs/.cache [--workers N]

Run from the repository root; writes excess-check.json beside this file and prints its summary."""
import argparse
import concurrent.futures
import gzip
import json
import pathlib
import pickle
import shutil
import sys
import tempfile
import time
import types

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import evaluator, manifests, scoring  # noqa: E402
from harness.runner import _build_results, expand, load_machine, write_seed_copy  # noqa: E402

SPEC = REPO / "harness" / "experiments" / "rq0-gate.yaml"
MACHINE = REPO / "harness" / "runner.yaml"
EXCESS = ("excess_switch", "excess_boost")
_CTX = None


def context(spec_path, machine):
    spec = evaluator.load_spec(spec_path)
    pins = spec["pins"]
    _s, _paths, axes = manifests.expand(spec, REPO)
    scoring_spec = scoring.with_variants(scoring.load_spec(REPO / pins["scoring_spec"]["path"]),
                                         {wid: machine.build_dir / f"{wid}.workload.json"
                                          for wid in (spec["files"].get("variants") or [])})
    by_set = {}
    for wid, (set_name, _record) in axes.items():
        by_set.setdefault(set_name, set()).add(wid)
    for set_name, wids in sorted(by_set.items()):
        scoring_spec = scoring.with_generated(scoring_spec, manifests.load(REPO / pins["generated"][set_name]["path"]),
                                              only=wids)
    return types.SimpleNamespace(scoring_spec=scoring_spec, table_path=REPO / pins["driver_table"]["path"])


def init(ctx):
    global _CTX
    _CTX = ctx


def check(job):
    run, run_dir, entry = job
    old = pickle.loads((entry / "result.pickle").read_bytes())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        (tmp / "trace.jsonl").write_bytes(gzip.decompress((run_dir / "trace.jsonl.gz").read_bytes()))
        for name in ("schedule.json", "log.json"):
            if (run_dir / name).exists():
                shutil.copy(run_dir / name, tmp / name)
        t0 = time.time()
        new = _build_results(run, _CTX, tmp, run.table_file or _CTX.table_path)
        seconds = round(time.time() - t0, 1)
        records_same = gzip.decompress((tmp / "records.csv.gz").read_bytes()) == \
            gzip.decompress((entry / "records.csv.gz").read_bytes())
    checks = {"records": records_same, **{k: new[k] == old[k] for k in ("aggregates", "messages", "grade_rows")}}
    return {"run": f"{run.workload_id}/{run.name}", "identical": all(checks.values()), "checks": checks,
            "excess_rows": sum(r["aggregate"] in EXCESS for r in old["aggregates"]), "seconds": seconds}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    smoke, cache = pathlib.Path(args.smoke), pathlib.Path(args.cache)
    machine = load_machine(MACHINE, REPO)
    with tempfile.TemporaryDirectory() as tmp:
        spec_path = write_seed_copy(SPEC, pathlib.Path(tmp) / "spec.yaml", 2, smoke.name, machine, REPO)
        runs = {(r.workload_id, r.name): r for r in expand(spec_path, machine, REPO)}
        ctx = context(spec_path, machine)
    jobs = []
    for entry in sorted(p for p in (cache / "results").iterdir() if (p / "result.pickle").exists()):
        old = pickle.loads((entry / "result.pickle").read_bytes())
        if not any(r["aggregate"] in EXCESS for r in old["aggregates"]):
            continue
        ident = old["aggregates"][0]
        run = next(r for (wid, _n), r in runs.items()
                   if (wid, r.condition, r.table, r.seed, r.boot_default, r.telemetry)
                   == tuple(ident[k] for k in ("workload_id", "condition", "table", "seed", "boot_default", "telemetry")))
        jobs.append((run, smoke / run.workload_id / run.name, entry))
    out = []
    heavy = lambda job: job[0].workload_file.stat().st_size >= machine.heavy_mb * (1 << 20)   # noqa: E731
    for n, part in ((args.workers, [j for j in jobs if not heavy(j)]), (machine.heavy_workers, [j for j in jobs if heavy(j)])):
        with concurrent.futures.ProcessPoolExecutor(n, initializer=init, initargs=(ctx,)) as pool:
            out += pool.map(check, part)
    out.sort(key=lambda r: r["run"])
    doc = {"smoke": str(smoke), "runs": len(out), "identical": all(r["identical"] for r in out), "results": out}
    (pathlib.Path(__file__).parent / "excess-check.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(f"{'identical' if doc['identical'] else 'DIFFERS'}: {len(out)} runs with a per-switch excess, "
          f"{sum(r['excess_rows'] for r in out)} excess rows")
    for r in out:
        if not r["identical"]:
            print(f"  differs: {r['run']} {r['checks']}")
    return 0 if doc["identical"] else 1


if __name__ == "__main__":
    sys.exit(main())
