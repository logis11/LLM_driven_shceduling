#!/usr/bin/env bash
# costs/run.sh <repeat> [full|dry] — the 9.12 kernel-cost repeat (research-slice changelog D31; method
# _dev/research/jioh/task-9.12-related-work-prose/campaign/method.md). On the runner's own kernel, every load
# pinned to the measured CPU (pin.sh):
#   1. context-switch cost — the two-process pipe ping-pong (round trip = two switches), the same two calls on one
#      process's own pipe, `perf bench sched pipe`, and lmbench `lat_ctx` at 0, 16 and 64 KB per process;
#   2. the fair class's pick — ftrace function_graph timing each call of `pick_next_task_fair` and, where
#      traceable, `pick_task_fair` and `sched_balance_newidle`, under the ping-pong, `perf bench sched messaging`
#      and a 1 ms sleeper; `__task_pid_nr_ns`, the whole of getpid's work, under a getpid loop calibrates the
#      tracer's own share (`__x64_sys_getpid` is not traceable on 6.17.0-1022-azure, the dry run);
#   3. switch rates at idle — per-CPU context switches (`perf stat -A`) and schedule() calls (/proc/schedstat).
# Writes report.json (key=value record), costs.json (the values), the traces and tool outputs.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEAS="$(cd "$HERE/.." && pwd)"
source "$MEAS/probe/common.sh"        # OUT, KV, rec, finish_report
source "$MEAS/pin.sh"
pin_self_harness
REPEAT="$1"; MODE="${2:-full}"
WORK=/tmp/costs; mkdir -p "$WORK"
if [ "$MODE" = dry ]; then
  RUNS=2; RT=100000; PERF_LOOPS=100000; TRACE_RT=20000; MSG_LOOPS=20; SLEEPS=500; GETPIDS=50000; IDLE_S=5; IDLE_W=1
else
  RUNS=5; RT=1000000; PERF_LOOPS=1000000; TRACE_RT=200000; MSG_LOOPS=100; SLEEPS=5000; GETPIDS=500000; IDLE_S=20; IDLE_W=3
fi

rec family costs; rec job kernel; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$MEAS/runner_spec.py" > "$OUT/spec.json"
source "$MEAS/machine_gate.sh"
rec machine.model "$(machine_model)"; rec machine.wanted "${MEAS_CPU_MODEL:-}"
if ! machine_gate "${MEAS_CPU_MODEL:-}"; then
  rec gate wrong-machine; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "machine gate: wanted '${MEAS_CPU_MODEL}', drew '$(machine_model)' — stopping before any measurement" >&2
  exit 0
fi
rec gate open
rec kernel "$(uname -r)"
cat /proc/cmdline > "$OUT/cmdline.txt"
grep -r . /sys/devices/system/cpu/vulnerabilities/ > "$OUT/vulnerabilities.txt" 2>&1
CFG="/boot/config-$(uname -r)"
[ -f "$CFG" ] && grep -E '^CONFIG_(HZ|HZ_[0-9]+|PREEMPT[A-Z_]*|SCHEDSTATS|FUNCTION_GRAPH_TRACER|FUNCTION_TRACER|FAIR_GROUP_SCHED|SCHED_CLASS_EXT|MITIGATION_[A-Z_]*)=' "$CFG" > "$OUT/kconfig.txt"
cat /sys/kernel/debug/sched/preempt > "$OUT/preempt.txt" 2>/dev/null || sudo cat /sys/kernel/debug/sched/preempt > "$OUT/preempt.txt" 2>&1

sudo apt-get update > "$OUT/apt.update.log" 2>&1; rec apt.update.rc "$?"
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
sudo apt-get install -y --no-install-recommends lmbench > "$OUT/apt.lmbench.log" 2>&1; rec apt.lmbench.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
LAT_CTX="$(dpkg -L lmbench 2>/dev/null | grep '/lat_ctx$' | head -1)"; rec lmbench.lat_ctx "$LAT_CTX"
rec lmbench.version "$(dpkg-query -W -f='${Version}' lmbench 2>/dev/null)"
gcc -O2 -Wall -o "$WORK/pingpong" "$HERE/pingpong.c" > "$OUT/gcc.log" 2>&1; rec pingpong.build.rc "$?"
rec gcc.version "$(gcc --version | head -1)"
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null 2>&1
sudo sysctl -w kernel.sched_schedstats=1 > /dev/null 2>&1; rec sysctl.sched_schedstats "$(cat /proc/sys/kernel/sched_schedstats 2>/dev/null || echo missing)"
CPU="$MEAS_CPU"

# 1. context-switch cost: the measured runs alternate pair and self so a drift in the machine reaches both
: > "$OUT/pingpong.txt"
for i in $(seq 1 "$RUNS"); do
  pin_load "$WORK/pingpong" pair "$RT" >> "$OUT/pingpong.txt" 2>&1
  pin_load "$WORK/pingpong" self "$RT" >> "$OUT/pingpong.txt" 2>&1
