#!/usr/bin/env python3
"""Per-phase analysis of a 9.8 desktop run (changelog D13; method §5).

The component layer is imported, not copied. `campaign/analyze.py` computes the components of every other
Chrome measurement in this dataset, and the two renderer entries here are the other half of the archetype it
computed for `web-browser`: that archetype was pooled with `exclude_roles=("renderer",)` (9.5 D14) and these
entries keep the renderers and drop the rest. Computing the two halves with different code would put a montage
inside one application through the analysis rather than through the measurement.

What is NOT reused is `analyze_run`, whose phase loop is fixed to 9.5's names — `idle`, `driven`, `driven-alt`,
`play`, `op` — and would skip every phase this slice records. Phase discovery is local, as
`background/analyze.py`'s is.

  analyze.py <run-dir> [--json out.json] [--phase NAME ...]
"""

import argparse
import json
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.campaign.analyze import (   # noqa: E402  — the component layer, one definition for both halves
    dist, load_all_wakeups, load_rows, merge_resumes, per_role, per_thread, pid_roles,
)

# the renderer-only view: the inverse of the filter that pools `web-browser`. pid_roles returns exactly these
# six values, so naming the five that go is equivalent to keeping the one that stays, and it stays honest if a
# future Chromium adds a role — an unrecognised role arrives as "other" and is dropped.
KEEP_ROLE = "renderer"
RENDERER_APPS = ("chrome-hidden", "chrome-visible")
# Chrome's own renderers, which are not a page's. They carry --type=renderer and pid_roles therefore calls them
# renderers, but they belong to the browser — to `web-browser`, the other half of this application — and not to
# the entry that describes a page's renderer. The dry run of 2026-09-20 found two extension processes and one
# top-chrome WebUI renderer among eight, diluting the archetype. They are read from renderers.tsv, the whole
# command lines: --extension-process sits about 129 characters in, past the 120 the snapshot keeps.
NOT_PAGE_RENDERER = ("--extension-process", "--top-chrome-webui")


def page_renderers(D):
    """pids of the renderers that are a page's, from renderers.tsv; None when the run recorded no such file."""
    p = os.path.join(D, "renderers.tsv")
    if not os.path.exists(p):
        return None
    out, seen = set(), False
    for line in open(p):
        parts = line.rstrip("\n").split("\t", 1)
        if len(parts) != 2:
            continue
        seen = True
        if not any(f in parts[1] for f in NOT_PAGE_RENDERER):
            out.add(int(parts[0]))
    return out if seen else None


def renderer_components(rows, span_s):
    """The components of ONE renderer, with the renderer processes present pooled as samples of it.

    A job measures N renderers so that a throttled entry yields enough wakes to read (method §9: at one wake per
    minute per renderer, twelve renderers yield about twelve wakes a minute). `per_thread` keys by thread comm,
    and every renderer's main thread is `chrome`, its hang watcher `HangWatcher`, and so on — so applied to the
    whole tree it returns the SUM over N renderers, which is not what the archetype describes. It is therefore
    applied per renderer process, exactly as `web-browser` has it applied to its tree, and the results pooled:
    `wakes_per_s` is the mean over renderers with the per-renderer values kept beside it for the spread the
    stability rule reads, and the gap and run tables are `dist` over every renderer's samples together.
    """
    by_pid = {}
    for r in rows:
        by_pid.setdefault(r.pid, []).append(r)
    per = {pid: per_thread(rs, span_s) for pid, rs in by_pid.items()}
    out, samples = {}, {}
    for comm in sorted({c for p in per.values() for c in p}):
        inst = [p[comm] for p in per.values() if comm in p]
        gaps, runs = [], []
        for rs in by_pid.values():
            by_tid = {}
            for r in rs:
                if r.comm == comm:
                    by_tid.setdefault(r.tid, []).append(r)
            for trs in by_tid.values():
                gaps += [(b.t_in - a.t_in) * 1000 for a, b in zip(trs, trs[1:])]
                runs += [r.run for r in trs]
        rates = [i["wakes_per_s"] for i in inst]
        samples[comm] = {"gaps": gaps, "runs": runs,
                         "t_in": sorted(r.t_in for rs in by_pid.values() for r in rs if r.comm == comm),
                         # per renderer, so the pool can build the residual of ONE renderer (changelog D19)
                         "t_in_by_pid": {pid: sorted(r.t_in for r in rs if r.comm == comm)
                                         for pid, rs in by_pid.items() if any(r.comm == comm for r in rs)}}
        out[comm] = {"renderers": len(inst),
                     "threads": [i["threads"] for i in inst],
                     "wakes_per_s": round(statistics.fmean(rates), 3),
                     "wakes_per_s_per_renderer": rates,
                     "cpu_share": round(statistics.fmean([i["cpu_share"] for i in inst]), 5),
                     "gap_ms": dist(gaps), "run_ms": dist(runs)}
    return out, samples


