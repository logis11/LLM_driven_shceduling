# Note for jioh — under EDF, are the WAKE-driven chain stages in the deadline class?

> Status: memo · Created 2026-10-01 · Updated 2026-10-10 · **Answered 2026-10-10 — see the end**
> Author: kyungmin. Raised while implementing EDF (stage S of the `steps/` ladder). A question, not a spec change. The full simulator status is in `../memo/memo_261001.md`.

## Checked first: what the repo already answers

Before writing this, I searched the docs for an answer to each question that came up while building EDF and LOTTERY. All but one are already settled, so they are not asked here:

| question | answered by |
|---|---|
| zero-wait `ready` when a blocking primitive completes without blocking | trace-clarifications memo 2026-09-07 §4; metrics.md §6.1, §11.1 |
| cold start on a switch into MLFQ; same-algorithm entries keep the granted slice | switch memo 2026-09-08 §3–§4, §7; metrics.md §11.9 |
| TIMER t₀ | simulator-guide §9.2 leaves it to the builder; on all 24 coreset files the two live readings coincide |
| is the gaming overload intended | coreset-guide demand table: `c1-gaming` at 1.46, calibration class |
| EDF admission control | vocabulary §2: none in v1 |

Your three questions to me in the boot-default memo §5 are mine to answer and are not repeated here.

## The question

Under EDF, a game frame is a chain: `game.chain.1` ticks on a TIMER and WAKEs `game.chain.2`, and so on down to `game.chain.16`. Only the head has a TIMER. **Are stages 2–16 in EDF's deadline class or in its residual class?**

## Why I can't settle it from the docs — three sources, two answers

1. **`docs/recognition-vocabulary.md` §2, EDF:** "The deadline class is the **TIMER-driven** tasks, behaviorally observed; each job's deadline is its next period boundary." Read literally, a WAKE-driven stage is not TIMER-driven, so it is **residual**.
2. **`docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` §3, rule B2:** the periodic class is a TIMER task "and every task reachable from it by following `WAKE` targets (the frame chain)", and "Under EDF, the deadline class is the periodic class of B2." So the stages are in the **deadline class**.
3. **`docs/daemon/prior-table-pair-review.md`**, finding 5 and the C7 `gaming` row: "the chain's woken stages sit in the residual class beside the scan, as in `c2-p2b`, so the floor cap holds the scan off the frames"; "`gaming` is not in this family because the chain's woken stages are residual-class, which is why `c2-p2b` measures its cap." So the stages are **residual**.

The implementation follows source 2. A stage with no TIMER needs a deadline value to be ordered, so it inherits the deadline of the task that woke it (the frame's tick + period). Nothing in the docs gives a stage's deadline either way.

## Why it matters — measured

EDF, boot-default params, no cap (the cap is not implemented yet). Frames are the harness's own `job` rows from `harness/tools/records.py` (metrics §6.2: the tail's iteration end − tick):

| | stages in deadline class (current) | stages in residual class |
|---|---|---|
| `c2-p2b`: frames missed | **0 of 7,199** | **5,189 of 5,201 (99.8%)** |
| `c1-gaming`: TIMER-task `deadline` lines met | 5 of 5,664 | 7,372 of 7,372 |
| `c3-evening`: TIMER-task `deadline` lines met | 9,917 of 20,459 | 25,227 of 25,227 |

What follows from each reading:

- **Deadline class.** On `c2-p2b` the frames are safe under EDF whatever the cap is, because EDF serves every stage before the residual-class clamscan. The p2 pair's rows (`gaming/true` and `gaming/false`, both EDF, differing only in cap 0.333 against 0.05) would then not differ on `game.chain.1`'s frames. That is the same "inert on the cap axis" family as finding 5's `meeting`/`media`, which contradicts the pair review's reason for keeping `c2-p2b` in the judging set. On the overloaded files (`c1-gaming`, `c3-evening`) the whole periodic class collapses together: the head's and the compositor's own deadlines go from all met to almost all missed.
- **Residual class.** Frames on `c2-p2b` compete with the scan in round-robin, so the cap is what protects them, as the pair review assumes. The TIMER tasks' own deadlines hold everywhere. EDF then protects only the chain head, not the frame.

Caveat: these traces still have a known simulator defect (missing zero-wait `ready` lines, memo §5.1). The residual-class `c2-p2b` run raised the harness's chain guard (5,201 tail iterations for 7,199 head ticks), so read that row as indicative, not final.

## What I need

- [x] **Which class** do the WAKE-driven chain stages belong to under EDF: deadline (batch memo B2) or residual (vocabulary wording, pair review)?
- [x] If **deadline class**: is "a stage inherits the deadline of the task that woke it" the deadline you intend?
- [x] ~~If **residual class**: should the batch memo's sentence … be narrowed?~~ — moot.

Switching the implementation either way is a two-line change in `deliver()` (both variants were run for the table above).

## Answer — from jioh, 2026-10-10 (relayed by kyungmin)

- **Deadline class.** Chain stages 2–16 are in EDF's deadline class. The current code stays as it is.
- **Inheritance is intended.** A stage inherits the waker's deadline unchanged: the head's tick + one period. Frames are scored from the head's tick to the tail's end, so ordering the stages by that deadline is the natural choice.
- **Dataset change pending.** jioh is reworking the dataset. In that rework, `c1-gaming` loses the compositor, and `c2-p2b`'s clamscan is replaced by Ubuntu unattended-upgrade. The EDF numbers above must be re-measured after the rebuild.

Consequences on the simulator side:
- D6 is closed: no code change. `steps/README.md` D6 and `src/notes.md` gap 11 are updated.
- Still to re-check after the rebuild: the "Deadline class" consequence above, that the p2 pair's two EDF rows would not differ on `game.chain.1`'s frames. jioh's answer does not address it, and the `c2-p2b` background task is changing. It is on kyungmin's TODO backlog.
