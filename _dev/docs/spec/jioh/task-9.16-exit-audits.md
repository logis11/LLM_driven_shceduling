# Task 9.16 — Exit audits

The claim, measurement and compiled-number audits re-run on the final repository state, so Phase 9 meets its exit criteria (phase spec decision 8: every finding resolved, the three audits returning nothing unresolved). Decided in the 2026-10-17 grill. Parent: `_dev/TODO.md`, (jioh, 9.16); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`.

## Scope

- The claim audit, the measurement audit and the compiled-number audit on the final state.
- The items handed to 9.16 on its `_dev/TODO.md` line, read per decision 3.
- The fixes the audits' findings call for.

The runs are kept light.

## Locked decisions

### 1. Claim audit: trace, plus a sample re-read

A claim inventory is built from the final repository. Each claim is checked to trace to a slice's read record that meets phase spec decision 1, with the repository's wording within what the record's passage says. A sample is re-read blind: the claims whose wording changed after their read, plus spot checks per slice.

### 2. Measurement audit: the slices' tools, plus a class read of every value

Every `meas-ci` value is reproduced from its released raw data with the slices' committed fold-in tools in their check mode, and every value gets a class read (measured, derived by arithmetic, our own convention) against what its method measured. An independent re-implementation is written only where a class read raises a doubt.

### 3. The handed-over items: final state only

The items on the TODO line that name an intermediate pin (9.17's, 9.18's, 9.22's, 9.19's, 9.20's, 9.21's) are closed by one run of the dataset gate at home and one CI run on the final build. The items on content that is still current run as listed. 9.15's two new computations stay in 9.16: the burstiness and window readings re-run on `renderer-hidden`'s and `video-editor`'s pools, and the stability ledger.

### 4. Findings fixed inside 9.16

Findings are fixed in 9.16, in 9.15's order: code and data first, with at most one rebuild, then the docs and memos. A finding whose fix is a judgement comes to 인지오 as one question in chat, and the answer is recorded.

### 5. Compiled-number audit: the exit criteria's list, as current

The compiled-number audit covers the prior driver table, its pair review, the scoring spec, the guard spec, the RQ0 gate spec, the memos whose open/closed line says open, and the final memo. Closed memos, and the docs and guidebooks 9.15 swept, are not re-audited.

### 6. Statements waiting on the simulator

A compiled-number statement whose truth depends on an executor rule the reference simulator does not implement yet is resolved when the document names the RQ0 gate spec's conformance item it waits on. The exit record lists every such statement by conformance item, as the check for 인경민 to run once each item lands.
