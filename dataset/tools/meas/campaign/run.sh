#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|full|idle|probe|probe-driven> — one campaign run (9.5 method §1–§4; idle: the settle and
# the idle phase alone, 9.10 D146), or a long-phase probe
# (probe: the 30 s settle, then one idle or play phase of $MEAS_PHASE_S seconds and nothing after it; 9.5 D35, D42), or
# a long driven probe (probe-driven: the campaign's settle and idle phase, then $MEAS_WINDOWS driven windows of
# $MEAS_WINDOW_S seconds back to back, each a phase of its own; 9.10 D143, D144).
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
APP="$1"; REPEAT="$2"; MODE_ARG="${3:-full}"
# the untraced control (_dev/docs/spec/jioh/task-9.5-untraced-control.md): `control` runs full's lengths and
# `control-dry` dry's, every carried phase as a traced and an untraced run
CONTROL=0; MODE="$MODE_ARG"
case "$MODE_ARG" in control) CONTROL=1; MODE=full ;; control-dry) CONTROL=1; MODE=dry ;; esac
# its decision 5: the pair's order alternates across jobs — odd jobs run it traced first, even jobs untraced first
if [ $((REPEAT % 2)) -eq 1 ]; then ORDER="traced untraced"; else ORDER="untraced traced"; fi
STREAMS="$(cd "$TOOLS/../../.." && pwd)/meas/streams"
# D34, D35: the idle or play phase starts after the application's launch work — a settle per application, set from its
# traces and stated in method §9 before its repeats; 30 s (method §2) where the traces show none. An application whose
# launch work reaches past 30 s (chrome, code, webrtc, thunderbird) has no entry until its settle is stated, and stops
# before any measurement.
settle_for() {
  case "$1" in
    soffice|gimp|mpv-video|mpv-audio) echo 30 ;;
    kdenlive) echo 240 ;;           # 9.10 D146: its main thread's work after launch ends about 200 s after the window
                                    # (the span probe; 9.5 D34's flat reading was on CPU printed to 0.1 ms/s)
    thunderbird-send) echo 390 ;;   # D44: its launch work ends ~340 s into a 30 s-settled idle phase (long-phase probe)
    chrome) echo 420 ;;             # D58: that run lands 95–300 s after the window over seven sessions (D51's 270 s
                                    # caught it in one repeat of five); the slice profile guards the rest
    code) echo 30 ;;                # D53: at its baseline within 10 s of the phase's start — no launch work to settle past
    webrtc) echo 210 ;;             # D54: its call's dense ramp-up episodes end by 170 s, the 240 s cadence holds after
    *) echo "" ;;
  esac
}
# D45: the idle phase holds the application's recurring episodes (D35) — 600 s for thunderbird-send, whose ~60 s
# StreamTrans episode and slower variation a 120 s window reproduces to within 31 % of the long-run level, a 600 s one
# to within 7.4 % (long-phase probe); 120 s (method §2) elsewhere
idle_for() {
  case "$1" in
    thunderbird-send) echo 600 ;;
    code) echo 900 ;;   # D53: its ~320 s episode is launch-anchored — a 120 s phase reads CPU +15.5 % at the placement
    chrome) echo 600 ;; # every repeat takes, a 900 s one +1.6 % (long-phase probe). D56: past D51's settle chrome's idle
                        # phase is quiet, and a 120 s window reads CPU +13.6 % there, a 600 s one +0.0 %
    kdenlive) echo 180 ;;   # 9.10 D146: past its 240 s settle 120 s reads +6.4 % at the worst placement, 180 s +4.6 %
    *) echo 120 ;;
  esac
}
# D54: the play phase holds whole cycles of a recurring episode — 480 s for webrtc, two of its 240 s saturation
# cycles (a 300 s phase reads CPU +78 % of the long-run level, a 600 s one strays 9.7 % by placement, being two and a
# half cycles); 300 s (method §2) elsewhere
play_for() {
  case "$1" in
    webrtc) echo 480 ;;
    *) echo 300 ;;
  esac
}
if [ "$MODE" = dry ]; then SETTLE=10; IDLE=30; DRIVEN=60; PLAY=60; OPS=90
elif [ "$MODE" = probe ]; then SETTLE=30; IDLE="${MEAS_PHASE_S:?probe needs MEAS_PHASE_S}"; DRIVEN=0; PLAY="$IDLE"; OPS=0
# 9.10 D143, D144: the campaign's own settle and idle phase, so the driven windows open where every repeat's driven
# phase opened; each window as long as a repeat's driven phase (600 s; a dry run shorter)
elif [ "$MODE" = idle ]; then SETTLE="$(settle_for "$APP")"; IDLE="$(idle_for "$APP")"; DRIVEN=0; PLAY=0; OPS=0
elif [ "$MODE" = probe-driven ]; then SETTLE="$(settle_for "$APP")"; IDLE="$(idle_for "$APP")"
  DRIVEN="${MEAS_WINDOW_S:-600}"; WINDOWS="${MEAS_WINDOWS:?probe-driven needs MEAS_WINDOWS}"; PLAY=0; OPS=0
