# Work-list rows — `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md`

Chunk K17, Memos (wave 4). 2 open rows. The file has 101 lines at `d5cc7711`.

### W-0687 · applied
- At: `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` the header block after the H1 (the `> Status:` line and the `> From …` line)
- Change: Add one header line after the Status line: either closed, naming where the memo's content now lives, or open, naming the ask still outstanding and its owner. Bump the header's `Updated`.
- Final word: 9.15 spec decision 10: each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner; a memo's original text is never edited; a correction is an appended `## Correction (<date>)` section in the memo's own language, the header's `Updated` bumped; no memo is moved or deleted.
- Sources: 9.15 spec decision 10 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:54`)
- Notes: The memo: to 인경민: the task queue, preemption and overhead at an algorithm switch; item (c) of the conformance statement (a switch into MLFQ as a cold start, a same-algorithm entry letting the slice finish) is held as owed by its owner (`harness/experiments/rq0-gate.yaml:333–335`, `:341–342`). Written in English; the header line in the memo's own language. Whether it is open or closed is decided against the code and the records, and logged.

### W-0688 · applied
- At: `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` new — an appended `## Correction (<date>)` section after §7; the corrected statement is in §1, line 16 ('Thrash guard: … The executor's starvation safety net already bounds this; no extra rule.')
- Change: Append a dated `## Correction (<date>)` section in English naming the statement and stating that the executor builds no starvation safety net: the harness's `starvation_floor` guard bounds every task's wait at 30 s by design (the declared-class memo, `docs/memos/2026-10-08-declared-scheduling-class.md` §2, line 20; 9.11 D19); bump the header's `Updated`; the memo's text stays.
- Final word: 9.12 D30 as amended by D79 and D114: the executor has no starvation window; FIFO and EDF's deadline class have no horizon, so beside them an unset cap can leave a task waiting without bound, and an idle-class task waits behind other classes by design; MLFQ's boost can be lengthened to 10 s but not removed; a run in which any task waits more than 30 s fails the harness's `starvation_floor` guard, and on a run the RQ0 (research question 0, the gate experiment: does configuration matter on these workloads at all) criterion reads, that makes the verdict invalid. The batch class's bandwidth cap is one configuration field, which the executor is to enforce (not yet implemented). D30 records the memos that told 인경민 a net exists as point-in-time records answered by the declared-class memo's paragraph (9.11 D19, 2026-10-08: 'No starvation safety net. The executor builds none.').
- Sources: S12-144 (9.12 D30, `task-9.12-related-work-prose/changelog.md:499`)
- Cross-ref: W-0690
- Resolved at merge: 9.12 D30 left the memo unrewritten, pointing to the declared-class memo; 9.15 spec decision 10 (later) sets the form: an appended correction naming the statement.
- Notes: Checked: `harness/guards/guard-spec.yaml:143–146` (`starvation_floor`, threshold 30,000,000 µs); the simulator's status memo lists the cap as not implemented (`simulator/memo/memo_261010.md:25`). The memo also gets its one open/closed header line at assembly.
