#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|probe|full> — one job of the 9.9 session campaign (changelog D8–D14; method
# _dev/research/jioh/task-9.9-daemons-session/campaign/method.md). One subject, `session`: Ubuntu 24.04's desktop
# session, installed on the runner, logged in with nobody present, observed in its terminal idle state — the four
# entries that replace `system-daemon` (GNOME Shell, the PipeWire stack, `systemd`, `dbus-daemon`) in one session.
#
# Sequence (method §2, §3): install → priming login → logout → measured login → pin and first sweep →
# session-settle and idle-settle → second sweep → census → edge check → steady → census. Only `steady` is carried.
#
#   dry    shortened priming, the measured login idled past `idle-delay` and the blank, the edge check recorded
#          (not stopping the job), a short steady; the raw perf file kept (D13)
#   probe  a 30 min priming login and a 3 h phase on the measured login, both recorded and read per 10 s slice,
#          the idle state polled every 10 s during the recording (D13); never a repeat
#   full   the campaign; the priming, steady-offset and steady lengths come from the probe (method §9) and a job
#          without them stops before measuring
#
# Pinning (method §2.5; D10, D12, D14): the job's own shell starts on the harness CPUs (pin.sh). After the measured
# login is up, the four entries' units get the measured CPU and every other service and scope of both managers the
# harness CPUs; the second sweep at the steady edge reaches what the settles started.
#
# Settings: nothing from the trigger beyond the mode. Every value the design fixes is a constant below.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEAS="$(cd "$HERE/.." && pwd)"
source "$MEAS/probe/common.sh"          # OUT, KV, rec, finish_report
source "$MEAS/pin.sh"
pin_self_harness
APP="$1"; REPEAT="$2"; MODE="${3:-full}"
CENSUS="python3 $HERE/census.py"

# ---- design constants (method §2, §3) ----------------------------------------------------------------------
SESSION_USER=meas                    # the dedicated user of method §2.2
VIRTUAL_MONITOR=1920x1080@60         # method §2.3
LEADER_UNIT=meas-session             # the transient unit that is the session leader (D11)
LOGIN_WAIT=240                       # how long a login may take to bring GNOME Shell up before the job stops
LOGOUT_WAIT=90                       # how long the user manager may take to stop after the logout
POLL_S=10                            # the probe's state polls (D13)

# Lengths from the long-phase probe, written into method §10 before the first batch (method §9). Empty until then:
# a full job without them stops before measuring, as the desktop family's does.
priming_for()      { echo ""; }      # the priming login's length (D13)
steady_offset_for(){ echo ""; }      # measured login → steady edge: past both settles and the blank (D13)
steady_for()       { echo ""; }

if [ "$MODE" = dry ]; then
  PRIMING=60; STEADY_OFFSET=420; STEADY=60        # 420 s: idle-delay 300 s, the 10 s fade, the blank, a margin
elif [ "$MODE" = probe ]; then
  PRIMING=1800; STEADY_OFFSET=0; STEADY=10800     # D13: 30 min priming, 3 h on the measured login from the pin
else
  PRIMING="$(priming_for "$APP")"; STEADY_OFFSET="$(steady_offset_for "$APP")"; STEADY="$(steady_for "$APP")"
fi

# ---- instruments -------------------------------------------------------------------------------------------

edge() { printf '{"phase":"%s","edge":"%s","mono_ns":%s}\n' "$1" "$2" "$(date +%s%9N)" >> "$OUT/edges.jsonl"; }
census() { sudo $CENSUS snapshot "$MEAS_UID" "$1" "$OUT/census.$1.json" 2>> "$OUT/census.log"; rec "census.$1.rc" "$?"; }

# poller: the probe's state polls during a recording, one JSON line per POLL_S (D13), stated in its record
poll_start() { ( while :; do sudo $CENSUS state "$MEAS_UID" >> "$OUT/poll.$1.jsonl" 2>/dev/null; sleep "$POLL_S"; done ) &
               POLL_PID=$!; rec "poll.$1.interval_s" "$POLL_S"; }
poll_stop()  { [ -n "${POLL_PID:-}" ] && kill "$POLL_PID" 2>/dev/null; POLL_PID=""; }

