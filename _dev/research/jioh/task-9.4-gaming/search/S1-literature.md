# S1 — peer-reviewed and preprint literature (T1–T5)

Reader: S1. Date of all searches and accesses: 2026-09-13. Source copies under `sources/S1-<id>/` (PDF or HTML plus pypdf/own-script text extraction). Only the input file and my own `S1-` folders were read; other readers' folders under `sources/` were not opened.

Extraction note: page numbers below are PDF page numbers from `pypdf`; for slide decks these coincide with the slide numbers printed on the slides. LWN HTML copies were converted to text with a tag-stripping script; passages are quoted from that text.

## 1. Search log

| # | Date | Engine / venue | Exact query | Hits followed | Dead ends |
|---|------|----------------|-------------|---------------|-----------|
| 1 | 2026-09-13 | WebSearch (general) | `Changwoo Min "Lessons from creating a gaming-oriented scheduler" LAVD` | lwn.net/Articles/1051430 (S1-06); lpc.events …/2150/attachments/1951/4162/Steps_Towards_a_Gaming_Optimized_Schedule-lpc2025.pdf (S1-05); static.sched.com …/scx-lavd-oss-na24.pdf (S1-01); YouTube OSPM25 talk (video only, not quotable) | slideshare mirror of the OSS NA deck (duplicate); Phoronix news (secondary) |
| 2 | 2026-09-13 | WebSearch | `scx_lavd Changwoo Min Linux Plumbers 2024 sched_ext latency criticality slides` | lwn.net/Articles/991205 (S1-03); lpc.events/event/19/sessions/229 (sched_ext MC page) | sched-ext.com docs and scx README (S2 territory, not opened) |
| 3 | 2026-09-13 | WebSearch | `LWN 1051430 scheduler gaming` | confirms 1051430 = LPC 2025 Gaming MC report | USPTO patent hits (irrelevant) |
| 4 | 2026-09-13 | WebSearch | `paper characterization mobile game workload thread frame pipeline critical path scheduling Android arXiv` | usenix.org/system/files/nsdi25-li-yang.pdf (S1-14) | arXiv 2601.20435 (user-space oversubscription scheduling, not games); WPC 2302.12954 (generic) |
| 5 | 2026-09-13 | WebSearch | `Proton Wine DXVK Linux gaming performance evaluation paper arXiv thread` | none academic | all hits are news/guides |
| 6 | 2026-09-13 | WebSearch | `"game" "thread" characterization PC games multithreaded CPU utilization "frame time" IEEE workload characterization study` | none academic | forum posts, NVIDIA blog, patents |
| 7 | 2026-09-13 | WebFetch | lwn.net/Articles/1051430/ ; lwn.net/Articles/991205/ ; lpc.events/event/19/sessions/229/ | fetched; then curl'd own HTML copies | sched_ext MC page lists no attachments |
| 8 | 2026-09-13 | WebSearch | `lpc.events 2025 "Gaming on Linux" microconference contributions frame pacing gamescope Proton` | lpc.events/event/19/sessions/225 (Gaming MC page, S1-lpc25-gaming-mc) | gamescope guides (S2/blog territory) |
| 9 | 2026-09-13 | WebSearch | `"Big or Little" mobile interactive applications asymmetric multi-core IISWC game threads Seo` | jaehyuk-huh.github.io/papers/seo_iiswc15.pdf (S1-10) | — |
| 10 | 2026-09-13 | WebSearch | `Android game "render thread" "main thread" frame deadline CPU scheduling paper MobiSys OR MobiCom OR ASPLOS OR EuroSys 2022 2023 2024 games frame drops` | arxiv.org/abs/2607.18097 SuperPass (S1-12); ipads.se.sjtu.edu.cn …/WuASPLOS25.pdf D-VSync (S1-13) | Android developer docs (S2 territory); patents |
| 11 | 2026-09-13 | WebSearch | `nsdi25 li-yang mobile cloud gaming VSync frame pipeline paper` | usenix nsdi25-li-yang.pdf (S1-14) | — |
| 12 | 2026-09-13 | WebFetch | lpc.events/event/19/sessions/225/ | seven Gaming MC contributions listed; page itself shows no attachment URLs; later curl of contribution pages found attachments (row 27) | — |
| 13 | 2026-09-13 | WebSearch | `Changwoo Min LAVD talk slides Kernel Recipes OR FOSDEM OR XDC OR "OSPM" 2025 "scx_lavd" pdf` | lwn.net/Articles/1021332 (OSPM 2025 day two, S1-04); lwn.net/Articles/1078696 (OSPM 2026 day two, S1-08) | no OSPM slide PDF located (retis.sssup.it summit page not listing slides in search results) |
| 14 | 2026-09-13 | WebSearch | `thesis "Proton" "Steam Play" Wine DXVK performance overhead Linux Windows games comparison bachelor OR master thesis pdf` | none | news only |
| 15 | 2026-09-13 | WebSearch | `"game engine" thread-level parallelism characterization paper IISWC OR ISPASS "Unreal" OR "Unity" threads per frame CPU study` | none on-topic | diva-portal "parallel design patterns" thesis (design, not measurement); Rochester TM paper (2009, simulation) |
| 16 | 2026-09-13 | WebSearch | `"frame limiter" OR "frame rate cap" latency measurement paper VSync input latency academic study games` | cse.wustl.edu/~jain/cse567-15/ftp/vsync.pdf (S1-15, course study, not peer-reviewed) | Blur Busters / wccftech (non-academic) |
| 17 | 2026-09-13 | WebSearch | `Igalia blog LAVD scheduler Steam Deck Changwoo Min gaming workload characterization "Terraria" OR "Cyberpunk" OR "Counter-Strike" tasks` | lpc.events/event/18/…/scx_lavd-lpc-mc-24.pdf (S1-02); igalia.com/downloads/slides/ChangwooMin-TheCurrentStatusAndFutureDirectionOfTheLAVDScheduler.pdf (S1-07) | igalia.com news posts (announcements, no data) |
| 18 | 2026-09-13 | WebSearch | `"sched_ext" OR "sched-ext" arXiv paper 2025 2026 evaluation games frame rate BPF scheduler latency-critical` | none with game measurements | arXiv 2511.11628 (Mixture-of-Schedulers) and 2509.01245 (sched-agent) cite LAVD but have no game characterisation (abstracts only checked via search snippets; not downloaded) |
| 19 | 2026-09-13 | WebSearch | `mobile game performance characterization paper "frame" "threads" CPU GPU "critical path" MICRO OR ISCA OR HPCA OR IISWC 2021 2022 2023 "mobile games"` | Peters et al. ICCD 2016 identified (row 24) | DAC 2015 power modelling (abstract only, not pursued) |
| 20 | 2026-09-13 | WebSearch | `"wineserver" scholar paper Wine architecture threads synchronization "futex" ntsync evaluation` | none academic | Phoronix/blogs only |
| 21 | 2026-09-13 | WebSearch | `"Steam Deck" academic paper measurement frame time power "refresh rate" OR "frame limiter" arXiv OR IEEE OR ACM` | none academic | consumer guides |
| 22 | 2026-09-13 | WebSearch | `dblp "video game" OR "game engine" workload characterization multicore threads "thread-level parallelism" PC games paper 2008..2020` | Blake et al. ISCA 2010 (dblp record) | — |
| 23 | 2026-09-13 | WebSearch | `Blake Dreslinski Mudge Flautner "Evolution of thread-level parallelism in desktop applications" ISCA 2010 pdf games threads` | tnm.engin.umich.edu 2014 Gao et al. ISPASS poster PDF (S1-11) | no open copy of the Blake paper found; ACM DL paywalled |
| 24 | 2026-09-13 | WebSearch | `"Frame-based and thread-based power management for mobile games on HMP platforms" ICCD 2016 pdf` | ieeexplore 7753277; mediatum.ub.tum.de/doc/1430017 | TUM mediatum served a bot-check page instead of the PDF; IEEE page fetch returned no content; Semantic Scholar and CrossRef return no abstract (publisher-elided). Not read. |
| 25 | 2026-09-13 | WebSearch | `OSPM 2025 scx_lavd Changwoo Min "What can EEVDF learn" slides pdf retis` | LWN 1021332 already held; YouTube video | no slide PDF |
| 26 | 2026-09-13 | WebSearch | `blogs.igalia.com changwoo LAVD scheduler gaming workload post` | nothing new | — |
| 27 | 2026-09-13 | curl | lpc.events/event/19/contributions/{2108,2109,2149,2150,2286,2287,2293}/ | 2109 Peri "Level Up Your Game" attachment (S1-09); 2293 Bossbaly "Resource management on embedded gaming devices" attachment (read: memory cgroup policy, no task/frame observations; copy deleted) | 2286/2287 no attachments |
| 28 | 2026-09-13 | WebSearch | `paper "critical path" analysis game frame CPU threads ETW OR "Event Tracing for Windows" "frame time" characterization Windows games study` | none academic | Microsoft PIX/WPA docs (tool docs, not observations) |
| 29 | 2026-09-13 | WebSearch | `academic study Proton compatibility layer Windows games Linux "frame time" OR "frames per second" comparison journal OR conference 2021..2026` | Kopel & Bożek, ICCCI 2023 "Is Proton Good Enough?" identified | Springer chapter redirects to IdP; ACM DL returns a 5.7 kB block page; springerprofessional page has no abstract text; Semantic Scholar/CrossRef abstract publisher-elided. Not read — no quotable passage. |
| 30 | 2026-09-13 | WebSearch | `"Evolution of thread-level parallelism in desktop applications" filetype:pdf` | cse.wustl.edu/~roger/566S.s21/… PDF | that file is a 2021 student presentation about the paper, not the paper; deleted |
| 31 | 2026-09-13 | WebSearch | `game "short-lived threads" OR "thread creation" per frame trace study threads created terminated during gameplay measurement paper` | none | patents, forum posts |
| 32 | 2026-09-13 | WebSearch | `empirical study mobile game performance Perfetto threads "main thread" "render thread" Unity Unreal Android paper 2023 2024 2025 frame drops characterization` | none new | blogs, Android docs |
| 33 | 2026-09-13 | Semantic Scholar API / CrossRef API | DOI 10.1109/ICCD.2016.7753277 ; DOI 10.1007/978-3-031-41456-5_48 | metadata only (JSON saved) | abstracts elided by publisher |

