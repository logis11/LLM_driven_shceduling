# Audit of the meas-ci measurement grounding for the workload dataset

Audited 2026-09-13. Repo HEAD e3d3c9a, read-only. Working files are in `_dev/research/jioh/2026-09-13-verification/meas/`.

Classes: **M** = measured, and my rerun gives the same number · **D** = worked out by the stated arithmetic from measured numbers, and the arithmetic checks · **C** = our own convention or placeholder, not produced by the measurement (says whether the entry admits this) · **X** = the number does not match, or the description contradicts what the workflow or method actually measured.

---

## X items (summary)

1. **The compiler "child" is a compiler-family process, not a make job and not a cc1.** `compiler_children` ≈ 11.9k per build. That is about 2,990 `gcc` + 2,970 `cc1` + 2,950 `as` + 2,890 `fixdep` + about 110 others, so roughly 4 processes per translation unit (analyze.py:25-26, 229-237). cc1 carries 99% of the sampled compiler CPU.
   - Mean CPU per cc1 exit is about 245–394 ms, and that is still a lower bound. The pooled mean "cpu/child" is 90 ms.
   - Timelines bind `child_name: cc1` (c1-compile.timeline.yaml:15 and others). `build-orchestrator` states a default spawn count of 2,430 from the literature (archetypes.yaml:247-248). Both are paired with a per-family-member CPU figure, so CPU per cc1 is understated about 4×.
   - The lifetime fit (median about 100 ms, sigma_log 2.37) spans two clusters: gcc/cc1 at about 0.7–0.95 s, and as/fixdep at about 7–15 ms. The `gcc` driver's lifetime nests around cc1 and as, so the same time is counted twice.
2. **compiler-child `disk_wait` median 3,600 µs is not a disk-wait measurement.** It equals 103,397 − 99,801 = 3,596 µs: the cold-build median of per-repeat lifetime medians minus the warm-build median. No I/O-wait quantity was measured.
   - Sampled `D` (disk-sleep) state makes up 0.03–0.11% of compiler-family observations in both builds.
   - The warm per-repeat lifetime medians alone span 76.9–105.7 ms.
   - The note (archetypes.yaml:216-218) says "per-child disk waits are noise-bounded at ~4 ms on runner NVMe" and calls 3.6 ms "that measured bound". Runner disk type is not recorded anywhere.
3. **Voluntary context switches count the main thread only, but CPU counts all threads.** proc_sampler.py:46-54 reads `/proc/<pid>/status`. In the kernel, `task_context_switch_counts()` prints `p->nvcsw` for that one task (fs/proc/array.c v6.17:398-404, called at :462). `utime`/`stime` from `/proc/<pid>/stat` come from `thread_group_cputime_adjusted()` over all threads (array.c:571-572, `proc_tgid_stat` → `do_task_stat(...,1)` :677-680).
   - So every `work_us` = (whole-process CPU) ÷ (main-thread wakes), and every `gap_us` = span ÷ (main-thread wakes).
   - Processes affected: the tracker miner (10 threads), chrome browser (36), Element main process (27–28), multipathd and udisksd (7). This feeds background-crawler, electron-comms and system-daemon.
4. **electron-comms (Element) has no Element renderer at all.** In all 5 repeats, the Element processes are: main process, GPU process, network service, zygotes and a broker. No `--type=renderer` process appears (forkstat cmdlines).
   - The 15 fitted processes are 5 main processes (gap 0.40–0.43 s) plus 10 GPU/network helpers (gap 3.84–3.92 s).
   - "Median 1.85 s" is the geometric mean falling between these two clusters. No process wakes near 1.85 s, and the plain median is 3.86 s.
   - "Cpu-per-wake 289 µs" is the same kind of in-between value (helpers 128–197 µs, main 531–857 µs).
5. **"Idle chromium renderers wake at median ~1.61 s" is not a renderer set** (archetypes.yaml:472-474). The 50 fitted processes are every process whose name starts with `chrom`/`chrome` and that lived ≥5 s with ≥5 wakes. Per repeat that is the browser (~55–66 ms gap), 2 zygotes, the GPU process, network and storage services, and 3–4 renderers.
6. **"Chromium at 10 file tabs peaked at 21–22 processes" is a launch transient** (archetypes.yaml:475-476).
   - The peak is one 200 ms sample, 2.4–3.0 s after launch, in every repeat.
   - After that the count holds at 11, including 2 `chrome_crashpad` handlers that the `chrom` prefix also matches.
   - The 11 renderers created for the tabs (renderer-client-id 6–16) all exited within about 0.35 s in all 5 repeats. Three long-lived renderers (id 5 WebUI, 17, 19) remain.
   - Likely cause, not verified: snap confinement gives Chromium a private `/tmp`, so `file:///tmp/tabs/*.html` (meas-gui.yml:44-46, 66) does not resolve.
7. **The background-crawler run shows no evidence of indexing.** The miner used 3, 22, 11, 18 and 25 clock ticks (30–250 ms of CPU) in 300 s. `tracker-extract-3` ran for only about 10 s (16 s after miner start, in r1; about 9.5 s of sampled span in r2).
   - The note's "indexing a corpus copy … self-paced wake structure across index + idle" (archetypes.yaml:321-325) is not supported.
   - `scan_burst` and `throttle` are a lognormal fit over **n = 5** per-process averages (one per repeat), and those averages are tick-quantized.
