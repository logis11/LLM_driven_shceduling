# Work-list rows — `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`

Chunk K17, Memos (wave 4). 2 open rows. The file has 86 lines at `d5cc7711`.

### W-0689 · applied
- At: `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` the header block after the H1 (the `> Status:` line and the `> From …` line)
- Change: Add one header line after the Status line: either closed, naming where the memo's content now lives, or open, naming the ask still outstanding and its owner. Bump the header's `Updated`.
- Final word: 9.15 spec decision 10: each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner; a memo's original text is never edited; a correction is an appended `## Correction (<date>)` section in the memo's own language, the header's `Updated` bumped; no memo is moved or deleted.
- Sources: 9.15 spec decision 10 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:54`)
- Notes: The memo: to 인경민: the batch class `batch_bandwidth_cap` applies to; item (d) of the conformance statement is owed (`harness/experiments/rq0-gate.yaml:335–337`). Written in English; the header line in the memo's own language. Whether it is open or closed is decided against the code and the records, and logged.

### W-0690 · applied
- At: `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` new — an appended `## Correction (<date>)` section after §7; the corrected statements are in §3, line 45 ('The starvation safety net is separate and unchanged: every runnable task, batch or not, makes progress within a bounded window regardless of the cap.') and §7, line 82 ('Keep the starvation safety net independent of the cap.')
- Change: Append a dated `## Correction (<date>)` section in English naming both statements and stating that the executor builds no starvation safety net: the harness's `starvation_floor` guard bounds every task's wait at 30 s by design (`docs/memos/2026-10-08-declared-scheduling-class.md` §2, line 20; 9.11 D19); the batch class's cap is still to be enforced by the executor (not yet implemented); bump the header's `Updated`; the memo's text stays.
- Final word: 9.12 D30 as amended by D79 and D114 (as W-0688): no executor starvation window; FIFO and EDF's deadline class have no horizon, so an unset cap can leave a task waiting without bound beside them; an idle-class task waits behind other classes by design; MLFQ's boost can be lengthened to 10 s but not removed; a wait over 30 s fails the `starvation_floor` guard and invalidates the RQ0 (the gate experiment) verdict on a run its criterion reads. The batch class's bandwidth cap is one configuration field — the driver table row's under every condition but `llm_full`, unset or 0.05–0.95 there — which the executor is to enforce (not yet implemented). D30 records these memos as point-in-time records answered by the declared-class memo's paragraph (9.11 D19).
- Sources: S12-145 (9.12 D30, `task-9.12-related-work-prose/changelog.md:499`)
- Cross-ref: W-0688
- Resolved at merge: As W-0688: 9.15 spec decision 10 sets the form.
- Notes: Checked as W-0688 (`harness/guards/guard-spec.yaml:143–146`; `simulator/memo/memo_261010.md:25`: 'Cap enforced on the batch class while a non-batch task is runnable — not implemented'). The memo also gets its one open/closed header line at assembly.