# phase <name> <seconds> — perf over the whole phase, as the desktop family's phase(), with the census in place of
# the tree snapshot; the census runs before perf starts and after it stops (D13)
phase() {
  local name="$1" secs="$2"
  census "$name.start"
  edge "$name" start
  [ "$MODE" = probe ] && poll_start "$name"
  pin_harness sudo perf sched record -k CLOCK_MONOTONIC -a -o "$OUT/perf.$name.data" -- sleep "$secs" > "$OUT/perf.$name.log" 2>&1
  rec "perf.$name.record.rc" "$?"
  poll_stop
  edge "$name" end
  census "$name.end"
  rec "perf.$name.data_bytes" "$(stat -c %s "$OUT/perf.$name.data" 2>/dev/null || echo 0)"
  # --state: each row's switch-out state, the cross-check of the wakeup-row wake (9.5 D39)
  sudo perf sched timehist --state -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
  rec "perf.$name.timehist.rc" "${PIPESTATUS[0]}"
  sudo perf sched timehist -w -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | grep -E "awakened|wakeup|\bwaker\b" | gzip > "$OUT/perf.$name.wakeups.txt.gz"
  rec "perf.$name.wakeups.rows" "$(gzip -dc "$OUT/perf.$name.wakeups.txt.gz" | wc -l)"
  if [ "$MODE" = dry ]; then sudo gzip -f "$OUT/perf.$name.data"; else sudo rm -f "$OUT/perf.$name.data"; fi
}

# checkpoint <stage> — the machine's state after a stage (network, memory, failed units, the journal), and, in dry
# mode only, a clean stop there when MEAS_STOP_AFTER names it: a diagnostic, never a design value. The first dry run
# (2026-09-22) lost its runner with no log; parallel dry jobs stopping after successive stages locate what does.
checkpoint() {
  local st="$1" d="$OUT/diag.$1"
  mkdir -p "$d"
  ip -brief addr > "$d/ip.txt" 2>&1; ip route >> "$d/ip.txt" 2>&1
  networkctl list --no-pager > "$d/networkctl.txt" 2>&1
  nmcli -t dev > "$d/nmcli.txt" 2>&1; systemctl is-active NetworkManager >> "$d/nmcli.txt" 2>&1
  free -m > "$d/free.txt" 2>&1; uptime >> "$d/free.txt" 2>&1
  systemctl --failed --no-pager > "$d/failed.txt" 2>&1
  sudo journalctl -b --no-pager -n 600 > "$d/journal.txt" 2>&1
  sudo dmesg | tail -200 > "$d/dmesg.txt" 2>&1
  rec "diag.$st.github" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 https://api.github.com)"
  rec "diag.$st.utc" "$(date -u +%FT%TZ)"
  : > "$d/done"                       # the workflow's partial upload waits on this marker
  if [ "$MODE" = dry ] && [ "${MEAS_STOP_AFTER:-}" = "$st" ]; then
    rec stopped_after "$st"; stop_recorded open "dry run stopped after $st (MEAS_STOP_AFTER)"
  fi
}

stop_recorded() {   # <gate-value> <message> — the machine gate's shape, for a state that makes the job worthless
  poll_stop
  rec gate "$1"; rec finished_utc "$(date -u +%FT%TZ)"
  sudo systemctl stop "$LEADER_UNIT.service" 2>/dev/null
  sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
  finish_report
  echo "$2" >&2
  exit 0
}

# ---- the session (method §2) -------------------------------------------------------------------------------

ucmd() { sudo -u "$SESSION_USER" env "XDG_RUNTIME_DIR=/run/user/$MEAS_UID" \
           "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$MEAS_UID/bus" "$@"; }

# the Ubuntu Wayland session as GDM would start it: Exec and DesktopNames from the installed session file
session_file() {
  local f
  for f in /usr/share/wayland-sessions/ubuntu-wayland.desktop /usr/share/wayland-sessions/ubuntu.desktop; do
    [ -f "$f" ] && { echo "$f"; return; }
  done
}

