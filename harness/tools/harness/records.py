"""Records — docs/harness/metrics.md §5.

`build` runs the readers and the primitives on one (run file, trace) pair —
plus the config schedule when given — and returns fully identified rows; `write_csv` writes them in the fixed column
order and row order, gzipped when the path ends in `.gz` (no name and mtime 0 in the header, so the bytes are the
content's alone; 10.4); `read_csv` reads a records file back into typed rows and `read_first` its first row alone,
either form;
`validate_rows` checks rows against the machine schema in
`harness/records/schema/records.schema.json`.
"""

import contextlib
import csv
import gzip
import io
import json
import pathlib

import jsonschema

from .primitives import compute
from .reader import read_config_schedule, read_run_file, read_trace

COLUMNS = ("workload_id", "condition", "table", "seed", "boot_default", "telemetry", "sim", "source_sha256",
           "entity", "metric", "t", "value",
           "cause", "channel", "provenance", "algorithm", "index", "period_us",
           "predicted", "truth", "validation", "familiarity", "hogs",
           "pre_committed_miss", "skipped", "censored")
_INT_COLUMNS = ("t", "value", "index", "period_us", "familiarity", "hogs",
                "pre_committed_miss", "skipped", "censored")

SCHEMA_PATH = (pathlib.Path(__file__).resolve().parents[2]
               / "records" / "schema" / "records.schema.json")


def _schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sort_key(row):
    return (row["entity"], row["metric"], int(row["t"]), str(row.get("cause", "")),
            str(row.get("channel", "")))


def build(run_path, trace_path, table="", seed="", schedule_path=None, boot_default="", telemetry=""):
    """Rows for one pair, sorted, with identity filled — `telemetry` the shape the run's daemon showed (9.17).
    Returns (rows, guards)."""
    run = read_run_file(run_path)
    trace = read_trace(trace_path)
    schedule = read_config_schedule(schedule_path) if schedule_path else None
    result = compute(run, trace, schedule)
    identity = {"workload_id": trace.meta.workload_id,
                "condition": trace.meta.condition,
                "table": table, "seed": seed, "boot_default": boot_default, "telemetry": telemetry,
                "sim": trace.meta.sim, "source_sha256": trace.sha256}
    # each primitives row is released as its records row is made, so the two lists never coexist whole (10.4
    # decision 2: c6-dual's fourteen million rows)
    src, result.rows = result.rows, None
    rows = [None] * len(src)
    for i in range(len(src)):
        row = dict(identity)
        row.update(src[i])
        src[i] = None
        rows[i] = row
    del src
    rows.sort(key=sort_key)
    validate_rows(rows)
    return rows, result.guards


@contextlib.contextmanager
def _open_write(path):
    if not str(path).endswith(".gz"):
        with open(path, "w", newline="", encoding="utf-8") as f:
            yield f
        return
    with open(path, "wb") as raw, \
            gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=6, mtime=0) as gz, \
            io.TextIOWrapper(gz, encoding="utf-8", newline="") as f:
        yield f


def _open_read(path):
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", newline="", encoding="utf-8")
    return open(path, "r", newline="", encoding="utf-8")


def write_csv(rows, path):
    with _open_write(path) as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n",
                           extrasaction="raise")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c, "")) for c in COLUMNS})


def _typed(raw):
    row = {}
    for c in COLUMNS:
        v = raw[c]
        if v == "":
            continue
        row[c] = int(v) if c in _INT_COLUMNS else v
    return row


def read_csv(path):
    """Typed rows: empty cells are absent, integer columns are ints."""
    with _open_read(path) as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError(f"{path}: columns {reader.fieldnames} != {list(COLUMNS)}")
        return [_typed(raw) for raw in reader]


def read_first(path):
    """The first typed row, or None for a file with none — what the guards read of a run's records (its identity
    and the trace's hash), without reading the rest."""
    with _open_read(path) as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError(f"{path}: columns {reader.fieldnames} != {list(COLUMNS)}")
        raw = next(reader, None)
        return None if raw is None else _typed(raw)


# The schema check by signature (10.4 decision 2): a row's validity against records.schema.json is decided by
# which keys it carries, each value's type, the values of the fields an `enum`, `const` or `pattern` reads, whether
# a free string is empty, and where an integer falls against the bounds the schema names (0, 1 and 5). `_signature`
# keeps exactly that, so two rows with one signature are both valid or both invalid; each signature is validated
# once, on the first row that carries it, and the first invalid row raises the error it raised before.
_KEPT = frozenset(("condition", "table", "telemetry", "metric", "cause", "channel", "provenance", "algorithm",
                   "validation", "source_sha256"))                # enum, const or pattern: the value itself
_FREE = frozenset(("workload_id", "seed", "boot_default", "sim", "predicted", "truth"))   # minLength at most
_ENTITY_CONSTS = frozenset(("schedule", "lane", "recognizer"))   # the entity consts of the schema's allOf
_INTEGERS = frozenset(("t", "value", "index", "period_us", "familiarity", "hogs", "pre_committed_miss",
                       "censored", "skipped"))                    # bounds in {0, 1, 5}: clamped to [-1, 6]
SIGNATURE_FIELDS = _KEPT | _FREE | _INTEGERS | {"entity"}


def _abstract(key, v):
    if type(v) is int:
        return (int, -1 if v < 0 else 6 if v > 5 else v) if key in _INTEGERS else (int, v)
    if type(v) is str:
        if key in _KEPT:
            return (str, v)
        if key == "entity":
            return (str, v if v in _ENTITY_CONSTS else bool(v))
        if key in _FREE:
            return (str, bool(v))
        return (str, v)
    return (type(v), v)                                           # anything else as it is (unhashable: no cache)


def _signature(clean):
    return tuple(sorted((k, _abstract(k, v)) for k, v in clean.items()))


def validate_rows(rows):
    validator = jsonschema.Draft202012Validator(_schema())
    valid = set()
    for i, row in enumerate(rows):
        clean = {k: v for k, v in row.items() if v not in ("", None)}
        try:
            sig = _signature(clean)
            hash(sig)
        except TypeError:
            sig = None
        if sig is not None and sig in valid:
            continue
        error = jsonschema.exceptions.best_match(validator.iter_errors(clean))
        if error is not None:
            where = "/".join(str(p) for p in error.absolute_path) or "row"
            raise ValueError(f"records row {i}: {where}: {error.message}")
        if sig is not None:
            valid.add(sig)
