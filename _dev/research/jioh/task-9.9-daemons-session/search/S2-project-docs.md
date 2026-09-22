# S2 — primary project and vendor documentation and source code (T1, T2, T4)

Reader S2 · slice 9.9 "Daemons and session processes" · written 2026-09-20 · all copies accessed 2026-09-20 from this environment (outbound HTTPS through the session proxy, TLS verified).

Method. Every source-code read is pinned to a commit: each upstream repository was shallow-cloned (`git clone --depth 1`) and its `HEAD` recorded with `git rev-parse HEAD` and `git log -1 --format=%cI`; the cited files were copied unchanged into `sources/S2-NN/<path as in the repository>` and hashed with `sha256sum`. Locators are `file:line` at that commit (line numbers as `cat -n` prints them in the saved copy). Passages are verbatim, including XML/roff markup where the file is a man-page source. Per the class rule: an interval, timeout, period or default stated by documentation or source is recorded as a **mechanism**; a nice level, scheduling policy, rlimit or cgroup weight as a **treatment fact**; nothing in this class is an observation. Sources are read independently of the repository's description of them; only `input.md` and this reader's own output folder were opened. Local paths below are for the record only — the quoted passages and the copy identification (URL/commit, version, SHA-256) are meant to be sufficient on their own.

Candidate ids S2-01 … S2-28; S2-11 is unassigned (the polkit clone yielded no quotable passage on the topics — see search log rows 20 and 74).

## 1. Search log

All rows dated 2026-09-20. "Venue" is the network venue (git remote, raw URL) or, for `grep`, the local shallow clone named in the same row. HTTP status is given for every URL fetch; git operations report the transport result.

| # | Venue | Exact query / URL | Hits followed | Dead ends (status) |
|---|---|---|---|---|
| 1 | git ls-remote + clone --depth 1 | https://github.com/systemd/systemd | HEAD e96ff3b5b92dc06ed6f623eaa0c44e97e1650dbb (2026-09-19) → S2-01 | — |
| 2 | git clone --depth 1 | https://gitlab.com/chrony/chrony.git | HEAD 8df4f1263e206585e6c4e61352d042c2dd12916a → S2-02 | — |
| 3 | git clone --depth 1 | https://github.com/cronie-crond/cronie | HEAD cede1d68645ef8d36dd9ce76e9baa1a71e3b4f35 → S2-03 | — |
| 4 | git clone --depth 1 | https://gitlab.freedesktop.org/dbus/dbus.git | HEAD b01f2e2c18cf4f10f2f2287f775134a2dc9182d1 → S2-04 | — |
| 5 | git clone --depth 1 | https://github.com/bus1/dbus-broker | HEAD 2956b5d381deeea709c53d02f10e799e50e44f4b → S2-05 | — |
| 6 | git clone --depth 1 | https://github.com/PackageKit/PackageKit | HEAD dc3604a0c07bc02e70e20edd57dd7cfb3a5c4b46 → S2-06 | — |
| 7 | git clone --depth 1 | https://github.com/opensvc/multipath-tools | HEAD d53932bdbee02f440518ea384e63d7c4d3f66685 → S2-07 | — |
| 8 | git clone --depth 1 | https://github.com/storaged-project/udisks | HEAD c731cee133bb3240a0b91b59f9995a42aafb0ac4 → S2-08 | — |
| 9 | git clone --depth 1 | https://github.com/rsyslog/rsyslog | HEAD c5cafe3e85679be9e6c3434c9ac23399eab32b9d → S2-09 | — |
| 10 | git clone --depth 1 | https://gitlab.freedesktop.org/NetworkManager/NetworkManager.git | HEAD 58864ef92d3241787c311fad9a16a28524b206e1 → S2-10 | — |
| 11 | git clone --depth 1 | https://gitlab.gnome.org/GNOME/mutter.git | HEAD 888a7b7dac0c58612007c46bbad75de9f9437f48 → S2-12 | — |
| 12 | git clone --depth 1 | https://gitlab.gnome.org/GNOME/gnome-shell.git | HEAD f8a5dc649022f94c63d0ee18daa8bf4f0e76f979 → S2-13 | — |
| 13 | git clone --depth 1 | https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas.git | HEAD 4dc6fa0a3526f8b4044962b8b3a3fb8b975a355c → S2-14 | — |
| 14 | git clone --depth 1 | https://invent.kde.org/plasma/kwin.git | HEAD b8ef79a70431550832671daa28f1a3201aeca575 → S2-15 | — |
| 15 | git clone --depth 1 | https://gitlab.freedesktop.org/xorg/xserver.git | HEAD 306071c0b9683ef0dfadcfc2dbb78d369680542b → S2-16 | — |
| 16 | git clone --depth 1 | https://gitlab.freedesktop.org/xorg/driver/xf86-video-dummy.git | HEAD 533b5313d658422039716f97d59a3eff281401fc → S2-17 | no man page in the tree (`ls man` → no such directory) |
| 17 | git clone --depth 1 | https://gitlab.freedesktop.org/pipewire/pipewire.git | HEAD decc0d2efa2db7476faaa70043774b722317da78 → S2-18 | — |
| 18 | git clone --depth 1 | https://gitlab.freedesktop.org/pipewire/wireplumber.git | HEAD 20704c4d0d909e8b1604f333129a7c3b90dfb764 → S2-19 | — |
| 19 | git clone --depth 1 | https://gitlab.freedesktop.org/pulseaudio/pulseaudio.git | HEAD 77d25a1e613095bdf87a1d13b65e7c330565077a → S2-20 | — |
| 20 | git clone --depth 1 | https://gitlab.freedesktop.org/polkit/polkit.git | HEAD 213680d1f122f35c9e454702e697cf7818d0b2b1 (2024-01-18); grep of src/polkitbackend for `timeout|idle|g_timeout` → no hit | no quotable passage on idle behaviour; not a candidate |
| 21 | git clone --depth 1 | https://github.com/heftig/rtkit | HEAD c295fa849f52b487be6433e69e08b46251950399 (2020-04-05, version 0.13) — read, then superseded by row 22 | — |
| 22 | git ls-remote --tags + clone --depth 1 --branch v0.14 | https://gitlab.freedesktop.org/pipewire/rtkit.git (URL taken from Fedora's rtkit.spec, row 34) | tag v0.14 = c52db0a9849908613ab8775b519834671b7bec8b (2025-12-10) → S2-21 | — |
| 23 | git clone --depth 1 | https://gitlab.freedesktop.org/wayland/weston.git | HEAD 46298ecc7e7ca393567d431a562ba1ce3eeed04b → S2-22 | — |
| 24 | git clone --depth 1 | https://gitlab.freedesktop.org/wlroots/wlroots.git | HEAD aef1af2718687cba2acc87d932592409776656f5 → S2-25 | — |
| 25 | git clone --depth 1 | https://github.com/CachyOS/ananicy-rules | HEAD 03ef03fbf7e834385377432ccecaedd32e3414bb (2026-09-08) → S2-26 | — |
| 26 | git clone --depth 1 | https://gitlab.gnome.org/GNOME/gnome-session.git | HEAD aed00cf18229a98231c23e14f5798ddb918c4956; grep `Slice=|app.slice|session.slice` → only `data/gnome-session-restart-dbus.service.in:11:Slice=-.slice` and a NEWS line | no treatment or interval passage; not a candidate |
| 27 | curl -sSL | https://blog.vladzahorodnii.com/2020/12/10/compositing-scheduling-in-kwin-past-now-and-future/ | HTTP 200 → S2-23 | — |
| 28 | curl -sSL | https://blogs.gnome.org/shell-dev/2020/07/02/splitting-up-the-frame-clock/ | HTTP 200 → S2-24 | — |
| 29 | curl -sSL | https://src.fedoraproject.org/rpms/pipewire/raw/rawhide/f/pipewire.spec | HTTP 200 → S2-27 | — |
| 30 | curl -sSL | https://src.fedoraproject.org/rpms/systemd/raw/rawhide/f/systemd.spec | HTTP 200 → S2-27 | — |
| 31 | curl -sSL | https://src.fedoraproject.org/rpms/gnome-shell/raw/rawhide/f/gnome-shell.spec | HTTP 200 → S2-27 (no slice/nice/CPUWeight lines) | — |
| 32 | curl -sSL | https://src.fedoraproject.org/rpms/rtkit/raw/rawhide/f/rtkit-daemon.service | — | HTTP 404 |
| 33 | curl -sSL | https://salsa.debian.org/utopia-team/rtkit/-/raw/debian/master/debian/patches/series | — | HTTP 200 but body is the GitLab "Sign in" HTML page (15361 bytes), i.e. not served; treated as dead end |
| 34 | curl -sSL | https://src.fedoraproject.org/rpms/rtkit/raw/rawhide/f/rtkit.spec | HTTP 200 → S2-27 | — |
| 35 | curl -sSL | https://salsa.debian.org/systemd-team/systemd/-/raw/debian/master/debian/rules | HTTP 200 → S2-28; grep `watchdog|Dservice` → no hit | — |
| 36 | curl -sSL | https://git.launchpad.net/ubuntu/+source/gnome-shell/plain/debian/rules | HTTP 200 → S2-28 | — |
| 37 | curl -sSL | https://salsa.debian.org/gnome-team/gnome-shell/-/raw/ubuntu/master/debian/rules | HTTP 200 (900 bytes; not used further) | — |
| 38 | curl -sS | https://git.launchpad.net/ubuntu/+source/gnome-shell/tree/debian | HTTP 200 → S2-28 (file listing; no unit or slice override files) | — |
| 39 | curl -sSL | https://gitlab.gnome.org/GNOME/glib/-/raw/main/gio/gdesktopappinfo.c (HEAD b6d9457b458126336d3707d4b4ad3e831933d127) | HTTP 200, 163369 bytes; grep `app.slice|app-glib|StartTransientUnit|Slice|systemd` → no hit | no passage on app scopes in this file; not a candidate |
| 40 | grep, systemd clone | `WatchdogSec` in man/systemd.service.xml; `RuntimeWatchdogSec` in man/systemd-system.conf.xml | S2-01 passages | — |
| 41 | grep, systemd clone | `SyncIntervalSec|RateLimitIntervalSec|RateLimitBurst` in man/journald.conf.xml; `DEFAULT_SYNC_INTERVAL_USEC|DEFAULT_RATE_LIMIT` in src/journal | S2-01 | — |
| 42 | grep, systemd clone | `IdleAction` in man/logind.conf.xml; `idle_action|idle` in src/login/logind.c | S2-01 | — |
| 43 | grep, systemd clone | `PollIntervalM` in man/timesyncd.conf.xml | S2-01 | — |
| 44 | grep, systemd clone | `SwapUsedLimit|interval` in man/oomd.conf.xml; `SWAP_INTERVAL_USEC|MEM_PRESSURE_INTERVAL_USEC` in src/oom | S2-01 | — |
| 45 | grep, systemd clone | `WatchdogSec|^Nice=|CPUWeight|OOMScoreAdjust|IOSchedulingClass|CPUSchedulingPolicy` in units/; `-i watchdog` in units/*.in; `service-watchdog|SERVICE_WATCHDOG` in meson.build meson_options.txt | S2-01 | no unit sets `Nice=`, `CPUWeight=` (other than the three user slices) or `CPUSchedulingPolicy=` |
| 46 | grep, systemd clone | `half|interval` in man/sd_event_set_watchdog.xml; `watchdog_ping|watchdog_runtime_wait` in src/core/manager.c src/shared/watchdog.c | S2-01 | — |
| 47 | grep, systemd clone | `idle|WORKER_` in src/udev/udev-manager.c; `event_timeout|exec_delay|children_max` in man/udev.conf.xml | S2-01 (worker cleanup timer) | udev man pages give no idle interval |
| 48 | grep, systemd clone | `-i cache` in man/resolved.conf.xml man/systemd-resolved.service.xml; `CACHE_TTL_MAX` in src/resolve/resolved-dns-cache.c | S2-01 | man pages state no cache TTL number |
| 49 | grep, systemd clone | `user.slice|session.slice|app.slice|background.slice` in man/systemd.special.xml; `slice|CPUWeight` in docs/DESKTOP_ENVIRONMENTS.md | S2-01 | — |
| 50 | grep, chrony clone | `minpoll|maxpoll` in doc/chrony.conf.adoc; `SRC_DEFAULT_MINPOLL|SRC_DEFAULT_MAXPOLL` in *.h *.c | S2-02 | — |
| 51 | grep, cronie clone | `cron_sleep|sleep(|inotify|load_database|SECONDS` in src/cron.c | S2-03 | — |
| 52 | grep, dbus clone | `reply_timeout|service_start_timeout|auth_timeout|idle|thread` in doc/dbus-daemon.1.xml.in; `limit name` in bus/system.conf.in bus/session.conf.in; `reply_timeout|auth_timeout` in bus/config-parser.c; `OOMScoreAdjust|Nice=|CPU` in bus/*.service.in | S2-04 | dbus-daemon(1) states no idle timer or thread structure |
| 53 | grep, dbus-broker clone | `-i idle|timeout|thread` in docs/dbus-broker.rst; treatment keys in src/units | S2-05 | — |
| 54 | grep, PackageKit clone | `timeout|exit_idle|idle` in src/pk-main.c; `ShutdownTimeout` in data/config/PackageKit.conf | S2-06 | — |
| 55 | grep, multipath-tools clone | `DEFAULT_CHECKINT|DEFAULT_MAX_CHECKINT` in libmultipath/defaults.h; `polling_interval` in multipath/multipath.conf.5.in; `pthread_create|checkerloop` in multipathd/main.c; multipathd/multipathd.service.in | S2-07 | — |
| 56 | grep, udisks clone | `g_timeout_add_seconds|g_timeout_add` in src/*.c | S2-08 | — |
| 57 | grep, rsyslog clone | `MainMsgQueue|wrkrThrds|DFLT_MAINQ` in runtime/queue.h runtime/rsconf.c | S2-09 | — |
| 58 | grep, NetworkManager clone | `-i interval|connectivity` in man/NetworkManager.conf.xml; treatment keys in data/*.service.in | S2-10 | no unit-file treatment lines |
| 59 | grep, mutter clone | `CLUTTER_FRAME_CLOCK_STATE_|inhibit` in clutter/clutter/clutter-frame-clock.c; `MUTTER_DEBUG_DUMMY_MODE_SPECS` over the tree; `"headless"` in src/core/meta-context-main.c; `MUTTER_DEBUG_KMS_THREAD_TYPE|MUTTER_DEBUG_KMS_SCHEDULING_PRIORITY` in src/backends/native/meta-kms.c; `rtkit|RealtimeKit|SCHED_RR` in src/backends/native/meta-thread.c | S2-12 | `MUTTER_DEBUG_DUMMY_MODE_SPECS` occurs only in .gitlab-ci.yml, not in src/ |
| 60 | grep, gnome-shell clone | `idle-delay|STANDARD_FADE_TIME` in js/ui/screenShield.js; `Slice=|OOMScoreAdjust` in data/*.service.in; `app.slice|StartTransientUnit|systemd` in src/shell-app.c js/ | S2-13 | no app.slice mechanism in gnome-shell itself |
| 61 | grep, gsettings-desktop-schemas clone | `idle-delay` in schemas/org.gnome.desktop.session.gschema.xml.in | S2-14 | — |
| 62 | grep, kwin clone | `inhibit|scheduleRepaint|compositeTimer|safetyMargin|maxPendingFrameCount|refreshRate|s_delayVrrTimer` in src/core/renderloop.cpp src/core/renderloop_p.h; `rtkit|SCHED_RR|sched_setscheduler` in src/; `CAP_SYS_NICE|gainRealTime` in src/main_wayland.cpp src/CMakeLists.txt CMakeLists.txt; plasma-kwin_wayland.service.in | S2-15 | kwin does not use rtkit (no hit) |
| 63 | grep, xserver clone | `WaitForSomething|timeout|ScreenSaverTime` in os/WaitFor.c; `defaultScreenSaverTime` in dix/globals.c; `SMART_SCHEDULE_DEFAULT_INTERVAL` in dix/dispatch.c; `BlankTime|StandbyTime` in hw/xfree86/man/xorg.conf.man; `\-s ` in man/Xserver.man; hw/vfb/man/Xvfb.man; `frame_callback` in hw/xwayland/xwayland-window.c | S2-16 | — |
| 64 | grep, xf86-video-dummy clone | `videoRam|SaveScreen|Timer` in src/dummy_driver.c; README.md | S2-17 | — |
| 65 | grep, pipewire clone | `default.clock|rt.prio|nice.level|suspend-on-idle|module-rt|rtkit` in src/daemon/pipewire.conf.in src/daemon/minimal.conf.in; `DEFAULT_RT_PRIO|DEFAULT_NICE_LEVEL|rt.prio` in src/modules/module-rt.c; `rtprio-server|rtprio-client|rlimits-` in meson_options.txt; `do_start|do_stop|set_timers|freewheel` in spa/plugins/support/node-driver.c; `node.suspend-on-idle` in src/pipewire/keys.h; `Slice=` in src/daemon/systemd/user/*.service.in; `find -name '*rlimits*'` | S2-18 | — |
| 66 | grep, wireplumber clone | `session.suspend-timeout-seconds|suspend-timeout` in src/ modules/ | S2-19 | — |
| 67 | grep, pulseaudio clone | `timeout` in src/modules/module-suspend-on-idle.c; `suspend-on-idle` in src/daemon/default.pa.in; `high-priority|nice-level|realtime` in src/daemon/daemon.conf.in src/daemon/daemon-conf.c; `Slice=` in src/daemon/systemd/user/pulseaudio.service.in | S2-20 | — |
| 68 | grep, rtkit (fdo v0.14) clone | `our_realtime_priority|our_nice_level|max_realtime_priority|min_nice_level|rttime_usec_max|users_max|processes_per_user_max|threads_per_user_max|actions_burst_sec|actions_per_burst_max|canary_cheep_msec|canary_watchdog_msec|canary_watchdog_realtime_priority|canary_refusal_sec|sched_policy` in rtkit-daemon.c; rtkit-daemon.service.in | S2-21 | — |
| 69 | grep, weston clone | `repaint_msec|REPAINT_|DEFAULT_REPAINT_WINDOW|idle_time` in libweston/compositor.c frontend/main.c; `idle-time` in man/weston.ini.man | S2-22 | — |
| 70 | grep, wlroots clone | `schedule_frame|frame_pending|idle_frame|needs_frame` in types/output/output.c | S2-25 | — |
| 71 | grep, ananicy-rules clone | names `gnome-shell|mutter|kwin_wayland|kwin_x11|plasmashell|systemd|dbus-daemon|dbus-broker|cron|chronyd|NetworkManager|polkitd|udisksd|packagekitd|rsyslogd|multipathd|sway|Xwayland|Xorg` over 00-default/; 00-types.types; ananicy.conf; 00-cgroups.cgroups | S2-26 | no rule for `mutter`, `systemd*`, `cron`/`crond`, `polkitd`, `packagekitd`, `rsyslogd`, `multipathd` (grep hits for "cron" are game names only) |
| 72 | grep, Fedora specs (S2-27) | `Dservice-watchdog|watchdog|CPUWeight|Nice` in systemd.spec; `rtprio|rtkit|limits` in pipewire.spec; `Patch|service` in rtkit.spec; `slice|Slice|CPUWeight|nice` in gnome-shell.spec | S2-27 | gnome-shell.spec: no hit |
| 73 | grep, Debian/Ubuntu files (S2-28) | `watchdog|Dservice` in debian-systemd-rules; `debian/[A-Za-z0-9_.@-]*` over the launchpad tree listing | S2-28 | no unit/slice override in Ubuntu's gnome-shell debian/ listing |
| 74 | grep, polkit clone | `-i timeout|idle|g_timeout` in src/polkitbackend/polkitbackendauthority.c src/polkitbackend/polkitd.c | — | no hit (see row 20) |

Not attempted (outside this class or judged unnecessary after the primary sources were read): wiki.archlinux.org, man7.org mirrors of the same man pages (the upstream XML sources were read instead), packages.debian.org / packages.ubuntu.com (previous readers report resets), LWN articles.

## 2. Candidates

Common fields: "copy read" gives repository URL, commit, version string as the tree states it, access date 2026-09-20, local path `sources/S2-NN/…`, SHA-256 per file. "One observation?" is answered per the class rule: source and documentation are mechanisms or treatment facts, not observations, so no machine, subject or window is named unless stated.

### S2-01 — systemd (man-page sources, units, source)

**Citation.** systemd project, *systemd* source tree, version `262~rc3` (meson.version), commit e96ff3b5b92dc06ed6f623eaa0c44e97e1650dbb (2026-09-19T05:16:58+09:00), https://github.com/systemd/systemd. Man-page sources under `man/` are the sources of systemd.service(5), systemd-system.conf(5), journald.conf(5), logind.conf(5), timesyncd.conf(5), oomd.conf(5), sd_event_set_watchdog(3), systemd.special(7).

**Copy read.** clone of the commit above; local `sources/S2-01/`; SHA-256:
- `meson.version` 6851cc8be183557e1e5a3417d2deacf28180f8c01b07bedc3eeccdd2664ace89 (content: `262~rc3`)
- `meson_options.txt` 3fc0cb52e97bbbc283849bb410720c0cc3d51413247f8922cb86676cd7501012
- `meson.build` 34abd1e8b703835f289bda28d2a4f060f93732185b910cfd89e588d9f363a927
- `man/systemd.service.xml` 12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44
- `man/systemd-system.conf.xml` 161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58
- `man/journald.conf.xml` ed71e38df308227a94aca77b0840742b2c6ec49c1e43c2376d4aa135908f87f2
- `man/logind.conf.xml` 0590e460b7b8f4fdc4a8a7fd246d72f008dc0eca092f06364a51f7c55e8449ff
- `man/timesyncd.conf.xml` 3d3ea9b1c3e994e1af229b10389db8cd0789e590c040b1e4031685dc9f3fde31
- `man/oomd.conf.xml` 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617
- `man/sd_event_set_watchdog.xml` ab86d9d2ca6df9b6b5470e3aec2caf14d42f1e0d35e8b753ae1d0512a05d33d8
- `man/systemd.special.xml` 2b073d486d3cb143151d1947c3b5af7aa40789efc1d2380ef76149ce6bc425fd
- `src/oom/oomd-manager.h` 577eb8b46eab96395f61c9eeb90d34e4d8d9194826b79af19eb80a93feaa2f4b
- `src/journal/journald-config.c` 99f3e972cc639985ff60f637a505938a65b164e9510fdcc30b15d9634bf81a9d
- `src/udev/udev-manager.c` 9cf3c7669760691dedfc10ea27c4dc5a29da7d878f139abb432d07bb844a5ebf
- `src/login/logind.c` bfff7354e32f7f800cf9a96c72d9e08a3f113962f71f265be04cb2f81cb0a818
- `src/core/manager.c` c1ee521b27c48350bc48dded702b68f93ec09dbcf968a0367da7f0a76d497b1f
- `src/shared/watchdog.c` 763089ce56d6b02e24af7b7d3bd33eac1b247b042deba37312ce1f948e61cd0a
- `src/resolve/resolved-dns-cache.c` 361b759d9dd04606cc8cffae6b5978e745c1c65c6b9044cbe4b9a4d5026286f9
- `units/systemd-journald.service.in` 3c60e091124a289d8cac891d4c6e66b56db9b7d047ae96b185711e03bfea1fad
- `units/systemd-logind.service.in` feaa7aecdf5e3da28c3214417c69e7d966e672135a1711f5ed47ab10218dbba0
- `units/systemd-udevd.service.in` 22f77e0c964d0f11ff28b9423b94172e9be4625c249c3cea6319fe83f756e672
- `units/systemd-oomd.service.in` 2f4c2862b5826e85d63d5c7993f8610556f2f201facc0b20af04c1b972f288d3
- `units/systemd-tmpfiles-clean.service` 91c07d7c7e13eae3dfe5c475eea3df4dc12f93d00b3b6c0b4e6f3f50e8f6cccf
- `units/user/app.slice` 2f692ece5b1dd36e8a09cb2cca022ce68cca75bda22a1503c2e98ebd6584001e
- `units/user/session.slice` bdc0526c3ea8634e7a22410ba70a7f4a9dc51a41a8bb7ed943c9bedd3c7069ae
- `units/user/background.slice` 64352a7d8e99827974ac7c51fb1672cfa00b90a0498e49bcf8db212efa2e861e
- `docs/DESKTOP_ENVIRONMENTS.md` 6c5117d959a566b212d1cb79e1ff8c4f736ddbef61d6ff199148ed2688f6f969

**Passages (verbatim).**

Service watchdog (mechanism) — `man/systemd.service.xml:842-848,865-866`:
> `<term><varname>WatchdogSec=</varname></term>` / `<listitem><para>Configures the watchdog timeout for a service.` / `The watchdog is activated when the start-up is completed. The` / `service must call` / `<citerefentry><refentrytitle>sd_notify</refentrytitle><manvolnum>3</manvolnum></citerefentry>` / `regularly with <literal>WATCHDOG=1</literal> (i.e. the` / `"keep-alive ping"). If the time between two such calls is` … `Defaults to 0, which disables this feature. The service can` / `check whether the service manager expects watchdog keep-alive`

Keep-alive cadence in sd-event (mechanism) — `man/sd_event_set_watchdog.xml:60-62`:
> `the protocol used. The wake-up interval is chosen as half the` / `watchdog timeout declared by the service manager via the` / `<varname>$WATCHDOG_USEC</varname> environment variable. If the`

Which systemd daemons carry the watchdog and its build-time default (mechanism) — `meson_options.txt:370-371`:
> `option('service-watchdog', type : 'string', value : '3min',` / `       description : 'default watchdog setting for systemd services')`

`meson.build:993-995`:
> `service_watchdog = get_option('service-watchdog')` / `watchdog_value = service_watchdog == '' ? '' : 'WatchdogSec=' + service_watchdog` / `conf.set_quoted('SERVICE_WATCHDOG', watchdog_value)`

`units/systemd-journald.service.in:62` and `units/systemd-logind.service.in:64` each read `{{SERVICE_WATCHDOG}}` (the template placeholder; the same placeholder is present in units/systemd-resolved.service.in:56, units/systemd-networkd.service.in:55, units/systemd-oomd.service.in:58, units/systemd-udevd is *not* in that list — grep of `units/*.in` for `-i watchdog`, search-log row 45). Reader's reading: with the upstream default the listed services get `WatchdogSec=3min` and, through sd-event, ping every 90 s; Fedora builds with `-Dservice-watchdog=` (empty), see S2-27.

pid 1 and the hardware watchdog (mechanism) — `man/systemd-system.conf.xml:379-384,399-400`:
> `<para>If <varname>RuntimeWatchdogSec=</varname> is set to a non-zero value, the watchdog hardware` / `(<filename>/dev/watchdog0</filename> or the path specified with <varname>WatchdogDevice=</varname> or` / `the kernel option <varname>systemd.watchdog_device=</varname>) will be programmed to automatically` / `reboot the system if it is not contacted within the specified timeout interval. The system manager` / `will ensure to contact it at least once in half the specified timeout interval. This feature requires` / `a hardware watchdog device to be present, as it is commonly the case in embedded and server` … `shutdown.target</filename> unit. By default, <varname>RuntimeWatchdogSec=</varname> defaults` / `to 0 (off), and <varname>RebootWatchdogSec=</varname> to 10min.</para>`

`src/core/manager.c:3642` (inside the `while (m->objective == MANAGER_OK)` loop of `manager_loop`): `                (void) watchdog_ping();` — `src/shared/watchdog.c:547-550`:
> `        /* Ping approximately watchdog_timeout/4 after a successful ping, or even less than that` / `         * after an unsuccessful ping. */` / `        if (watchdog_runtime_wait(/* divisor= */ 4) > 0)` / `                return 0;`

journald (mechanism) — `man/journald.conf.xml:366-374`:
> `<term><varname>SyncIntervalSec=</varname></term>` / (blank) / `<listitem><para>The timeout before synchronizing journal files` / `to disk. After syncing, journal files are placed in the` / `OFFLINE state. Note that syncing is unconditionally done` / `immediately after a log message of priority CRIT, ALERT or` / `EMERG has been logged. This setting hence applies only to` / `messages of the levels ERR, WARNING, NOTICE, INFO, DEBUG. The` / `default timeout is 5 minutes. </para>`

`man/journald.conf.xml:170-182`:
> `<term><varname>RateLimitIntervalSec=</varname></term>` / `<term><varname>RateLimitBurst=</varname></term>` / (blank) / `<listitem><para>Configures the rate limiting that is applied` / `to all messages generated on the system. If, in the time` / `interval defined by <varname>RateLimitIntervalSec=</varname>,` / `more messages than specified in` / `<varname>RateLimitBurst=</varname> are logged by a service,` / `all further messages within the interval are dropped until the` / `interval is over. A message about the number of dropped` / `messages is generated. This rate limiting is applied` / `per-service, so that two services which log do not interfere` / `with each other's limits. Defaults to 10000 messages in 30s.`

