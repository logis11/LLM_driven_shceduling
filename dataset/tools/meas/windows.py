#!/usr/bin/env python3
"""Each carried phase read in time windows (the 2026-09-28 review of 9.5–9.9). Per carried component, and for the
phase whole, the wake rate, the run mean and the CPU in each whole window of the phase, pooled over the carried
repeats — a window's rows over the repeats' time in it. A phase's carried values are means over the whole phase; where
the phase does part of its work only in part of it — launch work (9.5 D34, D83), work after a harness step or past the
steady edge — the windows show where. Rows are the ones the pool reads: a heavy event's runs apart (9.5 D64, 9.8 D33),
a session entry's wakes owed to causes outside the desktop out (9.9 D23, D27). A component the library does not carry
is read as the residual. An operation phase carries the rows inside its operations (9.5's operations, the pool's
`inside`), so it is read over the operations' time: each operation in the window its trigger falls in, and the
operations one by one in their order. A JSON record and a results page, per archetype.

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
# the 9.5 entries that carry an operation, read in the op phase
OPS_95 = ("chrome", "thunderbird-send", "gimp", "kdenlive")
BLOCKS = 10             # the page reads the operations in at most this many blocks of consecutive operations


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


def read_ops(rows, ops, t0, span, win):
    """rows: (name, t_in, run_ms) inside the operations; ops: the successful operations' (trigger, done) windows. By
    time: each operation, its rows and its length in the window its trigger falls in, whole windows only. By
    operation: the k-th operation a window of its own. Each (n windows, {k: {name: [wakes, run ms]}}, {k: seconds of
    operation})."""
    import bisect
    ops = sorted(ops)
    starts = [a for a, _ in ops]
    n = int(span // win)
    by_time, by_op = (n, {}, {}), (len(ops), {}, {})
    for j, (a, b) in enumerate(ops):
        k = int((a - t0) // win)
        if 0 <= k < n:
            by_time[2][k] = by_time[2].get(k, 0.0) + (b - a)
        by_op[2][j] = b - a
    for name, t, run in rows:
        j = bisect.bisect_right(starts, t) - 1
        if j < 0 or t >= ops[j][1]:
            continue
        k = int((ops[j][0] - t0) // win)
        for w, key in [(by_op[1], j)] + ([(by_time[1], k)] if 0 <= k < n else []):
            for nm in (name, "ALL"):
                c = w.setdefault(key, {}).setdefault(nm, [0, 0.0])
                c[0] += 1
                c[1] += run
    return by_time, by_op


def pool(readings, win):
    """readings: [(n windows, {k: {name: [wakes, run]}}[, {k: seconds}])] one per repeat. Per name, per window over
    every repeat that holds the window whole: wakes/s, run mean (ms), CPU (ms of run per s) — over the repeats' time in
    the window, or where a reading gives its seconds (an operation phase) over those; such an entry also keeps each
    window's seconds and each name's wakes and run, which `blocks` joins."""
    nwin = min(r[0] for r in readings)
    timed = any(len(r) > 2 for r in readings)
    secs = [sum((r[2].get(k, 0.0) if len(r) > 2 else win) for r in readings) for k in range(nwin)]
    names = sorted({name for r in readings for k in r[1] for name in r[1][k]}, key=lambda x: (x != "ALL", x))
    out = {}
    for name in names:
        wakes = [sum(r[1].get(k, {}).get(name, [0, 0.0])[0] for r in readings) for k in range(nwin)]
        run = [sum(r[1].get(k, {}).get(name, [0, 0.0])[1] for r in readings) for k in range(nwin)]
        out[name] = _rates(wakes, run, secs)
        if timed:
            out[name].update({"wakes": wakes, "run_ms": run})
    e = {"repeats": len(readings), "win_s": win, "windows": nwin, "components": out}
    if timed:
        e["time_s"] = secs
    return e


def _rates(wakes, run, secs):
    return {"wakes_per_s": [w / t if t else None for w, t in zip(wakes, secs)],
            "run_mean_ms": [r / w if w else None for r, w in zip(run, wakes)],
            "cpu_ms_per_s": [r / t if t else None for r, t in zip(run, secs)]}


def blocks(entry, size):
    """An operation entry's windows joined in blocks of `size` consecutive windows, each read over its seconds."""
    idx = [range(i, min(i + size, entry["windows"])) for i in range(0, entry["windows"], size)]
    secs = [sum(entry["time_s"][k] for k in ks) for ks in idx]
    comps = {name: _rates([sum(c["wakes"][k] for k in ks) for ks in idx], [sum(c["run_ms"][k] for k in ks) for ks in idx],
                          secs) for name, c in entry["components"].items()}
    return {"repeats": entry["repeats"], "windows": len(idx), "time_s": secs, "components": comps}


