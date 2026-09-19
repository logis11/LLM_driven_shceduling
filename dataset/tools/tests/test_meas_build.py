"""The 9.6 build campaign's carried quantities (changelog D16, D19–D24)."""

import pytest

from meas import stability as stab


def test_stability_default_is_unchanged():
    r = stab.stability({4: 360.0, 5: 372.0, 7: 365.0, 8: 369.0})
    assert r["k"] == 4 and r["passes"] is True
    assert r["half_width"] == pytest.approx(3.182 * 27 ** 0.5 / 2 / 366.5, abs=1e-4)
    assert "half_width_abs" in r


def test_abs_floor_passes_medians_at_the_trace_resolution():
    vals = [7.0, 7.0, 6.0, 6.0]          # µs: a one-step flip is 14 % of the mean
    assert stab.stability(vals)["passes"] is False
    r = stab.stability(vals, abs_floor=1.0)
    assert r["half_width_abs"] == pytest.approx(0.9186, abs=1e-3) and r["passes"] is True


def test_min_k_holds_the_criterion_back_below_five_repeats():
    vals = [100.0, 101.0, 100.5, 100.2]
    assert stab.stability(vals)["passes"] is True
    assert stab.stability(vals, min_k=5)["passes"] is False
    assert stab.stability(vals + [100.4], min_k=5)["passes"] is True


from meas.build import analyze as build  # noqa: E402
from meas.build import shapes  # noqa: E402


def seg(t_in, run_ms, tid, state, delay_ms=0.0):
    return build.Seg(t_in, t_in - delay_ms / 1000, t_in + run_ms / 1000, run_ms, "p", tid, 1, state, 3)


def test_runs_between_blocks_sum_across_preemptions_and_end_at_exit():
    rows = [seg(1.000, 4.0, 7, "R"), seg(1.005, 1.0, 8, "S"), seg(1.010, 3.0, 7, "S"),
            seg(1.020, 2.0, 7, "D"), seg(1.030, 5.0, 7, "Z")]
    assert sorted(shapes.runs_between_blocks(rows)) == pytest.approx([1.0, 2.0, 5.0, 7.0])


def test_share_past_slice():
    assert shapes.share_past_slice([12.0, 8.0, 30.0], 10.0) == pytest.approx(22.0 / 50.0)
    assert shapes.share_past_slice([]) is None


def test_program_gaps_count_runnable_time_as_busy():
    rows = [build.Seg(1.000, 1.000, 1.004, 4.0, "p", 7, 1, "S", 3),
            build.Seg(1.004, 1.003, 1.006, 2.0, "p", 8, 1, "R", 3),    # preempted at 1.006
            build.Seg(1.009, 1.009, 1.010, 1.0, "p", 8, 1, "S", 3),    # back at 1.009 with no reported delay
            build.Seg(1.015, 1.015, 1.016, 1.0, "p", 7, 1, "Z", 3)]
    assert shapes.program_gaps(rows, 1.000, 1.016) == pytest.approx([5.0])
    assert shapes.program_gaps(rows, 1.000, 1.020) == pytest.approx([5.0, 4.0])
