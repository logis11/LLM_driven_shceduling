# mock-scores — worked derivation

Hand-written records (not traces) for one small workload, `mock-score`, under five runs, with the aggregates, shares, and scores derived by hand. Built for sub-task 8.2 to hit every scorer rule: a windowed P99, a miss-rate term with no headroom, a progress term, a turnaround that finishes under `oracle` and is censored under one `random` seed, and an alternative-boot-default `fixed` run that re-scores the same `oracle` and `random` runs. `T_end` = 100000. All times µs. `seam/` holds hand-written `fixed` and `oracle` records for `mock-p1a`, used by the end-to-end seam test with the records the writer produces from `mock-p1a`'s trace.

## Scoring spec (`scoring-spec.yaml`)

| term | entity · metric · aggregate | filter | direction | weight |
|---|---|---|---|---|
| 1 | `editor` · `ready_wait` · P99 | `cause = wake`, window [10000, 100000] | lower | 1.0 |
| 2 | `video` · `job` · miss rate | — | lower | 0.5 |
| 3 | `train` · `cpu_delivered` · progress | — | higher | 0.5 |
| 4 | `build` · `turnaround` · turnaround | — | lower | 0.5 |

Weight sum 2.5.

## Runs (`records/`)

| file | condition | table | seed | `boot_default` |
|---|---|---|---|---|
| `fixed.csv` | `fixed` | — | — | — (primary) |
| `oracle.csv` | `oracle` | prior | — | — |
| `random-s1.csv` | `random` | prior | s1 | — |
| `random-s2.csv` | `random` | prior | s2 | — |
| `fixed-alt.csv` | `fixed` | — | — | `alt` |

