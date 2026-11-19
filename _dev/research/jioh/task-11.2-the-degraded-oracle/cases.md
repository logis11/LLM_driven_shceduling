# The degraded oracle — case table

The cases of the 11.2 spec (`_dev/docs/spec/jioh/task-11.2-the-degraded-oracle.md`, decision 2): a judging file's term on which the oracle is worse than fixed by the floor or more, under the scorer with 11.1's sign rule. *Primary* is the primary boot default (`ostep`, the 10 ms slice) under the primary table (`prior`). Values in µs, from `runs/rq0-gate/post-hoc/scores.csv`.

| # | file | term | combination | fixed | oracle | class | evidence | fixing commit |
|---|---|---|---|---|---|---|---|---|
| 1 | `c1-compile` | editor, input latency P99 | primary | 235,971,211.09 | 361,025,331.76 | unexplained | | |
| 2 | `c1-ml-train` | hog, turnaround | primary | 1,596,272,585 | 1,599,230,869 | unexplained | | |
| 3 | `c1-render` | bulk, turnaround | primary | 21,394,289 | 22,089,192 | unexplained | | |
| 4 | `c1-transcode` | batch, turnaround | primary | 3,894,612,815 | 4,134,853,844 | unexplained | | |
| 5 | `c2-p3a` | bulk, turnaround | primary | 22,482,188 | 23,119,499 | unexplained | | |
| 6 | `c7-compile` | editor, input latency P99 | primary | 58,431,291 | 87,359,931 | unexplained | | |
| 7 | `c7-dev` | editor, input latency P99 | primary | 1,750,097.40 | 5,600,806.08 | property | [7](#7-c7-dev) | |
| 8 | `c7-ml-train` | editor, input latency P99 | primary | 7,194,480.40 | 8,020,875.92 | unexplained | | |
| 9 | `c7-video-edit` | editor, app latency P99 | primary | 4,750,232.68 | 8,090,656.02 | unexplained | [9](#9-c7-video-edit) | |
| 10 | `c1-transcode` | video-editor, app latency P99 | 12 ms boot default, `prior` | 365,038.19 | 430,531.08 | unexplained | | |
| 11 | `c2-p1a` | editor, input latency P99 | 7 ms boot default, `prior` | 7,512,775.33 | 8,227,009.39 | unexplained | | |
| 12 | `c2-p3a` | editor, app latency P99 | 7 ms boot default, `prior` | 38,159.57 | 42,435.19 | unexplained | | |
| 13 | `c7-photo` | photo-editor, app latency P99 | 30 ms boot default, `prior` | 2,968,927.88 | 2,978,927.88 | unexplained | | |
| 14 | `c7-render` | editor, app latency P99 | 7 ms boot default, `prior` | 3,360,537.49 | 5,750,451.47 | unexplained | | |
| 15 | `c7-transcode` | video-editor, app latency P99 | primary boot default, `prior@floor-0.333` | 11,127,962 | 13,973,877 | unexplained | | |

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
