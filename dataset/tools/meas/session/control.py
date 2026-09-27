"""9.9's adapter for the untraced control (_dev/docs/spec/jioh/task-9.5-untraced-control.md).

A control job's (traced, untraced) values for each entry's carried components over the steady phase, keyed as
session/analyze.py keys them: `<instance>/<comm>`, the instance a process's unit and program as census.instances reads
them from its cgroup and comm, for the measured user the census recorded.
"""

import json
import os

from meas import control
from meas.session import census

PHASE = "steady"
RUNS = ("traced", "untraced")


def job_values(D, carried):
    """(order, {"<entry> <component> wakes/s" | "... run mean (ms)": (traced, untraced)}) for one control job;
    `carried` is the session's pooled entry."""
    report = json.load(open(os.path.join(D, "report.json")))
    entries = carried["phases"][PHASE]["entries"]
    per = {}
    for run in RUNS:
        name = PHASE if run == "traced" else f"{PHASE}-untraced"
        load = lambda edge: json.load(open(os.path.join(D, f"snap.{name}.{edge}.json")))
        before, after = load("before"), load("after")
        uid = json.load(open(os.path.join(D, f"census.{name}.start.json")))["uid"]
        procs = [{"pid": p["pid"], "comm": p.get("comm") or next((t["comm"] for t in p.get("tasks", []) if t["tid"] == p["pid"]), ""),
                  "cmd": p.get("cmd", ""), "cgroup": p.get("cgroup", ""), "kthread": not p.get("cmd")} for p in after["procs"]]
        inst, _ = census.instances(procs, uid)
        of = {pid: i for e in inst.values() for i, pids in e.items() for pid in pids}
        deltas, span = control.thread_deltas(before, after)
        per[run] = (control.group(deltas, lambda pid, comm: f"{of[pid]}/{comm}" if pid in of else None), span)
    vals = {}
    for entry, ent in entries.items():
        for comp in (ent.get("components") or {}).get("selected") or []:
            pair = {run: control.rate_and_run(per[run][0].get(comp) or {"run_ns": 0, "vol": 0}, per[run][1]) for run in RUNS}
            vals[f"{entry} {comp} wakes/s"] = (pair["traced"][0], pair["untraced"][0])
            vals[f"{entry} {comp} run mean (ms)"] = (pair["traced"][1], pair["untraced"][1])
    return report.get("control.order"), vals
