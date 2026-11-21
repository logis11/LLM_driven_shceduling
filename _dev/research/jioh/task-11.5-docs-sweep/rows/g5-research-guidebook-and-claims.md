# Rows — g5, the research guidebook and the claims

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/guidebook/README.md` | 46 | 7 | 0/0/0/0/0 |
| `docs/guidebook/vol-01-systems-and-scheduling.md` | 3780 | 25 | 1/0/0/0/0 |
| `docs/guidebook/vol-02-related-work.md` | 3964 | 11 | 1/0/0/0/0 |
| `docs/guidebook/vol-03-the-research.md` | 3896 | 32 | 7/2/1/2/3 |
| `docs/guidebook/vol-04-experiment-design.md` | 1897 | 7 | 5/2/0/1/0 |
| `docs/guidebook/vol-05-shared-vocabulary.md` | 2741 | 4 | 1/0/0/0/0 |
| `docs/guidebook/vol-06-archetypes-and-grounding.md` | 4207 | 33 | 0/0/1/0/0 |
| `docs/research-claims.md` | 368 | 30 | 2/0/0/0/0 |
| `docs/research-proposal.md` | 949 | 27 | 3/1/0/1/1 |
| `docs/terminology.md` | 362 | 12 | 0/1/0/1/2 |
| `docs/background-guide.md` | 260 | 8 | 2/0/0/0/1 |
| `docs/related-work.md` | 82 | 2 | 1/0/0/0/0 |

Beyond the term list, each volume was also searched for `RQ0`, the training run's old values (`69`, `27.3`), the floor rule (`절댓값`, `하한`, `여유 없음`), `fork`/`B1`, phase counts and the guidebook's markers (`미실행`, `미정`, `확인 필요`). Files under 400 lines were read whole.

### g5-01 · `docs/guidebook/vol-01-systems-and-scheduling.md:1349` · A · item 10 (the re-measurement)
- **Now:** "학습은 thread 하나가 한 번 잡으면 평균 69초 넘게 잠들지 않고 계산합니다."
- **Becomes:** "평균 55초 넘게" — 2026-11-21 재측정 값 55.27초.
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table ("run between voluntary blocks … 55.27 s ±5.89 %"); `dataset/archetypes.yaml`, `cpu-batch`'s `python3` note (line 1272)

### g5-02 · `docs/guidebook/vol-02-related-work.md:1429` · A · item 10 (the re-measurement)
- **Now:** "학습: thread 하나가 한 번 잡으면 평균 69초 넘게 잠들지 않고 계산한다."
- **Becomes:** "평균 55초 넘게".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-03 · `docs/guidebook/vol-03-the-research.md:1339` · D
- **Now:** "설정에 있는 상한은 batch class의 상한 하나이고, 시뮬레이터는 아직 그것을 집행하지 않습니다."
- **Why left:** stale before Phase 10, no item: the simulator enforces the cap since its stage V, 2026-10-20 (`simulator/steps/README.md`, row v); the volume's own glossary (line 3794) already says so.

### g5-04 · `docs/guidebook/vol-03-the-research.md:1562` · A · item 10 (the re-measurement)
- **Now:** "thread 1개, 평균 69초 / 넘게 잠들지 않고 계산"
- **Becomes:** "평균 55초 / 넘게" (the text box keeps its column width).
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-05 · `docs/guidebook/vol-03-the-research.md:1697` · A · item 1 (the RQ0 gate spec's pre-run lines)
- **Now:** "link 2에는 어떤 결과가 나오면 끊어진 것으로 칠지, 곧 **반증 조건**이 아직 없습니다."
- **Becomes:** link 2는 첫 관문 실험의 headroom 개수 줄이 읽습니다. primary 아래에서 headroom이 있는 판정 파일이 하나도 없으면 — `fixed`가 모든 판정 파일의 모든 항목에서 `oracle`의 결과에 닿으면 — 끊어진 것으로 칩니다(2026-11-01).
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`; `harness/CHANGELOG.md`, 2026-11-01

