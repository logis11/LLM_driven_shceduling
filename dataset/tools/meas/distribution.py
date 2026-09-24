"""The measured distributions every campaign carries, and the gaps of a component.

A table is the ten pooled quantiles p1 … p99.9 (9.5 changelog D17; linear between order statistics, as `pct`
has always computed them), the sample's minimum and maximum, and the mean of the samples each of the eleven
intervals they bound holds — so a table's mean is the sample's mean. The interval means are taken from the
sample's own step distribution with fractional mass at the edges, so their weighted sum is the sample mean exactly.

A component's gaps are taken over its merged wake times — every thread of it, one stream, as the compiler emits
one stream per component — and wrap around the span it was observed over: segments (a phase, the windows of an
operation, the renderers of one repeat) are laid end to end and the last wake's gap runs round to the first, so
the gaps sum to the span and there is one gap per wake. The rate a table implies is then the rate measured.
"""

QUANTILE_PROBS = (0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999)


def _linear_quantile(v, q):
    k = (len(v) - 1) * q
    lo = int(k)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def quantile_table(values):
    """{"p": ten quantiles, "min", "max", "means": eleven interval means} of a sample, in its own unit. A numpy
    array is sorted and summed as one (the background campaign's tables hold millions of samples)."""
    if type(values).__module__ == "numpy":
        import numpy as np
        v = np.sort(np.asarray(values, dtype=np.float64))
        prefix = np.concatenate(([0.0], np.cumsum(v)))
    else:
        v = sorted(values)
        prefix = [0.0]
        for x in v:
            prefix.append(prefix[-1] + x)
    n = len(v)
    if not n:
        return None

    def integral(u):   # ∫_0^u of the sample's step quantile function, each sample holding 1/n of the mass
        h = u * n
        j = min(int(h), n - 1)
        return (prefix[j] + v[j] * (h - j)) / n

    edges = (0.0, *QUANTILE_PROBS, 1.0)
    means = [float((integral(b) - integral(a)) / (b - a)) for a, b in zip(edges, edges[1:])]
    p = [float(_linear_quantile(v, q)) for q in QUANTILE_PROBS]
    bounds = [float(v[0]), *p, float(v[-1])]
    return {"p": p, "min": bounds[0], "max": bounds[-1], "means": _inside(means, bounds, edges)}


def _inside(means, bounds, edges):
    """Each interval's mean held inside its interval, the weighted sum kept. The sample's step mass and the linear
    knots disagree near a knot — by a fraction of one sample in a large table, across whole intervals in a table of a
    few samples — so a step mean can fall outside its interval. Each is clamped into it, and what the clamping took
    from the weighted sum is given back across the intervals in proportion to the room each has left toward the side
    it is owed; the table's mean stays the sample's (the sample mean always lies between the sums of the lower and of
    the upper bounds)."""
    w = [b - a for a, b in zip(edges, edges[1:])]
    target = sum(wi * mi for wi, mi in zip(w, means))
    m = [min(max(mi, lo), hi) for mi, lo, hi in zip(means, bounds, bounds[1:])]
    owed = target - sum(wi * mi for wi, mi in zip(w, m))
    room = [wi * ((hi - mi) if owed > 0 else (mi - lo)) for wi, mi, lo, hi in zip(w, m, bounds, bounds[1:])]
    total = sum(room)
    if owed and total > 0:
        share = min(1.0, abs(owed) / total)
        m = [mi + share * ((hi - mi) if owed > 0 else (lo - mi)) for mi, lo, hi in zip(m, bounds, bounds[1:])]
    return m


def circular_gaps(segments):
    """segments: [(wake times, start, end)] laid end to end, times inside their segment. The gaps between
    consecutive wakes on the joined axis, and the one that wraps from the last wake round to the first."""
    axis, offset = [], 0.0
    for times, start, end in segments:
        axis += [offset + (t - start) for t in times]
        offset += end - start
    axis.sort()
    if not axis:
        return []
    gaps = [b - a for a, b in zip(axis, axis[1:])]
    gaps.append(offset - (axis[-1] - axis[0]))
    return gaps


def yaml_table(table, tag, scale=1000.0, sampling="per-iteration"):
    """The library's `quantiles` param for a table: knots and extremes in integer microseconds, interval means to a
    thousandth of one. scale: microseconds per unit of the table (1000 for a table in ms, 1 for one in µs)."""
    us = lambda x: int(round(x * scale))
    return ("{dist: quantiles, p: [" + ", ".join(str(us(v)) for v in table["p"]) + "], "
            f"min: {us(table['min'])}, max: {us(table['max'])}, "
            "means: [" + ", ".join(f"{m * scale:.3f}".rstrip("0").rstrip(".") for m in table["means"]) + "], "
            f"sampling: {sampling}, source: \"{tag}\"}}")
