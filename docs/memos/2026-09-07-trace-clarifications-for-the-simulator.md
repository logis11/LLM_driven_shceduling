# Trace clarifications for the simulator — what the harness needs from the trace, and why

> Status: memo · Created 2026-09-07 · Updated 2026-09-07
> From 인지오 to 인경민. Written at the end of the Phase 5 spec session, where the metric definitions were fixed by hand-writing mock traces. Nothing here changes the trace format: no new event type, no new field. Everything here is a clarification of what an existing line means, plus one piece of advice. Please read it before deciding the open questions in `simulator-guide.md` §9, because three of them decide whether the harness can compute the paper's numbers at all.

## 1. The one-paragraph version

The harness computes every metric after the fact from the trace and never re-implements the simulator's semantics. That only works if the trace records the *boundaries* of things: when a keystroke was consumed, when a frame's tick was consumed, when one chain stage handed a frame to the next. Three of those boundaries are invisible in the trace today whenever the task in question did not have to wait. This memo asks for one rule that makes them visible — **emit a `ready` line every time a blocking primitive completes, even when it completed instantly** — and for two decisions in §9 to go the way the harness assumes. Then it explains one thing the harness does on its own (frame latency for the game chain), so you know you do not have to emit it.

## 2. What the harness reads, in plain terms

`data-contracts.md` §9 defines seven event types. The harness pairs them up:

- `ready` → the next `run_start` of the same task. The gap is *how long the task waited for the CPU after it became runnable*. For the editor, with `cause: wake`, that gap is the keystroke's scheduling delay — the number that decides whether typing feels laggy. For a frame task, with `cause: timer_tick`, it is how long the frame waited to start.
- `run_start` → `run_end`. An occupancy interval. Summed per task this is how much CPU the task got; summed over all tasks it is how busy the lane was.
- `task_arrive` → `task_end` with `reason: exit`. Turnaround for a finite task such as `make` or a compiler child.
- `config_applied` lines mark when each schedule entry took effect, so the harness can say what fraction of the run was spent under `fallback`, `held`, `clamped`, or `unmodified` configurations.

Everything the paper reports is an aggregate over those pairs. So the harness's whole correctness rests on one property: **every boundary that matters produces a line.**

## 3. Where a boundary goes missing today

The trace contract says `ready` is "the moment a task becomes runnable". Read literally, a task that never stopped being runnable never emits one. That happens in exactly the cases the experiment cares about most: when the machine is overloaded.

### 3a. A keystroke queued mid-burst (`simulator-guide` §9.1)

The editor is in the middle of a long `RUN` when the next keystroke's `wake` event fires. It is not waiting on anything, so nothing happens yet. When it reaches its next `WAIT input:editor`, the queued keystroke is there and the `WAIT` completes instantly. The editor never blocked, so under the literal reading there is no `ready` line and no `run_start` line for that keystroke.

Consequence for the harness: the keystroke disappears from the count. A configuration that starves the editor so badly that keystrokes pile up would show *fewer* stimuli, and its latency distribution would be computed over the keystrokes it handled comfortably. The metric would reward exactly the behaviour it is meant to punish.

### 3b. A frame task in backlog (`simulator-guide` §4, the backlog rule)

A frame task on a 16,667 µs grid gets held off the CPU long enough that two ticks pass. The guide's rule is right: the next two `TIMER`s complete immediately, one per loop iteration, so the task rattles off the overdue frames back to back. But from the trace's point of view that is one long occupancy interval with no `run_end`, no `ready`, and no visible boundary between frame k and frame k+1. The harness cannot tell where one job ended and the next began, so it cannot compute per-frame latency for exactly the frames that were late.

### 3c. A chain stage whose next wake was queued

The game chain is sixteen tasks: `game.chain.1` ticks on the TIMER, runs, and `WAKE`s `game.chain.2`; each stage `WAIT`s on its own channel, runs, and wakes the next. Under load, stage 7 can still be running frame k when stage 6 wakes it for frame k+1. If the wake is remembered, stage 7's next `WAIT` completes instantly and, again, no line marks the boundary between its two iterations.

## 4. The rule that fixes all three

> **A `ready` line is emitted every time a blocking primitive completes — `WAIT`, `TIMER`, `SLEEP`, and the fork-slot wait — with its usual `cause`. If the primitive did not actually block, the line is emitted at that instant with the task already running.**

In other words, `ready` means "a blocking primitive completed", not "the task stopped being unrunnable". The five `cause` values stay as they are. No field is added. The only change is that in the instant-completion case a line appears that today would not.

What the harness does with it: if a `ready` line falls *inside* the task's own occupancy interval (between a `run_start` and its `run_end`), the wait is recorded as **zero**. You do not need to split the occupancy, emit a fake `run_end`/`run_start` pair, or do anything else. Just emit the line.

