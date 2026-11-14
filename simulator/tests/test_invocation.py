#!/usr/bin/env python3
"""Conformance item (h) of the RQ0 gate spec (harness/experiments/rq0-gate.yaml,
`simulator-conformance`), black-box on the binary: the simulator run through the invocation contract
as the runner invokes it (data-contracts §11, contract 10).

    python3 simulator/tests/test_invocation.py [path/to/sim] [--version STRING]

`--version` is the string the trace header's `sim` must carry; by default `make -C simulator/src
version`, the string the runner's machine configuration names.

(1) Accepted: --workload, --schedule and --out-trace, in any order, write the trace to that file
    and nothing to standard output, exit 0; the same argument line twice writes byte-identical
    traces; the header's `sim` is the version string.
(2) Refused, each with exit 2 and no trace: the positional form `sim W S`; the three flags plus a
    positional argument; an unknown flag; a flag missing; a flag repeated; a flag without its
    value.
(3) Exit 0 only when the trace is written: an --out-trace in a directory that does not exist
    exits non-zero.
"""
import json
import os
import subprocess
import sys
import tempfile

import blackbox as bb

EVENTS = [{"op": "arrive", "t": 0, "id": "a", "name": "a", "program": [{"op": "RUN", "us": 25_000}, {"op": "EXIT"}]},
          {"op": "arrive", "t": 1_000, "id": "b", "name": "b", "depart": 40_000,
           "program": [{"op": "LOOP", "count": "unbounded", "body": [{"op": "WAIT", "channel": "input:b"}, {"op": "RUN", "us": 500}]}]},
          {"op": "wake", "t": 5_000, "channel": "input:b", "target": "b"}]


def files(d):
    w = os.path.join(d, "w.json"); s = os.path.join(d, "s.json")
    with open(w, "w") as f:
        json.dump({"meta": {"id": "invocation"}, "ground_truth": {}, "events": EVENTS}, f)
    with open(s, "w") as f:
        json.dump({"workload_id": "invocation", "condition": "fixed", "schedule": [bb.entry("MLFQ")]}, f)
    return w, s


def call(sim, *args):
    return subprocess.run([sim, *args], capture_output=True, text=True)


def expected_version():
    if "--version" in sys.argv:
        return sys.argv[sys.argv.index("--version") + 1]
    p = subprocess.run(["make", "-s", "--no-print-directory", "-C", os.path.join(bb.ROOT, "simulator", "src"), "version"],
                       capture_output=True, text=True, check=True)
    return p.stdout.strip()


def test_accepted(sim):
    with tempfile.TemporaryDirectory() as d:
        w, s = files(d)
        t1, t2 = os.path.join(d, "t1.jsonl"), os.path.join(d, "t2.jsonl")
        p1 = call(sim, "--workload", w, "--schedule", s, "--out-trace", t1)
        assert p1.returncode == 0, f"exit {p1.returncode}: {p1.stderr.strip()}"
        assert p1.stdout == "", f"{len(p1.stdout)} bytes on standard output"
        p2 = call(sim, "--out-trace", t2, "--schedule", s, "--workload", w)       # the flags in another order
        assert p2.returncode == 0, f"exit {p2.returncode} with the flags reordered: {p2.stderr.strip()}"
        p3 = call(sim, "--workload", w, "--schedule", s, "--out-trace", t1 + ".again")
        a, b = open(t1, "rb").read(), open(t1 + ".again", "rb").read()
        assert p3.returncode == 0 and a == b, "the same argument line wrote two different traces"
        assert open(t2, "rb").read() == a, "the reordered flags wrote another trace"
        head = json.loads(a.splitlines()[0])
        want = expected_version()
        assert head.get("event") == "meta" and head.get("sim") == want, f"header sim {head.get('sim')!r}, not {want!r}"
        return f"{len(a.splitlines())} lines, byte-identical twice, nothing on stdout, sim {head['sim']}"


def test_refused(sim):
    with tempfile.TemporaryDirectory() as d:
        w, s = files(d)
        t = os.path.join(d, "t.jsonl")
        cases = {
            "positional": [w, s],
            "flags plus a positional": ["--workload", w, "--schedule", s, "--out-trace", t, w],
            "unknown flag": ["--workload", w, "--schedule", s, "--out-trace", t, "--seed", "1"],
            "missing --schedule": ["--workload", w, "--out-trace", t],
            "repeated flag": ["--workload", w, "--workload", w, "--out-trace", t],
            "flag without its value": ["--workload", w, "--schedule", s, "--out-trace"],
        }
        wrong = []
        for name, args in cases.items():
            p = call(sim, *args)
            if p.returncode != 2 or os.path.exists(t):
                wrong.append(f"{name}: exit {p.returncode}, trace {'written' if os.path.exists(t) else 'absent'}")
            if os.path.exists(t):
                os.remove(t)
        assert not wrong, "; ".join(wrong)
        return f"{len(cases)} refusals, each exit 2 with no trace"


def test_unwritten(sim):
    with tempfile.TemporaryDirectory() as d:
        w, s = files(d)
        p = call(sim, "--workload", w, "--schedule", s, "--out-trace", os.path.join(d, "absent", "t.jsonl"))
        assert p.returncode != 0, "exit 0 with a trace path that cannot be written"
        return f"exit {p.returncode} when the trace cannot be written"


if __name__ == "__main__":
    argv = [a for i, a in enumerate(sys.argv) if a != "--version" and (i == 0 or sys.argv[i - 1] != "--version")]
    sys.exit(bb.main([("h-accepted", test_accepted), ("h-refused", test_refused), ("h-unwritten", test_unwritten)], argv))
