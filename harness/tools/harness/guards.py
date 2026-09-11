"""Guards — the checks that must pass before a run's numbers are read
(Phase 8 spec, decisions 6–7; sub-task 8.3 spec).

`harness/guards/guard-spec.yaml` lists the eight guards with their parameters
and groundings; each guard is a named function here, and the spec supplies
the threshold, the direction, and the conditions it applies to. `evaluate`
judges a whole run set at once — the two pair guards (determinism, c2_pair)
need a partner — and returns one row per (run, guard), dense, for the `guards`
file (`harness/guards/schema/guards.schema.json`): result `pass`, `fail`, or
`not_applicable`, the measured value, the threshold in force, the partner, and
a reason on fail. A guard whose input is missing fails: it has not cleared the
run. `not_applicable` is reserved for a run the guard's scope excludes by
construction (its condition is not in `applies_to`; a non-C2 file for the pair
check; a `fixed` run of a pair whose events differ).

Inputs per run (`Run`): its records file (identity and the trace hash), the
config schedule, the recognition log, the compiled workload (ground truth), an
optional rerun trace, the trace itself (the pair check hashes its body, header
left out, since the header names the workload), and the primitives' guard
messages the records build returned. The aggregates rows are passed once for the set. Exemptions are
per-experiment data (the RQ0 gate spec), never here.

`lint_spec` checks the spec against its schema, its ids against this module's
registry, every grounding non-empty, a threshold on every bounded guard, and
`pairs` against the dataset's C2 variant recipe.
"""

import hashlib
import json
import pathlib
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

import jsonschema
import yaml

from . import records as rec
from .aggregates import IDENTITY, fmt
from .reader import (LogError, ScheduleError, read_config_schedule,
                     read_recognition_log, RESERVED_ENTITIES)
from .scoring import variant_bases

HARNESS = pathlib.Path(__file__).resolve().parents[2]
SPEC_PATH = HARNESS / "guards" / "guard-spec.yaml"
SCHEMA_PATH = HARNESS / "guards" / "schema" / "guard-spec.schema.json"
GUARDS_SCHEMA = HARNESS / "guards" / "schema" / "guards.schema.json"

GUARDS = ("provenance_share", "config_age", "starvation_floor", "determinism",
          "utilisation_sanity", "tick_count", "validation_matches_provenance", "c2_pair")
COLUMNS = IDENTITY + ("guard", "result", "value", "threshold", "partner", "reason")
BOUNDED = ("below", "at_or_below")


@dataclass
class Run:
    """One run of the set: its identity and the paths the guards read."""
    workload_id: str
    condition: str
    table: str
    seed: str
    boot_default: str
    records: pathlib.Path
    schedule: Optional[pathlib.Path]
    log: Optional[pathlib.Path]
    workload: Optional[pathlib.Path]
    rerun_trace: Optional[pathlib.Path]
    guard_messages: Optional[List[str]]
    trace: Optional[pathlib.Path] = None      # the trace itself, for the pair check's body hash

    @property
    def identity(self):
        return (self.workload_id, self.condition, self.table, self.seed, self.boot_default)


class GuardError(ValueError):
    """The run set cannot be judged: a manifest or identity mistake, not a guard result."""


def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------------ results

def _pass(value=None, threshold=None, partner=""):
    return {"result": "pass", "value": value, "threshold": threshold, "partner": partner, "reason": ""}


def _fail(reason, value=None, threshold=None, partner=""):
    return {"result": "fail", "value": value, "threshold": threshold, "partner": partner, "reason": reason}


def _na():
    return {"result": "not_applicable", "value": None, "threshold": None, "partner": "", "reason": ""}


def _plain(d: Decimal) -> str:
    """A decimal string without trailing zeros, for reasons."""
    return format(d.normalize(), "f")


def _agg(ctx, entity, metric, aggregate):
    """The whole-file, unfiltered aggregate row, or None."""
    for r in ctx["aggregates"]:
        if (r["entity"] == entity and r["metric"] == metric and r["aggregate"] == aggregate
                and not r.get("cause") and not r.get("window_start_us") and not r.get("window_end_us")):
            return r
    return None


