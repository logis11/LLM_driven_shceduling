"""The integration gate (10.2 spec, _dev/docs/spec/jioh/task-10.2-integration-gate.md): the schedules
the fixtures are replayed under (decisions 1 and 5), when a replayed fixture matches (decisions 2 and
3), the gate's status over its parts (decision 13), and — when the reference simulator is built from
the current source — the replay itself."""

import json
import pathlib
import shutil
import subprocess

import pytest

from conftest import FIXTURES, REPO
from harness import integration as gate

SIM = REPO / "simulator" / "src" / "sim"
BOOT = json.loads((REPO / "harness" / "boot-defaults" / "ostep.json").read_text())


def _case(name):
    return next(c for c in gate.cases() if c.name == name)


def _lines(path):
    return gate.read_jsonl(path)


# ------------------------------------------------------------------ cases

def test_the_cases_are_the_nine_fixtures_with_a_trace():
    found = [(c.name, c.kind) for c in gate.cases()]
    assert found == [("fix-object", "reference"), ("fix-tree", "reference"),
                     ("mock-chain", "hand"), ("mock-guards", "hand"), ("mock-media", "hand"),
                     ("mock-office", "hand"), ("mock-p1a", "hand"), ("mock-switch", "hand"), ("mock-wakes", "hand")]


# -------------------------------------------------------------- schedules

@pytest.mark.parametrize("name", ["mock-office", "mock-wakes", "mock-media", "mock-chain"])
def test_a_fixture_without_a_schedule_file_is_replayed_under_its_own_config_applied_lines(name):
    case = _case(name)
    expected = _lines(case.dir / "trace.jsonl")
    sched = gate.schedule_for(case, expected)
    applied = [e for e in expected if e["event"] == "config_applied"]
    assert [(e["t_us"], e["config"]["algorithm"], e["provenance"]) for e in sched["schedule"]] == \
        [(e["t"], e["algorithm"], e["provenance"]) for e in applied]
    for e in sched["schedule"]:
        assert e["config"]["batch_bandwidth_cap"] is None
        assert e["config"]["params"] == (BOOT["params"] if e["config"]["algorithm"] == "MLFQ" else {})
    meta = expected[0]
    assert (sched["workload_id"], sched["condition"]) == (meta["workload_id"], meta["condition"])


@pytest.mark.parametrize("name", gate.CAP_NULL)
def test_the_three_schedule_files_are_replayed_with_every_cap_null(name):
    case = _case(name)
    own = json.loads((case.dir / "config-schedule.json").read_text())
    sched = gate.schedule_for(case, _lines(case.dir / "trace.jsonl"))
    assert [e["config"]["batch_bandwidth_cap"] for e in sched["schedule"]] == [None] * len(own["schedule"])
    for mine, theirs in zip(sched["schedule"], own["schedule"]):
        theirs["config"]["batch_bandwidth_cap"] = None
        assert mine == theirs                     # nothing else moves


def test_a_reference_fixture_is_replayed_under_the_boot_entry_alone():
    case = _case("fix-object")
    sched = gate.schedule_for(case, _lines(case.dir / "reference-trace.jsonl"))
    assert sched == {"workload_id": "fix-object", "condition": "fixed",
                     "schedule": [{"t_us": 0, "config": BOOT, "provenance": "fallback"}]}


def test_a_config_applied_line_of_an_algorithm_the_boot_default_does_not_carry_is_refused(tmp_path):
    d = tmp_path / "mock-x"
    d.mkdir()
    case = gate.Case("mock-x", d, "hand")
    expected = [{"event": "meta", "workload_id": "x", "condition": "oracle", "sim": "m", "schedule_entries": 2},
                {"event": "config_applied", "t": 0, "index": 0, "algorithm": "MLFQ", "provenance": "fallback"},
                {"event": "config_applied", "t": 5, "index": 1, "algorithm": "EDF", "provenance": "unmodified"}]
    with pytest.raises(ValueError, match="EDF"):
        gate.schedule_for(case, expected)


# -------------------------------------------------------------- matching

def _ev(t, event, **kw):
    return {"event": event, "t": t, **kw}


def test_lines_match_in_any_order_within_a_microsecond_and_only_there():
    a = [_ev(0, "ready", task="x", cause="arrive"), _ev(0, "ready", task="y", cause="arrive"), _ev(5, "run_start", task="x")]
    swapped = [a[1], a[0], a[2]]
    assert gate.compare_lines(a, a)[0] == "identical"
    assert gate.compare_lines(swapped, a)[0] == "same-µs order"
    moved = [a[0], _ev(1, "ready", task="y", cause="arrive"), a[2]]
    verdict, diff = gate.compare_lines(moved, a)
    assert verdict == "differs" and [t for t, _w, _g in diff] == [0, 1]


