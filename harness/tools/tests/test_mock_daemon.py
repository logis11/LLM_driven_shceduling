"""The mock daemon (8.5 spec, decisions 13–16, 19): the visible projection and
the telemetry rules of data-contracts §5, `fixed` / `oracle` / `random`
through the prior table, contract-valid schedules and logs, and the counts
pinned to the 8.4 spec's measured facts."""

import copy
import json
import subprocess
import sys

import pytest

from conftest import REPO, TOOLS
from harness.grader import Run, covering, grade_log, read_driver_table, read_ground_truth
from harness.reader import read_config_schedule, read_recognition_log
from mocks import daemon
from mocks.daemon import MockDaemonError

BUILD = REPO / "dataset" / "build" / "coreset-single"
PRIOR = REPO / "daemon" / "driver-table" / "prior.yaml"
BOOT = REPO / "harness" / "boot-defaults" / "ostep.json"
SCRIPT = TOOLS / "tests" / "mocks" / "mock_daemon.py"

needs_build = pytest.mark.skipif(not BUILD.exists(), reason="compiled coreset absent")


def _arrive(tid, name, t, depart=None, spawn=None):
    ev = {"op": "arrive", "t": t, "id": tid, "name": name,
          "program": [{"op": "RUN", "us": 10}, {"op": "EXIT"}]}
    if depart is not None:
        ev["depart"] = depart
        ev["program"] = [{"op": "WAIT", "channel": f"input:{tid}"}, {"op": "RUN", "us": 10}]
    if spawn is not None:
        ev["spawn_table"] = spawn
        ev["fork_cap"] = 2
    return ev


HAND = {
    "meta": {"id": "hand"},
    "ground_truth": [
        {"t_start": 0, "t_end": 300, "mode": "dev", "attributes": {"background_wanted": True}},
        {"t_start": 300, "t_end": 600, "mode": "ml-train",
         "attributes": {"background_wanted": False, "pre_committed_miss": True}},
        {"t_start": 600, "t_end": 1000, "mode": "ambiguous", "attributes": {"dual_active": True}},
    ],
    "events": [
        _arrive("editor", "code", 0, depart=1000),
        _arrive("chrome1", "chrome", 0, depart=600),
        _arrive("chrome2", "chrome", 0, depart=1000),
        _arrive("train", "python3", 300),
        _arrive("chrome3", "chrome", 300, depart=1000),
        _arrive("chrome4", "chrome", 600, depart=1000),           # replaces chrome1: no set change
        _arrive("build", "make", 800, spawn=[
            {"id": f"build.c{i}", "name": "cc1",
             "program": [{"op": "RUN", "us": 3}, {"op": "EXIT"}]} for i in range(3)]),
        {"op": "wake", "t": 50, "channel": "input:editor", "target": "editor"},
    ],
}


@pytest.fixture(scope="module")
def table():
    return read_driver_table(PRIOR)


@pytest.fixture(scope="module")
def boot():
    return json.loads(BOOT.read_text())


# ------------------------------------------------------- projection (§4, 3b)

def test_projection_is_one_entry_per_task_with_children_folded_by_name():
    proj = daemon.projection(HAND)
    assert proj["workload_id"] == "hand"
    by_id = {(t["name"], t["t_arrive"], t.get("t_depart")) for t in proj["tasks"]}
    assert ("chrome", 0, 600) in by_id and ("chrome", 0, 1000) in by_id      # never folded
    make = next(t for t in proj["tasks"] if t["name"] == "make")
    assert make == {"name": "make", "t_arrive": 800, "children": [{"name": "cc1", "count": 3}]}
    assert all(set(t) <= {"name", "t_arrive", "t_depart", "children"} for t in proj["tasks"])


# ---------------------------------------------------------- snapshots (§5)

def test_snapshots_follow_the_five_telemetry_rules():
    snaps = daemon.snapshots(daemon.projection(HAND))
    assert [s["t_us"] for s in snaps] == [0, 300, 800, 1000]      # 600: unchanged multiset; 50: a wake
    assert snaps[0]["processes"] == [{"name": "chrome", "count": 2}, {"name": "code", "count": 1}]
    assert snaps[1]["processes"] == [{"name": "chrome", "count": 3}, {"name": "code", "count": 1},
                                     {"name": "python3", "count": 1}]        # one snapshot for two events
    assert snaps[2]["processes"] == [{"name": "cc1", "count": 3}, {"name": "chrome", "count": 3},
                                     {"name": "code", "count": 1}, {"name": "make", "count": 1},
                                     {"name": "python3", "count": 1}]        # children with their parent
    assert snaps[3]["processes"] == [{"name": "cc1", "count": 3}, {"name": "make", "count": 1},
                                     {"name": "python3", "count": 1}]        # terminal: finite tasks stay


