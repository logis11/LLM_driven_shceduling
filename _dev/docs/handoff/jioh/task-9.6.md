# Handoff — task 9.6 Compile: done (2026-09-20)

Branch `jioh/dataset-rebuild` (Phase 9 works here). 9.6 is ticked in `_dev/TODO.md`. Decisions D1–D31 in `_dev/research/jioh/task-9.6-compile/changelog.md`; method and its dated amendments in `campaign/method.md`; final pool in `campaign/results.md` and `campaign/results/pooled.json`.

## What the slice produced

- **One campaign**, `meas-ci:build:2026-09-18`: 14 same-machine repeats (4, 5, 7, 8, 9–18) on the AMD EPYC 7763 under the machine gate, 28 jobs over runs #10–#37, 12 stopped by the gate, 2 cancelled. Raw records: release `meas-ci-build-2026-09-18`, created at the fold-in commit `6f1ad39` (Actions artifacts expire 2026-12-17).
- **Two conditions fixed mid-campaign**: `clamscan`'s signature database from repeat 9 (D27), `python3`'s warm start from repeat 11 (D28). Their values pool repeats 9–18 and 11–18.
- **The stability rule holds** over 29 of 33 carried values; four are carried with their half-widths under the rule's exception for a value whose spread follows the machine (D29) — the block after each run of `clamscan`, `python3` and `tracker-miner-fs-3`, and `python3`'s runs between blocks. The exception is in `_dev/research/jioh/measurement-campaign-workflow.md`, "The stability rule".
- **Folded in** (D31, plan `_dev/docs/plan/jioh/task-9.6-fold-in.md`): `compiler-child` is the six-member object job with 11 per-(role, step) tables; `build-orchestrator` carries the measured dispatch table and `fork_cap` = cap × 6; `cpu-batch` is a run-and-block loop over the bound program's tables, chosen by a new `program` binding. Three archetypes carry `validation_stats.scope` and rewritten `modeling_notes`; `docs/references.md`'s `meas-ci` status line is the campaign form.

## State of the checks

- Tests 167 passed, 1 skipped, 1 xfailed.
- `make -C dataset lint` and `check` fail on five `-single` demand-window files — the branch's known state until 9.14 — but `c3-workday` now fails **high** (4.84, was 0.86): a spawn-table entry was one process of about 89 ms and is now a job of six processes and about 471 ms. `c6-dual` 1.14 → 1.26 (inside the window); the calibration-exempt compile files 0.15 → 0.93.
- A full `tools/compile.py` now takes about 7 minutes: every draw is materialised (`c3-workday` holds 25 200 member programs; `tracker`'s 30 s job unrolls about 74 000 runs).

## Hands to other slices

- **9.5** — the five-repeat minimum applies to its campaigns (D24).
- **9.10** — `spawn_count` is sized against the old per-entry cost and is 9.10's to resize (인지오, 2026-09-20); whether `c2-p1b` takes the rescan's own tables rather than inheriting `python3`'s (D21); the compile timelines' member names now that a job is six processes (D2); the `file-backup` / `file-archiver` / `game-download` rebindings are 9.7's.
- **9.11** — whether a simulated baseline honours a task's declared scheduling class; `tracker`'s processes declare `SCHED_IDLE` nice 19 while the other four run at the default (D17).
- **9.12** — `docs/research-proposal.md` §2.2's `updatedb` sentence against the measured declarations (D17).
- **9.13** — whether the task model gains a field for a declared class (D17).
- **9.14** — the demand-window rule with `c3-workday` in its new state; the batch-class memo's "never blocks" worked example, which the measured shares contradict; the prior-table rows arguing on "compiler children" (D21, D2).
- **9.15** — the docs naming `cpu-batch`, `compiler-child` and `build-orchestrator`: `docs/data-contracts.md` quotes the old `cpu-batch` YAML, `docs/workload/coreset-guide.md` carries per-file event tables whose numbers moved, `docs/daemon/prior-table-pair-review.md` carries a stale demand column.

## Shared tooling this slice changed

- `dataset/tools/meas/build/` — `run.sh` (fixed signature database, warm `python3` start), `clamav_db.sh`, `analyze.py` (`build_tree` roots at the program forked inside the record), `shapes.py`, `pool.py` (per-repeat means, the D29 exception, per-value projected counts).
- `dataset/tools/meas/loop/` — `common.py` (`artifact_names`, path-limited trigger commits), `pool_runs.py` (skips a landed job whose run has no artifact of the campaign's mode; database check over the pooled `clamscan` repeats).
- `dataset/tools/wlc/sampling.py` — `allow_zero` on `sample()` / `_quantile_sample()`, so a zero-inclusive table may draw zero; every existing call keeps the 1 µs floor.
