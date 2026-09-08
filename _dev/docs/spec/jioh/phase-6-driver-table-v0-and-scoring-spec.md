# Phase 6 — Driver table v0 and the scoring spec

Stage 3 of `_dev/docs/rq0-preparation-notes.md`, plus the harness side of `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md`, as decided in the 2026-09-08 spec session. Parent: `_dev/TODO.md`, (jioh, 6). Work lands on `jioh/driver-table-v0`.

## Scope

- The prior driver table: every row authored from theory with its justification.
- The scoring spec: per-file terms and weights over records, as a machine-checked data file.
- The switch-overhead primitive, aggregates, fixture and check tool from the 2026-09-08 memo's harness-side action plan.
- The pair review of the prior table.

Out of scope: file classification for the gate (judging, reporting-only, separate, excluded), the `random` draw definition, the threshold — all Phase 7's gate spec. The calibrated table.

## Locked decisions

### 1. Row scope

All 32 rows are authored, each with `basis: theory` and a one-sentence justification on the row and on the entry. No row is filled with schema defaults. The coreset exercises 17 legal rows (16 in C1–C4); the other 15 are authored the same way because the `random` condition may land on any row.

### 2. Algorithm policy

Any of the four algorithms may be named per row, chosen by theory. How many algorithms the table uses is a result, not a target. Justifications are plain sentences; a `docs/references.md` id appears only where one already exists, and no new sources are added for the table.

### 3. Pair review scope

Two lists. The 16 same-mode `wanted=true/false` pairs, and the three C2 row-pairs as the files actually exercise them: `ml-train/true` vs `indexing/false` (p1), `gaming/true` vs `gaming/false` (p2), `render/true` vs `backup/true` (p3). Only p2 is a same-mode pair; the other two are cross-mode distances the lint does not see.

### 4. "Far enough apart"

A written judgement per pair, no numeric threshold: one sentence naming which knob differs (algorithm, cap, or a parameter), which scored term of the exercising file that knob moves, and that the direction agrees with the scoring weights. A pair whose sentence cannot be written is a table defect, fixed before the phase closes. Recorded in the phase archive.

### 5. Score form

One term type. A term names an entity, a primitive, a filter (`cause`, time window), an aggregate, a direction, and a weight. A file's score is the weighted sum of its terms' normalised shares. No constraint form; anything constraint-shaped is a guard and belongs to the gate spec.

### 6. Scored aggregate per term kind

`ready_wait` terms score P99. `job` terms score miss rate. Batch terms score progress (`cpu_delivered / demand`). `c1-compile`'s build scores `turnaround` (the makespan). Every other aggregate is reported beside the score, unweighted.

### 7. C2 weights

Foreground term 1.0 throughout. Wanted batch progress 0.5 (`c2-p1a` hog, `c2-p2a` download, `c2-p3a` ffmpeg). Unwanted batch unweighted (`c2-p1b`, `c2-p2b`). Scheduled wanted backup 0.25 (`c2-p3b` borg). p2's frame term is the chain (`game.chain.1`); the pair has no compositor.

### 8. C2 window rule

Every `ready_wait` and `job` term in the six C2 files is aggregated over 60 s to `T_end`. The switch at 60 s and its transient are inside the window and count against the condition. Progress terms are unwindowed.

### 9. `c1-compile`

Editor P99 1.0, build makespan 1.0.

### 10. `c1-media`

`music` miss rate 1.0, `video` miss rate 0.5, marked a stated assumption. No legal configuration can produce a missed tick in this file, so it is expected to report "no headroom"; this is written in the spec beside the weights. No perceptual-literature source is searched for in this phase.

### 11. `c1-gaming`

Chain miss rate 1.0, compositor (`gamescope`) miss rate 0.5. `c4-gaming` inherits unchanged.

### 12. Remaining C1

`c1-office` scores `writer` P99 alone; `c1-browsing` scores `browser` P99 alone; `c1-idle` has no terms.

### 13. C3 term rule

Per-task terms, no explicit windows (focus and task lifetimes window them). Each segment's foreground term 1.0; batch and media terms by decisions 7 and 10. `c3-workday`: `browser`, `writer`, `mailer` P99, `build` progress 0.5. `c3-evening`: `browser` P99, `game.chain.1` miss rate, `music` 1.0 / `video` 0.5. `c3-creation`: `photo-editor`, `video-editor` P99, `batch` progress 0.5, expected "no headroom" since it runs uncontended after 240 s.

### 14. Exclusions

The scoring spec carries terms only, no file classification. Derived files carry their base's terms verbatim: C4 from its C1 base, C5 from `c1-media`, `c6-spoof` and `c6-fold` from `c1-browsing`. `c6-dual` carries chain miss rate 1.0 and editor P99 1.0. `c1-idle` has no entry. Which files judge, report, are read as deltas, or are excluded from aggregation is the gate spec's list alone; the intended classification is recorded in the phase archive for Phase 7.

### 15. Scoring spec placement and lint

YAML in the harness tree, one file, with a JSON schema and a lint beside it, run in the `harness` CI workflow. The lint checks: every term's entity is a task id in that file's compiled workload or a reserved name; metric and aggregate form a legal combination; direction is fixed by the aggregate; weights positive; windows inside `[0, T_end]`; derived files equal their base's terms byte for byte. It reads the compiled workloads under `dataset/build/`.

### 16. Switch overhead

All five harness-side items of the memo land in this phase: the `switch_window` primitive in the metrics doc and in code; a `hogs` attribute column in the records schema; the two aggregates (per-switch excess wake `ready_wait`, switch and boost variants; share of the window inside switch windows); a FIFO → MLFQ mock fixture with hand-computed values; the `x_mlfq_level` check tool as a separate script beside the harness. The boost timer is assumed to restart at `t_apply`, written as a stated assumption to be confirmed or flipped when 인경민 decides, with a changelog entry either way. Switch overhead is never weighted in a score; it is reported beside every file's score. The primitive sits on entity `schedule` and its aggregate decomposes the already-scored `ready_wait` rows, so it changes no scored term.

### 17. Order

Switch overhead first, then the scoring spec, then the prior table, then the pair review. A row's justification names the scored term it serves, and a row that cannot be justified is a scoring gap.

## Invariants

- Nothing enters the table or the scoring spec that is not a field or rule in the frozen contracts or the metrics doc; entity names are read from the compiled coreset, never guessed.
- Condition names are `fixed`, `random`, `whitelist`, `llm_vocab`, `llm_algo`, `llm_full`, `oracle`.

## Open items

- Boost-timer behaviour at `t_apply` and the FIFO-outgoing apply rule: 인경민's, per the memo.
- Whether `c1-media` gets a tier-1 familiarity annotation (carried from Phase 5).
