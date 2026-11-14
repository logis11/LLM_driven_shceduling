"""10.4 decision 4's invariant: the runner before the pre-smoke changes and after, on the same files and the real
programs, write the same outputs — the experiment's aggregates, scores, guards, grades and report byte for byte,
and each run's records, schedule, log and trace equal once unpacked, the rerun trace's hash equal to the old rerun
trace's.

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/storage_check.py OLD_EXP NEW_EXP

OLD_EXP and NEW_EXP are the two smoke experiment directories (harness/tools/smoke.py run once from a checkout of
the commit before the change, once from the tree with it). Writes storage-check.json beside this file."""
import gzip, hashlib, json, pathlib, sys

COMPARED = ("aggregates.csv", "scores.csv", "guards.csv", "grades.csv", "report.md")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(old, new):
    old, new = pathlib.Path(old), pathlib.Path(new)
    out = {"experiment_files": {}, "runs": []}
    ok = True
    for name in COMPARED:
        same = (old / name).read_bytes() == (new / name).read_bytes()
        out["experiment_files"][name] = {"sha256": sha((new / name).read_bytes()), "identical": same}
        ok &= same
    ro, rn = json.loads((old / "report.json").read_text()), json.loads((new / "report.json").read_text())
    ro.pop("spec_sha256", None); rn.pop("spec_sha256", None)       # the generated spec names its own temp path
    out["experiment_files"]["report.json"] = {"identical_but_spec_sha256": ro == rn}
    ok &= ro == rn
    for run_dir in sorted(p for p in old.glob("*/*") if p.is_dir()):
        n = new / run_dir.relative_to(old)
        checks = {
            "records": (run_dir / "records.csv").read_bytes() == gzip.decompress((n / "records.csv.gz").read_bytes()),
            "trace": (run_dir / "trace.jsonl").read_bytes() == gzip.decompress((n / "trace.jsonl.gz").read_bytes()),
            "rerun_sha256": sha((run_dir / "trace.rerun.jsonl").read_bytes()) == (n / "trace.rerun.sha256").read_text().strip(),
        }
        for name in ("schedule.json", "log.json", "records-messages.json", "recognition-records.csv"):
            if (run_dir / name).exists() or (n / name).exists():
                checks[name] = (run_dir / name).read_bytes() == (n / name).read_bytes()
        old_bytes = sum(p.stat().st_size for p in run_dir.iterdir())
        new_bytes = sum(p.stat().st_size for p in n.iterdir())
        out["runs"].append({"run": str(run_dir.relative_to(old)), "identical": all(checks.values()),
                            "checks": checks, "run_dir_bytes_old": old_bytes, "run_dir_bytes_new": new_bytes})
        ok &= all(checks.values())
    out["identical"] = ok
    (pathlib.Path(__file__).parent / "storage-check.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"{'identical' if ok else 'DIFFERS'}: {len(out['runs'])} runs, "
          f"run directories {sum(r['run_dir_bytes_old'] for r in out['runs'])/2**20:.0f} MB → "
          f"{sum(r['run_dir_bytes_new'] for r in out['runs'])/2**20:.0f} MB")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
