"""Dataset linter — building-plan §6 + the schema-declared canonical invariants.

Three lint layers, each returning a list of error strings:
  repo lints       registry subset, archetype provenance, meas-pending freeze
  timeline lints   structural rules (delegated to Timeline's loader)
  canonical lints  event ordering, id uniqueness, FORK <-> spawn_table,
                   channel resolution, JSON-Schema validation, demand window
"""

import json
import pathlib
import re

import jsonschema
import yaml

from .estimate import check_window
from .timeline import Timeline, TimelineError

REQUIRED_ARCHETYPE_FIELDS = (
    "category_source", "pattern", "params", "lifetime", "binding_params",
    "scalable", "validation_stats", "modeling_notes")
LIFETIMES = {"segment-bound", "finite", "spawned"}
SAMPLING = {"per-instance", "per-task", "per-iteration"}


# ---- repo lints -------------------------------------------------------------

def reference_ids(references_md):
    text = pathlib.Path(references_md).read_text()
    return set(re.findall(r"^### `([^`]+)`", text, flags=re.M))


def lint_repo(archetypes_path, sources_path, references_md, freeze=False):
    errors = []
    registry = yaml.safe_load(pathlib.Path(sources_path).read_text())["sources"]
    known_refs = reference_ids(references_md)
    for sid in registry:
        if sid not in known_refs:
            errors.append(f"registry id {sid!r} has no docs/references.md entry "
                          "(subset lint)")

    archetypes = yaml.safe_load(
        pathlib.Path(archetypes_path).read_text())["archetypes"]
    for aid, entry in archetypes.items():
        for field in REQUIRED_ARCHETYPE_FIELDS:
            if field not in entry:
                errors.append(f"{aid}: missing field {field!r}")
        if entry.get("lifetime") not in LIFETIMES:
            errors.append(f"{aid}: bad lifetime {entry.get('lifetime')!r}")
        if entry.get("lifetime") == "spawned" and "spawned_by" not in entry:
            errors.append(f"{aid}: spawned but no spawned_by")
        for pname, param in (entry.get("params") or {}).items():
            where = f"{aid}.{pname}"
            if pname in ("components", "focus_components"):
                # 9.5 fold-in (D16): a list of measured timer components, each with gap and run distributions
                if not isinstance(param, list) or not param:
                    errors.append(f"{where}: must be a non-empty list of components")
                    continue
                for i, comp in enumerate(param):
                    for field in ("comm", "gap", "run"):
                        if field not in comp:
                            errors.append(f"{where}[{i}]: missing {field!r}")
                    for field in ("gap", "run"):
                        if field in comp:
                            errors.extend(_check_param(f"{where}[{i}].{field}", comp[field], registry, freeze))
                continue
            if pname == "operations":
                # 9.5 follow-ups (spec decision 8): named operations, each with a measured duration table and components
                if not isinstance(param, dict) or not param:
                    errors.append(f"{where}: must be a non-empty map of operations")
                    continue
                for oname, op in param.items():
                    if "duration" not in op:
                        errors.append(f"{where}.{oname}: missing 'duration'")
                    else:
                        errors.extend(_check_param(f"{where}.{oname}.duration", op["duration"], registry, freeze))
                    comps = op.get("components")
                    if not isinstance(comps, list) or not comps:
                        errors.append(f"{where}.{oname}: must carry a non-empty list of components")
                        continue
                    for i, comp in enumerate(comps):
                        for field in ("comm", "gap", "run"):
                            if field not in comp:
                                errors.append(f"{where}.{oname}.components[{i}]: missing {field!r}")
                        for field in ("gap", "run"):
                            if field in comp:
                                errors.extend(_check_param(f"{where}.{oname}.components[{i}].{field}", comp[field], registry, freeze))
                continue
            if pname == "heavy_events":
                # 9.5 D64: a rare run carried as its own stated event, not as a component's wake — what was measured
                # (the runs, their count and the span counted over) and no interval, none having been measured
                if not isinstance(param, list) or not param:
                    errors.append(f"{where}: must be a non-empty list of events")
                    continue
                for i, ev in enumerate(param):
                    for field in ("comm", "count", "span_s", "rate_per_s", "run"):
                        if field not in ev:
                            errors.append(f"{where}[{i}]: missing {field!r}")
                    if "run" in ev:
                        errors.extend(_check_param(f"{where}[{i}].run", ev["run"], registry, freeze))
                    if "gap" in ev:
                        errors.append(f"{where}[{i}]: a heavy event states no gap — none is measured (D64)")
                continue
            if pname == "stimulus":
                # 9.5 fold-in (D18): a replayed stream; the file must exist beside the library
                stream = param.get("stream")
                path = pathlib.Path(archetypes_path).resolve().parent / "stimulus" / f"{stream}.jsonl"
                if not stream or not path.exists():
                    errors.append(f"{where}: stream {stream!r} has no file at dataset/stimulus/")
                for kind in param.get("kinds") or []:
                    if kind not in STIMULUS_KINDS:
                        errors.append(f"{where}: kind {kind!r} is not an event kind of the streams")
            errors.extend(_check_param(where, param, registry, freeze))
    return errors


