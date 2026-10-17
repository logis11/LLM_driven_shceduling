#!/usr/bin/env python3
"""The stability ledger (the 2026-09-20 validity memo §3; 9.15's hand-off to 9.16): over the pooled records the
library's measured entries are folded from, how many values on the stability lists met the tolerance, how many are
carried under each exception class, and the largest half-width carried.

The population. Each measured entry's values are folded from one or more pooled records — the records the fold-in
tools name (`meas/control_report.py` POOL_95, IDLE_FROM_95, pool_98, POOL_99; `meas/batch_fold_in.py` POOLS). Each
record holds the stability list its pool tool tests (`stability.quantities`), the list the entries' scopes call
"every value on the list". A value is counted once, from the record its entry takes it from: a phase another
record supersedes (`mail-client`'s and `video-editor`'s idle phases, 9.5 D80, 9.10 D146), a subject the library no
longer carries (9.8's `chrome-visible`; 9.8's `chrome-hidden`, re-measured in 9.10 D152) and the retired 9.6 batch
programs (`batch_fold_in.py`: clamscan, ffmpeg, handbrake, train, tracker) are left out and counted apart.

The classes. A value that passes the rule (`meas/stability.py`: the 95 % t half-width at most 5 % of the mean, or
1 µs for a time where larger, over at least five repeats) met the tolerance. A value that does not is carried under
the class its record flags, the component's class before the field's: sparse component (`sparse`), varies between
sessions (`session_spread`), recording runs out (`limited`), spread follows the machine (`excepted`). A failing value
with no flag is reported as unresolved. The fifth class, the rare event within a run, is carried beside the rule,
not on it: the library's `heavy_events`, counted from `dataset/archetypes.yaml`.

Each value's pass is re-derived from its recorded mean, half-width and repeat count with the rule's tolerance and
floor (a check of the records, not a re-pool).

stability_ledger.py [--json OUT] [--md OUT]
"""

import argparse
import json
import os
import sys

def _repo(d=os.path.dirname(os.path.abspath(__file__))):
    """The repository root: the nearest directory up holding dataset/tools (the script runs from 9.16's research
    folder or from dataset/tools/meas alike)."""
    while not os.path.isdir(os.path.join(d, "dataset", "tools")):
        if os.path.dirname(d) == d:
            raise SystemExit("no dataset/tools above this script")
        d = os.path.dirname(d)
    return d


REPO = _repo()
sys.path.insert(0, os.path.join(REPO, "dataset", "tools"))

from meas import control_report as cr   # noqa: E402
from meas import batch_fold_in as bf   # noqa: E402
from meas.stability import TOLERANCE  # noqa: E402

MIN_REPEATS = 5
CLASSES = ("sparse", "session_spread", "limited", "excepted")   # the component's class before the field's
CLASS_NAME = {"sparse": "Sparse component", "session_spread": "Varies between sessions",
              "limited": "Recording runs out", "excepted": "Spread follows the machine",
              "rare": "Rare event within a run"}
# 9.6's record also holds the cpu-batch programs 9.10 replaced (batch_fold_in.py's TABLES comment)
RETIRED_96 = ("clamscan ", "ffmpeg ", "handbrake ", "train ", "tracker ")


def rel(p):
    return os.path.relpath(p, REPO)


def load(path):
    return json.load(open(os.path.join(REPO, path) if not os.path.isabs(path) else path))


def quantities(record, app=None):
    s = record["stability"] if app is None else record["runs"][app]["stability"]
    return s["quantities"]


def floor_of(name, record_floor_ms=None):
    """The rule's absolute floor in the value's unit: 1 µs for a time, none for a rate, share or count."""
    if "wakes/s" in name or "share" in name or "CPU total" in name:
        return None
    if "(ms)" in name:
        return 0.001
    return 1.0   # µs: the background records' "(µs)" values and 9.6's unlabelled step, dispatch and block values


