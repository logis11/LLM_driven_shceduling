# mock-grades — worked derivation

The Layer-1 grader's fixture (8.4). Not a trace pair: `workloads/` holds five hand-written compiled workloads carrying only `ground_truth` and a placeholder event, `logs/` twenty-one hand-written recognition logs, and `driver-table.yaml` a miniature calibrated driver table. `expected-records/` holds the recognition records rows the grader must produce for each of the twenty graded runs, and `expected-grades.csv` the pooled `grades` file. All times µs.

**Which numbers are hand-derived and which are not.** Every count, accuracy, recall, confusion cell, balanced accuracy, Matthews coefficient and configuration rate below was worked by hand from the tables in this file, and the tests assert them individually. The bootstrap interval bounds in `expected-grades.csv` are **not** hand-derived: they are the output of the seeded sampler at seed 20260911 and 500 repetitions, pinned so a rerun compares byte for byte. The sampler itself is checked separately against an exhaustive enumeration of all 3³ = 27 equally likely draws of the three files in the headline set.

## Ground truth

| workload | segment | mode | `background_wanted` | annotations |
|---|---|---|---|---|
| `g-alpha` | [0, 60 s) | `dev` | true | — |
| `g-alpha` | [60 s, 180 s) | `ml-train` | true | — |
| `g-beta` | [0, 60 s) | `media` | true | `familiarity: 5` |
| `g-gamma` | [0, 60 s) | `ml-train` | false | `pre_committed_miss: true` |
| `g-delta` | [0, 60 s) | `ambiguous` | — | `dual_active` |
| `g-epsilon` | [0, 60 s) | `indexing` | false | — |

## Query points

Every log carries one query per pinned set change plus a terminal snapshot at the file's end. Segments are half-open, so the terminal query has no covering segment and is skipped. `g-delta`'s only segment is `ambiguous`, so its one real query is skipped too and the file contributes nothing.

| workload | graded query points |
|---|---|
| `g-alpha` | 2, at 0 and 60 000 000 |
| `g-beta` | 1, at 0 |
| `g-gamma` | 1, at 0 |
| `g-epsilon` | 1, at 0 |
| `g-delta` | 0 |

**Five graded points over four files.** Dropping `g-gamma`, the pre-committed miss, leaves the headline set: **four points over three files**.

## The driver table

Eight rows, `role: calibrated`. The composed configuration is `{algorithm, params, batch_bandwidth_cap}` built from the row's `default` entry, canonical JSON, byte-identical with the daemon's own `compose`.

| row | cap | default | composed configuration |
|---|---|---|---|
| `dev` / true | 0.5 | MLFQ | A |
| `ml-train` / true | 0.333 | LOTTERY | B |
| `media` / true | 0.5 | EDF | C |
| `gaming` / true | 0.5 | EDF | C |
| `ml-train` / false | 0.05 | MLFQ | D |
| `office` / false | 0.05 | MLFQ | D |
| `backup` / false | 0.05 | MLFQ | D |
| `indexing` / false | 0.05 | MLFQ | D |

The four `false` rows compose to the **same** configuration D, and `media`/true and `gaming`/true both compose to C. That is deliberate: it makes a wrong mode that changes nothing the scheduler does, which is what the configuration-distance line counts.

## The answers

`mode` / `wanted`, with the algorithm named only under `llm_algo`. A dash means the proposal is `null`, an unparseable answer, so `validation` is `held`, both correctness metrics are 0, and `predicted` is empty.

| point | truth | `oracle` | `random` s1 | `random` s2 | `llm_vocab` | `llm_algo` |
|---|---|---|---|---|---|---|
| `g-alpha` @ 0 | `dev`/true | `dev`/true | `backup`/false | `dev`/true | `dev`/true | `dev`/true, MLFQ |
| `g-alpha` @ 60 s | `ml-train`/true | `ml-train`/true | `media`/true | `ml-train`/true | `ml-train`/true | `ml-train`/true, LOTTERY |
| `g-beta` @ 0 | `media`/true | `media`/true | `media`/true | `gaming`/true | — | `media`/true, MLFQ |
| `g-gamma` @ 0 | `ml-train`/false | `ml-train`/false | `office`/false | `backup`/false | `ml-train`/true | `ml-train`/true, MLFQ |
| `g-epsilon` @ 0 | `indexing`/false | `indexing`/false | `gaming`/true | `indexing`/false | `indexing`/false | `indexing`/false, MLFQ |

