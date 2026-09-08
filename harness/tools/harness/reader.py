"""Readers for the harness's two inputs.

`read_trace` streams a simulator trace (data-contracts §9): a `meta` header
line, then the seven runtime event types, `x_`-prefixed lines skipped. It
validates the closed event set, each type's required fields and enums, and
time order, refusing the file with a line number on the first violation.

`read_run_file` reads the run-file view of a workload (data-contracts §4) for
the three facts a trace does not carry (metrics doc §3): `T_end`, chain
topology, and per-task demand. Nothing here computes a metric.
"""

import gzip
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional

RESERVED_ENTITIES = ("lane", "schedule", "recognizer")

# data-contracts §9 — required fields per event type, and the closed enums.
_EVENT_FIELDS = {
    "task_arrive": ("t", "task", "source"),
    "task_end": ("t", "task", "reason"),
    "ready": ("t", "task", "cause"),
    "run_start": ("t", "task"),
    "run_end": ("t", "task", "reason"),
    "deadline": ("t", "task", "due", "met", "slack_us"),
    "config_applied": ("t", "index", "algorithm", "provenance"),
}
_ENUMS = {
    ("task_arrive", "source"): {"file", "spawn"},
    ("task_end", "reason"): {"exit", "depart"},
    ("ready", "cause"): {"arrive", "wake", "sleep_end", "timer_tick", "fork_slot"},
    ("run_end", "reason"): {"block", "preempt", "exit", "depart"},
    ("run_end", "blocked_on"): {"wait", "sleep", "timer", "fork_slot"},
    ("config_applied", "provenance"): {"unmodified", "clamped", "held", "fallback"},
    ("config_applied", "algorithm"): {"MLFQ", "EDF", "LOTTERY", "FIFO"},
}
_HEADER_FIELDS = ("workload_id", "condition", "sim", "schedule_entries")


class TraceError(ValueError):
    """The trace violates the frozen format. The message names the line."""


class RunFileError(ValueError):
    """The run file cannot be used as the reader's second input."""


@dataclass(frozen=True)
class TraceMeta:
    workload_id: str
    condition: str
    sim: str
    schedule_entries: int


def _open(path):
    path = str(path)
    if path.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, "r", encoding="utf-8")


