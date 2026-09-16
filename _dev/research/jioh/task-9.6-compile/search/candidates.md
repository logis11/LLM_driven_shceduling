# Task 9.6 — candidates per scope-card item

Stage 2 result, second run of the slice (issue #11). Each item of `../scope-card.md` with the candidates the four class records found (`S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`), what each covers, and what no class found. Candidate ids are the records' own. Written by the research routine; nothing here is a decision.

## Observations that exist

Observations (a population, trace, run, build or log with numbers), as distinct from documentation:

| Id | What | Machine / project / window | Kind of data |
|---|---|---|---|
| S1-01 (`ocallahan-atc17`) | rr paper §4.1/§4.3, read independently | Dell XPS15, quad-core Skylake (8 SMT), 16 GB, SSD/Btrfs, Fedora 23 / DynamoRio 6.1.0 `make -j8` / 20.99 s baseline, six runs, warm cache | one count: 2 430 processes forked and exec'd, "mostly short-lived"; the same build confined to one core with `taskset` (`-j8` omitted) takes 3.36× the wall; no lifetime statistic, no process kind; not a kernel build |
| S1-04 (Antfarm, USENIX ATC '06) | process-tracking evaluation, Table 2 and §6.1.1 | 2.4 GHz Pentium IV, 512 MB, Xen 2.0.6, 128 MB guests / bash sources `make -j 20`, clean object dir / one build per guest OS | 815 (Linux 2.4.30) and 748 (Linux 2.6.11) process creations per build (2 602 on Windows under Simics); OS context switches 4 447 / 2 550; mean fork→exec < 1 ms, mean exec→exit "more than 2 seconds"; no per-program breakdown, no CPU |
| S1-05 (Gouicem et al., ATC '20) | per-core frequency/activity trace of a kernel build | 4 × Xeon E7-8870 v4, 80 cores / 160 threads / Linux 5.4, `-j 320`, config unnamed / ≈ 31 s | phase structure (parallel bulk 4.5–18 s, near-sequential tails); sequential phases are fork/wait processes shorter than the frequency-transition latency (tens of ms); no counts |
| S1-06 (Lozi et al., EuroSys '16) | scheduler bug study | 8 × 8-core Opteron 6272, 512 GB / "make with 64 threads", kernel/config unnamed / window unstated | make completion −13 % after the fix; the one literature sentence on autogroup's load division |
| S1-07 (Boyd-Wickizer et al., OSDI '10) | MOSBENCH gmake | 48 × Opteron 8431 / Linux 2.6.35-rc5 defconfig objects, `-j` = 2 × cores, tmpfs, warm cache | 35× speedup at 48 cores vs one core; 7.6 % system time at one core; "more processes than there are cores"; Psearchy indexer kernel-time share 1.9 % → 23 % |
| S1-08 (Traeger et al., TOS 2008) | file-system benchmarking study, §12.2 | one machine (described in §6, not quoted) / OpenSSH 3.5/3.7/3.9 configure+compile on ext2 and a 32×-slowed ext2, ≥ 10 runs | CPU % "always more than 99.2 %"; a 32× read slowdown costs ≤ 4.5 % elapsed; compile benchmarks "are bound by CPU time spent in user space"; census: 36 of 106 papers timed a compile, 8 an OS kernel |
| S1-09 (Harchol-Balter & Downey, TOCS 1997) | UNIX process CPU lifetimes from `lastcomm` | six 1990s academic UNIX machines / > 1 M processes / semester-scale | P{L > T} ∝ T^k, k ∈ [−1.3, −0.8] for L > 1 s; sample mean 0.4 s, CV 5–7; Leland & Ott 1986 (9.5 M processes, k ∈ (−1.25, −1.05)) quoted second-hand, ACM copy 403 |
| S1-10 (Kubota & Kono, IEICE 2021) | per-file compile times of LLVM and WebKit | Dell PowerEdge R430, 8-core Xeon E5-2620 v4, 128 GB, SATA HDD, Fedora 29 / LLVM ca1e713, WebKit ec4eb02, Mesa 18.3.6; GCC 8.3.1 `-ftime-report`; `-j` unstated | parse share per file (> 60 % of compile time in 56 % of LLVM files, 80 % of WebKit files); per-file compile time as a scatter against ‘;’ count; no percentiles |
| S1-03 (`schedcp-mlsys25`) | build time under schedulers | 86-core / 172-thread Xeon 6787P, 758 GB / Linux 6.14 tinyconfig `make -j 172` / 13.57 s × 3 runs | 13.57 s EEVDF → 8.31 s scx_rusty → 7.60 s scx_layered; "short-lived processes" is an agent-generated profile string; no process data |
| S1-11 (Uluski et al., CAN 2005) | on-access antivirus overhead | Simics model of a 2 GHz Pentium 4, 256 MB, Windows XP / four AV products / three short scenarios | 23–129 % execution-time increase; no thread count, utilisation or full-scan duration |
| S3-01 = S3-02 (Gregg, `perf sched`, 2017) | one second of `perf sched record` during "a software build" | `bgregg-xenial`, Xeon E5-2680 v2, 8 vCPUs, 15.4 GB, kernel 4.10-virtual, 26 Feb 2017 / project, config, `-j` unnamed (task names `fixdep`, `recordmcount`, `cc1`, `gcc`, `as`, `ld`, `make`, `sh`) / 1 s | per-comm on-CPU totals and switches in the window: `cc1` (21 pids) 6 013 ms / 1 138 switches (avg delay 5.3 ms, max 44 ms), `gcc` (18) 43.6 ms, `as` (16) 121.8 ms, `sh` (25) 107 ms, `make` (18) 54 ms / 114, `fixdep` (6) 81 ms, `ld` (3) 14 ms; `sched_stat_runtime` slices of 3.0–4.0 ms; timehist rows with wait / delay / run per event (e.g. `cc1[17083]` wait 19.998 ms, run 9.948 ms); 1.886 MB / 13 502 samples per second on 8 CPUs; no lifetimes |
| S3-03 (Debian buildd, `linux` 7.1.13-1) | verbose sbuild log | `x86-conova-01.debian.org`, core count unstated, host kernel 6.12 / all amd64 flavours, `DEB_BUILD_OPTIONS=parallel=6`, gcc-15 / 2026-09-03 21:35 → 09-04 00:14 UTC, Build-Time 9 443 s | the reader's counts over the 214 MB log: 45 599 `gcc … -c -o` lines, 12 488 `ld` lines, 18 915 `objtool` lines; no per-process timing |
| S3-05 (Fedora Koji, kernel-7.2.6-300.fc45) | mock/rpmbuild logs, task 150245382 | 2 × EPYC 9174F, 64 threads (hw_info.log) / Fedora kernel configs, `make -j64` / 68 min | `-j` = logical CPUs; silent make; no per-object lines |
| S3-04 (LLVM compile-time tracker) | per-file `perf stat` for CTMark | tracker machine unnamed on the pages read, `-j` unnamed / 632 CTMark files at stated configs, one LLVM commit pair | per-file `task-clock`, `instructions:u`, `wall-time`; the reader's percentiles for stage1-O3: p50 96 ms, p90 236 ms, max 10.4 s; clang, not gcc; no blocking column |
| S3-14 (two public `.ninja_log` files) | per-edge wall times of LLVM builds | machines and `-j` unrecorded (one file a Windows `.obj` build) | per-edge duration p50 5–11 s; concurrency computed by the reader bounds `-j` from below |
| S3-09 (Yocto buildstats) | one `do_compile` record plus the format description | machine and `PARALLEL_MAKE` unnamed / one recipe, 2019 | per-task utime/stime (task shell + children), `/proc/pid/io` bytes, rusage `ru_inblock`, `ru_majflt`, `ru_nvcsw`/`ru_nivcsw`; whole-`make` granularity |
| S3-15, S3-16 (kcbench: Greg KH 2020; kcbench 0.9.0 announcement and man page) | kernel `defconfig` `make vmlinux` timings with `[P:…%]` CPU use | 8-CPU laptop / 40-CPU / 64-CPU (Greg KH, Linux 5.7.0, gcc 10.2, ccache off, caches pre-filled); i5-4570, i7-8700K, 3990X, EPYC 7742 (man page) / `-j` ∈ {N, N + a few, N/2, …} | e.g. 8 CPUs: 392.69 s at `[P:768%]` for `-j 8`, 441.86 s at `[P:392%]` for `-j 4`; 3990X: `-j 64` beats `-j 128`; no `-j 1` run anywhere |
| S3-07 (Phoronix 2019 + PTS `build-linux-kernel` 1.16.0) | whole-build wall time and the benchmark definition | 2 × EPYC 7742, Ubuntu 19.04, Optane / Linux 4.18 sources then (profile: Linux 6.8 defconfig/allmodconfig, `make -s -j $NUM_CPU_CORES`, 3 runs) | 15–16 s; OpenBenchmarking population mean 125 s over 2 687 submissions quoted second-hand; "I/O appears to be the bottleneck" at 256 threads |
| S3-17 (Desaulniers 2018, ccache) | whole kernel build at `-j4` | machine and config unnamed / 3 runs | user 2 008.93 s + system 231.69 s at 346 % over 10:47; 3 242 ccache misses read by the reader as compiler invocations reaching the compiler |
| S3-08 (LKML, Jan 1999) | two `make -j` timing posts | P166 / 92 MB and K6-266 / 32 MB, single CPU / kernel 2.2.0-pre, `-j` unbounded and `-j4…7` / whole builds | shell `time` summaries (32–90 % of one CPU for unbounded `-j`); wall time by `-j` cold vs preconditioned; 1999 hardware |
| S3-19 (LKML, Feb 2006) | "make -j with j ≤ 4 seems to only load a single CPU core" | Athlon 64 X2 4400+ / 2.6-era kernel builds, `-j 2…5+` / no window | an eyeballed observation, no numbers beyond "~half" and "close to 100 %" |
| S3-10 (four Launchpad DKMS `make.log`s) | DKMS module builds | user machines mostly unnamed / nvidia and other modules, kernel named / one failed build each | the module `make … -C /lib/modules/<kver>/build M=<dir> … modules` line, `CC [M]` / `AR` / `LD` lines; no `-j`, no elapsed time, no CPU in any of the four |
| S3-06 (Blender Open Data, 2026-09-16 snapshot) | 651 553 CPU scene renders, 91 088 on Linux | hundreds of machines, CPU model and thread count per record / named scenes / per-record timestamp | render durations and machine thread counts; no utilisation series |
| S3-13 (Microsoft Q&A 5550992, ClamAV) | two full-filesystem `clamscan -i -r /` summaries | two Azure RHEL VMs, hardware unnamed / 2025-08-05 and 2025-09-08 | 195 265 files, 451.9 GB read, 47 569 s; 70 593 files, 7.2 GB, 53 min; "A LOT of CPU"; single-process scanner |
| S3-18 (Launchpad 2025523, tracker3) | "100 % CPU for a long time" | Ubuntu 22.04, machine undescribed | a report without measurement |
| S4-19 (RunsOn, CPU-speed sample) | 30-day sample of CPU models on GitHub-hosted `ubuntu-24.04` | vendor aggregator / official runner labels | at least two Xeon models on one label (6973P-C vs Platinum 8573C), Passmark single-thread p50 3 382 vs 2 674 (26 % spread) |
| S4-22 (actions/runner-images issue bodies) | user reports on hosted runners | `ubuntu-24.04` x64 | `sudo sysctl kernel.perf_event_paranoid=1` accepted and `perf record -a` runs; a job-log block naming a "Hosted Compute Agent"; `Runner.Listener` / `Runner.Worker` process paths in a `ps` listing |

Everything else found is documentation or source code (S2-01…S2-23; S4-01…S4-18, S4-20, S4-21), argument or model papers (S1-12, S1-13), or qualitative statements (S1-02).

## Per item

### 1–3. `compiler-child.cpu_burst`, `cpu_tail` (per-child CPU and its spread)

- No observation gives the per-process CPU-time distribution of a Linux kernel build's compiler processes (S1 Not found T1; S2 Not found T1; S3 Not found T1).
- Nearest per-translation-unit CPU data: S3-04 (clang on CTMark, per-file `task-clock`, 632 files; the reader's p50 96 ms / p90 236 ms / max 10.4 s at stage1-O3; machine and `-j` not named on the pages read); S3-14 (per-edge wall times of LLVM builds, p50 5–11 s, machines unknown); S1-10 (LLVM/WebKit per-file compile time as a scatter, parse share only, gcc 8.3.1 on a named Xeon).
- Per-schedule cc1 behaviour in a kernel build: S3-01/02 — 21 `cc1` pids consumed 6 013 ms in 1 s on 8 vCPUs, 1 138 switches (≈ 5.3 ms per schedule), `sched_stat_runtime` slices of 3–4 ms, `gcc` drivers 43.6 ms; timehist rows `cc1[17083]` wait 19.998 ms / run 9.948 ms.
- Whole-build ratios: S3-17 (user 2 009 s + sys 232 s at `-j4`, 346 %); S3-15/16 (`[P:…%]` per `-j`); S1-07 (7.6 % system time at one core); S3-09 (Yocto per-task utime/stime at whole-`make` granularity).
- Lifetime shape in general: S1-04 (mean exec→exit "more than 2 seconds" for bash `make -j 20`, 2006); S1-09 (heavy-tailed CPU lifetimes across all UNIX processes, 1990s).
- Which processes a spawn-table entry could stand for: S2-01 (kbuild v6.6: per object one `$(CC)` — the driver spawns `cc1` and `as`, pipe-connected only with `-pipe` — then optional `objtool`, `fixdep`, `rm` in one `set -e` shell line; `$(NM)|grep|$(CPP)|genksyms` only for exporting objects under MODVERSIONS; one sub-make per directory; `modpost`/`modfinal` as later sub-makes; vmlinux linked by a shell script calling `$LD` directly, so no `collect2`), S2-02 (GCC driver stages; `collect2` only for user-space links).
- Own measurement under the pin: per-process CPU at exit for every process, including ms-lived ones, is documented for taskstats (S4-05: `ac_utime`/`ac_stime` µs, `cpu_run_real_total` ns, listener registered on a cpumask that can be exactly the pinned CPU, summed per thread group at the last thread's exit; needs `kernel.task_delayacct=1` before the build for the delay fields) and BSD accounting (S4-06: clock ticks, `comp_t`, `CAP_SYS_PACCT`); `perf sched timehist` gives per-schedule run time for every thread that ran on the pinned CPU (S4-09, `-C`); a `/proc` poller still misses processes that live between two polls and no document quantifies how time-sharing on one CPU changes that censoring (S4 Not found).

### 4–5. `compiler-child.disk_wait` (median and spread)

- No observation of a compiler process's blocked-on-I/O time under warm or cold cache (S1 Not found T2; S3 Not found T2).
- Whole-build evidence that a build is CPU-bound: S1-08 (OpenSSH build CPU % > 99.2 % on ext2 remounted per phase; a 32× read slowdown costs ≤ 4.5 % elapsed); S3-04 (`task-clock` and `wall-time` per file both published; the reader's ratio is not recorded as a value); S3-09 (`ru_inblock` at whole-task level, one tiny task); S3-07 ("I/O appears to be the bottleneck" only at 256 threads on a 2-socket EPYC); S3-08 (1999 cold-vs-preconditioned whole-build wall times).
- Instruments that would measure it on a pinned runner: taskstats `blkio_delay_total` / `blkio_count` per exiting task (ns, synchronous block I/O, excluding submission; delay accounting compiled in, off by default, `kernel.task_delayacct=1` at runtime and only tasks started afterwards carry it — S4-05, S4-17; the runner's kernel config has `CONFIG_TASK_DELAY_ACCT=y`, S4-04); `/proc/<pid>/stat` field 42 `delayacct_blkio_ticks` when polled (S4-08); cgroup `io.pressure` for the build as a whole (S4-14, PSI on by default); `vm.drop_caches` for the cold case (S4-17). BSD accounting's I/O fields are never set (S4-06), rusage gives block-op counts not time (S4-07), `strace -f -c -w` keeps only aggregate totals (S4-10).

### 6. `sampling: per-instance`

- Nothing found bears on it; consistent with the spawn table (scope card).

### 7. `pattern: RUN / WAIT disk / RUN / EXIT`

- No document or dataset shows a run / wait / run structure inside a compiler process; the per-file evidence is CPU-bound throughout (S1-08, S3-04), and the per-event evidence is many short schedules (S3-01: ≈ 5.3 ms per `cc1` schedule, 3–4 ms runtime slices).
- `perf sched timehist` (`--state`, `-w`) is the one instrument documenting per-schedule run/wait with the sched-out state of a process (S4-09).

### 8. `lifetime: spawned`, `spawned_by`

- Mechanism only: S2-03 (make 4.4.1: one job per recipe; `vfork`/`posix_spawn`; a shell whenever the recipe line contains shell metacharacters, which every kbuild line does), S2-01, S2-23 (affinity inherited across fork and exec, so a pinned `make` confines every child).

### 9, 19. `category_source: ocallahan-atc17` (both archetypes)

- S1-01 read independently confirms the K1 finding: DynamoRio 6.1.0 `make -j8` on a Skylake laptop; 2 430 processes; no process kind, no lifetime statistic; single-core `taskset` run 3.36× the wall.
- S1-02: Coetzee's short-lived processes are "cp and mkdir"; no count.
- Named-build alternatives with counts: S1-04 (bash `make -j 20`: 815 / 748 processes, mean post-exec lifetime > 2 s, machine named, 2006); S3-03 (a full Debian kernel build's invocation counts by tool, the reader's computation); S3-01 (a kernel build's process mix per second by comm).
- Named-build descriptions without counts: S1-05 (fork/wait processes shorter than tens of ms in the sequential phases), S1-07 ("more processes than there are cores"), S2-13 (autogroup commit: "parallel kbuild has a negative impact on desktop interactivity"; Kconfig: "aggressive CPU burners (like build jobs)"), S2-15 (CachyOS dropped compiler rules three times, 2022–2024: "every process which gets spawned … really noticeable cpu usage").

### 10, 20. `validation_stats` (concurrency unit; fork rate)

- The ≤ N-jobs invariant and what a job is: S2-03 (top-level `-jN` creates a FIFO pre-loaded with N−1 tokens; each make, sub-makes included, runs one job on an implicit slot and blocks in `read()` for more; token returned at reap; at the cap `new_job` blocks in `reap_children`; `-l` compares `/proc/loadavg`'s system-wide running-task count, not the affinity mask), S2-04 (design rationale).
- Live processes per job: S2-01 + S2-02 (`sh`, `gcc`, `cc1`, `as` can all be alive for one object; `-pipe` makes `cc1` and `as` concurrent), S3-01 (21 `cc1` and 18 `gcc` pids seen within 1 s on 8 vCPUs), S3-14 (peak concurrency under ninja), S3-19 (2006: `-j` ≤ 4 did not fill two cores).
- Under the pin: `nproc` returns the affinity-mask count so `make -j$(nproc)` under `taskset -c 3` is `-j1` (S2-16, S4-16); the given workflow's explicit `-j8` is unaffected; rpm, ninja, ffmpeg, x264 also follow `sched_getaffinity`, dpkg and PTS do not (S2-05, S2-08, S2-09, S2-18, S2-20); make applies no load limit without `-l` (S4-13).
- Fork/exec rate: S1-01 (2 430 / 20.99 s ≈ 116 /s, the reader's arithmetic); S1-04 (fork→exec < 1 ms).

### 11, 21. `modeling_notes` wording

- Corrected attributions follow from S1-01 (DynamoRio, not kernel), S1-02 (`cp`/`mkdir`), S2-14 (interbench Compile creates no process), and from the 9.3 re-analysis for the measured figures (scope card items 1–5, 13). The venue of the existing observation (four vCPUs, unpinned) is a scope-card fact, not a search finding.

### 12. Unit of the child (`cc1` vs make's child vs family member)

- S2-01: kbuild's per-object recipe is one make job that runs `/bin/sh`, the `gcc` driver, `cc1`, `as`, optionally `objtool`, then `fixdep` and `rm` — one make job is ≈ 6–7 processes for a plain object; per directory one sub-make.
- S3-01: within one second `gcc` drivers used 43.6 ms against `cc1`'s 6 013 ms (0.7 %); `as` 121.8 ms over 16 pids; `fixdep` 81 ms over 6 pids; `sh` 107 ms over 25 pids.
- S3-03: per full Debian kernel build (all amd64 flavours) 45 599 compiler-driver invocations, 12 488 `ld` lines, 18 915 `objtool` lines (the reader's counts).
- S2-15, S3-11: shipped catalogues match by executable basename (`gcc`, `make`, `ninja`, `cargo`…); `cc1`, `as`, `ld` are unlisted.
- S4-05 / S4-11 / S4-12: PPID and comm at exit are recorded by taskstats, BPF exit tracing and forkstat, so the nesting (`sh` ⊃ `gcc` ⊃ `cc1`, `as`) is observable on a runner.

### 13–15. `build-orchestrator.dispatch_overhead` (value, spread, sampling)

- No measurement of make's own CPU cost per dispatched job in any class (S1 Not found T3; S2 Not found T3; S3 Not found T1/T2; S4 documents no such figure).
- Mechanism: S2-03 (token read at the cap; `vfork`/`posix_spawn`; a shell for every kbuild recipe line); S2-05 (ninja: always `/bin/sh -c`, FIFO jobserver client since 1.13, default `nproc + 2`); S2-06 (cargo: "1 cargo to N rustc" over the same jobserver).
- Historical or qualitative: S1-12 (recursive make's cost, 1998), S1-13 (dispatch model only); S3-01 (`make` (18 pids) 53.968 ms / 114 switches in one second, avg delay 2.3 ms — per-comm total, not per job).
- Own measurement: `make --trace` / `--debug=j` log every dispatch without root (S4-13); make's own CPU per job is then an exit-record quantity (taskstats or BSD accounting for the `make` processes, S4-05, S4-06); per-schedule run of `make` on the pinned CPU from `perf sched timehist` (S4-09).

### 16. `pattern`: fork loop with a cap, `WAIT children`

- S2-03: the cap is enforced by blocking token reads; recursive makes (kbuild runs one per directory, S2-01) share the slots; `-l` is checked against the running-task count in `/proc/loadavg`.
- S3-01: 18 `make` pids alive within the 1 s window.
- No document supports or contradicts modelling one FORK per compiler process; the mechanism dispatches recipes, each of which is a small process tree (item 12).

### 17. `spawn_count` prose default 2,430

- S1-01: 2 430 is the DynamoRio build's count (not kernel).
- Counts for named builds: S1-04 (bash: 815 / 748); S3-03 (Debian kernel, all flavours: 45 599 compiles, the reader's count); S3-17 (3 242 ccache misses in one `-j4` kernel build, read as compiler invocations); S3-04 (CTMark: 632 files); S3-10 (DKMS module: `CC [M]` lines per log).
- Bound values in timelines are 9.10's (scope card).

### 18. `parallelism_cap` default -j8

- Vendor defaults, all with locators: make 1 (S2-03); ninja `processors + 2` where processors = min(cgroup quota, affinity mask) (S2-05); cargo logical CPUs, "fully saturating all cores" (S2-06); CMake defers to the native tool (S2-07); dpkg `-j auto` = `getconf _NPROCESSORS_ONLN`, opt-in via `parallel=N` (S2-08); rpm `%_smp_mflags` = affinity-mask CPUs capped by memory / 512 MB per process (S2-09); Arch template `-j2` commented out, wiki `--jobs=$(nproc)` and `chrt -i 0` (S2-10); Gentoo `nproc` since Portage 3.0.31/3.0.53, `-l` slightly above, cap by RAM / 2 GB (S2-11); Debian kernel handbook `-j$(nproc)` (S2-08); dkms `-j$(nproc)` (S2-12); PTS `-j $NUM_CPU_CORES` = online CPUs (S2-20, S3-07); Fedora guideline's `-j3` on UP machines is advice for flushing out parallel-unsafe makefiles (S2-09).
- Observed choices: Debian buildd `parallel=6` (S3-03); Fedora koji `-j64` on 64 threads (S3-05); kcbench's `-j` ∈ {N, N + a few, N/2} with `-j 64` beating `-j 128` on a 3990X (S3-15, S3-16); Desaulniers `-j4` (S3-17); papers: `-j8` on 8 threads (S1-01), 2 × cores (S1-07), 2 × threads (S1-05), 172 on 172 (S1-03), 64 on 64 (S1-06); 1999 and 2006 developers (S3-08, S3-19).
- The `-j4` that brackets the current convention labels an interbench emulation that runs no make (S2-14).
- No survey or observation of what desktop users pick (S1 Not found T4; S2 Not found T4; S3 Not found T4: Gentoo forum login-walled, S3-12 withdrawn).

### 22. `dkms` on `build-orchestrator` (c7-compile)

- S2-12: DKMS 3.1.8 runs `make -j$(nproc) KERNELRELEASE=<ver> -C <kernel-src> M=<build-dir>` per module (an out-of-tree kbuild run, so item 12's process chain per object plus `modpost`/`modfinal` sub-makes), triggered by `dkms.service` (`autoinstall --kernelver %v`, Before=graphical.target), Debian `postinst.d` → `dkms_autoinstaller`, Fedora `install.d` → `kernel_postinst` → `autoinstall`; no duration, CPU or process count documented.
- S3-10: four real `make.log`s — the module make line and `CC [M]` objects, no `-j`, no elapsed time, no CPU.
- The same kbuild process chain as `make` (S2-01), at `nproc` rather than a user-chosen `-j`; under a one-CPU affinity mask that is `-j1` (S2-16).

### 23–25. `cpu-batch` — `category_source`, notes, validation wording

- S2-14: interbench Burn = N pthreads spinning continuously (N = online CPUs in code at master, "4 by default" in the man page); Compile = Burn + one write + one read thread inside the interbench process; no process created; "until done" and finite work are not interbench's; the readme table is one run on an unnamed machine.
- S2-15, S3-11: upstream Ananicy types `compiler` = nice 1 for gcc/g++/make/ninja/cargo/rustc/javac/go (README recommends nice 19 for compiling; its `gcc` line is a syntax example with `Heavy_CPU`); CachyOS ships no compiler/make/linker rule after adding and removing them three times (2022, Feb 2024 "avoid freezes with BORE", May 2024 "really noticeable cpu usage … no real benefit"), keeps `ffmpeg` = `Heavy_CPU` (nice 9) and `clamd`/`baloo` = `BG_CPUIO` (nice 16, `SCHED_IDLE`, idle I/O), cgroup quotas cpu80/85/90; S2-13: the kernel's own Kconfig calls build jobs "aggressive CPU burners".
- No source calls interbench "the community's" model (S1 found no literature on it; S2-14).

### 26. `cpu-batch` bindings (`python3`, `ffmpeg`, `HandBrakeCLI`, `clamscan`, `tracker-miner-fs-3`, the `chrome` spoof)

- Thread counts from primary documentation: FFmpeg codec default 1 thread, `auto` = min(affinity-CPUs + 1, 16); x264 auto = 1.5 × affinity-CPUs (S2-18); PyTorch intra-op = physical cores via cpuinfo, not the affinity mask (S2-21); `clamd` `MaxThreads` 10 in multiscan mode only, `clamscan` documents no threading (S2-19); tracker-miner-fs sets `SCHED_IDLE` + nice 19 + idle I/O, plocate `updatedb` daily at Nice=19 / idle I/O, AC power only (S2-22); HandBrake CLI not fetched (S2 Not found T7).
- Observations: S3-06 (Blender CPU renders: durations and machine thread counts, no utilisation); S3-13 (two full `clamscan` runs: 47 569 s over 451.9 GB; 53 min over 7.2 GB; single process; "A LOT of CPU"); S1-07 (Psearchy indexer kernel-time share only); S1-11 (on-access AV overhead in a simulator, Windows XP); S3-18 (tracker "100 % CPU", no numbers).
- Not found: a measured full antivirus scan with utilisation, an indexer's full rescan, x264/ffmpeg or PyTorch utilisation logs (S1 Not found T7; S3 Not found T7), any observation of a single-thread saturating job matching the archetype's shape.

### 27–31. Registry lines

- Corrected wording follows from S1-01 (DynamoRio; no compiler named; single-core run), S1-02 (`cp`, `mkdir`), S2-14 (Burn thread count; Compile emulation) and, for `meas-ci`, from the 9.3 re-analysis and S4 (venue and what a pinned runner can observe).

### T6 addition — a build confined to one CPU

- The only confined-build observation in any class is S1-01's `taskset` row: the serial build on one core takes 3.36× the `-j8` wall, peak PSS lower "because not as many processes run simultaneously"; no process-lifetime or CPU-total comparison.
- Documentation of what confinement does to the tools: affinity inherited across fork/exec (S2-23, S4-16); `nproc`, rpm, ninja, DKMS, ffmpeg, x264 follow the mask, dpkg and PTS do not (S2-16, S2-09, S2-05, S2-12, S2-18, S2-08, S2-20); make's `-l` reads the system-wide running count (S2-03); Python `os.cpu_count()` ignores the mask, `os.sched_getaffinity(0)` honours it (S2-17, S4-16).
- No cgroup / `--cpus` / DVFS paper running `make -jN` across core counts (S1 Not found T6); no `-j1` row in the kcbench material (S3-15, S3-16); no public measurement of a build pinned to one CPU with process counts or CPU totals (S3 Not found T6).

### T8 — what a pinned single-core runner can observe of a build (S4 synthesis, cited)

- Platform: `ubuntu-latest` on a public repository is a fresh 4-vCPU / 16 GB / 14 GB-SSD Azure VM with passwordless sudo (S4-01), image 20260907.300.1, kernel `6.17.0-1022-azure` (S4-02), whose exact config (S4-04, from the `linux-buildinfo-6.17.0-1022-azure` deb) has `CONFIG_TASKSTATS`, `TASK_DELAY_ACCT`, `TASK_IO_ACCOUNTING`, `BSD_PROCESS_ACCT(_V3)`, `PSI` (on by default), `SCHEDSTATS`, `FTRACE`, `BPF_SYSCALL`/`BPF_EVENTS`, `PROC_EVENTS`, `CPUSETS`, `CGROUP_CPUACCT`, `HZ=1000` all `=y`; gcc 13, clang 16–18, make 4.3, ninja 1.13.2 installed; every instrument apt-installable (S4-20).
- Root and switches: everything except `make --trace` and a `/proc` sampler needs root — `kernel.task_delayacct=1` (only tasks started afterwards; S4-05, S4-17), `CAP_SYS_PACCT` (S4-06), `CAP_SYS_ADMIN` for BPF tools and forkstat (S4-11, S4-12), sudo for perf because `CONFIG_SECURITY_PERF_EVENTS_RESTRICT=y` sets `perf_event_paranoid` 4 (S4-21, S4-04; users lower it with `sudo sysctl`, S4-22); `isolcpus=`/`nohz_full=` are boot parameters, unavailable (S4-17).
- Per-process CPU at exit without polling: taskstats (µs; listener on a cpumask that can be exactly the pinned CPU; summed per thread group at the last exit; ENOBUFS loss at high exit rates, remedy a larger buffer and one listener per CPU pinned to it — S4-05) and BSD accounting (ticks, `comp_t` — S4-06). `wait4`/GNU `time` give one aggregate for the wrapped child plus waited-for descendants, i.e. one number for `make` (S4-07).
- Lifetime: taskstats `ac_etime`, BSD `ac_etime`, BCC `exitsnoop` AGE at 0.01 s (S4-11), forkstat's exit "Duration" as user-space arrival arithmetic, "unknown" when the start event was missed (S4-12).
- Blocked on I/O: only delay accounting per process (`blkio_delay_total`, S4-05; `delayacct_blkio_ticks` in `/proc/<pid>/stat` field 42, S4-08); PSI is per cgroup (S4-14).
- Per-schedule run/wait: `perf sched record` + `timehist` with `-w`, `-C <pinned CPU>`, `--state` (S4-09); catches processes of any lifetime; ring-buffer loss ("LOST", `-m`) documented, volume and overhead on one CPU not quantified (S4 Not found).
- The pin's effects: affinity inherited across fork/exec, `nproc` = 1 inside the pin, the workflow's explicit `-j8` unaffected, make applies no load limit without `-l` (S4-16, S4-13); a `/proc` sampler on another CPU still misses processes living between two polls, and no document says how time-sharing on one CPU changes that (S4 Not found); forkstat and taskstats both document loss under high exit rates (S4-12, S4-05).
- Sharing the pinned CPU: `Runner.Listener` / `Runner.Worker` under user `runner`, a separate "Hosted Compute Agent", a Docker server on the image (S4-22, S4-02, S4-03); sudo may `taskset -p` other users' processes or `systemd-run --scope -p AllowedCPUs=` root services (S4-15, S4-16), not kernel per-CPU threads; whether the hosted-compute agent is a movable process is undocumented (S4 Not found).
- Hardware, page cache, disk: GitHub documents the shape, not the CPU model; one vendor's sample shows two Xeon models on the same label with a 26 % single-thread spread (S4-19), so the model is logged per run; `vm.drop_caches` (S4-17); `/sys/block/<dev>/queue/rotational` and the Azure temporary disk at `/dev/disk/azure/resource` (S4-18).
- Not observable: desktop-class hardware, a user's own `-j`, an interactive session, and parallel execution itself — the pin serialises the build by construction on a hypervisor VM (`CONFIG_HYPERV=y`; `cpu_run_real_total` adjusts for stolen time on some architectures, S4-05).

## Not found, all classes

- Per-process lifetime or CPU-time distributions of a Linux kernel build's processes by role (T1): no paper, dataset, log or trace; the nearest are S3-01 (one second, per comm), S1-04 (bash, 2006, means only), S3-03 (invocation counts only).
- CPU time per translation unit for gcc or the kernel (T2): only clang/LLVM data (S3-04, S3-14) and a parse-share scatter on gcc (S1-10).
- A compiler process's blocked-on-I/O time, cold or warm (T2): no observation; only whole-build CPU-boundness (S1-08, S3-04, S3-09, S3-17).
- Make's own CPU cost per dispatched job (T3): no measurement anywhere; Belinassi et al. 2022 unreadable (IEEE challenge page, ResearchGate request-only).
- What `-j` desktop users pick (T4): no survey or poll; the Gentoo forum poll is behind a login.
- DKMS run CPU time, `-j`, duration or process counts (T5): four `make.log`s with objects only (S3-10); nothing with timing.
- A parallel build confined to one CPU with process counts or CPU totals (T6): only S1-01's wall-time ratio; no kcbench `-j1` row; no pinned-build measurement.
- Process-lifetime distributions on Linux desktops (T6): only the 1990s UNIX studies (S1-09; Leland & Ott second-hand); no dataset.
- A measured antivirus full scan with utilisation, an indexer's full rescan, encoder or training utilisation logs (T7): none open; S3-13 gives clamscan durations only.
- On the runner (T8): quantified `perf sched` / `strace` overhead on one CPU; how a `/proc` sampler's censoring changes under time-sharing; forkstat's loss rate; the `CAP_NET_ADMIN` requirement for a taskstats listener (lives in `kernel/taskstats.c`, not fetched); which daemons run on the image and whether the hosted-compute agent is movable; the Azure VM size and disk tier; the live `perf_event_paranoid` / `task_delayacct` / `sched_schedstats` values; USER_HZ; a GitHub statement on CPU variance or dedicated vCPUs; commit ids for files fetched from `main`/`master` raw URLs (pinned by SHA-256 and version strings instead).
- Unreachable or walled on 2026-09-16: github.com HTML, `<owner>/<repo>/raw/…` and api.github.com (403); codeload.github.com tarballs (403 for S3; `git clone` and raw.githubusercontent.com worked); dl.acm.org (403); ieeexplore.ieee.org (202 with a 0-byte challenge body); scholar.google.com (403); api.openalex.org ("Rate limit exceeded"); api.semanticscholar.org (429); export.arxiv.org API (429); dblp.org (Anubis challenge, one 429); researchgate.net (403); openbenchmarking.org (403); git.launchpad.net (403); www.gnu.org (connection reset / no response); git.sesse.net (502 via proxy); forums.gentoo.org (login wall); bugs.debian.org (JavaScript challenge); spinics.net (403); gitlab.gnome.org issue page (406); chromium-build-stats (form only); autobuilder.yocto.io subfolders (404); man7.org proc_pid_schedstat.5 (404); the GitHub MCP file and commit tools for repositories other than this one (denied; S4-22 and S3's code searches used the search endpoint only).
