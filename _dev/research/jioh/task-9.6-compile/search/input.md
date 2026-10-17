# Reader input — task 9.6 compile, stage 2 search

Given to each class reader verbatim. Readers do not see the repository's current values. Second run of this slice (issue #11); the first run's records were withdrawn and are not available to the readers.

## Topics

- **T1 Process population of a parallel build.** For a parallel `make -jN` build of a large C project (the Linux kernel above all, but also other trees) on Linux: which processes are created per translation unit and per link (compiler driver, `cc1`/`cc1plus`, assembler, linker, `collect2`, shells, kbuild helpers such as `fixdep`, `genksyms`, `modpost`), how many of each per build, how their lifetimes nest, and any observation giving per-process lifetime or CPU-time distributions rather than totals.
- **T2 CPU and blocking of one compiler process.** Observations of the CPU time a single compilation of a translation unit takes and how it is distributed across a project (histogram, percentiles, mean vs median); how much of a compiler process's lifetime is spent blocked on file I/O (reading sources and headers, writing objects) under a warm and a cold page cache; whether any measurement shows a run / wait / run structure inside a compiler process, or shows it CPU-bound throughout.
- **T3 The orchestrator.** How GNU make dispatches jobs under `-jN` (the jobserver, recursive makes, the shell between make and the compiler), what make's own CPU cost per dispatched job is, how the number of concurrently live processes relates to N, and what make does when the parallelism cap is reached; the same for other drivers a desktop build uses (ninja, cargo).
- **T4 Parallelism level in practice.** What `-j` (or the equivalent) developers, distributions and build tools use on desktops and laptops — defaults such as `nproc`, `nproc + 1`, `2 × nproc`, distribution packaging defaults (Debian `parallel=`, Fedora `%_smp_mflags`, Arch `MAKEFLAGS`, Gentoo `MAKEOPTS`), ninja's default — with the documented rationale, and any observation of the level users actually pick.
- **T5 Unattended module rebuilds.** For DKMS on a Linux desktop: what an autoinstall run does process-wise (which `make` invocation, with what parallelism, how many compiler processes, for how long), what triggers it (kernel install hook, boot service), and any observation of its duration or CPU.
- **T6 Builds as a scheduler workload.** Which builds scheduler evaluations and kernel developers use as a compile workload (kernel `defconfig` / `tinyconfig` / `allmodconfig`, LLVM, others), on what machines and with what `-j`, with any reported process counts, lifetimes or CPU-time distributions; kernel scheduler features motivated by parallel builds (autogroup, child-runs-first) and what their documentation says; any study of process lifetime distributions on Unix or Linux in general; and any observation of a parallel build's behaviour when confined to one CPU (single-core runs, `taskset`/cgroup-confined builds, `-jN` with N above the core count): how process lifetimes, concurrency and the build's CPU total change against an unconfined run of the same build.
- **T7 Saturating batch jobs.** How benchmarks and observations characterise a CPU-saturating desktop batch job — an antivirus scan, a video encode, a model-training loop, a file indexer's full rescan — in thread count, sustained utilisation and duration; whether shipped process-treatment catalogues (ananicy and its rule sets, distribution defaults) assign compilers and batch jobs a scheduling class, and which.
- **T8 CI observability under a single-core pin.** Given a GitHub Actions hosted runner (4 vCPUs) on which a build is confined to one CPU with `taskset` while the instruments run on the other CPUs (the tooling is quoted below): whether the runner can observe, for every process of a real build, CPU time at exit, lifetime, and time blocked on I/O (BSD process accounting, `wait4` rusage through a wrapper shell, taskstats delay accounting and its `blkio` delay, BCC/bpftrace exit and exec tracing, `perf sched record` / `timehist` per-schedule run and wait with wakeup rows, `perf trace`, `strace -f -c`, `make --trace`/`--debug=j` for dispatch), with what root and kernel-config requirements; what a pin to one CPU does to each instrument (a `/proc` sampler on another CPU: does its censoring of short-lived processes change when the observed processes are time-shared on one CPU; forkstat's event loss; `perf sched` volume on one CPU); what other processes share the pinned CPU on a hosted runner (the runner's own agent, containerd) and whether they can be moved or measured; what the runner's hardware variance, page-cache control and disk type allow; and what it cannot observe (desktop-class hardware, a user's own `-j` choice, an interactive session around the build, parallelism itself).

## Classes

- S1 — peer-reviewed and preprint literature (T1–T7).
- S2 — primary project and vendor documentation and source code (T1, T3, T4, T5, T6, T7).
- S3 — public traces, datasets, build logs and benchmark databases (T1, T2, T4, T5, T6, T7).
- S4 — own measurement on a CI runner (T8; documentation research and, where the reader can, checks of package availability and kernel configuration from public sources — nothing is measured in this session).

## The measurement tooling, as given (for T8)

Quoted from the repository at commit `94f75d8` so the S4 reader need not open it. It is the instrument, not a value to be found.

`dataset/tools/meas/pin.sh` (lines 1–13, 14–21, 25–27):

