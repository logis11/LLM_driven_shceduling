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
# The visible subject's two steady phases come from a page plan, not from driving the browser: the page holds
# the timer for STEP1 seconds from its load and then none. STEP1 is generous because the run waits on what the
# pages report rather than on this number; it only has to be long enough that the switch cannot fall inside the
# first phase. The probe's period sweep is three probe pushes with TIMER_MS edited between them (D13: the way to
# change a design value is to edit this file and bump the trigger's attempt), not three phases of one job.
STEP_GAP=120                # margin over a phase, absorbing perf post-processing
STEP_WAIT=600               # how long the run waits for every window to report the no-timer step
STEAM_CLIENT_WAIT=900       # the bootstrap downloads the client on first run; the helpers are the signal
HOMESERVER=synapse
TRAFFIC_PER_MIN=60          # instrument setting, not a claim about users (method §2 subject 4)
MATRIX_USER=meas; MATRIX_PASS=meas-9.8-local; MATRIX_SECRET=meas-9-8-registration-secret
SYNAPSE_PORT=8008; SYNAPSE_DIR=/tmp/synapse

# Steady-phase lengths come from the long-phase probe and are written into method §10 before the first batch
# (method §3, 9.5 D35). A subject without one stops before measuring, as campaign/run.sh's settle_for() does.
launch_settle_for() { case "$1" in *) echo "" ;; esac; }
steady_for()        { case "$1" in *) echo "" ;; esac; }

if [ "$MODE" = dry ]; then
  LAUNCH_SETTLE=20; STEADY=45; GRACE_S=75; ORIGINS=3; STEP_GAP=40; STEP_WAIT=180; STEAM_CLIENT_WAIT=900
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
  # every renderer's whole command line, which the snapshot truncates at 120 characters. The dry run of
  # 2026-09-20 saw four renderers ticking at the timer rate against three windows and three origins, and a
  # renderer's command line does not name the site it is locked to — these are the flags that might.
  for r in $(pgrep -f -- "--type=renderer" 2>/dev/null); do
    printf '%s\t%s\n' "$r" "$(tr '\0' ' ' < "/proc/$r/cmdline" 2>/dev/null)" >> "$OUT/renderers.tsv"
  done
  [ "$n" -ge "$want" ] || stop_recorded wrong-renderer-count "renderer gate: wanted at least $want renderers, observed $n — stopping before the steady phase"
}

# window_steps — one line per browser window: the step its page reports in its title. xdotool getwindowname
# reads a window without focusing it, which is what makes this work where typing did not.
window_steps() {
  local w
  for w in $(pin_harness xdotool search --onlyvisible --class "$CLASS" 2>/dev/null); do
    pin_harness xdotool getwindowname "$w" 2>/dev/null | grep -oE 'idle-page .*' || true
  done
}

# wait_for_step <label> <seconds> — block until every window's page reports <label> ("timer <n> ms" or "no
# timer"), then record what was seen. The page walks its own schedule from its load (idle-page.html), so the run
# SYNCHRONISES on what the pages report rather than assuming the phase boundary landed where it was planned —
# the gap between phases is dominated by perf post-processing, whose length is not knowable in advance.
wait_for_step() {
  local want="$1" secs="$2" i n_all n_want
  for i in $(seq 1 "$secs"); do
    n_all="$(window_steps | wc -l | tr -d ' ')"
    n_want="$(window_steps | grep -cF "$want" || true)"
    [ "$n_all" -gt 0 ] && [ "$n_all" = "$n_want" ] && break
    sleep 1
  done
  rec "step.$want.windows" "$n_all"; rec "step.$want.reporting" "$n_want"
  window_steps > "$OUT/steps.$want.txt"
  [ "$n_all" = "$n_want" ]
}

