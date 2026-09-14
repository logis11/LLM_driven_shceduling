#!/usr/bin/env bash
# appdefs.sh — install and launch definitions per application, shared by the
# probe (apps.sh) and the campaign (campaign/run.sh). `appdef <app>` installs
# the application and sets LAUNCH, CLASS (window class/name regex), PAT
# (process-tree pattern for snapshot.py), RX (comm regex for perf rows),
# DRIVER (type | pointer | stream | none) and STREAM (word | outlook | ie).
# Requires common.sh sourced and Xvfb running (version checks need a display).

appdef() {
  local app="$1"
  export DEBIAN_FRONTEND=noninteractive
  STREAM=""
  case "$app" in
    code)
      wget -qO /tmp/code.deb "https://update.code.visualstudio.com/latest/linux-deb-x64/stable"; rec download.rc "$?"
      apt_install_full /tmp/code.deb; ver code --version
      printf 'hello sample\n' > /tmp/sample.txt
      LAUNCH="code --no-sandbox --disable-gpu --user-data-dir=/tmp/vscode-data --disable-workspace-trust --skip-welcome --skip-release-notes /tmp/sample.txt"
      CLASS="code"; PAT="vscode-data"; RX="code|Code"; DRIVER=stream; STREAM=word ;;
    soffice)
      apt_install libreoffice-writer libreoffice-gtk3; ver soffice --version
      LAUNCH="soffice --norestore --nologo --nofirststartwizard --writer"
      CLASS="libreoffice|soffice"; PAT="soffice"; RX="soffice"; DRIVER=stream; STREAM=word ;;
    thunderbird)
      apt_install_full thunderbird; ver thunderbird --version
      mkdir -p "$HOME/tbprofile"
      cat > "$HOME/tbprofile/user.js" <<'PREFS'
user_pref("mail.shell.checkDefaultClient", false);
user_pref("mail.provider.enabled", false);
user_pref("app.update.enabled", false);
user_pref("datareporting.policy.dataSubmissionPolicyBypassNotification", true);
user_pref("mailnews.start_page.enabled", false);
user_pref("mail.accountmanager.accounts", "account1");
user_pref("mail.accountmanager.defaultaccount", "account1");
user_pref("mail.account.account1.server", "server1");
user_pref("mail.account.account1.identities", "id1");
user_pref("mail.server.server1.type", "none");
user_pref("mail.server.server1.hostname", "Local Folders");
user_pref("mail.server.server1.name", "Local Folders");
user_pref("mail.server.server1.userName", "nobody");
user_pref("mail.server.server1.directory-rel", "[ProfD]Mail/Local Folders");
user_pref("mail.identity.id1.useremail", "measure@example.invalid");
user_pref("mail.identity.id1.fullName", "Measure");
user_pref("mail.identity.id1.valid", true);
user_pref("mail.identity.id1.smtpServer", "smtp1");
user_pref("mail.smtpservers", "smtp1");
user_pref("mail.smtp.defaultserver", "smtp1");
user_pref("mail.smtpserver.smtp1.hostname", "smtp.example.invalid");
user_pref("mail.smtpserver.smtp1.username", "measure");
PREFS
      LAUNCH="thunderbird --profile $HOME/tbprofile -compose to=someone@example.invalid,subject=measure,body=measure"
      CLASS="Msgcompose|thunderbird"; PAT="thunderbird"; RX="thunderbird|Isolated|Web Content"; DRIVER=stream; STREAM=outlook ;;
    gimp)
      apt_install gimp; ver gimp --version
      convert -size 800x600 xc:white /tmp/sample.png
      LAUNCH="gimp --no-splash --new-instance /tmp/sample.png"
      CLASS="gimp"; PAT="gimp"; RX="gimp|script-fu"; DRIVER=pointer ;;
    kdenlive)
      apt_install_full kdenlive; ver kdenlive --version
      export QT_QPA_PLATFORM=xcb KDE_FULL_SESSION=true
      LAUNCH="kdenlive"
      CLASS="kdenlive"; PAT="kdenlive"; RX="kdenlive|melt"; DRIVER=pointer ;;
    chrome)
      ver google-chrome --version
      python3 - > /tmp/page.html <<'PY'
print('<html><body><textarea rows=12 cols=100 autofocus></textarea>')
for i in range(400): print(f'<p>Paragraph {i}: the quick brown fox jumps over the lazy dog, again and again, to give the page something to scroll and reflow.</p>')
print('</body></html>')
PY
      LAUNCH="google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data file:///tmp/page.html"
      CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=stream; STREAM=ie ;;
    webrtc)
      ver google-chrome --version
      LAUNCH="google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --allow-file-access-from-files file://$TOOLS/webrtc-loopback.html"
      CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=none ;;
    mpv-video|mpv-audio)
      apt_install mpv ffmpeg; ver mpv --version
      ffmpeg -loglevel error -f lavfi -i testsrc=size=1280x720:rate=30 -f lavfi -i sine=frequency=440:sample_rate=48000 -t 120 -c:v libx264 -preset veryfast -pix_fmt yuv420p -c:a aac /tmp/test.mp4; rec ffmpeg.rc "$?"
      if [ "$app" = mpv-video ]; then LAUNCH="mpv --no-config --vo=x11 --ao=null --loop=inf /tmp/test.mp4"; else LAUNCH="mpv --no-config --no-video --ao=null --loop=inf --force-window=yes /tmp/test.mp4"; fi
      CLASS="mpv"; PAT="test.mp4"; RX="mpv|^ *vo|^ *ao|demux|lavc|av:"; DRIVER=none ;;
    *) echo "unknown app $app" >&2; return 1 ;;
  esac
}
apt_install() { sudo apt-get install -y --no-install-recommends "$@" > "$OUT/apt.log" 2>&1; rec apt.rc "$?"; }
apt_install_full() { sudo apt-get install -y "$@" > "$OUT/apt.log" 2>&1; rec apt.rc "$?"; }
ver() { rec version "$("$@" 2>&1 | head -1 | tr -d '\n' | head -c 200)"; }
