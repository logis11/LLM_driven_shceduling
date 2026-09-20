#!/usr/bin/env bash
# run.sh <app> <repeat> <dry|probe|full> — one job of the 9.8 desktop campaign (changelog D13; method
# _dev/research/jioh/task-9.8-browser-comms/campaign/method.md). One subject per job, so one subject's failure
# does not cost the others:
#
#   chrome-hidden   one window, a foreground control tab and N measured background tabs at N loopback origins,
#                   observed past the intensive-throttling grace
#   chrome-visible  the same page set as N windows, one tab each; two steady phases, the second with the page's
#                   timer removed by navigation rather than relaunch
#   element         Element Desktop signed in to a Synapse homeserver on the harness CPUs; idle then traffic
#   steam           Valve's desktop client, logged out, under a window manager; shown then minimised
#
# Phases are a sequence with recorded edges (method §3), not one settle figure: launch, launch-settle, for the
# hidden subject the recorded moment the tabs are backgrounded, grace-settle, then the steady phase(s). Only a
# steady phase is carried.
#
# Single-core (pin.sh; 9.5 follow-ups spec decisions 2 and 5): this script and everything it starts — Xvfb, the
# window manager, perf, the page server, Synapse, the traffic driver — run on the harness CPUs; only the
# application tree is launched on the measured CPU.
#
# Settings: nothing from the trigger beyond the mode (D13). Every value the design fixes is a constant below,
# because a pool whose repeats ran at different N or different phase lengths is not a pool. The trigger carries
# mode, attempt, cpu_model, apps and repeats only.
set -u
export PROBE_OUT="${MEAS_OUT:-/tmp/meas}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEAS="$(cd "$HERE/.." && pwd)"
source "$MEAS/probe/common.sh"          # OUT, KV, TOOLS, rec, finish_report, start_xvfb, wait_window, snap, screenshot
source "$MEAS/pin.sh"
pin_self_harness
source "$TOOLS/appdefs.sh"              # appdef, apt_install, ver, appdef_cleanup
APP="$1"; REPEAT="$2"; MODE="${3:-full}"
PH="$MEAS/phase.sh $OUT/phases.jsonl"
export MEAS_PIN=harness                 # phase.sh here wraps drivers, which act on the pinned application from the harness CPUs
APP_PID=0; WID=""; PAT="?"; RX="?"

# ---- design constants (method §2, §3) ----------------------------------------------------------------------
ORIGINS=12                  # N: distinct loopback origins, hence distinct site-locked renderers
TIMER_MS=100                # the page's setInterval period; above both throttling caps
PAGE_PORT=8099
# The grace before intensive throttling is sixty seconds for a page that has finished loading and five minutes
# by default. Per-tab load completion is not observable from outside the browser, so the grace-settle covers the
# default: the steady phase then begins throttled whichever class Chromium put the pages in.
GRACE_S=330
PROBE_PERIODS="50 100 500"  # the visible subject's period sweep, run as successive phases of one probe job (D13)
HOMESERVER=synapse
TRAFFIC_PER_MIN=60          # instrument setting, not a claim about users (method §2 subject 4)
MATRIX_USER=meas; MATRIX_PASS=meas-9.8-local; MATRIX_SECRET=meas-9-8-registration-secret
SYNAPSE_PORT=8008; SYNAPSE_DIR=/tmp/synapse

# Steady-phase lengths come from the long-phase probe and are written into method §10 before the first batch
# (method §3, 9.5 D35). A subject without one stops before measuring, as campaign/run.sh's settle_for() does.
launch_settle_for() { case "$1" in *) echo "" ;; esac; }
steady_for()        { case "$1" in *) echo "" ;; esac; }

if [ "$MODE" = dry ]; then
  LAUNCH_SETTLE=20; STEADY=45; GRACE_S=75; ORIGINS=3; PROBE_PERIODS="100"
elif [ "$MODE" = probe ]; then
  LAUNCH_SETTLE=20; STEADY=1800          # one long phase, read per 10 s slice by campaign/slices.py
else
  LAUNCH_SETTLE="$(launch_settle_for "$APP")"; STEADY="$(steady_for "$APP")"
fi

# ---- instruments -------------------------------------------------------------------------------------------

