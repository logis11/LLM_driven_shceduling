#!/usr/bin/env python3
"""The compiled streams' burstiness against the measured (9.15's threat statement, from the 2026-09-26 review of
9.5–9.9). The compiler draws each component's gaps independently from its table (9.5 D77), which keeps each
component's rate, gap and run distributions but not the order of its gaps nor its components waking together. Per
carried repeat, the phase's wake stream — every row the pool reads, heavy events aside (D64) — and a compile of the
archetype's components over the same span, one seed per repeat, each read by its dispersion: the variance over the
mean of its wake counts in whole bins of 1 ms, 10 ms, 100 ms and 1 s (1 for a Poisson stream, above it bursty, below
it regular); the ratio, measured over compiled, per repeat. A JSON record and a results page, per archetype.

burstiness.py <campaign|desktop|session> <artifacts> <out.json> [--md PAGE] [--app APP]...
"""

import argparse
import glob
import json
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

BINS = {"1 ms": 0.001, "10 ms": 0.01, "100 ms": 0.1, "1 s": 1.0}
# the 9.5 entries that carry an idle phase's components (the periodic entries compile one job per cycle, and
# `image-editor` carries focus components only)
IDLE_95 = ("soffice", "code", "chrome", "thunderbird-send", "kdenlive")


def dispersion(times, span, w):
    """Variance over mean of the wake counts in the whole bins of width w over [0, span); None with no whole bin or no
    wake in them. Times in seconds from the phase's start, read at the microsecond."""
    w_us = int(round(w * 1e6))
    n = int(round(span * 1e6)) // w_us
    if not n:
        return None
    counts = [0] * n
    for t in times:
        k = int(round(t * 1e6)) // w_us
        if 0 <= k < n:
            counts[k] += 1
    m = statistics.fmean(counts)
    return statistics.pvariance(counts, m) / m if m else None


def compiled_times(components, span, seed):
    """The archetype's components compiled over [0, span) as the compiler emits them (wlc.compiler._component_events),
    their wake times in seconds."""
    from wlc.compiler import _component_events
    return sorted(t / 1e6 for t, _, _ in _component_events(components, seed, "b", 0, int(span * 1e6), "idle"))


def _spread(xs):
    xs = [x for x in xs if x is not None]
    return {"median": round(statistics.median(xs), 4), "min": round(min(xs), 4), "max": round(max(xs), 4)} if xs else None


def read_entry(measured, compiled):
    """{rep: (span, times)} each: per bin the measured and compiled dispersions and the per-repeat ratio, measured over
    compiled (none where the compiled stream has no spread), as their median, least and largest over the repeats."""
    reps = sorted(measured)
    bins = {}
    for label, w in BINS.items():
        dm = {r: dispersion(measured[r][1], measured[r][0], w) for r in reps}
        dc = {r: dispersion(compiled[r][1], compiled[r][0], w) for r in reps}
        ratio = [dm[r] / dc[r] if dm[r] is not None and dc[r] else None for r in reps]
        bins[label] = {"measured": _spread(dm.values()), "compiled": _spread(dc.values()), "ratio": _spread(ratio)}
    rate = lambda s: round(statistics.median(len(s[r][1]) / s[r][0] for r in reps), 3)
    return {"repeats": len(reps), "wakes_per_s": {"measured": rate(measured), "compiled": rate(compiled)}, "bins": bins}


def artifact_dir(root, app, rep, run_id, mode="full"):
    """A carried repeat's artifact: its run's copy of the repeat, wherever the loop cache holds it."""
    rep = str(rep).split("@")[0]   # 9.8 D24: a window landed more than once is keyed by its run as well
    found = {os.path.realpath(d) for d in glob.glob(os.path.join(root, "**", str(run_id), f"meas-*-{app}-r{rep}-{mode}"),
                                                     recursive=True)}
    if len(found) != 1:
        raise SystemExit(f"{app} repeat {rep} of run {run_id}: {len(found)} artifacts under {root}")
    return found.pop()


def _campaign_pool_module():
    """campaign/pool.py imports its sibling with a flat `from analyze import ...` (campaign/control.py's idiom)."""
    import importlib
    saved = sys.modules.pop("analyze", None)
    try:
        return importlib.import_module("meas.campaign.pool")
    finally:
        if saved is not None:
            sys.modules["analyze"] = saved


def campaign_streams(app, pooled, root, phase="idle"):
    """{rep: (span, times)} of a 9.5 app's carried repeats: the rows its pool reads (analyze_run with the pool's
    settings), heavy events aside, in seconds from the phase's start."""
    from meas.campaign.analyze import analyze_run
    split_events = _campaign_pool_module().split_events
    run = pooled["runs"][app]
    out = {}
    for rep in run["repeats"]:
        D = artifact_dir(root, app, rep, run["run_id"][str(rep)])
        _, raw = analyze_run(D, pooled.get("w_ms", 5.0), pooled.get("cap_ms", 0.0),
                             exclude_roles=tuple(pooled.get("exclude_roles") or ()))
        pd = raw["phases"][phase]
        rows, _ = split_events(app, phase, pd["rows"])
        out[rep] = (pd["span"], sorted(r.t_in - pd["t0"] for r in rows))
        print(f"{app} r{rep}: {len(rows)} wakes over {pd['span']:.0f} s", file=sys.stderr)
    return out


def renderer_streams(rows, t0):
    """{pid: its wake times} — a renderer entry's archetype is one renderer (9.8 D14), each renderer measured one stream."""
    out = {}
    for r in rows:
        out.setdefault(r.pid, []).append(r.t_in - t0)
    return {pid: sorted(ts) for pid, ts in out.items()}


