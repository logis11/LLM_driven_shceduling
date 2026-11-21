# Rows — g3, dataset guidebook chapters 5 and 6

| file | lines | hits read | rows (A/B/C/D/E) |
|---|---|---|---|
| `docs/guidebook/dataset/05-the-generated-layer.md` | 2175 | 122 | 6/2/0/1/0 |
| `docs/guidebook/dataset/06-grounding-measurement-verification.md` | 1892 | 120 | 9/2/4/0/1 |

## Chapter 5 — the generated layer

### g3-01 · `docs/guidebook/dataset/05-the-generated-layer.md:761` · A · item 12 (the experiment lint reads an executed spec's pins as notes)
- **Now:** "이 파일들을 한 글자라도 고치면 core manifest가 바뀌고, 그것을 pin하는 variants manifest와 RQ0 gate spec(`harness/experiments/rq0-gate.yaml`, …)의 pin이 줄줄이 따라 움직입니다."
- **Becomes:** core manifest가 바뀌면 그것을 pin하는 variants manifest가 따라 움직임. RQ0 gate spec은 실행된 spec이라(RQ0 run, 2026-11-16–18) 그 pin이 run이 읽은 tree를 이름 짓고 다시 고정되지 않음. experiment lint는 working tree와 맞지 않는 pin을 오류가 아니라 note로 출력함(2026-11-20). 두 번째 bless에서도 RQ0 gate spec은 고쳐지지 않았고, 그 dataset pin과 variants pin은 첫 bless를 이름 지음.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry "an executed spec's pins read as the tree its run read"; the same file, the 2026-11-21 re-measurement entry, its opening paragraph ("The RQ0 gate spec is not edited — its dataset and variants pins name the first bless")

### g3-02 · `docs/guidebook/dataset/05-the-generated-layer.md:1115` · A · item 14 (the hold-time plan's step 1 moved)
- **Now:** "\"the need measured with no rule\"은 Phase 10의 통합 직후 RQ0 run의 pipeline 안에서, `oracle`과 `random`만으로(LLM 없이) 하며, 나머지 단계는 RQ4 experiment spec 세션에서 합니다."
- **Becomes:** 규칙 없이 필요성을 재는 측정(계획의 step 1)은 Phase 12의 두 번째 RQ0 run 뒤에, 그 run이 쓰는 table과 program으로, `oracle`과 `random`만으로(LLM 없이) 함. 나머지 단계는 그대로 RQ4 experiment spec 세션.
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10
- **Flags:** for 인지오: the sentence says what the plan's When table states; it stays true only if the plan file's When-table row is restated in this sweep (spec decision 13). Line 1117 and §16.2 row 2 (line 2039), on the When table's step number "0", stay true: decision 10 itself says "its When table numbers it 0".

### g3-03 · `docs/guidebook/dataset/05-the-generated-layer.md:1213` · A · item 14 (the hold-time plan's step 1 moved)
- **Now:** "| 규칙 없이 필요성 재기(계획의 step 1) | Phase 10 통합 직후, RQ0 run의 pipeline 안 | …"
- **Becomes:** 언제 칸: Phase 12의 두 번째 RQ0 run 뒤, 그 run의 table과 program으로.
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10

### g3-04 · `docs/guidebook/dataset/05-the-generated-layer.md:1219` · A · item 14 (the hold-time plan's step 1 moved)
- **Now:** "데이터셋 쪽 준비는 끝났고, 실제 측정은 Phase 10 이후의 일입니다."
- **Becomes:** 실제 측정은 Phase 12의 두 번째 RQ0 run 뒤의 일.
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10

