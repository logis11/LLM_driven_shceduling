"""Sub-task 8.3: the guard spec (schema + lint), the eight guards over the
hand-written `mock-guards` fixture (records, aggregates, schedule, log, ground
truth in; the `guards` file out, byte for byte), the two pair guards over
synthetic runs, and the manifest CLI."""

import copy
import hashlib
import json
import subprocess
import sys

import pytest
import yaml

from conftest import REPO, TOOLS
from harness import aggregates as agg
from harness import records
from harness.guards import (COLUMNS, GUARDS, GUARDS_SCHEMA, SCHEMA_PATH, SPEC_PATH, Run,
                            evaluate, lint_spec, load_spec)
from harness.outputs import read_csv, validate_rows, write_csv

MG = TOOLS / "tests" / "fixtures" / "mock-guards"
RECIPES = REPO / "dataset" / "timelines" / "coreset"
IDENTITY = {"workload_id": "mock-guards", "condition": "llm_vocab", "table": "prior",
            "seed": "", "boot_default": ""}


@pytest.fixture(scope="module")
def spec():
    return load_spec(SPEC_PATH)


def _records(tmp_path, log="recognition-log.json"):
    """mock-guards' records from the writer, its aggregates, and its Run."""
    rows, msgs = records.build(MG / "run.json", MG / "trace.jsonl", table="prior",
                               schedule_path=MG / "config-schedule.json")
    out = tmp_path / "records.csv"
    records.write_csv(rows, out)
    aggs = agg.compute_aggregates(records.read_csv(out))
    run = Run(**IDENTITY, records=out, schedule=MG / "config-schedule.json", log=MG / log,
              workload=MG / "workload.json", rerun_trace=MG / "trace.jsonl", guard_messages=msgs)
    return run, aggs


def _row(rows, guard, **ident):
    found = [r for r in rows if r["guard"] == guard and all(r[k] == v for k, v in ident.items())]
    assert len(found) == 1, (guard, ident, found)
    return found[0]


# ------------------------------------------------------------------ the spec

def test_committed_spec_lints_clean():
    assert lint_spec(SPEC_PATH, SCHEMA_PATH, RECIPES) == []


def test_registry_is_the_eight_guards_in_spec_order(spec):
    assert tuple(g["id"] for g in spec["guards"]) == GUARDS
    assert len(GUARDS) == 8


def _lint(tmp_path, mutate):
    doc = copy.deepcopy(load_spec(SPEC_PATH))
    mutate(doc)
    p = tmp_path / "guard-spec.yaml"
    p.write_text(yaml.safe_dump(doc, allow_unicode=True))
    return lint_spec(p, SCHEMA_PATH, RECIPES)


def test_lint_rejects_an_id_the_code_does_not_implement(tmp_path):
    def mutate(doc):
        doc["guards"][0]["id"] = "random_beats_oracle"
    errors = _lint(tmp_path, mutate)
    assert any("random_beats_oracle" in e and "registry" in e for e in errors)
    assert any("provenance_share" in e for e in errors)


def test_lint_rejects_an_empty_grounding(tmp_path):
    def mutate(doc):
        doc["guards"][2]["grounding"] = "  "
    assert any("grounding" in e for e in _lint(tmp_path, mutate))


def test_lint_rejects_pairs_that_drift_from_the_recipe(tmp_path):
    def mutate(doc):
        doc["pairs"][0]["b"] = "c2-p9b"
    assert any("c2-pairs" in e or "recipe" in e for e in _lint(tmp_path, mutate))


def test_lint_rejects_a_missing_threshold_on_a_bounded_guard(tmp_path):
    def mutate(doc):
        doc["guards"][0]["threshold"] = None            # provenance_share, direction below
    assert any("threshold" in e for e in _lint(tmp_path, mutate))


# --------------------------------------------------------------- the fixture

def test_mock_guards_records_byte_for_byte(tmp_path):
    rows, msgs = records.build(MG / "run.json", MG / "trace.jsonl", table="prior",
                               schedule_path=MG / "config-schedule.json")
    assert msgs == []
    out = tmp_path / "records.csv"
    records.write_csv(rows, out)
    assert out.read_bytes() == (MG / "expected.csv").read_bytes()


def test_mock_guards_file_byte_for_byte(tmp_path, spec):
    run, aggs = _records(tmp_path)
    rows = evaluate([run], spec, aggs)
    out = tmp_path / "guards.csv"
    write_csv(rows, COLUMNS, out)
    assert out.read_bytes() == (MG / "expected-guards.csv").read_bytes()


def test_expected_guards_validate_against_the_schema():
    validate_rows(read_csv(MG / "expected-guards.csv", COLUMNS), GUARDS_SCHEMA)


