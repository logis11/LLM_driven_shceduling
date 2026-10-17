## `interbench`  (13 topics)
- C-interbench-1: in interbench's man page/source, the audio interactive task — how often it wakes, how its CPU demand is specified (percentage, duration, or both) and at what value, and whether a real-time scheduling-policy variant of it exists.
- C-interbench-2: in interbench's man page/source, the video interactive task — its frame or receipt rate / period, the CPU demand it is given and how that demand is expressed.
- C-interbench-3: in interbench's man page/source, the X interactive task — what user activity it emulates, how its CPU demand is specified, whether and how that demand varies (range and variation rule), and whether it is driven by input events.
- C-interbench-4: in interbench, the gaming interactive task — how its CPU demand is bounded and whether it carries deadlines.
- C-interbench-5: in interbench, the Burn background load — what it runs, its default number of threads or processes, and what CPU behaviour each has.
- C-interbench-6: in interbench, the Write background load — what it writes, how the written size relates to system memory, and its access pattern.
- C-interbench-7: in interbench, the Read background load — what it reads, how the file size relates to memory, and whether/how it avoids the page cache.
- C-interbench-8: whether interbench specifies any per-block, per-chunk or per-operation timing for its Write and Read loads.
- C-interbench-9: in interbench, the Compile background load — what it is composed of, whether it runs or emulates `make`, and any parallelism level stated for it.
- C-interbench-10: the complete list of interbench interactive tasks and background loads with each one's definition, including any custom task option, any memory-pressure load and its sizing, and any hackbench-based load and its argument.
- C-interbench-11: which statistics interbench reports per task, whether it states a human-perception jitter threshold (and its value), and its default run length.
- C-interbench-12: how interbench combines interactive tasks with background loads in a run.
- C-interbench-13: interbench's author, repository, license and version string; whether distributions package it.

## `rt-app`  (4 topics)
- C-rt-app-1: rt-app's JSON configuration format — the per-task and global fields it defines and the time unit of its duration fields.
- C-rt-app-2: what rt-app's `timer` event does, what `ref` and `period` mean, whether wake times are absolute or relative to the previous wake, and what happens when an iteration overruns.
- C-rt-app-3: the contents of rt-app's example template configuration.
- C-rt-app-4: rt-app's maintainer organization, license, and whether kernel documentation references it.

## `lavd-ossna24`  (20 topics)
- C-lavd-1: on the slides, the number of tasks observed while a game runs, which game(s) and system it was measured on, and whether it is a count, average or range.
- C-lavd-2: on the slides, the share of tasks classified as long-lived versus short-lived during gaming, and how "long-lived" is defined.
- C-lavd-3: on the slides, which non-game server processes appear among scheduled tasks and what share of scheduling activity they account for, and how "share of scheduling" is measured.
- C-lavd-4: on the slides, whether wine/wineserver (and graphics/audio components) are shown as linked with game tasks in the waker/wakee relationships, and at which slide.
- C-lavd-5: on the slides, the per-schedule runtime figures reported for game-related tasks — which tasks are named, what statistic each figure is (average, maximum, percentile), and the values.
- C-lavd-6: on the slides, whether a task's runtime per scheduling is described as consistent over time, and in what terms.
- C-lavd-7: on the slides, the breakdown of what causes scheduling events (e.g. blocking system calls vs timer preemption) during gaming, the shares, and any named system calls.
- C-lavd-8: on the slides, how game-related tasks wake one another (the depicted structure, its shape, and the stages it names between input and output).
- C-lavd-9: on the slides, the frame time budget and any targeted latency value stated for the gaming scenario, and the frame rate it corresponds to.
- C-lavd-10: on the slides, how concentrated scheduling activity is across tasks (how many top tasks account for what share) and how the share is measured.
- C-lavd-11: on the slides, the number of game (as opposed to non-game) tasks that dominate scheduling, their combined share, and whether they are described as frame-critical or as a pipeline.
- C-lavd-12: on the slides, what is said about the activity of tasks outside the dominant set (idle, waiting, or otherwise), and at which slide.
- C-lavd-13: on the slides, any CPU utilization figure reported during gaming.
- C-lavd-14: on the slides, how game frame-rate metrics are related to scheduler performance metrics.
- C-lavd-15: on the slides, the hardware (core count) and system on which the gaming observations were collected.
- C-lavd-16: on the slides, whether non-game applications (chat/voice/overlay) are mentioned or shown running during gaming.
- C-lavd-17: on the slides, how task durations are characterized and how latency outliers relate to user-perceived frame problems.
- C-lavd-18: which organizations are stated to ship or deploy the LAVD scheduler, and in what setting.
- C-lavd-19: whether the talk or the scheduler provides any workload description format.
- C-lavd-20: speaker, title, event, date and slide URL of the talk.

