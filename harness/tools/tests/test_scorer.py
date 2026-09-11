"""Sub-task 8.2: the aggregates module and the scorer against the hand-written
`mock-scores` fixture (records in, aggregates and scores out, byte for byte),
and one end-to-end seam case (mock-p1a's records from the records writer
scored against hand-written fixed and oracle records)."""

import pathlib
import subprocess
import sys

import pytest

from harness import aggregates as agg
from harness import records, scorer, scoring
from harness.outputs import AGGREGATES_SCHEMA, SCORES_SCHEMA, read_csv, validate_rows, write_csv

TOOLS = pathlib.Path(__file__).resolve().parents[1]
MS = TOOLS / "tests" / "fixtures" / "mock-scores"
SEAM = MS / "seam"


def _spec():
    return scoring.load_spec(MS / "scoring-spec.yaml")


def _windows(spec, workload):
    sys.path.insert(0, str(TOOLS))
    from score import windows_from_spec
    return windows_from_spec(spec, workload)


def _aggregate_all(files, spec):
    rows = []
    for f in files:
        run = records.read_csv(f)
        rows.extend(agg.compute_aggregates(run, _windows(spec, run[0]["workload_id"])))
    return rows


def test_fixture_aggregates_byte_for_byte(tmp_path):
    spec = _spec()
    rows = _aggregate_all(sorted((MS / "records").glob("*.csv")), spec)
    out = tmp_path / "aggregates.csv"
    write_csv(rows, agg.COLUMNS, out)
    assert out.read_bytes() == (MS / "expected-aggregates.csv").read_bytes()


def test_fixture_scores_byte_for_byte(tmp_path):
    spec = _spec()
    rows = _aggregate_all(sorted((MS / "records").glob("*.csv")), spec)
    term_rows, file_rows = scorer.score(rows, spec)
    out = tmp_path / "scores.csv"
    write_csv(term_rows + file_rows, scorer.COLUMNS, out)
    assert out.read_bytes() == (MS / "expected-scores.csv").read_bytes()


def test_expected_files_validate_against_their_schemas():
    validate_rows(read_csv(MS / "expected-aggregates.csv", agg.COLUMNS), AGGREGATES_SCHEMA)
    validate_rows(read_csv(MS / "expected-scores.csv", scorer.COLUMNS), SCORES_SCHEMA)


def _file_row(rows, condition, seed, boot):
    return next(r for r in rows if r["level"] == "file" and r["condition"] == condition
                and r["seed"] == seed and r["boot_default"] == boot)


def test_rules_show_in_the_scores():
    spec = _spec()
    term_rows, file_rows = scorer.score(_aggregate_all(sorted((MS / "records").glob("*.csv")), spec), spec)
    # the no-headroom term keeps its weight and contributes share 1: fixed's score is exactly its weight
    assert _file_row(file_rows, "fixed", "", "")["score"] == "0.500000"
    assert _file_row(file_rows, "oracle", "", "")["score"] == "2.500000"
    # random s2: censored turnaround (did not finish), negative share, mark carried
    s2 = [r for r in term_rows if r["condition"] == "random" and r["seed"] == "s2" and r["boot_default"] == ""]
    build = next(r for r in s2 if r["entity"] == "build")
    assert build["censored"] == 1 and build["value_condition"] == "90000.000000" and build["share"] == "-0.333333"
    assert _file_row(file_rows, "random", "s2", "")["n_censored"] == 1
    # the alternative-default fixed run re-scores the same oracle and random runs against itself
    assert _file_row(file_rows, "random", "s1", "alt")["score"] == "1.533876"
    assert _file_row(file_rows, "random", "s2", "alt")["score"] == "0.210172"
    # the video term is no headroom everywhere and its share is left empty
    assert all(r["share"] == "" and r["no_headroom"] == 1 for r in term_rows if r["entity"] == "video")


def test_empty_filter_stops_the_scorer():
    spec = _spec()
    spec["files"]["mock-score"]["terms"].append(
        {"entity": "ghost", "metric": "ready_wait", "cause": "wake", "aggregate": "p99",
         "direction": "lower", "weight": 1.0})
    rows = _aggregate_all(sorted((MS / "records").glob("*.csv")), spec)
    with pytest.raises(scorer.ScoringError, match="ghost"):
        scorer.score(rows, spec)


