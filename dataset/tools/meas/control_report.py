#!/usr/bin/env python3
"""The untraced control's report (_dev/docs/spec/jioh/task-9.5-untraced-control.md).

Every landed control job of a family through its adapter: each value's per-job ratios, untraced over traced, read as
9.7 D36 reads a check (decisions 11, 12), the shares of decisions 10, 22 and 23 beside them, the build census (decision
16) and, given the family's pool of the control's traced runs (pool.py --control), the workload check (decision 17).
A JSON record and a results page, per archetype.

control_report.py <campaign|desktop|session> <artifacts> <out.json> [--md PAGE] [--control-pool POOL.json]...
"""

import argparse
import glob
import json
import os
import re
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas import control  # noqa: E402

REPO = os.path.dirname(os.path.dirname(TOOLS))
RESEARCH = os.path.join(REPO, "_dev", "research", "jioh")
SAME = os.path.join(RESEARCH, "task-9.5-interactive-typing", "campaign", "results-same-machine")
REMEASURED = os.path.join(RESEARCH, "task-9.5-interactive-typing", "campaign", "results-re-measured")
# the pools the 9.5 fold-in reads (tests/test_meas.py POOLS_95): thunderbird-send's idle phase from the 43-repeat pool
POOL_95 = {**{a: SAME for a in ("gimp", "kdenlive", "mpv-audio", "mpv-video", "soffice")},
           **{a: REMEASURED for a in ("chrome", "code", "webrtc", "thunderbird-send")}}
IDLE_FROM_95 = {"thunderbird-send": SAME}
ARCH_95 = {"soffice": "office-writer", "code": "code-editor", "chrome": "web-browser", "thunderbird-send": "mail-client",
           "gimp": "image-editor", "kdenlive": "video-editor", "mpv-audio": "audio-player", "mpv-video": "video-player",
           "webrtc": "video-call"}
POOL_98 = os.path.join(RESEARCH, "task-9.8-browser-comms", "campaign", "results", "pooled.json")
POOL_99 = os.path.join(RESEARCH, "task-9.9-daemons-session", "campaign", "results", "pooled.json")
# the 9.8 subjects whose job records the build under its own key (a renderer's is `version`), and the name it goes by
VERSION_98 = {"chat-client": ("element.version", "Element "),
              "game-client": ("steam.buildid", "Steam client build ")}
# the notes' reading (decisions 2, 12, 20): 9.5's phases in campaign order, the others as they come
PHASES = ("idle", "driven", "op", "play")
QUANTITY = {"run mean (ms)": "run mean", "wakes/s": "wake rate", "gap mean (ms)": "gap mean"}
TREE = {"per-input run (ms)": "the per-input run", "CPU share": "the tree's CPU share",
        "operation duration mean (ms)": "the operation's duration mean"}
