#!/usr/bin/env bash
# Shared probe steps for the 9.5 runner probe. Sourced by apps.sh and the
# workflow. Nothing here fails the job: every check records rc and moves on.
set -u
OUT="${PROBE_OUT:-/tmp/probe}"
mkdir -p "$OUT"
KV="$OUT/report.kv"
TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

rec() { printf '%s=%s\n' "$1" "$2" >> "$KV"; echo "  $1=$2" >&2; }  # stderr: callers use command substitution
run_rec() { # run_rec <key> <cmd...> : records rc and captures output to a file
  local key="$1"; shift
  "$@" > "$OUT/$key.out" 2> "$OUT/$key.err"; local rc=$?
  rec "$key.rc" "$rc"; return 0
}
now_us() { date +%s%6N; }

finish_report() { python3 - "$KV" "$OUT/report.json" <<'PY'
import json, sys
kv = {}
for line in open(sys.argv[1]):
    k, _, v = line.rstrip("\n").partition("=")
    kv[k] = v
json.dump(kv, open(sys.argv[2], "w"), indent=1, sort_keys=True)
PY
}

start_xvfb() {
  export DISPLAY=:99
  Xvfb :99 -screen 0 1280x800x24 -ac > "$OUT/xvfb.log" 2>&1 &
  echo $! > "$OUT/xvfb.pid"; sleep 2
  rec xvfb.alive "$(kill -0 "$(cat "$OUT/xvfb.pid")" 2>/dev/null && echo 1 || echo 0)"
}

wait_window() { # wait_window <class-regex> <seconds> -> prints window id or empty
  local rx="$1" secs="$2" t0 id
  t0=$(now_us)
  for _ in $(seq 1 "$((secs * 2))"); do
    id=$(xdotool search --onlyvisible --class "$rx" 2>/dev/null | head -1)
    if [ -z "$id" ]; then id=$(xdotool search --onlyvisible --classname "$rx" 2>/dev/null | head -1); fi
    if [ -z "$id" ]; then id=$(xdotool search --onlyvisible --name "$rx" 2>/dev/null | head -1); fi
    if [ -n "$id" ]; then
      rec window.found 1; rec window.id "$id"
      rec window.wait_ms "$(( ($(now_us) - t0) / 1000 ))"
      rec window.name "$(xdotool getwindowname "$id" 2>/dev/null | tr -d '\n' | head -c 120)"
      echo "$id"; return 0
    fi
    sleep 0.5
  done
  rec window.found 0; rec window.wait_ms "$(( ($(now_us) - t0) / 1000 ))"
  echo ""; return 0
}

screenshot() { import -window root "$OUT/$1.png" 2>/dev/null || xwd -root -silent | convert xwd:- "$OUT/$1.png" 2>/dev/null; rec "shot.$1" "$([ -f "$OUT/$1.png" ] && echo 1 || echo 0)"; }

snap() { python3 "$TOOLS/snapshot.py" "$1" "${2:-snapshot.py|xdotool|probe|perf}" > "$OUT/snap.$3.json"; }

perf_capture() { # perf_capture <label> <seconds> <comm-regex> — runs in background over the window
  local label="$1" secs="$2" rx="$3"
  sudo perf sched record -a -o "$OUT/perf.$label.data" -- sleep "$secs" > "$OUT/perf.$label.log" 2>&1
  rec "perf.$label.record.rc" "$?"
  sudo perf sched timehist -i "$OUT/perf.$label.data" > "$OUT/perf.$label.timehist.txt" 2>> "$OUT/perf.$label.log"
  rec "perf.$label.timehist.rc" "$?"
  rec "perf.$label.sched_rows_matching" "$(grep -cE "$rx" "$OUT/perf.$label.timehist.txt" 2>/dev/null || echo 0)"
  rec "perf.$label.sched_rows_total" "$(wc -l < "$OUT/perf.$label.timehist.txt" 2>/dev/null || echo 0)"
}

# probe_phase <phase> <pattern> <comm-regex> <seconds> <driver-cmd or ''>
# Snapshots CPU/threads/switches around a phase; runs the driver (typing,
# pointer, nothing) and a 5 s perf capture inside it.
probe_phase() {
  local phase="$1" pat="$2" rx="$3" secs="$4" driver="$5"
  snap "$pat" "" "$phase.before"
  local t0; t0=$(now_us)
  local drv=""
  if [ -n "$driver" ]; then bash -c "$driver" > "$OUT/driver.$phase.log" 2>&1 & drv=$!; fi
  sleep 2; perf_capture "$phase" 5 "$rx"
  local left=$(( secs - 7 )); [ "$left" -gt 0 ] && sleep "$left"
  if [ -n "$drv" ]; then wait "$drv" 2>/dev/null; fi
  snap "$pat" "" "$phase.after"
  python3 - "$OUT/snap.$phase.before.json" "$OUT/snap.$phase.after.json" "$phase" <<'PY' | tee -a "$KV" | sed 's/^/  /' >&2
import json, sys
a, b, ph = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), sys.argv[3]
dt = b["t_mono"] - a["t_mono"]
print(f"{ph}.wall_s={dt:.2f}")
print(f"{ph}.n_procs={b['n_procs']}")
print(f"{ph}.n_threads={b['n_threads']}")
print(f"{ph}.cpu_s={b['cpu_s']-a['cpu_s']:.3f}")
print(f"{ph}.cpu_share={(b['cpu_s']-a['cpu_s'])/dt if dt else 0:.4f}")
print(f"{ph}.vol_switches={b['vol_switches']-a['vol_switches']}")
print(f"{ph}.nonvol_switches={b['nonvol_switches']-a['nonvol_switches']}")
print(f"{ph}.switches_per_s={(b['vol_switches']-a['vol_switches']+b['nonvol_switches']-a['nonvol_switches'])/dt if dt else 0:.1f}")
PY
}

type_driver() { # type_driver <window-id> — replays the probe gaps into the window
  echo "xdotool windowactivate --sync $1; sleep 0.5; python3 $TOOLS/replay.py $TOOLS/gaps-probe.txt active $OUT/replay.jsonl"
}
pointer_driver() { # pointer_driver <window-id> — drags and clicks around the window for ~20 s
  echo "xdotool windowactivate --sync $1; for i in \$(seq 1 20); do xdotool mousemove 300 300 mousedown 1 mousemove --sync 500 400 mousemove --sync 700 350 mouseup 1; sleep 0.3; xdotool mousemove 640 400 click 1; sleep 0.4; xdotool mousemove 400 500 click --repeat 3 --delay 100 4; sleep 0.3; done"
}