## 2. Candidates

### S1-01 — Min, "Optimizing Scheduler for Linux Gaming", Open Source Summit North America 2024 (slides)

- **Citation.** Changwoo Min (Igalia). *Optimizing Scheduler for Linux Gaming.* Slides, Open Source Summit North America, April 17, 2024. 30 slides.
- **Copy read.** URL `https://static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf`; PDF metadata title `scx-lavd-oss-na24`; version: the file as served on 2026-09-13; local `sources/S1-min-ossna24/scx-lavd-oss-na24.pdf` (+ `.txt`); SHA-256 `e62d69cd401021f8bfedadde2c4de62b01383facaa83acce7d218af3b6402475`.
- **Passages.**
  - Slide 4: "SteamDeck runs x86 Windows games! ● AMD APU ○ AMD Van Gogh: x86 8-core CPU + AMD GPU ● SteamOS ○ Arch-Linux based Linux distribution ○ with optimizations for SteamDeck hardware (especially AMDGPU) ● Proton ○ Compatibility layer for Windows games on Linux ○ Includes patched version of Wine ○ Plus a lot more: DXVK, VKD3D, gstreamer, ffmpeg"
  - Slide 10: "We collect and analyze all scheduling activities while playing games."
  - Slide 11 (title only, figure): "Analyzed a lot of scheduling traces"
  - Slide 12: "Task scheduling and CPU utilization ● Around 300 tasks are scheduled while running a game. ○ Around 90% are long-living tasks; only 10% of tasks are terminated. ● Top 30-40 most frequently scheduled tasks take 95% of scheduling. ○ Around half of them are system tasks -- especially, wine, graphics, and audio servers , taking 30--40% of scheduling. ○ There are 15-20 game-specific tasks, which takes 60-70% scheduling. ● CPU utilization is moderately high -- around 65-95%, but not overloaded (i.e., no 100%)."
  - Slide 13: "Task execution time per schedule ● In general, tasks run for very short duration – roughly a few 100s usec on average to a few msec maximum. ● Task execution time is very stable and is predictable using its average. Distribution of task's runtime average per schedule in a game tasks runtime avg (msec) ○ Some coordination tasks run very shortly (e.g., wineserver:260 usec) but some work tasks (e.g., a task worker: 1.65 msec) run longer than average. < 1 msec"
  - Slide 14: "What makes scheduling happen? ● Preemption (e.g., timer interrupt) takes only 25-30% of scheduling. ● 70-75% of scheduling is initiated by waiting system calls – such as epoll, pipe_read, futex_wait , etc. ● In this case, a task is first scheduled out waiting for an event then it is scheduled in when the event is notified. Call stacks which triggered scheduling in a game"
  - Slide 15: "Task waiting time ● Wait time from one schedule to another schedule is a task's behavioral property. Each task's wait time is pretty constant. Wait times over time in a game"
  - Slide 16: "Tasks are tightly linked in a graph ● Task graphs of top 50 percentile of waiter-wakers"
  - Slide 17: "● Majority of game tasks shows periodic behavior ○ given the fact that a task has a stable execution time and a stable wait time. ● A sequence of tasks serves for a single job (e.g., from a user input to display update). ● Therefore, the accumulated scheduling delay in a task chain will affect end-user's experience; it would eventually result in a sudden spike of frame time (low 1% FPS)."
  - Slide 29: "Early result is promising ● In many cases, LAVD provides better or similar performance than EEVDF in terms of average FPS and Low 1% FPS LAVD EEVDF 6.9-rc1 upstream kernel"
