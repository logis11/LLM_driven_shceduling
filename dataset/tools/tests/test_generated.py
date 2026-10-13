"""The generated layer (9.19 spec; 9.20 spec): the grid definition, the cells, the composition rules (9.19 decisions
1–3, 10), the splits and seeds (9.19 decision 6), the flap-stress set (9.19 decision 7), what each set's manifest
records (9.19 decisions 4–6); the distractor grid (9.20 decisions 1–4) and the familiarity ladder (9.20 decisions
5–7)."""

import hashlib
import importlib
import json

import pytest
import yaml

from gen import c1_sets, cells, compose, compose_full, grid_record, lint_grids, load_definition, modes_of, ordered_pairs, seed_of
from gen.cells import COMPILER_NAMES, focus_name, known_names, names_of, ranked_pairs
from wlc.grid import NAME_TIERS
from gen.compose import timeline_bytes
from wlc import Timeline
from wlc.linter import lint_bound_sources
from wlc.units import parse_us

generate = importlib.import_module("generate")

MODES = ["backup", "browsing", "compile", "dev", "gaming", "idle", "indexing", "mail", "media", "meeting",
         "ml-train", "office", "photo", "render", "transcode", "video-edit"]
S = 1_000_000


@pytest.fixture(scope="module")
def layer(repo_root):
    dataset = repo_root / "dataset"
    defn = load_definition(dataset / "grids.yaml")
    modes = modes_of(dataset / "timelines" / "coreset")
    sets = c1_sets(dataset / "timelines" / "coreset")
    by_set = cells(defn, modes, sets)
    return {"defn": defn, "modes": modes, "by_set": by_set, "sets": sets,
            "by_id": {c["id"]: c for s in by_set.values() for c in s}}


def composed(layer, cell_id):
    return compose(layer["by_id"][cell_id], layer["sets"], layer["defn"])


def task(data, task_id):
    return next(t for t in data["tasks"] if t["id"] == task_id)


def spans(items):
    return [(parse_us(x["from"]), parse_us(x["to"])) for x in items]


def test_the_definition_names_the_sixteen_modes_the_240_pairs_and_the_five_sets(layer):
    assert layer["modes"] == MODES
    assert len(ordered_pairs(layer["modes"])) == 240 == len({p for p in ordered_pairs(layer["modes"])})
    assert {k: len(v) for k, v in layer["by_set"].items()} == {"transition-grid": 480, "return-grid": 720,
                                                              "flap-stress": 24, "distractor-grid": 272,
                                                              "familiarity-ladder": 66}
    assert len(layer["by_id"]) == 1562


def test_departs_form_moves_every_task_at_the_boundary_and_scales_the_batch_job(layer):
    """Decisions 1–3 on compile -> office: A's tasks leave at 60 s, B's arrive; the build's spawn count is the C1
    value over the 58 s span, labelled design; the input windows keep the 2 s margins."""
    data = composed(layer, "tr-compile-to-office-departs")
    assert spans(data["segments"]) == [(0, 60 * S), (60 * S, 120 * S)]
    assert [s["mode"] for s in data["segments"]] == ["compile", "office"]
    assert data["segments"][1]["scenario"] == ["S1", "S2", "S4"]
    editor, build = task(data, "editor-s0"), task(data, "build-s0")
    assert (editor["arrive"], editor["depart"]) == ("0s", "60s")
    assert build["arrive"] == "2s" and "depart" not in build
    assert build["bind"] == {"spawn_count": round(2908 * 58 / 1592), "parallelism_cap": 8, "child_name": "cc1"}
    assert build["source"] == {"spawn_count": "design", "parallelism_cap": "design",
                               "child_name": "meas-ci:build:2026-09-18"}
    for tid in ("writer-s1", "browser-s1", "renderers-s1", "mail-s1"):
        assert (task(data, tid)["arrive"], task(data, tid)["depart"]) == ("60s", "120s")
    assert task(data, "renderers-s1")["count"] == 4
    assert task(data, "renderers-s1")["source"] == {"count": ["glam", "meas-ci:desktop:2026-10-04"]}
    assert [(w["task"], w["from"], w["to"]) for w in data["input"]] == [("editor-s0", "2s", "58s"),
                                                                        ("writer-s1", "62s", "118s")]
    assert [(f["task"], f["from"], f["to"]) for f in data["focus"]] == [("editor-s0", "0s", "60s"),
                                                                        ("writer-s1", "60s", "120s")]
    assert data["meta"] == {"id": "tr-compile-to-office-departs", "seed": seed_of("transition-grid",
                                                                                "tr-compile-to-office-departs"),
                            "demand": "calibration"}


