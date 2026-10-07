#!/usr/bin/env bash
# The scheduler tunables of the runner's kernel (9.11 D2). Run as root.
#
# base_slice_ns is kernel/sched/fair.c's sysctl_sched_base_slice, which
# update_sysctl() sets to the normalized value x (1 + ilog2(min(online CPUs, 8)))
# at boot and on every CPU online and offline (rq_online_fair, rq_offline_fair).
# It is read at the boot CPU count, after each CPU is taken offline down to one,
# and after each is brought back; each step is read at once and again after a
# 3 s settle, since the sched-domain rebuild runs after the hotplug. The other
# sched debugfs, sysctl and sched_ext values are read once, before any hotplug.
# A configuration read, not a workload measurement; a failed step is a recorded rc.
set -u
OUT=${PROBE_OUT:?}
mkdir -p "$OUT"
HERE=$(cd "$(dirname "$0")" && pwd)
python3 "$HERE/../runner_spec.py" > "$OUT/spec.json"
uname -a > "$OUT/uname.txt"
mountpoint -q /sys/kernel/debug || mount -t debugfs none /sys/kernel/debug
echo "debugfs mount rc=$?" > "$OUT/hotplug.txt"
S=/sys/kernel/debug/sched
SYS=/sys/devices/system/cpu

dump() {
  local f
  for f in "$@"; do
    [ -f "$f" ] && printf '%s\t%s\n' "$f" "$(tr '\n' ' ' 2>&1 < "$f")"
  done
}
{
  dump "$S"/features "$S"/preempt "$S"/base_slice_ns "$S"/tunable_scaling \
       "$S"/migration_cost_ns "$S"/nr_migrate "$S"/latency_warn_ms "$S"/latency_warn_once
  dump "$S"/fair_server/cpu*/runtime "$S"/fair_server/cpu*/period
  dump "$S"/ext_server/cpu*/runtime "$S"/ext_server/cpu*/period
  dump /proc/sys/kernel/sched_*
  dump /sys/kernel/sched_ext/state /sys/kernel/sched_ext/enable_seq /sys/kernel/sched_ext/root/ops
} > "$OUT/tunables.tsv"
ls -la "$S" > "$OUT/debugfs-sched.txt" 2>&1

TSV="$OUT/base_slice.tsv"
printf 'step\tsettle_s\tonline\tnum_online\tbase_slice_ns\ttunable_scaling\n' > "$TSV"
row() {  # step settle_s
  sleep "$2"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$(cat $SYS/online)" "$(getconf _NPROCESSORS_ONLN)" \
    "$(cat $S/base_slice_ns 2>&1)" "$(cat $S/tunable_scaling 2>&1)" >> "$TSV"
}

row boot 0
HOT=()
for c in $(ls -d $SYS/cpu[0-9]* | sed 's#.*/cpu##' | sort -n); do
  [ -e "$SYS/cpu$c/online" ] && HOT+=("$c")
done
echo "hotpluggable: ${HOT[*]}" >> "$OUT/hotplug.txt"
for ((i = ${#HOT[@]} - 1; i >= 0; i--)); do
  [ "$(getconf _NPROCESSORS_ONLN)" -le 1 ] && break
  c=${HOT[$i]}
  echo 0 > "$SYS/cpu$c/online"
  echo "offline cpu$c rc=$?" >> "$OUT/hotplug.txt"
  row "offline-cpu$c" 0
  row "offline-cpu$c" 3
done
for c in "${HOT[@]}"; do
  [ "$(cat "$SYS/cpu$c/online")" = 1 ] && continue
  echo 1 > "$SYS/cpu$c/online"
  echo "online cpu$c rc=$?" >> "$OUT/hotplug.txt"
  row "online-cpu$c" 0
  row "online-cpu$c" 3
done
exit 0
