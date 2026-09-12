"""The runner (8.6 spec): the matrix from the per-experiment spec, invocation
through contract 10 with both programs executed twice, the execution cache,
the run directories and manifests, and the pipeline through the report on a
handful of coreset files via the generated smoke spec."""

import json
import subprocess
import sys
import textwrap

import pytest
import yaml

from conftest import FIXTURES, REPO, TOOLS
from harness import guards as guards_mod
from harness.evaluator import GateError
from harness.outputs import read_csv
from harness.runner import (Machine, Program, RunError, cache_key, expand, invoke, load_machine,
                            run_experiment, write_smoke_spec)

FX = FIXTURES / "mock-experiment"
BUILD = REPO / "dataset" / "build" / "coreset-single"
EXAMPLE = REPO / "harness" / "runner.example.yaml"
needs_build = pytest.mark.skipif(not BUILD.exists(), reason="compiled coreset absent")


def _machine(tmp_path, **override):
    m = load_machine(EXAMPLE, REPO)
    fields = {"daemon": m.daemon, "simulator": m.simulator, "build_dir": m.build_dir,
              "boot_defaults_dir": m.boot_defaults_dir, "runs_dir": tmp_path / "runs",
              "cache_dir": tmp_path / "cache"}
    fields.update(override)
    return Machine(**fields)


# ------------------------------------------------------------------ matrix

def test_expand_gives_one_run_per_cell_of_the_matrix(tmp_path):
    runs = expand(FX / "experiment.yaml", _machine(tmp_path), REPO)
    assert [(r.condition, r.seed, r.boot_default) for r in runs] == [
        ("fixed", "", ""), ("fixed", "", "alt"), ("oracle", "", ""), ("random", "1", ""), ("random", "2", "")]
    assert {r.workload_id for r in runs} == {"mock-score"}
    assert [r.table for r in runs] == ["", "", "calibrated", "calibrated", "calibrated"]   # fixed: none
    assert runs[0].boot_file.name == "ostep.json" and runs[1].boot_file.name == "alt.json"
    assert [r.name for r in runs] == ["fixed", "fixed+alt", "oracle", "random-1", "random-2"]


def test_load_machine_resolves_paths_against_the_root():
    m = load_machine(EXAMPLE, REPO)
    assert m.daemon.version and m.simulator.version == "mock-simulator@0"
    assert m.daemon.command[-1].endswith("mock_daemon.py") and m.build_dir == BUILD
    assert m.boot_defaults_dir == REPO / "harness" / "boot-defaults"


# ------------------------------------------------------------------- cache

def test_cache_key_depends_on_version_prefix_condition_seed_and_input_bytes(tmp_path):
    a = tmp_path / "a.json"; a.write_text("{}")
    b = tmp_path / "b.json"; b.write_text("{ }")
    p = Program(command=["x"], version="v1")
    k = cache_key(p, "daemon", "oracle", "", {"workload": a})
    assert k == cache_key(p, "daemon", "oracle", "", {"workload": a})
    assert k != cache_key(p, "daemon", "oracle", "", {"workload": b})
    assert k != cache_key(p, "daemon", "random", "1", {"workload": a})
    assert k != cache_key(Program(command=["x"], version="v2"), "daemon", "oracle", "", {"workload": a})
    assert k != cache_key(Program(command=["x", "--flag"], version="v1"), "daemon", "oracle", "", {"workload": a})
    assert k != cache_key(p, "simulator", "oracle", "", {"workload": a})


FAKE = textwrap.dedent('''
    import argparse, pathlib, sys
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload"); ap.add_argument("--out-a", dest="a"); ap.add_argument("--out-b", dest="b")
    ap.add_argument("--condition"); ap.add_argument("--seed", default=None)
    args = ap.parse_args()
    side = pathlib.Path(sys.argv[0]).with_suffix(".calls")
    side.write_text(side.read_text() + "x" if side.exists() else "x")
    mode = pathlib.Path(sys.argv[0]).with_suffix(".mode").read_text().strip()
    if mode == "fail":
        print("boom", file=sys.stderr); sys.exit(3)
    payload = str(side.stat().st_size) if mode == "flaky" else "stable"
    pathlib.Path(args.a).write_text(payload + "\\n"); pathlib.Path(args.b).write_text("b\\n")
    print("noise on stdout")
''')


