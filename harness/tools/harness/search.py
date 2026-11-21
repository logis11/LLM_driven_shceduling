"""The configuration search (the RQ0 gate spec's statement `failure-procedure`; sub-task 11.4,
`_dev/docs/spec/jioh/task-11.4-the-configuration-search.md`).

A search spec (`harness/experiments/<search>.yaml`, schema `experiments/schema/search-spec.schema.json`) names the
files searched, the grid of configurations, how a point is read, the two checks run before the grid, the route rule,
and the pins. `lint_spec` checks it against its schema, the compiled files, the pinned scoring spec's terms, the
boot-default files, the prior table and the pins' bytes, and expands the grid: the count the spec states, every
point a legal configuration (the boot-default schema), no point twice, and the boot default, each alternative and
each of the prior table's distinct configurations among the points.

A point is one configuration applied where the oracle applies its row, the labels ignored: the oracle condition
under a table whose every row is the point's configuration (`point_table`), run by the runner's own `process_run`
— the daemon and the simulator through the invocation contract, each executed twice and cached, the records and
aggregates built as for any run — its rows labelled `<role>@<point>` in the `table` column, as an alternative
table's are (10.1). Beside each run: the pinned guard spec's guards on it, and `simulator/tools/wait_check.py`'s
four readings of its trace.

`search` runs the boot default's point and the row's point on every file first and checks them against the
corrected runs the spec names (`check_runs`); a check that does not reproduce its run stops the search before the
rest of the grid runs. Then every point, then `read` over the points' scored terms: per file the quantity of every
point, the finding at the primary, under the g band and under each alternative boot default, the best point, the
count of the prior table's configurations at least the row's for a file at finding 2, the points out of the reading
and why, the flag of a finding that would change with the LOTTERY points removed; and the route. `render` writes
the report as Markdown; nothing in the rendering is computed there.

Every judgement applied here is data in the spec, never a constant in code.
"""

import concurrent.futures
import csv
import gzip
import hashlib
import itertools
import json
import multiprocessing
import pathlib
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Optional

import jsonschema
import yaml

from . import aggregates as agg
from . import guards, manifests, runner, scorer, scoring
from .outputs import write_csv

HARNESS = pathlib.Path(__file__).resolve().parents[2]
REPO = HARNESS.parent
EXPERIMENTS = HARNESS / "experiments"
SEARCH_SCHEMA = EXPERIMENTS / "schema" / "search-spec.schema.json"
REPORT_SCHEMA = EXPERIMENTS / "schema" / "search-report.schema.json"
BOOT_SCHEMA = HARNESS / "boot-defaults" / "schema" / "boot-default.schema.json"
WAIT_CHECK = REPO / "simulator" / "tools"

PINS = ("dataset", "driver_table", "scoring_spec", "guard_spec")
FINDINGS = {1: "no spread", 2: "spread the prior table's row holds", 3: "spread the prior table missed"}
POINT_COLUMNS = ("workload_id", "point", "order", "algorithm", "batch_bandwidth_cap", "params", "read", "out",
                 "entity", "metric", "aggregate", "direction", "weight", "value", "censored", "improvement",
                 "reading", "against_floor", "quantity")
WAIT_COLUMNS = ("workload_id", "point", "longest_us", "kind", "task", "ready_done_us", "preempt_done_us",
                "ready_open_us", "preempt_open_us", "over")
PLACES = scorer.PLACES


class SearchError(ValueError):
    """A refusal: the spec is not legal, the inputs are not the pinned ones, or a check did not reproduce its run."""


def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_search_spec(doc) -> bool:
    return isinstance(doc, dict) and "search" in doc


def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt(x) -> str:
    return scorer.fmt(x)


# ------------------------------------------------------------------ the grid

@dataclass(frozen=True)
class Point:
    id: str
    order: int                  # its place in the grid's order (the best point's tie rule)
    config: dict                # {algorithm, params, batch_bandwidth_cap}, as the daemon composes a row

    @property
    def key(self) -> str:
        return config_key(self.config)


def config_key(config) -> str:
    """A configuration's canonical bytes — the daemon's and the harness's `compose` spelling (data-contracts §10)."""
    return json.dumps({"algorithm": config["algorithm"], "params": config.get("params") or {},
                       "batch_bandwidth_cap": config.get("batch_bandwidth_cap")},
                      sort_keys=True, separators=(",", ":"))


def canonical(config) -> dict:
    return json.loads(config_key(config))


def _num(x) -> str:
    return "none" if x is None else (str(x) if not isinstance(x, float) or not x.is_integer() else str(int(x)))


def point_id(config) -> str:
    """A point's name, from its configuration alone; also the stem of its table (`<role>@<point>`)."""
    a, p, cap = config["algorithm"], config.get("params") or {}, _num(config.get("batch_bandwidth_cap"))
    if a == "MLFQ":
        return (f"mlfq-s{p['timeslice_us']}-b{p['boost_interval_us']}-q{p['num_queues']}"
                f"-x{_num(p['timeslice_growth'])}-c{cap}")
    if a == "EDF":
        return f"edf-s{p['residual_timeslice_us']}-c{cap}"
    if a == "LOTTERY":
        return f"lottery-s{p['timeslice_us']}-w{_num(p['batch_share'])}-c{cap}"
    if a == "FIFO":
        return f"fifo-c{cap}"
    raise SearchError(f"unknown algorithm {a!r}")


def expand_grid(grid) -> List[Point]:
    """The grid's points in its order: per block, the product of its `cross` axes (the first axis slowest), each
    combination once per entry of `with`; `batch_bandwidth_cap` is the cap, every other key a param."""
    points = []
    for block in grid["blocks"]:
        axes = block.get("cross") or {}
        names = list(axes)
        for combo in itertools.product(*[axes[n] for n in names]):
            for extra in block.get("with") or [{}]:
                values = dict(zip(names, combo))
                values.update(extra)
                cap = values.pop("batch_bandwidth_cap", None)
                config = canonical({"algorithm": block["algorithm"], "params": values, "batch_bandwidth_cap": cap})
                points.append(Point(point_id(config), len(points), config))
    return points


def point_table(prior_doc, config) -> dict:
    """The table whose every row is `config`: the prior table's (mode, background_wanted) pairs and its role, each
    row's cap, default algorithm and that entry's params the point's. The daemon composes every row to `config`."""
    algorithm = config["algorithm"]
    rows = [{"mode": r["mode"], "background_wanted": r["background_wanted"],
             "batch_bandwidth_cap": config.get("batch_bandwidth_cap"), "default": algorithm,
             "entries": {algorithm: {"params": dict(config.get("params") or {})}}}
            for r in prior_doc["rows"]]
    return {"role": prior_doc.get("role", ""), "rows": rows}


