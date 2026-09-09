# The batch class — who the cap applies to, and the rule the simulator should use to decide it

> Status: memo · Created 2026-09-09 · Updated 2026-09-09
> From 인지오 to 인경민. Specifies the one behavioural rule the config schema promises but nobody has written yet: which tasks are in the **batch class** that `batch_bandwidth_cap` bounds. Comes out of the prior driver table's pair review (`docs/daemon/prior-table-pair-review.md`). Absorb into the simulator guide once implemented. No OS background assumed; the worked examples carry the argument.

## 1. The problem in plain words

Every configuration the simulator receives has three parts: an algorithm (MLFQ, EDF, LOTTERY, FIFO), that algorithm's params, and a number called `batch_bandwidth_cap`. The cap means:

> *While some task that is not batch wants the CPU, the batch-class tasks together may use at most this fraction of it.*

So a cap of 0.05 says "background work gets at most 5 % whenever the foreground has something to do", and a cap of 0.333 says "up to a third". Every row of the driver table sets this number, and the whole `background_wanted` attribute of the recognizer acts through it: the table gives wanted background a generous cap and unwanted background the floor, 0.05.

The cap only touches tasks in the **batch class**. And here is the gap: the config schema says the batch class "is determined behaviorally by the executor (observed CPU-bound behavior — the same evidence MLFQ demotion uses); the classification rule is identical across algorithms, frozen in the simulator's docs, and not configurable". The simulator's docs do not exist yet, so the rule is not written anywhere. This memo writes it.

Why it cannot be by name: the simulator never sees process names or the ground truth. That is deliberate — it is what makes the executor identical across every condition, so a difference between conditions can only come from the recognizer. The simulator sees each task's *behaviour*: when it runs, when it blocks, for how long. The class has to be read off that.

## 2. Why the rule matters: one wrong rule flips a whole file

Take the most obvious rule: *"a task that runs for a whole time slice (2 ms at the boot default) without stopping is batch."* Apply it to the game files.

| task in `c2-p2b` (a game plus a virus scan nobody asked for) | how it behaves | under the obvious rule |
|---|---|---|
| `clamscan` | runs 25 s of CPU without ever stopping | batch — correct |
| `game.chain.1 … 16`, the frame pipeline | one stage per frame, each running 0.2–2.2 ms then handing over; the head is a TIMER at 16.7 ms | the long stages **become batch** |
| `compositor` in `c1-gaming` (`gamescope`) | 6.7 ms of work every 16.7 ms tick | **batch** |

The driver table's `gaming / background_wanted: false` row caps the batch class at 0.05 to protect the frames from the scan. Under the obvious rule the frames themselves are in the batch class, so that cap throttles the game to 5 % of the CPU whenever anything else is runnable. The row built to protect the game would destroy it. The rule decides whether the whole experiment's central knob points the right way.

## 3. The rule

Two parts, both from behaviour the simulator already tracks.

**Rule B1 — entry and reset.** A task **enters the batch class** the moment it has consumed one full time slice of CPU since it last blocked voluntarily. It **leaves the batch class** at its next voluntary block. A voluntary block is a `WAIT` that has to wait, a `SLEEP`, or a `TIMER` that is not yet due — the task giving the CPU back on its own. Being preempted is not a voluntary block; the task stays in whatever class it was in.

"One full time slice" is the running configuration's `timeslice_us` (MLFQ, LOTTERY), or `residual_timeslice_us` under EDF; under FIFO, which has no slice, use the boot default's 2000 µs. This keeps the rule free of any number of its own.

**Rule B2 — the periodic class is never batch.** A task whose program contains a `TIMER`, and every task reachable from it by following `WAKE` targets (the frame chain), is in the **periodic class** and is never batch-class, however long its bursts are. The periodic class is exactly the set EDF treats as its deadline class, and exactly what the harness calls a chain, so the three definitions coincide.

Everything else follows from those two:

- The class is the same under every algorithm, because neither rule looks at the algorithm. Under MLFQ it is *not* the same thing as "being in the bottom queue" — MLFQ's queue level is that algorithm's own state; the class is the executor's.
- Under LOTTERY, `batch_share` is the ticket share of this same class; the non-batch class holds the remainder.
- Under EDF, the deadline class is the periodic class of B2; the residual class is everything else, batch or not.
- The starvation safety net is separate and unchanged: every runnable task, batch or not, makes progress within a bounded window regardless of the cap.

## 4. Worked examples, task by task

The boot slice is 2 ms throughout.

**A hog (`python3` in `c2-p1a`, `clamscan`, `ffmpeg`, a compiler child).** Runs until done, never blocks. Two ms after its first dispatch it enters the batch class and never leaves. With a 0.05 cap and an editor that has something to do, it gets 5 %. This is the case the cap was made for.

