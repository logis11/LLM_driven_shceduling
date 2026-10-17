#!/usr/bin/env bash
# apps.sh <app> — install, launch under Xvfb, find the window, run an idle
# phase and a driven phase with perf inside each, write $PROBE_OUT/report.json.
# One app per invocation; see the meas-probe workflow matrix.
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
APP="$1"
rec app "$APP"; rec started_utc "$(date -u +%FT%TZ)"
export DEBIAN_FRONTEND=noninteractive

source "$TOOLS/appdefs.sh"
sudo apt-get update > /dev/null 2>&1
apt_install xdotool imagemagick x11-apps python3-xlib dbus-x11
start_xvfb
appdef "$APP" || exit 0
[ "$DRIVER" = stream ] && DRIVER=type

rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"; rec op "${OP:-}"
T_LAUNCH=$(now_us)
setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 &
APP_PID=$!
WID=$(wait_window "$CLASS" 90)
sleep 5; screenshot after-launch
snap "$PAT" "" launch; rec launch.n_procs "$(python3 -c "import json;print(json.load(open('$OUT/snap.launch.json'))['n_procs'])")"

if [ -n "$WID" ]; then
  # idle: no input for 20 s
  probe_phase idle "$PAT" "$RX" 20 ""
  case "$DRIVER" in
    type) probe_phase driven "$PAT" "$RX" 35 "$(type_driver "$WID")" ;;
    pointer) probe_phase driven "$PAT" "$RX" 30 "$(pointer_driver "$WID")" ;;
    none) probe_phase driven "$PAT" "$RX" 20 "" ;;
  esac
  screenshot after-driven
  if [ -n "$OP" ]; then
    # operation probe: two operations, perf inside; ops.jsonl carries rc and duration per operation
    sleep 5
    probe_phase op "$PAT" "$RX" 120 "$(op_driver "$WID" 110 --count 2 --pause 5)"
    screenshot after-op
    rec ops.count "$(wc -l < "$OUT/ops.jsonl" 2>/dev/null || echo 0)"
    rec ops.rc "$(python3 -c "import json,sys; print(' '.join(str(json.loads(l)['rc']) for l in open('$OUT/ops.jsonl')))" 2>/dev/null)"
    rec ops.ms "$(python3 -c "import json,sys; print(' '.join(str(round((json.loads(l)['done_us']-json.loads(l)['trigger_us'])/1000)) for l in open('$OUT/ops.jsonl')))" 2>/dev/null)"
    rec ops.notes "$(python3 -c "import json,sys; print(' | '.join(json.loads(l)['note'] for l in open('$OUT/ops.jsonl')))" 2>/dev/null | head -c 300)"
  fi
  rec window.name_after "$(xdotool getwindowname "$WID" 2>/dev/null | tr -d '\n' | head -c 120)"
  [ -f "$OUT/replay.jsonl" ] && rec replay.sent "$(wc -l < "$OUT/replay.jsonl")"
fi
# never pkill -f: the script's own argv carries the app name (Phase 2 note)
kill -- "-$APP_PID" 2>/dev/null; sleep 2; kill -9 -- "-$APP_PID" 2>/dev/null; appdef_cleanup; kill "$(cat "$OUT/xvfb.pid")" 2>/dev/null
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
