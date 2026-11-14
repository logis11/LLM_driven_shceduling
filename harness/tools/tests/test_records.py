"""Records output: the four fixture pairs must reproduce their expected CSVs
byte for byte, and every row must validate against the records schema
(docs/harness/metrics.md §5)."""

import csv
import subprocess
import sys

import pytest

from conftest import FIXTURES, MOCKS, TOOLS
from harness.records import COLUMNS, build, read_csv, validate_rows, write_csv

IDENTITY = {                      # what the trace does not carry: table, seed
    "mock-office": ("", ""),
    "mock-media": ("prior", ""),
    "mock-p1a": ("prior", ""),
    "mock-chain": ("prior", ""),
    "mock-switch": ("calibrated", ""),
    "mock-wakes": ("", ""),
}


def schedule_of(d):
    """The config schedule beside a fixture, when it has one (metrics doc §3)."""
    p = d / "config-schedule.json"
    return p if p.exists() else None


@pytest.mark.parametrize("mock", MOCKS)
def test_expected_csv_byte_for_byte(fixture_dir, mock, tmp_path):
    d = fixture_dir(mock)
    table, seed = IDENTITY[mock]
    rows, guards = build(d / "run.json", d / "trace.jsonl", table=table, seed=seed,
                         schedule_path=schedule_of(d), telemetry="names")   # the fixtures predate the focus (9.17)
    assert guards == []
    out = tmp_path / "records.csv"
    write_csv(rows, out)
    assert out.read_bytes() == (d / "expected.csv").read_bytes()


@pytest.mark.parametrize("mock", MOCKS)
def test_fixture_csv_validates_against_schema(fixture_dir, mock):
    rows = read_csv(fixture_dir(mock) / "expected.csv")
    assert rows, "fixture has rows"
    validate_rows(rows)            # raises on the first invalid row


def test_columns_are_the_twenty_six_in_order(fixture_dir):
    with open(fixture_dir("mock-office") / "expected.csv", newline="") as f:
        header = next(csv.reader(f))
    assert header == list(COLUMNS)
    assert len(COLUMNS) == 26
    assert COLUMNS[COLUMNS.index("cause") + 1] == "channel"
    assert COLUMNS[COLUMNS.index("boot_default") + 1] == "telemetry"          # 9.17: the sixth identity column
    assert COLUMNS[-4:] == ("hogs", "pre_committed_miss", "skipped", "censored")


def test_channel_rides_on_wake_rows_only(fixture_dir):
    """metrics doc §5: `channel` is filled on `ready_wait` rows with cause `wake`
    and on no other row."""
    rows = read_csv(fixture_dir("mock-chain") / "expected.csv")
    wake = next(r for r in rows if r["metric"] == "ready_wait" and r["cause"] == "wake")
    assert wake["channel"] == "chain"
    validate_rows([dict(wake, channel="timer")])
    arrive = next(r for r in rows if r["metric"] == "ready_wait" and r["cause"] == "arrive")
    with pytest.raises(ValueError):
        validate_rows([dict(arrive, channel="input")])
    busy = next(r for r in rows if r["metric"] == "busy")
    with pytest.raises(ValueError):
        validate_rows([dict(busy, channel="input")])
    with pytest.raises(ValueError, match="channel"):
        validate_rows([dict(wake, channel="input:editor")])     # the kind, never the full name


def test_pre_committed_miss_is_zero_or_one():
    rec = {"workload_id": "w", "condition": "oracle", "sim": "", "source_sha256": "0" * 64,
           "entity": "recognizer", "metric": "mode_correct", "t": 0, "value": 1,
           "validation": "unmodified", "predicted": "dev", "truth": "dev",
           "pre_committed_miss": 2}
    with pytest.raises(ValueError, match="pre_committed_miss"):
        validate_rows([rec])
    rec["pre_committed_miss"] = 1
    validate_rows([rec])                                    # 0 and 1 are the only values


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
    sw = dict(next(r for r in read_csv(fixture_dir("mock-switch") / "expected.csv")
                   if r["metric"] == "switch_window"))
    validate_rows([sw])
    bad = dict(sw); del bad["hogs"]
    with pytest.raises(ValueError, match="hogs"):
        validate_rows([bad])
    bad = dict(sw); bad["entity"] = "hog"
    with pytest.raises(ValueError, match="schedule"):
        validate_rows([bad])


def test_cli_writes_the_same_file(fixture_dir, tmp_path):
    d = fixture_dir("mock-p1a")
    out = tmp_path / "records.csv"
    subprocess.run([sys.executable, str(TOOLS / "records.py"),
                    "--run", str(d / "run.json"), "--trace", str(d / "trace.jsonl"),
                    "--table", "prior", "--telemetry", "names", "--out", str(out)], check=True)
    assert out.read_bytes() == (d / "expected.csv").read_bytes()


