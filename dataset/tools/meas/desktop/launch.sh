#!/usr/bin/env bash
# launch.sh — the launch subjects of the desktop family (9.10 changelog D132–D135; method
# _dev/research/jioh/task-9.10-scenarios-timelines/campaign/launch/method.md). Sourced by run.sh, whose functions it
# uses: rec, snap, screenshot, wait_window, launch_app, stop_recorded, click_right_button, element_setup, steam_setup.
#
# A subject `launch-<arm>` is an entry's own campaign's launch (D133): 9.5's arms `soffice`, `thunderbird-send`,
# `kdenlive`, `mpv-video`, `mpv-audio` and `chrome` as campaign/run.sh launches them, 9.8's `chrome-hidden`, `element`
# and `steam` as run.sh does, and `webrtc`, the call opened in a running Chrome (D134). Each job runs the sequence
# twice (D135): the first launch through its settle, unmeasured, quit by the program's own command; the warm check
# (D132); then the same sequence traced under perf from 2 s before the exec to the settle's end. The campaign's lengths
# hold in every mode: a dry run checks the tooling at them (D135).

LN_ORIGINS=12            # 9.8's hidden-tab N (run.sh ORIGINS); a dry run does not shorten it here
LN_GRACE=630             # 9.8 D15's grace
LN_QUIT_WAIT=60          # D135: the tree exits within this of its quit, or the job stops
LN_BROWSER_SETTLE=420    # D134: web-browser's settle, before the call opens
LN_ELEMENT_SETTLE=50     # D135: 9.8's 30 s after the sign-in and its 20 s launch-settle

# the settle after the window and the post-launch steps (D133: campaign/run.sh's settle_for, run.sh's launch_settle_for)
ln_settle_for() {
  case "$1" in
    soffice|mpv-video|mpv-audio) echo 30 ;;
    kdenlive) echo 240 ;;       # 9.10 D146: campaign/run.sh's new settle_for, past its work after launch
    thunderbird-send) echo 390 ;;
    chrome) echo 420 ;;
    chrome-hidden) echo 20 ;;   # then the grace
    webrtc) echo 210 ;;         # from the call's opening
    element) echo "$LN_ELEMENT_SETTLE" ;;
    steam) echo 900 ;;
    *) echo "" ;;
  esac
}
# D135: the program's own quit, sent to its main window; the dry runs (#77, #78) took the window's own close (the title
# bar's, close_window.py) where the shortcut did nothing under Xvfb with no window manager: Kdenlive, Chrome
ln_quit_for() {
  case "$1" in
    soffice|thunderbird-send|element) echo "ctrl+q" ;;
    kdenlive|chrome|chrome-hidden|webrtc) echo "close-window" ;;
    mpv-video|mpv-audio) echo "q" ;;
    steam) echo "close-window" ;;   # dry run #77: the logged-out client's sign-in window; `steam -shutdown` after 30 s
  esac
}
# what a window the quit puts up is given: a "save changes?" dialog's discard key, or Element's confirmation "Are you
# sure you want to quit?", whose right-hand button is "Close Element" (dry run #77)
ln_discard_for() {
  case "$1" in
    soffice) echo "alt+n" ;;    # LibreOffice's "Don't Save" (9.5's soffice prelude)
    kdenlive) echo "alt+d" ;;   # KDE's "Discard"
    element) echo "right-button" ;;
    *) echo "" ;;
  esac
}

# perf's clock: CLOCK_MONOTONIC, as `perf sched record -k CLOCK_MONOTONIC` stamps its rows
ledge() { python3 -c 'import time,json,sys; print(json.dumps({"phase": sys.argv[1], "edge": sys.argv[2], "mono_ns": time.monotonic_ns(), "real_ns": time.time_ns()}))' "$1" "$2" >> "$OUT/launch-edges.jsonl"; }

ln_trace_start() {
  sudo taskset -c "$MEAS_HARNESS_CPUS" perf sched record -k CLOCK_MONOTONIC -a -e sched:sched_process_exec -o "$OUT/perf.launch.data" > "$OUT/perf.launch.log" 2>&1 &
  LN_PERF=$!
  sleep 2
}

