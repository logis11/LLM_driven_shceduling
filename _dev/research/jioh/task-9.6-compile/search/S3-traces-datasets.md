# S3 — public traces, datasets, build logs and benchmark databases

Reader class S3; topics T1, T2, T4, T5, T6, T7. Access date for everything: 2026-09-16. Outbound HTTPS through the session proxy; network reachable at start (brendangregg.com 200, raw.githubusercontent.com 200, buildd.debian.org 200, koji.fedoraproject.org 200, llvm-compile-time-tracker.com 200, opendata.blender.org 200, phoronix.com 200, bugs.launchpad.net 200, bugs.debian.org 200, autobuilder.yocto.io 200; openbenchmarking.org 403).

Copies are saved under `sources/S3-NN/` (gitignored). Candidate ids run S3-01 … S3-19; **S3-12 is withdrawn** (Gentoo forums thread, login-walled — folder holds only the login page), so 18 candidates are recorded. Every number computed by the reader from a downloaded file is labelled **reader's own computation** with the command; it locates a candidate and is not a value.

## 1. Search log

| # | date | engine / venue | query / URL | hits followed | dead ends (HTTP status) |
|---|------|----------------|-------------|---------------|-------------------------|
| 1 | 2026-09-16 | direct fetch (curl) | https://www.brendangregg.com/perf.html | S3-01 (section 6.7 Scheduler Analysis) | — (200) |
| 2 | 2026-09-16 | direct fetch (curl) | https://www.brendangregg.com/blog/2017-03-16/perf-sched.html | S3-02 | — (200) |
| 3 | 2026-09-16 | direct fetch (curl) | https://buildd.debian.org/status/package.php?p=linux | S3-03 (build log URLs) | — (200) |
| 4 | 2026-09-16 | direct fetch (curl) | https://llvm-compile-time-tracker.com/ | S3-04 | — (200) |
| 5 | 2026-09-16 | direct fetch (curl) | https://buildd.debian.org/status/fetch.php?pkg=linux&arch=amd64&ver=7.1.13-1&stamp=1788481014&raw=1 (streamed 3×) | S3-03 | first stream cut by proxy at 59 375 616 B (200, truncated body); streams 2–3 complete |
| 6 | 2026-09-16 | direct fetch (curl) | https://llvm-compile-time-tracker.com/about.php ; compare.php?from=0092388…&to=1de42f4…&stat=instructions:u ; same with &stat=task-clock&details=on | S3-04 | first details=on request 504 (server timeout); retry with --max-time 240 → 200 |
| 7 | 2026-09-16 | direct fetch (curl) | https://raw.githubusercontent.com/nikic/llvm-compile-time-data/master/README.md | S3-04 (README only; layout of the data repo not explored) | — |
| 8 | 2026-09-16 | direct fetch (curl) | https://koji.fedoraproject.org/koji/packageinfo?packageID=8 → buildinfo?buildID=3101293 → taskinfo?taskID=150245357 → taskinfo?taskID=150245382 → kojipkgs …/data/logs/x86_64/{build,root,hw_info,state}.log | S3-05 | — |
| 9 | 2026-09-16 | direct fetch (curl) | https://opendata.blender.org/ → /download/ → /snapshots/opendata-latest.zip (100 665 415 B) | S3-06 | — |
| 10 | 2026-09-16 | direct fetch (curl) | https://autobuilder.yocto.io/pub/ (+ /pub/non-release/, /pub/releases/, /pub/buildstats/) | none (listing shows only buildtools/ and extratools/) | /pub/non-release/ 404, /pub/releases/ 404, /pub/buildstats/ 404 |
| 11 | 2026-09-16 | direct fetch (curl) | https://openbenchmarking.org/test/pts/build-linux-kernel | none | 403 |
| 12 | 2026-09-16 | WebSearch | Phoronix "Timed Linux Kernel Compilation" defconfig build time cores -j | phoronix.com/news/Linux-16-Seconds-AMD-EPYC-2P (S3-07) | openbenchmarking.org/test/pts/build-linux-kernel 403 |
| 13 | 2026-09-16 | WebSearch | linux kernel compile "make -j1" vs "-j8" time table single core scaling benchmark | lkml.iu.edu 9901.1/1259, 9901.1/1406 (S3-08); kcbench man page (S3-16) | — |
| 14 | 2026-09-16 | WebSearch | ".ninja_log" llvm build public per-file start end times ninjatracing | none directly (tool pages only); led to GitHub code search (row 24) | — |
| 15 | 2026-09-16 | WebSearch | launchpad bug dkms make.log "CC [M]" "elapsed time" autoinstall | bugs.launchpad.net/bugs/2089335 (no make.log attached; see row 22) | — |
| 16 | 2026-09-16 | WebSearch | ananicy-cpp rules cc1 gcc make "type" compiler nice rules github | github.com/CachyOS/ananicy-rules, github.com/nefelim4ag/Ananicy (S3-11) | codeload.github.com tarballs 403; api.github.com 403; GitHub MCP tools restricted to the project repo |
| 17 | 2026-09-16 | WebSearch | public process accounting dataset lastcomm psacct process lifetime distribution unix | none (how-to pages and two arXiv tool papers, no dataset) | — |
| 18 | 2026-09-16 | WebSearch | gentoo forums MAKEOPTS poll "-j" what do you use | forums.gentoo.org/viewtopic-p-8695354.html | HTTP 200 but login wall ("The board requires you to be registered and logged in to view this forum"); folder S3-12 withdrawn |
| 19 | 2026-09-16 | WebSearch | yocto buildstats rusage ru_inblock "Elapsed time" per-task example output | wiki.yoctoproject.org InvestigatingBuildTime; docs ref-manual classes (S3-09); Packt cookbook page | subscription.packtpub.com 403 |
| 20 | 2026-09-16 | WebSearch | clamscan full system scan took hours "100% CPU" duration report | learn.microsoft.com Q&A 5550992 (S3-13) | — |
| 21 | 2026-09-16 | WebSearch | "perf sched timehist" OR "trace-cmd" kernel build "make -j" trace capture cc1 blog | only S3-02 again; no second public capture | — |
| 22 | 2026-09-16 | Launchpad API | ubuntu/+source/dkms searchTasks search_text=make.log (15 hits) → bugs 1871162, 1663876, 1689390, 1578455 attachments | S3-10 | — |
| 23 | 2026-09-16 | direct fetch | bugs.debian.org/cgi-bin/pkgreport.cgi?pkg=dkms;archive=both | none | HTTP 200 but JavaScript challenge page ("I Challenge Thee"), no bug list |
| 24 | 2026-09-16 | GitHub code search (MCP) | `"# ninja log v5" filename:.ninja_log` (54 656 hits); `"lib/IR/CMakeFiles/LLVMCore.dir" filename:.ninja_log` (7 hits) | raw.githubusercontent.com leikang123/LLVM-NMX build/.ninja_log; hoholee12/rpcs3-custom llvm_build/.ninja_log (S3-14) | — |
| 25 | 2026-09-16 | GitHub code search (MCP) | `"DKMS make.log for" "elapsed time" filename:make.log`; `NUM_CPU_JOBS defconfig repo:phoronix-test-suite/test-profiles`; `taskset defconfig "make -j" path:.github/workflows` | 0 hits each | — |
| 26 | 2026-09-16 | direct fetch (guessed) | raw.githubusercontent.com/phoronix-test-suite/test-profiles/master/pts/build-linux-kernel-1.16.0/{install.sh,test-definition.xml} | S3-07 | — |
| 27 | 2026-09-16 | GitHub code search (MCP) + WebSearch | `"rusage ru_inblock" "Elapsed time" "Event: TaskStarted"` (197 120 hits) ; "1502541082.15" buildstats ncurses | raw liyapenggo/raspberrypi3-openbmc …/buildstats/…/quilt-native-0.65-r0/do_compile (S3-09) | the ncurses example traced to a Packt book page, 403 |
| 28 | 2026-09-16 | direct fetch (guessed) | raw.githubusercontent.com/CachyOS/ananicy-rules/master/{00-types.types,00-cgroups.cgroups,README.md}; nefelim4ag/Ananicy README.md; WebFetch of the 00-default and "Development & Programming" tree pages | S3-11 | guessed paths 00-default/00-types.types etc. 404 |
| 29 | 2026-09-16 | WebSearch | kcbench results table "-j" 1 2 4 8 16 threads kernel compile time seconds scaling Ryzen | kroah.com 2020/09/18 fast-kernel-builds (S3-15); kcbench 0.9.0 announcement (S3-16) | lore.kernel.org not tried (403 known); spinics.net 403 (squid "Access Denied"); rescloud mirror 200 |
| 30 | 2026-09-16 | WebSearch | kernel build time cold cache vs warm page cache drop_caches "make -j" measured seconds difference | nickdesaulniers.github.io ccache post (S3-17; ccache, not page cache) | — |
| 31 | 2026-09-16 | WebSearch | x264 OR ffmpeg encode CPU utilization "all cores" threads scaling benchmark percent utilization measured | none with measured utilisation | — |
| 32 | 2026-09-16 | WebSearch | reddit archlinux MAKEFLAGS "-j" nproc poll what do you use makepkg.conf survey | none (ArchWiki only, documentation class) | — |
| 33 | 2026-09-16 | WebSearch | "taskset -c 0" "make -j" kernel build single core pinned time result | lkml.iu.edu 0602.2/1805 (S3-19; concurrency vs -j on 2 cores, not a pin) | — |
| 34 | 2026-09-16 | WebSearch | tracker-miner-fs OR baloo_file_extractor "100% CPU" hours full index bug report | bugs.launchpad.net/bugs/2025523 (S3-18) | gitlab.gnome.org/GNOME/localsearch/-/issues/228 HTTP 406 |
| 35 | 2026-09-16 | WebSearch | pytorch CPU training "torch.get_num_threads" top shows CPU utilization percent | none with a measured log | — |
| 36 | 2026-09-16 | direct fetch | gitlab.com/knurd42/kcbench/-/raw/master/kcbench.man1.md | S3-16 | — |
| 37 | 2026-09-16 | direct fetch | chromium-build-stats.appspot.com | HTTP 200; the page is a form "compile step URL or gs URI" with no browsable data (not a login wall, but nothing to read without a step URL) | — |

## 2. Candidates

### S3-01 — Brendan Gregg, "perf Examples", section 6.7 "Scheduler Analysis" (web page)

**Citation.** Brendan Gregg, *Linux perf Examples*, section 6.7 "Scheduler Analysis", https://www.brendangregg.com/perf.html, page footer "Last Updated: 29-Jul-2020" (`perf.html:3690`).

**Copy read.** URL https://www.brendangregg.com/perf.html, HTTP 200, fetched 2026-09-16 with curl; saved as `sources/S3-01/perf.html` (210 726 bytes); SHA-256 `a60d127603220a9f74776ed9c370a3ffc2d69383366f44241d3460ab434e99a4`. Locators below are line numbers of that HTML file. Parts of the tables sit inside HTML comment blocks (`<!-- … -->`) in the source, i.e. present in the file but not rendered in a browser; those are marked "(HTML-commented)".

**Verbatim passages.**

