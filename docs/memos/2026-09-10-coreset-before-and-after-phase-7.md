# Coreset, Phase 7 전과 후 — 무엇이 왜 바뀌었나

> Status: memo · Created 2026-09-10 · Updated 2026-09-10
> From 인지오 to 인경민, 박이안. Phase 7(coreset attribute coverage)이 coreset을 24개 파일에서 50개로 바꿨어요. 이 memo는 그 변화를 처음부터 끝까지 풀어 쓴 거예요 — 왜 필요했는지, 무엇이 추가됐는지, 각자의 작업(simulator, daemon)에 무엇이 달라지고 무엇이 그대로인지. 규범은 각 문서에 있고(아래에 링크), 이 글은 읽기 편하게 이어 붙인 거예요. 길어요. 급하면 §1과 §8만 읽어도 돼요.

## 1. 한 문단 요약

driver table은 32개 row예요 — mode 16개 × `background_wanted` true/false. Phase 6의 pair review에서 coreset이 그 32개 cell 중 **17개만** 실제로 담고 있다는 걸 발견했어요. 특히 `background_wanted: false` 쪽은 segment가 딱 두 개(`c2-p1b`, `c2-p2b`)뿐이었어요. 그러면 attribute accuracy라는 metric은 거의 의미가 없어요 — 항상 `true`라고 답해도 95%가 나오니까요. 원인은 dataset을 점검하던 도구(coverage grid)가 mode × familiarity tier만 세고 `background_wanted` 축이 없어서, 8월 28일 sign-off 때 이 구멍이 안 보였던 거예요. Phase 7은 (1) grid에 그 축을 넣고 CI가 빈 cell을 잡게 하고, (2) mode마다 C1 base 하나씩 채워 16개로 만들고, (3) mode마다 `false` 쪽 counterpart를 하나씩 파생해서(C7, 16개) **32개 cell 전부**에 pair를 만들었어요. 결과: coreset 24 → 50 파일, 38 → 64 segment, 빈 cell 0. simulator와 daemon의 contract는 하나도 안 바뀌었어요.

## 2. 왜 필요했나 — 구멍이 어디에 있었나

### 2.1 driver table의 row와 coreset의 cell

recognizer는 두 가지를 답해요: **mode**(16개 중 하나)와 **`background_wanted`**(배경 작업이 사용자가 원한 것인가, true/false). 그 답 하나하나가 driver table의 row 하나에 대응하고, row마다 scheduler config가 들어 있어요. 실험이 하려는 건 "상황을 제대로 읽으면 그 row의 config가 더 좋은 성능을 내나"를 재는 거예요.

그러려면 coreset 안에 각 row를 실제로 **exercise하는 segment**가 있어야 해요. 어떤 row를 아무 파일도 안 건드리면, 그 row는 `random` condition이 뽑을 수 있다는 것 말고는 실험에서 아무 역할이 없어요.

### 2.2 Phase 6 pair review가 본 것

Phase 6에서 prior driver table(이론으로 쓴 32 row)을 쓰고, row pair마다 "무슨 knob이 다르고 어느 파일의 어느 term을 움직이나"를 한 문장씩 검토했어요(`docs/daemon/prior-table-pair-review.md`). 그 검토가 이 표를 만들었어요:

| | 있음 | 없음 |
|---|---|---|
| `true` row (16) | 15 | `indexing/true` |
| `false` row (16) | 2 (`gaming`, `indexing`) | 나머지 14 |

`false` 쪽 두 개는 C2 pair의 b 파일(`c2-p1b`의 indexing rescan, `c2-p2b`의 clamscan)이에요. 원래 C2가 attribute를 시험하려고 만든 파일이라 거기엔 있었지만, 그 밖에는 없었어요.

(pair review의 finding 2가 처음엔 "빠진 14개 = false 13 + `meeting/true`"라고 셌는데, compiled ground truth로 다시 세니 "빠진 15개 = false 14 + `indexing/true`"가 맞아요. `meeting/true`는 `c6-fold`가 담고 있었어요 — 다만 그건 pre-committed miss라서 recognition으로는 못 재는 cell이었고요. 이 정정은 finding 4에 적혀 있어요.)

### 2.3 왜 못 봤나

