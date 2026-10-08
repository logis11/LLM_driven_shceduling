# S4 — own measurement on a CI runner (T15; through it T10 and T11)

Reader: S4 class reader, run unattended on 2026-10-07 in a Claude Code cloud sandbox.

**Status of every observation in this record: no observation was made on a GitHub Actions runner.** This reader cannot start a job on a GitHub-hosted runner (no workflow was created, modified, triggered or read; no git add/commit/push was done). What follows is (a) the documentation of what the runner is and what is on its image, (b) the documented method a later runner measurement would use per quantity, and (c) a clearly separated sandbox illustration made on a different machine. None of (a)–(c) is a runner observation of T10 or T11 quantities.

Inputs read: `search/input.md` only; no other repository file was opened. Source copies are under `sources/S4-NN/` (gitignored, not durable); everything needed is quoted below.

---

## 1. Search log

| # | Date | Engine / venue | Exact query or request | Hits followed | Dead ends (HTTP status) |
|---|---|---|---|---|---|
| 1 | 2026-10-07 | git (ls-remote) | `git ls-remote https://github.com/actions/runner-images HEAD` | HEAD = `e7c7cb8f4227797c6404a4e98c2ad463c2f70f91` | — |
| 2 | 2026-10-07 | raw.githubusercontent.com (curl) | `https://raw.githubusercontent.com/actions/runner-images/e7c7cb8f4227797c6404a4e98c2ad463c2f70f91/images/ubuntu/Ubuntu2404-Readme.md` | 200 → S4-01 | — |
| 3 | 2026-10-07 | docs.github.com (curl, HTML) | `https://docs.github.com/en/actions/reference/runners/github-hosted-runners` | 200 (no redirect; effective URL identical) → S4-02 | — |
| 4 | 2026-10-07 | man7.org (curl) | `https://man7.org/linux/man-pages/man5/proc_stat.5.html` | 200 → S4-03 | — |
| 5 | 2026-10-07 | man7.org (curl) | `https://man7.org/linux/man-pages/man8/vmstat.8.html` | 200 → S4-04 | — |
| 6 | 2026-10-07 | man7.org (curl) | `https://man7.org/linux/man-pages/man1/perf-bench.1.html` | 200 → S4-05 | — |
| 7 | 2026-10-07 | man7.org (curl) | `https://man7.org/linux/man-pages/man1/perf-sched.1.html` | 200 → S4-06 | — |
| 8 | 2026-10-07 | man7.org (curl) | `https://man7.org/linux/man-pages/man7/sched.7.html` | 200; read, not used (no passage on T15 quantities); copy deleted | — |
| 9 | 2026-10-07 | git ls-remote + raw.githubusercontent.com | `git ls-remote --tags https://github.com/torvalds/linux v6.17` → `6063257da111c7639d020c5f15bfb37fb839d8b6`; `https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/scheduler/sched-stats.rst` (v6.17 chosen to match the runner kernel series 6.17, S4-01) | 200 → S4-07 | — |
| 10 | 2026-10-07 | git ls-remote | `git ls-remote https://github.com/ggml-org/llama.cpp HEAD` | HEAD = `bd4eeaa047006cb1fe71999fbd11134b5836e167` | — |
| 11 | 2026-10-07 | raw.githubusercontent.com (curl) at llama.cpp `bd4eeaa0…` | `README.md`, `grammars/README.md`, `tools/llama-bench/README.md`, `docs/build.md`, `tools/cli/README.md` | all 200 → S4-08 | `tools/main/README.md` → **404** (path no longer exists at this commit; README links `tools/cli/README.md` instead) |
| 12 | 2026-10-07 | packages.ubuntu.com (curl) | `/noble/linux-tools-common`, `/noble/linux-tools-azure`, `/noble/sysstat`, `/noble/rt-tests`, `/noble/llama.cpp`, `/noble/lmbench`, `/noble-updates/linux-tools-6.17.0-1022-azure` | all 200 → S4-09 | `/noble/llama.cpp` → 200 but body "Package not available in this suite." (kept as evidence of absence); `/noble-security/linux-tools-6.17.0-1022-azure` → 200 with "Error" page (copy discarded) |
| 13 | 2026-10-07 | git clone --depth 1 | `https://github.com/intel/lmbench` (HEAD `27b43aeec9dc0bb45f420388c78e42dde4c23bf0`), file `doc/lat_ctx.8` | → S4-10 (only that file kept) | — |
| 14 | 2026-10-07 | WebSearch (standard) | `GitHub Actions ubuntu runner "perf bench sched pipe" context switch measurement` | Result list only: runs-on.com/benchmarks/github-actions-cpu-performance; github.com/actions/runner-images/issues/4974 (perf counters on runners); LKML threads on `perf bench sched pipe -G`. No result reports a `perf bench sched pipe` run on a GitHub-hosted runner. The search engine's summary is not used as a passage. | see #15 |
| 15 | 2026-10-07 | github.com HTML, api.github.com, GitHub MCP | `https://github.com/actions/runner-images/issues/4974`; `https://api.github.com/repos/actions/runner-images/issues/4974`; MCP `issue_read` actions/runner-images#4974 | — | HTML **403**; API **403**; MCP: "Access denied: repository "actions/runner-images" is not configured for this session". Not read; no passage. |
| 16 | 2026-10-07 | WebSearch (standard) | `llama.cpp benchmark GitHub Actions runner CPU tokens per second GGUF` | Result list only (llama-bench README mirrors on docs.rs, simplified.guide tutorials, skill indexes). None reports llama.cpp latency on a GitHub-hosted runner. Summary not used as a passage. | — |

---

## 2. Candidates

