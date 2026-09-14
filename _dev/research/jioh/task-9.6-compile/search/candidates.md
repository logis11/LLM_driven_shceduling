# Task 9.6 — candidates per scope-card item

Stage 2 result. Each item of `../scope-card.md` with the candidates the four class records found (`S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`), what each covers, and what no class found. Candidate ids are the records' own. Written by the research routine; nothing here is a decision.

## Observations that exist

Observations (a population, trace, run or build with numbers), as distinct from documentation:

| Id | What | Machine / project / window | Kind of data |
|---|---|---|---|
| S1-01 (`ocallahan-atc17`) | rr paper, §4.1/§4.3, read independently | Dell XPS15, quad-core Skylake (8 SMT), 16 GB, Fedora 23 / DynamoRio 6.1.0 `make -j8` / 20.99 s, six runs, warm cache | one count: 2 430 processes forked and exec'd, "mostly short-lived"; single-core run 3.36× the wall; no lifetime statistic; not a kernel build |
| S1-18 (Antfarm, ATC '06) | process-tracking evaluation | 2.4 GHz Pentium 4 host, Xen guests Linux 2.4.30 / 2.6.11 / bash `make -j 20` / one build each | 815 (2.4) and 748 (2.6) processes per build; mean fork→exec < 1 ms; mean exec→exit lifetime "more than 2 seconds"; no per-type breakdown |
| S1-05 (Gouicem, ATC '20) | scheduler trace of a kernel build | 4 × Xeon E7-8870 v4, 160 threads / Linux 5.4 `-j320` / 0–31 s | phase structure (parallel 4.5–18 s, sequential 0–4.5, 18–22, 22–31 s); short-lived fork/exec'd tasks, longest visible ≈ 20 ms; fork→wait ≈ 50 µs |
| S1-02 (Boyd-Wickizer, OSDI '10) | MOSBENCH gmake | 8 × 6-core Opteron 8431 / Linux 2.6.35-rc5 defconfig objects, `-j` = 2 × cores, tmpfs | 35× speedup at 48 cores; 7.6 % system time at one core; "more processes than there are cores" |
| S1-08 (Blanchard 2002) | kernel-compile benchmark run | 24-way POWER4 LPAR / 2.4.18 x86 cross build `make -j14 bzImage` / 10.31 s | user 130.63 s, system 71.31 s, 1957 % CPU; final link single-threaded |
| S1-26 (Traeger et al., TOS 2008) | file-system benchmark study | ext2 remounted per phase (cold-ish) / OpenSSH 3.5–3.9 build, serial | build > 99.2 % CPU-bound; a 32× read slowdown costs ≤ 4.5 % elapsed; kernel 2.4.20 defconfig VFS mix "strongly read biased" |
| S1-07 (Harchol-Balter & Downey, TOCS '97) | UNIX process CPU lifetimes from `lastcomm` | six 1990s academic UNIX machines / > 1 M processes / semesters | Pr{L > T} ≈ 1/T above 1 s CPU; sample mean 0.4 s, CV 5–7; the reader's computation: 92–96 % of processes ≤ 1 s CPU |
| S1-24 (ActPlane, arXiv 2606.25189) | fork/exec microbenchmark + kernel build | Core Ultra 9 285K, Linux 6.15.11 / defconfig `make -j24` | native fork 48.94 µs, exec 248.30 µs medians; build used as overhead workload, no process data |
| S1-04 (`schedcp-mlsys25`) | build time under schedulers | 86-core Xeon 6787P (machine not tied to the build in v4) / Linux 6.14 tinyconfig `make -j 172` | 13.57 s EEVDF → 8.31 → 7.60 s; "short-lived processes" is an agent-generated profile string |
| S3-01 (Gregg, `perf sched`, 2017) | one second of `perf sched record` during a kernel build | 8-vCPU Xeon E5-2680 v2 VM, kernel 4.10 / build tree and `-j` unstated / 1 s | per-comm runtime, switches, wakeup delay: `cc1` ×21 pids 6 013 ms / 1 138 switches (5.3 ms per schedule), `gcc` ×18 43.6 ms, `fixdep` ×6 81 ms, `recordmcount` ×7, `ld` ×3, `sh`→`cat`, two `make` pids; timehist rows with wait/run per event |
| S3-03 (Debian buildd, `linux` 7.1.13-1) | verbose build log | `x86-conova-01.debian.org` (hardware unstated) / three kernel flavours, `parallel=6`, gcc-15 / 2 h 39 m | the reader's counts: 45 608 `gcc -c` invocations over 19 819 distinct objects, 12 488 `ld` lines (3 073 `ld -r`), 18 972 `objtool`, 26 `modpost`; no timing per process |
| S3-04 (Fedora koji, kernel 6.17.0-rc1) | build logs | 2 × EPYC 9174F, 64 threads, 125 GiB / two kernel configs `-j64` / 63 min 47 s | `-j` = logical CPU count; silent make, no per-object lines |
| S3-05 (Yocto `yocto-buildstats`) | per-task rusage of a distribution build | `perf-debian12-vk` (CPU unstated), `PARALLEL_MAKE -j 16 -l 75` / poky master, `linux-yocto` 7.2.4 / 2026-09-14 | `do_compile` 229.0 s wall with 1 989 s user + 314 s system (10.05 CPUs busy), `ru_inblock` 568 (warm), 7.14 GB written, 140 666 involuntary vs 115 827 voluntary switches; children folded into one rusage; 556 `do_compile` tasks: p50 2.2 s, p90 30.2 s |
| S3-06 (Launchpad #2141316, DKMS `make.log`) | one DKMS module build | i7-4790 (4c/8t), Kubuntu 26.04 dev, kernel 6.19.0-3 / nvidia 580.126.09, `'make' -j8 … modules` / 58 s to failure | 208 `CC [M]` lines; `# elapsed time: 00:00:58`; triggered by an apt kernel upgrade; no CPU |
| S3-08 (three `.ninja_log` files, LLVM) | per-edge wall times | machines and `-j` unrecorded / LLVM sub-tree builds | per-TU wall p50 ≈ 6–8 s; peak concurrency 19 and 30 (one file is Windows) |
| S3-09 (LLVM compile-time tracker) | per-file `perf stat` | tracker machine (`-j7`, 8 CPUs implied) / 632 CTMark files, one LLVM commit, four configs | per-TU task-clock, wall, instructions; task-clock/wall ≈ 0.99 at `-O3` (CPU-bound, warm), 0.59–0.82 under ThinLTO; clang, not gcc |
| S3-10 (Phoronix) | kernel defconfig build times | 2 × EPYC 7742 / kernel 4.18 defconfig / 15–16 s; OpenBenchmarking mean 125 s over 2 687 submissions | wall only; "I/O appears to be the bottleneck" at 256 threads |
| S3-16 (Blender Open Data 2020) | 6 246 Linux CPU renders | hundreds of machines, CPU model per record / Blender 2.79 scenes | threads = all logical CPUs in every record; per-scene durations (bmw27 p50 224 s); no utilisation series |
| S1-15 (van Rijn, Middleware '21) | one transcode job | EPYC server VMs / ffmpeg H.264→H.265, 16 threads on 16 vCPUs / ≈ 65 s | "CPU bound"; no utilisation figure |
| S1-17 (Gyawali, arXiv 2309.02521) | CPU training run | unnamed workstation, 4.10 GHz / PyTorch CNN, 20 epochs | system-wide CPU utilisation 60–63 % |

Everything else found is documentation or source code (S2-01…S2-27; S3-11…S3-14; every S4 candidate), talk or course papers without process data (S1-08 aside, S1-19…S1-23, S1-25), qualitative statements (S1-03, S1-12), off-target measurements (S1-13 on-access antivirus on a Windows netbook; S1-14, S1-16 x264 threading on simulated or embedded hardware), or unmeasured claims (S3-07).

## Per item

### 1–3. `compiler-child.cpu_burst`, `cpu_tail` (per-child CPU and its spread)

- No observation gives the per-process CPU-time distribution of a Linux kernel build's compiler processes (S1 §3 T1/T2, S3 §3 T1/T2).
- Nearest per-translation-unit CPU data: S3-09, clang on CTMark, task-clock per file for 632 files at one commit, task-clock/wall ≈ 0.99 at `-O3`; S3-08, per-edge wall times of LLVM builds (p50 ≈ 6–8 s, machines unnamed); S3-14, Blender `-ftime-trace` frontend vs backend aggregate.
- Per-schedule and per-second cc1 behaviour in a kernel build: S3-01 — 21 `cc1` pids consumed 6 013 ms in 1 s on 8 vCPUs (75 % of capacity), 1 138 switches (≈ 5.3 ms per schedule), `gcc` drivers 43.6 ms; timehist rows `cc1[17083]` wait 19.998 ms / run 9.948 ms.
- Whole-build ratios: S3-05 `linux-yocto do_compile` 2 303 s CPU / 229 s wall at `-j16 -l75`, 13.6 % system; S1-08 user 130.6 s vs system 71.3 s at `-j14` (2002); S1-02 7.6 % system time at one core.
- Lifetime shape in general: S1-18 mean exec→exit "more than 2 seconds" for bash `make -j20` (2006, P4); S1-07 heavy-tailed CPU lifetimes across all UNIX processes.
- Which processes a spawn-table entry could stand for: S2-01 (per object `sh` → `gcc -c` [→ `cc1`, `as`] → optional `objtool` → `fixdep` → `rm`; `nm | grep` and `cpp | genksyms` for exporting objects; `ar` per directory; `ld -r` per module; 2–3 `ld` passes for vmlinux), S2-02 (driver stages; `-pipe` keeps compiler and assembler alive concurrently).
- Own measurement: per-process CPU at exit for every process of a build is documented for taskstats (S4-taskstats-delayacct, µs, `CAP_NET_ADMIN`), BSD accounting (S4-bsd-acct, 10 ms ticks, `comp_t`), a `CC=` wrapper with `/usr/bin/time -v` (S4-rusage-clock, wrapped children only), and `perf sched timehist` (S4-perf, per-thread run time per event, needs sudo, `perf` installable); polling `/proc` misses ms-lived processes (S4-proc-pid).

### 4–5. `compiler-child.disk_wait` (median and spread)

- No observation of a compiler process's blocked-on-I/O time under warm or cold cache (S1 §3 T2, S3 §3 T2).
- Whole-build evidence that a build is CPU-bound: S1-26 (OpenSSH build > 99.2 % CPU-bound on ext2 remounted before each phase; a 32× read slowdown costs ≤ 4.5 % elapsed); S3-09 (task-clock/wall ≈ 0.99 per file, warm); S3-05 (`ru_inblock` 568 against 7.14 GB written: reads served from the page cache); S3-10 ("I/O appears to be the bottleneck" only at 256 threads on a 2-socket EPYC).
- Instruments that would measure it on a runner: taskstats `blkio_delay_total`/`blkio_count` per exiting task, delay accounting compiled in but off by default — needs `kernel.task_delayacct=1` before the build (S4-taskstats-delayacct, S4-azure-kernel-config); `/proc/<pid>/stat` `delayacct_blkio_ticks` in centiseconds when polled (S4-proc-pid); cgroup `io.pressure` for the build as a whole (S4-psi-cgroup, PSI on by default); `vm.drop_caches` under sudo for the cold case (S4-page-cache-disk). BSD accounting records no I/O at all (`ac_io`/`ac_rw` never assigned, S4-bsd-acct).

### 6. `sampling: per-instance`

- Nothing found bears on it; consistent with the spawn table (scope card).

### 7. `pattern: RUN / WAIT disk / RUN / EXIT`

- No document or dataset shows a run / wait / run structure inside a compiler process; the per-file evidence is CPU-bound throughout (S3-09), and the per-event evidence is many short schedules (S3-01: ≈ 5.3 ms per `cc1` schedule; S3-02: `gcc` events of 1.148, 0.024, 0.022 ms).
- `perf sched timehist` is the one instrument documenting the run/wait/run structure of a process (S4-perf).

### 8. `lifetime: spawned`, `spawned_by`

- Mechanism only: S2-05 (make starts one job per recipe; `posix_spawn`/`vfork`; a shell whenever the recipe line contains `;`, which every kbuild `cmd` does), S2-01.

### 9, 19. `category_source: ocallahan-atc17` (both archetypes)

- S1-01 read independently confirms the K1 finding: DynamoRio 6.1.0 `make -j8` on a Skylake laptop; 2 430 processes; no process kind, no lifetime statistic.
- S1-03: Coetzee's short-lived processes are "cp and mkdir"; no count.
- Named-build alternatives with counts: S1-18 (bash `make -j20`: 815 / 748 processes, mean post-exec lifetime > 2 s, machine named); S3-03 (a full Debian kernel build's invocation counts by tool); S3-01 (a kernel build's process mix per second by comm).
- Named-build descriptions without counts: S1-05 ("short-lived processes … one after the other", ≤ 20 ms visible), S1-02 ("more processes than there are cores"), S1-12 (qualitative), S2-21 (CachyOS dropped compiler rules because "Every process which gets spawned, will be adjusted" caused "really noticeable cpu usage" — an indirect statement that builds spawn very many processes).

### 10, 20. `validation_stats` (concurrency unit; fork rate)

- The ≤ N-jobs invariant and what a job is: S2-05 (one slot per recipe; sub-makes share tokens; `+` jobs do not count).
- Live processes per job: S2-01 + S2-02 (`sh`, `gcc`, `cc1`, `as` can all be alive for one object; `-pipe` makes `cc1` and `as` concurrent), S3-01 (21 `cc1` and 18 `gcc` pids seen within 1 s on 8 vCPUs), S3-08 (peak concurrency 19 / 30 under ninja), S3-05 (peak 16 tasks = `BB_NUMBER_THREADS`).
- Fork/exec rate: S1-01 (the reader's 2 430 / 20.99 s ≈ 116 /s), S1-24 and S1-11 (fork+exec cost 0.3–0.5 ms on desktop CPUs).

### 11, 21. `modeling_notes` wording

- Corrected attributions follow from S1-01 (DynamoRio, not kernel), S1-03 (`cp`/`mkdir`), S2-19 (interbench Compile creates no process), and from the 9.3 re-analysis for the measured figures (scope card items 1–5, 13).

### 12. Unit of the child (`cc1` vs make's child vs family member)

- S2-01: kbuild's per-object recipe is one make job that runs `/bin/sh`, the `gcc` driver, `cc1`, `as`, optionally `objtool`, then `fixdep` and `rm` — so one make job is ≈ 6–7 processes for a plain object.
- S3-01: within one second `gcc` drivers used 43.6 ms against `cc1`'s 6 013 ms (0.7 %); `fixdep` 81 ms over 6 pids.
- S3-03: per full Debian kernel build (three flavours) 45 608 compiler-driver invocations, 12 488 `ld` lines, 18 972 `objtool` lines, 26 `modpost`.
- S2-20/S2-21: shipped catalogues match by executable basename (`gcc`, `make`, `cmake`, `ninja`…); `cc1`, `as`, `ld` are unlisted.
- S4-bcc / S4-ftrace-tracecmd / S4-taskstats-delayacct: PPID and comm at exit are recorded, so the nesting (`sh` ⊃ `gcc` ⊃ `cc1`, `as`) is observable on a runner.

### 13–15. `build-orchestrator.dispatch_overhead` (value, spread, sampling)

- No measurement of make's own CPU cost per dispatched job in any class (S1 §3 T3, S2 §3 T3, S3 §3 T3, S4 §3 T3).
- Mechanism: S2-05 (`new_job` blocks in `reap_children` or `jobserver_acquire` at the cap; one token read per job; `posix_spawn`/`vfork`; shell for `;`-containing lines); S2-06 (ninja: FIFO jobserver, cap = `-j`); S2-04 (sccache jobserver participation).
- Historical or qualitative cost figures: S1-09 (1997: 10 s of `stat` for 1 000 files on a 66 MHz i486, 15 s for 100 sub-makes); S1-10 (ninja's driver cost "relatively little", unmeasured).
- Fork/exec cost bounds: S1-11 (`posix_spawn` ≈ 0.5 ms; fork+exec up to 25 ms with parent size, i7-6850K), S1-24 (fork 48.94 µs, exec 248.30 µs, Core Ultra 9 285K).
- Own measurement: `make --debug=j` / `--trace` log every dispatch on make 4.3 (S4-make); make's own CPU per job is then an exit-record quantity (taskstats or BSD accounting for the `make` processes, S4-taskstats-delayacct, S4-bsd-acct).

### 16. `pattern`: fork loop with a cap, `WAIT children`

- S2-05: the cap is enforced by blocking token reads; recursive makes (kbuild runs one per directory, S2-01 `Makefile:1261–1263`) share the slots; `-l` is checked against the running-task count in `/proc/loadavg`.
- S3-01: two `make` pids alive in the 1 s window.
- No document supports or contradicts modelling one FORK per compiler process; the mechanism dispatches recipes, each of which is a small process tree (item 12).

### 17. `spawn_count` prose default 2,430

- S1-01: 2 430 is the DynamoRio build's count (not kernel).
- Counts for named builds: S1-18 (bash: 815 / 748); S3-03 (Debian kernel, three flavours: 19 819 distinct objects, 45 608 compiles); S3-06 (nvidia DKMS module: 208 objects); S3-05 (poky image: 556 `do_compile` tasks); S3-09 (CTMark: 632 files).
- Bound values in timelines are 9.10's (scope card).

### 18. `parallelism_cap` default -j8

- Vendor defaults, all with locators: dpkg `-j auto` = online processors (S2-09); rpm `-j${RPM_BUILD_NCPUS}` capped by memory (`%_smp_tasksize_proc` 512 MB; Fedora 1 024 MB per core) (S2-10); Arch template `#MAKEFLAGS="-j2"` with the wiki's `--jobs=$(nproc)` (S2-11); Gentoo ≤ min(threads, RAM / 2 GB) with `--load-average` slightly above the CPU count, Portage default `nproc` (S2-12); kernel docs `make -j $(nproc --all)`, Debian handbook and Ubuntu wiki `nproc` (S2-13); ninja `processors + 2` (S2-06, S4-ninja); cargo logical CPUs (S2-07); CMake defers (S2-08); dkms `-j$(nproc)` (S2-14); PTS `-j $NUM_CPU_CORES` (S2-17, S3-11); cachyos-benchmarker `-j$(nproc)` (S3-12).
- Observed choices: Debian buildd `parallel=6` (S3-03); Fedora koji `-j64` on 64 threads (S3-04); Yocto perf host `-j 16 -l 75` (S3-05); DKMS `-j8` on an 8-thread i7-4790 (S3-06); LLVM tracker `-j7` on 8 CPUs "to reduce noise" (S3-09); papers: 2 × cores (S1-02), 2 × threads (S1-05), 172 on 86 cores (S1-04), 64 on 64 (S1-06), 24 on 24 cores (S1-24), `-j8` on 8 threads (S1-01), the 2009 folk rule "-j greater than the number of CPUs" (S1-20).
- The `-j4` that brackets the current convention labels an interbench emulation that runs no make (S2-19).
- No survey or observation of what desktop users pick (S2 §3 T4, S3 §3 T4); no vendor rationale for `nproc + 1` or `2 × nproc` (S2 §3 T4).

### 22. `dkms` on `build-orchestrator` (c7-compile)

- S2-14: an autoinstall run executes `make -j$(nproc) KERNELRELEASE=<ver> -C <kernel-src> M=<build-dir>` per module (a kbuild external-module build, so item 12's process chain per object), triggered by the kernel package's `postinst.d` hook → `dkms_autoinstaller` → `dkms autoinstall`, by `dkms.service` at boot, or by Fedora's `kernel/install.d`; no duration or process count stated.
- S3-06: one real run — `'make' -j8 … modules`, 208 `CC [M]`, 58 s, i7-4790, triggered by an apt kernel upgrade.
- S3-07: an unmeasured forum claim (15–20 min vs 2–3 min, server hardware).
- The same kbuild process chain as `make` (S2-01), at `nproc` rather than a user-chosen `-j`.

### 23–25. `cpu-batch` — `category_source`, notes, validation wording

- S2-19: interbench Burn = N pthreads spinning continuously (N = online CPUs in code at master, "4" in the man page); Compile = Burn + one write + one read thread inside the interbench process; no process created; "until done" and finite work are not interbench's.
- S2-20: upstream Ananicy types compilers and build drivers `compiler` = nice 1 (README recommends nice 19 and a 90 % CPU-quota cgroup for compiling); S2-21: CachyOS classes `ffmpeg` `Heavy_CPU` (nice 9), `clamd` and HandBrake's `ghb` `BG_CPUIO` (nice 16, `SCHED_IDLE`, idle I/O), and leaves compilers unclassed with recorded reasons; S2-22: ananicy-cpp's gcc example nice 19 / `SCHED_BATCH` / idle I/O (an example, not a shipped default).
- No source calls interbench "the community's" model (S1 §3 T7 found no literature on it).

### 26. `cpu-batch` bindings (`python3`, `ffmpeg`, `HandBrakeCLI`, `clamscan`, `tracker-miner-fs-3`, the `chrome` spoof)

- Thread counts from primary documentation: x264 `1.5 × processors` frame threads, ffmpeg codec `threads` `auto` (S2-26); PyTorch intra-op pool = physical cores (S2-27); `clamd` up to `MaxThreads` 10 with `--multiscan`, otherwise one thread per request; `clamscan` single process (S2-23); tracker-miner-fs runs at `SCHED_IDLE`, nice 19, idle I/O in `background.slice` (S2-24); plocate `updatedb` daily at nice 19 / idle I/O (S2-25); HandBrake CLI documents no thread option (S2 §3 T7).
- Observations: S3-16 (Blender CPU renders use all logical CPUs, per-scene durations); S1-15 (ffmpeg 16 threads on 16 vCPUs ≈ 65 s, "CPU bound"); S1-17 (CPU training at 60–63 % system utilisation, unnamed machine); S1-14, S1-16 (x264 threading model, parallel fraction 0.888); S1-12 (Blender and video render named as batch loads in a scheduler-agent benchmark).
- Not found: a measured full antivirus scan (S1-13 is on-access overhead on a Windows netbook; Uluski 2005 and Dogonyaro 2020 unreachable), an indexer's full rescan (only unmeasured "100 % CPU for hours" bug reports, S3 log 33), any observation of a single-thread saturating job matching the archetype's shape.

### 27–31. Registry lines

- Corrected wording follows from S1-01 (DynamoRio; no compiler named), S1-03 (`cp`, `mkdir`), S2-19 (Burn thread count; Compile emulation) and, for `meas-ci`, from the 9.3 re-analysis and S4 (what a runner can observe).

### T8 — what a runner can observe (for a re-measurement, if stage 3 wants one)

- Runner: 4 vCPU / 16 GB / 14 GB SSD, fresh Azure VM per job, passwordless sudo; no CPU model, VM size, disk backend or variance statement in GitHub's docs (S4-gh-hosted-runners); image `ubuntu-latest` = 24.04, kernel `6.17.0-1022-azure`, gcc 13, clang 16–18, make 4.3, ninja 1.13.2, GNU time 1.9; no tracing or accounting tool preinstalled, all apt-installable including the kernel-matching `perf` (S4-runner-2404, S4-ubuntu-pkgs).
- Kernel config (Ubuntu package evidence): BSD accounting v3, taskstats, delay accounting, task I/O accounting, PSI (default on), schedstats, BTF, kprobes, ftrace, BPF all compiled in; `HZ=1000`; `perf_event_paranoid` defaults to 4, so perf needs sudo (S4-azure-kernel-config).
- Per-process at exit, whole population including ms-lived processes: taskstats (µs CPU, ns delays incl. `blkio_delay_total` if `kernel.task_delayacct=1`, bytes, PPID; listener overrun risk at high exit rates), BSD accounting (10 ms ticks, no I/O), BCC `execsnoop`/`exitsnoop` (lifetime, PPID, no CPU), trace-cmd `sched:*` (CPU as summed switch intervals), forkstat (wall lifetime, documented event loss under load), a `CC=` wrapper with `/usr/bin/time -v` (wrapped children only) (S4-taskstats-delayacct, S4-bsd-acct, S4-bcc, S4-ftrace-tracecmd, S4-forkstat, S4-rusage-clock).
- Run/wait structure: `perf sched record` + `timehist` (S4-perf). Build-wide stalls: `systemd-run --scope` + `cpu.stat`, `io.stat`, `io.pressure` (S4-psi-cgroup). Dispatch: `make --debug=j`/`--trace` (S4-make). Cold cache: `vm.drop_caches`; disk type via `queue/rotational` (S4-page-cache-disk).
- Not observable: desktop-class hardware, a user's own `-j`, an interactive session, hardware counters inside the VM (no primary statement), the runner's runtime sysctls until read on the runner (S4 §3).

## Not found, all classes

- Per-process lifetime or CPU-time distributions of a Linux kernel build's processes by role (T1): no paper, dataset or trace; the nearest are S3-01 (one second, per comm), S1-18 (bash, 2006, means only), S3-03 (invocation counts only).
- CPU time per translation unit for gcc or the kernel (T2): only clang/LLVM data (S3-09, S3-08) and a Blender `-ftime-trace` aggregate (S3-14).
- A compiler process's blocked-on-I/O time, cold or warm (T2): no observation; only whole-build CPU-boundness (S1-26, S3-05, S3-09).
- Make's own CPU cost per dispatched job (T3): no measurement; the one jobserver-related paper (Belinassi et al. 2022) is paywalled and unread.
- What `-j` desktop users pick (T4): no survey or poll; the Gentoo forum poll is behind a login.
- DKMS run CPU time and process counts (T5): one `make.log` with objects and wall time (S3-06); nothing with CPU.
- Process-lifetime distributions on Linux desktops (T6): only the 1990s UNIX study (S1-07) and the unread Leland & Ott 1986; no dataset.
- A measured antivirus full scan or file-indexer rescan (T7): none open; Uluski 2005, Kubota 2019, Belinassi 2022, Leland & Ott 1986 paywalled (dl.acm.org 403, ieeexplore 418).
- Hardware variance and VM size of hosted runners (T8): not documented by GitHub.
- Unreachable on 2026-09-14: github.com HTML and api.github.com (403), dl.acm.org (403), ieeexplore.ieee.org (418), openbenchmarking.org (403), lore.kernel.org (403), git.launchpad.net (403), dashboard.kernelci.org (403), chromium-build-stats (Google sign-in), docs.fedoraproject.org / sources.debian.org / salsa / gitlab.archlinux.org / code.videolan.org (proof-of-work challenge pages; sources.debian.org answered with curl's default UA), git.kernel.org (Anubis challenge mid-session; the GitHub mirror and curl's default UA were used), cmake.org (503), gitlab.gnome.org (406), git.sesse.net (proxy-rejected), en.opensuse.org (403), arXiv API (429), dblp API (bot-check page), diva-portal (503).
