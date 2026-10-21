#!/usr/bin/env python3
"""The 9.5–9.8 section's bound-only values that a removal can move other than by the run it removes, recomputed: each
pooled repeat read as `meas/campaign/pool.py` reads it (`analyze_run` at the pool's settings; census_campaign.py's
tree and tracer), every wake of the phase's tree traced by `chain_roots.RootTracer` (census_core's rules and classes),
and the value read again with the outside-cause wakes' segments taken out — every outside-cause wake (the rule as
written) and only those whose own wakeup row names the outside waker (direct.py's reading; the inherited put back).

- The per-input run (`input_run`, the driven phase under SWELL-KW): each input's window run net of the idle phase's CPU
  rate over the window, bounded below by zero (9.5 D13; `analyze._analyze`). The idle rate is the idle phase's whole
  tree run over its span, so removing the idle phase's outside-cause wakes lowers the rate and raises every window's
  net run — a move the run-share bound (effect_extra.py), which reads the driven phase's removed run alone, leaves
  out. Read four ways: both phases' removals (the rule as written), the idle phase's alone, the driven phase's alone,
  and both direct only.
- The playback cycle work and period (`cycle_run`, `period`; pool.cycle_windows, 9.5 D75): a cycle starts at a wake of
  the reference thread, so removing a reference wake that starts a cycle merges two cycles — the cycle count falls,
  the period rises and the work per cycle rises — a move the bound, which holds the cycles fixed, leaves out.
- `page-load` (the web-browser's operation): its components classified in the census's order and again with every
  wake of the phase traced first in time order (census_bg910.py's `--warm`), for the wakes the census keeps as
  `unknown: chain too deep`.

  python3 -I census_recompute95.py <app> <pool json> <out.json> <extracted dir> [<extracted dir> ...] [--only k,k]

<app>: soffice | code | thunderbird-send | chrome | mpv-video | mpv-audio | webrtc. A repeat already in the output is
skipped; the output is written after each repeat.
"""

import bisect
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402
import chain_roots as cr  # noqa: E402
import census_bg910 as b910  # noqa: E402
sys.path.insert(0, os.path.join(cc.TOOLS, "meas", "campaign"))
from analyze import analyze_run, component_name, HARNESS_COMMS  # noqa: E402
import pool as cp  # noqa: E402
import census_campaign as ccmp  # noqa: E402

NAME = re.compile(r"^meas-(interactive|playback)-(.+)-r(\d+)-(full|dry|idle)$")
INPUT = {"soffice": "office-writer", "code": "code-editor", "thunderbird-send": "mail-client", "chrome": "web-browser"}
CYCLE = {"mpv-video": "video-player", "mpv-audio": "audio-player", "webrtc": "video-call"}


def folders(roots, app):
    dirs = {}
    for root in roots:
        for d in sorted(glob.glob(os.path.join(root, "**", "meas-*"), recursive=True)):
            m = NAME.match(os.path.basename(d))
            if not m or m.group(2) != app or "-excluded" in d or not os.path.exists(os.path.join(d, "report.json")):
                continue
            k = int(m.group(3))
            if k in dirs:
                raise SystemExit(f"{app} r{k}: two folders {dirs[k]} {d}")
            dirs[k] = d
    return dirs


def tree_of(D, phase, res, pd):
    """census_campaign.py's tree: the snapshots' pids less the harness's, the transient children, every segment's pid."""
    ph = res["phases"][phase]
    snap_pids = set()
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p):
            snap_pids |= {pr["pid"] for pr in json.load(open(p))["procs"]
                          if pr.get("comm") not in HARNESS_COMMS and not pr.get("comm", "").startswith("llvmpipe-")}
    return snap_pids | {int(p) for p in ph.get("transient_pids", {})} | {r.pid for r in pd["segments"]}


def tracer(D, phase, res, pd):
    wk = os.path.join(D, f"perf.{phase}.wakeups.txt.gz")
    return cr.RootTracer(cc.load_wakeup_rows(wk), tree_of(D, phase, res, pd), cc.by_tid(pd["rows"]),
                         drivers=("python3", "xdotool") if phase in ("op", "driven") else ())


