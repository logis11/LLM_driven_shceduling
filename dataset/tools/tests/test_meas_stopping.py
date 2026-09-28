"""The stability rule's stopping simulated at an observed spread (9.5 D88)."""
import random

import pytest

from meas import stopping


def test_the_rule_stops_at_the_first_count_from_five_whose_half_width_is_within_the_tolerance():
    seq = [1.0, 1.2, 0.8, 1.1, 0.9] + [1.0] * 100
    it = iter(seq)
    k, mean, hw = stopping.stop(lambda: next(it), kmin=5, tol=0.05)
    first = next(n for n in range(5, len(seq) + 1) if stopping.half_width(seq[:n]) <= 0.05 * sum(seq[:n]) / n)
    assert k == first and k > 5 and hw <= 0.05 * mean


def test_the_widest_value_leaves_out_values_at_a_window_limit_or_carried_under_an_exception():
    q = {"a": {"half_width": 0.03, "k": 9, "cv": 0.05}, "b": {"half_width": 0.049, "k": 9, "cv": 0.08, "limited": True},
         "c": {"half_width": 0.06, "k": 9, "cv": 0.1, "carried": True}, "d": {"half_width": 0.04, "k": 9, "cv": 0.07}}
    assert stopping.widest(q)[0] == "d"
    assert stopping.widest(q, phases=("a",))[0] == "a"


def test_at_the_line_the_stated_interval_covers_less_than_its_nominal_95_percent():
    r = stopping.simulate(0.10, 1500, lognormal=False, rng=random.Random(3))
    assert 0.85 < r["coverage"] < 0.95 and abs(r["mean_bias"]) < 0.01


def test_every_caveat_the_fold_in_states_carries_the_record_s_figures(repo_root):
    import json
    from meas.campaign import fold_in
    rec = json.load(open(repo_root / "_dev" / "research" / "jioh" / "task-9.5-interactive-typing" / "campaign"
                         / "results-stopping" / "stopping.json"))
    near = {e["archetype"] for e in rec["entries"] if e["widest"]["half_width"] >= stopping.NEAR}
    assert set(fold_in.STOPPING_STATED) == near
    for e in rec["entries"]:
        if e["archetype"] in near:
            text = fold_in.STOPPING_STATED[e["archetype"]]
            lo, hi = stopping.coverage_range(e)
            assert f"{lo * 100:.0f}–{hi * 100:.0f} %" in text or f"{lo * 100:.0f} %" in text, e["archetype"]