Every run has the same shape: `editor` with an `arrive` row at 0 and five `wake` rows at 5000, 20000, 40000, 60000, 80000 (the 5000 row lies outside the term's window); `video` with three `job` rows at 16667, 33334, 50001 (period 16667) and values 5000, 6000, 7000 in every run (all met); `train` with `cpu_delivered` and `demand` 80000 at `T_end`; `build` arriving at 10000 with `demand` 30000; `lane` `busy` at `T_end`; `schedule` `config_interval` rows (one `fallback` entry for the `fixed` runs; a zero-length `fallback` entry beside an `unmodified` one for the others).

## Term 1 — editor P99 (wake, window [10000, 100000])

The window keeps the four rows at 20000, 40000, 60000, 80000. P99 by the linear rule on four sorted values: position `(4 − 1) · 0.99 = 2.97`, so `v[2] + 0.97 · (v[3] − v[2])`.

| run | in-window waits | P99 |
|---|---|---|
| `fixed` | 8000, 12000, 20000, 40000 | 20000 + 0.97 · 20000 = **39400** |
| `oracle` | 1000, 2000, 3000, 4000 | 3000 + 0.97 · 1000 = **3970** |
| `random` s1 | 4000, 6000, 10000, 20000 | 10000 + 0.97 · 10000 = **19700** |
| `random` s2 | 8000, 12000, 20000, 40000 | **39400** (equal to `fixed`) |
| `fixed` alt | 6000, 9000, 15000, 30000 | 15000 + 0.97 · 15000 = **29550** |

The whole-file wake P99 (five values, the 5000 row's 100 included) is 39200 under `fixed`: position 3.96, `20000 + 0.96 · 20000`. It is in the aggregates file and scored by nothing.

Lower is better, so `improvement(c) = fixed − c`. Against the primary `fixed`: `improvement(oracle)` = 35430 (above the 1000 floor); s1: 19700, share 19700 / 35430 = **0.556026**; s2: 0, share **0**. Against the alternative `fixed`: `improvement(oracle)` = 25580; s1: 9850, share **0.385066**; s2: −9850, share **−0.385066** (worse than that floor, shown as is).

## Term 2 — video miss rate

Three ticks, values 5000, 6000, 7000, all at or below the 16667 period, in every run: miss rate 0 everywhere. `improvement(oracle)` = 0, below the 0.01 floor → **no headroom** in every run. The share is left empty; in the file score the term counts at share 1 with its weight 0.5.

## Term 3 — train progress

`cpu_delivered / demand`, demand 80000. Higher is better: `improvement(c) = c − fixed`.

| run | `cpu_delivered` | progress |
|---|---|---|
| `fixed` | 20000 | 0.25 |
| `oracle` | 40000 | 0.5 |
| s1 | 30000 | 0.375 |
| s2 | 24000 | 0.3 |
| `fixed` alt | 16000 | 0.2 |

Primary: `improvement(oracle)` = 0.25; s1 0.125 → share **0.5**; s2 0.05 → **0.2**. Alternative: `improvement(oracle)` = 0.3; s1 0.175 → **0.583333**; s2 0.1 → **0.333333**.

## Term 4 — build turnaround

`build` arrives at 10000. Where it completes, the records carry `completed` 1 at the end time and `turnaround` = end − 10000; under s2 it does not complete (`completed` 0 at `T_end`, no `turnaround` row), so the aggregates carry `turnaround_censored` = `T_end − arrival` = 90000 and the term is marked censored.

| run | end | turnaround |
|---|---|---|
| `fixed` | 90000 | 80000 |
| `oracle` | 60000 | 50000 |
| s1 | 70000 | 60000 |
| s2 | — | 90000 (censored) |
| `fixed` alt | 95000 | 85000 |

Lower is better. Primary: `improvement(oracle)` = 30000; s1 20000 → **0.666667**; s2 −10000 → **−0.333333**. Alternative: `improvement(oracle)` = 35000; s1 25000 → **0.714286**; s2 −5000 → **−0.142857**.

## File scores

Weighted sum with the no-headroom term at share 1:

| run | baseline | terms 1 · 2 · 3 · 4 | score |
|---|---|---|---|
| `fixed` | primary | 0 · (1) · 0 · 0 | 0.5 · 1 = **0.500000** |
| `oracle` | primary | 1 · (1) · 1 · 1 | **2.500000** |
| s1 | primary | 0.556026 · (1) · 0.5 · 0.666667 | 0.556026 + 0.5 + 0.25 + 0.333333 = **1.639359** |
| s2 | primary | 0 · (1) · 0.2 · −0.333333 | 0.5 + 0.1 − 0.166667 = **0.433333** |
| `fixed` | alt | 0 · (1) · 0 · 0 | **0.500000** |
| `oracle` | alt | 1 · (1) · 1 · 1 | **2.500000** |
| s1 | alt | 0.385066 · (1) · 0.583333 · 0.714286 | 0.385066 + 0.5 + 0.291667 + 0.357143 = **1.533876** |
| s2 | alt | −0.385066 · (1) · 0.333333 · −0.142857 | −0.385066 + 0.5 + 0.166667 − 0.071429 = **0.210172** |

Each run scored against the alternative baseline carries `boot_default` `alt` in `scores`; `n_no_headroom` is 1 everywhere, `n_censored` is 1 on the s2 rows.

## Other aggregates in the file

Read straight off the records: `completion` 0 or 1 per task, `preempt_count` per task and summed on `lane`, `utilisation` = `busy / T_end` (0.70, 0.75, 0.72, 0.71, 0.69) and `idle`, the provenance time and count shares of `config_interval` (the `fixed` runs: `fallback_share` 1; the others: a zero-length `fallback` entry, so `time_share_fallback` 0 and `count_share_fallback` 0.5), and the config-age distribution over interval lengths. No `switch_window` rows, so no switch aggregate.

## Seam case (`seam/`)

`mock-p1a`'s records from the records writer (condition `llm_vocab`, table prior) scored against hand-written `fixed` and `oracle` records for the same reduced workload, under a two-term spec (editor wake P99 over [50000, 120000], weight 1.0; hog progress, weight 0.5).

| run | editor waits in window | P99 | hog `cpu_delivered` / 90000 |
|---|---|---|---|
| `fixed` (hand) | 4000, 8000 | 4000 + 0.99 · 4000 = 7960 | 60000 → 0.666667 |
| `oracle` (hand) | 500, 1000 | 995 | 50000 → 0.555556 |
| `llm_vocab` (writer) | 1500, 3000 | 2985 | 65000 → 0.722222 |

P99: `improvement(oracle)` 6965, `llm_vocab` 4975 → share **0.714286**. Progress: `improvement(oracle)` = 0.555556 − 0.666667 = −0.111111 (the oracle row caps the hog), `llm_vocab` +0.055556 → share **−0.5**. Score = 0.714286 − 0.25 = **0.464286**. The −0.5 is exact only because the aggregates file carries twelve places; at six it read −0.499995, which is why the precision is twelve.
