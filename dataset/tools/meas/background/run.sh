#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|probe|full> — one job of the 9.7 background campaign
# (research-slice changelog D2–D15; method
# _dev/research/jioh/task-9.7-background-io/campaign/method.md §1–§4).
#
# One job per program per repeat, its phases in the method's order (D14 (4)):
#   borg      borg-first-warm, borg-repeat-warm, borg-first-cold, borg-repeat-cold
#   7z        7z-mmt8-warm, 7z-mmt1-warm, 7z-mmt8-cold
#   steamcmd  steam-fresh-shaped, steam-fresh-untraced, steam-fresh-unshaped,
#             steam-update-shaped (only with a branch to stage)
# Every measured phase is one command pinned to the measured CPU (pin.sh,
# phase.sh MEAS_PIN=load), observed over the whole phase from the harness CPUs
# by `perf sched record -a` — with the exec rows that name each process's
# program — and a taskstats listener registered on the measured CPU. The traced
# SteamCMD phases add `perf trace record` of the method's calls on the measured
# CPU, filtered by call number in both the 64-bit and the i386 tables: SteamCMD
# is a 32-bit program (D4; nettrace.py). Setup — the set fetched, extracted and
# verified, warmed, changed and restored, the older build staged — runs on the
# harness CPUs. Dry mode: the 100 MB subset for borg and 7z plus one timed pass
# of the archetype's phase on the full set; for SteamCMD the smallest candidate
# app and the staging probe on the campaign's app (D12). Nothing here fails the
# job: every step records its rc and the next phase runs.
#
# Settings (the trigger file, through the workflow): MEAS_CPU_MODEL (the machine
# gate), MEAS_WORK_ROOT (auto | / | /mnt), MEAS_STEAM_APP, MEAS_STEAM_UPDATE_FROM
# (the branch staged before the update phase; empty: no update phase),
# MEAS_STEAM_UPDATE_TO (app_update's -beta argument back to the public build),
# MEAS_STEAM_DRY_APP (smallest | an app id), MEAS_ARCHIVER_SET (10gb | 1gb: the
# 7-Zip phases' input, method §3 "Dry mode").
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEAS="$(cd "$HERE/.." && pwd)"
source "$MEAS/probe/common.sh"        # OUT, KV, rec, finish_report
source "$MEAS/pin.sh"
pin_self_harness
APP="$1"; REPEAT="$2"; MODE="${3:-full}"
PH="$MEAS/phase.sh $OUT/phases.jsonl"
export MEAS_PIN=load
STEAM_APP="${MEAS_STEAM_APP:-232250}"
UPDATE_FROM="${MEAS_STEAM_UPDATE_FROM:-}"; UPDATE_TO="${MEAS_STEAM_UPDATE_TO:-public}"
DRY_APP="${MEAS_STEAM_DRY_APP:-smallest}"; ARCH_SET="${MEAS_ARCHIVER_SET:-10gb}"
CANDIDATES="90 232330 4020 244310 232250"   # the anonymous Linux dedicated servers the S4-16 record quotes from Valve's list
RATE_MBIT=121.0                             # D11
TBF_LATENCY=70ms                            # design: the queue bound of tc-tbf(8)'s example (S4-14)
export BORG_PASSPHRASE="meas-9.7"           # design: repokey's passphrase, from the environment (§2 "Builds")

rec family background; rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec settings.work_root "${MEAS_WORK_ROOT:-auto}"; rec settings.steam_app "$STEAM_APP"; rec settings.steam_update_from "$UPDATE_FROM"
rec settings.steam_update_to "$UPDATE_TO"; rec settings.steam_dry_app "$DRY_APP"; rec settings.archiver_set "$ARCH_SET"
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$MEAS/runner_spec.py" > "$OUT/spec.json"
# same-machine repeats: a job that drew another CPU model stops here, recorded, before any install or measurement
source "$MEAS/machine_gate.sh"
rec machine.model "$(machine_model)"; rec machine.wanted "${MEAS_CPU_MODEL:-}"
if ! machine_gate "${MEAS_CPU_MODEL:-}"; then
  rec gate wrong-machine; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "machine gate: wanted '${MEAS_CPU_MODEL}', drew '$(machine_model)' — stopping before any measurement" >&2
  exit 0
