"""The Layer-1 grader — docs/harness/metrics.md §7 and §8; sub-task 8.4 spec.

`grade_log` takes one recognition log (data-contracts §8), the compiled
workload whose `ground_truth` is the answer key, and the driver table, and
returns recognition records rows: entity `recognizer`, `t` the query's
`t_set_change`, one row per metric. A query is graded only when a
non-`ambiguous` ground-truth segment covers its `t_set_change`, so the terminal
snapshot and `c6-dual` drop out. Every row carries `validation`, the covering
segment's `familiarity` when it has one, and `pre_committed_miss`.

`compute_grades` pools those rows across workloads into the `grades` file
(`harness/grades/schema/`). Its rows come at four levels: `statistic`,
`class_recall`, `confusion`, and `paired`. Identity is condition, table and
seed — there is no workload, because Layer 1's numbers are pooled, and the boot
default has no bearing on recognition.

A seed is a repetition of the same question, not a new question, so it is
averaged over rather than pooled: pooling would multiply the observation count
while the query points stayed the same, and hand back intervals that are too
narrow. Each statistic is computed per seed and then averaged, exactly as the
Phase 8 spec's decision 3 does for Layer 2, and both readings are kept — rows
carry `over_seeds` 0 for one seed's own value and 1 for the mean, the latter with
`seed` empty and `n_seeds` saying how many went in. Rates average that way;
raw confusion cell counts do not, because averaging counts gives fractional cells,
so those stay per seed. Paired comparisons run between distinct conditions only,
on seed-averaged values (added 2026-09-11).

Which statistic goes on which axis is decided, not free (spec decision 4). The
attribute is two classes and lopsided, so its headline is balanced accuracy with
the Matthews correlation coefficient beside it. Mode and algorithm choice are
many classes and flat, so they report raw accuracy against a measured majority
baseline, with the confusion matrix and per-class recall. No macro-average is
computed on any axis.

Intervals come from a cluster bootstrap that resamples workload files, because
query points inside one file share its process names and its situation and are
not independent (spec decision 6). Condition comparisons are computed paired, on
the same drawn files. The seed and the repetition count are pinned, so a rerun
is byte-identical.
"""

import hashlib
import itertools
import json
import math
import pathlib
import random
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Optional

import yaml

from .aggregates import fmt as _fmt
from .reader import LogError, read_recognition_log

HARNESS = pathlib.Path(__file__).resolve().parents[2]
GRADES_SCHEMA = HARNESS / "grades" / "schema" / "grades.schema.json"

# recognition-vocabulary.md §1, in the document's own order.
MODES = ("browsing", "office", "mail", "dev", "photo", "meeting", "gaming", "media",
         "video-edit", "compile", "ml-train", "render", "transcode", "indexing",
         "backup", "idle")
ALGORITHMS = ("MLFQ", "EDF", "LOTTERY", "FIFO")
AMBIGUOUS = "ambiguous"

PLACES = 6                       # the grades file's precision; the scores file's too
BOOTSTRAP_SEED = 20260911        # metrics doc §10; pinned so reruns are byte-identical
BOOTSTRAP_REPETITIONS = 10_000   # metrics doc §10
INTERVAL_LEVEL = Fraction(95, 100)

IDENTITY = ("condition", "table", "seed")
COLUMNS = IDENTITY + ("pre_committed_miss_excluded", "over_seeds", "level", "axis",
                      "statistic", "class", "truth", "predicted", "partner_condition",
                      "value", "ci_low", "ci_high", "n", "n_files", "n_seeds")

AXES = ("mode", "attribute", "algo_choice", "configuration", "latency")
HEADLINE = {"mode": "raw_accuracy", "attribute": "balanced_accuracy",
            "algo_choice": "raw_accuracy", "configuration": "correct_rate"}
_LEVEL_ORDER = {"statistic": 0, "class_recall": 1, "confusion": 2, "paired": 3}


class GradeError(ValueError):
    """The grader cannot proceed: a malformed answer key or the wrong table."""


def fmt(x) -> str:
    return _fmt(x, places=PLACES)