def prior_configs(prior_doc) -> List[str]:
    """The prior table's distinct configurations, as canonical bytes, in the order of their first row."""
    out = []
    for r in prior_doc["rows"]:
        k = config_key({"algorithm": r["default"], "params": r["entries"][r["default"]]["params"],
                        "batch_bandwidth_cap": r["batch_bandwidth_cap"]})
        if k not in out:
            out.append(k)
    return out


def row_config(workload_path, prior_doc) -> List[str]:
    """The configurations the oracle applies on the file: the prior table's row of each ground-truth segment that
    carries `background_wanted` (the daemon's `recognize_oracle`), as canonical bytes."""
    with open(workload_path, "r", encoding="utf-8") as f:
        segments = json.load(f).get("ground_truth") or []
    rows = {(r["mode"], bool(r["background_wanted"])): r for r in prior_doc["rows"]}
    out = []
    for s in segments:
        attrs = s.get("attributes") or {}
        if "background_wanted" not in attrs:
            continue
        r = rows.get((s["mode"], bool(attrs["background_wanted"])))
        if r is None:
            continue
        k = config_key({"algorithm": r["default"], "params": r["entries"][r["default"]]["params"],
                        "batch_bandwidth_cap": r["batch_bandwidth_cap"]})
        if k not in out:
            out.append(k)
    return out


# ------------------------------------------------------------------ the lint

@dataclass
class Plan:
    """What a legal spec expands to: the points, each file's row and compiled path, the boot defaults as points."""
    spec: dict
    points: List[Point]
    by_key: Dict[str, Point]
    files: List[str]
    workloads: Dict[str, pathlib.Path]
    rows: Dict[str, str]                     # workload -> the row's point id
    fixed: str                               # the primary boot default's point id
    alternatives: Dict[str, str]             # alternative stem -> its point id
    prior: List[str]                         # the prior table's distinct configurations' point ids
    prior_doc: dict
    scoring_spec: dict


def _schema_errors(spec):
    validator = jsonschema.Draft202012Validator(json.loads(SEARCH_SCHEMA.read_text()))
    out = []
    for err in sorted(validator.iter_errors(spec), key=lambda e: [str(p) for p in e.absolute_path]):
        where = "/".join(str(p) for p in err.absolute_path)
        out.append(f"{where + ': ' if where else ''}{err.message}")
    return out


def _pin_errors(spec, root):
    errors = []
    pins = spec.get("pins") or {}
    for name in PINS:
        pin = pins.get(name) or {}
        path = pathlib.Path(root) / str(pin.get("path", ""))
        if not path.is_file():
            errors.append(f"pins/{name}: {pin.get('path')!r} is not a file under {root}")
            continue
        actual = _sha256(path)
        if actual != pin.get("sha256"):
            errors.append(f"pins/{name}: sha256 {actual} of {pin.get('path')} != pinned {pin.get('sha256')}")
    guard_pin = pins.get("guard_spec") or {}
    gpath = pathlib.Path(root) / str(guard_pin.get("path", ""))
    if gpath.is_file() and "version" in guard_pin:
        version = str((yaml.safe_load(gpath.read_text()) or {}).get("version"))
        if version != str(guard_pin["version"]):
            errors.append(f"pins/guard_spec: version {version!r} != pinned {guard_pin['version']!r}")
    return errors


def plan(spec, root, build_dir, boot_defaults_dir=None) -> Plan:
    """The spec expanded, or a `SearchError` naming every problem (`lint_spec` returns them as a list)."""
    errors = lint_spec(spec, root, build_dir, boot_defaults_dir)
    if errors:
        raise SearchError("; ".join(errors))
    return _plan(spec, pathlib.Path(root), pathlib.Path(build_dir),
                 pathlib.Path(boot_defaults_dir) if boot_defaults_dir else pathlib.Path(root) / "harness" / "boot-defaults")


def _plan(spec, root, build_dir, boot_dir) -> Plan:
    points = expand_grid(spec["grid"])
    by_key = {p.key: p for p in points}
    prior_doc = yaml.safe_load((root / spec["pins"]["driver_table"]["path"]).read_text())
    files = [f["workload"] for f in spec["files"]]
    workloads = {w: build_dir / f"{w}.workload.json" for w in files}
    boot = lambda stem: config_key(json.loads((boot_dir / f"{stem}.json").read_text()))   # noqa: E731
    rows = {}
    for w in files:
        keys = row_config(workloads[w], prior_doc)
        rows[w] = by_key[keys[0]].id
    return Plan(spec=spec, points=points, by_key=by_key, files=files, workloads=workloads, rows=rows,
                fixed=by_key[boot(spec["boot_defaults"]["primary"])].id,
                alternatives={s: by_key[boot(s)].id for s in spec["boot_defaults"]["alternatives"]},
                prior=[by_key[k].id for k in prior_configs(prior_doc)], prior_doc=prior_doc,
                scoring_spec=scoring.load_spec(root / spec["pins"]["scoring_spec"]["path"]))


