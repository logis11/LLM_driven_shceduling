"""10.4 decision 3: the integration gate's 28 short-run runs, each run's records rebuilt from its trace with the
harness as it stands and compared byte for byte with the records on disk (records.csv and records-messages.json).

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/rebuild_check.py [--workers N]

Run from the repository root; writes rebuild-check.json beside this file."""
import argparse, concurrent.futures, hashlib, json, pathlib, sys, tempfile, time

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import records  # noqa: E402

EXP = REPO / "runs" / "integration-gate" / "smoke"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def one(entry):
    run_dir = pathlib.Path(entry["records"]).parent
    t0 = time.time()
    rows, messages = records.build(entry["workload"], run_dir / "trace.jsonl", table=entry["table"],
                                   seed=entry["seed"], schedule_path=run_dir / "schedule.json",
                                   boot_default=entry["boot_default"], telemetry=entry["telemetry"])
    with tempfile.TemporaryDirectory() as tmp:
        out = pathlib.Path(tmp) / "records.csv"
        records.write_csv(rows, out)
        rebuilt = out.read_bytes()
    rebuilt_msgs = (json.dumps(messages, indent=1) + "\n").encode()
    on_disk = (run_dir / "records.csv").read_bytes()
    on_disk_msgs = (run_dir / "records-messages.json").read_bytes()
    drops = sum(1 for line in open(run_dir / "trace.jsonl", "rb") if b'"wake_drop"' in line)
    return {"run": f"{run_dir.parent.name}/{run_dir.name}", "wake_drop_lines": drops, "rows": len(rows),
            "records_sha256_on_disk": sha(on_disk), "records_sha256_rebuilt": sha(rebuilt),
            "messages_sha256_on_disk": sha(on_disk_msgs), "messages_sha256_rebuilt": sha(rebuilt_msgs),
            "identical": on_disk == rebuilt and on_disk_msgs == rebuilt_msgs,
            "seconds": round(time.time() - t0, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    runs = json.loads((EXP / "guards-manifest.json").read_text())["runs"]
    with concurrent.futures.ProcessPoolExecutor(args.workers) as pool:
        results = sorted(pool.map(one, runs), key=lambda r: r["run"])
    doc = {"experiment": str(EXP.relative_to(REPO)), "runs": len(results),
           "identical": sum(r["identical"] for r in results), "results": results}
    (pathlib.Path(__file__).parent / "rebuild-check.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(f"{doc['identical']} of {doc['runs']} runs byte-identical")
    for r in results:
        print(f"  {r['run']:40} drops {r['wake_drop_lines']:>7}  {r['seconds']:>7} s  "
              f"{'identical' if r['identical'] else 'DIFFERS'}")
    return 0 if doc["identical"] == doc["runs"] else 1


if __name__ == "__main__":
    sys.exit(main())
