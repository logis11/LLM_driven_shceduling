# Rows — g0, the docs index, the memos' status lines, the TODO Backlog, the hold-time plan file

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/README.md` | 180 | 29, and every memo line | 4/2/0/0/0 |
| `docs/memos/*.md`, the line under each status header (decision 4) | 25 memos | 25 | 1/3/0/1/0 |
| `_dev/TODO.md`, 인지오's Backlog (decision 8) | 7 lines | 7 | 0/0/0/1/0 |
| `_dev/docs/plan/jioh/hold-time-and-hysteresis.md` (decision 13) | 44 | 14 | 2/0/0/0/0 |
| `docs/workload/measurement-overview.md`, added at the merge | 229 | 3 | 3/0/0/0/0 |

## The docs index

### g0-01 · `docs/README.md:40` · A · items 7 (the sign rule), 8 (the degraded oracle), 10 (the re-measurement), 11 (the verdict final), 13 (the configuration search)
- **Now:** "the verdict (fail at the primary, 6 of 19 against K = 10; a range over g; provisional, the re-measurement contingency fired) and every reporting line, the report's and the hash manifest's paths"
- **Becomes:** the verdict as run (fail at the primary, 6 of 19 against K = 10; a range over g; provisional, the re-measurement contingency fired) and every reporting line; its dated corrections — the scorer's sign and the post hoc reading (4 of 19), the fork-slot wait, the re-measurement and the verdict final, fail, 5 of 19 against K = 10; the failure procedure's configuration search and its route, the table rewritten; the reports' and the hash manifests' paths
- **From:** `docs/rq0-run-record.md`, "Corrections" — 2026-11-18 (line 123), 2026-11-20, 2026-11-21 (line 192); "The failure procedure" (line 204)

### g0-02 · `docs/README.md:124` · B · items 7, 8, 10, 11, 13
- **Now:** "| the RQ0 run: its dates, machine, cost, blind reading, verdict and reporting lines | record |"
- **Becomes:** the list of what the record holds gains its corrections, the verdict final and the failure procedure's search and route
- **From:** `docs/rq0-run-record.md`, the `##` sections "Corrections" and "The failure procedure"

### g0-03 · `docs/README.md:115` · A · items 7 (the sign rule), 11 (the verdict final)
- **Now:** "the RQ0 run's result — FAIL at the primary, 6 of 19 against K = 10, provisional on the re-measurement contingency; PASS at g = 0.25; link 2 standing, 17 of 19 with headroom; what 인지오 does next — 10.6, then the failure procedure and the re-measurement in a later phase. Closed: no ask; the outcome is in `rq0-run-record.md`"
- **Becomes:** the memo's description as written, then its two dated corrections: the scorer's sign (2026-11-18; the post hoc reading, 4 of 19, 12 of 19 with headroom) and the re-measurement (2026-11-21; the verdict final, fail, 5 of 19 against K = 10). The closed clause stays
- **From:** `docs/memos/2026-11-18-rq0-run-result.md`, "정정 (2026-11-18)" (line 28) and "정정 (2026-11-21)" (line 41); `docs/rq0-run-record.md`, lines 123, 124, 192

### g0-04 · `docs/README.md:113` · A · items 1 (the pre-run lines), 6 (the RQ0 run)
- **Now:** "… and the concern that they are design — nine judging files on the cap-0.05 MLFQ rows — answered by a cap band line planned for the RQ0 gate spec. Closed 2026-10-21: …"
- **Becomes:** "… answered by the cap band line the RQ0 gate spec carries since 2026-11-01, which the RQ0 run read …" — "planned" is overtaken; the as-run count, if the line states one, is 6, 6, 7, 7 of 19 at 0.05, 0.2, 0.333, 0.5 (fail)
- **From:** `harness/CHANGELOG.md`, 2026-11-01; `docs/rq0-run-record.md`, "The reporting lines", line 88

### g0-05 · `docs/README.md:94` · A · item 2 (the integration gate passed)
- **Now:** "Open: three of §6's simulator items — `x_mlfq_level` with levels on every demotion and boost, the settled rules in the simulator's semantics notes, the test that remaining demand is conserved across a switch; owner 인경민"
- **Becomes:** "Open: two of §6's simulator items — `x_mlfq_level` …, the settled rules in the simulator's semantics notes; owner 인경민. The test that remaining demand is conserved across a switch is done since 2026-11-11 (`simulator/tests/test_switch_demand.py`, 인경민's commit `2ee49785`) and passed on the binary in the integration gate (2026-11-14)"
- **From:** `git log -- simulator/tests/test_switch_demand.py` (`2ee49785`, 2026-11-11, 인경민); `_dev/research/jioh/task-10.2-integration-gate/README.md`, line 7 (the seven unit tests on `simulator@0d323c84470a`); `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md`, line 51

### g0-06 · `docs/README.md:97, 98, 99` · B · items 3 (stages AD and AE), 2 (the integration gate), 9 (stage AF)
- **Now:** the three Open lines for `2026-11-13-simulator-changes-by-jioh.md`, `2026-11-15-integration-gate-and-cold-smoke.md` and `2026-11-19-simulator-changes-by-jioh.md` carry no "Open: …; owner …" clause, the form every other Open line has
- **Becomes:** each gains its clause, taken from the status line g0-08 adds to the memo
- **From:** each memo's "## 1. 경민이 할 일"; g0-08

## The memos' status lines (decision 4)

### g0-07 · `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md:4` · A · item 2 (the integration gate passed)
- **Now:** "> Open — of §6's simulator side, three items are owed: `x_mlfq_level {t, task, from, to}` on every demotion and boost …, the three settled rules written into the simulator's semantics notes, and the unit test that remaining demand is conserved across a switch, as the simulator's own record keeps them open (`simulator/memo/memo_261010.md` Part D, D2–D4); owner 인경민."
- **Becomes:** two items owed (`x_mlfq_level`, the semantics notes); the test done since 2026-11-11 (`simulator/tests/test_switch_demand.py`, `2ee49785`) and passed on the binary in the integration gate (2026-11-14). The status line only; no body correction
- **From:** as g0-05

### g0-08 · `docs/memos/2026-11-13-simulator-changes-by-jioh.md:4`, `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md:4`, `docs/memos/2026-11-19-simulator-changes-by-jioh.md:4` · B · items 3, 2, 9
- **Now:** no open-or-closed line under the status header, where the memo rule puts it (`docs/README.md:89`); the index lists all three as Open
- **Becomes:** a line under each header, in the memo's language, from its own §1 ("경민이 할 일"):
  - 2026-11-13: 열림 — 단계 AD와 AE를 읽는 일(§1의 2); batch-class 메모 §7의 항목 5(§1의 3)는 그 메모가 열어 둬요; 다시 build하는 일(§1의 1)은 2026-11-19 memo §1이 `simulator@841dc81131cb`로 이어받아요; 담당 인경민
  - 2026-11-15: 열림 — 새 unit test와 mutant를 읽는 일(§1의 2); §1의 3(source를 고치면 알리는 일)은 계속 지키는 규칙; 다시 build하는 일은 2026-11-19 memo §1이 이어받아요; 담당 인경민
  - 2026-11-19: 열림 — 다시 build하고(`simulator@841dc81131cb`) 단계 AF를 읽는 일(§1의 1과 2); batch-class 메모 §7의 항목 5는 그 메모가 열어 둬요; 담당 인경민
- **From:** each memo's "## 1. 경민이 할 일" (2026-11-13 lines 16–27; 2026-11-15 lines 17–29; 2026-11-19 lines 14–25); no commit by 인경민 in `simulator/` since 2026-11-13 (`git log --since=2026-11-13 -- simulator`)
- **Flags:** for 인지오 — the three lines restate asks already sent, not new ones; whether the 2026-11-13 and 2026-11-15 rebuild instructions read as handed on to the 2026-11-19 memo is yours to confirm

### g0-09 · `docs/memos/2026-10-20-batch-class-and-cap.md`, its index line (`docs/README.md:113`) · see g0-04
- The memo's own line ("닫힘 (2026-10-21) — … 남은 것은 (d)에 기대는 문장들의 확인이에요(§4)") is in line; the index line's "planned" is g0-04.

## The separate part — outside the fifteen items or outside the scope, left alone

### g0-10 · `docs/memos/2026-10-17-workload-dataset-rebuild.md:4` · D
- **Now:** "열림 — 인경민: rebuild된 core set에서 regression check와 EDF 재측정(§6.3)…"
- **Why left:** §6.3's regression check (the 51 core files and 78 variants) looks answered by 인경민's own stage-port regressions on the rebuilt build — `src/sim == steps/sim_y` 129/129 (2026-10-23, 인경민's TODO 1.6) — before Phase 10 and outside the fifteen items. The EDF re-measurement is still open on 인경민's Backlog.

### g0-11 · `_dev/TODO.md:53` (인경민's Backlog intro) · D, outside the scope (decision 13)
- **Now:** "Stages AD, the data contracts' End rule, and AE, the cap beside the idle class, were written by 인지오 on 2026-11-13 (memo_261111 Parts K and L)."
- **Why left:** stage AF, also 인지오's (2026-11-19, `simulator@841dc81131cb`), is not named; the line is in 인경민's tracking section, which the sweep does not touch.

### g0-12 · `_dev/TODO.md`, 인지오's Backlog, seven lines · D (none overtaken)
- Read against the fifteen items: the naturalistic generator; hold time step 1 (already restated to Phase 11 spec decision 10); hold time steps 2, 4, 5, 6; the form-2 return grid; unwanted jobs to measure ("after Phase 10's RQ0 run and before the RQ1 run" still holds); the held-out-rows arm ("on the calibrated table" — whether Phase 12's rewrite is that table is Phase 12's to decide); the Layer-1 and RQ4 items of 9.12. None is overtaken. Decision 14 adds one line at the close: the decision chronicle has no section for the re-measurement and the second bless.

## Added at the merge — `docs/workload/measurement-overview.md`

g7 read the overview and found no row; g3 (g3-16, g3-17) and g4 (g4-26) pointed at the three lines below, read again at the merge.

### g0-15 · `docs/workload/measurement-overview.md:73` · A · item 10 (the re-measurement)
- **Now:** "Over the campaigns behind the dataset's values, 40–83 % of a campaign's jobs drew it."
- **Becomes:** 15.7–83 % — 11.3's campaign, now behind two of `cpu-batch`'s values, drew the AMD EPYC 7763 on 107 of its 680 jobs
- **From:** `_dev/research/jioh/measurement-campaign-record.md`, "Machine draws", line 564 ("680 jobs — 107 landed on the AMD EPYC 7763 (15.7 %, all pooled)")

### g0-16 · `docs/workload/measurement-overview.md:79` · A · item 10 (the re-measurement)
- **Now:** "… and the campaigns' counts are 5 to 77."
- **Becomes:** 5 to 107
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, "The campaign" (107 fresh repeats)

### g0-17 · `docs/workload/measurement-overview.md:9` · A · item 10 (the re-measurement)
- **Now:** "Every number of one archetype comes from one observation: … — for `cpu-batch`, of each of its two programs, each in its own campaign. Where a phase was measured again, the entry's scope names the campaign each phase's values come from (`mail-client` and `video-editor`: …)"
- **Becomes:** the "measured again" clause gains `cpu-batch`'s `python3`: its run between voluntary blocks and its block per run from 11.3's campaign (`meas-ci:background:2026-11-20`), every other value from 9.10's (`meas-ci:background:2026-10-03`), as the entry's scope names
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `scope` (lines 1288–1293) and `params` (`python3_run`, `python3_block`, `source: "meas-ci:background:2026-11-20"`)

## The hold-time plan file (decision 13)

### g0-13 · `_dev/docs/plan/jioh/hold-time-and-hysteresis.md:12` · A · item 14 (the hold-time plan's step 1 moved)
- **Now:** "| 0, the need measured with no rule | right after Phase 10's integration, in the RQ0 run's pipeline | …"
- **Becomes:** "| 0, … | after Phase 12's second RQ0 run, on the table and programs that run uses (Phase 11 spec, decision 10) | …" — the needs column unchanged
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10

### g0-14 · `_dev/docs/plan/jioh/hold-time-and-hysteresis.md:15` · A · item 14
- **Now:** "Both later blocks are on the Phase 10 backlog in `_dev/TODO.md`."
- **Becomes:** both blocks are on 인지오's Backlog in `_dev/TODO.md`
- **From:** `_dev/TODO.md`, 인지오's `### Backlog`, lines 32–33