fi
rec gate open
python3 -c 'import time,json; print(json.dumps({"mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}))' > "$OUT/clock.json"
rec kernel "$(uname -r)"
rec shape.rate_mbit "$RATE_MBIT"; rec shape.latency "$TBF_LATENCY"

# ---- the machine as recorded (§1) ---------------------------------------------
df -B1 --output=source,target,fstype,size,avail / /mnt > "$OUT/df.txt" 2>&1
lsblk -o NAME,ROTA,SIZE,MODEL,TRAN,MOUNTPOINTS > "$OUT/lsblk.txt" 2>&1
for d in /sys/block/*; do [ -f "$d/queue/rotational" ] && rec "disk.rotational.$(basename "$d")" "$(cat "$d/queue/rotational")"; done
CFG="/boot/config-$(uname -r)"
[ -f "$CFG" ] && grep -E '^CONFIG_(TASKSTATS|TASK_DELAY_ACCT|TASK_IO_ACCOUNTING|TASK_XACCT|SCHEDSTATS|HZ|NET_SCH_TBF|IFB|NET_SCH_INGRESS|NET_ACT_MIRRED|NET_CLS_U32)=' "$CFG" > "$OUT/kconfig.txt"
HZ="$(sed -n 's/^CONFIG_HZ=//p' "$OUT/kconfig.txt" 2>/dev/null)"; HZ="${HZ:-1000}"; rec kernel.hz "$HZ"
IFACE="$(ip -o route get 1.1.1.1 2>/dev/null | sed -n 's/.* dev \([^ ]*\).*/\1/p')"; rec net.iface "$IFACE"
ip -s link > "$OUT/ip.link.before.txt" 2>&1
netc() { cat "/sys/class/net/$IFACE/statistics/$1" 2>/dev/null || echo 0; }

# the work directory: whichever of / and /mnt the setting names; auto takes the one with more free space (§2 "Disk")
A_ROOT="$(df -B1 --output=avail / | tail -1 | tr -d ' ')"; A_MNT="$(df -B1 --output=avail /mnt 2>/dev/null | tail -1 | tr -d ' ')"
rec disk.avail.root "$A_ROOT"; rec disk.avail.mnt "${A_MNT:-}"
case "${MEAS_WORK_ROOT:-auto}" in
  /) R=/ ;; /mnt) R=/mnt ;;
  *) if [ -n "${A_MNT:-}" ] && [ "$A_MNT" -gt "$A_ROOT" ]; then R=/mnt; else R=/; fi ;;
esac
WORK="${R%/}/meas-work"; sudo mkdir -p "$WORK"; sudo chown "$(id -u):$(id -g)" "$WORK"
rec work.root "$R"; rec work.dir "$WORK"; rec work.device "$(df --output=source "$WORK" | tail -1)"

# ---- packages ------------------------------------------------------------------
sudo apt-get update > "$OUT/apt.update.log" 2>&1; rec apt.update.rc "$?"
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" gcc linux-libc-dev > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
case "$APP" in
  borg) sudo apt-get install -y --no-install-recommends borgbackup zpaq util-linux-extra > "$OUT/apt.app.log" 2>&1; rec apt.app.rc "$?"
        rec borg.version "$(borg --version 2>&1 | head -1)" ;;
  7z)   sudo apt-get install -y --no-install-recommends 7zip zpaq util-linux-extra > "$OUT/apt.app.log" 2>&1; rec apt.app.rc "$?"
        Z="$(command -v 7z || command -v 7zz)"; rec 7z.binary "$Z"
        "$Z" i > "$OUT/7z.info.txt" 2>&1; rec 7z.version "$(grep -m1 '7-Zip' "$OUT/7z.info.txt")" ;;
  steamcmd)
        # multiverse, i386 multiarch, the licence preseeded for debconf; run as the runner user (§2 "SteamCMD"; S4-16)
        sudo dpkg --add-architecture i386
        sudo add-apt-repository -y multiverse > "$OUT/apt.multiverse.log" 2>&1; rec apt.multiverse.rc "$?"
        for owner in steam steamcmd; do
          echo "$owner steam/question select I AGREE" | sudo debconf-set-selections
          echo "$owner steam/license note ''" | sudo debconf-set-selections
        done
        sudo apt-get update > "$OUT/apt.update2.log" 2>&1
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y steamcmd > "$OUT/apt.app.log" 2>&1; rec apt.app.rc "$?"
        STEAMCMD="$( [ -x /usr/games/steamcmd ] && echo /usr/games/steamcmd || command -v steamcmd)"; rec steamcmd.binary "$STEAMCMD"
        rec steamcmd.package "$(dpkg-query -W -f '${Version}' steamcmd 2>/dev/null)" ;;
