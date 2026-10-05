#!/usr/bin/env python3
"""9.10's span probes read (9.10 changelog D143, D144; `task-9.10-scenarios-timelines/campaign/spans/method.md` §3).

  span_probe.py level <run-dir> <phase> <phase-s> <span-s> [--s 10] [--json OUT]
      D143's standard (9.5 D53, D56): from the 10 s slice profile (slices.py), the level over the file's span — CPU
      ms/s and wakes/s from the phase's opening — against the observed phase's window at the placement every repeat
      takes, the phase's first <phase-s>; the worst placement of a <phase-s> window inside the span, stepped by one
      slice, beside it. A difference over 5 % in either is a phase that does not hold over the span. <phase> `driven`
      reads a probe-driven run's windows driven-w01, driven-w02, … in order, their slices end to end.
  span_probe.py level-desktop <run-dir> <app> <phase-s> <span-s> [--s 10] [--json OUT]
      The same on a desktop probe's carried rows (desktop/analyze.py's view of the subject, 9.8's renderers).
  span_probe.py paired <run-dir> <pool.json> [--json OUT]
      D144: each driven window's per-input run mean — the window rule's `run_ms_minus_idle` (analyze.py), read as the
      pool reads a repeat, the idle rate from the probe's own idle phase — against the pooled record's repeat k's
      mean; the ratios read as 9.5 D81's stimulus check reads its per-repeat ratios (`pool.stimulus_check`), their
      least-squares slope on k with its 95 % t interval beside them.
"""

import argparse
import json
import os
import re
import shutil
import statistics
import sys
import tempfile

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import analyze_run  # noqa: E402
from meas.campaign.slices import profile  # noqa: E402
from meas.stability import t975  # noqa: E402

TOLERANCE = 0.05   # the dataset's tolerance (`measurement-campaign-workflow.md`, "The stability rule")
IDLE_FROM_S = {"code": 200.0}   # 9.5 D83, as campaign/pool.py reads `code`'s idle phase
WINDOW_RX = re.compile(r"^perf\.(driven-w\d+)\.timehist\.txt(\.gz)?$")


def window_names(run_dir):
    """A probe-driven run's driven windows, in order."""
    return sorted({m.group(1) for f in os.listdir(run_dir) if (m := WINDOW_RX.match(f))})


def view(run_dir, name, dest):
    """A folder in which window <name> is the run's `driven` phase: its trace, wakeup rows, snapshots and replay log
    linked under the names analyze.py reads, beside the run's report and idle phase."""
    os.makedirs(dest, exist_ok=True)
    links = {"report.json": "report.json"}
    for f in os.listdir(run_dir):
        if f.startswith(("perf.idle.", "snap.idle.")):
            links[f] = f
        elif f.startswith((f"perf.{name}.", f"snap.{name}.")):
            links[f.replace(f".{name}.", ".driven.", 1)] = f
    links["replay.jsonl"] = f"replay.{name}.jsonl"
    for to, frm in links.items():
        if os.path.exists(os.path.join(run_dir, frm)):
            os.symlink(os.path.abspath(os.path.join(run_dir, frm)), os.path.join(dest, to))
    return dest


def level_reading(cpu, wakes, slice_s, phase_s, span_s):
    """D143's reading on one slice profile: the level over the span's slices, the phase's first window against it,
    and the worst window of the phase's length inside the span. Relative differences, signed."""
    n, m = int(round(span_s / slice_s)), int(round(phase_s / slice_s))
    if n > len(cpu):
        raise ValueError(f"the probe holds {len(cpu) * slice_s:g} s, short of the {span_s:g} s span")
    if not 0 < m <= n:
        raise ValueError(f"a {phase_s:g} s phase does not fit a {span_s:g} s span")
    out = {"slice_s": slice_s, "phase_s": phase_s, "span_s": span_s}
    for key, xs in (("cpu_ms_per_s", cpu), ("wakes_per_s", wakes)):
        level = statistics.fmean(xs[:n])
        rel = [statistics.fmean(xs[i:i + m]) / level - 1 if level else 0.0 for i in range(n - m + 1)]
        worst = max(range(len(rel)), key=lambda i: abs(rel[i]))
        out[key] = {"level": round(level, 4), "placement": round(rel[0], 4),
                    "worst": round(rel[worst], 4), "worst_at_s": round(worst * slice_s, 1),
                    "holds": abs(rel[0]) <= TOLERANCE}
    out["holds"] = out["cpu_ms_per_s"]["holds"] and out["wakes_per_s"]["holds"]
    return out