def _entry(arch, app, phase, measured, components, jobs=None):
    compiled = {k: (span, compiled_times(components, span, seed=k)) for k, (span, _) in measured.items()}
    out = {"archetype": arch, "app": app, "phase": phase, **read_entry(measured, compiled)}
    if jobs is not None:
        out["jobs"] = jobs
    return out


def _library():
    import yaml
    from meas import control_report as cr
    return yaml.safe_load(open(os.path.join(cr.REPO, "dataset", "archetypes.yaml")))["archetypes"]


def desktop_entries(root, apps=()):
    """9.8's four entries over their carried phase (desktop/fold_in.CARRIED): the rows the analyzer keeps; a renderer
    entry's renderers each a stream."""
    from meas import control_report as cr
    from meas.desktop import analyze as a98
    from meas.desktop.fold_in import CARRIED, IDS
    pooled, lib, out = json.load(open(cr.POOL_98)), _library(), {}
    for app in apps or sorted(CARRIED):
        run, phase = pooled["runs"][app], CARRIED[app]
        measured = {}
        for rep in run["repeats"]:
            D = artifact_dir(root, app, rep, run["run_id"][str(rep)], run.get("mode") or "full")
            ph = a98.analyze_phase(D, phase, app, keep_rows=True)
            if app in a98.RENDERER_APPS:
                for pid, ts in renderer_streams(ph["_rows"], ph["t0"]).items():
                    measured[f"{rep}/{pid}"] = (ph["span_s"], ts)
            else:
                measured[str(rep)] = (ph["span_s"], sorted(r.t_in - ph["t0"] for r in ph["_rows"]))
            print(f"{app} r{rep}: {len(ph['_rows'])} wakes over {ph['span_s']:.0f} s", file=sys.stderr)
        out[IDS[app]] = _entry(IDS[app], app, phase, measured, lib[IDS[app]]["params"]["components"],
                               jobs=len(run["repeats"]) if app in a98.RENDERER_APPS else None)
    return out


def session_entries(root, apps=()):
    """9.9's four entries over the steady phase: each entry's rows after D23 and D27 take theirs out."""
    from meas import control_report as cr
    from meas.session import analyze as a99
    from meas.session.fold_in import IDS, PHASE
    run, lib = json.load(open(cr.POOL_99))["runs"]["session"], _library()
    measured = {e: {} for e in IDS}
    for rep in run["repeats"]:
        D = artifact_dir(root, "session", rep, run["run_id"][str(rep)], run.get("mode") or "full")
        report = json.load(open(os.path.join(D, "report.json")))
        ph = a99.analyze_phase(D, PHASE, int(report.get("pin.load_cpu") or 0), keep_rows=True)
        for e in IDS:
            measured[e][str(rep)] = (ph["span_s"], sorted(r.t_in - ph["t0"] for r in ph["entries"][e]["_rows_kept"]))
        print(f"session r{rep}: over {ph['span_s']:.0f} s", file=sys.stderr)
    return {IDS[e]: _entry(IDS[e], "session", PHASE, measured[e], lib[IDS[e]]["params"]["components"])
            for e in IDS if not apps or e in apps}


def campaign_entries(root, apps=IDLE_95):
    """9.5's idle entries over the pooled record the fold-in reads for their idle phase (control_report.POOL_95, D80)."""
    from meas import control_report as cr
    lib, out = _library(), {}
    for app in apps:
        arch = cr.ARCH_95[app]
        pooled = json.load(open(os.path.join(cr.IDLE_FROM_95.get(app, cr.POOL_95[app]), f"pool-{app}.json")))
        out[arch] = _entry(arch, app, "idle", campaign_streams(app, pooled, root), lib[arch]["params"]["components"])
    return out


def _cell(s):
    f = lambda x: f"{x:.4g}"
    return "—" if s is None else f"{f(s['median'])} ({f(s['min'])}–{f(s['max'])})"


def render(record):
    lines = [f"# Compiled burstiness — {record['family']}", ""]
    for arch, r in record["archetypes"].items():
        w = r["wakes_per_s"]
        streams = (f"{r['repeats']} streams, one per renderer, over {r['jobs']} repeats" if r.get("jobs")
                   else f"{r['repeats']} repeats")
        lines += [f"## {arch} (`{r['app']}`, {r['phase']})", "",
                  f"{streams}; wakes/s, median over the streams: measured {w['measured']}, compiled "
                  f"{w['compiled']}. Dispersion (variance over mean of the wake counts per bin), median (least–largest) "
                  "over the streams; the ratio measured over compiled, per stream.", "",
                  "| bin | measured | compiled | measured / compiled |", "|---|---|---|---|"]
        for label in BINS:
            b = r["bins"][label]
            lines.append(f"| {label} | {_cell(b['measured'])} | {_cell(b['compiled'])} | {_cell(b['ratio'])} |")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=("campaign", "desktop", "session"))
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--md")
    ap.add_argument("--app", action="append", default=[], help="one app (9.9: one entry's program) only, repeatable")
    a = ap.parse_args()
    read = {"campaign": lambda: campaign_entries(a.artifacts, tuple(a.app) or IDLE_95),
            "desktop": lambda: desktop_entries(a.artifacts, tuple(a.app)),
            "session": lambda: session_entries(a.artifacts, tuple(a.app))}[a.family]
    record = {"family": a.family, "archetypes": read()}
    json.dump(record, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(record))


if __name__ == "__main__":
    main()