def test_focus_form_keeps_a_alive_to_the_end_and_moves_the_input_with_the_focus(layer):
    """Decision 2: B arrives at 60 s and takes the focus; A's tasks stay to 120 s, A types until 58 s only, and A's
    batch job is sized to the 118 s it is alive in."""
    departs, focus = composed(layer, "tr-compile-to-office-departs"), composed(layer, "tr-compile-to-office-focus")
    assert task(focus, "editor-s0")["depart"] == "120s"
    assert task(focus, "build-s0")["bind"]["spawn_count"] == round(2908 * 118 / 1592)
    assert [(w["task"], w["from"], w["to"]) for w in focus["input"]] == [(w["task"], w["from"], w["to"])
                                                                         for w in departs["input"]]
    assert [(f["task"], f["from"], f["to"]) for f in focus["focus"]] == [(f["task"], f["from"], f["to"])
                                                                         for f in departs["focus"]]
    assert [t for t in focus["tasks"] if t["id"].endswith("-s1")] == [t for t in departs["tasks"]
                                                                       if t["id"].endswith("-s1")]
    assert [s["mode"] for s in focus["segments"]] == ["compile", "office"]


def test_layout_keeps_d44s_margins_and_operation_fractions(layer):
    """Decision 3 (9.10 D44) on mail -> idle -> mail with a 10 s middle: the send at 38/56 of each window; the idle
    middle shows its four system tasks with no input and no focus."""
    data = composed(layer, "rt-mail-to-idle-10s")
    assert spans(data["segments"]) == [(0, 60 * S), (60 * S, 70 * S), (70 * S, 130 * S)]
    assert [(w["task"], w["from"], w["to"]) for w in data["input"]] == [("mailer-s0", "2s", "58s"),
                                                                        ("mailer-s2", "72s", "128s")]
    assert [(o["task"], o["at"], o["name"]) for o in data["operations"]] == [("mailer-s0", "40s", "send"),
                                                                             ("mailer-s2", "110s", "send")]
    middle = [t for t in data["tasks"] if t["id"].endswith("-s1")]
    assert sorted(t["name"] for t in middle) == ["dbus-daemon", "gnome-shell", "pipewire", "systemd"]
    assert all((t["arrive"], t["depart"]) == ("60s", "70s") for t in middle)
    assert [f["task"] for f in data["focus"]] == ["mailer-s0", "mailer-s2"]


def test_a_two_second_segment_has_no_input_window_and_its_batch_job_arrives_at_its_start(layer):
    """Decision 3: the return grid's 2 s middle shows B with no keystroke and no operation; a finite task in such a
    segment arrives at the segment's start, its work the C1 value over the 2 s."""
    data = composed(layer, "rt-ml-train-to-browsing-2s")
    assert spans(data["segments"]) == [(0, 60 * S), (60 * S, 62 * S), (62 * S, 122 * S)]
    assert [w["task"] for w in data["input"]] == ["editor-s0", "editor-s2"]
    assert "operations" not in data                      # the page load fell with its window
    assert (task(data, "browser-s1")["arrive"], task(data, "browser-s1")["depart"]) == ("60s", "62s")
    assert [(f["task"], f["from"], f["to"]) for f in data["focus"]][1] == ("browser-s1", "60s", "62s")
    hog = task(data, "hog-s2")
    assert hog["arrive"] == "64s" and hog["bind"] == {"total_work": "50.070s", "program": "python3"}
    assert hog["source"] == {"total_work": "design", "program": ["pytorch-examples", "meas-ci:background:2026-10-03"]}
    short = composed(layer, "rt-browsing-to-ml-train-2s")
    hog = task(short, "hog-s1")
    assert hog["arrive"] == "60s" and hog["bind"]["total_work"] == f"{round(1389.885 * 2 / 1610, 3):.3f}s"


