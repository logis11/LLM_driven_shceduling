"""The RQ0 gate evaluator and the per-experiment spec (Phase 8 spec, decisions
1–8, 12–14, 21; sub-task 8.7).

A per-experiment spec (`harness/experiments/<id>.yaml`, schema in
`harness/experiments/schema/`) names, in its generic part, the conditions,
the seed count, the boot defaults, the judging and reporting files, the
derived Layer-1 exclusions, the guard exemptions, the reporting lines, and
the pins; its criterion section is typed. `lint_spec` checks it against the
schema, the compiled files, the pinned scoring spec's terms, the guard
registry, the registries of criterion and line types, and the pins' bytes.

`evaluate` reads a spec and the harness's four output files — aggregates,
scores, guards, grades — verifies the pins, computes every file's score per
condition, applies the criterion, echoes the spec's pre-registered
statements, and returns the report: one JSON document
(schema `report.schema.json`) whose every number carries the fields that
locate it. A pin mismatch, an incomplete run set, or an unknown type is a
refusal (`GateError`), never a verdict. A non-exempt guard failure on a run
the criterion reads makes the verdict `invalid`, naming the guard and the
run; the per-file rows are still computed. `render` writes the report as
Markdown; nothing in the rendering is computed there.

Every judgement applied here is data in the spec, never a constant in code.
"""

import decimal
import hashlib
import json
import pathlib
from decimal import Decimal
from fractions import Fraction
from typing import Dict, List

import jsonschema
import yaml

from . import aggregates as agg
from . import grader, guards, scorer, scoring
from .outputs import read_csv

HARNESS = pathlib.Path(__file__).resolve().parents[2]
EXPERIMENTS = HARNESS / "experiments"
SPEC_SCHEMA = EXPERIMENTS / "schema" / "experiment-spec.schema.json"
REPORT_SCHEMA = EXPERIMENTS / "schema" / "report.schema.json"

CONDITIONS = ("fixed", "random", "whitelist", "llm_vocab", "llm_algo", "llm_full", "oracle")
PINS = ("scoring_spec", "guard_spec", "driver_table", "dataset")
PROVENANCE_AGGREGATES = tuple(f"time_share_{p}" for p in agg.PROVENANCES) + ("fallback_share",)
PLACES = scorer.PLACES


class GateError(ValueError):
    """A refusal: the inputs are not the pre-registered experiment, or are incomplete."""


def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fmt(x) -> str:
    return agg.fmt(x, PLACES)


def _sqrt(x: Fraction) -> Fraction:
    """The square root of a non-negative rational, correctly rounded at 40 digits."""
    with decimal.localcontext() as c:
        c.prec = 40
        return Fraction((Decimal(x.numerator) / Decimal(x.denominator)).sqrt())


def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _schema_errors(spec):
    schema = json.loads(SPEC_SCHEMA.read_text())
    validator = jsonschema.Draft202012Validator(schema)
    out = []
    for err in sorted(validator.iter_errors(spec), key=lambda e: [str(p) for p in e.absolute_path]):
        where = "/".join(str(p) for p in err.absolute_path)
        out.append(f"{where + ': ' if where else ''}{err.message}")
    return out


def _pin_errors(spec, root):
    errors = []
    for name in PINS:
        pin = (spec.get("pins") or {}).get(name)
        if not isinstance(pin, dict):
            continue
        path = pathlib.Path(root) / pin.get("path", "")
        if not path.is_file():
            errors.append(f"pins/{name}: {pin.get('path')!r} is not a file under {root}")
            continue
        actual = _sha256(path)
        if actual != pin.get("sha256"):
            errors.append(f"pins/{name}: sha256 {actual} of {pin.get('path')} != pinned {pin.get('sha256')}")
    return errors


def _listed(spec):
    files = spec.get("files") or {}
    return list(files.get("judging") or []), list(files.get("reporting") or [])


# --------------------------------------------------------------------- lint

