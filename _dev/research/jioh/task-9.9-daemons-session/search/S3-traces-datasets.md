# S3 — public traces, datasets, logs, bug reports with profiles, benchmark databases

Reader class S3 for task 9.9 (daemons and session processes), stage 2 search. Topics searched: T1, T2, T3, T5 (T4, T6, T7 belong to other classes and were not searched). Date of work: 2026-09-20. Environment: the proxied session described in the brief (github.com HTML and api.github.com 403; raw.githubusercontent.com works; GitHub MCP tools scoped to one repository only). Every copy read is saved under `sources/S3-NN/` (gitignored); this record is self-sufficient.

Conventions in this record: a passage in a blockquote is verbatim from the saved copy; the locator names the post, comment id, note id, slide, line of the saved text extraction (`.txt`, produced by a whitespace-normalising HTML-to-text pass over the saved `.html`; `line N` refers to that file) or JSON field. "Own computation" marks numbers I derived from downloaded data; those locate a candidate and are not values. All HTTP statuses are as returned through the session proxy on 2026-09-20.

## 1. Search log

| # | Date | Engine / venue | Exact query or URL | Hits followed | Dead ends (HTTP status) |
|---|------|----------------|--------------------|---------------|-------------------------|
| 1 | 2026-09-20 | GitHub MCP `issue_read` | sched-ext/scx issues 234 and 296 | — | "Access denied: repository sched-ext/scx is not configured for this session" (tool error, both) |
| 2 | 2026-09-20 | curl | https://static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf | S3-01 | — |
| 3 | 2026-09-20 | curl reachability probe | https://github.com/sched-ext/scx/issues/234 ; https://api.github.com/repos/sched-ext/scx/issues/234 ; https://github.com/systemd/systemd/issues ; https://www.phoronix.com/ ; https://openbenchmarking.org/ ; https://lists.freedesktop.org/archives/ ; https://lore.kernel.org/ | — | all 403 |
| 4 | 2026-09-20 | curl reachability probe | https://raw.githubusercontent.com/sched-ext/scx/main/README.md 200; https://bugzilla.redhat.com/ 200; https://bugs.launchpad.net/ 200; https://lttng.org/ 200; https://marc.info/ 200; https://web.archive.org/ 200; https://bugzilla.kernel.org/ 200 | used below | https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/ 404 (HTML listing); https://gitlab.freedesktop.org/pipewire/pipewire/-/issues 404; https://invent.kde.org/plasma/kwin/-/issues 404; https://storage.googleapis.com/perfetto/test_data/ 404 (no directory listing) |
| 5 | 2026-09-20 | WebFetch | https://github.com/sched-ext/scx/issues/234 and …/296 | issue bodies summarised (not verbatim); the fetched page carried no comments | — |
| 6 | 2026-09-20 | Wayback `id_` | https://web.archive.org/web/2024id_/https://github.com/sched-ext/scx/issues/234 ; …/2025id_/…/296 | — | first attempts: connection reset by peer (curl 35, proxy "ws_closed_mid_exchange"), status 000 |
| 7 | 2026-09-20 | Wayback `id_` (retry) | https://web.archive.org/web/20240601id_/https://github.com/sched-ext/scx/issues/234 → 200, resolved to capture 20240628194502 (server-rendered, 116 `comment-body` blocks) | S3-02 | — |
| 8 | 2026-09-20 | Wayback `id_` (retry) | https://web.archive.org/web/{2025,20240601,20240901,20241201}id_/https://github.com/sched-ext/scx/issues/296 | — | every timestamp resolved to the same capture 20250730214324 (200, 53 452 bytes, React issue page with 0 `comment-body` blocks and no per-task text: grep for `lat_cri`, `wake_freq`, `pipewire`, `wireplumber` found nothing). #296 comments are unobtainable in this environment |
| 9 | 2026-09-20 | WebFetch | https://api.github.com/repos/sched-ext/scx/issues/296/comments ; …/234/comments | — | 403 both |
| 10 | 2026-09-20 | curl | https://gist.github.com/ChrisLane (200) → https://gist.githubusercontent.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1/raw (200, 118 045 bytes) | S3-02 | — |
| 11 | 2026-09-20 | GitLab REST API | https://gitlab.gnome.org/api/v4/projects/GNOME%2Fgnome-shell/issues?search=idle+CPU&per_page=20&scope=all | #3858 "Excessive CPU spin at idle" (S3-17); #8183 "Random high CPU usage" (not followed: no numbers in listing) | — |
| 12 | 2026-09-20 | GitLab REST API | https://gitlab.gnome.org/api/v4/projects/GNOME%2Fmutter/issues?search=idle+wakeups | #4622 (S3-06) | — |
| 13 | 2026-09-20 | GitLab REST API | https://gitlab.gnome.org/api/v4/projects/GNOME%2Fgnome-shell/issues?search=wakeups | none relevant (crashes, lock screen) | — |
| 14 | 2026-09-20 | GitLab REST API | https://gitlab.freedesktop.org/api/v4/projects/pipewire%2Fpipewire/issues?search=idle+CPU+usage | #3699 (not followed: no numbers), #1108 (read: no per-process numbers beyond "8-12%", see Not found) | — |
| 15 | 2026-09-20 | GitLab REST API | https://gitlab.freedesktop.org/api/v4/projects/pipewire%2Fpipewire/issues?search=wakeups | #3863 (S3-08); #3648 "pipewire-alsa: many spurious poll wakeups" (read: "high 10 thousands" wakeups of a test app, no daemon-side figure; not a candidate) | — |
| 16 | 2026-09-20 | GitLab REST API | https://invent.kde.org/api/v4/projects/plasma%2Fkwin/issues?search=idle+CPU ; …search=wakeups | #132 (read: screenshot only, redirected to bugs.kde.org; not a candidate) | — |
| 17 | 2026-09-20 | GitLab REST API | https://gitlab.freedesktop.org/api/v4/projects/xorg%2Fxserver/issues?search=idle+CPU | #1531 (S3-23) | — |
| 18 | 2026-09-20 | GitLab REST API | `…/issues/<iid>/notes` for the above | — | 401 (auth required) for every project |
| 19 | 2026-09-20 | GitLab web JSON | `https://<host>/<group>/<project>/-/issues/<iid>/discussions.json` | 200 for mutter 4622, gnome-shell 3858, pipewire 3863/3648/1108, kwin 132 | — |
| 20 | 2026-09-20 | WebSearch | powertop "wakeups/s" "gnome-shell" "Xorg" idle laptop report | Gentoo 1153076 (login wall, see #33); Arch 136354 (2012, context); Ubuntu wiki (S3-21); GNOME wiki archive Initiatives/GnomePerformance/Sleep (2007-era, context, read and not used) | — |
| 21 | 2026-09-20 | WebSearch | powertop overview "Usage" "Wakeups/s" "pipewire" OR "pipewire-pulse" idle "systemd-journald" table | columbia.edu PowerTOP report | https://www.columbia.edu/~swc2124/assets/HEAD02-INTL-03.html 403 |
| 22 | 2026-09-20 | WebSearch | "pw-top" output idle "pipewire" "wireplumber" "Xorg" OR "kwin_wayland" OR "gnome-shell" "perf sched" idle desktop trace | nothing usable (man pages, wikis) | — |
| 23 | 2026-09-20 | WebSearch | "wakeups from idle" powertop "kwin_wayland" OR "plasmashell" OR "gnome-shell" "wakeups/s" table 2023 OR 2024 OR 2025 | Arch 239846 (S3-03) | — |
| 24 | 2026-09-20 | WebSearch | sysprof OR "perf report" "gnome-shell" idle profile "wakeups" "mutter" frame clock idle CPU bug report numbers | Fedora Magazine profiling article (S3-10) | — |
| 25 | 2026-09-20 | WebSearch | "perf sched timehist" OR "perf sched latency" idle desktop "gnome-shell" OR "kwin_wayland" OR "Xorg" "pipewire" output posted | only man pages and Brendan Gregg's 2017 server example (no desktop process) | — |
| 26 | 2026-09-20 | WebSearch | Trace Compass test traces LTTng kernel trace sample download "kernel_vm" OR "trace2" OR "bug" tracecompass-test-traces | README (read, #46; no trace description) | — |
| 27 | 2026-09-20 | WebSearch | "systemd-oomd" idle wakeups sysprof battery life Fedora "wakeups per second" OR "wakeups/s" measurement patch | RH bug 1944646 (S3-09); Fedora wiki Changes/ImprovedLaptopBatteryLife (read: watt savings of hardware policies, no per-process data; not a candidate) | — |
| 28 | 2026-09-20 | WebSearch | sched-analyzer OR "sched_ext" perfetto trace example Linux desktop "kwin_wayland" OR "gnome-shell" trace file download | sched-analyzer README (read: screenshots only, no trace files) | — |
| 29 | 2026-09-20 | WebSearch | powertop "gnome-shell" "wakeups" idle Wayland 2022 OR 2023 OR 2024 OR 2025 blog "Events/s" "Usage" laptop Fedora OR Ubuntu OR Arch | nothing new | — |
| 30 | 2026-09-20 | WebSearch | "systemd-journald" OR "dbus-broker" OR "dbus-daemon" OR "NetworkManager" OR "chronyd" "wakeups" idle powertop table site:github.com OR site:bugzilla.redhat.com OR site:bugs.launchpad.net | nothing with numbers | — |
| 31 | 2026-09-20 | WebSearch | "kwin_wayland" idle "wakeups" OR "CPU usage" powertop OR perf "plasmashell" idle measurements bugs.kde.org 2024 2025 | KDE bugs 466414, 460248 (S3-18), KDE Discuss 32396 (S3-19), Manjaro 162038 (read: "about 100%"/"almost 50%" bug state, no machine state details beyond CPU model; not a candidate) | — |
| 32 | 2026-09-20 | WebSearch | Brendan Gregg "perf sched timehist" example output "gnome-shell" OR "Xorg" OR "chrome" desktop; "perf sched" idle laptop "wakeups" blog 2020..2025 | nothing usable | — |
| 33 | 2026-09-20 | curl / WebFetch / Wayback | https://forums.gentoo.org/viewtopic-t-1153076-start-0.html (200 but login wall: "The board requires you to be registered and logged in to view this forum."); …-view-previous.html (200, login wall); Wayback 2024id_ → 503; 2023id_/2022id_ → connection reset (000); 2025id_ → 200 but login page (0 occurrences of "wakeups"); WebFetch → login wall | — | Gentoo thread "Laptop burning hot, high wakeups, 50W power usage at idle" unreadable; the search snippet's "Dell Precision 7560 ~3000 wakeups per second at idle with 26% CPU" cannot be quoted |
| 34 | 2026-09-20 | bugs.kde.org REST | https://bugs.kde.org/rest/bug?quicksearch=kwin_wayland%20idle%20cpu&limit=20 | 486214 (S3-24), 525537 (S3-07); also 524046, 525955 (not followed: gaming/dma-buf bugs) | — |
| 35 | 2026-09-20 | bugzilla.redhat.com REST | https://bugzilla.redhat.com/rest/bug?quicksearch=gnome-shell%20idle%20wakeups ; …quicksearch=powertop%20wakeups%20gnome-shell | — | both 200 with `total_matches: 0` |
| 36 | 2026-09-20 | bugzilla.kernel.org REST | https://bugzilla.kernel.org/rest/bug?quicksearch=idle%20wakeups%20powertop&limit=10 | bugs 12118 (2008) and 120291 (2016 "swapper causes many timer wakeups", VM) — not followed (no desktop process) | — |
| 37 | 2026-09-20 | bugs.kde.org REST | https://bugs.kde.org/rest/bug/{486214,525537,466414,460248} and …/comment | S3-24, S3-07, S3-18; 466414 read (video attachment, "close to 100%", no table; not a candidate) | — |
| 38 | 2026-09-20 | bugzilla.redhat.com REST | https://bugzilla.redhat.com/rest/bug/1944646 and …/comment | S3-09 | — |
| 39 | 2026-09-20 | curl | https://fedoramagazine.org/performance-profiling-in-fedora-linux/ ; https://fedoraproject.org/wiki/Changes/ImprovedLaptopBatteryLife ; https://bbs.archlinux.org/viewtopic.php?id=239846 ; https://bbs.archlinux.org/viewtopic.php?id=136354 ; https://wiki.ubuntu.com/Kernel/PowerManagement/IdentifyingIssues ; https://wiki.gnome.org/Initiatives(2f)GnomePerformance(2f)Sleep.html | S3-10, S3-03, S3-21 | — |
| 40 | 2026-09-20 | Perfetto test data index | https://android.googlesource.com/platform/external/perfetto/+/refs/heads/main/test/data/?format=TEXT (200; base64 git tree listing of 168 entries) | S3-15 | — |
| 41 | 2026-09-20 | Perfetto test data download | https://storage.googleapis.com/perfetto/test_data/<name>-<sha256> for sched_wakeup_trace.atr, compact_sched.pb, sched_switch_original.pb, sched_switch_compact.pb, perf_sample.pb, perf_sample_sc.pb, linux_block_io_trace.pb, ui-funcgraph.pftrace (all 200) | ui-funcgraph.pftrace (S3-15). Own computation with the trace processor: compact_sched.pb / sched_switch_*.pb are Android aarch64 4.9 kernels, 0.17–0.45 s, no process names; perf_sample*.pb and linux_block_io_trace.pb carry `android_build_fingerprint` and no sched rows; sched_wakeup_trace.atr is an Android cuttlefish x86_64 image (`aosp_cf_x86_64_phone`, 5.15.83-android14 kernel; top processes com.android.systemui, system_server, surfaceflinger) — Android, context only | — |
| 42 | 2026-09-20 | pip | `pip install perfetto` in a venv (perfetto 0.58.2; trace_processor_shell v57.2 downloaded on first use from commondatastorage.googleapis.com/perfetto-luci-artifacts) | tool for #41 | — |
| 43 | 2026-09-20 | curl | https://raw.githubusercontent.com/google/perfetto/main/tools/install-build-deps (200; no test-trace URLs, test data is synced by `tools/test_data`) | — | — |
| 44 | 2026-09-20 | WebSearch | powertop "Summary:" "wakeups/second" "GPU ops/seconds" "gnome-shell" OR "kwin_wayland" OR "Xorg" idle "Process" | lkml psi_avgs_work mail (S3-04); Oracle PowerTOP reference (S3-22); pages.cs.wisc.edu/~kadav/PowerTOP.html (200, read: no powertop table in the text extraction; not a candidate) | — |
| 45 | 2026-09-20 | WebSearch | "systemd-journald" OR "systemd-udevd" OR "systemd-logind" idle "wakeups" OR "CPU" "powertop" OR "perf" github.com/systemd/systemd/issues idle laptop | systemd #21751 (S3-20), #5102 | #5102 via Wayback 2020id_/2021id_: connection reset (000) |
| 46 | 2026-09-20 | curl | https://raw.githubusercontent.com/eclipse-tracecompass/tracecompass-test-traces/master/README.md (200: build instructions only, traces not described); https://raw.githubusercontent.com/tuxology/tracevizlab/master/README.md and …/labs/004-record-kernel-trace-ftrace/README.md (200: instructions to record one's own trace, no published trace); https://raw.githubusercontent.com/qais-yousef/sched-analyzer/main/README.md (200: screenshots only); https://git.eclipse.org/c/tracecompass/tracecompass-test-traces.git/ 200 | — | https://github.com/tuxology/tracevizlab/raw/master/labs/001-what-is-tracing/README.md 403 |
| 47 | 2026-09-20 | WebSearch | "udisksd" OR "polkitd" OR "packagekitd" OR "NetworkManager" "wakeups" idle powertop laptop battery bug report "wakeups/s" | nothing with numbers | — |
| 48 | 2026-09-20 | WebFetch | https://www.phoronix.com/review/ubuntu-2404-idle-power | — | 403 |
| 49 | 2026-09-20 | Wayback `id_` | https://web.archive.org/web/2023id_/https://github.com/systemd/systemd/issues/21751 (200, capture with 20 comment bodies) | S3-20 | — |
| 50 | 2026-09-20 | Discourse JSON | https://discuss.kde.org/t/32396.json (200); https://forum.manjaro.org/t/162038.json (200) | S3-19; Manjaro read, not a candidate (see #31) | — |
| 51 | 2026-09-20 | curl | https://lkml.iu.edu/1606.2/06623.html (200); https://lkml.rescloud.iu.edu/hypermail/linux/kernel/2007.2/09914.html (200); https://docs.oracle.com/en/operating-systems/oracle-linux/9/tuned/powertop_command_reference.html (200) | S3-11, S3-04, S3-22 | — |
| 52 | 2026-09-20 | WebSearch | "Summary:" "wakeups/second" "gnome-shell" powertop idle site:community.frame.work OR site:discussion.fedoraproject.org OR site:askubuntu.com OR site:discourse.ubuntu.com | only 2008–2009 lkml/Debian threads (context, not followed) | — |
| 53 | 2026-09-20 | WebSearch | "Summary:" "wakeups/second" powertop "kwin_wayland" OR "plasmashell" OR "pipewire" OR "wireplumber" "Events/s" 2023 OR 2024 OR 2025 OR 2026 | nothing beyond S3-03 and S3-22 | — |
| 54 | 2026-09-20 | WebSearch | LTTng sample kernel trace download "lttng-modules" example trace tarball babeltrace "ctf-traces" test traces Linux desktop | github.com/lttng/lttng-ref-traces; https://www.efficios.com/pub/ctf/traces/ (S3-16) | https://raw.githubusercontent.com/lttng/lttng-ref-traces/{master,main}/README.md and …/master/README.adoc 404 (README unobtainable; only the script `traces/basic-kernel-analysis.sh` came through raw, 200) |
| 55 | 2026-09-20 | WebSearch | "dbus-broker" OR "chronyd" OR "systemd-timesyncd" OR "NetworkManager" idle "wakeups" powertop "Events/s" OR "wakeups/s" laptop report | nothing with numbers | — |
| 56 | 2026-09-20 | Discourse JSON | https://discussion.fedoraproject.org/t/150603.json ; …/133876.json ; …/171602.json (all 200) | S3-12; 133876 read (kwin_wayland "20-30%" then "0.1 to 0.3%" after an NVIDIA driver change, a driver bug state; not a candidate); 171602 read (llvmpipe fallback bug state; not a candidate) | — |
| 57 | 2026-09-20 | Launchpad API | https://api.launchpad.net/1.0/ubuntu/+source/gnome-shell?ws.op=searchTasks&search_text=idle%20CPU%20wakeups&status=… | 200, zero entries | — |
| 58 | 2026-09-20 | WebSearch | "perf sched" OR "trace-cmd" OR "perfetto" trace of idle Linux desktop released dataset "sched_switch" "gnome-shell" OR "kwin" OR "Xorg" download github trace file idle wakeups analysis | nothing: docs and man pages only | — |
| 59 | 2026-09-20 | WebSearch | GNOME vs KDE idle wakeups comparison powertop "wakeups/second" Wayland X11 idle desktop measurement blog | dedoimedo article (S3-05) | — |
| 60 | 2026-09-20 | WebSearch | "Xorg" idle powertop "Events/s" OR "wakeups/s" "tick_sched_timer" "Summary:" gnome OR xfce OR kde 2019 OR 2020 OR 2021 OR 2022 | Linux Mint 414319 (S3-13); Arch 252284 (S3-14); Arch 133843 (2012, read, context only: not used) | — |
| 61 | 2026-09-20 | WebSearch | "systemd-journald" idle CPU "%" OR "wakeups" laptop "journald" "SyncIntervalSec" observed powertop OR top measurement report | nothing with numbers | — |
| 62 | 2026-09-20 | curl | https://www.dedoimedo.com/computers/wayland-fedora-gnome-kde-neon-amd-graphics-benchmark.html ; https://forums.linuxmint.com/viewtopic.php?t=414319 ; https://bbs.archlinux.org/viewtopic.php?id=252284 ; https://bbs.archlinux.org/viewtopic.php?id=133843 (all 200) | S3-05, S3-13, S3-14 | — |

## 2. Candidates

### S3-01 — LAVD deck, Open Source Summit NA 2024

**Citation.** Changwoo Min, "Optimizing Scheduler for Linux Gaming" (scx_lavd), Open Source Summit North America, slides dated April 17, 2024, 30 pages.
**Copy read.** URL https://static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf, accessed 2026-09-20, PDF 1.4 (metadata title `scx-lavd-oss-na24`, creator Google), local `sources/S3-01/scx-lavd-oss-na24.pdf`, SHA-256 `e62d69cd401021f8bfedadde2c4de62b01383facaa83acce7d218af3b6402475`. Text extracted with PyMuPDF.

**Passages.** Slide 12, "Task scheduling and CPU utilization":
> Around 300 tasks are scheduled while running a game.
> Around 90% are long-living tasks; only 10% of tasks are terminated.
> Top 30-40 most frequently scheduled tasks take 95% of scheduling.
> Around half of them are system tasks -- especially, wine,
> graphics, and audio servers, taking 30--40% of scheduling.
> There are 15-20 game-speciﬁc tasks, which takes 60-70%
> scheduling.
> CPU utilization is moderately high -- around 65-95%, but not
> overloaded (i.e., no 100%).

Slide 14, "What makes scheduling happen?":
> Preemption (e.g., timer interrupt) takes only 25-30% of scheduling.
> 70-75% of scheduling is initiated by waiting system calls – such as
> epoll, pipe_read, futex_wait, etc.

**Coverage.** T5: covers — object: scheduling events of a running Linux game session; unit: share of scheduling events; statistic: share taken by "system tasks -- especially, wine, graphics, and audio servers" (30–40 %) versus 15–20 game tasks (60–70 %), and share initiated by blocking syscalls (70–75 %) versus preemption (25–30 %); scope: "while running a game", population and game(s), machine, kernel and trace tool are not named on the slide. T1, T2, T3: does not cover (no idle state, no per-daemon values). One observation? Unclear: the deck gives ranges across unnamed games; no machine, no version, no window; state = playing a game (not idle).

### S3-02 — sched-ext/scx issue #234 with its scx_lavd log gist

**Citation.** ChrisLane, "[scx_lavd] Getting large pauses and stutters in-game", sched-ext/scx issue #234, opened 2024-04-18, closed by the reporter after commit fa1c146; log gist https://gist.github.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1 ("gistfile1.txt").
**Copy read.** (a) Wayback capture https://web.archive.org/web/20240628194502id_/https://github.com/sched-ext/scx/issues/234, accessed 2026-09-20, local `sources/S3-02/scx-issue-234-wayback.html`, SHA-256 `3ae62cf85549a83050bc85dd5780ea8cfa992a92ba8be77c96544c8379bc254c`. (b) Gist raw https://gist.githubusercontent.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1/raw, accessed 2026-09-20, 424 lines, local `sources/S3-02/scx-234-gist-1945f66b.txt`, SHA-256 `05e1a6d1f106a7838dd34980c2f404d2d0b88e7c686c9d58b21e0aedfef41a94`. (c) For the record, issue #296 capture https://web.archive.org/web/20250730214324id_/https://github.com/sched-ext/scx/issues/296, local `sources/S3-02/scx-issue-296-wayback.html`, SHA-256 `5a8487763ea3e404c0fb4f567d94908ecbff978d16c38f10f4cd121e5f5a467b` — it carries the issue title and body only ("Ryzen 5950x (with one CCD disabled)", "roughly 20 percent less fps compared to eevdf", Starcraft 2 and Diablo 3, per the WebFetch summary) and no comments or per-task table; not quoted further.

**Passages.** Issue body (capture (a), first `comment-body` block):
> I have observed that I am able to quite reliably reproduce stutters and pauses, sometimes several seconds long while running around my ship in Helldivers 2.
> Here's the output from sudo scx_lavd while I was running the game with several stutters in the period (not sure on exact timestamps:
> Distro: Arch Linux
> Kernel: 6.8.7-1-cachyos
> GPU: AMD Radeon RX 6800 XT (RADV NAVI21)
> CPU: AMD Ryzen 9 5900X 12-Core Processor
> RAM: 36GB

Gist, line 4 (column header printed by scx_lavd once per second for the task it samples):
> 22:14:17 [INFO] | mseq      | pid      | comm              | cpu  | vtmc | vddln_ns  | elglty_ns | slice_ns   | grdy_rt   | lat_prio | lat_cri | min_lc  | avg_lc  | max_lc  | static_prio  | lat_bst | slice_bst | run_freq  | run_tm_ns | wait_freq | wake_freq | cpu_util | sys_ld |

Gist, lines 88, 144, 282, 290 — the only rows naming an audio or display server (own grep; the other 420 rows are kworker, wine/game threads, sudo, steam):
> 22:15:38 [INFO] |        82 |     1671 | pipewire-pulse    |    3 |   -1 |         0 |         0 |    3000000 |         5 |       14 |      42 |      40 |      48 |      56 |            9 |       5 |         0 |      3643 |     11619 |      3999 |       840 |       37 |     11 |
> 22:16:32 [INFO] |       136 |     2240 | Xwayland          |   13 |   -1 |         0 |         0 |    3000000 |       633 |       24 |      43 |      39 |      48 |      56 |           20 |       4 |         0 |     12013 |     33594 |     16394 |     15636 |       38 |      9 |
> 22:18:46 [INFO] |       270 |     1671 | pipewire-pulse    |    9 |   -1 |         0 |         0 |    3000000 |        15 |       11 |      42 |      40 |      43 |      51 |            9 |       2 |         0 |      3035 |     11820 |      3696 |      1087 |        4 |      0 |
> 22:18:54 [INFO] |       278 |     2241 | Xwayland:cs0      |   15 |   -1 |         0 |         0 |    3000000 |         8 |       23 |      42 |      33 |      48 |      56 |           20 |       3 |         0 |       126 |     36782 |       125 |       792 |       36 |     10 |

Own computation (command `awk -F'|' 'NF>20 && $4!~/comm/ {gsub(/^ +| +$/,"",$4); print $4}' scx-234-gist-1945f66b.txt | sort | uniq -c | sort -rn`): 424 log lines; distinct `comm` values sampled: 41; rows by name — sudo 56, kworker/u66:52 38, kworker/u66:26 35, kworker/u65:57 34, "thread pool wor" 33, … wineserver 9, winedevice.exe 4, dxvk-queue 4, pipewire-pulse 2, Xwayland 1, Xwayland:cs0 1, steam 1, explorer.exe 1; no row names systemd, wireplumber, kwin_wayland, plasmashell, Xorg, gnome-shell or dbus-daemon. The column semantics (run_freq, run_tm_ns, wait_freq, wake_freq as maintained per task by scx_lavd) are the scheduler's own instrumentation; what unit `run_freq`/`wake_freq` carry is not stated in the log.

**Coverage.** T5: covers — object: scx_lavd's per-task sampled statistics (one task per second, the task it chose to print) during a Linux game session; unit: per-task run frequency, run time in ns, wait frequency, wake frequency, cpu_util, sys_ld, latency criticality; statistic: point samples; scope: one machine (Ryzen 9 5900X, RX 6800 XT, Arch, 6.8.7-1-cachyos), Helldivers 2 under Proton, scx_lavd of April 2024, window 22:14:16–22:21 (about seven minutes of log); population: whichever task scx_lavd sampled each second. T2: covers weakly — pipewire-pulse (pid 1671, static_prio 9) and Xwayland (pid 2240/2241) rows with their run/wait/wake frequencies while a game plays; state = playing, not idle. T1, T3: does not cover. One observation: yes — one machine, one game session, one log; subject program versions of PipeWire/Xwayland not named; state "playing a game with stutters"; window as above.

### S3-03 — Arch Linux forum, "KDE High Number of Wakeups" (2018)

**Citation.** archapex, "KDE High Number of Wakeups", Arch Linux Forums, Applications & Desktop Environments, thread 239846, posts #1 (2018-08-24 22:34:51) and #3 (2018-08-26 15:33:03); reply #2 by seth.
**Copy read.** URL https://bbs.archlinux.org/viewtopic.php?id=239846, accessed 2026-09-20 (200), local `sources/S3-03/arch-bbs-239846.html` SHA-256 `7d44f615d6103f6710b33a94d0ce18c12897a441dee503dd20af3a6594e519e2`; text extraction `sources/S3-03/arch-bbs-239846.txt` SHA-256 `9aa471cf01b59356a0abe0897bbf43f278d2545366a433be722bd0b9b94c8de2`.

**Passages.** Post #1 (txt lines 26–31, 34–41):
> I've noticed that my laptop gets a high number of wakeups/second and the CPU hardly reaches sleep state. I thought values above 1000 were normal on idle until I researched that people get within 100-300. I suspect it's mostly KDE related according powertop. I have disabled animations and other effects. But wakeups still remain high, wakeups dropped from 1500 to 1000. I  notice that powertop is still finding wakeups from plasmashell and kwin. Any further suggestions?
> Summary: 1091.1 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 25.7% CPU use
> Power est.  Usage       Events/s    Category       Description
> 7.22 W     25.0%                      Device         Display backlight
> 695 mW      2.1 pkts/s                Device         Network interface: wlp3s0 (iwlwifi)
> 52.0 mW     36.7 ms/s      60.4        Process        [PID 14568] konsole [kdeinit5]
> 40.9 mW     21.9 ms/s     136.1        Process        [PID 1095] /usr/bin/telegram-desktop -startintray
> 38.5 mW     29.1 ms/s      21.1        Process        [PID 1054] /usr/bin/plasmashell
> 31.0 mW     20.2 ms/s      57.3        Process        [PID 641] /usr/lib/Xorg -nolisten tcp -auth /var/run/sddm/{89ed49f8-13c4-437e-a91c-7cb9b3f40525} -background none -noreset -dis
> 29.2 mW     18.3 ms/s      63.6        Process        [PID 1045] /usr/bin/kwin_x11
> 28.6 mW     11.6 ms/s     141.3        Interrupt      PS/2 Touchpad / Keyboard / Mouse
> 26.0 mW      6.0 ms/s     186.0        Process        [PID 1120] /usr/bin/kwin_x11

Post #1, `top` block (txt lines 58–61, 64–68, 77, 90):
> top - 00:31:37 up 2 days, 16:46,  5 users,  load average: 1.13, 1.15, 1.23
> Tasks: 277 total,   1 running, 276 sleeping,   0 stopped,   0 zombie
> %Cpu(s):  2.5 us,  1.3 sy,  0.0 ni, 95.6 id,  0.2 wa,  0.3 hi,  0.1 si,  0.0 st
> 1045 stcm      20   0 3149880  57444  30680 S   7.3   0.7 161:56.38 kwin_x11
> 14568 stcm      20   0  597888  91484  57524 S   5.3   1.2   0:36.97 konsole
> 641 root      20   0  686476 121644 103568 S   4.0   1.5 113:07.56 Xorg
> 1054 stcm      20   0 5405620 235932  73532 S   3.3   3.0 167:21.70 plasmashell
> 1215 stcm      20   0   24476   1848   1672 S   0.3   0.0   0:06.07 dbus-daemon
> 1 root      20   0  224268   5816   3684 S   0.0   0.1   0:06.62 systemd

Post #2 (seth, 2018-08-25):
> There're quite some input events and I assume telegram might update its systray icon which will wake plasmashell (to repaint the icon) and in turn kwin_x11 (assuming you did not stop the compositor, but "only" disabled fancy trasition events)?

Post #3 (txt lines 141–142, 150, 152–153, 156):
> Switched off composer and waited for a day, to find a difference. Wakeups still high around 900-1200 on average sometimes drops to 570 for a short time
> Summary: 1102.5 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 25.3% CPU use
> 107 mW      4.3 ms/s     114.3        Process        [PID 1123] /usr/bin/kwin_x11
> 84.0 mW     30.6 ms/s      32.6        Process        [PID 678] /usr/lib/Xorg -nolisten tcp -auth /var/run/sddm/{c249a932-baf7-451d-ae76
> 68.2 mW     12.5 ms/s      21.9        Process        [PID 1070] /usr/bin/kwin_x11
> 25.9 mW      8.5 ms/s      10.9        Process        [PID 1074] /usr/bin/plasmashell

**Coverage.** T3: covers — object: a KDE Plasma 5 X11 laptop session with konsole (running top), telegram-desktop in tray, chromium tabs and ksysguard open; unit: wakeups/second (powertop summary) and %CPU; statistic: two point samples (1091.1 and 1102.5 wakeups/s at 25.7 % and 25.3 % CPU; "900-1200 on average sometimes drops to 570"); population: the whole machine. T2: covers — per-process powertop Events/s and ms/s for plasmashell (21.1 /s, 29.1 ms/s; later 10.9 /s), Xorg (57.3 /s; 32.6 /s), kwin_x11 (63.6 and 186.0 /s for two PIDs; 114.3 and 21.9 /s with compositing off), and `top` cumulative CPU time over 2 d 16 h uptime (kwin_x11 161:56, Xorg 113:07, plasmashell 167:21). T1: covers weakly — `top` rows dbus-daemon 0.3 %CPU / 0:06.07 cumulative and systemd 0.0 % / 0:06.62 cumulative over the same uptime; no powertop row for any system service. T5: does not cover. One observation: yes — one laptop (4 CPUs per the rcuc/0–3 rows, 7.7 GB RAM, iwlwifi; model not named), Arch Linux 2018, KDE Plasma 5 on X11 (kwin_x11, sddm), state "idle" as the user calls it but with a chat client and browser open; window: powertop refresh samples of unknown length, uptime 2 d 16 h for the `top` totals.

### S3-04 — lkml, "`psi_avgs_work` shows up in PowerTOP" (2020)

**Citation.** Paul Menzel, "`psi_avgs_work` shows up in PowerTOP", linux-kernel mailing list, Thu Jul 23 2020 09:58:08 EST (to Johannes Weiner).
**Copy read.** URL https://lkml.rescloud.iu.edu/hypermail/linux/kernel/2007.2/09914.html, accessed 2026-09-20 (200), local `sources/S3-04/lkml-psi_avgs_work.html` SHA-256 `e79b7c13791cf32c353f836e799893fcd688539fe81744a1a1ab469a749b62b2`; text extraction `sources/S3-04/lkml-psi_avgs_work.html.txt` SHA-256 `0722d73db9eaba8281233f6f845eba9df6bcc1795b426d55336f8ca27212fa3b`.

**Passages.** (txt lines 8–9, 13–17, 21, 29, 32, 34–36)
> On the Dell Latitude E7250 with Debian Sid/unstable and Linux 5.6.7,
> running `powertop`, `psi_avgs_work` shows up there with 40 mW to 60 mW.
> Summary: 795.2 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 16.8% CPU use
> Power est.              Usage       Events/s    Category       Description
>   2.62 W      5.5 ms/s     328.9        Timer          tick_sched_timer
>   817 mW     21.9 ms/s      99.9        Process        [PID 519673] firefox
>   521 mW      3.2 ms/s      65.1        Process        [PID 519710] firefox
>   146 mW     16.0 ms/s      16.4        Process        [PID 72917] /usr/bin/gnome-shell
>   121 mW    160.7 us/s      15.2        Process        [PID 11] [rcu_sched]
>  62.5 mW      1.7 ms/s       7.6        Process        [PID 73223] ibus-daemon --panel disable -r --xim
>  59.6 mW     73.5 us/s       7.5        kWork          psi_avgs_work
>  56.9 mW      8.1 ms/s       6.1        Process        [PID 72956] /usr/bin/Xwayland :0 -rootless -norese

**Coverage.** T2: covers — object: gnome-shell (Wayland session: Xwayland `-rootless` present) and Xwayland on a Dell Latitude E7250, Debian sid, Linux 5.6.7, GNOME version not named; unit: powertop Events/s and ms/s of CPU per second; statistic: one refresh sample (gnome-shell 16.4 wakeups/s, 16.0 ms/s; Xwayland 6.1 /s, 8.1 ms/s); state: desktop with Firefox and Thunderbird open (not idle). T3: covers — whole machine 795.2 wakeups/s, 16.8 % CPU, tick_sched_timer 328.9 /s dominating, in that state. T1: covers weakly — ibus-daemon 7.6 /s and rcu_sched 15.2 /s rows; no systemd/dbus/journald row in the quoted top of the table. T5: does not cover. One observation: yes — machine, distribution and kernel named; session program versions not; state "with firefox/thunderbird open"; window: one powertop refresh (length not stated).

### S3-05 — Dedoimedo, "Wayland Fedora Gnome vs KDE neon Plasma, plus X11 data!" (2025)

**Citation.** Igor Ljubuncic (Dedoimedo), "Wayland Fedora Gnome vs KDE neon Plasma, plus X11 data!", dedoimedo.com, 2025 (the Tux Machines syndication dates it 2025-07-10); Fedora 42 Workstation (GNOME, Wayland) against KDE neon Plasma 6.4 in Wayland Power-Efficiency (PE), Wayland Color-Accuracy (CA) and X11 (compositing on) modes, on one Lenovo IdeaPad 3 (2019–2020) with AMD CPU and AMD graphics.
**Copy read.** URL https://www.dedoimedo.com/computers/wayland-fedora-gnome-kde-neon-amd-graphics-benchmark.html, accessed 2026-09-20 (200), local `sources/S3-05/dedoimedo-wayland-gnome-kde.html` SHA-256 `92d228f0c002246112daf0c10a85cd7ee94f71ac201e82cb5b31f3c19f8b174e`; text extraction `sources/S3-05/dedoimedo-wayland-gnome-kde.html.txt` SHA-256 `686aceeb5cfd7bea6d8a56f9d0a058cc0f91d6560cbf90b2f27d46b99fed714c`. Tables are rendered in the extraction as one cell per line in the column order Fedora 42 Wayland / KDE neon Wayland (PE) / KDE neon Wayland (CA) / KDE neon X11 (Comp ON).

**Passages.** Setup and vmstat (txt lines 64–65, 71–72, 78–79, 96–109):
> Idle desktop and loaded desktop benchmarks, similar to the KDE neon tests.
> Specifically, idle desktop vmstat, radeontop, powertop, and perf stat results.
> Accuracy (CA) modes in Plasma 6.4 and X11 session in Plasma 6.4 on this same AMD-powered,
> AMD-graphics laptop, one IdeaPad 3 from 2019-2020.
> Vmstat data
> The desktop be idling, with a single terminal window open:
> Interrupts (in)
> 929
> 1188
> 1173
> 937
> Context switches (cs)
> 536
> 1195
> 1208
> 803
> Idle CPU % (id)
> 97.8
> 98.03
> 97.90
> 98.17

Interpretation (txt lines 111–113):
> Wayland in Fedora 42 used 2.2% CPU on idle. This is higher than even Plasma's CA mode.

Power (txt lines 120, 126–130):
> Idle system, nothing running except a terminal window, battery drainage:
> Battery drain (W)
> 5.83-7.62
> 6.09
> 6.05-6.08
> 5.67-5.87

perf stat (txt lines 234, 240–255):
> Once again, as we did in KDE neon. An idle desktop, 60 seconds worth of samples:
> CPU clock (ms)
> ~492,000
> ~543,000
> ~540,000
> ~527,000
> Context switches
> 9,468 | 19.244/s
> 14,415 | 26.547/s
> 16,120 | 29.864/s
> 6,021 | 11.436/s
> CPU migrations
> 104 | 0.211/s
> 72 | 0.133/s
> 139 | 0.258/s
> 92 | 0.175/s

Conclusion (txt line 305):
> From here, my interim conclusion is that Fedora Gnome Wayland does more work on idle, which is

**Coverage.** T3: covers — object: whole idle desktop session (one terminal window open) in four configurations on one laptop; unit: vmstat interrupts/s and context switches/s, idle CPU %, battery drain W, `perf stat` 60 s totals (context switches, migrations, cycles); statistic: single readings per configuration (vmstat averaging window not stated; perf stat 60 s); population: GNOME 48-era Fedora 42 Wayland vs Plasma 6.4 Wayland PE / CA vs Plasma 6.4 X11 — the only cross-desktop idle comparison found. Note the powertop per-process tables are announced ("idle desktop … powertop") but only appear as images in the page; no per-process row is in the text. T1, T2: does not cover (no per-process split). T5: does not cover (no trace published). One observation: yes — one IdeaPad 3 (AMD, model year 2019–2020, CPU model not named in the extracted text), states idle-with-terminal; windows: perf stat 60 s, vmstat unspecified.

### S3-06 — GNOME mutter issue #4622 (gnome-shell wakeup rate, 2026)

**Citation.** flexlab, "gnome-shell enters high-frequency clock_nanosleep loop after extended fullscreen gaming session", GNOME/mutter issue #4622, opened 2026-02-18, closed 2026-03-07 (reporter could not reproduce on Mutter 49.4); replies by Michel Dänzer (daenzer).
**Copy read.** GitLab REST https://gitlab.gnome.org/api/v4/projects/GNOME%2Fmutter/issues/4622 (issue JSON) and https://gitlab.gnome.org/GNOME/mutter/-/issues/4622/discussions.json (notes), accessed 2026-09-20 (200 both), local `sources/S3-06/GNOME-mutter-4622.json` SHA-256 `3725fbc90c4d5d66fc536ab2cc4ee92a02fda91869cbed8f3cb750f68f598481` and `sources/S3-06/GNOME-mutter-4622-discussions.json` SHA-256 `2ed9afec55723b092ac15d27485d0ecc0c7958b18be0bc20703b81bd09d67325`.

**Passages.** Issue description (field `description`):
> OS: Debian Testing
> Mutter version: 49.3-1
> Display server: Wayland only (not tested on XOrg)
> GPU: AMD (amdgpu driver)
> gnome-shell enters a persistent busy-loop state. strace -c reveals that 98% of all syscalls are clock_nanosleep, with approximately 2.4 million calls recorded in \~30 seconds (\~80.000/s). The wakeup rate of the gnome-shell process rises from a normal \~1.500/s to \~15.500/s, measured via /proc/\<pid\>/schedstat. This persists indefinitely until the next logout/login and is not resolved by disabling all GNOME Shell extensions.
> Wakeup rate measurement via schedstat counter (field 3 of /proc/\<pid\>/schedstat, sampled over 5 seconds):
> - Fresh login (normal state): \~1.500 wakeups/s (confirmed via PowerTOP)
> - After 3h gaming session (degraded state): \~15.500 wakeups/s

Note 2684222 (flexlab, 2026-02-18):
> After terminating strace, the wakeup count immediately dropped back to baseline levels (\~3,000/5s). This means the elevated wakeup counts I reported (\~45,000–97,000/5s) were likely caused by strace itself rather than reflecting a genuine bug state.

Note 2686169 (flexlab, 2026-02-21):
> Four consecutive clean sysprof captures (each 20s) were taken over \~20 minutes with no significant system activity in the degraded state:
> Capture 1: \~11,600 drmModeAtomicAddProperty calls (\~580/s)
> Capture 2: \~36,300 calls (\~1,815/s) \[+6 min\]
> drmModeAtomicAddProperty dominates the gnome-shell call stack in all four captures. The call rate oscillates over time. The gnome-shell wakeup rate via /proc/\<pid\>/schedstat remains at baseline levels (\~3,200/5s) throughout.

Note 2686540 (daenzer, 2026-02-21):
> mutter KMS debug logging shows that it calls `drmModeAtomicAddProperty` 12 times for each normal output frame. 1800 calls per second would be consistent with 1 output updating at 150 Hz, 2 outputs updating at 75 Hz each, ...
> `clock_nanosleep` represents 0.02/1% of samples in sysprof capture 1/2. It's not clear why you consider this problematic.

**Coverage.** T2: covers — object: the gnome-shell process (Mutter 49.3, Wayland, amdgpu, Debian testing, two outputs: DisplayPort primary plus an HDMI TV powered off), unit: wakeups per second from `/proc/<pid>/schedstat` field 3 sampled over 5 s and PowerTOP; statistic: point readings — "\~1.500/s" at fresh login "(confirmed via PowerTOP)", and "\~3,000/5s" to "\~3,200/5s" (≈600–640/s) as the reporter's later baseline "with no significant system activity", which the reporter does not reconcile with the earlier 1,500/s; plus a maintainer's mechanism statement (12 `drmModeAtomicAddProperty` calls per output frame). State: logged-in desktop, nobody active ("no significant system activity"), after a gaming session; the "\~15.500/s" figure was withdrawn as a strace artefact. T1, T3, T5: does not cover (sysprof captures attached as `.syscap` uploads, not fetched: GitLab uploads require the web session). One observation: yes — one machine (AMD GPU, 32 GB RAM, CPU model not named), one program (gnome-shell/Mutter 49.3), states idle-after-gaming and fresh login, windows 5 s (schedstat) and 20 s (sysprof).

### S3-07 — KDE bug 525537 (plasmashell and kwin_wayland CPU per 60 s idle, 2026)

**Citation.** gauge2, "After resume from suspend, plasmashell desktop window repaints continuously at full refresh rate (~10% CPU idle), until plasmashell is restarted", KDE bug 525537, product plasmashell, component generic-performance, version 6.7.5, filed 2026-09-11, UNCONFIRMED; comments by Nate Graham and rafal@siliconet.pl.
**Copy read.** https://bugs.kde.org/rest/bug/525537 and https://bugs.kde.org/rest/bug/525537/comment, accessed 2026-09-20 (200 both), local `sources/S3-07/kde-525537.json` SHA-256 `aeb0af3baec6b4272d4c6d1e7226dfba9237a6e73c516a762ad5c43080434ad1` and `sources/S3-07/kde-525537-comments.json` SHA-256 `031f73f20e575542e172ca58bb8b10424ffc10a1cf09ecf9146974f3e52594cf`.

**Passages.** Comment 2546375 (reporter, 2026-09-11):
> After resuming from suspend (closing and reopening the laptop lid), plasmashell's desktop window begins repainting continuously at the display's full refresh rate (120 Hz), even though nothing on the desktop changes. This makes plasmashell use about 10% of a CPU core while the system is idle, and kwin_wayland about 8% compositing those frames. The state persists indefinitely until plasmashell is restarted, after which both drop to ~0%.
> 1. Log in to a Plasma Wayland session. Confirm plasmashell and kwin_wayland are idle (0-1 s of CPU time per 60 s, measured with the command under ADDITIONAL INFORMATION).
> - After resume, plasmashell uses 4-6 s and kwin_wayland ~5 s of CPU time per 60 s of complete idle (normal is 0 s for both).
> KDE Plasma Version: 6.7.5
> Kernel: 7.2.2-artix1-1.1
> Graphics Processor: Intel Arc B390
> CPU: Intel Core Ultra X9 388H
> Laptop model: Framework Laptop 13 pro
> Display: 2880x1920 @ 120 Hz, VRR off, HDR off
> CPU time consumed over exactly 60 seconds of no keyboard/mouse input:
> k=$(pgrep -x kwin_wayland); p=$(pgrep -x plasmashell); a1=$(ps -p $k -o times=); b1=$(ps -p $p -o times=); sleep 60; a2=$(ps -p $k -o times=); b2=$(ps -p $p -o times=); echo "kwin: $((a2-a1))s  plasmashell: $((b2-b1))s  (per 60s)"
> Before suspend / after a plasmashell restart:  kwin: 0s  plasmashell: 0s
> After suspend + resume:                        kwin: 5s  plasmashell: 4-6s
> While in the bad state, stopping plasmashell (kquitapp6 plasmashell) and measuring kwin_wayland alone for 60 s gave 0 s of CPU time. kwin's usage is entirely a consequence of plasmashell submitting new frames.
> Idle, healthy plasmashell: all threads at ~0%.
> After resume, the busy threads are:
>   QSGRenderThread   2.7%
>   plasmashell       2.0%   (main/GUI thread)
>   WaylandEventThr   1.3%
>   WaylandEventThr   1.3%
>   QThread           1.0%

Comment 2548760 (rafal@siliconet.pl, 2026-09-19, second machine, Arch Linux, Plasma 6.7.5, Framework Laptop 13 Pro with Intel Core Ultra X7 358H, 120 Hz built-in display):
> I cannot reproduce this bug - see my stats below - first measure is after a fresh cold boot, the second one is after resume from suspend.
> kwin: 0s  plasmashell: 1s  (per 60s)
> kwin: 0s  plasmashell: 0s  (per 60s)

Comment 2548813 (reporter, 2026-09-19):
> Before suspend: 7 commits on that surface (static wallpaper, as expected).
> After resume: 4,305 commits total, at a sustained ~119 commits/sec on a 120 Hz panel, indefinitely, with no content change on screen.
> strace -c over 10s in the bad state: 35,017 futex, 15,718 ioctl, 7,076 poll, 4,800 recvmsg (2,400 EAGAIN), 4,800 getpid — far above the ~120/s a 120 Hz frame loop would need.

**Coverage.** T2: covers — object: plasmashell and kwin_wayland (Plasma 6.7.5, Wayland) on two Framework Laptop 13 Pro machines (Intel Core Ultra X9 388H / X7 358H, Intel Arc B390, 120 Hz panel); unit: seconds of CPU time per 60 s of no input (`ps -o times`), per-thread %CPU from `top -H`, Wayland commits per second; statistic: point readings — healthy idle 0–1 s/60 s for both processes (i.e. ≤ 1.7 % of one CPU), the bug state 4–6 s (plasmashell) and ~5 s (kwin_wayland) per 60 s at 119 commits/s; the compositor's per-frame cost appears as ~5 s/60 s for ~120 frames/s ≈ 0.7 ms of kwin_wayland CPU per composited frame of a static full-screen surface (my arithmetic, not a stated value). State: idle desktop with nobody present (60 s no input), screen not blanked; kernel 7.2.x, Artix (dinit/elogind) and Arch. T1, T3, T5: does not cover. One observation: yes for each of two machines, subject programs and versions named, window 60 s.

### S3-08 — PipeWire issue #3863 (PowerTOP while playing, 2024)

**Citation.** Paul Menzel (pmenzel), "`pipewire` uses 2.44 W according to PowerTOP", pipewire/pipewire issue #3863, opened 2024-02-21, closed (reply by Wim Taymans).
**Copy read.** https://gitlab.freedesktop.org/api/v4/projects/pipewire%2Fpipewire/issues/3863 and https://gitlab.freedesktop.org/pipewire/pipewire/-/issues/3863/discussions.json, accessed 2026-09-20 (200 both), local `sources/S3-08/pipewire-pipewire-3863.json` SHA-256 `5c8a33aadc96ddb537a4c4e6824d3eba4ac0cab5b3a872a3b8ee8b60f10596de` and `sources/S3-08/pipewire-pipewire-3863-discussions.json` SHA-256 `f7cb6cb971f196f9526be317ae4df6d12708c6e52d75eae98fda6c8a16879513`.

**Passages.** Description:
> On a Dell XPS 13 9360 with Debian sid/unstable with *pipewire* 1.0.3-1 and *wireplumber* 0.4.17-1+b1, when playing a file in MuseScore3 3.2.3 PowerTOP 2.15 shows a usage of 2.44 W.
> Summary: 545.0 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 40.1% CPU use
> Power est.              Usage       Events/s    Category       Description
>   5.64 W    100.0%                      Device         USB device: USB 10/100/1000 LAN (Realtek)
>   2.44 W      0.0 us/s      0.00        Process        [PID 1490] /usr/bin/pipewire
>   2.36 W      0.0%                      Device         Display backlight
>       2.44 W    100.0%        Audio codec hwC0D0: Realtek (pipewire )

Note 2292071 (wtaymans, 2024-02-21):
> Is this bad? nothing we can do about that, kernel driver problem, likely.

**Coverage.** T2: covers weakly — object: the `pipewire` process (1.0.3, WirePlumber 0.4.17) on a Dell XPS 13 9360 (Debian sid, PowerTOP 2.15) while MuseScore3 plays; unit: PowerTOP power estimate and Events/s; statistic: one refresh — the process row shows `0.0 us/s 0.00` events (PowerTOP attributes the audio codec's 2.44 W to the pipewire process as the device's user, not measured CPU), whole machine 545.0 wakeups/s and 40.1 % CPU; the machine-level figure includes MuseScore. State: playing. T1, T3, T5: does not cover. One observation: yes — machine, distribution, program versions and state named; window: one PowerTOP refresh.

### S3-09 — Red Hat bug 1944646 (systemd-oomd CPU at idle, Fedora 34)

**Citation.** ego.cordatus, "[oomd] CPU usage 1.3% is somewhat to high", Red Hat Bugzilla 1944646, product Fedora, component systemd, version 34, filed 2021-03-30, CLOSED; comments by Zbigniew Jędrzejewski-Szmek (zbyszek), tavi, williambader.
**Copy read.** https://bugzilla.redhat.com/rest/bug/1944646 and https://bugzilla.redhat.com/rest/bug/1944646/comment, accessed 2026-09-20 (200 both), local `sources/S3-09/rh-1944646.json` SHA-256 `270422df48df0e33c46ad742afdf3ee87d0bf8aacb0990df2569ad8216329b09` and `sources/S3-09/rh-1944646-comments.json` SHA-256 `833a989a8251b4f4e3c4295cd90f2b3d4e613b9c0780d1514cb28a3139541b72`.

**Passages.** Comment 14921063 (reporter, 2021-03-30):
> The new one 'systemd-oomd' is replaced old one 'earlyoom' in f34. The CPU utilization is to high compared with earlyoom. systemd-oomd consumes 0.7-1.3% on Ryzen CPU (Zen 2). earlyoom usage was nearly zero.
> Tested on Fedora 34 Workstation (GNOME). KDE users reporting the same results.
> systemd-248~rc4-3.fc34
> * Current CPU usage: 0.7-1.3%.
> * TIME+: in top after the 'gnome-shell' process.

Comment 15011957 (tavi, 2021-04-29):
> On older systems systemd-oomd is non-stop 6-10% CPU usage.
> After a few hours of uptime, it consistently has more TIME+ then gnome-shell.

Comment 15162744 (williambader, 2021-06-08):
> On my laptop with Fedora 34 and MATE Desktop, systemd-oomd has the second highest total CPU in top.
> The only process with more CPU is Xorg, and systemd-oomd has about half of the total CPU as Xorg.
> I have kernel 5.12.9-300.fc34.x86_64 and systemd-248.3-1.fc34.x86_64

Comment 15576068 (zbyszek, 2021-10-12):
> systemd-248.4-1.fc34 included the patch to improve oomd resource usage:
> * 50fe0594d2 oomd: don't collect candidate stats on every interval

**Coverage.** T1: covers — object: systemd-oomd (systemd 248~rc4 to 248.3) on Fedora 34 desktops; unit: `top` %CPU and cumulative TIME+ relative to gnome-shell / Xorg; statistic: 0.7–1.3 % on a Zen 2 Ryzen, 6–10 % "on older systems", "about half of the total CPU as Xorg" on a MATE laptop; state: normal desktop use (not stated as idle); a treatment/mechanism fix (stats no longer collected every interval) closed it. T2: covers only by ratio (systemd-oomd's cumulative CPU exceeding gnome-shell's after hours of uptime). T3, T5: does not cover. One observation: several reporters, machines only partly named (Ryzen Zen 2; a laptop with 5.12.9 kernel), no window.

### S3-10 — Fedora Magazine, "Performance Profiling in Fedora Linux" (2024)

**Citation.** Christian Hergert, "Performance Profiling in Fedora Linux", Fedora Magazine, posted January 31, 2024.
**Copy read.** https://fedoramagazine.org/performance-profiling-in-fedora-linux/, accessed 2026-09-20 (200), local `sources/S3-10/fedoramagazine-performance-profiling.html` SHA-256 `3e4f869df46a3b85bfb74e0c1cc03beed4d22dbb8972ea9cbf66a84084dbe86f`; text extraction `sources/S3-10/fedoramagazine-performance-profiling.txt` SHA-256 `8fc3e8f83c47aee93b1c65a4fc925e47afd565bc8032f7a6ad13cd4b9a1846e4`.

**Passages.** (txt lines 168–172)
> systemd-oomd
> Ensuring systems stay idle when unused is essential to improving battery life.
> A quick recording, while my laptop was otherwise idle, kept revealing systemd-oomd multiple times per-second. How curious!
> A quick look at the code, and a post to the mailing list, showed that this was expected behavior but one that could potentially be avoided.
> One very small patch later we start to achieve longer periods of time without any code waking up the CPU. Exactly what we’re looking for!

**Coverage.** T1: covers weakly — object: systemd-oomd on the author's laptop (Fedora 39/40 era, machine not named); unit: sysprof samples; statistic: qualitative only ("multiple times per-second" while idle); state: idle laptop. T3: covers weakly (the stated goal "longer periods of time without any code waking up the CPU", no number). T2, T5: does not cover. One observation: yes, but no machine, version or window named.

### S3-11 — lkml, Doug Smythies on powertop and an idle headless server (2016)

**Citation.** Doug Smythies, "RE: regression caused by bb6ab52f2bef ("intel_pstate: Do not set utilization update hook too early")", linux-kernel mailing list, Thu Jun 23 2016 12:14:17 EST.
**Copy read.** https://lkml.iu.edu/1606.2/06623.html, accessed 2026-09-20 (200), local `sources/S3-11/lkml-1606.2-06623.html` SHA-256 `d58e26e64c96b93da293b9a2613250bf9c1a4e6dcab3518b4aa3837fbde22b57`; text extraction `sources/S3-11/lkml-1606.2-06623.html.txt` SHA-256 `d5a5f9b29e20eb888d3ec322a8b0dec2ad78a3aeaa4f247b767ba106dc2f179e`.

**Passages.** (txt lines 15–16, 26–27, 30–39, 42–44, 79–80)
> Isn't running powertop itself a significant contributor here?
> When running powertop, the system is no longer "idle".
> Note 1: On my system (server, no GUI), I could only get down to an "idle" of around
> 20 wakeups / second, after turning off Samba, mysql, apache, cron.
> As a function of sample time:
> Sample time (seconds)	Events/second
> 300				~20
> 200				~20
> 100				~22
>  50				~29
>  30				~33
>  20				~44
>   3				~155
> If I leave mysql running, chosen because while idling it has a fairly high number
> of events per second, no increase in wakeups per second is observed before or after the commit
> in question here (it is always around 25 Events / second).
> On my, otherwise idle, system package power goes up by about 1 watt while running powertop
> (with a sample time of 5 seconds) (from ~3.9 to ~4.9 watts).

**Coverage.** T3: covers as the headless contrast — object: a whole idle server without GUI (Intel, kernel 4.7-rc3/rc4, CPU model not named); unit: wakeups (events) per second, package watts; statistic: ~20 wakeups/s floor with Samba, mysql, apache and cron stopped; and the instrument effect table (powertop's own sampling raises the reading from ~20 at 300 s to ~155 at 3 s). T1: covers weakly — mysql idle "always around 25 Events / second" (a service, not one of the listed system daemons). T2, T5: does not cover. One observation: yes — one server, state idle headless, windows 3–300 s per row.

### S3-12 — Fedora Discussion 150603 (tick_nohz_handler on an idle GNOME Wayland laptop, 2025)

**Citation.** nekohayo, "Why is "tick_nohz_handler" showing up as waking up the CPU hundreds of times per second in powertop?", Fedora Discussion topic 150603, 2025-04-26; replies by adamwill, barryascott, crystalshower (2025-05-07).
**Copy read.** https://discussion.fedoraproject.org/t/150603.json, accessed 2026-09-20 (200), local `sources/S3-12/fedora-discussion-150603.json` SHA-256 `6c29bc4c13063f7136751a41660381b8b54fde0387d70c42aaf7f1eb0602172d` (Discourse post stream; post text in `cooked` HTML).

**Passages.** Post 1:
> I’m running Fedora 42’s Wayland GNOME session with Linux kernel 6.14.2 on a ThinkPad T480 (Intel Core i5-8350U CPU), with only a single GPU (Intel Kabylake chipset) connected to two external monitors at 60 Hz, connected to AC power in the default “Balanced” power mode… and I’ve been puzzled by the tick_nohz_handler timer item consistently showing up in powertop at the top of things waking up the CPU, no matter what I do with the computer sitting idle:
> On another computer with AMD CPU+GPU, with only a logged in GNOME Shell Wayland session with no apps running, I still see the tick happening, albeit less frequently than on my own computer:
> what is going on, is it normal to be seeing so many wakeups (between 200 to 700 per second) from that thing?

Post 4 (barryascott):
> On my KDE plasma desktop I see 700 events/second which is better then the 1,000 that the 1000Hz clock would generate. That is a 30% saving in CPU for timers.

Post 5 (crystalshower):
> On EndavourOS KDE, tick_nohz_handler operate below 500 event/s.

**Coverage.** T3: covers weakly — object: the kernel tick (`tick_nohz_handler`) on idle GNOME Wayland (Fedora 42, 6.14.2, ThinkPad T480) and idle KDE sessions; unit: powertop Events/s; statistic: 200–700 /s (T480, two 60 Hz external monitors), "less frequently" on an AMD machine with no apps, 700 /s on a Plasma desktop, below 500 /s on EndeavourOS KDE; the powertop process tables are screenshots, so no per-process row is quotable. T1, T2, T5: does not cover. One observation: several, machines partly named, state idle logged-in session, window unspecified.

### S3-13 — Linux Mint forum 414319 (powertop on a MATE/Xorg laptop, 2024)

**Citation.** NatS, "Powertop Behaving Oddly", Linux Mint Forums, Tue Feb 20, 2024 6:55 pm.
**Copy read.** https://forums.linuxmint.com/viewtopic.php?t=414319, accessed 2026-09-20 (200), local `sources/S3-13/linuxmint-414319.html` SHA-256 `3e13328e1b02513d4e0478b413a0038273a021873a2e9da999cc07d087292fc1`; text extraction `sources/S3-13/linuxmint-414319.html.txt` SHA-256 `90d1487524391a43e7ce62df9678c321b93a851a88defb3a9efbced0462b746d`.

**Passages.** (txt lines 37, 40–47, 56–58, 63)
> I have been using powertop a bit to figure out what is going on when my computer keeps spinning up fans for no reason, but recently I can't get it to work like it used to. The only thing I really did was move from the cinnamon to the MATE environment though I did fully wipe and reinstall to do so (did I maybe forget some drivers or something on the reinstall?)  Here is a current usage of powertop
> Summary: 685.5 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 12.2% CPU use
>                 Usage       Events/s    Category       Description
>               2.8 ms/s     256.0        Timer          tick_sched_timer
>               4.7 ms/s      60.1        Process        [PID 4015] /usr/lib/firefox/firefox
>               0.8 ms/s      56.2        kWork          engine_retire
>               1.3 ms/s      52.4        Interrupt      [0] HI_SOFTIRQ
>             573.5 µs/s      31.0        Process        [PID 14] [rcu_sched]
>              10.7 ms/s      21.3        Process        [PID 5751] powertop
>               2.0 ms/s       9.7        Process        [PID 1796] mate-system-monitor
>             108.1 µs/s       8.7        kWork          psi_avgs_work
>              15.9 ms/s       1.0        Process        [PID 1130] /usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolis
>               1.1 ms/s       3.9        Process        [PID 3415] mate-terminal

**Coverage.** T2: covers weakly — object: Xorg (lightdm, MATE session, Intel i915 graphics per the interrupt rows) on an unnamed laptop, Linux Mint 21-era; unit: powertop Events/s and ms/s; statistic: one refresh — Xorg 1.0 wakeups/s but 15.9 ms/s CPU, with Firefox and mate-system-monitor open. T3: covers weakly — whole machine 685.5 wakeups/s, 12.2 % CPU, tick_sched_timer 256 /s, in that (non-idle) state. T1: covers only rcu_sched 31.0 /s; no system service row. T5: does not cover. One observation: yes; machine not named; state: desktop with browser open; window: one refresh.

### S3-14 — Arch Linux forum 252284 (powertop on an i3/xcompmgr laptop, 2020)

**Citation.** NotKudo, "Annoying "Timers" Causing Huge Battery Drain", Arch Linux Forums, Laptop Issues, thread 252284, post #1 2020-01-19 18:51:25 (with two later edits/pastes in the same post).
**Copy read.** https://bbs.archlinux.org/viewtopic.php?id=252284, accessed 2026-09-20 (200), local `sources/S3-14/arch-252284.html` SHA-256 `fcec7e7898100c313c87d5b813f7fe4504317ae336c7580beeb07589c2649048`; text extraction `sources/S3-14/arch-252284.html.txt` SHA-256 `536e8eb79018b089a505e674a4c35fa69b527427b840a3bd96d5c490e5d3be6f`.

**Passages.** (txt lines 32, 34, 37–42, 46, 50, 54)
> - My battery life on my Predator Helios 300 2019 gets about 5 hours when on Windows 10 and I should be able to get about 4 hours in Arch. However my battery is draining severely when no processes are opening and Powertop is showing that these two timers are taking a significant chunk of that. My battery drain is really bad to the point where I only have 1 hour and 51 minutes on full charge when idle. This powertop was taken at 28% battery. Can I get any help with this please as I am deseperate to do anything to continue using arch and move away from windows. Thanks a ton guys
> The battery reports a discharge rate of 40.4 W
> Summary: 1858.4 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 11.0% CPU use
> Power est.              Usage       Events/s    Category       Description
>   4.77 W     11.6 ms/s     1203.4       Timer          hrtimer_wakeup
>   1.35 W      2.2 ms/s     340.2        Timer          tick_sched_timer
>   443 mW     14.4 ms/s     106.5        Process        [PID 19925] powertop
>   106 mW      2.0 ms/s      23.6        Process        [PID 19880] kitty
>  59.8 mW      2.5 ms/s      14.1        Process        [PID 988] /usr/lib/Xorg -nolisten tcp -auth /var/run/sddm/{596af6c5-c859-4042-91ed-21147dd7df41} -background none -noreset -dis
>  48.6 mW    143.0 µs/s      12.3        Process        [PID 11] [rcu_preempt]
>  36.9 mW    392.0 µs/s       8.5        Process        [PID 1082] xcompmgr

Later paste in the same post (txt lines 237–239, 248, 257):
> Summary: 4696.2 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 44.3% CPU use
> Power est.              Usage       Events/s    Category       Description
>   6.69 W     84.3 ms/s     1510.4       Process        [PID 1182] /usr/lib/firefox/firefox
>   281 mW     59.8 ms/s      47.4        Process        [PID 869] /usr/lib/Xorg -nolisten tcp -auth /var/run/sddm/{110b076a-d447-48f
>  79.8 mW      1.3 ms/s      19.0        Process        [PID 1043] xcompmgr

**Coverage.** T2: covers weakly — object: Xorg (sddm) and xcompmgr on an Acer Predator Helios 300 (2019, Intel/NVIDIA hybrid, Arch, i3 session per the i3blocks rows); unit: powertop Events/s and ms/s; statistic: Xorg 14.1 /s and 2.5 ms/s, xcompmgr 8.5 /s at "idle" with a terminal and Firefox processes present; Xorg 47.4 /s and 59.8 ms/s with Firefox active. T3: covers weakly — whole machine 1858.4 wakeups/s and 11.0 % CPU at "idle", dominated by hrtimer_wakeup 1203.4 /s and tick_sched_timer 340.2 /s (a laptop with a fan-control mono service and a power-management bug, not a clean idle). T1: covers only rcu_preempt 12.3 /s. T5: does not cover. One observation: yes; machine named; kernel not; window: one refresh.

### S3-15 — Perfetto test trace `ui-funcgraph.pftrace` (Linux x86_64 6.9.0-rc7)

**Citation.** Google Perfetto test data, file `test/data/ui-funcgraph.pftrace` (index entry `ui-funcgraph.pftrace.sha256` in the perfetto repository's `test/data/`), a Linux system trace used by Perfetto's UI tests.
**Copy read.** Download URL https://storage.googleapis.com/perfetto/test_data/ui-funcgraph.pftrace-4262c95bce220236289f70ec66f7c97b2133eefe6d380d09c6cc7217a41309c4 (the hash suffix comes from https://android.googlesource.com/platform/external/perfetto/+/refs/heads/main/test/data/ui-funcgraph.pftrace.sha256?format=TEXT), accessed 2026-09-20 (200, 58 391 230 bytes), local `sources/S3-15/ui-funcgraph.pftrace`, SHA-256 `4262c95bce220236289f70ec66f7c97b2133eefe6d380d09c6cc7217a41309c4` (matches the index). The decoded index listing is saved as `sources/S3-15/perfetto-test-data-listing.txt`, SHA-256 `d587984b638289d5362f715e2f7a95906c330bc473f5a300fd7bbb6b68ebc902`.

**Passages.** None quotable (binary protobuf); the trace's own metadata fields, read with the trace processor (`select name, str_value from metadata`), are: `system_name` = `Linux`, `system_release` = `6.9.0-rc7`, `system_version` = `#4 SMP PREEMPT_DYNAMIC Tue May  7 14:32:13 PDT 2024`, `system_machine` = `x86_64`, `trace_type` = `proto`, no `android_build_fingerprint`.

**Own computation** (perfetto Python package 0.58.2, trace_processor_shell v57.2; script: `from perfetto.trace_processor import TraceProcessor; tp=TraceProcessor(trace="ui-funcgraph.pftrace")` then `select (max(ts)-min(ts))/1e9, count(*) from sched` → 3.273 s, 21 264 rows; `select count(distinct cpu) from sched` → 8; `select count(distinct utid) from thread` → 96, `select count(*) from process` → 26; `select t.name, count(*), sum(dur)/1e6 from sched s join thread t using(utid) where t.name not in ('swapper') group by 1 order by 2 desc` → iperf 9725 rows / 2076.2 ms, cyclictest 4020 / 32.0 ms, tracebox 3113 / 1466.1 ms, dd 3046 / 1873.6 ms, kworker/u32:3 427, …, avahi-daemon 12 rows / 0.834 ms, pipewire-media- 10 rows / 0.356 ms, gmain 3 / 0.263 ms, sshd 2 / 0.172 ms, NetworkManager 2 rows / 0.171 ms, wpa_supplicant 1 row / 0.025 ms; `select name, count(*) from ftrace_event group by 1` → sched_stat_runtime 30 922, sched_wake_idle_without_ipi 113; `select count(*) from thread_state where state='R' and waker_utid is not null` → 10 697 runnable intervals with a recorded waker). No thread named systemd, journald, dbus, Xorg, gnome-shell or kwin appears; the machine is a Linux box running a latency test script (`test-latency.sh`, `trace-me.sh`) with iperf, cyclictest and dd, over sshd.

**Coverage.** T5: covers — object: a Perfetto proto trace of a Linux 6.9.0-rc7 x86_64 8-CPU machine; fields: `sched` (per-thread slices with ts, dur, cpu, end_state), `thread_state` with waker, `ftrace_event` rows for sched_stat_runtime and sched_wake_idle_without_ipi, process/thread tables (comm, pid, tid), funcgraph data (the file's purpose); scope: 3.27 s of a synthetic latency test, not idle, not a desktop session — the session daemons present are pipewire-media-session (`pipewire-media-` comm, 10 sched-ins in 3.27 s while otherwise unused), avahi-daemon, NetworkManager, wpa_supplicant. The other seven Perfetto test traces examined are Android (search log #41). T1: covers only as the presence and sched-in counts above, in a loaded not idle machine. T2: covers weakly (pipewire-media-session rows, no stream playing). T3: does not cover. One observation: yes — one trace, machine not named beyond the kernel string, state "running iperf/cyclictest/dd", window 3.27 s.

### S3-16 — LTTng reference traces: `basic-kernel-analysis.sh` and the EfficiOS CTF trace index

**Citation.** lttng/lttng-ref-traces, `traces/basic-kernel-analysis.sh` (the recording script of the "basic-kernel-analysis" reference kernel trace); EfficiOS, "Index of /pub/ctf/traces" (two CTF trace archives, `auto-20110713-104006.tar.bz2` 58M and `trace1.tar.bz2` 2.4M, both dated 2025-10-21 in the index).
**Copy read.** https://raw.githubusercontent.com/lttng/lttng-ref-traces/master/traces/basic-kernel-analysis.sh, accessed 2026-09-20 (200), local `sources/S3-16/lttng-basic-kernel-analysis.sh` SHA-256 `fd44a0a8fd9bae4ee8538f9df4f0146c0a0f07d4737d79bb6ca832d74939cf42`; https://www.efficios.com/pub/ctf/traces/, accessed 2026-09-20 (200), local `sources/S3-16/efficios-pub-traces.html` SHA-256 `3da6852445725cc13c93a026dd5724ed6ff189103fd0c3fbdbee630aa550e94a`, text `sources/S3-16/efficios-pub-traces.html.txt` SHA-256 `0d7fbadf5acedcac69f1734fd904418c36a252d2220eb9832f91e9a4f51bc6df`. The repository README (which the search engine summarised as describing "16-cores-rt, a real kernel trace of 2 seconds recorded with LTTng 2.9.0-pre on a 16 cores server" and "basic-kernel-analysis, a real kernel trace of ~5 seconds recorded with LTTng 2.10") returned 404 through raw.githubusercontent.com for README.md on master and main and for README.adoc, so those descriptions are not quotable here; the trace archives themselves were not downloaded.

**Passages.** `basic-kernel-analysis.sh` lines 3–9:
> lttng create basic-kernel-analysis
> lttng enable-channel -k chan1 --subbuf-size=8M
> lttng enable-event -s my-test-trace -k sched_switch,sched_wakeup,sched_waking,block_rq_complete,block_rq_issue,block_bio_remap,block_bio_backmerge,netif_receive_skb,net_dev_xmit,sched_process_fork,sched_process_exec,lttng_statedump_process_state,lttng_statedump_file_descriptor,lttng_statedump_block_device,mm_vmscan_wakeup_kswapd,mm_page_free,mm_page_alloc,block_dirty_buffer,irq_handler_entry,irq_handler_exit,softirq_entry,softirq_exit,softirq_raise,irq_softirq_entry,irq_softirq_exit,irq_softirq_raise,kmem_mm_page_alloc,kmem_mm_page_free -c chan1
> lttng enable-event -s my-test-trace -k -c chan1 --syscall -a

Lines 13–14, 26–27, 38–39, 44–45:
> echo "Send 2 ping request to google.com" > /proc/lttng-logger
> ping -c 2 google.com
> echo "Sleep for 2 seconds" > /proc/lttng-logger
> sleep 2
> echo "Extract the tarball" > /proc/lttng-logger
> tar xf tree-1.7.0.tgz
> echo "Build with 'make -j4'" > /proc/lttng-logger
> make -j4

EfficiOS index (txt lines 2–8):
> Index of /pub/ctf/traces
> auto-20110713-104006.tar.bz2
> 2025-10-21 14:39
>  58M
> trace1.tar.bz2
> 2025-10-21 14:39
> 2.4M

**Coverage.** T5: covers as a dataset pointer — object: an LTTng kernel reference trace of a scripted workload (ping, wget, dd, gzip, `make -j4`, a 2 s `sleep`); fields: sched_switch, sched_wakeup, sched_waking, block, net, irq/softirq, statedump events and all syscalls; scope: not idle, machine not named in the script; the 2011 `auto-20110713-104006` archive on efficios.com is a 2011-era trace (context by the two-decade rule's spirit; not downloaded). T1, T2, T3: does not cover. One observation: not applicable (a recording script; the trace was not read).

### S3-17 — GNOME gnome-shell issue #3858 (sysprof of gnome-shell at idle, 2021)

**Citation.** Christian Hergert (chergert), "Excessive CPU spin at idle", GNOME/gnome-shell issue #3858, opened 2021-03-11, closed 2021-07 (fixed by a mutter commit per the last notes).
**Copy read.** https://gitlab.gnome.org/api/v4/projects/GNOME%2Fgnome-shell/issues/3858 and https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/3858/discussions.json, accessed 2026-09-20 (200 both), local `sources/S3-17/GNOME-gnome-shell-3858.json` SHA-256 `170095f80db30751537b3f9c36338b4c293734e60770ae00db80728d00c5cfe2` and `sources/S3-17/GNOME-gnome-shell-3858-discussions.json` SHA-256 `74c61073afa6d4510e88f8aed5e7a44be5d1edd7e69ce1df1b7dc53a1592dcee`.

**Passages.** Description:
> I've been running 40.rc in Fedora 34 for a while now and I've been seeing an awful lot of CPU churn while idle (in betas too). Anywhere from 30-60%. It generally seems to happen after coming back from suspend. I usually only notice because my battery dies so quickly.
> After installing glib2-debuginfo, it appears that a majority of the time is getting spent in `g_source_unref_internal()`. Sadly I don't have enough stack pointers to get more info than that from perf/Sysprof.
>       SELF      TOTAL    FUNCTION
> [   0.00%] [ 100.00%]    [Everything]
> [   0.00%] [  72.30%]      [/usr/bin/gnome-shell]
> [  28.85%] [  28.97%]        g_source_unref_internal
> [  24.58%] [  24.79%]        g_source_ref
> [  11.59%] [  11.68%]        g_source_iter_next

Note 1101202 (gnumdk, 2021-05-08):
> Killing Xwayland fixes the issue here.

**Coverage.** T2: covers weakly — object: gnome-shell 40.rc on Fedora 34 after resume from suspend (a bug state); unit: %CPU and sysprof sample shares; statistic: 30–60 % CPU "while idle", 72.30 % of samples in gnome-shell, of which GLib main-loop source ref/unref dominate. T1, T3, T5: does not cover. One observation: yes; machine not named; state idle-after-resume; window not stated.

### S3-18 — KDE bug 460248 (plasmashell CPU at idle on Wayland, Plasma 5.26, 2022)

**Citation.** chn.isik, "plasmashell with high CPU usage in Wayland session", KDE bug 460248, product kwin, component wayland-generic, version 5.26.0, filed 2022-10-11, RESOLVED.
**Copy read.** https://bugs.kde.org/rest/bug/460248 and …/comment, accessed 2026-09-20 (200 both), local `sources/S3-18/kde-460248.json` SHA-256 `f3d28e0cef0b408880668b5ff79e2d44367e4a67c9f8c6ea4b8321acd7f0fb8b` and `sources/S3-18/kde-460248-comments.json` SHA-256 `3231a878f2f9c086f2f0ad20c74e129b8e83727d3dd509246d7acbca41a2a3bf`.

**Passages.** Comment 2159951 (reporter):
> I just updated to Plasma 5.26 and immediatly noticed that plasmashell is constantly using up 70-90% CPU in idle without anything else happening. It only happens when in a Wayland session, X session CPU usage is fine. Tested on both a Thinkpad E14 Gen 2 with AMD IGPU and on desktop with an AMD RX 6600XT discrete GPU.

Comment 2160243 (reporter, `perf top -K`):
>    4.60%  [vdso]                                   [.] __vdso_clock_gettime
>    2.23%  libwayland-client.so.0.21.0              [.] wl_proxy_marshal_array_flags
>    1.65%  libglib-2.0.so.0.7400.0                  [.] g_main_context_check

Comment 2160562 (bugseforuns@gmx.com):
> On my Arch Linux plasmashell uses 30% and kwin_wayland uses 20% of cpu all the time. This does not occur on X11.

**Coverage.** T2: covers weakly — object: plasmashell and kwin_wayland (Plasma 5.26.0 Wayland) in a bug state; unit: %CPU; statistic: 70–90 % (plasmashell) on a ThinkPad E14 Gen 2 and an RX 6600XT desktop; 30 % / 20 % on another Arch machine. T1, T3, T5: does not cover. One observation: several reporters, machines partly named, state idle (bug), no window.

### S3-19 — KDE Discuss 32396 (kwin_wayland and plasmashell ~10 % at idle, Plasma 6.3.4, 2025)

**Citation.** giotft, "High CPU usage by kwin_wayland and plasmashell when idle", KDE Discuss, Help, topic 32396, 2025-04-03 to 2025-04-14; replies by meven.
**Copy read.** https://discuss.kde.org/t/32396.json, accessed 2026-09-20 (200), local `sources/S3-19/kde-discuss-32396.json` SHA-256 `809145fac1f3f8b4bafef5a1529f655bfdc6fc6c734e8fcd83ce3ec0ba09f72b`.

**Passages.** Post 1:
> On my desktop I notice that kwin_wayland and plasmashell have CPU usage of around 10% even when there is essentially nothing open / running. I don’t have any fancy desktop widgets either.

Post 4:
> Yes, about 10% CPU usage of both kwin_wayland and plasmashell.
> Operating System: Arch Linux 
> KDE Plasma Version: 6.3.4
> Graphics Platform: Wayland
> Processors: 16 × Intel® Core™ i9-9900 CPU @ 3.10GHz
> Graphics Processor: Mesa Intel® UHD Graphics 630
> So far the problem hasn’t returned (with instant animations).

**Coverage.** T2: covers weakly — object: kwin_wayland and plasmashell (Plasma 6.3.4, Qt 6.8.3, Wayland, i9-9900 with UHD 630); unit: %CPU; statistic: "around 10%" each at idle, gone after setting animation speed to instant (no measurement of the fixed state). T1, T3, T5: does not cover. One observation: yes; machine named; state idle; window not stated.

### S3-20 — systemd issue #21751 (systemd and systemd-udevd CPU after resume, 2021)

**Citation.** "systemd an systemd-udevd CPU use is high after wakeup probably due to power_supply BAT0 (battery) continued polling", systemd/systemd issue #21751, opened December 2021 (systemd 249, Manjaro, Dell Latitude 3520); later comments quoting Launchpad bug 1944409 (Ubuntu 20.04.3, systemd 245.4, Dell Latitude 7520).
**Copy read.** Wayback capture https://web.archive.org/web/2023id_/https://github.com/systemd/systemd/issues/21751 (resolved capture of 2023, server-rendered, 20 comment bodies), accessed 2026-09-20 (200), local `sources/S3-20/systemd-21751-wayback.html` SHA-256 `707b2030ce5f66ae3fce9a9a820e9d1db3e54770ac1cdd44e7beeeb537fc4226`.

**Passages.** Issue body (first comment-body block; the HTML carries these as list items):
> Check top to see that the system load is around 3-4 and systemd-udevd and systemd CPU usage is higher then expected.
> UDEV  [15432.793289] change   /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0C0A:00/power_supply/BAT0 (power_supply)
> UDEV  [15432.904367] change   /devices/LNXSYSTM:00/LNXSYBUS:00/PNP0C0A:00/power_supply/BAT0 (power_supply)

Ninth comment body (quoting Launchpad 1944409):
> I leave my laptop docked and, after waking it up from sleep, the fans start blowing. After a quick inspection with top/htop, I always see /usr/lib/systemd/systemd-udev consuming 50+% of my CPU.

Sixth comment body:
> It seems like upgrading to BIOS 1.13.3 on Latitude 3520 seems to have solved the issue.

**Coverage.** T1: covers weakly — object: systemd (pid 1) and systemd-udevd reacting to a firmware-driven storm of `power_supply/BAT0` change uevents about every 110 ms (own reading of the two timestamps above: 15432.793 → 15432.904); unit: load average and %CPU; statistic: load 3–4, udevd "50+%" (bug state, firmware-caused, fixed by a BIOS update). T2, T3, T5: does not cover. One observation: several Dell Latitude laptops; state after resume; no window.

### S3-21 — Ubuntu wiki, Kernel/PowerManagement/IdentifyingIssues (context, powertop 1.13 era)

**Citation.** Ubuntu Wiki, "Kernel/PowerManagement/IdentifyingIssues", last edited 2015-11-11 (page footer); the powertop excerpt dates from the Ubuntu 12.04 era (powertop-1.13, gwibber, ubuntuone-syncd).
**Copy read.** https://wiki.ubuntu.com/Kernel/PowerManagement/IdentifyingIssues, accessed 2026-09-20 (200), local `sources/S3-21/ubuntu-wiki-IdentifyingIssues.html` SHA-256 `4008c9003ffa027f1842a27aaadeb4e2d5c93b4aba1c217dd4ce0960045653e9`; text extraction `sources/S3-21/ubuntu-wiki-IdentifyingIssues.txt` SHA-256 `84f4031d4d58f56743279d2d4b04528de5260807b316556b277679c3e8661228`.

**Passages.** (txt lines 53–58, 472)
> sudo powertop-1.13 -d -t 60 > powertop.log
> Looking at the powertop.log you will see a section titled "Top causes for wakeups:" and this will list running processes in order of wakeups per second.  An excerpt from this is a follows:
>    1.4% ( 10.0)   gwibber-service
>    1.4% (  9.9)   ubuntuone-syncd
>    0.8% (  5.5)   [ata_piix] <interrupt>
>    0.7% (  5.0)   syndaemon
> Kernel/PowerManagement/IdentifyingIssues  (last edited 2015-11-11 15:39:29 by 1)

**Coverage.** Context only (a distribution's diagnostic guide with one 60 s powertop excerpt naming user-session daemons of 2012; no system service or compositor row). T1–T3, T5: does not cover in the sense required; recorded because the search directions asked for distribution power-management wiki data where it carries a measurement.

### S3-22 — Oracle Linux 9 PowerTOP command reference (context, KVM host)

**Citation.** Oracle, "PowerTOP Command Reference", Oracle Linux 9: Monitoring and Tuning the System (TuneD), chapter 9, sample Overview output.
**Copy read.** https://docs.oracle.com/en/operating-systems/oracle-linux/9/tuned/powertop_command_reference.html, accessed 2026-09-20 (200), local `sources/S3-22/oracle-powertop-ref.html` SHA-256 `966310616e110ca19cfd4f5f43a28a34356f1764a8481ebccb1db01ef4f59bbb`; text extraction `sources/S3-22/oracle-powertop-ref.html.txt` SHA-256 `8b432e450990eb11f3aeadaa002bc875c6290373d4351e36d5dcc12e392a5f27`.

**Passages.** (txt lines 58–68)
> Summary: 1937.4 wakeups/second,  0.0 GPU ops/seconds, 0.0 VFS ops/sec and 18.2% CPU use
>                 Usage       Events/s    Category       Description
>             119.9 ms/s     1088.4	Process        [PID 52069] /usr/libexec/qemu-kvm...
>              52.2 ms/s     663.9        Process        [PID 52068] /usr/libexec/qemu-kvm -name ...
>               1.2 ms/s      60.4        Process        [PID 1793] /usr/libexec/platform-pyth...
>               3.5 ms/s      24.7        Timer          apic_timer_fn
>              80.0 µs/s      18.8        Process        [PID 962] [xfsaild/dm-0]
>              60.1 µs/s      18.8        Process        [PID 1459] [xfsaild/dm-1]
>              34.4 µs/s      10.9        Process        [PID 15] [rcu_sched]
>              66.8 µs/s       9.9        kWork          kvmclock_update_fn
>             670.7 µs/s       7.9        Timer          tick_sched_timer

**Coverage.** T1/T3 context — a headless Oracle Linux KVM host (itself a virtual machine: kvmclock, virtio_net) with two qemu-kvm guests; the only non-guest rows are a platform-python process (60.4 /s), xfsaild kernel threads (18.8 /s each), rcu_sched (10.9 /s) and tick_sched_timer (7.9 /s); no systemd, journald or dbus row appears in the sample. Not a desktop; machine and window not named. T2, T5: does not cover.

### S3-23 — xorg/xserver issue #1531 (Xorg 30 % at idle, bug state, 2023)

**Citation.** php4fan, "xorg process consuming 30% cpu for no reason when all applications are idle", xorg/xserver issue #1531, opened 2023-03-06, open.
**Copy read.** https://gitlab.freedesktop.org/api/v4/projects/xorg%2Fxserver/issues/1531, accessed 2026-09-20 (200), local `sources/S3-23/xorg-xserver-1531.json` SHA-256 `e01206dfbb9ba74e4e5044585c8365f2b00a202c9f78403c49f3cd971873d2a7`.

**Passages.** Description:
> For a few hours now, the Xorg process has been consuming more than 30% of CPU constantly, for no apparent reason.
> Operating System: Manjaro Linux
> KDE Plasma Version: 5.26.5
> Kernel Version: 6.0.19-3-MANJARO (64-bit)
> Graphics Platform: X11
> Processors: 8 × Intel® Core™ i7-1065G7 CPU @ 1.30GHz
> Product Name: 81WE
> System Version: IdeaPad 3 15IIL05

**Coverage.** T2: covers weakly — object: Xorg under Plasma 5.26.5 X11 on a Lenovo IdeaPad 3 15IIL05 (i7-1065G7, Iris Plus); unit: %CPU; statistic: "more than 30% of CPU constantly" with applications idle (a bug state with no profile). T1, T3, T5: does not cover. One observation: yes; machine named; window "a few hours".

### S3-24 — KDE bug 486214 (kwin_wayland CPU when idle, Plasma 6.0.4, 2024)

**Citation.** billy.nlv0a, "High CPU usage on kwin_wayland when idle", KDE bug 486214, product kwin, component performance, version 6.0.4, filed 2024-04-27, UNCONFIRMED; reply by Xaver Hugl (Zamundaaa); later comment by kdedev@tlcnet.info (2024-10-22).
**Copy read.** https://bugs.kde.org/rest/bug/486214 and …/comment, accessed 2026-09-20 (200 both), local `sources/S3-24/kde-486214.json` SHA-256 `6157b764729157126da2c3ec05869ae633ab62c9dd308591338b773ba6384a5c` and `sources/S3-24/kde-486214-comments.json` SHA-256 `7946c808cbde5eb7225580b9ba1d5c90a4db27a89c07feb994efafffb30ce2d1`.

**Passages.** Comment 2314762 (reporter):
> kwin_wayland usage cpu constantly, causing higher power draw, stoping cpu from deeper sleep state
> Operating System: Fedora Linux 40
> KDE Plasma Version: 6.0.4
> Kernel Version: 6.8.7-300.fc40.x86_64 (64-bit)
> Graphics Platform: Wayland
> Processors: 16 × 12th Gen Intel® Core™ i5-1240P
> Manufacturer: Framework

Comment 2314766 (reporter):
> I left the system to idle for about 10 mins, then took this.

Comment 2314972 (Xaver Hugl):
> I don't see anything particularly weird in the flamegraph, most of the CPU time is in compositing and processing Wayland events. There is a somewhat odd QThreadPool thing in there taking up a not insignificant part of CPU time, but it's not enough to cause this issue

Comment 2368423 (kdedev@tlcnet.info):
> kwin_wayland takes 180-200% CPU from system start, and then continuously
> Plasma 6.2.1

**Coverage.** T2: covers weakly — object: kwin_wayland (Plasma 6.0.4 / 6.2.1, Wayland) on a Framework 12th-gen laptop and a KDE neon VM; the hotspot/perf data, btop, intel_gpu_top and powertop screenshots are attachments (ids 168952–168955) that were not fetched (Bugzilla attachment download not attempted; images would not be quotable); the only numbers in text are "180-200% CPU" on the VM. State: idle 10 min. T1, T3, T5: does not cover. One observation: yes for the reporter's machine; window ~10 min idle before the capture.

## 3. Not found

- **T1 — per-service wake cadence or CPU per wake at idle on Linux, with machine and window named, for `systemd` (pid 1), `systemd-journald`, `systemd-udevd`, `systemd-logind`, `systemd-resolved`, NetworkManager/`systemd-networkd`, `systemd-timesyncd`/chrony, `dbus-daemon`/`dbus-broker`, cron, polkitd, udisksd, packagekitd, rsyslogd, multipathd.** Not found as a per-service table. Searches #20, #21, #30, #44, #45, #47, #52, #53, #55, #61 (WebSearch), #35 (Red Hat Bugzilla, zero matches), #36 (kernel Bugzilla), #57 (Launchpad, zero entries) returned no powertop, perf or sysprof table naming these services with a rate; the powertop tables that were found (S3-03, S3-04, S3-13, S3-14, S3-22) list timers, kworkers, `rcu_sched`/`rcu_preempt`, the display stack and applications, and no system service appears in their quoted top rows. What exists is: `top` rows in S3-03 (dbus-daemon 0.3 %, systemd 0:06.62 cumulative over 2 d 16 h); systemd-oomd 0.7–1.3 % (S3-09) and "multiple times per-second" idle wakeups (S3-10); a firmware-driven udevd bug state (S3-20); an idle headless server floor of ~20 wakeups/s and mysql at ~25 events/s (S3-11); NetworkManager, avahi-daemon and wpa_supplicant sched-in counts in a 3.27 s loaded Linux trace (S3-15). The Gentoo thread with a 2022 powertop table (search log #33) is behind a login wall and its Wayback captures failed.
- **T2 — per-frame CPU cost of a compositor on a GPU desktop, measured and published.** Not found as a stated per-frame value. The closest are S3-07 (kwin_wayland ~5 s CPU per 60 s while compositing a 119 commits/s static surface; my division to ≈0.7 ms/frame is not the source's statement) and S3-06 (Mutter's 12 `drmModeAtomicAddProperty` calls per output frame, a mechanism). No PipeWire `pw-top` output at idle or per-period CPU figure for PipeWire/WirePlumber was found (search #22, #53; PipeWire issues #3863, #3648, #1108 read); PulseAudio was not searched separately beyond these queries. No Wayland-compositor benchmark database was reachable (phoronix.com and openbenchmarking.org 403, search #3, #48). No observation of the blanked-screen state or of "one animating window" exists in any candidate; the states found are idle-logged-in (S3-06, S3-07, S3-12, S3-19), idle-with-apps-open (S3-03, S3-04, S3-13, S3-14) and playing (S3-02, S3-08).
- **T3 — process-population statistics of an idle desktop (how many processes/threads wake, aggregate rate, service-versus-session split), and GNOME Wayland vs GNOME X11 vs Plasma vs lighter sessions.** Partly found: S3-05 gives whole-system idle interrupts, context switches, idle % and battery watts for Fedora 42 GNOME Wayland against Plasma 6.4 Wayland (two modes) and X11 on one laptop; S3-03, S3-04, S3-12, S3-13, S3-14 give whole-machine wakeups/s with a few per-process rows but no process-population count or split; S3-11 gives the headless contrast (~20 wakeups/s). Not found: any published count of woken processes/threads per interval, any split between system services and session processes, any GNOME X11 measurement newer than the 2018 KDE X11 table (S3-03), and any measurement of a lighter session (Sway/wlroots, Xfce) — searches #20, #23, #29, #44, #52, #53, #59, #60.
- **T5 — a public trace (Perfetto, ftrace, perf sched, LTTng) of an idle Linux desktop session in which system services and the display/audio servers appear.** Not found. The Perfetto test corpus (168 entries listed, eight sched-bearing or Linux-looking files downloaded and read, search #40–#41) holds Android traces and one non-desktop Linux trace (S3-15); LTTng reference traces are scripted workloads (S3-16) whose README could not be fetched; Trace Compass and tracevizlab repositories describe only how to record one's own trace (#46); the sched_ext issue #234 log (S3-02) is a game session with scx_lavd's own per-task sampling, and issue #296's comments were unobtainable (#8, #9); the LAVD deck (S3-01) gives only the shares of "system tasks" in scheduling during games. Phoronix/openbenchmarking idle-power runs unreachable (#3, #48). Searches #22, #25, #26, #28, #32, #54, #58 established the rest.
- **Unreachable or unquotable sources, for the record:** github.com and api.github.com (403) — issue text obtained only through Wayback `id_` captures where the capture predates GitHub's React issue page; sched-ext/scx #296 comments (React capture only; retrieved 2026-09-22 from the development machine, §5 S3-25); forums.gentoo.org (login wall; Wayback 503/reset); columbia.edu PowerTOP report (403); phoronix.com, openbenchmarking.org (403); lore.kernel.org, lists.freedesktop.org (403); GitLab `notes` API (401) — replaced by `discussions.json`; lttng-ref-traces README (404 on raw); GitHub MCP tools (scoped to the task repository only).

## 5. Retry from the development machine (2026-09-22)

Fetched with the authenticated `gh` CLI and `curl` on the development Mac, outside the routine's proxy. Copies in `sources/retry-2026-09-22/` (local, gitignored).

| # | date | engine | URL | status | copy (SHA-256) |
|---|---|---|---|---|---|
| R1 | 2026-09-22 | `gh api` | `repos/sched-ext/scx/issues/296` | 200 | `scx-296.json` `fc74d4cd71ca34412774d940f6eb526d05461c6e8f76169a99eaa4ee8bf0c2c6` |
| R2 | 2026-09-22 | `gh api --paginate` | `repos/sched-ext/scx/issues/296/comments` | 200 (25 comments) | `scx-296-comments.json` `cde6757f42e80ac178bc9634591a46ec5aafd5be49ac726e495b2183e63470b3` |
| R3 | 2026-09-22 | `curl -L` | `https://github.com/sched-ext/scx/files/15368993/d3_lavd_2ccd.log` | 200 | `d3_lavd_2ccd.log` `08bc68c29101c99eba42a630c16bcb985c6d09dcd8746f0f68f93b43e504b83c` |
| R4 | 2026-09-22 | `curl -L` | `https://github.com/sched-ext/scx/files/15368992/sc2_lavd_2ccd.log` | 200 | `sc2_lavd_2ccd.log` `5a981dad0bab76f834d0916e788323a9bed461985084886e8ad440c4e91be128` |
| R5 | 2026-09-22 | `curl -L` | `https://github.com/sched-ext/scx/files/15369016/d3_lavd_1ccd.log` | 200 | `d3_lavd_1ccd.log` `7fd8b8e4974c1350513d30de8778a7845a74d465a9021871831cf61d3aba4aa6` |
| R6 | 2026-09-22 | `curl -L` | `https://github.com/sched-ext/scx/files/15369017/sc2_lavd_1ccd.log` | 200 | `sc2_lavd_1ccd.log` `ed4cde2e737f5c51bc86ee7d6a15fe548c6636c58967a2f396ac2ecf05699263` |
| R7 | 2026-09-22 | browser (인지오, logged in to gitlab.gnome.org), uploaded to the development machine | `https://gitlab.gnome.org/GNOME/mutter/uploads/eefef80ddd39970eb0d1bc85f26cc55c/capture_1.syscap` (anonymous `curl` → 404) | — | `capture_1.syscap` `56789854dd350715f2809ed74d95c3bdfab9382c5cd21b3d646b4a03604767f1` |
| R8 | 2026-09-22 | same | `https://gitlab.gnome.org/GNOME/mutter/uploads/54beb429c2983db46b7ade400ffd45c1/capture_2.syscap` | — | `capture_2.syscap` `81473fb65ddde301f8aec1f9076339b5cf5c5c500853017987c97badc743dd49` |
| R9 | 2026-09-22 | `curl` | `https://gitlab.gnome.org/GNOME/sysprof/-/raw/49.0/src/libsysprof-capture/sysprof-capture-types.h` | 200 | `sysprof-capture-types.h` `8c75d143116241ff5b394ca1e13362d1de25c03190967463485be671c036b90e` |
| R10 | 2026-09-22 | `curl` | `https://gitlab.gnome.org/GNOME/sysprof/-/raw/49.0/src/libsysprof/sysprof-sampler.c` | 200 | `sysprof-sampler-49.0.c` `f2d93e00b388cc47daceaf6f08ede879a12c4ec3a7c98a8d2fc0c8bb6091062b` |
| R11 | 2026-09-22 | `curl` | `https://bugs.kde.org/attachment.cgi?id=168952` (S3-24's `perf.data`) | 200, 3 936 532 bytes, header `PERFILE2` | `kde-perf.data` `2c3071c6e3e28cca0b70a5b1911aacfdc320d57f60c7979dddaeeaeae90af111`; read with `perf` 6.12.107 in a `debian:trixie` container (S3-27) |
| R12 | 2026-09-22 | `curl` (browser user agent) | `https://www.phoronix.com/review/ubuntu-2404-idle-power` (§1 row #48) | 403, Cloudflare challenge ("Just a moment...") | — ; no Wayback snapshot (`archive.org/wayback/available` empty); a site-restricted WebSearch (`phoronix Ubuntu 24.04 idle power consumption review`, phoronix.com) finds no article at this path — the Ubuntu 24.04 article is `review/ubuntu-2404-benchmarks`, a performance comparison; the row-#48 URL appears to be constructed, not found |
| R13 | 2026-09-22 | `curl` (browser user agent) | `https://www.columbia.edu/~swc2124/assets/HEAD02-INTL-03.html` (§1 row #21) | 403, Cloudflare challenge | — ; no Wayback snapshot; WebSearch (`columbia.edu swc2124 PowerTOP report HEAD02-INTL-03`) confirms a page titled "PowerTOP report" at this URL, its snippet naming a 22.2 wakeup/s system rate and 0.2 % CPU — snippet only, not quotable |
| R14 | 2026-09-22 | browser (인지오; the Cloudflare check passes in a browser), saved as HTML and uploaded to the development machine | `https://www.columbia.edu/~swc2124/assets/HEAD02-INTL-03.html` | — (the file carries `saved from url=(0060)https://www.columbia.edu/~swc2124/assets/HEAD02-INTL-03.html`) | `columbia-powertop-HEAD02-INTL-03.html` `56bcbbdaa1c64d64fda442c3720a3297c5b52462e6cb51c4b611ac5307e84d7b` (S3-29) |

### S3-25 — sched-ext/scx issue #296 and its four scx_lavd logs (Diablo III and StarCraft II under Proton, Plasma 6 Wayland, 2024)

**Citation.** sched-ext/scx issue #296, "scx_lavd: ~20% lower fps in Starcraft 2 and Diablo 3", opened by pingubot, 2024-05-18, https://github.com/sched-ext/scx/issues/296; logs attached to comment 2119184569 (2024-05-19), https://github.com/sched-ext/scx/issues/296#issuecomment-2119184569.

**Passages.**
- Issue body: > "Ryzen 5950x ( with one CCD disabled as the readme mentioned sxc_lavd is not optimized for more than 1 ccd cpus)" / "32Gb Ram"
- Comment 2119184569: > "I was in game in campaign in d3 and sc2 for half a minute or less before leaving the game again." / "Tested with: Linux 6.9-tkg, amd_pstate=active" / "Commit: 17c0c10b4efbfe9819ba818396b1c3438fc7e45c"
- Comment 2133863773: > "I am using Proton Experimental for sc2 and d3." / "DE: Plasma 6 on wayland"
- Comment 2119057998 (the maintainer's request): > "Could you please upload the log of lavd with `./scx_lavd -s $(nproc)` for each game?"
- `d3_lavd_2ccd.log:578`: > `10:22:17 [INFO] |       556 |     1482 | Xwayland          |   13 |   25 |  30075000 |      1176 |    1000000 |      7202 |       19 |      44 |           20 |      -1 |         0 |     13376 |     12691 |     18556 |     24048 |       39 |       40 |       13 |     13 |`
- `d3_lavd_2ccd.log:622`: > `10:22:18 [INFO] |       599 |     1422 | kwin_wayla:cs0    |   24 |   15 |  37500000 |       558 |    6223859 |      3180 |       20 |      44 |           20 |       0 |         0 |     12238 |     16812 |     18297 |     16380 |       39 |       40 |       13 |      2 |`
- `d3_lavd_2ccd.log:513`: > `10:22:15 [INFO] |       493 |     1888 | pipewire-pulse    |   10 |   -1 |         0 |         0 |   15000000 |        21 |        9 |      44 |            9 |       0 |         0 |      1455 |      7019 |      1849 |       873 |       48 |       39 |       15 |      6 |`
- `d3_lavd_1ccd.log:103`: > `10:35:17 [INFO] |        96 |     1399 | plasmashell       |   14 |   -1 |         0 |         0 |   15000000 |       324 |       21 |      45 |           20 |       1 |         0 |      1000 |     41809 |      1000 |      1002 |       44 |       40 |       25 |     26 |`
- `d3_lavd_2ccd.log:20` (fifth second of the log, the scheduler 1 s old): > `10:22:00 [INFO] |        15 |      680 | systemd-udevd     |    8 |   -1 |         0 |         0 |    1000000 |         0 |       20 |       0 |           20 |       0 |         1 |        17 |  11572749 |         0 |         0 |       24 |        0 |        0 |      0 |`

Column header (every log, e.g. `d3_lavd_2ccd.log:5`): `mseq | pid | comm | cpu | vtmc | vddln_ns | elglty_ns | slice_ns | grdy_rt | lat_prio | avg_lc | static_prio | lat_bst | slice_bst | run_freq | run_tm_ns | wait_freq | wake_freq | perf_cri | avg_pc | cpu_util | sys_ld`. The columns' semantics are those fixed against `scx_lavd`'s source in 9.8's S3 §4.4 (`_dev/research/jioh/task-9.8-browser-comms/search/S3-traces-datasets.md`): EWMAs; `run_tm_ns` CPU per runnable-to-sleep episode, biased upward by preemption; `run_freq` the reciprocal of one run-plus-wait cycle; `wake_freq` the rate at which the thread wakes *others*; rows are the first N schedule-ins after each refill, not a census. That reading was taken at a different `scx_lavd` commit than 17c0c10; the column set here lacks 9.8's `lat_cri`, `min_lc`, `max_lc` and adds `perf_cri`, `avg_pc`.

**[own computation]** `python3` over the four logs (ANSI codes stripped): 1 600 rows over 10:22:00–10:22:49 (`d3_lavd_2ccd`), 3 200 over 10:23:14–10:24:53 (`sc2_lavd_2ccd`), 1 312 over 10:35:12–10:36:33 (`d3_lavd_1ccd`), 1 840 over 10:36:45–10:38:39 (`sc2_lavd_1ccd`). Medians per comm of `run_tm_ns` across its rows, the four logs in that order: `Xwayland` (one pid) 15 937 / 19 149 / 16 378 / 18 057 ns (n = 24 / 20 / 25 / 15); `kwin_wayla:cs0` (one thread of `kwin_wayland`) 17 402 / 21 067 / 19 614 / 18 741 ns (n = 10 / 14 / 20 / 16); `pipewire-pulse` 9 074 / 10 533 / 8 509 / 9 136 ns (n = 15 / 61 / 14 / 47), `static_prio` 9 in every row; `plasmashell` one row each in the 1-CCD logs, 41 809 and 48 973 ns; `systemd-udevd` 11.6 / 13.3 / 11.3 / 13.2 ms (n = 3 / 4 / 1 / 2), every row within the first seconds of a log with `run_freq` 9–19 and `wait_freq` 0 — values still near the EWMA's seed rather than observed episodes; `systemd-coredum` present in both Diablo III logs (a core dump being written during the run). No `pipewire` (the graph process), `wireplumber`, `dbus-daemon`/`dbus-broker`, `systemd` (pid 1), `systemd-logind`, `polkitd` or `udisksd` row in any log. `nextcloud` (a user's sync client) samples at `run_freq` 167 in all four.

**Coverage.** T2: covers partly — CPU per wake of a Wayland compositor's thread (`kwin_wayla:cs0`), Xwayland and PulseAudio-on-PipeWire during play on a GPU desktop, under `scx_lavd` rather than the stock scheduler, one machine, under a minute to two minutes per log; the busy state (a game presenting frames), not idle; `kwin_wayla:cs0` is one thread, not the compositor whole, and no per-frame figure. T1: does not cover — no system service besides `systemd-udevd` (seed-valued rows) and `systemd-coredump` (an event) appears. T5: covers partly — a public scheduler-side sampled log of a Linux desktop naming the display server, a compositor thread and the audio server; not a trace, not idle. The routine's T5 "not found" for issue #296 (§1 rows #8–#9) is superseded: the comments hold no per-task table; the per-task rows are these four attached logs.


### S3-26 — the two sysprof captures attached to GNOME mutter issue #4622 (GNOME 49 Wayland desktop, Ryzen 5 3600, 2026-02-21)

**Citation.** flexlab, note 2686169 on GNOME/mutter issue #4622 (2026-02-21), https://gitlab.gnome.org/GNOME/mutter/-/issues/4622 — the issue of S3-06; attachments `capture_1.syscap`, `capture_2.syscap`. Format read against sysprof 49.0 (`sysprof-capture-types.h`, R9); sampler settings from `sysprof-sampler.c` at 49.0 (R10).

**Passages.**
- Note 2686169: > "Four consecutive clean sysprof captures (each 20s) were taken over \~20 minutes with no significant system activity in the degraded state:" … "The gnome-shell wakeup rate via /proc/\<pid\>/schedstat remains at baseline levels (\~3,200/5s) throughout." … "Capture 1 & Capture 2 are attached."
- Note 2686540 (daenzer, Mutter developer): > "1800 calls per second would be consistent with 1 output updating at 150 Hz, 2 outputs updating at 75 Hz each, ..." / "Offhand that doesn't look abnormal." / "The sysprof captures don't seem to have complete call traces (no symbols or frame pointer for at least some binaries?)"
- `sysprof-sampler.c:378-409` (49.0): `attr.sample_type = PERF_SAMPLE_IP | PERF_SAMPLE_TID | PERF_SAMPLE_IDENTIFIER | PERF_SAMPLE_CALLCHAIN | PERF_SAMPLE_TIME;` … `attr.exclude_idle = 1;` … `attr.type = PERF_TYPE_HARDWARE; attr.config = PERF_COUNT_HW_CPU_CYCLES; attr.sample_period = 1200000;` (the software fallback, `PERF_COUNT_SW_CPU_CLOCK` at `sample_period = 1000000`, is taken only when the hardware event fails, `:459-462`).
- Capture metadata frames (both): `org.gnome.sysprof.version = 49.0`, `n-cpu = 12`, `uname.release = 6.18.5+deb14-amd64`, `uname.version = #1 SMP PREEMPT_DYNAMIC Debian 6.18.5-1 (2026-01-16)`, `WAYLAND_DISPLAY = wayland-0`, `DESKTOP_SESSION = gnome`, `sysinfo.procs = 1783` / `1818`; `capture-time = 2026-02-21T04:00:46.247573+01` / `2026-02-21T04:11:05.590037+01`; the embedded `/proc/cpuinfo.gz`: `model name : AMD Ryzen 5 3600 6-Core Processor`.

**[own computation]** A frame parser written to the 49.0 header (`sources/retry-2026-09-22/syscap.py`; 256-byte file header, 24-byte frame header, sample = `n_addrs`, `tid`, addresses) reads every byte of both files (0 unparsed). Capture 1: 152 237 frames, 31 991 samples over 20.82 s; capture 2: 55 274 samples over 20.68 s. Samples per process (share of all samples; one sample = 1.2 × 10⁶ cycles, so a share of cycles, not of time — the clock frequency per CPU is not converted): `gnome-shell` 47.4 % / 74.0 % (≈ 874 / 2 374 Mcycles/s, i.e. ≈ 0.24 / 0.66 of one core at 3.6 GHz), one thread holding 11 705 / 36 551 of its samples; pid 0 (kernel work outside any task) 17.9 % / 13.3 %; `firefox` (11 / 14 processes) 17.2 % / 6.5 %; `xdg-desktop-portal-gnome` 2.7 % / 1.9 %; `qemu-system-x86_64` (a running VM) 2.1 % / 1.3 %; the profiler itself (`sysprof`, `sysprofd`) 2.1 % / 1.1 %+; `nxserver.bin` (NoMachine remote-desktop server) with its `nxchmod.sh`/`pgrep`/`awk` children ≈ 3 % / 0.1 %; `cupsd` 1.0 % / 0.7 %; `polkitd` 2.7 % / 0 samples; system `dbus-daemon` 1.5 % / 5 samples; `systemd` (pid 1 and user) 45 / 0 samples; `systemd-oomd` 10 / 13 samples. No sample in either capture for `pipewire`, `wireplumber`, `pipewire-pulse`, `systemd-journald`, `systemd-udevd`, `systemd-logind`, `NetworkManager` — each below one sample (1.2 × 10⁶ cycles) in 20 s.

**Coverage.** T2: covers partly — the compositor's CPU as a share of cycles on a GNOME 49 Wayland desktop at an idle-ish state (the reporter's "no significant system activity"), but in the state the reporter calls degraded after a gaming session, which the Mutter developer reads as not abnormal; no per-frame figure, no wakes (a cycle sampler records no scheduler events). T1: covers weakly — per-service cycle shares with machine and window named, on a desktop running a browser, a VM, a remote-desktop server and the profiler; zero samples for the audio server, journal, udev, logind and NetworkManager bound their CPU at idle from above for this machine and 20 s. T3: covers partly — a whole-system cycle split between session processes, system services and kernel on one desktop. T5: covers partly — a public system-wide profile of a Linux desktop naming the compositor and the services; not a scheduler trace. Not idle in the sense of an empty desktop: the co-running applications are listed above.

### S3-27 — the `perf.data` attached to KDE bug 486214 (kwin_wayland, Plasma 6.0.4, Framework laptop, 2024)

**Citation.** billy.nlv0a, attachment 168952 (`perf.data`) on KDE bug 486214, https://bugs.kde.org/attachment.cgi?id=168952 — the bug of S3-24, whose comment 2314766 states the state: "I left the system to idle for about 10 mins, then took this."

**Passages.** `perf report --header-only`: > `# hostname : violet-fw13` / `# os release : 6.8.7-300.fc40.x86_64` / `# cpudesc : 12th Gen Intel(R) Core(TM) i5-1240P` / `# cmdline : /usr/bin/perf record -o /home/bill/perf.data --call-graph dwarf,8192 --aio -z --sample-cpu --pid 2408` / `# event : name = cpu_core/cycles/Pu, …, { sample_period, sample_freq } = 4000, …, exclude_kernel = 1, …, freq = 1` (and the same for `cpu_atom/cycles/Pu`) / `# missing features: TRACING_DATA …`. `perf report --stats`: > `SAMPLE events: 12425`.

**[own computation]** `perf script -F comm,tid,cpu,time,event,period`: first sample 6198.045 s, last 6214.564 s (16.5 s); samples per thread — `kwin_wayland` (main, tid 2408) 10 792, `eDP-1` (tid 2477, the output's thread) 1 262, `Thread (pooled)` 212, `QDBusConnection` 106, `libinput-connec` 29, `QQmlThread` 24; summed period 1.41 × 10⁹ user-space cycles, ≈ 85 Mcycles/s for the process over the window.

**Coverage.** T2: covers weakly — user-space cycles of one compositor process, per thread, after 10 min idle on a laptop, in a state the reporter files as a bug ("usage cpu constantly") and the KWin developer reads as compositing and Wayland-event work; kernel time excluded (`exclude_kernel = 1`), no scheduler events recorded (one process, cycles only), so no wakes and no per-frame figure. T1, T3, T5: does not cover.

### S3-28 — Gentoo Forums topic 1152974, "Laptop burning hot, high wakeups, 50W power usage at idle." (KDE on X11, Dell Precision 7560, 2022)

**Correction to §1 rows #20 and #33.** The thread is topic **1152974**, not 1153076: the search result's link was the forum's "view previous topic" link from topic 1153076 (`viewtopic-t-1153076-view-previous.html`), and topic 1153076 itself is "Problems with touchpad (solved)" (Wayback `20251207161749id_`, `<title>`). The login wall stands for both on the live forum (2026-09-22, `<title>Gentoo Forums - Login`); the Wayback Machine holds the thread whole.

**Copy read.** `https://web.archive.org/web/20251203193848id_/https://forums.gentoo.org/viewtopic-t-1152974-start-0.html` (200, 43 388 bytes; the 2023-04-30 and 2023-05-05 captures carry the same posts), local `sources/retry-2026-09-22/gw20251203193848.html` SHA-256 `5166c1b7ea49f004701d065763424ae6aa5e018e29301ca7b94c9a8069bba20c`. Found by WebSearch `"Laptop burning hot" high wakeups 50W power usage at idle gentoo forums` (2026-09-22).

**Passages.**
- gustafson, 2022-07-18: > "The machine is a Dell Precision 7560. Battery life is roughly an hour (and its new). At idle, powertop reports ~3000 wakeups per second and 26% CPU usage. CPUs are averaging ~3.0 GHz but should be mostly idle at 800 MHz. Powertop is reporting 40-50W usage at idle..."
- gustafson, 2022-07-19: > "That was after boot up, starting x11 and kde, but nothing open." / "With firefox (only gentoo forums page) and thunderbird open, 55 Watts with 82% CPU... though it varies a lot."
- The quoted PowerTOP table (same post): > "Summary: 4729.4 wakeups/second, 0.0 GPU ops/seconds, 0.0 VFS ops/sec and 52.1% CPU use" / "90.9 ms/s 1569.4 Process [PID 14306] /usr/bin/kwin_x11" / "247.5 ms/s 821.4 Process [PID 18562] /usr/lib64/thunderbird/thunderbird" / "8.1 ms/s 711.2 Timer tick_sched_timer" / "48.2 ms/s 7.7 Process [PID 13707] /usr/bin/X -nolisten tcp -auth /var/run/sddm/{…} -background none -noreset" / "3.5 ms/s 19.3 Process [PID 14464] /usr/bin/plasmashell" / "3.9 ms/s 11.6 Process [PID 14723] thermald --dbus-enable --adaptive" / "1.3 ms/s 7.7 Process [PID 14608] /usr/bin/ksystemstats"
- xgivolari, 2022-07-19: > "KWin generating 1569 Events/s does not seem right at all."

**[own computation]** CPU per event from the table's two columns: `kwin_x11` 90.9 / 1 569.4 ≈ 58 µs; `X` 48.2 / 7.7 ≈ 6.3 ms; `plasmashell` 3.5 / 19.3 ≈ 0.18 ms. PowerTOP's "Events/s" counts wakeups attributed to the process, not scheduler wakes per thread.

**Coverage.** T2: covers weakly — per-process CPU (ms/s) and events/s for a compositor (`kwin_x11`), the X server and the shell on one KDE X11 laptop, with Firefox and Thunderbird open, in a state the poster and a replier call abnormal (a power-management misconfiguration is the thread's suspected cause; no resolution is posted). T1: does not cover — no system service appears among the listed rows. T3: covers weakly — a whole-machine wakeup rate and CPU share with the top rows named. T5: does not cover.

### S3-29 — a PowerTOP report of an idle Debian 8 machine at its login greeter (Pentium G3258, kernel 3.16), hosted at columbia.edu

**Citation.** "PowerTOP report", `HEAD02-INTL-03.html`, https://www.columbia.edu/~swc2124/assets/HEAD02-INTL-03.html (the personal pages of Columbia user swc2124); PowerTOP's own HTML report (`powertop --html`). No author statement, date, measurement window or purpose accompanies it; PowerTOP 2.6.1's default measurement is not stated in the file.

**Passages** (from the saved page; table cells joined with `|`).
- System Information: > `PowerTOP Version | v2.6.1` / `Kernel Version | Linux version 3.16.0-4-amd64` / `System Name | MSIH81I (MS-7851)2.0` / `CPU Information | Intel(R) Pentium(R) CPU G3258 @ 3.20GHz` / `OS Information | Debian GNU/Linux 8 (jessie)`
- Summary: > `Target: 1 units/s System: 22.2 wakeup/s CPU: 0.2% usage GPU: 0 ops/s GFX: 0 wakeups/s VFS: 0 ops/s`
- Overview of Software Power Consumers (Usage | Wakeups/s | Category | Description): > `1.2 ms/s | 8.2 | Process | /usr/lib/packagekit/packagekitd` / `54.2 us/s | 5.4 | Process | [rcu_sched]` / `423.5 us/s | 1.0 | Process | /usr/bin/boinc --check_all_logins --redirectio --dir /var/lib/boinc-client` / `185.2 us/s | 1.0 | Process | /usr/sbin/NetworkManager --no-daemon` / `66.2 us/s | 1.0 | Process | /usr/sbin/lightdm-gtk-greeter` / `697.5 us/s | | Process | /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation` / `3.5 us/s | 0.05 | Process | /lib/systemd/systemd-journald` / `3.5 us/s | 0.05 | Process | /lib/systemd/systemd-logind` / `1.6 us/s | 0.05 | Process | /sbin/rpcbind -w` / `10.5 us/s | | Process | /sbin/init`
- Processor Idle State Report: > `C6-HSW | 99.7% | 74.2 ms` (CPU 0) / `C6-HSW | 99.4% | 113.6 ms` (CPU 1)
- Process Device Activity lists `Xorg | /dev/dri/card0`.

**[own computation]** CPU per wakeup where both columns are given: `packagekitd` 1.2 ms / 8.2 ≈ 146 µs; `NetworkManager` ≈ 185 µs; `lightdm-gtk-greeter` ≈ 66 µs; `boinc` ≈ 424 µs; `systemd-journald` and `systemd-logind` 3.5 µs / 0.05 ≈ 70 µs each (one wakeup per 20 s). The system `dbus-daemon` and `/sbin/init` carry CPU with no wakeup rate printed.

**Coverage.** T1: covers — the only per-service table found with a wakeup rate and CPU per service at idle, machine named (a two-core Haswell desktop board), systemd-era (Debian 8, systemd as init), no user session (a display-manager greeter on Xorg); a 2014–2015-era distribution on kernel 3.16, window and date unstated, one reading, `packagekitd` and a BOINC client present. T3: covers partly — a whole-machine rate (22.2 wakeups/s, 0.2 % CPU) of a machine with no user session. T2, T5: does not cover.
