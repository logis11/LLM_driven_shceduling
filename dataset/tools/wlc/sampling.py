"""Keyed sampling substreams (task-2.3 spec §5).

Every draw is addressed by (seed, *key, index) through SHA-256 — never a
global draw sequence — so an edit to one task can never shift another
task's draws, and C2 byte-identity holds by construction. All math is
pure-Python and platform-deterministic.
"""

import hashlib
import math
from statistics import NormalDist

_NORMAL = NormalDist()
_EPS = 2**-53


def uniform(seed, *key):
    """Deterministic U(0,1) for a fully qualified key."""
    material = "|".join([str(seed), *map(str, key)]).encode()
    digest = hashlib.sha256(material).digest()
    u = int.from_bytes(digest[:8], "big") / 2**64
    return min(max(u, _EPS), 1 - _EPS)


def _lognormal_us(median_us, sigma_log, u):
    z = _NORMAL.inv_cdf(u)
    return max(1, round(median_us * math.exp(sigma_log * z)))


def anchored_lognormal_params(anchor_min_us, anchor_max_us):
    """Derive (median, sigma) treating the anchors as the p05/p95 span
    (game-task-chain modeling_notes)."""
    median = math.sqrt(anchor_min_us * anchor_max_us)
    sigma = math.log(anchor_max_us / median) / _NORMAL.inv_cdf(0.95)
    return median, sigma


def sample(param, seed, *key, allow_zero=False):
    """Draw one concrete value from an archetype param object. allow_zero applies to a quantile table whose zeros
    are measured values (9.6 D25); every other dist is unchanged."""
    dist = param["dist"]
    if dist == "constant":
        return param["value_us"] if "value_us" in param else param["value"]
    if dist == "uniform":
        u = uniform(seed, *key)
        return param["min"] + u * (param["max"] - param["min"])
    if dist == "lognormal":
        if "median_us" in param:
            median, sigma = param["median_us"], param["sigma_log"]
        else:
            median, sigma = anchored_lognormal_params(
                param["anchor_min_us"], param["anchor_max_us"])
        return _lognormal_us(median, sigma, uniform(seed, *key))
    if dist == "lognormal-mixture":
        pick = uniform(seed, *key, "component")
        if pick < param["pause_probability"]:
            mean, sigma = param["pause_mean_us"], param["pause_sigma_log"]
        else:
            mean, sigma = param["fluent_mean_us"], param["fluent_sigma_log"]
        median = mean / math.exp(sigma**2 / 2)  # mean -> median for lognormal
        return _lognormal_us(median, sigma, uniform(seed, *key, "value"))
    if dist == "quantiles":
        return _quantile_sample(param, uniform(seed, *key), allow_zero)
    raise ValueError(f"unknown dist {dist!r}")


# Quantile tables (9.5 changelog D17): measured distributions carried as the
# pooled percentiles QUANTILE_PROBS, in integer microseconds. A measured table
# also carries the sample's `min` and `max` and `means`, the measured mean of
# each of the eleven intervals they and the percentiles bound: a draw picks its
# interval by u and falls inside it on the curve lo + (hi - lo) * v**a, v the
# position in the interval, a set so the interval's mean is the measured one —
# the percentiles are kept and so is the table's mean. A table without them is
# sampled by linear interpolation on u with the tails held at the end values.
QUANTILE_PROBS = (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999)
_EDGES = (0.0, *QUANTILE_PROBS, 1.0)


def _interval(param):
    """(bounds, means) of a table carrying its extremes and interval means, the means held inside their
    intervals (a knot rounded to the microsecond can leave a mean a fraction outside)."""
    bounds = [param["min"], *param["p"], param["max"]]
    means = [min(max(m, lo), hi) for m, lo, hi in zip(param["means"], bounds, bounds[1:])]
    return bounds, means


def _power_draw(lo, hi, mean, v):
    if hi <= lo or mean <= lo:
        return lo
    if mean >= hi:
        return hi
    return lo + (hi - lo) * v ** ((hi - lo) / (mean - lo) - 1)


