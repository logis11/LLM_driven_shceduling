"""Sub-task 8.4: the Layer-1 grader — a recognition log graded against ground
truth into recognition records rows (metrics doc §7), and the `grades` file
computed over them (§8). Hand-worked against the `mock-grades` fixture; the
derivation of every value is in that fixture's `worked.md`."""

import json
import subprocess
import sys
from fractions import Fraction

import pytest

from conftest import REPO, TOOLS
from harness import grader, records
from harness.grader import (COLUMNS, GRADES_SCHEMA, GradeError, Run, compose_row,
                            compute_grades, grade_log, read_driver_table, read_ground_truth)
from harness.outputs import read_csv, validate_rows, write_csv

MG = TOOLS / "tests" / "fixtures" / "mock-grades"
TABLE = MG / "driver-table.yaml"
GRADED = ("g-alpha", "g-beta", "g-gamma", "g-epsilon")      # g-delta is `ambiguous` throughout
CONDITIONS = ("llm_algo", "llm_vocab", "oracle", "random")


def _identity(condition, workload):
    return {"workload_id": workload, "condition": condition, "table": "calibrated",
            "seed": "s1" if condition == "random" else "", "boot_default": ""}


def _runs(conditions=CONDITIONS, workloads=None):
    out = []
    for c in conditions:
        for w in (workloads if workloads is not None else GRADED):
            out.append(Run(**_identity(c, w), log=MG / "logs" / f"{c}--{w}.json",
                           workload=MG / "workloads" / f"{w}.workload.json", table_path=TABLE))
    return out


def _rows(runs=None):
    rows = []
    for run in (runs or _runs()):
        r, _ = grade_log(run)
        rows.extend(r)
    return rows


def _stat(grades, condition, axis, statistic, excluded=1):
    found = [g for g in grades if g["level"] == "statistic" and g["condition"] == condition
             and g["axis"] == axis and g["statistic"] == statistic
             and int(g["pre_committed_miss_excluded"]) == excluded]
    assert len(found) == 1, (condition, axis, statistic, excluded, found)
    return found[0]


# ------------------------------------------------------------------ readers

def test_ground_truth_segments_carry_their_annotations():
    segs = read_ground_truth(MG / "workloads" / "g-gamma.workload.json")
    assert len(segs) == 1
    s = segs[0]
    assert s.mode == "ml-train" and s.background_wanted is False
    assert s.pre_committed_miss is True and s.familiarity is None
    beta = read_ground_truth(MG / "workloads" / "g-beta.workload.json")[0]
    assert beta.familiarity == 5 and beta.pre_committed_miss is False


def test_driver_table_composes_the_row_the_daemon_would():
    table = read_driver_table(TABLE)
    assert table.role == "calibrated"
    assert table.default_algorithm("ml-train", True) == "LOTTERY"
    # the three `false` rows compose to identical configurations by construction
    assert compose_row(table.row("ml-train", False)) == compose_row(table.row("office", False))
    assert compose_row(table.row("ml-train", False)) != compose_row(table.row("ml-train", True))


def test_harness_composition_agrees_with_the_daemon_on_the_prior_table():
    """The harness re-reads the driver table rather than importing the daemon's
    module, so a test pins the two compositions together (8.4 spec, decision 7)."""
    sys.path.insert(0, str(REPO / "daemon" / "tools"))
    from drivertable.lint import compose as daemon_compose
    table = read_driver_table(REPO / "daemon" / "driver-table" / "prior.yaml")
    assert len(table.rows) == 32
    for (mode, wanted), row in table.rows.items():
        assert compose_row(row) == daemon_compose(row, row["default"]), (mode, wanted)


# ------------------------------------------------------------- grading scope

def test_ambiguous_and_terminal_query_points_are_skipped():
    run = Run(**_identity("llm_vocab", "g-delta"), log=MG / "logs" / "llm_vocab--g-delta.json",
              workload=MG / "workloads" / "g-delta.workload.json", table_path=TABLE)
    rows, messages = grade_log(run)
    assert rows == [] and messages == []


