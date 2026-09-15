"""Measured archetypes (9.5 fold-in): the quantiles distribution (D17), the
merged event stream (D9, D16), the replayed stimulus (D18) and the linter's
checks on components and stimulus."""

import json

import pytest
import yaml

from wlc import Timeline, compile_timeline, sampling
from wlc.compiler import canonical_bytes
from wlc.linter import lint_repo


Q = {"dist": "quantiles", "p": [10, 20, 30, 50, 100, 150, 200, 300, 500, 1000],
     "sampling": "per-iteration", "source": "meas-ci:interactive:3"}


def test_quantiles_reproduce_the_table():
    values = sorted(sampling.sample(Q, 7, "t", i) for i in range(20000))
    assert abs(values[10000] - 100) <= 3 and abs(values[18000] - 200) <= 6
    assert values[0] >= 10 and values[-1] <= 1000
    assert abs(sampling.mean_us(Q) - sum(values) / len(values)) < 3


def test_quantiles_are_keyed_and_deterministic():
    assert sampling.sample(Q, 7, "a", 1) == sampling.sample(Q, 7, "a", 1)
    assert [sampling.sample(Q, 7, "a", i) for i in range(50)] != [sampling.sample(Q, 7, "b", i) for i in range(50)]


def _timeline(tmp_path, tasks, focus, seed=3):
    data = {"meta": {"id": "x-measured", "seed": seed, "demand": "calibration"},
            "segments": [{"from": "0s", "to": "20s", "mode": "office", "attributes": {"background_wanted": True}}],
            "tasks": tasks, "focus": focus}
    path = tmp_path / "x-measured.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    return path


def test_measured_task_is_one_explicit_stream(tmp_path, library):
    path = _timeline(tmp_path, [{"id": "ed", "name": "soffice.bin", "archetype": "office-writer",
                                 "arrive": "0s", "depart": "20s"}],
                     [{"from": "2s", "to": "12s", "task": "ed"}])
    canonical, report = compile_timeline(Timeline(path, library), library, "single", rel_path="fx")
    arrive = next(e for e in canonical["events"] if e["op"] == "arrive")
    ops = [step["op"] for step in arrive["program"]]
    assert set(ops) <= {"TIMER", "WAIT", "RUN"} and ops.count("RUN") == ops.count("TIMER") + ops.count("WAIT")
    # timer periods chain to absolute deadlines inside the lifetime
    deadline = 0
    for step in arrive["program"]:
        if step["op"] == "TIMER":
            assert step["period_us"] >= 1
            deadline += step["period_us"]
    assert deadline < 20_000_000
    # input wakes only inside the focus window, one per WAIT
    wakes = [e for e in canonical["events"] if e["op"] == "wake"]
    assert len(wakes) == ops.count("WAIT") > 0
    assert all(2_000_000 <= w["t"] < 12_000_000 for w in wakes)
    assert report["per_task"]["ed"] == sum(s["us"] for s in arrive["program"] if s["op"] == "RUN")


def test_stimulus_slice_preserves_recorded_gaps(tmp_path, library):
    path = _timeline(tmp_path, [{"id": "ed", "name": "soffice.bin", "archetype": "office-writer",
                                 "arrive": "0s", "depart": "20s"}],
                     [{"from": "0s", "to": "20s", "task": "ed"}])
    canonical, _ = compile_timeline(Timeline(path, library), library, "single", rel_path="fx")
    wakes = sorted(e["t"] for e in canonical["events"] if e["op"] == "wake")
    gaps = {b - a for a, b in zip(wakes, wakes[1:])}
    stream = [json.loads(l)["t_us"] for l in open(library.path.parent / "stimulus" / "swell-word-c1.jsonl")]
    recorded = {b - a for a, b in zip(stream, stream[1:])}
    assert gaps and gaps <= recorded  # every simulated gap is a recorded gap (a contiguous slice)


def test_measured_stream_is_deterministic_and_seed_dependent(tmp_path, library):
    tasks = [{"id": "ed", "name": "code", "archetype": "code-editor", "arrive": "0s", "depart": "20s"}]
    focus = [{"from": "1s", "to": "6s", "task": "ed"}]
    a, _ = compile_timeline(Timeline(_timeline(tmp_path, tasks, focus, seed=3), library), library, "single", rel_path="fx")
    b, _ = compile_timeline(Timeline(_timeline(tmp_path, tasks, focus, seed=3), library), library, "single", rel_path="fx")
    c, _ = compile_timeline(Timeline(_timeline(tmp_path, tasks, focus, seed=4), library), library, "single", rel_path="fx")
    assert canonical_bytes(a) == canonical_bytes(b) != canonical_bytes(c)


def test_cadence_archetype_swaps_components_in_focus(tmp_path, library):
    path = _timeline(tmp_path, [{"id": "px", "name": "gimp", "archetype": "image-editor",
                                 "arrive": "0s", "depart": "20s"}],
                     [{"from": "5s", "to": "15s", "task": "px"}])
    canonical, _ = compile_timeline(Timeline(path, library), library, "single", rel_path="fx")
    arrive = next(e for e in canonical["events"] if e["op"] == "arrive")
    assert not [e for e in canonical["events"] if e["op"] == "wake"]  # scripted stimulus: no input wakes
    deadlines, t = [], 0
    for step in arrive["program"]:
        if step["op"] == "TIMER":
            t += step["period_us"]; deadlines.append(t)
    assert deadlines and all(5_000_000 <= d < 15_000_000 for d in deadlines)  # GIMP idles silently outside focus


def test_playback_archetype_runs_the_whole_lifetime(tmp_path, library):
    path = _timeline(tmp_path, [{"id": "v", "name": "mpv", "archetype": "video-player",
                                 "arrive": "0s", "depart": "20s"}], [])
    canonical, report = compile_timeline(Timeline(path, library), library, "single", rel_path="fx")
    arrive = next(e for e in canonical["events"] if e["op"] == "arrive")
    timers = [s for s in arrive["program"] if s["op"] == "TIMER"]
    assert 20 * 600 < len(timers) < 20 * 1000  # ≈ 790 wakes/s measured


def test_linter_checks_components_and_stimulus(tmp_path, repo_root):
    lib = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    entry = lib["archetypes"]["office-writer"]
    entry["params"]["stimulus"]["stream"] = "nonesuch"
    entry["params"]["components"][0]["gap"]["p"][3] = 10 ** 9  # not non-decreasing
    del entry["params"]["components"][0]["run"]
    path = tmp_path / "archetypes.yaml"
    path.write_text(yaml.safe_dump(lib))
    errors = lint_repo(path, repo_root / "dataset" / "sources.yaml", repo_root / "docs" / "references.md")
    joined = "\n".join(errors)
    assert "stream 'nonesuch'" in joined and "non-decreasing" in joined and "missing 'run'" in joined
