# 9.16 claim audit — dataset side: blind re-read topics

The sample for the blind re-read of task 9.16's claim audit (its spec's decision 1: trace each claim, then re-read a sample blind). 133 claims:
- **(a)** every claim whose repository wording changed after its read record was written (119 claims; LABELLED claims are excluded, since they have no source passage to re-read);
- **(b)** two spot checks per slice, 9.4 to 9.10 (14 claims). They were drawn at random with seed 20261017 (`random.Random(20261017).sample`, two per slice, over the TRACED claims not in (a), in slice order 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10).

Each topic says what to look up in the source, without the repository's wording or value. A reader reads the source for the topic first, records the passage, locator and copy (per phase spec decision 1, the verification standard), and only then opens `dataset-inventory.md` at the claim id to compare. Topics are grouped by source, with the bibliographic entry first.

## Min, C. (2024). "Optimizing Scheduler for Linux Gaming." Talk, Open Source Summit North America 2024, 2024-04-17. Slides: static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf (`lavd-ossna24`)
- D-F1-01 (a): the talk's title, speaker, event, city and date, and the number of slides in the deck.
- D-F1-02 (a): how many tasks the slides say are scheduled while a game runs, and whether that count includes system tasks.
- D-F1-03 (a): what share of those tasks the slides call long-lived.
- D-F1-04 (a): how the slides describe the concentration of scheduling activity:
  - how many top tasks account for how much of it;
  - how those tasks split between system and game-specific tasks, with their shares;
  - whether tasks outside that top group are described.
- D-F1-06 (a): what the slides state about per-schedule task runtimes (average and maximum), and which named tasks are given as examples, with what runtimes.
- D-F1-08 (a): what the slides say about how stable or predictable a task's execution time is.
- D-F1-10 (a): what the slides say initiates scheduling events, by kind and with shares, and what the slide's pie chart shows for preemption.
- D-F1-12 (a): whether the deck gives a targeted latency or time-slice example, its value, and on which slide. Also, separately, any per-task slice example in scx_lavd's source comments at the pinned scx release.
- D-F1-13 (a): the waiter–waker graph on slide 16: which thread and process names appear in it.
- D-F1-14 (a): on slide 16, how many nodes carry each name, in particular the game executable's name. Also how Wine names a thread that sets no name of its own (Wine source).
- D-F1-16 (a): what the slides say about a sequence of tasks serving one job, and about whether game tasks are periodic.
- D-F1-17 (a): whether the deck states a frame period or a frame budget, and what any latency figure in it is called.
- D-F1-18 (a): how the slides say their traces were obtained, and whether the game and the machine are named.
- D-F1-19 (a): which tool, if any, the 2024 deck names for collecting its scheduling traces.
- D-F1-20 (b 9.4): over how many distinct process trees (process ids) the deck's figures draw, and whether the text says which trace feeds slides 12–14.
- D-F1-09 (b 9.4): slide 13's runtime plot: how many tasks it orders, its axis ranges, and the runtimes at its low end and in its middle.

## Valve, Steam Support FAQ 4F9E-6328-E9B8-47F9 ("Downloads automatically pause when launching a game") and FAQ 71AB-698D-57EB-178C ("Managing Steam Downloads & Updates"), help.steampowered.com (`steam-downloads`)
- D-F1-26 (a): which client setting governs downloads while a game runs, where it sits in the client, and what Steam does with downloads by default when a game launches.
- D-F1-27 (a): which of the two articles mentions a per-game setting for downloads during play, and what that setting does.
- D-F1-28 (a): how game updates enter the download queue.

## rlach, ValveSoftware/steam-for-linux GitHub issue #8821 and its first comment, 2022-09-30 (`steam-for-linux-8821`)
- D-F1-29 (a): what happens, per the issue, to a download started while a game runs with the gameplay-download setting off, and what Valve's triager answered.