coverage grid(`dataset/coverage-grid.json`)는 "논문의 dataset-design 표"예요 — timeline에서 자동 생성하고 CI가 drift를 잡아요. 그런데 이 도구가 세는 축이 **mode × familiarity tier**뿐이었어요. building plan은 처음부터 "driver-table cell × familiarity × distractor"의 grid를 조직 원리라고 썼는데, 도구는 cell의 절반(mode)만 셌던 거예요. 표에 안 보이는 구멍은 sign-off에서 못 잡아요. 그래서 Phase 7의 첫 sub-task가 도구부터 고치는 거였어요.

### 2.4 왜 지금 고쳤나

pipeline(harness 상단, simulator 통합, RQ0 실행)이 아직 coreset 위에서 돌기 전이라 지금이 제일 싼 시점이에요. 나중에 고치면 records·scoring·pre-registration을 전부 다시 해야 해요.

## 3. 무엇을 결정했나 — grill에서 정한 것들

Phase 7 spec(`_dev/docs/spec/jioh/phase-7-coreset-attribute-coverage.md`)에 13개 결정이 있어요. 핵심만 풀어서:

1. **목표는 32 cell 전부, pair로.** 일부 mode만 채우는 안(interactive만, C1 base 있는 것만)도 있었지만, controlled claim은 coreset에만 기대니까 generalset에 미루면 영원히 안 재는 cell이 생겨요. 그래서 전부. 그리고 각 `false` cell은 같은 mode의 `true` base와 **한 군데만 다른 pair**로 만들어요 — attribute의 효과가 그 한 군데에 귀속되도록(C2/C4가 쓰던 원칙).

2. **batch mode에서 `false`의 뜻.** interactive mode(office 등)에서는 "사람이 하는 일 + 뒤에서 도는 원치 않는 job"이라 읽으면 돼요. batch mode(compile, ml-train, render, transcode, indexing, backup)는 batch job 자체가 그 mode라 애매했어요. 결정: **batch job 자체가 attribute가 판단하는 배경 작업**이에요. `compile/false`는 "아무도 안 시킨 build", `transcode/false`는 "아무도 안 시킨 conversion". `c2-p1b`가 이미 이렇게 읽고 있었어요(indexer 자체가 unwanted). recognition vocabulary §1에 이 clause가 한 줄 들어갔어요.

3. **이름·행동으로 구분이 안 되는 cell.** 어떤 counterpart는 base와 **의도만** 달라요 — 같은 indexer를 사용자가 직접 돌린 것(`true`)과 timer가 돌린 것(`false`). telemetry는 이름과 행동만 보니 recognizer가 맞힐 방법이 없어요. 이런 건 C6처럼 **pre-committed miss**로 배송해요: cell은 채워지고(`oracle`은 label을 직접 읽으니 그 row의 성능은 재요), recognition accuracy에서는 제외하고 따로 보고해요. 새 annotation `pre_committed_miss: true`가 segment에 붙어요.

4. **그룹 구조.** C1을 16개(mode당 하나)로 늘리고, 새 그룹 **C7**이 16개 counterpart를 담아요. `c7-<mode>`는 `c1-<mode>`에서 파생. C4(label을 안 바꾸는 injection)와 헷갈리지 않게 따로 뒀어요.

5. **interactive counterpart에 주입하는 job.** 열 개 전부 **`clamscan`(cpu-batch)** 하나로 통일. CPU-bound라 batch class에 잡혀 cap이 작동하고, tier 1이라 pair의 familiarity tier가 안 바뀌고, 이름이 하나라 열 개 `false` cell이 mode로만 달라요. meas-ci cli:3에서 full-scan 상태가 CPU 포화라는 게 이미 측정돼 있어요.

6. **batch counterpart의 이름.** P1b 수법 — 같은 archetype, 이름만 바꾸고 label flip. 이름은 base와 같은 tier를 우선, 없으면 다른 tier라도 쓰되 mismatch를 적고, 신뢰할 만한 이름이 아예 없으면 3번 규칙(miss). 이름은 반드시 name-verification workflow를 통과해야 해요.

7. **scan의 타이밍.** 0초 도착, `total_work` 60 s. segment 내내 살아 있어서 label이 매 순간 맞고, 어떤 policy에서도 그래요.

8. **demand class.** 모든 C7 파일과 기존 파생 8개(`c4-*`, `c5-*`, `c6-fold`, `c6-spoof`)가 recipe에 `demand: calibration`을 **명시**해요(전에는 base의 meta를 통째로 복사해서 상속됐고, Phase 3부터 미결이었어요). 실제 regime은 manifest의 utilization으로 읽어요.