8. **Sampling declarations do not match what the distributions describe.** These params are declared `per-iteration`:
   - background-crawler scan_burst and throttle
   - electron-comms heartbeat_work
   - system-daemon idle_gap and wake_burst

   But each fitted sigma is the spread **across processes** (or across repeats) of per-process averages. No distribution of individual wakes or gaps was measured.
   - system-daemon idle_gap sigma 1.9 is the heterogeneity between daemons (chronyd 0.25 s … systemd-udevd 120.6 s).
9. **system-daemon `wake_burst` 155 µs comes from 29 of 51 processes.** `lognormal_fit` drops zero values (analyze.py:81), and 22 daemons had 0 CPU ticks. Including them, the plain median is 62 µs. The remaining values are 1–20 ticks divided by the wake count.
10. **io-stream "compressing streams ~0.73" is a cli:1 number under a cli:3 tag.** cli:1 `untar_proc_duty` = 0.733. cli:3 (the cited batch) = 0.684 (range 0.670–0.754). The value is also the median of two processes, i.e. the mean of the tar duty (~0.47) and the xz duty (~1.0).
11. **network-bulk "saturating the runner link" is not measured.**
    - The download phase lasted 0.6–4.7 s.
    - Phase-level wget duty over 5 repeats was 0.014–0.571 (median 0.184).
    - The cited 0.0565 is the median of n = 2 values: 4 ticks over 3 s, and 40 ticks over 4 s.
    - No throughput was recorded.
12. **build-orchestrator `dispatch_overhead` is a mean, and it is divided by grandchildren.** The formula is sampled make CPU ÷ execs of 12 compiler-family names (analyze.py:240-242). That count includes cc1/as spawned by gcc and fixdep spawned by the shell.
    - The value is a ratio of totals (a mean) but is stored in `median_us`; with sigma 0.5 the implied mean is 265 µs.
    - "Make's own cpu time per spawned child" (archetypes.yaml:252-253) overstates the number of make children about 4×.
    - "Fork rate ~24 children/s" is the exec rate of compiler-family names.
13. **"Lifetime log-std overshot the mean 2.4×" does not reproduce.** With the cited warm sigma_log 2.366 it is 2.62×. 2.4× only comes out with σ = 2.329, the cold-build minimum (archetypes.yaml:213-214).
14. **Name verification is weaker than the docs claim** (§4):
    - `tracker-miner-fs-3` never appears as a process name: comm is truncated to `tracker-miner-f`, and on Arch no binary was found.
    - The level logic marks `runtime` without the catalog name being observed (cc1 on Arch observed only `gcc`), and marks `binary-only` with an empty binary list.
    - `clamscan` and `make` were observed at runtime only on Ubuntu in names:1.
15. **Stale or contradictory docs:**
    - docs/references.md:280 still says `meas-ci` is "reserved (no runs yet …)".
    - building-plan.md:61,65-67 and archetype-plan.md:53,58,64-66 still say `meas-pending`.
    - building-plan.md:183 says "1 s /proc state sampler" and "exact fork/exec/exit timestamps". Actual: 0.5 s / 0.2 s sampling; forkstat timestamps are whole seconds and durations are 1 ms.
    - dataset/README.md:130 says raw data is on "the GitHub release named in the tag's registry entry", but dataset/sources.yaml:265-273 names no release.
    - The release title says "cli:1, gui:2, names:1" and _dev/TODO.md:31 says "cli:1 … 11/15 folded". Both are superseded by cli:3 and 15/15.
    - The release notes say cli:1 is "cited nowhere", but system-daemon's notes cite it (archetypes.yaml:511-512).
16. **`tar-read-cold` does not read file contents.** `tar -cf /dev/null` (meas-cli.yml:88): GNU tar's `file_dumpable_p` returns false for regular files when `dev_null_output` is set (tar src/create.c, comment "b) current archive is /dev/null"). The phase takes 1.5 s against 17–24 s for the cold rsync of the same tree. Not cited by any archetype, but `tar_cold_duty` 0.386 in summary.json is not a read-stream duty.

---

## 1. Reproduction

### 1.1 Release `meas-ci-2026-08-28` inventory

| Asset | Workflow run | Run number | Head commit | Repeats | Runner (from spec.json) |
|---|---|---|---|---|---|
| `meas-cli3.zip` | 33144766132 | cli **3** | 246ddd4 | r1–r5, each: spec.json, phases.jsonl, lifecycle.log (~394 MB), proc_samples.jsonl (70–87 MB), sidecar start/stop | Ubuntu 24.04.4, kernel `6.17.0-1022-azure`, nproc 4, 16 GB. **CPU model differs:** r1–r3 AMD EPYC 9V74, r4–r5 AMD EPYC 7763 |
| `meas-gui.zip` | 33139471432 | gui **2** | 72db68b | r1–r5, same file set (proc_samples ~98–104 MB) | Same OS and kernel. **CPU:** r1–r3 EPYC 7763, r4 Intel Xeon 6973P-C, r5 Intel Xeon Platinum 8573C |
| `meas-names.zip` | 33067225138 | names **1** | c1d80a4 | ubuntu, fedora, arch: spec.json + names-<distro>.json | Containers `ubuntu:24.04`, `fedora:41`, `archlinux:latest` (20260823) on a 6.17.0-1022-azure host |
| `meas-cli.zip` | 33067219710 | cli **1** (superseded) | c1d80a4 | r1–r5 (11 warm phases only, 1 s sampler, no context-switch counters) | EPYC 7763 |