> `# pin.sh — single-core measurement (9.5 follow-ups spec, decisions 2, 3, 5).` / `# Source it. Every measured load on the runner is pinned to one CPU` / `# (MEAS_CPU, the last one); the harness — display server, replay driver,` / `# perf, sidecars, snapshots — runs on the others (MEAS_HARNESS_CPUS), so the` / `# observation is the load's own serialisation on one CPU with the rest of` / `# the machine idealised. On a one-CPU machine both sets are CPU 0. Without` / `# taskset (dev machines) nothing is pinned and MEAS_PIN_AVAILABLE=0 says so.`
>
> `MEAS_CPU="${MEAS_CPU:-$((MEAS_NPROC - 1))}"` / `MEAS_HARNESS_CPUS="${MEAS_HARNESS_CPUS:-0-$((MEAS_NPROC - 2))}"`
>
> `pin_load()    { if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_CPU" "$@"; else "$@"; fi; }` / `pin_harness() { if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -c "$MEAS_HARNESS_CPUS" "$@"; else "$@"; fi; }` / `pin_self_harness() { if [ "$MEAS_PIN_AVAILABLE" = 1 ]; then taskset -cp "$MEAS_HARNESS_CPUS" $$ > /dev/null; fi; }`

`dataset/tools/meas/phase.sh` (lines 1–10): a phase wrapper that runs one command inside a named phase, appending `{"phase","start_us","end_us","rc","pin","cpu"}` to a phases file; `MEAS_PIN=load` (default) runs the command on the one measured CPU, `MEAS_PIN=harness` on the harness CPUs, `MEAS_PIN=none` leaves it alone.

`.github/workflows/meas-cli.yml` (the CLI measurement batch; `runs-on: ubuntu-latest`, matrix `repeat: [1..5]`, `timeout-minutes: 180`):

> lines 38–41: `sudo apt-get install -y forkstat clamav plocate rsync xz-utils flex bison libssl-dev libelf-dev bc tracker tracker-miner-fs dbus-daemon dbus-user-session`
>
> lines 48–59 (Start sidecars): `# single-core measurement (dataset/tools/meas/pin.sh): sidecars on the harness CPUs,` / `# each measured phase on the one measured CPU (phase.sh, MEAS_PIN=load)` / `source dataset/tools/meas/pin.sh; pin_self_harness; pin_record | tee "$MEAS_DIR/pin.kv"` / `sudo sh -c "nohup forkstat -e fork,exec,exit,comm > '$MEAS_DIR/lifecycle.log' 2> '$MEAS_DIR/forkstat.err' &"` / `nohup python3 dataset/tools/meas/proc_sampler.py --interval 0.5 --ctxt --out "$MEAS_DIR/proc_samples.jsonl" 2> "$MEAS_DIR/sampler.err" &`
>
> lines 61–80 (Measured phases, each through `phase.sh` and so pinned to the measured CPU): `idle-baseline -- sleep 60`; `network-bulk -- wget … linux-6.6.tar.xz`; `untar -- tar -xf …`; `kernel-defconfig -- make -C "$CORPUS" defconfig`; `kernel-build-j8 -- make -C "$CORPUS" -j8`; `archive-tar-xz`, `rsync-copy`, `updatedb`, `locate-query`, `freshclam`, `clamscan -r -i "$CORPUS/Documentation"`; then cold-cache variants after `sudo sysctl -q vm.drop_caches=3`, including `kernel-clean -- make -C "$CORPUS" clean` and `kernel-build-cold -- make -C "$CORPUS" -j8`.

`dataset/tools/meas/proc_sampler.py`: a `/proc` poller at the given interval recording per-process CPU ticks, state and (with `--ctxt`) voluntary/involuntary context-switch counters, per pid and per thread. `dataset/tools/meas/runner_spec.py`: records `uname`, `nproc`, `/proc/cpuinfo` model name, `MemTotal`, `/etc/os-release`, the GitHub run ids.

The GUI campaign's instrument (not used by `meas-cli.yml`): `sudo perf sched record -k CLOCK_MONOTONIC -a -o … -- sleep <phase>` over each whole phase, read with `perf sched timehist` and `perf sched timehist -w` for the wakeup rows; the analysis counts a schedule-in as a wake only when a wakeup event for that thread lies between its previous schedule-out and this schedule-in, folding a resume after preemption into the preceding wake. Its method notes that on a hosted runner "the runner's own agent processes (containerd, the hosted-compute agent, its .NET runtime) are not ours to pin and share the measured CPU" (about 1 100 of their schedule rows on the measured CPU over a 60 s phase against 18 865 of a GUI application's, in one dry run).

## Record format

Each reader writes `search/S<k>-<class>.md`:

1. **Search log** — one row per query: date, engine or venue, query terms, hits followed, dead ends with the HTTP status.
2. **Candidates** — per candidate: a provisional id `S<k>-NN`; full citation; copy read (URL or commit, version, date accessed, local path under `sources/S<k>-NN/`, SHA-256 of each file fetched); verbatim passages with locators (page, section, slide, `file:line` at a commit); coverage per topic — covers (naming the object, unit, statistic, scope and population) or does not cover; whether it is one observation (one population, trace, run or build) and whether machine, subject (project, build configuration, `-j`) and window are named. Where the reader computes a number from downloaded data (a count over a log, a percentile over a file), the computation is labelled as the reader's own and the command recorded; it locates a candidate, it is not a value.
3. **Not found** — topics with no candidate, with the searches that established it.

Source copies go to `sources/S<k>-NN/` (gitignored; they do not survive this clone, so the record must be self-sufficient: everything a reader needs is in the quoted passages and the copy identification, never "see the local file"). Verbatim means verbatim; a passage that cannot be quoted is not a passage.