def drop(segments, rows, gone):
    """The phase's segments less those of the given wakes (each wake's segments: its thread's from its schedule-in to
    its end), in their own order."""
    if not gone:
        return segments
    per = collections.defaultdict(list)
    for r in rows:
        per[r.tid].append(r)
    for ws in per.values():
        ws.sort(key=lambda w: w.t_in)
    index = {tid: ([w.t_in for w in ws], ws) for tid, ws in per.items()}
    return b910.drop_segments(segments, gone, index)


def outside_sets(traced):
    rule = [x[0] for x in traced if x[1] == "outside"]
    direct = [x[0] for x in traced if x[1] == "outside" and x[6]]
    return {"rule": rule, "direct": direct}


def removed(ws):
    return {"n": len(ws), "run_ms": sum(w.run for w in ws)}


def windows(D, t0, t1, segments, idle_rate):
    """analyze._analyze's window rule (b) at the pool's settings (cap 0): per replayed input in the phase, the run of
    the segments starting in [s, next input) and that run net of the idle rate over the window, bounded below by 0."""
    sent = [json.loads(line) for line in open(os.path.join(D, "replay.jsonl")) if line.strip()]
    s_times = [e["sent_us"] / 1e6 for e in sent]
    t_in = [r.t_in for r in segments]
    run, corr, length = [], [], []
    for i, s in enumerate(s_times):
        if s < t0 or s > t1:
            continue
        nxt = s_times[i + 1] if i + 1 < len(s_times) else t1
        end = min(nxt, t1, nxt)
        a, b = bisect.bisect_left(t_in, s), bisect.bisect_left(t_in, end)
        x = sum(r.run for r in segments[a:b])
        run.append(x)
        length.append((end - s) * 1000)
        corr.append(max(0.0, x - idle_rate * (end - s) * 1000))
    return {"n": len(corr), "run_sum": sum(run), "corr_sum": sum(corr), "len_sum": sum(length),
            "clamped": sum(1 for c in corr if c == 0.0)}


def input_repeat(app, D):
    res, raw = analyze_run(D, 5.0, 0.0, idle_from_s=cp.IDLE_FROM_S.get(app, 0.0))
    out = {}
    if "driven" not in raw["phases"] or "per_input" not in res["phases"].get("driven", {}):
        return {"no_driven_phase": True, "values": {}}, res, raw
    pi_, pd_ = raw["phases"]["idle"], raw["phases"]["driven"]
    tri = tracer(D, "idle", res, pi_)
    ti = tri.trace(pi_["rows"])
    gi = outside_sets(ti)
    del tri
    trd = tracer(D, "driven", res, pd_)
    td = trd.trace(pd_["rows"])
    gd = outside_sets(td)
    del trd
    span_i = pi_["span"]
    t0, t1 = pd_["t0"], pd_["t0"] + pd_["span"]
    rate = {"base": sum(s.run for s in pi_["segments"]) / 1000 / span_i}
    seg_d = {"base": pd_["segments"]}
    for tag in ("rule", "direct"):
        rate[tag] = sum(s.run for s in drop(pi_["segments"], pi_["rows"], gi[tag])) / 1000 / span_i
        seg_d[tag] = drop(pd_["segments"], pd_["rows"], gd[tag])
    out["idle"] = {"span_s": span_i, "wakes": len(pi_["rows"]), "rate": rate,
                   "removed": {tag: removed(gi[tag]) for tag in gi},
                   "classes": dict(collections.Counter(x[1] for x in ti))}
    out["driven"] = {"wakes": len(pd_["rows"]), "removed": {tag: removed(gd[tag]) for tag in gd},
                     "classes": dict(collections.Counter(x[1] for x in td))}
    out["values"] = {"base": windows(D, t0, t1, seg_d["base"], rate["base"]),
                     "rule": windows(D, t0, t1, seg_d["rule"], rate["rule"]),
                     "rule_idle_only": windows(D, t0, t1, seg_d["base"], rate["rule"]),
                     "rule_driven_only": windows(D, t0, t1, seg_d["rule"], rate["base"]),
                     "direct": windows(D, t0, t1, seg_d["direct"], rate["direct"])}
    out["pooled_check"] = res["phases"]["driven"]["per_input"]["window"]["run_ms_minus_idle"]
    return out, res, raw


