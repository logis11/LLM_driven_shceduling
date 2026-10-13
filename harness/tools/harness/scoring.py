"""Scoring spec — Phase 6 spec, decisions 5–15.

`harness/scoring/scoring-spec.yaml` says, per coreset file, how its records are
valued: a list of terms, each naming an entity, a primitive, a filter (`cause`,
for a wake term the `channel` kind, a time window), an aggregate, a direction,
and a weight. A file's score is the
weighted sum of its terms' normalised shares (metrics doc §9). The file carries
terms only — which files judge, report, or are excluded is the RQ0 gate spec's.

`lint_spec` checks the file against its JSON schema and against the compiled
coreset: every entity is a task id in that file's compiled workload or a
reserved name; metric and aggregate form a scored pair; the direction is the
pair's; weights are positive; windows lie inside [0, T_end] and on the compiled
file's ground-truth segment boundaries (a window is a segment by design, 9.14
decision 5); a file that
declares a `base` is that base's variant in the dataset's recipes and carries
its terms verbatim — or, when its ground truth flips the base's
`background_wanted` to false, the base's terms minus the batch terms (unwanted
work carries no term, Phase 7 spec decision 10); a variant that declares no
base must differ from its base (identical terms without the declaration are a
forgotten line, not a decision).

The generated layer (9.21 spec, decisions 1–3) has no entries: `with_generated`
derives a generated file's terms at run time from the C1 entries, as
`with_variants` derives a variant's from its base's — per placement the
manifest records (`manifests.py`), the `c1-<mode>` entry's terms with the
placement's id suffix on the entity, the latency and periodic terms windowed to
the segments the placement is labelled in (no window when they span the file),
the batch terms unwindowed; a placement labelled in no segment carries none
(the distractor grid's B); a placement without an input window drops its
`channel: input` terms alone; an idle placement carries none, as `c1-idle` has
no entry. `lint_generated` checks the derived entries against the compiled
generated files as `lint_spec` checks the authored ones.
"""

import json
import pathlib

import jsonschema
import yaml

from . import manifests
from .reader import RESERVED_ENTITIES, RunFileError, read_run_file

HARNESS = pathlib.Path(__file__).resolve().parents[2]
SPEC_PATH = HARNESS / "scoring" / "scoring-spec.yaml"
SCHEMA_PATH = HARNESS / "scoring" / "schema" / "scoring-spec.schema.json"

# Terms an unwanted-flipped counterpart drops: the batch job's (decision 10).
BATCH_METRICS = {"turnaround", "cpu_delivered"}

# (metric, aggregate) → direction. The scored aggregates of spec decision 6;
# every other aggregate of metrics doc §8 is reported beside the score.
LEGAL = {
    ("ready_wait", "p99"): "lower",
    ("job", "miss_rate"): "lower",
    ("cpu_delivered", "progress"): "higher",
    ("turnaround", "turnaround"): "lower",
}
_TERM_KEYS = ("entity", "metric", "aggregate", "direction", "weight")


def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schema(path):
    return json.loads(pathlib.Path(path).read_text())


def variant_bases(recipes_dir):
    """{variant id: base id} from the dataset's `*.variant.yaml` recipes."""
    bases = {}
    for recipe in sorted(pathlib.Path(recipes_dir).glob("*.variant.yaml")):
        doc = yaml.safe_load(recipe.read_text()) or {}
        for v in doc.get("variants", []):
            src = str(v.get("from", ""))
            bases[v["id"]] = src.replace(".timeline.yaml", "")
    return bases


def label_changing_variants(recipes_dir):
    """{variant id: base id} for the recipe variants that change a segment's label —
    its mode or its background_wanted — the C2 pair shape (9.14 decision 7). A variant
    that changes a task's entry alone, as the bounding check's idle download does, is
    not one."""
    out = {}
    for recipe in sorted(pathlib.Path(recipes_dir).glob("*.variant.yaml")):
        doc = yaml.safe_load(recipe.read_text()) or {}
        for v in doc.get("variants", []):
            src = str(v.get("from", "")).replace(".timeline.yaml", "")
            for op in v.get("ops") or []:
                seg = op.get("patch-segment") if isinstance(op, dict) else None
                if isinstance(seg, dict) and ("mode" in seg or "background_wanted" in (seg.get("attributes") or {})):
                    out[v["id"]] = src
                    break
    return out


def label_flipped(build_dir, base, variant):
    """True when some segment is background_wanted true in the base's compiled
    ground truth and false in the variant's (the C7 counterpart shape)."""
    def segments(wid):
        with open(pathlib.Path(build_dir) / f"{wid}.workload.json", encoding="utf-8") as f:
            return json.load(f).get("ground_truth") or []
    pairs = zip(segments(base), segments(variant))
    return any((b.get("attributes") or {}).get("background_wanted") is True
               and (v.get("attributes") or {}).get("background_wanted") is False
               for b, v in pairs)


