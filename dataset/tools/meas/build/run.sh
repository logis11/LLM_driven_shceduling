#!/usr/bin/env bash
# run.sh <repeat> <dry|full> — one run of the 9.6 build-and-batch campaign
# (research-slice changelog D3–D8; method
# _dev/research/jioh/task-9.6-compile/campaign/method.md).
#
# Every measured phase is one command pinned to the measured CPU (pin.sh,
# phase.sh MEAS_PIN=load) and observed by two instruments on the harness CPUs:
# `perf sched record -a` over the whole phase (per-schedule run, wait, delay,
# sched-out state, wakeups, fork events) and a taskstats listener registered
# on the measured CPU (per-process CPU, elapsed, parent, comm, block-I/O and
# runnable delays at exit; delay accounting switched on before the phases).
# Phases: build-j8-warm, build-j8-cold, build-j1-warm (the -j1 invariance
# check), dkms (structural check), then the batch programs bound to
# cpu-batch: clamscan, ffmpeg, handbrake, train, tracker. Nothing here fails
# the job: every step records its rc and the next phase runs.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEAS="$(cd "$HERE/.." && pwd)"
source "$MEAS/probe/common.sh"        # OUT, KV, rec, run_rec, finish_report
source "$MEAS/pin.sh"
pin_self_harness
REPEAT="$1"; MODE="${2:-full}"
CORPUS=/tmp/linux-6.6
WORK=/tmp/work; mkdir -p "$WORK"
PH="$MEAS/phase.sh $OUT/phases.jsonl"
export MEAS_PIN=load

if [ "$MODE" = dry ]; then
  BUILD_TARGETS="init/ mm/"; CLAM_DIR="Documentation/admin-guide"; CLIP_S=10; TRAIN_STEPS=30; TRACKER_S=120
else
  BUILD_TARGETS=""; CLAM_DIR="Documentation"; CLIP_S=60; TRAIN_STEPS=300; TRACKER_S=600
fi

