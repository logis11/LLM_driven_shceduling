# Rows — g4, dataset guidebook chapters 4 and 2, and its README

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/guidebook/dataset/04-the-coreset.md` | 2385 | 89 | 6/3/1/1/3 |
| `docs/guidebook/dataset/02-the-archetype-library.md` | 1715 | 75 | 7/2/0/1/2 |
| `docs/guidebook/dataset/README.md` | 36 | 1 | 0/1/0/0/1 |

The current values of `cpu-batch`'s `python3` were taken from the RQ0 run record's 2026-11-21 correction, `dataset/archetypes.yaml` (`cpu-batch`), `dataset/variants.yaml` (`carried_values`) and `dataset/meas-releases.yaml`. Three byte counts were read from the built artifacts under `dataset/build/coreset-single/`. Each artifact's SHA-256 equals its entry in the committed `dataset/build.manifest.json`.

## Chapter 4 — the coreset

### g4-01 · `docs/guidebook/dataset/04-the-coreset.md:215` · A · item 6 (the RQ0 run), item 11 (the verdict final)
- **Now:** "core set 51개가 모두 같은 무게로 쓰이는 것은 아닙니다. 가장 먼저 돌 실험인 RQ0 gate에서는 19개만 판정에 쓰입니다."
- **Becomes:** 가장 먼저 돈 실험인 RQ0 run(2026-11-16–18, cold, RQ0 gate spec의 full matrix 19,425 run)에서는 19개만 판정에 쓰였음. 같은 문단 끝에 한 문장을 덧붙임: 판정은 fail이고, 2026-11-21에 final로 정해짐 — 19개 중 5개(`c2-p2a`, `c2-p2b`, `c1-ml-train`, `c7-browsing`, `c7-office`)가 g를 넘음, K = 10. 실행 당시의 판정(fail, 19개 중 6개, provisional)은 run 자신의 기록으로 남음.
- **From:** `docs/rq0-run-record.md`, "The run" (the started and finished rows, runs 19,425); "Corrections", 2026-11-21, the line "The verdict, final in place of provisional"; "Corrections", 2026-11-18, the line "The verdict above stands as run: fail, 6 of 19, provisional"

### g4-02 · `docs/guidebook/dataset/04-the-coreset.md:793` · A · item 10 (the re-measurement and the second bless)
- **Now:** "**compile된 모양.** arrive 2개, wake 184,268개(timer 181,454, event 830, input 1,984), 24,217,560 byte, utilization 0.9982."
- **Becomes:** 24,217,608 byte. 나머지(arrive 2개, wake 수, utilization 0.9982)는 둘째 bless 뒤에도 그대로임.
- **From:** `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json`, `build.manifest.json`'s `beyond_hash` (lists this file) and `demand_moves` (empty). The size is that of `dataset/build/coreset-single/c1-ml-train.workload.json`, whose SHA-256 `1e7ef444…` equals its entry in `dataset/build.manifest.json`. Its wake counts were recounted from the same file, and its utilization is the manifest's `demand` entry.
- **Flags:** for 인지오: no record states the byte count. It is read off the blessed artifact (spec decision 11: "for what a program does, the code and data as they stand"). The +48 bytes match `c7-ml-train`'s (g4-06), whose pre-bless size is confirmed by 11.3's control build.

### g4-03 · `docs/guidebook/dataset/04-the-coreset.md:797–800` · B · item 10 (the re-measurement and the second bless)
- **Now:** "**정한 결정.** … - 9.10 D85(training run은 `cpu-batch`의 `python3` program을 다시 측정한 것), D90(campaign `meas-ci:background:2026-10-03`이 반복 6회에서 안정, CPU 총량 1,389.885 s ±4.04 %, 2026-10-03). … - segment 1,612 s는 2.6절의 산술(…)입니다."
- **Becomes:** add one bullet beside D85/D90, at their level of detail: 2026-11-21, 11.3(RQ0 run의 carried-half-width line이 움직인 값을 다시 잰 Phase 11 sub-task). training run의 voluntary block 사이 run과 run당 block을 같은 job의 107 repeat로 다시 잼(`meas-ci:background:2026-11-20`): 55.27 s ±5.89 %, 403.96 µs ±2.15 %. 둘 다 예외 class는 그대로임. CPU 총량은 9.10 campaign의 1,389.885 s를 그대로 둠(107 repeat에서 1,413.843 s ±0.34 %로 읽혀, 실린 값의 구간 안). 이 파일은 둘째 bless로 다시 build됨.
- **From:** `docs/rq0-run-record.md`, "Corrections", 2026-11-21: "The campaign" paragraph and its table, and the sentence "Both values keep their exception class. The CPU total … read 1,413.843 s ±0.34 %, inside its interval"; `dataset/archetypes.yaml`, `cpu-batch` `validation_stats.scope` (lines 1288–1293)

### g4-04 · `docs/guidebook/dataset/04-the-coreset.md:982` · A · item 10 (the re-measurement and the second bless)
- **Now:** "**compile된 모양.** arrive 2개, wake 11,293개(timer 10,740, event 28, input 525), 1,471,142 byte. utilization은 파일 14.505, segment 0 0.5272, segment 1 35.7721입니다."
- **Becomes:** 1,472,070 byte. 나머지(wake 수와 utilization)는 그대로임.
- **From:** `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json`, `build.manifest.json`'s `beyond_hash` (lists `c2-p1a`) and `demand_moves` (empty). The size is that of `dataset/build/coreset-single/c2-p1a.workload.json`, whose SHA-256 `0678efa6…` equals its entry in `dataset/build.manifest.json`. Its utilization is the manifest's `demand` entry.
- **Flags:** for 인지오: as g4-02, the number comes from the artifact and not from a record. Line 1007 (`c2-p1b`'s "`c2-p1a`와 같은 수" wakes) stays true.

### g4-05 · `docs/guidebook/dataset/04-the-coreset.md:1571` · C · item 5 (the runner and the cost)
- **Now:** "> **열린 자리.** 이 파일은 시뮬레이션 비용이 큽니다. 9.14 D13–D14와 그 handoff는 `c6-dual` 한 run의 records build가 mock trace에서 약 40분 … 2026-10-16에 인지오는 대응을 지금 고르지 않고 Phase 10에서 실제 simulator의 측정된 비용을 보고 정하기로 했습니다. 더 싼 records 경로, … N의 변경 …, 또는 비용을 그대로 지는 것 가운데 하나입니다(`_dev/TODO.md`의 Phase 10 줄). 이 파일은 보고 파일입니다."
- **Becomes:** the box goes, and its matter is stated as plain text. 이 파일은 시뮬레이션 비용이 가장 큰 파일임(9.14 D13–D14: records build 약 40분, swap). Phase 10의 cold smoke와 비용 대응(10.4, 2026-11-14–15)에서 records를 trace에서 만드는 길이 바뀜. `c6-dual`의 `fixed` run은 build 213 s, write 110 s, aggregates 124 s, 최고 9.4 GB가 됨(그 전에는 15 GB를 넘어 swap). runner는 heavy run을 한 번에 하나씩 돌림(`heavy_workers` 1). 비용은 N = 100 그대로 지기로 함(2026-11-15; 전체 run의 위쪽 추정 50.33 h 가운데 `c6-dual`이 30.59 h). RQ0 run은 45 h 26 min에 끝남. 이 파일은 보고 파일임.
- **From:** `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`, the paragraph after the first table (`c6-dual`'s `fixed` run, its records), the worker configuration's `heavy_mb` and `heavy_workers` lines, and "The cost is carried (decision 13) … `c6-dual`, 30.59 h over its 112 runs"; `harness/CHANGELOG.md`, the 2026-11-15 entry "the cost response…"; `docs/rq0-run-record.md`, "The run" (machine row; finished row, 45 h 26 min)

### g4-06 · `docs/guidebook/dataset/04-the-coreset.md:1824–1826` · A · item 10 (the re-measurement and the second bless)
- **Now:** "… arrive 2개, wake 158,589개(timer 156,109, event 727, input 1,753), 20,825,630 byte, utilization 1.1405. …" and "… venue 둘, corner 둘의 variant가 붙고, corner는 training run의 두 block 값(`python3_run` ±27.3 %, `python3_block` ±10.8 %)을 움직입니다."
- **Becomes:** 20,825,678 byte (wake 수와 utilization은 그대로임). corner는 training run의 두 block 값(`python3_run` ±5.89 %, `python3_block` ±2.15 %, 2026-11-21에 11.3이 107 repeat로 다시 잰 반폭)을 움직임.
- **From:** `dataset/variants.yaml`, `carried_values`, the two `cpu-batch` rows (lines 132–135); `bless-report.json` (`beyond_hash` lists `c7-ml-train`); `dataset/build/coreset-single/c7-ml-train.workload.json`, whose SHA-256 `5465ad62…` equals its entry in `dataset/build.manifest.json`. 11.3's control build `_dev/research/jioh/task-11.3-the-re-measurement/finding/build/controls/c7-ml-train.workload.json` (local only; `finding-builds.json`, "nothing-moved") is byte-identical to the first bless and is 20,825,630 bytes, the value the guidebook states.

### g4-07 · `docs/guidebook/dataset/04-the-coreset.md:1934–1955` · A · item 10 (the re-measurement and the second bless)
- **Now:** "| `cpu-batch` (`python3`) | `python3_run` | 27.3 % | 9.10 D87, D88 |" / "| `cpu-batch` (`python3`) | `python3_block` | 10.8 % | 같음 |", and line 1934's history "2026-10-17에 … 열다섯 줄에서 열아홉 줄이 되었습니다 …"
- **Becomes:** `python3_run` 5.89 %, `python3_block` 2.15 %. 출처 결정 칸: 11.3의 재측정(`meas-ci:background:2026-11-20`; 9.10 D87, D88, 9.6 D29의 예외). Line 1934 gains one sentence: 2026-11-21에 `cpu-batch` `python3`의 두 줄이 11.3의 재측정 값으로 바뀜(줄 수는 열아홉 그대로).
- **From:** `dataset/variants.yaml`, `carried_values`, lines 132–135 (half-widths 0.0589 and 0.0215, their `source` strings); `harness/CHANGELOG.md`, the 2026-11-21 re-measurement entry, "The fold-in" bullet

### g4-08 · `docs/guidebook/dataset/04-the-coreset.md:1964` · B · item 4 (the unavailable rule)
- **Now:** "읽는 규칙은 statement `sensitivity-lines`에 있습니다. \"A verdict count that moves under any line makes the verdict a range over that axis.\" 어떤 line에서 통과 파일 수가 바뀌면, RQ0의 결론은 하나의 판정이 아니라 그 축 위의 범위로 보고된다는 뜻입니다."
- **Becomes:** add the statement's second reading rule, one sentence. 2026-11-14부터 같은 statement는 gap을 읽는 모든 line(variant line의 count, trace replay의 일치, bounding pair의 차이 등)에 규칙 하나를 둠. 그 line이 읽는 run에 면제되지 않은 guard 실패가 있으면 그 gap은 unavailable임. 그러면 line은 읽히지 않고, 판정은 그 축에서 "읽지 않음"으로 적힘. RQ0 run에서는 chain 배율 line 둘이 이렇게 읽히지 않았음(`c2-p2a@chain-x1.2`와 `@chain-x1.4`의 `oracle` run에서 `starvation_floor` 실패).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 entry "a line that reads a gap from a run with a failed guard gives no reading", its RQ0 gate spec bullet; `harness/experiments/rq0-gate.yaml`, statement `sensitivity-lines`; `docs/rq0-run-record.md`, "The reporting lines", the chain scale row

### g4-09 · `docs/guidebook/dataset/04-the-coreset.md:1968` · A · item 10 (the re-measurement and the second bless), item 12 (the experiment lint reads an executed spec's pins as notes)
- **Now:** "pin은 RQ0 gate spec의 `pins.variants.all`입니다. 2026-10-17의 값은 `8e2948b1…`이고(…), `shasum -a 256 dataset/build.variants.manifest.json`이 같은 값을 냅니다. 이 pin은 9.14 D12(2026-10-09)에 처음 걸렸고 그 뒤 9.17, 9.18, 9.22, 9.20, 9.23(D10, D17), 9.15(…), 9.16(2026-10-17, 출구 감사의 data rebuild)을 거치며 다시 걸렸습니다. …"
- **Becomes:** keep the dated 2026-10-17 value. Then add: RQ0 run(2026-11-16–18)이 읽은 pin은 첫 bless의 variants manifest를 가리킴. 2026-11-21의 둘째 bless가 variant 78개 가운데 `python3`를 담은 열네 개를 다시 build해, `dataset/build.variants.manifest.json`의 hash는 더 이상 pin과 같지 않음. 실행된 RQ0 gate spec은 고치지 않음. 그 dataset pin과 variants pin은 첫 bless를 가리킨 채 남음. experiment lint는 실행된 spec의 pin을 그 run이 읽은 tree로 읽어, 어긋난 pin을 오류가 아니라 note로 찍음(2026-11-20).
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry, its opening paragraph ("The RQ0 gate spec is not edited — its dataset and variants pins name the first bless …") and "The second bless" bullet (14 of the 78 variants); the 2026-11-20 entry "an executed spec's pins read as the tree its run read"; `harness/experiments/rq0-gate.yaml`, `pins.variants.all` (line 665)
- **Flags:** for 인지오: the re-pin enumeration also lacks the 2026-10-31 dataset rebuild's re-pin that set today's pin `de9802e7…` (`harness/CHANGELOG.md`, the 2026-10-31 entry "each measured operation's largest run…", its Pins line; commit `db2fda65`). That re-pin is outside the fifteen items (class D). Should the pin's current value be stated, the passage must name it.

### g4-10 · `docs/guidebook/dataset/04-the-coreset.md:1919–1927` · E · item 6 (the RQ0 run), item 10 (the re-measurement and the second bless)
- **Now:** the axis paragraphs of 11.4. Each states its line's reason and its expected reading. Examples: chain "the expected reading is that the gaming verdicts depend on the literature-grounded archetype's scale"; segment length "120 s 쪽은 'expected unchanged, the terms reading the second segment'"; carried values "이 variant에서 판정 수가 바뀌면 RQ0 gate spec의 `re-measurement-contingency`가 작동해, 해당 entry를 다시 측정한 뒤에야 결과를 보고합니다."
- **Becomes:** nothing in them is false: they state the pre-registered reasons and rules. The RQ0 run's readings of these lines appear nowhere in chapter 4:
  - venue ×0.8 gave 7 and ×1.25 gave 5;
  - chain scale was not read;
  - first segment 30 s gave 6 and 120 s gave 7, so the 120 s count moved;
  - carried half-widths gave 5 at the lower bound and 6 at the upper, and the contingency fired;
  - trace replay: agreement false.

  Post hoc: venue 5 and 4, segment 4 and 5, carried half-widths 4 and 4. The contingency's entry was `cpu-batch`'s `python3` run between voluntary blocks, re-measured at 107 repeats.
- **From:** `docs/rq0-run-record.md`, "The reporting lines" (table and the Trace replay bullet); "Corrections", 2026-11-18 table; "Corrections", 2026-11-21, "The finding"
- **Flags:** for 인지오: spec decision 1 corrects false statements only. Decide whether these paragraphs gain one sentence each with the run's reading, or stay as pre-registration text.

### g4-11 · `docs/guidebook/dataset/04-the-coreset.md:1858–1860` · E · item 13 (the configuration search and the route)
- **Now:** "… statement는 이것이 gate를 보수적으로 만들며, 실패가 이 아홉에 몰리면 실패 절차가 먼저 table을 점검한다고 적습니다." and "- **prior driver table** — … RQ0 gate에만 쓰입니다(`daemon/driver-table/prior.yaml`). 보고되는 결과는 따로 tuning한 calibrated table이 냅니다."
- **Becomes:** nothing false. The passage reports what the statement `prior-table-structure` says, and the prior table was used only in the RQ0 run. The failure procedure has since run: the configuration search of 2026-11-21 covered 470 configurations on ten files. The route is that the table is rewritten: 8 of 10 files are at finding 3 (spread the prior table missed), and `c7-transcode` and `c7-gaming` are at finding 2.
- **From:** `docs/rq0-run-record.md`, "The failure procedure", 2026-11-21; `harness/experiments/rq0-config-search/report.md`
- **Flags:** for 인지오: decide whether to state the route here. Item 15 limits what may be said about the rewrite itself (Phase 12's), and whether the rewritten table is "the calibrated table" is in no record.

### g4-12 · `docs/guidebook/dataset/04-the-coreset.md:2338–2357` · B · conditional on g4-03, g4-05, g4-07, g4-09
- **Now:** "## 14.7 이 권에 나온 phase와 sub-task" — the table ends at "| 9.23 | 이 guidebook이 찾은 어긋남(2026-10-14/15). … |"
- **Becomes:** if the applied rows name them, add rows at the neighbours' detail. "Phase 10 | 통합과 RQ0 run(RQ0 run 2026-11-16–18)". "10.4 | cold smoke와 비용 대응(2026-11-14/15). records 경로, worker 설정, 비용을 N = 100에서 짐". "Phase 11 | RQ0 실패 절차: 진단". "11.3 | 재측정과 둘째 bless(2026-11-20/21). `cpu-batch` `python3`의 두 block 값을 107 repeat로".
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md` and `phase-11-rq0-failure-procedure-diagnosis.md`, titles; `docs/rq0-run-record.md`, "The run"; `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`; `harness/CHANGELOG.md`, the 2026-11-15 cost-response entry and the 2026-11-21 re-measurement entry