`src/journal/journald-config.c:24-26`:
> `#define DEFAULT_SYNC_INTERVAL_USEC  (5*USEC_PER_MINUTE)` / `#define DEFAULT_RATE_LIMIT_INTERVAL (30*USEC_PER_SEC)` / `#define DEFAULT_RATE_LIMIT_BURST    10000`

logind idle action (mechanism) — `man/logind.conf.xml:149-155,157-162,169-173`:
> `<term><varname>IdleAction=</varname></term>` / (blank) / `<listitem><para>Configures the action to take when the system` / `is idle. Takes one of <literal>ignore</literal>, <literal>poweroff</literal>, <literal>reboot</literal>,` / `<literal>halt</literal>, <literal>kexec</literal>, <literal>suspend</literal>, <literal>hibernate</literal>,` / `<literal>hybrid-sleep</literal>, <literal>suspend-then-hibernate</literal>, <literal>sleep</literal>,` / `and <literal>lock</literal>. Defaults to <literal>ignore</literal>.</para>` … `<para>Note that this requires that user sessions correctly` / `report the idle status to the system. The system will execute` / `the action after all sessions report that they are idle, no` / `idle inhibitor lock is active, and subsequently, the time` / `configured with <varname>IdleActionSec=</varname> (see below)` / `has expired.</para>` … `<term><varname>IdleActionSec=</varname></term>` / (blank) / `<listitem><para>Configures the delay after which the action` / `configured in <varname>IdleAction=</varname> (see above) is` / `taken after the system is idle.</para>`

`src/login/logind.c:1127-1129` (the timer is not armed when the action is off): `        if (m->idle_action == HANDLE_IGNORE ||` / `            m->idle_action_usec <= 0)` / `                return 0;` — and `src/login/logind.c:1173`: `                                elapse, MIN(USEC_PER_SEC*30, m->idle_action_usec), /* accuracy of 30s, but don't have an accuracy lower than the idle action timeout */`

timesyncd (mechanism) — `man/timesyncd.conf.xml:103-105`:
> `<varname>PollIntervalMinSec=</varname> defaults to 32 seconds and must not be smaller than` / `16 seconds. <varname>PollIntervalMaxSec=</varname> defaults to 34 min 8 s (2048 seconds) and must be` / `larger than <varname>PollIntervalMinSec=</varname>.</para>` (the file uses U+00A0 no-break spaces inside the quantities; reproduced as in the file)

oomd polling (mechanism) — `src/oom/oomd-manager.h:13-15`:
> `#define SWAP_INTERVAL_USEC 150000 /* 0.15 seconds */` / `/* Pressure counters are lagging (~2 seconds) compared to swap so polling too frequently just wastes CPU */` / `#define MEM_PRESSURE_INTERVAL_USEC (1 * USEC_PER_SEC)`
`man/oomd.conf.xml:172` (end of the SwapUsedLimit= paragraph): `permille ("‰") or permyriad ("‱"), between 0% and 100%, inclusive. Defaults to 90%.</para>`

udevd idle workers (mechanism) — `src/udev/udev-manager.c:212-213`: `        log_debug("Cleaning up idle workers.");` / `        manager_kill_workers(manager, SIGTERM);` — armed at `src/udev/udev-manager.c:229-234`: `                r = event_reset_time_relative(` / `                                manager->event,` / `                                &manager->kill_workers_event,` / `                                CLOCK_MONOTONIC,` / `                                3 * USEC_PER_SEC,` / `                                USEC_PER_SEC,`

resolved cache (mechanism) — `src/resolve/resolved-dns-cache.c:22`: `#define CACHE_TTL_MAX_USEC (2 * USEC_PER_HOUR)` (the man pages resolved.conf(5)/systemd-resolved.service(8) state no cache TTL number, search-log row 48).

