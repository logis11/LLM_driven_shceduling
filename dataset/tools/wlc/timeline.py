"""Timeline loader + structural validation (task-2.3 spec §1–§4).

A timeline is meta + four tracks and an optional fifth:
  segments:   [{from, to, mode, attributes?, scenario?}]   -> ground_truth
  tasks:      [{id, name, archetype, arrive, depart?, bind?, count?}]
  input:      [{from, to, task, slice_of?}]   the keystroke windows — where the replayed stimulus lands (one user, one
              typing hand); `slice_of: {from, to, index}` names the stream window this one is a slice of (9.18)
  focus:      [{from, to, task}]   the window-focus track — which top-level task holds the focus (9.17); -> canonical
              `focus`
  operations: [{at, task, name}]   optional — a measured archetype's operation placed at a point in time (9.5
              follow-ups spec, decisions 8–9)
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
        self._load_input(raw, library)
        self._load_focus(raw)
        self._load_operations(raw, library)

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
                "familiarity": seg.get("familiarity"),
            }
            if entry["t_start"] >= entry["t_end"]:
                self._err(f"segment {seg['mode']!r}: from >= to")
            if entry["familiarity"] is not None and \
                    entry["familiarity"] not in (1, 2, 3, 4, 5):
                self._err(f"segment {seg['mode']!r}: familiarity must be 1-5")
            self._check_background_wanted(seg["mode"], entry["attributes"])
            self.segments.append(entry)
        self.segments.sort(key=lambda s: s["t_start"])
        for a, b in zip(self.segments, self.segments[1:]):
            if a["t_end"] > b["t_start"]:
                self._err(f"segments overlap at {b['t_start']} µs")

    def _check_background_wanted(self, mode, attributes):
        """Every segment carries the graded attribute — except `ambiguous`,
        whose label is the explicit marker that no legal value exists."""
        present = "background_wanted" in attributes
        if mode == "ambiguous":
            if present:
                self._err(f"segment {mode!r}: background_wanted must be absent")
        elif not present:
            self._err(f"segment {mode!r}: background_wanted missing")
        elif not isinstance(attributes["background_wanted"], bool):
            self._err(f"segment {mode!r}: background_wanted must be a boolean")

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
                "source": task.get("source") or {},   # the bound values' provenance (9.18); checked by the linter
            }
            if entry["depart"] is not None and entry["depart"] <= entry["arrive"]:
                self._err(f"task {tid!r}: depart <= arrive")
            self.tasks.append(entry)
        self.task_by_id = {t["id"]: t for t in self.tasks}

    def _load_input(self, raw, library):
        """input: [{from, to, task, slice_of?}] — the keystroke windows. The replayed stimulus lands inside them
        (compiler), so a window targets a task whose archetype has an input channel, within its lifetime; windows do
        not overlap. `slice_of: {from, to, index}` (9.18 spec, decision 1) names the stream window this one is a slice
        of — the compiler draws the stimulus offset for that window, by its length and its index among the task's
        windows, and places inside this one the keystrokes that fall in it; the window lies inside it."""
        self.input = []
        for win in raw.get("input") or []:
            for field in ("from", "to", "task"):
                if field not in win:
                    self._err(f"input window missing {field!r}")
            entry = {"from": parse_us(win["from"]), "to": parse_us(win["to"]),
                     "task": win["task"], "slice_of": None}
            if entry["from"] >= entry["to"]:
                self._err("input window: from >= to")
            if win.get("slice_of") is not None:
                outer = win["slice_of"]
                for field in ("from", "to", "index"):
                    if field not in outer:
                        self._err(f"input window slice_of missing {field!r}")
                if not isinstance(outer["index"], int) or outer["index"] < 0:
                    self._err("input window slice_of.index must be a non-negative integer")
                entry["slice_of"] = {"from": parse_us(outer["from"]), "to": parse_us(outer["to"]),
                                     "index": outer["index"]}
                if not (entry["slice_of"]["from"] <= entry["from"] and entry["to"] <= entry["slice_of"]["to"]):
                    self._err(f"input window {entry['from']}–{entry['to']} µs lies outside the stream window it "
                              "names as slice_of")
            task = self.task_by_id.get(entry["task"]) or self._err(
                f"input targets unknown task {win['task']!r}")
            if not library.has_input_channel(task["archetype"]):
                self._err(f"input targets {task['id']!r} whose archetype "
                          f"{task['archetype']!r} has no input channel")
            if entry["from"] < task["arrive"] or (
                    task["depart"] is not None and entry["to"] > task["depart"]):
                self._err(f"input window outside task {task['id']!r} lifetime")
            self.input.append(entry)
        self.input.sort(key=lambda w: w["from"])
        for a, b in zip(self.input, self.input[1:]):
            if a["to"] > b["from"]:
                self._err(f"input windows overlap at {b['from']} µs "
                          "(one user, one typing hand)")

    def _load_focus(self, raw):
        """focus: [{from, to, task}] — the window-focus track (9.17 spec, decisions 1, 2, 4). Required on every
        timeline, empty when no window exists. An interval names a top-level task of count 1 (the projection shows the
        holder by name; a spawn child has no pinned times, a counted task no single id), lies within its lifetime, and
        overlaps no other: one user, one attention track. Every input window lies inside a focus interval of its own
        task — the user types into the window in front."""
        if "focus" not in raw:
            self._err("missing focus track (an empty list when no window holds the focus)")
        self.focus = []
        for win in raw.get("focus") or []:
            for field in ("from", "to", "task"):
                if field not in win:
                    self._err(f"focus interval missing {field!r}")
            entry = {"from": parse_us(win["from"]), "to": parse_us(win["to"]),
                     "task": win["task"]}
            if entry["from"] >= entry["to"]:
                self._err("focus interval: from >= to")
            task = self.task_by_id.get(entry["task"]) or self._err(
                f"focus targets unknown task {win['task']!r}")
            if task["count"] != 1:
                self._err(f"focus targets {task['id']!r}, a counted task — the holder is one top-level task")
            if entry["from"] < task["arrive"] or (
                    task["depart"] is not None and entry["to"] > task["depart"]):
                self._err(f"focus interval outside task {task['id']!r} lifetime")
            self.focus.append(entry)
        self.focus.sort(key=lambda w: w["from"])
        for a, b in zip(self.focus, self.focus[1:]):
            if a["to"] > b["from"]:
                self._err(f"focus intervals overlap at {b['from']} µs "
                          "(one user, one attention track)")
        for win in self.input:
            if not any(f["task"] == win["task"] and f["from"] <= win["from"] and win["to"] <= f["to"]
                       for f in self.focus):
                self._err(f"input window {win['from']}–{win['to']} µs of task {win['task']!r} lies outside "
                          "its focus intervals (the user types into the window in front)")

    def _load_operations(self, raw, library):
        """operations: [{at, task, name}] — a measured archetype's heavy operation placed at a point in time
        (9.5 follow-ups spec, decisions 8–9); its length is drawn from the operation's measured duration at
        compile time, so only the start is authored. Whether it may start only inside an input window is 9.10's."""
        self.operations = []
        for op in raw.get("operations") or []:
            for field in ("at", "task", "name"):
                if field not in op:
                    self._err(f"operation missing {field!r}")
            entry = {"at": parse_us(op["at"]), "task": op["task"], "name": op["name"]}
            task = self.task_by_id.get(entry["task"]) or self._err(
                f"operation targets unknown task {op['task']!r}")
            available = library.operations(task["archetype"])
            if entry["name"] not in available:
                self._err(f"operation {op['name']!r} is not one of {task['archetype']!r}'s operations "
                          f"{sorted(available)}")
            if entry["at"] < task["arrive"] or (task["depart"] is not None and entry["at"] >= task["depart"]):
                self._err(f"operation starts outside task {task['id']!r} lifetime")
            self.operations.append(entry)
        self.operations.sort(key=lambda o: o["at"])

    @property
    def duration_us(self):
        ends = [s["t_end"] for s in self.segments]
        ends += [t["depart"] for t in self.tasks if t["depart"] is not None]
        return max(ends)
