#!/usr/bin/env python3
"""The resume exercised before the run (10.5 spec, decision 9): the integration gate's short run — seven files,
28 runs, the real programs — once uninterrupted and once killed midway and resumed, both through the launcher
(`rq0_run.py`), each on an empty cache of its own; the two experiments' outputs compared byte for byte.

    python3 _dev/research/jioh/task-10.5-the-rq0-run/resume_check.py --work WORK [--kill-after 10]

WORK is an empty directory for the two passes. The kill is SIGKILL to the launcher and to the runner's whole
process group once `--kill-after` runs have finished: nothing gets to write a stop. Compared: the experiment's
aggregates, scores, guards, grades and report, and every run's records, trace, rerun-trace hash, schedule, log
and records messages. Run from the repository root; writes resume-check.json beside this file and prints its
summary."""
import argparse
import hashlib
import json
import os
import pathlib
import re
import signal
import subprocess
import sys
import time

import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness.runner import load_machine, write_smoke_spec  # noqa: E402

FILES = ["c1-office", "c1-photo", "c7-mail", "c2-p2b", "c1-gaming", "c7-compile", "c1-compile"]
EXPERIMENT_FILES = ("aggregates.csv", "scores.csv", "guards.csv", "grades.csv", "report.json", "report.md")
RUN_FILES = ("records.csv.gz", "trace.jsonl.gz", "trace.rerun.sha256", "schedule.json", "log.json",
             "records-messages.json")
LINE = re.compile(r"^\[(\d+)/(\d+)\] ([^/ ]+)/(\S+) (.*)$")
LAUNCHER = HERE / "rq0_run.py"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def progress(log):
    if not log.exists():
        return []
    return [m for m in map(LINE.match, log.read_text(errors="replace").splitlines()) if m]


