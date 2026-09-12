# scores

The scores file is where a run's aggregates become a comparison: how much of the oracle's improvement over the fixed baseline this run captured, term by term and then for the file as a whole. It is the input to the RQ0 verdict and to every Layer-2 number the paper reports.

## What a row is

Two levels. A `term` row is one scoring-spec term of one run: the aggregate's value under `fixed`, under `oracle`, and under the run's own condition; both improvements; the normalised `share`, which is the run's improvement over the oracle's, signed by the term's direction; the `weight`; and two marks, `no_headroom` when the oracle's own improvement fell below the aggregate's floor and `censored` when the underlying aggregate was. A `file` row is the run's weighted score: the sum of weight × share over its terms, with `weight_sum`, `n_terms`, `n_no_headroom`, `n_censored` beside it. The oracle's file score is therefore its weight sum, and the gap RQ0 measures is one minus a run's score over that. `schema/scores.schema.json` is the machine form; `docs/harness/metrics.md` §9 the definitions.

## How runs are paired

A run's `fixed` baseline is the `fixed` run with the same workload and the same `boot_default`; `fixed` carries no table, so one baseline serves both tables. Its `oracle` is the `oracle` run with the same workload, table, and boot default. An alternative-default `fixed` run re-scores the oracle and every other condition against itself, and those rows carry the alternative's stem in `boot_default`, which is how the sensitivity line in the report is formed without re-running anything but `fixed`.

## Two rules to know before reading a score

- A no-headroom term keeps its weight and enters the file score as if the run had captured all of the headroom, share 1. This keeps a file's score comparable across conditions when one of its terms has nothing to measure; the mark says which terms those were.
- A judging file whose every term is no headroom counts, in RQ0, as not meeting the gap threshold. That is the RQ0 gate spec's rule, not the scorer's.

## How it is produced and read

`tools/score.py` writes it beside the aggregates; the runner writes one per experiment. The RQ0 gate evaluator reads the `file` rows for gaps and the seed statistics, the `term` rows stay for inspection. `tools/tests/fixtures/mock-scores/` carries hand-worked expected scores with the derivation in its `worked.md`.
