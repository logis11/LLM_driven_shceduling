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
#          the idle state polled every 10 s up to the steady edge and not past it (D13, D19); never a repeat
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
POLL_UNTIL=""                        # epoch second the polls stop at; set for the probe's measured phase (D19)
# How the session is logged in. `unit` is D11's transient PAM unit with GDM masked. GNOME Shell creates its screen
# shield only when a display manager answers on the system bus (gnome-shell 46.0 js/ui/main.js:230,
# js/misc/loginManager.js:38-53), so with `unit` alone the session never locks and never blanks: `gdm` logs in
# through GDM's automatic login instead, `stub` keeps D11's login and adds dm_stub.py on the system bus. The two
# are compared in a dry run before either is decided (Q14).
LOGIN_MODE="${MEAS_LOGIN_MODE:-gdm}"   # D16: GDM's automatic login; `unit` and `stub` are the compared alternatives

# Lengths from the long-phase probe, written into method §10 before the first batch (method §9). Empty until then:
# a full job without them stops before measuring, as the desktop family's does.
# Set from the long-phase probe of 2026-09-22 (run 35798819217; D18). The first-login work is over inside the
# first minute — the indexer crawls the empty home in under 60 s and gnome-initial-setup runs only in minute 0.
priming_for()      { echo 300; }
# The shield rises and the monitor blanks 304 s after the login (idle-delay 300 s and the 10 s fade, polls 10 s
# apart), and GNOME Shell's wake rate settles at the same moment; 420 s leaves a margin past it.
steady_offset_for(){ echo 420; }
# Withdrawn (D19): the 900 s of D18 rested on window spreads of a signal the probe's own 10 s polls dominated —
# at idle the entries wake 0.1-0.9 /s in an unpolled dry run against 15.06, 4.25, 3.67 and 2.17 /s in the probe —
# and a periodic instrument makes a spread read smaller than the subject's. Empty until the unpolled probe sets it,
# so a full job stops at the no-phase-lengths gate.
steady_for()       { echo; }

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

# poller: the probe's state polls during a recording, one JSON line per POLL_S (D13), stated in its record.
# A poll is five `sudo` commands — four `busctl --user` calls and `loginctl` — and every `sudo -u` registers a
# logind session, so the poll itself wakes the four entries it reads. D19 stops it at the steady edge: the settles
# stay polled, the region a full job carries is not. poll_start <phase> [stop-epoch]; no epoch, no bound.
poll_start() { local name="$1" until_epoch="${2:-}"
               ( while :; do
                   sudo $CENSUS state "$MEAS_UID" >> "$OUT/poll.$name.jsonl" 2>/dev/null
                   if [ -n "$until_epoch" ] && [ "$(date +%s)" -ge "$until_epoch" ]; then break; fi
                   sleep "$POLL_S"
                 done ) &
               POLL_PID=$!; rec "poll.$name.interval_s" "$POLL_S"
               [ -n "$until_epoch" ] && rec "poll.$name.until_epoch" "$until_epoch"; }
poll_stop()  { [ -n "${POLL_PID:-}" ] && kill "$POLL_PID" 2>/dev/null; POLL_PID=""; }