def cycle_repeat(app, D):
    res, raw = analyze_run(D, 5.0, 0.0, idle_from_s=cp.IDLE_FROM_S.get(app, 0.0))
    pd = raw["phases"]["play"]
    tr = tracer(D, "play", res, pd)
    traced = tr.trace(pd["rows"])
    del tr
    g = outside_sets(traced)
    roles = pd.get("roles") or {}
    ref_comm = cp.CYCLES[(app, "play")][0]
    is_ref = lambda r: component_name(roles.get(r.pid, "main"), cp.component_key(app, r.comm)) == ref_comm
    base = cp.cycle_windows(app, "play", pd["rows"], pd["segments"], roles)
    base_starts = set()
    out = {"wakes": len(pd["rows"]), "classes": dict(collections.Counter(x[1] for x in traced)), "values": {}}

    def summ(c):
        return {"n": len(c["work_ms"]), "work_sum": sum(c["work_ms"]), "length_sum": sum(c["length_ms"])}
    out["values"]["base"] = summ(base)
    # the reference's cycle starts, read as cycle_windows reads them, to tell which removed wakes started a cycle
    spec = cp.CYCLES[(app, "play")]

    def starts_of(rows):
        ref = sorted((r.t_in, r.run) for r in rows if is_ref(r))
        if spec[1] == "silence_ms":
            found = [t for i, (t, _) in enumerate(ref) if i == 0 or t - ref[i - 1][0] > spec[2] / 1000]
        else:
            found = [t for t, run in ref if run >= spec[2]]
        st = []
        for t in found:
            if not st or t - st[-1] >= spec[3] / 1000:
                st.append(t)
        return st
    base_list = starts_of(pd["rows"])
    base_starts = set(base_list)
    pos = {t: i for i, t in enumerate(base_list)}

    def gaps(t):
        """The base cycles on either side of a start, in ms: a start on the reference's own cadence has both near the
        period."""
        i = pos[t]
        return [round((t - base_list[i - 1]) * 1000, 3) if i > 0 else None,
                round((base_list[i + 1] - t) * 1000, 3) if i + 1 < len(base_list) else None]
    for tag in ("rule", "direct"):
        gone = g[tag]
        gone_set = {(w.tid, w.t_in) for w in gone}
        rows = [r for r in pd["rows"] if (r.tid, r.t_in) not in gone_set]
        segs = drop(pd["segments"], pd["rows"], gone)
        c = cp.cycle_windows(app, "play", rows, segs, roles)
        v = summ(c)
        ref_gone = [w for w in gone if is_ref(w)]
        v.update(removed=removed(gone), ref_removed=len(ref_gone),
                 ref_removed_starts=sum(1 for w in ref_gone if w.t_in in base_starts),
                 ref_removed_start_gaps=[gaps(w.t_in) for w in ref_gone if w.t_in in base_starts],
                 ref_removed_labels=dict(collections.Counter(
                     lab for (w, cls, lab, *_r) in traced if cls == "outside" and is_ref(w)
                     and (tag == "rule" or _r[3]))))
        out["values"][tag] = v
    out["pooled_check"] = {"n": len(base["work_ms"]), "work_mean": sum(base["work_ms"]) / max(len(base["work_ms"]), 1),
                           "length_mean": sum(base["length_ms"]) / max(len(base["length_ms"]), 1)}
    return out, res, raw


def op_tally(classified, name_of):
    out = {}
    for r, cls, lab, how, _root, _hops, direct in classified:
        c = out.setdefault(name_of(r), {"n": 0, "run": 0.0, "classes": {}, "labels": {},
                                        "split": {"direct": {"n": 0, "run": 0.0}, "inherited": {"n": 0, "run": 0.0}}})
        c["n"] += 1
        c["run"] += r.run
        k = c["classes"].setdefault(cls, {"n": 0, "run": 0.0})
        k["n"] += 1
        k["run"] += r.run
        if cls != "own":
            c["labels"][f"{cls}: {lab}"] = c["labels"].get(f"{cls}: {lab}", 0) + 1
        if cls == "outside":
            s = c["split"]["direct" if direct else "inherited"]
            s["n"] += 1
            s["run"] += r.run
    return out