## Valve, SteamOS 3.8 release note, Steam Community Announcements, 2026-06-18 (`steamos-lavd`); sched-ext/scx release v1.1.3 (`scx`); Edge, J., LWN.net, 2026-01-07, lwn.net/Articles/1051430/ (`edge-lwn26`)
- D-F1-30 (a): what the release note says about the LAVD scheduler: how it is turned on and whether it is the default.
- D-F1-31 (a): what scx_lavd's source copyright lines and Edge's report say about Valve's role in LAVD.
- D-F1-32 (a): what scx_lavd's README at v1.1.3 says the scheduler was designed for and which problem it targets.
- D-F1-34 (a): what Edge's report of Min's LPC 2025 session says about the scheduler's design and its lessons.

## Corbet, J. "Sched_ext at LPC 2024." LWN.net, 2024-09-26, lwn.net/Articles/991205/ (`corbet-lwn24`)
- D-F1-33 (a): what the report says about the LPC 2024 talks on LAVD and gaming.

## Dai, D., & Newton, R. "How do we make a Steamdeck scheduler work on large servers." LPC 2025 sched_ext MC abstract, contribution 2099 (`dai-lpc25`)
- D-F1-35 (a): what the abstract says the speakers intend to do with scx_lavd.

## Microsoft, Game Mode documentation, Microsoft Learn (portal; `expandedresources.h` and its function pages) (`gamemode-docs`); "Use Game Mode while gaming on your Windows device", Xbox Support (`xbox-gamemode`); Apple, "Use Game Mode", support.apple.com/en-us/105118 (`apple-gamemode`)
- D-F1-36 (a): what Microsoft's pages say Game Mode is, and what it does for the game and to other work.
- D-F1-37 (a): which functions the `expandedresources.h` header page documents, and where `SetProcessDefaultCpuSets` is mentioned.
- D-F1-38 (a): what the Xbox Support page says Game Mode does about Windows Update while a game runs.
- D-F1-39 (a): what Apple's page says Game Mode does on macOS.

## Feral Interactive GameMode 1.8.2 (`feral-gamemode`); Red Hat tuned v2.28.0, `tuned-main.conf` (`tuned`); systemd `oomd.conf(5)` (`systemd-oomd`)
- D-F1-40 (a): how a game requests GameMode, and what the configuration's whitelist and blacklist section does.
- D-F1-46 (a): what each of these time settings is described as doing, with its default, and whether dynamic tuning is on by default:
  - GameMode's `reaper_freq`;
  - tuned's `update_interval` and `dynamic_tuning`;
  - systemd-oomd's `DefaultMemoryPressureDurationSec`.

## Linux kernel source, `include/linux/sched.h`, tag v6.17 (`linux-sched-h`)
- D-F1-48 (a): the length of the task command-name buffer, whether the stored name is terminated and padded, and therefore the longest name it holds.

## Koldijk, S., et al. (2014). The SWELL Knowledge Work Dataset for Stress and User Modeling Research. ICMI 2014; data DANS doi:10.17026/dans-x55-69zp v4 (`swell-icmi14`)
- D-F2-01 (a): the SWELL-KW participants: who they were and how many, plus where, when and on what operating system the data was collected, and for how long per participant.
- D-F2-02 (a): what the uLog files record per keystroke and per pointer event, with which fields.
- D-F2-03 (a): the dataset's licence and access conditions in the DANS record.
- D-F2-06 (a): a computation from the uLog files: the distribution of time per focus episode, and how often a switch away from an application is followed by a return to it.

## Dhakal, V., et al. (2018). Observations on Typing from 136 Million Keystrokes. CHI 2018; data userinterfaces.aalto.fi/136Mkeystrokes/ (`dhakal-chi18`)
- D-F2-07 (a): the released data file: its name and size, its per-keystroke fields, the row count of the participant metadata, and the licence text.
- D-F2-08 (a): the paper's population and task, its final participant count, and the inter-key interval statistics it reports, with what they are computed over.
- D-F2-09 (a): two computations, the share of key-to-key gaps over 1 s in a within-sentence sample of this data and in SWELL-KW's Word stream; and which 9.5 decision records this alternative as not taken.

