#!/usr/bin/env python3
"""Driver table linter CLI.

Usage: lint.py [TABLE.yaml ...]
  With no arguments, lints every *.yaml under daemon/driver-table/ (none is
  not an error — the tables land in a later phase).
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from drivertable.lint import lint_table  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
TABLE_DIR = HERE.parent / "driver-table"
SCHEMA = TABLE_DIR / "schema" / "driver-table.schema.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tables", nargs="*", type=pathlib.Path)
    args = parser.parse_args()
    tables = args.tables or sorted(TABLE_DIR.glob("*.yaml"))
    if not tables:
        print("no driver tables present (daemon/driver-table/*.yaml); nothing to lint")
        return 0
    errors = []
    for table in tables:
        errors.extend(lint_table(table, SCHEMA))
    if errors:
        print(f"{len(errors)} error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    print(f"lint clean ({len(tables)} table(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
