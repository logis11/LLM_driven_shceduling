# 9.16 claim audit — claims outside the workload dataset: blind re-read topics

The sample for the blind re-read of task 9.16's decision 1 (the claim audit), for the claims of `outside-inventory.md`. Each topic says what to look up, without the repository's wording, values or conclusions. A reader receives only the topic and the bibliographic entry, records the copy read (URL or commit, version, date, SHA-256), the verbatim passages and their locators, and only then is compared with the claims listed under "Claims" (which the reader is not shown).

## How the sample was drawn

Record names in the "Claims" lines: "R0N", "R10" are the 2026-09-13 independent reads (`_dev/research/jioh/2026-09-13-verification/reads/`), "K1", "K4" that verification's comparisons (`compare/`); "9.N Sk" is slice 9.N's search log k under `_dev/research/jioh/task-9.N-*/search/` (S1 literature, S2 project documentation and source, S3 traces and datasets, S4 CI observability); "decision Dn" is that slice changelog's entry n; the claim ids (A-69 …) are rows of `outside-inventory.md`.

**(a) Wording changed after its read: 28 claims, 20 topics.** A claim is in (a) when its current wording (the most recent commit adding a distinctive phrase, by `git log -S`) is newer than every record entry stating the same content — the read's access date, or a slice's changelog or audit entry quoting this content — and the change touched what the claim says (object, value, statistic, scope, population), not only its formatting. Most claims in the files were reworded by the 9.15 sweep (docs, memos and guidebook corrections) on 2026-10-14 to 2026-10-17; those whose new content a dated 9.11 or 9.12 decision entry already states, after the read, are not in (a).

**(b) Spot checks: two per slice, four claims.** Frame: the TRACED claims, not already in (a), whose record lies in the slice — task 9.11, the scheduler-side constants (41 claims), and task 9.12, the related-work and proposal prose (117 claims) — sorted by claim id. Drawn with Python's `random.Random(20261017).sample(frame, 2)`, 9.11 first. Drawn: 9.11 → B-26, B-01; 9.12 → A-62, A-25.

## (a) Wording changed after its read

### T-01 — Chambers et al., IMC 2005
- Topic: in the study of a busy Counter-Strike server's connection trace, the session-time analysis: which distribution the authors fit to session durations, its parameters and units, what share of sessions exceeds a stated length, and whether the paper itself states any central value (median or mean) of session time.
- Bibliographic entry: Chambers, C., Feng, W.-c., Sahu, S., & Saha, D. (2005). "Measurement-based Characterization of a Collection of On-line Games." Proc. IMC '05. www.usenix.org/legacy/event/imc05/tech/full_papers/chambers/chambers.pdf.
- Claims: A-69 (`docs/research-proposal.md:309`; wording `32a5c9dd` 2026-10-17; record 9.12 audit A2-12, 2026-10-09).

### T-02 — Fiedler's game loop, mpv's audio output, Chromium's fake audio worker
- Topic: (1) in the article, what a fixed-timestep game loop does when more real time has passed than one simulation step: how many simulation steps it runs, whether a limit applies and what it is, and how often it renders; (2) in mpv's audio output layer, what the output thread writes each time it wakes, how often it wakes, and what it does when the device buffer has run empty — whether audio due earlier is played later or dropped; (3) in Chromium's fake audio worker, what happens when a scheduled callback runs late — how many callbacks run and when the next is scheduled — and in which situation Chromium uses this fake output.
- Bibliographic entry: (1) Fiedler, G. "Fix Your Timestep!" *Gaffer On Games*, 2004-06-10, gafferongames.com/post/fix_your_timestep/. (2) mpv, `audio/out/buffer.c`, `audio/out/ao_null.c`, `osdep/threads-posix.h`, github.com/mpv-player/mpv tag `v0.37.0` (`818ce7c51a6b9179307950e919983e0909942098`). (3) The Chromium Authors, `media/base/fake_audio_worker.cc`, `media/audio/fake_audio_output_stream.cc`, `media/audio/audio_output_resampler.cc`, chromium.googlesource.com/chromium/src tag `152.0.7977.82` (`d04cdb24d67b081f6cf80200ffc5233f44b61109`).
- Claims: C-18 (research guidebook vol-01:3059; wording `e4ac1624` 2026-10-17), D-13 (vol-06:460; `e4ac1624` 2026-10-17); the only reads are the `docs/references.md` author's of 2026-10-06. The reader's record also serves as the missing record for B-32, B-33, B-34, E-18 and F-52.

