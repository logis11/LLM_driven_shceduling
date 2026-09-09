#!/usr/bin/env python3
"""Lint: every fixture pair under tools/tests/fixtures parses under the frozen
contracts — the trace through the trace reader, the run file through the
run-file reader, the config schedule (when the fixture has one) through the
schedule reader — and its expected records validate against the records
schema. Exit 1 on the first refusal."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.reader import (RunFileError, ScheduleError, TraceError,  # noqa: E402
                            read_config_schedule, read_run_file, read_trace)
from harness.records import read_csv, validate_rows  # noqa: E402

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
            sched = ""
            if (d / "config-schedule.json").exists():
                sched = f", {len(read_config_schedule(d / 'config-schedule.json').entries)} schedule entries"
            rows = read_csv(d / "expected.csv")
            validate_rows(rows)
            print(f"  {d.name}: {n} events, T_end {run.t_end}, "
                  f"{len(run.chains)} chain(s){sched}, {len(rows)} expected rows valid")
        except (TraceError, RunFileError, ScheduleError, ValueError, OSError) as exc:
            failed += 1
            print(f"  {d.name}: {exc}")
    print("lint clean" if not failed else f"{failed} fixture(s) refused")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