9. **새 C1 base 만드는 법.** 그 mode를 이미 담고 있던 segment에서 task set을 그대로 들어 올려요(header에 출처 기록). `meeting`만 새로 설계.

10. **base의 scoring term.** mode class별 패턴에 그 mode가 이미 쓰던 weight를 붙여요. 기존 cap이 하나도 안 바뀌게.

11. **counterpart의 scoring term.** **unwanted work carries no term.** base의 term에서 batch term을 뺀 것. lint가 강제.

12. **grid.** 32 row × 5 tier, `ambiguous`는 밖에, 빈 cell이면 CI 실패, pre-committed miss는 표에 표시.

13. **generalset 요구사항.** 생성기의 출력도 32 cell 전부를 담아야 하고 같은 lint로 검사해요(building plan §4).

## 4. 무엇이 추가됐나 — 파일 단위로

### 4.1 C1: 6 → 16

원래 여섯(office, gaming, compile, media, browsing, idle)에 열 개가 더해졌어요. 전부 같은 모양이에요: 60 s, segment 하나, `background_wanted: true`, `demand: calibration`, foreground가 있으면 focus 2–58 s. seed는 107–116.

| 파일 | task set | 어디서 가져왔나 | utilization |
|---|---|---|---|
| `c1-dev` | `code` 혼자 | `c2-p1a` 첫 segment | 0.46 |
| `c1-video-edit` | `kdenlive` 혼자 | `c2-p3a` 첫 segment | 0.46 |
| `c1-photo` | `gimp` 혼자 | `c3-creation` 첫 segment | 0.47 |
| `c1-mail` | `thunderbird` + 40 s에 send burst | `c3-workday` 마지막 segment (browser·writer는 안 가져옴 — "pure mail") | 0.53 |
| `c1-meeting` | `zoom` ×3: video-playback + audio-playback + electron-comms helper | **새 설계.** `c6-fold`의 meeting segment는 browser 그대로라 가져올 게 없었어요. S3를 video-playback에 묶는 건 archetype-plan OQ-2의 stated approximation | 0.45 |
| `c1-ml-train` | `code` + `python3` cpu-batch 30 s | `c2-p1a` 둘째 segment (130 s → 30 s) | 0.97 |
| `c1-render` | `kdenlive` + `ffmpeg` cpu-batch 30 s, `initiated: user` | `c2-p3a` 둘째 segment (75 s → 30 s) | 0.90 |
| `c1-transcode` | `kdenlive` + `HandBrakeCLI` cpu-batch 30 s, `initiated: user` | `c3-creation` 셋째 segment (320 s → 30 s) | 0.97 |
| `c1-indexing` | `code` + `tracker-miner-fs-3` cpu-batch 30 s, `initiated: user`, **`pre_committed_miss: true`** | `c2-p1b` 둘째 segment (130 s → 30 s) | 0.96 |
| `c1-backup` | `kdenlive` + `borg` io-stream 30 s, `initiated: scheduled` | `c2-p3b` 둘째 segment (75 s → 30 s) | 0.97 |

batch job을 30 s로 줄인 이유: base는 job의 **turnaround**(끝나는 데 걸린 시간)를 채점하니까 60 s 안에 끝나야 해요. 어떤 policy든 lane의 절반이면 끝나요.

`c1-indexing`이 왜 pre-committed miss인지: 이건 indexing의 **`true`** cell이에요 — 사용자가 직접 돌린 reindex. `c2-p1b`의 unwanted rescan과 이름도 행동도 똑같고 의도만 달라요. recognizer가 맞힐 수 없으니 미리 miss로 약속해요.

### 4.2 C7: 새 그룹, 16개

recipe 하나(`dataset/timelines/coreset/c7.variant.yaml`)에서 전부 생성돼요. 두 종류:

**interactive 10개** (browsing, office, mail, dev, photo, meeting, gaming, media, video-edit, idle): base + `clamscan`(cpu-batch, 0 s부터 60 s 일) 하나. segment의 attributes는 `{background_wanted: false, background: av-scan}`, scenario에 S17 추가. 그 외엔 base와 byte-identical.