# phase <name> <seconds> — perf over the whole phase, as the desktop family's phase(), with the census in place of
# the tree snapshot; the census runs before perf starts and after it stops (D13)
phase() {
  local name="$1" secs="$2"
  census "$name.start"
  edge "$name" start
  [ "$MODE" = probe ] && poll_start "$name" "${POLL_UNTIL:-}"
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

# D21: `meas.slice` and the system bus's place in it, taken before the desktop is installed.
#
# A unit takes its slice when it starts, and this bus has run since boot, so a `Slice=` drop-in alone leaves it in
# `system.slice` — which D17's default then holds on the harness CPUs. That is how the 2026-09-23 probes measured
# an entry off the measured CPU with `pin.fails` 0. The bus is therefore restarted; it is done here, while its
# clients are still the base system services and no session exists.
#
# A bus restart leaves every service that had claimed a well-known name on the old bus connected to nothing: in
# the dry jobs of 2026-09-23 (32, 33) `systemd-logind` kept running without `org.freedesktop.login1`, GDM timed
# out activating it after 25 s, and no session was ever created. Every running service that declares a `BusName=`
# is restarted with the bus so that it claims its name again, and logind is then asked a question before the job
# goes on.
bus_into_meas_slice() {
  local u bus named=""
  printf '[Unit]\nDescription=Measured slice (9.9 campaign)\n[Slice]\nAllowedCPUs=%s\n' "$MEAS_CPU" \
    | sudo tee /etc/systemd/system/meas.slice > /dev/null
  for u in dbus dbus-broker; do
    sudo mkdir -p "/etc/systemd/system/$u.service.d"
    printf '[Service]\nSlice=meas.slice\n' | sudo tee "/etc/systemd/system/$u.service.d/meas-slice.conf" > /dev/null
  done
  sudo systemctl daemon-reload
  bus="$(systemctl show -p Id --value dbus.service 2>/dev/null)"; rec dbus.restart.unit "$bus"
  sudo systemctl restart "$bus" > "$OUT/dbus.restart.log" 2>&1; rec dbus.restart.rc "$?"
  for u in $(systemctl list-units --type=service --state=running --no-legend --plain 2>/dev/null | awk '{print $1}'); do
    [ "$u" = "$bus" ] && continue
    [ -n "$(systemctl show -p BusName --value "$u" 2>/dev/null)" ] || continue
    echo "== try-restart $u" >> "$OUT/dbus.restart.log"
    sudo systemctl try-restart "$u" >> "$OUT/dbus.restart.log" 2>&1 && named="$named $u"
  done
  rec dbus.restart.renamed "${named# }"
  rec dbus.restart.cgroup "$(systemctl show -p ControlGroup --value "$bus" 2>/dev/null)"
  # logind answering on the new bus is what GDM needs; a job whose bus restart broke it measures nothing
  sudo busctl --system get-property org.freedesktop.login1 /org/freedesktop/login1 \
    org.freedesktop.login1.Manager NAutoVTs > "$OUT/bus.login1.txt" 2>&1; rec bus.login1.rc "$?"
  if [ "$(sed -n 's/^bus.login1.rc=//p' "$KV" | tail -1)" != 0 ]; then
    stop_recorded bus-no-login1 "the system bus restarted into meas.slice but org.freedesktop.login1 does not answer (D21)"
  fi
}

install_session() {
  bus_into_meas_slice
  # services are not started by the packages' scripts (policy-rc.d 101) nor restarted by needrestart: every dry job of
  # 2026-09-22 that lost its runner lost it in the install's last service starts. The units are started afterwards,
  # one at a time and logged, as a boot would start them (start_boot_units).
  printf '#!/bin/sh\nexit 101\n' | sudo tee /usr/sbin/policy-rc.d > /dev/null; sudo chmod +x /usr/sbin/policy-rc.d
  sudo DEBIAN_FRONTEND=noninteractive NEEDRESTART_SUSPEND=1 apt-get install -y ubuntu-desktop-minimal > "$OUT/apt.desktop.log" 2>&1
  rec apt.desktop.rc "$?"
  sudo rm -f /usr/sbin/policy-rc.d
  local p
  for p in ubuntu-desktop-minimal gnome-shell mutter gnome-session pipewire wireplumber pipewire-pulse systemd dbus \
           dbus-daemon dbus-broker gdm3 gnome-initial-setup ubuntu-settings; do
    rec "version.$p" "$(dpkg-query -W -f='${Version}' "$p" 2>/dev/null)"
  done
  # D11: no display manager — the transient PAM unit is the login path — except in login mode `gdm`, where GDM's
  # own automatic login is the path and GDM stays as installed
  if [ "$LOGIN_MODE" != gdm ]; then
    sudo systemctl disable --now gdm.service > "$OUT/gdm.log" 2>&1; sudo systemctl mask gdm.service >> "$OUT/gdm.log" 2>&1
    sudo loginctl terminate-user gdm >> "$OUT/gdm.log" 2>&1
    sleep 5
  fi
  rec gdm.masked "$(systemctl is-enabled gdm.service 2>/dev/null)"
  rec gdm.procs_left "$(pgrep -u gdm 2>/dev/null | wc -l)"

  # the runner image exports its own XDG paths to every login through /etc/environment, which sends the session's
  # settings, its dconf database and the wizard's stamp to /home/runner; the file is restored to the stock lines
  cp /etc/environment "$OUT/environment.before" 2>/dev/null
  sudo sed -i '/^XDG_/d;/^HOME=/d;/^XDG/d' /etc/environment
  cp /etc/environment "$OUT/environment.after" 2>/dev/null

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

  if [ "$LOGIN_MODE" = gdm ]; then     # GDM's automatic login of the measured user, Wayland (Q14 test)
    printf '[daemon]\nWaylandEnable=true\nAutomaticLoginEnable=true\nAutomaticLogin=%s\n' "$SESSION_USER" \
      | sudo tee /etc/gdm3/custom.conf > /dev/null
    rec gdm.autologin "$SESSION_USER"
  fi
  # D17: the placement is a slice default, so a unit a timer starts during the measured window inherits the other
  # CPUs. The four entries move into a slice of their own; pid 1's init.scope and the user manager's are outside
  # these slices already. The system side of this — `meas.slice` and the system bus's place in it — is written and
  # taken before the install, by bus_into_meas_slice (D21).
  local u
  local ud="/home/$SESSION_USER/.config/systemd/user"
  sudo -u "$SESSION_USER" mkdir -p "$ud"
  printf '[Unit]\nDescription=Measured slice (9.9 campaign)\n[Slice]\nAllowedCPUs=%s\n' "$MEAS_CPU" \
    | sudo -u "$SESSION_USER" tee "$ud/meas.slice" > /dev/null
  for u in dbus org.gnome.Shell@wayland pipewire wireplumber pipewire-pulse; do
    sudo -u "$SESSION_USER" mkdir -p "$ud/$u.service.d"
    printf '[Service]\nSlice=meas.slice\n' | sudo -u "$SESSION_USER" tee "$ud/$u.service.d/meas-slice.conf" > /dev/null
  done
  sudo systemctl daemon-reload
  rec slices.written 1

  SESSION_FILE="$(session_file)"; rec session.file "${SESSION_FILE:-none}"
  SESSION_EXEC="$(sed -n 's/^Exec=//p' "$SESSION_FILE" 2>/dev/null | head -1)"
  SESSION_DESKTOPS="$(sed -n 's/^DesktopNames=//p' "$SESSION_FILE" 2>/dev/null | head -1 | tr ';' ':' | sed 's/:$//')"
  rec session.exec "$SESSION_EXEC"; rec session.desktop_names "$SESSION_DESKTOPS"
}

# the units graphical.target wants that the install left inactive, started one at a time, each logged before it
# starts so the last line names the unit that was starting if the runner is lost (gdm is masked by then)
start_boot_units() {
  local u n=0 rc
  : > "$OUT/units.start.log"
  while read -r u; do
    case "$u" in *.service|*.socket|*.path|*.timer) ;; *) continue ;; esac
    systemctl is-active --quiet "$u" && continue
    [ "$(systemctl is-enabled "$u" 2>/dev/null)" = masked ] && continue
    echo "$(date -u +%T) start $u" >> "$OUT/units.start.log"; sync
    timeout 90 sudo systemctl start "$u" > /dev/null 2>&1; rc=$?
    echo "$(date -u +%T) rc=$rc $u" >> "$OUT/units.start.log"; sync
    n=$((n + 1)); sleep 2
  done < <(systemctl list-dependencies --plain --no-pager graphical.target 2>/dev/null | sed 's/^[^a-zA-Z0-9@._-]*//' | sort -u)
  rec units.started "$n"
}