Treatment facts in shipped units — `units/systemd-journald.service.in:42`: `OOMScoreAdjust=-250`; `units/systemd-udevd.service.in:40-41`: `# Note that udev will reset the value internally for its workers` / `OOMScoreAdjust=-1000`; `units/systemd-oomd.service.in:38`: `OOMScoreAdjust=-900`; `units/systemd-tmpfiles-clean.service:23`: `IOSchedulingClass=idle`. No upstream systemd unit sets `Nice=` for a long-running daemon (`Nice=9` appears only in the coredump units), none sets `CPUSchedulingPolicy=`, and `CPUWeight=` appears only in the three user slices below (search-log row 45).

Session slices (treatment fact) — `units/user/session.slice:10-15`:
> `[Unit]` / `Description=User Core Session Slice` / `Documentation=man:systemd.special(7)` / (blank) / `[Slice]` / `CPUWeight=100`
`units/user/app.slice:11,15`: `Description=User Application Slice` … `CPUWeight=100`. `units/user/background.slice:11,15`: `Description=User Background Tasks Slice` … `CPUWeight=30`.

`man/systemd.special.xml:1398-1403`:
> `<term><filename>user.slice</filename></term>` / `<listitem>` / `<para>By default, all user processes and services started on` / `behalf of the user, including the per-user systemd instance` / `are found in this slice.  This is pulled in by` / `<filename>systemd-logind.service</filename>.</para>`
`man/systemd.special.xml:1578-1586`:
> `<term><filename>session.slice</filename></term>` / `<listitem>` / `<para>All essential services and applications required for the` / `session should use this slice.` / `These are services that either cannot be restarted easily` / `or where latency issues may affect the interactivity of the system and applications.` / `This includes the display server, screen readers and other services such as DBus or XDG portals.` / `Such services should be configured to be part of this slice by` / `adding <varname>Slice=session.slice</varname> to their unit files.</para>`
`man/systemd.special.xml:1568-1571` (app.slice): `<para>By default, all user services and applications managed by` / `<command>systemd</command> are found in this slice.` / `All interactively launched applications like web browsers and text editors` / `as well as non-critical services should be placed into this slice.</para>`; `:1595-1598` (background.slice): `<para>All services running low-priority background tasks should use this slice.` / `This permits resources to be preferentially assigned to the other slices.` / `Examples include non-interactive tasks like file indexing or backup operations` / `where latency is not important.</para>`

`docs/DESKTOP_ENVIRONMENTS.md:35-44`:
> ` * `session.slice`: Contains only processes essential to run the user's graphical session` / ` * `app.slice`: Contains all normal applications that the user is running` / ` * `background.slice`: Useful for low-priority background tasks` / (blank) / `The purpose of this grouping is to assign different priorities to the` / `applications.` / `This could e.g. mean reserving memory to session processes,` / `preferentially killing background tasks in out-of-memory situations` / `or assigning different memory/CPU/IO priorities to ensure that the session` / `runs smoothly under load.`

**Coverage.** T1 — covers, as mechanisms: object = systemd daemons (pid 1, journald, logind, udevd, timesyncd, oomd, resolved) and their timers; unit = seconds/µs; statistic = documented defaults and source constants (watchdog keep-alive = WatchdogSec/2 with WatchdogSec default 3min at build time; pid 1 hardware watchdog off by default, pinged at timeout/4 when on; journald sync 5 min, rate limit 10000/30 s; logind idle action off by default, timer accuracy 30 s; timesyncd poll 32 s → 2048 s; oomd swap poll 0.15 s and pressure poll 1 s; udev idle worker kill after 3 s; resolved cache TTL cap 2 h); scope = upstream defaults, population = none (no observation). No wake-cadence or CPU numbers. T2 — does not cover. T4 — covers, as treatment facts: OOMScoreAdjust of journald/udevd/oomd, IOSchedulingClass=idle for tmpfiles-clean, session/app/background slice CPUWeight 100/100/30 and their intended membership; carries no timing value. **One observation?** No — mechanism and treatment, no machine/subject/window.

### S2-02 — chrony (chrony.conf documentation and source defaults)

**Citation.** chrony project, *chrony* source tree, NEWS heading `New in version 4.9`, commit 8df4f1263e206585e6c4e61352d042c2dd12916a (2026-08-27T14:38:15+02:00), https://gitlab.com/chrony/chrony.git; `doc/chrony.conf.adoc` is the source of chrony.conf(5).

**Copy read.** local `sources/S2-02/`; SHA-256: `doc/chrony.conf.adoc` d47db23612b2298eefe819241288deff870b43d07cfc6820be36a4e27b8d61ab; `srcparams.h` 27e900e754cf63779810c25f0da15ec423be1074328c5b24b9deed7dd9bbe02a; `NEWS` 0dcdbe1ae44fc75544ceba7f2516a6736486c9c78ffbf50e9afc7bb789c536d8.

**Passages.** `doc/chrony.conf.adoc:92-96`:
> `*minpoll* _poll_:::` / `This option specifies the minimum interval between requests sent to the server` / `as a power of 2 in seconds. For example, *minpoll 5* would mean that the` / `polling interval should not drop below 32 seconds. The default is 6 (64` / `seconds), the minimum is -7 (1/128th of a second), and the maximum is 24 (6`
`doc/chrony.conf.adoc:102-107`:
> `*maxpoll* _poll_:::` / `This option specifies the maximum interval between requests sent to the server` / `as a power of 2 in seconds. For example, *maxpoll 9* indicates that the polling` / `interval should stay at or below 9 (512 seconds). The default is 10 (1024` / `seconds), the minimum is -7 (1/128th of a second), and the maximum is 24 (6` / `months).`
`srcparams.h:73-74`: `#define SRC_DEFAULT_MINPOLL 6` / `#define SRC_DEFAULT_MAXPOLL 10`

**Coverage.** T1 — covers as mechanism: chronyd NTP request interval per source, default 2^6 = 64 s minimum to 2^10 = 1024 s maximum; scope upstream default; no population. T2, T4 — do not cover (no treatment line in chrony's example unit was found; search-log row 50 and unit grep in row 45's companion grep across clones). **One observation?** No.

### S2-03 — cronie (crond main loop)

**Citation.** cronie project, *cronie* 1.7.2 (`configure.ac:1`: `AC_INIT([cronie],[1.7.2])`), commit cede1d68645ef8d36dd9ce76e9baa1a71e3b4f35 (2026-09-03T14:54:42+02:00), https://github.com/cronie-crond/cronie.

**Copy read.** local `sources/S2-03/`; SHA-256: `src/cron.c` d5416d701e677cb25ef386a2bbb117dd0d4838b1d437092d82865e42b566f61e; `configure.ac` a16533a6c6257fb7700fc06e00076e3616278a74ffc1c6018f8bda7640ee27bf.

**Passages.** `src/cron.c:359-366`:
> `	while (!got_sigintterm) {` / `		int timeDiff;` / `		enum timejump wakeupKind;` / (blank) / `		/* ... wait for the time (in minutes) to change ... */` / `		do {` / `			cron_sleep(timeRunning + 1, &database);` / `			set_time(FALSE);`
`src/cron.c:378-381`: `#if defined WITH_INOTIFY` / `		if (inotify_enabled) {` / `			check_inotify_database(&database);` / `		}`
`src/cron.c:628-644`:
> ` * Try to just hit the next minute.` / ` */` / `static void cron_sleep(int target, cron_db * db) {` / `	time_t t1, t2;` / `	int seconds_to_wait;` / (blank) / `	t1 = time(NULL) + GMToff;` / `	seconds_to_wait = (int)((time_t)target * SECONDS_PER_MINUTE - t1);` / `	/* always sleep at least once unless time goes backwards */` / `	if (seconds_to_wait == 0)` / `	    seconds_to_wait = 1;` / `	Debug(DSCH, ("[%ld] Target time=%ld, sec-to-wait=%d\n",` / `			(long) getpid(), (long) target * SECONDS_PER_MINUTE,` / `			seconds_to_wait));` / (blank) / `	while (seconds_to_wait > 0 && seconds_to_wait < 65) {` / `		sleep((unsigned int) seconds_to_wait);`

**Coverage.** T1 — covers as mechanism: crond wakes once per minute (sleeps to the next minute boundary) and re-reads crontabs via inotify when enabled; no CPU or wake statistic. T2, T4 — do not cover. **One observation?** No.

### S2-04 — dbus (dbus-daemon(1) source, bus configuration, units)

**Citation.** freedesktop.org D-Bus, *dbus* 1.16.99-alpha (`meson.build:24`: `    version: '1.16.99-alpha',`), commit b01f2e2c18cf4f10f2f2287f775134a2dc9182d1 (2026-09-19T17:05:07+00:00), https://gitlab.freedesktop.org/dbus/dbus.git; `doc/dbus-daemon.1.xml.in` is the source of dbus-daemon(1).

**Copy read.** local `sources/S2-04/`; SHA-256: `doc/dbus-daemon.1.xml.in` 13f692c3d7cdcaf969bd736f61ed76b40c31efa399a52b7940484ac26d815687; `bus/system.conf.in` 85fd4d49d012de9be1354d956ee489c1f4e26888d3ceb11ff6379dca56560251; `bus/session.conf.in` c36c254ab32b20eb618d8b22c6ab99f07f7a4145e1d02170e6b84393fe9798ac; `bus/config-parser.c` 8b35fad4a17b413e635b49071b64dd0500c7ccd685d1d7edb9f09c1d13c91850; `bus/dbus.service.in` 867744b701f529f4f8c6583a5465337cac279f16d1815979e9b1c9f223d0c2fe; `bus/systemd-user/dbus.service.in` 7af842ba2fc6843adfe8f111870af2ee2355ae1b2017b08d9b5380893e04638f; `meson.build` 198c4972cbd9c6ca7d285ee1d4c80cfadccaab7ce217f50cb1667e7060c4e063.

**Passages.** `doc/dbus-daemon.1.xml.in:834-841,857-858` (the `<limit>` table):
> `      "service_start_timeout"      : milliseconds (thousandths) until` / `                                     a started service has to connect` / `      "auth_timeout"               : milliseconds (thousandths) a` / `                                     connection is given to` / `                                     authenticate` / `      "pending_fd_timeout"         : milliseconds (thousandths) a` / `                                     fd is given to be transmitted to` / `                                     dbus-daemon before disconnecting the` … `      "reply_timeout"              : milliseconds (thousandths)` / `                                     until a method call times out`
`bus/system.conf.in:119-121` (commented defaults): `  <!-- <limit name="service_start_timeout">25000</limit> -->` / `  <!-- <limit name="auth_timeout">30000</limit> -->` / `  <!-- <limit name="pending_fd_timeout">150000</limit> -->`
`bus/config-parser.c:513`: `      parser->limits.auth_timeout = 30000; /* 30 seconds */`; `:551`: `      parser->limits.reply_timeout = -1; /* never */`
Treatment — `bus/dbus.service.in:9,11`: `ExecStart=@EXPANDED_BINDIR@/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only` … `OOMScoreAdjust=-900`; `bus/systemd-user/dbus.service.in:9,11`: `ExecStart=@EXPANDED_BINDIR@/dbus-daemon --session --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only` … `Slice=session.slice`.

**Coverage.** T1 — covers only as mechanism the bus's timeouts (auth 30 s, service start 25 s, pending fd 150 s, reply timeout unlimited by default); dbus-daemon(1) states no periodic idle activity and no thread structure (search-log row 52). T2 — does not cover. T4 — covers as treatment fact: system bus `OOMScoreAdjust=-900`; user bus `Slice=session.slice`; no timing value. **One observation?** No.

### S2-05 — dbus-broker (documentation and units)

**Citation.** bus1 project, *dbus-broker* 37 (`meson.build:16`: `        version: '37',`), commit 2956b5d381deeea709c53d02f10e799e50e44f4b (2026-07-02T11:13:39+02:00), https://github.com/bus1/dbus-broker; `docs/dbus-broker.rst` is the source of dbus-broker(1).

**Copy read.** local `sources/S2-05/`; SHA-256: `docs/dbus-broker.rst` 5db93f88ad4da8a81e2dac28be221aea7151feb9db510e13c61b6924715ddfbc; `src/units/system/dbus-broker.service.in` 847f1b0f0405e42111cd7cde483c0527aacdb7b19f9afd0afc30986207865371; `src/units/user/dbus-broker.service.in` 4e4679992971405d267781d445280c7340b2bbbdfbc23ef402694dbd707b5feb; `meson.build` 1e9ab68ea8343c317828324dc07709e01bc9258734d6b0b9a3a805624c870d6e.

**Passages.** `docs/dbus-broker.rst:85-89`:
> `By default, a broker instance is idle. That is, after forking and executing a` / `broker, it starts with an empty list of bus-sockets to manage, as well as no` / `way for clients to connect to it. The controller must use the controller` / `interface to create listener sockets, specify the bus policy, create` / `activatable names, and react to bus events.`
`docs/dbus-broker.rst:91-93`: `The **dbus-broker** process never accesses any external resources other than` / `those passed in either via the command-line or the controller interfaces. That` / `is, no file-system access, no **nss**\(5) calls, no external process`
Treatment — `src/units/system/dbus-broker.service.in:16-17,22`: `Type=notify-reload` / `OOMScoreAdjust=-900` … `ExecStart=@bindir@/dbus-broker-launch --scope system --audit`; `src/units/user/dbus-broker.service.in:17-18`: `ExecStart=@bindir@/dbus-broker-launch --scope user` / `Slice=session.slice`.

**Coverage.** T1 — covers as mechanism only the process model (a launcher process plus a broker that touches nothing but its sockets); no interval stated. T2 — does not cover. T4 — treatment fact: system broker `OOMScoreAdjust=-900`, user broker `Slice=session.slice`. **One observation?** No.

### S2-06 — PackageKit (packagekitd idle shutdown)

**Citation.** PackageKit project, *PackageKit* 1.4.1 (`meson.build:6`: `  version : '1.4.1',`), commit dc3604a0c07bc02e70e20edd57dd7cfb3a5c4b46 (2026-09-20T04:04:40+02:00), https://github.com/PackageKit/PackageKit.

**Copy read.** local `sources/S2-06/`; SHA-256: `src/pk-main.c` 21ad567eb924a64b25e53512534f536b1c0741232759b0ec9a1f7903d7f0c365; `data/config/PackageKit.conf` 8407f5c9bbcdbf33f23e97e67710b5794180a8b8c471ecc04829da690cf77fd5; `meson.build` e91a05c7d2218a98231a060703e12d46ab5c84c1a8d2de6974713dc7373f917b.

**Passages.** `data/config/PackageKit.conf:14-18`:
> `# Unlock the backend after this many seconds idle.` / `#BackendShutdownTimeout=5` / (blank) / `# Shut down the daemon after this many seconds idle. 0 means don't shutdown.` / `#ShutdownTimeout=300`
`src/pk-main.c:208-216`: `	/* after how long do we timeout? */` / `	exit_idle_time = g_key_file_get_integer (conf, "Daemon", "ShutdownTimeout", &error);` / `	/* THIS COMMENT IS A TSUNAMI STONE` / `	 * The automatic shutdown timeout prevents memory leaks in some` / `	 * backends from getting out of hand.  If you want to remove this` / `	 * timeout, please study the Git history and be sure that you are not` / `	 * regressing Red Hat bugzilla #1354074 (again). */` / `	if (error != NULL) {` / `		exit_idle_time = 300;`
`src/pk-main.c:267-275`: `	/* only poll when we are alive */` / `	if (exit_idle_time > 0 && !disable_timer) {` / `		helper.engine = engine;` / `		helper.exit_idle_time = exit_idle_time;` / `		helper.loop = loop;` / `		helper.timer_id = g_timeout_add_seconds (5,` / `							 (GSourceFunc) pk_main_timeout_check_cb,` / `							 &helper);` / `		g_source_set_name_by_id (helper.timer_id, "[PkMain] main poll");`

**Coverage.** T1 — covers as mechanism: packagekitd polls its own idle time every 5 s and exits after 300 s idle by default (so it is not resident on an idle system unless disabled). T2, T4 — do not cover. **One observation?** No.

### S2-07 — multipath-tools (multipathd polling interval, threads, unit)

**Citation.** opensvc/multipath-tools, `libmultipath/version.h:14`: `#define VERSION_CODE 0x000F01` (0.15.1), commit d53932bdbee02f440518ea384e63d7c4d3f66685 (2026-08-27T16:40:22+02:00), https://github.com/opensvc/multipath-tools; `multipath/multipath.conf.5.in` is the source of multipath.conf(5).

