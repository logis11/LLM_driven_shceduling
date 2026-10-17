#!/usr/bin/env python3
"""D57's test, as run for D83: code's `utility/libuv-worker` wake rate over a 700 s window (the idle phase read from 200 s,
D83) slid in 10 s steps along the D52 probe's idle phase (run 35496163876) from 200 s, against its spread across the
pooled repeats. Wakes are named as campaign/pool.py names them (role and comm, D67). Both spreads are half the range
over its midpoint.

within_libuv.py [<probe artifact dir> [<pooled.json>]]   (defaults: the loop's work directory, the committed pool)
"""
import json, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, *[".."] * 5, "dataset", "tools"))
from meas.campaign.analyze import analyze_run, component_name  # noqa: E402
from meas import burstiness  # noqa: E402
PROBE = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.cache/meas-loop/long-probe/35496163876/meas-long-probe-code-r1-probe")
POOL = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "results-re-measured", "pool-code.json")
FROM, W, STEP, COMP = 200.0, 700.0, 10.0, "utility/libuv-worker"
component_key = burstiness._campaign_pool_module().component_key
_, raw = analyze_run(PROBE)
p = raw["phases"]["idle"]
ts = sorted(r.t_in - p["t0"] for r in p["rows"]
            if component_name(p["roles"].get(r.pid, "main"), component_key("code", r.comm)) == COMP)
rates, s = [], FROM
while s + W <= p["span"] + 1e-9:
    rates.append(sum(1 for t in ts if s <= t < s + W) / W)
    s += STEP
half = lambda xs: (max(xs) - min(xs)) / 2 / statistics.fmean(xs) * 100
print(f"probe idle span {p['span']:.0f} s; {len(rates)} windows from {FROM:.0f} s, {W:.0f} s long, step {STEP:.0f} s")
print(f"within one run: {min(rates):.2f}–{max(rates):.2f} a second, ±{half(rates):.1f} %")
w = json.load(open(POOL))["runs"]["code"]["phases"]["idle"]["threads"][COMP]["wakes_per_s"]
print(f"across the {len(w)} pooled repeats: {min(w):.2f}–{max(w):.2f} a second, ±{half(w):.1f} %")