### g4-13 · `docs/guidebook/dataset/04-the-coreset.md:15` · E · item 10 (the re-measurement and the second bless)
- **Now:** "이 권은 2026-10-14의 tree를 기준으로 썼고, 2026-10-17에 그 뒤의 변화(…)에 맞춰 다시 셌습니다. 파일 수, segment 수, compile된 event 수, byte 수, utilization은 모두 tree에서 … 직접 세었고, …"
- **Becomes:** after g4-02, g4-04 and g4-06, three byte counts are those of the 2026-11-21 tree, so the intro's "2026-10-17에 … 다시 셌습니다" no longer covers every count. The 2026-10-31 re-read is not named either: commit `05f7a220` re-read "every per-file count, size and utilization" in the dataset guidebook, which is outside the fifteen items.
- **From:** `git show 05f7a220` (subject line); g4-02, g4-04, g4-06
- **Flags:** for 인지오: decide whether the intro names the later re-reads.

### g4-14 · `docs/guidebook/dataset/04-the-coreset.md:413` · D · outside the fifteen items
- **Now:** "> **코드로.** `dataset/tools/end_bound.py`가 이 산술을 compile된 artifact 위에서 계산합니다. 2026-10-14에 `python3.12 tools/end_bound.py build/coreset-single/c1-ml-train.workload.json hog 1612`를 돌리면 \"arrival 2.000 s + …\"가 나옵니다."
- **Why left:** the passage is dated. The command it cites now fails with `IndexError` in `wakes[(task["id"], op["channel"])][k]` on the current artifacts. It fails on `c1-render` too, a file the second bless did not change, so the cause is not one of the items. Probably it is the 2026-10-31 wake-channel rebuild.

