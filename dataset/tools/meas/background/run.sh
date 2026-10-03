#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|probe|full|diag|shapediag> — one job of the 9.7 background campaign
# (research-slice changelog D2–D15; method
# _dev/research/jioh/task-9.7-background-io/campaign/method.md §1–§4).
#
# One job per program per repeat, its phases in the method's order (D14 (4)):
#   borg      borg-first-warm, borg-repeat-warm, borg-first-cold, borg-repeat-cold
#   7z        7z-mmt8-warm, 7z-mmt1-warm, 7z-mmt8-cold
#   steamcmd  steam-fresh-shaped, steam-fresh-untraced, steam-fresh-unshaped,
#             steam-update-shaped (only with a branch to stage)
#   upgrade   upgrade-install — 9.10's unattended-upgrade campaign (9.10 changelog D3, D36, D37): the stock
#             Ubuntu 24.04 install stage over 2026-07-27's security updates in a chroot of the default layer
#   dkms      dkms-install — 9.10's DKMS campaign (9.10 changelog D4, D46–D50): the same install stage on 2026-09-23,
#             the security kernel 7.0.0-34, in that chroot with the HWE kernel 7.0.0-31 and nvidia-driver-595-open
#   tracker   tracker-index — 9.10's Tracker campaign (9.10 changelog D5, D60–D68): Tracker 3.7.1's first index of a
#             home holding HippoCamp's Bei profile as ~/Documents, in that chroot built at 2026-09-22T17:00Z
#   mnist     mnist-train — 9.10's MNIST training campaign (9.10 changelog D12, D82–D84): PyTorch's basic MNIST example
#             at its defaults, the checkpoint written, on torch 2.14.0's CPU build in that chroot, from a warm start
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
# app and the staging probe on the campaign's app (D12). Diag mode, SteamCMD
# only, not a repeat: the shaped traced download three times on one runner — as
# the campaign runs it, with the setting under test on the command line and in
# steam_dev.cfg (MEAS_STEAM_DIAG_SETTING, e.g. "@cMaxInitialDownloadSources 4";
# empty: @ForceContentServer with MEAS_STEAM_DIAG_FORCE or the first server the
# default download used), and as the campaign runs it again — the number of
# content servers, one connection each, sets the shaper's drops and with them
# every value on `game-download`'s list (run 35475239657, one runner, the atl3
# site: 6 servers 4.73 % of packets dropped and 4,070 B a wake, one server
# forced 0.0005 % and 2,131 B, 6 servers again 4.97 % and 4,137 B). Each
# download records SteamCMD's own find output, the servers its content log
# names, and download_sources after the update. Nothing here fails the job: every step
# records its rc and the next phase runs.
#
# Settings (the trigger file, through the workflow): MEAS_CPU_MODEL (the machine
# gate), MEAS_WORK_ROOT (auto | / | /mnt), MEAS_STEAM_APP, MEAS_STEAM_UPDATE_FROM
# (the branch staged before the update phase; empty: no update phase),
# MEAS_STEAM_UPDATE_TO (app_update's -beta argument back to the public build),
# MEAS_STEAM_DRY_APP (smallest | an app id), MEAS_ARCHIVER_SET (10gb | 1gb: the
# 7-Zip phases' input, method §3 "Dry mode"), MEAS_STEAM_DIAG_SETTING (diag
# mode's setting under test) and MEAS_STEAM_DIAG_FORCE (the server it forces
# when no setting is named; default: the first the run itself used).
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
SHAPE_DISCIPLINE="${MEAS_SHAPE_DISCIPLINE:-aqm}"   # D25: the campaign shapes with the fq_codel leaf; `tbf` is the superseded bucket
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
# the shaped link needs the accelerated-networking VF: without one the redirect sits on eth0's clsact hook behind the
# runner's own direct-action BPF program, which ends classification, so nothing reaches ifb0 (repeat 21, run
# 35584871283: shape.dev=eth0, 490 B through ifb0 of 10.5 GB received). Such a job stops here, recorded, and is relaunched.
if [ "$APP" = steamcmd ]; then
  GATE_IFACE="$(ip -o route get 1.1.1.1 2>/dev/null | sed -n 's/.* dev \([^ ]*\).*/\1/p')"
  GATE_VF="$(ip -o link show 2>/dev/null | awk -F': ' -v m="$GATE_IFACE" 'index($0, " master " m " ") {print $2}' | head -1)"
  if [ -z "$GATE_VF" ]; then
    ip -o link show > "$OUT/ip.link.oneline.txt" 2>&1
    rec gate no-vf; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
    echo "network gate: no accelerated-networking VF under '${GATE_IFACE}' — the shaper cannot sit on this runner; stopping" >&2
    exit 0
  fi
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
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
sudo apt-get install -y --no-install-recommends gcc libc6-dev linux-libc-dev > "$OUT/apt.gcc.log" 2>&1; rec apt.gcc.rc "$?"
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
  upgrade|dkms|tracker|mnist)
        # tracker: util-linux-extra for fincore, the cold start's check (D75; the runner's image lacks it, run #126);
        # mnist: the same, for the warm start's check (D83)
        sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends mmdebstrap \
          $( [ "$APP" = tracker ] || [ "$APP" = mnist ] && echo util-linux-extra) > "$OUT/apt.app.log" 2>&1; rec apt.app.rc "$?"
        rec mmdebstrap.version "$(mmdebstrap --version 2>&1 | head -1)" ;;
esac
rec zpaq.version "$(zpaq 2>&1 | head -1)"
rec util-linux.version "$(fincore --version 2>&1 | head -1)"
rec python.version "$(python3 --version 2>&1)"

