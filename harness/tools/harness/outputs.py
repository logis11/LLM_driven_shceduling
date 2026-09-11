"""The two files sub-task 8.2 writes — `aggregates` and `scores` — as CSV in a fixed column and row order."""

import csv
import json
import pathlib

import jsonschema

HARNESS = pathlib.Path(__file__).resolve().parents[2]
AGGREGATES_SCHEMA = HARNESS / "aggregates" / "schema" / "aggregates.schema.json"
SCORES_SCHEMA = HARNESS / "scores" / "schema" / "scores.schema.json"


def write_csv(rows, columns, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n", extrasaction="raise")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c, "")) for c in columns})


def read_csv(path, columns):
    """Rows as strings; empty cells kept as empty strings (the schemas treat them as absent)."""
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != tuple(columns):
            raise ValueError(f"{path}: columns {reader.fieldnames} != {list(columns)}")
        return [dict(r) for r in reader]


def validate_rows(rows, schema_path):
    schema = json.loads(pathlib.Path(schema_path).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for i, row in enumerate(rows):
        clean = {k: v for k, v in row.items() if v not in ("", None)}
        for k in ("no_headroom", "censored", "n_terms", "n_no_headroom", "n_censored"):
            if k in clean:
                clean[k] = int(clean[k])
        error = jsonschema.exceptions.best_match(validator.iter_errors(clean))
        if error is not None:
            raise ValueError(f"row {i}: {error.message}")
