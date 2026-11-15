# The cold smoke and the cost response (10.4)

The record of sub-task 10.4 (`_dev/docs/spec/jioh/task-10.4-cold-smoke-and-cost-response.md`). The paths in the files are relative to the repository root; each script runs from there.

## Before the smoke

| file | what it holds |
|---|---|
| `rebuild_check.py`, `rebuild-check.json`, `rebuild-check.log` | decision 3: the integration gate's 28 short-run runs (`runs/integration-gate/smoke/`), each run's records rebuilt from its trace with the harness as it stands — the drop count by bisection, the schema check by signature, the rows' memory (decisions 1–2) — and compared byte for byte with the records on disk, records and records messages, with both hashes. 28 of 28 identical; `c1-compile`'s four runs, 168,698–170,852 `wake_drop` lines, 6.6–6.8 s each where the records took about 12 minutes, `random-1` 59 s |
| `storage_check.py`, `storage-check.json` | decision 4's invariant: `harness/tools/smoke.py` through the real programs over the short run's seven files (`c1-office`, `c1-photo`, `c7-mail`, `c2-p2b`, `c1-gaming`, `c7-compile`, `c1-compile`; 28 runs), once from the commit before the changes (`7e852a8d`), once with them. The aggregates, scores, guards, grades and report identical; each run's records, schedule, log, records messages and trace identical once unpacked, the rerun trace's hash equal to the old rerun trace's. The run directories 1,468 MB before, 53 MB after |
| `calibrate.py`, `calibration.json`, `calibration.log` | decision 7: one `fixed` run of each heavy family and of the largest light files, one after another, each in a fresh process, wall time, peak memory (physical footprint) and bytes as the runner records them |

`c6-dual`'s `fixed` run, its records built from the trace with the changes of decision 2 (14,031,957 rows): build 213 s, write 110 s, aggregates 124 s, peak 9.4 GB. Before them the build ran past 15 GB and swapped on the 16 GB home machine, about 40 minutes a run (9.14 D13–D14).

### The calibration and the worker configuration (decision 7)

One `fixed` run each, one after another, nothing else running (`calibration.json`, 2026-11-14):

| file | workload file, MB | wall, s | peak memory, MB | run directory, MB |
|---|---|---|---|---|
| `c6-dual` | 178.9 | 588.2 | 9,593 | 347.3 |
| `c1-transcode` | 145.6 | 49.4 | 2,209 | 28.5 |
| `c7-transcode` | 90.3 | 30.3 | 1,466 | 18.1 |
| `c4-compile` | 30.1 | 26.7 | 672 | 45.1 |
| `c1-compile` | 28.7 | 26.4 | 647 | 44.9 |
| `c3-workday` | 18.3 | 25.1 | 566 | 44.1 |
| `c1-ml-train` | 23.1 | 8.9 | 445 | 5.3 |
| `c7-ml-train` | 19.9 | 7.7 | 396 | 4.6 |

`harness/runner.yaml` on the home machine (16,384 MB, 8 performance cores and 2 efficiency cores), for the smoke and the full run:

- `heavy_mb: 50` — the seven files of 90.3 MB and over (`c6-dual`, `c1-transcode` and `c7-transcode` with their two venue variants each; peaks 1,466–9,593 MB) are the heavy runs; the largest file under it is `c4-compile`, 30.1 MB, 672 MB.
- `heavy_workers: 1` — two `c6-dual` runs at once are 19,186 MB.
- `workers: 4` — the peaks at once are at most 9,593 + 4 × 672 = 12,281 MB; with the 2,370 MB the kernel held wired with no run going (`vm_stat`, 144,689 pages of 16 KB) that is 14,651 MB of the 16,384.

## The first smoke

Started 2026-11-14T13:04:18+0900 on `a0ed61ad`, `simulator@0d323c84470a`, `daemon@62c71f0d2de0`, workers 4 / 1 / 50, 324.2 GB free; stopped 18:22:00 (exit 143) at 1,151 of the 1,197 runs, 998 finished and 153 failed. `first-smoke/` holds its `start.json`, `exit.json` and log.