All candidates are documentation of the runner or of a measurement method. **None is an observation of a T10 or T11 quantity on a GitHub runner.**

### S4-01 — actions/runner-images, Ubuntu 24.04 image README

- Citation: GitHub, `actions/runner-images`, `images/ubuntu/Ubuntu2404-Readme.md`, Image Version 20260927.320.1.
- Copy read: `https://raw.githubusercontent.com/actions/runner-images/e7c7cb8f4227797c6404a4e98c2ad463c2f70f91/images/ubuntu/Ubuntu2404-Readme.md`; commit `e7c7cb8f4227797c6404a4e98c2ad463c2f70f91` (repo HEAD on access); accessed 2026-10-07; local `sources/S4-01/Ubuntu2404-Readme.md`; SHA-256 `1d144c7fb063ac2fb905133160d96b18c2ce99a7de120242540e14f6c5ca31cd`.
- Passages:
  - `Ubuntu2404-Readme.md:3` — "[[Ubuntu] `ubuntu-latest` label will use Ubuntu 26.04 in November 2026](https://github.com/actions/runner-images/issues/14748)"
  - `Ubuntu2404-Readme.md:8-12` — "# Ubuntu 24.04 / - OS Version: 24.04.5 LTS / - Kernel Version: 6.17.0-1022-azure / - Image Version: 20260927.320.1 / - Systemd version: 255.4-1ubuntu8.17"
  - `Ubuntu2404-Readme.md:18` — "- Clang: 16.0.6, 17.0.6, 18.1.3"; `:22` — "- GNU C++: 12.4.0, 13.3.0, 14.2.0"; `:28` — "- Python 3.12.3"; `:72` — "- CMake 3.31.6"
  - `Ubuntu2404-Readme.md:256` — "### Installed apt packages"; the table that follows (lines 257–332) lists, among others, "| gcc                    | 4:13.2.0-7ubuntu1             |" (`:280`), "| sudo                   | 1.9.15p5-3ubuntu5.24.04.3     |" (`:316`), "| time                   | 1.9-0.2build1                 |" (`:322`).
  - Absence check (not a passage; a search over the whole file): case-insensitive search for `perf`, `linux-tools`, `sysstat`, `rt-tests`, `llama` returns **no line**. The README therefore does not list perf/linux-tools, sysstat (vmstat-companion pidstat), rt-tests, or llama.cpp as installed. It also does not list `procps` (vmstat's package) in its apt table; whether `vmstat` is present on the runner is not stated by this README and was not observed.
- Coverage: T15 — covers *what the runner image is*: OS 24.04.5 LTS, kernel 6.17.0-1022-azure, image 20260927.320.1, compilers (gcc 13.3/14.2, clang, cmake 3.31.6) sufficient to build a C ping-pong or llama.cpp from source; shows that perf, sysstat, rt-tests, llama.cpp are not in the listed image contents. Does not state vCPU, RAM, disk, or VM-vs-container (see S4-02). T10, T11: does not cover. T1–T9, T12–T14: does not cover.
- Observation? No. A software manifest, not a measurement; no machine instance, subject or window.
- Note for later use: `ubuntu-latest` is announced to move to 26.04 in November 2026 (line 3), so a later measurement should pin `runs-on: ubuntu-24.04` (or name whichever image it used) and record the image version and `uname -r` it saw.

### S4-02 — GitHub Docs, "GitHub-hosted runners reference"

- Citation: GitHub Docs, "GitHub-hosted runners reference", docs.github.com, version current on access (page carries no version/date in the fetched HTML).
- Copy read: `https://docs.github.com/en/actions/reference/runners/github-hosted-runners` (HTTP 200, no redirect); accessed 2026-10-07; local `sources/S4-02/github-hosted-runners-reference.html`; SHA-256 `06d83773e37ab943ad4b8f5defa18270716d0d40a0bff742a714c3295134b312`. Passages quoted from the visible text of the HTML (tags stripped); locators are the page's section anchors.
- Passages:
  - `#standard-github-hosted-runners-for-public-repositories` — "For public repositories, jobs using the workflow labels shown in the table below will run with the associated specifications. With the exception of single-CPU runners, each GitHub-hosted runner is a new virtual machine (VM) hosted by GitHub. Single-CPU runners are hosted in a container on a shared VM—see GitHub-hosted runners reference. Use of the standard GitHub-hosted runners is free and unlimited on public repositories."
  - Same section, table (columns "Virtual machine / container | Processor (CPU) | Memory (RAM) | Storage (SSD) | Architecture | Workflow label"), row: "Linux | 4 | 16 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04"; row: "Linux | 1 | 5 GB | 14 GB | x64 | ubuntu-slim".
  - `#standard-github-hosted-runners-for--private-repositories` — "For  private repositories, jobs using the workflow labels shown in the table below will run on virtual machines with the associated specifications." Table row: "Linux | 2 | 8 GB | 14 GB | x64 | ubuntu-latest, ubuntu-24.04, ubuntu-22.04, ubuntu-26.04".
  - `#single-cpu-runners` — "ubuntu-slim runners execute Actions workflows in Ubuntu Linux, inside a container rather than a full VM instance." and "The container for ubuntu-slim runners runs in unprivileged mode. This means that some operations requiring elevated privileges—such as mounting file systems, using Docker-in-Docker, or accessing low-level kernel features—are not supported."
  - `#administrative-privileges` — "The Linux and macOS virtual machines both run using passwordless sudo. When you need to execute commands or install tools that require more privileges than the current user, you can use sudo without needing to provide a password."
  - `#ip-addresses` — "Windows and Ubuntu runners are hosted in Azure and subsequently have the same IP address ranges as the Azure datacenters."
- Coverage: T15 — covers the runner's shape: `ubuntu-24.04`/`ubuntu-latest` x64 is a fresh VM per job hosted in Azure, 4 CPUs / 16 GB RAM / 14 GB SSD on public repositories and 2 CPUs / 8 GB / 14 GB on private repositories; passwordless sudo (so `apt-get install` and `perf`/`sysctl` as root are permitted by policy); `ubuntu-slim` is a 1-CPU unprivileged container where "low-level kernel features" are unsupported (so not suitable for perf/schedstat). Does not name the CPU model, hypervisor, whether the VM's vCPUs are dedicated, or the guest's perf-event/PMU availability. T10, T11: does not cover. Other topics: does not cover.
- Observation? No. Documentation of a product specification; no machine instance or window.
- Consequence for model sizing (arithmetic on S4-02 and S4-08, not an observation): a 7B Q4_0 GGUF of 3.56 GiB (S4-08) fits 16 GB RAM and 14 GB SSD on the public-repo runner and also 8 GB RAM on the private-repo runner, with the 14 GB SSD shared with the image's own usage (free space on the runner's disk is not stated by S4-02 and was not observed).

