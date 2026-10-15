"""Dataset linter — building-plan §6 + the schema-declared canonical invariants.

Three lint layers, each returning a list of error strings:
  repo lints       registry subset, archetype provenance, meas-pending freeze
  timeline lints   structural rules (delegated to Timeline's loader)
  canonical lints  event ordering, id uniqueness, FORK <-> spawn_table,
                   channel resolution, the comm limit, programs' ends,
                   JSON-Schema validation
"""

import json
import pathlib
import re

import jsonschema_rs
import yaml

from .timeline import Timeline, TimelineError

REQUIRED_ARCHETYPE_FIELDS = (
    "category_source", "declared_class", "pattern", "params", "lifetime", "binding_params",
    "scalable", "validation_stats", "modeling_notes")
LIFETIMES = {"segment-bound", "finite", "spawned"}
DECLARED_CLASSES = {"normal", "idle"}   # 9.13 spec decision 2: widened only when an entry carries batch or real-time work
COMM_LIMIT = 15   # TASK_COMM_LEN 16 less the terminator (linux-sched-h)
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
        if "declared_class" in entry and entry["declared_class"] not in DECLARED_CLASSES:
            errors.append(f"{aid}: bad declared_class {entry['declared_class']!r}")
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
            if pname == "launch":
                # 9.10 D136: the observed launch phase, replayed; its streams' file must exist beside the library
                stream = param.get("stream")
                path = pathlib.Path(archetypes_path).resolve().parent / "launch" / f"{stream}.json.gz"
                if not stream or not path.exists():
                    errors.append(f"{where}: stream {stream!r} has no file at dataset/launch/")
            if pname == "replay":
                # 9.14 decision 12: one pooled repeat's observed stream in place of the sampled one (the trace-replay
                # variant); its file must exist beside the library
                stream = param.get("stream")
                path = pathlib.Path(archetypes_path).resolve().parent / "replay" / f"{stream}.json.gz"
                if not stream or not path.exists():
                    errors.append(f"{where}: stream {stream!r} has no file at dataset/replay/")
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

BOUND_LABELS = ("design", "convention", "arithmetic")   # 9.10 D32: a value no source states is labelled for what it is


def lint_bound_sources(path, registry):
    """9.18 spec, decision 4 (9.10 D32): every value a timeline binds — the `bind` keys and the task's `count` when
    stated — has an entry in the task's `source` map, and nothing else does; an entry is one source tag, a list of
    source tags, or one of BOUND_LABELS. Tags are checked against the registry as the library's are."""
    errors = []
    raw = yaml.safe_load(pathlib.Path(path).read_text())
    name = pathlib.Path(path).name
    for task in raw.get("tasks") or []:
        where = f"{name}: task {task.get('id')!r}"
        bound = set(task.get("bind") or {}) | ({"count"} if "count" in task else set())
        source = task.get("source")
        if source is None:
            if bound:
                errors.append(f"{where}: bound values {sorted(bound)} carry no source map")
            continue
        if not isinstance(source, dict):
            errors.append(f"{where}: source must be a map keyed by the bound values")
            continue
        missing, extra = bound - set(source), set(source) - bound
        if missing:
            errors.append(f"{where}: bound values {sorted(missing)} have no source entry")
        if extra:
            errors.append(f"{where}: source entries {sorted(extra)} name no bound value")
        for key in sorted(set(source) & bound):
            value = source[key]
            tags = value if isinstance(value, list) else [value]
            if not tags:
                errors.append(f"{where}: source of {key!r} is empty")
            for tag in tags:
                if not isinstance(tag, str):
                    errors.append(f"{where}: source of {key!r} is not a tag or a label: {tag!r}")
                elif tag in BOUND_LABELS:
                    if isinstance(value, list):
                        errors.append(f"{where}: source of {key!r} lists the label {tag!r}; a label stands alone")
                else:
                    errors.extend(_check_tag(f"{where}.{key}", tag, registry))
    return errors


def lint_timeline(path, library):
    try:
        Timeline(path, library)
        return []
    except TimelineError as err:
        return [str(err)]


# ---- canonical lints --------------------------------------------------------

def load_schema(schema_path):
    return json.loads(pathlib.Path(schema_path).read_text())


_VALIDATORS = {}   # id(schema) -> (schema, compiled validator); one compile per schema document per process


def _validator(schema):
    """The schema compiled by jsonschema-rs (9.22 spec, decision 3): the same 2020-12 validation as the Python
    jsonschema package gave, about a hundred times faster on the set's largest artifacts."""
    entry = _VALIDATORS.get(id(schema))
    if entry is None or entry[0] is not schema:
        entry = _VALIDATORS[id(schema)] = (schema, jsonschema_rs.validator_for(schema))
    return entry[1]


