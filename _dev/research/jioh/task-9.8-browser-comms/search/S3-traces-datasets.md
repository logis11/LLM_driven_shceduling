# S3 — public traces, datasets, logs, bug reports with profiles, benchmark databases

Reader: S3. Topics: T1, T2, T3, T5. All accesses 2026-09-19 unless stated. Every fetch went through the session's HTTPS proxy (CA bundle `/root/.ccr/ca-bundle.crt`), TLS verification on. Source copies are under `sources/S3-NN/` (gitignored); the SHA-256 given per file is of the copy read. "MCP body" below means the issue body as returned by the GitHub MCP `search_issues` tool (github.com HTML and api.github.com return 403 through the proxy; the MCP `issue_read` tool is restricted to the project repository, so issue *comments* were reachable only through Internet Archive captures).

Reader's own computations are labelled **[own computation]** with the command; they locate a candidate, they are not values.

## 1. Search log

| # | Date | Engine / venue | Query or request | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|---|
| 1 | 2026-09-19 | curl probe, 37 venues | HEAD/GET of candidate venues (see cells) | issues.chromium.org 200; bugs.chromium.org 200; raw.githubusercontent.com 200; community.zoom.com 200; discourse.ubuntu.com `search.json` 200; bugzilla.mozilla.org `/rest` 200; bugs.launchpad.net 200; api.launchpad.net 200; perfetto.dev 200; chromium.googlesource.com 200; gitlab.com API 200; forum.manjaro.org / forum.endeavouros.com `search.json` 200; bbs.archlinux.org 200; bugs.kde.org `/rest/bug` 200; ui.perfetto.dev 200; gitlab.gnome.org API 200; www.google.com 200; www.bing.com 200; html.duckduckgo.com 202 | github.com issue pages 403; api.github.com/search/issues 403; openbenchmarking.org 403; www.phoronix.com 403; phoronix.com/search 403; storage.googleapis.com/perfetto-ui-data/ (listing) 403; www.reddit.com 403; support.discord.com 403; lore.kernel.org 403; old.reddit.com 302 (not followed); feedback.discord.com 301 (not followed); discuss.zoom.us 000 (no connection); duckduckgo.com 000; web.archive.org `2024id_` capture of scx#300 404 |
| 2 | 2026-09-19 | GitHub MCP `search_issues` (sched-ext/scx) | `steamwebhelper lavd sample` | none relevant (#1580 task_ctx lookup, #269 fails to load) | — |
| 3 | 2026-09-19 | `git clone --depth 1 https://github.com/sched-ext/scx.git` | clone at commit `0b6f009f08df51ba8398a1ebe9fba0710191c85f` (2026-09-18); `grep -rIl "steamwebhelper\|gameoverlayui\|CQueuedPacketSe"` | 0 files match in the repository | — |
| 4 | 2026-09-19 | GitHub MCP `search_issues` (sched-ext/scx) | `steamwebhelper`; `gameoverlayui CQueuedPacketSe` | 0 and 0 results | — |
| 5 | 2026-09-19 | GitHub MCP `search_issues` (ValveSoftware/steam-for-linux, sort comments) | `steamwebhelper high CPU usage idle` | 498 total; followed #8258 (S3-25), #7241 (S3-23) | — |
| 6 | 2026-09-19 | GitHub MCP `search_issues` (element-hq/element-desktop) | `high CPU usage when idle Linux` | #1248 (Windows 10 report — context only, not a candidate), #1588 (server-side CPU, macOS) | — |
| 7 | 2026-09-19 | GitHub MCP `search_issues` (electron/electron) | `high CPU usage idle Linux background window`; `idle CPU usage on Linux when window is hidden or minimized, wakeups, powertop`; `high CPU usage on Linux when idle`; `CPU usage idle Linux` | 0 results for all four (the semantic index returned nothing for this repository) | — |
| 8 | 2026-09-19 | WebSearch | `scx_lavd steamwebhelper gameoverlayui CQueuedPacketSe` | only steamcommunity.com Windows help threads; nothing on scx | — |
| 9 | 2026-09-19 | WebSearch | `site:issues.chromium.org linux background tab renderer idle CPU usage perf profile wakeups` | 41476969 (S3-05), 41234063 (browser process 100–105 %, not fetched), 41217438, 41193006, 40272975 (GPU; not fetched) | — |
| 10 | 2026-09-19 | WebSearch | `discord linux idle high cpu usage powertop wakeups issue` | bbs.archlinux.org 255768 (S3-13) | support.discord.com post — host 403 |
| 11 | 2026-09-19 | WebSearch | `zoom linux client idle cpu usage "top" "zoom" percent bug community` | community.zoom.com 23201 (S3-10), 39563 (S3-11); forums.linuxmint.com t=317477 and community.zoom.com m-p/18001 not followed | — |
| 12 | 2026-09-19 | WebSearch | `dataset per-process CPU usage linux desktop trace perfetto chrome renderer processes public trace` | Perfetto docs pages only (documentation, no dataset) | — |
| 13 | 2026-09-19 | GitHub MCP `search_issues` (all repositories) | `scx_lavd steamwebhelper sample` | 0 results | — |
| 14 | 2026-09-19 | GitHub MCP `issue_read` | element-hq/element-desktop#1248, ValveSoftware/steam-for-linux#8258 | — | "Access denied: repository … is not configured for this session" (only logis11/llm_driven_shceduling allowed) |
| 15 | 2026-09-19 | Google / Bing HTML search | `site:issues.chromium.org idle renderer CPU linux perf` | Google 200 but the 92 KB page holds no result links (script page); Bing 200 but results were python-IDLE pages | dead end |
| 16 | 2026-09-19 | issues.chromium.org endpoints | `GET /action/issues/<id>` → 200 JSON (title, dates, description embedded); `POST /action/issues/list` with `[null,null,null,null,null,["157"],["<query>",null,50,"start_index:0"]]` → 200, query honoured; `GET /issues/<id>` HTML → 200 but only a sign-in shell (WebFetch: "sign-in link" only) | — | `/action/issues/<id>/events` 404, `/comments` 404 (GET) / 405 (POST), `/history` 404, `/attachments` 401 |
| 17 | 2026-09-19 | issues.chromium.org `/action/issues/list` | `steamwebhelper` | 485551544, 40268818, 41459128 (titles unrelated to CPU; not followed) | — |
| 18 | 2026-09-19 | issues.chromium.org `/action/issues/list` | `background tab idle CPU wakeups linux renderer` | 41335631 (OS Version 9592.42.0 = Chrome OS build; description only says "See attached trace … MessagePumpLibevent::OnLibeventNotification"; not a Linux-desktop candidate), 41097521 (timer coalescing, mechanism) | — |
| 19 | 2026-09-19 | issues.chromium.org `/action/issues/list` | `renderer idle CPU linux` | 553778325 "[Desktop Power Perf Sheriff]" (bot), 40919354 pre-paint tiles — not followed | — |
| 20 | 2026-09-19 | issues.chromium.org `/action/issues/list` | `background tab CPU linux idle` | 536046184 (S3-06), 41318993 (S3-04), 41335631, 40126658 (priority; T4 territory), 40128284 (throttle timers to 1/min; mechanism) | — |
| 21 | 2026-09-19 | issues.chromium.org `/action/issues/list` | `idle wakeups linux` | 525786173 (S3-07), 40657105 (S3-02), 41217089 (S3-01), 41248153 (S3-03), 41254298 (Windows procexp: "approximately 110 context switches per second" — context, not Linux), 41164651 (Mac 50 ms timer — not fetched), 40195339 (WebRTC wakeups tracking bug, no observation) | — |
| 22 | 2026-09-19 | issues.chromium.org `/action/issues/list` | `powertop wakeups`; `perf record idle CPU linux`; `wake ups background tab throttling linux`; `electron idle CPU linux` | output beyond the first 150 lines was not inspected (cut); no new ids followed | — |
| 23 | 2026-09-19 | issues.chromium.org `/action/issues/<id>` | 41217089, 40657105, 41248153, 41318993, 41476969, 536046184, 525786173, 41104634 | descriptions saved (S3-01…S3-07, S3-09) | comment threads and attachments (traces, powertop output, screenshots) not retrievable (see row 16) |
| 24 | 2026-09-19 | bugs.chromium.org old ids | `detail?id=368774`, `detail?id=470615` | 200: a 572-byte redirect script naming `https://issues.chromium.org/41104634` (S3-09, Mac) and `…/41164651` (Mac; not fetched) | — |
| 25 | 2026-09-19 | community.zoom.com | thread 23201 (`/meetings-2/zoom-on-linux-is-using-2-7-cpu-when-idle-23201`), thread 39563 | 200 each; posts embedded as HTML-escaped JSON (`content`/`repliedAt`) | old `/t5/…/m-p/48802` URL 404 after redirect |
| 26 | 2026-09-19 | bbs.archlinux.org | `viewtopic.php?id=255768`; `viewtopic.php?id=245442`; `search.php?action=search&keywords=steamwebhelper+cpu` | 255768 (S3-13), 245442 (S3-28) | search returns an "Info" page (no results without login) |
| 27 | 2026-09-19 | archive.org availability API | 4 GitHub issue URLs | — | 429 Too Many Requests ×4 |
| 28 | 2026-09-19 | web.archive.org `/web/<ts>id_/` captures | github.com sched-ext/scx#234, #296, #376, #2491; steam-for-linux#7241, #8258; element-web#29682, #32167; teams-for-linux#652 | #234 200 (memento 2025-02-21 08:39:09; React payload with 16 of 63 comment bodies); #296 200 (2025-07-30; shell with 0 bodies); #7241 200 (2025-12-22; 0 bodies); #8258 200 (2026-04-19 04:25:56; 14 bodies — S3-25); #29682 200 (2025-05-28; 0 bodies) | #376 404, #2491 404, #32167 404, #652 404; repeated `Recv failure: Connection reset by peer` / `SSL_ERROR_SYSCALL` on web.archive.org (proxy `ws_closed_mid_exchange`) |
| 29 | 2026-09-19 | archive.ph | scx#234 | — | connection reset (000) |
| 30 | 2026-09-19 | GitHub MCP `search_issues` (steam-for-linux) | `Steam idles in a power inefficient manner`; `significantly CPU intensive even idle and hidden`; `aggressive in using CPU time and RAM even when IDLE 2022`; `steamwebhelper CPU usage while game running Linux idle client`; `Client uses 100% CPU every seven seconds…`; `steamwebhelper stuck ~400% cpu 5 threads…`; `steamwebhelper uses 100% cpu core only when steam window is … on top` | #12616 (S3-22), #7241 (S3-23), #13309 (S3-24), #9266 (S3-26), #10619 (S3-27), #6603 (S3-35), #12973 (S3-29), #8553 (no numbers; not a candidate), #7424 (screenshot only), #7673 (Fedora 33, no numbers), #13437 (GPU-side), #13513 (overlay FPS, GPU) | #10656 and #12502 bodies were not returned by the semantic search (titles only from WebSearch row 46) |
| 31 | 2026-09-19 | GitHub MCP `search_issues` (element-hq/element-web) | `high CPU usage idle Linux`; `Constant CPU wakeups … background tab`; `CPU cycles over time … background desktop linux`; `Abnormal use of CPU when idle` | #29682 (S3-15), #32107 (S3-16), #32167 (S3-17); #32072 (macOS), #32145 (macOS), #32115 (macOS), #32113 (Windows) — context only | #21793 body not returned |
| 32 | 2026-09-19 | GitHub MCP `search_issues` (IsmaelMartinez/teams-for-linux) | `high CPU usage idle Linux top output`; `High CPU usage` | #328 (S3-18), #293 (S3-19), #652 (S3-20) | — |
| 33 | 2026-09-19 | GitHub MCP `search_issues` (wireapp/wire-desktop) | `Wire uses excessive amount of CPU while idle` | #8975 (S3-21, Ubuntu 24.04 process tree); #9693, #7771 (macOS) | #3338 (from WebSearch) not returned |
| 34 | 2026-09-19 | GitHub MCP `search_issues` (flathub repos) | `high CPU usage idle` in com.discordapp.Discord, com.slack.Slack, us.zoom.Zoom | Discord #260 (S3-14); Slack 0 results; Zoom #394 (0 comments, title only, not followed) | — |
| 35 | 2026-09-19 | GitHub MCP `search_issues` (brave/brave-browser; ungoogled-software/ungoogled-chromium) | `high CPU usage idle background tabs Linux renderer process`; `idle CPU usage Linux wakeups powertop background` | Brave 85 results, titles show service/GPU bugs (#8846 "Bat Ledger Service", #12947 "Excessive Ubuntu CPU usage") — not followed; ungoogled #2577 not followed | — |
| 36 | 2026-09-19 | GitHub MCP `search_issues` (all repositories) | `Slack desktop Linux idle CPU usage wakeups powertop`; `Discord Linux client idle CPU usage percent electron background` | 0 and 0 | — |
| 37 | 2026-09-19 | GitHub MCP `search_code` | `"CQueuedPacketSe"` | 144 code hits, all Source-engine source trees (`net_ws_queued_packet_sender.cpp`) — the thread name's origin, no log or trace | — |
| 38 | 2026-09-19 | GitHub MCP `search_issues` (sched-ext/scx) | `lavd monitor output table lat_cri comm game stutter`; `steam game chrome renderer monitor sched samples comm lat_cri`; `scx_lavd getting large pauses and stutters in-game`; `Lavd stalls again` | #234 (S3-30), #3739 (S3-31), #296 (25 comments, Wayback shell empty), #376, #2491, #3750, #3791, #3130, #3119, #2919, #3541 (GStreamer, not a game) | — |
| 39 | 2026-09-19 | WebSearch | `github issue "scx_lavd" "steamwebhelper" sched_ext game`; `"steamwebhelper" scx_lavd OR "scx_" monitor output "gameoverlayui" sched_ext issue` | scx #2491, #3750, #269, #234, #3791, #3413, #3198, #3259, #3739 — none of the returned pages mention steamwebhelper | — |
| 40 | 2026-09-19 | gist.githubusercontent.com | `ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1/raw` (linked from scx#234) | 200, 118 045 bytes (S3-30) | — |
| 41 | 2026-09-19 | api.launchpad.net | `ubuntu/+source/chromium-browser?ws.op=searchTasks&search_text=idle cpu usage` → 0; `…=cpu` → 9; `…=background tab` → 1; `ubuntu/+source/steam …=cpu` → 2; `/1.0/bugs?ws.op=searchTasks&search_text=idle cpu wakeups chromium` → 1 | bug 2090906 (S3-36); 1914918 (snap refresh, not CPU) | steam results unrelated (freezes) |
| 42 | 2026-09-19 | bugs.debian.org | `pkgreport.cgi?pkg=chromium;include=subject:cpu` | 200, no `bugreport.cgi?bug=` links in the page | dead end |
| 43 | 2026-09-19 | api.stackexchange.com (askubuntu) | `chromium idle cpu renderer` | 1 result (hardware acceleration on Intel NUC), unrelated | — |
| 44 | 2026-09-19 | zenodo.org/api/records | `"perf sched" OR "scheduler trace" linux desktop browser` | 16 372 hits; top 10 unrelated (Lichtblick-suite, OpenVPN connector, …) | — |
| 45 | 2026-09-19 | Discourse `search.json` | forum.manjaro.org `steamwebhelper cpu`; forum.endeavouros.com `steamwebhelper cpu`; discourse.ubuntu.com `chromium idle cpu renderer`; community.frame.work `powertop chrome tabs`, `zoom idle cpu`, `slack cpu idle`, `steam idle power`; discussion.fedoraproject.org and discuss.kde.org `chromium idle cpu wakeups` | community.frame.work topic 25401 (S3-12, from row 47); all other topic lists unrelated (freezes, controllers, firmware) | — |
| 46 | 2026-09-19 | WebSearch | `"steamwebhelper" "%CPU" linux htop in-game overlay cpu usage "gameoverlayui" forum` | bbs.archlinux.org 245442 (S3-28); steam-for-linux #10656 ("~400% cpu in 5 threads" after a CS2 profile view — body not retrievable), #12502 ("100% cpu core when steam window is on top" — body not retrievable) | — |
| 47 | 2026-09-19 | WebSearch | `discord linux client idle "top" CPU % "Discord" process electron battery wakeups github issue linux desktop` | community.frame.work 25401 (S3-12); simoniz0r/Discord-Linux-Client-Issues README (raw fetched: no CPU or wake-up content); wireapp/wire-desktop#3338 (not returned by MCP) | — |
| 48 | 2026-09-19 | WebSearch | `slack linux desktop idle cpu usage powertop wakeups electron` | HN item 16436815 (fetched via hn.algolia.com API: "Slack uses ~ 2 GB of Ram and ~ 10% CPU when idle" — no platform stated, 2018-02-22; context only, not a candidate); josephg blog (opinion) | no Linux Slack observation found |
| 49 | 2026-09-19 | WebSearch | `"teams-for-linux" idle CPU usage percent linux electron issue top` | #328, #293 (S3-18, S3-19); learn.microsoft.com Q&A threads (not fetched) | — |
| 50 | 2026-09-19 | WebSearch | `chromium linux idle tabs "wakeups" powertop "chrome" renderer "wakeups/s" battery report` | mail-archive.com chromium-dev msg06007 (S3-08) | — |
| 51 | 2026-09-19 | WebSearch | `chromium bug "background tab" linux "wakeups" OR "wake-ups" per second measured renderer idle "intensive wake up throttling"` | blink-dev intents (mechanism — S2 territory), bugzilla.mozilla.org 407325 (Firefox, off-topic), bugs.chromium.org 368774 → S3-09 (Mac) | — |
| 52 | 2026-09-19 | WebSearch | `"perf sched" OR perfetto trace chromium linux idle tabs wakeups per second renderer measured`; `element desktop linux idle CPU wakeups powertop "element-desktop" percent`; `dataset "sched_switch" OR "perf sched" trace Linux desktop browser Chrome renderer zenodo OR figshare OR kaggle OR github "trace" download` | google/IdleWakeups (ETW, Windows tool); tools only (perf-trace-viewer, sched-analyzer); no dataset | — |
| 53 | 2026-09-19 | chromium.googlesource.com (catapult) | `+/HEAD/tracing/test_data/` listing; `README.md`, `sfgate.json`, `tcmalloc_multi_renderer.json` via `?format=TEXT` (base64) | HEAD commit `e39ded11ffe971d360160c9d185a7e0ef98fb9a3` (2026-09-18); files saved (S3-32, S3-33) | `+log/…?format=JSON` 403 "Please sign in to view the history pages" |
| 54 | 2026-09-19 | android.googlesource.com (perfetto) | `+/HEAD/test/data/` and `test/data/chrome/` listings; `tools/test_data`; `*.sha256` placeholders | GCS file URLs `https://storage.googleapis.com/perfetto/test_data/<name>-<sha256>` → 200; six Chrome traces downloaded and queried with the `perfetto` Python trace processor (S3-34) | GCS bucket *listing* URLs 403 |
| 55 | 2026-09-19 | mail-archive.com | `chromium-dev@googlegroups.com/msg06007.html` | 200 (S3-08) | — |
| 56 | 2026-09-19 | hn.algolia.com API | `items/16436815` | 200 (context only, row 48) | — |
| 57 | 2026-09-19 | raw.githubusercontent.com | `simoniz0r/Discord-Linux-Client-Issues/master/README.md` | 200; `grep -i "cpu\|wakeup\|idle"` → no lines | — |

## 2. Candidates

### S3-01 — Chromium issue 41217089 ">60 wakeups/sec whilst idle"

- **Citation.** Chromium issue tracker, issue 41217089, ">60 wakeups/sec whilst idle", opened 2015-11-10 (earliest timestamp in the issue JSON, reader's extraction), last event 2017-04-17. Legacy Monorail id not recovered.
- **Copy read.** `https://issues.chromium.org/action/issues/41217089` (JSON, description embedded), 2026-09-19; `sources/S3-01/issue-41217089.json`, 99 353 bytes, SHA-256 `8c0e031dcaca47dbf119272b9a3409cbdc9a839958a892598995e43dc8a9cecd`. Comments and attachments not retrievable (log rows 16, 23).
- **Passages (description, comment #1).**
  > `UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36`
  >
  > `Steps to reproduce the problem:` / `1. Open Chrome to chrome://about.` / `2. Run PowerTOP in a terminal, observe each Chrome core and renderer processes waking up in excess of 60fps.` / `3. Look at your battery and be sad.`
  >
  > `What is the expected behavior?` / `No wakeups when completely idle (rendering quiesced, no scripts, etc).`
  >
  > `Chrome version: 46.0.2490.80  Channel: stable` / `OS Version: Fedora 23`
  >
  > `More than happy to help debug stuff, including the winsys / GPU driver if it looks like being that. This is on Intel/Mesa, running under XWayland, on GNOME/Wayland, stock Fedora 23.`
- **Coverage.** T1: covers — object: wake-ups of "each Chrome core and renderer processes" (Chrome 46 stable, Fedora 23, one `chrome://about` tab, idle), unit wake-ups per second as PowerTOP reports them, statistic a lower bound (">60", "in excess of 60fps"), scope one machine, population one reporter. T2, T3, T5: does not cover.
- **One observation?** Yes, one reporter's PowerTOP session. Machine: partly (Intel/Mesa graphics, XWayland on GNOME/Wayland; CPU model not named). Subject: Chrome 46.0.2490.80 stable, state idle on `chrome://about`. Window: not stated. The PowerTOP table itself is not in the description.

### S3-02 — Chromium issue 40657105 "Very high CPU usage on an idle web page/a large number of Idle Wake Ups > 270 per second"

- **Citation.** Chromium issue 40657105, opened 2019-11-05, last event 2024-01-08 (timestamps extracted from the JSON).
- **Copy read.** `https://issues.chromium.org/action/issues/40657105`, 2026-09-19; `sources/S3-02/issue-40657105.json`, 100 006 bytes, SHA-256 `3a6b181739f1674dd332e93d03c768a9d88e9d0dbf728830153c9915021908d0`.
- **Passages (description).**
  > `UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36`
  >
  > `Steps to reproduce the problem:` / `Open https://www.newegg.com/amd-ryzen-7-3800x/p/N82E16819113104?reviews=all` / `Scroll somewhere to the middle of reviews.`
  >
  > `What is the expected behavior?` / `Close to 0% CPU usage.` / `Close to 0 idle wake ups.`
  >
  > `What went wrong?` / `See the attached screenshot.`
  >
  > `Chrome version: 78.0.3904.87  Channel: stable` / `OS Version: Fedora 31`
- **Coverage.** T1: covers — object: one idle foreground tab's renderer (a product page) in Chrome 78 on Fedora 31, unit "Idle Wake Ups" per second as Chrome's Task Manager reports (the figure "> 270 per second" is in the title only; the screenshot carrying it is not retrievable), statistic a single reading. T2, T3, T5: does not cover.
- **One observation?** Yes. Machine: not named. Subject: Chrome 78.0.3904.87 stable, one idle loaded tab. Window: not stated.

### S3-03 — Chromium issue 41248153 "High resource consumption on (Ubuntu) Linux"

- **Citation.** Chromium issue 41248153, opened 2016-04-08, last event 2017-07-24.
- **Copy read.** `https://issues.chromium.org/action/issues/41248153`, 2026-09-19; `sources/S3-03/issue-41248153.json`, 99 185 bytes, SHA-256 `0a4c7c23d6062299b1edd34666718e8c894a29e4f0e8c4007fff3f76281dd0a4`.
- **Passages (description).**
  > `UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36`
  >
  > `1. Update to one of the recent version of Chromium` / `2. High resource consumption (see powertop output)` / `3. Interestingly task manager does not report a high resource use`
  >
  > `Due to this significantly increased resource use, the battery life of my Thinkpad X230 halved.`
  >
  > `Chrome version: 49.0.2623.108  Channel: stable` / `OS Version: 4.3.0-040300-generic`
- **Coverage.** T1: covers weakly — object: Ubuntu Chromium 49 on a ThinkPad X230 (kernel 4.3.0), evidence "powertop output" attached (not retrievable); no number in the text. T2, T3, T5: does not cover.
- **One observation?** Yes, but the numbers are in an attachment; machine named (ThinkPad X230), version named, state not stated, window not stated.

### S3-04 — Chromium issue 41318993 "Graylog tabs take up 100% CPU each when not the active tab"

- **Citation.** Chromium issue 41318993, opened 2017-05-11, last event 2017-06-26.
- **Copy read.** `https://issues.chromium.org/action/issues/41318993`, 2026-09-19; `sources/S3-04/issue-41318993.json`, 102 413 bytes, SHA-256 `9a601f50060819c4bd2178de4e283e7db0eb1856319aea2abc8e3e8ab8808e12`.
- **Passages (description).**
  > `UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.47 Safari/537.36`
  >
  > `1. Open a tab to the Graylog log server UI (any tab will do, search, list, etc)` / `2. Select a different tab in that window to be the active tab` / `3. Check the Task Manager in chrome and watch the CPU stick at 99-100% for that tab.` / `4. GO back and activate the Graylog tab again, and watch the CPU go back down to (or near) 0%`
  >
  > `With that profile, I have taken a performance save (from the Performance tab in devtools, attached), a screen capture (attached), and a chrome://tracing trace (also attached).  Hopefully this helps.  Since the Performance tab save showed the majority of the time being idle CPU, I'm assuming that something in chrome itself is eating the CPU, as opposed to some runaway javascript code.`
  >
  > `Did this work before? Yes 58.0.3029.110 (64-bit)` / `Chrome version: 59.0.3071.47  Channel: beta` / `OS Version: 18.1 (Serena)`
- **Coverage.** T1: covers — object: a *background* tab's renderer (one site) in Chrome 59 beta on Linux Mint 18.1, unit CPU % as Chrome's Task Manager shows per tab, statistic a steady reading (99–100 % hidden, ~0 % when active); a `chrome://tracing` trace was attached but is not retrievable. T2, T3, T5: does not cover (the trace attachment would be T5 if reachable).
- **One observation?** Yes. Machine: not named. Subject: Chrome 59.0.3071.47 beta, one hidden tab. Window: not stated.

### S3-05 — Chromium issue 41476969 "Browser process taking up >140% of CPU while idle"

- **Citation.** Chromium issue 41476969, opened 2019-08-19, last event 2021-05-13.
- **Copy read.** `https://issues.chromium.org/action/issues/41476969`, 2026-09-19; `sources/S3-05/issue-41476969.json`, 99 708 bytes, SHA-256 `e5d6a032df60fa00d6066222f200eb7c63fbeceb36374e61503bd2e3696976b3`.
- **Passages (description).**
  > `UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36`
  >
  > `1. Open chromium, new tab page is enough`
  >
  > `The main browser process is consistently taking up to 140% CPU. I've attached a trace, it seems that the culprit could be QuotaManager::OriginDataDeleter but that's the first time I'm reading one of these traces so I'm not 100% sure.`
  >
  > `Running with extensions disabled has no effect (--disable-extensions).`
  >
  > `Chrome version: 76.0.3809.100  Channel: stable` / `OS Version: arch linux`
- **Coverage.** T1: covers the *browser* process, not a renderer — object: Chromium 76 browser process on Arch Linux with only the new-tab page, unit CPU % (top-style, >100 % = more than one core), statistic "consistently … up to 140%"; a pathological case with a trace attached (not retrievable). T2, T3, T5: does not cover.
- **One observation?** Yes. Machine: not named. Subject: Chromium 76.0.3809.100 stable, idle new-tab page. Window: not stated.

### S3-06 — Chromium issue 536046184 "Gemini idle state causes high CPU load (40%+) and 1GB+ memory leak on Ubuntu"

- **Citation.** Chromium issue 536046184, opened 2026-07-19, last event 2026-07-20.
- **Copy read.** `https://issues.chromium.org/action/issues/536046184`, 2026-09-19; `sources/S3-06/issue-536046184.json`, 100 844 bytes, SHA-256 `cf82d6d6e8cc40d9f751b905e6fa5b48fe1b0d9908fe997afe2fef8a8457f505`.
- **Passages (description).**
  > `1. Open Google Gemini (gemini.google.com) in a tab on Google Chrome (Linux/Ubuntu).` / `2. Use the interface normally for a while, then leave the tab open and idle in the background.` / `3. Open the Chrome Task Manager and observe the resource usage.`
  >
  > `In an idle state, the Gemini tab permanently consumes around 40% CPU load and suffers from a severe memory leak, with RAM usage climbing well over 1 GB. Hardware acceleration is verified as working via chrome://gpu, and other extensions have been disabled to isolate the issue. The high resource consumption completely stops as soon as the Gemini tab is closed.`
  >
  > `Chrome Channel: Stable`
- **Coverage.** T1: covers — object: one background tab's renderer (a web app) in Chrome stable on Ubuntu, unit CPU % per tab as Chrome's Task Manager shows, statistic "around 40%" steady. T2, T3, T5: does not cover.
- **One observation?** Yes. Machine: not named. Subject: Chrome stable (version number not given), one idle background tab. Window: not stated.

### S3-07 — Chromium issue 525786173 "Main page of chrome://discards is unreasonably CPU-hungry (55% CPU consumption, 100+ idle wakeups/s)"

- **Citation.** Chromium issue 525786173, opened 2026-06-20, last event 2026-06-22.
- **Copy read.** `https://issues.chromium.org/action/issues/525786173`, 2026-09-19; `sources/S3-07/issue-525786173.json`, 104 563 bytes, SHA-256 `7d4523dda86db41ed48360b4208cb8156906890351e4fe7fc2e2ae770369f83a`.
- **Passages (description).**
  > `1. Enter "chrome://discards" in the location field of the browser on a system with many open tabs (215 in my case).` / `2. The main page opens with a table of the tabs with some information about each.` / `3. On an otherwise idle system, note that the table doesn't change visibly.` / `4. Press Shift-ESC to open the Task Manager, and note that chrome://discards how it is the top tab in terms of CPU consumption and idle wakeups, in my case 55% CPU consumption and 100+ idle wakeups/s.`
  >
  > `If I switch to its graph tab, I see that it updates extremely frequently, maybe 60 times per second or so. Doing all the graph layout that often is understandably CPU intensive, but the CPU consumption is actually not that much higher (~70%) than when just showing the non-changing table of the main tab.` / `I note that the Task Manager updates once every 2 seconds, which seems like a more reasonable choice.`
  >
  > `Chrome Channel: Stable`
- **Coverage.** T1: covers — object: the renderer of one internal page (`chrome://discards`) in a session with 215 open tabs, unit CPU % and "idle wakeups/s" as Chrome's Task Manager reports per tab, statistic one reading (55 %, 100+/s; 70 % on the graph tab); the 215 other tabs are described only as ranking below it. **Operating system is not stated** in the description; the platform is unknown, so this is not confirmed as a Linux observation. T2, T3, T5: does not cover.
- **One observation?** Yes. Machine: not named; OS not named. Subject: Chrome stable, one visible internal page, 215 tabs loaded. Window: not stated.

### S3-08 — chromium-dev mailing list, "Improving power usage" (2009) — context (old)

- **Citation.** Joel Stanley, "[chromium-dev] Improving power usage", chromium-dev@googlegroups.com, 2009-07-13 08:19 (quoted in full inside Ryosuke Niwa's forward of 2009-07-13 08:34), mail-archive.com msg06007.
- **Copy read.** `https://www.mail-archive.com/chromium-dev@googlegroups.com/msg06007.html`, 2026-09-19; `sources/S3-08/chromium-dev-msg06007.html`, 12 800 bytes, SHA-256 `dcd7979bed61994fb7cff3cc17dfd442ff3fc1444d0c1bfa68391229e04c8c27`.
- **Passages (quoted mail body).**
  > `On my laptop I send SIGSTOP to Firefox when I'm not using it, to save battery without losing state.  This saves me 1 Watt when running Gmail in Firefox 3, or around 8% of the system power draw on my Thinkpad X300.`
  >
  > `Wakeups are not too bad, but any savings will mean longer lasting batteries:`
  >
  > `28.4% (187.4)       firefox-3.5 : hrtimer_start_range_ns (hrtimer_wakeup)` / `4.1% ( 26.9)            chrome : hrtimer_start_range_ns (hrtimer_wakeup)` / `2.3% ( 15.0)            chrome : ep_poll (process_timeout)`
  >
  > `(Powertop output of Firefox 3 vs Chromium trunk, one tab running Gmail, on Ubuntu Karmic)`
  >
  > `Perhaps we could run a powertop bot, that monitors an idle session with a few tabs opened to catch any regressions with timers.`
- **Coverage.** T1: covers as **context (2009, seventeen years old)** — object: Chromium trunk process(es) named `chrome` with one Gmail tab on Ubuntu Karmic, unit PowerTOP wake-ups per second per cause (26.9/s hrtimer, 15.0/s ep_poll) and share of all wake-ups, statistic one PowerTOP reading; machine ThinkPad X300. T2, T3, T5: does not cover.
- **One observation?** Yes. Machine: ThinkPad X300. Subject: Chromium trunk (no build number), one Gmail tab, idle. Window: not stated. Recorded as context only per the age rule.

### S3-09 — Chromium issue 41104634 "Chrome caught causing excessive wakeups." — context (macOS)

- **Citation.** Chromium issue 41104634 (formerly bugs.chromium.org 368774), opened 2014-04-30, last event 2022-02-02.
- **Copy read.** `https://issues.chromium.org/action/issues/41104634`, 2026-09-19; `sources/S3-09/issue-41104634.json`, 100 121 bytes, SHA-256 `76f56614f195ce1e1c600647027131ddc13043ac6a9a762499e3a316eba8a7d3`.
- **Passage (description).**
  > `2014-04-30 4:04:42.000 PM kernel[0]: process Google Chrome[82255] caught causing excessive wakeups. Observed wakeups rate (per sec): 225; Maximum permitted wakeups rate (per sec): 150; Observation period: 300 seconds; Task lifetime number of wakeups: 2079800`
  >
  > `Chrome version: 36.0.1964.2  Channel: dev` / `OS Version: OS X 10.9.2`
- **Coverage.** T1: **non-Linux context** — the macOS kernel's own wake-rate log for the Chrome browser process (225 wake-ups/s over a 300 s window). Not a candidate value. T2, T3, T5: does not cover.
- **One observation?** Yes; machine not named; window 300 s; platform OS X 10.9.2.

### S3-10 — Zoom Community thread "Zoom on Linux is using 2-7% CPU when idle"

- **Citation.** community.zoom.com, Meetings board, topic 23201 "Zoom on Linux is using 2-7% CPU when idle", published 2022-03-17T22:33:44+00:00, 11 replies through 2023-10-03.
- **Copy read.** `https://community.zoom.com/meetings-2/zoom-on-linux-is-using-2-7-cpu-when-idle-23201`, 2026-09-19; `sources/S3-10/zoom-community-23201.html`, 1 949 774 bytes, SHA-256 `b4c26f978a95ba267cbe32f7d6d85298c49aa8e934cc168998a5c4cc22ebf000` (posts are embedded in the page as HTML-escaped JSON `content` fields; text below is after unescaping and tag removal).
- **Passages.**
  - Topic (2022-03-17): > `Zoom on Linux is using ~2-7% CPU when idle and minimized to tray. Tried on Ubuntu 20.04 and Debian 11 with KDE Plasma. This drains my laptop battery. How to fix it?`
  - Reply 2022-04-21: > `I'm having the exact same issue om Ubuntu 21.10.`
  - Reply 2022-06-22: > `Same problem for me with Debian 11 on amd64 and Zoom 5.10.7 (but the problem has been present for a long time)`
  - Reply 2022-08-12: > `Same Ubuntu 22.04, zoom Version: 5.11.3 (3882)`
  - Reply 2022-09-20: > `This is the case for all our company Linux computers. It eats an average of 7% when doing nothing - not in a meeting. Is it possible to have at least an acknowledge from the Zoom team ?`
  - Reply 2023-03-24: > `Same problem, has been present for a long time (and I note this thread is 1y old now):   Zoom 5.14.0-1 on Archlinux (6.2.7 kernel)   Has been a problem for every version of zoom I have used for at least six months.`
  - Reply 2023-04-20: > `This continues.  Zoom support says it's "expected".      The client is consuming more CPU idle than Xorg.`
  - Reply 2023-05-15: > `I have an update from Zoom support.   The dev team has found several locations to optimize.     There may be some hope for this soon.`
  - Reply 2023-10-03 16:36: > `Zoom consumes ~100% of single CPU core when IDLE.. are you guys trying to mine crypto on my laptop ryzen 4500u?)) PS: Ubuntu Ubuntu 20.04.5 LTS`
  - Reply 2023-10-03 16:57: > `FWIW I've noticed that it's always the same thread which chews up CPU time:       /opt/zoom/zoom --type=utility --utility-sub-type=unzip.mojom.Unzipper --service-sandbox-type=utility [...]   Killing this process (SIGTERM) has no noticeable impact on Zoom -- calls still work just fine.`
  - Reply 2023-10-03 17:32: > `In my case, it was not the `--type=utility` process, but the top child in the process hierarchy.    During idle, I see no activity at all for that `--type=utility` process at all.`
- **Coverage.** T2 (Zoom): covers — object: the Zoom Linux client idle and minimized to tray (versions 5.10.7, 5.11.3 (3882), 5.14.0-1 named by repliers), unit CPU % of one core as a system monitor shows, statistic "~2-7%" (topic), "an average of 7%" (one company's fleet), "~100% of single CPU core" (one Ryzen 4500U laptop, a pathological case attributed to a `--type=utility --utility-sub-type=unzip.mojom.Unzipper` helper process); also process-structure evidence (`/opt/zoom/zoom --type=utility …` helper). No wake cadence, no CPU per wake. T1, T3, T5: does not cover.
- **One observation?** No — several reporters, each one reading; machines mostly unnamed (one "ryzen 4500u"); state idle/minimized; windows not stated.

### S3-11 — Zoom Community thread "Zoom 5.15.3.4839 on Ubuntu Linux high CPU load"

- **Citation.** community.zoom.com, Meetings board, topic 39563, published 2023-07-22T01:18:14+00:00, 7 replies through 2024-05-20.
- **Copy read.** `https://community.zoom.com/meetings-2/zoom-5-15-3-4839-on-ubuntu-linux-high-cpu-load-39563`, 2026-09-19; `sources/S3-11/zoom-community-39563.html`, 1 920 032 bytes, SHA-256 `c4c9e89f80fd1ccff4a8b6cea8b7e7222a4f90bd753feabf2f83024e29d75927`.
- **Passages.**
  - Topic: > `Not sure if this is the right board to report this issue - I recently upgraded my zoom from 5.12.9.367 to 5.15.3.4839 on my Ubuntu 22.04 Linux, and found that the new version of zoom keeps on using 100% CPU even during idle. After I reverted the version back to 5.12, this behavior disappeared.   My Linux kernel is 5.15.0-76-generic, with NVIDIA rtx 2060 GPU, driver version 525.125.06.`
  - Reply 2023-09-28: > `I've been having similar issues for a while (I'm on 6.5 but this has been going on for over a year, possibly since 5.12/5.13). I'm pretty sure it's to do with the `mojom.Unzipper` module (from here: https://chromium.googlesource.com/chromium/src/+/HEAD/mojo/public/tools/bindings/README.md? ) because this is the process which has 100% CPU for me, and killing it always solves the problem (with no noticeable effect on Zoom).   See if you have the same process in something like htop.`
  - Reply 2024-01-11: > `I can confirm this issue on 5.16.6.382 on Ubuntu 22.04.3. Temporary fix mentioned by @gtf21  still works.`
  - Reply 2024-05-20: > `I still have this issue. I installed Zoom client to the following Ubuntu versions: 20.04, 22.04, 24.04 I observed the same behavior on all of those: within ~10 minutes of the meeting started it started loading the CPU to 100%. It doesn't depend on video cards - I tried two different ones: - nvidia Quadro M2200 (Driver Version: 535.171.04) - intel 630 My laptop specs: Intel® Core™ i7-7820HQ CPU @ 2.90GHz × 8 Memory: 32GB`
- **Coverage.** T2 (Zoom): covers a pathological idle case — object: Zoom 5.15.3.4839 / 5.16.x on Ubuntu 22.04 (kernel 5.15.0-76, RTX 2060 named), unit CPU % of one core, statistic "100% CPU even during idle", attributed by repliers to the `mojom.Unzipper` utility process; one replier reports 100 % "within ~10 minutes of the meeting started" on an i7-7820HQ laptop. T1, T3, T5: does not cover.
- **One observation?** No — several reporters; the topic author names machine parts (kernel, GPU, driver) and version; state idle; window not stated.

### S3-12 — Framework Community "Discord power usage on Linux" (powertop)

- **Citation.** community.frame.work topic 25401 "Discord power usage on Linux", user Stetsed, created 2022-12-07T16:03:25Z, 3 posts.
- **Copy read.** `https://community.frame.work/t/discord-power-usage-on-linux/25401.json` (Discourse JSON), 2026-09-19; `sources/S3-12/frame-work-25401.json`, 18 400 bytes, SHA-256 `51062730f19eb3b415e2beacce1cf223d61802cf86acb9d55ae64a6fa003240c`.
- **Passages (post 1, `cooked` field with tags removed).**
  > `today I decided to do some testing of power levels for discord on Linux desktop. Mostly I wanted to test between the main discord app, the discord canary app(which uses a newer version of electron) and the discord web browser version as I found that the default discord app doesn’t let the cpu enter lower c-states. I am using Librewolf as my browser and have installed discord and discord canary from there arch package and AUR package respectively. The modules that are installed are 2 USB-C, 1 USB type A and 1 DisplayPort. And optimizations are the ones done by powertop auto tune.`
  >
  > `Method I decided to for each of the setups test it 3 times using powertop to test it. I ran 3x each setup testing them for 240 seconds each time to give it time to equalize out and then averaged out the result. The first setup is librewolf empty + discord canary, the second is librewolf empty + discord main, and the third is librewolf with discord web app.`
  >
  > `Results Discord Canary + Librewolf : 5.6w Discord Main + Librewolf : 6.6w Librewolf Discord Webapp : 7.9w`
  >
  > `Why this is I do not exactly know but we suspect it has something to do with older versions of electron having problems with higher C-states as the main discord app I do not see high c-states.`
- **Coverage.** T2 (Discord): covers — object: whole-laptop power draw with Discord (main vs Canary vs web in Librewolf) idle, unit watts from powertop's discharge estimate, statistic mean of 3 × 240 s runs per setup (5.6 / 6.6 / 7.9 W); a Linux observation on a Framework laptop (Arch; expansion modules named; CPU model and Discord build not named). Not per process, not CPU %, no wake cadence. T1, T3, T5: does not cover.
- **One observation?** Yes, one reporter, one machine, three configurations. Machine: Framework laptop (model/CPU not named). Subject: Discord main and Canary from Arch/AUR packages (versions not named), idle. Window: 240 s × 3 per setup.

### S3-13 — Arch Linux forums "Discord high CPU usage (possible pulseaudio problem)"

- **Citation.** bbs.archlinux.org topic 255768, user ptersilie, posts #1 (2020-05-15 22:35:19) and #3 (2020-05-16 13:56:22).
- **Copy read.** `https://bbs.archlinux.org/viewtopic.php?id=255768`, 2026-09-19; `sources/S3-13/archlinux-bbs-255768.html`, 31 103 bytes, SHA-256 `5fc2da66892911ce8d3d438d3e56e5f76978991e751d25994fc7c2db61412591`.
- **Passages.**
  - #1: > `I'm having unusually high CPU usage (35-45%) when using Discord on my desktop (I would be expecting something more along 5%). The problem seems to be related to the recording of audio, since it goes down to 10% when I enable push-to-talk and am not speaking (though 10% is still a bit high). The problem is the same for both the Discord app and running it in the browser. On top of Discord I'm also getting another 10% CPU usage from pulseaudio, which makes me think this might actually be a pulseaudio issue.`
  - #3: > `I just ran another test and noticed that the CPU usage is not as high if I run Discord in Chrome (around 10% while recording audio, compared to 35% with the Electron app or in Firefox).`
  - #2 (moderator): > `There was a chromium/electron bug. It seems to have gotten fixed in chromium itself but it's unclear when all the gazillion electron implementations will be relevantly updated.`
- **Coverage.** T2 (Discord): covers — object: Discord Electron app on Arch Linux while in a voice channel (audio capture on / push-to-talk), unit CPU % (tool not named), statistic single readings (35–45 % capturing, 10 % with push-to-talk idle, ~10 % in Chrome; plus 10 % pulseaudio). "Under traffic" (voice) rather than idle. No wake cadence. T1, T3, T5: does not cover.
- **One observation?** Yes, one reporter. Machine: not named (the pasted `pacmd` output names an NVIDIA GP104 HDMI audio device and an Intel PCH ALC887 codec). Subject: Discord (version not named), voice active / push-to-talk. Window: not stated.

### S3-14 — flathub/com.discordapp.Discord issue #260 "Enabling Hardware Acceleration causes extermely high CPU usage"

- **Citation.** GitHub flathub/com.discordapp.Discord issue 260, opened 2023-01-08T22:50:31Z, closed, 2 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-14/flathub-com.discordapp.Discord-260.json`, 900 bytes, SHA-256 `6c18e55d73c9826ee56aadcf8cddc8f1899c9a8e493092cca1c0fa05f75fa7d5`.
- **Passage (body).**
  > `Enabling Hardware Acceleration cause my CPU (8700K) to jump to 70-90% CPU usage; making the application barely usable causing the Audio to lag, and everything to slow down to a crawl.` / `Turning off Hardware Acceleration brought down the CPU usage to 30-50%; which still seems high, but solves most of the problems.` / `FWIW I'm using Prime (which I think is actually Reverse Prime), I dunno if that has anything to do with it.`
- **Coverage.** T2 (Discord): covers — object: Discord Flatpak on Linux (Flathub tracker), unit CPU % (tool and per-process/whole-CPU basis not stated), statistic ranges (70–90 % with GPU acceleration, 30–50 % without) on an i7-8700K with PRIME graphics; state not stated (in use). T1, T3, T5: does not cover.
- **One observation?** Yes; machine partly named (8700K); Discord version not named; state and window not stated.

### S3-15 — element-hq/element-web issue #29682 "Constant CPU wakeups and CPU usage while the web version of Element is unfocused in a background tab"

- **Citation.** GitHub element-hq/element-web issue 29682, opened 2025-04-05T16:45:26Z, open, 8 comments (not retrievable; the Wayback capture of 2025-05-28 holds no comment bodies).
- **Copy read.** MCP body, 2026-09-19; `sources/S3-15/element-web-29682.json`, 3 500 bytes, SHA-256 `9fa05ba38bb345b670c8f7d456471b1c6cd9b96eee8ec6b8b03f8ddd4ce7f812`.
- **Passages (body).**
  > `1. Launch Firefox with just one normal static website loaded (ex: this GitHub ticket), observe CPU usage to be roughly 0% on idle.` / `2. Open a Firefox tab to app.element.io (with your user account logged in etc.)` / `4. Switch back to the other tab (ex: this github ticket) in Firefox, so that the Element tab is only in the background`
  >
  > `Constant 5 to 15% CPU usage (when not dividing CPU usage by the number of vCores, i.e. "not Solaris mode").`
  >
  > `My laptop computer has a fairly recent power-efficient Intel Kabylake i5-8350U CPU that normally sits around 37-40°C with the fan turned off completely when nothing is using the CPU (so that it can enter deep sleep states). When I _don't_ have the Element web app tab open, it happily goes back down to 0% CPU usage and lower temperatures with the fan turning off entirely.`
  >
  > `This happens even when the browser is minimized, on another workspace, etc.`
  >
  > `FWIW, my account is present in roughly 55 rooms, at least half (if not 70% or more) are mostly idle or fairly quiet, I'm not on super-busy rooms in general, and I'm not in thousands of rooms.`
  >
  > `### Operating system` / `Fedora 41` / `### Browser information` / `Firefox 137.0` / `### URL for webapp` / `app.element.io` / `### Homeserver` / `matrix.org`
- **Coverage.** T2 (Element): covers — object: the Element *web* client (app.element.io) in a background Firefox tab, logged in, ~55 rooms, idle, on Fedora 41 with an i5-8350U, unit CPU % of one core ("not Solaris mode"), statistic a steady range (5–15 %); the title's "constant CPU wakeups" is the reporter's inference from fan/temperature, no wake rate is given. This is Element under Gecko, not the Electron desktop client. T1: does not cover (Firefox). T3, T5: does not cover.
- **One observation?** Yes. Machine: laptop with Intel i5-8350U (model not named). Subject: Element web (version not given), Firefox 137.0, background tab, idle. Window: not stated.

### S3-16 — element-hq/element-web issue #32107 "Element-desktop-nightly have more CPU usage"

- **Citation.** GitHub element-hq/element-web issue 32107, opened 2024-03-13T20:42:57Z, open, 14 comments (not retrievable).
- **Copy read.** MCP body, 2026-09-19; `sources/S3-16/element-web-32107.json`, 1 256 bytes, SHA-256 `3568d371b26077ff6cf01e8ab22610f97c2d9ea300d2fd43888a06f0299ba11b`.
- **Passages (body).**
  > `1. start element-desktop-nightly` / `2. wait sync complyte` / `3. see cpu usage - element use ~60-70% cpu`
  >
  > `more use cpu usege by element in range 60-70% in idle state` / `I was try start element with disabling gpu, but this was not help:` / `--disable-gpu --in-process-gpu`
  >
  > `### Operating system` / `Debian 12` / `### Application version` / `Element-desktop-nightly 2024030901` / `### Homeserver` / `matrix-synapse-py3                   1.89.0+bullseye1`
- **Coverage.** T2 (Element): covers a pathological case — object: Element Desktop nightly 2024030901 on Debian 12 after initial sync, idle, unit CPU % (screenshot not retrievable), statistic "~60-70%". T1, T3, T5: does not cover.
- **One observation?** Yes. Machine: not named. Subject: Element Desktop nightly 2024030901, idle after sync, self-hosted Synapse. Window: not stated.

### S3-17 — element-hq/element-web issue #32167 "CPU cyles over time are very high, even only running in the background (desktop, linux)"

- **Citation.** GitHub element-hq/element-web issue 32167, opened 2023-04-26T08:55:36Z, open, 9 comments (Wayback 404).
- **Copy read.** MCP body, 2026-09-19; `sources/S3-17/element-web-32167.json`, 1 669 bytes, SHA-256 `6099b813cf0b5129b7299b892c754185a5f7258224680c42d27fdc858d9ddca6`.
- **Passages (body).**
  > `Starting to check CPU cycles on linux system via graphical process monitor (ubuntu linux 22.04 LTS, Kernel 6.3 mainline)` / `2. Checking the CPU-time collumn and comparing it with other processes` / `3. realizing that element-desktop is the 3rd CPU-cycle hungriest app (even only running in the background), after the gnome-shell and Xwayland, which are necessary and always used system components`
  >
  > `I did expect this messenger to use up less resources when running in the background with only 3 contacts and 2 news sources.`
  >
  > `### Application version` / `Element: 1.11.29 Olm: 3.2.12`
- **Coverage.** T2 (Element): covers only as a ranking — object: Element Desktop 1.11.29 on Ubuntu 22.04 running in the background with a small account, unit accumulated CPU time (rank among processes, no figure), statistic "3rd … after gnome-shell and Xwayland". T1, T3, T5: does not cover.
- **One observation?** Yes, but without a number; machine not named; window not stated.

### S3-18 — IsmaelMartinez/teams-for-linux issue #328 "100% cpu utilization"

- **Citation.** GitHub IsmaelMartinez/teams-for-linux issue 328, opened 2020-03-13T16:58:29Z, closed, 2 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-18/teams-for-linux-328.json`, 747 bytes, SHA-256 `42e8bde9a89380137a627515e291737d2cc58da3633cf38c257b4f4e178d7d71`.
- **Passage (body).**
  > `After every call, cpu usage of teams spike to 100% all the time.` / `Relaunching application fix it, untile the next call.` / `teams 1.3.00.958 (.deb package)` / `Ubuntu 18.04.4 LTS`
- **Coverage.** T2 (Teams): covers a pathological post-call state — object: teams-for-linux (Electron wrapper) 1.3.00.958 on Ubuntu 18.04.4, unit CPU % (screenshot not retrievable), statistic "100% all the time" after a call. Note the wrapper is the community `teams-for-linux`, not Microsoft's discontinued native Linux client. T1, T3, T5: does not cover.
- **One observation?** Yes; machine not named; window not stated.

### S3-19 — IsmaelMartinez/teams-for-linux issue #293 "CPU 100% Utilization"

- **Citation.** GitHub IsmaelMartinez/teams-for-linux issue 293, opened 2019-10-14T09:01:08Z, closed, 5 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-19/teams-for-linux-293.json`, 969 bytes, SHA-256 `f4f076fd58ac08c15238ef233dd5099bc9e4dd6aa696c175e82f7231ef4804cc`.
- **Passage (body).**
  > `I was install teams-for-linux on my Kali (Ubuntu) distribution via snap.` / `When I running app always I have 100% utilization of CPU. It's not change at all.` / ` - OS: Linux ghost 5.2.0-kali3-amd64 #1 SMP Debian 5.2.17-1kali1 (2019-09-27) x86_64 GNU/Linux` / ` - Installation package snap` / ` - Version 0.7.0`
- **Coverage.** T2 (Teams): covers a pathological case — teams-for-linux 0.7.0 snap on Kali (kernel 5.2.0), 100 % CPU continuously (screenshot not retrievable). T1, T3, T5: does not cover.
- **One observation?** Yes; machine not named; state "always"; window not stated.

### S3-20 — IsmaelMartinez/teams-for-linux issue #652 "High CPU usage"

- **Citation.** GitHub IsmaelMartinez/teams-for-linux issue 652, opened 2022-12-07T11:56:56Z, closed, 13 comments (Wayback 404).
- **Copy read.** MCP body, 2026-09-19; `sources/S3-20/teams-for-linux-652.json`, 759 bytes, SHA-256 `b09a11f2fc41cf3a522fafe044de8aec11c6a569d0aba82d418f878d6ca2c9d3`.
- **Passage (body).**
  > `Since last week, CPU usage has spiked to 100% whenever I open the program.` / `I've tried uninstalling and deleting all cache I could find, but the issue persists` / ` - OS: Kubuntu 22.04.1` / ` - Installation package deb` / ` - Version 1.0.45 and 1.1.46`
- **Coverage.** T2 (Teams): covers a pathological case — teams-for-linux 1.0.45/1.1.46 deb on Kubuntu 22.04.1, 100 % CPU on open. T1, T3, T5: does not cover.
- **One observation?** Yes; machine not named; window not stated.

### S3-21 — wireapp/wire-desktop issue #8975 (Electron chat client process tree on Ubuntu 24.04) — context

- **Citation.** GitHub wireapp/wire-desktop issue 8975 "Wire starts a process in the background consuming almost 100% of CPU core (/proc/self/exe)", opened 2025-08-02T12:10:31Z, open, 1 comment. Wire is not one of T2's named clients; recorded as context for Electron process structure on Linux.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-21/wire-desktop-8975.json`, 4 653 bytes, SHA-256 `cb84e863e325984ead03532d0988f4fb7c3f6d1c1d12d5dc090263c023edfb07`.
- **Passages (body; `ps -o pid,comm,args $(pgrep wire-desktop)` listing, command lines shortened by the reader with `…` only where marked).**
  > `It happens on all three computers running Ubuntu 24.04. When I start Wire, several new processes appear in the background. All of them are wire-desktop, but most of them were executed as  '/proc/self/exe ...', and one of them is consuming almost 100% of one CPU core.`
  >
  > `   7688 wire-desktop    wire-desktop` / `   7691 wire-desktop    /opt/Wire/wire-desktop --type=zygote --no-zygote-sandbox` / `   7693 wire-desktop    /opt/Wire/wire-desktop --type=zygote` / `   7695 wire-desktop    /opt/Wire/wire-desktop --type=zygote` / `   7736 wire-desktop    /opt/Wire/wire-desktop --type=zygote --no-zygote-sandbox` / `   7762 wire-desktop    /proc/self/exe --type=utility --utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=none …` / `   7793 wire-desktop    /proc/self/exe --type=renderer … --renderer-client-id=4 …` / `   7854 wire-desktop    /proc/self/exe --type=renderer … --renderer-client-id=9 …` / `   7855 wire-desktop    /proc/self/exe --type=renderer … --renderer-client-id=10 …` / `   7904 wire-desktop    /proc/self/exe --type=utility --utility-sub-type=audio.mojom.AudioService …` / `   7947 wire-desktop    /opt/Wire/wire-desktop --type=zygote`
  >
  > `The process with pid 7854 is the one consuming the CPU.`
  - Every renderer line carries `--disable-features=SpareRendererForSitePerProcess,WebRtcHideLocalIpsWithMdns` and `--num-raster-threads=4`.
- **Coverage.** T2: context only (client not in the list) — one Linux `ps` listing of an Electron chat client's tree: 1 main, 5 zygotes, 3 renderers, 2 utility processes (NetworkService, AudioService); one renderer at ~100 % of a core (pathological). T1: covers what Electron shares of Chromium's process model, as a Linux observation of process roles (`--type=zygote`, `--type=renderer`, `--type=utility --utility-sub-type=…`). T3, T5: does not cover.
- **One observation?** Yes (one listing); machine not named (Ubuntu 24.04, "three computers"); Wire version not named; state just started; window a `ps` snapshot.

### S3-22 — ValveSoftware/steam-for-linux issue #12616 "Steam idles in a power inefficient manner"

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 12616, opened 2026-01-03T20:15:27Z, open, 0 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-22/steam-for-linux-12616.json`, 5 958 bytes, SHA-256 `739bca9f363b4a99dd7c43e801c43afb117058575a7e5e97f704445fe229e841`.
- **Passages (body).**
  > `* Steam client version (build number or date): 1766451605` / `* Distribution (e.g. Ubuntu): NixOS` / `* GPU: Intel integrated on Laptop, AMD dedicated on desktop`
  >
  > `Steam when idle and offscreen uses additional extra power continuously and consistently. … On a laptop an extra 0.5W means quite a lot. On my desktop computer the power difference from steam idling in the background is more like 10W`
  >
  > `I attempted to isolate the problem as much as possible. I grabbed an older intel laptop and ran only steam as well as profiling tools on it. The laptop is running on battery power using the powersaving governor.`
  >
  > `The power consumption on the laptop right after boot with power just the profiling tools (powertop, turbostat) running is:` / `1. powertop: "The battery reports a discharge rate of 2.6 to 2.8W"` / `2. turbostat: "PkgWatt=0.19,CorrWatt=0.6,GFXWatt=0.00,RAMWatt=0.51,SysWatt=0.41"`
  >
  > `Then I ran (logged out) steam, moved it offscreen (a different workspace) and left it be there for a couple minutes to let it settle.` / `1. powertop: "The battery reports a discharge rate of 3.3W"` / `2. turbostat: "PkgWatt=0.6,CorWatt=0.29,GFXWatt=0.01,RamWatt=0.56,SysWatt=1.28"`
  >
  > `I then logged in, opened Divinity 2 Original Sin from my library, moved steam offscreen and left it there for a couple minutes to settle. There are no games installed and no updates to do.` / `1. powertop: "The battery reports a discharge rate of 3.3W"` / `2. turbostat: "PkgWatt=0.71,CorWatt=0.2, GFXWatt=0.02,RAMWatt=0.55,SysWatt=1.19"`
  >
  > `Powertop further shows significant wakeups produced by steam and various steamwebhelper processes. Here's an strace from one of the steamwebhelper processes:`
  >
  > `# strace -tt -p $EXPENSIVE_STEAM_THREAD` / `HH:MM:SS.226540 sendto(48, "\10\0\0\0h\0\0\0\30\0\24\0\0\0\0\0\200r\230\2\0\0\0\0\0\0\0\0\0\0\0\0"..., 104, MSG_NOSIGNAL, NULL, 0) = 104` / `HH:MM:SS.226559 recvmsg(18, {msg_namelen=0}, 0) = -1 EAGAIN (Resource temporarily unavailable)` / `HH:MM:SS.226570 poll([{fd=18, events=POLLIN}, {fd=40, events=POLLIN}, {fd=41, events=POLLIN}], 3, 0) = 0 (Timeout)` / `…` / `HH:MM:SS.226596 poll([{fd=18, events=POLLIN}, {fd=40, events=POLLIN}, {fd=41, events=POLLIN}], 3, 6) = 1 ([{fd=41, revents=POLLIN}])` / `HH:MM:SS.227833 recvmsg(18, {msg_namelen=0}, 0) = -1 EAGAIN (Resource temporarily unavailable)` / `HH:MM:SS.227852 read(41, "!", 2)        = 1` / `…` / `HH:MM:SS.227903 poll([{fd=18, events=POLLIN}, {fd=40, events=POLLIN}, {fd=41, events=POLLIN}], 3, 5) = 0 (Timeout)` / `HH:MM:SS.232969 recvmsg(18, {msg_namelen=0}, 0) = -1 EAGAIN (Resource temporarily unavailable)` / `HH:MM:SS.232991 sendto(48, "\10\0\0\0h\0\0\0\30\0\24\0\0\0\0\0\201r\230\2\0\0\0\0\0\0\0\0\0\0\0\0"..., 104, MSG_NOSIGNAL, NULL, 0) = 104` / `…` / `HH:MM:SS.238365 recvmsg(18, {msg_namelen=0}, 0) = -1 EAGAIN (Resource temporarily unavailable)` / `HH:MM:SS.238380 sendto(48, "\10\0\0\0h\0\0\0\30\0\24\0\0\0\0\0\202r\230\2\0\0\0\0\0\0\0\0\0\0\0\0"..., 104, MSG_NOSIGNAL, NULL, 0) = 104`
- **[own computation]** The three `sendto(48, …)` timestamps in the quoted strace are `.226540`, `.232991`, `.238380`: gaps of 6.451 ms and 5.389 ms (`python3 -c "print(232991-226540, 238380-232991)"` → `6451 5389` µs). Each cycle is a `poll` with a 5–6 ms timeout followed by a 104-byte `sendto` — the reporter's thread wakes roughly every 5–6 ms in this excerpt (three cycles, ~12 ms of trace). This locates a cadence; it is not a value.
- **Coverage.** T3: covers — object: the Steam client (build 1766451605, NixOS) idle and offscreen, logged out and logged in, no game running, unit whole-laptop watts (powertop discharge; turbostat PkgWatt/CorWatt/…), statistic settled readings after "a couple minutes" (2.6–2.8 W baseline → 3.3 W with Steam), plus a per-thread strace of one `steamwebhelper` thread showing a ~5–6 ms poll/sendto cycle; "Powertop further shows significant wakeups produced by steam and various steamwebhelper processes" without the table. Not during play. T1: context for CEF hosts (steamwebhelper is CEF). T2, T5: does not cover.
- **One observation?** Yes, one reporter, one laptop. Machine: "an older intel laptop" (model not named). Subject: Steam build 1766451605, idle offscreen. Window: "a couple minutes" per state; the strace excerpt spans ~12 ms.

### S3-23 — ValveSoftware/steam-for-linux issue #7241 "[beta] steam chat window is significantly CPU intensive, even idle and hidden"

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 7241, opened 2020-07-04T20:01:27Z, open, 16 comments (Wayback capture 2025-12-22 holds no comment bodies).
- **Copy read.** MCP body, 2026-09-19; `sources/S3-23/steam-for-linux-7241.json`, 1 108 bytes, SHA-256 `61fee3121313a25725c15b3befa5428770a0c7495a1cb0d0dcbbfb51aa702d19`.
- **Passage (body).**
  > `dota2 performance was significantly down.` / `Started to investigate and was lucky enough to find out it was the steam chat window: if opened, even "idling" and/or hidden, roughly 5 steam client related processes are eating each a steady 20-30% of CPU time (using "top" command). If I close the steam chat window, those processes have their CPU usage back to near 0.` / `I run an up-to-date beta steam client, onto a state of the art gfx stack, x11 native (no xwayland). I did disable GPU acceleration of the GUI, and even if I  do enable GPU acceleration I don't want the steam chat window to use the CPU/GPU while hidden.`
- **Coverage.** T3: covers — object: the Steam beta client's chat window (July 2020) with a game (Dota 2) running, unit CPU % per process as `top` shows, statistic "roughly 5 steam client related processes … each a steady 20-30%" while the chat window is open and hidden, "near 0" when closed. Machine, distribution and build not named. T1, T2, T5: does not cover.
- **One observation?** Yes (one reporter's `top` reading); machine not named; version "up-to-date beta" (2020-07); state chat window open/hidden during play; window not stated.

### S3-24 — ValveSoftware/steam-for-linux issue #13309 "steamwebhelper zygote spins at ~90%+ CPU (eventfd busy-loop) when "Explore Your Discovery Queue" banner is visible on Store front page"

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 13309, opened 2026-06-11T04:54:51Z, open, 2 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-24/steam-for-linux-13309.json`, 2 460 bytes, SHA-256 `bf7d7646e33deb24415dbe8cfb1835834785d7569609561073e31b123ddac906`.
- **Passages (body).**
  > `Steam client version: 1781041600` / `Distribution: Ubuntu 25.10` / `GPU: AMD RX 7800xt` / `Compositor/DE: Niri (Wayland)`
  >
  > `Actual: The steamwebhelper zygote process (--type=zygote) consumes ~90-95% of one CPU core continuously while the Store front page is open, specifically when the "Explore Your Discovery Queue" banner (rotating game-art carousel) is visible or near-visible in the viewport.`
  >
  > `strace on the zygote process shows it repeatedly writing \x01\x00\x00\x00\x00\x00\x00\x00 to an eventfd in a tight loop, consistent with a CEF/Chromium task being continuously reposted in the message loop (busy-wait), rather than the event loop idling normally.`
  >
  > `- Running with -disable-gpu reduces CPU usage from ~94% to ~36%, but does not eliminate it - the eventfd loop continues at a lower rate.` / `- Reproduces on both the native Steam package and the Flatpak (com.valvesoftware.Steam) build.`
  >
  > `2. Observe steamwebhelper CPU usage in htop/top (~90-95% on one core, even when idle).`
- **Coverage.** T3: covers a pathological idle case — object: one `steamwebhelper --type=zygote` process of Steam build 1781041600 on Ubuntu 25.10 (RX 7800 XT, Niri/Wayland) with the Store front page visible and no interaction, unit CPU % of one core from htop/top, statistic "~90-95%" (~36 % with `-disable-gpu`); triggered by an animated banner; no game running. T1: context for a CEF host's process naming (`--type=zygote` process doing rendering work). T2, T5: does not cover.
- **One observation?** Yes; machine partly named (GPU, distribution, compositor; CPU not named); Steam build named; state idle on Store page; window not stated.

### S3-25 — ValveSoftware/steam-for-linux issue #8258 "please reopen: steamwebhelper consuming cpu even if minimized" (Wayback capture with comments)

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 8258, opened 2021-11-24T11:42:33Z, closed, 63 comments; the capture holds the body and 13 comments (`createdAt` values in the capture: 2021-11-24T11:42:33Z, 2021-11-24T12:56:46Z, 2021-11-24T12:56:46Z, 2021-12-20T11:03:31Z, 2021-12-20T11:08:03Z, 2021-12-21T20:07:07Z, 2021-12-21T20:24:46Z, 2021-12-22T01:45:18Z, 2021-12-31T10:05:06Z, 2022-01-22T15:31:01Z, 2022-01-23T14:28:24Z, 2022-01-23T14:55:36Z, 2022-02-16T22:13:24Z, 2022-02-16T22:33:13Z, 2022-04-01T23:08:41Z, 2022-04-08T17:43:29Z; comment-to-date mapping below is by order, the reader's reading).
- **Copy read.** `https://web.archive.org/web/20260419042556id_/https://github.com/ValveSoftware/steam-for-linux/issues/8258` (memento 2026-04-19 04:25:56), fetched 2026-09-19; `sources/S3-25/wayback-20260419042556-steam-for-linux-8258.html`, 284 722 bytes, SHA-256 `e9986f9915cb40894b6f269a71b4769be25ab30988e619d171685d7633ba9902`. Bodies are JSON strings inside the page's React payload (`"body":"…"`), decoded by the reader.
- **Passages.**
  - Body (2021-11-24): > `* Steam client version: Nov 22 2021 at 22:12:42 ; Steam package version 1637624439` / `* Distribution: Archlinux` / `* Opted into Steam client beta?: NO` / `1. From the steam client store tab, have a video playing` / `2. note that the cpu is higher, it is due to steamwebhelper cpu usage, note it.` / `3. minimize steam client` / `4. Notice that the cpu usage remains the same`
  - Comment 1: > `Bump. From my testing, it's not only consuming ~25% single core CPU but also some amount of GPU, potentially lowering gaming performance. This can be quite a dealbreaker and should be fixed.` / `I did not observe this behavior on Windows.`
  - Comment 3: > `I can confirm that steam cpu usage really high especially with latest versions stemwebhelper few processes consuming in total about 130-150%, just one process about 70-80% and never gets low no matter is it minimized or not. It's 4 cored laptop with hyperthreading so basically almost half of CPU resources are busy with steam client it is additionally to high memory usage... I haven't played any video just simply launched steam client and sometimes I can play some games...`
  - Comment 5: > `**Problem**: steamwebhelper (CEF) does not detect whether it's occluded/minimized and constantly continues rendering in the background.` / `**Workaround**: Switch Steam to a page that does not have videos or animations. In the case of library pages, you need to enable "Low Performance Mode" from "Settings->Library" or the glowing achievements frames would ruin the performance.`
  - Comment 6: > `To add another feedback on Steam Beta for Linux, here on Arch:` / `- Steamwebhelper uses a full cpu thread from the moment I launch it on the 'Store' page till I change to eg the 'Library' page.` / `- Steamwebhelper's CPU use while playing a game goes up to 37.5% of my 4 threads 2 cores Intel CPU @3.3GHz (more CPU than the game I play...). That was after hours playing with Steam minimized before starting this game.` / `- observations above all are with "Low Performance Mode" activated.` / `- High CPU usage isn't new here. *staying high* is.`
  - Comment 7: > `Ate all my CPU too, indeed even with "low performance mode"` / `Workaround ~ load steam without the browser function :` / `steam steam://open/minigameslist -console -no-browser` / `Steam looks really dated like that, but I can at least play my games without the 50% FPS decrease.`
  - Comment 10: > `With around ~2000 games, my steam/steamwebhelper processes uses more than **1.45 GB**, just after launch. (Despite that I have all "low performance" boxes checked) + **10-40% CPU** (on a 12-cores Ryzen). Minimizing steam windows does not change anything.` / `If I launch steam with  `-no-browser` (what a lifesaver !), steam uses only **261 MB** + 0/1 % CPU`
  - Comment 12: > `This seems to be the only working solution for me. Otherwise 1 cpu core of my laptop is 25% utilized and the fans scream when ever steam just idles in the background.`
- **Coverage.** T3: covers — object: `steamwebhelper` (CEF) processes of Steam 1637624439-era clients (late 2021 – early 2022) on Arch and other Linux systems, minimized/backgrounded and *during play*, unit CPU % per process from system monitors, statistics from several reporters: ~25 % of one core (minimized, video on Store page); "in total about 130-150%, just one process about 70-80%" on a 4-core HT laptop (Store page, no video); "37.5% of my 4 threads 2 cores Intel CPU @3.3GHz" while a game runs (Low Performance Mode on); 10–40 % on a 12-core Ryzen with ~2000 games; ~0–1 % with `-no-browser`. Also the process structure: `steam` main plus `steamwebhelper` processes; the `-no-browser` switch removing CEF. No wake cadence. T1: context on what CEF hosts do with occluded windows (comment 5's diagnosis). T2, T5: does not cover.
- **One observation?** No — several reporters' single readings; machines named only as core counts/clock; Steam versions named for the body (1637624439) and "Beta" for comment 6; states minimized / Store page / during a game; windows not stated.

### S3-26 — ValveSoftware/steam-for-linux issue #9266 "Steam Client using 100% CPU when idle"

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 9266, opened 2023-03-16T13:36:21Z, closed, 3 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-26/steam-for-linux-9266.json`, 2 390 bytes, SHA-256 `718eb174748d58bd0e722ecce8707462e76ef270c564fe52909ee162f12d7fed`.
- **Passages (body).**
  > `* Steam client version (build number or date): 1676336721 (Feb 14, 2023)` / `* Distribution: EndeavourOS (Arch)`
  >
  > `Steam client uses 100% CPU when idle. Doesn't go away after any time period it seems. Steam will continue using 100% CPU until closed or a game is opened. **When a game is running the Steam client's CPU usage drops to a normal level.**` / `Once the game is closed the Steam client CPU usage spikes right back up to 100%.`
  >
  > `OS: EndeavourOS Linux x86_64` / `Kernel: 6.2.6-arch1-1` / `DE: Plasma 5.27.2` / `CPU: AMD Ryzen 5 5500U with Radeon Graphics (12) @ 2.100GHz` / `GPU: AMD ATI 03:00.0 Lucienne` / `GPU Driver: Mesa 22.3.6-1` / `Memory: 8GB`
- **Coverage.** T3: covers a pathological idle case with the machine fully named — object: Steam build 1676336721 on EndeavourOS (Ryzen 5 5500U, kernel 6.2.6, Plasma 5.27.2), unit CPU % (tool not named), statistic "100% CPU when idle", "drops to a normal level" with a game running. T1, T2, T5: does not cover.
- **One observation?** Yes; machine named; build named; states idle and in-game; window "doesn't go away after any time period".

### S3-27 — ValveSoftware/steam-for-linux issue #10619 "Random high CPU+RAM usage / hogging"

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 10619, opened 2024-03-15T09:05:41Z, open, 3 comments.
- **Copy read.** MCP body (excerpt of the body saved), 2026-09-19; `sources/S3-27/steam-for-linux-10619.json`, 2 119 bytes, SHA-256 `41f7b798b8eadcb65ec6db42e93c17c2fca74f0dca62728a03d18f63378f7ca4`.
- **Passages (body).**
  > `* Steam client version (build number or date): 1710281934 Tue, Mar 12 9:14 PM UTC -00:00` / `* Distribution (e.g. Ubuntu): Manjaro/KDE 5.27.10`
  >
  > `When steam is running in the background, regardless of whether it's doing something or not, there is a constant CPU usage of 20-30% (on a 16 core system) and a memory usage of at least 2GB). The problem appears sporadic and at first turning off the client beta appeared to fix it, but since them I've had the problem reoccur twice which has led to me having to shut down steam.`
  >
  > `Again, the laptop is hot to the touch, and steam is using 28-30% of my CPU. I had not opened steam; I will check it, and once again there are no updates happening.`
- **Coverage.** T3: covers a sporadic idle-background case — object: Steam build 1710281934 on Manjaro/KDE, started `-silent -minimized -vgui -nofriendsui`, unit CPU % of the whole 16-thread machine, statistic "20-30%" / "28-30%" sustained (i.e. several cores' worth), no game running. T1, T2, T5: does not cover.
- **One observation?** Yes; machine partly named (16 logical CPUs, laptop, Nvidia); build named; state background idle; window "indeterminate amounts of time".

### S3-28 — Arch Linux forums "High CPU load when running games with steam play" (`ps aux` with `gameoverlayui` and `steamwebhelper --type=renderer` beside a running game)

- **Citation.** bbs.archlinux.org topic 245442, user columbarius, post #1, 2019-04-04 00:01:11 (no replies).
- **Copy read.** `https://bbs.archlinux.org/viewtopic.php?id=245442`, 2026-09-19; `sources/S3-28/archlinux-bbs-245442.html`, 12 169 bytes, SHA-256 `c5f9bd9f44c8b56f5850adcd605c021206a43006b7c16f7e87a8602180e834b4`.
- **Passages (post #1).**
  > `I recently heard from the steam play feature and tried to test it with Age of Empires 2 HD and Ori and the blind forest, both not recommended by steam, but marked as working on protondb,  on my notebook (XPS 13, i7-7500U, HD Graphics 620, 8GB). The games worked, but every time the fan was spinning up and the notebook got very hot, cpu temperatures up to 100°C. Htop showed the game executable spawned two times, with cpu loads at 140% and 100%. Those seemed a bit high for an old game, so I tested it on an desktop pc (i5-6400, GeForce GTX 970 with nvidia driver) with the same setup with corresponding drivers.`
  >
  > `ps aux: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND` / `kodi 9112 0.0 0.7 608884 125872 ? S 01:04 0:00 /home/kodi/.local/share/Steam/ubuntu12_32/steam` / `kodi 9118 6.7 0.0 46480 12332 ? Rs 01:04 0:28 /home/kodi/.local/share/Steam/steamapps/common/Proton 3.16 Beta/dist/bin/wineserver` / `kodi 9203 140 0.9 3057568 161864 ? Rl 01:04 9:56 Z:\home\kodi\.local\share\Steam\steamapps\common\Age2HD\Launcher.exe` / `kodi 9206 0.6 0.3 137700 56764 ? Sl 01:04 0:02 /home/kodi/.local/share/Steam/ubuntu12_32/gameoverlayui -pid 9203 -steampid 7426 -manuallyclearframes 0 -gameid 221380` / `kodi 9208 0.0 0.4 469584 67336 ? Sl 01:04 0:00 /home/kodi/.local/share/Steam/ubuntu12_64/steamwebhelper --type=renderer --no-sandbox --disable-features=AsyncWheelEvents,TouchpadAndWheelScrollLatching --disable-gpu-compositing --service-pipe-token=************************** --enable-blink-features=ResizeObserver,Worklet,AudioWorklet --lang=de --log-file=/home/kodi/.local/share/Steam/logs/cef_log.txt --product-version=Valve Steam Client --webview-urls=http://localhost/*,http://steamloopback.host/*,https://steamloopback.host/*,https://localhost/* --num-raster-threads=2 --enable-main-frame-before-activation --service-request-channel-token=************************** --renderer-client-id=5 --shared-files=v8_context_snapshot_data:100,v8_natives_data:101`
  >
  > (nvidia-smi table) `| 0 7426 G ...di/.local/share/Steam/ubuntu12_32/steam 21MiB |` / `| 0 7433 G ./steamwebhelper 3MiB |` / `| 0 9203 G ...am\steamapps\common\Age2HD\Launcher.exe 26MiB |`
- **[own computation]** From the `ps` line for pid 9206 (`gameoverlayui`): `%CPU 0.6`, `TIME 0:02`, `START 01:04`; the game (pid 9203) shows `TIME 9:56` at `%CPU 140`, so the snapshot is ≈7 minutes after launch (9:56 / 1.40 ≈ 7.1 min). `steamwebhelper --type=renderer` (pid 9208) shows `%CPU 0.0`, `TIME 0:00` over the same interval; the `steam` main process 0.0 % / 0:00 (its own start was earlier — pid 7426 in the nvidia-smi table is the steam process, so 9112 is a second `steam` binary instance). Located, not a value.
- **Coverage.** T3: covers — object: the Steam client tree beside a running Proton game (Age of Empires II HD, Proton 3.16 Beta) on Arch (desktop i5-6400/GTX 970; also an XPS 13 i7-7500U), the process roles `steam`, `gameoverlayui -pid … -steampid … -gameid …`, `steamwebhelper --type=renderer …` (a 2019 CEF renderer command line), `wineserver`, unit `ps` %CPU (lifetime average) and cumulative TIME, statistic one snapshot ≈7 min into play: gameoverlayui 0.6 % / 0:02, steamwebhelper renderer 0.0 % / 0:00, game 140 %. Steam client build not named. T1: covers the CEF renderer's command-line switches as a Linux observation. T2, T5: does not cover.
- **One observation?** Yes; machine named (i5-6400, GTX 970, nvidia 418.56); Steam build not named; state in-game with overlay process alive; window ≈7 min (reader's estimate above).

### S3-29 — ValveSoftware/steam-for-linux issue #12973 (Flatpak `steamwebhelper --type=zygote` command line, 2026)

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 12973 "steamwebhelper crashes after starting a game", opened 2026-03-10T22:15:50Z, open, 1 comment. Process-structure evidence only.
- **Copy read.** MCP body (excerpt saved), 2026-09-19; `sources/S3-29/steam-for-linux-12973.json`, 2 374 bytes, SHA-256 `0d45d3b5def0f8f3d70bae720b6035c579c54c613c6e404e8922f84041b6fe66`.
- **Passage (body, `coredumpctl info`).**
  > `Command Line: /home/sjm/.var/app/com.valvesoftware.Steam/.local/share/Steam/ubuntu12_64/steamwebhelper --type=zygote --no-sandbox --crashpad-handler-pid=281 --enable-crash-reporter=, --change-stack-guard-on-fork=enable --enable-chrome-runtime --user-data-dir=/home/sjm/.var/app/com.valvesoftware.Steam/.local/share/Steam/config/htmlcache $'--user-agent-product=Valve Steam Client' --buildid=1769025840 --steamid=0` / `Control Group: /user.slice/user-1000.slice/user@1000.service/app.slice/app-flatpak-com.valvesoftware.Steam-638719171.scope`
  >
  > `steamwebhelper regularly crashes after I start a game. It seems to "settle down" after a while, but to begin with it'll crash one or more times.` (three SIGTRAP core dumps of `steamwebhelper` within one minute, 2026-03-10 22:03:08 – 22:04:03)
- **Coverage.** T3: covers only structure — the `steamwebhelper --type=zygote … --enable-chrome-runtime --buildid=1769025840` process of the Flatpak client on Fedora 43, and that helper crashes/restarts around game start. No CPU figure. T1: context (CEF "chrome runtime" mode switch). T2, T5: does not cover.
- **One observation?** Yes (one coredump listing); machine partly named (RX 5700, Fedora 43); build 1769025840; state game just started.

### S3-30 — sched-ext/scx issue #234 "[scx_lavd] Getting large pauses and stutters in-game" with the linked `scx_lavd` log (gist)

- **Citation.** GitHub sched-ext/scx issue 234, opened 2024-04-18T22:26:50Z by ChrisLane, closed, 63 comments; and the gist it links, `gist.github.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1` (a `sudo scx_lavd` console log, 424 lines, wall-clock 22:14:16 – 22:21:04).
- **Copies read.** (a) `https://web.archive.org/web/20250221083909id_/https://github.com/sched-ext/scx/issues/234` (memento 2025-02-21 08:39:09), fetched 2026-09-19; `sources/S3-30/wayback-scx-234.html`, 285 959 bytes, SHA-256 `1d6e33dddc9c5c0dd9b63209e1c5a17ea0962f9636f3e59bedd093bc176d74e2` (holds the body and 16 comment bodies of 63; none mentions steamwebhelper, gameoverlayui or CQueuedPacketSe — `grep -c` = 0 for each). (b) `https://gist.githubusercontent.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1/raw`, 2026-09-19; `sources/S3-30/gist-ChrisLane-1945f66b5d8a2f36a530ca9ac8abcfa1-raw.txt`, 118 045 bytes, SHA-256 `05e1a6d1f106a7838dd34980c2f404d2d0b88e7c686c9d58b21e0aedfef41a94`.
- **Passages (issue body).**
  > `I read about scx_lavd on Phoronix and decided to give it a try and get some basic benchmarks.` / `I have observed that I am able to quite reliably reproduce stutters and pauses, sometimes several seconds long while running around my ship in Helldivers 2.` / `Here's the output from `sudo scx_lavd` while I was running the game with several stutters in the period (not sure on exact timestamps:` / `https://gist.github.com/ChrisLane/1945f66b5d8a2f36a530ca9ac8abcfa1`
  >
  > `**System**:` / `Distro: Arch Linux` / `Kernel: 6.8.7-1-cachyos` / `GPU: AMD Radeon RX 6800 XT (RADV NAVI21)` / `CPU: AMD Ryzen 9 5900X 12-Core Processor` / `RAM: 36GB`
- **Passages (gist, `file:line`).**
  - line 1–3: `chris@chrispc% sudo scx_lavd` / `22:14:16 [INFO] scx_lavd scheduler is initialized` / `22:14:16 [INFO] scx_lavd scheduler starts running.`
  - line 4 (table header): > `22:14:17 [INFO] | mseq      | pid      | comm              | cpu  | vtmc | vddln_ns  | elglty_ns | slice_ns   | grdy_rt   | lat_prio | lat_cri | min_lc  | avg_lc  | max_lc  | static_prio  | lat_bst | slice_bst | run_freq  | run_tm_ns | wait_freq | wake_freq | cpu_util | sys_ld |`
  - line 48 (the only `steam` row): > `22:14:59 [INFO] |        43 |     2613 | steam             |   19 |   -1 |         0 |         0 |    3000000 |         0 |       26 |      42 |      40 |      51 |      56 |           20 |       6 |         0 |         4 |      7622 |         4 |         0 |       24 |      9 |`
  - line 134: > `22:16:23 [INFO] |       127 |     2352 | IPC:CSteamEngin   |    9 |   -1 |         0 |         0 |    3000000 |       279 |       25 |      42 |      40 |      48 |      56 |           20 |       5 |         0 |      7975 |     53448 |      9205 |      7719 |       37 |      6 |`
  - line 144: > `22:16:32 [INFO] |       136 |     2240 | Xwayland          |   13 |   -1 |         0 |         0 |    3000000 |       633 |       24 |      43 |      39 |      48 |      56 |           20 |       4 |         0 |     12013 |     33594 |     16394 |     15636 |       38 |      9 |`
  - line 207: > `22:17:33 [INFO] |       197 |    41402 | renderer          |   18 |   -1 |   2460000 |         0 |    3000000 |       226 |       15 |      50 |      38 |      43 |      51 |           17 |      -2 |         0 |         3 | 5736565658 |      1935 |    280469 |        5 |      6 |`
  - line 370: > `22:20:11 [INFO] |       355 |    41276 | explorer.exe      |    5 |   -1 |  11724000 |       868 |    3000000 |      1039 |       22 |      45 |      40 |      48 |      56 |           20 |       2 |         0 |     38233 |      9858 |     31580 |     30654 |       38 |      8 |`
  - last lines: `^C22:21:04 [INFO] |       408 | …` / `EXIT: BPF scheduler unregistered`
- **[own computation]** `python3` over the gist: 408 data rows (one sampled task per second, `mseq` 1–408, 22:14:17–22:21:04). Distinct `comm` counts (top): `sudo` 56, `kworker/u66:52` 38, `kworker/u66:26` 35, `kworker/u65:57` 34, `thread pool wor` 33, `kworker/u66:3` 31, `ad pool !LP wor` 23, `main` 13, `wineserver` 9, `winedevice.exe` 4, `dxvk-queue` 4, `01c0a57c917d2da` 3, `steam` 1, `IPC:CSteamEngin` 1, `renderer` 1, `Xwayland` 1, `explorer.exe` 1. No row names `steamwebhelper`, `gameoverlayui` or `CQueuedPacketSe` (`grep -c` = 0). Command: `rows=[l for l in open('gist_chrislane.txt') if l.count('|')>20 and 'mseq' not in l]; collections.Counter(l.split('|')[3].strip() for l in rows)`. The `steam` row's columns read `run_freq 4`, `wait_freq 4`, `wake_freq 0`, `cpu_util 24` (units are scx_lavd's; the tool's definitions are S2 material, not read here).
- **Coverage.** T3: covers partly — a Linux observation during play (Helldivers 2 via Proton, Ryzen 9 5900X, Arch, kernel 6.8.7-1-cachyos, scx_lavd of April 2024) that samples one task per second with per-task `run_freq`/`wait_freq`/`wake_freq`/`cpu_util` columns; Steam appears as `steam` (once) and `IPC:CSteamEngin` (once); no `steamwebhelper`/`gameoverlayui` row in this log. T5: covers — a public scheduler-side log with per-task frequency columns of a Linux gaming session, fields as in the header above (one sampled task per row, not a full trace). T1, T2: does not cover.
- **One observation?** Yes, one run. Machine: named. Subject: scx_lavd (commit not stated; April 2024), Steam + Helldivers 2 running, stutters present. Window: 22:14:17–22:21:04 (≈6 min 47 s, wall clock in the log).

### S3-31 — sched-ext/scx issue #3739 "[scx_lavd] Repeated system stutter under autopilot." (`perf sched` excerpt with browser threads)

- **Citation.** GitHub sched-ext/scx issue 3739, opened 2026-08-15T10:29:17Z, open, 3 comments.
- **Copy read.** MCP body (excerpt saved), 2026-09-19; `sources/S3-31/scx-3739.json`, 2 059 bytes, SHA-256 `302b6808f61c5fa6fefff08030e128782bf850aee801d33b5e7c10661d068df8`.
- **Passages (body).**
  > `While running `scx_lavd` 1.1.2 in autopilot mode on an Intel Core i7-12700H hybrid CPU, I observed the machine repeated stutter during normal use. I collected several groups of wake-to-switch scheduling delays via perf, ranging from approximately 200 ms to 660 ms.`
  >
  > `One of the captures contains a particularly clear case: two tasks were woken with `target_cpu=014` and did not run for 661.639 ms and 656.828 ms. During that interval, CPU 14 repeatedly scheduled a thread named `data-loop.0` and returned to idle. There were 62 `swapper/14 -> data-loop.0` switch-ins in the 660 ms interval.`
  >
  > `Top rows from perf sched latency` / `Task                         Max delay    Start          End` / `MediaDe~hine #8:560427       661.639 ms   64786.700419   64787.362058` / `kworker/u85:0-i:544390       656.828 ms   64786.705255   64787.362083` / `glean.dispatche:528272         9.618 ms   64787.585305   64787.594923` / `WRScene~der#137:551596         7.417 ms   64783.557922   64783.565338` / `WRScene~rLP#137:551597         7.034 ms   64782.891046   64782.898080` / `kwin_wayland:(3)               2.958 ms   64782.869110   64782.872068`
  >
  > `Kernel: Linux 7.1.8-1-cachyos` / `perf package: perf 7.1.8-1` / `scx package: scx-scheds 1.1.2-1` / `LAVD build ID: 1.1.2 x86_64-unknown-linux-gnu` / `CPU: 12th Gen Intel(R) Core(TM) i7-12700H` / `CPU 14: E-core (one hardware thread, maximum frequency reported as 3.5 GHz)`
- **Coverage.** T5: covers — a public `perf sched latency` excerpt (with `sched_waking`/switch lines in the body) of a Linux desktop session under scx_lavd 1.1.2, machine fully named, fields: task name:pid, max delay, start, end; the delayed tasks are browser threads (`MediaDe~hine`, `WRScene~der`, `glean.dispatche` are Firefox thread-name prefixes as they appear; the reader does not assert the browser's identity beyond the names). Not Chromium, not a comms client; a scheduling pathology, not idle behaviour. T1, T2, T3: does not cover.
- **One observation?** Yes, one capture; machine named; subject the whole desktop (browser not named as a program), state "normal use"; window one ~660 ms interval inside a perf record of unstated length.

### S3-32 — catapult `tracing/test_data/sfgate.json` (Chrome trace-event JSON, pre-2019)

- **Citation.** Chromium catapult repository, `tracing/test_data/sfgate.json`, at HEAD commit `e39ded11ffe971d360160c9d185a7e0ef98fb9a3` (2026-09-18); `tracing/test_data/README.md` at the same commit.
- **Copies read.** `https://chromium.googlesource.com/catapult/+/HEAD/tracing/test_data/sfgate.json?format=TEXT` (base64-decoded), 2026-09-19; `sources/S3-32/catapult-tracing-test_data-sfgate.json`, 8 336 397 bytes, SHA-256 `56fddbeea278ce21eb314206797a81ae6758a8fe1309b5064f8c64f33873410c`. Directory listing `sources/S3-32/catapult-test_data-listing.html`, 20 179 bytes, SHA-256 `2427748f674609563b5b4d8aa29bbc61934b8725906e48868ab06f471096c5c5`. Per-file history is behind sign-in (403), so the trace's own date is not recoverable.
- **Passage (README.md, lines 1–9).**
  > `# Trace Viewer Test Data` / `To view trace files in this folder:` / `* Start the development server.` / `* Open [http://127.0.0.1:8003/tracing_examples/trace_viewer.html](http://127.0.0.1:8003/tracing_examples/trace_viewer.html).` / `* Use the dropdown menu to select and load a trace file.` / `*Note:* These files date from 2019 or earlier and may not reflect current product code.`
- **[own computation]** `python3 -c "import json; d=json.load(open('sfgate.json')); …"`: a dict with one key `traceEvents`, 46 051 events; event keys `{ph, name, cat, pid, tid, ts, tts, dur, tdur, args, id, s}`; metadata events (`ph == 'M'`) name 4 processes — pid 28295 `Browser` (`num_cpus` 32), 28355 `GPU Process` (`num_cpus` 1), 28619 `Renderer` labelled `chrome://tracing`, 28803 `Renderer` labelled `SFGate: San Francisco Bay Area - News,Bay Area news, Sports, Business, Entertainment, Classifieds - SFGate`; thread names include `CrBrowserMain`, `Chrome_IOThread`, `Chrome_FileThread`, `CrRendererMain`, `Compositor`, `CompositorTileWorker1/109`, `CrGpuMain`, `Chrome_ChildIOThread`; categories `blink` 34 059, `blink,benchmark` 8 035, `benchmark` 3 929, `__metadata` 28. No OS, version or scheduling (`sched_switch`) data is present.
- **Coverage.** T5: covers partly — a public Chrome trace-event JSON of one browsing session with a browser, a GPU and two renderer processes (one for the `chrome://tracing` page, one for a news site), fields per event as listed; carries per-thread `tts`/`tdur` (thread CPU time per slice) but **no per-process CPU counters, no scheduler events, no platform or Chrome version**; dated "2019 or earlier". T1: context only (process/thread naming). T2, T3: does not cover.
- **One observation?** One trace; machine: only `num_cpus` 32; subject: Chrome of unknown version and OS, one loaded site plus the tracing page; window not stated in the file (timestamps are in µs relative to an unstated origin).

### S3-33 — catapult `tracing/test_data/tcmalloc_multi_renderer.json` (Chrome/29 trace with `clientInfo`)

- **Citation.** Chromium catapult repository, `tracing/test_data/tcmalloc_multi_renderer.json`, HEAD commit `e39ded11ffe971d360160c9d185a7e0ef98fb9a3`.
- **Copy read.** `…/tcmalloc_multi_renderer.json?format=TEXT` (base64-decoded), 2026-09-19; `sources/S3-33/catapult-tracing-test_data-tcmalloc_multi_renderer.json`, 10 555 630 bytes, SHA-256 `9012ed49c909706b63ebac2308179dbf11c941be270db58499c8267676b497f0`.
- **Passage (`clientInfo` object, verbatim JSON values).**
  > `"command_line": "out/Release/chrome --user-data-dir=/tmp/udd --login-user=stub-user@example.com --login-profile=test-user --flag-switches-begin --flag-switches-end"` / `"version": "Chrome/29.0.1524.0"`
- **[own computation]** top-level keys `traceEvents`, `systemTraceEvents`, `clientInfo`; `systemTraceEvents` is an empty list; 79 263 events over 6 pids and 11 (pid, tid) pairs; the only metadata events are 11 `thread_name` records (no `process_name`), so process roles are not labelled.
- **Coverage.** T5: covers partly — a public Chrome/29.0.1524.0 (2013-era) trace-event file with several processes (six pids) and a `clientInfo` block naming the build's command line (`--login-user`/`--login-profile` switches); `systemTraceEvents` (the slot for ftrace text) is empty, so no scheduling data; OS not stated. T1, T2, T3: does not cover.
- **One observation?** One trace; machine not named; Chrome/29.0.1524.0 named; state unknown; window not stated.

### S3-34 — Perfetto `test/data` Chrome traces (public Perfetto-format traces; all from Android builds)

- **Citation.** Perfetto repository (android.googlesource.com/platform/external/perfetto), `test/data/*.sha256` placeholders at HEAD (listing fetched 2026-09-19), `test/data/chrome/README.md`, `tools/test_data`; binaries served from the GCS bucket `gs://perfetto/test_data` as `<name>-<sha256>`.
- **Copies read.** Listings `sources/S3-34/perfetto-test-data-listing.html` (51 323 bytes, SHA-256 `884108c73c8f8a43cda5f7725eb1c5ba3f773ae8775e372cc6000ba8fa9b41de`), `perfetto-test-data-chrome-listing.html` (13 760 bytes, `f67c7cd9d7966d5319ac3b4be742f80426cf90df2ae09b0542c573fcfa3f3e5a`); `perfetto-test-data-chrome-README.md` (198 bytes, `d7f310ab938f278fa6bb8d34ec26c55dd89c15068e00ec0eae7709b6a27f10a3`); `perfetto-tools-test_data.py` (9 008 bytes, `c3f43e41b65d229a4c9d81dd8902b9b23eb129511495b70a40e6578863e98beb`). Six traces downloaded from `https://storage.googleapis.com/perfetto/test_data/<name>-<sha256>` (HTTP 200) into `sources/S3-34/traces/`; their SHA-256 equal the repository's `.sha256` placeholders: `chrome_rendering_desktop.pftrace` 8 305 513 B `f61971e42ea0ce0f6da71c87a0ab19da0e13deca0fa90c6bdc98782af01ae702`; `chrome_scroll_without_vsync.pftrace` 1 359 814 B `74890239a1042cb93a87b8b5b5d9942f821ed3cc0c1236e7734d45a550e3cde4`; `chrome_input_with_frame_view.pftrace` 6 392 331 B `a93548822e481508c728ccc5da3ad34afcd0aec02ca7a7a4dad84ff340ee5975`; `chrome_page_load_all_categories_not_extended.pftrace.gz` 1 277 750 B `6586e9e2bbc0c996caddb321a0374328654983733e6ffd7f4635ac07db32a493`; `chrome_example_wikipedia.perfetto_trace.gz` 21 537 072 B `7401f67e30cb025b113cef1db53d7e154705e688e33142f65fd7875df26f2cf0`; `cpu_powerups_1.pb` 2 033 064 B `70f5511ba0cd6ce1359e3cadb4d1d9301fb6e26be85158e3384b06f41418d386`.
- **Passages.**
  - `test/data/chrome/README.md` (whole file): > `# Chrome Stdlib Test Data` / `This directory contains the test data for the Chrome Stldib diff tests. This test data is to be rolled from the Chromium repository and should not be modified in Perfetto.`
  - `tools/test_data` line 9: > `File in the GCS bucket are content-indexed as gs://bucket/file_name-a1b2c3f4 .`; line 28: > `BUCKET = 'gs://perfetto/test_data'`; line 212: > `    uri = uri.replace('gs://', 'https://storage.googleapis.com/')`
- **[own computation]** Queried each trace with the `perfetto` Python trace processor (`pip install perfetto`, 2026-09-19), SQL over `metadata`, `trace_bounds`, `process`, `thread`, `sched_slice`, `thread_state`, `counter`, `slice`:
  - `chrome_rendering_desktop.pftrace`: `system_name = Linux`, `system_machine = armv8l`, `system_release = 5.9.0-mainline-android12-0-…`, `android_build_fingerprint = google/oriole/oriole:S/SD1A.210112.001/7076153:userdebug/dev-keys`; 53.9 s; 4 processes (`Browser` 12685, `Renderer` 12743, `GPU Process` 12781, plus pid 0); 47 threads; **sched_slice rows 0**; counter rows 195 191; 111 472 slices.
  - `chrome_scroll_without_vsync.pftrace`: Android 10 (`google/flame`), 5.0 s, 5 processes (two `Browser`, `Renderer`, `GPU Process`), 56 threads, sched_slice 0.
  - `chrome_input_with_frame_view.pftrace`: Android 13 (`google/oriole`), 10.1 s, 5 processes, 14 threads, sched_slice 0.
  - `chrome_page_load_all_categories_not_extended.pftrace.gz`: Android 12 (`google/sunfish`), 75.8 s, 9 processes (`Browser`, two `Renderer`, `GPU Process`, four `Service: data_decoder.mojom.DataDecoderService`), 86 threads, sched_slice 0.
  - `chrome_example_wikipedia.perfetto_trace.gz`: Android 13 (`google/oriole`), 29.2 s, 5 processes, 41 threads, sched_slice 0, 297 603 slices.
  - `cpu_powerups_1.pb`: Android 13 (`google/oriole …:eng/dev-keys`), 1.08 s, 698 processes, 3 724 threads, **sched_slice rows 620**, thread_state 1 279 — a system trace with Chrome threads (`CrRendererMain`, `CrBrowserMain`, `Chrome_IOThread` present) but on an Android device.
  - Despite the name, `chrome_rendering_desktop.pftrace` carries an Android build fingerprint.
- **Coverage.** T5: covers as a *negative* finding with the fields verified — Perfetto's public Chrome traces are Perfetto-proto traces from Android devices (system_name Linux, but Android build fingerprints), with Chrome process/thread naming, counters and slices; the `chrome_*` traces hold **no `sched_slice` rows** (no scheduler data), and none is a desktop Linux session. T1: context only (Chrome process naming `Browser`/`Renderer`/`GPU Process`/`Service: …` in traces). T2, T3: does not cover.
- **One observation?** Six traces, each one Android device run; machines named by build fingerprint; Chrome version not exposed by the queries run; windows 1–76 s.

### S3-35 — ValveSoftware/steam-for-linux issue #6603 "Client uses 100% CPU every seven seconds (spawning lots of processes)"

- **Citation.** GitHub ValveSoftware/steam-for-linux issue 6603, opened 2019-10-20T22:19:04Z, closed, 4 comments.
- **Copy read.** MCP body, 2026-09-19; `sources/S3-35/steam-for-linux-6603.json`, 2 260 bytes, SHA-256 `6c16fed39c769fe9bae130e56d6ddf8d1745521db875ebacdd06d7bdce36637b`.
- **Passages (body).**
  > `* Steam client version (build number or date): latest as of october 19` / `* Distribution (e.g. Ubuntu): Ubuntu 19.10`
  >
  > `The steam client is completely saturating the CPU every seven (7) seconds, even when no windows are on screen. Even when playing a game. This makes the game unplayable since it stutters every seven seconds.` / `- These CPU spikes go away as soon as the Steam client has quit.` / `- Same symptoms on both Ubuntu 19.10 (fresh install) and Xubuntu 19.04`
  >
  > `I later noticed that Steam is creating and terminating at least 7 new processes every seven seconds, coinciding with the CPU spikes and general slowdown. I'll attach a screenshot if it helps.`
- **Coverage.** T3: covers a pathological in-game case — object: Steam client (October 2019) on Ubuntu 19.10 during play, unit CPU saturation events with a period, statistic "every seven (7) seconds", with ~7 processes spawned per period (screenshot not retrievable). A cadence, but of a bug, on an unnamed machine. T1, T2, T5: does not cover.
- **One observation?** Yes; machine not named; build "latest as of october 19"; states background and in-game; window not stated.

### S3-36 — Launchpad bug 2090906 "Chromium 131.0.6778.85 memory leak 17 GB in hours, high CPU usage" (no figure; recorded for completeness)

- **Citation.** Launchpad, Ubuntu chromium-browser bug 2090906, filed 2024-12-03T07:39:55Z, status New, 2 messages.
- **Copies read.** `https://api.launchpad.net/1.0/bugs/2090906` and `…/messages`, 2026-09-19; `sources/S3-36/launchpad-bug-2090906.json` (9 390 bytes, SHA-256 `e7caf928863ae2c14cd8b1be41e65964be3b2861ae6cb8e6676d44b9111e71cf`), `launchpad-bug-2090906-messages.json` (8 546 bytes, `12f1583d4dbafba19eab658dbd8515dfb94d48c28c856fb72ccbf73778fac142`).
- **Passage (description).**
  > `Chromium seems to fill up the available 17-18GB of memory in hours, even if only a few tabs are active. Also the usage of CPU is high.` / `Description:	Ubuntu 24.04.1 LTS` / `Linux tom 6.8.0-49-generic #49-Ubuntu SMP PREEMPT_DYNAMIC Mon Nov  4 02:06:24 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux` / `chromium: /snap/bin/chromium` / `installed:          131.0.6778.85            (3002) 184MB -`
- **Coverage.** T1: names the snap Chromium 131.0.6778.85 on Ubuntu 24.04.1 with "a few tabs" and "high" CPU — **no number**; not a usable observation. T2, T3, T5: does not cover.
- **One observation?** Yes but without a figure; machine not named.

## 3. Not found

- **T1 — a Linux trace or profile of an idle or background renderer giving CPU per wake or wake cadence per tab state.** Not found. The Chromium tracker yields Linux reports with a single per-tab CPU % or a wake-ups-per-second reading in prose (S3-01, S3-02, S3-04, S3-06, S3-07 — the last without an OS), and reports whose evidence is an attachment (traces in S3-04, S3-05; powertop output in S3-03; screenshots in S3-02) that the tracker serves only to signed-in users (`/action/issues/<id>/attachments` 401; comment endpoints 404/405 — log rows 16, 23). The only PowerTOP table quoted in text is the 2009 chromium-dev mail (S3-08, context). Searches that established it: log rows 9, 15–24, 35, 41–43, 50–52.
- **T2 — Slack on Linux.** No Linux observation with a figure found: GitHub semantic search over all repositories and the flathub com.slack.Slack tracker returned nothing (rows 34, 36); the web result (HN 16436815, row 48) names no platform. **Discord, Zoom, Element, Teams**: only CPU-% readings and one powertop watt comparison (S3-10 – S3-20); nothing gives wake cadence, CPU per wake or an under-traffic (message-rate) measurement; Discord's own tracker (support.discord.com) is 403 through the proxy (row 1, 10). Element's Electron client on Linux has only S3-16 (nightly, pathological) and S3-17 (rank without a number); S3-15 is the web client in Firefox.
- **T3 — an scx_lavd sample table under a running game listing `steamwebhelper`, `gameoverlayui` or `CQueuedPacketSe`.** ***Superseded in part on 2026-09-20 — §4.2: the attachments of #234 were fetched once github.com answered, and one of them, `scx_lavd-12-05-2024.log` in comment 60, is such a table — it names `steamwebhelper`, `steam`, `SteamNetworking` and `IPC:CSteamEngin` with the scheduler's per-task columns, one sampled row each for the first three. `gameoverlayui` and `CQueuedPacketSe` still appear in no file. Everything else in this bullet stands as written.*** Not found as of 2026-09-19: the scx repository at commit 0b6f009f holds none of the three strings (row 3); GitHub semantic search of sched-ext/scx and of all repositories for those names returned nothing (rows 2, 4, 13, 38, 39); the one `scx_lavd` log reachable (S3-30 gist) samples 408 tasks and names only `steam` and `IPC:CSteamEngin` from the client; Wayback captures of scx #296/#376/#2491 hold no comment bodies or are absent (row 28); the `dump.txt` attachments in #234 are on github.com (403). GitHub code search finds `CQueuedPacketSe` only as Source-engine source (row 37). Steam-client CPU during play exists only as prose readings (S3-23, S3-25 comment 6, S3-28 `ps` snapshot, S3-35), none with wake counts.
- **T5 — a public per-process CPU or scheduling trace of a Linux desktop browsing session with several renderers, of an Electron/CEF client at idle, or of a conferencing client.** Not found. Perfetto's public Chrome traces are Android-device traces without `sched_slice` rows (S3-34); catapult's Chrome traces are pre-2019 trace-event JSON without OS, version or scheduler data (S3-32, S3-33); Zenodo, Discourse forums, StackExchange and Launchpad searches returned nothing (rows 41–45, 52); openbenchmarking.org and phoronix.com are 403 through the proxy (row 1), so browser-benchmark databases could not be checked for per-process CPU fields. The nearest items are the scx_lavd sampled-task log (S3-30) and a `perf sched latency` excerpt of a desktop with browser threads (S3-31), neither a browsing-session trace.

## 4. Amendment — GitHub retrieval retry, 2026-09-20

Added by 인지오 on 2026-09-20 from the development machine. Sections 1–3 are the S3 reader's record of 2026-09-19 and stand as written, apart from the clause marked in §3. The reader's box answered 403 on github.com issue pages, api.github.com and github.com/user-attachments, so issue comments were reachable only through Internet Archive captures and file attachments not at all (header note; §1 row 1). From the development machine all three answer normally. Threads read with `gh issue view <n> --repo <repo> --json title,body,comments` (GitHub CLI, account `retz8`); attachments with `curl -sS -L`, HTTP 200 each. Copies under `sources/A-2026-09-20/` (gitignored).

### 4.1 The four threads read in full

| Thread | What the reader had | Now | Change |
|---|---|---|---|
| `element-hq/element-web` #32107 (S3-16) | issue body through the GitHub MCP search endpoint; no comment bodies | body + 14 comments, SHA-256 `b2837e5bc660a00316dacfaf67991b259a6e8b364242102fb0aed98888550dd1` | None. The 60–70 % idle CPU reading is in the issue body, which the reader had; the comments carry cause discussion (a Rust crypto library migration, clearing the cache) and no figure |
| `element-hq/element-web` #32167 (S3-17) | as above | body + 9 comments, SHA-256 `6f5a19cccb077058e96d96df0c5debf63f364487f2b361b8e7314a208b9197f9` | None. The rank without a number — element-desktop "the 3rd CPU-cycle hungriest app" after gnome-shell — is in the body; the comments add no figure |
| `ValveSoftware/steam-for-linux` #8258 (S3-25) | Wayback capture 20260419042556, bodies decoded from the page's React payload | body + 63 comments, SHA-256 `25bd79bbe4a914235c405e641615514ab0e7e91e89f071ef2b6e7beb6590ed15` | None. Every figure S3-25 records is present and unchanged: ≈ 25 % of one core minimised, "130–150 % in total, one process 70–80 %", "37.5 % of my 4 threads" while playing, 10–40 % on a 12-core Ryzen, ≈ 0–1 % with `-no-browser`. The reader's decode was complete |
| `sched-ext/scx` #234 (S3-30) | Wayback capture 20250221083909: body + 16 of 63 comment bodies; the attachments 403 | body + 63 comments, SHA-256 `add3368e427b7921e3f11e6a049b14cf502eaae1079aa36d8dcd92f4996e399d`, + 6 attachments | **Changed — §4.2.** The 63 comment bodies confirm the reader's grep over 16: `steamwebhelper`, `gameoverlayui`, `CQueuedPacketSe` and the bare string `steam` occur in none of them. The attachments are a different matter |

### 4.2 S3-30 amended — the attachments of `sched-ext/scx` issue #234

Six attachments linked from the thread were fetched on 2026-09-20, all HTTP 200, all under `sources/A-2026-09-20/`:

| Comment | URL | Bytes | SHA-256 | What it is |
|---|---|---|---|---|
| 3 | `github.com/sched-ext/scx/files/15046314/scx_lavd_dump-2024-04-20-1.txt` | 5 616 | `2f0167c7ad1ca64e2e5adce4bf3b55fd4e7d1ef18ef3767cedb7b0b846593a34` | Watchdog exit dump (runnable task stall), no sampled-task table |
| 5 | `…/files/15098588/dump.txt` | 2 760 | `35cd5c91a75b0f970762dc64b78f043e2fe2178c095caca110bf16336f958f3b` | Watchdog exit dump, no sampled-task table |
| 6 | `…/files/15098674/dump.txt` | 342 390 | `4c6523bd596df3144e3c666e47644bf911d41221f61e32be111d45d1e982800d` | 1 092 sampled rows, 52 distinct comms, a different game (`LikeADragon8.ex`); no Steam-side comm |
| 19 | `…/files/15123361/dump.txt` | 2 794 | `80908a82f6e2afbf459777e6845d2a2921ee336b2e59e27e039fae0744fb4bb2` | Watchdog exit dump, no sampled-task table |
| 50 | `…/files/15180709/scx_lavd-01-05-2024.log` | 40 268 | `ae8cac443583f86da9b87bd662db9a4fb33887d7bb437ddce5c432ac218aa14a` | 132 sampled rows, 22 distinct comms, `r5apex.exe` running; no Steam-side comm |
| 60 | `…/files/15287842/scx_lavd-12-05-2024.log` | 142 628 | `caa86ecbd8137e1601adf153657d7b72f9f19b00a964d1984f53280e9220ee41` | **484 sampled rows, 46 distinct comms, `r5apex.exe` running, and four Steam-side comms** |

**The one that carries Steam-side rows.** `scx_lavd-12-05-2024.log`, posted by GitHub user DasLeo in comment 60 of `sched-ext/scx` issue #234 ("[scx_lavd] Getting large pauses and stutters in-game"), fetched 2026-09-20 from `https://github.com/sched-ext/scx/files/15287842/scx_lavd-12-05-2024.log`. 502 lines, timestamps 12:28:26 to 12:30:27 — about two minutes. The scheduler is `scx_lavd`, an out-of-tree sched_ext scheduler, not the stock kernel scheduler. The session shows Apex Legends (`r5apex.exe`, 97 of 484 sampled rows) running through Wine/Proton (`wineserver` 32 rows) on an X11 KDE desktop (`Xorg`, `plasmashell`), with the Steam client present.

**Passages.** Column header, line 3:

```
| mseq      | pid      | comm              | cpu  | vtmc | vddln_ns  | elglty_ns | slice_ns   | grdy_rt   | lat_prio | avg_lc  | static_prio  | lat_bst | slice_bst | run_freq  | run_tm_ns | wait_freq | wake_freq | perf_cri | avg_pc   | cpu_util | sys_ld |
```

Every Steam-side row in the file — seven of 484 sampled rows (ANSI colour codes and the `[INFO]` prefix stripped; line numbers of the file as fetched):

```
L31:  |  28 | 1603 | IPC:CSteamEngin |  2 |  2 |  60925830 |  472 | 1000000 | 1289 | 21 | 44 | 20 |  1 | 0 |  6361 | 28642 |  11420 |  11267 | 37 | 45 | 88 | 130 |
L170: | 162 | 1453 | steam           |  2 |  3 |  68292300 |    0 | 1458176 |  886 | 22 | 47 | 20 |  2 | 0 |  2908 | 79570 |    999 | 114319 | 49 | 47 | 89 | 116 |
L203: | 194 | 1603 | IPC:CSteamEngin |  2 | -1 |  47766600 | 1086 | 1000000 | 1941 | 21 | 47 | 20 |  1 | 0 |  4215 | 34390 |   6831 |  16565 | 37 | 47 | 87 | 102 |
L213: | 204 | 1603 | IPC:CSteamEngin |  0 | -1 |  58620000 |  534 | 1000000 | 1074 | 22 | 47 | 20 |  2 | 0 |  4261 | 32043 |   8498 |  33629 | 39 | 47 | 94 |  67 |
L254: | 244 | 1737 | steamwebhelper  |  2 | -1 | 1324140000 | 3906 | 1000000 | 1234 | 36 | 47 | 36 |  0 | 0 |    56 | 73460 |     58 |  88254 | 41 | 47 | 84 |  53 |
L289: | 278 | 39611 | SteamNetworking |  1 | -1 |   4020000 |    0 | 9023360 |  517 | 10 | 48 | 13 | -3 | 0 | 93783 |  3566 | 104624 |  87632 | 46 | 47 | 86 |  55 |
L472: | 455 | 1603 | IPC:CSteamEngin |  3 |  3 |  73005000 |  510 | 1000000 | 1821 | 23 | 47 | 20 |  3 | 0 |  8820 | 27651 |  17167 |  14046 | 38 | 47 | 92 |  73 |
```

**Coverage.** T3: this is the artifact §3's T3 bullet declared not found — an `scx_lavd` sampled-task table taken while a Steam-launched game runs, naming `steamwebhelper`. It names `steamwebhelper` (pid 1737), the client process `steam` (pid 1453), `SteamNetworking` (pid 39611) and `IPC:CSteamEngin` (pid 1603), each with the scheduler's per-task columns including `run_freq`, `run_tm_ns`, `wait_freq` and `wake_freq`. `gameoverlayui` and `CQueuedPacketSe` still appear in no file. T1, T2, T5: does not cover.

**What it does not establish, as it stands.**

- **One sample each.** `steamwebhelper`, `steam` and `SteamNetworking` appear once apiece; `IPC:CSteamEngin` four times. Seven rows of 484 over about two minutes, one machine, one session.
- **The columns' semantics are unverified.** `run_freq`, `run_tm_ns`, `wait_freq` and `wake_freq` are `scx_lavd`'s own per-task quantities and the log defines none of them. What each counts, over what window, and whether `run_tm_ns` is an average or a last value must be read out of `scx_lavd`'s source at a pinned commit before any number here is used.
- **Which rows the scheduler prints, and when, is unverified** — whether a row appears per scheduling decision, per interval, or on some other rule decides whether "one row" means the process was scheduled once or merely sampled once. This also decides whether seven rows of 484 says anything about how often the Steam processes run.
- **Not the stock scheduler.** The numbers are what these processes did under `scx_lavd`, not under the kernel's own scheduler.

The record is preserved here as a candidate. Whether it grounds anything for the Steam client binding is a stage-3 decision, and it cannot be taken further without the two verifications above.

### 4.3 Effect on §3

The T3 bullet is amended in place. The other three bullets stand: nothing retrieved on 2026-09-20 bears on T1, T2 or T5, and the venues that block those (the Chromium tracker's attachments and comment endpoints, openbenchmarking.org, phoronix.com) were not retried.