## Per-point outcomes

`m` is `mode_correct`, `a` is `attr_correct`, `c` is `config_correct`, comparing the composed configuration of the predicted row against the true row's.

| point | `oracle` m/a/c | `random` s1 m/a/c | `random` s2 m/a/c | `llm_vocab` m/a/c | `llm_algo` m/a/c |
|---|---|---|---|---|---|
| `g-alpha` @ 0 | 1/1/1 | 0/0/0 (A vs D) | 1/1/1 | 1/1/1 | 1/1/1 |
| `g-alpha` @ 60 s | 1/1/1 | 0/1/0 (B vs C) | 1/1/1 | 1/1/1 | 1/1/1 |
| `g-beta` @ 0 | 1/1/1 | 1/1/1 | 0/1/**1** (C vs C) | 0/0/0 (null) | 1/1/1 |
| `g-gamma` @ 0 | 1/1/1 | 0/1/**1** (D vs D) | 0/1/**1** (D vs D) | 1/0/0 (D vs B) | 1/0/0 (D vs B) |
| `g-epsilon` @ 0 | 1/1/1 | 0/0/0 (D vs C) | 1/1/1 | 1/1/1 | 1/1/1 |

`random` at `g-gamma` is the case the fixture exists to show: it names `office` where the truth is `ml-train`, a mode error, and the two rows compose to the same configuration, so the scheduler ran exactly as it should have.

`algo_choice_correct` under `llm_algo`, graded against the calibrated default of the **true** row: MLFQ against MLFQ at `g-alpha` @ 0, LOTTERY against LOTTERY at `g-alpha` @ 60 s, **MLFQ against EDF at `g-beta`, wrong**, MLFQ against MLFQ at `g-gamma` and `g-epsilon`. Four of five.

## The headline set — four points, three files

Truth on the attribute axis: `dev`/true, `ml-train`/true, `media`/true, `indexing`/false, so **three true against one false**. Truth on the mode axis: four distinct modes, one point each.

| condition | mode raw | attribute raw | true recall | false recall | balanced | Matthews (n) | config rate |
|---|---|---|---|---|---|---|---|
| `oracle` | 4/4 = 1.000000 | 4/4 = 1.000000 | 3/3 | 1/1 | 1.000000 | 1.000000 (4) | 4/4 = 1.000000 |
| `llm_algo` | 4/4 = 1.000000 | 4/4 = 1.000000 | 3/3 | 1/1 | 1.000000 | 1.000000 (4) | 4/4 = 1.000000 |
| `llm_vocab` | 3/4 = 0.750000 | 3/4 = 0.750000 | 2/3 | 1/1 | 0.833333 | 1.000000 (3) | 3/4 = 0.750000 |
| `random` s1 | 1/4 = 0.250000 | 2/4 = 0.500000 | 2/3 | 0/1 | 0.333333 | −0.333333 (4) | 1/4 = 0.250000 |
| `random` s2 | 3/4 = 0.750000 | 4/4 = 1.000000 | 3/3 | 1/1 | 1.000000 | 1.000000 (4) | 4/4 = 1.000000 |
| `random` mean | 0.500000 | 0.750000 | — | — | **0.666667** | 0.333333 (4) | 0.625000 |

**Majority baselines**, measured on this set: attribute 3/4 = 0.750000, mode 1/4 = 0.250000.

**Balanced accuracy** is the mean of the two recalls. For `llm_vocab`, (2/3 + 1)/2 = 5/6 = 0.833333. For `random`, (2/3 + 0)/2 = 1/3 = 0.333333.

**The Matthews coefficient** is computed only over points whose prediction names one of the two classes, so its count differs from the others'. `llm_vocab`'s `g-beta` proposal is `null` and has no cell in the two-by-two, leaving n = 3 with TP 2, FN 0, TN 1, FP 0, so the coefficient is exactly 1 while balanced accuracy is 0.833333 — the null still costs recall. For `random`, TP 2, FN 1, TN 0, FP 1 gives (2·0 − 1·1)/√(3·3·1·1) = −1/3.

**Per-class recall on the mode axis**, `llm_vocab`: `dev` 1/1, `ml-train` 1/1, `media` 0/1, `indexing` 1/1.

**Confusion cells on the mode axis**, `random`: (`dev`, `backup`) 1, (`ml-train`, `media`) 1, (`media`, `media`) 1, (`indexing`, `gaming`) 1. Under `llm_vocab` the null answer gets its own cell, (`media`, empty) 1, rather than being folded into a real class.

## The full set — five points, four files

| condition | mode raw | attribute raw | errors | of them, changing the configuration |
|---|---|---|---|---|
| `oracle` | 5/5 = 1.000000 | 5/5 = 1.000000 | 0 | — |
| `llm_algo` | 5/5 = 1.000000 | 4/5 = 0.800000 | 1 | 1/1 = 1.000000 |
| `llm_vocab` | 4/5 = 0.800000 | 3/5 = 0.600000 | 2 | 2/2 = 1.000000 |
| `random` s1 | 1/5 = 0.200000 | 3/5 = 0.600000 | 4 | **3/4 = 0.750000** |
| `random` s2 | 3/5 = 0.600000 | 5/5 = 1.000000 | 2 | 0/2 = 0.000000 |
| `random` mean | 0.400000 | 0.800000 | — | 0.375000 |

`random` s2's last cell is the sharpest version of the point: both of its errors named a different mode that composed to the same configuration, so none of them reached the scheduler at all. `random` s1's last cell is the point of the whole line. It answered four of five points wrongly, but one of those four produced the right configuration anyway, so only three of its errors reached the scheduler. `algo_choice_correct` under `llm_algo` is 4/5 = 0.800000.

## Intervals

At three files in the headline set the bootstrap has three clusters, so most intervals span nearly the whole range. That is the honest result and not a defect of the fixture: it is what three independent units buy. The exhaustive enumeration test uses `llm_vocab`'s mode accuracy, whose 27 draws run from 0, when all three draws take `g-beta` and its single wrong point, to 1, when all three take `g-alpha` and its two right ones.

## Seeds

`random` runs twice over the same questions, so the seed-averaging path is exercised. A seed is a repetition, not a new question, so each statistic is computed per seed and then averaged; both readings are in the file, told apart by `over_seeds`.

On the headline set of four points over three files:

| statistic | seed s1 | seed s2 | mean, `over_seeds` = 1 |
|---|---|---|---|
| mode raw accuracy | 1/4 = 0.250000 | 3/4 = 0.750000 | 0.500000 |
| attribute raw accuracy | 2/4 = 0.500000 | 4/4 = 1.000000 | 0.750000 |
| attribute balanced accuracy | 1/3 = 0.333333 | 1.000000 | **0.666667** |
| configuration correct rate | 1/4 = 0.250000 | 4/4 = 1.000000 | 0.625000 |

On the full five-point set: mode (1/5 + 3/5)/2 = 2/5 = 0.400000, attribute (3/5 + 5/5)/2 = 4/5 = 0.800000.

**The count on a mean row.** For statistics whose denominator is the graded point count, every seed agrees and `n` is that shared count. `errors_changing_config` is the exception: its denominator is itself a result, and the two seeds made three errors and one. The mean row then carries the **largest** per-seed count, so the column never understates the evidence behind any seed, and the per-seed rows carry their own.

Two things the balanced-accuracy row shows. The mean is taken on the exact fractions and rounded once at the end: averaging the two *written* values, 0.333333 and 1.000000, would give 0.666666 instead. And `n` on the mean row stays 4, the per-seed count, not 8 — four graded points measured twice are still four points.

Seed s2 also adds two more wrong-mode-same-configuration cases: at `g-beta` it names `gaming` where the truth is `media`, and both compose to configuration C; at `g-gamma` it names `backup` where the truth is `ml-train`/false, and both compose to D.