def lint_canonical(canonical, schema, report=None, mode=None, name=""):
    errors = []
    prefix = f"{name}: " if name else ""

    for err in _validator(schema).iter_errors(canonical):
        errors.append(f"{prefix}schema: {err.message} at "
                      f"{'/'.join(map(str, err.instance_path))}")
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

    # 9.11 D11, D33 (9.13): a TIMER-carrying program begins, in execution order, with its TIMER — a LOOP head's body
    # counting — so TIMER's t₀, its first execution, is the task's arrival and the two cannot come apart silently
    for entry in arrivals:
        for record in [entry] + list(entry.get("spawn_table") or []):
            opens_with = _timer_first_violation(record["program"])
            if opens_with:
                errors.append(f"{prefix}{record['id']}: TIMER is not the first executed instruction — the program "
                              f"opens with {opens_with}, so TIMER's t₀ would not be the arrival (9.11 D11)")

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
    for entry in arrivals:   # 9.23 B4: a spawned child's WAKE resolves as a top-level task's does
        for record in [entry] + list(entry.get("spawn_table") or []):
            for target in _wake_targets(record["program"]):
                if target not in known:
                    errors.append(f"{prefix}{record['id']}: WAKE targets unknown "
                                  f"task {target!r}")

    # 9.23 B4: a name within the kernel's comm limit, 15 characters and the terminator (linux-sched-h)
    for entry in arrivals:
        for record in [entry] + list(entry.get("spawn_table") or []):
            if len(record["name"]) > COMM_LIMIT:
                errors.append(f"{prefix}{record['id']}: name {record['name']!r} longer than "
                              f"{COMM_LIMIT} characters (the comm limit)")

    # 9.23 B4, N1: no program runs out — a task without a pinned depart ends with EXIT, a segment-bound task with
    # the blocking step its loop takes next (WAIT, TIMER) or an unbounded LOOP, so it is blocked when the user closes it
    for entry in arrivals:
        records = [(entry, entry.get("depart") is not None)]
        records += [(spawn, False) for spawn in entry.get("spawn_table") or []]
        for record, bound in records:
            ends_with = _end_violation(record["program"], bound)
            if ends_with:
                errors.append(f"{prefix}{record['id']}: the program ends with {ends_with}, so it runs out "
                              + ("before its depart" if bound else "without EXIT"))

    # 9.17: the focus track names top-level tasks within their pinned lifetimes, in time order, never overlapping
    by_id = {e["id"]: e for e in arrivals}
    focus = canonical.get("focus") or []
    for win in focus:
        task = by_id.get(win["task"])
        if task is None:
            errors.append(f"{prefix}focus names {win['task']!r}, not a top-level task")
            continue
        if win["t_start"] >= win["t_end"]:
            errors.append(f"{prefix}focus interval of {win['task']!r}: t_start >= t_end")
        if win["t_start"] < task["t"] or (task.get("depart") is not None and win["t_end"] > task["depart"]):
            errors.append(f"{prefix}focus interval of {win['task']!r} lies outside its pinned lifetime")
    starts = [w["t_start"] for w in focus]
    if starts != sorted(starts):
        errors.append(f"{prefix}focus intervals not sorted by t_start")
    else:
        for a, b in zip(focus, focus[1:]):
            if a["t_end"] > b["t_start"]:
                errors.append(f"{prefix}focus intervals overlap at {b['t_start']} (one user, one attention track)")

    return errors


def _walk(program):
    for instruction in program:
        if instruction["op"] == "LOOP":
            yield from _walk(instruction["body"])
        else:
            yield instruction


def _count_ops(program, op):
    return sum(1 for i in _walk(program) if i["op"] == op)


def _first_executed(program):
    """The first instruction a program executes, descending LOOP heads; None for an empty program."""
    while program:
        head = program[0]
        if head["op"] != "LOOP":
            return head
        program = head["body"]
    return None


def _timer_first_violation(program):
    """None when the program holds no TIMER or executes one first; otherwise the op it opens with instead."""
    if not _count_ops(program, "TIMER"):
        return None
    first = _first_executed(program)
    if first is not None and first["op"] == "TIMER":
        return None
    return first["op"] if first is not None else "nothing"


def _end_violation(program, bound):
    """None when the program ends as its lifetime requires; otherwise what it ends with instead."""
    last = program[-1] if program else None
    if bound:
        if last is not None and (last["op"] in ("WAIT", "TIMER")
                                 or (last["op"] == "LOOP" and last.get("count") == "unbounded")):
            return None
    elif last is not None and last["op"] == "EXIT":
        return None
    return last["op"] if last is not None else "nothing"


def _wait_channels(program):
    return {i["channel"] for i in _walk(program) if i["op"] == "WAIT"}


def _wake_targets(program):
    return {i["target"] for i in _walk(program) if i["op"] == "WAKE"}
