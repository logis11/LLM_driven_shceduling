# The degraded oracle (11.2)

The record of sub-task 11.2 (`_dev/docs/spec/jioh/task-11.2-the-degraded-oracle.md`). The paths in the files are relative to the repository root; each script runs from there.

| file | what it holds |
|---|---|
| `cases.md` | decision 8's case table: one row per case — the file, the term, the combination, the class, the evidence, the fixing commit — and each case's reading, its counterfactual's prediction recorded before the run |
| `cap_check.py`, `cap-check-<file>.json` | one run's trace read against the batch-class rule and the cap — every park on a batch-class task while a non-batch task is runnable, no parked task running, the batch class's CPU while capped within the cap and the bucket's depth — and the scored task's `input_latency` rows recomputed by the metrics doc's §6.12 against the run's records |
