#!/usr/bin/env bash
# The RQ0 run's programs (the 11.3 spec, decisions 2, 4 and 11): the harness and the simulator's source at the RQ0
# run's commit, 6086e7e1 (docs/rq0-run-record.md), extracted beside this script into as-run/, and the simulator
# built there with its Makefile's flags. The harness there is the one the run scored with — the scorer before
# 11.1's sign rule; the simulator builds to simulator@0d323c84470a, the version before stage AF.
#
#     bash as_run.sh        (from the repository root)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
rm -rf "$here/as-run"
mkdir -p "$here/as-run"
git archive 6086e7e1 harness simulator/src/sim.cpp simulator/src/mini_json.hpp simulator/src/Makefile \
  | tar -x -C "$here/as-run"
make -s -C "$here/as-run/simulator/src" sim
v="$(make -s -C "$here/as-run/simulator/src" version)"
echo "$v"
test "$v" = "simulator@0d323c84470a"