- **The failed runs** (decision 11): every run under an alternative driver table — the 17 judging files' `oracle`, `random-1` and `random-2` under each of `floor-0.2`, `floor-0.333` and `floor-0.5` — at the records' schema check, `table: 'prior@floor-0.2' is not one of ['prior', 'calibrated']`. The runner labels such a run `<role>@<stem>`, as the experiment-spec schema's `driver_table_alternatives` states; the five row schemas took the role alone. Fixed on the harness side (`df0b9348`, the harness changelog's entry of 2026-11-14).
- **The slow runs** (decision 14, ahead of the projection): `c1-transcode/random-1~focus` 4,297 s and `c1-transcode@venue-x1.25/random-1~focus` 4,041 s, where the file's `fixed` run took 49 s, `random-2` of the venue variant 53 s. Their aggregates' per-switch excess scanned every boost window of the MLFQ interval for each interactive latency point, twice — 1,014,792 `app_latency` points against 47,599 boost windows in the first, 2.6 ms a point. Replaced by a lookup over the windows sorted once.

| file | what it holds |
|---|---|
| `first-smoke/` | the first smoke's `start.json`, `exit.json` and `cold-smoke.log` |
| `excess_check.py`, `excess-check.json`, `excess-check.log` | the first smoke's 39 runs whose cached aggregates carry a per-switch excess (61 rows), each run's results built again from its trace with the lookup — records, records messages, aggregates and graded queries — and compared exactly with the ones cached before it. 39 of 39 identical; `c1-transcode/random-1` 42.6 s, the two `c6-dual` `random` runs 714 s and 616 s |

## The second smoke

