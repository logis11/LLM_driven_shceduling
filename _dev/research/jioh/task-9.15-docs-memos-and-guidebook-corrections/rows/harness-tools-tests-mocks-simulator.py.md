# Work-list rows — `harness/tools/tests/mocks/simulator.py`

No chunk: the harness test tree, outside the sweep; its rows are applied in a batch's harness part. 1 open row.

### W-0984 · applied
- At: `harness/tools/tests/mocks/simulator.py` the WAIT-first skip, lines 186–187 (`wait_first`, `:148–160`); the module docstring, lines 5–14
- Change: The mock completes a WAIT-first task's WAIT at its arrival when a wake is already stored for it (a pending external wake on its channel or a delivered WAKE in its mailbox), writing `ready(arrive)` as the reference simulator does, and skips the arrival stimulus only when none is; the docstring states the condition. Harness code: `make -C harness test` and lint passing, a `harness/CHANGELOG.md` entry. No core-set trace differs (no core-set wake falls at or before its target's arrival).
- Final word: 인지오's answer (c) of 2026-10-17 to K10 (X4): the mocks follow the reference simulator; `simulator/src/sim.cpp:688–691` (the WAIT completes on `chan_pending_` or a mailbox WAKE), `:737` (`on_arrive` enqueues with `ready(arrive)`).
- Sources: `logs/N3.md` ## Code-versus-decision mismatches (1), ## Rows for other chunks, ## Review round 2; `logs/B2-harness.md` (review finding 3)
- Cross-ref: W-0889; W-0982; W-0983; W-0981
- Notes: found in N3: its mismatch 1 and the docstring part of its harness-test row, one row. Harness test tree, an input of no manifest: in the next batch's harness part.
