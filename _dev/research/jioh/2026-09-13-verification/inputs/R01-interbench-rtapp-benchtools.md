# Reader input R01-interbench-rtapp-benchtools

## interbench
### Bibliographic entry
- cite: Kolivas, C. interbench. github.com/ckolivas/interbench, GPL-2.0, v0.31 (pin master commit).
### Topics
- C-interbench-1: in interbench's man page/source, the audio interactive task — how often it wakes, how its CPU demand is specified (percentage, duration, or both) and at what value, and whether a real-time scheduling-policy variant of it exists.
- C-interbench-2: in interbench's man page/source, the video interactive task — its frame or receipt rate / period, the CPU demand it is given and how that demand is expressed.
- C-interbench-3: in interbench's man page/source, the X interactive task — what user activity it emulates, how its CPU demand is specified, whether and how that demand varies (range and variation rule), and whether it is driven by input events.
- C-interbench-4: in interbench, the gaming interactive task — how its CPU demand is bounded and whether it carries deadlines.
- C-interbench-5: in interbench, the Burn background load — what it runs, its default number of threads or processes, and what CPU behaviour each has.
- C-interbench-6: in interbench, the Write background load — what it writes, how the written size relates to system memory, and its access pattern.
- C-interbench-7: in interbench, the Read background load — what it reads, how the file size relates to memory, and whether/how it avoids the page cache.
- C-interbench-8: whether interbench specifies any per-block, per-chunk or per-operation timing for its Write and Read loads.
- C-interbench-9: in interbench, the Compile background load — what it is composed of, whether it runs or emulates `make`, and any parallelism level stated for it.
- C-interbench-10: the complete list of interbench interactive tasks and background loads with each one's definition, including any custom task option, any memory-pressure load and its sizing, and any hackbench-based load and its argument.
- C-interbench-11: which statistics interbench reports per task, whether it states a human-perception jitter threshold (and its value), and its default run length.
- C-interbench-12: how interbench combines interactive tasks with background loads in a run.
- C-interbench-13: interbench's author, repository, license and version string; whether distributions package it.

## rt-app
### Bibliographic entry
- cite: rt-app. github.com/scheduler-tools/rt-app, GPLv2.
### Topics
- C-rt-app-1: rt-app's JSON configuration format — the per-task and global fields it defines and the time unit of its duration fields.
- C-rt-app-2: what rt-app's `timer` event does, what `ref` and `period` mean, whether wake times are absolute or relative to the previous wake, and what happens when an iteration overruns.
- C-rt-app-3: the contents of rt-app's example template configuration.
- C-rt-app-4: rt-app's maintainer organization, license, and whether kernel documentation references it.

## hackbench
### Bibliographic entry
- cite: hackbench, in rt-tests. git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git (`src/hackbench/hackbench.c`, `src/hackbench/hackbench.8`), GPL-2.0. Repository HEAD `fd45df83` at access; `hackbench.c` last modified 2024-05-22, man page dated 2020-09-19 (accessed 2026-09-12).
### Topics
- C-hackbench-1: hackbench's defaults (groups, file descriptors, message size, loops), how many tasks those defaults create, what it reports, and where it is distributed (rt-tests, perf).
- C-hackbench-2: the wording of the LWN article at that number about hackbench.

## schbench
### Bibliographic entry
- cite: Mason, C. schbench. github.com/masoncl/schbench, v1.0.
### Topics
- C-schbench-1: schbench's thread structure, what a request does, which latencies and percentiles it reports, its version and author.

## stress-ng
### Bibliographic entry
- cite: King, C. I. stress-ng. github.com/ColinIanKing/stress-ng, GPL-2.0.
### Topics
- C-stress-ng-1: stress-ng's author, licence, stressor categories, and whether it models timing of real application behaviour.

## kernelbuild
### Bibliographic entry
- (no single source; see topics)
### Topics
- C-kernelbuild-1: in Linux kernel documentation, what `sched_child_runs_first` and `SCHED_AUTOGROUP` are and whether the documentation motivates either with parallel builds.
- C-kernelbuild-2: whether scheduler evaluations commonly use a kernel build; what process structure (short-lived compiler processes vs long-lived make/linker) any cited source describes.