rec family build; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec build.targets "${BUILD_TARGETS:-all}"; rec clam.dir "$CLAM_DIR"; rec clip_s "$CLIP_S"; rec train.steps "$TRAIN_STEPS"; rec tracker.max_s "$TRACKER_S"
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$MEAS/runner_spec.py" > "$OUT/spec.json"
python3 -c 'import time,json; print(json.dumps({"mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}))' > "$OUT/clock.json"
rec kernel "$(uname -r)"
rec disk.root "$(df --output=source /tmp | tail -1)"
for d in /sys/block/*; do [ -f "$d/queue/rotational" ] && rec "disk.rotational.$(basename "$d")" "$(cat "$d/queue/rotational")"; done
lsblk -d -o NAME,ROTA,SIZE,MODEL,TRAN > "$OUT/lsblk.txt" 2>&1
CFG="/boot/config-$(uname -r)"
[ -f "$CFG" ] && grep -E '^CONFIG_(TASKSTATS|TASK_DELAY_ACCT|TASK_IO_ACCOUNTING|TASK_XACCT|SCHEDSTATS|PSI|HZ)=' "$CFG" > "$OUT/kconfig.txt"

# ---- packages -----------------------------------------------------------
sudo apt-get update > "$OUT/apt.update.log" 2>&1; rec apt.update.rc "$?"
sudo apt-get install -y --no-install-recommends flex bison libssl-dev libelf-dev bc xz-utils \
  linux-libc-dev build-essential > "$OUT/apt.build.log" 2>&1; rec apt.build.rc "$?"
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
sudo apt-get install -y --no-install-recommends clamav ffmpeg tracker tracker-miner-fs dbus-daemon dbus-user-session \
  python3-pip > "$OUT/apt.batch.log" 2>&1; rec apt.batch.rc "$?"
sudo apt-get install -y --no-install-recommends handbrake-cli > "$OUT/apt.handbrake.log" 2>&1; rec apt.handbrake.rc "$?"
sudo apt-get install -y --no-install-recommends dkms "linux-headers-$(uname -r)" > "$OUT/apt.dkms.log" 2>&1; rec apt.dkms.rc "$?"
# the package's postinst builds the module once, unpinned; the measured build is a rebuild under the pin (dkms phase)
sudo apt-get install -y --no-install-recommends v4l2loopback-dkms > "$OUT/apt.v4l2.log" 2>&1; rec apt.v4l2.rc "$?"
rec dkms.version "$(dkms --version 2>&1 | head -1)"
dkms status > "$OUT/dkms.status.txt" 2>&1
V4L2_VER="$(dkms status 2>/dev/null | sed -n 's#^v4l2loopback[/,] *\([^,: ]*\).*#\1#p' | head -1)"; rec dkms.v4l2_version "${V4L2_VER:-}"
pip3 install --break-system-packages --index-url https://download.pytorch.org/whl/cpu torch > "$OUT/pip.torch.log" 2>&1; rec pip.torch.rc "$?"
rec ffmpeg.version "$(ffmpeg -version 2>/dev/null | head -1)"
rec handbrake.version "$(HandBrakeCLI --version 2>/dev/null | head -1)"
rec clamav.version "$(clamscan --version 2>/dev/null | head -1)"
rec tracker.version "$(tracker3 --version 2>/dev/null | head -1)"
rec python.version "$(python3 --version 2>&1)"

# ---- instruments --------------------------------------------------------
gcc -O2 -Wall -o "$WORK/taskstats_listen" "$HERE/taskstats_listen.c" > "$OUT/gcc.listener.log" 2>&1; rec listener.build.rc "$?"
sudo sysctl -w kernel.task_delayacct=1 > /dev/null 2>&1; rec sysctl.task_delayacct "$(cat /proc/sys/kernel/task_delayacct 2>/dev/null || echo missing)"
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null 2>&1; rec sysctl.perf_event_paranoid "$(cat /proc/sys/kernel/perf_event_paranoid)"
rec sysctl.sched_schedstats "$(cat /proc/sys/kernel/sched_schedstats 2>/dev/null || echo missing)"

listener_start() { # listener_start <phase>
  sudo taskset -c "$MEAS_HARNESS_CPUS" "$WORK/taskstats_listen" -m "$MEAS_CPU" -o "$OUT/taskstats.$1.tsv" 2> "$OUT/taskstats.$1.err" &
  LISTENER_PID=$!; sleep 1
}
listener_stop() { # listener_stop <phase>
  sudo kill -INT "$LISTENER_PID" 2>/dev/null; wait "$LISTENER_PID" 2>/dev/null
  rec "taskstats.$1.rows" "$(grep -vc '^#\|^recv_mono' "$OUT/taskstats.$1.tsv" 2>/dev/null; true)"
  rec "taskstats.$1.enobufs" "$(grep -c ENOBUFS "$OUT/taskstats.$1.err" 2>/dev/null; true)"
}
# smoke: one pinned process must produce one exit record
listener_start smoke; taskset -c "$MEAS_CPU" sh -c 'true'; sleep 1; listener_stop smoke

# phase <name> -- <cmd...>: both instruments over the whole phase; the command pinned on the measured CPU
phase() {
  local name="$1"; shift; [ "${1:-}" = "--" ] && shift
  python3 -c 'import time,json,sys; print(json.dumps({"phase": sys.argv[1], "edge": "start", "mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}))' "$name" >> "$OUT/edges.jsonl"
  listener_start "$name"
  sudo taskset -c "$MEAS_HARNESS_CPUS" perf sched record -k CLOCK_MONOTONIC -a -o "$OUT/perf.$name.data" > "$OUT/perf.$name.log" 2>&1 &
  local perf_pid=$!; sleep 2
  $PH "$name" -- "$@" > "$OUT/cmd.$name.log" 2>&1
  sleep 2
  sudo kill -INT "$perf_pid" 2>/dev/null; wait "$perf_pid" 2>/dev/null; rec "perf.$name.record.rc" "$?"
  listener_stop "$name"
  python3 -c 'import time,json,sys; print(json.dumps({"phase": sys.argv[1], "edge": "end", "mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}))' "$name" >> "$OUT/edges.jsonl"
  sudo perf sched timehist --state -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
  rec "perf.$name.timehist.rc" "${PIPESTATUS[0]}"
  rec "perf.$name.timehist.rows" "$(gzip -dc "$OUT/perf.$name.timehist.txt.gz" | wc -l)"
  sudo perf sched timehist -w -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | grep -E "awakened|wakeup|\bwaker\b" | gzip > "$OUT/perf.$name.wakeups.txt.gz"
  rec "perf.$name.wakeups.rows" "$(gzip -dc "$OUT/perf.$name.wakeups.txt.gz" | wc -l)"
  sudo perf script -i "$OUT/perf.$name.data" -F time,event,trace 2>> "$OUT/perf.$name.log" | grep -E "sched_process_fork|sched_wakeup_new|sched_process_exit" | gzip > "$OUT/perf.$name.forks.txt.gz"
  rec "perf.$name.forks.rows" "$(gzip -dc "$OUT/perf.$name.forks.txt.gz" | wc -l)"
  rec "perf.$name.data_bytes" "$(stat -c %s "$OUT/perf.$name.data" 2>/dev/null || echo 0)"
  sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
  if [ "$MODE" = dry ]; then gzip -f "$OUT/perf.$name.data"; else rm -f "$OUT/perf.$name.data"; fi
}
unmeasured() { pin_harness "$@"; }   # setup steps on the harness CPUs, no instruments

# ---- corpus -------------------------------------------------------------
unmeasured wget -q --tries=5 --waitretry=15 --retry-connrefused \
  https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.6.tar.xz -O /tmp/linux-6.6.tar.xz; rec corpus.wget.rc "$?"
if ! xz -t /tmp/linux-6.6.tar.xz 2>/dev/null; then
  unmeasured wget -q --tries=5 --waitretry=15 https://mirrors.edge.kernel.org/pub/linux/kernel/v6.x/linux-6.6.tar.xz -O /tmp/linux-6.6.tar.xz; rec corpus.wget_mirror.rc "$?"
fi
rec corpus.sha256 "$(sha256sum /tmp/linux-6.6.tar.xz | cut -d' ' -f1)"
unmeasured tar -xf /tmp/linux-6.6.tar.xz -C /tmp; rec corpus.untar.rc "$?"
unmeasured make -C "$CORPUS" defconfig > "$OUT/defconfig.log" 2>&1; rec corpus.defconfig.rc "$?"
rec gcc.version "$(gcc --version | head -1)"; rec make.version "$(make --version | head -1)"
rec kbuild.pipe_lines "$(grep -c -- '-pipe' "$CORPUS/Makefile"; true)"   # -pipe would make cc1 and as overlap (D2: read from the run)

# ---- builds (D4, D5) ----------------------------------------------------
# an unmeasured warm-up build on the harness CPUs, then clean: the host tools (scripts/, objtool) stay built, so the
# three measured builds compile the same object set (dry run 1: the first build carried 37 extra host-tool jobs)
# shellcheck disable=SC2086
unmeasured make -C "$CORPUS" -j3 $BUILD_TARGETS > "$OUT/warmup.log" 2>&1; rec build.warmup.rc "$?"
unmeasured make -C "$CORPUS" clean > /dev/null 2>&1
# shellcheck disable=SC2086
phase build-j8-warm -- make -C "$CORPUS" -j8 $BUILD_TARGETS
unmeasured make -C "$CORPUS" clean > /dev/null 2>&1
sync; sudo sysctl -q vm.drop_caches=3
# shellcheck disable=SC2086
phase build-j8-cold -- make -C "$CORPUS" -j8 $BUILD_TARGETS
unmeasured make -C "$CORPUS" clean > /dev/null 2>&1
# shellcheck disable=SC2086
phase build-j1-warm -- make -C "$CORPUS" -j1 $BUILD_TARGETS

# ---- dkms structural check (D6): the module rebuilt under the pin, dkms's own -j$(nproc) = -j1 ----
if [ -n "$V4L2_VER" ]; then
  unmeasured sudo dkms remove "v4l2loopback/$V4L2_VER" --all > "$OUT/dkms.remove.log" 2>&1; rec dkms.remove.rc "$?"
  phase dkms -- sudo dkms build "v4l2loopback/$V4L2_VER" -k "$(uname -r)"
  sudo find /var/lib/dkms/v4l2loopback -name make.log -exec cp {} "$OUT/dkms.make.log" \; 2>/dev/null; sudo chown "$(id -u)" "$OUT/dkms.make.log" 2>/dev/null
fi

# ---- batch programs (D7) ------------------------------------------------
sudo freshclam > "$OUT/freshclam.log" 2>&1; rec freshclam.rc "$?"
rec clamav.db "$(clamscan --version 2>/dev/null)"; ls -la /var/lib/clamav > "$OUT/clamav.db.txt" 2>&1
phase clamscan -- clamscan -r -i "$CORPUS/$CLAM_DIR"

unmeasured ffmpeg -y -loglevel error -f lavfi -i "testsrc2=size=1280x720:rate=30" -f lavfi -i "sine=frequency=440" \
  -t "$CLIP_S" -c:v libx264 -preset ultrafast -c:a aac "$WORK/clip.mp4" > "$OUT/clip.log" 2>&1; rec clip.rc "$?"
phase ffmpeg -- ffmpeg -y -i "$WORK/clip.mp4" -c:v libx264 -preset medium -crf 23 -c:a aac "$WORK/ffmpeg-out.mp4"
grep -m3 -E "using cpu capabilities|threads|frame=" "$OUT/cmd.ffmpeg.log" > "$OUT/ffmpeg.threads.txt" 2>/dev/null
if command -v HandBrakeCLI > /dev/null 2>&1; then
  phase handbrake -- HandBrakeCLI -i "$WORK/clip.mp4" -o "$WORK/hb-out.mp4" --preset "Fast 720p30"
fi
phase train -- python3 "$HERE/train.py" "$TRAIN_STEPS" --record "$OUT/train.json"

# tracker full rescan: a fresh XDG data home over a corpus copy; the miner runs until tracker3 reports it idle or the cap
# each XDG special directory gets its own path: a path in both the miner's recursive and single lists is dropped
# from the recursive one (dry run 2: Documents mapped for every special dir was indexed one level deep, 0 files)
TH=/tmp/tracker-home; rm -rf "$TH"; mkdir -p "$TH/Documents" "$TH/Desktop" "$TH/Downloads" "$TH/Music" "$TH/Pictures" "$TH/Videos" "$TH/.config"
cp -r "$CORPUS/Documentation" "$TH/Documents/corpus" 2>/dev/null
printf 'XDG_DOCUMENTS_DIR="$HOME/Documents"\nXDG_DESKTOP_DIR="$HOME/Desktop"\nXDG_DOWNLOAD_DIR="$HOME/Downloads"\nXDG_MUSIC_DIR="$HOME/Music"\nXDG_PICTURES_DIR="$HOME/Pictures"\nXDG_VIDEOS_DIR="$HOME/Videos"\n' > "$TH/.config/user-dirs.dirs"
rec tracker.corpus_files "$(find "$TH/Documents/corpus" -type f | wc -l)"
MINER="$(ls /usr/libexec/tracker-miner-fs-3 /usr/libexec/tracker-miner-fs 2>/dev/null | head -1)"; rec tracker.miner "${MINER:-none}"
if [ -n "$MINER" ]; then
  cat > "$WORK/tracker-run.sh" <<EOF
export HOME=$TH XDG_DATA_HOME=$TH/.local/share XDG_CONFIG_HOME=$TH/.config XDG_CACHE_HOME=$TH/.cache
"$MINER" > "$OUT/tracker.miner.log" 2>&1 &
M=\$!
taskset -cp $MEAS_HARNESS_CPUS \$\$ > /dev/null 2>&1   # the poll loop leaves the measured CPU; the miner keeps it
end=\$((\$(date +%s) + $TRACKER_S)); idle=0
while [ \$(date +%s) -lt \$end ]; do
  sleep 5
  st=\$(tracker3 status 2>/dev/null)
  if echo "\$st" | grep -qi "idle" && ! echo "\$st" | grep -q "indexed: 0 files"; then idle=\$((idle + 1)); else idle=0; fi
  [ \$idle -ge 3 ] && break
done
tracker3 status > "$OUT/tracker.status.txt" 2>&1
kill -INT \$M 2>/dev/null; sleep 2; kill -9 \$M 2>/dev/null; wait \$M 2>/dev/null
echo "idle_polls=\$idle elapsed=\$((\$(date +%s) - end + $TRACKER_S))"
EOF
  phase tracker -- dbus-run-session -- bash "$WORK/tracker-run.sh"
fi

rec finished_utc "$(date -u +%FT%TZ)"
sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
finish_report