def lint_spec(spec, root, build_dir, boot_defaults_dir=None) -> List[str]:
    """Every problem with a search spec (a dict, or a path to one), as strings; empty means legal."""
    if not isinstance(spec, dict):
        spec = load_spec(spec)
    root, build_dir = pathlib.Path(root), pathlib.Path(build_dir)
    boot_dir = pathlib.Path(boot_defaults_dir) if boot_defaults_dir else root / "harness" / "boot-defaults"
    errors = _schema_errors(spec)
    if errors:
        return errors
    errors += _pin_errors(spec, root)
    scoring_path = root / spec["pins"]["scoring_spec"]["path"]
    table_path = root / spec["pins"]["driver_table"]["path"]
    if not scoring_path.is_file() or not table_path.is_file():
        return errors
    scoring_spec = scoring.load_spec(scoring_path)
    prior_doc = yaml.safe_load(table_path.read_text())

    files = [f["workload"] for f in spec["files"]]
    if len(set(files)) != len(files):
        errors.append("files: a workload listed twice")
    for w in files:
        if not (build_dir / f"{w}.workload.json").is_file():
            errors.append(f"files: {w} is not in the build {build_dir}")
        if not ((scoring_spec.get("files") or {}).get(w) or {}).get("terms"):
            errors.append(f"files: {w} has no scoring terms in {spec['pins']['scoring_spec']['path']}")
    for w in sorted(set(files) - set((spec.get("checks") or {}).get("runs") or {})):
        errors.append(f"checks/runs: no reference runs for {w}")
    if not prior_doc.get("role"):
        errors.append(f"pins/driver_table: {spec['pins']['driver_table']['path']} has no role to label the points' "
                      "tables with")

    points = expand_grid(spec["grid"])
    by_key = {}
    boot_validator = jsonschema.Draft202012Validator(json.loads(BOOT_SCHEMA.read_text()))
    counts = {}
    for p in points:
        counts[p.config["algorithm"]] = counts.get(p.config["algorithm"], 0) + 1
        bad = jsonschema.exceptions.best_match(boot_validator.iter_errors(p.config))
        if bad is not None:
            errors.append(f"grid: point {p.id} is not a legal configuration: {bad.message}")
        if p.key in by_key:
            errors.append(f"grid: point {p.id} appears twice")
        by_key[p.key] = p
    if len(points) != spec["grid"]["points"]:
        errors.append(f"grid: the blocks expand to {len(points)} points "
                      f"({', '.join(f'{a} {n}' for a, n in counts.items())}), the spec states {spec['grid']['points']}")
    stems = [spec["boot_defaults"]["primary"]] + list(spec["boot_defaults"]["alternatives"])
    for stem in stems:
        path = boot_dir / f"{stem}.json"
        if not path.is_file():
            errors.append(f"boot_defaults: no boot-default file {path}")
        elif config_key(json.loads(path.read_text())) not in by_key:
            errors.append(f"grid: the boot default {stem} is not a point")
    for k in prior_configs(prior_doc):
        if k not in by_key:
            errors.append(f"grid: the prior table's configuration {k} is not a point")
    for w in files:
        path = build_dir / f"{w}.workload.json"
        if not path.is_file():
            continue
        keys = row_config(path, prior_doc)
        if len(keys) != 1:
            errors.append(f"files: the oracle applies {len(keys)} configurations on {w}; a point replaces one row")
        elif keys[0] not in by_key:
            errors.append(f"grid: {w}'s row {keys[0]} is not a point")
    return errors


# ------------------------------------------------------------------ the runs

@dataclass
class SearchContext:
    """What a worker reads beyond its run — sent once to each worker process."""
    run_ctx: runner.RunContext
    guard_spec: dict
    t_ends: Dict[str, int]
    wait_floor: int


def _wait_check():
    if str(WAIT_CHECK) not in sys.path:
        sys.path.insert(0, str(WAIT_CHECK))
    import wait_check                                     # noqa: E402  simulator/tools/wait_check.py
    return wait_check


def wait_reading(trace_gz, t_end, floor) -> dict:
    """`wait_check.py`'s four readings of one trace and the longest of them, `over` when it exceeds the floor."""
    with gzip.open(trace_gz, "rb") as f:
        r = _wait_check().waits(f, t_end, floor)
    four = {"ready_done": r["ready_done"], "preempt_done": r["preempt_done"],
            "ready_open": r["ready_open"], "preempt_open": r["preempt_open"]}
    kind, worst = max(four.items(), key=lambda kv: kv[1][0])
    return {"longest_us": int(worst[0]), "kind": kind, "task": worst[1],
            **{f"{k}_us": int(v[0]) for k, v in four.items()}, "over": int(worst[0] > floor)}


def point_run(plan_: Plan, wid: str, point_id_: str, machine: runner.Machine, tables_dir: pathlib.Path
              ) -> runner.RunSpec:
    """The point's run on one file: the spec's condition under the point's table, labelled `<role>@<point>`."""
    spec = plan_.spec
    return runner.RunSpec(workload_id=wid, condition=spec["point"]["condition"],
                          table=f"{plan_.prior_doc['role']}@{point_id_}", seed="", boot_default="",
                          boot_file=machine.boot_defaults_dir / f"{spec['boot_defaults']['primary']}.json",
                          workload_file=plan_.workloads[wid], telemetry=spec["point"]["telemetry"],
                          table_file=tables_dir / f"{point_id_}.yaml")


def point_of(run: runner.RunSpec) -> str:
    return run.table_stem


def _guard_run(run: runner.RunSpec, run_dir: pathlib.Path, messages) -> guards.Run:
    return guards.Run(workload_id=run.workload_id, condition=run.condition, table=run.table, seed=run.seed,
                      boot_default=run.boot_default, records=run_dir / "records.csv.gz",
                      schedule=run_dir / "schedule.json", log=run_dir / "log.json", workload=run.workload_file,
                      rerun_trace=run_dir / "trace.rerun.sha256", guard_messages=messages,
                      trace=run_dir / "trace.jsonl.gz", telemetry=run.telemetry)


def term_values(agg_rows, terms, who) -> List[dict]:
    """Each scored term's value in one run's aggregates, as the scorer reads it (`scorer._lookup`: the censored
    bound for an unfinished turnaround, the censored mark for a latency term with an unserved wake)."""
    index = scorer._runs(agg_rows)
    if len(index) != 1:
        raise SearchError(f"{who}: aggregates of {len(index)} runs where one was expected")
    run = next(iter(index.values()))
    out = []
    for term in terms:
        tk = scorer._term_key(term)
        value, censored = scorer._lookup(run, tk, who)
        out.append({"entity": tk[0], "metric": tk[1], "aggregate": tk[2], "direction": term["direction"],
                    "weight": fmt(Fraction(str(term["weight"]))), "value": fmt(value), "censored": int(censored)})
    return out


_CTX: Optional[SearchContext] = None


def _init_worker(ctx: SearchContext):
    global _CTX
    _CTX = ctx


def _work(run: runner.RunSpec) -> dict:
    return work(run, _CTX)


def work(run: runner.RunSpec, ctx: SearchContext) -> dict:
    """One point on one file: the runner's `process_run`, the guards on it, the wait check on its trace, the scored
    terms' values. Returns the run's outcome without its aggregate rows (they stay in its results-cache entry)."""
    out = runner.process_run(run, ctx.run_ctx)
    if "failure" in out:
        return out
    run_dir = ctx.run_ctx.exp_dir / run.workload_id / run.name
    rows = out.pop("aggregates")
    gr = _guard_run(run, run_dir, out["messages"])
    out["guards"] = guards.evaluate([gr], ctx.guard_spec, rows, ctx.run_ctx.scoring_spec)
    out["waits"] = wait_reading(run_dir / "trace.jsonl.gz", ctx.t_ends[run.workload_id], ctx.wait_floor)
    terms = ctx.run_ctx.scoring_spec["files"][run.workload_id]["terms"]
    out["terms"] = term_values(rows, terms, f"{run.workload_id}/{run.name}")
    out.pop("grade_rows", None)
    with open(run_dir / "trace.rerun.sha256") as f:
        out["trace_sha256"] = f.read().split()[0]
    return out