else SETTLE="$(settle_for "$APP")"; IDLE="$(idle_for "$APP")"; DRIVEN=600; PLAY="$(play_for "$APP")"; OPS=600; fi
rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE_ARG"; rec control "$CONTROL"; rec started_utc "$(date -u +%FT%TZ)"
[ "$CONTROL" = 1 ] && rec control.order "$ORDER"
rec settle_s "${SETTLE:-unset}"; rec idle_s "$IDLE"; rec driven_s "$DRIVEN"; rec play_s "$PLAY"; rec op_s "$OPS"
[ "$MODE" = probe-driven ] && rec windows "$WINDOWS"
if [ -z "$SETTLE" ]; then
  rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "settle: no settle stated for $APP (D34, D35) — stopping before any measurement" >&2
  exit 0
fi
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$TOOLS/../runner_spec.py" > "$OUT/spec.json"
# the untraced control's decision 9: the schedstats switch, which neither perf nor this job sets
rec sysctl.sched_schedstats "$(cat /proc/sys/kernel/sched_schedstats 2>/dev/null || echo unknown)"
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
# D69: the build gate — a job whose appdef pins a build and drew another stops here, recorded, before any measurement,
# as the machine gate stops one that drew another CPU model
if ! build_gate; then
  rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "build gate: wanted '${BUILD_WANT}', installed '${APP_VERSION}' — stopping before any measurement" >&2
  exit 0
fi
rec launch "$LAUNCH"; rec driver "$DRIVER"; rec stream "${STREAM:-}"; rec op "${OP:-}"; rec rx "$RX"; rec pat "$PAT"
# the untraced control's decision 4: the prelude before each driven run — the 136M prelude where the appdef has one
CTRLPRELUDE="${CTRLPRELUDE:-$ALTPRELUDE}"
[ "$CONTROL" = 1 ] && rec ctrlprelude "$CTRLPRELUDE"
PH="$TOOLS/../phase.sh $OUT/phases.jsonl"
export MEAS_PIN=harness   # phase.sh here wraps drivers, which stimulate the pinned application from the harness CPUs
# launched directly under taskset (not through the pin_load function: a function run in the background forks a
# subshell, so $! would be the subshell, not the session leader the kill and the affinity record need)
if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_CPU" setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 & else setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 & fi
APP_PID=$!
WID=$(wait_window "$CLASS" 120)
if [ -z "$WID" ]; then screenshot no-window; rec finished_utc "$(date -u +%FT%TZ)"; finish_report; exit 0; fi
# the mask of the process owning the window, read once it exists: read at launch, $APP_PID could still be taskset before
# it applied the mask, and five webrtc repeats recorded the harness CPUs while their trace ran every thread on the load CPU
WIN_PID=$(xdotool getwindowpid "$WID" 2>/dev/null || echo "$APP_PID")
rec app.affinity "$(taskset -p "$WIN_PID" 2>/dev/null | sed 's/.*: //' || echo unknown)"; rec app.affinity_pid "$WIN_PID"
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
  phase_summary "$name"
  if [ "$MODE" = dry ]; then gzip -f "$OUT/perf.$name.data"; else rm -f "$OUT/perf.$name.data"; fi
}

