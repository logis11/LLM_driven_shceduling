"""The integration gate (Phase 10, sub-task 10.2; spec
`_dev/docs/spec/jioh/task-10.2-integration-gate.md`): what the simulator and the daemon must show
on the runner's machine configuration before the RQ0 run may start.

Four parts (decision 13), each run alone and tied to the version strings it checked:

- `unit` — the simulator's black-box unit tests on the configured binary, and each behavioural test
  shown to fail on its mutant (decisions 6–8; `simulator/tests/`);
- `replay` — every hand fixture with a trace under `harness/tools/tests/fixtures/` replayed through
  the configured binary with the invocation contract's flags, twice, the traces compared with the
  fixture's and the records built from them with its `expected.csv` (decisions 1–5);
- `daemon` — the configured daemon and the harness's mock daemon on the run list the runner
  expands from the RQ0 gate spec, every schedule and log compared byte for byte (decision 9);
- `short` — the smoke tool on the machine configuration over seven files, in runs and cache
  directories of its own (decision 12).

A part writes `<part>.json` (its verdict, the versions it checked, its figures) and `<part>.log` into
the results directory. `status` reads them back: the gate is passed when every part passed on the
two version strings the gate spec pins (decision 13), or, before the pins exist, on the versions the
machine configuration names.
"""

import collections
import concurrent.futures
import csv
import datetime
import hashlib
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from . import records as recs
from .runner import Machine, expand, load_machine

HARNESS = pathlib.Path(__file__).resolve().parents[2]
REPO = HARNESS.parent
FIXTURES = HARNESS / "tools" / "tests" / "fixtures"
SIM_TESTS = REPO / "simulator" / "tests"
PARTS = ("unit", "replay", "daemon", "short")
DEPENDS = {"unit": ("simulator",), "replay": ("simulator",), "daemon": ("daemon",), "short": ("simulator", "daemon")}

# decision 1: replayed with every batch_bandwidth_cap null (memo_261111 Part K2) — the mock scheduler
# the fixtures were derived with models no cap (the fixtures README, rule 7)
CAP_NULL = ("mock-guards", "mock-p1a", "mock-switch")
# the unit tests (simulator/src/Makefile's `check`), in its order
UNIT_TESTS = ("test_batch_class.py", "test_switch_demand.py", "test_cap_ceiling.py", "test_idle_class.py",
              "test_edf_chain.py", "test_spawn_children.py", "test_invocation.py")
# decision 12: the short run's files
SHORT_FILES = ("c1-photo", "c1-office", "c7-mail", "c2-p2b", "c1-gaming", "c7-compile", "c1-compile")
# records columns that name the program and the trace's bytes, not what the trace says (decision 3)
NOT_COMPARED = ("sim", "source_sha256")
BIG_WORKLOAD = 50 << 20          # bytes: a daemon on such a file holds 1–2 GB (c6-dual 1.7 GB, 2026-11-14)


class GateError(Exception):
    """A part cannot run: the machine configuration names a version its sources do not have."""


# ---------------------------------------------------------------- versions

def _sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _rel(path) -> str:
    """A path as the results record it: relative to the repository when it lies inside."""
    p = pathlib.Path(path).resolve()
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def make_version(tree) -> str:
    p = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(REPO / tree), "version"],
                       capture_output=True, text=True, check=True)
    return p.stdout.strip()


def compiler() -> str:
    cxx = os.environ.get("CXX", "g++")                   # simulator/src/Makefile's default
    p = subprocess.run([cxx, "--version"], capture_output=True, text=True)
    return f"{cxx}: " + (p.stdout.splitlines() or ["?"])[0]


