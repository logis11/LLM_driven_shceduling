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

**The slow-run flag's multiple**, 6: the largest ratio between one run's slowest and fastest time over the three smoke passes that built it — the second cold smoke, the rerun and the second rerun (the 10.4 record's three `run-times.csv`) — is 6.0. A run is flagged past 6 times its file's slowest run in the second cold smoke. The first cold smoke's two runs in the boost-window scan were 88 and 82 times their file's `fixed` run (4,297 s and 4,041 s against 49 s, the 10.4 record).

## The run

| file in `run/` | what it holds |
|---|---|
| `starts.jsonl` | the one start: 2026-11-16T08:57:02+0900 on `6086e7e1`, the RQ0 gate spec `9cfad697…`, the machine configuration `d402a05e…`, `simulator@0d323c84470a`, `daemon@62c71f0d2de0`, 4 workers, 1 heavy worker, `heavy_mb` 50, 325.9 GB free, 78 % of memory free, no swap |
| `stops.jsonl` | the one stop: 2026-11-18T06:23:03+0900, finished, 19,425 runs |
| `rq0-gate.log` | the runner's progress lines, one per run |
| `run-times.csv`, `stage-times.csv` | each run's build time; each stage's seconds |
| `runner-stdout.txt`, `exit-code` | the runner's verdict line and its exit code, 2, sealed until the opening |
| `blind-reading.json`, `blind-reading.log`, `waits.csv` | the blind reading; every trace's unread waits |
| `opens.jsonl` | the opening: 2026-11-18T11:14:21+0900, the blind reading clear |

**The run** (2026-11-16 08:57 to 2026-11-18 06:23, 45 h 26 min): no failed run, no slow-run flag, no stop but the finish. The 19,425 runs 152,010 s (42 h 14 min, the last at 03:10:48); the end stages: aggregates and scores 3,657 s, guards 2,491 s, grades 3,310 s, report 2,076 s. 37,863 program invocations executed and 987 served from the execution cache; no run's records from the results cache. The transcode files' runs came last and went one at a time in the heavy pool, 34–59 s a run on average per file.

**The disk**: 325.9 GB free at the start, 71.5 GB after the end stages, 254.4 GB fewer; `runs/rq0-gate` and `runs/.cache` 229 GB (`du`, a file with several links counted once); `aggregates.csv` 73,370,157,147 bytes.

**Beside the run**: VS Code with this conversation, and Spotify, throughout; a second VS Code window from about 22:11 on 2026-11-17, swap at 2.58 GB and 38 % of memory free at 22:18 (1.86 GB and 66 % at 03:59 on 2026-11-18); AhnLab V3's `v3svc` at about 34 % of one core (22:01 on 2026-11-17); a `docker-sandbox daemon` from about 12:00 on 2026-11-17, started by no command of 인지오's, near zero CPU. The three `uv run python -m app --mode stub` servers of 2026-11-15 were stopped before the start.

**The blind reading** (06:23 to 06:58, the wait check 2,110 s with 6 workers): clear. On the 1,938 runs the criterion reads, no invalidating guard failure, no run past the reopen point, no unread wait past 15 s. Outside them:

- 110 `starvation_floor` failures: 4 on judging files' `fixed` runs under `ostep-slice-100000us` (`c1-ml-train`, `c1-transcode`, `c7-ml-train`, `c7-transcode`); 105 on `c2-p2a@chain-x1.2`, `c2-p2a@chain-x1.4`, `c2-p2b@chain-x1.2`, `c2-p2b@chain-x1.4` and `c3-evening`, 20 `random` seeds and the `oracle` run each; 1 on `c3-creation`'s `fixed` run under `ostep-slice-100000us`.
- 101 `tick_count` failures: `c4-compile`, 44 `random` seeds; `c6-dual`, 57.
- The exempt rows: 8 `c2_pair` on the cap band's `oracle` runs of the C2 pairs, 1 `provenance_share` on `c6-dual`'s `oracle` run.
- 225 unread waits past 15 s: 98 after a preemption, on `c6-dual`'s runs (16.0–22.7 s); 127 open at the end — 104 on the chain variants of `c2-p2a`, `c2-p2b` and `c7-gaming` (26.4 s each), 21 on `c3-evening` (240.0 s each), and `c2-p1a`'s (38.7 s) and `c7-ml-train`'s (205.0 s) `fixed` runs under `ostep-slice-100000us`.

**The opening** (11:14:21): `verdict: fail — 6 of 19 judging files met the criterion (K = 10)`, exit code 2.

**The hash manifest** (115 s with 6 workers): 19,425 lines, 3,313,119 bytes. **The report's copy**: `report.json.gz` 1,863,420 bytes (`gzip -9 -n`), its uncompressed bytes' SHA-256 `309a13b4…70206`, the run's `report.json`'s; `report.md` 16,717,008 bytes, SHA-256 `4a7ba21b…b59ee`.