def lint_spec(spec_path, schema_path, build_dir, root):
    """Error strings; empty means the spec is legal. `build_dir` holds the
    compiled `<id>.workload.json` files, `root` resolves the pins' paths."""
    spec_path = pathlib.Path(spec_path)
    try:
        spec = load_spec(spec_path)
    except yaml.YAMLError as err:
        return [f"{spec_path.name}: YAML error: {err}"]
    if not isinstance(spec, dict):
        return [f"{spec_path.name}: not a mapping"]
    errors = _schema_errors(spec)
    if errors:
        return errors
    build_dir = pathlib.Path(build_dir)
    judging, reporting = _listed(spec)
    conditions = spec["conditions"]

    crit = spec["criterion"]
    if crit["type"] not in CRITERIA:
        errors.append(f"criterion type {crit['type']!r} is not registered ({', '.join(CRITERIA)})")
    else:
        for key in ("reference", "compared"):
            if crit.get(key) not in conditions:
                errors.append(f"criterion {key} {crit.get(key)!r} is not one of the experiment's conditions")
    for i, line in enumerate(spec["reporting_lines"]):
        if line["type"] not in LINES:
            errors.append(f"reporting_lines/{i}: type {line['type']!r} is not registered ({', '.join(LINES)})")
        elif line["type"] == "sensitivity":
            for stem in line["boot_defaults"]:
                if stem not in spec["boot_defaults"]["alternatives"]:
                    errors.append(f"reporting_lines/{i}: boot default {stem!r} is not an alternative")
            for stem in line.get("reasons") or {}:
                if stem != spec["boot_defaults"]["primary"] and stem not in line["boot_defaults"]:
                    errors.append(f"reporting_lines/{i}: reason for {stem!r}, which is neither the primary "
                                  f"nor a boot default of the line")
        elif line["type"] == "note" and line["workload"] not in judging + reporting:
            errors.append(f"reporting_lines/{i}: note workload {line['workload']!r} is not a listed file")
    for i, ex in enumerate(spec["guard_exemptions"]):
        if ex["guard"] not in guards.GUARDS:
            errors.append(f"guard_exemptions/{i}: guard {ex['guard']!r} is not in the guard registry")
        if ex["workload"] not in judging + reporting:
            errors.append(f"guard_exemptions/{i}: workload {ex['workload']!r} is not a listed file")
        for c in ex.get("conditions") or []:
            if c not in conditions:
                errors.append(f"guard_exemptions/{i}: condition {c!r} is not one of the experiment's")
    both = sorted(set(judging) & set(reporting))
    if both:
        errors.append(f"files listed as both judging and reporting: {both}")

    # the compiled files and the derived exclusions
    with_miss = []
    for wid in judging + reporting:
        path = build_dir / f"{wid}.workload.json"
        if not path.is_file():
            errors.append(f"file {wid!r} is not in the build ({build_dir})")
            continue
        try:
            segments = grader.read_ground_truth(path)
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f"file {wid!r}: unreadable ground truth: {exc}")
            continue
        if any(s.pre_committed_miss for s in segments):
            with_miss.append(wid)
    declared = sorted(spec["layer1_exclusions"])
    if declared != sorted(with_miss) and not any("is not in the build" in e for e in errors):
        errors.append(f"layer1_exclusions {declared} != the files carrying pre_committed_miss "
                      f"{sorted(with_miss)}; the list is derived, never authoritative")

    # the pinned scoring spec's terms
    errors.extend(_pin_errors(spec, root))
    scoring_path = pathlib.Path(root) / spec["pins"]["scoring_spec"]["path"]
    if scoring_path.is_file():
        try:
            terms = (scoring.load_spec(scoring_path) or {}).get("files") or {}
        except yaml.YAMLError as err:
            terms = {}
            errors.append(f"pins/scoring_spec: YAML error: {err}")
        for wid in judging:
            if not ((terms.get(wid) or {}).get("terms")):
                errors.append(f"judging file {wid!r} has no scoring terms in the pinned scoring spec")
    return errors


# ------------------------------------------------------------ the run set

def _identity(row):
    return tuple(row[k] for k in agg.IDENTITY)


