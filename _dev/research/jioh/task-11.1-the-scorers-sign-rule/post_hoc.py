#!/usr/bin/env python3
"""The RQ0 run's post hoc reading under the fixed sign rule (11.1 spec, decisions 4 and 5).

    python3 post_hoc.py [--run runs/rq0-gate] [--out runs/rq0-gate/post-hoc] [--machine harness/runner.yaml]

Re-scores the run's aggregates with the scorer as it now stands — the oracle's improvement read with its sign —
on the scoring spec the runner built for the run (its variant and generated files' entries included), then evaluates the RQ0 gate spec on those scores with the run's own guards and grades, labelled post hoc.
Nothing the run wrote is touched: the scores, the report and its rendering go to `--out`. The stage times, the
counts and the hashes go to `post-hoc.json` beside this script."""
import argparse
import hashlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))

from harness import aggregates as agg  # noqa: E402
from harness import evaluator, manifests, runner, scorer, scoring  # noqa: E402
from harness.evaluator import evaluate, render, validate_report, write_report  # noqa: E402
from harness.outputs import iter_csv, write_csv  # noqa: E402

SPEC = REPO / "harness" / "experiments" / "rq0-gate.yaml"
POST_HOC = ("Post hoc reading of the RQ0 run (2026-11-16 to 2026-11-18), not its verdict. The run's aggregates are "
            "re-scored with the oracle's improvement read with its sign: a term whose oracle is worse than fixed by "
            "the floor or more is no headroom, at share 1, and marked oracle worse than fixed (harness/CHANGELOG.md, "
            "2026-11-18; sub-task 11.1). The guards and the grades are the run's own. The RQ0 run's verdict is the "
            "report in harness/experiments/rq0-gate/: fail, 6 of 19 judging files against K = 10, provisional.")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def scoring_spec(machine_path):
    """The scoring spec as the runner builds it for the RQ0 gate spec (`harness/tools/harness/runner.py`,
    `run_experiment`): the pinned spec with an entry per variant file, from the machine configuration's build
    directory, and per selected generated file, from its set's pinned manifest."""
    gate = evaluator.load_spec(SPEC)
    pins = gate["pins"]
    machine = runner.load_machine(machine_path, REPO)
    gate, _paths, axes = manifests.expand(gate, REPO)
    out = scoring.with_variants(scoring.load_spec(REPO / pins["scoring_spec"]["path"]),
                                {wid: machine.build_dir / f"{wid}.workload.json"
                                 for wid in (gate["files"].get("variants") or [])})
    selected_by_set = {}
    for wid, (set_name, _record) in axes.items():
        selected_by_set.setdefault(set_name, set()).add(wid)
    for set_name, wids in sorted(selected_by_set.items()):
        out = scoring.with_generated(out, manifests.load(REPO / pins["generated"][set_name]["path"]), only=wids)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--run", default=str(REPO / "runs" / "rq0-gate"))
    ap.add_argument("--machine", default=str(REPO / "harness" / "runner.yaml"))
    ap.add_argument("--out", default=str(REPO / "runs" / "rq0-gate" / "post-hoc"))
    args = ap.parse_args()
    run, out = pathlib.Path(args.run), pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    times = {}

    t0 = time.time()
    spec = scoring_spec(args.machine)
    read, index = scorer.reads(spec), {}
    n = 0
    for row in iter_csv(run / "aggregates.csv", agg.COLUMNS):
        scorer.index_row(row, read, index)
        n += 1
    term_rows, file_rows = scorer.score_index(index, spec)
    del index
    write_csv(term_rows + file_rows, scorer.COLUMNS, out / "scores.csv")
    times["scores"] = round(time.time() - t0, 1)
    print(f"scored {n} aggregate rows: {len(term_rows)} term rows, {len(file_rows)} file rows "
          f"({times['scores']} s)", flush=True)

    t0 = time.time()
    report = evaluate(SPEC, run / "aggregates.csv", out / "scores.csv", run / "guards.csv", run / "grades.csv", REPO,
                      post_hoc=POST_HOC)
    validate_report(report)
    write_report(report, out / "report.json")
    (out / "report.md").write_text(render(report), encoding="utf-8")
    times["report"] = round(time.time() - t0, 1)

    d = report["verdict_detail"]
    head = next(l for l in report["lines"] if l["type"] == "headroom_count")
    summary = {"aggregate_rows": n, "term_rows": len(term_rows), "file_rows": len(file_rows),
               "oracle_worse_terms": sum(1 for r in term_rows if r["oracle_worse"]),
               "count": report["verdict"], "met": d["met"], "judging": d["judging"], "k": d["k"],
               "met_files": sorted(r["workload_id"] for r in report["gaps"]
                                   if r["judging"] and r["boot_default"] == "" and r["meets_g"]),
               "with_headroom": head["with_headroom"],
               "sha256": {p: sha256(out / p) for p in ("scores.csv", "report.json", "report.md")},
               "seconds": times}
    (pathlib.Path(__file__).parent / "post-hoc.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
