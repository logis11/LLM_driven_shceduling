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
  STREAM=""; AREA="0,0,0,0"; POSTLAUNCH=""; POSTCLASS=""; OP=""; ALTPRELUDE=""; KINDS="key,click,drag,wheel"
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
      # 9.5 D61: the 136M phase starts from the committed file — a pristine copy, and a key for VS Code's File: Revert
      # File (no default binding) so the prelude can return the unsaved buffer to it
      cp /tmp/project/source/index.ts /tmp/index.ts.orig
      mkdir -p /tmp/vscode-data/User
      printf '[{"key": "ctrl+alt+shift+r", "command": "workbench.action.files.revert"}]\n' > /tmp/vscode-data/User/keybindings.json
      LAUNCH="code --no-sandbox --disable-gpu --user-data-dir=/tmp/vscode-data --disable-workspace-trust --skip-welcome --skip-release-notes /tmp/project /tmp/project/source/index.ts"
      # the replayed pointer events must stay in the editor: the Explorer (27 % of the width) and the secondary side
      # bar are hidden after launch (Ctrl+B, Ctrl+Alt+B) — with the 8 % left inset of run 35092593907 the SWELL-KW clicks
      # opened files in the Explorer and the typing drifted into Markdown files; before the second stream the file is
      # reopened so both streams start on source/index.ts, and (D61) restored to its committed text: Escape closes any
      # widget the stream left open, the pristine copy goes back to disk (the stream may have saved), the buffer is
      # reverted to it, the caret goes to the end
      CLASS="code"; PAT="vscode-data"; RX="code|Code"; DRIVER=stream; STREAM=word; AREA="0.12,0.03,0.05,0.03"
      POSTLAUNCH="sleep 20; xdotool key ctrl+b; sleep 1; xdotool key ctrl+alt+b; sleep 1; xdotool key ctrl+End"
      ALTPRELUDE="xdotool key Escape; sleep 1; cp /tmp/index.ts.orig /tmp/project/source/index.ts; code --user-data-dir=/tmp/vscode-data --reuse-window /tmp/project/source/index.ts; sleep 4; xdotool key ctrl+alt+shift+r; sleep 8; xdotool key ctrl+End" ;;
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
      # 9.5 D28: keys only, at their recorded times — the stream's clicks, scrolls and drags moved the typing up the document
      KINDS="key"
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
    thunderbird-send)
      # 9.5 changelog D31 (from 9.7 D3): Thunderbird re-observed whole with operation `send` — the `thunderbird` setup
      # above, its SMTP server pointed at a local peer (smtp_peer.py: aiosmtpd on loopback, no authentication, no TLS,
      # on the harness CPUs), a copy of every sent message kept in Local Folders/Sent (the completion signal), and the
      # attachment: the Writer setup state's document (D22) with its ten pictures embedded, as .docx (CpsMark+'s
      # Outlook workload attaches Word files); pictures seeded so every repeat attaches the same bytes. Files live under
      # $HOME: Thunderbird is a snap on noble and its /tmp is private. The large-message confirmation is off: above
      # mailnews.message_warning_size (default 20 MiB) MessageSend.sys.mjs asks before delivery, and the send waits on it.
      # Attach File opens GTK's own chooser, whatever the automatic setting picks under the snap: through the desktop
      # portal with no portal service running it opens nothing (container check, Thunderbird 140, the pref at 1).
      appdef thunderbird || return 1
      cat >> "$HOME/tbprofile/user.js" <<'PREFS'