- `perf.html:2361–2369`: "The current overhead of this tool (as of up to Linux 4.10) may be noticeable, as it instruments and dumps scheduler events to the perf.data file for later analysis. For example: `# perf sched record -- sleep 1` / `[ perf record: Woken up 1 times to write data ]` / `[ perf record: Captured and wrote 1.886 MB perf.data (13502 samples) ]` … That's 1.9 Mbytes for one second, including 13,502 samples. The size and rate will be relative to your workload and number of CPUs (this example is an 8 CPU server running a software build)."
- `perf.html:2415–2420` (HTML-commented raw `perf script` rows): "`cc1 16881 [000] 991962.880058: sched:sched_stat_runtime: comm=cc1 pid=16881 runtime=3999231 [ns] vruntime=78979518773 [ns]`" / "`:17024 17024 [004] 991962.880058: sched:sched_stat_runtime: comm=cc1 pid=17024 runtime=3866637 [ns] …`" / "`cc1 16900 [001] … runtime=3006028 [ns]`" / "`cc1 16825 [006] … runtime=3999423 [ns]`" / "`cc1 16880 [002] … runtime=3999502 [ns]`" / "`cc1 16945 [003] … runtime=3008672 [ns]`".
- `perf.html:2475–2493` (`perf sched latency`, rendered part), header "`Task | Runtime ms | Switches | Average delay ms | Maximum delay ms | Maximum delay at`", rows:
  - "`cat:(6) | 12.002 ms | 6 | avg: 17.541 ms | max: 29.702 ms | max at: 991962.948070 s`"
  - "`ar:17043 | 3.191 ms | 1 | avg: 13.638 ms | max: 13.638 ms`"
  - "`rm:(10) | 20.955 ms | 10 | avg: 11.212 ms | max: 19.598 ms`"
  - "`objdump:(6) | 35.870 ms | 8 | avg: 10.969 ms | max: 16.509 ms`"
  - "`:17008:17008 | 462.213 ms | 50 | avg: 10.464 ms | max: 35.999 ms`"
  - "`grep:(7) | 21.655 ms | 11 | avg: 9.465 ms | max: 24.502 ms`"
  - "`fixdep:(6) | 81.066 ms | 8 | avg: 9.023 ms | max: 19.521 ms`"
  - "`mv:(10) | 30.249 ms | 14 | avg: 8.380 ms | max: 21.688 ms`"
  - "`ld:(3) | 14.353 ms | 6 | avg: 7.376 ms | max: 15.498 ms`"
  - "`recordmcount:(7) | 14.629 ms | 9 | avg: 7.155 ms | max: 18.964 ms`"
  - "`svstat:17067 | 1.862 ms | 1 | avg: 6.142 ms | max: 6.142 ms`"
  - "`cc1:(21) | 6013.457 ms | 1138 | avg: 5.305 ms | max: 44.001 ms | max at: 991963.436070 s`"
  - "`gcc:(18) | 43.596 ms | 40 | avg: 3.905 ms | max: 26.994 ms`"
  - "`ps:17073 | 27.158 ms | 4 | avg: 3.751 ms | max: 8.000 ms`"
- `perf.html:2495–2513` (HTML-commented continuation of the same table): "`sed:17075 | 2.993 ms | 3`", "`make:(18) | 53.968 ms | 114 | avg: 2.331 ms | max: 12.986 ms`", "`perl:17068 | 4.266 ms | 2`", "`chown:(6) | 17.345 ms | 6`", "`lsb_release:17136 | 81.920 ms | 4`", "`echo:17089 | 1.718 ms | 1`", "`ls:17101 | 3.340 ms | 1`", "`as:(16) | 121.816 ms | 69 | avg: 1.837 ms | max: 23.199 ms`", "`xargs:17077 | 2.655 ms | 4`", "`bash:(2) | 6.363 ms | 7`", "`sh:(25) | 107.078 ms | 108 | avg: 1.025 ms | max: 16.309 ms`", "`:17024:17024 | 151.717 ms | 232`", "`:17016:17016 | 208.478 ms | 356`", "`recordProgramSt:17113 | 71.450 ms | 14`", "`cut:17076 | 2.069 ms | 2`", "`chmod:(2) | 3.692 ms | 2`", "`redis-server:(2) | 1.659 ms | 22`", "`catalina.sh:17063 | 23.114 ms | 26`", "`ksoftirqd/7:52 | 0.821 ms | 22`".
- `perf.html:2520–2528`: "`sh 17028 [001] 991962.918368: sched:sched_wakeup_new: comm=sh pid=17030 prio=120 target_cpu=002` [...] `cc1 16819 [002] 991962.948070: sched:sched_switch: prev_comm=cc1 prev_pid=16819 prev_prio=120 prev_state=R ==> next_comm=sh next_pid=17030 next_prio=120` … The time from the wakeup (991962.918368, which is in seconds) to the context switch (991962.948070) is 29.702 ms. This process is listed as "sh" (shell) in the raw events, but execs "cat" soon after, so is shown as "cat" in the perf sched latency output."
- `perf.html:2536–2557` (`perf sched map`, 8 columns): rows include "`B0 => cc1:16863`", "`C0 => :17023:17023`", "`J0 => cc1:16996`", "`K0 => cc1:16945`", "`M0 => make:16637`", "`N0 => make:16545`", "`O0 => cc1:16819`", "`Q0 => cc1:16831`", "`R0 => cc1:16825`", "`S0 => cc1:16900`"; `perf.html:2576`: "This is an 8 CPU system, and you can see the 8 columns for each CPU starting from the left."
- `perf.html:2623–2671` (`perf sched timehist`): "perf sched timehist was added in Linux 4.10, and shows the scheduler latency by event, including the time the task was waiting to be woken up (wait time) and the scheduler latency after wakeup to running (sch delay)." Columns "`time cpu task name [tid/pid] wait time (msec) sch delay (msec) run time (msec)`"; rendered rows include "`991962.881839 [0003] cat[17022] 0.000 0.000 1.746`"; HTML-commented rows include "`991962.883102 [0006] make[16637] 0.000 0.004 0.813`", "`991962.883880 [0002] sh[17023] 0.000 0.000 3.810`", "`991962.884843 [0006] make[16545] 0.000 0.004 1.740`", "`991962.886893 [0003] cc1[16945] 1.758 0.000 5.053`", "`991962.888077 [0002] cc1[16819] 0.000 0.000 4.196`", "`991962.889559 [0002] cc1[16819] 0.007 0.000 1.474`", "`991962.892078 [0007] cc1[16863] 0.000 0.000 12.007`", "`991962.892083 [0003] cc1[16945] 0.024 0.000 5.165`"; rendered tail rows "`991963.885740 [0001] :17008[17008] 25.613 0.000 0.057`", "`991963.886009 [0001] sleep[16999] 1000.104 0.006 0.269`", "`991963.886018 [0005] cc1[17083] 19.998 0.000 9.948`".
- `perf.html:2713–2750` (`perf sched timehist -MVw`, wakeup rows): "`991962.882284 [0006] :17020 awakened: make[16637]`", "`991962.883098 [0006] make[16637] awakened: make[16545]`", "`991962.883770 [0002] sh[17023] awakened: sh[17025]`", "`991962.884703 [0006] make[16545] awakened: make[17026]`".

**Coverage.**
- T1 — covers, partially. Object: tasks present during one second of a parallel "software build" (not named; the task names in the table — `fixdep`, `recordmcount`, `cc1`, `gcc`, `as`, `ld`, `ar`, `objdump`, `make`, `sh` — are what the page shows; the reader notes that `fixdep` and `recordmcount` are kbuild helper names but the page itself does not say "kernel"). Unit: per-comm counts of distinct tasks seen in the window ("`cc1:(21)`", "`gcc:(18)`", "`as:(16)`", "`sh:(25)`", "`make:(18)`", "`fixdep:(6)`", "`ld:(3)`") and summed on-CPU "Runtime ms" per comm with context-switch counts. Statistic: sum, count, average/maximum scheduler delay. Scope: one 1-second window, 8 CPUs. Population: one build on one machine. It does not give per-process lifetimes or a CPU-time distribution over whole processes, only per-comm runtime totals and per-schedule slices.
- T2 — covers, partially. `sched_stat_runtime` rows give `cc1` run slices of ~3.0–4.0 ms; timehist rows give per-schedule run time / wait time for `cc1` (e.g. "`cc1[16863] … 12.007`" ms run, "`cc1[17083] 19.998 0.000 9.948`" wait/delay/run). No warm/cold cache distinction, no I/O blocking attribution (wait time is not broken down into I/O vs. other), no per-TU CPU time.
- T4 — does not cover (no `-j` stated).
- T5 — does not cover.
- T6 — covers, marginally: "8 CPU server running a software build" as the workload of a `perf sched` demonstration; no confinement, no lifetime distribution.
- T7 — does not cover.

**One observation?** Yes — one 1-second `perf sched record` on one machine. Machine: "an 8 CPU server" (perf.html); the S3-02 copy of the same capture names it (see S3-02). Subject: "a software build" — project, configuration and `-j` are not named. Window: "sleep 1" (1 s), timestamps 991962.879966–991963.886018 s.

### S3-02 — Brendan Gregg, "perf sched for Linux CPU scheduler analysis" (blog post, 16 Mar 2017)

**Citation.** Brendan Gregg, "perf sched for Linux CPU scheduler analysis", blog post dated 16 Mar 2017, https://www.brendangregg.com/blog/2017-03-16/perf-sched.html.

**Copy read.** URL above, HTTP 200, fetched 2026-09-16 with curl; saved as `sources/S3-02/perf-sched.html` (35 215 bytes); SHA-256 `37a80dd6662f1a669b36f0d3f45ea5af744aca012b646fd238e0670991e43bbe`. Locators are line numbers in the text-stripped rendering (tags removed, blank lines dropped, `sed 's/<[^>]*>//g' | grep -v '^\s*$'`) and, where quoted with `raw:`, raw HTML line numbers.

**Verbatim passages.**

- text line 91: "Linux perf gained a new CPU scheduler analysis view in Linux 4.10: perf sched timehist. … (I've also added this content to my perf examples page.)"
- text lines 94–97: "`# perf sched record -- sleep 1` / `[ perf record: Woken up 1 times to write data ]` / `[ perf record: Captured and wrote 1.886 MB perf.data (13502 samples) ]` That's 1.9 Mbytes for one second, including 13,502 samples. The size and rate will be relative to your workload and number of CPUs (this example is an 8 CPU server running a software build)."
- text lines 98–110 (`perf script --header`): "`# captured on: Sun Feb 26 19:40:00 2017`" / "`# hostname : bgregg-xenial`" / "`# os release : 4.10-virtual`" / "`# perf version : 4.10`" / "`# arch : x86_64`" / "`# nrcpus online : 8`" / "`# nrcpus avail : 8`" / "`# cpudesc : Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz`" / "`# cpuid : GenuineIntel,6,62,4`" / "`# total memory : 15401700 kB`" / "`# cmdline : /usr/bin/perf sched record -- sleep 1`".
- text lines 111–119: the recorded events are "`sched:sched_switch`", "`sched:sched_stat_wait`", "`sched:sched_stat_sleep`", "`sched:sched_stat_iowait`", "`sched:sched_stat_runtime`", "`sched:sched_process_fork`", "`sched:sched_wakeup`", "`sched:sched_wakeup_new`", "`sched:sched_migrate_task`".
- text lines 141–154 (`perf sched latency`, rendered, `raw:239–257`): the same 14 rows as S3-01 (`cat:(6)` … `ps:17073`), including "`cc1:(21) | 6013.457 ms | 1138 | avg: 5.305 ms | max: 44.001 ms | max at: 991963.436070 s`", "`fixdep:(6) | 81.066 ms | 8 | avg: 9.023 ms | max: 19.521 ms`", "`gcc:(18) | 43.596 ms | 40 | avg: 3.905 ms | max: 26.994 ms`"; the table ends with "`...]`" (text line 155), i.e. the post truncates the table after `ps:17073`.
- text lines 156–162: same wakeup→switch explanation as S3-01 ("The time from the wakeup (991962.918368, which is in seconds) to the context switch (991962.948070) is 29.702 ms. This process is listed as "sh" (shell) in the raw events, but execs "cat" soon after").
- text lines 164–189: same `perf sched map` as S3-01 with "`B0 => cc1:16863`", "`M0 => make:16637`", "`N0 => make:16545`" etc.; "This is an 8 CPU system".

**Coverage.** Same capture as S3-01 (identical timestamps 991962.8799…), so the same per-topic coverage; the added value is the machine identification: T1/T2/T6 as in S3-01. T4, T5, T7 — does not cover.

**One observation?** Yes — the same single 1-second trace as S3-01. Machine named here: hostname `bgregg-xenial`, `4.10-virtual`, x86_64, 8 CPUs online, `Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz`, 15 401 700 kB memory, captured 26 Feb 2017. Subject: "a software build", project/config/`-j` not named. Window: 1 s.

### S3-03 — Debian buildd build log, source package `linux` 7.1.13-1, amd64, builder x86-conova-01 (sbuild, 3–4 Sep 2026)