def test_every_run_gets_one_row_per_guard(tmp_path, spec):
    run, aggs = _records(tmp_path)
    rows = evaluate([run], spec, aggs)
    assert [r["guard"] for r in rows] == list(GUARDS)


def test_starvation_fails_past_its_threshold(tmp_path, spec):
    """The fixture's `batch` waits 1.95 s, inside the 30 s watchdog (9.11 D7); the
    same run read against a 1 s threshold fails, naming the task."""
    run, aggs = _records(tmp_path)
    tight = copy.deepcopy(spec)
    for g in tight["guards"]:
        if g["id"] == "starvation_floor":
            g["threshold"] = 1000000
    starve = _row(evaluate([run], tight, aggs), "starvation_floor")
    assert starve["result"] == "fail" and starve["reason"].startswith("batch:")


def test_the_rules_show_in_the_rows(tmp_path, spec):
    run, aggs = _records(tmp_path)
    rows = evaluate([run], spec, aggs)
    prov = _row(rows, "provenance_share")
    assert prov["result"] == "pass" and prov["value"] == "0.003733333333"
    age = _row(rows, "config_age")
    assert age["result"] == "fail" and age["value"] == "40000.000000000000"
    assert "80000" in age["reason"] and "query 1" in age["reason"]
    starve = _row(rows, "starvation_floor")
    assert starve["result"] == "pass" and starve["value"] == "1950000.000000000000"
    assert starve["threshold"] == "30000000.000000000000"
    det = _row(rows, "determinism")
    assert det["result"] == "pass"
    assert det["partner"] == hashlib.sha256((MG / "trace.jsonl").read_bytes()).hexdigest()
    assert _row(rows, "utilisation_sanity")["value"] == "0.836000000000"
    assert _row(rows, "tick_count")["result"] == "pass"
    assert _row(rows, "validation_matches_provenance")["result"] == "pass"
    assert _row(rows, "c2_pair")["result"] == "not_applicable"


def test_validation_mismatch_names_the_first_index(tmp_path, spec):
    run, aggs = _records(tmp_path, log="recognition-log-mismatch.json")
    row = _row(evaluate([run], spec, aggs), "validation_matches_provenance")
    assert row["result"] == "fail" and row["value"] == "1.000000000000"
    assert "index 1" in row["reason"] and "unmodified" in row["reason"] and "held" in row["reason"]


def test_determinism_fails_on_a_differing_rerun(tmp_path, spec):
    run, aggs = _records(tmp_path)
    other = tmp_path / "rerun.jsonl"
    other.write_bytes((MG / "trace.jsonl").read_bytes() + b"\n")
    run = Run(**{**run.__dict__, "rerun_trace": other})
    row = _row(evaluate([run], spec, aggs), "determinism")
    assert row["result"] == "fail" and row["partner"] == hashlib.sha256(other.read_bytes()).hexdigest()


def test_missing_inputs_fail_with_a_reason(tmp_path, spec):
    run, aggs = _records(tmp_path)
    bare = Run(**{**run.__dict__, "rerun_trace": None, "guard_messages": None, "log": None})
    rows = evaluate([bare], spec, [])
    for guard in ("provenance_share", "starvation_floor", "utilisation_sanity", "determinism",
                  "tick_count", "validation_matches_provenance", "config_age"):
        row = _row(rows, guard)
        assert row["result"] == "fail" and row["reason"], guard


def test_tick_count_carries_the_primitives_messages(tmp_path, spec):
    run, aggs = _records(tmp_path)
    run = Run(**{**run.__dict__, "guard_messages": ["chain a: tail b completed 3 iteration(s) for 4 head tick(s) inside the window"]})
    row = _row(evaluate([run], spec, aggs), "tick_count")
    assert row["result"] == "fail" and row["value"] == "1.000000000000" and "chain a" in row["reason"]


def test_fixed_marks_the_recognition_guards_not_applicable(tmp_path, spec):
    d = TOOLS / "tests" / "fixtures" / "mock-office"
    rows, msgs = records.build(d / "run.json", d / "trace.jsonl")
    out = tmp_path / "office.csv"
    records.write_csv(rows, out)
    aggs = agg.compute_aggregates(records.read_csv(out))
    run = Run(workload_id="mock-office", condition="fixed", table="", seed="", boot_default="",
              records=out, schedule=None, log=None, workload=None, rerun_trace=d / "trace.jsonl",
              guard_messages=msgs)
    got = evaluate([run], spec, aggs)
    for guard in ("provenance_share", "config_age", "validation_matches_provenance"):
        assert _row(got, guard)["result"] == "not_applicable", guard
    assert _row(got, "starvation_floor")["result"] == "pass"
    assert _row(got, "utilisation_sanity")["result"] == "pass"
    assert _row(got, "determinism")["result"] == "pass"


