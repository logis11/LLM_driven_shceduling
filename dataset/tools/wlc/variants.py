"""The sensitivity variants of the RQ0 gate spec (9.14 decisions 10 and 12).

`dataset/variants.yaml` names each set — a transform, its parameters, the files
it rebuilds — and the exception-carried values the corner sets scale. This
module applies one transform to one base file and returns the variant's
canonical dict with its `meta.id` set to `<base>@<set>`; `meta.derived_from`
and `meta.sampled` stay the base's (the workload contract has no slot for a
transform), and the variants manifest the CLI writes is the provenance.

Transforms on the blessed artifact (no recompile): `scale-runs` multiplies every
RUN of every task but the frame chain's members by a factor; `scale-chain` the
chain members' RUNs alone. Transforms that recompile with the pinned library:
`segment-length` edits the base timeline's segment bounds and shifts what
follows; `carried-bounds` scales the named tables in a copy of the library;
`trace-replay` points the named entries at observed wake streams
(dataset/replay/) and recompiles.
"""

import copy
import json
import pathlib
import tempfile

import yaml

from .compiler import _load_replay, compile_timeline
from .library import Library
from .timeline import Timeline
from .units import parse_us

DATASET = pathlib.Path(__file__).resolve().parents[2]
CHAIN_PREFIXES = ("game.chain.", "game.wineserver")
TRANSFORMS = ("scale-runs", "scale-chain", "segment-length", "carried-bounds", "trace-replay")


class VariantError(ValueError):
    """A set that cannot be built as named."""


def variant_id(base_id, set_name):
    return f"{base_id}@{set_name}"


def load_spec(path=None):
    path = pathlib.Path(path) if path else DATASET / "variants.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------- programs

def _scale_program(program, factor):
    """Every RUN's `us` multiplied by `factor`, rounded to whole µs, at least 1."""
    out = []
    for step in program:
        step = dict(step)
        if step.get("op") == "RUN":
            step["us"] = max(1, int(round(step["us"] * factor)))
        elif step.get("op") == "LOOP":
            step["body"] = _scale_program(step.get("body", []), factor)
        out.append(step)
    return out


def _is_chain_member(task_id):
    return any(task_id.startswith(p) for p in CHAIN_PREFIXES)


def scale_runs(canonical, factor, chain=False):
    """`scale-runs` (chain=False): every task but the chain's members; `scale-chain`
    (chain=True): the chain's members alone. Spawn-table children follow their parent."""
    out = copy.deepcopy(canonical)
    for ev in out["events"]:
        if ev.get("op") != "arrive":
            continue
        if _is_chain_member(ev["id"]) != chain:
            continue
        ev["program"] = _scale_program(ev["program"], factor)
        for child in ev.get("spawn_table") or []:
            child["program"] = _scale_program(child["program"], factor)
    return out


# ------------------------------------------------------------- timelines

def _shift(value_us, cut_us, delta_us):
    """A time at or past the cut moves by delta."""
    return value_us + delta_us if value_us >= cut_us else value_us


def shifted_timeline(raw, segment_index, length_us):
    """The base timeline's raw document with segment `segment_index` set to
    `length_us` long, and every segment bound, task arrival and depart, focus
    window edge and operation instant at or past the segment's old end shifted
    by the difference. Times stay as strings in µs."""
    doc = copy.deepcopy(raw)
    segs = doc["segments"]
    seg = segs[segment_index]
    old_start, old_end = parse_us(seg["from"]), parse_us(seg["to"])
    new_end = old_start + length_us
    delta = new_end - old_end
    if delta == 0:
        return doc
    us = lambda v: f"{v}us"  # noqa: E731

    def move(value):
        return us(_shift(parse_us(value), old_end, delta))

    seg["to"] = us(new_end)
    for s in segs[segment_index + 1:]:
        s["from"], s["to"] = move(s["from"]), move(s["to"])
    for task in doc.get("tasks") or []:
        if task.get("arrive") is not None:
            task["arrive"] = move(task["arrive"])
        if task.get("depart") is not None:
            task["depart"] = move(task["depart"])
    for win in doc.get("focus") or []:
        win["from"], win["to"] = move(win["from"]), move(win["to"])
    for op in doc.get("operations") or []:
        op["at"] = move(op["at"])
    return doc


def _compile_raw(raw, library, workdir, name):
    path = pathlib.Path(workdir) / f"{name}.timeline.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False, allow_unicode=True), encoding="utf-8")
    timeline = Timeline(path, library)
    canonical, report = compile_timeline(timeline, library, "single")
    return canonical, report


# --------------------------------------------------------------- library

