# 9.16 compiled-number audit — statements waiting on the simulator, by conformance item

This list is the RQ0 gate spec's statement `simulator-conformance` (`harness/experiments/rq0-gate.yaml:325–357`) read against the compiled-number statements of `report.md` (decision 6 of `_dev/docs/spec/jioh/task-9.16-exit-audits.md`).

- **NAMED** — the document names the conformance item it waits on.
- **UNNAMED** — it does not; the fix is in `findings.md`, F14.
- **"Check"** — what 인경민 runs once the item lands.

Items (c) and (f) are done. Items (a) and (h) carry no statement-specific dependence: (a) underlies every term read off ready lines and the `tick_count` reading of finding G1, and (h) the invocation shape.

## (b) The TIMER skip rule — a TIMER reached after ticks passed consumes the latest and skips the rest

| Location | Statement | Status |
|---|---|---|
| `harness/scoring/scoring-spec.yaml:62–65` | c3-evening's chain term "reads the policies' ordering above a floor of about 0.31 missed under every policy" | UNNAMED |

- The floor itself holds under any rule (1 − 16,667/24,166 = 0.310).
- Check: on c3-evening, the `game.chain.1` miss rate under several rows sits above 0.31 and differs between rows. Under today's backlog rule it is 99.8 % under MLFQ and 99.97 % under EDF (`out/sim.out`).

## (d) `batch_bandwidth_cap` read and applied as a work-conserving ceiling on the behavioural batch class

| Location | Statement | Status |
|---|---|---|
| `docs/daemon/prior-table-pair-review.md:21` | in c6-spoof, from 20 s, "the 0.05 cap holds the miner under the oracle" | UNNAMED |
| `docs/daemon/prior-table-pair-review.md:24` | dev: "the cap bounds the upgrade in the queue they then share" | UNNAMED |
| `docs/daemon/prior-table-pair-review.md:54` (and 55, 57, 58, 62: "same job, same mechanism") | the injected upgrade is batch class "and the floor cap bounds it" | UNNAMED |
| `docs/daemon/prior-table-pair-review.md:83` | on the dev, compile, ml-train and indexing files the editor's keystroke waits "read the floor cap's effect" | UNNAMED |
| `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md:4` | the memo's open item is (d) | NAMED (not a compiled-number statement) |

- Check: on c7-browsing, c7-office, c7-dev, c7-photo, c7-video-edit (the upgrade's batch CPU share is 88–92 %) and c6-spoof (the miner's is 100 %), the foreground's P99 under cap 0.05 is no worse than under cap 0.5, and the batch class's CPU while the foreground is runnable stays at or under the cap.
- On the indexing files, pair review line 83 conflicts with the idle rule — the indexer is idle class, so there is no shared queue. See finding F14.
- Not counted, because they are design rationale rather than compiled-number statements, but their realised effect waits on (d):
  - the prior table's "the floor cap bounds the CPU-bound job" sentences (`prior.yaml:76, 102, 128, 154, 180, 284, 310, 336, 362, 388, 414, 440, 466`);
  - `scoring-spec.yaml:276–279`.

## (e) The strict idle class — an idle task runs only when no other-class task is runnable, and is preempted at once when one wakes, under every algorithm

| Location | Statement | Status |
|---|---|---|
| `harness/experiments/rq0-gate.yaml:296–304` | statement `idle-class-files`: no row reaches the background task; its outcome is identical under every row; the editor's wait is untouched | UNNAMED |
| `harness/scoring/scoring-spec.yaml:36–43` | the six idle-class files are expected no headroom | UNNAMED |
| `harness/scoring/scoring-spec.yaml:96–98` | the idle-class generated placements' job ends at the same time under every row | UNNAMED |
| `daemon/driver-table/prior.yaml:30–34` | header: no row's share or cap reaches an idle task | UNNAMED |
| `daemon/driver-table/prior.yaml:396, 408, 422, 434` | indexing/true, indexing/false, backup/true, backup/false: inert on the files that exercise them | UNNAMED |
| `docs/daemon/prior-table-pair-review.md:15, 34, 35, 44, 46, 67, 68, 81` | the same reading in the rules paragraph, rows A indexing and backup, B p1b and p3b, C indexing and backup, and finding 7 | UNNAMED |
| `docs/memos/2026-10-17-workload-dataset-rebuild.md:71–77` | in c1-indexing the indexer yields at once to the editor's wake; "항목 (e)예요" | NAMED |

- Check, on c1-indexing, c7-indexing, c2-p1b, c1-backup, c7-backup and c2-p3b:
  - the background task's `turnaround` or `cpu_delivered` is identical under all 32 rows;
  - the editor's P99 equals its value with the background task removed.
- Also check the margins, from replaying the editor alone (`out/alone.out`):
  - c2-p3b's backup finishes about 0.3 s before T_end (166.2 s of idle lane against 165.86 s needed);
  - c1-backup's finishes about 0.5 s before T_end;
  - c7-backup's does not finish (98.9 s against 165.67 s).

## (g) `WAIT children:<id>` completes when every spawned child has ended, and without blocking when none is live

| Location | Statement | Status |
|---|---|---|
| `harness/scoring/scoring-spec.yaml:30–32`, applied at `:112` (c1-compile) and `:238` (c4-compile) | the build is "a job that finishes under every row", scored by its turnaround | UNNAMED |
| `docs/daemon/prior-table-pair-review.md:30` | compile row: `build` turnaround 1.0 in c1-compile and c4-compile | UNNAMED |
| `docs/memos/2026-10-17-workload-dataset-rebuild.md:277` | without (g), c1-compile's build time is the same censored value under every condition | NAMED |

- Check: on c1-compile and c4-compile, `make` exits within 0.82 s of T_end under every work-conserving row, and its turnaround differs between rows (`out/alone.out`).
- This also needs the loader fix the final memo asks for in §6.1 (a WAKE whose target is a spawned child); without it, these files do not load in the simulator.
