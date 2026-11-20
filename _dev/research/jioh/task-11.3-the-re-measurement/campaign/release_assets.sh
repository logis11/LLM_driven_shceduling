#!/usr/bin/env bash
# The campaign's release assets (method §2, Release): one zip per landed job as the loop downloaded it — the 107
# repeats (runs #229–#286), the stop's two (#199) and the probe's two (#209–#228), each named
# meas-background-<app>-r<k>-<mode>-<run id>.zip, the pool's own cache (pool-cache/) left out — and gated-reports.zip,
# the report of every job the machine gate stopped in runs #199–#286.
#
#     bash release_assets.sh <out dir>      (from the repository root; downloads under $MEAS_LOOP_WORK, default
#                                             ~/.cache/meas-loop)
set -euo pipefail
out="$1"; mkdir -p "$out"
work="${MEAS_LOOP_WORK:-$HOME/.cache/meas-loop}"
for d in "$work"/pool/background-mnist-from229/*/meas-background-mnist-r*-full \
         "$work"/pool/background-mnist-from199/44723839046/meas-background-mnist-r*-full \
         "$work"/pool/background-mnist-from209/*/meas-background-mnist-r*-probe; do
  run="$(basename "$(dirname "$d")")"; name="$(basename "$d")-$run.zip"
  [ -f "$out/$name" ] || (cd "$d" && zip -q -r -X "$out/$name" . -x 'pool-cache/*')
done
runs="$(python3 -c "
import json
ids=set()
for f in ('stop-2026-11-20','probe-2026-11-20','results'):
    p='_dev/research/jioh/task-11.3-the-re-measurement/campaign/'+f+'/draws.json'
    ids |= {str(r['id']) for r in json.load(open(p))['runs']}
print(' '.join(sorted(ids)))")"
rm -f "$out/gated-reports.zip"
(cd "$work/gate" && for r in $runs; do [ -d "$r" ] && find "$r" -name report.json; done | zip -q -X "$out/gated-reports.zip" -@)
ls "$out" | wc -l
du -sh "$out"