### T-03 — Periodic tasks whose activation time has passed; rt-app's units
- Topic: what each of these does when a periodic task reaches its wait after its next activation time has already passed — accumulate, skip to a later activation, or re-anchor: rt-app's timer event in each of its modes and which mode is the default; interbench's emulated periodic loads; ROS 2's default executor's timers (the study below); the reference periodic thread of Lipari & Palopoli's notes; mpv's default video output. Also, in rt-app's documentation, the unit of every time quantity in a task description (run, sleep, timer period, deadline parameters, the global duration) and whether they are integers.
- Bibliographic entry: rt-app, github.com/scheduler-tools/rt-app, `doc/tutorial.txt` and `src/rt-app.c` at `d6f8be41`; Kolivas, C., interbench, github.com/ckolivas/interbench, `interbench.c` at `e612a65`; Teper, H., Bell, O., Günzel, M., Gill, C., & Chen, J.-J. "Bridging the Gap between ROS 2 and Classical Real-Time Scheduling for Periodic Tasks", arXiv:2408.03696v1, 2024; Lipari, G., & Palopoli, L. "Real-Time scheduling: from hard to soft real-time systems", arXiv:1512.01978v1, 2015; mpv `DOCS/man/options.rst`, `video/out/vo.c` at tag `v0.37.0`.
- Claims: D-12 (vol-06, the TIMER passage; `e4ac1624` 2026-10-17; records 9.11 S1, S2, 2026-09-24), E-17 (dataset guidebook vol. 01; `c4f0ac36` 2026-10-17; same records, 9.11 decision D17 2026-10-08), E-16 (dataset guidebook vol. 03:244, :2397; `f30b086b` 2026-10-14; record the 2026-09-13 comparison K1, 2026-09-13).

### T-04 — GStreamer's sinks and late buffers
- Topic: in GStreamer's base sink and video sink, what happens to a buffer whose presentation time has already passed when it reaches the sink: the lateness threshold, its default in the base sink and the value the video sink sets, and whether such a frame is rendered or dropped.
- Bibliographic entry: GStreamer, gitlab.freedesktop.org/gstreamer/gstreamer, main at `83e7df9168dd73f5dcd1caa60195a9d9dce558b4`, `libs/gst/base/gstbasesink.c`, `gst-libs/gst/video/gstvideosink.c`.
- Claims: D-14 (vol-06:462; `e4ac1624` 2026-10-17; record 9.11 S2, 2026-09-24).

### T-05 — LAVD talk slides (OSS NA 2024)
- Topic: in the slide deck: the speaker and the date; on the slide about task scheduling and CPU utilisation while a game runs, how many tasks are reported, over what population (one game process, or the whole system while a game runs) and what share are system tasks; what the slides say initiates scheduling events (preemption versus waiting calls), with the shares given, and whether any slide states how many schedules one wake-up of a task spans; and in the task-graph figures of slides 11 and 16, which processes and threads are linked and by which calls.
- Bibliographic entry: Min, C. "Optimizing Scheduler for Linux Gaming." Open Source Summit North America 2024, Seattle, 2024-04-17. static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf (30 slides).
- Claims: D-21 (vol-06; `6eebab2d` 2026-10-17; record the 2026-09-13 LAVD read R02), E-28 (dataset guidebook vol. 04:1919; `f30b086b` 2026-10-14; record 9.4 changelog D9 and R02, 2026-09-13). The slide 11 and 16 figures settle the conflict between R02 and the 9.4 gaming record behind D-23 and F-16.

