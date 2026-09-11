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
directories — nothing experiment-shaped.
"""

import hashlib
import json
import pathlib
import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import yaml

from . import aggregates as agg
from . import evaluator, grader, guards, records, scorer, scoring
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


def load_machine(path, root) -> Machine:
    root = pathlib.Path(root)
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    def resolve(p):
        p = pathlib.Path(p)
        return p if p.is_absolute() else root / p

    def program(d):
        cmd = [str(c) for c in d["command"]]
        if len(cmd) > 1 and not cmd[1].startswith("-") and (root / cmd[1]).exists():
            cmd[1] = str(root / cmd[1])
        return Program(command=cmd, version=str(d["version"]))

    return Machine(daemon=program(doc["daemon"]), simulator=program(doc["simulator"]),
                   build_dir=resolve(doc["build_dir"]),
                   boot_defaults_dir=resolve(doc.get("boot_defaults_dir", "harness/boot-defaults")),
                   runs_dir=resolve(doc["runs_dir"]), cache_dir=resolve(doc["cache_dir"]))


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

    @property
    def name(self) -> str:
        return self.condition + (f"-{self.seed}" if self.seed else "") \
            + (f"+{self.boot_default}" if self.boot_default else "")

    @property
    def identity(self):
        return (self.workload_id, self.condition, self.table, self.seed, self.boot_default)


def expand(spec_path, machine: Machine, root) -> List[RunSpec]:
    spec = evaluator.load_spec(spec_path)
    root = pathlib.Path(root)
    table_doc = yaml.safe_load((root / spec["pins"]["driver_table"]["path"]).read_text())
    role = str((table_doc or {}).get("role", ""))
    primary = spec["boot_defaults"]["primary"]
    alternatives = list(spec["boot_defaults"]["alternatives"])
    n_seeds = int(spec["seed_count"])
    drawing = {"random"}
    runs = []
    files = list(spec["files"]["judging"]) + list(spec["files"]["reporting"])
    for wid in files:
        workload = machine.build_dir / f"{wid}.workload.json"
        for condition in spec["conditions"]:
            if condition == "fixed":
                for stem in [primary] + alternatives:
                    boot = "" if stem == primary else stem
                    runs.append(RunSpec(wid, "fixed", "", "", boot, machine.boot_defaults_dir / f"{stem}.json",
                                        workload))
            else:
                seeds = [str(i) for i in range(1, n_seeds + 1)] if condition in drawing else [""]
                for seed in seeds:
                    runs.append(RunSpec(wid, condition, role, seed, "",
                                        machine.boot_defaults_dir / f"{primary}.json", workload))
    return runs


# ------------------------------------------------------------- invocation

def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_key(program: Program, role: str, condition: str, seed: str, inputs: Dict[str, pathlib.Path]) -> str:
    material = {"program": role, "version": program.version, "command": list(program.command),
                "condition": condition, "seed": seed,
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
           with_condition: bool = True) -> Invocation:
    """Run `program` for one run, twice, through the invocation contract, or
    serve it from the cache; copy the first execution's outputs to `outputs`
    and its stderr to `stderr_log`. `inputs` and `outputs` map flag names
    (without dashes) to paths."""
    cache_dir = pathlib.Path(cache_dir)
    key = cache_key(program, role, condition, seed, inputs)
    entry = cache_dir / key
    stderr_log = pathlib.Path(stderr_log)
    if not entry.is_dir():
        tmp = cache_dir / f".tmp-{key}"
        if tmp.exists():
            shutil.rmtree(tmp)
        try:
            flags = []
            for name, path in inputs.items():
                flags += [f"--{name}", str(pathlib.Path(path).resolve())]
            if with_condition:
                flags += ["--condition", condition] + (["--seed", seed] if seed else [])
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
                 "condition": condition, "seed": seed,
                 "inputs": {n: _sha256(p) for n, p in sorted(inputs.items())},
                 "outputs": sorted(pathlib.Path(p).name for p in outputs.values())}, indent=1) + "\n")
            tmp.rename(entry)
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


def _trace_sim(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        head = json.loads(f.readline())
    return str(head.get("sim", ""))


# --------------------------------------------------------------- pipeline

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
    experiment_dir: Optional[pathlib.Path] = None


def run_experiment(spec_path, machine: Machine, root) -> Result:
    root = pathlib.Path(root)
    spec = evaluator.load_spec(spec_path)
    pins = spec["pins"]
    scoring_path = root / pins["scoring_spec"]["path"]
    guard_spec_path = root / pins["guard_spec"]["path"]
    table_path = root / pins["driver_table"]["path"]
    exp_dir = machine.runs_dir / spec["experiment"]
    exp_dir.mkdir(parents=True, exist_ok=True)
    result = Result(report=None, experiment_dir=exp_dir)
    runs = expand(spec_path, machine, root)

    built: Dict[tuple, dict] = {}           # identity -> {dir, rows, messages}
    for run in runs:
        run_dir = exp_dir / run.workload_id / run.name
        run_dir.mkdir(parents=True, exist_ok=True)
        try:
            d = invoke(machine.daemon, "daemon", machine.cache_dir, run.condition, run.seed,
                       inputs={"workload": run.workload_file, "driver-table": table_path,
                               "boot-default": run.boot_file},
                       outputs={"out-schedule": run_dir / "schedule.json", "out-log": run_dir / "log.json"},
                       stderr_log=run_dir / "daemon.stderr.log")
            s = invoke(machine.simulator, "simulator", machine.cache_dir, run.condition, run.seed,
                       inputs={"workload": run.workload_file, "schedule": run_dir / "schedule.json"},
                       outputs={"out-trace": run_dir / "trace.jsonl"},
                       stderr_log=run_dir / "simulator.stderr.log", with_condition=False)
            shutil.copy(s.entry / "second" / "trace.jsonl", run_dir / "trace.rerun.jsonl")
            sim = _trace_sim(run_dir / "trace.jsonl")
            if sim != machine.simulator.version:
                raise RunError(f"trace header names simulator {sim!r}, the machine configuration "
                               f"{machine.simulator.version!r}")
            rows, messages = records.build(run.workload_file, run_dir / "trace.jsonl", table=run.table,
                                           seed=run.seed, schedule_path=run_dir / "schedule.json",
                                           boot_default=run.boot_default)
            records.write_csv(rows, run_dir / "records.csv")
            (run_dir / "records-messages.json").write_text(json.dumps(messages, indent=1) + "\n")
            for inv in (d, s):
                result.cached += int(inv.cached)
                result.executed += int(not inv.cached)
            built[run.identity] = {"run": run, "dir": run_dir, "rows": rows, "messages": list(messages)}
        except (RunError, ValueError, OSError) as exc:
            for name in ("schedule.json", "log.json", "trace.jsonl", "trace.rerun.jsonl", "records.csv"):
                (run_dir / name).unlink(missing_ok=True)
            result.failed.append(Failure(run=f"{run.workload_id}/{run.name}", reason=str(exc)))
    if result.failed:
        (exp_dir / "failures.json").write_text(json.dumps(
            [{"run": f.run, "reason": f.reason} for f in result.failed], indent=1) + "\n")
        return result
    (exp_dir / "failures.json").unlink(missing_ok=True)

    # aggregates and scores
    scoring_spec = scoring.load_spec(scoring_path)
    agg_rows = []
    for identity, b in sorted(built.items()):
        wid = identity[0]
        agg_rows.extend(agg.compute_aggregates(b["rows"], scoring.windows_from_spec(scoring_spec, wid),
                                               scoring.interactive_from_spec(scoring_spec, wid)))
    write_csv(agg_rows, agg.COLUMNS, exp_dir / "aggregates.csv")
    term_rows, file_rows = scorer.score(agg_rows, scoring_spec)
    write_csv(term_rows + file_rows, scorer.COLUMNS, exp_dir / "scores.csv")

    # guards, through the manifest the guards command reads
    manifest = {"aggregates": str(exp_dir / "aggregates.csv"), "scoring_spec": str(scoring_path), "runs": []}
    guard_runs = []
    for identity, b in sorted(built.items()):
        run, run_dir = b["run"], b["dir"]
        entry = {"workload_id": run.workload_id, "condition": run.condition, "table": run.table,
                 "seed": run.seed, "boot_default": run.boot_default,
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
                                     trace=run_dir / "trace.jsonl"))
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
                                  "log": str(run_dir / "log.json"), "workload": str(run.workload_file)})
        rows, _messages = grader.grade_log(grader.Run(workload_id=run.workload_id, condition=run.condition,
                                                      table=run.table, seed=run.seed,
                                                      boot_default=run.boot_default, log=run_dir / "log.json",
                                                      workload=run.workload_file, table_path=table_path))
        records.write_csv(rows, run_dir / "recognition-records.csv")
        grade_rows.extend(rows)
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

def write_smoke_spec(path, machine: Machine, root, files=None, experiment="smoke") -> pathlib.Path:
    """A throwaway experiment spec over the compiled coreset for the pipeline
    smoke run (8.6 spec, decision 8): every file with scoring terms as judging
    (the first `files` of them when given), the mock conditions, two seeds, no
    alternative boot default, pins computed from the files as they are, and a
    placeholder criterion. Linted before it is returned; never committed."""
    root = pathlib.Path(root)
    pins = {"scoring_spec": "harness/scoring/scoring-spec.yaml", "guard_spec": "harness/guards/guard-spec.yaml",
            "driver_table": "daemon/driver-table/prior.yaml", "dataset": "dataset/build.manifest.json"}
    spec = scoring.load_spec(root / pins["scoring_spec"])
    judging = [wid for wid in sorted(spec["files"]) if (machine.build_dir / f"{wid}.workload.json").is_file()]
    if files is not None:
        judging = judging[:files]
    exclusions = [wid for wid in judging
                  if any(s.pre_committed_miss
                         for s in grader.read_ground_truth(machine.build_dir / f"{wid}.workload.json"))]
    guard_version = str(yaml.safe_load((root / pins["guard_spec"]).read_text()).get("version"))
    doc = {"experiment": experiment, "conditions": list(SMOKE_CONDITIONS), "seed_count": 2,
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


__all__ = ["Failure", "Invocation", "Machine", "Program", "Result", "RunError", "RunSpec", "cache_key",
           "expand", "invoke", "load_machine", "run_experiment", "write_smoke_spec"]