# dm_stub — the stand-in display manager of login mode `stub`: the one property gnome-shell's canLock() asks for
start_dm_stub() {
  printf '<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN" "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">\n<busconfig><policy user="root"><allow own="org.gnome.DisplayManager"/></policy><policy context="default"><allow send_destination="org.gnome.DisplayManager"/></policy></busconfig>\n' \
    | sudo tee /etc/dbus-1/system.d/meas-dm-stub.conf > /dev/null
  sudo systemctl reload dbus.service 2>/dev/null
  sudo setsid python3 "$HERE/dm_stub.py" "$(dpkg-query -W -f='${Version}' gdm3 2>/dev/null | sed 's/-.*//;s/[^0-9.].*//')" \
    > "$OUT/dm_stub.log" 2>&1 &
  sleep 3
  rec dm_stub.owner "$(sudo busctl --system call org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus GetNameOwner s org.gnome.DisplayManager 2>&1 | tail -c 60)"
  rec dm_stub.version "$(sudo busctl --system get-property org.gnome.DisplayManager /org/gnome/DisplayManager/Manager org.gnome.DisplayManager.Manager Version 2>&1 | tail -c 40)"
}

# login <label> — the seatless PAM login of D11: a transient system unit is the session leader; in login mode `gdm`
# the login is GDM's automatic one instead, started (and restarted, for the measured login) with the service
login() {
  local label="$1"
  if [ "$LOGIN_MODE" = gdm ]; then
    edge "login-$label" start
    sudo systemctl restart gdm.service > "$OUT/login.$label.log" 2>&1; rec "login.$label.rc" "$?"
    wait_for_shell "$label"
    return
  fi
  edge "login-$label" start
  sudo systemd-run --unit="$LEADER_UNIT" --service-type=simple -p PAMName=login -p User="$SESSION_USER" \
    -p WorkingDirectory="/home/$SESSION_USER" \
    --setenv=XDG_SESSION_TYPE=wayland --setenv=XDG_SESSION_CLASS=user --setenv=XDG_SESSION_DESKTOP=ubuntu \
    --setenv=DESKTOP_SESSION=ubuntu --setenv=XDG_CURRENT_DESKTOP="$SESSION_DESKTOPS" \
    /bin/sh -c "exec $SESSION_EXEC" > "$OUT/login.$label.log" 2>&1
  rec "login.$label.rc" "$?"
  wait_for_shell "$label"
}

