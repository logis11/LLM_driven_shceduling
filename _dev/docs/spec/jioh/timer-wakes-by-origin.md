# Timer wakes by origin

The Phase 10 item "Timer wakes that find their task behind" (`_dev/TODO.md`), decided by 인지오 on 2026-10-31, before the RQ0 run: how a measured application task's non-keystroke wakes behave when they arrive while the task is not waiting for them, in the dataset, the simulator, the harness and the contracts.

## Scope

- The measured applications' non-keystroke wakes, today all compiled onto the task's `timer:` channel and queued in its mailbox like keystrokes.
- The dataset: the wakes split by origin, re-derived from the campaigns' raw wakeups files, compiled onto two channels; the core set, its variants and the generated layer rebuilt and re-blessed. The workload schema's TIMER description is restated to the skip rule with this re-bless (decided 2026-10-30).
- The simulator's behaviour on the two channels and the trace line it writes, specified here for 인경민 to implement.
- The harness: the latency primitive the 15 non-keystroke terms read, the records, the guard.

## Locked decisions

### 1. Wakes are split by cause

A wake whose cause is a toolkit timer is not queued when its task is not waiting for it; a wake whose cause is input or a message from another thread or process is queued, as a keystroke is. Grounding: the three toolkits' timers do not catch up (`qt-qtimer`, `glib-timeout`, `gecko-nsitimer`); X input events queue (`xlib-xnextevent`).

### 2. The timer channel holds one pending wake, the first

A timer wake that arrives while the task is not blocked on its timer channel waits in the mailbox if the mailbox is empty; one that arrives while a wake is already waiting is dropped, and its (WAIT, RUN) pair passes without work when the program reaches it. The task's next WAIT on the channel completes at once with the waiting wake, whose latency is measured from its own arrival. Keystroke pairs keep their order.

### 3. A dropped wake has a latency row

Each dropped timer wake gets a latency row, its value the start of the one service that covered it minus its own arrival, marked `skipped`.

### 4. A new channel kind, `event:<id>`

Timer-caused wakes stay on `timer:<id>` under decision 2; the queued non-keystroke wakes go to `event:<id>`, under the mailbox rule keystrokes follow. Keystrokes stay on `input:<id>`.

### 5. The simulator writes `wake_drop` at the drop

At the instant a timer wake is dropped the simulator writes one trace line, event `wake_drop`, with the wake's time, its task and its channel. A dropped wake's pair, passed later, writes no line — an exception to the RQ0 gate spec's conformance item (a), a `ready` line at every completed blocking primitive.

### 6. Every source of an application's wakes is split

Components and focus components, operations, launch streams, trace-replay streams and heavy events alike: an observed stream's wakes each take their own origin's channel; a sampled component is split as decision 10 states.

### 7. The 15 non-keystroke terms read both channels

The terms that read the timer channel today read the task's `timer:` and `event:` wakes pooled, each wake's latency by its own channel's rule.

### 8. Only a timer origin goes to `timer:`

A wake's origin is the start of its wake chain: walked in time order, a wake by a thread of the application's tree takes the origin of that thread's own last wake, and the X server relays the same way. A chain that starts at a timer interrupt (the wakeup run on an idle CPU) is timer-caused and goes to `timer:`; every other origin — the measurement's input replay, the X server where its own origin is not traced, another process, a kernel thread, a thread not yet woken inside the capture — goes to `event:`.

### 9. Operations follow the same rule; the driver's channels count as input

An operation's wakes are split by decision 8. The measurement driver's channels into the application count as input: xdotool and the driver's processes, and GIMP's Script-Fu server, through which the driver runs unsharp mask.

### 10. Components split in two, the coverage cut per channel

Every component is split into its timer-caused and its other part, each with its gap and run tables re-derived from that part's wakes. The coverage cut of 9.5 D16 — components in descending wake rate until 95 % of the wakes, the rest pooled as one residual — applies within each channel separately.

### 11. One primitive, `app_latency`

`timer_latency` becomes `app_latency`: one row per `timer:` or `event:` wake of a task, its value by the channel's rule (decisions 2 and 3 on `timer:`, the queue on `event:`). The 15 terms read its P99.

### 12. The stimulus guard covers both channels (guard spec 1.4)

On `event:` the rule keystrokes follow: no more `ready` lines than wakes, and no wake lost at a task's end. On `timer:` every wake has exactly one of a service (`ready` line) or a drop (`wake_drop` line); a wake with neither is lost, and a drop while the mailbox is empty or more services and drops than wakes fail the check.
