#!/bin/bash
# fixed_check.sh OUT SIM PY — files under fixed at the primary (10 000 µs): c7-meeting's call
# and c7-media's two players, the share of boost intervals holding a demotion and the job miss
# rate by the records (harness/tools/records.py; PY a Python with harness/tools/requirements.txt);
# the editors of c7-office, c7-browsing, c1-mail and c7-dev, their demotions.
# Run from the repository root.
set -e
here=$(dirname "$0"); out=$1; sim=$2; py=$3
for f in c7-meeting c7-media; do
  bash "$here/run.sh" "$out" "$sim" "$f" 10000
  (cd harness/tools && "$py" records.py --run "../../dataset/build/coreset-single/$f.workload.json" \
     --trace "$out/$f.10000.jsonl" --out "$out/$f.10000.records.csv" > /dev/null)
done
for f in c7-office c7-browsing c1-mail c7-dev; do
  bash "$here/run.sh" "$out" "$sim" "$f" 10000
done
"$py" "$here/fixed_check.py" "$out"
