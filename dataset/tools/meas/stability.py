"""The stability criterion shared by the campaigns (9.6 changelog D10, D11; 9.5 changelog D26).

The pool of same-machine repeats is stable when the 95 % confidence half-width of the across-repeat mean of a
carried median (t multiplier, k − 1 degrees of freedom), relative to the mean, is at most TOLERANCE. Repeats are
added one at a time until it holds; every same-machine repeat obtained is pooled and reported.
"""

import statistics

T975 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262,
        11: 2.228, 12: 2.201, 13: 2.179, 14: 2.160, 15: 2.145, 16: 2.131, 17: 2.120, 18: 2.110, 19: 2.101, 20: 2.093}
TOLERANCE = 0.05


def stability(values_by_repeat, abs_floor=None, min_k=None, keep_zero=False):
    """The half-width of one carried median over its repeats (a dict keyed by repeat, or a list), and the largest
    shift of the mean when any one repeat is dropped. abs_floor (in the values' unit): the tolerance is the larger of
    TOLERANCE × mean and abs_floor, the instrument's resolution (9.6 changelog D23: the trace's 1 µs). min_k: the
    criterion holds only over at least that many repeats (9.6 changelog D24; kalibera-ismm13 §11). keep_zero: a zero
    is a repeat's value, not a missing repeat (9.5 changelog D30: a component absent from a repeat wakes 0 times a
    second; a median at the zero bound, D13); a zero mean is then judged on abs_floor alone. Without them the rule is
    the one 9.5 D26 and 9.6 D11 stated."""
    vals = values_by_repeat.values() if isinstance(values_by_repeat, dict) else values_by_repeat
    v = [x for x in vals if x is not None] if keep_zero else [x for x in vals if x]
    k = len(v)
    if k < 2:
        return {"k": k, "mean": v[0] if v else None, "cv": None, "half_width": None, "half_width_abs": None,
                "leave_one_out": None, "passes": False}
    m, sd = statistics.fmean(v), statistics.stdev(v)
    hw_abs = T975.get(k, T975[20]) * sd / (k ** 0.5)
    if m == 0:  # only under keep_zero: every repeat at zero
        ok = abs_floor is not None and hw_abs <= abs_floor
        if min_k is not None and k < min_k:
            ok = False
        return {"k": k, "mean": 0.0, "cv": None, "half_width": None, "half_width_abs": round(hw_abs, 4),
                "leave_one_out": None, "passes": ok}
    hw = hw_abs / m
    loo = max(abs(statistics.fmean(v[:i] + v[i + 1:]) - m) / m for i in range(k))
    ok = hw <= TOLERANCE if abs_floor is None else hw_abs <= max(TOLERANCE * m, abs_floor)
    if min_k is not None and k < min_k:
        ok = False
    return {"k": k, "mean": round(m, 4), "cv": round(sd / m, 4), "half_width": round(hw, 4),
            "half_width_abs": round(hw_abs, 4), "leave_one_out": round(loo, 4), "passes": ok}
