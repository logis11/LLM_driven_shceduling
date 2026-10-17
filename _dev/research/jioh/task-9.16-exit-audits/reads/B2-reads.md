# Task 9.16 blind re-read, reader B2: source readings (phase 1)

Blind reading of the source groups numbered 16 to 32 in `claims/dataset-blind-topics.md` (Killourhy and Maxion through the NVIDIA open GPU kernel modules). Each source was read from its primary location before opening any repository description of the claims. All access on 2026-10-17. Local copies live under the scratch root

`/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad/blind/b2/`

written below as `$B2/`. Every sha256 is of the local copy named on the same line. Claim ids (for example D-F2-19) are the ids the topics file gives; each is followed by what the topic asks.

One topic needs the repository's final build: the topic for claim D-F2-44 (the computation of how many core files the CachyOS rule catalogue fully matches). Phase 1 records only the source side of it (the lookup key and the catalogue's name list); the computation on `dataset/build/` is done in phase 2, since opening `dataset/` is barred in phase 1.

---

## 16. Killourhy and Maxion (2009), DSN 2009, and the CMU keystroke dataset page

**Copies read**
- Paper: https://www.cs.cmu.edu/~keystroke/KillourhyMaxion09.pdf, 6 pages, IEEE DSN 2009 camera copy (page footer "978-1-4244-4421-2/09/$25.00 c 2009 IEEE"). `$B2/killourhy/KillourhyMaxion09.pdf`, sha256 `cf36be7bd8b9431cf7cc0e329b2b66baac0d18efc0d9149664aa4029fc6d3170`.
- Dataset page: https://www.cs.cmu.edu/~keystroke/ ("Keystroke Dynamics - Benchmark Data Set"). `$B2/killourhy/index.html`, sha256 `d824cb2169b158f545a2b7537c4ab00422ccea6b6452fc99e437152d7ad9efd5`.

**Topic for claim D-F2-19 (what the released dataset is: subjects, typed string, sessions and repetitions, timing features)**

Dataset page, section "2. The Data":
> "The data consist of keystroke-timing information from 51 subjects (typists), each typing a password (.tie5Roanl) 400 times."

Dataset page, Q2-1:
> "We recruited 51 subjects (typists) from within a university community; all subjects fully completed the study—we did not drop any subjects. All subjects typed the same password, and each subject typed the password 400 times over 8 sessions (50 repetitions per session). They waited at least one day between sessions, to capture some of the day-to-day variation of each subject's typing. The password (.tie5Roanl) was chosen to be representative of a strong 10-character password."

Dataset page, Q2-3:
> "The data are arranged as a table with 34 columns. … The remaining 31 columns present the timing information for the password. … Column names of the form H.key designate a hold time for the named key … DD.key1.key2 designate a keydown-keydown time … UD.key1.key2 designate a keyup-keydown time … Note that UD times can be negative, and that H times and UD times add up to DD times."

Paper, §4.3 "Running subjects" and §4.4 "Extracting timing vectors" (page 3, right column):
> "We recruited 51 subjects from within the university. Subjects completed 8 data-collection sessions (of 50 passwords each), for a total of 400 password-typing samples."
> "we considered the Enter key to be part of the password (effectively making the 10-character password 11 keystrokes long), and we extracted keydown-keydown times, keyup-keydown times, and hold times for all keys in the password. For each password, 31 timing features were extracted … The times are stored in seconds"

Reading: 51 typists, one fixed password `.tie5Roanl` (10 characters, typed with Enter = 11 keystrokes), 8 sessions × 50 repetitions = 400 per subject, at least a day between sessions; 31 timing features per repetition: hold (H), keydown-keydown (DD), keyup-keydown (UD), in seconds. Subjects recruited from a university community; data collected on a Windows XP laptop with an external reference clock.

---

## 17. Sánchez Sánchez et al. (2020), BEHACOM, Data in Brief

**Copy read**: Data in Brief 31 (2020) 105767, doi:10.1016/j.dib.2020.105767, open access (CC BY 4.0), full text via PubMed Central PMC7270191 (OAI-PMH `GetRecord`, metadataPrefix `pmc`). `$B2/behacom/pmc.xml`, sha256 `6671dce8ba27da6ea2f6f4dc036387d02fa6a193196fad4fa91d3f45eaa8b71e`.

**Topic for claim D-F2-20 (number of users and their operating systems, collection period, fields, deposit)**

Abstract:
> "This paper details the methodology and approach conducted to monitor the behaviour of twelve users interacting with their computers for fifty-five consecutive days without preestablished indications or restrictions. The generated dataset, called BEHACOM, contains for each user a set of features that models, in one-minute time windows, the usage of computer resources such as CPU or memory, as well as the activities registered by applications, mouse and keyboard."

§2.1 "Scenario description and selected features":
> "The twelve individuals are right-handed male, with ages ranging from 20 to 45 years old. Eight of them use Windows as operating system, three Linux, and one both. … The first timestamp (UNIX ms) of the dataset is 1574245230186 (Wednesday, 20-Nov-19 10:20:30 UTC) and the last one is 1578995678310 (Tuesday, 14-Jan-20 09:54:38 UTC)."
> "we have considered the following four dimensions: keyboard, mouse, application usage statistics and resource consumption."

Specifications table:
> "Data repository: BEHACOM [1] Data identification number: 10.17632/cg4br62535.2 Direct URL to data: https://data.mendeley.com/datasets/cg4br62535/2 Source code repository: AuthCode [2] Source code URL: https://github.com/CyberDataLab/AuthCode"

§1.1 "Data repository":
> "The data repository of BEHACOM is publicly available in Mendeley Data [1]. … twelve folders, named Useri … Each folder contains a CSV file, named Useri_BEHACOM.csv, with a set of feature vectors that group the behaviours of each individual in time windows of one minute each."

Table 5 (application usage features) includes the foreground application executable name, the penultimate foreground application, "Number of changes between different foreground applications during the time window", seconds of the current application in foreground, and the mean and standard deviation of that application's process count; Table 6 has its CPU and memory percentages.

Reading: 12 users (8 Windows, 3 Linux, 1 both), 55 consecutive days, 2019-11-20 to 2020-01-14; one-minute feature vectors over keyboard, mouse, application usage and resource consumption; deposited on Mendeley Data (doi 10.17632/cg4br62535.2), collector code on GitHub (CyberDataLab/AuthCode).

---

## 18. Yin et al. (2026), FOCAL, arXiv:2604.19541 v2, and the DesktopBench release

**Copies read**
- arXiv abstract page https://arxiv.org/abs/2604.19541v2 (submission history: v1 2026-04-21, v2 Sat 2026-07-18 13:19:51 UTC; no journal-ref, no comments field). `$B2/focal/abs.html`, sha256 `12458d9d4628b85f88f75a623245eeec87a2156b6f46005b901ca732bdc1f317`.
- PDF https://arxiv.org/pdf/2604.19541v2. `$B2/focal/focal-v2.pdf`, sha256 `fb5742cf5e56f3b911cbaab8926db272314334a051886a1580df31bef2998734`.
- DesktopBench release: Hugging Face dataset `HaoranYin/desktopbench`, revision `49c3683061073ecf8cfadf962ce5d563a2e1dd43` (lastModified 2026-07-19), files read: `README.md` (sha256 `9964c7970d3726ee8bb7897be13d808573774fe8ec26d290c666a1bc475c74fb`), `DATA_TERMS.md` (`b7d0449c2f40508e3d39b038960dec1b0ce1b5f56ce8ba182050a4b8a2b11280`), `CITATION.cff` (`cbcf7946532ab63e139f5d3ff97436382416921c2b695cabef285937ca8babfc`), `scripts/prepare_videogui_raw_from_hf.py` (`19ff684067b79904886ea95976158b35e3e4ca8556d2cf00dd87b9d0b6a00f81`), `scripts/rebuild_desktopbench.py` (`02208c991d71934d53f22847c384b7066c307b5374374ad287e550e1703867cf`), `data/interruption_sessions/train.jsonl` (`7448caceec452d35a3b7cd2d69368de3ffe0ab7f8f44e0816ee6a7ff1834e8a6`), `data/multitask_sessions/train.jsonl` (`ffcfac606e2ce95ec8a605bc455a2a726bd1f974029e28c0412e067bfbd0bca7`), all under `$B2/focal/hf/`.

**Topic for claim D-F2-21 (how sessions are produced, how an interruption is structured, session counts)**

Paper §4 "DesktopBench Dataset Construction" (page 4):
> "We reconstruct VideoGUI [14] into DesktopBench, a benchmark for multi-task desktop activity logging. … DesktopBench has two splits: DesktopBench-Multitask for interleaved cross-application workflows and DesktopBench-Interruption for controlled 𝐴 → 𝐵 →𝐴 timelines"

§4.1 "Session Construction":
> "Because VideoGUI was built for single-task automation, it lacks the session organization and metadata required for activity logging. We therefore augment each action with the foreground application name (app) and window title (title)"
> "DesktopBench-Multitask (320 sessions). Sessions are assembled through template-based composition grounded in realistic creative workflows. We use 20 patterns … Each session contains at least two distinct application prefixes, and compatible subtasks may be reused to compose richer workflows. DesktopBench-Interruption (100 sessions). To evaluate robustness to context switching, we construct an 𝐴 → 𝐵 → 𝐴 split in which a long-running creative task 𝐴 is interrupted by a short YouTube browsing task 𝐵 before resuming."

Page 5:
> "DesktopBench is reconstructed from 2,572 screenshots and uses the session as the evaluation unit. It contains 420 sessions in total: 320 in DesktopBench-Multitask and 100 in DesktopBench-Interruption. Multitask sessions contain 2–4 tasks, while Interruption sessions contain exactly two tasks under the 𝐴 → 𝐵 →𝐴 structure. … The average session length is 17.3 actions for DesktopBench-Multitask and 16.5 for DesktopBench-Interruption."

Release README:
> "The 320 multitask sessions materialize to 5,540 actions (17.3125 per session). The 100 interruption sessions materialize to 1,691 actions (16.91 per session). The paper text reports 16.5 for the latter average; `16.91` is the value computed from the released catalog and is recorded as a known discrepancy."