def test_the_graded_set_is_five_points_over_four_files():
    rows = _rows(_runs(conditions=("oracle",)))
    points = sorted({(r["workload_id"], r["t"]) for r in rows})
    assert points == [("g-alpha", 0), ("g-alpha", 60000000), ("g-beta", 0),
                      ("g-epsilon", 0), ("g-gamma", 0)]


def test_every_graded_point_emits_its_metrics():
    rows, _ = grade_log(_runs(conditions=("llm_vocab",), workloads=("g-alpha",))[0])
    got = sorted({(r["t"], r["metric"]) for r in rows})
    assert got == [(0, "attr_correct"), (0, "config_correct"), (0, "latency_us"),
                   (0, "mode_correct"),
                   (60000000, "attr_correct"), (60000000, "config_correct"),
                   (60000000, "latency_us"), (60000000, "mode_correct")]
    assert all(r["entity"] == "recognizer" for r in rows)
    assert all(r["validation"] == "unmodified" for r in rows)
    assert all("sim" not in r or r["sim"] == "" for r in rows)


def test_algo_choice_rows_are_llm_algo_only():
    assert not [r for r in _rows(_runs(conditions=("llm_vocab",)))
                if r["metric"] == "algo_choice_correct"]
    algo = [r for r in _rows(_runs(conditions=("llm_algo",)))
            if r["metric"] == "algo_choice_correct"]
    assert len(algo) == 5
    beta = next(r for r in algo if r["workload_id"] == "g-beta")
    assert beta["value"] == 0 and beta["predicted"] == "MLFQ" and beta["truth"] == "EDF"


def test_a_null_proposal_scores_zero_with_an_empty_prediction():
    rows, _ = grade_log(_runs(conditions=("llm_vocab",), workloads=("g-beta",))[0])
    by = {r["metric"]: r for r in rows}
    assert by["mode_correct"]["value"] == 0 and by["attr_correct"]["value"] == 0
    assert by["mode_correct"]["predicted"] == "" and by["mode_correct"]["truth"] == "media"
    assert by["mode_correct"]["validation"] == "held"
    assert by["config_correct"]["value"] == 0


def test_annotations_ride_on_every_recognition_row():
    beta = _rows(_runs(conditions=("oracle",), workloads=("g-beta",)))
    assert all(r["familiarity"] == 5 for r in beta)
    assert all(r["pre_committed_miss"] == 0 for r in beta)
    gamma = _rows(_runs(conditions=("oracle",), workloads=("g-gamma",)))
    assert all(r["pre_committed_miss"] == 1 for r in gamma)
    assert all("familiarity" not in r for r in gamma)


def test_rows_validate_against_the_records_schema():
    records.validate_rows(_rows())


def test_an_off_menu_truth_is_refused(tmp_path):
    doc = json.loads((MG / "workloads" / "g-beta.workload.json").read_text())
    doc["ground_truth"][0]["mode"] = "build"
    p = tmp_path / "bad.workload.json"
    p.write_text(json.dumps(doc))
    run = Run(**_identity("oracle", "g-beta"), log=MG / "logs" / "oracle--g-beta.json",
              workload=p, table_path=TABLE)
    with pytest.raises(GradeError, match="build"):
        grade_log(run)


def test_an_off_menu_prediction_scores_wrong_and_is_recorded(tmp_path):
    doc = json.loads((MG / "logs" / "oracle--g-beta.json").read_text())
    doc["queries"][0]["proposal"]["system"]["mode"] = "build"
    p = tmp_path / "log.json"
    p.write_text(json.dumps(doc))
    run = Run(**_identity("oracle", "g-beta"), log=p,
              workload=MG / "workloads" / "g-beta.workload.json", table_path=TABLE)
    rows, messages = grade_log(run)
    mode = next(r for r in rows if r["metric"] == "mode_correct")
    assert mode["value"] == 0 and mode["predicted"] == "build"
    assert any("g-beta" in m for m in messages)          # the oracle was not perfect


