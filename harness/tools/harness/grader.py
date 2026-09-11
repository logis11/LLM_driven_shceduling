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
COLUMNS = IDENTITY + ("pre_committed_miss_excluded", "level", "axis", "statistic",
                      "class", "truth", "predicted", "partner_condition",
                      "value", "ci_low", "ci_high", "n", "n_files")

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
    names = sorted(files)
    if not names:
        return []
    rng = random.Random(seed)
    out = []
    for _ in range(repetitions):
        drawn = [names[rng.randrange(len(names))] for _ in names]
        value, _n = _statistic(statistic, _flat(files, drawn), axis)
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
    for r in rows:
        if r.get("condition") == condition:
            return (condition, str(r.get("table", "")), str(r.get("seed", "")))
    raise GradeError(f"no rows for condition {condition!r}")


def _interval(files, axis, statistic, boot):
    values = sorted(_sample(files, axis, statistic, boot.seed, boot.repetitions))
    if not values:
        return "", ""
    tail = (1 - boot.level) / 2
    return fmt(quantile(values, tail)), fmt(quantile(values, 1 - tail))


# ----------------------------------------------------------- the grades file

def compute_grades(rows, bootstrap: Optional[Bootstrap] = None):
    """The `grades` file's rows: statistics, per-class recall, confusion cells,
    and paired condition differences, each with its sample and file counts."""
    by_run = points_by_run(rows)
    out = []

    def row(ident, excluded, level, axis, **kw):
        base = dict(zip(IDENTITY, ident))
        base.update({"pre_committed_miss_excluded": 1 if excluded else 0,
                     "level": level, "axis": axis, "statistic": "", "class": "",
                     "truth": "", "predicted": "", "partner_condition": "",
                     "value": "", "ci_low": "", "ci_high": "", "n": "", "n_files": ""})
        base.update(kw)
        out.append(base)

    for ident, all_files in sorted(by_run.items()):
        for excluded in (False, True):
            files = _select(all_files, excluded)
            if not files:
                continue
            flat = _flat(files, sorted(files))
            n_files = len(files)
            for axis in AXES:
                names = {"mode": ("raw_accuracy", "majority_baseline"),
                         "attribute": ("raw_accuracy", "majority_baseline",
                                       "balanced_accuracy", "matthews"),
                         "algo_choice": ("raw_accuracy", "majority_baseline"),
                         "configuration": ("correct_rate", "errors_changing_config"),
                         "latency": ("p50", "p99")}[axis]
                for name in names:
                    value, n = _statistic(name, flat, axis)
                    if value is None:
                        continue
                    lo = hi = ""
                    if bootstrap is not None and name != "majority_baseline":
                        lo, hi = _interval(files, axis, name, bootstrap)
                    row(ident, excluded, "statistic", axis, statistic=name,
                        value=fmt(value), ci_low=lo, ci_high=hi, n=n, n_files=n_files)
                if axis in ("mode", "algo_choice", "attribute"):
                    pairs = _pairs(flat, axis)
                    for klass, recall in sorted(per_class_recall(pairs).items()):
                        n = sum(1 for t, _, _ in pairs if t == klass)
                        row(ident, excluded, "class_recall", axis, **{"class": klass},
                            value=fmt(recall), n=n, n_files=n_files)
                    cells = Counter((t, p) for t, p, _ in pairs)
                    for (truth, predicted), n in sorted(cells.items()):
                        row(ident, excluded, "confusion", axis, truth=truth,
                            predicted=predicted, n=n, n_files=n_files)

    # paired differences, on the same files and the same draws
    idents = sorted(by_run)
    for i, a in enumerate(idents):
        for b in idents[i + 1:]:
            for excluded in (False, True):
                fa = _select(by_run[a], excluded)
                fb = _select(by_run[b], excluded)
                shared = sorted(set(fa) & set(fb))
                if not shared:
                    continue
                fa = {k: fa[k] for k in shared}
                fb = {k: fb[k] for k in shared}
                for axis, name in sorted(HEADLINE.items()):
                    va, na = _statistic(name, _flat(fa, shared), axis)
                    vb, _nb = _statistic(name, _flat(fb, shared), axis)
                    if va is None or vb is None:
                        continue
                    lo = hi = ""
                    if bootstrap is not None:
                        diffs = sorted(_paired_sample(fa, fb, axis, name, bootstrap))
                        if diffs:
                            tail = (1 - bootstrap.level) / 2
                            lo, hi = fmt(quantile(diffs, tail)), fmt(quantile(diffs, 1 - tail))
                    row(a, excluded, "paired", axis, statistic=name,
                        partner_condition=b[0], value=fmt(va - vb), ci_low=lo, ci_high=hi,
                        n=na, n_files=len(shared))

    out.sort(key=sort_key)
    return out


def _paired_sample(fa, fb, axis, name, boot):
    """Both conditions rescored on identical draws, difference by difference."""
    names = sorted(fa)
    rng = random.Random(boot.seed)
    out = []
    for _ in range(boot.repetitions):
        drawn = [names[rng.randrange(len(names))] for _ in names]
        va, _ = _statistic(name, _flat(fa, drawn), axis)
        vb, _ = _statistic(name, _flat(fb, drawn), axis)
        if va is not None and vb is not None:
            out.append(va - vb)
    return out


def sort_key(row):
    return (_LEVEL_ORDER[row["level"]], row["condition"], row["partner_condition"],
            row["axis"], row["statistic"], row["class"], row["truth"], row["predicted"],
            int(row["pre_committed_miss_excluded"]))


__all__ = ["ALGORITHMS", "AXES", "BOOTSTRAP_REPETITIONS", "BOOTSTRAP_SEED", "Bootstrap",
           "COLUMNS", "GRADES_SCHEMA", "GradeError", "IDENTITY", "INTERVAL_LEVEL", "MODES",
           "Point", "Run", "Segment", "balanced_accuracy", "compose_row", "compute_grades",
           "covering", "enumerate_bootstrap", "fmt", "grade_log", "majority_baseline",
           "matthews", "per_class_recall", "points_by_run", "quantile", "raw_accuracy",
           "read_driver_table", "read_ground_truth", "sample_bootstrap", "sort_key"]