def _fake(tmp_path, mode):
    script = tmp_path / "fake.py"
    script.write_text(FAKE)
    script.with_suffix(".mode").write_text(mode)
    return Program(command=[sys.executable, str(script)], version="fake@1"), script.with_suffix(".calls")


def _invoke(tmp_path, program, condition="oracle", seed=""):
    wl = tmp_path / "w.json"; wl.write_text("{}")
    out = tmp_path / "run"; out.mkdir(exist_ok=True)
    return invoke(program, "daemon", tmp_path / "cache", condition, seed,
                  inputs={"workload": wl}, outputs={"out-a": out / "a.txt", "out-b": out / "b.txt"},
                  stderr_log=out / "stderr.log")


def test_invoke_executes_twice_then_serves_from_the_cache(tmp_path):
    program, calls = _fake(tmp_path, "stable")
    first = _invoke(tmp_path, program)
    assert first.cached is False and calls.read_text() == "xx"          # both executions
    assert (tmp_path / "run" / "a.txt").read_text() == "stable\n"
    assert (tmp_path / "run" / "stderr.log").exists()
    entry = tmp_path / "cache" / first.key
    assert (entry / "first" / "a.txt").exists() and (entry / "second" / "a.txt").exists()
    meta = json.loads((entry / "meta.json").read_text())
    assert meta["program"] == "daemon" and meta["version"] == "fake@1" and "workload" in meta["inputs"]
    (tmp_path / "run" / "a.txt").unlink()
    second = _invoke(tmp_path, program)
    assert second.cached is True and second.key == first.key and calls.read_text() == "xx"
    assert (tmp_path / "run" / "a.txt").read_text() == "stable\n"


def test_a_non_zero_exit_is_a_failure_with_nothing_cached_or_left_behind(tmp_path):
    program, calls = _fake(tmp_path, "fail")
    with pytest.raises(RunError, match="exit 3"):
        _invoke(tmp_path, program)
    assert not (tmp_path / "run" / "a.txt").exists()
    assert not any((tmp_path / "cache").iterdir()) if (tmp_path / "cache").exists() else True
    assert "boom" in (tmp_path / "run" / "stderr.log").read_text()
    assert calls.read_text() == "x"                                       # no second execution


def test_a_rerun_that_differs_is_a_failure_and_is_not_cached(tmp_path):
    program, calls = _fake(tmp_path, "flaky")
    with pytest.raises(RunError, match="byte-identical"):
        _invoke(tmp_path, program)
    assert calls.read_text() == "xx"
    assert not (tmp_path / "run" / "a.txt").exists()
    assert not any((tmp_path / "cache").iterdir()) if (tmp_path / "cache").exists() else True


# ---------------------------------------------------------------- pipeline