## González, V. M., & Mark, G. (2004). "Constant, Constant, Multi-tasking Craziness": Managing Multiple Working Spheres. CHI 2004, 113–120 (`gonzalez-chi04`)
- D-F2-10 (a): the mean time per "event", how an event is defined, and what the paper excludes.
- D-F2-11 (a): the mean continuous time in a working sphere before switching:
  - which spheres it covers;
  - its variants (all spheres; short switches ignored);
  - the average total time per sphere.
- D-F2-12 (a): spheres per day; time per device or document before switching; which statistics are reported; how the participants are described and how many there are.

## Mark, G., González, V. M., & Harris, J. (2005). No Task Left Behind? CHI 2005, 321–330 (`mark-chi05`)
- D-F2-14 (a): the mean time in a working sphere before a switch or interruption, which spheres, and the informants (how many, and their overlap with the 2004 study).
- D-F2-15 (a): how interruptions split between internal and external, and whether the paper's table and its text agree.
- D-F2-16 (a): how often interrupted work was resumed the same day and after how long. Also whether a resumption-time figure widely attributed to Mark (from a 2006 interview) appears in her CHI papers of 2004, 2005, 2008 and 2014.

## Czerwinski, M., Horvitz, E., & Wilhite, S. (2004). A Diary Study of Task Switching and Interruptions. CHI 2004, 175–182 (`czerwinski-chi04`)
- D-F2-17 (a): the study's method, its duration, the participants analysed, and the statistics reported.

## Roeser, J., et al. (2024). Modelling typing disfluencies as finite mixture process. Reading and Writing 37, 359–384 (`roeser-rw24`)
- D-F2-18 (a): the task, the sample, the model, and the Table 3 values: what each parameter is and on what scale.

## Killourhy, K. S., & Maxion, R. A. (2009). Comparing Anomaly-Detection Algorithms for Keystroke Dynamics. DSN 2009 (`killourhy-dsn09`)
- D-F2-19 (b 9.5): what the released dataset is: subjects, the typed string, sessions and repetitions, and which timing features it records.

## Sánchez Sánchez, P. M., et al. (2020). BEHACOM – a dataset modelling users' behaviour in computers. Data in Brief (`behacom-dib20`)
- D-F2-20 (a): the number of users and their operating systems, the collection period, the fields recorded, and where the data is deposited.

## Yin, H., et al. (2026). FOCAL. arXiv:2604.19541 v2, with its DesktopBench release (`focal-arxiv26`)
- D-F2-21 (a): how DesktopBench sessions are produced (observed or composed), how an interruption is structured within a session, and the session counts.
- D-F2-22 (a): the per-action timing in the released scripts, the release's location, version and terms, and the paper's venue status.

## Kolivas, C. interbench, github.com/ckolivas/interbench, master e612a65 (`interbench`); LWN 725238 and 1051430
- D-F2-23 (a): the pinned commit's version string and the licence files and headers.
- D-F2-25 (a): the interactive task constants for audio, video and X, and how the man page and the source describe the video task.
- D-F2-26 (a): how interbench handles a missed period in its interactive tasks.
- D-F2-27 (a): the Burn load's default thread count, and any jitter figure the documentation reports.
- D-F2-28 (a): which distributions package interbench (Repology), and what the two LWN articles say about the use of hackbench, rt-app, stress-ng and interbench.

## rt-app, github.com/scheduler-tools/rt-app, commit d6f8be41 (`rt-app`); LWN 725238
- D-F2-32 (a): who LWN says uses rt-app, and what rt-app's README says it is.

## Mason, C. schbench, git.kernel.org mason/schbench.git tag v1.0 (`schbench`); Zheng, Y., et al. (2025). Towards Agentic OS, arXiv:2509.01245 v4 (`schedcp-mlsys25`)
- D-F2-33 (a): the tag and commit, the copyright holder and the licence.
- D-F2-34 (a): which percentiles schbench v1.0 prints, for which quantities, and what one request does.
- D-F2-35 (a), D-F5-24 (a): whether SchedCP's reference list cites schbench, and at what URL.