- **Coverage.**
  - T1: does not cover (no frame period, refresh, limiter or VSync statement; slide 17 links task-chain delay to "a sudden spike of frame time" qualitatively only).
  - T2: covers. Object: tasks scheduled "while running a game" (slide 12), i.e. all tasks system-wide, not only the game process. Units/statistics: task count (~300); share of scheduling events by top 30–40 tasks (95%); split of those into "system tasks -- especially, wine, graphics, and audio servers" (about half, 30–40% of scheduling) and "15-20 game-specific tasks" (60–70%); per-schedule runtime "a few 100s usec on average to a few msec maximum", with two named examples (wineserver 260 usec; "a task worker" 1.65 msec); trigger of scheduling (70–75% waiting syscalls: epoll, pipe_read, futex_wait; 25–30% preemption); wait time "pretty constant" per task; a waker–waitee task graph for the top 50th percentile (figure only, no numbers). Roles of `dxvk-cs`, `dxvk-submit`, `winepulse_*` are not named; `wineserver` is named once as a coordination task. Population: "a game" (slides 13–16 captions) — one game, unnamed.
  - T3: partial. Only the aggregate statement "Majority of game tasks shows periodic behavior" (slide 17) and the complement of slide 12 (the ~260 tasks outside the top 30–40 take 5% of scheduling). No per-task statistic for the non-dominant set.
  - T4: covers, one number. "Around 90% are long-living tasks; only 10% of tasks are terminated." (slide 12). Window not stated.
  - T5: does not name the machine, core count or game behind slides 12–14. Slide 4 names the Steam Deck's "AMD Van Gogh: x86 8-core CPU" as the platform LAVD targets; nothing ties the trace on slides 12–14 to that machine. Slide 29 names "6.9-rc1 upstream kernel" for the LAVD-vs-EEVDF comparison, not for the characterisation.
  - T6: does not cover.
- **One observation?** The slide captions say "in a game" (singular) for slides 13, 14, 15; slide 12 says "while running a game". Reads as one population/trace per figure; whether the figures come from the same run is not stated. Machine: not named. Game: not named. Window: not named.

### S1-02 — Min, "Using sched_ext to improve frame rates on the SteamDeck", LPC 2024 sched_ext MC (slides)

- **Citation.** Changwoo Min (Igalia). *Using sched_ext to improve frame rates on the SteamDeck — Ideas behind the LAVD scheduler.* Slides, Linux Plumbers Conference 2024, sched_ext microconference, September 18, 2024. 20 slides.
- **Copy read.** URL `https://lpc.events/event/18/contributions/1713/attachments/1425/3058/scx_lavd-lpc-mc-24.pdf`; local `sources/S1-min-lpc24/scx_lavd-lpc-mc-24.pdf` (+ `.txt`); SHA-256 `77c9cefec98e0346d5b89a219ca30eff7cb4f448016b24fa0871b286ba421eb4`.
- **Passages.**
  - Slide 5: "Top 50% of waiters and wakers … Understanding game workloads ● Tasks run for very short duration ○ roughly a few 100s usec on average ● Multiple tasks are tightly linked to in a task graph to finish a single job (e.g., updating a frame). Distribution of task's runtime average per schedule in a game tasks runtime avg (msec) < 1 msec"
  - Slide 6: "Scheduling delay in a critical path of a task graph will significantly amplify the scheduling latency."
  - Slide 10: "a fixed time interval == targeted latency (e.g., 15 msec)"
  - Slide 13: "Core compaction ● Let's run minimal number of core in an optimal frequency range. ○ Run 16-cores in 5% CPU utilization for each vs. ○ Run 2-cores in 40% CPU utilization for each ○ around 50% fits well in Intel & AMD processors"
  - Slide 15: "Medium load (<70%) ○ Usage:running a casual game, a kernel module compilation … Heavy load (>70%) ○ Usage: running a AAA game, full kernel compilation"
  - Slide 17: "Performance Comparison with EEVDF ● FH5 in-game benchmark with background recording on SteamDeck OLED LAVD EEVDF 1419.49 J (15.4 W) 1423.75 J (15.5 W)"
  - Slide 18: "● Tomb Raider in-game benchmark without background task on SteamDeck OLED LAVD EEVDF 752.83 J (10.7 W) 896.07 J (12.7 W)"
- **Coverage.** T1: does not cover. T2: partial — repeats the runtime-per-schedule distribution figure of S1-01 slide 13 ("in a game", "a few 100s usec on average") and the top-50% waker/waiter graph; no counts or roles. T3, T4: do not cover. T5: names machine and games only for the LAVD-vs-EEVDF energy comparison ("SteamDeck OLED", "FH5", "Tomb Raider", slides 17–18); does not state the machine, core count or game of the characterisation figure (slide 5). T6: does not cover.
- **One observation?** Slide 5 figure: "in a game", unnamed; machine and window not named.

### S1-03 — Corbet, "Sched_ext at LPC 2024", LWN.net

- **Citation.** Jonathan Corbet. *Sched_ext at LPC 2024.* LWN.net, September 26, 2024. https://lwn.net/Articles/991205/
- **Copy read.** HTML as served 2026-09-13; local `sources/S1-lwn-991205/lwn-991205.html` (+ `.txt`); SHA-256 `0ba6ea8e0eb2f19eccf37ce6dad6bd1a99a74a48d5f9af3f799a1f0e810e5f22`.
- **Passages.** (section "Higher frame rates")
  - "The goal behind this scheduler was to provide the best gaming experience on Linux in general — not just on the Steam Deck."
  - "A key aspect of gaming workloads is that tasks tend to run quickly, typically no more than 100µs at a time. There are a lot of tightly linked tasks, though, and performance depends on the most critical of those tasks running in the necessary sequence; that is the critical path."
  - "Min concluded by saying that, for gaming applications, scx_lavd consistently enables higher frame rates than the EEVDF scheduler while using (slightly) less power and with fewer stutters."
