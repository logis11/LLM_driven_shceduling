"""The task-2.3 spec's invariant charter: determinism, keyed isolation,
one-entry diffs, and the single-lane scaling rule (the native mode left in 9.13)."""

import pytest
import yaml

from wlc import Timeline, compile_timeline
from wlc.compiler import MODES, canonical_bytes


def compile_fixture(path, library, mode, rel="fx"):
    timeline = Timeline(path, library)
    return compile_timeline(timeline, library, mode, rel_path=rel)


def arrivals_by_id(canonical):
    return {e["id"]: e for e in canonical["events"] if e["op"] == "arrive"}


def wakes(canonical):
    return [e for e in canonical["events"] if e["op"] == "wake"]


def rewrite(tmp_path, source, mutate):
    data = yaml.safe_load(source.read_text())
    mutate(data)
    out = tmp_path / source.name
    out.write_text(yaml.safe_dump(data))
    return out


def test_byte_determinism(fixture_path, library):
    path = fixture_path("fx-mixed.timeline.yaml")
    first, _ = compile_fixture(path, library, "single")
    second, _ = compile_fixture(path, library, "single")
    assert canonical_bytes(first) == canonical_bytes(second)


def test_keyed_isolation_unrelated_task(fixture_path, library, tmp_path):
    """Adding a task must not shift any other task's draws (spec §5)."""
    base_path = fixture_path("fx-mixed.timeline.yaml")
    base, _ = compile_fixture(base_path, library, "single")
    extended_path = rewrite(tmp_path, base_path, lambda d: d["tasks"].append(
        {"id": "extra", "name": "sleepd", "archetype": "service-manager",
         "arrive": "0s", "depart": "60s"}))
    extended, _ = compile_fixture(extended_path, library, "single")

    base_arrivals, new_arrivals = arrivals_by_id(base), arrivals_by_id(extended)
    assert set(new_arrivals) == set(base_arrivals) | {"extra"}
    for task_id, event in base_arrivals.items():
        assert new_arrivals[task_id] == event
    # the added task brings wakes of its own (a measured task's timer wakes, 9.5 D74); every other task's are unchanged
    assert [w for w in wakes(extended) if w["target"] != "extra"] == wakes(base)
    assert all(w["channel"] == "timer:extra" for w in wakes(extended) if w["target"] == "extra")


def test_one_entry_diff(fixture_path, library, tmp_path):
    """C2 discipline: a one-field edit changes exactly that task's event."""
    base_path = fixture_path("fx-mixed.timeline.yaml")
    base, _ = compile_fixture(base_path, library, "single")

    def rename(data):
        for task in data["tasks"]:
            if task["id"] == "transcode":
                task["name"] = "HandBrakeCLI"
    variant, _ = compile_fixture(rewrite(tmp_path, base_path, rename),
                                 library, "single")

    base_arrivals, variant_arrivals = arrivals_by_id(base), arrivals_by_id(variant)
    assert set(base_arrivals) == set(variant_arrivals)
    for task_id in base_arrivals:
        if task_id == "transcode":
            assert variant_arrivals[task_id]["name"] == "HandBrakeCLI"
            trimmed = {**variant_arrivals[task_id], "name": "ffmpeg"}
            assert trimmed == base_arrivals[task_id]
        else:
            assert variant_arrivals[task_id] == base_arrivals[task_id]
    assert wakes(variant) == wakes(base)
    assert variant["ground_truth"] == base["ground_truth"]


def test_single_is_the_only_mode(fixture_path, library):
    """9.5 spec decision 14 (9.13): the dataset ships the single-lane set only; the native mode is gone."""
    assert MODES == ("single",)
    with pytest.raises(ValueError, match="mode must be one of"):
        compile_fixture(fixture_path("fx-mixed.timeline.yaml"), library, "native")


def test_lane_scaling_lands_chain_on_lane_share(fixture_path, library):
    """The lane-scaling pass: the chain's aggregate demand per frame is lane_share of the lane."""
    single, _ = compile_fixture(fixture_path("fx-game.timeline.yaml"), library, "single")
    single_run_total = 0
    frame = None
    for event in arrivals_by_id(single).values():
        for op in event["program"][0]["body"]:
            if op["op"] == "RUN":
                single_run_total += op["us"]
            if op["op"] == "TIMER":
                frame = op["period_us"]
    assert abs(single_run_total / frame - 0.6) < 0.01


def test_chain_population(fixture_path, library):
    canonical, _ = compile_fixture(fixture_path("fx-game.timeline.yaml"),
                                   library, "single")
    arrivals = arrivals_by_id(canonical)
    chain = [i for i in arrivals if ".chain." in i]
    wine = [i for i in arrivals if i.endswith(".wineserver")]
    assert len(chain) == 16 and len(wine) == 1 and len(arrivals) == 17  # no tail
    names = [arrivals[i]["name"] for i in sorted(chain, key=lambda i: int(i.rsplit(".", 1)[1]))]
    assert names == ["Troy.exe", "Task worker thr", "Task worker thr", "Task worker thr", "Task worker thr",
                     "dxvk-cs", "dxvk-submit", "winepulse_mainl", "winepulse_timer", "FAudio_AudioCli"] + \
        ["Troy.exe"] * 6   # 9.10 D26: the head is the task's name, the members the bound member_names
    assert arrivals[wine[0]]["name"] == "wineserver"
    # wake order: head -> wineserver -> chain.2
    head_body = arrivals[f"{chain[0].rsplit('.', 2)[0]}.chain.1"]["program"][0]["body"]
    assert head_body[-1] == {"op": "WAKE", "target": wine[0]}
    wine_body = arrivals[wine[0]]["program"][0]["body"]
    assert wine_body[-1]["op"] == "WAKE" and wine_body[-1]["target"].endswith(".chain.2")