NUMBER = {3: "three", 4: "four", 5: "five", 6: "six"}
# lines stated beside an archetype's reading by 인지오's decisions (decision 17) — in its notes and on its page
NOTES_STATED = {
    "web-browser": ("The operation phase's second page-load pass wakes the network service's foreground pool "
                    "(`utility/ThreadPoolForeg`, in the residual since D84) about 40 % less than the first, which keeps "
                    "the residual's ratios from resolving. The difference sits in each pass's opening burst: the pool "
                    "wakes 417–556 times in the first pass's first page load and 149–162 times in the second pass's "
                    "second, and from the fourth page load on at 18.6 and 17.7 a second (D87)."),
    "chat-client": ("The second idle run wakes `Chrome_IOThread` and `Chrome_ChildIOT` about 3–4 % more than the first, "
                    "traced or not; the control ran Element 1.12.29, the carried pool 1.12.28."),
    "code-editor": ("The second idle run, 915–1815 s after the first began, differs from the first whichever is traced — the "
                    "main thread wakes about 7 % less and its runs are about 40 % shorter, the residual's about 70 % "
                    "shorter — which keeps those ratios from resolving; the first run holds VS Code's launch work, which "
                    "the carried idle values leave out (D83). Read from 200 s into each run as the carried values are, the "
                    "first run agrees with the carried pool, every value within 2.1 standard deviations of its spread, "
                    "and the second differs in the residual's run mean alone, about 35 % longer (0.060–0.066 against "
                    "0.046 ms)."),
    "image-editor": ("The driven runs start from the control's prelude (the image reverted, the pointer over the canvas), in "
                     "which the main thread wakes about 18 % less often with about 19 % longer runs than in the carried "
                     "pool at the same CPU share; the driven ratios are perf's effect in that state."),
    "mail-client": ("The operation phase's second send pass wakes `Socket Thread` about 22 % more and `TaskCon~ller` about "
                    "35 % less inside the sends than the first, which keeps `Socket Thread`'s wake rate and both of "
                    "`TaskCon~ller`'s ratios from resolving. The second pass continues a trend that runs through the "
                    "first: over the first pass's six 100 s windows `Socket Thread` wakes 638 → 838 a second and "
                    "`TaskCon~ller` 50.9 → 35.9, over the second's 842 → 963 and 34.5 → 23.1 (D87)."),
    "video-editor": ("The first preview render of each job's second operation run did not start (`kdenlive_render` never "
                     "appeared within 30 s), so that run's operation values rest on 25 renders against the first run's "
                     "26–27."),
}
# on the page only
PAGE_STATED = {
    "renderer-hidden": ("The workload check under the carried pool's selection, read by hand: the control's six repeats put "
                        "`ThreadPoolServi`, the slowest carried component, past the coverage cut (9.5 D16) into the "
                        "residual; under the carried selection `ThreadPoolServi`'s wake rate is 0.0056 against 0.0065 /s "
                        "(z −0.37) and its run mean 0.0197 against 0.0198 ms (z −0.07), the residual (`MemoryInfra`) "
                        "0.0034 against 0.0033 /s (z +0.10) and 0.193 against 0.188 ms (z +0.19) — no disagreement."),
}
VERSIONS_99 = {"gnome-shell": ("gnome-shell",), "pipewire": ("pipewire", "wireplumber"), "systemd": ("systemd",),
               "dbus-daemon": ("dbus-daemon",)}
NAME = {"campaign": re.compile(r"^meas-(?:interactive|playback)-(.+)-r(\d+)-control$"),
        "desktop": re.compile(r"^meas-desktop-(.+)-r(\d+)-control$"),
        "session": re.compile(r"^meas-session-(session)-r(\d+)-control$")}
MACHINE = "EPYC 7763"


def carried_95(app):
    p = json.load(open(os.path.join(POOL_95[app], f"pool-{app}.json")))
    e = dict(p["runs"][app], exclude_roles=p.get("exclude_roles") or [])
    if app in IDLE_FROM_95:
        e["phases"] = {**e["phases"], "idle": json.load(open(os.path.join(IDLE_FROM_95[app], f"pool-{app}.json")))["runs"][app]["phases"]["idle"]}
    return e


def find_jobs(family, root):
    """{app: {index or index@run: dir}} of the landed control jobs on the campaign's machine, gate open; a copy
    pool_runs.py --exclude moved to its pool's `-excluded` folder is not read."""
    found = {}
    for d in sorted(glob.glob(os.path.join(root, "**", "meas-*-control"), recursive=True)):
        if any(part.endswith("-excluded") for part in os.path.relpath(d, root).split(os.sep)):
            continue
        m = NAME[family].match(os.path.basename(d))
        if not m or not os.path.exists(os.path.join(d, "report.json")):
            continue
        rpt = json.load(open(os.path.join(d, "report.json")))
        if rpt.get("gate") not in (None, "open") or MACHINE not in (rpt.get("machine.model") or ""):
            continue
        run = os.path.basename(os.path.dirname(d))
        found.setdefault(m.group(1), {}).setdefault(int(m.group(2)), []).append((run, d))
    return {app: {k if len(ds) == 1 else f"{k}@{run}": d for k, ds in by.items() for run, d in ds} for app, by in found.items()}


