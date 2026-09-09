"""Scoring spec — Phase 6 spec, decisions 5–15.

`harness/scoring/scoring-spec.yaml` says, per coreset file, how its records are
valued: a list of terms, each naming an entity, a primitive, a filter (`cause`,
a time window), an aggregate, a direction, and a weight. A file's score is the
weighted sum of its terms' normalised shares (metrics doc §9). The file carries
terms only — which files judge, report, or are excluded is the gate spec's.

`lint_spec` checks the file against its JSON schema and against the compiled
coreset: every entity is a task id in that file's compiled workload or a
reserved name; metric and aggregate form a scored pair; the direction is the
pair's; weights are positive; windows lie inside [0, T_end]; a file that
declares a `base` is that base's variant in the dataset's recipes and carries
its terms verbatim; a variant that declares no base must differ from its base
(identical terms without the declaration are a forgotten line, not a decision).
"""

import json
import pathlib

import jsonschema
import yaml

from .reader import RESERVED_ENTITIES, RunFileError, read_run_file

HARNESS = pathlib.Path(__file__).resolve().parents[2]
SPEC_PATH = HARNESS / "scoring" / "scoring-spec.yaml"
SCHEMA_PATH = HARNESS / "scoring" / "schema" / "scoring-spec.schema.json"

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
        if not compiled.exists():
            errors.append(f"{wid}: no compiled workload at {compiled}")
            continue
        try:
            run = read_run_file(compiled)
        except (RunFileError, OSError, ValueError) as exc:
            errors.append(f"{wid}: compiled workload unreadable: {exc}")
            continue
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
            win = t.get("window")
            if isinstance(win, dict) and all(isinstance(win.get(k), int) for k in ("start_us", "end_us")):
                if not (0 <= win["start_us"] < win["end_us"] <= run.t_end):
                    errors.append(f"{where}window [{win['start_us']}, {win['end_us']}] is not "
                                  f"inside [0, T_end={run.t_end}] or is empty")
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
            elif (entry.get("terms") != files[base].get("terms")):
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


__all__ = ["LEGAL", "SPEC_PATH", "SCHEMA_PATH", "lint_spec", "load_spec", "variant_bases"]