esac
rec zpaq.version "$(zpaq 2>&1 | head -1)"
rec util-linux.version "$(fincore --version 2>&1 | head -1)"
rec python.version "$(python3 --version 2>&1)"

# ---- instruments ---------------------------------------------------------------
gcc -O2 -Wall -o "$WORK/taskstats_listen" "$MEAS/build/taskstats_listen.c" > "$OUT/gcc.listener.log" 2>&1; rec listener.build.rc "$?"
sudo sysctl -w kernel.task_delayacct=1 > /dev/null 2>&1; rec sysctl.task_delayacct "$(cat /proc/sys/kernel/task_delayacct 2>/dev/null || echo missing)"
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null 2>&1; rec sysctl.perf_event_paranoid "$(cat /proc/sys/kernel/perf_event_paranoid)"
SYSCALL_FILTER="$(python3 "$HERE/nettrace.py" filter)"; rec trace.filter "$SYSCALL_FILTER"

listener_start() { # listener_start <phase>
  sudo taskset -c "$MEAS_HARNESS_CPUS" "$WORK/taskstats_listen" -m "$MEAS_CPU" -o "$OUT/taskstats.$1.tsv" 2> "$OUT/taskstats.$1.err" &
  LISTENER_PID=$!; sleep 1
}
listener_stop() { # listener_stop <phase>
  sudo kill -INT "$LISTENER_PID" 2>/dev/null; wait "$LISTENER_PID" 2>/dev/null
  rec "taskstats.$1.rows" "$(grep -vc '^#\|^recv_mono' "$OUT/taskstats.$1.tsv" 2>/dev/null; true)"
  rec "taskstats.$1.enobufs" "$(grep -c ENOBUFS "$OUT/taskstats.$1.err" 2>/dev/null; true)"
}
listener_start smoke; taskset -c "$MEAS_CPU" sh -c 'true'; sleep 1; listener_stop smoke