### S4-03 — proc_stat(5), Linux man-pages

- Citation: Linux man-pages project, `proc_stat(5)`, "Linux man-pages 6.19 2026-02-08", HTML rendering created 2026-09-09 (man7.org).
- Copy read: `https://man7.org/linux/man-pages/man5/proc_stat.5.html`; accessed 2026-10-07; local `sources/S4-03/proc_stat.5.html`; SHA-256 `3f0b831fc0708a4e11e9dd2ec729f45677afeb353cba76261aa03004c1c4818d`.
- Passages (section DESCRIPTION):
  - "/proc/stat / kernel/system statistics.  Varies with architecture. / Common entries include:"
  - "ctxt 115315 / The number of context switches that the system / underwent."
- Coverage: T15 / T10 method — covers the counter for context switches per second: `ctxt` is a cumulative system-wide count (all CPUs), so rate = Δctxt / Δt; per-core rate needs division by CPU count (the counter is not per CPU). No values for any machine. Other topics: does not cover.
- Observation? No.

### S4-04 — vmstat(8), procps-ng

- Citation: procps-ng, `vmstat(8)`; man7.org page "obtained from the project's upstream Git repository ⟨https://gitlab.com/procps-ng/procps.git⟩ on 2026-08-04. (At that time, the date of the most recent commit that was found in the repository was 2026-07-30.)" (COLOPHON).
- Copy read: `https://man7.org/linux/man-pages/man8/vmstat.8.html`; accessed 2026-10-07; local `sources/S4-04/vmstat.8.html`; SHA-256 `a7eb6fb2e0e4fed7e273f1826f9958e22aa600de7ad8793b0592743ee1a938da`.
- Passages:
  - DESCRIPTION — "The first report produced gives averages since the last reboot. Additional reports give information on a sampling period of length delay.  The process and memory reports are instantaneous in either case."
  - OPTIONS — "delay  The delay between updates in seconds.  If no delay is specified, only one report is printed with the average values since boot."
  - FIELD DESCRIPTION FOR VM MODE, System — "in: The number of interrupts per second, including the clock." / "cs: The number of context switches per second."
- Coverage: T15 / T10 method — covers `vmstat <delay>` `cs` column as system-wide context switches per second over each sampling period; the first line is a since-boot average and must be discarded (or use `-y, --no-first`, "Omits first report with statistics since system boot." — OPTIONS). No values. Other topics: does not cover.
- Observation? No.

### S4-05 — perf-bench(1), Linux kernel perf tool

- Citation: Linux kernel `tools/perf`, `perf-bench(1)`; man7.org page "obtained from the project's upstream Git repository ⟨http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git⟩ on 2026-08-04. (At that time, the date of the most recent commit that was found in the repository was 2026-08-03.)" (COLOPHON).
- Copy read: `https://man7.org/linux/man-pages/man1/perf-bench.1.html`; accessed 2026-10-07; local `sources/S4-05/perf-bench.1.html`; SHA-256 `9859f6921208ae023eddd391eb4f0d65f70ae45e83eaf98b3e1f687be2e2b53b`.
- Passages:
  - SUITES FOR sched — "pipe / Suite for pipe() system call. Based on pipe-test-1m.c by Ingo Molnar."
  - Options of pipe — "-l, --loop= / Specify number of loops." and "-G, --cgroups= / Names of cgroups for sender and receiver, separated by a comma. This is useful to check cgroup context switching overhead."
  - Example of pipe — "% perf bench sched pipe / (executing 1000000 pipe operations between two tasks) / Total time:8.091 sec / 8.091833 usecs/op / 123581 ops/sec"
  - COMMON OPTIONS example — "% perf bench sched pipe                      # with no style specified / (executing 1000000 pipe operations between two tasks) / Total time:5.855 sec / 5.855061 usecs/op / 170792 ops/sec"
- Coverage: T15 / T10 method — covers `perf bench sched pipe`: two tasks exchange over pipes; result in µs per operation and ops/s. The man page does not itself pin the two tasks to one CPU; pinning is done externally (`taskset -c N perf bench sched pipe`). What it measures is a round trip of pipe write/read syscalls plus the wake-up and context switches it causes — not a bare context switch. The example numbers (8.09 and 5.86 µs/op) carry no machine, kernel or date and are not usable as T10 values. Other topics: does not cover.
- Observation? No (examples without machine named).
- Availability on the runner: perf is not on the image (S4-01); installable from the archive as the kernel-matched `linux-tools-6.17.0-1022-azure` (S4-09).

### S4-06 — perf-sched(1), Linux kernel perf tool

