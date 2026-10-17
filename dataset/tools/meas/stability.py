"""The stability criterion shared by the campaigns (9.6 changelog D10, D11; 9.5 changelog D26).

The pool of same-machine repeats is stable when the 95 % confidence half-width of each carried value, relative to it,
is at most TOLERANCE (t multiplier, k − 1 degrees of freedom). A rate or share is tested by its per-repeat values
(`stability`); a table's mean — gaps, runs, per-input runs, durations — as the table carries it, count-weighted over
the repeats, its half-width the ratio estimator's over them (`ratio_stability`, cochran-st77). Repeats are added one
at a time until it holds; every same-machine repeat obtained is pooled and reported.
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


def _pairs(sums, counts):
    """(sum, count) per repeat, from two lists or two dicts keyed by repeat; a repeat without the value (None count)
    is not one of its repeats, a repeat with no samples (count 0) is."""
    if isinstance(counts, dict):
        return [((sums.get(r) or 0.0), counts[r]) for r in counts if counts[r] is not None]
    return [((y or 0.0), x) for y, x in zip(sums, counts) if x is not None]


def _linearised_sd(pairs, ratio):
    """The spread of the per-repeat values the ratio's variance is read from: d = (y − R x) / x̄, whose sum is zero, so
    its sample standard deviation is √(Σd² / (k − 1)) — cochran-st77 (6.13) is s_d² / k with f = 0."""
    k = len(pairs)
    xbar = sum(x for _, x in pairs) / k
    return math.sqrt(sum(((y - ratio * x) / xbar) ** 2 for y, x in pairs) / (k - 1))


def ratio_stability(sums, counts, abs_floor=None, min_k=None):
    """The half-width of a table's mean as the table carries it: every repeat's samples pooled, so its mean is Σy / Σx
    over the per-repeat sums y and counts x — a ratio estimate, each repeat a cluster of samples (cochran-st77 §9A.1,
    its mean per element). The variance is cochran-st77 (6.13) with f = 0, the repeats drawn from an unbounded
    population of jobs, and the interval Student's t with k − 1 degrees of freedom in place of its z (the project's).
    A repeat with no samples counts toward k and adds its sum alone: a sparse component's gap span with no wake. The
    fields, the floor and the minimum are `stability`'s; cv is the linearised values' spread relative to the ratio."""
    pairs = _pairs(sums, counts)
    k, total_y, total_x = len(pairs), sum(y for y, _ in pairs), sum(x for _, x in pairs)
    ratio = total_y / total_x if total_x else None
    if k < 2 or not total_x:
        return {"k": k, "mean": None if ratio is None else round(ratio, 4), "cv": None, "half_width": None,
                "half_width_abs": None, "leave_one_out": None, "passes": False}
    sd = _linearised_sd(pairs, ratio)
    hw_abs = t975(k) * sd / (k ** 0.5)
    if ratio == 0:
        ok = abs_floor is not None and hw_abs <= abs_floor and (min_k is None or k >= min_k)
        return {"k": k, "mean": 0.0, "cv": None, "half_width": None, "half_width_abs": round(hw_abs, 4),
                "leave_one_out": None, "passes": ok}
    loo = max((abs((total_y - y) / (total_x - x) - ratio) / ratio for y, x in pairs if total_x - x), default=None)
    hw = hw_abs / ratio
    ok = hw <= TOLERANCE if abs_floor is None else hw_abs <= max(TOLERANCE * ratio, abs_floor)
    if min_k is not None and k < min_k:
        ok = False
    return {"k": k, "mean": round(ratio, 4), "cv": round(sd / ratio, 4), "half_width": round(hw, 4),
            "half_width_abs": round(hw_abs, 4), "leave_one_out": None if loo is None else round(loo, 4), "passes": ok}


def ratio_repeats_needed(sums, counts, abs_floor=None, min_k=None):
    """The smallest repeat count, at least min_k, at which `ratio_stability`'s half-width at the linearised spread of
    the given repeats is within the tolerance; None past 200."""
    pairs = _pairs(sums, counts)
    total_x = sum(x for _, x in pairs)
    if len(pairs) < 2 or not total_x:
        return None
    ratio = sum(y for y, _ in pairs) / total_x
    sd = _linearised_sd(pairs, ratio)
    bound = max(TOLERANCE * ratio, abs_floor or 0.0)
    for k in range(max(2, min_k or 2), 201):
        if t975(k) * sd / k ** 0.5 <= bound:
            return k
    return None
