# mock-guards — worked derivation

The guards' fixture (8.3): a schedule that mixes all four provenances, a recognition log whose `validation` sequence mirrors it, ground-truth segments for the staleness check, and a trace shaped so that two run-level guards fail by design (config age, starvation floor) while the rest pass. Condition `llm_vocab` on the prior table. Scheduler: the boot MLFQ governs nothing (no task runs before 600); entry 1 stamps FIFO at 600 and every later entry keeps FIFO, so the lane runs first-come-first-served with no preemption. All times µs.

## Run file

| task | name | arrive | depart | program | RUN total |
|---|---|---|---|---|---|
| `editor` | `code` | 0 | 3000000 | WAIT, RUN 4000, WAIT, RUN 4000, WAIT | 8000 |
| `hog` | `python3` | 50000 | — | RUN 2000000, EXIT | 2000000 |
| `batch` | `make` | 100000 | — | RUN 500000, EXIT | 500000 |

Keystrokes on `input:editor`: 2600000, 2700000. `T_end` = 3000000.

## Ground truth (`workload.json`)

| segment | mode | interval |
|---|---|---|
| 0 | dev | [0, 50000) |
| 1 | ml-train | [50000, 80000) |
| 2 | build | [80000, 3000000) |

Segment 2 starts at 80000 without a set change: the user's activity changes before the next launch does. Query 2's answer therefore governs segment 2 from 100600, and query 1's late answer is what the staleness guard catches.

## Set changes, queries, schedule

The daemon queries at every pinned set change: 0 (`code`), 50000 (`python3`), 100000 (`make`), 3000000 (`code` departs, the terminal snapshot). One schedule entry per query, stamped at `t_set_change` + latency, after the boot entry.

| index | query | `t_set_change` | latency | `t_us` | provenance | note |
|---|---|---|---|---|---|---|
| 0 | — | — | — | 0 | `fallback` | boot, MLFQ (OSTEP example) |
| 1 | 0 | 0 | 600 | 600 | `unmodified` | FIFO |
| 2 | 1 | 50000 | 40000 | 90000 | `held` | the answer could not be parsed (`proposal: null`, `raw` kept); FIFO carried forward |
| 3 | 2 | 100000 | 600 | 100600 | `clamped` | the cap pulled to 0.5 |
| 4 | 3 | 3000000 | 600 | 3000600 | `unmodified` | at or after the end: the simulator applies nothing, no `config_applied` line |

`recognition-log-mismatch.json` is the same log with query 1's `validation` written `unmodified` where the schedule says `held`.

## What happens

| t | event |
|---|---|
| 0 | boot config (index 0). `editor` arrives, reaches WAIT, blocks (zero-length occupancy). |
| 600 | entry 1 applies: MLFQ → FIFO, a switch with nobody runnable (`switch_window` value 0, no hogs). |
| 50000 | `hog` arrives; lane free; runs. |
| 90000 | entry 2 (`held`) applies: FIFO stays FIFO. |
| 100000 | `batch` arrives, ready; `hog` holds the lane under FIFO. |
| 100600 | entry 3 (`clamped`) applies: FIFO stays FIFO. The cap is not modelled by the mock. |
| 2050000 | `hog` exits; `batch` runs (waited 1950000). |
| 2550000 | `batch` exits. |
| 2600000 | keystroke 1; lane free; RUN 4000; blocks at 2604000. |
| 2700000 | keystroke 2; RUN 4000; blocks at 2704000. |
| 3000000 | `T_end`. `editor` departs. |

## Records (25 rows)

**`ready_wait`**: `editor` 0/arrive → 0; `hog` 50000/arrive → 0; `batch` 100000/arrive → `run_start` 2050000 → **1950000**; `editor` 2600000/wake → 0; `editor` 2700000/wake → 0.

**Lifetime**: `editor` [0,0] [2600000,2604000] [2700000,2704000] → `cpu_delivered` 8000, `demand` 8000, `completed` 0 (depart), `preempt_count` 0. `hog` [50000,2050000] → 2000000 / 2000000, `completed` 1 at 2050000, `turnaround` 2000000. `batch` [2050000,2550000] → 500000 / 500000, `completed` 1 at 2550000, `turnaround` 2450000. No preemptions under FIFO.

**`config_interval`**: 0 → 600 (`fallback`, 600); 600 → 90000 (`unmodified`, 89400); 90000 → 100600 (`held`, 10600); 100600 → 3000000 (`clamped`, 2899400). Entry 4 has no line.

**`switch_window`**: index 1 at 600, into FIFO, value 0, hogs 0.

**`busy`**: 8000 + 2000000 + 500000 = 2508000.

## Guards (`expected-guards.csv`)

| guard | value | threshold | result | why |
|---|---|---|---|---|
| `provenance_share` | 11200 / 3000000 = 0.003733333333 | 0.5 | pass | `fallback` 600 + `held` 10600, time-weighted |
| `config_age` | 40000 (the largest age: entries 1–3 aged 600, 40000, 600; entry 4 skipped, no covering segment) | — | **fail** | entry 2 stamped at 90000, after segment 1 ended at 80000 |
| `starvation_floor` | 1950000 (`batch`) | 1000000 | **fail** | the lane never yielded to `batch` under FIFO for 1.95 s |
| `determinism` | — (partner: the trace's SHA-256) | — | pass | the rerun is the same file in the test |
| `utilisation_sanity` | 2508000 / 3000000 = 0.836 | 1.0 | pass | |
| `tick_count` | 0 messages | — | pass | no chains; two wake lines for two wake events; config lines match the schedule |
| `validation_matches_provenance` | 0 mismatches | — | pass | `[unmodified, held, clamped, unmodified]` both sides; the mismatch log fails at index 1 |
| `c2_pair` | — | — | not_applicable | not a C2 file |