def test_an_unscaled_bound_value_keeps_its_source_tag(layer):
    """A 60 s segment from a 60 s C1 file: the index's work is the C1's and so is its tag (spec invariant)."""
    data = composed(layer, "tr-indexing-to-dev-departs")
    hog = task(data, "hog-s0")
    assert hog["bind"] == {"total_work": "39.435s"} and hog["source"] == {"total_work": "meas-ci:background:2026-10-02b"}
    game = task(composed(layer, "tr-gaming-to-dev-departs"), "game-s0")
    assert game["bind"]["lane_share"] == 0.9 and game["source"] == {"lane_share": "design",
                                                                     "member_names": "lavd-ossna24:s16"}


def test_the_return_grid_is_form_1_and_split_by_pair_into_exact_halves(layer):
    """Decisions 6 and 10: A departs and returns; 120 pairs tuning, 120 measurement, by keyed-hash rank, a pair's
    three middle lengths on one side."""
    by_pair = {}
    for cell in layer["by_set"]["return-grid"]:
        assert [m for m, *_ in cell["placements"]] == [cell["a"], cell["b"], cell["a"]]
        assert all(end == alive for _, _, end, alive in cell["placements"])
        by_pair.setdefault((cell["a"], cell["b"]), set()).add(cell["split"])
    assert len(by_pair) == 240 and all(len(s) == 1 for s in by_pair.values())
    tuning = {p for p, s in by_pair.items() if s == {"tuning"}}
    assert len(tuning) == 120
    assert tuning == set(ranked_pairs(ordered_pairs(layer["modes"]), "split", "return-grid")[:120])
    assert {c["grid"]["middle"] for c in layer["by_set"]["return-grid"]} == {"60s", "10s", "2s"}


def test_the_flap_stress_set_alternates_after_the_lead_in_in_two_seeds(layer):
    """Decision 7: three pairs by keyed hash, four intervals, a 60 s lead-in on A then eight segments B, A, B, …;
    one file per split name, the seeds distinct."""
    flap = layer["by_set"]["flap-stress"]
    pairs = {(c["a"], c["b"]) for c in flap}
    assert pairs == set(ranked_pairs(ordered_pairs(layer["modes"]), "pairs", "flap-stress")[:3])
    assert {(c["grid"]["interval"], c["grid"]["interval_source"]) for c in flap} == {
        ("2s", "design"), ("5s", "feral-gamemode"), ("10s", "tuned"), ("30s", "systemd-oomd")}
    for cell in flap:
        T = parse_us(cell["grid"]["interval"])
        modes = [m for m, *_ in cell["placements"]]
        assert modes == [cell["a"]] + [cell["b"] if i % 2 else cell["a"] for i in range(1, 9)]
        assert cell["placements"][0][1:] == (0, 60 * S, 60 * S)
        assert [(s, e) for _, s, e, _ in cell["placements"][1:]] == [(60 * S + (i - 1) * T, 60 * S + i * T)
                                                                      for i in range(1, 9)]
    for (a, b, interval), group in _group(flap).items():
        assert sorted(c["split"] for c in group) == ["measurement", "tuning"]
        assert len({c["seed"] for c in group}) == 2


def _group(flap):
    groups = {}
    for cell in flap:
        groups.setdefault((cell["a"], cell["b"], cell["grid"]["interval"]), []).append(cell)
    return groups


def test_seeds_are_keyed_draws_from_the_cell_id_and_distinct(layer):
    cell_id = "tr-browsing-to-office-departs"
    expected = int.from_bytes(hashlib.sha256(f"seed|transition-grid|{cell_id}".encode()).digest()[:4], "big")
    assert layer["by_id"][cell_id]["seed"] == seed_of("transition-grid", cell_id) == expected
    assert len({c["seed"] for c in layer["by_id"].values()}) == 1562


def test_every_cell_loads_as_a_timeline_with_sourced_bound_values(layer, library, repo_root, tmp_path):
    """The 1,562 cells written and read back through the loader's structural checks and the bound-source lint."""
    registry = yaml.safe_load((repo_root / "dataset" / "sources.yaml").read_text())["sources"]
    errors = []
    for cell in layer["by_id"].values():
        path = tmp_path / f"{cell['id']}.timeline.yaml"
        path.write_bytes(timeline_bytes(cell, layer["sets"], layer["defn"]))
        errors.extend(lint_bound_sources(path, registry))
        timeline = Timeline(path, library)
        assert timeline.id == cell["id"] and timeline.seed == cell["seed"]
        expected_segments = 2 if cell["set"] == "distractor-grid" else len(cell["placements"])
        assert len(timeline.segments) == expected_segments
    assert errors == []