### T-06 — Who develops LAVD, and Valve's role
- Topic: who develops the LAVD scheduler (person and employer), for which product or platform the development is said to be done, Valve's role in it, and whether Valve ships it in SteamOS — in which release, enabled by default or selected by the user; for each, whether the source presents it as the developer's statement or the reporter's.
- Bibliographic entry: Edge, J. "Lessons from creating a gaming-oriented scheduler." LWN.net, 2026-01-07, lwn.net/Articles/1051430/; scx repository `scheds/rust/scx_lavd/` at release `v1.1.3` (`c8728c6b`), github.com/sched-ext/scx; the SteamOS release notes behind `steamos-lavd` in `docs/references.md`.
- Claims: E-29 (dataset guidebook vol. 02:689; `f30b086b` 2026-10-14; record 9.12 decision D9, 2026-10-08), F-19 (dataset guidebook vol. 08:226; `556f188e` 2026-10-17; record 9.12 S2, 2026-10-07).

### T-07 — Steam Deck's display refresh
- Topic: in Valve's SteamOS 3.2 update note and the Steam Deck tech specs, the LCD model's default display refresh rate, the frame limits offered at it, and the frame time each corresponds to.
- Bibliographic entry: Valve. "The SteamOS 3.2 Update." Steam Deck news, 2022-05-26, store.steampowered.com/news/app/1675200/view/4437747060827905309; Steam Deck tech specs, steamdeck.com/en/tech/deck.
- Claims: D-27 (vol-06; `ba94cbb5` 2026-10-17; record 9.4 S2, 2026-09-13).

### T-08 — Gregg's `perf sched` example
- Topic: in the "Scheduler Analysis" section of the perf examples page, what was captured, over how long, during what workload, and which process names appear in the latency summary with their runtimes and switch counts.
- Bibliographic entry: Gregg, B. "Linux perf Examples", §6.7, brendangregg.com/perf.html (Last Updated 29-Jul-2020).
- Claims: D-31 (vol-06; `da39802c` 2026-10-17; record 9.6 S3, 2026-09-16).

### T-09 — Chromium's process model
- Topic: in Chromium's process-model document, how renderer processes relate to sites on desktop platforms: whether a process can hold documents of more than one site, and whether one site can occupy more than one process.
- Bibliographic entry: The Chromium Authors, `docs/process_model_and_site_isolation.md`, chromium/src at `2ea96871`.
- Claims: D-36 (vol-06:1818; `ba94cbb5` 2026-10-17; record the 2026-09-13 browser-tabs read R09, 2026-09-13).

### T-10 — Firefox tab and window telemetry (GLAM)
- Topic: in Mozilla's GLAM aggregates of Firefox Desktop release telemetry on Linux, the distribution across clients of the largest number of tabs and of browser windows open at once: which percentiles are served, for which versions, how stable the median is across versions, and whether the tab count is per window or across all windows.
- Bibliographic entry: Mozilla, GLAM public API glam.telemetry.mozilla.org/api/v1/data/, product `fog`, release channel, metrics ping, probes `browser_engagement_max_concurrent_tab_count` and `…_window_count`; metric definitions `browser/modules/metrics.yaml`, mozilla-firefox/firefox at `cf51949351fa`.
- Claims: D-37 (vol-06; `ba94cbb5` 2026-10-17), E-13 (dataset guidebook vol. 01:598, vol. 03:419; `f30b086b` 2026-10-14); record 9.10 S3, 2026-10-01.

### T-11 — The SWELL Knowledge Work dataset
- Topic: who the participants were (number, kind, setting), in what year and on what platform the data were recorded, how long each session lasted, which tasks they did, and what the computer-interaction log records per event (keystroke timestamps and their resolution, application, window).
- Bibliographic entry: Koldijk, S., Sappelli, M., Verberne, S., Neerincx, M. A., & Kraaij, W. "The SWELL Knowledge Work Dataset for Stress and User Modeling Research." Proc. ICMI 2014, DOI 10.1145/2663204.2663257; data DANS doi:10.17026/dans-x55-69zp, version 4.
- Claims: D-38 (vol-06; `ba94cbb5` 2026-10-17; record 9.5 S3, 2026-09-13), E-20 (dataset guidebook vol. 01:788; `da39802c` 2026-10-17; records the 2026-09-13 task-switching read R10 (2026-09-13) and the 9.10 search log S1 (2026-10-01)).

