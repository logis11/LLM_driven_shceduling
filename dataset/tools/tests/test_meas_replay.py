"""Constructed cases for the replay streams' extraction (9.14 decision 12; dataset/tools/meas/replay_fold_in.py):
one pooled repeat per entry over its carried phase, as a `wakes`, `cycles` or `runs` stream."""

from meas import replay_fold_in as rf
from meas.build import shapes
from meas.build.analyze import Seg
from meas.campaign import pool
from meas.campaign.analyze import Row


def test_a_wake_stream_is_the_merged_wakes_from_the_phase_start_with_components_indexed():
    rows = [Row(99.9, 99.8999, 99.9005, 0.5, "code", 11, 1, "S"),            # before the start: dropped
            Row(100.5, 100.4999, 100.5015, 1.5, "code", 11, 1, "S"),
            Row(101.25, 101.2499, 101.25025, 0.25, "Compositor", 22, 2, "S"),
            Row(101.5, 101.4999, 101.5010, 1.0, "code", 11, 1, "S"),
            Row(120.0, 119.9999, 120.0005, 0.5, "code", 11, 1, "S")]          # at the end: dropped
    comms = []
    stream = rf.wake_stream(rows, 100.0, 120.0, {1: "main", 2: "renderer"}, comms)
    assert stream == [[500_000, 1500, 0], [1_250_000, 250, 1], [1_500_000, 1000, 0]]
    assert comms == ["code", "renderer/Compositor"]
    # a second stream of the repeat shares the comm index
    more = rf.wake_stream([Row(102.0, 101.9999, 102.001, 1.0, "Compositor", 33, 3, "S")], 100.0, 120.0,
                          {3: "renderer"}, comms)
    assert more == [[2_000_000, 1000, 1]] and comms == ["code", "renderer/Compositor"]


def test_a_cycle_stream_is_the_pools_cycles_as_start_work_and_length():
    roles = {5: "utility", 6: "main"}
    ref = [Row(t, t, t + 0.00005, 0.05, "AudioWorkerThre", 50, 5, "S") for t in (1.000, 1.010, 1.020)]
    work = [Row(1.001, 1.001, 1.0013, 0.3, "chrome", 60, 6, "S"), Row(1.012, 1.012, 1.0124, 0.4, "chrome", 60, 6, "S"),
            Row(1.015, 1.015, 1.0151, 0.1, "chrome", 61, 6, "S"), Row(1.025, 1.025, 1.0252, 0.2, "chrome", 60, 6, "S")]
    rows = sorted(ref + work, key=lambda r: r.t_in)
    stream = rf.cycle_stream("webrtc", "play", rows, rows, roles, 1.0)
    assert stream == [[0, 350, 10_000], [10_000, 550, 10_000]]   # the last start closes no cycle
    windows = pool.cycle_windows("webrtc", "play", rows, rows, roles)
    assert [w for _, w, _ in stream] == [round(w * 1000) for w in windows["work_ms"]]
    assert [n for _, _, n in stream] == [round(n * 1000) for n in windows["length_ms"]]


def test_a_run_stream_is_the_runs_between_voluntary_blocks_with_the_block_after_each():
    a = Seg(0.000, 0.000, 0.003, 3.0, "python", 1, 1, "S", 3)
    b = Seg(0.004, 0.004, 0.006, 2.0, "python", 1, 1, "R", 3)   # preempted: its run continues in c
    c = Seg(0.007, 0.007, 0.011, 4.0, "python", 1, 1, "S", 3)
    d = Seg(0.012, 0.012, 0.013, 1.0, "python", 1, 1, "R", 3)   # the thread's last run, no voluntary end
    assert rf.run_stream([a, b, c, d]) == [[0, 3000, 1000], [4000, 6000, 1000], [12_000, 1000, 0]]
    rows = [a, b, c, d]
    assert [r for _, r, _ in rf.run_stream(rows)] == [round(x * 1000) for x in shapes.runs_between_blocks(rows)]
    assert [k for _, _, k in rf.run_stream(rows)][:2] == [round(x * 1000) for x in shapes.blocks_after_runs(rows, 0.0, 0.013)]


def test_a_run_stream_of_two_threads_is_in_sched_out_order_and_a_runnable_sibling_makes_a_zero_block():
    t1a = Seg(0.000, 0.000, 0.001, 1.0, "a", 1, 1, "S", 3)
    t2a = Seg(0.001, 0.0005, 0.003, 2.0, "b", 2, 1, "S", 3)   # runnable from 0.5 ms: t1a's block is zero
    t1b = Seg(0.003, 0.002, 0.004, 1.0, "a", 1, 1, "S", 3)
    assert rf.run_stream([t1a, t2a, t1b]) == [[0, 1000, 0], [1000, 2000, 0], [3000, 1000, 0]]


def test_the_document_carries_the_landing_and_encodes_byte_stable():
    spec = rf.SOURCES["code-editor"]
    doc = rf.document("code-editor", spec, [[[0, 1, 0]]], ["code"], 700_000_000)
    assert doc["entry"] == "code-editor" and doc["kind"] == "wakes" and doc["program"] is None
    assert doc["source"] == "meas-ci:interactive:2026-09-25" and doc["release"] == "meas-ci-2026-09-25"
    assert doc["landing"].endswith("meas-interactive-code-r1-full") and doc["phase"] == "idle"
    assert doc["read_from_s"] == 200.0
    rep = doc["repeats"][0]
    assert rep["phase_us"] == 700_000_000 and rep["comms"] == ["code"] and rep["streams"] == [[[0, 1, 0]]]
    assert rf.encode(doc) == rf.encode(dict(reversed(list(doc.items()))))
    assert rf.SOURCES["cpu-batch"]["program"] == "python3" and rf.SOURCES["cpu-batch"]["repeat"] == "6"
    assert {s["kind"] for s in rf.SOURCES.values()} == {"wakes", "cycles", "runs"}
    assert set(rf.SOURCES) == {"code-editor", "web-browser", "renderer-hidden", "video-call", "package-upgrade", "cpu-batch"}
