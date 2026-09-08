"""The visible projection — the parse boundary of the whole experiment.

`read_projection` is the only way a canonical workload file (data-contracts §4)
enters the daemon, and it returns the slice a recognizer is entitled to see
(daemon-guide §3): process names, counts, and pinned lifetime times. Everything
else in the file — task programs, task ids, spawn-table programs, `wake`
events, `meta.sampled`, and `ground_truth` — is dropped here and is not
reachable from the returned value by any path.

Why the boundary is a module and not a convention: the project's central claim
is that *names alone* carry enough meaning to schedule well (daemon-guide §2.1).
If behavioral information reaches a recognizer through any side door, a
positive result stops being publishable, because no reviewer can tell whether
the model read the names or peeked at the behavior. So the raw parse is local
to `_read_json` and the returned dataclasses are frozen: there is no attribute
to follow back to the file.

What survives, per task:

    name        the process name a recognizer sees (collides by design —
                thirteen `chrome` are thirteen tasks, c6-spoof depends on it)
    t_arrive    the `arrive` event's `t`
    t_depart    the pinned `depart` iff the task is segment-bound, else None.
                None means "ends when it finishes", and *when* it finishes is
                scheduler-dependent — a result of the experiment, never an
                input. Treat the task as present through the end of the run.
    children    the spawn table folded to name→count. Which children a parent
                will launch is fixed at compile time, so it is visible and
                attaches to the parent's lifetime; when each one starts and
                stops is emergent, so no times are carried.
"""

import json
from dataclasses import dataclass
from typing import Optional, Tuple

from .errors import ProjectionError

# The three top-level keys of a canonical file. `ground_truth` is named here
# only so this module can refuse a file that lacks it — its *content* is read
# exclusively by `groundtruth.py`, and never by anything on this path.
_TOP_LEVEL = ("meta", "ground_truth", "events")


@dataclass(frozen=True)
class ChildGroup:
    """`count` processes named `name`, launched by a parent while it runs."""

    name: str
    count: int


@dataclass(frozen=True)
class TaskView:
    """One task, as the recognizer is allowed to know it."""

    name: str
    t_arrive: int
    t_depart: Optional[int]
    children: Tuple[ChildGroup, ...] = ()


@dataclass(frozen=True)
class Projection:
    """One workload's visible projection.

    `tasks` is sorted by `(t_arrive, name)` and each task's `children` by name,
    so two builders — and two runs — produce the same order. Nothing downstream
    may rely on the file's own event order.
    """

    workload_id: str
    tasks: Tuple[TaskView, ...]

    def to_json(self):
        """The shape shown in daemon-guide §3. Optional keys are omitted rather
        than emitted as null, so a hand-check reads like the guide's example."""
        tasks = []
        for task in self.tasks:
            entry = {"name": task.name, "t_arrive": task.t_arrive}
            if task.t_depart is not None:
                entry["depart"] = task.t_depart
            if task.children:
                entry["children"] = [{"name": c.name, "count": c.count}
                                     for c in task.children]
            tasks.append(entry)
        return {"workload_id": self.workload_id, "tasks": tasks}


def _read_json(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise ProjectionError(f"{path}: cannot be opened ({exc.strerror})") from exc
    except json.JSONDecodeError as exc:
        raise ProjectionError(f"{path}: not JSON ({exc})") from exc


def _time(value, path, what):
    """Times are integer microseconds. `bool` is an `int` in Python and would
    slip through an isinstance check, so it is rejected explicitly."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ProjectionError(f"{path}: {what} must be a non-negative integer "
                              f"microsecond value, got {value!r}")
    return value


def _children(event, path):
    """Fold a spawn table to name→count, dropping every child's program and id.

    First-seen order is kept while counting and the result is sorted by name;
    both are deliberate — the count is signal (a hundred `cc1` read as a
    parallel build), the order in the table is not.
    """
    table = event.get("spawn_table")
    if table is None:
        return ()
    if not isinstance(table, list):
        raise ProjectionError(f"{path}: task {event.get('name')!r} has a "
                              f"non-list spawn_table")
    counts = {}
    for entry in table:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise ProjectionError(f"{path}: task {event.get('name')!r} has a "
                                  f"spawn-table entry without a name")
        counts[entry["name"]] = counts.get(entry["name"], 0) + 1
    return tuple(ChildGroup(name=name, count=counts[name])
                 for name in sorted(counts))


def _task(event, path):
    name = event.get("name")
    if not isinstance(name, str) or not name:
        raise ProjectionError(f"{path}: an arrive event has no usable name")
    t_arrive = _time(event.get("t"), path, f"task {name!r}'s arrive time")
    depart = event.get("depart")
    if depart is not None:
        depart = _time(depart, path, f"task {name!r}'s depart time")
        if depart < t_arrive:
            raise ProjectionError(f"{path}: task {name!r} departs at {depart} "
                                  f"before it arrives at {t_arrive}")
    return TaskView(name=name, t_arrive=t_arrive, t_depart=depart,
                    children=_children(event, path))


def read_projection(path):
    """Read a canonical workload file and return its visible projection.

    Raises `ProjectionError` — never a bare KeyError or TypeError — on anything
    that is not a usable canonical file, because a daemon sweep names the file
    it refused rather than dying with a traceback halfway through 24 of them.
    """
    document = _read_json(path)
    if not isinstance(document, dict):
        raise ProjectionError(f"{path}: top level is not an object")
    missing = [key for key in _TOP_LEVEL if key not in document]
    if missing:
        raise ProjectionError(f"{path}: not a canonical workload file "
                              f"(missing {', '.join(missing)})")

    meta = document["meta"]
    workload_id = meta.get("id") if isinstance(meta, dict) else None
    if not isinstance(workload_id, str) or not workload_id:
        raise ProjectionError(f"{path}: meta.id is missing or not a string")

    events = document["events"]
    if not isinstance(events, list):
        raise ProjectionError(f"{path}: events is not a list")

    # `wake` events are skipped, not refused: they are real canonical events,
    # but a wake changes no process's existence, so the projection — and every
    # query point built from it (daemon-guide §2.2) — cannot see one.
    tasks = [_task(event, path) for event in events
             if isinstance(event, dict) and event.get("op") == "arrive"]
    if not tasks:
        raise ProjectionError(f"{path}: no arrive events; nothing to project")

    tasks.sort(key=lambda task: (task.t_arrive, task.name))
    return Projection(workload_id=workload_id, tasks=tuple(tasks))
