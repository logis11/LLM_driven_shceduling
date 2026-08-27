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
            tag = param.get("source")
            if tag is None:
                errors.append(f"{where}: numeric param without source tag")
            else:
                errors.extend(_check_tag(where, tag, registry))
                if freeze and tag == "meas-pending":
                    errors.append(f"{where}: meas-pending after freeze")
            if param.get("sampling") not in SAMPLING:
                errors.append(f"{where}: bad sampling {param.get('sampling')!r}")
    return errors


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
