#!/usr/bin/env bash
# apps.sh <app> — install, launch under Xvfb, find the window, run an idle
# phase and a driven phase with perf inside each, write $PROBE_OUT/report.json.
# One app per invocation; see the meas-probe workflow matrix.
source "$(dirname "${BASH_SOURCE[0]}")/common.sh"
APP="$1"
rec app "$APP"; rec started_utc "$(date -u +%FT%TZ)"
export DEBIAN_FRONTEND=noninteractive

apt_install() { sudo apt-get install -y --no-install-recommends "$@" > "$OUT/apt.log" 2>&1; rec apt.rc "$?"; }
apt_install_full() { sudo apt-get install -y "$@" > "$OUT/apt.log" 2>&1; rec apt.rc "$?"; }
ver() { rec version "$("$@" 2>&1 | head -1 | tr -d '\n' | head -c 200)"; }

sudo apt-get update > /dev/null 2>&1
apt_install xdotool imagemagick x11-apps python3-xlib dbus-x11
start_xvfb
case "$APP" in
  code)
    wget -qO /tmp/code.deb "https://update.code.visualstudio.com/latest/linux-deb-x64/stable"; rec download.rc "$?"
    apt_install_full /tmp/code.deb; ver code --version
    printf 'hello sample\n' > /tmp/sample.txt
    LAUNCH="code --no-sandbox --disable-gpu --user-data-dir=/tmp/vscode-data --disable-workspace-trust --skip-welcome --skip-release-notes /tmp/sample.txt"
    CLASS="code"; PAT="vscode-data"; RX="code|Code"; DRIVER=type ;;
  soffice)
    apt_install libreoffice-writer libreoffice-gtk3; ver soffice --version
    LAUNCH="soffice --norestore --nologo --nofirststartwizard --writer"
    CLASS="libreoffice|soffice"; PAT="soffice"; RX="soffice"; DRIVER=type ;;
  thunderbird)
    apt_install_full thunderbird; ver thunderbird --version
    mkdir -p "$HOME/tbprofile"
    printf 'user_pref("mail.shell.checkDefaultClient", false);\nuser_pref("mail.provider.enabled", false);\nuser_pref("app.update.enabled", false);\nuser_pref("datareporting.policy.dataSubmissionPolicyBypassNotification", true);\n' > "$HOME/tbprofile/user.js"
    LAUNCH="thunderbird --profile $HOME/tbprofile -compose to=probe@example.invalid,subject=probe,body=probe"
    CLASS="thunderbird|Msgcompose|Mail"; PAT="thunderbird"; RX="thunderbird|Isolated|Web Content"; DRIVER=type ;;
  gimp)
    apt_install gimp; ver gimp --version
    convert -size 800x600 xc:white /tmp/sample.png
    LAUNCH="gimp --no-splash --new-instance /tmp/sample.png"
    CLASS="gimp"; PAT="gimp"; RX="gimp"; DRIVER=pointer ;;
  kdenlive)
    apt_install_full kdenlive; ver kdenlive --version
    export QT_QPA_PLATFORM=xcb KDE_FULL_SESSION=true
    LAUNCH="kdenlive"
    CLASS="kdenlive"; PAT="kdenlive"; RX="kdenlive|melt"; DRIVER=pointer ;;
  chrome)
    ver google-chrome --version
    printf '<html><body><textarea rows=30 cols=100 autofocus></textarea></body></html>' > /tmp/page.html
    LAUNCH="google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data file:///tmp/page.html"
    CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=type ;;
  webrtc)
    ver google-chrome --version
    LAUNCH="google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --allow-file-access-from-files file://$TOOLS/webrtc-loopback.html"
    CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=none ;;
  mpv-video|mpv-audio)
    apt_install mpv ffmpeg; ver mpv --version
    ffmpeg -loglevel error -f lavfi -i testsrc=size=1280x720:rate=30 -f lavfi -i sine=frequency=440:sample_rate=48000 -t 120 -c:v libx264 -preset veryfast -pix_fmt yuv420p -c:a aac /tmp/test.mp4; rec ffmpeg.rc "$?"
    if [ "$APP" = mpv-video ]; then LAUNCH="mpv --no-config --vo=x11 --ao=null --loop=inf /tmp/test.mp4"; CLASS="mpv"; else LAUNCH="mpv --no-config --no-video --ao=null --loop=inf --force-window=yes /tmp/test.mp4"; CLASS="mpv"; fi
    PAT="test.mp4"; RX="mpv|ao|vo|demux|lavc"; DRIVER=none ;;
  *) echo "unknown app $APP"; exit 0 ;;
esac

rec launch "$LAUNCH"
T_LAUNCH=$(now_us)
setsid bash -c "$LAUNCH" > "$OUT/app.log" 2>&1 &
APP_PID=$!
WID=$(wait_window "$CLASS" 90)
sleep 5; screenshot after-launch
snap "$PAT" "" launch; rec launch.n_procs "$(python3 -c "import json;print(json.load(open('$OUT/snap.launch.json'))['n_procs'])")"

if [ -n "$WID" ]; then
  # idle: no input for 20 s
  probe_phase idle "$PAT" "$RX" 20 ""
  case "$DRIVER" in
    type) probe_phase driven "$PAT" "$RX" 35 "$(type_driver "$WID")" ;;
    pointer) probe_phase driven "$PAT" "$RX" 30 "$(pointer_driver "$WID")" ;;
    none) probe_phase driven "$PAT" "$RX" 20 "" ;;
  esac
  screenshot after-driven
  rec window.name_after "$(xdotool getwindowname "$WID" 2>/dev/null | tr -d '\n' | head -c 120)"
  [ -f "$OUT/replay.jsonl" ] && rec replay.sent "$(wc -l < "$OUT/replay.jsonl")"
fi
# never pkill -f: the script's own argv carries the app name (Phase 2 note)
kill -- "-$APP_PID" 2>/dev/null; sleep 2; kill -9 -- "-$APP_PID" 2>/dev/null; kill "$(cat "$OUT/xvfb.pid")" 2>/dev/null
rec finished_utc "$(date -u +%FT%TZ)"
finish_report
