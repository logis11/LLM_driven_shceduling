"""The scoring spec (Phase 6 spec, decisions 5–15): one YAML file of per-file
terms in the harness tree, a JSON schema, and a lint that checks every term
against the compiled coreset and the dataset's variant recipes."""

import copy
import json
import subprocess
import sys

import pytest
import yaml

from conftest import REPO, TOOLS
from harness.scoring import LEGAL, SCHEMA_PATH, SPEC_PATH, lint_spec, load_spec

BUILD = REPO / "dataset" / "build" / "coreset-single"
RECIPES = REPO / "dataset" / "timelines" / "coreset"

C2_WINDOWS = {"c2-p1a": (60000000, 180000000), "c2-p1b": (60000000, 180000000),
              "c2-p2a": (60000000, 120000000), "c2-p2b": (60000000, 120000000),
              "c2-p3a": (60000000, 120000000), "c2-p3b": (60000000, 120000000)}


@pytest.fixture(scope="module")
def spec():
    return load_spec(SPEC_PATH)


def terms(spec, wid):
    return spec["files"][wid]["terms"]


def one(spec, wid, entity, metric):
    found = [t for t in terms(spec, wid) if t["entity"] == entity and t["metric"] == metric]
    assert len(found) == 1, (wid, entity, metric, found)
    return found[0]


# ------------------------------------------------------------------ the file

def test_committed_spec_lints_clean():
    assert lint_spec(SPEC_PATH, SCHEMA_PATH, BUILD, RECIPES) == []


def test_every_coreset_file_but_idle_has_terms(spec):
    compiled = {p.name.replace(".workload.json", "") for p in BUILD.glob("*.workload.json")}
    assert compiled - set(spec["files"]) == {"c1-idle"}
    assert set(spec["files"]) <= compiled
    assert all(f["terms"] for f in spec["files"].values())


def test_scored_aggregates_are_the_locked_ones(spec):
    for wid, f in spec["files"].items():
        for t in f["terms"]:
            assert (t["metric"], t["aggregate"]) in LEGAL, (wid, t)
            assert t["direction"] == LEGAL[(t["metric"], t["aggregate"])], (wid, t)
            assert t["weight"] > 0


def test_c2_weights_and_windows(spec):
    for wid, (start, end) in C2_WINDOWS.items():
        for t in terms(spec, wid):
            if t["metric"] in ("ready_wait", "job"):
                assert t["window"] == {"start_us": start, "end_us": end}, (wid, t)
                assert t["weight"] == 1.0
            else:
                assert "window" not in t, (wid, t)
    assert one(spec, "c2-p1a", "editor", "ready_wait")["cause"] == "wake"
    assert one(spec, "c2-p1a", "hog", "cpu_delivered")["weight"] == 0.5
    assert [t["entity"] for t in terms(spec, "c2-p1b")] == ["editor"]
    assert one(spec, "c2-p2a", "game.chain.1", "job")["aggregate"] == "miss_rate"
    assert one(spec, "c2-p2a", "download", "cpu_delivered")["weight"] == 0.5
    assert [t["entity"] for t in terms(spec, "c2-p2b")] == ["game.chain.1"]
    assert one(spec, "c2-p3a", "bulk", "cpu_delivered")["weight"] == 0.5
    assert one(spec, "c2-p3b", "bulk", "cpu_delivered")["weight"] == 0.25


def test_c1_terms(spec):
    assert [(t["entity"], t["metric"], t["weight"]) for t in terms(spec, "c1-office")] == [("writer", "ready_wait", 1.0)]
    assert [(t["entity"], t["metric"], t["weight"]) for t in terms(spec, "c1-browsing")] == [("browser", "ready_wait", 1.0)]
    assert one(spec, "c1-compile", "editor", "ready_wait")["weight"] == 1.0
    assert one(spec, "c1-compile", "build", "turnaround")["weight"] == 1.0
    assert one(spec, "c1-media", "music", "job")["weight"] == 1.0
    assert one(spec, "c1-media", "video", "job")["weight"] == 0.5
    assert one(spec, "c1-gaming", "game.chain.1", "job")["weight"] == 1.0
    assert one(spec, "c1-gaming", "compositor", "job")["weight"] == 0.5
    for wid in ("c1-office", "c1-browsing", "c1-compile", "c1-media", "c1-gaming"):
        assert all("window" not in t for t in terms(spec, wid))


def test_c3_terms(spec):
    assert {(t["entity"], t["metric"], t["weight"]) for t in terms(spec, "c3-workday")} == {
        ("browser", "ready_wait", 1.0), ("writer", "ready_wait", 1.0), ("mailer", "ready_wait", 1.0),
        ("build", "cpu_delivered", 0.5)}
    assert {(t["entity"], t["metric"], t["weight"]) for t in terms(spec, "c3-evening")} == {
        ("browser", "ready_wait", 1.0), ("game.chain.1", "job", 1.0),
        ("music", "job", 1.0), ("video", "job", 0.5)}
    assert {(t["entity"], t["metric"], t["weight"]) for t in terms(spec, "c3-creation")} == {
        ("photo-editor", "ready_wait", 1.0), ("video-editor", "ready_wait", 1.0),
        ("batch", "cpu_delivered", 0.5)}


def test_derived_files_carry_their_base_terms_verbatim(spec):
    bases = {wid: f["base"] for wid, f in spec["files"].items() if "base" in f}
    assert bases == {"c4-office": "c1-office", "c4-compile": "c1-compile", "c4-gaming": "c1-gaming",
                     "c5-t3": "c1-media", "c5-t4": "c1-media", "c5-t5": "c1-media",
                     "c6-spoof": "c1-browsing", "c6-fold": "c1-browsing"}
    for wid, base in bases.items():
        assert terms(spec, wid) == terms(spec, base), wid


