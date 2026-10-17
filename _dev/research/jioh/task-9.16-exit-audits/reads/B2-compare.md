# Task 9.16 blind re-read, reader B2: comparison (phase 2)

Comparison of the repository's wording, at `928aa8fd` (branch `jioh/dataset-rebuild`), with reader B2's blind passages in `reads/B2-reads.md` (written and closed before this file). Scope: the 50 claims of source groups 16 to 32 of `claims/dataset-blind-topics.md`. Each claim was checked over object, unit, statistic, scope and population. Locations are file:line on the current tree; passages are cited by their source number and topic in `B2-reads.md`.

## Summary

| verdict | count |
|---|---|
| SUPPORTED | 41 |
| WORDING-FIX | 8 |
| CONTRADICTED | 1 |
| NOT IN SOURCE | 0 |
| UNVERIFIABLE | 0 |

| claim | what it is about | verdict |
|---|---|---|
| D-F2-19 | the CMU keystroke dataset (Killourhy and Maxion) | WORDING-FIX |
| D-F2-20 | BEHACOM's users, platforms, period, fields | SUPPORTED |
| D-F2-21 | DesktopBench sessions: composed, the A → B → A split, counts | SUPPORTED |
| D-F2-22 | DesktopBench release: 6.0 s per action, v0.1.0, terms, preprint | SUPPORTED |
| D-F2-23 | interbench pin, version, licence | SUPPORTED |
| D-F2-25 | interbench's audio, video and X constants | SUPPORTED |
| D-F2-26 | interbench's missed-period handling | SUPPORTED |
| D-F2-27 | interbench's Burn default and its 7 ms jitter figure | WORDING-FIX |
| D-F2-28 | interbench packaging; LWN precedents for hackbench, rt-app, stress-ng | SUPPORTED |
| D-F2-32 | rt-app's users per LWN and its documentation | SUPPORTED |
| D-F2-33 | schbench pin, copyright, licence | SUPPORTED |
| D-F2-34 | schbench's printed percentiles and one request | SUPPORTED |
| D-F2-35 | SchedCP cites schbench at kernel.googlesource.com | SUPPORTED |
| D-F2-36 | hackbench pin, purpose, defaults, output | SUPPORTED |
| D-F2-37 | LWN on hackbench | SUPPORTED |
| D-F2-38 | stress-ng licence, `--workload`, `--cyclic`, README disclaimer | SUPPORTED |
| D-F2-39 | Ananicy and ananicy-cpp: status, licences, self-description, fields | WORDING-FIX |
| D-F2-40 | ananicy-cpp's rule lookup key | SUPPORTED |
| D-F2-41 | CachyOS installs and enables ananicy-cpp with the catalogue | SUPPORTED |
| D-F2-42 | the CachyOS rule catalogue's counts, types, values, maintainers | SUPPORTED |
| D-F2-43 | the catalogue on audio servers, indexers, compilers; no wanted/unwanted split | WORDING-FIX |
| D-F2-44 | how much of the core set the shipped catalogue matches | WORDING-FIX |
| D-F2-45 | DARPA OpTC: what its release documents | SUPPORTED |
| D-F2-46 | Carat: running apps per sample | SUPPORTED |
| D-F3-01 | the build behind O'Callahan et al.'s 2 430 processes | SUPPORTED |
| D-F3-02 | what that count grounds ("compiler children") | WORDING-FIX |
| D-F3-03 | Coetzee et al. on the Linux kernel build's short-lived processes | SUPPORTED |
| D-F3-04 | the reach of Coetzee's corroboration ("builds") | WORDING-FIX |
| D-F3-05 | SchedCP's kernel-compilation workload | SUPPORTED |
| D-F3-06 | the source-vetting correction: sambatest, kernel docs, autogroup | SUPPORTED |
| D-F3-07 | the build tools' documented default parallelism | CONTRADICTED |
| D-F3-09 | make's jobserver counts jobs | SUPPORTED |
| D-F3-13 | Meyer and Bolosky: half the bytes in files over 30 MB | SUPPORTED |
| D-F3-14 | GNU/Linux users' median file size, 4.60 KB | SUPPORTED |
| D-F3-15 | Cumulus's personal-machine daily change rates | SUPPORTED |
| D-F3-16 | how Déjà Dup's monitor starts the scheduled backup | SUPPORTED |
| D-F3-18 | Déjà Dup's defaults | SUPPORTED |
| D-F3-19 | Déjà Dup in Ubuntu 24.04's extended install | SUPPORTED |
| D-F3-21 | the CPU groups (slices) of the indexer and the backup | SUPPORTED |
| D-F3-22 | how apt's units start the daily upgrade | SUPPORTED |
| D-F3-23 | unattended-upgrades default-installed and enabled | SUPPORTED |
| D-F3-24 | the glibc update of 2026-07-27 | SUPPORTED |
| D-F3-28 | DKMS's kernel hooks and the build's `nproc` | SUPPORTED |
| D-F3-29 | NVIDIA's 595 open module: version, branch, five modules | WORDING-FIX |
| D-F3-30 | kernels: 7.0.0-34 to security 2026-09-23; installer's HWE 7.0.0-31 | SUPPORTED |
| D-F3-32 | Tracker 3.7.1 in the default install | SUPPORTED |
| D-F3-34 | Tracker's threads: SCHED_IDLE at nice 19 | SUPPORTED |
| D-F5-22 | SchedCP's kernel-compilation workload and gain | SUPPORTED |
| D-F5-23 | where SchedCP's "short-lived processes" comes from | SUPPORTED |
| D-F5-24 | that SchedCP cites schbench, and how | SUPPORTED |

---

## Per claim

