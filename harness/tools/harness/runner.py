"""The runner (Phase 8 spec, decisions 9–12; sub-task 8.6).

`expand` turns a per-experiment spec's generic part into the run matrix: for
every listed file, `fixed` under the primary boot default and under each
alternative, every other condition under the primary, a drawing condition once
per seed from 1 to the seed count. `invoke` starts one program for one run
through the invocation contract (data-contracts §11): a configured command
prefix plus the named flags, absolute paths, stdout ignored, stderr captured,
exit 0 or failure. Every invocation is executed twice and the declared outputs
must be byte-identical — the contract's one behavioural clause — and both
executions are kept in the cache under a key over the program's version, its
prefix, the condition and seed, and the input files' bytes; a known key is
never re-executed and a failed invocation is never cached.

`run_experiment` drives the whole pipeline from the run matrix to the report:
records per run (the build's guard messages recorded as an explicit list),
aggregates and scores, the guards over the run set through the manifest the
guards command reads, the grader over the recognition logs through its own
manifest, and the RQ0 gate evaluator. A failed invocation leaves the run's
outputs absent; the runner names every failed run and stops before scoring.
Traces are asked for uncompressed in this phase (8.6 spec, decision 3).

The machine configuration (`Machine`, an uncommitted YAML beside
`harness/runner.example.yaml`) names the two commands with their version
strings, the compiled build, the boot-default files, the runs and cache
directories — nothing experiment-shaped. A spec that pins the two programs'
version strings (`pins.simulator`, `pins.daemon`; 10.2) is refused before any
run when the machine configuration names other versions.

The configuration's `workers` spreads the runs over processes (`run_all`), the
runs on heavy files in a pool of their own; every stage after the runs reads
them sorted by identity, so the outputs do not depend on how many ran at once.
Each run's records, aggregates and graded queries are kept in a results cache
beside the execution cache (`process_run`), keyed by both invocations, the
run's identity, its scoring windows and the harness's own code, so a run met
again — a restart after a crash, a second pass — is not rebuilt.
"""

import concurrent.futures
import csv
import hashlib
import json
import multiprocessing
import os
import pathlib
import pickle
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import yaml

from . import aggregates as agg
from . import evaluator, grader, guards, manifests, records, scorer, scoring
from .reader import read_config_schedule, read_recognition_log
from .outputs import write_csv

HARNESS = pathlib.Path(__file__).resolve().parents[2]
REPO = HARNESS.parent
SMOKE_CONDITIONS = ("fixed", "oracle", "random")


class RunError(Exception):
    """One invocation failed: a non-zero exit, outputs that differ across the
    two executions, or a trace header naming another simulator."""


@dataclass(frozen=True)
class Program:
    command: List[str]          # the prefix the contract's flags are appended to
    version: str                # hashed into the cache key; the simulator's is checked against `sim`


@dataclass
class Machine:
    daemon: Program
    simulator: Program
    build_dir: pathlib.Path
    boot_defaults_dir: pathlib.Path
    runs_dir: pathlib.Path
    cache_dir: pathlib.Path
    workers: int = 1            # runs at once on a file under heavy_mb; 1 runs everything in this process, in order
    heavy_workers: int = 1      # with workers > 1: runs at once on a file of heavy_mb or more, each in a fresh process
    heavy_mb: int = 50          # a workload file this large or larger is a heavy run (its records hold gigabytes)


def load_machine(path, root) -> Machine:
    root = pathlib.Path(root)
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    def resolve(p):
        p = pathlib.Path(p)
        return p if p.is_absolute() else root / p

    def program(d):
        cmd = [str(c) for c in d["command"]]
        if "/" in cmd[0] and not pathlib.Path(cmd[0]).is_absolute() and (root / cmd[0]).exists():
            cmd[0] = str(root / cmd[0])                 # a program run directly: simulator/src/sim
        if len(cmd) > 1 and not cmd[1].startswith("-") and (root / cmd[1]).exists():
            cmd[1] = str(root / cmd[1])
        return Program(command=cmd, version=str(d["version"]))

    return Machine(daemon=program(doc["daemon"]), simulator=program(doc["simulator"]),
                   build_dir=resolve(doc["build_dir"]),
                   boot_defaults_dir=resolve(doc.get("boot_defaults_dir", "harness/boot-defaults")),
                   runs_dir=resolve(doc["runs_dir"]), cache_dir=resolve(doc["cache_dir"]),
                   workers=int(doc.get("workers", 1)), heavy_workers=int(doc.get("heavy_workers", 1)),
                   heavy_mb=int(doc.get("heavy_mb", 50)))