**batch 6개**:
- `c7-compile`: `make` → **`dkms`** rename. DKMS는 kernel이 업데이트되면 배포판이 알아서 module을 다시 build하는 framework예요 — 사용자가 시킨 build가 아니에요. 세 배포판(Ubuntu·Fedora·Arch) container에서 name-verification workflow로 확인했어요(`meas-ci:names:2`, process 이름 `dkms`, runtime level). Fedora는 kernel-install hook과 `dkms.service`까지 패키지에 들어 있어서 "kernel 바뀌면 돈다"는 주장의 직접 증거예요. 근거는 `docs/references.md`의 `dkms-man`, `dkms-debian`.
- `c7-indexing`: `c1-indexing`에서 label만 `false`로. 이쪽은 S14의 indexer가 기본적으로 unwanted라 recognizer가 맞힐 수 있는 쪽이에요. miss는 `true` 쪽(`c1-indexing`)에 있어요.
- `c7-ml-train`, `c7-render`, `c7-transcode`, `c7-backup`: **label만 flip, `pre_committed_miss: true`.** 이 네 mode는 배포판이나 vendor가 *다른 이름*으로 돌리는 같은 종류의 unwanted job이 없었어요. transcode는 Jellyfin의 background transcoder를 후보로 봤는데, 패키지가 binary를 `usr/lib/jellyfin-ffmpeg/ffmpeg`로 설치해서 process 이름이 그냥 `ffmpeg`예요 — render pair가 쓰는 wanted 이름과 같아서 cue가 아니라 spoof가 돼요. 그래서 miss.

| counterpart | utilization |
|---|---|
| browsing, dev, media, meeting, photo, video-edit | 1.45–1.47 |
| office | 1.50 |
| mail | 1.53 |
| gaming | 2.46 (base가 이미 1.46) |
| idle | 1.00 (scan만) |
| compile, ml-train, render, transcode, indexing, backup | base와 같음 (rename·flip은 일을 안 늘림) |

### 4.3 pre-committed miss 다섯 개 (attribute 쪽)

`c1-indexing`, `c7-ml-train`, `c7-render`, `c7-transcode`, `c7-backup`. 전부 "같은 이름, 같은 일, 의도만 다름"이에요. grid에 표시되고, Phase 8의 grader가 accuracy에서 빼요. `oracle`은 label을 직접 읽으니 그 row의 scheduling 성능은 여전히 재요.

## 5. 도구와 검사 — 무엇이 CI에서 강제되나

- **coverage grid** (`dataset/tools/wlc/grid.py`, 출력 `dataset/coverage-grid.json`): 이제 32 row(mode × `background_wanted`) × 5 tier. `ambiguous`(c6-dual)는 밖에 따로. pre-committed miss segment는 cell에 세되 `miss` 열에 표시. **빈 cell이 하나라도 있으면 `make -C dataset check`가 실패해요** (`derive.py --require-coverage`). 지금은 32/32, 빈 cell 0.
- **deriver**: `patch-meta` op 추가(seed·id는 못 바꿈). 다섯 recipe(`c2-pairs`, `c4`, `c5`, `c6`, `c7`) 전부 재파생해도 기존 파생 파일은 byte-identical.
- **scoring lint** (`harness/tools/harness/scoring.py`): "파생 파일은 base의 term 그대로" 규칙에 한 clause — ground truth가 base의 `true`를 `false`로 뒤집은 파생 파일은 base의 term에서 batch term(`turnaround`, `cpu_delivered`)만 뺀 것이어야 해요. 그 외 파생은 여전히 verbatim.
- **manifest**: 100 artifacts(50 × 2 mode). 기존 48개 hash는 안 바뀌었어요.
- 테스트: dataset 71, harness 85, daemon 28. 전부 green. `make -C dataset check`, `make -C harness lint`, `make -C daemon lint` clean.

## 6. 문서에 무엇이 바뀌었나