- Citation: Linux kernel `tools/perf`, `perf-sched(1)` (man7.org rendering, same upstream source and fetch date convention as S4-05).
- Copy read: `https://man7.org/linux/man-pages/man1/perf-sched.1.html`; accessed 2026-10-07; local `sources/S4-06/perf-sched.1.html`; SHA-256 `545b3f01a34d3f00e27421f9f5d9ef17c656a68724fd57f87f7f9c40ad095268`.
- Passages:
  - NAME — "perf-sched - Tool to trace/measure scheduler properties (latencies)"
  - SYNOPSIS — "perf sched {record|latency|map|replay|script|timehist|stats}"
  - DESCRIPTION — "'perf sched record <command>' to record the scheduling events of an arbitrary workload." / "'perf sched latency' to report the per task scheduling latencies and other scheduling properties of the workload."
  - DESCRIPTION — "It shows Runtime(time that a task spent actually running on the CPU), Count(number of times a delay was calculated) and delay(time that a task was ready to run but was kept waiting)."
  - DESCRIPTION — "'perf sched timehist' provides an analysis of scheduling events." … "By default it shows the individual schedule events, including the wait time (time between sched-out and next sched-in events for the task), the task scheduling delay (time between runnable and actually running) and run time for the task:"
  - DESCRIPTION — "'perf sched stats {record | report | diff} <command>' to capture, report the diff in schedstat counters … schedstat counters which are present in the linux kernel and are exposed through the file ``/proc/schedstat``. These counters are enabled or disabled via the sysctl governed by the file ``/proc/sys/kernel/sched_schedstats``."
- Coverage: T15 / T10 method — covers scheduling latency measurement: per-task average and maximum "delay" (runnable → running) from `perf sched record` + `perf sched latency`, per-event "sch delay" from `timehist`. Units ms (examples). Requires tracepoint access (root on the runner, via passwordless sudo per S4-02). Whether the `stats` subcommand exists in the perf built for kernel 6.17 (`linux-tools-6.17.0-1022-azure`) is not established by this page (the page reflects the 2026-08 mainline tree) and was not checked. Example values in the page carry no machine named; not usable as T10 values. Other topics: does not cover.
- Observation? No.

### S4-07 — Linux kernel `Documentation/scheduler/sched-stats.rst` at v6.17

- Citation: Linux kernel, `Documentation/scheduler/sched-stats.rst`, tag v6.17 (tag object resolved by `git ls-remote` to `6063257da111c7639d020c5f15bfb37fb839d8b6`).
- Copy read: `https://raw.githubusercontent.com/torvalds/linux/v6.17/Documentation/scheduler/sched-stats.rst`; accessed 2026-10-07; local `sources/S4-07/sched-stats.rst`; SHA-256 `6c80bd9a62d50aa37161d6d909dfeff8c460c3b949454bf4c093c211f6252335`.
- Passages:
  - `sched-stats.rst:5-9` — "Version 17 of schedstats removed 'lb_imbalance' field as it has no significance anymore and instead added more relevant fields namely 'lb_imbalance_load', 'lb_imbalance_util', 'lb_imbalance_task' and 'lb_imbalance_misfit'. The domain field prints the name of the corresponding sched domain from this version onwards."
  - `sched-stats.rst:59` — "cpu<N> 1 2 3 4 5 6 7 8 9"
  - `sched-stats.rst:65-70` — "Next three are schedule() statistics: … 3) # of times schedule() was called / 4) # of times schedule() left the processor idle"
  - `sched-stats.rst:77-82` — "Next three are statistics describing scheduling latency: / 7) sum of all time spent running by tasks on this processor (in nanoseconds) / 8) sum of all time spent waiting to run by tasks on this processor (in nanoseconds) / 9) # of timeslices run on this cpu"
  - `sched-stats.rst:190-198` — "/proc/<pid>/schedstat … There are three fields in this file correlating for that process to: / 1) time spent on the cpu (in nanoseconds) / 2) time spent waiting on a runqueue (in nanoseconds) / 3) # of timeslices run on this cpu"
- Coverage: T15 / T10 method — covers `/proc/schedstat` per-CPU counters: schedule() calls (field 3, a per-CPU scheduling-decision count; Δ/Δt gives scheduling events per second per core), total runqueue wait (field 8, ns) and timeslices run (field 9), so mean wait per timeslice = Δfield8 / Δfield9 per CPU. Per-process the same in `/proc/<pid>/schedstat`. The file exists only with CONFIG_SCHEDSTATS; collection is gated by `/proc/sys/kernel/sched_schedstats` (S4-06). Whether the 6.17.0-1022-azure kernel has CONFIG_SCHEDSTATS is not stated by any source read and was not observed. No values. Other topics: does not cover.
- Observation? No.

### S4-08 — llama.cpp documentation at commit bd4eeaa0

- Citation: ggml-org/llama.cpp, `README.md`, `docs/build.md`, `grammars/README.md`, `tools/cli/README.md`, `tools/llama-bench/README.md` at commit `bd4eeaa047006cb1fe71999fbd11134b5836e167` (repo HEAD on access).
- Copy read: `https://raw.githubusercontent.com/ggml-org/llama.cpp/bd4eeaa047006cb1fe71999fbd11134b5836e167/<path>`; accessed 2026-10-07; local `sources/S4-08/`; SHA-256:
  - `README.md` `dc2d34687c844ecf929d9e9a9c9c78e8023b52abf3b2b3d039600c79016673b6`
  - `docs/build.md` `af682686b967d62f06514edddcbbfb0f4d83a6f730ec6ce1432b015a5212032a`
  - `grammars/README.md` `e1874c0f08abbcfe45eff0b7b0290faa58f630981bf94274e2d99751ef3b0208`
  - `tools/cli/README.md` `e3a54cd7cbff9ece775c36f22ca91bd587a8c513040224b99fe1d6a45d159917`
  - `tools/llama-bench/README.md` `46825a7bf868295d927366b5960ca7154523402c5e8cbe8cb9b019fc425471e6`