def test_the_oracle_is_checked_for_perfection():
    for run in _runs(conditions=("oracle",)):
        assert grade_log(run)[1] == []
    for run in _runs(conditions=("random",)):
        pass                                              # random is never checked
    assert all(grade_log(r)[1] == [] for r in _runs(conditions=("random", "llm_vocab")))


def test_a_prior_table_is_refused_for_algorithm_choice():
    run = Run(**_identity("llm_algo", "g-alpha"), log=MG / "logs" / "llm_algo--g-alpha.json",
              workload=MG / "workloads" / "g-alpha.workload.json",
              table_path=REPO / "daemon" / "driver-table" / "prior.yaml")
    with pytest.raises(GradeError, match="prior"):
        grade_log(run)


# -------------------------------------------------------------- the statistics

@pytest.fixture(scope="module")
def grades():
    return compute_grades(_rows(), bootstrap=None)


def test_counts_match_the_hand_worked_table(grades):
    """Five graded points over four files; four over three once the
    pre-committed-miss file drops out."""
    unexcluded = _stat(grades, "oracle", "mode", "raw_accuracy", excluded=0)
    assert int(unexcluded["n"]) == 5 and int(unexcluded["n_files"]) == 4
    excluded = _stat(grades, "oracle", "mode", "raw_accuracy", excluded=1)
    assert int(excluded["n"]) == 4 and int(excluded["n_files"]) == 3


@pytest.mark.parametrize("condition,axis,expected", [
    ("oracle", "mode", Fraction(4, 4)), ("oracle", "attribute", Fraction(4, 4)),
    ("random", "mode", Fraction(1, 4)), ("random", "attribute", Fraction(2, 4)),
    ("llm_vocab", "mode", Fraction(3, 4)), ("llm_vocab", "attribute", Fraction(3, 4)),
    ("llm_algo", "mode", Fraction(4, 4)), ("llm_algo", "attribute", Fraction(4, 4)),
])
def test_raw_accuracy_excluded(grades, condition, axis, expected):
    assert _stat(grades, condition, axis, "raw_accuracy")["value"] == grader.fmt(expected)


@pytest.mark.parametrize("condition,axis,expected", [
    ("random", "mode", Fraction(1, 5)), ("random", "attribute", Fraction(3, 5)),
    ("llm_vocab", "mode", Fraction(4, 5)), ("llm_vocab", "attribute", Fraction(3, 5)),
    ("llm_algo", "attribute", Fraction(4, 5)),
])
def test_raw_accuracy_unexcluded(grades, condition, axis, expected):
    assert _stat(grades, condition, axis, "raw_accuracy", excluded=0)["value"] == grader.fmt(expected)


def test_majority_baselines(grades):
    # excluded truths: attribute 3 true / 1 false; mode dev, ml-train, media, indexing
    assert _stat(grades, "oracle", "attribute", "majority_baseline")["value"] == grader.fmt(Fraction(3, 4))
    assert _stat(grades, "oracle", "mode", "majority_baseline")["value"] == grader.fmt(Fraction(1, 4))


def test_balanced_accuracy_is_the_attribute_only(grades):
    assert [g for g in grades if g["statistic"] == "balanced_accuracy" and g["axis"] != "attribute"] == []
    # true recall 2/3 and false recall 0/1 for random; 2/3 and 1/1 for llm_vocab
    assert _stat(grades, "random", "attribute", "balanced_accuracy")["value"] == grader.fmt(Fraction(1, 3))
    assert _stat(grades, "llm_vocab", "attribute", "balanced_accuracy")["value"] == grader.fmt(Fraction(5, 6))
    assert _stat(grades, "oracle", "attribute", "balanced_accuracy")["value"] == grader.fmt(Fraction(1))


