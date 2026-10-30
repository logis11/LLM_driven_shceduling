# experiments

A per-experiment spec is the pre-registration of one experiment as data the harness executes: which conditions, how many seeds, which boot defaults, which files judge and which only report, which guard failures are exempt and why, which reporting lines the report carries, which bytes of the scoring spec, guard spec, driver table, and dataset it was written against, and the criterion that turns scores into a verdict. The runner reads the generic part as its run matrix; the RQ0 gate evaluator reads the whole file. Every judgement the evaluator applies is in the spec, never a constant in code.

`rq0-gate.yaml` is the RQ0 gate spec, committed 2026-09-12. Only pre-registered experiments live here; the smoke run generates its spec in a temporary directory and discards it.

## Anatomy of a spec

```yaml
experiment: rq0-gate
conditions: [fixed, random, oracle]
telemetry: [focus]                              # the shapes shown to the recognizer: every condition under each; the criterion judged on the first (9.17)
seed_count: 100                                 # seeds 1..N for every condition that draws
boot_defaults: {primary: ostep, alternatives: [ostep-slice-500us, …]}
files: {judging: [...], reporting: [...],
        select: [{manifest: return-grid, where: {split: measurement}}]}   # files chosen from a generated set's manifest by its axes (9.21); added to reporting
layer1_exclusions: [...]                        # derived from pre_committed_miss over the expanded list; the lint checks it
guard_exemptions: [{guard, workload, conditions, reason}]
reporting_lines: [{type: sensitivity, …}, {type: floor_band, …}, {type: g_band, …}, …]
statements: [{id, text}]                        # pre-registered text, echoed verbatim into the report
pins: {scoring_spec, guard_spec, driver_table, dataset,    # path + sha256
       generated: {return-grid: {path, sha256}}}           # one pin per generated set's manifest a selection or a line reads (9.21)
criterion: {type: k_of_n_gap, k: 13, g: 0.5, reference: oracle, compared: random, seed_statistic: mean}
```

The RQ0 gate spec's `statements` carry the reason behind every number in it: the judging rule and the re-entry condition for two files, the executor assumptions pending confirmation, the groundings of g, K, and N, the prior table's duplicate structure, the design of the boot-default sweep, the failure procedure, and the held-out-rows pre-registration. Read them before reading the numbers.

## The criterion and the lines

`k_of_n_gap` is RQ0's criterion: at least K judging files show a gap of at least g, the gap being one minus the compared condition's seed-mean score over the reference's. A failed non-exempt guard on a run the criterion reads makes the verdict `invalid` instead of pass or fail.

Reporting lines are typed and each has a function in the evaluator: `sensitivity` recomputes the verdict count under each alternative boot default and prints the reason per point; `floor_band` and `g_band` recompute it under a band of latency floors and of gap thresholds at scoring time; `seed_standard_error` prints the precision the seed count bought, per file; `exclusion_accuracy` and `layer1_headline` read the grades file; `random_beats_oracle` flags files where the compared mean exceeded the reference; `note` binds a pre-registered sentence to one workload.

Five more since 2026-10-09 (sub-task 9.14, decisions 10 and 12) read **variant files** — rebuilt judging files listed under `files.variants`, run under the primary boot default alone and never judged, pinned through `pins.variants` by their manifests: `variant_set` recomputes the verdict count with each named judging file's gap taken from its variant (the venue factor, the chain scale, a segment length, the carried half-widths at a bound); `trace_replay` compares each named file's gap with its rebuild on a measured wake sequence and reports agreement under a tolerance; `bounding_pair` reports two files that differ in one task's declared class alone; `input_wake_count` prints, per judging file and interaction-latency term, the number of observations its P99 rests on (an `input_latency` term's keystrokes); `longest_wait` prints each run's longest `ready_wait` against the starvation floor and flags any past the reopen point.

Since 2026-10-13 (sub-task 9.21) a spec may **select files from a generated set** instead of listing them: `files.select` names a manifest pinned under `pins.generated` and a condition on the manifest's grid records — `split: measurement` for the return grid's or the flap-stress set's measurement half, `form: focus` for one form of the transition grid, `tier: 5` for one rung of the ladder — and the runner, the lint and the evaluator expand it to ids before anything else runs; the selected files join `reporting` (every generated file is reporting material) and the Layer-1 exclusion lint runs over the expanded list. A selected file's compiled artifact is read from `dataset/build/` through the manifest, and its scoring terms come from the scoring spec's generated-layer rule, not from an entry. The same manifest's record is where a reporting line finds a file's axes, by `workload_id`; the records keep their columns. One more line, `flip_cost`, prints per recognizing run the configuration changes the daemon applied, those on a query graded config-incorrect, the per-switch excess summed over the wrong switches into MLFQ, and the file's score — the hold-time plan's step-1 measurement (`_dev/docs/plan/jioh/hold-time-and-hysteresis.md`). The RQ0 gate spec uses none of these: its lists stay explicit.

## The report

`schema/report.schema.json` is the shape of the one machine-readable report per experiment run: header, verdict and its detail, per-file gaps with every per-seed score beside the mean, every scored run, the provenance breakdown, every guard result, the statements, and the lines. `report.md` beside it is rendered from the JSON and never edited by hand; paper tables come from the JSON.

## Commands

```
python3 tools/experiment_lint.py [--spec experiments/rq0-gate.yaml]      # schema, files against the build, terms, registries, pins
python3 tools/evaluate.py --spec … --aggregates … --scores … --guards … --grades … --out-report report.json --out-render report.md
python3 tools/run.py --spec experiments/rq0-gate.yaml --machine runner.yaml   # the whole matrix, then evaluate
```

`evaluate` exits 0 on pass, 2 on fail or invalid, and 1 on a refusal: a pin mismatch or an incomplete run set writes nothing. Changing a frozen file means a new pin here and an entry in `../CHANGELOG.md` first.
