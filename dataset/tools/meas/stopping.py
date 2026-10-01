#!/usr/bin/env python3
"""The stability rule's stopping simulated at an observed spread (9.5 D88). The rule adds one repeat at a time from
five and stops at the first count whose 95 % half-width (`stability.t975`) is within 5 % of the mean, so the count is
chosen by the estimate it produces. For each 9.5 entry, its widest value the rule is read on (neither at a recording's
window limit nor carried under an exception), in the pools the fold-in carries: repeats drawn at that value's spread
(its per-repeat coefficient of variation in the pooled record), normal and lognormal, the rule run on that value alone,
and read over the simulated campaigns — the stopped mean's bias, the share of stopped intervals that cover the true
mean, the mean count at the stop.

stopping.py <out.json> [--md PAGE] [--n N]
"""

import argparse
import json
import math
import os
import random
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.stability import TOLERANCE, t975  # noqa: E402

NEAR = 0.045            # a value within half a point of the tolerance (the campaign record's line)
# D99: code's campaign stopped at window 44, then read as its recording's last; the recording holds 57, so the count is
# neither the rule's first pass nor the recording's end, and the stopping simulated does not describe it
STOPPED_SHORT = {"code": "stopped at window 44, short of its recording's 57, not by the rule"}
KMAX = 2000


def half_width(xs):
    return t975(len(xs)) * statistics.stdev(xs) / math.sqrt(len(xs))


def stop(draw, kmin=5, tol=TOLERANCE, kmax=KMAX):
    """Repeats drawn one at a time until, from kmin, the half-width is within tol of the mean: (k, mean, half-width)."""
    xs = []
    for k in range(1, kmax + 1):
        xs.append(draw())
        if k >= kmin:
            m, hw = statistics.fmean(xs), half_width(xs)
            if hw <= tol * m:
                break
    return k, m, hw


def simulate(cv, n, lognormal, rng, kmin=5, tol=TOLERANCE):
    """n campaigns of repeats with mean 1 and coefficient of variation cv: the stopped mean's bias, the stopped
    intervals' coverage of 1, the mean count at the stop."""
    sig = math.sqrt(math.log(1 + cv * cv))
    draw = (lambda: rng.lognormvariate(-0.5 * sig * sig, sig)) if lognormal else (lambda: rng.gauss(1.0, cv))
    bias, cover, ks = [], 0, []
    for _ in range(n):
        k, m, hw = stop(draw, kmin, tol)
        bias.append(m - 1.0)
        cover += abs(m - 1.0) <= hw
        ks.append(k)
    return {"mean_bias": statistics.fmean(bias), "coverage": cover / n, "mean_k": statistics.fmean(ks)}


def widest(quantities, phases=None):
    """(name, quantity) of the widest value the rule is read on — not at a window limit, not carried under an
    exception — in the named phases (the name's first word) or in all."""
    ok = {n: q for n, q in quantities.items() if not q.get("limited") and not q.get("carried")
          and (phases is None or n.split()[0] in phases)}
    return max(ok.items(), key=lambda kv: kv[1]["half_width"])


def coverage_range(entry):
    c = [s["coverage"] for s in entry["simulated"].values()]
    return min(c), max(c)


def entries(n, seed=1):
    """Each 9.5 entry whose repeat count the rule chose, in the pools the fold-in carries; an entry that stopped at its
    recording's last window, or short of it (D99), is listed, not simulated."""
    from meas import control_report as cr
    out = []
    for app, arch in cr.ARCH_95.items():
        idle_from = cr.IDLE_FROM_95.get(app)
        src = idle_from or cr.POOL_95[app]
        run = json.load(open(os.path.join(src, f"pool-{app}.json")))["runs"][app]
        st = run["stability"]
        by_window = st["window_limit"] is not None and not idle_from and len(run["repeats"]) >= st["window_limit"]
        short = STOPPED_SHORT.get(app)
        name, q = widest(st["quantities"], ("idle",) if idle_from else None)
        e = {"archetype": arch, "app": app, "pool": os.path.relpath(src, cr.REPO), "repeats": len(run["repeats"]),
             "stopped_at_window_limit": by_window, "widest": {"value": name, **{k: q[k] for k in ("k", "cv", "half_width")}}}
        if short:
            e["stop"] = short
        elif not by_window:
            e["simulated"] = {d: simulate(q["cv"], n, d == "lognormal", random.Random(seed))
                              for d in ("normal", "lognormal")}
        out.append(e)
        print(arch, file=sys.stderr)
    return out


def render(record):
    lines = ["# The stability rule's stopping, simulated", "",
             f"Each entry's widest value the rule is read on, its repeats drawn at the value's per-repeat spread and the "
             f"rule run on it alone, {record['n']} simulated campaigns per distribution: the stopped mean's bias, the "
             "share of stopped 95 % intervals covering the true mean, the mean count at the stop. Where the count at the "
             "stop falls well short of the repeats obtained, other values set the count, and the value's own stopping "
             "does not describe how the campaign stopped.", "",
             "| entry | widest value | repeats | spread (CV) | half-width | mean bias (normal · lognormal) "
             "| coverage (normal · lognormal) | count at the stop (normal · lognormal) |",
             "|---|---|---|---|---|---|---|---|"]
    for e in record["entries"]:
        w = e["widest"]
        head = (f"| `{e['archetype']}` | {w['value']} | {w['k']} | {w['cv'] * 100:.2f} % | {w['half_width'] * 100:.2f} % |")
        if "simulated" not in e:
            lines.append(head + " " + e.get("stop", "stopped at its recording's last window") + " | | |")
            continue
        s = e["simulated"]
        lines.append(head + " " + " · ".join(f"{s[d]['mean_bias'] * 100:+.2f} %" for d in s) + " | "
                     + " · ".join(f"{s[d]['coverage'] * 100:.1f} %" for d in s) + " | "
                     + " · ".join(f"{s[d]['mean_k']:.1f}" for d in s) + " |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--md"); ap.add_argument("--n", type=int, default=4000)
    a = ap.parse_args()
    record = {"n": a.n, "entries": entries(a.n)}
    json.dump(record, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(record))


if __name__ == "__main__":
    main()
