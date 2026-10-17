#!/bin/bash
# tracker-session.sh <measured cpu> <cap s> <out dir> — the Tracker campaign's session (9.10 D61–D65; method §2, §3).
# Run by run.sh inside the chroot, as the user, under dbus-run-session, on the harness CPUs. Starts the miner as its
# user unit's ExecStart (S2-41), its settings as shipped, taskset placing it — and so the extractor it starts and
# every process below it — on the measured CPU. TRACKER_DEBUG=status alone (D69): the status trace the job's boundaries
# are read from — the miner's Idle and Initializing (the initial sleep), the extractor's Extracting metadata and Idle
# (D62's "Extraction finished", logged in the same millisecond). The phase ends once the extractor's last status is Idle
# after Extracting metadata and no extractor runs — it exits after its 10 s of inactivity — or at the cap; the
# database's counts are read and the miner is stopped with SIGTERM, its clean shutdown.
CPU="$1"; CAP="$2"; L="$3"
gsettings list-recursively org.freedesktop.Tracker3.Miner.Files > "$L/tracker.settings.txt" 2>&1
gsettings list-recursively org.freedesktop.Tracker3.Extract >> "$L/tracker.settings.txt" 2>&1
cat /proc/self/mountinfo > "$L/tracker.mountinfo.txt" 2>&1
env | sort > "$L/tracker.env.txt"
TRACKER_DEBUG=status taskset -c "$CPU" /usr/libexec/tracker-miner-fs-3 > "$L/tracker.log" 2>&1 &
M=$!
echo "miner_pid=$M"
t0=$(date +%s); done=0
while [ $(( $(date +%s) - t0 )) -lt "$CAP" ]; do
  sleep 2
  kill -0 "$M" 2>/dev/null || { echo "miner_exited=1"; break; }
  last="$(grep -E "TrackerExtractDecorator'\) set property:'status' to '(Idle|Extracting metadata)'" "$L/tracker.log" | tail -1)"
  if grep -q "TrackerExtractDecorator') set property:'status' to 'Extracting metadata'" "$L/tracker.log" \
     && [ "${last##*to }" = "'Idle'" ] && ! pgrep -P "$M" -x tracker-extract > /dev/null; then done=1; break; fi
done
echo "done=$done elapsed_s=$(( $(date +%s) - t0 ))"
tracker3 status > "$L/tracker.status.txt" 2>&1
q() { tracker3 sparql --dbus-service org.freedesktop.Tracker3.Miner.Files -q "$2" > "$L/tracker.count.$1.txt" 2>&1; }
D='file:///home/'"$USER"'/Documents/'
q types "SELECT ?t (COUNT(?i) AS ?n) WHERE { ?f a nfo:FileDataObject ; nie:url ?u ; nie:interpretedAs ?i . ?i a ?t . FILTER (STRSTARTS(?u, \"$D\")) } GROUP BY ?t"
kill -TERM "$M" 2>/dev/null
for _ in $(seq 1 30); do kill -0 "$M" 2>/dev/null || break; sleep 1; done
if kill -0 "$M" 2>/dev/null; then kill -KILL "$M"; echo "miner_killed=1"; fi
wait "$M" 2>/dev/null; echo "miner_rc=$?"
