# Task 11.5 work list — the docs sweep

Built 2026-11-21 at HEAD `f7d29b57` from eight readers' rows (`rows/`, one file per group) against the task spec `_dev/docs/spec/jioh/task-11.5-docs-sweep.md`. Each row in `rows/` carries the statement as it stands, what it becomes, and the record each fact is taken from.

## The search

Every file in scope was grepped, case-insensitive, extended regex:

```
Phase 1[0-2]|RQ0 (run|실행)|미실행|열린 자리|not yet|later phase|owed|pending|예정|headroom|claim-links|cap.band|link 2|integration gate|통합 gate|mock|daemon\.py|conformance|stage A[D-F]|sim_a[d-f]|unavailable|results cache|19,425|starvation|cold smoke|smoke|trace.replay|half.width|반폭|re-measure|재측정|contingency|verdict|provisional|of 19|oracle.worse|oracle_worse|post hoc|random.beats|degraded|fork.slot|fork_cap|rule B1|voluntary block|0d323c84470a|841dc81131cb|python3|MNIST|bless|meas-ci:background|machine spread|machine 따라|experiment.lint|configuration search|config search|search spec|route|rewritten|calibrated table|workload redesign|hold.time|hysteresis|flap|second RQ0|failure procedure|failure-procedure
```

and every hit's passage read; files under 400 lines read whole. The research guidebook was also searched for `RQ0`, `69`, `27.3`, `절댓값`, `하한`, `여유 없음`, `fork`, `B1`, `미정`, `확인 필요`. Enumerating passages were compared with the tree (`ls` of the harness's tool, test and experiment folders, `harness/Makefile`). The second search runs the same terms.

## Counts

246 rows: A (overtaken) 127, B (absence) 50, C (open-spot box or "not yet run" marker) 23, D (stale outside the fifteen items, left) 28, E (for 인지오) 18.

| disposition | rows |
|---|---|
| apply | 170 |
| waits on a question below | 47 (Q1 20, Q2 6, Q3 11, Q4 8, Q5 2) |
| left (D) | 28 |
| outside the sweep | 1 |

## Resolved at the merge

- **R1 — the per-statement checks are still owed by 인경민.** 9.16 decision 6 lists the compiled-number statements that wait on conformance items "as the check for 인경민 to run once each item lands" (`_dev/research/jioh/task-9.16-exit-audits/compiled/uncheckable-by-item.md`); every item has landed and no record holds the checks. g1-33, g2-08, g2-37, g3-24 keep their boxes, narrowed to those checks, owner 인경민. The ask is 9.16's, not new.
- **R2 — chapter 8's item 2 (Layer 1 and RQ4) moved, not closed.** Phase 10 spec decision 9: "The Layer 1 and RQ4 item of the old Phase 10 list moves to the Backlog, carried by the experiment specs its text names." g2-11 keeps its place and gains that outcome, in place of decision 14's "닫힘".
- **R3 — data read off the committed build.** Byte counts, instruction counts and manifest hashes no changelog lists are read off the artifacts and manifests whose hashes the committed manifests hold — spec decision 11, "for what a program does, the code and data as they stand": g1-10, g1-12, g1-13, g1-28, g2-31, g2-35, g4-02, g4-04, g4-06, g5-42, g7-04, g7-05, g7-06.
- **R4 — the measurement overview.** g7 found no row; g0-15, g0-16, g0-17 (lines 73, 79, 9) are added from g3-16, g3-17 and g4-26. g3-16 follows g0-16.
- **R5 — `c2-p1a`'s hog moved at the second bless.** g7-05 compiled the first bless's hog at `bb16f63a` (RUN 192, SLEEP 378); the committed build holds RUN 191, SLEEP 472. g5-42 is an A row on item 10.
- **R6 — partial rows.** g5-32 and g5-40 apply their overtaken clause (the response to a narrow gap; "will run"); the outcome each adds waits on Q3.
- **R7 — g5-27** names the second RQ0 gate spec as where an added analysis would be settled; item 15 names that spec as Phase 12's.

## Questions for 인지오