def sources():
    """(entry or entries, record path, app key or None, keep(name) -> bool, note) for every record the library folds."""
    out = []
    for app, arch in cr.ARCH_95.items():
        main = os.path.join(cr.POOL_95[app], f"pool-{app}.json")
        if app in cr.IDLE_FROM_95:
            idle = os.path.join(cr.IDLE_FROM_95[app], f"pool-{app}.json")
            out.append((arch, idle, app, lambda n: n.startswith("idle "), "idle phase"))
            out.append((arch, main, app, lambda n: not n.startswith("idle "), "phases but idle"))
        else:
            out.append((arch, main, app, lambda n: True, ""))
    from meas.desktop.fold_in import IDS as IDS98
    for app, arch in IDS98.items():
        out.append((arch, cr.pool_98(app), app, lambda n: True, ""))
    from meas.session.fold_in import IDS as IDS99
    for prog, arch in IDS99.items():
        out.append((arch, cr.POOL_99, "session", (lambda p: lambda n: n.startswith(p + " "))(prog), ""))
    P = bf.POOLS
    out += [("build-orchestrator", P["build"], None, lambda n: n == "make dispatch", ""),
            ("compiler-child", P["build"], None,
             lambda n: n.startswith("object-job ") or n.endswith(" CPU per process"), ""),
            ("file-archiver", P["7z"], "7z", lambda n: True, ""),
            ("game-download, game-download-idle", P["steamcmd"], "steamcmd", lambda n: True, "one job, two entries"),
            ("package-upgrade", P["upgrade"], "upgrade", lambda n: True, ""),
            ("module-build-orchestrator", P["dkms"], "dkms", lambda n: " step " not in n, ""),
            ("module-compiler-child", P["dkms"], "dkms", lambda n: " step " in n, ""),
            ("file-indexer", P["tracker"], "tracker", lambda n: True, ""),
            ("cpu-batch (python3)", P["mnist"], "mnist", lambda n: True, ""),
            ("cpu-batch (kdenlive_render)", P["kdenlive"], "kdenlive", lambda n: True, ""),
            ("video-transcoder", P["handbrake"], "handbrake", lambda n: True, ""),
            ("incremental-backup", P["dejadup"], "dejadup", lambda n: True, "")]
    return out


def classify(name, c):
    passes = c["passes"]
    floor = floor_of(name)
    k, mean, hw_abs = c["k"], c["mean"], c["half_width_abs"]
    if hw_abs is None or mean is None:
        rederived = False
    else:
        bound = TOLERANCE * abs(mean) if floor is None else max(TOLERANCE * abs(mean), floor)
        rederived = hw_abs <= bound * (1 + 1e-3) + 1e-12 and k >= MIN_REPEATS   # the records round to 4 decimals
    flags = [f for f in CLASSES if c.get(f)]
    if passes:
        cls = "met"
    else:
        cls = next((f for f in CLASSES if c.get(f)), "unresolved")
        if c["k"] < MIN_REPEATS:
            cls = "unresolved"
    by_floor = bool(passes and c["half_width"] is not None and c["half_width"] > TOLERANCE)
    return cls, flags, rederived, by_floor


