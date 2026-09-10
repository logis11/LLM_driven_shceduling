# Phase 7 — Coreset attribute coverage

The fix from the Phase 6 pair review (`docs/daemon/prior-table-pair-review.md`, finding 2): the coverage grid tracked mode × familiarity only, so the coreset instances 17 of the 32 driver-table cells. Decided in the 2026-09-09 spec session. Parent: `_dev/TODO.md`, (jioh, 7).

## Scope

- The coverage grid gains the `background_wanted` axis and enforces coverage.
- C1 grows to one base per mode; a new group C7 holds one counterpart per mode.
- Scoring-spec entries for the new files and the term rule for label-flipping derivations.
- The prior-table pair review extended to the new pairs; feedback into the prior table.
- The generalset coverage requirement; the vocabulary's attribute clause; the demand-class declarations.
- Docs: building plan, dataset-design table, dataset README, terminology, docs index, both study guides.

Out of scope: records and scoring code; contracts, simulator, daemon; the grader's exclusion rule for pre-committed misses; the throwaway pool's definition; the judging set (all the RQ0 gate spec, Phase 8).

## Locked decisions

### 1. Coverage target

All 32 driver-table cells are instanced in the coreset, each `false` cell as a one-diff pair of a same-mode `true` base. Recounted 2026-09-09 from the compiled ground truth: 17 cells exercised; missing are the 14 `false` cells other than `gaming` and `indexing`, and `indexing/true`. `meeting/true` is instanced only by `c6-fold`, a pre-committed miss.

### 2. `false` in the batch modes

The same-job reading, the P1b precedent: in `compile`, `ml-train`, `render`, `transcode`, `indexing`, `backup` the batch job is itself the sustained background work the attribute judges, so the `false` cell is that job unwanted. The vocabulary's attribute sentence gains one clarifying clause stating this reading, with a changelog entry.

### 3. Cells with no telemetry-visible cue

Where a counterpart differs from its base only by intent (`indexing/true` for certain; any batch `false` cell for which the name search finds no credible unwanted name), the file ships as a pre-committed miss in the C6 sense: the cell is instanced, the `oracle` condition measures its row, recognition on it is excluded from accuracy and reported separately. The file carries the `initiated` annotation. Which cells ended up this way is a recorded output of the work.

### 4. Groups and ids

C1 becomes one authored single-segment base per mode, sixteen files. A new group C7 holds sixteen counterparts, one per mode, `c7-<mode>` derived from `c1-<mode>`, including `gaming` and `indexing`. The C2 instances of `gaming/false` and `indexing/false` stay as the two-segment versions. C4 stays label-invariant.

### 5. Interactive counterparts

For the ten interactive modes the counterpart injects one job: `clamscan` bound to `cpu-batch`, the same name in every file, arriving at 0 s with `total_work` equal to the 60 s segment, label flipped to `false`. One name so the ten `false` cells differ only in mode; tier 1 so no pair changes familiarity tier.

### 6. Batch counterparts

For the six batch modes the counterpart swaps the orchestrator's name for an unwanted one of the same archetype, mode unchanged, label flipped. Name rule: prefer a verified name at the base's tier; if the only credible name sits at another tier, take it, add it to the grid tool's tier table at its judged tier, and state the mismatch in the pair review; if no credible name exists, decision 3 applies. Every name passes the name-verification workflow before binding and the citation rule where a source is cited for its behaviour.

### 7. Demand class

Every C7 file and the eight existing C1-derived files (`c4-*`, `c5-*`, `c6-fold`, `c6-spoof`) declare `demand: calibration` as an authored `patch-meta` in their variant recipe. A file's regime is read from the manifest's utilization, and the pair review reports per pair whether the counterpart lands in the window. This closes the Phase 3 archive's inherited-demand-class item.

### 8. New bases

The ten new C1 files (`mail`, `dev`, `photo`, `meeting`, `video-edit`, `ml-train`, `render`, `transcode`, `indexing`, `backup`) are authored in the existing C1 shape, task sets lifted from the segment that already carries the mode elsewhere in the coreset, the source named in the file's header; batch jobs sized to the 60 s segment where the source segment was longer. `meeting` has no liftable task set and is designed as a live call with a periodic consumer. `c1-indexing` is the `true` cell, a user-initiated reindex of the same indexer.

### 9. Base terms

Terms on the new bases follow the pattern by mode class with the weight the mode's existing instance already carries: interactive-only modes score the foreground's P99 `ready_wait`; periodic modes score the consumer's `job` miss rate with a secondary where one exists; batch-beside-editor modes score the editor's P99 plus the job's term, `turnaround` where the job is sized to finish and `progress` otherwise. `indexing/true` gets a turnaround term as a stated assumption, so its prior-table cap becomes derived rather than assumed. Exact entities and numbers are fixed in the sub-task, and no existing `true`-row cap changes.

### 10. Counterpart terms

Unwanted work carries no term. A C7 entry declares `base` and repeats the base's terms minus any term whose entity is the flipped job. The scoring lint's derived-equals-base check gains that clause; the rule is stated in the scoring spec's header and explains P1b and P2b.

### 11. Grid

The grid becomes one row per driver-table cell, 32 rows with the five tier columns, per-segment counts, `ambiguous` reported outside the 32. The CI check fails when any cell has zero segments. Pre-committed-miss files count in their cells and the table marks them as recognition-limited. The grid remains the paper's dataset-design table.

### 12. Generalset requirement

Building plan §4 states that a generated set instances every driver-table cell, checked by the same grid lint run on the generated set.

### 13. Pair review

The pair review gains one sentence per new pair, sixteen, in the form Phase 6 fixed: the knob, the scored term it moves, agreement with the weights. Fixes feed back into the prior table.

## Invariants

- Records and scoring code unchanged; harness lint extended only by decision 10. Contracts, simulator, daemon unchanged.
- Every name and every judgement rests on a reference; unverified entries are marked, not invented.
- Nothing enters code or docs that is not a field or rule in the contracts, the metrics doc, or this spec.

## Open items

- The throwaway pool the calibrated table is tuned on is undefined in every document; its definition belongs to the RQ0 gate spec (Phase 8). This spec names the gap only.
- Phase 8 note: C1 is now sixteen files, which touches the judging set and the building plan's "this is where the whitelist should score perfectly" line.
- Inputs to the RQ0 gate spec from the 7.5 pair review (decided 2026-09-10): the calibration class stays on C7 with the reason stated in the building plan's demand-budget paragraph (a counterpart's demand is its base's plus the injected job by construction; the pair, not the window, is the control); `c7-meeting` and `c7-media` count toward the RQ0 headroom like any file, with two reporting lines — their `oracle`-versus-`fixed` gap is an EDF-versus-MLFQ result with the cap axis unmeasured, and a condition reading the mode right and the attribute wrong is predicted to score the same as `llm_vocab` there. The attribute-accuracy headline is balanced accuracy with the confusion matrix beside it, raw accuracy only next to its majority baseline: the coreset's `false` share is 18 of 63 segments, so raw accuracy alone stays majority-flattered, and the imbalance is answered by the metric definition rather than by adding files.
