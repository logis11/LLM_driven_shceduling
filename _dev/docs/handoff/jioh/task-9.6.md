# Handoff — task 9.6 Compile, stages 1–2 (research routine, 2026-09-14)

Stages 1 and 2 of `_dev/research/jioh/research-slice-workflow.md` are done on `jioh/dataset-rebuild`; stage 3 (decisions) is 인지오's. Issue #9.

## Files

- `_dev/research/jioh/task-9.6-compile/scope-card.md` — 31 items: `compiler-child` (params 1–6, structure and unit 7–12), `build-orchestrator` (params 13–15, structure, defaults and bindings 16–22), and, by this run's boundary assumption, `cpu-batch` (23–26); registry lines 27–31.
- `…/search/input.md` — topics T1–T8 in neutral form, classes, record format.
- `…/search/S1-literature.md` (55 searches, 26 candidates), `S2-project-docs.md` (44 searches, 27 candidates), `S3-traces-datasets.md` (40 searches, 16 candidates, computations labelled), `S4-ci-observability.md` (35 searches, 19 candidates).
- `…/search/candidates.md` — observations that exist, per-item findings, not-found across classes.
- Source copies under `…/sources/` were local to the routine's clone and are gone; every record is self-sufficient (URL or commit, SHA-256, verbatim passages with locators).

## Boundary assumption to confirm first

The routine took `cpu-batch` into 9.6 because the library files it under the same "compute/batch family" header as the two build archetypes, its only source is interbench Burn, and 9.5's card handed the interbench Burn/Compile lines to 9.6 without naming an owner for the archetype. If it belongs to 9.7 (its heaviest binding is the `clamscan` scan), items 23–26 and topic T7 move with it; nothing else on the card depends on them.

## The one-observation situation

Both build archetypes already rest on one observation, `meas-ci:cli:3` (five repeats of a linux-6.6 defconfig `make -j8` on 4-vCPU runners), and the 9.3 re-analysis has re-cut its numbers to `cc1` alone (lifetime median 840 ms, CPU mean 358 ms, `make` dispatch 474 µs over 5 947 make children). What the search found is that no external observation replaces it, and several bound its weak points:

- **Process population and unit.** kbuild source (S2-01) fixes the per-object chain (`sh` → `gcc` → `cc1`, `as` → optional `objtool` → `fixdep` → `rm`), so one make job is six or seven processes; Gregg's one-second `perf sched` capture of a kernel build (S3-01) shows `cc1` carrying 6 013 ms against the `gcc` drivers' 43.6 ms; a Debian kernel build's verbose log (S3-03) gives invocation counts per tool. No source gives per-role lifetime or CPU distributions.
- **Per-compiler CPU.** The only per-translation-unit CPU data is clang on CTMark (S3-09: task-clock/wall ≈ 0.99 at `-O3`, so CPU-bound throughout, warm cache) and per-edge wall times of LLVM builds (S3-08). Nothing for gcc or the kernel.
- **Disk wait.** No observation of a compiler's blocked time. Whole-build evidence says builds are CPU-bound (Traeger et al. S1-26: > 99.2 %; Yocto S3-05: reads from the page cache). A runner can measure it directly: taskstats delay accounting is compiled into the runner kernel and gives `blkio_delay_total` per exiting task once `kernel.task_delayacct=1` is set (S4-taskstats-delayacct).
- **Dispatch cost.** No measurement of make's own cost per job anywhere; the mechanism is fully documented (S2-05: token read at the cap, `posix_spawn`/`vfork`, a shell for every kbuild recipe).
- **Parallelism.** Every vendor default is `nproc` or a memory-capped variant (dpkg, rpm, Arch wiki, Gentoo, kernel docs, dkms, PTS); ninja is `nproc + 2`; build farms run `parallel=6`, `-j64` on 64 threads, `-j16 -l75`; papers use 2 × cores or threads. No survey of what desktop users pick. The current `-j8` sits between these and its bracketing `-j4` is an interbench emulation that runs no make (S2-19).
- **Category source.** `ocallahan-atc17` read independently is a DynamoRio build (S1-01); Antfarm (S1-18) is the one paper with a named build's process count and mean lifetime (bash `make -j20`, 815 / 748 processes, > 2 s post-exec); Coetzee names `cp` and `mkdir`.
- **DKMS.** dkms 3.4.3 runs `make -j$(nproc) … -C <ksrc> M=<dir>` from the kernel postinst hook or `dkms.service` (S2-14); one real log (S3-06: 208 objects, 58 s, i7-4790). Nothing with CPU.
- **`cpu-batch`.** interbench Burn is N spinning threads with no finite work (S2-19); shipped catalogues class `ffmpeg` Heavy_CPU and `clamd` BG_CPUIO and deliberately leave compilers unclassed (S2-21); encoders and PyTorch use all cores or all physical cores by documentation (S2-26, S2-27); `clamscan` is single-process (S2-23). The only measured saturating desktop batch population is Blender's (S3-16); no measured antivirus full scan or indexer rescan exists.

## Stage 3's first question

What a spawn-table child is: `cc1` (the 9.3 re-cut), a make job (≈ 6–7 processes per object per S2-01, the concurrency unit the cap counts), or a compiler-family member (the current pooled numbers). Items 1–5, 10, 12, 13, 17 and 20 all change together with that answer, and it decides whether the existing `meas-ci:cli:3` observation is re-cut once more or re-measured on a runner with exit-time instruments (taskstats for CPU and block-I/O delay per process, `perf sched timehist` for run/wait structure). Only after that: `disk_wait` (a measured quantity or a labelled placeholder), the `-j` convention against the vendor `nproc` defaults, and whether `cpu-batch` stays in this slice.

## Flags from the readers

- Unreachable on 2026-09-14: github.com HTML and api.github.com (403) — issues, discussions and commit pages were not read verbatim; dl.acm.org (403), ieeexplore (418), openbenchmarking.org (403), lore.kernel.org (403), git.launchpad.net (403), dashboard.kernelci.org (403); proof-of-work challenge pages from git.kernel.org (mid-session), sources.debian.org, salsa, gitlab.archlinux.org, code.videolan.org, docs.fedoraproject.org (worked around via GitHub mirrors, Debian pool tarballs and curl's default user agent); cmake.org 503, gitlab.gnome.org 406, en.opensuse.org 403, arXiv API 429, dblp API bot-check.
- Paywalled and unread: Belinassi et al. 2022 (parallel compilation with GCC), Uluski et al. 2005 (antivirus workload), Kubota et al. 2019 (unified builds), Leland & Ott 1986 (process lifetimes).
- Login-walled: chromium-build-stats (ninja logs of real Chromium builds), the Gentoo MAKEOPTS forum poll.
- S3's numbers on the Debian log, the Yocto note and the `.ninja_log` files are the reader's own computations on the downloaded data; they locate candidates, they are not values.
- The readers shared one `sources/` tree; S1's staging folder was deleted by another reader mid-run and the disk filled twice (a 29 GB clone, a 100 MB JSON); every cited copy was re-fetched and re-hashed afterwards.
