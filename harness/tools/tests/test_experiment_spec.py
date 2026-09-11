"""The per-experiment spec (8.7 spec, decisions 2–8): the schema, the lint
against the compiled files, the scoring terms, the registries, and the pins,
on the `mock-experiment` fixture and broken copies of it."""

import copy
import json
import subprocess
import sys

import jsonschema
import pytest
import yaml

from conftest import FIXTURES, REPO, TOOLS
from harness.evaluator import SPEC_SCHEMA, lint_spec, load_spec

FX = FIXTURES / "mock-experiment"
BUILD = FX / "workloads"
VARIANTS = ("experiment.yaml", "experiment-fail.yaml", "experiment-invalid.yaml")


def _schema():
    return json.loads(SPEC_SCHEMA.read_text())


def _broken(tmp_path, mutate):
    spec = load_spec(FX / "experiment.yaml")
    mutate(spec)
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(spec, sort_keys=False))
    return p


def _errors(path):
    return lint_spec(path, SPEC_SCHEMA, BUILD, REPO)


@pytest.mark.parametrize("name", VARIANTS)
def test_fixture_variants_validate_and_lint_clean(name):
    spec = load_spec(FX / name)
    jsonschema.Draft202012Validator(_schema()).validate(spec)
    assert _errors(FX / name) == []


def test_schema_refuses_an_unknown_top_level_key_and_a_missing_criterion():
    v = jsonschema.Draft202012Validator(_schema())
    spec = load_spec(FX / "experiment.yaml")
    assert next(v.iter_errors({**spec, "extra": 1}), None) is not None
    assert next(v.iter_errors({k: s for k, s in spec.items() if k != "criterion"}), None) is not None


def test_lint_refuses_an_unknown_criterion_type(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s["criterion"].update(type="majority_vote")))
    assert any("majority_vote" in e for e in errs)


def test_lint_refuses_an_unknown_reporting_line_type(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s["reporting_lines"].append({"type": "haiku"})))
    assert any("haiku" in e for e in errs)


def test_lint_refuses_an_exemption_naming_no_guard_or_no_reason(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s["guard_exemptions"][0].update(guard="vibes")))
    assert any("vibes" in e for e in errs)
    errs = _errors(_broken(tmp_path, lambda s: s["guard_exemptions"][0].update(reason="")))
    assert any("reason" in e for e in errs)


def test_lint_refuses_an_unknown_condition(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s["conditions"].append("psychic")))
    assert any("psychic" in e for e in errs)


def test_lint_refuses_a_file_missing_from_the_build_or_without_terms(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s["files"]["judging"].append("ghost")))
    assert any("ghost" in e for e in errs)
    # mock-p1a has scoring terms in the pinned spec but no compiled file in this build
    errs = _errors(_broken(tmp_path, lambda s: s["files"]["reporting"].append("mock-p1a")))
    assert any("mock-p1a" in e for e in errs)


def test_lint_checks_the_derived_layer1_exclusions(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s.update(layer1_exclusions=[])))
    assert any("layer1_exclusions" in e and "mock-score" in e for e in errs)


def test_lint_refuses_a_pin_that_does_not_match(tmp_path):
    errs = _errors(_broken(tmp_path, lambda s: s["pins"]["scoring_spec"].update(sha256="0" * 64)))
    assert any("scoring_spec" in e and "sha256" in e for e in errs)


def test_lint_refuses_a_sensitivity_line_naming_an_unknown_boot_default(tmp_path):
    def mutate(s):
        s["reporting_lines"][0]["boot_defaults"] = ["nope"]
    errs = _errors(_broken(tmp_path, mutate))
    assert any("nope" in e for e in errs)


def test_lint_cli(tmp_path):
    ok = subprocess.run([sys.executable, str(TOOLS / "experiment_lint.py"), "--spec", str(FX / "experiment.yaml"),
                         "--build", str(BUILD)], capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    bad = _broken(tmp_path, lambda s: s["criterion"].update(type="majority_vote"))
    proc = subprocess.run([sys.executable, str(TOOLS / "experiment_lint.py"), "--spec", str(bad),
                           "--build", str(BUILD)], capture_output=True, text=True)
    assert proc.returncode == 1 and "majority_vote" in proc.stdout