def _read_inputs(aggregates_path, scores_path, guards_path, grades_path):
    return (read_csv(aggregates_path, agg.COLUMNS), read_csv(scores_path, scorer.COLUMNS),
            read_csv(guards_path, guards.COLUMNS), read_csv(grades_path, grader.COLUMNS))


class _Set:
    """The experiment's run set as the four files describe it."""

    def __init__(self, spec, agg_rows, score_rows, guard_rows, grade_rows):
        self.spec = spec
        self.judging, self.reporting = _listed(spec)
        self.listed = self.judging + self.reporting
        self.agg_rows = [r for r in agg_rows if r["workload_id"] in self.listed]
        self.file_rows = {_identity(r): r for r in score_rows
                          if r["level"] == "file" and r["workload_id"] in self.listed}
        self.guard_rows = [r for r in guard_rows if r["workload_id"] in self.listed]
        self.grade_rows = grade_rows
        crit = spec["criterion"]
        self.reference, self.compared = crit["reference"], crit["compared"]
        self.n_seeds = int(spec["seed_count"])
        self.boots = [""] + list(spec["boot_defaults"]["alternatives"])

    def scored(self, wid, condition, boot):
        """File-level score rows of `condition` on `wid` scored against `boot`, by seed."""
        return {k[3]: r for k, r in self.file_rows.items()
                if k[0] == wid and k[1] == condition and k[4] == boot}

    def runs_feeding(self, wid, boot):
        """Identities (own) of the runs a gap under `boot` reads."""
        found = set()
        for key in self.file_rows:
            if key[0] != wid:
                continue
            cond = key[1]
            if cond == "fixed" and key[4] == boot:
                # the scorer stamps fixed's rows with the group's table; the run itself has none
                found.add((wid, "fixed", "", "", boot))
            elif cond in (self.reference, self.compared) and key[4] == boot:
                found.add((wid, cond, key[2], key[3], ""))
        return found

    def check_complete(self):
        for wid in self.judging:
            for boot in self.boots:
                fixed = [k for k in self.file_rows if k[0] == wid and k[1] == "fixed" and k[4] == boot]
                if not fixed:
                    raise GateError(f"{wid}: no fixed run scored against boot default {boot or 'the primary'!r}")
                if not self.scored(wid, self.reference, boot):
                    raise GateError(f"{wid}: no {self.reference} run scored against boot default "
                                    f"{boot or 'the primary'!r}")
                seeds = self.scored(wid, self.compared, boot)
                if len(seeds) != self.n_seeds:
                    raise GateError(f"{wid}: {len(seeds)} {self.compared} seed(s) scored against boot default "
                                    f"{boot or 'the primary'!r}, the spec names {self.n_seeds}: "
                                    f"{sorted(seeds) or 'none'}"
                                    + (f"; missing among the expected" if len(seeds) < self.n_seeds else ""))
            guarded = {_identity(r) for r in self.guard_rows if r["workload_id"] == wid}
            for run in sorted(self.runs_feeding(wid, "")):
                if run not in guarded:
                    raise GateError(f"{wid}: no guard rows for run {run[1]}"
                                    f"{' seed ' + run[3] if run[3] else ''}; the guards were not run on it")


# ------------------------------------------------------------- criterion

def _exempt(spec, row):
    for ex in spec["guard_exemptions"]:
        if ex["guard"] != row["guard"] or ex["workload"] != row["workload_id"]:
            continue
        if ex.get("conditions") and row["condition"] not in ex["conditions"]:
            continue
        return ex["reason"]
    return None


