# Task 10.5 — The RQ0 run

인지오's sub-task 10.5 in `_dev/TODO.md` (Phase 10, Integration and the RQ0 run), decided on 2026-11-15: the full matrix of the RQ0 gate spec (`harness/experiments/rq0-gate.yaml`) on the gated simulator and the real daemon, the reading of its verdict, and its record. It carries the Phase 10 spec's decisions 1 and 8 — the phase ends at the verdict; the exit criteria (`_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`) — and the two items the 10.4 spec and the tracker left to this session: whether the run starts from the smoke's cache, and the report's place in the repository.

## Scope

- The state the run starts from: the smoke's files on disk, the RQ0 gate spec's pre-run edits, the resume exercised.
- The run: the machine's use beside it, an interruption, a failed run, a run that takes long.
- The reading: what is read before the report is opened, and what a failure found there leads to.
- The record: the report and its hash manifest, the run's record under `docs/`, the lines of `docs/research-claims.md`, the memo to the team.

Out of scope: the failure procedure the RQ0 gate spec names on a FAIL; the re-measurement the RQ0 gate spec's `re-measurement-contingency` statement names; the removal of the run's outputs from disk; the docs sweep (10.6).

## Locked decisions

### 1. The run starts on 2026-11-16, at home, on the machine itself

Every piece of pre-run work is done before it. The run is started and watched on the home M1 Pro directly. The "leave two weeks on" wording of the tracker and of the Phase 10 spec's decisions 5 and 9 is restated.

### 2. The run is cold

`runs/.cache` and the three smoke directories — `runs/cold-smoke`, `runs/smoke-rerun`, `runs/smoke-rerun-2` — are deleted whole before the run, on 인지오's word. The smokes' record stays `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/`. `runs/integration-gate` stays. The run does not start with less than 273.5 GB free, the 10.4 record's upper disk projection.

### 3. The `random` condition's definition is confirmed

박이안 confirmed the RQ0 gate spec's `random-reading` statement — the reading of `random` and N = 100 — to 인지오 verbally (recorded 2026-11-15). The statement is restated to say so, and the memo that asked it, `docs/memos/2026-09-12-rq0-pre-registration.md`, is closed.

### 4. Guards before gaps

After the last run, the report, the runner's verdict line and its exit code stay unread until the blind reading of decision 5 is done. A failure the blind reading finds has its cause placed with the gaps unseen — by the 10.2 spec's procedure, the ratified contract deciding which side is wrong (`_dev/docs/spec/jioh/task-10.2-integration-gate.md`, decisions 13 and 14), with 인경민 when it is an executor question — and is fixed by a harness changelog entry; the affected runs are rerun; then the report is opened.

### 5. The blind reading

Three things, on the full run's runs:

- The guard table on the runs the criterion reads — on each of the 19 judging files, the primary boot default's `fixed` run, the `oracle` run and the 100 `random` seeds, 1,938 runs. A non-exempt failure there is what makes the verdict `invalid`.
- The longest-wait line's reopen condition as the RQ0 gate spec's `sensitivity-lines` statement states it: a judging file's run past 15 s, under every boot default but `ostep-slice-100000us`, reopens the executor-net question with 인경민 before the verdict is read.
- `simulator/tools/wait_check.py` on every trace, for the waits `starvation_floor` cannot read — one still open at the end, one after a preemption — with the thresholds of the 10.4 spec's decision 17: on a run the criterion reads, an unread wait over 30 s is handled as a `starvation_floor` failure is; past 15 s it reopens the question with 인경민; on any other file it is recorded with its run.

The wait check's rule is written into the RQ0 gate spec before the run.

### 6. One harness changelog entry and one re-pin before the run

The RQ0 gate spec's two pre-run edits — the wait check's rule (decision 5) and the `random-reading` statement (decision 3) — take one harness changelog entry and one re-pin.

### 7. Light use of the machine during the run

