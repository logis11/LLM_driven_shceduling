"""Constructed cases for the launch phase's compilation (9.10 changelog D21, D133, D136–D138)."""

import yaml

from wlc import Library, Timeline, compile_timeline
from wlc import compiler
from wlc.linter import lint_repo

SPEC = {"stream": "fx-launch", "sampling": "per-task", "source": "meas-ci:interactive:3"}
# two repeats of a whole tree, one stream each, each wake [t_us, run_us, thread]; the last wake of the first lies past
# its phase's end
DATA = {"repeats": [
    {"repeat": "1", "phase_us": 3_000_000, "streams": [
        [[0, 400_000, 0], [500_000, 300_000, 0], [2_500_000, 1_000, 0], [3_500_000, 9_999, 0]]]},
    {"repeat": "2", "phase_us": 3_000_000, "streams": [
        [[0, 410_000, 0], [600_000, 290_000, 0]]]}]}
# two repeats of a renderer group: two streams each, from which a group draws distinct ones
GROUP = {"repeats": [
    {"repeat": "1", "phase_us": 3_000_000, "streams": [
        [[0, 400_000, 0], [500_000, 300_000, 0], [2_500_000, 1_000, 0], [3_500_000, 9_999, 0]],
        [[100_000, 7_000, 0], [1_100_000, 8_000, 0]]]},
    {"repeat": "2", "phase_us": 3_000_000, "streams": [
        [[0, 410_000, 0], [600_000, 290_000, 0]],
        [[200_000, 6_000, 0]]]}]}


def _lib(tmp_path, repo_root, monkeypatch, entries, streams=DATA):
    data = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    for e in entries:
        data["archetypes"][e]["params"]["launch"] = dict(SPEC)
    path = tmp_path / "archetypes.yaml"
    path.write_text(yaml.safe_dump(data))
    monkeypatch.setitem(compiler._LAUNCH, "fx-launch", streams)
    return Library(path)


def _compile(tmp_path, lib, tasks, focus=(), operations=(), end="20s", seed=7):
    data = {"meta": {"id": "x-launch", "seed": seed, "demand": "calibration"},
            "segments": [{"from": "0s", "to": end, "mode": "office", "attributes": {"background_wanted": True}}],
            "tasks": tasks, "focus": list(focus), "operations": list(operations)}
    path = tmp_path / "x-launch.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    return compile_timeline(Timeline(path, lib), lib, "single", rel_path="fx")


def _timer_wakes(canonical, iid):
    return sorted(e["t"] for e in canonical["events"] if e["op"] == "wake" and e["channel"] == f"timer:{iid}")


def test_a_task_started_mid_file_replays_one_repeat_then_runs_steady(tmp_path, repo_root, monkeypatch):
    lib = _lib(tmp_path, repo_root, monkeypatch, ["office-writer"])
    canonical, report = _compile(tmp_path, lib, [{"id": "w", "name": "soffice.bin", "archetype": "office-writer",
                                                  "arrive": "2s", "depart": "20s"}])
    timer = _timer_wakes(canonical, "w")
    replay = [t for t in timer if t < 5_000_000]
    # one repeat's first stream from the arrival, its wakes past the phase's end left out (D136)
    assert replay in ([2_000_000, 2_500_000, 4_500_000], [2_000_000, 2_600_000])
    # the steady components begin at the phase's end, already running
    assert any(t >= 5_000_000 for t in timer)
    arrive = next(e for e in canonical["events"] if e["op"] == "arrive")
    runs = [s["us"] for s in arrive["program"] if s["op"] == "RUN"]
    assert runs[0] in (400_000, 410_000) and report["per_task"]["w"] == sum(runs)


def test_a_task_at_zero_seconds_is_steady_and_unchanged(tmp_path, repo_root, monkeypatch):
    task = [{"id": "w", "name": "soffice.bin", "archetype": "office-writer", "arrive": "0s", "depart": "20s"}]
    plain = Library(repo_root / "dataset" / "archetypes.yaml")
    a, _ = _compile(tmp_path, plain, task)
    lib = _lib(tmp_path, repo_root, monkeypatch, ["office-writer"])
    b, _ = _compile(tmp_path, lib, task)
    assert a["events"] == b["events"]


def test_a_task_group_draws_one_repeat_and_distinct_streams(tmp_path, repo_root, monkeypatch):
    lib = _lib(tmp_path, repo_root, monkeypatch, ["renderer-hidden"], GROUP)
    canonical, _ = _compile(tmp_path, lib, [{"id": "r", "name": "chrome", "archetype": "renderer-hidden",
                                             "arrive": "2s", "depart": "20s", "count": 2}])
    firsts = sorted(_timer_wakes(canonical, f"r.{n}")[0] for n in (1, 2))
    # one launch's two renderers, distinct: its streams start at 0 and 100 ms, or at 0 and 200 ms
    assert firsts in ([2_000_000, 2_100_000], [2_000_000, 2_200_000])


def test_an_operation_replaces_the_replay_inside_its_window(tmp_path, repo_root, monkeypatch):
    lib = _lib(tmp_path, repo_root, monkeypatch, ["office-writer"])
    # the replay is the timeline's to cut: a departure inside the phase ends it there (D21, D136)
    canonical, _ = _compile(tmp_path, lib, [{"id": "w", "name": "soffice.bin", "archetype": "office-writer",
                                             "arrive": "2s", "depart": "4s"}], end="4s")
    timer = _timer_wakes(canonical, "w")
    assert timer and max(timer) < 4_000_000 and 4_500_000 not in timer


def test_a_periodic_entry_bins_the_replay_onto_its_cycle_grid(tmp_path, repo_root, monkeypatch):
    lib = _lib(tmp_path, repo_root, monkeypatch, ["video-player"])
    canonical, _ = _compile(tmp_path, lib, [{"id": "v", "name": "mpv", "archetype": "video-player",
                                             "arrive": "2s", "depart": "20s"}])
    arrive = next(e for e in canonical["events"] if e["op"] == "arrive")
    period = lib.entry("video-player")["params"]["period"]["value_us"]
    prog = arrive["program"]
    timers = [i for i, s in enumerate(prog) if s["op"] == "TIMER"]
    # the grid from the arrival, unchanged (D138)
    assert len(timers) == -(-18_000_000 // period)
    runs = [prog[i + 1]["us"] if i + 1 < len(prog) and prog[i + 1]["op"] == "RUN" else 0 for i in timers]
    # cycle 0 carries the first wake's 400 or 410 ms; the cycles of the phase carry nothing else but its wakes
    assert runs[0] in (400_000, 410_000)
    in_phase = -(-3_000_000 // period)
    assert sum(runs[:in_phase]) in (400_000 + 300_000 + 1_000, 410_000 + 290_000)
    assert sum(1 for r in runs[in_phase:] if r) > 0   # steady cycles past the phase


def test_the_linter_wants_the_launch_streams_file(tmp_path, repo_root):
    data = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    data["archetypes"]["office-writer"]["params"]["launch"] = {"stream": "nonesuch", "sampling": "per-task",
                                                              "source": "meas-ci:interactive:2026-09-18"}
    path = tmp_path / "archetypes.yaml"
    path.write_text(yaml.safe_dump(data))
    errors = lint_repo(path, repo_root / "dataset" / "sources.yaml", repo_root / "docs" / "references.md")
    assert any("stream 'nonesuch' has no file at dataset/launch/" in e for e in errors)
