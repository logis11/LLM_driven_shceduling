#!/usr/bin/env python3
"""A desktop long-phase probe read in time windows (9.8 D35). One probe job's phase, past the length the entry carries,
per carried component as `meas/windows.py` names a 9.8 entry's (the rows `desktop/analyze.py` keeps, a thread the
library does not carry read as the residual), in 100 s windows and in windows of the carried phase's length (the
pooled record's span): whether a component drifts past the carried phase, and how far its short windows spread.

probe_windows.py <probe-dir> <app> <out.json> [--md PAGE]
"""

import argparse
import json
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas import windows  # noqa: E402


def read_probe(rows, t0, span, carried_s):
    """rows: (name, t_in, run_ms). The phase in the short windows and in windows of the carried length."""
    return {"short": windows.pool([windows.read(rows, t0, span, windows.WIN_S)], windows.WIN_S),
            "carried": windows.pool([windows.read(rows, t0, span, carried_s)], carried_s)}


def entry(D, app):
    from meas import control_report as cr
    from meas.desktop import analyze as a98
    from meas.desktop.fold_in import CARRIED, IDS
    run = json.load(open(cr.pool_98(app)))["runs"][app]
    carried_s = float(round(min(run["phases"][CARRIED[app]]["span_s"])))
    carried = [c["comm"] for c in windows._library()[IDS[app]]["params"]["components"] if c["comm"] != "residual"]
    ph = a98.analyze_phase(D, CARRIED[app], app, keep_rows=True)
    named = [((r.comm if r.comm in carried else "residual"), r.t_in, r.run) for r in ph["_rows"]]
    report = json.load(open(os.path.join(D, "report.json")))
    return {"archetype": IDS[app], "app": app, "probe": os.path.basename(os.path.normpath(D)),
            "version": report.get(f"{app}.version"), "span_s": ph["span_s"], "carried_s": carried_s,
            **read_probe(named, ph["t0"], ph["span_s"], carried_s)}


def render(rec):
    per = ("Per component: each {0}'s wake rate over the component's mean over the {0}s, each {0}'s run mean (ms), its "
           "share of the phase's CPU, and the CPU its {0}s hold above its median {0} as a share of the phase's CPU.")
    lines = [f"# {rec['archetype']} (`{rec['app']}`): the long-phase probe in time windows", "",
             f"{rec['app'].capitalize()} {rec['version']}, one job, {rec['span_s']:g} s of the phase the entry carries "
             f"for {rec['carried_s']:g} s.", "",
             f"In {rec['short']['windows']} windows of {rec['short']['win_s']:g} s. " + per.format("window"), ""]
    lines += windows._table(rec["short"], "window")
    lines += ["", f"In windows of the carried phase's length, {rec['carried_s']:g} s ({rec['carried']['windows']}). "
              + per.format("window"), ""] + windows._table(rec["carried"], "window") + [""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("probe"); ap.add_argument("app"); ap.add_argument("out")
    ap.add_argument("--md")
    a = ap.parse_args()
    rec = entry(a.probe, a.app)
    json.dump(rec, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(rec))


if __name__ == "__main__":
    main()
