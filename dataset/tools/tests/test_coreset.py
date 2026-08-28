"""Coreset-level invariants (task-2.4 spec): derive idempotency, the C2
one-entry-diff discipline on the real pair files, and window compliance."""

import pytest

from wlc import Timeline, compile_timeline
from wlc.deriver import DeriveError, apply_ops, run as derive_check
from wlc.linter import lint_canonical


@pytest.fixture(scope="module")
def coreset(repo_root, library):
    compiled = {}
    for path in sorted((repo_root / "dataset" / "timelines").glob(
            "**/*.timeline.yaml")):
        timeline = Timeline(path, library)
        canonical, report = compile_timeline(timeline, library, "single")
        compiled[timeline.id] = (canonical, report)
    return compiled


def test_derive_idempotent(repo_root):
    assert derive_check(repo_root / "dataset" / "timelines", check=True) == []


def events_by_id(canonical):
    return {e["id"]: e for e in canonical["events"] if e["op"] == "arrive"}


def test_p1_pair_rename_only(coreset):
    """P1 is the load-bearing pair: byte-identical except the hog's name
    and the second segment's label."""
    base, _ = coreset["c2-p1a"]
    variant, _ = coreset["c2-p1b"]
    base_events, variant_events = events_by_id(base), events_by_id(variant)
    assert set(base_events) == set(variant_events)
    for task_id, event in base_events.items():
        if task_id == "hog":
            assert variant_events[task_id]["name"] == "tracker-miner-fs-3"
            assert {**variant_events[task_id], "name": "python3"} == event
        else:
            assert variant_events[task_id] == event
    assert base["ground_truth"][0] == variant["ground_truth"][0]
    assert variant["ground_truth"][1]["mode"] == "indexing"
    wakes = lambda c: [e for e in c["events"] if e["op"] == "wake"]
    assert wakes(base) == wakes(variant)


@pytest.mark.parametrize("pair,changed", [
    (("c2-p2a", "c2-p2b"), "download"),
    (("c2-p3a", "c2-p3b"), "bulk"),
])
def test_pair_one_task_diff(coreset, pair, changed):
    base, _ = coreset[pair[0]]
    variant, _ = coreset[pair[1]]
    base_events, variant_events = events_by_id(base), events_by_id(variant)
    assert set(base_events) == set(variant_events)
    for task_id, event in base_events.items():
        if task_id == changed:
            assert variant_events[task_id] != event
        else:
            assert variant_events[task_id] == event


def test_c4_injection_only(coreset):
    base, _ = coreset["c1-gaming"]
    variant, _ = coreset["c4-gaming"]
    base_events, variant_events = events_by_id(base), events_by_id(variant)
    assert set(variant_events) - set(base_events) == {"injected-overlay"}
    for task_id, event in base_events.items():
        assert variant_events[task_id] == event


def test_c5_names_only(coreset):
    base, _ = coreset["c1-media"]
    for tier in ("c5-t3", "c5-t4", "c5-t5"):
        variant, _ = coreset[tier]
        base_events, variant_events = events_by_id(base), events_by_id(variant)
        assert set(base_events) == set(variant_events)
        for task_id, event in base_events.items():
            trimmed = {**variant_events[task_id], "name": event["name"]}
            assert trimmed == event  # identical but for the name


def test_c6_fold_tasks_unchanged(coreset):
    base, _ = coreset["c1-browsing"]
    variant, _ = coreset["c6-fold"]
    assert events_by_id(base) == events_by_id(variant)
    assert len(variant["ground_truth"]) == 2


def test_windows(coreset, schema):
    for name, (canonical, report) in coreset.items():
        assert lint_canonical(canonical, schema, report=report,
                              mode="single", name=name) == []


def test_variant_cannot_change_seed():
    with pytest.raises(DeriveError, match="unknown op"):
        apply_ops({"meta": {"seed": 1}, "tasks": [], "segments": []},
                  [{"set-seed": 2}], "test")