def test_the_grid_definition_lint(repo_root, tmp_path):
    registry = yaml.safe_load((repo_root / "dataset" / "sources.yaml").read_text())["sources"]
    assert lint_grids(repo_root / "dataset" / "grids.yaml", registry) == []
    bad = yaml.safe_load((repo_root / "dataset" / "grids.yaml").read_text())
    bad["sets"]["flap-stress"]["intervals"][1]["source"] = "no-such-source"
    bad["sets"]["flap-stress"]["intervals"][2].pop("source")
    bad["sets"]["return-grid"]["split"]["by"] = "mood"
    path = tmp_path / "grids.yaml"
    path.write_text(yaml.safe_dump(bad))
    errors = lint_grids(path, registry)
    assert any("not in registry" in e for e in errors)
    assert any("carries no source tag or label" in e for e in errors)
    assert any("split must be by pair or by seed" in e for e in errors)
    bad = yaml.safe_load((repo_root / "dataset" / "grids.yaml").read_text())
    ladder = bad["sets"]["familiarity-ladder"]
    ladder["tier4_names"]["code"] = "a-name-longer-than-fifteen"
    ladder["tier4_names"]["make"] = "chrome"
    ladder["tier3"]["render"]["kdenlive_render"]["source"] = "no-such-source"
    bad["sets"]["distractor-grid"]["relations"].append("by-smell")
    bad["sets"]["distractor-grid"]["programs"][1]["total_work"] = "6s"
    bad["comm_limit"].pop("source")
    path.write_text(yaml.safe_dump(bad))
    errors = lint_grids(path, registry)
    assert any("exceeds the 15-character comm limit" in e for e in errors)
    assert any("is a real name" in e for e in errors)
    assert any("tier3[render]" in e and "not in registry" in e for e in errors)
    assert any("unknown relations" in e for e in errors)
    assert any("total_work must be `span`" in e for e in errors)
    assert any("comm_limit carries no source tag" in e for e in errors)


def test_the_committed_manifests_pin_the_generator_and_record_each_cells_coordinates(repo_root, layer):
    """Decisions 4–6: each set's manifest pins the definition, the generator and the sixteen C1 timelines by content
    beside the compile's inputs, and its `grid` section carries every artifact's coordinates and split."""
    dataset = repo_root / "dataset"
    generator_inputs = {p.relative_to(repo_root).as_posix() for p in generate.generator_inputs(repo_root)}
    assert {"dataset/grids.yaml", "dataset/tools/generate.py", "dataset/tools/gen/cells.py",
            "dataset/tools/gen/compose.py"} <= generator_inputs
    assert sum(1 for p in generator_inputs if "/c1-" in p) == 16
    for set_name, set_cells in layer["by_set"].items():
        path = dataset / f"build.{set_name}.manifest.json"
        if not path.is_file():
            pytest.skip(f"{path.name} not built")
        manifest = json.loads(path.read_text())
        assert set(manifest) == {"inputs", "artifacts", "demand", "reports", "grid"}
        assert set(manifest["grid"]) == set(manifest["artifacts"]) == set(manifest["demand"])
        assert generator_inputs <= set(manifest["inputs"])
        for rel, digest in manifest["inputs"].items():
            assert hashlib.sha256((repo_root / rel).read_bytes()).hexdigest() == digest, rel
        for cell in set_cells:
            rel = f"{set_name}-single/{cell['id']}.workload.json"
            coords = dict(cell["grid"])
            if "split" in cell:
                coords["split"] = cell["split"]
            coords.update(grid_record(*compose_full(cell, layer["sets"], layer["defn"])))   # 9.21 decisions 1, 4
            assert manifest["grid"][rel] == coords


# ---- 9.21: the manifest's record of each file — its placements and its segments' labels ------------------------------


def record(layer, cell_id):
    return grid_record(*compose_full(layer["by_id"][cell_id], layer["sets"], layer["defn"]))


