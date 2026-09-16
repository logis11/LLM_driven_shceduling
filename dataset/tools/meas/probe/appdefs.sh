#!/usr/bin/env bash
# appdefs.sh — install and launch definitions per application, shared by the
# probe (apps.sh) and the campaign (campaign/run.sh). `appdef <app>` installs
# the application and sets LAUNCH, CLASS (window class/name regex), PAT
# (process-tree pattern for snapshot.py), RX (comm regex for perf rows),
# DRIVER (type | pointer | stream | none), STREAM (word | outlook | ie) and,
# for an application with a heavy operation (9.5 follow-ups spec decisions
# 7–10), OP (the operation name ops_driver.py implements).
# Requires common.sh sourced and Xvfb running (version checks need a display).
#
# Setup states and operation inputs (spec decision 10): taken from the
# benchmark documentation where it states the corresponding input — PCMark 10
# Technical Guide (11 Feb 2021): Photo Editing image 4952 × 3288 (p. 71) and
# the unsharp-mask filter with its batch parameters (p. 74); Video Editing
# 1080p H.264 sharpened with ffmpeg unsharp lx=7:ly=7:la=0.56:cx=7:cy=7:
# ca=0.28 (p. 76); Web Browsing pages served by a local server, a feed page
# updated by script and a shop page with high-resolution images (pp. 52–53);
# CpsMark+ §4.3.3: Chrome pages "contain text, pictures, JS scripts" from
# local services. Everything else — document length, project, clip length,
# image content, page sizes — is design and says so below.

appdef() {
  local app="$1"
  export DEBIAN_FRONTEND=noninteractive
  STREAM=""; AREA="0,0,0,0"; POSTLAUNCH=""; POSTCLASS=""; OP=""
  case "$app" in
    code)
      wget -qO /tmp/code.deb "https://update.code.visualstudio.com/latest/linux-deb-x64/stable"; rec download.rc "$?"
      apt_install_full /tmp/code.deb; ver code --version
      # setup state (design): a TypeScript project open with its dependencies installed, so VS Code's built-in
      # TypeScript language server (tsserver) runs and re-checks the file the stream types into.
      # Project: sindresorhus/got at commit 64f21e2a4797b8c56493143e416508893983063f (tag v16.0.0), pinned.
      GOT_SHA=64f21e2a4797b8c56493143e416508893983063f
      mkdir -p /tmp/project && wget -qO /tmp/project.tar.gz "https://github.com/sindresorhus/got/archive/$GOT_SHA.tar.gz"; rec project.download.rc "$?"
      tar -xzf /tmp/project.tar.gz -C /tmp/project --strip-components=1; rec project.untar.rc "$?"
      (cd /tmp/project && npm install --ignore-scripts --no-audit --no-fund > /tmp/npm.log 2>&1); rec project.npm.rc "$?"
      rec project.files "$(find /tmp/project -name '*.ts' -not -path '*/node_modules/*' | wc -l)"
      rec node.version "$(node --version 2>/dev/null)"
      LAUNCH="code --no-sandbox --disable-gpu --user-data-dir=/tmp/vscode-data --disable-workspace-trust --skip-welcome --skip-release-notes /tmp/project /tmp/project/source/index.ts"
      CLASS="code"; PAT="vscode-data"; RX="code|Code"; DRIVER=stream; STREAM=word; AREA="0.10,0.08,0.05,0.03"
      POSTLAUNCH="sleep 20; xdotool key ctrl+End" ;;
    soffice)
      apt_install libreoffice-writer libreoffice-gtk3; ver soffice --version
      # setup state (design): a large document — 100 pages of running text (≈ 50 000 words) with ten
      # 1024×768 pictures, generated here and converted to ODT headless; the stream types at its end.
      mkdir -p /tmp/doc && for k in 0 1 2 3 4 5 6 7 8 9; do convert -size 1024x768 plasma:fractal "/tmp/doc/pic-$k.png"; done
      python3 - > /tmp/doc/large.html <<'PY'
words = "the quick brown fox jumps over the lazy dog while the office desktop schedules its interactive work and the writer keeps typing".split()
print("<html><body>")
for page in range(100):
    print(f"<h2>Section {page + 1}</h2>")
    for para in range(5):
        seed = page * 5 + para
        print("<p>" + " ".join(words[(seed * 7 + k * 13) % len(words)] for k in range(100)) + ".</p>")
    if page % 10 == 0:
        print(f'<p><img src="pic-{page // 10}.png" width="480" height="360"></p>')