edge() { printf '{"phase":"%s","edge":"%s","mono_ns":%s}\n' "$1" "$2" "$(date +%s%9N)" >> "$OUT/edges.jsonl"; }

# phase <name> <seconds> <driver-cmd or ''> — copied from campaign/run.sh's phase() (D13: copied, not extracted;
# 9.5 is still adding repeats through that file). perf over the whole phase, driver inside it.
phase() {
  local name="$1" secs="$2" driver="$3"
  edge "$name" start
  snap "$PAT" "" "$name.before"
  pin_harness sudo perf sched record -k CLOCK_MONOTONIC -a -o "$OUT/perf.$name.data" -- sleep "$secs" > "$OUT/perf.$name.log" 2>&1 &
  local perf_pid=$!
  sleep 1
  if [ -n "$driver" ]; then
    $PH "$name-driver" -- bash -c "$driver" > "$OUT/driver.$name.log" 2>&1
  fi
  wait "$perf_pid"; rec "perf.$name.record.rc" "$?"
  snap "$PAT" "" "$name.after"
  screenshot "after-$name"
  # --state: each row's switch-out state, the cross-check of the wakeup-row wake (9.5 D39)
  sudo perf sched timehist --state -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | gzip > "$OUT/perf.$name.timehist.txt.gz"
  rec "perf.$name.timehist.rc" "${PIPESTATUS[0]}"
  rec "perf.$name.rows_matching" "$(gzip -dc "$OUT/perf.$name.timehist.txt.gz" | grep -cE "$RX" || echo 0)"
  sudo perf sched timehist -w -i "$OUT/perf.$name.data" 2>> "$OUT/perf.$name.log" | grep -E "awakened|wakeup|\bwaker\b" | gzip > "$OUT/perf.$name.wakeups.txt.gz"
  rec "perf.$name.wakeups.rows" "$(gzip -dc "$OUT/perf.$name.wakeups.txt.gz" | wc -l)"
  if [ "$MODE" = dry ]; then gzip -f "$OUT/perf.$name.data"; else rm -f "$OUT/perf.$name.data"; fi
  edge "$name" end
}

stop_recorded() {   # <gate-value> <message> — the machine gate's shape, for a state that makes the job worthless
  rec gate "$1"; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "$2" >&2
  kill -- "-$APP_PID" 2>/dev/null; appdef_cleanup
  exit 0
}

launch_app() {
  # launched directly under taskset, not through pin_load: a function run in the background forks a subshell, so
  # $! would be the subshell and not the session leader the kill and the affinity record need (campaign/run.sh)
  if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_CPU" setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 &
  else setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 & fi
  APP_PID=$!
  rec app.affinity "$(taskset -p "$APP_PID" 2>/dev/null | sed 's/.*: //' || echo unknown)"
}

# ---- the renderer subjects ---------------------------------------------------------------------------------

# renderer_gate <expected-minimum> — decision 9: the count is knowable right after the settle, and a job that
# came up with too few renderers measured something else, with the steady phase still ahead of it. Extra
# renderers (Chromium keeps a spare) are benign and fall into the components' residual, so the test is a
# minimum. Roles are read exactly as campaign/analyze.py's pid_roles does, from the command line the snapshot
# records — truncated to 120 characters, which --type=renderer sits well inside.
renderer_gate() {
  local want="$1" n
  snap "$PAT" "" gate
  n="$(python3 -c 'import json,sys; print(sum(1 for p in json.load(open(sys.argv[1]))["procs"] if "--type=renderer" in p.get("cmd","")))' "$OUT/snap.gate.json" 2>/dev/null || echo 0)"
  rec renderers.observed "$n"; rec renderers.wanted_min "$want"
  [ "$n" -ge "$want" ] || stop_recorded wrong-renderer-count "renderer gate: wanted at least $want renderers, observed $n — stopping before the steady phase"
}

# navigate <window-id> <url> — through the omnibox, as ops_driver.py's chrome operation drives it
navigate() {
  pin_harness xdotool windowactivate --sync "$1"
  pin_harness xdotool key --clearmodifiers ctrl+l; sleep 0.3
  pin_harness xdotool type --delay 5 "$2"
  pin_harness xdotool key --clearmodifiers Return
}

navigate_all() {   # <url> — every window of the browser, so both phases observe one process tree
  local w
  for w in $(pin_harness xdotool search --onlyvisible --class "$CLASS" 2>/dev/null); do navigate "$w" "$1"; done
  sleep 15
}

