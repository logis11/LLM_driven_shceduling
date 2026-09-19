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
