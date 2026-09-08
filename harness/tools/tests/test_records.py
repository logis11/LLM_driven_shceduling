"""Records output: the four fixture pairs must reproduce their expected CSVs
byte for byte, and every row must validate against the records schema
(docs/harness/metrics.md §5)."""

import csv
import subprocess
import sys

import pytest

from conftest import MOCKS, TOOLS
from harness.records import COLUMNS, build, read_csv, validate_rows, write_csv

IDENTITY = {                      # what the trace does not carry: table, seed
    "mock-office": ("", ""),
    "mock-media": ("prior", ""),
    "mock-p1a": ("prior", ""),
    "mock-chain": ("", ""),
}


@pytest.mark.parametrize("mock", MOCKS)
def test_expected_csv_byte_for_byte(fixture_dir, mock, tmp_path):
    d = fixture_dir(mock)
    table, seed = IDENTITY[mock]
    rows, guards = build(d / "run.json", d / "trace.jsonl", table=table, seed=seed)
    assert guards == []
    out = tmp_path / "records.csv"
    write_csv(rows, out)
    assert out.read_bytes() == (d / "expected.csv").read_bytes()


@pytest.mark.parametrize("mock", MOCKS)
def test_fixture_csv_validates_against_schema(fixture_dir, mock):
    rows = read_csv(fixture_dir(mock) / "expected.csv")
    assert rows, "fixture has rows"
    validate_rows(rows)            # raises on the first invalid row


def test_columns_are_the_nineteen_in_order(fixture_dir):
    with open(fixture_dir("mock-office") / "expected.csv", newline="") as f:
        header = next(csv.reader(f))
    assert header == list(COLUMNS)
    assert len(COLUMNS) == 19


def test_schema_rejects_bad_rows(fixture_dir):
    rows = read_csv(fixture_dir("mock-chain") / "expected.csv")
    bad = dict(rows[0]); bad["metric"] = "latency_p95"        # an aggregate is not a metric
    with pytest.raises(ValueError, match="metric"):
        validate_rows([bad])
    bad = dict(rows[0]); bad["entity"] = ""
    with pytest.raises(ValueError, match="entity"):
        validate_rows([bad])
    bad = dict(next(r for r in rows if r["metric"] == "ready_wait")); bad["cause"] = "poke"
    with pytest.raises(ValueError, match="cause"):
        validate_rows([bad])
    bad = dict(rows[0]); bad["familiarity"] = 7
    with pytest.raises(ValueError, match="familiarity"):
        validate_rows([bad])


def test_cli_writes_the_same_file(fixture_dir, tmp_path):
    d = fixture_dir("mock-p1a")
    out = tmp_path / "records.csv"
    subprocess.run([sys.executable, str(TOOLS / "records.py"),
                    "--run", str(d / "run.json"), "--trace", str(d / "trace.jsonl"),
                    "--table", "prior", "--out", str(out)], check=True)
    assert out.read_bytes() == (d / "expected.csv").read_bytes()
