# The scorer's sign rule (11.1)

The record of sub-task 11.1 (`_dev/docs/spec/jioh/task-11.1-the-scorers-sign-rule.md`). The paths in the files are relative to the repository root; each script runs from there.

| file | what it holds |
|---|---|
| `post_hoc.py` | decisions 4 and 5: the RQ0 run's aggregates (`runs/rq0-gate/aggregates.csv`) re-scored on the scoring spec the runner built for the run, its variant and generated files' entries included; the RQ0 gate spec evaluated on those scores with the run's own guards and grades, labelled post hoc. Writes `runs/rq0-gate/post-hoc/` — `scores.csv`, `report.json`, `report.md` — and `post-hoc.json` |
| `post-hoc.json`, `post-hoc.log` | the counts, the met files, the hashes of the three outputs and the two stages' times; the script's output |
| `scores_check.py`, `scores-check.json` | decision 1: the post hoc scores against the run's, row by row — every row that reads no oracle worse than fixed equal to the run's in every column |

**The reading** (2026-11-18): 741,057,971 aggregate rows into 182,784 term rows and 126,888 file rows, 1,912 s; the report 2,049 s. 58,140 term rows are marked oracle worse than fixed. At the primary 4 of 19 judging files meet g — `c2-p2a`, `c2-p2b`, `c7-browsing`, `c7-office` — and 12 of 19 have headroom. The report is copied into `harness/experiments/rq0-gate/post-hoc/`, `report.json` gzipped (`-9 -n`).

**The check**: the same 309,672 rows in both files, the post hoc file adding `oracle_worse` and `n_oracle_worse`; the 197,574 unmarked rows unchanged, the 112,098 marked rows — 58,140 term and 53,958 file — each changed.