def launcher(command, spec, machine, record):
    return [sys.executable, str(LAUNCHER), command, "--spec", str(spec), "--machine", str(machine),
            "--record", str(record), "--min-free-gb", "0"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--work", required=True)
    ap.add_argument("--kill-after", type=int, default=10)
    args = ap.parse_args()
    work = pathlib.Path(args.work).resolve()
    if any(work.iterdir()):
        sys.exit(f"{work} is not empty")
    machine_doc = yaml.safe_load((REPO / "harness" / "runner.yaml").read_text())
    machine, record, runs = {}, {}, {}
    for side in ("whole", "resumed"):
        runs[side] = work / f"{side}-runs"
        doc = dict(machine_doc, runs_dir=str(runs[side]), cache_dir=str(work / f"{side}-cache"))
        machine[side] = work / f"{side}-machine.yaml"
        machine[side].write_text(yaml.safe_dump(doc))
        record[side] = work / f"{side}-record"
    spec = write_smoke_spec(work / "spec.yaml", load_machine(machine["whole"], REPO), REPO, only=FILES)
    experiment = yaml.safe_load(spec.read_text())["experiment"]
    seconds = {}

    # the uninterrupted pass
    t0 = time.time()
    proc = subprocess.run(launcher("start", spec, machine["whole"], record["whole"]), cwd=REPO,
                          capture_output=True, text=True)
    seconds["whole"] = round(time.time() - t0, 1)
    if proc.returncode != 0:
        sys.exit(f"the uninterrupted pass: the launcher exited {proc.returncode}\n{proc.stdout[-2000:]}\n{proc.stderr}")

    # the pass killed midway
    log = runs["resumed"] / f"{experiment}.log"
    t0 = time.time()
    first = subprocess.Popen(launcher("start", spec, machine["resumed"], record["resumed"]), cwd=REPO,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    while len(progress(log)) < args.kill_after:
        if first.poll() is not None:
            sys.exit(f"the pass to be killed ended by itself (exit {first.returncode}) before "
                     f"{args.kill_after} runs finished")
        time.sleep(0.2)
    runner_pids = subprocess.run(["pgrep", "-f", f"run.py --spec {spec}"], capture_output=True,
                                 text=True).stdout.split()
    groups = sorted({os.getpgid(int(p)) for p in runner_pids})
    os.kill(first.pid, signal.SIGKILL)
    for g in groups:
        try:
            os.killpg(g, signal.SIGKILL)
        except ProcessLookupError:
            pass
    first.wait()
    time.sleep(2)
    at_kill = progress(log)
    total = int(at_kill[-1].group(2))
    seconds["to_the_kill"] = round(time.time() - t0, 1)
    stray = sorted(p.name for p in (work / "resumed-cache").rglob(".tmp-*") if p.is_dir())
    stops_before = (record["resumed"] / "stops.jsonl").exists()

    # the resume
    t0 = time.time()
    proc = subprocess.run(launcher("resume", spec, machine["resumed"], record["resumed"]), cwd=REPO,
                          capture_output=True, text=True)
    seconds["resume"] = round(time.time() - t0, 1)
    if proc.returncode != 0:
        sys.exit(f"the resume: the launcher exited {proc.returncode}\n{proc.stdout[-2000:]}\n{proc.stderr}")
    after = progress(log)[len(at_kill):]
    served = sum("records from the cache" in m.group(5) for m in after)

    # the comparison
    exp = {side: runs[side] / experiment for side in runs}
    sealed = {side: all(((exp[side] / n).stat().st_mode & 0o777) == 0 for n in ("report.json", "report.md", "scores.csv"))
              for side in exp}
    for side in exp:                                    # the launcher sealed them; the smoke spec's verdict is a
        for name in ("report.json", "report.md", "scores.csv"):      # placeholder criterion's, read by nobody
            (exp[side] / name).chmod(0o644)
    compared, differing = {}, []
    for name in EXPERIMENT_FILES:
        a, b = sha(exp["whole"] / name), sha(exp["resumed"] / name)
        compared[name] = {"identical": a == b, "sha256": a, "bytes": (exp["whole"] / name).stat().st_size}
        if a != b:
            differing.append(name)
    run_dirs = sorted(str(p.parent.relative_to(exp["whole"])) for p in exp["whole"].glob("*/*/schedule.json"))
    run_files = 0
    for rel in run_dirs:
        for name in RUN_FILES:
            a, b = exp["whole"] / rel / name, exp["resumed"] / rel / name
            if a.exists() != b.exists() or (a.exists() and sha(a) != sha(b)):
                differing.append(f"{rel}/{name}")
            run_files += a.exists()
    other = sorted(str(p.parent.relative_to(exp["resumed"])) for p in exp["resumed"].glob("*/*/schedule.json"))
    if other != run_dirs:
        differing.append("the two experiments' run directories differ")
    stops = [json.loads(x) for x in (record["resumed"] / "stops.jsonl").read_text().splitlines()]
    out = {"files": FILES, "experiment": experiment, "runs": total, "kill_after": args.kill_after,
           "finished_at_the_kill": len(at_kill), "stop_recorded_at_the_kill": stops_before,
           "stray_tmp_entries_after_the_kill": stray,
           "resume": {"progress_lines": len(after), "records_from_the_results_cache": served,
                      "records_built": len(after) - served},
           "stops_recorded": [s["cause"] for s in stops], "sealed_at_the_end": sealed,
           "seconds": seconds, "experiment_files": compared, "run_directories": len(run_dirs),
           "run_files_compared": run_files, "differing": differing, "identical": not differing}
    (HERE / "resume-check.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{'identical' if out['identical'] else 'DIFFERS'}: {len(EXPERIMENT_FILES)} experiment files and "
          f"{run_files} run files over {len(run_dirs)} runs; killed at {len(at_kill)} of {total} runs, "
          f"{len(stray)} stray temporary entries; the resume served {served} runs' records from the results cache "
          f"and built {len(after) - served}; {seconds}")
    for name in differing:
        print(f"  differs: {name}")
    return 0 if out["identical"] else 1


if __name__ == "__main__":
    sys.exit(main())