def slices_of_rows(rows, t0, span, slice_s):
    """(CPU ms/s, wakes/s) per slice from (t_in, run_ms) wake rows, as slices.profile slices a campaign phase."""
    n = max(1, int(span // slice_s))
    cpu, wakes = [0.0] * n, [0] * n
    for t_in, run in rows:
        i = int((t_in - t0) // slice_s)
        if 0 <= i < n:
            cpu[i] += run
            wakes[i] += 1
    return [c / slice_s for c in cpu], [w / slice_s for w in wakes]


def driven_profile(run_dir, slice_s):
    """The probe-driven run's windows' slice profiles end to end, the gaps between windows left out."""
    cpu, wakes = [], []
    tmp = tempfile.mkdtemp()
    try:
        for name in window_names(run_dir):
            _, c, w = profile(view(run_dir, name, os.path.join(tmp, name)), "driven", slice_s)
            cpu += c
            wakes += w
    finally:
        shutil.rmtree(tmp)
    return cpu, wakes


def window_means(run_dir, w_ms, cap_ms, idle_from_s):
    """{k: the mean of window k's per-input runs net of the idle rate}, the window rule as the pool reads a repeat."""
    out = {}
    tmp = tempfile.mkdtemp()
    try:
        for name in window_names(run_dir):
            _, raw = analyze_run(view(run_dir, name, os.path.join(tmp, name)), w_ms, cap_ms, idle_from_s=idle_from_s)
            corr = raw["phases"].get("driven", {}).get("per_input", {}).get("win_run_corr") or []
            out[int(name.rsplit("w", 1)[1])] = statistics.fmean(corr) if corr else None
    finally:
        shutil.rmtree(tmp)
    return out


def campaign_means(pool, app):
    """{repeat: its per-input run mean net of the idle rate} from a 9.5 pooled record (`pool-<app>.json`)."""
    d = pool["runs"][app]["phases"]["driven"]
    return dict(zip(d["repeats"], d["per_input"]["window"]["run_ms_minus_idle"]["repeat_mean"]))


def slope(xs, ys):
    """The least-squares slope of ys on xs with its 95 % t interval (n − 2 degrees of freedom)."""
    n = len(xs)
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    resid = [y - (my + b * (x - mx)) for x, y in zip(xs, ys)]
    se = (sum(r * r for r in resid) / (n - 2) / sxx) ** 0.5
    hw = t975(n - 1) * se
    return {"per_window": b, "interval": [b - hw, b + hw],
            "reading": "difference" if not b - hw <= 0 <= b + hw else "not resolved"}


def paired_reading(probe, campaign):
    """D144: probe window k's mean against the campaign's repeat k's, over the windows both hold. The ratios as
    9.5 D81's check reads its per-repeat ratios — a difference when the 95 % t interval of their mean excludes 1, not
    resolved otherwise — and their trend over k."""
    ks = [k for k in sorted(probe) if probe[k] and campaign.get(k)]
    r = [probe[k] / campaign[k] for k in ks]
    m, hw = statistics.fmean(r), t975(len(r)) * statistics.stdev(r) / len(r) ** 0.5
    trend = slope(ks, r)
    return {"windows": ks, "per_window": [round(x, 4) for x in r], "per_window_mean": round(m, 4),
            "interval": [round(m - hw, 4), round(m + hw, 4)],
            "reading": "difference" if not m - hw <= 1 <= m + hw else "not resolved",
            "trend": {"per_window": round(trend["per_window"], 5), "interval": [round(x, 5) for x in trend["interval"]],
                      "reading": trend["reading"]},
            "probe_ms": {k: round(probe[k], 4) for k in ks}, "campaign_ms": {k: campaign[k] for k in ks}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    lv = sub.add_parser("level"); lv.add_argument("run_dir"); lv.add_argument("phase")
    lv.add_argument("phase_s", type=float); lv.add_argument("span_s", type=float)
    lv.add_argument("--s", type=float, default=10.0); lv.add_argument("--json")
    ld = sub.add_parser("level-desktop"); ld.add_argument("run_dir"); ld.add_argument("app")
    ld.add_argument("phase_s", type=float); ld.add_argument("span_s", type=float)
    ld.add_argument("--s", type=float, default=10.0); ld.add_argument("--json")
    pr = sub.add_parser("paired"); pr.add_argument("run_dir"); pr.add_argument("pool"); pr.add_argument("--json")
    a = ap.parse_args()
    if a.cmd == "level":
        if a.phase == "driven":
            cpu, wakes = driven_profile(a.run_dir, a.s)
        else:
            _, cpu, wakes = profile(a.run_dir, a.phase, a.s)
        out = level_reading(cpu, wakes, a.s, a.phase_s, a.span_s)
    elif a.cmd == "level-desktop":
        from meas.desktop import analyze as a98
        from meas.desktop.fold_in import CARRIED
        ph = a98.analyze_phase(a.run_dir, CARRIED[a.app], a.app, keep_rows=True)
        cpu, wakes = slices_of_rows([(r.t_in, r.run) for r in ph["_rows"]], ph["t0"], ph["span_s"], a.s)
        out = level_reading(cpu, wakes, a.s, a.phase_s, a.span_s)
    else:
        pool = json.load(open(a.pool))
        app = next(iter(pool["runs"]))
        report = json.load(open(os.path.join(a.run_dir, "report.json")))
        if report.get("app") != app:
            raise SystemExit(f"the probe ran {report.get('app')!r}, the pool holds {app!r}")
        probe = window_means(a.run_dir, pool.get("w_ms", 5.0), pool.get("cap_ms", 0.0), IDLE_FROM_S.get(app, 0.0))
        out = paired_reading(probe, campaign_means(pool, app))
    print(json.dumps(out, indent=1))
    if a.json:
        open(a.json, "w").write(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