# ------------------------------------------------------------- ground truth

@dataclass(frozen=True)
class Segment:
    t_start: int
    t_end: int
    mode: str
    background_wanted: Optional[bool]
    familiarity: Optional[int]
    pre_committed_miss: bool


def read_ground_truth(path) -> List[Segment]:
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    out = []
    for s in doc.get("ground_truth") or []:
        attrs = s.get("attributes") or {}
        out.append(Segment(t_start=int(s["t_start"]), t_end=int(s["t_end"]), mode=s["mode"],
                           background_wanted=attrs.get("background_wanted"),
                           familiarity=s.get("familiarity"),
                           pre_committed_miss=bool(attrs.get("pre_committed_miss"))))
    return out


def covering(segments, t) -> Optional[Segment]:
    """The segment covering an instant, half-open as everywhere else."""
    return next((s for s in segments if s.t_start <= t < s.t_end), None)


# -------------------------------------------------------------- driver table

@dataclass
class DriverTable:
    role: str
    rows: Dict[tuple, dict] = field(default_factory=dict)

    def row(self, mode, wanted) -> Optional[dict]:
        return self.rows.get((mode, bool(wanted)))

    def default_algorithm(self, mode, wanted) -> Optional[str]:
        row = self.row(mode, wanted)
        return None if row is None else row["default"]


def compose_row(row) -> str:
    """The configuration a `system`-only condition receives from this row: the
    envelope the simulator sees, as canonical bytes (data-contracts §10). Kept
    byte-identical with the daemon's own `compose`, which a test pins."""
    algorithm = row["default"]
    entry = row["entries"][algorithm]
    config = {"algorithm": algorithm, "params": entry["params"],
              "batch_bandwidth_cap": row["batch_bandwidth_cap"]}
    return json.dumps(config, sort_keys=True, separators=(",", ":"))


def read_driver_table(path) -> DriverTable:
    doc = yaml.safe_load(pathlib.Path(path).read_text())
    if not isinstance(doc, dict) or not isinstance(doc.get("rows"), list):
        raise GradeError(f"{path}: not a driver table")
    rows = {}
    for r in doc["rows"]:
        rows[(r["mode"], bool(r["background_wanted"]))] = r
    return DriverTable(role=doc.get("role", ""), rows=rows)


# -------------------------------------------------------------------- a run

@dataclass
class Run:
    """One recognition log and the two files needed to grade it."""
    workload_id: str
    condition: str
    table: str                      # the identity column: prior or calibrated
    seed: str
    boot_default: str
    log: pathlib.Path
    workload: pathlib.Path
    table_path: Optional[pathlib.Path] = None

    @property
    def identity(self):
        return (self.condition, self.table, self.seed)


def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _boolstr(v) -> str:
    return "" if v is None else ("true" if v else "false")


