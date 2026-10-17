#!/usr/bin/env python3
"""D57's test, as run for D59: each of webrtc's seven failing play values over a 480 s window (the play phase) slid in
10 s steps along the D52 probe's steady call (run 35496212906, from the 210 s settle), against its spread across the
pooled repeats. Values are computed as campaign/pool.py computes them: per-thread gaps pooled per component, the
residual's gaps over its merged wake times. Both spreads are half the range over its midpoint.

within_call.py [<probe artifact dir> [<pooled.json>]]   (defaults: the loop's work directory)
"""
import json, os, statistics, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 5, "dataset", "tools", "meas", "campaign"))
from analyze import analyze_run
PROBE = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/.cache/meas-loop/long-probe/35496212906/meas-long-probe-webrtc-r1-probe")
POOL = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.cache/meas-loop/pool/playback-webrtc-from245/pooled.json")
SETTLE, W, STEP = 210.0, 480.0, 10.0
e = json.load(open(POOL))["runs"]["webrtc"]
comp = e["phases"]["play"]["components"]
rest = set(comp["residual"]["comms"])
_, raw = analyze_run(PROBE)
p = raw["phases"]["play"]; rows, t0, span = p["rows"], p["t0"], p["span"]
print(f"probe play span {span:.0f} s, rows {len(rows)}; windows from {SETTLE:.0f} s, {W:.0f} s long, step {STEP:.0f} s")
def values(a, b):
    sel = [r for r in rows if a <= r.t_in - t0 < b]
    out = {}
    for name in ("AudioProcessing", "AudioOutputDevi", "AudioInputDevic", "FakeAudioInput", "residual"):
        rs = [r for r in sel if (r.comm in rest if name == "residual" else r.comm == name)]
        if name == "residual":
            ts = sorted(r.t_in for r in rs); gaps = [(y - x) * 1000 for x, y in zip(ts, ts[1:])]
        else:
            by = {}
            for r in rs: by.setdefault(r.tid, []).append(r.t_in)
            gaps = [(y - x) * 1000 for ts in by.values() for x, y in zip(ts, ts[1:])]
        out[f"{name} wakes/s"] = len(rs) / (b - a)
        out[f"{name} gap mean (ms)"] = statistics.fmean(gaps) if gaps else None
        out[f"{name} run mean (ms)"] = statistics.fmean(r.run for r in rs) if rs else None
    return out
starts = [SETTLE + i * STEP for i in range(int((span - SETTLE - W) // STEP) + 1)]
win = [values(s, s + W) for s in starts]
q = e["stability"]["quantities"]
print(f"{len(starts)} windows, {len(e['repeats'])} repeats\n")
print(f"{'value':38} {'within the call: range':>24} {'±half-range':>11} | {'across repeats: range':>26} {'±half-range':>11} {'cv':>6}  pool")
for key in win[0]:
    xs = [w[key] for w in win if w[key] is not None]
    lo, hi = min(xs), max(xs); mid = (lo + hi) / 2
    name = "play " + key
    rp = None
    # the per-repeat means the pool tests
    ph = e["phases"]["play"]
    c, what = key.rsplit(" ", 1)[0].split(" ")[0], key.split(" ", 1)[1]
    src = ph["components"]["residual"] if c == "residual" else ph["threads"].get(c) if "threads" in ph else None
    stat = q.get(name)
    fail = "" if stat is None else ("passes" if stat["passes"] else "carried (D57)" if stat.get("session_spread") else "fails")
    reps = None
    if src is not None:
        if what == "wakes/s": reps = src.get("wakes_per_s")
        elif what.startswith("gap"): reps = src["gap_ms"]["repeat_mean"]
        else: reps = src["run_ms"]["repeat_mean"]
    if reps and isinstance(reps, list):
        rl, rh = min(reps), max(reps); rm = (rl + rh) / 2
        across = f"{rl:10.4g} – {rh:<10.4g}  ±{(rh-rl)/2/rm*100:6.1f} % {statistics.stdev(reps)/statistics.fmean(reps):6.3f}"
    else:
        across = "(not in pooled record)"
    print(f"{name:38} {lo:10.4g} – {hi:<10.4g} ±{(hi-lo)/2/mid*100:6.1f} % | {across}  {fail}")

# the part of the spread that follows the runner: per-repeat means against FakeAudioInput's run mean, a 100-a-second
# timer thread whose work is the same in every session
ph = e["phases"]["play"]; th = ph["threads"]
def corr(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / ((len(a) - 1) * statistics.stdev(a) * statistics.stdev(b))
ref = th["FakeAudioInput"]["run_ms"]["repeat_mean"]
print("\ncorrelation across repeats with FakeAudioInput's run mean:")
for label, v in [("AudioInputDevic run mean", th["AudioInputDevic"]["run_ms"]["repeat_mean"]),
                 ("WebRTC_W_and_N run mean", th["WebRTC_W_and_N"]["run_ms"]["repeat_mean"]),
                 ("residual run mean", ph["components"]["residual"]["run_ms"]["repeat_mean"]),
                 ("AudioOutputDevi run mean", th["AudioOutputDevi"]["run_ms"]["repeat_mean"]),
                 ("AudioProcessing run mean", th["AudioProcessing"]["run_ms"]["repeat_mean"]),
                 ("AudioProcessing wakes/s", th["AudioProcessing"]["wakes_per_s"]),
                 ("play CPU share", ph["cpu_share"])]:
    print(f"   {label:26} {corr(ref, v):+.2f}")