# phase_summary <name>: the tree's CPU and switches over a phase, from its two snapshots, into report.kv
phase_summary() {
  python3 - "$OUT/snap.$1.before.json" "$OUT/snap.$1.after.json" "$1" <<'PY' | tee -a "$KV" | sed 's/^/  /' >&2
import json, sys
a, b, ph = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
dt = b["t_mono"] - a["t_mono"]
print(f"{ph}.wall_s={dt:.2f}"); print(f"{ph}.n_procs={b['n_procs']}"); print(f"{ph}.n_threads={b['n_threads']}")
print(f"{ph}.cpu_s={b['cpu_s']-a['cpu_s']:.3f}"); print(f"{ph}.cpu_share={(b['cpu_s']-a['cpu_s'])/dt if dt else 0:.4f}")
print(f"{ph}.switches_per_s={(b['vol_switches']-a['vol_switches']+b['nonvol_switches']-a['nonvol_switches'])/dt if dt else 0:.1f}")
PY
}

# quiet <name> <seconds> <driver-cmd or ''>: phase()'s untraced twin (the untraced control's decision 1) — the same
# snapshots, driver and length, and no perf
quiet() {
  local name="$1" secs="$2" driver="$3"
  snap "$PAT" "" "$name.before"
  sleep "$secs" &
  local sleep_pid=$!
  sleep 1
  if [ -n "$driver" ]; then
    $PH "$name-driver" -- bash -c "$driver" > "$OUT/driver.$name.log" 2>&1
  fi
  wait "$sleep_pid"
  snap "$PAT" "" "$name.after"
  screenshot "after-$name"
  phase_summary "$name"
}

# ctrl_prelude <label>: the untraced control's prelude (decision 4) — the application back in its designed state
# before a driven run; the window is read again, since a prelude may reopen the document. With no window manager a key
# reaches the window under the pointer, so the pointer goes to the window's centre first, where a dialog the prelude
# raises also opens (dry run 2026-09-27)
ctrl_prelude() {
  local x y w h
  read -r x y w h < <(xdotool getwindowgeometry --shell "$WID" 2>/dev/null | awk -F= '/^X=/{x=$2} /^Y=/{y=$2} /^WIDTH=/{w=$2} /^HEIGHT=/{h=$2} END{print x, y, w, h}')
  [ -n "$h" ] && xdotool mousemove "$((x + w / 2))" "$((y + h / 2))"
  rec "ctrlprelude.$1.pointer" "$((x + w / 2)),$((y + h / 2))"
  xdotool windowactivate --sync "$WID" 2>/dev/null
  bash -c "$CTRLPRELUDE" > "$OUT/ctrlprelude.$1.log" 2>&1; rec "ctrlprelude.$1.rc" "$?"
  local w; w=$(wait_window "$CLASS" 60); [ -n "$w" ] && WID="$w"
  rec "ctrlprelude.$1.window" "$WID"
  screenshot "after-ctrlprelude-$1"; sleep 5
}

# pair <name> <seconds> <driver-builder> [prelude]: one carried phase as its traced run <name> and its untraced run
# <name>-untraced, adjacent, in the job's ORDER (decisions 1, 5, 6); the builder echoes a run's driver command, given
# the run, once any prelude has run
pair() {
  local name="$1" secs="$2" builder="$3" prelude="${4:-}" run first=1
  for run in $ORDER; do
    [ "$first" = 1 ] || sleep 10
    first=0
    [ -n "$prelude" ] && ctrl_prelude "$name.$run"
    if [ "$run" = traced ]; then
      $PH "$name" -- bash -c "true"; phase "$name" "$secs" "$($builder traced)"
    else
      $PH "$name-untraced" -- bash -c "true"; quiet "$name-untraced" "$secs" "$($builder untraced)"
    fi
  done
}

