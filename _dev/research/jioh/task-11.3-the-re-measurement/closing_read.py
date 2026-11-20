#!/usr/bin/env python3
"""Decisions 11 and 12's reading: the count at the re-measured value.

    python3 closing_read.py [--out closing.json]      (from the repository root)

The closing (decision 11): the gap rows of the three rebuilt judging files from `runs/rq0-gate-11-3-closing/` (the
RQ0 run's programs, the scorer as run) with the other sixteen judging files' rows carried from the RQ0 run
(`runs/rq0-gate/report.json`), at the primary boot default; the count of files meeting g against K, and each rebuilt
file's row beside the RQ0 run's. The current programs (decision 12): the same three from `runs/rq0-gate-11-3-current/`
(simulator@841dc81131cb, the fixed scorer) with the other sixteen from 11.2's rerun on those programs
(`runs/rq0-gate-rerun/report.json`) — the post hoc reading at the re-measured value. Each copy's own verdict detail
(its invalid runs) and guard rows beside."""
import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
RUNS = REPO / "runs"
REBUILT = ["c2-p1a", "c1-ml-train", "c7-ml-train"]
FIELDS = ("gap", "meets_g", "reference_score", "compared_mean", "n_terms", "n_no_headroom", "n_oracle_worse",
          "all_no_headroom", "random_beats_oracle", "available")


def primary(report):
    return {g["workload_id"]: g for g in report["gaps"] if g.get("boot_default", "") == "" and g["judging"]}


def reading(copy_dir, base_dir):
    copy = json.loads((copy_dir / "report.json").read_text())
    base = json.loads((base_dir / "report.json").read_text())
    c, b = primary(copy), primary(base)
    judging = list(base["criterion"].get("judging") or []) or sorted(b)
    k = int(base["criterion"]["k"])
    rows = {}
    for w in sorted(b):
        src = c if w in REBUILT else b
        rows[w] = {"from": copy_dir.name if w in REBUILT else base_dir.name,
                   **{f: src[w].get(f) for f in FIELDS if f in src[w]}}
    rebuilt = {w: {"now": {f: c[w].get(f) for f in FIELDS if f in c[w]},
                   "before": {f: b[w].get(f) for f in FIELDS if f in b[w]}} for w in REBUILT}
    met = sorted(w for w, r in rows.items() if r["meets_g"])
    guards = copy.get("guards") or {}
    return {"copy": copy_dir.name, "carried_from": base_dir.name, "k": k, "judging": len(rows),
            "met": len(met), "met_files": met, "verdict": "pass" if len(met) >= k else "fail",
            "base_met": base["verdict_detail"]["met"], "copy_invalid_runs": copy["verdict_detail"].get("invalid_runs"),
            "copy_guards": guards if isinstance(guards, dict) else {"rows": len(guards)},
            "rebuilt": rebuilt, "rows": rows, "judging_listed": judging}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(HERE / "closing.json"))
    args = ap.parse_args()
    out = {}
    for name, copy, base in (("closing", "rq0-gate-11-3-closing", "rq0-gate"),
                             ("current", "rq0-gate-11-3-current", "rq0-gate-rerun")):
        if (RUNS / copy / "report.json").is_file():
            out[name] = reading(RUNS / copy, RUNS / base)
            r = out[name]
            print(f"{name}: {r['met']} of {r['judging']} meet g (K = {r['k']}), {r['verdict']}; "
                  f"{r['carried_from']} {r['base_met']}; invalid runs {r['copy_invalid_runs']}")
            for w, x in r["rebuilt"].items():
                print(f"   {w}: gap {x['before'].get('gap')} -> {x['now'].get('gap')}, meets g "
                      f"{x['before'].get('meets_g')} -> {x['now'].get('meets_g')}")
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
