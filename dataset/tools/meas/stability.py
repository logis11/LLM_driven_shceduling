"""The stability criterion shared by the campaigns (9.6 changelog D10, D11; 9.5 changelog D26).

The pool of same-machine repeats is stable when the 95 % confidence half-width of the across-repeat mean of a
carried median (t multiplier, k − 1 degrees of freedom), relative to the mean, is at most TOLERANCE. Repeats are
added one at a time until it holds; every same-machine repeat obtained is pooled and reported.
"""

import statistics

T975 = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262,
        11: 2.228, 12: 2.201, 13: 2.179, 14: 2.160, 15: 2.145, 16: 2.131, 17: 2.120, 18: 2.110, 19: 2.101, 20: 2.093}
TOLERANCE = 0.05


def stability(values_by_repeat):
    """The half-width of one carried median over its repeats (a dict keyed by repeat, or a list), and the largest
    shift of the mean when any one repeat is dropped."""
    vals = values_by_repeat.values() if isinstance(values_by_repeat, dict) else values_by_repeat
    v = [x for x in vals if x]
    k = len(v)
    if k < 2:
        return {"k": k, "mean": v[0] if v else None, "cv": None, "half_width": None, "leave_one_out": None, "passes": False}
    m, sd = statistics.fmean(v), statistics.stdev(v)
    hw = T975.get(k, T975[20]) * sd / (k ** 0.5) / m
    loo = max(abs(statistics.fmean(v[:i] + v[i + 1:]) - m) / m for i in range(k))
    return {"k": k, "mean": round(m, 4), "cv": round(sd / m, 4), "half_width": round(hw, 4), "leave_one_out": round(loo, 4),
            "passes": hw <= TOLERANCE}