def run_all(runs, ctx: SearchContext, progress=None):
    """Every run's `work`, as (run, outcome) pairs in the order they finish — `runner.run_all`'s two pools: the runs
    on files under `heavy_mb` in `workers` processes, the rest in `heavy_workers` fresh processes, largest first."""
    machine = ctx.run_ctx.machine
    total = len(runs)
    if machine.workers <= 1:
        for k, run in enumerate(runs, 1):
            out = work(run, ctx)
            if progress:
                progress(k, total, run, out)
            yield run, out
        return
    by_size = sorted(runs, key=lambda r: -r.workload_file.stat().st_size)
    heavy = [r for r in by_size if runner.is_heavy(r, machine)]
    light = [r for r in by_size if not runner.is_heavy(r, machine)]
    spawn = multiprocessing.get_context("spawn")
    pools = [concurrent.futures.ProcessPoolExecutor(max_workers=machine.workers, mp_context=spawn,
                                                    initializer=_init_worker, initargs=(ctx,))]
    if heavy:
        pools.append(concurrent.futures.ProcessPoolExecutor(max_workers=max(1, machine.heavy_workers),
                                                            mp_context=spawn, initializer=_init_worker,
                                                            initargs=(ctx,), max_tasks_per_child=1))
    try:
        futures = {pools[0].submit(_work, r): r for r in light}
        futures.update({pools[-1].submit(_work, r): r for r in heavy})
        for k, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            run, out = futures[fut], fut.result()
            if progress:
                progress(k, total, run, out)
            yield run, out
    finally:
        for pool in pools:
            pool.shutdown(wait=True, cancel_futures=True)


# ------------------------------------------------------------------ the checks

def _lines(trace_gz, set_aside, boosts_at=()):
    """The trace's lines but those whose event is in `set_aside` (`meta` the header), and the `x_mlfq_boost` lines
    at the instants in `boosts_at`."""
    marks = tuple(f'{{"event":"{e}"'.encode() for e in set_aside)
    boosts = {f'{{"event":"x_mlfq_boost","t":{t}}}'.encode() for t in boosts_at}
    with gzip.open(trace_gz, "rb") as f:
        for line in f:
            if not line.startswith(marks) and line.rstrip(b"\n") not in boosts:
                yield line


def applied_after_boot(trace_gz) -> List[int]:
    """The instants of the trace's applied schedule entries after the boot entry (`config_applied`, index ≥ 1),
    t > 0: where an applied MLFQ entry restarts the boost timer (metrics doc §11 item 9)."""
    out = []
    with gzip.open(trace_gz, "rb") as f:
        for line in f:
            if line.startswith(b'{"event":"config_applied"'):
                e = json.loads(line)
                if e["index"] >= 1 and e["t"] > 0:
                    out.append(int(e["t"]))
    return out


def compare_lines(a_gz, b_gz, set_aside, boosts_at=()) -> dict:
    """Two traces line by line, the `set_aside` events and the boosts at `boosts_at` left out of both: the count
    compared, the first line that differs and the number of lines each holds."""
    n = 0
    first = None
    a_n = b_n = 0
    for x, y in itertools.zip_longest(_lines(a_gz, set_aside, boosts_at), _lines(b_gz, set_aside, boosts_at)):
        a_n += x is not None
        b_n += y is not None
        if x != y and first is None:
            first = {"line": n + 1, "point": (x or b"").decode().strip(), "reference": (y or b"").decode().strip()}
        n += 1
    return {"equal": first is None, "lines_point": a_n, "lines_reference": b_n, "first_difference": first}


def _gz_sha256(path) -> str:
    h = hashlib.sha256()
    with gzip.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _reference_scores(spec, root, wid, run_path):
    """The corrected run's scored terms' values from its experiment's scores file: `value_fixed` and `value_oracle`
    of the term rows on the primary boot default and table, by (entity, metric, aggregate)."""
    exp = str(pathlib.PurePosixPath(run_path).parent.parent)
    scores = pathlib.Path(root) / spec["checks"]["scores"][exp]
    out = {}
    with open(scores, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r["workload_id"] == wid and r["level"] == "term" and r["condition"] == "oracle"
                    and not r["boot_default"] and r["table"] == "prior"):
                out[(r["entity"], r["metric"], r["aggregate"])] = (r["value_fixed"], r["value_oracle"])
    return out


def check_runs(plan_: Plan, outcomes: Dict[tuple, dict], exp_dir, root) -> List[dict]:
    """Decision 10's two checks per file, from the boot default's and the row's point runs (`outcomes` by
    (workload, point)): the row's trace byte-identical to the corrected oracle run's; the boot default's trace the
    same lines as the corrected fixed run's but those `set_aside`, and both points' scored terms the corrected run's
    scores. Each reference trace is first checked against the hash the spec pins."""
    spec, root, exp_dir = plan_.spec, pathlib.Path(root), pathlib.Path(exp_dir)
    set_aside = spec["checks"]["set_aside"]
    rows = []
    for wid in plan_.files:
        ref = spec["checks"]["runs"][wid]
        scores = _reference_scores(spec, root, wid, ref["oracle"]["run"])
        for which, pid, col in (("fixed", plan_.fixed, 0), ("oracle", plan_.rows[wid], 1)):
            out = outcomes[(wid, pid)]
            ref_trace = root / ref[which]["run"] / "trace.jsonl.gz"
            ref_sha = _gz_sha256(ref_trace)
            row = {"workload_id": wid, "check": which, "point": pid, "reference": ref[which]["run"],
                   "reference_trace_sha256": ref_sha, "reference_pinned": ref_sha == ref[which]["trace_sha256"],
                   "point_trace_sha256": out["trace_sha256"]}
            if which == "oracle":
                row["trace_equal"] = out["trace_sha256"] == ref[which]["trace_sha256"]
            else:
                trace = exp_dir / wid / point_run_name(plan_, pid) / "trace.jsonl.gz"
                boosts = applied_after_boot(trace) if spec["checks"].get("restarted_boost") else []
                row["lines"] = compare_lines(trace, ref_trace, set_aside, boosts)
                row["restarted_boosts_set_aside"] = boosts
                row["trace_equal"] = row["lines"]["equal"]
            terms = []
            for t in out["terms"]:
                want = scores.get((t["entity"], t["metric"], t["aggregate"]))
                got = fmt(Fraction(t["value"]))
                terms.append({"entity": t["entity"], "metric": t["metric"], "aggregate": t["aggregate"],
                              "point": got, "reference": None if want is None else want[col],
                              "equal": want is not None and want[col] == got})
            row["terms"] = terms
            row["reproduced"] = bool(row["reference_pinned"] and row["trace_equal"] and all(t["equal"] for t in terms))
            rows.append(row)
    return rows