Own count of `data/interruption_sessions/train.jsonl`: 100 rows, each with exactly 3 segments (A, YouTube task, A again); the middle segment's action count is 2 in 24 sessions, 3 in 40, 4 in 8, and 6, 7, 8 or 10 in 7 each. `multitask_sessions` has 320 rows.

Reading: sessions are composed (template-based recomposition of VideoGUI's single-task recordings), not observed user sessions. An interruption session is a creative task A split at a step, a short YouTube task B inserted, then the rest of A. Counts: 320 multitask + 100 interruption = 420.

**Topic for claim D-F2-22 (per-action timing in the released scripts; release location, version and terms; venue status)**

`scripts/prepare_videogui_raw_from_hf.py`, function `build_records` (lines 190–260):
> `duration = 6.0` … `"timestamp": current_ts.isoformat(),` … `"duration": duration,` … `current_ts = current_ts + timedelta(seconds=duration)`

`scripts/rebuild_desktopbench.py`, line 13:
> `DROP_FIELDS = {"timestamp", "duration", "kpm", "cpm", "screenshot_paths"}`

README:
> "This public `v0.1.0` release contains only project-generated annotations, session constructions, ground-truth summaries, provenance, and deterministic reconstruction tools. It does **not** redistribute VideoGUI screenshots …"
> "Scripts are MIT licensed under [LICENSE_CODE](LICENSE_CODE). The dataset itself is marked `license: other`; repository visibility does not grant a redistribution license for the annotations or GT."

DATA_TERMS.md:
> "Public repository visibility is not a license grant: the dataset remains marked `license: other`, and no redistribution, sublicensing, or republication license is granted for annotations or ground-truth summaries unless separately authorized by the applicable rights holder."

CITATION.cff: `version: 0.1.0`, `date-released: 2026-07-19`, `repository: "https://huggingface.co/datasets/HaoranYin/desktopbench"`. The README names a companion code repository `Haoran2099/focal` on GitHub.

Paper, every page header/footer: "Preprint. Under review." The PDF itself carries no release URL (no GitHub or Hugging Face link found in the text).

Reading: the raw-record script assigns every action a fixed 6.0-second duration and a synthetic sequential timestamp from a base time; the rebuild step drops `timestamp` and `duration`. Release: Hugging Face `HaoranYin/desktopbench`, v0.1.0, 2026-07-19; code MIT, data `license: other` with no redistribution grant. Venue: preprint under review (arXiv v2 2026-07-18, no journal reference).

---

## 19. interbench (Kolivas), github.com/ckolivas/interbench at e612a65; LWN 725238 and 1051430; Repology

**Copies read**
- Git clone of https://github.com/ckolivas/interbench.git checked out at `e612a65ce941028ddea804e6b45ccde2750720d2` (committed 2016-10-24, "Hackbench still frequently fails to return so disable it for the time being."). `$B2/interbench/repo/`. Files: `interbench.c` sha256 `a381b94085427cda4169466d3833c272fe4e9672cfbad74a64897621db7f2191`; `interbench.8` `31bc88e508bb7f81cc01a4ef632fbee4f4acb908082140427acba11ca2ee92ee`; `readme` `a67f2b8b3d92896e63f2f03e25dc3f59077eb49192fa353d56cbe0da1f7c0b29`; `LICENSE` `589ed823e9a84c56feb95ac58e7cf384626b9cbf4fda2a907bc36e103de1bad2`; `COPYING` `204d8eff92f95aac4df6c8122bc1505f468f3a901e5a4cc08940e0ede1938994`.
- LWN 725238, Matt Fleming, "A survey of scheduler benchmarks", June 14, 2017, https://lwn.net/Articles/725238/. `$B2/lwn/lwn-725238.html`, sha256 `172dd7f92bc7ccdac0ff1969031c4104a817ecea6fcf7d1b6c3850e74734526f`.
- LWN 1051430, Jake Edge, "Lessons from creating a gaming-oriented scheduler", January 7, 2026, https://lwn.net/Articles/1051430/. `$B2/lwn/lwn-1051430.html`, sha256 `4a7b994f2e866490c36c3add7dffcb784f4e197e04fc642d545565b55c871af8`.
- Repology API https://repology.org/api/v1/project/interbench. `$B2/interbench/repology-interbench.json`, sha256 `5fe4c1cacd88761c40b9ce8812588fe30de6062ca656c2564b2fd2dbbbe6f84b`.

**Topic for claim D-F2-23 (version string; licence files and headers)**

`interbench.c` line 25: `#define INTERBENCH_VERSION	"0.31"`. Man page header: `.TH interbench "8" "March 2006" "Interbench 0.31"`.

`interbench.c` header (lines 7–10):
> "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version."

`COPYING` first lines: "GNU GENERAL PUBLIC LICENSE Version 2, June 1991". `LICENSE` first lines: "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007". `hackbench.c` carries no licence header.

Reading: version 0.31; the repository holds both a GPL-2.0 `COPYING` and a GPL-3.0 `LICENSE`; the source header says GPL version 2 or later.

**Topic for claim D-F2-25 (audio, video and X task constants; how man page and source describe video)**

`interbench.c` lines 490–528:
> `#define AUDIO_INTERVAL	(50000)` / `#define AUDIO_RUN	(AUDIO_INTERVAL / 20)` / `/* We emulate audio by using 5% cpu and waking every 50ms */`
> `/* We emulate video by using 40% cpu and waking for 60fps */` / `#define VIDEO_INTERVAL	(1000000 / 60)` / `#define VIDEO_RUN	(VIDEO_INTERVAL * 40 / 100)`

`interbench.c` lines 530–552 (X):
> "We emulate X by running for a variable percentage of cpu from 0-100% in 1ms chunks." … `for (i = 0 ; i <= 100 ; i++) { j = 100 - i; deadline = periodic_schedule(th, i * 1000, j * 1000, deadline);`

Man page, "What interactive tasks are simulated and how?":
> "Audio is simulated as a thread that tries to run at 50ms intervals that then requires 5% cpu."
> "Video is simulated as a thread that tries to receive cpu 60 times per second and uses 40% cpu. This would be quite a demanding video playback at 60fps."
> "X is simulated as a thread that uses a variable amount of cpu ranging from 0 to 100%. This simulates an idle gui where a window is grabbed and then dragged across the screen."

Reading: audio period 50 000 µs with 2 500 µs run (5 %); video period 16 666 µs (integer 1000000/60) with 40 % run (6 666 µs); X sweeps run i ms and sleep (100−i) ms for i = 0…100. Both man page and source describe video as 60 per second at 40 % CPU.

**Topic for claim D-F2-26 (how a missed period is handled)**

`periodic_schedule`, `interbench.c` lines 397–440:
> `if (interval_usecs && current_time > deadline + interval_usecs) { /* We missed the deadline even before we consumed cpu */ … intervals = (current_time - deadline) / interval_usecs + 1; tb->missed_deadlines += intervals; missed_latency = intervals * interval_usecs; deadline += intervals * interval_usecs; tb->missed_burns += intervals; goto bypass_burn; }`
> "If we meet the deadline we move the deadline forward, otherwise we consider it a missed deadline and dropped frame etc."

Reading: if a period is already overdue by more than one interval before work starts, the burn is skipped, the missed periods are counted, and the deadline jumps forward by whole intervals (the work is dropped, not queued). If work completes after the deadline, the missed intervals are counted and the deadline jumps forward likewise.

**Topic for claim D-F2-27 (Burn default thread count; jitter figure in the documentation)**

Man page and `readme`, "What loads are simulated?": "Burn: A configurable number of threads fully cpu bound (4 by default)." Man page options: "-L Use cpu load of with burn load (default: 4)".

Source at the pinned commit, `interbench.c` line 1520: `ud.cpu_load = sysconf(_SC_NPROCESSORS_ONLN);`; usage text line 1436: `" -L\tUse cpu load of <int> with burn load (default: detected processors)\n"`.

Man page, "What is relevant in the data?":
> "Average humans' limit of perception for jitter is in the order of 7ms. Trained audio observers might notice much less."

Man page, "What is measured": "2. The scheduling jitter is represented by calculating the standard deviation of the latency".

Reading: the documentation says 4 Burn threads by default; the code at e612a65 defaults to the number of online processors (the docs are stale). Jitter figure: about 7 ms human perception limit.

**Topic for claim D-F2-28 (which distributions package interbench; what the two LWN articles say about hackbench, rt-app, stress-ng and interbench)**

Repology, all entries version 0.31 "newest": aosc, aur, freebsd, gentoo, gnuguix, liguros_stable, liguros_develop, opensuse_leap_15_5, opensuse_leap_15_6, void_x86_64. No Debian, Ubuntu, Fedora or official Arch repository entry.

LWN 725238 (introduction):
> "recent kernel commit messages have shown a particular pattern of tools being used (some relatively new), all of which were created specifically for developing scheduler patches."

LWN 725238, Hackbench:
> "Hackbench is a message-passing scheduler benchmark … This benchmark is a stalwart of kernel scheduler testing … Because hackbench calculates an average latency for communicating a fixed amount of data between two tasks, it is most often used by developers who are making changes to the scheduler's load-balancing code."

LWN 725238, Rt-app:
> "Today, ARM and Linaro are using rt-app to trigger specific scheduler code paths. … it is heavily used to model workloads when they are impractical to run directly, such as Android benchmarks on mainline Linux."
> "Many developers run rt-app indirectly via ARM's LISA framework"

LWN 1051430:
> "So, microbenchmarks are of interest as well, but most of the ones he has found for schedulers (e.g. stress-ng and hackbench) are focused on stressing schedulers and measuring the scheduling overhead. That is useful, but improving those numbers does not always lead to better game performance."
> "There are some microbenchmarks that mimic specific workloads; one example is schbench, which is meant to reproduce the scheduling characteristics of production web-server workloads."

Neither LWN article mentions interbench (text search, zero hits in both); LWN 725238 does not mention stress-ng.

Reading: interbench is packaged by about ten community/rolling repositories (AUR, Gentoo, FreeBSD ports, Guix, openSUSE Leap, Void, AOSC, Liguros), not by Debian/Ubuntu/Fedora. LWN 725238 covers hackbench (load-balancing work), schbench, adrestia and rt-app (ARM/Linaro, LISA); LWN 1051430 reports Changwoo Min finding stress-ng and hackbench focused on stress and overhead, not game performance.

---

## 20. rt-app, github.com/scheduler-tools/rt-app at d6f8be41; LWN 725238

**Copies read**: git clone of https://github.com/scheduler-tools/rt-app.git at `d6f8be41107642fd6ab41bc1ab3bb01a486fd00e` (2026-06-10). `README.in` sha256 `a35dec3593020b2fcb0be7ac17ede7c16c06e2a289623db3e582635ff3d3ad93` (`$B2/rtapp/repo/README.in`). LWN 725238 as in source 19.

**Topic for claim D-F2-32 (who LWN says uses rt-app; what the README says rt-app is)**

`README.in`, INTRODUCTION:
> "rt-app is a test application that starts multiple periodic threads in order to simulate a real-time periodic load."

LWN 725238: "Rt-app is a highly configurable real-time workload simulator that accepts a JSON grammar for describing task execution and periodicity." … "Today, ARM and Linaro are using rt-app to trigger specific scheduler code paths." … "Lelli himself uses it primarily for handling bug reports … He also uses it for regression testing" … "Many developers run rt-app indirectly via ARM's LISA framework".

Reading: users named by LWN are ARM and Linaro, Juri Lelli, and developers via ARM's LISA. README: a test application starting periodic threads to simulate a real-time periodic load.

---

## 21. schbench (Mason), git.kernel.org mason/schbench.git tag v1.0; SchedCP (Zheng et al.), arXiv:2509.01245 v4

**Copies read**
- Git clone of https://git.kernel.org/pub/scm/linux/kernel/git/mason/schbench.git, tag `v1.0` (lightweight tag; resolves directly to commit `ab22f3f8766e1bf8a3e8f481c205c8f153dd200d`, Chris Mason, 2023-04-17). `schbench.c` sha256 `2588404b0922e9a67133fef5440cbfcdcabe5b0954fd8943f635ec600a13da82`; `README.md` `b05bdfe9ca6f6e620dd31f476ff5fab9b4c2816b5d586b2febf845f6365bf5e4` (`$B2/schbench/repo/`). No LICENSE or COPYING file in the tree.
- SchedCP: https://arxiv.org/abs/2509.01245v4 (v4 2025-09-30) and PDF https://arxiv.org/pdf/2509.01245v4, 5 pages. `$B2/schedcp/schedcp-v4.pdf` sha256 `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c`; `$B2/schedcp/abs.html` sha256 `f066867fb5950efe6e02bb254fe0ae56dad530ae293feacda0e85cffbbdc3be9`.

**Topic for claim D-F2-33 (tag and commit, copyright holder, licence)**

`schbench.c` lines 1–9:
> "schbench.c … Copyright (C) 2016 Facebook … Chris Mason <clm@fb.com> … GPLv2, portions copied from the kernel and from Jens Axboe's fio"

Reading: tag v1.0 = commit ab22f3f8…; copyright 2016 Facebook; licence GPLv2 stated in the header only (no licence file).

**Topic for claim D-F2-34 (which percentiles v1.0 prints, for which quantities; what one request does)**

`schbench.c` line 104: `static double plist[PLAT_LIST_MAX] = { 20.0, 50.0, 90.0, 99.0, 99.9 };`; lines 101–102: `#define PLIST_FOR_LAT (PLIST_50 | PLIST_90 | PLIST_99 | PLIST_999)` / `#define PLIST_FOR_RPS (PLIST_20 | PLIST_50 | PLIST_90)`; final report lines 1405–1410 print "Wakeup Latencies" and "Request Latencies" with `PLIST_FOR_LAT` and "RPS" with `PLIST_FOR_RPS`; pipe mode adds the 20th percentile to wakeup latencies.

README "Methodology":
> "Workers perform an artificial request comprised of two usleeps (simulating network/disk/locking) and some matrix math."
> "Results are recorded for three primary metrics: Wakeup latency … Request latency: time required to complete our fake request. Requests per second"

Source at v1.0, `worker_thread` lines 1063–1078: in normal mode `gettimeofday(&work_start, NULL); usleep(100);` then `do_work(td);` — `do_work` takes a per-CPU lock (unless `--no-locking`) and runs `operations` rounds of `do_some_math` (README: "-n (--operations): think time operations to perform (def: 5)", "-F (--cache_footprint): cache footprint (kb, def: 256)").

Reading: wakeup and request latencies at p50, p90, p99, p99.9; RPS at p20, p50, p90 (plus min and max lines). One request: a usleep (one 100 µs usleep in the v1.0 source; the README says two usleeps) followed by matrix math under a per-CPU spinlock-style lock.

**Topic for claims D-F2-35 and D-F5-24 (does SchedCP's reference list cite schbench, at what URL)**

SchedCP v4 reference list:
> "[12] Chris Mason. schbench: Scheduler benchmark. https://kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench, 2016. A scheduler benchmark that measures wakeup latency and throughput."

Reading: yes, reference [12], at the kernel.googlesource.com mirror URL (not git.kernel.org), dated 2016.

---

## 22. hackbench in rt-tests, tag v2.11

**Copies read**: git clone of https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git, tag `v2.11` (annotated tag object `711978b9a377f97d4b04e8e1a4a91ef412942ebc`, commit `62da2befac98f811af8e56f2b7992fb09faa33d6`). `src/hackbench/hackbench.8` sha256 `84fe7408e1d820ee88a4114fbeb60cef600ebc70f07d27814030d728e091f3fc`; `src/hackbench/hackbench.c` `36e5b4c86aee10fa7422e16c2a3cb218e7b040a364fe52f943ad8d68b167ac3e`. LWN 725238 as in source 19.

**Topic for claim D-F2-36 (what the man page says hackbench is for; defaults; output)**

`hackbench.8`, DESCRIPTION:
> "Hackbench is both a benchmark and a stress test for the Linux kernel scheduler. It's main job is to create a specified number of pairs of schedulable entities (either threads or traditional processes) which communicate via either sockets or pipes and time how long it takes for each pair to send data back and forth."

EXAMPLES:
> "Running hackbench without any options will give default behaviour, using fork() and sending data between senders and receivers via sockets. … Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks) … Each sender will pass 100 messages of 100 bytes … Time: 0.890"

`hackbench.c` lines 37–40: `datasize = 100; loops = 100; num_groups = 10; num_fds = 20;`; line 570 prints `"Time: %lu.%03lu\n"`.

Reading: scheduler benchmark and stress test; defaults processes via fork(), sockets, 10 groups × 20 senders + 20 receivers (400 tasks), 100 messages of 100 bytes each; output is one elapsed "Time:" in seconds.

**Topic for claim D-F2-37 (what LWN 725238 says hackbench is used for)**

> "Because hackbench calculates an average latency for communicating a fixed amount of data between two tasks, it is most often used by developers who are making changes to the scheduler's load-balancing code. On the flip side, the lack of data for analyzing the entire latency distribution makes it difficult to dig into scheduler latency wakeup issues without using tracing tools."

Reading: most often used by developers changing the scheduler's load-balancing code; called "a stalwart of kernel scheduler testing".

---

## 23. stress-ng (King), commit 3ac9d7a8

**Copies read**: git clone of https://github.com/ColinIanKing/stress-ng.git at `3ac9d7a8aed7048d73d3a308b829b07f30166198` (2026-09-23; `git describe` V0.22.01-24-g3ac9d7a8). `README.md` sha256 `b7e6ff904fc8a2ee177f10443a587ac0000543c9ca699b05c3ea33cf5c29659f`; `stress-ng.1` `0d8bc6227e1d93b54f6940a9a354b66c7fa456d6abf004e827c18f05e45bd243`; `COPYING` `8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643`.

**Topic for claim D-F2-38 (licence; what `--workload` and `--cyclic` do; what the README says about precise benchmarking)**

`COPYING`: "GNU GENERAL PUBLIC LICENSE Version 2, June 1991". `stress-workload.c` header: "Copyright (C) 2023-2026 Colin Ian King. … GNU General Public License … (at your option) any later version."

`stress-ng.1`, `--workload N`:
> "start N workers that exercise the scheduler with items of work that are started at random times with random sleep delays between work items. By default a 100000 microsecond slice of time has 100 work items that start at random times during the slice. The work items by default run for a quanta of 1000 microseconds scaled by the percentage work load (default of 30%). … This emulates bursty scheduled compute, such as handling input packets where one may have lots of work items bunched together or with random unpredictable delays between work items."

`stress-ng.1`, `--cyclic N`:
> "start N workers that exercise schedulers with cyclic nanosecond sleeps. Normally one would just use 1 worker instance with this stressor to get reliable statistics. By default this stressor measures the first 10 thousand latencies and calculates the mean, mode, minimum, maximum latencies along with various latency percentiles … The FIFO scheduling policy is the default."

`README.md`:
> "stress-ng can also measure test throughput rates; this can be useful to observe performance changes across different operating system releases or types of hardware. However, it has never been intended to be used as a precise benchmark test suite, so do NOT use it in this manner."

Reading: GPL-2.0-or-later. `--workload`: random-start work items in a 100 ms slice, 1 ms quantum at 30 % load by default, emulating bursty compute. `--cyclic`: cyclic nanosecond sleeps measuring wake latency (first 10 000 samples, FIFO by default). README: not a precise benchmark suite.

---

## 24. Ananicy, ananicy-cpp v1.2.0, CachyOS `cachyos-settings` 1.4.1, CachyOS ananicy-rules at 03ef03fb

**Copies read**
- Ananicy: GitHub API metadata for `Nefelim4ag/Ananicy` (`$B2/ananicy/ananicy-repo-meta.json`, sha256 `1ebf9df0082a9ed0d573ce7552db4b58e464b7930bf0f7428b0289220c8c87fb`) and a clone at HEAD `1e2cc9a62ba3b6793e59da66aa0039f89e1ad49f` (2021-10-07); `LICENSE` sha256 `f363f0358c85092a82a2458415905f6ff762d62dcdecfbe12fcee159a7ed7733`.
- ananicy-cpp: clone of https://gitlab.com/ananicy-cpp/ananicy-cpp.git, tag `v1.2.0` = commit `cf5ac2eb7b9660794f26f274975066f33359c63e` (2026-03-26). `LICENSE` `6e096bc13fefad3dee878b31edc4b040f5021ac56d0590d1748a09aa45fcf50a`; `README.md` `60cf8c5de365f7f344235a9479c3db66a8738670ba72b84d9ec83b6d5c588ad2`; `src/platform/linux/process.cpp` `9256c305d21591c887c4e038faa39ebc722135c849de87bd8a942a2d7984fa20`; `src/rules.cpp` `9a56344d6baca144a626e0a78be7b5617d865fe338fcc540d820b8416f17770b`.
- CachyOS packaging: clone of https://github.com/CachyOS/CachyOS-PKGBUILDs (HEAD `3933fa84c42affc0646eddc6723a48d7ca6a90d5`, 2026-10-17; `cachyos-settings/PKGBUILD` last changed in `244473b45de57b1b33e1fb00e429ea78c66f5a2f`, 2026-09-23). `cachyos-settings/PKGBUILD` `13451f633724b71a355c9e196de3d0f190029e006166c68791f270fb29d1e1c4`; `cachyos-settings/cachyos-settings.install` `806cd2b00996f0baf914ed5ce427fa760f0484a0eed8ac31214e04313fd53f5f`; `cachyos-ananicy-rules/PKGBUILD` `22bf2b7b98c90e6b98aa13bfd6322e51c4fbdd1aba281e2c764afa102e31efdb`. Settings source clone https://github.com/CachyOS/CachyOS-Settings tag `1.4.1` = `764693fe2863bc2b00db6ad6f4c1d57cded739f2` (2026-09-22).
- CachyOS mirror listing https://mirror.cachyos.org/repo/x86_64_v3/cachyos-extra-v3/ (`$B2/ananicy/idx-cachyos-extra-v3.html`, sha256 `77bceac7581358ecf500bf3e9d0eaad5c09e31e58d1efdcff78bfe1a2be6ce50`) and `x86_64/cachyos/`; Arch Linux package search JSON for `ananicy-cpp`.
- CachyOS ananicy-rules: clone of https://github.com/CachyOS/ananicy-rules at `03ef03fbf7e834385377432ccecaedd32e3414bb` (2026-09-08, "Merge pull request #605 from Tiagoquix/samp"; `git describe` = tag 1.1.49). `00-types.types` `667d89cb61a949ac9b6595f2f318dc452b65c735d8cd6d4fcd5f934dc940591d`; `README.md` `0886ec1f23a1ef772e676ba65bc13961ce7942bec6e0dc9d0936a4f60b16b7ed`; `00-default/Audio-Video/audioserver.rules` `3b8b4a9d6f52298e7f9ac738615909846932645ec9af2edf9ed4c8b1baa41bd5`. Parsed rule list saved as `/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad/rules.json`.

**Topic for claim D-F2-39 (Ananicy repository status and licence; ananicy-cpp licence, version on CachyOS, self-description, rule fields, lineage)**

GitHub metadata for Nefelim4ag/Ananicy: `"archived":true`, `"license":"GPL-3.0"`, `"pushed_at":"2023-03-21T15:03:42Z"`, description "Ananicy - is Another auto nice daemon, with community rules support". `LICENSE`: GPL version 3.

ananicy-cpp `LICENSE`: "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007". README:
> "[Ananicy](https://github.com/Nefelim4ag/Ananicy) rewritten in C++ for much lower CPU and memory usage." … "_Beta status_" … "It should be a fully drop-in replacement from Ananicy."

README rule fields: `nice` (−20…19), `latency_nice` (−20…19, "A additonal kernel patch is needed"), `sched` (fifo, rr, normal, batch, idle), `rtprio`, `ioclass` (best-effort, realtime, idle, none), `ionice` (0…7), `oom_score_adj`, `cpuset`, `cgroup`, `type`.

Versions: CachyOS `cachyos-extra-v3` lists `ananicy-cpp-1.2.0-1.1-x86_64_v3.pkg.tar.zst`; CachyOS `x86_64/cachyos` lists `ananicy-cpp-git-1.1.1.r29.gcf5ac2e-1` (the same commit cf5ac2e as v1.2.0); Arch `extra` has ananicy-cpp 1.2.0-1. Git authorship of ananicy-cpp: Antoine Viallon 244 commits, Vladislav Nepogodin 186.

Reading: Ananicy archived, GPL-3.0; ananicy-cpp GPL-3.0, a C++ rewrite of Ananicy marked beta, version 1.2.0 on CachyOS.

**Topic for claim D-F2-40 (which process attribute ananicy-cpp matches rules against)**

`src/platform/linux/process.cpp`, `get_command_from_pid` (v1.2.0): first the "Cmdline method": `cmdline[0].substr(exe_name_begin + 1)` (the basename of argv[0]); if the cmdline is empty, the "Exe method": the filename of the `/proc/<pid>/exe` link; then the "Comm method": `/proc/<pid>/comm`. The worker does `rules->get_rule(p.name)`, and `Rules::get_rule` looks the name up in `m_program_rules` exactly (regex rules only with `ENABLE_REGEX_SUPPORT` and a `name_regex` field). The BPF event path takes `get_command_from_pid` as well and strips a Windows path for names ending in `.exe`.

Reading: the lookup key is the basename of argv[0] from `/proc/<pid>/cmdline`, falling back to the exe link's basename, then to `comm`; matched by exact string equality against rule `name`.

**Topic for claim D-F2-41 (does CachyOS install and enable ananicy-cpp, with which rules package)**

`cachyos-settings/PKGBUILD`: `pkgver=1.4.1` … `depends=( zram-generator ananicy-cpp cachyos-ananicy-rules inxi "systemd>=256" … )`.

`cachyos-settings.install`:
> `SERVICES=("ananicy-cpp" "systemd-resolved" "systemd-oomd")` … `post_install() { echo "Enabling services..."; for service in "${SERVICES[@]}"; do systemctl enable "$service"; done`

`cachyos-ananicy-rules/PKGBUILD`: `pkgver=1.1.49`, `url='https://github.com/CachyOS/ananicy-rules'`, `source=("${_gitname}::git+$url.git#tag=${pkgver}")`, installs into `/etc/ananicy.d`.

Reading: yes; cachyos-settings 1.4.1 depends on ananicy-cpp and cachyos-ananicy-rules and its install script enables the ananicy-cpp service; the rules package is cachyos-ananicy-rules 1.1.49, built from tag 1.1.49 (which is commit 03ef03fb).

**Topic for claim D-F2-42 (at the commit: number of rules and types, values set, maintainer)**

`00-types.types` defines 15 types: Game (nice −5, ioclass best-effort, sched normal), Player-Audio (−4), Player-Video (−4), Image-View (−4), Doc-View (−4), LowLatency_RT (nice −12, best-effort), BG_CPUIO (nice 16, ioclass idle, sched idle), BG_CPU (nice 14, best-effort, sched idle), Launcher (nice 16, idle, sched normal), Heavy_CPU (nice 9, best-effort, ionice 7), Chat (nice −3, best-effort, ionice 7), Service (nice 10, best-effort, ionice 6), IN_DIFF (nice 0, best-effort, ionice 7), OOM_KILL (oom_score_adj 1000), OOM_NO_KILL (oom_score_adj −1000).

Own count over `00-default/**/*.rules`: 361 rule files, 15 814 rule lines (all parse as JSON), 15 812 distinct names; by type: Game 13 529, BG_CPUIO 1 615, Service 194, Doc-View 160, LowLatency_RT 109, Chat 51, Heavy_CPU 33, Image-View 32, Player-Audio 28, Launcher 24, Player-Video 24, IN_DIFF 10, OOM_NO_KILL 2, no type 2, `TODO` 1. Per-rule overrides use only `ionice` (9 rules), `nice` (3), `ioclass` (2), `oom_score_adj` (1). No rule or type sets `latency_nice`, `cpuset` or `cgroup`.

`README.md`: "This is a ananicy-cpp-rules collection for ananicy-cpp maintained by the CachyOS team and the community." Top git authors at the commit: Luka Ogadze 1 221 commits, Matias 407, pollux78 142.

Reading: about 15.8 thousand rules, 15 types; values are nice, sched policy, I/O class and level, and OOM score adjustment; maintained by the CachyOS team and community.

**Topic for claim D-F2-43 (what the catalogue sets for audio servers, file indexers and compilers; does it distinguish wanted from unwanted background work)**

`00-default/Audio-Video/audioserver.rules`: `{ "name": "pipewire", "type": "LowLatency_RT" }`, `pipewire-pulse`, `wireplumber`, `pulseaudio` all LowLatency_RT (nice −12).

File indexers: `00-default/DEs-and-WMs/plasma.rules` — `baloo_file`, `baloorunner`, `baloo_file_extractor` BG_CPUIO; `recoll.rules` — `recollindex` BG_CPUIO. No rule for `tracker-miner-fs-3`, `tracker-extract-3` or `localsearch` (search over all rule files).

Compilers: no rule named gcc, g++, cc1, cc1plus, clang, rustc, cargo, make, ninja, ld, as or cmake; development rules are for IDE/tools (for example `clangd` Service, `cmake-gui` BG_CPUIO).

`00-types.types` comments: BG_CPUIO "Background CPU/IO it's needed, but it must be as silent as possible"; BG_CPU "Background CPU but demands more I/O, One example: File Synchronization"; Launcher "Runs quietly but may spawn foreground or latency-sensitive workloads".

Reading: audio servers get nice −12; the KDE and Recoll indexers get nice 16 + SCHED_IDLE + idle I/O; GNOME's Tracker has no rule; compilers have no rules. The catalogue classifies by process name only; no type marks a background job as user-requested versus unrequested (background is a single class of "as silent as possible", with BG_CPU and Launcher variants).

**Topic for claim D-F2-44 (source side only)**: the lookup key is the argv[0] basename as recorded under D-F2-40; the name set is the 15 812 distinct `name` values of the parsed rule list. The computation over `dataset/build/` is in phase 2.

---

## 25. Five Directions OpTC data release documentation at 5b108604; University of Helsinki Carat Top 1000 page

**Copies read**
- Clone of https://github.com/FiveDirections/OpTC-data at `5b108604f11f767aa11ea79ff827595f3fad15fd` (2020-06-17). `README.md` sha256 `bbbeca5d5a861ffc765a6d42ddd19cb84acb93861226b4b93887bb950e121074`; `ecar.md` `1df4539c49963cc49b783580033fe1ec68bbae68434abf29da83c47b5d26d16b`.
- https://www.cs.helsinki.fi/group/carat/data-sharing/ ("Carat Top 1000 Users Long-Term App Usage Dataset"). `$B2/carat/data-sharing.html`, sha256 `a3f3e5fed2761ac72af6e0f3434aa54d86a1b2c6544ef32b1c9b971fc15768b2`.

**Topic for claim D-F2-45 (which events and fields OpTC documents, from which endpoints)**

`README.md`:
> "Each Windows 10 endpoint is equipped with an endpoint sensor that monitors host events, packs them into JSON records, and sends them to Kafka. As these records flow into Kafka, a translation server aggregates them into new data records in a format called eCAR"
> "Due to constraints in collection data space during the evaluation, data from five hundred hosts was collected rather than from the full set of one-thousand hosts."
> "ecar-bro: Contains the eCAR FLOW-START events annotated with the bro-id of the flow"

`ecar.md`:
> "CAR defines a three tuple object-action-fields to describe an event." … "timestamp_ms long int - time since epoch / id string - UUID of this object / hostname string / objectID string - UUID of the Object in event / object ObjectType / action ActionType / actorID … pid int - process ID / tid int - thread ID / principal string … properties map of strings"
> Example: `"object": "PROCESS", "action": "CREATE", … "ppid": 6260, … "properties": { "parent_image_path": …, "command_line": …, "image_path": …`

Reading: eCAR object/action events (process create shown; FLOW-START named in the manifest; file and module loads named in the errata) with timestamp, host, object/actor UUIDs, pid/ppid/tid, principal and a properties map (image path, command line, parent image path). Endpoints: Windows 10 enterprise hosts, 500 of 1 000 collected, red-team exercise. The documentation does not give a full ObjectType/ActionType list.

**Topic for claim D-F2-46 (what a Carat sample records about running applications)**

> "The app collected application usage and battery level information every time the battery level changed by 1%, as allowed by the mobile operating system."
> "For each user, the dataset includes a time series of data samples, the following fields in JSON format: uuid … timestamp … batteryLevel … batteryStatus … timeZone … mobileCountryCode … apps (app usage data, see below) Where app usage is a list of JSON objects with the following attributes: processName (App Android package name) priority (background, foreground, etc, see Android documentation)"

Reading: each sample (taken at 1 % battery change) lists running apps as Android package name plus Android process importance ("priority": background, foreground, etc.). No CPU usage or duration per app.

---

## 26. O'Callahan et al. (2017), USENIX ATC '17; Coetzee et al. (2012), arXiv:1203.2704; linux-6.6 Documentation; SCHED_AUTOGROUP Kconfig

**Copies read**
- https://www.usenix.org/system/files/conference/atc17/atc17-o_callahan.pdf, 15 pages, USENIX ATC '17 proceedings copy. `$B2/ocallahan/atc17-o_callahan.pdf`, sha256 `589ec37978260f968312288061e710e64b58e2e652c8479649694403ac037772`.
- https://arxiv.org/abs/1203.2704 (v1 only, 2012-03-13) and PDF v1. `$B2/coetzee/coetzee.pdf` sha256 `637cbce65f2ceceed18434f59efadbfd54dc3bdcfdc85ee5f6cb75fd4ae882b9`; `$B2/coetzee/abs.html` `607f1014e1e46c2fc4e5e4ebc9748faa626ed2dc0f5ce4b64dbeabcc8400aec4`.
- Linux v6.6: sparse shallow clone of git.kernel.org torvalds/linux.git at tag v6.6 = `ffc253263a1375a65fa6c9f62a893e9767fbebfa` (Documentation/, init/, kernel/sched/; 9 462 files under Documentation). `init/Kconfig` sha256 `6c5442c33760782fce0b93126f5a6966cf9fe3dab3d109827f473e7ddcc5ca7a`.

**Topic for claim D-F3-01 (build workload behind the process count; section)**

§4.1 "Workloads":
> "make builds DynamoRio [8] (version 6.1.0) with make -j8 (-j8 omitted when restricting to a single core). This tests potentially-parallel execution of many short-lived processes."

Reading: DynamoRIO 6.1.0 built with `make -j8`, §4.1 (workloads) on a quad-core Skylake laptop (8 SMT threads), Fedora Core 23.

**Topic for claim D-F3-02 (what exactly the count counts; does the paper say what the processes run)**

§4.3 "Observations":
> "Overhead on make is significantly higher than for the other workloads. Forcing make onto a single core imposes major slowdown. Also, make forks and execs 2430 processes, mostly short-lived. (The next most prolific workload is sambatest with 89.) In-process system-call interception only starts working in a process once the interception library has been loaded, but at least 80 system calls are performed before that completes, so its effectiveness is limited for short-lived processes."

Reading: 2 430 processes forked and exec'd during the make workload, "mostly short-lived"; the paper does not say which programs those processes are (no breakdown into compiler, shell, etc.).

**Topic for claims D-F3-03 and D-F3-04 (what the preprint says about processes in builds; which builds it names)**

Coetzee et al., "Preliminary experimental results":
> "Given enough concurrent processes, this build scaled to 85% the time of a parallel make build of the Linux kernel."
> "In practice, even with caching, the system added too much overhead to be practical due to the Linux kernel build's enormous number of short-lived processes like cp and mkdir. This is less likely to be an issue in a more monolithic build system."

"Task and resource granularity":
> "Generally the most fine-grained task possible is an execution of a build process … a large number of processes leads to a large number of tasks and a large dependency graph"

Reading: the preprint gives no process count; it names the Linux kernel build (and generic make builds), saying it has an "enormous number of short-lived processes like cp and mkdir".

**Topic for claim D-F3-06 (next most prolific workload; whether linux-6.6 Documentation mentions `sched_child_runs_first`; SCHED_AUTOGROUP help text)**

O'Callahan §4.3: "(The next most prolific workload is sambatest with 89.)" — stated in the text, not in Table 1.

Linux v6.6: `grep -r child_runs_first Documentation` returns no file. The sysctl exists in code: `kernel/sched/fair.c:149: .procname = "sched_child_runs_first",`.

`init/Kconfig` lines 1261–1271:
> "config SCHED_AUTOGROUP … help This option optimizes the scheduler for common desktop workloads by automatically creating and populating task groups. This separation of workloads isolates aggressive CPU burners (like build jobs) from desktop applications. Task group autogeneration is currently based upon task session."

Reading: sambatest with 89 processes; Documentation at v6.6 does not mention `sched_child_runs_first`; the autogroup help says it isolates "aggressive CPU burners (like build jobs) from desktop applications", grouping by session.

---

## 27. SchedCP: Zheng et al. (2025), "Towards Agentic OS", arXiv:2509.01245 v4

**Copy read**: as in source 21 (`$B2/schedcp/schedcp-v4.pdf`, sha256 `cce49d3c0ff5466cafc3b921373f6d43df2adcb97e38b40c9d45e3b21206e97c`). arXiv stamp on page 1: "arXiv:2509.01245v4 [cs.AI] 30 Sep 2025"; footer "Preprint."

**Topic for claims D-F3-05 and D-F5-22 (kernel-compilation workload: kernel version, configuration, make options; gain over default scheduler)**

§5 "Preliminary Evaluation":
> "Evaluation uses two machines: 86-core Intel Xeon 6787P with 758GB RAM running Linux 6.14, and 8-core Intel Core Ultra 7 258V with 30GB RAM running Linux 6.13. Agents use Claude Code (Opus 4), testing each case three times and averaging results."
> "Scheduler Configuration: For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered for 16% additional gain, reaching 1.79× total improvement over EEVDF (Figure 2a)."

Figure 2a labels: "7.60s 1.79×", "8.31s 1.63×", "13.57s"; caption "(a) AI configured scheduler for Linux build time". Introduction: "sched-agent achieves up to 1.79× performance on kernel compilation".

Reading: Linux 6.14 source, `tinyconfig`, `make -j 172`; 1.79× over EEVDF (13.57 s to 7.60 s), 1.63× with scx_rusty first.

**Topic for claim D-F5-23 (where the phrase about process lifetimes appears: author text or agent output)**

§4 "sched-agent: A Multi-Agent Framework for OS Optimization":
> "The Observation Agent builds Workload Profiles by querying the Workload Analysis Engine strategically … synthesizing data into natural language descriptions and optimization goals while managing cost-precision tradeoffs. For kernel compilation, it produces profiles like "CPU-intensive parallel compilation with short-lived processes, inter-process dependencies, targeting makespan minimization.""

Reading: the "short-lived processes" phrase is quoted as an example of a profile the Observation Agent produces (agent output), in §4, not an author measurement.

---

## 28. GNU make 4.4.1 manual (`doc/make.texi`); DKMS 3.0.11 as Ubuntu 24.04 packages it

**Copies read**
- https://ftp.gnu.org/gnu/make/make-4.4.1.tar.gz, `$B2/make/make-4.4.1.tar.gz` sha256 `dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3`; extracted `doc/make.texi` sha256 `4bc3c176c7eacefae7fdafd0665138372943f9e15cf6b6e816ad8062a31689dd`.
- DKMS: Launchpad shows `dkms 3.0.11-1ubuntu13` Published in noble Release (2024-04-13). Downloaded from http://archive.ubuntu.com/ubuntu/pool/main/d/dkms/: `dkms_3.0.11-1ubuntu13_all.deb` sha256 `18d098c65e3002040afc11f80656e84377551a5d1bdcd3933cdf6ae2e58dcd75`, plus `.dsc`, `.orig.tar.gz`, `.debian.tar.xz`. Extracted `usr/sbin/dkms` sha256 `3631986f06506124c7e2390abeabd8b30d5eb75025b0c373a89ee622180cc00e`; `etc/kernel/postinst.d/dkms` `6676f59b21b9678f05bc2d74afe613120aa1fbf08971ab7d1f319f962ac82a7f`.

**Topic for claim D-F3-07 (make's default number of parallel jobs; parallelism DKMS uses)**

`make.texi`, node "Parallel":
> "Normally, make will execute only one recipe at a time, waiting for it to finish before executing the next." … "If the -j option is followed by an integer, this is the number of recipes to execute at once; this is called the number of job slots. If there is nothing looking like an integer after the -j option, there is no limit on the number of job slots. The default number of job slots is one, which means serial execution (one thing at a time)."

`usr/sbin/dkms` lines 178–188 and 2593–2597:
> "Find out how many CPUs there are so that we may pass an appropriate -j option to make. Ignore hyperthreading for now." … `if [ -x /usr/bin/nproc ]; then nproc else echo "1"` … `# Default to -j<number of CPUs>` `parallel_jobs=${parallel_jobs:-$(get_num_cpus)}`

Line 1113: `local the_make_command="${make_command/#make/make -j$parallel_jobs KERNELRELEASE=$kernelver}"`

Reading: make defaults to one job slot; DKMS defaults to `-j$(nproc)` (one job per online CPU), overridable with `-j`, inserted only when the module's MAKE command begins with `make`.

**Topic for claim D-F3-09 (what make's jobserver counts: jobs or processes)**

`make.texi`, node "Job Slots":
> "GNU make uses a method called the "jobserver" to control the number of active jobs across recursive invocations." … "Second, every command make starts has one implicit job slot reserved for it before it starts." … "Tools that make invokes which are also able to run multiple operations in parallel, either using multiple threads or multiple processes, can be enhanced to participate in GNU make's job management facility to ensure that the total number of active threads/processes running on the system does not exceed the maximum number of slots"

Reading: the jobserver counts jobs (recipes; one slot per command make starts), not processes; a recipe may spawn many processes inside one slot unless the tool itself participates.

**Topic for claim D-F3-28 (DKMS's kernel install hooks; job count its build passes)**

Hooks shipped in the deb: `/etc/kernel/postinst.d/dkms`, `/etc/kernel/header_postinst.d/dkms`, `/etc/kernel/install.d/dkms`, `/etc/kernel/prerm.d/dkms`. `postinst.d/dkms` and `header_postinst.d/dkms`:
> `if [ -x /usr/lib/dkms/dkms_autoinstaller ]; then exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"; fi`

`/usr/lib/dkms/dkms_autoinstaller` line 75: `dkms autoinstall --kernelver $kernel`. `install.d/dkms`: on `add` runs the postinst hook, on `remove` the prerm hook; `prerm.d/dkms` removes installed modules for that kernel.

Job count: as under D-F3-07, `make -j$parallel_jobs` with `parallel_jobs` defaulting to `nproc`.

Reading: on kernel (or header) installation the postinst hooks run `dkms autoinstall` for the new kernel; builds get `make -j<nproc>`.

---

## 29. Meyer and Bolosky (2011), FAST '11; Dinneen `fm-results-tables`, ASIST21-FSD; Vrable et al. (2009), Cumulus, FAST '09

**Copies read**
- https://www.usenix.org/legacy/event/fast11/tech/full_papers/Meyer.pdf, 13 pages. `$B2/meyer/Meyer.pdf`, sha256 `9c91ba8b42d7a42d39fb78eb4a79cc7b51bfc8e9249558b5db09476609a371c5`.
- Clone of https://github.com/jddinneen/fm-results-tables at `1a5a2436c5ff76295bfda729f5076c5068e6239b` (2021-07-08), folder `ASIST21-FSD`: `1-sample-breakdown.csv` `66b5ed4f73fbf1bb686b9def6127b805e8203ad45cbd1eef594fad2e5ff5d14f`; `2-normal-stats.csv` `37568550d1fb99903c3a2644cb0b2651648dbe6153913b599ed97f66281ef7b6`; `3-lognormal-stats.csv` `68d582d4bd803ef68160cdb486b5afc90be428b1f574897430f4cce2295d912a`.
- https://www.usenix.org/legacy/event/fast09/tech/full_papers/vrable/vrable.pdf, 14 pages. `$B2/vrable/vrable.pdf`, sha256 `7ce5a31c975e09a97e311745544af8f92a026d4c1cb1c8a3710c522410dcfe83`.

**Topic for claim D-F3-13 (file size above which half of all bytes lie)**

Meyer and Bolosky, §1 (Introduction):
> "We find that the previously observed trend toward storage being consumed by files of increasing size continues unabated; half of all bytes are in files larger than 30MB (this figure was 2MB in 2000)."

Abstract and §2: "We collected file system content data from 857 desktop computers at Microsoft over a span of 4 weeks." … "Potential participants were selected randomly from Microsoft employees. … ran autonomously during off hours once per week from September 18 – October 16, 2009."

§4.4.1: "The median file size remains 4K".

Reading: half of all bytes are in files larger than 30 MB (2009, 857 Microsoft desktop Windows file systems); the median file is 4 KB.

**Topic for claim D-F3-14 (median file size for GNU/Linux users in the tables)**

`2-normal-stats.csv`: `linux,4.596679688,2236.45735,148417.2171,265931072,` (columns: Median file size (in KB), Mean, Standard deviation, Maximum).
`3-lognormal-stats.csv`: `linux,10.82777225,1739.766342,24.22256562,` (lognormal median in KB, lognormal mean, lognormal SD). The header of file 2 says "Normal stats are provided for comparison to prior works; please refer to lognormal stats since data are highly skewed".
`1-sample-breakdown.csv`: `operating system,linux,4464785,42,,` (files, participants).

Reading: GNU/Linux median file size 4.597 KB (normal statistics), 10.83 KB lognormal median; 42 participants, 4 464 785 files.

**Topic for claim D-F3-15 (Cumulus daily change rates for personal machines: statistic, days traced)**

§5.1 "Trace Workloads":
> "A user trace is taken from the Cumulus backups of the home directory of one of the author's personal computers, and models the use of remote backup in a home setting. The traces contain a daily record of the metadata of all files in each setting"

Table 2 "Key statistics of the two traces", User column: "Duration (days) 223"; "Update Rates: New data/day 10.3 MB; Changed data/day 29.9 MB; Total data/day 40.2 MB" (Fileserver: 157 days; 9.50 GB, 805 MB, 10.3 GB).

Reading: one personal computer's home directory, 223 days; per-day new 10.3 MB, changed 29.9 MB, total 40.2 MB. The table labels these "data/day" without naming the statistic (it does not say mean or median); file counts and sizes are for the last trace day.

---

## 30. Déjà Dup 45.2; Ubuntu 24.04.5.1 desktop manifests; systemd 255.4, tracker-miners 3.7.1, gnome-session 46.0

**Copies read**
- Déjà Dup: clone of https://gitlab.gnome.org/World/deja-dup.git at tag `45.2` = `585b723da27fdc6ad5c2a3b27858fdc9056f0038` (2023-12-22). `monitor/monitor.vala` `e9f27daa73d72b6c15199ad5c037a9753bf791c52a6ce8843988c791142b18d9`; `monitor/BackupInterface.vala` `1e6d602bab0fea117e25cd7eabd3c6b8c980b70c0a8fe3bff42ab1b648dbcc7e`; `monitor/Scheduler.vala` `498e41fa189ef662cacdbdd729b097ba4bea0356403c013d0839c7f637967116`; `libdeja/CommonUtils.vala` `68af73a61f0080ee448f33772472417d778926fe73251937e0dc6d24b0a02785`; `data/app.gschema.xml.in` `c59ff9d536e806e81367ee9b15ab3d425e16b0a818ef79390032bbe2c9927980`; `libdeja/duplicity/DuplicityJob.vala` `b7fd22e76b4aa9f6f6ad451e3dbb77f5e63503d12d0b4bca02657e04896765e7`; `app/AssistantOperation.vala` `e28befeb350f02e6338954432249f2a8b9575a4e9ba7891cf6114c7d46649faf`. Ubuntu package (Launchpad: `45.2-1build2` Published noble Release 2024-04-04): `deja-dup_45.2-1build2_amd64.deb` `092007f597967e564b326550845ed814a06aa254cd31cc9e198a91da2e14b4e8`; `deja-dup_45.2-1build2.debian.tar.xz` `3556f2b7b9ac275ddba6815b48a46ffe1d4ff31723422d1c327c7299ab09b776` (its `debian/patches/series` is empty).
- Ubuntu 24.04.5.1 desktop: https://releases.ubuntu.com/24.04/ `ubuntu-24.04.5.1-desktop-amd64.manifest` (`6c200933618b2e382e7732b69b247aa5f63ed6600d8ee730d57b02ec74e4f8ff`) and `.list` (`9fb3e8041e7e95b028f5629069295fb079e93499f55ce2c88901afc087895ad2`); ISO sha256 per SHA256SUMS `4da4a0c9035da8e68a59a838674f403f0a54472c78a83b4fb7f78d03588f85a7`. Layer files read from the ISO by HTTP byte-range reads of its ISO 9660 directory: `casper/minimal.manifest` (`31544e9fb82e6c7e4d8f6062f46bc2ec5d7e7061b4df1040036c061d33206a49`), `casper/minimal.standard.manifest` (`99fce3823f2ce2f253ff92f5517f94f0779afa3ade60ff881fc8ef58adb5aa1d`), `casper/minimal.standard.live.manifest` (`d94776bd26ffd5223b271e4616fb272b0fba6a8734cfc2fa7d113f4e25694c07`), `casper/install-sources.yaml` (`3d3e0d097b51c21aeb8d3330de0220e33d29e694dd56c0de5797b8bbc6cb1ec9`). Layer manifests are unified diffs against the layer below, built 2026-09-14.
- systemd: Ubuntu pool `systemd_255.4.orig.tar.gz` (`96e75bd08c57ad401677456fb88ef54a9f05bb1695693013bc6ecce839640fd5`) and `systemd_255.4-1ubuntu8.17.debian.tar.xz` (`4695ff34f83b1f7e6e02bf3cfac2e2a44ac76b6cfc5a38c0081bac6919d547bb`); 255.4-1ubuntu8.17 is the version in the 24.04.5.1 manifest. `units/user/background.slice` `64352a7d8e99827974ac7c51fb1672cfa00b90a0498e49bcf8db212efa2e861e`; `units/user/app.slice` `2f692ece5b1dd36e8a09cb2cca022ce68cca75bda22a1503c2e98ebd6584001e`; `src/xdg-autostart-generator/xdg-autostart-service.c` `eaf0d446ff5087955639d75cb54abc98786c8dd2c6fb3dcbd9c173d3465618ff`. No Ubuntu patch touches the user slices.
- tracker-miners: Ubuntu pool `tracker-miners_3.7.1.orig.tar.xz` (`50a3abe40cfb0b35ced43ec716dbf1368992e444ef7a0babf202c7ac6ab2f6f4`) and `tracker-miners_3.7.1-1ubuntu0.1.debian.tar.xz` (`52f4b191aebcb699178dd635ef52613fe0f9a22eda950998a46ea207a556299e`). `src/miners/fs/tracker-miner-fs.service.in` `a74c3215d280bcb99580d13298eb35a78eb95ee6a5235d4bd501d05ec4e47b81`; `src/miners/fs/tracker-main.c` `511edaf49ecda04d787ba4bf60b62f66867f346e3e9b645381145b676ea3883c`; `src/libtracker-miners-common/tracker-sched.c` `ea780d2ec0d900747eb6de50128f0d3fe0a736f53c40a80cea18f389a9d3e56e`.
- gnome-session: Ubuntu pool `gnome-session_46.0.orig.tar.xz` (`c6e1624af6090bc4e1a191fe2268abfa7a8de07831ca7a57f217e679bf7b9a54`) and `gnome-session_46.0-1ubuntu4.debian.tar.xz` (`d91cfe857e66f71d51d7c7e8ac8f3fc0ebc6e340e3af4bf65d6a08b4b16f4622`).
- gnome-desktop 44.0 (noble ships 44.0-5build2 per the manifest): https://gitlab.gnome.org/GNOME/gnome-desktop/-/raw/44.0/libgnome-desktop/gnome-systemd.c, `$B2/gnomedesktop/gnome-systemd.c` `260e79ad3ecae558e4cb46a02a15dfe0b969acd3d991cdda63085071c3d30816`.

**Topic for claim D-F3-16 (how `deja-dup-monitor` starts a scheduled backup: which processes, when)**

Autostart entry in the Ubuntu deb, `/etc/xdg/autostart/org.gnome.DejaDup.Monitor.desktop`: `Exec=/usr/libexec/deja-dup/deja-dup-monitor`, `X-GNOME-Autostart-Delay=120`.

`monitor/monitor.vala`, `begin_monitoring`:
> "Delay first check to give the network and desktop environment a chance to start up." `var delay_time = 120;` … `Timeout.add_seconds(delay_time, () => {make_first_check(); …`

`monitor/Scheduler.vala`: computes the next run from `last-backup` and `periodic-period`; "if (wait_time > 0 …) … Timeout.add_seconds((uint)secs, …initiate_backup()…) else { debug("Late by %ld seconds. Backing up now."…); initiate_backup(); }"; "this Scheduler class will actually schedule a fresh backup signal every day, until LAST_BACKUP_KEY is set."

`monitor/BackupInterface.vala`, `start_auto`:
> "Done by calling the executable rather than a dbus call because we want to call it with nice / ionice, etc if possible." … `DejaDup.run_deja_dup({"--backup", "--auto"});`

`libdeja/CommonUtils.vala`, `nice_prefix` and `run_deja_dup`:
> `cmd = "ionice -c3 " + cmd; // idle class` … `// chrt's idle class is more-idle than nice, so prefer it` … `cmd = "chrt --idle 0 " + cmd;` … `else if (Environment.find_program_in_path("nice") != null) cmd = "nice -n19 " + cmd;` … `Process.spawn_async(null, argv, …)`

Default tool: `data/app.gschema.xml.in` key `tool` default `'duplicity'`.

Reading: the monitor is started at login (desktop entry delay 120 s), waits a further 120 s before its first check, then fires at the scheduled time or at once if overdue (also on readiness events while overdue). It spawns `chrt --idle 0 ionice -c3 deja-dup --backup --auto` (SCHED_IDLE, idle I/O class), and deja-dup then runs the backup tool (duplicity by default).

**Topic for claim D-F3-18 (Déjà Dup 45.2 defaults: schedule once on, encryption, volume size, password storage)**

`data/app.gschema.xml.in` (identical in the Ubuntu deb's installed schema): `periodic` default `false` ("Whether to automatically back up on a regular schedule."); `periodic-period` default `7` ("The number of days between backups."); `full-backup-period` default `90`; `delete-after` default `0` ("A value of 0 means forever").

`app/AssistantOperation.vala` line 345: `encrypt_enabled.active = true; // always default to encrypted`; lines 370–373 create the "_Remember password" switch with no default set (a `SwitchRow` starts off).

`libdeja/duplicity/DuplicityJob.vala`, `get_volsize`: "duplicity's default is 200MB … Let's just use that" … `return 200;` (megabytes; 1 in testing mode).

`libdeja/CommonUtils.vala`, `store_passphrase`: if remember, `Secret.password_store_sync(get_passphrase_schema(), Secret.COLLECTION_DEFAULT, _("Backup encryption password"), …)`; otherwise the stored password is cleared.

Reading: automatic backups off by default; once turned on, every 7 days; encryption on by default in the setup assistant; 200 MB duplicity volumes; password kept in the Secret Service default collection (the keyring) only if "Remember password" is switched on (off by default).

**Topic for claim D-F3-19 (default or extended desktop install)**

`casper/install-sources.yaml`: `id: ubuntu-desktop-minimal`, `default: true`, `path: minimal.squashfs`, name "Ubuntu Desktop (minimized)"; `id: ubuntu-desktop`, `default: false`, `path: minimal.standard.squashfs`, description "A full featured Ubuntu Desktop."

`casper/minimal.standard.manifest` (diff from minimal to minimal.standard): `+deja-dup	45.2-1build2`, `+duplicity	2.1.4-3ubuntu2`. `deja-dup` does not appear in `casper/minimal.manifest`.

Reading: Déjà Dup is in the extended ("full featured", not default) desktop layer, not in the default minimal install.

**Topic for claim D-F3-21 (slice or scope of the file indexer and backup monitor on the stock desktop; CPU weights)**

`tracker-miner-fs.service.in`: `[Service] Type=dbus … Slice=background.slice … [Install] WantedBy=gnome-session.target`. The Ubuntu package installs `usr/lib/systemd/user/tracker-miner-fs*-3.service`. Its XDG desktop file carries `X-GNOME-HiddenUnderSystemd=true` and `X-systemd-skip=true`; gnome-session 46.0 (`gsm-autostart-app.c` lines 141–150) skips apps with `X-GNOME-HiddenUnderSystemd` when systemd-managed.

systemd 255.4 `units/user/background.slice`: `Description=User Background Tasks Slice … [Slice] CPUWeight=30`. `units/user/app.slice`: `Description=User Application Slice … CPUWeight=100`. `units/user/session.slice`: `CPUWeight=100`. `man/systemd.special.xml` for background.slice: "All services running low-priority background tasks should use this slice. … Examples include non-interactive tasks like file indexing or backup operations where latency is not important."

Backup monitor: gnome-session 46.0 `gsm-session-fill.c` `load_standard_apps` adds autostart apps from the autostart dirs also when systemd-managed; `gsm-autostart-app.c` `app_launched` calls `gnome_start_systemd_scope (priv->desktop_id, pid, …)`; gnome-desktop 44.0 `gnome-systemd.c`: `unit_name = g_strdup_printf ("app-gnome-%s-%d.scope", task_data->name, task_data->pid);` with properties Description, PIDs and CollectMode only (no Slice). systemd 255.4 `src/core/unit.c` `unit_set_default_slice`: in the user manager a non-instance unit without a slice goes to `SPECIAL_APP_SLICE` = "app.slice". (The systemd XDG autostart generator would also use `Slice=app.slice`.) Ubuntu's gnome-session patch `support_autostart_delay.patch` implements `X-GNOME-Autostart-Delay`.

Reading: Tracker's file miner runs as a user service in background.slice (CPUWeight 30); the Déjà Dup monitor is launched by gnome-session into a transient `app-gnome-org.gnome.DejaDup.Monitor-<pid>.scope` in app.slice (CPUWeight 100), and the backup it spawns stays in that scope. Weights are relative among sibling slices of the user manager.

**Topic for claim D-F3-32 (is Tracker's file miner in the default install, at which version)**

`casper/minimal.manifest`: `+tracker	3.7.1-1build1`, `+tracker-extract	3.7.1-1ubuntu0.1`, `+tracker-miner-fs	3.7.1-1ubuntu0.1`.

Reading: yes, tracker-miner-fs 3.7.1-1ubuntu0.1 (upstream 3.7.1) is in the default minimal layer.

**Topic for claim D-F3-34 (scheduling policy and nice level Tracker 3.7.1's threads set on themselves)**

`tracker-main.c`, `initialize_priority_and_scheduling` (called early in `main`, line 821, "This makes sure we don't steal all the system's resources"):
> `/* Set CPU priority */ tracker_sched_idle ();` `/* Set disk IO priority and scheduling */ tracker_ioprio_init ();` … `TRACKER_NOTE (CONFIG, g_message ("Setting priority nice level to 19"));` … `if (nice (19) == -1 && errno != 0)`

`tracker-sched.c`:
> "Sets the priority of the current thread to SCHED_IDLE. Threads spawned from a SCHED_IDLE thread will inherit the same priority, so you just need to call this function when the main thread starts to set priority for the whole process." … `pthread_setschedparam (pthread_self(), SCHED_IDLE, &sp);`

`tracker-ioprio.c`: `set_io_priority_idle ()`, falling back to best-effort level 7.

Reading: SCHED_IDLE plus nice 19 (and idle I/O class), set by the main thread at start and inherited by threads it spawns.

---

## 31. unattended-upgrades 2.9.1+nmu4ubuntu1; APT 2.8.3 systemd units; glibc 2.39-0ubuntu8.8

**Copies read**
- http://archive.ubuntu.com/ubuntu/pool/main/u/unattended-upgrades/: `unattended-upgrades_2.9.1+nmu4ubuntu1.tar.xz` (`722e25650392a1c0f2cbafe2c9cf5bc91e3961009908118208c3e1d7d409d3fe`), `_all.deb` (`13c576c7d8184f509d5ddc4d75bec6e62ef3f745319cce60f8131f401091113b`), `.dsc`.
- http://archive.ubuntu.com/ubuntu/pool/main/a/apt/: `apt_2.8.3.tar.xz` (`088522b3613b28fdbcfa61f1f7e476bf6dc6b0120a8f74409e9527580c9f9d3b`), `.dsc`.
- glibc: Launchpad API `getPublishedSources` for glibc in noble (`$B2/glibc/lp-glibc-noble-sources.json`, `96d8f886f184f4338d475c57ef7c3df03cbfa37e7cb8045603b09a336e84e05e`); `getPublishedBinaries` (all, not only active) for source publication 18645059 (`$B2/glibc/lp-glibc-8.8-security-binaries.json`, `d3eb4b94591106dcc4aa4a7a1df1b8b807b15683fae1568fd523c195349f8153`); `glibc_2.39-0ubuntu8.8_source.changes` (`9c14ceae746de2d90902a921205df28cdb2d9b8533d92e550be5e1decca96cba`) and `glibc_2.39-0ubuntu8.8.dsc` (`69c09b540d03e56b3adea7c4af98b862bfc36789795c9e21d37e58e699f57b00`) from launchpad.net `+files`.

**Topic for claim D-F3-23 (is unattended-upgrades in the default install and enabled by default)**

`casper/minimal.manifest` (24.04.5.1): `+unattended-upgrades	2.9.1+nmu4ubuntu1`.

`debian/templates`:
> "Template: unattended-upgrades/enable_auto_updates Type: boolean Default: true _Description: Automatically download and install stable updates?"

`debian/postinst`: `db_get unattended-upgrades/enable_auto_updates` … `if [ "${RET}" = "true" ]; then NEWFILE="/usr/share/unattended-upgrades/20auto-upgrades"; ucf … "$CONFIG"` with `CONFIG="/etc/apt/apt.conf.d/20auto-upgrades"`. `data/20auto-upgrades`: `APT::Periodic::Update-Package-Lists "1"; APT::Periodic::Unattended-Upgrade "1";`. `data/50unattended-upgrades.Ubuntu` Allowed-Origins: `${distro_codename}`, `${distro_codename}-security`, and the ESM security origins.

Reading: yes, in the default minimal install; the debconf default (true) writes `20auto-upgrades` enabling daily list updates and unattended upgrades, from the release and security pockets (plus ESM security).

**Topic for claim D-F3-22 (how apt's units start the daily upgrade: timer schedule, randomised delay, service)**

`debian/apt-daily-upgrade.timer`:
> `[Timer] OnCalendar=*-*-* 6:00` `RandomizedDelaySec=60m` `Persistent=true`

`debian/apt-daily-upgrade.service`:
> `ConditionACPower=true` … `ExecStartPre=-/usr/lib/apt/apt-helper wait-online` `ExecStart=/usr/lib/apt/apt.systemd.daily install` `KillMode=process` `TimeoutStopSec=900`

`debian/apt-daily.timer`: `OnCalendar=*-*-* 6,18:00`, `RandomizedDelaySec=12h`, `Persistent=true`; `apt-daily.service` runs `apt.systemd.daily update`.

Reading: the upgrade timer fires daily at 06:00 with up to 60 minutes random delay (persistent across power-off) and runs `apt-daily-upgrade.service` → `apt.systemd.daily install` (on AC power only). The separate download timer fires at 06:00 and 18:00 with up to 12 h delay.

**Topic for claim D-F3-24 (the 2026-07 glibc security update: version, publication date, binary packages)**

Launchpad: `2.39-0ubuntu8.8 Security Superseded 2026-07-27T12:28:23 UTC` and `Updates Superseded 2026-07-27T14:17:51 UTC`; superseded by `2.39-0ubuntu8.9` (Security 2026-09-10).

`.changes`: "Date: Thu, 23 Jul 2026 13:18:13 -0400 … Version: 2.39-0ubuntu8.8 Distribution: noble-security … SECURITY UPDATE … CVE-2026-4046 … CVE-2026-4437 … CVE-2026-4438 … CVE-2026-5435 … CVE-2026-5450 … CVE-2026-5928 …" (the list continues).

Binaries published for that source publication: 127 binary publications across 7 architectures, 28 distinct names, 19 without the `-dbgsym` suffix: glibc-doc, glibc-source, libc-bin, libc-dev-bin, libc-devtools, libc6, libc6-amd64, libc6-dbg, libc6-dev, libc6-dev-amd64, libc6-dev-i386, libc6-dev-s390, libc6-dev-x32, libc6-i386, libc6-s390, libc6-x32, locales, locales-all, nscd. For amd64: glibc-doc, glibc-source, libc-bin, libc-dev-bin, libc-devtools, libc6, libc6-dbg, libc6-dev, libc6-dev-i386, libc6-dev-x32, libc6-i386, libc6-x32, locales, locales-all, nscd (15) plus 7 dbgsym.

Note: the 24.04.5.1 minimal layer already carries `libc6:amd64 2.39-0ubuntu8.9`.

Reading: version 2.39-0ubuntu8.8, published to noble-security on 2026-07-27 (uploaded 2026-07-23), now superseded by 8.9; 15 non-debug binary packages on amd64 (libc6, libc-bin, locales, …).

---

## 32. NVIDIA open GPU kernel modules 595.91.07 as Ubuntu packages them; the Ubuntu archive's kernel publication history

**Copies read**
- Launchpad: `nvidia-graphics-drivers-595 595.91.07-0ubuntu0.24.04.1` in noble Updates (published 2026-09-15, multiverse, now Superseded by 595.99.02); `nvidia-graphics-drivers-595-server 595.91.07-0ubuntu0.24.04.1` Published in noble Updates (2026-09-15) and Security (2026-10-08). Source files from launchpad.net `+sourcefiles` (the non-server source is no longer in the archive pool): `nvidia-graphics-drivers-595_595.91.07-0ubuntu0.24.04.1.dsc` (`e1df584323a0e94d63624e267aef9a70b15fe57fa5b4332dd360d63909199f84`), `.debian.tar.xz` (`ffad99df6182b74fa932cb204d1c40839452b51ce53a5858a94368fd2d39cbfa`). The `-server` source was not downloaded.
- Launchpad `getPublishedSources` for `linux-hwe-7.0`, `linux-meta-hwe-7.0`, `linux-signed-hwe-7.0` in noble (`$B2/nvidia/lp-linux-hwe-7.0-noble.json`, `ff04b5067e5047104f0b6b9e44b61ee504de5968ae60a2ac86843304f522c992`), and the 24.04.5.1 ISO files listed in source 30.

**Topic for claim D-F3-29 (module package version and branch; how many kernel modules it builds)**

`.dsc` `Binary:` includes `nvidia-dkms-595-open`, `nvidia-kernel-source-595-open`, `nvidia-driver-595-open`; `Version: 595.91.07-0ubuntu0.24.04.1`. `debian/changelog`: "nvidia-graphics-drivers-595 (595.91.07-0ubuntu0.24.04.1) noble; urgency=medium * New upstream version 595.91.07 (LP: #2163130) -- … Sun, 09 Aug 2026". Earlier entry: "New upstream release 595.71.05 UDA".

`debian/dkms_nvidia_open.conf`: `PACKAGE_VERSION="595.91.07"`, `BUILT_MODULE_NAME[0]="nvidia"`, `[1]="nvidia-modeset"`, `[2]="nvidia-drm"`, `PROCS_NUM=\`nproc\``, `[ $PROCS_NUM -gt 16 ] && PROCS_NUM=16`, `MAKE[0]="… 'make' -j$PROCS_NUM … modules"`. `debian/dkms.conf.fragment`: `BUILT_MODULE_NAME[3]="nvidia-uvm"`, `BUILT_MODULE_NAME[4]="nvidia-peermem"`. `debian/rules` lines 156–162: `cp -f …/dkms_nvidia_open.conf …/open-kernel/dkms.conf` and, unless `nvidia-uvm` is disabled (only on i386 and armhf), `cat …/dkms.conf.fragment >> …/open-kernel/dkms.conf`. `nvidia-dkms-595-open.install` puts that `dkms.conf` into `usr/src/nvidia-595.91.07`.

Reading: Ubuntu's `nvidia-dkms-595-open` 595.91.07-0ubuntu0.24.04.1 (branch 595; the source package is `nvidia-graphics-drivers-595`, with a separate `-server` branch at the same upstream version). On amd64 its DKMS config builds 5 kernel modules: nvidia, nvidia-modeset, nvidia-drm, nvidia-uvm, nvidia-peermem, with its own `make -j<nproc, capped at 16>` (the MAKE line does not start with `make`, so DKMS's own `-j` substitution does not apply).

**Topic for claim D-F3-30 (when the newest 24.04 HWE kernel ABI reached `noble-security` in September 2026 and which ABI it replaced; which HWE kernel the 24.04.5.1 installer adds)**

Launchpad `linux-hwe-7.0` in noble (identical dates for linux-meta-hwe-7.0 and linux-signed-hwe-7.0):
> `7.0.0-38.38~24.04.4 Security Published 2026-10-08T12:46:35` / `7.0.0-34.34~24.04.1 Security Superseded 2026-09-23T15:49:46` / `7.0.0-34.34~24.04.1 Updates Superseded 2026-09-22T17:43:27` / `7.0.0-31.31~24.04.1 Security Superseded 2026-09-04T08:56:27` / `7.0.0-31.31~24.04.1 Updates Superseded 2026-09-03T13:46:21` / `7.0.0-30.30~24.04.1 Security Superseded 2026-08-20T23:01:11`

24.04.5.1 ISO: `casper/minimal.standard.live.manifest` adds `linux-generic-hwe-24.04 7.0.0-31.31~24.04.1`, `linux-image-7.0.0-31-generic`, `linux-modules-7.0.0-31-generic`, `linux-headers-7.0.0-31-generic`; the ISO pool (`.list`) carries `/pool/main/l/linux-meta-hwe-7.0/linux-generic-hwe-24.04_7.0.0-31.31~24.04.1_amd64.deb` and `/pool/main/l/linux-signed-hwe-7.0/linux-image-7.0.0-31-generic_7.0.0-31.31~24.04.1_amd64.deb` (also an OEM 6.17.0-1032 kernel and GA 6.8.0-31 images).

Reading: the newest HWE ABI to reach noble-security in September 2026 is 7.0.0-34 (2026-09-23 15:49 UTC), replacing ABI 7.0.0-31 (itself in security since 2026-09-04, replacing 7.0.0-30). The 24.04.5.1 image carries the HWE 7.0 kernel at ABI 7.0.0-31 (linux-generic-hwe-24.04 7.0.0-31.31~24.04.1) in its live layer and pool; the installed-system kernel package selection itself is not stated in the files read (it comes from the installer's pool, which offers this HWE meta-package, the OEM 6.17 meta-package and GA 6.8 images).
