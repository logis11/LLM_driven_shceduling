"""Canonical-output checks: schema conformance, the schema-declared linter
invariants, focus-driven wake generation, and the demand estimate."""

from wlc import Timeline, compile_timeline
from wlc.linter import lint_canonical


def compiled(fixture_path, library, name, mode="single"):
    timeline = Timeline(fixture_path(name), library)
    canonical, report = compile_timeline(timeline, library, mode, rel_path="fx")
    return timeline, canonical, report


def test_fixtures_lint_clean(fixture_path, library, schema):
    for name in ("fx-mixed.timeline.yaml", "fx-game.timeline.yaml",
                 "fx-oversub.timeline.yaml"):
        for mode in ("native", "single"):
            _, canonical, report = compiled(fixture_path, library, name, mode)
            assert lint_canonical(canonical, schema, report=report,
                                  mode=mode) == []


def test_events_sorted_and_ids_unique(fixture_path, library):
    _, canonical, _ = compiled(fixture_path, library, "fx-mixed.timeline.yaml")
    times = [e["t"] for e in canonical["events"]]
    assert times == sorted(times)
    ids = [e["id"] for e in canonical["events"] if e["op"] == "arrive"]
    assert len(ids) == len(set(ids))


def test_orchestrator_spawn_table(fixture_path, library):
    _, canonical, _ = compiled(fixture_path, library, "fx-mixed.timeline.yaml")
    build = next(e for e in canonical["events"]
                 if e["op"] == "arrive" and e["id"] == "build")
    assert build["fork_cap"] == 2
    assert len(build["spawn_table"]) == 6
    assert sum(1 for i in build["program"] if i["op"] == "FORK") == 6
    assert all(s["name"] == "cc1" for s in build["spawn_table"])
    assert all(s["program"][-1] == {"op": "EXIT"} for s in build["spawn_table"])
    assert "depart" not in build  # finite: ends via EXIT at an emergent time


def test_count_expansion(fixture_path, library):
    _, canonical, _ = compiled(fixture_path, library, "fx-mixed.timeline.yaml")
    renderers = [e for e in canonical["events"] if e["op"] == "arrive"
                 and e["id"].startswith("renderers.")]
    assert len(renderers) == 3
    assert all(e["name"] == "chrome" for e in renderers)
    periods = set()
    for event in renderers:
        body = event["program"][0]["body"]
        periods.add(next(i["period_us"] for i in body if i["op"] == "TIMER"))
    assert len(periods) == 3  # per-instance draws differ across the expansion


def test_focus_wakes_inside_windows(fixture_path, library):
    timeline, canonical, _ = compiled(fixture_path, library,
                                      "fx-mixed.timeline.yaml")
    wake_events = [e for e in canonical["events"] if e["op"] == "wake"]
    assert wake_events, "focused interactive task must receive input wakes"
    windows = [(w["from"], w["to"]) for w in timeline.focus]
    for event in wake_events:
        assert event["target"] == "editor"
        assert event["channel"] == "input:editor"
        assert any(lo <= event["t"] < hi for lo, hi in windows)
    editor = next(e for e in canonical["events"]
                  if e["op"] == "arrive" and e["id"] == "editor")
    bursts = [i for i in editor["program"] if i["op"] == "RUN"]
    assert len(bursts) == len(wake_events)  # one unrolled burst per wake


def test_demand_estimate(fixture_path, library):
    _, _, report = compiled(fixture_path, library, "fx-oversub.timeline.yaml")
    # cpu-batch 66s/60s + audio duty 2500/50000 = 1.10 + 0.05
    assert abs(report["utilization"] - 1.15) < 0.005
