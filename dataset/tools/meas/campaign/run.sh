#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|full> — one campaign run (9.5 method §1–§4).
# Installs the application (appdefs.sh), starts Xvfb, launches, waits for the
# window, then runs the phases with `perf sched record -a` over each whole
# phase: interactive apps — settle, idle, driven (stream or scripted pointer);
# playback and webrtc — settle, play. Everything lands in $MEAS_OUT.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
PROBE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../probe" && pwd)"
source "$PROBE_DIR/common.sh"
source "$TOOLS/appdefs.sh"
APP="$1"; REPEAT="$2"; MODE="${3:-full}"
STREAMS="$(cd "$TOOLS/../../.." && pwd)/meas/streams"
if [ "$MODE" = dry ]; then SETTLE=10; IDLE=30; DRIVEN=60; PLAY=60; else SETTLE=30; IDLE=120; DRIVEN=600; PLAY=300; fi
rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec settle_s "$SETTLE"; rec idle_s "$IDLE"; rec driven_s "$DRIVEN"; rec play_s "$PLAY"
python3 "$TOOLS/../runner_spec.py" > "$OUT/spec.json"
sudo apt-get update > /dev/null 2>&1
apt_install xdotool imagemagick x11-apps python3-xlib dbus-x11
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
start_xvfb
appdef "$APP" || exit 0
rec launch "$LAUNCH"; rec driver "$DRIVER"; rec stream "${STREAM:-}"
PH="$TOOLS/../phase.sh $OUT/phases.jsonl"
setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 &
APP_PID=$!
WID=$(wait_window "$CLASS" 120)
if [ -z "$WID" ]; then screenshot no-window; rec finished_utc "$(date -u +%FT%TZ)"; finish_report; exit 0; fi
sleep "$SETTLE"; screenshot after-settle
snap "$PAT" "" launch

# phase <name> <seconds> <driver-cmd or ''>: perf over the whole phase, driver inside it
phase() {
  local name="$1" secs="$2" driver="$3"
  snap "$PAT" "" "$name.before"
  sudo perf sched record -k CLOCK_MONOTONIC -a -o "$OUT/perf.$name.data" -- sleep "$secs" > "$OUT/perf.$name.log" 2>&1 &
  local perf_pid=$!
  sleep 1
  if [ -n "$driver" ]; then
    $PH "$name-driver" -- bash -c "$driver" > "$OUT/driver.$name.log" 2>&1
  fi
  wait "$perf_pid"; rec "perf.$name.record.rc" "$?"
  snap "$PAT" "" "$name.after"
  screenshot "after-$name"
  sudo perf sched timehist -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
  rec "perf.$name.timehist.rc" "${PIPESTATUS[0]}"
  rec "perf.$name.rows_matching" "$(gzip -dc "$OUT/perf.$name.timehist.txt.gz" | grep -cE "$RX" || echo 0)"
  python3 - "$OUT/snap.$name.before.json" "$OUT/snap.$name.after.json" "$name" <<'PY' | tee -a "$KV" | sed 's/^/  /' >&2
import json, sys
a, b, ph = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
dt = b["t_mono"] - a["t_mono"]
print(f"{ph}.wall_s={dt:.2f}"); print(f"{ph}.n_procs={b['n_procs']}"); print(f"{ph}.n_threads={b['n_threads']}")
print(f"{ph}.cpu_s={b['cpu_s']-a['cpu_s']:.3f}"); print(f"{ph}.cpu_share={(b['cpu_s']-a['cpu_s'])/dt if dt else 0:.4f}")
print(f"{ph}.switches_per_s={(b['vol_switches']-a['vol_switches']+b['nonvol_switches']-a['nonvol_switches'])/dt if dt else 0:.1f}")
PY
  gzip -f "$OUT/perf.$name.data"
}

case "$DRIVER" in
  stream)
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    sleep 10
    SFILE="$STREAMS/$STREAM-r$REPEAT.jsonl"; rec stream_file "$(basename "$SFILE")"
    DRV="python3 $TOOLS/replay_stream.py $SFILE $WID $OUT/replay.jsonl --seconds $DRIVEN"
    $PH driven -- bash -c "true"; phase driven "$((DRIVEN + 5))" "$DRV"
    rec replay.sent "$(wc -l < "$OUT/replay.jsonl" 2>/dev/null || echo 0)" ;;
  pointer)
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    sleep 10
    DRV="xdotool windowactivate --sync $WID; end=\$((\$(date +%s)+$DRIVEN)); while [ \$(date +%s) -lt \$end ]; do xdotool mousemove 300 300 mousedown 1 mousemove --sync 500 400 mousemove --sync 700 350 mouseup 1; sleep 0.8; xdotool mousemove 640 400 click 1; sleep 1.2; xdotool mousemove 400 500 click --repeat 3 --delay 100 4; sleep 1.0; xdotool mousemove 520 380 click --repeat 2 --delay 100 5; sleep 1.5; done"
    $PH driven -- bash -c "true"; phase driven "$((DRIVEN + 5))" "$DRV" ;;
  none)
    phase play "$PLAY" "" ;;
esac
rec window.name_after "$(xdotool getwindowname "$WID" 2>/dev/null | tr -d '\n' | head -c 120)"
kill -- "-$APP_PID" 2>/dev/null; sleep 2; kill -9 -- "-$APP_PID" 2>/dev/null; kill "$(cat "$OUT/xvfb.pid")" 2>/dev/null
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
