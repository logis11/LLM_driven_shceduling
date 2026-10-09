"""Constructed cases for the trace-replay variant's compilation (9.14 decision 12; the replay set of
dataset/variants.yaml): an entry whose params carry `replay` compiles each task from one pooled repeat's observed
stream (dataset/replay/<stream>.json.gz) in place of its sampled one."""

import pytest
import yaml

from wlc import Library, Timeline, compile_timeline
from wlc import compiler
from wlc.linter import lint_repo

SOURCE = "meas-ci:interactive:2026-09-25"


def _doc(entry, kind, phase_us, streams, program=None):
    """A replay stream file's document: one repeat, one or more streams of [t_us, x, y] rows (the columns per kind)."""
    return {"entry": entry, "program": program, "kind": kind, "source": SOURCE,
            "repeats": [{"repeat": "1", "run_id": "0", "phase_us": phase_us, "comms": ["x"], "streams": streams}]}


def _lib(tmp_path, repo_root, monkeypatch, entries, doc, name="fx-replay"):
    data = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    for e in entries:
        data["archetypes"][e]["params"]["replay"] = {"stream": name, "sampling": "per-task", "source": SOURCE}
    path = tmp_path / "archetypes.yaml"
    path.write_text(yaml.safe_dump(data))
    monkeypatch.setitem(compiler._REPLAY, name, doc)
    return Library(path)


def _compile(tmp_path, lib, tasks, focus=(), operations=(), end="20s", seed=7):
    data = {"meta": {"id": "x-replay", "seed": seed, "demand": "calibration"},
            "segments": [{"from": "0s", "to": end, "mode": "office", "attributes": {"background_wanted": True}}],
            "tasks": tasks, "focus": list(focus), "operations": list(operations)}
    path = tmp_path / "x-replay.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    return compile_timeline(Timeline(path, lib), lib, "single", rel_path="fx")


def _wakes(canonical, iid, channel):
    return sorted(e["t"] for e in canonical["events"] if e["op"] == "wake" and e["channel"] == f"{channel}:{iid}")


def _program(canonical, iid):
    return next(e for e in canonical["events"] if e["op"] == "arrive" and e["id"] == iid)["program"]


EDITOR = [{"id": "w", "name": "code", "archetype": "code-editor", "arrive": "0s", "depart": "20s"}]
GRID = [[k * 1_000_000, 1000 + k, 0] for k in range(20)]   # a wake a second over 20 s


def test_a_measured_entry_replays_the_stream_in_place_of_its_components(tmp_path, repo_root, monkeypatch):
    # the stream spans exactly the task's lifetime, so the window is the whole of it
    lib = _lib(tmp_path, repo_root, monkeypatch, ["code-editor"], _doc("code-editor", "wakes", 20_000_000, [GRID]))
    canonical, report = _compile(tmp_path, lib, EDITOR)
    assert _wakes(canonical, "w", "timer") == [t for t, _, _ in GRID]
    runs = [s["us"] for s in _program(canonical, "w") if s["op"] == "RUN"]
    assert runs == [r for _, r, _ in GRID] and report["per_task"]["w"] == sum(runs)
    assert report["replay"]["w"] == {"stream": "fx-replay", "offset_us": 0}


def test_the_window_is_a_seeded_contiguous_slice_of_a_longer_stream(tmp_path, repo_root, monkeypatch):
    long = [[k * 1_000_000, 1, 0] for k in range(40)]   # 40 s of a wake a second; the task lives 20 s
    lib = _lib(tmp_path, repo_root, monkeypatch, ["code-editor"], _doc("code-editor", "wakes", 40_000_000, [long]))
    firsts = {}
    for seed in (7, 8, 9):
        canonical, report = _compile(tmp_path, lib, EDITOR, seed=seed)
        timer = _wakes(canonical, "w", "timer")
        assert len(timer) == 20 and all(b - a == 1_000_000 for a, b in zip(timer, timer[1:]))
        assert 0 <= timer[0] < 1_000_000
        offset = report["replay"]["w"]["offset_us"]
        assert 0 <= offset <= 20_000_000 and timer[0] == (-offset) % 1_000_000
        again, _ = _compile(tmp_path, lib, EDITOR, seed=seed)
        assert _wakes(again, "w", "timer") == timer
        firsts[seed] = offset
    assert len(set(firsts.values())) > 1   # a draw by the seed, not the phase's opening