def binary_header(binary) -> str:
    """The `sim` the binary writes in a trace header, read off a one-task run."""
    with tempfile.TemporaryDirectory() as d:
        w, s, t = (pathlib.Path(d) / n for n in ("w.json", "s.json", "t.jsonl"))
        w.write_text(json.dumps({"meta": {"id": "probe"}, "ground_truth": {},
                                 "events": [{"op": "arrive", "t": 0, "id": "a", "name": "a",
                                             "program": [{"op": "RUN", "us": 1}, {"op": "EXIT"}]}]}))
        boot = json.loads((HARNESS / "boot-defaults" / "ostep.json").read_text())
        s.write_text(json.dumps({"workload_id": "probe", "condition": "fixed",
                                 "schedule": [{"t_us": 0, "config": boot, "provenance": "fallback"}]}))
        subprocess.run([binary, "--workload", str(w), "--schedule", str(s), "--out-trace", str(t)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return json.loads(t.read_text().splitlines()[0])["sim"]


def simulator_identity(machine: Machine) -> dict:
    """The configured simulator checked against its sources: the version the machine configuration
    names must be the one `make -C simulator/src version` prints and the one the binary writes."""
    binary = machine.simulator.command[0]
    source = make_version("simulator/src")
    header = binary_header(binary)
    if not (machine.simulator.version == source == header):
        raise GateError(f"simulator: the machine configuration names {machine.simulator.version!r}, the source "
                        f"{source!r}, the binary {binary} writes {header!r} — rebuild (make -C simulator/src) "
                        f"and name the source's version")
    return {"version": source, "binary": _rel(binary), "binary_sha256": _sha256(binary), "compiler": compiler()}


def daemon_identity(machine: Machine) -> dict:
    source = make_version("daemon")
    if machine.daemon.version != source:
        raise GateError(f"daemon: the machine configuration names {machine.daemon.version!r}, the source "
                        f"{source!r} (make -C daemon version)")
    return {"version": source, "command": [_rel(c) if pathlib.Path(c).is_absolute() else c
                                           for c in machine.daemon.command]}


# ------------------------------------------------------------------ results

def _now() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def write_result(results_dir, part, passed, identity, figures, log_text, started):
    results_dir = pathlib.Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    doc = {"part": part, "passed": bool(passed), "started": started, "finished": _now(), **identity,
           "figures": figures}
    (results_dir / f"{part}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    (results_dir / f"{part}.log").write_text(log_text)
    return doc


def status(results_dir, pins: Dict[str, Optional[str]]):
    """[(part, state, detail)] and the gate's verdict. `pins` maps `simulator` and `daemon` to the
    version each part must have passed on."""
    rows, ok = [], True
    for part in PARTS:
        path = pathlib.Path(results_dir) / f"{part}.json"
        if not path.is_file():
            rows.append((part, "not run", "")); ok = False
            continue
        doc = json.loads(path.read_text())
        stale = [f"{p} {doc.get(p, {}).get('version')!r} ≠ {pins[p]!r}" for p in DEPENDS[part]
                 if doc.get(p, {}).get("version") != pins[p]]
        versions = ", ".join(str(doc.get(p, {}).get("version")) for p in DEPENDS[part])
        if stale:
            rows.append((part, "stale", "; ".join(stale))); ok = False
        elif not doc["passed"]:
            rows.append((part, "failed", f"on {versions}, {doc['finished']}")); ok = False
        else:
            rows.append((part, "passed", f"on {versions}, {doc['finished']}"))
    return rows, ok


# --------------------------------------------------------------- part: unit

def part_unit(machine: Machine, results_dir, mutants=True):
    started = _now()
    ident = {"simulator": simulator_identity(machine)}
    binary = machine.simulator.command[0]
    log, tests = io.StringIO(), []
    for name in UNIT_TESTS:
        p = subprocess.run([sys.executable, str(SIM_TESTS / name), binary], capture_output=True, text=True,
                           timeout=1800)
        tests.append({"test": name, "exit": p.returncode})
        log.write(f"== {name} (exit {p.returncode})\n{p.stdout}{p.stderr}\n")
    figures = {"tests": tests}
    passed = all(t["exit"] == 0 for t in tests)
    if mutants:                                                         # decision 8, simulator/tests/mutants.py
        p = subprocess.run([sys.executable, str(SIM_TESTS / "mutants.py"), "--json"], capture_output=True,
                           text=True, timeout=3600)
        try:
            rows = json.loads(p.stdout)
        except ValueError:
            rows = []
            log.write(f"== mutants: no result (exit {p.returncode})\n{p.stdout}{p.stderr}\n")
        for r in rows:
            log.write(f"== mutant {r['mutant']} → {r['test']}: "
                      f"{'fails as it must' if r['test_failed'] else 'DOES NOT FAIL'}\n{r['output']}\n")
        figures["mutants"] = [{k: r[k] for k in ("mutant", "test", "takes_out", "test_failed")} for r in rows]
        passed = passed and bool(rows) and all(r["test_failed"] for r in rows)
    else:
        passed = False                    # a quick look: the part passes only with every test shown to fail
    return write_result(results_dir, "unit", passed, ident, figures, log.getvalue(), started)


# ------------------------------------------------------------- part: replay

@dataclass
class Case:
    name: str
    dir: pathlib.Path
    kind: str                       # "hand": run.json + trace.jsonl; "reference": workload.json + reference-trace.jsonl


def cases(fixtures=FIXTURES, only=None) -> List[Case]:
    out = []
    for d in sorted(pathlib.Path(fixtures).iterdir()):
        if only and d.name not in only:
            continue
        if (d / "run.json").is_file() and (d / "trace.jsonl").is_file():
            out.append(Case(d.name, d, "hand"))
        elif (d / "workload.json").is_file() and (d / "reference-trace.jsonl").is_file():
            out.append(Case(d.name, d, "reference"))
    return out


def read_jsonl(path) -> List[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def boot_entry() -> dict:
    return json.loads((HARNESS / "boot-defaults" / "ostep.json").read_text())


def schedule_for(case: Case, expected: List[dict]) -> dict:
    """The config schedule the case is replayed under (decisions 1 and 5)."""
    boot = boot_entry()
    if case.kind == "reference":                      # its reference trace's own schedule: the boot entry alone
        wl = json.loads((case.dir / "workload.json").read_text())
        return {"workload_id": wl["meta"]["id"], "condition": "fixed",
                "schedule": [{"t_us": 0, "config": boot, "provenance": "fallback"}]}
    path = case.dir / "config-schedule.json"
    if path.is_file():
        sched = json.loads(path.read_text())
        if case.name in CAP_NULL:
            for e in sched["schedule"]:
                e["config"]["batch_bandwidth_cap"] = None
        return sched
    # decision 5: one entry per config_applied line at its time, the boot parameters from ostep.json
    meta = next(e for e in expected if e["event"] == "meta")
    entries = []
    for e in expected:
        if e["event"] != "config_applied":
            continue
        if e["algorithm"] == boot["algorithm"]:
            params = dict(boot["params"])
        elif e["algorithm"] == "FIFO":
            params = {}                               # FIFO takes no parameter (recognition-vocabulary §2)
        else:
            raise ValueError(f"{case.name}: a config_applied line under {e['algorithm']}, whose parameters "
                             f"the boot default does not carry")
        entries.append({"t_us": e["t"], "config": {"algorithm": e["algorithm"], "params": params,
                                                   "batch_bandwidth_cap": None},
                        "provenance": e["provenance"]})
    return {"workload_id": meta["workload_id"], "condition": meta["condition"], "schedule": entries}


def workload_for(case: Case) -> dict:
    if case.kind == "reference":
        return json.loads((case.dir / "workload.json").read_text())
    run = json.loads((case.dir / "run.json").read_text())   # the run file is the workload; its id becomes meta.id
    return {"meta": {"id": run["workload_id"]}, "ground_truth": {}, "events": run["events"]}


def compared(events: List[dict]) -> List[dict]:
    """The lines compared: the header and the x_ diagnostics left out on both sides (decision 2)."""
    return [e for e in events if e["event"] != "meta" and not e["event"].startswith("x_")]


def by_instant(events: List[dict]):
    groups = collections.OrderedDict()
    for e in events:
        groups.setdefault(e["t"], []).append(json.dumps(e, sort_keys=True))
    return {t: sorted(v) for t, v in groups.items()}


def compare_lines(got: List[dict], want: List[dict]):
    """('identical' | 'same-µs order' | 'differs', the first differing instants)."""
    got, want = compared(got), compared(want)
    if got == want:
        return "identical", []
    g, w = by_instant(got), by_instant(want)
    if g == w:
        return "same-µs order", []
    diff = [(t, w.get(t, []), g.get(t, [])) for t in sorted(set(g) | set(w)) if g.get(t) != w.get(t)]
    return "differs", diff[:5]


def _csv_rows(path) -> List[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return [{k: v for k, v in r.items() if k not in NOT_COMPARED} for r in csv.DictReader(f)]


def compare_records(case: Case, trace_path, tmp) -> Optional[dict]:
    """The records the harness builds from the simulator's trace against the fixture's expected.csv, every
    column but `sim` and `source_sha256` (decision 3), built as the fixture's own test builds them: its
    config-schedule.json when it has one, else no schedule (decision 5), the identity the trace does not
    carry — table, seed, telemetry — read from expected.csv. None for a fixture with no expected.csv."""
    expected = case.dir / "expected.csv"
    if not expected.is_file():
        return None
    want = _csv_rows(expected)
    ident = want[0] if want else {}
    schedule = case.dir / "config-schedule.json"
    rows, messages = recs.build(case.dir / "run.json", trace_path, table=ident.get("table", ""),
                                seed=ident.get("seed", ""), boot_default=ident.get("boot_default", ""),
                                schedule_path=schedule if schedule.is_file() else None,
                                telemetry=ident.get("telemetry", ""))
    out = pathlib.Path(tmp) / f"{case.name}.records.csv"
    recs.write_csv(rows, out)
    got = _csv_rows(out)
    first = next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), None)
    if first is None and len(got) != len(want):
        first = min(len(got), len(want))
    return {"equal": first is None, "rows": len(got), "expected_rows": len(want), "guard_messages": messages,
            "first_difference": None if first is None else {
                "row": first + 1, "want": want[first] if first < len(want) else None,
                "got": got[first] if first < len(got) else None}}


def replay_case(binary, version, case: Case, tmp) -> dict:
    expected = read_jsonl(case.dir / ("trace.jsonl" if case.kind == "hand" else "reference-trace.jsonl"))
    tmp = pathlib.Path(tmp)
    w, s = tmp / f"{case.name}.workload.json", tmp / f"{case.name}.schedule.json"
    w.write_text(json.dumps(workload_for(case)))
    s.write_text(json.dumps(schedule_for(case, expected)))
    traces = []
    for k in (1, 2):
        t = tmp / f"{case.name}.trace{k}.jsonl"
        p = subprocess.run([binary, "--workload", str(w), "--schedule", str(s), "--out-trace", str(t)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if p.returncode != 0:
            return {"case": case.name, "kind": case.kind, "passed": False,
                    "error": f"exit {p.returncode}: {p.stderr.strip()}"}
        traces.append(t)
    got = read_jsonl(traces[0])
    rerun_identical = traces[0].read_bytes() == traces[1].read_bytes()
    header = got[0].get("sim") if got and got[0]["event"] == "meta" else None
    verdict, diff = compare_lines(got, expected)
    rec = compare_records(case, traces[0], tmp) if case.kind == "hand" else None
    passed = (verdict in ("identical", "same-µs order") and rerun_identical and header == version
              and (rec is None or rec["equal"]))
    return {"case": case.name, "kind": case.kind, "passed": passed, "lines": verdict,
            "compared_lines": len(compared(got)), "rerun_identical": rerun_identical, "header_sim": header,
            "cap_null": case.name in CAP_NULL,
            "schedule": "config-schedule.json" if (case.dir / "config-schedule.json").is_file()
            else ("boot entry" if case.kind == "reference" else "rebuilt from config_applied"),
            "records": rec, "first_differences": diff}


def part_replay(machine: Machine, results_dir, only=None):
    started = _now()
    ident = {"simulator": simulator_identity(machine)}
    rows, log = [], io.StringIO()
    with tempfile.TemporaryDirectory() as tmp:
        for case in cases(only=only):
            r = replay_case(machine.simulator.command[0], ident["simulator"]["version"], case, tmp)
            rows.append(r)
            rec = r.get("records")
            log.write(f"{case.name:14} {case.kind:9} {r.get('lines', r.get('error'))}"
                      f"{'' if rec is None else ', records ' + ('equal' if rec['equal'] else 'DIFFER') + ' (%d rows)' % rec['rows']}"
                      f", rerun {'identical' if r.get('rerun_identical') else 'DIFFERS'}"
                      f", header {r.get('header_sim')}\n")
            for t, want, got in r.get("first_differences") or []:
                log.write(f"    at {t} µs\n      want {want}\n      got  {got}\n")
            if rec and rec.get("first_difference"):
                log.write(f"    records row {rec['first_difference']['row']}\n"
                          f"      want {rec['first_difference']['want']}\n      got  {rec['first_difference']['got']}\n")
    passed = bool(rows) and all(r["passed"] for r in rows)
    return write_result(results_dir, "replay", passed, ident, {"cases": rows}, log.getvalue(), started)


# ------------------------------------------------------------- part: daemon

def mock_daemon(root=REPO):
    """The harness's mock daemon, as the committed example configuration names it."""
    return load_machine(HARNESS / "runner.example.yaml", root).daemon


def daemon_argv(command, run, table_path, out_dir):
    argv = list(command) + ["--workload", str(run.workload_file.resolve()),
                            "--driver-table", str(pathlib.Path(run.table_file or table_path).resolve()),
                            "--boot-default", str(run.boot_file.resolve()),
                            "--condition", run.condition] + (["--seed", run.seed] if run.seed else [])
    argv += ["--telemetry", run.telemetry,
             "--out-schedule", str(out_dir / "schedule.json"), "--out-log", str(out_dir / "log.json")]
    return argv


def compare_daemon_run(real, mock, run, table_path, tmp_root, big: threading.Semaphore):
    """One run of the list through both daemons, as the runner invokes a daemon (runner.invoke's flags);
    (identity, None) when every output is byte-identical, else (identity, what differs)."""
    ident = "/".join([run.workload_id, run.name])
    heavy = run.workload_file.stat().st_size >= BIG_WORKLOAD
    if heavy:
        big.acquire()
    try:
        with tempfile.TemporaryDirectory(dir=tmp_root) as d:
            outs = {}
            for which, prog in (("real", real), ("mock", mock)):
                out = pathlib.Path(d) / which
                out.mkdir()
                p = subprocess.run(daemon_argv(prog.command, run, table_path, out), stdout=subprocess.DEVNULL,
                                   stderr=subprocess.PIPE, text=True)
                if p.returncode != 0:
                    return ident, f"{which} exit {p.returncode}: {p.stderr.strip()[-300:]}"
                outs[which] = {n: (out / n).read_bytes() for n in ("schedule.json", "log.json")}
            bad = [n for n in ("schedule.json", "log.json") if outs["real"][n] != outs["mock"][n]]
            return ident, (f"{', '.join(bad)} differ" if bad else None)
    finally:
        if heavy:
            big.release()


def run_list_sha256(runs) -> str:
    material = [[r.workload_id, r.condition, r.table, r.seed, r.boot_default, r.telemetry,
                 str(r.table_file or "")] for r in runs]
    return hashlib.sha256(json.dumps(material).encode()).hexdigest()


def part_daemon(machine: Machine, results_dir, spec_path, workers=6, heavy=2, limit=None, progress=None):
    started = _now()
    ident = {"daemon": daemon_identity(machine)}
    import yaml
    spec = yaml.safe_load(pathlib.Path(spec_path).read_text())
    table_path = REPO / spec["pins"]["driver_table"]["path"]
    runs = expand(spec_path, machine, REPO)
    listed = len(runs)
    if limit:
        runs = runs[:limit]
    mock = mock_daemon()
    mock_sources = {p.name: _sha256(p) for p in (HARNESS / "tools" / "tests" / "mocks").glob("*daemon.py")}
    t0 = time.time()
    differing, done = [], 0
    big = threading.Semaphore(heavy)
    with tempfile.TemporaryDirectory() as tmp_root:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(compare_daemon_run, machine.daemon, mock, r, table_path, tmp_root, big) for r in runs]
            for f in concurrent.futures.as_completed(futures):
                name, what = f.result()
                done += 1
                if what:
                    differing.append({"run": name, "difference": what})
                if progress and done % 500 == 0:
                    progress(f"daemon: {done} of {len(runs)} compared, {len(differing)} differing, "
                             f"{time.time() - t0:.0f} s")
    differing.sort(key=lambda d: d["run"])
    figures = {"spec": str(pathlib.Path(spec_path).resolve().relative_to(REPO)), "spec_sha256": _sha256(spec_path),
               "run_list": listed, "compared": len(runs), "identical": len(runs) - len(differing),
               "differing": differing[:50], "differing_count": len(differing),
               "run_list_sha256": run_list_sha256(runs), "mock": {"command": [_rel(c) if pathlib.Path(c).is_absolute() else c
                                                                               for c in mock.command],
                                                                   "version": mock.version, "sources": mock_sources},
               "workers": workers, "heavy_at_once": heavy, "wall_seconds": round(time.time() - t0, 1)}
    passed = not differing and len(runs) == listed
    log = (f"{len(runs)} of the {listed} runs the runner expands from {figures['spec']} compared: "
           f"{figures['identical']} byte-identical (schedule and log), {len(differing)} differing\n"
           + "".join(f"  {d['run']}: {d['difference']}\n" for d in differing))
    return write_result(results_dir, "daemon", passed, ident, figures, log, started)


# -------------------------------------------------------------- part: short

def part_short(machine_path, machine: Machine, results_dir, runs_dir):
    started = _now()
    ident = {"simulator": simulator_identity(machine), "daemon": daemon_identity(machine)}
    runs_dir = pathlib.Path(runs_dir)
    cmd = [sys.executable, str(HARNESS / "tools" / "smoke.py"), "--machine", str(machine_path),
           "--workloads", *SHORT_FILES, "--runs-dir", str(runs_dir), "--cache-dir", str(runs_dir / ".cache")]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    wall = time.time() - t0
    exp = runs_dir / "smoke"
    figures = {"files": list(SHORT_FILES), "exit": p.returncode, "wall_seconds": round(wall, 1),
               "runs_dir": _rel(runs_dir)}
    guards_csv = exp / "guards.csv"
    if p.returncode == 0 and guards_csv.is_file():
        with open(guards_csv, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        figures["guard_rows"] = len(rows)
        figures["guard_results"] = dict(collections.Counter(r["result"] for r in rows))
        figures["guards_failed"] = [{k: r[k] for k in ("workload_id", "condition", "seed", "guard", "value", "reason")}
                                    for r in rows if r["result"] == "fail"]
        report = json.loads((exp / "report.json").read_text())
        figures["verdict"] = report["verdict"]
    if (exp / "failures.json").is_file():
        figures["failures"] = json.loads((exp / "failures.json").read_text())
    passed = p.returncode == 0 and (exp / "report.json").is_file()
    return write_result(results_dir, "short", passed, ident, figures, p.stdout + p.stderr, started)


__all__ = ["CAP_NULL", "Case", "GateError", "PARTS", "SHORT_FILES", "UNIT_TESTS", "cases", "compare_lines",
           "compare_records", "part_daemon", "part_replay", "part_short", "part_unit", "replay_case",
           "schedule_for", "status", "workload_for"]
