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
                                schedule_path=d / "config-schedule.json", telemetry="names")
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
    50100 wake (0: keystroke 2 reached the editor at 46000 while it was ready in Q1 mid-burst,
    preempted behind the hog, so it was queued and its next WAIT completed at 50100 with zero wait),
    the boost windows [60600, 80600] and [80600, 86600] hold the 62000 wake (600), the rest of the
    MLFQ interval holds the 90000 wake (0): excess 0 (switch), 600 (boost)."""
    d = fixture_dir("mock-switch")
    rows, _ = records.build(d / "run.json", d / "trace.jsonl", table="calibrated",
                            schedule_path=d / "config-schedule.json")
    out = {(r["aggregate"], r["index"]): r["value"]
           for r in agg.compute_aggregates(rows, interactive=("editor",)) if r["metric"] == "switch_window"}
    assert out[("excess_switch", "3")] == "0.000000000000"
    assert out[("excess_boost", "3")] == "600.000000000000"
    assert out[("share_inside_switch_windows", "")] == "0.125000000000"


def _wake_records(condition, wakes, t_end=100000, extra=()):
    """Typed records rows of one run of workload `w`: the lane's busy row and one
    editor ready_wait wake row per (t, value, channel)."""
    ident = {"workload_id": "w", "condition": condition, "source_sha256": "0" * 64, "sim": "mock@0"}
    rows = [dict(ident, entity="lane", metric="busy", t=t_end, value=0)]
    rows += [dict(ident, entity="editor", metric="ready_wait", t=t, value=v, cause="wake", channel=ch)
             for (t, v, ch) in wakes]
    rows += [dict(ident, **r) for r in extra]
    return rows


def test_censored_turnaround_reads_the_arrival_row():
    """Metrics doc §9: an unfinished task's turnaround is scored on T_end − arrival, the
    arrival its task_arrive line's time, which its `arrival` row carries (§6.6). A task
    whose first instruction is a WAIT has no ready(cause = arrive) line (§11 item 5) and
    keeps its bound: `waiter` arrives at 300 blocked, first runs on a wake at 500, never
    ends — 1000 − 300 = 700. `runner`, ready at its arrival (200), gets 800 as before."""
    from harness.primitives import compute
    from harness.reader import RunFile, TaskInfo
    tasks = {tid: TaskInfo(id=tid, name=tid, arrive=t, depart=None, demand=None, period_us=None,
                           wake_targets=[], waits=w)
             for tid, t, w in (("runner", 200, ["timer"]), ("waiter", 300, ["timer"]))}
    run = RunFile(workload_id="w", t_end=1000, tasks=tasks, chains=[], input_wakes={})
    events = [{"event": "task_arrive", "t": 200, "task": "runner", "source": "file"},
              {"event": "ready", "t": 200, "task": "runner", "cause": "arrive"},
              {"event": "run_start", "t": 200, "task": "runner"},
              {"event": "run_end", "t": 300, "task": "runner", "reason": "block", "blocked_on": "wait"},
              {"event": "task_arrive", "t": 300, "task": "waiter", "source": "file"},
              {"event": "ready", "t": 500, "task": "waiter", "cause": "wake"},
              {"event": "run_start", "t": 500, "task": "waiter"},
              {"event": "run_end", "t": 600, "task": "waiter", "reason": "block", "blocked_on": "wait"}]
    ident = {"workload_id": "w", "condition": "fixed", "source_sha256": "0" * 64, "sim": "mock@0"}
    rows = [dict(ident, **r) for r in compute(run, events).rows]
    assert {(r["entity"], r["t"], r["value"]) for r in rows if r["metric"] == "arrival"} == {
        ("runner", 1000, 200), ("waiter", 1000, 300)}
    assert not any(r["entity"] == "waiter" and r.get("cause") == "arrive" for r in rows)
    out = {(r["entity"], r["aggregate"]): r["value"]
           for r in agg.compute_aggregates(rows) if r["metric"] == "turnaround"}
    assert out == {("runner", "turnaround_censored"): "800.000000000000",
                   ("waiter", "turnaround_censored"): "700.000000000000"}


def test_wake_aggregates_split_by_channel():
    """Metrics doc §8: the ready_wait aggregates over cause wake come once over
    every channel and once per channel kind, so interaction latency can read the
    input channel alone (9.5 D74)."""
    rows = _wake_records("fixed", [(10, 100, "input"), (20, 5000, "timer"), (30, 300, "input"),
                                   (40, 7000, "timer"), (50, 9000, "timer")])
    out = {(r["cause"], r["channel"], r["aggregate"]): r["value"]
           for r in agg.compute_aggregates(rows) if r["entity"] == "editor"}
    assert out[("wake", "input", "count")] == "2.000000000000"
    assert out[("wake", "input", "max")] == "300.000000000000"
    assert out[("wake", "input", "p99")] == "298.000000000000"         # 100 + 0.99 · 200
    assert out[("wake", "timer", "count")] == "3.000000000000"
    assert out[("wake", "timer", "mean")] == "7000.000000000000"
    assert out[("wake", "", "count")] == "5.000000000000"
    assert out[("", "", "count")] == "5.000000000000"
    assert not any(k[1] and k[0] != "wake" for k in out)                  # the split is on wake only


def test_excess_reads_the_input_channel_only():
    """Metrics doc §8's per-switch excess is interaction latency: with the switch
    window [10000, 15000] holding a keystroke (400) and a timer wake (9000), and the
    rest of the interval a keystroke (100) and a timer wake (7000), the excess is
    400 − 100 = 300; over every wake it would be 4700 − 3550 = 1150."""
    extra = [dict(entity="schedule", metric="config_interval", t=0, value=10000,
                  provenance="unmodified", algorithm="FIFO", index=0),
             dict(entity="schedule", metric="config_interval", t=10000, value=90000,
                  provenance="unmodified", algorithm="MLFQ", index=1),
             dict(entity="schedule", metric="switch_window", t=10000, value=5000,
                  algorithm="MLFQ", index=1, hogs=1)]
    rows = _wake_records("llm_full", [(12000, 400, "input"), (13000, 9000, "timer"),
                                      (50000, 100, "input"), (60000, 7000, "timer")], extra=extra)
    out = {(r["aggregate"], r["index"]): r["value"]
           for r in agg.compute_aggregates(rows, interactive=("editor",)) if r["metric"] == "switch_window"}
    assert out[("excess_switch", "1")] == "300.000000000000"


def test_a_channel_term_scores_the_channel_aggregate():
    """A term naming `channel: input` scores the input channel's P99: fixed [1000, 3000]
    → 2980, oracle [100, 100] → 100, llm_full [500, 1500] → 1490; share 1490/2880.
    The timer wakes beside them would dominate a P99 over every wake."""
    spec = {"files": {"w": {"terms": [
        {"entity": "editor", "metric": "ready_wait", "cause": "wake", "channel": "input",
         "aggregate": "p99", "direction": "lower", "weight": 1.0}]}}}
    runs = {"fixed": [(10, 1000, "input"), (20, 3000, "input"), (30, 50000, "timer")],
            "oracle": [(10, 100, "input"), (20, 100, "input"), (30, 50000, "timer")],
            "llm_full": [(10, 500, "input"), (20, 1500, "input"), (30, 90000, "timer")]}
    rows = []
    for condition, wakes in runs.items():
        rows.extend(agg.compute_aggregates(_wake_records(condition, wakes)))
    term_rows, _ = scorer.score(rows, spec)
    llm = next(r for r in term_rows if r["condition"] == "llm_full")
    assert llm["channel"] == "input"
    assert (llm["value_fixed"], llm["value_oracle"], llm["value_condition"]) == (
        "2980.000000", "100.000000", "1490.000000")
    assert llm["share"] == "0.517361"


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


def test_flip_aggregates_on_mock_switch(fixture_dir, tmp_path):
    """9.21 decision 7 on mock-switch's schedule (boot MLFQ; entry 1 MLFQ with a shorter slice; entry 2 FIFO; entry
    3 MLFQ): three configuration changes; with a log of three queries graded correct, wrong, wrong, two of them
    wrong, and the wrong switch into MLFQ (entry 3) contributing its excess; the wrong FIFO entry contributes nothing
    (no window into FIFO). The fixture's own switch excess for entry 3 is 0 µs (worked.md, "The aggregates, by hand"), so the entry-3
    `excess_switch` row's value is replaced by a 250 µs stand-in: the stand-in is what makes the contribution
    visible — 250 µs when entry 3 is wrong, 0 when every query is correct."""
    import json
    from harness.reader import read_config_schedule, read_recognition_log
    d = fixture_dir("mock-switch")
    rows, _ = records.build(d / "run.json", d / "trace.jsonl", table="calibrated",
                            schedule_path=d / "config-schedule.json")
    aggregates = agg.compute_aggregates(rows, interactive=("editor",))
    stand_in = "250.000000000000"
    entry3 = [i for i, r in enumerate(aggregates) if r["metric"] == "switch_window"
              and r["aggregate"] == "excess_switch" and r["index"] == "3"]
    assert len(entry3) == 1 and aggregates[entry3[0]]["value"] == "0.000000000000"
    aggregates[entry3[0]] = dict(aggregates[entry3[0]], value=stand_in)
    schedule = read_config_schedule(d / "config-schedule.json")
    queries = [{"t_set_change": t, "telemetry": {"t_us": t, "processes": []}, "validation": "unmodified",
                "latency_us": 100, "proposal": {"system": {"mode": "dev", "background_wanted": True}}}
               for t in (500, 10500, 40500)]
    (tmp_path / "log.json").write_text(json.dumps({"workload_id": "mock-switch", "condition": "llm_algo",
                                                   "seed": None, "telemetry": "names", "queries": queries}))
    log = read_recognition_log(tmp_path / "log.json")
    grades = [{"metric": "config_correct", "t": 500, "value": 1}, {"metric": "config_correct", "t": 10500, "value": 0},
              {"metric": "config_correct", "t": 40500, "value": 0}, {"metric": "mode_correct", "t": 40500, "value": 1}]
    out = {r["aggregate"]: r["value"] for r in agg.flip_aggregates(aggregates, schedule, log, grades)}
    assert out == {"change_count": "3.000000000000", "wrong_change_count": "2.000000000000",
                   "wrong_switch_excess_sum": stand_in}
    flip_rows = agg.flip_aggregates(aggregates, schedule, log, grades)
    assert all(r["entity"] == "schedule" and r["metric"] == "config_interval" and r["index"] == "" for r in flip_rows)
    assert {r["workload_id"] for r in flip_rows} == {"mock-switch"} and all(r["condition"] == "llm_algo" for r in flip_rows)
    validate_rows(flip_rows, AGGREGATES_SCHEMA)
    # every query correct: changes stay, nothing is wrong, no excess
    out = {r["aggregate"]: r["value"] for r in agg.flip_aggregates(
        aggregates, schedule, log, [dict(g, value=1) for g in grades])}
    assert out["change_count"] == "3.000000000000" and out["wrong_change_count"] == "0.000000000000"
    assert out["wrong_switch_excess_sum"] == "0.000000000000"
    # an ungraded query (no config_correct row) is a change and never a wrong one
    out = {r["aggregate"]: r["value"] for r in agg.flip_aggregates(aggregates, schedule, log, grades[:1])}
    assert out["wrong_change_count"] == "0.000000000000"
    # a one-entry schedule (the fixed condition's) has no change
    (tmp_path / "one.json").write_text(json.dumps({"workload_id": "mock-switch", "condition": "fixed",
                                                   "schedule": [json.loads((d / "config-schedule.json").read_text())["schedule"][0]]}))
    out = {r["aggregate"]: r["value"] for r in agg.flip_aggregates(aggregates, read_config_schedule(tmp_path / "one.json"), log, grades)}
    assert out["change_count"] == "0.000000000000"
    assert agg.flip_aggregates([], schedule, log, grades) == []


def test_input_latency_aggregates_and_the_censored_mark():
    """input_latency aggregates carry the count of censored keystrokes beside the statistics
    (metrics doc §8, §6.12), and a term whose window holds one is marked censored (§9)."""
    ident = {"workload_id": "w", "condition": "", "table": "", "seed": "", "boot_default": "",
             "telemetry": "focus", "sim": "s", "source_sha256": "0" * 64}

    def rows(condition, values):
        base = [dict(ident, condition=condition, table="" if condition == "fixed" else "prior",
                     entity="lane", metric="busy", t=1000, value=500)]
        return base + [dict(ident, condition=condition, table="" if condition == "fixed" else "prior",
                            entity="e", metric="input_latency", t=10 * k, value=v, censored=c)
                       for k, (v, c) in enumerate(values)]

    fixed = agg.compute_aggregates(rows("fixed", [(9000, 0), (40000, 1)]))
    got = {(r["aggregate"]): r["value"] for r in fixed if r["metric"] == "input_latency"}
    assert got["count"] == agg.fmt(2) and got["censored_count"] == agg.fmt(1) and got["max"] == agg.fmt(40000)
    oracle = agg.compute_aggregates(rows("oracle", [(1000, 0), (2000, 0)]))
    spec = {"files": {"w": {"terms": [{"entity": "e", "metric": "input_latency", "aggregate": "p99",
                                       "direction": "lower", "weight": 1.0}]}}}
    terms, files = scorer.score(fixed + oracle, spec)
    marks = {t["condition"]: t["censored"] for t in terms}
    assert marks == {"fixed": 1, "oracle": 0}