**Copy read.** local `sources/S2-07/`; SHA-256: `multipath/multipath.conf.5.in` 95895fa8805fdd2ba93c1d54379da71a50b2555fb39ccc1c1cb208da96cd0bb5; `libmultipath/defaults.h` c1ee91165d8c59e59dc7239971e65ed5bf1325e4bff4bd4ffe379e465f64ff99; `libmultipath/config.c` 6be1e1937c25f6c7dc97ade984da8b86ba250e4799e9921acb1535c5122634c9; `multipathd/multipathd.service.in` 13c4668b78fdc5b732d0a25777c855ed8d5024de75fa34cf25898ffa6623b72c; `multipathd/main.c` 3ddf619a7a57253ca5e9e786047a6fb786b409930b0ad36998b638fc7c5e916a; `libmultipath/version.h` 6b6a5ee1aad5465f5658a7af80b9cc4c43e96f177e96b4601d2c090f328b8d07.

**Passages.** `multipath/multipath.conf.5.in:149-166`:
> `.B polling_interval` / `Interval between two path checks in seconds. For properly functioning paths,` / `the interval between checks will gradually increase to \fImax_polling_interval\fR.` / `This value will be overridden by the \fIWatchdogSec\fR` / `setting in the multipathd.service definition if systemd is used.` / `.RS` / `.TP` / `The default is: \fB5\fR` / `.RE` / `.` / `.` / `.TP` / `.B max_polling_interval` / `Maximal interval between two path checks in seconds.` / `.RS` / `.TP` / `The default is: \fB4 * polling_interval\fR` / `.RE`
`libmultipath/defaults.h:64`: `#define DEFAULT_CHECKINT	5`
Threads — `multipathd/main.c:4043`: `	rc = pthread_create(&uxlsnr_thr, &misc_attr, uxlsnrloop, vecs);`; `:4081`: `	if ((rc = pthread_create(&uevent_thr, &uevent_attr, ueventloop, udev))) {`; `:4091`: `	if ((rc = pthread_create(&check_thr, &misc_attr, checkerloop, vecs))) {`; `:4096`: `	if ((rc = pthread_create(&purge_thr, &misc_attr, purgeloop, vecs))) {`; `:4101`: `	if ((rc = pthread_create(&uevq_thr, &misc_attr, uevqloop, vecs))) {` (plus dmevent at :4069 and the two fpin threads at :4108, :4115, conditionally).
Treatment — `multipathd/multipathd.service.in:22,26-27`: `ExecStart=@BINDIR@/multipathd -d -s` … `LimitRTPRIO=10` / `CPUWeight=1000`

**Coverage.** T1 — covers as mechanism: path-checker period 5 s default rising to 20 s; thread structure (uxlsnr, uevent, checker, purge, uevq, optional dmevent/fpin threads). T2 — does not cover. T4 — treatment fact: shipped unit `CPUWeight=1000` and `LimitRTPRIO=10`. **One observation?** No.

### S2-08 — udisks (udisksd housekeeping timer)

**Citation.** storaged-project/udisks 2.12.0 (`configure.ac:2-4`: major 2, minor 12, micro 0), commit c731cee133bb3240a0b91b59f9995a42aafb0ac4 (2026-08-28T08:25:48+02:00), https://github.com/storaged-project/udisks.

**Copy read.** local `sources/S2-08/`; SHA-256: `src/udiskslinuxprovider.c` 8cf1b894f7b0c2375d61a99734e17f1ff5b26c55a3a79facfb0241d6fe44ef07; `configure.ac` 2ecff9f495956906ec5ca3a0035825df49781220a2c5aca8384a53b1ad1f32a7.

**Passages.** `src/udiskslinuxprovider.c:817-822`:
> `  /* schedule housekeeping for every 10 minutes */` / `  provider->housekeeping_timeout = g_timeout_add_seconds (10*60,` / `                                                          on_housekeeping_timeout,` / `                                                          provider);` / `  /* ... and also do an initial run */` / `  on_housekeeping_timeout (provider);`

**Coverage.** T1 — covers as mechanism: udisksd's periodic housekeeping every 600 s (besides udev events). T2, T4 — do not cover (no treatment line in its unit; search-log row 45 companion grep). **One observation?** No.

### S2-09 — rsyslog (main queue worker defaults)

**Citation.** rsyslog 8.2610.0.daily (`configure.ac:5`: `AC_INIT([rsyslog],[8.2610.0.daily],[rsyslog@lists.adiscon.com])     # UPDATE on release`), commit c5cafe3e85679be9e6c3434c9ac23399eab32b9d (2026-09-16T16:17:50+02:00), https://github.com/rsyslog/rsyslog.

**Copy read.** local `sources/S2-09/`; SHA-256: `runtime/rsconf.c` f5bfcc60dd1ed7b53df53b57b6d58f07ca95c83e97fb013c10804011f5168bef; `configure.ac` c45192216e5f9285f29dc98a0ceb5d2f82a8330255d1fa648463bcb3108d3a84.

**Passages.** `runtime/rsconf.c:381,386,394-396`:
> `    pThis->globals.mainQ.iMainMsgQueueSize = 100000;` … `    pThis->globals.mainQ.iMainMsgQueueNumWorkers = 2;` … `    pThis->globals.mainQ.iMainMsgQtoEnq = 2000;` / `    pThis->globals.mainQ.iMainMsgQtoWrkShutdown = 60000;` / `    pThis->globals.mainQ.iMainMsgQWrkMinMsgs = 40000;`

**Coverage.** T1 — covers as mechanism: rsyslogd's main queue has up to 2 worker threads by default and idle workers are shut down after 60000 ms (`iMainMsgQtoWrkShutdown`); no periodic idle timer stated. T2, T4 — do not cover. **One observation?** No.

### S2-10 — NetworkManager (connectivity-check interval)

**Citation.** NetworkManager 1.59.2-dev (`meson.build:8`: `  version: '1.59.2-dev',`), commit 58864ef92d3241787c311fad9a16a28524b206e1 (2026-09-17T09:17:52+02:00), https://gitlab.freedesktop.org/NetworkManager/NetworkManager.git; `man/NetworkManager.conf.xml` is the source of NetworkManager.conf(5).

**Copy read.** local `sources/S2-10/`; SHA-256: `man/NetworkManager.conf.xml` 3ff544498ccdec4c7ae62defb0761d78d4199e12553874967de0a410107c45a0; `meson.build` 0ebd5cacf9c0ccfb74f9923b483ecd8995e2473019c2b094465f8852793f51b9.

**Passages.** `man/NetworkManager.conf.xml:1589-1593`:
> `          <term><varname>interval</varname></term>` / `          <listitem><para>Specified in seconds; controls how often` / `          connectivity is checked when a network connection exists. If` / `          set to 0 connectivity checking is disabled.  If missing, the` / `          default is 300 seconds.</para></listitem>`

**Coverage.** T1 — covers as mechanism: NetworkManager's connectivity check every 300 s when a `[connectivity]` URI is configured; nothing on thread structure or other idle work. T2, T4 — do not cover (no treatment key in `data/*.service.in`, search-log row 58). **One observation?** No.

### S2-12 — Mutter (frame clock, KMS thread scheduling, headless option, idle monitor)

**Citation.** GNOME Mutter 51.0 (`meson.build:2`: `  version: '51.0',`), commit 888a7b7dac0c58612007c46bbad75de9f9437f48 (2026-09-17T21:51:45+00:00), https://gitlab.gnome.org/GNOME/mutter.git.

**Copy read.** local `sources/S2-12/`; SHA-256: `clutter/clutter/clutter-frame-clock.c` 779f66d529e3d6b253334f42c6deddc89488ba711eff75019990f17c87e4b4de; `src/backends/native/meta-kms.c` 96a3a7632c83fdb2489ec6dac364f37c0b36fe8c945505931d5440290a3ecf1e; `src/backends/native/meta-thread.c` 9c7f83ef6139230ec58f3432b48d26c6e5b46c3b6fc0e1820c0b624ee29f6548; `src/core/meta-context-main.c` 21c0bd4c87b73ff5ed142abebd64d80af2982f09ee474d441fadfc8fb1bde7d6; `src/backends/meta-idle-monitor.c` fcd558f8600d5ffe3ed7951d3aad57f5bc693988e63dccf9765aa0b6dc573a85; `.gitlab-ci.yml` 80d83de89b64d957588ccda4c2f1231b82c377d7d7832cae5369c67cdf51d8c6; `meson.build` 6558a30d17ffdb711367576d8edff55530fc067820403a0b6ad39cf275ba576a.

**Passages.** Frame-clock states — `clutter/clutter/clutter-frame-clock.c:76-88`:
> `typedef enum _ClutterFrameClockState` / `{` / `  CLUTTER_FRAME_CLOCK_STATE_INIT,` / `  CLUTTER_FRAME_CLOCK_STATE_IDLE,` / `  CLUTTER_FRAME_CLOCK_STATE_SCHEDULED,` / `  CLUTTER_FRAME_CLOCK_STATE_SCHEDULED_NOW,` / `  CLUTTER_FRAME_CLOCK_STATE_SCHEDULED_LATER,` / `  CLUTTER_FRAME_CLOCK_STATE_DISPATCHED_ONE,` / `  CLUTTER_FRAME_CLOCK_STATE_DISPATCHED_ONE_AND_SCHEDULED,` / `  CLUTTER_FRAME_CLOCK_STATE_DISPATCHED_ONE_AND_SCHEDULED_NOW,` / `  CLUTTER_FRAME_CLOCK_STATE_DISPATCHED_ONE_AND_SCHEDULED_LATER,` / `  CLUTTER_FRAME_CLOCK_STATE_DISPATCHED_TWO,` / `} ClutterFrameClockState;`
The clock returns to IDLE after a presented frame with nothing further scheduled — `:904-908` (in `clutter_frame_clock_notify_presented`, whose header is at `:623`): `    case CLUTTER_FRAME_CLOCK_STATE_DISPATCHED_ONE:` / `      clutter_frame_clock_set_state (frame_clock,` / `                                     CLUTTER_FRAME_CLOCK_STATE_IDLE);` / `      maybe_reschedule_update (frame_clock);` / `      break;` — and after a dispatch that painted nothing, `:1980-1983`: `    case CLUTTER_FRAME_RESULT_IGNORED:` / `      frame_clock->state = CLUTTER_FRAME_CLOCK_STATE_IDLE;` / `      clear_frame (&frame_clock->next_presentation);` / `      maybe_reschedule_update (frame_clock);`
Inhibit (used while an output is off/paused) — `:1319-1336`:
> `void` / `clutter_frame_clock_inhibit (ClutterFrameClock *frame_clock)` / `{` / `  frame_clock->inhibit_count++;` / (blank) / `  if (frame_clock->inhibit_count == 1)` / `    {` / `      switch (frame_clock->state)` / `        {` / `        case CLUTTER_FRAME_CLOCK_STATE_INIT:` / `        case CLUTTER_FRAME_CLOCK_STATE_IDLE:` / `          break;` / `        case CLUTTER_FRAME_CLOCK_STATE_SCHEDULED:` / `        case CLUTTER_FRAME_CLOCK_STATE_SCHEDULED_LATER:` / `          frame_clock->pending_reschedule = TRUE;` / `          clutter_frame_clock_set_state (frame_clock,` / `                                         CLUTTER_FRAME_CLOCK_STATE_IDLE);` / `          break;`
The source is a GSource backed by timerfd when available — `:64-74`: `typedef struct _ClutterClockSource` / `{` / `  GSource source;` / (blank) / `  ClutterFrameClock *frame_clock;` / (blank) / `#ifdef HAVE_TIMERFD` / `  int tfd;` / `  struct itimerspec tfd_spec;` / `#endif` / `} ClutterClockSource;`
KMS thread and its scheduling (treatment fact set by the program on itself) — `src/backends/native/meta-kms.c:421`: `  MetaThreadType thread_type = META_THREAD_TYPE_KERNEL;`; `:453-459`: `  else` / `    {` / `      if (flags & META_KMS_FLAG_NO_MODE_SETTING)` / `        preferred_scheduling_priority = META_SCHEDULING_PRIORITY_NORMAL;` / `      else` / `        preferred_scheduling_priority = META_SCHEDULING_PRIORITY_HIGH_PRIORITY;` / `    }`; `:461-468`: `  kms = g_initable_new (META_TYPE_KMS,` / `                        NULL, error,` / `                        "backend", backend,` / `                        "name", "KMS thread",` / `                        "thread-type", thread_type,` / `                        "preferred-scheduling-priority", preferred_scheduling_priority,` / `                        NULL);`
How the priority is obtained (through rtkit) — `src/backends/native/meta-thread.c:286-288`: `  meta_topic (META_DEBUG_BACKEND, "Setting '%s' thread nice level to %d",` / `              priv->name, nice_level);` / `  if (!meta_dbus_realtime_kit1_call_make_thread_high_priority_sync (priv->kernel.rtkit_proxy,` (nice_level read from rtkit's `MinNiceLevel` at `:265-271`); realtime path `:346-349`: `  meta_topic (META_DEBUG_BACKEND,` / `              "Setting soft and hard RLIMIT_RTTIME limit to %lu", rttime);` / `  rl.rlim_cur = rttime;` / `  rl.rlim_max = rttime;` and `:358-360`: `  meta_topic (META_DEBUG_BACKEND, "Setting '%s' thread real time priority to %d",` / `              priv->name, priority);` / `  if (!meta_dbus_realtime_kit1_call_make_thread_realtime_sync (priv->kernel.rtkit_proxy,` (priority read from rtkit's `MaxRealtimePriority` at `:315-321`).
Headless — `src/core/meta-context-main.c:367-369`: `      "headless", 0, 0, G_OPTION_ARG_NONE,` / `      &context_main->options.headless,` / `      N_("Run as a headless display server")`. `MUTTER_DEBUG_DUMMY_MODE_SPECS` appears in this tree only in `.gitlab-ci.yml:516`: `    MUTTER_DEBUG_DUMMY_MODE_SPECS: "800x600@10.0"` (no occurrence under `src/` or `clutter/`, search-log row 59).
Idle monitor — `src/backends/meta-idle-monitor.c:26`: ` * Mutter idle counter (similar to X's IDLETIME)`.

**Coverage.** T2 — covers as mechanism: the per-view frame clock is a state machine that is IDLE unless an update is scheduled by damage/timelines, is inhibited (returned to IDLE) when the output is inhibited, and is driven by a timerfd-backed GSource; the KMS work runs on a dedicated "KMS thread" which by default requests high-priority (nice) scheduling via rtkit and can request SCHED realtime via rtkit with `RLIMIT_RTTIME` set to rtkit's `RTTimeUSecMax`; `--headless` exists. No per-frame CPU cost, wake cadence or CPU share is stated anywhere in these files. T1 — does not cover. T4 — covers, as treatment fact, only what Mutter asks rtkit for its KMS thread (default `META_SCHEDULING_PRIORITY_HIGH_PRIORITY`, i.e. rtkit's `MinNiceLevel`; realtime only when `MUTTER_DEBUG_KMS_SCHEDULING_PRIORITY=realtime`); numeric values come from rtkit (S2-21). **One observation?** No.

### S2-13 — GNOME Shell (screen shield idle fade, systemd unit)

**Citation.** GNOME Shell 51.0 (`meson.build:2`: `  version: '51.0',`), commit f8a5dc649022f94c63d0ee18daa8bf4f0e76f979 (2026-09-17T16:24:10+02:00), https://gitlab.gnome.org/GNOME/gnome-shell.git.

**Copy read.** local `sources/S2-13/`; SHA-256: `js/ui/screenShield.js` cbe6c9f35362fe485b961574b35f59fcd777bae8f36ec713ad1d2461eeeba0ca; `data/org.gnome.Shell@.service.in` 7ae8174282fdb8f9f02ff6bc3cf3823689d2cc3ec115719d81928fa8706c71eb; `meson.build` 225de1dd51f586cce28461732707fa15e9bdcb871be4c302e71d69565aaf4965.

