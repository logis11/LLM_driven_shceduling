# 11.3 — The re-measurement

Sub-task 11.3 of 인지오's Phase 11 (`_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 6), decided on 2026-11-20: the re-measurement the RQ0 gate spec's statement `re-measurement-contingency` names (`harness/experiments/rq0-gate.yaml`) — the entry whose carried value moved `c7-ml-train` across g found, re-measured at a count fixed here, folded in by a second bless, and the first verdict's provisional status closed.

## Scope

- The finding step: the carried values `c7-ml-train` holds moved one at a time (decisions 1 to 4).
- The campaign on each entry found, at its count (decisions 5 to 7).
- The fold-in and the second bless (decisions 8 to 10).
- The runs on the rebuilt judging files: the closing of the first verdict and the runs on the current programs (decisions 11 and 12).
- The record and what stays on disk (decisions 13 and 14).

## Locked decisions

### 1. The values moved

`c7-ml-train` holds two entries of the library, the editor (`code-editor`) and the training run (`cpu-batch`'s `python3`), and four of the values `dataset/variants.yaml` lists under `carried_values`:

| entry | value | half-width |
|---|---|---|
| `code-editor`, `utility/libuv-worker` | gap table | ±5.63 % |
| `code-editor`, `utility/libuv-worker` | run table | ±2.36 % |
| `cpu-batch`, `python3` | runs between voluntary blocks | ±27.3 % |
| `cpu-batch`, `python3` | block per run | ±10.8 % |

### 2. The finding test

Four builds of `c7-ml-train`, each with one of the four values at the lower bound of its interval and the other three at the library's values. Each build gets the 102 runs the criterion reads: `fixed`, `oracle` and the 100 `random` seeds. A value moved the file when its build's gap is below g = 0.5 under the scorer as run, at the run's 1,000 µs floor.

Two controls beside the four builds: the build with nothing moved reproduces the RQ0 run's values at the primary, and the build with all four moved reproduces the RQ0 run's values on `c7-ml-train@corner-low`, both to the last digit.

### 3. Outcomes other than one value

Every entry holding a value that moves the file alone is re-measured. If no value moves it alone, the six pairs are built, then the four triples if no pair moves it, and every entry holding a value in a smallest moving set is re-measured. This is a reading of the statement's wording, "the entry whose value moved it", committed before the builds run.

### 4. The finding step's simulator

The finding step runs on the RQ0 run's simulator, `simulator@0d323c84470a`, rebuilt from its source.

### 5. The counts

The count is the one the stability rule projects at the pool as carried:

| entry | count | source |
|---|---|---|
| `code-editor` | 56 repeats | 9.5 D83, `utility/libuv-worker`'s wake rate and gap mean at ±5.63 % over 44 repeats, "the rule needing 56" |
| `cpu-batch`, `python3` | 107 repeats | the campaign's pooled record over 6 repeats (`_dev/research/jioh/task-9.10-scenarios-timelines/campaign/mnist/results/pooled.json`): 107 for the runs between voluntary blocks, 19 for the block per run, the larger taken |

Both counts are fixed before the finding step runs. A campaign stops at its count whether or not the 5 % tolerance holds there.

### 6. Fresh repeats

Every repeat of the count is new. The existing pool is left out of the re-measured value.

### 7. The campaign's method

The entry's original campaign's method unchanged: its workflow, pinned software, settings and validity rules. The count is of valid repeats; a job stopped by the machine gate, or left out under a rule the original method names, is replaced and its reason recorded, and no repeat is left out for any other reason. The editor's 56 repeats are one per window of the recording that holds input. A difference the venue forces is recorded; if it changes what is measured, the campaign stops for 인지오's decision. The campaign has its own tag, and its raw records are a GitHub release mapped in `dataset/meas-releases.yaml`.

### 8. The fold-in

The fresh campaign replaces the found entry's exception-carried values, each exception kept whole: for the editor, `utility/libuv-worker`'s wake rate, gap mean and run mean together; for the training run, the runs between voluntary blocks and the block per run. Every other value of the entry stays as its original campaign measured it, and the entry's scope states both campaigns.

The fresh campaign's other values are reported beside the library's, each inside the library's stated interval or not, and change nothing. A value held to the rule that falls outside the library's interval is recorded as a finding for Phase 12.

### 9. The values' status afterwards

A re-measured value keeps its exception class, its scope stating the fresh campaign's half-width, range and count. `carried_values` in `dataset/variants.yaml` takes the new half-width. Whether the second RQ0 gate spec keeps a carried-half-widths line or a contingency on the value is Phase 12's.

### 10. The second bless

The coreset, the five other sets under `dataset/build/` and the 78 sensitivity variants are rebuilt on the re-measured library and blessed, with a report of the artifacts that change beyond the library hash. The RQ0 gate spec is not edited: its dataset pins name the first bless, as its simulator pin names the RQ0 run's simulator. Phase 12's second RQ0 gate spec pins the second bless.

### 11. The closing

Every judging file holding the found entry is rebuilt on the re-measured library and gets its 102 criterion runs on the RQ0 run's simulator, scored under the scorer as run, through a throwaway copy of the RQ0 gate spec.

| entry | judging files holding it |
|---|---|
| `code-editor` | `c2-p1a`, `c1-compile`, `c1-ml-train`, `c7-dev`, `c7-compile`, `c7-ml-train` |
| `cpu-batch`, `python3` | `c2-p1a`, `c1-ml-train`, `c7-ml-train` |

The other judging files' rows are carried from the RQ0 run, after a check that their artifacts change in nothing but the library hash. The run record's dated correction states the count at the re-measured value, the verdict against K = 10, and "final" in place of "provisional".

### 12. The runs on the current programs

The same rebuilt files get their 102 criterion runs on the fixed simulator, `simulator@841dc81131cb`, scored under the fixed scorer. The run record's correction states the post hoc reading at the re-measured value beside the closing count. With 11.2's rerun for the unchanged files, these are the corrected runs on the re-blessed dataset; how the configuration search's picks are computed from them is 11.4's.

### 13. The record

11.3 writes:

- the harness changelog entry;
- the dated correction in `docs/rq0-run-record.md`: the finding (each build's `fixed` and `oracle` P99 and its gap, the entry found), the campaign (its tag, its count, the values before and after), the closing count with "final", and the post hoc reading;
- the dated correction in `docs/memos/2026-11-18-rq0-run-result.md`;
- the archetype's scope, the exceptions and campaign figures of `docs/workload/measurement-overview.md`, and `dataset/meas-releases.yaml`.

Every other doc that quotes the old figures, the guidebook volumes and the docs index among them, is 11.5's.

### 14. On disk

The finding step's builds are built from a copy of the library under the sub-task's research folder, `_dev/research/jioh/task-11.3-the-re-measurement/`; they are not added to `dataset/variants.yaml` and are never blessed.

At 11.3's end the RQ0 run's traces of `c7-ml-train` and its four variants are deleted, and the traces of the finding step's runs and of decision 11's runs with them, their aggregates and scores kept in the research folder. `runs/rq0-gate/aggregates.csv` and `runs/rq0-gate/scores.csv` stay until Phase 12's second RQ0 run. Decision 12's runs stay on disk whole until 11.4 ends.

## Invariants

- This spec is committed before any run of the finding step.
- A control of decision 2 that does not reproduce the RQ0 run's values stops the finding step; the mismatch is diagnosed before any build is read.
