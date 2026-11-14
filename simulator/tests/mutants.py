#!/usr/bin/env python3
"""The mutants of `simulator/src/sim.cpp` that each behavioural unit test must fail on: a simulator
without the behaviour the test asserts (the integration gate's spec, decision 8,
_dev/docs/spec/jioh/task-10.2-integration-gate.md).

    python3 simulator/tests/mutants.py [--only NAME] [--keep DIR] [--json]

Each mutant is one textual replacement in the current source — the line that gives the behaviour,
taken out — compiled with the flags `simulator/src/Makefile` uses, and the test run on it must exit
non-zero. A replacement that no longer matches the source exactly once is an error, not a pass: the
source moved and the mutant has to be restated. Exit 0 when every test fails on its mutant.
`--json` prints one JSON list instead, a row per mutant with the test's output.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")

# (name, test file, what the mutant takes out, [(old, new), ...])
MUTANTS = [
    ("idle-band-off", "test_idle_class.py",
     "the idle band (stage Z) never holds an idle task out: idle_gate() returns at once",
     [("  void idle_gate() {\n    if (!has_idle_) return;\n", "  void idle_gate() {\n    return;\n")]),
    ("chain-no-deadline", "test_edf_chain.py",
     "a WAKE carries no deadline: a woken chain stage is never in EDF's deadline class",
     [("    const i64 dl = deadline(waker);\n", "    const i64 dl = -1;\n")]),
    ("spawn-wake-dropped", "test_spawn_children.py",
     "a WAKE naming a spawn-table entry not yet born is dropped, not held for its birth (stage W)",
     [("      if (live < 0) { spawn_mail_[slot].push_back(deadline(waker)); return; }",
       "      if (live < 0) { return; }")]),
    ("children-never-complete", "test_spawn_children.py",
     "the last child's task_end does not complete the orchestrator's WAIT children:<id> (stage AA)",
     [("    else if (p.blocked_by == 'c' && p.live_children == 0) on_unblock(t.parent);   // (g)\n", "")]),
    ("children-always-block", "test_spawn_children.py",
     "a WAIT children:<id> reached with no child live blocks instead of completing at once (stage AA)",
     [("            if (t.live_children == 0) { t.chain_dl = -1; ++t.pc;   // none live → zero-wait line\n",
       "            if (false) { t.chain_dl = -1; ++t.pc;   // none live → zero-wait line\n")]),
]


def build(name, out_dir, cxx=None):
    """Write the mutant's source into out_dir and compile it; return the binary's path."""
    m = next(m for m in MUTANTS if m[0] == name)
    with open(os.path.join(SRC, "sim.cpp")) as f:
        text = f.read()
    for old, new in m[3]:
        n = text.count(old)
        if n != 1:
            raise RuntimeError(f"mutant {name}: its replacement matches the source {n} times, not once — restate it")
        text = text.replace(old, new)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copy(os.path.join(SRC, "mini_json.hpp"), out_dir)
    with open(os.path.join(out_dir, "sim.cpp"), "w") as f:
        f.write(text)
    binary = os.path.join(out_dir, "sim")
    cmd = [cxx or os.environ.get("CXX", "g++"), "-std=c++17", "-O2", "-Wall", "-Wextra",   # src/Makefile's
           f'-DSIM_VERSION="mutant@{name}"', "-o", binary, os.path.join(out_dir, "sim.cpp")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"mutant {name} does not compile: {p.stderr.strip()[-400:]}")
    return binary


def run(name, out_dir):
    """(failed as it must, the test's output) for one mutant."""
    m = next(m for m in MUTANTS if m[0] == name)
    binary = build(name, out_dir)
    p = subprocess.run([sys.executable, os.path.join(HERE, m[1]), binary], capture_output=True, text=True,
                       timeout=600)
    return p.returncode != 0, (p.stdout + p.stderr).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--keep", help="build the mutants here and keep them")
    ap.add_argument("--json", action="store_true", help="one JSON list on stdout, a row per mutant")
    a = ap.parse_args()
    ok, rows = True, []
    base = a.keep or tempfile.mkdtemp(prefix="sim-mutants-")
    try:
        for name, test, what, _ in MUTANTS:
            if a.only and name not in a.only:
                continue
            try:
                failed, out = run(name, os.path.join(base, name))
            except RuntimeError as e:
                failed, out = False, f"ERROR — {e}"
            ok &= failed
            rows.append({"mutant": name, "test": test, "takes_out": what, "test_failed": failed, "output": out})
            if not a.json:
                print(f"{name:24} {test:24} {'fails as it must' if failed else 'DOES NOT FAIL — the test cannot see the change'}"
                      f" ({what})")
                for line in out.splitlines():
                    print("    " + line)
    finally:
        if not a.keep:
            shutil.rmtree(base, ignore_errors=True)
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
