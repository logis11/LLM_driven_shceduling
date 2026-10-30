#!/bin/bash
# sweep.sh OUT SIM — every file at every slice, then the table. Run from the repository root.
set -e
here=$(dirname "$0"); out=$1; sim=$2
for f in c1-meeting c1-media c1-gaming c2-p2a; do
  for sl in 500 700 900 1200 1500 2000 3000 5000 7000 9000 10000 12000 14000 20000 30000 40000 100000; do
    bash "$here/run.sh" "$out" "$sim" "$f" "$sl"
  done
done
python3 "$here/table.py" "$out"