edge() { python3 -c 'import time,json,sys; print(json.dumps({"phase": sys.argv[1], "edge": sys.argv[2], "mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}))' "$1" "$2" >> "$OUT/edges.jsonl"; }
elf_class() { python3 -c '
import sys
try:
    b = open(sys.argv[1], "rb").read(5)
except OSError:
    print("missing"); sys.exit()
print("ELF32" if b[:4] == b"\x7fELF" and b[4:5] == b"\x01" else "ELF64" if b[:4] == b"\x7fELF" else "script" if b[:2] == b"#!" else "other")' "$1"; }

# phase <name> -- <cmd...>: the instruments over the whole phase, the command pinned on the measured CPU; TRACE=1 adds
# perf trace record (the method's calls; nettrace.py) on the measured CPU
phase() {
  local name="$1"; shift; [ "${1:-}" = "--" ] && shift
  local tpid="" keep=0
  [ "$MODE" = dry ] && case "$name" in *-fullset) ;; *) keep=1 ;; esac
  edge "$name" start
  listener_start "$name"
  sudo taskset -c "$MEAS_HARNESS_CPUS" perf sched record -k CLOCK_MONOTONIC -a -e sched:sched_process_exec -o "$OUT/perf.$name.data" > "$OUT/perf.$name.log" 2>&1 &
  local perf_pid=$!
  if [ "${TRACE:-0}" = 1 ]; then
    sudo taskset -c "$MEAS_HARNESS_CPUS" perf trace record --filter "$SYSCALL_FILTER" -k CLOCK_MONOTONIC -C "$MEAS_CPU" -o "$OUT/trace.$name.data" > "$OUT/trace.$name.log" 2>&1 &
    tpid=$!
  fi
  sleep 2
  if [ -n "$tpid" ] && ! kill -0 "$tpid" 2>/dev/null; then   # perf trace record refused: the same events through perf record
    rec "trace.$name.fallback" perf-record
    sudo taskset -c "$MEAS_HARNESS_CPUS" perf record -e raw_syscalls:sys_enter,raw_syscalls:sys_exit --filter "$SYSCALL_FILTER" -R -m 1024 -c 1 \
      -k CLOCK_MONOTONIC -C "$MEAS_CPU" -o "$OUT/trace.$name.data" >> "$OUT/trace.$name.log" 2>&1 &
    tpid=$!; sleep 2
  fi
  $PH "$name" -- "$@" > "$OUT/cmd.$name.log" 2>&1
  sleep 2
  if [ -n "$tpid" ]; then sudo kill -INT "$tpid" 2>/dev/null; wait "$tpid" 2>/dev/null; rec "perf.$name.trace.record.rc" "$?"; fi
  sudo kill -INT "$perf_pid" 2>/dev/null; wait "$perf_pid" 2>/dev/null; rec "perf.$name.record.rc" "$?"
  listener_stop "$name"
  edge "$name" end
  sudo perf sched timehist --state -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
  rec "perf.$name.timehist.rc" "${PIPESTATUS[0]}"
  rec "perf.$name.timehist.rows" "$(gzip -dc "$OUT/perf.$name.timehist.txt.gz" | wc -l)"
  sudo perf sched timehist -w -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | grep -E "awakened|wakeup|\bwaker\b" | gzip > "$OUT/perf.$name.wakeups.txt.gz"
  rec "perf.$name.wakeups.rows" "$(gzip -dc "$OUT/perf.$name.wakeups.txt.gz" | wc -l)"
  sudo perf script -i "$OUT/perf.$name.data" -F time,event,trace 2>> "$OUT/perf.$name.log" \
    | grep -E "sched_process_fork|sched_wakeup_new|sched_process_exit|sched_process_exec" | gzip > "$OUT/perf.$name.forks.txt.gz"
  rec "perf.$name.forks.rows" "$(gzip -dc "$OUT/perf.$name.forks.txt.gz" | wc -l)"
  gzip -dc "$OUT/perf.$name.forks.txt.gz" | sed -n 's/.*sched_process_exec: filename=\(.*\) pid=[0-9]* old_pid=[0-9]*.*/\1/p' | sort -u \
    | while read -r f; do printf '%s\t%s\n' "$f" "$(elf_class "$f")"; done > "$OUT/execs.$name.tsv"
  rec "perf.$name.data_bytes" "$(stat -c %s "$OUT/perf.$name.data" 2>/dev/null || echo 0)"
  if [ -n "$tpid" ]; then
    sudo perf script -i "$OUT/trace.$name.data" --ns -F pid,tid,time,event,trace 2>> "$OUT/trace.$name.log" | gzip > "$OUT/trace.$name.txt.gz"
    rec "trace.$name.script.rc" "${PIPESTATUS[0]}"
    rec "trace.$name.rows" "$(gzip -dc "$OUT/trace.$name.txt.gz" | wc -l)"
    rec "trace.$name.data_bytes" "$(stat -c %s "$OUT/trace.$name.data" 2>/dev/null || echo 0)"
    rec "trace.$name.lost" "$(grep -ioE 'lost [0-9]+ (chunks|events|samples)' "$OUT/trace.$name.log" | tr '\n' ' ')"
  fi
  sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
  if [ "$keep" = 1 ]; then gzip -f "$OUT/perf.$name.data"; [ -n "$tpid" ] && gzip -f "$OUT/trace.$name.data"
  else rm -f "$OUT/perf.$name.data" "$OUT/trace.$name.data"; fi
}
unmeasured() { pin_harness "$@"; }   # setup on the harness CPUs, no instruments

# ---- the file set (§2; D7) -----------------------------------------------------
set_field() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))["sets"][sys.argv[2]][sys.argv[3]]; print(" ".join(v) if isinstance(v, list) else ("" if v is None else v))' "$HERE/inputs.json" "$1" "$2"; }
pin_state() { [ -z "$1" ] && echo unpinned || { [ "$1" = "$2" ] && echo ok || echo mismatch; }; }

