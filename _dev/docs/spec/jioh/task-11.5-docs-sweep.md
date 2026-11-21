# Task 11.5 — The docs sweep

The sweep that closes Phase 11: the docs, the two guidebooks and the READMEs brought in line with what Phases 10 and 11 settled, and the TODO closed. Decided in the 2026-11-21 grill. Parent: `_dev/TODO.md`, (jioh, 11.5); phase spec `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 9.

## Scope

- Every statement under `docs/` that an item of decision 7's list overtakes, the research guidebook and the dataset guidebook included.
- The root `README.md` and every README under `harness/` and `dataset/`.
- The hold-time plan file, `_dev/docs/plan/jioh/hold-time-and-hysteresis.md`: its When table's row for the need measured with no rule, and its line on the backlog.
- The docs index, `docs/README.md`.
- `_dev/TODO.md` closed for Phase 11.

Out of scope: corrections inside a memo's or a record's body; `harness/CHANGELOG.md`; the simulator tree and the daemon tree; every other file under `_dev/`; new sections in any doc; a Phase 12 heading in `_dev/TODO.md`.

## Locked decisions

### 1. The sweep is by consequence

"The docs the phase changed" is every statement the phases' outcomes made false, whether or not Phase 11 edited the file that holds it.

### 2. Both guidebooks are in

The research guidebook (`docs/guidebook/vol-*`) and the dataset guidebook (`docs/guidebook/dataset/`) are swept like any other doc.

### 3. Phase 10's leftovers are searched for

The sweep searches against Phase 10's outcomes as well as Phase 11's, across everything in scope.

### 4. Memos and records: status only

No correction is added to a memo's or a record's body. For each memo, the open or closed line under its status header is checked against what Phases 10 and 11 settled, and the docs index's description of the memo is brought in line with it.

### 5. Prose outside `docs/`

The root `README.md` and every README under `harness/` and `dataset/` are searched against the same list. `harness/CHANGELOG.md` is left alone. The simulator tree and the daemon tree are left alone.

### 6. Absences

A false statement is corrected. A member the phases added is also added to a passage that enumerates — a list of the harness's tools, a table of blesses whose last row is labelled current, a count of phases, a list of an experiment folder's specs — at the level of detail its neighbours have. No new section is written.

### 7. What moved

A statement counts as overtaken only if one of these fifteen items overtakes it. Anything else found stale is listed in the sweep's record and left alone.

From Phase 10:

1. The RQ0 gate spec's pre-run lines: the headroom-count line, the statement `claim-links`, the cap band line (2026-11-01).
2. The integration gate passed on the real simulator and the real daemon (2026-11-14): the mocks out of the runner, `daemon/daemon.py` in the repository, conformance items (a) through (j) shown on the binary.
3. The simulator's stages by 인지오: stage AD, a schedule entry at or after the workload's end ignored; stage AE, the cap beside the idle class.
4. The unavailable rule: a reporting line that reads a gap from a failed run gives no reading.
5. The runner spreading runs over processes with a results cache; the run list of 19,425 runs; the starvation net reopened and settled.
6. The RQ0 run of 2026-11-16 to 2026-11-18 and every reporting line it carries, the trace-replay check and the carried-half-width lines among them; the re-measurement contingency fired.

From Phase 11:

7. The scorer's sign rule and the mark `oracle_worse`; the post hoc reading, 4 of 19 judging files meeting g and 12 of 19 with headroom.
8. The degraded oracle: fifteen cases, each a property of the configuration.
9. The simulator's stage AF, a fork-slot wait resetting the batch rule's counter, at `simulator@841dc81131cb`.
10. The re-measurement: `cpu-batch`'s `python3`, its two block values at 107 repeats, the campaign `meas-ci:background:2026-11-20`; the second bless.
11. The verdict final: fail, 5 of 19 against K = 10 on the RQ0 run's programs; 4 of 19 on the fixed programs.
12. The experiment lint reading an executed spec's pins as notes.
13. The configuration search — its search spec, its tool, its report — and the route: the table is rewritten; 8 of 10 files with spread the prior table missed, `c7-transcode` and `c7-gaming` with spread the row holds.
14. The hold-time plan's step 1 moved to after Phase 12's second RQ0 run.
15. Phase 12 as what comes next: the table rewrite, the second RQ0 gate spec, the second RQ0 run.

### 8. The TODO closed

As Phase 10 closed: 11.5's line ticked with its Done text, Phase 11 marked `[done]`, its whole section moved verbatim into `_dev/TODO-done.md`, one index line under the Done list. 인지오's Backlog lines are read against the fifteen items and restated where one overtakes them. No Phase 12 heading is written.

### 9. Open-spot boxes and "not yet run" markers

A box or marker whose matter the fifteen items closed is removed, and the passage states the outcome as ordinary text with its date and the record that holds it. Where part of the matter is still open, the box stays, narrowed to that part.

### 10. The work list comes first

Before any edit, the search runs over everything in scope and produces one work list in a research folder for 11.5. Each row carries the file and line, the statement as it stands, which of the fifteen items overtakes it, and the record the correction is taken from. Stale statements outside the fifteen items go in a separate part of the same list. 인지오 reviews the list before any edit.

### 11. Order of authority

For what a program does, the code and data as they stand. For a result or a count, the committed report or the RQ0 run record's latest dated entry. For a decision, the latest spec or changelog entry on it. The current docs and the tracker's done lines only say where to look. A number is written into a doc only if the row's named record holds it. A mismatch between code and record is logged for 인지오 and not resolved by the sweep.

### 12. Review, commit and the sweep's end

The work list's review also fixes the grouping of files into chunks, proposed from the counts. A fresh reviewer checks each chunk against its rows and their named records; the chunk is committed on the reviewer's pass. 인지오 reads afterwards, and anything he overturns becomes a new row. The sweep ends when every row is applied or marked left, a second search over the same terms finds nothing new, the `Updated` dates and the index lines are in line, and the suites that read a touched file pass.

### 13. `_dev/`: the hold-time plan file only

The hold-time plan file's When table row and its line on the backlog are restated to the Phase 11 spec's decision 10. Everything else under `_dev/` stays as it is. Another live plan found with an overtaken row goes in the work list's separate part for 인지오 to decide.

### 14. The decision chronicle: corrections only

In the dataset guidebook's chapter 8, section 12.4's eight items each keep their place and gain "closed" with the outcome, its date and its record, in the form chapter 3's list uses; the open-spot box under them follows decision 9; the sentences counting the phases and naming the dataset-related ones are corrected. No section is written for the re-measurement and the second bless. A Backlog line records that the chronicle has no section for them.

### 15. The memo is decided at the work list's review

No memo to 인경민 and 박이안 by default. If the work list holds a row that changes what a teammate would do, not only what a doc says, 인지오 decides at the list's review.

### 16. The work is on `main`

Every file in scope is prose; the sweep is done on `main`, with no worktree.