- **Coverage.** T1: does not cover. T2: one reported statistic ("typically no more than 100µs at a time"), which differs from the slide it reports (S1-02 slide 5: "a few 100s usec on average"); the reporter's paraphrase, no population named. T3, T4: do not cover. T5: does not name machine, core count or game. T6: does not cover.
- **One observation?** Not an observation; a talk report.

### S1-04 — Reports from OSPM 2025, day two — section "What can EEVDF learn from a special-purpose scheduler? The case of scx_lavd", LWN.net

- **Citation.** LWN.net, *Reports from OSPM 2025, day two*, section by Changwoo Min (speaker) as written up in the OSPM 2025 report, published 2025 (article 1021332). https://lwn.net/Articles/1021332/
- **Copy read.** HTML as served 2026-09-13; local `sources/S1-lwn-1021332/lwn-1021332.html` (+ `.txt`); SHA-256 `291adf08a0778992fdbfb5f9652a5abfe57ccc3a5c985cf9d8adaf7ead9bec9e`.
- **Passages.**
  - "He clarified that the main target applications are unmodified Windows games running on the Proton/Wine layer, so it is hard to expect additional latency hints from the application."
  - "Games are communication-intensive; 10-20 tasks are easily involved in finishing a single job (such as updating the display after a button press), and they communicate through primitives such as futexes, epoll, and NTSync. A scheduling delay among one of the tasks can cause cascading delay and latency (frame time) spikes."
  - "Min answered that it simply measures the frequencies without distinguishing individual wakers and wakees, so it is pretty cheap. Those frequencies are decayed using the standard exponential weighted moving average (EWMA) technique, converging very quickly (a few hundreds of milliseconds) in practice."
  - "Min showed a video demo, of a game that achieves high, stable frame rates while running a background job."
  - "He is particularly interested in the system being under-utilized (say 20-30% CPU utilization) for running an old, casual game."
- **Coverage.** T1: does not cover. T2: one number — "10-20 tasks are easily involved in finishing a single job", and the wake primitives named (futexes, epoll, NTSync). T3, T4: do not cover. T5: does not name the machine, core count or game of the characterisation; the demo game is unnamed. T6: does not cover.
- **One observation?** Talk report; no trace identified.

### S1-05 — Min, "Steps Towards a Gaming-Optimized Scheduler", LPC 2025 Gaming on Linux MC (slides)

- **Citation.** Changwoo Min (Igalia). *Steps Towards a Gaming-Optimized Scheduler.* Slides, Linux Plumbers Conference 2025, Gaming on Linux microconference, Tokyo, December 13, 2025. 15 slides.
- **Copy read.** URL `https://lpc.events/event/19/contributions/2150/attachments/1951/4162/Steps_Towards_a_Gaming_Optimized_Schedule-lpc2025.pdf`; local `sources/S1-min-lpc25/Steps_Towards_a_Gaming_Optimized_Schedule-lpc2025.pdf` (+ `.txt`); SHA-256 `e478aa851e39c1d01e94e3b7bcbecaaf51310107c801b6c1821015ff57267059`. (Igalia hosts a byte-identical copy at `https://www.igalia.com/downloads/slides/ChangwooMin-StepsTowardsaGamingOptimizedScheduler.pdf` per the search hit; not separately verified.)
- **Passages.**
  - Slide 2: "○ Primary target: Windows games running on Linux (SteamOS) ○ Implemented based on the sched_ext framework (BPF + Rust)"
  - Slide 6: "● We developed an analysis tool, VaporMark ○ https://github.com/Igalia/vapormark ● VaporMark collects all the scheduling activities during a period using "perf sched record" ● Then, it analyzes the collected trace to understand high-level properties."
  - Slide 8: "Key finding: task graph, waker-wakee ● To accomplish a single high-level job (e.g., moving a character upon a keypress event), many tasks should tightly collaborate. ● Task graphs of top 50 percentile of waker-wakees ● Let's prioritize a task with high waker-wakee frequency! ○ Those tasks are in the middle of the task chain."
  - Slide 10: "● Thankfully, some games provide in-game benchmarks! ○ E.g., Cyber Punk 2077, Far Cry, Forza Horizon, etc. ● Or, some games allow to replay the recorded game sequences. ○ E.g., Counter Strike"
  - Slide 14: "● LAVD also partially addresses the problem. ○ Handles only futex, which is a building block of user-space locks. ● What about NTsync? ○ NTsync is a support driver for emulation of NT synchronization primitives by user-space NT emulators."
- **Coverage.** T1: does not cover. T2: names the collection method ("perf sched record" via VaporMark) and restates the waker–wakee graph; no counts. T3, T4: do not cover. T5: does not name the machine, core count or game behind the characterisation; the games on slide 10 are named as benchmark candidates, not as the trace source. T6: does not cover.
- **One observation?** Slide 7 shows a "VaporMark analysis report" figure whose text did not extract; no population named.

### S1-06 — Edge, "Lessons from creating a gaming-oriented scheduler", LWN.net (report of S1-05's session)

- **Citation.** Jake Edge. *Lessons from creating a gaming-oriented scheduler.* LWN.net, January 7, 2026. https://lwn.net/Articles/1051430/ (CC BY-SA 4.0).
- **Copy read.** HTML as served 2026-09-13; local `sources/S1-lwn-1051430/lwn-1051430.html` (+ `.txt`); SHA-256 `172d4d5e8e4a347a0dead826b684a728559f4db2ae918811e07bb4b4127f4d31`.
- **Passages.**
  - "Min said that he has been developing LAVD as part of his work at Igalia on SteamOS and the Steam Deck."
  - "For games, there are usually multiple tasks, but some of them can be run on the slower, more energy-efficient cores. Most of the tasks are fairly short running, around 1ms, though there are a few that run for 2-3ms or more. There are also tasks that run for less than 100µs, which means there is more flexibility in terms of their task placement, he said."
  - "So he developed VaporMark—the name refers to Steam—which analyzes data collected using "perf sched record". "After collecting huge amounts of data, post-processing it for an hour or two, it shows some reports.""
  - "The key finding that came out of his analysis is perhaps somewhat obvious: a single high-level action, such as moving a character on-screen and emitting a sound based on a key-press event, requires that many tasks work together. Some of the tasks are threads in the game process, but others are not because they are in the game engine, kernel, and device drivers; there are often 20 or 30 tasks in a chain that all need to collaborate."
  - "For example, a game may run smoothly most of the time, but have a latency spike every five minutes or so that results in a drop in the FPS rate."
  - "Vernet noted that some games, such as Civilization VI, have CPU-intensive tasks that may need to be handled differently."
  - "Fortunately, some games, such as Cyberpunk 2077, Far Cry, and Forza Horizon, have an in-game benchmark, which is useful; others, like Counter-Strike, allow replaying recorded game sequences, which also helps."
  - "for example, some users have complained that LAVD does not work well with the games using the Unreal engine."
  - "Most of the tasks in a Windows game are short-running and computation-intensive, so it is important to avoid situations where locking prevents a task from quickly completing."
  - "An attendee asked whether LAVD used the same scheduler for all games on the Steam Deck. Min said that LAVD is a single scheduler, though there are some tuning knobs that can be changed with command-line parameters."
