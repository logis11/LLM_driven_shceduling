# Phase 8 — Harness upper half through pre-registration

Stages 4–5 of `_dev/docs/rq0-preparation-notes.md`: the harness from `records` to a verdict, run end to end on mocks, ending at the committed RQ0 gate spec. Decided in the 2026-09-11 spec session. Parent: `_dev/TODO.md`, (jioh, 8).

## Scope

- Scorer, guards, L1 grader, runner with execution cache, report.
- The RQ0 gate evaluator and the per-experiment spec it reads.
- Mock daemon and mock simulator; the invocation contract they are the first implementations of.
- Pre-registration: the RQ0 gate spec committed with its threshold, seed count, failure procedure, reporting lines, exemptions, and pins; the scoring spec and the guard spec frozen.
- The driver table tuning set's rule, written into the building plan; the term "throwaway pool" retired.
- Docs: the metrics doc, the data-contracts doc, the harness study guide, terminology, docs index, the RQ0 preparation notes.

Out of scope: the real simulator and daemon, the whitelist and LLM conditions, the configuration search tool, the generalset and the driver table tuning set's files, the K, g, and N values (each sub-task's own grill).

The harness modules are research-wide instruments; RQ0 is one experiment run on them. Every decision below is placed by that reading.

## Locked decisions

### 1. The RQ0 gate evaluator is built in Phase 8

The code that reads the RQ0 gate spec and the `scores` file and outputs the verdict is built and tested on mocks in this phase, so the committed gate spec is executable data. The module is named in full, "RQ0 gate evaluator", never "gate".

### 2. Per-file gap

For a judging file, the gap is the fraction of the oracle's headroom that `random` fails to capture: one minus the file's `random` score divided by its `oracle` score, where a file's score is the scoring spec's weighted sum of its terms' normalised shares and the oracle's score is therefore the file's weight sum. Unit-free, so one g applies to all 27 files.

### 3. Statistic over seeds

The file's one gap uses the mean of the `random` scores over its seeds. Every per-seed value is kept in `scores` and shown in the report beside the mean.

### 4. No headroom

A term marked no headroom (the oracle's improvement over the boot default below the aggregate's floor) keeps its weight in the file's score and is scored as if `random` had captured all of it. This is a research-wide scoring rule and goes into the metrics doc's normalisation section with a changelog entry. A judging file whose every term is no headroom stays in the 27 and counts as not meeting g; this is RQ0's rule and goes into the RQ0 gate spec. Both are marked in the report. A no-headroom judging file is a trigger for the table check in the failure procedure (decision 17).

### 5. K is an absolute count

The per-file criterion reads "at least K of the 27 judging files show a gap of at least g", with K a whole number of files, never a fraction of the set.

### 6. Failed guards block the verdict

When any non-exempt guard fails on a run that feeds a judging file, the RQ0 gate evaluator emits `invalid` in place of pass or fail, naming the guard and the run. Exemptions are data in the RQ0 gate spec. The guard list carried into the phase: provenance share, config age, starvation floor, determinism, utilisation sanity, tick count, `validation` equals `provenance`, and the C2 pair check (under `oracle` the two files of a C2 pair produce different traces, under `fixed` identical ones).

### 7. Guard spec

The guards are research-wide, so their list and thresholds live in a guard spec data file beside the scoring spec, with grounding per threshold, a schema, and a lint, frozen in this phase. The RQ0 gate spec carries only exemptions and pins the guard spec's version.

### 8. Per-experiment spec

The RQ0 gate spec is the first instance of a per-experiment spec with one shared schema: a generic part every experiment needs (conditions, judging and reporting files, seed count, guard exemptions, reporting lines, pins of the scoring spec, guard spec, driver table and dataset versions) and an experiment-specific criterion section. The evaluator's generic part (load, verify pins, apply guards, per-file scores per condition) is shared; RQ0's criterion is the K-of-27 gap rule.

### 9. Invocation contract

The runner fixes a command shape for the daemon and the simulator: input paths and condition in, output paths out, an exit code, no other channel. The mock daemon and mock simulator are its first implementations; 인경민 and 박이안 meet it when they deliver. Written into the data-contracts doc with a changelog entry and told to both.

### 10. Mock simulator

