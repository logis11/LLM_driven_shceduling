# 2권 · 관련 연구 지형도

**이 분야에서 무엇이 시도됐고, 어디서 멈췄나**

---

앞 권에서 문제를 봤습니다. scheduler는 지금 컴퓨터가 무엇에 쓰이고 있는지 모르고, 그 모름을 세 가지로 메우고 있습니다. 행동을 관찰하거나, 프로그램의 자기 선언을 받거나, 사람이 손으로 적어둔 목록을 뒤지거나.

이 권은 그 문제를 다른 연구자들이 어떻게 다뤄왔는지를 봅니다.

목적이 둘입니다. 첫째, 남들이 어디까지 갔는지 알아야 이 연구가 무엇을 새로 하는지 말할 수 있습니다. 둘째, 논문의 related work 절은 결국 이 지형도를 글로 옮긴 것이라서, 여기서 정리한 것이 그대로 논문의 한 절이 됩니다.

읽고 나면 네 갈래의 연구 흐름을 각각 설명할 수 있고, 각 흐름이 어디서 멈췄는지 말할 수 있고, 이 연구가 그 사이 어느 빈칸에 서 있는지 그림으로 그릴 수 있습니다.

---

## 목차

1. [이 장르의 논문을 읽는 법](#1장--이-장르의-논문을-읽는-법)
2. [고전: 지금 쓰는 것들이 어디서 왔나](#2장--고전-지금-쓰는-것들이-어디서-왔나)
3. [mechanism: policy를 갈아 끼울 수 있게 만든 연구들](#3장--mechanism-policy를-갈아-끼울-수-있게-만든-연구들)
4. [behavior를 읽는 계열](#4장--behavior를-읽는-계열)
5. [학습된 scheduler](#5장--학습된-scheduler)
6. [LLM을 kernel policy에 쓰는 시도들](#6장--llm을-kernel-policy에-쓰는-시도들)
7. [이미 배포되어 있는 semantic recognition](#7장--이미-배포되어-있는-semantic-recognition)
8. [평가는 무엇으로 하나](#8장--평가는-무엇으로-하나)
9. [지형도: 두 축과 빈칸](#9장--지형도-두-축과-빈칸)
10. [related work 절은 어떻게 쓰는가](#10장--related-work-절은-어떻게-쓰는가)
11. [용어 정리](#11장--용어-정리)

---

## 이 권의 표기

본문 중간에 인용 블록으로 붙는 표시가 넷입니다.

> **논문으로.** 이 내용이 논문의 어느 절에서 어떤 역할을 하는지.

> **이 연구에서는.** 앞의 연구와 이 연구가 무엇이 같고 무엇이 다른지.

> **확인 필요.** 1차 자료를 직접 읽고 확인하지 못한 부분. 무엇을 확인해야 하는지와 왜 지금 확인하지 못했는지를 함께 적습니다.

> **코드로.** 저장소의 어느 파일에 대응하는지.

세 번째 표시에 대해 한 가지 밝혀둡니다. 이 권을 쓰는 환경에서 학술 논문 사이트 상당수에 접근할 수 없었습니다. 그래서 원문을 직접 읽고 확인한 것과, 저자들의 공개 저장소나 2차 자료로만 확인한 것을 구분해서 표시했습니다. 표시가 붙은 곳은 논문에 인용하기 전에 반드시 원문을 확인해야 합니다.

---

# 1장 · 이 장르의 논문을 읽는 법

## 1.1 왜 남의 논문을 읽어야 하나

이 연구의 최종 산출물은 논문입니다. 그리고 논문에는 related work라는 절이 반드시 들어갑니다.

related work를 인용 목록으로 오해하기 쉽습니다. "이런 연구들이 있었다"를 나열하고 넘어가는 절처럼 보이니까요.

실제로는 그 절이 하는 일이 다릅니다. **이 연구가 앉을 자리가 비어 있다는 것을 증명하는 글입니다.**

심사자는 논문을 읽으면서 계속 이렇게 묻습니다. 이거 이미 있는 거 아닌가. 저 논문이 이미 했잖아. 왜 저 방법으로는 안 되는데. related work의 각 문단은 그 질문 하나씩을 미리 받아서 답하는 자리입니다.

그러니까 남의 연구를 정확히 아는 것이 자기 연구를 방어하는 일과 같습니다. 대충 알면 대충 방어하게 되고, 심사자는 그걸 바로 알아봅니다.

## 1.2 systems 논문의 생김새

컴퓨터 시스템 분야의 논문은 대체로 같은 골격을 가집니다. 각 절이 무슨 일을 하는지 알면 읽는 속도가 크게 달라집니다.

### Abstract

논문 전체를 열 문장 정도로 압축한 것입니다. 보통 이런 순서입니다. 문제가 무엇이고, 기존 방법이 왜 부족하고, 우리는 무엇을 만들었고, 얼마나 좋아졌는가.

마지막 항목이 중요합니다. **abstract에 적힌 숫자가 그 논문이 스스로 내세우는 성적표입니다.** 그 숫자가 어떤 조건에서 나왔는지가 논문의 절반입니다.

### Introduction

문제를 풀어서 설명하고, 왜 어려운지 보이고, 자기 접근을 소개하고, 마지막에 기여 목록을 붙입니다.

**기여 목록은 introduction의 끝에 있습니다.** 보통 "이 논문의 기여는 다음과 같다"로 시작하는 목록입니다. 논문을 빨리 파악하려면 abstract 다음에 이걸 읽는 것이 가장 효율적입니다.

### Motivation 또는 Background

문제가 실재한다는 것을 보이는 자리입니다. 측정을 해서 "지금 이런 손해가 나고 있다"를 숫자로 제시하는 경우가 많습니다.

이 절이 강하면 논문 전체가 설득력을 얻습니다. 반대로 이 절이 약하면 "그래서 이게 왜 문제인데"라는 질문이 끝까지 따라다닙니다.

### Design

시스템의 구조를 설명합니다. 어떤 구성 요소가 있고, 어떻게 상호작용하고, 어떤 결정을 왜 그렇게 내렸는지.

여기서 눈여겨볼 것은 **거절한 대안**입니다. 좋은 논문은 "이렇게 할 수도 있었지만 이런 이유로 하지 않았다"를 적습니다. 그게 없으면 저자가 대안을 검토하지 않았거나 숨기고 있는 것입니다.

### Implementation

실제로 무엇으로 어떻게 만들었는지. 코드 줄 수, 어떤 커널 버전에 붙였는지, 어떤 언어를 썼는지 같은 것들입니다.

짧게 넘어가는 절이지만 정보가 있습니다. 구현이 몇백 줄이면 아이디어가 단순하다는 뜻이고, 몇만 줄이면 실용화 부담이 크다는 뜻입니다.

### Evaluation

가장 중요하고, 가장 의심해야 할 절입니다. 다음 절에서 따로 다룹니다.

### Related work

앞에서 말한 그 절입니다.

### Conclusion과 Future work

요약과 남은 일. 대체로 새 정보가 없습니다. 다만 future work에 적힌 것이 그 연구팀의 다음 논문 주제인 경우가 많아서, 후속 연구를 찾을 때 단서가 됩니다.

### 읽는 순서

처음부터 끝까지 순서대로 읽는 것은 비효율적입니다. 보통 이렇게 합니다.

1. Abstract를 읽는다.
2. Introduction의 마지막, 기여 목록을 읽는다.
3. Evaluation의 그림과 표만 훑는다. 무엇을 무엇과 비교했는지 본다.
4. 여기까지에서 관심이 생기면 Design을 읽는다.
5. 이 논문을 인용하거나 반박할 거라면 그때 전부 읽는다.

## 1.3 어디에 실렸는지가 말해주는 것

같은 내용이라도 어디에 실렸느냐에 따라 읽는 태도가 달라집니다. 이건 권위를 따지자는 게 아니라 **얼마나 걸러졌는지**를 아는 문제입니다.

### 정식 학회

운영체제와 시스템 분야에서 자주 만나게 될 이름들입니다.

**SOSP**와 **OSDI**가 이 분야의 대표 학회로 꼽힙니다. 게재율이 낮고 심사가 깁니다.

**EuroSys**, **ASPLOS**, **USENIX ATC**, **NSDI**, **FAST**도 주요 학회입니다. 각각 성격이 조금씩 다릅니다. NSDI는 네트워크와 분산 시스템 쪽, FAST는 저장 장치 쪽, ASPLOS는 하드웨어와 소프트웨어의 경계 쪽입니다.

**SIGCOMM**은 네트워크 분야의 대표 학회인데, 시스템 분야의 학습 기반 연구가 여기 실리는 경우가 있습니다.

이런 학회의 논문은 여러 명의 심사자가 여러 차례 검토했고, 대체로 반박 기회와 수정 기회를 거쳤습니다. 그래도 틀릴 수 있지만, 명백한 결함은 대부분 걸러졌다고 봐도 됩니다.

### Workshop

학회에 붙어서 열리는 소규모 행사입니다. 논문이 짧고, 심사가 가볍고, 아이디어 단계의 연구를 받아줍니다.

workshop 논문은 **"이런 방향이 있다"까지가 주장의 범위**라고 보는 것이 안전합니다. 평가가 충분하지 않은 경우가 많습니다. 저자들도 그걸 알고 있고, 보통 정식 학회 논문으로 확장하는 것을 목표로 합니다.

### arXiv

심사가 없습니다. 저자가 올리면 그대로 공개됩니다.

그래서 arXiv 논문을 읽을 때는 검증되지 않았다는 것을 전제해야 합니다. 좋은 연구도 많고, 실제로 학회에 내기 전에 미리 올리는 것이 관행이라서 나중에 정식 게재되는 경우도 많습니다. 하지만 지금 이 순간의 그 문서는 심사를 통과한 것이 아닙니다.

**두 가지를 꼭 확인해야 합니다.** 첫째, 판본 번호입니다. arXiv 논문은 저자가 계속 고쳐 올릴 수 있어서, v1과 v4의 내용이 크게 다를 수 있습니다. 인용할 때는 판본을 명시해야 합니다. 둘째, 그 사이에 정식 게재됐는지입니다. 게재됐다면 그쪽을 인용해야 합니다.

> **이 연구에서는.** 저장소의 인용 목록에 이 규칙이 실제로 적혀 있습니다. arXiv 인용에는 판본 번호가 붙어 있고, 가장 가까운 선행 연구에 대해서는 "제출할 때마다 후속 논문이 나왔는지 다시 확인할 것"이라는 메모가 달려 있습니다. 뒤에서 그 연구를 다룰 때 다시 나옵니다.

### Artifact evaluation

최근 시스템 분야 학회들은 논문과 별도로 코드와 데이터를 심사하는 절차를 둡니다. 통과하면 논문 첫 페이지에 배지가 붙습니다.

배지가 있으면 최소한 남이 돌려봤다는 뜻입니다. 재현 가능성 면에서 의미 있는 신호입니다.

## 1.4 evaluation을 의심하는 법

논문에서 가장 조심해서 읽어야 할 절입니다. 저자가 자기 시스템이 좋다는 것을 보이려고 쓴 절이기 때문입니다.

의심할 지점을 순서대로 정리하면 이렇습니다.

### 무엇과 비교했는가

**가장 중요한 질문입니다.** 성능 개선 수치는 baseline이 무엇이냐에 따라 얼마든지 달라집니다.

기본 설정 그대로의 시스템과 비교하면 개선폭이 크게 나옵니다. 하지만 그 분야에서 실제로 쓰이는 최선의 방법과 비교하면 개선폭이 작아지거나 사라질 수 있습니다.

논문을 읽을 때 이렇게 물어야 합니다. **이 저자가 이길 수 있는 상대를 고른 것은 아닌가?**

> **이 연구에서는.** 이 질문이 이 연구의 설계에 직접 반영되어 있습니다. 기본 scheduler와 비교하는 것으로는 부족하다고 보고, 사람이 손으로 적은 이름 목록을 충실히 재현한 조건을 만들어서 그것과 비교합니다. 이름을 읽는다는 아이디어의 가장 강한 비LLM 구현이 그것이기 때문입니다. 그리고 그쪽이 이기는 경우도 이긴 대로 보고한다는 원칙을 미리 정해뒀습니다.

### 무엇을 돌렸는가

workload가 무엇인지, 그리고 그게 현실을 대표하는지입니다.

특정 workload에서만 좋고 다른 데서는 나쁘다면, 그 사실이 논문에 나와 있어야 합니다. 좋은 논문은 자기가 나쁜 경우도 보고합니다.

### 어떤 숫자를 보여주는가

평균만 보여주는지, 꼬리도 보여주는지입니다.

앞 권에서 봤듯이 평균은 자주 거짓말을 합니다. 대화형 성능을 다루는 논문이 평균만 보고한다면 그 자체가 신호입니다.

### 몇 번 돌렸는가

한 번 돌린 결과인지, 여러 번 돌려서 분산을 보고했는지입니다.

시스템 측정은 생각보다 흔들립니다. 오차 막대가 없는 그래프는 그것만으로 신뢰도가 낮아집니다.

### 어디까지가 측정이고 어디부터가 추정인가

시뮬레이션 결과를 실측처럼 제시하거나, 일부만 측정하고 나머지를 외삽한 경우가 있습니다.

논문이 정직하면 그 경계를 명시합니다. 명시하지 않았다면 독자가 찾아내야 합니다.

## 1.5 인용을 등급으로 나눈다는 것

논문에서 어떤 주장을 하려면 근거가 필요합니다. 그런데 모든 근거가 같은 무게를 갖지는 않습니다.

예를 들어 이런 세 문장을 봅시다.

1. "사용자가 상호작용에 대한 반응을 0.1초 안에 받으면 즉각적이라고 느낀다."
2. "게임 실행 중 배경 다운로드를 자동으로 멈추는 설정이 실제 소프트웨어에 존재한다."
3. "우리가 측정한 결과, 이 프로그램의 CPU 사용량은 평균 12퍼센트였다."

세 문장은 근거의 성격이 완전히 다릅니다.

첫 번째는 사람의 지각에 대한 주장입니다. 실험으로 확인된 학술 문헌이 뒷받침해야 합니다.

두 번째는 존재에 대한 주장입니다. 그런 설정이 있다는 것만 보이면 되고, 제품 문서나 공개 저장소로 충분합니다.

세 번째는 우리가 직접 잰 것입니다. 어떻게 쟀는지를 재현 가능하게 적어야 합니다.

### 세 등급

이 연구는 인용을 세 등급으로 나눠서 관리합니다.

| 등급 | 무엇인가 | 어디에 실리나 | 무엇을 뒷받침할 수 있나 |
|---|---|---|---|
| scholarly | 심사를 거친 학술 문헌 | 번호 붙은 참고문헌 목록 | 실험적, 행동적, 통계적 주장 |
| deployed-system | 배포된 소프트웨어의 문서나 저장소 | 각주에 URL과 확인 날짜와 판본 | **존재 주장만** |
| measurement | 우리가 직접 측정한 것 | 실행 식별자와 함께 | 우리 측정 범위 안의 값 |

가운데 등급의 제약이 핵심입니다. **배포된 시스템은 그런 것이 존재한다는 것만 증명합니다.**

게임 실행 파일 목록을 쓰는 기능이 있다는 것은 그 제품 문서로 보일 수 있습니다. 하지만 "그래서 사용자들이 이렇게 행동한다"거나 "그 방식이 얼마나 효과적이다"는 그 문서로 뒷받침할 수 없습니다. 그건 다른 종류의 주장이고 다른 종류의 근거가 필요합니다.

이 구분을 지키지 않으면 논문이 조용히 무너집니다. 심사자는 이런 것을 잘 찾아냅니다.

### 확인하지 않은 것은 확인하지 않았다고 적는다

한 가지 규칙이 더 있습니다.

인용은 **1차 자료를 직접 확인한 것만** 씁니다. 다른 논문이 인용한 것을 그대로 옮기지 않습니다. 확인했으면 확인한 날짜를 적고, 확인하지 못했으면 미확인이라고 표시합니다.

이게 왜 중요한지 실제 사례가 있습니다. 이 연구의 초기 조사에서, 널리 인용되는 수치 하나가 어느 심사 논문에도 없고 인터뷰 기사 한 편에만 존재한다는 것을 발견했습니다. 여러 논문이 그 수치를 학술 문헌인 것처럼 인용하고 있었습니다. 결국 그 수치는 인터뷰로 인용하거나 아예 빼는 것으로 정리했습니다.

또 다른 사례로, 저자를 잘못 붙인 인용과 연도가 틀린 인용도 조사 과정에서 발견되어 고쳤습니다. 원문을 직접 열어보지 않으면 이런 것을 잡을 수 없습니다.

> **논문으로.** 이 규칙 자체가 논문의 신뢰도를 만듭니다. 심사자가 인용 하나를 찍어서 확인했는데 틀렸다면, 나머지 인용도 전부 의심받습니다. 반대로 인용이 정확하면 본문의 주장도 함께 신뢰를 얻습니다.

---

## 1장 정리

- related work는 인용 나열이 아니라 이 연구가 앉을 자리가 비어 있음을 증명하는 글입니다. 각 문단은 심사자의 반론 하나씩을 미리 받아서 답합니다.
- systems 논문은 abstract, introduction, motivation, design, implementation, evaluation, related work, conclusion의 골격을 가집니다. 빠르게 파악하려면 abstract, introduction 끝의 기여 목록, evaluation의 그림 순서로 읽습니다.
- design 절에서는 거절한 대안이 적혀 있는지를 봅니다. 없으면 검토하지 않았거나 숨기는 것입니다.
- 어디에 실렸는지가 얼마나 걸러졌는지를 말해줍니다. 정식 학회는 여러 차례 심사를 거쳤고, workshop은 아이디어 단계이며, arXiv는 심사가 없습니다. arXiv를 인용할 때는 판본 번호를 적고 정식 게재 여부를 다시 확인해야 합니다.
- evaluation에서 가장 중요한 질문은 무엇과 비교했는가입니다. 저자가 이길 수 있는 상대를 고른 것은 아닌지 의심해야 합니다. 이어서 어떤 workload인지, 평균인지 꼬리인지, 몇 번 돌렸는지, 어디까지가 측정인지를 봅니다.
- 인용은 세 등급으로 나뉩니다. 심사를 거친 학술 문헌은 실험적이고 통계적인 주장을 뒷받침할 수 있고, 배포된 시스템의 문서는 존재 주장만 뒷받침할 수 있으며, 직접 측정한 값은 재현 가능하게 적어야 합니다.
- 1차 자료를 직접 확인한 것만 인용합니다. 널리 인용되는 수치가 어느 심사 논문에도 없는 경우가 실제로 있습니다.

---

# 2장 · 고전: 지금 쓰는 것들이 어디서 왔나

## 2.1 이 장이 하는 일

앞 권에서 알고리즘을 여럿 배웠습니다. MLFQ, lottery, EDF, fair-share. 그런데 출처를 붙이지 않고 넘어갔습니다.

이 장에서 그 출처를 붙입니다.

목적이 둘입니다. 첫째, 논문을 쓰려면 인용해야 하고, 인용하려면 원문에 무엇이 적혀 있는지 알아야 합니다. 둘째, 원문을 보면 그 아이디어가 어떤 문제를 풀려고 나왔는지가 드러납니다. 교과서에서 정리된 형태로 배우면 그 맥락이 사라집니다.

이 장의 인용문은 대부분 이 연구팀이 원문을 직접 열어서 확인하고 기록해둔 것입니다. 확인 날짜와 어느 절의 어느 문장인지까지 저장소에 적혀 있습니다. 확인되지 않은 것은 그렇다고 표시합니다.

## 2.2 timesharing의 시작

### 무엇을 풀려던 문제였나

1960년대 초의 컴퓨터는 한 번에 프로그램 하나를 돌렸습니다. 프로그램을 카드 뭉치로 만들어서 제출하면, 운영자가 순서대로 넣어서 돌리고, 결과를 종이로 받아 갔습니다.

문제는 오타 하나였습니다. 오타 하나 때문에 프로그램이 죽으면, 고쳐서 다시 제출하고 다음 차례를 기다려야 했습니다. 한 번의 수정에 몇 시간이 걸렸습니다.

여기서 나온 발상이 timesharing입니다. 여러 사람이 각자 단말기 앞에 앉아서 동시에 컴퓨터를 쓰는 것입니다. 컴퓨터는 하나지만 아주 빠르게 번갈아 처리하면 각자 자기 컴퓨터를 쓰는 것처럼 느낍니다.

### 인용

- Corbató, F. J., Merwin-Daggett, M., & Daley, R. C. (1962). An Experimental Time-Sharing System. *Proc. Spring Joint Computer Conference (AFIPS '62)*, 335–344. DOI 10.1145/1460833.1460871.

이 논문이 발표한 시스템이 **CTSS**입니다. Compatible Time-Sharing System의 약자입니다.

그리고 이 논문이 앞 권에서 다룬 MLFQ의 원조로 인용됩니다. 여러 단계의 대기열을 두고 프로그램을 그 사이에서 옮기는 구조가 여기서 처음 나왔습니다.

> **확인 필요.** 이 논문의 서지 정보는 확인됐지만, 본문의 scheduling 알고리즘 서술을 직접 읽고 확인하지는 못했습니다. 이 권을 쓰는 환경에서 논문 원문을 담은 사이트에 접근할 수 없었습니다. 구체적으로 확인해야 할 것은 세 가지입니다. 프로그램이 처음 어느 단계에 배치되는지를 정하는 규칙, 각 단계에서 주는 시간의 크기, 그리고 단계 사이를 오가는 조건입니다. 논문에 인용하기 전에 원문을 열어서 확인해야 합니다.

> **논문으로.** MLFQ를 인용할 때 선택지가 둘입니다. 원조인 이 논문을 인용하거나, 교과서를 인용하거나. 이 연구는 상황에 따라 나눠 씁니다. "MLFQ라는 알고리즘 계열이 여기서 시작됐다"는 역사적 주장에는 원조를, "MLFQ의 규칙은 이렇다"는 서술과 실험의 기본 설정값에는 교과서를 인용합니다. 뒤에서 그 이유를 봅니다.

## 2.3 real-time scheduling의 이론적 기반

### 인용

- Liu, C. L., & Layland, J. W. (1973). Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment. *Journal of the ACM*, 20(1), 46–61. DOI 10.1145/321738.321743.

앞 권에서 EDF를 다루면서 "utilization의 합이 1 이하이면 모든 마감을 지킨다"는 정리를 소개했습니다. 그 정리가 이 논문에 있습니다.

### 논문이 세운 전제

이 논문은 다섯 개의 가정 위에서 논의합니다. 그중 이 연구에 직접 쓰이는 것이 두 번째 가정입니다.

> "each task must be completed before the next request for it occurs"

각 작업은 다음 요청이 도착하기 전에 끝나야 한다는 뜻입니다. 즉 **마감이 곧 다음 주기의 시작**입니다.

앞 권에서 이걸 period-implicit deadline이라고 불렀습니다. 그 개념의 출처가 여기입니다.

> **이 연구에서는.** 시뮬레이터의 EDF 구현이 이 가정을 그대로 씁니다. 주기적으로 도는 task의 각 job은 다음 주기가 시작되는 시점을 마감으로 갖습니다. 설정 파일에 마감을 따로 적을 필요가 없고, 적을 수도 없습니다. 이 설계 결정의 근거가 이 문장입니다.

### 핵심 정리

논문의 일곱 번째 정리가 EDF의 조건을 말합니다.

> "the deadline driven scheduling algorithm is feasible if and only if (C₁/T₁) + (C₂/T₂) + … + (Cₘ/Tₘ) ≤ 1"

C는 각 작업이 한 번에 필요한 계산 시간이고, T는 주기입니다. 그 비율의 합이 1 이하일 때, 그리고 그때만, EDF가 모든 마감을 지킬 수 있다는 뜻입니다.

**if and only if라는 표현이 중요합니다.** 두 방향을 다 말하고 있습니다. 합이 1 이하이면 EDF가 성공하고, 1을 넘으면 어떤 알고리즘으로도 불가능합니다. 그러니까 EDF는 이 조건에서 최적입니다.

### 고정 우선순위와의 대비

논문의 초록은 고정 priority 방식과 비교합니다. 최적의 고정 priority 방식이라도 작업 수가 많아지면 utilization 한계가

> "may be as low as 70 percent for large task sets"

까지 떨어질 수 있다고 적혀 있습니다.

앞 권에서 rate monotonic을 다루며 언급한 그 숫자입니다. EDF가 100퍼센트까지 가는데 고정 priority는 70퍼센트 근처에서 막힌다는 것이 이 대비의 요점입니다.

### 인용할 때의 범위

이 논문을 인용할 때 지켜야 할 선이 있습니다. **논문은 다섯 개 가정 아래, 단일 프로세서 위의 주기적 작업에 대해서만 말합니다.** utilization이 1을 넘었을 때 무슨 일이 일어나는지는 다루지 않습니다.

앞 권에서 EDF가 과부하에서 연쇄적으로 무너진다고 설명했는데, 그 서술은 이 논문에서 나온 것이 아닙니다. 다른 근거가 필요합니다.

> **논문으로.** 인용의 범위를 넘지 않는 것이 이 연구의 원칙입니다. 저장소의 인용 기록에는 각 문헌마다 "이 문헌은 어떤 주장을 뒷받침할 수 있는가"가 한 줄로 적혀 있고, 그 범위를 벗어나서 인용하지 말라고 규칙에 명시되어 있습니다.

## 2.4 비율로 나누기의 원조

### 인용

- Waldspurger, C. A., & Weihl, W. E. (1994). Lottery Scheduling: Flexible Proportional-Share Resource Management. *Proc. First Symposium on Operating Systems Design and Implementation (OSDI '94)*, USENIX.

앞 권에서 다룬 lottery scheduling의 원 논문입니다. 각 task에 티켓을 나눠 주고 추첨으로 고르는 그 방식입니다.

### 무엇을 보장하는가

논문의 첫 절이 이 방식이 보장하는 것을 이렇게 적습니다.

> "the resource consumption rates of active computations are proportional to the relative shares that they are allocated"

활성 계산들의 자원 소비율이 각자 할당받은 상대적 몫에 비례한다는 뜻입니다.

여기서 **비례한다**는 것이 핵심입니다. 순서를 정하는 것이 아니라 비율을 정합니다. 앞 권에서 priority 기반과 proportional share 기반을 구분한 이유가 이것입니다.

### 시간 척도에 대한 정직한 서술

무작위 추첨의 약점은 짧은 구간에서 비율이 흔들린다는 것입니다. 논문은 이 문제를 숨기지 않고 이렇게 적습니다.

> "With a scheduling quantum of 10 milliseconds (100 lotteries per second), reasonable fairness can be achieved over subsecond time intervals. As computation speeds continue to increase, shorter time quanta can be used to further improve accuracy"

10밀리초 quantum이면 초당 100번 추첨이고, 그 정도면 1초 이하 구간에서도 어느 정도의 공정성이 나온다는 뜻입니다. 그리고 계산 속도가 빨라지면 quantum을 줄여서 정확도를 더 높일 수 있다고 덧붙입니다.

**"reasonable fairness"라는 표현에 주목할 만합니다.** 완벽한 공정성이 아니라 합리적인 수준의 공정성입니다. 논문이 자기 한계를 정확히 말하고 있습니다.

### 논문이 말하지 않는 것

이 연구에 실질적으로 중요한 지점이 여기 있습니다.

이 연구의 시뮬레이터는 lottery 방식을 지원하는데, task 하나하나에 티켓을 주는 대신 task를 두 부류로 나누고 부류 사이의 비율을 설정값으로 둡니다. 그럼 그 비율의 기본값을 얼마로 해야 할까요?

**원 논문은 부류 사이의 비율을 말하지 않습니다.** 티켓 수에 비례해서 나눈다는 원리만 제시하고, 어떤 종류의 작업에 얼마를 주라는 이야기는 없습니다.

> **이 연구에서는.** 그래서 이 값은 근거 없는 가정이라고 문서에 명시해뒀습니다. 저장소의 설정 스키마 문서를 보면 각 기본값마다 근거가 한 줄씩 적혀 있는데, 이 값의 칸에는 "출처 없음, 가정"이라고 적혀 있습니다.
>
> 근거가 없으면 없다고 적는 것이 왜 중요한가. 논문 심사자가 "이 값은 왜 이겁니까"라고 물었을 때, "저희가 정한 가정입니다"라고 답하는 것과 답을 못 하는 것은 완전히 다릅니다. 그리고 그 값 때문에 결론이 흔들리는지 확인하는 절차를 미리 계획에 넣어둘 수 있습니다.

## 2.5 fair-share의 이론

### 인용

- Stoica, I., & Abdel-Wahab, H. (1995). Earliest Eligible Virtual Deadline First: A Flexible and Accurate Mechanism for Proportional Share Resource Allocation. Technical Report TR-95-22, Old Dominion University.

앞 권에서 Linux가 CFS를 EEVDF로 교체했다고 언급했습니다. 그 EEVDF의 원 문헌입니다.

주의할 점이 하나 있습니다. **연도가 1995년입니다.** 1996년으로 잘못 적힌 인용을 종종 보게 되는데, 저장소의 인용 기록에 이 점이 명시되어 있습니다. 이런 것이 원문을 직접 확인해야 하는 이유입니다.

> **확인 필요.** 이 기술보고서의 서지 정보는 확인됐지만, 본문을 직접 읽고 확인하지는 못했습니다. 확인해야 할 것은 네 가지입니다. virtual time, eligible time, virtual deadline, lag 각각의 정의, 그리고 이상적인 배분과 실제 배분의 차이에 대한 보장이 정확히 어떤 형태인지입니다. 이 개념들이 지금 Linux scheduler의 동작을 설명하는 데 그대로 쓰이므로, 논문에서 이 계열을 서술하려면 원문 확인이 필요합니다.

## 2.6 0.1초는 어디서 왔나

앞 권에서 "사람은 0.1초 안에 반응이 오면 즉각적이라고 느낀다"는 값을 여러 번 썼습니다. 이 값이 이 연구의 측정 상수로 들어가 있어서, 출처가 특히 중요합니다.

### 원 출처

- Miller, R. B. (1968). Response time in man-computer conversational transactions. *Proc. AFIPS Fall Joint Computer Conference (FJCC '68)*, 267–277.

이 논문은 사람과 컴퓨터가 주고받는 여러 종류의 상호작용을 열여덟 가지 주제로 나누고, 각각에 대해 허용 가능한 응답 시간을 제시합니다.

그중 첫 번째 주제가 "Response to control activation", 즉 조작에 대한 반응입니다.

> "should be immediate and perceived as a part of the mechanical action induced by the operator. Time delay: No more than 0.1 second."

반응이 즉각적이어야 하고, 조작자가 유발한 기계적 동작의 일부처럼 지각되어야 하며, 지연은 0.1초를 넘지 않아야 한다는 뜻입니다.

타이핑에 대해서는 조금 다르게 말합니다.

> "the delay between depressing the key and the visual feedback should be no more than 0.1 to 0.2 seconds"

그리고 곧바로 단서를 답니다.

> "this delay in feedback may be far too slow for skilled keyboard users"

숙련된 타이피스트에게는 이것도 너무 느릴 수 있다는 것입니다.

**이 단서가 중요합니다.** 0.1초는 편안한 목표가 아니라 느슨한 상한입니다.

### 널리 인용되는 2차 출처

- Nielsen, J. (1993). *Usability Engineering*. Academic Press. 5장 "Usability Heuristics"의 응답 시간 절.

> "0.1 second is about the limit for having the user feel that the system is reacting instantaneously"

인터페이스 설계 쪽에서 이 값이 널리 알려진 것은 이 책 덕분입니다. 그리고 이 책은 자기 출처로 Miller의 1968년 논문을 명시하고 있습니다.

### 범위를 알려주는 세 번째 출처

- Shneiderman, B. (1984). Response Time and Display Rate in Human Performance with Computers. *ACM Computing Surveys*, 16(3), 265–285.

이 논문은 Long이 1976년에 한 연구를 보고합니다. 키 입력이 화면에 나타나기까지의 지연이

> "approximately 0.1–0.5 second"

일 때 이미

> "unskilled and skilled typists worked more slowly and made more errors with longer response times. Even these brief delays were distracting in the rapid process of typing."

라는 결과가 나왔다고 적혀 있습니다.

숙련자와 비숙련자 모두 느려지고 실수가 늘었으며, 이 짧은 지연조차 타이핑이라는 빠른 과정에서는 방해가 됐다는 것입니다.

**여기서 인용 규율의 실제 사례가 나옵니다.** 이 결과는 Long의 연구인데, 우리가 읽은 것은 Shneiderman의 리뷰 논문입니다. 그러면 인용은 "Shneiderman이 보고한 Long의 결과"로 해야지, Long을 직접 인용하면 안 됩니다. 저장소의 인용 기록에 이 점이 명시되어 있습니다.

> **이 연구에서는.** 세 문헌이 함께 쓰입니다. 0.1초라는 임계값 자체는 Miller가 근거이고, Nielsen이 그것을 널리 알린 2차 근거이며, Shneiderman은 그 값이 여유로운 목표가 아니라 느슨한 상한이라는 것을 보여주는 범위입니다.
>
> 그리고 이 값이 측정에 어떻게 쓰이는지도 정해져 있습니다. 사용자가 기다리는 성격의 task가 깨어난 뒤 실행되기까지의 지연이 이 값을 넘은 비율을 셉니다. 다만 이 비율 하나만 보지 않고 백분위수 값들도 함께 봅니다. 비율은 넘었는지 여부만 세기 때문에 얼마나 크게 넘었는지를 버리기 때문입니다.

## 2.7 교과서를 인용한다는 것

### 인용

- Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books. "Scheduling: The Multi-Level Feedback Queue" 장.

무료로 공개된 운영체제 교과서입니다. 이 연구가 이 책을 인용하는 방식이 조금 특이해서 따로 다룹니다.

### 보통은 서술의 근거로 씁니다

MLFQ의 규칙을 설명할 때 이 책의 정리를 인용합니다. 앞 권에서 규칙 다섯 개를 순서대로 쌓았는데, 그 형태가 이 책의 정리를 따른 것입니다.

교과서를 인용하는 것은 흔한 일입니다. 원 논문은 역사적 맥락 속에서 쓰여서 지금의 용어와 다를 수 있고, 교과서는 정리된 형태를 제공합니다.

### 그런데 이 연구는 설정값까지 가져왔습니다

여기가 특이한 부분입니다.

실험을 하려면 비교 기준이 될 scheduler 설정이 필요합니다. queue를 몇 개로 할지, 최상위 slice를 얼마로 할지, boost를 얼마마다 할지.

**그런데 표준이라고 부를 만한 값이 존재하지 않습니다.** 실제 운영체제들의 값은 각자 다르고, 왜 그 값인지에 대한 공개된 근거도 없습니다.

이 연구는 이 문제를 이렇게 풀었습니다. **한 출처의 예제를 통째로 가져다 씁니다.**

가져온 값과 그 근거는 이렇습니다.

| 설정 | 값 | 이 책의 어디 |
|---|---|---|
| queue 개수 | 3 | 8장의 예제들이 "a three-queue scheduler"로 돌아가고, 모든 그림에 Q2, Q1, Q0이 나옵니다 |
| 최상위 slice | 10 밀리초 | 첫 번째 예제가 "with a time slice of 10 ms (and with the allotment set equal to the time slice)"입니다 |
| slice 증가 비율 | 2 | "Lower Priority, Longer Quanta"라는 제목의 그림이 10밀리초, 20밀리초, 40밀리초로 갑니다 |
| boost 간격 | 100 밀리초 | 그림 하나가 "a priority boost every 100 ms (which is likely too small of a value, but used here for the example)"로 설명됩니다 |

### 왜 통째로 가져오는가

값을 여러 출처에서 하나씩 골라 조합할 수도 있습니다. queue 개수는 이 논문에서, slice는 저 커널 소스에서, boost 간격은 또 다른 데서.

그렇게 하면 **그 조합 자체가 어디에도 없는 새로운 설정이 됩니다.** 각 값에는 출처가 있지만 그 조합에는 출처가 없습니다. 심사자가 "왜 이 조합입니까"라고 물으면 답할 말이 없습니다.

한 출처에서 통째로 가져오면 최소한 "이 교과서의 예제 설정"이라고 말할 수 있습니다. 방어 가능한 형태입니다.

이 원칙이 저장소 문서에 한 문장으로 적혀 있습니다. 한 텍스트에서 나온 설정은 하나의 주장이고, 여러 출처에서 조립한 값은 쓰지 않는다는 것입니다.

### 교과서가 스스로 붙인 단서

재미있는 것은 이 책이 자기 예제 값에 단서를 달아뒀다는 점입니다.

boost 간격 100밀리초에 대해 이 책은 "which is likely too small of a value, but used here for the example"이라고 적습니다. 아마 너무 작은 값일 텐데 예제를 위해 쓴다는 뜻입니다.

그리고 이런 종류의 값을 부르는 이름을 소개합니다. **voo-doo constant**입니다. 원래 이 표현을 쓴 사람의 이름을 밝히면서, 이런 값은 이론으로 정할 수 없고 결국 경험으로 정한다고 설명합니다.

> **이 연구에서는.** 이 단서를 숨기지 않고 그대로 인용합니다. 우리가 가져온 값이 그 책 스스로 "아마 너무 작다"고 말한 값이라는 사실을 문서에 적어뒀습니다.
>
> 그리고 그 값 하나 때문에 결론이 뒤집히지 않는지 확인하는 절차를 미리 계획에 넣었습니다. 최상위 slice를 0.5밀리초부터 100밀리초까지 아홉 가지로 바꿔가며 전체 실험을 다시 돌리고, 결론이 유지되는지 봅니다. 유지되지 않으면 결론을 하나의 값이 아니라 범위로 보고합니다.
>
> 이 아홉 개 값도 아무렇게나 고른 것이 아닙니다. 각각에 이유가 붙어 있습니다. 예를 들어 그중 하나는 실제 Linux의 fair-share scheduler가 쓰는 최소 단위이고, 다른 하나는 정책 교체 기능이 쓰는 기본값이며, 또 다른 하나는 상용 유닉스 계열의 표에서 나온 값입니다.

### 모델과 예제가 다른 지점

한 가지 더. 이 연구의 시뮬레이터와 교과서 예제가 정확히 한 군데서 다릅니다.

앞 권에서 allotment를 다뤘습니다. 한 queue에서 쓸 수 있는 누적 시간이고, 이걸 넘으면 아래로 내려갑니다.

이 교과서의 첫 번째 예제는 allotment를 slice와 같게 놓습니다. 즉 slice 하나를 다 쓰면 바로 내려갑니다. 그런데 같은 장의 다른 그림에서는 상위 두 단계에 slice 두 개 분량의 allotment를 줍니다.

이 연구의 시뮬레이터는 앞의 방식을 따릅니다. allotment를 별도 설정으로 두지 않고 slice 하나로 내립니다.

**이 차이가 문서에 명시되어 있습니다.** "우리 모델과 인용한 예제가 정확히 여기서 다르다"고요. 나중에 결과를 해석할 때 이 차이를 알고 있어야 하기 때문입니다.

## 2.8 실제 시스템의 숫자들

고전 문헌과 별개로, 지금 돌아가는 시스템들이 실제로 어떤 값을 쓰는지도 확인해두면 감이 잡힙니다. 이 값들은 전부 소스 코드나 공식 문서에서 직접 읽어 확인한 것입니다.

**Linux의 fair-share scheduler.** CFS 시절의 소스에는 목표 지연이 6밀리초, 최소 단위가 0.75밀리초로 적혀 있습니다. EEVDF로 바뀐 뒤에는 기본 slice가 0.75밀리초입니다. 둘 다 소스의 주석에 코어 수에 따라 늘어난다는 설명이 붙어 있습니다.

**Linux의 정책 교체 기능.** 기본 slice 상수가 20밀리초로 정의되어 있습니다.

**상용 유닉스 계열의 MLFQ.** 우선순위 단계가 60개이고, 표로 각 단계의 quantum이 정해져 있으며, 초당 한 번 전체를 훑으면서 조정하는 함수가 돕니다. 기본 설정에서 quantum은 최상위가 2밀리초, 최하위가 20밀리초입니다.

이 값들을 나란히 놓으면 폭이 꽤 넓습니다. 0.75밀리초부터 20밀리초까지입니다. **어느 하나를 표준이라고 부를 수 없다는 것이 이 목록이 보여주는 사실입니다.**

> **논문으로.** 이 목록 자체가 논문에서 쓰입니다. "왜 교과서 예제를 기준으로 삼았는가"에 대한 답이 "실제 시스템들의 값이 이만큼 흩어져 있고 표준이 없기 때문"이고, 그 흩어짐을 보이는 것이 이 목록입니다.
>
> 다만 인용 등급을 지켜야 합니다. 이 값들은 소스 코드와 제품 문서에서 왔으므로 **존재 주장에만** 쓸 수 있습니다. "이 시스템은 이 값을 쓴다"까지가 한계이고, "그러므로 이 값이 좋다"로 넘어갈 수 없습니다.

---

## 2장 정리

- CTSS를 발표한 1962년 논문이 timesharing과 multilevel feedback의 출발점으로 인용됩니다. 다만 이 권을 쓰는 환경에서 원문을 확인하지 못해, 알고리즘 서술의 세부는 미확인으로 남겨뒀습니다.
- 1973년 Liu와 Layland의 논문이 EDF의 이론적 기반입니다. 마감이 다음 주기의 시작이라는 가정, 그리고 utilization 합이 1 이하일 때 그리고 그때만 EDF가 성공한다는 정리가 여기 있습니다. 고정 priority 방식은 작업 수가 많으면 70퍼센트 근처까지 떨어질 수 있다는 대비도 초록에 있습니다.
- 이 논문은 다섯 가지 가정 아래 단일 프로세서의 주기적 작업만 다룹니다. 과부하 상황은 다루지 않으므로 그 서술에 인용할 수 없습니다.
- 1994년 Waldspurger와 Weihl의 논문이 lottery scheduling의 원조입니다. 소비율이 할당된 몫에 비례한다는 것이 보장이고, 10밀리초 quantum이면 1초 이하 구간에서도 합리적인 수준의 공정성이 나온다고 스스로 적었습니다. 부류 사이의 비율은 말하지 않습니다.
- 1995년 EEVDF 기술보고서가 지금 Linux scheduler의 기반입니다. 연도를 1996년으로 잘못 적는 인용이 흔합니다. 본문은 미확인으로 남겨뒀습니다.
- 0.1초라는 값은 1968년 Miller의 논문이 원 출처이고, 1993년 Nielsen의 책이 널리 알린 2차 출처이며, 1984년 Shneiderman의 리뷰가 그 값이 여유로운 목표가 아님을 보여줍니다. Shneiderman이 보고한 것은 Long의 연구이므로 Shneiderman을 통해 인용해야 합니다.
- 이 연구는 실험의 기본 scheduler 설정을 한 교과서의 예제에서 통째로 가져왔습니다. 여러 출처에서 값을 조합하면 그 조합 자체에 출처가 없어지기 때문입니다. 그 교과서가 자기 값에 붙인 단서까지 그대로 인용하고, 값 하나 때문에 결론이 뒤집히는지 확인하는 절차를 미리 계획에 넣어뒀습니다.
- 실제 시스템들의 slice 값은 0.75밀리초부터 20밀리초까지 흩어져 있습니다. 표준이 없다는 사실 자체가 근거로 쓰입니다.

---

# 3장 · mechanism: policy를 갈아 끼울 수 있게 만든 연구들

## 3.1 이 갈래가 푸는 문제

지금까지의 이야기는 "어떤 정책이 좋은가"였습니다. 이 장의 연구들은 다른 질문을 붙잡습니다.

> **정책을 바꾸는 것 자체가 왜 이렇게 어려운가.**

앞 권에서 봤듯이 scheduler는 kernel 안에 있는 함수입니다. 그러니까 정책을 바꾸려면 kernel 코드를 고쳐야 합니다. 고치고, 다시 빌드하고, 재부팅해야 합니다.

이게 실무에서 어떤 의미인지 생각해보면 문제가 보입니다.

**실험이 느립니다.** 아이디어 하나를 시험하는 데 빌드와 재부팅이 필요합니다.

**배포가 위험합니다.** 새 scheduler에 버그가 있으면 시스템이 멈춥니다. 수천 대의 기계에 배포하는 상황이라면 감당할 수 없는 위험입니다.

**되돌리기가 어렵습니다.** 문제가 생겨도 다시 재부팅해야 합니다.

그래서 새 scheduling 아이디어가 나와도 실제로 쓰이기까지 몇 년이 걸렸습니다. 그리고 그 사이에 아이디어를 검증할 방법이 사실상 없었습니다.

이 갈래의 연구들은 그 벽을 낮췄습니다.

## 3.2 ghOSt: 결정을 user space로 넘기기

### 인용

- Humphries, J. T., Natu, N., Chaugule, A., Weisse, O., Rhoden, B., Don, J., Rizzo, L., Rombakh, O., Turner, P., & Kozyrakis, C. (2021). ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling. *Proc. SOSP '21*. DOI 10.1145/3477132.3483542.

> **확인 필요.** 이 논문의 본문을 직접 읽지 못했습니다. 이 권을 쓰는 환경에서 논문 PDF를 담은 사이트와 출판사 사이트에 모두 접근할 수 없었습니다.
>
> 아래 인용문은 전부 **저자들이 직접 공개한 코드 저장소의 설명 문서**에서 가져온 것입니다. 저자가 같으니 내용은 신뢰할 만하지만, 논문의 초록이나 본문과는 다른 문서입니다. 논문에 인용할 때는 반드시 논문 원문을 확인하고, 저장소 문서를 인용하는 경우에는 그렇다고 명시해야 합니다.
>
> 특히 확인하지 못한 것은 성능 수치입니다. 이 연구가 어떤 workload에서 얼마나 개선했다고 주장하는지는 논문을 열어봐야 알 수 있습니다.

### 무엇을 하는가

저자들의 저장소는 이 시스템을 이렇게 설명합니다.

> "ghOSt is a general-purpose delegation of scheduling policy implemented on top of the Linux kernel. The ghOSt framework provides a rich API that receives scheduling decisions for processes from userspace and actuates them as transactions."

kernel 위에 얹은 범용 정책 위임 장치이고, user space에서 온 scheduling 결정을 받아서 **transaction으로 실행한다**는 것입니다.

여기서 두 단어가 핵심입니다.

**delegation, 즉 위임.** 결정을 내리는 주체가 kernel 밖으로 나갔습니다. kernel은 결정을 받아서 실행만 합니다.

**transaction.** 결정이 하나의 원자적 단위로 전달되고 적용됩니다. 데이터베이스의 transaction과 같은 발상입니다.

### 왜 이게 큰 변화인가

저장소는 이렇게 이어갑니다.

> "Programmers can use any language or tools to develop policies, which can be upgraded without a machine reboot."

정책을 **어떤 언어로든** 짤 수 있고, **재부팅 없이 교체할 수 있다**는 것입니다.

kernel 코드를 짜려면 C를 써야 하고, kernel 안에서는 쓸 수 있는 라이브러리가 제한되고, 실수하면 시스템 전체가 죽습니다. 그 제약이 사라집니다.

> "ghOSt supports policies for a range of scheduling objectives, from µs-scale latency, to throughput, to energy efficiency, and beyond, and incurs low overheads for scheduling actions. Many policies are just a few hundred lines of code."

**정책 하나가 몇백 줄**이라는 대목이 인상적입니다. 앞 권에서 본 MLFQ의 규칙이 여섯 줄이었던 것을 떠올리면, 알고리즘 자체는 원래 크지 않습니다. 크고 어려웠던 것은 그걸 kernel 안에 안전하게 넣는 일이었습니다.

### enclave라는 구조

이 시스템은 기계를 여러 구역으로 나눌 수 있게 합니다.

> "ghOSt uses **enclaves** to group agents and the threads that they are scheduling. An enclave contains a subset of CPUs (i.e., logical cores) in a machine, the agents that embody those CPUs, and the threads in the ghOSt scheduling class that the enclave agents can schedule onto the enclave CPUs."

> "Enclaves provide an easy way to partition the machine to support co-location of policies and tenants, a particularly important feature as machines scale out horizontally to contain hundreds of CPUs and new accelerators."

core가 수백 개인 기계에서는 전체에 하나의 정책을 쓰는 것이 오히려 이상합니다. 구역을 나눠서 각 구역에 다른 정책을 두는 것이 자연스럽습니다.

### 재부팅 없는 교체가 실제로 어떻게 되는가

저장소가 그 절차를 설명합니다.

> "When you want to upgrade a policy, the agents in the new process that you launch attempt to attach to the existing enclave, waiting for the old agents running in the enclave to exit. Once the old agents exit, the new agents take over the enclave and begin scheduling."

새 정책 프로세스를 띄우면 기존 구역에 붙으려고 대기하고, 기존 것이 빠지면 인계받습니다.

### 정책이 망가지면

가장 중요한 질문입니다. user space의 프로그램에 scheduling을 맡겼는데 그게 죽으면 어떻게 되나요?

> "ghOSt also recovers from scheduler failures (e.g., crashes, malfunctions, etc.) without triggering a kernel panic or machine reboot. To recover from a scheduler failure, you should generally destroy the failed scheduler's enclave and then launch the scheduler again. Destroying an enclave will kill the malfunctioning agents if necessary and will move the threads in the ghOSt scheduling class to CFS (Linux Completely Fair Scheduler) so that they can continue to be scheduled until you potentially pull them into ghOSt again."

구역을 없애면 그 안의 thread들이 기본 scheduler로 되돌아간다는 것입니다. 시스템은 멈추지 않습니다.

**이 설계가 정책 실험을 가능하게 만든 핵심입니다.** 실패해도 기본값으로 돌아가면 되니까 시도해볼 수 있습니다.

## 3.3 sched_ext: 같은 일을 mainline에서

### 인용

- Linux kernel documentation. "Extensible Scheduler Class." Linux 6.12에 병합.

앞의 연구는 별도의 kernel 패치가 필요했습니다. 그러니까 그 패치를 적용한 kernel을 써야 했습니다.

**sched_ext는 같은 능력을 표준 Linux에 넣었습니다.** 2024년 말에 나온 kernel 버전부터 들어가 있습니다.

> **확인 필요, 그리고 어떻게 해결했는지.** 공식 문서 사이트에도 접근할 수 없었습니다. 대신 그 문서가 생성되는 **원본 파일을 Linux 소스 트리에서 직접 읽었습니다.** 렌더링된 웹 페이지가 아니라 소스의 원문이므로 내용은 동일하고, 오히려 kernel 버전별 차이까지 확인할 수 있었습니다.
>
> 아래 인용문에는 어느 버전의 문서인지를 함께 적었습니다. 병합된 버전과 최신 버전의 서술이 다른 곳이 있기 때문입니다.

### 무엇인가

문서의 첫 문장입니다. 병합된 버전과 최신 버전이 동일합니다.

> "sched_ext is a scheduler class whose behavior can be defined by a set of BPF programs - the BPF scheduler."

**BPF**는 kernel 안에서 안전하게 프로그램을 돌릴 수 있게 해주는 장치입니다. 원래는 네트워크 패킷을 거르는 용도로 만들어졌는데, 지금은 kernel의 여러 곳에 사용자 프로그램을 끼워 넣는 범용 수단이 됐습니다.

핵심은 kernel이 그 프로그램을 실행하기 전에 검사한다는 점입니다. 무한 루프를 돌지 않는지, 접근하면 안 되는 메모리를 건드리지 않는지 확인합니다.

### 문서가 내세우는 네 가지

> "* sched_ext exports a full scheduling interface so that any scheduling algorithm can be implemented on top.
> * The BPF scheduler can group CPUs however it sees fit and schedule them together, as tasks aren't tied to specific CPUs at the time of wakeup.
> * The BPF scheduler can be turned on and off dynamically anytime.
> * The system integrity is maintained no matter what the BPF scheduler does. The default scheduling behavior is restored anytime an error is detected, a runnable task stalls, or on invoking the SysRq key sequence `SysRq-S`."

넷째 항목이 앞의 연구와 같은 발상입니다. **BPF scheduler가 무슨 짓을 하든 시스템의 무결성은 유지됩니다.** 오류가 감지되거나, 실행 가능한 task가 멈춰 있거나, 특정 키 조합을 누르면 기본 동작으로 되돌아갑니다.

### 정확히 짚어야 할 두 가지

여기서 흔히 잘못 서술되는 지점이 둘 있습니다. 원문을 확인해서 알게 된 것입니다.

**첫째, 이 문서는 BPF 검사기가 무엇을 보장하는지에 대해 일반적인 진술을 하지 않습니다.** 검사기를 뜻하는 단어는 문서 전체에서 딱 한 번, 예제 코드의 주석 안에만 나옵니다.

> "/* Need to initialize or the BPF verifier will reject the program */"

그러니까 "BPF 검사기가 scheduler의 안전을 보장한다"는 식의 서술을 이 문서에 기대어 쓸 수 없습니다. 이 문서가 실제로 하는 안전 주장은 위에 인용한 "무슨 짓을 하든 무결성은 유지된다"입니다.

**둘째, 이 문서에는 감시 타이머라는 말이 나오지 않습니다.** 최신 버전과 병합 당시 버전 모두에 없습니다. 그 개념은 다음 절에서 다룰 다른 저장소의 문서에 나옵니다.

이런 것이 원문을 직접 확인해야 하는 이유입니다. 2차 자료를 읽고 쓰면 이런 구분이 뭉개집니다.

### 되돌아가는 조건

최신 버전 문서입니다.

> "Terminating the sched_ext scheduler program, triggering `SysRq-S`, or detection of any internal error including stalled runnable tasks aborts the BPF scheduler and reverts all tasks back to the fair-class scheduler."

병합 당시 버전은 같은 문장의 끝이 다릅니다. "reverts all tasks back to CFS"입니다. 그 사이에 Linux의 기본 scheduler 이름이 바뀐 것이 문서에 반영된 것입니다.

### 실행 중 켜고 끄기

문서에 실제 터미널 기록이 들어 있습니다.

```text
    # tools/sched_ext/build/bin/scx_simple
    local=0 global=3
    …
    ^CEXIT: BPF scheduler unregistered
```

프로그램을 실행하면 그 scheduler가 켜지고, 종료시키면 꺼집니다. 재부팅이 없습니다.

현재 상태는 파일로 확인할 수 있습니다. 상태를 담은 파일에 `enabled`가 들어 있고, 어떤 scheduler가 올라가 있는지를 담은 파일에 이름이 들어 있습니다.

### 다른 scheduling class와의 순서

최신 버전 문서에만 있는 문장입니다. 일부 task만 이 방식으로 돌릴 때의 이야기입니다.

> "only tasks with the ``SCHED_EXT`` policy are scheduled by sched_ext, while tasks with ``SCHED_NORMAL``, ``SCHED_BATCH`` and ``SCHED_IDLE`` policies are scheduled by the fair-class scheduler which has higher sched_class precedence than ``SCHED_EXT``."

기본 클래스가 sched_ext보다 우선한다는 것입니다.

**병합 당시 버전에는 이 우선순위 문장이 없습니다.** 그러니 이 문장을 인용하려면 최신 문서를 인용해야 합니다.

### 안정성에 대한 경고

문서가 스스로 붙인 단서입니다.

> "The APIs provided by sched_ext to BPF schedulers programs have no stability guarantees… they are subject to change without warning between kernel versions."

인터페이스가 kernel 버전 사이에 예고 없이 바뀔 수 있다는 것입니다. 이 기능이 아직 젊다는 신호입니다.

## 3.4 그 위에 실제로 올라간 scheduler들

### 인용

- sched-ext/scx 저장소.

sched_ext는 틀만 제공합니다. 실제 정책은 따로 짜야 합니다. 그 정책들을 모아둔 공식 저장소가 있습니다.

저장소의 자기 설명입니다.

> "sched_ext is a Linux kernel feature which enables implementing kernel thread schedulers in BPF and dynamically loading them. This repository contains various scheduler implementations and support utilities."

> "sched_ext enables safe and rapid iterations of scheduler implementations, thus radically widening the scope of scheduling strategies that can be experimented with and deployed; even in massive and complex production environments."

**빠른 반복이 가능해졌다**는 것이 이 문장의 요점입니다. 이 장의 서두에서 말한 벽이 낮아졌다는 뜻입니다.

### 감시 타이머는 여기 있습니다

앞에서 kernel 문서에 감시 타이머 이야기가 없다고 했습니다. 이 저장소에 있습니다.

> "In addition to terminating the program, there are two more ways to disable a `sched_ext` scheduler - `sysrq-S` and the watchdog timer. Ignoring kernel bugs, the worst damage a `sched_ext` scheduler can do to a system is starving some threads until the watchdog timer triggers."

**kernel 버그를 논외로 하면, BPF scheduler가 시스템에 입힐 수 있는 최악의 피해는 감시 타이머가 울릴 때까지 일부 thread를 굶기는 것**이라는 진술입니다.

앞 권에서 starvation을 배웠는데, 그 개념이 여기서 안전 논증의 상한으로 쓰이고 있습니다. 최악이 starvation이고 그것도 시간제한이 있다면, 정책을 실험해도 괜찮다는 논리입니다.

### 어떤 scheduler들이 있나

저장소에는 여러 정책이 들어 있습니다. 각자의 설명 문서에서 첫 줄을 옮기면 이렇습니다.

**scx_rusty** — "A multi-domain, BPF / user space hybrid scheduler. The BPF portion of the scheduler does a simple round robin in each domain, and the user space portion (written in Rust) calculates the load factor of each domain, and informs BPF of how tasks should be load balanced accordingly."

빠른 결정은 kernel 안에서, 느린 판단은 밖에서 하는 구조입니다. **이 분업이 이 시리즈의 연구와 같은 발상입니다.** 뒤에서 다시 나옵니다.

**scx_layered** — "A highly configurable multi-layer BPF / user space hybrid scheduler." 사용자가 task를 여러 층으로 분류하고 층마다 다른 정책을 적용할 수 있습니다.

**scx_lavd** — "scx_lavd is a BPF scheduler that implements an LAVD (Latency-criticality Aware Virtual Deadline) scheduling algorithm." 다음 장에서 따로 다룹니다.

**scx_bpfland** — "a vruntime-based sched_ext scheduler that prioritizes interactive workloads."

**scx_flash** — "A scheduler that focuses on ensuring fairness among tasks and performance predictability." 마감이 이른 순서로 고르는 방식을 쓰되 각 task에 지연 가중치를 준다고 적혀 있습니다.

이 목록에서 읽어야 할 것이 있습니다. **정책들이 서로 다른 목표를 겨냥하고 있습니다.** 어떤 것은 대화형 우선, 어떤 것은 공정성, 어떤 것은 지역성입니다.

앞 권에서 "모든 상황에서 최고인 scheduler는 없다"고 했는데, 그 사실이 이 목록으로 드러납니다. **사람들이 실제로 여러 개를 만들어두고 골라 쓰고 있습니다.**

### 얼마나 실제로 쓰이나

저장소의 진술입니다.

> "sched_ext is supported by the upstream kernel starting from version 6.12. Both Meta and Google are fully committed to sched_ext and Meta is in the process of mass production deployment."

개요 문서에는 이렇게도 적혀 있습니다.

> "At Meta, we are actively experimenting with multiple production workloads and seeing significant performance gains, and are in the process of deploying sched_ext schedulers on production workloads at scale."

배포판에 대해서는 이 진술이 가장 강합니다.

> "Distros are able to package and release these schedulers, allowing users to utilize these schedulers out-of-the-box without requiring any additional work or dependencies such as clang or building the scheduler programs themselves."

**배포판이 패키지로 제공할 수 있다는 것이지, 기본으로 켜서 출하한다는 뜻이 아닙니다.** 저장소 어디에도 특정 배포판이 이 중 하나를 기본값으로 쓴다는 진술은 없습니다.

> **논문으로.** 이 구분이 중요합니다. "이미 배포판이 이걸 기본으로 쓴다"고 쓰면 심사자가 근거를 요구할 것이고, 이 저장소로는 뒷받침되지 않습니다. 쓸 수 있는 것은 "패키지로 제공된다", "두 대형 사업자가 도입을 진행 중이라고 밝혔다"까지입니다.

## 3.5 이 갈래가 이 연구에 주는 것

### 액추에이터는 이미 있습니다

정리하면 이 갈래의 결론은 하나입니다.

**scheduling 정책을 실행 중에 바꾸는 일은 이제 가능합니다.** 재부팅도, kernel 재빌드도 필요 없습니다. 실패해도 기본값으로 돌아갑니다.

앞 권에서 스위치와 목록을 구분했습니다. 게임 모드가 하는 동작 자체는 잘 만들어져 있고, 없는 것은 그 스위치를 언제 눌러야 하는지 아는 능력이라고요.

이 갈래는 **스위치 쪽을 만든 연구들**입니다. 그리고 스위치는 완성됐습니다.

> **이 연구에서는.** 이 사실이 이 연구의 전제입니다. 저장소의 related work 초고에 이 관계가 한 문장으로 적혀 있습니다. 이 갈래는 경쟁 상대가 아니라 보완 관계이고, **기계가 고른 정책을 어떻게 실행하는가**에 답하면서 **기계가 어느 정책이 맞는지 어떻게 아는가**는 열어뒀다는 것입니다. 이 연구가 그 열린 질문을 맡습니다.
>
> 비유하면 이 갈래는 액추에이터를 만들었고, 이 연구는 센서를 만듭니다.

### 그리고 시뮬레이터 기반 평가의 정당화이기도 합니다

한 가지 더 있습니다. 이건 논문의 방어 논리와 직결됩니다.

이 연구는 실제 kernel이 아니라 시뮬레이터 위에서 실험합니다. 심사자는 당연히 이렇게 물을 것입니다. **왜 실제 시스템에서 안 했습니까?**

이 갈래의 존재가 그 질문에 대한 답의 절반입니다. **실행 계층은 이미 검증됐습니다.** 정책을 갈아 끼우고 안전하게 되돌리는 일이 실제로 가능하다는 것을 이 연구들이 이미 보였습니다.

그러니까 실행기를 시뮬레이터로 대체해서 잃는 것이 생각보다 적습니다. 이 연구가 검증하려는 것은 실행 가능성이 아니라 **인식이 도움이 되는가**이기 때문입니다.

> **논문으로.** 저장소의 related work 초고에 이 논리가 명시되어 있습니다. 이 문단이 "왜 시뮬레이터인가"에 대한 정직한 틀이 되고, 실제 kernel 구현은 future work으로 남긴다는 것입니다. 물론 이것으로 모든 반론이 막히지는 않습니다. 시뮬레이터가 실제 하드웨어의 무엇을 놓치는지는 별도로 다뤄야 합니다.

---

## 3장 정리

- 이 갈래는 "어떤 정책이 좋은가"가 아니라 "정책을 바꾸는 것 자체가 왜 어려운가"를 붙잡습니다. 원래는 kernel을 고치고 다시 빌드하고 재부팅해야 했고, 그래서 실험이 느리고 배포가 위험했습니다.
- ghOSt는 scheduling 결정을 user space로 위임하고 kernel은 그것을 transaction으로 실행합니다. 정책을 어떤 언어로든 짤 수 있고 재부팅 없이 교체할 수 있으며, 정책이 죽으면 그 구역의 thread들이 기본 scheduler로 되돌아갑니다. 다만 이 권을 쓰는 환경에서 논문 원문을 확인하지 못해, 인용문은 저자들의 코드 저장소에서 가져왔습니다.
- sched_ext는 같은 능력을 표준 Linux에 넣었습니다. BPF 프로그램으로 scheduler를 정의하고 실행 중에 켜고 끕니다. 문서가 내세우는 안전 주장은 BPF scheduler가 무슨 짓을 하든 오류나 멈춤이 감지되면 기본 동작으로 되돌아간다는 것입니다.
- 흔한 오해 둘을 원문 확인으로 바로잡았습니다. 이 문서는 BPF 검사기가 무엇을 보장하는지 일반적으로 진술하지 않으며, 감시 타이머라는 말도 나오지 않습니다. 감시 타이머는 정책 모음 저장소의 문서에 나옵니다.
- 그 저장소에는 서로 다른 목표를 겨냥한 정책이 여럿 들어 있습니다. 대화형 우선, 공정성, 지역성, 마감 기반이 각각 따로 있습니다. 모든 상황에 맞는 하나가 없다는 사실이 이 목록으로 드러납니다.
- 그중 하나는 빠른 결정을 kernel 안에서 하고 느린 판단을 밖에서 하는 분업 구조를 씁니다. 이 시리즈의 연구와 같은 발상입니다.
- 배포 현황에 대해 저장소가 뒷받침하는 것은 배포판이 패키지로 제공할 수 있다는 것과 두 대형 사업자가 도입을 진행 중이라는 진술까지입니다. 어떤 배포판이 기본으로 켠다는 진술은 없습니다.
- 이 갈래의 결론은 액추에이터가 이미 완성됐다는 것입니다. 이 연구는 그 위에 얹을 센서를 만듭니다. 그리고 실행 계층이 이미 검증됐다는 사실이 시뮬레이터 기반 평가를 정당화하는 논리의 절반입니다.

---

# 4장 · behavior를 읽는 계열

## 4.1 이 갈래가 하는 일

앞 장의 연구들은 정책을 갈아 끼우는 장치를 만들었습니다. 이 장의 연구들은 다른 질문을 붙잡습니다.

> **scheduler가 스스로 관찰해서 더 똑똑해질 수 있는가.**

앞 권에서 봤듯이 scheduler는 프로그램이 무엇인지 모릅니다. 대신 행동을 봅니다. CPU를 얼마나 쓰는지, 어떻게 놓는지, 얼마나 자주 깨어나는지.

이 갈래는 그 관찰을 더 정교하게 만들어서, 지금보다 나은 판단을 뽑아내려는 시도들입니다.

**그리고 이 갈래가 이 연구의 가장 직접적인 반대 입장입니다.** 이 갈래가 성공하면 이 연구가 필요 없어집니다. 그래서 정확히 알아야 합니다.

## 4.2 이미 배운 것들

앞 권에서 다룬 알고리즘들이 이미 이 갈래에 속합니다. 짧게 짚고 넘어갑니다.

**MLFQ의 강등 규칙.** task가 주어진 시간을 다 쓰면 우선순위를 낮추고, 스스로 잠들면 유지합니다. 이 규칙 하나로 계산 작업과 대화형 작업이 자동으로 분류됩니다. 프로그램이 무엇인지 전혀 몰라도 됩니다.

**fair-share의 누적 회계.** 각 task가 지금까지 쓴 시간을 가중치로 나눈 값을 추적하고, 가장 뒤처진 것을 실행합니다. 자고 있는 동안에는 그 값이 올라가지 않으니, 깨어났을 때 자연스럽게 앞줄에 섭니다. MLFQ가 규칙으로 하는 일을 구조적으로 하는 셈입니다.

두 방식 모두 재료가 같습니다. **시간과 횟수입니다.**

## 4.3 scx_lavd: 이 계열의 가장 발전한 형태

### 무엇인가

앞 장에서 본 정책 모음 저장소에 들어 있는 scheduler 중 하나입니다. 저장소의 설명 문서에서 옮깁니다.

> "scx_lavd is a BPF scheduler that implements an LAVD (Latency-criticality Aware Virtual Deadline) scheduling algorithm."

이름을 풀면 "지연 민감도를 아는 가상 마감"입니다.

핵심 아이디어를 문서가 두 줄로 정리합니다.

> "its core ideas are 1) measuring how much a task is latency critical and 2) leveraging the task's latency-criticality information in making various scheduling decisions"

**첫째, 각 task가 얼마나 지연에 민감한지를 측정합니다. 둘째, 그 정보를 여러 scheduling 결정에 씁니다.**

앞 권에서 fair-share 계열이 각 task에 가상의 마감을 부여한다고 했습니다. 이 방식은 그 마감을 정할 때 지연 민감도를 반영합니다. 민감한 task에게 이른 마감을 주면 먼저 실행됩니다.

### 어디서 나왔나

> "scx_lavd is initially motivated by gaming workloads."

게임 workload에서 출발했습니다. 그리고 저장소는 이 정책이 실전에서 쓸 만하다고 표시하고 있습니다.

> "Production Ready?: Yes, scx_lavd should be performant across various CPU architectures."

### 게임에서 실제로 무슨 일이 벌어지는가

이 정책을 만든 사람이 2024년 한 공개 행사에서 발표한 자료가 있습니다. 이 연구팀이 그 자료를 확인해서 숫자를 기록해뒀습니다.

발표 자료가 보고하는 게임 실행 중의 실제 모습은 이렇습니다.

| 관찰 | 값 |
|---|---|
| 실행 중인 task 수 | 약 300개 |
| 그중 오래 사는 task의 비율 | 약 90퍼센트 |
| 상위 30에서 40개 task가 차지하는 scheduling 비중 | 95퍼센트 |
| 상위 15에서 20개가 차지하는 비중 | 60에서 70퍼센트 |
| 한 번 실행될 때의 시간 | 약 260마이크로초에서 1.65밀리초 |
| 대기 계열 system call에서 깨어나는 비율 | 70에서 75퍼센트 |
| frame 예산 | 16.7밀리초 |

이 표에서 읽어야 할 것이 셋입니다.

**첫째, task가 많지만 대부분은 별로 안 씁니다.** 300개가 돌지만 그중 30에서 40개가 전체의 95퍼센트를 차지합니다. 나머지 260개는 거의 놀고 있습니다.

**둘째, 한 번에 쓰는 시간이 짧습니다.** 260마이크로초에서 1.65밀리초입니다. 앞 권에서 본 time slice가 밀리초 단위였던 것을 떠올리면, 이 task들은 slice를 다 쓰지 않고 내려간다는 뜻입니다.

**셋째, 대부분 다른 것을 기다리다가 깨어납니다.** 70에서 75퍼센트가 대기 계열 system call에서 깨어납니다. 앞 권에서 본 chain 구조입니다. 서로가 서로를 깨우면서 frame 하나를 만들어냅니다.

> **이 연구에서는.** 이 숫자들이 실제로 이 연구의 데이터셋을 만드는 데 쓰였습니다. 가상의 게임 workload를 만들 때 task를 몇 개로 하고 각각이 얼마나 쓰게 할지를 정해야 하는데, 그 근거가 이 발표 자료입니다.
>
> 특히 "상위 소수가 대부분을 차지한다"는 관찰이 중요하게 쓰였습니다. 이 연구의 실험은 core 하나만 쓰는데, 그러면 300개 task를 그대로 넣을 수 없습니다. 상위 몇 개로 줄여야 하고, 그 축소가 정당한지를 이 통계로 뒷받침합니다.
>
> 다만 인용 등급을 지켜야 합니다. 이건 발표 자료이므로 논문의 각주 수준으로 다뤄야 하고, 같은 내용을 다룬 기사 형태의 2차 자료를 함께 인용하는 방식으로 정리해뒀습니다.

## 4.4 왜 게임이 이 문제를 드러내는가

이 정책이 게임에서 출발한 것은 우연이 아닙니다. 게임이 이 갈래의 한계를 가장 잘 드러내는 상황이기 때문입니다.

앞 권에서 chain을 다뤘습니다. 여러 task가 순서대로 서로를 깨우면서 하나의 결과를 만드는 구조입니다. frame 하나가 그렇게 만들어집니다.

여기서 문제는 **scheduler가 각 task를 따로 본다**는 것이었습니다. 어떤 task가 사슬의 중간 단계라는 사실을 모릅니다. 그래서 각 단계에서 "이 정도 기다림은 괜찮다"고 판단한 것들이 쌓여서 마감을 넘깁니다.

이 정책이 하려는 것이 정확히 그 문제를 푸는 것입니다. **task가 어떤 사슬에 속해 있는지, 그 사슬이 얼마나 급한지를 행동에서 추정해서** 마감에 반영합니다.

**그리고 상당 부분 성공합니다.** 실전에서 쓸 만하다고 표시되어 있고, 게임 성능 개선 사례로 언급됩니다.

## 4.5 이 갈래의 한계

그럼 이걸로 충분한가요? 이 연구가 왜 필요한가요?

두 가지 층위의 답이 있습니다.

### 첫째, task의 성질이지 machine의 상황이 아닙니다

이 정책이 알아내는 것은 "이 task가 지연에 민감하다"입니다.

**"지금 이 컴퓨터가 게임 중이다"가 아닙니다.**

둘의 차이가 무엇인지 봅시다.

task 하나의 성질을 알면 그 task를 어떻게 대우할지 정할 수 있습니다. 유용합니다.

하지만 machine 전체의 상황을 알면 다른 종류의 결정이 가능해집니다. 배경 작업 전체를 억누를지, 알고리즘 자체를 바꿀지, 어떤 지표를 우선할지 같은 것들입니다. 그건 task 하나를 봐서는 나오지 않습니다.

앞 권에서 봤듯이 좋은 scheduling의 정의 자체가 상황에 따라 달라집니다. **정의를 바꾸려면 상황을 알아야 하고, 상황은 task 하나의 성질이 아닙니다.**

### 둘째, 행동 채널로는 원리적으로 안 되는 것이 있습니다

이게 더 근본적인 지점입니다.

앞 권에서 든 예를 다시 가져옵니다. 이 연구가 실험에서 실제로 쓰는 대비입니다.

한쪽에는 사용자가 직접 시작한 머신러닝 학습이 돌고 있고, 편집기가 옆에 켜져 있습니다. 다른 쪽에는 파일 색인 작업이 예약 실행으로 돌고 있고, 역시 편집기가 켜져 있습니다.

scheduler가 관찰할 수 있는 것을 나열해봅시다.

- CPU를 계속 쓰는 process가 하나 있다
- 짧게 깨어났다 자는 process가 하나 있다
- 디스크를 읽는다
- 가끔 잠든다

**두 상황에서 이 관찰이 전부 동일합니다.** 설계상 동일하게 만들었습니다.

그런데 올바른 대우는 정반대입니다. 앞쪽은 사용자가 결과를 기다리고 있으니 빨리 끝나야 하고, 뒤쪽은 아무도 부탁하지 않았으니 방해하면 안 됩니다.

**이 차이를 행동 관찰로 알아낼 방법이 없습니다.** 이 갈래를 아무리 정교하게 다듬어도 마찬가지입니다. 구분에 필요한 정보가 관찰 가능한 데이터에 존재하지 않기 때문입니다.

> **논문으로.** 이 논증의 형태가 중요합니다. "저 방법은 성능이 부족하다"가 아니라 **"저 방법의 입력 채널에 그 정보가 없다"**입니다.
>
> 앞엣것은 상대가 개선하면 무너지는 주장입니다. 뒤엣것은 개선으로 무너지지 않습니다. 그래서 이 연구는 뒤엣것으로 논증합니다.
>
> 그리고 그 논증을 말로만 하지 않고 **데이터셋으로 만들어뒀습니다.** 행동이 동일하고 올바른 설정이 다른 workload 쌍을 실제로 작성해서, 실험에서 그 쌍을 직접 돌립니다. 주장이 아니라 측정 대상이 됩니다.

## 4.6 그래도 이 연구는 이 계열을 버리지 않습니다

여기서 오해하기 쉬운 지점을 짚어둡니다.

이 연구가 행동 관찰을 대체하려는 것이 아닙니다. **그대로 씁니다.**

이 연구의 시뮬레이터가 실행하는 scheduler는 여전히 행동 기반입니다. MLFQ의 강등 규칙도 그대로이고, 계산 작업 부류를 판별하는 규칙도 행동으로 합니다. 프로그램 이름으로 판별하지 않습니다.

**추가되는 것은 그 위에 얹히는 상황 판단 한 겹입니다.** 그 판단이 scheduler의 설정을 바꾸고, scheduler는 바뀐 설정으로 평소처럼 행동 기반으로 동작합니다.

> **이 연구에서는.** 계산 작업 부류를 이름이 아니라 행동으로 판별하도록 못 박은 이유가 여기 있습니다. 만약 이름으로 판별한다면, 언어 모델이 이름을 읽어서 얻는 이득과 판별기가 이름을 읽어서 얻는 이득이 섞입니다. 그러면 무엇을 측정했는지 알 수 없게 됩니다.
>
> 이 규칙은 네 알고리즘 전부에서 동일하고 설정으로 바꿀 수 없게 고정되어 있습니다. 실험에서 변수를 하나만 두는 원칙이 여기에도 적용된 것입니다.

---

## 4장 정리

- 이 갈래는 scheduler가 스스로 관찰해서 더 똑똑해질 수 있는가를 묻습니다. 이 연구의 가장 직접적인 반대 입장이라서 정확히 알아야 합니다.
- MLFQ의 강등 규칙과 fair-share의 누적 회계가 이미 이 갈래에 속합니다. 두 방식 모두 재료가 시간과 횟수뿐입니다.
- 이 계열의 가장 발전한 형태가 scx_lavd입니다. 각 task가 얼마나 지연에 민감한지를 측정하고 그 정보를 마감 부여에 씁니다. 게임 workload에서 출발했고 실전에서 쓸 만하다고 표시되어 있습니다.
- 이 정책을 만든 사람의 발표 자료에 게임 실행 중의 실제 통계가 있습니다. task가 약 300개인데 상위 30에서 40개가 전체 scheduling의 95퍼센트를 차지하고, 한 번 실행이 260마이크로초에서 1.65밀리초이며, 70에서 75퍼센트가 대기 계열 system call에서 깨어납니다. 이 숫자들이 이 연구의 데이터셋 설계에 쓰였습니다.
- 게임이 이 갈래의 한계를 잘 드러내는 이유는 chain 구조 때문입니다. 각 단계의 작은 대기가 쌓여서 마감을 넘기는데, scheduler는 각 task를 따로 봅니다.
- 이 갈래의 한계는 두 층위입니다. 알아내는 것이 task 하나의 성질이지 machine 전체의 상황이 아니라는 것, 그리고 행동이 동일하고 올바른 대우가 다른 경우를 원리적으로 구분할 수 없다는 것입니다.
- 두 번째 논증의 형태가 중요합니다. 성능이 부족하다가 아니라 입력 채널에 그 정보가 없다는 것입니다. 앞엣것은 상대가 개선하면 무너지지만 뒤엣것은 무너지지 않습니다.
- 이 연구는 행동 관찰을 대체하지 않고 그대로 씁니다. 계산 작업 부류를 판별하는 규칙도 행동 기반으로 고정해뒀습니다. 이름으로 판별하면 무엇을 측정했는지 알 수 없어지기 때문입니다.

---

# 5장 · 학습된 scheduler

## 5.1 이 갈래가 하는 일

앞 장의 연구들은 사람이 손으로 쓴 규칙을 정교하게 다듬는 방향이었습니다. 이 장의 연구들은 다른 발상에서 출발합니다.

> **규칙을 사람이 쓰지 말고 기계가 배우게 하면 어떤가.**

scheduling은 결국 상태를 보고 행동을 고르는 문제입니다. 그런 문제는 기계학습, 특히 강화학습이 잘하는 영역입니다. 그러니 관찰된 시스템 상태를 입력으로 받아 scheduling 행동을 출력하는 모델을 학습시키자는 것입니다.

> **확인 필요, 이 장 전체에 해당.** 이 장에서 다루는 논문들의 초록은 확인했지만 **본문은 읽지 못했습니다.** 이 권을 쓰는 환경에서 출판사 사이트에 접근할 수 없었습니다.
>
> 아래 초록 인용문은 GitHub에 있는 논문 정보 모음 저장소에서 가져온 것입니다. 내용은 각 논문의 공식 초록과 일치하는 것으로 보이지만, 출판사 원문에서 다시 확인해야 합니다.
>
> 그리고 본문에만 있는 정보, 예를 들어 정확한 비교 대상이나 학습 비용 같은 것은 이 장에 적지 않았습니다. 기억으로 채우지 않았습니다.

## 5.2 Decima: cluster scheduling을 배우기

### 인용

- Mao, H., Schwarzkopf, M., Venkatakrishnan, S. B., Meng, Z., & Alizadeh, M. (2019). Learning Scheduling Algorithms for Data Processing Clusters. *Proc. SIGCOMM '19*. DOI 10.1145/3341302.3342080.

### 문제 설정

이 논문이 다루는 것은 데스크톱이 아니라 데이터 처리 cluster입니다. 서버 수십 대에 작업을 나눠 배치하는 문제입니다.

초록의 첫 두 문장이 동기를 정확히 말합니다.

> "Efficiently scheduling data processing jobs on distributed compute clusters requires complex algorithms. Current systems use simple, generalized heuristics and ignore workload characteristics, since developing and tuning a scheduling policy for each workload is infeasible."

**현재 시스템은 단순하고 일반적인 heuristic을 쓰고 workload의 특성을 무시하는데, 그 이유는 workload마다 정책을 만들고 조율하는 것이 현실적으로 불가능하기 때문**이라는 것입니다.

이 진단이 흥미롭습니다. 앞 권에서 봤듯이 좋은 scheduling은 상황에 따라 다릅니다. 이 논문도 같은 것을 봤습니다. 다만 답이 다릅니다.

### 답

> "In this paper, we show that modern machine learning techniques can generate highly-efficient policies automatically. Decima uses reinforcement learning (RL) and neural networks to learn workload-specific scheduling algorithms without any human instruction beyond a high-level objective, such as minimizing average job completion time."

**workload에 특화된 scheduling 알고리즘을 자동으로 만들어냅니다.** 사람이 주는 것은 "평균 작업 완료 시간을 최소화하라" 같은 고수준 목표 하나뿐입니다.

### 무엇이 어려웠나

초록이 자기가 넘은 장벽을 밝힙니다.

> "However, off-the-shelf RL techniques cannot handle the complexity and scale of the scheduling problem. To build Decima, we had to develop new representations for jobs' dependency graphs, design scalable RL models, and invent RL training methods for dealing with continuous stochastic job arrivals."

기성 강화학습 기법으로는 안 됐고, 작업 의존 관계를 표현하는 새 방법, 규모를 감당하는 모델, 작업이 계속 들어오는 상황을 다루는 학습 방법을 새로 만들어야 했다는 것입니다.

**"작업 의존 관계 그래프"라는 말이 중요합니다.** 데이터 처리 작업은 여러 단계로 나뉘고 단계 사이에 선후 관계가 있습니다. 앞 권에서 본 chain의 일반화된 형태입니다. 이 논문은 그 구조 자체를 모델의 입력으로 표현했습니다.

### 결과

> "Our prototype integration with Spark on a 25-node cluster shows that Decima improves average job completion time by at least 21% over hand-tuned scheduling heuristics, achieving up to 2x improvement during periods of high cluster load."

**최소 21퍼센트 개선, 부하가 높을 때는 최대 두 배**입니다.

여기서 앞 장에서 배운 대로 읽어야 합니다. 비교 대상이 "hand-tuned scheduling heuristics"라고만 되어 있습니다. **어떤 heuristic인지는 초록에 없습니다.** 그리고 workload는 "Spark on a 25-node cluster"라고만 되어 있습니다.

구체적인 비교 대상과 workload는 논문 본문에 있고, 이 권을 쓰면서 확인하지 못했습니다. 그러니 이 결과를 인용할 때는 초록이 말하는 범위까지만 써야 합니다.

## 5.3 FIRM: microservice의 자원 관리

### 인용

- Qiu, H., Banerjee, S. S., Jha, S., Kalbarczyk, Z. T., & Iyer, R. K. (2020). FIRM: An Intelligent Fine-Grained Resource Management Framework for SLO-Oriented Microservices. *Proc. OSDI '20*.

### 문제 설정

웹 서비스가 여러 개의 작은 서비스로 나뉘어 서로 호출하는 구조를 다룹니다. 그중 하나가 느려지면 전체 응답이 느려집니다.

> "multiplexing of compute resources across microservices is still challenging in production because contention for shared resources can cause latency spikes that violate the service-level objectives (SLOs) of user requests."

**공유 자원 경합이 지연 급증을 일으키고, 그것이 사용자 요청의 목표 응답 시간을 위반한다**는 것입니다.

앞 권에서 다룬 tail latency 문제가 분산 환경에서 나타난 형태입니다.

### 무엇을 하는가

> "FIRM leverages online telemetry data and machine-learning methods to adaptively (a) detect/localize microservices that cause SLO violations, (b) identify low-level resources in contention, and (c) take actions to mitigate SLO violations via dynamic reprovisioning."

세 단계입니다. **문제를 일으킨 서비스를 찾아내고, 어떤 자원이 경합 중인지 알아내고, 자원 배분을 조정합니다.**

여기서 눈여겨볼 것은 첫 단계입니다. **"어디가 문제인가"를 먼저 알아내는 구조**입니다. 무작정 전체를 조정하는 것이 아니라 원인을 특정하고 거기에 개입합니다.

### 결과

> "Experiments across four microservice benchmarks demonstrate that FIRM reduces SLO violations by up to 16x while reducing the overall requested CPU limit by up to 62%. Moreover, FIRM improves performance predictability by reducing tail latencies by up to 11x."

목표 위반이 최대 16배 감소, 요청 CPU 한도가 최대 62퍼센트 감소, tail latency가 최대 11배 감소입니다.

여기서도 앞 장의 독법을 적용하면, "four microservice benchmarks"가 무엇인지 초록에 없습니다. 그리고 **"up to"라는 표현이 세 번 반복됩니다.** 최대치를 보고하는 것은 흔한 관행이지만, 평균이 얼마인지는 본문을 봐야 압니다.

## 5.4 Park: 이 갈래를 위한 실험 환경

### 인용

- Mao, H., et al. (2019). Park: An Open Platform for Learning-Augmented Computer Systems. *NeurIPS 32*.

### 왜 이런 것이 필요했나

강화학습을 시스템 문제에 적용하려면 실험 환경이 필요합니다. 그런데 게임과 달리 시스템 문제는 환경을 만드는 것 자체가 큰 일입니다.

> "We present Park, a platform for researchers to experiment with Reinforcement Learning (RL) for computer systems. Using RL for improving the performance of systems has a lot of potential, but is also in many ways very different from, for example, using RL for games."

**시스템에 강화학습을 쓰는 것은 게임에 쓰는 것과 여러 면에서 아주 다르다**는 것이 이 논문의 출발점입니다.

> "Thus, in this work we first discuss the unique challenges RL for systems has, and then propose Park an open extensible platform, which makes it easier for ML researchers to work on systems problems. Currently, Park consists of 12 real world system-centric optimization problems with one common easy to use interface."

열두 개의 실제 시스템 최적화 문제를 하나의 인터페이스로 묶었습니다.

### 열두 개가 무엇인가

논문 초록에는 목록이 없습니다. 저자들의 공개 저장소 문서에 있어서 그쪽에서 옮깁니다. 저장소 문서를 인용하는 것이므로 논문의 표현과 다를 수 있습니다.

적응형 영상 스트리밍, Spark cluster 작업 배치, 데이터베이스 질의 최적화, 네트워크 혼잡 제어, 네트워크 큐 관리, 연산 배치, 회로 설계, 콘텐츠 전송망 캐시, 다차원 데이터베이스 색인, 계정 지역 할당, 서버 부하 분산, 스위치 scheduling입니다.

열두 개가 맞고, 그중 하나가 앞에서 본 cluster 작업 배치입니다.

### 확인하지 못한 부분

> **확인 필요.** 이 논문에서 가장 중요한 부분이 "시스템에 강화학습을 쓰는 것이 왜 어려운가"에 대한 논의인데, 그 부분이 본문에 있고 읽지 못했습니다.
>
> 초록이 그런 논의가 있다고 말하는 것까지만 확인됐습니다. 구체적인 어려움이 무엇이라고 적혀 있는지는 원문을 확인해야 합니다. 이 부분은 이 연구가 왜 학습 기반 접근을 택하지 않았는지를 설명할 때 직접 쓰일 자료라서, 논문을 쓰기 전에 반드시 확인해야 합니다.

## 5.5 이 갈래의 공통 한계

세 논문을 놓고 보면 공통된 성질이 보입니다.

### 재학습이 필요합니다

각 논문이 학습시킨 모델은 그 환경에 맞춰 학습된 것입니다. 다른 cluster, 다른 workload, 다른 하드웨어로 옮기면 다시 학습해야 합니다.

데이터센터에서는 감당할 만합니다. 기계가 수천 대이고 workload가 반복되니 학습 비용을 나눌 수 있습니다.

**데스크톱에서는 사정이 다릅니다.** 사용자마다 쓰는 프로그램이 다르고, 어제 설치한 프로그램이 오늘 처음 돌아갑니다. 각 사용자의 기계에서 학습시킬 수도 없습니다.

### 사람이 이미 형식화한 공간 안에서만 움직입니다

더 근본적인 한계입니다.

강화학습 모델은 사람이 정해준 것 안에서 최적화합니다. 어떤 값을 관측할지, 어떤 행동이 가능한지, 무엇을 보상으로 삼을지를 전부 사람이 먼저 정해야 합니다.

**그러면 그 틀 밖의 정보는 모델에 도달하지 않습니다.**

앞 장에서 본 대비를 다시 봅시다. 사용자가 시작한 학습과 예약된 색인 작업. 관측 항목에 "CPU 사용률"과 "깨어나는 빈도"만 있다면, 모델이 아무리 잘 학습해도 두 상황을 구분하지 못합니다. 구분에 필요한 정보가 관측 항목에 없기 때문입니다.

**즉 이 갈래는 앞 장의 갈래와 같은 한계를 공유합니다.** 방법이 규칙에서 학습으로 바뀌었을 뿐, 읽는 채널은 여전히 행동입니다.

## 5.6 ASA: 골격이 같은 연구

이 갈래에서 이 연구와 가장 비슷한 것이 하나 있습니다. 정확히 알아둬야 합니다.

### 인용

- Wang, X., Jia, S., Huang, Z., Cao, J., & Song, M. (2025). Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies. arXiv:2511.11628.

정식 학회에 실린 논문이 아니라 arXiv에 올라온 원고입니다. 앞에서 정리한 대로, 심사를 거치지 않았다는 것을 전제하고 읽어야 합니다.

### 문제 인식이 같습니다

초록의 첫 문장입니다.

> "Modern operating system schedulers employ a single, static policy, which struggles to deliver optimal performance across the diverse and dynamic workloads of contemporary systems. This "one-policy-fits-all" approach leads to significant compromises in fairness, throughput, and latency"

**하나의 고정된 정책으로는 다양하고 변화하는 workload를 감당할 수 없다**는 것입니다. 앞 권에서 내린 결론과 같습니다.

### 해법의 골격도 같습니다

> "This paper proposes a new paradigm: dynamically selecting the optimal policy from a portfolio of specialized schedulers rather than designing a single, monolithic one. We present the Adaptive Scheduling Agent (ASA), a lightweight framework that intelligently matches workloads to the most suitable "expert" scheduling policy at runtime."

**하나의 정책을 잘 만드는 대신, 여러 전문 정책을 두고 상황에 맞는 것을 고른다**는 것입니다.

이 연구의 골격과 같습니다. 인식한 다음 고르는 구조입니다.

### 어떻게 동작하는가

> "ASA's core is a novel, low-overhead offline/online approach. First, an offline process trains a universal, hardware-agnostic machine learning model to recognize abstract workload patterns from system behaviors. Second, at runtime, ASA continually processes the model's predictions using a time-weighted probability voting algorithm to identify the workload, then makes a scheduling decision by consulting a pre-configured, machine-specific mapping table to switch to the optimal scheduler via Linux's sched_ext framework."

풀어보면 이렇습니다.

**미리 할 일.** 시스템 행동에서 workload 패턴을 알아보는 모델을 학습시킵니다. 이 모델은 하드웨어에 무관하다고 주장합니다.

**실행 중에 할 일.** 모델의 예측을 시간 가중 투표로 모아서 지금 workload가 무엇인지 판정합니다. 그리고 기계별로 미리 만들어둔 대응표를 참조해서, 앞 장에서 본 정책 교체 기능으로 scheduler를 바꿉니다.

투표를 쓰는 이유는 짐작할 수 있습니다. 모델이 매 순간 다른 답을 내면 scheduler가 계속 바뀌어서 오히려 손해입니다. 시간 가중 투표로 그것을 눌러줍니다.

### 결과

> "Our evaluation, based on a novel benchmark focused on user-experience metrics, demonstrates that ASA consistently outperforms the default Linux scheduler (EEVDF), achieving superior results in 86.4% of test scenarios. Furthermore, ASA's selections are near-optimal, ranking among the top three schedulers in 78.6% of all scenarios."

시나리오의 86.4퍼센트에서 기본 scheduler보다 나았고, 78.6퍼센트에서 상위 세 개 안에 드는 선택을 했다는 것입니다.

**여기서 앞 장의 독법이 필요합니다.** 평가에 쓴 것이 "a novel benchmark", 즉 저자들이 새로 만든 벤치마크입니다. 표준 벤치마크가 아닙니다. 그리고 그 벤치마크의 구성이 초록에 없습니다.

자기가 만든 벤치마크로 평가하는 것 자체가 잘못은 아닙니다. 기존 벤치마크가 재려는 것을 못 재는 경우가 실제로 있고, 이 연구도 데이터셋을 직접 만듭니다. 다만 그럴 때는 벤치마크의 설계와 근거를 함께 공개해야 합니다.

### 무엇이 다른가

이 연구와 골격이 같으니 차이를 정확히 말해야 합니다. 그리고 그 차이는 하나입니다.

**인식하는 채널이 다릅니다.**

이쪽은 시스템 행동에서 패턴을 읽습니다. 이 연구는 프로세스의 이름에서 상황을 읽습니다.

그러니까 이쪽은 앞 장에서 정리한 행동 채널의 한계를 그대로 가집니다. 골격이 아무리 같아도, 행동이 동일하고 의도가 다른 상황은 구분하지 못합니다.

### 한 가지 짚어둘 이음매

초록에 흥미로운 대목이 있습니다.

> "This decoupled architecture allows ASA to adapt to new hardware platforms rapidly without expensive retraining of the core recognition model."

새 하드웨어에 적응할 때 인식 모델을 다시 학습시킬 필요가 없다는 주장입니다.

그런데 같은 초록에 이런 표현이 있습니다. **"a pre-configured, machine-specific mapping table"**, 즉 기계별로 미리 만들어둔 대응표입니다.

모델은 기계에 무관하지만 **대응표는 기계별입니다.** 그러면 그 표는 누가 어떻게 만드나요? 측정해서 만든다면 그것도 비용입니다. 손으로 쓴다면 앞 권에서 본 목록 문제가 여기서 반복됩니다.

초록에는 답이 없습니다.

> **논문으로.** 이런 이음매를 찾아내는 것이 related work를 쓰는 실력입니다. "저 연구는 재학습이 필요 없다고 주장하지만, 기계별 대응표를 미리 만들어야 한다고 같은 초록에 적혀 있다"는 지적은 근거가 명확하고 검증 가능합니다.
>
> 다만 논문에 쓸 때는 조심해야 합니다. 본문을 읽으면 그 표를 자동으로 만드는 절차가 있을 수도 있습니다. **본문을 확인하기 전에는 이 지적을 논문에 쓰면 안 됩니다.** 지금은 열린 질문으로 기록해둘 뿐입니다.

> **이 연구에서는.** 저장소의 related work 초고에 이 연구를 어떻게 다룰지가 적혀 있습니다. 골격이 같다는 것을 서론에서 흐리게 말했다가 뒤에서 축소하는 방식은 쓰지 말라고, 심사자들이 그 두 부분을 대조해서 읽는다고 적혀 있습니다. 골격은 같고 채널이 다르다는 것을 처음부터 분명히 말하는 쪽입니다.

---

## 5장 정리

- 이 갈래는 scheduling 규칙을 사람이 쓰지 말고 기계가 배우게 하자는 발상입니다. 이 장의 논문들은 초록만 확인했고 본문은 읽지 못해, 본문에만 있는 정보는 적지 않았습니다.
- Decima는 데이터 처리 cluster의 작업 배치를 강화학습으로 배웁니다. 현재 시스템이 단순한 heuristic을 쓰고 workload 특성을 무시하는 이유가 workload마다 정책을 만드는 것이 불가능하기 때문이라고 진단합니다. 작업 의존 관계 그래프를 모델 입력으로 표현한 것이 기술적 기여이고, 최소 21퍼센트에서 최대 두 배 개선을 보고합니다.
- FIRM은 microservice 환경에서 목표 응답 시간 위반을 다룹니다. 원인 서비스를 찾아내고, 경합 자원을 특정하고, 자원 배분을 조정하는 세 단계 구조입니다.
- Park은 이 갈래를 위한 실험 환경으로 열두 개의 시스템 최적화 문제를 하나의 인터페이스로 묶었습니다. 시스템에 강화학습을 쓰는 것이 왜 어려운지에 대한 논의가 이 논문의 핵심인데, 그 부분은 본문에 있어 확인하지 못했습니다.
- 이 갈래의 공통 한계는 둘입니다. 환경이 바뀌면 재학습이 필요하다는 것, 그리고 사람이 미리 정해준 관측 항목과 행동 공간 안에서만 움직인다는 것입니다.
- 두 번째 한계 때문에 이 갈래도 행동 채널의 한계를 그대로 가집니다. 방법이 규칙에서 학습으로 바뀌었을 뿐 읽는 채널이 같습니다.
- ASA는 이 연구와 골격이 같습니다. 하나의 정책 대신 여러 전문 정책을 두고 상황에 맞는 것을 고르며, 정책 교체 기능으로 실제로 바꿉니다. 차이는 인식 채널 하나입니다. 이쪽은 시스템 행동을 읽고 이 연구는 프로세스 이름을 읽습니다.
- ASA의 초록에는 확인해볼 이음매가 있습니다. 인식 모델은 하드웨어에 무관하다면서, 기계별로 미리 만들어둔 대응표를 참조한다고 적혀 있습니다. 그 표를 누가 어떻게 만드는지는 초록에 없습니다. 본문을 확인하기 전에는 논문에 쓸 수 없는 지적입니다.

---

# 6장 · LLM을 kernel policy에 쓰는 시도들

## 6.1 이 갈래가 하는 일

앞의 두 갈래는 행동을 읽었습니다. 규칙으로 읽거나 학습된 모델로 읽거나.

이 갈래는 다른 채널을 씁니다. **언어 모델의 지식을 kernel 정책에 끌어옵니다.**

최근 몇 년 사이에 생긴 흐름이고, 이 연구와 가장 가깝습니다. 그래서 이 장이 이 권에서 가장 중요합니다. 논문 심사자가 가장 먼저 찌를 자리이기도 합니다.

> **확인 필요, 그리고 어떻게 해결했는지.** 이 장의 논문들도 출판사 사이트와 논문 저장소에 접근할 수 없었습니다.
>
> 다만 이 장의 자료는 상태가 좋습니다. 저자들이 논문의 **원고 소스를 공개 저장소에 올려두었기 때문에**, 그 원고 파일을 직접 읽을 수 있었습니다. 초록도 논문 저장소가 배포하는 공식 요약 자료를 통해 확인했습니다.
>
> 그래도 최종 PDF를 눈으로 본 것은 아닙니다. 인용문마다 어디서 읽었는지를 적어둡니다.

## 6.2 SchedCP: 가장 가까운 선행 연구

### 인용

- Zheng, Y., Hu, Y., Zhang, W., & Quinn, A. (2025). Towards Agentic OS: An LLM Agent Framework for Linux Schedulers. arXiv:2509.01245. ML for Systems @ NeurIPS 2025.

이 연구를 정확히 아는 것이 중요합니다. 문제 인식이 거의 같기 때문입니다.

### 판본에 대한 주의

이 논문은 arXiv에 여러 판본이 올라와 있습니다. 확인한 바로는 네 번째 판본까지 나왔고, 세 번째와 네 번째 판본에 학회 정보가 붙어 있습니다.

흥미로운 것은 판본마다 길이가 다르다는 점입니다. 두 번째 판본은 정식 학회 형식의 긴 원고이고, 최신 판본은 workshop 형식의 짧은 원고입니다. 길게 썼다가 다시 짧은 형태로 돌아온 것입니다.

**그러니 "이 논문에 무엇이 적혀 있다"고 말할 때 어느 판본인지를 밝혀야 합니다.** 긴 원고에만 있는 내용을 짧은 판본을 인용하며 쓰면 안 됩니다.

### 문제 인식

초록의 첫 문장입니다.

> "Operating system schedulers suffer from a fundamental semantic gap, where kernel policies fail to understand application-specific needs, leading to suboptimal performance."

**kernel 정책이 응용의 필요를 이해하지 못하는 근본적인 semantic gap이 있다**는 것입니다.

긴 원고의 서론은 더 구체적입니다.

> "Operating system schedulers face a fundamental challenge: kernel policies cannot understand what applications need. This semantic gap leads to suboptimal performance across modern computing infrastructure. In cloud platforms, system administrators who manage schedulers are not the developers who understand application behavior."

**scheduler를 관리하는 사람과 응용의 동작을 아는 사람이 다르다**는 지적이 붙어 있습니다.

이 진단은 앞 권에서 도달한 결론과 사실상 같습니다. 용어까지 같습니다.

### 구조

핵심 발상을 초록이 이렇게 말합니다.

> "Our core insight is that the challenge is not merely to apply a better LLM, but to architect a decoupled control plane that separates the AI's role of semantic reasoning ("what to optimize") from the system's role of execution ("how to observe and act")"

**더 좋은 언어 모델을 쓰는 것이 문제가 아니라, 의미 추론과 실행을 분리하는 제어 계층을 설계하는 것이 문제**라는 것입니다.

무엇을 최적화할지는 인공지능의 몫이고, 어떻게 관찰하고 행동할지는 시스템의 몫입니다.

**이 분리가 이 연구와 같은 발상입니다.** 앞 권에서 언어 모델을 scheduler 안에 넣을 수 없다는 물리적 제약을 봤고, 그래서 바깥에 두고 설정만 바꾼다고 했습니다. 같은 결론입니다.

원고는 이 계층을 이렇게 부릅니다.

> "SchedCP is a secure control plane acting as an 'API for OS optimization,' separating systems infrastructure from AI logic, distinguishing "what to optimize" (AI's domain) from "how to observe and act" (system's domain)."

### 세 가지 구성 요소

초록이 세 가지를 나열합니다.

> "SchedCP provides a stable interface with three key services: a Workload Analysis Engine, an evolving Scheduler Policy Repository, and an Execution Verifier that validates all AI-generated code and configure before deployment with static and dynamic analysis."

하나씩 봅니다.

**Workload Analysis Engine.** 시스템 성능 데이터에 대한 접근을 세 단계로 제공합니다. 원고의 설명입니다.

> "Provides tiered access to system performance data: (1) cost-effective API endpoints with pre-processed summaries (CPU load, memory usage), (2) secure sandbox access to file reading, application building, Linux profiling tools (`perf`, `top`) and dynamically attachable eBPF probes, (3) feedback channel reporting post-deployment metrics (percentage change in throughput/latency)."

**단계가 있다는 것이 중요합니다.** 값싼 요약부터 시작해서, 필요하면 격리된 환경에서 파일을 읽고 프로파일러를 돌리고 커널 탐침을 붙일 수 있습니다.

이 접근 범위를 기억해두세요. 뒤에서 이 연구와 비교할 때 결정적인 차이가 됩니다.

**Scheduler Policy Repository.** 실행 가능한 scheduler 프로그램들을 설명과 함께 저장해둔 데이터베이스입니다.

> "Database storing executable eBPF scheduler programs with metadata (natural language descriptions, target workloads, historical performance metrics). It provides APIs for semantic search and retrieval"

**Execution Verifier.** 인공지능이 만든 코드를 배포 전에 검증합니다.

> "includes a multi-stage validation pipeline: (1) kernel's eBPF verifier ensures memory safety and termination, (2) scheduler-specific static analysis detects logic flaws (starvation, unfairness) the standard verifier misses, (3) dynamic validation in secure micro-VM tests correctness and performance."

앞 장에서 kernel의 BPF 검사기가 무엇을 보장하는지 확인했습니다. 메모리 안전과 종료입니다. **이 연구는 그것만으로 부족하다고 보고 두 겹을 더 얹었습니다.** 표준 검사기가 놓치는 starvation과 불공정을 잡는 정적 분석, 그리고 격리된 가상 기계에서의 실제 실행입니다.

앞 권에서 배운 starvation 개념이 여기서 검증 항목으로 등장합니다.

### 실제로 일을 하는 부분

제어 계층 위에 올라가는 것이 여러 개의 에이전트입니다.

> "sched-agent is the first autonomous multi-agent system that decomposes scheduler optimization into four specialized agents (Observation, Planning, Execution, Learning)"

관찰, 계획, 실행, 학습 넷입니다. 각자의 역할을 원고가 설명합니다.

**관찰 에이전트**는 workload의 특성을 파악해서 요약을 만듭니다. 원고가 실제 예를 듭니다.

> "For kernel compilation, it produces profiles like ``CPU-intensive parallel compilation with short-lived processes, inter-process dependencies, targeting makespan minimization.''"

커널 빌드를 보고 "짧게 사는 프로세스가 많고 프로세스 간 의존이 있는 CPU 집약 병렬 컴파일이며 전체 완료 시간 최소화가 목표"라는 요약을 만든다는 것입니다.

**계획 에이전트**는 그 요약을 최적화 전략으로 바꿉니다. 우선순위가 정해져 있습니다.

> "For existing production-ready scheduler solutions with strong performance history, it configures parameters. For partial matches, it retrieves code and generates patches. When no suitable base exists, it composes new schedulers from algorithm primitives."

**기존 scheduler의 설정을 바꾸는 것이 1순위, 코드를 부분 수정하는 것이 2순위, 새로 만드는 것이 마지막**입니다.

**실행 에이전트**가 코드를 만들어 검증기에 넘기고, **학습 에이전트**가 결과를 분석해서 저장소를 갱신합니다.

### 결과

원고의 평가 부분에서 옮깁니다.

**커널 빌드.**

> "The workload shows 1.63x speedup from 13.57s to 8.31s using scx_rusty as the first attempt. After 3 iterations of observe-optimization process, the sched-agent selects the scx_layered scheduler and adds 16% additional gain beyond LLM configuration, with total improvements of 1.79x over baseline EEVDF."

여기서 정확히 읽어야 할 것이 있습니다. **1.79배라는 숫자는 세 번의 반복을 거친 뒤의 결과이고, 새로 만든 코드가 아니라 기존 scheduler를 고른 결과입니다.** 첫 시도는 1.63배였습니다.

원고가 덧붙인 문장도 의미가 있습니다.

> "In contrast, basic RL approaches show no improvement in our tests, likely because they require hardware or workload-specific retraining, which is costly and time-consuming."

앞 장에서 정리한 학습 기반 접근의 한계를 이 논문도 같은 이유로 지적하고 있습니다.

**응답 시간 측정 도구.**

> "While AI configured scheduler initially underperformed with 13% worse P99 latency (46.1ms vs 40.3ms) and 19% lower throughput (741 vs 910 req/s), AI iterative refinement identified scx_rusty as superior. After three iterations, scx_rusty achieved 2.11× better P99 latency (19.1ms) and 1.60× higher throughput (1452 req/s) versus EEVDF"

**첫 시도가 기본값보다 나빴다는 것을 그대로 적었습니다.** 정직한 보고입니다.

**배치 작업.** 여기가 유일하게 새 코드를 만든 사례입니다.

> "8 diverse batch workloads (e.g. file compression, video transcoding, software testing, and data analytics tasks) running on machine 2. To simulate a long-tail distribution, each workload comprised 40 parallel tasks: 39 short and one significantly longer... The agent consistently identified this pattern and generated custom eBPF code implementing a Longest Job First (LJF) scheduling policy—a scheduler not present in our repository—achieving an average 20% reduction in end-to-end processing time."

짧은 작업 39개와 긴 작업 1개라는 구조를 알아보고, 저장소에 없던 정책을 직접 만들어냈다는 것입니다.

### 비용

이 연구가 비용을 정직하게 보고한다는 점이 좋습니다.

> "The cost for this analysis averaged \$0.15 per workload"

> "In addition to performance gains, our framework's optimizations reduced generation costs per iteration: time fell from 33 to 2.5 minutes (a 13x reduction), and the monetary cost dropped from \$6 to \$0.5."

그리고 최적화 전의 상태를 이렇게 적습니다.

> "The successful generation required 33 minutes, 221 LLM API calls, and 15+ iterations, costing \$6 (vs. 5 minutes typically for an expert developer)."

**33분에 221번의 호출, 15회 이상의 반복, 6달러.** 전문 개발자가 5분이면 하는 일에 대해서입니다. 이 대비를 논문에 스스로 적어둔 것이 인상적입니다.

### hot path에 대한 입장

앞 권에서 언어 모델을 결정 경로에 둘 수 없다는 물리적 제약을 봤습니다. 이 논문도 같은 입장입니다.

> "(4) operating in the control plane to generate optimized code that runs natively with negligible runtime overhead, unlike traditional ML models that would cause unacceptable inference latency in the scheduler hot path. This control plane separation represents a key architectural insight: LLMs generate and optimize scheduling policies offline, producing native eBPF code that executes without any ML inference overhead during actual scheduling decisions."

> "Deployed on the production-ready sched_ext infrastructure, our approach executes with zero LLM overhead in the critical path"

**다만 이 주장을 뒷받침하는 측정값은 없습니다.** 구조적으로 그렇다는 것이지, 추론 지연을 재서 보인 것이 아닙니다. 언어 모델이 제어 계층에 있고 실행 시점에는 컴파일된 코드만 돌기 때문에 논리적으로 맞는 주장이지만, 숫자는 없습니다.

### 무엇을 평가했는가

이 부분이 이 연구와의 차이에서 가장 중요합니다.

원고에 적힌 연구 질문 넷입니다.

> "• RQ1: Can SchedCP effectively configure existing schedulers? • RQ2: Can SchedCP generate new schedulers for specific workloads? • RQ3: What is the cost and efficiency of SchedCP's scheduler generation? • RQ4: How much can sched-agent continue to improve performance after initial attempt?"

**넷 다 최종 성능과 비용에 대한 질문입니다.** 기존 scheduler를 잘 설정하는가, 새 것을 만들 수 있는가, 비용은 얼마인가, 반복하면 더 나아지는가.

**언어 모델이 workload를 얼마나 정확히 이해했는가를 따로 재는 질문이 없습니다.**

그리고 흥미로운 흔적이 있습니다. 저자들이 공개한 원고 소스에, 주석 처리되어 제출본에서 빠진 다섯 번째 질문이 남아 있습니다.

> "How effectively can SchedCP understand workloads?"

**이 질문을 넣으려다 뺐다는 뜻입니다.** 왜 뺐는지는 알 수 없습니다. 분량 때문일 수도 있고, 측정 방법을 정하지 못해서일 수도 있습니다.

인식에 관한 서술은 배치 작업 실험 안에 한 문장으로만 나옵니다.

> "We note that the powerful Claude Opus agent successfully classified all 8 workloads, whereas the smaller Claude Sonnet model could not."

큰 모델은 여덟 개를 다 분류했고 작은 모델은 못 했다는 것입니다. **정확도 표도, 정답 라벨을 만든 절차도, 별도의 인식 평가도 없습니다.**

저자들도 평가가 예비 단계임을 밝힙니다.

> "All experiments successfully created working custom scheduler configurations or eBPF programs. Future evaluation requires a complete benchmark."

### 이 연구와 무엇이 다른가

문제 인식이 같고 구조도 비슷한데, 세 가지가 다릅니다. 논문에서 이 세 가지를 정확히 말해야 합니다.

**첫째, 출력이 다릅니다.**

저쪽이 만들어내는 것은 **정책**입니다. workload마다 scheduler 코드를 고르거나, 고치거나, 새로 만듭니다.

이 연구가 만들어내는 것은 **신호**입니다. 상황을 나타내는 작은 고정 어휘 하나입니다. 정책은 미리 정해진 표 안에 있고 언어 모델은 그 표를 건드리지 않습니다.

차이가 왜 중요한가. 저쪽 방식에서는 언어 모델이 만든 코드가 실제로 시스템을 제어합니다. 그래서 세 겹의 검증기가 필요합니다. 이 연구에서는 언어 모델의 출력이 정해진 어휘 중 하나이고, 그것이 미리 검토된 설정으로 번역됩니다. 모델이 이상한 답을 내도 어휘 밖으로 나갈 수 없습니다.

**둘째, 대상이 다릅니다.**

저쪽은 서버와 배치 작업을 다룹니다. 커널 빌드, 응답 시간 측정 도구, 파일 압축과 영상 변환입니다. 이런 것들은 **최적화할 대상이 명확한 하나의 작업**입니다.

데스크톱은 다릅니다. 최적화할 작업 하나가 있는 것이 아니라 **상황이 계속 흘러갑니다.** 같은 기계가 저녁 여덟 시에는 게임기이고 아홉 시에는 빌드 서버입니다.

저쪽 구조는 시간을 들여 workload를 분석하고 정책을 만드는 것을 전제합니다. 33분과 6달러가 그 전제 위에서 합리적입니다. 상황이 몇 분마다 바뀌는 환경에는 맞지 않습니다.

**셋째, 무엇을 재는지가 다릅니다.**

이게 가장 실질적인 차이입니다.

저쪽은 최종 성능만 잽니다. 앞에서 본 대로입니다.

이 연구는 **인식 자체를 따로 잽니다.** 언어 모델이 내놓은 상황 판단을 정답 라벨과 대조해서 채점합니다. 정확도, 반복 실행 시의 일관성, 방해 요소가 섞였을 때의 견고함을 따로 봅니다.

왜 이게 중요한가. 최종 성능만 보면 **왜 좋았는지 또는 왜 나빴는지를 알 수 없습니다.** 성능이 안 나왔을 때 인식이 틀린 것인지, 인식은 맞았는데 그 인식을 설정으로 옮기는 표가 나쁜 것인지, 아니면 애초에 그 상황에서는 설정을 바꿔봤자 차이가 없는 것인지 구분되지 않습니다.

앞 권에서 본 것처럼, 이 연구의 주장은 여러 개의 고리로 되어 있고 각 고리가 독립적으로 실패할 수 있습니다. 고리별로 재지 않으면 어디가 끊어졌는지 알 수 없습니다.

> **논문으로.** 이 세 가지 차이가 논문에서 이 연구를 방어하는 핵심입니다. 심사자가 "이건 그 연구의 데스크톱 판 아닌가"라고 물을 것이고, 답은 출력 계약과 측정 계층입니다.
>
> 그리고 두 번째 방어가 더 강합니다. 인식을 따로 재는 것은 저쪽 평가에 대응물이 없습니다. 저자들이 그 질문을 넣으려다 뺀 흔적까지 있으니, 그 자리가 비어 있다는 것은 확인된 사실입니다.
>
> 다만 이 지적을 논문에 쓸 때는 조심해야 합니다. 주석 처리된 연구 질문을 근거로 드는 것은 공격적으로 읽힐 수 있습니다. 안전한 서술은 "그 연구의 평가는 최종 성능만 다룬다"까지이고, 그건 제출된 원고만으로도 확인됩니다.

## 6.3 Kgent: 자연어에서 kernel 확장 만들기

### 인용

- Zheng, Y., Yang, Y., Chen, M., & Quinn, A. (2024). Kgent: Kernel Extensions Large Language Model Agent. *Proc. SIGCOMM 2024 Workshop on eBPF and Kernel Extensions (eBPF '24)*, 30–36. DOI 10.1145/3672197.3673434.

앞 연구와 저자가 겹칩니다. 시기적으로 먼저이고, scheduler가 아니라 kernel 확장 일반을 다룹니다.

### 문제

> "The extended Berkeley Packet Filters (eBPF) ecosystem allows for the extension of Linux and Windows kernels, but writing eBPF programs is challenging due to the required knowledge of OS internals and programming limitations enforced by the eBPF verifier. These limitations ensure that only expert kernel developers can extend their kernels, making it difficult for junior sys admins, patch makers, and DevOps personnel to maintain extensions."

**kernel을 확장할 수 있는 사람이 전문가로 제한된다**는 것이 문제입니다.

### 해법

> "This paper presents Kgent, an alternative framework that alleviates the difficulty of writing an eBPF program by allowing Kernel Extensions to be written in Natural language. Kgent uses recent advances in large language models (LLMs) to synthesize an eBPF program given a user's English language prompt."

영어 문장을 주면 eBPF 프로그램을 만들어줍니다.

### 어떻게 믿을 수 있게 하는가

여기가 이 논문의 기여입니다.

> "To ensure that LLM's output is semantically equivalent to the user's prompt, Kgent employs a combination of LLM-empowered program comprehension, symbolic execution, and a series of feedback loops. Kgent's key novelty is the combination of these techniques."

**만들어낸 코드가 사용자의 요청과 의미적으로 같은지를 확인합니다.** 언어 모델로 프로그램을 이해하게 하고, 기호 실행으로 검증하고, 틀리면 되돌려서 다시 만듭니다.

### 결과

> "We show that Kgent produces correct eBPF programs on 80%—which is an improvement of a factor of 2.67 compared to GPT-4 program synthesis baseline."

80퍼센트가 맞았고, 직접 생성 대비 2.67배 개선입니다.

> "Moreover, we find that Kgent very rarely synthesizes "false positive" eBPF programs—i.e., eBPF programs that Kgent verifies as correct but manual inspection reveals to be semantically incorrect for the input prompt."

검증기가 맞다고 했는데 실제로는 틀린 경우가 아주 드물다는 것입니다. **다만 초록에 그 비율의 숫자는 없습니다.**

> **이 연구에서는.** 이 논문이 다루는 문제는 이 연구와 다르지만, 한 가지 발상이 공통됩니다. **언어 모델의 출력을 그대로 믿지 않고 검증기를 통과시킨다**는 것입니다.
>
> 이 연구에도 검증기가 있습니다. 언어 모델이 내놓은 설정이 허용된 어휘와 값 범위 안에 있는지 확인하고, 벗어나면 거부하거나 범위 안으로 끌어당깁니다. 앞의 연구처럼 코드를 검증하는 것이 아니라 값을 검증하는 것이라 훨씬 단순합니다. 출력이 코드가 아니라 신호이기 때문에 가능한 단순함입니다.

## 6.4 인접한 두 시도

### kernel 설정 조율

- Lin, H., Li, Y., Luo, H., Lin, Z., Zhang, L., Xing, M., & Wu, Y. (2025). TuneAgent: Agentic Operating System Kernel Tuning with Reinforcement Learning. arXiv:2508.12551.

kernel의 설정 항목을 언어 모델과 강화학습으로 조율합니다.

> "Linux kernel tuning is essential for optimizing operating system (OS) performance, yet remains challenging due to the complex kernel space, sparse performance feedback, and strong workload sensitivity."

**설정 공간이 복잡하고, 성능 신호가 드물게 오고, workload에 민감하다**는 것이 어려움입니다.

> "TuneAgent formulates the kernel space as a constrained RL environment, enabling large language models (LLMs) to autonomously explore the kernel while enforcing valid and precise configuration modifications."

결과는 최대 5.6퍼센트 개선입니다.

> **확인 필요, 그리고 인용 정보 정정.** 이 논문에 대해 확인 과정에서 두 가지를 발견했습니다.
>
> **첫째, 제목이 바뀌었습니다.** 첫 판본의 제목은 다른 이름이었고, 저자 목록도 한 명이 다릅니다. 지금 제목과 저자 구성은 두 번째 판본의 것입니다.
>
> **둘째, 저자들의 공개 저장소가 특정 학회 게재를 언급하고 있습니다.** 이 연구 저장소의 인용 기록에는 게재 학회가 없다고 적혀 있는데, 그 사이에 상황이 바뀌었을 수 있습니다.
>
> 두 가지 모두 논문에 인용하기 전에 확인해야 합니다. 앞에서 정리한 대로, arXiv 논문은 판본과 게재 여부를 다시 확인하는 것이 원칙입니다. 이 사례가 그 원칙이 왜 필요한지를 보여줍니다.

### 고성능 컴퓨팅 작업 배치

- Jadhav, P., Jin, H., Deelman, E., & Balaprakash, P. (2025). Evaluating the Efficacy of LLM-Based Reasoning for Multiobjective HPC Job Scheduling. arXiv:2506.02025.

이쪽은 접근이 다릅니다. **언어 모델이 scheduler 자체입니다.**

> "we propose a novel Large Language Model (LLM)-based scheduler using a ReAct-style framework (Reason + Act), enabling iterative, interpretable decision-making. The system incorporates a scratchpad memory to track scheduling history and refine decisions via natural language feedback, while a constraint enforcement module ensures feasibility and safety."

추론하고 행동하는 것을 번갈아 하면서 배치 결정을 직접 내립니다. 제약 조건을 강제하는 별도 모듈이 안전을 담당합니다.

결과에 대한 서술이 정직합니다.

> "The method excels in constraint satisfaction and adapts to diverse workloads without domain-specific training. However, a trade-off between reasoning quality and computational overhead challenges real-time deployment."

제약 만족은 잘하고 별도 학습 없이 다양한 workload에 적응하지만, **추론 품질과 계산 비용 사이의 상충 때문에 실시간 배치가 어렵다**는 것입니다.

**이 한 문장이 이 갈래 전체의 경계를 보여줍니다.** 언어 모델을 결정 경로에 직접 두면 품질은 얻지만 속도를 잃습니다. 앞 권에서 본 물리적 제약이 여기서 실험으로 확인된 셈입니다.

> **이 연구에서는.** 이 논문과의 대비가 이 연구의 구조를 설명하는 데 유용합니다. 저쪽은 언어 모델이 매 결정을 내리고, 이 연구는 언어 모델이 훨씬 느린 주기로 상황 판단만 내놓습니다. 그래서 저쪽은 실시간 배치가 어렵다는 결론에 도달하고, 이 연구는 그 문제를 구조로 피해 갑니다.

## 6.5 이 갈래 전체를 놓고 보면

네 연구를 나란히 놓으면 언어 모델을 어디에 두느냐가 갈립니다.

| 연구 | 언어 모델의 위치 | 출력 | hot path에 있나 |
|---|---|---|---|
| SchedCP | 제어 계층 | scheduler 코드 또는 설정 | 없음 |
| Kgent | 개발 도구 | kernel 확장 코드 | 없음 |
| TuneAgent | 조율 과정 | kernel 설정값 | 없음 |
| HPC 작업 배치 | 결정 경로 | 배치 결정 자체 | 있음 |
| **이 연구** | **제어 계층** | **상황 신호** | **없음** |

넷 중 셋이 언어 모델을 결정 경로 밖에 둡니다. 그리고 안에 둔 하나는 실시간 배치가 어렵다는 결론에 도달했습니다.

**이 연구도 밖에 둡니다.** 다만 출력이 코드도 설정값도 아니라 상황을 나타내는 신호라는 점이 다릅니다.

---

## 6장 정리

- 이 갈래는 언어 모델의 지식을 kernel 정책에 끌어옵니다. 이 연구와 가장 가까우므로 정확히 알아야 합니다. 이 장의 인용문은 저자들이 공개한 원고 소스에서 읽었고, 최종 PDF를 본 것은 아닙니다.
- SchedCP가 가장 가까운 선행 연구입니다. 문제 인식이 거의 같습니다. kernel 정책이 응용의 필요를 이해하지 못하는 semantic gap이 있고, 그 해법은 더 좋은 모델이 아니라 의미 추론과 실행을 분리하는 제어 계층이라는 것입니다.
- 구성 요소가 셋입니다. 단계별 접근을 제공하는 workload 분석 엔진, scheduler 프로그램 저장소, 그리고 인공지능이 만든 코드를 세 겹으로 검증하는 검증기입니다. kernel의 BPF 검사기만으로 부족하다고 보고 starvation과 불공정을 잡는 정적 분석을 얹은 점이 눈에 띕니다.
- 결과는 커널 빌드에서 반복 세 번 뒤 1.79배, 응답 시간 측정 도구에서 P99 2.11배 개선입니다. 첫 시도가 기본값보다 나빴던 사례도 그대로 보고합니다. 새 코드를 만든 것은 배치 작업 실험 하나이고, 거기서 20퍼센트 개선입니다.
- 비용을 정직하게 보고합니다. 최적화 전에는 33분과 221번의 호출과 6달러가 들었고, 전문 개발자가 5분이면 하는 일이라고 스스로 적었습니다.
- 평가의 연구 질문 넷이 모두 최종 성능과 비용에 관한 것입니다. 언어 모델이 workload를 얼마나 정확히 이해했는가를 따로 재는 질문은 없습니다. 공개된 원고 소스에 그런 질문이 주석 처리된 채 남아 있습니다.
- 이 연구와의 차이는 셋입니다. 출력이 정책이 아니라 신호라는 것, 대상이 서버 작업이 아니라 흘러가는 데스크톱 상황이라는 것, 그리고 인식 자체를 따로 잰다는 것입니다. 마지막이 가장 실질적입니다. 최종 성능만 보면 어느 고리가 끊어졌는지 알 수 없기 때문입니다.
- Kgent는 자연어로 kernel 확장을 쓰게 합니다. 언어 모델의 출력을 그대로 믿지 않고 검증기를 통과시킨다는 발상이 이 연구와 공통됩니다.
- kernel 설정을 조율하는 연구가 있고, 확인 과정에서 제목과 저자와 게재 상태가 바뀐 것을 발견했습니다. arXiv 인용을 다시 확인해야 하는 이유의 실제 사례입니다.
- 고성능 컴퓨팅 작업 배치 연구는 언어 모델을 결정 경로에 직접 둡니다. 그 결과 추론 품질과 계산 비용 사이의 상충 때문에 실시간 배치가 어렵다는 결론에 도달했습니다. 이 갈래 전체의 경계를 보여주는 결과입니다.

---

# 7장 · 이미 배포되어 있는 semantic recognition

## 7.1 이 장이 다루는 것

지금까지 본 세 갈래는 전부 연구입니다. 논문이 있고 실험이 있습니다.

이 장에서 다루는 것은 연구가 아닙니다. **지금 수백만 대의 컴퓨터에서 실제로 돌고 있는 소프트웨어입니다.**

그리고 그 소프트웨어들이 하는 일이 이 연구가 하려는 일과 같습니다. **프로그램의 이름을 보고 상황을 판단해서 시스템 설정을 바꿉니다.**

다만 판단하는 방법이 다릅니다. 사람이 미리 표에 적어뒀습니다.

**그래서 이 장의 대상이 이 연구의 진짜 비교 상대입니다.** 기본 scheduler가 아니라 이쪽입니다.

## 7.2 Windows의 게임 모드

### 확인할 수 있었던 것

> **확인 필요.** 제조사의 공식 문서 사이트에 접근할 수 없었습니다. 대신 그 문서가 생성되는 **공개 원본 저장소**에서 일부를 읽었습니다. 개념 설명 페이지는 그 저장소에 없고 보관용 사이트에만 있어서 읽지 못했습니다.
>
> 특히 **게임인지 아닌지를 어떻게 판별하는지는 확인하지 못했습니다.** 읽을 수 있었던 어느 문서에도 그 방법이 적혀 있지 않습니다. 목록 방식인지, 개발자 등록인지, 다른 방법인지 이 권의 근거만으로는 말할 수 없습니다.
>
> 배경 작업 억제, 업데이트 연기, 알림 보류에 대해서도 확인된 문서가 없습니다.

읽을 수 있었던 것은 두 종류입니다.

**게임 개발 안내 문서의 한 문장.**

> "Improve performance by getting exclusive or priority access to hardware resources using Game Mode APIs"

**하드웨어 자원에 대한 독점적 또는 우선적 접근**을 얻는다는 것입니다.

**개발자용 함수 문서 두 개.**

첫 번째 함수는 현재 상태를 알려줍니다.

> "Gets the current resource state (that is, whether the app is running in Game Mode or shared mode)."

> "This function should be called during each iteration of the game loop to check when the app enters and exits Game Mode so that the appropriate settings can be applied."

**게임 루프를 돌 때마다 확인하라**고 되어 있습니다. 상태가 실행 중에 바뀔 수 있다는 뜻입니다.

그리고 조건이 붙습니다.

> "The app must be in the foreground and have focus before exclusive resources are granted."

**전면에 있고 초점을 가지고 있어야** 독점 자원을 받습니다.

두 번째 함수는 받을 수 있는 자원의 양을 알려줍니다.

> "Gets the expected number of exclusive CPU sets that are available to the app when in Game Mode."

> "This function returns 0 if no exclusive CPU sets are available, or if the customer opted out of Game Mode via the Settings in Windows 10."

### 여기서 읽을 수 있는 것

확인된 범위 안에서도 몇 가지가 보입니다.

**자원 모델이 구체적입니다.** 막연한 우선순위 상향이 아니라 **독점적인 CPU 집합**입니다. 특정 core를 이 응용에만 배정한다는 뜻입니다.

**전면과 초점이 조건입니다.** 앞 권에서 Windows가 전면 창을 우대한다고 했는데, 게임 모드에서도 같은 조건이 붙습니다. 시스템이 "사용자가 지금 이걸 보고 있다"는 정보를 알고 있고 그걸 씁니다.

**사용자가 끌 수 있습니다.** 설정에서 끄면 함수가 0을 돌려줍니다.

> **논문으로.** 확인 범위를 넘지 않는 것이 중요합니다. 게임 모드가 게임 목록을 쓴다는 것은 널리 알려진 이야기이지만, 이 권에서 그것을 제조사 문서로 확인하지 못했습니다.
>
> 그러니 논문에서 이 시스템을 다룰 때 두 가지 선택지가 있습니다. 제조사 문서를 확보해서 확인된 내용만 쓰거나, 아니면 다음 절에서 다룰 공개 소프트웨어를 주된 예로 삼고 이쪽은 존재만 언급하는 것입니다. 저장소의 related work 초고는 뒤쪽을 택했습니다. 이쪽은 닫힌 소프트웨어라서 검증이 안 되고, 공개 소프트웨어 쪽은 카탈로그가 그대로 공개되어 있어 재현 가능하기 때문입니다.

## 7.3 Linux의 우선순위 조정 데몬

이쪽은 전부 공개되어 있습니다. 코드도, 규칙 카탈로그도, 그 카탈로그의 변경 이력도 볼 수 있습니다.

### 무엇을 하는 프로그램인가

원래 프로젝트의 자기 설명입니다.

> "Ananicy (ANother Auto NICe daemon) — is a shell daemon created to manage processes' IO and CPU priorities, with community-driven set of rules for popular applications (anyone may add their own rule via github's pull request mechanism). It's mainly for desktop usage."

**프로세스의 입출력과 CPU 우선순위를 관리하는 데몬**이고, **인기 있는 응용에 대한 규칙을 커뮤니티가 함께 만든다**는 것입니다. 누구나 규칙을 추가할 수 있습니다. 데스크톱용입니다.

앞 권에서 우선순위를 누가 정하느냐가 근본 문제라고 했습니다. 이 프로그램의 답은 이렇습니다. **사용자도 프로그램도 아니고, 커뮤니티가 미리 정해둔다.**

### 규칙 하나가 어떻게 생겼나

문서의 예시입니다.

```json
{ "name": "gcc", "type": "Heavy_CPU", "nice": 19, "ioclass": "best-effort", "ionice": 7, "cgroup": "cpu90" }
```

문서가 설명을 붙입니다.

> "All fields except `name` are optional."

> "`name` used for match processes by exec bin name"

**실행 파일 이름으로 프로세스를 찾습니다.** 그게 전부입니다. 이름을 보고 표를 뒤져서 설정을 적용합니다.

이름만으로 부족한 경우를 위한 장치도 있습니다.

```json
{ "name": "java", "cmdlines": ["freenet.node.NodeStarter"], "type": "service" }
```

> "This translates to: apply the rule to any process named `java`, that received `freenet.node.NodeStarter` as a command line argument."

이름이 같아도 실행 인자가 다르면 다른 프로그램일 수 있습니다. 그래서 인자까지 봅니다.

**이게 앞 권에서 말한 이름 기반 인식의 실제 구현입니다.** 그리고 명령줄 인자까지 본다는 점이 흥미롭습니다. 이 연구가 언어 모델에게 보여주는 것도 프로세스 이름과 명령줄입니다.

### 설정할 수 있는 것들

C++로 다시 만든 판본의 문서에 전체 목록이 있습니다.

| 항목 | 무엇을 정하나 |
|---|---|
| `nice` | CPU 우선순위, -20에서 19 |
| `latency_nice` | 지연 민감도 힌트, 별도 kernel 패치 필요 |
| `sched` | scheduling policy 자체를 지정 |
| `rtprio` | real-time policy일 때의 정적 우선순위 |
| `ioclass`, `ionice` | 입출력 우선순위 |
| `oom_score_adj` | 메모리 부족 시 죽일 순서 |
| `cpuset` | 특정 core에 고정 |
| `cgroup` | 자원 그룹에 배치 |

몇 가지가 눈에 띕니다.

**`sched`가 scheduling policy 자체를 바꿉니다.** 문서가 설명하는 값들 중에 배치용과 유휴용이 있습니다. 배치용에 대한 설명입니다.

> "Very useful for compilers or other CPU-hungry, non-interactive programs"

**컴파일러처럼 CPU를 많이 쓰는 비대화형 프로그램에 유용하다**는 것입니다. 앞 권에서 본 batch 구분이 여기 그대로 있습니다.

**`cpuset`에 이름 붙은 별칭이 있습니다.** 큰 core, 작은 core, 성능 core, 효율 core, 특정 캐시를 가진 core 같은 것들입니다. 요즘 CPU가 성능이 다른 core를 섞어 쓰기 때문입니다.

### type이라는 묶음

같은 설정을 반복해서 쓰지 않도록 묶음을 정의할 수 있습니다.

> "To avoid repeating yourself, you can add types. It must be defined in a `.types` file."

그러니까 규칙 하나는 대개 이렇게 짧습니다.

```json
{ "name": "JustCause2.exe", "type": "Game" }
```

**이름과 분류 하나입니다.** 나머지는 분류가 정해줍니다.

## 7.4 카탈로그를 직접 들여다보기

이 연구가 재현하려는 것이 바로 이 카탈로그이므로, 실제 내용을 확인해봤습니다.

가장 널리 쓰이는 카탈로그 하나를 2026년 9월 12일 시점으로 내려받아 세어봤습니다. 그 시점의 최신 변경은 나흘 전인 9월 8일입니다.

### 분류 정의

카탈로그의 분류 정의 파일 전체입니다. 주석까지 그대로 옮깁니다.

```text
# Type: Game
# Use more CPU time if possible
# Games do not always need more IO, but in most cases can be hungry for CPU
{ "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }

# Type: Player Audio/Video
# Try to add more CPU power to decrease latency/lags
{ "type": "Player-Audio", "nice": -4 }
{ "type": "Player-Video", "nice": -4 }

# Must have more CPU/IO time, but not so much as other apps
{ "type": "Image-View", "nice": -4 }
{ "type": "Doc-View",   "nice": -4 }

# Type: Low Latency Realtime Apps
# In general case not so heavy, but must not lag
{ "type": "LowLatency_RT", "nice": -12, "ioclass": "best-effort" }

# Type: BackGround CPU/IO Load
# Background CPU/IO it's needed, but it must be as silent as possible
{ "type": "BG_CPUIO", "nice": 16, "ioclass": "idle", "sched": "idle" }

# Type: Background CPU but demands more I/O, One example: File Synchronization
{ "type": "BG_CPU", "nice": 14, "ioclass": "best-effort", "sched": "idle" }

# Type: Background Launcher
# Runs quietly but may spawn foreground or latency-sensitive workloads
{ "type": "Launcher", "nice": 16, "ioclass": "idle", "sched": "normal" }

# Type: Heavy CPU Load
# It must work fast enough but must not create so much noise
{ "type": "Heavy_CPU", "nice": 9, "ioclass": "best-effort", "ionice": 7 }

# Type: Chat
{ "type": "Chat", "nice": -3, "ioclass": "best-effort", "ionice": 7 }

# Type: Service
{ "type": "Service", "nice": 10, "ioclass": "best-effort", "ionice": 6 }
```

**이 파일이 앞 권에서 말한 "사람이 손으로 적어 넣은 의미"의 순수한 형태입니다.**

주석을 읽어보면 사람의 판단이 그대로 드러납니다. 게임은 입출력보다 CPU가 급하다. 배경 작업은 필요하긴 하지만 최대한 조용해야 한다. 무거운 계산은 충분히 빨라야 하지만 시끄러우면 안 된다.

전부 맞는 판단입니다. 그리고 전부 사람이 앉아서 생각해서 적은 것입니다.

### 규모

카탈로그를 세어보면 이렇습니다.

| 항목 | 수 |
|---|---|
| 규칙 파일 | 361개 |
| 개별 규칙 항목 | 15,815개 |
| 그중 게임으로 분류된 것 | 13,528개 |

**전체의 85퍼센트가 게임 하나의 분류입니다.**

나머지 분류별로 세어보면 이렇습니다.

| 분류 | 항목 수 |
|---|---|
| Game | 13,528 |
| BG_CPUIO | 1,614 |
| Service | 194 |
| Doc-View | 160 |
| LowLatency_RT | 110 |
| Chat | 51 |
| Heavy_CPU | 33 |
| Image-View | 32 |
| Player-Audio | 28 |
| Player-Video | 24 |
| Launcher | 24 |

**이 표가 앞 권에서 말한 열거의 한계를 숫자로 보여줍니다.**

게임 하나를 알아보기 위해 13,528개의 항목이 필요합니다. 그리고 게임은 계속 나옵니다. 이 카탈로그는 나흘 전에도 갱신됐습니다.

그리고 분류가 열한 가지뿐입니다. 항목이 만 오천 개인데 구분할 수 있는 상황은 열한 가지입니다.

### 규칙이 실제로 어떻게 추가되나

카탈로그의 안내 문서입니다.

> "This is a ananicy-cpp-rules collection for ananicy-cpp maintained by the CachyOS team and the community."

> "You can add your favorite games, apps, and more. Any help would be greatly appreciated!"

> "Please also add the name of the game next to the url, which you get the name of said game from the Steam store."

**게임을 추가할 때 상점 페이지 주소와 이름을 함께 적어달라**고 되어 있습니다. 사람이 상점에서 게임을 찾아보고, 실행 파일 이름을 알아내서, 항목을 만들어 제출하는 흐름입니다.

문서의 실제 예시입니다.

```text
# Just Cause 2 https://store.steampowered.com/app/8190/Just_Cause_2/
{ "name": "JustCause2.exe", "type": "Game" }
```

**게임 하나에 한 줄, 그리고 사람이 확인했다는 흔적으로 주소 하나.**

### 게임 하나가 항목 하나가 아닙니다

문서의 두 번째 예시가 더 흥미롭습니다.

```text
# Mortal Shell https://store.steampowered.com/app/1110910/Mortal_Shell/
{ "name": "Dungeonhaven.exe", "type": "BG_CPUIO" }
{ "name": "Dungeonhaven-Win64-Shipping.exe", "type": "Game" }
```

게임 하나에 항목이 둘입니다. 그리고 **분류가 서로 다릅니다.**

하나는 실행 관리 역할을 하는 실행 파일이라 배경 작업으로 분류하고, 다른 하나가 실제 게임이라 게임으로 분류합니다.

**이걸 알려면 그 게임을 실제로 실행해보고 어떤 프로세스가 뜨는지 확인해야 합니다.** 그리고 그 판단을 사람이 해야 합니다.

만 오천 개의 항목 뒤에 이런 확인이 하나씩 있습니다.

> **이 연구에서는.** 이 카탈로그가 이 연구의 비교 조건을 만드는 근거입니다. 실험에서 이름 목록 기반 인식을 하나의 조건으로 두는데, 그것을 이 카탈로그의 설계를 충실히 재현해서 만듭니다.
>
> 그리고 이 카탈로그가 데이터셋의 근거로도 쓰입니다. 어떤 프로그램이 어떤 분류에 속하는지를 커뮤니티가 정리해둔 것이므로, 배경 작업이 사용자가 원한 것인지 아닌지를 나누는 축이 실제 관행에 존재한다는 근거가 됩니다.

### 상위 프로젝트와 이 카탈로그는 다릅니다

확인 과정에서 알게 된 것 하나를 덧붙입니다.

**원래 프로젝트의 현재 분류 정의 파일은 위와 다릅니다.** 소문자로 된 다른 분류들을 쓰고 있고, 위에서 본 대문자 분류들은 파일 안에 주석 처리된 채로 남아 있습니다. 그 위에 붙은 제목이 "폐기된 분류"입니다.

그러니까 위의 분류 체계는 **C++ 판본과 그 카탈로그 계열의 것**이고, 원래 프로젝트의 현재 상태와는 다릅니다.

> **논문으로.** 이런 구분을 놓치면 인용이 틀어집니다. "이 프로젝트는 이런 분류를 쓴다"고 썼는데 그 프로젝트의 현재 버전은 다른 분류를 쓴다면, 확인한 심사자가 지적할 것입니다.
>
> 정확하게 쓰려면 어느 프로젝트의 어느 카탈로그를 언제 확인했는지까지 적어야 합니다. 이 연구의 인용 기록에는 확인 날짜와 함께 특정 시점의 상태를 고정하라는 메모가 붙어 있습니다.

## 7.5 사용자가 원한 배경 작업이라는 축

한 가지 더 확인된 것이 있습니다. 이 연구의 핵심 구분과 직접 연결됩니다.

앞 권에서 게임 중 다운로드 예를 들었습니다. 사용자가 그 다운로드를 기다리고 있는지 아닌지에 따라 올바른 대우가 정반대라고요.

**그 구분이 실제 소프트웨어에 설정 항목으로 존재합니다.**

한 게임 배포 플랫폼의 도움말 문서 제목이 "게임을 실행하면 다운로드가 자동으로 멈춥니다"입니다. 그리고 설정에 "게임 중 다운로드 허용"이라는 선택 항목이 있습니다. 기본값은 멈추는 쪽이고, 게임별로 따로 정할 수도 있습니다.

**이게 무엇을 뜻하는가.**

기본값이 멈추는 쪽이라는 것은, 대부분의 경우 사용자가 게임을 우선한다고 소프트웨어가 판단했다는 뜻입니다.

그리고 그 선택 항목이 존재한다는 것은, **반대 경우도 실재하기 때문에 사용자가 바꿀 수 있게 했다**는 뜻입니다.

> **이 연구에서는.** 이 설정 항목이 이 연구의 어휘에 있는 축 하나의 근거입니다. 배경에서 도는 일을 사용자가 원했는지 아닌지를 나타내는 참거짓 값이 있는데, 그 축이 실재한다는 것을 이 설정으로 뒷받침합니다.
>
> 그리고 인용 등급을 지킵니다. 이 문서는 배포된 소프트웨어의 문서이므로 **존재 주장에만** 쓸 수 있습니다. "이런 구분이 실제 설정으로 존재한다"까지가 한계이고, "사용자들이 이 설정을 얼마나 바꾼다"거나 "이 구분이 성능에 얼마나 영향을 준다"로 넘어갈 수 없습니다.

## 7.6 그래서 이 갈래가 이 연구에 주는 것

### 전제를 증명해줍니다

이 연구의 전제는 이렇습니다. **프로세스의 이름에 scheduling에 쓸 만한 정보가 들어 있다.**

이건 증명이 필요한 주장처럼 보입니다. 그런데 이 장의 소프트웨어들이 이미 증명하고 있습니다. **만 오천 개의 항목을 사람들이 손으로 만들어 쓰고 있다는 사실 자체가 그 정보가 유용하다는 증거입니다.**

쓸모없었으면 아무도 안 만들었을 것입니다.

### 동시에 두 한계를 체현합니다

**열거의 한계.** 게임 하나를 알아보려고 13,528개가 필요하고, 그것도 게임 하나에 항목이 여러 개일 수 있으며, 새 게임이 나올 때마다 늘어납니다. 그리고 앞 권에서 봤듯이 프로그램들의 조합은 애초에 열거할 수 없습니다.

**노후화의 한계.** 항목 하나마다 사람의 노동이 들어갑니다. 상점에서 확인하고, 실행해보고, 실행 파일 이름을 알아내고, 제출하고, 검토받습니다. 그 노동이 영원히 계속돼야 합니다.

### 그래서 진짜 비교 상대입니다

이 연구가 무엇을 주장하는지 정확히 말하면 이렇습니다.

**같은 입력을 쓰고, 같은 종류의 출력을 내되, 표를 지식으로 바꾼다.**

입력이 같습니다. 프로세스 이름과 명령줄입니다.

출력의 종류가 같습니다. 상황에 대한 판단입니다.

다른 것은 그 판단을 어디서 가져오느냐입니다. 미리 적어둔 표에서 찾는 대신, 세상에 대한 지식으로 추론합니다.

> **논문으로.** 그래서 실험의 비교 조건이 기본 scheduler가 아니라 이 방식이어야 합니다. 기본 scheduler를 이기는 것은 별로 어렵지 않고, 이겨도 "그건 이름 목록으로도 됐을 텐데요"라는 반문을 못 막습니다.
>
> 저장소의 related work 초고에 이 입장이 명확히 적혀 있습니다. 이 갈래를 경쟁자가 아니라 baseline으로 다루고, 논문의 핵심 실험은 정확히 **이름 표가 따라올 수 없는 경우들**이라는 것입니다.
>
> 그리고 한 가지 원칙이 더 있습니다. **이름 표가 이기는 경우도 이긴 대로 보고합니다.** 유명한 소프트웨어이고 이름이 정확히 일치하는 경우에는 표가 더 나을 수 있습니다. 그걸 숨기면 논문 전체의 신뢰가 떨어집니다.

---

## 7장 정리

- 이 장의 대상은 연구가 아니라 지금 실제로 돌고 있는 소프트웨어입니다. 프로그램 이름을 보고 상황을 판단해 시스템 설정을 바꾸는데, 판단을 사람이 미리 표에 적어뒀습니다.
- Windows의 게임 모드는 제조사 문서 사이트에 접근하지 못해 확인 범위가 좁습니다. 확인된 것은 하드웨어 자원에 대한 독점적 접근을 준다는 것, 자원 모델이 독점 CPU 집합이라는 것, 전면에 있고 초점을 가져야 한다는 조건, 사용자가 끌 수 있다는 것입니다. 게임을 어떻게 판별하는지는 확인하지 못했습니다.
- Linux 쪽의 우선순위 조정 데몬은 전부 공개되어 있습니다. 실행 파일 이름으로 프로세스를 찾아 표를 뒤지고 설정을 적용합니다. 이름이 같아도 실행 인자로 구분할 수 있습니다.
- 설정할 수 있는 항목이 넓습니다. CPU 우선순위, scheduling policy 자체, 입출력 우선순위, 메모리 부족 시 죽일 순서, core 고정까지 포함합니다.
- 널리 쓰이는 카탈로그를 직접 세어보니 규칙 파일 361개에 항목 15,815개였고, 그중 13,528개가 게임으로 분류되어 있었습니다. 전체의 85퍼센트입니다. 분류는 열한 가지뿐입니다.
- 항목 추가는 사람이 상점에서 게임을 찾고 실행 파일 이름을 알아내서 제출하는 방식입니다. 게임 하나에 항목이 여럿일 수 있고, 같은 게임의 다른 실행 파일이 다른 분류를 받기도 합니다. 그걸 알려면 직접 실행해봐야 합니다.
- 게임 실행 시 다운로드를 멈추는 설정이 실제 소프트웨어에 존재합니다. 기본값이 멈추는 쪽이고 사용자가 바꿀 수 있다는 것은, 반대 경우도 실재하기 때문입니다. 이 연구의 어휘에 있는 축 하나의 근거입니다.
- 이 갈래가 이 연구의 전제를 증명합니다. 만 오천 개의 항목을 사람들이 손으로 만들어 쓰고 있다는 사실 자체가 이름에 쓸 만한 정보가 있다는 증거입니다.
- 동시에 두 한계를 체현합니다. 열거의 한계와 노후화의 한계입니다. 그래서 이 연구의 진짜 비교 상대이고, 이쪽이 이기는 경우도 이긴 대로 보고한다는 원칙이 함께 갑니다.

---

# 8장 · 평가는 무엇으로 하나

## 8.1 이 장이 짧은 이유

새 scheduler를 만들었으면 좋아졌는지 재야 합니다. 무엇으로 잴까요?

이 분야에는 표준적으로 쓰이는 도구들이 있습니다. 이 장에서 그것들을 훑습니다.

다만 짧게 다룹니다. 데이터셋 이야기는 뒤에 따로 세 권이 있고, 거기서 자세히 볼 것이기 때문입니다. 여기서 알아야 할 것은 하나입니다. **왜 이 연구가 기존 도구를 그대로 쓸 수 없었는가.**

## 8.2 kernel을 괴롭히는 도구들

### 많은 task를 만들어 부하를 주는 것

가장 오래되고 널리 쓰이는 도구가 있습니다. 문서의 설명입니다.

> "Hackbench is both a benchmark and a stress test for the Linux kernel scheduler. It's main job is to create a specified number of pairs of schedulable entities (either threads or traditional processes) which communicate via either sockets or pipes and time how long it takes for each pair to send data back and forth."

**서로 통신하는 task 쌍을 잔뜩 만들어놓고 얼마나 걸리는지 재는 것**입니다.

기본값을 문서에서 옮기면 이렇습니다.

> "Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)"

> "Each sender will pass 100 messages of 100 bytes"

400개의 task가 100바이트짜리 메시지를 100번씩 주고받습니다.

**이 도구가 재는 것은 처리량입니다.** 전부 끝나는 데 걸린 시간 하나입니다. 누가 얼마나 기다렸는지, 반응이 빨랐는지는 재지 않습니다.

### 꼬리 지연을 재는 것

좀 더 최근에 만들어진 도구는 다른 것을 겨냥합니다. 문서가 목표를 세 줄로 밝힙니다.

> "- Saturate all the CPUs on the system. Leaving idle CPUs behind will result in lower RPS.
> - Long timeslices. Involuntary context switches will result in lower RPS.
> - Low scheduling delays. Higher wakeup latencies will result in lower RPS."

**core를 놀리지 말 것, 강제로 끌어내리지 말 것, 깨운 뒤 빨리 실행할 것.** 앞 권에서 배운 개념들이 그대로 목표로 적혀 있습니다.

구조는 이렇습니다.

> "schbench uses messaging threads and worker threads. Workers perform an artificial request comprised of two usleeps (simulating network/disk/locking) and some matrix math. Messaging threads just queue up the work and wait for results."

일을 넘겨주는 thread와 처리하는 thread가 있습니다. 앞 권에서 본 chain 구조의 단순한 형태입니다.

재는 것이 셋입니다.

> "- Wakeup latency: messaging threads record the time a worker is posted, and workers compare this with the time when they start running.
> - Request latency: time required to complete our fake request.
> - Requests per second: total number of requests all the threads are able to complete."

**깨운 뒤 실제 실행까지의 시간**이 첫 번째 항목입니다. 앞 권에서 이 연구의 가장 중요한 숫자라고 한 것과 같습니다.

그리고 이 도구는 결과를 백분위수로 보고합니다. 50, 90, 99, 99.9 백분위수와 최솟값 최댓값입니다. 앞 권에서 왜 평균이 아니라 꼬리를 봐야 하는지 설명했는데, 그 원칙이 도구에 반영되어 있습니다.

> **이 연구에서는.** 이 도구의 보고 방식이 이 연구의 선례로 쓰입니다. 지연 지표를 백분위수로 보고하는 것이 이 분야의 관행이라는 근거입니다.

## 8.3 대화형 상황을 흉내 내는 도구들

### 상호작용성 벤치마크

앞의 두 도구는 부하를 주고 처리량이나 지연을 잽니다. 대화형 상황 자체를 흉내 내는 도구도 있습니다.

> "This benchmark application is designed to benchmark interactivity in Linux."

> "It is designed to emulate the cpu scheduling behaviour of interactive tasks and measure their scheduling latency and jitter."

이 도구가 흉내 내는 작업 목록이 흥미롭습니다. 문서에서 옮깁니다.

> "X: X is simulated as a thread that uses a variable amount of cpu ranging from 0 to 100%. This simulates an idle gui where a window is grabbed and then dragged across the screen."

> "Audio: Audio is simulated as a thread that tries to run at 50ms intervals that then requires 5% cpu."

> "Video: Video is simulated as a thread that tries to receive cpu 60 times per second and uses 40% cpu. This would be quite a demanding video playback at 60fps."

> "Gaming: The cpu usage behind gaming is not at all interactive, yet games clearly are intended for interactive usage. This load simply uses as much cpu as it can get. It does not return deadlines met as there are no deadlines with an unlocked frame rate in a game."

**앞 권에서 배운 것들이 여기 수치로 박혀 있습니다.** 오디오는 50밀리초마다 5퍼센트, 영상은 초당 60번에 40퍼센트입니다.

게임에 대한 설명이 특히 정직합니다. **게임의 CPU 사용은 전혀 대화형이 아니지만 게임은 분명히 대화형 용도**라는 것입니다. 그래서 이 도구는 게임을 그냥 CPU를 최대한 쓰는 부하로 모델링하고, frame 상한이 없으면 마감도 없으므로 마감 달성률을 보고하지 않는다고 밝힙니다.

배경 부하도 여러 가지를 제공합니다. 아무것도 없음, 영상, 창 끌기, CPU 태우기, 디스크 쓰기, 디스크 읽기, 컴파일 흉내, 메모리 압박입니다.

측정 항목은 다섯입니다.

> "1. The average scheduling latency... 2. The scheduling jitter is represented by calculating the standard deviation of the latency 3. The maximum latency seen during the test period 4. Percentage of desired cpu 5. Percentage of deadlines met."

평균, 흔들림, 최댓값, 원하는 만큼 받았는지, 마감을 지켰는지입니다.

> **이 연구에서는.** 이 도구의 작업 모델이 이 연구 데이터셋의 근거 중 하나로 쓰입니다. 다만 인용할 때 표현을 조심합니다. **"데스크톱이 실제로 이렇게 동작한다"가 아니라 "커뮤니티가 대화형 작업을 이렇게 모델링한다"**로 씁니다.
>
> 차이가 큽니다. 앞엣것은 측정 결과에 대한 주장이고, 뒤엣것은 관행의 존재에 대한 주장입니다. 이 도구는 뒤엣것만 뒷받침합니다.

### 작업 모델을 파일로 쓰는 도구

또 하나 중요한 도구가 있습니다. 문서의 설명입니다.

> "rt-app is a test application that starts multiple periodic threads in order to simulate a real-time periodic load."

주기적인 부하를 흉내 냅니다. 특이한 것은 **그 부하를 JSON 파일로 기술한다**는 점입니다.

> "The json file that describes a workload is made on 3 main objects: tasks, resources and global objects."

> "phases: Object. The phases object describes the behavior of the thread. This behavior can be split in several distinct phases with their own events and properties."

thread의 동작을 여러 국면으로 나누고, 각 국면에 일어날 일을 순서대로 적습니다.

적을 수 있는 동작들입니다.

| 동작 | 무엇을 하나 |
|---|---|
| `run` | 정해진 시간만큼 CPU를 태운다 |
| `runtime` | CPU 성능과 무관하게 정해진 시간 동안 실행한다 |
| `sleep` | 잠든다 |
| `timer` | 타이머로 깨어난다 |
| `mem`, `iorun` | 메모리 쓰기와 입출력을 흉내 낸다 |

그리고 각 thread에 scheduling policy와 마감까지 지정할 수 있습니다.

> **이 연구에서는.** 이 도구가 이 연구 데이터셋의 **형식적 선례**입니다.
>
> 이 연구도 workload를 파일로 기술합니다. task 하나가 무엇을 하는지를 몇 가지 기본 동작의 나열로 적습니다. 실행, 잠들기, 타이머, 대기, 깨우기, 생성과 종료입니다.
>
> 그 발상이 여기서 왔습니다. 특히 타이머로 주기를 표현하는 방식이 그렇습니다. 뒤 권에서 그 형식을 자세히 다룹니다.

## 8.4 상용 데스크톱 벤치마크

지금까지의 도구들은 kernel 개발자용입니다. 상용 벤치마크는 다른 것을 겨냥합니다. **실제 응용을 실제로 돌립니다.**

가장 널리 쓰이는 것 하나의 기술 문서를 확인했습니다. 2021년 2월판이고 141쪽짜리입니다.

구조를 문서가 이렇게 설명합니다.

> "PCMark 10 uses a modular approach to build relevant tests around common end-user scenarios. There are three levels to this approach: benchmarks, test groups, and workloads."

시나리오 묶음과 그 안의 개별 작업으로 나뉩니다.

묶음이 넷입니다.

| 묶음 | 안에 든 작업 |
|---|---|
| Essentials | 앱 시작, 웹 브라우징, 화상 회의 |
| Productivity | 문서 작성, 스프레드시트 |
| Digital Content Creation | 사진 편집, 영상 편집, 렌더링 |
| Gaming | 그래픽 성능 시험 |

**앞 권에서 다룬 상황들과 겹칩니다.** 그리고 이 연구의 어휘에 있는 항목들과도 겹칩니다.

그리고 이 문서는 어떤 프로그램을 쓰는지까지 밝힙니다.

> "• Chromium web browser • Firefox web browser • LibreOffice Writer word processing program • GIMP image manipulation program"

사진 편집은 이미지 처리 라이브러리를, 영상 편집은 영상 변환 라이브러리를, 렌더링은 광선 추적 프로그램을 씁니다. 화상 회의는 얼굴 인식 라이브러리를 씁니다.

문서 뒤쪽에는 쓰인 소프트웨어의 버전까지 전부 나열되어 있습니다.

> **이 연구에서는.** 이런 상용 벤치마크가 데이터셋의 근거 중 하나로 쓰입니다. 다만 쓰는 방식이 제한적입니다. **어떤 상황들이 데스크톱의 대표적인 사용으로 여겨지는지에 대한 분류 근거**로만 씁니다.
>
> "이 회사가 데스크톱 사용을 이 네 묶음으로 나눈다"는 것은 그 문서로 뒷받침됩니다. 하지만 "사용자들이 실제로 이렇게 쓴다"는 다른 주장이고 그 문서로 뒷받침되지 않습니다.

> **확인 필요.** 다른 두 상용 벤치마크에 대해서는 제조사 사이트에 접근할 수 없어서 아무것도 확인하지 못했습니다. 이 연구의 인용 기록에도 그 둘은 제출 전에 주소를 확정해야 할 항목으로 표시되어 있습니다.

## 8.5 왜 이걸로 안 되는가

도구들을 훑고 나면 질문이 남습니다. 이렇게 많은데 왜 데이터셋을 새로 만들었을까요?

이유가 하나입니다.

> **어느 도구에도 의도가 라벨로 붙어 있지 않습니다.**

하나씩 확인해봅시다.

**kernel 벤치마크들**은 부하를 만들고 지연이나 처리량을 잽니다. 그 부하가 어떤 상황인지에 대한 정보가 없습니다. 400개의 task가 메시지를 주고받는 것이 게임인지 빌드인지 알 수 없습니다. 애초에 그런 개념이 없습니다.

**상호작용성 벤치마크**는 상황을 흉내 냅니다. 오디오, 영상, 게임 같은 이름이 붙어 있습니다. 여기까지는 좋습니다. 하지만 **배경 작업이 사용자가 원한 것인지 아닌지를 구분하지 않습니다.** CPU 태우기 부하는 그냥 CPU 태우기입니다. 사용자가 시작한 것인지 예약된 것인지가 없습니다.

**상용 벤치마크**는 실제 응용을 돌리고 시나리오 이름도 붙어 있습니다. 하지만 목적이 다릅니다. **하드웨어를 비교하려고 만든 도구**입니다. 같은 작업을 여러 기계에서 돌려서 점수를 매기는 것이 목적이고, scheduling 정책의 차이를 드러내려고 만든 것이 아닙니다.

그리고 결정적으로, **이 연구가 필요로 하는 구조가 어디에도 없습니다.**

이 연구가 필요로 하는 것은 이렇습니다. **행동이 완전히 동일하고, 올바른 설정이 정반대인 workload 쌍.**

그런 쌍은 우연히 만들어지지 않습니다. 설계해서 만들어야 합니다. 두 workload가 CPU 사용 패턴, 깨어나는 빈도, 잠드는 방식까지 같도록 맞추고, 프로세스 이름만 다르게 해야 합니다.

**그리고 각 workload에 정답 라벨이 붙어 있어야 합니다.** 언어 모델의 인식을 채점하려면 정답이 필요하기 때문입니다. 기존 벤치마크에는 그런 라벨이 없습니다.

> **논문으로.** 이것이 데이터셋 절의 첫 문단이 됩니다. "왜 기존 벤치마크를 쓰지 않았는가"는 심사자가 반드시 묻는 질문이고, 답이 명확해야 합니다.
>
> 그리고 답이 "기존 것이 나빠서"가 아니라 **"기존 것이 다른 질문에 답하려고 만들어졌기 때문"**이어야 합니다. 앞의 도구들은 각자의 목적에 잘 맞습니다. 이 연구의 질문에 맞지 않을 뿐입니다.

---

## 8장 정리

- 이 분야에는 표준적으로 쓰이는 평가 도구들이 있습니다. 이 장은 짧게 훑고, 자세한 것은 데이터셋을 다루는 뒤 권으로 넘깁니다.
- kernel을 괴롭히는 도구 중 오래된 것은 서로 통신하는 task를 400개쯤 만들어 전체 완료 시간을 잽니다. 처리량 도구입니다.
- 더 최근 도구는 core를 놀리지 말 것, 강제로 끌어내리지 말 것, 깨운 뒤 빨리 실행할 것을 목표로 삼고, 깨움 지연과 요청 지연과 초당 처리량을 백분위수로 보고합니다. 앞 권에서 배운 개념들이 그대로 도구의 목표에 들어 있습니다.
- 상호작용성 벤치마크는 대화형 작업 자체를 흉내 냅니다. 오디오는 50밀리초마다 5퍼센트, 영상은 초당 60번에 40퍼센트 같은 식으로 수치가 박혀 있습니다. 게임에 대해서는 CPU 사용이 전혀 대화형이 아니라는 점을 스스로 밝힙니다.
- 작업 모델을 JSON 파일로 기술하는 도구가 있습니다. thread의 동작을 국면으로 나누고 실행, 잠들기, 타이머 같은 기본 동작의 나열로 적습니다. 이 연구 데이터셋의 형식적 선례입니다.
- 상용 데스크톱 벤치마크는 실제 응용을 실제로 돌립니다. 시나리오를 네 묶음으로 나누고 각 묶음에 어떤 프로그램을 쓰는지까지 문서에 밝힙니다. 다만 하드웨어를 비교하려고 만든 도구입니다.
- 이 연구가 데이터셋을 새로 만든 이유는 하나입니다. 어느 도구에도 의도가 라벨로 붙어 있지 않습니다. 그리고 행동이 동일하고 올바른 설정이 정반대인 workload 쌍은 우연히 만들어지지 않고 설계해야 합니다. 인식을 채점하려면 정답 라벨도 필요합니다.

---

# 9장 · 지형도: 두 축과 빈칸

## 9.1 이 장이 하는 일

앞의 여섯 장에서 여러 연구를 봤습니다. 이제 한 장의 그림으로 정리합니다.

목적이 둘입니다. 첫째, 전체가 어떻게 배치되어 있는지 한눈에 보기 위해서입니다. 둘째, 이 그림이 논문에 실제로 들어갈 그림이기 때문입니다.

## 9.2 축을 고르는 일

지형도를 그리려면 축을 골라야 합니다. 그런데 축을 고르는 것 자체가 주장입니다.

예를 들어 "발표 연도"를 축으로 삼으면 시간 순서만 보이고 왜 이 연구가 필요한지는 안 보입니다. "성능 개선폭"을 축으로 삼으면 서로 다른 문제를 푼 연구들을 억지로 한 줄에 세우게 됩니다.

**좋은 축은 이 연구가 서 있는 자리를 드러내는 축입니다.** 그리고 그 축 위에서 빈칸이 자연스럽게 보여야 합니다.

앞의 장들을 되짚어보면 연구들이 두 가지 면에서 갈렸습니다.

**무엇을 읽는가.** 어떤 연구는 행동을 읽고, 어떤 연구는 이름과 세상에 대한 지식을 읽습니다.

**무엇을 만드는가.** 어떤 연구는 정책 자체를 만들어내고, 어떤 연구는 미리 있는 정책 중에서 고를 신호를 만듭니다.

이 둘이 축입니다.

## 9.3 지형도

```text
                무엇을 만드는가
                
                정책을 생성한다          신호를 만들고 고른다
              ┌─────────────────────┬─────────────────────┐
              │                     │                     │
   행동을     │  학습된 scheduler   │  MLFQ, fair-share   │
   읽는다     │  Decima             │  scx_lavd           │
              │  FIRM               │  ASA                │
              │                     │                     │
  무 ─────────┼─────────────────────┼─────────────────────┤
  엇          │                     │                     │
  을          │  LLM agent 계열     │  ★ 이 연구          │
  읽          │  SchedCP            │                     │
  는          │  Kgent              │  지금 이 칸에 있는  │
  가          │  TuneAgent          │  것은 정적인        │
              │                     │  이름 표뿐          │
   이름과     │                     │  Game Mode          │
   지식을     │                     │  우선순위 조정 데몬 │
   읽는다     │                     │                     │
              └─────────────────────┴─────────────────────┘

   그리고 네 칸 전체의 아래에 mechanism 계열이 깔려 있다
   ghOSt, sched_ext — 어느 칸의 결정이든 실제로 실행하는 층
```

## 9.4 칸을 하나씩 읽기

### 왼쪽 위: 행동을 읽고 정책을 생성

강화학습으로 scheduling 정책을 배우는 연구들입니다.

관찰된 시스템 상태를 입력으로 받아 행동을 출력하는 모델을 학습시킵니다. 사람이 규칙을 쓰지 않는다는 점이 기여입니다.

**한계는 두 가지였습니다.** 환경이 바뀌면 재학습이 필요하고, 사람이 미리 정해준 관측 항목 안에서만 움직입니다.

### 오른쪽 위: 행동을 읽고 신호를 만듦

지금 실제로 돌아가는 scheduler 대부분이 여기 있습니다. MLFQ의 강등 규칙, fair-share의 누적 회계.

그리고 이 칸의 가장 발전한 형태가 지연 민감도를 추정하는 정책과, 인식한 뒤 전문 정책을 고르는 연구입니다.

**한계는 채널입니다.** 행동이 동일하고 의도가 다른 상황을 구분할 수 없습니다.

### 왼쪽 아래: 이름과 지식을 읽고 정책을 생성

언어 모델로 kernel 정책을 만들어내는 최근 연구들입니다.

읽는 채널이 바뀌었습니다. 행동만이 아니라 소스 코드, 문서, 프로파일 결과까지 읽고 의미를 해석합니다.

**대상이 서버 작업입니다.** 최적화할 대상이 명확한 하나의 workload를 놓고 시간을 들여 분석합니다.

### 오른쪽 아래: 이름과 지식을 읽고 신호를 만듦

**이 칸이 이 연구의 자리입니다.**

그리고 이 칸이 비어 있지 않습니다. 앞 장에서 본 이름 표들이 여기 있습니다.

게임 모드도, 우선순위 조정 데몬도, 정확히 이 일을 합니다. 이름을 읽고, 상황을 판단하고, 미리 정해진 설정을 적용합니다.

**다만 판단하는 방법이 정적입니다.** 사람이 미리 적어둔 표를 뒤집니다.

그러니까 정확히 말하면 이렇습니다. **이 칸의 정적인 자리는 차 있고, 동적인 자리가 비어 있습니다.**

### 아래에 깔린 층

네 칸 전부의 아래에 실행 계층이 있습니다. 정책을 갈아 끼울 수 있게 만든 연구들입니다.

이건 축 위의 한 점이 아니라 **모든 칸이 딛고 서는 바닥**입니다. 어느 칸의 결정이든 실제 시스템에서 작동하려면 이 층이 필요합니다.

## 9.5 이 그림이 말하는 것

지형도를 다 그리고 나면 이 연구의 주장이 한 문단으로 정리됩니다.

**데스크톱의 상황 인식이 있어야 할 자리는 오른쪽 아래 칸입니다.**

왼쪽 위와 오른쪽 위는 행동을 읽으므로 의도를 볼 수 없습니다. 왼쪽 아래는 의미를 읽지만 그것을 서버 작업의 정책 합성에 씁니다.

**그리고 오른쪽 아래 칸에는 지금 정적인 이름 표만 있습니다.**

이 연구가 하려는 것은 그 칸의 동적인 자리를 채우는 것입니다. **이름 표가 읽는 것을 읽고, 이름 표가 만드는 것을 만들되, 표를 지식으로 바꾸는 것입니다.**

## 9.6 축을 다르게 그으면 어떻게 되나

한 가지 연습을 해두면 좋습니다. **이 축이 유일한 정답이 아닙니다.**

다른 축을 생각해봅시다.

**"얼마나 자주 판단하는가"를 축으로 삼으면** 어떻게 될까요. 매 scheduling 결정마다 판단하는 것부터, 몇 초에 한 번, 몇 분에 한 번, 배포할 때 한 번까지. 이 축 위에서는 이 연구가 중간쯤에 놓입니다. 흥미로운 그림이지만 이 연구의 기여가 잘 안 보입니다.

**"누가 지식을 제공하는가"를 축으로 삼으면** 사용자, 개발자, 커뮤니티, 학습된 모델, 언어 모델로 나뉩니다. 이것도 말이 되는 그림이고, 앞 권에서 우선순위를 누가 정하느냐를 다룰 때 썼던 구분과 통합니다.

**축을 고르는 것이 주장이라는 말이 이 뜻입니다.** 같은 연구들을 놓고도 축을 다르게 그으면 다른 이야기가 됩니다.

그러면 아무 축이나 골라서 유리하게 그려도 되나요? 안 됩니다. 좋은 축에는 조건이 있습니다.

**연구들이 실제로 그 축에서 갈려야 합니다.** 억지로 나누면 심사자가 알아봅니다.

**그 축이 결과의 차이를 설명해야 합니다.** 이 연구의 두 축이 그렇습니다. 읽는 채널이 다르면 볼 수 있는 것이 다르고, 만드는 것이 다르면 검증 부담과 비용이 다릅니다.

**그리고 빈칸이 진짜로 비어 있어야 합니다.** 채워져 있는데 안 보이는 척하면 안 됩니다. 그래서 이 연구는 오른쪽 아래 칸이 완전히 비어 있다고 말하지 않고, 정적인 자리는 차 있다고 명시합니다.

> **논문으로.** 이 그림은 논문에 실제로 들어갈 후보입니다. 저장소의 related work 초고에 그렇게 적혀 있습니다. 서론이나 related work 절에 그림 하나로 넣고, 그 문단은 두 문장으로 줄여서 그림을 가리키라는 것입니다.
>
> 그림이 있으면 심사자가 5초 만에 이 연구의 자리를 파악합니다. 같은 내용을 문단으로 쓰면 세 번 읽어야 합니다.

---

## 9장 정리

- 지형도의 축을 고르는 것 자체가 주장입니다. 좋은 축은 이 연구가 서 있는 자리를 드러내고 빈칸이 자연스럽게 보이는 축입니다.
- 이 연구가 고른 두 축은 무엇을 읽는가와 무엇을 만드는가입니다. 행동을 읽는가 이름과 지식을 읽는가, 그리고 정책을 생성하는가 신호를 만들어 고르는가입니다.
- 왼쪽 위는 학습된 scheduler입니다. 재학습 비용과 미리 정해진 관측 항목이 한계입니다.
- 오른쪽 위는 지금 실제로 돌아가는 scheduler 대부분과 그 계열의 최신 연구들입니다. 채널이 한계입니다.
- 왼쪽 아래는 언어 모델로 정책을 만드는 최근 연구들입니다. 채널은 바뀌었지만 대상이 서버 작업입니다.
- 오른쪽 아래가 이 연구의 자리이고, 완전히 비어 있지는 않습니다. 정적인 이름 표들이 이미 여기서 정확히 같은 일을 하고 있습니다. 비어 있는 것은 동적인 자리입니다.
- 네 칸 전부의 아래에 정책을 갈아 끼우는 실행 계층이 깔려 있습니다. 축 위의 한 점이 아니라 모두가 딛는 바닥입니다.
- 축은 유일한 정답이 아닙니다. 판단 빈도나 지식의 출처를 축으로 삼아도 말이 되는 그림이 나옵니다. 다만 좋은 축에는 조건이 있습니다. 연구들이 실제로 그 축에서 갈려야 하고, 그 축이 결과의 차이를 설명해야 하며, 빈칸이 진짜로 비어 있어야 합니다.

---

# 10장 · related work 절은 어떻게 쓰는가

## 10.1 이 절의 진짜 목적

이 권의 첫 장에서 말했습니다. related work는 인용 나열이 아니라 이 연구가 앉을 자리가 비어 있음을 증명하는 글이라고요.

이제 그것을 구체적으로 봅니다.

심사자가 논문을 읽으면서 던지는 질문은 정해져 있습니다. **이거 이미 있는 거 아닌가.** 그리고 그 질문은 막연하지 않습니다. 특정 연구를 지목합니다.

**그러니까 related work의 각 문단은 특정 반론 하나를 받아내는 자리입니다.**

## 10.2 반론을 먼저 적고 문단을 쓰기

이 연구의 related work 초고는 실제로 그 방식으로 쓰여 있습니다.

각 소절의 끝에 기울임체로 메모가 붙어 있습니다. 그 메모에 **이 문단이 흡수하려는 반론**이 적혀 있고, 제출 전에 지우라고 표시되어 있습니다.

메모에 적힌 반론들을 옮기면 이렇습니다.

| 소절 | 흡수하려는 반론 | 답의 요지 |
|---|---|---|
| mechanism 계열 | 정책 교체 기능이 이미 이거 아닌가 | 그건 액추에이터이고 센서가 아니다 |
| behavior 계열 | 지연 민감도를 이미 추정하는데 왜 부족한가 | task 하나의 성질이지 machine의 상황이 아니고, 채널이 행동이다 |
| 학습된 scheduler | 인식한 뒤 고르는 구조가 이미 있다 | 기여는 골격이 아니라 채널이다 |
| LLM 계열 | 이건 그 연구의 데스크톱 판 아닌가 | 출력 계약과 측정 계층이 다르다 |
| 이름 표 | 게임 모드가 이미 있다 | 그건 경쟁자가 아니라 우리의 baseline이다 |

**이 표가 related work 절의 설계도입니다.**

문단을 먼저 쓰고 반론을 나중에 생각하는 것이 아니라, 반론을 먼저 적고 그것을 받아내는 문단을 씁니다.

> **논문으로.** 이 방식을 권합니다. 어떤 연구를 다룰지 정할 때 "관련 있으니까"가 아니라 "이걸 안 다루면 심사자가 이 논문을 들고 올 것이니까"로 정하면, 넣을 것과 뺄 것이 명확해집니다.

## 10.3 순서에도 이유가 있습니다

초고의 소절 순서는 이렇습니다. 실행 계층, 행동 기반 추론, 학습된 scheduler, 언어 모델 계열, 배포된 이름 표, 그리고 마지막에 위치 정리입니다.

이 순서가 우연이 아닙니다.

**실행 계층을 맨 앞에 둔 이유.** 이 갈래는 경쟁자가 아니라 전제입니다. 먼저 "이건 우리가 딛고 서는 바닥이다"를 정리해두면, 뒤의 이야기가 그 위에서 진행됩니다. 그리고 시뮬레이터 기반 평가의 정당화도 여기서 미리 깔립니다.

**이름 표를 맨 뒤에 둔 이유.** 이것이 진짜 baseline이기 때문입니다. 마지막에 두면 그다음에 오는 위치 정리와 자연스럽게 이어지고, 독자의 머리에 "그러니까 이 연구는 저 표를 대체하려는 것"이 남은 채로 다음 절로 넘어갑니다.

**가운데 세 갈래의 순서.** 행동에서 학습으로, 학습에서 의미로 갑니다. 읽는 채널이 점점 이 연구에 가까워지는 순서입니다. 마지막의 언어 모델 계열이 가장 가까우므로 가장 길게 다룹니다.

## 10.4 가장 강한 반대편을 후하게 다루기

초고의 메모 중에 이런 것이 있습니다. 행동 기반 추론 계열에 대한 것입니다.

**그 계열의 가장 발전한 연구를 후하게 인용하라**는 내용입니다. 이유가 둘 적혀 있습니다.

첫째, 그 연구가 실제 제품에 쓰인다는 사실이 **데스크톱 scheduling이 중요하다는 것을 뒷받침**해줍니다. 이 연구에 유리한 근거입니다.

둘째, 그것이 **이 연구가 반대하는 입장의 가장 강한 버전**이기 때문입니다.

두 번째가 중요합니다. 반대편을 약하게 그려놓고 이기는 것은 아무 의미가 없습니다. 심사자가 바로 알아봅니다. 반대편을 가장 강한 형태로 세워놓고, 그래도 이 지점에서는 안 된다고 보여야 논증이 섭니다.

## 10.5 서론과 related work가 어긋나면 안 됩니다

또 하나의 메모가 학습된 scheduler 계열에 붙어 있습니다.

골격이 같은 연구에 대해, **서론에서 가깝다는 것을 흐리게 말했다가 related work에서 축소하지 말라**는 내용입니다. 그리고 이유가 붙어 있습니다. **심사자들이 그 두 부분을 대조해서 읽는다**는 것입니다.

이건 실무적인 조언입니다. 논문을 쓰다 보면 서론에서는 기여를 크게 말하고 싶고 related work에서는 선행 연구와의 거리를 벌리고 싶어집니다. 그러다 보면 두 절이 서로 다른 이야기를 하게 됩니다.

**심사자는 그 불일치를 찾아냅니다.** 그리고 한 번 찾으면 논문 전체를 의심하기 시작합니다.

## 10.6 인용 규율

이 권을 쓰면서 실제로 겪은 것들을 정리합니다. 전부 논문 작업에 그대로 적용되는 사항입니다.

### 판본과 게재 여부는 바뀝니다

앞에서 본 대로, 심사 없이 올라간 원고는 계속 바뀝니다.

이 권을 쓰면서 실제로 발견한 것들입니다.

**한 논문은 제목이 바뀌었습니다.** 첫 판본과 지금 판본의 제목이 다르고, 저자 목록도 한 명이 다릅니다.

**한 논문은 길이가 오갔습니다.** 짧은 형태로 올라갔다가 학회 형식의 긴 원고가 됐다가 다시 짧은 형태로 돌아왔습니다. 그래서 "이 논문에 이렇게 적혀 있다"고 말할 때 어느 판본인지가 중요합니다.

**한 논문은 저장소가 특정 학회 게재를 언급하고 있습니다.** 이 연구의 인용 기록에는 게재 학회가 없다고 적혀 있는데, 그 사이에 바뀌었을 수 있습니다.

**그러니 제출 직전에 다시 확인하는 절차가 필요합니다.** 이 연구의 인용 기록에는 가장 가까운 선행 연구에 대해 "제출할 때마다 후속 논문이 나왔는지 다시 확인할 것"이라는 메모가 명시되어 있습니다. 이 권의 확인으로 그 메모가 옳다는 것이 다시 확인됐습니다.

### 저자 이름은 정확히

같은 연구실에서 나온 두 논문의 저자 표기가 다른 경우가 있습니다. 한 논문에서는 이름을 줄여 쓰고 다른 논문에서는 전체를 쓰는 식입니다.

사소해 보이지만 참고문헌 목록에서는 두 사람으로 보일 수 있습니다.

### 어디서 읽었는지를 구분해서 적기

이 권을 쓰면서 접근할 수 없는 자료가 많았습니다. 그때 취한 방침이 이렇습니다.

**논문 원문을 읽은 것, 저자들의 공개 저장소를 읽은 것, 그리고 읽지 못한 것을 구분해서 표시했습니다.**

저자들의 저장소는 신뢰할 만하지만 논문이 아닙니다. 저장소의 설명 문구를 논문의 초록인 것처럼 인용하면 안 됩니다. 확인한 심사자가 지적할 것입니다.

**그리고 읽지 못한 것에는 무엇을 확인해야 하는지를 함께 적었습니다.** 나중에 접근이 가능해졌을 때 무엇을 열어봐야 하는지 알 수 있게요.

### 등급을 지키기

첫 장에서 정리한 세 등급이 이 권 전체에서 지켜졌습니다. 다시 짚으면 이렇습니다.

심사를 거친 학술 문헌은 실험적이고 통계적인 주장을 뒷받침할 수 있습니다.

배포된 소프트웨어의 문서와 저장소는 **존재 주장만** 뒷받침합니다. 카탈로그에 항목이 만 오천 개 있다는 것은 셀 수 있으므로 사실이지만, 그것으로 "이름 기반 인식이 얼마나 효과적이다"를 말할 수는 없습니다.

직접 측정한 것은 어떻게 쟀는지를 재현 가능하게 적어야 합니다.

## 10.7 이 권이 논문의 어디가 되는가

정리하면 이렇습니다.

| 이 권의 장 | 논문의 어디 |
|---|---|
| 고전 | 배경 절, 그리고 설정값의 근거 |
| mechanism 계열 | related work 첫 소절, 그리고 시뮬레이터 평가의 정당화 |
| behavior 계열 | related work 둘째 소절, 그리고 주장의 핵심 논증 |
| 학습된 scheduler | related work 셋째 소절 |
| LLM 계열 | related work 넷째 소절, 가장 길게 |
| 이름 표 | related work 다섯째 소절, 그리고 실험 조건의 근거 |
| 평가 도구 | 데이터셋 절의 첫 문단 |
| 지형도 | 서론 또는 related work의 그림 하나 |

**그리고 이 권 전체가 하나의 문장으로 수렴합니다.**

지형도의 오른쪽 아래 칸, 이름과 지식을 읽어서 신호를 만드는 자리에, 지금은 사람이 손으로 적은 표만 있습니다. 이 연구는 그 자리에 추론을 놓으려고 합니다.

---

## 10장 정리

- related work의 각 문단은 특정 반론 하나를 받아내는 자리입니다. 문단을 먼저 쓰고 반론을 생각하는 것이 아니라, 반론을 먼저 적고 그것을 받아내는 문단을 씁니다.
- 이 연구의 초고에는 실제로 소절마다 흡수하려는 반론이 메모로 적혀 있고 제출 전에 지우라고 표시되어 있습니다.
- 소절 순서에도 이유가 있습니다. 전제가 되는 실행 계층을 맨 앞에, 진짜 비교 상대인 이름 표를 맨 뒤에 둡니다. 가운데는 읽는 채널이 점점 이 연구에 가까워지는 순서입니다.
- 반대편의 가장 강한 버전을 후하게 다뤄야 논증이 섭니다. 약하게 그려놓고 이기면 심사자가 알아봅니다.
- 서론과 related work가 어긋나면 안 됩니다. 심사자는 두 절을 대조해서 읽습니다.
- 심사 없이 올라간 원고는 제목, 저자, 길이, 게재 여부가 바뀝니다. 이 권을 쓰는 동안에도 그런 사례를 여럿 확인했습니다. 제출 직전에 다시 확인하는 절차가 필요합니다.
- 논문 원문을 읽은 것과 저자들의 저장소를 읽은 것을 구분해서 적어야 합니다. 저장소의 설명을 논문의 초록처럼 인용하면 안 됩니다.
- 인용 등급을 지켜야 합니다. 배포된 소프트웨어의 문서는 존재 주장만 뒷받침합니다.

---

# 11장 · 용어 정리

이 권에서 나온 용어와 시스템 이름을 모았습니다.

## 논문과 학계

| 용어 | 뜻 |
|---|---|
| **abstract** | 논문 전체를 열 문장 정도로 압축한 것. 스스로 내세우는 성적표가 여기 있다 |
| **baseline** | 성능을 비교하는 기준 대상. 무엇을 골랐느냐가 결과 해석의 절반 |
| **artifact evaluation** | 논문과 별도로 코드와 데이터를 심사하는 절차 |
| **workshop** | 학회에 붙어 열리는 소규모 행사. 짧고 심사가 가벼우며 아이디어 단계의 연구를 받는다 |
| **preprint** | 심사 전에 공개된 원고. 판본이 계속 바뀔 수 있다 |
| **related work** | 이 연구가 앉을 자리가 비어 있음을 증명하는 절 |

## 이 연구의 인용 규율

| 용어 | 뜻 |
|---|---|
| **scholarly** | 심사를 거친 학술 문헌. 실험적, 행동적, 통계적 주장을 뒷받침할 수 있다 |
| **deployed-system** | 배포된 소프트웨어의 문서나 저장소. 존재 주장만 뒷받침한다 |
| **measurement** | 직접 측정한 값. 재현 가능하게 기록해야 한다 |

## 알고리즘과 시스템

| 용어 | 뜻 |
|---|---|
| **CTSS** | 1962년에 발표된 초기 timesharing 시스템. multilevel feedback의 원조로 인용된다 |
| **EDF** | 마감이 가장 임박한 job을 먼저 실행. utilization 합이 1 이하일 때 그리고 그때만 모든 마감을 지킨다 |
| **rate monotonic** | period가 짧은 작업에 높은 priority를 고정으로 주는 방식. 작업 수가 많으면 70퍼센트 근처에서 막힌다 |
| **lottery scheduling** | ticket을 나눠 주고 추첨으로 고르는 proportional share 방식 |
| **EEVDF** | 각 task에 가상의 deadline을 두고 이른 순서로 고르는 fair-share 방식. 지금 Linux의 기본 |
| **voo-doo constant** | 이론으로 정할 수 없고 경험으로 정하는 설정값 |

## 정책 교체 계층

| 용어 | 뜻 |
|---|---|
| **ghOSt** | scheduling 결정을 user space로 위임하고 kernel이 transaction으로 실행하는 틀 |
| **enclave** | ghOSt에서 기계를 나눈 구역. core 일부와 그것을 담당하는 agent와 task들의 묶음 |
| **BPF** | kernel 안에서 사용자 프로그램을 안전하게 돌리는 장치. 실행 전에 검사를 거친다 |
| **sched_ext** | BPF로 scheduler를 정의하고 실행 중에 켜고 끄는 표준 Linux 기능 |
| **scx** | sched_ext 위에 올라간 정책 구현들을 모은 공식 저장소 |
| **scx_lavd** | 지연 민감도를 측정해 가상 deadline에 반영하는 정책. 게임 workload에서 출발했다 |

## 학습과 언어 모델 계열

| 용어 | 뜻 |
|---|---|
| **Decima** | 강화학습으로 cluster 작업 배치를 배운 연구. 작업 의존 그래프를 모델 입력으로 표현했다 |
| **FIRM** | microservice 환경에서 목표 응답 시간 위반의 원인을 찾아 자원을 재배분하는 연구 |
| **Park** | 시스템 문제에 강화학습을 적용하기 위한 실험 환경. 열두 개 문제를 묶었다 |
| **ASA** | 인식한 뒤 전문 정책을 고르는 연구. 이 연구와 골격이 같고 채널이 다르다 |
| **SchedCP** | 언어 모델 에이전트가 scheduler를 설정하거나 생성하는 제어 계층. 가장 가까운 선행 연구 |
| **Kgent** | 자연어로 kernel 확장을 작성하게 하는 연구. 만들어낸 코드를 검증기로 확인한다 |
| **semantic gap** | kernel 정책이 응용의 필요를 이해하지 못하는 간극. 이 연구와 SchedCP가 공유하는 문제 인식 |
| **hot path** | 매 결정마다 지나가는 실행 경로. 여기에 느린 것을 두면 시스템이 멈춘다 |
| **control plane** | 결정 경로 바깥에서 느리게 도는 층. 언어 모델이 놓이는 자리 |

## 배포된 이름 표

| 용어 | 뜻 |
|---|---|
| **Game Mode** | 게임 실행이 감지되면 자원을 몰아주는 Windows 기능 |
| **ananicy** | 프로세스 이름으로 표를 뒤져 우선순위를 조정하는 Linux 데몬 |
| **rules catalog** | 그 데몬이 참조하는 이름과 분류의 목록. 커뮤니티가 손으로 관리한다 |

## 평가 도구

| 용어 | 뜻 |
|---|---|
| **hackbench** | 서로 통신하는 task를 대량으로 만들어 전체 완료 시간을 재는 도구 |
| **schbench** | 깨움 지연, 요청 지연, 초당 처리량을 백분위수로 보고하는 도구 |
| **interbench** | 대화형 작업을 흉내 내고 지연과 흔들림과 마감 달성률을 재는 도구 |
| **rt-app** | 작업 모델을 JSON으로 기술해 주기적 부하를 만드는 도구 |

---

## 이 권을 다 읽었으면

**계보 확인**

- 네 갈래의 연구 흐름을 각각 한 문단으로 설명할 수 있다.
- 각 갈래가 어디서 멈췄는지, 그것이 성능의 문제인지 채널의 문제인지 구분해서 말할 수 있다.
- 지형도의 두 축을 그리고 각 칸에 연구를 배치할 수 있다.

**비판적 독해 확인**

- 논문의 evaluation을 읽을 때 무엇을 먼저 의심해야 하는지 말할 수 있다.
- "저 연구가 이미 했다"는 반론에 대해, 성능 논증과 채널 논증이 왜 다른 힘을 갖는지 설명할 수 있다.
- 배포된 소프트웨어의 문서로 뒷받침할 수 있는 주장과 없는 주장을 구분할 수 있다.

**쓰기 확인**

- related work의 각 문단이 어떤 반론을 흡수하는지 표로 정리할 수 있다.
- 가장 가까운 선행 연구와의 차이를 세 가지로 나눠 말할 수 있다.
- 인용을 세 등급으로 나누고 각 등급의 표기 방식을 말할 수 있다.

다음 권에서는 이 연구 자체를 봅니다. 무엇을 주장하고, 그 주장이 어떤 고리들로 되어 있고, 각 고리가 어떻게 무너질 수 있는지입니다.