def test_matthews_is_computed_over_answered_points_only(grades):
    # llm_vocab's g-beta proposal is null, so it has no cell in the 2x2: n is 3, not 4
    mcc = _stat(grades, "llm_vocab", "attribute", "matthews")
    assert mcc["value"] == grader.fmt(Fraction(1)) and int(mcc["n"]) == 3
    # random: TP 2, FN 1, TN 0, FP 1
    assert _stat(grades, "random", "attribute", "matthews")["value"] == grader.fmt(Fraction(-1, 3))
    assert [g for g in grades if g["statistic"] == "matthews" and g["axis"] != "attribute"] == []


def test_no_macro_average_is_computed(grades):
    assert [g for g in grades if "macro" in g["statistic"]] == []


def test_per_class_recall(grades):
    rec = {g["class"]: g["value"] for g in grades
           if g["level"] == "class_recall" and g["condition"] == "llm_vocab"
           and g["axis"] == "mode" and int(g["pre_committed_miss_excluded"]) == 1}
    assert rec == {"dev": grader.fmt(Fraction(1)), "ml-train": grader.fmt(Fraction(1)),
                   "media": grader.fmt(Fraction(0)), "indexing": grader.fmt(Fraction(1))}


def test_confusion_cells(grades):
    cells = {(g["truth"], g["predicted"]): int(g["n"]) for g in grades
             if g["level"] == "confusion" and g["condition"] == "random"
             and g["axis"] == "mode" and int(g["pre_committed_miss_excluded"]) == 1}
    assert cells == {("dev", "backup"): 1, ("ml-train", "media"): 1,
                     ("media", "media"): 1, ("indexing", "gaming"): 1}
    # a null prediction gets its own column rather than being folded into a class
    nulls = [g for g in grades if g["level"] == "confusion" and g["condition"] == "llm_vocab"
             and g["axis"] == "mode" and g["predicted"] == ""
             and int(g["pre_committed_miss_excluded"]) == 1]
    assert len(nulls) == 1 and nulls[0]["truth"] == "media"


def test_configuration_distance(grades):
    # excluded: oracle 4/4, random 1/4, llm_vocab 3/4, llm_algo 4/4
    assert _stat(grades, "random", "configuration", "correct_rate")["value"] == grader.fmt(Fraction(1, 4))
    assert _stat(grades, "llm_vocab", "configuration", "correct_rate")["value"] == grader.fmt(Fraction(3, 4))
    # unexcluded, random makes 4 errors and only 3 of them changed the configuration:
    # g-gamma names office/false where the truth is ml-train/false, and those two rows
    # compose to identical configurations
    errors = _stat(grades, "random", "configuration", "errors_changing_config", excluded=0)
    assert errors["value"] == grader.fmt(Fraction(3, 4)) and int(errors["n"]) == 4


def test_latency_percentiles(grades):
    p50 = _stat(grades, "llm_vocab", "latency", "p50")
    assert p50["value"] == grader.fmt(Fraction(450000))
    assert _stat(grades, "oracle", "latency", "p50")["value"] == grader.fmt(Fraction(0))


# ---------------------------------------------------------------- bootstrap

def test_the_bootstrap_is_reproducible():
    rows = _rows()
    a = compute_grades(rows, bootstrap=grader.Bootstrap(seed=7, repetitions=200))
    b = compute_grades(rows, bootstrap=grader.Bootstrap(seed=7, repetitions=200))
    assert a == b
    c = compute_grades(rows, bootstrap=grader.Bootstrap(seed=8, repetitions=200))
    assert c != a


def test_the_bootstrap_resamples_files_not_query_points():
    """Exhaustive check: with 3 contributing files in the excluded set there are
    3**3 = 27 equally likely draws, so the exact distribution of any statistic is
    enumerable. The seeded sampler must converge to it (8.4 spec, decision 16)."""
    rows = _rows()
    exact = grader.enumerate_bootstrap(rows, "llm_vocab", "mode", "raw_accuracy", excluded=True)
    assert len(exact) == 27
    assert min(exact) == Fraction(0) and max(exact) == Fraction(1)
    sampled = grader.sample_bootstrap(rows, "llm_vocab", "mode", "raw_accuracy",
                                      excluded=True, seed=1, repetitions=20000)
    for q in (Fraction(1, 20), Fraction(1, 2), Fraction(19, 20)):
        e = grader.quantile(sorted(exact), q)
        s = grader.quantile(sorted(sampled), q)
        assert abs(float(e) - float(s)) < 0.05, (q, float(e), float(s))


