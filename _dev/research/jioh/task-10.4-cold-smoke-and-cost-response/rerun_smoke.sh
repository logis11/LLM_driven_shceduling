#!/bin/bash
# 10.4 decision 14: the smoke rerun, its traces served from the execution cache the cold smoke left — the RQ0 gate
# spec's run list at seed count 2 (1,197 runs), the machine configuration's workers. Run from the repository root,
# through the tunnel; it runs unattended:
#
#     nohup bash _dev/research/jioh/task-10.4-cold-smoke-and-cost-response/rerun_smoke.sh &
#
# Writes rerun/start.json (date, commit, versions, free space) beside this file, the run under runs/smoke-rerun/, and
# its log to runs/smoke-rerun.log; rerun/exit.json at the end.
set -u
HERE=_dev/research/jioh/task-10.4-cold-smoke-and-cost-response
if [ -e runs/smoke-rerun ]; then
  echo "runs/smoke-rerun exists" >&2; exit 1
fi
if [ ! -d runs/.cache ]; then
  echo "runs/.cache is absent: the rerun serves the cold smoke's traces from it" >&2; exit 1
fi
mkdir -p "$HERE/rerun"
FREE_KB=$(df -k . | tail -1 | awk '{print $4}')
python3 - "$FREE_KB" > "$HERE/rerun/start.json" <<'PY'
import json, subprocess, sys, time, yaml
m = yaml.safe_load(open("harness/runner.yaml"))
print(json.dumps({"started": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                  "commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
                  "dirty": bool(subprocess.run(["git", "status", "--porcelain", "harness/tools"], capture_output=True, text=True).stdout.strip()),
                  "simulator": m["simulator"]["version"], "daemon": m["daemon"]["version"],
                  "workers": m.get("workers", 1), "heavy_workers": m.get("heavy_workers", 1), "heavy_mb": m.get("heavy_mb", 50),
                  "free_gb": round(int(sys.argv[1]) * 1024 / 1e9, 1)}, indent=1))
PY
cat "$HERE/rerun/start.json"
python3 harness/tools/run.py --spec harness/experiments/rq0-gate.yaml --machine harness/runner.yaml \
  --seed-count 2 --experiment smoke-rerun > runs/smoke-rerun.log 2>&1
CODE=$?
printf '{"ended": "%s", "exit": %d}\n' "$(date +%Y-%m-%dT%H:%M:%S%z)" "$CODE" > "$HERE/rerun/exit.json"
cat "$HERE/rerun/exit.json"