- **Coverage.** T1: does not cover (frame period not discussed; only "a latency spike every five minutes or so"). T2: partial — per-schedule runtime bands as reported ("around 1ms", "2-3ms or more", "less than 100µs"), chain length "20 or 30 tasks", and the statement that chain members include threads outside the game process ("game engine, kernel, and device drivers"). No counts of the population. T3, T4: do not cover. T5: names "SteamOS and the Steam Deck" as the development context and "Windows games" as the workload class; does not name the machine, core count or game behind the characterisation slides. T6: does not cover.
- **One observation?** Talk report; the numbers are reported speech, populations unnamed.

### S1-07 — Min, "The Current Status and Future Direction of the LAVD Scheduler", LPC 2025 sched_ext MC (slides)

- **Citation.** Changwoo Min (Igalia). *The Current Status and Future Direction of the LAVD Scheduler.* Slides, Linux Plumbers Conference 2025, sched_ext microconference, December 12, 2025. 21 slides. PDF metadata title `scx_lavd-lpc2025`.
- **Copy read.** URL `https://www.igalia.com/downloads/slides/ChangwooMin-TheCurrentStatusAndFutureDirectionOfTheLAVDScheduler.pdf`; local `sources/S1-min-igalia-status/ChangwooMin-TheCurrentStatusAndFutureDirectionOfTheLAVDScheduler.pdf` (+ `.txt`); SHA-256 `1393c9d8ebd39adb01bc885e374bd0f34ada015b7a2ff41ac8c98b47b6d81974`.
- **Passages.**
  - Slide 3: "● Aimed for better gaming experience on Linux ○ Target application: unmodified Windows games running on Linux ○ Target hardware: SteamDeck (x86 AMD CPU) ● Inspired by the characteristics of gaming workloads ○ Many tasks interact with each other to complete a single high-level job (e.g., moving a game character upon a key press). ○ Tasks in task graphs communicate heavily (i.e., wake-up) with each other."
  - Slide 12: "/sys/kernel/debug/energy_model ├── cpu0 # Efficiency core (x2) … ├── cpu2 # Performance core (x3) … ├── cpu5 # Performance core (x2) … └── cpu7 # Prime core (x1)"
  - Slide 16: "Experimental Results ● On a Snapdragon development board. ● EEVDF ○ FPS: around 50 ○ CPU utilization ● LAVD ○ FPS: around 57, energy-rate: smaller than EEVDF"
  - Slide 20: "● Extend the coverage of LAVD to large servers ○ 8 cores ⇒ 100+ cores ○ A single LLC domain ⇒ 10+ LLC domain"
  - Slide 21: "Image credits https://store.steampowered.com/app/253230/A_Hat_in_Time/ https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice__GOTY_Edition/"
- **Coverage.** T1, T2, T3, T4: do not cover (no trace statistics). T5: names the *target* hardware ("SteamDeck (x86 AMD CPU)") and a later experiment machine ("a Snapdragon development board", 8 CPUs by the energy-model listing); "8 cores ⇒ 100+ cores" describes the current scope. None of this is tied to the OSS NA 2024 characterisation slides. Two game store pages appear only as image credits (slide 21), not as trace sources. T6: does not cover.
- **One observation?** Slides 16–17 are two runs on one Snapdragon board with an unnamed game.

### S1-08 — Reports from OSPM 2026, day two — section "Evolving sched_ext: resource control, topology awareness, and energy efficiency for modern systems", LWN.net

- **Citation.** LWN.net, *Reports from OSPM 2026, day two* (article 1078696), section on the joint talk by Changwoo Min and Gavin Guo, 2026. https://lwn.net/Articles/1078696/
- **Copy read.** HTML as served 2026-09-13; local `sources/S1-lwn-1078696/lwn-1078696.html` (+ `.txt`); SHA-256 `e626fdf0e0ff12adf239511b81c6d321cb7ef2915b65cb803cb1a3c85682c95f`.
- **Passages.**
  - "When Min first presented scx_lavd at OSPM 2025, it was a gaming-focused scheduler aimed at improving Windows games running on Linux through SteamOS, with waker/wakee frequency as its primary hint for task urgency. A year later, the project is broader, expanding scx_lavd into a potential default fleet scheduler, and that expansion has highlighted two parts of the scheduling problem."
  - "Min showed results from a 2-socket, 96-core AMD EPYC machine (192 CPUs)"
- **Coverage.** T1–T4: do not cover. T5: does not name the characterisation machine or game; the 96-core EPYC is the cpu.max experiment machine, not gaming. T6: does not cover.

### S1-09 — Peri, "Level Up Your Game: OS Kernel and Game interactions revealed with Perfetto", LPC 2025 Gaming on Linux MC (slides)