wait_for_shell() {
  local label="$1"
  if [ "$LOGIN_MODE" = gdm ]; then     # the user's uid exists before the session does; wait for its manager first
    local w=0
    while [ "$w" -lt "$LOGIN_WAIT" ] && ! systemctl is-active --quiet "user@$MEAS_UID.service"; do sleep 2; w=$((w + 2)); done
    rec "login.$label.user_manager_s" "$w"
  fi
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
  if [ "$LOGIN_MODE" = gdm ]; then
    sudo loginctl terminate-user "$SESSION_USER" > /dev/null 2>&1; rec "logout.$label.rc" "$?"
  else
    sudo systemctl stop "$LEADER_UNIT.service"; rec "logout.$label.rc" "$?"
  fi
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
  local bus u id fails=0 sl
  # D17: the slices everything else lands in, including what a timer starts later
  sudo systemctl set-property --runtime system.slice AllowedCPUs="$MEAS_HARNESS_CPUS" || fails=$((fails + 1))
  for sl in app.slice session.slice background.slice; do
    ucmd systemctl --user set-property --runtime "$sl" AllowedCPUs="$MEAS_HARNESS_CPUS" || fails=$((fails + 1))
  done
  rec pin.slice_defaults "$MEAS_HARNESS_CPUS"
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
  # D21: the control group each entry's unit is actually in — `Slice=` reports the configuration, which a unit
  # running since boot has not taken
  rec pin.entry_cgroups "$(systemctl show -p ControlGroup --value dbus.service 2>/dev/null) $(ucmd systemctl --user show -p ControlGroup --value org.gnome.Shell@wayland.service 2>/dev/null)"
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
  adopt "$n"
}

