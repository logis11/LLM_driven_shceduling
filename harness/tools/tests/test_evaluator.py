"""The RQ0 gate evaluator and the report (8.7 spec, decisions 5, 9–13): the
`mock-experiment` fixture's three variants against the expected reports, the
refusals, the reporting lines, and the command."""

import json
import subprocess
import sys

import pytest
import yaml

from conftest import FIXTURES, REPO, TOOLS
from harness import guards as guards_mod
from harness import scorer
from harness.evaluator import REPORT_SCHEMA, GateError, evaluate, render, write_report
from harness.outputs import read_csv, write_csv

FX = FIXTURES / "mock-experiment"
MS = FIXTURES / "mock-scores"
INPUTS = {"aggregates": MS / "expected-aggregates.csv", "scores": MS / "expected-scores.csv",
          "guards": FX / "guards.csv", "grades": FX / "grades.csv"}


def _evaluate(spec=FX / "experiment.yaml", **override):
    paths = dict(INPUTS); paths.update(override)
    return evaluate(spec, paths["aggregates"], paths["scores"], paths["guards"], paths["grades"], REPO)


def _gap(report, boot=""):
    return next(r for r in report["gaps"] if r["workload_id"] == "mock-score" and r["boot_default"] == boot)


def _line(report, kind):
    return next(l for l in report["lines"] if l["type"] == kind)


# ------------------------------------------------------------ the fixture

def test_pass_variant_reproduces_the_expected_report(tmp_path):
    report = _evaluate()
    assert report["verdict"] == "pass"
    out = tmp_path / "report.json"
    write_report(report, out)
    assert out.read_bytes() == (FX / "expected-report.json").read_bytes()
    assert render(report) == (FX / "expected-report.md").read_text()


def test_fail_and_invalid_variants_reproduce_their_expected_reports(tmp_path):
    for name in ("fail", "invalid"):
        report = _evaluate(FX / f"experiment-{name}.yaml")
        assert report["verdict"] == name
        out = tmp_path / f"{name}.json"
        write_report(report, out)
        assert out.read_bytes() == (FX / f"expected-report-{name}.json").read_bytes()


def test_reports_validate_against_the_report_schema():
    import jsonschema
    schema = json.loads(REPORT_SCHEMA.read_text())
    for name in ("", "-fail", "-invalid"):
        jsonschema.Draft202012Validator(schema).validate(
            json.loads((FX / f"expected-report{name}.json").read_text()))


# -------------------------------------------------------------- the numbers

def test_the_gap_is_one_minus_the_seed_mean_over_the_weight_sum():
    report = _evaluate()
    g = _gap(report)
    assert g["reference_score"] == "2.500000"
    assert sorted((s["seed"], s["score"]) for s in g["compared_scores"]) == \
        [("s1", "1.639359"), ("s2", "0.433333")]
    assert g["compared_mean"] == "1.036346"
    assert g["gap"] == "0.585462" and g["meets_g"] is True
    assert g["all_no_headroom"] is False and g["n_no_headroom"] == 1
    assert g["random_beats_oracle"] is False
    alt = _gap(report, "alt")
    assert alt["compared_mean"] == "0.872024" and alt["gap"] == "0.651190"
    assert report["criterion"] == {"type": "k_of_n_gap", "k": 1, "g": "0.500000", "reference": "oracle",
                                   "compared": "random", "seed_statistic": "mean"}
    assert report["verdict_detail"] == {"met": 1, "judging": 1, "k": 1, "invalid_runs": []}


def test_the_fail_variant_fails_on_the_primary_and_passes_under_alt():
    report = _evaluate(FX / "experiment-fail.yaml")
    assert report["verdict"] == "fail"
    assert _gap(report)["meets_g"] is False and _gap(report, "alt")["meets_g"] is True
    assert _line(report, "sensitivity")["rows"] == [
        {"boot_default": "", "met": 0, "judging": 1, "verdict": "fail", "available": True},
        {"boot_default": "alt", "met": 1, "judging": 1, "verdict": "pass", "available": True}]


