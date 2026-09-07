"""Driver table lint — structure, legality, and the byte-identical pair check."""

import json

import pytest

from conftest import REPO, clone, row, schema_default_params
from drivertable.config_schema import ALGORITHMS, MODES
from drivertable.lint import lint_table

SCHEMA = REPO / "daemon" / "driver-table" / "schema" / "driver-table.schema.json"


def errors_of(table_file, table):
    return lint_table(table_file(table), SCHEMA)


def test_valid_prior_table_is_clean(table_file, prior):
    assert errors_of(table_file, prior) == []


def test_valid_calibrated_table_is_clean(table_file, calibrated):
    assert errors_of(table_file, calibrated) == []


def test_sixteen_modes_two_attributes_is_thirty_two_rows(prior):
    assert len(MODES) == 16 and len(prior["rows"]) == 32


@pytest.mark.parametrize("expect,mutate", [
    ("row (gaming, background_wanted=false) missing",
     lambda t: t["rows"].remove(row(t, "gaming", False))),
    ("duplicate row (gaming, background_wanted=true)",
     lambda t: t["rows"].append(clone(row(t, "gaming", True)))),
    ("mode 'interactive' not one of",
     lambda t: row(t, "office", True).update(mode="interactive")),
    ("default 'EDF' has no entry",
     lambda t: row(t, "office", True).update(default="EDF")),
    ("entries/MLFQ/params: missing 'boost_interval_us'",
     lambda t: row(t, "office", True)["entries"]["MLFQ"]["params"].pop("boost_interval_us")),
    ("entries/MLFQ/params: unexpected 'batch_share'",
     lambda t: row(t, "office", True)["entries"]["MLFQ"]["params"].update(batch_share=0.1)),
    ("entries/MLFQ/params/num_queues: num_queues 9 outside [2, 8]",
     lambda t: row(t, "office", True)["entries"]["MLFQ"]["params"].update(num_queues=9)),
    ("timeslice_us must be an integer",
     lambda t: row(t, "office", True)["entries"]["MLFQ"]["params"].update(timeslice_us=2000.5)),
    ("batch_bandwidth_cap 0.96 outside [0.05, 0.95]",
     lambda t: row(t, "office", True).update(batch_bandwidth_cap=0.96)),
    ("entries: unexpected 'CFS'",
     lambda t: row(t, "office", True)["entries"].update(CFS={"params": {}, "basis": "theory", "justification": "x"})),
    ("basis 'guess' not one of",
     lambda t: row(t, "office", True)["entries"]["MLFQ"].update(basis="guess")),
    ("row (office, background_wanted=true): missing 'justification'",
     lambda t: row(t, "office", True).pop("justification")),
    ("entry MLFQ: justification required unless basis is schema-default",
     lambda t: row(t, "office", True)["entries"]["MLFQ"].pop("justification")),
    ("role 'v0' not one of",
     lambda t: t.update(role="v0")),
])
def test_prior_table_rules(table_file, prior, expect, mutate):
    mutate(prior)
    errors = errors_of(table_file, prior)
    assert any(expect in e for e in errors), errors


def test_schema_default_entry_needs_no_justification(table_file, prior):
    r = row(prior, "office", True)
    r["entries"]["EDF"] = {"params": schema_default_params("EDF"), "basis": "schema-default"}
    r["default"] = "EDF"
    prior["role"] = "calibrated"  # prior allows one entry only; use calibrated shape…
    for alg in ("LOTTERY", "FIFO"):
        r["entries"][alg] = {"params": schema_default_params(alg), "basis": "schema-default"}
    # …but every other row must then be full too; so check only this row's messages
    errors = [e for e in errors_of(table_file, prior) if "(office, background_wanted=true)" in e]
    assert errors == []


def test_prior_table_has_exactly_one_entry_per_row(table_file, prior):
    r = row(prior, "office", True)
    r["entries"]["EDF"] = {"params": schema_default_params("EDF"), "basis": "theory",
                           "justification": "x"}
    errors = errors_of(table_file, prior)
    assert any("prior table: row (office, background_wanted=true) must carry exactly one entry" in e
               for e in errors), errors


def test_calibrated_table_must_be_full(table_file, calibrated):
    row(calibrated, "office", True)["entries"].pop("FIFO")
    errors = errors_of(table_file, calibrated)
    assert any("calibrated table: row (office, background_wanted=true) missing entry for FIFO" in e
               for e in errors), errors


def test_lottery_batch_share_must_not_exceed_cap(table_file, calibrated):
    r = row(calibrated, "office", False)          # cap 0.05
    r["entries"]["LOTTERY"]["params"]["batch_share"] = 0.10
    errors = errors_of(table_file, calibrated)
    assert any("LOTTERY batch_share 0.1 exceeds batch_bandwidth_cap 0.05" in e for e in errors), errors


def test_null_cap_lifts_the_batch_share_bound(table_file, calibrated):
    r = row(calibrated, "office", False)
    r["batch_bandwidth_cap"] = None
    r["entries"]["LOTTERY"]["params"]["batch_share"] = 0.90
    assert errors_of(table_file, calibrated) == []


def test_byte_identical_wanted_pair_fails(table_file, prior):
    row(prior, "gaming", False)["batch_bandwidth_cap"] = row(prior, "gaming", True)["batch_bandwidth_cap"]
    errors = errors_of(table_file, prior)
    assert any("gaming: wanted=true and wanted=false default configurations are byte-identical" in e
               for e in errors), errors


def test_json_schema_matches_config_schema_data():
    """Drift guard: the hand-written JSON schema and the importable field data agree."""
    schema = json.loads(SCHEMA.read_text())
    entries = schema["$defs"]["row"]["properties"]["entries"]["properties"]
    assert set(entries) == set(ALGORITHMS)
    for alg, fields in ALGORITHMS.items():
        params = entries[alg]["properties"]["params"]
        assert set(params.get("properties", {})) == set(fields)
        assert set(params.get("required", [])) == set(fields)
        assert params.get("additionalProperties") is False
        for name, spec in fields.items():
            p = params["properties"][name]
            assert p["type"] == spec.json_type
            assert p["minimum"] == spec.lo and p["maximum"] == spec.hi
    assert set(schema["$defs"]["row"]["properties"]["mode"]["enum"]) == set(MODES)
