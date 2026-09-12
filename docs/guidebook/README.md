# 가이드북 시리즈

이 연구를 처음부터 끝까지 이해하기 위한 교과서 시리즈입니다.

운영체제를 전혀 모르는 상태에서 시작해서, 이 연구가 무엇을 주장하고 어떻게 검증하며 그 결과가 논문의 어느 부분이 되는지까지 갑니다.

## 권 목록

| 권 | 제목 | 답하는 질문 | 상태 |
|---|---|---|---|
| 1 | [시스템과 scheduling](vol-01-systems-and-scheduling.md) | scheduler는 왜 어려운 문제이고, MLFQ는 무엇을 보고 판단하나 | 초고 |
| 2 | [관련 연구 지형도](vol-02-related-work.md) | 이 분야에서 무엇이 시도됐고 어디서 멈췄나 | 초고 |
| 3 | 이 연구의 큰 그림 | 무엇이 gap이고, recognition layer는 어떤 architecture이며, 무엇이 이 주장을 무너뜨리나 | 예정 |
| 4 | 실험의 뼈대 | 이 주장을 어떻게 측정 가능한 형태로 바꾸나 | 예정 |
| 5 | 공유 어휘 | mode와 attribute는 왜 이 목록인가 | 예정 |
| 6 | Workload 1: 재료와 근거 | archetype의 숫자들은 어디서 왔나 | 예정 |
| 7 | Workload 2: 조립과 compile | timeline이 어떻게 실행 가능한 workload가 되나 | 예정 |
| 8 | Workload 3: 50개 coreset | 각 파일이 어떤 질문에 답하나 | 예정 |
| 9 | Simulator와 interpretation contract | workload가 어떻게 실행되는 task가 되나 | 예정 |
| 10 | Config schema와 driver table | 어휘가 어떻게 scheduler 설정이 되나 | 예정 |
| 11 | Daemon과 recognition | LLM에게 무엇을 보여주고 그 답을 왜 검증하나 | 예정 |
| 12 | Harness | trace가 어떻게 논문의 숫자가 되나 | 예정 |
| 13 | RQ0 gate와 그 너머 | 왜 gate를 먼저 통과해야 하고, 그 다음은 무엇인가 | 예정 |

## 본문 안의 네 가지 장치

개념을 설명한 직후에 인용 블록으로 붙습니다.

- **이 연구에서는.** 방금 배운 일반론이 이 연구에서 어떤 결정으로 나타났는지, 왜 그렇게 정했는지.
- **코드로.** 그 개념이 어디에 어떻게 구현되어 있는지.
- **논문으로.** 그 내용이 논문의 어느 부분이 되는지.
- **아직 미정.** 확정되지 않았거나 코드가 없는 지점. RQ0 너머의 계획도 이 표시를 씁니다.