def point_run_name(plan_: Plan, pid: str) -> str:
    """The point's run directory's name, `runner.RunSpec.name` of `point_run`."""
    return f"{plan_.spec['point']['condition']}@{pid}~{plan_.spec['point']['telemetry']}"


# ------------------------------------------------------------------ the reading

def floors_of(spec) -> Dict[str, Fraction]:
    f = spec["reading"]["floors"]
    return scorer.floors_for(Fraction(str(f["latency_us"])), Fraction(str(f["fraction"])))


def _improve(direction, base, value):
    return base - value if direction == "lower" else value - base


def term_reading(direction, fixed, value, floor):
    """(improvement, reading, against the floor) of one term at one point: the improvement over fixed, divided by
    fixed's value — signed, zero when the improvement is under the floor."""
    imp = _improve(direction, fixed, value)
    if abs(imp) < floor:
        return imp, Fraction(0), "under"
    if fixed == 0:
        raise SearchError(f"an improvement of {fmt(imp)} over a fixed value of 0 has no reading as a fraction")
    return imp, imp / fixed, "better" if imp > 0 else "worse"


def quantity(terms, fixed_values, values, floors):
    """(the point's quantity, per-term readings): the readings weighted over the file's terms by their weights."""
    total = wsum = Fraction(0)
    readings = []
    for t, f, v in zip(terms, fixed_values, values):
        imp, r, against = term_reading(t["direction"], f, v, floors[t["aggregate"]])
        w = Fraction(t["weight"])
        total += w * r
        wsum += w
        readings.append({"improvement": imp, "reading": r, "against_floor": against})
    return total / wsum, readings


def find(values: Dict[str, List[Fraction]], order: Dict[str, int], terms, row: str, fixed: str, g: Fraction,
         floors) -> dict:
    """A file's finding over its read points (`values`: point → the scored terms' values, in the terms' order),
    with `fixed` in place of fixed and `row` the configuration the oracle applies."""
    q = {pid: quantity(terms, values[fixed], v, floors)[0] for pid, v in values.items()}
    spread = []
    for i, t in enumerate(terms):
        col = [v[i] for v in values.values()]
        spread.append({"entity": t["entity"], "metric": t["metric"], "aggregate": t["aggregate"],
                       "min": min(col), "max": max(col), "range": max(col) - min(col),
                       "floor": floors[t["aggregate"]]})
    no_spread = all(s["range"] < s["floor"] for s in spread)
    best_q = max(q.values())
    tied = sorted((pid for pid, x in q.items() if x == best_q), key=lambda p: order[p])
    best = row if row in tied else tied[0]
    better = [t["entity"] for i, t in enumerate(terms)
              if _improve(t["direction"], values[row][i], values[best][i]) >= floors[t["aggregate"]]]
    missed = q[row] <= (1 - g) * best_q and bool(better)
    finding = 1 if no_spread else (3 if missed else 2)
    return {"finding": finding, "quantity": q, "best": best, "best_quantity": best_q, "tied": tied,
            "row_quantity": q[row], "best_better_on": better, "spread": spread}


def _range(findings) -> str:
    got = sorted({f for f in findings if f is not None})
    return "–".join(str(x) for x in (got[:1] + got[-1:] if len(got) > 1 else got)) if got else ""


def read_file(wid, points: Dict[str, dict], plan_: Plan) -> dict:
    """One file's reading from its points' outcomes (`points`: point → {terms, out}); see `find`."""
    spec = plan_.spec
    floors = floors_of(spec)
    terms = spec_terms(plan_, wid)
    order = {p.id: p.order for p in plan_.points}
    algo = {p.id: p.config["algorithm"] for p in plan_.points}
    read = {pid: [Fraction(t["value"]) for t in o["terms"]] for pid, o in points.items() if not o["out"]}
    out = [{"point": pid, "failed": o["out"]} for pid, o in sorted(points.items(), key=lambda kv: order[kv[0]])
           if o["out"]]
    row, fixed = plan_.rows[wid], plan_.fixed
    g = Fraction(str(spec["reading"]["g"]))
    result = {"workload_id": wid, "row": row, "fixed": fixed, "points": len(points), "read": len(read), "out": out}
    for need, what in ((row, "the row's point"), (fixed, "the boot default's point")):
        if need not in read:
            result.update({"finding": None, "no_reading": f"{what} {need} is out of the reading"})
            return result

    def finding_or_none(kept, base, gv):
        try:
            return find(kept, order, terms, row, base, gv, floors)["finding"], ""
        except SearchError as exc:          # fixed's value 0 on a term some point moves past the floor
            return None, str(exc)
    try:
        primary = find(read, order, terms, row, fixed, g, floors)
    except SearchError as exc:
        result.update({"finding": None, "no_reading": str(exc)})
        return result
    result.update({"finding": primary["finding"], "finding_name": FINDINGS[primary["finding"]],
                   "row_quantity": fmt(primary["row_quantity"]), "best": primary["best"],
                   "best_quantity": fmt(primary["best_quantity"]), "tied": primary["tied"],
                   "best_better_on": primary["best_better_on"],
                   "best_terms": [{"entity": t["entity"], "value": fmt(read[primary["best"]][i]),
                                   "row": fmt(read[row][i]), "fixed": fmt(read[fixed][i])}
                                  for i, t in enumerate(terms)],
                   "spread": [{**s, **{k: fmt(s[k]) for k in ("min", "max", "range", "floor")}}
                              for s in primary["spread"]]})
    if primary["finding"] == 2:
        prior_read = [p for p in plan_.prior if p in read]
        result["prior_at_least_row"] = sum(1 for p in prior_read if primary["quantity"][p] >= primary["row_quantity"])
        result["prior_read"] = len(prior_read)
    band = {}
    for gb in spec["reading"]["g_band"]:
        band[str(gb)] = finding_or_none(read, fixed, Fraction(str(gb)))[0]
    result["g_band"] = band
    result["g_range"] = _range(list(band.values()) + [primary["finding"]])
    boots = {spec["boot_defaults"]["primary"]: {"point": fixed, "finding": primary["finding"]}}
    for stem, pid in plan_.alternatives.items():
        if pid not in read:
            boots[stem] = {"point": pid, "finding": None, "no_reading": "the point is out of the reading"}
        else:
            f, why = finding_or_none(read, pid, g)
            boots[stem] = {"point": pid, "finding": f, **({"no_reading": why} if why else {})}
    result["boot_defaults"] = boots
    result["boot_range"] = _range(b["finding"] for b in boots.values())
    if spec["reading"].get("lottery_flag"):
        kept = {pid: v for pid, v in read.items() if algo[pid] != "LOTTERY" or pid == row}
        without = finding_or_none(kept, fixed, g)[0]
        changes = {"primary": without} if without != primary["finding"] else {}
        for gb in spec["reading"]["g_band"]:
            f = finding_or_none(kept, fixed, Fraction(str(gb)))[0]
            if f != band[str(gb)]:
                changes[f"g {gb}"] = f
        for stem, b in boots.items():
            if b["finding"] is None or b["point"] not in kept:
                continue
            f = finding_or_none(kept, b["point"], g)[0]
            if f != b["finding"]:
                changes[stem] = f
        result["lottery"] = {"removed": sum(1 for pid in read if pid not in kept), "finding_without": without,
                             "changes": changes}
    return result


