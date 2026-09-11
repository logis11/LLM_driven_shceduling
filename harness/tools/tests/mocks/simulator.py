"""Mock simulator — a trivial generator and a replay (Phase 8 spec, decision
10; 8.5 spec, decisions 17–18).

The generator emits a contract-valid trace (data-contracts §9) for any
workload and config schedule from one rule that models no scheduling: at every
stimulus instant — a pinned arrival, a pinned wake, a periodic task's tick, and
each chain stage's wake in turn — the stimulated task is `ready`, runs for
exactly 1 µs, and ends its run. A finite task exits after its last stimulus
run, a segment-bound task departs at its pinned depart, spawn children arrive
with their parent, every periodic job gets a met `deadline` line, and each
schedule entry before the workload's end gets its `config_applied` line at its
stamped time. Same-instant lines: config entries in list order, then arrivals
in file order, then the rest, a run closing before a run opening.

The replay copies a hand-written fixture trace after checking that it belongs
to the workload named. Both paths validate every input before writing.
"""

import gzip
import json
import pathlib
from collections import defaultdict

from harness.reader import RunFileError, read_run_file

SIM = "mock-simulator@0"
_RANK = {"config_applied": 0, "task_arrive": 1, "run_end": 2, "deadline": 3,
         "ready": 4, "run_start": 5, "task_end": 6}


class MockSimulatorError(ValueError):
    """A refused invocation: contract-invalid input, mismatched identities."""


def _load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as exc:
        raise MockSimulatorError(f"{path}: {exc}") from None


def _workload_id(doc) -> str:
    return ((doc.get("meta") or {}).get("id")) or doc.get("workload_id") or ""


def _check_schedule(sched, wid):
    entries = sched.get("schedule") if isinstance(sched, dict) else None
    if not isinstance(entries, list) or not entries:
        raise MockSimulatorError("config schedule: no 'schedule' list")
    if sched.get("workload_id") != wid:
        raise MockSimulatorError(f"config schedule: workload_id {sched.get('workload_id')!r} "
                                 f"is not the workload's {wid!r}")
    if int(entries[0].get("t_us", -1)) != 0:
        raise MockSimulatorError("config schedule: the first entry must be at t_us 0")
    for i, e in enumerate(entries):
        cfg = e.get("config") or {}
        if "algorithm" not in cfg or "params" not in cfg or "provenance" not in e:
            raise MockSimulatorError(f"config schedule: entry {i} is malformed")


def _open_text(path):
    path = pathlib.Path(path)
    return gzip.open(path, "rt", encoding="utf-8") if path.suffix == ".gz" else open(path, "r", encoding="utf-8")


def _write_text(text, out):
    out = pathlib.Path(out)
    if out.suffix == ".gz":
        with gzip.open(out, "wt", encoding="utf-8") as f:
            f.write(text)
    else:
        out.write_text(text, encoding="utf-8")


def generate(workload_path, schedule_path, out_path, replay=None):
    """Write the trace for (workload, schedule) to `out_path`; with `replay`,
    copy that trace instead. Nothing is written until every input passed."""
    doc = _load(workload_path)
    wid = _workload_id(doc)
    sched = _load(schedule_path)
    _check_schedule(sched, wid)
    if replay is not None:
        with _open_text(replay) as f:
            text = f.read()
        try:
            head = json.loads(text.splitlines()[0])
        except (IndexError, ValueError):
            raise MockSimulatorError(f"{replay}: no header line") from None
        if head.get("event") != "meta" or head.get("workload_id") != wid:
            raise MockSimulatorError(f"{replay}: header workload_id {head.get('workload_id')!r} "
                                     f"is not the workload's {wid!r}")
        _write_text(text, out_path)
        return
    try:
        run = read_run_file(workload_path)
    except RunFileError as exc:
        raise MockSimulatorError(f"{workload_path}: {exc}") from None
    lines = _lines(doc, run, sched)
    _write_text("".join(json.dumps(l, separators=(",", ":")) + "\n" for l in lines), out_path)


def _lines(doc, run, sched):
    t_end = run.t_end
    entries = sched["schedule"]
    out = []

    def emit(t, obj):
        out.append((t, _RANK[obj["event"]], len(out), obj))

    for i, e in enumerate(entries):
        t = int(e["t_us"])
        if t < t_end:
            emit(t, {"event": "config_applied", "t": t, "index": i,
                     "algorithm": e["config"]["algorithm"], "provenance": e["provenance"]})

    # stimuli per task, in file order of first appearance
    stimuli = defaultdict(list)
    order, parent_of = [], {}
    for ev in doc["events"]:
        if ev.get("op") == "arrive":
            order.append(ev["id"])
            stimuli[ev["id"]].append((int(ev["t"]), "arrive"))
            for child in ev.get("spawn_table", []):
                order.append(child["id"])
                parent_of[child["id"]] = ev["id"]
                stimuli[child["id"]].append((int(ev["t"]), "arrive"))
        elif ev.get("op") == "wake":
            stimuli[ev["target"]].append((int(ev["t"]), "wake"))
    ticks = {}
    for chain in run.chains:
        head = run.tasks[chain[0]]
        period = head.period_us
        until = head.depart if head.depart is not None else t_end
        grid = [head.arrive + k * period for k in range((min(until, t_end) - head.arrive + period - 1) // period)]
        grid = [t for t in grid if t < until and t < t_end]
        ticks[chain[0]] = (grid, period)
        for t in grid:
            stimuli[chain[0]].append((t, "timer_tick"))
            for stage in chain[1:]:
                stimuli[stage].append((t, "wake"))

    for tid in order:
        info = run.tasks[tid]
        arrive_t = stimuli[tid][0][0]
        arrival = {"event": "task_arrive", "t": arrive_t, "task": tid, "source": "file"}
        if tid in parent_of:
            arrival["source"] = "spawn"
            arrival["parent"] = parent_of[tid]
        emit(arrive_t, arrival)
        groups = defaultdict(list)
        for t, cause in sorted(stimuli[tid], key=lambda s: s[0]):
            groups[t].append(cause)
        finite = info.depart is None and info.period_us is None
        instants = sorted(groups)
        for t in instants:
            for cause in groups[t]:
                emit(t, {"event": "ready", "t": t, "task": tid, "cause": cause})
            emit(t, {"event": "run_start", "t": t, "task": tid})
            if finite and t == instants[-1]:
                emit(t + 1, {"event": "run_end", "t": t + 1, "task": tid, "reason": "exit"})
                emit(t + 1, {"event": "task_end", "t": t + 1, "task": tid, "reason": "exit"})
            else:
                blocked = "timer" if info.period_us is not None else "wait"
                emit(t + 1, {"event": "run_end", "t": t + 1, "task": tid, "reason": "block",
                             "blocked_on": blocked})
        if info.depart is not None:
            emit(info.depart, {"event": "task_end", "t": info.depart, "task": tid, "reason": "depart"})
        if tid in ticks:
            grid, period = ticks[tid]
            for t in grid:
                emit(t + 1, {"event": "deadline", "t": t + 1, "task": tid, "due": t + period,
                             "met": True, "slack_us": period - 1})

    out.sort(key=lambda x: x[:3])
    meta = {"event": "meta", "workload_id": _workload_id(doc), "condition": sched.get("condition", ""),
            "sim": SIM, "schedule_entries": len(entries)}
    return [meta] + [obj for _, _, _, obj in out]