**Citation.** Debian Package Auto-Building, build log for `linux` 7.1.13-1 on amd64, sbuild on `x86-conova-01.debian.org`, started "Thu, 03 Sep 2026 21:35:10 +0000", https://buildd.debian.org/status/fetch.php?pkg=linux&arch=amd64&ver=7.1.13-1&stamp=1788481014&raw=1 (linked from https://buildd.debian.org/status/package.php?p=linux, "Page generated on 2026-09-16 21:20:16 UTC").

**Copies read.**
- Status page: https://buildd.debian.org/status/package.php?p=linux, HTTP 200, 2026-09-16, `sources/S3-03/package.php.html` (23 662 bytes), SHA-256 `50b6894aed3189b0a54146d411775b990fe5024a89321defdc6db4e1b9284791`.
- The amd64 log (raw=1): not saved whole (214 MB, over the download allowance); streamed three times with `curl -sSL "$URL" | tee >(sha256sum) | awk …`. The first stream was cut by the proxy at 59 375 616 bytes / 72 579 lines (hash `8225e082…`, discarded); the second and third streams were complete and both hash to SHA-256 `25b9841439e0b8525ce6ef7ff37fcc7ec7eba355823e23944cf0ec839ec0aa58`, **214 411 815 bytes, 644 941 lines** (`wc -c`, `wc -l` on the stream). Only extracted lines are kept: `sources/S3-03/amd64-log.extract{,2,3}.txt`, `amd64-log.tail.txt` (last 150 lines), `amd64-log.url`. Locators `log:N` are line numbers in that full stream.

**Verbatim passages.**
- `log:2`: "sbuild (Debian sbuild) 0.91.9~bpo13+1 (23 May 2026) on x86-conova-01.debian.org"
- `log:5`: "| linux 7.1.13-1 (amd64)                       Thu, 03 Sep 2026 21:35:10 +0000 |"
- `log:12–15`: "Machine Architecture: amd64" / "Host Architecture: amd64" / "Build Architecture: amd64" / "Build Type: any"
- `log:1623`: "Kernel: Linux 6.12.107+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.107-1 (2026-08-29) amd64 (x86_64)"
- `log:2668`: "DEB_BUILD_OPTIONS=parallel=6"
- `log:2708`: "make[1]: Entering directory '/build/reproducible-path/linux-7.1.13'"
- `log:7235` (first compiler line, abridged in the middle): "   x86_64-linux-gnu-gcc-15 -Wp,-MMD,scripts/mod/.empty.o.d -nostdinc -I/build/reproducible-path/linux-7.1.13/arch/x86/include … -DKBUILD_MODNAME='"empty"' -D__KBUILD_MODNAME=empty -c -o scripts/mod/empty.o /build/reproducible-path/linux-7.1.13/scripts/mod/empty.c"
- `log:30187–30188`: "# CC [M]  net/8021q/vlanproc.o" / "   x86_64-linux-gnu-gcc-15 -Wp,-MMD,net/8021q/.vlanproc.o.d -nostdinc -I/build/reproducible-path/linux-7.1.13/arch/x86/include -I./arch/x86/include/generated …"
- `log:33497–33500`: "# LD [M]  net/can/j1939/can-j1939.o" / "  x86_64-linux-gnu-ld -m elf_x86_64 -z noexecstack --no-warn-rwx-segments   -r -o net/can/j1939/can-j1939.o @net/can/j1939/can-j1939.mod  ; ./tools/objtool/objtool --hacks=jump_label --hacks=noinstr --hacks=skylake --ibt --orc --retpoline --rethunk -…" / "# cmd_gen_objtooldep net/can/j1939/can-j1939.o" / "   { echo ; echo 'net/can/j1939/can-j1939.o: $(wildcard ./tools/objtool/objtool)' ; } >> net/can/j1939/.can-j1939.o.cmd"
- `log:73881`: "+ pahole -J -j6 --btf_features=encode_force,var,float,enum64,decl_tag,type_tag,optimized_func,consistent_func,decl_tag_kfuncs --btf_features=attributes --btf_features=layout -j6 --btf_features=+reprod…"
- `log:599161`: " DEB_BUILD_OPTIONS="parallel=6"" (in the .buildinfo section)
- `log:644919–644934` (Summary): "Build-Space: 100835680" / "Build-Time: 9443" / "Install-Time: 92" / "Package-Time: 9567" / "Finished at 2026-09-04T00:14:37Z" / "Build needed 02:39:27, 100835680k disk space"
- Status page (`package.php.html`, rendered row for amd64): "amd64    7.1.13-1   Installed   12d 20h 13m   x86-conova-01     kernel"; the page's "Tail of log for linux on sh4" shows the verbose kbuild form including "perl /build/reproducible-path/linux-7.1.13/scripts/recordmcount.pl "sh" "little" "32" "sh4-linux-gnu-objdump" …" and "# LD [M]  net/hsr/hsr.o / sh4-linux-gnu-ld -EL -z noexecstack --no-warn-rwx-segments   -r -o net/hsr/hsr.o @net/hsr/hsr.mod".

**Reader's own computations** (over the full 214 MB stream; awk on the third stream; they locate, they are not values):
- `awk '/^ +x86_64-linux-gnu-gcc-15 .* -c -o /{n++}'` → 45 599 target-compiler `-c -o` lines, of which 29 416 end in `.o <path>.c` and 342 in `.o <path>.S` (`/-c -o [^ ]*\.o [^ ]*\.c *$/`, `…\.S *$/`); all `x86_64-linux-gnu-gcc-15` lines: 45 643; host `gcc … -c -o`: 87.
- kbuild tag lines: `^# CC \[M\] ` 37 222; `^# CC  ` 8 050 (45 272 `CC` tags in total); `^# LD` 12 431; `^# AS` 342; `^# AR` 2 239; `^# HOSTCC` 129; `^# RUSTC` 45; `# INSTALL` 18 920; `# STRIP`/`# XZ`/`# SIGN`/`cmd_mod`/`cmd_strip` 9 447 each; `# BTF` 9 305.
- Other tools: `x86_64-linux-gnu-ld` lines 12 488; `objtool/objtool` 18 915; `x86_64-linux-gnu-strip` 9 510; `pahole|resolve_btfids` 19 388; explicit `scripts/basic/fixdep` command lines only 4, `scripts/genksyms/genksyms` 1, `scripts/mod/modpost` 6 (kbuild does not echo the `fixdep` step per object in this verbose output; the count is of echoed command lines only).
- Caveat: the Debian source package builds several kernel flavours and the `tools/` packages in one log, so the counts span more than one kernel configuration; the log does not say how many CPUs `x86-conova-01` has, and no explicit `make -jN` line appears — the parallelism appears as `DEB_BUILD_OPTIONS=parallel=6` and as `pahole … -j6`.