**Passages.** `js/ui/screenShield.js:33-40`:
> `// ScreenShield animation time` / `// - STANDARD_FADE_TIME is used when the session goes idle` / `// - MANUAL_FADE_TIME is used for lowering the shield when asked by the user,` / `//   or when cancelling the dialog` / `// - CURTAIN_SLIDE_TIME is used when raising the shield before unlocking` / `const STANDARD_FADE_TIME = 10000;` / `const MANUAL_FADE_TIME = 300;` / `const CURTAIN_SLIDE_TIME = 300;`
`js/ui/screenShield.js:43-48`:
> ` * If you are setting org.gnome.desktop.session.idle-delay directly in dconf,` / ` * rather than through System Settings, you also need to set` / ` * org.gnome.settings-daemon.plugins.power.sleep-display-ac and` / ` * org.gnome.settings-daemon.plugins.power.sleep-display-battery to the same value.` / ` * This will ensure that the screen blanks at the right time when it fades out.` / ` * https://bugzilla.gnome.org/show_bug.cgi?id=668703 explains the dependency.`
Unit — `data/org.gnome.Shell@.service.in:17-20`: `[Service]` / `Slice=session.slice` / `Type=notify` / `ExecStart=@bindir@/gnome-shell --mode=%i`; `:32-33`: `# Lower down gnome-shell's OOM score to avoid being killed by OOM-killer too early` / `OOMScoreAdjust=-1000`

**Coverage.** T2 — covers as mechanism: on session idle the shell fades the screen over 10000 ms; the actual blank timing is delegated to gnome-settings-daemon's power plugin (not read here — its repository was not cloned; recorded in Not found). T4 — treatment fact: `Slice=session.slice`, `OOMScoreAdjust=-1000`; no `Nice=`/`CPUWeight=`. T1 — does not cover. **One observation?** No.

### S2-14 — gsettings-desktop-schemas (org.gnome.desktop.session idle-delay)

**Citation.** GNOME gsettings-desktop-schemas 51.0 (`meson.build:3`: `  version: '51.0',`), commit 4dc6fa0a3526f8b4044962b8b3a3fb8b975a355c (2026-09-19T21:15:51+00:00), https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas.git.

**Copy read.** local `sources/S2-14/`; SHA-256: `schemas/org.gnome.desktop.session.gschema.xml.in` a18788e5bc793c92ed0763c57aa33560a07527e785029c6d7fb224c95796c858; `meson.build` d3e95e8b6ae098b6cd25d7dcb61bac2479db0757e199af9fe3b6124bd157c9e5.

**Passages.** `schemas/org.gnome.desktop.session.gschema.xml.in:4-8`:
> `    <key name="idle-delay" type="u">` / `      <default>300</default>` / `      <summary>Time before session is considered idle</summary>` / `      <description>The number of seconds of inactivity before the session is considered idle.</description>` / `    </key>`

**Coverage.** T2 — covers as mechanism: GNOME session idle after 300 s of inactivity by default. T1, T4 — do not cover. **One observation?** No.

### S2-15 — KWin (RenderLoop scheduling, real-time thread policy, unit)

**Citation.** KDE KWin 6.8.80 (`CMakeLists.txt:3`: `set(PROJECT_VERSION "6.8.80") # Handled by release scripts`), commit b8ef79a70431550832671daa28f1a3201aeca575 (2026-09-20T01:52:51+00:00), https://invent.kde.org/plasma/kwin.git.

**Copy read.** local `sources/S2-15/`; SHA-256: `src/core/renderloop.cpp` 31eb3f1f871c914433579a0ad928115a873c09ba4aaa882d8d006372ed9f3b8f; `src/core/renderloop_p.h` ee2c8bef2446c95239da276aa8b30cfcd15e9eef57a5c02227e06854532cef0e; `src/utils/realtime.cpp` 0a1bcf4a74aedb699f5713059fb2e3c2dc86be4ae594f4d6f7e646cfa8e51a3b; `src/main_wayland.cpp` 17ad8fad7686195065b80a77d7ab50bc7aedf3a242b6a292edb2057b6d5c6881; `src/CMakeLists.txt` 5272796dff8ba3d1621ef8994e6859bb0510516adab5239ec9bab0fb9c3b0eef; `plasma-kwin_wayland.service.in` 24e39ad7db554249cc1254f610db2328293802d8ab981d5eb88be307a6bf27aa; `CMakeLists.txt` eb0f0118efc1f03d553eb77ae503b6fc1b2fd1595c48248457057fea05bfdafb.

**Passages.** Repaint scheduling — `src/core/renderloop.cpp:50-53`: `void RenderLoopPrivate::scheduleRepaint(std::chrono::nanoseconds lastTargetTimestamp, std::chrono::nanoseconds presentNotBefore)` / `{` / `    pendingReschedule.reset();` / `    const std::chrono::nanoseconds vblankInterval(1'000'000'000'000ull / refreshRate);`; `:59-61`: `    // Estimate when it's a good time to perform the next compositing cycle.` / `    // the 1ms on top of the safety margin is required for timer and scheduler inaccuracies` / `    std::chrono::nanoseconds expectedCompositingTime = std::min(renderJournal.result() + safetyMargin + 1ms, 2 * vblankInterval);`; `:66-69`: `        if (pageflipsSince > 100) {` / `            // if it's been a while since the last frame, the GPU is likely in a low power state and render time will be increased` / `            // -> take that into account and start compositing very early` / `            expectedCompositingTime = std::max(vblankInterval - 1us, expectedCompositingTime);`; `:140-141`: `    const std::chrono::nanoseconds nextRenderTimestamp = nextPresentationTimestamp - expectedCompositingTime;` / `    compositeTimer.start(nextRenderTimestamp);`
Idle: the timer is only started by a repaint request — `:296-303`: `    d->delayedVrrTimer.stop();` / `    const int effectiveMaxPendingFrameCount = (vrr || tearing) ? 1 : d->maxPendingFrameCount;` / `    if (d->pendingFrameCount < effectiveMaxPendingFrameCount && !d->inhibitCount) {` / `        d->scheduleNextRepaint(presentNotBefore);` / `    } else if (d->pendingReschedule) {` / `        d->pendingReschedule = std::min(*d->pendingReschedule, presentNotBefore.value_or(std::chrono::steady_clock::now()));` / `    } else {` / `        d->pendingReschedule = presentNotBefore.value_or(std::chrono::steady_clock::now());`
Inhibit — `:228-235`: `void RenderLoop::inhibit()` / `{` / `    d->inhibitCount++;` / (blank) / `    if (d->inhibitCount == 1) {` / `        d->compositeTimer.stop();` / `    }` / `}`
VRR delay timer — `:291-292`: `            constexpr std::chrono::milliseconds s_delayVrrTimer = 1'000ms / 30;` / `            d->delayedVrrTimer.start(s_delayVrrTimer, Qt::PreciseTimer, this);`
Defaults — `src/core/renderloop_p.h:50`: `    int refreshRate = 60000;`; `:55`: `    std::chrono::nanoseconds safetyMargin{0};`; `:58`: `    int maxPendingFrameCount = 1;`
Real-time policy set on itself (treatment fact) — `src/utils/realtime.cpp:17-28`:
> `void gainRealTime()` / `{` / `#if HAVE_SCHED_RESET_ON_FORK` / `    const int minPriority = sched_get_priority_min(SCHED_RR);` / `    sched_param sp;` / `    sp.sched_priority = minPriority;` / `    const int error = pthread_setschedparam(pthread_self(), SCHED_RR | SCHED_RESET_ON_FORK, &sp);` / `    if (error) {` / `        qWarning("Failed to gain real time thread priority (See CAP_SYS_NICE in the capabilities(7) man page). error: %s", strerror(error));` / `    }` / `#endif` / `}`
`src/main_wayland.cpp:290-292,297`: `    // Some Linux distros may set ambient capabilities, so clear CAP_SYS_NICE here to avoid` / `    // leaking it to all child processes.` / `    prctl(PR_CAP_AMBIENT, PR_CAP_AMBIENT_LOWER, CAP_SYS_NICE, 0, 0);` … `    KWin::gainRealTime();`
`src/CMakeLists.txt:701-708`: `if(CMAKE_SYSTEM_NAME MATCHES "Linux")` / `    install(` / `        CODE "execute_process(` / `        COMMAND ${SETCAP_EXECUTABLE}` / `        CAP_SYS_NICE=+ep` / `        \$ENV{DESTDIR}${CMAKE_INSTALL_FULL_BINDIR}/kwin_wayland)"` / `    )` / `endif()`
Unit — `plasma-kwin_wayland.service.in:6-8`: `ExecStart=@CMAKE_INSTALL_FULL_BINDIR@/kwin_wayland_wrapper --xwayland` / `BusName=org.kde.KWinWrapper` / `Slice=session.slice`

**Coverage.** T2 — covers as mechanism: one RenderLoop per output; the composite timer fires at (next presentation − predicted compositing time) and is armed only on repaint requests, stopped by inhibit; refreshRate default 60000 mHz, maxPendingFrameCount 1, VRR delay 33 ms; the main thread sets `SCHED_RR` at the minimum RT priority via its own `CAP_SYS_NICE` file capability (not rtkit). No CPU-per-frame or wake numbers. T4 — treatment fact: `SCHED_RR|SCHED_RESET_ON_FORK` at `sched_get_priority_min(SCHED_RR)` for kwin_wayland's main thread, `CAP_SYS_NICE=+ep` set at install, `Slice=session.slice`. T1 — does not cover. **One observation?** No.

### S2-16 — X.Org X server (WaitForSomething, screensaver/DPMS defaults, SmartSchedule, Xvfb, Xwayland)

**Citation.** X.Org xserver 26.1.99.1 (`meson.build:6`: `        version: '26.1.99.1',`), commit 306071c0b9683ef0dfadcfc2dbb78d369680542b (2026-09-13T15:16:44-07:00), https://gitlab.freedesktop.org/xorg/xserver.git; `hw/xfree86/man/xorg.conf.man`, `man/Xserver.man`, `hw/vfb/man/Xvfb.man` are the sources of xorg.conf(5), Xserver(1), Xvfb(1).

**Copy read.** local `sources/S2-16/`; SHA-256: `os/WaitFor.c` 848f816fe462110d4cf5024bc08f3e854961fc1bb8ab02d75a3e9affea6522f0; `dix/globals.c` 6bdeeb70d77c1e80d78e67d2e1a436ab3a76fe7f0ab9cf94f8b43be95a2860f0; `dix/dispatch.c` 11b92b7c1d885164c201f0b0838614ca908dd478fbe083f52fc226f84a85f131; `hw/xfree86/man/xorg.conf.man` cbabc655db1d67f67fe5edb5d84f50eccc06ac1c0401964435459850bd04881a; `man/Xserver.man` 51b6d5f638a3ac7d323c993af687edfad45881156f47271cc1b9eeebd7bf62d9; `hw/vfb/man/Xvfb.man` fac0a08ca3649b516e435d984981e05b33963fa55efb4f15b999b3661eb96ce5; `hw/xwayland/xwayland-window.c` 0fbed29c23f5d0bfcf32635b8663e6ea1230b738e17927d5e37171037534baa6; `meson.build` e6aa33820a4df135aeb4e915c487e49f4ff8c10ecc3224ac12076fa79aedb292.

**Passages.** `os/WaitFor.c:159-163`:
> ` *     If the time between INPUT events is` / ` *     greater than ScreenSaverTime, the display is turned off (or` / ` *     saved, depending on the hardware).  So, WaitForSomething()` / ` *     has to handle this also (that's why the select() has a timeout.` / ` *     For more info on ClientsWithInput, see ReadRequestFromClient().`
`os/WaitFor.c:195-208`:
> `        timeout = check_timers();` / `        are_ready = clients_are_ready();` / (blank) / `        if (are_ready)` / `            timeout = 0;` / (blank) / `        BlockHandler(&timeout);` / `        if (NewOutputPending)` / `            FlushAllOutput();` / `        /* keep this check close to select() call to minimize race */` / `        if (dispatchException)` / `            i = -1;` / `        else` / `            i = ospoll_wait(server_poll, timeout);`
`dix/globals.c:95-97`: `/* default time of 10 minutes */` / `CARD32 defaultScreenSaverTime = (10 * (60 * 1000));` / `CARD32 defaultScreenSaverInterval = (10 * (60 * 1000));`
`dix/dispatch.c:240-242`: `/* in milliseconds */` / `#define SMART_SCHEDULE_DEFAULT_INTERVAL	5` / `#define SMART_SCHEDULE_MAX_SLICE	15`
`hw/xfree86/man/xorg.conf.man:566-576`:
> `.BI "Option \*qBlankTime\*q  \*q" time \*q` / `sets the inactivity timeout for the` / `.B blank` / `phase of the screensaver.` / `.I time` / `is in minutes.` / `This is equivalent to the Xorg server's` / `.B \-s` / `flag, and the value can be changed at run\-time with` / `.BR xset (@appmansuffix@).` / `Default: 10 minutes.`
(`StandbyTime`, `SuspendTime` likewise `Default: 10 minutes.` at `:585` and `:599`.) `man/Xserver.man:282-283`: `.B \-s \fIminutes\fP` / `sets screen-saver timeout time in minutes.`
`hw/vfb/man/Xvfb.man:31,37-39`: `Xvfb \- virtual framebuffer X server for X Version 11` … `is an X server that can run on machines with no display hardware` / `and no physical input devices.  It emulates a dumb framebuffer using` / `virtual memory.`
Xwayland frame pacing by Wayland frame callbacks — `hw/xwayland/xwayland-window.c:2004-2014`: `frame_callback(void *data,` / `               struct wl_callback *callback,` / `               uint32_t time)` / `{` / `    struct xwl_window *xwl_window = data;` / (blank) / `    wl_callback_destroy (xwl_window->frame_callback);` / `    xwl_window->frame_callback = NULL;` / (blank) / `    if (xwl_window->xwl_screen->present) {` / `        xwl_present_for_each_frame_callback(xwl_window, xwl_present_frame_callback);`

**Coverage.** T2 — covers as mechanism: the X server blocks in `ospoll_wait` with a timeout computed from its timers (screensaver/DPMS default 10 min blank, standby, suspend), i.e. no periodic wake of its own with idle clients; the client scheduler ("SmartSchedule") uses a 5 ms interval/15 ms max slice when clients are busy; Xvfb is the same server on a memory framebuffer; Xwayland paces windows by the compositor's frame callbacks. No CPU or wake numbers. T1, T4 — do not cover. **One observation?** No.

### S2-17 — xf86-video-dummy (the Xorg dummy driver)

**Citation.** X.Org xf86-video-dummy 0.4.1 (`configure.ac:25-26`: `AC_INIT([xf86-video-dummy],` / `        [0.4.1],`), commit 533b5313d658422039716f97d59a3eff281401fc (2025-08-12T17:39:30-07:00), https://gitlab.freedesktop.org/xorg/driver/xf86-video-dummy.git.

**Copy read.** local `sources/S2-17/`; SHA-256: `README.md` c1ad51c2fba1125553b0addb3a7cee3da8767097c6b486793088f4c934cd2933; `src/dummy_driver.c` c28053035ac0a107e95baaeb49339bb0b7231448a4375038f803a2010b77b8b1; `configure.ac` e47c8fb80c3dadc8bc96e09df868d155619987c9130cf51056f7804615520ffd.

**Passages.** `README.md:1`: `xf86-video-dummy - virtual/offscreen frame buffer driver for the Xorg X server`. `src/dummy_driver.c:634-637`: `    } else {` / `	pScrn->videoRam = 4096;` / `	xf86DrvMsg(pScrn->scrnIndex, X_PROBED, "VideoRAM: %d kByte\n",` / `		   pScrn->videoRam);`. The tree ships no man page (search-log row 16).

**Coverage.** T2 — covers as mechanism only that a headless Xorg can be run with an offscreen framebuffer driver (default 4096 kByte VideoRAM); nothing on timing. T1, T4 — do not cover. **One observation?** No.

### S2-18 — PipeWire (daemon configuration defaults, module-rt, driver node, node suspension, units)

**Citation.** PipeWire 1.7.0 (`meson.build:2`: `  version : '1.7.0',`), commit decc0d2efa2db7476faaa70043774b722317da78 (2026-09-18T14:58:01+02:00), https://gitlab.freedesktop.org/pipewire/pipewire.git; `src/daemon/pipewire.conf.in` is the shipped `pipewire.conf`, the `\page` comment in `src/modules/module-rt.c` is the source of the module-rt page at docs.pipewire.org.