Started 2026-11-14T18:54:22+0900 on `a3aadfe9`, the same versions and workers, 319.6 GB free. The 1,197 runs finished at 22:20:57, none failed. The end stages: `aggregates.csv` written 22:24 (47,089,102 rows, 4.65 GB), `scores.csv` 22:30, then the guards; stopped 2026-11-15T07:52:30 (exit 143) inside the guards, 9 h 22 min after they began, before `guards.csv`. `second-smoke/` holds its `start.json`, `exit.json`, log and `run-times.csv` (every run's wall time, peak memory and bytes).

- **The guards stage**, `tools/harness/guards.py` `evaluate`: for each run, its aggregates are the rows of the whole experiment whose identity matches, read by a pass over all 47,089,102 rows — 0.55 s a million rows in memory, about 26 s a run and 8.6 h for the 1,197. The runner held every run's aggregates as Python dicts: footprint 26 GB on the 16 GB machine, 10.9 GB of swap in use, the runner at 48 % CPU.
- **The rows**: `ready_wait`'s seven aggregates per entity (count, max, mean, over_threshold, p50, p95, p99) are 39.9 million of the 47.1 million; `c1-compile`'s runs 10.5 million, a `c6-dual` run 457,000, the median run 103. Of the seven, `max` alone is read after the aggregates are written — by `starvation_floor` and by the evaluator's longest-wait line; no scoring term reads `ready_wait`.
- **At the full run's 19,425 runs**, each run's rows as its smoke counterpart's (seed 1 for a drawing run): 740,818,977 aggregate rows, about 73 GB as CSV; `ready_wait` 627,173,344 of them, its `max` 89,596,192.
- **The end stages a run at a time** (decision 14, ahead of the projection; the harness changelog's entry of 2026-11-15): no stage holds the experiment's aggregates whole. The rows are kept as they are.

| file | what it holds |
|---|---|
| `second-smoke/` | the second smoke's `start.json`, `exit.json`, `cold-smoke.log` and `run-times.csv` |
| `end_stage_check.py`, `end-stage-check.json`, `end-stage-check.log` | the runner before the change (`a3aadfe9`'s harness tree) and after, through the real programs on the integration gate's short run's seven files, the smoke spec with the cap band's `floor-0.2` table and the input wake count, longest wait and flip cost lines added — 49 runs, 21 under `floor-0.2`: aggregates (471 MB), scores, guards, grades, report JSON and Markdown identical; old 399 s, new 186 s, the second's programs from the shared execution cache |

## The smoke rerun

Started 2026-11-15T08:28:04+0900 on `5c434017`, the same versions and workers, 299.8 GB free, its traces served from the execution cache the second smoke left: 2,394 program invocations from the cache, none executed; every run's records and aggregates built again. The 1,197 runs finished at 11:19:12 (10,268 s), none failed. The end stages, 577 s: aggregates and scores 224 s, guards 93 s, grades 132 s, report 128 s. Ended 11:29:17, exit 2 — the runner's code for a finished experiment whose verdict is not pass.

- `aggregates.csv` (4,652,470,598 bytes) and `scores.csv` (SHA-256 `d592f4a2…83b95`) identical byte for byte to the second smoke's; `guards-manifest.json` identical but for the experiment's name.
- Run-seconds 15,416 against the second smoke's 19,037: `c6-dual`'s 14 runs 457–977 s against 508–983 s, the transcode files' 62 runs 0.79 of their second-smoke time, the 68 other runs over 20 s 0.88.

| file | what it holds |
|---|---|
| `rerun/` | the rerun's `start.json`, `exit.json`, `smoke-rerun.log`, `run-times.csv` and `stage-times.csv` |

## The projection

`project.py --smoke runs/cold-smoke --stages runs/smoke-rerun --free-gb 319.6` (`projection.json`): the second smoke's run times and bytes, the rerun's end stages scaled from 1,197 runs to 19,425; the free space measured at the second smoke's start.

| | wall, h | light pool, h | heavy pool, h | end stages, h | runs, GB | experiment files, GB | disk, GB |
|---|---|---|---|---|---|---|---|
| upper | 50.33 | 13.29 | 47.73 | 2.60 | 200.1 | 73.4 | 273.5 |
| mean | 38.75 | 8.23 | 36.15 | 2.60 | 170.3 | 73.4 | 243.7 |

The cost is carried (decision 13): 50.33 h of the 80, 273.5 GB of the 319.6. The largest file's share of the upper projection: `c6-dual`, 30.59 h over its 112 runs, then `c1-compile`, 13.36 h over 415.

A run's bytes, as the runner records them, are its run directory and its execution-cache and results-cache entries, a file with several links counted once. The experiment's own files (decision 12 as restated 2026-11-15): the rerun's `aggregates.csv`, 4,652,470,598 bytes over 47,089,102 rows, at the full run's 740,818,977 rows — each full run's rows its smoke counterpart's, seed 1 for a drawing run — 73.2 GB; the other files, 11.4 MB over 1,197 runs, 0.19 GB at 19,425. Free on 2026-11-15 after the rerun: 286.1 GB, with `runs/.cache` (18.6 GB), `runs/cold-smoke` and `runs/smoke-rerun` (4.7 GB each) on disk.

## The starvation readings

`starvation.py --smoke runs/smoke-rerun` (`starvation.json`, `starvation.log`), on the rerun's 1,197 runs. The boot default `ostep-slice-100000us` is the config schema's upper bound on the top slice, 100 ms.

- **The guard table on the 19 judging files**: 12 failed rows.
  - `starvation_floor` under `fixed` with the 100 ms boot default, four: `c1-ml-train` (`editor`, 320.3 s), `c7-ml-train` (`editor`, 300.0 s), `c1-transcode` (`video-editor`, 168.0 s), `c7-transcode` (`video-editor`, 167.9 s).
  - `c2_pair` under `oracle` with the cap band's tables, eight: `c2-p1a` and `c2-p3a` under each of the three, their partners `c2-p1b` and `c2-p3b` not in the run set; `c2-p2a` and `c2-p2b` under `floor-0.333`, their configurations identical over [60 s, 86.385 s).
- **The wait check**: nine waits the guard cannot read past 15 s.
  - On judging files, under the 100 ms boot default: `c2-p1a`'s `editor` still ready at the end after 38.7 s, `c7-ml-train`'s `editor` after 205.0 s.
  - On other files, recorded with their runs: `c3-evening/oracle`'s `chat` still ready at the end after 240.0 s; `c6-dual/random-1` and `random-2` after a preemption, 21.8 s and 16.0 s; `steam` on the two chain-scaled `c7-gaming` variants under `oracle` and `random-1`, still ready at the end after 26.4 s.
- **`starvation_floor` on every file**: 14 runs.
  - The five named `oracle` runs, all five: `c3-evening`'s `steam` 240.0 s, the four chain-scaled `c2` variants' `steam` 86.4 s.
  - Beside them: the four chain-scaled `c2` variants' `random-1` runs, `steam` 60.0 s; and under the 100 ms boot default the four judging files above and `c3-creation` (`video-editor`, 197.3 s).
- **The starvation net is reopened** (decision 17): `starvation_floor` failed on four judging files, and two unread waits on judging files are over 30 s. The longest-wait line's reopen condition (decision 16) is met by the four judging-file runs past 15 s.
- **The lines' availability** (the 10.3 spec's decision 8): 34 readings, six unavailable — not as expected.
  - The two chain-scale lines, `chain-x1.2` and `chain-x1.4`, on their files' `oracle` and `random` runs' `starvation_floor`.
  - The 100 ms boot default's sensitivity count, on the four judging files' `starvation_floor`.
  - The three cap band tables' counts, on the judging files' `c2_pair`.

## The second smoke rerun

Started 2026-11-15T12:18:04+0900 on `dd03f515`, the harness with the cost response (`251eb50f`), the same versions and workers, 285.6 GB free: 2,394 program invocations from the execution cache, none executed; no run's records from the results cache, whose key carries the harness package's own source, which `251eb50f` changed — every run's records and aggregates built again. The 1,197 runs finished in 11,671 s, none failed. The end stages, 582 s: aggregates and scores 225 s, guards 96 s, grades 133 s, report 128 s. Ended 15:42:45, exit 2.

- `aggregates.csv`, `scores.csv`, `guards.csv` and `grades.csv` identical byte for byte to the rerun's.
- Run-seconds 17,964 against the rerun's 15,416, every run's bytes the rerun's: `c6-dual`'s 14 runs 1.16 of their rerun time (494–1,033 s), the transcode files' 62 runs 1.04, the 68 other runs over 20 s 1.14, the other 1,053 runs 1.30. By completion order, each quarter of the runs 1.22, 1.22, 2.13 (100 s against 47 s) and 1.14 of its rerun time. 140 runs over their second-smoke time, 890 s over in all, the most `c6-dual`'s `fixed+ostep-slice-500us` (923.1 s against 822.9 s) and `random-1` (1,033.1 s against 983.1 s); all the runs 0.94 of the second smoke's run-seconds.
- **The projection** with these end stages (`rerun-2/projection.json`): upper 50.35 h, its end stages 2.62 h, the pools and the disk as before (273.5 GB); mean 38.77 h. Carried.
- **The starvation readings** (`rerun-2/starvation.json`, `rerun-2/starvation.log`), with `starvation.py` as the starvation net's decision session left it: the same failed guard rows, `starvation_floor` failures and unread waits as on the rerun, run for run and wait for wait. Nothing reopened: the six on judging files under the 100 ms boot default — four `starvation_floor` failures, two unread waits — are listed apart as that point's own. 34 line readings, three unavailable, as expected: the 100 ms boot default's sensitivity count and the two chain-scale lines. In the report, the eight `c2_pair` rows under the cap band's tables are exempt, and the longest-wait line, the 100 ms boot default left out, does not reopen.
- Free after: 271.5 GB, with `runs/.cache` (24.9 GB) and `runs/cold-smoke`, `runs/smoke-rerun` and `runs/smoke-rerun-2` (4.7 GB each beyond it) on disk, 38.9 GB in all.

| file | what it holds |
|---|---|
| `rerun-2/` | the second rerun's `start.json`, `exit.json`, `smoke-rerun-2.log`, `run-times.csv` and `stage-times.csv`; `projection.json` from its end stages; `starvation.json` and `starvation.log` on its runs |

## The smoke and after

| file | what it holds |
|---|---|
| `cold_smoke.sh` | decisions 9–10: the launcher — refuses to start over an existing `runs/cold-smoke` or `runs/.cache`, writes `start.json` (date, commit, versions, workers, free space), runs `harness/tools/run.py` on `harness/experiments/rq0-gate.yaml` with `--seed-count 2 --experiment cold-smoke`, writes `exit.json` |
| `rerun_smoke.sh` | decision 14: the smoke rerun, its traces from the execution cache the cold smoke left — refuses to start over an existing `runs/smoke-rerun` or without `runs/.cache`, writes `rerun/start.json` and `rerun/exit.json`, runs `harness/tools/run.py` on `harness/experiments/rq0-gate.yaml` with `--seed-count 2`; the experiment's name and the record's folder are its two arguments, `smoke-rerun` and `rerun` when left out |
| `project.py`, `projection.json` | decisions 12–13: the upper and the mean projection of the full run's wall time and disk from `runs/cold-smoke/run-times.csv` and a `stage-times.csv` — the smoke's, or with `--stages` the rerun's — the disk with the experiment's own files from the same experiment (decision 12 as restated 2026-11-15), and whether the cost is carried |
| `starvation.py`, `starvation.json` | decisions 16–17: the guard table of every condition on the judging files, `simulator/tools/wait_check.py` on every trace, the `starvation_floor` failures beside the five named `oracle` runs; and the 10.3 spec's decision 8 (`_dev/docs/spec/jioh/task-10.3-variant-lines-read-a-failed-guard.md`): every reporting line's availability in the smoke's report, the two chain-scale lines expected unavailable on the four chain-scaled `oracle` runs and no other; since the starvation net's decision session of 2026-11-15 (the 10.4 spec's decisions 16, 20 and 21), the 100 ms boot default's count and the chain-scale lines on their `oracle` and `random` runs, a judging file's failure or unread wait under `ostep-slice-100000us` listed apart from what reopens |
