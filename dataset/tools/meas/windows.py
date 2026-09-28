#!/usr/bin/env python3
"""Each carried phase read in time windows (the 2026-09-28 review of 9.5–9.9). Per carried component, and for the
phase whole, the wake rate, the run mean and the CPU in each whole window of the phase, pooled over the carried
repeats — a window's rows over the repeats' time in it. A phase's carried values are means over the whole phase; where
the phase does part of its work only in part of it — launch work (9.5 D34, D83), work after a harness step or past the
steady edge — the windows show where. Rows are the ones the pool reads: a heavy event's runs apart (9.5 D64, 9.8 D33),
a session entry's wakes owed to causes outside the desktop out (9.9 D23, D27). A component the library does not carry
is read as the residual. A JSON record and a results page, per archetype.

windows.py <campaign|desktop|session> <artifacts> <out.json> [--md PAGE] [--app APP]...
"""

import argparse
import json
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

WIN_S = 100.0           # design: a phase of 600 s or more reads six or more windows
SHORT_WIN_S = 20.0      # a phase under 300 s (9.5's 120 s idle phases, D45) reads 20 s windows
# the 9.5 entries and the phase each carries: the idle entries' components, the periodic entries' play phase
PHASES_95 = (("soffice", "idle"), ("code", "idle"), ("chrome", "idle"), ("thunderbird-send", "idle"),
             ("kdenlive", "idle"), ("mpv-video", "play"), ("mpv-audio", "play"), ("webrtc", "play"))


def window_of(span):
    return WIN_S if span >= 3 * WIN_S else SHORT_WIN_S