def test_the_header_and_the_x_lines_are_left_out_of_the_comparison():
    want = [{"event": "meta", "workload_id": "w", "condition": "fixed", "sim": "mock@0", "schedule_entries": 1},
            _ev(0, "run_start", task="x")]
    got = [{"event": "meta", "workload_id": "w", "condition": "fixed", "sim": "simulator@0123456789ab",
            "schedule_entries": 1}, _ev(0, "x_mlfq_boost"), _ev(0, "run_start", task="x")]
    assert gate.compare_lines(got, want)[0] == "identical"


@pytest.mark.parametrize("name", ["mock-office", "mock-guards", "mock-switch"])
def test_the_fixtures_own_trace_builds_records_equal_to_its_expected_csv(name, tmp_path):
    case = _case(name)
    rec = gate.compare_records(case, case.dir / "trace.jsonl", tmp_path)
    assert rec["equal"] and rec["rows"] == rec["expected_rows"] > 0 and rec["guard_messages"] == []


def test_records_ignore_the_program_and_the_bytes_but_nothing_else(tmp_path):
    case = _case("mock-office")
    lines = _lines(case.dir / "trace.jsonl")
    lines[0]["sim"] = "simulator@0123456789ab"            # sim and source_sha256 change, nothing else does
    renamed = tmp_path / "renamed.jsonl"
    renamed.write_text("".join(json.dumps(e) + "\n" for e in lines))
    assert gate.compare_records(case, renamed, tmp_path)["equal"]
    k = next(i for i, e in enumerate(lines) if e["event"] == "run_end")
    lines[k]["t"] += 1
    shifted = tmp_path / "shifted.jsonl"
    shifted.write_text("".join(json.dumps(e) + "\n" for e in lines))
    rec = gate.compare_records(case, shifted, tmp_path)
    assert not rec["equal"] and rec["first_difference"]["row"] >= 1


def test_a_reference_fixture_has_no_records_comparison(tmp_path):
    assert gate.compare_records(_case("fix-tree"), FIXTURES / "fix-tree" / "reference-trace.jsonl", tmp_path) is None


# ---------------------------------------------------------------- status

def _result(d, part, passed=True, sim="simulator@aaaaaaaaaaaa", daemon="daemon@bbbbbbbbbbbb"):
    doc = {"part": part, "passed": passed, "finished": "2026-11-14T00:00:00+09:00"}
    for role in gate.DEPENDS[part]:
        doc[role] = {"version": sim if role == "simulator" else daemon}
    (d / f"{part}.json").write_text(json.dumps(doc))


PINS = {"simulator": "simulator@aaaaaaaaaaaa", "daemon": "daemon@bbbbbbbbbbbb"}


def test_the_gate_is_passed_when_every_part_passed_on_the_pinned_versions(tmp_path):
    for part in gate.PARTS:
        _result(tmp_path, part)
    rows, ok = gate.status(tmp_path, PINS)
    assert ok and [s for _p, s, _d in rows] == ["passed"] * 4


def test_a_part_not_run_failed_or_on_another_version_leaves_the_gate_unpassed(tmp_path):
    _result(tmp_path, "unit")
    _result(tmp_path, "replay", sim="simulator@cccccccccccc")       # a simulator change after the part ran
    _result(tmp_path, "daemon", passed=False)
    rows, ok = gate.status(tmp_path, PINS)
    assert not ok
    assert [s for _p, s, _d in rows] == ["passed", "stale", "failed", "not run"]


def test_a_daemon_change_makes_the_daemon_and_short_parts_stale_alone(tmp_path):
    for part in gate.PARTS:
        _result(tmp_path, part)
    rows, ok = gate.status(tmp_path, {**PINS, "daemon": "daemon@dddddddddddd"})
    assert not ok and [s for _p, s, _d in rows] == ["passed", "passed", "stale", "stale"]


# -------------------------------------------------------- on the binary

def _built_from_source():
    if not SIM.is_file():
        return False
    return gate.binary_header(str(SIM)) == gate.make_version("simulator/src")


needs_sim = pytest.mark.skipif(not _built_from_source(),
                               reason="simulator/src/sim absent or not built from the current source")


@needs_sim
@pytest.mark.parametrize("case", gate.cases(), ids=lambda c: c.name)
def test_every_fixture_replays_through_the_binary(case, tmp_path):
    r = gate.replay_case(str(SIM), gate.make_version("simulator/src"), case, tmp_path)
    assert r["passed"], r
