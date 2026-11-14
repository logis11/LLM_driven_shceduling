"""The end stages read a run's aggregates a run at a time (harness changelog, 2026-11-15): the runner before the
change and after write the same experiment files byte for byte — aggregates, scores, guards, grades, report — on
the integration gate's short run's seven files through the real programs, the smoke spec with the cap band's
`floor-0.2` table pinned and the evaluator's lines that read the aggregates added (the floor band is already there;
the input wake count, the longest wait, the flip cost).

    python3 _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/end_stage_check.py --old OLD --work WORK

OLD is the harness tree of the commit before the change (`git archive <commit> harness | tar -x -C OLD`), WORK an
empty directory for the two experiments and their shared execution cache. Run from the repository root; writes
end-stage-check.json beside this file and prints its summary."""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import time

import yaml

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness.runner import load_machine, write_smoke_spec  # noqa: E402

FILES = ["c1-office", "c1-photo", "c7-mail", "c2-p2b", "c1-gaming", "c7-compile", "c1-compile"]
COMPARED = ("aggregates.csv", "scores.csv", "guards.csv", "grades.csv", "report.json", "report.md")
LINES = [{"type": "input_wake_count"}, {"type": "longest_wait", "threshold_us": 30000000, "reopen_us": 15000000},
         {"type": "flip_cost"}]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    ap.add_argument("--work", required=True)
    args = ap.parse_args()
    old, work = pathlib.Path(args.old).resolve(), pathlib.Path(args.work).resolve()
    machine_doc = yaml.safe_load((REPO / "harness" / "runner.yaml").read_text())
    machines = {}
    for side in ("old", "new"):
        doc = dict(machine_doc, runs_dir=str(work / f"{side}-runs"), cache_dir=str(work / "cache"))
        machines[side] = work / f"{side}-machine.yaml"
        machines[side].write_text(yaml.safe_dump(doc))
    spec = write_smoke_spec(work / "spec.yaml", load_machine(machines["new"], REPO), REPO, only=FILES)
    doc = yaml.safe_load(spec.read_text())
    gate = yaml.safe_load((REPO / "harness" / "experiments" / "rq0-gate.yaml").read_text())
    doc["pins"]["driver_table_alternatives"] = {"floor-0.2": gate["pins"]["driver_table_alternatives"]["floor-0.2"]}
    doc["reporting_lines"] += LINES
    spec.write_text(yaml.safe_dump(doc, sort_keys=False))
    seconds = {}
    for side, tools in (("old", old / "tools"), ("new", REPO / "harness" / "tools")):
        t0 = time.time()
        proc = subprocess.run([sys.executable, str(tools / "run.py"), "--spec", str(spec), "--machine",
                               str(machines[side]), "--root", str(REPO), "--quiet"], capture_output=True, text=True)
        seconds[side] = round(time.time() - t0, 1)
        if proc.returncode not in (0, 2):         # 2: a verdict other than pass, the experiment's files written
            sys.exit(f"{side}: run.py exited {proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    exp = {side: work / f"{side}-runs" / doc["experiment"] for side in ("old", "new")}
    files = {name: {"identical": (exp["old"] / name).read_bytes() == (exp["new"] / name).read_bytes(),
                    "sha256": sha(exp["new"] / name), "bytes": (exp["new"] / name).stat().st_size}
             for name in COMPARED}
    report = json.loads((exp["new"] / "report.json").read_text())
    out = {"files": FILES, "experiment": doc["experiment"], "seconds": seconds,
           "lines": [line["type"] for line in report["lines"]], "compared": files,
           "identical": all(f["identical"] for f in files.values())}
    (pathlib.Path(__file__).parent / "end-stage-check.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"{'identical' if out['identical'] else 'DIFFERS'}: {', '.join(n for n in COMPARED)}; "
          f"old {seconds['old']} s, new {seconds['new']} s; lines {out['lines']}")
    for name, f in files.items():
        if not f["identical"]:
            print(f"  differs: {name}")
    return 0 if out["identical"] else 1


if __name__ == "__main__":
    sys.exit(main())