def validity(D):
    """What would leave a control job out, one line each: the gate, a run's missing snapshot, two driven runs that
    replayed different counts, failed operations, a prelude that returned non-zero or left its dialog up after the
    focus (ctrlprelude logs, the 2026-09-27 dry runs). The screenshots are compared apart (prelude_screens)."""
    r = json.load(open(os.path.join(D, "report.json")))
    probs = []
    if r.get("gate") not in (None, "open"):
        probs.append(f"gate {r.get('gate')}")
    names = sorted({os.path.basename(p)[len("snap."):].rsplit(".", 2)[0] for p in glob.glob(os.path.join(D, "snap.*.*.json"))} - {"launch"})
    phases = sorted({n[:-len("-untraced")] if n.endswith("-untraced") else n for n in names})
    for ph in phases:
        for name in (ph, f"{ph}-untraced"):
            if not all(os.path.exists(os.path.join(D, f"snap.{name}.{e}.json")) for e in ("before", "after")):
                probs.append(f"{name}: a snapshot is missing")
    a, b = r.get("replay.sent"), r.get("replay_untraced.sent")
    if a is not None and b is not None and a != b:
        probs.append(f"driven: the two runs replayed {a} and {b} events")
    for count, ok, label in (("ops.count", "ops.rc0", "op"), ("ops_untraced.count", "ops_untraced.rc0", "op-untraced")):
        if r.get(count) is not None and int(r.get(ok) or 0) < int(r[count]):
            probs.append(f"{label}: {int(r[count]) - int(r.get(ok) or 0)} of {r[count]} operations failed")
    for k, v in sorted(r.items()):
        m = re.fullmatch(r"ctrlprelude\.(.+)\.rc", k)
        if m and str(v) != "0":
            probs.append(f"prelude {m.group(1)}: rc {v}")
    for log in sorted(glob.glob(os.path.join(D, "ctrlprelude.*.log"))):
        if "dialog-still-up-after-focus" in open(log).read():
            probs.append(f"prelude {os.path.basename(log)[len('ctrlprelude.'):-len('.log')]}: its dialog stayed up")
    return probs


def prelude_screens(D):
    """The box in which a job's two screenshots after its preludes differ, None when identical — for reading beside
    the designed state; needs PIL, and returns None without it."""
    shots = sorted(glob.glob(os.path.join(D, "after-ctrlprelude-*.png")))
    if len(shots) != 2:
        return None
    try:
        from PIL import Image, ImageChops
    except ImportError:
        return None
    a, b = (Image.open(x).convert("RGB") for x in shots)
    return ImageChops.difference(a, b).getbbox() if a.size == b.size else ("sizes", a.size, b.size)


def _adapter(family):
    if family == "campaign":
        from meas.campaign import control as c
        return (lambda D, app, carried: c.job_values(D, app, carried)), (lambda D, app, carried: c.shares(D, app, carried))
    if family == "desktop":
        from meas.desktop import control as c
        return (lambda D, app, carried: c.job_values(D, app, carried)), (lambda D, app, carried: c.shares(D, app, carried))
    from meas.session import control as c
    return (lambda D, app, carried: c.job_values(D, carried)), (lambda D, app, carried: c.shares(D, carried))


def _archetypes(family, app, names):
    """{archetype: [value names]} — 9.9's session carries four entries, the value names prefixed by the entry."""
    if family == "campaign":
        return {ARCH_95[app]: names}
    if family == "desktop":
        from meas.desktop.fold_in import IDS
        return {IDS[app]: names}
    from meas.session.fold_in import IDS
    out = {}
    for n in names:
        out.setdefault(IDS[n.split(" ", 1)[0]], []).append(n)
    return out


def _census(family, archetype, reports):
    if family == "session":
        from meas.session.fold_in import IDS
        entry = {v: k for k, v in IDS.items()}[archetype]
        ver = {k: ", ".join(f"{p} {r.get('version.' + p) or '?'}" for p in VERSIONS_99[entry]) for k, r in reports.items()}
    elif family == "desktop" and archetype in VERSION_98:
        key, name = VERSION_98[archetype]
        ver = {k: (name + r[key]) if r.get(key) else None for k, r in reports.items()}
    else:
        ver = {k: r.get("version") for k, r in reports.items()}
    by = {}
    for k, v in ver.items():
        by.setdefault((v or "?").strip(), []).append(k)
    return {v: sorted(ks, key=lambda x: int(str(x).split("@")[0])) for v, ks in by.items()}