def segment_bounds(compiled_path):
    """The compiled file's ground-truth segment starts and ends, in µs."""
    with open(compiled_path, encoding="utf-8") as f:
        segments = json.load(f).get("ground_truth") or []
    return ({int(s["t_start"]) for s in segments}, {int(s["t_end"]) for s in segments})


def lint_terms(wid, entry, compiled):
    """One entry's terms against the compiled workload at `compiled`: the entity exists, the metric and aggregate
    form a scored pair with its direction, the weight is positive, the filters belong to their metric, each window
    lies inside the file and on its segment boundaries (9.14 decision 5). Error strings, empty when legal."""
    errors = []
    compiled = pathlib.Path(compiled)
    if not compiled.exists():
        return [f"{wid}: no compiled workload at {compiled}"]
    try:
        run = read_run_file(compiled)
    except (RunFileError, OSError, ValueError) as exc:
        return [f"{wid}: compiled workload unreadable: {exc}"]
    for i, t in enumerate(entry.get("terms") or []):
        if not isinstance(t, dict) or any(k not in t for k in _TERM_KEYS):
            continue                      # the schema already said what is missing
        where = f"{wid}: term {i} ({t['entity']}/{t['metric']}): "
        if t["entity"] not in run.tasks and t["entity"] not in RESERVED_ENTITIES:
            errors.append(f"{where}no task with that id in the compiled workload")
        pair = (t["metric"], t["aggregate"])
        if pair not in LEGAL:
            errors.append(f"{where}{t['metric']} with {t['aggregate']} is not a scored "
                          f"combination (spec decision 6)")
        elif t["direction"] != LEGAL[pair]:
            errors.append(f"{where}direction must be {LEGAL[pair]!r} for {t['aggregate']}")
        if isinstance(t["weight"], bool) or not isinstance(t["weight"], (int, float)) or t["weight"] <= 0:
            errors.append(f"{where}weight must be a positive number")
        if t["metric"] == "ready_wait" and not t.get("cause"):
            errors.append(f"{where}a ready_wait term names its cause")
        if t["metric"] != "ready_wait" and "cause" in t:
            errors.append(f"{where}cause is a ready_wait filter only")
        if "channel" in t and (t["metric"] != "ready_wait" or t.get("cause") != "wake"):
            errors.append(f"{where}channel is a filter of a ready_wait term with cause wake only")
        win = t.get("window")
        if isinstance(win, dict) and all(isinstance(win.get(k), int) for k in ("start_us", "end_us")):
            if not (0 <= win["start_us"] < win["end_us"] <= run.t_end):
                errors.append(f"{where}window [{win['start_us']}, {win['end_us']}] is not "
                              f"inside [0, T_end={run.t_end}] or is empty")
            else:
                # 9.14 decision 5: a window is a segment by design, so each bound must be a
                # ground-truth segment boundary of the compiled file; a stale window in
                # either direction fails here
                starts, ends = segment_bounds(compiled)
                if win["start_us"] not in starts or win["end_us"] not in ends:
                    errors.append(f"{where}window [{win['start_us']}, {win['end_us']}] does not lie on "
                                  f"the file's segment boundaries (starts {sorted(starts)}, "
                                  f"ends {sorted(ends)})")
    return errors