def read(rows, t0, span, win):
    """rows: (name, t_in, run_ms). {window index: {name: [wakes, run ms]}} over the phase's whole windows, each row in
    the window its schedule-in falls in, and under "ALL" too."""
    n = int(span // win)
    out = {}
    for name, t, run in rows:
        k = int((t - t0) // win)
        if 0 <= k < n:
            for key in (name, "ALL"):
                c = out.setdefault(k, {}).setdefault(key, [0, 0.0])
                c[0] += 1
                c[1] += run
    return n, out


def pool(readings, win):
    """readings: [(n windows, {k: {name: [wakes, run]}})] one per repeat. Per name, per window over every repeat that
    holds the window whole: wakes/s, run mean (ms), CPU (ms of run per s)."""
    nwin = min(n for n, _ in readings)
    names = sorted({name for _, w in readings for k in w for name in w[k]}, key=lambda x: (x != "ALL", x))
    out = {}
    for name in names:
        rate, run_mean, cpu = [], [], []
        for k in range(nwin):
            wakes = sum(w.get(k, {}).get(name, [0, 0.0])[0] for _, w in readings)
            run = sum(w.get(k, {}).get(name, [0, 0.0])[1] for _, w in readings)
            t = win * len(readings)
            rate.append(wakes / t)
            run_mean.append(run / wakes if wakes else None)
            cpu.append(run / t)
        out[name] = {"wakes_per_s": rate, "run_mean_ms": run_mean, "cpu_ms_per_s": cpu}
    return {"repeats": len(readings), "win_s": win, "windows": nwin, "components": out}


def shares(entry):
    """Per component: its share of the phase's CPU, and the CPU its windows hold above its median window, as a share
    of the phase's CPU — the part of the phase's mean a window of the component's own typical level would not hold."""
    comps = entry["components"]
    total = sum(comps["ALL"]["cpu_ms_per_s"]) or 0.0
    out = {}
    for name, c in comps.items():
        cpu = c["cpu_ms_per_s"]
        med = statistics.median(cpu) if cpu else 0.0
        out[name] = {"share_of_cpu": sum(cpu) / total if total else None,
                     "above_median_window": sum(max(0.0, x - med) for x in cpu) / total if total else None}
    return out


def _entry(arch, app, phase, readings, win):
    e = pool(readings, win)
    e.update({"archetype": arch, "app": app, "phase": phase})
    e["shares"] = shares(e)
    return e


def _library():
    import yaml
    from meas import control_report as cr
    return yaml.safe_load(open(os.path.join(cr.REPO, "dataset", "archetypes.yaml")))["archetypes"]


def campaign_entries(root, apps=()):
    """9.5: the pooled record the fold-in reads for each phase (control_report.POOL_95, IDLE_FROM_95), analysed with
    the pool's settings; components named as the pool names them (9.5 D67), the library's carried ones kept."""
    from meas import burstiness as b, control_report as cr
    from meas.campaign.analyze import analyze_run, component_name
    cp = b._campaign_pool_module()
    lib, out = _library(), {}
    for app, phase in PHASES_95:
        if apps and app not in apps:
            continue
        arch = cr.ARCH_95[app]
        src = cr.IDLE_FROM_95.get(app, cr.POOL_95[app]) if phase == "idle" else cr.POOL_95[app]
        pooled = json.load(open(os.path.join(src, f"pool-{app}.json")))
        run = pooled["runs"][app]
        carried = [c["comm"] for c in lib[arch]["params"].get("components") or [] if c["comm"] != "residual"]
        if not carried:   # a periodic entry carries its cycles, not components: the pool's selection names them
            carried = [c for c in (run["phases"][phase].get("components") or {}).get("selected") or []]
        readings, win = [], None
        for rep in run["repeats"]:
            D = b.artifact_dir(root, app, rep, run["run_id"][str(rep)])
            _, raw = analyze_run(D, pooled.get("w_ms", 5.0), pooled.get("cap_ms", 0.0),
                                 exclude_roles=tuple(pooled.get("exclude_roles") or ()),
                                 idle_from_s=run.get("idle_from_s", 0.0))
            pd = raw["phases"][phase]
            rows, _ = cp.split_events(app, phase, pd["rows"])
            win = win or window_of(pd["span"])
            named = []
            for r in rows:
                name = component_name(pd["roles"].get(r.pid, "main"), cp.component_key(app, r.comm))
                named.append((name if name in carried else "residual", r.t_in, r.run))
            readings.append(read(named, pd["t0"], pd["span"], win))
            print(f"{app} r{rep}", file=sys.stderr)
        out[arch] = _entry(arch, app, phase, readings, win)
    return out


def desktop_entries(root, apps=()):
    """9.8: each entry's carried phase (desktop/fold_in.CARRIED), the rows the analyzer keeps — a renderer entry's
    renderers together, so its rates are the renderers' sum."""
    from meas import burstiness as b, control_report as cr
    from meas.desktop import analyze as a98
    from meas.desktop.fold_in import CARRIED, IDS
    pooled, lib, out = json.load(open(cr.POOL_98)), _library(), {}
    for app in sorted(CARRIED):
        if apps and app not in apps:
            continue
        run, phase = pooled["runs"][app], CARRIED[app]
        carried = [c["comm"] for c in lib[IDS[app]]["params"]["components"] if c["comm"] != "residual"]
        readings, win = [], None
        for rep in run["repeats"]:
            D = b.artifact_dir(root, app, rep, run["run_id"][str(rep)], run.get("mode") or "full")
            ph = a98.analyze_phase(D, phase, app, keep_rows=True)
            win = win or window_of(ph["span_s"])
            named = [((r.comm if r.comm in carried else "residual"), r.t_in, r.run) for r in ph["_rows"]]
            readings.append(read(named, ph["t0"], ph["span_s"], win))
            print(f"{app} r{rep}", file=sys.stderr)
        out[IDS[app]] = _entry(IDS[app], app, phase, readings, win)
    return out


def session_entries(root, apps=()):
    """9.9: the steady phase, each entry's rows after D23 and D27 take theirs out, named `<instance>/<comm>`."""
    from meas import burstiness as b, control_report as cr
    from meas.session import analyze as a99
    from meas.session.fold_in import IDS, PHASE
    run = json.load(open(cr.POOL_99))["runs"]["session"]
    entries = [e for e in IDS if not apps or e in apps]
    readings, win = {e: [] for e in entries}, None
    for rep in run["repeats"]:
        D = b.artifact_dir(root, "session", rep, run["run_id"][str(rep)], run.get("mode") or "full")
        report = json.load(open(os.path.join(D, "report.json")))
        ph = a99.analyze_phase(D, PHASE, int(report.get("pin.load_cpu") or 0), keep_rows=True)
        win = win or window_of(ph["span_s"])
        for e in entries:
            en = ph["entries"][e]
            inst = {p: i for i, ps in en["instances"].items() for p in ps}
            named = [(f"{inst.get(r.pid, '?')}/{r.comm}", r.t_in, r.run) for r in en["_rows_kept"]]
            readings[e].append(read(named, ph["t0"], ph["span_s"], win))
        print(f"session r{rep}", file=sys.stderr)
    return {IDS[e]: _entry(IDS[e], "session", PHASE, readings[e], win) for e in entries}


def _f(x, nd=3):
    return "—" if x is None else f"{x:.{nd}f}"


def _pct(x):
    return "—" if x is None else f"{x * 100:.1f} %"


def render(record):
    lines = [f"# Carried phases in time windows — {record['family']}", ""]
    for arch, r in record["archetypes"].items():
        lines += [f"## {arch} (`{r['app']}`, {r['phase']})", "",
                  f"{r['repeats']} repeats, {r['windows']} whole windows of {r['win_s']:g} s. Per component, pooled over "
                  "the repeats: each window's wake rate over the component's mean over the windows, each window's run "
                  "mean (ms), its share of the phase's CPU, and the CPU its windows hold above its median window as a "
                  "share of the phase's CPU.", "",
                  "| component | wakes/s | wake rate per window, over its mean | run mean per window (ms) | share of CPU "
                  "| above its median window |", "|---|---|---|---|---|---|"]
        for name, c in r["components"].items():
            rate = c["wakes_per_s"]
            m = statistics.fmean(rate) if rate else 0.0
            s = r["shares"][name]
            lines.append(f"| `{name}` | {m:.4g} | " + " · ".join(_f(x / m if m else None, 2) for x in rate) + " | "
                         + " · ".join(_f(x) for x in c["run_mean_ms"]) + f" | {_pct(s['share_of_cpu'])} | "
                         f"{_pct(s['above_median_window'])} |")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=("campaign", "desktop", "session"))
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--md")
    ap.add_argument("--app", action="append", default=[], help="one app (9.9: one entry's program) only, repeatable")
    a = ap.parse_args()
    read_ = {"campaign": campaign_entries, "desktop": desktop_entries, "session": session_entries}[a.family]
    record = {"family": a.family, "archetypes": read_(a.artifacts, tuple(a.app))}
    json.dump(record, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(record))


if __name__ == "__main__":
    main()
