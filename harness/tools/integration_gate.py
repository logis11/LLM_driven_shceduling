#!/usr/bin/env python3
"""integration_gate: the integration gate before the RQ0 run (Phase 10, sub-task 10.2; spec
_dev/docs/spec/jioh/task-10.2-integration-gate.md) — the simulator and the daemon the runner's
machine configuration names, shown against the ratified contract.

    integration_gate.py [--parts unit replay daemon short] [--machine runner.yaml]
                        [--results DIR] [--workers N] [--heavy N] [--no-mutants]
    integration_gate.py --status [--machine runner.yaml] [--results DIR]

Runs the named parts, every part when `--parts` is not given (decision 13):

- unit    the simulator's unit tests on the configured binary (simulator/src/Makefile's `check`),
          and each behavioural test shown to fail on its mutant (simulator/tests/mutants.py)
- replay  every hand fixture with a trace replayed through the binary with the contract's flags,
          twice; its lines and its records compared with the fixture's
- daemon  the configured daemon and the mock daemon on the RQ0 gate spec's run list, byte for byte
- short   the smoke tool on the machine configuration over seven files, in runs/integration-gate/

A part first checks that the version the machine configuration names is its source's (`make -C
simulator/src version`, which the binary must also write; `make -C daemon version`) and refuses
otherwise. Each part writes <part>.json and <part>.log into the results directory, by default
_dev/research/jioh/task-10.2-integration-gate/.

`--status` reads them: the gate is passed when every part passed on the version strings the RQ0
gate spec pins (`pins.simulator`, `pins.daemon`), or, while it pins none, on those the machine
configuration names. Exit 0 when the gate is passed or every part run passed, 1 otherwise.
"""
import argparse
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import yaml  # noqa: E402

from harness import integration as gate  # noqa: E402
from harness.runner import load_machine  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
SPEC = REPO / "harness" / "experiments" / "rq0-gate.yaml"
RESULTS = REPO / "_dev" / "research" / "jioh" / "task-10.2-integration-gate"


def pins_of(machine):
    """What each part must have passed on: the gate spec's pins, else the machine configuration's names."""
    pins = (yaml.safe_load(SPEC.read_text()) or {}).get("pins") or {}
    return ({"simulator": (pins.get("simulator") or {}).get("version", machine.simulator.version),
             "daemon": (pins.get("daemon") or {}).get("version", machine.daemon.version)},
            bool(pins.get("simulator") or pins.get("daemon")))


def say(msg):
    print(msg, flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--parts", nargs="+", choices=gate.PARTS, default=list(gate.PARTS))
    ap.add_argument("--status", action="store_true", help="read the parts' results; run nothing")
    ap.add_argument("--machine", default=str(REPO / "harness" / "runner.yaml"))
    ap.add_argument("--results", default=str(RESULTS))
    ap.add_argument("--workers", type=int, default=6, help="daemon: runs compared at once")
    ap.add_argument("--heavy", type=int, default=2, help="daemon: of them, runs at once on a file over 50 MB")
    ap.add_argument("--limit", type=int, default=None, help="daemon: the first N runs alone — a dry run, never a pass")
    ap.add_argument("--no-mutants", action="store_true", help="unit: leave the mutants out — never a pass")
    args = ap.parse_args(argv)
    machine = load_machine(args.machine, REPO)
    if args.status:
        pins, pinned = pins_of(machine)
        rows, ok = gate.status(args.results, pins)
        say(f"against the {'pinned' if pinned else 'configured (nothing pinned yet)'} versions "
            f"{pins['simulator']}, {pins['daemon']}:")
        for part, state, detail in rows:
            say(f"  {part:7} {state:8} {detail}")
        say("integration gate: " + ("passed" if ok else "not passed"))
        return 0 if ok else 1
    ok = True
    for part in args.parts:
        t0 = time.time()
        say(f"== {part}")
        try:
            if part == "unit":
                doc = gate.part_unit(machine, args.results, mutants=not args.no_mutants)
            elif part == "replay":
                doc = gate.part_replay(machine, args.results)
            elif part == "daemon":
                doc = gate.part_daemon(machine, args.results, SPEC, workers=args.workers, heavy=args.heavy,
                                       limit=args.limit, progress=say)
            else:
                doc = gate.part_short(args.machine, machine, args.results, REPO / "runs" / "integration-gate")
        except gate.GateError as exc:
            say(f"{part}: refused — {exc}")
            ok = False
            continue
        say((pathlib.Path(args.results) / f"{part}.log").read_text().rstrip()[-4000:])
        say(f"{part}: {'passed' if doc['passed'] else 'FAILED'} in {time.time() - t0:.0f} s → "
            f"{pathlib.Path(args.results) / (part + '.json')}")
        ok &= doc["passed"]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
