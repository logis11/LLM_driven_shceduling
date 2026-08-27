"""The task-2.3 spec's invariant charter: determinism, keyed isolation,
one-entry diffs, and the -native/-single scalable-fields-only rule."""

import yaml

from wlc import Timeline, compile_timeline
from wlc.compiler import canonical_bytes


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
        {"id": "extra", "name": "sleepd", "archetype": "system-daemon",
         "arrive": "0s", "depart": "60s"}))
    extended, _ = compile_fixture(extended_path, library, "single")

    base_arrivals, new_arrivals = arrivals_by_id(base), arrivals_by_id(extended)
    assert set(new_arrivals) == set(base_arrivals) | {"extra"}
    for task_id, event in base_arrivals.items():
        assert new_arrivals[task_id] == event
    assert wakes(extended) == wakes(base)


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


def test_modes_identical_without_scalable_archetypes(fixture_path, library):
    path = fixture_path("fx-mixed.timeline.yaml")
    native, _ = compile_fixture(path, library, "native")
    single, _ = compile_fixture(path, library, "single")
    assert canonical_bytes(native) == canonical_bytes(single)


def test_lane_scaling_touches_only_chain_runs(fixture_path, library):
    path = fixture_path("fx-game.timeline.yaml")
    native, _ = compile_fixture(path, library, "native")
    single, _ = compile_fixture(path, library, "single")

    native_arrivals, single_arrivals = arrivals_by_id(native), arrivals_by_id(single)
    assert set(native_arrivals) == set(single_arrivals)
    single_run_total = 0
    frame = None
    for task_id, native_event in native_arrivals.items():
        single_event = single_arrivals[task_id]
        if ".tail." in task_id:
            assert single_event == native_event
            continue
        body_native = native_event["program"][0]["body"]
        body_single = single_event["program"][0]["body"]
        assert len(body_native) == len(body_single)
        for op_native, op_single in zip(body_native, body_single):
            if op_native["op"] == "RUN":
                single_run_total += op_single["us"]
            else:
                assert op_native == op_single  # only RUN values may differ
            if op_native["op"] == "TIMER":
                frame = op_native["period_us"]
    # the chain's aggregate demand per frame lands on lane_share of the lane
    assert abs(single_run_total / frame - 0.6) < 0.01


def test_chain_population(fixture_path, library):
    canonical, _ = compile_fixture(fixture_path("fx-game.timeline.yaml"),
                                   library, "single")
    arrivals = arrivals_by_id(canonical)
    chain = [i for i in arrivals if ".chain." in i]
    tail = [i for i in arrivals if ".tail." in i]
    assert len(chain) == 16 and len(chain) + len(tail) == 300
    assert all(arrivals[i]["name"] == "game.exe" for i in arrivals)