install_session() {
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ubuntu-desktop-minimal > "$OUT/apt.desktop.log" 2>&1
  rec apt.desktop.rc "$?"
  local p
  for p in ubuntu-desktop-minimal gnome-shell mutter gnome-session pipewire wireplumber pipewire-pulse systemd dbus \
           dbus-daemon dbus-broker gdm3 gnome-initial-setup ubuntu-settings; do
    rec "version.$p" "$(dpkg-query -W -f='${Version}' "$p" 2>/dev/null)"
  done
  # D11: no display manager — the transient PAM unit below is the only login path
  sudo systemctl disable --now gdm.service > "$OUT/gdm.log" 2>&1; sudo systemctl mask gdm.service >> "$OUT/gdm.log" 2>&1
  rec gdm.masked "$(systemctl is-enabled gdm.service 2>/dev/null)"
  sudo loginctl terminate-user gdm >> "$OUT/gdm.log" 2>&1
  sleep 5
  rec gdm.procs_left "$(pgrep -u gdm 2>/dev/null | wc -l)"

  # D14: the cpuset controller delegated to the user manager, so the user side's AllowedCPUs= apply
  sudo mkdir -p /etc/systemd/system/user@.service.d
  printf '[Service]\nDelegate=pids memory cpu cpuset\n' | sudo tee /etc/systemd/system/user@.service.d/meas-cpuset.conf > /dev/null
  sudo systemctl daemon-reload

  sudo useradd -m -s /bin/bash "$SESSION_USER"; rec user.rc "$?"
  MEAS_UID="$(id -u "$SESSION_USER")"; rec user.uid "$MEAS_UID"

  # method §2.3: GNOME Shell headless with a virtual monitor — a user drop-in changing ExecStart= and nothing else,
  # the shipped command line kept and the two options appended
  local shipped
  shipped="$(sed -n 's/^ExecStart=//p' /usr/lib/systemd/user/org.gnome.Shell@wayland.service | head -1)"
  rec shell.exec_shipped "$shipped"
  local d="/home/$SESSION_USER/.config/systemd/user/org.gnome.Shell@wayland.service.d"
  sudo -u "$SESSION_USER" mkdir -p "$d"
  printf '[Service]\nExecStart=\nExecStart=%s --headless --virtual-monitor %s\n' "$shipped" "$VIRTUAL_MONITOR" \
    | sudo -u "$SESSION_USER" tee "$d/headless.conf" > /dev/null
  rec shell.exec "$shipped --headless --virtual-monitor $VIRTUAL_MONITOR"

  SESSION_FILE="$(session_file)"; rec session.file "${SESSION_FILE:-none}"
  SESSION_EXEC="$(sed -n 's/^Exec=//p' "$SESSION_FILE" 2>/dev/null | head -1)"
  SESSION_DESKTOPS="$(sed -n 's/^DesktopNames=//p' "$SESSION_FILE" 2>/dev/null | head -1 | tr ';' ':' | sed 's/:$//')"
  rec session.exec "$SESSION_EXEC"; rec session.desktop_names "$SESSION_DESKTOPS"
}

# login <label> — the seatless PAM login of D11: a transient system unit is the session leader
login() {
  local label="$1"
  edge "login-$label" start
  sudo systemd-run --unit="$LEADER_UNIT" --service-type=simple -p PAMName=login -p User="$SESSION_USER" \
    -p WorkingDirectory="/home/$SESSION_USER" \
    --setenv=XDG_SESSION_TYPE=wayland --setenv=XDG_SESSION_CLASS=user --setenv=XDG_SESSION_DESKTOP=ubuntu \
    --setenv=DESKTOP_SESSION=ubuntu --setenv=XDG_CURRENT_DESKTOP="$SESSION_DESKTOPS" \
    /bin/sh -c "exec $SESSION_EXEC" > "$OUT/login.$label.log" 2>&1
  rec "login.$label.rc" "$?"
  local t=0
  while [ "$t" -lt "$LOGIN_WAIT" ]; do
    [ "$(ucmd systemctl --user is-active org.gnome.Shell@wayland.service 2>/dev/null)" = active ] && break
    sleep 2; t=$((t + 2))
  done
  rec "login.$label.shell_up_s" "$t"
  edge "login-$label" end
  if [ "$t" -ge "$LOGIN_WAIT" ]; then
    sudo journalctl -b --no-pager -n 400 > "$OUT/journal.login-$label.txt" 2>&1
    ucmd journalctl --user -b --no-pager -n 400 > "$OUT/journal.user.login-$label.txt" 2>&1
    stop_recorded session-not-up "login $label: GNOME Shell not active after ${LOGIN_WAIT}s (method §9)"
  fi
  local u
  for u in dbus.service pipewire.service wireplumber.service pipewire-pulse.service; do
    rec "login.$label.active.$u" "$(ucmd systemctl --user is-active "$u" 2>/dev/null)"
  done
}