**Coverage.**
- T1 — covers, partially. Object: the command lines kbuild echoes (verbose `V=1`-style) for one Debian `linux` package build: per translation unit one `x86_64-linux-gnu-gcc-15 … -c -o` line, per module one `ld -r` plus an `objtool` invocation, per `.mod.o` a further compile, `pahole`, `strip`, `xz`, signing. Unit: command lines, not processes; no PIDs, lifetimes or CPU times. Statistic: counts (reader's own). Scope: one full package build of all amd64 flavours. Population: one build. It does not show `cc1`/`as`/`collect2` as separate processes (only the driver line), and does not show lifetimes.
- T2 — does not cover (no per-TU time).
- T4 — covers: an observed distribution-packaging parallelism for the kernel package, "DEB_BUILD_OPTIONS=parallel=6" on buildd `x86-conova-01` (one build; the builder's core count is not stated in the log).
- T5 — does not cover.
- T6 — covers, marginally: a whole-build wall time for a distribution kernel package build, "Build-Time: 9443" seconds / "Build needed 02:39:27" at `parallel=6`; no process counts or CPU totals.
- T7 — does not cover.

**One observation?** Yes: one build, machine named only as `x86-conova-01.debian.org` (amd64; core count not stated; host kernel "Linux 6.12.107+deb13-amd64"), subject `linux` 7.1.13-1 Debian configs (all amd64 flavours + tools), `parallel=6`, window 2026-09-03 21:35:10 UTC → 2026-09-04 00:14:37 UTC.

### S3-04 — LLVM Compile-Time Tracker (nikic), per-file `task-clock` for CTMark

**Citation.** Nikita Popov, *LLVM Compile-Time Tracker*, https://llvm-compile-time-tracker.com/ (about page https://llvm-compile-time-tracker.com/about.php; raw data at https://github.com/nikic/llvm-compile-time-data, server code at https://github.com/nikic/llvm-compile-time-tracker). Comparison page read: `compare.php?from=00923887162fdb44e80531687ffacb6a085cb008&to=1de42f4fcc07cb4163732f5bfc112c47b01b4044&stat=task-clock&details=on` (two adjacent LLVM commits taken from the tracker's index on 2026-09-16).

**Copies read (all 2026-09-16, curl).**
- `sources/S3-04/index.html` — https://llvm-compile-time-tracker.com/ , HTTP 200, 985 820 B, SHA-256 `1267a54560c5d3d2faf853a4acfc41c4f8e23dcbb0f8c63b3b2340f06a5aa18d`.
- `sources/S3-04/about.html` — about.php, HTTP 200, 3 858 B, SHA-256 `1d42303120bb035b8960811afe78a43c611bd8ff1e9440b64432578519418b77`.
- `sources/S3-04/compare-0092388-1de42f4.html` — `stat=instructions:u`, no details, HTTP 200, 13 450 B, SHA-256 `8c1f685fff9bdf94e6a5e9e839835fe370843367124c3ba1885f257b52299df5`.
- `sources/S3-04/compare-details-task-clock.html` — `stat=task-clock&details=on`, first attempt HTTP 504, retry HTTP 200, 708 944 B, SHA-256 `74bc9c499efa5011ec884e8f1cc5c0ba0858d86d656bd422181400c7bf6ac610`.
- `sources/S3-04/llvm-compile-time-data-README.md` — raw.githubusercontent.com/nikic/llvm-compile-time-data/master/README.md, HTTP 200, 345 B, SHA-256 `8055db1a1b95e2dad9578243244d4ce8e209c2123bd24b5a5c8e91756cc7693d`.

**Verbatim passages.**
- about.php (text-stripped): "The compile time tracker tests the CTMark portion of the LLVM test-suite against specific cached CMake configurations." … "The $CONFIGs used by the tracker are O3, ReleaseThinLTO, ReleaseLTO-g and O0-g." … "Next, you will want to pick out a single file with a particularly large regression by enabling the "Per-file details" checkbox on the comparison page." … "Compilers: host : gcc 11.4 / stage1 : clang compiled using host compiler (release build) / stage2 : clang compiled using stage1 compiler (release build with ThinLTO)" … "Displayed statistics for clang generally refer to the stage2 build. The stage1 build uses ccache and as such does not produce stable timing results." … "Tested configurations: stage1-O3 : -O3, stage1 clang, native x86_64 target … stage2-O0-g : -O0 -g, stage2 clang, native x86_64 target".
- compare page, metric list (text-stripped): "instructions / instructions:u / max-rss / task-clock / cycles / branches / branch-misses / wall-time / size-total / size-text / size-data / size-bss / size-file".
- compare-details-task-clock.html line 42: "Warning: The task-clock metric is very noisy and likely not meaningful for comparisons between specific revisions." followed by "stage1-O3:"; lines 43–49: "Benchmark Old New / kimwitu++ / 5771ms / 5711ms (-1.03%)"; lines 137–140: "CMakeFiles/sqlite3.dir/sqlite3.c.o / 4227ms / 4367ms ( +3.31% )".
- README.md (lines 1–7): "LLVM Compile Time Data … This repository contains raw compile-time statistics for LLVM. The data can be viewed at http://llvm-compile-time-tracker.com."
- Neither the about page nor the compare page states the tracker machine's CPU model, core count, or the `-j` used for the builds; the about page says how to reproduce ("cmake .. -G Ninja -C ../cmake/caches/$CONFIG.cmake") and how to isolate one file ("ninja -v lencod" then "valgrind --tool=callgrind $PATH_TO_CLANG …").

**Reader's own computation** (python over `compare-details-task-clock.html`, "Old" column, rows whose name ends in `.o`; command in `sources/S3-04/details-parse.txt`): per configuration 632 per-file rows and 21 benchmark rows (9 CTMark programs plus their `.link` steps plus geomean). stage1-O3 task-clock per object file: min 5 ms, p10 25, p25 52, p50 96, mean 143, p75 144, p90 236, p99 634, max 10 446 ms (`CMakeFiles/tramp3d-v4.dir/tramp3d-v4.cpp.o`); sum 90 298 ms. stage1-O0-g: p50 46, p90 112, max 2 963 ms, sum 41 360 ms. stage2-O3: p50 85, p90 212, max 9 564 ms. These locate the shape of the distribution; the page itself warns the metric is noisy.

**Coverage.**
- T1 — does not cover (no processes).
- T2 — covers: object = one clang compilation per CTMark object file (632 files across 9 programs), unit = `task-clock` in ms (also `instructions:u`, `max-rss`, `wall-time`, `cycles` selectable), statistic = one value per file per commit (distribution computable by the reader as above), scope = CTMark at four optimisation configs, native x86_64 and aarch64 cross, population = one tracker machine (not described on the pages read). No blocking/I-O breakdown, no cache-state statement.
- T4 — does not cover (no `-j`).
- T5, T6, T7 — does not cover.

**One observation?** Per commit yes (one machine, one build per config); the machine is not named on the pages read; subject = CTMark programs (kimwitu++, sqlite3, consumer-typeset, Bullet, tramp3d-v4, mafft, ClamAV, lencod, SPASS, 7zip) at stated configs; window = per-commit builds (the page compared commits `0092388…`→`1de42f4…`).

### S3-05 — Fedora Koji build `kernel-7.2.6-300.fc45`, x86_64 `buildArch` task 150245382 (mock/rpmbuild logs)

**Citation.** Fedora Koji, build kernel-7.2.6-300.fc45 (buildID 3101293), task 150245357 → buildArch x86_64 task 150245382; logs at https://kojipkgs.fedoraproject.org//packages/kernel/7.2.6/300.fc45/data/logs/x86_64/{build.log,root.log,hw_info.log,state.log} (the task page links the same files under `/work/tasks/5382/150245382/`).

**Copies read (2026-09-16, curl, all HTTP 200).**
- `sources/S3-05/buildinfo.html` (306 265 B) SHA-256 `f2917f5189769a7509511c44e3b26a4152a10a300bbee0e2cf6e10035392487e`
- `sources/S3-05/taskinfo-150245357.html` (11 679 B) SHA-256 `ddbda4f85e3bf7c7ccc7ad2052ec98b8fb215127aea4a42679944a9752316e7a`
- `sources/S3-05/taskinfo-150245382.html` (23 457 B) SHA-256 `a3b8f4d517bcb44140b206230e0c32f426e24ee32577ffe2004a375987216013`
- `sources/S3-05/x86_64-build.log` (7 872 440 B, 15 939 lines) SHA-256 `db1316932e2d47bafbbfb59ca8fac9777aa63f70357d1835ada5ff748244090e`
- `sources/S3-05/x86_64-root.log` (460 397 B) SHA-256 `632c244f80a868c2c255584cbada82a2deb6d23a1b4ebfc54d1bc18173a322ff`
- `sources/S3-05/x86_64-hw_info.log` (4 477 B) SHA-256 `68e633adb4300388eff8bf5412eb411c95216fe952916a6c04f78612d9fa1b41`
- `sources/S3-05/x86_64-state.log` (1 234 B) SHA-256 `2ab1b5a7004e0441dc36f7e9edc3ebeb704a683dd9a756d1ce5c5a8adc0be534`

**Verbatim passages.**
- `hw_info.log:1–13`: "CPU info:" / "Architecture: x86_64" / … / "CPU(s): 64" / "On-line CPU(s) list: 0-63" / "Vendor ID: AuthenticAMD" / "Model name: AMD EPYC 9174F 16-Core Processor" / "Thread(s) per core: 2" / "Core(s) per socket: 16" / "Socket(s): 2".
- `root.log:1`: "INFO buildroot.py:704:  Mock Version: 6.8"; `root.log:13`: "DEBUG util.py:537:  CPU(s): 64".
- `state.log` (whole): "2026-09-14 23:09:21,419 - Start: rpmbuild kernel-7.2.6-300.fc45.src.rpm" / "2026-09-15 00:17:22,200 - Finish: rpmbuild kernel-7.2.6-300.fc45.src.rpm".
- `build.log:1266`: "Executing(%build): /bin/sh -e /var/tmp/rpm-tmp.nEkkMw"; `build.log:1324` (end of the line): "… -specs=/usr/lib/rpm/redhat/redhat-package-notes  ' -j64 mrproper"; `build.log:1335–1336` (abridged): "kernel.spec:: BUILDING A KERNEL FOR debug x86_64..." / "+ /usr/bin/make -s 'HOSTCFLAGS=-O2  -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security …"; `build.log:1526` (end): "' -j64 ARCH=x86_64 INSTALL_MOD_PATH=/builddir/build/BUILD/kernel-7.2.6-build/BUILDROOT -j64 modules_install KERNELRELEASE=7.2.6-300.fc45.x86…"; `build.log:6042`: "  BUILD:   Doing 'make -j64' parallel build"; `build.log:1685`: "+ env PYTHONHASHSEED=0 /usr/bin/python3 -s -B -m compileall -j64 …"; `build.log:13725`: "+ /usr/bin/find-debuginfo -j64 --strict-build-id …".

**Reader's own computation.** `grep -c '^  CC ' x86_64-build.log` → 29; `grep -c ' -c -o '` → 547; the kernel `make` is invoked with `-s` (silent), so the log does not list per-object compiler lines for the kernel itself (only the `tools/` sub-builds echo commands). `-j64` equals the builder's "CPU(s): 64".

**Coverage.**
- T1 — does not cover usefully (silent make; no per-object lines).
- T2 — does not cover.
- T4 — covers: an observed distribution build parallelism, `make … -j64` on a 64-thread builder ("CPU(s): 64", "AMD EPYC 9174F 16-Core Processor", 2 sockets × 16 cores × 2 threads); the value is what rpmbuild expanded, the log does not print the macro name.
- T5 — does not cover.
- T6 — covers, marginally: one whole-package wall time, rpmbuild 2026-09-14 23:09:21 → 2026-09-15 00:17:22 (about 68 min, reader's subtraction) for the Fedora kernel package (several variants incl. "debug") at `-j64` on the machine above; no process counts.
- T7 — does not cover.

**One observation?** Yes; machine named (hw_info.log), subject = Fedora kernel 7.2.6-300.fc45 x86_64 with Fedora configs, `-j64`, window = state.log timestamps.

### S3-06 — Blender Open Data, daily snapshot `opendata-2026-09-16-000000+0000.jsonl` (Blender Benchmark results)

**Citation.** Blender Foundation, *Blender Open Data*, https://opendata.blender.org/ ; download page https://opendata.blender.org/download/ ("Here you can download the daily snapshot of the entire opendata.blender.org dataset."); snapshot https://opendata.blender.org/snapshots/opendata-latest.zip, `last-modified: Wed, 16 Sep 2026 00:01:20 GMT`, licence CC0 1.0.

**Copies read (2026-09-16, curl).** `sources/S3-06/download.html` HTTP 200, 36 298 B, SHA-256 `e61f9fa5ed59d1e7f58308210442ec5bfbf37a6440999818e7b3317116d75a35`; `sources/S3-06/opendata-latest.zip` HTTP 200, 100 665 415 B, SHA-256 `eec155820dc4c6e9995c9b011b6fa02a97b8315d888b4a0ab7a184b9b3f09aea`, containing `LICENSE.txt` (7 049 B), `README.txt` (374 B), `opendata-2026-09-16-000000+0000.jsonl` (1 874 702 760 B, read as a stream from the zip, never extracted). Parse output in `sources/S3-06/parse-summary.txt`.

**Verbatim passages.**
- `README.txt`: "# Blender Open Data / This archive contains a direct dump of [Blender Open Data](https://opendata.blender.org/). The data itself is contained in the `xxxx.jsonl` file. This file contains a JSON-formatted document on each line. / ## License / The data in this archive is licensed under the *Creative Commons 0* license."
- jsonl line 1 (schema v3, abridged to the fields of interest): `{"created_at": "2021-02-09T07:53:10.072659+00:00", "data": [{"benchmark_launcher": {… "label": "2.0.4"}, … "blender_version": {… "version": "2.91.2"}, "device_info": {"compute_devices": [{"name": "AMD Ryzen 3 3100 4-Core Processor", "type": "CPU"}, …], "device_type": "CPU", "num_cpu_threads": 8}, "scene": {… "label": "bmw27"}, "stats": {"device_peak_memory": 144.22, "render_time_no_sync": 384.355, "total_render_time": 384.782}, "system_info": {"bitness": "64bit", … "machine": "AMD64", "num_cpu_cores": 4, "num_cpu_sockets": 1, "num_cpu_threads": 8, "system": "Windows"}, "timestamp": "2021-02-09T07:50:04.046554+00:00"}], "id": "8b78e6e0-c83e-4f40-9282-455bb6d29652", "schema_version": "v3"}`
- jsonl line 30144 (schema v4, id `8db6435a-1ddb-4e19-8548-13e62dbbbb87`, abridged): `{"benchmark_launcher": {… "label": "3.0.0"}, "benchmark_script": {… "label": "3.0.0"}, "blender_version": {… "version": "3.0.1"}, "device_info": {"compute_devices": [{"name": "Intel Core i7-4770 CPU @ 3.40GHz", "type": "CPU"}], "device_type": "CPU", "num_cpu_threads": 8}, "scene": {… "label": "monster"}, "stats": {"device_peak_memory": 709.66, "number_of_samples": 19, "render_time_no_sync": 30.6933, "samples_per_minute": 37.14213431410289, "time_for_samples": 30.692905, "time_limit": 30, "total_render_time": 33.5701}, "system_info": {"bitness": "64bit", … "dist_name": "Ubuntu", "dist_version": "21.10", "machine": "x86_64", "num_cpu_cores": 4, "num_cpu_sockets": 1, "num_cpu_threads": 8, "system": "Linux"}, "timestamp": "2022-03-01T14:30:33.749979+00:00"}`

**Reader's own computation** (python streaming the jsonl; `sources/S3-06/parse-summary.txt`): 429 723 lines, 1 287 633 scene entries, 651 553 with `device_type == "CPU"`; schema versions v1 11 043 / v2 1 / v3 76 804 / v4 341 875 lines; CPU entries by `num_cpu_threads`: 16 → 155 942, 32 → 111 519, 12 → 105 852, 24 → 81 622, 8 → 68 514, 20 → 42 398, 4 → 25 438, …; CPU entries by `system`: Windows 510 945, Linux 91 088, Darwin 49 520; `render_time_no_sync` over Linux CPU entries (n = 89 640): min 15.15 s, p10 30.19, p50 31.37, p90 157.38, max 239 259 s. The v4 records carry `time_limit: 30` and `samples_per_minute`, i.e. the newer launcher renders for a fixed time budget, so `render_time_no_sync` clusters near 30 s in v4 and is a full-scene render time in v1–v3 (the reader's reading of the fields; the dataset carries no documentation of them beyond the README).

**Coverage.**
- T7 — covers: object = one Blender Cycles CPU render per scene per submission, unit = seconds (`render_time_no_sync`, `total_render_time`, `time_for_samples`) and `samples_per_minute`, plus `num_cpu_threads`/`num_cpu_cores`/`num_cpu_sockets` of the machine and `device_type`; statistic = one value per submission (distribution computable); scope = user-submitted Blender Benchmark runs 2021–2026; population = 651 553 CPU scene entries (91 088 on Linux). It does not record CPU utilisation, the renderer's thread count as chosen (only the machine's thread count), or the process structure.
- T1, T2, T4, T5, T6 — does not cover.

**One observation?** No — a population of user submissions; machine per record (CPU model, threads), subject = named scenes (`classroom`, `junkshop`, `monster`, `bmw27`, …), window = per-record timestamp.

### S3-07 — Phoronix, "Building The Default x86_64 Linux Kernel In Just 16 Seconds" (14 Aug 2019) + PTS `build-linux-kernel` 1.16.0 profile

**Citation.** Michael Larabel, "Building The Default x86_64 Linux Kernel In Just 16 Seconds", Phoronix, 14 August 2019, https://www.phoronix.com/news/Linux-16-Seconds-AMD-EPYC-2P ; Phoronix Test Suite test profile `pts/build-linux-kernel-1.16.0`, files `install.sh` and `test-definition.xml`, https://raw.githubusercontent.com/phoronix-test-suite/test-profiles/master/pts/build-linux-kernel-1.16.0/ (branch `master` as of 2026-09-16; commit not identified because the GitHub API is unavailable in this session).

**Copies read (2026-09-16).** `sources/S3-07/phoronix-16s.html` HTTP 200, 82 032 B, SHA-256 `f93666a907a25938a3e5c0d24008b0993968b357e32e01879d45edbc9992818a`; `sources/S3-07/install-1.16.0.sh` HTTP 200, 151 B, SHA-256 `735dcb5ea399ccc18b65981ca6e60165e1f1bc79caabf29802051054874485dd`; `sources/S3-07/test-definition-1.16.0.xml` HTTP 200, 1 807 B, SHA-256 `791b68cc7162446c00d10c63e7846847b2b2debab3db1b18b994159e03290ae9`.

**Verbatim passages.**
- Article (text-stripped): "It used to be that building out the Linux kernel could easily take the time needed to enjoy a beverage or have a meal while now with the EPYC 7742 2P it's easy to build the Linux kernel in just 15~16 seconds! Up until the Rome testing I was never able to crack 20 seconds with any of the hardware at my disposal while now it's easy hitting 15 seconds. That is with a Linux x86_64 default "defconfig"" … "That's with each server tested using an Intel Optane 900p 280GB NVMe SSD and maximum channels/frequency supported RAM and running Ubuntu 19.04 with the stock compiler. … as I/O appears to be the bottleneck at this point." … "If pulling up statistics from OpenBenchmarking.org with that same exact test profile version for building the kernel in the same manner and the same Linux 4.18 LTS sources, of 2,687 public sample results the average kernel build time is 125 seconds."
- `install.sh:1–6`: "#!/bin/sh / echo "#!/bin/sh / cd linux-6.8 / make -s -j \$NUM_CPU_CORES 2>&1 / echo \$? > ~/test-exit-status" > build-linux-kernel / chmod +x build-linux-kernel"
- `test-definition.xml:5–7,11,14,34–40`: "<Title>Timed Linux Kernel Compilation</Title>" / "<AppVersion>6.8</AppVersion>" / "This test times how long it takes to build the Linux kernel in a default configuration (defconfig) for the architecture being tested or alternatively an allmodconfig for building all possible kernel modules for the build." / "<TimesToRun>3</TimesToRun>" / "<Version>1.16.0</Version>" / options "defconfig" and "allmodconfig".

**Coverage.** T6 — covers: the workload definition of the most-cited public kernel-compile benchmark (Linux 6.8, `defconfig` or `allmodconfig`, `make -s -j $NUM_CPU_CORES`, i.e. `-j` = core count, three runs) and one whole-build wall time (15–16 s, EPYC 7742 2P, defconfig, Linux 4.18 sources at the time) plus a population statistic reported by the article ("2,687 public sample results", average 125 s) whose underlying results are on openbenchmarking.org (403 to this reader). No process counts or CPU totals. T4 — covers marginally: the benchmark's `-j` rule (`$NUM_CPU_CORES`). T1, T2, T5, T7 — does not cover.

**One observation?** The article's 15–16 s is one machine (EPYC 7742 2P, Ubuntu 19.04, Optane 900p); `-j` implied by the profile (`$NUM_CPU_CORES`); window not stated beyond the profile's 3 runs. The 125 s average is a population figure quoted second-hand.

### S3-08 — LKML, January 1999: two posts with `make -j` kernel-compile timings

**Citation.** (a) Balázs Szabó, "Kernel make -j timings with and without Arcangeli patches", linux-kernel, Mon 11 Jan 1999, https://lkml.iu.edu/hypermail/linux/kernel/9901.1/1259.html ; (b) Robert B. Hamilton, "pre[456] Kernel Compiles(x)make -j[44567]", linux-kernel, Tue 12 Jan 1999, https://lkml.iu.edu/hypermail/linux/kernel/9901.1/1406.html .

**Copies read (2026-09-16, HTTP 200).** `sources/S3-08/lkml-9901.1-1259.html` 2 946 B, SHA-256 `aa6d8c0ad42dc0a5d57bd82ce17474dac157fa84aeb320e276571c1161a6f9a8`; `sources/S3-08/lkml-9901.1-1406.html` 3 392 B, SHA-256 `284cad522b7d78b38f4beb4d4df234cb286c033d5bd5cd02f0db060afd5a0edb`.

**Verbatim passages.**
- (a): "Today I compiled some kernels and tests these kernels on compiling kernel with make -j." / "Comfiguration: P166, 92M RAM, 428M swap" / "Compiled kernel: 2.2.0-pre5" / "2.0.35 (with QNX scheduler patch): 1032.34s user 119.88s system 82% cpu 23:12.85 total" / "2.1.131 (wo arca-44 patch): 920.75s user 265.35s system 32% cpu 1:00:45.70 total" / "2.2.0-pre5: 855.83s user 112.39s system 88% cpu 18:17.14 total" / "2.2.1-pre6: 865.68s user 139.36s system 90% cpu 18:25.27 total".
- (b): "For each, in sequence the commands / make clean / time make -jn zImage / are applied for successive values of n=4,4,5,6, and 7." / "my idea is to simulate this with the first compile, in order to "precondition" the cache/buffers." / "Reported are total elapsed time (minute:sec) for each compile. Processor is K6-266 with 32MB memory, 512k cache memory." / "Kernel | j4(1) j4 j5 j6 j7" / "220-6 | 4:53 4:40 4:53 5:15 5:54" / "220-5 | 4:50 4:39 4:55 5:00 6:16" / "220-4 | 4:59 4:45 4:57 5:34 5:52" / "2.1.131| 4:49 4:45 5:20 6:25 8:02".

**Coverage.** T6 — covers, historically: (a) whole-build user/system/CPU-percent/wall for an unbounded `make -j` of kernel 2.2.0-pre5 on a single-CPU P166 across host kernels (one machine, one project; the "% cpu" figure is the shell `time` summary, showing 32–90 % of one CPU); (b) wall time vs `-j4…7` on a single-CPU K6-266 with 32 MB, first run cold ("j4(1)") vs warm — a single-core observation of `-jN` with N above the core count, wall time only, and a warm-vs-cold pair. T2 — covers marginally (cold vs preconditioned cache at whole-build level only). T4 — covers marginally (one user's habitual `make -j` choices in 1999). T1, T5, T7 — does not cover.

**One observation?** Each post is one machine (named: P166/92 MB; K6-266/32 MB), one project (kernel 2.2.0-pre5; `zImage` of 2.2.0-pre4…6 and 2.1.131), `-j` stated, windows are the whole builds; 1999-era hardware and kernels.

### S3-09 — Yocto buildstats: one `do_compile` record from a public build tree, plus the Yocto wiki description

**Citation.** (a) File `build/tmp/buildstats/20190213084550/quilt-native-0.65-r0/do_compile` in GitHub repository `liyapenggo/raspberrypi3-openbmc`, branch `master` (raw at https://raw.githubusercontent.com/liyapenggo/raspberrypi3-openbmc/master/build/tmp/buildstats/20190213084550/quilt-native-0.65-r0/do_compile; commit not identifiable this session). (b) Yocto Project wiki, "TipsAndTricks/InvestigatingBuildTime", https://wiki.yoctoproject.org/wiki/TipsAndTricks/InvestigatingBuildTime .

**Copies read (2026-09-16, HTTP 200).** `sources/S3-09/openbmc-quilt-native-do_compile` 811 B, SHA-256 `4aae89ff1746baae5f5f195785a373086eba2f51becc03745122dbe3c70a0aa1`; `sources/S3-09/yocto-investigating-build-time.html` 16 055 B, SHA-256 `3003d7e92a69cd32cee1a519e8097179c33a835e8e41a661ca053a2c541b207f`; also fetched and found not useful: `yocto-ref-classes.html` (366 530 B, SHA-256 `514fb6c8b6dcb6683b9531f9a1837c22c4d34d0b450d7c71ca571cba9f87c9c2`, no example record), `embeddedguruji-buildstats.html` (134 540 B, SHA-256 `7af5596af98f6235755d1e4eb33dc6d1dccfc259761c5c6ba50e7a8e71106a71`, no per-task record).

**Verbatim passages.**
- (a) whole file: "Event: TaskStarted / Started: 1550047567.51 / quilt-native-0.65-r0: do_compile / Elapsed time: 0.52 seconds / utime: 6 / stime: 1 / cutime: 49 / cstime: 12 / IO cancelled_write_bytes: 0 / IO syscw: 1429 / IO write_bytes: 364544 / IO syscr: 5393 / IO wchar: 730269 / IO rchar: 3672744 / IO read_bytes: 573440 / rusage ru_utime: 0.06824999999999999 / rusage ru_stime: 0.018958 / rusage ru_maxrss: 104288 / rusage ru_minflt: 5564 / rusage ru_majflt: 0 / rusage ru_inblock: 0 / rusage ru_oublock: 40 / rusage ru_nvcsw: 42 / rusage ru_nivcsw: 1 / Child rusage ru_utime: 0.491017 / Child rusage ru_stime: 0.12116099999999999 / Child rusage ru_maxrss: 101660 / Child rusage ru_minflt: 82162 / Child rusage ru_majflt: 1 / Child rusage ru_inblock: 1120 / Child rusage ru_oublock: 672 / Child rusage ru_nvcsw: 1035 / Child rusage ru_nivcsw: 259 / Status: PASSED / Ended: 1550047568.02".
- (b) wiki (text-stripped): "The buildstats data produced by the class with the same name provides process statistics for every recipe task." / "buildstats.bbclass stores mainly two set of process' stats: time and IO stats. For the moment, we are currently focusing on the following time data: /proc/[pid]/stat: utime, stime / /proc/[pid]/stat: cutime, cstime / python resource module: rusage ru_utime, rusage ru_stime / python resource module: Child rusage ru_utime, Child rusage ru_stime / and the IO stats: /proc/[pid]/io: IO rchar, IO wchar / /proc/[pid]/io: IO read_bytes, IO write_bytes".

**Coverage.** T2/T6 — covers the *format* and one tiny instance: per-task (a whole `do_compile`, i.e. a whole `make` of one recipe, not a compiler process) wall time, utime/stime of the task shell and cumulative children, `/proc/pid/io` bytes and syscall counts, rusage including `ru_inblock` (blocks read from disk), `ru_majflt`, voluntary/involuntary context switches. The one record is `quilt-native` (0.52 s, children 0.49 s user, `ru_inblock 1120`, `ru_nvcsw 1035`, `ru_nivcsw 259`); `PARALLEL_MAKE` is not in the record; machine not identified. The search found no public buildstats tree for a large recipe (kernel/LLVM) this session; the Yocto autobuilder publishes no buildstats directory at the URLs tried (404). T1, T4, T5, T7 — does not cover.

**One observation?** Yes, one task of one build (2019-02-13 by the repo's timestamp), machine and `PARALLEL_MAKE` unnamed.

### S3-10 — DKMS `make.log` files attached to Ubuntu Launchpad bugs (1871162, 1663876, 1689390, 1578455)

**Citation.** Launchpad bug attachments: bug 1871162 "dkms error kernel 5.6.2" — `make.log` (attachment 5347872) and `ProcCpuinfoMinimal.txt` (5347874); bug 1663876 "[zesty] dkms nvidia error with linux-headers-4.10.0-7" — `make.log` (4816967); bug 1689390 "Kernel 4.11 update" — `make.log` (4873695); bug 1578455 "bcmwl-kernel-source … bcmwl kernel module …" — `DKMSBuildLog.txt` (4656064). Found through https://api.launchpad.net/1.0/ubuntu/+source/dkms?ws.op=searchTasks&search_text=make.log (15 tasks).

**Copies read (2026-09-16, all HTTP 200, `https://api.launchpad.net/1.0/bugs/<bug>/+attachment/<id>/data`).** `sources/S3-10/lp-1871162-make.log` 1 532 B SHA-256 `53c6644f424394251ddb98eb4fee81c9b54d6ef256ed6ab676ec091c010d403b`; `lp-1871162-ProcCpuinfoMinimal.txt` 1 303 B SHA-256 `8ba014b522d7dd863df5467db75126e9ef9c0cac1268ce52540fc0ed7ba6d7ef`; `lp-1663876-make.log` 7 416 B SHA-256 `25fdd2f2a18bde258a3739ef2767a07d7ac76515be1e3de96c883928bef5259b`; `lp-1689390-make.log` 93 928 B SHA-256 `8d7547d8b49e7299e088794bdaf170df4db3d762bb140e7e84130da2b57370d0`; `lp-1578455-DKMSBuildLog.txt` 1 150 B SHA-256 `e17d75172dd1f5289aaf0c5e24b314adac84eed84893f8353ff09dced04443c3`; plus `lp-dkms-search.json`, `lp-<bug>-attachments.json`, and bug 2089335's page/attachment list (no make.log there).

**Verbatim passages.**
- `lp-1871162-make.log:1–5`: "DKMS make.log for acpi-call-1.1.0 for kernel 5.6.2-050602-generic (x86_64)" / "Mon 06 Apr 2020 12:09:04 PM EDT" / "make: Entering directory '/usr/src/linux-headers-5.6.2-050602-generic'" / "  AR      /var/lib/dkms/acpi-call/1.1.0/build/built-in.a" / "  CC [M]  /var/lib/dkms/acpi-call/1.1.0/build/acpi_call.o"; `:16–19`: "cc1: some warnings being treated as errors" / "make[1]: *** [scripts/Makefile.build:268: /var/lib/dkms/acpi-call/1.1.0/build/acpi_call.o] Error 1" / "make: *** [Makefile:1683: /var/lib/dkms/acpi-call/1.1.0/build] Error 2" / "make: Leaving directory '/usr/src/linux-headers-5.6.2-050602-generic'". `ProcCpuinfoMinimal.txt`: "processor	: 11" / "model name	: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz" / "siblings	: 12".
- `lp-1663876-make.log:1–3`: "DKMS make.log for nvidia-378-378.09 for kernel 4.10.0-7-generic (x86_64)" / "samedi 11 février 2017, 11:36:02 (UTC+0100)" / "make "CC=cc"  KBUILD_VERBOSE= -C /lib/modules/4.10.0-7-generic/build M=/var/lib/dkms/nvidia-378/378.09/build ARCH=x86_64 NV_KERNEL_SOURCES=/lib/modules/4.10.0-7-generic/build NV_KERNEL_OUTPUT=/lib/modules/4.10.0-7-generic/build NV_KERNEL_MODULES="nvidia nvidia-uvm nvidia-modeset nvidia-drm" INSTALL_MOD_DIR=kernel/drivers/video modules"; `:115–122`: "  CC [M]  /var/lib/dkms/nvidia-378/378.09/build/nvidia/nv-frontend.o" … "  CC [M]  /var/lib/dkms/nvidia-378/378.09/build/nvidia/nv-dma.o" (reader's count: 15 `CC [M]` lines before the failure).
- `lp-1689390-make.log:1–3`: "DKMS make.log for nvidia-304-304.135 for kernel 4.11.0-041100-generic (x86_64)" / "lun may  8 22:08:43 CEST 2017" / "NVIDIA: calling KBUILD..."; last lines: "nvidia.ko failed to build!" / "make: *** [module] Error 2".
- `lp-1578455-DKMSBuildLog.txt:1–3`: "DKMS make.log for bcmwl-6.30.223.248+bdcom for kernel 4.4.0-21-generic (x86_64)" / "Thu May  5 06:57:03 IST 2016" / "make: Entering directory '/usr/src/linux-headers-4.4.0-21-generic'".

**Coverage.** T5 — covers, partially: the shape of a DKMS module build as recorded by DKMS's own `make.log` — header naming module and kernel, the `make … -C /lib/modules/<kver>/build M=<dir> … modules` command as the module's own Makefile issues it (nvidia-378 case), and the kbuild `CC [M]`/`AR`/`LD` lines; **no `-j` appears in any of the four logs, and no elapsed time, CPU time or process count** (these logs come from failed builds attached to bug reports; the reporter's machine is known only for 1871162: i7-9750H, 12 threads). T1 — covers marginally (per-object `CC [M]` lines for one small module: 1 object for acpi-call, 15 objects before failure for nvidia-378). T2, T4, T6, T7 — does not cover.

**One observation?** Each log is one failed build on one user machine (mostly unnamed), module and kernel named, `-j` not stated, no timing.

### S3-11 — ananicy rule sets: CachyOS `ananicy-rules` type definitions and the original Ananicy README

**Citation.** (a) CachyOS, `ananicy-rules` repository, files `00-types.types`, `00-cgroups.cgroups`, `README.md`, branch `master` (https://raw.githubusercontent.com/CachyOS/ananicy-rules/master/…; commit not identifiable this session), and the directory listing of `00-default/Development & Programming` (read through WebFetch of https://github.com/CachyOS/ananicy-rules/tree/master/00-default/Development%20%26%20Programming). (b) nefelim4ag, `Ananicy` repository `README.md`, branch `master` (https://raw.githubusercontent.com/nefelim4ag/Ananicy/master/README.md).

**Copies read (2026-09-16, HTTP 200).** `sources/S3-11/cachyos-00-types.types` 1 734 B SHA-256 `667d89cb61a949ac9b6595f2f318dc452b65c735d8cd6d4fcd5f934dc940591d`; `cachyos-00-cgroups.cgroups` 298 B SHA-256 `ab78e8b36d6c7c5f1e347df552edfb2d7073e41ef8e0a1f484ff93afb994e67a`; `cachyos-README.md` 4 245 B SHA-256 `0886ec1f23a1ef772e676ba65bc13961ce7942bec6e0dc9d0936a4f60b16b7ed`; `nefelim4ag-README.md` 4 884 B SHA-256 `7879441e10863035f42421925356910a9bbcc3040fc76346abb349e3bdc6b8d2`. (Two codeload tarballs saved as 378-byte 403 bodies, SHA-256 `b3e03aaaff81d68730d67392a135ac3fdfdf022880c66632ab188d2fe084cda3`, are error pages, not sources.)

**Verbatim passages.**
- `cachyos-00-types.types`: "# Type: BackGround CPU/IO Load / # Background CPU/IO it's needed, but it must be as silent as possible / { "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }" / "# Type: Background CPU but demands more I/O, One example: File Synchronization / { "type": "BG_CPU", "nice": 14, "ioclass": "best-effort", "sched": "idle" }" / "# Type: Heavy CPU Load / # It must work fast enough but must not create so much noise / { "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }" / "{ "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }" / "{ "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }" / "{ "type": "Service", "nice": 10, "ioclass": "best-effort", "ionice": 6 }".
- `cachyos-00-cgroups.cgroups`: "# cpuquota same as systemd CPUQuota, / # only difference is - meaning of N% is all CPUs, not one core. / { "cgroup": "cpu90", "CPUQuota": 90 } / { "cgroup": "cpu85", "CPUQuota": 85 } / { "cgroup": "cpu80", "CPUQuota": 80 }".
- CachyOS `00-default/Development & Programming` listing (WebFetch, 17 files): "android-studio.rules, bruno.rules, bun.rules, clang-tidy.rules, clangd.rules, cmake.rules, dart_flutter.rules, deno.rules, gitkraken.rules, gnur.rules, mongodb_compass.rules, mysql-workbench.rules, nix.rules, node.rules, rstudio.rules, sqlitebrowser.rules, unity.rules" — no `gcc`, `cc1`, `clang`, `make` or `ld` rule file is listed there; the reader did not find a compiler rule elsewhere in the tree (only this folder and the root were listed).
- `nefelim4ag-README.md:25`: "* Why do I get lag, while compiling kernel and playing games?"; `:64–68`: "Rules files should be placed under `/etc/ananicy.d/` directory and have `*.rules` extension. … General syntax is described below: / { "name": "gcc", "type": "Heavy_CPU", "nice": 19, "ioclass": "best-effort", "ionice": 7, "cgroup": "cpu90" }"; `:101`: "5. For CPU hungry backround task like compiling, just use `NICE=19`."; `:103–104`: "About IO priority: / 1. It's useful to use `{"ioclass": "idle"}` for IO hungry background tasks like: file indexers, Cloud Clients, Backups and etc."

**Coverage.** T7 — covers the "shipped process-treatment catalogue" half: the type classes a rule set ships (`Heavy_CPU` nice 9, `BG_CPUIO` nice 16 + `SCHED_IDLE` + idle I/O, `BG_CPU`, `Game` nice −5, …) and cgroup CPU quotas (80/85/90 % of all CPUs); the original project's README uses `gcc` as its syntax example with `"type": "Heavy_CPU", "nice": 19` and advises nice 19 for compiling and `ioclass idle` for indexers. Whether the CachyOS shipped set actually assigns compilers a class could not be established (no gcc/clang rule file found in the folders listed). T1, T2, T4, T5, T6 — does not cover.

**One observation?** Not an observation; a shipped configuration (versions: `master` on 2026-09-16, commits unidentified).

### S3-13 — Microsoft Q&A 5550992, "Clamscan is taking 11-12hrs to complete" (ClamAV scan summaries)

**Citation.** Microsoft Q&A question 5550992, "Clamscan is taking 11-12hrs to complete", https://learn.microsoft.com/en-us/answers/questions/5550992/clamscan-is-taking-11-12hrs-to-complete (Azure RHEL VMs; question with clamscan SCAN SUMMARY output and an answer).

**Copy read (2026-09-16).** `sources/S3-13/msqa-clamscan.html` HTTP 200, 98 070 B, SHA-256 `d685b88f10b919d4ab787b4bc0f2fd3bf8b5ce1eea0cb6e49c8d13b559118fcd`. Locators are lines of the text-stripped copy.

**Verbatim passages.**
- line 173: "I have two boxes both running clamscan virus software. On the box running RHEL 8.4, Clam runs in ~2hrs. On the box running RHEL 8.10, Clam is taking 11-12hrs and using A LOT of CPU. The boxes are very similar except for the OS."
- line 175: "7 4 * * * clamscan --exclude-dir="^/sys/|^/var/lib/clamav/|^/var/lib/clamav-unofficial-sigs/" -i -r / |tee /u/pick/last.clamscan|logger -t clamav -p security.alert"
- lines 180–183, 186–188 (box 1): "Aug  5 05:00:26 AZR-DEV-PICKD3 clamav[39091]: Scanned directories: 17,175" / "Scanned files: 70,593" / "Data scanned: 7,222.68 MB" / "Known viruses: 8,885,612" / "Start Date: 2025:08:05 04:07:01" / "End Date:   2025:08:05 05:00:26".
- lines 189–197 (box 2): "Sep  8 17:19:50 AZR-PRD-PICKD3 clamav[66168]: ----------- SCAN SUMMARY -----------" / "Engine version: 1.0.8" / "Scanned directories: 38,015" / "Scanned files: 195,265" / "Data scanned: 54,019.94 MB" / "Data read: 451,901.67 MB (ratio 0.12:1)" / "Time: 47,569.255 sec (792 m 49 s)".
- answer, lines 520–521, 524: "RHEL 8.4: ~70k files, 21 GB read, ~53 minutes" / "RHEL 8.10: ~195k files, 451 GB read, ~13 hours" / "Use ClamAV Daemon (clamdscan) : Switching from clamscan to clamdscan avoids the repeated database reload and enables parallel scanning."

**Coverage.** T7 — covers: one antivirus batch job's duration (47 569 s = 792 min 49 s for 195 265 files / 451.9 GB read; 53 min for 70 593 files / 7.2 GB scanned), file and byte counts, invocation (`clamscan -i -r /`, a single-process scanner — the answer contrasts it with the daemon's "parallel scanning"), and a qualitative CPU statement ("A LOT of CPU"); no thread count or measured utilisation. Server VMs, not a desktop. T1, T2, T4, T5, T6 — does not cover.

**One observation?** Two runs on two Azure RHEL VMs (hardware unnamed), subject = full-filesystem `clamscan`, windows given by the summaries (2025-08-05 04:07→05:00; 2025-09-08, 47 569 s).

### S3-14 — Two public `.ninja_log` files of LLVM builds (GitHub)

**Citation.** (a) `build/.ninja_log` in repository `leikang123/LLVM-NMX`, branch `master`, https://raw.githubusercontent.com/leikang123/LLVM-NMX/master/build/.ninja_log ; (b) `llvm_build/.ninja_log` in repository `hoholee12/rpcs3-custom`, branch `master`, https://raw.githubusercontent.com/hoholee12/rpcs3-custom/master/llvm_build/.ninja_log . Located by GitHub code search `"lib/IR/CMakeFiles/LLVMCore.dir" filename:.ninja_log` (7 hits). Commits not identifiable this session (GitHub API restricted); branch `master` as fetched on 2026-09-16.

**Copies read (2026-09-16, HTTP 200).** `sources/S3-14/LLVM-NMX-build.ninja_log` 80 301 B, SHA-256 `45cd1c3b1e31f84020aa8a6a3875c325ad7e58e65a435a5f5d83579d870a9b35`; `sources/S3-14/rpcs3-custom-llvm_build.ninja_log` 195 712 B, SHA-256 `5d245b331b088b523b871d6b8240352f14949c13047d0393982174b3bfadb4cf`.

**Verbatim passages.**
- (a) lines 1–2: "# ninja log v5" / "110481	115752	1690268614368356786	lib/Support/CMakeFiles/LLVMSupport.dir/raw_ostream.cpp.o	17c2d7ba31ff0a38".
- (b) lines 1–3: "# ninja log v5" / "39	144	6799304867112142	lib/Support/CMakeFiles/LLVMSupport.dir/ABIBreak.cpp.obj	aa0cf3a30bdda31c" / "145	234	6799304868085969	lib/Support/CMakeFiles/LLVMSupport.dir/AutoConvert.cpp.obj	8266305d5720769f".
- The files carry no header naming the machine, compiler, `-j`, or LLVM revision; (b)'s `.obj` suffix and the columns are what the file shows.

**Reader's own computation** (python over the tab-separated columns start-ms, end-ms, mtime, output, hash; command in the shell history, duration = end − start): (a) 740 edges, 711 ending in `.o`; per-edge duration min 22 ms, p10 2 336, p50 11 345, p90 26 486, max 1 874 951 ms (`lib/CodeGen/…/LatencyPriorityQueue.cpp.o`, 2 968 421→4 843 372); sum of `.o` durations 25 429 s over a span of 5 489 s; maximum simultaneous open edges (sampled at the first 3 000 distinct start times) 11. (b) 1 712 edges (`.obj`), duration min 88 ms, p10 1 270, p50 5 248, p90 11 882, max 1 528 911 ms; span 2 556 s; maximum simultaneous edges 19. The 30-minute outliers in (a) overlap in time (three `lib/CodeGen` objects starting within 10 s and ending within 10 s of each other), which the reader reads as a stall of the whole build rather than compile time; the file cannot distinguish.

**Coverage.** T2 — covers, partially: wall-clock duration per compile edge (one clang/clang-cl invocation per object) across a whole LLVM build, from which a distribution is computable; not CPU time, no blocking breakdown, no cache state, machine and `-j` unknown (the concurrency computed above bounds `-j` from below). T1 — covers marginally: edge counts and overlap, not processes. T4, T5, T6, T7 — does not cover.

**One observation?** Each file is one build on one unnamed machine; subject = LLVM (revision unknown; (b) a Windows `.obj` build inside an rpcs3 tree), `-j` unknown; window = the log's span.

### S3-15 — Greg Kroah-Hartman, "Fast Kernel Builds" (blog, 18 Sep 2020): kcbench on three machines

**Citation.** Greg Kroah-Hartman, "Fast Kernel Builds", 2020-09-18, http://www.kroah.com/log/blog/2020/09/18/fast-kernel-builds/ .

**Copy read (2026-09-16).** `sources/S3-15/kroah-fast-kernel-builds.html` HTTP 200, 42 929 B, SHA-256 `f02820ecb38b10e368eb0bc2d987fcdf3a199186b61167efc9fdbd6e83bb02ea`. Locators are lines of the text-stripped copy.

**Verbatim passages.**
- 111–114: "I've used the tool Fio version fio-3.23-28-g7064, kcbench version v0.9.0 (from git), and perf version 5.7.g3d77e6a8804a."
- 130–141: "Processor:           Intel Core Processor (Broadwell) [40 CPUs] / Cpufreq; Memory:     Unknown; 120757 MiB / Linux running:       5.8.7-200.fc32.x86_64 [x86_64] / Compiler:            gcc (GCC) 10.2.1 20200723 (Red Hat 10.2.1-1) / Linux compiled:      5.7.0 [/home/gregkh/.cache/kcbench/linux-5.7] / Config; Environment: defconfig; CCACHE_DISABLE="1" / Build command:       make vmlinux / Filling caches:      This might take a while... Done / Run 1 (-j 40):       81.92 seconds / 43.95 kernels/hour [P:3033%] / Run 2 (-j 40):       83.38 seconds / 43.18 kernels/hour [P:2980%] / Run 3 (-j 46):       82.11 seconds / 43.84 kernels/hour [P:3064%] / Run 4 (-j 46):       81.43 seconds / 44.21 kernels/hour [P:3098%]"
- 143–158: "Processor:           Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz [8 CPUs] / Cpufreq; Memory:     powersave [intel_pstate]; 15678 MiB / Linux running:       5.8.8-arch1-1 [x86_64] / Compiler:            gcc (GCC) 10.2.0 / Linux compiled:      5.7.0 … / Config; Environment: defconfig; CCACHE_DISABLE="1" / Build command:       make vmlinux / Run 1 (-j 8):        392.69 seconds / 9.17 kernels/hour [P:768%] / Run 2 (-j 8):        393.37 seconds / 9.15 kernels/hour [P:768%] / Run 3 (-j 10):       394.14 seconds / 9.13 kernels/hour [P:767%] / Run 4 (-j 10):       392.94 seconds / 9.16 kernels/hour [P:769%] / Run 5 (-j 4):        441.86 seconds / 8.15 kernels/hour [P:392%] / Run 6 (-j 4):        440.31 seconds / 8.18 kernels/hour [P:392%] / Run 7 (-j 6):        413.48 seconds / 8.71 kernels/hour [P:586%] / Run 8 (-j 6):        412.95 seconds / 8.72 kernels/hour [P:587%]"
- 160–175: "Processor:           AMD Ryzen Threadripper 3970X 32-Core Processor [64 CPUs] / Cpufreq; Memory:     schedutil [acpi-cpufreq]; 257693 MiB / Linux running:       5.8.8-arch1-1 [x86_64] / Compiler:            gcc (GCC) 10.2.0 / … / Run 1 (-j 64):       37.15 seconds / 96.90 kernels/hour [P:4223%] / Run 2 (-j 64):       37.14 seconds / 96.93 kernels/hour [P:4223%] / Run 3 (-j 71):       37.16 seconds / 96.88 kernels/hour [P:4240%] / Run 4 (-j 71):       37.12 seconds / 96.98 kernels/hour [P:4251%] / Run 5 (-j 32):       43.12 seconds / 83.49 kernels/hour [P:2470%] / Run 6 (-j 32):       43.81 seconds / 82.17 kernels/hour [P:2435%] / Run 7 (-j 38):       41.57 seconds / 86.60 kernels/hour [P:2850%] / Run 8 (-j 38):       42.53 seconds / 84.65 kernels/hour [P:2787%]"

**Coverage.** T6 — covers: kernel `defconfig` `make vmlinux` (Linux 5.7.0, gcc 10.2, ccache disabled, caches pre-filled) on three named machines with `-j` = N, N + a few, N/2, N/2 + a few, giving wall time and the `[P:…%]` CPU-utilisation figure that kcbench prints (e.g. 8-CPU laptop: 392.69 s at `[P:768%]` for `-j 8`, 441.86 s at `[P:392%]` for `-j 4`; 64-CPU: 37.15 s at `[P:4223%]` for `-j 64`, 43.12 s at `[P:2470%]` for `-j 32`). The reader notes that P% × seconds gives a CPU total per run (8-CPU laptop: 392.69 × 7.68 ≈ 3 016 CPU-s at `-j 8` vs 441.86 × 3.92 ≈ 1 732 CPU-s at `-j 4`, reader's arithmetic) — the meaning of `P` is not defined on the page and must be taken from the kcbench source (S2's domain). No process counts, no single-core run (`-j 1` absent). T4 — covers marginally: a kernel maintainer's `-j` choices as tested (N, N+~15 %, N/2). T1, T2, T5, T7 — does not cover.

**One observation?** Three machines named with RAM, host kernel, compiler; subject and `-j` named; window = 4–8 runs each; warm caches ("Filling caches").

### S3-16 — kcbench 0.9.0 announcement (LKML, 23 Jun 2020) and the kcbench man page's result tables

**Citation.** Thorsten Leemhuis, "kcbench, the Linux kernel compile benchmark, version 0.9.0 is out", linux-kernel, Tue 23 Jun 2020, mirror https://lkml.rescloud.iu.edu/2006.2/10984.html (lore.kernel.org not tried — 403 in earlier runs; spinics.net 403); kcbench man page source `kcbench.man1.md`, https://gitlab.com/knurd42/kcbench/-/raw/master/kcbench.man1.md (branch `master` on 2026-09-16).

**Copies read (2026-09-16).** `sources/S3-16/rescloud-kcbench-0.9.0.html` HTTP 200, 10 003 B, SHA-256 `34ab78bb6724b46085edce93abd67c7e08273499179a9610aab3d2638f1e40e2`; `sources/S3-16/kcbench.man1.md` HTTP 200, 18 540 B, SHA-256 `395d59a8b707970a0b137c3628b9a6aef38175c96171ec363de3b69b21e56404`; `sources/S3-16/spinics-kcbench-0.9.0.html` is a 403 squid error page (3 127 B, SHA-256 `363a721d1b5a80705b18805bf99bddde4cf1a630775f54abf76dde3f7125e378`), not a source.

**Verbatim passages.**
- Announcement: "It basically downloads a Linux version (which one depends on the compiler used), extracts it, creates a configuration ('defconfig' by default), before it compiles a kernel ('vmlinux') in a temporary directory ('O=/tmp/foo/') while measuring the time it takes to build. It compiles a few kernels that way using different number of jobs (make -j #)." / "> Processor:           Intel(R) Core(TM) i5-3350P CPU @ 3.10GHz [4 CPUs] / > Cpufreq; Memory:     powersave [intel_pstate]; 7895 MiB / > Linux running:       5.6.2-125.vanilla.knurd.1.fc31.x86_64 [x86_64] / > Compiler:            gcc (GCC) 9.3.1 20200317 (Red Hat 9.3.1-1) / > Linux compiled:      4.19.0 … / > Config; Environment: defconfig; CCACHE_DISABLE="1" / > Build command:       make vmlinux / > Run 1 (-j 4):        288.16 seconds / 12.49 kernels/hour [P:384%] / > Run 2 (-j 4):        288.19 seconds / 12.49 kernels/hour [P:384%] / > Run 3 (-j 6):        291.01 seconds / 12.37 kernels/hour [P:384%] / > Run 4 (-j 6):        291.28 seconds / 12.36 kernels/hour [P:385%]" / "It's also a good tool to find the optimal number of jobs for compiling source code, as 'just use all cores' sometimes is not the fastest setting, as a quick test on an AMD Ryzen Threadripper 3990X (64 cores/128 threads) recently showed: … > Run 1 (-j 128):       260.43 seconds / 13.82 kernels/hour / > Run 2 (-j 136):       262.67 seconds / 13.71 kernels/hour / > Run 3 (-j 64):        215.54 seconds / 16.70 kernels/hour / > Run 4 (-j 72):        215.97 seconds / 16.67 kernels/hour" (that run: "kcbench -s 5.3 -n 1 -m", i.e. allmodconfig). / "the man-page for kcbenchrate (which is new with 0.9.0 …), which by default compiles one kernel on each CPU using one job to measure the rate and keep the all cores busy all the time".
- `kcbench.man1.md:210–226`: "ON THE DEFAULT NUMBER OF JOBS / The optimal number of compile jobs (-j) to get the best result depends on the machine being benched. On most systems you will achieve the best result if the number of jobs matches the number of CPU cores. That for example is the case on this 4 core Intel processor without SMT: / … Processor:            Intel(R) Core(TM) i5-4570 CPU @ 3.20GHz [4 threads] / … Linux compiled:       5.3.0 … / Config; Environment:  defconfig; CCACHE_DISABLE="1" / Build command:        make vmlinux / Run 1 (-j 4):         250.03 seconds / 14.40 kernels/hour / Run 2 (-j 6):         255.88 seconds / 14.07 kernels/hour"; `:235–245`: "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz [12 threads] … Run 1 (-j 12):        92.55 seconds / 38.90 kernels/hour / Run 2 (-j 15):        91.91 seconds / 39.17 kernels/hour / Run 3 (-j 6):         113.66 seconds / 31.67 kernels/hour / Run 4 (-j 9):         101.32 seconds / 35.53 kernels/hour"; `:254–264`: "AMD Ryzen Threadripper 3990X 64-Core Processor [128 threads] … Run 1 (-j 128):       26.16 seconds / 137.61 kernels/hour / Run 2 (-j 136):       26.19 seconds / 137.46 kernels/hour / Run 3 (-j 64):        21.45 seconds / 167.83 kernels/hour / Run 4 (-j 72):        22.68 seconds / 158.73 kernels/hour"; `:288–298`: "AMD EPYC 7742 64-Core Processor [256 threads] … Run 1 (-j 256):       128.24 seconds / 28.07 kernels/hour / Run 2 (-j 268):       128.87 seconds / 27.94 kernels/hour / Run 3 (-j 128):       141.83 seconds / 25.38 kernels/hour / Run 4 (-j 140):       137.46 seconds / 26.19 kernels/hour"; `:423`: "Run 1 (-j 4): 230.30 sec / 15.63 kernels/hour [P:389%, 24 maj. pagefaults]".

**Coverage.** T6 — covers: the kernel-compile benchmark most used by kernel developers for machine comparison (defconfig `make vmlinux`, Linux 5.3/4.19/5.7 sources, `-j` ∈ {N, N+~6 %, N/2, N/2+…}) with wall time and `[P:…%]` per run on five named CPUs, and the observation that `-j` = thread count is not fastest on SMT-heavy machines (3990X: `-j 64` beats `-j 128`); no `-j 1` table and no process counts. T4 — covers: the benchmark author's documented rule ("On most systems you will achieve the best result if the number of jobs matches the number of CPU cores") with the data behind it. T1, T2, T5, T7 — does not cover.

**One observation?** Several one-machine runs, machines named; subject and `-j` named; windows = the runs.

### S3-17 — Nick Desaulniers, "Speeding Up Linux Kernel Builds With ccache" (blog, 2 Jun 2018)

**Citation.** Nick Desaulniers, "Speeding Up Linux Kernel Builds With ccache", 2018-06-02, https://nickdesaulniers.github.io/blog/2018/06/02/speeding-up-linux-kernel-builds-with-ccache/ .

**Copy read (2026-09-16).** `sources/S3-17/desaulniers-ccache.html` HTTP 200, 19 494 B, SHA-256 `95d5738e1703fcfd1d1178499b3a34fff14833fcc2250f42991b2b3c295b6629`. Locators are lines of the text-stripped copy.

**Verbatim passages.** 25–28: "No Cache      $ make clean / $  time  make -j4 / ... / make -j4  2008.93s user 231.69s system 346% cpu 10:47.07 total"; 29, 45–47, 54: "Cold Cache      $ ccache -Cz" / "$  time   KBUILD_BUILD_TIMESTAMP  =  ''  make  CC  =  "ccache gcc"  -j4" / "KBUILD_BUILD_TIMESTAMP  =  ''  make  CC  =  "ccache gcc"  -j4  2426.79s user 312.08s system 372% cpu 12:15.22 total" / "cache miss                           3242"; 62, 65–67: "Hot Cache      $ ccache -z" / "$  time   KBUILD_BUILD_TIMESTAMP  =  ''  make  CC  =  "ccache gcc"  -j4" / "KBUILD_BUILD_TIMESTAMP  =  ''  make  CC  =  "ccache gcc"  -j4  151.85s user 132.98s system 288% cpu 1:38.90 total". The page names no machine and no kernel configuration.

**Coverage.** T6 — covers marginally: a whole kernel build at `-j4` with user/system/CPU % totals (2 008.93 s user + 231.69 s system at 346 % over 10:47) and the "3242" ccache misses, which the reader reads as the number of compiler invocations that reached the compiler in that build (a count of cache-miss compilations, not of processes). T2 — covers marginally: the hot-ccache run (compiler replaced by cache hits) still costs 151.85 s user + 132.98 s system at 288 % — a bound on the non-compiler part (make, shells, preprocessing by ccache) of that build; not page-cache cold/warm. T1, T4, T5, T7 — does not cover (the `-j4` is not explained).

**One observation?** One unnamed machine, unnamed kernel config, `-j4`, three runs.

### S3-18 — Ubuntu Launchpad bug 2025523, "tracker3 taking 100% CPU for a long time"

**Citation.** Launchpad bug #2025523, tracker-miners (Ubuntu), "tracker3 taking 100% CPU for a long time", https://bugs.launchpad.net/bugs/2025523 .

**Copy read (2026-09-16).** `sources/S3-18/lp-2025523.html` HTTP 200, 74 570 B, SHA-256 `b9a97f05db7655c837bb6861b175c8212fd504be7faaab899860fed1c9fbfefb`. (gitlab.gnome.org/GNOME/localsearch/-/issues/228, the upstream report of "100% CPU activity for hours", returned HTTP 406 to curl with a browser UA and is not a source here.)

**Verbatim passages** (text-stripped): "/usr/libexec/tracker-extract-3 and /usr/libexec/tracker-miner-fs-3 are constantly taking 100% CPU, causing the machine to overheat and the fans to work overtime. The problem is that on the next boot, tracker3 restarts and again takes 100% of CPU. EDIT: running "tracker3 status" claims "Estimated less than one second left", but it nevertheless runs continuously." / "Description:	Ubuntu 22.04.2 LTS" / "ProcVersionSignature: Ubuntu 5.19.0-46.47~22.04.1-generic 5.19.17".

**Coverage.** T7 — covers marginally: a desktop indexer reported at "100% CPU" (one core's worth, as the reporter phrases it; no measurement, no duration beyond "a long time", no file count) on Ubuntu 22.04. T1, T2, T4, T5, T6 — does not cover.

**One observation?** One user report, machine not described, no window.

### S3-19 — LKML, Feb 2006: "make -j with j <= 4 seems to only load a single CPU core"

**Citation.** Jesper Juhl, "make -j with j <= 4 seems to only load a single CPU core", linux-kernel, Tue Feb 21 2006, https://lkml.iu.edu/hypermail/linux/kernel/0602.2/1805.html (replies at …/1830, /1842, /2634 not read).

**Copy read (2026-09-16).** `sources/S3-19/lkml-0602.2-1805.html` HTTP 200, 5 764 B, SHA-256 `b1fd15a16709b80bf367f6ba92c3df2d0196e0279989a8796e5f79c583f04df4`.

**Verbatim passages.** "I'm running SMP 2.6.x kernels on a Athlon 64 X2 4400+ / When I build new kernels I use 'make -j' to get both CPU cores busy and minimize build time. / I've observed that when I use 'make -j 2', 'make -j 3' or 'make -j 4' only ~half of my CPU resources get used during the build and when I look at the output it looks exactely like output from plain 'make' for something like 95% of the build - that is, files get build sequentially, not in parallel. / However, if I run 'make -j 5' or higher, then both cores get lots of work to do and utilization of both cores stay close to 100% for almost the entire build" / "Another datapoint: This is most pronounced when I am also running the make process nice'd." / "This is what I usually run to load both cores well : / nice make -j 5 2>&1 | tee build.log".

**Coverage.** T6 — covers marginally: an eyeballed observation (no numbers beyond "~half" and "close to 100%") that a 2.6-era kernel build on two cores did not fill both cores for `-j` ≤ 4 and did for `-j` ≥ 5, worse when niced — i.e. concurrency of live compiler processes below `-j`; the cause is not established in this post. T4 — covers marginally: one developer's habitual choice (`nice make -j 5` on 2 cores). T1, T2, T5, T7 — does not cover.

**One observation?** One machine (Athlon 64 X2 4400+), kernel 2.6.x builds, `-j 2…5+`, no window, no measurement.


## 3. Not found

- **T1 — per-process lifetime or CPU-time distributions of a kernel build.** No public trace, accounting dump or dataset gives per-process (cc1/as/ld/sh/make/fixdep) lifetimes or CPU times for a whole build. The only scheduler-level capture found is S3-01/S3-02 (1 s window, per-comm on-CPU totals and per-slice run/wait, no lifetimes). Established by: search rows 1, 2, 17 (process-accounting datasets: none), 21 (other `perf sched`/`trace-cmd` captures of a build: none), 24–25 (GitHub code searches). Build logs (S3-03, S3-05, S3-10) give command counts only.
- **T2 — blocking on file I/O inside a compiler process, warm vs cold page cache; run/wait/run structure.** Nothing found that measures a compiler process's blocked time or I/O wait. The nearest are S3-01 (per-slice wait time for `cc1`, undifferentiated), S3-09 (Yocto `ru_inblock`/`ru_nvcsw` at whole-task level, one tiny task), S3-08(b) (cold vs preconditioned whole-build wall time, 1999), S3-17 (ccache, not page cache). Established by rows 21, 30 (cold-vs-warm page-cache build measurements: none beyond ccache posts), 6 (LLVM tracker: `task-clock`/`wall-time` per file, no blocking column; the pages read do not describe the machine).
- **T4 — observations of what users actually pick.** No poll or survey with data reachable: Gentoo forums login-walled (row 18, S3-12 withdrawn), Reddit/Arch surveys not found (row 32). What was found are single observed values: Debian buildd `parallel=6` (S3-03), Koji `-j64` on 64 threads (S3-05), PTS `-j $NUM_CPU_CORES` (S3-07), kcbench's rule and tables (S3-16), Greg KH's runs (S3-15), one 1999 and one 2006 developer (S3-08, S3-19).
- **T5 — DKMS run duration, CPU, parallelism.** Four DKMS `make.log`s (S3-10) show the module `make` line and `CC [M]` objects but no `-j`, no elapsed time, no CPU; no bug report or dataset with a DKMS duration or CPU figure was found. Established by rows 15, 22, 25 (GitHub search for make.log with "elapsed time": 0 hits), 23 (Debian BTS unreachable: challenge page).
- **T6 — single-CPU-confined builds; process-lifetime studies.** No public measurement of a parallel build pinned to one CPU (`taskset`/cgroup) or of `-jN` on one core with process counts/CPU totals (row 33: none; S3-08(b) is a 1999 single-CPU `-j4…7` wall-time table; S3-19 is a two-core eyeball). No `-j1` vs `-jN` table in the kcbench material (S3-15, S3-16 have no `-j 1` run). OpenBenchmarking `build-linux-kernel` result pages: 403 with default and browser UAs (rows 11, 12). No process-lifetime dataset (row 17). Yocto autobuilder buildstats: not published at the URLs tried (row 10). Chromium build stats: form only (row 37).
- **T7 — measured thread count / sustained utilisation of encoders, training loops, indexers.** Blender Open Data (S3-06) gives render durations and machine thread counts but not utilisation; ClamAV (S3-13) gives durations and file counts, "A LOT of CPU" only; tracker (S3-18) gives "100% CPU" without measurement; x264/ffmpeg and PyTorch searches (rows 31, 35) returned guidance pages, no measured utilisation logs. ananicy: type classes found (S3-11) but no shipped compiler rule located in the CachyOS tree folders listed; the original README's `gcc` line is a syntax example.