def _quantile_sample(param, u, allow_zero=False):
    """allow_zero: keep a drawn zero instead of the 1 us floor — for a zero-inclusive table, where a zero is the
    measured value and not a too-short duration (9.6 D25: the block after a run is zero when the program ran on)."""
    floor = (lambda v: max(0, round(v))) if allow_zero else (lambda v: max(1, round(v)))
    q = param["p"]
    if len(q) != len(QUANTILE_PROBS):
        raise ValueError("quantiles param needs %d values" % len(QUANTILE_PROBS))
    if "means" in param:
        bounds, means = _interval(param)
        for i in range(len(_EDGES) - 1):
            if u <= _EDGES[i + 1] or i == len(_EDGES) - 2:
                v = (u - _EDGES[i]) / (_EDGES[i + 1] - _EDGES[i])
                return floor(_power_draw(bounds[i], bounds[i + 1], means[i], min(max(v, 0.0), 1.0)))
    if u <= QUANTILE_PROBS[0]:
        return floor(q[0])
    if u >= QUANTILE_PROBS[-1]:
        return floor(q[-1])
    for i in range(1, len(QUANTILE_PROBS)):
        if u <= QUANTILE_PROBS[i]:
            p0, p1 = QUANTILE_PROBS[i - 1], QUANTILE_PROBS[i]
            v0, v1 = q[i - 1], q[i]
            return floor(v0 + (v1 - v0) * (u - p0) / (p1 - p0))
    return floor(q[-1])


def sample_first_gap(param, seed, *key):
    """The first gap of a stream already running: the time from an arbitrary instant to its next wake, the forward
    recurrence of a measured gap table (9.5 D77). An arbitrary instant falls in a gap with probability in proportion
    to its length, and anywhere in it: the gap is drawn length-biased — its interval by mass × interval mean, then
    inside the interval with density in proportion to x on the draw's curve — and the instant a uniform fraction into
    it. On the curve lo + (hi − lo)·v**a, v uniform, the length-biased v has density (lo + (hi − lo)·v**a) / mean: v
    uniform with probability lo / mean, else v**(a + 1) uniform. A table without extremes and means is uniform between
    its quantiles and held at the end ones: the same curve, each interval's mean its midpoint."""
    if param.get("dist") != "quantiles":
        raise ValueError("a running stream's first gap needs a quantile table")
    if "means" in param:
        bounds, means = _interval(param)
    else:
        q = param["p"]
        bounds = [q[0], *q, q[-1]]
        means = [(lo + hi) / 2 for lo, hi in zip(bounds, bounds[1:])]
    weights = [m * (b - a) for m, a, b in zip(means, _EDGES, _EDGES[1:])]
    pick = uniform(seed, *key, "first", "interval") * sum(weights)
    i = 0
    while i < len(weights) - 1 and pick > weights[i]:
        pick -= weights[i]
        i += 1
    lo, hi, mean = bounds[i], bounds[i + 1], means[i]
    if hi <= lo or mean <= lo:
        length = lo
    elif mean >= hi:
        length = hi
    else:
        a = (hi - lo) / (mean - lo) - 1
        v = uniform(seed, *key, "first", "v")
        if uniform(seed, *key, "first", "part") >= lo / mean:
            v = v ** (1 / (a + 1))
        length = lo + (hi - lo) * v ** a
    return max(1, round(uniform(seed, *key, "first", "at") * length))


def quantile_mean_us(param):
    """A table's mean: its interval means weighted by their mass, or, for a table without them, the mean of the
    piecewise-linear quantile function (trapezoids between the tabulated probabilities; the tails held flat)."""
    if "means" in param:
        _, means = _interval(param)
        return sum(m * (b - a) for m, a, b in zip(means, _EDGES, _EDGES[1:]))
    q = param["p"]
    total = q[0] * QUANTILE_PROBS[0]
    for i in range(1, len(QUANTILE_PROBS)):
        total += (q[i - 1] + q[i]) / 2 * (QUANTILE_PROBS[i] - QUANTILE_PROBS[i - 1])
    total += q[-1] * (1 - QUANTILE_PROBS[-1])
    return total


def mean_us(param):
    """Analytic mean of a param, for the static demand estimate."""
    dist = param["dist"]
    if dist == "constant":
        return param["value_us"] if "value_us" in param else param["value"]
    if dist == "uniform":
        return (param["min"] + param["max"]) / 2
    if dist == "lognormal":
        if "median_us" in param:
            median, sigma = param["median_us"], param["sigma_log"]
        else:
            median, sigma = anchored_lognormal_params(
                param["anchor_min_us"], param["anchor_max_us"])
        return median * math.exp(sigma**2 / 2)
    if dist == "lognormal-mixture":
        p = param["pause_probability"]
        return (1 - p) * param["fluent_mean_us"] + p * param["pause_mean_us"]
    if dist == "quantiles":
        return quantile_mean_us(param)
    raise ValueError(f"unknown dist {dist!r}")