### T-12 — Proton
- Topic: in Proton's README, how Proton is described in relation to the Steam client, and whether it documents running Proton without the Steam client.
- Bibliographic entry: Valve, Proton, github.com/ValveSoftware/Proton, branch `proton_9.0`, `README.md`.
- Claims: D-39 (vol-06:2366; `ba94cbb5` 2026-10-17; record 9.4 S4, 2026-09-13).

### T-13 — SteamCMD
- Topic: in Valve's SteamCMD documentation, what SteamCMD is for, and what account is required to download a game's content (anonymous login versus an account that owns the game).
- Bibliographic entry: Valve Developer Community, "SteamCMD", developer.valvesoftware.com/wiki/SteamCMD.
- Claims: D-40 (vol-06; `ba94cbb5` 2026-10-17; record 9.4 S4, 2026-09-13).

### T-14 — CpsMark+ sensitivity tables
- Topic: in the CpsMark+ paper, what Table 4 tabulates (per workload or per module, which hardware factors), where module-level sensitivities are given, and which module and hardware factor the largest ratio belongs to.
- Bibliographic entry: Zhang, Y., & Wu, T. (2023). "CpsMark+: A scenario-oriented benchmark system for office desktop performance evaluation in centralized procurement via simulating user experience." *BenchCouncil Transactions on Benchmarks, Standards and Evaluations* 2(4), 100084. DOI 10.1016/j.tbench.2023.100084.
- Claims: D-42 (vol-06:2248; `ba94cbb5` 2026-10-17; record the 2026-09-13 CpsMark read R04, 2026-09-13).

### T-15 — interbench's Burn load
- Topic: in interbench's man page and source, what the "Burn" background load is: how many threads, what each does, and when it stops.
- Bibliographic entry: Kolivas, C., interbench, github.com/ckolivas/interbench, `interbench.8` and `interbench.c` at `e612a65` (version string 0.31).
- Claims: E-38 (dataset guidebook vol. 02:1044; `f30b086b` 2026-10-14; record the 2026-09-13 comparison K1, 2026-09-13).

### T-16 — González & Mark, CHI 2004
- Topic: in the study of information workers, the average continuous time spent on an event and on a working sphere before switching, and which event types and which sphere kinds each average covers.
- Bibliographic entry: González, V. M., & Mark, G. (2004). "'Constant, Constant, Multi-tasking Craziness': Managing Multiple Working Spheres." Proc. CHI 2004, 113–120. DOI 10.1145/985692.985707.
- Claims: E-50, E-51 (dataset guidebook vol. 01:1057, vol. 03:603, vol. 04:1564; `d62372dc` 2026-10-17; records the 2026-09-13 task-switching read R10 and comparison K4, 2026-09-13).

### T-17 — ananicy-cpp's rule matching and CachyOS's default install
- Topic: how ananicy-cpp picks the name it matches against its rule catalogue for a running process (which source of the name, whether truncated), and whether CachyOS's installer installs and enables ananicy-cpp with its catalogue by default.
- Bibliographic entry: ananicy-cpp, gitlab.com/ananicy-cpp/ananicy-cpp, tag `v1.2.0` (`cf5ac2eb`), `src/platform/linux/process.cpp`, `src/rules.cpp`; CachyOS `cachyos-settings` package (CachyOS-PKGBUILDS) and the CachyOS desktop ISO of 2026-08-09; CachyOS/ananicy-rules at `03ef03fb`.
- Claims: E-52 (dataset guidebook; `d62372dc` / `df38aa54` 2026-10-17; records 9.12 decisions D105, D109 2026-10-09, S2-45 and S2-46 2026-10-08).

### T-18 — GitHub-hosted runners
- Topic: GitHub's documented limits for a job on a GitHub-hosted runner — the maximum execution time per job — and the processor count, memory and storage of the standard Linux runner for public repositories.
- Bibliographic entry: GitHub Docs, "Actions limits" (docs.github.com/en/actions/reference/limits) and "GitHub-hosted runners reference" (docs.github.com/en/actions/reference/runners/github-hosted-runners).
- Claims: E-53 (dataset guidebook vol. 01:874; `d62372dc` 2026-10-17; record 9.10 S4, 2026-10-01).