- `docs/recognition-vocabulary.md` §1: `pre_committed_miss` annotation(다섯 번째), batch-mode에서 `background_wanted`의 읽기(clause 한 줄). changelog 두 항목.
- `docs/workload/building-plan.md`: §3 C1(16), 새 C7 절, counts(50 파일·64 segment·novel 23·derived 27), balance check(grid가 32 cell을 세고 CI가 강제), §4 generalset의 all-32 요구, §5a 면제 family 목록과 이유, §9의 grid-fill 항목 closed, throwaway pool 항목 추가.
- `docs/daemon/prior-table-pair-review.md`: §C에 C7 pair 16개(knob, 움직이는 term, 방향, demand와 window, miss). finding 4(32 cell 전부 + 정정), 5(아래 §7), 6(defect 없음). `prior.yaml`의 `false` row 13개가 자기 C7 파일을 문장에 명시.
- `daemon/driver-table/prior.yaml`: cap·algorithm 변화 없음. `indexing/true`의 cap 0.5가 "stated assumption"에서 `c1-indexing`의 weight로 **derived**로 바뀜(값은 같음).
- `docs/references.md` + `dataset/sources.yaml`: `dkms-man`, `dkms-debian`. `docs/workload/scenario-catalog.md` S11 row에 dkms.
- `docs/terminology.md`: counterpart (C7), pre-committed miss.
- `docs/workload/coreset-guide.md`(공부용, 한국어): §9 일곱 그룹, §10에 C1 추가분과 C7 절, §11 파생 관계, §12·§13.
- `docs/harness/harness-and-records-guide.md`: §15 표에 C1 16·C7 행, 새 파일들의 term.
- `dataset/README.md`: 50 파일, 일곱 그룹, grid 설명.

## 7. 알아둘 finding — cap이 안 닿는 두 pair

pair review의 finding 5. `c7-meeting`과 `c7-media`는 `true` row도 `false` row도 **EDF**예요(mode가 algorithm을 정하니까). EDF는 TIMER task(call의 video·audio, player의 video·music)를 deadline class로 먼저 돌리고, scan은 residual class로 남는 시간에만 돌아요. tick이 기다리는 최대는 residual slice 하나, 2 ms. 그런데 video tick은 10 ms, audio tick은 47.5 ms 넘게 기다려야 miss예요. 그러니 **cap이 0.5든 0.05든 tick은 한 번도 안 늦어요** — 두 row의 점수가 같아요.

이게 뜻하는 것:
- 이 두 파일은 **recognition**(mode·attribute accuracy, latency)은 전부 재요. label은 명확하고 miss도 아니에요.
- **`oracle` 대 `fixed`의 headroom**도 재요 — `fixed`는 MLFQ boot default라 6.67 ms짜리 video burst를 2 ms slice 뒤에 강등시키고 scan과 경쟁시켜서 tick이 늦어요. `oracle`은 EDF라 안 늦고요. 이 gap은 진짜지만 **algorithm 선택(EDF vs MLFQ)에서 오지 cap 값에서 오지 않아요.**
- 못 재는 건 딱 하나: "`false` row의 cap 값이 맞았나". calibrated table이 이 두 row에서 cap을 tuning할 근거가 없어요.

일반화하면: attribute가 scheduling에 영향을 주는 곳은 interactive mode(MLFQ 아래서 cap이 keystroke foreground를 보호), batch mode(wanted/unwanted가 algorithm과 share를 바꿈), gaming(chain의 woken stage가 residual class라 scan과 경쟁)이고, 순수 periodic mode(meeting, media)에서는 EDF가 이미 다 막아줘서 **없어요**. 이건 table의 결함이 아니라 policy space의 성질이고, RQ0 gate spec의 reporting line으로 pre-register해요.

## 8. 각자에게 — 무엇이 바뀌고 무엇이 그대로인가

**인경민 (simulator).**
- 바뀐 것 없음. interpretation contract, canonical schema, event op set, config schedule — 전부 그대로예요. 파일이 26개 늘었을 뿐 형식은 같아요.
- `batch_bandwidth_cap`의 batch-class rule(9월 9일 memo)이 C7에서 더 중요해졌어요: interactive counterpart 10개의 `clamscan`은 cpu-batch라 그 rule로 batch class에 들어가야 cap이 작동해요. `c7-backup`의 `borg`(io-stream, 3 ms burst)도 "한 slice를 꽉 채우면 batch"라는 rule로 batch class예요.
- §7의 finding 5가 simulator의 EDF 구현에 기대고 있어요: deadline class가 residual class보다 먼저, residual slice는 `residual_timeslice_us`(2 ms). 이게 맞다면 `c7-meeting`·`c7-media`에서 어떤 cap에서도 miss가 0이어야 해요 — 통합 때 sanity check로 쓸 수 있어요.

