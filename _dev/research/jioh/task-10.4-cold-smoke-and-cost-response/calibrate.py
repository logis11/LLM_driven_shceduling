"""10.4 decision 7: the memory calibration — one run of each heavy family and of the largest light files, one
after another, each in a fresh process, on the real programs, in a runs and cache directory of its own (the
smoke's cache stays empty). Each run's wall time, peak resident memory and bytes come from the runner itself
(`process_run`), so the figures are the ones `run-times.csv` will carry in the smoke.

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/calibrate.py --scratch DIR [FILE ...]

Run from the repository root; writes calibration.json beside this file."""
import argparse, concurrent.futures, json, multiprocessing, pathlib, sys, tempfile, time

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import evaluator, manifests, runner, scoring  # noqa: E402

# the heavy families (workload files of 50 MB or more) and the largest light files, by the seed-count-2 copy's
# file sizes (2026-11-14): one run each, `fixed` under the primary boot default
FILES = ["c1-transcode", "c7-transcode", "c4-compile", "c1-compile", "c1-ml-train", "c7-ml-train", "c3-workday",
         "c6-dual"]                                    # c6-dual last: its records outgrow the machine and swap


def context(spec_path, machine):
    """The RunContext run_experiment builds, for one spec."""
    spec = evaluator.load_spec(spec_path)
    pins = spec["pins"]
    spec, _paths, axes = manifests.expand(spec, REPO)
    scoring_spec = scoring.with_variants(scoring.load_spec(REPO / pins["scoring_spec"]["path"]),
                                         {w: machine.build_dir / f"{w}.workload.json"
                                          for w in (spec["files"].get("variants") or [])})
    return runner.RunContext(machine=machine, exp_dir=machine.runs_dir / spec["experiment"],
                             table_path=REPO / pins["driver_table"]["path"], scoring_spec=scoring_spec,
                             harness=runner.harness_version())


def one(run, ctx):
    return runner.process_run(run, ctx)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, help="runs and cache directory of the calibration's own")
    ap.add_argument("files", nargs="*", default=FILES)
    args = ap.parse_args()
    scratch = pathlib.Path(args.scratch).resolve()
    machine = runner.load_machine(REPO / "harness" / "runner.yaml", REPO)
    import dataclasses
    machine = dataclasses.replace(machine, runs_dir=scratch / "runs", cache_dir=scratch / "cache", workers=1)
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        spec = runner.write_seed_copy(REPO / "harness" / "experiments" / "rq0-gate.yaml",
                                      pathlib.Path(tmp) / "spec.yaml", 2, "calibration", machine, REPO)
        ctx = context(spec, machine)
        runs = runner.expand(spec, machine, REPO)
        for wid in args.files:
            run = next(r for r in runs if r.workload_id == wid and r.condition == "fixed" and not r.boot_default)
            spawn = multiprocessing.get_context("spawn")
            with concurrent.futures.ProcessPoolExecutor(1, mp_context=spawn) as pool:
                res = pool.submit(one, run, ctx).result()
            if "failure" in res:
                print(f"{wid}: FAILED {res['failure']}", flush=True)
                out.append({"workload_id": wid, "run": run.name, "failure": res["failure"]})
                continue
            row = {"workload_id": wid, "run": run.name, "workload_mb": round(run.workload_file.stat().st_size / 2**20, 1),
                   "seconds": res["seconds"], "peak_rss_mb": round(res["peak_rss"] / 2**20), "bytes": res["bytes"]}
            out.append(row)
            print(json.dumps(row), flush=True)
    doc = {"date": time.strftime("%Y-%m-%d"), "machine": "home M1 Pro, 16 GB",
           "simulator": machine.simulator.version, "daemon": machine.daemon.version, "runs": out}
    (pathlib.Path(__file__).parent / "calibration.json").write_text(json.dumps(doc, indent=1) + "\n")


if __name__ == "__main__":
    main()