def grade_log(run: Run):
    """Recognition records rows for one run, plus consistency messages."""
    try:
        log = read_recognition_log(run.log)
    except LogError as exc:
        raise GradeError(f"{run.log}: {exc}") from None
    segments = read_ground_truth(run.workload)
    table = read_driver_table(run.table_path) if run.table_path else None
    if run.condition == "llm_algo" and table is not None and table.role != "calibrated":
        raise GradeError(f"{run.table_path}: algorithm choice is graded against the calibrated "
                         f"table's default; this table's role is {table.role!r}")

    identity = {"workload_id": run.workload_id, "condition": run.condition,
                "table": run.table, "seed": run.seed, "boot_default": run.boot_default,
                "sim": "", "source_sha256": _sha256(run.log)}
    rows, messages = [], []

    def emit(metric, t, value, attrs):
        row = dict(identity)
        row.update({"entity": "recognizer", "metric": metric, "t": t, "value": value})
        row.update(attrs)
        rows.append(row)

    for query in log.queries:
        seg = covering(segments, query.t_set_change)
        if seg is None or seg.mode == AMBIGUOUS:
            continue                                   # terminal snapshot; c6-dual
        if seg.mode not in MODES:
            raise GradeError(f"{run.workload}: ground-truth mode {seg.mode!r} at "
                             f"t={seg.t_start} is not on the sixteen-mode menu")
        system = (query.proposal or {}).get("system") or {}
        pred_mode = system.get("mode")
        pred_wanted = system.get("background_wanted")
        common = {"validation": query.validation,
                  "pre_committed_miss": 1 if seg.pre_committed_miss else 0}
        if seg.familiarity is not None:
            common["familiarity"] = int(seg.familiarity)

        mode_ok = 1 if pred_mode == seg.mode else 0
        emit("mode_correct", query.t_set_change, mode_ok,
             {**common, "predicted": pred_mode or "", "truth": seg.mode})
        attr_ok = 1 if (pred_wanted is not None and seg.background_wanted is not None
                        and bool(pred_wanted) == bool(seg.background_wanted)) else 0
        emit("attr_correct", query.t_set_change, attr_ok,
             {**common, "predicted": _boolstr(pred_wanted),
              "truth": _boolstr(seg.background_wanted)})
        emit("latency_us", query.t_set_change, int(query.latency_us), dict(common))

        if table is not None:
            if run.condition == "llm_algo":
                named = (((query.proposal or {}).get("subsystems") or {})
                         .get("cpu_scheduler") or {}).get("algorithm")
                truth_alg = table.default_algorithm(seg.mode, seg.background_wanted)
                if truth_alg is None:
                    raise GradeError(f"{run.table_path}: no row for "
                                     f"({seg.mode}, background_wanted="
                                     f"{_boolstr(seg.background_wanted)})")
                emit("algo_choice_correct", query.t_set_change,
                     1 if named == truth_alg else 0,
                     {**common, "predicted": named or "", "truth": truth_alg})
            true_row = table.row(seg.mode, seg.background_wanted)
            if true_row is None:
                raise GradeError(f"{run.table_path}: no row for ({seg.mode}, "
                                 f"background_wanted={_boolstr(seg.background_wanted)})")
            pred_row = (table.row(pred_mode, pred_wanted)
                        if pred_mode in MODES and pred_wanted is not None else None)
            same = pred_row is not None and compose_row(pred_row) == compose_row(true_row)
            emit("config_correct", query.t_set_change, 1 if same else 0, dict(common))

        if run.condition == "oracle" and not (mode_ok and attr_ok):
            messages.append(f"oracle is not perfect: {run.workload_id} at "
                            f"t={query.t_set_change} answered "
                            f"({pred_mode or '<none>'}, {_boolstr(pred_wanted) or '<none>'}) "
                            f"where the answer key says ({seg.mode}, "
                            f"{_boolstr(seg.background_wanted)})")

    rows.sort(key=lambda r: (r["metric"], r["t"]))
    return rows, messages


# -------------------------------------------------------------- the points

@dataclass
class Point:
    """One graded query point, with every metric joined."""
    workload_id: str
    t: int
    excluded: bool                     # True when the segment is a pre-committed miss
    mode_truth: str = ""
    mode_pred: str = ""
    mode_correct: int = 0
    attr_truth: str = ""
    attr_pred: str = ""
    attr_correct: int = 0
    algo_truth: Optional[str] = None
    algo_pred: Optional[str] = None
    algo_correct: Optional[int] = None
    config_correct: Optional[int] = None
    latency_us: Optional[int] = None