class Trace:
    """A streamed trace. `meta` is read eagerly; iterating yields each
    runtime event as a dict, in file order, validated line by line."""

    def __init__(self, path):
        self.path = path
        self.meta = self._read_header()

    def _read_header(self) -> TraceMeta:
        with _open(self.path) as f:
            line = f.readline()
        if not line.strip():
            raise TraceError("line 1: empty trace, expected a meta header")
        obj = _parse_line(line, 1)
        if obj.get("event") != "meta":
            raise TraceError("line 1: expected the meta header, got "
                             f"{obj.get('event')!r}")
        missing = [k for k in _HEADER_FIELDS if k not in obj]
        if missing:
            raise TraceError(f"line 1: meta header missing {missing}")
        return TraceMeta(obj["workload_id"], obj["condition"], obj["sim"],
                         int(obj["schedule_entries"]))

    def __iter__(self) -> Iterator[dict]:
        last_t = None
        with _open(self.path) as f:
            for lineno, line in enumerate(f, start=1):
                if lineno == 1 or not line.strip():
                    continue
                obj = _parse_line(line, lineno)
                kind = obj.get("event")
                if isinstance(kind, str) and kind.startswith("x_"):
                    continue
                if kind not in _EVENT_FIELDS:
                    raise TraceError(f"line {lineno}: unknown event {kind!r}")
                for key in _EVENT_FIELDS[kind]:
                    if key not in obj:
                        raise TraceError(f"line {lineno}: {kind} missing {key!r}")
                for (k, key), allowed in _ENUMS.items():
                    if k == kind and key in obj and obj[key] not in allowed:
                        raise TraceError(f"line {lineno}: {kind}.{key} = "
                                         f"{obj[key]!r} not in {sorted(allowed)}")
                if "task" in obj and obj["task"] in RESERVED_ENTITIES:
                    raise TraceError(f"line {lineno}: task id {obj['task']!r} "
                                     "is a reserved entity name")
                t = obj["t"]
                if not isinstance(t, int):
                    raise TraceError(f"line {lineno}: t must be an integer µs")
                if last_t is not None and t < last_t:
                    raise TraceError(f"line {lineno}: t={t} precedes t={last_t} "
                                     "(trace lines must be ordered by t)")
                last_t = t
                yield obj

    @property
    def sha256(self) -> str:
        h = hashlib.sha256()
        with open(self.path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()


def _parse_line(line, lineno):
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as exc:
        raise TraceError(f"line {lineno}: not JSON ({exc.msg})") from None
    if not isinstance(obj, dict):
        raise TraceError(f"line {lineno}: expected an object")
    return obj


def read_trace(path) -> Trace:
    return Trace(path)


# ---------------------------------------------------------------- run file

@dataclass
class TaskInfo:
    id: str
    name: str
    arrive: Optional[int]          # pinned arrival; None for spawned children
    depart: Optional[int]          # pinned depart for segment-bound tasks
    demand: Optional[int]          # total RUN work; None when unbounded
    period_us: Optional[int]       # the TIMER period, when the program has one
    wake_targets: List[str] = field(default_factory=list)
    spawned: bool = False


@dataclass
class RunFile:
    workload_id: str
    t_end: int
    tasks: Dict[str, TaskInfo]
    chains: List[List[str]]        # each from a TIMER head to its tail
    wakes: Dict[str, int]          # exogenous wake events per target task


def _walk(program):
    """Yield every op in a program, descending into LOOP bodies."""
    for op in program:
        yield op
        if op.get("op") == "LOOP":
            yield from _walk(op.get("body", []))


def _run_total(program) -> Optional[int]:
    """Sum of RUN work; None if any LOOP is unbounded."""
    total = 0
    for op in program:
        kind = op.get("op")
        if kind == "RUN":
            total += int(op["us"])
        elif kind == "LOOP":
            if op.get("count") == "unbounded":
                return None
            inner = _run_total(op.get("body", []))
            if inner is None:
                return None
            total += int(op["count"]) * inner
    return total


def _task_info(tid, name, program, arrive=None, depart=None, spawned=False):
    if tid in RESERVED_ENTITIES:
        raise RunFileError(f"task id {tid!r} is a reserved entity name")
    period = next((int(op["period_us"]) for op in _walk(program)
                   if op.get("op") == "TIMER"), None)
    targets = [op["target"] for op in _walk(program) if op.get("op") == "WAKE"]
    return TaskInfo(id=tid, name=name, arrive=arrive, depart=depart,
                    demand=_run_total(program), period_us=period,
                    wake_targets=targets, spawned=spawned)


def read_run_file(path) -> RunFile:
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    if "events" not in doc:
        raise RunFileError("run file has no 'events'")
    tasks: Dict[str, TaskInfo] = {}
    wakes: Dict[str, int] = {}
    pinned = [0]
    for ev in doc["events"]:
        op = ev.get("op")
        if op == "arrive":
            tid = ev["id"]
            if tid in tasks:
                raise RunFileError(f"duplicate task id {tid!r}")
            tasks[tid] = _task_info(tid, ev["name"], ev["program"],
                                    arrive=int(ev["t"]), depart=ev.get("depart"))
            pinned.append(int(ev["t"]))
            if ev.get("depart") is not None:
                pinned.append(int(ev["depart"]))
            for child in ev.get("spawn_table", []):
                cid = child["id"]
                if cid in tasks:
                    raise RunFileError(f"duplicate task id {cid!r}")
                tasks[cid] = _task_info(cid, child["name"], child["program"],
                                        spawned=True)
        elif op == "wake":
            pinned.append(int(ev["t"]))
            wakes[ev["target"]] = wakes.get(ev["target"], 0) + 1
        else:
            raise RunFileError(f"unknown event op {op!r}")
    chains = []
    for tid, info in tasks.items():
        if info.period_us is None:
            continue
        chain = [tid]
        cur = info
        while cur.wake_targets:
            nxt = cur.wake_targets[0]
            if nxt in chain or nxt not in tasks:
                break
            chain.append(nxt)
            cur = tasks[nxt]
        chains.append(chain)
    return RunFile(workload_id=doc.get("workload_id", ""), t_end=max(pinned),
                   tasks=tasks, chains=chains, wakes=wakes)