chrome_subject() {
  export MEAS_ORIGINS="$ORIGINS" MEAS_TIMER_MS="$TIMER_MS" MEAS_PAGE_PORT="$PAGE_PORT"
  appdef "$APP" || exit 0
  rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"
  launch_app
  WID=$(wait_window "$CLASS" 120)
  [ -n "$WID" ] || { screenshot no-window; stop_recorded no-window "no browser window after 120 s"; }
  if [ -n "$POSTLAUNCH" ]; then bash -c "$POSTLAUNCH" > "$OUT/postlaunch.log" 2>&1; screenshot after-postlaunch; fi
  edge launch-settle start; sleep "$LAUNCH_SETTLE"; edge launch-settle end
  screenshot after-launch-settle
  if [ "$APP" = chrome-hidden ]; then
    renderer_gate "$((ORIGINS + 1))"
    # the measured tabs are background pages from the launch — the control tab is first and stays selected — so
    # the grace runs from here, and the moment is recorded rather than folded into one settle figure
    edge backgrounded mark
    edge grace-settle start; sleep "$GRACE_S"; edge grace-settle end
    phase steady "$STEADY" ""
  else
    renderer_gate "$ORIGINS"
    if [ "$MODE" = probe ]; then
      for ms in $PROBE_PERIODS; do
        navigate_all "http://127.0.0.2:$PAGE_PORT/idle-page.html?ms=$ms"
        phase "steady-timer-$ms" "$STEADY" ""
      done
    else
      phase steady-timer "$STEADY" ""
    fi
    navigate_all "http://127.0.0.2:$PAGE_PORT/idle-page.html?timer=0"
    screenshot after-notimer-nav
    phase steady-notimer "$STEADY" ""
  fi
}

# ---- the chat client -----------------------------------------------------------------------------------------

synapse_start() {
  # The .deb installs a systemd unit and systemd would own the process, defeating the pin; the unit is masked
  # and the homeserver is started here under pin_harness (method §2 subject 4).
  sudo apt-get install -y --no-install-recommends lsb-release wget apt-transport-https > "$OUT/apt.synapse-pre.log" 2>&1
  wget -qO /tmp/matrix-org-archive-keyring.gpg https://packages.matrix.org/debian/matrix-org-archive-keyring.gpg
  sudo cp /tmp/matrix-org-archive-keyring.gpg /usr/share/keyrings/
  echo "deb [signed-by=/usr/share/keyrings/matrix-org-archive-keyring.gpg] https://packages.matrix.org/debian/ $(lsb_release -cs) main" \
    | sudo tee /etc/apt/sources.list.d/matrix-org.list > /dev/null
  sudo apt-get update > /dev/null 2>&1
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends matrix-synapse-py3 > "$OUT/apt.synapse.log" 2>&1
  rec apt.synapse.rc "$?"
  rec synapse.version "$(/opt/venvs/matrix-synapse/bin/python -m synapse.app.homeserver --version 2>&1 | head -1)"
  sudo systemctl mask matrix-synapse.service > /dev/null 2>&1
  sudo systemctl stop matrix-synapse.service > /dev/null 2>&1
  mkdir -p "$SYNAPSE_DIR"
  pin_harness /opt/venvs/matrix-synapse/bin/python -m synapse.app.homeserver \
    --server-name meas.local --config-path "$SYNAPSE_DIR/homeserver.yaml" --generate-config \
    --report-stats=no --data-directory "$SYNAPSE_DIR" > "$OUT/synapse.generate.log" 2>&1
  rec synapse.generate.rc "$?"
  {
    echo "registration_shared_secret: \"$MATRIX_SECRET\""
    echo "enable_registration: false"
    echo "listeners:"
    echo "  - port: $SYNAPSE_PORT"
    echo "    tls: false"
    echo "    type: http"
    echo "    x_forwarded: false"
    echo "    bind_addresses: ['127.0.0.1']"
    echo "    resources: [{names: [client], compress: false}]"
  } >> "$SYNAPSE_DIR/homeserver.yaml"
  pin_harness /opt/venvs/matrix-synapse/bin/python -m synapse.app.homeserver \
    --config-path "$SYNAPSE_DIR/homeserver.yaml" > "$OUT/synapse.log" 2>&1 &
  echo $! > "$OUT/synapse.pid"
  local i
  for i in $(seq 1 60); do
    curl -sf "http://127.0.0.1:$SYNAPSE_PORT/health" > /dev/null 2>&1 && break
    sleep 2
  done
  rec synapse.health "$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$SYNAPSE_PORT/health")"
}