def points_by_run(rows) -> Dict[tuple, Dict[str, List[Point]]]:
    """{(condition, table, seed): {workload_id: [Point, …]}}, files in id order."""
    joined: Dict[tuple, Dict[tuple, Point]] = {}
    for r in rows:
        if r.get("entity") != "recognizer":
            continue
        ident = (r["condition"], str(r.get("table", "")), str(r.get("seed", "")))
        key = (r["workload_id"], int(r["t"]))
        p = joined.setdefault(ident, {}).get(key)
        if p is None:
            p = Point(workload_id=r["workload_id"], t=int(r["t"]),
                      excluded=bool(int(r.get("pre_committed_miss", 0) or 0)))
            joined[ident][key] = p
        metric, value = r["metric"], int(r["value"])
        if metric == "mode_correct":
            p.mode_truth, p.mode_pred, p.mode_correct = r.get("truth", ""), r.get("predicted", ""), value
        elif metric == "attr_correct":
            p.attr_truth, p.attr_pred, p.attr_correct = r.get("truth", ""), r.get("predicted", ""), value
        elif metric == "algo_choice_correct":
            p.algo_truth, p.algo_pred, p.algo_correct = r.get("truth", ""), r.get("predicted", ""), value
        elif metric == "config_correct":
            p.config_correct = value
        elif metric == "latency_us":
            p.latency_us = value
    out = {}
    for ident, by_key in joined.items():
        files: Dict[str, List[Point]] = {}
        for (wid, _), p in sorted(by_key.items()):
            files.setdefault(wid, []).append(p)
        out[ident] = dict(sorted(files.items()))
    return out


def _select(files, excluded):
    """{workload_id: [Point]} keeping only points the exclusion rule keeps."""
    out = {}
    for wid, pts in files.items():
        kept = [p for p in pts if not (excluded and p.excluded)]
        if kept:
            out[wid] = kept
    return out


def _pairs(points, axis):
    """(truth, predicted, correct) per point on an axis; None where the axis is absent."""
    out = []
    for p in points:
        if axis == "mode":
            out.append((p.mode_truth, p.mode_pred, p.mode_correct))
        elif axis == "attribute":
            out.append((p.attr_truth, p.attr_pred, p.attr_correct))
        elif axis == "algo_choice":
            if p.algo_correct is not None:
                out.append((p.algo_truth, p.algo_pred, p.algo_correct))
    return out


# ---------------------------------------------------------- the statistics

def raw_accuracy(pairs) -> Optional[Fraction]:
    return Fraction(sum(c for _, _, c in pairs), len(pairs)) if pairs else None


def majority_baseline(pairs) -> Optional[Fraction]:
    if not pairs:
        return None
    counts = Counter(t for t, _, _ in pairs)
    return Fraction(max(counts.values()), len(pairs))


def per_class_recall(pairs) -> Dict[str, Fraction]:
    total, right = Counter(), Counter()
    for truth, _, correct in pairs:
        total[truth] += 1
        right[truth] += correct
    return {k: Fraction(right[k], total[k]) for k in total}


def balanced_accuracy(pairs) -> Optional[Fraction]:
    """The unweighted mean of per-class recall over the classes present in the
    truth (`brodersen-icpr10`; binary axes only, spec decision 4). A class the
    run was never asked about has undefined recall and stays out of the mean."""
    recalls = per_class_recall(pairs)
    if not recalls:
        return None
    return Fraction(sum(recalls.values()), len(recalls))


def matthews(pairs, positive="true", negative="false") -> Optional[Fraction]:
    """The binary Matthews correlation coefficient (`chicco-bmcg20`), over the
    points whose prediction names one of the two classes. A null or off-menu
    answer has no cell in the two-by-two and is left out, so this statistic's
    count is its own; balanced accuracy still counts it against recall."""
    tp = fp = tn = fn = 0
    for truth, pred, _ in pairs:
        if pred not in (positive, negative):
            continue
        if truth == positive:
            tp += pred == positive
            fn += pred == negative
        elif truth == negative:
            tn += pred == negative
            fp += pred == positive
    denom = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    if denom == 0:
        return None                      # a class is empty: the coefficient is undefined
    num = tp * tn - fp * fn
    root = math.isqrt(denom)
    if root * root == denom:
        return Fraction(num, root)
    # integer arithmetic only, so the value is identical on every platform:
    # sqrt(denom) ~ isqrt(denom * 10**(2k)) / 10**k, with k far beyond the file's precision
    k = PLACES + 6
    return Fraction(num * 10 ** k, math.isqrt(denom * 10 ** (2 * k)))