- **Citation.** Ramesh Peri (Meta). *Level Up Your Game: OS Kernel and Game interactions revealed with Perfetto.* Slides, Linux Plumbers Conference 2025, Gaming on Linux microconference, December 13, 2025. 24 slides.
- **Copy read.** URL `https://lpc.events/event/19/contributions/2109/attachments/1955/4167/Level%20Up%20Your%20Game_%20OS%20Kernel%20and%20Game%20interactions%20revealed%20with%20Perfetto.pdf`; local `sources/S1-peri-lpc25/peri-perfetto-lpc2025.pdf` (+ `.txt`); contribution page copy `sources/S1-lpc25-gaming-mc/contrib-2109.html`; SHA-256 (PDF) `eec6040b7170449f535c46041763a01437ac351bd742319b53337c43ab4a87fa`.
- **Passages.**
  - Slide 2: "Traces are collected on Pixel8 running angry birds"
  - Slide 3: "Games vs. Apps Game Normal App Repetitiveness Every Frame Usually not repetitive Realtime Yes No Latency Sensitivity Yes No Memory Usage Spiky Uniform Kernel Impact Kernel scheduler, interrupts,tick rates, migrations, affinity, IRQs Minimal Scheduler Quantum In milliseconds In seconds"
  - Slide 5: "Perfetto config to collect data OS scheduler events irq/softirq entry exits The overhead is reasonably low with these events - around 2-3%"
  - Slide 6: "Overall Performance 10 secs of wall time across 9 cores 41.48sec out of 90 secs - 46% utilization"
  - Slide 7: "Frame time Here 16.6 ms which is 60FPS Main process com.rovio.baba's UnityMain thread shows the frame time"
  - Slide 8: "4.05 secs in IRQs and softIRQs 41.48 secs of cpu time Total time on user threads is 41.48-4.05 = 37.43 secs"
  - Slide 10: "Thread wakeups and their reasons Audio thread woken by surfaceflinger In reality audio thread woken by arch timer interrupt cpu3 in interrupt handler Interrupt handler wakes up audio writer thread"
  - Slide 11: "OS scheduler time is distributed across many small time slots and can be up to 15% of total execution time"
- **Coverage.** T1: covers for Android, not Proton/Linux desktop — frame period 16.6 ms (60 FPS) read from the game's `UnityMain` thread in a Perfetto trace; what governs it (display refresh vs. limiter) is not stated. T2: partial, Android — a 10 s trace on 9 cores, 46% utilization, IRQ/softIRQ share, one wake relation (audio thread woken by surfaceflinger / arch timer interrupt); no thread count, no per-schedule runtime distribution. T3, T4: do not cover. T5: not applicable. T6: does not cover.
- **One observation?** Yes: one trace, machine named (Pixel 8), game named (Angry Birds, package `com.rovio.baba`), window named (10 s wall time).

### S1-10 — Seo, Im, Choi, Huh, "Big or Little: A Study of Mobile Interactive Applications on an Asymmetric Multi-core Platform", IISWC 2015

- **Citation.** Wonik Seo, Daegil Im, Jeongim Choi, Jaehyuk Huh. *Big or Little: A Study of Mobile Interactive Applications on an Asymmetric Multi-core Platform.* IEEE International Symposium on Workload Characterization (IISWC), 2015. IEEE Xplore document 7314142. 11 pages.
- **Copy read.** Author copy `https://jaehyuk-huh.github.io/papers/seo_iiswc15.pdf`; local `sources/S1-seo-iiswc15/seo_iiswc15.pdf` (+ `.txt`); SHA-256 `420eac2252ec88bef8f96194770c8bb1a9961b363429e9adf95ce405379932a7`.
- **Passages.**
  - §II (p. 2): "we use Galaxy S5 as our target device, with the Exynos 5422 CPU which includes four ARM Cortex-A7 cores (little core), four ARM Cortex-A15 cores (big core), and a GPU."
  - §II (p. 2): "The target system runs Android 4.4.2. The default asymmetric scheduler is the HMP (Heterogeneous Multi-Processing) scheduler derived from the Linaro system."
  - Table II (p. 2): "Angry Brid Shooting game with physics engine FPS / Eternity Warriors 2 3D action RPG game FPS / FIFA 15 3D sport game FPS"
  - §V.A, Table III "THREAD-LEVEL PARALLELISM WITH 8 CORES" (p. 6), columns "App Name Idle Little Big TLP": "Angry Brid 4.41 99.88 0.11 2.34 / Eternity Warrior 2 3.65 72.64 27.35 2.85 / FIFA 15 9.27 85.62 14.37 2.37"
  - §V.A (p. 6): "The last column, TLP, shows the average number of active cores (both little and bit cores) when the processor is not completely idle. We use the same metric as proposed by Blake et al. for TLP [27]." … "All of the benchmark applications, except for bbench, have less than 3 cores active on average."
- **Coverage.** T1: does not cover (FPS is the metric, values per game not quoted here as frame period). T2: partial, Android 2015 — per-game TLP (average active cores during non-idle cycles) and idle/little/big cycle shares for three named games; no thread counts, wake graph or per-schedule runtime. T3, T4: do not cover. T5: not applicable. T6: does not cover.
- **One observation?** One device (Galaxy S5, Exynos 5422, 8 cores), three named games; window not quoted.

### S1-11 — Gao, Gutierrez, Dreslinski, Mudge, Flautner, Blake, "A Study of Thread Level Parallelism on Mobile Devices", ISPASS 2014 (2-page poster paper)

- **Citation.** Cao Gao, Anthony Gutierrez, Ronald G. Dreslinski, Trevor Mudge, Krisztian Flautner, Geoffery Blake. *A Study of Thread Level Parallelism on Mobile Devices.* IEEE ISPASS 2014, pp. 126–127 (page numbers per footer "126" and ISBN "978-1-4799-3606-9/14").
- **Copy read.** `https://tnm.engin.umich.edu/wp-content/uploads/sites/353/2017/12/2014.03.A-Study-of-Thread-Level-Parallelism-on-Mobile-Devices.pdf`; local `sources/S1-gao-ispass14/gao-ispass14-tlp-mobile.pdf` (+ `.txt`); SHA-256 `1030f3d05f48239fe8c8e7814cf192d0cdbda22fe8559756e2463210f4dc57ad`.
- **Passages.**
  - Abstract (p. 1): "Our results demonstrate that mobile applications are utilizing less than 2 cores on average"
  - §III (p. 1): "for a 4-core system, on average, we see a TLP of 1.4. The applications with high TLP, namely Games, Browser and Navigation, have TLPs around 1.5 to 1.6."
- **Coverage.** T2: partial, Android, category-level ("Games" TLP 1.5–1.6 on a 4-core board); no counts or wake structure. T1, T3, T4, T5, T6: do not cover.
- **One observation?** Category aggregate; individual games, boards and windows not quoted in the 2-page version.

### S1-12 — Li, Liang, Pan, Sun, Guan, Kuo, Xue, "SuperPass: Fast-Tracking Blocking Threads to Mitigate Priority Inversion on Mobile Devices", arXiv 2607.18097

