#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|full> — one campaign run (9.5 method §1–§4).
# Installs the application (appdefs.sh), starts Xvfb, launches, waits for the
# window, then runs the phases with `perf sched record -a` over each whole
# phase: interactive apps — settle, idle, driven (stream or scripted pointer),
# and for an application with a heavy operation (appdefs OP) an `op` phase in
# which ops_driver.py triggers it repeatedly and logs ops.jsonl (spec decisions
# 7–10); playback and webrtc — settle, play. Everything lands in $MEAS_OUT.
# Single-core (pin.sh; 9.5 follow-ups spec decisions 2 and 5): this script and
# everything it starts — Xvfb, perf, the replay driver, snapshots — run on the
# harness CPUs; only the application tree is launched on the measured CPU.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
PROBE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../probe" && pwd)"
source "$PROBE_DIR/common.sh"
source "$TOOLS/../pin.sh"
pin_self_harness
source "$TOOLS/appdefs.sh"
APP="$1"; REPEAT="$2"; MODE="${3:-full}"
STREAMS="$(cd "$TOOLS/../../.." && pwd)/meas/streams"
if [ "$MODE" = dry ]; then SETTLE=10; IDLE=30; DRIVEN=60; PLAY=60; OPS=90; else SETTLE=30; IDLE=120; DRIVEN=600; PLAY=300; OPS=600; fi
rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec settle_s "$SETTLE"; rec idle_s "$IDLE"; rec driven_s "$DRIVEN"; rec play_s "$PLAY"; rec op_s "$OPS"
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$TOOLS/../runner_spec.py" > "$OUT/spec.json"
sudo apt-get update > /dev/null 2>&1
apt_install xdotool imagemagick x11-apps python3-xlib dbus-x11
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
start_xvfb
appdef "$APP" || exit 0
rec launch "$LAUNCH"; rec driver "$DRIVER"; rec stream "${STREAM:-}"; rec op "${OP:-}"
PH="$TOOLS/../phase.sh $OUT/phases.jsonl"
export MEAS_PIN=harness   # phase.sh here wraps drivers, which stimulate the pinned application from the harness CPUs
pin_load setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 &
APP_PID=$!
rec app.affinity "$(taskset -p "$APP_PID" 2>/dev/null | sed 's/.*: //' || echo unknown)"
WID=$(wait_window "$CLASS" 120)
if [ -z "$WID" ]; then screenshot no-window; rec finished_utc "$(date -u +%FT%TZ)"; finish_report; exit 0; fi
if [ -n "$POSTLAUNCH" ]; then
  xdotool windowactivate --sync "$WID"; bash -c "$POSTLAUNCH" > "$OUT/postlaunch.log" 2>&1
  W2=$(wait_window "$POSTCLASS" 30); rec postlaunch.window "$W2"
  if [ -n "$W2" ]; then WID="$W2"; fi
  screenshot after-postlaunch
fi
rec area "$AREA"
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
  sudo perf sched timehist -w -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | grep -E "awakened|wakeup|\bwaker\b|^\s*[0-9]+\.[0-9]+ +\[[0-9]+\] +\S.*\[[0-9/]+\] +awakened" | gzip > "$OUT/perf.$name.wakeups.txt.gz"
  rec "perf.$name.wakeups.rows" "$(gzip -dc "$OUT/perf.$name.wakeups.txt.gz" | wc -l)"
  python3 - "$OUT/snap.$name.before.json" "$OUT/snap.$name.after.json" "$name" <<'PY' | tee -a "$KV" | sed 's/^/  /' >&2
import json, sys
a, b, ph = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
dt = b["t_mono"] - a["t_mono"]
print(f"{ph}.wall_s={dt:.2f}"); print(f"{ph}.n_procs={b['n_procs']}"); print(f"{ph}.n_threads={b['n_threads']}")
print(f"{ph}.cpu_s={b['cpu_s']-a['cpu_s']:.3f}"); print(f"{ph}.cpu_share={(b['cpu_s']-a['cpu_s'])/dt if dt else 0:.4f}")
print(f"{ph}.switches_per_s={(b['vol_switches']-a['vol_switches']+b['nonvol_switches']-a['nonvol_switches'])/dt if dt else 0:.1f}")
PY
  if [ "$MODE" = dry ]; then gzip -f "$OUT/perf.$name.data"; else rm -f "$OUT/perf.$name.data"; fi
}

case "$DRIVER" in
  stream)
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    sleep 10
    SFILE="$STREAMS/$STREAM-r$REPEAT.jsonl"; rec stream_file "$(basename "$SFILE")"
    DRV="python3 $TOOLS/replay_stream.py $SFILE $WID $OUT/replay.jsonl --seconds $DRIVEN --area $AREA"
    $PH driven -- bash -c "true"; phase driven "$((DRIVEN + 5))" "$DRV"
    rec replay.sent "$(wc -l < "$OUT/replay.jsonl" 2>/dev/null || echo 0)"
    # driven-alt (spec decision 11): the same phase under the 136M Keystrokes stream, for the stimulus-sensitivity check
    AFILE="$STREAMS/aalto-r$REPEAT.jsonl"
    if [ -f "$AFILE" ]; then
      sleep 10; rec stream_alt_file "$(basename "$AFILE")"
      DRVA="python3 $TOOLS/replay_stream.py $AFILE $WID $OUT/replay-alt.jsonl --seconds $DRIVEN --area $AREA"
      $PH driven-alt -- bash -c "true"; phase driven-alt "$((DRIVEN + 5))" "$DRVA"
      rec replay_alt.sent "$(wc -l < "$OUT/replay-alt.jsonl" 2>/dev/null || echo 0)"
    fi ;;
  pointer)
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    sleep 10
    DRV="xdotool windowactivate --sync $WID; end=\$((\$(date +%s)+$DRIVEN)); while [ \$(date +%s) -lt \$end ]; do xdotool mousemove 300 300 mousedown 1 mousemove --sync 500 400 mousemove --sync 700 350 mouseup 1; sleep 0.8; xdotool mousemove 640 400 click 1; sleep 1.2; xdotool mousemove 400 500 click --repeat 3 --delay 100 4; sleep 1.0; xdotool mousemove 520 380 click --repeat 2 --delay 100 5; sleep 1.5; done"
    $PH driven -- bash -c "true"; phase driven "$((DRIVEN + 5))" "$DRV" ;;
  none)
    phase play "$PLAY" "" ;;
esac
if [ -n "$OP" ]; then
  # op: the operation triggered repeatedly with 10 s pauses; window and duration per operation in ops.jsonl
  sleep 10
  $PH op -- bash -c "true"; phase op "$((OPS + 5))" "$(op_driver "$WID" "$OPS")"
  rec ops.count "$(wc -l < "$OUT/ops.jsonl" 2>/dev/null || echo 0)"
  rec ops.rc0 "$(grep -c '"rc": 0' "$OUT/ops.jsonl" 2>/dev/null || echo 0)"
fi
rec window.name_after "$(xdotool getwindowname "$WID" 2>/dev/null | tr -d '\n' | head -c 120)"
kill -- "-$APP_PID" 2>/dev/null; sleep 2; kill -9 -- "-$APP_PID" 2>/dev/null; appdef_cleanup; kill "$(cat "$OUT/xvfb.pid")" 2>/dev/null
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