def test_utilisation_zero_fails_only_where_the_file_has_terms(tmp_path, spec):
    run, aggs = _records(tmp_path)
    zero = [dict(r, value="0.000000000000") if r["aggregate"] == "utilisation" else r for r in aggs]
    scoring = {"files": {"mock-guards": {"terms": [{"entity": "editor", "metric": "ready_wait",
                                                    "cause": "wake", "aggregate": "p99",
                                                    "direction": "lower", "weight": 1.0}]}}}
    assert _row(evaluate([run], spec, zero), "utilisation_sanity")["result"] == "pass"
    assert _row(evaluate([run], spec, zero, scoring), "utilisation_sanity")["result"] == "fail"


# ------------------------------------------------------------- pair guards

BOOT_CFG = {"algorithm": "MLFQ", "params": {"num_queues": 3, "timeslice_us": 10000,
                                              "timeslice_growth": 2, "boost_interval_us": 100000},
            "batch_bandwidth_cap": None}
LOTTERY_CFG = {"algorithm": "LOTTERY", "params": {"batch_share": 0.333, "timeslice_us": 10000},
               "batch_bandwidth_cap": 0.333}
MLFQ_FLOOR_CFG = {"algorithm": "MLFQ", "params": BOOT_CFG["params"], "batch_bandwidth_cap": 0.05}


def _pair_run(tmp_path, wid, condition, config, seed="", boot="", schedule=True,
              wanted=None, early=None):
    """A run of a pair member: a two-segment workload whose second segment carries the
    label (`wanted` defaults to true for an `a` file, false for a `b` file) and a config
    schedule of the boot entry, an optional entry inside the first segment (`early`) and
    `config` stamped at the second segment's start (9.14 decision 7: the guard reads the
    configuration sequence over the differing segment)."""
    stem = f"{wid}-{condition}-{seed or 'x'}-{boot or 'x'}"
    out = tmp_path / f"{stem}.csv"
    records.write_csv([{"workload_id": wid, "condition": condition, "table": "prior", "seed": seed,
                        "boot_default": boot, "sim": "mock@0", "source_sha256": "0" * 64,
                        "entity": "lane", "metric": "busy", "t": 100, "value": 50}], out)
    if wanted is None:
        wanted = wid.endswith("a")
    workload = tmp_path / f"{stem}.workload.json"
    workload.write_text(json.dumps({"meta": {"id": wid}, "events": [], "ground_truth": [
        {"t_start": 0, "t_end": 60, "mode": "dev", "attributes": {"background_wanted": True}},
        {"t_start": 60, "t_end": 120, "mode": "ml-train", "attributes": {"background_wanted": wanted}}]}))
    entries = [{"t_us": 0, "config": BOOT_CFG, "provenance": "fallback"}]
    if early is not None:
        entries.append({"t_us": 30, "config": early, "provenance": "unmodified"})
    entries.append({"t_us": 60, "config": config, "provenance": "unmodified"})
    sched = tmp_path / f"{stem}.schedule.json"
    sched.write_text(json.dumps({"workload_id": wid, "condition": condition, "schedule": entries}))
    return Run(workload_id=wid, condition=condition, table="prior", seed=seed, boot_default=boot,
               records=out, schedule=sched if schedule else None, log=None, workload=workload,
               rerun_trace=None, guard_messages=[], trace=None)


def test_c2_pair_under_oracle_fails_on_identical_configuration_sequences(tmp_path, spec):
    runs = [_pair_run(tmp_path, "c2-p1a", "oracle", LOTTERY_CFG),
            _pair_run(tmp_path, "c2-p1b", "oracle", LOTTERY_CFG)]
    rows = evaluate(runs, spec, [])
    a = _row(rows, "c2_pair", workload_id="c2-p1a")
    b = _row(rows, "c2_pair", workload_id="c2-p1b")
    assert a["result"] == "fail" and a["partner"] == "c2-p1b" and "identical configuration" in a["reason"]
    assert b["result"] == "fail" and b["partner"] == "c2-p1a"


def test_c2_pair_under_oracle_passes_on_different_configurations(tmp_path, spec):
    runs = [_pair_run(tmp_path, "c2-p1a", "oracle", LOTTERY_CFG),
            _pair_run(tmp_path, "c2-p1b", "oracle", MLFQ_FLOOR_CFG)]
    row = _row(evaluate(runs, spec, []), "c2_pair", workload_id="c2-p1a")
    assert row["result"] == "pass" and row["partner"] == "c2-p1b"