def _gap_rows(rs: _Set, g: Fraction, file_rows=None, boots=None, unavailable=()):
    """One gap row per listed file per boot default, from `file_rows` (default the set's)."""
    file_rows = rs.file_rows if file_rows is None else file_rows
    rows = []
    for wid in rs.listed:
        for boot in (rs.boots if boots is None else boots):
            ref = {k[3]: r for k, r in file_rows.items() if k[0] == wid and k[1] == rs.reference and k[4] == boot}
            cmp = {k[3]: r for k, r in file_rows.items() if k[0] == wid and k[1] == rs.compared and k[4] == boot}
            if not ref or not cmp:
                continue
            ref_row = next(iter(ref.values()))
            ref_score = Fraction(ref_row["weight_sum"])
            scores = {seed: Fraction(r["score"]) for seed, r in sorted(cmp.items())}
            mean = sum(scores.values(), Fraction(0)) / len(scores)
            gap = 1 - mean / ref_score if ref_score else Fraction(0)
            n_terms, n_nh = int(ref_row["n_terms"]), int(ref_row["n_no_headroom"])
            all_nh = n_terms > 0 and n_nh == n_terms
            rows.append({"workload_id": wid, "judging": wid in rs.judging, "boot_default": boot,
                         "reference_score": fmt(ref_score),
                         "compared_scores": [{"seed": s, "score": fmt(v)} for s, v in scores.items()],
                         "compared_mean": fmt(mean), "gap": fmt(gap),
                         "meets_g": bool(gap >= g and not all_nh),
                         "all_no_headroom": all_nh, "n_no_headroom": n_nh, "n_terms": n_terms,
                         "random_beats_oracle": bool(mean > ref_score),
                         "available": (wid, boot) not in unavailable})
    return rows


def _count(gap_rows, boot, k):
    judging = [r for r in gap_rows if r["judging"] and r["boot_default"] == boot]
    met = sum(1 for r in judging if r["meets_g"])
    available = all(r["available"] for r in judging)
    verdict = ("pass" if met >= k else "fail") if available else None
    return {"met": met, "judging": len(judging), "verdict": verdict, "available": available}


def k_of_n_gap(rs: _Set, crit, guard_report):
    """RQ0's criterion (Phase 8 spec, decisions 2–6): at least K of the judging
    files show a gap of at least g, the gap being one minus the compared
    condition's seed-mean score over the reference's, with a failed non-exempt
    guard on a run the criterion reads making the verdict invalid."""
    k, g = int(crit["k"]), Fraction(str(crit["g"]))
    failing = {(r["workload_id"], r["condition"], r["table"], r["seed"], r["boot_default"]): r
               for r in guard_report if r["result"] == "fail" and not r["exempt"]}
    unavailable = set()
    invalid_runs = []
    for wid in rs.judging:
        for boot in rs.boots:
            hit = sorted(run for run in rs.runs_feeding(wid, boot) if run in failing)
            if hit:
                unavailable.add((wid, boot))
            if boot == "":
                for run in hit:
                    row = failing[run]
                    row["invalidating"] = True
                    invalid_runs.append({**{c: row[c] for c in agg.IDENTITY}, "guard": row["guard"]})
    gaps = _gap_rows(rs, g, unavailable=unavailable)
    primary = _count(gaps, "", k)
    verdict = "invalid" if invalid_runs else primary["verdict"]
    detail = {"met": primary["met"], "judging": primary["judging"], "k": k, "invalid_runs": invalid_runs}
    shown = {"type": "k_of_n_gap", "k": k, "g": fmt(g), "reference": crit["reference"],
             "compared": crit["compared"], "seed_statistic": crit["seed_statistic"]}
    return verdict, detail, gaps, shown, {"g": g, "k": k, "unavailable": unavailable}


CRITERIA = {"k_of_n_gap": k_of_n_gap}


# ------------------------------------------------------- reporting lines

def line_sensitivity(rs, params, ctx):
    reasons = dict(params.get("reasons") or {})
    primary = rs.spec["boot_defaults"]["primary"]
    rows = [dict(boot_default=b, **_count(ctx["gaps"], b, ctx["k"]), reason=reasons.get(b or primary, ""))
            for b in [""] + list(params["boot_defaults"])]
    return {"type": "sensitivity", "boot_defaults": list(params["boot_defaults"]), "reasons": reasons, "rows": rows}


def line_g_band(rs, params, ctx):
    """The verdict count under each gap threshold of the band (8.8): the same
    gap rows judged against a different g, on the primary boot default."""
    rows = []
    for g in params["gaps"]:
        gap_rows = _gap_rows(rs, Fraction(str(g)), boots=[""], unavailable=ctx["unavailable"])
        count = _count(gap_rows, "", ctx["k"])
        rows.append({"g": str(g), "met": count["met"], "judging": count["judging"], "verdict": count["verdict"]})
    return {"type": "g_band", "gaps": [str(g) for g in params["gaps"]], "rows": rows}