# the trace stopped at the settle's end, then the rows the analysis reads (the background family's phase())
ln_trace_stop() {
  sudo kill -INT "$LN_PERF" 2>/dev/null; wait "$LN_PERF" 2>/dev/null; rec perf.launch.record.rc "$?"
  sudo perf sched timehist --state -i "$OUT/perf.launch.data" 2>> "$OUT/perf.launch.log" | gzip > "$OUT/perf.launch.timehist.txt.gz"
  rec perf.launch.timehist.rc "${PIPESTATUS[0]}"
  rec perf.launch.timehist.rows "$(gzip -dc "$OUT/perf.launch.timehist.txt.gz" | wc -l)"
  sudo perf sched timehist -w -i "$OUT/perf.launch.data" 2>> "$OUT/perf.launch.log" | grep -E "awakened|wakeup|\bwaker\b" | gzip > "$OUT/perf.launch.wakeups.txt.gz"
  rec perf.launch.wakeups.rows "$(gzip -dc "$OUT/perf.launch.wakeups.txt.gz" | wc -l)"
  sudo perf script -i "$OUT/perf.launch.data" -F time,event,trace 2>> "$OUT/perf.launch.log" \
    | grep -E "sched_process_fork|sched_wakeup_new|sched_process_exit|sched_process_exec" | gzip > "$OUT/perf.launch.forks.txt.gz"
  rec perf.launch.forks.rows "$(gzip -dc "$OUT/perf.launch.forks.txt.gz" | wc -l)"
  rec perf.launch.data_bytes "$(stat -c %s "$OUT/perf.launch.data" 2>/dev/null || echo 0)"
  rec perf.launch.lost "$(grep -ioE 'lost [0-9]+ (chunks|events|samples)' "$OUT/perf.launch.log" | tr '\n' ' ')"
  sudo chown -R "$(id -u):$(id -g)" "$OUT" 2>/dev/null
  if [ "$MODE" = dry ]; then gzip -f "$OUT/perf.launch.data"; else rm -f "$OUT/perf.launch.data"; fi
}

# ln_tree <label>: the launched tree at the settle's end, its roles' source, and the harness check (run.sh's check_tree,
# read from the tree itself: these subjects' process patterns match run.sh's own command line, `launch-soffice`)
ln_tree() {
  local n
  n="$(python3 "$HERE/launch.py" tree --root "$APP_PID" --json "$OUT/launch.tree.$1.json" --check 2>> "$OUT/tree.$1.txt")"
  rec "launch.$1.tree_procs" "$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$OUT/launch.tree.$1.json" 2>/dev/null)"
  rec "tree.$1.harness_procs" "$n"
  [ "$n" = 0 ] || stop_recorded harness-in-tree "the launched tree contains $n harness process(es) — see tree.$1.txt"
}

ln_renderers() {   # <label>: every renderer's whole command line (D127's roles), as run.sh's renderer gate records them
  local r
  : > "$OUT/launch.renderers.$1.tsv"
  for r in $(pgrep -f -- "--type=renderer" 2>/dev/null); do
    printf '%s\t%s\n' "$r" "$(tr '\0' ' ' < "/proc/$r/cmdline" 2>/dev/null)" >> "$OUT/launch.renderers.$1.tsv"
  done
  rec "launch.$1.page_renderers" "$(grep -c -- '--type=renderer' "$OUT/launch.renderers.$1.tsv" | head -1)"
}

ln_window() {   # <label> <seconds>: the window, its time from the exec
  local t0; t0=$(now_us)
  WID=$(wait_window "$CLASS" "$2")
  rec "launch.$1.window_ms" "$(( ($(now_us) - t0) / 1000 ))"
  [ -n "$WID" ] || { screenshot "no-window-$1"; stop_recorded no-window "no window after $2 s ($1 launch)"; }
  ledge "$1.window" mark
}

