#!/usr/bin/env python3
"""Replay the harness's hand fixtures through a simulator binary and compare line by line.

    python3 simulator/tools/replay_fixtures.py [--sim simulator/steps/sim_ad] [--cap-null] [--only mock-wakes] [--show 8]

The binary is called in the positional form (`sim W [S]`, trace on stdout), so it is a ladder rung:
`simulator/src/sim` takes the invocation contract's flags only, and the last rung is that binary but
for the header's `sim`, which is not compared.

Each directory under harness/tools/tests/fixtures/ holding a trace is one case:

- a hand fixture (`run.json` + `trace.jsonl`): the run file is the workload (its `workload_id` becomes
  `meta.id`); the schedule is `config-schedule.json` when there is one, else the fixture's own
  `config_applied` lines at their times with the boot params (a fixture without a schedule file
  applies its entries where they are written, so no drain stands between);
- a reference fixture (`workload.json` + `reference-trace.jsonl`, fix-object and fix-tree): the
  reference simulator's own output, run with the boot entry alone as its schedule
  (harness/boot-defaults/ostep.json at t = 0, provenance fallback), as fix-object/generate.py
  produces it through `simulator/src/sim`.

`meta` and `x_` diagnostic lines are dropped on both sides (the harness reads neither,
data-contracts §9). A case is `identical`, `same-us order` (the same lines at every µs in another
order — the fixtures do not all fix the order of lines at one instant), or `differs` with the first
differing lines. `--cap-null` turns every schedule's batch_bandwidth_cap to null: the mock
scheduler the fixtures were derived with does not model the cap (memo_261023 Part B).

Exit status 0 when every case is identical or same-µs order, 1 otherwise. One simulator process at
a time; the fixtures are a few hundred lines each.
"""
import argparse
import collections
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIXTURES = os.path.join(ROOT, "harness", "tools", "tests", "fixtures")

# The boot default (recognition-vocabulary §2; Params in src/sim.cpp) — what a schedule entry
# reconstructed from a config_applied line carries
BOOT = {
    "MLFQ": {"num_queues": 3, "timeslice_us": 10000, "timeslice_growth": 2, "boost_interval_us": 100000},
    "EDF": {"residual_timeslice_us": 10000},
    "LOTTERY": {"timeslice_us": 10000, "batch_share": 0.15},
    "FIFO": {},
}


def read_lines(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def kept(events):
    return [e for e in events if e["event"] != "meta" and not e["event"].startswith("x_")]


def cases(only):
    for name in sorted(os.listdir(FIXTURES)):
        d = os.path.join(FIXTURES, name)
        if only and name not in only:
            continue
        if os.path.exists(os.path.join(d, "run.json")) and os.path.exists(os.path.join(d, "trace.jsonl")):
            yield name, d, "hand"
        elif os.path.exists(os.path.join(d, "workload.json")) and os.path.exists(os.path.join(d, "reference-trace.jsonl")):
            yield name, d, "reference"


def schedule_for(d, expected, cap_null):
    path = os.path.join(d, "config-schedule.json")
    if os.path.exists(path):
        with open(path) as f:
            sched = json.load(f)
    else:
        meta = next(e for e in expected if e["event"] == "meta")
        entries = [{"t_us": e["t"], "config": {"algorithm": e["algorithm"], "params": BOOT[e["algorithm"]],
                                                "batch_bandwidth_cap": None},
                    "provenance": e["provenance"]}
                   for e in expected if e["event"] == "config_applied"]
        if not entries:
            return None
        sched = {"workload_id": meta["workload_id"], "condition": meta["condition"], "schedule": entries}
    if cap_null:
        for e in sched["schedule"]:
            e["config"]["batch_bandwidth_cap"] = None
    return sched


def by_instant(events):
    groups = collections.OrderedDict()
    for e in events:
        groups.setdefault(e["t"], []).append(json.dumps(e, sort_keys=True))
    return {t: sorted(v) for t, v in groups.items()}


def run_case(sim, name, d, kind, cap_null, tmp):
    if kind == "hand":
        expected = read_lines(os.path.join(d, "trace.jsonl"))
        with open(os.path.join(d, "run.json")) as f:
            run = json.load(f)
        wl = {"meta": {"id": run["workload_id"]}, "ground_truth": {}, "events": run["events"]}
        sched = schedule_for(d, expected, cap_null)
    else:
        expected = read_lines(os.path.join(d, "reference-trace.jsonl"))
        with open(os.path.join(d, "workload.json")) as f:
            wl = json.load(f)
        with open(os.path.join(ROOT, "harness", "boot-defaults", "ostep.json")) as f:
            boot = json.load(f)
        sched = {"workload_id": wl["meta"]["id"], "condition": "fixed",
                 "schedule": [{"t_us": 0, "config": boot, "provenance": "fallback"}]}
    wl_path = os.path.join(tmp, name + ".workload.json")
    with open(wl_path, "w") as f:
        json.dump(wl, f)
    argv = [sim, wl_path]
    if sched is not None:
        s_path = os.path.join(tmp, name + ".schedule.json")
        with open(s_path, "w") as f:
            json.dump(sched, f)
        argv.append(s_path)
    p = subprocess.run(argv, capture_output=True, text=True)
    if p.returncode != 0:
        return "error", [p.stderr.strip()]
    got = kept([json.loads(l) for l in p.stdout.splitlines() if l.strip()])
    want = kept(expected)
    if got == want:
        return "identical", []
    if by_instant(got) == by_instant(want):
        return "same-us order", []
    diff = []
    for i in range(max(len(got), len(want))):
        g = got[i] if i < len(got) else None
        w = want[i] if i < len(want) else None
        if g != w:
            diff.append((i + 1, w, g))
    return f"differs ({len(diff)} lines)", diff


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sim", default=os.path.join(ROOT, "simulator", "steps", "sim_ad"))
    ap.add_argument("--cap-null", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--show", type=int, default=6, help="differing lines to print per case")
    a = ap.parse_args()
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, d, kind in cases(a.only):
            verdict, diff = run_case(a.sim, name, d, kind, a.cap_null, tmp)
            print(f"{name:14} {kind:9} {verdict}")
            if verdict.startswith(("differs", "error")):
                bad += 1
                for item in diff[: a.show]:
                    if isinstance(item, str):
                        print("    " + item)
                    else:
                        i, w, g = item
                        print(f"    line {i}\n      want {json.dumps(w)}\n      got  {json.dumps(g)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