logout() {
  local label="$1" t=0
  edge "logout-$label" start
  sudo systemctl stop "$LEADER_UNIT.service"; rec "logout.$label.rc" "$?"
  while [ "$t" -lt "$LOGOUT_WAIT" ]; do
    systemctl is-active --quiet "user@$MEAS_UID.service" || break
    sleep 2; t=$((t + 2))
  done
  rec "logout.$label.user_manager_stopped_s" "$t"
  rec "logout.$label.user_manager_state" "$(systemctl is-active "user@$MEAS_UID.service" 2>/dev/null)"
  edge "logout-$label" end
}

# ---- pin and sweep (method §2.5; D10, D12, D14) ---------------------------------------------------------------

unit_id() { "$@" show -p Id --value 2>/dev/null | head -1; }   # resolves an alias: dbus.service -> dbus-broker.service

pin_four() {
  local bus u id fails=0
  sudo systemctl set-property --runtime init.scope AllowedCPUs="$MEAS_CPU" || fails=$((fails + 1))
  bus="$(systemctl show -p Id --value dbus.service 2>/dev/null)"; rec pin.system_bus_unit "$bus"
  sudo systemctl set-property --runtime "$bus" AllowedCPUs="$MEAS_CPU" || fails=$((fails + 1))
  PINNED_USER=""
  for u in dbus.service org.gnome.Shell@wayland.service pipewire.service wireplumber.service pipewire-pulse.service; do
    id="$(ucmd systemctl --user show -p Id --value "$u" 2>/dev/null | head -1)"
    PINNED_USER="$PINNED_USER $id"
    ucmd systemctl --user set-property --runtime "$id" AllowedCPUs="$MEAS_CPU" || fails=$((fails + 1))
  done
  rec pin.user_units "${PINNED_USER# }"
  # the user manager by its own cgroup, so what it forks later does not inherit the measured CPU (D14). Written
  # after the user units, whose AllowedCPUs= make the user manager enable cpuset below its service.
  local cg="/sys/fs/cgroup/user.slice/user-$MEAS_UID.slice/user@$MEAS_UID.service/init.scope"
  echo "$MEAS_CPU" | sudo tee "$cg/cpuset.cpus" > /dev/null || fails=$((fails + 1))
  rec pin.user_manager_cpuset "$(cat "$cg/cpuset.cpus.effective" 2>/dev/null)"
  rec pin.fails "$fails"
}

# sweep <n>: every loaded service and scope of both managers other than the four entries' units, their ancestors
# and the measured user's user@ service goes to the harness CPUs (D12)
sweep() {
  local n="$1" u moved=0 failed=0 keep_sys keep_user
  keep_sys="^(init\.scope|$(systemctl show -p Id --value dbus.service 2>/dev/null | sed 's/\./\\./g')|user@$MEAS_UID\.service)$"
  keep_user="^(init\.scope|$(echo $PINNED_USER | sed 's/\./\\./g; s/ /|/g'))$"
  : > "$OUT/sweep.$n.txt"
  while read -r u _; do
    [ -z "$u" ] && continue
    if [[ "$u" =~ $keep_sys ]]; then echo "system keep $u" >> "$OUT/sweep.$n.txt"; continue; fi
    if sudo systemctl set-property --runtime "$u" AllowedCPUs="$MEAS_HARNESS_CPUS" 2>/dev/null; then
      moved=$((moved + 1)); echo "system moved $u" >> "$OUT/sweep.$n.txt"
    else failed=$((failed + 1)); echo "system failed $u" >> "$OUT/sweep.$n.txt"; fi
  done < <(systemctl list-units --type=service,scope --state=active,activating,reloading --no-legend --plain --no-pager)
  while read -r u _; do
    [ -z "$u" ] && continue
    if [[ "$u" =~ $keep_user ]]; then echo "user keep $u" >> "$OUT/sweep.$n.txt"; continue; fi
    if ucmd systemctl --user set-property --runtime "$u" AllowedCPUs="$MEAS_HARNESS_CPUS" 2>/dev/null; then
      moved=$((moved + 1)); echo "user moved $u" >> "$OUT/sweep.$n.txt"
    else failed=$((failed + 1)); echo "user failed $u" >> "$OUT/sweep.$n.txt"; fi
  done < <(ucmd systemctl --user list-units --type=service,scope --state=active,activating,reloading --no-legend --plain --no-pager)
  rec "sweep.$n.moved" "$moved"; rec "sweep.$n.failed" "$failed"
}

# ---- the job ---------------------------------------------------------------------------------------------------