def app_reports(family, app, jobs, carried, with_shares=True, control_pool=None):
    """{archetype: its report} for one app's landed control jobs `jobs` {index: dir}."""
    values_of, shares_of = _adapter(family)
    per, orders, reports, shares, checks = {}, {}, {}, {}, {}
    for k, D in sorted(jobs.items(), key=lambda kv: str(kv[0])):
        order, vals = values_of(D, app, carried)
        orders[k] = order
        reports[k] = json.load(open(os.path.join(D, "report.json")))
        checks[k] = {"problems": validity(D), "prelude_screens": prelude_screens(D)}
        for name, (t, u) in vals.items():
            per.setdefault(name, {})[k] = (order, t, u)
        if with_shares:
            for prefix, rec in shares_of(D, app, carried).items():
                shares.setdefault(prefix, []).append(rec)
    out = {}
    for arch, names in _archetypes(family, app, sorted(per)).items():
        values = {n: control.read(per[n]) for n in names}
        n_int = sum(1 for v in values.values() if v.get("interval"))
        rep = {"archetype": arch, "app": app, "jobs": len(jobs),
               "orders": {o: sum(1 for x in orders.values() if x == o) for o in sorted(set(orders.values()) - {None})},
               "builds": _census(family, arch, reports),
               "values": values, "intervals": n_int, "chance": round(0.05 * n_int, 1),
               "differences": sorted(n for n, v in values.items() if v.get("reading") == "difference"),
               "validity": {str(k): c for k, c in checks.items() if c["problems"] or c["prelude_screens"]},
               "shares": {p: _mean_shares(recs) for p, recs in shares.items() if any(n.startswith(p + " ") for n in names)}}
        if control_pool is not None:
            ctl = control_pool["runs"].get(app)
            if ctl:   # decision 17 over the archetype's own values: 9.9's session pool carries four entries
                q = {n for p in (carried, ctl) for n in ((p.get("stability") or {}).get("quantities") or {})}
                rep["workload"] = control.workload(carried, ctl, _archetypes(family, app, sorted(q)).get(arch, []))
            else:
                rep["workload"] = None
            rep["left_out"] = (ctl or {}).get("excluded_repeats") or {}
        rep["notes"] = control_notes(rep)
        out[arch] = rep
    return out


def _mean_shares(recs):
    """Each share's mean and largest value over the jobs."""
    out = {}
    for kind in ("exited", "left", "inside"):
        for i, what in ((0, "cpu"), (1, "wakes")):
            xs = [r[kind][i] for r in recs if r.get(kind) and r[kind][i] is not None]
            if xs:
                out[f"{kind} {what}"] = {"mean": round(statistics.fmean(xs), 4), "max": max(xs)}
    return out


def _fmt(x, nd=4):
    return "—" if x is None else f"{x:.{nd}f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x)


def control_notes(rep):
    """The archetype's control reading for its modeling_notes: the counts (decision 12), each difference by phase and
    component (decision 20), the operation phase read over the whole phase (decision 23), then its stated line."""
    n = rep["intervals"]
    s = (f"Untraced control (the 9.5 untraced-control spec): {NUMBER.get(rep['jobs'], rep['jobs'])} jobs each ran every "
         "carried phase twice, traced under `perf sched record` and untraced, read by the 95 % interval of the per-job "
         f"ratios, untraced over traced; {n} interval{'' if n == 1 else 's'} read, about {rep['chance']} differences by "
         "chance alone")
    if not rep["differences"]:
        s += ", none found."
    else:
        groups = {}
        for name in rep["differences"]:
            v = rep["values"][name]
            head, rest = name.split(" ", 1)
            phase = "steady" if rep["app"] == "session" else head   # a 9.9 value is named by its program, not its phase
            lo, hi = v["interval"]
            num = f"{v['per_repeat_mean']:.3f} ({lo:.3f}–{hi:.3f})"
            if rest in TREE:
                groups.setdefault(phase, {})[TREE[rest]] = [num]
            else:
                q = next(q for q in QUANTITY if rest.endswith(" " + q))
                groups.setdefault(phase, {}).setdefault(f"`{rest[:-len(q) - 1]}`", []).append(f"{QUANTITY[q]} {num}")
        parts = [("operation phase, over the whole phase" if ph == "op" else f"{ph} phase") + ": "
                 + ", ".join(f"{c} {' and '.join(qs)}" for c, qs in groups[ph].items())
                 for ph in sorted(groups, key=lambda p: PHASES.index(p) if p in PHASES else len(PHASES))]
        s += ". Perf's effect on the carried values, which stay the traced ones — " + "; ".join(parts) + "."
    if NOTES_STATED.get(rep.get("archetype")):
        s += " " + NOTES_STATED[rep["archetype"]]
    return s