def test_cli_takes_the_config_schedule(fixture_dir, tmp_path):
    d = fixture_dir("mock-switch")
    out = tmp_path / "records.csv"
    subprocess.run([sys.executable, str(TOOLS / "records.py"),
                    "--run", str(d / "run.json"), "--trace", str(d / "trace.jsonl"),
                    "--schedule", str(d / "config-schedule.json"),
                    "--table", "calibrated", "--telemetry", "names", "--out", str(out)], check=True)
    assert out.read_bytes() == (d / "expected.csv").read_bytes()


# ---- 10.4 decision 2: the schema check by signature

def _walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def test_the_signature_covers_every_field_and_bound_the_schema_names():
    """A field or a bound added to the schema must be added to the signature: the cache is sound only while
    the signature keeps everything the schema can reject a row on."""
    from harness import records as rec
    schema = rec._schema()
    assert set(schema["properties"]) == rec.SIGNATURE_FIELDS
    bounds = set()
    for node in _walk(schema):
        for k in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"):
            if k in node:
                bounds.add(node[k])
        for k in ("minLength", "maxLength"):
            if k in node:
                assert node[k] in (0, 1), node            # a free string: empty or not
    assert bounds <= {0, 1, 5}
    entity_consts = {n["const"] for n in _walk(schema) if isinstance(n.get("entity"), dict)
                     for n in [n["entity"]] if "const" in n}
    assert entity_consts <= rec._ENTITY_CONSTS


def test_rows_sharing_a_signature_are_all_valid_or_all_invalid():
    import random
    from harness import records as rec
    import jsonschema
    validator = jsonschema.Draft202012Validator(rec._schema())
    base = []
    for mock in MOCKS:
        d = FIXTURES / mock
        rows, _ = build(d / "run.json", d / "trace.jsonl")
        base.extend(rows[:200])
    rng = random.Random(1042)
    values = [-7, -1, 0, 1, 2, 4, 5, 6, 9, 10 ** 9, "", "x", "fixed", "schedule", "lane", "recognizer", "wake",
              "timer", "a:b", "MLFQ", True, 1.5, None]
    rows = list(base)
    for _ in range(4000):
        r = dict(rng.choice(base))
        for _k in range(rng.randint(1, 3)):
            key = rng.choice(list(rec.SIGNATURE_FIELDS) + ["extra"])
            v = rng.choice(values)
            if v is None:
                r.pop(key, None)
            else:
                r[key] = v
        rows.append(r)
    seen = {}
    for r in rows:
        clean = {k: v for k, v in r.items() if v not in ("", None)}
        ok = validator.is_valid(clean)
        sig = rec._signature(clean)
        assert seen.setdefault(sig, ok) == ok, clean
    assert True in seen.values() and False in seen.values()


def test_the_schema_check_raises_on_the_first_invalid_row_as_before(tmp_path):
    from harness import records as rec
    d = FIXTURES / "mock-office"
    rows, _ = build(d / "run.json", d / "trace.jsonl")
    rec.validate_rows(rows)
    bad = [dict(r) for r in rows]
    bad[7]["t"] = -3
    bad[9]["metric"] = "nope"
    with pytest.raises(ValueError, match=r"records row 7: t: "):
        rec.validate_rows(bad)


def test_the_frame_built_a_chunk_at_a_time_equals_the_frame_of_the_whole_list(monkeypatch):
    """10.4 decision 2: compute_aggregates(consume=True) frees the rows as its frame is built; same frame, same
    aggregates, the list emptied."""
    import pandas as pd
    from harness import aggregates as agg
    rows = []
    for mock in MOCKS:
        d = FIXTURES / mock
        part, _ = build(d / "run.json", d / "trace.jsonl")
        rows.extend(part)
    monkeypatch.setattr(agg, "FRAME_CHUNK", 37)                 # chunks that split the metrics and the columns
    whole = pd.DataFrame(rows)
    copy = list(rows)
    chunked = agg._frame_consuming(copy)
    assert copy == [] and whole.equals(chunked)
    assert list(whole.columns) == list(chunked.columns) and list(whole.dtypes) == list(chunked.dtypes)
    d = FIXTURES / "mock-office"
    one, _ = build(d / "run.json", d / "trace.jsonl")
    consumed = list(one)
    assert agg.compute_aggregates(consumed, consume=True) == agg.compute_aggregates(one) and consumed == []