@needs_build
def test_c1_compile_opens_with_the_guides_two_snapshots():
    doc = json.loads((BUILD / "c1-compile.workload.json").read_text())
    snaps = daemon.snapshots(daemon.projection(doc))
    assert snaps[0] == {"t_us": 0, "processes": [{"name": "code", "count": 1}]}
    assert snaps[1] == {"t_us": 2000000, "processes": [{"name": "cc1", "count": 100},
                                                        {"name": "code", "count": 1},
                                                        {"name": "make", "count": 1}]}
    assert snaps[2]["t_us"] == 60000000 and len(snaps) == 3                  # rule 4


# -------------------------------------------------------------- conditions

def _valid(schedule, log, tmp_path):
    """Round-trip through the frozen readers."""
    sp, lp = tmp_path / "s.json", tmp_path / "l.json"
    sp.write_text(json.dumps(schedule))
    lp.write_text(json.dumps(log))
    return read_config_schedule(sp), read_recognition_log(lp)


def test_fixed_is_the_boot_entry_alone_and_an_empty_log(table, boot, tmp_path):
    schedule, log = daemon.run(HAND, "fixed", table, boot)
    assert schedule == {"workload_id": "hand", "condition": "fixed",
                        "schedule": [{"t_us": 0, "config": boot, "provenance": "fallback"}]}
    assert log == {"workload_id": "hand", "condition": "fixed", "seed": None, "queries": []}
    s, l = _valid(schedule, log, tmp_path)
    assert len(s.entries) == 1 and l.queries == []


def test_oracle_reads_the_segment_and_composes_the_rows_default(table, boot, tmp_path):
    schedule, log = daemon.run(HAND, "oracle", table, boot)
    s, l = _valid(schedule, log, tmp_path)
    assert [q.t_set_change for q in l.queries] == [0, 300, 800, 1000]
    assert [q.latency_us for q in l.queries] == [0, 0, 0, 0]
    assert log["seed"] is None
    q0, q1 = log["queries"][0], log["queries"][1]
    assert q0["proposal"] == {"system": {"mode": "dev", "background_wanted": True}}
    assert q0["validation"] == "unmodified"
    assert q0["telemetry"] == daemon.snapshots(daemon.projection(HAND))[0]
    assert q0["source"]["segment"] == HAND["ground_truth"][0]
    assert q1["proposal"] == {"system": {"mode": "ml-train", "background_wanted": False}}
    row = table.row("ml-train", False)
    e1 = schedule["schedule"][2]
    assert e1["t_us"] == 300 and e1["provenance"] == "unmodified"
    assert e1["config"] == {"algorithm": row["default"],
                            "params": row["entries"][row["default"]]["params"],
                            "batch_bandwidth_cap": row["batch_bandwidth_cap"]}
    assert schedule["schedule"][0] == {"t_us": 0, "config": boot, "provenance": "fallback"}
    assert schedule["schedule"][1]["t_us"] == 0                             # beside the boot entry


def test_oracle_falls_back_on_ambiguous_and_terminal_points(table, boot):
    schedule, log = daemon.run(HAND, "oracle", table, boot)
    for q, entry in zip(log["queries"][2:], schedule["schedule"][3:]):
        assert q["proposal"] is None and q["validation"] == "fallback"
        assert entry["provenance"] == "fallback" and entry["config"] == boot
    assert log["queries"][2]["source"]["segment"]["mode"] == "ambiguous"
    assert log["queries"][3]["source"]["segment"] is None


def test_validation_sequence_mirrors_provenance_minus_boot(table, boot):
    for condition, seed in (("oracle", None), ("random", 3)):
        schedule, log = daemon.run(HAND, condition, table, boot, seed=seed)
        assert ([q["validation"] for q in log["queries"]]
                == [e["provenance"] for e in schedule["schedule"][1:]])
        assert ([q["t_set_change"] for q in log["queries"]]
                == [e["t_us"] for e in schedule["schedule"][1:]])


