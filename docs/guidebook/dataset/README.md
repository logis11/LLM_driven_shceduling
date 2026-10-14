# 데이터셋 가이드북

> Status: draft · Created 2026-10-14 · Updated 2026-10-14

이 저장소의 workload dataset을 처음부터 끝까지 이해하기 위한 여덟 권입니다. 데이터셋이 연구에서 맡는 일, 재료가 되는 archetype library, timeline이 canonical workload로 compile되는 규칙, core set의 51개 파일, 생성한 층의 1,562개 파일, 숫자 하나하나의 근거와 측정과 검증, 같은 바이트를 보장하는 build gate와 CI, 그리고 그 모든 모양을 정한 결정들의 연대기를 다룹니다.

독자는 운영체제와 scheduling을 처음 접하는, 경험 있는 full-stack software engineer입니다. 설명은 한국어로 쓰고 기술 용어는 영어 그대로 둡니다. 이 저장소가 만든 용어와 OS·scheduling 용어는 쓰기 전에 한 줄로 풀고, 참조하는 문서·결정·memo는 그 내용을 본문에 적어 다른 파일을 열지 않아도 읽히게 합니다. 모든 결정은 기록된 이유와 함께 적고, 기록된 이유가 없으면 그렇다고 적습니다. 모든 수는 트리와 대조했습니다(2026-10-14).

## 권 목록

| 권 | 제목 | 답하는 질문 |
|---|---|---|
| 1 | [데이터셋의 큰 그림](01-the-big-picture.md) | 이 데이터셋은 무엇이고, 연구에서 어떤 일을 맡으며, 왜 이런 모양인가 |
| 2 | [Archetype library: process 하나를 scheduler의 눈으로 적기](02-the-archetype-library.md) | `archetypes.yaml`의 29개 항목은 각각 무엇을 어떻게 흉내 내고, 그 숫자들은 어디서 왔나 |
| 3 | [Timeline에서 canonical workload로: 포맷과 compiler](03-timeline-to-canonical-workload.md) | 사람이 쓴 timeline 파일 하나가 어떤 규칙으로 simulator가 읽는 workload JSON이 되나 |
| 4 | [51개의 coreset: 파일마다 어떤 질문에 답하나](04-the-coreset.md) | core set의 파일 하나하나는 무슨 상황을 적고, 어떤 label을 달고, 어떤 질문에 답하나 |
| 5 | [Generated layer: 열여섯 task set으로 만든 1,562개 파일](05-the-generated-layer.md) | 왜 손으로 쓴 core set 옆에 생성한 층이 있고, 그 파일들은 어떤 규칙으로 만들어지며 어떻게 점수를 받나 |
| 6 | [근거, 측정, 검증: 숫자 하나가 믿을 수 있게 되는 길](06-grounding-measurement-verification.md) | 데이터셋의 숫자와 구조는 어떤 기준으로 근거를 얻고, 직접 잰 것은 어떻게 재고 확인했으며, 틀린 것은 어떻게 찾아내 고쳤나 |
| 7 | [Build gate, manifest, CI, tests: 같은 바이트를 보장하는 장치](07-build-gate-manifests-ci-tests.md) | 아무도 commit하지 않는 `build/`가 어떻게 모두에게 같은 파일임이 보장되고, 무엇이 그것을 지키나 |
| 8 | [의사결정 연대기: 2026-08-23부터 지금까지](08-decision-chronicle.md) | 이 데이터셋의 모양을 정한 결정들은 언제, 왜, 무엇을 대신해서 내려졌고, 무엇이 아직 열려 있나 |

## 읽는 순서

1권이 틀을 잡고 2권부터 7권이 층마다 안으로 들어갑니다. 8권은 같은 내용을 시간 순서로 다시 봅니다. 처음이면 1 → 3 → 4 → 2 → 5 → 7 → 6 → 8을 권합니다. 어떤 파일이 왜 그렇게 생겼는지가 급하면 4권(core set)이나 5권(generated layer)에서 그 파일 항목을 바로 찾아도 됩니다. 각 권은 다른 권을 절 번호가 아니라 이름과 내용으로 가리키며, 마지막 장에 그 권에서 푼 용어를 모아 둡니다.

## 본문 안의 표시

개념을 설명한 직후에 인용 블록으로 붙습니다.

- **왜 이렇게 정했나.** 그 결정의 기록된 이유, 날짜, 기록된 곳.
- **코드로.** 어디에 어떻게 구현되어 있고 그 코드가 무엇을 하는지.
- **열린 자리.** 기록이 아직 정하지 않았거나(미정), 확인하지 않았거나(확인 필요), 아직 돌리지 않은(미실행) 자리 — 무엇이 열려 있고 누가 정하는지.

문서와 트리가 어긋나는 곳은 현재의 트리(data file, manifest, code, Phase 9의 기록)를 기준으로 적고, 어긋남 자체를 그 자리에 밝힙니다.