def line_seed_standard_error(rs, params, ctx):
    """Per judging file on the primary boot default: the sample standard
    deviation of the compared condition's per-seed file scores, its standard
    error (over the square root of the seed count), and that error as a share
    of the reference score — the precision the seed count buys (8.8)."""
    rows = []
    for r in ctx["gaps"]:
        if not r["judging"] or r["boot_default"] != "":
            continue
        scores = [Fraction(s["score"]) for s in r["compared_scores"]]
        n = len(scores)
        mean = sum(scores, Fraction(0)) / n
        ref = Fraction(r["reference_score"])
        if n > 1:
            variance = sum((s - mean) ** 2 for s in scores) / (n - 1)
            sd, se = _sqrt(variance), _sqrt(variance / n)
            row = {"workload_id": r["workload_id"], "n_seeds": n, "compared_mean": fmt(mean),
                   "standard_deviation": fmt(sd), "standard_error": fmt(se),
                   "standard_error_share": fmt(se / ref) if ref else ""}
        else:
            row = {"workload_id": r["workload_id"], "n_seeds": n, "compared_mean": fmt(mean),
                   "standard_deviation": "", "standard_error": "", "standard_error_share": ""}
        rows.append(row)
    return {"type": "seed_standard_error", "rows": rows}


def line_floor_band(rs, params, ctx):
    spec = scoring.load_spec(ctx["scoring_spec_path"])
    rows, gaps = [], []
    for floor in params["latency_floors_us"]:
        _, file_rows = scorer.score(rs.agg_rows, spec, floors=scorer.floors_for(latency_floor_us=floor))
        rescored = {_identity(r): r for r in file_rows if r["workload_id"] in rs.listed}
        gap_rows = _gap_rows(rs, ctx["g"], file_rows=rescored, boots=[""], unavailable=ctx["unavailable"])
        count = _count(gap_rows, "", ctx["k"])
        rows.append({"latency_floor_us": int(floor), "met": count["met"], "judging": count["judging"],
                     "verdict": count["verdict"]})
        for r in gap_rows:
            if r["judging"]:
                gaps.append({"latency_floor_us": int(floor), "workload_id": r["workload_id"],
                             "reference_score": r["reference_score"], "compared_mean": r["compared_mean"],
                             "gap": r["gap"], "meets_g": r["meets_g"], "all_no_headroom": r["all_no_headroom"]})
    return {"type": "floor_band", "latency_floors_us": [int(f) for f in params["latency_floors_us"]],
            "rows": rows, "gaps": gaps}


def _grade_stat(rows, condition, table, axis, statistic, excluded, over_seeds=1):
    return next((r for r in rows if r["condition"] == condition and r["table"] == table and r["seed"] == ""
                 and r["level"] == "statistic" and r["axis"] == axis and r["statistic"] == statistic
                 and int(r["pre_committed_miss_excluded"]) == excluded and int(r["over_seeds"]) == over_seeds),
                None)


def line_exclusion_accuracy(rs, params, ctx):
    rows = []
    for condition, table in sorted({(r["condition"], r["table"]) for r in rs.grade_rows}):
        for axis, statistic in sorted(grader.HEADLINE.items()):
            ex = _grade_stat(rs.grade_rows, condition, table, axis, statistic, 1)
            inc = _grade_stat(rs.grade_rows, condition, table, axis, statistic, 0)
            if ex is None or inc is None:
                continue
            rows.append({"condition": condition, "table": table, "axis": axis, "statistic": statistic,
                         "excluded": ex["value"], "included": inc["value"],
                         "n_excluded": int(ex["n"]), "n_included": int(inc["n"])})
    return {"type": "exclusion_accuracy", "rows": rows}


