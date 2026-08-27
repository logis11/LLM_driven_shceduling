"""Timeline loader + structural validation (task-2.3 spec §1–§4).

A timeline is meta + three independent tracks:
  segments: [{from, to, mode, attributes?, scenario?}]   -> ground_truth
  tasks:    [{id, name, archetype, arrive, depart?, bind?, count?}]
  focus:    [{from, to, task}]   single input-attention track
"""

import pathlib

import yaml

from .library import git_blob_hex
from .units import parse_us

DEMAND_CLASSES = ("oversubscribed", "calibration")


class TimelineError(Exception):
    """A structural violation in a timeline file (lint category: timeline)."""


class Timeline:
    def __init__(self, path, library):
        self.path = pathlib.Path(path)
        self.blob_hex = git_blob_hex(self.path)
        raw = yaml.safe_load(self.path.read_text())
        self._load_meta(raw)
        self._load_segments(raw)
        self._load_tasks(raw, library)
        self._load_focus(raw, library)

    def _err(self, msg):
        raise TimelineError(f"{self.path.name}: {msg}")

    def _load_meta(self, raw):
        meta = raw.get("meta") or self._err("missing meta block")
        for field in ("id", "seed"):
            if field not in meta:
                self._err(f"meta missing {field!r}")
        if not isinstance(meta["seed"], int):
            self._err("meta.seed must be an integer")
        self.id = meta["id"]
        self.seed = meta["seed"]
        self.demand_class = meta.get("demand", "oversubscribed")
        if self.demand_class not in DEMAND_CLASSES:
            self._err(f"meta.demand must be one of {DEMAND_CLASSES}")

    def _load_segments(self, raw):
        self.segments = []
        for seg in raw.get("segments") or self._err("missing segments track"):
            for field in ("from", "to", "mode"):
                if field not in seg:
                    self._err(f"segment missing {field!r}")
            entry = {
                "t_start": parse_us(seg["from"]),
                "t_end": parse_us(seg["to"]),
                "mode": seg["mode"],
                "attributes": seg.get("attributes") or {},
                "scenario": seg.get("scenario") or [],
            }
            if entry["t_start"] >= entry["t_end"]:
                self._err(f"segment {seg['mode']!r}: from >= to")
            self.segments.append(entry)
        self.segments.sort(key=lambda s: s["t_start"])
        for a, b in zip(self.segments, self.segments[1:]):
            if a["t_end"] > b["t_start"]:
                self._err(f"segments overlap at {b['t_start']} µs")

    def _load_tasks(self, raw, library):
        self.tasks = []
        seen = set()
        for task in raw.get("tasks") or self._err("missing tasks track"):
            for field in ("id", "name", "archetype", "arrive"):
                if field not in task:
                    self._err(f"task missing {field!r}")
            tid, archetype = task["id"], task["archetype"]
            if tid in seen:
                self._err(f"duplicate task id {tid!r}")
            seen.add(tid)
            if archetype not in library:
                self._err(f"task {tid!r}: unknown archetype {archetype!r}")

            declared = set(library.binding_params(archetype))
            bind = task.get("bind") or {}
            undeclared = set(bind) - declared
            if undeclared:
                self._err(
                    f"task {tid!r}: bind keys {sorted(undeclared)} not in "
                    f"{archetype!r} binding_params (inline-numerics violation)")
            missing = declared - set(bind)
            if missing:
                self._err(f"task {tid!r}: missing bind keys {sorted(missing)} "
                          f"declared by {archetype!r}")

            lifetime = library.lifetime(archetype)
            if lifetime == "spawned":
                self._err(f"task {tid!r}: archetype {archetype!r} is spawned-"
                          "only — it lives in spawn tables, not the tasks track")
            has_depart = "depart" in task
            if (lifetime == "segment-bound") != has_depart:
                self._err(
                    f"task {tid!r}: depart {'missing' if not has_depart else 'present'}"
                    f" but archetype lifetime is {lifetime!r} (depart iff segment-bound)")

            count = task.get("count", 1)
            if not isinstance(count, int) or count < 1:
                self._err(f"task {tid!r}: count must be a positive integer")

            entry = {
                "id": tid,
                "name": task["name"],
                "archetype": archetype,
                "arrive": parse_us(task["arrive"]),
                "depart": parse_us(task["depart"]) if has_depart else None,
                "bind": bind,
                "count": count,
            }
            if entry["depart"] is not None and entry["depart"] <= entry["arrive"]:
                self._err(f"task {tid!r}: depart <= arrive")
            self.tasks.append(entry)
        self.task_by_id = {t["id"]: t for t in self.tasks}

    def _load_focus(self, raw, library):
        self.focus = []
        for win in raw.get("focus") or []:
            for field in ("from", "to", "task"):
                if field not in win:
                    self._err(f"focus window missing {field!r}")
            entry = {"from": parse_us(win["from"]), "to": parse_us(win["to"]),
                     "task": win["task"]}
            if entry["from"] >= entry["to"]:
                self._err("focus window: from >= to")
            task = self.task_by_id.get(entry["task"]) or self._err(
                f"focus targets unknown task {win['task']!r}")
            if not library.has_input_channel(task["archetype"]):
                self._err(f"focus targets {task['id']!r} whose archetype "
                          f"{task['archetype']!r} has no input channel")
            if entry["from"] < task["arrive"] or (
                    task["depart"] is not None and entry["to"] > task["depart"]):
                self._err(f"focus window outside task {task['id']!r} lifetime")
            self.focus.append(entry)
        self.focus.sort(key=lambda w: w["from"])
        for a, b in zip(self.focus, self.focus[1:]):
            if a["to"] > b["from"]:
                self._err(f"focus windows overlap at {b['from']} µs "
                          "(one user, one attention track)")

    @property
    def duration_us(self):
        ends = [s["t_end"] for s in self.segments]
        ends += [t["depart"] for t in self.tasks if t["depart"] is not None]
        return max(ends)