def quantile(sorted_values, q: Fraction):
    """The q-quantile by the linear convention the aggregates module uses."""
    if not sorted_values:
        return None
    n = len(sorted_values)
    pos = Fraction(n - 1) * q
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * frac


def _statistic(name, points, axis):
    """One statistic over a list of points. None where it is undefined."""
    if axis == "configuration":
        vals = [p for p in points if p.config_correct is not None]
        if not vals:
            return None, 0
        if name == "correct_rate":
            return Fraction(sum(p.config_correct for p in vals), len(vals)), len(vals)
        if name == "errors_changing_config":
            errs = [p for p in vals if not (p.mode_correct and p.attr_correct)]
            if not errs:
                return None, 0
            return Fraction(sum(1 for p in errs if not p.config_correct), len(errs)), len(errs)
        return None, 0
    if axis == "latency":
        vals = sorted(p.latency_us for p in points
                      if p.latency_us is not None and p.mode_correct)
        if not vals:
            return None, 0
        q = Fraction(50, 100) if name == "p50" else Fraction(99, 100)
        return quantile([Fraction(v) for v in vals], q), len(vals)
    pairs = _pairs(points, axis)
    if not pairs:
        return None, 0
    if name == "raw_accuracy":
        return raw_accuracy(pairs), len(pairs)
    if name == "majority_baseline":
        return majority_baseline(pairs), len(pairs)
    if name == "balanced_accuracy":
        return balanced_accuracy(pairs), len(pairs)
    if name == "matthews":
        n = sum(1 for _, pred, _ in pairs if pred in ("true", "false"))
        return matthews(pairs), n
    return None, 0


def _by_condition(by_run):
    """{(condition, table): {seed: {workload_id: [Point]}}} — the seed is a
    dimension inside a condition, never a condition of its own."""
    out = {}
    for (condition, table, seed), files in by_run.items():
        out.setdefault((condition, table), {})[seed] = files
    return {k: dict(sorted(v.items())) for k, v in sorted(out.items())}


def _shared_files(seed_files):
    """The files every seed of this condition graded, so each seed weighs the same."""
    sets = [set(f) for f in seed_files.values()]
    return sorted(set.intersection(*sets)) if sets else []


def _seed_mean(seed_files, names, axis, statistic):
    """The statistic per seed over `names`, then the unweighted mean of those.
    Returns (value, per-seed n, seed count); value is None if any seed lacks it."""
    values, n = [], 0
    for seed in sorted(seed_files):
        value, seed_n = _statistic(statistic, _flat(seed_files[seed], names), axis)
        if value is None:
            return None, 0, 0
        values.append(value)
        n = max(n, seed_n)
    if not values:
        return None, 0, 0
    return Fraction(sum(values), len(values)), n, len(values)


# ---------------------------------------------------------------- bootstrap

@dataclass(frozen=True)
class Bootstrap:
    seed: int = BOOTSTRAP_SEED
    repetitions: int = BOOTSTRAP_REPETITIONS
    level: Fraction = INTERVAL_LEVEL


def _flat(files, names):
    out = []
    for name in names:
        out.extend(files[name])
    return out


def sample_bootstrap(rows, condition, axis, statistic, excluded, seed, repetitions):
    """The statistic over `repetitions` seeded draws of the files, with replacement."""
    files = _select(points_by_run(rows)[_ident_of(rows, condition)], excluded)
    return _sample(files, axis, statistic, seed, repetitions)


def _sample(files, axis, statistic, seed, repetitions):
    return _sample_seeds({"": files}, sorted(files), axis, statistic, seed, repetitions)


def _sample_seeds(seed_files, names, axis, statistic, seed, repetitions):
    """Draw the files once per repetition, then average the statistic over the
    condition's seeds on that same draw: the file stays the cluster."""
    if not names:
        return []
    rng = random.Random(seed)
    out = []
    for _ in range(repetitions):
        drawn = [names[rng.randrange(len(names))] for _ in names]
        value, _n, _k = _seed_mean(seed_files, drawn, axis, statistic)
        if value is not None:
            out.append(value)
    return out


