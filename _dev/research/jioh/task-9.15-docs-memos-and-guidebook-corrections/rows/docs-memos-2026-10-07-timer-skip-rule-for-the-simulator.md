# Work-list rows — `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md`

Chunk K17, Memos (wave 4). 1 open rows. The file has 66 lines at `d5cc7711`.

### W-0706 · open
- At: `docs/memos/2026-10-07-timer-skip-rule-for-the-simulator.md` the header block after the H1 (the `> Status:` line and the `> From …` line)
- Change: Add one header line after the Status line: either closed, naming where the memo's content now lives, or open, naming the ask still outstanding and its owner. Bump the header's `Updated`.
- Final word: 9.15 spec decision 10: each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner; a memo's original text is never edited; a correction is an appended `## Correction (<date>)` section in the memo's own language, the header's `Updated` bumped; no memo is moved or deleted.
- Sources: 9.15 spec decision 10 (`jioh/task-9.15-docs-memos-and-guidebook-corrections.md:54`)
- Notes: The memo: to 인경민: the TIMER skip rule; the simulator still runs the backlog rule (`simulator/src/sim.cpp`), item (b) of the conformance statement owed; the docs keep the backlog rule until it lands (spec decision 9; the Phase 10 TIMER line in `_dev/TODO.md`). Written in English; the header line in the memo's own language. Whether it is open or closed is decided against the code and the records, and logged.