def test_c6_dual_scores_its_two_foregrounds(spec):
    assert {(t["entity"], t["metric"], t["weight"]) for t in terms(spec, "c6-dual")} == {
        ("game.chain.1", "job", 1.0), ("editor", "ready_wait", 1.0)}


# ------------------------------------------------------------------ the lint

def write(tmp_path, doc):
    p = tmp_path / "spec.yaml"
    p.write_text(yaml.safe_dump(doc, sort_keys=False))
    return p


def minimal(**files):
    return {"files": files}


def term(entity="editor", metric="ready_wait", aggregate="p99", direction="lower",
         weight=1.0, **extra):
    t = {"entity": entity, "metric": metric, "aggregate": aggregate,
         "direction": direction, "weight": weight}
    if metric == "ready_wait" and "cause" not in extra:
        t["cause"] = "wake"
    t.update(extra)
    return t


def errors_of(tmp_path, doc):
    return lint_spec(write(tmp_path, doc), SCHEMA_PATH, BUILD, RECIPES)


def test_unknown_entity_is_an_error(tmp_path):
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [term(entity="trainer")]}}))
    assert any("c2-p1a" in e and "trainer" in e for e in errs)


def test_reserved_entity_is_accepted_by_the_entity_check(tmp_path):
    # `lane` exists as an entity; the pair check then rejects busy-less metrics — only
    # the entity rule is under test here, so use a legal pair and expect no entity error
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [term(entity="lane")]}}))
    assert not any("no task" in e for e in errs)


def test_unknown_workload_is_an_error(tmp_path):
    errs = errors_of(tmp_path, minimal(**{"c9-nope": {"terms": [term()]}}))
    assert any("c9-nope" in e and "compiled" in e for e in errs)


def test_illegal_metric_aggregate_pair_is_an_error(tmp_path):
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [term(metric="job", aggregate="p99", cause=None)]}}))
    errs = [e for e in errs if "p99" in e or "job" in e]
    assert errs


def test_direction_must_match_the_aggregate(tmp_path):
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [term(direction="higher")]}}))
    assert any("direction" in e and "lower" in e for e in errs)


def test_weight_must_be_positive(tmp_path):
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [term(weight=0)]}}))
    assert any("weight" in e for e in errs)


def test_window_must_lie_inside_the_file(tmp_path):
    bad = term(window={"start_us": 60000000, "end_us": 190000000})     # T_end is 180 s
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [bad]}}))
    assert any("window" in e and "180000000" in e for e in errs)
    bad = term(window={"start_us": 70000000, "end_us": 60000000})
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [bad]}}))
    assert any("window" in e for e in errs)


def test_ready_wait_needs_a_cause_and_others_must_not_carry_one(tmp_path):
    t = term(); del t["cause"]
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [t]}}))
    assert any("cause" in e for e in errs)
    t = term(entity="hog", metric="cpu_delivered", aggregate="progress", direction="higher", cause="wake")
    errs = errors_of(tmp_path, minimal(**{"c2-p1a": {"terms": [t]}}))
    assert any("cause" in e for e in errs)


def test_declared_base_must_match_the_variant_recipe_and_terms_must_equal(tmp_path):
    base_terms = [term(entity="writer")]
    doc = minimal(**{"c1-office": {"terms": base_terms},
                     "c4-office": {"base": "c1-media", "terms": copy.deepcopy(base_terms)}})
    errs = errors_of(tmp_path, doc)
    assert any("c4-office" in e and "recipe" in e and "c1-office" in e for e in errs)
    doc = minimal(**{"c1-office": {"terms": base_terms},
                     "c4-office": {"base": "c1-office", "terms": [term(entity="writer", weight=0.5)]}})
    errs = errors_of(tmp_path, doc)
    assert any("c4-office" in e and "verbatim" in e for e in errs)
    doc = minimal(**{"c1-office": {"terms": base_terms, "base": "c1-media"}})
    errs = errors_of(tmp_path, doc)
    assert any("c1-office" in e and "not a variant" in e for e in errs)


def test_variant_without_a_base_must_differ_from_its_base(tmp_path):
    base_terms = [term(entity="writer")]
    # copied the base entry and forgot the base line → error
    doc = minimal(**{"c1-office": {"terms": base_terms},
                     "c4-office": {"terms": copy.deepcopy(base_terms)}})
    errs = errors_of(tmp_path, doc)
    assert any("c4-office" in e and "variant of 'c1-office'" in e and "base" in e for e in errs)
    # a C2 b-file differs from its a-file by decision → no such error
    a = [term(), term(entity="hog", metric="cpu_delivered", aggregate="progress",
                      direction="higher", weight=0.5)]
    doc = minimal(**{"c2-p1a": {"terms": a}, "c2-p1b": {"terms": [term()]}})
    errs = errors_of(tmp_path, doc)
    assert not any("c2-p1b" in e for e in errs)


def test_schema_rejects_unknown_fields(tmp_path):
    doc = minimal(**{"c2-p1a": {"terms": [term(note="why")]}})
    errs = errors_of(tmp_path, doc)
    assert any("note" in e for e in errs)


def test_cli_exit_codes(tmp_path):
    p = subprocess.run([sys.executable, str(TOOLS / "scoring_lint.py")], capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "scoring spec" in p.stdout and "lint clean" in p.stdout
    bad = write(tmp_path, minimal(**{"c2-p1a": {"terms": [term(entity="trainer")]}}))
    p = subprocess.run([sys.executable, str(TOOLS / "scoring_lint.py"), "--spec", str(bad)],
                       capture_output=True, text=True)
    assert p.returncode == 1
