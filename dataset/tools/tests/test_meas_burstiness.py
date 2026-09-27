"""The compiled streams' burstiness against the measured (9.15's threat statement, from the 2026-09-26 review of
9.5–9.9): each carried repeat's wake stream and a compile of its archetype's components over the same span, read by
the dispersion of their wake counts per bin."""

import pytest

from meas import burstiness
from meas.distribution import quantile_table


def _burst_times():
    # ten bursts, one per 10 ms, each ten wakes 50 µs apart inside the burst's first millisecond
    return [k * 0.01 + j * 0.00005 for k in range(10) for j in range(10)]


def test_the_dispersion_is_the_variance_over_the_mean_of_the_counts_per_bin():
    # 1 ms bins over 4 ms: counts 2, 1, 0, 1 — mean 1, variance 0.5
    assert burstiness.dispersion([0.0005, 0.0006, 0.0015, 0.0035], 0.004, 0.001) == pytest.approx(0.5)
    # ten wakes in each of ten bins of 100: mean 1, variance (10 × 81 + 90 × 1) / 100 = 9
    assert burstiness.dispersion(_burst_times(), 0.1, 0.001) == pytest.approx(9.0)
    # every 10 ms bin holds one whole burst: no spread
    assert burstiness.dispersion(_burst_times(), 0.1, 0.01) == pytest.approx(0.0)


def test_only_whole_bins_are_read_and_a_span_with_none_reads_nothing():
    # 2.5 ms: two whole 1 ms bins (counts 1, 1); the wake in the part bin is not counted
    assert burstiness.dispersion([0.0005, 0.0015, 0.0022], 0.0025, 0.001) == pytest.approx(0.0)
    assert burstiness.dispersion(_burst_times(), 0.1, 1.0) is None
    assert burstiness.dispersion([], 0.1, 0.001) is None


def test_the_compiled_stream_is_the_archetype_s_components_over_the_repeat_s_span():
    gap = {"dist": "quantiles", **quantile_table([1000.0] * 50)}   # every gap 1 ms, in µs
    run = {"dist": "quantiles", **quantile_table([10.0] * 50)}
    times = burstiness.compiled_times([{"comm": "a", "gap": gap, "run": run}], 0.1, seed=3)
    assert times == sorted(times) and all(0 <= t < 0.1 for t in times)
    assert len(times) in (99, 100)
    assert all(b - a == pytest.approx(0.001) for a, b in zip(times, times[1:]))


def test_an_entry_is_read_per_repeat_measured_over_compiled():
    pairs = [k * 0.002 + j * 0.0001 for k in range(50) for j in range(2)]   # two wakes in every other 1 ms bin
    measured = {1: (0.1, _burst_times()), 2: (0.1, _burst_times())}
    compiled = {1: (0.1, pairs), 2: (0.1, _burst_times())}
    out = burstiness.read_entry(measured, compiled)
    assert out["repeats"] == 2
    one = out["bins"]["1 ms"]
    # repeat 1: 9 against 1 (pairs: mean 1, variance 1); repeat 2: 9 against 9
    assert one["measured"] == {"median": 9.0, "min": 9.0, "max": 9.0}
    assert one["compiled"] == {"median": 5.0, "min": 1.0, "max": 9.0}
    assert one["ratio"] == {"median": 5.0, "min": 1.0, "max": 9.0}
    # at 10 ms both have no spread, so there is no ratio to read
    assert out["bins"]["10 ms"]["ratio"] is None
    assert out["wakes_per_s"] == {"measured": 1000.0, "compiled": 1000.0}


def test_a_repeat_s_artifact_is_found_by_its_run_and_repeat(tmp_path):
    kept = tmp_path / "interactive-code-from566" / "36126154552" / "meas-interactive-code-r42-full"
    other = tmp_path / "interactive-code-from566-excluded" / "36126168885" / "meas-interactive-code-r42-full"
    for d in (kept, other):
        d.mkdir(parents=True)
    assert burstiness.artifact_dir(str(tmp_path), "code", 42, "36126154552") == str(kept)
    with pytest.raises(SystemExit):
        burstiness.artifact_dir(str(tmp_path), "code", 43, "36126154552")


def test_a_renderer_entry_reads_each_renderer_as_one_stream():
    # the archetype is one renderer (9.8 D14): each renderer measured in a repeat is one stream beside the compile of one
    from collections import namedtuple
    Row = namedtuple("Row", "pid t_in")
    rows = [Row(20, 100.5), Row(30, 100.2), Row(20, 100.1), Row(30, 101.0)]
    assert burstiness.renderer_streams(rows, 100.0) == {20: [pytest.approx(0.1), pytest.approx(0.5)],
                                                        30: [pytest.approx(0.2), pytest.approx(1.0)]}


def test_the_page_carries_each_entry_s_ratios_by_bin():
    rep = {"archetype": "code-editor", "app": "code", "phase": "idle", "repeats": 2,
           "wakes_per_s": {"measured": 112.6, "compiled": 114.6},
           "bins": {w: {"measured": {"median": 11.0, "min": 10.0, "max": 12.0},
                        "compiled": {"median": 3.0, "min": 2.9, "max": 3.1},
                        "ratio": {"median": 3.67, "min": 3.2, "max": 4.1}} for w in burstiness.BINS}}
    md = burstiness.render({"family": "campaign", "archetypes": {"code-editor": rep}})
    assert "## code-editor (`code`, idle)" in md
    assert "| 10 ms | 11 (10–12) | 3 (2.9–3.1) | 3.67 (3.2–4.1) |" in md.splitlines()
