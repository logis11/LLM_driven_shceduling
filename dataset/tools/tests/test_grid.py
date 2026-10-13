"""Coverage grid (Phase 7 spec, decisions 1 and 11): one row per driver-table
cell — mode × background_wanted — with the five familiarity-tier columns;
`ambiguous` reported outside the 32; pre-committed-miss segments counted in
their cell and marked; an empty cell is a coverage error. The generated
layer's tables (9.21 decision 4) beside it, one per set, from the committed
manifests' segment labels."""

import json

import pytest
import yaml

from gen import coverage
from wlc import grid

MODES = ["browsing", "office", "mail", "dev", "photo", "meeting", "gaming",
         "media", "video-edit", "compile", "ml-train", "render", "transcode",
         "indexing", "backup", "idle"]

# Recounted 2026-09-09 from the compiled coreset ground truth (Phase 7 spec,
# decision 1): 17 cells exercised before Phase 7. 7.2 added indexing/true,
# 7.3 the fifteen remaining false cells: all 32 instanced. Five segments are
# pre-committed misses (decision 3): indexing/true and the ml-train, render,
# transcode, backup false cells; media/true since c6-alias (9.20 decision 8), the
# name-collision alias beside the authored ladder files.
MISS_CELLS = {("indexing", True), ("ml-train", False), ("render", False),
              ("transcode", False), ("backup", False), ("media", True)}


@pytest.fixture(scope="module")
def coverage(repo_root):
    return grid.build_grid(repo_root / "dataset" / "timelines")


def cell_keys(coverage):
    return [(c["mode"], c["background_wanted"]) for c in coverage["cells"]]


def test_32_cells_in_menu_order(coverage):
    assert cell_keys(coverage) == [(m, w) for m in MODES for w in (True, False)]


def test_tier_columns_and_counts_agree(coverage):
    for cell in coverage["cells"]:
        assert list(cell["tiers"]) == ["t1", "t2", "t3", "t4", "t5"]
        assert sum(cell["tiers"].values()) == cell["segments"]
        assert 0 <= cell["pre_committed_miss"] <= cell["segments"]


def test_coreset_instances_all_32_cells(coverage):
    exercised = {(c["mode"], c["background_wanted"])
                 for c in coverage["cells"] if c["segments"]}
    assert exercised == {(m, w) for m in MODES for w in (True, False)}
    assert coverage["empty_cells"] == []
    misses = {(c["mode"], c["background_wanted"])
              for c in coverage["cells"] if c["pre_committed_miss"]}
    assert misses == MISS_CELLS
    for cell in coverage["cells"]:
        assert cell["pre_committed_miss"] <= 1
    assert coverage["per_file"]["c1-indexing"][0]["pre_committed_miss"] is True
    assert coverage["per_file"]["c7-backup"][0]["pre_committed_miss"] is True
    assert "pre_committed_miss" not in coverage["per_file"]["c7-compile"][0]


def test_every_c7_counterpart_is_the_false_cell_of_its_base(coverage):
    for mode in MODES:
        base, counterpart = (coverage["per_file"][f"c1-{mode}"],
                             coverage["per_file"][f"c7-{mode}"])
        assert len(base) == len(counterpart) == 1
        assert base[0]["mode"] == counterpart[0]["mode"] == mode
        assert base[0]["background_wanted"] is True
        assert counterpart[0]["background_wanted"] is False
        assert base[0]["tier"] == counterpart[0]["tier"], mode


def test_ambiguous_is_outside_the_grid(coverage):
    outside = coverage["outside"]
    assert [o["mode"] for o in outside] == ["ambiguous"]
    assert outside[0]["file"] == "c6-dual"
    on_grid = sum(c["segments"] for c in coverage["cells"])
    assert on_grid + len(outside) == coverage["segments_total"]


def test_per_file_rows_carry_the_attribute(coverage):
    rows = coverage["per_file"]["c2-p1b"]
    assert [(r["mode"], r["background_wanted"]) for r in rows] == [
        ("dev", True), ("indexing", False)]
    assert all("pre_committed_miss" not in r for r in rows)


def generated_manifests(repo_root):
    sets = yaml.safe_load((repo_root / "dataset" / "grids.yaml").read_text())["sets"]
    return [repo_root / "dataset" / f"build.{name}.manifest.json" for name in sets]