### g5-06 · `docs/guidebook/vol-03-the-research.md:1777` · A · items 1 (the pre-run lines), 6 (the RQ0 run), 7 (the sign rule)
- **Now:** "**아직 이 link를 시험하는 조건이 없습니다.** … 명세(`harness/experiments/rq0-gate.yaml`)가 시험하는 것은 link 1입니다. … link 1은 그 명세가 시험하고, link 3은 데이터셋을 만드는 방식이 지키며, link 2에는 아직 반증 조건이 없다는 것입니다."
- **Becomes:** 첫 관문 실험의 명세가 link 1을 판정 기준으로, link 2를 headroom 개수 줄로 시험합니다(2026-11-01, statement `claim-links`). 둘은 따로 읽습니다 — `random`이 headroom을 잡아낸 파일은 link 1의 읽기에서 떨어지고 link 2의 읽기에서는 떨어지지 않습니다. RQ0 실행(2026-11-16~18)에서는 primary 아래 19개 중 17개에 headroom이 있어 link 2가 섰습니다. 부호 규칙으로 다시 읽은 사후 읽기(판정 아님, 2026-11-18)에서는 19개 중 12개입니다. 주장 문서도 같은 것을 적습니다.
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`; `docs/rq0-run-record.md`, "The outcome" ("Link 2 stands … 17 of the 19"); same record, Corrections, 2026-11-18 ("12 of 19 have headroom")
- **Flags:** for 인지오: the record says "link 2 stands" only of the as-run count. That 12 of 19 also leaves it standing follows from `claim-links`' rule (falsified at 0), but no record states it.

### g5-07 · `docs/guidebook/vol-03-the-research.md:1785` · C · items 1 (the pre-run lines), 6 (the RQ0 run), 7 (the sign rule)
- **Now:** "> **미정.** 어떤 결과가 나오면 이 link가 끊어진 것으로 칠지는 어느 기록에도 정해져 있지 않습니다. 주장 문서는 link 2를 한 문장으로 적고 반증 조건은 아직 없다고 말하며, 첫 관문 실험의 명세에도 link 2에 대한 조건은 없습니다."
- **Becomes:** the box goes; nothing in it is still open. As text: 2026-11-01에 첫 관문 실험의 명세가 link 2의 반증 조건을 정했습니다(statement `claim-links`). primary 아래에서 headroom이 있는 판정 파일이 하나도 없으면 끊어진 것이고, 판정 기준의 간격과 따로 읽습니다. RQ0 실행에서는 19개 중 17개에 headroom이 있어 link 2가 섰고(`docs/rq0-run-record.md`), 부호 규칙의 사후 읽기에서는 12개입니다(같은 기록, 2026-11-18 정정).
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`; `harness/CHANGELOG.md`, 2026-11-01; `docs/rq0-run-record.md`, "The outcome"; same record, Corrections, 2026-11-18

### g5-08 · `docs/guidebook/vol-03-the-research.md:1837` · A · item 1 (the pre-run lines)
- **Now:** "link 2의 반증 조건은 아직 정해지지 않았습니다."
- **Becomes:** link 2는 첫 관문 실험의 headroom 개수 줄이 시험합니다(2026-11-01).
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`

### g5-09 · `docs/guidebook/vol-03-the-research.md:2170` · A · item 1 (the pre-run lines)
- **Now:** "link 2에는 아직 반증 조건이 없습니다." (chapter 6's summary)
- **Becomes:** link 2는 첫 관문 실험의 headroom 개수 줄이 읽고, headroom이 있는 판정 파일이 하나도 없으면 끊어집니다.
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`