# the drivers a pair's runs take, one log per run
no_driver() { echo ""; }
stream_driver() {
  local log="$OUT/replay.jsonl"; [ "$1" = untraced ] && log="$OUT/replay-untraced.jsonl"
  echo "python3 $TOOLS/replay_stream.py $SFILE $WID $log --seconds $DRIVEN --area $AREA --kinds $KINDS"
}
pointer_loop() {
  echo "xdotool windowactivate --sync $WID; end=\$((\$(date +%s)+$DRIVEN)); while [ \$(date +%s) -lt \$end ]; do xdotool mousemove 300 300 mousedown 1 mousemove --sync 500 400 mousemove --sync 700 350 mouseup 1; sleep 0.8; xdotool mousemove 640 400 click 1; sleep 1.2; xdotool mousemove 400 500 click --repeat 3 --delay 100 4; sleep 1.0; xdotool mousemove 520 380 click --repeat 2 --delay 100 5; sleep 1.5; done"
}
op_run_driver() {
  local log="$OUT/ops.jsonl"; [ "$1" = untraced ] && log="$OUT/ops-untraced.jsonl"
  OPS_OUT="$log" op_driver "$WID" "$OPS"
}

# window_phase <name> <seconds> <driver-cmd>: phase()'s twin for a long driven probe (9.10 D144) — perf over the
# window with the driver inside it from 1 s, as phase(); the trace converted in the background at the lowest
# priority, on the harness CPUs this script is pinned to, so the next window opens as soon as this one's trace stops
# and the perf data, deleted once converted, never accumulates
WINDOW_JOBS=""
window_phase() {
  local name="$1" secs="$2" driver="$3"
  snap "$PAT" "" "$name.before"
  pin_harness sudo perf sched record -k CLOCK_MONOTONIC -a -o "$OUT/perf.$name.data" -- sleep "$secs" > "$OUT/perf.$name.log" 2>&1 &
  local perf_pid=$!
  sleep 1
  $PH "$name-driver" -- bash -c "$driver" > "$OUT/driver.$name.log" 2>&1
  wait "$perf_pid"; rec "perf.$name.record.rc" "$?"
  snap "$PAT" "" "$name.after"
  screenshot "after-$name"
  phase_summary "$name"
  convert_window "$name" &
  WINDOW_JOBS="$WINDOW_JOBS $!"
}
convert_window() {
  local name="$1"
  nice -n 19 sudo perf sched timehist --state -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
  rec "perf.$name.timehist.rc" "${PIPESTATUS[0]}"
  rec "perf.$name.rows_matching" "$(gzip -dc "$OUT/perf.$name.timehist.txt.gz" | grep -cE "$RX" || echo 0)"
  nice -n 19 sudo perf sched timehist -w -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | grep -E "awakened|wakeup|\bwaker\b|^\s*[0-9]+\.[0-9]+ +\[[0-9]+\] +\S.*\[[0-9/]+\] +awakened" | gzip > "$OUT/perf.$name.wakeups.txt.gz"
  rec "perf.$name.wakeups.rows" "$(gzip -dc "$OUT/perf.$name.wakeups.txt.gz" | wc -l)"
  sudo rm -f "$OUT/perf.$name.data"
}
# driven_windows: the probe's driven phase, $WINDOWS windows back to back (9.10 D144). A stream application's window
# k replays the stream's window k, the one 9.5's repeat k replayed, into the document the earlier windows typed — no
# prelude between windows; a pointer application runs its loop in every window
driven_windows() {
  local k name drv f
  rec stream_kinds "$KINDS"
  for k in $(seq 1 "$WINDOWS"); do
    name="driven-w$(printf %02d "$k")"
    if [ "$DRIVER" = stream ]; then
      f="$STREAMS/$STREAM-r$k.jsonl"
      if [ ! -s "$f" ]; then rec "$name.stopped" "window $STREAM-r$k not cut"; break; fi
      rec "$name.stream_file" "$(basename "$f")"
      drv="python3 $TOOLS/replay_stream.py $f $WID $OUT/replay.$name.jsonl --seconds $DRIVEN --area $AREA --kinds $KINDS"
    else
      drv="$(pointer_loop)"
    fi
    $PH "$name" -- bash -c "true"; window_phase "$name" "$((DRIVEN + 5))" "$drv"
    [ "$DRIVER" = stream ] && rec "replay.$name.sent" "$(wc -l < "$OUT/replay.$name.jsonl" 2>/dev/null || echo 0)"
  done
  # shellcheck disable=SC2086
  wait $WINDOW_JOBS
}

