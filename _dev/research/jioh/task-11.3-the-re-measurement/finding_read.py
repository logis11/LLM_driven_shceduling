#!/usr/bin/env python3
"""The finding step's reading (the 11.3 spec, decisions 2 and 3, and the invariant on the controls): each build's
`fixed` and `oracle` P99 of the editor's input latency and its gap under the scorer as run, the value whose build
falls below g, and the two controls against the RQ0 run.

    python3 finding_read.py [--prefix rq0-gate-finding] [--out finding.json]

Reads each build's `runs/<prefix>-<dir>/report.json` and `scores.csv` (finding_run.sh; the as-run harness's
outputs) and the RQ0 run's `runs/rq0-gate/report.json` and `scores.csv`; the controls first, the builds only when
both reproduce. A control reproduces the RQ0 run when every score row of its build at
the primary boot default under the primary table equals the RQ0 run's row of the file it reproduces
(`c7-ml-train`, `c7-ml-train@corner-low`) in every column but the workload id, and its gap row equals the run's in
every field but the id. Writes the reading beside this script; exit 1 when a control does not reproduce."""
import argparse
import csv
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
RQ0 = REPO / "runs" / "rq0-gate"
G = 0.5
BASE = "c7-ml-train"
CONTROLS = {"nothing-moved": BASE, "all-four-low": f"{BASE}@corner-low"}   # build -> the RQ0 run's file


def score_rows(path, wids):
    out = {w: [] for w in wids}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            w = row["workload_id"]
            if w in out and row["boot_default"] == "" and row["table"] == "prior":
                out[w].append(row)
    return out


def keyed(rows):
    return sorted(({k: v for k, v in r.items() if k != "workload_id"} for r in rows),
                  key=lambda r: (r["condition"], r["seed"], r["level"], r["entity"], r["metric"], r["aggregate"]))


def gap_rows(path, wids):
    report = json.loads(pathlib.Path(path).read_text())
    return {g["workload_id"]: g for g in report["gaps"] if g["workload_id"] in wids and g.get("boot_default", "") == ""}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--prefix", default="rq0-gate-finding")
    ap.add_argument("--out", default=str(HERE / "finding.json"))
    args = ap.parse_args()
    builds = json.loads((HERE / "finding-builds.json").read_text())["builds"]
    run_of = {b["build"]: REPO / "runs" / f"{args.prefix}-{pathlib.Path(b['build_dir']).name}" for b in builds}
    rq0_scores = score_rows(RQ0 / "scores.csv", list(CONTROLS.values()))
    rq0_gaps = gap_rows(RQ0 / "report.json", list(CONTROLS.values()))
    controls = {}
    for b in builds:
        if b["build"] not in CONTROLS:
            continue
        w, ref, run = b["workload_id"], CONTROLS[b["build"]], run_of[b["build"]]
        mine = keyed(score_rows(run / "scores.csv", [w])[w])
        theirs = keyed(rq0_scores[ref])
        g = gap_rows(run / "report.json", [w])[w]
        controls[b["build"]] = {"workload_id": w, "experiment": run.name, "reproduces": ref,
                                "score_rows": len(mine), "rq0_score_rows": len(theirs),
                                "score_rows_equal": mine == theirs, "gap_row_equal": g == rq0_gaps[ref],
                                "gap": g["gap"], "rq0_gap": rq0_gaps[ref]["gap"]}
    ok = all(c["score_rows_equal"] and c["gap_row_equal"] for c in controls.values())
    for k, c in controls.items():
        print(f"control {k} ({c['workload_id']}) vs the RQ0 run's {c['reproduces']}: score rows {c['score_rows']} "
              f"{'equal' if c['score_rows_equal'] else 'DIFFER'}, gap row {'equal' if c['gap_row_equal'] else 'DIFFERS'}")
    out = {"g": G, "floor_us": 1000, "scorer": "as run (commit 6086e7e1)", "simulator": "simulator@0d323c84470a",
           "controls_reproduce": ok, "controls": controls}
    if not ok:      # the spec's invariant: the mismatch is diagnosed before any build is read
        pathlib.Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
        print("a control does not reproduce the RQ0 run: the builds are not read")
        return 1
    rows = []
    for b in builds:
        w, run = b["workload_id"], run_of[b["build"]]
        if not (run / "report.json").is_file():
            print(f"{b['build']}: no run yet ({run.name})")
            continue
        scores = score_rows(run / "scores.csv", [w])[w]
        term = [r for r in scores if r["level"] == "term" and r["condition"] == "fixed"]
        if len(term) != 1:
            raise SystemExit(f"{b['build']}: {len(term)} fixed term rows, one expected")
        t, g = term[0], gap_rows(run / "report.json", [w])[w]
        rows.append({"build": b["build"], "workload_id": w, "experiment": run.name, "moved": b["moved"],
                     "term": f"{t['entity']} {t['metric']} {t['aggregate']}",
                     "fixed_p99_us": float(t["value_fixed"]), "oracle_p99_us": float(t["value_oracle"]),
                     "oracle_minus_fixed_us": float(t["value_oracle"]) - float(t["value_fixed"]),
                     "no_headroom": t["no_headroom"] == "1",
                     "random_mean_score": float(g["compared_mean"]), "gap": float(g["gap"]),
                     "meets_g": bool(g["meets_g"]), "below_g": float(g["gap"]) < G})
    out["builds"] = rows
    out["moving_alone"] = [r["build"] for r in rows if r["below_g"] and r["build"] not in CONTROLS]
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    for r in rows:
        print(f"{r['build']:18} fixed {r['fixed_p99_us']:>16,.2f}  oracle {r['oracle_p99_us']:>16,.2f}  "
              f"gap {r['gap']:>10.6f}  {'below g' if r['below_g'] else 'meets g'}")
    print("moving alone:", out["moving_alone"] or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