## `corbet-lwn24` (docs/references.md only; not in sources.yaml)  (2 topics)
- C-corbet-1: the LWN article on sched_ext at LPC — its date, which conference year it covers, whether it has a section on scx_lavd and what gaming characterization that section gives.
- C-corbet-2: whether that LWN article exists, its date and author.

## `scx` (docs/references.md only) — borderline dataset-side use  (1 topics)
- C-scx-1: whether scx_lavd lives in the sched-ext/scx repository and the repository's license.

## `ocallahan-atc17`  (3 topics)
- C-ocallahan-1: in the paper's section describing its benchmark workloads, what the kernel-build workload builds and how it is configured; any stated count of processes forked/exec'd by make and any characterization of their lifetimes; the next workload listed and its count.
- C-ocallahan-2: whether the paper reports any distribution or summary statistic of the lifetimes of the processes in its kernel-build workload.
- C-ocallahan-3: authors, title, venue, pages; whether arXiv:1705.05937 is an extended version; which version has a section numbered 4.3 with the workload description.

## `coetzee-arxiv12`  (2 topics)
- C-coetzee-1: in the paper's section 9 (or wherever it appears), what is said about the Linux kernel build's processes — their number and lifetimes — and whether the statement is specific to that build.
- C-coetzee-2: authors, title, year, arXiv number, TR number, venue status.

## Kernel build — plain-text citations (no id)  (2 topics)
- C-kernelbuild-1: in Linux kernel documentation, what `sched_child_runs_first` and `SCHED_AUTOGROUP` are and whether the documentation motivates either with parallel builds.
- C-kernelbuild-2: whether scheduler evaluations commonly use a kernel build; what process structure (short-lived compiler processes vs long-lived make/linker) any cited source describes.

## `schedcp-mlsys25` — plain-text "SchedCP" citations on the dataset side (references.md entry is related-work only)  (5 topics)
- C-schedcp-1: the kernel-compilation workload configuration in the SchedCP paper (config target, make parallelism, kernel version).
- C-schedcp-2: the list of batch workloads evaluated in SchedCP.
- C-schedcp-3: the machines and workload categories used in SchedCP's evaluation.
- C-schedcp-4: how SchedCP references schbench in its bibliography; SchedCP's venue.
- C-schedcp-5: what SchedCP says about the completeness of its evaluation benchmark.

## `cpsmark-tbench23`  (13 topics)
- C-cpsmark-1: CpsMark+'s usage scenarios — how many, their names, how they are grouped into modules, and the user types or weight classes associated with each module.
- C-cpsmark-2: the content of CpsMark+ Table 1 — user categories and what is stated for each.
- C-cpsmark-3: the content of CpsMark+ Table 2 — application names and versions, and how the applications were selected.
- C-cpsmark-4: in CpsMark+, which named application is used in which usage scenario/workload.
- C-cpsmark-5: in CpsMark+, whether CA workloads run in a fixed order, what the stages are and their order, and whether outputs of one workload feed the next (and which files).
- C-cpsmark-6: the content of CpsMark+ Table 4 — which hardware factors are varied, the sensitivity values per workload/module, and which workloads are sensitive to CPU frequency or storage.
- C-cpsmark-7: the operating system CpsMark+ targets; whether it contains any gaming scenario; whether it reports per-process timing.
- C-cpsmark-8: whether CpsMark+ is released as open source, where its control program and resource packages are hosted.
- C-cpsmark-9: what CpsMark+ says about SYSmark and PCMark methodology and about openness/vendor neutrality.
- C-cpsmark-10: which prior benchmarks (and versions) CpsMark+ compares itself against.
- C-cpsmark-11: whether CpsMark+ reports a real procurement deployment and any user validation period.
- C-cpsmark-12: what the CC module contains and whether its workloads are sequenced (and in what order).
- C-cpsmark-13: authors, title, journal, article number, DOI.

## `pcmark10`  (5 topics)
- C-pcmark-1: in the PCMark 10 technical guide, the benchmark's scenario groups and the individual tests in each group, including any gaming group and its tests.
- C-pcmark-2: which software the PCMark 10 photo editing test uses.
- C-pcmark-3: which applications PCMark 10's Applications benchmark uses.
- C-pcmark-4: whether PCMark 10 has a battery-life video playback profile.
- C-pcmark-5: whether the technical guide documents per-process or per-task timing of its workloads.