def test_seam_records_writer_to_scorer(fixture_dir):
    """mock-p1a's records as written by the records writer (llm_vocab) scored against
    hand-written fixed and oracle records for the same reduced workload."""
    d = fixture_dir("mock-p1a")
    llm_rows, _ = records.build(d / "run.json", d / "trace.jsonl", table="prior",
                                schedule_path=d / "config-schedule.json")
    spec = _spec()
    win = _windows(spec, "mock-p1a")
    rows = agg.compute_aggregates(llm_rows, win)
    for f in ("fixed", "oracle"):
        rows.extend(agg.compute_aggregates(records.read_csv(SEAM / f"{f}.csv"), win))
    term_rows, file_rows = scorer.score(rows, spec)
    llm = {r["entity"]: r for r in term_rows if r["condition"] == "llm_vocab"}
    # editor P99 over the window [50000, 120000]: llm_vocab [1500, 3000] → 2985; fixed 7960; oracle 995
    assert llm["editor"]["value_condition"] == "2985.000000"
    assert llm["editor"]["value_fixed"] == "7960.000000" and llm["editor"]["value_oracle"] == "995.000000"
    assert llm["editor"]["share"] == "0.714286"
    # hog progress: llm_vocab 65000/90000 against fixed 60000/90000 and oracle 50000/90000 → share −0.5
    assert llm["hog"]["value_condition"] == "0.722222" and llm["hog"]["share"] == "-0.500000"
    assert _file_row(file_rows, "llm_vocab", "", "")["score"] == "0.464286"


def test_cli_writes_both_files(tmp_path):
    out_a, out_s = tmp_path / "a.csv", tmp_path / "s.csv"
    p = subprocess.run([sys.executable, str(TOOLS / "score.py"), "--records", str(MS / "records"),
                        "--spec", str(MS / "scoring-spec.yaml"),
                        "--out-aggregates", str(out_a), "--out-scores", str(out_s)],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    assert out_a.read_bytes() == (MS / "expected-aggregates.csv").read_bytes()
    assert out_s.read_bytes() == (MS / "expected-scores.csv").read_bytes()


def test_percentile_is_numpy_linear_and_exact():
    import numpy as np
    from fractions import Fraction
    vals = [8000, 12000, 20000, 40000]
    assert agg.percentile(vals, 99) == Fraction(39400)
    assert abs(float(agg.percentile(vals, 99)) - float(np.percentile(vals, 99, method="linear"))) < 1e-6
    assert agg.percentile([7], 50) == Fraction(7)
    assert agg.fmt(agg.percentile([1000, 2000, 3000, 4000], 99), 6) == "3970.000000"


def test_excess_aggregates_on_mock_switch(fixture_dir):
    """Metrics doc §8 on mock-switch's worked values: the switch window [40600, 53100] holds the
    46000 wake (100), the boost windows [60600, 69600] and [80600, 86600] hold the 62000 wake (600),
    the rest of the MLFQ interval holds the 90000 wake (0): excess 100 (switch), 600 (boost)."""
    d = fixture_dir("mock-switch")
    rows, _ = records.build(d / "run.json", d / "trace.jsonl", table="calibrated",
                            schedule_path=d / "config-schedule.json")
    out = {(r["aggregate"], r["index"]): r["value"]
           for r in agg.compute_aggregates(rows, interactive=("editor",)) if r["metric"] == "switch_window"}
    assert out[("excess_switch", "3")] == "100.000000000000"
    assert out[("excess_boost", "3")] == "600.000000000000"
    assert out[("share_inside_switch_windows", "")] == "0.125000000000"


def test_scorer_floors_are_overridable_with_the_same_default():
    """8.7 spec, decision 11: an optional floors argument for the floor band."""
    from fractions import Fraction
    spec = _spec()
    rows = _aggregate_all(sorted((MS / "records").glob("*.csv")), spec)
    terms, files = scorer.score(rows, spec)
    terms_default, files_default = scorer.score(rows, spec, floors=scorer.FLOOR)
    assert (terms, files) == (terms_default, files_default)
    assert scorer.floors_for(latency_floor_us=1000) == scorer.FLOOR
    raised = scorer.floors_for(latency_floor_us=40000)
    assert raised["p99"] == Fraction(40000) and raised["miss_rate"] == scorer.FRACTION_FLOOR
    terms_r, files_r = scorer.score(rows, spec, floors=raised)
    editor = [t for t in terms_r if t["entity"] == "editor" and t["boot_default"] == ""]
    assert editor and all(t["no_headroom"] == 1 for t in editor)
    s1 = next(f for f in files_r if f["condition"] == "random" and f["seed"] == "s1" and f["boot_default"] == "")
    assert s1["score"] == "2.250000" and s1["n_no_headroom"] == 3