- **Q1 — lists that also lack members from outside the fifteen items.** g1-01, g1-03, g1-26, g1-32, g1-40, g2-01, g2-06, g2-07, g2-23, g2-24, g2-27, g2-29, g3-05, g3-07, g3-21, g3-22, g4-09, g4-12, g4-13, g4-27. g2-01 and g2-24 apply their phase count regardless. **Decided (인지오, 2026-11-21): by date.** An explicitly dated list stays as it is — g1-26, g3-05, g3-07, g3-21, left. A list that presents itself as current or whole gains the item member and every older member it lacks, each from its record, this sweep's own pass among them in the guidebook's lists of its correction passes — the other sixteen, applied.
- **Q2 — corrections that stay false without a fact from outside the fifteen items.** g1-06, g1-25, g1-36, g2-31, g2-35, g3-17. **Decided (인지오, 2026-11-21): the outside fact or fix is included** wherever the corrected passage would otherwise stay false, each from its record — applied.
- **Q3 — passages where nothing is false but the run's outcome, the route or Phase 12's table is absent.** g1-39, g4-10, g4-11, g4-25, g5-11, g5-12, g5-16, g5-30, g5-37, g5-38, g6-02, and the outcome halves of g5-32 and g5-40. **Decided (인지오, 2026-11-21): left**, the rows kept here for Phase 12's spec session — but for one verb: in g5-12, `vol-03-the-research.md:2442`'s "RQ0의 문을 이 표로 통과한다" becomes "시험한다"; the rest of g5-12 and the passages at 2631, 3188 and 3755 stay.
- **Q4 — passages that may not enumerate.** g2-03, g2-25, g4-08, g4-28, g5-39, g6-06, g6-10, g6-12. **Decided (인지오, 2026-11-21): left** — none presents itself as the whole set.
- **Q5 — the three memos with no open-or-closed line.** g0-08 and its index lines g0-06. **Decided (인지오, 2026-11-21): added** — each memo's line, in its language, names the asks of its §1 still open, owner 인경민; the two earlier memos' rebuild ask points to the 2026-11-19 memo's `simulator@841dc81131cb`; the 2026-11-15 memo's §1 item 3 is named as a standing rule; the index's three Open lines gain the clause — applied.
- **Q6 — the memo to 인경민 and 박이안** (decision 15). No row changes what either does: the rows with a teammate side restate asks already sent (R1, Q5). **Decided (인지오, 2026-11-21): no memo.**
- **Q7 — the chunks and waves** below. **Decided (인지오, 2026-11-21): as drafted.**

