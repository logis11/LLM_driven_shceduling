"""within_event_desktop.py APP PROBE PHASE POOL WINDOW_S STEP_S FROM_S PART... — 9.5 D57's test on a desktop subject's
event parts (one process tree): each part's wake rate over a WINDOW_S window slid in STEP_S steps along the probe's
phase from FROM_S, against its spread across the pool's repeats; both half the range over the midpoint. Wakes are the
desktop analysis's (desktop/analyze.py, its rows kept), named by channel (campaign/analyze.py's channel_named)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, *[".."] * 4, "dataset", "tools"))
from meas.desktop import analyze  # noqa: E402
from meas.campaign.analyze import channel_named  # noqa: E402
app, probe, phase, pool_path, W, STEP, FROM = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])
parts = sys.argv[8:]
ph = analyze.analyze_phase(probe, phase, app, keep_rows=True)
rows = channel_named(ph["_rows"]); t0, span = ph["t0"], ph["span_s"]
pool = json.load(open(pool_path))["runs"][app]["phases"][phase]
half = lambda xs: (max(xs) - min(xs)) / 2 / ((max(xs) + min(xs)) / 2) * 100 if max(xs) + min(xs) else float("nan")
print(f"{app} {phase}: probe span {span:.0f} s; windows {W:.0f} s from {FROM:.0f} s, step {STEP:.0f} s")
for part in parts:
    members = set(pool["components"]["residual_event"]["comms"]) if part == "residual [event]" else {part}
    ts = sorted(r.t_in - t0 for r in rows if r.comm in members)
    rates, s = [], FROM
    while s + W <= span + 1e-9:
        rates.append(sum(1 for t in ts if s <= t < s + W) / W); s += STEP
    w = pool["components"]["residual_event"]["wakes_per_s"] if part == "residual [event]" else pool["threads"][part]["wakes_per_s"]
    counts = [round(x * y) for x, y in zip(w, pool["span_s"])]
    print(f"  {part:28} within one run {min(rates):.4f}–{max(rates):.4f}/s ±{half(rates):.1f} % ({len(rates)} windows); "
          f"across the {len(w)} repeats {min(w):.4f}–{max(w):.4f}/s ±{half(w):.1f} %; {min(counts)}–{max(counts)} wakes a phase")
