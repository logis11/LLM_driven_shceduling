# Phase 9 — Workload dataset rebuild from the critical findings

Resolve what the workload dataset and everything built on it rest on, rebuild the dataset, and return the project to the state Phase 8 ended in: the RQ0 gate spec committed and ready for the RQ0 run. Decided in the 2026-09-13 spec session. Parent: `_dev/TODO.md`, (jioh, 9).

## Scope

- The 13 findings in `docs/memos/2026-09-13-critical-findings.md`.
- The six findings from the 2026-09-13 check that the memo lacks: interbench's Compile load forks no processes; the "~5.7 ms" download sleep matches no version of `dataset/archetypes.yaml`; Roeser's Table 3 reports the spreads the archetype calls convention; LAVD slides 12 and 16 on wineserver; CpsMark+ contradicts "time-shared compositions"; the `chang-chi21` details.
- Every claim the dataset takes from a source (the 2026-09-13 claim inventory), including the twelve registry entries not read against their primary text before: `pcmark10`, `sysmark30`, `sysmark25`, `procyon`, `gamemode-docs`, `steam-downloads`, `dkms-man`, `dkms-debian`, `zhang-chb15`, `gonzalez-chi04`, `mark-chi05`, `focal-arxiv26`.
- Every `meas-ci` value, against the raw release and the method that produced it.
- Everything the 2026-09-13 verification found: the independent reads and comparisons of the source claims, the measurement audit, and the audit of compiled-number statements in settled decisions.
- Four groups of artifacts:
  - the dataset — archetypes, timelines, the measurement campaign and its tools, the dataset docs;
  - what consumes the dataset — the prior driver table and its pair review, the scoring spec, the guard spec including `tick_count`, the RQ0 gate spec, the demand-window rule;
  - citations outside the dataset — related-work and research-proposal prose, harness and metrics constants, the boot default's provenance, the boot-default sweep's backbone citations, the guard thresholds' groundings, and corrections to the guidebook volumes already written;
  - team memos.

Out of scope: writing new guidebook volumes.

## Locked decisions

### 1. Verification standard

A claim taken from a source is verified when it is recorded with the verbatim passage, its locator, and the copy read (URL or commit, version, date), and the check covers the whole claim the repository makes — its object, unit, statistic, scope and population. The source is read independently, without the repository's description of the claim, before the reading is compared with the repository's wording. A claim whose passage is not found is unverified. A value no source states carries no source tag and is labelled for what it is: convention, arithmetic, placeholder, or design.

### 2. No montage within an archetype

All numbers of one archetype come from one observation: one study population, one trace, or one measurement run. Several documents about the same observation count as one source; one document mixing different traces does not. Our own measurement run counts as one observation. Research looks for one observation that covers the whole archetype first; where none exists, the archetype comes to 인지오 as a decision.

### 3. The rule applied to timelines

Timeline content presented as how real desktops behave — task sets, co-occurrence, order, counts, typical durations, process names — follows decision 2, one observation per situation. The experiment's own interventions and calibration sizes — label flips, injections, renames, file length, `lane_share` — are labelled as design and carry no source tag.

### 4. Research fills gaps

Where the current sources do not ground a value or a structure, the phase researches new grounding rather than leaving the gap empty. A slice declares that no single observation exists only after a search log covering four classes — peer-reviewed and preprint literature; primary project and vendor documentation and source code; public traces and datasets; whether our own measurement can observe it — with the terms, venues and results recorded, and then brings 인지오 the nearest candidates with what each covers and does not.

### 5. Measurement venue

Our own measurement runs on CI runners only. What a runner cannot observe comes from literature or public traces, or to 인지오 as a decision. This is a stated limitation.

### 6. Structure of the phase

First, the 2026-09-13 verification records are persisted into the repository, and the measurement tools are fixed, including preserving the `meas-ci:names:2` run before its Actions artifacts expire on 2026-12-09. Then research-and-decision slices by domain, runnable in parallel: gaming; interactive and typing; compile; background and IO; browser and comms; daemons and session processes; scenarios and timelines; scheduler-side constants and groundings; related-work and proposal prose. Then one rebuild of the dataset. Then one consumer rework — scoring spec, guard spec, prior table and pair review, RQ0 gate spec — with one harness changelog entry and one re-pin. Last, one sweep of docs, memos and guidebook corrections.

### 7. Team communication

A heads-up memo to 인경민 and 박이안 at the start of the phase: what will change, what stays stable, and three executor questions to 인경민 — how LOTTERY splits the batch share when an editor's own burst tail is batch-class; whether chain stages are deadline or residual class under EDF, where the recognition vocabulary and the batch-class memo disagree; what happens to a keystroke that arrives while the editor is still running. A final memo at the end of the phase with the actual changes.

### 8. Exit criteria

Every finding is resolved. The claim audit, the measurement audit and the compiled-number audit are re-run on the final repository state and return nothing unresolved: every claim meets decision 1, every archetype and every realism claim in a timeline meets decisions 2 and 3 or carries 인지오's recorded decision, every measured value reproduces from the released raw data and describes what its method measured, and no statement in the prior table, pair review, scoring spec, guard spec, RQ0 gate spec or memos is wrong or stale against the rebuilt data. The final memo is sent. The project stands where Phase 8 ended: the RQ0 gate spec committed and ready for the RQ0 run.

## Open items

Left to each sub-task's own spec session:

- The format and location of the verification records, and whether source copies are kept.
- How the measurement tools are fixed.
- Each archetype's and each timeline's values and structure.
- Any re-decision of the RQ0 judging set, the boot-default sweep points, or K.