fetch_set() {   # fetch_set <name> <record prefix>: fetched, checked, extracted on the harness CPUs, manifest verified; sets SET
  local name="$1" p="$2" url ok=0 dest="$WORK/sets/$name" arc="$WORK/$name.zpaq" t0
  for url in $(set_field "$name" urls); do
    t0=$(date +%s)
    if unmeasured wget -q --tries=5 --waitretry=15 --retry-connrefused -O "$arc" "$url"; then ok=1; rec "$p.url" "$url"; rec "$p.fetch_s" "$(( $(date +%s) - t0 ))"; break; fi
  done
  rec "$p.fetch.ok" "$ok"
  rec "$p.archive_bytes" "$(stat -c %s "$arc" 2>/dev/null || echo 0)"
  local sha; sha="$(sha256sum "$arc" 2>/dev/null | cut -d' ' -f1)"
  rec "$p.archive_sha256" "$sha"; rec "$p.archive_pin" "$(pin_state "$(set_field "$name" archive_sha256)" "$sha")"
  rm -rf "$dest"; mkdir -p "$dest"
  t0=$(date +%s)
  (cd "$dest" && unmeasured zpaq x "$arc" > "$OUT/zpaq.$name.log" 2>&1); rec "$p.extract.rc" "$?"; rec "$p.extract_s" "$(( $(date +%s) - t0 ))"
  rm -f "$arc"
  local tops; tops="$(ls -A "$dest")"   # zpaq restores the stored tree: 10gb/ for the full set
  if [ "$(printf '%s\n' "$tops" | wc -l)" = 1 ] && [ -d "$dest/$tops" ]; then SET="$dest/$tops"; else SET="$dest"; fi
  rec "$p.dir" "$SET"
  SET_MANIFEST="$OUT/manifest-$name.tsv.gz"
  unmeasured python3 "$HERE/fileset.py" manifest "$SET" "$SET_MANIFEST" > "$OUT/manifest-$name.kv" 2>&1
  SET_DIGEST="$(sed -n 's/^manifest_sha256=//p' "$OUT/manifest-$name.kv")"
  rec "$p.manifest_sha256" "$SET_DIGEST"; rec "$p.manifest_pin" "$(pin_state "$(set_field "$name" manifest_sha256)" "$SET_DIGEST")"
  python3 "$HERE/fileset.py" setcheck "$SET_MANIFEST" | while IFS='=' read -r k v; do rec "$p.$k" "$v"; done
  df -B1 --output=target,avail "$WORK" > "$OUT/df.$name.txt" 2>&1
}
verify_set() {   # verify_set <label>: the tree against this job's manifest
  unmeasured python3 "$HERE/fileset.py" verify "$SET" "$SET_MANIFEST" > "$OUT/verify.$1.kv" 2>&1
  local rc=$?; rec "set.verify.$1" "$( [ "$rc" = 0 ] && echo ok || echo mismatch)"
}
cached() { rec "cache.$1.fraction" "$(find "$SET" -type f -print0 | xargs -0 fincore -b -n -r -o RES,SIZE 2>/dev/null | awk '{r += $1; s += $2} END {if (s > 0) printf "%.4f", r / s}')"; }
warm() { unmeasured sh -c 'find "$1" -type f -exec cat {} + > /dev/null' _ "$SET"; cached "$1"; }   # warm <phase> (§3)
cold() { sync; sudo sysctl -q vm.drop_caches=3; cached "$1"; sync; sudo sysctl -q vm.drop_caches=3; }   # the second drop undoes fincore's metadata reads
change_apply() {   # change_apply <label>: the repeat backup's change set (D6), originals kept aside
  rm -rf "$WORK/stash"; mkdir -p "$WORK/stash"
  unmeasured python3 "$HERE/fileset.py" change "$SET" "$WORK/stash" "$OUT/change.$1.json" > "$OUT/change.$1.kv" 2>&1; rec "change.$1.rc" "$?"
  while IFS='=' read -r k v; do rec "change.$1.$k" "$v"; done < "$OUT/change.$1.kv"
  rec "change.$1.sha256" "$(sha256sum "$OUT/change.$1.json" | cut -d' ' -f1)"
}
change_restore() {   # change_restore <label>: originals back, new files removed, the tree verified
  unmeasured python3 "$HERE/fileset.py" restore "$SET" "$WORK/stash" "$OUT/change.$1.json" > /dev/null 2>&1; rec "change.$1.restore.rc" "$?"
  rm -rf "$WORK/stash"; verify_set "restored-$1"
}

