"""The stability criterion shared by the campaigns (9.6 changelog D10, D11; 9.5 changelog D26).

The pool of same-machine repeats is stable when the 95 % confidence half-width of the across-repeat mean of a
carried median (t multiplier, k − 1 degrees of freedom), relative to the mean, is at most TOLERANCE. Repeats are
added one at a time until it holds; every same-machine repeat obtained is pooled and reported.
"""

import functools
import math
import statistics

TOLERANCE = 0.05


def _within(t, nu):
    """P(|T| <= t) for Student's t with nu (a positive integer) degrees of freedom: the closed form of its
    distribution function as a finite sum in theta = atan(t / sqrt(nu))."""
    th = math.atan(t / math.sqrt(nu))
    c2 = math.cos(th) ** 2
    term, total = 1.0, 1.0
    if nu % 2:
        for j in range(1, (nu - 1) // 2):
            term *= c2 * (2 * j) / (2 * j + 1)
            total += term
        return 2 / math.pi * (th + (math.sin(th) * math.cos(th) * total if nu > 1 else 0.0))
    for j in range(1, nu // 2):
        term *= c2 * (2 * j - 1) / (2 * j)
        total += term
    return math.sin(th) * total


@functools.lru_cache(maxsize=None)
def t975(k):
    """The 97.5 % point of Student's t with k - 1 degrees of freedom, to three decimals as printed tables give it:
    the multiplier of a 95 % two-sided interval over k repeats."""
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _within(mid, k - 1) < 0.95 else (lo, mid)
    return round((lo + hi) / 2, 3)


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
    hw_abs = t975(k) * sd / (k ** 0.5)
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
