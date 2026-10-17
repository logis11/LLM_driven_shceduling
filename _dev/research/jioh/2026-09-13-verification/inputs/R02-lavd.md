# Reader input R02-lavd

## lavd-ossna24
### Bibliographic entry
- cite: Min, C. (2024). "Optimizing Scheduler for Linux Gaming." Talk, Open Source Summit North America 2024, Seattle, 2024-04-17. Slides: static.sched.com/hosted_files/ossna2024/9b/scx-lavd-oss-na24.pdf; schedule page: ossna2024.sched.com/event/1aBOT (accessed 2026-08-26).
### Topics
- C-lavd-1: on the slides, the number of tasks observed while a game runs, which game(s) and system it was measured on, and whether it is a count, average or range.
- C-lavd-2: on the slides, the share of tasks classified as long-lived versus short-lived during gaming, and how "long-lived" is defined.
- C-lavd-3: on the slides, which non-game server processes appear among scheduled tasks and what share of scheduling activity they account for, and how "share of scheduling" is measured.
- C-lavd-4: on the slides, whether wine/wineserver (and graphics/audio components) are shown as linked with game tasks in the waker/wakee relationships, and at which slide.
- C-lavd-5: on the slides, the per-schedule runtime figures reported for game-related tasks — which tasks are named, what statistic each figure is (average, maximum, percentile), and the values.
- C-lavd-6: on the slides, whether a task's runtime per scheduling is described as consistent over time, and in what terms.
- C-lavd-7: on the slides, the breakdown of what causes scheduling events (e.g. blocking system calls vs timer preemption) during gaming, the shares, and any named system calls.
- C-lavd-8: on the slides, how game-related tasks wake one another (the depicted structure, its shape, and the stages it names between input and output).
- C-lavd-9: on the slides, the frame time budget and any targeted latency value stated for the gaming scenario, and the frame rate it corresponds to.
- C-lavd-10: on the slides, how concentrated scheduling activity is across tasks (how many top tasks account for what share) and how the share is measured.
- C-lavd-11: on the slides, the number of game (as opposed to non-game) tasks that dominate scheduling, their combined share, and whether they are described as frame-critical or as a pipeline.
- C-lavd-12: on the slides, what is said about the activity of tasks outside the dominant set (idle, waiting, or otherwise), and at which slide.
- C-lavd-13: on the slides, any CPU utilization figure reported during gaming.
- C-lavd-14: on the slides, how game frame-rate metrics are related to scheduler performance metrics.
- C-lavd-15: on the slides, the hardware (core count) and system on which the gaming observations were collected.
- C-lavd-16: on the slides, whether non-game applications (chat/voice/overlay) are mentioned or shown running during gaming.
- C-lavd-17: on the slides, how task durations are characterized and how latency outliers relate to user-perceived frame problems.
- C-lavd-18: which organizations are stated to ship or deploy the LAVD scheduler, and in what setting.
- C-lavd-19: whether the talk or the scheduler provides any workload description format.
- C-lavd-20: speaker, title, event, date and slide URL of the talk.

## corbet-lwn24
### Bibliographic entry
- cite: Corbet, J. "Sched_ext at LPC 2024." *LWN.net*, 2024-09-26. lwn.net/Articles/991205/ (accessed 2026-08-26).
### Topics
- C-corbet-1: the LWN article on sched_ext at LPC — its date, which conference year it covers, whether it has a section on scx_lavd and what gaming characterization that section gives.
- C-corbet-2: whether that LWN article exists, its date and author.

## scx
### Bibliographic entry
- cite: sched-ext/scx repository. github.com/sched-ext/scx, GPLv2 (pin commit).
### Topics
- C-scx-1: whether scx_lavd lives in the sched-ext/scx repository and the repository's license.
