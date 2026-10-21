"""The daemon skeleton — the contract invariants a grown daemon must keep.

These pin the shape of what the daemon hands on, not the recognizer's judgement:
the invocation contract's refusals and determinism (`docs/data-contracts.md` §11),
the telemetry rules that decide where the query points are (§5), and the two
output contracts' agreement with each other (§7, §8).
"""

import json
import pathlib
import subprocess
import sys

import pytest

from conftest import REPO, make_table

sys.path.insert(0, str(REPO / "daemon"))

from daemon import DaemonError, projection, run, snapshots  # noqa: E402

DAEMON = REPO / "daemon" / "daemon.py"
BOOT = {"algorithm": "MLFQ",
        "params": {"num_queues": 3, "timeslice_us": 10000,
                   "timeslice_growth": 2, "boost_interval_us": 100000},
        "batch_bandwidth_cap": None}


def table_rows():
    return {(r["mode"], r["background_wanted"]): r for r in make_table("prior")["rows"]}


def workload():
    """Two editors of one name, a hog and an idle indexer, with a focus track
    that moves between the two same-named editors and then to the hog, and a
    middle segment that is `ambiguous`."""
    return {
        "meta": {"id": "hand"},
        "ground_truth": [
            {"t_start": 0, "t_end": 60_000_000, "mode": "dev",
             "attributes": {"background_wanted": True}},
            {"t_start": 60_000_000, "t_end": 90_000_000, "mode": "ambiguous", "attributes": {}},
            {"t_start": 90_000_000, "t_end": 120_000_000, "mode": "ml-train",
             "attributes": {"background_wanted": False}},
        ],
        "focus": [{"t_start": 0, "t_end": 30_000_000, "task": "ed1"},
                  {"t_start": 30_000_000, "t_end": 60_000_000, "task": "ed2"},
                  {"t_start": 60_000_000, "t_end": 120_000_000, "task": "hog"}],
        "events": [
            {"op": "arrive", "t": 0, "id": "ed1", "name": "code",
             "declared_class": "normal", "depart": 120_000_000, "program": []},
            {"op": "arrive", "t": 0, "id": "ed2", "name": "code",
             "declared_class": "normal", "depart": 120_000_000, "program": []},
            {"op": "arrive", "t": 60_000_000, "id": "hog", "name": "python3",
             "declared_class": "normal", "depart": 120_000_000, "program": []},
            {"op": "arrive", "t": 70_000_000, "id": "idx", "name": "tracker-miner-f",
             "declared_class": "idle", "depart": 120_000_000, "program": []},
        ],
    }


# ------------------------------------------------------------- telemetry (§5)

def test_a_move_between_two_instances_of_one_name_is_not_a_set_change():
    """Rule 6: the recognizer learns that *a* process of that name holds the
    focus, not which, so the focus moving from ed1 to ed2 changes nothing."""
    snaps = snapshots(projection(workload()), "focus")
    assert 30_000_000 not in [s["t_us"] for s in snaps]


def test_the_shape_changes_the_snapshot_but_never_the_query_points():
    proj = projection(workload())
    assert ([s["t_us"] for s in snapshots(proj, "focus")]
            == [s["t_us"] for s in snapshots(proj, "names")])
    assert "focus" not in snapshots(proj, "names")[0]


def test_processes_are_sorted_and_counts_are_kept():
    """Rules 1 and 3: the multiset, by name, so two editors of one name are a
    count of two and reruns are byte-identical."""
    first = snapshots(projection(workload()), "focus")[0]
    assert first == {"t_us": 0, "processes": [{"name": "code", "count": 2}], "focus": "code"}


def test_the_final_instant_is_a_snapshot_like_any_other():
    """Rule 4: the daemon cannot know it is the end — the departs at 120 s emit."""
    assert snapshots(projection(workload()), "focus")[-1]["t_us"] == 120_000_000


# ----------------------------------------------------- the two output contracts

def test_fixed_is_one_entry_and_asks_nothing():
    schedule, log = run(workload(), "fixed", table_rows(), BOOT)
    assert schedule["schedule"] == [{"t_us": 0, "config": BOOT, "provenance": "fallback"}]
    assert log["queries"] == []


def test_every_query_point_yields_exactly_one_schedule_entry():
    """§7: so the provenance breakdown is computable from the schedule alone."""
    schedule, log = run(workload(), "oracle", table_rows(), BOOT)
    assert len(schedule["schedule"]) == len(log["queries"]) + 1       # + the boot entry


def test_the_logs_validation_sequence_equals_the_schedules_provenance():
    """§8: the harness guards check this for free; it must hold at the source."""
    schedule, log = run(workload(), "oracle", table_rows(), BOOT)
    assert ([q["validation"] for q in log["queries"]]
            == [e["provenance"] for e in schedule["schedule"][1:]])