def test_a_placement_record_names_the_mode_the_suffix_the_labelled_segments_and_the_input_window(layer):
    """9.21 decision 1: the k-th placement of a composed grid file labels the k-th segment; a placement in a
    segment of `no_input_below` or less has no input window (9.19 decision 3), so its record says `input: false`
    (decision 3 drops its keystroke terms)."""
    assert record(layer, "tr-compile-to-office-departs")["placements"] == [
        {"mode": "compile", "suffix": 0, "segments": [0], "input": True},
        {"mode": "office", "suffix": 1, "segments": [1], "input": True}]
    assert record(layer, "tr-media-to-office-focus")["placements"][0] == \
        {"mode": "media", "suffix": 0, "segments": [0], "input": False}   # the players have no keystroke stream
    middle = record(layer, "rt-office-to-dev-2s")["placements"]
    assert [p["suffix"] for p in middle] == [0, 1, 2] and [p["segments"] for p in middle] == [[0], [1], [2]]
    assert [p["input"] for p in middle] == [True, False, True]   # dev for 2 s shows no keystroke
    flap = next(c for c in layer["by_set"]["flap-stress"] if c["id"].startswith("flap-mail-to-gaming-2s"))
    placements = grid_record(*compose_full(flap, layer["sets"], layer["defn"]))["placements"]
    assert len(placements) == 9 and placements[0]["input"] is True
    assert all(p["input"] is False for p in placements[1:])   # 2 s alternations: no window for mail, none for gaming


def test_a_distractor_cell_records_a_over_both_segments_and_b_labelled_nowhere(layer):
    """9.21 decisions 1–2: A is labelled in both segments and keeps its input window to the file's end; B's task set
    arrives under suffix 1 and is labelled in no segment (so it carries no scoring term); a program arrival is one
    task, not a placement."""
    assert record(layer, "dx-office-with-compile")["placements"] == [
        {"mode": "office", "suffix": 0, "segments": [0, 1], "input": True},
        {"mode": "compile", "suffix": 1, "segments": [], "input": False}]
    assert record(layer, "dx-compile-with-7z")["placements"] == [
        {"mode": "compile", "suffix": 0, "segments": [0, 1], "input": True}]


def test_segment_labels_carry_mode_attribute_tier_and_miss(layer):
    """9.21 decision 4: the coverage table's inputs — the ladder's segment at its tier, a distractor cell's second
    segment a pre-committed miss where the focus holders share a name, indexing/true inheriting c1-indexing's miss."""
    assert record(layer, "fl-compile-t4-focus")["segments"] == [
        {"mode": "compile", "background_wanted": True, "tier": 4, "pre_committed_miss": False}]
    assert record(layer, "fl-render-t3")["segments"][0]["tier"] == 3
    shared = record(layer, "dx-dev-with-compile")["segments"]
    assert [s["pre_committed_miss"] for s in shared] == [False, True] and [s["mode"] for s in shared] == ["dev", "dev"]
    assert all(s["pre_committed_miss"] for s in record(layer, "tr-office-to-indexing-departs")["segments"][1:])
    assert record(layer, "tr-office-to-indexing-departs")["segments"][0]["pre_committed_miss"] is False
    assert record(layer, "fl-idle-t5-all")["placements"] == [{"mode": "idle", "suffix": 0, "segments": [0], "input": False}]


# ---- 9.20: the distractor grid -------------------------------------------------------------------------------------


def test_a_cross_mode_cell_is_the_focus_form_with_the_focus_kept_on_a(layer):
    """9.20 decision 1 on office <- compile: the same tasks as `tr-office-to-compile-focus` (B's set arriving at
    60 s, the build scaled to its span), but the focus and the input stay with the writer to 118/120 s and both
    segments are office, the second with compile's scenario tag added."""
    cell = composed(layer, "dx-office-with-compile")
    twin = composed(layer, "tr-office-to-compile-focus")
    assert cell["tasks"] == twin["tasks"]
    assert task(cell, "build-s1")["bind"]["spawn_count"] == 106 and task(cell, "build-s1")["source"]["spawn_count"] == "design"
    assert spans(cell["segments"]) == [(0, 60 * S), (60 * S, 120 * S)]
    assert [s["mode"] for s in cell["segments"]] == ["office", "office"]
    assert cell["segments"][0]["scenario"] == ["S1", "S2", "S4"]
    assert cell["segments"][1]["scenario"] == ["S1", "S2", "S4", "S11"]
    assert cell["segments"][1]["attributes"] == {"background_wanted": True}
    assert cell["focus"] == [{"from": "0s", "to": "120s", "task": "writer-s0"}]
    assert cell["input"] == [{"from": "2s", "to": "118s", "task": "writer-s0"}]
    assert twin["focus"] == [{"from": "0s", "to": "60s", "task": "writer-s0"}, {"from": "60s", "to": "120s", "task": "editor-s1"}]
    assert "operations" not in cell or all(op["task"].endswith("-s0") for op in cell["operations"])