- Passages:
  - `README.md:65` — "- Plain C/C++ implementation without any dependencies"; `:67` — "- AVX, AVX2, AVX512 and AMX support for x86 architectures"; `:69` — "- 1.5-bit, 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, and 8-bit integer quantization for faster inference and reduced memory use"
  - `README.md:34-35` — "- Download pre-built binaries from the [releases page](https://github.com/ggml-org/llama.cpp/releases)" / "- Build from source by cloning this repository - check out [our build guide](docs/build.md)"
  - `docs/build.md:33-39` — "## CPU Build / Build llama.cpp using `CMake`: / ```bash / cmake -B build / cmake --build build --config Release"
  - `docs/build.md:44` — "- For faster compilation, add the `-j` argument to run multiple jobs in parallel, or use a generator that does this automatically such as Ninja. For example, `cmake --build build --config Release -j 8` will run 8 jobs in parallel."
  - `grammars/README.md:3` — "GBNF (GGML BNF) is a format for defining [formal grammars](https://en.wikipedia.org/wiki/Formal_grammar) to constrain model outputs in `llama.cpp`. For example, you can use it to force the model to generate valid JSON, or speak only in emojis. GBNF grammars are supported in various ways in `tools/cli`, `tools/completion` and `tools/server`."
  - `grammars/README.md:143` and `:148` — "`llama.cpp` supports converting a subset of https://json-schema.org/ to GBNF grammars:" … "- In [llama-cli](../tools/cli) and [llama-completion](../tools/completion), passed as the `--json` / `-j` flag"
  - `grammars/README.md:151` — "> The JSON schema is only used to constrain the model output and is not injected into the prompt. The model has no visibility into the schema, so if you want it to understand the expected structure, describe it explicitly in your prompt."
  - `grammars/README.md:207` — "- Unsupported features are skipped silently."
  - `tools/cli/README.md:134-136` — "| `--grammar GRAMMAR` | BNF-like grammar to constrain generations (see samples in grammars/ dir) |" / "| `--grammar-file FNAME` | file to read grammar from |" / "| `-j, --json-schema SCHEMA` | JSON schema to constrain generations (https://json-schema.org/), e.g. `{"type": "object"}` for any JSON object |"
  - `tools/llama-bench/README.md:88-89` — "- Prompt processing (pp): processing a prompt in batches (`-p`)" / "- Text generation (tg): generating a sequence of tokens (`-n`)"
  - `tools/llama-bench/README.md:94` — "Each test is repeated the number of times given by `-r`, and the results are averaged. The results are given in average tokens per second (t/s) and standard deviation. Some output formats (e.g. json) also include the individual results of each repetition."
  - `tools/llama-bench/README.md:141-142` (table "Different numbers of threads") — "| llama 7B mostly Q4_0           |   3.56 GiB |     6.74 B | CPU        |          1 | pp 64      |      6.17 ± 0.07 |" / "| llama 7B mostly Q4_0           |   3.56 GiB |     6.74 B | CPU        |          1 | tg 16      |      4.05 ± 0.02 |"; `:145-146` — "| llama 7B mostly Q4_0           |   3.56 GiB |     6.74 B | CPU        |          4 | pp 64      |     23.18 ± 0.06 |" / "| llama 7B mostly Q4_0           |   3.56 GiB |     6.74 B | CPU        |          4 | tg 16      |     12.22 ± 0.07 |"
  - `tools/llama-bench/README.md:187-188` — "| qwen2 7B Q4_K - Medium         |   4.36 GiB |     7.62 B | CUDA       |  -1 |           pp512 |      7340.20 ± 23.45 |" (model size only used here)
- Coverage: T15 / T11 method — covers: build on the runner from source with CMake (cmake and gcc are on the image, S4-01) or use release binaries; JSON-constrained output via `llama-cli -j/--json-schema` or `--grammar(-file)` (GBNF; schema subset, unsupported features skipped silently, schema not shown to the model); throughput measurement via `llama-bench` (prompt-processing and generation t/s, mean ± sd over `-r` repetitions, JSON output with per-repetition results). End-to-end latency for a short JSON answer would be derived as prompt tokens / pp-rate + output tokens / tg-rate, or timed directly around one `llama-cli` call; the README itself notes no such end-to-end figure. Model sizes: 7B Q4_0 3.56 GiB, Qwen2 7B Q4_K_M 4.36 GiB — both within the runner's 16 GB (public) / 8 GB (private) RAM and 14 GB SSD (S4-02). The CPU-thread table is the README's example without CPU model, date or commit named — not usable as a T11 value and not a runner observation. T11 (decoding documentation): partly covers what GBNF/JSON schema constrains (the S2 reader owns that topic). Other topics: does not cover.
- Observation? No (example tables without machine named).
- Availability on the runner: llama.cpp is not on the image (S4-01) and not an Ubuntu 24.04 package (S4-09).

### S4-09 — packages.ubuntu.com, Ubuntu 24.04 "noble" package pages

