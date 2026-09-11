"""Records — docs/harness/metrics.md §5.

`build` runs the readers and the primitives on one (run file, trace) pair —
plus the config schedule when given — and returns fully identified rows; `write_csv` writes them in the fixed column
order and row order; `read_csv` reads a records file back into typed rows;
`validate_rows` checks rows against the machine schema in
`harness/records/schema/records.schema.json`.
"""

import csv
import json
import pathlib

import jsonschema

from .primitives import compute
from .reader import read_config_schedule, read_run_file, read_trace

COLUMNS = ("workload_id", "condition", "table", "seed", "boot_default", "sim", "source_sha256",
           "entity", "metric", "t", "value",
           "cause", "provenance", "algorithm", "index", "period_us",
           "predicted", "truth", "validation", "familiarity", "hogs",
           "pre_committed_miss")
_INT_COLUMNS = ("t", "value", "index", "period_us", "familiarity", "hogs",
                "pre_committed_miss")

SCHEMA_PATH = (pathlib.Path(__file__).resolve().parents[2]
               / "records" / "schema" / "records.schema.json")


def _schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sort_key(row):
    return (row["entity"], row["metric"], int(row["t"]), str(row.get("cause", "")))


def build(run_path, trace_path, table="", seed="", schedule_path=None, boot_default=""):
    """Rows for one pair, sorted, with identity filled. Returns (rows, guards)."""
    run = read_run_file(run_path)
    trace = read_trace(trace_path)
    schedule = read_config_schedule(schedule_path) if schedule_path else None
    result = compute(run, trace, schedule)
    identity = {"workload_id": trace.meta.workload_id,
                "condition": trace.meta.condition,
                "table": table, "seed": seed, "boot_default": boot_default,
                "sim": trace.meta.sim, "source_sha256": trace.sha256}
    rows = []
    for r in result.rows:
        row = dict(identity)
        row.update(r)
        rows.append(row)
    rows.sort(key=sort_key)
    validate_rows(rows)
    return rows, result.guards


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n",
                           extrasaction="raise")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c, "")) for c in COLUMNS})


def read_csv(path):
    """Typed rows: empty cells are absent, integer columns are ints."""
    rows = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError(f"{path}: columns {reader.fieldnames} != {list(COLUMNS)}")
        for raw in reader:
            row = {}
            for c in COLUMNS:
                v = raw[c]
                if v == "":
                    continue
                row[c] = int(v) if c in _INT_COLUMNS else v
            rows.append(row)
    return rows


def validate_rows(rows):
    validator = jsonschema.Draft202012Validator(_schema())
    for i, row in enumerate(rows):
        clean = {k: v for k, v in row.items() if v not in ("", None)}
        error = jsonschema.exceptions.best_match(validator.iter_errors(clean))
        if error is not None:
            where = "/".join(str(p) for p in error.absolute_path) or "row"
            raise ValueError(f"records row {i}: {where}: {error.message}")