Why this is cheap for you: you already know the exact instant a `TIMER` or `WAIT` is consumed, because that is where your interpreter advances the task's program counter. The line goes there.

Why it matters beyond the metrics: with this rule the count of `ready(cause: wake)` lines for the editor equals the number of keystrokes it consumed, and the count of `ready(cause: timer_tick)` lines for a frame task equals the number of ticks it consumed. The harness will check those counts against the workload file. A lost keystroke or a skipped tick becomes a failed guard instead of a silently wrong number.

## 5. Two §9 questions the harness has taken a position on

### 5a. §9.1 — a wake with no waiter: **remembered, with depth**

The harness's frame-latency computation (§6 below) assumes that iteration k of every chain stage corresponds to tick k of the head. That is only true if wakes are queued: if stage 6 wakes stage 7 twice while stage 7 is busy, stage 7 must later complete two `WAIT`s, not one. A "lost" or "collapsed" wake would silently drop a frame from the middle of the pipeline, and the harness would then pair the wrong tick with the wrong completion for every frame after it.

The same holds for the editor, for the reason in §3a. The guide already leans this way ("the mailbox-with-depth reading is probably the realistic one"). The harness's mock traces are written on this assumption, and the harness guards that a chain tail's iteration count equals the head's tick count, so if you decide otherwise the guard will tell us immediately rather than the numbers quietly changing.

### 5b. §9.3 — simultaneous events: **any deterministic order, written down**

The harness does not depend on which order you choose. It does depend on the order being fixed and documented, because the mock traces have to encode some order, and because two same-instant lines with different orders are two different traces (the byte-identical-rerun test, non-negotiable 4). Please write the rule next to the tie-break for schedule entries, as the guide already suggests.

## 6. Something the harness does itself: frame latency for the game chain

You do not need to do anything for this section. It is here so that the `deadline` line's role is clear.

The `deadline` line is emitted per TIMER task, per job, with the working definition "job k completes when the task next reaches a TIMER". In the game chain only the head, `game.chain.1`, has a TIMER, and its job is done after its own sub-millisecond burst. So the head's `deadline` line answers "did the input stage finish its 230 µs before the next tick", which is almost always yes. The frame is actually done when `game.chain.16` finishes iteration k, and nothing in the trace labels that moment "frame k".

The harness reconstructs it: it reads the run file, follows the `WAKE` targets from the TIMER-headed task to find the chain and its tail, and computes frame k's latency as the tail's k-th iteration end minus tick k. For a single-stage periodic task such as `mpv` or `gamescope`, the chain has length one and this reconstruction gives exactly what your `deadline` line says — so the harness uses your `deadline` lines as a cross-check on its own computation, and a disagreement is a bug on one side or the other. Please keep emitting them exactly as the contract says.

One small correction we will make on our side: the `deadline` example in `data-contracts.md` §9 names `game.chain.16` as the task, which is the tail; under the rule it would be `game.chain.1`. We will fix the example when the metrics doc lands.

## 7. Advice, not a contract line: you can stop at the workload's end

No document says when a run ends. Every coreset file's last pinned event is a segment-bound depart (the terminal telemetry snapshot's instant), but a finite task can outlive it: `c2-p1a`'s training run has 130 s of work from t = 60 s in a file whose labels end at 180 s, so it would keep running alone past the end.

The harness fixes its observation window as `[0, T_end]`, with `T_end` read from the run file, and reads nothing after it. Any task still alive at `T_end` is recorded as "not completed within the window"; it is never recorded as "completed late". So whether you keep simulating past `T_end` makes no difference to any number. Stopping there is safe and saves time; it is your call.

## 8. Summary of what we ask

| # | Item | Kind | What breaks without it |
|---|---|---|---|
| 1 | `ready` line at every blocking-primitive completion, at zero wait if it did not block (§4) | contract clarification, no format change | queued keystrokes vanish; late frames and chain hand-offs have no boundary |
| 2 | §9.1 decided as remembered-with-depth (§5a) | your decision, harness assumes it | frames silently dropped mid-chain; tick/iteration pairing wrong thereafter |
| 3 | §9.3 tie-break order written down (§5b) | your decision, any order | mocks and reruns cannot be byte-compared |
| 4 | Keep emitting `deadline` lines as the contract says (§6) | nothing new | the harness loses its cross-check |
| 5 | Stop at the workload's end if you like (§7) | advice | nothing; the harness never reads past it |

If any of 1–3 goes differently, tell 인지오 before the harness's mock traces are finalised, because they encode these assumptions and would be changed deliberately rather than discovered wrong later. The full reasoning behind each item is in `_dev/archive/2026-09-07-phase-5-primitive-metrics.md`.
