#!/usr/bin/env python3
"""Decisions 1 and 2 of the 11.4 spec read again from the corrected runs' scores: 11.2's rerun on the fixed simulator
(runs/rq0-gate-rerun) for sixteen judging files, 11.3's runs on the current programs (runs/rq0-gate-11-3-current) for
the three rebuilt on the second bless (c2-p1a, c1-ml-train, c7-ml-train). Per judging file: the gap as the evaluator
computes it (one minus the random seeds' mean score over the oracle's weight sum), whether it meets g, whether every
term is no headroom and which are oracle worse than fixed, and the oracle's improvement over fixed as a fraction of
fixed's value — signed, zero under the floor — weighted over the file's terms (the weighted mean); then the three
picks by the RQ0 gate spec's statement `failure-procedure` and the files with no headroom on every term.

    python3 picks.py            (from the repository root; writes picks.json beside this script)
"""
import csv
import json
import pathlib
import sys
from fractions import Fraction

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import evaluator, search  # noqa: E402

GATE = REPO / "harness" / "experiments" / "rq0-gate.yaml"
CURRENT = ("c2-p1a", "c1-ml-train", "c7-ml-train")
# the nine judging files whose scored segment maps to MLFQ with cap 0.05 (statement `prior-table-structure`)
DUPLICATE_HEAVY = ("c7-browsing", "c7-office", "c7-dev", "c7-photo", "c7-video-edit", "c7-compile", "c7-ml-train",
                   "c7-render", "c7-transcode")


def rows_of(path, files):
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["workload_id"] in files and not r["boot_default"] and r["table"] in ("prior", ""):
                out.setdefault(r["workload_id"], []).append(r)
    return out


def main():
    gate = evaluator.load_spec(GATE)
    judging = list(gate["files"]["judging"])
    g = Fraction(str(gate["criterion"]["g"]))
    floors = search.scorer.floors_for()
    rows = rows_of(REPO / "runs" / "rq0-gate-rerun" / "scores.csv", set(judging) - set(CURRENT))
    rows.update(rows_of(REPO / "runs" / "rq0-gate-11-3-current" / "scores.csv", set(CURRENT)))
    files = []
    for wid in judging:
        rs = rows[wid]
        oracle_file = next(r for r in rs if r["level"] == "file" and r["condition"] == "oracle")
        randoms = [Fraction(r["score"]) for r in rs if r["level"] == "file" and r["condition"] == "random"]
        ref = Fraction(oracle_file["weight_sum"])
        gap = 1 - (sum(randoms, Fraction(0)) / len(randoms)) / ref
        terms = [r for r in rs if r["level"] == "term" and r["condition"] == "oracle"]
        spec_terms = [{"entity": t["entity"], "metric": t["metric"], "aggregate": t["aggregate"],
                       "direction": t["direction"], "weight": t["weight"]} for t in terms]
        q, readings = search.quantity(spec_terms, [Fraction(t["value_fixed"]) for t in terms],
                                      [Fraction(t["value_oracle"]) for t in terms], floors)
        all_nh = all(int(t["no_headroom"]) for t in terms)
        files.append({"workload_id": wid, "runs": "rq0-gate-11-3-current" if wid in CURRENT else "rq0-gate-rerun",
                      "class": "duplicate-heavy" if wid in DUPLICATE_HEAVY else "low-duplicate",
                      "n_random": len(randoms), "gap": float(gap), "meets_g": bool(gap >= g and not all_nh),
                      "all_no_headroom": all_nh,
                      "terms": [{"entity": t["entity"], "metric": t["metric"], "value_fixed": t["value_fixed"],
                                 "value_oracle": t["value_oracle"], "no_headroom": int(t["no_headroom"]),
                                 "oracle_worse": int(t["oracle_worse"]), "against_floor": rd["against_floor"]}
                                for t, rd in zip(terms, readings)],
                      "improvement": float(q)})
    failing = [f for f in files if not f["meets_g"]]
    by_id = lambda f: f["workload_id"]                                       # noqa: E731
    picks = []
    for cls in ("duplicate-heavy", "low-duplicate"):
        pool = sorted((f for f in failing if f["class"] == cls and not f["all_no_headroom"]), key=by_id)
        best = max(pool, key=lambda f: f["improvement"])                     # max keeps the first of a tie: id order
        picks.append({"rule": f"the largest oracle improvement among the failing files with headroom, {cls}",
                      "workload_id": best["workload_id"], "improvement": best["improvement"], "gap": best["gap"]})
    lowest = min(sorted(failing, key=by_id), key=lambda f: f["gap"])
    picks.append({"rule": "the failing file whose gap fell furthest below g", "workload_id": lowest["workload_id"],
                  "improvement": lowest["improvement"], "gap": lowest["gap"]})
    seven = [{"workload_id": f["workload_id"],
              "oracle_worse_terms": [t["entity"] for t in f["terms"] if t["oracle_worse"]]}
             for f in files if f["all_no_headroom"]]
    out = {"g": float(g), "meets_g": sum(f["meets_g"] for f in files), "fail": len(failing), "picks": picks,
           "no_headroom_on_every_term": seven, "files": files}
    (pathlib.Path(__file__).parent / "picks.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{out['meets_g']} of {len(files)} meet g, {out['fail']} fail")
    for p in picks:
        print(f"  {p['workload_id']}: improvement {p['improvement']:.3f}, gap {p['gap']:.3f} — {p['rule']}")
    print("  no headroom on every term:", ", ".join(f"{s['workload_id']} (oracle worse: {s['oracle_worse_terms']})"
                                                     for s in seven))


if __name__ == "__main__":
    main()