user_pref("mail.smtpserver.smtp1.hostname", "127.0.0.1");
user_pref("mail.smtpserver.smtp1.port", 2525);
user_pref("mail.smtpserver.smtp1.authMethod", 1);
user_pref("mail.smtpserver.smtp1.try_ssl", 0);
user_pref("mail.smtpserver.smtp1.username", "");
user_pref("mail.identity.id1.fcc", true);
user_pref("mail.identity.id1.fcc_folder", "mailbox://nobody@Local%20Folders/Sent");
user_pref("mail.warn_on_send_accel_key", false);
user_pref("mail.compose.attachment_reminder", false);
user_pref("mailnews.message_warning_size", 0);
user_pref("widget.use-xdg-desktop-portal.file-picker", 0);
PREFS
      sudo apt-get install -y --no-install-recommends python3-aiosmtpd libreoffice-writer unzip > "$OUT/apt.send.log" 2>&1; rec apt.send.rc "$?"
      mkdir -p "$HOME/tbdoc" && for k in 0 1 2 3 4 5 6 7 8 9; do convert -seed "$((k + 1))" -size 1024x768 plasma:fractal "$HOME/tbdoc/pic-$k.png"; done
      python3 "$TOOLS/writer_doc.py" "$HOME/tbdoc" > "$HOME/tbdoc/large.html"
      (cd "$HOME/tbdoc" && soffice --headless --infilter="HTML (StarWriter)" --convert-to "docx:MS Word 2007 XML" large.html > "$OUT/doc.convert.log" 2>&1); rec doc.convert.rc "$?"
      rec doc.bytes "$(stat -c %s "$HOME/tbdoc/large.docx" 2>/dev/null || echo 0)"
      rec doc.pictures "$(unzip -l "$HOME/tbdoc/large.docx" 2>/dev/null | grep -c 'word/media/')"
      rec doc.sha256 "$(sha256sum "$HOME/tbdoc/large.docx" 2>/dev/null | cut -d' ' -f1)"
      # D49: the .docx is the same size in every repeat and not the same bytes; its member listing — per-member
      # CRCs and stored dates — records which members move. Setup, before the peer, the launch and the settle.
      unzip -v "$HOME/tbdoc/large.docx" > "$OUT/doc.zip.txt" 2>&1; rec doc.zip.rc "$?"
      rec doc.crc_sha256 "$(sha256sum "$OUT/doc.zip.txt" 2>/dev/null | cut -d' ' -f1)"
      setsid python3 "$TOOLS/smtp_peer.py" 2525 "$OUT/smtp.jsonl" > "$OUT/smtp.log" 2>&1 &
      echo $! > "$OUT/smtp.pid"; sleep 2
      rec smtp.peer "$(python3 -c 'import socket; s = socket.create_connection(("127.0.0.1", 2525), 5); print(s.recv(200).decode().strip())' 2>&1 | head -c 120)"
      OP=send ;;
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
      # shortcuts for the zone actions (shipped without defaults): KXMLGUI merges the ActionProperties of a per-user
      # copy of the app's ui file — <GenericDataLocation>/kxmlgui5/kdenlive/kdenliveui.rc (kxmlguiclient.cpp) — into the
      # shipped file when the user's copy carries a LOWER version (kxmlguiversionhandler.cpp: the best version wins,
      # the local ActionProperties are stored into it). Kdenlive's own file is a compiled-in resource (version 227), so the
      # per-user file is this stub at version 1; an equal version would replace the whole GUI (probe 35090333141: crash).
      mkdir -p "$HOME/.local/share/kxmlgui5/kdenlive" "$HOME/.config"
      cat > "$HOME/.local/share/kxmlgui5/kdenlive/kdenliveui.rc" <<'RC'
<!DOCTYPE kpartgui SYSTEM "kpartgui.dtd">
<kpartgui name="kdenlive" version="1">
<ActionProperties scheme="Default">
  <Action name="clear_render_timeline_zone" shortcut="Ctrl+Shift+F10"/>
  <Action name="set_render_timeline_zone" shortcut="Ctrl+Shift+F9"/>