def test_committed_grid_matches_the_timelines_and_the_generated_manifests(repo_root):
    assert coverage.write(repo_root / "dataset" / "timelines", generated_manifests(repo_root),
                          repo_root / "dataset" / "coverage-grid.json", check=True) == []


# --- 9.21: the generated layer's tables ---------------------------------

@pytest.fixture(scope="module")
def generated(repo_root):
    return coverage.build_generated_grid(generated_manifests(repo_root))


def test_generated_tables_one_per_set_over_the_true_cells_alone(generated):
    """Every C1 file is the `true` side of its mode, so every generated segment lands in a `true` cell; the file
    and segment counts are the sets' (480 × 2, 720 × 3, 24 × 9, 272 × 2, 66 × 1)."""
    assert {s: (t["files"], t["segments_total"]) for s, t in generated.items()} == {
        "transition-grid": (480, 960), "return-grid": (720, 2160), "flap-stress": (24, 216),
        "distractor-grid": (272, 544), "familiarity-ladder": (66, 66)}
    for table in generated.values():
        assert [(c["mode"], c["background_wanted"]) for c in table["cells"]] == [(m, w) for m in MODES for w in (True, False)]
        for cell in table["cells"]:
            assert sum(cell["tiers"].values()) == cell["segments"]
            if not cell["background_wanted"]:
                assert cell["segments"] == 0


def test_the_ladder_fills_tiers_4_and_5_for_every_mode_and_tier_3_where_the_definition_names_one(generated):
    by_mode = {c["mode"]: c for c in generated["familiarity-ladder"]["cells"] if c["background_wanted"]}
    for mode in MODES:
        assert by_mode[mode]["tiers"]["t4"] >= 1 and by_mode[mode]["tiers"]["t5"] >= 1, mode
        assert by_mode[mode]["tiers"]["t4"] == by_mode[mode]["tiers"]["t5"]
        assert by_mode[mode]["tiers"]["t1"] == by_mode[mode]["tiers"]["t2"] == 0
    assert {m for m, c in by_mode.items() if c["tiers"]["t3"]} == {"render", "backup"}
    assert sum(c["tiers"]["t4"] for c in by_mode.values()) == sum(c["tiers"]["t5"] for c in by_mode.values()) == 32


def test_every_transition_cell_holds_sixty_segments_and_indexing_true_is_always_a_miss(generated):
    for table_name, per_mode in (("transition-grid", 60), ("return-grid", 135), ("distractor-grid", 34)):
        for cell in generated[table_name]["cells"]:
            if cell["background_wanted"]:
                assert cell["segments"] == per_mode, (table_name, cell["mode"])
                if cell["mode"] == "indexing":
                    assert cell["pre_committed_miss"] == per_mode   # inherited from c1-indexing's annotation
    # 9.20 decision 3: the 26 cells whose focus holders share a name mark their second segment; beside indexing's
    dx = {c["mode"]: c["pre_committed_miss"] for c in generated["distractor-grid"]["cells"] if c["background_wanted"]}
    assert dx["browsing"] == 1 and dx["meeting"] == 1          # chrome: browsing <-> meeting
    assert dx["dev"] == dx["compile"] == dx["ml-train"] == 3   # code: dev / compile / ml-train / indexing
    assert dx["video-edit"] == dx["render"] == dx["transcode"] == dx["backup"] == 3   # kdenlive
    assert dx["office"] == 0


def test_a_manifest_without_segment_labels_is_refused(tmp_path):
    path = tmp_path / "build.toy.manifest.json"
    path.write_text(json.dumps({"grid": {"toy-single/x.workload.json": {"a": "office"}}}))
    with pytest.raises(grid.GridError, match="predates"):
        coverage.build_generated_grid([path])
    with pytest.raises(grid.GridError, match="no manifest"):
        coverage.build_generated_grid([tmp_path / "build.none.manifest.json"])
    text = coverage.render_generated({"toy": {"files": 1, "segments_total": 1, "cells": [
        {"mode": "office", "background_wanted": True, "tiers": {t: 0 for t in grid.TIERS}, "segments": 0, grid.MISS_KEY: 0}]}})
    assert "generated toy: 1 files, 1 segments" in text


def test_coverage_errors_are_empty_on_the_coreset(coverage):
    assert grid.coverage_errors(coverage) == []