### g3-05 · `docs/guidebook/dataset/05-the-generated-layer.md:1649` · B · item 10 (the re-measurement and the second bless)
- **Now:** "generated manifest는 2026-10-11부터 2026-10-17까지 아홉 번 bless되었습니다." … the table's last row "| 9.16 (2026-10-17) | `01e539ee` | `2d80cff9` | `53420ed5` | `21502219` | `1dd08130` | …" … (line 1663) "2026-10-17 tree의 다섯 manifest의 SHA-256은 마지막 줄(9.16, 2026-10-17)의 값과 같습니다."
- **Becomes:** 표에 두 번째 bless를 한 행으로 추가: 11.3 (2026-11-21) | `d6ded38a` | `2189c0d2` | `879fd4d8` | `6091e382` | `b465bfbe` | `cpu-batch`의 `python3`의 두 block 값을 다시 잰 library 위에서 다섯 set을 다시 build. library hash 말고 바뀐 artifact는 `python3`가 든 파일뿐(transition grid 49개, return grid 70개, distractor grid 22개, familiarity ladder 5개, flap-stress 0개). 어떤 demand도 바뀌지 않음. 끝 문장의 "지금 tree"는 이 행을 가리키게 됨.
- **From:** `harness/CHANGELOG.md`, the 2026-11-21 re-measurement entry, its "The second bless" bullet; `_dev/research/jioh/task-11.3-the-re-measurement/bless-report.json`, `manifests` (`beyond_hash` and `demand_moves` per manifest); the five committed `dataset/build.<set>.manifest.json` at `2e3fade3` (= HEAD), each file's SHA-256, first eight hex
- **Flags:** for 인지오: the passage is dated ("2026-10-11부터 2026-10-17까지", "2026-10-17 tree"). The table also lacks the two 2026-10-31 rebuilds (commits `658d7124`, `bb16f63a`; e.g. transition grid `e6603b2b`, `eee6a020`), which are outside the fifteen items. Adding only the 2026-11-21 row leaves a gap, and the count "아홉 번" is wrong either way. Your call: add all three rows, add only this one, or leave the dated table as it is.

### g3-06 · `docs/guidebook/dataset/05-the-generated-layer.md:1711` · D · outside the fifteen items
- **Now:** "2026-10-30에 키 입력 term 24개가 `input_latency`를 읽게 되면서(그 header 문장도 함께) 지금의 hash는 `1c738540…`입니다."
- **Why left:** the scoring spec changed three more times after `1c738540` (2026-10-30 `2dfcdbe9`; 2026-10-31 `dfe62736` and `0a941e1a`) and is now `4f3e34c1…`. None of those changes is among the fifteen items.

### g3-07 · `docs/guidebook/dataset/05-the-generated-layer.md:1822` · B · item 13 (the configuration search)
- **Now:** "이 권을 쓰는 2026-10-14 현재 `harness/experiments/`에는 `rq0-gate.yaml`만 있고, generated manifest를 pin하거나 선택하는 실험 spec은 아직 없습니다."
- **Becomes:** `harness/experiments/`에는 `rq0-gate.yaml` 옆에 search spec `rq0-config-search.yaml`이 있음(2026-11-21, 어떤 search run보다 먼저 커밋됨). 그것이 pin하는 dataset manifest는 core manifest(`dataset/build.manifest.json`)뿐이라, generated manifest를 pin하거나 선택하는 실험 spec은 여전히 없음.
- **From:** `harness/CHANGELOG.md`, the 2026-11-21 configuration-search entry ("Search spec" bullet); `harness/experiments/rq0-config-search.yaml`, `pins` (line 258–264: `dataset: {path: dataset/build.manifest.json, …}`, no `generated` pin)
- **Flags:** for 인지오: the sentence is dated ("2026-10-14 현재"). It is the folder's list of specs that decision 6 names, which is why it is a row.