element_setup() {
  synapse_start
  [ "$(cat "$OUT/report.kv" | grep -c '^synapse.health=200$')" -ge 1 ] || stop_recorded no-homeserver "Synapse did not answer /health — stopping before any measurement"
  # the account: register_new_matrix_user against the shared secret, so open registration is never left running
  pin_harness /opt/venvs/matrix-synapse/bin/register_new_matrix_user \
    -u "$MATRIX_USER" -p "$MATRIX_PASS" -a -k "$MATRIX_SECRET" "http://127.0.0.1:$SYNAPSE_PORT" \
    > "$OUT/register.log" 2>&1
  rec matrix.register.rc "$?"
  sudo apt-get install -y --no-install-recommends element-desktop > "$OUT/apt.element.log" 2>&1
  rec apt.element.rc "$?"
  rec element.version "$(element-desktop --version 2>&1 | head -1)"
  export ELEMENT_DESKTOP_CONFIG_JSON="$(printf '{"default_server_config":{"m.homeserver":{"base_url":"http://127.0.0.1:%s","server_name":"meas.local"}},"disable_custom_urls":true,"show_labs_settings":false}' "$SYNAPSE_PORT")"
  LAUNCH="element-desktop --no-sandbox --disable-gpu"
  CLASS="element|Element"; PAT="element-desktop|element"; RX="element|Element"
  rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"
  launch_app
  WID=$(wait_window "$CLASS" 180)
  [ -n "$WID" ] || { screenshot no-window; stop_recorded no-window "no Element window after 180 s"; }
  sleep 20; screenshot before-login
  # The sign-in form: the exact field order is a dry-run finding (method §9). Tab order from the focused
  # username field is username, password, submit.
  pin_harness xdotool windowactivate --sync "$WID"
  pin_harness xdotool type --delay 40 "$MATRIX_USER"
  pin_harness xdotool key --clearmodifiers Tab; sleep 0.5
  pin_harness xdotool type --delay 40 "$MATRIX_PASS"
  pin_harness xdotool key --clearmodifiers Return
  sleep 30; screenshot after-login
  # verified from the server's side: a signed-in client holds a /sync long poll, and a signed-out one cannot
  rec matrix.sync_rows "$(grep -c '/_matrix/client/.*/sync' "$OUT/synapse.log" 2>/dev/null || echo 0)"
  [ "$(grep -c '/_matrix/client/.*/sync' "$OUT/synapse.log" 2>/dev/null || echo 0)" -gt 0 ] \
    || stop_recorded not-logged-in "no /sync request reached the homeserver — the client is not signed in, so the idle phase is a login screen (D7)"
  edge launch-settle start; sleep "$LAUNCH_SETTLE"; edge launch-settle end
}

element_traffic_driver() {   # <seconds> — a client-server API script on the harness CPUs, not an Element window
  echo "python3 $HERE/traffic.py --base http://127.0.0.1:$SYNAPSE_PORT --user $MATRIX_USER --password $MATRIX_PASS --per-min $TRAFFIC_PER_MIN --seconds $1 --out $OUT/traffic.jsonl"
}

element_cleanup() {
  kill "$(cat "$OUT/synapse.pid" 2>/dev/null)" 2>/dev/null
}

# ---- the Steam desktop client --------------------------------------------------------------------------------

