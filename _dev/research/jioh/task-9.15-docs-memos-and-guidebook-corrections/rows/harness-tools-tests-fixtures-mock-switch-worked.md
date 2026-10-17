# Work-list rows — `harness/tools/tests/fixtures/mock-switch/worked.md`

No chunk: the harness test tree, outside the sweep; its rows are applied in a batch's harness part. 1 open row.

### W-1004 · applied
- At: `harness/tools/tests/fixtures/mock-switch/worked.md` line 5, the scheduler behaviour "assumed here" ("a switch **out of** MLFQ applies at the running task's slice boundary (the drain)")
- Change: The drain restated to the next time the lane is free (the running task's slice or current RUN ends, or it is preempted or departs), as `docs/data-contracts.md` §7's **Drain** has it. The fixture's own drain (12000, the hog's slice end, the lane's first freeing) is the same under both: no trace or expected row moves.
- Final word: `docs/data-contracts.md` §7's **Drain** and its §14 entry of 2026-10-17 (W-0949's answer (c)); `simulator/src/sim.cpp:573–577`, `:823–828`; W-0973 (metrics §11 item 8, applied in P2).
- Sources: `logs/P1.md` ## Rows for other chunks (X2)
- Cross-ref: W-0973; W-0920; W-0974
- Notes: found in P1. Harness test tree, an input of no manifest: in the next batch's harness part, with W-0973's metrics item 8 restatement already applied.
