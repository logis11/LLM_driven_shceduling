"""The trace-replay set of the variant builder (9.14 decision 12): the library copy's `replay` params and the
variant's report."""

import json

import pytest
import yaml

from wlc import compiler
from wlc.variants import VariantError, build_variant, load_spec, replayed_library

SOURCE = "meas-ci:interactive:2026-09-25"


def _doc(entry, kind, phase_us, streams, program=None, source=SOURCE):
    return {"entry": entry, "program": program, "kind": kind, "source": source,
            "repeats": [{"repeat": "1", "run_id": "0", "phase_us": phase_us, "comms": ["x"], "streams": streams}]}


def test_the_library_copy_points_each_entry_at_its_stream_with_the_streams_source(repo_root, monkeypatch):
    lib_doc = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    monkeypatch.setitem(compiler._REPLAY, "fx-a", _doc("code-editor", "wakes", 1, [[]], source="meas-ci:interactive:2026-09-25"))
    monkeypatch.setitem(compiler._REPLAY, "fx-b", _doc("cpu-batch", "runs", 0, [[]], "python3", "meas-ci:background:2026-10-03"))
    out = replayed_library(lib_doc, {"code-editor": "fx-a", "cpu-batch": "fx-b"})
    assert out["archetypes"]["code-editor"]["params"]["replay"] == {
        "stream": "fx-a", "sampling": "per-task", "source": "meas-ci:interactive:2026-09-25"}
    assert out["archetypes"]["cpu-batch"]["params"]["replay"] == {
        "stream": "fx-b", "sampling": "per-task", "source": "meas-ci:background:2026-10-03"}
    assert "replay" not in lib_doc["archetypes"]["code-editor"]["params"]   # a copy
    with pytest.raises(VariantError, match="nonesuch"):
        replayed_library(lib_doc, {"nonesuch": "fx-a"})


def test_a_replay_variant_reports_what_each_task_replayed(repo_root, tmp_path, monkeypatch):
    build_dir = repo_root / "dataset" / "build" / "coreset-single"
    if not (build_dir / "c7-dev.workload.json").exists():
        pytest.skip("needs the compiled coreset")
    grid = [[k * 1_000_000, 100, 0] for k in range(30)]
    runs = [[k * 10_000, 5_000, 5_000] for k in range(6000)]   # 30 s of CPU in 5 ms runs
    monkeypatch.setitem(compiler._REPLAY, "fx-editor", _doc("code-editor", "wakes", 30_000_000, [grid]))
    monkeypatch.setitem(compiler._REPLAY, "fx-upgrade", _doc("package-upgrade", "runs", 0, [runs], source="meas-ci:background:2026-10-01"))
    spec = load_spec(repo_root / "dataset" / "variants.yaml")
    set_spec = {"name": "replay", "transform": "trace-replay", "files": ["c7-dev"],
                "streams": {"code-editor": "fx-editor", "package-upgrade": "fx-upgrade"}}
    canonical, report = build_variant(spec, set_spec, "c7-dev", repo_root, build_dir, tmp_path)
    assert canonical["meta"]["id"] == "c7-dev@replay"
    base = json.loads((build_dir / "c7-dev.workload.json").read_text())
    assert canonical["meta"]["derived_from"] == base["meta"]["derived_from"]
    assert report["replay"]["editor"]["stream"] == "fx-editor" and 0 <= report["replay"]["editor"]["offset_us"] <= 3_615_000
    assert report["replay"]["upgrade"] == {"stream": "fx-upgrade", "offset_us": 0}
    timer = sorted(e["t"] for e in canonical["events"] if e["op"] == "wake" and e["channel"] == "timer:editor")
    assert len(timer) in (26, 27) and all(b - a == 1_000_000 for a, b in zip(timer, timer[1:]))   # 26.385 s of the grid
