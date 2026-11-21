# Rows — g2 (dataset guidebook, chapters 8 and 3)

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/guidebook/dataset/08-decision-chronicle.md` | 2135 | 150 | 6/4/11/3/2 |
| `docs/guidebook/dataset/03-timeline-to-canonical-workload.md` | 2390 | 82 | 9/1/2/0/0 |

## `docs/guidebook/dataset/08-decision-chronicle.md`

### g2-01 · `docs/guidebook/dataset/08-decision-chronicle.md:54` · A · items 7–15 (Phase 11) for the count; item 10 (the re-measurement and the second bless) for the dataset-related list
- **Now:** "`_dev/TODO.md`의 인지오 section에 Phase 1부터 Phase 10까지 번호가 붙어 있습니다. 데이터셋에 직접 관계된 phase는 1, 2, 3, 7, 9입니다."
- **Becomes:** 인지오의 phase는 Phase 1부터 Phase 11까지입니다. 끝난 phase의 section은 `_dev/TODO-done.md`로 옮겨지고, `_dev/TODO.md`에는 Done 목록의 한 줄이 남습니다. 데이터셋에 직접 관계된 phase는 1, 2, 3, 7, 9, 11입니다(11은 sub-task 11.3의 재측정과 second bless).
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, header ("인지오's Phase 11 in `_dev/TODO.md`, decided on 2026-11-18"), Scope (the re-measurement); `_dev/docs/spec/jioh/task-11.5-docs-sweep.md`, decision 8 (a closed phase's section moved verbatim into `_dev/TODO-done.md`, one index line under the Done list); `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry (`dataset/archetypes.yaml` folded in, the second bless)
- **Flags:** for 인지오: whether Phase 11 counts as "직접 관계된" is a judgement. The argument for it is that 11.3 changed `dataset/archetypes.yaml` and re-blessed every manifest. Phase 10 changed no dataset file: every CHANGELOG entry from 2026-11-01 to 2026-11-18 says "the dataset manifests unchanged" or "no pin moves".

### g2-02 · `docs/guidebook/dataset/08-decision-chronicle.md:59` · D · outside the fifteen items
- **Now:** "위치는 `_dev/archive/`이고, 지금 일곱 개가 있습니다."
- **Becomes:** (left alone) `_dev/archive/` has held eight files since 2026-10-16, when `2026-08-27-phase-2-grills-rationales.md` was added (commit `0987dc64`). The chronicle cites that archive itself at line 371. No item of the fifteen touches it.

### g2-03 · `docs/guidebook/dataset/08-decision-chronicle.md:695` · B · item 9 (the simulator's stage AF)
- **Now:** "**voluntary block**은 task가 스스로 CPU를 내려놓고 기다리는 것(I/O나 신호 대기)입니다."
- **Becomes:** add a member at the gloss's level. Since 2026-11-19 the simulator also counts a `FORK` that finds `fork_cap` reached and waits for a slot as a voluntary block. This is the stage AF fix (`simulator@841dc81131cb`), and it resets the B1 counter quoted two lines above ("a full slice since the last voluntary block").
- **From:** `docs/memos/2026-11-19-simulator-changes-by-jioh.md`, TL;DR; `simulator/steps/README.md`, row **af**; `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`, its 2026-11-19 correction
- **Flags:** for 인지오: this is a gloss with examples in parentheses, not a closed list. Listed because it sits beside the B1 quote that item 9 changes.

### g2-04 · `docs/guidebook/dataset/08-decision-chronicle.md:1277` · A · item 2 (the integration gate passed)
- **Now:** "이 결정 때문에 harness와 simulator 사이에 "약속된 행동"과 "구현된 행동"의 차이가 생겼고, 그 차이가 지금의 열린 자리 중 하나입니다(12장)."
- **Becomes:** …차이가 생겼고, 그 차이는 2026-11-14의 통합 gate로 닫혔습니다. conformance 항목 (a)–(j)가 모두 `simulator@0d323c84470a`의 binary 위에서 보였습니다(12.4의 4).
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed; the RQ0 gate spec pins the simulator and the daemon; re-pinned"

### g2-05 · `docs/guidebook/dataset/08-decision-chronicle.md:1318` · C · item 5 (the runner and the cost)
- **Now:** "> **열린 자리.** `c6-dual`의 records build 비용(실행 하나에 약 40분, random seed 100개 계획)은 Phase 10의 RQ0 실행에서 계획해야 할 비용으로 남아 있습니다. … 대응은 실제 simulator로 잰 비용 위에서 Phase 10에 정합니다. 선택지는 "a cheaper records path, N changed …, or the cost carried"입니다(12.4)."
- **Becomes:** the box goes, and the passage states the outcome as text. In 10.4 (2026-11-14 → 11-15) the records path was rebuilt. Since then the records build and aggregates of `c6-dual`'s `fixed` run (14,031,957 rows) take about 7.5 minutes at a peak of 9.4 GB; before, they took about 40 minutes, ran past 15 GB and swapped. The runner now spreads runs over processes (`workers`, `heavy_workers`, `heavy_mb`) and keeps a results cache. On 2026-11-15 인지오 decided to carry the cost, with N = 100 unchanged. The upper projection for the full run was 50.33 h of the 80 h budget and 273.5 GB, of which `c6-dual` takes 30.59 h over its 112 runs. The RQ0 run took 45 h 26 min.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "before the cold smoke: the records path's count…" (the `c6-dual` figures) and 2026-11-14 "the runner: runs at once and a results cache"; `harness/CHANGELOG.md`, 2026-11-15 "the cost response…" (cost carried, 50.33 h, 273.5 GB); `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`, "The projection" (`c6-dual` 30.59 h over 112 runs); `docs/rq0-run-record.md`, "The run" (N 100, 45 h 26 min)