**A download (`c2-p2a`'s Steam download).** Its program is "run about 1 ms, sleep about 5.7 ms" 22 000 times — a chunk arrives, gets handled, the task waits for the network. It never reaches a full slice before it blocks, so under B1 it never enters the batch class. **The cap does not apply to it, in any row.** Its progress is decided by the algorithm alone: under EDF it runs in the residual class, in whatever time the frames leave; under MLFQ it stays in the top queue like an interactive task. We know this and accept it (§5); it is the price of deciding by behaviour, and no shipped scheduler would cap it either without someone naming it.

**A backup (`c2-p3b`'s `borg`).** "Run 3 ms, sleep 2 ms", repeated. Two ms into each burst it enters the class; 1 ms later it blocks and leaves. So it is batch for the last third of every burst — the cap bites, partially. Under `backup / wanted: true` (cap 0.2, LOTTERY share 0.2) that is what the row intends.

**The compositor and the frame chain.** The compositor is a TIMER task; the chain's head is a TIMER task and the stages are woken from it. All of them are periodic class under B2, never batch, whatever their burst length. The cap never touches a frame. In `c2-p2b` the 0.05 cap therefore lands on `clamscan` alone.

**An editor (`code`, `soffice.bin`, `kdenlive`).** In the coreset the editors' keystroke bursts are long — a median of 80–90 ms of CPU per keystroke, then hundreds of ms waiting for the next key. So under B1 an editor is non-batch at the instant a keystroke wakes it, becomes batch 2 ms into the burst, and leaves the class when it blocks for the next key. What this means:

- When the keystroke arrives, the editor is non-batch and runnable, so the cap bites on the hog and the editor gets the CPU quickly. The number the harness scores for editors is exactly this wait, `ready_wait` with cause `wake`, so the property that matters is protected.
- Later in the same burst the editor is batch too. If nothing non-batch is runnable at that moment, the cap is off and the editor and the hog share the CPU under the algorithm's ordinary rules. If a periodic task wakes (a renderer heartbeat, a media tick), the cap applies to the editor's burst tail for the microseconds that task runs. That slows burst completion slightly; it does not touch the wake-to-run wait.

**"While non-batch work is runnable."** The cap is not a permanent budget; it is a ceiling that applies only during the stretches when some non-batch task is runnable. A hog alone on the machine runs at 100 % under any cap. The moment an editor wakes, the ceiling is on until the editor blocks again.

## 5. What this settles for one judging file, and what it does not

The pair review found that in `c2-p2a` the `gaming / wanted: true` row's cap of 0.333 is inert — the download never enters the class — while in `c2-p2b` the `gaming / wanted: false` row's 0.05 cap acts on the CPU-bound scan. So p2 tests the attribute in one direction: misreading unwanted CPU work as wanted costs frames (p2b); misreading a wanted download as unwanted costs nothing (p2a). We decided to keep the file and state this rather than reshape the download or the cap: a cap-only mechanism can protect against unwanted CPU work but cannot favour wanted IO-shaped work, and that is a finding worth having. The conclusion holds under any classification rule, since a 1 ms chunk is shorter than every legal slice; B1 just makes it exact.

What the rule does *not* fix and is not meant to: it cannot tell an editor's long burst from a hog's within the burst. Nothing behavioural can; that is the whole reason the recognizer exists. The rule only makes sure the cap protects what the scoring measures (the wake-to-run wait, the frames) and lands on what the row means it for (work that never gives the CPU back).

## 6. Where this comes from

- **B1 is MLFQ's own evidence.** OSTEP ch. 8 (`ostep` in `docs/references.md`): rule 4a, a job that uses up its time slice is demoted; rule 4b, a job that gives up the CPU before the slice ends stays at its level. The config schema's sentence "the same evidence MLFQ demotion uses" is this pair of rules. Solaris's timesharing class (`illumos-ts`) is the same idea as a table: a priority for "quantum expired" and a priority for "returned from sleep".
- **B2 is the periodic task model.** Liu & Layland 1973 (`liu-jacm73`): periodic requests, each due before the next request. Our TIMER tasks are that model, and the harness's chain definition (metrics doc §3: the WAKE path from a TIMER head to its tail) is the closure that keeps a frame pipeline's stages together.
- **The split between "who is CPU-bound" and "who gets capped".** Shipped systems decide the first by behaviour (feedback queues) and the second by declaration (`SCHED_BATCH`, cgroup CPU quotas, `nice` — an admin or the program names the work). We fuse them because the executor may not see names; the recognizer's row is the declaration, at the level of the whole situation rather than per task. That is the design choice behind §5, and the paper will say so.

## 7. Action plan (simulator side)

1. **Implement B1 as executor state, per task, independent of the algorithm:** a counter of CPU consumed since the last voluntary block; the task is batch-class while the counter ≥ the running slice length; reset the counter to zero on every voluntary block (`WAIT` that blocks, `SLEEP`, `TIMER` not yet due). Preemption does not reset it. Use `timeslice_us` (MLFQ, LOTTERY), `residual_timeslice_us` (EDF), 2000 µs (FIFO).
2. **Implement B2 from the program:** at load, mark every task with a `TIMER` and every task reachable from one through `WAKE` targets as periodic class; periodic tasks are never batch-class. This is the same set EDF uses as its deadline class — compute it once.
3. **Apply the cap to the batch class only, and only while a non-batch task is runnable.** How you account the ceiling (the window over which "at most this fraction" is measured) is yours to design; write the window down in the simulator doc, since the harness reads only outcomes. Keep the starvation safety net independent of the cap.
4. **Keep the class identical across algorithms.** LOTTERY's `batch_share` splits tickets between this class and the rest; EDF's residual class contains batch and non-batch tasks alike; MLFQ's queue level is not the class.
5. **Write both rules into the simulator's semantics notes**, beside the switch rules from the 2026-09-08 memo, so the config schema's sentence "frozen in the simulator's docs" becomes true.
6. **Two unit tests that pin the rule:** (a) a task running 1 ms then sleeping 5.7 ms in a loop is never batch-class, however long it runs; (b) a TIMER head waking a two-stage chain whose stages run longer than a slice is never batch-class, while a plain task with the same bursts is batch-class 2 ms into each burst and non-batch again after it blocks.
7. **Optional diagnostic, no contract change:** emit `x_batch_class {t, task, in}` when a task enters or leaves the class. The harness ignores `x_` lines; a check tool beside it can then verify the rule against traces the way `check_mlfq_levels.py` does for switch windows.