### T-19 — Coetzee et al.'s build-system preprint
- Topic: in the preprint's section on preliminary experimental results, what workload the first prototype was run on, what the text says about the number and the lifetime of the processes that workload creates (whether a count is given), and which programs it names as examples.
- Bibliographic entry: Coetzee, D., Bhaskar, A., & Necula, G. (2012). "A model and framework for reliable build systems." arXiv:1203.2704v1; UC Berkeley TR UCB/EECS-2012-27.
- Claims: F-13 (dataset guidebook vol. 06:518; `da39802c` 2026-10-17; record the 2026-09-13 build-papers read R03, 2026-09-13).

### T-20 — Game Mode documentation on recognising a game
- Topic: whether Microsoft's and Apple's own Game Mode documentation states how the operating system decides that a running application is a game (a list, a heuristic, a declaration or a category), and on which page.
- Bibliographic entry: Microsoft Learn, Game Mode API pages (learn.microsoft.com/en-us/windows/win32/gamemode/) and Xbox Support, "Game Mode"; Apple Support, "Use Game Mode" (support.apple.com/en-us/105118); Apple Developer, the `LSSupportsGameMode` Info.plist key.
- Claims: B-41 (`docs/background-guide.md:18`; `0e3b627d` 2026-10-17; record 9.12 S2, 2026-10-07).

## (b) Spot checks

### S-01 — Field & Welsh 2007 (task 9.11)
- Topic: for which data structures and models the paper shows the cluster bootstrap consistent, in which asymptotic regime (number of clusters, cluster size), and what its simulations used (number and size of clusters) and found about the bootstrap's variance estimate.
- Bibliographic entry: Field, C. A., & Welsh, A. H. (2007). "Bootstrapping Clustered Data." *JRSS-B* 69(3), 369–390. DOI 10.1111/j.1467-9868.2007.00593.x.
- Claim: B-26 (`harness/experiments/rq0-gate.yaml:476–481`; record the 9.11 changelog decision D27 (the statistics citations), `task-9.11-scheduler-constants/changelog.md:373`, 2026-10-08).

### S-02 — Brodersen et al. 2010 (task 9.11)
- Topic: how the paper defines balanced accuracy, from which quantities, and whether it gives a form for more than two classes.
- Bibliographic entry: Brodersen, K. H., Ong, C. S., Stephan, K. E., & Buhmann, J. M. (2010). "The Balanced Accuracy and Its Posterior Distribution." Proc. ICPR 2010, 3121–3124. DOI 10.1109/ICPR.2010.764; kaybrodersen.github.io/publications/Brodersen_2010b_ICPR.pdf.
- Claim: B-01 (`docs/harness/metrics.md:258`; record 9.11 S1, 2026-09-24).

### S-03 — The Cargo Book (task 9.12)
- Topic: what `cargo build` compiles, and how the book describes Cargo's relation to the Rust compiler.
- Bibliographic entry: The Cargo Book, doc.rust-lang.org/cargo/, `commands/cargo-build.html` and `guide/why-cargo-exists.html`.
- Claim: A-62 (`docs/research-proposal.md:185`; record 9.12 S2-56 and audit A2-07, 2026-10-09).

### S-04 — Ananicy and ananicy-cpp (task 9.12)
- Topic: the upstream Ananicy repository's status and the date of its last change; in ananicy-cpp, which attribute of a process a rule's name is matched against and whether it is truncated, and what a rule's type can set (nice value and on which threads, I/O class, scheduling policy).
- Bibliographic entry: Nefelim4ag, Ananicy, github.com/Nefelim4ag/Ananicy (last commit `1e2cc9a6`); ananicy-cpp, gitlab.com/ananicy-cpp/ananicy-cpp, tag `v1.2.0` (`cf5ac2eb`) and README at `3554447c`.
- Claim: A-25 (`docs/related-work.md:40`, `docs/research-proposal.md:540`; records 9.12 S2-30, S2-31, audit A3-07, decision D105, 2026-10-07/09). Overlaps T-17 on the matching rule; one reader may take both.
