#!/usr/bin/env bash
# phase.sh <phases-file> <phase-name> -- <command...>
# Runs the command inside a named measurement phase, appending
# {"phase","start_us","end_us","rc","pin","cpu"} to the phases file. Never
# fails the job — a failed phase is recorded (rc != 0), not fatal, so one
# broken phase can't void the rest of the batch.
#
# Pinning (pin.sh): MEAS_PIN=load (default) runs the command on the one
# measured CPU; MEAS_PIN=harness runs it on the harness CPUs (a driver that
# stimulates a load launched elsewhere); MEAS_PIN=none leaves it alone.
set -u
PHASES_FILE="$1"; PHASE_NAME="$2"; shift 2
[ "${1:-}" = "--" ] && shift
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pin.sh"
PIN="${MEAS_PIN:-load}"
case "$PIN" in
  load)    CPUS="$MEAS_CPU"; RUN=pin_load ;;
  harness) CPUS="$MEAS_HARNESS_CPUS"; RUN=pin_harness ;;
  *)       PIN=none; CPUS=""; RUN="" ;;
esac
[ "$MEAS_PIN_AVAILABLE" = 1 ] || { PIN=none; CPUS=""; RUN=""; }
START_US=$(date +%s%6N)
$RUN "$@"
RC=$?
END_US=$(date +%s%6N)
printf '{"phase":"%s","start_us":%s,"end_us":%s,"rc":%d,"pin":"%s","cpu":"%s"}\n' \
  "$PHASE_NAME" "$START_US" "$END_US" "$RC" "$PIN" "$CPUS" >> "$PHASES_FILE"
echo "phase $PHASE_NAME: rc=$RC $(( (END_US - START_US) / 1000000 ))s pin=$PIN${CPUS:+ cpu=$CPUS}"
exit 0