def render(record):
    lines = [f"# Untraced control — {record['family']}", ""]
    for arch, r in record["archetypes"].items():
        orders = ", ".join(f"{n} {o}" for o, n in r["orders"].items())
        builds = "; ".join(f"{v} ({', '.join(map(str, ks))})" for v, ks in r["builds"].items())
        ops = any("inside cpu" in sh or "inside wakes" in sh for sh in r["shares"].values())   # decision 23
        lines += [f"## {arch} (`{r['app']}`)", "",
                  f"{r['jobs']} jobs ({orders}); builds: {builds}.",
                  f"{r['intervals']} intervals read; at 95 % chance alone gives about {r['chance']} differences; "
                  f"differences found: {len(r['differences'])}" + (f" ({', '.join(r['differences'])})." if r["differences"] else "."), "",
                  "| value | traced median | untraced median | medians' ratio | per-job mean | 95 % interval | reading | by order | n | exited (CPU, wakes) | left out (CPU, wakes) |"
                  + (" in the operation windows (CPU, wakes) |" if ops else ""),
                  "|---|---|---|---|---|---|---|---|---|---|---|" + ("---|" if ops else "")]
        for name, v in r["values"].items():
            prefix = name.rsplit(" wakes/s", 1)[0].rsplit(" run mean (ms)", 1)[0]
            sh = r["shares"].get(prefix) or {}
            pair = lambda kind: (f"{_fmt((sh.get(kind + ' cpu') or {}).get('mean'), 3)}, {_fmt((sh.get(kind + ' wakes') or {}).get('mean'), 3)}"
                                 if sh.get(kind + " cpu") or sh.get(kind + " wakes") else "—")
            iv = v.get("interval")
            lines.append(f"| {name} | {_fmt(v.get('a'))} | {_fmt(v.get('b'))} | {_fmt(v.get('ratio'))} | {_fmt(v.get('per_repeat_mean'))} | "
                         f"{(_fmt(iv[0]) + '–' + _fmt(iv[1])) if iv else '—'} | {v.get('reading') or '—'} | "
                         f"{'; '.join(f'{o.split()[0]} first {m}' for o, m in v.get('order_means', {}).items()) or '—'} | {v.get('n', 0)} | "
                         f"{pair('exited')} | {pair('left')} |" + (f" {pair('inside')} |" if ops else ""))
        if r.get("validity") or r.get("left_out"):
            lines.append("")
        for k, c in (r.get("validity") or {}).items():
            if c["problems"]:
                lines.append(f"- job {k}: " + "; ".join(c["problems"]))
            if c["prelude_screens"]:
                lines.append(f"- job {k}: the screenshots after its two preludes differ in {c['prelude_screens']}")
        for k, why in (r.get("left_out") or {}).items():
            lines.append(f"- left out of the control's pool: {k} — {why}")
        for text in (NOTES_STATED.get(arch), PAGE_STATED.get(arch)):
            if text:
                lines += ["", text]
        w = r.get("workload")
        if w:
            lines += ["", f"The traced runs against the carried pool (decision 17): largest |z| {w['max_abs_z']} over {len(w['z'])} values"
                      + (f"; only in the carried pool: {', '.join(w['only_carried'])}" if w["only_carried"] else "")
                      + (f"; only in the control's: {', '.join(w['only_control'])}" if w["only_control"] else "") + "."]
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("family", choices=("campaign", "desktop", "session"))
    ap.add_argument("artifacts"); ap.add_argument("out")
    ap.add_argument("--md"); ap.add_argument("--control-pool", action="append", default=[],
                                             help="a pool of the control's traced runs (pool.py --control); one per app, repeatable")
    a = ap.parse_args()
    ctl = {"runs": {k: v for p in a.control_pool for k, v in json.load(open(p))["runs"].items()}} if a.control_pool else None
    record = {"family": a.family, "archetypes": {}}
    for app, jobs in sorted(find_jobs(a.family, a.artifacts).items()):
        if a.family == "campaign":
            carried = carried_95(app)
        else:
            carried = json.load(open(POOL_98 if a.family == "desktop" else POOL_99))["runs"][app]
        record["archetypes"].update(app_reports(a.family, app, jobs, carried, control_pool=ctl))
    json.dump(record, open(a.out, "w"), indent=1)
    if a.md:
        open(a.md, "w").write(render(record))


if __name__ == "__main__":
    main()
