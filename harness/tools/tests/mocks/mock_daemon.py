#!/usr/bin/env python3
"""mock_daemon: the invocation contract's daemon side (data-contracts, contract
10), served by the mock daemon in `daemon.py`.

    mock_daemon.py --workload WORKLOAD.json --condition fixed|oracle|random
                   --driver-table TABLE.yaml --boot-default BOOT.json
                   --out-schedule SCHEDULE.json --out-log LOG.json [--seed N]

Every flag is required; `--seed` exactly when the condition draws (`random`).
Exit 0 after both outputs are written; any other code means neither is to be
read. Nothing on stdout; diagnostics on stderr.
"""

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))        # tools/: the harness package
sys.path.insert(0, str(HERE.parents[1]))        # tests/: the mocks package

from harness.drivertable import DriverTableError, read_driver_table  # noqa: E402
from mocks.daemon import CONDITIONS, MockDaemonError, run, write  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="mock_daemon.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--workload", required=True, help="canonical workload file")
    ap.add_argument("--condition", required=True, choices=CONDITIONS)
    ap.add_argument("--driver-table", required=True, dest="driver_table")
    ap.add_argument("--boot-default", required=True, dest="boot_default")
    ap.add_argument("--out-schedule", required=True, dest="out_schedule")
    ap.add_argument("--out-log", required=True, dest="out_log")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)
    try:
        with open(args.workload, "r", encoding="utf-8") as f:
            doc = json.load(f)
        with open(args.boot_default, "r", encoding="utf-8") as f:
            boot = json.load(f)
        table = read_driver_table(args.driver_table)
        schedule, log = run(doc, args.condition, table, boot, seed=args.seed)
    except (MockDaemonError, DriverTableError, OSError, ValueError, KeyError) as exc:
        print(f"mock_daemon: {exc}", file=sys.stderr)
        return 1
    write(schedule, args.out_schedule)
    write(log, args.out_log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