def lint_spec(spec_path, schema_path, build_dir, recipes_dir):
    """Returns a list of error strings; empty means the spec is legal."""
    spec_path = pathlib.Path(spec_path)
    try:
        spec = load_spec(spec_path)
    except yaml.YAMLError as err:
        return [f"{spec_path.name}: YAML error: {err}"]
    errors = []
    validator = jsonschema.Draft202012Validator(load_schema(schema_path))
    for err in sorted(validator.iter_errors(spec), key=lambda e: [str(p) for p in e.absolute_path]):
        errors.append(f"{_where(err.absolute_path)}{err.message}")
    files = spec.get("files") if isinstance(spec, dict) else None
    if not isinstance(files, dict):
        return errors

    build_dir = pathlib.Path(build_dir)
    bases = variant_bases(recipes_dir)
    for wid, entry in files.items():
        if not isinstance(entry, dict):
            continue
        compiled = build_dir / f"{wid}.workload.json"
        term_errors = lint_terms(wid, entry, compiled)
        errors.extend(term_errors)
        if any(e.endswith(f"no compiled workload at {compiled}") or "compiled workload unreadable" in e
               for e in term_errors):
            continue
        if "base" not in entry and wid in bases and bases[wid] in files:
            base_entry = files[bases[wid]]
            if isinstance(base_entry, dict) and entry.get("terms") == base_entry.get("terms"):
                errors.append(f"{wid}: a variant of {bases[wid]!r} carrying its terms unchanged "
                              f"must declare base: {bases[wid]}")
        if "base" in entry:
            base = entry["base"]
            if wid not in bases:
                errors.append(f"{wid}: declares base {base!r} but is not a variant in the "
                              f"dataset's recipes")
            elif bases[wid] != base:
                errors.append(f"{wid}: declares base {base!r} but the recipe says {bases[wid]!r}")
            if base not in files:
                errors.append(f"{wid}: base {base!r} has no entry in the spec")
            elif entry.get("terms") != files[base].get("terms"):
                base_terms = files[base].get("terms") or []
                compiled_base = build_dir / f"{base}.workload.json"
                if compiled_base.exists() and label_flipped(build_dir, base, wid):
                    kept = [t for t in base_terms
                            if not (isinstance(t, dict) and t.get("metric") in BATCH_METRICS)]
                    if entry.get("terms") != kept:
                        errors.append(f"{wid}: a counterpart that flips {base!r} to unwanted "
                                      f"carries the base's terms minus its batch terms; "
                                      f"they differ")
                else:
                    errors.append(f"{wid}: a derived file carries its base's terms verbatim; "
                                  f"they differ from {base!r}")
    return errors


def _where(path):
    parts = list(path)
    if len(parts) >= 2 and parts[0] == "files":
        rest = parts[2:]
        if len(rest) >= 2 and rest[0] == "terms" and isinstance(rest[1], int):
            tail = "/".join(str(p) for p in rest[2:])
            return f"{parts[1]}: term {rest[1]}: {tail + ': ' if tail else ''}"
        tail = "/".join(str(p) for p in rest)
        return f"{parts[1]}: {tail + ': ' if tail else ''}"
    return ("/".join(str(p) for p in parts) + ": ") if parts else ""


__all__ = ["LEGAL", "SPEC_PATH", "SCHEMA_PATH", "base_id", "generated_entries", "label_changing_variants",
           "lint_generated", "lint_spec", "lint_terms", "load_spec", "suffixed", "variant_bases", "with_generated",
           "with_variants"]


def base_id(workload_id):
    """A variant file's base: the id before `@` (`c7-dev@replay` → `c7-dev`); a base's own id otherwise."""
    return workload_id.split("@", 1)[0]


def with_variants(spec, variant_files):
    """A copy of the scoring spec with an entry per variant file (9.14 decision 12: a rebuilt judging file is
    scored on its base's terms): `variant_files` maps each variant id to its compiled file, whose base lies beside
    it. Each window follows its segment (decision 5: a window is a segment by design): the base's and the
    variant's ground-truth segments are paired by index and a bound on the base's k-th boundary moves to the
    variant's k-th. A variant whose base has no entry gets none; segment lists of different lengths are an error."""
    out = dict(spec, files=dict(spec["files"]))
    for vid, path in sorted(variant_files.items()):
        base = base_id(vid)
        entry = spec["files"].get(base)
        if entry is None or vid in spec["files"]:
            continue
        path = pathlib.Path(path)
        with open(path, encoding="utf-8") as f:
            v_segments = json.load(f).get("ground_truth") or []
        with open(path.parent / f"{base}.workload.json", encoding="utf-8") as f:
            b_segments = json.load(f).get("ground_truth") or []
        if len(v_segments) != len(b_segments):
            raise ValueError(f"{vid}: {len(v_segments)} segments against its base's {len(b_segments)}")
        moved = {}
        for b, v in zip(sorted(b_segments, key=lambda s: int(s["t_start"])),
                        sorted(v_segments, key=lambda s: int(s["t_start"]))):
            moved[int(b["t_start"])] = int(v["t_start"])
            moved[int(b["t_end"])] = int(v["t_end"])
        terms = []
        for term in entry["terms"]:
            term = dict(term)
            w = term.get("window")
            if w:
                try:
                    term["window"] = {"start_us": moved[int(w["start_us"])], "end_us": moved[int(w["end_us"])]}
                except KeyError as err:
                    raise ValueError(f"{vid}: the base's window bound {err} is not a segment boundary") from None
            terms.append(term)
        out["files"][vid] = dict(entry, terms=terms)
    return out


def windows_from_spec(spec, workload_id):
    """{(entity, metric): [(start_us, end_us), …]} named by the workload's terms."""
    out = {}
    entry = spec["files"].get(workload_id)
    if not entry:
        return out
    for term in entry["terms"]:
        w = term.get("window")
        if w:
            out.setdefault((term["entity"], term["metric"]), []).append((w["start_us"], w["end_us"]))
    return out