# the 9.5 arms' steps after the window, as campaign/run.sh runs them
ln_steps_95() {
  local W2
  [ -n "$POSTLAUNCH" ] || return 0
  xdotool windowactivate --sync "$WID" 2>/dev/null; bash -c "$POSTLAUNCH" > "$OUT/postlaunch.$1.log" 2>&1
  if [ -n "$POSTCLASS" ]; then
    W2=$(wait_window "$POSTCLASS" 30); rec "launch.$1.postwindow" "$W2"; [ -n "$W2" ] && WID="$W2"
  fi
  screenshot "after-postlaunch-$1"
}

# ln_once <first|traced>: one launch of a 9.5 arm or of chrome-hidden, from the exec through the settle
ln_once() {
  local L="$1" n
  [ "$L" = traced ] && ln_trace_start
  ledge "$L.exec" mark
  launch_app; rec "launch.$L.root" "$APP_PID"
  ln_window "$L" 120
  ln_steps_95 "$L"
  ledge "$L.settle" start
  if [ "$SUBJ" = chrome-hidden ]; then
    sleep "$LN_SETTLE"
    # the tabs' renderers are those at the gate: a plain renderer can start later in the grace (dry run #80, client
    # id 21 against the tabs' 6–18), and it hosts no tab
    ln_renderers "$L.gate"
    n="$(grep -c -- '--type=renderer' "$OUT/launch.renderers.$L.gate.tsv" | head -1)"
    # run.sh's renderer gate: at least N + 1 renderers, the control tab's and the N measured ones
    [ "$n" -ge $((LN_ORIGINS + 1)) ] || stop_recorded wrong-renderer-count "wanted at least $((LN_ORIGINS + 1)) renderers, observed $n ($L launch)"
    ledge "$L.backgrounded" mark
    sleep "$LN_GRACE"
  else
    sleep "$LN_SETTLE"
  fi
  ledge "$L.settle" end
  screenshot "after-settle-$L"
  [ "$SUBJ" = chrome-hidden ] && ln_renderers "$L"
  ln_tree "$L"
  [ "$L" = traced ] && ln_trace_stop
  return 0
}

# ln_call <first|traced>: D134 — Chrome on web-browser's page through web-browser's settle, then the call page opened
ln_call() {
  local L="$1" title
  ledge "$L.exec" mark
  launch_app; rec "launch.$L.root" "$APP_PID"
  ln_window "$L" 120
  sleep "$LN_BROWSER_SETTLE"
  ledge "$L.browser-settle" end
  if [ "$L" = traced ]; then
    ln_trace_start
    rec launch.seed.threads "$(python3 "$HERE/launch.py" seed --pattern chrome-data --out "$OUT/launch.seed.tsv")"
  fi
  ledge "$L.call" open
  # hands the address to the running browser over its user-data directory's singleton and exits
  google-chrome --no-sandbox --user-data-dir=/tmp/chrome-data "file://$TOOLS/webrtc-loopback.html" > "$OUT/call-open.$L.log" 2>&1
  rec "launch.$L.call_open.rc" "$?"
  ledge "$L.settle" start
  sleep "$LN_SETTLE"
  ledge "$L.settle" end
  title="$(xdotool search --name 'webrtc-loopback' getwindowname 2>/dev/null | head -1)"
  rec "launch.$L.call_title" "$title"
  # the call connected: the page's title reports encoded and decoded frames
  rec "launch.$L.call_connected" "$(echo "$title" | grep -qE 'enc=[1-9][0-9]* dec=[1-9]' && echo 1 || echo 0)"
  screenshot "after-settle-$L"
  ln_tree "$L"
  [ "$L" = traced ] && ln_trace_stop
  return 0
}

ln_element_traced() {
  local n0 i n
  ln_trace_start
  n0="$(grep -c '/_matrix/client/.*/sync' "$SYNAPSE_LOG" 2>/dev/null)"
  ledge traced.exec mark
  launch_app; rec launch.traced.root "$APP_PID"
  ln_window traced 180
  # the restored session's first /sync (D135); the keyring modal, if the relaunch shows it again, given 9.8's answer
  for i in $(seq 1 120); do
    if xdotool getwindowname "$WID" 2>/dev/null | grep -qi "system unsupported"; then
      rec launch.traced.keyring_modal 1
      click_right_button "$WID" launch.traced.keyring
      W2=$(wait_window "$CLASS" 60); [ -n "$W2" ] && WID="$W2"
    fi
    n="$(grep -c '/_matrix/client/.*/sync' "$SYNAPSE_LOG" 2>/dev/null)"
    [ "${n:-0}" -gt "${n0:-0}" ] && break
    sleep 1
  done
  rec launch.traced.sync_wait_s "$i"
  [ "${n:-0}" -gt "${n0:-0}" ] || stop_recorded not-logged-in "the relaunched client sent no /sync within 120 s of its window"
  ledge traced.signed-in mark
  ledge traced.settle start; sleep "$LN_SETTLE"; ledge traced.settle end
  screenshot after-settle-traced
  ln_tree traced
  ln_trace_stop
}

