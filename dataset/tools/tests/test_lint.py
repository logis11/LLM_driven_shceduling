"""Linter behavior: repo lints on the real repo, the freeze gate, the
registry subset rule, timeline structural rules, and the demand window."""

import pytest
import yaml

from wlc import Timeline, TimelineError, compile_timeline
from wlc.linter import lint_canonical, lint_repo


def test_real_repo_lint_clean(repo_root):
    errors = lint_repo(repo_root / "dataset" / "archetypes.yaml",
                       repo_root / "dataset" / "sources.yaml",
                       repo_root / "docs" / "references.md")
    assert errors == []


def test_repo_is_freeze_clean(repo_root):
    """All meas-pending placeholders have been folded in (cli:3/gui:2)."""
    errors = lint_repo(repo_root / "dataset" / "archetypes.yaml",
                       repo_root / "dataset" / "sources.yaml",
                       repo_root / "docs" / "references.md", freeze=True)
    assert errors == []


def test_freeze_rejects_meas_pending(repo_root, tmp_path):
    archetypes = tmp_path / "archetypes.yaml"
    archetypes.write_text(
        "archetypes:\n"
        "  probe:\n"
        "    category_source: meas\n"
        "    pattern: {program: []}\n"
        "    params:\n"
        "      x: {dist: constant, value_us: 1, sampling: per-task,\n"
        "          source: meas-pending}\n"
        "    lifetime: finite\n"
        "    binding_params: []\n"
        "    scalable: []\n"
        "    validation_stats: {}\n"
        "    modeling_notes: probe\n")
    sources = repo_root / "dataset" / "sources.yaml"
    references = repo_root / "docs" / "references.md"
    assert lint_repo(archetypes, sources, references, freeze=False) == []
    errors = lint_repo(archetypes, sources, references, freeze=True)
    assert errors == ["probe.x: meas-pending after freeze"]


def test_registry_subset_rule(repo_root, tmp_path):
    sources = tmp_path / "sources.yaml"
    sources.write_text((repo_root / "dataset" / "sources.yaml").read_text()
                       + "\n  ghost-source:\n    type: scholarly\n"
                         "    notes: not in references\n")
    errors = lint_repo(repo_root / "dataset" / "archetypes.yaml", sources,
                       repo_root / "docs" / "references.md")
    assert errors == ["registry id 'ghost-source' has no docs/references.md "
                      "entry (subset lint)"]


BASE = {
    "meta": {"id": "bad", "seed": 1, "demand": "calibration"},
    "segments": [{"from": "0s", "to": "10s", "mode": "office"}],
    "tasks": [{"id": "player", "name": "mpv", "archetype": "audio-playback",
               "arrive": "0s", "depart": "10s"}],
}


def load_bad(tmp_path, mutate):
    data = {"meta": dict(BASE["meta"]),
            "segments": [dict(s) for s in BASE["segments"]],
            "tasks": [dict(t) for t in BASE["tasks"]], "focus": []}
    mutate(data)
    path = tmp_path / "bad.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    return path


@pytest.mark.parametrize("expect,mutate", [
    ("unknown archetype",
     lambda d: d["tasks"][0].update(archetype="nonesuch")),
    ("not in 'audio-playback' binding_params",
     lambda d: d["tasks"][0].update(bind={"burst_len": 5})),
    ("missing bind keys",
     lambda d: d["tasks"].append({"id": "job", "name": "ffmpeg",
                                  "archetype": "io-stream", "arrive": "0s"})),
    ("depart missing but archetype lifetime is 'segment-bound'",
     lambda d: d["tasks"][0].pop("depart")),
    ("depart present but archetype lifetime is 'finite'",
     lambda d: d["tasks"].append({"id": "job", "name": "python3",
                                  "archetype": "cpu-batch", "arrive": "0s",
                                  "depart": "5s", "bind": {"total_work": "1s"}})),
    ("spawned-only",
     lambda d: d["tasks"].append({"id": "kid", "name": "cc1",
                                  "archetype": "compiler-child", "arrive": "0s"})),
    ("duplicate task id",
     lambda d: d["tasks"].append(dict(d["tasks"][0]))),
    ("segments overlap",
     lambda d: d["segments"].append({"from": "5s", "to": "15s", "mode": "x"})),
    ("no input channel",
     lambda d: d["focus"].append({"from": "1s", "to": "2s", "task": "player"})),
    ("focus windows overlap",
     lambda d: (d["tasks"].append({"id": "ed", "name": "code",
                                   "archetype": "desktop-interactive",
                                   "arrive": "0s", "depart": "10s"}),
                d["focus"].extend([{"from": "1s", "to": "5s", "task": "ed"},
                                   {"from": "4s", "to": "6s", "task": "ed"}]))),
    ("outside task",
     lambda d: (d["tasks"].append({"id": "ed", "name": "code",
                                   "archetype": "desktop-interactive",
                                   "arrive": "2s", "depart": "10s"}),
                d["focus"].append({"from": "1s", "to": "5s", "task": "ed"}))),
    ("meta.demand",
     lambda d: d["meta"].update(demand="whatever")),
])
def test_timeline_rules(tmp_path, library, expect, mutate):
    with pytest.raises(TimelineError, match=expect):
        Timeline(load_bad(tmp_path, mutate), library)


def test_demand_window_enforced(tmp_path, library, schema):
    """An underloaded default-class file fails -single lint; the calibration
    class and -native mode are exempt."""
    data = {"meta": {"id": "under", "seed": 1},
            "segments": [{"from": "0s", "to": "60s", "mode": "office"}],
            "tasks": [{"id": "job", "name": "python3", "archetype": "cpu-batch",
                       "arrive": "0s", "bind": {"total_work": "20s"}}]}
    path = tmp_path / "under.timeline.yaml"
    path.write_text(yaml.safe_dump(data))
    timeline = Timeline(path, library)

    canonical, report = compile_timeline(timeline, library, "single")
    errors = lint_canonical(canonical, schema, report=report, mode="single")
    assert len(errors) == 1 and "outside" in errors[0]

    canonical, report = compile_timeline(timeline, library, "native")
    assert lint_canonical(canonical, schema, report=report, mode="native") == []

    data["meta"]["demand"] = "calibration"
    path.write_text(yaml.safe_dump(data))
    timeline = Timeline(path, library)
    canonical, report = compile_timeline(timeline, library, "single")
    assert lint_canonical(canonical, schema, report=report, mode="single") == []