### g5-10 · `docs/guidebook/vol-03-the-research.md:2269` · B · item 1 (the pre-run lines: the cap band line)
- **Now:** "세 가지를 흔듭니다. **부팅 기본값을 흔듭니다.** … **통과 간격을 흔듭니다.** … **지연 바닥값을 흔듭니다.** …"
- **Becomes:** "네 가지", with a fourth paragraph at its neighbours' level: **표의 상한을 흔듭니다.** 원치 않음 줄들의 상한(스키마 하한 0.05)을 원함 줄들의 값 0.2, 0.333, 0.5로 옮긴 세 표에서 판정 파일의 `oracle`과 `random`을 다시 돌려 다시 셉니다. 판정이 하한의 가혹함에 얼마나 기대는지를 봅니다(2026-11-01).
- **From:** `harness/experiments/rq0-gate.yaml`, statement `cap-band`; `harness/CHANGELOG.md`, 2026-11-01
- **Flags:** the passage also lacks lines that predate the items, and those stay as D: the variant lines (venue factor, chain scale, first segment's length, carried half-widths), the trace replay and the bounding pair are in the spec before 2026-11-01 (`git show b5c38398^:harness/experiments/rq0-gate.yaml`). The headroom-count line is not a shaking, so it does not belong in this list.

### g5-11 · `docs/guidebook/vol-03-the-research.md:2307` · E · items 6 (the RQ0 run), 11 (the verdict final), 13 (the configuration search), 15 (Phase 12 next)
- **Now:** "### 실패했을 때의 절차가 미리 적혀 있습니다 … **workload를 건드리기 전에, 실패한 파일 두세 개에 대해 설정 전수 탐색을 돌린다.** … 벌어지는데 표가 그걸 못 잡았으면 → 원인 3. 표를 다시 쓴다. / 이 탐색 도구는 원래 계획에 이미 있었습니다."
- **Becomes:** nothing here is false, but no passage of the research guidebook says that the RQ0 run ran, what its verdict was, or which route the search named. If 인지오 wants it here, as text: RQ0 실행(2026-11-16~18)은 실패였고, 재측정 뒤 2026-11-21에 확정됐습니다 — 판정 파일 19개 중 5개, K = 10. 실패 절차의 설정 탐색(2026-11-21)은 규칙으로 고른 세 파일(`c7-transcode`, `c7-gaming`, `c1-transcode`)과 모든 항목에 headroom이 없는 일곱 파일, 열 개에서 470개 설정을 돌렸습니다. 경로는 **표를 다시 쓴다**입니다 — 10개 중 8개에 사전 표가 놓친 폭이 있었습니다. 표를 다시 쓰는 일, 두 번째 RQ0 gate spec, 두 번째 RQ0 실행은 Phase 12에서 합니다. "두세 개" against the spec: the statement `failure-procedure` names three picks by rule, plus a judging file with no headroom on every term as an additional trigger for the table check.
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the verdict line; same record, "The failure procedure", 2026-11-21; `harness/experiments/rq0-gate.yaml`, statement `failure-procedure`; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1
- **Flags:** for 인지오: cannot decide. No statement is false. Whether the outcome goes here, or waits for the planned vol 13 ("RQ0 gate와 그 너머", 예정 in `docs/guidebook/README.md`), is a decision.

### g5-12 · `docs/guidebook/vol-03-the-research.md:2442` · E · items 11 (the verdict final), 13 (the configuration search), 15 (Phase 12 next)
- **Now:** "사전 표(prior) 측정 전에 이론으로 쓴 표. 한 줄에 항목 하나. 절대 조정하지 않는다. RQ0의 문을 이 표로 통과한다." The same role is stated at line 2631 ("RQ0의 문을 통과하는 데 쓰는 사전 표"), line 3188 ("사전 표는 측정 없이 이론으로만 썼습니다") and line 3755 (glossary: "절대 조정하지 않는다").
- **Becomes:** undecided. The RQ0 run on this table failed (fail, 5 of 19, final), and the route is that the table is rewritten in Phase 12. "이 표로 통과한다" reads as a pass. Whether the rewritten table keeps the name, the "never adjusted" rule and "written from theory before measurement" is for Phase 12 to settle, and no record states it. The minimal fix now is "통과한다" → "시험한다", plus the route.
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the verdict line; same record, "The failure procedure" ("Route: the table is rewritten"); `harness/experiments/rq0-gate.yaml`, statement `failure-procedure` (3)
- **Flags:** for 인지오: cannot decide. This depends on what Phase 12 does with the table. The same question sits in g5-30 and g5-37.

### g5-13 · `docs/guidebook/vol-03-the-research.md:2487` · D
- **Now:** "그 묶음의 구성은 통합 실행 이후에 보정 방법과 함께 정하기로 문서에 미뤄져 있습니다." The same appears at lines 3194 and 3204 ("어느 쪽이든 통합 실행 이후의 결정입니다").
- **Why left:** the normative home says "after Phase 9" (`docs/workload/building-plan.md` line 212), not after integration. The integration gate's pass (item 2) leaves the tuning set's composition unfixed, so no item closes the matter. The 미실행 box at 2485 (the held-out-rows arm, unrun) stays.

### g5-14 · `docs/guidebook/vol-03-the-research.md:2688` · B · item 1 (the pre-run lines: the cap band line)
- **Now:** "부팅 기본값 열 가지, 통과 간격 네 가지, 지연 바닥값 네 가지로 흔들어보고" (chapter 7's summary)
- **Becomes:** "…, 지연 바닥값 네 가지, 원치 않음 줄의 상한을 옮긴 표 세 가지로 흔들어보고".
- **From:** `harness/experiments/rq0-gate.yaml`, statement `cap-band`

### g5-15 · `docs/guidebook/vol-03-the-research.md:2723` · A · item 1 (the pre-run lines)
- **Now:** table cell "미정. 어느 기록도 정하지 않음. 첫 관문 실험의 명세에도 이 link의 조건이 없음. …" and line 2730 "link 2의 칸에는 반증 조건이 아직 없습니다. 어느 기록도 그것을 정하지 않았고, 첫 관문 실험의 명세도 이 link를 시험하지 않습니다. 칸에는 그 사실과 판정하지 않는 파일이 적혀 있습니다."
- **Becomes:** the cell reads "판정 파일 어느 것에도 primary 아래 headroom이 없음 — `fixed`가 모든 판정 파일의 모든 항목에서 oracle의 결과에 닿음(첫 관문 실험의 headroom 개수 줄, 2026-11-01)", and keeps its pair sentence and the frequency sentence. The three sentences at 2730 about link 2 go; the link 3 sentences there stay.
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`

### g5-16 · `docs/guidebook/vol-03-the-research.md:2796` · E · items 6 (the RQ0 run), 11 (the verdict final), 13 (the configuration search)
- **Now:** "## 8.4 손으로 따라가기: 문이 열리지 않았을 때 … 판정 파일 19개 중 간격 0.5 이상: 5개 … 실패한 14개 중 / 그 13줄에 걸리는 파일 9개 (그런 파일 9개 전부) … 실패한 파일 중 셋을 골라서 … 이 탐색 도구는 원래 계획에 이미 있었습니다. 표를 조정하는 데 쓰는 도구와 같은 도구입니다."
- **Becomes:** undecided. The hand trace is hypothetical, but its count, 5 of 19, is now the final verdict's, so a reader can take it for the run. The real run's details differ:
  - Two of the five files that met g, `c7-browsing` and `c7-office`, belong to the nine-file class (`prior-table-structure`).
  - Ten files were searched, not three.
  - The route was table-side, the hypothetical's shape B.

  Options are to mark the trace as hypothetical, to move its numbers off 5, or to follow it with the run's outcome. Separately, the tool that was built is `harness/tools/search.py`. No record says it is the calibrated table's tuning tool ("표를 조정하는 데 쓰는 도구와 같은 도구").
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the verdict line (the five files); `harness/experiments/rq0-gate.yaml`, statement `prior-table-structure` (the nine files); `docs/rq0-run-record.md`, "The failure procedure" (ten files, the route); `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry (the tool)
- **Flags:** for 인지오: cannot decide.

### g5-17 · `docs/guidebook/vol-03-the-research.md:2987` · A · item 1 (the pre-run lines)
- **Now:** "link 2의 반증 조건은 아직 어느 기록에도 정해져 있지 않고, 첫 관문 실험의 명세도 link 2를 시험하지 않습니다." (chapter 8's summary)
- **Becomes:** link 2는 첫 관문 실험의 headroom 개수 줄이 시험하고, headroom이 있는 판정 파일이 하나도 없으면 끊어집니다(2026-11-01).
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`

### g5-18 · `docs/guidebook/vol-04-experiment-design.md:191` · A · item 7 (the scorer's sign rule)
- **Now:** "천장이 얻은 개선폭의 절댓값이 이 하한보다 작으면, **그 파일의 그 지표에 대해서는 비율을 아예 만들지 않습니다.** 원래 값만 보고하고 "여유 없음"이라고 표시합니다."
- **Becomes:** 천장의 개선폭을 부호까지 읽어 이 하한보다 작으면 — 크기가 하한 아래이거나, 천장이 바닥보다 하한 이상 나쁘면 — 비율을 만들지 않고 원래 값만 보고하며 "여유 없음"으로 표시합니다. 천장이 바닥보다 하한 이상 나쁜 항목에는 *oracle worse than fixed* 표시가 따로 붙어 두 경우를 가릅니다(2026-11-18). 11.1 corrected only the glossary rows at 1824–1825; this body passage still states the old absolute-value rule.
- **From:** `docs/harness/metrics.md` §9, the Floor paragraph, and its changelog, 2026-11-18; `harness/CHANGELOG.md`, 2026-11-18

### g5-19 · `docs/guidebook/vol-04-experiment-design.md:221` · A · item 1 (the pre-run lines)
- **Now:** "link 2에는 아직 반증 조건이 없습니다."
- **Becomes:** link 2는 같은 명세의 headroom 개수 줄이 읽습니다. `oracle`이 `fixed`보다 나은 항목이 있는 판정 파일이 primary 아래 하나도 없으면 끊어진 것으로 칩니다(2026-11-01, statement `claim-links`).
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`

### g5-20 · `docs/guidebook/vol-04-experiment-design.md:249` · A · item 7 (the scorer's sign rule)
- **Now:** "천장이 얻은 개선폭이 너무 작으면 비율을 만들지 않습니다." (chapter 1's summary)
- **Becomes:** 천장의 개선폭이 하한보다 작거나 천장이 바닥보다 하한 이상 나쁘면 비율을 만들지 않고, 뒤엣것에는 *oracle worse than fixed* 표시가 따로 붙습니다.
- **From:** `docs/harness/metrics.md` §9, the Floor paragraph

### g5-21 · `docs/guidebook/vol-04-experiment-design.md:1093` · A · item 10 (the re-measurement)
- **Now:** "학습은 thread 하나가 스스로 멈추기 전까지 평균 69.49초(±27.3%)를 계산하고"
- **Becomes:** "평균 55.27초(±5.89%)".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-22 · `docs/guidebook/vol-04-experiment-design.md:1157` · A · item 7 (the scorer's sign rule)
- **Now:** "천장이 바닥보다 거의 나아지지 않으면 비율을 만들지 않고 표시를 답니다. 합산할 때는 만점을 받은 것처럼 들어갑니다."
- **Becomes:** 천장이 바닥보다 거의 나아지지 않거나 하한 이상 나쁘면 비율을 만들지 않고 표시를 답니다. 뒤엣것에는 *oracle worse than fixed* 표시가 함께 붙습니다. 합산할 때는 만점을 받은 것처럼 들어갑니다.
- **From:** `docs/harness/metrics.md` §9, the Floor and Composition paragraphs

### g5-23 · `docs/guidebook/vol-04-experiment-design.md:1318` · D
- **Now:** "2026-09-12에 얼린 1.0이 처음 고정됐고, 지금은 2026-10-09의 1.1이 RQ0 gate spec에 고정되어 있습니다."
- **Why left:** stale before Phase 10. The RQ0 gate spec pins guard spec 1.4, dated 2026-10-31 (`harness/CHANGELOG.md`, 2026-10-31; `harness/experiments/rq0-gate.yaml` pins), and no item moved it.

### g5-24 · `docs/guidebook/vol-04-experiment-design.md:1725` · B · item 1 (the pre-run lines: the cap band line)
- **Now:** "세 가지를 흔듭니다. **기본 설정값.** … **통과 간격.** … **지연 하한.** …"
- **Becomes:** "네 가지", with a fourth paragraph at its neighbours' level: **표의 상한.** 원치 않음 줄들의 상한(스키마 하한 0.05)을 원함 줄들의 값 0.2, 0.333, 0.5로 옮긴 세 표로 다시 셉니다. 판정이 그 하한의 가혹함에 얼마나 기대는지를 봅니다.
- **From:** `harness/experiments/rq0-gate.yaml`, statement `cap-band`; `harness/CHANGELOG.md`, 2026-11-01
- **Flags:** the variant lines, the trace replay and the bounding pair are also missing here. They predate the items and stay as D, as in g5-10.

### g5-25 · `docs/guidebook/vol-04-experiment-design.md:1784` · B · item 1 (the pre-run lines: the cap band line)
- **Now:** "기본 설정값, 통과 간격, 지연 하한 셋을 흔들고" (chapter 10's summary)
- **Becomes:** "기본 설정값, 통과 간격, 지연 하한, 표의 상한 넷을 흔들고".
- **From:** `harness/experiments/rq0-gate.yaml`, statement `cap-band`

### g5-26 · `docs/guidebook/vol-05-shared-vocabulary.md:2172` · A · item 10 (the re-measurement)
- **Now:** "학습은 thread 하나가 스스로 멈추기 전까지 평균 69초 넘게 계산하는 작업이고"
- **Becomes:** "평균 55초 넘게".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-27 · `docs/guidebook/vol-06-archetypes-and-grounding.md:3732` · C · items 6 (the RQ0 run), 15 (Phase 12 next)
- **Now:** "> 누가 정해야 하나: RQ0 gate의 판정 절차는 결과를 보기 전에 얼려두는 것이 원칙이므로, 분석을 넣는다면 gate를 돌리기 전에 세 사람이 함께 정해야 합니다." This is the last line of the 미정 box (3722–3732) on whether to test how far the conventional values sway the result.
- **Becomes:** the box stays, narrowed. As text: RQ0 실행(2026-11-16~18)은 이 관례 값들을 바꿔 보는 줄 없이 돌았습니다. The run record's reporting lines contain none, and the chain-scale variant scales the chain's per-wake run, not its length. Still open: whether such an analysis is added at all. If it is, it is settled before the second RQ0 gate spec is pinned before its run.
- **From:** `docs/rq0-run-record.md`, "The reporting lines"; `dataset/variants.yaml`, `chain-x1.2` / `chain-x1.4` (`transform: scale-chain`); `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1 and its out-of-scope line (what shows the matter still open: nothing decides it, and the second RQ0 gate spec is Phase 12's)
- **Flags:** for 인지오: the narrowed line names the second RQ0 gate spec. Check it says nothing about Phase 12 beyond item 15.

### g5-28 · `docs/research-claims.md:58` · A · items 6 (the RQ0 run), 7 (the sign rule), 10 (the re-measurement), 11 (the verdict final), 13 (the configuration search), 15 (Phase 12 next)
- **Now:** "on the RQ0 run (2026-11-18, `rq0-run-record.md`) the verdict at the primary is fail, 6 of the 19 judging files meeting g = 0.5 against K = 10, and provisional — the carried-half-width lines move a judging file across g, so the re-measurement contingency has fired and its entry is owed. The count ranges over g, 10 at 0.25 to 4 at 0.67 … On the RQ0 run 17 of the 19 judging files have headroom under the primary, and link 2 stands … If link 1 fails, no model recovers the paper."
- **Becomes:**
  - The as-run verdict stays as the run's own record: fail, 6 of 19, provisional.
  - The re-measurement contingency fired. Its entry, `cpu-batch`'s `python3` run between voluntary blocks, was re-measured at 107 repeats (campaign `meas-ci:background:2026-11-20`) and folded in by a harness changelog entry and the second bless.
  - The verdict became final in place of provisional on 2026-11-21: fail, 5 of 19 judging files meeting g against K = 10 (`c2-p2a`, `c2-p2b`, `c1-ml-train`, `c7-browsing`, `c7-office`), on the RQ0 run's programs.
  - On the fixed programs (the sign rule, `simulator@841dc81131cb`), the post hoc reading at the re-measured value gives 4 of 19. It is not a verdict.
  - The band and line ranges (g band 10 to 4, boot-default sweep 3 to 9, floor band 4 to 6, cap band 6 to 7, venue factor 5 to 7, first segment's length 6 to 7, carried half-widths 5 to 6; chain scale and the 100 ms point not read) stay, stated as the run's reading under the scorer as run. The record gives no g band, sweep or headroom count for the final verdict.
  - Link 2: 17 of 19 with headroom as run, so link 2 stands. The sign rule's post hoc reading of the run's scores gives 12 of 19 (2026-11-18).
  - What follows the fail: the failure procedure's configuration search (2026-11-21) named the route, which is that the table is rewritten. 8 of the 10 searched files have spread the prior table missed; `c7-transcode` and `c7-gaming` have spread the row holds.
  - Phase 12 holds the rewrite, the second RQ0 gate spec pinned before its run, and the second RQ0 run with its verdict.
- **From:** `docs/rq0-run-record.md`, "The outcome" and "The reporting lines"; same record, Corrections, 2026-11-18 (the post hoc reading, 12 of 19); same record, Corrections, 2026-11-21 (the finding, the campaign, "The closing", the verdict line, the post hoc reading at the re-measured value); same record, "The failure procedure", 2026-11-21; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decisions 1 and 2
- **Flags:** for 인지오, two calls. (a) The record says "link 2 stands" only of the as-run count. (b) "If link 1 fails, no model recovers the paper": no record says what the route means for link 1, so the sentence is left as it is unless he decides otherwise.

### g5-29 · `docs/research-claims.md:283` · A · item 10 (the re-measurement)
- **Now:** "one thread, 69.49 s ±27.3 % between voluntary blocks, at nice 0"
- **Becomes:** "55.27 s ±5.89 %".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-30 · `docs/research-proposal.md:459` · E · items 13 (the configuration search), 15 (Phase 12 next)
- **Now:** "The **prior table** is written from scheduling theory before any measurement and is used only for the pre-registered headroom gate (RQ0)."
- **Becomes:** undecided. The route rewrites the table for the second RQ0 run (Phase 12). Whether the rewritten table is still "written from scheduling theory before any measurement" is for Phase 12 to settle, and no record states it.
- **From:** `docs/rq0-run-record.md`, "The failure procedure" ("Route: the table is rewritten"); `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1
- **Flags:** for 인지오: cannot decide (the same question as g5-12 and g5-37).

### g5-31 · `docs/research-proposal.md:480` · D
- **Now:** "The batch class's bandwidth cap is one configuration field … which the executor is to enforce (not yet implemented)."
- **Why left:** stale before Phase 10, no item. The cap is enforced since stage V, 2026-10-20 (`simulator/steps/README.md`, row v; `docs/terminology.md` line 119).

### g5-32 · `docs/research-proposal.md:559` · A · item 13 (the configuration search: the route)
- **Now:** "If the gap is narrow, we redesign workloads or deliberately weaken the executor's self-correction before investing in prompt engineering."
- **Becomes:** "If the gap is narrow, the pre-registered failure procedure runs first: a configuration search before any workload change — no spread found means workload redesign; spread the prior table missed means the table is rewritten." If the proposal is to carry outcomes, add: on the RQ0 run the gap was narrow (fail, 5 of 19 against K = 10, final 2026-11-21), and the search named the route that the table is rewritten (2026-11-21), which Phase 12 carries out.
- **From:** `harness/experiments/rq0-gate.yaml`, statement `failure-procedure`; `docs/rq0-run-record.md`, Corrections, 2026-11-21, the verdict line; same record, "The failure procedure"
- **Flags:** for 인지오: the proposal (a draft, Updated 2026-10-31) states no outcome anywhere. Whether to add the run's outcome or only correct the response list is his call.

### g5-33 · `docs/research-proposal.md:561` · B · items 1 (the pre-run lines), 2 (the integration gate's re-pin)
- **Now:** "*Pre-registered 2026-09-12, re-pinned 2026-10-09:* … with the boot-default sweep at ten alternatives (…), the latency-floor and threshold sensitivity lines, the sensitivity lines over the rebuilt files' variants, the failure procedure (configuration search before any workload change), and the grounding of every number written beside it."
- **Becomes:** the list gains "the cap band line, over three tables moving the unwanted rows' cap to 0.2, 0.333 and 0.5, and the headroom-count line reading link 2 (2026-11-01)". The label's re-pin date becomes the last re-pin, 2026-11-14 (the integration gate, when the spec came to pin the simulator and the daemon).
- **From:** `harness/CHANGELOG.md`, 2026-11-01 and 2026-11-14 ("the integration gate passed …; re-pinned"); `harness/experiments/rq0-gate.yaml`, the pins comment and the statements `claim-links` and `cap-band`
- **Flags:** the 2026-10-31 re-pin, the trace replay and the bounding pair predate the items and stay as D.

### g5-34 · `docs/research-proposal.md:642` · A · item 10 (the re-measurement)
- **Now:** "is one thread, 69.49 s ±27.3 % between voluntary blocks, at the default policy and nice 0."
- **Becomes:** "55.27 s ±5.89 %".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-35 · `docs/research-proposal.md:780` · A · item 13 (the configuration search: the route)
- **Now:** "**Is the random-to-oracle gap large enough to measure?** If not, the pre-registered failure procedure: configuration search first, then redesign"
- **Becomes:** "If not, the pre-registered failure procedure: configuration search first; workload redesign if it finds no spread, the table rewritten if it finds spread the prior table missed".
- **From:** `harness/experiments/rq0-gate.yaml`, statement `failure-procedure`; `docs/rq0-run-record.md`, "The failure procedure"

### g5-36 · `docs/terminology.md:142` · D
- **Now:** "**Executor** — the part of the simulator that applies a config: assigning processes to classes and enforcing the batch class's cap (to be implemented)."
- **Why left:** stale before Phase 10, no item. The cap is enforced since 2026-10-20 (`simulator/steps/README.md`, row v), as the same doc's Config entry at line 119 already says.

### g5-37 · `docs/terminology.md:179` · E · items 13 (the configuration search), 15 (Phase 12 next)
- **Now:** "**Prior table** — the driver table written from scheduling theory before any measurement: one entry per row, one sentence of justification each. Runs the RQ0 gate and is the baseline of RQ5's fragility check. Never tuned."
- **Becomes:** undecided, the same as g5-30. The route rewrites this table in Phase 12, and whether "Never tuned" and "before any measurement" still describe the rewritten table is not recorded.
- **From:** `docs/rq0-run-record.md`, "The failure procedure"; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1
- **Flags:** for 인지오: cannot decide.

### g5-38 · `docs/terminology.md:196` · E · item 13 (the configuration search)
- **Now:** "**Search engine** — the part of the harness that runs many configs against one workload and keeps the best. Used twice: to tune the driver table offline, and to produce the perfect-configuration diagnostic."
- **Becomes:** if `harness/tools/search.py` is this search engine, the entry would read "Used three times: …, and, after the RQ0 run's fail, for the failure procedure's configuration search (`harness/tools/search.py`, 2026-11-21)". No record says whether it is.
- **From:** `harness/CHANGELOG.md`, 2026-11-21 configuration-search entry; `docs/rq0-run-record.md`, "The failure procedure"
- **Flags:** for 인지오: cannot decide. The search tool reads one configuration per point on ten files at the primary boot default, and no record ties it to the table's tuning or to the perfect-configuration diagnostic.

### g5-39 · `docs/terminology.md:270` · B · item 4 (the unavailable rule)
- **Now:** "**RQ0 gate evaluator** — … applies the criterion and the reporting lines … a failed non-exempt guard on a run the criterion reads makes the verdict `invalid`."
- **Becomes:** add after it: "; on a run a reporting line's gap reads, the same failure makes that gap unavailable, and the line gives no reading over its axis".
- **From:** `harness/experiments/rq0-gate.yaml`, statement `sensitivity-lines` ("A failed non-exempt guard on a run a gap reads makes that gap unavailable … gives no reading"); `harness/CHANGELOG.md`, 2026-11-14, "a line that reads a gap from a run with a failed guard gives no reading"

### g5-40 · `docs/background-guide.md:71` · A · items 6 (the RQ0 run), 11 (the verdict final), 13 (the configuration search), 15 (Phase 12 next)
- **Now:** "If perfect recognition barely beats random guessing, then recognition quality doesn't matter on these workloads — the experiment is dead and no prompt engineering can revive it. That check needs no model, no API key, just the simulator. It's the first real experiment the simulator will run."
- **Becomes:** "… It was the first real experiment the simulator ran. The RQ0 run, 2026-11-16 to 2026-11-18, failed: 5 of 19 judging files met the criterion against the 10 it needed, final on 2026-11-21. A fail does not end the experiment by itself. The pre-registered failure procedure ran a configuration search first, and its route is that the driver table is rewritten, followed by a second RQ0 run (Phase 12)." This softens "the experiment is dead" to what a fail actually triggers.
- **From:** `docs/rq0-run-record.md`, "The run" (started, finished); same record, Corrections, 2026-11-21, the verdict line; same record, "The failure procedure"; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 1

### g5-41 · `docs/background-guide.md:116` · A · item 10 (the re-measurement)
- **Now:** "PyTorch's basic MNIST example on the CPU runs 69.49 s between voluntary blocks at nice 0"
- **Becomes:** "55.27 s".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

### g5-42 · `docs/background-guide.md:124` · E · item 10 (the re-measurement: the second bless)
- **Now:** "Here's a real one, abbreviated (`c2-p1a` …)" with `"sampled": { "seed": 201, "archetypes": "archetypes.yaml@c78d8cf…" }` and the hog's `{ "op": "RUN", "us": 192 }`, `{ "op": "SLEEP", "us": 378 }`
- **Becomes:** the current build (`dataset/build/coreset-single/c2-p1a.workload.json`) has `archetypes.yaml@a25178d…`, and the hog's first two lines are RUN 191 and SLEEP 472. Its 1,389.885 s of CPU and the editor's lines are unchanged.
- **From:** the committed build as it stands, read 2026-11-21; `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json` (`c2-p1a` in `beyond_hash`)
- **Flags:** for 인지오: cannot attribute. `c78d8cf` is the library of commit `17f28d7f`, before the 2026-10-31 re-folds, so the example was already stale before Phase 10. The second bless changed `c2-p1a` beyond its hash, but without a pre-bless build I cannot tell whether the hog's two lines moved there or earlier. He decides whether to refresh the example from the build.

### g5-43 · `docs/related-work.md:18` · A · item 10 (the re-measurement)
- **Now:** "one thread, 69.49 s (±27.3 %) between voluntary blocks, at nice 0."
- **Becomes:** "55.27 s (±5.89 %)".
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table; `dataset/archetypes.yaml` line 1272

## Checked, no row

- **The research guidebook's 미실행 markers** (defined in `docs/guidebook/README.md` line 40), read against decision 9. None has its matter closed by the fifteen items:
  - vol-03 2485: the held-out-rows arm, still unrun.
  - vol-03 3594: the cost's unit.
  - vol-05 2550: the extension rule, never used.
  - vol-06 700, 2358, 3494 and 3512: simulated traces against the measurements, never compared.
  - vol-06 3606: already closed by its 2026-10-17 note.
- **The README's own lines**: line 42 ("RQ0 너머의 계획은 대개 제안 또는 미실행으로 표시됩니다") and vol 13's 예정 status still hold.
- **vol-05 2596** counts the vocabulary's six changes since ratification. Those are §1 label-side changes. Item 3's 2026-11-13 entry in `docs/recognition-vocabulary.md` changes §2 (the cap beside the idle class), so it is not a member of that list.
- **Other passages that stand**: the hold-time passages (research-claims 226, proposal 309 and 736, vol-03 488, 1974 and 3243) give no timing for step 1, so item 14 makes none of them false. The mentions of the mock generator (proposal 756, 782) describe ownership and milestones, not the runner.

## Added while editing (K5's editor, 2026-11-21)

### g5-44 · `docs/guidebook/vol-03-the-research.md:2195` · A · item 1 (the RQ0 gate spec's pre-run lines)
- **Now:** "| RQ0 | 이 workload들에서 설정이 결과를 바꾸기는 하나 | link 1 |"
- **Becomes:** the link column reads link 1과 link 2 — the criterion reads link 1, the headroom-count line link 2 (2026-11-01)
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`; `harness/CHANGELOG.md`, 2026-11-01

### g5-45 · `docs/guidebook/vol-03-the-research.md:2686` · A · item 1 (the RQ0 gate spec's pre-run lines)
- **Now:** "RQ0이 link 1, RQ1이 link 4, RQ2가 link 5, RQ4가 link 6을 재고, …"
- **Becomes:** "RQ0이 link 1과 link 2, …"
- **From:** `harness/experiments/rq0-gate.yaml`, statement `claim-links`

## Added at the second search (2026-11-21)

### g5-46 · `docs/guidebook/vol-03-the-research.md:640` · A · item 2 (the integration gate passed), with Q2's earlier fact
- **Now:** "실행부가 집행해야 하는 값인데, 시뮬레이터는 아직 이 값을 읽지 않습니다. 구현해야 할 항목입니다."
- **Becomes:** the simulator reads and enforces the cap since 2026-10-20, and the integration gate of 2026-11-14 showed it on the binary (conformance item (d))
- **From:** `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`, its status line ("is in it since stage V (2026-10-20)"); `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"; `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md`, the `test_cap_ceiling.py` row

### g5-47 · `docs/guidebook/vol-04-experiment-design.md:1111` · A · item 2 (the integration gate passed), with Q2's earlier fact
- **Now:** "지금의 참조 시뮬레이터(`simulator/src/sim.cpp`)는 아직 선언된 등급을 읽지 않습니다. RQ0 gate spec은 RQ0을 돌리기 전에 시뮬레이터가 이 규칙을 보여야 한다고 적어두고, …"
- **Becomes:** the simulator reads the declared class and keeps the rule since 2026-10-28; the integration gate of 2026-11-14 showed it on the binary (conformance item (e))
- **From:** `docs/memos/2026-10-08-declared-scheduling-class.md`, its status line ("in the simulator since its stage Z (2026-10-28, commit `8dab1176`)"); `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"; `docs/memos/2026-11-15-integration-gate-and-cold-smoke.md`, the `test_idle_class.py` row