def test_coverage_errors_name_every_empty_cell():
    coverage = {"empty_cells": ["browsing/false", "idle/false"]}
    errors = grid.coverage_errors(coverage)
    assert len(errors) == 1
    assert "2 empty" in errors[0] and "browsing/false" in errors[0]


def test_render_lists_cells_outside_and_empties(coverage):
    text = grid.render(coverage)
    assert "browsing/true" in text and "browsing/false" in text
    assert "outside the grid: ambiguous" in text
    assert "empty cells: 0" in text


# --- synthetic timelines -----------------------------------------------

def _timeline(tmp_path, wid, segments, tasks):
    (tmp_path / f"{wid}.timeline.yaml").write_text(yaml.safe_dump(
        {"meta": {"id": wid, "seed": 1}, "segments": segments,
         "tasks": tasks, "focus": []}))


def test_pre_committed_miss_is_counted_and_marked(tmp_path):
    _timeline(tmp_path, "x-miss", [
        {"from": "0s", "to": "60s", "mode": "indexing",
         "attributes": {"background_wanted": True, "initiated": "user",
                        "pre_committed_miss": True}}],
        [{"id": "hog", "name": "tracker-miner-f", "archetype": "cpu-batch",
          "arrive": "0s", "bind": {"total_work": "60s"}}])
    coverage = grid.build_grid(tmp_path)
    cell = next(c for c in coverage["cells"]
                if (c["mode"], c["background_wanted"]) == ("indexing", True))
    assert cell["segments"] == 1 and cell["pre_committed_miss"] == 1
    assert cell["tiers"]["t3"] == 1
    assert coverage["per_file"]["x-miss"][0]["pre_committed_miss"] is True
    assert "indexing/true" not in coverage["empty_cells"]


def test_constructor_emitted_names_count_toward_the_tier(tmp_path):
    # game.exe is tier 1; the chain constructor emits a wineserver member
    # (tier 2) beside it, so the segment's default tier is 2
    _timeline(tmp_path, "x-game", [
        {"from": "0s", "to": "60s", "mode": "gaming",
         "attributes": {"background_wanted": True}}],
        [{"id": "game", "name": "game.exe", "archetype": "game-task-chain",
          "arrive": "0s", "depart": "60s", "bind": {"lane_share": 0.9}}])
    coverage = grid.build_grid(tmp_path)
    assert coverage["per_file"]["x-game"][0]["tier"] == 2


def test_full_coverage_has_no_errors(tmp_path):
    segments = [{"from": "0s", "to": "10s", "mode": m,
                 "attributes": {"background_wanted": w}}
                for m in MODES for w in (True, False)]
    _timeline(tmp_path, "x-full", segments,
              [{"id": "a", "name": "chrome", "archetype": "web-browser",
                "arrive": "0s", "depart": "10s"}])
    coverage = grid.build_grid(tmp_path)
    assert coverage["empty_cells"] == []
    assert grid.coverage_errors(coverage) == []
    assert "empty cells: 0" in grid.render(coverage)


def test_menu_mode_without_the_attribute_is_an_error(tmp_path):
    _timeline(tmp_path, "x-bad", [
        {"from": "0s", "to": "10s", "mode": "office", "attributes": {}}],
        [{"id": "a", "name": "chrome", "archetype": "web-browser",
          "arrive": "0s", "depart": "10s"}])
    with pytest.raises(grid.GridError, match="x-bad.*background_wanted"):
        grid.build_grid(tmp_path)
    errors = grid.write(tmp_path, tmp_path / "grid.json", check=True)
    assert len(errors) == 1 and "background_wanted" in errors[0]


def test_unknown_mode_is_an_error(tmp_path):
    _timeline(tmp_path, "x-mode", [
        {"from": "0s", "to": "10s", "mode": "cooking",
         "attributes": {"background_wanted": True}}],
        [{"id": "a", "name": "chrome", "archetype": "web-browser",
          "arrive": "0s", "depart": "10s"}])
    with pytest.raises(grid.GridError, match="cooking"):
        grid.build_grid(tmp_path)


def test_committed_json_is_sorted_and_stable(repo_root):
    path = repo_root / "dataset" / "coverage-grid.json"
    data = json.loads(path.read_text())
    assert list(data) == sorted(data)
    assert {"cells", "empty_cells", "outside", "per_file",
            "segments_total"} <= set(data)
