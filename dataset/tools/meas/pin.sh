#!/usr/bin/env bash
# pin.sh — single-core measurement (9.5 follow-ups spec, decisions 2, 3, 5).
# Source it. Every measured load on the runner is pinned to one CPU
# (MEAS_CPU, the last one); the harness — display server, replay driver,
# perf, sidecars, snapshots — runs on the others (MEAS_HARNESS_CPUS), so the
# observation is the load's own serialisation on one CPU with the rest of
# the machine idealised. On a one-CPU machine both sets are CPU 0. Without
# taskset (dev machines) nothing is pinned and MEAS_PIN_AVAILABLE=0 says so.
#
#   pin_load    <cmd...>   run cmd on MEAS_CPU
#   pin_harness <cmd...>   run cmd on MEAS_HARNESS_CPUS
#   pin_self_harness       move the calling shell (and its future children) to MEAS_HARNESS_CPUS
#   pin_record             print the pin as key=value lines
MEAS_NPROC="${MEAS_NPROC:-$(nproc 2>/dev/null || echo 1)}"
if [ "$MEAS_NPROC" -gt 1 ]; then
  MEAS_CPU="${MEAS_CPU:-$((MEAS_NPROC - 1))}"
  MEAS_HARNESS_CPUS="${MEAS_HARNESS_CPUS:-0-$((MEAS_NPROC - 2))}"
else
  MEAS_CPU="${MEAS_CPU:-0}"; MEAS_HARNESS_CPUS="${MEAS_HARNESS_CPUS:-0}"
fi
if command -v taskset > /dev/null 2>&1; then MEAS_PIN_AVAILABLE=1; else MEAS_PIN_AVAILABLE=0; fi
export MEAS_NPROC MEAS_CPU MEAS_HARNESS_CPUS MEAS_PIN_AVAILABLE

pin_load()    { if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_CPU" "$@"; else "$@"; fi; }
pin_harness() { if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_HARNESS_CPUS" "$@"; else "$@"; fi; }
pin_self_harness() { if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -cp "$MEAS_HARNESS_CPUS" $$ > /dev/null; fi; }
pin_record() {
  printf 'pin.nproc=%s\npin.load_cpu=%s\npin.harness_cpus=%s\npin.available=%s\n' \
    "$MEAS_NPROC" "$MEAS_CPU" "$MEAS_HARNESS_CPUS" "$MEAS_PIN_AVAILABLE"
}
