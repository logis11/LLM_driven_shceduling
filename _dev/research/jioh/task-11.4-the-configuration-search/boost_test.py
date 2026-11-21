#!/usr/bin/env python3
"""The evidence behind the search spec's `checks.restarted_boost` (decided by 인지오 2026-11-21): on two judging
files outside the search whose oracle applies its row again at 2 s, c1-compile and c1-ml-train, the boot default
applied where the oracle applies its row — the corrected oracle run's schedule with each `unmodified` entry's
configuration replaced by the boot default's — run on the pinned simulator and read line by line against the
corrected fixed run's trace, the header and the config lines set aside (the search's `compare_lines`), with and
without the `x_mlfq_boost` line at each re-applied entry's instant.

    python3 boost_test.py       (from the repository root; writes boost-test.json beside this script)
"""
import json
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "harness" / "tools"))
from harness import runner, search  # noqa: E402

FILES = {"c1-compile": "runs/rq0-gate-rerun", "c1-ml-train": "runs/rq0-gate-11-3-current"}
ASIDE = ["meta", "config_applied", "x_config_pending"]


def main():
    boot = json.loads((REPO / "harness" / "boot-defaults" / "ostep.json").read_text())
    sim = REPO / "simulator" / "src" / "sim"
    version = subprocess.run(["make", "-s", "-C", str(REPO / "simulator" / "src"), "version"], capture_output=True,
                             text=True).stdout.strip().splitlines()[-1]
    out = {"simulator": version, "files": []}
    for wid, exp in FILES.items():
        sched = json.loads((REPO / exp / wid / "oracle~focus" / "schedule.json").read_text())
        for e in sched["schedule"]:
            if e["provenance"] == "unmodified":
                e["config"] = search.canonical(boot)
        with tempfile.TemporaryDirectory() as tmp:
            tmp = pathlib.Path(tmp)
            (tmp / "schedule.json").write_text(json.dumps(sched, indent=1))
            subprocess.run([str(sim), "--workload", str(REPO / "dataset" / "build" / "coreset-single" /
                                                         f"{wid}.workload.json"),
                            "--schedule", str(tmp / "schedule.json"), "--out-trace", str(tmp / "trace.jsonl")],
                           check=True, stderr=subprocess.DEVNULL)
            runner.gzip_file(tmp / "trace.jsonl", tmp / "trace.jsonl.gz")
            ref = REPO / exp / wid / "fixed~focus" / "trace.jsonl.gz"
            boosts = search.applied_after_boot(tmp / "trace.jsonl.gz")
            out["files"].append({"workload_id": wid, "reference": f"{exp}/{wid}/fixed~focus",
                                 "re_applied_at": boosts,
                                 "strict": search.compare_lines(tmp / "trace.jsonl.gz", ref, ASIDE),
                                 "restarted_boost_set_aside": search.compare_lines(tmp / "trace.jsonl.gz", ref, ASIDE,
                                                                                   boosts)})
    (pathlib.Path(__file__).parent / "boost-test.json").write_text(json.dumps(out, indent=1) + "\n")
    for f in out["files"]:
        s, b = f["strict"], f["restarted_boost_set_aside"]
        print(f"{f['workload_id']}: strict {s['equal']} ({s['lines_point']} / {s['lines_reference']} lines, first "
              f"difference {s['first_difference']}); restarted boost set aside {b['equal']} ({b['lines_point']} lines)")


if __name__ == "__main__":
    main()