## hackbench in rt-tests, tag v2.11 (`hackbench`)
- D-F2-36 (a): what the man page says hackbench is for, its defaults and what it outputs.
- D-F2-37 (a): what LWN 725238 says hackbench is used for.

## King, C. I. stress-ng, commit 3ac9d7a8 (`stress-ng`)
- D-F2-38 (a): the licence; what the `--workload` and `--cyclic` stressors do; what the README says about precise benchmarking.

## Ananicy (github.com/Nefelim4ag/Ananicy) and ananicy-cpp v1.2.0 (`ananicy`); CachyOS `cachyos-settings` 1.4.1 (`cachyos-settings`); CachyOS ananicy-rules commit 03ef03fb (`ananicy-rules`)
- D-F2-39 (a): Ananicy's repository status and licence; ananicy-cpp's licence, its version on CachyOS, its self-description, its rule fields and its lineage.
- D-F2-40 (a): which process attribute ananicy-cpp matches its rules against.
- D-F2-41 (a): whether CachyOS installs and enables ananicy-cpp, and with which rules package.
- D-F2-42 (a): at the commit, how many rules and types the catalogue has, which values they set, and who maintains it.
- D-F2-43 (a): what the catalogue sets for audio servers, file indexers and compilers, and whether it distinguishes wanted from unwanted background work.
- D-F2-44 (a): a computation on the final build (`dataset/build/`), using ananicy-cpp's lookup key: for how many core files the catalogue matches every bound process name, and which bound names it matches no rule for.

## Five Directions, OpTC data release documentation, commit 5b108604 (`darpa-optc`); University of Helsinki, Carat Top 1000 data-sharing page (`carat-top1000`)
- D-F2-45 (a): which events and fields OpTC documents, and from which kind of endpoints.
- D-F2-46 (a): what a Carat sample records about running applications.

## O'Callahan, R., et al. (2017). Engineering Record and Replay for Deployability. USENIX ATC '17 (`ocallahan-atc17`); Coetzee, D., et al. (2012). arXiv:1203.2704 (`coetzee-arxiv12`)
- D-F3-01 (a): the build workload behind the paper's process count (project, version, make options), and its section.
- D-F3-02 (a): what exactly the process count counts, and whether the paper says what those processes run.
- D-F3-03 (a), D-F3-04 (a): what the preprint says about processes in builds, and which builds it names.
- D-F3-06 (a): three things:
  - the next most prolific workload in O'Callahan et al.'s table;
  - whether linux-6.6's Documentation mentions `sched_child_runs_first`;
  - what SCHED_AUTOGROUP's Kconfig help text says about the workloads it isolates.

## SchedCP: Zheng, Y., et al. (2025). Towards Agentic OS, arXiv:2509.01245 v4 (`schedcp-mlsys25`)
- D-F3-05 (a), D-F5-22 (a): SchedCP's kernel-compilation workload (kernel version, configuration, make options) and the gain it reports over the default scheduler.
- D-F5-23 (a): where in the paper the phrase about process lifetimes of that workload appears: author text, or output generated by the system's agent.

## GNU make 4.4.1 manual (`doc/make.texi`); DKMS 3.0.11 as Ubuntu 24.04 packages it (`dkms`)
- D-F3-07 (a): GNU make's default number of parallel jobs, and the parallelism DKMS uses for a module build.
- D-F3-09 (b 9.6): what make's jobserver counts: jobs or processes.
- D-F3-28 (a): DKMS's kernel install hooks, and the job count its build passes.