def test_the_invalid_variant_names_the_guard_and_the_run():
    report = _evaluate(FX / "experiment-invalid.yaml")
    assert report["verdict"] == "invalid"
    assert report["verdict_detail"]["invalid_runs"] == [
        {"workload_id": "mock-score", "condition": "random", "table": "prior", "seed": "s2",
         "boot_default": "", "guard": "starvation_floor"}]
    assert _gap(report)["gap"] == "0.585462"                       # still computed and reported
    fails = [r for r in report["guards"] if r["result"] == "fail"]
    assert len(fails) == 1 and fails[0]["exempt"] is False and fails[0]["invalidating"] is True


def test_an_exempt_failure_is_reported_and_does_not_invalidate():
    report = _evaluate()
    fails = [r for r in report["guards"] if r["result"] == "fail"]
    assert len(fails) == 1 and fails[0]["exempt"] is True and fails[0]["invalidating"] is False
    assert fails[0]["exemption_reason"].startswith("The fixture's random s2 run")


def test_a_failure_on_an_alternative_default_run_marks_its_count_unavailable(tmp_path):
    rows = read_csv(FX / "guards.csv", guards_mod.COLUMNS)
    for r in rows:
        if r["boot_default"] == "alt" and r["guard"] == "utilisation_sanity":
            r.update(result="fail", value="1.200000000000", reason="busy above T_end")
    p = tmp_path / "guards.csv"
    write_csv(rows, guards_mod.COLUMNS, p)
    report = _evaluate(guards=p)
    assert report["verdict"] == "pass"                              # the verdict is untouched
    alt = next(r for r in _line(report, "sensitivity")["rows"] if r["boot_default"] == "alt")
    assert alt["available"] is False and alt["verdict"] is None
    assert any(r["result"] == "fail" and r["boot_default"] == "alt" and not r["invalidating"]
               for r in report["guards"])


def test_random_beats_oracle_is_flagged_when_the_mean_exceeds_the_reference(tmp_path):
    rows = read_csv(MS / "expected-scores.csv", scorer.COLUMNS)
    for r in rows:
        if r["level"] == "file" and r["condition"] == "random" and r["boot_default"] == "":
            r["score"] = "2.600000"
    p = tmp_path / "scores.csv"
    write_csv(rows, scorer.COLUMNS, p)
    report = _evaluate(scores=p)
    assert _gap(report)["random_beats_oracle"] is True and _gap(report)["gap"] == "-0.040000"
    assert _line(report, "random_beats_oracle")["rows"] == [{"workload_id": "mock-score", "flagged": True,
                                                            "gap": "-0.040000"}]


def test_a_judging_file_with_no_headroom_everywhere_is_marked_and_does_not_meet_g(tmp_path):
    rows = read_csv(MS / "expected-scores.csv", scorer.COLUMNS)
    for r in rows:
        if r["level"] == "file":
            r["n_no_headroom"] = r["n_terms"]
    p = tmp_path / "scores.csv"
    write_csv(rows, scorer.COLUMNS, p)
    report = _evaluate(scores=p)
    assert _gap(report)["all_no_headroom"] is True and _gap(report)["meets_g"] is False
    assert report["verdict"] == "fail"


def test_the_floor_band_recomputes_the_verdict_count_per_floor():
    line = _line(_evaluate(), "floor_band")
    assert line["rows"] == [
        {"latency_floor_us": 500, "met": 1, "judging": 1, "verdict": "pass"},
        {"latency_floor_us": 1000, "met": 1, "judging": 1, "verdict": "pass"},
        {"latency_floor_us": 40000, "met": 0, "judging": 1, "verdict": "fail"}]
    band = next(r for r in line["gaps"] if r["latency_floor_us"] == 40000)
    assert band["gap"] == "0.130000"