def ledger():
    import yaml
    lib = yaml.safe_load(open(os.path.join(REPO, "dataset", "archetypes.yaml")))["archetypes"]
    measured = {a for a, e in lib.items() if (e.get("validation_stats") or {}).get("referee") == "meas-ci"}
    rows, seen, left_out = [], set(), []
    for entry, path, app, keep, note in sources():
        base = entry.split(" (")[0].split(", ")[0]
        if base not in lib:
            # a subject the library no longer carries (renderer-visible)
            q = quantities(load(path), app)
            left_out.append({"what": f"{entry}: not in the library", "record": rel(path), "values": len(q)})
            continue
        q = quantities(load(path), app)
        for name, c in q.items():
            if not keep(name):
                continue
            key = (rel(path), app, name)
            if key in seen:
                continue
            seen.add(key)
            cls, flags, rederived, by_floor = classify(name, c)
            rows.append({"entry": entry, "record": rel(path), "app": app, "value": name, "k": c["k"], "mean": c["mean"],
                         "half_width": c["half_width"], "half_width_abs": c["half_width_abs"],
                         "needed": c.get("needed"), "passes": c["passes"], "pass_rederived": rederived,
                         "class": cls, "flags": flags, "met_by_floor": by_floor, "note": note})
    # what the records hold that no entry takes from them
    for app in cr.IDLE_FROM_95:
        main = os.path.join(cr.POOL_95[app], f"pool-{app}.json")
        idle = os.path.join(cr.IDLE_FROM_95[app], f"pool-{app}.json")
        n_main = sum(1 for n in quantities(load(main), app) if n.startswith("idle "))
        n_idle = sum(1 for n in quantities(load(idle), app) if not n.startswith("idle "))
        left_out.append({"what": f"{cr.ARCH_95[app]}: the idle values of the record its other phases come from",
                         "record": rel(main), "values": n_main})
        if n_idle:
            left_out.append({"what": f"{cr.ARCH_95[app]}: the other phases' values of its idle record",
                             "record": rel(idle), "values": n_idle})
    from meas.desktop.fold_in import IDS as IDS98
    for app in IDS98:
        if cr.pool_98(app) != cr.POOL_98 and app in load(cr.POOL_98)["runs"]:
            left_out.append({"what": f"{IDS98[app]}: 9.8's record, superseded", "record": rel(cr.POOL_98),
                             "values": len(quantities(load(cr.POOL_98), app))})
    q96 = quantities(load(bf.POOLS["build"]))
    left_out.append({"what": "9.6's retired cpu-batch programs (clamscan, ffmpeg, handbrake, train, tracker)",
                     "record": rel(bf.POOLS["build"]), "values": sum(1 for n in q96 if n.startswith(RETIRED_96))})
    rare = [{"entry": a, "event": h["comm"], "count": h["count"], "span_s": h["span_s"]} for a, e in lib.items()
            if a in measured for h in ((e.get("params") or {}).get("heavy_events") or [])]
    return rows, left_out, rare, measured


def summarise(rows, rare, measured):
    by = {}
    for r in rows:
        by.setdefault(r["class"], []).append(r)
    carried = [r for r in rows if r["class"] != "unresolved"]
    widest = max(carried, key=lambda r: r["half_width"] or 0.0)
    met = by.get("met", [])
    widest_met = max(met, key=lambda r: r["half_width"] or 0.0)
    covered = set()
    for r in rows:
        for e in r["entry"].split(" (")[0].split(", "):
            covered.add(e)
    return {
        "values": len(rows),
        "met_tolerance": len(met),
        # the stimulus-sensitivity check's per-input means (9.5 method §3): on the lists, not carried
        "stimulus_check_values": sum(1 for r in rows if "136M" in r["value"]),
        "stimulus_check_values_met": sum(1 for r in met if "136M" in r["value"]),
        "met_by_1us_floor": sum(1 for r in met if r["met_by_floor"]),
        "met_in_a_flagged_component": sum(1 for r in met if set(r["flags"]) & {"sparse", "session_spread"}),
        "carried_under": {c: len(by.get(c, [])) for c in CLASSES},
        "rare_events_beside_the_rule": len(rare),
        "unresolved": len(by.get("unresolved", [])),
        "pass_flag_disagrees_with_rederived": sum(1 for r in rows if r["passes"] != r["pass_rederived"]),
        "largest_half_width_carried": {k: widest[k] for k in ("entry", "value", "half_width", "k", "class")},
        "largest_half_width_met": {k: widest_met[k] for k in ("entry", "value", "half_width", "half_width_abs", "k")},
        "largest_per_class": {c: max(({k: r[k] for k in ("entry", "value", "half_width", "k")} for r in by.get(c, [])),
                                     key=lambda x: x["half_width"] or 0.0, default=None) for c in CLASSES},
        "entries_covered": sorted(covered),
        "measured_entries_without_a_value": sorted(measured - covered),
    }


def pct(x):
    return "—" if x is None else f"{100 * x:.2f} %"


