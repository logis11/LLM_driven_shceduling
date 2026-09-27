# Task 9.5 — The untraced control for 9.5, 9.8 and 9.9

The method of the untraced control set by the 2026-09-26 review of 9.5–9.9: whether `perf sched record` over a measured phase moves the values the archetypes carry. Parent: `_dev/TODO.md`, (jioh, 9.5), the item "an untraced control for 9.5, 9.8 and 9.9"; phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`. Decided in the 2026-09-27 grill session.

## Scope

- Every archetype 9.5, 9.8 and 9.9 measured: 14 subjects — 9.5's nine applications, 9.8's four subjects (hidden renderer, visible renderer, chat client, Steam client) and 9.9's session, which carries four entries.
- The control job: its phases, their order and sequence, the instrument, the quantities compared.
- The reading of the ratios and where it is written.
- The dry runs before launch and the release of the raw records.

## Locked decisions

### 1. A traced and an untraced run in the same job

Each control job runs a measured phase twice: traced, under the campaign's `perf sched record` over the whole phase, and untraced, with no `perf`. `/proc` is read over both. Each job gives one ratio per value, the untraced run's over the traced run's.

### 2. Every archetype is controlled on itself

Each of the 14 subjects gets its own control jobs, and each archetype its own ratios and intervals. A difference is written into that archetype's `modeling_notes` as a limitation of its values. No carried value changes.

### 3. The phases paired

Every phase whose values the archetype carries is run as a pair, the driven phases included. That means 9.5's idle, driven, operation and play phases as each application carries them; 9.8's `steady` (hidden renderer), `steady-notimer` (visible renderer), `idle` (chat client) and `shown` (Steam client); and 9.9's `steady`. Phases no archetype carries are left out: 9.5's 136M phase, the visible renderer's phase with the page's timer and the Steam client's minimised phase.

### 4. The two driven runs start from one state

The same prelude runs before each of the two driven runs and returns the application to one designed state. `code-editor`, `web-browser` and `mail-client` use their existing 136M preludes (9.5 D61 and D63: the committed file restored and reverted, the caret at its end; D60 and D62: the page's text box focused and emptied; D79: the message body emptied in its Paragraph format). `office-writer`, `image-editor` and `video-editor` get new ones. Each prelude is checked by the screenshot after it.

### 5. The order alternates across jobs

In half of a subject's jobs the traced run of each pair comes first; in the other half the untraced run does.

### 6. The sequence: the campaign's order, each pair adjacent

A control job follows its campaign's phase order, with each carried phase run as an adjacent pair: the idle pair, then the driven pair (each run after its prelude), then the operation pair. Both idle runs come before any input.

### 7. Each ratio at the grouping of its carried value

- Per component, for the component tables: the wake rate and the run mean.
- Over the whole application tree, for the values carried over the tree: the typing entries' per-input run, and the play phase's CPU share and cycle run.
- The operation's duration, from the operation log, where the phase has an operation.

### 8. Per wake

The run mean is CPU time over voluntary switches, and the wake rate is voluntary switches over the phase's time — the wake of 9.5 D21, a schedule-in preceded by a wakeup, with a resume after preemption folded into its wake. The involuntary switch count is recorded beside them.

### 9. The instrument

Each thread's CPU time comes from its `/proc` `schedstat` (the first field, the scheduler's runtime in nanoseconds). Its voluntary and involuntary switch counts come from its `/proc` `status`. Each job records the runner's `kernel.sched_schedstats` value.

### 10. Threads that exit within a run

Each ratio is taken over the threads alive at both edges of the run. The share of each component's CPU and wakes held by threads that start or exit within the run is read from the traced run's trace and stated beside the ratio.

### 11. The reading: as 9.7 D36 reads a check

The 95 % t interval of the per-job ratios (k − 1 degrees of freedom, the stability rule's multiplier) gives a difference when it excludes 1, and not resolved otherwise. The pooled medians' ratio and the two order groups' mean ratios are reported beside it.

### 12. Many intervals per archetype

Each interval is read at 95 %. The archetype's notes state how many intervals were read and how many differences a 95 % level gives by chance alone.

### 13. Six jobs per subject, fixed in advance

Six control jobs per subject, three in each order, fixed before launch.

### 14. Input windows 1–6

The typing entries' six jobs replay input windows 1–6, the campaign's first six in its own order. Both runs of a job replay the same window.

### 15. The traced runs stay out of the pools

The control's traced runs serve the ratio only. The carried values stay those of the closed pools.

### 16. Builds: 9.5 D69's rule

Where an appdef pins a build, the control runs it under the build gate (`code` 1.138.0). Otherwise the control runs the build the job installs. The build is recorded per job, and the control's build census is stated beside each archetype's ratio, including where it differs from the pool's.

### 17. The traced runs checked against their pool

Each control job's traced run is analysed as a campaign repeat is. Each carried value is placed in the pool's spread in standard deviations, and components that appear or disappear are listed, in the form of 9.5 D69 and D80. A disagreement is a decision taken before the archetype's ratio is written into its notes.

### 18. Everything else follows the family's campaign method

The settles, phase lengths, single-core pin, machine gate on the AMD EPYC 7763 and setup states are those of each family's campaign method.

### 19. Dry runs before launch

One dry run per family checks the control sequence: the pairing, the alternation and the `/proc` reads. One dry run for each of `office-writer`, `image-editor` and `video-editor` checks its new prelude, its screenshots read against the prelude's designed state.

### 20. Where the results are written

The ratio tables go on the family's results pages and in the campaign record. Each archetype's notes carry its control reading (decision 12's counts), with one limitation line for each difference.

### 21. The raw records are released

The raw records of every landed control job and the gate-stop reports are released as the campaigns' were.

### 22. Work a carried value leaves out by a rule read from the trace

Where a component's carried value leaves part of its thread's work out by a rule read from the trace — 9.5 D64's heavy events, 9.9 D23's cron sessions, the wakes 9.9 D27 and D32 trace to packages outside the desktop manifest or to the harness — the ratio is taken over the thread's whole work in both runs. The share the carried value leaves out, CPU and wakes, is read from the traced run's trace and stated beside the ratio.

### 23. An operation phase's components over the whole phase

Each ratio of an operation phase's component is taken over the whole phase: the operation windows and the pauses between them. The share of the component's CPU and wakes inside the operation windows, the [trigger, done) windows its carried value is pooled from (9.5 follow-ups D8), is read from the traced run's trace and stated beside the ratio.

## Invariants

- Every dry run, control launch and release waits on 인지오's approval.

## Open items

- Whether the raw records go out as one release per family or one for the whole control, decided when they are released.
