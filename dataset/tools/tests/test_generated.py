"""The generated layer (9.19 spec): the grid definition, the cells, the composition rules (decisions 1–3, 10), the
splits and seeds (decision 6), the flap-stress set (decision 7), and what each set's manifest records (decisions 4–6)."""

import hashlib
import importlib
import json

import pytest
import yaml

from gen import c1_sets, cells, compose, lint_grids, load_definition, modes_of, ordered_pairs, seed_of
from gen.cells import ranked_pairs
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
    by_set = cells(defn, modes)
    return {"defn": defn, "modes": modes, "by_set": by_set, "sets": c1_sets(dataset / "timelines" / "coreset"),
            "by_id": {c["id"]: c for s in by_set.values() for c in s}}


def composed(layer, cell_id):
    return compose(layer["by_id"][cell_id], layer["sets"], layer["defn"])


def task(data, task_id):
    return next(t for t in data["tasks"] if t["id"] == task_id)


def spans(items):
    return [(parse_us(x["from"]), parse_us(x["to"])) for x in items]


def test_the_definition_names_the_sixteen_modes_the_240_pairs_and_the_three_sets(layer):
    assert layer["modes"] == MODES
    assert len(ordered_pairs(layer["modes"])) == 240 == len({p for p in ordered_pairs(layer["modes"])})
    assert {k: len(v) for k, v in layer["by_set"].items()} == {"transition-grid": 480, "return-grid": 720,
                                                              "flap-stress": 24}
    assert len(layer["by_id"]) == 1224


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
    assert len({c["seed"] for c in layer["by_id"].values()}) == 1224


def test_every_cell_loads_as_a_timeline_with_sourced_bound_values(layer, library, repo_root, tmp_path):
    """The 1,224 cells written and read back through the loader's structural checks and the bound-source lint."""
    registry = yaml.safe_load((repo_root / "dataset" / "sources.yaml").read_text())["sources"]
    errors = []
    for cell in layer["by_id"].values():
        path = tmp_path / f"{cell['id']}.timeline.yaml"
        path.write_bytes(timeline_bytes(cell, layer["sets"], layer["defn"]))
        errors.extend(lint_bound_sources(path, registry))
        timeline = Timeline(path, library)
        assert timeline.id == cell["id"] and timeline.seed == cell["seed"]
        assert len(timeline.segments) == len(cell["placements"])
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
            assert manifest["grid"][rel] == coords