# ---- instruments ---------------------------------------------------------------
gcc -O2 -Wall -o "$WORK/taskstats_listen" "$MEAS/build/taskstats_listen.c" > "$OUT/gcc.listener.log" 2>&1; rec listener.build.rc "$?"
sudo sysctl -w kernel.task_delayacct=1 > /dev/null 2>&1; rec sysctl.task_delayacct "$(cat /proc/sys/kernel/task_delayacct 2>/dev/null || echo missing)"
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null 2>&1; rec sysctl.perf_event_paranoid "$(cat /proc/sys/kernel/perf_event_paranoid)"
# schedstats: the kernel's sched_stat_iowait row marks each uninterruptible sleep spent waiting on I/O (the disk rule,
# method §9, the dry-run entry; kernel/sched/stats.c __update_stats_enqueue_sleeper); perf sched record already
# asks for sched_stat_{wait,sleep,iowait} where CONFIG_SCHEDSTATS exposes them (tools/perf/builtin-sched.c), and the
# kernel fires them only with this switch on
sudo sysctl -w kernel.sched_schedstats=1 > /dev/null 2>&1; rec sysctl.sched_schedstats "$(cat /proc/sys/kernel/sched_schedstats 2>/dev/null || echo missing)"
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
    | grep -E "sched_process_fork|sched_wakeup_new|sched_process_exit|sched_process_exec|sched_stat_iowait" | gzip > "$OUT/perf.$name.forks.txt.gz"
  rec "perf.$name.forks.rows" "$(gzip -dc "$OUT/perf.$name.forks.txt.gz" | wc -l)"
  rec "perf.$name.iowait.rows" "$(gzip -dc "$OUT/perf.$name.forks.txt.gz" | grep -c sched_stat_iowait)"
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
  local name="$1" p="$2" url ok=0 t0
  local dest="$WORK/sets/$name" arc="$WORK/$name.zpaq"   # a separate statement: `local` expands every word before assigning any
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
PAGE="$(getconf PAGESIZE)"
cached() {   # resident pages over the pages the files span (fincore counts residency in whole pages)
  rec "cache.$1.fraction" "$(find "$SET" -type f -print0 | xargs -0 fincore -b -n -r -o PAGES,SIZE 2>/dev/null \
    | awk -v pg="$PAGE" '{r += $1; s += int(($2 + pg - 1) / pg)} END {if (s > 0) printf "%.4f", r / s}')"
}
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
# where the shaper sits (dry runs 35425404685, 35426597604): the runner's eth0 carries a clsact qdisc whose ingress hook
# holds the runner's own BPF program (`tc_ingress_traffic`, direct-action, pref 1) — an ingress qdisc is refused and a
# filter beside it at pref 1 is refused. Traffic arrives on the accelerated-networking VF enslaved to eth0, so the
# redirect goes on the VF's own ingress when there is one: packets pass the shaper, then reach eth0 and its program as
# before. Without a VF, eth0's clsact hook after the runner's filter. The interfaces, qdiscs and filters are recorded,
# and after every shaped phase the bytes that went through ifb0.
SHAPE_DEV="$(ip -o link show 2>/dev/null | awk -F': ' -v m="$IFACE" 'index($0, " master " m " ") {print $2}' | head -1)"
SHAPE_DEV="${SHAPE_DEV:-$IFACE}"; rec shape.dev "$SHAPE_DEV"
ip -o link show > "$OUT/ip.link.oneline.txt" 2>&1
shape_on() {   # shape_on [tbf|aqm]: ingress on the interface that carries the traffic redirected to ifb0,
               # the root at the D11 rate — the committed drop-tail bucket, or D24's AQM leaf under test
  local variant="${1:-$SHAPE_DISCIPLINE}"
  { echo "== before"; tc -s qdisc show dev "$SHAPE_DEV"; tc filter show dev "$SHAPE_DEV" ingress; } >> "$OUT/tc.iface.txt" 2>&1
  sudo modprobe ifb numifbs=1 > /dev/null 2>&1; sudo ip link add ifb0 type ifb > /dev/null 2>&1; sudo ip link set ifb0 up
  if tc qdisc show dev "$SHAPE_DEV" | grep -q clsact; then HOOK="ingress"; PREF=49152; SHAPE_OWN_QDISC=0
  else sudo tc qdisc add dev "$SHAPE_DEV" handle ffff: ingress 2>> "$OUT/tc.log"; HOOK="parent ffff:"; PREF=1; SHAPE_OWN_QDISC=1; fi
  rec shape.hook "$HOOK pref $PREF"
  # shellcheck disable=SC2086
  sudo tc filter add dev "$SHAPE_DEV" $HOOK protocol all pref "$PREF" u32 match u32 0 0 action mirred egress redirect dev ifb0 2>> "$OUT/tc.log"
  local frc=$?
  local qrc
  if [ "$variant" = aqm ]; then
    # D24: a rate cap with an active-queue-management leaf (`fqcodel-rfc18`), against the committed bucket.
    # The rate is D11's, untouched; only the queue changes.
    sudo modprobe sch_htb > /dev/null 2>&1; sudo modprobe sch_fq_codel > /dev/null 2>&1
    sudo tc qdisc add dev ifb0 root handle 1: htb default 10 2>> "$OUT/tc.log" \
      && sudo tc class add dev ifb0 parent 1: classid 1:10 htb rate "${RATE_MBIT}mbit" ceil "${RATE_MBIT}mbit" 2>> "$OUT/tc.log" \
      && sudo tc qdisc add dev ifb0 parent 1:10 handle 10: fq_codel 2>> "$OUT/tc.log"
    qrc=$?
  else
    sudo tc qdisc add dev ifb0 root tbf rate "${RATE_MBIT}mbit" burst "$BURST" latency "$TBF_LATENCY" 2>> "$OUT/tc.log"
    qrc=$?
  fi
  rec shape.variant "$variant"
  if [ "$frc" = 0 ] && [ "$qrc" = 0 ]; then SHAPED=1; else SHAPED=0; fi
  { echo "== shaped ($SHAPED, $variant)"; tc filter show dev "$SHAPE_DEV" ingress; tc qdisc show dev ifb0; } >> "$OUT/tc.iface.txt" 2>&1
}
shape_off() {
  # shellcheck disable=SC2086
  if [ "${SHAPE_OWN_QDISC:-1}" = 1 ]; then sudo tc qdisc del dev "$SHAPE_DEV" ingress 2>/dev/null
  else sudo tc filter del dev "$SHAPE_DEV" ${HOOK:-ingress} pref "${PREF:-49152}" 2>/dev/null; fi
  sudo tc qdisc del dev ifb0 root 2>/dev/null; SHAPED=0
}
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
  # shellcheck disable=SC2086   # STEAM_PRE, STEAM_POST: diag mode's settings before login and commands after the update
  TRACE="$tr" phase "$name" -- "$STEAMCMD" ${STEAM_PRE:-} +force_install_dir "$INSTALL" +login anonymous +app_update "$app" "$@" ${STEAM_POST:-} +quit
  rec "net.$name.rx_bytes" "$(( $(netc rx_bytes) - rx0 ))"; rec "net.$name.tx_bytes" "$(( $(netc tx_bytes) - tx0 ))"
  rec "shape.$name" "$SHAPED"
  if [ "$SHAPED" = 1 ]; then
    tc -s qdisc show dev ifb0 > "$OUT/tc.$name.txt" 2>&1
    rec "tc.$name.stats" "$(grep -m1 -oE 'Sent [0-9]+ bytes [0-9]+ pkt \(dropped [0-9]+, overlimits [0-9]+' "$OUT/tc.$name.txt")"
    rec "shape.$name.through_ifb_bytes" "$(grep -m1 -oE 'Sent [0-9]+ bytes' "$OUT/tc.$name.txt" | grep -oE '[0-9]+')"
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
DEV_CFG_DIRS="$HOME/.local/share/Steam $HOME/.local/share/Steam/steamcmd $HOME/.steam/steam $HOME/.steam/steamcmd $HOME/Steam"
steam_find() {   # steam_find <label>: what SteamCMD's own console reports for the download settings
  # shellcheck disable=SC2086
  unmeasured "$STEAMCMD" ${STEAM_PRE:-} +find ContentServer +find DownloadSource +find Connection +find CellID +quit > "$OUT/steamcmd.find.$1.log" 2>&1
  rec "steamcmd.find.$1.rc" "$?"
  local v
  for v in cMaxContentServersToRequest cMaxInitialDownloadSources cDefaultInitialDownloadSources ForceContentServer ForceContentServerType; do
    rec "steamcmd.find.$1.$v" "$(grep -m1 -oE "@$v[^:]*" "$OUT/steamcmd.find.$1.log" | tr -s ' ')"
  done
}
diag_dev_cfg() {   # diag_dev_cfg <setting line or empty to remove>: the setting in every Steam directory that exists
  local d written=""
  for d in $DEV_CFG_DIRS; do
    [ -d "$d" ] || continue
    if [ -n "$1" ]; then echo "$1" > "$d/steam_dev.cfg"; written="$written $d"; else rm -f "$d/steam_dev.cfg"; fi
  done
  [ -n "$1" ] && rec steam.diag.dev_cfg_written "${written# }"
}
diag_download() {   # diag_download <phase> <app> [setting]: one shaped, traced download, the setting on both routes
  local ph="$1" app="$2" setting="${3:-}"
  [ -n "$setting" ] && diag_dev_cfg "$setting"
  shape_on
  STEAM_PRE="$(printf '%s' "$setting" | sed 's/@/+@/g')" STEAM_POST=+download_sources steam_phase "$ph" 1 fresh "$app"
  shape_off
  [ -n "$setting" ] && diag_dev_cfg ""
  rec "steam.diag.$ph.servers" "$(grep -oE "to host [a-z0-9.-]+" "$OUT/steamlogs/$ph/content_log.txt" 2>/dev/null | sort -u | wc -l | tr -d ' ')"
  rec "steam.diag.$ph.sources" "$(grep -m1 -oE 'Got [0-9]+ download sources' "$OUT/steamlogs/$ph/content_log.txt" 2>/dev/null)"
}
diag_first_host() {   # the first content server the named phase's download used
  sed -n "s/.*to host \([a-z0-9.-]*\) (.*/\1/p" "$OUT/steamlogs/$1/content_log.txt" 2>/dev/null | head -1
}
steam_diag() {   # steam_diag <app>: diag mode — default, the setting under test, default again
  local app="$1" setting host
  steam_find default
  diag_download steam-diag-default "$app"
  setting="${MEAS_STEAM_DIAG_SETTING:-}"   # a setting line, e.g. "@cMaxInitialDownloadSources 4"; empty: force one server
  if [ -z "$setting" ]; then
    host="${MEAS_STEAM_DIAG_FORCE:-$(diag_first_host steam-diag-default)}"
    rec steam.diag.force_host "$host"
    [ -n "$host" ] && setting="@ForceContentServer $host"
  fi
  rec steam.diag.setting "$setting"
  if [ -n "$setting" ]; then
    diag_dev_cfg "$setting"; steam_find devcfg; diag_dev_cfg ""
    STEAM_PRE="+$setting" steam_find cmdline
    diag_download steam-diag-setting "$app" "$setting"
    steam_find after
  else
    rec steam.diag.setting skipped-none
  fi
  diag_download steam-diag-default2 "$app"
}
shape_download() {   # shape_download <phase> <app> <variant>: one shaped, traced download under the named discipline
  local ph="$1" app="$2" variant="$3"
  shape_on "$variant"
  rec "shape.$ph.discipline" "$variant"
  STEAM_POST=+download_sources steam_phase "$ph" 1 fresh "$app"
  shape_off
  rec "steam.diag.$ph.servers" "$(grep -oE "to host [a-z0-9.-]+" "$OUT/steamlogs/$ph/content_log.txt" 2>/dev/null | sort -u | wc -l | tr -d ' ')"
  rec "steam.diag.$ph.sources" "$(grep -m1 -oE 'Got [0-9]+ download sources' "$OUT/steamlogs/$ph/content_log.txt" 2>/dev/null)"
}
steam_shape_diag() {   # D24: the committed tbf root, the AQM leaf under test, the committed root again
  local app="$1"
  shape_download steam-shape-tbf "$app" tbf
  shape_download steam-shape-aqm "$app" aqm
  shape_download steam-shape-tbf2 "$app" tbf
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

# ---- the unattended upgrade (9.10 D3, D36–D38) ---------------------------------
# The default layer of an English install (upgrade-layer.txt) built by mmdebstrap from the archive as Ubuntu's
# snapshot service serves it at T0, on the harness CPUs; the stock download stage, `apt.systemd.daily update`, run in
# the chroot against the archive at T1, on the harness CPUs; then apt-daily-upgrade.service's ExecStart,
# `apt.systemd.daily install`, run in the chroot on the measured CPU as the phase. Its ExecStartPre, `apt-helper
# wait-online`, is not run: in a chroot systemctl answers every is-active query with success, so all three waiters
# run and systemd-networkd's times out after 30 s, a state no online desktop is in (D38). The
# chroot's /run is its own tmpfs, never the runner's: with /run/systemd/system absent the packages' scripts cannot
# reach the runner's systemd, and ischroot holds, as on any chroot (S2-32).
UPG_T0="${MEAS_UPGRADE_T0:-20260727T000000Z}"; UPG_T1="${MEAS_UPGRADE_T1:-20260728T000000Z}"   # D36
UPG_SNAP=http://snapshot.ubuntu.com/ubuntu
UPG_COMPONENTS="main restricted universe multiverse"
upg_mount() {   # upg_mount <root>: proc, sys, the runner's /dev, a fresh /run with the resolver's stub file
  local r="$1"
  sudo mount -t proc proc "$r/proc"; sudo mount -t sysfs sys "$r/sys"
  sudo mount --bind /dev "$r/dev"; sudo mount --bind /dev/pts "$r/dev/pts"
  sudo mount -t tmpfs -o mode=755 tmpfs "$r/run"
  sudo mkdir -p "$r/run/systemd/resolve" "$r/run/lock"
  sudo cp -L /etc/resolv.conf "$r/run/systemd/resolve/stub-resolv.conf"
  [ -L "$r/etc/resolv.conf" ] || sudo cp -L /etc/resolv.conf "$r/etc/resolv.conf"
  rec upgrade.run_systemd_system "$( [ -d "$r/run/systemd/system" ] && echo present || echo absent)"
}
upg_umount() { local r="$1" m; for m in run dev/pts dev sys proc; do sudo umount -l "$r/$m" 2>/dev/null; done; }
upg_sources() {   # upg_sources <root> <timestamp>: the stock deb822 pair (installer form, the archive and security
  # hosts) pointed at the snapshot of <timestamp>; mmdebstrap's own sources and apt options removed
  local r="$1" ts="$2"
  sudo rm -f "$r/etc/apt/sources.list" "$r/etc/apt/apt.conf.d/99mmdebstrap"
  sudo tee "$r/etc/apt/sources.list.d/ubuntu.sources" > /dev/null <<SRC
Types: deb
URIs: $UPG_SNAP/$ts/
Suites: noble noble-updates noble-backports
Components: $UPG_COMPONENTS
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: $UPG_SNAP/$ts/
Suites: noble-security
Components: $UPG_COMPONENTS
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
SRC
  sudo cp "$r/etc/apt/sources.list.d/ubuntu.sources" "$OUT/upgrade.sources.$ts.txt"
}
upg_build() {   # upg_build <root>: the layer at T0, on the harness CPUs
  local r="$1" t0 layer
  layer="$(grep -v '^#' "$HERE/upgrade-layer.txt" | paste -sd, -)${UPG_EXTRA:+,$UPG_EXTRA}"   # UPG_EXTRA: a job's own additions
  rec upgrade.layer.packages "$(grep -vc '^#' "$HERE/upgrade-layer.txt")"; rec upgrade.layer.added "${UPG_EXTRA:-}"
  rec upgrade.layer.sha256 "$(sha256sum "$HERE/upgrade-layer.txt" | cut -d' ' -f1)"
  rec upgrade.t0 "$UPG_T0"; rec upgrade.t1 "$UPG_T1"
  t0=$(date +%s)
  unmeasured sudo mmdebstrap --mode=root --variant=apt --format=directory \
    --components="$(echo $UPG_COMPONENTS | tr ' ' ',')" --include="$layer" \
    --aptopt='Acquire::Retries "5"' \
    noble "$r" \
    "deb $UPG_SNAP/$UPG_T0/ noble $UPG_COMPONENTS" \
    "deb $UPG_SNAP/$UPG_T0/ noble-updates $UPG_COMPONENTS" \
    "deb $UPG_SNAP/$UPG_T0/ noble-security $UPG_COMPONENTS" > "$OUT/upgrade.mmdebstrap.log" 2>&1
  rec upgrade.build.rc "$?"; rec upgrade.build_s "$(( $(date +%s) - t0 ))"
  # the English install's system locale (design, D37); locale-gen reads supported.d and locale.gen alike (S2-32)
  echo "LANG=en_US.UTF-8" | sudo tee "$r/etc/default/locale" > /dev/null
  sudo chroot "$r" dpkg-query -W -f '${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' > "$OUT/upgrade.dpkg.t0.tsv" 2>&1
  rec upgrade.t0.installed "$(wc -l < "$OUT/upgrade.dpkg.t0.tsv")"
  python3 - "$HERE/upgrade-layer.txt" "$OUT/upgrade.dpkg.t0.tsv" > "$OUT/upgrade.layer.diff.txt" <<'PY'
import sys
want = {l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")}
have = {l.split("\t")[0].split(":")[0] for l in open(sys.argv[2]) if "\t" in l}
print("missing\t" + " ".join(sorted(want - have)))
print("extra\t" + " ".join(sorted(have - want)))
PY
  rec upgrade.layer.missing "$(sed -n 's/^missing\t//p' "$OUT/upgrade.layer.diff.txt" | wc -w)"
  rec upgrade.layer.extra "$(sed -n 's/^extra\t//p' "$OUT/upgrade.layer.diff.txt" | wc -w)"
  sudo cat "$r/etc/apt/apt.conf.d/20auto-upgrades" > "$OUT/upgrade.20auto-upgrades.txt" 2>&1
  sudo cat "$r/etc/apt/apt.conf.d/10periodic" > "$OUT/upgrade.10periodic.txt" 2>&1
  ls "$r/var/lib/locales/supported.d/" > "$OUT/upgrade.supported.d.txt" 2>&1
  sudo du -sb "$r" 2>/dev/null | cut -f1 | { read -r b; rec upgrade.chroot_bytes "$b"; }
}
upg_download() {   # upg_download <root>: the stock download stage against T1, on the harness CPUs
  local r="$1" t0
  upg_sources "$r" "$UPG_T1"
  t0=$(date +%s)
  unmeasured sudo chroot "$r" /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=en_US.UTF-8 /usr/lib/apt/apt.systemd.daily update < /dev/null > "$OUT/upgrade.update-stage.log" 2>&1
  rec upgrade.update_stage.rc "$?"; rec upgrade.update_stage_s "$(( $(date +%s) - t0 ))"
  ls -l "$r/var/cache/apt/archives/" > "$OUT/upgrade.archives.txt" 2>&1
  rec upgrade.downloaded "$(ls "$r/var/cache/apt/archives/" | grep -c '\.deb$')"
  sudo cat "$r/var/log/unattended-upgrades/unattended-upgrades.log" > "$OUT/upgrade.uu.download.log" 2>/dev/null
  ls -l --time-style=full-iso "$r/var/lib/apt/periodic/" > "$OUT/upgrade.stamps.after-update.txt" 2>&1
}
upg_after() {   # upg_after <root>: what the measured stage installed
  local r="$1"
  sudo chroot "$r" dpkg-query -W -f '${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' > "$OUT/upgrade.dpkg.t1.tsv" 2>&1
  diff "$OUT/upgrade.dpkg.t0.tsv" "$OUT/upgrade.dpkg.t1.tsv" > "$OUT/upgrade.dpkg.diff.txt"
  rec upgrade.changed "$(grep -c '^>' "$OUT/upgrade.dpkg.diff.txt")"
  rec upgrade.changed_sha256 "$(grep '^>' "$OUT/upgrade.dpkg.diff.txt" | sha256sum | cut -d' ' -f1)"
  sudo cp "$r/var/log/unattended-upgrades/unattended-upgrades.log" "$OUT/upgrade.uu.log" 2>/dev/null
  sudo cp "$r/var/log/unattended-upgrades/unattended-upgrades-dpkg.log" "$OUT/upgrade.uu-dpkg.log" 2>/dev/null
  rec upgrade.uu.all_installed "$(grep -c 'INFO All upgrades installed' "$OUT/upgrade.uu.log" 2>/dev/null)"
  sudo cp "$r/var/log/dpkg.log" "$OUT/upgrade.dpkg.log" 2>/dev/null
  ls -l --time-style=full-iso "$r/var/lib/apt/periodic/" > "$OUT/upgrade.stamps.after-install.txt" 2>&1
  [ -e "$r/var/run/reboot-required" ] && rec upgrade.reboot_required yes || rec upgrade.reboot_required no
}
upg_job() {
  local r="$WORK/chroot"
  sudo rm -rf "$r"; upg_build "$r"; upg_mount "$r"; upg_download "$r"
  # the unit's ExecStart (D38), its environment reduced to a service's (PATH, the system locale), stdin from /dev/null
  # sudo stays on the harness CPUs; taskset puts the chroot's command, and only it, on the measured CPU
  export MEAS_PIN=none
  phase upgrade-install -- sudo taskset -c "$MEAS_CPU" chroot "$r" /usr/bin/env -i \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=en_US.UTF-8 \
    /usr/lib/apt/apt.systemd.daily install < /dev/null
  export MEAS_PIN=load
  upg_after "$r"; upg_umount "$r"
  df -B1 --output=target,avail "$WORK" > "$OUT/df.upgrade.txt" 2>&1
}

# ---- the DKMS autoinstall (9.10 D4, D46–D50) ----------------------------------------
# D49's state: D37's chroot built at T0 = 2026-09-22T17:00Z (D51: after that day's security update to sudo, before the
# updates pocket published the kernel 7.0.0-34), then, on the harness CPUs, the kernel the installer adds
# (linux-generic-hwe-24.04, 7.0.0-31 at T0) and the driver package D46's user installs (nvidia-driver-595-open, which
# pulls in dkms and nvidia-dkms-595-open 595.91.07 and builds the module for 7.0.0-31). The download stage against
# T1 = 2026-09-24T00:00Z fetches the day's security updates — the kernel 7.0.0-34 (D48) and xdg-desktop-portal — and
# the install stage is measured as D38's. Its environment carries OMP_NUM_THREADS=8: nproc returns it (coreutils,
# S2-40), and both NVIDIA's dkms.conf (make -j`nproc`, S2-39) and dkms's default -j read nproc, so the build runs at
# D4's eight-thread desktop's -j on the one measured CPU (D50). The job — every process under the two DKMS hooks the
# kernel install runs — is cut by analyze.py (D50).
dkms_state() {   # dkms_state <root>: the kernel and the driver package at T0, on the harness CPUs
  local r="$1" t0
  upg_sources "$r" "$UPG_T0"
  unmeasured sudo chroot "$r" apt-get update > "$OUT/dkms.state.apt-update.log" 2>&1; rec dkms.state.apt_update.rc "$?"
  t0=$(date +%s)
  unmeasured sudo chroot "$r" /usr/bin/env DEBIAN_FRONTEND=noninteractive apt-get install -y linux-generic-hwe-24.04 \
    < /dev/null > "$OUT/dkms.state.kernel.log" 2>&1
  rec dkms.state.kernel.rc "$?"; rec dkms.state.kernel_s "$(( $(date +%s) - t0 ))"
  t0=$(date +%s)
  unmeasured sudo chroot "$r" /usr/bin/env DEBIAN_FRONTEND=noninteractive apt-get install -y nvidia-driver-595-open \
    < /dev/null > "$OUT/dkms.state.driver.log" 2>&1
  rec dkms.state.driver.rc "$?"; rec dkms.state.driver_s "$(( $(date +%s) - t0 ))"
  unmeasured sudo chroot "$r" apt-get clean   # the download stage's count is then the day's alone
  rec dkms.state.kernels "$(ls "$r/lib/modules" 2>/dev/null | paste -sd, -)"
  rec dkms.state.status "$(sudo chroot "$r" dkms status 2>&1 | paste -sd';' -)"
  rec dkms.version "$(sudo chroot "$r" dkms --version 2>&1 | head -1)"
  rec dkms.state.nvidia_dkms "$(sudo chroot "$r" dpkg-query -W -f '${Version}' nvidia-dkms-595-open 2>/dev/null)"
  rec dkms.state.gcc "$(sudo chroot "$r" sh -c 'readlink -f /usr/bin/gcc; ls /usr/bin/gcc-[0-9]* 2>/dev/null' | paste -sd, -)"
  sudo chroot "$r" dpkg --print-foreign-architectures > "$OUT/dkms.state.foreign-arch.txt" 2>&1
  # the installed set the measured stage starts from (upg_after diffs against it)
  sudo chroot "$r" dpkg-query -W -f '${binary:Package}\t${Version}\t${db:Status-Abbrev}\n' > "$OUT/upgrade.dpkg.t0.tsv" 2>&1
  rec dkms.state.installed "$(wc -l < "$OUT/upgrade.dpkg.t0.tsv")"
  sudo du -sbx "$r" 2>/dev/null | cut -f1 | { read -r b; rec dkms.state.chroot_bytes "$b"; }
}
dkms_after() {   # dkms_after <root>: the module the stage built, and DKMS's own records
  local r="$1" k=7.0.0-34-generic
  rec dkms.after.kernels "$(ls "$r/lib/modules" 2>/dev/null | paste -sd, -)"
  rec dkms.after.status "$(sudo chroot "$r" dkms status 2>&1 | paste -sd';' -)"
  rec dkms.after.installed_new "$(sudo chroot "$r" dkms status -k "$k" 2>/dev/null | grep -c ': installed')"
  sudo find "$r/lib/modules/$k/updates" -name 'nvidia*.ko*' -printf '%P\t%s\n' > "$OUT/dkms.modules.$k.txt" 2>/dev/null
  rec dkms.after.modules "$(wc -l < "$OUT/dkms.modules.$k.txt")"
  sudo find "$r/var/lib/dkms/nvidia" -path "*$k*" -name make.log -exec cp {} "$OUT/dkms.make.$k.log" \; 2>/dev/null
  rec dkms.after.make_log_cc "$(grep -c ' CC \[M\]' "$OUT/dkms.make.$k.log" 2>/dev/null)"
  grep -n -E 'dkms|Building module|Signing|depmod|initrd|Done' "$OUT/upgrade.uu-dpkg.log" > "$OUT/dkms.hooks.txt" 2>/dev/null
}
dkms_job() {
  local r="$WORK/chroot"
  UPG_T0="${MEAS_DKMS_T0:-20260922T170000Z}"; UPG_T1="${MEAS_DKMS_T1:-20260924T000000Z}"   # D48, D51
  sudo rm -rf "$r"; upg_build "$r"; upg_mount "$r"; dkms_state "$r"; upg_download "$r"
  export MEAS_PIN=none
  phase dkms-install -- sudo taskset -c "$MEAS_CPU" chroot "$r" /usr/bin/env -i \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=en_US.UTF-8 OMP_NUM_THREADS=8 \
    /usr/lib/apt/apt.systemd.daily install < /dev/null
  export MEAS_PIN=load
  upg_after "$r"; dkms_after "$r"; upg_umount "$r"
  df -B1 --output=target,avail "$WORK" > "$OUT/df.dkms.txt" 2>&1
}

# ---- the Tracker index (9.10 D5, D60–D68) ---------------------------------------------
# D37's chroot built at D64's T0, the DKMS campaign's: Tracker 3.7.1 and its extractors as the English default install
# holds them, nothing installed and no setting written (D61, D63). A user with its XDG folders, created by the layer's
# xdg-user-dirs-update; HippoCamp's Bei tree at a pinned revision as the content of ~/Documents, the other folders
# empty (D66–D68), downloaded and checked file by file on the harness CPUs (hippocamp.py). The phase is a session bus
# of the user's own (dbus-run-session) on the harness CPUs, the miner in it on the measured CPU (tracker-session.sh);
# the job — every process in the miner's tree, from its first schedule-in to the extractor's "Extraction finished" — is
# cut by analyze.py (D62, D63, D65). The chroot's root is bound onto itself, so /proc/self/mountinfo inside it shows the
# filesystem under /, where GIO looks a path's mount up for the miner's storage.
TRK_REPO=MMMem-org/HippoCamp; TRK_REV=ff212ff7ec1a60d28023e65f7e7c4df5a87f552c; TRK_TREE=Bei/Fullset/Bei   # D67
TRK_USER=user; TRK_UID=1000; TRK_CAP_S=3600   # the user's name: design; the phase's cap (method §3)
trk_as_user() {   # trk_as_user <root> <cmd...>: in the chroot as the user, the environment reduced to the user's
  local r="$1"; shift
  sudo chroot "$r" setpriv --reuid="$TRK_UID" --regid="$TRK_UID" --init-groups /usr/bin/env -i HOME="/home/$TRK_USER" \
    USER="$TRK_USER" LOGNAME="$TRK_USER" PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=en_US.UTF-8 "$@"
}
trk_home() {   # trk_home <root>: the user, its folders, the set as ~/Documents, the session script
  local r="$1" h="/home/$TRK_USER"
  sudo chroot "$r" useradd -m -u "$TRK_UID" -U -s /bin/bash "$TRK_USER" > "$OUT/tracker.useradd.log" 2>&1; rec tracker.useradd.rc "$?"
  trk_as_user "$r" xdg-user-dirs-update > "$OUT/tracker.xdg.log" 2>&1; rec tracker.xdg.rc "$?"
  sudo cat "$r$h/.config/user-dirs.dirs" > "$OUT/tracker.user-dirs.dirs.txt" 2>&1
  rec tracker.home.entries "$(sudo ls -A "$r$h" | paste -sd, -)"
  # the home is the user's alone (mode 750): the set is fetched into the work directory, then renamed into place as
  # ~/Documents on the same filesystem (dry run 1, run #118: the fetch into the home was refused)
  rm -rf "$WORK/trk-set"
  unmeasured python3 "$HERE/hippocamp.py" "$TRK_REPO" "$TRK_REV" "$TRK_TREE" "$WORK/trk-set" "$OUT/tracker.set.tsv" \
    > "$OUT/tracker.set.kv" 2> "$OUT/tracker.set.log"
  rec tracker.set.rc "$?"
  while IFS='=' read -r k v; do [ -n "$k" ] && rec "tracker.set.$k" "$v"; done < "$OUT/tracker.set.kv"
  rec tracker.set.repo "$TRK_REPO"; rec tracker.set.revision "$TRK_REV"; rec tracker.set.tree "$TRK_TREE"
  sudo rmdir "$r$h/Documents" && sudo mv "$WORK/trk-set" "$r$h/Documents"; rec tracker.set.placed.rc "$?"
  sudo chroot "$r" chown -R "$TRK_USER:$TRK_USER" "$h"
  rec tracker.set.files_on_disk "$(sudo find "$r$h/Documents" -type f | wc -l)"
  rec tracker.set.dirs_on_disk "$(sudo find "$r$h/Documents" -mindepth 1 -type d | wc -l)"
  rec tracker.set.bytes_on_disk "$(sudo find "$r$h/Documents" -type f -printf '%s\n' | awk '{s += $1} END {print s + 0}')"
  rec tracker.gst_registry.before "$(sudo test -e "$r$h/.cache/gstreamer-1.0" && echo present || echo absent)"
  rec tracker.db.before "$(sudo test -e "$r$h/.cache/tracker3" && echo present || echo absent)"
  rec tracker.miner.version "$(sudo chroot "$r" dpkg-query -W -f '${Version}' tracker-miner-fs 2>/dev/null)"
  rec tracker.extract.version "$(sudo chroot "$r" dpkg-query -W -f '${Version}' tracker-extract 2>/dev/null)"
  rec tracker.chroot_tz "$(sudo chroot "$r" date +%Z)"
  sudo mkdir -p "$r/var/tmp/meas"; sudo chroot "$r" chown "$TRK_USER:$TRK_USER" /var/tmp/meas
  sudo install -m 755 "$HERE/tracker-session.sh" "$r/usr/local/lib/meas-tracker-session.sh"
}
trk_after() {   # trk_after <root>: the session's records and what the index left
  local r="$1" h="/home/$TRK_USER" c="$OUT/cmd.tracker-index.log"
  sudo cp "$r/var/tmp/meas/"* "$OUT/" 2>/dev/null
  rec tracker.done "$(sed -n 's/^done=\([0-9]*\).*/\1/p' "$c" | tail -1)"
  rec tracker.elapsed_s "$(sed -n 's/.*elapsed_s=\([0-9]*\).*/\1/p' "$c" | tail -1)"
  rec tracker.miner_rc "$(sed -n 's/^miner_rc=//p' "$c" | tail -1)"
  rec tracker.miner_killed "$(grep -c '^miner_killed=1' "$c")"
  local L="$OUT/tracker.log"
  rec tracker.log.lines "$(wc -l < "$L" 2>/dev/null || echo 0)"
  rec tracker.log.debug_lines "$(grep -c -- '-DEBUG' "$L" 2>/dev/null)"
  rec tracker.log.warnings "$(grep -c -- '-WARNING\|-CRITICAL' "$L" 2>/dev/null)"
  # the status trace (D69): the initial sleep as the miner's first Idle to its Initializing, in s; the extractor's runs
  rec tracker.log.sleep_s "$(python3 - "$L" <<'PY'
import re, sys
t = {}
for line in open(sys.argv[1], errors="replace"):
    m = re.search(r"Tracker-Message: (\d\d):(\d\d):(\d\d)\.(\d{3}): \(Miner:'TrackerMinerFiles'\) set property:'status' to '(Idle|Initializing)'", line)
    if m and m.group(5) not in t:
        h, mi, s_, ms = map(int, m.groups()[:4])
        t[m.group(5)] = h * 3600 + mi * 60 + s_ + ms / 1000
print(round(t["Initializing"] - t["Idle"], 3) if len(t) == 2 else "")
PY
)"
  rec tracker.log.extracting "$(grep -c "TrackerExtractDecorator') set property:'status' to 'Extracting metadata'" "$L" 2>/dev/null)"
  rec tracker.log.deadline_exits "$(grep -c 'took too long to process' "$L" 2>/dev/null)"
  rec tracker.log.extractor_died "$(grep -c 'Extractor subprocess died unexpectedly' "$L" 2>/dev/null)"
  rec tracker.db.files "$(sed -n 's/^Currently indexed: \([0-9]*\) files.*/\1/p' "$OUT/tracker.status.txt" 2>/dev/null)"
  rec tracker.db.folders "$(sed -n 's/^Currently indexed: [0-9]* files, \([0-9]*\) folders.*/\1/p' "$OUT/tracker.status.txt" 2>/dev/null)"
  rec tracker.db.failures "$(sed -n 's/^\([0-9]*\) recorded failures.*/\1/p' "$OUT/tracker.status.txt" 2>/dev/null)"
  rec tracker.gst_registry.after "$(sudo ls "$r$h/.cache/gstreamer-1.0" 2>/dev/null | paste -sd, -)"
  sudo ls -laR "$r$h/.cache" > "$OUT/tracker.cache.txt" 2>&1
}
trk_cold() {   # trk_cold: the clean page cache dropped before the index (D75), the set's cached fraction recorded —
  # fincore read as root, the home being the user's alone; the second drop undoes its metadata reads (as cold())
  local d="$WORK/chroot/home/$TRK_USER/Documents"
  sync; sudo sysctl -q vm.drop_caches=3
  rec cache.tracker-index.fraction "$(sudo find "$d" -type f -print0 | sudo xargs -0 fincore -b -n -r -o PAGES,SIZE 2>/dev/null \
    | awk -v pg="$PAGE" '{r += $1; s += int(($2 + pg - 1) / pg)} END {if (s > 0) printf "%.4f", r / s}')"
  sync; sudo sysctl -q vm.drop_caches=3
}
trk_job() {
  local r="$WORK/chroot"
  UPG_T0="${MEAS_TRACKER_T0:-20260922T170000Z}"   # D64
  sudo rm -rf "$r"; upg_build "$r"
  sudo mount --bind "$r" "$r"; upg_mount "$r"; trk_home "$r"
  trk_cold
  export MEAS_PIN=none
  phase tracker-index -- sudo taskset -c "$MEAS_HARNESS_CPUS" chroot "$r" setpriv --reuid="$TRK_UID" --regid="$TRK_UID" \
    --init-groups /usr/bin/env -i HOME="/home/$TRK_USER" USER="$TRK_USER" LOGNAME="$TRK_USER" \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=en_US.UTF-8 \
    dbus-run-session -- /bin/bash /usr/local/lib/meas-tracker-session.sh "$MEAS_CPU" "$TRK_CAP_S" /var/tmp/meas
  export MEAS_PIN=load
  trk_after "$r"; upg_umount "$r"; sudo umount -l "$r" 2>/dev/null
  df -B1 --output=target,avail "$WORK" > "$OUT/df.tracker.txt" 2>&1
}

# ---- the MNIST training run (9.10 D12, D82–D84) ------------------------------------------
# D37's chroot built at D64's T0 with python3-venv added, the package a venv needs (D82); the Tracker job's user and
# home; torch 2.14.0 and torchvision 0.29.0, the release current at T0 (S2-48), installed into a venv in the home by
# PyTorch's own command for Linux, pip and the CPU (S2-47), the two versions pinned; the example's three files from
# pytorch/examples at acc295d (S2-31) as ~/examples/mnist, each checked by its SHA-256 — fetched into the work
# directory and moved into the home, which is the user's alone. An unmeasured start of the example, its own --dry-run
# for one epoch, on the harness CPUs: torchvision's MNIST download places the dataset in ../data, the example's own
# path, and torch's files enter the page cache (D83; 9.6 D28). The phase is the README's `python main.py`, with
# --save-model, as the user in the chroot with the venv activated (its bin first on PATH, VIRTUAL_ENV), on the measured
# CPU (D84); the job — every process of the tree, from its first schedule-in to its exit — is cut by analyze.py.
MN_REV=acc295dc7b90714f1bf47f06004fc19a7fe235c4                                    # S2-31
MN_TORCH=2.14.0; MN_VISION=0.29.0; MN_INDEX=https://download.pytorch.org/whl/cpu   # D82; S2-47, S2-48
MN_FILES="main.py:30a3359d1911d2d859dd090ce20be7ed132a33f508dc389f40366010b3e9ecc8
README.md:df847dfd52aad2e1d03bcaee6d7bcf7d013202fa8727f76f38fe0fce22d32cf1
requirements.txt:005cbc6604c36772776d4e1104cc0ab3e2869f1fab0bfbbbd3540592792f7108"
MN_H="/home/$TRK_USER"; MN_DIR="/home/$TRK_USER/examples/mnist"; MN_VENV="/home/$TRK_USER/venv"
MN_PATH="$MN_VENV/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
mn_user() {   # mn_user <root> <cpus> <dir> <cmd...>: in the chroot as the user, the venv activated, in <dir>, on <cpus>
  local r="$1" cpus="$2" dir="$3"; shift 3
  sudo taskset -c "$cpus" chroot "$r" setpriv --reuid="$TRK_UID" --regid="$TRK_UID" --init-groups /usr/bin/env -i -C "$dir" \
    HOME="$MN_H" USER="$TRK_USER" LOGNAME="$TRK_USER" VIRTUAL_ENV="$MN_VENV" PATH="$MN_PATH" LANG=en_US.UTF-8 "$@"
}
mn_state() {   # mn_state <root>: the user, the example, the venv with torch and torchvision — on the harness CPUs
  local r="$1" t0 f name want got
  sudo chroot "$r" useradd -m -u "$TRK_UID" -U -s /bin/bash "$TRK_USER" > "$OUT/mnist.useradd.log" 2>&1; rec mnist.useradd.rc "$?"
  rec mnist.python.version "$(sudo chroot "$r" dpkg-query -W -f '${Version}' python3.12 2>/dev/null)"
  rec mnist.venv_pkg.version "$(sudo chroot "$r" dpkg-query -W -f '${Version}' python3-venv 2>/dev/null)"
  rm -rf "$WORK/mn-ex"; mkdir -p "$WORK/mn-ex/mnist"
  for f in $MN_FILES; do
    name="${f%%:*}"; want="${f#*:}"
    unmeasured wget -q --tries=5 --waitretry=15 -O "$WORK/mn-ex/mnist/$name" \
      "https://raw.githubusercontent.com/pytorch/examples/$MN_REV/mnist/$name"
    got="$(sha256sum "$WORK/mn-ex/mnist/$name" | cut -d' ' -f1)"; rec "mnist.example.$name.pin" "$(pin_state "$want" "$got")"
  done
  sudo mv "$WORK/mn-ex" "$r$MN_H/examples"; sudo chroot "$r" chown -R "$TRK_USER:$TRK_USER" "$MN_H/examples"; rec mnist.example.placed.rc "$?"
  t0=$(date +%s)
  mn_user "$r" "$MEAS_HARNESS_CPUS" "$MN_H" /usr/bin/python3 -m venv "$MN_VENV" > "$OUT/mnist.venv.log" 2>&1; rec mnist.venv.rc "$?"
  mn_user "$r" "$MEAS_HARNESS_CPUS" "$MN_H" pip3 install "torch==$MN_TORCH" "torchvision==$MN_VISION" --index-url "$MN_INDEX" \
    > "$OUT/mnist.pip.log" 2>&1; rec mnist.pip.rc "$?"; rec mnist.pip_s "$(( $(date +%s) - t0 ))"
  mn_user "$r" "$MEAS_HARNESS_CPUS" "$MN_H" pip3 freeze --all > "$OUT/mnist.pip-freeze.txt" 2>&1
  rec mnist.torch.version "$(sed -n 's/^torch==//p' "$OUT/mnist.pip-freeze.txt")"
  rec mnist.torchvision.version "$(sed -n 's/^torchvision==//p' "$OUT/mnist.pip-freeze.txt")"
  rec mnist.pip-freeze.sha256 "$(sha256sum "$OUT/mnist.pip-freeze.txt" | cut -d' ' -f1)"
  sudo du -sb "$r$MN_VENV" 2>/dev/null | cut -f1 | { read -r b; rec mnist.venv_bytes "$b"; }
  sudo cat "$r$MN_VENV/bin/activate" > "$OUT/mnist.activate.txt" 2>&1   # what activating the venv sets (D84)
}
mn_fraction() {   # mn_fraction <dir> <name filter>: resident pages over the pages the files span, read as root
  sudo find "$1" -type f -name "$2" -print0 | sudo xargs -0 fincore -b -n -r -o PAGES,SIZE 2>/dev/null \
    | awk -v pg="$PAGE" '{r += $1; s += int(($2 + pg - 1) / pg)} END {if (s > 0) printf "%.4f", r / s}'
}
mn_warm() {   # mn_warm <root>: the example's own dry run for one epoch on the harness CPUs (D83), then what torch sees on
  # the measured CPU and the page cache's state
  local r="$1" t0 raw="$1/home/$TRK_USER/examples/data/MNIST/raw"
  t0=$(date +%s)
  mn_user "$r" "$MEAS_HARNESS_CPUS" "$MN_DIR" python main.py --dry-run --epochs 1 > "$OUT/mnist.warm.log" 2>&1; rec mnist.warm.rc "$?"
  rec mnist.warm_s "$(( $(date +%s) - t0 ))"
  sudo ls -l "$raw" > "$OUT/mnist.data.txt" 2>&1
  sudo sh -c 'cd "$1" && sha256sum *' _ "$raw" > "$OUT/mnist.data.sha256" 2>&1
  rec mnist.data.files "$(sudo find "$raw" -type f | wc -l)"
  rec mnist.data.sha256 "$(sha256sum "$OUT/mnist.data.sha256" | cut -d' ' -f1)"
  mn_user "$r" "$MEAS_CPU" "$MN_DIR" python -c 'import json, torch
print(json.dumps({"torch": torch.__version__, "threads": torch.get_num_threads(), "interop_threads": torch.get_num_interop_threads()}))
print(torch.__config__.parallel_info())' > "$OUT/mnist.probe.txt" 2>&1; rec mnist.probe.rc "$?"
  rec mnist.probe.threads "$(head -1 "$OUT/mnist.probe.txt" | python3 -c 'import json,sys; print(json.load(sys.stdin)["threads"])' 2>/dev/null)"
  rec mnist.probe.interop_threads "$(head -1 "$OUT/mnist.probe.txt" | python3 -c 'import json,sys; print(json.load(sys.stdin)["interop_threads"])' 2>/dev/null)"
  rec cache.mnist-train.fraction "$(mn_fraction "$raw" '*-ubyte')"   # the dataset as the run reads it (D83)
  rec cache.mnist-train.torch_lib_fraction "$(mn_fraction "$r$MN_VENV/lib" '*.so*')"
}
mn_thp() {   # mn_thp <label>: the kernel's transparent-hugepage settings and its counters — every block of the dry run's
  # training run was ended by khugepaged (run #142)
  local f k v
  for f in enabled defrag khugepaged/defrag khugepaged/scan_sleep_millisecs khugepaged/alloc_sleep_millisecs khugepaged/pages_to_scan; do
    rec "thp.$1.${f//\//.}" "$(cat "/sys/kernel/mm/transparent_hugepage/$f" 2>/dev/null)"
  done
  while read -r k v; do rec "thp.$1.$k" "$v"; done < <(grep -E '^thp_(collapse_alloc|collapse_alloc_failed|fault_alloc|fault_fallback) ' /proc/vmstat)
}
mn_after() {   # mn_after <root>: the run's own output and the checkpoint
  local r="$1" c="$OUT/cmd.mnist-train.log"
  rec mnist.train.epochs "$(grep -c '^Test set:' "$c")"
  rec mnist.train.log_lines "$(grep -c '^Train Epoch:' "$c")"
  rec mnist.train.last_test "$(grep '^Test set:' "$c" | tail -1)"
  rec mnist.checkpoint.bytes "$(sudo stat -c %s "$r$MN_DIR/mnist_cnn.pt" 2>/dev/null || echo 0)"
  rec mnist.checkpoint.sha256 "$(sudo sha256sum "$r$MN_DIR/mnist_cnn.pt" 2>/dev/null | cut -d' ' -f1)"
}
mn_job() {
  local r="$WORK/chroot"
  UPG_T0="${MEAS_MNIST_T0:-20260922T170000Z}"; UPG_EXTRA=python3-venv   # D82: D64's T0
  sudo rm -rf "$r"; upg_build "$r"; upg_mount "$r"; mn_state "$r"; mn_warm "$r"
  mn_thp before
  export MEAS_PIN=none
  phase mnist-train -- sudo taskset -c "$MEAS_CPU" chroot "$r" setpriv --reuid="$TRK_UID" --regid="$TRK_UID" --init-groups \
    /usr/bin/env -i -C "$MN_DIR" HOME="$MN_H" USER="$TRK_USER" LOGNAME="$TRK_USER" VIRTUAL_ENV="$MN_VENV" PATH="$MN_PATH" \
    LANG=en_US.UTF-8 python main.py --save-model
  export MEAS_PIN=load
  mn_thp after
  mn_after "$r"; upg_umount "$r"
  df -B1 --output=target,avail "$WORK" > "$OUT/df.mnist.txt" 2>&1
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
    elif [ "$MODE" = shapediag ]; then
      appinfo "$STEAM_APP"; RUN_APP="$STEAM_APP"; rec steam.app "$RUN_APP"
      steam_shape_diag "$RUN_APP"
    elif [ "$MODE" = diag ]; then
      appinfo "$STEAM_APP"; RUN_APP="$STEAM_APP"; rec steam.app "$RUN_APP"
      steam_diag "$RUN_APP"
    else
      appinfo "$STEAM_APP"; RUN_APP="$STEAM_APP"; rec steam.app "$RUN_APP"
      steam_phases "$RUN_APP" "$UPDATE_FROM" "$UPDATE_TO"
    fi
    rec steam.buildid "$(sed -n 's/^steam\.steam-fresh-shaped\.buildid=//p' "$KV" | tail -1)"
    df -B1 --output=target,avail "$WORK" > "$OUT/df.steam.txt" 2>&1 ;;
  upgrade) upg_job ;;
  dkms) dkms_job ;;
  tracker) trk_job ;;
  mnist) mn_job ;;
  *) rec error "unknown app $APP" ;;
esac

ip -s link > "$OUT/ip.link.after.txt" 2>&1
rec finished_utc "$(date -u +%FT%TZ)"
sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
finish_report
