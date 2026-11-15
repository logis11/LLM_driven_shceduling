#!/usr/bin/env python3
"""The RQ0 run's launcher (10.5 spec, decisions 2, 4, 7, 8, 10, 11): the RQ0 gate spec's full matrix through
`harness/tools/run.py` on the machine configuration's real programs. Run from the repository root, in a terminal
on the home machine:

    python3 _dev/research/jioh/task-10.5-the-rq0-run/rq0_run.py start
    python3 _dev/research/jioh/task-10.5-the-rq0-run/rq0_run.py resume
    python3 _dev/research/jioh/task-10.5-the-rq0-run/rq0_run.py open [--settled NOTE]

`start` begins the run and refuses when a start is on record, when the experiment's directory or the cache
exists (decision 2: the run is cold), when the harness, simulator, daemon or dataset trees hold an uncommitted
change, or with less free space than `--min-free-gb` (273.5, the 10.4 record's upper disk projection).

`resume` starts a stopped run again from its own caches (decision 8) and refuses unless the commit, the spec's
hash, the machine configuration's hash and both program versions equal the first start's.

While the run goes, the runner's progress lines are written to `runs/<experiment>.log` and echoed. At the first
failed run the runner is stopped (decision 10). A run that takes more than `SLOW_MULTIPLE` times its file's
slowest run in the second cold smoke is flagged — time alone — in `flags.jsonl` (decision 11).

The verdict stays unread (decision 4): the runner's standard output, which carries the verdict line, and its
exit code go to `runs/<experiment>.sealed/` and are never echoed; when the experiment finishes, those two files
and the experiment's `report.json`, `report.md` and `scores.csv` are set unreadable. `open` makes them readable
again and prints the verdict line — only once `blind_reading.py` has written `blind-reading.json`, and, when
that reading is not clear, only with `--settled` naming where what it found was settled.

Every start, stop, flag and opening is a line in the record folder (`run/` beside this file): `starts.jsonl`
(time, kind, commit, hashes, versions, workers, free space, the memory free percentage and the swap in use),
`stops.jsonl` (time, cause, runs finished), `flags.jsonl`, `opens.jsonl`."""
import argparse
import csv
import hashlib
import json
import os
import pathlib
import re
import shutil
import signal
import subprocess
import sys
import time

import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
SMOKE_TIMES = REPO / "_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/second-smoke/run-times.csv"
# The largest ratio between one run's slowest and fastest time over the three smoke passes that built it (the
# second cold smoke, the rerun, the second rerun; the 10.4 record's three run-times.csv): 6.0.
SLOW_MULTIPLE = 6.0
SEALED = ("report.json", "report.md", "scores.csv")
LINE = re.compile(r"^\[(\d+)/(\d+)\] ([^/ ]+)/(\S+) (.*)$")
BUILT = re.compile(r"in (\d+) s$")
TRACKED = ("harness", "simulator", "daemon", "dataset")


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def sh(*argv):
    return subprocess.run(argv, capture_output=True, text=True, cwd=REPO).stdout.strip()


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def append(path, doc):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")


def lines_of(path):
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