def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _body_sha256(path) -> str:
    """The trace's hash with its header line left out: the header names the
    workload, so two files' traces could never be byte-identical as wholes.
    The pair check compares what the simulator did, not what it was called."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        f.readline()
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------- guards

def provenance_share(run, ctx, params):
    row = _agg(ctx, "schedule", "config_interval", "fallback_share")
    threshold = fmt(params["threshold"])
    if row is None:
        return _fail("no fallback_share aggregate for the run", threshold=threshold)
    value = Decimal(row["value"])
    if value >= Decimal(threshold):
        return _fail(f"fallback + held share {_plain(value)} is not below {_plain(Decimal(threshold))}",
                     value=row["value"], threshold=threshold)
    return _pass(value=row["value"], threshold=threshold)


def config_age(run, ctx, params):
    missing = [n for n, p in (("schedule", run.schedule), ("log", run.log), ("workload", run.workload)) if p is None]
    if missing:
        return _fail(f"no {' or '.join(missing)} for the run")
    try:
        schedule = read_config_schedule(run.schedule)
        log = read_recognition_log(run.log)
    except (ScheduleError, LogError, OSError, ValueError) as exc:
        return _fail(str(exc))
    with open(run.workload, "r", encoding="utf-8") as f:
        segments = json.load(f).get("ground_truth") or []
    ages, fails = [], []
    for entry, query in zip(schedule.entries[1:], log.queries):
        seg = next((s for s in segments if int(s["t_start"]) <= query.t_set_change < int(s["t_end"])), None)
        if seg is None:
            continue                                   # the terminal snapshot: nothing to govern
        ages.append(entry.t_us - query.t_set_change)
        if entry.t_us >= int(seg["t_end"]):
            fails.append(f"entry {entry.index} (query {query.index}, t_set_change {query.t_set_change}) "
                         f"stamped at {entry.t_us}, after its segment ended at {seg['t_end']}")
    value = fmt(max(ages)) if ages else None
    if fails:
        return _fail("; ".join(fails), value=value)
    return _pass(value=value)


def starvation_floor(run, ctx, params):
    threshold = fmt(params["threshold"])
    rows = [r for r in ctx["aggregates"]
            if r["metric"] == "ready_wait" and r["aggregate"] == "max" and r["entity"] not in RESERVED_ENTITIES
            and not r.get("cause") and not r.get("window_start_us") and not r.get("window_end_us")]
    if not rows:
        return _fail("no ready_wait max aggregate for the run", threshold=threshold)
    worst = sorted(rows, key=lambda r: (-Decimal(r["value"]), r["entity"]))[0]
    value = Decimal(worst["value"])
    if value > Decimal(threshold):
        return _fail(f"{worst['entity']}: max ready_wait {_plain(value)} exceeds {_plain(Decimal(threshold))}",
                     value=worst["value"], threshold=threshold)
    return _pass(value=worst["value"], threshold=threshold)


def determinism(run, ctx, params):
    if run.rerun_trace is None:
        return _fail("no rerun trace recorded; the run has not been shown deterministic")
    rerun = _sha256(run.rerun_trace)
    if rerun != ctx["sha256"]:
        return _fail(f"trace {ctx['sha256']} differs from its rerun {rerun}", partner=rerun)
    return _pass(partner=rerun)


def utilisation_sanity(run, ctx, params):
    threshold = fmt(params["threshold"])
    row = _agg(ctx, "lane", "busy", "utilisation")
    if row is None:
        return _fail("no utilisation aggregate for the run", threshold=threshold)
    value = Decimal(row["value"])
    if value > Decimal(threshold):
        return _fail(f"utilisation {_plain(value)} exceeds {_plain(Decimal(threshold))}: busy > T_end",
                     value=row["value"], threshold=threshold)
    scoring = ctx.get("scoring_spec") or {}
    terms = ((scoring.get("files") or {}).get(run.workload_id) or {}).get("terms") or []
    if "min_exclusive" in params and terms and value <= Decimal(repr(float(params["min_exclusive"]))):
        return _fail(f"utilisation {_plain(value)} on a file with {len(terms)} scored term(s): an empty trace",
                     value=row["value"], threshold=threshold)
    return _pass(value=row["value"], threshold=threshold)


def tick_count(run, ctx, params):
    if run.guard_messages is None:
        return _fail("no primitives messages recorded; the records build's checks were not run")
    value = fmt(len(run.guard_messages))
    if run.guard_messages:
        return _fail("; ".join(run.guard_messages), value=value)
    return _pass(value=value)


def validation_matches_provenance(run, ctx, params):
    missing = [n for n, p in (("schedule", run.schedule), ("log", run.log)) if p is None]
    if missing:
        return _fail(f"no {' or '.join(missing)} for the run")
    try:
        prov = [e.provenance for e in read_config_schedule(run.schedule).entries[1:]]
        val = [q.validation for q in read_recognition_log(run.log).queries]
    except (ScheduleError, LogError, OSError, ValueError) as exc:
        return _fail(str(exc))
    reasons = []
    if len(prov) != len(val):
        reasons.append(f"{len(val)} queries for {len(prov)} non-boot entries")
    n = 0
    for i in range(max(len(prov), len(val))):
        p = prov[i] if i < len(prov) else None
        v = val[i] if i < len(val) else None
        if p != v:
            n += 1
            if len(reasons) < 2:
                reasons.append(f"index {i}: log says {v!r} where the schedule says {p!r}")
    if n or reasons:
        return _fail("; ".join(reasons), value=fmt(n))
    return _pass(value=fmt(0))


def c2_pair(run, ctx, params):
    pair = next((p for p in ctx["pairs"] if run.workload_id in (p["a"], p["b"])), None)
    if pair is None:
        return _na()
    if run.condition == "fixed" and not pair["fixed_identical"]:
        return _na()
    other = pair["b"] if run.workload_id == pair["a"] else pair["a"]
    partner = ctx["runs"].get((other, run.condition, run.table, run.seed, run.boot_default))
    if partner is None:
        return _fail(f"partner {other} not in the run set (condition {run.condition}, seed {run.seed!r}, "
                     f"boot_default {run.boot_default!r})")
    if run.trace is None or partner.trace is None:
        missing = run.workload_id if run.trace is None else other
        return _fail(f"no trace recorded for {missing}; the pair check compares the traces' bodies",
                     partner=other)
    mine, theirs = _body_sha256(run.trace), _body_sha256(partner.trace)
    same = mine == theirs
    if run.condition == "fixed":
        if not same:
            return _fail(f"traces differ under fixed where the pair's events are identical apart from the label "
                         f"({run.workload_id} vs {other})", partner=other)
        return _pass(partner=other)
    if same:
        return _fail(f"identical trace bodies under {run.condition}: the configuration never changed "
                     f"between {run.workload_id} and {other} ({mine[:12]})", partner=other)
    return _pass(partner=other)


REGISTRY = {
    "provenance_share": provenance_share,
    "config_age": config_age,
    "starvation_floor": starvation_floor,
    "determinism": determinism,
    "utilisation_sanity": utilisation_sanity,
    "tick_count": tick_count,
    "validation_matches_provenance": validation_matches_provenance,
    "c2_pair": c2_pair,
}
assert tuple(REGISTRY) == GUARDS


# ----------------------------------------------------------------- evaluate

def _applies(params, condition):
    conds = params["applies_to"]
    return conds == "all" or condition in conds


def evaluate(runs, spec, aggregates, scoring_spec=None):
    """One row per (run, guard), in run-identity order then spec order."""
    by_identity = {}
    hashes = {}
    for run in runs:
        if run.identity in by_identity:
            raise GuardError(f"run {run.identity} listed twice")
        rows = rec.read_csv(run.records)
        if not rows:
            raise GuardError(f"{run.records}: empty records file")
        first = rows[0]
        found = tuple(str(first.get(k, "")) for k in IDENTITY)
        if found != run.identity:
            raise GuardError(f"{run.records}: records identity {found} != manifest {run.identity}")
        by_identity[run.identity] = run
        hashes[run.identity] = first["source_sha256"]

    out = []
    for run in sorted(runs, key=lambda r: r.identity):
        ctx = {
            "aggregates": [r for r in aggregates
                           if tuple(str(r.get(k, "")) for k in IDENTITY) == run.identity],
            "sha256": hashes[run.identity],
            "hashes": hashes,
            "runs": by_identity,
            "pairs": spec.get("pairs") or [],
            "scoring_spec": scoring_spec,
        }
        for params in spec["guards"]:
            gid = params["id"]
            result = REGISTRY[gid](run, ctx, params) if _applies(params, run.condition) else _na()
            row = dict(zip(IDENTITY, run.identity))
            row["guard"] = gid
            row.update(result)
            out.append(row)
    return out


# --------------------------------------------------------------------- lint

def lint_spec(spec_path, schema_path, recipes_dir):
    """Returns a list of error strings; empty means the spec is legal."""
    spec_path = pathlib.Path(spec_path)
    try:
        spec = load_spec(spec_path)
    except yaml.YAMLError as err:
        return [f"{spec_path.name}: YAML error: {err}"]
    errors = []
    schema = json.loads(pathlib.Path(schema_path).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(spec), key=lambda e: [str(p) for p in e.absolute_path]):
        where = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"{where + ': ' if where else ''}{err.message}")
    if not isinstance(spec, dict):
        return errors

    guards = [g for g in (spec.get("guards") or []) if isinstance(g, dict) and "id" in g]
    ids = [g["id"] for g in guards]
    for gid in ids:
        if gid not in REGISTRY:
            errors.append(f"guard {gid!r} is not in the code's registry ({', '.join(GUARDS)})")
    for gid in GUARDS:
        if gid not in ids:
            errors.append(f"registry guard {gid!r} has no entry in the spec")
    if len(set(ids)) != len(ids):
        errors.append("duplicate guard ids")
    if tuple(ids) != GUARDS and set(ids) == set(GUARDS):
        errors.append("guards are not in the registry's order")
    for g in guards:
        if not str(g.get("grounding", "")).strip():
            errors.append(f"guard {g['id']!r}: grounding is empty")
        if g.get("direction") in BOUNDED and g.get("threshold") is None:
            errors.append(f"guard {g['id']!r}: direction {g['direction']!r} needs a threshold")
        if g.get("direction") == "structural" and g.get("threshold") is not None:
            errors.append(f"guard {g['id']!r}: a structural guard carries no threshold")

    expected = {v: b for v, b in variant_bases(recipes_dir).items() if v.startswith("c2-")}
    declared = {p["b"]: p["a"] for p in (spec.get("pairs") or [])
                if isinstance(p, dict) and "a" in p and "b" in p}
    if declared != expected:
        errors.append(f"pairs {sorted(declared.items())} != the recipe's "
                      f"{sorted(expected.items())} (dataset/timelines/coreset/c2-pairs.variant.yaml)")
    return errors


__all__ = ["COLUMNS", "GUARDS", "GUARDS_SCHEMA", "GuardError", "REGISTRY", "Run", "SCHEMA_PATH",
           "SPEC_PATH", "evaluate", "lint_spec", "load_spec"]
