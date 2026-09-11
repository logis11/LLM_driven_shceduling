# Task 8.4 — L1 grader

The Layer-1 grader: a recognition log graded against ground truth into recognition records rows, and the accuracy file computed over them. Parent: `_dev/TODO.md` (jioh, 8), sub-task 8.4; Phase 8 spec decisions 13 and 21; metrics doc §7 and §8. Decided in the 2026-09-11 grill.

## Scope

- Recognition records rows from a recognition log, a compiled workload's ground truth, and a driver table.
- The `grades` file with its schema: the Layer-1 statistics, confusion matrices, per-class recall, and paired comparisons.
- The configuration-distance line and the oracle-perfection consistency message.
- A new `mock-grades` fixture and tests.
- Doc touches: the metrics doc, the records schema, `docs/references.md`, the two README files, and the harness guide's recognition chapter.

Out of scope: the familiarity experiment, run-to-run consistency and distractor robustness, the mock daemon that will produce real logs (8.5), the runner (8.6), the RQ0 gate evaluator and the report (8.7), and the freeze (8.8).

## Locked decisions

### 1. A separate records file

The grader's rows are records rows in the committed format and schema, written to their own file per recognition log. The metrics doc §5 already states one file per trace or per recognition log, and `source_sha256` is the hash of whichever artifact the row came from. The trace records and the recognition records are joined by identity at scoring time.

### 2. The grader owns the recognition aggregates

The grader computes the Layer-1 numbers itself and writes its own `grades` file, rather than the aggregates module gaining them. The aggregates row is keyed by entity, metric, cause, and window, which fits neither a confusion-matrix cell nor a pooled accuracy, and the aggregates module recovers its window end from a `busy` row that a recognition-only file does not have. The aggregates module's docstring line assigning the recognition aggregates to this sub-task is superseded.

### 3. `pre_committed_miss` becomes a records column

Records gain a twenty-second column, `pre_committed_miss`, carried from the covering ground-truth segment onto recognition rows exactly as `familiarity` already is. The exclusion is then applied when the numbers are formed rather than by withholding rows, so the with-and-without-exclusion line falls out of one pass, and a reader of the records file alone can tell which rows the headline excluded.

### 4. Balanced accuracy on the binary attribute only

The attribute headline is balanced accuracy with the Matthews correlation coefficient beside it. Mode and algorithm choice report raw accuracy with its majority baseline, the full confusion matrix, and per-class recall, and no macro-average is computed on either. Raw accuracy never appears without its majority baseline on any axis. This restores the Phase 7 spec's own scoping, which named the attribute specifically; Phase 8 spec decision 21 dropped that word when compressing it.

### 5. No multiclass chance-corrected statistic

The measured mode baseline leaves nothing for one to correct, and the candidate source could not carry the load: its full text is paywalled, its abstract states neither the reduction to the binary coefficient nor the range nor the chance value, it makes no imbalance argument, and a published criticism reports the statistic reading too optimistically for poor classifiers at high class counts.

### 6. Clustered intervals and paired comparisons

Every interval comes from a seeded cluster bootstrap that resamples workload files, because query points inside one file share its process names and its situation and are not independent observations. Condition comparisons are computed paired, on the same drawn files, since every condition is graded on identical query points. The seed, the repetition count, and the interval level are constants with the metrics doc §10 as their normative home, carrying the same stated-assumption status as the latency floor, and the RQ0 gate spec pins them. Determinism here means reproducibility: a pinned seed makes reruns byte-identical.

### 7. The configuration-distance line

For every graded query point the grader composes the configuration implied by the true driver-table row and by the predicted row, and records whether they are identical over algorithm, parameters, and cap together. The reported number is what fraction of a condition's errors changed the configuration at all. It uses the table the run itself used, named in the row's `table` column, because the question is about the run that happened; this differs from the algorithm-choice metric, which the metrics doc pins to the calibrated table. A test checks the harness's composition against the daemon's on every row of the committed prior table, so the two implementations cannot drift silently.

### 8. Familiarity is carried, never aggregated

The tier stays a column on the records row and the grader computes no per-tier aggregate. Familiarity answers a different question from Layer 1's, namely the ceiling of a rule-based recognizer, and its evidence is structural rather than a rate. It becomes its own per-experiment spec under the shared schema that Phase 8 spec decision 8 defines. The metrics doc §8 line requiring every recognition aggregate also per familiarity tier is amended accordingly.

### 9. The grader grades everything it is handed

File selection belongs to the per-experiment spec, not to the grader. The grader skips only what the rules skip, being the terminal snapshot and `ambiguous` segments, applies the pre-committed-miss exclusion to the headline while also computing the unexcluded figure, and never decides on its own that a file is uninteresting.

### 10. The `grades` file

One file with a level discriminator over statistic, class recall, confusion, and paired rows, and a schema whose required fields depend on the level, mirroring the scores file's structure. Identity is condition, table, and seed; there is no workload, because the numbers are pooled across files, and the boot default has no bearing on recognition. Every row carries `pre_committed_miss_excluded` and its sample count. Interval bounds appear only where an interval was computed. A paired row names the other condition.

### 11. Off-menu answers

A predicted mode outside the sixteen-label menu scores incorrect and is recorded verbatim in `predicted`, with its own confusion-matrix row rather than being folded into a real class. A truth mode outside the menu is refused outright, since a malformed answer key is a broken input rather than a result. The same asymmetry applies to the four-algorithm set. The realistic path remains `proposal: null`, which the metrics doc §7 already defines as zero on both correctness metrics with an empty `predicted`.

### 12. Algorithm-choice grading is built now

