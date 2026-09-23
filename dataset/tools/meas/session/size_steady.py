#!/usr/bin/env python3
"""Size the steady phase of the 9.9 session campaign from the unpolled long-phase probes (changelog D19).

  size_steady.py <run-dir> [<run-dir> ...] [--margin 60] [--lengths 300,600,900,1200,1800,2700]
                 [--phase idle] [--no-components] [--json out.json]

Each run dir is one `probe` job's output. The probe's 10 s state polls stop at the steady edge (D19), so the
region a full job would carry is recorded with nothing polling it, and only that region is read here. The polls
write `CLOCK_MONOTONIC` in `poll.<phase>.jsonl` and `perf sched record -k CLOCK_MONOTONIC` wrote the trace on the
same clock, so the last poll places the cut inside the trace; `--margin` is what is dropped after it, and the
poll-tail table says whether that margin was enough.

Per entry and candidate length L:
  - `within`  — the clean region cut into non-overlapping windows of L, the spread across them, pooled over the
                runs: the part of the across-repeat spread the phase length controls (`desktop/window_spread.py`);
  - `between` — the spread across the runs' own means, which no phase length changes: a repeat redraws the
                runner, and this is what that costs;
  - `total`   — the two in quadrature, and `hw@5rep`, the 95 % half-width a five-repeat batch would show
                (t = 2.776 at 4 degrees of freedom), against the 5 % tolerance of the stability rule. The length
                is chosen on this column: where it stops falling, a longer phase buys nothing and repeats do.
  - `clean`   — the share of candidate windows with no foreign user-space schedule-in on the measured CPU. Under
                D12's absolute gate that was the share of launched jobs a length would keep; D20 replaced it with
                a bound on the share of the CPU that work took, which this tool prints per run so method §5 can
                state the bound beside what was observed.

And per component, the samples a window of L would hold for the gap and run tables it carries — method §6 puts
every one of them on the stability list, so a length that leaves a component a handful of samples per repeat
cannot hold.
"""
import argparse
import json
import math
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.session.analyze import ENTRIES, analyze_phase    # noqa: E402
from meas.desktop.window_spread import T95_4DF, windows    # noqa: E402

LENGTHS = (300, 600, 900, 1200, 1800, 2700)
BANDS = ((-120, 0), (0, 30), (30, 60), (60, 120), (120, 300), (300, 900))   # the poll-tail check, around the cut


def polls_of(D, phase):
    p = os.path.join(D, f"poll.{phase}.jsonl")
    if not os.path.exists(p):
        return None
    t = [json.loads(ln)["mono_ns"] / 1e9 for ln in open(p) if ln.strip()]
    return (t[0], t[-1], len(t)) if t else None


def read_run(D, margin, phase, components=True):
    """One probe job: the phase whole (slices and the foreign counts), and its components past the last poll."""
    report = json.load(open(os.path.join(D, "report.json")))
    meas_cpu = int(report.get("pin.load_cpu") or 0)
    full = analyze_phase(D, phase, meas_cpu)
    if full.get("missing"):
        raise SystemExit(f"{D}: {phase} not readable ({full.get('why', 'no trace')})")
    t0, t1 = full["t0"], full["t0"] + full["span_s"]
    pol = polls_of(D, phase)
    if pol:
        first, last, n = pol
        if not t0 <= last < t1:
            raise SystemExit(f"{D}: the polls ({first:.3f}-{last:.3f}) do not fall in the trace "
                             f"[{t0:.3f}, {t1:.3f}] — they are not on the trace's clock, so no cut can be placed")
        cut, polls = last + margin, {"n": n, "first_s": round(first - t0, 1), "last_s": round(last - t0, 1)}
    else:
        cut, polls = t0, None                    # an unpolled phase is clean whole
    clean = analyze_phase(D, phase, meas_cpu, from_mono=cut) if components else None
    src = clean or full                      # the clean region's own foreign counts where they were computed
    fu, fo = src["foreign"]["user"], src["foreign"]["in_unit_other"]
    span = src["span_s"]
    foreign = {"schedule_ins": fu["schedule_ins"] + fo["schedule_ins"],
               "cpu_ms": round(fu["cpu_ms"] + fo["cpu_ms"], 1),
               "share_of_phase": (fu["cpu_ms"] + fo["cpu_ms"]) / 1000.0 / max(span, 1e-9),
               "by_comm": dict(sorted({**fu["by_comm"], **fo["by_comm"]}.items(),
                                      key=lambda kv: -kv[1]["cpu_ms"])[:8]),
               "over": span, "kernel_schedule_ins": src["foreign"]["kernel"]["schedule_ins"]}
    return {"dir": D, "repeat": report.get("repeat"), "mode": report.get("mode"), "gate": report.get("gate"),
            "cut_s": round(cut - t0, 1), "span_s": full["span_s"], "clean_span_s": round(t1 - cut, 1),
            "polls": polls, "foreign": foreign, "full": full, "clean": clean}


