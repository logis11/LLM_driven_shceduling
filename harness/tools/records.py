#!/usr/bin/env python3
"""records: one (run file, trace) pair -> one records CSV.

    records.py --run RUN.json --trace TRACE.jsonl[.gz] --out RECORDS.csv
               [--table prior|calibrated] [--seed N]

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
    ap.add_argument("--table", default="", choices=["", "prior", "calibrated"])
    ap.add_argument("--seed", default="")
    args = ap.parse_args()
    rows, guards = build(args.run, args.trace, table=args.table, seed=args.seed)
    write_csv(rows, args.out)
    for g in guards:
        print(f"guard: {g}", file=sys.stderr)
    print(f"wrote {len(rows)} rows to {args.out}")
    return 2 if guards else 0


if __name__ == "__main__":
    sys.exit(main())