def shares(entry):
    """Per component: its share of the phase's CPU, and the CPU its windows hold above its median window, as a share
    of the phase's CPU — the part of the phase's mean a window of the component's own typical level would not hold."""
    comps = entry["components"]
    total = sum(x for x in comps["ALL"]["cpu_ms_per_s"] if x is not None) or 0.0
    out = {}
    for name, c in comps.items():
        cpu = [x for x in c["cpu_ms_per_s"] if x is not None]
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
    for app in OPS_95:
        if apps and app not in apps:
            continue
        arch = cr.ARCH_95[app]
        (op_name, op), = lib[arch]["params"]["operations"].items()
        pooled = json.load(open(os.path.join(cr.POOL_95[app], f"pool-{app}.json")))
        run = pooled["runs"][app]
        carried = [c["comm"] for c in op["components"] if c["comm"] != "residual"]
        by_time, by_op, win = [], [], None
        for rep in run["repeats"]:
            D = b.artifact_dir(root, app, rep, run["run_id"][str(rep)])
            _, raw = analyze_run(D, pooled.get("w_ms", 5.0), pooled.get("cap_ms", 0.0),
                                 exclude_roles=tuple(pooled.get("exclude_roles") or ()))
            pd = raw["phases"]["op"]
            rows, _ = cp.split_events(app, "op", pd["operation"]["inside"])
            win = win or window_of(pd["span"])
            named = []
            for r in rows:
                name = component_name(pd["roles"].get(r.pid, "main"), cp.component_key(app, r.comm))
                named.append((name if name in carried else "residual", r.t_in, r.run))
            t, o = read_ops(named, pd["operation"]["windows"], pd["t0"], pd["span"], win)
            by_time.append(t)
            by_op.append(o)
            print(f"{app} op r{rep}", file=sys.stderr)
        e = _entry(arch, app, "op", by_time, win)
        e.update({"operation": op_name, "by_operation": pool(by_op, None)})
        out[f"{arch}/{op_name}"] = e
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


def _table(r, per):
    rows = [f"| component | wakes/s | wake rate per {per}, over its mean | run mean per {per} (ms) | share of CPU "
            f"| above its median {per} |", "|---|---|---|---|---|---|"]
    sh = shares(r)
    for name, c in r["components"].items():
        rate = c["wakes_per_s"]
        known = [x for x in rate if x is not None]
        m = statistics.fmean(known) if known else 0.0
        s = sh[name]
        rows.append(f"| `{name}` | {m:.4g} | " + " · ".join(_f(x / m if m and x is not None else None, 2) for x in rate)
                    + " | " + " · ".join(_f(x) for x in c["run_mean_ms"]) + f" | {_pct(s['share_of_cpu'])} | "
                    f"{_pct(s['above_median_window'])} |")
    return rows


def _remainder(n, size):
    return f", the last block the remaining {n % size}" if n % size else ""


def render(record):
    lines = [f"# Carried phases in time windows — {record['family']}", ""]
    for arch, r in record["archetypes"].items():
        per = ("Per component, pooled over the repeats: each {0}'s wake rate over the component's mean over the {0}s, "
               "each {0}'s run mean (ms), its share of the phase's CPU, and the CPU its {0}s hold above its median {0} "
               "as a share of the phase's CPU.")
        if "operation" not in r:
            lines += [f"## {arch} (`{r['app']}`, {r['phase']})", "",
                      f"{r['repeats']} repeats, {r['windows']} whole windows of {r['win_s']:g} s. " + per.format("window"),
                      ""] + _table(r, "window") + [""]
            continue
        n = r["by_operation"]["windows"]
        size = -(-n // BLOCKS)
        lines += [f"## {arch.split('/')[0]} (`{r['app']}`, the `{r['operation']}` operation)", "",
                  f"{r['repeats']} repeats, {r['windows']} whole windows of {r['win_s']:g} s, each holding the operations "
                  "triggered in it, read over their time. " + per.format("window"), ""] + _table(r, "window") + [
                  "", f"By operation, in blocks of {size} ({n} operations a repeat{_remainder(n, size)}), each block read "
                  "over its operations' time. " + per.format("block"), ""] + _table(blocks(r["by_operation"], size), "block") + [""]
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