rec family session; rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec settings.virtual_monitor "$VIRTUAL_MONITOR"; rec settings.session_user "$SESSION_USER"
rec priming_s "${PRIMING:-unset}"; rec steady_offset_s "${STEADY_OFFSET:-unset}"; rec steady_s "${STEADY:-unset}"
pin_record | tee -a "$KV" | sed 's/^/  /' >&2
python3 "$MEAS/runner_spec.py" > "$OUT/spec.json"

# same-machine repeats (9.6 D10; 9.5 D26): a job that drew another CPU model stops here, recorded, before any
# install or measurement
source "$MEAS/machine_gate.sh"
rec machine.model "$(machine_model)"; rec machine.wanted "${MEAS_CPU_MODEL:-}"
if ! machine_gate "${MEAS_CPU_MODEL:-}"; then
  rec gate wrong-machine; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "machine gate: wanted '${MEAS_CPU_MODEL}', drew '$(machine_model)' — stopping before any measurement" >&2
  exit 0
fi
if [ "$APP" != session ]; then
  rec gate unknown-app; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "unknown subject $APP (the one subject is session)" >&2; exit 0
fi
if [ -z "$PRIMING" ] || [ -z "$STEADY_OFFSET" ] || [ -z "$STEADY" ]; then
  rec gate no-phase-lengths; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "phases: no priming, steady-offset or steady length stated (method §9) — stopping before any measurement" >&2
  exit 0
fi
rec gate open
# the journal followed from here on, so a partial upload carries what happened up to it
sudo journalctl -f -o short-monotonic --no-pager > "$OUT/journal.follow.txt" 2>&1 &
JOURNAL_PID=$!

sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
rec kernel "$(uname -r)"
grep -E "CONFIG_(PERF_EVENTS|SCHED_TRACER|TASKSTATS|TASK_DELAY_ACCT|HZ)" "/boot/config-$(uname -r)" > "$OUT/kconfig.txt" 2>/dev/null
rec kernel.hz "$(grep -E '^CONFIG_HZ=' "/boot/config-$(uname -r)" 2>/dev/null | head -1)"

install_session
[ -n "$SESSION_EXEC" ] || stop_recorded no-session-file "no Ubuntu Wayland session file after the install (method §2.1)"
checkpoint install

# priming login (D11): the account's first-login work, then a logout. The probe records it (D13).
login priming
census priming.up
if [ "$MODE" = probe ]; then phase priming "$PRIMING"
else edge priming start; sleep "$PRIMING"; edge priming end; census priming.end; fi
rec wizard.seen_priming "$(python3 -c "import json,sys; print(sum('initial-setup' in p['cmd'] for f in sys.argv[1:] for p in json.load(open(f))['procs']))" "$OUT/census.priming.up.json" "$OUT/census.priming.end.json" 2>/dev/null)"
logout priming
checkpoint priming
# the first-run wizard dismissed as a user would, by its done stamp (D11), if the install ships it
if [ -e /usr/libexec/gnome-initial-setup ]; then
  echo yes | sudo -u "$SESSION_USER" tee "/home/$SESSION_USER/.config/gnome-initial-setup-done" > /dev/null
  rec wizard.stamp 1
else
  rec wizard.stamp 0
fi

# the measured login
LOGIN_T0=$(date +%s)
login measured
census login
pin_four
sweep 1
census pinned
checkpoint pinned

if [ "$MODE" = probe ]; then
  phase idle "$STEADY"                         # one long phase from the pin: settles, shield, blank, and after
else
  left=$(( LOGIN_T0 + STEADY_OFFSET - $(date +%s) )); rec steady.wait_s "$left"
  [ "$left" -gt 0 ] && sleep "$left"
  sweep 2
  sudo $CENSUS state "$MEAS_UID" > "$OUT/state.edge.json" 2>> "$OUT/census.log"
  if sudo $CENSUS check "$OUT/state.edge.json"; then rec edge.idle 1; else rec edge.idle 0; fi
  checkpoint edge
  if [ "$MODE" = full ] && [ "$(sed -n 's/^edge.idle=//p' "$KV" | tail -1)" != 1 ]; then
    census steady.start
    stop_recorded not-idle "steady edge: the session is not in the terminal idle state (method §3, D13)"
  fi
  phase steady "$STEADY"
fi

logout measured
checkpoint end
rec finished_utc "$(date -u +%FT%TZ)"
sudo kill "$JOURNAL_PID" 2>/dev/null
sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
finish_report