Under Q1, the lists of the phases "directly related to the dataset" (g1-40, g2-01, g2-24) gain Phase 10 — the 2026-10-31 rebuilds are its item ("The Phase 10 item 'Timer wakes that find their task behind'", `_dev/docs/spec/jioh/timer-wakes-by-origin.md`, line 3) — and Phase 11 (11.3's re-measurement and second bless).

## Outside the sweep, for 인지오

- `harness/CHANGELOG.md`, 2026-11-14 "the rows' table column takes a cap-band run's label": its test is said to run "through the real programs"; `test_runner.py` builds its machine from `runner.example.yaml`, the mocks (g1-20).
- `dataset/archetypes.yaml`, `cpu-batch` `scope`: its first sentence says each program's values come from 9.10's own campaign, a later one that two are 11.3's (g4-26).
- `daemon/README.md` (박이안's tree) calls the mock daemon "the harness's reference mock" (g2-34).
- No build release holds the second bless's build; the root README names `dataset-build-2026-10-26` (g7-32).
- `dataset/tools/end_bound.py` fails with `IndexError` on the current artifacts, `c1-render` included (g4-14).
- 인경민's Backlog intro in `_dev/TODO.md` names stages AD and AE as 인지오's and not AF (g0-11).
- The rebuild memo's open regression check looks answered by 인경민's stage-port regressions, `src/sim == steps/sim_y` 129/129 (g0-10).
- No record names a Linux CI run on the 2026-10-31 or 2026-11-21 manifests (g1-18, g1-19, g1-29).

## Chunks and waves

A chunk owns its files; no two chunks share one. An editing agent applies the chunk's rows; a fresh reviewer checks them against their rows and records; the main session commits each chunk on its reviewer's pass.

| chunk | files | rows to apply |
|---|---|---|
| K1 · Dataset guidebook 7 and 1 | `07-build-gate-manifests-ci-tests.md`, `01-the-big-picture.md` | g1 |
| K2 · Dataset guidebook 8 and 3 | `08-decision-chronicle.md`, `03-timeline-to-canonical-workload.md` | g2 |
| K3 · Dataset guidebook 5 and 6 | `05-the-generated-layer.md`, `06-grounding-measurement-verification.md` | g3 |
| K4 · Dataset guidebook 2, 4 and README | `02-the-archetype-library.md`, `04-the-coreset.md`, `guidebook/dataset/README.md` | g4 |
| K5 · Research guidebook | `docs/guidebook/vol-01` … `vol-06` | g5-01 – g5-27 |
| K6 · Research docs | `research-claims.md`, `research-proposal.md`, `terminology.md`, `background-guide.md`, `related-work.md` | g5-28 – g5-43 |
| K7 · Harness | `docs/harness/` and the READMEs under `harness/` | g6 |
| K8 · Workload, contracts, daemon, dataset READMEs | `docs/workload/` (the overview's three rows with them), `docs/data-contracts.md`, `docs/daemon/daemon-guide.md`, `dataset/README.md`, `dataset/tools/meas/README.md` | g7, g0-15 – g0-17 |
| K9 · Index, memo status lines, hold-time plan file | `docs/README.md`, the memos' status lines, `_dev/docs/plan/jioh/hold-time-and-hysteresis.md` | g0-01 – g0-14 |

Wave 1: K1–K4. Wave 2: K5–K8. Wave 3: K9, its index lines read against the edits before it; then the TODO closed (decision 8) and the second search.

## Rows by file

| file | apply | waits on a question | left |
|---|---|---|---|
| `README.md` |  |  | g7-32 |
| `_dev/TODO.md` |  |  | g0-11, g0-12 |
| `_dev/docs/plan/jioh/hold-time-and-hysteresis.md` | g0-13, g0-14 |  |  |
| `dataset/README.md` | g7-27, g7-28, g7-29 |  | g7-30 |
| `dataset/archetypes.yaml` |  |  | g4-26 (outside the sweep) |
| `dataset/tools/meas/README.md` | g7-31 |  |  |
| `docs/README.md` | g0-01, g0-02, g0-03, g0-04, g0-05 | Q5: g0-06 |  |
| `docs/background-guide.md` | g5-40, g5-41, g5-42 |  |  |
| `docs/daemon/daemon-guide.md` | g7-21, g7-22, g7-23, g7-24, g7-25, g7-26 |  |  |
| `docs/data-contracts.md` | g7-13, g7-14 |  | g7-15, g7-16 |
| `docs/guidebook/dataset/01-the-big-picture.md` | g1-27, g1-28, g1-29, g1-30, g1-31, g1-33, g1-34, g1-35, g1-37, g1-38 | Q1: g1-26, g1-32, g1-40; Q2: g1-25, g1-36; Q3: g1-39 |  |
| `docs/guidebook/dataset/02-the-archetype-library.md` | g4-15, g4-16, g4-17, g4-18, g4-20, g4-21, g4-22, g4-23, g4-24 | Q3: g4-25 | g4-19 |
| `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` | g2-28, g2-30, g2-32, g2-33, g2-34, g2-36, g2-37, g2-38 | Q1: g2-27, g2-29; Q2: g2-31, g2-35 |  |
| `docs/guidebook/dataset/04-the-coreset.md` | g4-01, g4-02, g4-03, g4-04, g4-05, g4-06, g4-07 | Q1: g4-09, g4-12, g4-13; Q3: g4-10, g4-11; Q4: g4-08 | g4-14 |
| `docs/guidebook/dataset/05-the-generated-layer.md` | g3-01, g3-02, g3-03, g3-04, g3-08, g3-09 | Q1: g3-05, g3-07 | g3-06 |
| `docs/guidebook/dataset/06-grounding-measurement-verification.md` | g3-10, g3-11, g3-12, g3-13, g3-14, g3-15, g3-16, g3-18, g3-19, g3-20, g3-23, g3-24, g3-25 | Q1: g3-21, g3-22; Q2: g3-17 |  |
| `docs/guidebook/dataset/07-build-gate-manifests-ci-tests.md` | g1-02, g1-04, g1-05, g1-07, g1-08, g1-09, g1-10, g1-11, g1-12, g1-13, g1-14, g1-15, g1-16, g1-17, g1-18, g1-19, g1-20, g1-21, g1-22 | Q1: g1-01, g1-03; Q2: g1-06 | g1-23, g1-24 |
| `docs/guidebook/dataset/08-decision-chronicle.md` | g2-04, g2-05, g2-08, g2-09, g2-10, g2-11, g2-12, g2-13, g2-14, g2-15, g2-16, g2-17, g2-18, g2-19, g2-20, g2-21 | Q1: g2-01, g2-06, g2-07, g2-23, g2-24; Q4: g2-03, g2-25 | g2-02, g2-22, g2-26 |
| `docs/guidebook/dataset/README.md` |  | Q1: g4-27; Q4: g4-28 |  |
| `docs/guidebook/vol-01-systems-and-scheduling.md` | g5-01 |  |  |
| `docs/guidebook/vol-02-related-work.md` | g5-02 |  |  |
| `docs/guidebook/vol-03-the-research.md` | g5-04, g5-05, g5-06, g5-07, g5-08, g5-09, g5-10, g5-14, g5-15, g5-17 | Q3: g5-11, g5-12, g5-16 | g5-03, g5-13 |
| `docs/guidebook/vol-04-experiment-design.md` | g5-18, g5-19, g5-20, g5-21, g5-22, g5-24, g5-25 |  | g5-23 |
| `docs/guidebook/vol-05-shared-vocabulary.md` | g5-26 |  |  |
| `docs/guidebook/vol-06-archetypes-and-grounding.md` | g5-27 |  |  |
| `docs/harness/harness-and-records-guide.md` | g6-01 | Q3: g6-02 | g6-22 |
| `docs/harness/metrics.md` | g6-03 |  |  |
| `docs/memos/`, three memos (2026-11-13, 2026-11-15, 2026-11-19) |  | Q5: g0-08 |  |
| `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` | g0-07 |  |  |
| `docs/memos/2026-10-17-workload-dataset-rebuild.md` |  |  | g0-10 |
| `docs/recognition-vocabulary.md` |  |  | g7-17 |
| `docs/related-work.md` | g5-43 |  |  |
| `docs/research-claims.md` | g5-28, g5-29 |  |  |
| `docs/research-proposal.md` | g5-32, g5-33, g5-34, g5-35 | Q3: g5-30 | g5-31 |
| `docs/simulator/simulator-guide.md` |  |  | g7-18, g7-19, g7-20 |
| `docs/terminology.md` |  | Q3: g5-37, g5-38; Q4: g5-39 | g5-36 |
| `docs/workload/archetype-plan.md` | g7-12 |  |  |
| `docs/workload/building-plan.md` | g7-10, g7-11 |  |  |
| `docs/workload/coreset-guide.md` | g7-01, g7-02, g7-03, g7-04, g7-05, g7-06, g7-07, g7-08, g7-09 |  |  |
| `docs/workload/measurement-overview.md` | g0-15, g0-16, g0-17 |  |  |
| `harness/README.md` | g6-04, g6-05, g6-07 | Q4: g6-06 |  |
| `harness/experiments/README.md` | g6-08, g6-09, g6-11 | Q4: g6-10 | g6-21, g6-23 |
| `harness/guards/README.md` |  | Q4: g6-12 |  |
| `harness/tools/README.md` | g6-13, g6-14, g6-15, g6-16 |  |  |
| `harness/tools/harness/README.md` | g6-17, g6-18 |  |  |
| `harness/tools/tests/README.md` | g6-19 |  | g6-24 |
| `harness/tools/tests/fixtures/README.md` | g6-20 |  |  |