# ------------------------------------------------------------------ matrix

@dataclass(frozen=True)
class RunSpec:
    workload_id: str
    condition: str
    table: str                  # the pinned driver table's role; empty for fixed
    seed: str                   # "1".."N" for a drawing condition, else ""
    boot_default: str           # the alternative's stem; "" for the primary
    boot_file: pathlib.Path
    workload_file: pathlib.Path
    telemetry: str              # the telemetry shape shown to the recognizer: `focus` or `names` (9.17)
    table_file: Optional[pathlib.Path] = None   # an alternative driver table's path (10.1); None: the pinned primary

    @property
    def table_stem(self) -> str:
        """The alternative table's stem from its label (`prior@floor-0.2` → `floor-0.2`); empty under the primary."""
        return self.table.partition("@")[2]

    @property
    def name(self) -> str:
        return self.condition + (f"-{self.seed}" if self.seed else "") \
            + (f"+{self.boot_default}" if self.boot_default else "") \
            + (f"@{self.table_stem}" if self.table_stem else "") + f"~{self.telemetry}"

    @property
    def identity(self):
        return (self.workload_id, self.condition, self.table, self.seed, self.boot_default, self.telemetry)


def expand(spec_path, machine: Machine, root) -> List[RunSpec]:
    spec = evaluator.load_spec(spec_path)
    root = pathlib.Path(root)
    spec, paths, _axes = manifests.expand(spec, root)             # 9.21 decision 6: the selections as ids
    table_doc = yaml.safe_load((root / spec["pins"]["driver_table"]["path"]).read_text())
    role = str((table_doc or {}).get("role", ""))
    primary = spec["boot_defaults"]["primary"]
    alternatives = list(spec["boot_defaults"]["alternatives"])
    n_seeds = int(spec["seed_count"])
    drawing = {"random"}
    runs = []
    files = list(spec["files"]["judging"]) + list(spec["files"]["reporting"])
    variants = list(spec["files"].get("variants") or [])          # 9.14 decision 12: the primary boot default alone
    shapes = list(spec["telemetry"])                                # 9.17: every condition under every shape listed
    for wid in files + variants:
        workload = manifests.workload_path(wid, paths, machine.build_dir)
        for shape in shapes:
            for condition in spec["conditions"]:
                if condition == "fixed":
                    for stem in [primary] + ([] if wid in variants else alternatives):
                        boot = "" if stem == primary else stem
                        runs.append(RunSpec(wid, "fixed", "", "", boot, machine.boot_defaults_dir / f"{stem}.json",
                                            workload, telemetry=shape))
                else:
                    seeds = [str(i) for i in range(1, n_seeds + 1)] if condition in drawing else [""]
                    for seed in seeds:
                        runs.append(RunSpec(wid, condition, role, seed, "",
                                            machine.boot_defaults_dir / f"{primary}.json", workload,
                                            telemetry=shape))
    # 10.1: the cap band's alternative driver tables — every condition that reads the table (all but fixed), on
    # the judging files alone, under the primary boot default and every shape, at the run's N; the daemon reads
    # the alternative's file and the rows carry the label `<role>@<stem>`
    for stem, pin in sorted((spec["pins"].get("driver_table_alternatives") or {}).items()):
        label = evaluator.table_label(role, stem)
        for wid in spec["files"]["judging"]:
            workload = manifests.workload_path(wid, paths, machine.build_dir)
            for shape in shapes:
                for condition in spec["conditions"]:
                    if condition == "fixed":
                        continue
                    seeds = [str(i) for i in range(1, n_seeds + 1)] if condition in drawing else [""]
                    for seed in seeds:
                        runs.append(RunSpec(wid, condition, label, seed, "",
                                            machine.boot_defaults_dir / f"{primary}.json", workload,
                                            telemetry=shape, table_file=root / pin["path"]))
    return runs