# ---- borg (D6, D8, D9) ---------------------------------------------------------
REPO="$WORK/borg-repo"; export BORG_BASE_DIR="$WORK/borg-home"
borg_new_repo() {   # borg_new_repo <label>: a repository just made by `borg init` on the harness CPUs; the old one and its cache gone
  rm -rf "$REPO" "$BORG_BASE_DIR"; mkdir -p "$BORG_BASE_DIR"
  unmeasured borg init --encryption=repokey "$REPO" > "$OUT/borg.init.$1.log" 2>&1; rec "borg.init.$1.rc" "$?"
}
borg_after() { rec "borg.$1.repo_bytes" "$(du -sb "$REPO" 2>/dev/null | cut -f1)"; }
borg_phases() {
  borg_new_repo first-warm
  warm borg-first-warm;  phase borg-first-warm  -- borg create "$REPO::first" "$SET";  borg_after borg-first-warm
  change_apply warm
  warm borg-repeat-warm; phase borg-repeat-warm -- borg create "$REPO::repeat" "$SET"; borg_after borg-repeat-warm
  change_restore warm
  borg_new_repo first-cold
  cold borg-first-cold;  phase borg-first-cold  -- borg create "$REPO::first" "$SET";  borg_after borg-first-cold
  change_apply cold
  cold borg-repeat-cold; phase borg-repeat-cold -- borg create "$REPO::repeat" "$SET"; borg_after borg-repeat-cold
  change_restore cold
  rec change.identical "$( [ "$(sha256sum < "$OUT/change.warm.json")" = "$(sha256sum < "$OUT/change.cold.json")" ] && echo 1 || echo 0)"
  rm -rf "$REPO" "$BORG_BASE_DIR"
}

# ---- 7-Zip (D8, D9, D15 (a)) -----------------------------------------------------
ARCHIVE="$WORK/archive.7z"
z_phase() {   # z_phase <name> <threads>
  rm -f "$ARCHIVE"; phase "$1" -- "$Z" a "-mmt$2" "$ARCHIVE" "$SET"
  rec "7z.$1.archive_bytes" "$(stat -c %s "$ARCHIVE" 2>/dev/null || echo 0)"; rm -f "$ARCHIVE"
}
z_phases() {
  warm 7z-mmt8-warm; z_phase 7z-mmt8-warm 8
  warm 7z-mmt1-warm; z_phase 7z-mmt1-warm 1
  cold 7z-mmt8-cold; z_phase 7z-mmt8-cold 8
}