def test_a_batch_mode_a_keeps_its_job_alive_to_the_end_and_its_operations_at_their_fraction(layer):
    """A = render: the editor's preview render sits at its C1 fraction (30 s of 2–58 s) of the 2–118 s window; the
    export is scaled to the 118 s span, design."""
    cell = composed(layer, "dx-render-with-mail")
    assert cell["operations"] == [{"at": "60s", "name": "preview-render", "task": "editor-s0"}]
    bulk = task(cell, "bulk-s0")
    c1 = layer["sets"]["render"]
    c1_bulk = next(t for t in c1["tasks"] if t["id"] == "bulk")
    expected_us = round(parse_us(c1_bulk["bind"]["total_work"]) * (118 * S) / (58 * S) / 1000) * 1000
    assert parse_us(bulk["bind"]["total_work"]) == expected_us and bulk["source"]["total_work"] == "design"


def test_the_out_of_vocabulary_cells_bring_one_measured_program(layer):
    """9.20 decision 2: `element-desktop` to the file's end, `7z` with its work bound to the 60 s span (design);
    the scenario tags the authored C4 files gave them; sixteen modes each."""
    oov = [c for c in layer["by_set"]["distractor-grid"] if c["grid"]["relation"] == "out-of-vocabulary"]
    assert len(oov) == 32 and {c["grid"]["b"] for c in oov} == {"element-desktop", "7z"}
    assert all(c["grid"]["focus_name_shared"] is False for c in oov)
    cell = composed(layer, "dx-dev-with-7z")
    assert task(cell, "distractor") == {"id": "distractor", "name": "7z", "archetype": "file-archiver", "arrive": "60s",
                                        "bind": {"total_work": "60s"}, "source": {"total_work": "design"}}
    assert cell["segments"][1]["scenario"] == ["S11", "S16"]
    cell = composed(layer, "dx-gaming-with-element-desktop")
    assert task(cell, "distractor") == {"id": "distractor", "name": "element-desktop", "archetype": "chat-client",
                                        "arrive": "60s", "depart": "120s"}
    assert cell["segments"][1]["scenario"] == ["S9", "S5"]
    assert cell["focus"] == [{"from": "0s", "to": "120s", "task": "game-s0"}]
    assert cell["input"] == []


def test_the_26_cells_whose_focus_holders_share_a_name_are_pre_committed_misses(layer):
    """9.20 decision 3: `code` over dev, compile, ml-train, indexing; `kdenlive` over video-edit, render, transcode,
    backup; `chrome` over browsing and meeting — 12 + 12 + 2 ordered pairs."""
    groups = [["compile", "dev", "indexing", "ml-train"], ["backup", "render", "transcode", "video-edit"],
              ["browsing", "meeting"]]
    expected = {f"dx-{a}-with-{b}" for g in groups for a in g for b in g if a != b}
    shared = {c["id"] for c in layer["by_set"]["distractor-grid"] if c["grid"]["focus_name_shared"]}
    assert shared == expected and len(shared) == 26
    for cell_id in ("dx-dev-with-compile", "dx-browsing-with-meeting"):
        data = composed(layer, cell_id)
        assert data["segments"][1]["attributes"]["pre_committed_miss"] is True
        assert "pre_committed_miss" not in data["segments"][0]["attributes"]
    assert "pre_committed_miss" not in composed(layer, "dx-dev-with-office")["segments"][1]["attributes"]
    idle = composed(layer, "dx-idle-with-office")   # no focus holder: nothing to share, the label stays idle
    assert idle["focus"] == [] and [s["mode"] for s in idle["segments"]] == ["idle", "idle"]


# ---- 9.20: the familiarity ladder ----------------------------------------------------------------------------------


