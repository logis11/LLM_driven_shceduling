#!/usr/bin/env bash
# The finding step's runs (the 11.3 spec, decisions 2 and 4): the criterion's 102 runs of each build on the RQ0
# run's programs (as_run.sh), one throwaway spec copy per build directory of finding_builds.py — the controls
# (`c7-ml-train` with nothing moved, `c7-ml-train@corner-low` with all four moved) first, then each single-value
# build as `c7-ml-train`. Outputs under runs/rq0-gate-finding-<dir>/; read by finding_read.py.
#
#     bash finding_run.sh [DIR…]     (from the repository root; default every directory, the controls first)
set -euo pipefail
here="_dev/research/jioh/task-11.3-the-re-measurement"
dirs=("$@")
[ ${#dirs[@]} -gt 0 ] || dirs=(controls libuv-gap-low libuv-run-low python3-run-low python3-block-low)
for d in "${dirs[@]}"; do
  variants=""
  [ "$d" = controls ] && variants="c7-ml-train@corner-low"
  python3 "$here/spec_copy.py" --experiment "rq0-gate-finding-$d" --harness "$here/as-run/harness" \
    --simulator simulator@0d323c84470a --sim-command "$here/as-run/simulator/src/sim" \
    --build-dir "$here/finding/build/$d" --judging c7-ml-train --variants "$variants" > /dev/null
  echo "== $d $(date +%T)"
  # exit 2 is the copy's verdict (one judging file against K = 10), not read; 1 is a failed run
  rc=0
  python3 "$here/as-run/harness/tools/run.py" --spec "runs/rq0-gate-finding-$d.spec.yaml" \
    --machine "runs/rq0-gate-finding-$d.machine.yaml" --root . --quiet || rc=$?
  [ "$rc" -eq 1 ] && { echo "== $d: a run failed"; exit 1; }
  echo "== $d done $(date +%T)"
done