- **Citation.** Lei Li, Yu Liang, Riwei Pan, Youcheng Sun, Nan Guan, Tei-Wei Kuo, Chun Jason Xue. *SuperPass: Fast-Tracking Blocking Threads to Mitigate Priority Inversion on Mobile Devices.* arXiv:2607.18097 (PDF created 2026-07-22). 14 pages.
- **Copy read.** `https://arxiv.org/pdf/2607.18097`; local `sources/S1-superpass-2607.18097/2607.18097.pdf` (+ `.txt`); SHA-256 `881518e31a8eb58839b9ec44bff9b6b736e644dbbc7e6ad600d17a8c4f71013e`.
- **Passages.**
  - §2 (p. 3): "It initiates frame production (input callbacks, layout, and draw command recording) under a per-frame deadline set by the display refresh rate (e.g., 8.3 ms at 120 Hz). Blocking on this thread can miss the deadline and cause janky frames (dropped or delayed frames with visible stutter) [4, 5]."
  - §2.1 (p. 3): "We evaluate the UI threads of 16 popular applications on a Google Pixel 8. In each evaluation, we interact with one foreground app for one-minute interval, while 12 apps run concurrently in the background."
  - §2.1 (p. 3): "Figure 1a presents the 99.9th/99.99th percentile blocking durations with tail latencies up to ∼210 ms; … For example, Alipay reaches P99.99≈210 ms with ∼906 inversions exceeding 100 µs and 207 inversion blockings exceeding 1ms per minute."
  - §1 contributions list (p. 2): "We implement and evaluate SuperPass on a Google Pixel 8 (Linux 5.15, Android 14) and observe significant reductions in blocking duration and dropped frames in UI-thread instantiation compared to state-of-the-art"
- **Coverage.** T1: partial, Android — per-frame deadline = display refresh (8.3 ms at 120 Hz) stated as the governing quantity for the UI thread; no game. T2: partial — UI-thread blocking counts per minute for 16 apps (not games), on a named device. T3, T4, T5: do not cover. T6: does not cover.
- **One observation?** One device (Pixel 8), 16 apps, one-minute windows, ten repetitions.

### S1-13 — Wu, Du, Xu, Xia, Fu, Zang, Chen, "D-VSync: Decoupled Rendering and Displaying for Smartphone Graphics", ASPLOS 2025

- **Citation.** Yuanpei Wu, Dong Du, Chao Xu, Yubin Xia, Ming Fu, Binyu Zang, Haibo Chen. *D-VSync: Decoupled Rendering and Displaying for Smartphone Graphics.* ASPLOS '25, March 30–April 3, 2025, Rotterdam. DOI 10.1145/3669940.3707235. 16 pages (proceedings pp. 326–).
- **Copy read.** Author copy `https://ipads.se.sjtu.edu.cn/zh/publications/WuASPLOS25.pdf` (stamped "Downloaded from the ACM Digital Library on April 7, 2025"); local `sources/S1-dvsync-asplos25/WuASPLOS25.pdf` (+ `.txt`); SHA-256 `0d99200a2c4a42f1f135036ef7b0483d5fe980568c4d033a41f91df98f991b85`.
- **Passages.**
  - §1 (p. 1): "on state-of-the-art commercial smartphone (Mate60 Pro, 120Hz screen, OpenHarmony [23]). Many important cases like closing the notification center or clearing all notifications can only reach 95–105 FPS on the 120 Hz screen, causing noticeable stutters to users."
  - Figure 1 caption (p. 2): "Cumulative Distribution Function (CDF) of the frame rendering time (following the power law distribution). Most frames finish in one VSync period (78.3%). However, despite the support of triple buffering, approximately 5% of frames fail to finish on time, causing stutters."
  - §1 (p. 2): "We measured an average of 45.8 ms end-to-end rendering latency on Pixel 5, and 32.2 ms and 24.2 ms on Mate 40 Pro and Mate 60 Pro, respectively (§3.3)."
  - §2 (p. 3): "Smartphone screens update frames at a configured refresh rate, e.g., 60 Hz (or 120 Hz). Before every physical panel refresh, the screen generates a hardware VSync signal, marked HW-VSync, sending it to the rendering architecture via a hardware abstraction layer (HAL) every fixed 16.7 ms (or 8.3 ms)."
  - §2 (p. 3): "VSync pipeline. The end-to-end rendering procedure usually spans at least two VSync periods, following a pipeline structure illustrated in Figure 2."
  - Abstract (p. 1): "simulations of 15 mobile games show that compared to VSync, D-VSync on average reduces frame drops by 72.7%"
- **Coverage.** T1: covers for Android/OpenHarmony smartphones — the frame period is the display refresh (16.7 ms / 8.3 ms), the rendering pipeline spans ≥2 VSync periods, 78.3% of frames finish within one VSync period and ~5% miss. Not Linux desktop, not Proton. T2: does not cover at task level. T3, T4, T5: do not cover. T6: does not cover.
- **One observation?** Several devices named (Mate 60 Pro, Mate 40 Pro, Pixel 5); the CDF population ("real-world traces") is not named per game; the 15 games are simulated.

### S1-14 — Li, Qiu, Wang, Li, Qian, Yang, Lin, Liu, Xiao, Qin, Xu, "Dissecting and Streamlining the Interactive Loop of Mobile Cloud Gaming", NSDI '25

- **Citation.** Yang Li, Jiaxing Qiu, Hongyi Wang, Zhenhua Li (Tsinghua), Feng Qian (USC), Jing Yang (Tsinghua), Hao Lin (Tsinghua and UIUC), Yunhao Liu (Tsinghua), Bo Xiao, Xiaokang Qin (Ant Group), Tianyin Xu (UIUC). *Dissecting and Streamlining the Interactive Loop of Mobile Cloud Gaming.* 22nd USENIX NSDI, April 28–30, 2025, Philadelphia. ISBN 978-1-939133-46-5. https://www.usenix.org/conference/nsdi25/presentation/li-yang
- **Copy read.** `https://www.usenix.org/system/files/nsdi25-li-yang.pdf` (pypdf reports 8 pages in this copy); local `sources/S1-li-nsdi25/nsdi25-li-yang.pdf` (+ `.txt`); SHA-256 `2f2d505d150d8902de4e5f5037b66c2cf00165100bd992feb83a5b655fa3a8e9`.
- **Passages.**
  - §1 (p. 2): "the major latency of the cloud-side graphics pipeline does not lie in game rendering (23%), but the Vertical Synchronization (VSync) operations [2, 18, 53] (36%) in mobile OSes."
  - §1 (p. 2): "Given that graphics pipelines of mobile systems are designed to handle diverse workloads with power-constrained hardware and fixed-refresh-rate display [18], VSync is built into the Android graphics pipeline as a system-level always-on mechanism."
  - §1 (p. 2): "As shown in Figure 1, a game frame encounters as many as five VSync events, creating up to 83 ms extra latency. Given the periodicity of VSync events, even a slight network jitter (e.g., 1 ms) can lead to a frame deadline miss, resulting in a significant fluctuation (e.g., 13ms) in interactive latency."