**박이안 (daemon).**
- recognizer가 보는 것(telemetry의 이름 multiset)의 형식은 그대로예요. 새로 보게 될 이름: `zoom`(c1-meeting), `dkms`(c7-compile). 나머지는 이미 있던 이름이에요. `clamscan`이 열 개 파일에 더 나타나요.
- ground truth에 새 annotation key `pre_committed_miss`가 `attributes` 안에 들어와요(다섯 segment). validator는 annotation을 안 보니 영향 없고, grader(Phase 8)가 이걸로 accuracy에서 제외해요.
- `oracle`은 여전히 ground truth를 그대로 읽어요. C7의 `false` label도 그대로.
- attribute accuracy에 `false` 쪽이 생겼어요: grid 위 63 segment 중 18개가 `false`(전에는 2). 다만 segment 수로 세면 항상 `true`라고 답해도 약 71%(전에는 95%)라 **아직 majority가 큰 편**이에요 — 그리고 grader는 segment가 아니라 query point 단위로 채점하니 실제 baseline은 log가 나와야 알아요. 그래서 headline은 raw accuracy가 아니라 **balanced accuracy**(true recall과 false recall의 평균 — 항상 `true`면 정확히 50)에 confusion matrix를 옆에 두는 것으로 가야 하고, raw accuracy는 majority baseline을 옆에 찍은 채로만 보고해요. 32 cell 전부에 instance가 있으니 `false` recall을 mode별로 읽을 수 있어요. 이건 Phase 8(RQ0 gate spec)의 결정이고, 아래 공통 항목에 넣었어요.
- repeat index memo(9월 7일)는 그대로 유효해요.

**공통 (RQ0 gate spec, Phase 8).**
- judging set은 Phase 7에서 다시 정했어요(7.7, 2026-09-10). 규칙: label이 다른 pair의 한쪽이고 scored term이 row 차이를 설계상 감지하는 파일 — demand는 기준이 아니에요. 27개: C2 6 + batch C1 base 6 + term 있는 C7 15. interactive·periodic C1 base 10개, C3, C4, idle 둘은 보고만. `c7-gaming`·`c7-meeting`·`c7-media`는 note가 붙은 채로 judging, pre-committed miss 5개는 judging에 들어가되 Layer 1 accuracy에서만 제외. Q8의 per-file admission test가 gate의 per-file 기준이 돼요("27개 중 K개 이상이 gap ≥ g", K·g는 Phase 8이 실행 전에 확정). 자세한 건 RQ0 preparation notes §8.
- reporting line 후보: `c7-meeting`·`c7-media`의 headroom은 EDF-vs-MLFQ(§7); pre-committed miss 다섯 segment는 accuracy 제외; C7의 demand는 calibration class로 면제(pair가 통제).
- attribute accuracy의 headline은 **balanced accuracy + confusion matrix**, raw accuracy는 majority baseline과 함께만. `false`가 18/63 segment라 raw accuracy 혼자서는 majority에 끌려요. 파일을 더 늘려 50:50을 맞추는 대신 metric 정의로 푸는 거예요.
- calibrated table을 tuning하는 "throwaway pool"이 어디에도 정의돼 있지 않아요. RQ0 gate spec에서 정해야 해요.

## 9. 숫자 요약

| | Phase 7 전 | Phase 7 후 |
|---|---|---|
| 파일 | 24 | 50 |
| segment (grid 위) | 37 (+1 ambiguous) | 63 (+1 ambiguous) |
| driver-table cell 채움 | 17 / 32 | 32 / 32 |
| `false` segment | 2 | 18 |
| always-`true`의 attribute accuracy (segment 기준 raw; headline은 balanced accuracy) | ≈ 95% | ≈ 71% |
| pre-committed miss (attribute 쪽) | 0 | 5 |
| novel / derived timeline | 13 / 11 | 23 / 27 |
| recipe 파일 | 4 | 5 |
| compiled artifacts | 48 | 100 |
| scoring spec | 23 파일, 44 term | 48 파일, 78 term |
| CI가 빈 cell을 잡나 | 아니오 | 예 |

## 10. 어디를 읽으면 되나

- 결정 전체: `_dev/docs/spec/jioh/phase-7-coreset-attribute-coverage.md`
- 파일 하나하나: `docs/workload/coreset-guide.md` §10 (C1 추가분, C7)
- 설계 근거: `docs/workload/building-plan.md` §3 (C1, C7, counts, balance check), §5a
- pair 검토와 finding: `docs/daemon/prior-table-pair-review.md` §C, findings 4–6
- annotation과 batch-mode clause: `docs/recognition-vocabulary.md` §1, changelog
- 이름 검증 결과: `dataset/meas/names/run-2/`
- 직접 보기: `cd dataset && make dataset && python3 tools/derive.py` — grid가 32줄로 찍혀요.