steam_setup() {
  # this job alone runs a window manager: minimising is a window-manager operation, and the shown-against-
  # minimised comparison is what turns D5's inference into an observation (method §2 subject 5)
  apt_install openbox
  pin_harness openbox > "$OUT/openbox.log" 2>&1 &
  echo $! > "$OUT/openbox.pid"; sleep 3
  rec wm "openbox $(openbox --version 2>&1 | head -1)"
  sudo dpkg --add-architecture i386 > /dev/null 2>&1; sudo apt-get update > /dev/null 2>&1
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y steam-installer > "$OUT/apt.steam.log" 2>&1
  rec apt.steam.rc "$?"
  # no account is used and none may be: Steam Subscriber Agreement §4.C and §1.C (D6). The job signs into
  # nothing, drives no store and performs no account action.
  LAUNCH="steam -silent"
  CLASS="Steam|steam"; PAT="steam"; RX="steam|Steam"
  rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"
  launch_app
  WID=$(wait_window "$CLASS" 300)
  [ -n "$WID" ] || { screenshot no-window; stop_recorded no-window "no Steam window after 300 s — the client may not hold a stable state logged out (D6's fallback)"; }
  rec steam.buildid "$(grep -ho '[0-9]\{6,\}' /tmp/dumps/*.txt 2>/dev/null | head -1)"
  edge launch-settle start; sleep "$LAUNCH_SETTLE"; edge launch-settle end
}

steam_record_helpers() {   # <label> — D5's open question: each helper's --type= role and full command line
  local label="$1"
  for p in $(pgrep -f steamwebhelper 2>/dev/null); do
    printf '%s\t%s\t%s\n' "$label" "$p" "$(tr '\0' ' ' < "/proc/$p/cmdline" 2>/dev/null)" >> "$OUT/steam-helpers.tsv"
  done
  rec "steam.helpers.$label" "$(pgrep -cf steamwebhelper 2>/dev/null || echo 0)"
}

# ---- the job ---------------------------------------------------------------------------------------------------

rec family desktop; rec app "$APP"; rec repeat "$REPEAT"; rec mode "$MODE"; rec started_utc "$(date -u +%FT%TZ)"
rec settings.origins "$ORIGINS"; rec settings.timer_ms "$TIMER_MS"; rec settings.grace_s "$GRACE_S"
rec settings.homeserver "$HOMESERVER"; rec settings.traffic_per_min "$TRAFFIC_PER_MIN"
rec launch_settle_s "${LAUNCH_SETTLE:-unset}"; rec steady_s "${STEADY:-unset}"
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
if [ -z "$LAUNCH_SETTLE" ] || [ -z "$STEADY" ]; then
  rec gate no-phase-lengths; rec finished_utc "$(date -u +%FT%TZ)"; finish_report
  echo "phases: no launch-settle or steady length stated for $APP (method §3) — stopping before any measurement" >&2
  exit 0
fi
rec gate open

sudo apt-get update > /dev/null 2>&1
apt_install xdotool x11-apps dbus-x11 imagemagick
sudo apt-get install -y --no-install-recommends linux-tools-common "linux-tools-$(uname -r)" > "$OUT/apt.perf.log" 2>&1; rec apt.perf.rc "$?"
rec perf.version "$(perf --version 2>&1 | head -1)"
rec kernel "$(uname -r)"
grep -E "CONFIG_(PERF_EVENTS|SCHED_TRACER|TASKSTATS|TASK_DELAY_ACCT|HZ)" "/boot/config-$(uname -r)" > "$OUT/kconfig.txt" 2>/dev/null
rec kernel.hz "$(grep -E '^CONFIG_HZ=' "/boot/config-$(uname -r)" 2>/dev/null | head -1)"
start_xvfb

case "$APP" in
  chrome-hidden|chrome-visible) chrome_subject ;;
  element)
    element_setup
    phase idle "$STEADY" ""
    [ "$MODE" = probe ] || phase traffic "$STEADY" "$(element_traffic_driver "$STEADY")" ;;
  steam)
    steam_setup
    steam_record_helpers shown
    phase shown "$STEADY" ""
    if [ "$MODE" != probe ]; then
      pin_harness xdotool windowminimize "$WID"; sleep 10; screenshot after-minimize
      steam_record_helpers minimised
      phase minimised "$STEADY" ""
    fi ;;
  *) rec error "unknown app $APP" ;;
esac

kill -- "-$APP_PID" 2>/dev/null; sleep 2; kill -9 -- "-$APP_PID" 2>/dev/null
appdef_cleanup
[ "$APP" = element ] && element_cleanup
kill "$(cat "$OUT/openbox.pid" 2>/dev/null)" 2>/dev/null
kill "$(cat "$OUT/xvfb.pid" 2>/dev/null)" 2>/dev/null
rec finished_utc "$(date -u +%FT%TZ)"
sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
finish_report