def test_the_keystroke_replay_stays_as_compiled_over_the_replayed_stream(tmp_path, repo_root, monkeypatch):
    focus = [{"from": "2s", "to": "18s", "task": "w"}]
    plain, _ = _compile(tmp_path, Library(repo_root / "dataset" / "archetypes.yaml"), EDITOR, focus=focus)
    lib = _lib(tmp_path, repo_root, monkeypatch, ["code-editor"], _doc("code-editor", "wakes", 20_000_000, [GRID]))
    replayed, _ = _compile(tmp_path, lib, EDITOR, focus=focus)
    assert _wakes(replayed, "w", "input") == _wakes(plain, "w", "input") != []
    assert _wakes(replayed, "w", "timer") == [t for t, _, _ in GRID]


BROWSER = [{"id": "b", "name": "chrome", "archetype": "web-browser", "arrive": "0s", "depart": "20s"}]


def test_an_operation_keeps_its_precedence_over_the_replay(tmp_path, repo_root, monkeypatch):
    fine = [[k * 100_000, 10, 0] for k in range(200)]   # a wake every 100 ms
    lib = _lib(tmp_path, repo_root, monkeypatch, ["web-browser"], _doc("web-browser", "wakes", 20_000_000, [fine]))
    canonical, report = _compile(tmp_path, lib, BROWSER, operations=[{"at": "5s", "name": "page-load", "task": "b"}])
    op = report["operations"]["b"][0]
    lo, hi = op["at_us"], op["at_us"] + op["duration_us"]
    timer = set(_wakes(canonical, "b", "timer"))
    grid = {t for t, _, _ in fine}
    assert {t for t in grid if not lo <= t < hi} <= timer           # the stream outside the window
    assert not {t for t in grid if lo <= t < hi} & timer             # dropped inside it
    assert any(lo <= t < hi for t in timer)                          # the operation's components run there


def test_a_task_started_mid_file_replays_the_stream_and_no_launch_phase(tmp_path, repo_root, monkeypatch):
    grid = [[k * 1_000_000, 5, 0] for k in range(18)]
    lib = _lib(tmp_path, repo_root, monkeypatch, ["web-browser"], _doc("web-browser", "wakes", 18_000_000, [grid]))
    assert "launch" in lib.entry("web-browser")["params"]
    canonical, _ = _compile(tmp_path, lib, [dict(BROWSER[0], arrive="2s")])
    assert _wakes(canonical, "b", "timer") == [2_000_000 + t for t, _, _ in grid]


def test_a_task_group_takes_distinct_streams_of_the_repeat(tmp_path, repo_root, monkeypatch):
    a = [[k * 1_000_000, 7, 0] for k in range(20)]
    b = [[k * 1_000_000 + 500_000, 8, 0] for k in range(20)]
    lib = _lib(tmp_path, repo_root, monkeypatch, ["renderer-hidden"],
               _doc("renderer-hidden", "wakes", 20_000_000, [a, b]))
    canonical, _ = _compile(tmp_path, lib, [{"id": "r", "name": "chrome", "archetype": "renderer-hidden",
                                             "arrive": "0s", "depart": "20s", "count": 2}])
    got = sorted([_wakes(canonical, "r.1", "timer"), _wakes(canonical, "r.2", "timer")])
    assert got == sorted([[t for t, _, _ in a], [t for t, _, _ in b]])


CALL = [{"id": "v", "name": "chrome", "archetype": "video-call", "arrive": "0s", "depart": "20s"}]