**Copy read.** local `sources/S2-18/`; SHA-256: `src/daemon/pipewire.conf.in` 8bb0dda1eecefd05f7fb234811e560a5c0edd467db16c9cefdd780c63fab0369; `src/daemon/minimal.conf.in` eb073c2ffe62035ca6b4e33e8d2e6fbeb62c394644639e0de1250f0f81944df7; `src/modules/module-rt.c` 4dfbb92bc899d1d384d3c782740dc8c18e3a801b91d29b703bca60d2d455290e; `src/modules/module-rt/25-pw-rlimits.conf.in` b2292f2ffb27059cf963aad4d0f4a4bb4219f8311addfcf869bb42f6ec684f81; `meson_options.txt` 663fe1e994203d5f95a9a0b7bd379822a3ec91e3cd8e66a50e5b8d28723c8383; `spa/plugins/support/node-driver.c` 545b78d2251faaf0d91f5e1fb59c64dd7dcea64fb8aa1cf43a0d0e0ceb4f34fc; `src/pipewire/keys.h` 02028b55b18aa5cc6ad1476b8f594ab0d63f5d8e9393084fe889cee62ebf9309; `src/daemon/systemd/user/pipewire.service.in` 758ffe661c516331e2e8106dbfe3dac8d51e729e76e854934c9b8832e65cc7c1; `src/daemon/systemd/user/pipewire-pulse.service.in` 2ffb6b2661064aafacc2c967de6e7ecd859ec2043242aa81c2bd21d863566b83; `meson.build` 2c9daecc71852dc9b1453ab5be71e5f413231791251330027f037c06155d3acb.

**Passages.** Clock/quantum defaults (mechanism) — `src/daemon/pipewire.conf.in:45-51`:
> `    #default.clock.rate          = 48000` / `    #default.clock.allowed-rates = [ 48000 ]` / `    #default.clock.quantum       = 1024` / `    #default.clock.min-quantum   = 32` / `    #default.clock.max-quantum   = 2048` / `    #default.clock.quantum-limit = 8192` / `    #default.clock.quantum-floor = 4`
Thread structure — `:27-30`: `    #loop.rt-prio = -1            # -1 = use module-rt prio, 0 disable rt` / `    #loop.class = data.rt` / `    #thread.affinity = [ 0 1 ]    # optional array of CPUs` / `    #context.num-data-loops = 1   # -1 = num-cpus, 0 = no data loops`
VM override — `:66`: `                default.clock.min-quantum = 1024`
module-rt as shipped (treatment fact) — `:123-131`: `    { name = libpipewire-module-rt` / `        args = {` / `            nice.level    = -11` / `            rt.prio       = @rtprio_server@` / `            #rt.time.soft = -1` / `            #rt.time.hard = -1` / `            #rlimits.enabled = true` / `            rtportal.enabled = false` / `            #rtkit.enabled = true`
`meson_options.txt:342-347`: `option('rtprio-server',` / `       description : 'PipeWire server realtime priority',` / `       type : 'integer',` / `       min: 11,` / `       max: 99,` / `       value: 88)`; `:348-353` `option('rtprio-client',` … `       value: 83)`; `:354-359` `option('rlimits-rtprio',` / `       description : 'RR and FIFO scheduler priority permitted for realtime threads of the matching user(s)',` / `       type : 'integer',` / `       min: 11,` / `       max: 99,` / `       value: 95)`; `:364-369` `option('rlimits-nice',` … `       value: -19)`; `:338-341` `option('rlimits-match',` / `       description : 'PAM match rule for the generated limits.d file. @<name> denotes matching a group.',` / `       type : 'string',` / `       value: '@pipewire')`
`src/modules/module-rt/25-pw-rlimits.conf.in:12-14`: `@MATCH@   - rtprio  @RTPRIO@` / `@MATCH@   - nice    @NICE@` / `@MATCH@   - memlock @MEMLOCK@`
`src/modules/module-rt.c:66-74`:
> ` * The `rt` modules can give real-time priorities to processing threads.` / ` *` / ` * It uses the operating system's scheduler to enable realtime scheduling` / ` * for certain threads to assist with low latency audio processing.` / ` * This requires `RLIMIT_RTPRIO` to be set to a value that's equal to this` / ` * module's `rt.prio` parameter or higher. Most distros will come with some` / ` * package that configures this for certain groups or users. If this is not set` / ` * up and DBus is available, then this module will fall back to using the Portal` / ` * Realtime DBus API or RTKit.`
`:84-89`: ` * - `rt.prio`: The realtime priority of the data thread. Higher values are` / ` *              higher priority.` / ` * - `rt.time.soft`, `rt.time.hard`: The amount of CPU time an RT thread can` / ` *              consume without doing any blocking calls before the kernel kills` / ` *              the thread. This is a safety measure to avoid lockups of the complete` / ` *              system when some thread consumes 100%.`; `:156-160`: `#define DEFAULT_NICE_LEVEL	20 	/* invalid value by default, see above */` / `#define DEFAULT_RT_PRIO_MIN	11` / `#define DEFAULT_RT_PRIO		RTPRIO_CLIENT` / `#define DEFAULT_RT_TIME_SOFT	-1` / `#define DEFAULT_RT_TIME_HARD	-1`
Graph driver and how it stops (mechanism) — `src/daemon/pipewire.conf.in:293-301`: `    # A default dummy driver. This handles nodes marked with the "node.always-process"` / `    # property when no other driver is currently active. JACK clients need this.` / `    { factory = spa-node-factory` / `        args = {` / `            factory.name    = support.node.driver` / `            node.name       = Dummy-Driver` / `            node.group      = pipewire.dummy` / `            node.sync-group  = sync.dummy` / `            priority.driver = 200000`; `spa/plugins/support/node-driver.c:210-221`:
> `static int set_timers(struct impl *this)` / `{` / `	this->next_time = gettime_nsec(this, this->timer_clockid);` / (blank) / `	spa_log_debug(this->log, "%p now:%"PRIu64, this, this->next_time);` / (blank) / `	if (this->following || !this->started) {` / `		set_timeout(this, 0);` / `	} else {` / `		set_timeout(this, this->next_time);` / `	}` / `	return 0;`
and `:555-561`: `static int do_stop(struct impl *this)` / `{` / `	if (!this->started)` / `		return 0;` / `	this->started = false;` / `	spa_loop_locked(this->data_loop, do_set_timers, 0, NULL, 0, this);` / `	return 0;` (a stopped driver disarms its timerfd — `set_timeout(this, 0)`).
Node suspension key — `src/pipewire/keys.h:191`: `#define PW_KEY_NODE_SUSPEND_ON_IDLE	"node.suspend-on-idle"	/**< suspend the node when idle */`; `src/daemon/minimal.conf.in:341`: `            node.suspend-on-idle   = true`
Units (treatment fact) — `src/daemon/systemd/user/pipewire.service.in:28`: `Slice=session.slice`; `src/daemon/systemd/user/pipewire-pulse.service.in:33`: `Slice=session.slice`.

**Coverage.** T2 — covers as mechanism: default graph rate 48000 Hz and quantum 1024 (32–2048, floor 4, limit 8192; min-quantum 1024 in a VM), one RT data-loop thread by default plus the main loop; the driver node's timerfd is disarmed when the driver is not started; `node.suspend-on-idle` marks nodes to be suspended (the timeout is WirePlumber's, S2-19). No CPU or wake numbers. T4 — treatment fact: server data thread `rt.prio` 88 (build default) with `nice.level` −11 for the daemon, clients 83; PAM limits file for group `@pipewire`: rtprio 95, nice −19, memlock 4194304 kB; fallback to portal/rtkit; `Slice=session.slice`. T1 — does not cover. **One observation?** No.

### S2-19 — WirePlumber (node suspend timeout)

**Citation.** WirePlumber 0.5.17 (`meson.build:2`: `  version : '0.5.17',`), commit 20704c4d0d909e8b1604f333129a7c3b90dfb764 (2026-09-15T04:00:01+03:00), https://gitlab.freedesktop.org/pipewire/wireplumber.git.

**Copy read.** local `sources/S2-19/`; SHA-256: `src/scripts/node/suspend-node.lua` 6ac2f7f2cfe739db462b1a9f10b580fd08339d6d15025dbab9060ce290bd09e6; `src/systemd/user/wireplumber.service.in` 8f12d8e81dd8db9e375817721cdbad4384bc722497f95e8de65da2666123b427; `meson.build` 9cdd18124f2a3b7ab5c7f62e477e47db9810d5b95310ec69b4e91ced7748a07b.

**Passages.** `src/scripts/node/suspend-node.lua:37-48`:
> `    -- Add a timeout source if idle for at least 5 seconds` / `    if new_state == "idle" or new_state == "error" then` / `      -- honor "session.suspend-timeout-seconds" if specified` / `      local timeout =` / `          tonumber(node.properties["session.suspend-timeout-seconds"]) or 5` / (blank) / `      if timeout == 0 then` / `        return` / `      end` / (blank) / `      -- add idle timeout; multiply by 1000, timeout_add() expects ms` / `      sources[id] = Core.timeout_add(timeout * 1000, function()`
`:51-53`: `        if (node:get_active_features() & Feature.Proxy.BOUND) ~= 0 then` / `          log:info(node, "was idle for a while; suspending ...")` / `          node:send_command("Suspend")`
Unit — `src/systemd/user/wireplumber.service.in:16`: `Slice=session.slice`.

**Coverage.** T2 — covers as mechanism: an Audio/* or Video/* node that becomes idle is sent `Suspend` after 5 s (`session.suspend-timeout-seconds`, 0 disables). T4 — treatment fact: `Slice=session.slice`. T1 — does not cover. **One observation?** No.

### S2-20 — PulseAudio (module-suspend-on-idle, daemon.conf RT defaults, unit)

**Citation.** PulseAudio, NEWS heading `PulseAudio 17.0` (development tree after 17.0), commit 77d25a1e613095bdf87a1d13b65e7c330565077a (2026-09-01T12:09:07-07:00), https://gitlab.freedesktop.org/pulseaudio/pulseaudio.git.

**Copy read.** local `sources/S2-20/`; SHA-256: `src/modules/module-suspend-on-idle.c` 2201cb1a27eaf3df8394ad83c1fae2cbe08b31982259cdde0a7639966bcd4cfa; `src/daemon/daemon.conf.in` bbf56058a8c339270c490098cc6f6d90fe20d9c0bc1eeac612d455b644c19001; `src/daemon/daemon-conf.c` 15ba21d02da74e1320b6db716378f62ce15445f9724c2f9f5f4af8cdd4a123c7; `src/daemon/default.pa.in` 2a92b7d0bc0027a78889602d72ff4c88f24d62d94da1d87bfe578a83b8416803; `src/daemon/systemd/user/pulseaudio.service.in` 3c2a33c1114e3ec0f2923333baa07dde9f394fe8e119d1f9b00f5ccdff00a9de; `NEWS` 9662af3ecd88ff572447efd2921bf22a40fe7ffbcc3dbeb86d521c0625f32087.

**Passages.** `src/modules/module-suspend-on-idle.c:421`: `    uint32_t timeout = 5;`; `:433`: `    if (pa_modargs_get_value_u32(ma, "timeout", &timeout) < 0) {`; `src/daemon/default.pa.in:143`: `load-module module-suspend-on-idle`.
`src/daemon/daemon.conf.in:36-40`: `; high-priority = yes` / `; nice-level = -11` / (blank) / `; realtime-scheduling = yes` / `; realtime-priority = 5`
`src/daemon/daemon-conf.c:140`: `   ,.rlimit_nice = { .value = 31, .is_set = true }     /* nice level of -11 */`; `:143`: `   ,.rlimit_rtprio = { .value = 9, .is_set = true }    /* One below JACK's default for the server */`; `:146`: `   ,.rlimit_rttime = { .value = 200*PA_USEC_PER_MSEC, .is_set = true } /* rtkit's limit is 200 ms */`
Unit — `src/daemon/systemd/user/pulseaudio.service.in:31`: `Slice=session.slice`.

**Coverage.** T2 — covers as mechanism: sinks/sources are suspended after 5 s idle by default. T4 — treatment fact: daemon defaults nice −11, realtime scheduling on at RT priority 5, self-imposed rlimits (RTPRIO 9, RTTIME 200 ms, NICE 31); `Slice=session.slice`. T1 — does not cover. **One observation?** No.

### S2-21 — rtkit (RealtimeKit daemon: limits, canary/watchdog, unit)

**Citation.** RealtimeKit 0.14 (`meson.build:3`: `        version: '0.14',`), tag v0.14 = commit c52db0a9849908613ab8775b519834671b7bec8b (2025-12-10T14:48:07-08:00), https://gitlab.freedesktop.org/pipewire/rtkit.git (the location Fedora's rtkit.spec names; the older mirror https://github.com/heftig/rtkit at c295fa849f52b487be6433e69e08b46251950399, version 0.13, carries the same default values at line numbers four less).

**Copy read.** local `sources/S2-21/`; SHA-256: `rtkit-daemon.c` 0ec8230c7e382db5a62454c162d3ca95c5077b457c9b5f8feee06bd211a208be; `rtkit-daemon.service.in` 0f5b1bb7d14471100ffda24bca7b19dd64402ab8d792d9e9772d32a64220a9fe; `meson.build` 585dd4796fe98db542fa556120ff979292821182a52c10fc55f6df2dd9e23b5c.

**Passages (treatment facts and mechanism).** `rtkit-daemon.c:96`: `static unsigned our_realtime_priority = 21;`; `:99`: `static int our_nice_level = 1;`; `:102`: `static unsigned max_realtime_priority = 20;`; `:105`: `static int min_nice_level = -15;`; `:111`: `static unsigned long long rttime_usec_max = 200000ULL; /* 200 ms */`; `:114`: `static unsigned users_max = 2048;`; `:117`: `static unsigned processes_per_user_max = 15;`; `:120`: `static unsigned threads_per_user_max = 25;`; `:123`: `static unsigned actions_burst_sec = 20;`; `:126`: `static unsigned actions_per_burst_max = 25;`; `:141`: `static unsigned canary_cheep_msec = 5000; /* 5s */`; `:144`: `static unsigned canary_watchdog_msec = 10000; /* 10s */`; `:147`: `static unsigned canary_watchdog_realtime_priority = 99;`; `:150`: `static unsigned canary_refusal_sec = 5*60;`; `:165`: `static int sched_policy = SCHED_RR;`
Unit — `rtkit-daemon.service.in:22-23,26`: `ExecStart=@LIBEXECDIR@/rtkit-daemon` / `Type=dbus` … `CapabilityBoundingSet=CAP_SYS_NICE CAP_DAC_READ_SEARCH CAP_SYS_CHROOT CAP_SETGID CAP_SETUID`

**Coverage.** T1 — covers as mechanism: rtkit-daemon (a system service) runs a canary thread that signals every 5 s and a watchdog thread at RT priority 99 that, if no signal arrives within 10 s, demotes the RT threads it granted and refuses requests for 300 s — a periodic wake even at idle when the daemon is running (it is D-Bus activated: `Type=dbus`). T2 — covers as mechanism the limits that bound what compositors/audio servers obtain through rtkit: max RT priority 20, min nice −15, `RLIMIT_RTTIME` ≤ 200 ms required, policy SCHED_RR, at most 15 processes / 25 threads per user. T4 — the same values as treatment facts. **One observation?** No.

### S2-22 — Weston (repaint window, idle time, sleep state)

**Citation.** Weston 16.0.90 (`meson.build:3`: `	version: '16.0.90',`), commit 46298ecc7e7ca393567d431a562ba1ce3eeed04b (2026-09-15T16:18:05+01:00), https://gitlab.freedesktop.org/wayland/weston.git; `man/weston.ini.man` is the source of weston.ini(5).

**Copy read.** local `sources/S2-22/`; SHA-256: `libweston/compositor.c` 6a95eeaab3aef20a746df3eb665811c483945c0a99641ee79bc265dc6f4f897b; `frontend/main.c` 3deae82338493d9beff1e552919f634a8233383013fe4475c35e4704e77190c3; `man/weston.ini.man` cc2911a37501c114498520bf59eac22f5f3d1eeb456ca85c83f7e9d1e434467b; `meson.build` f2f1394ab8961af9ecc843baf3312353bf55388be1254c999107f9a76b2fc969.

**Passages.** `libweston/compositor.c:110`: `#define DEFAULT_REPAINT_WINDOW 7 /* milliseconds */`; `:4281-4282`: `	/* repaint_msec is, roughly speaking, the amount of time the compositor` / `	 * reserves before presentation to complete a repaint.`; `:4294-4298`: `	 * To avoid this forced latency, always ensure that repaint_msec is` / `	 * at least 1ms shorter than the refresh duration.` / `	 */` / `	if (repaint_msec > refresh_msec)` / `		repaint_msec = refresh_msec - 1;`
Idle/sleep — `:4243-4247`: `	/* If we're sleeping, drop the repaint machinery entirely; we will` / `	 * explicitly repaint all outputs when we come back. */` / `	if (compositor->state == WESTON_COMPOSITOR_SLEEPING ||` / `	    compositor->state == WESTON_COMPOSITOR_OFFSCREEN)` / `		goto out;`
`frontend/main.c:5202-5205`: `	if (idle_time < 0)` / `		weston_config_section_get_int(section, "idle-time", &idle_time, -1);` / `	if (idle_time < 0)` / `		idle_time = 300; /* default idle timeout, in seconds */`
`man/weston.ini.man:143-146`: `.BI "idle-time="seconds` / `sets Weston's idle timeout in seconds. This idle timeout is the time` / `after which Weston will enter an "inactive" mode and screen will fade to` / `black. A value of 0 disables the timeout.`