def render(rows, left_out, rare, s):
    L = ["# Stability ledger — script output", "",
         f"Values on the stability lists of the records the library is folded from: **{s['values']}**, over "
         f"{len(s['entries_covered'])} entries (measured entries with no value on a list: "
         f"{', '.join(s['measured_entries_without_a_value']) or 'none'}). {s['stimulus_check_values']} of them are "
         "the stimulus-sensitivity check's per-input means under 136M, on the lists but not carried "
         f"({s['stimulus_check_values_met']} met the tolerance).", "",
         f"- Met the tolerance: **{s['met_tolerance']}** — of which {s['met_by_1us_floor']} by the 1 µs floor rather "
         f"than the 5 %, and {s['met_in_a_flagged_component']} belong to a component carried under a class (its "
         "values together).",
         ]
    for c in CLASSES:
        L.append(f"- Carried under '{CLASS_NAME[c]}': **{s['carried_under'][c]}**")
    L += [f"- '{CLASS_NAME['rare']}', beside the rule, not on a list: **{s['rare_events_beside_the_rule']}** events "
          f"({', '.join(f"{r['entry']} `{r['event']}`, {r['count']} over {r['span_s']:,.0f} s" for r in rare)})",
          f"- Unresolved (failing, no class, or under five repeats): **{s['unresolved']}**",
          f"- Records' pass flag against the rule re-derived from mean, half-width and count: "
          f"{s['pass_flag_disagrees_with_rederived']} disagree",
          f"- Largest half-width carried: **{pct(s['largest_half_width_carried']['half_width'])}**, "
          f"{s['largest_half_width_carried']['entry']} `{s['largest_half_width_carried']['value']}` "
          f"({CLASS_NAME.get(s['largest_half_width_carried']['class'], s['largest_half_width_carried']['class'])}, "
          f"{s['largest_half_width_carried']['k']} repeats)",
          f"- Largest half-width among the values that met the tolerance: "
          f"{pct(s['largest_half_width_met']['half_width'])} ({s['largest_half_width_met']['half_width_abs']} µs), "
          f"{s['largest_half_width_met']['entry']} `{s['largest_half_width_met']['value']}`, by the 1 µs floor", ""]
    L += ["## Per entry", "", "| entry | values | met | " + " | ".join(CLASS_NAME[c] for c in CLASSES) + " | widest half-width |",
          "|---|---|---|" + "---|" * len(CLASSES) + "---|"]
    ents = {}
    for r in rows:
        ents.setdefault(r["entry"], []).append(r)
    for e, rs in ents.items():
        w = max(rs, key=lambda r: r["half_width"] or 0.0)
        L.append(f"| {e} | {len(rs)} | {sum(r['class'] == 'met' for r in rs)} | "
                 + " | ".join(str(sum(r['class'] == c for r in rs) or "") for c in CLASSES)
                 + f" | {pct(w['half_width'])} (`{w['value']}`) |")
    L += ["", "## The values carried under a class", "",
          "| class | entry | value | repeats | half-width | repeats the rule would need |", "|---|---|---|---|---|---|"]
    for c in CLASSES:
        for r in sorted((r for r in rows if r["class"] == c), key=lambda r: -(r["half_width"] or 0)):
            L.append(f"| {CLASS_NAME[c]} | {r['entry']} | `{r['value']}` | {r['k']} | {pct(r['half_width'])} | "
                     f"{r['needed'] if r['needed'] is not None else 'over 200'} |")
    L += ["", "## Met by the 1 µs floor", "", "| entry | value | repeats | half-width | absolute |", "|---|---|---|---|---|"]
    for r in sorted((r for r in rows if r["met_by_floor"]), key=lambda r: -(r["half_width"] or 0)):
        L.append(f"| {r['entry']} | `{r['value']}` | {r['k']} | {pct(r['half_width'])} | {r['half_width_abs']} |")
    L += ["", "## Held in the records, taken by no entry", "", "| what | record | values |", "|---|---|---|"]
    for x in left_out:
        L.append(f"| {x['what']} | `{x['record']}` | {x['values']} |")
    L += ["", "## Records read", ""] + [f"- `{p}`" for p in sorted({r['record'] for r in rows})]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--md")
    a = ap.parse_args()
    os.chdir(REPO)
    rows, left_out, rare, measured = ledger()
    s = summarise(rows, rare, measured)
    if a.json:
        json.dump({"summary": s, "rare_events": rare, "left_out": left_out, "values": rows}, open(a.json, "w"), indent=1)
    md = render(rows, left_out, rare, s)
    if a.md:
        open(a.md, "w").write(md)
    print(md)


if __name__ == "__main__":
    main()
