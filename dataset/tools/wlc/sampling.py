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


def sample(param, seed, *key):
    """Draw one concrete value from an archetype param object."""
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
    raise ValueError(f"unknown dist {dist!r}")


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
    raise ValueError(f"unknown dist {dist!r}")
