#!/usr/bin/env python3
"""Lint: every fixture pair under tools/tests/fixtures parses under the frozen
contracts — the trace through the trace reader, the run file through the
run-file reader, the config schedule (when the fixture has one) through the
schedule reader, any recognition log through the log reader — and its expected
records validate against the records schema; `mock-scores` and `mock-guards`
expected outputs validate against their schemas. Exit 1 on the first refusal."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.reader import (LogError, RunFileError, ScheduleError, TraceError,  # noqa: E402
                            read_config_schedule, read_recognition_log, read_run_file,
                            read_trace)
from harness import aggregates, grader, guards, scorer  # noqa: E402
from harness.grader import GradeError  # noqa: E402
from harness.outputs import AGGREGATES_SCHEMA, GRADES_SCHEMA, SCORES_SCHEMA  # noqa: E402
from harness.outputs import read_csv as read_table  # noqa: E402
from harness.outputs import validate_rows as validate_table  # noqa: E402
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
            logs = ""
            for lg in sorted(d.glob("recognition-log*.json")):
                logs += f", {len(read_recognition_log(lg).queries)} queries in {lg.name}"
            rows = read_csv(d / "expected.csv")
            validate_rows(rows)
            extra = ""
            if (d / "expected-guards.csv").exists():
                g = read_table(d / "expected-guards.csv", guards.COLUMNS)
                validate_table(g, guards.GUARDS_SCHEMA)
                extra = f", {len(g)} expected guard rows valid"
            print(f"  {d.name}: {n} events, T_end {run.t_end}, "
                  f"{len(run.chains)} chain(s){sched}{logs}, {len(rows)} expected rows valid{extra}")
        except (TraceError, RunFileError, ScheduleError, LogError, ValueError, OSError) as exc:
            failed += 1
            print(f"  {d.name}: {exc}")
    ms = FIXTURES / "mock-scores"
    if ms.exists():
        try:
            n_rec = 0
            for f in sorted((ms / "records").glob("*.csv")) + sorted((ms / "seam").glob("*.csv")):
                rows = read_csv(f)
                validate_rows(rows)
                n_rec += len(rows)
            a = read_table(ms / "expected-aggregates.csv", aggregates.COLUMNS)
            validate_table(a, AGGREGATES_SCHEMA)
            sc = read_table(ms / "expected-scores.csv", scorer.COLUMNS)
            validate_table(sc, SCORES_SCHEMA)
            print(f"  mock-scores: {n_rec} records rows valid, {len(a)} expected aggregate rows valid, "
                  f"{len(sc)} expected score rows valid")
        except (ValueError, OSError) as exc:
            failed += 1
            print(f"  mock-scores: {exc}")
    mg = FIXTURES / "mock-grades"
    if mg.exists():
        try:
            table = grader.read_driver_table(mg / "driver-table.yaml")
            n_seg = sum(len(grader.read_ground_truth(w))
                        for w in sorted((mg / "workloads").glob("*.workload.json")))
            n_q = sum(len(read_recognition_log(l).queries)
                      for l in sorted((mg / "logs").glob("*.json")))
            n_rec = 0
            for f in sorted((mg / "expected-records").glob("*.csv")):
                rows = read_csv(f)
                validate_rows(rows)
                n_rec += len(rows)
            gr = read_table(mg / "expected-grades.csv", grader.COLUMNS)
            validate_table(gr, GRADES_SCHEMA)
            print(f"  mock-grades: {len(table.rows)} table rows ({table.role}), {n_seg} segments, "
                  f"{n_q} queries, {n_rec} expected records rows valid, "
                  f"{len(gr)} expected grade rows valid")
        except (LogError, GradeError, ValueError, OSError) as exc:
            failed += 1
            print(f"  mock-grades: {exc}")
    print("lint clean" if not failed else f"{failed} fixture(s) refused")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
