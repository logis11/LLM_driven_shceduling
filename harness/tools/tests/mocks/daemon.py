"""Mock daemon — faithful for `fixed`, `oracle`, and `random` (Phase 8 spec,
decision 11; 8.5 spec, decisions 13–16).

`projection` extracts the visible projection (data-contracts §4, contract 3b)
from a canonical workload; `snapshots` walks its pinned events under the five
telemetry rules of §5; `run` answers every snapshot through the driver table
and returns a contract-valid config schedule (§7) and recognition log (§8).
It emits `unmodified` only — no validator, no clamping, no `held`, no LLM
path. Where the oracle's answer is undefined (an `ambiguous` segment, the
terminal snapshot, any row the table cannot serve) the query carries a null
proposal and `fallback`, and the schedule entry repeats the boot default.
"""

import json
import random
from collections import Counter, defaultdict

from harness.drivertable import compose_row

CONDITIONS = ("fixed", "oracle", "random")
DRAWING = ("random",)                   # the conditions that take a seed


class MockDaemonError(ValueError):
    """A refused invocation: a condition the mock does not implement, a seed
    where none belongs or none where one does, an unusable input."""


def workload_id(doc) -> str:
    meta = doc.get("meta") or {}
    return meta.get("id") or doc.get("workload_id") or ""


# ------------------------------------------------------ the visible projection

def projection(doc) -> dict:
    """One entry per canonical task instance, never folded; a spawn table's
    children folded by name under their parent (§4)."""
    tasks = []
    for ev in doc.get("events", []):
        if ev.get("op") != "arrive":
            continue
        task = {"name": ev["name"], "t_arrive": int(ev["t"])}
        if ev.get("depart") is not None:
            task["t_depart"] = int(ev["depart"])
        if ev.get("spawn_table"):
            counts = Counter(child["name"] for child in ev["spawn_table"])
            task["children"] = [{"name": n, "count": c} for n, c in sorted(counts.items())]
        tasks.append(task)
    return {"workload_id": workload_id(doc), "tasks": tasks}


# ------------------------------------------------------------- telemetry (§5)

def snapshots(proj) -> list:
    """The telemetry snapshots: the name→count multiset after every pinned
    instant at which it changed. Rule 1: counts matter. Rule 2: all events at
    one instant give one snapshot. Rule 3: sorted by name. Rule 4: the final
    instant is emitted like any other. Rule 5: nothing else emits. Children
    enter with their parent and never leave (8.5 spec, decision 16)."""
    deltas = defaultdict(Counter)
    for task in proj["tasks"]:
        deltas[task["t_arrive"]][task["name"]] += 1
        for child in task.get("children", []):
            deltas[task["t_arrive"]][child["name"]] += child["count"]
        if "t_depart" in task:
            deltas[task["t_depart"]][task["name"]] -= 1
    live = Counter()
    out = []
    for t in sorted(deltas):
        before = dict(live)
        live.update(deltas[t])
        live = Counter({n: c for n, c in live.items() if c > 0})
        if dict(live) != before:
            out.append({"t_us": t, "processes": [{"name": n, "count": c}
                                                 for n, c in sorted(live.items())]})
    return out


# ----------------------------------------------------------------- the run

def _covering(segments, t):
    return next((s for s in segments if int(s["t_start"]) <= t < int(s["t_end"])), None)


def _config(row) -> dict:
    """The row's default entry as the simulator receives it — the harness's
    own composition, pinned to the daemon's by test."""
    return json.loads(compose_row(row))


def run(doc, condition, table, boot, seed=None):
    """(config schedule, recognition log) for one workload under one condition.
    `table` is a harness `DriverTable`, `boot` the boot-default configuration."""
    if condition not in CONDITIONS:
        raise MockDaemonError(f"condition {condition!r}: the mock daemon implements "
                              f"{', '.join(CONDITIONS)} only")
    if condition in DRAWING and seed is None:
        raise MockDaemonError(f"condition {condition!r} draws and needs a seed")
    if condition not in DRAWING and seed is not None:
        raise MockDaemonError(f"condition {condition!r} does not draw; no seed belongs")
    wid = workload_id(doc)
    schedule = {"workload_id": wid, "condition": condition,
                "schedule": [{"t_us": 0, "config": boot, "provenance": "fallback"}]}
    log = {"workload_id": wid, "condition": condition, "seed": seed, "queries": []}
    if condition == "fixed":
        return schedule, log

    segments = doc.get("ground_truth") or []
    ordered = sorted(table.rows)
    rng = random.Random(seed)
    for snap in snapshots(projection(doc)):
        t = snap["t_us"]
        if condition == "oracle":
            seg = _covering(segments, t)
            attrs = (seg or {}).get("attributes") or {}
            row = (table.row(seg["mode"], attrs["background_wanted"])
                   if seg is not None and "background_wanted" in attrs else None)
            source = {"segment": seg}
            system = (None if row is None
                      else {"mode": seg["mode"], "background_wanted": bool(attrs["background_wanted"])})
        else:
            draw = rng.randrange(len(ordered))
            mode, wanted = ordered[draw]
            row = table.rows[(mode, wanted)]
            source = {"draw": draw, "row": {"mode": mode, "background_wanted": wanted}}
            system = {"mode": mode, "background_wanted": wanted}
        if row is None:
            proposal, validation, config = None, "fallback", boot
        else:
            proposal, validation, config = {"system": system}, "unmodified", _config(row)
        log["queries"].append({"t_set_change": t, "telemetry": snap, "proposal": proposal,
                               "validation": validation, "latency_us": 0, "source": source})
        schedule["schedule"].append({"t_us": t, "config": config, "provenance": validation})
    return schedule, log


def write(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")
