"""within_event.py APP PROBE POOL FROM_S WINDOW_S PART... — 9.5 D57's test (task-9.5's campaign/within_libuv.py) on the
event parts: each part's wake rate over a WINDOW_S window slid in 10 s steps along the probe's idle phase from FROM_S,
against its spread across the pool's repeats; both as half the range over the midpoint. Wakes are named as
campaign/pool.py names them (role and comm, D67; an event part with its suffix). A part named `residual [event]` is the
pool's event residual, its comms summed. FROM_S puts the window past the campaign's settle where the probe's is shorter."""
import json, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, *[".."] * 4, "dataset", "tools"))
from meas.campaign.analyze import analyze_run, component_name, wake_channel  # noqa: E402
from meas import burstiness  # noqa: E402
app, probe, pool_path, FROM, W = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
parts = sys.argv[6:]
pm = burstiness._campaign_pool_module()
_, raw = analyze_run(probe)
p = raw["phases"]["idle"]
def name(r):
    n = component_name(p["roles"].get(r.pid, "main"), pm.component_key(app, r.comm))
    return n + ("" if wake_channel(r) == "timer" else pm.EVENT_SUFFIX)
pool = json.load(open(pool_path))["runs"][app]["phases"]["idle"]
half = lambda xs: (max(xs) - min(xs)) / 2 / ((max(xs) + min(xs)) / 2) * 100 if max(xs) + min(xs) else float("nan")
ev = sum(1 for r in p["rows"] if wake_channel(r) == "event")
print(f"{app}: probe idle span {p['span']:.0f} s, {len(p['rows'])} wakes, {ev} event; windows {W:.0f} s from {FROM:.0f} s, step 10 s")
for part in parts:
    members = set(pool["components"]["residual_event"]["comms"]) if part == "residual [event]" else {part}
    ts = sorted(r.t_in - p["t0"] for r in p["rows"] if name(r) in members)
    rates, s = [], FROM
    while s + W <= p["span"] + 1e-9:
        rates.append(sum(1 for t in ts if s <= t < s + W) / W); s += 10.0
    w = pool["components"]["residual_event"]["wakes_per_s"] if part == "residual [event]" else pool["threads"][part]["wakes_per_s"]
    print(f"  {part:30} within one run {min(rates):.4f}–{max(rates):.4f}/s ±{half(rates):.1f} % ({len(rates)} windows, "
          f"probe mean {sum(1 for t in ts if t >= FROM) / max(p['span'] - FROM, 1):.4f}/s); across the {len(w)} repeats {min(w):.4f}–{max(w):.4f}/s ±{half(w):.1f} %")
