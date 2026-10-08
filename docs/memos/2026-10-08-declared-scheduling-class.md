# The declared scheduling class — a field in the workload, a rule in the executor

> Status: memo · Created 2026-10-08 · Updated 2026-10-08
> From 인지오 to 인경민 and 박이안. Decisions D4–D6, D16, D18 and D19 of task 9.11 (`_dev/research/jioh/task-9.11-scheduler-constants/changelog.md`). The workload and the run file gain a field, a change to two frozen contracts that needs the three of us (`docs/data-contracts.md` §13). The heads-up memo of 2026-09-13 said your programs' input and output formats were outside the rebuild; this field is the exception.

## 1. The field

- **What it carries.** The scheduling policy a program sets for itself, read from its source and from the class census of the carried work (`_dev/research/jioh/task-9.11-scheduler-constants/classes/audit.md`). Values: `normal`, and `idle` on the two entries whose programs declare it — `file-indexer` (Tracker sets SCHED_IDLE on every thread) and `incremental-backup` (Déjà Dup starts the backup under `chrt --idle 0`). A batch or real-time value is added only when an entry carries work in that class.
- **The class is the entry's.** A task carries the class of the entry it binds, never one inferred from its name: `c5-t3` shows two media players as `tracker-miner-f` and `baloo_file`, and they stay `normal`.
- **Nice is not carried.** Nice is a weight within the normal class, not a class, and of the four algorithms only LOTTERY has a weight to carry it.
- **Where it goes.** Into the workload file and so into the run file the simulator reads. Its name and place in the schema are set by the dataset rebuild (task 9.13), after your agreement.

## 2. The executor rule (인경민)

A task whose class is `idle` runs only when no task of another class is runnable, and a task of another class that becomes runnable preempts it at once. The executor applies this below whatever the configured algorithm decides — the same under MLFQ, EDF, LOTTERY and FIFO; under FIFO too, a waking `normal` task preempts a running `idle` one. The algorithm orders the other tasks as before, and orders idle tasks among themselves when only they are runnable.

The rule is our design for the scheduler under test, which through sched_ext schedules every task, idle-policy ones included, and decides what an idle task's weight means (`kernel/sched/ext.c` at v6.17, `:4663–4670`, `:5736`, `:3850–3860`). Against the stock desktop it depicts: the backup runs in the editor's CPU group and gets about 0.3 % of the CPU beside it there, as the rule nearly gives; Tracker runs in `background.slice`, whose group gets about 23 % against the editor's, so the simulated indexer interferes less than the real one.

**No starvation safety net.** The executor builds none. The algorithm-switch memo (2026-09-08) and the batch-class memo (2026-09-09) said one exists, and your status memo lists it as owed (§5.5); instead the harness's `starvation_floor` guard bounds every task's wait at 30 s, the bound sched_ext's watchdog enforces, by design. If the consumer rework's dry runs (task 9.14) show waits near 30 s, the question comes back to you.

## 3. The visible projection (박이안)

The recognizer's view (`docs/data-contracts.md` §4, "The two derived views": names, counts and pinned lifetime times) does not say whether it shows a task's declared class. That is open.

## 4. What I need from you

1. 인경민: the rule of §2 in the executor, and anything in it that conflicts with the simulator's other invariants.
2. 박이안: whether the visible projection shows the class.
3. Both: the contract change agreed — the workload and the run file carry the class of §1 — so that the rebuild can add the field with an entry in `docs/data-contracts.md` §14.
