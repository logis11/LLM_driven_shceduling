# S2 — primary project and vendor documentation and source code

Reader S2 for task 9.5 "interactive and typing", stage 2 search. Class: primary project and vendor documentation and source code (T3, T4, T5; T1 and T2 only where a project documents its own measurements). All fetches on 2026-09-13 (UTC). Every commit id below was recorded from the clone or from `git ls-remote` at fetch time; `file:line` locators refer to that commit. Local copies live under `sources/S2-<id>/` (gitignored); the record does not depend on them.

Conventions in this file: "not an observation" means the source is documentation or code stating a default or a design, not a measured trace; a source is marked "one observation" only when it reports a measurement with machine, application, subject and window named.

---

## 1. Search log

Date for every row: 2026-09-13. "Engine/venue" is the site queried or the tool used. Status is the HTTP status curl reported; "OK" rows are 200 with usable content. Anubis = the host answered 200 with an anti-bot JavaScript challenge page ("Making sure you're not a bot!") instead of the document; treated as a dead end.

| # | Engine / venue | Query or URL | Result |
|---|---|---|---|
| 1 | raw.githubusercontent.com | GNOME/gtk main README.md (reachability probe) | 200 |
| 2 | git clone --depth 1 | gitlab.gnome.org/GNOME/gtk.git | OK, commit ae709f962a51f9108a1e6381bcfbd05bbaecc840 |
| 3 | git clone --depth 1 | gitlab.gnome.org/GNOME/glib.git | OK, 50d402c78a496e0fe51a846803a94b77285d6ab3 |
| 4 | git clone --depth 1 | github.com/qt/qtbase.git | OK, 21ef489f08e7d39bf744234154ca0146d381028b |
| 5 | git clone --depth 1 | github.com/qt/qtdeclarative.git | OK, 0c83f44827b34af74327707fafad352fe3bc6001 |
| 6 | git clone --depth 1 | gitlab.freedesktop.org/pipewire/pipewire.git | OK, 1cd56b0615bb8bd112d9a2865a41cfdf638692f6 |
| 7 | git clone --depth 1 | gitlab.freedesktop.org/pulseaudio/pulseaudio.git | OK, 77d25a1e613095bdf87a1d13b65e7c330565077a |
| 8 | git clone --depth 1 | github.com/mpv-player/mpv.git | OK, 13a4bfbc1a184c0576ca69c2de486a972aeb2407 |
| 9 | git clone --depth 1 | gitlab.freedesktop.org/wayland/wayland.git | OK, 381af21cf84f13be0ca24aed756a9cded3290d49 |
| 10 | git clone --depth 1 | gitlab.freedesktop.org/xorg/proto/xorgproto.git | OK, fcb7e9a1a0b593a44740d83b0babddd331fea830 |
| 11 | git clone --depth 1 | github.com/mltframework/mlt.git | OK, 64fa0287ed114bf3dac8ec8fd1e3d37164657c2d |
| 12 | git clone --depth 1 | gitlab.gnome.org/GNOME/gegl.git | OK, ce4948b06639a7e1838f903c87eef1d0fcfb2a97 |
| 13 | git clone --depth 1 | gitlab.gnome.org/GNOME/gimp.git | OK, d586c1c51cc7b3d3ba2758d9e23eb54c74ce0827 |
| 14 | git clone --depth 1 | github.com/alsa-project/alsa-lib.git | OK, f84cd4ced7b36fddb8e4ee24404cf7c091d27020 |
| 15 | git clone --depth 1 | code.videolan.org/videolan/vlc.git | OK, 289a425a89e36f3af8dae040259bbe27dc801b15 |
| 16 | git clone --depth 1 | github.com/microsoft/vscode.git | OK, 7fe7e98238e3ce45219881622cf2abdee0b426a5 |
| 17 | git clone --depth 1 | github.com/electron/electron.git | OK, b260e07d9ce0465d0687acf4c6e8044782c9430d |
| 18 | git clone --depth 1 | gitlab.freedesktop.org/gstreamer/gstreamer.git | OK, 4902f8122b10673f3fc1b70f7db2076464ce317c |
| 19 | git clone --depth 1 | github.com/alacritty/alacritty.git | OK, d692748d3f61253ebe9f5094320120d22f6a046f |
| 20 | git clone --depth 1 | github.com/zed-industries/zed.git | OK, 7960b2a7c9568e90fbe0727332149e5b2a5fd57a (repo grepped for latency docs; nothing quotable beyond the blog, not cited) |
| 21 | git clone --depth 1 | github.com/ThomasDickey/xterm-snapshots.git | OK, 9489b2056ee51fa9dd6a7087483b9b8f85d6a0c4 (no latency documentation found; not cited) |
| 22 | git ls-remote | github.com/chromium/chromium.git refs/heads/main | 184d9c6f21fe1c07572ade84e8682137813cf8ff |
| 23 | git ls-remote | github.com/mozilla-firefox/firefox.git refs/heads/main | 0304f5a3e392699f440f0e15f9ea0bc2790309c6 |
| 24 | git ls-remote | github.com/LibreOffice/core.git refs/heads/master | 2410e6d5e8f08f537a76027be263849a52181b2c |
| 25 | raw.githubusercontent.com chromium/chromium main | third_party/blink/renderer/platform/scheduler/README.md | 200 |
| 26 | raw.githubusercontent.com chromium/chromium main | third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md | 200 |
| 27 | raw.githubusercontent.com chromium/chromium main | third_party/blink/renderer/platform/scheduler/links.md | 200 (index of links only; not cited) |
| 28 | raw.githubusercontent.com chromium/chromium main | cc/README.md | 200 (not cited; superseded by docs/how_cc_works.md) |
| 29 | raw.githubusercontent.com chromium/chromium main | cc/scheduler/README.md | 404 |
| 30 | raw.githubusercontent.com chromium/chromium main | third_party/blink/renderer/platform/scheduler/main_thread/README.md | 404 |
| 31 | raw.githubusercontent.com chromium/chromium main | components/viz/README.md | 200 |
| 32 | raw.githubusercontent.com chromium/chromium main | components/viz/common/frame_sinks/begin_frame_args.h | 200 (read; no cadence default stated; not cited) |
| 33 | raw.githubusercontent.com chromium/chromium main | docs/how_cc_works.md | 200 |
| 34 | raw.githubusercontent.com chromium/chromium main | docs/threading_and_tasks.md | 200 |
| 35 | raw.githubusercontent.com chromium/chromium main | docs/speed/metrics_changelog/README.md | 200 (changelog index; not cited) |
| 36 | api.github.com | repos/chromium/chromium/commits/main | 403 (commit id taken via git ls-remote instead) |
| 37 | api.github.com | repos/mozilla-firefox/firefox/commits/main | 403 |
| 38 | api.github.com | repos/LibreOffice/core/commits/master | 403 |
| 39 | raw.githubusercontent.com mozilla-firefox/firefox main | layout/base/nsRefreshDriver.cpp, nsRefreshDriver.h | 200, 200 |
| 40 | raw.githubusercontent.com mozilla-firefox/firefox main | modules/libpref/init/all.js, StaticPrefList.yaml | 200, 200 |
| 41 | raw.githubusercontent.com mozilla-firefox/firefox main | widget/gtk/nsLookAndFeel.cpp, widget/LookAndFeel.h | 200, 200 |
| 42 | hg.mozilla.org comm-central | raw-file/tip/mailnews/mailnews.js; raw-file/tip/mail/app/profile/all-thunderbird.js; json-log?rev=tip | 200, 200, 200 — tip node 7fed5f308e374cfa07ea2d67a05be7949c1452f3 |
| 43 | webrtc.googlesource.com src main (?format=TEXT) | video/video_stream_encoder.h; video/video_stream_encoder.cc; modules/video_capture/video_capture_defines.h; modules/video_capture/linux/video_capture_v4l2.cc; media/base/media_constants.h; media/base/media_constants.cc; video/frame_cadence_adapter.h; video/frame_cadence_adapter.cc; `+/refs/heads/main?format=JSON` | all 200 — main commit e42b7b0ed1123ed5051d4716e370bf0639c246f0 |
| 44 | raw.githubusercontent.com LibreOffice/core master | vcl/README.scheduler.md | 200 |
| 45 | raw.githubusercontent.com LibreOffice/core master | vcl/README.scheduler | 404 (file is `.md`) |
| 46 | raw.githubusercontent.com LibreOffice/core master | vcl/source/app/scheduler.cxx; include/vcl/scheduler.hxx; include/vcl/task.hxx; vcl/source/app/settings.cxx | 200 ×4 |
| 47 | raw.githubusercontent.com LibreOffice/core master | officecfg/registry/schema/org/openoffice/Office/Recovery.xcs; …/Common.xcs; officecfg/registry/data/org/openoffice/Office/Recovery.xcu | 200 ×3 |
| 48 | raw.githubusercontent.com LibreOffice/core master | sw/README.md; editeng/README.md | 200, 200 (no timer values; not cited) |
| 49 | raw.githubusercontent.com LibreOffice/core master | sw/source/core/doc/DocumentTimerManager.cxx; sw/source/core/inc/DocumentTimerManager.hxx; editeng/source/editeng/impedit2.cxx | 200 ×3 |
| 50 | docs.pipewire.org | page_man_pipewire_conf_5.html; page_man_pw-top_1.html | 200, 200 (same text as repo `doc/dox`; repo copies cited) |
| 51 | gitlab.freedesktop.org/pipewire/pipewire/-/wikis | Config-PipeWire (.md and ?format=raw); Performance-tuning (.md and ?format=raw); home?format=raw; FAQ?format=raw | 200 ×6 but Anubis challenge page each time — dead end |
| 52 | www.freedesktop.org/wiki | Software/PulseAudio/Documentation/Developer/Clients/LatencyControl/; Software/PulseAudio/Documentation/User/PerfectSetup/ | 418, 418 |
| 53 | gavv.net | articles/pulseaudio-under-the-hood/ | 200 (third-party article, not primary; not cited) |
| 54 | code.visualstudio.com | docs/reference/default-settings | 200 but the served HTML carries no `cursorBlinking` text (settings table rendered client-side) — dead end; source code cited instead |
| 55 | raw.githubusercontent.com microsoft/vscode main | .github/perf.md | 404 |
| 56 | raw.githubusercontent.com/wiki microsoft/vscode | Performance-Issues.md; Source-Code-Organization.md | 200, 200 |
| 57 | support.zoom.com | hc/en/article?id=zm_kb&sysparm_article=KB0061059 | 200, JavaScript shell only ("Loading…"), no article text |
| 58 | support.zoom.us | hc/en-us/articles/204003179-System-requirements-for-Linux | 200, JavaScript shell only |
| 59 | support.zoom.com | hc/en/article?id=zm_kb&sysparm_article=KB0060748 | 200, JavaScript shell only (102 characters of text) |
| 60 | web.archive.org | web/2026id_/https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060748 | 200, gzip body; decoded to full article text (cited as S2-17) |
| 61 | doc.qt.io | qt-6/qguiapplication.html; qstylehints.html; qtquick-visualcanvas-scenegraph.html; qtimer.html; qabstractanimation.html | 200 ×5 (same text as qtbase/qtdeclarative sources; sources cited) |
| 62 | zed.dev | blog/videogame | 200 |
| 63 | github.com | neovim/neovim/issues/2976 | 403 |
| 64 | firefox-source-docs.mozilla.org | performance/index.html; layout/index.html | 200, 200 (index pages only, no measurements or refresh-driver values; not cited) |
| 65 | chromium.googlesource.com | chromium/src/+/main/third_party/blink/renderer/platform/scheduler/README.md | 200 (rendered; raw copy cited) |
| 66 | www.chromium.org | developers/design-documents/rendering-benchmarks/ | 200 |
| 67 | webrtc.github.io | webrtc-org/native-code/native-apis/ | 200 |
| 68 | jitsi.github.io | handbook/docs/dev-guide/dev-guide-web | 404 |
| 69 | microsoft.github.io | monaco-editor/typedoc/interfaces/editor.IEditorOptions.html | 404 |
| 70 | docs.gtk.org | gdk4/class.FrameClock.html; gtk4/property.Settings.gtk-cursor-blink-time.html; gtk4/property.Settings.gtk-cursor-blink-timeout.html; glib/main-loop.html; gtk4/drawing-model.html | 200 ×5 |
| 71 | mpv.io | manual/stable/ | 200 (same text as DOCS/man; repo cited) |
| 72 | www.alsa-project.org | alsa-doc/alsa-lib/pcm.html; group___p_c_m.html | 200, 200 (generated from src/pcm/pcm.c; source cited) |
| 73 | gstreamer.freedesktop.org | documentation/audio/gstaudiobasesink.html; pulseaudio/pulsesink.html; base/gstbasesink.html | 200 ×3 (generated from sources; sources cited) |
| 74 | gitlab.freedesktop.org/gstreamer/gstreamer/-/raw/main | subprojects/gstreamer/docs/random/design/qos.txt | 200 but Anubis challenge — dead end |
| 75 | www.spotify.com | us/download/linux/ | 200 |
| 76 | raw.githubusercontent.com electron/electron main | docs/tutorial/process-model.md | 200 (identical SHA-256 to the clone's copy) |
| 77 | docs.kdenlive.org | en/user_interface/menu/settings_menu/configure_kdenlive/playback.html | 404 |
| 78 | docs.kdenlive.org | en/exporting/render.html; en/getting_started/configure_kdenlive/configuration_environment.html | 200, 200 |
| 79 | userbase.kde.org | Kdenlive/Manual/Settings_Menu/Configure_Kdenlive | 200 |
| 80 | wiki.videolan.org | Hacker_Guide/Video_Output/; Hacker_Guide/Core/ | 200, 200 (read; no timing constants; VLC source cited instead) |
| 81 | WebSearch | `Chromium documentation input latency "renderer" main thread scheduler input priority docs` | hits: scheduler links.md, RenderingNG page, how_cc_works, threading_and_tasks — followed rows 25–34 |
| 82 | WebSearch | `Zed editor blog typing latency measurement ms keystroke` | hits were third-party review blogs (petronellatech, tech-insider, weavai…) — not primary, none followed |
| 83 | WebSearch | `Kdenlive documentation preview render threads "processing threads" MLT real-time` | hits: docs.kdenlive.org render.html, configuration_environment.html, userbase.kde.org — followed rows 78–79 |
| 84 | WebSearch | `Zoom Linux client system requirements processor documentation support.zoom.com` | hit KB0060748 — followed rows 59–60 |
| 85 | WebSearch | `Alacritty documentation input latency measurement typometer` | hits: Alacritty CONTRIBUTING.md (cited from clone), danluu.com/term-latency, tomscii.sig7.se Zutty measurement, lwn.net — third-party measurements belong to S1/S3, not followed |

Totals: 5 WebSearch queries; 20 shallow clones; 3 ls-remote; about 95 file/page fetches (rows 25–80), of which dead ends: 8 × 404, 3 × 403, 2 × 418, 7 × Anubis challenge, 3 × Zoom JavaScript shell, 1 × client-side-rendered settings page.

---

## 2. Candidates

### S2-01 GTK 4 / GDK frame clock, cursor blink, GLib main-loop priorities

**Citation.** GTK (GNOME), source tree at commit ae709f962a51f9108a1e6381bcfbd05bbaecc840 (gitlab.gnome.org/GNOME/gtk, main, 2026-09-13); GLib at commit 50d402c78a496e0fe51a846803a94b77285d6ab3 (gitlab.gnome.org/GNOME/glib, main); GTK 4 documentation page "The GTK Drawing Model", https://docs.gtk.org/gtk4/drawing-model.html (docs.gtk.org, current gtk4 docs, fetched 2026-09-13).

**Copy read.** `sources/S2-gtk/repo/` (files: gdk/gdkframeclock.c SHA-256 5ed21086c21e3dd8bd256c81be510c270696044be8df47e8cb3b4abd1530e28f; gdk/gdkframeclockidle.c 08dbba8b7b068f2dd1e5d5e8ab4194f517fcff02d9fe4700c31bd39adda5211a; gdk/gdksurface.c 9101ce7f660a03df40d77f1412f98d49226d4b74fd75e340069f8ab53e7a62d4; gtk/gtksettings.c 53720a79121615dfb37cc4cc9008522c9a300c4427ad016747ffea65254cacca; gtk/gtktext.c 79195a182cc33f6cdf38bb916484f4ae8905e46b35d40409f028d5f987b45af9); `sources/S2-glib/repo/glib/gmain.h` 0a105da4d9bd643cecaad56022e74c562f451f9d2912ef9a74ffff2b1426d94c; `sources/S2-gtk-docs/gtk4-drawing-model.html` 998c9442d81e80ba9fb5b9594cb65e36df49da8c72d8ea603b29aa34f65adc5d; `sources/S2-gtk-docs/gtk-settings-cursor-blink-time.html` 7ad6ed276f6d03955e20078b533dddfbb9251eb8d33b756ecaddf348c769e62a; `sources/S2-gtk-docs/gtk-settings-cursor-blink-timeout.html` 9c9e0fa6e4c44ed4f816327f37eb2d835dee8804c2ce363f8ac29ae96385ec63.

**Passages.**

gdk/gdkframeclock.c:53–58 (class doc):
> Tells the application when to update and repaint a surface.
>
> This may be synced to the vertical refresh rate of the monitor, for example. Even when the frame clock uses a simple timer rather than a hardware-based vertical sync, the frame clock helps because it ensures everything paints at the same time (reducing the total number of frames).

gdk/gdkframeclock.c:66–69:
> A frame clock is idle until someone requests a frame with [method@Gdk.FrameClock.request_phase]. At some later point that makes sense for the synchronization being implemented, the clock will process a frame and emit signals for each phase that has been requested.

gdk/gdkframeclock.c:192–197 (signal `flush-events`): "Used to flush pending motion events that are being batched up and compressed together." 225–232 (`update`): "Emitted as the first step of toolkit and application processing of the frame. Animations should be updated using [method@Gdk.FrameClock.get_frame_time]." 245–251 (`layout`): "Emitted as the second step of toolkit and application processing of the frame. Any work to update sizes and positions of application elements should be performed." 263–271 (`paint`): "Emitted as the third step of toolkit and application processing of the frame. The frame is repainted." 299–305 (`resume-events`): "Emitted after processing of the frame is finished. This signal is handled internally by GTK to resume normal event processing."

gdk/gdkframeclockidle.c:35:
> `#define FRAME_INTERVAL ((G_NSEC_PER_SEC + 30) / 60) /* nanoseconds */`

gdk/gdkframeclockidle.c:50:
> `uint64_t min_next_frame_time;          /* We're not synced to vblank, so wait at least until this before next cycle to avoid busy looping */`

gdk/gdkframeclockidle.c:241–247 (comment):
> In this first clock cycle, the "smooth" frame time is simply the time when the cycle was started. This could be followed by several cycles which are not vsync-related. As long as we don't get a "frame drawn" signal from the compositor, the clock cycles will occur every about frame_interval. Once we do get a "frame drawn" signal, from this point on the frame clock cycles will start shortly after the corresponding vsync signals, again every about frame_interval.

gdk/gdkframeclockidle.c:270–273:
> Note that the clock cycle cadence changed after the first vsync-related cycle. This cadence is kept even if we don't receive a 'frame drawn' signal in a subsequent frame, since then we schedule the clock at intervals of refresh_interval.

gdk/gdksurface.c:1501–1511 (`gdk_surface_freeze_updates`): the function increments `surface->update_freeze_count` and, at 1509–1510, "`if (surface->update_freeze_count == 1) gdk_frame_clock_stop (surface->frame_clock);`" (GDK Wayland backend requests `wl_surface_frame` and freezes updates until the callback arrives: gdk/wayland/gdksurface-wayland.c:376 "`self->frame_callback = wl_surface_frame (self->display_server.wl_surface);`", :285 "`gdk_surface_thaw_updates (surface);`" inside `gdk_wayland_surface_frame_callback`.)

docs.gtk.org/gtk4/drawing-model.html, section "The frame clock":
> All GTK applications are mainloop-driven, which means that most of the time the app is idle inside a loop that just waits for something to happen and then calls out to the right place when it does. On top of this GTK has a frame clock that gives a "pulse" to the application. This clock beats at a steady rate, which is tied to the framerate of the output (this is synced to the monitor via the window manager/compositor). A typical refresh rate is 60 frames per second, so a new "pulse" happens roughly every 16 milliseconds.

same section:
> The Events phase is a stretch of time between each redraw where GTK processes input events from the user and other events (like e.g. network I/O). Some events, like mouse motion are compressed so that only a single mouse motion event per clock cycle needs to be handled. Once the Events phase is over, external events are paused and the redraw loop is run.

same section:
> If nothing requires the Update/Layout/Paint phases we will stay in the Events phase forever, as we don't want to redraw if nothing changes.

gtk/gtksettings.c:360–366 (property `gtk-cursor-blink-time`): doc "Length of the cursor blink cycle, in milliseconds."; pspec `g_param_spec_int ("gtk-cursor-blink-time", NULL, NULL, 100, G_MAXINT, 1200, …)`. docs.gtk.org page for the property: "Default value 1200".

gtk/gtksettings.c:369–379 (`gtk-cursor-blink-timeout`): doc "Time after which the cursor stops blinking, in seconds. The timer is reset after each user interaction. Setting this to zero has the same effect as setting [property@Gtk.Settings:gtk-cursor-blink] to %FALSE."; pspec range and default `1, G_MAXINT, 10`. docs.gtk.org page: "Default value 10".

gtk/gtktext.c:6748–6751:
> `#define CURSOR_ON_MULTIPLIER 2` / `#define CURSOR_OFF_MULTIPLIER 1` / `#define CURSOR_PEND_MULTIPLIER 3` / `#define CURSOR_DIVIDER 3`

glib/gmain.h:426–434 (`G_PRIORITY_DEFAULT` = 0): "In GLib this priority is used when adding timeout functions with [func@GLib.timeout_add]. In GDK this priority is used for events from the X server." 437–446 (`G_PRIORITY_HIGH_IDLE` = 100): "GTK uses %G_PRIORITY_HIGH_IDLE + 10 for resizing operations, and %G_PRIORITY_HIGH_IDLE + 20 for redrawing operations. (This is done to ensure that any pending resizes are processed before any pending redraws, so that widgets are not redrawn twice unnecessarily.)" 449–456 (`G_PRIORITY_DEFAULT_IDLE` = 200): "In GLib this priority is used when adding idle functions with [func@GLib.idle_add]."

**Coverage.** T3 — covers (documentation, not measurement): object = GTK 4 application wake structure; the toolkit documents that an idle application stays in the Events phase with no repaint wakeups, that repaint wakeups are driven by the compositor frame callback (Wayland `wl_surface_frame`) at the output refresh rate ("roughly every 16 milliseconds" at 60 Hz), that GDK falls back to a 60 Hz timer (`FRAME_INTERVAL` = 1 s/60) when no "frame drawn" signal arrives, that motion events are compressed to one per clock cycle, and that the text cursor blinks on a 1200 ms cycle (on 2/3, off 1/3 of the cycle) and stops after 10 s of no interaction. Unit: ms / Hz. Statistic: defaults and design statements only. Scope: GTK 4 (`main` branch 2026-09-13); population: none. T1, T2, T4, T5, T6, T7 — does not cover.

**One observation?** No — documentation and source defaults; not an observation. No machine, application, subject or window.

---

### S2-02 Qt 6 — cursor flash time, timer coalescing, animation timer, Qt Quick render loops

**Citation.** qtbase at commit 21ef489f08e7d39bf744234154ca0146d381028b (github.com/qt/qtbase, dev branch head on 2026-09-13); qtdeclarative at commit 0c83f44827b34af74327707fafad352fe3bc6001 (github.com/qt/qtdeclarative).

**Copy read.** `sources/S2-qtbase/repo/`: src/gui/kernel/qstylehints.cpp SHA-256 734318ec4b9cd558774caf4effa18b131a5002a98ae7ef3bf3413ce3686adacc; src/gui/kernel/qplatformtheme.cpp 043acb0b9ebb558399b1427e76f14aea0ff6728ae4352446be2e72d50b572b1b; src/corelib/kernel/qtimer.cpp db1624d33a8d1a20bcee00ca351811e682b3aa206c8b73dd6cd60f44cba92bc1; src/corelib/global/qnamespace.qdoc e2e457043fb7547ed7e4d60687b86fe7bcf0a14e3f69a0587d07869191a6ee5b; src/corelib/animation/qabstractanimation.cpp b2a7fbe591d1714c7acc14c66fdb61656760d9e1b6061396c925668ec964a1ee. `sources/S2-qtdeclarative/repo/src/quick/doc/src/concepts/visualcanvas/scenegraph.qdoc` cb3d5653e053d8a48fea3fb528bcc5754374576cf9b1d8b5d6db25794298a865.

**Passages.**

qstylehints.cpp:425–430:
> \property QStyleHints::cursorFlashTime
> \brief the text cursor's flash (blink) time in milliseconds.
>
> The flash time is the time used to display, invert and restore the caret display. Usually the text cursor is displayed for half the cursor flash time, then hidden for the same amount of time.

qplatformtheme.cpp:610–614 (`QPlatformTheme::defaultThemeHint`):
> `case QPlatformTheme::CursorFlashTime: return QVariant(1000);`

(qstylehints.cpp:432–437: `cursorFlashTime()` returns the explicitly set value if ≥ 0, else `themeableHint(QPlatformTheme::CursorFlashTime, QPlatformIntegration::CursorFlashTime)` — i.e. the platform theme may override the 1000 ms fallback.)

qtimer.cpp:94–96:
> For Qt::CoarseTimer and Qt::VeryCoarseTimer types, QTimer may wake up earlier than expected, within the margins for those types: 5% of the interval for Qt::CoarseTimer and 500 ms for Qt::VeryCoarseTimer.

qtimer.cpp:722–725: "\property QTimer::timerType … The default value for this property is \c Qt::CoarseTimer."

qnamespace.qdoc:3292–3296:
> On UNIX (including Linux, \macos, and iOS), Qt will keep millisecond accuracy for Qt::PreciseTimer. For Qt::CoarseTimer, the interval will be adjusted up to 5% to align the timer with other timers that are expected to fire at or around the same time. The objective is to make most timers wake up at the same time, thereby reducing CPU wakeups and power consumption.

qabstractanimation.cpp:51–53: "Note that neither the interval between calls nor the number of calls to this function are defined; though, it will normally be 60 updates per second." qabstractanimation.cpp:128: `#define DEFAULT_TIMER_INTERVAL 16`.

scenegraph.qdoc:155–157:
> There are two render loop variants available: \c basic, and \c threaded. \c basic is single-threaded, while \c threaded performs scene graph rendering on a dedicated thread.

scenegraph.qdoc:240–243:
> The threaded renderer is currently used by default on Windows with Direct3D 11 and with OpenGL when using opengl32.dll, Linux excluding Mesa llvmpipe, \macos with Metal, mobile platforms, and Embedded Linux with EGLFS, and with Vulkan regardless of the platform.

scenegraph.qdoc:250–252: "The non-threaded render loop is currently used by default on Windows with OpenGL when not using the system's standard opengl32.dll, \macos with OpenGL, WebAssembly, and Linux with some drivers."

scenegraph.qdoc:282–288:
> By default, a Qt Quick animation (such, as a \l NumberAnimation) is driven by the default animation driver. This relies on basic system timers, such as QObject::startTimer(). The timer typically runs with an interval of 16 milliseconds. […] This is how animations work with the \c basic render loop.

scenegraph.qdoc:296–302:
> This is what the \c threaded render loop implements. In fact, it installs not one, but two animation drivers: one on the gui thread (to drive regular animations, such as \l NumberAnimation), and one on the render thread […]. Both of these are advanced during the preparation of a frame, i.e. animations are now synchronized with rendering. This makes sense due to presentation being throttled to the display's vertical sync by the underlying graphics stack.

scenegraph.qdoc:306–312: "as the thread is being throttled to vsync, advancing animations (for \l Animator types) in each frame as if 16.67 milliseconds had elapsed gives more accurate results than relying on a system timer. (when throttled to the vsync timing, which is \c{1000/60} milliseconds with a 60 Hz refresh rate, it is fair to assume that it has been approximately that long since the same operation was done for the previous frame)"

scenegraph.qdoc:355–361: "When there is no renderable window, for example because our QQuickWindow is minimized (Windows) or fully obscured (macOS), we cannot present frames […]. In this case, the \c threaded render loop automatically switches over to a system timer based approach to drive animations".

**Coverage.** T3 — covers (documentation): object = Qt application wake structure; documents the cursor blink period fallback (1000 ms; visible half, hidden half), the default coarse-timer coalescing (up to 5 % of the interval, to reduce CPU wakeups), the animation tick (16 ms timer, "normally" 60 updates/s), and the thread organisation of Qt Quick (gui thread + dedicated render thread throttled to vsync by default on Linux except llvmpipe). Unit: ms, Hz. Statistic: defaults. Scope: Qt 6 dev branch. Population: none. T1, T2, T4, T5, T6, T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-03 Chromium — Blink main-thread scheduler, cc scheduler, threading

**Citation.** Chromium source at commit 184d9c6f21fe1c07572ade84e8682137813cf8ff (github.com/chromium/chromium `main`, 2026-09-13): `third_party/blink/renderer/platform/scheduler/README.md`, `third_party/blink/renderer/platform/scheduler/TaskSchedulingInBlink.md`, `docs/how_cc_works.md`, `docs/threading_and_tasks.md`, `components/viz/README.md`. Also Chromium design page "Rendering Benchmarks", https://www.chromium.org/developers/design-documents/rendering-benchmarks/ (fetched 2026-09-13).

**Copy read.** `sources/S2-chromium/blink-scheduler-README.md` SHA-256 877fe9ab9ff32f70e50a35a8edb3f706ea45ac70d2086b7e80ce89ace35aa2cc; `sources/S2-chromium/TaskSchedulingInBlink.md` 1bcbdbd9cad1caae87d26272b17501eb2acd6c7a8ab845aa2b158d72036443b8; `sources/S2-chromium-docs/how-cc-works.md` 0d11f78b53aa8fe6bba67d4ea0b38163aab918fbcc17460822d60c18af817593; `sources/S2-chromium-docs/threading-and-tasks.md` 9509b1038e0c5dc1091347599dd99e6a90987888078e65adbd9610e2a7c87999; `sources/S2-chromium/viz-README.md` e3b3b4e02a6216c887fa211e74d555aaa7f4533bc9597a578b102e2aca686134; `sources/S2-chromium-docs/input-latency-design.html` 715d95e467d7ff21d20228ba6eddfc00c13fa6dedb5b36457ebcc3d1ef228050.

**Passages.**

TaskSchedulingInBlink.md:9–13:
> Most of Blink is essentially single-threaded: most important things happen on the main thread (including JavaScript execution, DOM, CSS, layout calculations), which means that there are many things which want to run on the main thread at the same time. Therefore Blink needs a scheduling policy to prioritise the right thing — for example, to schedule input handling above everything else.

TaskSchedulingInBlink.md:107–117 (§ Scheduling policies › Priorities):
> The scheduler selects the next task to run based on the priority (modulo some starvation logic). The tasks with the same priority run in order.
> There are following rules to assign priorities:
> - Input task runner has the highest priority.
> - Compositor task runner has high priority when user gestures are observed.
> - There are several ongoing experiments to increase or decrease priorities for individual frames.
> The default priority is normal.

scheduler/README.md:3–15: "This directory contains the Blink Scheduler, which coordinates task execution in renderer processes. […] `main_thread` -- contains implementation of the main thread scheduler (`MainThreadSchedulerImpl`) and main thread scheduling policies. `worker` -- contains implementation of scheduling infrastructure for the non-main threads (compositor thread, worker threads)."

how_cc_works.md:22–25 (§ Process / thread architecture):
> cc can be embedded in both single-threaded and multi-threaded incarnations. The single-threaded version has less overhead. The multi-threaded version incurs a latency cost, but allows for input and animations to be responsively handled on one thread while the other thread is busy. In general, the browser uses the single-threaded version as its main thread is cheap and light, whereas the renderer uses the multi-threaded version as its main thread (Blink) can be quite busy on some pages.

how_cc_works.md:306–315 (§ Scheduling):
> cc's actions are driven by a cc::Scheduler. This is one of many schedulers in Chrome, including the Blink scheduler, the viz::DisplayScheduler, the browser UI task scheduler, and the gpu scheduler. […] cc::Scheduler code differentiates begin frames from the display compositor as BeginImplFrame (i.e. should cc produce a compositor frame) and a begin frame for its embedder as BeginMainFrame (i.e. should cc tell Blink to run requestAnimationFrame and produce a commit […]). The BeginImplFrame is driven by a viz::BeginFrameSource which in turn is driven the the display compositor.

how_cc_works.md:317: "In a full pipeline update with low latency and fast rasterization, the general scheduling flow is BeginImplFrame -> BeginMainFrame -> Commit -> ReadyToActivate -> Activate -> ReadyToDraw -> Draw."

how_cc_works.md:325–327: "The cc::Scheduler maintains a deadline by which it expects its embedder to respond. If the main thread is slow to respond, then the Scheduler may draw without waiting for a commit. If this happens, then Scheduler is considered to be in high latency mode."

how_cc_works.md:53–58 (§ Input Data Flow Overview): "In the renderer process, input is forwarded from the browser process. It is processed by ui::InputHandlerProxy (a cc::InputHandlerClient). […] Some input can't be handled by the compositor thread (e.g. there's a synchronous Javascript touch or wheel handler) and so that input is forwarded along to Blink to handle directly."

threading_and_tasks.md:28–32:
> Do not perform expensive computation or blocking IO on the main thread (a.k.a. "UI" thread in the browser process) or IO thread (each process's thread for receiving IPC). A busy UI / IO thread can cause user-visible latency, so prefer running that work on the thread pool.

Rendering Benchmarks page (www.chromium.org), § "Smoothness Metrics":
> Remember, unless you pass --disable-gpu-vsync, scrolling goes only as fast as your screen. So, for screen with 60 Hz refresh, 16.6 is usually a good thing.
> […] mean_frame_time: arithmetic mean of frame times […] mean_input_event_latency: time between receiving a touchmove event and performing the frame swap for the corresponding scroll event.

Same page, earlier, an example benchmark output line: "ms Avg frame_times: 17.267564ms Sd frame_times: 0.279332ms *RESULT jank: jank= 19.4673 *RESULT mean_frame_time: mean_frame_time= 17.268 ms" (no machine, date or page named; scrolling benchmark, not typing).

**Coverage.** T3 — covers (documentation): object = Chromium renderer wake structure; documents that the renderer main thread (Blink) is one thread with input tasks at highest priority and compositor tasks high during gestures; that the renderer uses a separate compositor thread (cc multi-threaded); that frame production is driven by BeginFrame messages from the display compositor (viz) rather than by input alone; that cc has a deadline/high-latency mode. Unit: none (design). Scope: Chromium main 2026-09-13. T2 — the Rendering Benchmarks page defines `mean_input_event_latency` (touchmove → frame swap) and shows one example run with mean frame time 17.268 ms, but it is a scrolling benchmark without machine or page; it does not report CPU per keystroke. Not usable as T2 evidence. T1, T4, T5, T6, T7 — does not cover.

**One observation?** No — design documentation; the benchmark page's example is not attributable (no machine, subject, window).

---

### S2-04 Electron process model; VS Code cursor blink, rendering scheduling, extension host

**Citation.** Electron docs `docs/tutorial/process-model.md` at commit b260e07d9ce0465d0687acf4c6e8044782c9430d (github.com/electron/electron main). VS Code source at commit 7fe7e98238e3ce45219881622cf2abdee0b426a5 (github.com/microsoft/vscode main): `src/vs/editor/common/config/editorOptions.ts`, `src/vs/editor/browser/viewParts/viewCursors/viewCursors.ts`, `src/vs/editor/browser/widget/codeEditor/codeEditorWidget.ts`. VS Code wiki page "Source Code Organization" (github.com/microsoft/vscode/wiki, fetched raw 2026-09-13).

**Copy read.** `sources/S2-electron/repo/docs/tutorial/process-model.md` SHA-256 f4c00bac9e25afe87dad781eb9a6bdaee798ed533dd58cb138692fe9a30cb961 (identical to the raw fetch at `sources/S2-electron-docs/process-model.md`); `sources/S2-vscode/repo/src/vs/editor/common/config/editorOptions.ts` 2fbb4e05e90219c42bbf49f02161c52aa83419e7a981f7ab206c3c426aec6bb5; `…/viewCursors.ts` b4f2e15e8600c3cf188b35bd3f99a0c8912046dd7d538f3dbb2a22fa6ffee1eb; `…/codeEditorWidget.ts` 18dd294ed185a29c590df75656f18f27d0cefc8d4d778559db946d447130e5d8; `sources/S2-vscode-docs/wiki-source-org.md` 385af2b6f69542c31e6dd69c306f6b972bdf1933ff55fddbea6daf940350442b.

**Passages.**

process-model.md:10–11: "Electron inherits its multi-process architecture from Chromium, which makes the framework architecturally very similar to a modern web browser." :44–46: "Each Electron app has a single main process, which acts as the application's entry point. The main process runs in a Node.js environment". :114–116: "Each Electron app spawns a separate renderer process for each open `BrowserWindow` (and each web embed). As its name implies, a renderer is responsible for _rendering_ web content." :220–223: "Each Electron app can spawn multiple child processes from the main process using the [UtilityProcess][] API. The utility process runs in a Node.js environment […] The utility process can be used to host for example: untrusted services, CPU intensive tasks or crash prone components".

VS Code wiki "Source Code Organization", first paragraph: "Visual Studio Code consists of a layered and modular `core` that can be extended using extensions. Extensions are run in a separate process referred to as the `extension host`."

editorOptions.ts:6238–6244:
> `cursorBlinking: register(new EditorEnumOption(` / `EditorOption.cursorBlinking, 'cursorBlinking',` / `TextEditorCursorBlinkingStyle.Blink, 'blink',` / `['blink', 'smooth', 'phase', 'expand', 'solid'],` / … / `{ description: nls.localize('cursorBlinking', "Control the cursor animation style.") }`

viewCursors.ts:32: `static readonly BLINK_INTERVAL = 500;`

viewCursors.ts:262–263:
> `if (blinkingStyle === TextEditorCursorBlinkingStyle.Blink) {` / `// flat blinking is handled by JavaScript to save battery life due to Chromium step timing issue https://bugs.chromium.org/p/chromium/issues/detail?id=361587`
(263–270: `this._cursorFlatBlinkInterval.cancelAndSet(() => { if (this._isVisible) { this._hide(); } else { this._show(); } }, ViewCursors.BLINK_INTERVAL, …)`.)

codeEditorWidget.ts:1770 (argument passed when constructing the `ViewModel`): `(callback) => dom.scheduleAtNextAnimationFrame(dom.getWindow(this._domElement), callback),`

**Coverage.** T3 — covers (documentation/source): object = Electron/VS Code process and wake structure; documents one main process + one renderer per window + utility processes; VS Code's extension host as a separate process; the editor cursor blinks by default (`blink` style) on a 500 ms JavaScript interval (so a focused idle editor wakes at least every 500 ms), and editor view updates are scheduled at the next animation frame (compositor-driven). Unit: ms. Statistic: defaults. Scope: VS Code main 2026-09-13. Population: none. T1, T2, T4–T7 — does not cover. The VS Code wiki "Performance Issues" page was fetched (row 56) but contains troubleshooting steps only, no measured typing latency; not quoted.

**One observation?** No — not an observation.

---

### S2-05 LibreOffice — VCL Scheduler, task priorities, autosave interval, Writer idle and spell timers

**Citation.** LibreOffice core at commit 2410e6d5e8f08f537a76027be263849a52181b2c (github.com/LibreOffice/core master, 2026-09-13): `vcl/README.scheduler.md`, `include/vcl/task.hxx`, `include/vcl/scheduler.hxx`, `officecfg/registry/schema/org/openoffice/Office/Recovery.xcs`, `sw/source/core/doc/DocumentTimerManager.cxx`, `editeng/source/editeng/impedit2.cxx`.

**Copy read.** `sources/S2-libreoffice/README.scheduler.md` SHA-256 21fb8417d0081faecdeb7209b8599a7cab085070a0228581c9c74b0a73712651; `task.hxx` c25a4697a40f062048116a6b7bd2dd3a5973dfe44de4004b94fa380304b648f7; `scheduler.hxx` 812c943f909961ecd9289f8cbd3d8d3e248bd7a4456226d20b23171901a738b6; `Recovery.xcs` 331a89a71f66b83e38f1798b28154aa2f103920ff8a68c8525a028862dcb6f8f; `DocumentTimerManager.cxx` c66b02b2a3f690d9da122565adbb92ce9bfc03ebc8d24685372f1ed52a954b4b; `impedit-onlinespell.cxx` (= editeng/source/editeng/impedit2.cxx) c9eed2f18550908727c83c538d174ea5cff2888a876be5c09afa3d712c02f9d8.

**Passages.**

vcl/README.scheduler.md:5–7:
> The VCL scheduler handles LOs primary event queue. It is simple by design, currently just a single-linked list, processed in list-order by priority using round-robin for reoccurring tasks.

:41–46 (§ Driving the scheduler AKA the system timer):
> 1. There is just one system timer, which drives LO event loop
> 2. The timer has to run in the main window thread
> 3. The scheduler is run with the Solar mutex acquired
> 4. The system timer is a single-shot timer
> 5. The scheduler system event / message has a low system priority. All system events should have a higher priority.

:48–52: "Every time a task is started, the scheduler timer is adjusted. When the timer fires, it posts an event to the system message queue. If the next most important task is an Idle (AKA instant, 0ms timeout), the event is pushed to the back of the queue, so we don't starve system messages, otherwise to the front."

:88–96 (§ Idle processing): "Instant (zero timeout) tasks, represented e.g. by the Idle class. This is a misnomer, as these tasks are processed after returning to the main loop. This is not necessarily when LO is idle, in fact such tasks may be invoked while there is input in the OS event queue pending. […] Low priority tasks, represented by priorities `TaskPriority::HIGH_IDLE` and lower. In addition to being invoked only when there is no task with a higher priority, pending input in the OS event queue also takes precedence."

:25–26: "C.1. Higher priority tasks starve lower priority tasks — As long as a higher task is available, lower tasks are never run!"

include/vcl/task.hxx:27–40:
> `enum class TaskPriority { HIGHEST, ///< These events should run very fast! DEFAULT, ///< Default priority used, e.g. the default timer priority // Input from the OS event queue is processed before HIGH_IDLE tasks. HIGH_IDLE, ///< Important idle events to be run before processing drawing events RESIZE, ///< Resize runs before repaint, so we won't paint twice REPAINT, ///< All repaint events should go in here SKIA_FLUSH, … POST_PAINT, ///< Everything running directly after painting DEFAULT_IDLE, ///< Default idle priority LOWEST, ///< Low, very idle cleanup tasks TOOLKIT_DEBUG … };`

include/vcl/scheduler.hxx:43–44: `static constexpr sal_uInt64 ImmediateTimeoutMs = 0;` / `static constexpr sal_uInt64 InfiniteTimeoutMs = SAL_MAX_UINT64;`

Recovery.xcs:130–133 and 148 (group `AutoSave`, prop `TimeIntervall`): `<desc>Specifies the AutoSave time interval in minutes.</desc>` … `<value>10</value>`; :115–122 (prop `Enabled`): `<desc>Specifies whether all modified documents are automatically saved in a time interval.</desc> <label>AutoSave every</label> … <value>true</value>`; constraints 135–147: "Specifies that the minimum time interval is 1 minute." / "Specifies that the maximum time interval is 60 minutes."

sw/source/core/doc/DocumentTimerManager.cxx:49–54:
> `m_aDocIdle.SetPriority(TaskPriority::LOWEST);` / `m_aDocIdle.SetInvokeHandler(LINK(this, DocumentTimerManager, DoIdleJobs));` / `m_aFireIdleJobsTimer.SetPriority(TaskPriority::DEFAULT_IDLE);` / … / `m_aFireIdleJobsTimer.SetTimeout(1000); // Enough time for LOK to render the first tiles.`

editeng/source/editeng/impedit2.cxx:142, 145, 148–149:
> `maStatusTimer.SetTimeout(200);` … `maIdleFormatter.SetPriority(TaskPriority::REPAINT);` … `maOnlineSpellTimer.SetTimeout(100);` / `maOnlineSpellTimer.SetInvokeHandler(LINK( this, ImpEditEngine, OnlineSpellHdl));`

**Coverage.** T3 — covers (documentation/source): object = LibreOffice wake structure; documents a single-threaded, single-system-timer, priority-ordered cooperative scheduler in the main thread; OS input processed before HIGH_IDLE and lower tasks; autosave default every 10 minutes; Writer's idle-jobs (layout/spell/grammar) run as a LOWEST-priority Idle after a 1000 ms timer; EditEngine (used for text boxes/Impress/Calc) online spell timer 100 ms, status timer 200 ms. Unit: ms, minutes. Statistic: defaults. Scope: LibreOffice master 2026-09-13. T1, T2, T4–T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-06 Gecko (Firefox/Thunderbird) — refresh driver, frame-rate prefs, caret blink, mail check interval

**Citation.** Firefox source at commit 0304f5a3e392699f440f0e15f9ea0bc2790309c6 (github.com/mozilla-firefox/firefox main, 2026-09-13): `layout/base/nsRefreshDriver.cpp`, `modules/libpref/init/StaticPrefList.yaml`, `widget/gtk/nsLookAndFeel.cpp`. Thunderbird comm-central tip 7fed5f308e374cfa07ea2d67a05be7949c1452f3 (hg.mozilla.org/comm-central, 2026-09-13): `mailnews/mailnews.js`.

**Copy read.** `sources/S2-gecko/nsRefreshDriver.cpp` SHA-256 acfe7e45c50b2ebecbd9f53035e2b9786dcf6f297938e5ff5427fe17b3e19a2f; `sources/S2-gecko/StaticPrefList.yaml` 74e45641a109ae6a61b671ccc1a55a2d9f6b3e292b78b24a2a934c1dfb36a5c7; `sources/S2-gecko/nsLookAndFeel-gtk.cpp` 025f7bc066285ede3ad34b639b2034e64014070696f3a76f4fde839bdea4ef28; `sources/S2-thunderbird/mailnews.js` c428e2a504e2939d0e2286a352b6a5a7389672c8e6ae197b44f7d3e6d9e809f6.

**Passages.**

nsRefreshDriver.cpp:114–115:
> `// after 10 minutes, stop firing off inactive timers` / `#define DEFAULT_INACTIVE_TIMER_DISABLE_SECONDS 600`

nsRefreshDriver.cpp:480–483 (`VsyncRefreshDriverTimer::GetTimerRate`):
> `// If hardware queries fail / are unsupported, we have to just guess.` / `return mVsyncRate != TimeDuration::Forever() ? mVsyncRate : TimeDuration::FromMilliseconds(1000.0 / 60.0);`

nsRefreshDriver.cpp:528–530: "// Compress vsync notifications such that only 1 may run at a time // This is so that we don't flood the refresh driver with vsync messages // if the main thread is blocked for long periods of time"

nsRefreshDriver.cpp:238–240: "// If we haven't painted for some time, then guess that we won't paint // again for a while, so the refresh driver is not a good way to predict // idle time."

nsRefreshDriver.cpp:1324–1326: `int32_t nsRefreshDriver::DefaultInterval() { return NSToIntRound(1000.0 / gfxPlatform::GetDefaultFrameRate()); }`

StaticPrefList.yaml:11566–11571:
> `# Pref to control browser frame rate, in Hz. A value <= 0 means choose` / `# automatically based on knowledge of the platform (or 60Hz if no platform-` / `# specific information is available).` / `- name: layout.frame_rate` / `type: RelaxedAtomicInt32` / `value: -1`

StaticPrefList.yaml:11574–11578: "# If it has been this many frame periods since a refresh, assume that painting # is quiescent (will not happen again soon). - name: layout.idle_period.required_quiescent_frames … value: 2"

StaticPrefList.yaml:11707–11710: `# Throttled frame rate, in frames per second.` / `- name: layout.throttled_frame_rate` / `type: uint32_t` / `value: 1`

widget/gtk/nsLookAndFeel.cpp:1866–1878:
> `gint blink_time = 0; // In milliseconds` / `gint blink_timeout = 0; // in seconds` / `gboolean blink;` / `g_object_get(settings, "gtk-cursor-blink-time", &blink_time, "gtk-cursor-blink-timeout", &blink_timeout, "gtk-cursor-blink", &blink, nullptr);` … `mCaretBlinkTime = blink && blink_timeout ? (int32_t)blink_time : 0;`

mailnews/mailnews.js:540: `pref("mail.server.default.check_time", 10);` (:539 `pref("mail.server.default.download_on_biff", false);`)

**Coverage.** T3 — covers (source): object = Gecko wake structure; the refresh driver ticks on vsync notifications (compressed to one pending), guesses 60 Hz when the hardware rate is unknown, throttles to 1 fps for inactive/background documents, stops inactive timers after 10 minutes, and Firefox on GTK takes its caret blink time from the GTK settings (S2-01: 1200 ms cycle, 10 s timeout). Thunderbird's default new-mail check interval is 10 (the pref is `check_time`; the source does not state the unit on that line — the unit is not quoted here). Unit: Hz, ms, s. Statistic: defaults. Scope: Firefox main and comm-central tip, 2026-09-13. T1, T2, T4–T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-07 GIMP / GEGL — projection idle rendering, chunk iterator interval, GEGL thread count

**Citation.** GIMP at commit d586c1c51cc7b3d3ba2758d9e23eb54c74ce0827 (gitlab.gnome.org/GNOME/gimp master): `app/core/gimpprojection.c`, `app/gimp-priorities.h`, `app/core/gimpchunkiterator.c`. GEGL at commit ce4948b06639a7e1838f903c87eef1d0fcfb2a97 (gitlab.gnome.org/GNOME/gegl master): `gegl/gegl-config.c`, `gegl/gegl-config.h`, `gegl/gegl-init.c`.

**Copy read.** `sources/S2-gimp/repo/app/core/gimpprojection.c` SHA-256 1d5a4bf86ab2046edb08edcc42320945e5f6149e8b2dccbd9aa83e862a8b21d6; `app/gimp-priorities.h` d15b451cbed68af8c7c6e3e818cdaee1931868c4f5fc5fd9ab64d968a2ddc16c; `app/core/gimpchunkiterator.c` c6881cc6f60251244585b9b0d38f5176c9305a5c57241753393f146ed3e08c0d; `sources/S2-gegl/repo/gegl/gegl-config.c` bd18225ebe711a04e9d3f299d04594cf4282f5aff85d3a8f00ec989f44572558; `gegl/gegl-config.h` 3b83e95e6214f32121087c1b4d34d2ed82ee85af152a657d9a42718250185641; `gegl/gegl-init.c` 204f03d3b1ab964cbff6e86bb27f3720bca6c018bb843dcbe3416b382d001be2.

**Passages.**

gimpprojection.c:50–52: `/* chunk size for area updates */` / `#define GIMP_PROJECTION_UPDATE_CHUNK_WIDTH 32` / `#define GIMP_PROJECTION_UPDATE_CHUNK_HEIGHT 32`

gimpprojection.c:521–524 (comment at 521, call at 522–524): `/* Construct in chunks - asynchronously in the main thread */` / `g_idle_add_full (G_PRIORITY_HIGH_IDLE, (GSourceFunc) gimp_projection_chunk_render_start, proj_ref, NULL);`

gimpprojection.c:743–745: `proj->priv->idle_id = g_idle_add_full (GIMP_PRIORITY_PROJECTION_IDLE + proj->priv->priority, (GSourceFunc) gimp_projection_chunk_render_callback, proj, NULL);`

gimp-priorities.h:33–34: `/* just a bit less than GDK_PRIORITY_REDRAW */` / `#define GIMP_PRIORITY_PROJECTION_IDLE (G_PRIORITY_HIGH_IDLE + 22)`

gimpchunkiterator.c:41–45: `/* the default iteration interval */` / `#define DEFAULT_INTERVAL (1.0 / 15.0) /* seconds */` / `/* the minimal area to process per iteration */` / `#define MIN_AREA_PER_ITERATION 4096`

gegl-config.c:73: `gint _gegl_threads = 1;` ; gegl-config.c:404–409: `g_param_spec_int ("threads", "Number of threads", "Number of concurrent evaluation threads", 0, GEGL_MAX_THREADS, _gegl_threads, …)`; gegl-config.h:59: `#define GEGL_MAX_THREADS 64`; gegl-init.c:459–461: `"gegl-threads", 0, 0, G_OPTION_ARG_STRING, &cmd_gegl_threads, N_("The number of concurrent processing threads to use"), "<threads>"`; gegl-init.c:542–544: `if (g_getenv ("GEGL_THREADS")) { _gegl_threads = atoi(g_getenv("GEGL_THREADS"));`.

**Coverage.** T3 — covers (source): object = GIMP image-editor wake structure; projection (canvas) rendering proceeds in the main thread as GLib idle callbacks at priority just below GTK redraw, in chunks sized to a 1/15 s target iteration interval; GEGL's compiled-in default evaluation thread count is 1, configurable to 64 (GIMP sets it from its own preference; that code was not read). Unit: s, count. Statistic: defaults. Scope: GIMP master / GEGL master 2026-09-13. T1, T2, T4–T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-08 MLT framework (Kdenlive engine) — consumer read-ahead thread, worker threads, `real_time`; Kdenlive manual

**Citation.** MLT at commit 64fa0287ed114bf3dac8ec8fd1e3d37164657c2d (github.com/mltframework/mlt master): `src/framework/mlt_consumer.c`. Kdenlive Manual 26.08, pages "Rendering" (https://docs.kdenlive.org/en/exporting/render.html) and "Environment" (https://docs.kdenlive.org/en/getting_started/configure_kdenlive/configuration_environment.html); KDE UserBase "Kdenlive/Manual/Settings Menu/Configure Kdenlive" (https://userbase.kde.org/Kdenlive/Manual/Settings_Menu/Configure_Kdenlive). All fetched 2026-09-13.

**Copy read.** `sources/S2-mlt/repo/src/framework/mlt_consumer.c` SHA-256 3856053eb4ba05294823bd64619be6e7d9c22ea89186f2bd851f7e1b8e9098f1; `sources/S2-kdenlive/render.html` 7fee4b7e12578aae17df634377da137e09b858268b077967c85b09d481a474eb; `sources/S2-kdenlive/configuration-environment.html` 4d17d13bb80de665deec1a527cc4bcc68c2a68f09225680a5825590faebffd77; `sources/S2-kdenlive/userbase-configure.html` a060da25d13abb0a25cff49ea51330567ecc1408c82fb622d41cff2d9c73f8dc.

**Passages.**

mlt_consumer.c:567–572:
> `// Set the real_time preference` / `priv->real_time = mlt_properties_get_int(properties, "real_time");` / `// For worker threads implementation, buffer must be at least # threads` / `if (abs(priv->real_time) > 1 && mlt_properties_get_int(properties, "buffer") <= abs(priv->real_time)) mlt_properties_set_int(properties, "_buffer", abs(priv->real_time) + 1);`

mlt_consumer.c:774–781: `/** The thread procedure for asynchronously pulling frames through the service network connected to a consumer. … */` / `static void *consumer_read_ahead_thread(void *arg)`

mlt_consumer.c:1060–1066: `/** The worker thread procedure for parallel processing frames. … */` / `static void *consumer_worker_thread(void *arg)`

mlt_consumer.c:1416–1432 (`worker_get_frame`): `/** Use multiple worker threads and a work queue. */` … `int threads = abs(priv->real_time);` … `// This is a heuristic to determine a suitable minimum buffer size for the number of threads.` / `int headroom = (priv->real_time < 0) ? threads : (2 + threads * threads);`

Kdenlive Manual 26.08, "Rendering" › Encoder: "If you have a CPU capable of multi-threading you can select the number of Encoding threads to be passed to melt [1]. For encoding with certain codecs (MPEG-2, MPEG-4, H.264, and VP8) Kdenlive can use more than one thread and thus make use of multiple cores."

Kdenlive Manual 26.08, "Environment": "Concurrent threads. Defines the number of threads to use for proxy clip generation and transcode jobs. Those jobs will run in the background. The value entered is passed to ffmpeg as the -threads parameter."

KDE UserBase, Configure Kdenlive: "Processing threads: This is experimental and was removed in ver 0.9.10. This number was passed to melts real_time consumer property. This parameter increases the number of threads the program uses for video decoding and processing (but not encoding which is controlled via Render>Encoder threads)."

**Coverage.** T3 — covers (source/manual): object = video-editor (Kdenlive/MLT) thread organisation; MLT consumers pull frames in a read-ahead thread and, when `|real_time| > 1`, in that many worker threads with a work queue; Kdenlive exposes encoder threads and background proxy/transcode threads. T5 — partial: the MLT consumer is the playback path of Kdenlive's monitor, but no default frame cadence or per-frame CPU is stated in the read passages (the `real_time` default value is not quoted because it is set per consumer and was not read). T1, T2, T4, T6, T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-09 PipeWire — default quantum/rate, `pw-top` semantics

**Citation.** PipeWire at commit 1cd56b0615bb8bd112d9a2865a41cfdf638692f6 (gitlab.freedesktop.org/pipewire/pipewire master, 2026-09-13): `src/daemon/pipewire.conf.in`, `doc/dox/config/pipewire.conf.5.md` (source of `pipewire.conf(5)`), `doc/dox/programs/pw-top.1.md` (source of `pw-top(1)`).

**Copy read.** `sources/S2-pipewire/repo/src/daemon/pipewire.conf.in` SHA-256 8bb0dda1eecefd05f7fb234811e560a5c0edd467db16c9cefdd780c63fab0369; `doc/dox/config/pipewire.conf.5.md` 4469e3a19bb84ec372bc613fec5eaf22aa0666604102d52671802bc42a6735e6; `doc/dox/programs/pw-top.1.md` 7b9ce3b1032ee9fadc8ce42aa09c7ec5ecdcc525a18752a96a10541d45cbbbc5.

**Passages.**

pipewire.conf.in:45–51 (commented defaults in the shipped config):
> `#default.clock.rate          = 48000` / `#default.clock.allowed-rates = [ 48000 ]` / `#default.clock.quantum       = 1024` / `#default.clock.min-quantum   = 32` / `#default.clock.max-quantum   = 2048` / `#default.clock.quantum-limit = 8192` / `#default.clock.quantum-floor = 4`

pipewire.conf.in:61–69: `context.properties.rules = [ { matches = [ { cpu.vm.name = !null } ] actions = { update-props = { # These overrides are only applied when running in a vm. default.clock.min-quantum = 1024 } } } ]`

pipewire.conf.in:22: `#clock.power-of-two-quantum = true`

pipewire.conf.5.md:246–250:
> @PAR@ pipewire.conf default.clock.rate = 48000
> The default clock rate determines the real time duration of the min/max/default quantums. You might want to change the quantums when you change the default clock rate to maintain the same duration for the quantums.

pipewire.conf.5.md:259–274: "default.clock.min-quantum = 32 — Default minimum quantum." / "default.clock.max-quantum = 8192 — Default maximum quantum." / "default.clock.quantum = 1024 — Default quantum used when no client specifies one." / "default.clock.quantum-limit = 8192 — Maximum quantum to reserve space for. This is the maximum buffer size used in the graph, regardless of the samplerate." / "default.clock.quantum-floor = 4 — Minimum quantum to reserve space for."

(Note the discrepancy inside the project's own files: the man page states max-quantum = 8192, the shipped `pipewire.conf.in` comments `max-quantum = 2048`. Both quoted; neither reconciled here.)

pw-top.1.md:14–16: "A hierarchical view is shown of Driver nodes and follower nodes. The Driver nodes are actively using a timer to schedule dataflow in the followers."

pw-top.1.md:43–48 (§ QUANT):
> The quantum by itself needs to be divided by the RATE column to calculate the duration of a scheduling period in fractions of a second.
> For a QUANT of 1024 and a RATE of 48000, the duration of one period in the graph is 1024/48000 or 21.3 milliseconds.

pw-top.1.md:54–56: "The driver will use the lowest quantum of any of the followers. If none of the followers select a quantum, the default quantum in the pipewire configuration file will be used."

pw-top.1.md:94–97 (§ WAIT): "For Driver nodes, this is the time between when the node wakes up to start processing the graph and when the driver (and thus also the graph) completes a cycle. The WAIT time for driver is thus the elapsed time processing the graph." :99–102: "For follower nodes, it is the time spent between being woken up (when all dependencies of the node are satisfied) and when processing starts. The WAIT time for follower nodes is thus mostly caused by context switching."

pw-top.1.md:110–111 (§ BUSY): "The processing time is started when the node starts processing until it completes and wakes up the next nodes in the graph."

**Coverage.** T4 — covers (documentation): object = PipeWire graph scheduling period; the server's own documentation states the default quantum 1024 samples at 48000 Hz = 21.3 ms per period when no client requests smaller; min 32 samples (0.67 ms at 48 kHz — derived by the reader, not stated), VM override min 1024; drivers wake on a timer; `pw-top` exposes per-node WAIT and BUSY per cycle (a way to observe per-wake processing time, but no values are documented). No per-wake CPU value or trace is given. Unit: samples, Hz, ms. Statistic: defaults. Scope: PipeWire master 2026-09-13. T1–T3, T5–T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-10 PulseAudio — fragment defaults, timer-based scheduling constants, real-time IO threads

**Citation.** PulseAudio at commit 77d25a1e613095bdf87a1d13b65e7c330565077a (gitlab.freedesktop.org/pulseaudio/pulseaudio master): `man/pulse-daemon.conf.5.xml.in` (source of `pulse-daemon.conf(5)`), `src/daemon/daemon-conf.c`, `src/modules/alsa/alsa-sink.c`, `src/modules/alsa/module-alsa-sink.c`.

**Copy read.** `sources/S2-pulseaudio/repo/man/pulse-daemon.conf.5.xml.in` SHA-256 aa19a6ca2208b427a57ae126beb272a88b0622122bd3d2682315957751328c45; `src/daemon/daemon-conf.c` 15ba21d02da74e1320b6db716378f62ce15445f9724c2f9f5f4af8cdd4a123c7; `src/modules/alsa/alsa-sink.c` 002c8f0a380fecb4643d763197cdb5d0e6c3720673b78270dd46b90ffb05f727; `src/modules/alsa/module-alsa-sink.c` dbf48b1028a773db9b85526766c02e9466ce4dcc0fbcb9e4cbea2570ff2af9dc.

**Passages.**

pulse-daemon.conf.5.xml.in:524–541 (§ Default Fragment Settings):
> Some hardware drivers require the hardware playback buffer to be subdivided into several fragments. It is possible to change these buffer metrics for machines with high scheduling latencies. Not all possible values that may be configured here are available in all hardware. The driver will find the nearest setting supported. Modern drivers that support timer-based scheduling ignore these options.
> default-fragments= The default number of fragments. Defaults to 4.
> default-fragment-size-msec= The duration of a single fragment. Defaults to 25ms (i.e. the total buffer is thus 100ms long).

daemon-conf.c:102–103: `.default_n_fragments = 4,` / `.default_fragment_size_msec = 25,`

pulse-daemon.conf.5.xml.in:287–297: "realtime-scheduling= Try to acquire SCHED_FIFO scheduling for the IO threads. […] Please note that only the IO threads of PulseAudio are made real-time. The controlling thread is left a normally scheduled thread. […] Takes a boolean argument, defaults to yes." :301–306: "realtime-priority= The realtime priority to acquire, if realtime-scheduling is enabled. […] Defaults to 5."

alsa-sink.c:71–72:
> `#define DEFAULT_TSCHED_BUFFER_USEC (2*PA_USEC_PER_SEC)             /* 2s    -- Overall buffer size */` / `#define DEFAULT_TSCHED_WATERMARK_USEC (20*PA_USEC_PER_MSEC)        /* 20ms  -- Fill up when only this much is left in the buffer */`

alsa-sink.c:74–75: `TSCHED_WATERMARK_INC_STEP_USEC (10*PA_USEC_PER_MSEC) /* 10ms -- On underrun, increase watermark by this */` / `TSCHED_WATERMARK_DEC_STEP_USEC (5*PA_USEC_PER_MSEC) /* 5ms -- When everything's great, decrease watermark by this */`

alsa-sink.c:83–84:
> `#define TSCHED_MIN_SLEEP_USEC (10*PA_USEC_PER_MSEC)                /* 10ms  -- Sleep at least 10ms on each iteration */` / `#define TSCHED_MIN_WAKEUP_USEC (4*PA_USEC_PER_MSEC)                /* 4ms   -- Wakeup at least this long before the buffer runs empty*/`

module-alsa-sink.c:51–53 (module usage string): `"tsched=<enable system timer based scheduling mode?> " "tsched_buffer_size=<buffer size when using timer based scheduling> " "tsched_buffer_watermark=<lower fill watermark> "`

**Coverage.** T4 — covers (documentation/source): object = PulseAudio ALSA sink wake cadence; in timer-based scheduling mode (the default for modern drivers per the man page) the sink sleeps at least 10 ms per iteration and wakes at least 4 ms before the 2 s hardware buffer would run empty relative to a 20 ms watermark, so the wake interval is adaptive rather than a fixed period; when fragments are used, 4 × 25 ms = 100 ms buffer. IO threads run SCHED_FIFO priority 5 by default. No per-wake CPU value. Unit: ms, s. Statistic: defaults. Scope: PulseAudio master 2026-09-13. T1–T3, T5–T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-11 ALSA (alsa-lib) — period concepts and period wakeups

**Citation.** alsa-lib at commit f84cd4ced7b36fddb8e4ee24404cf7c091d27020 (github.com/alsa-project/alsa-lib master): `src/pcm/pcm.c` (also the source of the "PCM (digital audio) interface" doxygen page at www.alsa-project.org/alsa-doc/alsa-lib/pcm.html).

**Copy read.** `sources/S2-alsa-lib/repo/src/pcm/pcm.c` SHA-256 530676d66aea3654b1f7b5e0be0b1183f24254d0dd8709ee4896c5c0a4c6c4cb.

**Passages.**

pcm.c:852 (doc of `snd_pcm_async`): "A signal is raised every period."

pcm.c:936–939 (doc of `snd_pcm_hw_params`): "The configuration is chosen fixing single parameters in this order: first access, first format, first subformat, min channels, min rate, min period time, max buffer size, min tick time."

pcm.c:2514: "The asynchronous callback is called when period boundary elapses."

pcm.c:2933–2934 (`snd_pcm_wait_nocheck`): `/* period size is the time boundary */` / `timeout = (pcm->period_size * 1000ULL) / pcm->rate;`

pcm.c:5050–5066 (doc of `snd_pcm_hw_params_set_period_wakeup`): "\brief Restrict a configuration space to settings without period wakeups … \param val 0 = disable, 1 = enable (default) period wakeup … To check whether the hardware does support disabling period wakeups, call #snd_pcm_hw_params_can_disable_period_wakeup(). If the hardware does not support this mode, standard period wakeups will be generated. Even with disabled period wakeups, the period size/time/count parameters are valid".

pcm.c:5207–5212: "\brief Restrict a configuration space to contain only one period time … \param val approximate period duration in us".

**Coverage.** T4 — covers (documentation): object = ALSA PCM period as the wake unit; the library documents that the hardware raises an interrupt/signal per period, that period wakeups are enabled by default and may be disabled where hardware supports it, and that period time is in microseconds. No default period value is stated (it is chosen per device/application). T1–T3, T5–T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-12 mpv — audio buffer, video sync modes, hardware decoding default, decoder threads, VO thread

**Citation.** mpv at commit 13a4bfbc1a184c0576ca69c2de486a972aeb2407 (github.com/mpv-player/mpv master, 2026-09-13): `DOCS/man/options.rst`, `DOCS/man/ao.rst`, `video/out/vo.c`.

**Copy read.** `sources/S2-mpv/repo/DOCS/man/options.rst` SHA-256 e78aabb4a03f4cc3dfcf3221cd499a792a5914fedc3f272b088d1023418084fd; `DOCS/man/ao.rst` c3416e6d5e12f592762810ee802269ea9af784618c9f8a171a0c5e41ea67318f; `video/out/vo.c` 8504b70c5ec07cb79f6fc4b5c7e332eb46376a97539feaaef2bfcd2e1adacbd1.

**Passages.**

options.rst:2452–2465 (`--audio-buffer=<seconds>`):
> Set the audio output minimum buffer. The audio device might actually create a larger buffer if it pleases. If the device creates a smaller buffer, additional audio is buffered in an additional software buffer. […] Default: 0.2 (200 ms).

ao.rst:212–216 (`--pipewire-buffer=<1-2000|native>`): "Set the audio buffer size in milliseconds. A higher value buffers more data, and has a lower probability of buffer underruns. A smaller value makes the audio stream react faster, e.g. to playback speed changes. "native" lets the sound server determine buffers." (Same wording for `--pulse-buffer` at ao.rst:189–193.)

options.rst:8162–8172 (`--video-sync=<audio|...>`):
> How the player synchronizes audio and video. If you use this option, you usually want to set it to ``display-resample`` to enable a timing mode that tries to not skip or repeat frames when for example playing 24fps video on a 24Hz screen.
> The modes starting with ``display-`` try to output video frames completely synchronously to the display, using the detected display vertical refresh rate as a hint how fast frames will be displayed on average. These modes change video speed slightly to match the display.

options.rst:8197–8202: ":audio: Time video frames to audio. This is the most robust mode, because the player doesn't have to assume anything about how the display behaves. The disadvantage is that it can lead to occasional frame drops or repeats. If audio is disabled, this uses the system clock. This is the default mode."

options.rst:8189–8191: "These modes also require a vsync blocked presentation mode. For OpenGL, this translates to ``--opengl-swapinterval=1``. For Vulkan, it translates to ``--vulkan-swap-mode=fifo`` (or ``fifo-relaxed``)."

options.rst:1326–1336 (`--hwdec`): "Hardware decoding is not enabled by default, to keep the out-of-the-box configuration as reliable as possible. However, when using modern hardware, hardware video decoding should work correctly, offering reduced CPU usage, and possibly lower power consumption. On older systems, it may be necessary to use hardware decoding due to insufficient CPU resources; and even on modern systems, sufficiently complex content (eg: 4K60 AV1) may require it."

options.rst:2019–2023 (`--vd-lavc-threads=<N>`): "Number of threads to use for decoding. Whether threading is actually supported depends on codec (default: 0). 0 means autodetect number of cores on the machine and use that, up to the maximum of 16."

options.rst:1316–1318 (`--display-fps-override=<fps>`): "Set the display FPS used with the ``--video-sync=display-*`` modes. By default, a detected value is used."

vo.c:1114–1120: `static MP_THREAD_VOID vo_thread(void *ptr)` … `mp_thread_set_name("vo");` (vo.c:751–752: "// Wakeup VO thread, and make it check for new events with VOCTRL_CHECK_EVENTS. // To be used by threaded VO backends.")

**Coverage.** T4 — covers (documentation): mpv's audio output keeps a 200 ms minimum buffer by default; buffer size for PulseAudio/PipeWire outputs is configurable in ms or left to the server. No wake period or CPU share stated. T5 — covers (documentation): object = mpv frame cadence driver; by default frames are timed to the audio clock (`--video-sync=audio`), optionally to the detected display refresh (`display-*` modes, requiring vsync-blocked presentation); software decoding is the default (`--hwdec` off) with up to 16 decoder threads autodetected from core count; video output runs in its own thread named "vo". No per-frame CPU measurement. T1–T3, T6, T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-13 GStreamer — audio sink buffer/latency defaults; base sink sync/QoS defaults

**Citation.** GStreamer monorepo at commit 4902f8122b10673f3fc1b70f7db2076464ce317c (gitlab.freedesktop.org/gstreamer/gstreamer main): `subprojects/gst-plugins-base/gst-libs/gst/audio/gstaudiobasesink.c`, `subprojects/gstreamer/libs/gst/base/gstbasesink.c`.

**Copy read.** `sources/S2-gstreamer/repo/subprojects/gst-plugins-base/gst-libs/gst/audio/gstaudiobasesink.c` SHA-256 fed32b304347841782073687305c63d81fd208509c4404dc870d25680656457b; `subprojects/gstreamer/libs/gst/base/gstbasesink.c` 43a7223ce9ab63dc0bae4868f0660d6bf3e4e3201cf883eaee21cac2addd14c7.

**Passages.**

gstaudiobasesink.c:87–89:
> `/* FIXME: 2.0, store the buffer_time and latency_time in nanoseconds */` / `#define DEFAULT_BUFFER_TIME     ((200 * GST_MSECOND) / GST_USECOND)` / `#define DEFAULT_LATENCY_TIME    ((10 * GST_MSECOND) / GST_USECOND)`

gstaudiobasesink.c:187–196: property "buffer-time": "Size of audio buffer in microseconds, this is the minimum latency that the sink reports" (default `DEFAULT_BUFFER_TIME`); property "latency-time": "The minimum amount of data to write in each iteration in microseconds" (default `DEFAULT_LATENCY_TIME`).

gstaudiobasesink.c:96–98: `/* when timestamps drift for more than 40ms we resync. This should be enough to compensate for timestamp rounding errors. */` / `#define DEFAULT_ALIGNMENT_THRESHOLD (40 * GST_MSECOND)`

gstbasesink.c:299–301: `#define DEFAULT_SYNC TRUE` / `#define DEFAULT_MAX_LATENESS -1` / `#define DEFAULT_QOS FALSE`; gstbasesink.c:458 property "sync": "Sync on the clock"; :467–469 property "qos": "Generate Quality-of-Service events upstream".

gstbasesink.c:65–69 (SECTION:gstbasesink doc comment): "When the element is set to PLAYING, #GstBaseSink will synchronise on the clock using the times returned from #GstBaseSinkClass::get_times. If this function returns %GST_CLOCK_TIME_NONE for the start time, no synchronisation will be done. Synchronisation can be disabled entirely by setting the object #GstBaseSink:sync property to %FALSE." :74–77: "Subclasses that synchronise on the clock in the #GstBaseSinkClass::render method are supported as well. […] A typical example is an audiosink."

**Coverage.** T4 — covers (source): GStreamer audio sinks default to a 200 ms ring buffer written in 10 ms segments ("latency-time"), i.e. the sink's write iteration cadence defaults to 10 ms; no CPU share stated. T5 — covers (source): sinks synchronise rendering to the pipeline clock by default (`sync=TRUE`), QoS events off by default; cadence is thus driven by buffer timestamps against the clock, not by display refresh. T1–T3, T6, T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-14 Wayland `wl_surface.frame` and X11 Present extension — what a frame callback means for an idle client

**Citation.** Wayland protocol `protocol/wayland.xml` at commit 381af21cf84f13be0ca24aed756a9cded3290d49 (gitlab.freedesktop.org/wayland/wayland main); xorgproto `presentproto.txt` (The Present Extension, Version 1.4, 2023-06-13, Keith Packard) at commit fcb7e9a1a0b593a44740d83b0babddd331fea830 (gitlab.freedesktop.org/xorg/proto/xorgproto master).

**Copy read.** `sources/S2-wayland/repo/protocol/wayland.xml` SHA-256 cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07; `sources/S2-presentproto/repo/presentproto.txt` fe0f731420b5458efc4339dbea782046f1ace6ea4bece8a6e4dde363c0bddf65.

**Passages.**

wayland.xml:1630–1638 (`wl_surface.frame`, request declared at 1628):
> Request a notification when it is a good time to start drawing a new frame, by creating a frame callback. This is useful for throttling redrawing operations, and driving animations.
> When a client is animating on a wl_surface, it can use the 'frame' request to get notified when it is a good time to draw and commit the next frame of animation. If the client commits an update earlier than that, it is likely that some updates will not make it to the display, and the client is wasting resources by drawing too often.

wayland.xml:1640–1643: "The frame request will take effect on the next wl_surface.commit. The notification will only be posted for one frame unless requested again."

wayland.xml:1645–1650: "The server must send the notifications so that a client will not send excessive updates, while still allowing the highest possible update rate for clients that wait for the reply before drawing again. The server should give some time for the client to draw and commit after sending the frame callback events to let it hit the next output refresh."

wayland.xml:1652–1654: "A server should avoid signaling the frame callbacks if the surface is not visible in any way, e.g. the surface is off-screen, or completely obscured by other opaque surfaces."

presentproto.txt:10–13: "The Present extension provides a way for applications to update their window contents from a pixmap in a well defined fashion, synchronizing with the display refresh and potentially using a more efficient mechanism than copying the contents of the source pixmap." :535–536 (PresentCompleteNotify): "'msc' and 'ust' indicate the frame count and system time when the presentation actually occurred."

**Coverage.** T3 and T5 — covers (protocol specification): object = compositor-driven wake semantics; a frame callback is one-shot and only requested by a client that intends to draw, so an idle client that does not commit receives no frame callbacks (no per-refresh wake); an animating client is throttled to the output refresh; X11 Present reports the refresh count (msc) at which presentation occurred. No numeric cadence is specified (it is the output's). T1, T2, T4, T6, T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-15 VLC — video output thread timing constants

**Citation.** VLC at commit 289a425a89e36f3af8dae040259bbe27dc801b15 (code.videolan.org/videolan/vlc master): `src/video_output/video_output.c`.

**Copy read.** `sources/S2-vlc/repo/src/video_output/video_output.c` SHA-256 c995848c2c772252c1f0375c14d86884d901f1c883557f397041a23a51e052f2.

**Passages.**

video_output.c:188–199:
> `/* Maximum delay between 2 displayed pictures. * XXX it is needed for now but should be removed in the long term. */` / `#define VOUT_REDISPLAY_DELAY VLC_TICK_FROM_MS(80)` / `/** * Late pictures having a delay higher than this value are thrashed. */` / `#define VOUT_DISPLAY_LATE_THRESHOLD VLC_TICK_FROM_MS(20)` / `/* Better be in advance when awakening than late... */` / `#define VOUT_MWAIT_TOLERANCE VLC_TICK_FROM_MS(4)`

video_output.c:1989–2000: `* Thread: video output thread … * Video output thread. This function does only returns when the thread is terminated. It handles the pictures arriving in the video heap and the display device events.` / `static void *Thread(void *object)` … `vlc_thread_set_name("vlc-vout");`

video_output.c:2393–2398: `/* The Render thread wait for a deadline that is either: * - VOUT_REDISPLAY_DELAY * - calculated from the clock * In case of a clock discontinuity, we need to wake up the Render thread, in order to trigger the rendering of the next picture, if new timings require it. */`

**Coverage.** T5 — covers (source): object = VLC video output cadence driver; a dedicated "vlc-vout" thread waits for a deadline computed from the playback clock (content timestamps) or at most 80 ms between displayed pictures, wakes up to 4 ms early, and discards pictures more than 20 ms late — i.e. cadence is content-clock driven, not display-refresh driven, with an 80 ms redisplay floor. No per-frame CPU. T1–T4, T6, T7 — does not cover.

**One observation?** No — not an observation.

---

### S2-16 WebRTC (libwebrtc) — default max frame rate, V4L2 capture thread, encoder queue, frame cadence adapter, threading model

**Citation.** WebRTC `src` at commit e42b7b0ed1123ed5051d4716e370bf0639c246f0 (webrtc.googlesource.com/src main, 2026-09-13): `media/base/media_constants.h`, `modules/video_capture/linux/video_capture_v4l2.cc`, `video/video_stream_encoder.h`, `video/frame_cadence_adapter.h`. WebRTC project page "Native APIs" § Threading Model, https://webrtc.github.io/webrtc-org/native-code/native-apis/ (fetched 2026-09-13).

**Copy read.** `sources/S2-webrtc-docs/media_constants.h` SHA-256 51c4095b83ad2102c76b4f2a0bd7e8b2cfd2d6dab8a5c70e0141adf863cacff5; `sources/S2-webrtc-docs/video-capture-linux` (= video_capture_v4l2.cc) 15a058342fdadddc3982704e86d7b475dc8298e555b1d69b9233c50e221c680e; `sources/S2-webrtc/video_stream_encoder.h` 399bcad135cbb14e0d211eae8cee6db4d70c53979255032b7fd1383a851fd586; `sources/S2-webrtc/frame_cadence_adapter.h` 7a1bc7edf602bdc9bd7c638434b9d90393b2508bcf6a3b82879a6109ea88a6f4; `sources/S2-webrtc-docs/native-code-threads.html` d960abe551524e2df15c9aab78e339af33d2330526fe4705c2f623aca9cf3e2f.

**Passages.**

media_constants.h:166: `inline constexpr int kDefaultVideoMaxFramerate = 60;`

video_capture_v4l2.cc:262–266: `// driver supports the feature. Set required framerate.` … `streamparms.parm.capture.timeperframe.numerator = 1;` / `streamparms.parm.capture.timeperframe.denominator = capability.maxFPS;`

video_capture_v4l2.cc:273–282: `// If driver doesn't support framerate control, need to hardcode. // Hardcoding the value based on the frame size.` / `if (!driver_framerate_support) { if (configured_capability_.width >= 800 && configured_capability_.videoType != VideoType::kMJPEG) { configured_capability_.maxFPS = 15; } else { configured_capability_.maxFPS = 30; } }`

video_capture_v4l2.cc:304–311: `// start capture thread;` … `_captureThread = PlatformThread::SpawnJoinable( [this] { while (CaptureProcess()) { } }, "CaptureThread", ThreadAttributes().SetPriority(ThreadPriority::kHigh));`

video_stream_encoder.h:99: constructor parameter `std::unique_ptr<TaskQueueBase, TaskQueueDeleter> encoder_queue,`; :153–154: `// be called on `encoder_queue_`.` / `TaskQueueBase* encoder_queue() { return encoder_queue_.get(); }`; :304: `TaskQueueBase* const worker_queue_;`; :334: `int max_framerate_ RTC_GUARDED_BY(encoder_queue_) = -1;`

frame_cadence_adapter.h:36–39: `// Averaging window spanning 90 frames at default 30fps, matching old media // optimization module defaults.` / `static constexpr int64_t kFrameRateAveragingWindowSizeMs = (1000 / 30) * 90;`; :40–44: `// In zero-hertz mode, the idle repeat rate is a compromise between // RTP receiver keyframe-requesting timeout (3s), other backend limitations // and some worst case RTT.` / `static constexpr TimeDelta kZeroHertzIdleRepeatRatePeriod = TimeDelta::Millis(1000);`; :98–100: "Returns the input framerate. This is measured by RateStatistics when zero-hertz mode is off, and returns the max framerate in zero-hertz mode."

Native APIs page, § Threading Model:
> WebRTC Native APIs use two globally available threads: the signaling thread and the worker thread. Depending on how the PeerConnection factory is created, the application can either provide those two threads or just let them be created internally. […] All callbacks will be made on the signaling thread. […] The worker thread is used to handle more resource-intensive processes, such as data streaming.

**Coverage.** T5 — covers (source/documentation): object = conferencing client capture/encode thread structure and cadence; on Linux, capture runs in a high-priority "CaptureThread" polling V4L2 at the requested `maxFPS` (fallback 30 fps, or 15 fps for ≥ 800 px non-MJPEG when the driver cannot set a rate); encoding runs on a dedicated encoder task queue; the frame cadence adapter assumes a "default 30fps" for its averaging window and, in zero-hertz (screen-share) mode, repeats idle frames every 1000 ms; the stack's default max frame rate constant is 60. Public API threading: signaling thread + worker thread. No per-frame CPU value. T1–T4, T6, T7 — does not cover. Decoder-thread organisation was not read.

**One observation?** No — not an observation.

---

### S2-17 Zoom desktop client — system requirements (Windows, macOS, Linux)

**Citation.** Zoom Support article "Zoom system requirements: Windows, macOS, Linux", https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060748. The live page returns a JavaScript shell without article text (row 59); the text below is from the Wayback Machine copy fetched via `https://web.archive.org/web/2026id_/<url>` (row 60), gzip-encoded body decoded locally; capture timestamp not present in the returned body.

**Copy read.** `sources/S2-zoom/sysreq-all.html` (live shell) SHA-256 5d0d2196d48a901ab1f74b41924771df327e67a5f217921085d7ebee16476abe; `sources/S2-zoom/sysreq-all-wayback.html` (gzip as served) 9c0a3c189bc86d3856f16c553407ca66eebd83921e3f01e59d3fa64a2b93879a; `sources/S2-zoom/sysreq-all-wayback.decoded.html` 81509b1f8dbddd0eabec145afd09f6b58d08e5111bfc29fc77ea5a35d146d154.

**Passages.** § Supported operating systems: "Linux: Ubuntu 20.04 or higher Mint 20 or higher Red Hat Enterprise Linux 9.0 or higher Oracle Linux 9.0 or higher CentOS 9 or higher Fedora 32 or higher OpenSUSE 16 or higher Debian 11 or higher ArchLinux (64-bit only) Other Linux OS with GCC 9.4 or higher". § Processor, RAM, and CPU bit requirements: "Processor — Minimum: Dual-core 2Ghz or higher — Recommended: Quad-core 2.5Ghz or higher; RAM 4 GB / 16 GB; CPU bit 32/64 / 64." Notes: "Dual and single-core laptops have a reduced frame rate when screen sharing (around 5 frames per second). For optimum screen-sharing performance on laptops, we recommend a quad-core processor or higher. Linux requires a processor or graphics card that can support OpenGL 2.0 or higher."

**Coverage.** T5 — covers only marginally (vendor documentation): the only cadence statement is "around 5 frames per second" screen-sharing on dual/single-core laptops; no thread model, capture/encode cadence or CPU share is documented. Records the absence of primary thread/cadence documentation for the Zoom Linux client. Other topics — does not cover.

**One observation?** No — not an observation.

---

### S2-18 Spotify for Linux — absence of technical documentation

**Citation.** Spotify, "Spotify for Linux" download page, https://www.spotify.com/us/download/linux/ (fetched 2026-09-13).

**Copy read.** `sources/S2-spotify/linux.html` SHA-256 81e8a31c256d74187624e3c859f0975ccd7a1140863396032a2704848b8008a5.

**Passage.** "Spotify for Linux is a labor of love from our engineers that wanted to listen to Spotify on their Linux development machines. They work on it in their spare time and it is currently not a platform that we actively support."

**Coverage.** T4 — records absence: the vendor page documents no thread model, buffer size or playback cadence for the Linux client. Other topics — does not cover.

**One observation?** No.

---

### S2-19 Zed — blog "Leveraging Rust and the GPU to render user interfaces at 120 FPS"

**Citation.** Antonio Scandurra, Zed's Blog, March 7th, 2023, https://zed.dev/blog/videogame (fetched 2026-09-13).

**Copy read.** `sources/S2-zed-docs/zed-blog-latency.html` SHA-256 8f5f16293e660f39cb2f6ea2b7efc332182fb5313f585418a8ff7562fcca34cf.

**Passage.** Opening paragraph: "A modern display's refresh rate ranges from 60 to 120 frames per second, which means an application only has 8.33ms per frame to push pixels to screen. This includes updating the application state, laying out UI elements, and finally writing data into the frame buffer. It's a tight deadline, and if you've ever built an application with Electron, it's a deadline that may feel impossible to consistently meet." Also: "One key observation about the problem is that text normally doesn't change much across frames. For example, editing a line of code doesn't affect the surrounding lines, so it would be unnecessarily expensive to shape those again."

**Coverage.** T2 — does not cover with a measurement: the post states the per-frame budget (8.33 ms at 120 Hz) and design choices; it reports no measured keystroke CPU or latency numbers. T3 — states the editor targets display-refresh-driven frames (120 fps). No numbers other than the budget. The Zed repository (commit 7960b2a7…) was grepped for latency benchmarks; nothing quotable found. Third-party review sites returned by WebSearch (row 82) claim 1–2 ms keystroke latency but are not primary and were not read.

**One observation?** No — not an observation.

---

### S2-20 Alacritty — CONTRIBUTING.md on latency measurement

**Citation.** Alacritty at commit d692748d3f61253ebe9f5094320120d22f6a046f (github.com/alacritty/alacritty master): `CONTRIBUTING.md`.

**Copy read.** `sources/S2-alacritty/repo/CONTRIBUTING.md` SHA-256 37ab3c68696ce0c3ab465044d0bb2c49722ee434ceeedd3543193808de50181d.

**Passage.** CONTRIBUTING.md:82–83: "Latency is another important factor for Alacritty. On X11, Windows, and macOS the [typometer](https://github.com/pavelfatin/typometer) tool allows measuring keyboard latency."

**Coverage.** T2 — does not cover with numbers: the project names its measurement tool (typometer: keystroke-to-screen latency, X11/Windows/macOS, i.e. not Wayland) but publishes no measured values in the repository. Third-party measurements (danluu.com, tomscii.sig7.se, lwn.net; row 85) are outside S2.

**One observation?** No.

---

## 3. Not found

**T1 Input inter-arrival.** No project or vendor documentation read publishes inter-key or pointer-event inter-arrival distributions. Searches establishing this: rows 25–35, 39–41, 44–49, 54–56, 62–67, 70–72, 81–82, 85 (Chromium, Gecko, LibreOffice, VS Code, Zed, Alacritty, xterm, GTK documentation). The only project-published input-timing constants are Qt's `KeyboardInputInterval` 400 ms, `KeyboardAutoRepeatRate` 30 and `MouseDoubleClickInterval` 400 ms defaults (qplatformtheme.cpp:615–620, S2-02), which are UI thresholds, not observed inter-arrival statistics. S1/S3 territory.

**T2 CPU per input.** No project documents a measured per-keystroke CPU-time distribution. Chromium's Rendering Benchmarks page (S2-03) defines `mean_input_event_latency` for touch scrolling and shows one unattributed example; Zed (S2-19) states a frame budget, not a measurement; Alacritty (S2-20) names a tool, no values; VS Code's Performance-Issues wiki (row 56) is troubleshooting guidance; Firefox performance docs index (row 64) has no keypress-to-paint numbers; neovim issue #2976 blocked (403, row 63). Searches: rows 25–35, 54–56, 62–66, 81–82, 85.

**T3 Wake structure.** Candidates S2-01 through S2-08 and S2-14 document *designs and defaults* (frame-clock/vsync-driven repaint, cursor-blink 1200/1000/500 ms, autosave 10 min, spell-check 100 ms, mail check 10, idle-render 1/15 s, thread organisation). **Not found in S2:** any project-published per-schedule runtime or wake-gap distribution from a scheduler trace of a GUI application; Kdenlive's monitor-playback thread documentation (docs.kdenlive.org playback page 404, row 77; the rendering/environment pages cover encoder and proxy threads only); a Monaco/VS Code documentation page stating the `cursorBlinking` default (rows 54, 69 dead ends — default taken from source instead).

**T4 Audio cadence.** Candidates S2-09 through S2-13 document defaults (PipeWire 1024/48000 = 21.3 ms per period; PulseAudio tsched min sleep 10 ms / wakeup 4 ms before empty / 2 s buffer, fragments 4 × 25 ms; GStreamer 10 ms write iteration / 200 ms buffer; mpv 200 ms minimum buffer; ALSA period wakeups). **Not found in S2:** any documented per-wake CPU or CPU-share figure for an audio path; PipeWire wiki pages (Config-PipeWire, Performance-tuning, FAQ "buffering explained") — Anubis challenge (row 51); PulseAudio freedesktop wiki latency pages — 418 (row 52); Spotify Linux client internals — absent (S2-18).

**T5 Video/conferencing cadence.** Candidates S2-12 (mpv), S2-13 (GStreamer), S2-15 (VLC), S2-16 (WebRTC), S2-14 (protocols), S2-17 (Zoom) document what drives cadence (audio clock by default in mpv, pipeline clock in GStreamer/VLC with an 80 ms redisplay floor in VLC, V4L2 capture rate 30/15 fallback and encoder queue in WebRTC). **Not found in S2:** any documented per-frame CPU or CPU share per frame period; WebRTC decoder-thread organisation (not read); Jitsi Meet developer handbook page (404, row 68); GStreamer QoS design document (Anubis, row 74); Zoom client thread/cadence documentation (does not exist on the vendor pages read; only system requirements, S2-17).

**T6 Application classes.** Out of S2 scope by class definition; no project documentation read compares editor, office, mail, browser, image and video editors' input or wake behaviour. The defaults collected across S2-01–S2-08 differ per application (e.g. cursor blink 1200 ms GTK vs 1000 ms Qt vs 500 ms VS Code; autosave 10 min LibreOffice; mail check 10 Thunderbird; GIMP idle render 1/15 s), which is design evidence, not observation.

**T7 CI observability.** Out of S2 scope (S4). Nothing searched.