- **Coverage.** T1: partial, Android in a cloud-gaming emulator — VSync as the frame-period governor with a five-stage VSync count and latency budget; not Linux desktop, not Proton. T2: does not cover at thread level (stages are pipeline components, not threads). T3, T4, T5: do not cover. T6: does not cover.
- **One observation?** One platform ("X-MCG"), games not named in the quoted passages; window not quoted.

### S1-15 — Tang (WUSTL CSE 567 course study, not peer-reviewed), "A Measurement Study of Vertical Synchronization Configurations in PC Video Games", 2015

- **Citation.** WUSTL CSE 567 (R. Jain) student project report, dated 5/6/2015, page header "A Measurement Study of Vertical Synchronization Configurations in PC Video Games."; data reference "[Tang15]". 9 pages. Not peer-reviewed; included because it is the only measurement document found for VSync vs. frame-cap on PC games.
- **Copy read.** `https://www.cse.wustl.edu/~jain/cse567-15/ftp/vsync.pdf`; local `sources/S1-wustl-vsync/vsync.pdf` (+ `.txt`); SHA-256 `14abd40ce4f8fcc229fa7cf2cc505da9ec5730b4c45f4952d0a8410c650f1a54`.
- **Passages.**
  - Abstract (p. 1): "The video games used in this study are Left 4 Dead 2, Super Meat Boy, and Sleeping Dogs. We conclude that fullscreen VSync with frame rate locking is the most balanced configuration, providing minimal input latency while maintaining VSync."
  - §2.2 (p. 2): "A typical computer monitor refreshes at 60 Hz, so a video game with VSync enabled will render at 60 FPS."
  - §2.3 (p. 2): "RadeonPro was used extensively in this study to override the VSync settings of the games under test. It was also used to enforce a 60 FPS frame rate cap."
  - §3 (p. 3): "The laptop's NVIDIA GT755M GPU is used to render frames from the video game." … "Because the laptop monitor refreshes at 60 Hz, input latency will be measured in terms of the number of screen refreshes between a keyboard keypress and the screen changing in response."
  - §4 (p. 5): "A quick visual analysis shows that enabling VSync in fullscreen without locking the frame rate has the most input latency, as much as 7.5 frames. Disabling VSync in fullscreen without locking the frame rate has the least input latency, with only 1.333 frames of latency."
- **Coverage.** T1: partial, Windows PC — VSync (60 Hz) vs. an external 60 FPS cap as frame-period governors, with input-latency consequences in frames; not Linux, not Proton; no task-wake linkage. T2–T5: do not cover. T6: does not cover.
- **One observation?** One laptop (GT755M, 60 Hz panel), three named games, menu-screen measurements, 30 keypresses per configuration.

### Identified but not read (no passage; listed so the gap is explicit)

- **Kopel, Bożek. "Is Proton Good Enough?" – A Performance Comparison Between Gaming on Windows and Linux.** ICCCI 2023, LNCS/LNAI 14162, DOI 10.1007/978-3-031-41456-5_48. Paywalled; no accessible abstract text (Springer IdP redirect, ACM DL block page, publisher-elided abstract in Semantic Scholar/CrossRef; JSON saved at `sources/S1-kopel-iccci23/semanticscholar.json`, SHA-256 `657d8247d7abca060f3f0fff5bfbf226d824797aa32acc6d093237497f4a84b8`). Likely relevant to T1 (Proton frame rates on named games); cannot be quoted.
- **Peters, Fuss, Park, Chakraborty. Frame-based and thread-based power management for mobile games on HMP platforms.** ICCD 2016, DOI 10.1109/ICCD.2016.7753277. Paywalled; TUM mirror bot-blocked; no abstract obtainable (JSON at `sources/S1-peters-iccd16/semanticscholar.json`, SHA-256 `462de83655d43c5290e7ae900deef3800f385e492652f2c0183b5e6d7b02fb7c`). Likely relevant to T2 (per-thread view of mobile games); cannot be quoted.
- **Blake, Dreslinski, Mudge, Flautner. Evolution of thread-level parallelism in desktop applications.** ISCA 2010, DOI 10.1145/1816038.1816000. No open copy found; the only "PDF" hit was a 2021 student presentation about the paper (discarded).

## 3. Not found

- **T1 for Proton on a Linux desktop or Steam Deck** — no peer-reviewed or preprint document found that states what governs the frame period under Proton (display refresh, frame limiter, uncapped), gives observed values, or ties frame cadence to task wakes. Searches 5, 14, 16, 21, 29. The only Proton paper found (Kopel & Bożek 2023) is paywalled and unquotable. Frame-period statements exist only for Android/OpenHarmony (S1-09, S1-12, S1-13, S1-14) and one Windows course study (S1-15).
- **T2 wake graph / per-schedule runtime for a Linux game with named Wine/DXVK/audio components** — only Changwoo Min's OSS NA 2024 slides (S1-01) give counts and a runtime distribution, naming `wineserver` (260 usec) and "a task worker" (1.65 msec); `dxvk-cs`, `dxvk-submit`, `winepulse_*` are not named in any document found. Searches 6, 15, 20, 28, 32.
- **T3 non-dominant tasks with numbers** — nothing beyond the complement of S1-01 slide 12 (top 30–40 tasks take 95% of scheduling) and the qualitative "majority of game tasks shows periodic behavior". Searches 31, 32.
- **T4 task termination during play** — only S1-01 slide 12 ("only 10% of tasks are terminated"), window unstated. Search 31.
- **T5 machine / core count / game behind OSS NA 2024 slides 12–14** — none of the eight Min/LWN documents read (S1-01 through S1-08) states it. The nearest statements are: target hardware "SteamDeck (x86 AMD CPU)" (S1-07 slide 3) and "AMD Van Gogh: x86 8-core CPU" as the Steam Deck's APU (S1-01 slide 4); development context "SteamOS and the Steam Deck" (S1-06); benchmark machines "SteamDeck OLED" with FH5 / Tomb Raider (S1-02 slides 17–18) and "a Snapdragon development board" (S1-07 slide 16); none is tied to the characterisation trace. OSPM 2025 slides were not located (search 25); the OSPM 2025 and LPC 2025 YouTube recordings were not transcribed.
