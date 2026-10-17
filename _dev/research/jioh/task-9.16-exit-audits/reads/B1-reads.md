# Blind reader B1 — Phase 1 reads (source groups 1–15 of the dataset blind-topics file)

Reader B1, task 9.16 (the Phase 9 exit audits), blind re-read of the claim audit. Scope: the first fifteen `##` source groups of `_dev/research/jioh/task-9.16-exit-audits/claims/dataset-blind-topics.md` (Min 2024 through Roeser et al. 2024). Written before opening `dataset-inventory.md` or any repository location of the claims; no repository description of any claim was read. Access date for every copy: 2026-10-17. Local copies live under `/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad/blind/` (abbreviated `$B/` below; it is that absolute path). Hashes are sha256 of the local copy.

Conventions: "passage" blocks are verbatim (PDF text extraction, whitespace normalised; line breaks inside a passage are the source's). "Reading" is B1's own one-to-three-sentence interpretation. "Not in source" means B1 looked for it in the copy named and did not find it.

---

## 1. Min, C. (2024). "Optimizing Scheduler for Linux Gaming." Open Source Summit North America 2024 (topics D-F1-01 … D-F1-20, D-F1-09)

### Copies read
- Slide deck: `https://static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf`, PDF 1.4, 30 pages, producer "Google" (Google Slides export), local `$B/lavd/scx-lavd-oss-na24.pdf`, sha256 `e62d69cd401021f8bfedadde2c4de62b01383facaa83acce7d218af3b6402475`. Slides 11, 12, 13, 14, 15, 16, 29 and 30 were also rendered to PNG and read as images (charts and graphs carry text not in the PDF text layer).
- Session page: `https://ossna2024.sched.com/event/1aBOT/optimizing-scheduler-for-linux-gaming-changwoo-min-igalia`, local `$B/lavd/sched/event.html`, sha256 `6a321cff51138e550c4dec56aa851ed1aea542d0080d57b978073491a391ac8c` (city taken from the same site's header text, `$B/lavd/sched/search.html`).
- scx_lavd source at sched-ext/scx tag `v1.1.3`, commit `c8728c6b6a3fde451f0f10b95f99aad7a32a750a` (2026-08-19), shallow clone `$B/scx/` (files cited individually below).
- Wine source, tag `wine-11.20` (gitlab.winehq.org), `dlls/ntdll/unix/thread.c` local `$B/wine/thread.c` sha256 `c95a38708337dc2d95207533b6ba5a182f80670317b5fbb2d5ed66a4f9405ad2`; `dlls/ntdll/unix/env.c` local `$B/wine/env.c` sha256 `eac82bd2769b1622dd2d308169f9e1750c41169640656e832eb1f8992248396f`. (The topic names no Wine version; wine-11.20 is the newest tag on 2026-10-17.)

### D-F1-01 — title, speaker, event, city, date, slide count
- Slide 1: "Optimizing Scheduler for Linux Gaming / Changwoo Min / changwoo@igalia.com / April 17, 2024".
- Session page: "Optimizing Scheduler for Linux Gaming - Changwoo Min, Igalia / Wednesday April 17, 2024 2:55pm - 3:35pm PDT / 345-346 (Level 3)"; page title "Open Source Summit North America 2024: …"; site header "Seattle, WA, USA".
- pdfinfo: "Pages: 30". Slide 30 is "Join us!" with the Igalia logo.
- Reading: talk "Optimizing Scheduler for Linux Gaming", Changwoo Min (Igalia), Open Source Summit North America 2024, Seattle, 2024-04-17; the deck has 30 slides (the city is on the event site, not in the deck).

### D-F1-02 — number of tasks scheduled while a game runs; system tasks included?
- Slide 12: "● Around 300 tasks are scheduled while running a game."
- Slide 12: "○ Around half of them are system tasks -- especially, wine, graphics, and audio servers, taking 30--40% of scheduling." (the "them" refers to the top 30–40 tasks).
- Reading: about 300 tasks. The slide does not say explicitly whether the 300 includes system tasks; the same slide counts system tasks (wine, graphics, audio servers) among the top 30–40 scheduled tasks, so the count is of all tasks scheduled while the game runs, not only game threads — B1's inference, not a stated sentence.

### D-F1-03 — share called long-lived
- Slide 12: "○ Around 90% are long-living tasks; only 10% of tasks are terminated."
- Reading: about 90% long-living ("long-living" is the slide's word); 10% terminate.

### D-F1-04 — concentration of scheduling activity
- Slide 12: "● Top 30-40 most frequently scheduled tasks take 95% of scheduling. ○ Around half of them are system tasks -- especially, wine, graphics, and audio servers, taking 30--40% of scheduling. ○ There are 15-20 game-specific tasks, which takes 60-70% scheduling."
- Reading: top 30–40 tasks = 95% of scheduling; about half system tasks (30–40% of scheduling), 15–20 game-specific tasks (60–70%). Tasks outside the top group are not described beyond the implied remaining 5%.

### D-F1-06 — per-schedule runtimes, named examples
- Slide 13: "● In general, tasks run for very short duration – roughly a few 100s usec on average to a few msec maximum."
- Slide 13: "○ Some coordination tasks run very shortly (e.g., wineserver:260 usec) but some work tasks (e.g., a task worker: 1.65 msec) run longer than average."
- Slide 13 chart caption: "Distribution of task's runtime average per schedule in a game", y-axis "runtime avg (msec)", shaded band labelled "< 1 msec".
- Reading: average a few hundred µs, maximum a few ms; examples wineserver 260 µs and "a task worker" 1.65 ms.

### D-F1-08 — stability / predictability of execution time
- Slide 13: "● Task execution time is very stable and is predictable using its average."
- (Related, slide 15: "Wait time from one schedule to another schedule is a task's behavioral property. Each task's wait time is pretty constant.")
- Reading: per-task execution time stated as very stable and predictable from its average.

### D-F1-10 — what initiates scheduling; pie chart's preemption share
- Slide 14: "● Preemption (e.g., timer interrupt) takes only 25-30% of scheduling."
- Slide 14: "● 70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait, etc."
- Slide 14: "● In this case, a task is first scheduled out waiting for an event then it is scheduled in when the event is notified."
- Slide 14 pie chart ("Call stacks which triggered scheduling in a game"), labels read from the image: "sched_preempt (28.78%)", "ioctl (13.25%)", "alloc (7.95%)", "unlock (7.28%)", "syscall (6.76%)", "futex_wait (5.94%)", "fs_write (4.11%)", "lock (3.96%)", "fs_read (3.83%)", "pipe_write (3.69%)", "pipe_read (2.96%)", "futex_wake (2.23%)", "page_fault (1.57%)", "recvmsg (1.36%)", "poll (1.26%)", "futex (1.05%)", smaller unreadable slices.
- Reading: preemption 25–30% (pie: sched_preempt 28.78%); waiting system calls 70–75%.

### D-F1-12 — targeted latency / time-slice example (deck; scx_lavd source comments at v1.1.3)
- Slide 27 ("Task's time slice"): "● The LAVD scheduler tries to schedule all runnable tasks at least once within a predefined time window, which is called a targeted latency (e.g., 15 msec). ● The scheduler proportionally divides the targeted latency as per task's nice priority (i.e., weight)."
- `scheds/rust/scx_lavd/src/bpf/main.bpf.c` lines 68–74 (v1.1.3): "We borrow the time slice calculation idea from the CFS and scx_rustland schedulers. The LAVD scheduler tries to schedule all the runnable tasks at least once within a predefined time window, which is called a targeted latency. For example, if a targeted latency is 15 msec and 10 tasks are runnable, the scheduler equally divides 15 msec of CPU time into 10 tasks. Of course, the scheduler will consider the task's priority -- a task with higher priority (lower nice value) will receive a longer time slice."
- `scheds/rust/scx_lavd/src/bpf/lavd.bpf.h` lines 73–75 (v1.1.3): "LAVD_TARGETED_LATENCY_NS = (10ULL * NSEC_PER_MSEC)," / "LAVD_SLICE_MIN_NS_DFL = (500ULL * NSEC_PER_USEC), /* min time slice */" / "LAVD_SLICE_MAX_NS_DFL = (5ULL * NSEC_PER_MSEC), /* max time slice */".
- Reading: the deck gives a targeted-latency example of 15 ms on slide 27 (no per-task slice value). The v1.1.3 source comment gives the example "15 msec … 10 tasks", i.e. an implied 1.5 ms per task, without stating 1.5 ms. The v1.1.3 code constant is 10 ms targeted latency, slice bounds 0.5–5 ms.

### D-F1-13 — waiter–waker graph on slide 16: names
- Slide 16 title "Tasks are tightly linked in a graph", bullet "● Task graphs of top 50 percentile of waiter-wakers". Node labels read from the image: "swapper[0/0]", "Task worker thr[7826/7781]", "Task worker thr[7828/7781]", "Task worker thr[7827/7781]", "Task worker thr[7825/7781]", "SteamControlle[4908/4788]" (left edge cut), "winedevice.exe[7284/7273]", "dxvk-cs[7922/7781]", "dxvk-submit[7920/7781]", "winepulse_mainl[7991/7781]", "pipewire-pulse[1707/1703]", "winepulse_timer[7993/7781]", "pipewire-pulse[1703/0]", "pipewire[1214/1204]", "FAudio_AudioCli[7992/7781]". Edge labels are wait kinds with counts (sleep, futex_wait, poll, epoll).
- Reading: thread/process names: swapper, Task worker thr, SteamControlle(r), winedevice.exe, dxvk-cs, dxvk-submit, winepulse_mainl, winepulse_timer, FAudio_AudioCli, pipewire-pulse, pipewire.

### D-F1-14 — node counts per name; the game executable's name; Wine's naming of unnamed threads
- Slide 16 counts (B1's count of the labels above): "Task worker thr" 4; "pipewire-pulse" 2 (two different tids, 1707 and 1703); every other name 1. No node carries a game-executable name (no `*.exe` name for the game; the only `.exe` label is winedevice.exe, a separate process 7273). The game process (tgid 7781) appears only through named threads.
- Wine `dlls/ntdll/unix/env.c` lines 481–503: "* set_process_name * * Change the process name in the ps output. */ static void set_process_name( const char *name ) { … if ((p = strrchr( name, '\\' ))) name = p + 1; if ((p = strrchr( name, '/' ))) name = p + 1; … prctl( PR_SET_NAME, name ); …}", called from `rebuild_argv` and `prepend_argv` with `main_argv[0]`.
- Wine `dlls/ntdll/unix/thread.c` lines 2057–2091 (`set_native_thread_name`): on Linux it writes the converted name to "/proc/%u/task/%u/comm"; it is reached only from `NtSetInformationThread` cases `ThreadNameInformation` and `ThreadWineNativeThreadName` (lines 2620–2658).
- Reading: Wine sets the process's (calling thread's) comm to the executable's base name via `prctl(PR_SET_NAME)` and renames a thread only when the program sets a thread name. Wine has no code that names an unnamed thread; such a thread keeps the comm it inherits at creation. That inheritance is kernel behaviour, which B1 did not read in a source here, so the passages show only that Wine itself assigns no name.

### D-F1-16 — task chains; periodicity
- Slide 17 ("Summary of game workloads characteristics"): "● Majority of game tasks shows periodic behavior ○ given the fact that a task has a stable execution time and a stable wait time. ● A sequence of tasks serves for a single job (e.g., from a user input to display update). ● Therefore, the accumulated scheduling delay in a task chain will affect end-user's experience; it would eventually result in a sudden spike of frame time (low 1% FPS)."
- Reading: majority of game tasks periodic (inferred from stable execution and wait time); a sequence of tasks serves one job, from user input to display update.

### D-F1-17 — frame period / frame budget; name of latency figures
- No slide states a frame period or frame budget. Slide 8: "In games, FPS (frame per second) or frame time are the widely used metric ○ Average FPS ≈ throughput of FPS ○ Low 1% FPS ≈ 99p latency of FPS ○ Low 0.1% FPS ≈ 99.9p latency of FPS". Slide 7: "Latency: time to process a task"; "Tail latency (99p, 99.9p): latency of the worst 1% or 0.1%". Slide 27: "targeted latency (e.g., 15 msec)". Slide 29's screenshots show in-game benchmark panels with "Refresh Rate: 60" and an overlay "16.5ms … min: 5.5ms, max: 43.4ms" (frame-time overlay, unlabelled in the slide text).
- Reading: no frame budget stated; the only millisecond latency figure in the slide text is the 15 ms "targeted latency", a scheduler time window, not a frame budget.

### D-F1-18 — how traces were obtained; game and machine named?
- Slide 10: "● We collect and analyze all scheduling activities while playing games." Slide 11 title "Analyzed a lot of scheduling traces" (images of analysis reports). Slide 4 describes Steam Deck hardware ("AMD Van Gogh: x86 8-core CPU + AMD GPU") in general. Slides 13 and 14 captions say "in a game".
- Reading: the deck says scheduling activity was collected while playing games; it names neither the game(s) traced nor the machine used for the traces (Steam Deck is the context of the talk, but no slide says the traces were taken on one). Slide 29's benchmark screenshots show 1280 × 800 resolution, also unattributed.

### D-F1-19 — tool named for collecting traces (2024 deck)
- No slide names a tracing tool (no perf, ftrace, bpftrace, Perfetto or VaporMark in the text layer or in the rendered image slides 11, 13–16).
- Reading: the 2024 deck names no collection tool. (Edge's LWN report of the 2025 session, group 4 below, names "VaporMark" built on "perf sched record" — a different, later source.)

### D-F1-20 — distinct process trees in the figures; which trace feeds slides 12–14
- Process ids (the number after "/" in "name[tid/tgid]") visible in figures: slide 11 — game threads under 6340 ("redDispatcher1…7[63xx/6340]", "wine_xinput_hid[6597/6340]"), "wineserver[5789/0]"; slide 15 — "wineserver[3845/0]", "Umask: 0022[4856/4727]", "dxvk-cs[4876/4727]", "CrBrowserMain[4336/4221]"; slide 16 — game threads under 7781, plus 4788, 7273, 1703, 1204, 0.
- Reading: the game-process trees differ across figures — 6340 (slide 11), 4727 (slide 15), 7781 (slide 16) — so the figures draw on at least three distinct game process trees (traces). Slides 12–14 carry no process ids and no text names the trace(s) behind their numbers.

### D-F1-09 — slide 13 runtime plot
- Image read: x-axis "tasks", ticks 0–120, curve ends near x ≈ 127 (about 128 tasks ordered by runtime average); y-axis "runtime avg (msec)", ticks 0.0–1.4. Curve: ≈ 0.01–0.02 ms at the low end (x = 0), ≈ 0.04 ms around x = 60 (middle), ≈ 0.1 ms at x = 100, rising steeply after x ≈ 120 to ≈ 1.38 ms at the last task. The shaded band "< 1 msec" covers all but the last two or three tasks.
- Reading: about 128 tasks, sorted ascending; axis ranges 0–~128 tasks and 0–1.4 ms; low end ~10–20 µs, middle ~40 µs. Values are read off a raster image (precision ±0.01 ms). The text's "task worker: 1.65 msec" exceeds the plot's maximum (~1.38 ms), so the plot is not the source of that example, or is a different game.

---

## 2. Valve, Steam Support FAQs 4F9E-6328-E9B8-47F9 and 71AB-698D-57EB-178C (topics D-F1-26, -27, -28)

### Copies read
- `https://help.steampowered.com/en/faqs/view/4F9E-6328-E9B8-47F9`, local `$B/steam/4F9E-6328-E9B8-47F9.html`, sha256 `7688b171284dd942910c6edc0a451433954df6f854784ef85c36204f86ff3256`; FAQ JSON in the page: `version: 3`, `timestamp: 1625946595` (2021-07-10 UTC).
- `https://help.steampowered.com/en/faqs/view/71AB-698D-57EB-178C`, local `$B/steam/71AB-698D-57EB-178C.html`, sha256 `839cbcaab2bcc9ab7d883e6eabc2cfe13a202f0bccd42273867f45143c700862`; `version: 4`, `timestamp: 1727216103` (2024-09-24 UTC).

### D-F1-26 — the client setting; where; default behaviour
- 4F9E: "Why do downloads in Steam stop when I begin playing a game? Steam automatically pauses your downloads when a game is launched in order to prioritize the network activity for the game itself. You can turn this feature off by navigating to your download settings: Steam > Settings > Downloads. From here, check the Allow Downloads During Gameplay box."
- Reading: setting "Allow Downloads During Gameplay" under Steam > Settings > Downloads; by default Steam pauses downloads when a game launches (to prioritise the game's network activity).

### D-F1-27 — per-game setting
- 71AB, section "Customizing settings per game": "There's also a per-game setting to allow/prevent the downloading of other updates while you're playing."
- 4F9E mentions no per-game setting.
- Reading: only 71AB mentions it; it allows or prevents downloading other updates while that game is played.

### D-F1-28 — how updates enter the queue
- 71AB: "Steam will automatically download updates for your games based on the Steam client's download settings." and "Games are automatically put into your download queue when a game releases an update." Also "Scheduling automatic updates … check the Only auto-update games box and specify the time … Launching the game will also force the game to update immediately".
- Reading: an update release puts the game into the download queue automatically; download timing follows client settings (optionally restricted to a time window).

---

## 3. rlach, ValveSoftware/steam-for-linux issue #8821 (topic D-F1-29)

### Copy read
- GitHub REST API `repos/ValveSoftware/steam-for-linux/issues/8821` and `/comments`, local `$B/gh8821/issue.json` sha256 `ccb01df53f0e23eb69d4d0fd683e627fd2c1a3a2bd0c2dd8f606d6463c17317a`, `$B/gh8821/comments.json` sha256 `a3ac0c315033d9b2733626792253dc08ada25f7253d6f95db0d8275f09e8cfa7`. Issue title "If "Allow downloads during gameplay" is off don't start the download automatically when a game is running", author rlach, created 2022-09-30T11:55:01Z, state open, labels Feature Request, Steam client.

### D-F1-29
- Issue body: "When "Allow downloads during gameplay" is turned off Steam Deck won't download scheduled games and also will pause download when you launch game. But if you have a game launched and during gameplay press "Install" for another game that game will start downloading immediately."
- First comment, kisak-valve (author_association MEMBER), 2022-09-30T12:57:41Z: "Hello @rlach, this is not specific to SteamOS or the Steam Deck. Personally, I don't think that this behavior should be changed. You explicitly told Steam to start installing a game while playing, and it's doing exactly what you told it to do. This can be useful in general when you want to cherry pick a game update or play a game with what resources are available while waiting on a long download."
- Reading: with the setting off, a download the user starts during play (pressing Install) starts immediately; scheduled downloads wait and running downloads pause at launch. Valve's triager said the behaviour is not SteamOS-specific and, personally, should not change, since the user explicitly asked.

---

## 4. Valve SteamOS 3.8 release note; sched-ext/scx v1.1.3; Edge, LWN 1051430 (topics D-F1-30, -31, -32, -34)

### Copies read
- Steam News API `https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1675200&count=100&maxlength=0&feeds=steam_community_announcements`, local `$B/steamos/news.json` sha256 `6d01f838120caed337ccebb80a7e4ec23c614e2a168971d2bce7eb1c9a1cfff5`; item gid `1835871199302299`, title "SteamOS 3.8", date 2026-06-18 00:07:43 UTC, feed "Community Announcements"; body extracted to `$B/steamos/steamos38.txt` sha256 `666003afcfaf8dfd9bd1b34939d10b1a2521f49feeb83bbf068506e30986707d`.
- scx v1.1.3 as in group 1 (`$B/scx/`, commit `c8728c6b…`).
- `https://lwn.net/Articles/1051430/` "Lessons from creating a gaming-oriented scheduler", Jake Edge, January 7, 2026, local `$B/lwn/1051430.html` sha256 `1657a8fba33a51e6919b7c2145949423830b639a33608d2e105f388af6512bd3`.

### D-F1-30 — release note on LAVD
- Body opens "SteamOS 3.8.10 has just been released for all users with the following changes: These notes contain all changes since the previous SteamOS 3.7 stable release." Under "Developer": "Initial support for LAVD CPU scheduler via `steamosctl set-cpu-scheduler lavd`". Same section: "Updated Linux kernel to 6.16".
- Reading: LAVD is turned on with the `steamosctl set-cpu-scheduler lavd` command; the note calls it "initial support" in the Developer list and does not say it is the default (nothing says default).

### D-F1-31 — Valve's role (copyright lines; Edge)
- scx_lavd copyright lines at v1.1.3 (all files in `scheds/rust/scx_lavd/src/`): e.g. `src/bpf/main.bpf.c` line 180–181 "Copyright (c) 2023, 2024 Valve Corporation. / Author: Changwoo Min <changwoo@igalia.com>"; `src/main.rs` line 3 "Copyright (c) 2024 Valve Corporation."; `src/bpf/lat_cri.bpf.c` "Copyright (c) 2023-2025 Valve Corporation."; `src/bpf/power.bpf.h` "Copyright (c) 2026 Valve Corporation."; one file `src/bpf_streams.rs` "Copyright (c) 2026 Meta Platforms".
- Edge: "Min said that he has been developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck." The article contains no occurrence of "Valve".
- Reading: Valve Corporation holds the copyright of scx_lavd's files (one file Meta), with Min (Igalia) as author; Edge reports Min develops LAVD as part of his Igalia work on SteamOS and the Steam Deck, without naming Valve.

### D-F1-32 — README at v1.1.3: designed for what, which problem
- `scheds/rust/scx_lavd/README.md` lines 20–23: "`scx_lavd` is initially motivated by gaming workloads. It aims to improve interactivity and reduce stuttering while playing games on Linux. Hence, this scheduler's typical use case involves highly interactive applications, such as gaming, which requires high throughput and low tail latencies."
- README lines 27–31: "Yes, `scx_lavd` should be performant across various CPU architectures. … It mainly targets single CCX / single-socket systems."
- Reading: initially motivated by gaming; targets stuttering / interactivity (high throughput and low tail latency).

### D-F1-34 — Edge on Min's LPC 2025 session: design and lessons
- "At the 2025 Linux Plumbers Conference (LPC), held in Tokyo in mid-December, Changwoo Min led a session on what he has learned while developing the "latency-criticality aware virtual deadline" (LAVD) scheduler, which is aimed at gaming workloads. … LAVD uses the extensible scheduler class (sched_ext) and has the primary goal of minimizing stuttering in games; it is implemented in a combination of BPF and Rust."
- "Most of the tasks are fairly short running, around 1ms, though there are a few that run for 2-3ms or more. There are also tasks that run for less than 100µs, which means there is more flexibility in terms of their task placement, he said."
- "So he developed VaporMark—the name refers to Steam—which analyzes data collected using "perf sched record"."
- "The key finding … a single high-level action, such as moving a character on-screen and emitting a sound based on a key-press event, requires that many tasks work together. Some of the tasks are threads in the game process, but others are not because they are in the game engine, kernel, and device drivers; there are often 20 or 30 tasks in a chain that all need to collaborate. Finding tasks with a high waker or wakee frequency and prioritizing them is the basis of the LAVD scheduling policy."
- "benchmarking games is "super hard". … a "reliably reproducible benchmark is absolutely necessary", but games lack that"; "most of the ones he has found for schedulers (e.g. stress-ng and hackbench) are focused on stressing schedulers and measuring the scheduling overhead. That is useful, but improving those numbers does not always lead to better game performance."; "There are some microbenchmarks that mimic specific workloads; one example is schbench, which is meant to reproduce the scheduling characteristics of production web-server workloads. There is a need for something like that to mimic gaming workloads, he said."
- "Min said that LAVD is a single scheduler, though there are some tuning knobs that can be changed with command-line parameters."
- Reading: design — sched_ext, BPF + thin Rust, prioritise tasks with high waker/wakee frequency in task chains (often 20–30 tasks); lessons — tooling gaps (VaporMark on perf sched record, Perfetto), lack of reproducible game benchmarks, scheduler microbenchmarks not predictive of game performance, a gaming analogue to schbench is needed, lock-holder preemption.

---

## 5. Corbet, J. "Sched_ext at LPC 2024." LWN 991205 (topic D-F1-33)

### Copy read
- `https://lwn.net/Articles/991205/`, Jonathan Corbet, September 26, 2024, local `$B/lwn/991205.html` sha256 `a301f8bc17848bc6ce041e57f019a650195013ed096abda4c33eb28fc1eb49e7`.

### D-F1-33
- Heo's overview: "The scx_lavd scheduler, for example, is focused on interactivity and, specifically, consistently getting higher frame rates out of games." and "One of those appears to be scx_lavd (about which more was heard later), which is headed for shipment in Steam Deck gaming systems."
- Section "Higher frame rates": "Changwoo Min took over via a remote link to talk about scx_lavd, which is a "latency criticality aware virtual deadline" scheduler aimed at gaming applications. … The goal behind this scheduler was to provide the best gaming experience on Linux in general — not just on the Steam Deck. … A key aspect of gaming workloads is that tasks tend to run quickly, typically no more than 100µs at a time. There are a lot of tightly linked tasks, though, and performance depends on the most critical of those tasks running in the necessary sequence; that is the critical path. … Time slices are then assigned in a manner similar to how the completely fair scheduler does it; slices are fixed, but get shorter as the number of runnable tasks increases."
- "Min concluded by saying that, for gaming applications, scx_lavd consistently enables higher frame rates than the EEVDF scheduler while using (slightly) less power and with fewer stutters."
- Reading: LPC 2024 talks: Heo said scx_lavd was headed for shipment in Steam Deck systems; Min (remote) presented LAVD for gaming — tasks typically ≤ 100 µs, critical-path task chains, latency criticality from wake/wait frequencies, CFS-like slices; claims higher frame rates than EEVDF with slightly less power.

---

## 6. Dai, D., & Newton, R. LPC 2025 sched_ext MC, contribution 2099 (topic D-F1-35)

### Copy read
- `https://lpc.events/event/19/contributions/2099/`, local `$B/lpc/2099.html` sha256 `74577594f9334c25735f9592960835208160f9facf0c191d0189ef616ab0add5`. Title "How do we make a Steamdeck scheduler work on large servers", 12 Dec 2025 18:12, 18 m, Hall B2, sched_ext MC; speakers David Dai (Meta), Ryan Newton (Meta).

### D-F1-35
- Description: "With the proliferations of many sched_ext schedulers, including ones that caters for very specific workloads within Meta. There exists a need for a "default" fleet scheduler that "just works" for a wide range of hardware and use cases. SCX_LAVD is one such candidate as one of the more mature sched_ext schedulers out there with various heuristics to favor latency critical threads. The talk will focus on various challenges and strategies in bringing in SCX_LAVD and trying to run it on large production workloads and large topologies: How do we handle large and varied topologies and cache hierarchies that exists in the fleet to take optimal advantage of the hardware? How do we tune LAVD such that it performs well in a wide range of different services and use cases?"
- Reading: the speakers intend to run scx_lavd as a candidate default fleet scheduler on Meta's large production servers/topologies and to tune it for a wide range of services.

---

## 7. Microsoft Game Mode documentation; Xbox Support; Apple "Use Game Mode" (topics D-F1-36 … D-F1-39)

### Copies read
- Game Mode programming-guide page (the Learn portal; the old `windows/win32/gamemode/` path returns 404): `https://learn.microsoft.com/en-us/previous-versions/windows/desktop/gamemode/game-mode-portal`, local `$B/gamemode/prev_portal.html` sha256 `4304eaa1f8b7d59c724eecdd507ac98a7db6e16c5fdbc08f1a5dc982b289d964`.
- API overview `https://learn.microsoft.com/en-us/windows/win32/api/_gamemode/`, local `$B/gamemode/api_gamemode.html` sha256 `8c551083a545b625e11aa952c1b46272beb3fde285050e240effd6b98c4ebbff` ("Last updated on 2023-01-24").
- Header page `https://learn.microsoft.com/en-us/windows/win32/api/expandedresources/`, local `$B/gamemode/expandedresources.html` sha256 `76450167976b6233938de330af4f43667749d921a397796da5154a87ad5c9125` ("Last updated on 2023-01-24").
- Function pages `…/nf-expandedresources-getexpandedresourceexclusivecpucount` (sha256 `7d5f92da1f42249af58f46bf5e988b79d45778f480fddc75c84f97fdcc4ddaff`), `…-hasexpandedresources` (`0cec31aa28c30c72146febb01a0e71066d457ddd31f30c4f371b0c65ccb701f9`), `…-releaseexclusivecpusets` (`0b5810d95087ddf63fdc038b4eb05931367a375c2a6979f77d88a5ea06453382`), local `$B/gamemode/*.html`.
- Xbox Support `https://support.xbox.com/en-US/help/games-apps/game-setup-and-play/use-game-mode-gaming-on-pc` — the server returns a JavaScript shell; rendered with headless Chrome (`--dump-dom`), local `$B/gamemode/xbox_dom.html` sha256 `75a9590ee2821b84b089886cbe6e2e176c6fee1b4130f0f52e84c815c7da554b`.
- Apple `https://support.apple.com/en-us/105118`, local `$B/gamemode/apple105118.html` sha256 `99173c1124d432687fc3234e155d697f6c60f6436f57bb05799554cbbffb83f9`, "Published Date: September 14, 2026".

### D-F1-36 — what Game Mode is and does
- Portal: "Important: The Game Mode APIs are deprecated in Windows 10, version 1809 and later." … "Game Mode provides customers with the best possible gaming experience by fully utilizing the capacity of their current hardware. It does this by granting a game exclusive or priority access to hardware resources. These resources being dedicated to the game help it hit performance targets more consistently. The performance increase that comes from Game Mode is directly related to the number and impact of other activities running on the device." … "The app must be in the foreground and have focus before exclusive resources are granted." … "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer."
- Portal: "… they may opt-out of CPU exclusivity by calling ReleaseExclusiveCpuSets to get access to all cores, but at a higher latency due to other processes and system activities being scheduled on the same cores as the game. However, the game would still get access to other Game Mode resources, such as increased GPU prioritization."
- Reading: Game Mode grants the foreground game exclusive or priority access to hardware resources (exclusive CPU sets, GPU prioritisation); other work is kept off the game's exclusive cores. The API is deprecated since Windows 10 1809.

### D-F1-37 — functions in `expandedresources.h`; where `SetProcessDefaultCpuSets` appears
- Header page: "expandedresources.h contains the following programming interfaces: Functions GetExpandedResourceExclusiveCpuCount … HasExpandedResources … ReleaseExclusiveCpuSets …".
- `ReleaseExclusiveCpuSets` page, Remarks: "As with SetProcessDefaultCpuSets, ReleaseExclusiveCpuSets applies to the whole process." The same sentence is in the portal page. `SetProcessDefaultCpuSets` is not on the header page.
- Reading: three functions; `SetProcessDefaultCpuSets` appears only as a comparison in the ReleaseExclusiveCpuSets remarks (and the portal), not as a header member.

### D-F1-38 — Xbox Support: Windows Update
- "When you use Game Mode, Windows prioritizes your gaming experience by turning things off in the background. When you're running a game, Game Mode: Prevents Windows Update from performing driver installations and sending restart notifications / Helps achieve a more stable frame rate depending on the specific game and system" … "Note Game Mode is turned on by default."
- Reading: during play Game Mode stops Windows Update from installing drivers and sending restart notifications; on by default.

### D-F1-39 — Apple Game Mode
- "Game Mode optimizes your gaming experience by giving your game the highest priority access to your CPU and GPU, lowering usage for background tasks. This can result in smoother, more consistent frame rates and improved in-game responsiveness. Game Mode doubles the Bluetooth sampling rate, which reduces input latency and audio latency for wireless accessories like game controllers and AirPods." … "Mac with Apple silicon and macOS Sonoma 14 or later and a game that supports macOS full-screen mode." … "When your game enters full screen, Game Mode automatically turns on for that game."
- Reading: highest-priority CPU/GPU access for the game, lower usage for background tasks, doubled Bluetooth sampling rate; automatic in full screen on Apple-silicon Macs with macOS 14+.

---

## 8. Feral GameMode 1.8.2; Red Hat tuned v2.28.0 `tuned-main.conf`; systemd `oomd.conf(5)` (topics D-F1-40, -46)

### Copies read
- FeralInteractive/gamemode tag `1.8.2` → commit `c54d6d4243b0dd0afcb49f2c9836d432da171a2b`: `example/gamemode.ini` local `$B/feral/gamemode.ini` sha256 `678cd894d8ae5db955808b98a4caf124fb3b6ef6bd8b7c2be430136a03d06db9`; `README.md` `$B/feral/README.md` sha256 `51010c969f4be55ab299e87a961d55ef7f7799570ac62c35e3c622e54a2ce991`; `daemon/gamemode-config.c` `$B/feral/gamemode-config.c` sha256 `d937ac1f2413b7bada8805f65ae6c222a5f002f98ac7658ef65e5f810072e293`.
- redhat-performance/tuned tag `v2.28.0` → commit `a4907c9af9ea0a29f208b8f024465af16a7c9cbf`: `tuned-main.conf` local `$B/tuned/tuned-main.conf` sha256 `6a41544b2a508d2046ba087b221fb619149ab37f053902debfae723e36117f62`.
- systemd tag `v255` → commit `db11bab38ccf1ed257f310d29070843d4c58ea01`: `man/oomd.conf.xml` local `$B/oomd/oomd.conf.xml` sha256 `9cbf877fb07971ce71e4a5aa3b4ad92e6c734a9e36acaa2cba87d72258f3ff73`. (The topic names no systemd version; v255 is the upstream tag of the Ubuntu 24.04 series; 255.4 is a stable point release not separately read.)

### D-F1-40 — how a game requests GameMode; whitelist/blacklist
- README "Requesting GameMode": "For games/launchers which integrate GameMode support (see list later on), simply running the game will automatically activate GameMode. For others, you must manually request GameMode when running the game. This can be done by launching the game through `gamemoderun`: … gamemoderun ./game … Or edit the Steam launch options: gamemoderun %command%". README line 2: "GameMode is a daemon/lib combo for Linux that allows games to request a set of optimisations be temporarily applied to the host OS and/or a game process."
- `gamemode.ini` lines 44–51: "[filter] ; If "whitelist" entry has a value(s) ; gamemode will reject anything not in the whitelist ;whitelist=RiseOfTheTombRaider ; Gamemode will always reject anything in the blacklist ;blacklist=HalfLife3 ; glxgears".
- `gamemode-config.c` lines 600–607: "/* If the whitelist is empty then everything passes */ … Currently is a simple strstr check, but could be modified for wildcards etc."
- Reading: a game requests GameMode itself (integrated support via the client library) or is launched via `gamemoderun` (preload). The `[filter]` section rejects clients not in a non-empty whitelist and always rejects blacklisted ones (substring match on the client name).

### D-F1-46 — time settings and defaults
- GameMode `gamemode.ini` lines 2–3: "; The reaper thread will check every 5 seconds for exited clients, for config file changes, and for the CPU/iGPU power balance / reaper_freq=5"; `gamemode-config.c` line 55 "#define DEFAULT_REAPER_FREQ 5", line 380 sets it as the default.
- tuned `tuned-main.conf` lines 9–18: "# Dynamically tune devices, if disabled only static tuning will be used. / dynamic_tuning = 0 / … / # How long to sleep before checking for events (in seconds) … sleep_interval = 1 / # Update interval for dynamic tunings (in seconds). # It must be multiply of the sleep_interval. / update_interval = 10".
- `oomd.conf.xml` lines 83–88: "DefaultMemoryPressureDurationSec= Sets the amount of time a unit's control group needs to have exceeded memory pressure limits before systemd-oomd will take action. … Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0." (Lines 70–77, for DefaultMemoryPressureLimit=: pressure measured as "the fraction of time in a 10 second window …", default 60%.)
- Reading: GameMode reaper every 5 s (exited clients, config changes, CPU/iGPU power balance), default 5. tuned: dynamic tuning off by default (`dynamic_tuning = 0`); `update_interval = 10` s for dynamic tunings. systemd-oomd acts after pressure has exceeded the limit for 30 s by default.

---

## 9. Linux `include/linux/sched.h`, tag v6.17 (topic D-F1-48)

### Copy read
- `https://raw.githubusercontent.com/torvalds/linux/v6.17/include/linux/sched.h` (tag v6.17 → commit `e5f0a698b34ed76002dc5cff3804a61c80233a7a`), local `$B/linux/sched.h` sha256 `d7a2b1e7876e8893308c7d737ba6b2cfa6bf6f77820dc44884caa6cd0855d7ab`.

### D-F1-48
- Lines 314–321: "/* Define the task command name length as enum, then it can be visible to BPF programs. */ enum { TASK_COMM_LEN = 16, };"
- Lines 1155–1165: "/* executable name, excluding path. * * - normally initialized begin_new_exec() * - set it with set_task_comm() *   - strscpy_pad() to ensure it is always NUL-terminated and *     zero-padded …*/ char comm[TASK_COMM_LEN];"
- Reading: 16-byte buffer, always NUL-terminated and zero-padded, so the longest stored name is 15 characters.

---

## 10. Koldijk, S., et al. (2014). SWELL-KW, ICMI 2014; DANS doi:10.17026/dans-x55-69zp (topics D-F2-01, -02, -03, -06)

### Copies read
- DANS Data Station (SSH) dataset metadata: `https://ssh.datastations.nl/api/datasets/:persistentId/?persistentId=doi:10.17026/DANS-X55-69ZP`, local `$B/swell/dataset.json` sha256 `fa6e6ee01d0246d4864df69744ca65453b72330acc74f2c272ed3538cbec7c3e`. Latest version 4.1, RELEASED 2025-06-04T08:57:35Z, 919 files.
- ICMI 2014 paper as deposited in the dataset ("ICMI 2014 paper_final_cr.pdf", datafile id 171660), local `$B/swell/icmi2014.pdf` sha256 `940c544ca829d18776b4e95e659684ad2ace9e1166aa12982bfd4bec5fa710e2`.
- Dataset manual ("Manual KW Dataset .docx", id 172099), local `$B/swell/manual.docx` sha256 `294a690ac7b63b7661c271bbcc1a3f1bcdc146196257a91f02a06bc22cce98e0`.
- All 76 uLog XML files (`a_pp*_c*_uLog_*.xml`, folder "0 - Raw data/A - anonimized Computer interaction - raw data uLog"), local `$B/swell/ulog/`; every file's SHA-1 matched the DANS checksum; sha256 of the concatenation in name order `5c712bcc85e141d09b61cb5d7d21b9e21f3d6cf93ca317dd3eaa5696c39d01ff`.

### D-F2-01 — participants; where, when, OS; time per participant
- Paper §3.7 "Participants": "25 students participated in our experiment, of which 8 were female and 17 male. The average age was 25 (standard deviation 3.25). Most participants were native Dutch. They were interns from TNO and students from Delft University of Technology who were approached by advertising."
- Paper §3.4 "Apparatus": "Participants performed their tasks on a computer (Dell Latitude E6400) with Windows 7 Professional with a 17 inch screen and mouse and keyboard (see Figure 2). Office 2010 was installed, which the participants used for email (Outlook), report writing (Word) and making presentations (Powerpoint). As a browser, Internet Explorer was used with Google as default search engine."
- Paper §3.3: "The experiment was divided into three blocks for the different stressor conditions, each taking approximately one hour. … the total experiment took about 3 hours." Manual: "The SWELL-KW dataset contains data from 25 participants (~3 hours each), for working under 3 conditions: neutral, interruptions and time pressure (plus a relax phase)."
- When: uLog file names carry dates from `20120918` (participant 1) to `20121107` (participant 25). The paper mentions "the lab" (§3.6) but names no city or site.
- Reading: 25 students/interns (TNO interns, TU Delft students; 8 F / 17 M; mean age 25); Windows 7 Professional, Office 2010; recorded 2012-09-18 to 2012-11-07 (from file names); about 3 hours per participant (three ~1 h blocks). Location: a lab, not named in the paper or manual.

### D-F2-02 — what uLog records per keystroke and per pointer event
- Paper §3.6: "Computer interactions were logged with the key-logging application uLog (version 3.2.5, by Noldus Information Technology), which ran as a background application on the users' computer."
- From the XML (file `a_pp1_c1_uLog_20120918_131425.xml`, profiled programmatically): Keyboard events have fields `EventType, EventAction ('character' | 'special key' | 'key combination'), TimeStamp (UTC, 100-ns resolution, e.g. "2012-09-18T11:30:20.6644181Z"), Date, Time (local with offset), Milliseconds, EventDescription, KeyboardValue, KeyboardModifiers, Control` — `Control` for character events holds `ControlType, ControlCaption, ControlValue, ControlIsPassword, ControlFramework, ControlClass, ControlApplication, ControlWindowText`; for special keys `Control` holds only `ControlIsPassword`. Mouse events: `EventAction ('clicked' | 'doubleclicked' | 'dragged' | 'wheel turned'), TimeStamp, Date, Time, Milliseconds, EventDescription, MouseButton, MouseCursorX, MouseCursorY, MouseWheelDirection, MouseWheelTurnAmount, MouseRelDistance, MouseTotDistance, Control, TargetControl`. Other events: 'Window Activated', 'Keyboard focus changed', 'Application started', 'Application exited', 'Browser URL changed', 'MessageBox activated'.
- Example keyboard event: "<EventAction>character</EventAction> <TimeStamp>2012-09-18T11:30:20.6644181Z</TimeStamp> … <KeyboardValue>w</KeyboardValue> … <ControlApplication>iexplore</ControlApplication> <ControlWindowText>New Tab - Windows Internet Explorer</ControlWindowText>".
- Reading: one event per keystroke (no separate key-down/key-up), with timestamp, the key value, modifiers and the focused control/application/window title; pointer events carry button, cursor x/y, wheel, distances and control.

### D-F2-03 — licence and access
- dataset.json: `"license": {"name": "CC-BY-NC-SA-4.0", "uri": "http://creativecommons.org/licenses/by-nc-sa/4.0"}`, `"termsOfAccess": "N/a"`, `"fileAccessRequest": false`; every file listed has `"restricted": false`. Rights holder field: `dansRightsHolder: ["TNO"]`. Files downloaded without login.
- Reading: CC BY-NC-SA 4.0, open (unrestricted) access in version 4.1.

### D-F2-06 — computation: focus-episode durations; returns after a switch
- Method (B1's own, script `$B/../scripts/swell_focus.py`): over all 76 uLog files, the foreground-application sequence is the `ControlApplication` of each "Window Activated" event, consecutive identical applications merged; an episode lasts from one activation to the next different-application activation (last episode cut at the file's last event). A switch A→B "returns" if the next switch goes back to A (immediate), or if A appears again later in the same file.
- Result: 9,575 episodes; median 5.47 s, mean 24.13 s; p10 0.69 s, p25 1.64 s, p75 19.21 s, p90 53.49 s, p99 452.73 s; share ≤ 1 s 0.140, ≤ 2 s 0.296, ≤ 5 s 0.479, ≤ 10 s 0.622, ≤ 30 s 0.823, ≤ 60 s 0.913, ≤ 300 s 0.987. 9,499 switches; immediate return A→B→A 54.1%; A seen again later in the same file 95.1%. Most frequent applications by episode count: iexplore 2,939, WINWORD 2,874, explorer 1,934, OUTLOOK 611, POWERPNT 534, uLog 3.2 377.
- Reading: focus episodes are heavy-tailed (median ~5 s, mean ~24 s); about half of the switches away are followed directly by a return. Numbers depend on B1's episode definition; the repository's definition was not seen.

---

## 11. Dhakal, V., et al. (2018). Observations on Typing from 136 Million Keystrokes. CHI 2018 (topics D-F2-07, -08, -09)

### Copies read
- Project page `https://userinterfaces.aalto.fi/136Mkeystrokes/`, local `$B/dhakal/page.html` sha256 `320fd2561632119e1cc8ad5da9fbecaf8b66730befdbd3f1fb78df6dd3bb010c`.
- Paper PDF linked there, `https://userinterfaces.aalto.fi/136Mkeystrokes/resources/chi-18-analysis.pdf`, 12 pages, local `$B/dhakal/chi-18-analysis.pdf` sha256 `e5e72facf874deed7b18fcf87f827dce565a8c56f6f7a99de4564303301496a2`.
- Data `https://userinterfaces.aalto.fi/136Mkeystrokes/data/Keystrokes.zip` (HTTP Content-Length 1572785433, Last-Modified 2018-03-29) — see the data paragraph at the end of this group.

### D-F2-07 — released data (page part)
- Page: "Text files of the keystrokes in a .zip file (1.4 GB zipped, 16 GB unzipped). The data contains the keystroke-by-keystroke entries typed by every participant. The package also includes a metadata file. See readme.txt for introduction and license. This data is free to use for research and non-commercial use with attribution to the authors." Link target `data/Keystrokes.zip`.
- (Fields, metadata row count and the readme's licence text: see the data paragraph below.)

### D-F2-08 — population, task, participants, IKI statistics
- Paper "Sampling and Participants": "Participants in the study were self-selected from the user base of the commercial site. … The user base of the company is composed mainly of younger people from the US who are interested in testing and improving their typing skills. Table 1 summarises the demographics of 168,960 voluntary participants who completed all 15 sentences and filled in the demographic questionnaire. … of ∼406,000 participants starting the study, only ∼193,000 finished the test and questionnaire. Of these, we excluded 12% as detailed below."
- "Task and Procedure": "The task was to transcribe 15 English sentences. Participants were shown instructions stating to first read through and memorise a sentence, then type it as quickly and accurately as possible."
- "Materials": "Sentences were drawn randomly from a set of 1,525 sentences, composed of the Enron mobile email corpus [38] and English gigaword newswire corpus [11]."
- "Performance Measures": "INTER-KEY INTERVAL (IKI) is the difference in timestamps between two keypress events. For IKI-based analysis, we removed keystrokes that were typed more than 5000 ms after the previous keystroke."
- "Results": "The final dataset includes 136,857,600 keystrokes from 168,960 participants with, on average, about 810 keypresses per participant." "INTER-KEY INTERVALS Average inter-key interval is 238.656 ms (SD = 111.6). A lower bound of about 60 ms can be observed. The IKI distribution shown in Figure 2 has a skewness of 1.98 and kurtosis measure of 7.1. … For fast typists, the average IKI is ∼120 ms, with a standard deviation of only 11 ms, while slow typists have an IKI of over 480 ms". Table 3: "IKI (ms) 238.66 111.60"; caption "At the left are the mean and SD for each measure"; Figure 2 caption "Histogram and density estimate of WPM, uncorrected errors, IKI, and keypress duration." and text "Figure 2 shows the distribution of WPM, uncorrected error rate, IKI, and keypress duration over all participants."
- Reading: self-selected online volunteers (mainly young, US) on a typing-test site; transcription of 15 sentences; 168,960 participants in the final set; mean IKI 238.66 ms with SD 111.6 ms. The SD (and the distribution in Figure 2) is across participants' per-participant values (fast-typist SD 11 ms only makes sense per participant). The IKI analysis drops keystrokes > 5000 ms after the previous one.

### D-F2-09 — computations (share of gaps > 1 s)
- SWELL-KW Word stream (B1's computation over the 76 uLog files, same script as D-F2-06): consecutive keyboard events both of type 'character' and both in application WINWORD: 102,274 gaps, share > 1 s = 3.07%.
- Dhakal within-sentence sample: see the data paragraph below.
- "Which 9.5 decision records this alternative as not taken" is a question about the repository's own decision record (9.5, the workload-dataset slice on interactive timing); it is not answerable from the source and is left to Phase 2.

### Dhakal data paragraph
See "Group 11 data" at the end of this file (the archive was read last).

---

## 12. González, V. M., & Mark, G. (2004). "Constant, Constant, Multi-tasking Craziness". CHI 2004, 113–120 (topics D-F2-10, -11, -12)

### Copy read
- ACM DL (`dl.acm.org/doi/pdf/10.1145/985692.985707`) returned a Cloudflare challenge page — not readable. Read the author-hosted camera-ready copy `https://www.ics.uci.edu/~gmark/CHI2004.pdf` (8 pages, headers "CHI 2004 ׀ Paper … 24-29 April ׀ Vienna, Austria", footers "113" … "120 Volume 6, Number 1"), local `$B/papers/gmark-CHI2004.pdf` sha256 `988981bfff2408ba2158cf6bcc8bc24c4b1eed9e9cfd3490c69044ea88dcfac4`.

### D-F2-10 — mean time per event; definition; exclusions
- p. 115: "We coded our data into events that we defined as any continuous use of a device or engagement in an interaction with other individuals (e.g. phone conversation, using a spreadsheet with the PC, annotating documents, or talking "through the wall"). Following Sproull [12], we considered that in any particular event neither the structure nor the content changes."
- p. 116 Table 2 ("Average continuous time spent on events before switching (hour:min:sec)"): row "All events except "Formal meetings" and "Other"" — "% entire day 70.52%, Avg. Time/Day 0:45:56 (0:52:03), Avg. Time/Event 0:03:08 (0:02:27)"; row "All events total" — "Avg. Time/Event 0:08:55 (0:13:23)". "Other" = "unknown, personal".
- p. 116 text: "What was most surprising to us was that people spend on the average slightly over three minutes on an event (leaving out formal meetings, unknown, and personal events) before another event is initiated."
- Abstract: "People average about three minutes on a task and somewhat more than two minutes using any electronic tool or paper document before switching tasks."
- Reading: mean 3 min 8 s (SD 2 min 27 s) per event excluding formal meetings, unknown and personal events; 8 min 55 s over all events. An event is a continuous use of a device or interaction with someone, constant in structure and content.

### D-F2-11 — continuous time in a working sphere before switching
- p. 117 Table 4 ("Avg. no. of working spheres (WS) per person, and avg. time spent in each WS per day"): "Central and Peripheral WS only 9.81 (3.39) | 0:33:32 (0:50:59) | 0:11:28 (0:10:54)"; "All All 12.81 (3.39) | 0:40:41 (0:50:58) | 0:13:49 (0:16:14)" (columns: Average WS/day (sd); Avg. Time/WS (sd); Avg. Time/segment (sd)).
- p. 117 text: "An individual spent about 33 min. 32 sec. per working sphere; however it does not occur as a continuous period of time. … Table 4 shows that the actual average duration of a working sphere segment is quite short (11 min, 28 sec.)."
- p. 117 Table 5 ("Avg. time per WS segment without "nonsignificant" disruptions"): "Both All 0:12:18 (0:11:53)"; text p. 118: "Thus, a segment was considered as "continuous" even if people turned to another working sphere for less than two minutes. Table 5 shows that even after removing what we consider "nonsignificant" disruptions, people still spent only a short average time in a working sphere segment (somewhat more than 12 minutes)."
- Abstract: "people spend about 12 minutes in a working sphere before they switch to another."
- Reading: central + peripheral spheres: 11 min 28 s per segment (SD 10:54); with switches < 2 min ignored: 12 min 18 s (SD 11:53); total per sphere per day 33 min 32 s. Including metawork, personal, unknown: 13 min 49 s per segment, 40 min 41 s per sphere.

### D-F2-12 — spheres per day; time per device/document; statistics; participants
- p. 117: "We identified that each person worked on an average of ten working spheres per day, during the three days of our observation." Table 4: central + peripheral 9.81 (3.39); all 12.81 (3.39).
- p. 116 Table 3 ("Average time usage per device per person"): "All devices 51.59% 100% 0:44:57 (1:13:27) 0:02:11 (0:01:52)" (footnote 4 "Weighted average"); text: "People spent an average of 2 min. 11 sec. working with any device or paper before they switched to another device or event."
- Statistics: means with SD in parentheses throughout; ANOVA and Tukey post-hoc tests (e.g. "F(2,13)=6.74, p<0.01").
- pp. 114–115: "we conducted an observational study at ITS, an investment management company located on the west coast of the U.S." … "Fourteen people were observed over a seven-month period. Each person was observed for a period of three and a half days. … the average time of formal observation for each individual was 26 hours." … "We studied analysts, developers and managers"; "A total of 477 hours was spent in observation at the field site."
- Reading: ~10 spheres/day (9.81 central+peripheral; 12.81 all); 2 min 11 s per device/document before switching (weighted mean, SD 1:52); means and SDs with ANOVA; 14 informants (analysts, developers, managers) at one US west-coast investment-management IT firm, shadowed 3.5 days each.

---

## 13. Mark, G., González, V. M., & Harris, J. (2005). No Task Left Behind? CHI 2005, 321–330 (topics D-F2-14, -15, -16)

### Copies read
- ACM DL: Cloudflare challenge, not readable. Author-hosted camera-ready `https://www.ics.uci.edu/~gmark/CHI2005.pdf` (10 pages, header "CHI 2005 ׀ PAPERS: Take a Number, Stand in Line (Interruptions & Attention 1) April 2–7 ׀ Portland, Oregon, USA", page numbers 321–330), local `$B/papers/gmark-CHI2005.pdf` sha256 `ec8ae49c99e17ff6d48b88edbb787b128bae97fa7c8928c5f9788175be4f664a`.
- For the resumption-figure check (D-F2-16): CHI 2004 copy (group 12); Mark, Gudith & Klocke, "The Cost of Interrupted Work: More Speed and Stress", CHI 2008, author copy `https://www.ics.uci.edu/~gmark/chi08-mark.pdf` (4 pages, Word-derived), local `$B/papers/gmark-chi08-mark.pdf` sha256 `e562bd16eca40a2a59499d79b15d5577d1ea3365401a8b6cb8e834187fb7fb8b`; Mark, Iqbal, Czerwinski & Johns, "Bored Mondays and Focused Afternoons", CHI 2014, author copy `https://www.ics.uci.edu/~gmark/Home_page/Publications_files/Focus%20_1.pdf` (8 pages), local `$B/papers/gmark-chi2014.pdf` sha256 `bfaa317691c9e67b8201bfb064a353e095f6a1b9f3b0ed38d12ea1ec4b1276a6`. The 2006 interview itself was not read.

### D-F2-14 — time in a working sphere before switch/interruption; informants
- p. 324–325: "The average length of time that the informants spent in central and peripheral working spheres was 11 min. 4 sec., (sd=18 min. 9 sec.) before switching to another working sphere or being interrupted."
- p. 323: "The study occurred in two phases over a thirteen-month period. Twenty-four people in total were observed in detail: 7 managers, 9 analysts, and 8 developers. Fourteen members from the JEB team were shadowed and in the second phase ten members of the AUG team were shadowed." … "three days for an average time of 25 hours, 42 minutes per person. Over 700 formal hours of observation were done."
- p. 321: "In a previous study, we discovered that information workers switched work events frequently: averaging every three minutes [6]. … We have expanded our observations to include almost double the number of informants".
- p. 324: "Our informants worked in an average of 11.7 (sd=2.4) different working spheres."
- Reading: 11 min 4 s (SD 18 min 9 s) in central + peripheral spheres before a switch or interruption; 24 informants (7 managers, 9 analysts, 8 developers); the 14 JEB-team members are the first phase — the same 14-person JEB team the 2004 paper observed (2004 paper: "Twenty-two members of the JEB team" and fourteen people observed) — plus 10 AUG-team members. The paper calls ref [6] "a previous study" and expands it to "almost double the number of informants"; it does not say in so many words that the 14 are the same individuals, but the JEB/14 match makes that the reading.

### D-F2-15 — internal vs external; table vs text
- p. 326 Table 3 ("Percent of internal/external interruptions according to the source of the interruption. Data in parentheses are percentages within internal/external. N=1282."): rows "Central WS 38.0% 62.0% 100% / (28.8%)* (43.3%) (36.3%)"; "Peripheral WS 20.0% 80.0% 100% / (7.6%) (28.2%) (18.3%)"; "Other WS (personal, metawork, unknown) 67.3% 32.7% 100% / (63.6%) (28.5%) (45.3%)"; "Column avg. 52.0% 48.0% 100%" (columns Internal, External, Total).
- p. 326 text: "Managers are more likely to experience external interruptions (59.2%) than internal interruptions (40.8%), whereas analysts and developers experience internal and external interruptions about equally, X2(2)=.10.1, p<.006." and "Most internal interruptions are due to personal, metawork or unknown working spheres (63.6%) whereas most external interruptions are due to work related to central working spheres (43.3%)".
- B1's check: with row shares and row totals, internal overall = 0.363·0.380 + 0.183·0.200 + 0.453·0.673 ≈ 0.138 + 0.037 + 0.305 = 0.480; the within-column percentages give the same (e.g. 0.48·0.288/0.363 = 0.381 ≈ 38.0%). So the table's own rows imply 48% internal / 52% external, while its "Column avg." row prints 52.0% internal / 48.0% external.
- Reading: overall split is about half and half; the table's column-average row contradicts the table's rows (the rows imply external 52%, internal 48%). The text gives no overall split, only by role (managers 59.2% external) and by source, and those agree with the rows.

### D-F2-16 — same-day resumption and lag; the 2006-interview figure
- p. 326: "77.2% of interrupted work was resumed on the same day." … "When people did resume work on the same day, it took an average length of time of 25 min. 26 sec (sd=54 min. 48 sec.). … before resuming work, our informants worked in an average of 2.26 (sd=2.79) working spheres." Scope p. 326: "We only consider work that was interrupted and resumed on the same day in order to make a uniform comparison among all informants. … We also do not consider interrupted work during the last work hour".
- Abstract: "Though most interrupted work is resumed on the same day, more than two intervening activities occur before it is."
- Resumption-figure check: text search of the four papers (CHI 2004, 2005, 2008, 2014 copies above) finds no "23 min" or "23:15" resumption figure. The only resumption time is 2005's 25 min 26 s; CHI 2004 gives a share only ("About two-thirds of the time people resume work in their working sphere after interruption", p. 118); CHI 2008 and CHI 2014 report no resumption time.
- Reading: 77.2% resumed the same day; mean lag 25 min 26 s (SD 54 min 48 s) with 2.26 intervening spheres. A "23 minutes" figure does not appear in any of the four CHI papers read.

---

## 14. Czerwinski, M., Horvitz, E., & Wilhite, S. (2004). A Diary Study of Task Switching and Interruptions. CHI 2004, 175–182 (topic D-F2-17)

### Copy read
- ACM DL (`10.1145/985692.985715`): Cloudflare challenge, not readable; microsoft.com research PDF URLs return 403. Read the author-hosted copy `https://erichorvitz.com/taskdiary.pdf` (8 pages; PDF title "Microsoft Word - CHI2004DiaryStudyfinal.doc", created 2022-11-07; page numbers 1–8, not the proceedings' 175–182), local `$B/papers/czerwinski-taskdiary.pdf` sha256 `67d370e0c3d7d3cb4bc228a6ada2c8ad43d5e2a784dbfbd9c67fd1a9fd43bacf`. This is an author-prepared final manuscript, not the ACM typeset; wording may differ from the proceedings.

### D-F2-17
- Abstract: "We report on a diary study of the activities of information workers aimed at characterizing how people interleave multiple tasks amidst interruptions. The week-long study revealed the type and complexity of activities performed, the nature of the interruptions experienced, and the difficulty of shifting among numerous tasks."
- p. 2 "Method": "Eleven experienced Microsoft Windows™ users (3 female) participated in the study. … Participants' occupations spanned a spectrum of domains, including a stock broker, professor of Computer Science, web designer, software developer, boat salesman, and network administrator. The participants' ages ranged from 25 to 50 years of age. A Microsoft Excel XP™ spreadsheet, with worksheets for each day of the week … columns for … Time of Task Start, Difficulty Switching to the Task, What Documents Were Included in the Task, What Was Forgotten If Anything, Comments, and the Number of Interruptions Experienced and the users' task descriptions."
- p. 3: "Types of Tasks. One outlier participant was removed from the rest of the analyses because the subject did not switch among more than two tasks on any given day of the week … For the ten remaining participants …"; "Diary Analyses. … frequency counts of the number of diary entries for each dependent measure were calculated. … subjective ratings of task-switch difficulty … the amount of time spent on the tasks was obtained for each entry. … Most statistics were then collapsed across days … The data was subjected to multivariate logistical regression with each user's task switch entry included as input."
- p. 4: "Reported task lengths averaged 53 minutes, with a large standard deviation of 90.9 minutes. The distribution of task lengths was highly negatively skewed, with the majority of the tasks reported being shorter than the average length." "users reported an average of 0.7 interruptions per task". Task-switch causes: self-initiated 40%, next task on to-do list 19%, telephone 14%, meetings/reminders 10%, deadlines 3%, email 3%, requests 3%. p. 5: "Participants in our study reported an average of 50 task shifts over the week." Returned-to tasks: "average task length = 120 minutes v. 45 minutes … F(1,494)= 23.95, p<.001".
- Reading: self-report diary (Excel) over one work week; 11 participants, 10 analysed; statistics are frequencies/percentages, means with SD, ratings, F tests and logistic regression. Mean task length 53 min (SD 90.9). (The paper calls the distribution "negatively skewed" while saying most tasks are shorter than the mean — that describes a positive skew.)

---

## 15. Roeser, J., et al. (2024). Modelling typing disfluencies as finite mixture process. Reading and Writing 37, 359–384 (topic D-F2-18)

### Copies read
- DOI `10.1007/s11145-021-10203-z` (Crossref: vol. 37, pp. 359–384, licence CC BY 4.0). The direct PDF URL served HTML to curl; read the open-access HTML article rendered with headless Chrome, `https://link.springer.com/article/10.1007/s11145-021-10203-z`, local `$B/papers/roeser_article.html` sha256 `6a024a74bd5eda7b77f95cab1c2adcaaa83d12097317a4ed516fbf7bb0d17530` ("Published: 24 August 2021", "Volume 37, pages 359–384 (2024)"); Table 3 page `…/tables/3`, local `$B/papers/roeser_table3.html` sha256 `83ce45acea50c05bdaad0c483e1870ff7a2863c0bf1c16b6c423d8ea76e77a44`.

### D-F2-18 — task, sample, model, Table 3
- Abstract: "We tested these models on a random sample of 250 copy-task recordings. Our results illustrate that we can model copy typing as a mixture process of fluent and disfluent key transitions."
- Method: "The copy-task corpus consists of keystroke data collected via a Javascript-based web application as part of Inputlog 8 … We used a random sample of 250 participants (175 females, 71 males, 4 unknown) from the age range of 18 to 25 years (median age = 22 years). In this analysis we focus on the difference between key-down presses … Before analysis we excluded spaces and editing operations from the data." "In the consonants task, participants saw and copy-typed a single time four blocks of six consonants; i.e. "tjxgfl pgkfkq dtdrgt npwdvf." … In the LF-bigram task, participants typed three-word combinations seven times (een chaotische cowboy "a chaotic cowboy" in the Dutch version) of which four bigrams are low frequent. … we removed all repetitions after the first time the three-word sequence was copied." Data: "a subset of the Dutch copy-task corpus".
- Model (Eq. 7): "y_ij ∼ θ_i · LogNormal(β + δ + u_i + w_j, σ²_e′) + (1 − θ_i) · LogNormal(β + u_i + w_j, σ²_e)", with an autoregressive term φ_i · log(y_ij−1) in the best model (M3). Footnote: "We use a log-normal models as this is equivalent to the standard statistical method used in the field".
- Table 3 ("Parameter estimates with 95% PIs separated into population estimates and estimates for variance components"; columns LF bigrams | Consonants): "β (fluent typing) 158 [139, 180] | 429 [356, 515]"; "δ (disfluency slowdown) 95 [76, 116] | 414 [333, 509]"; "θ (disfluency probability) 0.34 [0.31, 0.38] | 0.73 [0.66, 0.8]"; "ϕ (autoregressor) 0 [−0.02, 0.02] | −0.08 [−0.1, −0.05]"; variance estimates "σ² (residual error) 0.73 [0.7, 0.75] | 0.54 [0.52, 0.56]", "σ²_e (fluent typing) 0.29 [0.27, 0.3] | 0.29 [0.26, 0.32]", "σ²_e′ (disfluency) 1.16 [1.12, 1.21] | 0.79 [0.77, 0.81]", "η² (autoregressor) 0.04 [0.04, 0.05] | 0.01 [0, 0.02]", "σ²_u (between-participants) 0.03 [0, 0.08] | 0.27 [0.23, 0.31]", "σ²_w (between-bigrams) 0.22 [0.17, 0.3] | 0.24 [0.17, 0.33]".
- Text: "Table 3 summarises the population and variance estimates as posterior mean with 95% probability intervals (PI). … keystroke intervals were longer for the consonants task (429 msecs, PI: 356–515) compared to the LF-bigrams task (158 msecs, PI: 139–180). … For the LF-bigrams task, the model determined a slowdown of 95 msecs (PI: 76–116) with a probability of 0.34 (PI: 0.31–0.38); for the consonants task we found a slowdown of 414 msecs (PI: 333–509) with a probability of 0.73 (PI: 0.66–0.80)."
- Reading: copy typing (Dutch Inputlog copy task, consonant and low-frequency-bigram subtasks), 250 participants aged 18–25; Bayesian two-component log-normal mixture with by-participant and by-bigram random effects and autoregression. Table 3 values are posterior means with 95% PIs. β and δ are reported in milliseconds (the text says "msecs"; δ enters the model on the log scale, so the 95/414 ms slowdowns are back-transformed, and the paper does not show how). θ is a probability; φ is a coefficient on log(previous IKI); the variance components are log-scale parameters of the LogNormal terms (units not stated in the table).

---

## Group 11 data (Dhakal 136M Keystrokes archive)

- Archive: `https://userinterfaces.aalto.fi/136Mkeystrokes/data/Keystrokes.zip`, 1,572,785,433 bytes, local `$B/dhakal/Keystrokes.zip` sha256 `5fb217e0e1273017a6789c5c7ebcc00eed624f2f6426c284da2077a88e270420`. Uncompressed total 18,854,241,824 bytes; 168,597 entries (2 directories, `readme.txt`, `metadata_participants.txt`, 168,593 `<id>_keystrokes.txt` files). `readme.txt` sha256 `c81fcbee7e98e53a5bc789074207ec338e66edd204bbf9a160c8edfaf098a08c`; `metadata_participants.txt` sha256 `3ba22e2c23dbcbb5645197b9dd68c17e9ef68a1be7170e1bc1f0cd869a68ac6d`.

### D-F2-07 — data file, fields, metadata rows, licence (data part)
- File name `Keystrokes.zip`: 1,572,785,433 bytes (1.57 GB, 1.46 GiB; the page says "1.4 GB zipped"); unzipped 18,854,241,824 bytes (18.9 GB, 17.6 GiB; the page says "16 GB unzipped").
- `readme.txt` lines 53–62 (per-keystroke columns): "PARTICIPANT_ID Unique ID of participant / TEST_SECTION_ID Unique ID of the presented sentence / SENTENCE Sentence shown to the user / USER_INPUT Sentence typed by the user after pressing Enter or Next button / KEYSTROKE_ID Unique ID of the keypress / PRESS_TIME Timestamp of the key down event (in ms) / RELEASE_TIME Timestamp of the key release event (in ms) / LETTER The typed letter / KEYCODE The javascript keycode of the pressed key". The header of `100001_keystrokes.txt` matches these nine columns.
- `metadata_participants.txt`: 168,595 lines = 1 header + 168,594 data rows (tab-separated; header "PARTICIPANT_ID AGE GENDER HAS_TAKEN_TYPING_COURSE COUNTRY LAYOUT NATIVE_LANGUAGE FINGERS TIME_SPENT_TYPING KEYBOARD_TYPE ERROR_RATE AVG_WPM_15 AVG_IKI ECPC KSPC ROR"; the readme lists an AVG_KEYPRESS column that the file does not have, and calls LAYOUT "KEYBOARD_LAYOUT").
- `readme.txt` lines 17–21: "LICENSE AND ATTRIBUTION … You are free to use this data for non-commercial use in your own research or projects with attribution to the authors." (page: "free to use for research and non-commercial use with attribution to the authors").
- Reading: `Keystrokes.zip`, 1.57 GB zipped (page: 1.4 GB) / 18.9 GB unzipped (page: 16 GB); per keystroke: participant, sentence id, sentence, final input, keystroke id, press and release times (ms), letter, keycode; 168,594 metadata rows (vs 168,593 keystroke files and the paper's 168,960 participants); licence: non-commercial use with attribution (no named licence such as CC).

### D-F2-09 — Dhakal within-sentence computation
- Method (script `$B/../scripts/dhakal_gaps.py`): `random.seed(20261017)`, 2,000 keystroke files sampled from the 168,593; within each TEST_SECTION_ID (one sentence), consecutive PRESS_TIME differences in file order.
- Result: 1,424,638 within-sentence press-to-press gaps (0 negative; 7 malformed lines skipped); share > 1,000 ms = 2.13%; dropping gaps > 5,000 ms first (the paper's IKI rule), share in (1,000, 5,000] = 2.09%; median 168 ms, mean 249.0 ms.
- Reading: about 2% of within-sentence key-to-key gaps exceed 1 s in this sample, against 3.07% for SWELL-KW's Word character stream (group 10/11 computation above).

---

Phase 1 closed 2026-10-17 before `dataset-inventory.md` or any repository claim location was opened. Unreachable copies: ACM Digital Library PDFs (Cloudflare challenge) for groups 12–14, replaced by author-hosted copies as noted; the 2006 interview behind the resumption figure (group 13) was not read.