# ------------------------------------------------------------- invocation

def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_key(program: Program, role: str, condition: str, seed: str, inputs: Dict[str, pathlib.Path],
              telemetry: str = "") -> str:
    material = {"program": role, "version": program.version, "command": list(program.command),
                "condition": condition, "seed": seed, "telemetry": telemetry,
                "inputs": {name: _sha256(path) for name, path in sorted(inputs.items())}}
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()


@dataclass
class Invocation:
    key: str
    cached: bool
    entry: pathlib.Path         # the cache entry: first/, second/, stderr.log, stderr.rerun.log, meta.json


def _execute(argv, out_dir, stderr_path):
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(stderr_path, "w", encoding="utf-8") as err:
        proc = subprocess.run(argv, stdout=subprocess.DEVNULL, stderr=err)
    return proc.returncode


def invoke(program: Program, role: str, cache_dir, condition: str, seed: str,
           inputs: Dict[str, pathlib.Path], outputs: Dict[str, pathlib.Path], stderr_log,
           with_condition: bool = True, telemetry: str = "") -> Invocation:
    """Run `program` for one run, twice, through the invocation contract, or
    serve it from the cache; copy the first execution's outputs to `outputs`
    and its stderr to `stderr_log`. `inputs` and `outputs` map flag names
    (without dashes) to paths. `telemetry`, the daemon's shape flag (9.17), is
    passed when given and is part of the key."""
    cache_dir = pathlib.Path(cache_dir)
    key = cache_key(program, role, condition, seed, inputs, telemetry)
    entry = cache_dir / key
    stderr_log = pathlib.Path(stderr_log)
    if not entry.is_dir():
        tmp = cache_dir / f".tmp-{key}-{os.getpid()}"     # one per process: parallel runs may share a key
        if tmp.exists():
            shutil.rmtree(tmp)
        try:
            flags = []
            for name, path in inputs.items():
                flags += [f"--{name}", str(pathlib.Path(path).resolve())]
            if with_condition:
                flags += ["--condition", condition] + (["--seed", seed] if seed else [])
            if telemetry:
                flags += ["--telemetry", telemetry]
            for which in ("first", "second"):
                out_dir = tmp / which
                argv = list(program.command) + flags
                for name, path in outputs.items():
                    argv += [f"--{name}", str(out_dir / pathlib.Path(path).name)]
                err = tmp / ("stderr.log" if which == "first" else "stderr.rerun.log")
                code = _execute(argv, out_dir, err)
                if code != 0:
                    shutil.copy(err, stderr_log)
                    raise RunError(f"{role} exit {code} ({which} execution); stderr in {stderr_log}")
                for path in outputs.values():
                    if not (out_dir / pathlib.Path(path).name).is_file():
                        shutil.copy(err, stderr_log)
                        raise RunError(f"{role} exit 0 but did not write {pathlib.Path(path).name}")
            for path in outputs.values():
                name = pathlib.Path(path).name
                if (tmp / "first" / name).read_bytes() != (tmp / "second" / name).read_bytes():
                    shutil.copy(tmp / "stderr.log", stderr_log)
                    raise RunError(f"{role}: {name} is not byte-identical across the two executions "
                                   f"(contract 10, determinism)")
            (tmp / "meta.json").write_text(json.dumps(
                {"program": role, "version": program.version, "command": list(program.command),
                 "condition": condition, "seed": seed, "telemetry": telemetry,
                 "inputs": {n: _sha256(p) for n, p in sorted(inputs.items())},
                 "outputs": sorted(pathlib.Path(p).name for p in outputs.values())}, indent=1) + "\n")
            _publish(tmp, entry)
            cached = False
        except RunError:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
    else:
        cached = True
    for path in outputs.values():
        path = pathlib.Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(entry / "first" / path.name, path)
    shutil.copy(entry / "stderr.log", stderr_log)
    return Invocation(key=key, cached=cached, entry=entry)


def _publish(tmp: pathlib.Path, entry: pathlib.Path):
    """Move a finished cache entry into place. Another process may have published the same key meanwhile — the same
    bytes, by the determinism clause — and then its entry stands and this one is dropped."""
    try:
        tmp.rename(entry)
    except OSError:
        if not entry.is_dir():
            raise
        shutil.rmtree(tmp, ignore_errors=True)


