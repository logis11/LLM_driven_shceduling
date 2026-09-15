# Reader input — task 9.6 compile, stage 2 search

Given to each class reader verbatim. Readers do not see the repository's current values.

## Topics

- **T1 Process population of a parallel build.** For a parallel `make -jN` build of a large C project (the Linux kernel above all, but also other trees) on Linux: which processes are created per translation unit and per link (compiler driver, `cc1`/`cc1plus`, assembler, linker, `collect2`, shells, kbuild helpers such as `fixdep`, `genksyms`, `modpost`), how many of each per build, how their lifetimes nest, and any observation giving per-process lifetime or CPU-time distributions rather than totals.
- **T2 CPU and blocking of one compiler process.** Observations of the CPU time a single compilation of a translation unit takes and how it is distributed across a project (histogram, percentiles, mean vs median); how much of a compiler process's lifetime is spent blocked on file I/O (reading sources and headers, writing objects) under a warm and a cold page cache; whether any measurement shows a run / wait / run structure inside a compiler process, or shows it CPU-bound throughout.
- **T3 The orchestrator.** How GNU make dispatches jobs under `-jN` (the jobserver, recursive makes, the shell between make and the compiler), what make's own CPU cost per dispatched job is, how the number of concurrently live processes relates to N, and what make does when the parallelism cap is reached; the same for other drivers a desktop build uses (ninja, cargo).
- **T4 Parallelism level in practice.** What `-j` (or the equivalent) developers, distributions and build tools use on desktops and laptops — defaults such as `nproc`, `nproc + 1`, `2 × nproc`, distribution packaging defaults (Debian `parallel=`, Fedora `%_smp_mflags`, Arch `MAKEFLAGS`, Gentoo `MAKEOPTS`), ninja's default — with the documented rationale, and any observation of the level users actually pick.
- **T5 Unattended module rebuilds.** For DKMS on a Linux desktop: what an autoinstall run does process-wise (which `make` invocation, with what parallelism, how many compiler processes, for how long), what triggers it (kernel install hook, boot service), and any observation of its duration or CPU.
- **T6 Builds as a scheduler workload.** Which builds scheduler evaluations and kernel developers use as a compile workload (kernel `defconfig` / `tinyconfig` / `allmodconfig`, LLVM, others), on what machines and with what `-j`, with any reported process counts, lifetimes or CPU-time distributions; kernel scheduler features motivated by parallel builds (autogroup, child-runs-first) and what their documentation says; any study of process lifetime distributions on Unix or Linux in general.
- **T7 Saturating batch jobs.** How benchmarks and observations characterise a CPU-saturating desktop batch job — an antivirus scan, a video encode, a model-training loop, a file indexer's full rescan — in thread count, sustained utilisation and duration; whether shipped process-treatment catalogues (ananicy and its rule sets, distribution defaults) assign compilers and batch jobs a scheduling class, and which.
- **T8 CI observability.** Whether a GitHub Actions hosted runner can observe, for every process of a real build, CPU time at exit, lifetime, and time blocked on I/O (BSD process accounting, `wait4` rusage through a wrapper shell, taskstats delay accounting and its `blkio` delay, BCC/bpftrace exit and exec tracing, `perf sched timehist`, `perf trace`, `strace -f -c`, `make --trace`/`--debug=j` for dispatch), with what root and kernel-config requirements; what the runner's hardware variance, page-cache control and disk type allow; what it cannot observe (desktop-class hardware, a user's own `-j` choice, an interactive session around the build).

## Classes

- S1 — peer-reviewed and preprint literature (T1, T2, T3, T6, T7).
- S2 — primary project and vendor documentation and source code (T1, T3, T4, T5, T6, T7).
- S3 — public traces and datasets (T1, T2, T4, T5, T6, T7).
- S4 — own measurement on a CI runner (T8; and what of T1, T2, T3, T5 a runner could observe).

## Record format

Each reader writes `search/S<k>-<class>.md`:

1. **Search log** — one row per query: date, engine or venue, query terms, hits followed, dead ends with the HTTP status.
2. **Candidates** — per candidate: a provisional id; full citation; copy read (URL or commit, version, date accessed, local path under `sources/<id>/`, SHA-256); verbatim passages with locators (page, section, `file:line` at a commit); coverage per topic T1–T8 — covers (naming the object, unit, statistic, scope and population) or does not cover; whether it is one observation (one population, trace, run or build) and whether machine, project built and window are named.
3. **Not found** — topics with no candidate, with the searches that established it.

Source copies go to `sources/<id>/` (gitignored, local to this clone only). The record must be self-sufficient: everything a reader needs is in the quoted passages and the copy identification, never "see the local file". Verbatim means verbatim; a passage that cannot be quoted is not a passage.