done
: > "$OUT/perf-bench-pipe.txt"
for i in $(seq 1 "$RUNS"); do
  pin_load perf bench sched pipe -l "$PERF_LOOPS" >> "$OUT/perf-bench-pipe.txt" 2>&1
done
: > "$OUT/lat_ctx.txt"
if [ -n "$LAT_CTX" ]; then
  for size in 0 16 64; do
    echo "## -s $size" >> "$OUT/lat_ctx.txt"
    pin_load "$LAT_CTX" -P 1 -W 3 -N 11 -s "$size" 2 >> "$OUT/lat_ctx.txt" 2>&1
  done
fi

# 2. the fair class's pick, timed by the function-graph tracer on the measured CPU only
T=/sys/kernel/tracing; [ -d "$T/events" ] || T=/sys/kernel/debug/tracing
rec tracefs "$T"
sudo cat "$T/available_filter_functions" > "$WORK/aff.txt" 2>/dev/null; gzip -c "$WORK/aff.txt" > "$OUT/available_filter_functions.txt.gz"
for f in pick_next_task_fair __pick_next_task_fair pick_task_fair sched_balance_newidle __task_pid_nr_ns __x64_sys_getpid; do
  rec "traceable.$f" "$(grep -c -E "^$f( |$)" "$WORK/aff.txt")"
done
MASK="$(printf '%x' $((1 << CPU)))"
tw() { echo "$2" | sudo tee "$T/$1" > /dev/null; }
trace_pass() { # trace_pass <function> <label> <load cmd...>
  local f="$1" label="$2"; shift 2
  if [ "$(grep -c -E "^$f( |$)" "$WORK/aff.txt")" = 0 ]; then rec "trace.$f.$label" untraceable; return 0; fi
  tw tracing_on 0; tw current_tracer nop; tw trace ""
  tw tracing_cpumask "$MASK"
  tw "per_cpu/cpu$CPU/buffer_size_kb" 262144
  tw set_ftrace_filter "$f"; tw set_graph_function "$f"; tw max_graph_depth 1
  tw current_tracer function_graph
  for o in funcgraph-duration funcgraph-overhead funcgraph-cpu; do tw "options/$o" 1; done
  for o in funcgraph-proc funcgraph-abstime funcgraph-tail; do tw "options/$o" 0; done
  tw tracing_on 1
  "$@" > "$OUT/trace.$f.$label.load.txt" 2>&1
  tw tracing_on 0
  sudo cat "$T/per_cpu/cpu$CPU/stats" > "$OUT/trace.$f.$label.stats" 2>&1
  sudo cat "$T/per_cpu/cpu$CPU/trace" > "$WORK/trace.txt"
  python3 "$HERE/graph_durations.py" "$WORK/trace.txt" "$f" > "$OUT/trace.$f.$label.json"
  gzip -c "$WORK/trace.txt" > "$OUT/trace.$f.$label.txt.gz"
  rec "trace.$f.$label" "$(cat "$OUT/trace.$f.$label.json")"
  rec "trace.$f.$label.overrun" "$(sed -n 's/^overrun: *//p' "$OUT/trace.$f.$label.stats")"
  tw current_tracer nop; tw set_ftrace_filter ""; tw set_graph_function ""
}
# the same loads untraced, beside the traced passes: the difference per call is the tracer's whole cost
pin_load "$WORK/pingpong" pair "$TRACE_RT" > "$OUT/untraced.pingpong.load.txt" 2>&1
pin_load "$WORK/pingpong" getpid "$GETPIDS" > "$OUT/untraced.getpid.load.txt" 2>&1
for f in pick_next_task_fair pick_task_fair sched_balance_newidle; do
  trace_pass "$f" pingpong pin_load "$WORK/pingpong" pair "$TRACE_RT"
  trace_pass "$f" messaging pin_load perf bench sched messaging -p -g 2 -l "$MSG_LOOPS"
  trace_pass "$f" sleep pin_load "$WORK/pingpong" sleep "$SLEEPS" 1000
done
trace_pass __task_pid_nr_ns getpid pin_load "$WORK/pingpong" getpid "$GETPIDS"

# 3. switch rates at idle: nothing of the job runs but perf's own sleep, on a harness CPU
: > "$OUT/idle.txt"
for w in $(seq 1 "$IDLE_W"); do
  sudo cat /proc/schedstat > "$OUT/schedstat.idle.$w.start" 2>&1
  t0=$(now_us)
  sudo perf stat -a -A -x, -e context-switches -o "$OUT/perfstat.idle.$w.csv" -- sleep "$IDLE_S" > /dev/null 2>&1
  t1=$(now_us)
  sudo cat /proc/schedstat > "$OUT/schedstat.idle.$w.end" 2>&1
  echo "window=$w t0_us=$t0 t1_us=$t1" >> "$OUT/idle.txt"
done

python3 "$HERE/analyze.py" "$OUT" > "$OUT/costs.json" 2> "$OUT/analyze.err"; rec analyze.rc "$?"
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