def test_intervals_appear_only_where_computed():
    g = compute_grades(_rows(), bootstrap=grader.Bootstrap(seed=7, repetitions=200))
    stat = _stat(g, "llm_vocab", "attribute", "balanced_accuracy")
    lo, hi = Fraction(stat["ci_low"]), Fraction(stat["ci_high"])
    assert lo <= Fraction(stat["value"]) <= hi
    assert all(c["ci_low"] == "" for c in g if c["level"] == "confusion")


def test_paired_rows_compare_on_the_same_draws():
    g = compute_grades(_rows(), bootstrap=grader.Bootstrap(seed=7, repetitions=200))
    paired = [r for r in g if r["level"] == "paired" and r["condition"] == "llm_vocab"
              and r["partner_condition"] == "random" and r["axis"] == "mode"
              and int(r["pre_committed_miss_excluded"]) == 1]
    assert len(paired) == 1
    row = paired[0]
    assert row["value"] == grader.fmt(Fraction(3, 4) - Fraction(1, 4))
    assert Fraction(row["ci_low"]) <= Fraction(row["value"]) <= Fraction(row["ci_high"])


# --------------------------------------------------------- file, schema, CLI

def test_expected_grades_file_byte_for_byte(tmp_path):
    g = compute_grades(_rows(), bootstrap=grader.Bootstrap(seed=20260911, repetitions=500))
    out = tmp_path / "grades.csv"
    write_csv(g, COLUMNS, out)
    assert out.read_bytes() == (MG / "expected-grades.csv").read_bytes()


def test_expected_files_validate_against_their_schemas():
    validate_rows(read_csv(MG / "expected-grades.csv", COLUMNS), GRADES_SCHEMA)
    for f in sorted((MG / "expected-records").glob("*.csv")):
        records.validate_rows(records.read_csv(f))


def test_expected_records_byte_for_byte(tmp_path):
    for run in _runs():
        rows, _ = grade_log(run)
        out = tmp_path / "r.csv"
        records.write_csv(rows, out)
        name = f"{run.condition}--{run.workload_id}.csv"
        assert out.read_bytes() == (MG / "expected-records" / name).read_bytes(), name


def test_cli_writes_records_and_grades(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "driver_table": str(TABLE),
        "bootstrap": {"seed": 20260911, "repetitions": 500},
        "runs": [{**_identity(c, w), "log": str(MG / "logs" / f"{c}--{w}.json"),
                  "workload": str(MG / "workloads" / f"{w}.workload.json")}
                 for c in CONDITIONS for w in GRADED]}))
    out = tmp_path / "grades.csv"
    r = subprocess.run([sys.executable, str(TOOLS / "grade.py"), "--manifest", str(manifest),
                        "--out-grades", str(out), "--out-records", str(tmp_path / "records")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert out.read_bytes() == (MG / "expected-grades.csv").read_bytes()
    assert len(list((tmp_path / "records").glob("*.csv"))) == 16


def test_cli_exits_non_zero_when_the_oracle_is_not_perfect(tmp_path):
    doc = json.loads((MG / "logs" / "oracle--g-beta.json").read_text())
    doc["queries"][0]["proposal"]["system"]["mode"] = "dev"
    log = tmp_path / "oracle--g-beta.json"
    log.write_text(json.dumps(doc))
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "driver_table": str(TABLE),
        "runs": [{**_identity("oracle", "g-beta"), "log": str(log),
                  "workload": str(MG / "workloads" / "g-beta.workload.json")}]}))
    r = subprocess.run([sys.executable, str(TOOLS / "grade.py"), "--manifest", str(manifest),
                        "--out-grades", str(tmp_path / "g.csv")], capture_output=True, text=True)
    assert r.returncode == 2
    assert "oracle" in r.stderr and "g-beta" in r.stderr
