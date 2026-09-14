#!/usr/bin/env bash
# timing.sh — does per-event xdotool replay hold the requested intervals
# under Xvfb? Logs delivered KeyPress times in an X client and compares.
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y --no-install-recommends xdotool python3-xlib > "$OUT/apt.log" 2>&1; rec apt.rc "$?"
start_xvfb
python3 "$TOOLS/xkeylog.py" "$OUT/delivered.jsonl" 60 > "$OUT/xkeylog.log" 2>&1 &
XKL=$!
sleep 2
WID=$(wait_window "xkeylog" 20)
if [ -n "$WID" ]; then
  xdotool windowactivate --sync "$WID"; xdotool windowfocus --sync "$WID"; sleep 0.5
  python3 "$TOOLS/replay.py" "$TOOLS/gaps-probe.txt" "$WID" "$OUT/replay.jsonl"; rec replay.rc "$?"
  sleep 1
  python3 "$TOOLS/timing_report.py" "$OUT/replay.jsonl" "$OUT/delivered.jsonl" > "$OUT/timing.json"; rec timing.rc "$?"
  cat "$OUT/timing.json"
  # constant-delay baseline
  : > "$OUT/delivered.jsonl"
  xdotool type --window "$WID" --delay 100 "$(head -c 60 < /dev/zero | tr '\0' 'a')"; rec type_delay.rc "$?"
  sleep 1; rec type_delay.delivered "$(wc -l < "$OUT/delivered.jsonl")"
fi
wait "$XKL" 2>/dev/null; kill "$(cat "$OUT/xvfb.pid")" 2>/dev/null; rec finished_utc "$(date -u +%FT%TZ)"
finish_report
