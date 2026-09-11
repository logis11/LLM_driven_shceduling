#!/usr/bin/env python3
"""records: one (run file, trace) pair -> one records CSV.

    records.py --run RUN.json --trace TRACE.jsonl[.gz] --out RECORDS.csv
               [--schedule CONFIG-SCHEDULE.json] [--table prior|calibrated] [--seed N]

The config schedule is the third input (metrics doc §3): without it a switch
into MLFQ has no params to size its window from, and a guard says so.

Guard messages go to stderr; the file is written regardless, and the exit
code is 2 when any guard fired."""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from harness.records import build, write_csv  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True)
    ap.add_argument("--trace", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--schedule", default=None, help="the daemon's config schedule for this run")
    ap.add_argument("--table", default="", choices=["", "prior", "calibrated"])
    ap.add_argument("--seed", default="")
    ap.add_argument("--boot-default", default="", dest="boot_default",
                    help="id of the boot configuration the run started in; empty = the primary")
    args = ap.parse_args()
    rows, guards = build(args.run, args.trace, table=args.table, seed=args.seed,
                         schedule_path=args.schedule, boot_default=args.boot_default)
    write_csv(rows, args.out)
    for g in guards:
        print(f"guard: {g}", file=sys.stderr)
    print(f"wrote {len(rows)} rows to {args.out}")
    return 2 if guards else 0


if __name__ == "__main__":
    sys.exit(main())