### g3-08 · `docs/guidebook/dataset/05-the-generated-layer.md:2012` · A · item 12 (the experiment lint reads an executed spec's pins as notes)
- **Now:** "| C1 timeline 하나 | … | core manifest, variants manifest, 다섯 generated manifest, `coverage-grid.json`, (pin이 움직이면) RQ0 gate spec |" and (line 2014) "| `harness/scoring/scoring-spec.yaml`의 C1 entry | harness의 lint | scoring spec (다시 frozen), 그것을 pin하는 실험 spec |"
- **Becomes:** 두 행 모두에서, 다시 commit하는 spec은 아직 실행되지 않은 실험 spec뿐임. 실행된 spec(옆에 run record가 커밋된 RQ0 gate spec, 옆에 report가 커밋된 search spec)은 그 run이 읽은 tree를 pin으로 가짐. experiment lint는 맞지 않는 pin을 note로 읽고, 그 spec은 다시 고정되지 않음.
- **From:** `harness/CHANGELOG.md`, 2026-11-20 entry ("Experiment lint" bullet); the 2026-11-21 configuration-search entry ("Experiment lint" bullet: "once its report is committed beside it … a pin the working tree no longer matches is a note, as for an executed experiment spec")

### g3-09 · `docs/guidebook/dataset/05-the-generated-layer.md:2062` · A · item 14 (the hold-time plan's step 1 moved)
- **Now:** "| 규칙 없이 flap의 필요성 재기(계획의 step 1; flap-stress set과 저작된 C4 파일 `c4-*`, `oracle`과 `random`) | Phase 10 통합 직후 | hold-time 계획; backlog |"
- **Becomes:** 언제 칸: Phase 12의 두 번째 RQ0 run 뒤, 그 run의 table과 program으로. 기록 칸에 Phase 11 spec decision 10 추가. 아직 돌지 않았으므로 미실행 표시는 그대로 둠.
- **From:** `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md`, decision 10

## Chapter 6 — grounding, measurement, verification

### g3-10 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:698` · A · item 10 (the re-measurement)
- **Now:** " GitHub-hosted runner  (ubuntu-24.04, 4 vCPU, kernel 6.17.0-1022-azure)"
- **Becomes:** 그림 아래에 한 줄 추가: 11.3의 재측정 캠페인(`meas-ci:background:2026-11-20`)은 kernel `7.0.0-1017-azure`(transparent huge pages 기본값 `madvise`) 위에서 돌았고, job이 huge page를 `always`로 씀. runner agent `provjobd`가 끝낸 wait는 그것이 끊은 run에 접음.
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, "The campaign"; `_dev/research/jioh/task-11.3-the-re-measurement/campaign/method.md`, §4
- **Flags:** for 인지오: the diagram draws one venue, and only one entry's two values now come from the newer kernel. The 2026-10-31 GIMP repeats (release `meas-ci-interactive-2026-10-31`, not pooled) also ran on a newer kernel and are outside the items. You may prefer to leave the diagram as it is.

### g3-11 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:743` · A · item 10 (the re-measurement)
- **Now:** "예를 들어 지금 `campaign-background.json`은 `\"mode\": \"full\"`, `\"cpu_model\": \"EPYC 7763\"`, `\"apps\": [\"dejadup\"]`, `\"repeats\": {\"dejadup\": [27, 28]}`, `\"attempt\": 196`입니다."
- **Becomes:** 지금 값은 `"mode": "full"`, `"cpu_model": "EPYC 7763"`, `"apps": ["mnist"]`, `"repeats": {"mnist": [74, 102]}`, `"attempt": 284`. 마지막으로 바꾼 것은 11.3의 캠페인으로, machine gate에 걸린 창을 다시 띄운 것임.
- **From:** `.github/campaign-background.json` as it stands; its last commit `03723634` (2026-11-21, "campaign — gated windows retried (mnist 74, mnist 102)")