- Citation: Canonical, packages.ubuntu.com, suite noble / noble-updates.
- Copies read (all accessed 2026-10-07, local `sources/S4-09/`):
  - `https://packages.ubuntu.com/noble/linux-tools-common` — SHA-256 `62913e2f18ddb6763410de93e2d49fed210e7af29712c0a09d3c82b63e0192ac`
  - `https://packages.ubuntu.com/noble/linux-tools-azure` — `2575f3d281b18a5c79ff5775927d397630c5c15bfc6c5671b276da51e241fed8`
  - `https://packages.ubuntu.com/noble-updates/linux-tools-6.17.0-1022-azure` — `3096196ba49b36eb1b458bb45e8ef7604e8ff6bcc03d97837d0910877817df70`
  - `https://packages.ubuntu.com/noble/sysstat` — `1dca9cd0e7f2081058ece3888a5a55396aaaed0b56bb6773eea15a08fe4e0d91`
  - `https://packages.ubuntu.com/noble/rt-tests` — `db2d21941608b919e42b000826d426eaf5a7b6fd0f2b979ef345636bb346d433`
  - `https://packages.ubuntu.com/noble/lmbench` — `e4ec7f7163324ab924c29f01957ec7cdad5ef25b86f3be2daf6925a2196685ca`
  - `https://packages.ubuntu.com/noble/llama.cpp` — `1050db90e7e06cad5486c7412cd755e4840375e3d1282e37226c949cc8bf5008`
- Passages (page headings, verbatim):
  - linux-tools-common: "Package: linux-tools-common (6.8.0-142.142)"; "Linux kernel version specific tools for version 6.8.0"
  - linux-tools-azure: "Package: linux-tools-azure (7.0.0-1014.14~24.04.1 and others)"; "Linux kernel versioned tools for Azure systems."; dependency list: "linux-tools-7.0.0-1014-azure [amd64] … Linux kernel version specific tools for version 7.0.0-1014"
  - noble-updates: "Package: linux-tools-6.17.0-1022-azure (6.17.0-1022.22)"; "Linux kernel version specific tools for version 6.17.0-1022"
  - sysstat: "Package: sysstat (12.6.1-2)"; "system performance tools for Linux"
  - rt-tests: "Package: rt-tests (2.5-1)" "[universe]"; "Test programs for rt kernels"
  - lmbench: "Package: lmbench (3.0-a9+debian.1-6build3)"; "Utilities to benchmark UNIX systems"
  - llama.cpp: "Error … Package not available in this suite."
- Coverage: T15 — covers installability on Ubuntu 24.04: perf for the runner's exact kernel is packaged as `linux-tools-6.17.0-1022-azure` in noble-updates (the `linux-tools-azure` metapackage at access time pointed at 7.0.0-1014, so installing the metapackage alone would not match the runner's 6.17 kernel); sysstat, rt-tests (universe) and lmbench are packaged; llama.cpp is not packaged for noble. Whether the runner's apt sources enable universe/the lmbench component, and whether `apt-get install` of these succeeds on the runner, was not observed. Other topics: does not cover.
- Observation? No.

### S4-10 — lmbench `lat_ctx(8)`

- Citation: Carl Staelin and Larry McVoy, `lat_ctx(8)`, lmbench, "$Id: lat_ctx.8 1.2 00/10/16 17:13:42+02:00 staelin@hpli8.hpli.hpl.hp.com $"; copy from the `intel/lmbench` GitHub mirror (not the original distribution).
- Copy read: `git clone --depth 1 https://github.com/intel/lmbench` at `27b43aeec9dc0bb45f420388c78e42dde4c23bf0`, file `doc/lat_ctx.8`; accessed 2026-10-07; local `sources/S4-10/lat_ctx.8`; SHA-256 `04015eb32f5378d88dbcf7945d00bd484247e9a7fa6ec881943e9f5191c6c634`.
- Passages:
  - `lat_ctx.8:24-29` — "lat_ctx measures context switching time for any reasonable number of processes of any reasonable size. The processes are connected in a ring of Unix pipes.  Each process reads a token from its pipe, possibly does some work, and then writes the token to the next process."
  - `lat_ctx.8:47-57` — "The pollution of the caches results in larger context switching times for the larger processes.  This may be confusing because the benchmark takes pains to measure only the context switch time, not including the overhead of doing the work.  The subtle point is that the overhead is measured using hot caches. … a context switch is defined as the switch time plus the time it takes to restore all of the process state, including cache state.  This means that the switch includes the time for the cache misses on larger processes."
  - `lat_ctx.8:62-64` — "Each subsequent line is a pair of numbers that indicates the number of processes and the cost of a context switch.  The overhead and the context switch times are in micro second units.  The numbers below are for a SPARCstation 2."
  - `lat_ctx.8:78-80` — "The numbers produced by this benchmark are somewhat inaccurate; they vary by about 10 to 15% from run to run.  A series of runs may be done and the lowest numbers reported."