def test_the_ladder_has_one_cell_per_distinct_name_set_and_two_tier_3_cells(layer):
    """9.20 decisions 5–6: tiers 4 and 5 over the sixteen modes in the carrier forms that rename something, forms
    with the same name set collapsed into `all`; tier 3 where the job ran under its own opaque name."""
    ladder = layer["by_set"]["familiarity-ladder"]
    by_tier = {}
    for c in ladder:
        by_tier.setdefault(c["grid"]["tier"], []).append(c)
    assert {t: len(v) for t, v in by_tier.items()} == {3: 2, 4: 32, 5: 32}
    grid = {c["id"]: c["grid"] for c in ladder}
    assert grid["fl-dev-t4-all"]["carriers"] == ["all", "focus"] and "fl-dev-t4-others" not in grid
    assert grid["fl-idle-t4-all"]["carriers"] == ["all", "others"] and "fl-idle-t4-focus" not in grid
    assert grid["fl-browsing-t5-all"]["carriers"] == ["all", "focus"]   # every browsing name is `chrome`
    assert {grid[f"fl-office-t4-{c}"]["carrier"] for c in ("all", "focus", "others")} == {"all", "focus", "others"}
    assert grid["fl-render-t3"] == {"mode": "render", "tier": 3, "carrier": "others", "carriers": ["others"],
                                    "renamed": {"kdenlive_render": "melt-7"},
                                    "sources": {"kdenlive_render": "meas-ci:background:2026-10-03c"}}
    assert grid["fl-backup-t3"]["renamed"] == {"deja-dup": "duplicity"}
    assert grid["fl-backup-t3"]["sources"] == {"deja-dup": "meas-ci:background:2026-10-04"}


def test_ladder_names_follow_the_table_the_keyed_draws_and_the_comm_limit(layer):
    """9.20 decision 7: tier 4 from the table, tier 5 four lowercase letters not equal to any known name, one
    substitute per real name within a file (counts preserved), every name within 15 characters, the child name and
    the member names renamed with `design` sources, `wineserver` untouched, the tier on the segment, 60 s files."""
    defn, sets = layer["defn"], layer["sets"]
    table = defn["sets"]["familiarity-ladder"]["tier4_names"]
    known = known_names(defn, sets)
    assert set(COMPILER_NAMES) <= known and set(NAME_TIERS[1]) <= known
    for cell in layer["by_set"]["familiarity-ladder"]:
        data = composed(layer, cell["id"])
        tier = cell["grid"]["tier"]
        rename = cell["rename"]
        for real, new in rename.items():
            assert len(new) <= 15
            if tier == 4:
                assert new == table[real]
            elif tier == 5:
                assert len(new) == 4 and new.islower() and new.isalpha() and new not in known
        assert len(set(rename.values())) == len(rename)
        (segment,) = data["segments"]
        assert segment["familiarity"] == tier and parse_us(segment["to"]) == 60 * S
        names = []
        for t in data["tasks"]:
            names.append(t["name"])
            bind = t.get("bind") or {}
            if "child_name" in bind:
                names.append(bind["child_name"])
                if bind["child_name"] in rename.values():
                    assert t["source"]["child_name"] == "design"
            if "member_names" in bind:
                names.extend(bind["member_names"])
                if any(n in rename.values() for n in bind["member_names"]):
                    assert t["source"]["member_names"] == "design"
        assert not (set(rename) & set(names))   # every renamed real name is gone
        assert set(rename.values()) <= set(names)
        assert "wineserver" not in names
    browsing = composed(layer, "fl-browsing-t5-all")
    assert len({t["name"] for t in browsing["tasks"]}) == 1 and sum(t.get("count", 1) for t in browsing["tasks"]) == 5
    compile_others = composed(layer, "fl-compile-t4-others")
    build = task(compile_others, "build-s0")
    assert (build["name"], build["bind"]["child_name"]) == ("build-runner", "c-compiler")
    assert build["source"]["child_name"] == "design" and build["source"]["spawn_count"] == "design"
    assert task(compile_others, "editor-s0")["name"] == "code"
    render_t3 = composed(layer, "fl-render-t3")
    bulk = task(render_t3, "bulk-s0")
    assert bulk["name"] == "melt-7" and bulk["bind"]["program"] == "kdenlive_render"
    assert bulk["bind"]["total_work"] == "16.545s" and bulk["source"]["total_work"] == "meas-ci:background:2026-10-03c"
