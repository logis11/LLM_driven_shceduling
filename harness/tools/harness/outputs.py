"""The long-format CSVs the harness writes — `aggregates` and `scores` (8.2), `guards` (8.3),
`grades` (8.4) — each in a fixed column and row order."""

import csv
import json
import pathlib

import jsonschema

HARNESS = pathlib.Path(__file__).resolve().parents[2]
AGGREGATES_SCHEMA = HARNESS / "aggregates" / "schema" / "aggregates.schema.json"
SCORES_SCHEMA = HARNESS / "scores" / "schema" / "scores.schema.json"
GRADES_SCHEMA = HARNESS / "grades" / "schema" / "grades.schema.json"


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


def iter_csv(path, columns):
    """`read_csv`'s rows one at a time, the file opened and its columns checked before the first is asked for."""
    f = open(path, "r", newline="", encoding="utf-8")
    try:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != tuple(columns):
            raise ValueError(f"{path}: columns {reader.fieldnames} != {list(columns)}")
    except BaseException:
        f.close()
        raise

    def rows():
        with f:
            for r in reader:
                yield dict(r)
    return rows()


def validate_rows(rows, schema_path):
    schema = json.loads(pathlib.Path(schema_path).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for i, row in enumerate(rows):
        clean = {k: v for k, v in row.items() if v not in ("", None)}
        for k in ("no_headroom", "oracle_worse", "censored", "n_terms", "n_no_headroom", "n_oracle_worse", "n_censored",
                  "pre_committed_miss_excluded", "over_seeds", "n", "n_files", "n_seeds"):
            if k in clean:
                clean[k] = int(clean[k])
        error = jsonschema.exceptions.best_match(validator.iter_errors(clean))
        if error is not None:
            raise ValueError(f"row {i}: {error.message}")