def page_load(D, res, raw):
    """The operation's components as census_campaign.py tallies them, in the census's order and traced in time order."""
    pd = raw["phases"]["op"]
    op = pd["operation"]
    roles = pd.get("roles") or {}
    comps = ccmp.carried("web-browser", "operations.page-load.components")
    rows, events = cp.split_events("chrome", "op", op["inside"])
    span = (sum(op["durations_ms"]) / 1000 or 1e-6)

    def name_of(r):
        n = component_name(roles.get(r.pid, "main"), cp.component_key("chrome", r.comm))
        return n if n in comps else "residual"
    out = {}
    for order in ("census", "time"):
        tr = tracer(D, "op", res, pd)
        if order == "time":
            tr.trace(sorted(pd["rows"], key=lambda r: r.t_in))
        traced = tr.trace(rows)
        cold = None
        if order == "time":
            cold = out["census"]["_deep"]
            moved = collections.Counter()
            for (r, cls, lab, *_x) in traced:
                if (r.tid, r.t_in) in cold:
                    moved[f"{cls}: {lab}"] += 1
            out["deep_become"] = dict(moved.most_common())
        t = op_tally(traced, name_of)
        for c in t.values():
            c["span"] = span
        out[order] = {"tally": t, "deep": sum(1 for x in traced if x[2] == "chain too deep"),
                      "_deep": {(x[0].tid, x[0].t_in) for x in traced if x[2] == "chain too deep"}}
        del tr
    for order in ("census", "time"):
        out[order].pop("_deep")
    return out


def main():
    only = None
    if "--only" in sys.argv:
        i = sys.argv.index("--only")
        only = set(sys.argv[i + 1].split(","))
        del sys.argv[i:i + 2]
    app, pool_json, out_path, roots = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    reps = json.load(open(pool_json))["runs"][app]["repeats"]
    dirs = folders(roots, app)
    missing = [k for k in reps if k not in dirs]
    if missing:
        raise SystemExit(f"{app}: pooled repeats without a folder: {missing}")
    result = json.load(open(out_path)) if os.path.exists(out_path) else {}
    entry = INPUT.get(app) or CYCLE[app]
    sec = result.setdefault(entry, {"app": app, "field": "input_run" if app in INPUT else "cycle", "repeats": {}})
    for k in reps:
        if str(k) in sec["repeats"] or (only and str(k) not in only):
            continue
        D = dirs[k]
        if app in INPUT:
            o, res, raw = input_repeat(app, D)
            if app == "chrome":
                o["page_load"] = page_load(D, res, raw)
        else:
            o, res, raw = cycle_repeat(app, D)
        del res, raw
        o["dir"] = D
        sec["repeats"][str(k)] = o
        v = o["values"]
        if app in INPUT and not v:
            msg = "no driven phase"
        elif app in INPUT:
            msg = " ".join(f"{t} {v[t]['corr_sum'] / max(v[t]['n'], 1):.4f}" for t in v)
            msg += f"; idle removed {o['idle']['removed']['rule']['n']}, driven removed {o['driven']['removed']['rule']['n']}"
            if "page_load" in o:
                msg += f"; page-load deep {o['page_load']['census']['deep']} -> {o['page_load']['time']['deep']}"
        else:
            msg = " ".join(f"{t} n {v[t]['n']} period {v[t]['length_sum'] / max(v[t]['n'], 1):.5f} work "
                           f"{v[t]['work_sum'] / max(v[t]['n'], 1):.5f}" for t in v)
            msg += f"; ref removed {v['rule']['ref_removed']} (starts {v['rule']['ref_removed_starts']})"
        print(f"{entry} r{k}: {msg}", flush=True)
        json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
