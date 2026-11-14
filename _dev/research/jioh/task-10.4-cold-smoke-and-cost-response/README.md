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

## The smoke and after

| file | what it holds |
|---|---|
| `cold_smoke.sh` | decisions 9–10: the launcher — refuses to start over an existing `runs/cold-smoke` or `runs/.cache`, writes `start.json` (date, commit, versions, workers, free space), runs `harness/tools/run.py` on `harness/experiments/rq0-gate.yaml` with `--seed-count 2 --experiment cold-smoke`, writes `exit.json` |
| `project.py`, `projection.json` | decisions 12–13: the upper and the mean projection of the full run's wall time and disk from `runs/cold-smoke/run-times.csv` and `stage-times.csv`, and whether the cost is carried |
| `starvation.py`, `starvation.json` | decisions 16–17: the guard table of every condition on the judging files, `simulator/tools/wait_check.py` on every trace, the `starvation_floor` failures beside the five named `oracle` runs; and the 10.3 spec's decision 8 (`_dev/docs/spec/jioh/task-10.3-variant-lines-read-a-failed-guard.md`): every reporting line's availability in the smoke's report, the two chain-scale lines expected unavailable on the four chain-scaled `oracle` runs and no other |