def test_an_ambiguous_segment_and_the_terminal_snapshot_fall_back():
    """The oracle has no answer where the answer key has none; the entry still
    exists, repeating the boot default."""
    schedule, log = run(workload(), "oracle", table_rows(), BOOT)
    by_t = {e["t_us"]: e for e in schedule["schedule"][1:]}
    assert by_t[70_000_000]["provenance"] == "fallback"    # inside `ambiguous`
    assert by_t[70_000_000]["config"] == BOOT
    assert by_t[120_000_000]["provenance"] == "fallback"   # no segment covers it
    assert all(q["proposal"] is None for q in log["queries"]
               if q["t_set_change"] in (70_000_000, 120_000_000))


def test_the_oracle_reads_the_segment_covering_each_query_point():
    schedule, _ = run(workload(), "oracle", table_rows(), BOOT)
    at_zero = schedule["schedule"][1]
    assert at_zero["t_us"] == 0 and at_zero["provenance"] == "unmodified"
    assert at_zero["config"]["batch_bandwidth_cap"] == 0.30     # the dev/true row's cap


def test_the_config_is_composed_in_canonical_key_order():
    """The same configuration must not reach the simulator under two spellings:
    the schedule carries the bytes `tools/drivertable/lint.py` composes."""
    schedule, _ = run(workload(), "oracle", table_rows(), BOOT)
    config = schedule["schedule"][1]["config"]
    assert list(config) == sorted(config)
    assert list(config["params"]) == sorted(config["params"])


# --------------------------------------------------------- the seed and refusals

def test_random_draws_from_the_seed_and_nothing_else():
    a, _ = run(workload(), "random", table_rows(), BOOT, seed=5)
    b, _ = run(workload(), "random", table_rows(), BOOT, seed=5)
    c, _ = run(workload(), "random", table_rows(), BOOT, seed=6)
    assert a == b and a != c


@pytest.mark.parametrize("condition,seed", [("random", None), ("oracle", 3), ("fixed", 3)])
def test_the_seed_belongs_to_the_drawing_conditions_alone(condition, seed):
    with pytest.raises(DaemonError):
        run(workload(), condition, table_rows(), BOOT, seed=seed)


@pytest.mark.parametrize("condition", ["llm_vocab", "llm_algo", "llm_full",
                                       "shipped_catalogue", "strongest_name_table", "nope"])
def test_a_condition_this_daemon_does_not_serve_is_refused(condition):
    with pytest.raises(DaemonError):
        run(workload(), condition, table_rows(), BOOT)


# ----------------------------------------------------------- the invocation (§11)

def _invoke(tmp_path, **flags):
    wl = tmp_path / "w.json"
    wl.write_text(json.dumps(workload()))
    boot = tmp_path / "boot.json"
    boot.write_text(json.dumps(BOOT))
    argv = [sys.executable, str(DAEMON), "--workload", str(wl),
            "--driver-table", str(REPO / "daemon" / "driver-table" / "prior.yaml"),
            "--boot-default", str(boot),
            "--out-schedule", str(tmp_path / "s.json"),
            "--out-log", str(tmp_path / "l.json")]
    for name, value in flags.items():
        argv += [f"--{name.replace('_', '-')}", str(value)]
    return subprocess.run(argv, capture_output=True, text=True)


def test_exit_zero_writes_both_outputs_and_nothing_to_stdout(tmp_path):
    done = _invoke(tmp_path, condition="oracle", telemetry="focus")
    assert done.returncode == 0 and done.stdout == ""
    assert json.loads((tmp_path / "s.json").read_text())["condition"] == "oracle"
    assert json.loads((tmp_path / "l.json").read_text())["telemetry"] == "focus"


def test_a_refused_invocation_exits_non_zero_and_says_why_on_stderr(tmp_path):
    done = _invoke(tmp_path, condition="llm_full", telemetry="focus")
    assert done.returncode != 0 and "llm_full" in done.stderr
    assert not (tmp_path / "s.json").exists()


def test_a_missing_flag_is_a_failure_not_a_default(tmp_path):
    """Rule 2: no defaults, no positional arguments."""
    assert _invoke(tmp_path, condition="fixed").returncode != 0


def test_the_same_argument_line_gives_byte_identical_outputs(tmp_path):
    """Rule 11, on which the harness's determinism guard and its cache rest."""
    first = tmp_path / "1"
    second = tmp_path / "2"
    first.mkdir()
    second.mkdir()
    for where in (first, second):
        assert _invoke(where, condition="random", telemetry="names", seed=5).returncode == 0
    assert (first / "s.json").read_bytes() == (second / "s.json").read_bytes()
    assert (first / "l.json").read_bytes() == (second / "l.json").read_bytes()
