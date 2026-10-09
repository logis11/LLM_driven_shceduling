# Task 9.14 — reads

Facts established for the consumer rework with no value changed, each with its method and the copy read. All on branch `jioh/dataset-rebuild` (2026-10-09), Python 3.12.4 on an Apple M1 Pro; the scan scripts are in `scans/`. The raw landings were read from the releases' assets as `gh release download` unpacks them.

## R1 — the MNIST repeats' CPU against `c2-p1a`'s bind (2026-10-09)

`c2-p1a` and `c1-ml-train` bind the training job at 1 389.885 s of CPU, the pool's mean over the six repeats of `meas-ci:background:2026-10-03` (9.10 D88, ±4.04 %, 1 293.8–1 455.8 s). A replay stream must hold the CPU its task binds (grill Q6), so each repeat's python process was read: taskstats' `utime + stime` of the `python` row of `taskstats.mnist-train.tsv`, and perf's sum of the process's timehist runs (`scans/mnist_cpu.py`: `campaign/analyze.py`'s `load_rows` over the process's pid, resumes merged by `merge_resumes`).

| repeat | run | taskstats (s) | perf (s) | against the bind |
|---|---|---|---|---|
| r1 | 37091275421 | 1 379.004 | 1 378.849 | 11.0 s short |
| r2 | 37091275421 | 1 404.338 | 1 404.222 | 14.3 s over |
| r3 | 37091313419 | 1 455.878 | — | 66.0 s over |
| r4 | 37091275421 | 1 293.981 | — | 95.9 s short |
| r5 | 37091275421 | 1 407.361 | 1 407.249 | 17.4 s over |
| r6 | 37093607991 | 1 399.504 | 1 399.391 | 9.5 s over |

perf and taskstats agree within 0.16 s. The sixth repeat is the nearest that covers the bind and is the stream (`dataset/replay/replay-cpu-batch-python3.json.gz`): 25 runs between voluntary blocks, 1 399.391 s of CPU over 1 399.5 s.

## R2 — the upgrade repeats' CPU against the C7 files' bind (2026-10-09)

The C7 counterparts and `c2-p2a`/`c2-p2b` bind the unattended upgrade at 26.385 s, the pool's mean CPU total over the nine repeats of `meas-ci:background:2026-10-01` (9.10 D45, ±3.78 %). Each repeat's install stage read as the entry's tables are (`scans/upgrade_cpu.py` → `replay_fold_in.read_runs`: the stage's tree by `background/analyze.py`'s `phase_tree`, every process of it the program (9.10 D37), its segments on the measured CPU), beside taskstats' sum over every `pid` row:

| repeat | run | perf (s) | taskstats (s) |
|---|---|---|---|
| r1 | 36847549673 | 25.559 | 25.343 |
| r2 | 36847096521 | 25.247 | 25.030 |
| r3 | 36847096521 | 25.563 | 25.372 |
| r4 | 36848289469 | 27.245 | 27.034 |
| r5 | 36847549673 | 29.155 | 28.928 |
| r6 | 36851095354 | 25.724 | 25.512 |
| r7 | 36851095354 | 25.413 | 25.215 |
| r8 | 36851095354 | 26.174 | 25.962 |
| r9 | 36851095354 | 27.381 | 27.201 |

The perf totals' mean is 26.385 s, D45's value. Six of the nine fall short of the bind; the fourth repeat is the nearest that covers it and is the stream (`replay-package-upgrade.json.gz`): 14 699 runs, 27.245 s of CPU over 27.4 s, 916 processes in the stage's tree.

## R3 — the six replay streams as read (2026-10-09)

`replay_fold_in.py` over the landings its `SOURCES` table names, the readings beside the carried values:

| stream | landing | read | reading | carried value beside it |
|---|---|---|---|---|
| `replay-code-editor` | `meas-ci-2026-09-25`, repeat 1, idle phase from 200 s (9.5 D83) | 700.0 s | 78 415 wakes, 112.0/s, CPU share 0.0128 | the idle phase's 13.6 ms/s baseline (9.5 D53) |
| `replay-web-browser` | `meas-ci-2026-09-20`, repeat 1, idle phase | 600.0 s | 26 752 wakes, 44.6/s, CPU share 0.0032 | — |
| `replay-renderer-hidden` | `meas-ci-desktop-2026-10-05b`, repeat 1, steady phase | 600.0 s | 12 page renderers present for the whole phase, the control tab dropped; 1 535 wakes, 0.213/s per renderer | steady wakes/s per renderer 0.2082–0.2152 (the entry's `validation_stats`) |
| `replay-video-call` | `meas-ci-2026-09-20`, repeat 1, play phase | 480.0 s | 47 997 cycles, 10.0 ms apart | the period 10 001 µs |
| `replay-package-upgrade` | `meas-ci-background-2026-10-01`, repeat 4 (R2) | 27.4 s | 14 699 runs, 27.245 s of CPU | the bind 26.385 s |
| `replay-cpu-batch-python3` | `meas-ci-background-2026-10-03`, repeat 6 (R1) | 1 399.5 s | 25 runs, 1 399.391 s of CPU | the bind 1 389.885 s |

`replay_fold_in.py --check` reproduces every file byte for byte from the landings.

## R4 — the four replay artifacts against their bases (2026-10-09)

`scans/replay_compare.py` over `dataset/build/coreset-single/<file>.workload.json` and `<file>@replay.workload.json`: the input wakes are identical in all four (the keystroke replay stays as compiled); the batch binds compile exactly (26.385 s, 1 389.885 s); `meta` differs in `id` alone.

| file | timer wakes, base → replay | demand, base → replay |
|---|---|---|
| `c7-dev` | editor 2 774 → 2 813 | editor 7.784 → 7.725 s |
| `c7-browsing` | browser 2 060 → 2 042; the four renderers 7, 3, 5, 9 → 6, 8, 2, 11 | browser 0.464 → 0.466 s |
| `c7-meeting` | — (TIMER grid, 2 638 ticks both) | call 6.333 → 3.858 s |
| `c2-p1a` | editor 10 819 → 10 929 | editor 52.421 → 52.278 s |

The call's demand falls by 39 % under its measured window: the play phase holds 240 s saturation cycles (9.5 D54), and the window the seed draws lands in a quiet stretch where the compiled stream draws every cycle's run from the pooled table. That is the sensitivity the trace-replay line reads, not a defect of either build.
