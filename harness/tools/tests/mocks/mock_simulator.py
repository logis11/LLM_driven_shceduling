#!/usr/bin/env python3
"""mock_simulator: the invocation contract's simulator side (data-contracts,
contract 10), served by the mock simulator in `simulator.py`.

    mock_simulator.py [--replay TRACE.jsonl] --workload WORKLOAD.json
                      --schedule SCHEDULE.json --out-trace TRACE.jsonl[.gz]

The three contract flags are required. `--replay` is the mock's own option,
placed in the runner's command prefix for a replay run: the named fixture
trace is copied to the output after its workload id is checked against the
workload's. Exit 0 after the trace is written; any other code means it is not
to be read. Nothing on stdout; diagnostics on stderr.
"""

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2]))        # tools/: the harness package
sys.path.insert(0, str(HERE.parents[1]))        # tests/: the mocks package

from mocks.simulator import MockSimulatorError, generate  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="mock_simulator.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--replay", default=None, help="mock-only: the fixture trace to copy")
    ap.add_argument("--workload", required=True, help="canonical workload file")
    ap.add_argument("--schedule", required=True, help="config schedule from the daemon")
    ap.add_argument("--out-trace", required=True, dest="out_trace")
    args = ap.parse_args(argv)
    try:
        generate(args.workload, args.schedule, args.out_trace, replay=args.replay)
    except (MockSimulatorError, OSError) as exc:
        print(f"mock_simulator: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