def enumerate_bootstrap(rows, condition, axis, statistic, excluded):
    """Every equally likely draw of the files, exhaustively — k**k of them."""
    files = _select(points_by_run(rows)[_ident_of(rows, condition)], excluded)
    names = sorted(files)
    out = []
    for drawn in itertools.product(names, repeat=len(names)):
        value, _n = _statistic(statistic, _flat(files, list(drawn)), axis)
        if value is not None:
            out.append(value)
    return out


def _ident_of(rows, condition):
    """The one identity a condition names. These two samplers are inspection
    helpers over a single run group, so a condition run under several seeds is
    an error here rather than an arbitrary pick; `compute_grades` handles seeds."""
    found = sorted({(condition, str(r.get("table", "")), str(r.get("seed", "")))
                    for r in rows if r.get("condition") == condition})
    if not found:
        raise GradeError(f"no rows for condition {condition!r}")
    if len(found) > 1:
        raise GradeError(f"condition {condition!r} has {len(found)} identities "
                         f"{[i[2] for i in found]}; name the seed instead")
    return found[0]


def _interval(seed_files, names, axis, statistic, boot):
    values = sorted(_sample_seeds(seed_files, names, axis, statistic,
                                  boot.seed, boot.repetitions))
    return _bounds(values, boot)


def _bounds(values, boot):
    if not values:
        return "", ""
    tail = (1 - boot.level) / 2
    return fmt(quantile(values, tail)), fmt(quantile(values, 1 - tail))


# ----------------------------------------------------------- the grades file

STATS = {"mode": ("raw_accuracy", "majority_baseline"),
         "attribute": ("raw_accuracy", "majority_baseline", "balanced_accuracy", "matthews"),
         "algo_choice": ("raw_accuracy", "majority_baseline"),
         "configuration": ("correct_rate", "errors_changing_config"),
         "latency": ("p50", "p99")}


