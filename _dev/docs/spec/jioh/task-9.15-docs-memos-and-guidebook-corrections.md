# Task 9.15 — Docs, memos and guidebook corrections

The one sweep that brings the public docs, the memos and the guidebook volumes already written in line with the rebuilt workload dataset and the decisions of Phase 9, ending in the final memo to 인경민 and 박이안. Decided in the 2026-10-14 grill. Parent: `_dev/TODO.md`, (jioh, 9.15); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`.

## Scope

- Every item handed to 9.15: the 9.15 line in `_dev/TODO.md`, every "Hands to 9.15" line in the slices' changelogs under `_dev/research/jioh/` (9.12's and 9.10's in full), and the 2026-10-10 dataset audit's items.
- `docs/` (the guidebook included), `dataset/README.md`, the memos.
- A root `LICENSE` and `dataset/LICENSE`.
- The final memo to 인경민 and 박이안.

Out of scope: the existing files under `_dev/`; the simulator-side TIMER rows (decision 9); new guidebook volumes.

## Locked decisions

### 1. A combined work list comes first

Before any edit, one work list is built in a 9.15 research folder. Three agents read the sources — 9.12's changelog, 9.10's changelog, and everything else including the TODO line — and each row carries the decision's final word after its amendment chain and the text's current location. A merge agent removes duplicates, groups the rows by target file and proposes the chunk grouping from the counts. 인지오 reviews the list and the grouping before any edit.

### 2. Agents decide and log; code first

An editing agent resolves the items it meets — ambiguous, conflicting, stale against the doc — and logs each resolution. Code is first, not docs: the hand-offs and the docs may be stale.

### 3. Precedence when sources disagree

Highest first: the code and data as they stand (`dataset/`, `harness/`, `simulator/`, the committed manifests) for anything the code expresses; the latest decision record on the matter for what code does not express, a later decision superseding an earlier; the hand-off text, which says where to look and not what to write; the current docs, never an authority. Where code contradicts its own latest decision, the doc describes the code and the mismatch is logged as a finding for 인지오. A new `docs/references.md` entry needs a verified passage on file; without one the entry is marked unverified, not invented.

### 4. Scope of each doc

The docs that explain the dataset — `docs/workload/`, `dataset/README.md`, `docs/data-contracts.md`, the harness guide's records and dataset chapters — get a full pass against the code. Every other doc gets its listed rows. Staleness an agent notices outside its rows becomes a new row.

### 5. Chunks by target doc

A chunk owns a set of files and applies every row touching them, whichever slice the row came from; no two chunks share a file. The `docs/references.md` chunk runs alone first; the rest run in waves of up to four, in the same tree on `jioh/dataset-rebuild`.

### 6. Review and commit

A fresh reviewer agent checks each chunk: every row applied, nothing outside its rows touched, every edit matching the code under decision 3, the header's `Updated` bumped, `docs/README.md`'s index updated where a doc's status or name changed. Findings go back to the editing agent. On a pass the main session commits the chunk's files by path, one commit per chunk; editing and reviewing agents do not commit. The branch is pushed after each wave's commits.

### 7. Records

Each chunk writes only its own log in the 9.15 research folder: each row's outcome, the decisions with their reasons, the code-versus-decision mismatches, and the rows found for other chunks. The work list is read-only during a wave; the main session folds statuses and cross-chunk rows into it between waves. The chunk logs are 9.15's record; there is no numbered changelog.

### 8. 인지오's review is non-blocking

A chunk is committed on its reviewer's pass. 인지오 reads the chunk logs afterwards; a decision he overturns becomes a new row, applied by a follow-up chunk.

### 9. TIMER rows split by component

The simulator runs the backlog rule (`simulator/src/sim.cpp`); the harness reads the skip rule (`docs/harness/metrics.md` §6.2, `harness/tools/harness/primitives.py`). Rows on the harness's reading are applied in 9.15. Rows on the simulator's behaviour or the TIMER op's meaning are blocked — the docs keep the backlog rule — and carried to the Phase 10 TIMER line in `_dev/TODO.md`. The final memo names the simulator's skip rule and the zero-wait `ready` line as owed.

### 10. Memos

A memo's original text is never edited. A correction is appended as a `## Correction (<date>)` section naming each corrected statement and stating the current fact, in the memo's own language, with the header's `Updated` bumped. Each memo carries one header line — closed, with where its content now lives, or open, with the ask and its owner — and `docs/README.md`'s memo list is split into open and closed. No memo is moved or deleted.

### 11. `_dev/` is dev history

The existing files under `_dev/` are not touched. 9.15 adds only its research folder (the work list and the chunk logs) and its `_dev/TODO.md` updates. The row naming `_dev/docs/rq0-preparation-notes.md` is dropped.

### 12. Licences

A root `LICENSE` puts the code under MIT; `dataset/LICENSE` puts the dataset's data and its release assets under CC-BY-NC-SA-4.0. Both name Jioh In, Kyungmin Inn and Ian Park as the copyright holders; `dataset/LICENSE` credits SWELL-KW (Koldijk et al., 2014, DANS) for the stimulus streams.

### 13. The final memo

The final memo comes last, after the doc chunks. A subagent drafts it from the work list's memo rows, checked against the code; 인지오 and the main session go through it before it is committed. Beyond the TODO line's items it carries the memos still open, the simulator's skip rule and zero-wait `ready` line as owed, and the licences chosen.

### 14. Done

9.15 is done when every work-list row is closed — applied, decided and logged, not applicable against the code, or carried; every chunk has passed its reviewer and is committed; 인지오 has read every chunk log and every overturned decision is applied; every logged code-versus-decision mismatch has 인지오's answer, any code work it needs on its own `_dev/TODO.md` line; every memo carries its open or closed line; and the final memo is committed. 9.16's exit audits run on that state.

## Open items

- The final memo's language — decided at the memo step.
