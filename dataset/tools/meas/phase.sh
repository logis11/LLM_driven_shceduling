#!/usr/bin/env bash
# phase.sh <phases-file> <phase-name> -- <command...>
# Runs the command inside a named measurement phase, appending
# {"phase","start_us","end_us","rc"} to the phases file. Never fails the
# job — a failed phase is recorded (rc != 0), not fatal, so one broken
# phase can't void the rest of the batch.
set -u
PHASES_FILE="$1"; PHASE_NAME="$2"; shift 2
[ "${1:-}" = "--" ] && shift
START_US=$(date +%s%6N)
"$@"
RC=$?
END_US=$(date +%s%6N)
printf '{"phase":"%s","start_us":%s,"end_us":%s,"rc":%d}\n' \
  "$PHASE_NAME" "$START_US" "$END_US" "$RC" >> "$PHASES_FILE"
echo "phase $PHASE_NAME: rc=$RC $(( (END_US - START_US) / 1000000 ))s"
exit 0