def compute_grades(rows, bootstrap: Optional[Bootstrap] = None):
    """The `grades` file's rows: statistics, per-class recall, confusion cells,
    and paired condition differences, each per seed and again averaged over the
    condition's seeds, with its sample, file and seed counts."""
    by_condition = _by_condition(points_by_run(rows))
    out = []

    def row(condition, table, seed, excluded, over_seeds, level, axis, **kw):
        base = {"condition": condition, "table": table, "seed": seed,
                "pre_committed_miss_excluded": 1 if excluded else 0,
                "over_seeds": 1 if over_seeds else 0, "level": level, "axis": axis,
                "statistic": "", "class": "", "truth": "", "predicted": "",
                "partner_condition": "", "value": "", "ci_low": "", "ci_high": "",
                "n": "", "n_files": "", "n_seeds": ""}
        base.update(kw)
        out.append(base)

    def shapes(condition, table, seed, excluded, over_seeds, axis, seed_files, names):
        """Per-class recall and confusion cells. Recall is a rate and averages over
        seeds; raw cell counts do not, so they are emitted per seed only."""
        per_seed = {sd: _pairs(_flat(f, names), axis) for sd, f in seed_files.items()}
        classes = sorted({t for pairs in per_seed.values() for t, _, _ in pairs})
        for klass in classes:
            values, n = [], 0
            for pairs in per_seed.values():
                recall = per_class_recall(pairs).get(klass)
                if recall is None:
                    values = []
                    break
                values.append(recall)
                n = max(n, sum(1 for t, _, _ in pairs if t == klass))
            if not values:
                continue
            row(condition, table, seed, excluded, over_seeds, "class_recall", axis,
                **{"class": klass}, value=fmt(Fraction(sum(values), len(values))),
                n=n, n_files=len(names), n_seeds=len(values))
        if over_seeds:
            return
        for (truth, predicted), n in sorted(Counter(
                (t, p) for pairs in per_seed.values() for t, p, _ in pairs).items()):
            row(condition, table, seed, excluded, over_seeds, "confusion", axis,
                truth=truth, predicted=predicted, n=n, n_files=len(names), n_seeds=1)

    for (condition, table), seeds in by_condition.items():
        # ---- one row set per seed, and one for the mean over them
        variants = [(sd, {sd: files}, False) for sd, files in seeds.items()]
        variants.append(("", seeds, True))
        for seed, group, over_seeds in variants:
            for excluded in (False, True):
                selected = {sd: _select(f, excluded) for sd, f in group.items()}
                selected = {sd: f for sd, f in selected.items() if f}
                if not selected:
                    continue
                names = _shared_files(selected)
                if not names:
                    continue
                for axis in AXES:
                    for name in STATS[axis]:
                        value, n, k = _seed_mean(selected, names, axis, name)
                        if value is None:
                            continue
                        lo = hi = ""
                        if bootstrap is not None and name != "majority_baseline":
                            lo, hi = _interval(selected, names, axis, name, bootstrap)
                        row(condition, table, seed, excluded, over_seeds, "statistic", axis,
                            statistic=name, value=fmt(value), ci_low=lo, ci_high=hi,
                            n=n, n_files=len(names), n_seeds=k)
                    if axis in ("mode", "attribute", "algo_choice"):
                        shapes(condition, table, seed, excluded, over_seeds, axis,
                               selected, names)

    # ---- paired differences: between distinct conditions only, seed-averaged,
    # both sides rescored on identical draws of identical files
    groups = sorted(by_condition)
    for i, a in enumerate(groups):
        for b in groups[i + 1:]:
            for excluded in (False, True):
                sa = {sd: f for sd, f in ((sd, _select(f, excluded))
                                          for sd, f in by_condition[a].items()) if f}
                sb = {sd: f for sd, f in ((sd, _select(f, excluded))
                                          for sd, f in by_condition[b].items()) if f}
                if not sa or not sb:
                    continue
                names = sorted(set(_shared_files(sa)) & set(_shared_files(sb)))
                if not names:
                    continue
                for axis, name in sorted(HEADLINE.items()):
                    va, na, ka = _seed_mean(sa, names, axis, name)
                    vb, _nb, _kb = _seed_mean(sb, names, axis, name)
                    if va is None or vb is None:
                        continue
                    lo = hi = ""
                    if bootstrap is not None:
                        lo, hi = _bounds(sorted(_paired_sample(sa, sb, names, axis, name,
                                                               bootstrap)), bootstrap)
                    row(a[0], a[1], "", excluded, True, "paired", axis, statistic=name,
                        partner_condition=b[0], value=fmt(va - vb), ci_low=lo, ci_high=hi,
                        n=na, n_files=len(names), n_seeds=ka)

    out.sort(key=sort_key)
    return out


def _paired_sample(sa, sb, names, axis, name, boot):
    """Both conditions rescored on identical draws, each seed-averaged first."""
    rng = random.Random(boot.seed)
    out = []
    for _ in range(boot.repetitions):
        drawn = [names[rng.randrange(len(names))] for _ in names]
        va, _n, _k = _seed_mean(sa, drawn, axis, name)
        vb, _n, _k = _seed_mean(sb, drawn, axis, name)
        if va is not None and vb is not None:
            out.append(va - vb)
    return out


def sort_key(row):
    return (_LEVEL_ORDER[row["level"]], row["condition"], row["partner_condition"],
            row["axis"], row["statistic"], row["class"], row["truth"], row["predicted"],
            int(row["pre_committed_miss_excluded"]), int(row["over_seeds"]), str(row["seed"]))


__all__ = ["ALGORITHMS", "AXES", "BOOTSTRAP_REPETITIONS", "BOOTSTRAP_SEED", "Bootstrap",
           "COLUMNS", "GRADES_SCHEMA", "GradeError", "IDENTITY", "INTERVAL_LEVEL", "MODES",
           "Point", "Run", "Segment", "balanced_accuracy", "compose_row", "compute_grades",
           "covering", "enumerate_bootstrap", "fmt", "grade_log", "majority_baseline",
           "matthews", "per_class_recall", "points_by_run", "quantile", "raw_accuracy",
           "read_driver_table", "read_ground_truth", "sample_bootstrap", "sort_key"]