chrome_subject() {
  export MEAS_ORIGINS="$ORIGINS" MEAS_TIMER_MS="$TIMER_MS" MEAS_PAGE_PORT="$PAGE_PORT"
  if [ "$APP" = chrome-visible ]; then
    export MEAS_PAGE_PLAN="$TIMER_MS:$((LAUNCH_SETTLE + STEADY + STEP_GAP)),0:$((STEADY + STEP_GAP + STEP_WAIT))"
    rec page.plan "$MEAS_PAGE_PLAN"
  fi
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
    # every window must still be on the timer step, or the phase is not the phase it claims
    wait_for_step "timer $TIMER_MS ms" 30 || rec step.timer.incomplete 1
    phase steady-timer "$STEADY" ""
    # the pages switch themselves off on their own schedule; the run waits for every window to report it
    wait_for_step "no timer" "$STEP_WAIT" || stop_recorded timer-not-stopped \
      "not every window reported the no-timer step within ${STEP_WAIT}s — the second phase would carry timers the first already had"
    screenshot after-notimer
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
  rec synapse.version "$(dpkg-query -W -f='${Version}' matrix-synapse-py3 2>/dev/null)"
  sudo systemctl mask matrix-synapse.service > /dev/null 2>&1
  sudo systemctl stop matrix-synapse.service > /dev/null 2>&1
  mkdir -p "$SYNAPSE_DIR"
  pin_harness /opt/venvs/matrix-synapse/bin/python -m synapse.app.homeserver \
    --server-name meas.local --config-path "$SYNAPSE_DIR/homeserver.yaml" --generate-config \
    --report-stats=no --data-directory "$SYNAPSE_DIR" > "$OUT/synapse.generate.log" 2>&1
  rec synapse.generate.rc "$?"
  # the generated config already listens on 8008 for the client API and carries a random
  # registration_shared_secret; it is read back rather than overridden, so there is no second `listeners:` key
  MATRIX_SECRET="$(sed -n 's/^registration_shared_secret: *"\{0,1\}\([^"]*\)"\{0,1\} *$/\1/p' "$SYNAPSE_DIR/homeserver.yaml" | head -1)"
  rec synapse.secret_read "$([ -n "$MATRIX_SECRET" ] && echo yes || echo no)"
  # longhand taskset, not pin_harness: a function backgrounded forks a subshell, so $! would be the subshell and
  # element_cleanup would kill that instead of the homeserver
  if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then
    taskset -c "$MEAS_HARNESS_CPUS" setsid /opt/venvs/matrix-synapse/bin/python -m synapse.app.homeserver \
      --config-path "$SYNAPSE_DIR/homeserver.yaml" > "$OUT/synapse.log" 2>&1 &
  else
    setsid /opt/venvs/matrix-synapse/bin/python -m synapse.app.homeserver \
      --config-path "$SYNAPSE_DIR/homeserver.yaml" > "$OUT/synapse.log" 2>&1 &
  fi
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
  grep -q '^synapse.health=200$' "$KV" || stop_recorded no-homeserver "Synapse did not answer /health — stopping before any measurement"
  # the account: register_new_matrix_user against the shared secret, so open registration is never left running
  # -c, not -k: register_new_matrix_user reads the shared secret from the config itself, so the secret never
  # makes a round trip through the shell. The dry run of 2026-09-20 failed here with "-k/--shared-secret:
  # expected one argument" although the read-back had reported a value.
  pin_harness /opt/venvs/matrix-synapse/bin/register_new_matrix_user \
    -u "$MATRIX_USER" -p "$MATRIX_PASS" -a --exists-ok -c "$SYNAPSE_DIR/homeserver.yaml" \
    "http://127.0.0.1:$SYNAPSE_PORT" > "$OUT/register.log" 2>&1
  rec matrix.register.rc "$?"
  wget -qO /tmp/element-io-archive-keyring.gpg https://packages.element.io/debian/element-io-archive-keyring.gpg
  sudo cp /tmp/element-io-archive-keyring.gpg /usr/share/keyrings/
  echo "deb [signed-by=/usr/share/keyrings/element-io-archive-keyring.gpg] https://packages.element.io/debian/ default main" \
    | sudo tee /etc/apt/sources.list.d/element-io.list > /dev/null
  sudo apt-get update > /dev/null 2>&1
  sudo apt-get install -y --no-install-recommends element-desktop > "$OUT/apt.element.log" 2>&1
  rec apt.element.rc "$?"
  # under `timeout`, and from the package first: an Electron binary given --version may start its GUI instead of
  # printing and exiting, and the dry runs of 2026-09-20 hung here twice — the last key recorded was
  # apt.element.rc, and the next statement is this one.
  rec element.version "$(dpkg-query -W -f='${Version}' element-desktop 2>/dev/null || timeout 20 element-desktop --version 2>&1 | head -1)"
  export ELEMENT_DESKTOP_CONFIG_JSON="$(printf '{"default_server_config":{"m.homeserver":{"base_url":"http://127.0.0.1:%s","server_name":"meas.local"}},"disable_custom_urls":true,"show_labs_settings":false}' "$SYNAPSE_PORT")"
  # --disable-gpu alone is what meas-gui.yml used, but Element 1.12.28 died with "GPU process launch failed:
  # error_code=1002 … GPU process isn't usable. Goodbye." and showed its "System unsupported" page: Electron
  # treats an unusable GPU process as fatal where Chrome tolerates it. The GPU sandbox is disabled with the
  # rest, and /dev/shm is not used, which is the shape a hosted runner needs.
  # --password-store=basic: a hosted runner has no gnome-keyring or kwallet, and Electron's safeStorage then
  # puts up "Your system has an unsupported keyring meaning the database cannot be opened" — a modal the dry run
  # of 2026-09-20 found sitting where the login form should have been, titled "System unsupported". The dialog
  # names this argument as the fix. The client therefore stores its session with Electron's basic backend, which
  # the entry's scope states.
  LAUNCH="element-desktop --no-sandbox --disable-gpu --disable-gpu-sandbox --disable-software-rasterizer --disable-dev-shm-usage --password-store=basic"
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
  if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_HARNESS_CPUS" setsid openbox > "$OUT/openbox.log" 2>&1 &
  else setsid openbox > "$OUT/openbox.log" 2>&1 & fi
  echo $! > "$OUT/openbox.pid"; sleep 3
  rec wm "openbox $(openbox --version 2>&1 | head -1)"
  sudo dpkg --add-architecture i386 > /dev/null 2>&1; sudo apt-get update > /dev/null 2>&1
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y steam-installer > "$OUT/apt.steam.log" 2>&1
  rec apt.steam.rc "$?"
  # no account is used and none may be: Steam Subscriber Agreement §4.C and §1.C (D6). The job signs into
  # nothing, drives no store and performs no account action.
  LAUNCH="steam"
  CLASS="Steam|steam"; PAT="steam"; RX="steam|Steam"
  rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"
  launch_app
  # `steam-installer` is a bootstrap: the first `steam` opens a window named "Steam installer" which downloads
  # the real client. The dry run of 2026-09-20 measured that dialog — `steam.helpers` 0 in both phases and no
  # row matching the process regex — so the window alone is not the signal. The client is up when its CEF
  # helpers exist, which is also what D5's open question is about, so that is what the run waits for.
  WID=$(wait_window "$CLASS" 300)
  [ -n "$WID" ] || { screenshot no-window; stop_recorded no-window "no Steam window after 300 s — the client may not hold a stable state logged out (D6's fallback)"; }
  rec steam.first_window "$(pin_harness xdotool getwindowname "$WID" 2>/dev/null)"
  # `steam-installer` ships a bootstrap, and its first run puts up a zenity consent dialog — "Steam is
  # proprietary (binary-only) software … Steam will be installed into ~/.steam/debian-installation", Cancel or
  # Install — and waits. The dry run of 2026-09-20 sat on it for 900 s. This accepts the package's own
  # installation prompt, which is what D6 already decided when it said the probe installs and launches the
  # client; it is not an account action, and none is taken anywhere.
  if pin_harness xdotool getwindowname "$WID" 2>/dev/null | grep -qi "steam installer"; then
    rec steam.installer_dialog 1
    pin_harness xdotool windowactivate --sync "$WID" 2>/dev/null
    # The Install button is clicked by position, never by Return: the dry run of 2026-09-20 pressed Return and
    # the log read "steam: Installation cancelled" — zenity's default button here is Cancel, on the left, with
    # Install on the right of the bottom row.
    eval "$(pin_harness xdotool getwindowgeometry --shell "$WID" 2>/dev/null)"
    for dy in 26 40 14; do
      pin_harness xdotool getwindowname "$WID" 2>/dev/null | grep -qi "steam installer" || break
      pin_harness xdotool mousemove $((X + WIDTH * 3 / 4)) $((Y + HEIGHT - dy)) click 1
      rec "steam.installer_click_dy" "$dy"
      sleep 5
    done
    rec steam.installer_dismissed "$(pin_harness xdotool getwindowname "$WID" 2>/dev/null | grep -qi "steam installer" && echo no || echo yes)"
    screenshot after-installer-consent
  fi
  for i in $(seq 1 "$STEAM_CLIENT_WAIT"); do
    [ "$(pgrep -cf steamwebhelper 2>/dev/null | head -1)" -gt 0 ] && break
    sleep 1
  done
  rec steam.helpers.at_launch "$(pgrep -cf steamwebhelper 2>/dev/null | head -1)"
  [ "$(pgrep -cf steamwebhelper 2>/dev/null | head -1)" -gt 0 ] || {
    screenshot no-client
    stop_recorded no-steam-client "the bootstrap did not reach a running client within ${STEAM_CLIENT_WAIT}s — no steamwebhelper (D6's fallback: the binding retires to 9.10 instead of being measured)"
  }
  # the client's own window, once the bootstrap's dialog has gone
  W2=$(wait_window "$CLASS" 120); [ -n "$W2" ] && WID="$W2"
  rec steam.client_window "$(pin_harness xdotool getwindowname "$WID" 2>/dev/null)"
  screenshot after-client
  # the client's own build id is a dry-run finding (method §9); what is recorded here is the package the runner
  # installed, which is observable now
  rec steam.package "$(dpkg-query -W -f='${Package} ${Version}' steam-installer 2>/dev/null)"
  edge launch-settle start; sleep "$LAUNCH_SETTLE"; edge launch-settle end
}

steam_record_helpers() {   # <label> — D5's open question: each helper's --type= role and full command line
  local label="$1"
  for p in $(pgrep -f steamwebhelper 2>/dev/null); do
    printf '%s\t%s\t%s\n' "$label" "$p" "$(tr '\0' ' ' < "/proc/$p/cmdline" 2>/dev/null)" >> "$OUT/steam-helpers.tsv"
  done
  # pgrep -c prints its count and exits 1 when there are none, so `|| echo 0` printed a second line and `rec`
  # wrote a bare `0` into report.kv
  rec "steam.helpers.$label" "$(pgrep -cf steamwebhelper 2>/dev/null | head -1)"
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
