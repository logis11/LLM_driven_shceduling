#!/usr/bin/env python3
"""Lint: every fixture pair under tools/tests/fixtures parses under the frozen
contracts — the trace through the trace reader, the run file through the
run-file reader. Exit 1 on the first refusal."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.reader import RunFileError, TraceError, read_run_file, read_trace  # noqa: E402

FIXTURES = pathlib.Path(__file__).resolve().parent / "tests" / "fixtures"


def main():
    pairs = sorted(p for p in FIXTURES.iterdir() if (p / "trace.jsonl").exists())
    if not pairs:
        print("nothing to lint")
        return 0
    failed = 0
    for d in pairs:
        try:
            run = read_run_file(d / "run.json")
            trace = read_trace(d / "trace.jsonl")
            n = sum(1 for _ in trace)
            print(f"  {d.name}: {n} events, T_end {run.t_end}, "
                  f"{len(run.chains)} chain(s)")
        except (TraceError, RunFileError, OSError) as exc:
            failed += 1
            print(f"  {d.name}: {exc}")
    print("lint clean" if not failed else f"{failed} fixture(s) refused")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