**Coverage.** T2 — covers as mechanism: repaint is scheduled 7 ms (clamped to refresh − 1 ms) before the target presentation; the repaint machinery is dropped entirely while the compositor sleeps; the idle timeout is 300 s by default. T1, T4 — do not cover. **One observation?** No.

### S2-23 — V. Zahorodnii, "Compositing Scheduling in KWin: Past, Present, and Future" (blog, 2020-12-10)

**Citation.** Vlad Zahorodnii, *Compositing Scheduling in KWin: Past, Present, and Future*, blog post dated December 10, 2020, https://blog.vladzahorodnii.com/2020/12/10/compositing-scheduling-in-kwin-past-now-and-future/ (the page title reads "Past, Present, and Future"; the slug reads "past-now-and-future").

**Copy read.** HTTP 200, saved as `sources/S2-23/kwin-compositing-scheduling.html` (SHA-256 a196a3d91f3491627da3c7728f3ad7f8f6c12838b4358d530949b68a28b5e02a); article text extracted by the reader (tags stripped, one paragraph per line) to `sources/S2-23/kwin-compositing-scheduling.txt` (SHA-256 fbe08f2f3b6a76a074e60bff6e39c8ff399123a109ba94649df3b3613f042761); locators below are paragraph numbers in that extraction, counted from the title (`txt:1`).

**Passages.** `txt:4` (section "Past & Present"): `With the current scheduling algorithm, compositing /should/ start immediately right after a vblank. A vblank is the time between the vertical front porch and the vertical back porch, or simply put, it’s the time when the display starts scanning out the contents of the next frame.`. `txt:10`: `With the current compositing timing, if you press a key on the keyboard, it may take up to two frame before the corresponding symbol shows up on the screen. Same thing with videos, the audio might be playing two frames ahead of what is on the screen.` `txt:16` (section "Future"): `If we start compositing as close as possible to the next vblank, then applications, such as video players, will be able to get their contents on the screen in the shortest amount of time without inducing any screen tearing.` `txt:18`: `The main idea behind the compositing timing rework is to introduce a new class, called RenderLoop, that notifies the compositor when it’s a good time to start painting the next frame. On X11, there is going to be only one RenderLoop. On Wayland, every output is going to have its own RenderLoop.` `txt:20-22`: `The first guess is based on a desired latency level that comes from a config. If the desired latency level is high, the predicted render time will be longer; on the other hand, if the desired latency level is low, the predicted render time will be shorter;` / `The second guess is based on the duration of previous compositing cycles.` / `The RenderLoop makes two guesses and the one with the longest render time is used for scheduling compositing for the next frame. By making two estimates rather than one, hopefully, animations will be more or less stable.` `txt:24`: `The introduction of the RenderLoop helper is only half of the battle. At the moment, all compositing is done on the main thread and it can get crowded. For example, if you have several outputs with different refresh rates, some of them will have to wait until it’s their turn to get repainted. This may result in missed vblanks, and thus laggy frames. In order to address this issue, we need to put compositing on different threads. That way, monitors will be repainted independently of each other. There is no concrete milestone for compositing on different threads, but most likely, it’s going to be KDE Plasma 5.22.`

**Coverage.** T2 — covers as a description of the compositor schedule (start-of-compositing relative to vblank, render-time prediction from a latency setting and past cycle durations, one RenderLoop per output on Wayland, compositing on the main thread as of 2020). It states **no** per-frame CPU cost, no CPU share and no wake cadence; it gives no measurement. T1, T4 — do not cover. **One observation?** No (a design description; no machine, subject or window).

### S2-24 — J. Ådahl, "Splitting up the Frame Clock" (GNOME Shell & Mutter blog, 2020-07-02)

**Citation.** Jonas Ådahl, *Splitting up the Frame Clock*, GNOME Shell & Mutter development blog, posted July 2, 2020, https://blogs.gnome.org/shell-dev/2020/07/02/splitting-up-the-frame-clock/.

**Copy read.** HTTP 200, saved as `sources/S2-24/splitting-up-the-frame-clock.html` (SHA-256 71d53c6cf69dae9fd7e5ac0605428e608a08b88b438889639ca00a23570737e9); reader's text extraction `sources/S2-24/splitting-up-the-frame-clock.txt` (SHA-256 a16146c6d8e7c646fab0c093e42567990a9bedcbf9f6d5d3766dac74c1945723), paragraph numbers as locators (`txt:1` is the "Posted on" line, `txt:2` the title).

**Passages.** `txt:4`: `Not too long ago mutter saw a merge request land, that has one major aim: split up the frame clock so that when using the Wayland session, each monitor is driven by its own frame clock. In effect the goal here is that e.g. a 144 Hz monitor and a 60 Hz monitor being active in the same session will not have to wait for each other to update, and that the space they occupy on the screen will draw at their own pace. A window on the 144 Hz monitor will paint at 144 Hz, and mutter will composite to the monitor at 144 Hz, while a window on the 60 Hz monitor will paint at 60 Hz and Mutter will composite to the monitor at 60 Hz.` `txt:15`: `ClutterFrameClock is the new frame clock object that aims to drive a single “output”. Right now, it has a fixed refresh rate, and a single “frame listener” and “presenter” notifying about frames being presented. It is also possible to have multiple frame clocks running in parallel.`. `txt:22`: `The frame scheduling related logic (including flip counting, schedule time calculation, etc) was spread out in ClutterMasterClockDefault, ClutterStage, ClutterStageCogl, MetaRendererNative, MetaStageNative, and MetaStageX11, but has now now been concentrated to ClutterFrameClock and ClutterStageView alone.` `txt:29` (section "What About X11?"): `In the X11 session, we composite the whole X11 screen at once, without any separation between monitors. This remains unchanged, with the difference being where scheduling takes place (as mentioned in an earlier point). The improvements described here are thus limited to using the Wayland session.`

**Coverage.** T2 — covers as a description of Mutter's frame clock (one clock per monitor on Wayland, a single one for X11; animations/timelines attach to the clock of the view they are on). It states **no** per-frame CPU cost, no idle behaviour numbers and no measurement. T1, T4 — do not cover. **One observation?** No.

### S2-25 — wlroots (output frame scheduling)

**Citation.** wlroots 0.21.0-dev (`meson.build:4`: `	version: '0.21.0-dev',`), commit aef1af2718687cba2acc87d932592409776656f5 (2026-09-17T15:14:57+08:00), https://gitlab.freedesktop.org/wlroots/wlroots.git.

**Copy read.** local `sources/S2-25/`; SHA-256: `types/output/output.c` e8e56c36dd523ab025534bc6eb52502cc094797ec3224c7df5b5e07346e1d1de; `meson.build` 21d6a0ae5b05fb26f203530a6acfbddd28fea3af43680d658f5eebc5654c193c.

**Passages.** `types/output/output.c:862-876`:
> `void wlr_output_schedule_frame(struct wlr_output *output) {` / `	// Make sure the compositor commits a new frame. This is necessary to make` / `	// clients which ask for frame callbacks without submitting a new buffer` / `	// work.` / `	wlr_output_update_needs_frame(output);` / (blank) / `	if (output->frame_pending || output->idle_frame != NULL) {` / `		return;` / `	}` / (blank) / `	// We're using an idle timer here in case a buffer swap happens right after` / `	// this function is called` / `	output->idle_frame = wl_event_loop_add_idle(output->event_loop,` / `		schedule_frame_handle_idle_timer, output);` / `}`
`:847-852`: `void wlr_output_send_frame(struct wlr_output *output) {` / `	output->frame_pending = false;` / `	if (output->enabled) {` / `		wl_signal_emit_mutable(&output->events.frame, NULL);` / `	}` / `}`

**Coverage.** T2 — covers as mechanism: wlroots emits an output `frame` event only when a frame is scheduled (on demand, or by the backend after a page flip); no periodic clock of its own and no timing constant. Sway itself was not read. T1, T4 — do not cover. **One observation?** No.

### S2-26 — CachyOS ananicy-rules (process-treatment catalogue)

**Citation.** CachyOS, *ananicy-rules* ("Ananicy-cpp-rules for CachyOS"), commit 03ef03fbf7e834385377432ccecaedd32e3414bb (2026-09-08T19:11:25-03:00), https://github.com/CachyOS/ananicy-rules.

**Copy read.** local `sources/S2-26/`; SHA-256: `00-types.types` 667d89cb61a949ac9b6595f2f318dc452b65c735d8cd6d4fcd5f934dc940591d; `ananicy.conf` dd02bfc0c62fdc12b7c5cfc3efc6587a12087158ad0782e5416e08dd8537a0ed; `00-cgroups.cgroups` ab78e8b36d6c7c5f1e347df552edfb2d7073e41ef8e0a1f484ff93afb994e67a; `README.md` 0886ec1f23a1ef772e676ba65bc13961ce7942bec6e0dc9d0936a4f60b16b7ed; `00-default/DEs-and-WMs/gnome.rules` 4cd43aab6cd3170348c0d36d53195cef6b9ef884b6cc101c1c2c324f879fce23; `00-default/DEs-and-WMs/gdm.rules` 123bf9b34befff56e0301bcaf6aa63b496644f2092aa9358f58ddbdbadb19b72; `00-default/DEs-and-WMs/plasma.rules` 090a8f88fb82a3be2699d762d431f80814e4bb466a8ea1ea467039001cc56800; `00-default/DEs-and-WMs/sway.rules` 1df2005c17a015745f55eba418cc420342da7644b2241430f6b1983d8726ea9b; `00-default/DEs-and-WMs/xorg.rules` 6654e3d96a1fc6f4f14dcbf25021abfe186e05bf1017d1163fe4ebb60ceeb61d; `00-default/DEs-and-WMs/xwayland.rules` a835ba440fda657d4a7ecc082f9bbc328833703e21d55c4b57aa3a6c141bea65; `00-default/Audio-Video/audioserver.rules` 3b8b4a9d6f52298e7f9ac738615909846932645ec9af2edf9ed4c8b1baa41bd5; `00-default/Services/dbus.rules` 6031e0c59e3c7c51d403c45bd4f48c0df33d164d3d1386bd9b086935a6830d00; `00-default/Services/misc-services.rules` c32f7c7e56058993441ee52ce44ea0815f7aa1ac7104eb49c611329f82ba2712; `00-default/Services/networkmanager.rules` 9b76cc845b79e3b669557e6de848467e09b0fbd3bac2df28af06b766abca8d4e; `00-default/Tools/chrony.rules` 7b6d90160949cf04db0def7f608f7066c7469e7fad558a0a5a9ac700dd011ca2.

**Passages (all treatment facts).** Types — `00-types.types:16-18`: `# Type: Low Latency Realtime Apps` / `# In general case not so heavy, but must not lag` / `{ "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }`; `:20-22`: `# Type: BackGround CPU/IO Load` / `# Background CPU/IO it's needed, but it must be as silent as possible` / `{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }`; `:27-29`: `# Type: Background Launcher` / `# Runs quietly but may spawn foreground or latency-sensitive workloads` / `{ "type": "Launcher", "nice": 16, "ioclass": "idle", "sched": "normal" }`; `:38-39`: `# Type: Service` / `{ "type": "Service", "nice": 10, "ioclass": "best-effort", "ionice": 6 }`.
Rules — `00-default/DEs-and-WMs/gdm.rules:7-8`: `# gnome shell` / `{ "name": "gnome-shell","type": "LowLatency_RT"}`; `:9-10`: `{ "name": "gnome-session-binary","type": "Launcher"}` / `{ "name": "gnome-session-ctl","type": "BG_CPUIO"}`; `:2-3`: `{ "name": "gdm3", "type": "BG_CPUIO" }` / `{ "name": "gdm", "type": "BG_CPUIO" }`. `00-default/DEs-and-WMs/gnome.rules:88-89`: `# mutter-x11-frames` / `{ "name": "mutter-x11-frames", "type": "LowLatency_RT" }`; `:34-35`: `# gsd-power` / `{ "name": "gsd-power", "type": "Service" }` (the other gsd-* entries at `:16-80` are all `"type": "Service"`). `00-default/DEs-and-WMs/plasma.rules:26-29`: `{ "name": "kwin_wayland", "type": "LowLatency_RT" }` / `{ "name": "kwin_wayland_wrapper", "type": "LowLatency_RT" }` / `{ "name": "kwin_x11", "type": "LowLatency_RT" }` / `{ "name": "plasmashell", "nice": -6 }`. `00-default/DEs-and-WMs/sway.rules:2`: `{ "name": "sway", "type": "LowLatency_RT" }`. `00-default/DEs-and-WMs/xorg.rules:1-2`: `# Rule for Xorg server, runs the graphical desktop.` / `{ "name": "Xorg", "type": "LowLatency_RT" }`. `00-default/DEs-and-WMs/xwayland.rules:1`: `{ "name": "Xwayland", "type": "LowLatency_RT" }`. `00-default/Audio-Video/audioserver.rules:1-4`: `{ "name": "pipewire", "type": "LowLatency_RT" }` / `{ "name": "pipewire-pulse", "type": "LowLatency_RT" }` / `{ "name": "wireplumber", "type": "LowLatency_RT" }` / `{ "name": "pulseaudio", "type": "LowLatency_RT" }`. `00-default/Services/dbus.rules:3-5`: `{ "name": "dbus-daemon", "type": "Service" }` / `{ "name": "dbus-broker", "type": "Service" }` / `{ "name": "dbus-broker-launch", "type": "Service" }`. `00-default/Services/misc-services.rules:10`: `{ "name": "udisksd", "type": "Service" }`. `00-default/Services/networkmanager.rules:2`: `{ "name": "NetworkManager", "type": "BG_CPUIO" }`. `00-default/Tools/chrony.rules:2`: `{ "name": "chronyd", "type": "BG_CPUIO" }`.
Daemon cadence — `ananicy.conf:2-5`: `# Ananicy run full system scan every "check_freq" seconds` / `# supported values 0.01..86400` / `# values which have sense: 1..60` / `check_freq = 15`. Cgroups — `00-cgroups.cgroups:4-8`: `# cpuquota same as systemd CPUQuota,` / `# only difference is - meaning of N% is all CPUs, not one core.` / `{ "cgroup": "cpu90", "CPUQuota": 90 }` / `{ "cgroup": "cpu85", "CPUQuota": 85 }` / `{ "cgroup": "cpu80", "CPUQuota": 80 }`.
Absent: no rule names `mutter`, `systemd*` (any systemd daemon), `cron`/`crond`, `polkitd`, `packagekitd`, `rsyslogd` or `multipathd` in `00-default/` (search-log row 71).

**Coverage.** T4 — covers, as treatment facts: nice −12 best-effort for gnome-shell, kwin_wayland, kwin_x11, sway, Xorg, Xwayland, pipewire, pipewire-pulse, wireplumber, pulseaudio, mutter-x11-frames; nice −6 for plasmashell; nice 10 / ionice 6 for dbus-daemon, dbus-broker, udisksd and the gsd-* helpers; nice 16 / idle io / SCHED_IDLE for NetworkManager, chronyd, gdm and gnome-session-ctl; nothing for systemd's daemons, cron, polkitd, packagekitd, rsyslogd, multipathd. The carried timing value is the 15 s rescan period of ananicy-cpp. T1, T2 — do not cover. **One observation?** No.

### S2-27 — Fedora packaging (systemd, pipewire, rtkit, gnome-shell spec files, rawhide)

**Citation.** Fedora Project, dist-git `rpms/systemd`, `rpms/pipewire`, `rpms/rtkit`, `rpms/gnome-shell`, branch `rawhide`, raw spec files fetched 2026-09-20 (no commit id is exposed by the raw URL; versions as stated inside each file).