From the start to the end of the end stages the machine carries, beside the run, a terminal on the log and the conversation the run is started from. Nothing that builds or runs the harness, the harness suite or the simulator; no heavy browser use. The worker configuration is the smoke's. The memory pressure and the swap in use are recorded at the start, and the run's record states what ran beside the run.

### 8. An interruption with nothing changed resumes as the same run

A run stopped with no source changed is started again from its own caches, and is the same run. A resume is allowed only when the commit, the RQ0 gate spec's hash, the machine configuration and both program versions equal the first start's; otherwise it is refused. Every stop and start goes into the run's record with its time, the runs finished and the cause where known. No harness changelog entry.

### 9. The resume is exercised before the run

A kill and a resume are exercised once on the integration gate's short run — seven files, 28 runs — and the outputs compared byte for byte with an uninterrupted pass.

### 10. A failed run stops the run

At the first failed run the run is stopped, automatically, and the stop recorded. The failure is placed by the 10.2 spec's procedure. A source fix is made by a harness changelog entry and the run starts again; a failure with no source cause resumes under decision 8.

### 11. No stop on time

The run goes to its end however long it takes. A run that takes more than a stated multiple of its file's slowest smoke run is flagged — a reading of time alone — and recorded; it is profiled after the run, not during it. The Phase 10 spec's 80 hours stays the bound the projection was held against.

### 12. The report's place and form

`harness/experiments/rq0-gate/`, beside the RQ0 gate spec: the report gzipped, `report.json.gz`, and its rendering, `report.md`. Nothing else of the run directory is committed there. The run's operational files — its starts, stops and exit, its log, the blind reading's output, the run times — go into a research folder for task 10.5 under `_dev/research/jioh/`.

### 13. A hash manifest; nothing deleted by 10.5

One committed file beside the report lists every run's trace hash and records hash. The run's outputs stay on disk through the phase's close; their removal is a later decision.

### 14. The run's record

`docs/rq0-run-record.md`, status record, under the docs index's Research section. It holds what the Phase 10 spec's decision 8 lists — the dates, the machine, the cost, N and the changelog entries behind it, the verdict and the reporting lines — and with them the blind reading's outcome, every stop and start, what ran beside the run, the wall time and the disk against the projection, and the paths of the report and the hash manifest. A rerun after a blind fix is appended to it.

### 15. Both links' lines of `docs/research-claims.md` are restated

Link 1's line — there exist realistic situations where the correct config differs, and the difference is measurable — is restated to the criterion's reading: the verdict at the primary with its count, each axis over which the count ranges and whether the verdict holds across it, each axis not read. Link 2's line — some of those differences are invisible to behavioural observation — is restated to the headroom-count line's reading: the count, and stands or falsified. Outcomes only, in the RQ0 gate spec's terms; both cite the run's record.

### 16. The re-measurement contingency fired does not hold 10.5 open

If the carried-half-width lines move a judging file across g, 10.5 closes with the outcome recorded as provisional: the run's record and link 1's line state the verdict as a range over that axis, the contingency as fired, the entry owed, and the result as not final until the re-measurement. The re-measurement is a later phase, and the Phase 10 spec's out-of-scope list gains it.

### 17. A result memo of the RQ0 run

One memo to 인경민 and 박이안 under `docs/memos/`, in Korean, written after the run's record, on any outcome: the outcome in the RQ0 gate spec's terms, what it means for each owner's next work, and links to the run's record and the report.

## Invariants

- The report, the runner's verdict line and its exit code are not read before the blind reading is done.
- Nothing in the run changes after execution begins except by a harness changelog entry made before any run (the Phase 10 spec's invariant).
- No pre-run work changes the harness package's source: the run uses the harness source and the worker configuration of the smoke (the 10.4 spec's invariant).

## Open items

- Left to the implementation plan: how the verdict line and the exit code are kept out of sight; the multiple that flags a slow run, its reason from the smoke's run times; how the hash manifest is built.
- Left to the blind decision session of decision 4, with 인경민: a `random` seed's run on a judging file that fails `starvation_floor` through a configuration it drew, neither program at fault.