### g2-06 · `docs/guidebook/dataset/08-decision-chronicle.md:1759` · B · items 1–6, 10, 11, 14 (the chapter's re-readings)
- **Now:** "…이 장의 인용은 2026-10-14에 읽은 상태입니다. … 2026-10-21에 다시 읽어 Phase 10의 새 항목들(12.4의 6–8)과 conformance 항목 (d)의 구현을 더했습니다. 2026-10-30에 다시 읽어 conformance 항목 (a), (b), (e)의 구현과 TIMER 문서의 고침을 더했습니다."
- **Becomes:** add the next re-reading at the same level of detail. On 2026-11-21 the chapter was re-read, and the eight items of 12.4 were closed together with the outcomes of Phase 10 and Phase 11. That re-reading also covers the open-spot boxes of 12.2 and 12.4, the hold-time line in 12.5, and the re-measurement in 12.7.
- **From:** the records named in g2-08 to g2-21
- **Flags:** for 인지오: this follows the chapter's own convention of listing its re-readings. Drop it if that list is not to grow.

### g2-07 · `docs/guidebook/dataset/08-decision-chronicle.md:1799` · B · item 10 (the second bless); item 2 for the 2026-11-14 re-pin
- **Now:** "…2026-10-17에 9.15의 re-pin을 두 번 거쳤습니다. … 같은 날 출구 감사 9.16의 re-pin이 현재입니다. scoring spec `f7d1df4c…`, guard spec 1.2 `c2dad06f…`, driver table `e1155a72…`(…), dataset `8e1eb753…`, variants `8e2948b1…`, 생성 manifest는 …"
- **Becomes:** the passage lists pins and labels its last one "현재", so the later members are added.
  - On 2026-10-17 the 9.16 re-pin was the latest one.
  - The RQ0 gate spec was re-pinned on 2026-10-31 (scoring spec `4f3e34c1…`, guard spec 1.4 `7d79201d…`, dataset `27d347bc…`, variants `de9802e7…`).
  - It was re-pinned on 2026-11-01 (the cap band's three alternative tables).
  - It was re-pinned on 2026-11-14 (driver table `f693bfbe…`, `simulator@0d323c84470a`, `daemon@62c71f0d2de0`).
  - The 2026-11-21 second bless rebuilt all seven manifests (dataset `9f30ea8f…`, variants `3438be7f…`). The RQ0 gate spec was not edited and still pins the bless its run read (dataset `27d347bc…`, variants `de9802e7…`). The configuration search spec pins the second bless's dataset manifest.
- **From:** `harness/CHANGELOG.md`, the 2026-10-31 entries (pins), 2026-11-01 (pins), 2026-11-14 "the integration gate passed…" (pins), 2026-11-20 and 2026-11-21 re-measurement entries (the RQ0 gate spec not edited, its pins naming the first bless; the second bless's seven sets); `harness/experiments/rq0-gate.yaml`, `pins`; `harness/experiments/rq0-config-search.yaml`, `pins.dataset`; the committed `dataset/build.manifest.json` (SHA-256 `9f30ea8f3a99…`) and `dataset/build.variants.manifest.json` (`3438be7f516f…`)
- **Flags:** for 인지오: the 2026-10-31 re-pins lie outside the fifteen items, so "현재" was already stale before Phase 10 (a D part). They are listed here only so the list's members stay in order.

### g2-08 · `docs/guidebook/dataset/08-decision-chronicle.md:1851` · C · item 2 (the integration gate passed)
- **Now:** "(d)는 2026-10-20에, (b)는 2026-10-23에, (e)는 2026-10-28에 구현되었고(12.4의 4), 그 확인은 기록에 아직 없습니다. 빚으로 남은 conformance 항목은 (g), (h)의 둘이고, 구현은 인경민의 몫이며, 그 전에는 RQ0 실행이 허용되지 않습니다(12.4)."
- **Becomes:** the box stays, narrowed to the per-item checks. The implementation dates gain (g), which 인경민 implemented on 2026-11-11 as stage AA. The 2026-11-14 integration gate showed (a)–(j) on the binary. The sentence "빚으로 남은 … (g), (h) … RQ0 실행이 허용되지 않습니다" goes. What stays open: no record yet holds the result of the per-item check on the statements in `compiled/uncheckable-by-item.md` (its "Check" lines).
- **From:** `simulator/memo/memo_261111.md`, Part B (stage AA, (g)); `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…" (where each item is shown); still open: `_dev/research/jioh/task-9.16-exit-audits/compiled/uncheckable-by-item.md`, lines 7 and the "Check" lines, unchanged since commit `b51df8a4` (2026-10-17), and no later record of those checks

### g2-09 · `docs/guidebook/dataset/08-decision-chronicle.md:1859` · A · items 1–6 (Phase 10), 11 (the verdict final)
- **Now:** "데이터셋과 관계된 열린 항목은 여덟입니다."
- **Becomes:** 데이터셋과 관계된 항목은 여덟이었습니다. Phase 10은 2026-11-01에 열려 2026-11-18에 RQ0 run의 판정과 함께 끝났고, 여덟 항목은 아래처럼 닫혔습니다(2는 Phase 10 밖으로 옮겨짐). The quoted TODO line stays as a quote.
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 2 (opens 2026-11-01); `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, header ("Phase 10 ended with the verdict", decided 2026-11-18); `docs/rq0-run-record.md`, "The run" (finished 2026-11-18)

### g2-10 · `docs/guidebook/dataset/08-decision-chronicle.md:1861` · C · items 1 and 6 (the pre-run lines; the RQ0 run's trace-replay line)
- **Now:** "**1. trace-replay 점검.** … 9.14가 이미 파일 넷(`c7-dev`, `c7-browsing`, `c7-meeting`, `c2-p1a`)과 일치 기준(…)을 gate spec에 사전 등록했습니다(9.14 결정 10). 실행은 Phase 10의 것입니다."
- **Becomes:** **1. trace-replay 점검 — 닫힘.**
  - 2026-11-01: Phase 10 spec 결정 6이 사전 등록(파일 넷, 일치 기준, 불일치가 이끄는 것)을 done으로 적었습니다.
  - RQ0 run(2026-11-16 → 11-18)의 결과는 agreement false였습니다(tolerance 0.17).
    - `c2-p1a` 0.377 대 0.367과 `c7-meeting` 0.279 대 0.261은 일치했습니다.
    - `c7-browsing` 1.121 대 0.475는 g를 건넜습니다.
    - `c7-dev` 0.254 대 0.000은 tolerance를 넘었습니다.
  - 이 결과는 판정 옆에 compile된 stream의 순서 위협으로 적혔습니다(statement `sensitivity-lines`).
  - sign rule로 다시 읽은 post hoc reading(판정 아님)에서도 false입니다: `c7-dev` 0.000 대 0.000, `c7-browsing`은 run과 같습니다.
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 6; `docs/rq0-run-record.md`, "The reporting lines", Trace replay bullet; `docs/rq0-run-record.md`, "Corrections", 2026-11-18 table, trace replay row

### g2-11 · `docs/guidebook/dataset/08-decision-chronicle.md:1863` · E · none of the fifteen closes it (decision 14 asks that it gain "닫힘")
- **Now:** "**2. Layer 1과 RQ4의 항목.** 9.12의 recognizer 쪽 항목들이 Layer 1과 RQ1–RQ4 실험 spec으로 넘어갔습니다. "the two rule lists' build (…; no phase yet, 박이안 the owner)"도 여기 있습니다."
- **Becomes (proposed):** **2. Layer 1과 RQ4의 항목 — Phase 10 밖으로.** 2026-11-01의 Phase 10 spec 결정 9가 이 항목을 Backlog로 옮겼습니다. 그 글이 이름 붙인 실험 spec들이 맡습니다. RQ1–RQ4 실험 spec은 Phase 10과 Phase 11의 범위 밖입니다.
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 9 and the Scope's out-of-scope line; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, the Scope's out-of-scope line
- **Flags:** for 인지오 (cannot decide):
  - The matter moved; it did not close. No record closes it, so "닫힘" would be false here, and the right word is yours to choose.
  - The RQ0 run's Layer 1 reporting line ran (`docs/rq0-run-record.md`, "The reporting lines"). That line is a different thing from this item and is not proposed as its outcome.
  - If the item now sits in the Backlog, 12.5's "Backlog의 데이터셋 관련 줄은 다섯입니다" may need a sixth line. That count rests on the TODO, which this sweep does not read for numbers.

### g2-12 · `docs/guidebook/dataset/08-decision-chronicle.md:1865` · C · item 1 (the RQ0 gate spec's pre-run lines; the Phase 10 spec marks it done)
- **Now:** "**3. TIMER 문서.** 2026-10-14에 9.15에서 넘어온 줄입니다. … 남아 있던 schema(`dataset/schema/workload.schema.json`)의 TIMER 설명도 2026-10-31에 … skip 규칙으로 고쳐졌습니다(2026-10-30 결정)."
- **Becomes:** the heading becomes **3. TIMER 문서 — 닫힘.** The body keeps its closing sentences (2026-10-30: the docs; 2026-10-31: the schema) and gains one more: "Phase 10 spec 결정 6(2026-11-01)이 이 항목을 done으로 적었습니다."
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 6; `docs/data-contracts.md` §14, 2026-10-30 entry (already cited in the passage)
- **Flags:** the closing itself is older than the fifteen items and already stated. Only the "닫힘" form is new, as decision 14 asks.

### g2-13 · `docs/guidebook/dataset/08-decision-chronicle.md:1867` · C · item 2 (the integration gate passed); item 3 (stages AD and AE) for the binary's contents
- **Now:** "**4. simulator의 blocker.** … 이것들이 구현되기 전에는 RQ0 실행이 허용되지 않습니다. … 그래서 지금 빚으로 남은 항목은 (g), (h), (j)의 셋입니다."
- **Becomes:** **4. simulator의 blocker — 닫힘.** The history stays. The last sentence becomes "2026-10-31에 빚으로 남은 항목은 (g), (h), (j)의 셋이었습니다", followed by:
  - 2026-11-11: 인경민이 (g)를 stage AA로, (j)를 stage AC로 구현했습니다. (h)는 simulator가 계약의 세 flag만 받고 trace 머리에 version 문자열을 쓰게 된 것입니다.
  - 2026-11-13: 인지오가 stage AD(끝 이후의 schedule entry 무시)와 AE(idle class 옆의 cap)를 더했습니다.
  - 2026-11-14: 통합 gate가 `simulator@0d323c84470a`와 `daemon@62c71f0d2de0`에서 통과했습니다. statement `simulator-conformance`가 각 항목을 보인 곳을 적습니다. binary로 재생한 hand fixture가 (a), (b), (c), (g), (i), (j)를, `simulator/tests/`의 black-box unit test가 (d), (e), (f), (g), (i), (h)를 보였습니다.
  - RQ0 gate spec이 두 version을 pin하고, runner는 다른 version을 거부합니다.
- **From:** `simulator/memo/memo_261111.md`, Parts B, D, E (author kyungmin, 2026-11-11); `docs/memos/2026-11-13-simulator-changes-by-jioh.md`, TL;DR (AD, AE; version `simulator@0d323c84470a`); `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…" (where each item is shown; pins); `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md` §2–§3

### g2-14 · `docs/guidebook/dataset/08-decision-chronicle.md:1869` · C · item 5 (the runner and the cost)
- **Now:** "**5. `c6-dual`의 비용.** … 대응(더 싼 records 경로, gate spec의 `n-grounding` statement 아래에서 N을 바꾸기, 비용을 그대로 지기)은 실제 simulator로 잰 비용 위에서 Phase 10에 정한다고 적습니다(8.5)."
- **Becomes:** **5. `c6-dual`의 비용 — 닫힘.**
  - 2026-11-14: records 경로를 고쳐, `c6-dual`의 `fixed` run(14,031,957 row)의 records와 aggregates가 peak 9.4 GB에서 약 7.5분이 되었습니다(전에는 약 40분이었고, 15 GB를 넘어 swap했습니다). 같은 날 runner가 run을 process에 나누고 results cache를 두게 되었습니다.
  - 2026-11-15: 비용을 지기로 정했습니다(N = 100 그대로). 상한 투영은 50.33 h(80 h 중)과 273.5 GB이고, 그중 `c6-dual`이 112 run에 30.59 h입니다.
  - RQ0 run은 45 h 26 min이 걸렸습니다.
- **From:** as g2-05: `harness/CHANGELOG.md`, the two 2026-11-14 entries and 2026-11-15 "the cost response…"; `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`, "The projection"; `docs/rq0-run-record.md`, "The run"

### g2-15 · `docs/guidebook/dataset/08-decision-chronicle.md:1871` · C · items 1 (the RQ0 gate spec's pre-run lines: `claim-links`), 6 (the RQ0 run's headroom count), 7 (the post hoc reading)
- **Now:** "**6. Link 2의 반증 조건.** … TODO 줄은 "no record sets one, and the RQ0 gate spec names no link; fixed in the RQ0 gate spec before the RQ0 run"입니다. 정하는 사람은 인지오입니다."
- **Becomes:** **6. Link 2의 반증 조건 — 닫힘.**
  - 2026-11-01: 인지오가 RQ0 gate spec의 statement `claim-links`로 정했습니다(10.1).
  - 규칙: headroom-count line이 link 2를 읽습니다. primary 아래에서 어느 판정 파일도 headroom을 갖지 않을 때, 곧 fixed가 모든 판정 파일의 모든 term에서 oracle의 결과에 닿을 때 반증됩니다. criterion의 gap과는 따로 읽습니다.
  - RQ0 run에서는 19개 중 17개가 headroom을 가져 link 2가 섰습니다.
  - sign rule로 다시 읽은 post hoc reading에서는 19개 중 12개입니다(판정이 아님).
- **From:** `harness/CHANGELOG.md`, 2026-11-01; `harness/experiments/rq0-gate.yaml`, statement `claim-links`; `docs/rq0-run-record.md`, "The outcome" (Link 2 stands, 17 of 19); `docs/rq0-run-record.md`, "Corrections", 2026-11-18 (12 of 19)

### g2-16 · `docs/guidebook/dataset/08-decision-chronicle.md:1873` · C · items 1 (the cap band line), 6 (the RQ0 run's cap band), 7 (the post hoc reading)
- **Now:** "**7. cap band line.** 2026-10-20에 더해진 줄입니다. "A cap band line in the RQ0 gate spec, … the values fixed in the RQ0 gate spec before the RQ0 run." … 정하는 사람은 인지오입니다."
- **Becomes:** **7. cap band line — 닫힘.**
  - 2026-11-01: statement `cap-band`와 cap band line이 RQ0 gate spec에 들어갔습니다(10.1).
  - 고정된 prior table에서 원치 않는 row의 cap만 0.2, 0.333, 0.5로 옮긴 table 셋(`daemon/driver-table/prior-floor-0.2.yaml`, `-0.333`, `-0.5`)이 `driver_table_alternatives`로 pin됩니다. 각 table 아래에서 oracle과 random을 판정 파일에 다시 돌립니다.
  - RQ0 run: 0.05, 0.2, 0.333, 0.5에서 6, 6, 7, 7이고 모두 fail입니다.
  - post hoc reading: 4, 4, 4, 5입니다.
- **From:** `harness/CHANGELOG.md`, 2026-11-01; `harness/experiments/rq0-gate.yaml`, statement `cap-band`; `docs/rq0-run-record.md`, "The reporting lines" (cap band row); "Corrections", 2026-11-18 table (cap band row)

### g2-17 · `docs/guidebook/dataset/08-decision-chronicle.md:1875` · C · item 5 (the cold smoke)
- **Now:** "**8. smoke의 cold 수치.** … cache 없이 처음부터 도는 smoke의 시간은 기록에 없고, real simulator로 Phase 10에서 잽니다."
- **Becomes:** **8. smoke의 cold 수치 — 닫힘.**
  - 2026-11-14의 cold smoke(10.4)는 RQ0 gate spec의 run 목록을 seed 2개로 돌렸습니다. 129개 파일의 1,197 run을 real simulator(`simulator@0d323c84470a`)와 real daemon 위에서 빈 cache로 돌렸습니다.
  - 첫 smoke(13:04:18 시작)는 1,151 run에서 멈췄습니다. 대체 driver table 아래의 153 run이 records schema check에서 실패했고, harness 쪽에서 고쳤습니다.
  - 둘째 smoke는 18:54:22에 시작해 22:20:57에 1,197 run을 모두 끝냈습니다(실패 없음).
  - 둘째 smoke의 run 시간과 byte에서 전체 run의 투영(상한 50.33 h)이 나왔습니다.
  - RQ0 run 자체가 cold로 돌아 45 h 26 min이 걸렸습니다.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "before the cold smoke…" (Commands: "1 197 runs over its 129 files"); `_dev/research/jioh/task-10.4-cold-smoke-and-cost-response/README.md`, "The first smoke", "The second smoke", "The projection"; `docs/rq0-run-record.md`, "The run"

### g2-18 · `docs/guidebook/dataset/08-decision-chronicle.md:1877` · C · items 2, 5, 6, 11, 13, 15
- **Now:** "> **열린 자리.** Phase 10의 시작은 인경민의 통합 gate와 박이안의 daemon에 달려 있습니다(TODO). simulator 쪽 세 항목 (g), (h), (j)는 인경민이, `c6-dual` records 비용의 대응은 Phase 10에 인지오가 정합니다. trace-replay 점검의 실행 결과에 따라 "what a disagreement leads to"가 이미 gate spec에 고정되어 있어야 한다는 것이 TODO 줄의 조건입니다."
- **Becomes:** the box goes, because no part of it is still open. It is replaced by text:
  - Phase 10은 2026-11-01에 열렸습니다. RQ0 run은 `daemon/daemon.py`로 돌았습니다.
  - Phase 10은 통합 gate(2026-11-14), 비용 대응(2026-11-15), RQ0 run(2026-11-16 → 11-18)을 거쳐 판정 fail, 6 of 19, provisional로 끝났습니다.
  - 2026-11-21: 재측정 뒤 판정은 final이 되었습니다. fail, 판정 파일 19개 중 5개가 g를 넘음, K = 10입니다(RQ0 run의 programs 위에서).
  - 고친 programs 위의 post hoc reading은 4 of 19이고 판정이 아닙니다.
  - failure procedure의 configuration search(2026-11-21)가 이름 붙인 route는 table rewrite입니다. 10개 파일 중 8개가 finding 3(prior table이 놓친 spread)이고, `c7-transcode`와 `c7-gaming`은 finding 2입니다.
  - route의 고침(table rewrite), 두 번째 RQ0 gate spec, 두 번째 RQ0 run은 Phase 12입니다.
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decisions 2, 3; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…", 2026-11-15 "the cost response…"; `docs/rq0-run-record.md`, "The outcome"; "Corrections", 2026-11-21, "The closing" and the post hoc line after it; "The failure procedure", 2026-11-21; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1

### g2-19 · `docs/guidebook/dataset/08-decision-chronicle.md:1885` · A · item 14 (the hold-time plan's step 1)
- **Now:** "남은 것은 둘입니다. 첫째는 그 측정, 계획의 step 1입니다. "the need measured with no rule — … — right after Phase 10's integration, in the RQ0 run's pipeline; no LLM needed. …""
- **Becomes:** the quote stays, dated as the TODO line of 2026-10-14. After it:
  - 2026-11-01: Phase 10 spec 결정 7이 그 측정을 Phase 10 밖, phase가 끝난 뒤로 두었습니다.
  - 2026-11-18: Phase 11 spec 결정 10이 그 측정을 Phase 12의 두 번째 RQ0 run 뒤로 옮겼습니다("runs after Phase 12's second RQ0 run, on the table and programs that run uses").
- **From:** `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 7; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10
- **Flags:** for 인지오: the sentence at the end of the paragraph ("계획의 When 표는 … 0이라고 적습니다") depends on how this sweep restates the hold-time plan file's When table row. Phase 11 decision 10 itself says "its When table numbers it 0". Check that sentence after that row lands.

### g2-20 · `docs/guidebook/dataset/08-decision-chronicle.md:1893` · A · item 14 (the hold-time plan's step 1)
- **Now:** "hold time의 규칙 없는 측정(step 1)은 Phase 10 통합 직후,"
- **Becomes:** hold time의 규칙 없는 측정(step 1)은 Phase 12의 두 번째 RQ0 run 뒤에 합니다. The box stays, because its other places are still open.
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10

### g2-21 · `docs/guidebook/dataset/08-decision-chronicle.md:1920` · C · items 6 (the re-measurement contingency fired), 10 (the re-measurement and the second bless)
- **Now:** "- **사전 등록된 조건부 재측정.** 9.14 결정 3의 "The re-measurement of the exception-carried values (…) is a pre-registered contingency." 조건이 맞을 때만 실행됩니다."
- **Becomes:** the bullet keeps its place and its quote, and states that the matter is closed:
  - RQ0 run에서 조건이 맞았습니다. carried-half-width line의 lower bound가 `c7-ml-train`을 g 너머로 옮겼습니다(5 to 6, fail).
  - 11.3이 예외로 실린 값을 하나씩 옮겨, 그렇게 만든 값이 `cpu-batch`의 `python3`의 run between voluntary blocks(−27.3 %)임을 찾았습니다. 그 값만으로 gap이 2.512에서 0.000이 됩니다.
  - 이 값은 RQ0 gate spec의 statement `re-measurement-contingency`가 적은 실린 값의 목록에 있고, 9.14 결정 3의 인용에는 없습니다.
  - 2026-11-21: campaign `meas-ci:background:2026-11-20`에서 107 repeats로 다시 쟀습니다. run 55.27 s ±5.89 %, block per run 403.96 µs ±2.15 %이고, 둘 다 예외 class를 유지합니다.
  - 같은 날 second bless가 있었습니다. 판정은 final이 되었습니다(fail, 5 of 19).
- **From:** `docs/rq0-run-record.md`, "The outcome" (contingency fired); "Corrections", 2026-11-21 (the finding table, the campaign table, "Both values keep their exception class", "The closing"); `harness/experiments/rq0-gate.yaml`, statement `re-measurement-contingency`; `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry

### g2-22 · `docs/guidebook/dataset/08-decision-chronicle.md:1930` · D · outside the fifteen items
- **Now:** "고쳐짐. 첫 줄이 "(v0.2)"(2026-10-16, 커밋 `37c2e233`, 11.5)"
- **Becomes:** (left alone) "11.5" looks like a slip. Commit `37c2e233` is 9.15's batched rebuild ("fix(jioh/phase-9): 9.15 — the batched dataset rebuild…"), and the passage's own 11.5 section at line 1712 says 9.15 too. The section is dated "(2026-10-14 현재)". No item of the fifteen touches it.

### g2-23 · `docs/guidebook/dataset/08-decision-chronicle.md:1939` · E · item 10 (the second bless), with items 1, 2, 6, 11
- **Now:** chapter 13's one-page timeline ends with the row "| 2026-10-31 | 측정된 프로그램 자신의 wake를 … core set, variant, generated layer rebuild와 re-bless, re-pin | …|"
- **Becomes (proposed, if 인지오 rules it in):** add one dated row, at the 2026-10-31 row's detail. It would read: "2026-11-21 | 11.3: `cpu-batch`의 `python3`의 run between voluntary blocks와 block per run을 107 repeats로 재측정(`meas-ci:background:2026-11-20`), second bless(일곱 manifest; core 3, variant 14와 생성 파일만 `meta` 밖에서 바뀜), RQ0 판정 final(fail, 5 of 19). records: `_dev/research/jioh/task-11.3-the-re-measurement/`; `harness/CHANGELOG.md`; `docs/rq0-run-record.md`". Rows for 2026-11-01, 2026-11-14 and 2026-11-16 → 11-18 would follow only if the timeline is to carry non-dataset events.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry; `docs/rq0-run-record.md`, "Corrections", 2026-11-21
- **Flags:** for 인지오 (cannot decide): two spec decisions point opposite ways here.
  - Decision 6 adds members to a passage that enumerates. The timeline is a dated list, and it already carries a post-Phase-9 dataset rebuild (2026-10-31).
  - Decision 14 says corrections only, with no section for the re-measurement and the second bless. A table row is not a section, but it is new content.

### g2-24 · `docs/guidebook/dataset/08-decision-chronicle.md:1987` · A · items 7–15 (Phase 11); item 10 (the re-measurement and the second bless)
- **Now:** "- **phase** — `_dev/TODO.md`의 인지오 section에 번호가 붙은 작업 단위입니다. 데이터셋과 직접 관계된 것은 Phase 1, 2, 3, 7, 9입니다."
- **Becomes:** …데이터셋과 직접 관계된 것은 Phase 1, 2, 3, 7, 9, 11입니다(11은 11.3의 재측정과 second bless). The location half may also say that closed phases are in `_dev/TODO-done.md`, as in g2-01.
- **From:** as g2-01
- **Flags:** for 인지오: the same judgement as g2-01.

### g2-25 · `docs/guidebook/dataset/08-decision-chronicle.md:2116` · B · item 9 (the simulator's stage AF)
- **Now:** "- **voluntary block** — task가 스스로 CPU를 내려놓고 I/O나 신호를 기다리는 것입니다."
- **Becomes:** …I/O나 신호를 기다리는 것입니다. simulator에서는 2026-11-19부터 `fork_cap`에 차서 자리를 기다리는 `FORK`도 그렇습니다(stage AF).
- **From:** as g2-03
- **Flags:** for 인지오: same caveat as g2-03 (a gloss, not a closed list).

### g2-26 · `docs/guidebook/dataset/08-decision-chronicle.md:109` (and the volume as a whole) · D · item 10 (the re-measurement and the second bless): no section, by decision 14
- **Now:** §1.5's five segments end at "10-17/18 … 9.15, 9.16 끝 / Phase 9 끝"; the opening's last dated event is Phase 9's end (line 11).
- **Becomes:** (left alone) The chronicle has no section for Phase 10 or Phase 11. That includes the re-measurement of `cpu-batch`'s `python3` (`meas-ci:background:2026-11-20`) and the second bless of 2026-11-21, its last dataset change. Spec decision 14 leaves this as it is, and the Backlog line that decision names records it. Only 12.4's eight items, its box, and the phase-count sentences (g2-01, g2-24) are corrected.

## `docs/guidebook/dataset/03-timeline-to-canonical-workload.md`

### g2-27 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:11` · A · item 10 (the second bless)
- **Now:** "설명하는 것은 2026-10-14 기준의 tree이고, 그 뒤 2026-10-17까지 바뀐 것(…)은 해당 절에 반영했습니다."
- **Becomes:** …그 뒤 바뀐 것은 해당 절에 반영했습니다. The parenthesis keeps its list and gains two items: the 2026-10-31 re-bless that split a measured program's own wakes by origin, which the volume already describes in 7.7, and the `c2-p1a` training job after the 2026-11-21 second bless (6.2, 11.6).
- **From:** `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry ("3 of the core set's 51 (`c1-ml-train`, `c2-p1a`, `c7-ml-train`)"); `harness/CHANGELOG.md`, 2026-10-31 "a measured program's own wakes by origin"
- **Flags:** for 인지오: the 2026-10-31 half is stale from outside the fifteen items (a D part). The volume already carries the 2026-10-31 content and its header reads "Updated 2026-10-31". The second-bless half follows only if g2-31 and g2-35 apply.

### g2-28 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:75` · A · items 1 (`claim-links`), 7 (the scorer's sign rule)
- **Now:** "이 workload들에서 scheduler 설정의 선택이 측정할 만큼 결과를 바꾸는지를, 완벽한 인식(oracle)과 무작위 인식을 비교해 묻습니다(…). 그 차이를 headroom이라고 부릅니다."
- **Becomes:** …비교해 묻습니다. 판정은 판정 파일마다 `random` seed 평균과 `oracle` 사이의 gap을 봅니다(K개 이상의 파일에서 g 이상이면 통과). headroom은 그와 따로, oracle이 boot default(`fixed`)보다 나은 것입니다(statement `claim-links`, 2026-11-01). 2026-11-18부터는 부호를 읽어, oracle이 `fixed`보다 floor 이상 나쁜 term은 headroom이 없고 `oracle_worse`로 표시됩니다.
- **From:** `harness/experiments/rq0-gate.yaml`, `criterion` (`k_of_n_gap`, reference `oracle`, compared `random`) and statement `claim-links` ("headroom, the oracle improving on fixed … read apart from the criterion's gap"); `harness/CHANGELOG.md`, 2026-11-01 and 2026-11-18; `docs/harness/metrics.md` §9
- **Flags:** for 인지오: this use of "headroom" goes back to the 2026-08-23 Q8 "headroom admission test" (an oracle-vs-random gap). The line may have been loose before Phase 10. It is listed because `claim-links` separates the two terms explicitly.

### g2-29 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:136` · B · items 2 (the integration gate), 10 (the re-measurement)
- **Now:** "이 권은 결정을 인용할 때 … 이 권에 나오는 기록을 한 번 모아 둡니다." with a table running from "2026-08-26 grill" to "2026-10-10 audit".
- **Becomes:** if g2-31, g2-33, g2-35 and g2-36 apply, the table gains rows at its neighbours' detail:
  - "10.2 | 통합 gate. simulator 적합성 항목 (a)–(j)가 binary 위에서 | `_dev/docs/spec/jioh/task-10.2-integration-gate.md`, `_dev/research/jioh/task-10.2-integration-gate/`"
  - "11.3 | 재측정과 second bless. `cpu-batch`의 `python3` | `_dev/docs/spec/jioh/task-11.3-the-re-measurement.md`, `_dev/research/jioh/task-11.3-the-re-measurement/`"
- **From:** `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…" (spec path) and 2026-11-21 re-measurement entry (spec path)
- **Flags:** for 인지오: this row is conditional on the corrections that would cite these records. The table already lacks the timer-wakes-by-origin spec (`_dev/docs/spec/jioh/timer-wakes-by-origin.md`), which 7.7 cites as "timer-wakes-by-origin spec 결정 4". That gap is stale from outside the items (a D part).

### g2-30 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:491` · A · item 5 (the starvation net reopened and settled)
- **Now:** "기아(starvation)를 막는 안전망은 simulator가 만들지 않고, harness의 `starvation_floor` guard가 모든 task의 대기를 30 s로 제한합니다."
- **Becomes:**
  - 기아를 막는 안전망은 simulator가 만들지 않습니다. 2026-11-15의 cold smoke에서 그 질문이 다시 열렸고, 인지오는 계약 그대로 두기로 정했습니다(안전망도 simulator 변경도 없음).
  - harness의 `starvation_floor` guard는 task가 ready로 30 s를 넘게 기다린 run을 실패로 둡니다.
  - guard가 읽지 못하는 두 대기가 있습니다: workload나 task의 끝에 아직 열린 대기와, 선점 뒤의 대기입니다. 이 둘은 `simulator/tools/wait_check.py`가 trace에서 읽습니다.
- **From:** `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md`, TL;DR and §7; `harness/experiments/rq0-gate.yaml`, statement `sensitivity-lines`; `harness/CHANGELOG.md`, 2026-11-15 "before the RQ0 run: the wait check's rule…"

### g2-31 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:983` (and 986) · A · item 10 (the re-measurement and the second bless)
- **Now:** "{"op": "RUN", "us": 192}, {"op": "SLEEP", "us": 378}, {"op": "RUN", "us": 135}, {"op": "SLEEP", "us": 359}, …" and "명령어는 56개뿐입니다(RUN 28, SLEEP 27, EXIT 1). 23분짜리 job이 56개 명령어인 것은, … block이 0으로 나오면(…) 앞뒤 run을 하나로 합칩니다(11.6절). 그래서 RUN 하나가 685,714,830 µs, 약 11.4분짜리도 있습니다. RUN 28개를 모두 더하면 정확히 1,389,885,000 µs, 즉 `total_work`입니다."
- **Becomes:**
  - The JSON excerpt reads `{"op": "RUN", "us": 191}, {"op": "SLEEP", "us": 472}, {"op": "RUN", "us": 159}, {"op": "SLEEP", "us": 450}, …`.
  - 명령어는 96개입니다(RUN 48, SLEEP 47, EXIT 1).
  - 가장 긴 RUN은 560,069,421 µs(약 9.3분)이고, RUN 48개를 더하면 정확히 1,389,885,000 µs, 즉 `total_work`입니다.
  - 명령어가 적은 것은 측정된 run 표(`python3_run`)의 run이 길기 때문입니다(max 1,297,955,204 µs). block 표(`python3_block`)는 min이 1 µs라서 합치기는 일어나지 않습니다.
  - 이 program은 2026-11-21의 second bless 뒤의 것입니다. `python3`의 run과 block 값은 11.3의 재측정(`meas-ci:background:2026-11-20`)에서 왔고, CPU 총량과 timeline의 `source`는 그대로입니다.
- **From:** the artifact `dataset/build/coreset-single/c2-p1a.workload.json` (its SHA-256 `0678efa68cef…` is the committed `dataset/build.manifest.json` entry; read with `python3`: the hog's program, its first four instructions, its counts, its largest RUN, its sum); `dataset/archetypes.yaml`, `cpu-batch` `python3_run` and `python3_block` (lines 1256–1259, source `meas-ci:background:2026-11-20`) and the scope ("every other value of the program is the 9.10 campaign's"); `harness/CHANGELOG.md`, 2026-11-21 re-measurement entry; `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json` (`c2-p1a` in `beyond_hash`)
- **Flags:** for 인지오: the explanation "block이 0으로 나오면 … 합칩니다 … 그래서 RUN 하나가 …" was never true for `python3`. Its 9.10 block table had min 12 µs (`dataset/archetypes.yaml` at `17f28d7f`, `37c2e233`, `b5678087`), so the old long RUN came from the run table, not from merging. That is a D part, stale from outside the items. The row rewrites the explanation because item 10 forces the paragraph to be rewritten anyway. "약 9.3분" is arithmetic on the artifact's µs.

### g2-32 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:1213` · A · item 2 (the integration gate passed)
- **Now:** "| `children:<task id>` | 빌드 orchestrator가 모든 자식을 낳은 뒤 | 파일 안에는 깨우는 것이 없음. 자식이 모두 끝났을 때 executor가 완료(제안된 규칙, 아래) | `children:build` |"
- **Becomes:** …자식이 모두 끝났을 때 executor가 완료(conformance 항목 (g); 2026-11-11 stage AA로 구현, 아래) | `children:build` |
- **From:** `simulator/memo/memo_261111.md`, Part B; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…"
- **Flags:** the "제안된 규칙" label was already overtaken on 2026-10-31, when the rule was agreed. That date is outside the fifteen items, and the box below states it.

### g2-33 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:1219` · C · item 2 (the integration gate passed)
- **Now:** "> **열린 자리.** `children:<id>` channel을 깨우는 사건은 canonical 파일에 없습니다. … 지금의 reference simulator는 이 channel을 보통 channel로 다루어(`simulator/src/sim.cpp`의 `on_task_end`는 fork 자리만 돌려줍니다), 자식이 다 끝나도 orchestrator가 막힌 채로 남습니다. 그래서 `c1-compile`의 build turnaround를 재려면 이 구현이 먼저 있어야 하고, RQ0 gate spec은 이것을 simulator 적합성 항목 (g)로 적습니다(…)."
- **Becomes:** the box goes. Its rule sentences stay as ordinary text: the 2026-10-16 decision, the contracts' wording, and 인경민's verbal agreement of 2026-10-31. The "지금의 reference simulator …" sentences become:
  - 인경민이 2026-11-11에 stage AA로 구현했습니다. orchestrator의 WAIT는 마지막 자식의 `task_end` 바로 뒤에 `ready(wake)`로 끝나고, 살아 있는 자식이 없으면 대기 0으로 끝납니다.
  - 2026-11-14의 통합 gate가 그것을 `simulator@0d323c84470a`의 binary 위에서 보였습니다. 보인 것은 fixture `fix-object`, `fix-tree`의 재생과 black-box unit test `simulator/tests/test_spawn_children.py`입니다.
- **From:** `simulator/memo/memo_261111.md`, Part B; `harness/CHANGELOG.md`, 2026-11-13 (`fix-object`, `fix-tree` as item (g)'s evidence) and 2026-11-14 "the integration gate passed…"; `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md` §2 (the `test_spawn_children.py` row)

### g2-34 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:1305` · A · item 2 (the integration gate passed: the mocks are test fixtures only, `daemon/daemon.py` in the repository)
- **Now:** "> **코드로.** 이 규칙의 참조 구현은 harness의 mock daemon입니다(`harness/tools/tests/mocks/daemon.py`의 `projection`)."
- **Becomes:**
  - 이 규칙을 구현하는 것은 `daemon/daemon.py`의 `projection`입니다(RQ0 run의 daemon, `daemon@62c71f0d2de0`).
  - harness의 mock daemon(`harness/tools/tests/mocks/daemon.py`의 `projection`)은 test fixture로 남습니다.
  - 2026-11-14의 통합 gate에서 두 daemon은 RQ0 gate spec의 run 19,425개 모두에서 schedule과 log가 byte까지 같았습니다.
  - The step-by-step description that follows stays: it fits both.
- **From:** `daemon/daemon.py`, `def projection` (line 70); `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…" ("the daemon byte-identical to the mock daemon on the 19 425 runs"); `_dev/research/jioh/task-10.2-integration-gate/README.md`, part `daemon`; `_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 3
- **Flags:** for 인지오: `daemon/README.md` (박이안's tree) still calls the mock "the harness's reference mock". The guidebook sentence is false only in naming the mock as the implementation. The correction is wording in this doc and changes nothing in the daemon tree.

### g2-35 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:1673` · A · item 10 (the re-measurement and the second bless)
- **Now:** "`c2-p1a`의 학습 job이 56 명령어인 이유가 3단계입니다(6.2절). MNIST 학습의 측정 block 표는 0이 많아서, 대부분의 run이 합쳐져 수 분짜리 RUN이 됩니다."
- **Becomes:**
  - `c2-p1a`의 학습 job은 96 명령어(RUN 48, SLEEP 47, EXIT 1)입니다(6.2절).
  - MNIST 학습의 측정 run 표(`python3_run`, `meas-ci:background:2026-11-20`)가 voluntary block 사이의 긴 run을 담고 있어(p90 1,177,733,035 µs, max 1,297,955,204 µs) RUN이 수 분짜리가 됩니다.
  - block 표(`python3_block`)는 0을 담지 않으므로(min 1 µs) 3단계의 합치기는 이 job에서 일어나지 않습니다.
  - 0이 많은 block 표의 예로는 `kdenlive_render_block`(p의 앞 여덟이 0)을 들 수 있습니다.
- **From:** `dataset/archetypes.yaml`, `cpu-batch` params (lines 1256–1263); the artifact and manifest as in g2-31
- **Flags:** for 인지오: same D part as g2-31. The "0이 많아서" reason was never true for `python3` (9.10 table min 12 µs). Proposing `kdenlive_render` as the example goes beyond a pure correction; the line can be dropped instead.

### g2-36 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:2240` · C · item 2 (the integration gate passed)
- **Now:** "**2. `children:<id>` channel을 누가 깨우나 — 규칙은 정해졌고 동의됨, 구현을 기다림.** … 구현될 때까지 reference simulator에서는 `c1-compile`의 build turnaround를 잴 수 없고, RQ0 gate spec이 그 구현을 simulator 적합성 항목 (g)로 요구합니다(7.7절). 인경민의 구현 대기."
- **Becomes:** **2. `children:<id>` channel을 누가 깨우나 — 닫힘.** The rule and its agreement stay. The last two sentences become: 인경민이 2026-11-11에 simulator의 stage AA로 구현했고, 2026-11-14의 통합 gate가 그것을 binary 위에서 보였습니다(7.7절).
- **From:** `simulator/memo/memo_261111.md`, Part B; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…"

### g2-37 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:2252` · A · item 2 (the integration gate passed); the per-item check still open
- **Now:** "위의 2(`children:<id>` channel, 항목 (g))는 그대로 열려 있고, 4(TIMER skip 규칙, 항목 (b))는 2026-10-23에 구현되었습니다. (b)에 기대는 문장의 확인은 기록에 아직 없습니다."
- **Becomes:** 위의 4(TIMER skip 규칙, 항목 (b))는 2026-10-23에, 2(`children:<id>` channel, 항목 (g))는 2026-11-11에 구현되었고, 2026-11-14의 통합 gate가 두 항목을 binary 위에서 보였습니다. (b)와 (g)에 기대는 문장의 확인(`compiled/uncheckable-by-item.md`의 "Check" 줄)은 기록에 아직 없습니다.
- **From:** `simulator/memo/memo_261111.md`, Part B; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed…"; still open: `_dev/research/jioh/task-9.16-exit-audits/compiled/uncheckable-by-item.md`, the (b) and (g) "Check" lines, unchanged since `b51df8a4` (2026-10-17), with no later record of those checks

### g2-38 · `docs/guidebook/dataset/03-timeline-to-canonical-workload.md:2362` · A · item 1 (`claim-links`)
- **Now:** "| `RQ0` | project | 첫 관문 실험. oracle과 무작위 조건 사이에 headroom이 있는지 묻는 것(1.2) |"
- **Becomes:** | `RQ0` | project | 첫 관문 실험. 판정 파일 K개 이상에서 `random` seed 평균과 `oracle` 사이의 gap이 g 이상인지 묻는 것. headroom(oracle이 `fixed`보다 나음)은 따로 셈(1.2) |
- **From:** `harness/experiments/rq0-gate.yaml`, `criterion` and statement `claim-links`
- **Flags:** for 인지오: same caveat as g2-28.

## Added at K2's review (2026-11-21)

### g2-39 · `docs/guidebook/dataset/08-decision-chronicle.md:1849` · A · item 2 (the integration gate passed)
- **Now:** "compile된 숫자에 관한 문장 가운데 참인지가 reference simulator가 아직 구현하지 않은 executor 규칙에 달린 것은, …"
- **Becomes:** the clause dated to the decision: "…참인지가 그때(2026-10-17) reference simulator가 아직 구현하지 않은 executor 규칙에 달린 것은, …" — the box under it (g2-08) carries the current state
- **From:** `_dev/docs/spec/jioh/task-9.16-exit-audits.md`, decision 6; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"