print("</body></html>")
PY
      # --infilter forces the Writer module: without it LibreOffice imports HTML into Writer/Web and the result opens as a web document (probe 35087191213)
      (cd /tmp/doc && soffice --headless --infilter="HTML (StarWriter)" --convert-to odt:writer8 large.html > /tmp/doc/convert.log 2>&1); rec doc.convert.rc "$?"
      rec doc.bytes "$(stat -c %s /tmp/doc/large.odt 2>/dev/null || echo 0)"
      LAUNCH="soffice --norestore --nologo --nofirststartwizard /tmp/doc/large.odt"
      CLASS="libreoffice|soffice"; PAT="soffice"; RX="soffice"; DRIVER=stream; STREAM=word; AREA="0.30,0.15,0.08,0.20"
      POSTLAUNCH="sleep 10; xdotool key ctrl+End" ;;
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
      CLASS="thunderbird"; PAT="thunderbird"; RX="thunderbird|Isolated|Web Content"; DRIVER=stream; STREAM=outlook; AREA="0.30,0.02,0.05,0.02"
      POSTLAUNCH="sleep 8; xdotool key Escape; sleep 2; xdotool key ctrl+n; sleep 6"; POSTCLASS="Write" ;;
    gimp)
      apt_install gimp; ver gimp --version
      # image: 4952 × 3288 (PCMark 10 Photo Editing interactive image, Technical Guide p. 71); content synthetic (design)
      convert -size 4952x3288 plasma:fractal /tmp/photo.png; rec photo.rc "$?"
      # operation `unsharp-mask` through the Script-Fu server started with the GUI (ops_driver.py)
      LAUNCH="gimp --no-splash --new-instance -b '(plug-in-script-fu-server RUN-NONINTERACTIVE \"127.0.0.1\" 10008 \"\")' /tmp/photo.png"
      CLASS="gimp"; PAT="gimp"; RX="gimp|script-fu"; DRIVER=pointer; OP=unsharp-mask ;;
    kdenlive)
      apt_install_full kdenlive ffmpeg; ver kdenlive --version
      export QT_QPA_PLATFORM=xcb KDE_FULL_SESSION=true
      # clip: 1920×1080 H.264 (PCMark 10 Video Editing, Technical Guide p. 76); 20 s at 30 fps, synthetic content (design)
      ffmpeg -loglevel error -y -f lavfi -i testsrc=size=1920x1080:rate=30 -t 20 -an -c:v libx264 -preset veryfast -pix_fmt yuv420p /tmp/clip.mp4; rec ffmpeg.rc "$?"
      python3 "$TOOLS/kdenlive_project.py" /tmp/clip.mp4 600 30 /tmp/project.kdenlive; rec project.rc "$?"
      rec melt.unsharp "$(melt -query filter=avfilter.unsharp 2>/dev/null | grep -c identifier)"
      # shortcuts for the zone actions (shipped without defaults): KXMLGUI applies the ActionProperties of the per-user
      # copy of the app's ui file (kxmlguiclient.cpp: <GenericDataLocation>/kxmlgui5/<app>/<file>; kxmlguifactory.cpp
      # refreshActionProperties) — the shipped file with one element added, same version, so nothing else changes
      RC=$(ls /usr/share/kxmlgui5/kdenlive/kdenliveui.rc /usr/share/kdenlive/kdenliveui.rc 2>/dev/null | head -1); rec kdenlive.rc "$RC"
      mkdir -p "$HOME/.local/share/kxmlgui5/kdenlive" "$HOME/.config"
      python3 - "$RC" "$HOME/.local/share/kxmlgui5/kdenlive/kdenliveui.rc" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
xml = open(src, encoding="utf-8").read() if src else '<!DOCTYPE kpartgui SYSTEM "kpartgui.dtd">\n<kpartgui name="kdenlive" version="227">\n</kpartgui>\n'
props = ('<ActionProperties scheme="Default">\n'
         '  <Action name="clear_render_timeline_zone" shortcut="Ctrl+Shift+F10"/>\n'
         '  <Action name="set_render_timeline_zone" shortcut="Ctrl+Shift+F9"/>\n'
         '</ActionProperties>\n')
i = xml.rfind("</kpartgui>")
open(dst, "w", encoding="utf-8").write(xml[:i] + props + xml[i:] if i >= 0 else xml + props)
PY
      rec kdenlive.rc_user "$(grep -c ActionProperties "$HOME/.local/share/kxmlgui5/kdenlive/kdenliveui.rc")"
      printf '[timeline]\nautopreview=false\n' > "$HOME/.config/kdenliverc"
      LAUNCH="kdenlive /tmp/project.kdenlive"
      CLASS="kdenlive"; PAT="kdenlive"; RX="kdenlive|melt"; DRIVER=pointer; OP=preview-render ;;
    chrome)
      ver google-chrome --version
      python3 - > /tmp/page.html <<'PY'
print('<html><body><textarea rows=12 cols=100 autofocus></textarea>')
for i in range(400): print(f'<p>Paragraph {i}: the quick brown fox jumps over the lazy dog, again and again, to give the page something to scroll and reflow.</p>')
print('</body></html>')
PY
      # operation `page-load`: the scripted feed page (feed.html, design after PCMark 10 pp. 52–53 and CpsMark+ §4.3.3)
      # with thirty 1600×1200 pictures, served by a local server on the harness CPUs
      mkdir -p /tmp/feed && cp "$TOOLS/feed.html" /tmp/feed/ && for k in $(seq 0 29); do convert -size 1600x1200 plasma:fractal -quality 85 "/tmp/feed/img-$k.jpg"; done
      rec feed.images "$(ls /tmp/feed/img-*.jpg | wc -l)"
      setsid python3 -m http.server 8088 --bind 127.0.0.1 --directory /tmp/feed > /tmp/feed/httpd.log 2>&1 &
      echo $! > "$OUT/httpd.pid"; sleep 1
      rec feed.server "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8088/feed.html)"
      LAUNCH="google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data file:///tmp/page.html"
      CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=stream; STREAM=ie; AREA="0.13,0,0.02,0.02"; OP=page-load ;;
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
op_driver() { # op_driver <window-id> <seconds> [extra ops_driver args] — the operation loop for the `op` phase
  local wid="$1" secs="$2"; shift 2
  echo "python3 $TOOLS/ops_driver.py $APP $wid $secs $OUT/ops.jsonl $*"
}
appdef_cleanup() { [ -f "$OUT/httpd.pid" ] && kill "$(cat "$OUT/httpd.pid")" 2>/dev/null; return 0; }