ln_steam_traced() {
  local i
  ln_trace_start
  ledge traced.exec mark
  launch_app; rec launch.traced.root "$APP_PID"
  # the client is up when its web helpers run (9.8's signal: the window alone was the bootstrap's)
  for i in $(seq 1 "$STEAM_CLIENT_WAIT"); do
    [ "$(pgrep -cf steamwebhelper 2>/dev/null | head -1)" -gt 0 ] && break
    sleep 1
  done
  rec launch.traced.helpers_wait_s "$i"
  [ "$(pgrep -cf steamwebhelper 2>/dev/null | head -1)" -gt 0 ] || stop_recorded no-steam-client "no steamwebhelper within ${STEAM_CLIENT_WAIT}s of the relaunch"
  ledge traced.window mark
  W2=$(wait_window "$CLASS" 120); [ -n "$W2" ] && WID="$W2"
  rec launch.traced.steamid "$(tr '\0' ' ' < /proc/$(pgrep -f steamwebhelper | head -1)/cmdline 2>/dev/null | grep -o 'steamid=[0-9]*' | head -1 | cut -d= -f2)"
  ledge traced.settle start; sleep "$LN_SETTLE"; ledge traced.settle end
  screenshot after-settle-traced
  ln_tree traced
  ln_trace_stop
}

ln_main_window() {   # the largest visible window of the application's class (kdenlive_export.py's find_window)
  local w best="$WID" area=0 a
  for w in $(xdotool search --onlyvisible --class "$CLASS" 2>/dev/null); do
    eval "$(xdotool getwindowgeometry --shell "$w" 2>/dev/null)"
    a=$(( ${WIDTH:-0} * ${HEIGHT:-0} ))
    [ "$a" -gt "$area" ] && { area="$a"; best="$w"; }
  done
  echo "$best"
}

ln_visible() { { xdotool search --onlyvisible --class '' 2>/dev/null; xdotool search --onlyvisible --name '' 2>/dev/null; } | sort -u; }

