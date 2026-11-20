#!/usr/bin/env bash
# Decisions 11 and 12: the judging files holding cpu-batch's python3 — c2-p1a, c1-ml-train, c7-ml-train — rebuilt on
# the re-measured library (the second bless), each with the criterion's 102 runs at the primary boot default under the
# primary table, beside c2-p1b, the reporting half of c2-p1a's C2 pair that the pair guard reads; one throwaway spec
# copy per program set, its dataset and variants pins on the second bless (spec_copy.py --repin):
#   closing  — the RQ0 run's programs (as_run.sh): simulator@0d323c84470a, the harness of commit 6086e7e1, the
#              scorer as run (decision 11)
#   current  — the fixed programs: simulator@841dc81131cb (simulator/src/sim), the repository's harness, the fixed
#              scorer (decision 12)
# Outputs under runs/rq0-gate-11-3-<name>/.
#
#     bash closing_run.sh [closing] [current]     (from the repository root; default both, the closing first)
set -euo pipefail
here="_dev/research/jioh/task-11.3-the-re-measurement"
judging="c2-p1a,c1-ml-train,c7-ml-train"
names=("$@")
[ ${#names[@]} -gt 0 ] || names=(closing current)
for n in "${names[@]}"; do
  case "$n" in
    closing) harness="$here/as-run/harness"; sim="simulator@0d323c84470a"; cmd="$here/as-run/simulator/src/sim" ;;
    current) harness="harness"; sim="simulator@841dc81131cb"; cmd="simulator/src/sim" ;;
    *) echo "unknown run $n"; exit 2 ;;
  esac
  python3 "$here/spec_copy.py" --experiment "rq0-gate-11-3-$n" --harness "$harness" --simulator "$sim" \
    --sim-command "$cmd" --build-dir dataset/build/coreset-single --judging "$judging" --reporting c2-p1b \
    --repin > /dev/null
  echo "== $n $(date +%T)"
  rc=0   # exit 2 is the copy's verdict (three judging files against K = 10), not read; 1 is a failed run
  python3 "$harness/tools/run.py" --spec "runs/rq0-gate-11-3-$n.spec.yaml" --machine "runs/rq0-gate-11-3-$n.machine.yaml" \
    --root . --quiet || rc=$?
  [ "$rc" -eq 1 ] && { echo "== $n: a run failed"; exit 1; }
  echo "== $n done $(date +%T)"
done