The driver table's shape is committed and a calibrated table will differ in values and role, not structure, so the metric is implemented against that shape rather than deferred to whichever phase first runs `llm_algo`. The harness reads the YAML directly rather than importing the daemon's module, keeping the trees uncoupled. Rows are emitted only for `llm_algo`, and the grader refuses to grade when handed a table whose role is prior, so the delegation rung cannot be scored against the wrong table.

### 13. The oracle-perfection consistency message

When a condition named `oracle` is not perfect on graded points, the grader returns a message naming the condition, the file, and the query point, which the CLI prints before exiting non-zero. This follows the primitives' existing pattern. It is not a ninth guard, which would reopen a list the phase spec fixes at eight and freezes in 8.8, and it is not a new row, since the grades file already carries the oracle's accuracy. What was missing was a loud failure, not another number.

### 14. Entry point

One manifest-driven CLI covering the whole run set, with the per-run grading step exposed as a library function beside it. The bootstrap and the paired comparison force the set-level shape regardless, and the runner in 8.6 already produces manifests for the guards. The pooled stage is deliberately not folded into the scoring CLI, which exists to apply the scoring spec that Layer 1 never reads.

### 15. No grading spec

The statistics and constants live in code with the metrics doc §10 as their normative home and its changelog as their audit trail, exactly as the scoring floors and the interaction threshold do. A third research-wide data file would mean a third schema, a third lint, and a third freeze for choices the metrics doc already governs. A later Layer-1 judgement that a gate reads belongs in the per-experiment spec beside the exclusion list.

### 16. Fixture

A new `mock-grades` fixture in the shape of `mock-scores`, which is already a fixture that is not a trace pair. It carries several files, so the bootstrap has clusters, and several conditions, so the paired comparison has a partner, and covers a null proposal, a skipped `ambiguous` segment, a skipped terminal snapshot, a pre-committed-miss segment, a familiarity annotation, and the algorithm axis against a miniature table. Every point estimate is hand-worked. The interval is verified two ways: one test enumerates the exhaustive bootstrap distribution over the fixture's few files and checks the seeded implementation converges to it, and the committed expected file pins its bounds at a small pinned repetition count. The `worked.md` states which numbers are hand-derived and which are the enumeration's.

### 17. Documentation

The metrics doc gains the twenty-second column in §5, the pre-committed-miss exclusion in §7 where only `ambiguous` and the terminal snapshot are named today, the amended recognition row and the Layer-1 statistics in §8, the bootstrap constants in §10, and a changelog entry. The records schema gains the column. Both README files gain their lines. The harness guide's recognition chapter carries a stale row showing `validation` as a metric with a string value, which the frozen records schema does not allow, and it is corrected here rather than in the 8.9 sweep, on the same reasoning as 8.3: a chapter contradicting the frozen schema is a correctness bug.

### 18. References

Four verified entries are added under the scholarly grounding section, whose tier rule already names statistical claims: Brodersen and colleagues 2010 for balanced accuracy, restricted to the binary case and never cited for a multiclass measure or for an interval; Chicco and Jurman 2020 for the Matthews correlation coefficient and the imbalance caveat, never cited as preferring it to balanced accuracy; Field and Welsh 2007 for the cluster bootstrap, carrying its consistency condition in the number of clusters and its anti-conservatism at very few clusters; and Dietterich 1998 for the paired comparison on one test set and for the two alternatives it rules out.

### 19. The measured dataset facts

The grill measured the graded set by applying the telemetry rules to the compiled coreset, as a one-off, because no recognition log exists yet. Those numbers are recorded in this spec as facts measured on 2026-09-11, with the derivation named, and no tool is built: a permanent tool would put a second implementation of the daemon's query-point rules inside the harness, and from 8.6 onward the grades file carries the counts by its own schema and cannot go stale.

| quantity | value |
|---|---|
| query points in the coreset | 134 |
| skipped as terminal snapshots | 50 |
| skipped inside an `ambiguous` segment | 2 |
| graded | 82, across 49 files |
| carrying `pre_committed_miss` | 10 |
| headline set after exclusion | 72, across 44 files |
| attribute truth | 57 true against 25 false |
| attribute majority baseline | 69.5 per cent |
| mode classes present | all 16, largest 11.0 per cent |
| query points per file | mean 1.67, 22 files with one, maximum 5 |
| graded points at familiarity tiers 4 and 5 | one each |

The attribute is corrected because its baseline is high; mode is not because its baseline is low. The 2026-09-10 coreset memo estimated the attribute baseline at about 71 per cent from segment counts and said the query-point figure was unknown until a log existed; it is now known and agrees.

### 20. Stated limitations

Two limitations are written into this spec rather than discovered while writing the paper. At 44 to 49 independent units a proportion near one half carries an interval of roughly eleven percentage points before clustering widens it, so Layer 1 is well powered against `random`, whose separation needs no statistics, and underpowered for the whitelist comparison that carries the scientific content. And the whitelist-ceiling contrast at familiarity tiers 4 and 5 rests on one graded query point per tier, so it is reportable as a demonstration, which needs no sample size because the whitelist's failure there is true by construction, and never as a rate.

## Invariants

- Every number in the `grades` file carries its sample count, so no figure can be read without its denominator.
- A statistic is cited only within its source's stated role; where no verified source covers a choice, it is marked a stated assumption rather than attributed.
- The harness does not import the daemon's or the dataset's modules; where it must reproduce their logic, a test pins the two together.

## Open items

- The familiarity experiment needs its own per-experiment spec. Supporting a rate rather than a demonstration would need the annotation authored on many more timelines, which is dataset work.
- Run-to-run consistency and distractor robustness remain unmeasurable, blocked on the repeat index the recognition log's envelope does not carry, already raised with 박이안 in the repeat-samples memo.