</ActionProperties>
</kpartgui>
RC
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
      CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=stream; STREAM=ie; AREA="0.13,0,0.02,0.02"; OP=page-load
      # 9.5 D60: the 136M phase types into the text box whatever the SWELL-KW window left — a click on blank body right
      # of the box (x 18–842 at the page's top) takes focus off any field, Ctrl+Home scrolls to the top, a click in the
      # box and Ctrl+End put the caret after its text
      ALTPRELUDE="xdotool mousemove 950 600 click 1; sleep 1; xdotool key ctrl+Home; sleep 2; xdotool mousemove 430 255 click 1; sleep 1; xdotool key ctrl+End" ;;
    chrome-hidden|chrome-visible)
      # 9.8 D13: the two renderer subjects. The flags match the `chrome` arm above — web-browser carries Chrome's
      # tree minus its renderers (9.5 D14) and these entries carry the renderers, so the two halves of one
      # application must be the same program launched the same way; tests/test_meas_desktop.py asserts the three
      # arms' flag portions are identical. The `chrome` arm is not called: its feed page costs thirty ImageMagick
      # renders and a server these subjects never use, each an unguarded way for an expensive job to die.
      ver google-chrome --version
      # N origins are N loopback addresses, not N ports: a site is scheme plus eTLD+1 (S2-01), which excludes the
      # port, so N ports on one address would share one site-locked renderer. 127.0.0.0/8 is routed to lo with no
      # interface configuration, and an address literal needs no name resolution — a resolver that failed to pick
      # up a hosts entry would leave the tabs unloaded, which is how the Phase 2 run was lost.
      N="${MEAS_ORIGINS:?chrome-hidden/chrome-visible need MEAS_ORIGINS}"
      PORT="${MEAS_PAGE_PORT:-8099}"; MS="${MEAS_TIMER_MS:?need MEAS_TIMER_MS}"
      # the page drives itself from its own load (idle-page.html): the hidden subject holds one period, the
      # visible subject walks a two-step plan, the timer and then none. Nothing is typed into a window.
      PAGEQ="${MEAS_PAGE_PLAN:+plan=$MEAS_PAGE_PLAN}"; PAGEQ="${PAGEQ:-ms=$MS}"
      mkdir -p /tmp/idle-page && cp "$TOOLS/idle-page.html" /tmp/idle-page/
      # one server answers every loopback address; --bind takes a single address, so it binds 0.0.0.0
      setsid python3 -m http.server "$PORT" --bind 0.0.0.0 --directory /tmp/idle-page > /tmp/idle-page/httpd.log 2>&1 &
      echo $! > "$OUT/httpd.pid"; sleep 1
      rec page.origins "$N"; rec page.port "$PORT"; rec page.timer_ms "$MS"; rec page.query "$PAGEQ"
      rec page.server "$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.2:$PORT/idle-page.html")"
      URLS=""; FIRST=""; REST=""
      for i in $(seq 2 $((N + 1))); do
        u="http://127.0.0.$i:$PORT/idle-page.html?$PAGEQ"
        URLS="$URLS $u"
        if [ -z "$FIRST" ]; then FIRST="$u"; else REST="$REST $u"; fi
      done
      rec page.urls "$URLS"
      # The flags are the `chrome` arm's, plus exactly one: Chrome keeps a spare renderer warm for the next
      # navigation, and it hosts no page but is a --type=renderer process indistinguishable from a real one by
      # command line. The dry run of 2026-09-20 measured it at 0.356 wakes/s beside three page renderers at
      # ~10.6, taking the entry's per-renderer value from 10.64 to 8.07. It cannot be separated afterwards — in
      # the hidden subject it reads 5 wakes against the measured tabs' 8 — so it is not created. The flag
      # changes only the renderer population, which is the half `web-browser` excludes (9.5 D14) and these
      # entries own; the browser, GPU and utility processes launch as they do for `chrome`.
      CHROME="google-chrome --no-sandbox --disable-gpu --no-first-run --user-data-dir=/tmp/chrome-data --disable-features=SpareRendererForSitePerProcess"
      if [ "$app" = chrome-hidden ]; then
        # one window: the first tab stays selected and is the control tab, the N measured tabs are background
        # pages. The control tab carries the SAME timer as the measured pages: being the selected tab it stays
        # visible to Blink and is never throttled, so it wakes at the timer rate while the measured renderers
        # fall to the documented budget — a gap of some 600x that identifies it for exclusion. (It cannot be
        # identified by role or command line, and the components' coverage cut does not separate it: every
        # renderer shares the same thread comms.)
        LAUNCH="$CHROME http://127.0.0.1:$PORT/idle-page.html?ms=$MS$URLS"
      else
        # N windows, one tab each: every mapped window's selected tab is visible to Blink, the occlusion tracker
        # that would hide a covered window being Windows-only (D4). The first window comes from the launch; the
        # rest are asked for by a second invocation against the same profile, which the running browser serves
        # and which then exits — the windows are created by the already-pinned process.
        LAUNCH="$CHROME $FIRST"
        POSTLAUNCH=""
        for u in $REST; do
          POSTLAUNCH="$POSTLAUNCH google-chrome --user-data-dir=/tmp/chrome-data --new-window '$u' > /dev/null 2>&1; sleep 2;"
        done
      fi
      CLASS="google-chrome|Google-chrome"; PAT="chrome-data"; RX="chrome"; DRIVER=none ;;
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
  echo "python3 $TOOLS/ops_driver.py $APP $wid $secs $OUT/ops.jsonl --pat '$PAT' $*"
}
appdef_cleanup() {
  [ -f "$OUT/httpd.pid" ] && kill "$(cat "$OUT/httpd.pid")" 2>/dev/null
  [ -f "$OUT/smtp.pid" ] && kill "$(cat "$OUT/smtp.pid")" 2>/dev/null
  return 0
}
