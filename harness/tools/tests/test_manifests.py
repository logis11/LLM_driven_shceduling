"""The generated layer's manifests as the harness reads them (9.21 spec, decisions 5 and 6): the records and their
keys, the selection by axes, the spec's expansion, the compiled-path resolution — on the toy manifest beside the
mock-experiment fixture and on the committed manifests when they are present."""

import copy
import json

import pytest
import yaml

from conftest import FIXTURES, REPO
from harness import manifests

FX = FIXTURES / "mock-experiment"
TOY = FX / "build.toy-grid.manifest.json"


def _spec(**files_extra):
    spec = yaml.safe_load((FX / "experiment.yaml").read_text())
    spec["files"].update(files_extra)
    spec["pins"]["generated"] = {"toy-grid": {"path": TOY.relative_to(REPO).as_posix(), "sha256": "0" * 64}}
    return spec


def test_records_are_keyed_by_workload_id_and_carry_the_artifact():
    m = manifests.load(TOY)
    recs = manifests.records(m)
    assert sorted(recs) == ["tg-a", "tg-b"]
    assert recs["tg-a"]["split"] == "measurement" and recs["tg-a"]["_artifact"] == "toy-grid-single/tg-a.workload.json"
    assert manifests.keys(m) == {"a", "b", "form", "split", "placements", "segments"}
    assert manifests.workload_id("return-grid-single/rt-office-to-dev-2s.workload.json") == "rt-office-to-dev-2s"


def test_select_matches_every_named_key_and_refuses_a_key_the_records_lack():
    m = manifests.load(TOY)
    assert manifests.select(m, {"split": "measurement"}) == ["tg-a"]
    assert manifests.select(m, {"a": "dev", "form": "departs"}) == ["tg-a", "tg-b"]
    assert manifests.select(m, {"split": "none"}) == []
    with pytest.raises(KeyError, match="middle"):
        manifests.select(m, {"middle": "2s"})


def test_artifact_paths_resolve_under_build_beside_the_manifest():
    paths = manifests.artifact_paths(TOY, manifests.load(TOY))
    assert paths["tg-b"] == (FX / "build" / "toy-grid-single" / "tg-b.workload.json").resolve()
    assert paths["tg-b"].is_file()
    assert manifests.workload_path("mock-score", paths, FX / "workloads") == FX / "workloads" / "mock-score.workload.json"
    assert manifests.workload_path("tg-b", paths, FX / "workloads") == paths["tg-b"]


def test_expand_adds_the_selected_files_to_reporting_and_hands_back_their_paths_and_axes():
    spec = _spec(select=[{"manifest": "toy-grid", "where": {"split": "measurement"}}])
    out, paths, axes = manifests.expand(spec, REPO)
    assert out["files"]["reporting"] == ["tg-a"] and "select" not in out["files"]
    assert out["files"]["judging"] == ["mock-score"]
    assert set(paths) == {"tg-a"} and paths["tg-a"].is_file()
    assert axes["tg-a"][0] == "toy-grid" and axes["tg-a"][1]["split"] == "measurement"
    assert "_artifact" not in axes["tg-a"][1]
    assert spec["files"].get("select")                            # the input is untouched
    none, paths, axes = manifests.expand(yaml.safe_load((FX / "experiment.yaml").read_text()), REPO)
    assert none["files"]["reporting"] == [] and paths == {} and axes == {}


def test_expand_refuses_an_unpinned_manifest_an_unknown_key_an_empty_selection_and_a_judging_file():
    with pytest.raises(ValueError, match="not pinned"):
        manifests.expand(_spec(select=[{"manifest": "other-grid", "where": {"split": "measurement"}}]), REPO)
    with pytest.raises(ValueError, match="no key"):
        manifests.expand(_spec(select=[{"manifest": "toy-grid", "where": {"tier": 5}}]), REPO)
    with pytest.raises(ValueError, match="no file of"):
        manifests.expand(_spec(select=[{"manifest": "toy-grid", "where": {"split": "neither"}}]), REPO)
    spec = _spec(select=[{"manifest": "toy-grid", "where": {"split": "tuning"}}])
    spec["files"]["judging"].append("tg-b")
    with pytest.raises(ValueError, match="already listed"):
        manifests.expand(spec, REPO)
    spec = _spec(select=[{"manifest": "toy-grid", "where": {"split": "tuning"}}])
    spec["pins"]["generated"]["toy-grid"]["path"] = "harness/tools/tests/fixtures/no-such.manifest.json"
    with pytest.raises(ValueError, match="not a file"):
        manifests.expand(spec, REPO)


def test_the_committed_manifests_carry_the_record_and_split_as_the_specs_will_read_them(repo_root):
    """The five sets' records (9.19 decision 6; 9.20; 9.21 decisions 1 and 4): the return grid and the flap-stress
    set select by `split`, the transition grid by `form`, the distractor grid by `relation`, the ladder by `tier` and
    `carrier`; every record carries placements and segment labels."""
    sets = yaml.safe_load((repo_root / "dataset" / "grids.yaml").read_text())["sets"]
    for name in sets:
        path = repo_root / "dataset" / f"build.{name}.manifest.json"
        if not path.is_file():
            pytest.skip(f"{path.name} not built")
        m = manifests.load(path)
        ks = manifests.keys(m)
        assert {"placements", "segments"} <= ks, name
        if name in ("return-grid", "flap-stress"):
            tuning, measurement = manifests.select(m, {"split": "tuning"}), manifests.select(m, {"split": "measurement"})
            assert len(tuning) == len(measurement) == len(manifests.records(m)) // 2, name
        elif name == "transition-grid":
            assert len(manifests.select(m, {"form": "focus"})) == 240
        elif name == "distractor-grid":
            assert len(manifests.select(m, {"relation": "out-of-vocabulary"})) == 32
            assert len(manifests.select(m, {"focus_name_shared": True})) == 26
        else:
            assert len(manifests.select(m, {"tier": 5, "carrier": "all"})) == 16
            assert manifests.select(m, {"tier": 3}) == ["fl-backup-t3", "fl-render-t3"]