def line_layer1_headline(rs, params, ctx):
    rows = []
    for condition, table in sorted({(r["condition"], r["table"]) for r in rs.grade_rows}):
        head = _grade_stat(rs.grade_rows, condition, table, "attribute", "balanced_accuracy", 1)
        if head is None:
            continue
        cells = [{"seed": r["seed"], "truth": r["truth"], "predicted": r["predicted"], "count": int(r["n"])}
                 for r in rs.grade_rows
                 if r["condition"] == condition and r["table"] == table and r["level"] == "confusion"
                 and r["axis"] == "attribute" and int(r["pre_committed_miss_excluded"]) == 1
                 and int(r["over_seeds"]) == 0]                 # cells are counts, per seed only
        cells.sort(key=lambda c: (c["seed"], c["truth"], c["predicted"]))
        rows.append({"condition": condition, "table": table, "balanced_accuracy": head["value"],
                     "ci_low": head["ci_low"], "ci_high": head["ci_high"], "n": int(head["n"]),
                     "n_files": int(head["n_files"]), "n_seeds": int(head["n_seeds"]), "confusion": cells})
    return {"type": "layer1_headline", "rows": rows}


def line_random_beats_oracle(rs, params, ctx):
    rows = [{"workload_id": r["workload_id"], "flagged": r["random_beats_oracle"], "gap": r["gap"]}
            for r in ctx["gaps"] if r["judging"] and r["boot_default"] == ""]
    return {"type": "random_beats_oracle", "rows": rows}


def line_note(rs, params, ctx):
    return {"type": "note", "workload_id": params["workload"], "text": params["text"]}


LINES = {"sensitivity": line_sensitivity, "g_band": line_g_band, "seed_standard_error": line_seed_standard_error,
         "floor_band": line_floor_band,
         "exclusion_accuracy": line_exclusion_accuracy, "layer1_headline": line_layer1_headline,
         "random_beats_oracle": line_random_beats_oracle, "note": line_note}


# --------------------------------------------------------------- evaluate

def evaluate(spec_path, aggregates_path, scores_path, guards_path, grades_path, root):
    """The report for one experiment run, or a `GateError` refusal."""
    spec_path = pathlib.Path(spec_path)
    try:
        spec = load_spec(spec_path)
    except yaml.YAMLError as err:
        raise GateError(f"{spec_path.name}: YAML error: {err}") from None
    problems = _schema_errors(spec) if isinstance(spec, dict) else ["not a mapping"]
    if problems:
        raise GateError(f"{spec_path.name}: " + "; ".join(problems))
    pins = _pin_errors(spec, root)
    if pins:
        raise GateError("pin mismatch: " + "; ".join(pins))
    crit = spec["criterion"]
    if crit["type"] not in CRITERIA:
        raise GateError(f"criterion type {crit['type']!r} is not registered")
    for line in spec["reporting_lines"]:
        if line["type"] not in LINES:
            raise GateError(f"reporting line type {line['type']!r} is not registered")

    try:
        agg_rows, score_rows, guard_rows, grade_rows = _read_inputs(aggregates_path, scores_path,
                                                                    guards_path, grades_path)
    except (OSError, ValueError) as exc:
        raise GateError(str(exc)) from None
    rs = _Set(spec, agg_rows, score_rows, guard_rows, grade_rows)
    rs.check_complete()

    guard_report = []
    for r in sorted(rs.guard_rows, key=lambda r: (_identity(r), guards.GUARDS.index(r["guard"]))):
        reason = _exempt(spec, r) if r["result"] == "fail" else None
        guard_report.append({**{c: r[c] for c in guards.COLUMNS}, "exempt": reason is not None,
                             "exemption_reason": reason or "", "invalidating": False})

    verdict, detail, gaps, shown, ctx = CRITERIA[crit["type"]](rs, crit, guard_report)
    ctx.update({"gaps": gaps, "scoring_spec_path": pathlib.Path(root) / spec["pins"]["scoring_spec"]["path"]})

    scores_out = [{**{c: r[c] for c in agg.IDENTITY}, "score": r["score"], "weight_sum": r["weight_sum"],
                   "n_terms": int(r["n_terms"]), "n_no_headroom": int(r["n_no_headroom"]),
                   "n_censored": int(r["n_censored"])}
                  for _, r in sorted(rs.file_rows.items())]
    provenance = {}
    for r in rs.agg_rows:
        if r["entity"] == "schedule" and r["metric"] == "config_interval" and r["aggregate"] in PROVENANCE_AGGREGATES \
                and not r["cause"] and not r["window_start_us"] and not r["window_end_us"]:
            provenance.setdefault(_identity(r), {c: r[c] for c in agg.IDENTITY})[r["aggregate"]] = r["value"]
    prov_out = [provenance[k] for k in sorted(provenance) if all(a in provenance[k] for a in PROVENANCE_AGGREGATES)]

    lines = [LINES[line["type"]](rs, line, ctx) for line in spec["reporting_lines"]]
    return {"experiment": spec["experiment"], "spec_sha256": _sha256(spec_path), "pins": spec["pins"],
            "conditions": list(spec["conditions"]), "seed_count": int(spec["seed_count"]),
            "boot_defaults": spec["boot_defaults"], "criterion": shown,
            "verdict": verdict, "verdict_detail": detail, "gaps": gaps, "scores": scores_out,
            "provenance": prov_out, "guards": guard_report,
            "statements": [dict(s) for s in spec.get("statements") or []], "lines": lines}