def test_a_periodic_entry_takes_the_cycle_runs_in_order_on_its_own_grid(tmp_path, repo_root, monkeypatch):
    # 3 000 observed cycles 10 ms apart over 30 s, work 100 + k (one of them zero); the task lives 20 s
    cycles = [[k * 10_000, 0 if k == 1500 else 100 + k, 10_000] for k in range(3000)]
    lib = _lib(tmp_path, repo_root, monkeypatch, ["video-call"], _doc("video-call", "cycles", 30_000_000, [cycles]))
    canonical, report = _compile(tmp_path, lib, CALL)
    prog = _program(canonical, "v")
    period = lib.entry("video-call")["params"]["period"]["value_us"]
    timers = [i for i, s in enumerate(prog) if s["op"] == "TIMER"]
    assert len(timers) == -(-20_000_000 // period) and all(prog[i]["period_us"] == period for i in timers)
    runs = [prog[i + 1]["us"] if i + 1 < len(prog) and prog[i + 1]["op"] == "RUN" else 0 for i in timers]
    offset = report["replay"]["v"]["offset_us"]
    k0 = next(k for k, c in enumerate(cycles) if c[0] >= offset)
    assert runs == [c[1] for c in cycles[k0:k0 + len(timers)]]
    assert report["per_task"]["v"] == sum(runs)


UPGRADE = [{"id": "u", "name": "unattended-upgr", "archetype": "package-upgrade", "arrive": "0s",
            "bind": {"total_work": "10ms"}}]
RUNS = [[0, 3000, 1000], [4000, 2000, 0], [6000, 4000, 500], [10_500, 5000, 100]]   # [t, run, block after]


def test_a_batch_entry_takes_run_block_pairs_from_the_start_until_its_total_work(tmp_path, repo_root, monkeypatch):
    lib = _lib(tmp_path, repo_root, monkeypatch, ["package-upgrade"], _doc("package-upgrade", "runs", 0, [RUNS]))
    canonical, report = _compile(tmp_path, lib, UPGRADE)
    # a zero block joins the runs on either side (D25); the last run is cut at the bind
    assert _program(canonical, "u") == [{"op": "RUN", "us": 3000}, {"op": "SLEEP", "us": 1000},
                                        {"op": "RUN", "us": 6000}, {"op": "SLEEP", "us": 500},
                                        {"op": "RUN", "us": 1000}, {"op": "EXIT"}]
    assert report["per_task"]["u"] == 10_000 and report["replay"]["u"] == {"stream": "fx-replay", "offset_us": 0}


HOG = [{"id": "h", "name": "python", "archetype": "cpu-batch", "arrive": "0s",
        "bind": {"total_work": "10ms", "program": "python3"}}]


def test_a_batch_stream_applies_to_the_program_it_names_alone(tmp_path, repo_root, monkeypatch):
    doc = _doc("cpu-batch", "runs", 0, [RUNS], program="python3")
    lib = _lib(tmp_path, repo_root, monkeypatch, ["cpu-batch"], doc)
    canonical, report = _compile(tmp_path, lib, HOG)
    assert _program(canonical, "h")[0] == {"op": "RUN", "us": 3000} and report["replay"]["h"]["offset_us"] == 0
    other = [dict(HOG[0], name="kdenlive_rende", bind={"total_work": "10ms", "program": "kdenlive_render"})]
    plain, _ = _compile(tmp_path, Library(repo_root / "dataset" / "archetypes.yaml"), other)
    replayed, report = _compile(tmp_path, lib, other)
    assert _program(replayed, "h") == _program(plain, "h")
    assert report["replay"]["h"] == {"stream": "fx-replay", "applied": False, "program": "kdenlive_render"}


def test_a_stream_shorter_than_its_task_fails_the_build(tmp_path, repo_root, monkeypatch):
    short = [[k * 1_000_000, 1, 0] for k in range(10)]
    lib = _lib(tmp_path, repo_root, monkeypatch, ["code-editor"], _doc("code-editor", "wakes", 10_000_000, [short]))
    with pytest.raises(ValueError, match=r"code-editor.*fx-replay.*10000000.*20000000"):
        _compile(tmp_path, lib, EDITOR)
    few = [[k * 10_000, 100, 10_000] for k in range(100)]   # 1 s of cycles under a 20 s task
    lib = _lib(tmp_path, repo_root, monkeypatch, ["video-call"], _doc("video-call", "cycles", 1_000_000, [few]))
    with pytest.raises(ValueError, match=r"video-call.*fx-replay"):
        _compile(tmp_path, lib, CALL)
    lib = _lib(tmp_path, repo_root, monkeypatch, ["package-upgrade"],
               _doc("package-upgrade", "runs", 0, [[[0, 3000, 1000], [4000, 2000, 0]]]))
    with pytest.raises(ValueError, match=r"package-upgrade.*fx-replay.*5000.*10000"):
        _compile(tmp_path, lib, UPGRADE)


def test_a_stream_of_the_wrong_kind_fails_the_build(tmp_path, repo_root, monkeypatch):
    lib = _lib(tmp_path, repo_root, monkeypatch, ["video-call"], _doc("video-call", "wakes", 20_000_000, [GRID]))
    with pytest.raises(ValueError, match=r"video-call.*cycles.*wakes"):
        _compile(tmp_path, lib, CALL)


def test_the_linter_wants_the_replay_streams_file(tmp_path, repo_root):
    data = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    data["archetypes"]["code-editor"]["params"]["replay"] = {"stream": "nonesuch", "sampling": "per-task",
                                                            "source": SOURCE}
    path = tmp_path / "archetypes.yaml"
    path.write_text(yaml.safe_dump(data))
    errors = lint_repo(path, repo_root / "dataset" / "sources.yaml", repo_root / "docs" / "references.md")
    assert any("stream 'nonesuch' has no file at dataset/replay/" in e for e in errors)