def spec_terms(plan_: Plan, wid) -> List[dict]:
    return [{"entity": scorer._term_key(t)[0], "metric": t["metric"], "aggregate": scorer._term_key(t)[2],
             "direction": t["direction"], "weight": fmt(Fraction(str(t["weight"])))}
            for t in plan_.scoring_spec["files"][wid]["terms"]]


def route(files: List[dict], spec) -> dict:
    """The route over the files' findings: the table rewritten if any file is at finding 3, else workload
    redesign; under each g of the band and each boot default beside it."""
    r = spec["route"]

    def one(findings):
        if any(f == 3 for f in findings):
            return r["table_rewrite"]
        if any(f is None for f in findings):
            return None
        return r["workload_redesign"]
    out = {"route": one([f.get("finding") for f in files]),
           "files_at_3": [f["workload_id"] for f in files if f.get("finding") == 3],
           "g_band": {g: one([f.get("g_band", {}).get(str(g)) for f in files]) for g in spec["reading"]["g_band"]},
           "boot_defaults": {}}
    for stem in [spec["boot_defaults"]["primary"]] + list(spec["boot_defaults"]["alternatives"]):
        out["boot_defaults"][stem] = one([f.get("boot_defaults", {}).get(stem, {}).get("finding") for f in files])
    return out


def point_rows(plan_: Plan, wid, points: Dict[str, dict]) -> List[dict]:
    """The points file's rows for one file: per point and term, the value, its improvement over fixed, its reading
    against the floor, and the point's quantity — fixed the boot default's point; empty readings for a point out
    of the reading, or for every point when the boot default's point is."""
    floors = floors_of(plan_.spec)
    terms = spec_terms(plan_, wid)
    pmap = {p.id: p for p in plan_.points}
    base = points.get(plan_.fixed)
    fixed_values = None if base is None or base["out"] else [Fraction(t["value"]) for t in base["terms"]]
    rows = []
    for pid, o in sorted(points.items(), key=lambda kv: pmap[kv[0]].order):
        p = pmap[pid]
        values = [Fraction(t["value"]) for t in o["terms"]]
        q = readings = None
        if fixed_values is not None and not o["out"]:
            try:
                q, readings = quantity(terms, fixed_values, values, floors)
            except SearchError:
                pass                        # fixed's value 0: the file's reading says so (`read_file`)
        for i, t in enumerate(o["terms"]):
            rows.append({"workload_id": wid, "point": pid, "order": p.order, "algorithm": p.config["algorithm"],
                         "batch_bandwidth_cap": "" if p.config["batch_bandwidth_cap"] is None
                         else p.config["batch_bandwidth_cap"],
                         "params": json.dumps(p.config["params"], sort_keys=True, separators=(",", ":")),
                         "read": int(not o["out"]), "out": "; ".join(o["out"]),
                         "entity": t["entity"], "metric": t["metric"], "aggregate": t["aggregate"],
                         "direction": t["direction"], "weight": t["weight"], "value": t["value"],
                         "censored": t["censored"],
                         "improvement": "" if readings is None else fmt(readings[i]["improvement"]),
                         "reading": "" if readings is None else fmt(readings[i]["reading"]),
                         "against_floor": "" if readings is None else readings[i]["against_floor"],
                         "quantity": "" if q is None else fmt(q)})
    return rows


def out_reasons(outcome: dict, spec) -> List[str]:
    """What took a point out of the reading: each failed guard, and a wait over the spec's bound."""
    rule = spec["reading"]["out_of_reading"]
    reasons = []
    if rule.get("guards"):
        for g in outcome["guards"]:
            if g["result"] == "fail":
                reasons.append(f"{g['guard']}: {g['reason']}")
    w = outcome["waits"]
    if w["longest_us"] > int(rule["longest_wait_us"]):
        reasons.append(f"wait_check: {w['task']} waited {w['longest_us']} µs ({w['kind']})")
    return reasons


# ------------------------------------------------------------------ the search

@dataclass
class Result:
    report: Optional[dict] = None
    checks: List[dict] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    stopped: Optional[str] = None
    exp_dir: Optional[pathlib.Path] = None