**Copy read.** `https://src.fedoraproject.org/rpms/systemd/raw/rawhide/f/systemd.spec` → `sources/S2-27/systemd.spec` (SHA-256 8607830255c0518025c8faaae192a492e9774be09105cac4525032b50a9323f7; `systemd.spec:88`: `Version:        %{?version_override}%{!?version_override:262~rc3}`); `https://src.fedoraproject.org/rpms/pipewire/raw/rawhide/f/pipewire.spec` → `pipewire.spec` (SHA-256 f7a7466e8ac03a1869a0c6d6f2e48c274a4e16420ae6a37e2398f3e59192e67c; `:1-3`: `%global majorversion 1` / `%global minorversion 6` / `%global microversion 9`); `https://src.fedoraproject.org/rpms/rtkit/raw/rawhide/f/rtkit.spec` → `rtkit.spec` (SHA-256 c09cb691813948cf95e790281f6b03c4f456e81482dd163f7c3c3ebf602a2838; `:2`: `Version:          0.14`); `https://src.fedoraproject.org/rpms/gnome-shell/raw/rawhide/f/gnome-shell.spec` → `gnome-shell.spec` (SHA-256 b7ef07a758816872ccf500949686e036969c33ba07b449eb7c3bebc353a23a07; `:25`: `Version:        51.0`).

**Passages.** `systemd.spec:898`: `        -Dservice-watchdog=` (inside `CONFIGURE_OPTS=(` at `:893`). `pipewire.spec:481`: `    -D rtprio-server=60 -D rtprio-client=55 -D rlimits-rtprio=70		\`; `:602`: `%config(noreplace) %{_sysconfdir}/security/limits.d/*.conf`; `:144`: `Requires:       rtkit`. `rtkit.spec:8-11`: `%define forgeurl https://gitlab.freedesktop.org/pipewire/rtkit` / `%define tag v%{version}` / `%forgemeta` / `URL:              %{forgeurl}`; `:26`: `Patch:            remove-debug-messages.patch` (the only patch). `gnome-shell.spec`: no line matching `slice|Slice|CPUWeight|nice` (search-log row 72).

**Coverage.** T1 — covers as mechanism: Fedora builds systemd with the service watchdog disabled (`-Dservice-watchdog=` empty → no `WatchdogSec=` in journald/logind/resolved/… units, hence no keep-alive pings), against the upstream default of 3min (S2-01). T4 — treatment facts: Fedora's PipeWire is built with server RT priority 60, client 55 and a PAM `limits.d` rtprio of 70 (against upstream 88/83/95); rtkit is packaged unpatched from upstream v0.14 (so S2-21's limits apply); Fedora's gnome-shell spec adds no slice/nice settings. T2 — does not cover. **One observation?** No.

### S2-28 — Debian and Ubuntu packaging (systemd debian/rules; gnome-shell debian/ tree)

**Citation.** Debian systemd team, `debian/rules` of the `systemd` package, branch `debian/master`, https://salsa.debian.org/systemd-team/systemd/-/raw/debian/master/debian/rules (fetched 2026-09-20, HTTP 200); Ubuntu `gnome-shell` source package, `debian/rules` and the `debian/` tree listing, https://git.launchpad.net/ubuntu/+source/gnome-shell/plain/debian/rules and https://git.launchpad.net/ubuntu/+source/gnome-shell/tree/debian (HTTP 200; no commit id exposed by these URLs).

**Copy read.** `sources/S2-28/debian-systemd-rules` (SHA-256 7662d5079bf22dc0a30e4f48326fbaf4523e854e9bc42631e6038320b7fc613f); `sources/S2-28/ubuntu-gnome-shell-debian-rules` (SHA-256 4535fe01d3b4d9dee2b3001006c89ec87116d7c1cf0bd78fe5586c8f1f25fc07); `sources/S2-28/ubuntu-gnome-shell-debian-tree.html` (SHA-256 03033339c3f2f291d972620c80676118a194e71edbe59f66545fedef8cfd80a4).

**Passages.** Negative findings only (the reader's own grep, search-log rows 35, 73): the Debian systemd `debian/rules` contains no line matching `watchdog` or `Dservice`; the Ubuntu gnome-shell `debian/rules` configures with `-Dnetworkmanager=true \` / `-Dsystemd=true` (`ubuntu-gnome-shell-debian-rules:12-13`) and the `debian/` listing contains no `*.service`, `*.slice`, `*.conf` drop-in or `*.override` file (entries are: README.Ubuntu, changelog, clean, control, copyright, gbp.conf, gnome-shell-common.*, gnome-shell.bug-control, gnome-shell.docs, gnome-shell.gsettings-override, gnome-shell.install, gnome-shell.lintian-overrides, gnome-shell.maintscript, gnome-shell.postinst, patches, rules, salsa-ci.yml, shlibs.local, source, source_gnome-shell.py, tests, ubuntu-session-mods, upstream, watch, plus release-name directories).

**Coverage.** T1 — indirectly: with no `-Dservice-watchdog` override in Debian's rules, the upstream default (`WatchdogSec=3min`, S2-01) is the reader's inference for Debian/Ubuntu builds, not a stated fact in the file (Debian may set it elsewhere, e.g. in a patch; not checked). T4 — Ubuntu's gnome-shell packaging ships no `CPUWeight=`/`Nice=`/slice override visible in its `debian/` tree; nothing on session-scope `CPUWeight=` defaults was found. T2 — does not cover. **One observation?** No.

## 3. Not found

Topics or sub-questions for which this class produced no candidate, with the searches that established it (row numbers refer to the search log):

- **T1, any Linux observation of per-service wake cadence, CPU per wake or CPU share at idle.** None exists in project documentation or source by construction of the class; every T1 candidate above is a mechanism. Not searched outside primary sources (that is S1/S3's remit).
- **T1, systemd-udevd idle behaviour in its man pages.** `man/udev.conf.xml` and `man/systemd-udevd.service.xml` document `event_timeout=`, `exec_delay=`, `children_max=`, `timeout_signal=` only; the 3 s idle-worker cleanup comes from source (row 47).
- **T1, systemd-resolved cache lifetime in documentation.** `resolved.conf(5)` and `systemd-resolved.service(8)` sources describe `Cache=` but state no TTL; the 2 h cap is a source constant (row 48).
- **T1, systemd-networkd idle activity.** Not searched beyond confirming its unit carries the `{{SERVICE_WATCHDOG}}` placeholder (row 45); no interval is documented in the man page tree that was grepped.
- **T1, polkitd idle behaviour and thread structure.** polkit 125 clone grepped for timeouts/idle timers in `src/polkitbackend/` — no hit (rows 20, 74); no candidate.
- **T1, dbus-daemon thread structure and idle activity.** `dbus-daemon(1)` source states neither (row 52); only limits/timeouts recorded (S2-04).
- **T1, NetworkManager thread structure.** Not stated in `NetworkManager.conf(5)`; source not grepped for threads (row 58).
- **T1, rsyslogd idle timers.** Only main-queue worker defaults found (row 57); no periodic timer documented in the file read.
- **T2, any measurement of a compositor's per-frame CPU cost, wake cadence or CPU share per state.** Neither Mutter, KWin, Weston, wlroots sources nor the two blog posts (S2-23, S2-24) state any such number (rows 27, 28, 59, 62, 69, 70).
- **T2, GNOME screen-blank timing.** Delegated by gnome-shell to gnome-settings-daemon (`org.gnome.settings-daemon.plugins.power.sleep-display-ac/-battery`, S2-13 passage); the gnome-settings-daemon repository was not cloned, so the blank delay default is not recorded here.
- **T2, `MUTTER_DEBUG_DUMMY_MODE_SPECS` as a documented mechanism.** Found only as a CI variable (`.gitlab-ci.yml:516`), not in Mutter's source or docs at this commit (row 59).
- **T2, Sway itself.** Only wlroots was read (S2-25); Sway's repository was not cloned.
- **T2, PipeWire thread priority as actually granted through rtkit on a given distribution.** Only the requested values (S2-18) and rtkit's caps (S2-21) are recorded; the effective priority (min of the two) is an inference, not a stated value.
- **T4, distribution-shipped `Nice=`, `CPUWeight=`, `CPUSchedulingPolicy=`, `IOSchedulingClass=` for the named services.** Upstream units of systemd, dbus, dbus-broker, PipeWire, WirePlumber, PulseAudio, rtkit, gnome-shell, kwin, NetworkManager, chrony, udisks, polkit, rsyslog, cronie, PackageKit were grepped (rows 45, 52, 53, 58, 62, 65-68 and the cross-clone unit grep): the only hits are `OOMScoreAdjust=` (journald −250, udevd −1000, oomd −900, dbus/dbus-broker system −900, gnome-shell −1000), `IOSchedulingClass=idle` (systemd-tmpfiles-clean), `CPUWeight=1000`/`LimitRTPRIO=10` (multipathd), and `Slice=session.slice` (gnome-shell, kwin_wayland, pipewire, pipewire-pulse, wireplumber, pulseaudio, user dbus, user dbus-broker). No `Nice=` or `CPUSchedulingPolicy=` for any of these daemons; no `CPUWeight=` on session scopes in Fedora's or Ubuntu's gnome-shell packaging (rows 31, 36, 38, 72, 73).
- **T4, Debian rtkit packaging.** salsa raw URL returned a sign-in page (row 33); not recorded.
- **T4, the GLib mechanism that places launched applications into `app-*.scope` under `app.slice`.** `gio/gdesktopappinfo.c` at GLib main (row 39) contains no `app.slice`/`StartTransientUnit` text; the code has evidently moved and was not located in this session.
- **Unreachable or not served:** `https://src.fedoraproject.org/rpms/rtkit/raw/rawhide/f/rtkit-daemon.service` (404, row 32); `https://salsa.debian.org/utopia-team/rtkit/-/raw/debian/master/debian/patches/series` (200 but GitLab sign-in HTML, row 33). All git remotes and the two blog hosts were reachable.

## 5. Retry from the development machine (2026-09-22)

Read during stage 3 to settle whether an idle GNOME 46 session runs an X server. Copies in `sources/retry-2026-09-22/` (local, gitignored).

| # | date | engine | URL | status | copy (SHA-256) |
|---|---|---|---|---|---|
| R1 | 2026-09-22 | `curl` | `https://gitlab.gnome.org/GNOME/mutter/-/raw/46.2/src/core/meta-context-main.c` | 200 | `mutter-46.2-src_core_meta-context-main.c` `a559e0b970c23f9f04fce303d1077f2ec9d20196d685b61c2aae0830a6b4d2d7` (the same file S4-08 read) |
| R2 | 2026-09-22 | `curl` | `https://gitlab.gnome.org/GNOME/mutter/-/raw/46.2/data/org.gnome.mutter.gschema.xml.in` | 200 | `mutter-46.2-data_org.gnome.mutter.gschema.xml.in` `e950c02788bd6bd9886ad46ce6c9ccd45fa245d4b676e1f1b0433109ad449006` |
| R3 | 2026-09-22 | `curl` | `https://gitlab.gnome.org/GNOME/gnome-shell/-/raw/46.0/data/org.gnome.Shell@wayland.service.in` | 200 | `gnome-shell-46.0-org.gnome.Shell@wayland.service.in` `0b3ce9179c6ab60dd1e12b4d4223899bb056cdce995da8d2de29859888d1f40e` |
| R4 | 2026-09-22 | `curl` | `https://git.launchpad.net/ubuntu/+source/gdm3/plain/data/61-gdm.rules.in?h=ubuntu/noble-updates` | 200 | `gdm3-noble-updates-61-gdm.rules.in` `b1db35a79d951fc21210c1850154500cea9f7d244335fd130df54040f9907f00` |
| R5 | 2026-09-22 | `curl` | `…/gdm3/plain/debian/custom.conf?h=ubuntu/noble-updates` (and `debian/default.conf`, `data/custom.conf`) | 404 | — ; the shipped `custom.conf` was not read |
| R6 | 2026-09-22 | `curl` | `https://raw.githubusercontent.com/systemd/systemd/v255/units/user%40.service.in` | 200 | `systemd-v255-user@.service.in` `0b0147ccd524ae37b8dd37979f0007997574dd6ed690bf772c49ab901f19f616` (S2-29) |
| R7 | 2026-09-22 | `api.launchpad.net` | `getPublishedBinaries` for `systemd`, noble amd64, Published | 200 | not saved; versions `255.4-1ubuntu8` (Release), `255.4-1ubuntu8.17` (Security, Updates) |

### S2-28 — Mutter 46.2's X11 display policy and GNOME Shell 46.0's Wayland unit: Xwayland on demand

**Citation.** GNOME Mutter 46.2, `src/core/meta-context-main.c` and `data/org.gnome.mutter.gschema.xml.in`, tag `46.2`, https://gitlab.gnome.org/GNOME/mutter; GNOME Shell 46.0, `data/org.gnome.Shell@wayland.service.in`, tag `46.0`, https://gitlab.gnome.org/GNOME/gnome-shell; Ubuntu `gdm3` source package, `data/61-gdm.rules.in`, branch `ubuntu/noble-updates`, https://git.launchpad.net/ubuntu/+source/gdm3.

**Passages.**
- `meta-context-main.c:333-353`: `meta_context_main_get_x11_display_policy (MetaContext *context)` … `case META_COMPOSITOR_TYPE_X11:` / `return META_X11_DISPLAY_POLICY_MANDATORY;` / `case META_COMPOSITOR_TYPE_WAYLAND:` … `if (context_main->options.no_x11)` / `return META_X11_DISPLAY_POLICY_DISABLED;` / `else if (sd_pid_get_user_unit (0, &unit) < 0)` / `return META_X11_DISPLAY_POLICY_MANDATORY;` / `else` / `return META_X11_DISPLAY_POLICY_ON_DEMAND;`
- `org.gnome.mutter.gschema.xml.in:104-106, :129-131`: `<key name="experimental-features"` … `<default>[]</default>` … `• “autoclose-xwayland” — automatically terminates Xwayland if all relevant X11 clients are gone. Requires a restart.`
- `org.gnome.Shell@wayland.service.in`: `Description=GNOME Shell on Wayland` … `ConditionEnvironment=XDG_SESSION_TYPE=%I` … `[Service]` / `Slice=session.slice` / `Type=notify` / `ExecStart=@bindir@/gnome-shell`
- `61-gdm.rules.in` (Ubuntu noble-updates): `# disable Wayland on Hi1710 chipsets` … `# disable Wayland if modesetting is disabled` … `IMPORT{cmdline}="nomodeset", GOTO="gdm_disable_wayland"` … and the NVIDIA vendor-driver checks `TEST{0711}!="/usr/bin/nvidia-sleep.sh", GOTO="gdm_disable_wayland"` / `ENV{NVIDIA_PRESERVE_VIDEO_MEMORY_ALLOCATIONS}!="1", GOTO="gdm_disable_wayland"`.

**Coverage.** T2 — covers as mechanism: GNOME Shell 46 on Wayland runs as the systemd user unit `org.gnome.Shell@wayland.service`, so `sd_pid_get_user_unit` succeeds and Mutter's X11 display policy is ON_DEMAND — Xwayland starts only when an X11 client connects — and since `autoclose-xwayland` is not in the default experimental features, a started Xwayland stays for the session. Run outside a user unit, Mutter's Wayland compositor takes the MANDATORY policy and starts Xwayland at once; `--no-x11` disables it. GDM on Ubuntu 24.04 disables Wayland only under the listed conditions (the Hi1710 chipset, `nomodeset`, the NVIDIA vendor driver without its suspend services), so the GNOME session is Wayland otherwise; the shipped `custom.conf`, which can set `WaylandEnable=false`, was not read (R5). T1, T4 — do not cover.

### S2-29 — systemd v255's `user@.service`: the per-user manager

**Citation.** systemd project, `units/user@.service.in`, tag `v255`, https://github.com/systemd/systemd — the upstream release Ubuntu 24.04 packages (`255.4-1ubuntu8`, R7).

**Passages.** `units/user@.service.in`: `Description=User Manager for UID %i` / `After=user-runtime-dir@%i.service dbus.service systemd-oomd.service` / `[Service]` / `User=%i` / `PAMName=systemd-user` / `Type=notify-reload` / `ExecStart={{LIBEXECDIR}}/systemd --user` / `Slice=user-%i.slice` / `KillMode=mixed` / `Delegate=pids memory cpu`.

**Coverage.** T1 — covers as structure: for each logged-in user, pid 1 starts a second `systemd` process, the user manager (`systemd --user`), in the user's slice with the CPU controller delegated to it; the session's user units — GNOME Shell's `org.gnome.Shell@wayland.service` (S2-28), the session bus's user unit (S2-04, S2-05), the PipeWire services (S2-18, S2-19) — run under it. No idle cadence is stated. T2, T4 — do not cover.