## Meyer, D. T., & Bolosky, W. J. (2011). A Study of Practical Deduplication. FAST '11 (`meyer-fast11`); Dinneen, J. D., `fm-results-tables`, folder ASIST21-FSD (`fm-results-tables`); Vrable, M., et al. (2009). Cumulus. FAST '09 (`vrable-fast09`)
- D-F3-13 (a): how bytes are distributed over file sizes: the file size above which half of all bytes lie.
- D-F3-14 (a): the median file size for GNU/Linux users in the tables.
- D-F3-15 (a): Cumulus's daily change rates for personal machines: the statistic, and how many days were traced.

## Déjà Dup 45.2 (`deja-dup`); Ubuntu 24.04.5.1 desktop manifests (`ubuntu-desktop-manifest`); systemd 255.4, tracker-miners 3.7.1, gnome-session 46.0
- D-F3-16 (a): how `deja-dup-monitor` starts a scheduled backup: which processes, and when.
- D-F3-18 (a): Déjà Dup 45.2's defaults: the schedule once backups are on, encryption, volume size, and password storage.
- D-F3-19 (a): whether Déjà Dup is in the default or the extended desktop install.
- D-F3-21 (a): which systemd slice or scope the file indexer and the backup monitor run in on the stock desktop, and the CPU weights those slices set.
- D-F3-32 (a): whether Tracker's file miner is in the default install, and at which version.
- D-F3-34 (b 9.6): which scheduling policy and nice level Tracker 3.7.1's threads set on themselves.

## unattended-upgrades 2.9.1+nmu4ubuntu1 (`unattended-upgrades`); APT 2.8.3's systemd units (`apt`); glibc 2.39-0ubuntu8.8 (`glibc`)
- D-F3-23 (a): whether unattended-upgrades is in the default install and enabled by default.
- D-F3-22 (b 9.10): how apt's units start the daily upgrade: the timer's schedule, its randomised delay, and the service it runs.
- D-F3-24 (a): the 2026-07 glibc security update: version, publication date and binary packages.

## NVIDIA open GPU kernel modules 595.91.07 as Ubuntu packages them (`nvidia-open-kernel-modules`); the Ubuntu archive's kernel publication history
- D-F3-29 (a): the module package's version and branch, and how many kernel modules it builds.
- D-F3-30 (a): when the newest 24.04 HWE kernel ABI reached `noble-security` in September 2026 and which ABI it replaced, and which HWE kernel the 24.04.5.1 installer adds.

## HandBrake 1.7.2, `preset/preset_builtin.json`, and `handbrake-cli` as Ubuntu 24.04 packages it (`handbrake`); CPSmarkPLUS bf24434 (`cpsmarkplus`); DCI Digital Cinema System Specification 1.4.1 (`dci-dcss`)
- D-F3-35 (a): which preset is marked default, with its encoder, encoder speed, quality, profile, level, audio and container.
- D-F3-36 (a): the Ubuntu package and version of HandBrakeCLI, and the x264 library it uses.
- D-F3-38 (a): CPSmarkPLUS's HandBrake workload: the input codec, the target resolution and the name its code gives that target. Also how the DCI specification defines that name.
- D-F3-39 (a): whether the CPSmarkPLUS repository carries a licence.

## Valve, "Steam Download Stats", store.steampowered.com/stats/content/ (`steam-download-stats`)
- D-F3-40 (a): the download rate the page reports for the country and network chosen: the statistic, the window and the data version.

## Jellyfin 12.0 and Plex Media Server 1.43.4 documentation (as read in the 2026-09-13 verification, R11)
- D-F3-44 (a): whether any distribution or media server starts a model-training, rendering or transcoding job on a schedule without the user asking, and the process names their transcoders run under.

## Ubuntu 24.04 `7zip` / `p7zip-full` packages
- D-F3-42 (b 9.7): which 7-Zip version Ubuntu 24.04 ships as `7z`, and its default archive format and compression level.

## Mahoney, M. "10 GB Compression Benchmark." mattmahoney.net/dc/10gb.html (`mahoney-10gb`)
- D-F4-34 (b 9.7): what the benchmark set contains (file count, total size) and where its files came from.

