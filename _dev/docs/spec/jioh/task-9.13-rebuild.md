# Task 9.13 — Rebuild

The one build of the workload dataset after the research slices 9.4–9.12: the structural changes the slices could not make as their decisions landed, then a single blessed single-lane set for 9.14 to re-pin. Decided in the 2026-10-09 grill. Parent: `_dev/TODO.md`, (jioh, 9.13); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`; decision record `_dev/research/jioh/task-9.13-rebuild/changelog.md`.

## Scope

- The declared-class field, on the library, in the workload and in its two views.
- The idle variant of the download entry and the file that binds it.
- The native compiled set dropped.
- The lints and tests the decisions imply.
- The data-contracts entries the field changes and the dataset README's structural lines.
- One blessed build.
- The reads handed in by 9.5, 9.7 and 9.11, recorded with no value changed.

Out of scope: any archetype value — the slices' values stand as applied. Prose under `docs/` other than the data-contracts pieces named here — 9.15's. The demand-window rule, the judging set, the pins — 9.14's.

## Locked decisions

### 1. No agreement gate

인경민 and 박이안 have agreed the contract change of the 2026-10-08 declared-scheduling-class memo. Throughout 9.13, 인지오 decides; the teammates are told in the phase's final memo.

### 2. The field: `declared_class`

Every task record — the top-level arrive event and every spawn-table entry — carries `declared_class`, required, from the closed set `normal` and `idle`; a batch or real-time value is added only when an entry carries work in that class. Every library entry carries it, required, with no default. It is `idle` on `file-indexer` and `incremental-backup` and `normal` on every other entry. A task's class is its bound entry's, never one read from its name; a spawned task's is its child entry's.

### 3. The visible projection carries the class

The daemon's view of the workload includes each task's `declared_class`, on the standing that a real machine exposes a process's class as it exposes its name.

### 4. The idle download variant

A library entry `game-download-idle` shares `game-download`'s tables, lifetime, scaling rule and validation record by reference, its own content only the class `idle` and a short modelling note. A file `c2-p2a-idle`, derived from `c2-p2a` by the one change of the `download` task's entry, inherits the seed and keeps the ground truth and segment attributes. The two compiled files differ in that task's class and nowhere else. Both are in the manifest; the file is outside the judging set and read by 9.14's bounding check alone.

### 5. The native set dropped

The native compile mode leaves the compiler, the lints and the manifest; the lane-scaling pass is the only pass. The single-lane set keeps the name `coreset-single`.

### 6. Docs 9.13 touches

In `docs/data-contracts.md`: the §14 changelog entry, §2's archetype, §4's workload and its two views. In `dataset/README.md`: the layout, the pipeline, the modes, the canonical-format example and the lint list. Everything else under `docs/` is 9.15's.

### 7. Records

This spec carries the decisions. A research folder `_dev/research/jioh/task-9.13-rebuild/` holds a changelog in the slices' form and the reads. Hand-offs go onto the 9.14, 9.15 and 9.16 TODO lines.

### 8. Lints and tests

Four, and no more. TIMER-first: in the canonical lint, over top-level and spawned programs, a program that contains a TIMER anywhere has a TIMER as its first executed instruction, a LOOP head's body counting as its head. The class on every library entry, from the closed set, in the repository lint. The class on every task record, by the schema, with a test that every compiled task's class equals its bound entry's. The bounding pair's byte-identity, as decision 4 states it.

### 9. The library's version

The library's stated version moves from v0.1 to v0.2 in the data-contracts §2 and the dataset README; the §14 entry names it.

### 10. The bless and the demand window

The bless runs the dataset target with the compiler's existing allowance that reports demand-window violations as warnings and still writes. The nine violating files and their demands are recorded in the changelog as the state 9.14 inherits; the CI gate stays strict, red on the window until 9.14 redoes the rule.

### 11. Placements

The compiler copies the class from the bound entry onto each arrive event, and from the child entry onto each spawn entry, beside the task's name. The §14 entry is dated, names the field, its values, the two idle entries, the variant entry, the dropped mode and v0.2, and records that 인지오 decided it with the teammates to be told in the final memo; the 2026-10-08 memo gets one dated line naming the field and pointing to §14; nothing else is sent now. The two modelling notes are restated per 9.11 D16. The 9.13 TODO line's wake-event count and size are replaced at bless time by the measured ones, and the size is handed to 9.14 and to the final memo. The DKMS read is recorded with no value changed. The manifest and the regenerated coverage grid are committed; `build/` is not. All of 9.13 is committed on `jioh/dataset-rebuild`, no sub-worktree.

### 12. Reads recorded, no value changed

- `network-bulk` is gone from the library and every timeline (9.7 D30's condition met).
- All 22 TIMER-carrying tasks of the current set satisfy the TIMER-first rule — 7 through a LOOP head, 15 literally.
- `module-build-orchestrator`'s tables hold no `apt-check` or `dpkg` work: the pooling keeps only the DKMS hook's own process subtree (9.10 D50); 9.11 D20's 0.85 % was read over the whole stage's taskstats, which the tables do not carry.
- The current single-lane set: 50 files, 4,496,190 exogenous wake events, 666 MB; `c6-dual` 190 MB. The 9.13 line's 531,740 and 84 MB are 2026-09-26's figures.
- Compilation of the single-lane set takes about 129 s; the full lint with schema validation runs past 28 minutes.
- Nine of the ten oversubscribed-class files are outside the demand window; the 40 calibration-class files are exempt.
- No I/O class field: the simulator schedules one CPU lane (9.11 D33).
