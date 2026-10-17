#!/usr/bin/env python3
"""Does a failing component's value vary within one run, or between runs (changelog D28; 9.5 D57)?

  within_run.py <pooled.json> <probe-run-dir> [<probe-run-dir> ...] [--window 1800] [--step 60] [--margin 60]
                [--phase idle] [--component ENTRY:INSTANCE/COMM ...]

9.5 D57 carries a component whose values vary between sessions with its half-widths, in place of the tolerance,
once three findings place the spread: not the analysis — the same threads in every repeat; not the phase's
placement — a window of the phase's length slid along one long run moves the value far less than it moves across
repeats; and its weight — the share of the entry's wakes it holds. This reads all three for each component the
pooled record's rule does not hold on (or those named), under the cause rules the pool applied (D27).

The long runs are the unpolled region of the long-phase probes, from `--margin` seconds past the last poll (D19,
D22), read through `size_steady.read_run`. Spread is half the range over the mean, the measure 9.8 stated
(`desktop/within_run.py`): across the window positions of each probe, and across the pooled repeats' own values.
"""
import argparse
import json
import os
import statistics
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

from meas.session.size_steady import read_run   # noqa: E402

LABELS = ("wakes/s", "gap mean (ms)", "run mean (ms)")


def spread(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 2 or not statistics.fmean(vals):
        return None
    return (max(vals) - min(vals)) / 2 / statistics.fmean(vals)


def failing(pooled):
    out = []
    for key, q in pooled["stability"]["quantities"].items():
        if q["passes"]:
            continue
        entry, rest = key.split(" ", 1)
        comp = next(rest[:-len(lb) - 1] for lb in LABELS if rest.endswith(" " + lb))
        if (entry, comp) not in out:
            out.append((entry, comp))
    return out


def window_values(samples, t0, t1, window, step):
    """Per window position: (wakes/s, gap mean ms, run mean ms) of a single-thread component's kept wakes."""
    pairs = sorted(zip(samples["t_in"], samples["runs"]))
    out, start = [], t0
    while start + window <= t1 + 1e-6:
        w = [(t, r) for t, r in pairs if start <= t < start + window]
        ts = [t for t, _ in w]
        gaps = [(b - a) * 1000 for a, b in zip(ts, ts[1:])]
        out.append((len(w) / window, statistics.fmean(gaps) if gaps else None,
                    statistics.fmean([r for _, r in w]) if w else None))
        start += step
    return out


def across(pooled_entry, comp):
    th = pooled_entry["threads"][comp]
    return (th["wakes_per_s"], [x.get("mean") if x else None for x in th["gap_ms"]],
            [x.get("mean") if x else None for x in th["run_ms"]], th["threads"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pooled")
    ap.add_argument("probes", nargs="+")
    ap.add_argument("--window", type=float, default=1800.0)
    ap.add_argument("--step", type=float, default=60.0)
    ap.add_argument("--margin", type=float, default=60.0)
    ap.add_argument("--phase", default="idle")
    ap.add_argument("--component", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    p = json.load(open(a.pooled))
    run = next(iter(p["runs"].values()))
    entries = next(iter(run["phases"].values()))["entries"]
    comps = [tuple(c.split(":", 1)) for c in a.component] or failing(run)
    probes = [read_run(D, a.margin, a.phase) for D in a.probes]
    result = {}
    for entry, comp in comps:
        pe = entries[entry]
        rate, gap, runm, threads = across(pe, comp)
        k = len(pe["repeats"])
        span = statistics.fmean(pe["span_s"])
        n_wakes = [round(r * span) for r in rate]
        # the entry's wakes from its threads' exact rates (D24), not its rate rounded to three places
        tot = sum(round(r * span) for th in pe["threads"].values() for r in th["wakes_per_s"])
        rec = {"analysis": {"repeats_with_it": len(rate), "of": k, "threads": sorted(set(threads))},
               "weight": {"share_of_entry_wakes": round(sum(n_wakes) / max(tot, 1), 4),
                          "wakes_per_phase": [min(n_wakes), max(n_wakes)],
                          "wakes_per_phase_mean": round(statistics.fmean(n_wakes), 1)},
               "across": {lb: spread(v) for lb, v in zip(LABELS, (rate, gap, runm))},
               "within": {}}
        for pr in probes:
            c = pr["clean"]
            sm = ((c["entries"][entry].get("_samples") or {}).get(comp))
            if not sm:
                rec["within"][str(pr["repeat"])] = None
                continue
            t0 = c["t0"]
            v = window_values(sm, t0, t0 + c["span_s"], a.window, a.step)
            rec["within"][str(pr["repeat"])] = {"positions": len(v), "clean_span_s": c["span_s"],
                                               **{lb: spread([x[i] for x in v]) for i, lb in enumerate(LABELS)}}
        result[f"{entry} {comp}"] = rec
        pct = lambda x: "—" if x is None else f"±{x * 100:.1f} %"
        print(f"== {entry} {comp}: in {len(rate)} of {k} repeats, threads {sorted(set(threads))}; "
              f"{rec['weight']['share_of_entry_wakes'] * 100:.1f} % of the entry's wakes, "
              f"{rec['weight']['wakes_per_phase'][0]}–{rec['weight']['wakes_per_phase'][1]} wakes a phase")
        for lb in LABELS:
            w = "; ".join(f"probe {r} {pct(x[lb]) if x else '—'}" for r, x in rec["within"].items())
            print(f"   {lb:14s} across the repeats {pct(rec['across'][lb])}   within one run: {w}")
    if a.json:
        json.dump(result, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main()