# ---- SteamCMD (D4, D10–D12) -------------------------------------------------------
INSTALL="$WORK/steam-install"; SHAPED=0
BURST=$(( (121000000 / 8 + HZ - 1) / HZ ))   # bytes: the rate over HZ, the least tc-tbf(8) allows at this rate (§2 "The shaped link")
rec shape.burst_bytes "$BURST"
shape_on() {   # ingress on the runner's interface redirected to ifb0, a tbf root at the D11 rate
  sudo modprobe ifb numifbs=1 > /dev/null 2>&1; sudo ip link add ifb0 type ifb > /dev/null 2>&1; sudo ip link set ifb0 up
  sudo tc qdisc add dev "$IFACE" handle ffff: ingress 2>> "$OUT/tc.log"
  sudo tc filter add dev "$IFACE" parent ffff: protocol all u32 match u32 0 0 action mirred egress redirect dev ifb0 2>> "$OUT/tc.log"
  if sudo tc qdisc add dev ifb0 root tbf rate "${RATE_MBIT}mbit" burst "$BURST" latency "$TBF_LATENCY" 2>> "$OUT/tc.log"; then SHAPED=1; else SHAPED=0; fi
}
shape_off() { sudo tc qdisc del dev "$IFACE" ingress 2>/dev/null; sudo tc qdisc del dev ifb0 root 2>/dev/null; SHAPED=0; }
steam_logs_dir() {
  local f; f="$(find "$HOME/.steam" "$HOME/Steam" "$HOME/.local/share/Steam" -maxdepth 5 -name content_log.txt 2>/dev/null | head -1)"
  if [ -n "$f" ]; then dirname "$f"; else find "$HOME/.steam" "$HOME/Steam" -maxdepth 4 -type d -name logs 2>/dev/null | head -1; fi
}
logs_mark() {
  local d f; d="$(steam_logs_dir)"; : > "$WORK/logmark"
  [ -n "$d" ] && for f in "$d"/*; do [ -f "$f" ] && echo "$(basename "$f") $(stat -c %s "$f")" >> "$WORK/logmark"; done
}
logs_take() {   # logs_take <phase>: what SteamCMD's logs gained during the phase
  local d f b s; d="$(steam_logs_dir)"; mkdir -p "$OUT/steamlogs/$1"; [ -z "$d" ] && return
  for f in "$d"/*; do
    [ -f "$f" ] || continue; b="$(basename "$f")"; s="$(awk -v b="$b" '$1 == b {print $2}' "$WORK/logmark")"
    tail -c +"$(( ${s:-0} + 1 ))" "$f" > "$OUT/steamlogs/$1/$b"
  done
}
buildid_of() { sed -n 's/.*"buildid"[[:space:]]*"\([0-9]*\)".*/\1/p' "$1/steamapps/appmanifest_$2.acf" 2>/dev/null | head -1; }
appinfo() {   # appinfo <app>: printed twice (a first print may be stale), summarised
  [ -s "$OUT/appinfo.$1.txt" ] && return
  unmeasured "$STEAMCMD" +login anonymous +app_info_update 1 +app_info_print "$1" +app_info_print "$1" +quit > "$OUT/appinfo.$1.txt" 2>&1
  python3 "$HERE/appinfo.py" summary "$1" "$OUT/appinfo.$1.txt" | while IFS='=' read -r k v; do rec "steam.appinfo.$1.$k" "$v"; done
}
steam_phase() {   # steam_phase <name> <trace 0|1> <fresh|staged> <app> [app_update args]
  local name="$1" tr="$2" state="$3" app="$4"; shift 4
  if [ "$state" = fresh ]; then rm -rf "$INSTALL"; mkdir -p "$INSTALL"; fi
  find "$HOME/.steam" "$HOME/Steam" -maxdepth 5 -type d -name depotcache -prune -exec rm -rf {} + 2>/dev/null   # every phase fetches its manifests
  local rx0 tx0; rx0="$(netc rx_bytes)"; tx0="$(netc tx_bytes)"
  logs_mark
  TRACE="$tr" phase "$name" -- "$STEAMCMD" +force_install_dir "$INSTALL" +login anonymous +app_update "$app" "$@" +quit
  rec "net.$name.rx_bytes" "$(( $(netc rx_bytes) - rx0 ))"; rec "net.$name.tx_bytes" "$(( $(netc tx_bytes) - tx0 ))"
  rec "shape.$name" "$SHAPED"
  if [ "$SHAPED" = 1 ]; then
    tc -s qdisc show dev ifb0 > "$OUT/tc.$name.txt" 2>&1
    rec "tc.$name.stats" "$(grep -m1 -oE 'Sent [0-9]+ bytes [0-9]+ pkt \(dropped [0-9]+, overlimits [0-9]+' "$OUT/tc.$name.txt")"
  fi
  logs_take "$name"
  rec "steam.$name.success" "$(grep -c "Success! App '$app' fully installed" "$OUT/cmd.$name.log")"
  rec "steam.$name.buildid" "$(buildid_of "$INSTALL" "$app")"
  rec "steam.$name.install_bytes" "$(du -sb "$INSTALL" 2>/dev/null | cut -f1)"
  rm -rf "$INSTALL"
}
steam_phases() {   # steam_phases <app> <branch to stage or empty> <-beta argument back to public>
  local app="$1" from="$2" to="$3"
  shape_on; steam_phase steam-fresh-shaped 1 fresh "$app"; shape_off
  shape_on; steam_phase steam-fresh-untraced 0 fresh "$app"; shape_off
  steam_phase steam-fresh-unshaped 1 fresh "$app"
  if [ -n "$from" ]; then   # D12: an older public build staged on the harness CPUs, then updated to the public build
    rm -rf "$INSTALL"; mkdir -p "$INSTALL"
    unmeasured "$STEAMCMD" +force_install_dir "$INSTALL" +login anonymous +app_update "$app" -beta "$from" +quit > "$OUT/steam.stage.log" 2>&1
    rec steam.stage.rc "$?"; rec steam.stage.from "$from"; rec steam.stage.buildid "$(buildid_of "$INSTALL" "$app")"
    shape_on; steam_phase steam-update-shaped 1 staged "$app" -beta "$to"; shape_off
  else
    rec steam.update_phase none
  fi
}
stage_probe() {   # stage_probe <app>: D12 — does the nearest older public build install anonymously, and then update?
  local app="$1" dir="$WORK/steam-probe" from want pub got to
  appinfo "$app"
  from="$(python3 "$HERE/appinfo.py" older "$app" "$OUT/appinfo.$app.txt")"; rec steam.probe.app "$app"; rec steam.probe.from "$from"
  if [ -z "$from" ]; then rec steam.probe.result no-older-branch; return; fi
  want="$(python3 "$HERE/appinfo.py" buildid "$app" "$OUT/appinfo.$app.txt" "$from")"
  pub="$(python3 "$HERE/appinfo.py" buildid "$app" "$OUT/appinfo.$app.txt" public)"
  rm -rf "$dir"; mkdir -p "$dir"
  unmeasured "$STEAMCMD" +force_install_dir "$dir" +login anonymous +app_update "$app" -beta "$from" +quit > "$OUT/steam.probe.stage.log" 2>&1
  rec steam.probe.stage.rc "$?"; got="$(buildid_of "$dir" "$app")"; rec steam.probe.staged_buildid "$got"; rec steam.probe.branch_buildid "$want"
  rec steam.probe.install_bytes "$(du -sb "$dir" 2>/dev/null | cut -f1)"
  rec steam.probe.result staging-failed
  if [ -n "$got" ] && [ "$got" = "$want" ]; then
    for to in public none; do
      unmeasured "$STEAMCMD" +force_install_dir "$dir" +login anonymous +app_update "$app" -beta "$to" +quit > "$OUT/steam.probe.update-$to.log" 2>&1
      rec "steam.probe.update.$to.rc" "$?"; got="$(buildid_of "$dir" "$app")"; rec "steam.probe.update.$to.buildid" "$got"
      if [ "$got" = "$pub" ]; then rec steam.probe.result ok; rec steam.probe.update_to "$to"; break; fi
      rec steam.probe.result update-failed
    done
  fi
  rm -rf "$dir"
}

# ---- the job ----------------------------------------------------------------------
case "$APP" in
  borg)
    if [ "$MODE" = dry ]; then
      fetch_set 100mb set; borg_phases; rm -rf "$WORK/sets/100mb"
      fetch_set 10gb fullset   # one timed pass on the full set, for disk and time (§3 "Dry mode")
      borg_new_repo fullset; warm borg-first-warm-fullset; phase borg-first-warm-fullset -- borg create "$REPO::first" "$SET"
      borg_after borg-first-warm-fullset; rm -rf "$REPO" "$BORG_BASE_DIR"
    else
      fetch_set 10gb set; borg_phases
    fi ;;
  7z)
    if [ "$MODE" = dry ]; then
      fetch_set 100mb set; z_phases; rm -rf "$WORK/sets/100mb"
      fetch_set 10gb fullset; warm 7z-mmt8-warm-fullset; z_phase 7z-mmt8-warm-fullset 8
    else
      fetch_set "$ARCH_SET" set; z_phases
    fi ;;
  steamcmd)
    rm -rf "$HOME/.steam/steamcmd/logs" 2>/dev/null
    unmeasured "$STEAMCMD" +quit > "$OUT/steamcmd.selfupdate.log" 2>&1; rec steamcmd.selfupdate.rc "$?"   # SteamCMD's own update, once
    rec steamcmd.version "$(grep -oE 'version [0-9]+' "$OUT/steamcmd.selfupdate.log" | tail -1)"
    if [ "$MODE" = dry ]; then
      for a in $CANDIDATES; do appinfo "$a"; done
      if [ "$DRY_APP" = smallest ]; then RUN_APP="$(python3 "$HERE/appinfo.py" smallest $(for a in $CANDIDATES; do echo "$OUT/appinfo.$a.txt"; done))"; else RUN_APP="$DRY_APP"; fi
      RUN_APP="${RUN_APP:-$STEAM_APP}"   # no candidate's size could be read: the campaign's app
      FROM="$(python3 "$HERE/appinfo.py" older "$RUN_APP" "$OUT/appinfo.$RUN_APP.txt")"
      rec steam.app "$RUN_APP"; steam_phases "$RUN_APP" "$FROM" public
      stage_probe "$STEAM_APP"
    else
      appinfo "$STEAM_APP"; RUN_APP="$STEAM_APP"; rec steam.app "$RUN_APP"
      steam_phases "$RUN_APP" "$UPDATE_FROM" "$UPDATE_TO"
    fi
    rec steam.buildid "$(sed -n 's/^steam\.steam-fresh-shaped\.buildid=//p' "$KV" | tail -1)"
    df -B1 --output=target,avail "$WORK" > "$OUT/df.steam.txt" 2>&1 ;;
  *) rec error "unknown app $APP" ;;
esac

ip -s link > "$OUT/ip.link.after.txt" 2>&1
rec finished_utc "$(date -u +%FT%TZ)"
sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
finish_report