- Coverage: T15 / T10 method — covers the pipe-ring context-switch benchmark: it subtracts the measured pipe-passing overhead ("ovr") to report per-switch cost in µs, and with `-s <size_in_kbytes>` includes cache-refill effects ("direct cost and with cache effects" in T10's terms); stated run-to-run variation 10–15%, report lowest. The only numbers (SPARCstation 2) are not current x86 and not a runner. Other topics: does not cover.
- Observation? The example is one machine named (SPARCstation 2) without kernel, date or window; not a runner, not current hardware.

---

## 3. Method a later runner measurement would use (derived from the passages above; not executed on a runner)

Runner: `runs-on: ubuntu-24.04` (not `ubuntu-latest`, which moves to 26.04 in November 2026 — S4-01:3); record `uname -a`, `nproc`, `/proc/cpuinfo` model name, image version (`$ImageVersion` / README version), job start/end time, and repository visibility (4 vs 2 vCPU — S4-02).

| Quantity (topic) | Method on the runner | Documentation |
|---|---|---|
| Context switches per second, idle and under load (T10) | Read `ctxt` from `/proc/stat` before/after a fixed window (e.g. 5 s, repeated); rate = Δctxt/Δt, per core = rate / nproc; cross-check with `vmstat 1 N` `cs` column, discarding the since-boot first line. "Load" = the same window while a named workload runs (e.g. the build of llama.cpp, or `stress-ng`). Note the runner is never truly idle: the runner agent and the job's own shell are running. | S4-03 ("ctxt … The number of context switches that the system underwent"), S4-04 ("cs: The number of context switches per second", first report = since boot) |
| Context-switch cost (T10) | `sudo apt-get install linux-tools-6.17.0-1022-azure` (kernel-matched), then `taskset -c 0 perf bench sched pipe -l 1000000`, repeated; per switch ≈ (µs/op) / 2. Fallback without perf: a compiled C pipe ping-pong pinned with `taskset` (as in §4), or `lmbench lat_ctx -s 0 2` and `-s 64 2` for the cache-effect variant. State that `perf bench sched pipe` and the ping-pong measure syscall + wakeup + switch round trips, not a bare switch; lat_ctx subtracts measured overhead. | S4-05, S4-09, S4-10 |
| Scheduling decisions per second and scheduling latency (T10) | `cat /proc/schedstat` before/after a window: field 3 (schedule() calls) Δ/Δt per CPU; mean wait per timeslice = Δfield 8 / Δfield 9. If `/proc/schedstat` is absent (no CONFIG_SCHEDSTATS) or `kernel.sched_schedstats=0`, use `sudo perf sched record -- <workload>` then `perf sched latency` (avg/max delay per task) and `perf sched timehist` (per-event sch delay). | S4-07, S4-06 |
| Small quantized LLM latency, short JSON output (T11) | Build llama.cpp from source with CMake on the runner (or download a release binary); download a 1–8B GGUF (e.g. Q4 ≈ 3.5–4.4 GiB for 7B; fits 16 GB/8 GB RAM and 14 GB SSD); `llama-bench -m <gguf> -p <prompt_len> -n <out_len> -r 5 -t <nproc> -o json` for pp/tg t/s; time `llama-cli -m <gguf> -j '<schema>' -n <max> -p '<prompt>'` end-to-end, wall clock, repeated, cold and warm (page cache). Report model file, quantization, commit, threads, prompt/output token counts. | S4-08, S4-02 |

Caveats a runner measurement must state (from S4-02): the VM is in Azure and the docs do not say whether vCPUs are dedicated; the CPU model is not documented and can vary between jobs, so each job must record it; `ubuntu-slim` is an unprivileged container where "accessing low-level kernel features" is unsupported, so it cannot be used for perf/schedstat.

---

## 4. Sandbox illustration (not a runner)

**These numbers were measured in this Claude Code cloud sandbox on 2026-10-07 (~21:18–21:25 UTC). This is a different machine from any GitHub Actions runner: a different kernel (6.18.44-fc-v77, not 6.17.0-1022-azure), a container (`systemd-detect-virt` → `docker`) inside a hypervisor, a different host. They are not a runner observation and must not be cited as one or as a T10/T11 value for a runner.** They only show that the method runs and what its output looks like.

Machine identification (verbatim):
```
$ uname -a; nproc; cat /proc/cpuinfo | grep 'model name' | head -1
Linux vm 6.18.44-fc-v77 #1 SMP PREEMPT_DYNAMIC @0 x86_64 x86_64 x86_64 GNU/Linux
4
model name	: Intel(R) Xeon(R) Processor @ 2.10GHz
$ free -m | head -2
               total        used        free      shared  buff/cache   available
Mem:           16094         543       15375          13         396       15550
$ cat /proc/sys/kernel/sched_schedstats; head -3 /proc/schedstat
cat: /proc/sys/kernel/sched_schedstats: No such file or directory
head: cannot open '/proc/schedstat' for reading: No such file or directory
$ systemd-detect-virt
docker
$ which perf pidstat     # both absent (no output)
```
So in the sandbox `/proc/schedstat` is unavailable and perf is not installed; scheduling latency (T10 third quantity) could not be illustrated here.

Context-switch rate at "idle" over 5 s from `/proc/stat` `ctxt` (the sandbox is not truly idle: the agent harness and this shell are running):
```
ctxt_before=545355 ctxt_after=551079 t0=1791407930.503783360 t1=1791407935.510023223
cs/s=1143.4
```
→ 5,724 switches in 5.006 s ≈ 1,143 /s system-wide (4 CPUs) ≈ 286 /s per CPU. Cross-check `vmstat 1 6` (first line is the since-boot average):
```
procs -----------memory---------- ---swap-- -----io---- -system-- -------cpu-------
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st gu
 0  0      0 15746584   8552 401292    0    0   552   426  707    2  2  1 97  0  0  0
 0  0      0 15747460   8552 401456    0    0     0     0 1163 1190  3  1 95  0  0  0
 1  0      0 15746152   8552 401492    0    0     0   572  992 1047  3  2 95  0  0  0
 0  0      0 15739920   8552 401520    0    0     0    16  961  993  7  2 90  0  0  0
 0  0      0 15742928   8556 403212    0    0     0     8 1287 1433  4  1 94  0  1  0
 0  0      0 15727244   8556 403240    0    0    76     8  793  914  3  1 96  0  0  0
```

Pipe ping-pong (perf absent, so a C program). Script `sources/S4-sandbox/pingpong.c` (SHA-256 `c957537fcfe6f495e9bafd90a99755101bc26080128f3cca8ba8e9caa4d8c8dc`), compiled with `gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`, `-O2`:
```c
/* Pipe ping-pong between two processes. Run under `taskset -c N` so both
 * processes share one CPU: each round trip = 2 write+read syscall pairs and
 * 2 context switches. Prints mean ns per round trip. */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <sys/wait.h>
int main(int argc, char **argv) {
    long n = argc > 1 ? atol(argv[1]) : 200000;
    int p2c[2], c2p[2]; char b = 'x';
    if (pipe(p2c) || pipe(c2p)) { perror("pipe"); return 1; }
    pid_t pid = fork();
    if (pid == 0) {
        for (long i = 0; i < n; i++) {
            if (read(p2c[0], &b, 1) != 1) _exit(1);
            if (write(c2p[1], &b, 1) != 1) _exit(1);
        }
        _exit(0);
    }
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long i = 0; i < n; i++) {
        if (write(p2c[1], &b, 1) != 1) return 1;
        if (read(c2p[0], &b, 1) != 1) return 1;
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    waitpid(pid, NULL, 0);
    double ns = (t1.tv_sec - t0.tv_sec) * 1e9 + (t1.tv_nsec - t0.tv_nsec);
    printf("round_trips=%ld total_s=%.4f ns_per_round_trip=%.1f\n", n, ns / 1e9, ns / n);
    return 0;
}
```
Run (each run bracketed by `/proc/stat` `ctxt` reads), pinned to CPU 1 with `taskset -c 1`, then once unpinned:
```
round_trips=200000 total_s=0.6261 ns_per_round_trip=3130.6
ctxt_delta=400687
round_trips=200000 total_s=0.6253 ns_per_round_trip=3126.4
ctxt_delta=401132
round_trips=200000 total_s=0.6177 ns_per_round_trip=3088.5
ctxt_delta=400502
-- unpinned (no taskset):
round_trips=200000 total_s=4.7913 ns_per_round_trip=23956.4
```
Reading: pinned, ≈ 3.09–3.13 µs per round trip (3 runs); `ctxt_delta` ≈ 400,500–401,100 for 200,000 round trips confirms ≈ 2 context switches per round trip, so ≈ 1.55 µs per (switch + one write/read syscall pair + wakeup). The same windows give a "under load" system-wide rate of ≈ 400,700 / 0.62 s ≈ 640,000 switches/s on one CPU. Unpinned, the two processes run on different CPUs and the round trip (≈ 24 µs) measures cross-CPU wakeup, not a switch — which is why the method pins. One machine (this sandbox), one subject (the ping-pong), windows as stated; three repetitions; no variance analysis beyond the three values. No LLM model was downloaded or run (disk limits; instruction).

---

## 5. Coverage summary per topic for this class

- T1–T9, T12–T14: this class (own measurement on a CI runner) does not apply — these topics are claims about what documents say or about published measurements, which a runner cannot observe. One line each:
  - T1: S4 not applicable (claims about ghOSt/sched_ext/scx documents).
  - T2: S4 not applicable (claims about scx_lavd documentation, talks and reports).
  - T3: S4 not applicable (claims about textbook/paper/kernel-doc content).
  - T4: S4 not applicable (claims about learned-scheduler papers).
  - T5: S4 not applicable (claims about LLM-agent papers).
  - T6: S4 not applicable (claims about vendor game-mode documentation).
  - T7: S4 not applicable (claims about man pages, vendor docs, unit files and surveys).
  - T8: S4 not applicable (claims about rule-daemon repositories).
  - T9: S4 not applicable (claims about theory papers and kernel docs).
  - T12: S4 not applicable (desktop session durations are not observable on a CI runner).
  - T13: S4 not applicable (claims about documented audio/display parameters).
  - T14: S4 not applicable (historical reports).
- T15: covered as *capability and method* by S4-01 (image: Ubuntu 24.04.5, kernel 6.17.0-1022-azure, image 20260927.320.1; no perf/sysstat/rt-tests/llama.cpp installed), S4-02 (fresh Azure VM per job, 4 vCPU/16 GB/14 GB SSD public, 2 vCPU/8 GB/14 GB private, passwordless sudo; ubuntu-slim is an unprivileged 1-CPU container without low-level kernel features), S4-09 (kernel-matched perf, sysstat, rt-tests, lmbench installable; llama.cpp not packaged), S4-03..S4-08, S4-10 (methods). **Not covered as an observation**: no runner run was made.
- T10 (via T15): methods only (S4-03..S4-07, S4-10); no runner value. Sandbox illustration only (§4), not a runner.
- T11 (via T15): method only (S4-08; model size vs runner RAM/disk from S4-02/S4-08); no runner or sandbox value.

---

## 6. Not found

- **T15 / T10 — any observation on a GitHub-hosted runner** of context switches per second, context-switch cost, or scheduling latency: none. This reader cannot run a job on a runner (stated above). Searches #14 (WebSearch: `GitHub Actions ubuntu runner "perf bench sched pipe" context switch measurement`) returned no published runner measurement; the one lead on perf on runners (actions/runner-images issue #4974) could not be read: github.com HTML 403, api.github.com 403, GitHub MCP access denied (search #15).
- **T15 / T11 — any observation of llama.cpp latency on a GitHub-hosted runner CPU**: none. Search #16 (WebSearch: `llama.cpp benchmark GitHub Actions runner CPU tokens per second GGUF`) returned no runner measurement; llama.cpp's own llama-bench example tables (S4-08) name no machine. No model was downloaded in the sandbox.
- **Runner CPU model, vCPU dedication, PMU/perf-event availability, CONFIG_SCHEDSTATS on 6.17.0-1022-azure, free disk on the runner**: not stated by S4-01 or S4-02; not found in the searches above; would only be established by a runner job recording `/proc/cpuinfo`, `/boot/config-$(uname -r)` (or `/proc/schedstat` existence), `perf stat -e cycles true`, and `df -h`.
- **T1–T9, T12–T14**: not applicable to this class (see §5); no searches run for them by this reader.