def _after_cut(series, slice_s, cut_s):
    return series[int(math.ceil(cut_s / slice_s)):]


def series_of(run, entry):
    sl = run["full"]["entries"][entry]["slices"]
    return _after_cut(sl["wakes_per_s"], sl["slice_s"], run["cut_s"]), sl["slice_s"]


def sd_pct(vals):
    m = statistics.fmean(vals) if vals else 0.0
    return statistics.stdev(vals) / m * 100 if len(vals) > 1 and m else None


def clean_share(runs, length_s):
    """The share of non-overlapping windows of L with no foreign user-space schedule-in (D12's gate)."""
    kept = total = 0
    for r in runs:
        f = r["full"]["foreign"]["user"]
        per = _after_cut(f["per_slice"], 10.0, r["cut_s"])
        k = int(length_s // 10.0)
        if not k:
            continue
        for i in range(0, len(per) - k + 1, k):
            total += 1
            kept += not sum(per[i:i + k])
    return kept / total if total else None


def entry_report(runs, entry, lengths):
    per_run = []
    for r in runs:
        vals, step = series_of(r, entry)
        per_run.append({"repeat": r["repeat"], "vals": vals, "step": step,
                        "mean": statistics.fmean(vals) if vals else 0.0})
    means = [p["mean"] for p in per_run if p["mean"]]
    between = sd_pct(means)
    rows = []
    for L in lengths:
        sds, nw = [], 0
        for p in per_run:
            w = windows(p["vals"], p["step"], L)
            s = sd_pct(w)
            if s is not None:
                sds.append(s)
                nw += len(w)
        within = math.sqrt(statistics.fmean([s * s for s in sds])) if sds else None
        # no total without the within part: a length whose windows are too few to spread is unread, not clean
        tot = math.sqrt(within ** 2 + (between or 0.0) ** 2) if within is not None else None
        rows.append({"length_s": L, "windows": nw, "within_sd_pct": within, "between_sd_pct": between,
                     "total_sd_pct": tot, "hw5_pct": T95_4DF * tot / 5 ** 0.5 if tot else None,
                     "clean_share": clean_share(runs, L)})
    return {"entry": entry, "mean_wakes_per_s": statistics.fmean(means) if means else 0.0,
            "runs": [{"repeat": p["repeat"], "mean_wakes_per_s": p["mean"]} for p in per_run],
            "between_sd_pct": between, "lengths": rows}


def component_yield(runs, entry, lengths):
    """Samples a window of L would hold, per component, averaged over the runs: wakes, and the gap and run tables."""
    acc = {}
    for r in runs:
        clean = r["clean"]
        if not clean:
            continue
        span = clean["span_s"]
        for key, c in clean["entries"][entry]["threads"].items():
            a = acc.setdefault(key, {"wakes_per_s": [], "gaps_per_s": [], "runs_per_s": []})
            a["wakes_per_s"].append(c["wakes_per_s"])
            a["gaps_per_s"].append(c["gap_ms"]["n"] / span)
            a["runs_per_s"].append(c["run_ms"]["n"] / span)
    return [{"component": k,
             "wakes_per_s": statistics.fmean(v["wakes_per_s"]),
             "per_window": {L: {"gaps": statistics.fmean(v["gaps_per_s"]) * L,
                                "runs": statistics.fmean(v["runs_per_s"]) * L} for L in lengths}}
            for k, v in sorted(acc.items(), key=lambda kv: -statistics.fmean(kv[1]["wakes_per_s"]))]


def poll_tail(runs, entry):
    """Wake rate in bands around the cut: the polls' disturbance is over when the bands past it agree."""
    out = []
    for lo, hi in BANDS:
        vals = []
        for r in runs:
            sl = r["full"]["entries"][entry]["slices"]
            step = sl["slice_s"]
            origin = r["polls"]["last_s"] if r["polls"] else 0.0        # the last poll, in phase seconds
            a, b = int((origin + lo) // step), int((origin + hi) // step)
            part = sl["wakes_per_s"][max(a, 0):max(b, 0)]
            if part:
                vals.append(statistics.fmean(part))
        out.append({"from_s": lo, "to_s": hi, "wakes_per_s": statistics.fmean(vals) if vals else None})
    return out


def report(dirs, margin=60.0, lengths=LENGTHS, phase="idle", components=True):
    runs = [read_run(d, margin, phase, components) for d in dirs]
    for r in runs:
        p = r["polls"]
        print(f"{os.path.basename(r['dir'])}  repeat {r['repeat']} {r['mode']} gate {r['gate']}: {phase} "
              f"{r['span_s']:.0f}s"
              + (f", {p['n']} polls ({p['first_s']:.0f}-{p['last_s']:.0f}s)" if p else ", unpolled")
              + f", cut at {r['cut_s']:.0f}s, clean {r['clean_span_s']:.0f}s")
        g = r["foreign"]
        top = ", ".join(f"{c} {v['cpu_ms']:.0f}ms" for c, v in list(g["by_comm"].items())[:5])
        print(f"    foreign user work on the measured CPU (D20): {g['schedule_ins']} schedule-ins, "
              f"{g['cpu_ms']:.0f} ms over {g['over']:.0f}s = {g['share_of_phase'] * 100:.4f}% of the CPU"
              + (f"   [{top}]" if top else ""))
    res = {"runs": [{k: r[k] for k in ("dir", "repeat", "mode", "gate", "cut_s", "span_s", "clean_span_s",
                                       "polls", "foreign")} for r in runs], "margin_s": margin, "entries": {}}
    for e in ENTRIES:
        ent = entry_report(runs, e, lengths)
        ent["poll_tail"] = poll_tail(runs, e)
        ent["components"] = component_yield(runs, e, lengths) if components else []
        res["entries"][e] = ent
        print(f"\n{e}: {ent['mean_wakes_per_s']:.3f} wakes/s over {len(runs)} run(s)"
              + (f", between-run sd {ent['between_sd_pct']:.1f}%" if ent["between_sd_pct"] is not None else "")
              + "   [" + "  ".join(f"r{r['repeat']} {r['mean_wakes_per_s']:.3f}" for r in ent["runs"]) + "]")
        print("   past the last poll: " + "  ".join(
            f"{b['from_s']}..{b['to_s']}s {b['wakes_per_s']:.2f}" for b in ent["poll_tail"] if b["wakes_per_s"] is not None))
        print(f"   {'length':>7}  {'windows':>7}  {'within':>7}  {'between':>7}  {'total':>7}  {'hw@5rep':>7}  {'clean':>6}")
        for row in ent["lengths"]:
            f = lambda k: f"{row[k]:.1f}%" if row[k] is not None else "-"     # noqa: E731
            print(f"   {row['length_s']:>6}s  {row['windows']:>7}  {f('within_sd_pct'):>7}  {f('between_sd_pct'):>7}"
                  f"  {f('total_sd_pct'):>7}  {f('hw5_pct'):>7}"
                  + (f"  {row['clean_share'] * 100:>5.0f}%" if row["clean_share"] is not None else "      -"))
        for c in ent["components"]:
            print(f"     {c['component']:<34} {c['wakes_per_s']:>7.3f}/s  " + "  ".join(
                f"{L}s: {c['per_window'][L]['gaps']:.0f} gaps/{c['per_window'][L]['runs']:.0f} runs" for L in lengths))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", nargs="+")
    ap.add_argument("--margin", type=float, default=60.0)
    ap.add_argument("--lengths", default=",".join(str(x) for x in LENGTHS))
    ap.add_argument("--phase", default="idle")
    ap.add_argument("--no-components", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    res = report(a.run_dir, a.margin, tuple(int(x) for x in a.lengths.split(",")), a.phase, not a.no_components)
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