### D-F2-19 — the CMU keystroke dataset
- location: docs/references.md:64
- repo: "public raw per-keystroke latency dataset (cs.cmu.edu/~keystroke) for direct empirical fits if needed. Caveat: single practiced password, lab setting."
- passage (source 16): dataset page "The data are arranged as a table with 34 columns … The remaining 31 columns present the timing information for the password" (H, DD, UD columns); "The raw records of all the subjects' keystrokes and timestamps were analyzed to create a password-timing table"; paper §4.4 "For each password, 31 timing features were extracted".
- verdict: WORDING-FIX — the object is a per-repetition table of 31 derived timing features, not raw per-keystroke data (the page says the raw records were processed into this table). Single password and lab setting hold.
- fix: "public table of 31 keystroke timing features (hold, keydown-keydown, keyup-keydown) per repetition, 51 typists × 400 repetitions of one password (cs.cmu.edu/~keystroke)".

### D-F2-20 — BEHACOM
- location: docs/workload/grounding-sources.md:44
- repo: "Per-minute application-usage vectors of 12 users on their own computers (eight on Windows, three on Linux, one on both), 2019–2020: the foreground executable name and the switches between applications per minute"
- passage (source 17): "twelve users interacting with their computers for fifty-five consecutive days"; "Eight of them use Windows as operating system, three Linux, and one both"; first and last timestamps 20-Nov-19 and 14-Jan-20; Table 5 foreground executable name and "Number of changes between different foreground applications during the time window" (one-minute windows).
- verdict: SUPPORTED. (references.md:73–74's Mendeley byte count, SHA-256 and licence were not part of this read.)
- fix: none.

### D-F2-21 — DesktopBench sessions
- location: docs/workload/grounding-sources.md:45; docs/references.md:79
- repo: "Multitask and interruption sessions with app names and window titles, composed from templates over VideoGUI's single-task actions, not observed"; references.md:79 "320 multitask + 100 interruption sessions", the quoted A → B → A sentence and §4.1 composition.
- passage (source 18): §4.1 "We therefore augment each action with the foreground application name (app) and window title (title)"; "Sessions are assembled through template-based composition"; "a long-running creative task 𝐴 is interrupted by a short YouTube browsing task 𝐵 before resuming"; "320 in DesktopBench-Multitask and 100 in DesktopBench-Interruption".
- verdict: SUPPORTED.
- fix: none.

### D-F2-22 — DesktopBench release
- location: docs/references.md:78–79; docs/workload/building-plan.md:204; docs/workload/grounding-sources.md:45
- repo: "the release's only timestamps are synthetic, a fixed 6.0 s per action, dropped before use … released on HuggingFace `HaoranYin/desktopbench` v0.1.0; data terms restrictive — research inspection only, no redistribution; scripts MIT"; ":78 (v2, 2026-07-18). Preprint — no venue."
- passage (source 18): `prepare_videogui_raw_from_hf.py` `duration = 6.0`, timestamps advanced by it; `rebuild_desktopbench.py` `DROP_FIELDS = {"timestamp", "duration", …}`; README "public `v0.1.0` release"; DATA_TERMS "available for research inspection … no redistribution, sublicensing, or republication license is granted"; "Scripts are MIT licensed"; arXiv v2 2026-07-18; "Preprint. Under review."
- verdict: SUPPORTED.
- fix: none.

### D-F2-23 — interbench pin, version, licence
- location: docs/references.md:170
- repo: "master commit e612a65 (2016-10-24), version string 0.31; its load defaults differ from tag v0.31. Licence GPL-2.0-or-later per the source headers; COPYING is GPLv2 and a GPLv3 LICENSE file also ships, which GitHub reports."
- passage (source 19): `#define INTERBENCH_VERSION "0.31"`; header "version 2 of the License, or (at your option) any later version"; COPYING GPL v2, LICENSE GPL v3; tag v0.31 `.cpu_load = 4` against master's `sysconf(_SC_NPROCESSORS_ONLN)`; GitHub API licence GPL-3.0 (checked in phase 2).
- verdict: SUPPORTED.
- fix: none.

### D-F2-25 — interbench's interactive constants
- location: docs/references.md:171; docs/workload/source-vetting.md:142, :162
- repo: "Audio (50 ms @ 5%), Video (16.7 ms @ 40%) and X (0–100% variable)"; ":162 the Video task 'tries to receive cpu 60 times per second'"
- passage (source 19): `AUDIO_INTERVAL (50000)`, `AUDIO_RUN (AUDIO_INTERVAL / 20)`; `VIDEO_INTERVAL (1000000 / 60)`, `VIDEO_RUN (VIDEO_INTERVAL * 40 / 100)`; X "a variable percentage of cpu from 0-100%"; man page "tries to receive cpu 60 times per second and uses 40% cpu".
- verdict: SUPPORTED.
- fix: none.

### D-F2-26 — interbench's missed-period handling
- location: docs/references.md:171
- repo: "how those emulations treat a missed period — counted as missed deadlines, the deadline moved past the current time by whole periods, the burn bypassed (`interbench.c:398–436` at `e612a65`)"
- passage (source 19): `periodic_schedule`: "We missed the deadline even before we consumed cpu" … `tb->missed_deadlines += intervals; … deadline += intervals * interval_usecs; … goto bypass_burn;`; after a late burn the missed intervals are counted and the deadline advanced likewise.
- verdict: SUPPORTED (the burn is bypassed for a period already missed before its burn, which is what "a missed period" names; a period that overruns during its burn has already burned).
- fix: none.

### D-F2-27 — interbench's Burn default and 7 ms jitter figure
- location: docs/workload/source-vetting.md:162
- repo: "Burn defaults to the online CPU count, 4 being the man page's … Its '~7 ms' jitter figure is the program's own, stated without a source in its man page, readmes and code — not a human-perception threshold"
- passage (source 19): `ud.cpu_load = sysconf(_SC_NPROCESSORS_ONLN);`; man page "Burn: … (4 by default)"; man page "Average humans' limit of perception for jitter is in the order of 7ms. Trained audio observers might notice much less."
- verdict: WORDING-FIX — Burn part holds. The man page does present 7 ms as a human-perception limit; "not a human-perception threshold" reads as contradicting the source's own statement, where the intended point is that the statement is unsourced.
- fix: "Its '~7 ms' is the man page's unsourced statement that human perception of jitter is about 7 ms — not an established perception threshold".

### D-F2-28 — interbench packaging; LWN precedents
- location: docs/workload/source-vetting.md:181, :141
- repo: ":181 interbench's packaging is Gentoo, FreeBSD ports, AUR, GNU Guix, openSUSE Leap, Void, AOSC and LiGurOS — no Debian package was found"; ":141 The precedent holds for hackbench and rt-app (LWN 725238) and as an LWN mention for stress-ng (LWN 1051430); none was found for interbench."
- passage (source 19): Repology entries aosc, aur, freebsd, gentoo, gnuguix, liguros_stable/develop, opensuse_leap_15_5/15_6, void_x86_64; LWN 725238's hackbench and rt-app sections; LWN 1051430 "(e.g. stress-ng and hackbench)"; neither article mentions interbench.
- verdict: SUPPORTED.
- fix: none.

### D-F2-32 — rt-app's users and documentation
- location: docs/workload/grounding-sources.md:26; docs/workload/source-vetting.md:87, :55
- repo: "rt-app (scheduler-tools; used by ARM and Linaro, per LWN)"; ":87 rt-app: referenced in kernel deadline docs"; ":55 doc/examples/template.json: wake every 100 ms, run 10 ms, SCHED_OTHER, 6 s"
- passage (source 20): LWN 725238 "Today, ARM and Linaro are using rt-app to trigger specific scheduler code paths"; README "rt-app is a test application that starts multiple periodic threads in order to simulate a real-time periodic load"; checked in phase 2: v6.6 `Documentation/scheduler/sched-deadline.rst:724` "The first testing application is called rt-app"; `doc/examples/template.json` `"run" : 10000`, timer period 100000, `"duration" : 6`, `"default_policy" : "SCHED_OTHER"`.
- verdict: SUPPORTED.
- fix: none.

### D-F2-33 — schbench pin, copyright, licence
- location: docs/references.md:180; docs/workload/source-vetting.md:164
- repo: "tag `v1.0` (commit `ab22f3f8`, 2023-04-17), its only tag; github.com/masoncl/schbench continues the same history without tags. 'Copyright (C) 2016 Facebook', GPLv2 (`schbench.c:1–7`)"
- passage (source 21): `git tag` lists only `v1.0` → `ab22f3f8…` (2023-04-17); `schbench.c` "Copyright (C) 2016 Facebook … GPLv2, portions copied from the kernel and from Jens Axboe's fio".
- verdict: SUPPORTED (the GitHub mirror clause was not part of this read).
- fix: none.

### D-F2-34 — schbench's percentiles and request
- location: docs/references.md:181; docs/workload/grounding-sources.md:28; docs/workload/source-vetting.md:164
- repo: "at v1.0 it prints wakeup and request latency at p50/p90/p99/p99.9, p99 marked in its output, and requests per second at p20/p50/p90 … its 2016 first version printed p50/75/90/95/99/99.5/99.9"; ":164 v1.0 does one `usleep(100)` per request"
- passage (source 21): `plist = { 20.0, 50.0, 90.0, 99.0, 99.9 }`, `PLIST_FOR_LAT (PLIST_50 | PLIST_90 | PLIST_99 | PLIST_999)`, `PLIST_FOR_RPS (PLIST_20 | PLIST_50 | PLIST_90)`, the star on `PLIST_99`; `worker_thread` `usleep(100);` then `do_work`; phase 2: first commit `36d859a` (2016-04-04) `plist = { 50.0, 75.0, 90.0, 95.0, 99.0, 99.5, 99.9 }`. (The README's "two usleeps" is what the source-vetting body line 58 kept; the correction at :164 states the code.)
- verdict: SUPPORTED.
- fix: none.

### D-F2-35 — SchedCP cites schbench
- location: docs/references.md:181; docs/workload/grounding-sources.md:28; docs/workload/source-vetting.md:141, :181
- repo: "Cited in SchedCP's references by kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench"
- passage (sources 21, 27): "[12] Chris Mason. schbench: Scheduler benchmark. https://kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench, 2016."
- verdict: SUPPORTED.
- fix: none.

### D-F2-36 — hackbench
- location: docs/references.md:185–186; docs/workload/grounding-sources.md:29
- repo: "tag `v2.11` (commit `62da2bef`) … 'Hackbench is both a benchmark and a stress test …' … `datasize = 100`, `loops = 100`, `num_groups = 10`, `num_fds = 20` … 10 × 20 × 2 = 400. Reports a single completion time"
- passage (source 22): tag v2.11 → commit `62da2bef…`; man page DESCRIPTION (same words); `hackbench.c:37–40` the four defaults; example banner "(== 400 tasks)"; `printf("Time: …")`.
- verdict: SUPPORTED.
- fix: none.

### D-F2-37 — LWN on hackbench
- location: docs/workload/grounding-sources.md:29; docs/workload/source-vetting.md:87
- repo: "LWN notes it is most often used for load-balancing changes"; ":87 'a stalwart of kernel scheduler testing' (LWN survey, Articles/725238)"
- passage (source 22): "This benchmark is a stalwart of kernel scheduler testing"; "it is most often used by developers who are making changes to the scheduler's load-balancing code".
- verdict: SUPPORTED.
- fix: none.

### D-F2-38 — stress-ng
- location: docs/references.md:190–191; docs/workload/grounding-sources.md:31; docs/workload/source-vetting.md:167
- repo: "commit `3ac9d7a8` (2026-09-23; newest tag V0.22.01), GPL-2.0-or-later … `--workload` stressor 'emulates bursty scheduled compute' — work items of 1 ms quanta at random times in a 100 ms slice, 30 % load by default … `--cyclic` stressor reports wake-latency percentiles p25 to p99.99 … 'it has never been intended to be used as a precise benchmark test suite, so do NOT use it in this manner'"
- passage (source 23): `git describe` V0.22.01-24-g3ac9d7a8; COPYING GPL v2, headers "or (at your option) any later version"; man page `--workload` "a 100000 microsecond slice … 100 work items … a quanta of 1000 microseconds … (default of 30%) … This emulates bursty scheduled compute"; `--cyclic` latency percentiles; phase 2: `stress-cyclic.c` percentiles 25.0 … 99.99; README disclaimer verbatim.
- verdict: SUPPORTED.
- fix: none.

### D-F2-39 — Ananicy and ananicy-cpp
- location: docs/references.md:201–203; docs/workload/source-vetting.md:158
- repo: ":201 Ananicy (GPL), archived; its last commit `1e2cc9a6`, 2023-03-21 … ananicy-cpp (GPL-3.0), version 1.2.0"; ":202 Self-description: 'a shell daemon created to manage processes' IO and CPU priorities, with community-driven set of rules for popular applications … mainly for desktop usage'. Matching is by executable name, optionally narrowed by command line: `name` is the only required field ('used for match processes by exec bin name'), with `cmdlines`, `type`, `nice`, … `cgroup` optional (field list from the ananicy-cpp README)."
- passage (source 24): GitHub `"archived":true`, `"license":"GPL-3.0"`; phase 2: `1e2cc9a` committer date 2023-03-21; ananicy-cpp LICENSE GPL v3 and README "Ananicy rewritten in C++ for much lower CPU and memory usage"; ananicy-cpp v1.2.0 README field list: nice, latency_nice, sched, rtprio, ioclass, ionice, oom_score_adj, cpuset, cgroup, type — no `cmdlines`; the "shell daemon" sentence (README:22), "`name` used for match processes by exec bin name" (README:73) and the `cmdlines` rule example (README:15) are in upstream Ananicy's README; phase 2: no `cmdlines` handling in ananicy-cpp v1.2.0's `src/`, and none in its README at `3554447c`.
- verdict: WORDING-FIX — status and licences hold; the self-description, the required-field quote and `cmdlines` are upstream Ananicy's, while the line places them in a field list "from the ananicy-cpp README" right after ananicy-cpp's matching rule. ananicy-cpp matches by `argv[0]` basename only.
- fix: "Ananicy's self-description: '…'. Ananicy matches by executable name, optionally narrowed by `cmdlines` (Ananicy README); ananicy-cpp's README lists `type`, `nice`, `latency_nice`, `sched`, `rtprio`, `ioclass`, `ionice`, `oom_score_adj`, `cpuset`, `cgroup`, and has no `cmdlines`".

### D-F2-40 — ananicy-cpp's lookup key
- location: docs/references.md:202
- repo: "ananicy-cpp looks a rule up by the basename of the process's first `/proc/<pid>/cmdline` argument (`argv[0]`), untruncated — failing that the `/proc/<pid>/exe` link's basename, then `/proc/<pid>/comm`"
- passage (source 24): `get_command_from_pid`: "Cmdline method" `cmdline[0].substr(exe_name_begin + 1)`, then "Exe method", then "Comm method"; `Rules::get_rule` `m_program_rules.contains(name)`.
- verdict: SUPPORTED (the per-thread nice clause was not part of this read).
- fix: none.

### D-F2-41 — CachyOS enables ananicy-cpp with the catalogue
- location: docs/references.md:207–208
- repo: "the package depends on `ananicy-cpp` and `cachyos-ananicy-rules` (`PKGBUILD:23–26`), and its install hook runs `systemctl enable` on `ananicy-cpp` (`cachyos-settings.install:1`, `:23–27`). The catalogue it installs is `ananicy-rules`"
- passage (source 24): PKGBUILD `pkgver=1.4.1`, `depends=(` at line 23 with `ananicy-cpp` (25) and `cachyos-ananicy-rules` (26); `.install` line 1 `SERVICES=("ananicy-cpp" …)`, `post_install` `systemctl enable "$service"` (lines 23–27); `cachyos-ananicy-rules` built from github.com/CachyOS/ananicy-rules tag 1.1.49.
- verdict: SUPPORTED (the installer and live-image paths were not part of this read).
- fix: none.

### D-F2-42 — the catalogue's counts, types, values, maintainers
- location: docs/references.md:212–215; docs/workload/source-vetting.md:158
- repo: "361 `.rules` files; 15 813 rule entries; 13 528 … `Game` … fifteen types; thirteen are used … one entry is not valid JSON (a stray `+` at end of line, `…linux-native_d.rules:315`)"; type values as listed; "maintained 'by the CachyOS team and the community'"; ":158 15,811 distinct names"
- passage (source 24): 361 files, 15 814 lines under a lenient parse that tolerates the stray `+` (phase 2: `linux-native_d.rules:315` is `{ "name": "Dungeon Drafters.x86_64", "type": "Game" }+`), so 15 813 strict entries, Game 13 528 strict, 15 811 distinct strict names; 15 types defined, 13 used; type values as in `00-types.types`; README "maintained by the CachyOS team and the community".
- verdict: SUPPORTED.
- fix: none.

### D-F2-43 — audio servers, indexers, compilers; no wanted/unwanted split
- location: docs/workload/source-vetting.md:158; docs/workload/grounding-sources.md:18
- repo: "`Player-Audio` is nice −4, nice −11 having existed only in 2022–2025 commits, on audio-server rules; only KDE's Baloo and Recoll are typed `BG_CPUIO` …, GNOME's Tracker and `updatedb` having no entry; 'compilers batch/idle' is ananicy-cpp's README example `gcc` rule, the catalogue holding no compiler entries … No type, comment or README text draws a wanted/unwanted-background distinction"
- passage (source 24): `audioserver.rules` pipewire, pipewire-pulse, wireplumber, pulseaudio all `LowLatency_RT` (nice −12); `Player-Audio` nice −4 (players); Baloo and `recollindex` BG_CPUIO; no Tracker, updatedb or compiler rule; ananicy-cpp README `gcc` example `"sched": "batch", "ioclass": "idle"`; type comments draw no such distinction. Phase 2: `git log -S'"nice": -11'` shows −11 added by `6474a905` "Adjust audioserver.rules" (2022-10-01) and removed by `2223eefd` (2025-02-03).
- verdict: WORDING-FIX — every clause holds, but the line never says what the audio servers are set to at the pin (LowLatency_RT, nice −12); placed after "`Player-Audio` is nice −4", it reads as if audio servers carry −4.
- fix: "audio servers (pipewire, pipewire-pulse, wireplumber, pulseaudio) are `LowLatency_RT`, nice −12 (their nice −11 existed 2022–2025); `Player-Audio`, nice −4, is for players".

### D-F2-44 — how much of the core set the shipped catalogue matches
- location: dataset/README.md:114; docs/workload/building-plan.md:121
- repo: README "matches none of its rules to several names the files bind — `kdenlive`, `make`, `python`, `HandBrakeCLI`, `deja-dup` among them (9.12 D109)"; building-plan "which on ananicy-cpp's key keys every bound name of a file in only 7 of the 50 core files it was counted on (9.12 D109)"
- passage (source 24): lookup key = `argv[0]` basename, exact match; 15 812 distinct names (lenient parse). Phase 2 computation on `dataset/build/coreset-single` (the unsuffixed `*.workload.json`, names from `arrive` events and their `spawn_table`): 51 core files, 44 distinct bound names; on the dataset's own names 14 match and 7 files match whole (`c1-browsing`, `c1-dev`, `c1-media`, `c1-meeting`, `c1-photo`, `c6-fold`, `c6-spoof`). No rule exists for `kdenlive`, `make`, `python`, `python3`, `HandBrakeCLI`, `deja-dup` or `duplicity`. `c2-p2a-idle` (added 2026-10-09 in `ea5c6ab1`) binds exactly `c2-p2a`'s names, and `c2-p2a` is in 9.12 A3-09's "strict 7" list; `c6-alias` was added 2026-10-12.
- verdict: WORDING-FIX — the README clause holds on the final build under any reasonable `argv[0]` reading of those five names. The building-plan count is from the 2026-10-09 build (50 files, 35 names); the final build has 51 files and 44 names, and the file that binds `c2-p2a`'s names puts the count on 9.12's own mapping at no fewer than 8. A full recount needs 9.12's per-name `argv[0]` table, which no source read here provides.
- fix: recount on the final build with 9.12's `argv[0]` table and state it ("in N of the 51 core files"), or date the figure ("7 of 50 on the 2026-10-09 build").

### D-F2-45 — DARPA OpTC
- location: docs/workload/grounding-sources.md:60
- repo: "Process-create events with image paths, from Windows 10 enterprise endpoints, not personal desktops"
- passage (source 25): "Each Windows 10 endpoint is equipped with an endpoint sensor"; enterprise exercise (USTRANSCOM JDDE context, 500 of 1 000 hosts); eCAR example `"object": "PROCESS", "action": "CREATE"` with `image_path`; "an 'image_path' entry in Event.properties will also typically be present".
- verdict: SUPPORTED.
- fix: none.

### D-F2-46 — Carat
- location: docs/workload/grounding-sources.md:69
- repo: "Carat, whose samples list several running apps (`carat-top1000`), is noted and not used"
- passage (source 25): "apps (app usage data, see below) Where app usage is a list of JSON objects with the following attributes: processName … priority (background, foreground, etc …)".
- verdict: SUPPORTED.
- fix: none.

### D-F3-01 — O'Callahan et al.'s build workload
- location: dataset/sources.yaml:85–87; dataset/archetypes.yaml:1035–1036; docs/references.md:84; docs/workload/grounding-sources.md:32; docs/workload/building-plan.md:101; docs/workload/source-vetting.md:168
- repo: "\"make forks and execs 2430 processes, mostly short-lived\" (sec-4.3 …). The workload is a `make -j8` build of DynamoRio 6.1.0 (sec-4.1), not a Linux kernel build."
- passage (source 26): §4.1 "make builds DynamoRio [8] (version 6.1.0) with make -j8"; §4.3 "make forks and execs 2430 processes, mostly short-lived".
- verdict: SUPPORTED.
- fix: none.

### D-F3-02 — what O'Callahan's count grounds
- location: dataset/sources.yaml:87–88; docs/references.md:84; docs/workload/building-plan.md:101; dataset/archetypes.yaml:1034
- repo: "Grounds only the existence and short-lived character of compiler children"; archetypes "The literature grounds the class's existence and short-lived character only" (the class `compiler-child`)
- passage (source 26): "make forks and execs 2430 processes, mostly short-lived" — no statement of what the processes run (references.md:84 itself: "The paper does not say what the 2430 processes run").
- verdict: WORDING-FIX — the object narrows from all processes a parallel make forks to compiler children, which the paper does not name.
- fix: "grounds only that a parallel `make` build (DynamoRio, `-j8`) forks and execs many processes, mostly short-lived; the paper does not say what they run".

### D-F3-03 — Coetzee et al. on the Linux kernel build
- location: dataset/sources.yaml:95–97; dataset/archetypes.yaml:1036–1037; docs/references.md:89
- repo: "\"the Linux kernel build's enormous number of short-lived processes\" (sec-9). The characterization is specific to the Linux kernel build"; archetypes "its examples `cp` and `mkdir`, with no count (sec-9)"
- passage (source 26): "the Linux kernel build's enormous number of short-lived processes like cp and mkdir" (section 9, "Preliminary experimental results"); no count.
- verdict: SUPPORTED.
- fix: none.

### D-F3-04 — the reach of Coetzee's corroboration
- location: docs/references.md:89
- repo: "so beside `ocallahan-atc17` it corroborates only that builds spawn many short-lived processes"
- passage (source 26): the passage names "the Linux kernel build's" processes; the same entry says to cite it for the kernel build only.
- verdict: WORDING-FIX — "builds" widens the scope from the Linux kernel build.
- fix: "corroborates only that the Linux kernel build spawns many short-lived processes".

### D-F3-05 — SchedCP's kernel-compilation workload
- location: docs/workload/grounding-sources.md:32
- repo: "(kernel compilation, \"make -j 172\" on 6.14 tinyconfig, 1.79× over EEVDF) … SchedCP's \"short-lived processes\" is its Observation Agent's generated profile text"
- passage (source 27): "For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), … reaching 1.79× total improvement over EEVDF"; §4 "For kernel compilation, it [the Observation Agent] produces profiles like "CPU-intensive parallel compilation with short-lived processes, …"".
- verdict: SUPPORTED.
- fix: none.

### D-F3-06 — sambatest, kernel docs, autogroup
- location: docs/workload/source-vetting.md:168
- repo: "89 is the next most prolific workload's (sambatest). `sched_child_runs_first` is in no kernel Documentation file; SCHED_AUTOGROUP's Kconfig help says \"build jobs\", not \"make -j\"."
- passage (source 26): "(The next most prolific workload is sambatest with 89.)"; no `child_runs_first` under v6.6 `Documentation/`; Kconfig "isolates aggressive CPU burners (like build jobs) from desktop applications".
- verdict: SUPPORTED.
- fix: none.

### D-F3-07 — the build tools' documented default parallelism
- location: docs/workload/measurement-overview.md:52
- repo: "The kernel build and the DKMS rebuild run `-j8`: the build tools' documented defaults follow `nproc`, here for an eight-thread desktop."
- passage (source 28): make.texi "The default number of job slots is one, which means serial execution (one thing at a time)"; dkms "# Default to -j<number of CPUs>" `parallel_jobs=${parallel_jobs:-$(get_num_cpus)}` (nproc); NVIDIA's `dkms.conf` `PROCS_NUM=\`nproc\`` capped at 16 (source 32).
- verdict: CONTRADICTED — for the kernel build the tool is GNU make, whose documented default is one job, not `nproc`; only the DKMS side follows `nproc`.
- fix: "run `-j8`, the `nproc` rule applied to an eight-thread desktop (DKMS and NVIDIA's `dkms.conf` read `nproc`; GNU make defaults to one job)".

### D-F3-09 — make's jobserver counts jobs
- location: dataset/archetypes.yaml:1075
- repo: "`parallelism_cap` counts jobs, as make's jobserver counts them"
- passage (source 28): "GNU make uses a method called the "jobserver" to control the number of active jobs across recursive invocations"; "every command make starts has one implicit job slot reserved for it".
- verdict: SUPPORTED.
- fix: none.

### D-F3-13 — Meyer and Bolosky's 30 MB
- location: docs/workload/measurement-overview.md:188; dataset/archetypes.yaml:1357; docs/references.md:159
- repo: "half of the bytes in files over 30 MB, Windows, 2009"; archetypes "against the 2009 Windows population's half"
- passage (source 29): "half of all bytes are in files larger than 30MB (this figure was 2MB in 2000)"; "857 desktop computers at Microsoft over a span of 4 weeks"; scans September–October 2009.
- verdict: SUPPORTED.
- fix: none.

### D-F3-14 — GNU/Linux median file size
- location: docs/workload/measurement-overview.md:188; dataset/archetypes.yaml:1357; docs/references.md:537
- repo: "the GNU/Linux users' 4.60 KB (4,707 B)"; references.md:537 the column, the 42 participants and the lognormal 10.83 KB note
- passage (source 29): `2-normal-stats.csv` `linux,4.596679688,…` (Median file size (in KB)); `1-sample-breakdown.csv` `linux,4464785,42`; `3-lognormal-stats.csv` `linux,10.82777225,…`; header "please refer to lognormal stats since data are highly skewed".
- verdict: SUPPORTED.
- fix: none.

### D-F3-15 — Cumulus's personal-machine change rates
- location: docs/workload/measurement-overview.md:52, :189; dataset/archetypes.yaml:1682–1683; docs/references.md:164
- repo: "the incremental after seven days of Cumulus's personal-machine change rates"; references.md:164 "223 days, 2.37 GB, 'New data/day 10.3 MB', 'Changed data/day 29.9 MB' … one personal machine … daily rates, no weekly union"
- passage (source 29): user trace "taken from the Cumulus backups of the home directory of one of the author's personal computers"; Table 2 user column 223 days, "New data/day 10.3 MB", "Changed data/day 29.9 MB".
- verdict: SUPPORTED (seven days is the repository's application of the per-day rates, labelled as such; the table names no mean or median, and the repository names none).
- fix: none.

### D-F3-16 — how Déjà Dup's monitor starts the backup
- location: dataset/archetypes.yaml:1680–1681, :1708; docs/workload/coreset-guide.md:220; docs/references.md:471
- repo: "started by its own monitor through `chrt --idle 0 ionice -c3`"; references.md:471 "When a backup is due, the monitor, 120 s after its start, runs `chrt --idle 0 ionice -c3 deja-dup --backup --auto`"
- passage (source 30): `begin_monitoring` `var delay_time = 120;`; `start_auto` `DejaDup.run_deja_dup({"--backup", "--auto"})`; `nice_prefix` builds `chrt --idle 0 ionice -c3 deja-dup`. (The autostart entry adds its own `X-GNOME-Autostart-Delay=120` before the monitor starts.)
- verdict: SUPPORTED.
- fix: none.

### D-F3-18 — Déjà Dup's defaults
- location: dataset/archetypes.yaml:1679–1680; docs/workload/building-plan.md:85; docs/workload/scenario-catalog.md:26; docs/references.md:471
- repo: "at Déjà Dup's defaults with its password remembered (D117) — encrypted by gpg, 200 MB volumes — making its scheduled weekly incremental"; catalog "a periodic backup every 7 days once turned on"; references.md:471 "weekly once turned on, encryption on with the password not remembered"
- passage (source 30): `periodic` default false, `periodic-period` default 7; `encrypt_enabled.active = true; // always default to encrypted`; "Remember password" switch not set (off); `get_volsize` `return 200;`.
- verdict: SUPPORTED (the remembered password is stated as the measurement's departure, D117).
- fix: none.

### D-F3-19 — Déjà Dup in the extended install
- location: docs/workload/scenario-catalog.md:26
- repo: "Déjà Dup in Ubuntu 24.04's extended install"
- passage (source 30): `install-sources.yaml` `ubuntu-desktop` (default: false, "A full featured Ubuntu Desktop", `minimal.standard.squashfs`); `minimal.standard.manifest` `+deja-dup 45.2-1build2`; absent from `minimal.manifest`.
- verdict: SUPPORTED.
- fix: none.

### D-F3-21 — the slices of the indexer and the backup
- location: dataset/archetypes.yaml:1592–1594, :1710–1712
- repo: "the miner's unit runs in `background.slice`, a separate CPU group from the editor's `app.slice`, where the slice weights give it about 23 % of the CPU"; "the monitor's autostart scope under `app.slice` … an idle weight of 3 against 1 024"
- passage (source 30): `tracker-miner-fs.service.in` `Slice=background.slice`; `background.slice` `CPUWeight=30`, `app.slice` `CPUWeight=100` (30 / 130 ≈ 23 %); gnome-session `gnome_start_systemd_scope` → gnome-desktop `app-gnome-%s-%d.scope` with no Slice → systemd user default `app.slice`; phase 2: v6.6 `kernel/sched/sched.h:2179` `#define WEIGHT_IDLEPRIO 3`.
- verdict: SUPPORTED (that the editor itself sits in `app.slice` was not part of this read).
- fix: none.

### D-F3-22 — apt's daily upgrade units
- location: dataset/archetypes.yaml:1495–1496; docs/references.md:481
- repo: "`apt.systemd.daily install` (apt-daily-upgrade.service's ExecStart)"; references.md:481 "the timer fires daily at 06:00 with up to 60 min random delay, `Persistent=true` (`apt-daily-upgrade.timer:6–8`); the service runs `/usr/lib/apt/apt.systemd.daily install` after `apt-helper wait-online` (`apt-daily-upgrade.service:9–10`)"
- passage (source 31): `OnCalendar=*-*-* 6:00`, `RandomizedDelaySec=60m`, `Persistent=true` (lines 6–8); `ExecStartPre=-/usr/lib/apt/apt-helper wait-online`, `ExecStart=/usr/lib/apt/apt.systemd.daily install` (lines 9–10).
- verdict: SUPPORTED.
- fix: none.

### D-F3-23 — unattended-upgrades default and enabled
- location: docs/workload/scenario-catalog.md:28; dataset/README.md:120; dataset/timelines/coreset/c7.variant.yaml:10–11; docs/references.md:486
- repo: "The stock unattended upgrade, in Ubuntu 24.04's default install and enabled by default"
- passage (source 31): `minimal.manifest` `+unattended-upgrades 2.9.1+nmu4ubuntu1`; template `Default: true`; postinst writes `20auto-upgrades` (`Unattended-Upgrade "1"`); Allowed-Origins release, security, ESM security.
- verdict: SUPPORTED.
- fix: none.

### D-F3-24 — the glibc update of 2026-07-27
- location: dataset/archetypes.yaml:1496–1498; docs/workload/measurement-overview.md:52; docs/workload/coreset-guide.md:217
- repo: "installing the security update Ubuntu published on 2026-07-27 — glibc 2.39-0ubuntu8.7 to 2.39-0ubuntu8.8, four binaries: `libc-bin`, `libc6`, `libc6-dbg`, `locales`" (on a chroot built from the archive as it stood at 2026-07-27T00:00Z)
- passage (source 31): 2.39-0ubuntu8.8 Security 2026-07-27T12:28 UTC, Updates 14:17 UTC, preceded by 8.7 (2026-02-03); amd64 non-debug binaries of the publication include `libc-bin`, `libc6`, `libc6-dbg`, `locales` among 15; `minimal.manifest` (24.04.5.1) carries `libc6-dbg`.
- verdict: SUPPORTED (four is the count of the update's binaries present in the default layer, which the sentence's subject — the install on that layer — scopes).
- fix: none.

### D-F3-28 — DKMS's kernel hooks and `nproc`
- location: dataset/archetypes.yaml:1132–1135; docs/workload/scenario-catalog.md:22; docs/references.md:496
- repo: "every process under the two DKMS kernel hooks … `nproc` being what NVIDIA's `dkms.conf` and dkms read"; references.md:496 "a kernel's and its headers' postinst run `dkms_autoinstaller start` (`postinst.d/dkms:37–38`, `header_postinst.d/dkms:37–38`), which runs `dkms autoinstall --kernelver` … `dkms`'s own parallelism is `nproc` (`dkms:180–187`)"
- passage (sources 28, 32): both hooks `exec /usr/lib/dkms/dkms_autoinstaller start "$inst_kern"`; autoinstaller `dkms autoinstall --kernelver $kernel`; `get_num_cpus` returns `nproc` (dkms lines 180–188); NVIDIA `PROCS_NUM=\`nproc\``.
- verdict: SUPPORTED.
- fix: none.

### D-F3-29 — NVIDIA's 595 open module
- location: dataset/archetypes.yaml:1126–1127; docs/references.md:501; docs/workload/building-plan.md:162
- repo: "DKMS's autoinstall of `nvidia-dkms-595-open` 595.91.07, the open kernel module of NVIDIA's production branch (D47)"; references.md:501 "builds five modules — `nvidia`, `nvidia-modeset`, `nvidia-drm`, `nvidia-uvm`, `nvidia-peermem` — from one `make -j$PROCS_NUM`, `PROCS_NUM` being `nproc` capped at 16"
- passage (source 32): `.dsc` Binary includes `nvidia-dkms-595-open`, Version 595.91.07-0ubuntu0.24.04.1; `dkms_nvidia_open.conf` modules 0–2 plus `dkms.conf.fragment` modules 3–4 (nvidia-uvm, nvidia-peermem) appended on amd64; `PROCS_NUM` capped at 16. Phase 2: `debian/control` (sha256 `72ed38d8…`) stanzas carry `XB-Support: PB`; no file read spells out "PB"; the changelog calls 595.71.05 "UDA".
- verdict: WORDING-FIX — version and the five modules hold; "production branch" expands Ubuntu's `XB-Support: PB` with no source in the copies read that defines the abbreviation.
- fix: "the open kernel module of NVIDIA's 595 branch (Ubuntu's control file: `XB-Support: PB`)", or add and cite the Ubuntu/NVIDIA page that defines PB as production branch.

### D-F3-30 — the kernels
- location: dataset/archetypes.yaml:1127–1130; docs/workload/building-plan.md:162; docs/workload/coreset-guide.md:238
- repo: "for the security kernel `7.0.0-34-generic`, run by the stock Ubuntu 24.04 unattended upgrade's install stage of 2026-09-23 … with the HWE kernel the installer adds (`7.0.0-31`)"
- passage (source 32): `linux-hwe-7.0 7.0.0-34.34~24.04.1 Security … 2026-09-23T15:49:46`, preceded by 7.0.0-31 (Security 2026-09-04); 24.04.5.1 live layer and pool carry `linux-generic-hwe-24.04 7.0.0-31.31~24.04.1` and `linux-image-7.0.0-31-generic`.
- verdict: SUPPORTED (the ISO carries HWE 7.0.0-31 as its only HWE kernel; the installer's own package selection was not part of this read).
- fix: none.

### D-F3-32 — Tracker in the default install
- location: docs/workload/scenario-catalog.md:25
- repo: "Tracker 3.7.1 in Ubuntu 24.04's default install (`ubuntu-desktop-manifest`)"
- passage (source 30): `minimal.manifest` `+tracker 3.7.1-1build1`, `+tracker-extract 3.7.1-1ubuntu0.1`, `+tracker-miner-fs 3.7.1-1ubuntu0.1`; `install-sources.yaml` minimal is `default: true`.
- verdict: SUPPORTED.
- fix: none.

### D-F3-34 — Tracker's SCHED_IDLE at nice 19
- location: dataset/archetypes.yaml:1588–1589
- repo: "Every thread of the miner and the extractor declares itself background work, SCHED_IDLE at nice 19 (9.6 D17)"
- passage (source 30): `initialize_priority_and_scheduling`: `tracker_sched_idle ()` (`pthread_setschedparam (pthread_self(), SCHED_IDLE, &sp)`, "Threads spawned from a SCHED_IDLE thread will inherit the same priority"), then `nice (19)`; the extractor's `tracker-main.c` carries the same `nice()` block.
- verdict: SUPPORTED.
- fix: none.

### D-F5-22 — SchedCP's workload and gain
- location: docs/workload/grounding-sources.md:32
- repo: "A compile workload SchedCP's evaluation uses (kernel compilation, \"make -j 172\" on 6.14 tinyconfig, 1.79× over EEVDF)"
- passage (source 27): as D-F3-05; Figure 2a 13.57 s → 7.60 s, "1.79×".
- verdict: SUPPORTED.
- fix: none.

### D-F5-23 — where "short-lived processes" comes from
- location: docs/workload/grounding-sources.md:32
- repo: "SchedCP's \"short-lived processes\" is its Observation Agent's generated profile text"
- passage (source 27): §4 "The Observation Agent builds Workload Profiles … For kernel compilation, it produces profiles like "CPU-intensive parallel compilation with short-lived processes, inter-process dependencies, targeting makespan minimization.""
- verdict: SUPPORTED.
- fix: none.

### D-F5-24 — SchedCP cites schbench
- location: docs/workload/grounding-sources.md:28; docs/workload/source-vetting.md:14, :87, :141
- repo: "a citation precedent (SchedCP cites it)"; ":141 SchedCP cites schbench at kernel.googlesource.com, not by its GitHub URL"
- passage (source 21): reference [12] at `https://kernel.googlesource.com/pub/scm/linux/kernel/git/mason/schbench`, 2016.
- verdict: SUPPORTED (the venue named at source-vetting.md:14 and :87 belongs to the venue claim, not checked here).
- fix: none.
