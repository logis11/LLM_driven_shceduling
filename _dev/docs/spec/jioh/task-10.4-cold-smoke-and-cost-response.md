# Task 10.4 — The cold smoke and the cost response

인지오's sub-task 10.4 in `_dev/TODO.md` (Phase 10, Integration and the RQ0 run), decided on 2026-11-14: the smoke on the real simulator and the real daemon with an empty cache, the full run's cost projected from it, and the cost response fixed before the RQ0 run. It carries the Phase 10 spec's decision 5 — a cold smoke, then the cost response, then the full run (`_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`). The integration gate (10.2) passed on 2026-11-14, so the smoke runs on the gated binary.

## Scope

- The harness changes that land before the smoke: the records path's quadratic count, what a finished run leaves on disk, each run's memory recorded, the worker configuration.
- The cold smoke: the RQ0 gate spec's own run list at a low seed count, on the gated simulator and the real daemon.
- The rule, written before the smoke, that projects the full run's cost and selects the cost response.
- The starvation readings on the smoke: the guard table, the wait check, the five `oracle` runs that fail the starvation guard today.
- The sub-task's record.

Out of scope: the RQ0 run (10.5); the variant lines reading a failed guard (10.3).

## Locked decisions

### 1. The quadratic count is fixed before the smoke

`held()` in `harness/tools/harness/primitives.py` counts every earlier drop for each `wake_drop` line — 92 % of `c1-compile`'s records time, 168,698 drops (`_dev/research/jioh/task-10.2-integration-gate/records-profile-c1-compile.txt`). Its replacement lands before the smoke, and the smoke measures the records path the full run uses. The Phase 10 spec's decision 5 names one response chosen from the smoke's figures; here the fix precedes the smoke, and the cost response is what the smoke's figures select after it.

### 2. The pre-smoke records change is the count, the schema check and the rows' memory

Extended 2026-11-14. Beside the count, the rows' schema check — 18.7 of `c7-compile`'s 19.5 s records build once the count is fixed — and the memory the rows hold — `c6-dual`'s records build past 15 GB on the 16 GB home machine, swapping — change before the smoke, the records held byte for byte by decision 3's suite and its 28 runs. The smoke measures the records path after all three.

### 3. The fix is held byte for byte by three things

- The suite.
- The 28 runs of the integration gate's short run (`runs/integration-gate/smoke/`; seven files, 1 to 168,698 `wake_drop` lines under `fixed`): each run's records rebuilt from its trace and compared byte for byte with the records on disk, the comparison recorded with its hashes.
- A test that keeps the old count as a reference and compares the two on generated drop sequences, those reaching the two guard branches among them — a drop that names no timer wake, a drop with none held.

### 4. Disk is a second budget

Disk stands beside the 80 hours of the Phase 10 spec's decision 5. As the runner stores a run today — each trace four times, two in the execution cache and two in the run directory, the records beside them, every run's outputs kept until the guards stage at the end — the full run's run directories come to about 2.3 TB against 145 GB free on the home machine (estimated 2026-11-14: seven files' sizes from the short run, the others from the October smoke's directories on the mock simulator). The runner's storage changes before the smoke with no output changed, and the smoke measures bytes per file on the storage the full run uses.

### 5. What a finished run leaves

The records and one trace gzipped, the rerun trace as its SHA-256, the small files as they are. On `c1-compile`'s `fixed` run gzip takes the records from 59.7 MB to 2.6 MB and the trace from 58.9 MB to 3.9 MB. The fallback, taken by decision 15: the records gzipped, both traces as hashes.

### 6. The October smoke's outputs are deleted

`runs/smoke` (83 GB) and `runs/.cache` (65 GB) are deleted whole before the smoke, on 인지오's word. The October smoke's record stays `_dev/research/jioh/task-9.16-exit-audits/gate/smoke-status.txt`.

### 7. The worker configuration comes from a memory calibration

The runner records each run's peak resident memory beside its wall time. A short sequential pass measures one run of each heavy family and of the largest light files, and `workers`, `heavy_workers` and `heavy_mb` are fixed so that the peaks running at once fit the home machine's 16 GB. The smoke and the full run use that one configuration.

### 8. The variant lines land before the smoke

Sub-task 10.3 — a failed non-exempt guard on a run a variant's gap reads makes that line's count unavailable — lands before the smoke. Phase 10's sub-tasks are renumbered to that order (2026-11-14).

### 9. The smoke is the RQ0 gate spec's run list at seed count 2