### g3-12 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:822` · B · item 10 (the re-measurement)
- **Now:** "**background (9.7, 9.10).** 9.7은 … 9.10은 같은 workflow로 무인 업그레이드, DKMS 자동 설치, Tracker의 첫 색인, PyTorch MNIST 학습, HandBrake 변환, Kdenlive 내보내기, Déjà Dup 증분 백업을 쟀습니다."
- **Becomes:** 첫머리를 "(9.7, 9.10, 11.3)"으로. 문장 하나 추가: 11.3(2026-11-20)이 같은 workflow와 9.10 캠페인의 방법 그대로 PyTorch MNIST 학습을 새 반복 107회로 다시 재어, `cpu-batch`의 `python3`의 두 block 값(run between voluntary blocks, block per run)을 바꿈(`meas-ci:background:2026-11-20`).
- **From:** `_dev/research/jioh/task-11.3-the-re-measurement/campaign/method.md`, §1 (the original campaign's method unchanged, `meas-background.yml`) and §2 (107 fresh repeats); `docs/rq0-run-record.md`, Corrections, 2026-11-21, "The campaign"

### g3-13 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:926` · A · item 10 (the re-measurement)
- **Now:** "`cpu-batch`의 `python3`의 run between blocks와 block per run(±27.3 %, ±10.8 %; runner의 `khugepaged`)"
- **Becomes:** `cpu-batch`의 `python3`의 run between blocks와 block per run(±5.89 %, ±2.15 %, 11.3이 107회로 다시 잼; 9.10 캠페인의 6회로는 ±27.3 %, ±10.8 %; runner의 `khugepaged`). 두 값 모두 이 예외 class에 남음.
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, the campaign table and "Both values keep their exception class"; `dataset/variants.yaml`, `carried_values` (`python3_run` 0.0589, `python3_block` 0.0215, each `source` naming "the runner's khugepaged" for the run)

### g3-14 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:934` · A · item 10 (the re-measurement)
- **Now:** "(`clamscan`과 `tracker`의 값은 그 뒤 library에 없고, `python3`은 9.10의 MNIST 캠페인으로 다시 쟀습니다)"
- **Becomes:** … `python3`은 9.10의 MNIST 캠페인으로 다시 쟀고, 그 두 block 값은 11.3이 2026-11-20 캠페인에서 107회로 다시 쟀습니다(둘 다 이 예외 class에 남음).
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, "The campaign"; `harness/CHANGELOG.md`, the 2026-11-21 re-measurement entry, "The fold-in" bullet

### g3-15 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:936` · C · items 6 (the RQ0 run), 10 (the re-measurement), 11 (the verdict final)
- **Now:** "> **열린 자리.** 예외로 담은 값을 미리 정한 반복 수로 다시 잴지는 9.14 decision 3이 \"pre-registered contingency\"로 정했습니다. … 이것은 simulator가 계약대로 구현된 뒤 Phase 10의 RQ0 run에서 돌아갑니다. 아직 돌지 않았습니다(미실행)."
- **Becomes:** 상자를 없애고 결과를 본문으로 씀. 9.14 decision 3이 사전 등록한 contingency는 RQ0 run(2026-11-16–18)에서 발동함: 반폭 줄의 하한이 `c7-ml-train`을 g 너머로 옮겨(primary에서 gap 2.512, 하한에서 0.000) 그 축의 판정이 5–6, fail이 됨. 11.3이 값을 하나씩 옮겨 그 entry를 찾음: `cpu-batch`의 `python3` run between voluntary blocks를 −27.3 %로 옮기면 그것만으로 파일이 g를 넘음. 그 값을 미리 정한 107회로 `meas-ci:background:2026-11-20`에서 다시 잼(55.27 s ±5.89 %, block per run 403.96 µs ±2.15 %, 둘 다 예외 class 유지). harness changelog 항목과 두 번째 bless로 접음. 판정은 provisional에서 final로 바뀜: fail, 19개 판정 파일 가운데 5개가 g를 만족, K = 10. 열린 부분은 남지 않음.
- **From:** `docs/rq0-run-record.md`, "The outcome" (the re-measurement contingency bullet) and "The reporting lines" (carried half-widths 5, 6); the same record, Corrections, 2026-11-21 ("The finding", "The campaign", "The closing" and the verdict line); `harness/CHANGELOG.md`, the 2026-11-21 re-measurement entry

### g3-16 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:959` · A · item 10 (the re-measurement)
- **Now:** "캠페인의 반복 수는 5부터 45입니다(workflow 문서; `measurement-overview.md`는 `mail-client`의 77을 넣어 \"5 to 77\"로 적습니다). 대부분 30보다 작으므로, 표의 반폭도 낮게 나올 수 있습니다."
- **Becomes:** 범위에 11.3의 재측정 캠페인 107회(`cpu-batch`의 `python3`)를 더함. 결론 "대부분 30보다 작으므로"는 그대로.
- **From:** `docs/rq0-run-record.md`, Corrections, 2026-11-21, "The campaign" (107 fresh repeats)
- **Flags:** for 인지오: two records disagree. `docs/workload/measurement-overview.md` line 79, which 11.3 brought in line elsewhere, still reads "the campaigns' counts are 5 to 77". That file is another reader's. Decide whether the overview gains 107 too, so that the guidebook's quote of it stays true.

### g3-17 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:965` · E · item 10 (the re-measurement), and a stale quote outside the items
- **Now:** "`measurement-overview.md` §6은 이것을 \"About half of all jobs draw it (50–59 % by campaign)\"로 요약합니다."
- **Becomes:** — (for 인지오)
- **From:** `docs/workload/measurement-overview.md` line 73 ("Over the campaigns behind the dataset's values, 40–83 % of a campaign's jobs drew it", in place since `c59b6a89`, 2026-10-17); `_dev/research/jioh/measurement-campaign-record.md` line 564 (11.3: 680 jobs, 107 landed, 15.7 %)
- **Flags:** for 인지오: two records disagree. The quoted summary was replaced in the overview on 2026-10-17, which is outside the items and on its own would be a D row. The overview's current range, 40–83 %, does not hold 11.3's 15.7 % from the campaign record. Quoting either range would put a number in the guidebook that no in-line record backs.

### g3-18 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1041` · A · item 6 (the RQ0 run)
- **Now:** "그리고 이 위협이 결과에 영향을 주는지는 Phase 10의 **trace-replay check**로 확인합니다."
- **Becomes:** 과거형으로: Phase 10의 RQ0 run(2026-11-16–18)에서 trace-replay check로 확인했습니다. 결과는 아래 g3-19의 본문.
- **From:** `docs/rq0-run-record.md`, "The reporting lines", the trace replay bullet

### g3-19 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1043` · C · item 6 (the RQ0 run)
- **Now:** "> **열린 자리.** trace-replay check는 아직 돌지 않았습니다(미실행). simulator가 계약대로 구현된 뒤 Phase 10의 RQ0 run과 함께 돕니다. 불일치가 나오면 \"disagreement stated as the compiled streams' ordering threat\"입니다(9.14 decision 10). 그 뒤에 무엇을 할지(예: 순서를 보존하는 compile)는 기록에 정해지지 않았습니다."
- **Becomes:** 결과를 본문으로 씀. trace-replay check는 RQ0 run(2026-11-16–18)에서 돌았고 일치하지 않음(agreement false, tolerance 0.17): `c2-p1a` 0.377 대 0.367, `c7-meeting` 0.279 대 0.261은 일치. `c7-browsing` 1.121 대 0.475는 g를 넘고, `c7-dev` 0.254 대 0.000은 tolerance 너머로 다름. 이 불일치는 verdict 옆에 compiled streams의 ordering threat로 적힘. 2026-11-18의 post hoc reading에서도 일치하지 않음: `c7-dev` 0.000 대 0.000, `c7-browsing` 1.121 대 0.475가 run에서처럼 g를 넘음. 상자는 한 문장으로 줄여 남김: "불일치 뒤에 무엇을 할지(예: 순서를 보존하는 compile)는 기록에 정해지지 않았습니다."
- **From:** `docs/rq0-run-record.md`, "The reporting lines", the trace replay bullet; the same record, Corrections, 2026-11-18, the line table's "trace replay" row. Still open: `harness/experiments/rq0-gate.yaml`, the `trace_replay` line's `reason` (line 246: "a disagreement is stated beside the verdict as the compiled streams' ordering threat", no step beyond it) and statement `sensitivity-lines`; the run record's trace replay bullet states the threat beside the verdict and nothing further; `_dev/docs/spec/jioh/phase-11-rq0-failure-procedure-diagnosis.md` (Scope and decisions 1–10) takes no such step up.

### g3-20 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1055` · C · item 6 (the RQ0 run)
- **Now:** "이 variant들은 Phase 10에서 처음 돌아갑니다(미실행)."
- **Becomes:** 미실행 표시를 없앰. 이 variant들은 RQ0 run(2026-11-16–18)에서 처음 돌았음: venue factor ×0.8, ×1.25에서 count 7, 5(fail). carried half-widths 하한 5, 상한 6(fail, re-measurement contingency 발동). trace replay는 일치하지 않음. 2026-11-18의 post hoc reading에서는 venue factor 5, 4, carried half-widths 4, 4(어느 쪽 끝도 count를 움직이지 않음). 열린 부분은 남지 않음.
- **From:** `docs/rq0-run-record.md`, "The reporting lines" (venue factor, carried half-widths, trace replay rows); the same record, Corrections, 2026-11-18, the line table
- **Flags:** the record gives no variant-line counts after the 2026-11-21 re-measurement. None is to be derived.

### g3-21 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1075` · B · item 10 (the re-measurement)
- **Now:** "2026-10-17에 `gh release list`로 확인한 release는 34개입니다(…)." The table ends at "| `meas-ci-probes-2026-09-23` | 9.9 session long-phase probes | …"
- **Becomes:** 표에 행 하나 추가: `meas-ci-background-2026-11-20` | meas-ci background 2026-11-20 — 11.3 MNIST training re-measurement (single-core) | `cpu-batch`의 `python3`의 run between voluntary blocks와 block per run(11.3의 재측정).
- **From:** `dataset/meas-releases.yaml`, lines 298–300 (`meas-ci:background:2026-11-20` → release `meas-ci-background-2026-11-20`); `docs/workload/measurement-overview.md`, §9, line 165; the release's title as `gh release list` prints it today
- **Flags:** for 인지오: the count "34개" is dated 2026-10-17. Three other releases since then are outside the items: `dataset-build-2026-10-26`, `meas-ci-interactive-2026-10-31` (GIMP repeats, not pooled) and `dataset-build-2026-10-31`. Adding only this row leaves those out and leaves the count as it is.

### g3-22 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1132` · A · item 10 (the re-measurement)
- **Now:** "| `_dev/research/jioh/measurement-campaign-record.md` | … | 9.12까지 기록 |" and (line 1138) "| `docs/workload/measurement-overview.md` | … | draft, 2026-09-29 작성, 2026-10-17 갱신 |"
- **Becomes:** campaign record의 상태 칸: 9.12까지, 그리고 11.3의 재측정(Campaigns 표의 `meas-ci:background:2026-11-20` 행, 절 "11.3 — `cpu-batch`'s `python3`, its two block values re-measured", 그 기계 뽑기). measurement-overview의 상태 칸: draft, 2026-09-29 작성, 2026-11-21 갱신.
- **From:** `_dev/research/jioh/measurement-campaign-record.md`, lines 25, 327, 564; `docs/workload/measurement-overview.md`, header line ("Updated 2026-11-21")
- **Flags:** the campaign record also gained 2026-10-31 notes (e.g. the GIMP repeats on `meas-ci:interactive:2026-09-18`'s row), which are outside the items.

### g3-23 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1142` · A · item 10 (the re-measurement)
- **Now:** "지금은 … §9의 release 표가 9.10의 캠페인 release까지 담습니다. 다른 하나인 `measurement-campaign-record.md`의 맨 앞 Campaigns 표는 14개 태그만 싣고 9.10의 나머지 캠페인(…)은 본문 절에만 있습니다."
- **Becomes:** §9의 release 표는 9.10의 캠페인 release와 11.3의 `meas-ci-background-2026-11-20`까지 담음. Campaigns 표에는 태그가 15개이고, 11.3의 `meas-ci:background:2026-11-20`이 더해진 것임. 9.10의 나머지 캠페인은 여전히 본문 절에만 있음.
- **From:** `docs/workload/measurement-overview.md`, §9, line 165; `_dev/research/jioh/measurement-campaign-record.md`, the Campaigns table (lines 9–25, fifteen `meas-ci` rows, the last `meas-ci:background:2026-11-20`)

### g3-24 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1713` · C · item 2 (the integration gate passed), item 6 (the RQ0 run)
- **Now:** "> **열린 자리.** decision 6에 따라 해결된 것으로 본 진술들은 simulator를 기다립니다. … 짝 검토의 cap 문장들, `c3-evening`의 chain term, idle class 파일 여섯의 진술에 대한 확인은 기록에 아직 없습니다. … (h)는 (g)처럼 simulator 담당이 아직 갚을 것으로 두고 있습니다. 각 항목이 보여지기 전에는 RQ0 run이 시작되지 않습니다(…)."
- **Becomes:** simulator를 기다리는 부분은 본문으로 옮김. integration gate가 2026-11-14에 `simulator@0d323c84470a`와 `daemon@62c71f0d2de0`에서 통과함. statement `simulator-conformance`는 각 항목을 어디서 보이는지 적음: binary를 통해 재생한 fixture로 (a), (b), (c), (g), (i), (j), binary에 대한 black-box unit test로 (d), (e), (f), (g), (i), (h). RQ0 run은 그 뒤 2026-11-16–18에 돌았음. 상자는 남기되 줄임. 남는 것은 그 항목들에 기대는 진술의 확인으로, 짝 검토의 cap 문장들((d)), `c3-evening`의 chain term((b)), idle class 파일 여섯의 진술((e)), `c1-compile`과 `c4-compile`의 build turnaround((g))임. 이 확인은 어떤 기록에도 없음.
- **From:** `harness/CHANGELOG.md`, 2026-11-14 entry "the integration gate passed …" (its opening paragraph and the "RQ0 gate spec" bullet); `docs/rq0-run-record.md`, "The run" (programs, started, finished). Still open: `_dev/research/jioh/task-10.2-integration-gate/README.md` (the gate's four parts are unit tests, fixtures, the daemon comparison and the short run; it lists no check of these statements)
- **Flags:** teammate (the box names these checks as 인경민's to run once each item is in; whether they are still owed after the integration gate changes his to-do); for 인지오: no record says whether the checks are still owed or were overtaken by the gate.

### g3-25 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1727` · A · item 6 (the RQ0 run)
- **Now:** "9. **순서와 동시 깨어남.** compile된 흐름은 component의 빈도와 분포를 재현하나 gap의 순서와 함께 깨어남은 재현하지 않음(`measurement-overview.md` §8의 위협 진술; trace-replay check로 경계)."
- **Becomes:** 괄호의 "trace-replay check로 경계"를 바꿈: RQ0 run(2026-11-16–18)의 trace-replay check는 일치하지 않았고(`c7-browsing`이 g를 넘음), verdict 옆에 ordering threat로 진술됨.
- **From:** `docs/rq0-run-record.md`, "The reporting lines", the trace replay bullet

## Added at the second search (2026-11-21)

### g3-26 · `docs/guidebook/dataset/06-grounding-measurement-verification.md:1691` · A · item 2 (the integration gate passed)
- **Now:** "decision 6, simulator를 기다리는 진술. reference simulator가 아직 구현하지 않은 executor 규칙에 참이 기대는 진술은, …"
- **Becomes:** the clause dated to the decision, "그때(2026-10-17) reference simulator가 …", as chapter 8's paraphrase of the same decision is (g2-39); the box under it (g3-24) carries the current state
- **From:** `_dev/docs/spec/jioh/task-9.16-exit-audits.md`, decision 6; `harness/CHANGELOG.md`, 2026-11-14 "the integration gate passed"