def drop_control_tab(rows, span_s):
    """The hidden subject's control tab is the selected tab, so it stays visible to Blink and is never
    throttled, while the measured renderers fall to one wake a minute. It is the single fastest renderer, by
    construction exactly one, and the ratio to the next fastest is recorded so the pool can see whether the
    identification was clean rather than assume it. Returns (rows without it, a record of what was dropped)."""
    rates = {}
    for r in rows:
        rates[r.pid] = rates.get(r.pid, 0) + 1
    if len(rates) < 2:
        return rows, {"dropped": None, "reason": "fewer than two renderers"}
    ordered = sorted(rates, key=lambda p: -rates[p])
    control, nxt = ordered[0], ordered[1]
    ratio = (rates[control] / rates[nxt]) if rates[nxt] else None
    return ([r for r in rows if r.pid != control],
            {"dropped": control,
             "wakes_per_s": round(rates[control] / span_s, 3),
             "next_wakes_per_s": round(rates[nxt] / span_s, 3),
             "ratio_to_next": round(ratio, 2) if ratio else None})


def slice_profile(rows, t0, span_s, slice_s=10.0):
    """CPU ms per second and wakes per second per slice, as `campaign/slices.py` reports them for the long-phase
    probe (9.5 D35, D42) — the shape that tells launch work from behaviour that recurs.

    It is computed here rather than by that module because `slices.profile` goes through `campaign.analyze_run`,
    whose phase loop is fixed to 9.5's names, so it raises KeyError on every phase this slice records.
    """
    n = max(1, int(span_s // slice_s))
    cpu, wakes = [0.0] * n, [0] * n
    for r in rows:
        i = int((r.t_in - t0) // slice_s)
        if 0 <= i < n:
            cpu[i] += r.run
            wakes[i] += 1
    return {"slice_s": slice_s,
            "cpu_ms_per_s": [round(c / slice_s, 2) for c in cpu],
            "wakes_per_s": [round(w / slice_s, 2) for w in wakes]}


def phases_in(D):
    """Every phase with a timehist, in the order the run recorded them (edges.jsonl), else alphabetical."""
    have = set()
    for f in os.listdir(D):
        if f.startswith("perf.") and ".timehist.txt" in f:
            have.add(f.split(".")[1])
    order = []
    p = os.path.join(D, "edges.jsonl")
    if os.path.exists(p):
        for line in open(p):
            if not line.strip():
                continue
            name = json.loads(line).get("phase")
            if name in have and name not in order:
                order.append(name)
    return order + sorted(have - set(order))


def analyze_phase(D, phase, app):
    th = next((f"perf.{phase}.timehist.txt{s}" for s in (".gz", "")
               if os.path.exists(os.path.join(D, f"perf.{phase}.timehist.txt{s}"))), None)
    if not th:
        return {"missing": True}
    pids, ends = set(), []
    for snap in (f"snap.{phase}.before.json", f"snap.{phase}.after.json"):
        p = os.path.join(D, snap)
        if os.path.exists(p):
            here = {pr["pid"] for pr in json.load(open(p))["procs"]}
            pids |= here
            ends.append(here)
    whole_phase = set.intersection(*ends) if len(ends) == 2 else pids
    segments, (t0, t1), extra = load_rows(os.path.join(D, th), pids)
    span = max(t1 - t0, 1e-6)
    roles = pid_roles(D, phase)

    wk = os.path.join(D, f"perf.{phase}.wakeups.txt.gz")
    if not os.path.exists(wk):
        wk = os.path.join(D, f"perf.{phase}.wakeups.txt")
    wakeups = load_all_wakeups(wk, pids | set(extra)) if os.path.exists(wk) else {}
    segments, merged = merge_resumes(segments, wakeups)

    out = {"span_s": round(span, 3), "rows": len(segments), "resumes_merged": merged,
           "roles": per_role(segments, roles, span),
           "renderer_pids": sorted(p for p, r in roles.items() if r == KEEP_ROLE)}
    if app in RENDERER_APPS:
        kept = [r for r in segments if roles.get(r.pid, "main") == KEEP_ROLE]
        out["role_filter"] = f"kept {KEEP_ROLE} only"
        pages = page_renderers(D)
        if pages is not None:
            dropped = sorted({r.pid for r in kept} - pages)
            out["renderers_not_page"] = dropped
            kept = [r for r in kept if r.pid in pages]
            out["role_filter"] += ", browser's own renderers dropped"
    else:
        kept = segments
        out["role_filter"] = "none"
    out["per_pid_wakes_per_s"] = {str(p): round(sum(1 for r in kept if r.pid == p) / span, 3)
                                  for p in sorted({r.pid for r in kept})}
    if app in RENDERER_APPS:
        # A renderer is a sample of the phase only if it existed for the phase. One that died partway has its
        # wakes divided by the whole span, so its rate is understated and it drags the pooled mean down — in the
        # 2026-09-20 dry run two such renderers took the visible subject's mean from about 10.9 to 6.66.
        short = sorted({r.pid for r in kept} - whole_phase)
        out["renderers_part_phase"] = [{"pid": p, "wakes_per_s": out["per_pid_wakes_per_s"][str(p)]} for p in short]
        kept = [r for r in kept if r.pid in whole_phase]
    if app == "chrome-hidden":
        kept, out["control_tab"] = drop_control_tab(kept, span)
    out["wakes_per_s"] = round(len(kept) / span, 3)          # the whole measured set, a diagnostic
    out["cpu_share"] = round(sum(r.run for r in kept) / 1000 / span, 5)
    if app in RENDERER_APPS:
        # what the archetype carries: ONE renderer. The job measures N of them for sample count, so the headline
        # rate is per renderer, not the sum the phase total gives.
        n_rend = len({r.pid for r in kept})
        out["renderers_measured"] = n_rend
        out["wakes_per_s_per_renderer"] = round(out["wakes_per_s"] / n_rend, 4) if n_rend else None
        out["cpu_share_per_renderer"] = round(out["cpu_share"] / n_rend, 6) if n_rend else None
    out["slices"] = slice_profile(kept, t0, span)
    # one renderer's components, the renderers present pooled as its samples
    if app in RENDERER_APPS:
        out["threads"], out["_samples"] = renderer_components(kept, span)
    else:
        out["threads"] = per_thread(kept, span)
        out["_samples"] = {}
        for comm in out["threads"]:
            rs = [r for r in kept if r.comm == comm]
            by_tid = {}
            for r in rs:
                by_tid.setdefault(r.tid, []).append(r)
            out["_samples"][comm] = {
                "gaps": [(b.t_in - a.t_in) * 1000 for trs in by_tid.values() for a, b in zip(trs, trs[1:])],
                "runs": [r.run for r in rs], "t_in": sorted(r.t_in for r in rs)}
    return out


def analyze_run_dir(D, only=()):
    report = json.load(open(os.path.join(D, "report.json")))
    app = report.get("app")
    res = {"run_dir": D, "app": app, "repeat": report.get("repeat"), "mode": report.get("mode"),
           "gate": report.get("gate"), "renderers_observed": report.get("renderers.observed"),
           "origins": report.get("settings.origins"), "timer_ms": report.get("settings.timer_ms"),
           "phases": {}}
    for phase in phases_in(D):
        if only and phase not in only:
            continue
        res["phases"][phase] = analyze_phase(D, phase, app)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--phase", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    res = analyze_run_dir(a.run_dir, tuple(a.phase))
    for ph in res["phases"].values():        # the sample lists are for the pool, not for the printed record
        ph.pop("_samples", None)
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    for name, ph in res["phases"].items():
        if ph.get("missing"):
            print(f"{name}: missing")
            continue
        print(f"{name}: span {ph['span_s']}s  wakes/s {ph['wakes_per_s']}  cpu_share {ph['cpu_share']}  "
              f"comms {len(ph['threads'])}  renderers {len(ph['renderer_pids'])}")


if __name__ == "__main__":
    main()