def test_random_draws_uniformly_over_the_sorted_rows_from_the_seed(table, boot, tmp_path):
    a, log_a = daemon.run(HAND, "random", table, boot, seed=11)
    b, log_b = daemon.run(HAND, "random", table, boot, seed=11)
    c, log_c = daemon.run(HAND, "random", table, boot, seed=12)
    assert (a, log_a) == (b, log_b)
    assert log_a != log_c
    assert log_a["seed"] == 11
    _valid(a, log_a, tmp_path)
    ordered = sorted(table.rows)
    for q in log_a["queries"]:
        draw = q["source"]["draw"]
        assert 0 <= draw < 32
        mode, wanted = ordered[draw]
        assert q["proposal"] == {"system": {"mode": mode, "background_wanted": wanted}}
        assert q["validation"] == "unmodified" and q["latency_us"] == 0
    # every point draws, the terminal one included: the daemon cannot know it is the end
    assert len(log_a["queries"]) == 4 and len(a["schedule"]) == 5


def test_other_conditions_and_wrong_seed_pairings_are_refused(table, boot):
    with pytest.raises(MockDaemonError, match="whitelist"):
        daemon.run(HAND, "whitelist", table, boot)
    with pytest.raises(MockDaemonError, match="seed"):
        daemon.run(HAND, "random", table, boot)
    with pytest.raises(MockDaemonError, match="seed"):
        daemon.run(HAND, "oracle", table, boot, seed=1)
    with pytest.raises(MockDaemonError, match="seed"):
        daemon.run(HAND, "fixed", table, boot, seed=1)


# --------------------------------------------- the 8.4 measured facts (dec. 19)

@needs_build
def test_oracle_over_the_coreset_reproduces_the_measured_graded_set(table, boot, tmp_path):
    files = sorted(BUILD.glob("*.workload.json"))
    assert len(files) == 50
    points = terminal = ambiguous = 0
    graded, graded_files, miss, headline, headline_files = 0, set(), 0, 0, set()
    for path in files:
        doc = json.loads(path.read_text())
        schedule, log = daemon.run(doc, "oracle", table, boot)
        segments = read_ground_truth(path)
        for q in log["queries"]:
            points += 1
            seg = covering(segments, q["t_set_change"])
            if seg is None:
                terminal += 1
            elif seg.mode == "ambiguous":
                ambiguous += 1
        lp = tmp_path / f"{doc['meta']['id']}.json"
        lp.write_text(json.dumps(log))
        rows, messages = grade_log(Run(doc["meta"]["id"], "oracle", "prior", "", "", lp, path, PRIOR))
        assert messages == [], messages                              # the oracle is perfect where graded
        for r in rows:
            if r["metric"] != "mode_correct":
                continue
            graded += 1
            graded_files.add(doc["meta"]["id"])
            if r["pre_committed_miss"]:
                miss += 1
            else:
                headline += 1
                headline_files.add(doc["meta"]["id"])
    assert (points, terminal, ambiguous) == (134, 50, 2)
    assert (graded, len(graded_files), miss) == (82, 49, 10)
    assert (headline, len(headline_files)) == (72, 44)


# --------------------------------------------------------------- the command

@needs_build
def test_cli_writes_both_outputs_deterministically_and_stays_silent(tmp_path):
    wl = BUILD / "c2-p1a.workload.json"
    outs = []
    for i in range(2):
        d = tmp_path / str(i)
        d.mkdir()
        proc = subprocess.run([sys.executable, str(SCRIPT),
                               "--workload", str(wl), "--condition", "random", "--seed", "5",
                               "--driver-table", str(PRIOR), "--boot-default", str(BOOT),
                               "--out-schedule", str(d / "schedule.json"),
                               "--out-log", str(d / "log.json")],
                              capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
        assert proc.stdout == ""
        assert set(p.name for p in d.iterdir()) == {"schedule.json", "log.json"}
        outs.append(((d / "schedule.json").read_bytes(), (d / "log.json").read_bytes()))
        s = read_config_schedule(d / "schedule.json")
        l = read_recognition_log(d / "log.json")
        assert s.workload_id == l.workload_id == "c2-p1a" and l.seed == "5"
    assert outs[0] == outs[1]


@needs_build
def test_cli_refuses_a_missing_flag_a_bad_pairing_and_an_unknown_condition(tmp_path):
    wl = BUILD / "c2-p1a.workload.json"
    base = [sys.executable, str(SCRIPT), "--workload", str(wl),
            "--driver-table", str(PRIOR), "--boot-default", str(BOOT),
            "--out-schedule", str(tmp_path / "s.json"), "--out-log", str(tmp_path / "l.json")]
    for extra in (["--condition", "oracle", "--seed", "1"],
                  ["--condition", "random"],
                  ["--condition", "llm_vocab"],
                  []):
        proc = subprocess.run(base + extra, capture_output=True, text=True)
        assert proc.returncode != 0, extra
        assert proc.stdout == ""
        assert not (tmp_path / "s.json").exists() and not (tmp_path / "l.json").exists()