## `sysmark30`  (6 topics)
- C-sysmark30-1: in the SYSmark 30 user guide, the scenario names and the activities each scenario models.
- C-sysmark30-2: which applications and activities the General Productivity scenario includes (browser and version, archiving tool and version).
- C-sysmark30-3: whether the Advanced Content Creation scenario includes a workload that switches between photo and video editing, and in what order.
- C-sysmark30-4: the applications and versions listed per scenario in the SYSmark 30 user guide.
- C-sysmark30-5: whether the user guide separates scenario descriptions from scoring; the 2011 departures of vendors from BAPCo and their stated reasons (needs a separate source).
- C-sysmark30-6: the user guide's revision number(s), date, page count, and product release year.

## `sysmark25`  (2 topics)
- C-sysmark25-1: in SYSmark 25 documentation, the scenario list, whether a software-development/code-compilation workload exists and under which scenario, and whether a Responsiveness scenario exists.
- C-sysmark25-2: which SYSmark version defines scenarios named Productivity, Creativity and Responsiveness, and the activities listed under each (email, face recognition).

## `procyon`  (3 topics)
- C-procyon-1: the list of benchmarks in the UL Procyon suite and whether any run AI inference locally, with their names and descriptions.
- C-procyon-2: the non-AI benchmarks in the Procyon suite and the applications each uses.
- C-procyon-3: how much workload detail Procyon's public documentation provides.

## `gamemode-docs`  (5 topics)
- C-gamemode-1: in Microsoft's Game Mode documentation, what Game Mode does for games and which resources it affects.
- C-gamemode-2: the resources Game Mode grants, the condition for granting them, and when each resource is revoked.
- C-gamemode-3: which functions the expandedresources header documents, whether users can opt out and how that is reported, and any deprecation notice.
- C-gamemode-4: whether Microsoft documents how Game Mode recognizes a game (list, name matching, declaration, other), what it says about default coverage of games, and how the `expandedResources` capability is granted.
- C-gamemode-5: what Microsoft documentation says about how background processes are treated during Game Mode, and whether it mentions deferring updates, driver installs, restarts or notifications.

## `ananicy-rules`  (12 topics)
- C-ananicy-rules-1: in the CachyOS ananicy-rules repository, the defined rule `type` names and what each type sets.
- C-ananicy-rules-2: in `00-types.types` at a pinned commit, the nice, ioclass, sched and oom_score_adj values set for each type, including the audio-player type.
- C-ananicy-rules-3: how the catalogue separates Proton/Wine games from Linux-native games (directories, types, or both).
- C-ananicy-rules-4: whether the catalogue or its documentation distinguishes background work the user wants from background work to be deprioritized, and how (types, comments, documentation).
- C-ananicy-rules-5: which type(s) the catalogue assigns to file indexers (e.g. tracker, baloo, updatedb) and the ioclass/nice/sched of that type; whether the catalogue carries any timing or rate values.
- C-ananicy-rules-6: what the catalogue's Heavy_CPU type sets and which processes are assigned to it; which type(s) compiler processes receive and their sched policy.
- C-ananicy-rules-7: how the catalogue classifies voice/chat clients, download clients (e.g. transmission), backup/sync tools (rsync, borg, rclone) and antivirus scanners (clamscan, freshclam) — type and ioclass for each.
- C-ananicy-rules-8: whether catalogue entries match on executable/process names and roughly how many distinct names it lists.
- C-ananicy-rules-9: at the named commit, the number of rules files, rule entries, and entries per type, counted per file.
- C-ananicy-rules-10: at the named commit, how many types the types file defines, which are unused, any undefined type strings, and any malformed rule lines.
- C-ananicy-rules-11: the catalogue README's maintainer statement, contribution instructions for game entries, and any example assigning different types to executables of one game.
- C-ananicy-rules-12: see C-ananicy-2 (upstream types file) and the CachyOS types file.

## `ananicy` (upstream Ananicy / ananicy-cpp; docs/references.md only)  (3 topics)
- C-ananicy-1: the rule fields documented by ananicy/ananicy-cpp, which are required, value ranges, the rules directory, and any example rule for gcc.
- C-ananicy-2: the type names in upstream Ananicy's types file at HEAD and how older type names are marked.
- C-ananicy-3: Ananicy's README self-description, repository locations, licenses and ananicy-cpp version; whether distribution wikis document it.

