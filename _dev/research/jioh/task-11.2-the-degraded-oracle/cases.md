# The degraded oracle — case table

The cases of the 11.2 spec (`_dev/docs/spec/jioh/task-11.2-the-degraded-oracle.md`, decision 2): a judging file's term on which the oracle is worse than fixed by the floor or more, under the scorer with 11.1's sign rule. *Primary* is the primary boot default (`ostep`, the 10 ms slice) under the primary table (`prior`). Values in µs, from `runs/rq0-gate/post-hoc/scores.csv`.

| # | file | term | combination | fixed | oracle | class | evidence | fixing commit |
|---|---|---|---|---|---|---|---|---|
| 1 | `c1-compile` | editor, input latency P99 | primary | 235,971,211.09 | 361,025,331.76 | property | [1](#1-c1-compile) | |
| 2 | `c1-ml-train` | hog, turnaround | primary | 1,596,272,585 | 1,599,230,869 | property | [2](#2-c1-ml-train) | |
| 3 | `c1-render` | bulk, turnaround | primary | 21,394,289 | 22,089,192 | property | [3](#3-c1-render) | |
| 4 | `c1-transcode` | batch, turnaround | primary | 3,894,612,815 | 4,134,853,844 | property | [4](#4-c1-transcode) | |
| 5 | `c2-p3a` | bulk, turnaround | primary | 22,482,188 | 23,119,499 | property | [5](#5-c2-p3a) | |
| 6 | `c7-compile` | editor, input latency P99 | primary | 58,431,291 | 87,359,931 | property | [6](#6-c7-compile) | |
| 7 | `c7-dev` | editor, input latency P99 | primary | 1,750,097.40 | 5,600,806.08 | property | [7](#7-c7-dev) | |
| 8 | `c7-ml-train` | editor, input latency P99 | primary | 7,194,480.40 | 8,020,875.92 | property | [8](#8-c7-ml-train) | |
| 9 | `c7-video-edit` | editor, app latency P99 | primary | 4,750,232.68 | 8,090,656.02 | property | [9](#9-c7-video-edit) | |
| 10 | `c1-transcode` | video-editor, app latency P99 | 12 ms boot default, `prior` | 365,038.19 | 430,531.08 | unexplained | | |
| 11 | `c2-p1a` | editor, input latency P99 | 7 ms boot default, `prior` | 7,512,775.33 | 8,227,009.39 | property | [11](#11-c2-p1a) | |
| 12 | `c2-p3a` | editor, app latency P99 | 7 ms boot default, `prior` | 38,159.57 | 42,435.19 | property | [12](#12-c2-p3a) | |
| 13 | `c7-photo` | photo-editor, app latency P99 | 30 ms boot default, `prior` | 2,968,927.88 | 2,978,927.88 | property | [13](#13-c7-photo) | |
| 14 | `c7-render` | editor, app latency P99 | 7 ms boot default, `prior` | 3,360,537.49 | 5,750,451.47 | property | [14](#14-c7-render) | |
| 15 | `c7-transcode` | video-editor, app latency P99 | primary boot default, `prior@floor-0.333` | 11,127,962 | 13,973,877 | unexplained | [15](#15-c7-transcode) | |

## 7. `c7-dev`

**Configurations.** Fixed: the boot MLFQ (three queues, 10 ms slice, doubling, 100 ms boost), no cap. Oracle: the `dev` / `background_wanted: false` row, the same MLFQ with `batch_bandwidth_cap` 0.05, applied at 0 for the whole window (`runs/rq0-gate/c7-dev/oracle~focus/schedule.json`, `log.json`). The cap is the one difference.

**Mechanism traced.** A keystroke costs VS Code about 78 ms of CPU, so under rule B1 (the batch-class memo, `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` §3: in the class from one full slice of CPU since the last voluntary block, out at the next one) the editor is in the batch class from 10 ms into each keystroke's burst. From 13.49 s the upgrade alternates runs and sleeps of microseconds; each sleep is a voluntary block, so it is out of the class. Over those stretches the cap holds the batch class — the editor's burst tail — to 0.05 while the upgrade is runnable: of the run's 1,211 parks, 1,107 are the editor's. The editor is delivered 4.18 s of CPU in the window against 5.47 s under fixed, its keystrokes queue behind their bursts, and the input latency the term reads — from the keystroke to the start of its service, the queueing counted (`docs/harness/metrics.md` §6.12) — has its median at 3,005,178 against 769,507 and its P99 at 5,600,806.08 against 1,750,097.40.

**Programs on the path** (`cap-check-c7-dev.json`, `cap_check.py`):
- The daemon: the schedule's entry is the row's algorithm, params and cap, for the ground truth's segment (`dev`, `background_wanted: false`).
- The row: `dev` is an interactive-only mode — MLFQ; unwanted background — the floor cap 0.05; boot params (`daemon/driver-table/prior.yaml`, the header's rules).
- The simulator: every park finds the parked task in the batch class by B1 and not periodic by B2, with a task not in the batch class and not idle runnable (1,211 of 1,211); no parked task runs before its unpark; the batch class's CPU while capped is 101,326 over 3,059,550, a share of 0.033, within the cap's 0.05 plus the bucket's depth of one slice (`simulator/memo/memo_261020.md` Part F).
- The harness: the 49 `input_latency` rows recomputed from the trace and the workload by §6.12 equal the run's records row for row; their P99 by the harness's percentile is 5,600,806.08, the scored value.

**Counterfactual** (recorded before the run): the oracle on `c7-dev` with the row's `batch_bandwidth_cap` moved from 0.05 to 0.95, everything else as the oracle's schedule. Predicted: the editor's input latency P99 moves down from 5,600,806.08 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c7-dev/cap-0.95/`): the editor's input latency P99 is 2,669,474.24, down 2,931,331.84 — the predicted direction, past the floor. The same pipeline with nothing moved (`counterfactual/c7-dev/replay/`) reproduces the RQ0 run's trace hash and its P99, 5,600,806.08. Under 0.95 the cap still parks 372 times, every park on a batch-class task while a non-batch task is runnable (`counterfactual/c7-dev/cap-0.95/cap-check.json`).

**Class: property.** Every program follows its reference; the row's floor cap reaches the editor's own burst tail, which B1 puts in the batch class, while the upgrade's short sleeps keep it out of the class.

## 9. `c7-video-edit`

**Configurations.** As `c7-dev`'s: fixed the boot MLFQ with no cap; the oracle the `video-edit` / `background_wanted: false` row, the same MLFQ with `batch_bandwidth_cap` 0.05, for the whole window (`runs/rq0-gate/c7-video-edit/oracle~focus/schedule.json`). The cap is the one difference.

**Mechanism traced** (`run_profile.py`). The video editor (Kdenlive) has no keystroke stream; its term reads the wait of its own timer and event wakes (`docs/harness/metrics.md` §6.13). In the first half of the window the cap parks the upgrade (518 parks); in the second half it parks the editor (685 of its 785), while the upgrade's bursts are mostly under a millisecond (median 259 µs between voluntary blocks), out of the batch class by B1, and the editor's longer bursts — up to 131,658 — put it in. Inside the window the editor is delivered 8,690,964 of CPU against 11,721,488 under fixed and the upgrade 17,640,099 against 14,602,611: the cap the row sets to hold the upgrade leaves it more. The app latency P50 is 3,506,504 and the P99 8,090,656.02, against 4,750,232.68 under fixed.

**Programs on the path** (`cap-check-c7-video-edit.json`):
- The daemon: the schedule's entry is the row's algorithm, params and cap, for the ground truth's segment.
- The row: `video-edit` is an interactive-only mode — MLFQ; unwanted background — the floor cap 0.05; boot params.
- The simulator: 1,303 of 1,303 parks on a batch-class task while a task not in the batch class and not idle is runnable; no parked task runs; the batch class's CPU while capped 169,850 over 4,381,034, a share of 0.039, within the cap plus one slice.
- The harness: the 9,523 `app_latency` rows recomputed by §6.13 equal the run's records row for row; their P99 is 8,090,656.02, the scored value.

**Counterfactual** (recorded before the run): the oracle on `c7-video-edit` with the row's `batch_bandwidth_cap` moved from 0.05 to 0.95, everything else as the oracle's schedule. Predicted: the editor's app latency P99 moves down from 8,090,656.02 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c7-video-edit/cap-0.95/`): the editor's app latency P99 is 4,755,986.34, down 3,334,669.68 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace hash and its P99. Under 0.95 the cap parks 25 times, each on a batch-class task while a non-batch task is runnable, and the 9,523 rows recompute equal to the counterfactual's records.

**Class: property.** Every program follows its reference; as on `c7-dev`, the row's floor cap reaches the editor's burst tails, which B1 puts in the batch class, while the upgrade's short bursts keep it out.

## Programs checked, then the mechanism

The three files below pass every check of `cap_check.py` — every park on a batch-class task while a task not in the batch class and not idle is runnable, no parked task running, the batch class's CPU while capped within the cap plus one slice, the scored latency rows recomputed equal to the records and their P99 the scored value — with the simulator's reading of a fork-slot wait (below); each one's mechanism and counterfactual follow its checks.

### 1. `c1-compile`

`cap-check-c1-compile.json`: 48,463 parks; the batch class's share while capped 0.367 under the 0.5 cap; 2,544 rows equal, P99 361,025,331.76. Oracle: LOTTERY, `batch_share` and cap 0.5, the `compile` / `background_wanted: true` row. The editor is delivered the same CPU as under fixed (253,348,583 against 253,566,630, `run_profile.py`); its longest burst without a voluntary block is 235,469,634 against 136,488,095 — keystrokes queued behind its own work complete their WAITs at zero wait, so the bursts merge.

**Mechanism traced.** The keystrokes wait 68 s longer on average under the oracle (1,837 of 2,544 worse). Behind on its keystrokes, the editor's bursts end in no block, so during the build it is in the batch class for nearly all its CPU: 153.18 s of 153.74 under the oracle, 178.93 of 180.00 under fixed, up to the build's end (1,471,617,554 and 1,497,877,689). The row's share and cap, set for the build, therefore treat the editor as the build's batch work: LOTTERY draws the batch class at 0.5 when a task outside it is runnable and a task uniformly inside it, against up to 48 live compile jobs (`simulator/src/sim.cpp`, `Lottery::pick`), and the cap parks it with them — 2,933 parks, 57.61 s of wall time parked during the build. The editor is delivered 25.75 s less CPU during the build and catches up after it.

**Counterfactual** (recorded before the run): the oracle on `c1-compile` with the row's `batch_share` and `batch_bandwidth_cap` moved together from 0.5 to 0.95 in the schedule's entries 1 and 2, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source): the batch class, the editor in it, draws at 0.95 and is parked less. Predicted: the editor's input latency P99 moves down from 361,025,331.76 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c1-compile/share-cap-0.95/`): the editor's input latency P99 is 358,178,804.33, down 2,846,527.43 — the predicted direction, past the floor. It is 2.85 s of the 125.05 s by which the oracle trails fixed; this reading does not attribute the rest. The replay with nothing moved reproduces the run's trace and its P99.

**Class: property.** Every program follows its reference — with the simulator's fork-slot rule as it was, the defect stage AF fixed, which moves this P99 by 2.1 s (above); the row treats the editor, in the batch class through the build, as the build's batch work.

### 6. `c7-compile`

`cap-check-c7-compile.json`: 24,299 parks; share while capped 0.0498 under the 0.05 cap; 398 rows equal, P99 87,359,931. The editor is delivered 19,240,992 of CPU against 25,289,134 under fixed; the parks fall on `make` (`build`) and the compile jobs' `cc1`.

**Mechanism traced.** The cap is the one difference between the two runs (fixed the boot MLFQ, the oracle the `compile` / `background_wanted: false` row, the same MLFQ with `batch_bandwidth_cap` 0.05). The keystrokes wait 13.3 s longer on average under the oracle (256 of 398 worse). Behind on its keystrokes, the editor is in the batch class for nearly all its CPU during the build (18.45 s of 19.24 under the oracle, 24.84 of 25.28 under fixed). Under fixed it is delivered about one top-queue slice per 100 ms boost interval, 10.08 ms on average over 2,509 intervals: the boost puts every ready task back in the top queue in task-id order (`Mlfq::on_timer`), the editor ahead of the compile jobs, and it is demoted behind them before its next turn. Under the oracle the cap parks the batch class — the editor with the compile jobs — while a build step outside it is runnable: in the 220 of 2,449 intervals where the editor is parked at the boost it misses the rebuild and is delivered 1.05 ms; in the others 8.53 ms, its slice cut by a park. The compile jobs are delivered 5.71 s more, the editor 6.05 s less.

**Counterfactual** (recorded before the run): the oracle on `c7-compile` with the row's `batch_bandwidth_cap` moved from 0.05 to 0.95 in the schedule's entry 1, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the editor's input latency P99 moves down from 87,359,931 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c7-compile/cap-0.95/`): the editor's input latency P99 is 79,761,519.40, down 7,598,411.60 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and its P99.

**Class: property.** Every program follows its reference; the row's floor cap, meant for the upgrade-shaped build, parks the editor with the compile jobs while it is in the batch class, and costs it the one top-queue turn per boost MLFQ otherwise gives it.

### 8. `c7-ml-train`

`cap-check-c7-ml-train.json`: 9,579 parks, all but 11 the hog's; share while capped 0.040; 1,753 rows equal, P99 8,020,875.92. The editor is delivered the same CPU as under fixed (187,667,633 against 186,923,275), and its keystrokes wait 143 ms less on average under the oracle. The P99 is set by one cluster near 1,013 s: under fixed the editor's burst from 996.86 s blocked once, at 1,003.57 s; under the oracle, its timing moved by the hog's earlier parks, it runs on to 1,024.05 s at a 0.30 share, and the keystrokes queued behind it wait about 2.1 s longer. Inside an editor burst both tasks are batch class and the cap is off; MLFQ splits the lane 0.30 / 0.70 between them, the task leading after each 100 ms boost taking 10 + 20 + 40 of its milliseconds.

**Counterfactual** (recorded before the run): the oracle on `c7-ml-train` with the row's `boost_interval_us` moved from 100,000 to 20,000 in the schedule's entry 1, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source): after each boost both tasks run their 10 ms in the top queue, so inside an editor burst the editor's share is about 0.5 in place of 0.30. Predicted: the editor's input latency P99 moves down from 8,020,875.92 by at least the 1,000 µs floor. Beside it, reported and not predicted: the oracle with the row's `batch_bandwidth_cap` moved from 0.05 to 0.95 in entry 1 — the cap's parks are what moved the timing, and the trace gives no direction for the P99 under fewer of them.

**Result** (2026-11-19): with the boost interval at 20,000 (`counterfactual/c7-ml-train/boost-20ms/`) the editor's input latency P99 is 2,249,295.68, down 5,771,580.24 — the predicted direction, past the floor. Reported beside it: with the cap at 0.95 (`counterfactual/c7-ml-train/cap-0.95/`) the P99 is 7,194,480.40, fixed's value to the last digit — with the cap's parks fewer, the cluster near 1,013 s meets the editor's burst as under fixed. The replay with nothing moved reproduces the run's trace and its P99.

**Class: property.** Every program follows its reference; the row's floor cap parks the hog when the editor is out of the batch class, which shifts the timing of one long editor burst against the boost grid, and MLFQ's boost order at the boot params gives the editor 0.30 of the lane inside it — the P99 of the file's 1,753 keystrokes is set by the cluster queued behind that burst, while the keystrokes wait 143 ms less on average.

## The fork-slot wait and rule B1

The simulator's FORK that finds `fork_cap` reached blocks the task without resetting its B1 counter (`simulator/src/sim.cpp`, the FORK case: no `t.burst = 0`), where SLEEP, a TIMER not yet due, a WAIT on a channel and a WAIT on the children each reset it. The batch-class memo's B1 lists a WAIT that has to wait, a SLEEP and a TIMER not yet due as the voluntary blocks — "the task giving the CPU back on its own" — written before the spawn table and its FORK existed. No simulator memo or note records the fork-slot wait's place in B1. `make` (`build`) in `c1-compile` and `c7-compile` stays in the batch class across its fork-slot waits — 17,004 and 5,639 of them in the two oracle runs.

**A defect** (decided 2026-11-19): B1's definition — the task giving the CPU back on its own — covers the fork-slot wait, and the simulator resets at the WAIT on the children, the same act. Fixed as the simulator's stage AF (`simulator@841dc81131cb`): the reset at the fork-slot wait; test (d) of `simulator/tests/test_batch_class.py`, failing on `simulator@0d323c84470a` (the parent parked at 46,620, 49,511 and 52,511 µs after its slot came at 46,000) and passing on the fix, with the mutant `fork-wait-keeps-burst` in `simulator/tests/mutants.py`; the batch-class memo's and the batch-class-and-cap memo's dated corrections. Against the RQ0 run's traces (`stage-regression-af.json`): under fixed all 129 files identical, under oracle 117 — the 12 differing are the files with a build.

Before the fix, on a copy of the simulator with the reset added (the same change): the oracle's editor input latency P99 is 87,359,931 on `c7-compile`, unchanged, and 363,144,270.32 on `c1-compile`, against 361,025,331.76.

## 3. `c1-render`

**Configurations.** Fixed: the boot MLFQ, no cap. Oracle: the `render` / `background_wanted: true` row — LOTTERY, `batch_share` 0.333 and `batch_bandwidth_cap` 0.333, the 10 ms quantum — applied at 0 and again at 2,000,000 (the schedule's entries 1 and 2), the boot MLFQ from 60,000,000 (`runs/rq0-gate/c1-render/oracle~focus/schedule.json`).

**Mechanism traced** (`run_profile.py`). The bulk task (the render) arrives at 2,000,000 and is delivered the same CPU under both, 16,545,000; it ends at 24,089,192 under the oracle against 23,394,289 under fixed. The editor is delivered 22,598,722 of CPU in the window against 21,962,695: the row's share and cap, the batch term's weight share of the file (0.5 against 1.0, `daemon/driver-table/prior.yaml`'s header), give the editor's work the lane before the render's, and the render finishes 694,903 later. The editor's own term reads no headroom (its app latency P99 535,735.06 under both), so the score carries the render's loss alone.

**Programs on the path** (`cap-check-c1-render.json`):
- The daemon: the schedule's entries are the row's algorithm, params and cap, for the ground truth's segment (`render`, `background_wanted: true`).
- The row: wanted batch work — LOTTERY; its cap the batch term's share of the file's scoring weight, 0.5 / (1.0 + 0.5) = 0.333; `batch_share` equal to the cap; the boot quantum.
- The simulator: 1,815 of 1,815 parks on a batch-class task while a task not in the batch class and not idle is runnable; no parked task runs; the batch class's CPU while capped 2,075,891 over 12,668,482, a share of 0.164, within the cap plus one slice.
- The harness: the bulk task's `turnaround` recomputed by `docs/harness/metrics.md` §6.6 — its `task_end` minus its `task_arrive` — equals the run's record, 22,089,192, the scored value.

**Counterfactual** (recorded before the run): the oracle on `c1-render` with the row's `batch_share` and `batch_bandwidth_cap` moved together from 0.333 to 0.95 in the schedule's entries 1 and 2, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the bulk task's turnaround moves down from 22,089,192 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c1-render/share-cap-0.95/`): the bulk task's turnaround is 18,948,257, down 3,140,935 — the predicted direction, past the floor. The replay with nothing moved, on the same rebuilt simulator, reproduces the run's trace and its turnaround.

**Class: property.** Every program follows its reference; the row's share and cap, set by the table's rule from the batch term's weight, give the editor's work the lane first, and the render's turnaround carries the cost while the editor's term has no headroom to show the gain.

## 2. `c1-ml-train`

**Configurations.** Fixed: the boot MLFQ, no cap. Oracle: the `ml-train` / `background_wanted: true` row — LOTTERY, `batch_share` and `batch_bandwidth_cap` 0.333, the 10 ms quantum — applied at 0 and again at 2,000,000 (entries 1 and 2), the boot MLFQ from 1,612,000,000.

**Mechanism traced** (`run_profile.py`). The hog (the training run) arrives at 2,000,000 and is delivered the same CPU under both, 1,389,885,000; it ends 2,958,284 later under the oracle. The editor is delivered 212,723,492 of CPU in the window against 209,973,279, and its term gains: its input latency P99 is 2,078,714.21 against 7,085,597.24. The row's share and cap, the batch term's weight share of the file, give the editor's work the lane before the hog's, and the hog's turnaround carries the cost.

**Programs on the path** (`cap-check-c1-ml-train.json`):
- The daemon: the schedule's entries are the rows' algorithms, params and caps, for the ground truth's segments.
- The row: wanted batch work — LOTTERY; its cap the batch term's share of the file's scoring weight, 0.5 / (1.0 + 0.5) = 0.333; `batch_share` equal to the cap; the boot quantum.
- The simulator: 105,055 of 105,055 parks on a batch-class task while a task not in the batch class and not idle is runnable; no parked task runs; the batch class's CPU while capped a share of 0.330, within the cap plus one slice.
- The harness: the hog task's `turnaround` recomputed by `docs/harness/metrics.md` §6.6 equals the run's record, 1,599,230,869, the scored value.

**Counterfactual** (recorded before the run): the oracle on `c1-ml-train` with the row's `batch_share` and `batch_bandwidth_cap` moved together from 0.333 to 0.95 in the schedule's entries 1 and 2, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the hog task's turnaround moves down from 1,599,230,869 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c1-ml-train/share-cap-0.95/`): the hog task's turnaround is 1,595,291,798, down 3,939,071 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and its turnaround.

**Class: property.** Every program follows its reference; the row's share and cap, set by the table's rule from the batch term's weight, give the foreground the lane first — its term gains — and the training run's turnaround carries the cost.

## 4. `c1-transcode`

**Configurations.** Fixed: the boot MLFQ, no cap. Oracle: the `transcode` / `background_wanted: true` row — LOTTERY, `batch_share` and `batch_bandwidth_cap` 0.333, the 10 ms quantum — applied at 0 and again at 2,000,000 (entries 1 and 2), the boot MLFQ from 4,762,000,000.

**Mechanism traced** (`run_profile.py`). The batch task (the transcode) arrives at 2,000,000 and is delivered the same CPU under both, 2,970,871,000; it ends 240,241,029 later under the oracle. The video editor is delivered 1,371,524,019 of CPU in the window against 1,211,372,935, and its term gains: its app latency P99 is 430,531.08 against 447,969.18. The row's share and cap give the video editor's work the lane before the transcode's, and the transcode's turnaround carries the cost.

**Programs on the path** (`cap-check-c1-transcode.json`):
- The daemon: the schedule's entries are the rows' algorithms, params and caps, for the ground truth's segments.
- The row: wanted batch work — LOTTERY; its cap the batch term's share of the file's scoring weight, 0.5 / (1.0 + 0.5) = 0.333; `batch_share` equal to the cap; the boot quantum.
- The simulator: 422,963 of 422,963 parks on a batch-class task while a task not in the batch class and not idle is runnable; no parked task runs; the batch class's CPU while capped a share of 0.296, within the cap plus one slice.
- The harness: the batch task's `turnaround` recomputed by `docs/harness/metrics.md` §6.6 equals the run's record, 4,134,853,844, the scored value.

**Counterfactual** (recorded before the run): the oracle on `c1-transcode` with the row's `batch_share` and `batch_bandwidth_cap` moved together from 0.333 to 0.95 in the schedule's entries 1 and 2, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the batch task's turnaround moves down from 4,134,853,844 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c1-transcode/share-cap-0.95/`): the batch task's turnaround is 3,391,719,510, down 743,134,334 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and its turnaround.

**Class: property.** Every program follows its reference; the row's share and cap, set by the table's rule from the batch term's weight, give the foreground the lane first — its term gains — and the transcode's turnaround carries the cost.

## 5. `c2-p3a`

**Configurations.** Fixed: the boot MLFQ, no cap. Oracle: the `video-edit` / `background_wanted: true` row — the boot MLFQ with `batch_bandwidth_cap` 0.5 — from 0, then the `render` / `background_wanted: true` row — LOTTERY, `batch_share` and `batch_bandwidth_cap` 0.333, the 10 ms quantum — from 60,000,000 (entry 2), the boot MLFQ from 326,000,000.

**Mechanism traced** (`run_profile.py`). The bulk task (the render) arrives at 60,000,000, in the render segment, and is delivered the same CPU under both, 16,545,000; it ends 637,311 later under the oracle. The editor is delivered 110,900,243 of CPU in the window against 110,531,784, and its term gains: its app latency P99 is 42,435.19 against 45,133.12. The render row's share and cap give the editor's work the lane before the render's, and the render's turnaround carries the cost.

**Programs on the path** (`cap-check-c2-p3a.json`):
- The daemon: the schedule's entries are the rows' algorithms, params and caps, for the ground truth's segments.
- The row: the render segment's row is wanted batch work — LOTTERY; its cap the batch term's share of the file's scoring weight, 0.5 / (1.0 + 0.5) = 0.333; `batch_share` equal to the cap; the boot quantum.
- The simulator: 1,737 of 1,737 parks on a batch-class task while a task not in the batch class and not idle is runnable; no parked task runs; the batch class's CPU while capped a share of 0.041, within the caps plus one slice.
- The harness: the bulk task's `turnaround` recomputed by `docs/harness/metrics.md` §6.6 equals the run's record, 23,119,499, the scored value.

**Counterfactual** (recorded before the run): the oracle on `c2-p3a` with the row's `batch_share` and `batch_bandwidth_cap` moved together from 0.333 to 0.95 in the schedule's entry 2, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the bulk task's turnaround moves down from 23,119,499 by at least the 1,000 µs floor.

**Result** (2026-11-19, `counterfactual/c2-p3a/share-cap-0.95/`): the bulk task's turnaround is 19,484,568, down 3,634,931 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and its turnaround.

**Class: property.** Every program follows its reference; the row's share and cap, set by the table's rule from the batch term's weight, give the foreground the lane first — its term gains — and the render's turnaround carries the cost.

## The cases read at other combinations

In cases 10 to 14 the oracle run is the primary one; the case is the boot MLFQ at another slice serving the term better than the oracle's row, which sits at the boot values by the table's header (the 10 ms slice and quantum). Fixed's term is jagged across the sweep's slices (`runs/rq0-gate/post-hoc/scores.csv`): `c7-render`'s editor 5.75 s at 10 ms and 30 ms, 3.42 s at most others; `c2-p1a`'s 12.95 s at 10 and 30 ms, 7.5–7.9 s at most others. Under OSTEP's rules at three queues and a 100 ms boost (`ostep` ch. 8, Rules 4 and 5; `simulator/src/sim.cpp`, `Mlfq`), two CPU-bound tasks each take up to slice × (1 + 2 + 4) of every boost interval: at 7 ms the two allotments, 49 ms each, fit in the interval and split it evenly; at 10 ms they do not, and the task leading after the boost takes 70 ms to the other's 30. LOTTERY never preempts the holder before its quantum ends (`Lottery::preempts`), so a woken foreground task waits out the holder's quantum before the next draw. In case 15 the oracle runs under the cap band's 0.333 table. Each counterfactual moves the oracle row's knob to the value the fixed run of the combination used, the 11.2 grill's choice.

### 11. `c2-p1a`

The term reads the window [60,000,000, 99,435,000), the `ml-train` / `background_wanted: true` segment: the oracle's entry 2, LOTTERY, `batch_share` and cap 0.333, the 10 ms quantum. In the window the editor's input latency P99 is 12,953.19 ms under fixed at 10 ms, 7,512.78 at 7 ms and 8,227.01 under the oracle; the editor is delivered 11.33 s of CPU in the window at 10 ms, 15.98 at 7 ms and 15.59 under the oracle. The boot MLFQ at 10 ms splits the lane 0.30 / 0.70 with the hog inside a boost interval and at 7 ms evenly; the oracle's LOTTERY row delivers the editor nearly the 7 ms share, and its keystrokes wait out the hog's quantum at each wake.

**Counterfactual** (recorded before the run): the oracle on `c2-p1a` with entry 2's `timeslice_us` moved from 10,000 to 7,000, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the editor's input latency P99 in the window moves down from 8,227,009.39 by at least the 1,000 µs floor.

**Programs on the path** (`elsewhere/cap-check-c2-p1a-*.json`): the oracle run — 654 parks, each on a batch-class task while a task not in the batch class and not idle is runnable, no parked task running, the batch class's CPU while capped a share of 0.073 within the caps plus one slice; the 525 `input_latency` rows recomputed equal to the records. The fixed run at the combination (`fixed+ostep-slice-7000us~focus`) — no cap, the 525 rows recomputed equal. The daemon's schedule is the rows' algorithms, params and caps for the ground truth's segments, and the rows follow the table's rules: the boot params, the cap by the header's rule.

**Result** (2026-11-19, `counterfactual/c2-p1a/slice-7ms/`): the term is 7,744,910.11, down 482,099.28 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and the scored value.

**Class: property.** Every program follows its reference; the row's 10 ms quantum, which a woken editor waits out at each keystroke beside the hog, sets the window's tail.


### 12. `c2-p3a`

The term reads the window [60,000,000, 326,000,000), the `render` / `background_wanted: true` segment: the oracle's entry 2, LOTTERY, `batch_share` and cap 0.333, the 10 ms quantum. In the window the editor's app latency P99 is 45.13 ms under fixed at 10 ms, 38.16 at 7 ms and 42.44 under the oracle, its CPU 84.44, 84.29 and 84.81 s — the editor's work is light and the term is the wait at its wakes; the oracle's LOTTERY row never preempts, so a woken editor waits out the holder's quantum (`Lottery::preempts`).

**Counterfactual** (recorded before the run): the oracle on `c2-p3a` with entry 2's `timeslice_us` moved from 10,000 to 7,000, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the editor's app latency P99 in the window moves down from 42,435.19 by at least the 1,000 µs floor.

**Programs on the path** (`elsewhere/cap-check-c2-p3a-*.json`): the oracle run — 1,737 parks, each on a batch-class task while a task not in the batch class and not idle is runnable, no parked task running, the batch class's CPU while capped a share of 0.041 within the caps plus one slice; the 73,832 `app_latency` rows recomputed equal to the records. The fixed run at the combination (`fixed+ostep-slice-7000us~focus`) — no cap, the 73,832 rows recomputed equal. The daemon's schedule is the rows' algorithms, params and caps for the ground truth's segments, and the rows follow the table's rules: the boot params, the cap by the header's rule.

**Result** (2026-11-19, `counterfactual/c2-p3a/slice-7ms/`): the term is 40,209.97, down 2,225.22 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and the scored value.

**Class: property.** Every program follows its reference; the row's 10 ms quantum, which a woken editor waits out beside the render, sets the window's tail.


### 13. `c7-photo`

Oracle: the `photo` / `background_wanted: false` row, the boot MLFQ with cap 0.05, for the whole window. The photo editor's app latency P99 over its 193 wakes is 2,978,927.88 under fixed at 10 ms and under the oracle, 2,968,927.88 at 30 ms — one 10 ms slice less; its CPU 2.55 s under all three. The P99 falls between the 191st and 192nd of the 193 wakes: wakes from 13.5 to 14.7 s queued behind the photo editor's own burst from 13.4 s, which shares the lane slice by slice with the CPU-bound upgrade; the burst reaches the WAITs that serve them at 16.74 s under fixed at 10 ms and 10 ms sooner at 30 ms (the four longest rows each 10,000 shorter).

**Counterfactual** (recorded before the run): the oracle on `c7-photo` with entry 1's `timeslice_us` moved from 10,000 to 30,000, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the photo editor's app latency P99 moves down from 2,978,927.88 by at least the 1,000 µs floor.

**Programs on the path** (`elsewhere/cap-check-c7-photo-*.json`): the oracle run — 17 parks, each on a batch-class task while a task not in the batch class and not idle is runnable, no parked task running, the batch class's CPU while capped a share of 0.004 within the caps plus one slice; the 193 `app_latency` rows recomputed equal to the records. The fixed run at the combination (`fixed+ostep-slice-30000us~focus`) — no cap, the 193 rows recomputed equal. The daemon's schedule is the rows' algorithms, params and caps for the ground truth's segments, and the rows follow the table's rules: the boot params, the cap by the header's rule.

**Result** (2026-11-19, `counterfactual/c7-photo/slice-30ms/`): the term is 2,968,927.88, down 10,000 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and the scored value.

**Class: property.** Every program follows its reference; the row's boot slice sets how fast the photo editor's burst moves against the upgrade, and the queued wakes wait for its end.


### 14. `c7-render`

Oracle: the `render` / `background_wanted: false` row, the boot MLFQ with cap 0.05, for the whole window. The editor's app latency P99 is 5,750.29 ms under fixed at 10 ms, 3,360.54 at 7 ms and 5,750.45 under the oracle; its CPU 4.02, 5.67 and 4.25 s. Beside the CPU-bound render most of the editor's CPU is in long bursts, in the batch class by B1 — 3.06 s of 4.02 under fixed at 10 ms, 4.88 of 5.67 at 7 ms, 3.06 of 4.25 under the oracle — which share the lane with the render by the boost-interval split above; the oracle's cap, the row's one difference from fixed at 10 ms, moves the editor's CPU by 0.23 s.

**Counterfactual** (recorded before the run): the oracle on `c7-render` with entry 1's `timeslice_us` moved from 10,000 to 7,000, everything else as the oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the editor's app latency P99 moves down from 5,750,451.47 by at least the 1,000 µs floor.

**Programs on the path** (`elsewhere/cap-check-c7-render-*.json`): the oracle run — 283 parks, each on a batch-class task while a task not in the batch class and not idle is runnable, no parked task running, the batch class's CPU while capped a share of 0.030 within the caps plus one slice; the 6,452 `app_latency` rows recomputed equal to the records. The fixed run at the combination (`fixed+ostep-slice-7000us~focus`) — no cap, the 6,452 rows recomputed equal. The daemon's schedule is the rows' algorithms, params and caps for the ground truth's segments, and the rows follow the table's rules: the boot params, the cap by the header's rule.

**Result** (2026-11-19, `counterfactual/c7-render/slice-7ms/`): the term is 3,323,032.74, down 2,427,418.73 — the predicted direction, past the floor. The replay with nothing moved reproduces the run's trace and the scored value.

**Class: property.** Every program follows its reference; the row's boot slice sets the editor's share of each boost interval beside the CPU-bound render.


### 15. `c7-transcode`

The cap band's 0.333 table moves the `transcode` / `background_wanted: false` row's cap from 0.05 to 0.333, nothing else (`daemon/driver-table/prior-floor-0.333.yaml`). The video editor's app latency P99 under the oracle is 1,500.32 ms at 0.05 and 0.2, 13,973.88 at 0.333 and 2,715.92 at 0.5, against 11,127.96 under fixed; its CPU 908.37 s at 0.05, 839.02 at 0.333, 699.55 under fixed. Its 0.333 oracle's schedule differs from the primary oracle's in that cap alone, so this counterfactual's schedule is the primary oracle's.

**Counterfactual** (recorded before the run): the 0.333 table's oracle on `c7-transcode` with entry 1's `batch_bandwidth_cap` moved from 0.333 to 0.05, everything else as that oracle's schedule, on the RQ0 run's simulator (`simulator@0d323c84470a`, rebuilt from its source). Predicted: the video editor's app latency P99 moves down from 13,973,877 by at least the 1,000 µs floor.