## Chapter 2 — the archetype library

### g4-15 · `docs/guidebook/dataset/02-the-archetype-library.md:439` · B · item 10 (the re-measurement and the second bless)
- **Now:** "library에 쓰인 workflow는 여섯입니다. … `background`(9.7과 9.10의 batch job들), …"
- **Becomes:** `background`(9.7과 9.10의 batch job들, 그리고 11.3의 `cpu-batch` `python3` 재측정).
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `params` (lines 1257, 1259: `source: "meas-ci:background:2026-11-20"`); `dataset/meas-releases.yaml`, line 298

### g4-16 · `docs/guidebook/dataset/02-the-archetype-library.md:597` · A · item 10 (the re-measurement and the second bless)
- **Now:** "기준 문서는 `docs/workload/measurement-overview.md`(측정 개요; status draft, 2026-09-29 작성, 2026-10-17 갱신)와 …"
- **Becomes:** 2026-11-21 갱신.
- **From:** `docs/workload/measurement-overview.md`, header line 2 (`Updated 2026-11-21`, set by `2e3fade3`, 11.3's fold-in)
- **Flags:** for 인지오: the date was already stale from 2026-10-31 (outside the items). The sentence after it ("§2는 2026-10-17에 9.15가 다시 써서 … 28개") stays true.

### g4-17 · `docs/guidebook/dataset/02-the-archetype-library.md:635` · A · item 10 (the re-measurement and the second bless)
- **Now:** "`dataset/meas-releases.yaml`이 데이터가 인용하는 campaign 23개마다 그 release(하나 이상)와 각 asset의 SHA-256을 적고, …"
- **Becomes:** campaign 24개마다.
- **From:** `dataset/meas-releases.yaml`: 24 `meas-ci:` entries, against 23 at `2487ba27^`. The added entry is `meas-ci:background:2026-11-20` (line 298).

### g4-18 · `docs/guidebook/dataset/02-the-archetype-library.md:660` · A · item 10 (the re-measurement and the second bless)
- **Now:** "| machine 따라 흩어짐 | … | `game-client`, `renderer-hidden`의 run 평균; `cpu-batch` `python3`의 block 값(9.6 D29, 9.10 D87) |"
- **Becomes:** `cpu-batch` `python3`의 block 값 둘(9.6 D29, 9.10 D87; 2026-11-21에 11.3이 107 repeat로 다시 재어 ±5.89 %, ±2.15 %, class는 그대로).
- **From:** `docs/rq0-run-record.md`, "Corrections", 2026-11-21, the campaign table and "Both values keep their exception class"; `docs/workload/measurement-overview.md` §7, the "Spread follows the machine" row

### g4-19 · `docs/guidebook/dataset/02-the-archetype-library.md:660` · D · outside the fifteen items
- **Now:** "| machine 따라 흩어짐 | runner의 디스크나 속도를 따라 움직임. …"
- **Why left:** since 2026-10-17 (`c59b6a89`) the overview's row reads "its disk, its speed or its kernel's housekeeping". `python3`'s values follow `khugepaged`, the kernel's housekeeping. The guidebook's cell lacks that third cause from before Phase 10.

### g4-20 · `docs/guidebook/dataset/02-the-archetype-library.md:1013` · A · item 10 (the re-measurement and the second bless)
- **Now:** "| tag | `meas-ci:background:2026-10-03`(`python3`), `meas-ci:background:2026-10-03c`(`kdenlive_render`) |"
- **Becomes:** `meas-ci:background:2026-11-20`(`python3`의 run·block table, 11.3), `meas-ci:background:2026-10-03`(`python3`의 CPU 총량, timeline이 묶음), `meas-ci:background:2026-10-03c`(`kdenlive_render`).
- **From:** `dataset/archetypes.yaml`, lines 1257 and 1259 (`python3_run`, `python3_block` sources); `dataset/timelines/coreset/c1-ml-train.timeline.yaml` line 24 and `c2-p1a.timeline.yaml` line 25 (`total_work: "meas-ci:background:2026-10-03"`)

### g4-21 · `docs/guidebook/dataset/02-the-archetype-library.md:1017–1027` · A · item 10 (the re-measurement and the second bless)
- **Now:** "… 이름은 `python`입니다(…, 9.10 D84). 6 repeat." / "| voluntary block 사이 run | 평균 69.49 s ±27.3 %(repeat당 53.9–114.9 s) |" / "| run당 block | 311.5 μs ±10.8 % |" / "| block 수 | repeat당 11–24개; 처음 두 번의 sleep 말고는 모두 `khugepaged`가 끝냄 |" / "`python3_run` table의 중간값은 228 ms이지만 p75가 43.5초, 최대가 1,006초입니다. … 그래서 block 값 둘은 \"machine 따라 흩어짐\" 예외로 반폭과 함께 실립니다."
- **Becomes:**
  - "6 repeat" → job 전체 CPU와 포화도는 9.10 campaign(`meas-ci:background:2026-10-03`)의 6 repeat. voluntary block 사이 run과 run당 block은 2026-11-21에 11.3이 같은 job, 같은 CPU 모델로 107 repeat를 돌려 다시 잰 값(`meas-ci:background:2026-11-20`). 그때의 runner는 kernel 7.0.0-1017-azure였고, runner의 agent `provjobd`가 job마다 수천 번의 대기를 끝내며, 그 대기는 끊긴 run에 접힘.
  - table: voluntary block 사이 run, 평균 55.27 s ±5.89 %(repeat당 30.6–121.2 s); run당 block, 403.96 μs ±2.15 %(233–504 μs); block 수, repeat당 11–46개, 모두 kernel이 끝냄(`khugepaged` 9–44개, 107 중 91 repeat에서 시작의 두 sleep, migration wakeup 하나), `provjobd`가 끝낸 대기 repeat당 2,890–8,343개는 run에 접힘.
  - optional row: 11.3이 읽은 CPU 총량은 1,413.843 s ±0.34 %로 실린 값의 구간 안.
  - median sentence: 중간값은 1.2 ms(1,223 μs)이지만 p75가 20.5초, 최대가 1,298초.
  - last sentence: 반폭(±5.89 %, ±2.15 %)과 함께 실림.
- **From:** `docs/rq0-run-record.md`, "Corrections", 2026-11-21, "The campaign" paragraph and table; `dataset/archetypes.yaml`, `cpu-batch` `validation_stats.stats` (lines 1272–1273), `scope` (lines 1288–1293, 1303–1307), `params.python3_run` (line 1257; `p` positions per the header, line 46: p50 = 1,223, p75 = 20,473,778, `max` = 1,297,955,204 µs)

### g4-22 · `docs/guidebook/dataset/02-the-archetype-library.md:1031` · A · item 10 (the re-measurement and the second bless)
- **Now:** "> **왜 이렇게 정했나 — huge page 설정은 runner의 것(9.10 D87, D88, 2026-10-03).** runner의 커널은 transparent huge pages(…)를 `always` 모드로 돌리는데, Ubuntu desktop 커널의 기본값은 `madvise`입니다. … 실린 값은 runner(`always`)의 것이고, …"
- **Becomes:** keep the 9.10 sentence as the runner of then (kernel 6.17.0-1022-azure). Add one sentence: 11.3의 campaign(2026-11-20)에서는 runner가 kernel 7.0.0-1017-azure로 바뀌어 image의 기본값이 `madvise`였음. job이 run 전에 `always`를 써서 같은 모드로 잼. 실린 값은 여전히 `always` 아래의 값.
- **From:** `docs/rq0-run-record.md`, "Corrections", 2026-11-21, "The campaign" paragraph; `dataset/archetypes.yaml`, `cpu-batch` `scope` (lines 1286–1292)

### g4-23 · `docs/guidebook/dataset/02-the-archetype-library.md:1449–1453` · B · item 10 (the re-measurement and the second bless)
- **Now:** "## 11.4 재건의 순서" — the table's rows run to "| 2026-10-31 | 측정된 모든 component를 … timer part와 event part … | timer-wakes-by-origin spec 결정 6, 8, 10, 13 |"
- **Becomes:** add a last row: "| 2026-11-21 | `cpu-batch` `python3`의 voluntary block 사이 run과 run당 block을 107 repeat로 다시 잼(`meas-ci:background:2026-11-20`); 둘째 bless | 11.3 |".
- **From:** `harness/CHANGELOG.md`, the 2026-11-21 re-measurement entry; `docs/rq0-run-record.md`, "Corrections", 2026-11-21

### g4-24 · `docs/guidebook/dataset/02-the-archetype-library.md:1491` · A · item 10 (the re-measurement and the second bless)
- **Now:** "- **CPU 모델 하나, 시기 하나.** AMD EPYC 7763 하나만, 2026-09-18부터 2026-10-05 사이에. runner 커널(6.17.0-1022-azure)은 THP `always`이고 desktop 기본은 `madvise`입니다(학습 job 1.144배)."
- **Becomes:** AMD EPYC 7763 하나만, 2026-09-18부터 2026-10-05 사이에, 그리고 2026-11-20의 11.3 재측정(`cpu-batch` `python3`의 block 값 둘). 2026-10-05까지의 runner 커널(6.17.0-1022-azure)은 THP `always`였음. 11.3의 runner(7.0.0-1017-azure)는 기본값이 `madvise`라, job이 `always`를 쓰고 잼. desktop 기본은 `madvise`(학습 job 1.144배).
- **From:** `docs/rq0-run-record.md`, "Corrections", 2026-11-21, "The campaign" paragraph; `dataset/archetypes.yaml`, `cpu-batch` `scope`

### g4-25 · `docs/guidebook/dataset/02-the-archetype-library.md:1495–1516` · E · item 6 (the RQ0 run), item 10 (the re-measurement and the second bless)
- **Now:** chapter 12's "the way the consumer handles it" passages. 1495: "판정 개수가 이 축에서 움직이면 판정을 범위로 보고합니다." 1510: "`dataset/variants.yaml`의 `replay` 변형이 이 한계를 위한 것입니다 …". 1516: "RQ0 gate spec은 이 값들을 모두 95 % 구간의 아래 끝과 위 끝으로 옮긴 `corner-low`, `corner-high` 변형으로 판정이 바뀌는지 봅니다 …"
- **Becomes:** nothing false; the passages state the pre-registered checks. The RQ0 run's readings:
  - venue factor ×0.8 gave 7 and ×1.25 gave 5;
  - trace replay: agreement false (`c7-browsing` crosses g);
  - carried half-widths gave 5 and 6, the contingency fired, the entry found was `cpu-batch`'s `python3` run between voluntary blocks, and it was re-measured on 2026-11-21.

  The 2026-10-17 list of 19 tables at 1516 stays true.
- **From:** `docs/rq0-run-record.md`, "The reporting lines"; "Corrections", 2026-11-21
- **Flags:** for 인지오: same question as g4-10. Decide whether the limit passages state what the run found.

### g4-26 · `dataset/archetypes.yaml:1279` (bears on `02-the-archetype-library.md:1013`, `1017`) · E · item 10 (the re-measurement and the second bless)
- **Now:** `cpu-batch` `scope` opens "One observation per program (phase decision 2; D3, D7, D30), each in 9.10's own campaign, … kernel 6.17.0-1022-azure …", and the same scope says later "Its run between voluntary blocks and block per run are 11.3's re-measurement (`meas-ci:background:2026-11-20` …)".
- **Becomes:** no guidebook change. g4-20 and g4-21 follow the later sentence and the params' tags.
- **From:** `dataset/archetypes.yaml`, lines 1279–1293
- **Flags:** for 인지오: the record disagrees with itself. Its first sentence still says each program's values come from 9.10's own campaign. `docs/workload/measurement-overview.md` §1 ("for `cpu-batch`, of each of its two programs, each in its own campaign") reads the same way. Neither file is the sweep's to edit (data; the overview is in scope only for overtaken statements).

## README

### g4-27 · `docs/guidebook/dataset/README.md:7` · E · item 10 (the re-measurement and the second bless)
- **Now:** "모든 수는 처음 쓸 때(2026-10-14) 트리와 대조했습니다. 문서 정정 작업(9.15)에서는 각 권에서 고친 대목을 2026-10-17의 트리와 대조했습니다. exit audit(9.16)과 Phase 9가 2026-10-18에 끝난 뒤, … 2026-10-20의 트리에 대조해 고쳤습니다."
- **Becomes:** the list of correction passes ends at 2026-10-20. It lacks the 2026-10-31 pass (`05f7a220`, "the dataset guidebook", outside the items) and will lack this sweep's corrections against the 2026-11-21 tree.
- **From:** `git show 05f7a220` (subject line); this work list
- **Flags:** for 인지오: decide whether the README names the later passes. The header's `Updated 2026-10-20` moves only if the README's content changes.

### g4-28 · `docs/guidebook/dataset/README.md:36` · B · item 10 (the re-measurement and the second bless)
- **Now:** "문서와 트리가 어긋나는 곳은 현재의 트리(data file, manifest, code, Phase 9의 기록)를 기준으로 적고, 어긋남 자체를 그 자리에 밝힙니다."
- **Becomes:** 현재의 트리(data file, manifest, code, Phase 9의 기록과 그 뒤의 기록 — 이를테면 `cpu-batch` `python3`의 block 값 둘을 다시 잰 11.3의 기록).
- **From:** `dataset/archetypes.yaml`, `cpu-batch` `scope` (names `_dev/research/jioh/task-11.3-the-re-measurement/`); `harness/CHANGELOG.md`, the 2026-11-21 re-measurement entry
- **Flags:** for 인지오: low confidence. The parenthesis may read as examples rather than a whole set. The 2026-10-31 timer-wakes-by-origin records are also missing from it (outside the items).