def _trace_sim(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        head = json.loads(f.readline())
    return str(head.get("sim", ""))


# ------------------------------------------------------------- one run's work

@dataclass
class RunContext:
    """What one run's work reads beyond its RunSpec — the same for every run, sent once to each worker process."""
    machine: Machine
    exp_dir: pathlib.Path
    table_path: pathlib.Path    # the pinned primary driver table
    scoring_spec: dict          # with the variant and generated files' entries
    harness: str                # harness_version()


def harness_version() -> str:
    """The SHA-256 of the harness package's own source files: part of every results-cache key, so a change to
    any module that builds records, aggregates or graded queries rebuilds every run's."""
    h = hashlib.sha256()
    for path in sorted(pathlib.Path(__file__).resolve().parent.glob("*.py")):
        h.update(path.name.encode() + b"\0" + path.read_bytes() + b"\0")
    return h.hexdigest()


RESULT_FILES = ("records.csv", "records-messages.json", "recognition-records.csv")


def result_key(ctx: RunContext, run: RunSpec, daemon_key: str, simulator_key: str) -> str:
    """The results cache's key: both invocations' keys (every input byte and both programs' versions), the run's
    identity, the scoring windows its aggregates read, and the harness's own code."""
    material = {"harness": ctx.harness, "daemon": daemon_key, "simulator": simulator_key,
                "identity": list(run.identity),
                "windows": repr(scoring.windows_from_spec(ctx.scoring_spec, run.workload_id)),
                "interactive": repr(scoring.interactive_from_spec(ctx.scoring_spec, run.workload_id))}
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()


def _place(src: pathlib.Path, dst: pathlib.Path):
    """dst as a hard link to src where the file system allows, else a copy. A run never writes into a file
    it placed: every result file is unlinked before the run's work begins."""
    dst.unlink(missing_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy(src, dst)


def process_run(run: RunSpec, ctx: RunContext) -> dict:
    """One run's work: the daemon and the simulator through the invocation contract (served from the
    execution cache when known), the trace header checked, then the records, the aggregates and, for a
    recognizing run, the graded queries and the flip aggregates — or those served from the results cache
    under `result_key`, the records files placed in the run directory as if built. Returns a dict with
    `aggregates`, `messages`, `grade_rows`, `executed`, `cached`, `results_cached` and `seconds`, or
    `failure` with the reason when an invocation or a reader failed (the run's outputs then removed).
    The cache entry is a pickle the runner wrote itself; nothing else writes into the cache directory."""
    t0 = time.time()
    machine = ctx.machine
    run_dir = ctx.exp_dir / run.workload_id / run.name
    run_dir.mkdir(parents=True, exist_ok=True)
    run_table = run.table_file or ctx.table_path                 # 10.1: an alternative table's run reads its own
    try:
        d = invoke(machine.daemon, "daemon", machine.cache_dir, run.condition, run.seed,
                   inputs={"workload": run.workload_file, "driver-table": run_table,
                           "boot-default": run.boot_file},
                   outputs={"out-schedule": run_dir / "schedule.json", "out-log": run_dir / "log.json"},
                   stderr_log=run_dir / "daemon.stderr.log", telemetry=run.telemetry)
        s = invoke(machine.simulator, "simulator", machine.cache_dir, run.condition, run.seed,
                   inputs={"workload": run.workload_file, "schedule": run_dir / "schedule.json"},
                   outputs={"out-trace": run_dir / "trace.jsonl"},
                   stderr_log=run_dir / "simulator.stderr.log", with_condition=False)
        shutil.copy(s.entry / "second" / "trace.jsonl", run_dir / "trace.rerun.jsonl")
        sim = _trace_sim(run_dir / "trace.jsonl")
        if sim != machine.simulator.version:
            raise RunError(f"trace header names simulator {sim!r}, the machine configuration "
                           f"{machine.simulator.version!r}")
        for name in RESULT_FILES:
            (run_dir / name).unlink(missing_ok=True)
        entry = machine.cache_dir / "results" / result_key(ctx, run, d.key, s.key)
        if (entry / "result.pickle").is_file():
            with open(entry / "result.pickle", "rb") as f:
                kept = pickle.load(f)
            for name in RESULT_FILES:
                if (entry / name).is_file():
                    _place(entry / name, run_dir / name)
            from_cache = True
        else:
            kept = _build_results(run, ctx, run_dir, run_table)
            _store_results(entry, run_dir, kept)
            from_cache = False
        return {**kept, "executed": int(not d.cached) + int(not s.cached), "cached": int(d.cached) + int(s.cached),
                "results_cached": from_cache, "seconds": round(time.time() - t0, 1)}
    except (RunError, ValueError, OSError) as exc:
        for name in ("schedule.json", "log.json", "trace.jsonl", "trace.rerun.jsonl") + RESULT_FILES:
            (run_dir / name).unlink(missing_ok=True)
        return {"failure": str(exc)}


def _build_results(run: RunSpec, ctx: RunContext, run_dir: pathlib.Path, run_table: pathlib.Path) -> dict:
    # each run is aggregated as soon as its records are built, so a run's rows — fourteen million for c6-dual —
    # live only until its aggregates exist, never all runs' at once
    rows, messages = records.build(run.workload_file, run_dir / "trace.jsonl", table=run.table,
                                   seed=run.seed, schedule_path=run_dir / "schedule.json",
                                   boot_default=run.boot_default, telemetry=run.telemetry)
    records.write_csv(rows, run_dir / "records.csv")
    (run_dir / "records-messages.json").write_text(json.dumps(messages, indent=1) + "\n")
    aggregates = agg.compute_aggregates(rows, scoring.windows_from_spec(ctx.scoring_spec, run.workload_id),
                                        scoring.interactive_from_spec(ctx.scoring_spec, run.workload_id))
    del rows
    grade_rows_run = []
    if run.condition != "fixed":
        # Layer 1 for this run now, so the flip aggregates (9.21 decision 7) can read its graded queries
        grade_rows_run, _gmessages = grader.grade_log(grader.Run(
            workload_id=run.workload_id, condition=run.condition, table=run.table, seed=run.seed,
            boot_default=run.boot_default, log=run_dir / "log.json", workload=run.workload_file,
            table_path=run_table, telemetry=run.telemetry))
        records.write_csv(grade_rows_run, run_dir / "recognition-records.csv")
        aggregates = aggregates + agg.flip_aggregates(
            aggregates, read_config_schedule(run_dir / "schedule.json"),
            read_recognition_log(run_dir / "log.json"), grade_rows_run)
        aggregates.sort(key=agg.sort_key)
    return {"aggregates": aggregates, "messages": list(messages), "grade_rows": grade_rows_run}


def _store_results(entry: pathlib.Path, run_dir: pathlib.Path, kept: dict):
    tmp = entry.parent / f".tmp-{entry.name}-{os.getpid()}"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    for name in RESULT_FILES:
        if (run_dir / name).is_file():
            _place(run_dir / name, tmp / name)
    with open(tmp / "result.pickle", "wb") as f:
        pickle.dump(kept, f, protocol=pickle.HIGHEST_PROTOCOL)
    _publish(tmp, entry)


# ------------------------------------------------------------ runs at once

_WORKER_CTX: Optional[RunContext] = None


def _init_worker(ctx: RunContext):
    global _WORKER_CTX
    _WORKER_CTX = ctx


def _in_worker(run: RunSpec) -> dict:
    return process_run(run, _WORKER_CTX)


def is_heavy(run: RunSpec, machine: Machine) -> bool:
    return run.workload_file.stat().st_size >= machine.heavy_mb * (1 << 20)


def run_all(runs: List[RunSpec], ctx: RunContext, progress=None):
    """Every run's work, as (run, outcome) pairs in the order the runs finish. With `workers` 1 the runs
    go one after another in this process, in matrix order. Otherwise a pool of `workers` processes takes
    the runs on files under `heavy_mb` and a pool of `heavy_workers` the rest, each heavy run in a fresh
    process so that the gigabytes its records held go back to the system when it ends; each pool takes
    its largest files first. Nothing the runner writes depends on the order: the stages after the runs
    read them sorted by identity."""
    machine = ctx.machine
    total = len(runs)
    if machine.workers <= 1:
        for k, run in enumerate(runs, 1):
            out = process_run(run, ctx)
            if progress:
                progress(k, total, run, out)
            yield run, out
        return
    by_size = sorted(runs, key=lambda r: -r.workload_file.stat().st_size)
    heavy = [r for r in by_size if is_heavy(r, machine)]
    light = [r for r in by_size if not is_heavy(r, machine)]
    spawn = multiprocessing.get_context("spawn")
    pools = [concurrent.futures.ProcessPoolExecutor(max_workers=machine.workers, mp_context=spawn,
                                                    initializer=_init_worker, initargs=(ctx,))]
    if heavy:
        pools.append(concurrent.futures.ProcessPoolExecutor(max_workers=max(1, machine.heavy_workers),
                                                            mp_context=spawn, initializer=_init_worker,
                                                            initargs=(ctx,), max_tasks_per_child=1))
    try:
        futures = {pools[0].submit(_in_worker, r): r for r in light}
        futures.update({pools[-1].submit(_in_worker, r): r for r in heavy})
        for k, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            run, out = futures[fut], fut.result()
            if progress:
                progress(k, total, run, out)
            yield run, out
    finally:
        for pool in pools:
            pool.shutdown(wait=True, cancel_futures=True)


# --------------------------------------------------------------- pipeline

def program_pin_errors(spec, machine: Machine) -> List[str]:
    """The spec's program pins against the machine configuration (10.2, decision 11): each of
    `pins.simulator` and `pins.daemon` the spec carries must name the version the configuration
    names. Optional: a spec without them (the mocks', the generated smoke spec) checks nothing."""
    errors = []
    pins = spec.get("pins") or {}
    for role, program in (("simulator", machine.simulator), ("daemon", machine.daemon)):
        pin = pins.get(role)
        if pin and pin.get("version") != program.version:
            errors.append(f"pins/{role}: the spec pins {pin.get('version')!r}, the machine configuration "
                          f"names {program.version!r}")
    return errors


@dataclass
class Failure:
    run: str
    reason: str


@dataclass
class Result:
    report: Optional[dict]
    failed: List[Failure] = field(default_factory=list)
    executed: int = 0
    cached: int = 0
    results_cached: int = 0     # runs whose records, aggregates and graded queries came from the results cache
    experiment_dir: Optional[pathlib.Path] = None


def run_experiment(spec_path, machine: Machine, root,
                   progress: Optional[Callable[[int, int, "RunSpec", dict], None]] = None) -> Result:
    """The pipeline from the run matrix to the report. Runs are spread over the machine configuration's
    workers (`run_all`); `progress(done, total, run, outcome)` is called as each one finishes."""
    root = pathlib.Path(root)
    spec = evaluator.load_spec(spec_path)
    refused = program_pin_errors(spec, machine)                  # 10.2: before any run, and before any directory
    if refused:
        raise RunError("the spec's program pins do not match the machine configuration: " + "; ".join(refused))
    pins = spec["pins"]
    scoring_path = root / pins["scoring_spec"]["path"]
    guard_spec_path = root / pins["guard_spec"]["path"]
    table_path = root / pins["driver_table"]["path"]
    exp_dir = machine.runs_dir / spec["experiment"]
    exp_dir.mkdir(parents=True, exist_ok=True)
    result = Result(report=None, experiment_dir=exp_dir)
    runs = expand(spec_path, machine, root)
    spec, _paths, axes = manifests.expand(spec, root)              # 9.21 decision 6: the selected files and their sets
    # the scoring spec, with an entry per variant file (9.14 decision 12: scored on its base's terms, its windows
    # on its own segments) and per selected generated file (9.21 decision 1: the rule over the C1 entries, from the
    # set's pinned manifest)
    scoring_spec = scoring.with_variants(scoring.load_spec(scoring_path),
                                         {wid: machine.build_dir / f"{wid}.workload.json"
                                          for wid in (spec["files"].get("variants") or [])})
    selected_by_set = {}
    for wid, (set_name, _record) in axes.items():
        selected_by_set.setdefault(set_name, set()).add(wid)
    for set_name, wids in sorted(selected_by_set.items()):
        manifest = manifests.load(root / pins["generated"][set_name]["path"])
        scoring_spec = scoring.with_generated(scoring_spec, manifest, only=wids)

    built: Dict[tuple, dict] = {}           # identity -> {run, dir, aggregates, messages, grade_rows}
    ctx = RunContext(machine=machine, exp_dir=exp_dir, table_path=table_path, scoring_spec=scoring_spec,
                     harness=harness_version())
    times = []
    for run, out in run_all(runs, ctx, progress):
        if "failure" in out:
            result.failed.append(Failure(run=f"{run.workload_id}/{run.name}", reason=out["failure"]))
            continue
        result.executed += out["executed"]
        result.cached += out["cached"]
        result.results_cached += int(out["results_cached"])
        times.append((run.workload_id, run.name, out["seconds"], "cache" if out["results_cached"] else "built"))
        built[run.identity] = {"run": run, "dir": exp_dir / run.workload_id / run.name,
                               "aggregates": out["aggregates"], "messages": out["messages"],
                               "grade_rows": out["grade_rows"]}
    with open(exp_dir / "run-times.csv", "w", newline="", encoding="utf-8") as f:   # wall seconds per run, for cost
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["workload_id", "run", "seconds", "records"])
        w.writerows(sorted(times))
    order = {f"{r.workload_id}/{r.name}": k for k, r in enumerate(runs)}
    result.failed.sort(key=lambda f: order[f.run])                 # matrix order, however the runs finished
    if result.failed:
        (exp_dir / "failures.json").write_text(json.dumps(
            [{"run": f.run, "reason": f.reason} for f in result.failed], indent=1) + "\n")
        return result
    (exp_dir / "failures.json").unlink(missing_ok=True)

    # aggregates and scores
    agg_rows = [row for _identity, b in sorted(built.items()) for row in b["aggregates"]]
    write_csv(agg_rows, agg.COLUMNS, exp_dir / "aggregates.csv")
    term_rows, file_rows = scorer.score(agg_rows, scoring_spec)
    write_csv(term_rows + file_rows, scorer.COLUMNS, exp_dir / "scores.csv")

    # guards, through the manifest the guards command reads
    manifest = {"aggregates": str(exp_dir / "aggregates.csv"), "scoring_spec": str(scoring_path), "runs": []}
    guard_runs = []
    for identity, b in sorted(built.items()):
        run, run_dir = b["run"], b["dir"]
        entry = {"workload_id": run.workload_id, "condition": run.condition, "table": run.table,
                 "seed": run.seed, "boot_default": run.boot_default, "telemetry": run.telemetry,
                 "records": str(run_dir / "records.csv"), "schedule": str(run_dir / "schedule.json"),
                 "log": str(run_dir / "log.json"), "workload": str(run.workload_file),
                 "rerun_trace": str(run_dir / "trace.rerun.jsonl"), "trace": str(run_dir / "trace.jsonl"),
                 "guard_messages": b["messages"]}
        manifest["runs"].append(entry)
        guard_runs.append(guards.Run(workload_id=run.workload_id, condition=run.condition, table=run.table,
                                     seed=run.seed, boot_default=run.boot_default,
                                     records=run_dir / "records.csv", schedule=run_dir / "schedule.json",
                                     log=run_dir / "log.json", workload=run.workload_file,
                                     rerun_trace=run_dir / "trace.rerun.jsonl", guard_messages=b["messages"],
                                     trace=run_dir / "trace.jsonl", telemetry=run.telemetry))
    (exp_dir / "guards-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    guard_rows = guards.evaluate(guard_runs, guards.load_spec(guard_spec_path), agg_rows, scoring_spec)
    write_csv(guard_rows, guards.COLUMNS, exp_dir / "guards.csv")

    # grades, through the grade command's manifest, over every recognizing run
    gmanifest = {"driver_table": str(table_path),
                 "bootstrap": {"seed": grader.BOOTSTRAP_SEED, "repetitions": grader.BOOTSTRAP_REPETITIONS},
                 "runs": []}
    grade_rows = []
    for identity, b in sorted(built.items()):
        run, run_dir = b["run"], b["dir"]
        if run.condition == "fixed":
            continue
        gmanifest["runs"].append({"workload_id": run.workload_id, "condition": run.condition,
                                  "table": run.table, "seed": run.seed, "boot_default": run.boot_default,
                                  "telemetry": run.telemetry,
                                  "log": str(run_dir / "log.json"), "workload": str(run.workload_file),
                                  **({"driver_table": str(run.table_file)} if run.table_file else {})})
        grade_rows.extend(b["grade_rows"])                      # graded in the main loop, beside its aggregates
    (exp_dir / "grade-manifest.json").write_text(json.dumps(gmanifest, indent=1) + "\n")
    grades = grader.compute_grades(grade_rows, bootstrap=grader.Bootstrap())
    write_csv(grades, grader.COLUMNS, exp_dir / "grades.csv")

    # the verdict
    report = evaluator.evaluate(spec_path, exp_dir / "aggregates.csv", exp_dir / "scores.csv",
                                exp_dir / "guards.csv", exp_dir / "grades.csv", root)
    evaluator.validate_report(report)
    evaluator.write_report(report, exp_dir / "report.json")
    (exp_dir / "report.md").write_text(evaluator.render(report), encoding="utf-8")
    result.report = report
    return result


# ------------------------------------------------------------------ smoke

def write_smoke_spec(path, machine: Machine, root, files=None, experiment="smoke", only=None) -> pathlib.Path:
    """A throwaway experiment spec over the compiled coreset for the pipeline
    smoke run (8.6 spec, decision 8): every file with scoring terms as judging
    (the first `files` of them when given, or the files named in `only` — 10.2's
    short run), the mock conditions, two seeds, no alternative boot default, pins
    computed from the files as they are, and a placeholder criterion. Linted
    before it is returned; never committed."""
    root = pathlib.Path(root)
    pins = {"scoring_spec": "harness/scoring/scoring-spec.yaml", "guard_spec": "harness/guards/guard-spec.yaml",
            "driver_table": "daemon/driver-table/prior.yaml", "dataset": "dataset/build.manifest.json"}
    spec = scoring.load_spec(root / pins["scoring_spec"])
    judging = [wid for wid in sorted(spec["files"]) if (machine.build_dir / f"{wid}.workload.json").is_file()]
    if only is not None:
        missing = sorted(set(only) - set(judging))
        if missing:
            raise RunError(f"smoke: no scored, compiled file {missing}")
        judging = [wid for wid in judging if wid in set(only)]
    if files is not None:
        judging = judging[:files]
    exclusions = [wid for wid in judging
                  if any(s.pre_committed_miss
                         for s in grader.read_ground_truth(machine.build_dir / f"{wid}.workload.json"))]
    guard_version = str(yaml.safe_load((root / pins["guard_spec"]).read_text()).get("version"))
    doc = {"experiment": experiment, "conditions": list(SMOKE_CONDITIONS), "telemetry": ["focus"], "seed_count": 2,
           "boot_defaults": {"primary": "ostep", "alternatives": []},
           "files": {"judging": judging, "reporting": []},
           "layer1_exclusions": exclusions, "guard_exemptions": [],
           "reporting_lines": [{"type": "floor_band", "latency_floors_us": [1000]},
                               {"type": "exclusion_accuracy"}, {"type": "layer1_headline"},
                               {"type": "random_beats_oracle"}],
           "pins": {name: {"path": rel, "sha256": _sha256(root / rel)} for name, rel in pins.items()},
           "criterion": {"type": "k_of_n_gap", "k": 1, "g": 0.1, "reference": "oracle", "compared": "random",
                         "seed_statistic": "mean"}}
    doc["pins"]["guard_spec"]["version"] = guard_version
    path = pathlib.Path(path)
    path.write_text("# throwaway smoke spec — generated by harness/tools/harness/runner.py, never committed\n"
                    + yaml.safe_dump(doc, sort_keys=False))
    errors = evaluator.lint_spec(path, evaluator.SPEC_SCHEMA, machine.build_dir, root)
    if errors:
        raise RunError("smoke spec does not lint: " + "; ".join(errors))
    return path


__all__ = ["Failure", "Invocation", "Machine", "Program", "Result", "RunContext", "RunError", "RunSpec",
           "cache_key", "expand", "harness_version", "invoke", "is_heavy", "load_machine", "process_run",
           "program_pin_errors", "result_key", "run_all", "run_experiment", "write_smoke_spec"]