# adopt <n>: the processes in the pinned units that are none of the entries' — services the session bus starts on
# demand, a helper GNOME Shell forks, (sd-pam) beside the user manager — moved into a scope of their own on the
# harness CPUs, created by the manager owning their unit with StartTransientUnit's PIDs (changelog D15)
adopt() {
  local n="$1" m pids_user="" pids_sys="" rc
  m="$($CENSUS mask "$MEAS_HARNESS_CPUS")"
  while read -r mgr pid; do
    case "$mgr" in user) pids_user="$pids_user $pid" ;; system) pids_sys="$pids_sys $pid" ;; esac
  done < <(sudo $CENSUS others "$MEAS_UID")
  echo "adopt $n user:$pids_user system:$pids_sys" >> "$OUT/sweep.$n.txt"
  set -- $pids_user
  if [ "$#" -gt 0 ]; then
    ucmd busctl --user call org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager \
      StartTransientUnit 'ssa(sv)a(sa(sv))' "meas-offcpu-$n.scope" fail 2 PIDs au "$#" "$@" AllowedCPUs $m 0 \
      >> "$OUT/sweep.$n.txt" 2>&1; rc=$?
    rec "sweep.$n.adopted_user" "$#"; rec "sweep.$n.adopt_user.rc" "$rc"
  fi
  set -- $pids_sys
  if [ "$#" -gt 0 ]; then
    sudo busctl call org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager \
      StartTransientUnit 'ssa(sv)a(sa(sv))' "meas-offcpu-$n.scope" fail 2 PIDs au "$#" "$@" AllowedCPUs $m 0 \
      >> "$OUT/sweep.$n.txt" 2>&1; rc=$?
    rec "sweep.$n.adopted_system" "$#"; rec "sweep.$n.adopt_system.rc" "$rc"
  fi
  rec "sweep.$n.left_in_units" "$(sudo $CENSUS others "$MEAS_UID" | wc -l)"
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

rec settings.login_mode "$LOGIN_MODE"
install_session
[ "$LOGIN_MODE" = stub ] && start_dm_stub
[ -n "$SESSION_EXEC" ] || stop_recorded no-session-file "no Ubuntu Wayland session file after the install (method §2.1)"
checkpoint install
start_boot_units
checkpoint units

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
# D21: the placement of method §2.5 read from the processes, before anything is measured
if sudo $CENSUS placed "$OUT/census.pinned.json" "$MEAS_CPU" > "$OUT/placement.pinned.txt" 2>&1; then
  rec placement.pinned 1
else
  rec placement.pinned 0; echo "placement (pinned census):" >&2; cat "$OUT/placement.pinned.txt" >&2
fi
if [ "$MODE" != dry ] && [ "$(sed -n 's/^placement.pinned=//p' "$KV" | tail -1)" != 1 ]; then
  stop_recorded misplaced-entry "the entries are not alone on the measured CPU (method §2.5, D21); see placement.pinned.txt"
fi
checkpoint pinned

if [ "$MODE" = probe ]; then
  # D19: the polls stop at the edge a full job measures from, so the settles are read and the carried region is not
  # polled. The offset is the login's, as in a full job; the phase starts at the pin, a little after it.
  POLL_UNTIL=$(( LOGIN_T0 + $(steady_offset_for "$APP") ))
  phase idle "$STEADY"                         # one long phase from the pin: settles, shield, blank, and after
else
  left=$(( LOGIN_T0 + STEADY_OFFSET - $(date +%s) )); rec steady.wait_s "$left"
  [ "$left" -gt 0 ] && sleep "$left"
  sweep 2
  census edge
  if sudo $CENSUS placed "$OUT/census.edge.json" "$MEAS_CPU" > "$OUT/placement.edge.txt" 2>&1; then
    rec placement.edge 1
  else
    rec placement.edge 0; echo "placement (edge census):" >&2; cat "$OUT/placement.edge.txt" >&2
  fi
  if [ "$MODE" = full ] && [ "$(sed -n 's/^placement.edge=//p' "$KV" | tail -1)" != 1 ]; then
    stop_recorded misplaced-entry "the entries are not alone on the measured CPU at the steady edge (method §2.5, D21)"
  fi
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
