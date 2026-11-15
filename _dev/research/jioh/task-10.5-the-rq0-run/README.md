# The RQ0 run (10.5)

The record of sub-task 10.5 (`_dev/docs/spec/jioh/task-10.5-the-rq0-run.md`). The paths in the files are relative to the repository root; each script runs from there.

## Before the run

| file | what it holds |
|---|---|
| `rq0_run.py` | decisions 2, 4, 7, 8, 10, 11: the launcher — `start`, `resume`, `open`. It writes the record folder `run/`: `starts.jsonl`, `stops.jsonl`, `flags.jsonl`, `opens.jsonl`; the run's log is `runs/rq0-gate.log`, the runner's verdict line and exit code `runs/rq0-gate.sealed/` |
| `blind_reading.py` | decisions 4–5: the guard table on the runs the criterion reads, the longest-wait line's reopen condition, `simulator/tools/wait_check.py` on every trace; writes `run/blind-reading.json` and `run/waits.csv` |
| `hash_manifest.py` | decision 13: every run's trace hash and records hash, uncompressed, to `harness/experiments/rq0-gate/runs.sha256.csv` |
| `resume_check.py`, `resume-check.json` | decision 9: the integration gate's short run (seven files, 28 runs, the real programs) through the launcher, once uninterrupted and once killed and resumed, each on an empty cache |

**The resume** (2026-11-15, on `d730a0ac`): SIGKILL to the launcher and the runner's process group at 10 of 28 runs, no stop written, two stray temporary entries left in the cache; the resume served those 10 runs' records from the results cache and built the other 18. The six experiment files (aggregates, scores, guards, grades, report JSON and Markdown) and the 168 run files (records, trace, rerun-trace hash, schedule, log, records messages) are identical byte for byte to the uninterrupted pass's. Uninterrupted 130 s; 58 s to the kill and 113 s resumed. The launcher recorded the missing stop at the resume and sealed the report at the end of both passes.

**The launcher's refusals and its stop**, on the same short run: a `start` over a start on record, over an existing experiment directory, a `resume` under another spec hash, an `open` with no blind reading — each refused; with the simulator's command replaced by one that exits 1, the runner was stopped at the first failed run and the stop and the flag recorded.

**The blind reading on the second smoke rerun** (`runs/smoke-rerun-2`, 1,197 runs, 76 of them runs the criterion reads): clear — no invalidating failure, no run past the reopen point, no unread wait past 15 s on the criterion's runs. Outside them, the 10.4 record's readings run for run: nine unread waits past 15 s, 14 `starvation_floor` failures, the eight exempt `c2_pair` rows and the exempt `provenance_share` row; and two `tick_count` failures, `c4-compile`'s `random-1` and `random-2`. The wait check took 226 s with 6 workers.

**The hash manifest on two smoke passes** (`runs/cold-smoke`, `runs/smoke-rerun-2`): the two manifests are identical, 1,197 lines; 16 s and 21 s with 6 workers.

**The slow-run flag's multiple**, 6: the largest ratio between one run's slowest and fastest time over the three smoke passes that built it — the second cold smoke, the rerun and the second rerun (the 10.4 record's three `run-times.csv`) — is 6.0. A run is flagged past 6 times its file's slowest run in the second cold smoke. The first cold smoke's two runs in the boost-window scan were 88 and 76 times their file's `fixed` run.