def _check_param(where, param, registry, freeze):
    errors = []
    tag = param.get("source")
    if tag is None:
        errors.append(f"{where}: numeric param without source tag")
    else:
        errors.extend(_check_tag(where, tag, registry))
        if freeze and tag == "meas-pending":
            errors.append(f"{where}: meas-pending after freeze")
    if param.get("sampling") not in SAMPLING:
        errors.append(f"{where}: bad sampling {param.get('sampling')!r}")
    if param.get("dist") == "quantiles":
        q = param.get("p")
        if not isinstance(q, list) or len(q) != 10 or any((not isinstance(v, (int, float))) or v < 0 for v in q) \
                or any(b < a for a, b in zip(q, q[1:])):
            errors.append(f"{where}: quantiles need 10 non-decreasing non-negative values (p1 … p99.9, µs)")
        else:
            errors.extend(_check_table_extremes(where, param, q))
    return errors


def _check_table_extremes(where, param, q):
    """A measured table's `min`, `max` and eleven interval `means` (the fidelity fix): all three or none; the
    extremes bound the quantiles; each mean inside its interval, to the microsecond the knots are rounded to."""
    have = {k for k in ("min", "max", "means") if k in param}
    if not have:
        return []
    if have != {"min", "max", "means"}:
        return [f"{where}: a table carries min, max and means together"]
    errors = []
    lo, hi, means = param["min"], param["max"], param["means"]
    if lo > q[0]:
        errors.append(f"{where}: min above p1")
    if hi < q[-1]:
        errors.append(f"{where}: max below p99.9")
    if not isinstance(means, list) or len(means) != 11:
        return errors + [f"{where}: eleven interval means (min … p1 … p99.9 … max)"]
    bounds = [lo, *q, hi]
    for i, m in enumerate(means):
        if not bounds[i] - 1 <= m <= bounds[i + 1] + 1:
            errors.append(f"{where}: interval mean {i} ({m}) outside [{bounds[i]}, {bounds[i + 1]}]")
    return errors


STIMULUS_KINDS = {"key", "click", "wheel", "drag"}   # the event kinds of dataset/stimulus/ streams


def _check_tag(where, tag, registry):
    m = re.fullmatch(r"([a-z0-9-]+)(?::(.+))?", tag)
    if not m:
        return [f"{where}: malformed source tag {tag!r}"]
    sid, locator = m.group(1), m.group(2)
    if sid not in registry:
        return [f"{where}: source id {sid!r} not in registry"]
    pattern = registry[sid].get("locator_pattern")
    if locator and not pattern:
        return [f"{where}: {tag!r} has a locator but {sid!r} declares no pattern"]
    if locator and pattern and not re.fullmatch(pattern, locator):
        return [f"{where}: locator {locator!r} violates {sid} pattern {pattern}"]
    return []


# ---- timeline lints ---------------------------------------------------------

def lint_timeline(path, library):
    try:
        Timeline(path, library)
        return []
    except TimelineError as err:
        return [str(err)]


# ---- canonical lints --------------------------------------------------------

def load_schema(schema_path):
    return json.loads(pathlib.Path(schema_path).read_text())


def lint_canonical(canonical, schema, report=None, mode=None, name=""):
    errors = []
    prefix = f"{name}: " if name else ""

    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(canonical):
        errors.append(f"{prefix}schema: {err.message} at "
                      f"{'/'.join(map(str, err.absolute_path))}")
    if errors:
        return errors  # structural failures make the rest unreliable

    events = canonical["events"]
    times = [e["t"] for e in events]
    if times != sorted(times):
        errors.append(f"{prefix}events not sorted by t")

    arrivals = [e for e in events if e["op"] == "arrive"]
    ids = [e["id"] for e in arrivals]
    for entry in arrivals:
        ids.extend(s["id"] for s in entry.get("spawn_table") or [])
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        errors.append(f"{prefix}duplicate task ids: {sorted(duplicates)}")

    waits = {}  # task id -> set of channels its program waits on
    for entry in arrivals:
        forks = _count_ops(entry["program"], "FORK")
        table = entry.get("spawn_table")
        if forks and table is None:
            errors.append(f"{prefix}{entry['id']}: FORK without spawn_table")
        if table is not None and not forks:
            errors.append(f"{prefix}{entry['id']}: spawn_table without FORK")
        if table is not None and forks > len(table):
            errors.append(f"{prefix}{entry['id']}: {forks} FORKs > "
                          f"{len(table)} spawn entries")
        waits[entry["id"]] = _wait_channels(entry["program"])
        for spawn in table or []:
            waits[spawn["id"]] = _wait_channels(spawn["program"])

    for event in events:
        if event["op"] != "wake":
            continue
        target = event["target"]
        if target not in waits:
            errors.append(f"{prefix}wake targets unknown task {target!r}")
        elif event["channel"] not in waits[target]:
            errors.append(f"{prefix}wake channel {event['channel']!r} never "
                          f"awaited by {target!r}")

    known = set(waits)
    for entry in arrivals:
        for target in _wake_targets(entry["program"]):
            if target not in known:
                errors.append(f"{prefix}{entry['id']}: WAKE targets unknown "
                              f"task {target!r}")

    if report is not None and mode is not None:
        violation = check_window(report, mode)
        if violation:
            errors.append(f"{prefix}{violation}")
    return errors


def _walk(program):
    for instruction in program:
        if instruction["op"] == "LOOP":
            yield from _walk(instruction["body"])
        else:
            yield instruction


def _count_ops(program, op):
    return sum(1 for i in _walk(program) if i["op"] == op)


def _wait_channels(program):
    return {i["channel"] for i in _walk(program) if i["op"] == "WAIT"}


def _wake_targets(program):
    return {i["target"] for i in _walk(program) if i["op"] == "WAKE"}