The smoke runs a throwaway copy of `harness/experiments/rq0-gate.yaml` with the seed count at 2: all 129 files, 1,197 runs — 23 on each of the 19 judging files, 14 on each of the 32 reporting files, 4 on each of the 78 variant files — the ten alternative boot defaults and the three cap band tables among them. The verdict and the gap lines of its report are not read. The cost response is decided from the wall times, the memory, the bytes, the guard table and the wait check, by the rule of decisions 12–15.

### 10. The smoke starts once the pre-smoke work is merged

It is started through the tunnel and runs unattended on the home machine; no leave is needed for it. No date is fixed: it moves with 인지오's schedule. The RQ0 run keeps its leave.

### 11. A failed run goes through the integration gate's procedure

A run of the smoke that fails is placed and fixed by the 10.2 spec's decisions 13 and 14 (`_dev/docs/spec/jioh/task-10.2-integration-gate.md`: the ratified contract decides which side is wrong and 인지오 changes it; a change to a program's source reruns the gate's parts that read it). The gate is re-passed on the new version, the RQ0 gate spec re-pinned, and the smoke restarted. The projection and the cost response are made only from a smoke in which every run finished.

### 12. The upper projection

For each file, its slowest measured run of any condition stands for every one of its runs in the full run, and its largest run directory for their bytes. The wall projection is the longer of the two pools, plus the smoke's end stages scaled by the run count. The full run is counted cold: all 19,425 runs executed, all their bytes new. The mean projection is printed beside the upper one, for the record.

### 13. When the cost is carried

The cost is carried when the upper wall projection is at most 80 hours and the upper disk projection is at most the free space measured at the smoke's start.

### 14. Over on wall time

The largest share in a fresh profile of the file that dominates the projection is removed, the outputs held byte for byte, and the smoke is rerun, its traces served from the execution cache. If the projection is still over, the cap band's and the variant files' runs — 13,713 of the 19,425 — take a seed count of their own, the largest that fits, stated with its sampling error by the `n-grounding` statement's formula, and that statement's "at the same N" sentences are restated. The criterion's runs stay at N = 100 with both of the statement's arguments. If that does not fit, the rule ends and the criterion's N returns to 인지오 as a new decision.

### 15. Over on disk

The fallback of decision 5.

### 16. The five failing `oracle` runs are recorded in the RQ0 gate spec

The runs that fail `starvation_floor` under `oracle` today — `c3-evening`, `c2-p2a@chain-x1.2`, `c2-p2a@chain-x1.4`, `c2-p2b@chain-x1.2`, `c2-p2b@chain-x1.4`; `steam` behind the frame chain under EDF (`simulator/memo/memo_261111.md` Part L) — are named with their cause in the RQ0 gate spec's `sensitivity-lines` statement. The longest-wait line's reopen condition — any run past 15 s reopens the executor-net question with 인경민 before the verdict is read — is scoped to runs on the judging files.

### 17. The guard table and the wait check

The guard table of every condition is read on the judging files; a failed `starvation_floor` there reopens the executor's starvation net. `simulator/tools/wait_check.py` is run on the smoke's traces. A wait it finds that the guard cannot read — one still open at the end, one after a preemption — leads to what the guard's own reading leads to: on a judging file under any condition, over 30 s reopens the starvation net before the full run and past 15 s reopens the question with 인경민; on any other file it is recorded with its run. Reopened: the sub-task stops short of the full run, and the net is its own decision session.

### 18. The record

A research folder for task 10.4 under `_dev/research/jioh/` holds the calibration's figures, the wall time, memory and bytes per run, the two projections, the guard table, the wait check's output and a README. The harness changelog takes one entry for the pre-smoke changes and one for the cost response; the second carries decision 16's restatement and the re-pin.

### 19. A memo only when a teammate is reached

A memo under `docs/memos/` is written if the starvation net is reopened (to 인경민) or if the seed count of the cap band and the variant files changes (to 박이안; the RQ0 gate spec's `random-reading` statement has N proposed to 박이안 and pending confirmation). A carried cost takes no memo.

## Invariants

- Every change before the smoke leaves the runner's outputs byte for byte as they are.
- The smoke runs the harness source and the worker configuration the full run uses; a harness change after it reruns the smoke.
- The verdict and the gap lines of the smoke's report are not read.
- Nothing in the run changes after execution begins except by a harness changelog entry made before any run (the Phase 10 spec's invariant).

## Open items

- Left to the implementation plan: which files the calibration measures and how much memory it leaves free; how the seed-count-2 copy of the RQ0 gate spec is produced; how the guards stage is restructured for the storage change.
- Left to sub-task 10.5's spec session: whether the RQ0 run starts from the smoke's cache.