## Zhang, Y., & Wu, T. (2023). CpsMark+. BenchCouncil TBench 2(4), 100084 (`cpsmark-tbench23`)
- D-F4-01 (a): what CpsMark+ calls its usage scenarios and modules, and which applications each one runs.
- D-F4-02 (a): whether CpsMark+ has an archiving workload, with which application, and what it compresses.
- D-F4-04 (a): the stages of the CA module's cooperative workflow, in order.
- D-F4-05 (a): the order of the CC module's workloads, and whether any workload's output feeds the next.
- D-F4-06 (a): the hardware-sensitivity results: each module's figure for its best graphics configuration against its base.

## UL, PCMark 10 Technical Guide, 2021-02-11 (`pcmark10`)
- D-F4-14 (a): whether the guide documents timing per scripted task or per process.
- D-F4-15 (a): where the video playback test sits in the product: in a test group, a profile, or a scenario.
- D-F4-13 (b 9.5): which application the Writing workload runs.

## BAPCo, SYSmark 30 User Guide v1.2, and BAPCo's whitepaper "SYSmark 30 – An Overview of SYSmark 30" v1.2 (`sysmark30`); BAPCo, SYSmark 25 User Guide rev. 1.9 (`sysmark25`)
- D-F4-18 (a): SYSmark 30's scenarios and what each one models.
- D-F4-19 (a): the applications SYSmark 30 names for each scenario.
- D-F4-20 (a): SYSmark 30's archiving workload: what it archives and unpacks, and with what.
- D-F4-21 (a): in each of the two documents, what runs concurrently in Advanced Content Creation, and whether Outlook stays open through the office scenario.
- D-F4-23 (a): whether SYSmark 25 includes code compilation, and in what form.
- D-F4-24 (a): which SYSmark versions define the Productivity, Creativity and Responsiveness scenarios.

## UL Solutions, "Procyon benchmark suite", benchmarks.ul.com/procyon (`procyon`)
- D-F4-26 (a): how many benchmarks the page lists, and which of them run AI inference on the device.
- D-F4-27 (a): which applications the office, photo and video benchmarks drive.

## Mozilla, GLAM public API, product `fog`, release, probes `browser_engagement_max_concurrent_tab_count` and `…_window_count` (`glam`)
- D-F4-29 (a): what the tab-count probe measures (over which windows, over what period), and which population GLAM aggregates.
- D-F4-30 (a): GLAM's Linux median of the per-client maximum of open tabs, and of open windows, for Firefox release 152.
- D-F4-31 (a): whether the tab probe counts per window or across all windows.

## PyTorch contributors, examples, "Basic MNIST Example", commit acc295dc (`pytorch-examples`); KDE Kdenlive 23.08.5 as Ubuntu 24.04 packages it (`kdenlive`)
- D-F4-36 (a): the README's run command, and the script's default arguments (epochs, batch size, model saving).
- D-F4-37 (a): which processes Kdenlive's render dialog starts, and the default render profile.

## Chromium source (the window-occlusion tracker; background timer throttling), at the tags the 9.8 browser and comms slice read
- D-F4-45 (a): whether Chromium on Linux marks a window as occluded when another application's window covers it.
- D-F4-43 (b 9.8): how long after a page goes to the background Chromium starts throttling its timer wake-ups, by default.

## Matrix Client-Server API specification and matrix-js-sdk, as read by the 9.8 browser and comms slice
- D-F4-46 (b 9.8): the timeout an idle client's `/sync` long-poll request uses.

## GNOME 46 (gsettings-desktop-schemas, gnome-session, gnome-settings-daemon, Mutter 46.2), as read by the 9.9 daemons and session slice
- D-F4-40 (b 9.9): GNOME's default idle delay, and what the session does when it is reached.
- D-F4-42 (b 9.9): whether Mutter 46 starts Xwayland at session start or only on demand.

## Ubuntu 24.04 generic kernel configuration, as read by the 9.10 scenarios and timelines slice
- D-F5-21 (b 9.10): the transparent-hugepage default.
