"""Driver table lint — structure and legality of one table file.

Everything JSON Schema can say lives in driver-table.schema.json; this module
adds the cross-checks it cannot: the 32-row key space, default ∈ entries,
role-specific entry counts, LOTTERY's batch_share ≤ cap, and the
byte-identical wanted-pair check.
"""

import json
import pathlib

import jsonschema
import yaml

from .config_schema import ALGORITHMS, CAP_RANGE, MODES


def load_schema(path):
    return json.loads(pathlib.Path(path).read_text())


def _key(row):
    return f"({row.get('mode')}, background_wanted={str(row.get('background_wanted')).lower()})"


def compose(row, algorithm):
    """The configuration a condition receives from this row for `algorithm`:
    the envelope the simulator sees. Canonical bytes, for the pair check."""
    entry = row["entries"][algorithm]
    config = {"algorithm": algorithm, "params": entry["params"],
              "batch_bandwidth_cap": row["batch_bandwidth_cap"]}
    return json.dumps(config, sort_keys=True, separators=(",", ":"))


def lint_table(path, schema_path):
    """Returns a list of error strings; empty means the table is legal."""
    path = pathlib.Path(path)
    try:
        table = yaml.safe_load(path.read_text())
    except yaml.YAMLError as err:
        return [f"{path.name}: YAML error: {err}"]

    schema = load_schema(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    errors = []
    for err in sorted(validator.iter_errors(table), key=lambda e: [str(p) for p in e.absolute_path]):
        errors.append(f"{path.name}: {_describe_path(table, err.absolute_path)}{_phrase(err)}")
    if errors:
        return errors   # structural problems first; the cross-checks assume shape

    role = table["role"]
    rows = table["rows"]

    # --- key space: every (mode, background_wanted) exactly once
    seen = {}
    for row in rows:
        key = (row["mode"], row["background_wanted"])
        if key in seen:
            errors.append(f"{path.name}: duplicate row {_key(row)}")
        seen[key] = row
    for mode in MODES:
        for wanted in (True, False):
            if (mode, wanted) not in seen:
                errors.append(f"{path.name}: row ({mode}, background_wanted="
                              f"{str(wanted).lower()}) missing")

    # --- per-row legality
    for row in rows:
        k = _key(row)
        entries = row["entries"]
        if row["default"] not in entries:
            errors.append(f"{path.name}: row {k}: default {row['default']!r} has no entry")
        cap = row["batch_bandwidth_cap"]
        if cap is not None and not CAP_RANGE[0] <= cap <= CAP_RANGE[1]:
            errors.append(f"{path.name}: row {k}: batch_bandwidth_cap {cap} outside "
                          f"[{CAP_RANGE[0]}, {CAP_RANGE[1]}]")
        if role == "prior" and len(entries) != 1:
            errors.append(f"{path.name}: prior table: row {k} must carry exactly one entry "
                          f"(has {len(entries)})")
        if role == "calibrated":
            for alg in ALGORITHMS:
                if alg not in entries:
                    errors.append(f"{path.name}: calibrated table: row {k} missing entry for {alg}")
        for alg, entry in entries.items():
            if entry.get("basis") != "schema-default" and not entry.get("justification"):
                errors.append(f"{path.name}: row {k}: entry {alg}: justification required "
                              f"unless basis is schema-default")
            if alg == "LOTTERY" and cap is not None:
                share = entry["params"].get("batch_share")
                if isinstance(share, (int, float)) and share > cap:
                    errors.append(f"{path.name}: row {k}: LOTTERY batch_share {share} "
                                  f"exceeds batch_bandwidth_cap {cap}")

    # --- byte-identical wanted pairs on the default configuration
    for mode in MODES:
        a, b = seen.get((mode, True)), seen.get((mode, False))
        if a is None or b is None:
            continue
        if a["default"] in a["entries"] and b["default"] in b["entries"]:
            if compose(a, a["default"]) == compose(b, b["default"]):
                errors.append(f"{path.name}: {mode}: wanted=true and wanted=false default "
                              f"configurations are byte-identical")
    return errors


def _phrase(err):
    """One phrasing for schema violations, independent of the jsonschema version."""
    leaf = err.absolute_path[-1] if len(err.absolute_path) else None
    sub = err.schema if isinstance(err.schema, dict) else {}
    if err.validator == "enum":
        return f"{leaf} {err.instance!r} not one of {sub.get('enum')}"
    if err.validator == "required":
        missing = [k for k in sub.get("required", []) if k not in err.instance]
        return "missing " + ", ".join(repr(m) for m in missing)
    if err.validator == "additionalProperties":
        extra = [k for k in err.instance if k not in sub.get("properties", {})]
        return "unexpected " + ", ".join(repr(x) for x in extra)
    if err.validator in ("minimum", "maximum"):
        return f"{leaf} {err.instance} outside [{sub.get('minimum')}, {sub.get('maximum')}]"
    if err.validator == "type":
        kinds = sub.get("type"); kinds = kinds if isinstance(kinds, list) else [kinds]
        names = {"integer": "an integer", "number": "a number", "null": "null",
                 "string": "a string", "boolean": "a boolean", "object": "an object",
                 "array": "a list"}
        return f"{leaf} must be " + " or ".join(names.get(k, k) for k in kinds)
    if err.validator == "minLength":
        return f"{leaf} must not be empty"
    if err.validator == "minProperties":
        return f"{leaf} needs at least one entry"
    return err.message


def _describe_path(table, abs_path):
    """'row (mode, background_wanted=…): ' prefix when the error sits inside a row."""
    parts = list(abs_path)
    if len(parts) >= 2 and parts[0] == "rows" and isinstance(parts[1], int):
        try:
            row = table["rows"][parts[1]]
            rest = "/".join(str(p) for p in parts[2:])
            return f"row {_key(row)}: {rest + ': ' if rest else ''}"
        except (KeyError, IndexError, TypeError):
            pass
    return ("/".join(str(p) for p in parts) + ": ") if parts else ""


__all__ = ["lint_table", "load_schema", "compose"]