def search(spec_path, machine: runner.Machine, root, progress=None, only_checks=False) -> Result:
    """The search the spec names: the lint, the point tables, the checks' runs and the checks — stopping on a check
    that does not reproduce its run — then every point, the reading, and the report under the runs directory."""
    root = pathlib.Path(root)
    spec_path = pathlib.Path(spec_path)
    spec = load_spec(spec_path)
    refused = runner.program_pin_errors(spec, machine)
    if refused:
        raise SearchError("the spec's program pins do not match the machine configuration: " + "; ".join(refused))
    plan_ = plan(spec, root, machine.build_dir, machine.boot_defaults_dir)
    exp_dir = machine.runs_dir / spec["search"]
    tables_dir = exp_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    for p in plan_.points:
        path = tables_dir / f"{p.id}.yaml"
        text = (f"# the table of point {p.id}: every row the one configuration — generated by "
                f"harness/tools/harness/search.py from {spec_path.name}, never committed\n"
                + yaml.safe_dump(point_table(plan_.prior_doc, p.config), sort_keys=False))
        if not path.is_file() or path.read_text() != text:
            path.write_text(text)
    pins = spec["pins"]
    run_ctx = runner.RunContext(machine=machine, exp_dir=exp_dir, table_path=root / pins["driver_table"]["path"],
                                scoring_spec=plan_.scoring_spec, harness=runner.harness_version())
    wc = _wait_check()
    ctx = SearchContext(run_ctx=run_ctx, guard_spec=guards.load_spec(root / pins["guard_spec"]["path"]),
                        t_ends={w: wc.t_end_of(str(plan_.workloads[w])) for w in plan_.files},
                        wait_floor=int(spec["reading"]["out_of_reading"]["longest_wait_us"]))
    result = Result(exp_dir=exp_dir)
    outcomes: Dict[tuple, dict] = {}
    times = []

    def go(runs):
        for run, out in run_all(runs, ctx, progress):
            if "failure" in out:
                result.failed.append(f"{run.workload_id}/{run.name}: {out['failure']}")
                continue
            outcomes[(run.workload_id, point_of(run))] = out
            times.append((run.workload_id, point_of(run), out["seconds"],
                          "cache" if out["results_cached"] else "built", round(out["peak_rss"] / (1 << 20)),
                          out["bytes"]))

    check_runs_ = [point_run(plan_, w, pid, machine, tables_dir)
                   for w in plan_.files for pid in (plan_.fixed, plan_.rows[w])]
    go(check_runs_)
    if result.failed:
        result.stopped = "a check's run failed"
        _write_failures(exp_dir, result)
        return result
    result.checks = check_runs(plan_, outcomes, exp_dir, root)
    (exp_dir / "checks.json").write_text(json.dumps(result.checks, indent=1, default=str) + "\n")
    bad = [f"{c['workload_id']}/{c['check']}" for c in result.checks if not c["reproduced"]]
    if bad:
        result.stopped = "the checks did not reproduce their runs: " + ", ".join(bad)
        return result
    if only_checks:
        return result
    done = set(outcomes)
    rest = [point_run(plan_, w, p.id, machine, tables_dir)
            for w in plan_.files for p in plan_.points if (w, p.id) not in done]
    go(rest)
    if result.failed:
        result.stopped = f"{len(result.failed)} run(s) failed"
        _write_failures(exp_dir, result)
        return result
    with open(exp_dir / "run-times.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["workload_id", "point", "seconds", "records", "peak_rss_mb", "bytes"])
        w.writerows(sorted(times))
    write_outputs(plan_, outcomes, exp_dir)
    result.report = read(spec_path, exp_dir, root, machine.build_dir, machine.boot_defaults_dir,
                         checks=result.checks)
    return result


def _write_failures(exp_dir, result):
    (exp_dir / "failures.json").write_text(json.dumps(result.failed, indent=1) + "\n")


def write_outputs(plan_: Plan, outcomes: Dict[tuple, dict], exp_dir):
    """The search's files under its runs directory: every run's aggregates (gzipped), the guards, the wait
    readings, and the points file the reading reads."""
    exp_dir = pathlib.Path(exp_dir)
    keys = sorted(outcomes, key=lambda k: (k[0], {p.id: p.order for p in plan_.points}[k[1]]))
    with gzip.open(exp_dir / "aggregates.csv.gz", "wt", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=agg.COLUMNS, lineterminator="\n")
        w.writeheader()
        for k in keys:
            for r in runner._aggregates_of(pathlib.Path(outcomes[k]["results_entry"])):
                w.writerow({c: ("" if r.get(c) is None else r.get(c, "")) for c in agg.COLUMNS})
    write_csv((g for k in keys for g in outcomes[k]["guards"]), guards.COLUMNS, exp_dir / "guards.csv")
    write_csv(({"workload_id": k[0], "point": k[1], **outcomes[k]["waits"]} for k in keys), WAIT_COLUMNS,
              exp_dir / "waits.csv")
    points = {}
    for k in keys:
        o = outcomes[k]
        points.setdefault(k[0], {})[k[1]] = {"terms": o["terms"], "out": out_reasons(o, plan_.spec)}
    rows = [r for wid in plan_.files for r in point_rows(plan_, wid, points.get(wid, {}))]
    write_csv(rows, POINT_COLUMNS, exp_dir / "points.csv")


def read_points(path) -> Dict[str, Dict[str, dict]]:
    """The points file back as {workload: {point: {terms, out}}}."""
    out: Dict[str, Dict[str, dict]] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            p = out.setdefault(r["workload_id"], {}).setdefault(
                r["point"], {"terms": [], "out": [x for x in r["out"].split("; ") if x]})
            p["terms"].append({k: r[k] for k in ("entity", "metric", "aggregate", "direction", "weight", "value")}
                              | {"censored": int(r["censored"])})
    return out


def read(spec_path, exp_dir, root, build_dir, boot_defaults_dir=None, checks=None) -> dict:
    """The report from the search's points file (`write_outputs`) — re-readable without a run."""
    spec_path, exp_dir = pathlib.Path(spec_path), pathlib.Path(exp_dir)
    spec = load_spec(spec_path)
    plan_ = plan(spec, root, build_dir, boot_defaults_dir)
    if checks is None and (exp_dir / "checks.json").is_file():
        checks = json.loads((exp_dir / "checks.json").read_text())
    points = read_points(exp_dir / "points.csv")
    missing = [f"{w}/{p.id}" for w in plan_.files for p in plan_.points if p.id not in points.get(w, {})]
    if missing:
        raise SearchError(f"{len(missing)} point(s) absent from the points file, the first {missing[0]}")
    files = []
    for f in spec["files"]:
        r = read_file(f["workload"], points[f["workload"]], plan_)
        r.update({"kind": f["kind"], "reason": f["reason"]})
        files.append(r)
    counts = {}
    for p in plan_.points:
        counts[p.config["algorithm"]] = counts.get(p.config["algorithm"], 0) + 1
    try:
        shown = spec_path.resolve().relative_to(pathlib.Path(root).resolve())
    except ValueError:
        shown = spec_path
    report = {"search": spec["search"], "spec": str(shown), "spec_sha256": _sha256(spec_path), "read": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
              "pins": spec["pins"], "points": len(plan_.points), "points_by_algorithm": counts,
              "files_searched": len(plan_.files), "runs": sum(len(v) for v in points.values()),
              "g": spec["reading"]["g"], "g_band": spec["reading"]["g_band"], "floors": spec["reading"]["floors"],
              "boot_default": {"primary": spec["boot_defaults"]["primary"], "point": plan_.fixed,
                               "alternatives": plan_.alternatives},
              "prior_configurations": plan_.prior, "checks": checks or [], "files": files,
              "route": route(files, spec), "statements": spec.get("statements") or []}
    validate_report(report)
    return report


def validate_report(report):
    validator = jsonschema.Draft202012Validator(json.loads(REPORT_SCHEMA.read_text()))
    error = jsonschema.exceptions.best_match(validator.iter_errors(json.loads(json.dumps(report, default=str))))
    if error is not None:
        raise SearchError(f"report: {error.message} at {'/'.join(str(p) for p in error.absolute_path)}")


def write_report(report, path):
    pathlib.Path(path).write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str) + "\n",
                                  encoding="utf-8")