def interactive_from_spec(spec, workload_id):
    """The entities of the workload's `ready_wait` terms — the interactive tasks the excess aggregates measure."""
    entry = spec["files"].get(workload_id)
    if not entry:
        return ()
    return tuple(dict.fromkeys(t["entity"] for t in entry["terms"] if t["metric"] == "ready_wait"))


def suffixed(entity, k):
    """A C1 entity under a placement's id suffix: the task id carries `-s<k>`, and a chain head's `.chain.<n>` — the
    compiler's member id, formed from the task id — comes after it (`game.chain.1` -> `game-s0.chain.1`)."""
    if ".chain." in entity:
        head, tail = entity.split(".chain.", 1)
        return f"{head}-s{k}.chain.{tail}"
    return f"{entity}-s{k}"


def generated_entries(spec, manifest, only=None):
    """{workload id: entry} the generated-layer rule derives (9.21 decisions 1–3) for the manifest's files, or for the
    ids in `only`. Per placement the manifest records: the `c1-<mode>` entry's terms, the entity suffixed `-s<k>`,
    the latency and periodic terms windowed to the placement's labelled segments (no window when they span the
    file), the batch terms unwindowed; nothing from a placement labelled in no segment, from one whose mode has no
    entry (idle), nor the `channel: input` terms of one without an input window. A file deriving no term has no
    entry. A manifest without placements predates the record and is an error."""
    out = {}
    demand = manifest.get("demand") or {}
    for wid, record in manifests.records(manifest).items():
        if only is not None and wid not in only:
            continue
        if "placements" not in record:
            raise ValueError(f"{wid}: the manifest records no placements (it predates 9.21); run `make generated`")
        segments = {int(s["index"]): (int(s["t_start_us"]), int(s["t_end_us"]))
                    for s in (demand.get(record["_artifact"]) or {}).get("segments") or []}
        if not segments:
            raise ValueError(f"{wid}: the manifest records no segment bounds under demand")
        t_end = max(end for _, end in segments.values())
        terms = []
        for placement in record["placements"]:
            entry = spec["files"].get(f"c1-{placement['mode']}")
            labelled = sorted(int(i) for i in placement["segments"])
            if entry is None or not labelled:
                continue
            if labelled != list(range(labelled[0], labelled[-1] + 1)):
                raise ValueError(f"{wid}: placement -s{placement['suffix']} is labelled in segments {labelled}, "
                                 "which are not contiguous; the rule windows one span")
            start, end = segments[labelled[0]][0], segments[labelled[-1]][1]
            whole = start == 0 and end == t_end
            for term in entry.get("terms") or []:
                if term["metric"] == "ready_wait" and term.get("channel") == "input" and not placement["input"]:
                    continue                                   # decision 3: no keystroke to read
                t = {k: v for k, v in term.items() if k != "window"}
                t["entity"] = suffixed(term["entity"], placement["suffix"])
                if term["metric"] not in BATCH_METRICS and not whole:
                    t["window"] = {"start_us": start, "end_us": end}
                terms.append(t)
        if terms:
            out[wid] = {"terms": terms}
    return out


def with_generated(spec, manifest, only=None):
    """A copy of the scoring spec with the generated-layer rule's entries added for the manifest's files (or the ids
    in `only`); a generated file that already has an entry is an error — the rule, not an entry, scores it."""
    out = dict(spec, files=dict(spec["files"]))
    for wid, entry in generated_entries(spec, manifest, only).items():
        if wid in out["files"]:
            raise ValueError(f"{wid}: a generated file is scored by the rule and cannot also have an entry")
        out["files"][wid] = entry
    return out


def lint_generated(spec, manifest_path):
    """The rule's entries for one generated manifest against the set's compiled files (9.21 decision 1): every
    derived term passes `lint_terms`. Error strings, empty when legal; a missing build is an error that names the
    step to run."""
    manifest_path = pathlib.Path(manifest_path)
    if not manifest_path.is_file():
        return [f"{manifest_path.name}: no manifest (run `make -C dataset generated`)"]
    manifest = manifests.load(manifest_path)
    try:
        entries = generated_entries(spec, manifest)
    except ValueError as err:
        return [f"{manifest_path.name}: {err}"]
    paths = manifests.artifact_paths(manifest_path, manifest)
    errors = []
    for wid, entry in sorted(entries.items()):
        compiled = paths[wid]
        if not compiled.is_file():
            errors.append(f"{wid}: no compiled workload at {compiled} (run `make -C dataset generated`)")
            continue
        errors.extend(lint_terms(wid, entry, compiled))
    return errors
