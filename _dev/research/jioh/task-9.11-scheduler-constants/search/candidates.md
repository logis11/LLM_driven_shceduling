# Task 9.11 — candidates per scope-card item

Stage 2 result. Each item of `../scope-card.md` with the candidates the four class records found (`S1-literature.md`, `S2-project-docs.md`, `S3-traces-datasets.md`, `S4-ci-observability.md`), what each covers, and what no class found. Candidate ids are the records' own. Passages, copy identification and SHA-256 are in the records; this file only routes them to the card's items.

## Observations that exist

Observations (a population, trace or run with numbers), as distinct from documentation, source code and guidelines:

| Id | What | Machine / subject / window | Kind of data |
|---|---|---|---|
| S1-10 (Jota et al., CHI 2013) | latency JND for touch tapping and dragging | FPGA high-speed touch prototype; 20 participants; lab sessions | JND tap 64 ms (SD 24) |
| S1-11 (Deber et al., CHI 2015) | latency JND for direct and indirect touch, four tasks | FMT sensor prototype; 14 participants | JNDs 11 / 55 / 69 / 96 ms by task |
| S1-12 (Annett et al., GI 2014) | stylus inking latency perception | prototype; 12 participants | median JND 53 ms |
| S1-13 (Forch et al., 2017) | mouse latency perception | abstract only read | ≈ 60 ms |
| S1-17 (Bilodeau-Savaria et al., arXiv 2026) | SCHED_IDLE CPU-bound workers beside TPC-C | Xeon 6248R, kernel 6.17, 4 cores; window not stated | throughput drop, attributed to wake-up placement; no periodic-task wake latency |
| S3-01 (Kumar, LKML 2019) | mean wake-up latency of 8 CFS tasks beside 5 SCHED_IDLE hogs, rt-app | octacore Hikey, "tip/master" June 2019, 5 s run, N = 4 710 | 104 µs → 1 116.68 µs (max 67 664 µs); patched 102.683 µs |
| S3-02 (commit 51ce83ed523b, 2021) | SCHED_IDLE entity's run and wait lengths before and after a slice patch | HZ = 1000; machine unnamed | "runs for 4ms then waits for 1.4s"; 1 ms / 340 ms after |
| S3-03 (Bristot, deadline-server V3/V7, LKML 2023–2024) | FIFO thread's CPU share against a CFS busy loop | 6.3-rt and v6.10-rc1; machine model unnamed; 10–12.6 min osnoise runs | ≈ 94.8 % kept by FIFO |
| S3-04 (Chu, LKML 2013) | RT throttling message and the two sysctls read | host lxc34, kernel 3.12.3; no subject, no window | 1 000 000 / 950 000 µs |
| S3-06 (mpv #16346) | frames dropped on resume after buffer underrun | Apple M4, mpv 0.40-dev | "~30 or more frames" (issue text); log shows 8.9 s stalls, no per-frame drop lines |
| S3-07 (GStreamer #3798) | sink drops frames when the display has no monitor | Celeron J1900 | ≈ 1 fps rendered, ≈ 24 dropped of 25; no backlog |
| S3-08 (scx #3791) | sched_ext watchdog ejections under desktop use | Ryzen 5 PRO 2500U, linux-zen 7.2.3, 2026-09-04 19:50–20:22 | stalls at 30.387–45.099 s |
| S3-09 (scx #3739) | scx_lavd max scheduling delay | i7-12700H, 7.1.8-cachyos; window not stated | max 661.639 ms |
| S3-10 (scx #3119) | tasks waiting ≈ 20 ms with CPUs idle under lavd | Cooperlake; slice flags overridden; kernel and window unstated | ≈ 20 ms |

Illustrative samples inside documentation, no machine named: interbench man-page table, schbench README runs, hackbench man-page example (S2-15, S2-18, S2-20). No observation exists of any value on a GitHub Actions runner (S4, Not found).

## Per item

### 1. `T_interaction` (100 000 µs)

- S1-01 Miller 1968: ≤ 0.1 s for response to control activation; 0.1–0.2 s for key-to-visual echo — by Miller's own words his "best calculated guesses", not measurements, no source cited.
- S1-05 Nielsen's excerpt: the 0.1 / 1 / 10 s limits, restating Miller 1968 and Card et al. 1991 (Card not fetched: 403).
- S1-07 Shneiderman 1984: restates earlier sources ("within a tenth of a second" class); the Long 1976 report is inside it.
- Measured JNDs (S1-10, S1-11, S1-12, S1-13) are touch, stylus and mouse perception of latency differences, 11–96 ms by task, on prototypes with 12–20 participants. None measures keyboard echo; none is a "feels instantaneous" threshold in Miller's sense.
- S3: no released dataset of a latency-perception threshold (Zenodo, OSF, SHARE searched).
- Stage-3 question: whether a guideline (Miller) or a measured JND family grounds the threshold, and for which input kind.

### 2–8. Floors, seed, level, percentile method, `W_single`, boost grid

Conventions, arithmetic and design; no class was asked for a source and none is expected. Nothing found bears on them.

### 9. §8 statistics citations

- S1-04 Brodersen: ½(TP/P + TN/N), binary only, test cases as independent Bernoulli trials.
- S1-08 Chicco & Jurman: MCC formula; high only when all four cells are good; undefined when a row or column of the matrix is zero.
- S1-09 Field & Welsh (read from a third-party mirror, ism.ac.jp; OUP and Wiley copies 403): cluster bootstrap consistent as the number of clusters grows with cluster size fixed, under balanced one-way arrays.
- S1-06 Dietterich (1997-12 preprint; journal version 403): McNemar or 5×2cv recommended; the difference-of-proportions test and the resampled t test "should never be used".

### 10. §11 simulator assumptions

Design; the confirmations are 인경민's, not a source's. No class searched.

### 11 / 39. TIMER backlog semantics (rt-app attribution; 9.5 D11 hand-off)

- S2-14 rt-app: default `relative` mode re-anchors on an overrun; `absolute` mode keeps the original grid and runs back-to-back to catch up.
- S2-15 interbench: audio and video loops count missed periods and skip ahead by whole intervals.
- S2-16 mpv: drops late frames, not below 10 FPS. S2-17 GStreamer: video sinks drop frames more than 5 ms late by default; base sink default −1 never drops.
- S1-15 Lipari & Palopoli: options are abort, finish late, skip; a Linux loop skipping late instances. S1-16 ROS 2 timers: skip missed activations, stay on the original grid. S1-14 Lelli et al.: CBS re-anchors a late wake with deadline t + T.
- S3-06, S3-07: player logs showing drops, not backlog.
- No source found models a media or periodic task that accumulates a backlog except rt-app's non-default `absolute` mode.

### 12. `schbench` as tail-latency precedent

- S2-18 (git.kernel.org `mason/schbench`, only tag v1.0) and S2-19 (GitHub, no tags): the 2016 code printed p50/75/90/95/99/99.5/99.9; since 2023-04-11 latency lines print p50/90/99/99.9 and RPS lines p20/50/90; copyright 2016 Facebook, GPLv2.

### 13–17. The OSTEP values and the allotment

- S1-02 OSTEP Version 1.10 (© 2008–23): Fig 8.1 shows 8 queues, the worked examples use 3; Example 1 a 10 ms slice with the allotment equal to one slice; Fig 8.4 a 100 ms boost, "likely too small"; Fig 8.6 10 / 20 / 40 ms per level; the "voo-doo constants" and "no easy answers" passages. All quoted.

### 18. Same-granularity rule's premise (no shipped EDF residual slice)

- Not searched as its own topic. S2-05 (deadline class, fair server) and S1-14 bear on it: Linux's deadline class serves fair tasks through a server reservation (50 ms per 1 000 ms per CPU from v6.12), not a round-robin residual slice.

### 19–20. LOTTERY `batch_share`; Waldspurger's quantum

- S1-03: a 10 ms design quantum; the prototype ran at 100 ms (Mach 3.0, DECStation 5000/125). Full-text search found no ticket ratio between classes of work; every ratio is between peer clients. Confirms the "no source" label; the quantum statement is more than the registry's one sentence.

### 21. `batch_bandwidth_cap` and `linux-sched-bwc`

- S2-03 `sched-bwc.rst`: limits a cgroup's CPU time, quota per period; default period 100 ms, quota −1 (unlimited), burst 0, minimum 1 ms, maximum period 1 s. S2-04 RT throttling; S2-05 deadline admission M × runtime/period.

### 22. Config schema ranges

Design; no class searched.

### 23. Memo §3 comparison points

- illumos TS (S2-08, S2-09): 60 levels, quanta 20 down to 2 ticks, hz 1000 by default since 2020, so ≈ 20 ms at the bottom to 2 ms at the top; `ts_update` once a second.
- Solaris 2.6 lecture notes (S1-19 = S2-28, A. Arpaci-Dusseau, CS 537, 2000): 60 levels, quanta 200 ms to 20 ms (the Solaris 2.6 table, a different tick than illumos today), once-per-second boost; "no one really knows how to configure these tables well" — the literal "nobody knows" is not in it.
- MINIX 3 (S2-10): 16 queues, 200 ms quantum, rebalance every 5 s.
- scx (S2-11–13, at HEAD `00fec1e`, not a release tag): lavd 10 ms × active CPUs ÷ queued tasks clamped 0.5–5 ms; bpfland 1 ms ÷ waiting tasks, lag 40 ms; rusty 20 ms, 1 ms when fully utilised.
- Not found: Silberschatz, Stallings, the "papers" on per-level doubling; macOS, FreeBSD, Windows (not searched by any class).

### 24–26. Sweep backbone

- 26a Linux (S2-01): CFS v6.5 latency 6 ms, min_granularity 0.75 ms, wakeup granularity 1 ms, each × (1 + ilog2(min(ncpus, 8))) by the default `SCHED_TUNABLESCALING_LOG`. EEVDF `base_slice` 0.75 ms v6.6–v6.14, **0.70 ms from v6.15 to v7.2**, same factor; the changing commit not identified. S4-05: on a 4-CPU runner at 6.17 the predicted effective value is 0.70 × 3 = 2.1 ms — prediction, not observed.
- 26b illumos (S2-08, S2-09): top-level quantum 2 ticks at hz 1000.
- 26c sched_ext (S2-02): `SCX_SLICE_DFL` 20 ms at v6.12 and v7.2; v7.2 adds a 5 ms bypass slice.
- S3: no observation of the default base slice on a real machine (S3-02 and S3-10 are an idle-entity slice and an overridden lavd slice).
- S4-03: the runner's 6.17 azure kernel has `SCHED_CLASS_EXT=y`, HZ = 1000, voluntary preemption; 22.04's 6.8 kernel has no sched_ext.

### 27. `provenance_share` (0.5)

Convention reading the project's own proposal; no class searched.

### 28. `starvation_floor` (1 000 000 µs)

- Shipped bounds found: sched_ext watchdog 30 s default and maximum; lavd 30 s, bpfland 5 s, rusty 10 s (S2-02, S2-11–13). Fair server 50 ms per 1 000 ms per CPU from v6.12; v7.2 adds an ext_server (S2-05). RT throttling 950 000 / 1 000 000 µs to v7.1; at v7.2 `rt.c` sets runtime 1 000 000 while the docs still say 950 000 (S2-04, recorded as read). illumos `ts_maxwait` 0 s at levels 0–58 (boost every second), 32 000 at 59 (S2-08, S1-19).
- Observations: S3-08 watchdog ejections at 30.4–45.1 s; S3-09 661.6 ms delay under lavd; S3-03 fair-server share; S3-04 the sysctls on one host.
- None of these is the simulator's executor; the threshold still waits on 인경민's constant. They are what a shipped scheduler bounds, for the grounding's wording.

### 29–34. Arithmetic and structural guards

No class searched; none needed.

### 35–37. Role B registry entries

- `corbet-lwn24`, `scx`: not re-searched (K2 verdicts stand); S2-11–13 read scx at `00fec1e`, which could serve the open "pin commit".
- `hackbench` (S2-20, rt-tests v2.11): prints total time only; defaults 10 groups × 40 fds, 100 messages of 100 bytes.
- `stress-ng` (S2-21): a `--workload` stressor emulating timed work items; the README disclaims precise benchmarking — consistent with K1's WORDING-FIX.
- `interbench` C-interbench-11 (S2-15): mean and SD latency, max latency, % CPU, % deadlines met, 30 s default; "~7ms" stated with **no source cited** in man page, readmes or code.

### 38. Declared scheduling class (9.6 D17 hand-off)

- Kernel (S2-01, S2-06, S2-07): weights nice 0 = 1024, nice 19 = 15, SCHED_IDLE = 3; a non-idle waker preempts an idle task; idle and batch wakers do not preempt. S4-06: nice acts only within a task group (sched(7)).
- Shipped defaults: LocalSearch/tracker SCHED_IDLE + nice 19 + idle I/O (S2-22); plocate Nice=19 + idle I/O (S2-23); Baloo daemon SCHED_BATCH, extractor SCHED_IDLE, CPUWeight=1 (S2-24); ClamAV nothing (S2-25); borgmatic's sample unit nice 19 + SCHED_BATCH, borg and restic nothing (S2-26); Déjà Dup `chrt --idle` or nice 19 (S2-27).
- Observations: S3-01 (mean wake latency ×10 beside SCHED_IDLE hogs on a 2019 kernel, before its patch), S3-02 (idle entity's run length), S1-17 (throughput, not latency).
- S4 method (S4-06–S4-10): `cyclictest --policy=other` pinned to one vCPU with no hog, a nice-19 hog, a `chrt -i 0` hog and a nice-0 control; `perf sched timehist`; steal time from `/proc/stat` around each run; hog and probe in one cgroup. Not run.

## Not found, across classes

- **T1:** a keyboard-echo latency-perception measurement; the Ng et al. UIST 2012 value first-hand (ACM 403, mirror reset); any released JND dataset.
- **T3:** the commit changing EEVDF's base slice from 0.75 to 0.70 ms; per-release-tag scx values; the default base slice observed on a real machine or on a runner.
- **T6:** a literature statement of the sched_ext watchdog timeout; a prose statement of the fair server's defaults in kernel documentation.
- **T7:** literature on rt-app, interbench or player late-frame handling (documentation and source only); an rt-app overrun log; VLC (not searched).
- **T9:** a measured wake-up latency of a periodic task beside a SCHED_IDLE or nice-19 hog on a current kernel; literature on desktop indexers' declared classes.
- **T11:** any value on a GitHub Actions runner; whether debugfs `sched/` is mounted and readable there (in this cloud sandbox the entries listed but reads returned "Operation not permitted"); runner steal time and perf availability (runner-images issues #11789, #12512, #11790, #7107, #2607 found but github.com 403).
- **Memo §3:** Silberschatz, Stallings, the per-level doubling "papers", macOS, FreeBSD, Windows.

Reachability across readers: github.com pages and api.github.com returned 403 through the proxy (raw.githubusercontent.com worked); lore.kernel.org, phoronix.com, openbenchmarking.org 403; ACM DL 403; OUP and Wiley 403; Springer and BMC bot challenges; git.sesse.net and invent.kde.org 502; salsa.debian.org credential redirect; manpages.ubuntu.com 503. S3's GitHub issue passages (S3-06 issue page, S3-08–S3-10) were read through WebFetch's rendered text and are hashed as transcripts, not byte-exact copies.