Cited runs, checked against the release and the Actions API (`gh run list`):
- `meas-ci:cli:3`: **present**.
- `meas-ci:gui:2`: **present**.
- `meas-ci:names:1`: **present**. The repo's `dataset/meas/names/names-*.json` are byte-identical to the release.
- **`meas-ci:names:2` is NOT in the release.** It is cited in c7.variant.yaml:17, coreset-guide.md:930, the 2026-09-10 memo and `dataset/meas/names/run-2/`. Source is run 34466009254 at 2273feb. I downloaded its Actions artifacts: the three tables are byte-identical to `dataset/meas/names/run-2/`, and its spec.json confirms run number 2. The repo keeps no spec.json for names:2, and the artifacts expire 2026-12-09.
- cli:2 (run 33142895691) and gui:1 (run 33067222560, failed) exist as runs, are cited nowhere, and are not released.
- The workflow and tool files at each run's head commit match HEAD: meas-cli.yml at 246ddd4, meas-gui.yml at 72db68b, meas-names.yml and verify_names.py at 2273feb. Between c1d80a4 (names:1) and HEAD, the only change is the added `dkms` candidate. analyze.py at HEAD differs from 246ddd4 only in the across-repeat aggregation.

### 1.2 Rerun
Layout: `run_cli3/{cli → cli3/meas-cli-r1..5, gui → gui/meas-gui-r1..5}`. Command: `python3 analyze.py run_cli3 --json out_cli3.json` with HEAD analyze.py, Python 3.13.0, 95 s.

**Result: `out_cli3.json` is byte-identical to `dataset/meas/summary.json`** (SHA1 106633e2…, `cmp` clean). All 1,083 leaf fields reproduce, per-repeat blocks included; 0 differ.

Control: running on cli:1 + gui:2 instead gives 408 differing leaves (e.g. compiler_cpu_mean 56,610 vs 89,997). The summary is unambiguously cli:3 + gui:2.

---

## 2. Method audit (from workflow files, tools, spec.json and raw data, not repo prose)

### 2.1 What the workflows ran
- **meas-cli (cli:3):** 5-way matrix, one runner per repeat (meas-cli.yml:28). Phases in order (meas-cli.yml:61-108), with phase wall times from phases.jsonl across r1–r5:
  - idle-baseline `sleep 60`
  - network-bulk: `wget` of cdn.kernel.org `linux-6.6.tar.xz`, 0.6–4.7 s. No mirror fallback ran: no `wget` exec of mirrors.edge in lifecycle.log.
  - download-verify: `xz -t`, 6–7.7 s
  - untar, 7.2–9.0 s
  - `make defconfig`
  - **kernel-build-j8: `make -j8` on nproc 4**, 399–528 s
  - archive-tar-xz, 170–208 s
  - rsync-copy (warm), 6.2–8.6 s
  - `sudo updatedb` (whole filesystem, not the corpus), 2.0–2.5 s
  - locate-query **rc=1 in all repeats**
  - freshclam **rc=2 in all repeats**
  - clamscan `-r -i linux-6.6/Documentation`, 70–91 s, rc 0
  - cold section with `vm.drop_caches=3` before each step:
    - tar-read-cold, 1.5–1.7 s
    - rsync-copy-cold, 17–24 s
    - clamscan-cold, 78–100 s
    - updatedb-cold, 17–21.5 s
    - kernel-clean
    - kernel-build-cold `-j8`, 386–527 s
  - tracker-daemon: copies Documentation into `$HOME/Documents/corpus`, then runs `timeout 300 dbus-run-session -- tracker-miner-fs-3 || true`, so **rc is always 0** (meas-cli.yml:108). Wall 301.4–302.1 s.
- **meas-gui (gui:2):**
  - `snap install chromium`, run as `xvfb-run -a snap run chromium --no-sandbox --no-first-run --disable-gpu` with 10 `file:///tmp/tabs/tabN.html`, `sleep 300` (meas-gui.yml:67-71). Phase 303 s.
  - Element Desktop (packages.element.io apt) run as `xvfb-run -a element-desktop --no-sandbox --disable-gpu`, unauthenticated, `sleep 600` (meas-gui.yml:72-76). Phase 603 s.
- **meas-names:** three containers, one job each, no repeats. Package install is best-effort, then `verify_names.py`.

