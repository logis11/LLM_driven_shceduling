"""Coverage grid (Phase 7 spec, decisions 1 and 11): one row per driver-table
cell — mode × background_wanted — with the five familiarity-tier columns;
`ambiguous` reported outside the 32; pre-committed-miss segments counted in
their cell and marked; an empty cell is a coverage error."""

import json

import pytest
import yaml

from wlc import grid

MODES = ["browsing", "office", "mail", "dev", "photo", "meeting", "gaming",
         "media", "video-edit", "compile", "ml-train", "render", "transcode",
         "indexing", "backup", "idle"]

# Recounted 2026-09-09 from the compiled coreset ground truth (Phase 7 spec,
# decision 1): 17 cells exercised before Phase 7; 7.2 added indexing/true
# (c1-indexing, a pre-committed miss). 7.3 fills the remaining 14.
EXERCISED_AFTER_7_2 = {
    ("browsing", True), ("office", True), ("mail", True), ("dev", True),
    ("photo", True), ("meeting", True), ("gaming", True), ("gaming", False),
    ("media", True), ("video-edit", True), ("compile", True),
    ("ml-train", True), ("render", True), ("transcode", True),
    ("indexing", True), ("indexing", False), ("backup", True), ("idle", True),
}


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


def test_current_coreset_exercises_the_recorded_18(coverage):
    exercised = {(c["mode"], c["background_wanted"])
                 for c in coverage["cells"] if c["segments"]}
    assert exercised == EXERCISED_AFTER_7_2
    empty = {(m, w) for m in MODES for w in (True, False)} - exercised
    assert coverage["empty_cells"] == sorted(
        f"{m}/{str(w).lower()}" for m, w in empty)
    assert len(coverage["empty_cells"]) == 14
    indexing_true = next(c for c in coverage["cells"]
                         if (c["mode"], c["background_wanted"]) == ("indexing", True))
    assert indexing_true["segments"] == 1 and indexing_true["pre_committed_miss"] == 1
    assert coverage["per_file"]["c1-indexing"][0]["pre_committed_miss"] is True


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


def test_committed_grid_matches_the_timelines(repo_root):
    assert grid.write(repo_root / "dataset" / "timelines",
                      repo_root / "dataset" / "coverage-grid.json",
                      check=True) == []


def test_coverage_errors_name_every_empty_cell(coverage):
    errors = grid.coverage_errors(coverage)
    assert len(errors) == 1
    assert "14 empty" in errors[0]
    assert "browsing/false" in errors[0]


def test_render_lists_cells_outside_and_empties(coverage):
    text = grid.render(coverage)
    assert "browsing/true" in text and "browsing/false" in text
    assert "outside the grid: ambiguous" in text
    assert "empty cells: 14" in text


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
        [{"id": "hog", "name": "tracker-miner-fs-3", "archetype": "cpu-batch",
          "arrive": "0s", "bind": {"total_work": "60s"}}])
    coverage = grid.build_grid(tmp_path)
    cell = next(c for c in coverage["cells"]
                if (c["mode"], c["background_wanted"]) == ("indexing", True))
    assert cell["segments"] == 1 and cell["pre_committed_miss"] == 1
    assert cell["tiers"]["t3"] == 1
    assert coverage["per_file"]["x-miss"][0]["pre_committed_miss"] is True
    assert "indexing/true" not in coverage["empty_cells"]


def test_full_coverage_has_no_errors(tmp_path):
    segments = [{"from": "0s", "to": "10s", "mode": m,
                 "attributes": {"background_wanted": w}}
                for m in MODES for w in (True, False)]
    _timeline(tmp_path, "x-full", segments,
              [{"id": "a", "name": "chrome", "archetype": "desktop-interactive",
                "arrive": "0s", "depart": "10s"}])
    coverage = grid.build_grid(tmp_path)
    assert coverage["empty_cells"] == []
    assert grid.coverage_errors(coverage) == []
    assert "empty cells: 0" in grid.render(coverage)


def test_menu_mode_without_the_attribute_is_an_error(tmp_path):
    _timeline(tmp_path, "x-bad", [
        {"from": "0s", "to": "10s", "mode": "office", "attributes": {}}],
        [{"id": "a", "name": "chrome", "archetype": "desktop-interactive",
          "arrive": "0s", "depart": "10s"}])
    with pytest.raises(grid.GridError, match="x-bad.*background_wanted"):
        grid.build_grid(tmp_path)
    errors = grid.write(tmp_path, tmp_path / "grid.json", check=True)
    assert len(errors) == 1 and "background_wanted" in errors[0]


def test_unknown_mode_is_an_error(tmp_path):
    _timeline(tmp_path, "x-mode", [
        {"from": "0s", "to": "10s", "mode": "cooking",
         "attributes": {"background_wanted": True}}],
        [{"id": "a", "name": "chrome", "archetype": "desktop-interactive",
          "arrive": "0s", "depart": "10s"}])
    with pytest.raises(grid.GridError, match="cooking"):
        grid.build_grid(tmp_path)


def test_committed_json_is_sorted_and_stable(repo_root):
    path = repo_root / "dataset" / "coverage-grid.json"
    data = json.loads(path.read_text())
    assert list(data) == sorted(data)
    assert {"cells", "empty_cells", "outside", "per_file",
            "segments_total"} <= set(data)
