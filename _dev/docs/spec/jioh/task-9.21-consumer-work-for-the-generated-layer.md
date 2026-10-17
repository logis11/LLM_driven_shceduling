# 9.21 — Consumer work for the generated layer

Sub-task 9.21 of Phase 9 (spec decision 9, the generated layer; decision 6, "their consumer work" before the sweep): the harness and the dataset tools made able to read the five generated sets 9.19 and 9.20 built — scoring terms, the coverage table, the grid axes, the hold-time plan's measurement, the CI build. Decided in the 2026-10-13 grill. Parent: `_dev/TODO.md`, (jioh, 9.21).

## Scope

- Scoring terms for the 1,562 generated files, assigned by rule from the sixteen C1 entries, not written per file.
- The coverage table over the generated layer, beside the core set's.
- The generated sets' file-level axes — pair, form, middle length, interval, split, relation, shared focus name, tier, carrier — readable by the harness, and usable by an experiment spec to select files.
- The hold-time plan's step-1 material confirmed present, and the flip count with its cost delivered as the plan assigns to this sub-task.
- The CI build strategy for the generated layer decided on the measured size and time.
- The documents that describe these consumers restated here; the scoring spec re-frozen and the RQ0 gate spec re-pinned; one Linux CI run.

## Locked decisions

### 1. Generated files are scored by a run-time rule from the C1 entries, as the variants are

No generated file has an entry in the scoring spec. Its terms are derived when the harness runs, the way `with_variants` derives a variant's from its base's (9.14 decision 12): for each placement in the file — a mode's C1 task set under one id suffix — the `c1-<mode>` entry's terms, their entities carrying the placement's suffix, their latency and periodic terms windowed to the segments the placement is labelled in, their batch terms unwindowed. The rule's statement lives in the scoring spec's text, so it is pinned with the spec. The generator records each file's placements — the mode, the suffix, the labelled segments, whether the placement has an input window — in the manifest's grid record, the harness's one source for them; the five manifests are re-blessed, their artifacts unchanged.

### 2. A placement labelled in no segment carries no term

In the distractor grid both segments are labelled A; B's task set arrives under its own suffix and holds no label. B's tasks carry no term: the score reads the labelled situation, and B's effect on the user is in A's terms. The same reading as Phase 7 spec decision 10 (unwanted work carries no term).

### 3. A placement without an input window drops its input-channel terms alone

Where the generator placed no input window (a segment of `no_input_below` or less, 9.19 decision 3), the placement's `channel: input` terms are dropped, since they would read no row; its timer-channel terms and its periodic job terms stay. The rule adds no judgement of its own — it follows the fact the generator already decided.

### 4. The generated layer's coverage table is derived from the manifests

The generator records each file's segment labels — mode, `background_wanted`, tier, `pre_committed_miss` — in the manifest's grid record, and the coverage tool derives a generated-layer table per set from the committed manifests alone, written beside the core set's table in the same artifact and drift-checked by the gate. No empty-cell rule applies to it: the sets' full enumeration is asserted by the generator's tests, and the ladder fills one cell per mode by design. The timeline lints already run on every generated file at generation; nothing is added, the fact is stated.

### 5. The file-level axes reach the harness by a manifest join; the records are unchanged

The records keep their columns. The harness gains a reader of a manifest's grid section — workload id to axis record — which an experiment spec's reporting lines use to group by an axis, the manifest pinned by the spec as the RQ0 gate spec pins the dataset's. The lint checks that a key a spec names exists in the pinned manifest. `familiarity` and `pre_committed_miss` stay on the rows, where the segment puts them.

### 6. An experiment spec selects files from a manifest by its axes, built now

The experiment spec's file list accepts a selection — a manifest and a condition on its grid keys, such as the return grid's `split: measurement` — expanded to ids before anything else runs and linted against the pinned manifest. The RQ0 gate spec keeps its explicit lists. Not deferred to the RQ1 or RQ4 experiment spec sessions.

### 7. The flip count and its cost are one reporting line over the rows that exist

A reporting line reports, per file and condition: the number of configuration changes the daemon applied, the number of those whose query the grader marked `config_correct` false (one query yields one schedule entry, contract 7), the sum of the per-switch excess over the switches into MLFQ among them (metrics doc §8), and the file's score beside them. No new primitive, metric or records column; defining a flip's cost beyond this is the RQ4 experiment spec session's, on real traces. The hold-time plan's step-1 material — the flap-stress set split by seed, the return grid split by pair — is confirmed present, and the plan's table records this sub-task as having delivered the line.

### 8. The generated layer is built in every CI run

The three workflows keep building the five sets on every run (5 min 13 s of a 12 min 04 s run on the 4-vCPU runner; 1,562 artifacts, `build/` 6.8 GB; 9.20 D10, CI run 38243554308). The dataset README states the strategy with the measurements and the criterion for revisiting it — the generated step's time and the build's size against the runner's disk, the next set added being the occasion. On-demand builds and pinned subsets are not taken: both put an exception into the gate's rule that `build/` equals the union of every manifest.

### 9. Documents, pins and verification

The scoring spec's text change re-freezes it; the RQ0 gate spec's scoring-spec pin follows; one harness changelog entry carries the rule, the selector, the flip line and the re-pin. The five generated manifests' new hashes go to the sub-task changelog and to 9.16; the core set's and the variants' manifests are unchanged. Restated here: the dataset README, the metrics doc where the flip line needs a definition, the harness records README, the experiment spec's schema documentation, the hold-time plan, the harness changelog. The harness guide, the coreset guide, the proposal, the research-claims chain and the daemon guide are 9.15's. Verification: the dataset and harness test suites, a hand-worked fixture for the flip line, `make check`, one Linux CI run whose id goes to the changelog.

## Invariants

- Every generated file is reporting material; the RQ0 gate spec's file lists do not change.
- An idle placement carries no term, as `c1-idle` has no entry; a file whose placements all carry none has no scoring entry and the scorer skips it.
- The Layer-1 exclusion lint runs over a spec's expanded file list, so a selection that brings in the 26 distractor files with `pre_committed_miss` is checked as the core set's are.
- The schema, the compiler, the lints and every artifact are unchanged; the 9.19 and 9.20 manifests move only in their grid records.