### 2.2 Instruments
| Instrument | What it records | Resolution |
|---|---|---|
| forkstat `-e fork,exec,exit,comm`, run as root (meas-cli.yml:50-51, meas-gui.yml:52-53) | One line per event: `HH:MM:SS event pid info duration cmdline`. Exit durations count from fork. **Thread** exits are logged too (renderer-client-id groups show one line per thread). | Timestamps in **whole seconds**; durations printed `%5.3f` in s/m/h units. analyze.py's `_DUR` regex (`…s`, analyze.py:32) silently drops durations printed in minutes/hours (≥60 s). I checked: 0 compiler-family exits were dropped. |
| proc_sampler.py | Per sample: every `/proc/<pid>/stat` (thread-group `utime+stime`, `threads`, `state`, `starttime`), plus with `--ctxt` the voluntary/nonvoluntary switches of the **main thread only** (see X3) | cli:3 `--interval 0.5` (measured median 500.2 ms, p99 525–530 ms); gui:2 `--interval 0.2` (median 200 ms, p99 201–202 ms). Docstring still says "1 s" (proc_sampler.py:2). |
| CPU ticks | `TICK_US = 10_000` (analyze.py:23) | Correct for x86 (`__USER_HZ 100`, include/uapi/asm-generic/param.h). The comment "spec.json corroborates" is false: runner_spec.py:37-47 records no clock-tick value. |
| Phase windows | `hms_us` truncates epoch µs to **integer seconds-of-day** (analyze.py:47-49). `in_phase` is inclusive on both ends. | Windows bleed up to about 1 s into neighbouring phases. Seen: the download-verify window catches the network-bulk wget; the untar window catches download-verify's xz. `phase_wall_us` (the divisor for duty) is exact µs, but the tick numerator uses the integer window. Spans in `per_proc_duty`/`wake_stats` are whole seconds (analyze.py:181, 207), so single-thread duties come out above 1 (clamscan r4 1.006) and 5 s spans carry up to ±20% error. |

### 2.3 Each measured quantity: what it actually is
| summary.json field | Actual definition (code) | Censoring and caveats |
|---|---|---|
| `compiler_lifetime` {median_us, sigma_log, p90} | Lognormal fit over all forkstat exit durations whose `basename(argv0)` is in COMPILER_NAMES (`cc1 cc1plus gcc g++ as ld collect2 objtool fixdep objcopy genksyms modpost`) and whose birth (exit second − duration) falls in the build window. Floor 1 ms (analyze.py:96-115, 229-230). | Per-event values, pooled over roles. Per-name geometric medians for cli:3 r1 warm: gcc 860 ms (n 2991), cc1 841 ms (2973), as 9.1 ms (2951), fixdep 14.8 ms (2890), ld 16 ms (53), objcopy 6.7 ms, collect2 39 ms, objtool 12 ms, modpost 4.3 s. |
| `compiler_children` | Count of those exits | ≈ 4 per translation unit, not per make job |
| `compiler_cpu_mean_us` | Σ over compiler procs of (last − first sampled ticks) × 10 ms ÷ number of lifetimes (analyze.py:140-160, 235) | The numerator is censored: CPU before a process's first sample and after its last is lost, and processes that live < 0.5 s mostly vanish. The denominator is not censored. cc1 = 99% of the numerator. |
| `compiler_life_mean_us` | Arithmetic mean of the lifetimes | Pooled roles, nested gcc ⊃ cc1 |
| `compiler_peak_concurrent` | Maximum per sample of live compiler-family processes | 16 in every repeat = 8 jobs × (gcc + cc1). Peak live cc1 = 8. |
| `make_dispatch_us` | Sampled CPU of all `make` processes (recursive makes included) ÷ count of compiler-family **execs** in the window (analyze.py:240-242) | Ratio of totals (a mean); the denominator includes grandchildren |
| `fork_rate_hz` | Compiler-family execs ÷ build wall seconds | Exec rate, not fork rate |
| `<phase>_duty` | Sampled CPU of the matching comm set ÷ exact phase wall | Sums several processes (rsync 3 roles → 1.24; tar + xz → 1.36) |
| `<phase>_proc_duty` | **Median over processes** (span ≥ 3 s) of each process's CPU ÷ span | rsync = median of generator/sender/receiver (warm r1: 0.307 / 0.146 / 0.994; cold r1: 0.256 / 0.065 / 0.445). untar = mean of tar ≈ 0.47 and xz ≈ 1.04. Null when the phase is < 3 s (warm updatedb). |
| `tracker`, `element`, `chromium`, `daemons` {gap, work} | Per process (span ≥ 5 s, ≥ 5 voluntary wakes): gap = span_s ÷ Δvctxt, work = Δticks × 10 ms ÷ Δvctxt. Then a lognormal fit **across processes**, zero-valued entries dropped from the median/sigma (analyze.py:81) but **kept in p90** (analyze.py:87). | Main-thread wakes vs whole-process CPU (X3). Tick-quantized. One value per process, not per wake. |
| `chromium_peak_procs` | Maximum per sample of processes whose comm starts with `chrom`/`chrome` | Launch transient (X6); includes crashpad handlers |

---

## 3. The 15 `meas-ci` params

Derivations use the reproduced summary. Warm/cold medians below are the across-repeat medians.

