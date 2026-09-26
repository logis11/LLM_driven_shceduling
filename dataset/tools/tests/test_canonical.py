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


def test_orchestrator_spawn_table_is_six_member_object_jobs(fixture_path, library):
    # D19: one object job = six spawn-table entries, forked together, woken in D2's parent-child order
    _, canonical, _ = compiled(fixture_path, library, "fx-mixed.timeline.yaml")
    build = next(e for e in canonical["events"]
                 if e["op"] == "arrive" and e["id"] == "build")
    assert build["fork_cap"] == 12                 # parallelism_cap 2 x the job's six members
    table = build["spawn_table"]
    assert len(table) == 36                        # 6 object jobs x 6 members
    assert len({s["id"] for s in table}) == 36
    assert sum(1 for i in build["program"] if i["op"] == "FORK") == 36
    assert [s["name"] for s in table[:6]] == ["sh", "gcc", "cc1", "as", "fixdep", "rm"]
    job = {s["name"]: s for s in table[:6]}
    assert [op["op"] for op in job["sh"]["program"]] == [
        "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "RUN",
        "WAKE", "WAKE", "WAKE", "WAKE", "WAKE", "EXIT"]      # four steps, then it releases the five it held
    assert [op["op"] for op in job["gcc"]["program"]] == [
        "WAIT", "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "EXIT"]
    assert [op["op"] for op in job["cc1"]["program"]] == ["WAIT", "RUN", "WAKE", "WAIT", "EXIT"]
    assert job["sh"]["program"][1]["target"] == job["gcc"]["id"]    # sh wakes gcc first (D2's order)
    assert job["gcc"]["program"][2]["target"] == job["cc1"]["id"]   # gcc wakes cc1, then as, then sh
    assert job["cc1"]["program"][0]["channel"] == f"job:{job['cc1']['id']}"
    cc1_us = job["cc1"]["program"][1]["us"]
    assert 6_414 <= cc1_us <= 4_005_164                            # inside its table's support, p1 to p99.9
    others = sum(op["us"] for name, s in job.items() if name != "cc1"
                 for op in s["program"] if op["op"] == "RUN")
    assert cc1_us > 10 * others                                    # cc1 carries the job's CPU (D2, D20)
    assert all(s["program"][-1] == {"op": "EXIT"} for s in table)
    assert "depart" not in build  # finite: ends via EXIT at an emergent time


def test_count_expansion(fixture_path, library):
    _, canonical, _ = compiled(fixture_path, library, "fx-mixed.timeline.yaml")
    renderers = [e for e in canonical["events"] if e["op"] == "arrive"
                 and e["id"].startswith("renderers.")]
    assert len(renderers) == 3
    assert all(e["name"] == "chrome" for e in renderers)
    # a measured archetype compiles to an explicit event stream per instance (9.5 D9): each instance draws its own —
    # its timer wakes are wake events on its own timer channel (D74), its runs in its program
    streams = {(tuple(i.get("us") for i in event["program"]),
                tuple(w["t"] for w in canonical["events"] if w["op"] == "wake" and w["target"] == event["id"]))
               for event in renderers}
    assert len(streams) == 3  # per-instance draws differ across the expansion


def test_focus_wakes_inside_windows(fixture_path, library):
    timeline, canonical, _ = compiled(fixture_path, library,
                                      "fx-mixed.timeline.yaml")
    wake_events = [e for e in canonical["events"] if e["op"] == "wake" and e["target"] == "editor"]
    inputs = [e for e in wake_events if e["channel"] == "input:editor"]
    assert inputs, "focused interactive task must receive input wakes"
    windows = [(w["from"], w["to"]) for w in timeline.focus]
    for event in inputs:
        assert any(lo <= event["t"] < hi for lo, hi in windows)
    # every other wake is a timer wake on the task's own timer channel (9.5 D74)
    assert {e["channel"] for e in wake_events} <= {"input:editor", "timer:editor"}
    editor = next(e for e in canonical["events"]
                  if e["op"] == "arrive" and e["id"] == "editor")
    waits = [i for i in editor["program"] if i["op"] == "WAIT"]
    assert len(waits) == len(wake_events)  # one WAIT per wake, input or timer


def test_demand_estimate(fixture_path, library):
    _, _, report = compiled(fixture_path, library, "fx-oversub.timeline.yaml")
    # cpu-batch 66s/60s = 1.10 + the measured audio-player's mean duty (9.5 D19: mpv audio ≈ 0.0076)
    assert abs(report["utilization"] - 1.1076) < 0.005


def test_familiarity_annotation_carried_into_ground_truth(fixture_path, library,
                                                          schema):
    # authored on the segment -> present in ground_truth, and schema-clean
    _, canonical, report = compiled(fixture_path, library,
                                    "fx-mixed.timeline.yaml")
    assert canonical["ground_truth"][0]["familiarity"] == 3
    assert lint_canonical(canonical, schema, report=report, mode="single") == []
    # not authored -> the key is absent, never null or derived
    _, canonical, _ = compiled(fixture_path, library, "fx-game.timeline.yaml")
    assert all("familiarity" not in s for s in canonical["ground_truth"])


def test_cpu_batch_runs_and_blocks_until_total_work(fixture_path, library):
    # D21, D22, D25: RUN from the bound program's runs between voluntary blocks, then the block that followed it
    _, canonical, _ = compiled(fixture_path, library, "fx-oversub.timeline.yaml")
    task = next(e for e in canonical["events"]
                if e["op"] == "arrive" and e["id"] == "train")
    ops = [op["op"] for op in task["program"]]
    assert ops[-1] == "EXIT" and ops.count("RUN") > 1      # a loop, not one uninterrupted RUN
    assert set(ops) == {"RUN", "SLEEP", "EXIT"}
    assert sum(op["us"] for op in task["program"] if op["op"] == "RUN") == 66_000_000
    assert all(op["us"] >= 1 for op in task["program"] if op["op"] in ("RUN", "SLEEP"))


def test_zero_inclusive_block_table_leaves_the_program_running(library):
    # D25: HandBrakeCLI's block table is zero up to p99.9 — 0.08 % of its runs end in a block, so the task runs on
    # through almost every run and those runs join one RUN; the table's top interval carries the rare blocks it
    # measured (9.5 D71: about two in the ~1,840 runs of 2 s), and the CPU still sums to total_work
    from wlc import compiler
    build = compiler._TaskBuild("batch", "HandBrakeCLI")
    params = library.entry("cpu-batch")["params"]
    compiler._batch_loop(build, params, {"bind": {"program": "handbrakecli", "total_work": "2s"}}, "seed", "batch")
    ops = [op["op"] for op in build.program]
    assert ops[-1] == "EXIT" and ops.count("RUN") == ops.count("SLEEP") + 1 and ops.count("SLEEP") <= 10
    assert sum(op["us"] for op in build.program if op["op"] == "RUN") == 2_000_000 == build.demand_us
    build = compiler._TaskBuild("hog", "python3")
    compiler._batch_loop(build, params, {"bind": {"program": "python3", "total_work": "2s"}}, "seed", "hog")
    assert "SLEEP" in {op["op"] for op in build.program}          # python3 blocks after every run
    assert sum(op["us"] for op in build.program if op["op"] == "RUN") == 2_000_000


def test_a_single_table_set_batch_loop_needs_no_program_binding(library):
    # 9.7 D29: file-backup, file-archiver and game-download each carry one table set, taken without a `program` binding;
    # cpu-batch, with five, still needs one
    import pytest
    from wlc import compiler
    build = compiler._TaskBuild("backup", "borg")
    compiler._batch_loop(build, library.entry("file-backup")["params"], {"bind": {"total_work": "2s"}}, "seed", "backup")
    assert "SLEEP" in {op["op"] for op in build.program}          # borg blocks after almost every run
    assert sum(op["us"] for op in build.program if op["op"] == "RUN") == 2_000_000 == build.demand_us
    build = compiler._TaskBuild("archive", "7z")
    compiler._batch_loop(build, library.entry("file-archiver")["params"], {"bind": {"total_work": "2s"}}, "seed", "archive")
    assert [op["op"] for op in build.program] == ["RUN", "EXIT"]  # 7-Zip's block is zero at every quantile
    with pytest.raises(ValueError):
        compiler._batch_loop(compiler._TaskBuild("x", "x"), library.entry("cpu-batch")["params"],
                             {"bind": {"total_work": "2s"}}, "seed", "x")