# window_state: whether this job's recorded-input window is cut and holds events — ok, empty or uncut
window_state() {
  python3 -c 'import json, sys; w = json.load(open(sys.argv[1]))["windows"].get(sys.argv[2]); print("uncut" if w is None else "ok" if w.get("events") else "empty")' "$STREAMS/windows.json" "$STREAM-r$REPEAT"
}

# control_phases: the untraced control's sequence (decisions 3, 6) — the campaign's phase order, each carried phase an
# adjacent pair; the 136M phase, which no archetype carries, left out
control_phases() {
  case "$DRIVER" in
    stream|pointer)
      pair idle "$IDLE" no_driver
      sleep 10
      if [ "$DRIVER" = stream ]; then
        local w; w="$(window_state)"; rec recording.window "$w"
        if [ "$w" != ok ]; then rec control.stopped "window $w"; return; fi
        SFILE="$STREAMS/$STREAM-r$REPEAT.jsonl"; rec stream_file "$(basename "$SFILE")"; rec stream_kinds "$KINDS"
        pair driven "$((DRIVEN + 5))" stream_driver prelude
        rec replay.sent "$(wc -l < "$OUT/replay.jsonl" 2>/dev/null || echo 0)"
        rec replay_untraced.sent "$(wc -l < "$OUT/replay-untraced.jsonl" 2>/dev/null || echo 0)"
      else
        pair driven "$((DRIVEN + 5))" pointer_loop prelude
      fi ;;
    none)
      pair play "$PLAY" no_driver ;;
  esac
  if [ -n "$OP" ]; then
    sleep 10
    pair op "$((OPS + 5))" op_run_driver
    rec ops.count "$(wc -l < "$OUT/ops.jsonl" 2>/dev/null || echo 0)"
    rec ops.rc0 "$(grep -c '"rc": 0' "$OUT/ops.jsonl" 2>/dev/null || echo 0)"
    rec ops_untraced.count "$(wc -l < "$OUT/ops-untraced.jsonl" 2>/dev/null || echo 0)"
    rec ops_untraced.rc0 "$(grep -c '"rc": 0' "$OUT/ops-untraced.jsonl" 2>/dev/null || echo 0)"
  fi
}

if [ "$CONTROL" = 1 ]; then
  control_phases
else
case "$DRIVER" in
  stream)
    # D32: a repeat past the recording's end — its window recorded empty in windows.json (an empty window is not
    # committed) — runs the idle phase alone and is pooled into the idle values only; no operation phase either,
    # since without the driven phases it would start from another application state
    WINDOW="$(window_state)"
    rec recording.window "$WINDOW"
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    if [ "$MODE" = probe ] || [ "$MODE" = idle ]; then OP=""
    elif [ "$MODE" = probe-driven ]; then OP=""; sleep 10; driven_windows
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
      if [ -n "$ALTPRELUDE" ]; then xdotool windowactivate --sync "$WID"; bash -c "$ALTPRELUDE" > "$OUT/altprelude.log" 2>&1; rec altprelude.rc "$?"; screenshot after-altprelude; sleep 5; fi
      DRVA="python3 $TOOLS/replay_stream.py $AFILE $WID $OUT/replay-alt.jsonl --seconds $DRIVEN --area $AREA"
      $PH driven-alt -- bash -c "true"; phase driven-alt "$((DRIVEN + 5))" "$DRVA"
      rec replay_alt.sent "$(wc -l < "$OUT/replay-alt.jsonl" 2>/dev/null || echo 0)"
    fi
    fi ;;
  pointer)
    $PH idle -- bash -c "true"; phase idle "$IDLE" ""
    if [ "$MODE" = probe ] || [ "$MODE" = idle ]; then OP=""
    elif [ "$MODE" = probe-driven ]; then OP=""; sleep 10; driven_windows; else
    sleep 10
    DRV="$(pointer_loop)"
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
fi
rec window.name_after "$(xdotool getwindowname "$WID" 2>/dev/null | tr -d '\n' | head -c 120)"
kill -- "-$APP_PID" 2>/dev/null; sleep 2; kill -9 -- "-$APP_PID" 2>/dev/null; appdef_cleanup; kill "$(cat "$OUT/xvfb.pid")" 2>/dev/null
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
