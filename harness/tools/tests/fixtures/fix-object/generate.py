#!/usr/bin/env python3
"""Regenerate fix-object/workload.json and fix-tree/workload.json from the dataset's own job
builders (compiler._object_job / _tree_job, seed 1), and each reference-trace.jsonl from the
reference simulator. Run from anywhere: python3 generate.py [path/to/sim]."""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
FIXTURES = HERE.parent
REPO = FIXTURES.parents[3]
sys.path.insert(0, str(REPO / "dataset" / "tools"))
from wlc import compiler  # noqa: E402
from wlc.library import Library  # noqa: E402

SEED = 1


def doc(wid, table, jobs, cap):
    prog = []
    for n in jobs:   # one dispatch RUN per job, then its members forked together (9.6 D19)
        prog.append({"op": "RUN", "us": 500})
        prog += [{"op": "FORK"} for _ in range(n)]
    prog.append({"op": "EXIT"})   # not WAIT children:<id> — that is conformance (g)
    return {"meta": {"id": wid}, "ground_truth": {},
            "events": [{"op": "arrive", "t": 0, "id": "build", "name": "make",
                        "program": prog, "spawn_table": table, "fork_cap": cap}]}


def main():
    sim = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "simulator" / "src" / "sim"
    lib = Library(REPO / "dataset" / "archetypes.yaml")
    docs = {}

    cc = lib.entry("compiler-child")
    tab, jobs = [], []
    for i in range(2):
        e, _ = compiler._object_job("build", i, cc, SEED, "cc1")
        tab += e
        jobs.append(len(e))
    docs["fix-object"] = doc("fix-object", tab, jobs, 8)

    mc = lib.entry("module-compiler-child")
    pat = mc["pattern"]
    names = dict(pat.get("names") or {})
    tab, jobs = [], []
    for i, kind in enumerate(["conftest_a", "conftest_b"]):
        e, _ = compiler._tree_job("build", i, kind, pat["trees"][kind], mc["params"], SEED,
                                  names, mc["declared_class"])
        tab += e
        jobs.append(len(e))
    docs["fix-tree"] = doc("fix-tree", tab, jobs, 12)

    for wid, d in docs.items():
        w = FIXTURES / wid / "workload.json"
        w.write_text(json.dumps(d, indent=1))
        with open(FIXTURES / wid / "reference-trace.jsonl", "wb") as out:
            subprocess.run([str(sim), str(w)], stdout=out, check=True)
        print(wid, "written")


if __name__ == "__main__":
    main()
