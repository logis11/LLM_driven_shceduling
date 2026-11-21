#!/usr/bin/env python3
"""The search's points read for the record and the memo, beside the report: per file, from the points file
(`points.csv`, the search tool's), the row's and the boot default's quantities, the best read point per algorithm
and per cap, how many read points have a quantity above the row's and how many beat the row by the floor or more on
a scored term, the ten best points, and the read points' range per term.

    python3 read_search.py [--points harness/experiments/rq0-config-search/points.csv]
                           [--report harness/experiments/rq0-config-search/report.json]
    (from the repository root; writes summary.json beside this script, or --out)

A point's quantity is computed again from its terms' values by the search tool's own rule
(`harness/tools/harness/search.py`, `quantity`, the floors of the search spec), not read from the points file's
quantity column, which is printed to six places: points whose quantities differ past the sixth place read equal
there. Among points of equal quantity the row comes first, then grid order — the search spec's `best_tie`."""
import argparse
import csv
import json
import pathlib
import sys
from fractions import Fraction

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness/tools"))

from harness import search  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--spec", default=str(REPO / "harness/experiments/rq0-config-search.yaml"))
    ap.add_argument("--points", default=str(REPO / "harness/experiments/rq0-config-search/points.csv"))
    ap.add_argument("--report", default=str(REPO / "harness/experiments/rq0-config-search/report.json"))
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent / "summary.json"))
    args = ap.parse_args()
    floors = search.floors_of(search.load_spec(args.spec))
    report = json.loads(pathlib.Path(args.report).read_text())
    files = {f["workload_id"]: f for f in report["files"]}
    pts = {}
    with open(args.points, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            p = pts.setdefault(r["workload_id"], {}).setdefault(r["point"], {
                "order": int(r["order"]), "algorithm": r["algorithm"], "cap": r["batch_bandwidth_cap"] or "none",
                "params": json.loads(r["params"]), "read": r["read"] == "1", "out": r["out"], "terms": []})
            p["terms"].append({"entity": r["entity"], "aggregate": r["aggregate"], "direction": r["direction"],
                               "weight": r["weight"], "value": Fraction(r["value"])})
    out = {"report_spec_sha256": report["spec_sha256"], "route": report["route"]["route"], "files": []}
    for wid, points in pts.items():
        rf = files[wid]
        row_id = rf["row"]
        row, fixed = points[row_id], points[rf["fixed"]]
        fixed_values = [t["value"] for t in fixed["terms"]]
        read = {pid: p for pid, p in points.items() if p["read"]}
        for p in read.values():
            p["quantity"] = search.quantity(p["terms"], fixed_values, [t["value"] for t in p["terms"]], floors)[0]

        def beats_row(p):
            return [t["entity"] for t, rt in zip(p["terms"], row["terms"])
                    if ((rt["value"] - t["value"]) if t["direction"] == "lower" else (t["value"] - rt["value"]))
                    >= floors[t["aggregate"]]]

        def rank(kv):
            return (-kv[1]["quantity"], kv[0] != row_id, kv[1]["order"])

        def best_of(key):
            groups = {}
            for pid, p in sorted(read.items(), key=rank):
                groups.setdefault(key(p), (pid, p))
            return {k: {"point": pid, "quantity": float(p["quantity"])} for k, (pid, p) in sorted(groups.items())}
        ranked = sorted(read.items(), key=rank)
        out["files"].append({
            "workload_id": wid, "finding": rf.get("finding"), "row": row_id,
            "row_quantity": float(row["quantity"]) if row_id in read else None,
            "fixed": rf["fixed"], "read": len(read), "out": len(points) - len(read),
            "best": ranked[0][0], "best_is_report_best": ranked[0][0] == rf.get("best"),
            "above_row": sum(1 for p in read.values() if p["quantity"] > row["quantity"]),
            "beat_row_by_the_floor": sum(1 for p in read.values() if beats_row(p)),
            "best_by_algorithm": best_of(lambda p: p["algorithm"]),
            "best_by_cap": best_of(lambda p: p["cap"]),
            "top10": [{"point": pid, "quantity": float(p["quantity"]),
                       "values": {t["entity"]: float(t["value"]) for t in p["terms"]}} for pid, p in ranked[:10]],
            "terms": [{"entity": t["entity"], "fixed": float(t["value"]), "row": float(rt["value"]),
                       "min": float(min(p["terms"][i]["value"] for p in read.values())),
                       "max": float(max(p["terms"][i]["value"] for p in read.values()))}
                      for i, (t, rt) in enumerate(zip(fixed["terms"], row["terms"]))]})
    pathlib.Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for f in out["files"]:
        print(f"{f['workload_id']}: finding {f['finding']}, row {f['row']} at {f['row_quantity']:.3f}; "
              f"{f['above_row']} of {f['read']} read above it, {f['beat_row_by_the_floor']} better by the floor on a "
              f"term; best {f['best']} at {f['top10'][0]['quantity']:.6f} (the report's: {f['best_is_report_best']})")


if __name__ == "__main__":
    main()