def write_report(report, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
        f.write("\n")


def validate_report(report):
    jsonschema.Draft202012Validator(json.loads(REPORT_SCHEMA.read_text())).validate(report)


# ------------------------------------------------------------------ render

def _table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def _ident(r):
    return f"{r['workload_id']} · {r['condition']}" + (f" · {r['seed']}" if r["seed"] else "") \
        + (f" · boot {r['boot_default']}" if r["boot_default"] else "")


def render(report) -> str:
    """The report as Markdown. Every number is copied from the report; none is computed here."""
    c = report["criterion"]
    d = report["verdict_detail"]
    out = [f"# Report — {report['experiment']}", "",
           f"**Verdict: {report['verdict']}** — {d['met']} of {d['judging']} judging files met the criterion "
           f"(K = {d['k']}). Spec `{report['spec_sha256'][:12]}`.", ""]
    if d["invalid_runs"]:
        out.append("Invalidating guard failures (non-exempt, on runs the criterion reads):")
        out.append("")
        for r in d["invalid_runs"]:
            out.append(f"- `{r['guard']}` on {_ident(r)}")
        out.append("")
    out += ["## Criterion", "", _table(["field", "value"], [[k, v] for k, v in c.items()]), "",
            "## Pins", "",
            _table(["pin", "path", "sha256", "version"],
                   [[k, v["path"], v["sha256"], v.get("version", "")] for k, v in report["pins"].items()]), "",
            *(["## Statements", ""] + [f"**{s['id']}** — {s['text']}\n" for s in report["statements"]]
              if report["statements"] else []),
            "## Per-file gaps", "",
            _table(["workload", "judging", "boot default", "reference", "compared (per seed)", "mean", "gap",
                    "meets g", "no headroom", "random beats oracle", "available"],
                   [[r["workload_id"], r["judging"], r["boot_default"] or "(primary)", r["reference_score"],
                     ", ".join(f"{s['seed']}: {s['score']}" for s in r["compared_scores"]),
                     r["compared_mean"], r["gap"], r["meets_g"], f"{r['n_no_headroom']}/{r['n_terms']}"
                     + (" (all)" if r["all_no_headroom"] else ""), r["random_beats_oracle"], r["available"]]
                    for r in report["gaps"]]), ""]
    for line in report["lines"]:
        t = line["type"]
        out.append(f"## Line: {t}")
        out.append("")
        if t == "sensitivity":
            out.append(_table(["boot default", "met", "judging", "verdict", "available", "reason"],
                              [[r["boot_default"] or "(primary)", r["met"], r["judging"], r["verdict"],
                                r["available"], r["reason"]] for r in line["rows"]]))
        elif t == "g_band":
            out.append(_table(["g", "met", "judging", "verdict"],
                              [[r["g"], r["met"], r["judging"], r["verdict"]] for r in line["rows"]]))
        elif t == "seed_standard_error":
            out.append(_table(["workload", "seeds", "mean", "sd", "standard error", "as share of reference"],
                              [[r["workload_id"], r["n_seeds"], r["compared_mean"], r["standard_deviation"],
                                r["standard_error"], r["standard_error_share"]] for r in line["rows"]]))
        elif t == "floor_band":
            out.append(_table(["latency floor (µs)", "met", "judging", "verdict"],
                              [[r["latency_floor_us"], r["met"], r["judging"], r["verdict"]] for r in line["rows"]]))
            out.append("")
            out.append(_table(["latency floor (µs)", "workload", "reference", "mean", "gap", "meets g", "all no headroom"],
                              [[r["latency_floor_us"], r["workload_id"], r["reference_score"], r["compared_mean"],
                                r["gap"], r["meets_g"], r["all_no_headroom"]] for r in line["gaps"]]))
        elif t == "exclusion_accuracy":
            out.append(_table(["condition", "table", "axis", "statistic", "excluded (headline)", "included",
                               "n excluded", "n included"],
                              [[r["condition"], r["table"], r["axis"], r["statistic"], r["excluded"], r["included"],
                                r["n_excluded"], r["n_included"]] for r in line["rows"]]))
        elif t == "layer1_headline":
            out.append(_table(["condition", "table", "balanced accuracy", "CI", "n", "files", "seeds"],
                              [[r["condition"], r["table"], r["balanced_accuracy"],
                                f"[{r['ci_low']}, {r['ci_high']}]" if r["ci_low"] else "", r["n"], r["n_files"],
                                r["n_seeds"]] for r in line["rows"]]))
            for r in line["rows"]:
                if r["confusion"]:
                    out.append("")
                    out.append(f"Confusion, attribute, {r['condition']} ({r['table']}):")
                    out.append("")
                    out.append(_table(["seed", "truth", "predicted", "count"],
                                      [[c["seed"] or "(one)", c["truth"], c["predicted"], c["count"]]
                                       for c in r["confusion"]]))
        elif t == "random_beats_oracle":
            out.append(_table(["workload", "flagged", "gap"],
                              [[r["workload_id"], r["flagged"], r["gap"]] for r in line["rows"]]))
        elif t == "note":
            out.append(f"**{line['workload_id']}** — {line['text']}")
        out.append("")
    fails = [r for r in report["guards"] if r["result"] == "fail"]
    out += ["## Guards", "",
            f"{sum(1 for r in report['guards'] if r['result'] == 'pass')} pass, {len(fails)} fail, "
            f"{sum(1 for r in report['guards'] if r['result'] == 'not_applicable')} not applicable.", ""]
    if fails:
        out.append(_table(["run", "guard", "value", "threshold", "reason", "exempt", "invalidating"],
                          [[_ident(r), r["guard"], r["value"], r["threshold"], r["reason"],
                            (r["exemption_reason"] if r["exempt"] else "no"), r["invalidating"]] for r in fails]))
        out.append("")
    out += ["## Provenance breakdown", "",
            _table(["run", "unmodified", "clamped", "held", "fallback", "fallback share"],
                   [[_ident(r), r["time_share_unmodified"], r["time_share_clamped"], r["time_share_held"],
                     r["time_share_fallback"], r["fallback_share"]] for r in report["provenance"]]), "",
            "## Scores", "",
            _table(["run", "scored against", "score", "weight sum", "terms", "no headroom", "censored"],
                   [[f"{r['workload_id']} · {r['condition']}" + (f" · {r['seed']}" if r["seed"] else ""),
                     r["boot_default"] or "(primary)", r["score"], r["weight_sum"], r["n_terms"],
                     r["n_no_headroom"], r["n_censored"]] for r in report["scores"]]), ""]
    return "\n".join(out)


__all__ = ["CONDITIONS", "CRITERIA", "EXPERIMENTS", "GateError", "LINES", "REPORT_SCHEMA", "SPEC_SCHEMA",
           "evaluate", "lint_spec", "load_spec", "render", "validate_report", "write_report"]
