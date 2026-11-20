#!/usr/bin/env bash
# The campaign's watch (method §2): dataset/tools/meas/loop/watch.py in batch mode over the runs from the launch's
# run number, restarted after each landing, gated indices relaunched at their index as each is read; stops on an event
# that needs a decision — a failed job, a job short without the gate — or when every index 1–COUNT has landed (107 for
# the campaign, 5 for the probe).
#
#     bash watch_loop.sh <the launch's run number> <COUNT>      (from the repository root)
set -uo pipefail
since="$1"; count="$2"
export MEAS_LOOP_SCOPE=jioh/phase-11
loop="dataset/tools/meas/loop"
while true; do
  out="$(python3 "$loop/watch.py" background/mnist --since "$since" --batch 2>&1)"; rc=$?
  printf '%s\n' "$out" | grep -v "^watching runs from"
  if [ "$rc" -ne 0 ]; then echo "WATCH-ERROR rc=$rc"; sleep 60; continue; fi
  if printf '%s\n' "$out" | grep -q "^FAILED\|^SHORT"; then echo "STOP: an event needs a decision"; exit 3; fi
  n="$(python3 - "$since" "$count" <<'PY'
import sys
sys.path.insert(0, "dataset/tools/meas/loop")
import common
since, count = int(sys.argv[1]), int(sys.argv[2])
landed = {j["k"] for r in common.runs("background", since) for j in common.jobs("background", r["databaseId"])
          if j["app"] == "mnist" and j["state"] == "landed"}
print(len(landed & set(range(1, count + 1))))
PY
)"
  echo "$(date +%H:%M) landed $n of $count"
  [ "$n" = "$count" ] && { echo "DONE: $count landed"; exit 0; }
done