@needs_build
def test_the_pipeline_runs_a_handful_of_files_through_to_the_report(tmp_path):
    machine = _machine(tmp_path)
    spec = write_smoke_spec(tmp_path / "smoke.yaml", machine, REPO, files=3)
    doc = yaml.safe_load(spec.read_text())
    assert len(doc["files"]["judging"]) == 3 and doc["boot_defaults"]["alternatives"] == []
    result = run_experiment(spec, machine, REPO)
    assert result.failed == [] and result.report["verdict"] in ("pass", "fail", "invalid")
    exp = machine.runs_dir / doc["experiment"]
    for name in ("aggregates.csv", "scores.csv", "guards.csv", "grades.csv", "guards-manifest.json",
                 "grade-manifest.json", "report.json", "report.md"):
        assert (exp / name).exists(), name
    wid = doc["files"]["judging"][0]
    run_dir = exp / wid / "random-1"
    for name in ("schedule.json", "log.json", "trace.jsonl", "trace.rerun.jsonl", "daemon.stderr.log",
                 "simulator.stderr.log", "records.csv", "recognition-records.csv"):
        assert (run_dir / name).exists(), name
    assert not list(run_dir.glob("*.gz"))
    guard_rows = read_csv(exp / "guards.csv", guards_mod.COLUMNS)
    det = [r for r in guard_rows if r["guard"] == "determinism"]
    assert det and all(r["result"] == "pass" for r in det)
    assert {r["condition"] for r in guard_rows} == {"fixed", "oracle", "random"}
    assert len({(r["workload_id"], r["condition"], r["seed"]) for r in guard_rows}) == 3 * 4
    manifest = json.loads((exp / "guards-manifest.json").read_text())
    assert all(r["guard_messages"] == [] and r["rerun_trace"] and r["trace"] for r in manifest["runs"])
    assert result.executed > 0 and result.cached == 0
    again = run_experiment(spec, machine, REPO)
    assert again.executed == 0 and again.cached == result.executed
    assert again.report == result.report


@needs_build
def test_a_failed_run_stops_the_pipeline_before_scoring(tmp_path):
    machine = _machine(tmp_path, simulator=Program(command=[sys.executable, "-c", "import sys; sys.exit(9)"],
                                                    version="broken@0"))
    spec = write_smoke_spec(tmp_path / "smoke.yaml", machine, REPO, files=1)
    result = run_experiment(spec, machine, REPO)
    assert result.report is None and len(result.failed) >= 1
    assert "exit 9" in result.failed[0].reason
    exp = machine.runs_dir / yaml.safe_load(spec.read_text())["experiment"]
    assert not (exp / "scores.csv").exists() and (exp / "failures.json").exists()


@needs_build
def test_a_trace_header_that_names_another_simulator_is_a_failure(tmp_path):
    machine = _machine(tmp_path)
    machine = _machine(tmp_path, simulator=Program(command=machine.simulator.command, version="other@9"))
    spec = write_smoke_spec(tmp_path / "smoke.yaml", machine, REPO, files=1)
    result = run_experiment(spec, machine, REPO)
    assert result.report is None and any("other@9" in f.reason for f in result.failed)


# --------------------------------------------------------------- commands

@needs_build
def test_run_cli(tmp_path):
    machine_path = tmp_path / "machine.yaml"
    doc = yaml.safe_load(EXAMPLE.read_text())
    doc["runs_dir"] = str(tmp_path / "runs"); doc["cache_dir"] = str(tmp_path / "cache")
    machine_path.write_text(yaml.safe_dump(doc))
    spec = write_smoke_spec(tmp_path / "smoke.yaml", load_machine(machine_path, REPO), REPO, files=1)
    proc = subprocess.run([sys.executable, str(TOOLS / "run.py"), "--spec", str(spec),
                           "--machine", str(machine_path)], capture_output=True, text=True)
    assert proc.returncode in (0, 2), proc.stderr
    assert "verdict:" in proc.stdout
    assert (tmp_path / "runs" / yaml.safe_load(spec.read_text())["experiment"] / "report.json").exists()


@needs_build
def test_smoke_cli_generates_runs_and_discards_the_spec(tmp_path):
    machine_path = tmp_path / "machine.yaml"
    doc = yaml.safe_load(EXAMPLE.read_text())
    doc["runs_dir"] = str(tmp_path / "runs"); doc["cache_dir"] = str(tmp_path / "cache")
    machine_path.write_text(yaml.safe_dump(doc))
    proc = subprocess.run([sys.executable, str(TOOLS / "smoke.py"), "--machine", str(machine_path),
                           "--files", "1"], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr                  # the smoke's code is not the verdict's
    assert "verdict:" in proc.stdout
    assert not list((REPO / "harness" / "experiments").glob("*.yaml"))
    assert not list(tmp_path.glob("*.yaml")) or all(p.name == "machine.yaml" for p in tmp_path.glob("*.yaml"))