Both a trivial generator and a replay. The generator emits a contract-valid trace for any coreset file and schedule from a trivial rule with no scheduling modelled, so all 50 files flow through the whole pipeline; the replay returns the hand-written fixtures so values are checkable. The generator stays trivial: it never models a queue. Both live under `harness/`, never under the simulator tree, and are discarded in Phase 9.

### 11. Mock daemon

Faithful for `fixed`, `oracle`, and `random`: it walks the visible projection's pinned events for query points, reads ground truth or draws, maps through the prior table, and emits contract-valid schedules and recognition logs for any coreset file. It emits `unmodified` only, has no validator, clamping, `held`, or LLM path, lives in the harness test tree, and is discarded in Phase 9. One hand-written schedule fixture covers `held` and `clamped` for the guards.

### 12. Sensitivity as a reporting line

The verdict is computed once, on the primary boot default. The two alternative-default `fixed` runs the vocabulary names (OSTEP's example configuration, a Linux-like short slice) are two more runs per judging file; the gaps are recomputed under each and the three verdict counts are a pre-registered reporting line in the RQ0 gate spec.

### 13. L1 grader exclusion

The grader reads the `pre_committed_miss` annotation from the ground truth and skips those segments in every experiment. The per-experiment spec's exclusion list is derived from the same annotation and linted to match, never authoritative. Accuracy with and without the exclusion is a second report line; the headline is the excluded one.

### 14. Report

One machine-readable report per experiment run is the source of truth: every reported number with the fields that locate it (workload, condition, seed, entity, metric, aggregate) and the guard results and provenance breakdown beside it. A human-readable rendering is generated from it and never edited by hand. Paper tables come from the machine file.

### 15. `random`

The daemon guide's definition is adopted as the draw definition: at every telemetry set change, one uniform draw over the 32 driver-table rows, independent of previous draws and of the telemetry, from a seeded PRNG, logged with its draw and seed, at zero latency. The item with 박이안 is confirming this reading and the seed count.

### 16. Seed count

N is a number committed in the RQ0 gate spec before execution, grounded by an argument written beside it in the pre-registration sub-task's grill, decided after K and g. Not a rule applied in Phase 9, not an enumeration of the draw space.

### 17. Failure procedure

The procedure is written into the RQ0 gate spec as ordered steps with their decision rule: on a fail, a configuration search on two or three failing files before any workload change; no spread found means workload redesign, spread that v0 missed means the table is rewritten; a no-headroom judging file is an additional trigger for the table check. The search tool is built in Phase 9 only if the gate fails.

### 18. Driver table tuning set

The proposal's "disjoint throwaway pool" is renamed the driver table tuning set. Phase 8 commits its rule, not a file list, into the building plan's §4 as the dataset's normative home; the lines that say the definition belongs to the RQ0 gate spec are corrected to point there. The term is renamed in every document outside the append-only archives and added to the terminology doc. The rule's exact wording, and how disjointness is guaranteed, is the sub-task's.

### 19. Freeze

인지오 freezes the scoring spec and the guard spec alone, recorded in the harness tree's own changelog. The RQ0 gate spec pins the frozen commit. Team ratification is handled afterwards in a team meeting.

### 20. Closing with a pending confirmation

The RQ0 gate spec commits N, its grounding, and the `random` reading marked as proposed to 박이안 on a date and pending confirmation; the memo carries the proposal and the invocation contract. The phase closes without waiting. Confirmation is a Phase 9 prerequisite, recorded in the RQ0 gate spec when it arrives; a changed N is a changelog entry made before any run.

### 21. Reporting lines carried from Phase 7

The RQ0 gate spec carries as fields: the `c7-gaming`, `c7-meeting`, `c7-media` judging notes, `c1-gaming`'s separate line, balanced accuracy with the confusion matrix as the Layer-1 headline, the sensitivity line (decision 12), and the with-and-without-exclusion accuracy line (decision 13).

## Invariants

- Every judgement the evaluator applies is data in a committed file, never a constant in code; the judging set, weights, and guard list do not change after the numbers are seen.
- Names are written in full: RQ0 gate spec, RQ0 gate evaluator, guard spec, per-experiment spec, driver table tuning set.

## Open items

- The values K, g, and N: each sub-task's own grill, with grounding written beside the number.
- Enumerating `random`'s draw space instead of sampling it: named to 박이안 in the memo as a future option, not adopted.