def test_c2_pair_reads_the_differing_segment_only(tmp_path, spec):
    """Configurations that differ only inside the first segment, where the labels agree,
    do not count: over the differing segment the sequences are identical."""
    runs = [_pair_run(tmp_path, "c2-p1a", "llm_vocab", LOTTERY_CFG, early=MLFQ_FLOOR_CFG),
            _pair_run(tmp_path, "c2-p1b", "llm_vocab", LOTTERY_CFG)]
    assert _row(evaluate(runs, spec, []), "c2_pair", workload_id="c2-p1a")["result"] == "fail"


def test_c2_pair_under_fixed_and_random_is_not_applicable(tmp_path, spec):
    """9.11 D15: no pair's events are identical apart from the label, so `fixed` has
    nothing to require; `random` ignores telemetry."""
    runs = [_pair_run(tmp_path, "c2-p1a", "fixed", BOOT_CFG), _pair_run(tmp_path, "c2-p1b", "fixed", BOOT_CFG),
            _pair_run(tmp_path, "c2-p2a", "random", LOTTERY_CFG, seed="1"),
            _pair_run(tmp_path, "c2-p2b", "random", LOTTERY_CFG, seed="1")]
    rows = evaluate(runs, spec, [])
    assert _row(rows, "c2_pair", workload_id="c2-p1a")["result"] == "not_applicable"
    assert _row(rows, "c2_pair", workload_id="c2-p2a")["result"] == "not_applicable"


def test_c2_pair_without_a_schedule_fails_with_a_reason(tmp_path, spec):
    runs = [_pair_run(tmp_path, "c2-p1a", "oracle", LOTTERY_CFG, schedule=False),
            _pair_run(tmp_path, "c2-p1b", "oracle", MLFQ_FLOOR_CFG)]
    row = _row(evaluate(runs, spec, []), "c2_pair", workload_id="c2-p1a")
    assert row["result"] == "fail" and "schedule" in row["reason"]


def test_c2_pair_with_no_differing_segment_fails(tmp_path, spec):
    runs = [_pair_run(tmp_path, "c2-p1a", "oracle", LOTTERY_CFG, wanted=True),
            _pair_run(tmp_path, "c2-p1b", "oracle", MLFQ_FLOOR_CFG, wanted=True)]
    row = _row(evaluate(runs, spec, []), "c2_pair", workload_id="c2-p1a")
    assert row["result"] == "fail" and "differs in no segment" in row["reason"]


def test_c2_pair_partner_is_matched_on_seed_and_boot_default(tmp_path, spec):
    runs = [_pair_run(tmp_path, "c2-p1a", "oracle", LOTTERY_CFG, boot="alt"),
            _pair_run(tmp_path, "c2-p1b", "oracle", MLFQ_FLOOR_CFG, boot="")]
    row = _row(evaluate(runs, spec, []), "c2_pair", workload_id="c2-p1a")
    assert row["result"] == "fail" and "partner" in row["reason"] and row["partner"] == ""


def test_the_idle_download_variant_is_not_a_pair(spec):
    """9.14 decision 7: the lint's pair rule reads the recipes' label-changing c2 variants;
    c2-p2a-idle changes a task's entry and no label."""
    from harness.scoring import label_changing_variants
    pairs = {v: b for v, b in label_changing_variants(RECIPES).items() if v.startswith("c2-")}
    assert pairs == {"c2-p1b": "c2-p1a", "c2-p2b": "c2-p2a", "c2-p3b": "c2-p3a"}
    assert {p["b"]: p["a"] for p in spec["pairs"]} == pairs


# -------------------------------------------------------------------- CLIs

def test_cli_reproduces_the_fixture_and_exits_2_on_a_fail(tmp_path):
    rows, msgs = records.build(MG / "run.json", MG / "trace.jsonl", table="prior",
                               schedule_path=MG / "config-schedule.json")
    rec = tmp_path / "records.csv"
    records.write_csv(rows, rec)
    aggs = tmp_path / "aggregates.csv"
    write_csv(agg.compute_aggregates(records.read_csv(rec)), agg.COLUMNS, aggs)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "aggregates": str(aggs),
        "runs": [{**IDENTITY, "records": str(rec), "schedule": str(MG / "config-schedule.json"),
                  "log": str(MG / "recognition-log.json"), "workload": str(MG / "workload.json"),
                  "rerun_trace": str(MG / "trace.jsonl"), "guard_messages": msgs}]}))
    out = tmp_path / "guards.csv"
    r = subprocess.run([sys.executable, str(TOOLS / "guards.py"), "--manifest", str(manifest),
                        "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 2, r.stderr
    assert out.read_bytes() == (MG / "expected-guards.csv").read_bytes()
    assert "1 fail" in r.stdout


def test_lint_cli_is_clean_on_the_committed_spec():
    r = subprocess.run([sys.executable, str(TOOLS / "guards_lint.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "lint clean" in r.stdout