| Location | Stored | Reproduced / derived | Class | Note |
|---|---|---|---|---|
| archetypes.yaml:183 compiler-child `cpu_burst.median_us` | 12900 | 0.9 × (89,997 / 625,335 × 99,801) = 0.9 × 14,363 = 12,927 | D (split is C, labeled "ours" at :214) · **X** unit | Arithmetic checks. The inputs describe a pooled compiler-family member; timelines bind the child as `cc1`, whose own sampled CPU per exit is 245–394 ms (X1). |
| archetypes.yaml:183 `cpu_burst.sigma_log` | 1.91 | √(2·ln 6.266) = 1.916 (1.914 with the rounded 6.25) | D | |
| archetypes.yaml:186 `cpu_tail.median_us` | 1440 | 0.1 × 14,363 = 1,436 | D (split C, labeled) | |
| archetypes.yaml:186 `cpu_tail.sigma_log` | 1.91 | same as burst | D | Burst and tail sampled independently keep the mean (means add); the median of their sum is not 14.4 ms. |
| archetypes.yaml:189 `disk_wait.median_us` | 3600 | 103,397 − 99,801 = 3,596 | **X** | A difference of lifetime medians between builds, inside the warm spread (76.9–105.7 ms). Not a wait. D-state share 0.03–0.11% (X2). |
| archetypes.yaml:189 `disk_wait.sigma_log` | 0.8 | none | C, **unlabeled** | The note labels only the shape and family as ours |
| archetypes.yaml:182-190 sampling | per-instance ×3 | spawn table | consistent | |
| archetypes.yaml:234 build-orchestrator `dispatch_overhead.median_us` | 234 | `make_dispatch_us` median 234 (r1); per repeat 183 / 230 / 234 / 257 / 262 | M · **X** semantics | A mean stored as a median; divided by compiler-family execs (X12) |
| archetypes.yaml:234 `dispatch_overhead.sigma_log` | 0.5 | none | C, labeled (:254-255) | |
| archetypes.yaml:235 sampling | per-iteration | one ratio per repeat; no per-dispatch distribution | C (sigma labeled) | |
| archetypes.yaml:269 io-stream `block_cpu.median_us` | 3000 | none | C, labeled (:287) | |
| archetypes.yaml:269 `block_cpu.sigma_log` | 0.6 | none | C, labeled | |
| archetypes.yaml:272 `io_wait.median_us` | 10000 | 3,000 × (1/0.231 − 1) = 9,987 | D | 0.231 = `rsync_cold_proc_duty` (M). It is the median of rsync's 3 process roles, so the "wait" includes pipe waits between them; the busiest role runs 0.42–0.45 cold. Writes are not cache-defeating (no fsync). |
| archetypes.yaml:272 `io_wait.sigma_log` | 0.6 | none | C, labeled | |
| archetypes.yaml:304 background-crawler `scan_burst.median_us` | 1608 | `tracker.work.median_us` 1608 | M · **X** | n = 5 per-process averages; whole-process CPU ÷ main-thread wakes; ticks per repeat 3 / 22 / 11 / 18 / 25 (X3, X7) |
| archetypes.yaml:304 `scan_burst.sigma_log` | 0.639 | 0.639 | M · **X** sampling | Spread across 5 repeats, declared per-iteration (X8) |
| archetypes.yaml:307 `io_wait.median_us` | 5870 | 1,608 × (1/0.215 − 1) = 5,871 | D | 0.215 = `updatedb_cold_proc_duty` (M). updatedb crawls the whole filesystem (three kernel trees plus the OS). |
| archetypes.yaml:307 `io_wait.sigma_log` | 0.6 | none | C, labeled (:327-328) | |
| archetypes.yaml:310 `throttle.median_us` | 3800000 | `tracker.gap.median_us` 3,801,982 | M · **X** | 300 s ÷ main-thread wakes of an essentially idle miner (X7) |
| archetypes.yaml:310 `throttle.sigma_log` | 0.428 | 0.428 | M · **X** sampling | n = 5 (X8) |
| archetypes.yaml:417 network-bulk `chunk_cpu.median_us` | 1000 | none | C, labeled (:433-434) | |
| archetypes.yaml:417 `chunk_cpu.sigma_log` | 0.5 | none | C, labeled | |
| archetypes.yaml:420 `net_wait.median_us` | 16700 | 1,000 × (1/0.0565 − 1) = 16,699 (16,544 with the note's rounded 0.057) | D · **X** grounding | Input n = 2: 4 ticks / 3 s (r3) and 40 ticks / 4 s (r5). Phase-level duty 0.014–0.571. No link saturation measured (X11). |
| archetypes.yaml:420 `net_wait.sigma_log` | 0.5 | none | C, labeled | |
| archetypes.yaml:451 electron-comms `heartbeat.median_us` | 1850000 | `element.gap.median_us` 1,848,645 | M · **X** | Two clusters: main process 0.40–0.43 s (5) and GPU/network helpers 3.84–3.92 s (10); no renderer (X4) |
| archetypes.yaml:451 `heartbeat.sigma_log` | 1.09 | 1.088 | M · **X** | Spread between the two clusters |
| archetypes.yaml:452 sampling | per-task | one value per process | consistent | Assigning one period per task matches what was measured (a per-process average) |
| archetypes.yaml:454 `heartbeat_work.median_us` | 289 | 289 | M · **X** | Helpers 128–197 µs (2–3 ticks each), main 531–857 µs |
| archetypes.yaml:454 `heartbeat_work.sigma_log` | 0.713 | 0.713 | M · **X** sampling | Across-process spread declared per-iteration |
| archetypes.yaml:493 system-daemon `idle_gap.median_us` | 11240000 | `daemons.gap.median_us` 11,239,013 | M · **X** sampling | 51 per-daemon means; processes with < 5 wakes excluded; main-thread wakes only |
| archetypes.yaml:493 `idle_gap.sigma_log` | 1.9 | 1.898 | M · **X** sampling | Heterogeneity between daemons, applied per-iteration |
| archetypes.yaml:496 `wake_burst.median_us` | 155 | 155 (n = 29) | M · **X** | 22 of 51 zero-tick daemons dropped; median including them is 62 µs (X9) |
| archetypes.yaml:496 `wake_burst.sigma_log` | 0.809 | 0.809 | M · **X** | |

### 3.1 Measured numbers quoted in `modeling_notes`

| Location | Stored text | Reproduced / derived | Class | Note |
|---|---|---|---|---|
| archetypes.yaml:205-206 | "linux-6.6 defconfig, make -j8, 5 repeats" | meas-cli.yml:28, 64, 76-77 | M | Also true and unstated: nproc 4, so -j8 = 2× cores; CPU model mixed across repeats |
| :206-207 | "~11.9k compiler-family children per build" | 11,883 (11,835–11,914) | M · **X** vs bindings | ≈ 4 per translation unit; compare spawn_count 2,430 (:247-248) and `child_name: cc1` |
| :207 | "lifetime median ~100 ms" | 99,801 | M · **X** description | Pooled two-cluster mixture, nested gcc ⊃ cc1 |
| :207-208 | "sigma_log ~2.37" | 2.366 | M | |
| :208-209 | "500 ms sampler" | meas-cli.yml:52; measured 500 ms | M | |
| :209 | "mean cpu/child ~90 ms … lower bound" | 89,997 | M | Lower-bound wording is correct; per cc1 it is ~358 ms (r1) |
| :210-211 | "4-core utilization bound ~165 ms" | 4 × wall / children: 134–178 ms per repeat; 167.9 from the medians | D (approximate) | |
| :211 | "median cpu … ~14.4 ms" | 14,363 | D | |
| :212 | "mean/median = 6.25" | 6.266 | D | |
| :213-214 | "overshot the mean 2.4x" | 2.62× with σ 2.366 | **X** | 2.4× only with σ = 2.329 (cold minimum) (X13) |
| :215-216 | "cold-cache rebuild statistically identical (cpu and lifetime means within repeat spread)" | cold cpu_mean 91,465 inside warm 61,620–98,793; cold life_mean 633,185 inside 499,646–669,059 | M | |
| :216-218 | "disk waits noise-bounded at ~4 ms on runner NVMe; median 3.6 ms is that measured bound" | 3,596 = difference of medians | **X** | No I/O-wait measurement; disk type not recorded (X2) |
| :247-248 | "kernel-build default is 2,430 (ocallahan-atc17)" | literature, not meas-ci | n/a · **X** vs meas unit | The same build measured ≈ 2,990 gcc invocations and ≈ 11.9k compiler-family processes |
| :253-254 | "5-repeat medians 183-262 us" | per-repeat ratios 183–262 | M (wording) | Each is a ratio of totals, not a median |
| :254 | "observed fork rate ~24 children/s at -j8" | 24.2 (22.8–30.1) | M · **X** description | Exec rate of compiler-family names |
| :290 | "0.231 (spread 0.155-0.267)" | 0.231 (0.155–0.267) | M | |
| :291 | "~10 ms" | 9,987 | D | |
| :291-292 | "warm-cache rsync runs 0.276" | 0.276 | M | |
| :292 | "compressing streams ~0.73" | cli:3 0.684 (0.670–0.754); cli:1 0.733 | **X** | Stale cli:1 value (X10) |
| :321-323 | "300 s per repeat (5 repeats, one miner process each)" | timeout 300; wall 301–302 s; procs = 5 | M | |
| :322 | "indexing a corpus copy" | miner CPU 30–250 ms per 300 s | **X** | (X7) |
| :323-325 | "~1.6 ms sigma_log ~0.64 … ~3.8 s sigma_log ~0.43" | 1,608 / 0.639 / 3,801,982 / 0.428 | M · **X** semantics | |
| :326 | "cold-cache updatedb duty 0.215 (spread 0.147-0.244)" | 0.215 (0.147–0.244) | M | |
| :327 | "~5.9 ms" | 5,871 | D | |
| :329-330 | "clamscan per-proc duty ~1.0 warm AND ~0.98 cold" | 0.999 / 0.976 | M | freshclam rc = 2 every repeat, so the signature DB state is unrecorded; clamscan rc = 0 |
| :317 validation_stats | "burst/idle duty cycle of updatedb + clamscan runs" | — | note | Contradicts :330 ("the daemon-mode run is the only valid pacing referee") |
| :435-436 | "~0.057, wide spread 0.013-0.1 … only 2 of 5 repeats" | 0.0565 (0.013–0.100), n_repeats 2 | M | Honest about n |
| :436 | "saturating the runner link" | not measured | **X** | (X11) |
| :437 | "~16.7 ms" | 16,699 | D | |
| :468-470 | "15 processes across 5 repeats … ~1.85 s sigma_log ~1.09, cpu-per-wake ~289 us" | 15 / 1,848,645 / 1.088 / 289 | M · **X** | No Element renderer; two clusters (X4) |
| :472-474 | "idle chromium renderers wake at median ~1.61 s sigma_log ~1.72" | 1,609,098 / 1.718 (n = 50) | M numbers · **X** description | Not renderers (X5). The "no split warranted" judgement rests on geometric means of mixed process sets. |
| :475-476 | "Chromium at 10 file tabs peaked at 21-22 processes" | 21–22 | M number · **X** meaning | One transient sample; steady state 11; tab renderers died at ~0.35 s (X6) |
| :508-510 | "sampled at 200 ms with ctxt counters … 51 processes across 5 repeats" | meas-gui.yml:54; procs 51 | M | |
| :510-511 | "~11.2 s sigma_log ~1.9, cpu-per-wake ~155 us" | 11,239,013 / 1.898 / 155 | M · **X** | (X8, X9) |
| :511-512 | "cli:1 idle-baseline corroborates near-zero daemon cpu at 1 s sampling" | Not in summary.json. Ad hoc on the release: daemon CPU 10–40 ms per 60 s in cli:1 (1 s sampler at c1d80a4), 20–30 ms in cli:3 | M (ad hoc) | The release notes call cli:1 "cited nowhere" |

### 3.2 Measured numbers and claims in docs and other dataset files

| Location | Stored text | Check | Class | Note |
|---|---|---|---|---|
| docs/references.md:278 | "workflow files and raw outputs released in the artifact" | names:2 raw files not in the release | **X** (partial) | |
| docs/references.md:280 | "status: reserved (no runs yet; `meas-pending` placeholders…)" | 15 params cite meas-ci | **X** stale | |
| dataset/sources.yaml:265-273 | Scope note; no release named | — | note | |
| dataset/README.md:19 | "names/: run 1; names/run-2/: the Phase 7 dkms run" | names:1 files = release; run-2 files = run 34466009254 artifacts | M | |
| dataset/README.md:130 | "raw data lives on the GitHub release named in the tag's registry entry" | the registry entry names no release | **X** | |
| building-plan.md:183 | "exact fork/exec/exit timestamps … 1 s /proc state sampler" | forkstat is second-resolution; sampler 0.5 s / 0.2 s | **X** | |
| building-plan.md:61, 65, 66, 67; archetype-plan.md:53, 58, 64, 65, 66 | "`meas-pending`" | archetypes cite meas-ci | **X** stale | |
| scenario-catalog.md:36 | name workflow "confirms each name as it actually appears in comm/cmdline across distro containers (… updatedb vs updatedb.plocate, cc1 visibility)" | see §4 | **X** (overstated) | |
| coreset-guide.md:162, 505 | c1-compile children "총 3.84 s, 중앙값 18.5 ms, 최대 478 ms, SLEEP 중앙값 3.6 ms … 출처는 meas-ci의 실제 kernel build 측정" ("total 3.84 s, median 18.5 ms, max 478 ms, SLEEP median 3.6 ms … the source is meas-ci's real kernel-build measurement") | These are compiled draws from the archetype params, not measured values (not re-derived here) | C (wording implies measurement) | The per-child definition issue (X1) carries through |
| coreset-guide.md:182 | "1.6 ms 일하고 5.9 ms 기다리고 3.8 s 쉼" ("works 1.6 ms, waits 5.9 ms, rests 3.8 s") | matches params | D | Inherits X7 and X8 |
| coreset-guide.md:211 | "heartbeat … 중앙값 1.85 s, sigma 1.09" ("heartbeat … median 1.85 s, sigma 1.09") | matches | M · **X** | Inherits X4 |
| coreset-guide.md:217 | "SLEEP 중앙값 11 s (sigma 1.9), RUN ~155 µs" ("SLEEP median 11 s (sigma 1.9), RUN ~155 µs") | matches | M · **X** | Inherits X8 and X9 |
| c7.variant.yaml:7-8; c2-pairs.variant.yaml:16-17 | clamscan full-scan state CPU-saturating (meas-ci:cli:3) | per-process duty 0.999 warm / 0.976 cold | M | Scanned text docs with a DB whose provenance is unrecorded (freshclam failed) |
| c7.variant.yaml:15-18; coreset-guide.md:930 | dkms: names:2 observed comm `dkms` at runtime on all three distros; Fedora ships a kernel-install hook and dkms.service | names:2 tables: `runtime` with observed `dkms` on ubuntu, fedora and arch; Fedora binaries include `/usr/lib/kernel/install.d/40-dkms.install` and `/usr/lib/systemd/system/dkms.service` | M | Raw data outside the release |
| analyze.py:23 | "USER_HZ=100 on the runners (spec.json corroborates)" | value correct by kernel ABI; spec.json has no such field | C (mislabeled evidence) | |
| _dev/TODO.md:31; release title | "cli:1/gui:2/names:1; 11/15 folded" | cli:3, 15/15 | **X** stale | |

---

## 4. Name verification (`dataset/meas/names/`, meas-names.yml)

**What the instrument does** (verify_names.py):
- For each candidate: install the package, list the package manifest filtered to paths containing `/bin/`, `/libexec/` or `/lib/` (:185-186; this drops `/usr/sbin/`, e.g. the dkms binary on Ubuntu).
- If a run command exists, run it while a thread polls `/proc/*/comm` every ~5 ms and records comms starting with the watch prefixes (:136-159, 216-218).
- **Level logic (:241-248):**
  - `runtime` if *any* watch prefix was seen, even when the catalog name itself was not.
  - Otherwise `binary-only`, even when the run was attempted and nothing was seen (`observed: {}`), and even when the binary list is empty.
  - The thunderbird note "recorded as found only if a real binary ships" (:109-110) is not implemented.
  - Short `--version` processes often exit before the 5 ms poll sees them, so the level flips between runs (make, tar, xz on Ubuntu: `runtime` in names:1, `binary-only` in names:2).

**Distros:** Ubuntu 24.04, Fedora 41, Arch (image 20260823), all as containers. names:1 = 22 candidates; names:2 = 23 (adds dkms). Both list 20 names as `not_attempted`.

**Timeline names versus verification output** (names used in dataset/timelines/coreset/*.yaml):

| Name (use count) | names:1 (u / f / a) | names:2 (u / f / a) | Other runtime evidence | Verdict |
|---|---|---|---|---|
| `dkms` (1, C7) | — | runtime, observed `dkms` / runtime / runtime | — | **Verified** as claimed |
| `clamscan` (22) | runtime (observed) / binary-only, not observed / binary-only, not observed | binary-only, not observed ×3 | comm `clamscan` in meas-cli samples (Ubuntu runner) | Seen at runtime on Ubuntu only |
| `make` (4) | runtime / not observed / not observed | not observed ×3 | comm `make` in meas-cli | Ubuntu only |
| `cc1` (5, `child_name`) | observed `cc1` / observed `cc1` / **only `gcc` observed**, level still `runtime` | same | comm `cc1` in meas-cli | Ubuntu and Fedora; **not Arch** |
| `soffice.bin` (4) | observed on all three | observed on all three | — | Verified |
| `tracker-miner-fs-3` (4) | binary-only (4 paths) / binary-only (6) / binary-only with **0 binaries** | same | Runtime comm on the Ubuntu runner is **`tracker-miner-f`** (15-character truncation); cmdline shows `/usr/libexec/tracker-miner-fs-3` | Binary exists on Ubuntu and Fedora; **not found on Arch**; never appears as a comm |
| `baloo_file` (1) | binary-only (4) / binary-only with **0 binaries** / binary-only (2) | same | — | Binary on Ubuntu and Arch only |
| `wineserver` (7) | binary-only; Ubuntu ships only `/usr/bin/wineserver-stable` | same | — | Plain name `wineserver` found on Fedora and Arch only |
| `gamescope` (3) | package-not-found / binary-only / binary-only | same | — | Not on Ubuntu |
| `HandBrakeCLI` (3), `ffmpeg` (3) | runtime / package-not-found / runtime | same | — | Ubuntu and Arch |
| `borg` (4), `python3` (3), `mpv` (3) | runtime on all three | runtime on all three | — | Verified |
| `thunderbird` (9), `gimp` (3), `kdenlive` (11) | binary-only on all three | same | — | Binary only; Ubuntu's `/usr/bin/thunderbird` is not checked for being a snap stub |
| `chrome` (24) | not_attempted ("measured in meas-gui") | same | comm `chrome` in meas-gui (Ubuntu snap Chromium) | Ubuntu snap only |
| `systemd` (2), `dbus-daemon` (2) | not_attempted | same | comms seen in meas-gui and meas-cli samples | Ubuntu runner |
| `code`, `steam`, `steamwebhelper`, `zoom`, `spotify`, `discord`, `Xorg`, `pipewire`, `gnome-shell`, `game.exe` | not_attempted | same | none | Not verified (stated) |
| `7z` (c4), `xkrr`, `qzvd`, `video-playback-svc`, `audio-stream-helper` (c4/c5) | **absent** from the verification tables | absent | none | Not verified; not listed as not_attempted |

Other name claims:
- The note that plocate systems name the process `updatedb.plocate` (verify_names.py:40) is not what was observed. All three distros, and the meas-cli samples, show comm `updatedb`, because the process is launched via the `updatedb` name.

---

## Working files (_dev/research/jioh/2026-09-13-verification/meas/)
- `release/`: downloaded zips. `cli3/`, `gui/`, `names/`, `cli1/`: extracted. `names2/`: names:2 Actions artifacts.
- `out_cli3.json`: rerun summary, byte-identical to dataset/meas/summary.json. `out_cli1.json`: control run.
- Scripts: `diff_summary.py`, `method_checks.py` (compiler lifetimes by name), `cc1_cpu.py` (CPU per cc1, D-state share), `gui_detail.py`, `chrome_timeline.py`, `renderers.py`, `element_types.py`, `chrome_kept_types2.py`, `tracker_detail.py`, `io_detail.py`.
- `array.c`: Linux v6.17 fs/proc/array.c. `tar_create.c`: GNU tar src/create.c.