# ln_quit: D135 — the files the tree maps, the program's own quit, the tree's exit within LN_QUIT_WAIT, the warm check
ln_quit() {
  local quit discard i left dlg before
  rec launch.first.mapped_files "$(python3 "$HERE/launch.py" maps --root "$APP_PID" --out "$OUT/launch.mapped.txt")"
  quit="$(ln_quit_for "$SUBJ")"; discard="$(ln_discard_for "$SUBJ")"
  rec launch.quit "$quit"
  # the quit goes to the application's largest visible window, as the export's driver finds Kdenlive's main window: a
  # search by class can return a secondary top-level first (dry run #78 closed Kdenlive's window titled "Kdenlive")
  WID="$(ln_main_window)"
  rec launch.quit_window "$(xdotool getwindowname "$WID" 2>/dev/null | head -c 120)"
  before="$(ln_visible)"
  ledge first.quit mark
  if [ "$quit" = close-window ]; then rec launch.close_window "$(python3 "$HERE/close_window.py" "$WID" 2>&1 | tail -1)"
  else xdotool windowfocus --sync "$WID" 2>/dev/null; xdotool key --clearmodifiers "$quit"; fi
  local qwait="$LN_QUIT_WAIT"; [ "$SUBJ" = steam ] && qwait=120
  for i in $(seq 1 "$qwait"); do
    left="$(python3 "$HERE/launch.py" tree --root "$APP_PID" --app-only)"
    [ -z "$left" ] && break
    if [ "$SUBJ" = steam ] && [ "$i" = 30 ]; then   # the client's own command, if its window's close left it running
      rec launch.quit_second "steam -shutdown"; timeout 60 steam -shutdown > "$OUT/quit.log" 2>&1 &
    fi
    if [ "$i" = 4 ]; then   # a window the quit put up: recorded, and given the program's answer where it has one
      xdotool search --onlyvisible --name '.' getwindowname %@ > "$OUT/quit-windows.txt" 2>/dev/null
      dlg="$(comm -13 <(echo "$before") <(ln_visible) | head -1)"
      if [ -n "$dlg" ]; then
        rec launch.quit_dialog "$(xdotool getwindowname "$dlg" 2>/dev/null | head -c 120)|$(xdotool getwindowgeometry "$dlg" 2>/dev/null | tr '\n' ' ')"
        screenshot quit-dialog
        if [ "$discard" = right-button ]; then click_right_button "$dlg" launch.quit_dialog
        elif [ -n "$discard" ]; then xdotool windowfocus --sync "$dlg" 2>/dev/null; xdotool key --clearmodifiers "$discard"; fi
      fi
    fi
    sleep 1
  done
  rec launch.first.quit_s "$i"
  rec launch.first.left_after_quit "$(python3 "$HERE/launch.py" tree --root "$APP_PID" | wc -w | tr -d ' ')"
  [ -z "$left" ] || { screenshot unclean-quit; stop_recorded unclean-quit "the tree did not exit within ${qwait}s of its quit ($quit): $left"; }
  ledge first.exited mark
  python3 "$HERE/launch.py" warm "$OUT/launch.mapped.txt" --tsv "$OUT/launch.cache.tsv" >> "$KV"
  sleep 5
}

launch_subject() {
  SUBJ="$1"
  LN_SETTLE="$(ln_settle_for "$SUBJ")"
  rec launch.subject "$SUBJ"; rec launch.settle_s "$LN_SETTLE"; rec launch.quit_wait_s "$LN_QUIT_WAIT"
  [ -n "$LN_SETTLE" ] || stop_recorded unknown-subject "no launch subject $SUBJ (D133)"
  # fincore for the warm check (the image lacks it; the background family's run #126), python3-xlib for close_window.py
  sudo apt-get install -y --no-install-recommends util-linux-extra python3-xlib > "$OUT/apt.launch.log" 2>&1; rec apt.launch.rc "$?"
  rec util-linux.version "$(fincore --version 2>&1 | head -1)"
  case "$SUBJ" in
    element)
      LAUNCH_SETTLE=20                        # 9.8's sequence through its launch-settle: the first launch
      element_setup
      ledge first.settle end
      ln_tree first
      ln_quit
      ln_element_traced ;;
    steam)
      LAUNCH_SETTLE=900; STEAM_CLIENT_WAIT=900
      steam_setup
      ledge first.settle end
      ln_tree first
      ln_quit
      ln_steam_traced ;;
    webrtc)
      appdef chrome || exit 0                 # web-browser's page, /tmp/page.html (D134)
      appdef webrtc || exit 0
      LAUNCH="${LAUNCH% file://*} file:///tmp/page.html"
      rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"; rec launch.call_page "file://$TOOLS/webrtc-loopback.html"
      ln_call first
      ln_quit
      ln_call traced ;;
    chrome-hidden)
      export MEAS_ORIGINS="$LN_ORIGINS" MEAS_TIMER_MS="$TIMER_MS" MEAS_PAGE_PORT="$PAGE_PORT"
      appdef chrome-hidden || exit 0
      rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"; rec launch.origins "$LN_ORIGINS"; rec launch.grace_s "$LN_GRACE"
      ln_once first
      ln_quit
      ln_once traced ;;
    *)
      appdef "$SUBJ" || exit 0
      build_gate || exit 0
      rec launch "$LAUNCH"; rec rx "$RX"; rec pat "$PAT"; rec postclass "${POSTCLASS:-}"
      ln_once first
      ln_quit
      ln_once traced ;;
  esac
  python3 "$HERE/launch.py" analyze "$OUT" >> "$KV"
}