def test_exclusion_and_headline_lines_read_the_grades_file():
    report = _evaluate()
    ex = _line(report, "exclusion_accuracy")["rows"]
    assert {"condition": "random", "table": "prior", "axis": "attribute", "statistic": "balanced_accuracy",
            "excluded": "0.750000", "included": "0.625000", "n_excluded": 2, "n_included": 4} in ex
    head = _line(report, "layer1_headline")
    assert [r["condition"] for r in head["rows"]] == ["oracle", "random"]
    rnd = next(r for r in head["rows"] if r["condition"] == "random")
    assert rnd["balanced_accuracy"] == "0.750000" and rnd["n_seeds"] == 2
    assert {"seed": "s2", "truth": "true", "predicted": "true", "count": 2} in rnd["confusion"]


def test_the_note_line_is_bound_to_its_workload():
    note = _line(_evaluate(), "note")
    assert note["workload_id"] == "mock-score" and note["text"].startswith("A pre-registered note")


def test_provenance_breakdown_sits_beside_every_scored_run():
    report = _evaluate()
    keys = {(r["condition"], r["seed"], r["boot_default"]) for r in report["provenance"]}
    assert ("random", "s1", "") in keys and ("fixed", "", "alt") in keys
    row = next(r for r in report["provenance"] if r["condition"] == "fixed" and r["boot_default"] == "alt")
    assert row["time_share_fallback"] == "1.000000000000" and row["fallback_share"] == "1.000000000000"


# --------------------------------------------------------------- refusals

def test_a_pin_mismatch_is_a_refusal(tmp_path):
    spec = yaml.safe_load((FX / "experiment.yaml").read_text())
    spec["pins"]["driver_table"]["sha256"] = "f" * 64
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(spec, sort_keys=False))
    with pytest.raises(GateError, match="driver_table"):
        _evaluate(p)


def test_a_missing_criterion_run_is_a_refusal(tmp_path):
    rows = [r for r in read_csv(MS / "expected-scores.csv", scorer.COLUMNS)
            if not (r["condition"] == "random" and r["seed"] == "s2")]
    p = tmp_path / "scores.csv"
    write_csv(rows, scorer.COLUMNS, p)
    with pytest.raises(GateError, match="1 random seed"):
        _evaluate(scores=p)
    rows = [r for r in read_csv(FX / "guards.csv", guards_mod.COLUMNS) if r["condition"] != "oracle"]
    p = tmp_path / "guards.csv"
    write_csv(rows, guards_mod.COLUMNS, p)
    with pytest.raises(GateError, match="oracle"):
        _evaluate(guards=p)


# ------------------------------------------------------------- the command

def _cli(spec, tmp_path, **override):
    paths = dict(INPUTS); paths.update(override)
    return subprocess.run([sys.executable, str(TOOLS / "evaluate.py"), "--spec", str(spec),
                           "--aggregates", str(paths["aggregates"]), "--scores", str(paths["scores"]),
                           "--guards", str(paths["guards"]), "--grades", str(paths["grades"]),
                           "--out-report", str(tmp_path / "report.json"),
                           "--out-render", str(tmp_path / "report.md")],
                          capture_output=True, text=True)


def test_cli_writes_both_files_and_exits_by_verdict(tmp_path):
    proc = _cli(FX / "experiment.yaml", tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert (tmp_path / "report.json").read_bytes() == (FX / "expected-report.json").read_bytes()
    assert (tmp_path / "report.md").read_text() == (FX / "expected-report.md").read_text()
    assert _cli(FX / "experiment-fail.yaml", tmp_path).returncode == 2
    assert _cli(FX / "experiment-invalid.yaml", tmp_path).returncode == 2


def test_cli_refuses_without_writing(tmp_path):
    spec = yaml.safe_load((FX / "experiment.yaml").read_text())
    spec["pins"]["dataset"]["sha256"] = "0" * 64
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(spec, sort_keys=False))
    proc = _cli(p, tmp_path)
    assert proc.returncode == 1 and "dataset" in proc.stderr
    assert not (tmp_path / "report.json").exists() and not (tmp_path / "report.md").exists()