## `steam-downloads`  (6 topics)
- C-steam-1: in Steam Support articles, the name and menu location of the setting controlling downloads while a game runs.
- C-steam-2: what Steam does with downloads when a game launches, by default.
- C-steam-3: whether Steam offers a per-game setting for downloads during gameplay, and what it does.
- C-steam-4: see C-steam-1 to C-steam-3 (the setting's existence and user control).
- C-steam-5: the title and last-updated date of the named Steam Support article.
- C-steam-6: under what process name(s) the Steam client performs downloads on Linux.

## `dkms-man`  (3 topics)
- C-dkms-man-1: the dkms(8) man page's description of what DKMS is.
- C-dkms-man-2: in dkms(8), what the autoinstall action and the autoinstaller service do, when they run (boot, kernel install, other), and whether user action is required.
- C-dkms-man-3: the command/executable name DKMS runs under and how it is implemented (script or binary).

## `dkms-debian`  (2 topics)
- C-dkms-debian-1: the Debian bookworm `dkms` package description text.
- C-dkms-debian-2: the version of `dkms` packaged in Debian bookworm (and whether the cited page speaks to other distributions).

## `dhakal-chi18`  (6 topics)
- C-dhakal-1: the mean inter-key interval the paper reports, the dispersion statistic reported with it and over what unit (keystrokes, participants' means), and the population it is computed over.
- C-dhakal-2: the shape of the inter-key-interval distribution as described or plotted.
- C-dhakal-3: the number of keystrokes and participants in the study, and how participants were recruited.
- C-dhakal-4: the typing task participants performed (transcription or free composition), whether pauses between sentences/phrases are included or excluded from the reported intervals, and whether any pointing-device input was recorded.
- C-dhakal-5: availability and licence of the study's dataset.
- C-dhakal-6: which of the following the paper reports: a mixture model of inter-key intervals, a fluent-component location, a pause probability, a pause-component location, log-scale spreads.

## `roeser-rw24`  (5 topics)
- C-roeser-1: the statistical model the paper fits to inter-keystroke intervals — distribution family and number of components — and whether alternatives were compared.
- C-roeser-2: the fitted location parameter of the fluent component per task/condition, whether reported on log or raw scale, and whether it is a mean, median or other statistic.
- C-roeser-3: the fitted mixing proportion of the slower component per task/condition, and how the paper interprets that component.
- C-roeser-4: whether and how the fitted parameters differ across the tasks or conditions in the paper.
- C-roeser-5: authors, title, journal volume/pages/year, DOI; data and code availability.

## `zhang-chb15`  (6 topics)
- C-zhang-1: the study's duration, number of subjects, number of log records and distinct processes, data provider, and data availability.
- C-zhang-2: the distribution the paper reports for task-switching (which quantity follows which law), and what term it uses for highly connected tasks.
- C-zhang-3: the average interval between task switches the paper reports, and how a task switch is defined.
- C-zhang-4: whether the paper publishes per-user distributions or fitted parameters for switch intervals/session durations, or only aggregate statistics and figures.
- C-zhang-5: whether the paper says anything about stability of application sets versus process-level churn.
- C-zhang-6: the author list, title, volume and pages of the CHB 2015 paper.

## `gonzalez-chi04`  (7 topics)
- C-gonzalez-1: the average continuous time spent in a working sphere before switching, with and without brief disruptions, and how a working sphere is defined.
- C-gonzalez-2: the average number of distinct working spheres per person per day.
- C-gonzalez-3: the average time spent on an event/task before switching.
- C-gonzalez-4: the average time spent using one electronic tool or paper document before switching.
- C-gonzalez-5: the study population (roles, organization, sample size) and whether distributions or only averages are reported.
- C-gonzalez-6: what interruption statistics (frequency, source) the paper reports.
- C-gonzalez-7: see C-gonzalez-1, -3, -4, and C-mark08-1.

## `mark-chi05`  (3 topics)
- C-mark05-1: the average time spent in a working sphere before switching reported in the 2005 paper.
- C-mark05-2: the proportions of self-initiated (internal) vs external interruptions, overall and by job role.
- C-mark05-3: whether the 2005 paper states what fraction of switches/interruptions are self-initiated.

## `mark-chi08` (references.md only)  (1 topics)
- C-mark08-1: the study design of the CHI 2008 paper and whether it reports time-per-task or time-per-working-sphere figures.

## `mark-chi14` (references.md only)  (1 topics)
- C-mark14-1: what the CHI 2014 paper reports about attention over the day and whether it states the share of self-initiated switches.

## `czerwinski-chi04` (references.md only)  (1 topics)
- C-czerwinski-1: the method and main task-switching/interruption findings of the CHI 2004 diary study.

## `mark-gallup06` (references.md only)  (1 topics)
- C-gallup-1: whether the Gallup interview states a time to resume an interrupted task and its value; whether that figure appears in the Mark et al. CHI papers.

## `swell-icmi14` (references.md only)  (1 topics)
- C-swell-1: the SWELL-KW dataset's participants, conditions, logged modalities (including application names/window switching), and access terms.

## `dubroy-chi10`  (2 topics)
- C-dubroy-1: the distribution of simultaneously open tabs logged per user — most common value, range of per-user medians, maximum.
- C-dubroy-2: number and recruitment of participants, browser and version studied, study period, data availability.

## `chang-chi21`  (3 topics)
- C-chang-1: the number of open tabs at which participants reported feeling overwhelmed — central value and spread.
- C-chang-2: the reported distribution of currently open tabs among participants and any cap on the reported value.
- C-chang-3: whether tab counts were self-reported or logged.

## `mozilla-testpilot10`  (5 topics)
- C-testpilot-1: in the aggregated Test Pilot tables, the mean number of open tabs, the number of participants, the study length and year.
- C-testpilot-2: the median of each user's maximum tab count over the week.
- C-testpilot-3: the tab count reached by the top quarter of users.
- C-testpilot-4: the location, licence and form (raw vs aggregate) of the surviving Test Pilot study data; how participants were recruited.
- C-testpilot-5: whether any publicly available large-scale logged browser tab-count data newer than 2010 exists.

## `singervine-slate10` (references.md only)  (1 topics)
- C-singervine-1: whether the Slate article analyses the Mozilla Test Pilot browsing dataset and which figures it reports.

## Tab-count literature — shared claim  (1 topics)
- C-tabs-1: for each of the three sources, the browser studied and whether it says anything about processes per tab; separately, Chromium's documented process model (how renderer processes relate to tabs/sites).

## `focal-arxiv26`  (5 topics)
- C-focal-1: in the FOCAL paper's DesktopBench description, the interruption split — number of sessions, the structure of a session, what the primary and interrupting activities are.
- C-focal-2: the multitask split — number of sessions, number of templates, and what fields each recorded action carries.
- C-focal-3: how DesktopBench sessions were produced (recorded natural use vs constructed from another dataset) and from which dataset.
- C-focal-4: where DesktopBench is released, its version, the data licence terms and the script licence; whether per-action timestamps are included.
- C-focal-5: authors, title, arXiv number, version and date, venue status.

## `videogui-arxiv24` (references.md only)  (1 topics)
- C-videogui-1: the VideoGUI paper's identity and whether DesktopBench derives from it.

## `schbench` (references.md only)  (1 topics)
- C-schbench-1: schbench's thread structure, what a request does, which latencies and percentiles it reports, its version and author.

## `hackbench` (references.md only)  (2 topics)
- C-hackbench-1: hackbench's defaults (groups, file descriptors, message size, loops), how many tasks those defaults create, what it reports, and where it is distributed (rt-tests, perf).
- C-hackbench-2: the wording of the LWN article at that number about hackbench.

## `stress-ng` (references.md only)  (1 topics)
- C-stress-ng-1: stress-ng's author, licence, stressor categories, and whether it models timing of real application behaviour.

## Unattributed / plain-text external claims (no docs/references.md id)  (9 topics)
- C-plain-1: Chromium's documented process model — which processes a browser session runs, how renderer processes map to tabs or sites, and their process name on Linux.
- C-plain-2: whether ClamAV packages ship a scheduled scan by default (timer/cron) and which process performs it (clamscan, clamd, freshclam).
- C-plain-3: whether GNOME ships tracker-miner-fs(-3), KDE ships baloo_file, and plocate ships an updatedb timer enabled by default; the process names each runs under.
- C-plain-4: the executable/process name Jellyfin uses for transcoding on Linux (and whether it ships a renamed build).
- C-plain-5: for scheduled/automatic ML training, media rendering, transcoding and backup jobs that distributions or vendors start without the user, the process names they run under.
- C-plain-6: the process names under which Windows games run through Proton/Wine on Linux, and whether all game threads/processes share one name.
- C-plain-7: whether public traces of desktop process activity with process names exist; what process-identity fields Azure/Google cluster traces carry.
- C-plain-8: what Phoronix Test Suite and UnixBench measure; whether mobile app-usage datasets record concurrent foreground apps.
- C-plain-9: examples of peer-reviewed papers citing these tools by repository URL.
