#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|full|probe> — one campaign run (9.5 method §1–§4), or a long-phase probe (probe: the
# 30 s settle, then one idle or play phase of $MEAS_PHASE_S seconds and nothing after it; 9.5 D35, D42).
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
# D34, D35: the idle or play phase starts after the application's launch work — a settle per application, set from its
# traces and stated in method §9 before its repeats; 30 s (method §2) where the traces show none. An application whose
# launch work reaches past 30 s (chrome, code, webrtc, thunderbird, thunderbird-send) has no entry until its settle is
# stated, and stops before any measurement.
settle_for() {
  case "$1" in
    soffice|gimp|kdenlive|mpv-video|mpv-audio) echo 30 ;;
    *) echo "" ;;
  esac
}
if [ "$MODE" = dry ]; then SETTLE=10; IDLE=30; DRIVEN=60; PLAY=60; OPS=90
elif [ "$MODE" = probe ]; then SETTLE=30; IDLE="${MEAS_PHASE_S:?probe needs MEAS_PHASE_S}"; DRIVEN=0; PLAY="$IDLE"; OPS=0
else SETTLE="$(settle_for "$APP")"; IDLE=120; DRIVEN=600; PLAY=300; OPS=600; fi
rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec settle_s "${SETTLE:-unset}"; rec idle_s "$IDLE"; rec driven_s "$DRIVEN"; rec play_s "$PLAY"; rec op_s "$OPS"
if [ -z "$SETTLE" ]; then
  rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "settle: no settle stated for $APP (D34, D35) — stopping before any measurement" >&2
  exit 0
fi
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$TOOLS/../runner_spec.py" > "$OUT/spec.json"
# same-machine repeats (9.6 D10; 9.5 D26): a job that drew another CPU model stops here, recorded, before any install or measurement
source "$TOOLS/../machine_gate.sh"
rec machine.model "$(machine_model)"; rec machine.wanted "${MEAS_CPU_MODEL:-}"
if ! machine_gate "${MEAS_CPU_MODEL:-}"; then
  rec gate wrong-machine; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "machine gate: wanted '${MEAS_CPU_MODEL}', drew '$(machine_model)' — stopping before any measurement" >&2
  exit 0
fi
rec gate open
sudo apt-get update > /dev/null 2>&1
apt_install xdotool imagemagick x11-apps python3-xlib dbus-x11
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
start_xvfb
appdef "$APP" || exit 0
rec launch "$LAUNCH"; rec driver "$DRIVER"; rec stream "${STREAM:-}"; rec op "${OP:-}"; rec rx "$RX"; rec pat "$PAT"
PH="$TOOLS/../phase.sh $OUT/phases.jsonl"
export MEAS_PIN=harness   # phase.sh here wraps drivers, which stimulate the pinned application from the harness CPUs
# launched directly under taskset (not through the pin_load function: a function run in the background forks a
# subshell, so $! would be the subshell, not the session leader the kill and the affinity record need)
if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_CPU" setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 & else setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 & fi
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
  pin_harness sudo perf sched record -k CLOCK_MONOTONIC -a -o "$OUT/perf.$name.data" -- sleep "$secs" > "$OUT/perf.$name.log" 2>&1 &
  local perf_pid=$!
  sleep 1
  if [ -n "$driver" ]; then
    $PH "$name-driver" -- bash -c "$driver" > "$OUT/driver.$name.log" 2>&1
  fi
  wait "$perf_pid"; rec "perf.$name.record.rc" "$?"
  snap "$PAT" "" "$name.after"
  screenshot "after-$name"
  # --state: each row's switch-out state, the cross-check of the wakeup-row wake (9.5 D39)
  sudo perf sched timehist --state -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
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
    # D32: a repeat past the recording's end — its window recorded empty in windows.json (an empty window is not
    # committed) — runs the idle phase alone and is pooled into the idle values only; no operation phase either,
    # since without the driven phases it would start from another application state
    WINDOW="$(python3 -c 'import json, sys; w = json.load(open(sys.argv[1]))["windows"].get(sys.argv[2]); print("uncut" if w is None else "ok" if w.get("events") else "empty")' "$STREAMS/windows.json" "$STREAM-r$REPEAT")"
    rec recording.window "$WINDOW"
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    if [ "$MODE" = probe ]; then OP=""
    elif [ "$WINDOW" = empty ]; then rec recording.past_end 1; OP=""; else
    sleep 10
    SFILE="$STREAMS/$STREAM-r$REPEAT.jsonl"; rec stream_file "$(basename "$SFILE")"; rec stream_kinds "$KINDS"
    DRV="python3 $TOOLS/replay_stream.py $SFILE $WID $OUT/replay.jsonl --seconds $DRIVEN --area $AREA --kinds $KINDS"
    $PH driven -- bash -c "true"; phase driven "$((DRIVEN + 5))" "$DRV"
    rec replay.sent "$(wc -l < "$OUT/replay.jsonl" 2>/dev/null || echo 0)"
    # driven-alt (spec decision 11): the same phase under the 136M Keystrokes stream, for the stimulus-sensitivity check
    AFILE="$STREAMS/aalto-r$REPEAT.jsonl"
    if [ -f "$AFILE" ]; then
      sleep 10; rec stream_alt_file "$(basename "$AFILE")"
      if [ -n "$ALTPRELUDE" ]; then xdotool windowactivate --sync "$WID"; bash -c "$ALTPRELUDE" > "$OUT/altprelude.log" 2>&1; screenshot after-altprelude; sleep 5; fi
      DRVA="python3 $TOOLS/replay_stream.py $AFILE $WID $OUT/replay-alt.jsonl --seconds $DRIVEN --area $AREA"
      $PH driven-alt -- bash -c "true"; phase driven-alt "$((DRIVEN + 5))" "$DRVA"
      rec replay_alt.sent "$(wc -l < "$OUT/replay-alt.jsonl" 2>/dev/null || echo 0)"
    fi
    fi ;;
  pointer)
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    if [ "$MODE" = probe ]; then OP=""; else
    sleep 10
    DRV="xdotool windowactivate --sync $WID; end=\$((\$(date +%s)+$DRIVEN)); while [ \$(date +%s) -lt \$end ]; do xdotool mousemove 300 300 mousedown 1 mousemove --sync 500 400 mousemove --sync 700 350 mouseup 1; sleep 0.8; xdotool mousemove 640 400 click 1; sleep 1.2; xdotool mousemove 400 500 click --repeat 3 --delay 100 4; sleep 1.0; xdotool mousemove 520 380 click --repeat 2 --delay 100 5; sleep 1.5; done"
    $PH driven -- bash -c "true"; phase driven "$((DRIVEN + 5))" "$DRV"
    fi ;;
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