def _scale_table(table, factor):
    """A quantile table (p, min, max, means) or a constant scaled by `factor`."""
    t = dict(table)
    if t.get("dist") == "constant":
        t["value_us"] = max(1, int(round(t["value_us"] * factor)))
        return t
    if t.get("dist") == "quantiles":
        t["p"] = [max(0, int(round(v * factor))) for v in t["p"]]
        for k in ("min", "max"):
            if k in t:
                t[k] = max(0, int(round(t[k] * factor)))
        if "means" in t:
            t["means"] = [round(m * factor, 3) for m in t["means"]]
        return t
    raise VariantError(f"cannot scale a table of dist {t.get('dist')!r}")


def scaled_library(lib_doc, carried_values, side):
    """A copy of the library document with every carried value's table scaled by
    (1 − h) on the low side and (1 + h) on the high side."""
    doc = copy.deepcopy(lib_doc)
    entries = doc.get("archetypes") or doc
    for cv in carried_values:
        h = float(cv["half_width"])
        factor = 1 - h if side == "low" else 1 + h
        entry = entries[cv["entry"]]
        params = entry["params"]
        if "component" in cv:
            comps = [c for c in params["components"] if c.get("comm") == cv["component"]]
            if not comps:
                raise VariantError(f"{cv['entry']}: no component {cv['component']!r}")
            for c in comps:
                c[cv["table"]] = _scale_table(c[cv["table"]], factor)
        else:
            if cv["table"] not in params:
                raise VariantError(f"{cv['entry']}: no param {cv['table']!r}")
            params[cv["table"]] = _scale_table(params[cv["table"]], factor)
    return doc


def _library_from(doc, workdir):
    path = pathlib.Path(workdir) / "archetypes.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8")
    return Library(path)


# ---------------------------------------------------------------- replay

def replayed_library(lib_doc, streams):
    """A copy of the library with each named entry's `replay` param pointing at
    its observed stream (dataset/replay/<stream>.json.gz), the param's source
    the stream file's; the compiler replays it in place of the entry's sampled
    stream over a seeded window of the task's lifetime (a batch job from its
    start)."""
    doc = copy.deepcopy(lib_doc)
    entries = doc.get("archetypes") or doc
    for entry_name, stream in streams.items():
        if entry_name not in entries:
            raise VariantError(f"no entry {entry_name!r} to replay")
        params = entries[entry_name].setdefault("params", {})
        params["replay"] = {"stream": stream, "sampling": "per-task", "source": _load_replay(stream).get("source")}
    return doc


# ------------------------------------------------------------------ build

def build_variant(spec, set_spec, base_id, root, build_dir, workdir):
    """(canonical, report or None) for one base under one set."""
    root, build_dir = pathlib.Path(root), pathlib.Path(build_dir)
    transform = set_spec["transform"]
    vid = variant_id(base_id, set_spec["name"])
    if transform in ("scale-runs", "scale-chain"):
        base = json.loads((build_dir / f"{base_id}.workload.json").read_text(encoding="utf-8"))
        out = scale_runs(base, float(set_spec["factor"]), chain=(transform == "scale-chain"))
        out["meta"]["id"] = vid
        return out, None
    library_path = root / "dataset" / "archetypes.yaml"
    timeline_path = root / "dataset" / "timelines" / "coreset" / f"{base_id}.timeline.yaml"
    raw = yaml.safe_load(timeline_path.read_text(encoding="utf-8"))
    if transform == "segment-length":
        library = Library(library_path)
        raw = shifted_timeline(raw, int(set_spec["segment"]), parse_us(set_spec["length"]))
    elif transform == "carried-bounds":
        lib_doc = yaml.safe_load(library_path.read_text(encoding="utf-8"))
        library = _library_from(scaled_library(lib_doc, spec.get("carried_values") or [], set_spec["side"]), workdir)
    elif transform == "trace-replay":
        lib_doc = yaml.safe_load(library_path.read_text(encoding="utf-8"))
        library = _library_from(replayed_library(lib_doc, set_spec["streams"]), workdir)
    else:
        raise VariantError(f"unknown transform {transform!r}")
    base_meta = json.loads((build_dir / f"{base_id}.workload.json").read_text(encoding="utf-8"))["meta"]
    canonical, report = _compile_raw(raw, library, workdir, base_id)
    canonical["meta"] = dict(base_meta, id=vid)          # the base's provenance; the manifest records the transform
    return canonical, report


def build_all(spec, root, build_dir, only=None):
    """Yields (set_spec, base_id, canonical, report) for every (set, file), in spec order."""
    with tempfile.TemporaryDirectory() as workdir:
        for set_spec in spec["sets"]:
            if only and set_spec["name"] not in only:
                continue
            if set_spec["transform"] not in TRANSFORMS:
                raise VariantError(f"set {set_spec['name']!r}: unknown transform {set_spec['transform']!r}")
            for base_id in set_spec["files"]:
                yield set_spec, base_id, *build_variant(spec, set_spec, base_id, root, build_dir, workdir)