# ------------------------------------------------------------------ the rendering

def _table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _f(x):
    return "no reading" if x is None else str(x)


def render(report) -> str:
    """The report as Markdown; every number is the JSON's."""
    r = report["route"]
    lines = [f"# {report['search']} — report", "",
             f"Search spec `{report['spec']}`, SHA-256 `{report['spec_sha256']}`; read {report['read']}. "
             f"{report['points']} configurations ({', '.join(f'{a} {n}' for a, n in report['points_by_algorithm'].items())}) "
             f"on {report['files_searched']} files, {report['runs']} runs; g = {report['g']}, the band "
             f"{', '.join(str(g) for g in report['g_band'])}; floors {report['floors']['latency_us']} µs and "
             f"{report['floors']['fraction']}. Fixed is the boot default's point `{report['boot_default']['point']}`.",
             "", f"**Route: {_f(r['route'])}.** Files at finding 3: "
             f"{', '.join(f'`{w}`' for w in r['files_at_3']) or 'none'}.", "",
             "## Findings", "",
             _table(["file", "kind", "finding", "under the g band", "under the boot defaults", "row's quantity",
                     "best point", "best's quantity", "out of the reading", "LOTTERY removed"],
                    [[f"`{f['workload_id']}`", f["kind"], _f(f.get("finding")), f.get("g_range", ""),
                      f.get("boot_range", ""), f.get("row_quantity", ""), f"`{f.get('best', '')}`",
                      f.get("best_quantity", ""), len(f["out"]),
                      ("changes: " + ", ".join(f"{k} → {v}" for k, v in f["lottery"]["changes"].items()))
                      if f.get("lottery", {}).get("changes") else "no change"]
                     for f in report["files"]]), ""]
    lines += ["Finding 1 — no spread; finding 2 — spread the prior table's row holds; finding 3 — spread the prior "
              "table missed.", ""]
    lines += ["## Checks", "",
              _table(["file", "check", "point", "reference", "pinned", "trace", "terms", "reproduced"],
                     [[f"`{c['workload_id']}`", c["check"], f"`{c['point']}`", f"`{c['reference']}`",
                       c["reference_pinned"], c["trace_equal"],
                       "; ".join(f"{t['entity']} {t['point']} / {t['reference']}" for t in c["terms"]),
                       c["reproduced"]] for c in report["checks"]]), ""]
    lines += ["## Route under the g band and the boot defaults", "",
              _table(["g", "route"], [[g, _f(v)] for g, v in r["g_band"].items()]), "",
              _table(["boot default", "route"], [[b, _f(v)] for b, v in r["boot_defaults"].items()]), ""]
    for f in report["files"]:
        lines += [f"## `{f['workload_id']}`", "", f"{f['kind']}: {f['reason']}. The row `{f['row']}`; "
                  f"{f['read']} of {f['points']} points read.", ""]
        if f.get("finding") is None:
            lines += [f"No reading: {f.get('no_reading')}.", ""]
        else:
            lines += [f"Finding {f['finding']} — {f['finding_name']}. The row's quantity {f['row_quantity']}; the "
                      f"best point `{f['best']}` at {f['best_quantity']}"
                      + (f", tied with {len(f['tied']) - 1} more" if len(f["tied"]) > 1 else "")
                      + (f"; better than the row by the floor or more on {', '.join(f['best_better_on'])}"
                         if f["best_better_on"] else "; better than the row by the floor on no term") + ".", ""]
            if "prior_at_least_row" in f:
                lines += [f"Of the prior table's {len(report['prior_configurations'])} distinct configurations, "
                          f"{f['prior_at_least_row']} of the {f['prior_read']} read have a quantity at least the "
                          f"row's.", ""]
            lines += [_table(["term", "fixed", "row", "best", "spread (min – max)", "floor"],
                             [[s["entity"], b["fixed"], b["row"], b["value"], f"{s['min']} – {s['max']}", s["floor"]]
                              for s, b in zip(f["spread"], f["best_terms"])]), ""]
            lines += [_table(["g"] + list(f["g_band"]), [["finding"] + [_f(v) for v in f["g_band"].values()]]), ""]
            lines += [_table(["boot default", "point", "finding"],
                             [[stem, f"`{b['point']}`", _f(b["finding"])] for stem, b in f["boot_defaults"].items()]),
                      ""]
            if "lottery" in f:
                lines += [f"With the {f['lottery']['removed']} LOTTERY points removed"
                          + (" (the row's own kept)" if f["row"].startswith("lottery") else "")
                          + f": finding {f['lottery']['finding_without']}"
                          + (f"; changes {f['lottery']['changes']}" if f["lottery"]["changes"] else "; no finding changes")
                          + ".", ""]
        if f["out"]:
            lines += [f"Out of the reading ({len(f['out'])}):", ""]
            lines += [f"- `{o['point']}` — {'; '.join(o['failed'])}" for o in f["out"]]
            lines += [""]
    lines += ["## Statements", ""]
    for s in report["statements"]:
        lines += [f"**{s['id']}.** {s['text'].strip()}", ""]
    return "\n".join(lines).rstrip() + "\n"


__all__ = ["Plan", "Point", "Result", "SearchError", "check_runs", "compare_lines", "config_key", "expand_grid",
           "find", "is_search_spec", "lint_spec", "load_spec", "plan", "point_id", "point_table", "quantity",
           "read", "read_file", "render", "route", "search", "term_reading", "validate_report", "write_report"]