class Run:
    def __init__(self, args):
        self.spec = (REPO / args.spec).resolve()
        self.machine = (REPO / args.machine).resolve()
        self.record = (REPO / args.record).resolve()
        self.min_free_gb = args.min_free_gb
        self.smoke_times = (REPO / args.smoke_times).resolve()
        m = yaml.safe_load(self.machine.read_text())
        self.machine_doc = m
        runs_dir = pathlib.Path(m["runs_dir"])
        self.runs_dir = runs_dir if runs_dir.is_absolute() else REPO / runs_dir
        cache = pathlib.Path(m["cache_dir"])
        self.cache_dir = cache if cache.is_absolute() else REPO / cache
        self.experiment = yaml.safe_load(self.spec.read_text())["experiment"]
        self.exp_dir = self.runs_dir / self.experiment
        self.log = self.runs_dir / f"{self.experiment}.log"
        self.sealed_dir = self.runs_dir / f"{self.experiment}.sealed"
        self.pidfile = self.record / "running.pid"

    # ---------------------------------------------------------------- what a start is held to
    def identity(self):
        m = self.machine_doc
        return {"commit": sh("git", "rev-parse", "HEAD"), "spec_sha256": sha(self.spec),
                "machine_sha256": sha(self.machine), "simulator": m["simulator"]["version"],
                "daemon": m["daemon"]["version"]}

    def free_gb(self):
        probe = self.runs_dir if self.runs_dir.exists() else self.runs_dir.parent
        return round(shutil.disk_usage(probe).free / 1e9, 1)

    def start_doc(self, kind):
        m = self.machine_doc
        pressure = sh("memory_pressure").splitlines()
        return {"started": now(), "kind": kind, **self.identity(),
                "workers": m.get("workers", 1), "heavy_workers": m.get("heavy_workers", 1),
                "heavy_mb": m.get("heavy_mb", 50), "free_gb": self.free_gb(),
                "memory_free": pressure[-1] if pressure else "", "swap": sh("sysctl", "-n", "vm.swapusage")}

    def finished_runs(self):
        """The runs the log's progress lines name as finished and not failed, each once."""
        done = set()
        if self.log.exists():
            for line in self.log.read_text(errors="replace").splitlines():
                m = LINE.match(line)
                if m and not m.group(5).startswith("FAILED"):
                    done.add((m.group(3), m.group(4)))
        return len(done)

    def refuse_if_running(self):
        if self.pidfile.exists():
            pid = int(self.pidfile.read_text())
            try:
                os.kill(pid, 0)
            except OSError:
                self.pidfile.unlink()
            else:
                sys.exit(f"refused: a launcher is running (pid {pid})")

    # ---------------------------------------------------------------- start, resume
    def start(self):
        self.refuse_if_running()
        if (self.record / "starts.jsonl").exists():
            sys.exit(f"refused: {self.record / 'starts.jsonl'} holds a start; `resume` continues that run")
        for path in (self.exp_dir, self.cache_dir, self.sealed_dir):
            if path.exists():
                sys.exit(f"refused: {path} exists; the run is cold")
        dirty = sh("git", "status", "--porcelain", "--", *TRACKED)
        if dirty:
            sys.exit(f"refused: uncommitted changes under {', '.join(TRACKED)}:\n{dirty}")
        free = self.free_gb()
        if free < self.min_free_gb:
            sys.exit(f"refused: {free} GB free, under {self.min_free_gb} GB")
        self.record.mkdir(parents=True, exist_ok=True)
        return self.go("start")

    def resume(self):
        self.refuse_if_running()
        starts = lines_of(self.record / "starts.jsonl")
        if not starts:
            sys.exit(f"refused: no start on record in {self.record}")
        first, here = starts[0], self.identity()
        differs = [f"{k}: {first[k]} at the first start, {here[k]} now" for k in here if first[k] != here[k]]
        if differs:
            sys.exit("refused: not the same run —\n  " + "\n  ".join(differs))
        dirty = sh("git", "status", "--porcelain", "--", *TRACKED)
        if dirty:
            sys.exit(f"refused: uncommitted changes under {', '.join(TRACKED)}:\n{dirty}")
        if len(lines_of(self.record / "stops.jsonl")) < len(starts):     # the last start left no stop: the
            append(self.record / "stops.jsonl",                           # launcher itself was stopped
                   {"stopped": now(), "cause": "no stop was recorded: the launcher did not end by itself; "
                    "cause unknown, recorded at the resume", "runs_finished": self.finished_runs()})
        return self.go("resume")

    # ---------------------------------------------------------------- the run
    def slowest(self):
        slow = {}
        if self.smoke_times.exists():
            with open(self.smoke_times, newline="") as f:
                for r in csv.DictReader(f):
                    slow[r["workload_id"]] = max(slow.get(r["workload_id"], 0.0), float(r["seconds"]))
        return slow

    def unseal(self):
        for path in [self.exp_dir / n for n in SEALED] + [self.sealed_dir / "stdout.txt", self.sealed_dir / "exit-code"]:
            if path.exists():
                path.chmod(0o644)

    def seal(self):
        for path in [self.exp_dir / n for n in SEALED] + [self.sealed_dir / "stdout.txt", self.sealed_dir / "exit-code"]:
            if path.exists():
                path.chmod(0o000)

    def go(self, kind):
        append(self.record / "starts.jsonl", self.start_doc(kind))
        self.pidfile.write_text(str(os.getpid()))
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.sealed_dir.mkdir(exist_ok=True)
        self.unseal()
        slow = self.slowest()
        argv = [sys.executable, str(REPO / "harness/tools/run.py"), "--spec", str(self.spec),
                "--machine", str(self.machine), "--root", str(REPO)]
        if shutil.which("caffeinate"):
            argv = ["caffeinate", "-i", "-s"] + argv          # no idle or system sleep while the runner lives
        sealed_out = open(self.sealed_dir / "stdout.txt", "a")
        proc = subprocess.Popen(argv, cwd=REPO, stdout=sealed_out, stderr=subprocess.PIPE, text=True,
                                errors="replace", start_new_session=True)
        cause = {}

        def stop_group(why):
            cause.setdefault("cause", why)
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

        def on_signal(signum, _frame):
            stop_group(f"interrupted: the launcher took {signal.Signals(signum).name}")

        for s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(s, on_signal)
        with open(self.log, "a", encoding="utf-8") as log:
            log.write(f"=== {kind} {now()}\n")
            for line in proc.stderr:
                log.write(line)
                log.flush()
                print(line, end="", flush=True)
                m = LINE.match(line.rstrip("\n"))
                if not m:
                    continue
                wid, run, what = m.group(3), m.group(4), m.group(5)
                if what.startswith("FAILED"):
                    append(self.record / "flags.jsonl", {"time": now(), "flag": "failed run", "workload_id": wid,
                                                         "run": run, "line": what})
                    stop_group(f"a run failed: {wid}/{run}: {what}")
                    continue
                b = BUILT.search(what)
                if b and wid in slow and int(b.group(1)) > SLOW_MULTIPLE * slow[wid]:
                    append(self.record / "flags.jsonl",
                           {"time": now(), "flag": "slow run", "workload_id": wid, "run": run,
                            "seconds": int(b.group(1)), "file_slowest_smoke_seconds": slow[wid],
                            "multiple": SLOW_MULTIPLE})
                    print(f"  FLAGGED slow: {wid}/{run} {b.group(1)} s against {slow[wid]} s in the smoke", flush=True)
        try:
            code = proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            code = proc.wait()
        sealed_out.close()
        finished = code in (0, 2) and "cause" not in cause       # 0 and 2 differ by the verdict alone
        if finished:
            (self.sealed_dir / "exit-code").write_text(f"{code}\n")
            self.seal()
            why = "finished: every run and the end stages; the verdict line and the exit code sealed"
        else:
            why = cause.get("cause") or (f"the runner exited {code}: see the log's last lines" if code >= 0
                                         else f"the runner was ended by {signal.Signals(-code).name}")
        append(self.record / "stops.jsonl", {"stopped": now(), "cause": why, "runs_finished": self.finished_runs()})
        self.pidfile.unlink(missing_ok=True)
        print(f"\n{why}; {self.finished_runs()} runs finished", flush=True)
        return 0 if finished else 1

    # ---------------------------------------------------------------- the opening
    def open(self, settled):
        reading = self.record / "blind-reading.json"
        if not reading.exists():
            sys.exit(f"refused: {reading} is absent; the blind reading comes first (10.5 spec, decision 4)")
        doc = json.loads(reading.read_text())
        if not doc["clear"] and not settled:
            sys.exit("refused: the blind reading is not clear; `--settled NOTE` names where what it found was settled")
        self.unseal()
        code = (self.sealed_dir / "exit-code").read_text().strip()
        append(self.record / "opens.jsonl", {"opened": now(), "blind_reading_clear": doc["clear"],
                                             "settled": settled or "", "exit_code": int(code)})
        print((self.sealed_dir / "stdout.txt").read_text(), end="")
        print(f"exit code {code}; the report: {self.exp_dir / 'report.md'}")
        return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("command", choices=["start", "resume", "open"])
    ap.add_argument("--spec", default="harness/experiments/rq0-gate.yaml")
    ap.add_argument("--machine", default="harness/runner.yaml")
    ap.add_argument("--record", default=str(HERE / "run"))
    ap.add_argument("--min-free-gb", type=float, default=273.5)
    ap.add_argument("--smoke-times", default=str(SMOKE_TIMES))
    ap.add_argument("--settled", default=None)
    args = ap.parse_args()
    run = Run(args)
    if args.command == "start":
        return run.start()
    if args.command == "resume":
        return run.resume()
    return run.open(args.settled)


if __name__ == "__main__":
    sys.exit(main())
