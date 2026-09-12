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

세 번째 표시는 두 가지 모습으로 나타납니다. **확인 필요**는 아직 확인하지 못한 자리이고, **확인한 방식**은 같은 표시가 해소된 자리입니다. 뒤엣것에는 **어느 판본을 언제 어디서 읽었는지**가 적혀 있습니다.

이 권의 인용문은 원칙적으로 1차 자료 원문에서 읽은 것입니다. 판본이 여럿인 문헌은 어느 판본의 문장인지를 문장마다 구분했습니다.

**확인 필요** 표시가 남은 자리는 한 군데뿐입니다. 게임 모드가 게임 중에 업데이트나 알림을 미루는지에 대한 것이고, 제조사 문서에서 그 서술을 찾지 못했습니다. 그 자리에 무엇을 확인해야 하는지와 왜 확인하지 못했는지가 함께 적혀 있습니다.

그 밖에 확정하지 못한 것이 하나 더 있습니다. 한 논문의 게재 학회가 저자들의 저장소에만 적혀 있고 논문집 쪽 서지 정보를 확인하지 못했습니다. 그 자리에도 무엇이 확정되지 않았는지를 적어뒀습니다.

그리고 논문이 아닌 자료를 인용한 곳이 있습니다. 저자들의 공개 저장소, 제품 문서, 발표 자료입니다. 그런 곳은 **논문이 아니라는 것을 그 자리에서 밝히고** 씁니다. 저장소의 설명 문구를 논문의 초록인 것처럼 인용하면 안 되기 때문입니다.

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

그리고 한 가지를 덧붙입니다. **찾아봤는데 없더라는 것도 확인의 결과입니다.** 어떤 문서에 어떤 내용이 있을 것이라 기대하고 열었는데 없었다면, 그것은 실패가 아니라 결론입니다. "아직 확인하지 못했다"와 "확인했고 거기에 없다"는 전혀 다른 진술이고, 뒤엣것은 심사자가 직접 검증할 수 있는 주장입니다. 이 권에서 실제로 그런 경우를 만나게 됩니다.

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
- 찾아봤는데 없더라는 것도 확인의 결과입니다. "아직 확인하지 못했다"와 "확인했고 거기에 없다"는 다른 진술이고, 뒤엣것은 심사자가 직접 검증할 수 있는 주장입니다.

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

### 논문이 이 알고리즘을 왜 꺼내는가

먼저 맥락이 중요합니다. 이 논문은 "더 빠른 scheduler를 만들었다"고 말하지 않습니다. **포화 상황을 어떻게 견딜 것인가**를 말합니다.

> "one is inevitably faced with the problem of system saturation where the total size of active user programs exceeds that of the high-speed memory or there are too many active user programs to maintain an adequate response at each user console"

활성 프로그램 전체의 크기가 고속 memory를 넘어서거나, 활성 프로그램이 너무 많아서 각 단말기에서 적당한 응답을 유지할 수 없게 되는 포화 문제를 반드시 마주치게 된다는 것입니다.

그리고 그때 단순한 round-robin을 쓰면 무슨 일이 벌어지는지 적습니다.

> "If the strategy near saturation is to execute the simple round-robin of all users, then there is an abrupt collapse of service due to the sudden onset of the large amount of time required to swap programs in-and-out of the secondary memory such as a disc or drum unit."

포화 근처에서 모든 사용자를 단순 round-robin으로 돌리면, 프로그램을 보조 기억장치로 넣고 빼는 데 드는 시간이 갑자기 커지면서 **서비스가 급격히 붕괴한다**는 것입니다.

논문이 원하는 것은 붕괴가 아니라 완만한 악화입니다.

> "a good design for the system is to have a saturation procedure which gives graceful degradation of the response time and effective real-time computation speed of the large and long-running users"

크고 오래 도는 사용자의 응답 시간과 실효 계산 속도가 **완만하게 나빠지는** 포화 처리 절차를 두는 것이 좋은 설계라는 것입니다.

**여기서 읽어야 할 것이 있습니다.** 이 알고리즘의 목적은 평균을 개선하는 것이 아니라, 나빠질 때 누가 먼저 나빠지는지를 정하는 것입니다. 크고 오래 도는 쪽이 먼저 양보하고, 작고 짧은 쪽이 보호받습니다.

### 처음 어느 단계에 놓이는가

논문은 먼저 기본 발상을 적습니다.

> "The basis of the multi-level scheduling algorithm is to assign each user program as it enters the system to be run (or completes a response to a user) to an ℓth level priority queue."

시스템에 들어오는 프로그램, 그리고 **사용자에게 응답을 마친 프로그램**을 ℓ번째 단계의 queue에 배치한다는 것입니다. 응답을 마치면 다시 배치된다는 대목이 중요합니다. 한 번 내려간 프로그램이 영원히 밑에 머무는 구조가 아닙니다.

그럼 처음 들어올 때 어느 단계일까요.

> "Programs are initially entered into a level ℓ₀, corresponding to their size such that … where w_p is the number of words in the program, w_q is the number of words which can be transmitted in and out of the high-speed memory from the secondary memory in the time of one quantum, q, and the bracket indicates 'the integral part of'."

수식으로는 ℓ₀ = [log₂([w_p / w_q] + 1)]입니다. w_p는 프로그램의 word 수, w_q는 quantum 하나의 시간 동안 고속 memory와 보조 기억장치 사이로 옮길 수 있는 word 수이고, 대괄호는 정수부를 뜻합니다.

**풀어 말하면 이렇습니다. 처음 단계는 프로그램의 크기로 정해집니다.** 정확히는 크기를 "옮기는 데 quantum 몇 개가 필요한가"로 환산한 값입니다. 작은 프로그램은 위쪽 단계에서 시작하고, 큰 프로그램은 아래쪽 단계에서 시작합니다.

앞 권에서 MLFQ를 배울 때는 "새 job은 무조건 최상위에서 시작한다"고 했습니다. **원조는 다릅니다.** 크기를 보고 시작 위치를 정합니다. 교과서가 정리한 형태와 원 논문이 다른 지점이고, 인용할 때 주의해야 할 대목입니다.

왜 크기로 정할까요. 논문이 그 이유를 결과로 보여줍니다.

> "Because a program is always operated for a time greater than or equal to the swap time (i.e. the time required to move the program in and out of secondary memory), it follows that the computational efficiency never falls below one-half."

프로그램이 항상 **swap 시간 이상으로 실행되도록** 시작 단계를 정했기 때문에, 계산 효율이 절반 밑으로 떨어지지 않는다는 것입니다. 큰 프로그램을 위쪽 단계에 놓으면 짧게 돌리고 바로 내보내게 되어, 일하는 시간보다 옮기는 시간이 더 커집니다. 그걸 막는 규칙입니다.

논문은 이 절반이라는 값이 조정 가능하다고 덧붙입니다.

> "(Clearly, this fraction is adjustable in the formula for the initial level, ℓ₀.)"

### 각 단계에서 얼마나 주는가

> "The process starts with the time-sharing supervisor operating the program at the head of the lowest level occupied queue, ℓ, for up to 2^ℓ quanta of time"

비어 있지 않은 가장 낮은 번호의 queue에서 맨 앞 프로그램을 꺼내, **2^ℓ개의 quantum만큼** 돌린다는 것입니다.

단계 번호가 하나 올라갈 때마다 시간이 **두 배**가 됩니다. 앞 권에서 본 "아래로 갈수록 긴 quantum"이 여기서 처음 나왔고, 그 증가가 구체적으로 2의 거듭제곱입니다.

quantum 자체의 크기에 대해서도 한 줄 적습니다.

> "Ordinarily the time of a quantum, being the basic time unit, should be as small as possible without excessive overhead losses when the supervisor switches from one program in high-speed memory to another."

전환 부담이 과해지지 않는 선에서 최대한 작아야 한다는 것입니다. 앞 권에서 slice 길이의 상충으로 배운 그 내용입니다.

그리고 논문은 당시 기계의 실제 값을 적어둡니다. IBM 7090에 대해 **q = 16밀리초**이고, 근거는 "전환 부담 1퍼센트 기준"입니다.

> "q = 16 m.s. (based on 1% switching overhead)"

### 단계 사이를 오가는 조건

네 가지가 있습니다.

**내려가는 조건.**

> "and then if the program is not completed (i.e. has not made a response to the user) placing it at the end of the ℓ+1 level queue"

주어진 2^ℓ quanta를 다 썼는데도 완료되지 않았으면, 즉 **사용자에게 응답을 내놓지 못했으면** 다음 단계 queue의 끝으로 보냅니다.

여기서 "완료"의 정의가 중요합니다. 계산이 끝난 것이 아니라 **사용자에게 응답한 것**입니다. 앞 권에서 MLFQ의 강등 규칙을 "시간을 다 쓰면 내려간다"로 배웠는데, 원조의 기준은 그보다 사용자 쪽에 붙어 있습니다.

**다음 단계로 넘어가는 조건.**

> "If there are no programs entering the system at levels lower than ℓ, this process proceeds until the queue at level ℓ is exhausted; the process is then iteratively begun again at level ℓ+1, where now each program is run for 2^(ℓ+1) quanta of time."

더 낮은 단계에 새로 들어오는 프로그램이 없으면 현재 단계의 queue를 비울 때까지 진행하고, 그다음 단계로 내려가서 두 배의 시간으로 같은 일을 반복합니다.

**끼어드는 조건.**

> "If during the execution of the 2^ℓ quanta of a program at level ℓ, a lower level, ℓ′, becomes occupied, the current user is replaced at the head of the ℓth queue and the process is reinitiated at level ℓ′."

어떤 프로그램이 2^ℓ quanta를 쓰는 도중에 더 낮은 단계가 채워지면, 지금 프로그램을 자기 queue의 **맨 앞**에 되돌려 놓고 낮은 단계부터 다시 시작합니다. 맨 뒤가 아니라 맨 앞이라는 점이 중요합니다. 끼어들기 때문에 손해를 보지는 않습니다.

**크기가 바뀌는 조건.**

> "Similarly, if a program of size w_p at level ℓ, during operation requests a change in memory size from the time-sharing supervisor, then the enlarged (or reduced) version of the program should be placed at the end of the ℓ″ queue"

실행 중에 memory 크기 변경을 요청하면, 바뀐 크기로 단계를 다시 계산해서 그 queue의 끝에 놓습니다.

**그리고 하나 더 있습니다. 입출력을 기다리는 프로그램입니다.**

> "One systematic method of handling this case is to modify the scheduling algorithm so that programs which become dormant at level ℓ are entered into the queue at level ℓ+1. The scheduling algorithm proceeds as before with the dormant programs continuing to cascade but not operating when they reached the head of a queue."

ℓ단계에서 휴면 상태가 된 프로그램은 ℓ+1 queue로 넣고, 계속 아래로 흘러내리되 queue의 맨 앞에 와도 실행하지는 않습니다.

**이 규칙이 지금의 MLFQ와 반대 방향입니다.** 앞 권에서 배운 현대 MLFQ는 스스로 잠든 task의 우선순위를 유지하거나 올려줍니다. 대화형 작업을 우대하기 위해서입니다. 원조는 잠든 프로그램을 아래로 내립니다. 목적이 달랐기 때문입니다. 1962년에는 고속 memory에서 누구를 먼저 내보낼지를 정하는 것이 급했고, 논문은 바로 그 용도로 이 규칙을 씁니다.

> "Whenever a program must be removed from high-speed memory, a program is selected from the end-of-the-queue of the highest occupied level number."

### 논문이 스스로 자랑하는 성질

다섯 개의 결론 중 두 개가 이 연구와 직접 통합니다.

**첫째, 긴 작업은 길다는 것을 스스로 증명해야 합니다.**

> "It is an important feature of the algorithm that long runs must in effect prove they are long so that programs which have an unexpected demise are detected quickly."

**둘째, 분류가 전적으로 자동입니다.**

> "In the multi-level algorithm the level classification procedure for programs is entirely automatic, depending on performance and program size rather than on the declarations (or hopes) of each user."

단계 분류가 **각 사용자의 선언(또는 희망)이 아니라 성능과 프로그램 크기에 따라** 자동으로 이루어진다는 것입니다.

> **이 연구에서는.** 두 번째 문장이 이 연구가 서 있는 자리를 1962년 논문이 먼저 짚은 장면입니다. 앞 권에서 프로그램의 자기 선언을 믿을 수 없다는 것을 봤는데, 이 논문은 그것을 설계 원칙으로 명시하고 declarations 옆에 hopes라는 단어를 나란히 적었습니다. 선언은 희망이라는 것입니다.
>
> 그리고 이 연구는 그 원칙을 그대로 유지합니다. 언어 모델은 프로그램의 자기 선언을 읽지 않습니다. 프로그램이 무엇인지를 밖에서 판단합니다. 행동 관찰에서 판단을 가져오던 자리를 세상에 대한 지식으로 바꾸는 것이지, 프로그램에게 물어보는 것이 아닙니다.

> **논문으로.** 이 대비가 related work의 첫 문단에 쓸 수 있는 재료입니다. 자동 분류라는 원칙은 1962년부터 있었고 지금도 유효한데, **그 자동 분류가 읽을 수 있는 것이 행동과 크기뿐이었다**는 것이 이 연구가 지적하는 빈칸입니다.

> **확인한 방식.** 이 절의 인용문은 AFIPS 1962 논문집 335–344쪽을 촬영한 PDF에서 읽었습니다(2026-09-12 확인). 그 PDF의 문자 인식 결과가 수식 기호를 흐리게 옮기는 구간이 있어서, 같은 문장을 MIT가 공개한 저자 감수 전사본과 대조해 기호를 확정했습니다. 위의 ℓ, ℓ₀, 2^ℓ 표기가 그렇게 확정한 부분입니다.

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

주의할 점이 하나 있습니다. **연도가 1995년입니다.** 1996년으로 잘못 적힌 인용을 종종 보게 됩니다.

원문을 열어보면 그 착오가 어디서 나오는지가 보입니다. 표지에 보고서 번호 TR-95-22가 찍혀 있고, 그 아래 각주에 이렇게 적혀 있습니다.

> "Revised January 26, 1996."

**1995년 보고서를 1996년 1월에 개정했습니다.** 개정일만 보고 연도를 적으면 1996년이 됩니다. 원문을 열지 않고 2차 자료에서 옮기면 어느 쪽이 맞는지 알 수 없습니다.

### 무엇을 풀려던 문제였나

논문의 서론이 당시 상황을 둘로 나눕니다. 한쪽은 proportional share, 즉 각 client에게 몫을 주고 그 비율대로 자원을 나누는 계열입니다. 다른 한쪽은 real-time 계열로, 사건이 주기적으로 도착하고 각 사건에 예상 처리 시간과 마감이 붙어 있다고 봅니다.

그리고 둘의 장단을 이렇게 정리합니다.

> "While in general the proportional share schedulers tend to be more flexible and to ensure a graceful degradation in overload situations, real-time based schedulers tend to offer better guarantees for applications with timeliness constraints, such as multimedia."

비율 배분 계열이 더 유연하고 과부하에서 완만하게 나빠지는 반면, real-time 계열은 시간 제약이 있는 응용에 더 나은 보장을 준다는 것입니다.

앞 권에서 EDF가 과부하에서 연쇄적으로 무너진다고 배웠는데, 이 문장이 그 대비의 반대편입니다.

그리고 real-time 계열의 한계를 짚습니다.

> "Although real-time based schedulers provide better support for multimedia, they cannot be easily extended to support batch applications. The main reason is that while multimedia and interactive applications fit the event-driven model implicitly assumed by these schedulers, batch applications do not."

multimedia와 대화형 응용은 사건 기반 모형에 맞지만 **batch 응용은 맞지 않는다**는 것입니다. 배경에서 계산만 도는 작업에는 "사건"도 "마감"도 없습니다.

이 논문이 하려는 것은 두 계열을 하나로 묶는 것입니다.

> "our algorithm provides a unified approach for scheduling continuous media, interactive and batch applications"

### 네 개의 개념

이 계열을 이해하려면 네 단어를 알아야 합니다. 논문의 서론에 네 개가 한 문단에 다 나옵니다.

**virtual time.** 실제 시계와 별개로 도는 시계입니다. 논문의 정의는 적분으로 되어 있습니다.

> "Similarly to [31] and [23] we define the system virtual time as V(t) = ∫₀ᵗ 1 / (Σ_{j∈A(τ)} w_j) dτ"

A(τ)는 그 시점에 활성 상태인 client들의 집합이고 w_j는 각자의 가중치입니다. 그러니까 **활성 client들의 가중치 합의 역수를 시간에 대해 쌓아 올린 것**이 virtual time입니다.

논문이 그 성질을 말로 풀어줍니다.

> "We note that the virtual time increases at a rate inverse proportional to the sum of the weights of all active clients. Notice that when the competition increases the virtual time slows down, while when the competition decreases it accelerates."

**경쟁이 심해지면 virtual time이 느려지고, 경쟁이 줄면 빨라집니다.**

왜 이렇게 만들까요. 논문이 직관을 붙입니다.

> "Intuitively, the flow of the virtual time changes to 'accommodate' all active clients in one virtual time unit. That is, the size of a virtual time unit is modified such that in the corresponding fluid-flow system each active client i receives w_i real-time units during one virtual time unit."

virtual time 한 단위 안에 활성 client 전부가 들어가도록 시계가 늘었다 줄었다 한다는 것입니다. virtual time 한 단위 동안 각 client는 자기 가중치만큼의 실제 시간을 받습니다.

**풀어 말하면 virtual time은 "공평한 세계의 시계"입니다.** 웹 서비스에 비유하면, 접속자가 열 명일 때와 백 명일 때 각자가 받아야 할 몫이 다른데, 그 몫을 매번 다시 계산하는 대신 시계 자체를 인원수에 맞춰 늘렸다 줄였다 하는 것입니다. 그러면 "지금까지 자기 몫을 다 받았는가"를 시계 한 번 읽는 것으로 판정할 수 있습니다.

**virtual eligible time과 virtual deadline.** 논문은 이 둘을 한 문장에 함께 정의합니다.

> "Based on the client share and on the service time that the client has already received, the scheduler associates to each client's request a virtual eligible time and a virtual dead line which are the corresponding starting and finishing times of servicing the request in the fluid-flow model."

각 요청에 두 시각이 붙는데, 그 둘은 **이상적인 흐름 모형에서 그 요청을 처리하기 시작하는 시각과 끝내는 시각**이라는 것입니다. 그리고 그 시각은 client의 몫과 **이미 받은 처리 시간**으로 정해집니다.

여기서 eligible이라는 단어의 의미가 나옵니다.

> "A request is said to be eligible if its virtual eligible time is less than or equal to the current virtual time."

자기 eligible time이 현재 virtual time 이하이면 그 요청은 **자격을 얻었다**는 것입니다. 아직 그 시각이 오지 않았으면 자격이 없고, 마감이 아무리 급해도 고려 대상이 아닙니다.

그리고 알고리즘 전체가 한 문장으로 끝납니다.

> "The algorithm simply allocates a new time quantum to the client that has the eligible request with the earliest virtual deadline."

**자격을 얻은 요청 중에서 virtual deadline이 가장 이른 것에 다음 quantum을 준다.** 이름이 그대로 알고리즘입니다. Earliest Eligible Virtual Deadline First.

논문은 eligible time이 자기 고유의 기여라고 밝힙니다.

> "We note that while the concept of virtual deadline is also employed by other proportional-share algorithms […], the concept of eligible time is a unique feature of our algorithm (which, as we will show, plays a decisive role in improving the allocation accuracy)."

**virtual deadline은 다른 비율 배분 알고리즘에도 있지만 eligible time은 이 알고리즘의 고유 기능**이라는 것입니다.

왜 자격 검사가 필요한지는 짐작할 수 있습니다. 자격 검사가 없으면, 한동안 자고 있다가 깨어난 client가 밀린 몫을 근거로 마감을 아주 이르게 잡고 자원을 한꺼번에 가져갈 수 있습니다. 앞 권에서 fair-share 계열의 깨어남 처리를 다룰 때 나왔던 그 문제입니다. eligible time은 "받아야 할 몫이 실제로 도착한 시점"을 정해서 그 몰아 쓰기를 막습니다.

**lag.** 마지막 개념이고, 이 논문의 주인공입니다.

> "Due to quantization, in a system in which the resource is allocated in discrete time quanta (as it is in ours), it is not possible for a client to always receive exactly the service time it is entitled to. The difference between the service time that a client should receive at a time t, and the service time it actually receives is called service time lag."

자원을 이산적인 quantum 단위로 나눠 주는 이상 각 client가 받아야 할 만큼 정확히 받는 것은 불가능하고, **받아야 할 처리 시간과 실제로 받은 처리 시간의 차이**를 service time lag이라 부른다는 것입니다.

식으로는 lag_i(t) = S_i(t⁰ᵢ, t) − s_i(t⁰ᵢ, t)입니다. 앞의 항이 이상적인 세계에서 받았어야 할 양, 뒤의 항이 실제로 받은 양입니다.

lag이 양수이면 덜 받은 상태, 음수이면 더 받은 상태입니다.

그리고 논문이 lag을 왜 주인공으로 삼는지 밝힙니다.

> "Since the service time lag determines both the throughput accuracy and the system predictability, we use it as the main parameter in characterizing our proportional resource allocation algorithm."

lag이 처리량의 정확도와 시스템의 예측 가능성을 **둘 다** 결정하기 때문에, 이 값을 알고리즘을 특징짓는 주 지표로 쓴다는 것입니다.

### 이상과 실제의 차이에 대한 보장

이제 이 논문이 증명하는 것이 무엇인지 볼 수 있습니다. 초록에 한 문장으로 있습니다.

> "we show that in steady conditions our algorithm guarantees that the difference between the service time that a client should receive in the idealized system and the service time it actually receives in the real system is bounded by the size q of a time quantum"

**이상적인 시스템에서 받았어야 할 처리 시간과 실제 시스템에서 받은 처리 시간의 차이가 quantum 하나의 크기 q로 묶인다**는 것입니다.

본문의 정리는 조금 더 일반적인 형태입니다.

> "Theorem 1 The lag of any active client k in a steady system is bounded as follows, −r_max < lag_k(d) < max(r_max, q), where r_max represents the maximum duration of any request issued by client k. Moreover, these bounds are asymptotically tight."

각 client의 lag이 그 client가 내는 **요청의 최대 길이** r_max와 quantum 크기 q로 묶인다는 것입니다. 그리고 그 한계는 점근적으로 빠듯합니다.

초록의 q라는 숫자는 요청이 quantum보다 길지 않은 특수한 경우입니다.

> "Corollary 2 Consider a steady system and a client k such that no request of client k is larger than a time quantum. Then at any time t, the lag of client k is bounded as follows: −q < lag_k(t) < q."

그리고 논문은 이 한계가 자기 알고리즘만의 성취가 아니라 **누구도 넘을 수 없는 한계**임을 따로 증명합니다.

> "Lemma 5 Given any steady system with time quanta of size q and any proportional share algorithm, the lag of any client is bounded by −q and q."

quantum 크기 q인 시스템에서는 **어떤 비율 배분 알고리즘이든** lag이 −q와 q 사이라는 것입니다. 그러니까 EEVDF의 보장은 그 이론적 한계에 닿아 있습니다.

**논증의 형태를 눈여겨보세요.** "우리가 제일 좋다"가 아니라 "이 값이 최선이고 우리가 그 값이다"입니다. 앞 장에서 본 EDF의 if and only if와 같은 종류의 논증입니다.

### 인용할 때의 범위

정리 하나에 steady라는 조건이 붙어 있는데, 이게 무슨 뜻인지 알아야 인용할 수 있습니다. 논문의 정의입니다.

> "Definition 2 An interval is said to be steady if all the events occurring in that interval involve only clients with zero lag."

그 구간에서 일어나는 모든 사건이 **lag이 0인 client에 대해서만** 일어나면 그 구간을 steady라고 부른다는 것입니다. 사건이란 client가 들어오거나, 나가거나, 가중치를 바꾸는 일입니다.

**그러니까 위의 한계는 아무 때나 성립하는 것이 아닙니다.** lag이 0이 아닌 client가 경쟁에서 빠지거나 합류하면 조건이 깨집니다. 논문은 그 경우를 뒤에서 따로 다루는데, 인용할 때는 조건을 함께 적어야 합니다.

> **이 연구에서는.** 이 계열의 개념이 이 연구에 직접 쓰이지는 않습니다. 이 연구의 시뮬레이터가 돌리는 알고리즘 넷 중 fair-share 계열이 하나 있지만, 그것은 누적 사용량 기반의 단순한 형태이고 eligible time이나 lag 한계를 구현하지 않습니다.
>
> 그럼에도 이 문헌이 필요한 이유가 둘입니다. 첫째, 지금 Linux의 기본 scheduler가 이 알고리즘이므로 비교 대상을 서술할 때 원 문헌이 필요합니다. 둘째, 앞 장에서 본 ASA의 평가가 기본 scheduler로 삼은 것이 정확히 이것입니다. "기본값을 이겼다"는 주장을 읽으려면 그 기본값이 무엇을 보장하는지를 알아야 합니다.

> **논문으로.** 이 계열을 related work에서 다룰 때 지켜야 할 선이 여기 있습니다. 이 논문이 보장하는 것은 **비율 배분의 정확도**이지 대화형 응답성이 아닙니다. lag 한계는 "누구도 자기 몫에서 quantum 하나 이상 벗어나지 않는다"는 말이고, "사용자가 빠르다고 느낀다"는 말이 아닙니다. 둘을 섞으면 인용 범위를 넘습니다.

> **확인한 방식.** 이 절의 인용문은 저자가 공개한 기술보고서 PDF 전문에서 읽었습니다(2026-09-12 확인). 표지의 TR-95-22, Old Dominion University 소속 표기, 그리고 개정일 각주를 함께 확인했습니다.

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

- CTSS를 발표한 1962년 논문이 timesharing과 multilevel feedback의 출발점입니다. 이 논문의 multi-level scheduling algorithm은 성능 개선이 아니라 포화 시의 완만한 악화를 목적으로 제시됩니다. 처음 배치되는 단계는 프로그램의 크기를 swap 비용으로 환산해서 정하고, ℓ단계에서는 2^ℓ개의 quantum을 주며, 사용자에게 응답하지 못한 채 그 시간을 다 쓰면 아래 단계로 내려갑니다. 더 낮은 단계가 채워지면 현재 프로그램은 자기 queue의 맨 앞에 되돌아가고, 입출력을 기다리는 프로그램은 아래로 흘러내리되 실행되지 않습니다.
- 1973년 Liu와 Layland의 논문이 EDF의 이론적 기반입니다. 마감이 다음 주기의 시작이라는 가정, 그리고 utilization 합이 1 이하일 때 그리고 그때만 EDF가 성공한다는 정리가 여기 있습니다. 고정 priority 방식은 작업 수가 많으면 70퍼센트 근처까지 떨어질 수 있다는 대비도 초록에 있습니다.
- 이 논문은 다섯 가지 가정 아래 단일 프로세서의 주기적 작업만 다룹니다. 과부하 상황은 다루지 않으므로 그 서술에 인용할 수 없습니다.
- 1994년 Waldspurger와 Weihl의 논문이 lottery scheduling의 원조입니다. 소비율이 할당된 몫에 비례한다는 것이 보장이고, 10밀리초 quantum이면 1초 이하 구간에서도 합리적인 수준의 공정성이 나온다고 스스로 적었습니다. 부류 사이의 비율은 말하지 않습니다.
- 원조와 교과서가 다른 지점이 둘입니다. 원조는 새 프로그램을 최상위가 아니라 크기에 따른 단계에 놓고, 잠든 프로그램을 우대하는 대신 아래로 내립니다. 인용할 때 구분해야 합니다.
- 이 논문은 단계 분류가 "각 사용자의 선언(또는 희망)이 아니라 성능과 프로그램 크기에 따라" 전적으로 자동이라고 명시합니다. 프로그램의 자기 선언을 믿지 않는다는 원칙이 1962년부터 있었고, 그 자동 분류가 읽을 수 있는 것이 행동과 크기뿐이라는 것이 이 연구가 지적하는 빈칸입니다.
- 1995년 EEVDF 기술보고서가 지금 Linux scheduler의 기반입니다. 연도를 1996년으로 잘못 적는 인용이 흔한데, 원문 표지의 각주에 1996년 1월 개정이라고 적혀 있는 것이 그 착오의 출처입니다.
- EEVDF의 네 개념은 이렇습니다. virtual time은 활성 client 가중치 합의 역수를 쌓은 시계라서 경쟁이 심하면 느려지고 줄면 빨라집니다. virtual eligible time과 virtual deadline은 이상적 흐름 모형에서 그 요청을 처리하기 시작하고 끝내는 시각이며, eligible time이 현재 virtual time 이하일 때만 그 요청이 후보가 됩니다. lag은 받아야 할 처리 시간과 실제로 받은 처리 시간의 차이입니다.
- 알고리즘은 한 문장입니다. 자격을 얻은 요청 중 virtual deadline이 가장 이른 것에 다음 quantum을 줍니다. eligible time이 이 논문의 고유 기여이고, virtual deadline은 다른 비율 배분 알고리즘에도 있습니다.
- 보장은 lag의 한계입니다. 요청이 quantum보다 길지 않으면 lag이 −q와 q 사이에 묶입니다. 그리고 같은 논문이 그 한계가 어떤 비율 배분 알고리즘도 넘을 수 없는 값임을 따로 증명합니다. 다만 이 한계는 lag이 0인 client에 대해서만 사건이 일어나는 steady 구간의 이야기이므로, 인용할 때 조건을 함께 적어야 합니다.
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

- Humphries, J. T., Natu, N., Chaugule, A., Weisse, O., Rhoden, B., Don, J., Rizzo, L., Rombakh, O., Turner, P., & Kozyrakis, C. (2021). ghOSt: Fast & Flexible User-Space Delegation of Linux Scheduling. *Proc. SOSP '21*, 588–604. DOI 10.1145/3477132.3483542.

> **확인한 방식.** 이 절에는 두 종류의 인용문이 섞여 있고, 어느 쪽인지를 매번 밝힙니다.
>
> 하나는 **논문 원문**입니다. 저자 중 한 명이 소속 기관 페이지에 올려둔 SOSP '21 논문 PDF 전문을 읽었습니다(2026-09-12 확인). 첫 쪽에 588쪽, 마지막 쪽에 604쪽이 찍혀 있어 서지 정보의 쪽 범위도 함께 확인됐습니다.
>
> 다른 하나는 **저자들이 공개한 코드 저장소의 설명 문서**입니다. 논문에 없는 운용상의 설명이 그쪽에만 있어서, 그 부분은 저장소에서 가져왔다고 표시하고 그대로 씁니다. 저자가 같아도 논문이 아니므로 인용할 때 구분해야 합니다.

### 무엇을 하는가

논문의 초록 첫 문장입니다.

> "We present ghOSt, our infrastructure for delegating kernel scheduling decisions to userspace code. ghOSt is designed to support the rapidly evolving needs of our data center workloads and platforms."

**kernel의 scheduling 결정을 user space 코드로 위임하는 기반 구조**라는 것입니다. our라는 단어가 두 번 나오는데, 저자 대부분이 한 대형 사업자 소속이고 자기네 데이터센터를 위해 만들었다는 뜻입니다.

저자들의 저장소는 같은 시스템을 이렇게 설명합니다.

> "ghOSt is a general-purpose delegation of scheduling policy implemented on top of the Linux kernel. The ghOSt framework provides a rich API that receives scheduling decisions for processes from userspace and actuates them as transactions."

> "ghOSt is a general-purpose delegation of scheduling policy implemented on top of the Linux kernel. The ghOSt framework provides a rich API that receives scheduling decisions for processes from userspace and actuates them as transactions."

kernel 위에 얹은 범용 정책 위임 장치이고, user space에서 온 scheduling 결정을 받아서 **transaction으로 실행한다**는 것입니다.

여기서 두 단어가 핵심입니다.

**delegation, 즉 위임.** 결정을 내리는 주체가 kernel 밖으로 나갔습니다. kernel은 결정을 받아서 실행만 합니다.

**transaction.** 결정이 하나의 원자적 단위로 전달되고 적용됩니다. 데이터베이스의 transaction과 같은 발상입니다.

논문이 그 구조를 더 정확히 적습니다.

> "ghOSt's kernel side is implemented as a scheduling class, akin to the commonly used CFS class. This scheduling class provides userspace code with a rich API to define arbitrary scheduling policies. To help the agents make scheduling decisions, the kernel exposes thread state to the agents via messages and status words. The agents then instruct the kernel on scheduling decisions via transactions and system calls."

kernel 쪽은 CFS와 나란한 **scheduling class**로 구현되어 있고, kernel은 thread 상태를 message와 status word로 밖에 내보내며, agent는 transaction과 system call로 결정을 돌려보냅니다.

왜 transaction이어야 하는지도 적혀 있습니다.

> "Agents must be able to schedule both their local CPU (per-CPU case) as well as other remote CPUs (centralized case). The commit mechanism must be fast to support µs-scale policies and scale to hundreds of cores. For the per-CPU example, a syscall interface, in theory, would suffice."

**자기 CPU만 다룬다면 system call로 충분한데, 다른 CPU까지 다루려면 그것으로 부족하다**는 것입니다. 한 곳에서 기계 전체를 지휘하는 구조를 지원하려고 transaction을 도입했습니다.

### 왜 이게 큰 변화인가

논문의 초록입니다.

> "Programmers use any language to develop and optimize policies, which are modified without a host reboot. ghOSt supports a wide range of scheduling models, from per-CPU to centralized, run-to-completion to preemptive, and incurs low overheads for scheduling actions."

**어떤 언어로든 정책을 짤 수 있고, 호스트를 재부팅하지 않고 바꿀 수 있다**는 것입니다. 그리고 per-CPU에서 중앙 집중까지, 끝까지 실행하는 방식에서 선점 방식까지 넓은 범위를 지원합니다.

논문의 서론은 그 결과를 이렇게 요약합니다.

> "With ghOSt, scheduling strategies — previously requiring extensive kernel modification — can be implemented in just 10s or 100s of lines of code."

저장소는 이렇게 이어갑니다.

> "Programmers can use any language or tools to develop policies, which can be upgraded without a machine reboot."

정책을 **어떤 언어로든** 짤 수 있고, **재부팅 없이 교체할 수 있다**는 것입니다.

kernel 코드를 짜려면 C를 써야 하고, kernel 안에서는 쓸 수 있는 라이브러리가 제한되고, 실수하면 시스템 전체가 죽습니다. 그 제약이 사라집니다.

> "ghOSt supports policies for a range of scheduling objectives, from µs-scale latency, to throughput, to energy efficiency, and beyond, and incurs low overheads for scheduling actions. Many policies are just a few hundred lines of code."

**정책 하나가 몇백 줄**이라는 대목이 인상적입니다. 앞 권에서 본 MLFQ의 규칙이 여섯 줄이었던 것을 떠올리면, 알고리즘 자체는 원래 크지 않습니다. 크고 어려웠던 것은 그걸 kernel 안에 안전하게 넣는 일이었습니다.

### 왜 이런 것이 필요했나

논문의 서론이 동기를 셋으로 나눕니다. 첫째, 정책을 잘 고르면 실제로 크게 좋아집니다. 논문은 선행 연구의 수치를 그대로 인용합니다.

> "the Shinjuku request scheduler optimized highly dispersive workloads – workloads with a mix of short and long requests – improving request tail latency and throughput by an order of magnitude. The Tableau scheduler for virtual machine workloads demonstrated improved throughput by 1.6× and latency by 17× under multi-tenant scenarios. The Caladan scheduler focused on resource interference between foreground low-latency apps and background best effort apps, improving network request tail latency by as much as 11,000×."

**앞 권에서 배운 "좋은 scheduling의 정의는 상황마다 다르다"가 이 목록의 모양입니다.** 짧은 요청과 긴 요청이 섞인 상황, 여러 손님이 한 기계를 나눠 쓰는 상황, 전면 작업과 배경 작업이 부딪치는 상황. 각각에 맞춘 scheduler가 각각 큰 개선을 보고했습니다.

둘째, 그럼에도 실제로 배포하기가 어렵습니다.

> "Designing, implementing, and deploying new scheduling policies across a large fleet is an exacting task. It requires developers to design policies capable of balancing the specific performance requirements of many applications. The implementation must conform with a complex kernel architecture, and errors will, in many cases, crash the entire system or otherwise severely impede performance due to unintended side effects. Even when successful, the disruptive nature of an upgrade carries its own opportunity cost in host and application downtime. This creates a challenging conflict between risk-minimization and progress."

마지막 문장이 이 장의 요지입니다. **위험을 줄이는 것과 앞으로 나아가는 것 사이의 갈등**입니다.

셋째, 기존의 user space 해법들은 응용을 뜯어고쳐야 했습니다.

> "Prior attempts to improve performance and reduce complexity in the kernel by designing userspace solutions have significant shortcomings: they require substantial modification of application implementation"

논문은 설계 목표를 다섯 개로 정리하는데, 그중 마지막이 앞 권에서 본 문제의 언어입니다.

> "Non-disruptive updates and fault isolation. OS upgrades on a large fleet incur expensive downtime. […] Therefore, the scheduling policy should be decoupled from the host kernel and ghOSt must allow new policies to be deployed, updated, rolled-back, or even crash without incurring the machine-reboot costs."

**정책이 죽어도 기계를 재부팅하지 않아야 한다**는 것이 설계 요구사항으로 못 박혀 있습니다.

### enclave라는 구조

이 시스템은 기계를 여러 구역으로 나눌 수 있게 합니다. 논문의 서술입니다.

> "ghOSt supports multiple concurrent policies on a single machine using enclaves. A system can be partitioned into multiple independent enclaves, at CPU granularity, each of which runs its own policy. […] From a scheduling perspective, the enclaves are isolated. Partitioning makes sense especially when running different workloads on a single machine. It is often useful to set the granularity of these enclaves by machine topology, such as per-NUMA-socket or per-AMD-CCX. Enclaves also help in isolating faults, limiting the damage of an agent-crash to the enclave it belongs to."

CPU 단위로 기계를 독립된 구역으로 쪼개고, 각 구역이 자기 정책을 돌립니다. 구역 나누기의 기준으로는 기계의 지형이 유용하다고 적혀 있습니다.

저장소의 설명은 같은 것을 조금 더 구체적으로 적습니다.

> "ghOSt uses **enclaves** to group agents and the threads that they are scheduling. An enclave contains a subset of CPUs (i.e., logical cores) in a machine, the agents that embody those CPUs, and the threads in the ghOSt scheduling class that the enclave agents can schedule onto the enclave CPUs."

> "Enclaves provide an easy way to partition the machine to support co-location of policies and tenants, a particularly important feature as machines scale out horizontally to contain hundreds of CPUs and new accelerators."

core가 수백 개인 기계에서는 전체에 하나의 정책을 쓰는 것이 오히려 이상합니다. 구역을 나눠서 각 구역에 다른 정책을 두는 것이 자연스럽습니다.

### 재부팅 없는 교체가 실제로 어떻게 되는가

논문이 절차와 이유를 함께 적습니다.

> "ghOSt enables rapid deployment, since updating the scheduling policy (i.e., the agents) does not require restarting the kernel or applications. Many production services can take minutes to hours to start, particularly to populate in-memory caches. […] These long-running applications continue to run correctly during a planned agent update or an unplanned agent crash."

**왜 재부팅이 그렇게 비싼지**를 짚습니다. 서비스 하나를 띄우는 데 몇 분에서 몇 시간이 걸리고, 그 대부분이 memory 안의 cache를 채우는 시간입니다.

교체 방식은 둘입니다.

> "ghOSt achieves dynamic upgrades by either (a) replacing the agents while keeping the enclave infrastructure intact, or by (b) destroying the enclave and starting from scratch."

저장소가 첫 번째 방식의 절차를 설명합니다.

> "When you want to upgrade a policy, the agents in the new process that you launch attempt to attach to the existing enclave, waiting for the old agents running in the enclave to exit. Once the old agents exit, the new agents take over the enclave and begin scheduling."

새 정책 프로세스를 띄우면 기존 구역에 붙으려고 대기하고, 기존 것이 빠지면 인계받습니다.

논문은 인계 시점에 무엇이 오가는지까지 적습니다.

> "The new agent extracts the state of all threads in the enclave from the kernel and resumes scheduling."

새 agent가 kernel에서 그 구역의 모든 thread 상태를 꺼내 와서 이어받습니다.

### 정책이 망가지면

가장 중요한 질문입니다. user space의 프로그램에 scheduling을 맡겼는데 그게 죽으면 어떻게 되나요?

논문의 답은 세 겹입니다.

**첫째, 다른 클래스보다 낮은 우선순위에 둡니다.**

> "One of ghOSt's design goals is enabling easy adoption on existing systems. So even if a ghOSt policy is faulty, we still want ghOSt-managed threads to interact well with other threads in the system. We want to avoid ghOSt threads causing unintended consequences for other threads, such as starvation, priority inversion, deadlock, etc. We achieve this goal by assigning ghOSt's kernel scheduler class a lower priority than the default scheduler class — typically CFS — in the kernel's scheduling class hierarchy. The result is that most threads in the system will preempt ghOSt threads."

**정책이 고장 나 있어도 시스템의 대부분 thread가 ghOSt thread를 밀어낼 수 있습니다.** 피해가 구조적으로 제한됩니다. 뒤에서 볼 sched_ext의 클래스 순서도 같은 발상입니다.

**둘째, 구역을 없애면 기본 scheduler로 돌아갑니다.**

> "Destroying the enclave kills all the agents in that enclave, keeping other enclaves in the system intact, and automatically moves all threads in the destroyed enclave back to CFS. At this point, the threads are still functioning normally but are scheduled by CFS instead of ghOSt."

저장소도 같은 것을 적습니다.

> "ghOSt also recovers from scheduler failures (e.g., crashes, malfunctions, etc.) without triggering a kernel panic or machine reboot. To recover from a scheduler failure, you should generally destroy the failed scheduler's enclave and then launch the scheduler again. Destroying an enclave will kill the malfunctioning agents if necessary and will move the threads in the ghOSt scheduling class to CFS (Linux Completely Fair Scheduler) so that they can continue to be scheduled until you potentially pull them into ghOSt again."

**셋째, 감시 장치가 자동으로 그 일을 합니다.**

> "Scheduling bugs in ghOSt or in any other kernel scheduler have system-wide consequences. For example, a ghOSt thread may be preempted while holding a kernel mutex, and if it is not scheduled for too long, it could transitively stall other threads including those in CFS or other ghOSt enclaves. […] As a safety mechanism, ghOSt automatically destroys enclaves with misbehaving agents. For example, the kernel will destroy an enclave when it detects an agent has not scheduled a runnable thread within a user-configurable number of milliseconds."

**실행 가능한 thread를 정해진 밀리초 안에 배치하지 않으면 kernel이 그 구역을 없앱니다.** 시간 제한은 설정으로 정합니다.

그리고 왜 굶주림이 남의 문제가 되는지를 한 문장으로 설명한 점이 좋습니다. 어떤 thread가 kernel의 잠금을 쥔 채로 밀려나면, 그 잠금을 기다리는 다른 thread들이 전부 멈춥니다. 굶주림은 굶는 쪽만의 문제가 아닙니다.

**이 설계가 정책 실험을 가능하게 만든 핵심입니다.** 실패해도 기본값으로 돌아가면 되니까 시도해볼 수 있습니다.

### 얼마나 무거운가

논문은 이 방식이 새로 만들어내는 비용을 따로 잽니다. 2소켓 기계에서 잰 값입니다.

| 항목 | 값 |
|---|---|
| 자기 CPU의 agent에게 message 전달 | 725나노초 |
| 중앙 agent에게 message 전달 | 265나노초 |
| 자기 CPU에 thread 배치 (transaction 1개) | 888나노초 |
| 다른 CPU에 thread 배치, 전체 지연 | 1,772나노초 |
| 참고: system call 자체의 부담 | 72나노초 |
| 참고: CFS의 문맥 교환 부담 | 599나노초 |

**단위가 나노초입니다.** 앞 권에서 문맥 교환이 마이크로초 단위라고 배웠는데, 이 표가 그 값을 실제로 보여줍니다. CFS의 문맥 교환이 599나노초이고, 결정을 밖으로 빼냈을 때의 배치 비용이 888나노초입니다.

서론이 그 의미를 정리합니다.

> "We show that ghOSt's overheads are small and range from 265 ns for message delivery, several hundred nanoseconds to context-switch into an agent, and 888 ns to schedule a thread, making ghOSt scheduling overheads only slightly higher than in existing kernel schedulers. With amortization, these overheads allow just a single ghOSt agent to schedule over 2 million threads per second."

**agent 하나가 초당 200만 개의 thread를 배치할 수 있다**는 것입니다.

### 무엇으로 검증했나

논문은 네 가지 workload에서 평가합니다. 두 개는 학계의 것이고 두 개는 이 회사의 실제 서비스입니다.

**첫째, 학계 시스템과의 비교.** 짧은 요청과 긴 요청이 섞인 key-value 저장소 부하입니다. 요청의 99.5퍼센트는 4마이크로초, 0.5퍼센트는 10밀리초가 걸리도록 만들었습니다. 앞 권에서 본 "대부분 짧고 가끔 아주 긴" 분포입니다.

> "ghOSt is competitive with Shinjuku for µs-scale tail workloads, even though its Shinjuku policy is implemented in 82% fewer lines of code than the custom Shinjuku data plane system. ghOSt has slightly higher tail latencies than Shinjuku at high loads and is within 5% of Shinjuku's saturation throughput."

**82퍼센트 적은 코드로 5퍼센트 안쪽까지 따라붙었다**는 것입니다. 이기지 못했다는 사실을 그대로 적었습니다.

그리고 이 비교에서 더 중요한 대목이 따로 있습니다. 전용 시스템은 core를 점유하고 놓지 않습니다.

> "Fig. 6c shows that when we co-locate a batch application with a RocksDB workload managed by Shinjuku, the batch application cannot get any CPU resources even when the RocksDB load is low."

부하가 낮을 때도 배경 작업이 CPU를 한 톨도 못 받습니다. ghOSt 쪽은 정책 17줄을 더해서 남는 자원을 배경 작업에 주고, 꼬리 지연은 그대로 유지했습니다.

**둘째, 패킷 처리 프레임워크.** 이 회사가 실제로 쓰는 소프트 실시간 scheduler를 대체해봤습니다. 기존 방식은 이렇게 동작합니다.

> "we deploy in production MicroQuanta, a custom, soft real-time scheduler that guarantees that for any period, e.g., 1 ms, at most a quanta of time, e.g., 0.9 ms, is given to each packet processing worker. This policy ensures worker threads receive runtime while not starving other threads. However, it also leads to networking blackouts of up to 0.1 ms."

1밀리초마다 최대 0.9밀리초를 주는 방식이라서, 나머지 0.1밀리초 동안은 **네트워크가 잠깐 끊깁니다.**

결과가 흥미롭습니다. 서론은 이렇게 요약합니다.

> "leading to comparable and in some cases 5-30% better tail latency than MicroQuanta"

그런데 본문을 읽으면 그 5에서 30퍼센트가 어느 조건인지가 나오고, **반대 방향의 결과도 함께 있습니다.**

> "For 64B messages, ghOSt performs similar or 10% better than the baseline when we consider up to 99.9th percentile latency. For 99.99% and above, ghOSt latencies are up to 1.7× worse. […] For 64kB messages, ghOSt performs similarly to the baseline for up to the 99th percentile latency (within 15% in either direction). For 99.9th percentile and above, ghOSt leads to tail latencies that are 5% to 30% lower."

**작은 message에서는 99.99 백분위수 이상에서 최대 1.7배 나빴습니다.** 서론이 내세운 5에서 30퍼센트는 큰 message의 99.9 백분위수 이상에서 나온 값입니다.

논문은 그 이유도 적습니다. 작은 message는 처리할 것이 적어서 scheduling 사건의 비율이 높고, 그래서 scheduling 부담이 드러납니다.

> **논문으로.** 이것이 앞 장에서 말한 "evaluation을 의심하는 법"의 실제 사례입니다. 서론의 한 줄만 옮기면 "기존 방식보다 5에서 30퍼센트 좋다"가 되는데, 본문에는 나쁜 조건이 함께 적혀 있습니다.
>
> 이 논문은 나쁜 결과를 숨기지 않았습니다. 숨기지 않았는데도 서론만 읽으면 안 보입니다. 그러니 인용할 때는 본문의 조건까지 옮기는 것이 정확하고, 그렇게 하면 심사자에게 이 논문을 꼼꼼히 읽었다는 신호도 됩니다.

**셋째, 검색 서비스.** 256개 CPU를 중앙 agent 하나가 전부 맡는 정책을 짰습니다. 기계의 지형을 읽어서 thread가 직전에 돌던 core 근처에 다시 배치하는 방식입니다.

> "ghOSt leads to about 40-45% reduction in tail latency for query types A and B, compared to CFS, and comparable tail latency for query type C."

그리고 그 개선의 출처를 솔직하게 밝힙니다.

> "Prior to socket- and CCX-aware optimizations, the ghOSt policy led to nearly 2x worse latency for query type A and was on par with CFS for query type B and C. […] The NUMA and CCX optimizations were critical in achieving parity with CFS as they delivered 27% and 10% throughput improvements, respectively."

**지형 최적화를 넣기 전에는 오히려 2배 가까이 나빴습니다.** 좋은 결과가 틀에서 저절로 나온 것이 아니라 정책을 다듬어서 나왔다는 것입니다.

그리고 바로 그 다듬기가 이 연구의 진짜 기여라고 말합니다.

> "When developing a kernel scheduler, the write-test-write cycle includes (a) compiling a kernel (up to 15 minutes), (b) deploying the kernel (10-20 minutes), and (c) running the test (1 hour due to database initialization following a reboot). As a result, the enthusiastic kernel developer experiments with 5 variants per day. With ghOSt, compiling, deploying and launching the new agent is comfortably done within one minute."

**하루에 5번 시도할 수 있던 것이 1분에 한 번이 됐습니다.** 이 장의 서두에서 말한 벽이 무엇이었는지를 숫자로 보여주는 문단입니다.

**넷째, 가상 기계의 보안 격리.** 하드웨어 취약점 때문에 서로 믿지 못하는 손님을 같은 물리 core에 올리면 안 되는 상황을 정책으로 처리합니다. 이 사례가 이 갈래의 성격을 잘 보여줍니다. scheduling이 성능만의 문제가 아니라 **보안 정책의 집행 지점**이기도 하다는 것입니다.

## 3.3 sched_ext: 같은 일을 mainline에서

### 인용

- Linux kernel documentation. "Extensible Scheduler Class." Linux 6.12에 병합.

앞의 연구는 별도의 kernel 패치가 필요했습니다. 그러니까 그 패치를 적용한 kernel을 써야 했습니다.

**sched_ext는 같은 능력을 표준 Linux에 넣었습니다.** 2024년 말에 나온 kernel 버전부터 들어가 있습니다.

> **확인한 방식.** 이 문서는 렌더링된 웹 페이지가 아니라 **그 페이지가 생성되는 원본 파일을 Linux 소스 트리에서 직접 읽었습니다.** 내용은 동일하고, 그렇게 하면 kernel 버전별 차이까지 확인할 수 있습니다.
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
- ghOSt는 scheduling 결정을 user space로 위임하고 kernel은 그것을 transaction으로 실행합니다. kernel 쪽은 CFS와 나란한 scheduling class이고, thread 상태를 message로 내보내고 결정을 transaction으로 돌려받습니다. transaction이 필요한 이유는 한 agent가 다른 CPU까지 지휘하는 구조를 지원하기 위해서입니다.
- 안전은 세 겹입니다. ghOSt의 클래스가 기본 클래스보다 낮은 우선순위라서 대부분의 thread가 ghOSt thread를 밀어낼 수 있고, 구역을 없애면 그 안의 thread가 기본 scheduler로 돌아가며, 실행 가능한 thread를 정해진 밀리초 안에 배치하지 않으면 kernel이 그 구역을 자동으로 없앱니다.
- 부담은 나노초 단위입니다. thread 하나를 배치하는 데 888나노초이고, 참고로 CFS의 문맥 교환이 599나노초입니다. agent 하나가 초당 200만 개의 thread를 배치할 수 있다고 보고합니다.
- 평가에서 읽어야 할 것이 있습니다. 서론은 실제 서비스에서 꼬리 지연이 5에서 30퍼센트 좋아졌다고 적는데, 본문을 보면 그 값은 큰 message의 99.9 백분위수 이상에서 나온 것이고, 작은 message의 99.99 백분위수 이상에서는 최대 1.7배 나빴습니다. 검색 서비스에서도 지형 최적화를 넣기 전에는 2배 가까이 나빴다고 스스로 적습니다. 서론만 읽으면 보이지 않는 조건입니다.
- 이 갈래가 무엇을 바꿨는지는 이 문장이 가장 잘 보여줍니다. kernel scheduler를 고치던 시절에는 빌드와 배포와 시험에 시간이 들어 하루에 다섯 번 시도할 수 있었는데, 이 틀에서는 1분 안에 한 번이 됩니다.
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

> **확인한 방식, 이 장 전체에 해당.** 이 장의 인용문은 전부 각 논문의 원문 PDF 전문에서 읽었습니다(2026-09-12 확인). 셋 다 저자 또는 학회가 공개한 판본입니다. 앞의 두 논문은 각각 저자 소속 기관 페이지와 USENIX가 공개한 PDF이고, 세 번째는 NeurIPS 논문집이 공개한 PDF입니다. 마지막 논문은 arXiv 원고로만 존재합니다.

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

여기서 앞 장에서 배운 대로 읽어야 합니다. 비교 대상이 "hand-tuned scheduling heuristics"라고만 되어 있습니다. **어떤 heuristic인지는 초록에 없습니다.** 그리고 workload는 "Spark on a 25-node cluster"라고만 되어 있습니다. 본문을 열어서 그 둘을 확인해봅니다.

### job DAG란 정확히 무엇인가

먼저 이 논문이 다루는 job의 구조입니다.

> "A Spark job consists of a DAG whose nodes are the execution stages of the job. Each stage represents an operation that the system runs in parallel over many shards of the stage's input data. The inputs are the outputs of one or more parent stages, and each shard is processed by a single task. A stage's tasks become runnable as soon as all parent stages have completed."

job 하나가 여러 **stage**로 나뉘고, 각 stage는 자기 입력 데이터의 여러 조각에 같은 연산을 병렬로 적용합니다. 어떤 stage의 입력은 부모 stage들의 출력이고, 부모가 전부 끝나야 자식의 task들이 실행 가능해집니다.

그러니까 여기서 DAG의 노드는 **task 하나가 아니라 stage 하나**입니다. 이 구분이 중요합니다. 앞 권에서 본 chain은 task 사이의 사슬이었는데, 여기서는 한 단계 위에서 묶인 그룹 사이의 의존 관계입니다.

논문은 Spark가 실제로 내리는 결정이 셋이라고 정리합니다.

> "Spark must therefore handle three kinds of scheduling decisions: (i) deciding how many executors to give to each job; (ii) deciding which stages' tasks to run next for each job, and (iii) deciding which task to run next when an executor becomes idle."

그리고 그중 둘만 가져갑니다.

> "Decima focuses on DAG scheduling (i.e., which stage to run next) and executor allocation (i.e., each job's degree of parallelism). Since tasks in a stage run identical code and request identical resources, we use Spark's existing task-level scheduling."

**세 번째, 즉 진짜 task 하나를 고르는 일은 기존 방식에 그대로 맡깁니다.** 같은 stage 안의 task들은 코드도 자원 요구도 같아서 고를 이유가 없기 때문입니다.

이 절단이 이 연구를 읽을 때 중요합니다. 학습이 들어간 자리는 앞 권에서 배운 "다음에 어느 task를 실행할까"가 아니라, 그보다 한참 위의 **배분 결정**입니다.

### 상태를 어떻게 보여주는가

가장 단순한 방법이 왜 안 되는지부터 적습니다.

> "One option is to create a flat feature vector containing all the state information. However, this approach cannot scale to arbitrary number of DAGs of arbitrary sizes and shapes. Further, even with a hard limit on the number of jobs and stages, processing a high-dimensional feature vector would require a large policy network that would be difficult to train."

**크기와 모양이 제각각인 그래프를 하나의 평평한 벡터에 담을 수 없다**는 것입니다. 억지로 상한을 정해 담아도 벡터가 너무 커져서 학습이 안 됩니다.

그래서 그래프 구조를 그대로 읽는 신경망을 씁니다. 노드마다 특징 벡터를 붙이고, 그것을 노드 수준, job 수준, 전체 수준의 세 종류 요약으로 압축합니다.

**여기가 이 논문의 기술적 기여입니다.** 강화학습 자체가 아니라, scheduling 상태를 학습 가능한 모양으로 바꾼 방법입니다.

### 행동을 어떻게 정의하는가

행동 공간을 정하는 문제도 양 극단이 막혀 있습니다.

> "As a naive approach, consider a solution, that given the embeddings, returns the assignment for all executors to job stages in one shot. This approach has to choose actions from an exponentially large set of combinations. On the other extreme, consider a solution that invokes the scheduling agent to pick one stage every time an executor becomes available. This approach has a much smaller action space (O(# stages)), but it requires long sequences of actions to schedule a given set of jobs. In RL, both large action spaces and long action sequences increase sample complexity and slow down training."

한 번에 전부 배정하면 경우의 수가 지수적으로 커지고, 하나씩 배정하면 행동의 수가 너무 길어집니다. **둘 다 학습을 어렵게 만듭니다.**

절충안이 행동을 2차원으로 만드는 것입니다.

> "Decima balances the size of the action space and the number of actions required by decomposing scheduling decisions into a series of two-dimensional actions, which output (i) a stage designated to be scheduled next, and (ii) an upper limit on the number of executors to use for that stage's job."

**다음에 실행할 stage 하나, 그리고 그 stage가 속한 job이 쓸 수 있는 executor 수의 상한.** 이 두 값을 한 번에 냅니다.

판단을 언제 하는지도 정해져 있습니다.

> "Decima invokes the scheduling agent when the set of runnable stages — i.e., stages whose parents have completed and which have at least one waiting task — in any job DAG changes."

실행 가능한 stage의 집합이 바뀔 때마다입니다. stage가 끝났거나, 자식이 열렸거나, 새 job이 들어왔을 때입니다.

### 보상을 어떻게 주는가

목표가 평균 작업 완료 시간의 최소화일 때 보상이 이렇게 정의됩니다.

> "Decima gives the agent a reward r_k after each action based on its high-level scheduling objective. For example, if the objective is to minimize the average JCT, Decima penalizes the agent r_k = −(t_k − t_{k−1})J_k after the kth action, where J_k is the number of jobs in the system during the interval."

**시스템 안에 남아 있는 job의 수에, 그 상태가 지속된 시간을 곱한 만큼 벌점을 줍니다.**

그리고 왜 그 형태인지를 밝힙니다.

> "This objective minimizes the average number of jobs in the system, and hence, by Little's law, it effectively minimizing the average JCT."

시스템 안의 평균 job 수를 줄이는 것이 대기 이론의 법칙에 의해 평균 완료 시간을 줄이는 것과 같다는 것입니다.

**보상 설계를 눈여겨보세요.** 재고 싶은 것은 평균 완료 시간인데, 그것은 job이 끝나야만 알 수 있습니다. 계속 돌아가는 시스템에서는 끝을 기다릴 수 없으니, **매 순간 잴 수 있는 다른 값**으로 바꿔 놓았습니다. 그 둘이 같다는 근거로 대기 이론의 정리를 댑니다.

### 그래서 무엇과 비교했는가

초록의 "hand-tuned scheduling heuristics"가 본문에서는 일곱 개입니다.

> "In our evaluation, we compare Decima's performance to that of seven baseline algorithms: (1) Spark's default FIFO scheduling […] (2) A shortest-job-first critical-path heuristic (SJF-CP) […] (3) Simple fair scheduling […] (4) Naive weighted fair scheduling […] (5) A carefully-tuned weighted fair scheduling […] (6) The standard multi-resource packing algorithm from Tetris […] (7) Graphene*, an adaptation of Graphene for Decima's discrete executor classes"

**앞 권에서 배운 알고리즘들이 그대로 있습니다.** FIFO, 짧은 일 먼저, 공정 분배. 그리고 그것들의 가중치 붙인 변형과, 튜닝을 거친 변형이 있습니다.

다섯 번째 항목의 튜닝 방식을 눈여겨보세요.

> "We sweep through α ∈ {−2,−1.9,…,2} for the optimal factor."

**조정 인자를 41개 값으로 훑어서 각 실험마다 최적값을 찾아 씁니다.** 이건 이길 수 있는 상대를 고른 것이 아니라, 반대로 baseline을 최대한 강하게 세운 것입니다. 앞 장에서 "반대편을 가장 강한 형태로 세워야 논증이 선다"고 했는데, 이 논문이 그렇게 했습니다.

### 21퍼센트와 두 배가 나온 조건

**21퍼센트는 batch 도착 실험의 값입니다.**

> "We randomly sample jobs from six different input sizes (2, 5, 10, 20, 50, and 100 GB) and all 22 TPC-H queries, producing a heavy-tailed distribution: 23% of the jobs contain 82% of the total work. A combination of 20 random jobs (unseen in training) arrives as a batch, and we measure their average JCT."

표준 질의 모음에서 20개를 뽑아 한꺼번에 던지고 평균 완료 시간을 재는 실험입니다. **23퍼센트의 job이 전체 작업량의 82퍼센트를 차지하는 꼬리가 두꺼운 분포**입니다.

> "Decima outperforms all baseline algorithms and improves the average JCT by 21% over the closest heuristic ('opt. weighted fair')."

**21퍼센트는 일곱 개 중 가장 강한 상대와의 차이입니다.** 기본값과의 차이가 아닙니다. 논문은 그 기본값과의 차이도 적어두는데, 단순 공정 분배만으로도 FIFO보다 2.5배 좋습니다. 그러니 21퍼센트는 이미 잘 튜닝된 상대 위에 얹은 값입니다.

**두 배는 연속 도착 실험의 특정 구간입니다.**

> "We sample 1,000 TPC-H jobs of six different sizes uniformly at random, and model their arrival as a Poisson process with an average interarrival time of 45 seconds. The resulting cluster load is about 85%."

job 1,000개가 평균 45초 간격으로 계속 들어오고, 그 결과 cluster 부하가 85퍼센트가 되는 상황입니다.

> "Decima's average JCT is 29% lower. In particular, Decima shines during busy, high-load periods […] Decima maintains a lower concurrent job count than the tuned heuristic particularly during the busy period in hours 7–9, where Decima completes jobs about 2× faster."

**전체로는 29퍼센트이고, 두 배는 부하가 몰린 7시에서 9시 구간의 값입니다.** 초록의 "up to 2x improvement during periods of high cluster load"가 정확히 이 구간을 가리킵니다.

개선이 어디서 나오는지도 밝힙니다.

> "Decima's performance gain comes from finishing small jobs faster […] Decima achieves this by assigning more executors to the small jobs."

작은 job에 executor를 더 주는 것입니다. 그런데 무작정 더 주면 자원이 낭비됩니다.

> "The right number of executors for each job is workload-dependent: indiscriminately giving small jobs more executors would use cluster resources inefficiently."

**얼마나 더 줄지가 workload마다 다르다는 것**, 그 값을 사람이 정하지 않고 배웠다는 것이 이 논문의 주장입니다.

### 학습에 얼마나 드는가

이 연구가 데스크톱에 맞는지를 판단하려면 이 숫자가 필요합니다.

> "Finally, we train Decima for at least 50,000 iterations for all experiments."

> "We implemented Decima's training framework using TensorFlow, and we use 16 workers to compute episodes with the same job sequence in parallel during training. Each training iteration, including interaction with the simulator, model inference and model update from all training workers, takes roughly 1.5 seconds on a machine with Intel Xeon E5-2640 CPU and Nvidia Tesla P100 GPU."

**모든 실험에 최소 5만 번의 반복**, 반복 한 번에 약 1.5초, 그것도 병렬 작업자 16개와 GPU 한 장을 쓴 경우입니다. 두 숫자를 곱하면 실험 하나마다 20시간 남짓입니다.

본문의 다른 곳에는 다른 값이 적혀 있습니다.

> "Each training iteration takes about 5 seconds."

연속 도착 실험의 학습 곡선을 설명하는 문단입니다. 설정이 달라서 값이 다른 것으로 보이지만, 논문이 그 차이를 설명하지는 않습니다. 둘 중 어느 쪽을 쓰든 결론은 같습니다. **학습 한 번이 기계 한 대에서 하루 가까이 걸립니다.**

그리고 학습이 시뮬레이터 위에서 이루어진다는 점도 중요합니다.

> "Our training infrastructure relies on a faithful simulator of Spark job execution in a cluster."

실제 cluster에서 5만 번을 돌릴 수는 없기 때문입니다. 논문은 시뮬레이터의 충실도를 따로 검증해서, 단독 실행에서 평균 오차 5퍼센트 이내, 공유 실행에서 9퍼센트 이내라고 보고합니다.

### 환경이 바뀌면

이 연구가 스스로 밝힌 한계입니다.

> "When training with a mixed set of workloads that cover the whole interarrival time range, Decima can learn a more general policy. This policy fits less strongly to a specific interarrival time distribution and therefore becomes more robust to workload changes."

특정 도착 간격으로만 학습하면 그 분포에 맞춰지고, 범위 전체를 덮는 여러 workload로 학습해야 더 일반적인 정책이 나온다는 것입니다.

> "These results highlight that a diverse training workload set helps make Decima's learned policies robust to workload shifts"

**다양한 workload로 학습해야 workload 변화에 견딘다.** 뒤집어 말하면, 학습 때 본 적 없는 종류의 상황에는 약합니다.

> **이 연구에서는.** 이 두 문단이 이 연구가 학습 기반을 택하지 않은 이유의 절반입니다. 데이터센터에서는 학습에 하루를 쓰고 그 비용을 수천 대에 나눌 수 있습니다. 데스크톱은 기계가 한 대이고, 그 한 대에서 어제 설치한 프로그램이 오늘 처음 돕니다. 학습 때 본 적 없는 상황이 기본값인 환경입니다.

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

여기서도 앞 장의 독법을 적용하면, "four microservice benchmarks"가 무엇인지 초록에 없습니다. 그리고 **"up to"라는 표현이 세 번 반복됩니다.** 본문에서 둘 다 확인해봅니다.

### 네 개의 벤치마크

> "We evaluated FIRM on a set of end-to-end interactive and responsive real-world microservice benchmarks: (i) DeathStarBench, consisting of Social Network, Media Service, and Hotel Reservation microservice applications, and (ii) Train-Ticket, consisting of the Train-Ticket Booking Service."

두 개의 공개 벤치마크 모음에서 나온 네 개의 응용입니다.

> "Social Network implements a broadcast-style social network with unidirectional follow relationships whereby users can publish, read, and react to social media posts. Media Service provides functionalities such as reviewing, rating, renting, and streaming movies. Hotel Reservation is an online hotel reservation site for browsing hotel information and making reservations. Train-Ticket Booking Service provides typical train-ticket booking functionalities, such as ticket inquiry, reservation, payment, change, and user notification."

소셜 네트워크, 영화 서비스, 호텔 예약, 기차표 예매입니다. **전부 사람이 쓰는 웹 서비스이고, 네 개 다 공개된 벤치마크입니다.**

규모도 적혀 있습니다.

> "These benchmarks contain 36, 38, 15, and 41 unique microservices, respectively; cover all workflow patterns; and use various programming languages including Java, Python, Node.js, Go, C/C++, Scala, PHP, and Ruby. All microservices are deployed in separate Docker containers."

각각 서비스가 15개에서 41개이고, 언어가 여덟 가지 섞여 있습니다.

**이 마지막 대목이 이 갈래의 성격을 보여줍니다.** 서비스 하나가 무슨 언어로 짜였는지가 scheduling 판단에 들어가지 않습니다. 자원 사용량과 지연만 봅니다.

### 안에서 무엇이 도는가

FIRM은 단계별로 나뉜 구성요소들입니다.

**추적 수집기.** 각 서비스에서 추적 데이터와 원격 측정값을 모아 한곳의 그래프 데이터베이스에 넣습니다.

**추출기.** 목표 위반을 감지하면 그 데이터를 질의해서 두 가지를 뽑습니다. 하나는 지금 응답 시간을 결정하고 있는 경로이고, 다른 하나는 그 경로에서 문제를 일으킨 서비스입니다. 논문이 근거를 이렇게 적습니다.

> "Based on the insight that resource contention manifests as dynamically evolving CPs, FIRM first detects CP changes and extracts critical microservice instances from them."

**자원 경합이 "지금 가장 오래 걸리는 경로가 계속 바뀌는" 형태로 나타난다**는 통찰입니다. 경로가 고정되어 있으면 미리 계산해두면 되는데, 경합 때문에 매 순간 바뀝니다.

**자원 추정기.** 여기가 학습이 들어간 자리입니다. 무엇을 조절할 수 있는지가 구체적으로 적혀 있습니다.

> "FIRM estimates and controls a fine-grained set of resources, including CPU time, memory bandwidth, LLC capacity, disk I/O bandwidth, and network bandwidth. It makes decisions on scaling each type of resource or the number of containers"

CPU 시간, memory 대역폭, 마지막 단계 cache의 용량, 디스크 입출력 대역폭, 네트워크 대역폭, 그리고 컨테이너 수입니다.

**앞 권에서 CPU만 다뤘는데 여기는 다섯 가지입니다.** 실제 시스템에서 경합이 일어나는 곳이 CPU만이 아니라는 뜻입니다.

**배포 모듈.** 결정을 실제로 먹이는 부분인데, 수단이 전부 기존 Linux 기능입니다.

> "CPU Actions: Actions on scaling CPU utilization are executed through modification of cpu.cfs_period_us and cpu.cfs_quota_us in the cgroups CPU subsystem."

**앞 권에서 본 자원 그룹의 주기와 할당량**입니다. 이 연구가 하는 일은 새 scheduler를 만드는 것이 아니라, 이미 있는 손잡이를 언제 얼마나 돌릴지를 배우는 것입니다.

**성능 이상 주입기.** 학습을 위해 일부러 경합을 만들어내는 장치입니다. 어느 자원에 얼마나 세게 부하를 걸지를 설정할 수 있습니다.

> "FIRM includes a performance anomaly injection framework that triggers SLO violations by generating resource contention with configurable intensity and timing."

**이게 없으면 학습이 안 됩니다.** 목표 위반은 드물게 일어나는데, 강화학습은 그 상황을 수없이 겪어야 배웁니다. 그래서 일부러 만들어냅니다.

논문이 그 이유를 강화학습 쪽에서 설명합니다.

> "Model-free RL does not need the ergodic distribution of states or the environment dynamics (i.e., transitions between states), which are difficult to model precisely."

상태 사이의 전이를 정확히 모형화하기 어려우니 환경 모형 없는 방식을 쓴다는 것인데, 그러면 대신 **직접 겪어봐야** 합니다.

### 최대치가 무엇과의 최대치인가

초록의 세 개의 "up to"가 본문에서 이렇게 풀립니다. 비교 대상은 둘입니다. 하나는 컨테이너 관리 도구의 기본 자동 확장이고, 다른 하나는 네트워크에서 쓰는 고전적인 증감 방식입니다.

> "We observed that the AIMD-based method, albeit simple, outperforms the Kubernetes autoscaling approach by 1.7× on average and by 1.6× in the worst case. In contrast, FIRM: 1. Outperformed both baselines by up to 6× and 11×, which leads to 9× and 16× fewer SLO violations; 2. Lowered the overall requested CPU limit by 29–62%, and increased the average cluster-level CPU utilization by up to 33%; 3. Reduced the number of dropped or timed out user requests by up to 8×."

**16배는 둘 중 약한 쪽과의 차이이고, 강한 쪽과는 9배입니다.** 그리고 62퍼센트는 29에서 62퍼센트라는 범위의 위쪽 끝입니다.

> **논문으로.** 이것이 "up to"를 읽는 방법입니다. 초록의 숫자가 틀린 것이 아닙니다. 다만 초록은 범위의 위쪽 끝만 적고, 본문에는 범위와 비교 대상이 함께 있습니다. 인용할 때 본문의 범위를 쓰면 정확하고, 그 편이 오히려 설득력이 있습니다. 29에서 62퍼센트라고 쓰면 읽는 사람이 실제 분포를 짐작할 수 있습니다.

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

논문의 표 하나에 전부 있습니다.

적응형 영상 스트리밍, Spark cluster 작업 배치, 데이터베이스 질의 최적화, 네트워크 혼잡 제어, 네트워크 능동 큐 관리, 연산 장치 배치, 회로 설계, 콘텐츠 전송망 캐시, 다차원 데이터베이스 색인, 계정 지역 할당, 서버 부하 분산, 스위치 scheduling입니다.

열두 개가 맞고, 그중 하나가 앞에서 본 cluster 작업 배치입니다.

그리고 그중 일곱 개는 실제 시스템을 뒤에 붙이고, 다섯 개는 시뮬레이터를 씁니다.

> "Seven of the environments use real systems in the backend. For the remaining five environments, which have well-understood dynamics, we provide a simulator to facilitate easier setup and faster RL training."

시뮬레이터를 쓰는 쪽은 **동작이 잘 이해된** 문제들이라는 단서가 붙어 있습니다.

### 이 논문의 핵심: 왜 어려운가

이제 이 논문이 정말로 하는 이야기로 갑니다. 논문의 한 절 전체가 여기에 쓰여 있고, 제목이 "RL for Systems Characteristics and Challenges"입니다.

> "In this section, we explain the unique characteristics and challenges that often prevent off-the-shelf RL methods from achieving strong performance in different computer system problems."

기성 강화학습 방법이 시스템 문제에서 좋은 성능을 내지 못하게 막는 **고유한 어려움**들입니다. 네 갈래로 나뉩니다.

#### 첫째, 상태와 행동의 공간

**건초더미 속 바늘 문제.**

> "In some computer systems, the majority of the state-action space presents little difference in reward feedback for exploration. This provides no meaningful gradient during RL training, especially in the beginning, when policies are randomly initialized."

**공간의 대부분에서 보상이 똑같이 나빠서, 어느 쪽으로 가야 할지 알 수 없다**는 것입니다.

논문이 드는 예가 명료합니다. 네트워크 혼잡 제어에서, 보낼 수 있는 것보다 빠르게 보내면 회선과 대기열이 꽉 찹니다. 그 지점을 넘어선 뒤에는 더 빠르게 보내든 조금 덜 빠르게 보내든 결과가 똑같이 나쁩니다.

> "To exit this bad state, the agent must set a low sending rate for multiple consecutive steps to drain the queue before receiving any positive reward. Random exploration is not effective at learning this behavior because any random action can easily overshadow several good actions, making it difficult to distinguish good action sequences from bad ones."

빠져나오려면 **여러 단계 연속으로** 낮게 보내서 대기열을 비워야 하는데, 무작위로 탐색하면 좋은 행동 몇 개를 나쁜 행동 하나가 덮어버립니다.

**앞 권에서 본 과부하 상황이 이 모양입니다.** 이미 밀려 있는 상태에서는 어떤 선택을 해도 당장은 나쁘고, 회복은 여러 결정을 연속으로 잘해야 옵니다.

논문이 제안하는 대응도 적혀 있습니다.

> "In these environments, using domain-knowledge to confine the search space helps to train a strong policy."

**사람의 지식으로 탐색 공간을 미리 좁혀야** 한다는 것입니다.

**표현의 문제.**

> "When designing RL methods for problems with complex structure, properly encoding the state-action space is the key challenge. In some systems, the action space grows exponentially large as the problem size increases. For example, in switch scheduling, the action is a bijection mapping (a matching) between input and output ports — a standard 32-port would have 32! possible matching."

포트 32개짜리 스위치의 행동 공간이 32의 계승입니다.

> "In other cases, the size of the action space is constantly changing over time. For example, a typical problem is to map jobs to machines. In this case, the number of possible mappings and thus, actions increases with the number of new jobs in the system."

**행동 공간의 크기 자체가 계속 변합니다.** 새 작업이 들어오면 선택지가 늘어납니다.

그리고 마지막 한 문장이 무겁습니다.

> "However, finding the right representation for each problem is a central challenge, and for some domains, e.g., query optimization, remains largely unsolved."

**문제마다 맞는 표현을 찾는 것이 핵심 난제이고, 어떤 영역에서는 아직 풀리지 않았다**는 것입니다.

#### 둘째, 결정 과정 자체의 성질

**입력의 무작위성이 보상을 흔듭니다.**

> "Queuing systems environments (e.g., job scheduling, load balancing, cache admission) have dynamics partially dictated by an exogenous, stochastic input process. Specifically, their dynamics are governed not only by the decisions made within the system, but also the arrival process that brings work (e.g., jobs, packets) into the system. In these environments, the stochasticity in the input process causes huge variance in the reward."

시스템의 움직임이 **내 결정만이 아니라 밖에서 들어오는 일감에도** 좌우된다는 것입니다.

논문이 그림으로 설명하는 예가 정확합니다.

> "If the arrival sequence after time t consists of a burst of large jobs, the job queue will grow and the agent will receive low rewards. In contrast, a stream of lightweight jobs will lead to short queues and large rewards. The problem is that this difference in reward is independent of the action at time t; rather, it is caused purely by the randomness in the job arrival process. In these environments, the agents cannot tell whether two reward feedbacks differ due to disparate input processes, or due to the quality of the actions."

**같은 상태에서 같은 행동을 했는데 보상이 전혀 다르게 나옵니다.** 그 차이가 내가 잘해서인지 운이 좋아서인지 구분할 수 없습니다.

논문은 대응책을 언급하면서 동시에 그 대응책의 한계도 적습니다.

> "However, the proposed training implementations ('multi-value network' and 'meta baseline') are tailored for policy gradient methods and require the environments to have a repeatable input process (e.g., in simulation, or real systems with controllable input sequence). Thus, coping with input-driven variance remains an open problem for value-based RL methods and for environments with uncontrollable input processes."

**그 대응책은 입력을 반복 재생할 수 있어야 쓸 수 있고**, 입력을 통제할 수 없는 환경에서는 여전히 열린 문제입니다.

**끝이 없는 문제입니다.**

> "In practice, production computer systems (e.g., Spark schedulers, load balancers, cache controllers, etc.) are long running and host services indefinitely. This creates an infinite horizon MDP that prevents the RL agents from performing episodic training."

**시스템은 끝나지 않습니다.** 게임은 이기거나 지면 끝나고, 그 끝에 점수를 매길 수 있습니다. scheduler에는 끝이 없습니다. 끝이 없으면 "이 판의 결과가 얼마였다"는 기준점을 만들 수 없습니다.

> "Moreover, the discounted total reward formulation in the episodic case might not be suitable — an action in a long running system can have impact beyond a fixed discounting window. For example, scheduling a large job on a slow server blocks future small jobs, no matter whether the small jobs arrive immediately after the large job or much farther in the future over the course of the lifetime of the large job."

먼 미래의 보상을 깎아서 보는 통상의 방식도 맞지 않습니다. **긴 작업을 느린 서버에 올리면 그 작업이 사는 내내 뒤에 오는 작업을 막는데**, 그 피해가 얼마나 뒤에 오느냐와 무관하게 같은 크기이기 때문입니다.

#### 셋째, 시뮬레이션과 현실의 간극

이 항목이 이 연구와 가장 직접적으로 연결됩니다.

> "Unlike training RL in simulation, robustly deploying a trained RL agent or directly training RL on an actual running computer systems has several difficulties."

세 가지를 듭니다.

**모형의 정확도가 문제의 복잡도에 따라 무너집니다.**

> "First, discrepancies between simulation and reality prevent direct generalization. For example, in database query optimization, existing simulators or query planners use offline cost models to predict query execution time (as a proxy for the reward). However, the accuracy of the cost model quickly degrades as the query gets more complex due to both variance in the underlying data distribution and system-specific artifacts."

**실제 시스템은 느립니다.**

> "Second, interactions with some real systems can be slow. In adaptive video streaming, for example, the agent controls the bitrate for each chunk of a video. Thus, the system returns a reward to the agent only after a video chunk is downloaded, which typically takes a few seconds. Naively using the same training method from simulation would take a single-threaded agent more than 10 years to complete training in reality."

**시뮬레이터에서 하던 방식 그대로 실제 시스템에서 학습하면 10년이 넘게 걸립니다.**

**학습 중이거나 배포된 agent가 시스템을 망가뜨릴 수 있습니다.**

> "Finally, live training or directly deploying an agent from simulation can degrade the system performance."

논문이 드는 구체적인 예가 무섭습니다. 부하 분산 환경에서 학습한 agent가, 처음에 본 작업 크기 분포가 둘로 갈린 모양이었기 때문에 **작은 작업 전용으로 서버 하나를 비워두는 정책**을 배웠습니다. 그런데 분포가 바뀌자 그 비워둔 서버가 그냥 낭비가 되어 전체 처리량이 떨어졌습니다.

> "Therefore, to deploy training algorithms online, these problems require RL to train robust policies that ensure safety."

#### 넷째, 기존 heuristic과의 이해 가능성 경쟁

마지막 항목이 다른 셋과 성격이 다릅니다. 기술적 난점이 아니라 **채택의 문제**입니다.

> "As in other areas of ML, interpretability plays an important role in making learning techniques practical. However, in contrast to perception-based problems or games, for system problems, many reasonable good heuristics exist. For example, every introductory course to computer science features a basic scheduling algorithm such as FIFO. These heuristics are often easy to understand and to debug, whereas a learned approach is often not. Hence, making learning algorithms in systems as debuggable and interpretable as existing heuristics is a key challenge."

**시스템 분야에는 이미 꽤 괜찮은 heuristic이 많습니다.** 이미지 인식과 다른 점이 여기입니다. 고양이를 알아보는 손으로 쓴 규칙은 없지만, 작업을 배치하는 손으로 쓴 규칙은 강의 첫 주에 나옵니다. 그리고 그 규칙은 읽을 수 있고 고칠 수 있습니다.

그러니 학습 기반이 이기려면 성능만으로는 부족하고, **이해 가능성과 디버깅 가능성에서도 기존 규칙만큼은 되어야** 합니다.

논문이 제안하는 방향도 적혀 있습니다.

> "Here, a unique opportunity is to build hybrid solutions, which combine learning-based techniques with traditional heuristics. Existing heuristics can not only help to bootstrap certain problems, but also help with safety and generalizability. For example, a learned scheduling algorithm could fall back to a simple heuristic if it detects that the input distribution significantly drifted."

**학습된 것과 전통적인 규칙을 섞는 것**, 그리고 입력 분포가 크게 달라지면 단순한 규칙으로 되돌아가는 것입니다.

> **이 연구에서는.** 이 네 갈래가 이 연구의 설계에 그대로 반영되어 있습니다. 하나씩 대응시켜 봅니다.
>
> **상태와 행동의 공간.** 이 연구는 공간을 학습으로 탐색하지 않습니다. 상황을 나타내는 어휘가 작고 고정되어 있고, 그 어휘가 어떤 설정으로 번역되는지도 미리 적힌 표입니다. 탐색할 공간 자체를 만들지 않았습니다.
>
> **결정 과정의 성질.** 이 연구에는 보상 함수가 없습니다. 언어 모델의 출력은 정답 라벨과 대조해서 채점되지, 시스템 성능으로 되먹임되지 않습니다. 입력의 무작위성이 보상을 흔드는 문제가 생길 자리가 없습니다.
>
> **시뮬레이션과 현실의 간극.** 이 연구도 시뮬레이터를 씁니다. 그래서 이 항목은 피해 가지 못하고 그대로 받습니다. 다만 이 연구가 시뮬레이터에서 하는 것은 학습이 아니라 **비교**입니다. 같은 workload를 여러 설정으로 돌려서 차이를 봅니다. 학습한 정책을 실제 기계에 옮길 때 생기는 문제와는 성격이 다르지만, 시뮬레이터가 실제 하드웨어의 무엇을 놓치는지는 여전히 따로 다뤄야 할 숙제입니다.
>
> **이해 가능성.** 이 연구가 가장 크게 기대는 항목입니다. 이 연구의 정책은 전부 사람이 읽을 수 있는 표이고, 언어 모델이 바꾸는 것은 그 표의 어느 줄을 쓸지뿐입니다. 그리고 마지막 인용문의 되돌아가기 제안이 이 연구의 검증기와 같은 발상입니다. 판단이 허용된 어휘 밖으로 나가면 기본값으로 되돌립니다.

> **논문으로.** 이 절이 논문에서 "왜 학습 기반을 택하지 않았는가"를 쓸 때의 근거입니다. 그리고 인용의 성격이 좋습니다. **이 갈래를 비판하는 외부 문헌이 아니라, 이 갈래를 만들어낸 사람들이 스스로 정리한 난점 목록**입니다. 같은 저자가 앞에서 본 cluster 배치 연구의 제1저자이기도 합니다.
>
> 그러니 "학습 기반은 이런 어려움이 있다고 그 분야가 스스로 정리했다"고 쓸 수 있습니다. 밖에서 던지는 비판보다 훨씬 방어하기 쉬운 형태입니다.

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

- Wang, X., Jia, S., Huang, Z., Cao, J., & Song, M. (2025). Mixture-of-Schedulers: An Adaptive Scheduling Agent as a Learned Router for Expert Policies. arXiv:2511.11628 (v1, 2025-11-07).

정식 학회에 실린 논문이 아니라 arXiv에 올라온 원고입니다. 앞에서 정리한 대로, 심사를 거치지 않았다는 것을 전제하고 읽어야 합니다.

**판본과 게재 여부를 확인했습니다.** 2026년 9월 12일 기준으로 arXiv에 올라온 판본은 첫 번째 하나뿐이고, 2025년 11월 7일에 올라온 뒤 개정되지 않았습니다. 서지 정보에 학회 게재란과 비고란이 모두 비어 있습니다. **게재된 곳이 없습니다.**

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

투표를 쓰는 이유를 본문이 밝힙니다. 그리고 그 값을 실험으로 정했습니다.

> "The results show a clear U-shaped curve for response delay. A very short window (W<4s) leads to high average delay because the system becomes overly sensitive to transient noise, causing frequent, erroneous scheduler switches. This policy "thrashing" means the system spends significant time in a suboptimal state while oscillating […] Conversely, a very long window (W>10s) also increases delay by making the system too slow to respond to genuine workload changes. The plot reveals a Pareto-optimal range between 4s and 7s. We chose W=6s as a robust compromise"

창이 4초보다 짧으면 잡음에 반응해서 scheduler가 계속 바뀌고, 10초보다 길면 진짜 변화에 늦게 반응합니다. **6초를 골랐습니다.**

**이 숫자를 기억해두세요.** 이쪽이 상황이 바뀌었다고 판정하는 데 6초가 걸립니다. 뒤 장에서 이 연구의 판단 주기와 비교할 때 쓰입니다.

### 라우터가 읽는 것

이 연구와 가장 중요한 차이가 여기 있으므로 정확히 봅니다. 본문의 표 하나에 감시하는 항목이 전부 나열되어 있습니다.

| 갈래 | 항목 |
|---|---|
| CPU | 사용자/커널 모드 사용률, nice·유휴·입출력 대기·하드웨어 인터럽트·소프트웨어 인터럽트·steal 사용률, 과열 core 비율 |
| 메모리 | 전체/여유/캐시 메모리, 전체/가용 스왑, 버퍼 |
| 디스크 | 입출력 대기열 길이, 읽기/쓰기 횟수, 읽기/쓰기 지연, 평균 입출력 크기 |
| 프로세스 | 프로세스 수, GPU를 쓰는 프로세스 수와 그 CPU 사용률, **창에 초점이 있는 프로세스의 CPU/메모리 사용률**, 입력 이벤트 |
| scheduling | task 이주 횟수, 잠금 경합과 획득 실패 횟수, 잠금 보유 시간과 thread 차단 시간, thread 깨움 지연과 문맥 교환 지연, 문맥 교환 횟수, 실행 대기열 길이 |
| 네트워크 | 전체/신규/종료/재설정 연결 수, 송수신 데이터량, 패킷 수, 재전송률, TCP/UDP 비율, 네트워크 인터럽트 수와 처리 지연, 송수신 지연, 커널-사용자 공간 지연 |

수집 방식도 적혀 있습니다.

> "The Perception module collects data from multiple sources, including kernel-level eBPF programs, the procfs file system, and GNOME Shell for desktop environment information."

kernel 안의 탐침, 프로세스 정보 파일 체계, 그리고 **데스크톱 환경**에서 가져옵니다.

**이 표를 자세히 봐야 하는 이유가 있습니다.** 목록에 데스크톱 신호가 실제로 들어 있습니다. 창에 초점이 있는 프로세스, 입력 이벤트, GPU를 쓰는 프로세스 수. 앞 권에서 본 "전면 창 우대"의 재료들입니다.

**그런데 목록 어디에도 프로세스의 이름이 없습니다.** 초점이 있는 프로세스의 CPU 사용률은 읽지만, 그 프로세스가 무엇인지는 읽지 않습니다. 관측 항목 전체가 수치입니다.

앞 장에서 정리한 대비를 여기에 대보면 결론이 바로 나옵니다. 사용자가 시작한 학습과 예약된 색인 작업은 이 표의 모든 칸에서 같은 값을 낼 수 있습니다. **이 표에 그 구분을 담을 칸이 없습니다.**

### 전문 정책의 목록

무엇 중에서 고르는지도 본문에 있습니다.

> "The expert scheduler set available to ASA includes: scx_p2dq, scx_bpfland, scx_nest, scx_lavd, scx_simple, scx_flash, scx_rusty"

일곱 개이고, 여기에 기본 scheduler가 비교 대상으로 더해집니다.

**앞 장에서 본 정책 모음 저장소의 이름들이 그대로 있습니다.** 대화형 우선, 지연 민감도 기반, 공정성 중심, 여러 영역 기반. 앞 장에서 "사람들이 여러 개를 만들어두고 골라 쓰고 있다"고 했는데, 이 연구가 그 고르는 일을 자동화한 것입니다.

그리고 이 목록이 성능의 상한이라고 스스로 밝힙니다.

> "The primary limitation of ASA is that its performance ceiling is defined by the quality and diversity of its expert scheduler portfolio."

### 무엇으로 평가했는가

초록의 "a novel benchmark"가 본문에서 이렇게 풀립니다.

> "we constructed a benchmark suite of 28 scenarios. These are generated by pairing 4 interactive, latency-sensitive applications (Web Browsing, Audio Remix, Office File, Game Play) with 7 resource-intensive, background workloads (e.g., kernel compilation, blender render, LLM local generation)."

**대화형 응용 넷과 배경 부하 일곱을 짝지어 만든 28개 상황**입니다. 배경 부하에는 커널 빌드, 3차원 렌더링, 언어 모델 실행, 압축 해제, 디스크 입출력, 네트워크 전송, 영상 변환이 있습니다.

> **이 연구에서는.** 이 벤치마크의 구성이 이 연구의 데이터셋과 놀랍도록 가깝습니다. 대화형 작업 하나와 배경 부하 하나를 짝지어 상황을 만든다는 발상이 같습니다.
>
> **차이는 배경 부하에 라벨이 붙어 있느냐입니다.** 이쪽의 28개 상황에는 어떤 프로그램이 도는지가 이름으로 적혀 있지만, 그 이름은 사람이 실험을 구성하기 위한 것이지 시스템에게 주는 정보가 아닙니다. 시스템은 앞의 표에 있는 수치만 봅니다. 그리고 배경 부하가 사용자가 원한 것인지 아닌지는 이 28개 어디에도 구분되어 있지 않습니다. 커널 빌드가 사용자가 지금 기다리는 것인지 예약된 것인지에 따라 올바른 대우가 달라지는데, 그 축이 없습니다.

평가 기기도 적혀 있습니다. 가상 기계 10대이고, core 수가 2개에서 20개까지입니다. 그중 4대는 모델을 만들 때 쓰고 6대는 처음 보는 기계로 남겨둡니다.

### 결과

> "Our evaluation, based on a novel benchmark focused on user-experience metrics, demonstrates that ASA consistently outperforms the default Linux scheduler (EEVDF), achieving superior results in 86.4% of test scenarios. Furthermore, ASA's selections are near-optimal, ranking among the top three schedulers in 78.6% of all scenarios."

시나리오의 86.4퍼센트에서 기본 scheduler보다 나았고, 78.6퍼센트에서 상위 세 개 안에 드는 선택을 했다는 것입니다.

본문은 개선폭도 함께 적습니다.

> "The results show that ASA achieves an overall win rate of 86.4% against EEVDF, with a global average improvement of +8.83% (95% CI [7.08%, 10.59%])."

**이긴 비율은 86.4퍼센트인데 평균 개선은 8.83퍼센트입니다.** 자주 이기되 조금씩 이깁니다. 구간 추정까지 붙여둔 점은 앞 장에서 말한 좋은 보고 관행입니다.

그리고 이긴 비율이 높은 이유를 스스로 낮춰 말합니다.

> "Notably, in many scenarios where ASA does not significantly outperform EEVDF, it is because EEVDF itself is the optimal or near-optimal choice for that specific workload. In these cases, ASA correctly identifies this and selects EEVDF (or a similarly performing scheduler), with its marginal overhead sometimes resulting in performance slightly below the native EEVDF."

기본 scheduler가 이미 최선인 상황에서는 그것을 고르고, 그러면 감시 부담 때문에 **오히려 아주 조금 못한 결과가 나온다**는 것입니다.

### 초록과 본문의 숫자가 다릅니다

원문을 대조하다 발견한 것을 적어둡니다. 초록은 상위 세 개 안에 드는 비율을 78.6퍼센트로 적는데, 본문은 다르게 적습니다.

> "ASA's selected scheduler is the single best one in 45.4% of cases and ranks among the top three in 78.9% of cases."

**본문은 78.9퍼센트입니다.** 0.3퍼센트포인트 차이이고 결론이 달라지지 않지만, 같은 원고 안에서 같은 값이 두 번 다르게 적혀 있습니다.

> **논문으로.** 이런 것을 인용 근거로 쓰면 안 됩니다. 오타일 가능성이 높고, 그것을 지적하는 것은 연구의 주장과 무관합니다. 다만 **어느 쪽 숫자를 옮길지는 정해야** 합니다. 이 연구는 본문 값을 쓰고 초록과 다르다는 사실을 주석으로 남기는 쪽을 택합니다. 초록만 읽고 옮겼다면 이 차이를 몰랐을 것입니다.

### 인식 정확도를 따로 잽니다

이 연구가 이 갈래에서 드문 일을 하나 합니다. **최종 성능과 별개로 인식 자체의 정확도를 보고합니다.**

> "Even without any environment-specific fine-tuning, the base model correctly identifies the running workload scenario with 96.83% accuracy."

> "Without fine-tuning, the base workload classifier achieves a notable accuracy of 96.83%. After the online fine-tuning process, the accuracy of the raw model output (before the time-weighted voting is applied) increases to 99.19%."

28개 상황을 알아맞히는 정확도가 미세 조정 전 96.83퍼센트, 후 99.19퍼센트입니다.

> **이 연구에서는.** 이 대목을 정확히 다뤄야 합니다. 뒤 장에서 언어 모델 계열을 다룰 때 "인식 자체를 따로 재는 평가는 그쪽에 대응물이 없다"고 말하게 되는데, **그 서술은 언어 모델 계열에 대해서만 성립합니다.** 이쪽은 잽니다.
>
> 그러니 이 연구의 측정 계층이 완전히 새로운 것은 아닙니다. 다른 것은 **무엇을 정답으로 놓았느냐**입니다. 이쪽의 정답은 "이 실험이 28개 중 몇 번 상황인가"이고, 상황의 목록은 실험 설계자가 정한 28개입니다. 이 연구의 정답은 상황을 기술하는 어휘의 각 항목이고, 같은 상황에 여러 번 물었을 때의 일관성과 방해 요소가 섞였을 때의 견고함을 따로 봅니다.
>
> 요약하면, 인식을 잰다는 발상 자체는 이 연구가 처음이 아닙니다. 그 점을 논문에서 흐리면 안 됩니다.

### 무엇이 다른가

이 연구와 골격이 같으니 차이를 정확히 말해야 합니다. 그리고 그 차이는 하나입니다.

**인식하는 채널이 다릅니다.**

이쪽은 시스템 행동에서 패턴을 읽습니다. 이 연구는 프로세스의 이름에서 상황을 읽습니다.

그러니까 이쪽은 앞 장에서 정리한 행동 채널의 한계를 그대로 가집니다. 골격이 아무리 같아도, 행동이 동일하고 의도가 다른 상황은 구분하지 못합니다.

### 기계별 대응표는 누가 만드는가

초록에 눈에 걸리는 대목이 있습니다.

> "This decoupled architecture allows ASA to adapt to new hardware platforms rapidly without expensive retraining of the core recognition model."

새 하드웨어에 적응할 때 인식 모델을 다시 학습시킬 필요가 없다는 주장입니다.

그런데 같은 초록에 이런 표현이 있습니다. **"a pre-configured, machine-specific mapping table"**, 즉 기계별로 미리 만들어둔 대응표입니다.

모델은 기계에 무관한데 대응표는 기계별입니다. 그러면 그 표는 누가 어떻게 만드나요? 손으로 쓴다면 앞 권에서 본 목록 문제가 여기서 반복됩니다.

**초록에는 답이 없습니다. 본문에는 있습니다.**

먼저 왜 표를 기계별로 두는지가 적혀 있습니다.

> "This is complicated by two factors: the platform dependency of workload characteristics, where the same application exhibits different features on different hardware, and the hardware adaptability of scheduling policies, where the optimal policy for a given workload can vary with the hardware configuration. However, our core insight is that for any single machine, a workload pattern can correspond to an optimal scheduler. This principle enables a practical cross-platform optimization strategy, where the general task of pattern recognition can be decoupled from the machine-specific task of policy selection."

같은 응용이 기계마다 다른 특징을 보이고, 같은 workload에 맞는 정책도 기계 구성에 따라 달라집니다. 그래서 **패턴을 알아보는 일반적인 일과 정책을 고르는 기계별 일을 분리했다**는 것입니다.

그리고 표를 만드는 절차가 세 단계로 적혀 있습니다.

**1단계.** 여러 scheduler로 미리 정한 상황들을 전부 돌려보면서 두 종류의 데이터를 모읍니다. 하나는 분류 모델을 학습시킬 특징값이고, 다른 하나는 각 scheduler를 채점할 성능 지표입니다.

> "With the system operational metrics, we train a preliminary workload classification model. Concurrently, based on the performance evaluation results, we determine the optimal scheduling strategy for each test scenario, thereby constructing an initial scheduler mapping table of 'scenario-optimal scheduler'."

**표의 각 줄은 측정으로 채워집니다.** 상황마다 후보를 전부 돌려보고 가장 좋았던 것을 적습니다.

**2단계.** scheduler를 바꾸는 일 자체의 비용을 재서 반영합니다. 실제로 갈아 끼우지는 않고 준비 절차만 밟는 "그림자" scheduler를 써서, 감시와 판단에 드는 부담만 따로 측정합니다.

**3단계.** 실제로 갈아 끼우면서 돌리고, 그 결과로 모델과 표를 다시 다듬습니다.

그리고 새 기계에 옮길 때의 절차가 이것입니다.

> "Deploying the generalized ASA agent onto a new hardware platform is a streamlined process. By exclusively running the 'Generalization Model Training' (Stage 3) on the target machine, ASA can interact directly with the new environment and its available schedulers, resulting in the creation of a precise, hardware-specific scheduler mapping table ready for immediate use."

**대상 기계에서 3단계만 돌리면 그 기계용 표가 만들어집니다.**

### 그래서 결론은

원래의 의심은 반만 맞았습니다.

**사람이 손으로 쓰지 않습니다.** 표는 대상 기계에서 실제로 돌려보고 채워집니다. 자동 생성 절차가 본문에 명시되어 있으므로, 앞 권에서 본 이름 목록의 노후화 문제는 여기 해당하지 않습니다. 새 프로그램이 나온다고 사람이 줄을 추가해야 하는 구조가 아닙니다.

**다만 비용은 남습니다.** 기계마다 미리 돌려보는 시간이 필요하고, 저자들도 그 단계를 없애지는 못했습니다. 초록의 "expensive retraining 없이"라는 말은 정확히 **인식 모델의 재학습**을 가리키는 것이지, 기계별 준비가 없다는 뜻이 아닙니다.

> **논문으로.** 이 대비가 이 절의 교훈입니다. 초록만 읽었을 때 떠오른 의심은 합리적이었지만 **본문에 답이 있었습니다.** 초록의 표현이 답을 담기에 짧았을 뿐입니다.
>
> 만약 확인하지 않고 "저 연구는 기계별 표를 누가 만드는지 말하지 않는다"고 논문에 썼다면, 그 논문을 읽어본 심사자가 **대상 기계에서 마지막 단계만 돌리면 그 기계용 표가 만들어진다고 설명하는 절**을 가리키며 틀렸다고 했을 것입니다. 그리고 한 번 그런 지적을 받으면 나머지 related work 전체가 의심받습니다.
>
> 그러니 이 연구가 이쪽과의 차이로 내세울 수 있는 것은 **채널 하나입니다.** 준비 비용이나 표의 유지 문제가 아닙니다. 이쪽은 수치를 읽고 이 연구는 이름을 읽습니다. 차이를 하나로 좁히는 것이 오히려 논증을 강하게 만듭니다.

> **이 연구에서는.** 저장소의 related work 초고에 이 연구를 어떻게 다룰지가 적혀 있습니다. 골격이 같다는 것을 서론에서 흐리게 말했다가 뒤에서 축소하는 방식은 쓰지 말라고, 심사자들이 그 두 부분을 대조해서 읽는다고 적혀 있습니다. 골격은 같고 채널이 다르다는 것을 처음부터 분명히 말하는 쪽입니다.

---

## 5장 정리

- 이 갈래는 scheduling 규칙을 사람이 쓰지 말고 기계가 배우게 하자는 발상입니다.
- Decima는 데이터 처리 cluster의 작업 배치를 강화학습으로 배웁니다. 학습이 들어간 자리는 "다음에 어느 task를 실행할까"가 아니라 그보다 위의 배분 결정, 즉 어느 stage를 다음에 돌릴지와 각 job이 쓸 executor 수의 상한입니다. 실제 task 하나를 고르는 일은 기존 방식에 그대로 맡깁니다.
- Decima의 기술적 기여는 강화학습 자체가 아니라 상태와 행동을 학습 가능한 모양으로 바꾼 방법입니다. 크기와 모양이 제각각인 그래프를 평평한 벡터에 담을 수 없어서 그래프 구조를 그대로 읽는 신경망을 쓰고, 한 번에 전부 배정하는 것과 하나씩 배정하는 것 사이의 절충으로 행동을 2차원으로 만들었습니다.
- 보상은 시스템 안에 남은 job 수에 그 상태의 지속 시간을 곱한 벌점입니다. 재고 싶은 것은 평균 완료 시간인데 그건 job이 끝나야 알 수 있으므로, 대기 이론의 법칙을 근거로 매 순간 잴 수 있는 값으로 바꿔 놓았습니다.
- 초록의 "hand-tuned scheduling heuristics"는 본문에서 일곱 개이고, 그중 하나는 조정 인자를 41개 값으로 훑어 실험마다 최적값을 찾아 씁니다. 21퍼센트는 그 가장 강한 상대와의 차이이지 기본값과의 차이가 아닙니다. 두 배는 연속 도착 실험에서 부하가 몰린 특정 두 시간 구간의 값이고, 그 실험의 전체 개선은 29퍼센트입니다.
- 학습 비용은 실험마다 최소 5만 번의 반복입니다. 반복 하나가 병렬 작업자 16개와 GPU 한 장으로 약 1.5초이므로 실험 하나에 20시간 남짓입니다. 학습은 실제 cluster가 아니라 시뮬레이터 위에서 이루어지고, 논문은 그 시뮬레이터의 오차를 따로 검증해 보고합니다.
- Decima는 특정 도착 간격으로만 학습하면 그 분포에 맞춰지고, 범위 전체를 덮는 여러 workload로 학습해야 변화에 견딘다고 스스로 밝힙니다. 학습 때 본 적 없는 종류의 상황에는 약하다는 뜻입니다.
- FIRM은 microservice 환경에서 목표 응답 시간 위반을 다룹니다. 원인 서비스를 찾아내고, 경합 자원을 특정하고, 자원 배분을 조정하는 세 단계 구조입니다. 조절하는 자원이 CPU 시간, 메모리 대역폭, 마지막 단계 캐시 용량, 디스크 입출력 대역폭, 네트워크 대역폭, 컨테이너 수로 여섯 가지이고, 먹이는 수단은 전부 기존 Linux 기능입니다.
- FIRM의 네 벤치마크는 소셜 네트워크, 영화 서비스, 호텔 예약, 기차표 예매이며 각각 서비스가 15개에서 41개입니다. 학습을 위해 일부러 경합을 만들어내는 주입 장치가 따로 있습니다. 목표 위반은 드물게 일어나는데 강화학습은 그 상황을 수없이 겪어야 배우기 때문입니다.
- 초록의 "up to" 셋은 본문에서 범위로 풀립니다. 16배는 두 비교 대상 중 약한 쪽과의 차이이고 강한 쪽과는 9배이며, 62퍼센트는 29에서 62퍼센트라는 범위의 위쪽 끝입니다.
- Park은 이 갈래를 위한 실험 환경으로 열두 개의 시스템 최적화 문제를 하나의 인터페이스로 묶었습니다. 그중 일곱 개는 실제 시스템을 뒤에 붙이고 다섯 개는 시뮬레이터를 씁니다.
- Park의 핵심은 시스템에 강화학습을 쓰는 것이 왜 어려운지에 대한 네 갈래 정리입니다. 첫째, 공간의 대부분에서 보상이 똑같이 나빠 방향을 알 수 없고, 문제마다 맞는 표현을 찾는 일이 아직 풀리지 않은 영역이 있습니다. 둘째, 밖에서 들어오는 일감의 무작위성 때문에 같은 상태에서 같은 행동을 해도 보상이 다르게 나오고, 시스템은 끝나지 않아서 한 판의 결과라는 기준점을 만들 수 없습니다. 셋째, 시뮬레이션과 현실이 다르고 실제 시스템은 느리며 학습 중인 정책이 시스템을 망가뜨릴 수 있습니다. 넷째, 시스템 분야에는 이미 읽을 수 있고 고칠 수 있는 heuristic이 많아서 학습 기반이 이해 가능성에서도 그만큼은 되어야 합니다.
- 이 정리의 인용 가치가 높은 이유는 밖에서 던지는 비판이 아니라 이 갈래를 만든 사람들이 스스로 적은 난점 목록이기 때문입니다. Park의 저자 중 한 명이 Decima의 제1저자입니다.
- 이 갈래의 공통 한계는 둘입니다. 환경이 바뀌면 재학습이 필요하다는 것, 그리고 사람이 미리 정해준 관측 항목과 행동 공간 안에서만 움직인다는 것입니다. 두 번째 때문에 방법이 규칙에서 학습으로 바뀌었을 뿐 읽는 채널은 여전히 행동입니다.
- ASA는 이 연구와 골격이 같습니다. 하나의 정책 대신 일곱 개의 전문 정책을 두고 상황에 맞는 것을 고르며, 정책 교체 기능으로 실제로 바꿉니다. 판정이 흔들리지 않도록 6초 창의 시간 가중 투표를 쓰고, 그 값은 4초보다 짧으면 잡음에 흔들리고 10초보다 길면 늦게 반응한다는 실험으로 정했습니다.
- ASA가 읽는 항목은 CPU, 메모리, 디스크, 프로세스, scheduling, 네트워크의 여섯 갈래 수치입니다. 창에 초점이 있는 프로세스의 사용률과 입력 이벤트 같은 데스크톱 신호가 들어 있지만, 목록 어디에도 프로세스의 이름이 없습니다. 그래서 행동이 같고 의도가 다른 두 상황을 담을 칸이 없습니다.
- ASA의 벤치마크는 대화형 응용 넷과 배경 부하 일곱을 짝지은 28개 상황이고, 이 연구의 데이터셋 구성과 발상이 가깝습니다. 다른 점은 배경 부하가 사용자가 원한 것인지 아닌지를 구분하는 축이 없다는 것입니다.
- ASA의 초록에 있던 이음매는 본문에서 해소됩니다. 기계별 대응표는 사람이 쓰는 것이 아니라 대상 기계에서 후보 scheduler를 전부 돌려보고 채웁니다. 초록의 "재학습 없이"는 인식 모델의 재학습을 가리키는 말이지 기계별 준비가 없다는 뜻이 아닙니다. 이 연구가 내세울 수 있는 차이는 채널 하나로 좁혀지고, 좁히는 편이 논증을 강하게 만듭니다.
- ASA는 인식 정확도를 따로 보고합니다. 28개 상황 분류가 미세 조정 전 96.83퍼센트, 후 99.19퍼센트입니다. 그러므로 인식을 따로 잰다는 발상 자체는 이 연구가 처음이 아니며, 논문에서 그 점을 흐리면 안 됩니다. 다른 것은 무엇을 정답으로 놓았느냐입니다.
- ASA의 초록과 본문에서 같은 값이 다르게 적힌 곳이 있습니다. 상위 세 개 안에 드는 비율이 초록에서는 78.6퍼센트, 본문에서는 78.9퍼센트입니다. 이 연구는 본문 값을 쓰고 차이를 주석으로 남깁니다.

---

# 6장 · LLM을 kernel policy에 쓰는 시도들

## 6.1 이 갈래가 하는 일

앞의 두 갈래는 행동을 읽었습니다. 규칙으로 읽거나 학습된 모델로 읽거나.

이 갈래는 다른 채널을 씁니다. **언어 모델의 지식을 kernel 정책에 끌어옵니다.**

최근 몇 년 사이에 생긴 흐름이고, 이 연구와 가장 가깝습니다. 그래서 이 장이 이 권에서 가장 중요합니다. 논문 심사자가 가장 먼저 찌를 자리이기도 합니다.

> **확인한 방식.** 이 장의 인용문은 원문에서 읽었습니다(2026-09-12 확인). 첫 두 연구는 판본이 여럿이라 어느 판본인지를 매번 밝힙니다. 앞의 연구는 arXiv가 배포하는 최신 판본의 본문을 읽었고, 그보다 긴 이전 판본에만 있는 문장은 그렇다고 표시했습니다. 두 번째 연구는 저자 소속 기관이 공개한 학회 논문 PDF 전문을 읽었습니다. 나머지 둘은 arXiv 원고로만 존재하며 서지 정보와 초록을 arXiv에서 확인했습니다.

## 6.2 SchedCP: 가장 가까운 선행 연구

### 인용

- Zheng, Y., Hu, Y., Zhang, W., & Quinn, A. (2025). Towards Agentic OS: An LLM Agent Framework for Linux Schedulers. arXiv:2509.01245 (v4, 2025-09-30). ML for Systems @ NeurIPS 2025.

이 연구를 정확히 아는 것이 중요합니다. 문제 인식이 거의 같기 때문입니다.

### 판본과 게재 여부

이 논문은 arXiv에 판본이 넷 올라와 있습니다. 2025년 9월 1일, 9월 3일, 9월 26일, 9월 30일 순이고, **네 번째가 최신입니다.** 2026년 9월 12일 기준으로 다섯 번째 판본은 없습니다.

게재 정보도 arXiv의 서지 항목에 붙어 있습니다. 학회 게재란에 **ML for Systems 2025**라고 적혀 있습니다. 앞에서 정리한 대로 이것은 정식 학회가 아니라 workshop이고, 그래서 주장의 범위를 workshop 수준으로 읽어야 합니다.

판본마다 길이가 다르다는 점이 중요합니다. 두 번째 판본은 정식 학회 형식의 긴 원고이고, 최신 판본은 workshop 형식의 짧은 원고입니다. 길게 썼다가 다시 짧은 형태로 돌아온 것입니다.

**그러니 "이 논문에 무엇이 적혀 있다"고 말할 때 어느 판본인지를 밝혀야 합니다.** 긴 원고에만 있는 내용을 짧은 판본을 인용하며 쓰면 안 됩니다.

아래에서는 최신 판본에 있는 문장은 그냥 인용하고, **긴 판본에만 있는 문장은 그렇다고 표시합니다.**

### 후속 논문이 나왔는지 확인했습니다

이 연구의 인용 기록에는 이 문헌에 대해 "제출할 때마다 후속 논문이 나왔는지 다시 확인할 것"이라는 메모가 붙어 있습니다. 이 갈래가 빠르게 움직이기 때문입니다. 그 확인을 했습니다.

**같은 저자들이 낸 Linux scheduler 후속 논문은 없습니다.** 2026년 9월 12일 기준으로, 이 논문의 저자 중 한 명이 참여한 arXiv 원고를 전부 훑었습니다. 그 사이에 여러 편이 나왔지만 scheduler 정책을 다루는 것은 없습니다. 가장 가까운 것이 GPU를 대상으로 같은 확장 방식을 적용한 연구인데, 대상이 다릅니다.

**다른 연구팀에서 나온 인접 연구는 둘 있습니다.** 이 권을 쓸 때까지 이 연구의 인용 기록에 없던 것이라 여기 적어둡니다.

하나는 kernel 설정을 언어 모델로 조율하는 연구입니다(arXiv:2605.15026, v2 2026-07-14). 최대 41개의 Linux 설정 항목을 살아 있는 호스트에서 조율하고, 빠른 순환과 느린 순환을 나누며, 모든 변경이 형식 검증을 거친 뒤에야 kernel에 닿습니다. 이 연구의 검증기와 같은 발상입니다.

다른 하나는 시스템 heuristic 자체를 언어 모델로 합성하는 연구입니다(arXiv:2512.25065, v2 2026-06-16). 언어 모델이 쓸 수 있는 코드를 **상태 없는 결정 함수**로 제한하고, 제약된 언어로만 쓰게 해서 안전 성질을 구조적으로 보장합니다. 대상은 가상 기계 배치, 캐시 축출, 계층형 메모리입니다.

> **이 연구에서는.** 두 번째 연구의 발상이 이 연구와 같은 방향입니다. **언어 모델의 출력이 닿을 수 있는 범위를 구조로 좁히면 검증이 쉬워진다**는 것입니다. 이 연구는 그 좁히기를 더 멀리 밀어붙입니다. 출력이 제한된 언어의 코드도 아니고 고정된 어휘의 항목 하나입니다.
>
> 다만 이 두 연구는 서지 정보와 초록만 확인했고 본문은 읽지 않았습니다. 이 연구의 인용 기록에 항목은 만들어뒀지만 **아직 인용할 수 없는 상태로 표시해뒀습니다.** 본문을 읽은 뒤에 related work에 넣을지, 넣는다면 어느 소절에 넣을지를 정해야 합니다.

> **논문으로.** 이 확인 자체가 왜 필요한지가 이 절에서 드러납니다. 이 갈래는 1년 사이에 인접 연구가 둘 더 생겼습니다. 제출 직전에 다시 훑지 않으면 심사자가 아는 논문을 저자가 모르는 상황이 생깁니다.

### 문제 인식

초록의 첫 문장입니다.

> "Operating system schedulers suffer from a fundamental semantic gap, where kernel policies fail to understand application-specific needs, leading to suboptimal performance."

**kernel 정책이 응용의 필요를 이해하지 못하는 근본적인 semantic gap이 있다**는 것입니다.

최신 판본의 서론은 그 결과를 구체적으로 적습니다.

> "Operating system schedulers face a fundamental challenge: kernel policies cannot understand what applications need, leading to suboptimal performance as Linux's EEVDF scheduler applies one-size-fits-all policies to diverse workloads."

앞 장에서 본 그 EEVDF입니다. 기본 scheduler가 다양한 workload에 하나의 정책을 적용한다는 것입니다.

그리고 그 semantic gap이 사람 사이의 간극이기도 하다고 짚습니다.

> "a domain knowledge gap exists between developers and users: DevOps engineers lack insight into workload characteristics (latency-sensitive vs. throughput-oriented), while edge/personal device users lack both kernel optimization expertise and understanding of application-specific targets."

**scheduler를 관리하는 사람은 workload의 성격을 모르고, 개인 기기 사용자는 kernel 지식도 자기 응용의 목표도 모른다**는 것입니다.

긴 판본은 같은 것을 이렇게 적었습니다. 아래 문장은 **긴 판본에만 있습니다.**

> "In cloud platforms, system administrators who manage schedulers are not the developers who understand application behavior."

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

> "SchedCP provides a stable interface with three key services: a Workload Analysis Engine, an evolving Scheduler Policy Repository, and an Execution Verifier that validates all AI-generated code and configurations before deployment with static and dynamic analysis."

**작은 것 하나를 짚어둡니다.** 저자들이 공개한 원고 소스에는 이 문장의 끝이 "code and configure"로 되어 있었는데, 최신 판본에서 "code and configurations"로 고쳐졌습니다. 원고 소스를 읽고 옮겼다면 틀린 문장을 인용할 뻔했습니다. 최종 판본을 확인해야 하는 이유가 이런 것입니다.

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

> "The Planning Agent transforms profiles into optimization strategies via the Scheduler Policy Repository, following a decision hierarchy: configuring existing schedulers, generating patches, or composing new schedulers from primitives."

**기존 scheduler의 설정을 바꾸는 것이 1순위, 코드를 부분 수정하는 것이 2순위, 새로 만드는 것이 마지막**입니다.

긴 판본은 각 단계의 조건까지 적었습니다. 아래는 **긴 판본에만 있는 문장입니다.**

> "For existing production-ready scheduler solutions with strong performance history, it configures parameters. For partial matches, it retrieves code and generates patches. When no suitable base exists, it composes new schedulers from algorithm primitives."

**실행 에이전트**가 코드를 만들어 검증기에 넘기고, **학습 에이전트**가 결과를 분석해서 저장소를 갱신합니다.

### 결과

원고의 평가 부분에서 옮깁니다.

**커널 빌드.**

> "For kernel compilation (tinyconfig, "make -j 172" on 6.14 source), SchedCP achieves 1.63× speedup with scx_rusty initially, then iterative refinement selects scx_layered for 16% additional gain, reaching 1.79× total improvement over EEVDF."

여기서 정확히 읽어야 할 것이 있습니다. **1.79배라는 숫자는 반복을 거친 뒤의 결과이고, 새로 만든 코드가 아니라 기존 scheduler를 고른 결과입니다.** 첫 시도는 1.63배였습니다.

그리고 최신 판본은 workload를 구체적으로 밝힙니다. 최소 설정으로 172개 병렬 작업을 걸어 6.14 소스를 빌드하는 것입니다. 긴 판본에는 절대 시간도 적혀 있습니다. 아래는 **긴 판본에만 있는 문장입니다.**

> "The workload shows 1.63x speedup from 13.57s to 8.31s using scx_rusty as the first attempt."

13.57초가 8.31초가 됐습니다. **원래 13초 걸리던 빌드입니다.** 이 대비가 뒤에서 중요해집니다.

원고가 덧붙인 문장도 의미가 있습니다.

> "Pre-trained RL approaches show no improvement, likely because they require costly hardware/workload-specific retraining."

앞 장에서 정리한 학습 기반 접근의 한계를 이 논문도 같은 이유로 지적하고 있습니다.

**다만 이 문장을 인용할 때 범위를 지켜야 합니다.** 여기서 시험한 강화학습 방식은 앞 장에서 본 cluster 배치 연구가 아닙니다. 이 문장에 붙은 참고문헌은 Linux의 부하 분산에 기계학습을 적용한 사례를 다룬 기사 한 편입니다. 그러니 "이 연구가 앞 장의 연구들을 직접 시험해서 이겼다"고 읽으면 안 됩니다.

**응답 시간 측정 도구.**

> "On schbench, initial AI configuration (scx_bpfland) underperformed, but three refinement iterations identified scx_rusty as superior: 2.11× better P99 latency and 1.60× higher throughput versus EEVDF, demonstrating effective learning from feedback."

**첫 시도가 기본값보다 나빴다는 것을 그대로 적었습니다.** 정직한 보고입니다.

긴 판본에는 그 나빴던 정도가 숫자로 있습니다. 아래는 **긴 판본에만 있는 문장입니다.**

> "While AI configured scheduler initially underperformed with 13% worse P99 latency (46.1ms vs 40.3ms) and 19% lower throughput (741 vs 910 req/s), AI iterative refinement identified scx_rusty as superior."

P99 지연이 13퍼센트 나쁘고 처리량이 19퍼센트 낮았습니다.

**배치 작업.** 여기가 유일하게 새 코드를 만든 사례입니다.

> "For 8 diverse batch workloads (file compression, video transcoding, software testing, data analytics) with long-tail distributions (40 parallel tasks: 39 short, one long), sched-agent correctly identified the optimization goal and workload pattern, implementing Longest Job First (LJF) scheduling to achieve 20% average latency reduction."

짧은 작업 39개와 긴 작업 1개라는 구조를 알아보고 정책을 직접 만들어냈다는 것입니다.

그 정책이 새로 만든 것이라는 점은 긴 판본이 더 분명히 적습니다. 아래는 **긴 판본에만 있는 표현입니다.**

> "generated custom eBPF code implementing a Longest Job First (LJF) scheduling policy—a scheduler not present in our repository"

**저장소에 없던 정책**이라는 것입니다.

### 비용

이 연구가 비용을 정직하게 보고한다는 점이 좋습니다.

분석 한 번의 비용은 최신 판본에 이렇게 적혀 있습니다.

> "Claude Opus successfully classified all 8 workloads at \$0.15 per analysis"

긴 판본의 표현은 이렇습니다.

> "The cost for this analysis averaged \$0.15 per workload"

생성 비용은 이렇습니다.

> "Generation efficiency improved 13× (to 2.5 minutes) with \$0.45 synthesis cost per workload."

긴 판본은 같은 것을 이렇게 적었습니다. 아래는 **긴 판본에만 있는 문장이고, 금액이 다릅니다.**

> "In addition to performance gains, our framework's optimizations reduced generation costs per iteration: time fell from 33 to 2.5 minutes (a 13x reduction), and the monetary cost dropped from \$6 to \$0.5."

긴 판본은 0.5달러, 최신 판본은 0.45달러입니다. 시간은 둘 다 2.5분이고 13배 개선이라는 서술도 같습니다. **어느 판본을 인용하느냐에 따라 옮겨 적을 숫자가 달라지는 실제 사례입니다.**

그리고 최적화 전의 상태를 이렇게 적습니다.

> "The successful generation required 33 minutes, 221 LLM API calls, and 15+ iterations, costing \$6 (vs. 5 minutes typically for an expert developer)."

**33분에 221번의 호출, 15회 이상의 반복, 6달러.** 전문 개발자가 5분이면 하는 일에 대해서입니다. 이 대비를 논문에 스스로 적어둔 것이 인상적입니다.

그리고 그 33분이 세 번의 시도 중 성공한 한 번이라는 것도 밝힙니다.

> "We tested Claude Code, the state-of-the-art LLM agent, with "write a FIFO scheduler in eBPF" from an empty folder, with all permissions and bash access. Of three attempts, only one succeeded. The second attempt produced pseudo-code after 6 minutes trying, and the third generated a scheduler tracer instead after 8 minutes of development."

세 번 중 한 번만 성공했고, 나머지 둘은 각각 6분 뒤에 의사 코드를, 8분 뒤에 엉뚱한 도구를 내놨습니다.

**그리고 이 실패담이 이 논문의 동기입니다.** 언어 모델에게 kernel 접근 권한을 주고 알아서 하라고 하면 이렇게 된다는 것을 보이고, 그래서 제어 계층이 필요하다고 말합니다.

> "The agent required root access, could crash the system during testing, and lacked fallback mechanisms, which also raises safety concerns."

**앞 장에서 본 되돌아가기 장치가 없다는 지적입니다.** 이 갈래가 왜 검증기에 그렇게 공을 들이는지가 여기 있습니다.

**빌드 시간과 비교해보면 이 숫자의 의미가 더 선명해집니다.** 이 연구가 최적화한 커널 빌드가 원래 13.57초입니다. 그 빌드를 8.31초로 줄이기 위해 첫 생성에 33분과 6달러를 썼습니다. 최적화 후에도 2.5분과 0.45달러입니다.
>
> 물론 한 번 만든 정책을 계속 쓰면 되니까 이 대비가 곧바로 손익은 아닙니다. 다만 **판단 한 번의 비용이 최적화 대상보다 훨씬 크다**는 사실은 이 구조가 어떤 환경을 전제하는지를 말해줍니다. 같은 workload가 반복되는 환경입니다.

### hot path에 대한 입장

앞 권에서 언어 모델을 결정 경로에 둘 수 없다는 물리적 제약을 봤습니다. 이 논문도 같은 입장입니다.

> "(4) operating in the control plane to generate optimized code that runs natively with negligible runtime overhead, unlike traditional ML models that would cause unacceptable inference latency in the scheduler hot path."

긴 판본은 여기에 두 문장을 덧붙입니다. 아래 둘은 **긴 판본에만 있습니다.**

> "This control plane separation represents a key architectural insight: LLMs generate and optimize scheduling policies offline, producing native eBPF code that executes without any ML inference overhead during actual scheduling decisions."

> "Deployed on the production-ready sched_ext infrastructure, our approach executes with zero LLM overhead in the critical path"

**다만 이 주장을 뒷받침하는 측정값은 없습니다.** 구조적으로 그렇다는 것이지, 추론 지연을 재서 보인 것이 아닙니다. 언어 모델이 제어 계층에 있고 실행 시점에는 컴파일된 코드만 돌기 때문에 논리적으로 맞는 주장이지만, 숫자는 없습니다.

### 무엇을 평가했는가

이 부분이 이 연구와의 차이에서 가장 중요합니다.

최신 판본은 연구 질문 넷을 한 문장으로 적습니다.

> "We validate SchedCP's effectiveness through four research questions: configuring existing schedulers (RQ1), generating new schedulers for specific workloads (RQ2), cost and efficiency of scheduler generation (RQ3), and iterative refinement improvements (RQ4)."

긴 판본은 같은 넷을 목록으로 적었습니다. 아래는 **긴 판본의 표현입니다.**

> "• RQ1: Can SchedCP effectively configure existing schedulers? • RQ2: Can SchedCP generate new schedulers for specific workloads? • RQ3: What is the cost and efficiency of SchedCP's scheduler generation? • RQ4: How much can sched-agent continue to improve performance after initial attempt?"

**두 판본 모두 넷 다 최종 성능과 비용에 대한 질문입니다.** 기존 scheduler를 잘 설정하는가, 새 것을 만들 수 있는가, 비용은 얼마인가, 반복하면 더 나아지는가.

**언어 모델이 workload를 얼마나 정확히 이해했는가를 따로 재는 질문이 없습니다.**

그리고 흥미로운 흔적이 있습니다. 저자들이 공개한 원고 소스에, 주석 처리되어 제출본에서 빠진 다섯 번째 질문이 남아 있습니다.

> "How effectively can SchedCP understand workloads?"

**이 질문을 넣으려다 뺐다는 뜻입니다.** 왜 뺐는지는 알 수 없습니다. 분량 때문일 수도 있고, 측정 방법을 정하지 못해서일 수도 있습니다.

인식에 관한 서술은 배치 작업 실험 안에 한 문장으로만 나옵니다.

> "Claude Opus successfully classified all 8 workloads at \$0.15 per analysis, while Claude Sonnet failed."

큰 모델은 여덟 개를 다 분류했고 작은 모델은 못 했다는 것입니다. **정확도 표도, 정답 라벨을 만든 절차도, 별도의 인식 평가도 없습니다.** 여덟 개를 다 맞혔다는 한 문장이 전부입니다.

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

검증기가 맞다고 했는데 실제로는 틀린 경우가 아주 드물다는 것입니다. **초록에는 그 비율의 숫자가 없습니다. 본문에는 있습니다.**

### 그 숫자는 2.5퍼센트입니다

논문은 실패를 두 종류로 나누고, 왜 나누는지를 밝힙니다.

> "We split the prompts for which Kgent fails to correctly synthesize an eBPF program into two categories: False Negative (FNs), which are the percentage of prompts for which Kgent fails to synthesize a verified eBPF program, and False Positives (FPs), which are the percentage of prompts for which Kgent synthesizes a verified eBPF program that does not correctly implement the prompt."

**검증을 통과한 프로그램을 아예 못 만든 경우가 앞쪽, 검증은 통과했는데 요청한 일을 하지 않는 경우가 뒤쪽**입니다.

그리고 둘의 무게가 다르다고 말합니다.

> "Conceptually, FPs represent a safety violation since a developer using Kgent may extend their kernel incorrectly when Kgent produces a false positive. In contrast, FNs represent a liveness violation since a developer is effectively unable to use Kgent for such prompts."

**앞쪽은 안전의 문제이고 뒤쪽은 쓸모의 문제**입니다. 못 만들면 못 쓰고 끝이지만, 틀린 것을 맞다고 하면 kernel이 잘못 확장됩니다.

본문의 표가 설계 요소를 하나씩 얹으면서 세 값이 어떻게 변하는지를 보여줍니다.

| 구성 | 만들지 못함 | 틀린 것을 통과시킴 | 정확도 |
|---|---|---|---|
| 직접 생성만 | 67.5% | 2.5% | 30% |
| + 되먹임 | 32.5% | 7.5% | 60% |
| + 이해와 기호 실행 | 17.5% | 5% | 77.5% |
| 사람의 전문 지식으로 대체 | 72.5% | 2.5% | 25% |
| **최종 구성** | **17.5%** | **2.5%** | **80%** |

**최종 구성의 거짓 양성 비율이 2.5퍼센트입니다.**

표를 읽으면 더 흥미로운 것이 보입니다.

> "The results indicate that model-guided feedback plays a large role in improving the accuracy of Kgent, as it improves the accuracy by a factor of 2 (from 30% to 60%). However, this increase in accuracy comes with a factor of 3 increase in false positive rate (from 2.5% to 7.5%)."

**되먹임을 넣으면 정확도가 두 배가 되는데 거짓 양성도 세 배가 됩니다.** 더 자주 성공하게 만드는 장치가 더 자주 잘못 통과시키기도 한 것입니다.

> "Including the comprehension and symbolic execution component also improves Kgent's effectiveness substantially—accuracy improves to 77.5%, while the false positive rate moves to 5%. Including the eBPFNLDataset dataset in training comes with a relatively small impact on Kgent's accuracy—it only improves by 2.5%. However, training using the eBPFNLDataset dataset does bring Kgent's false positive rate back down to the baseline of 2.5%"

기호 실행을 더하면 5퍼센트로 내려가고, 데이터셋을 학습에 넣으면 정확도는 2.5퍼센트포인트만 오르지만 **거짓 양성이 처음 수준인 2.5퍼센트까지 내려옵니다.**

> **논문으로.** 이 표가 좋은 ablation study의 본보기입니다. 구성 요소를 하나씩 얹으면서 **좋아지는 지표와 나빠지는 지표를 함께** 보여줍니다. 정확도만 보고했다면 되먹임이 거짓 양성을 세 배로 늘린다는 사실이 묻혔을 것입니다.
>
> 이 연구의 실험 설계에도 같은 요구가 있습니다. 인식의 정확도만 보면 안 되고, 틀렸을 때 어떤 종류로 틀리는지를 함께 봐야 합니다. 안전한 실패와 위험한 실패를 구분하지 않으면 지표가 거짓말을 합니다.

> **이 연구에서는.** 이 논문이 다루는 문제는 이 연구와 다르지만, 한 가지 발상이 공통됩니다. **언어 모델의 출력을 그대로 믿지 않고 검증기를 통과시킨다**는 것입니다.
>
> 이 연구에도 검증기가 있습니다. 언어 모델이 내놓은 설정이 허용된 어휘와 값 범위 안에 있는지 확인하고, 벗어나면 거부하거나 범위 안으로 끌어당깁니다. 앞의 연구처럼 코드를 검증하는 것이 아니라 값을 검증하는 것이라 훨씬 단순합니다. 출력이 코드가 아니라 신호이기 때문에 가능한 단순함입니다.

## 6.4 인접한 두 시도

### kernel 설정 조율

- Lin, H., Li, Y., Luo, H., Lin, Z., Zhang, L., Xing, M., & Wu, Y. (2025). TuneAgent: Agentic Operating System Kernel Tuning with Reinforcement Learning. arXiv:2508.12551 (v2, 2026-05-31).

kernel의 설정 항목을 언어 모델과 강화학습으로 조율합니다.

> "Linux kernel tuning is essential for optimizing operating system (OS) performance, yet remains challenging due to the complex kernel space, sparse performance feedback, and strong workload sensitivity."

**설정 공간이 복잡하고, 성능 신호가 드물게 오고, workload에 민감하다**는 것이 어려움입니다.

> "TuneAgent formulates the kernel space as a constrained RL environment, enabling large language models (LLMs) to autonomously explore the kernel while enforcing valid and precise configuration modifications."

결과는 최대 5.6퍼센트 개선입니다.

> **인용 정보 정정.** 이 논문의 서지 정보에서 세 가지를 확인했고, 그중 둘은 정정입니다(2026-09-12 확인).
>
> **첫째, 제목이 바뀌었습니다.** 첫 판본의 제목은 "OS-R1: Agentic Operating System Kernel Tuning with Reinforcement Learning"이었습니다. 시스템 이름 자체가 OS-R1에서 TuneAgent로 바뀌었습니다.
>
> **둘째, 저자 한 명이 바뀌었습니다.** 일곱 명 중 네 번째가 첫 판본에서는 Kaichun Yao이고 현재 판본에서는 Zhenghong Lin입니다. 나머지 여섯 명은 같습니다.
>
> 두 판본은 2025년 8월 18일과 2026년 5월 31일에 올라왔습니다. 초록도 다시 쓰였습니다. 첫 판본은 "효율, 확장성, 일반화" 세 가지를 어려움으로 들었는데, 현재 판본은 "복잡한 kernel 공간, 드문 성능 신호, 강한 workload 민감성"으로 바뀌었습니다. 최대 5.6퍼센트라는 결과 숫자는 두 판본이 같습니다.
>
> **셋째, 게재 학회는 저자들의 저장소에만 적혀 있습니다.** 저장소의 설명 문서 첫머리에 KDD 2026이라고 명시되어 있습니다. 다만 arXiv의 서지 정보에는 학회 게재란이 비어 있고, 이 권을 쓰는 환경에서 그 학회의 논문집에 접근할 수 없어 논문집 쪽 서지 정보는 확인하지 못했습니다.
>
> 그러니 지금 말할 수 있는 것은 **"저자들이 자기 저장소에 KDD 2026 게재라고 적어두었다"**까지입니다. 제출 전에 논문집에서 쪽 번호와 식별자를 확정해야 합니다.

> **논문으로.** 이 사례가 arXiv 인용을 다시 확인해야 하는 이유를 한꺼번에 보여줍니다. 시스템 이름이 바뀌었고, 저자가 바뀌었고, 초록이 다시 쓰였고, 게재 정보가 생겼습니다.
>
> 특히 **시스템 이름이 바뀐 것이 위험합니다.** 첫 판본을 읽고 "OS-R1이라는 연구가 있다"고 적어뒀다면, 지금 그 이름으로 검색해도 나오지 않습니다. 반대로 두 연구를 별개로 세어 참고문헌에 둘 다 올리는 실수도 가능합니다.

### 고성능 컴퓨팅 작업 배치

- Jadhav, P., Jin, H., Deelman, E., & Balaprakash, P. (2025). Evaluating the Efficacy of LLM-Based Reasoning for Multiobjective HPC Job Scheduling. arXiv:2506.02025 (v2, 2025-09-03).

**판본과 게재 여부를 확인했습니다.** 2026년 9월 12일 기준으로 두 번째 판본이 최신이고, 2025년 9월 3일 이후 개정되지 않았습니다. 서지 정보의 비고란에 "work under review"라고 적혀 있습니다. **아직 심사 중이고 게재된 곳이 없습니다.**

이쪽은 접근이 다릅니다. **언어 모델이 scheduler 자체입니다.**

> "we propose a novel Large Language Model (LLM)-based scheduler using a ReAct-style framework (Reason + Act), enabling iterative, interpretable decision-making. The system incorporates a scratchpad memory to track scheduling history and refine decisions via natural language feedback, while a constraint enforcement module ensures feasibility and safety."

추론하고 행동하는 것을 번갈아 하면서 배치 결정을 직접 내립니다. 제약 조건을 강제하는 별도 모듈이 안전을 담당합니다.

무엇으로 시험했는지도 초록에 있습니다.

> "We evaluate our approach using OpenAI's O4-Mini and Anthropic's Claude 3.7 across seven real-world HPC workload scenarios, including heterogeneous mixes, bursty patterns, and adversarial cases etc. Comparisons against FCFS, SJF, and Google OR-Tools (on 10 to 100 jobs) reveal that LLM-based scheduling effectively balances multiple objectives"

**모델 둘, 상황 일곱, 작업 10개에서 100개**입니다. 비교 대상은 앞 권에서 배운 FCFS와 SJF, 그리고 최적화 도구 하나입니다.

작업 수가 100개까지라는 점을 기억해두세요. 앞 권에서 본 데스크톱의 task 수가 수백 개였습니다.

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

- 이 갈래는 언어 모델의 지식을 kernel 정책에 끌어옵니다. 이 연구와 가장 가까우므로 정확히 알아야 합니다.
- SchedCP는 arXiv 판본이 넷이고 최신은 네 번째이며, 서지 정보의 학회 게재란에 ML for Systems 2025가 적혀 있습니다. workshop이므로 주장의 범위를 그 수준으로 읽어야 합니다. 판본마다 길이가 달라서, 긴 판본에만 있는 문장을 짧은 판본을 인용하며 쓰면 안 됩니다. 이 장은 어느 판본의 문장인지를 매번 밝힙니다.
- 후속 논문 확인 결과, 같은 저자들이 낸 Linux scheduler 후속 논문은 없습니다. 다만 다른 연구팀에서 인접 연구가 둘 나왔습니다. kernel 설정을 언어 모델로 조율하면서 모든 변경을 형식 검증에 통과시키는 연구와, 언어 모델이 쓸 수 있는 코드를 상태 없는 결정 함수로 제한해 안전 성질을 구조적으로 보장하는 연구입니다. 뒤엣것의 발상이 이 연구와 같은 방향이고, 이 연구는 그 좁히기를 더 멀리 밀어붙입니다.
- 판본 대조에서 실제로 달랐던 곳이 있습니다. 원고 소스의 "code and configure"가 최신 판본에서 "code and configurations"로 고쳐졌고, 생성 비용이 긴 판본의 0.5달러에서 최신 판본의 0.45달러로 달라졌습니다. 원고 소스만 읽고 옮겼다면 틀린 문장과 틀린 숫자를 인용할 뻔했습니다.
- SchedCP가 가장 가까운 선행 연구입니다. 문제 인식이 거의 같습니다. kernel 정책이 응용의 필요를 이해하지 못하는 semantic gap이 있고, 그 해법은 더 좋은 모델이 아니라 의미 추론과 실행을 분리하는 제어 계층이라는 것입니다.
- 구성 요소가 셋입니다. 단계별 접근을 제공하는 workload 분석 엔진, scheduler 프로그램 저장소, 그리고 인공지능이 만든 코드를 세 겹으로 검증하는 검증기입니다. kernel의 BPF 검사기만으로 부족하다고 보고 starvation과 불공정을 잡는 정적 분석을 얹은 점이 눈에 띕니다.
- 결과는 커널 빌드에서 반복 세 번 뒤 1.79배, 응답 시간 측정 도구에서 P99 2.11배 개선입니다. 첫 시도가 기본값보다 나빴던 사례도 그대로 보고합니다. 새 코드를 만든 것은 배치 작업 실험 하나이고, 거기서 20퍼센트 개선입니다.
- 비용을 정직하게 보고합니다. 최적화 전에는 33분과 221번의 호출과 6달러가 들었고, 전문 개발자가 5분이면 하는 일이라고 스스로 적었습니다.
- 평가의 연구 질문 넷이 모두 최종 성능과 비용에 관한 것입니다. 언어 모델이 workload를 얼마나 정확히 이해했는가를 따로 재는 질문은 없습니다. 공개된 원고 소스에 그런 질문이 주석 처리된 채 남아 있습니다.
- 이 연구와의 차이는 셋입니다. 출력이 정책이 아니라 신호라는 것, 대상이 서버 작업이 아니라 흘러가는 데스크톱 상황이라는 것, 그리고 인식 자체를 따로 잰다는 것입니다. 마지막이 가장 실질적입니다. 최종 성능만 보면 어느 고리가 끊어졌는지 알 수 없기 때문입니다.
- SchedCP가 제어 계층을 필요하다고 본 이유는 스스로 겪은 실패입니다. 언어 모델 에이전트에게 권한을 주고 eBPF scheduler를 짜라고 했더니 세 번 중 한 번만 성공했고, 성공한 한 번에 33분과 221번의 호출과 6달러가 들었습니다. 그리고 그 에이전트는 root 권한을 요구했고 시험 중에 시스템을 멈출 수 있었으며 되돌아가기 장치가 없었습니다.
- 그 비용을 최적화 대상과 나란히 놓으면 이 구조가 어떤 환경을 전제하는지 보입니다. 최적화한 커널 빌드가 원래 13.57초이고 8.31초가 됐는데, 첫 생성에 33분과 6달러, 최적화 후에도 2.5분과 0.45달러가 듭니다. 같은 workload가 반복되는 환경을 전제한 구조입니다.
- Kgent는 자연어로 kernel 확장을 쓰게 합니다. 언어 모델의 출력을 그대로 믿지 않고 검증기를 통과시킨다는 발상이 이 연구와 공통됩니다.
- Kgent의 거짓 양성 비율은 초록에 없고 본문에 있습니다. 최종 구성에서 2.5퍼센트입니다. 논문은 실패를 둘로 나누는데, 검증을 통과한 것을 못 만드는 실패는 쓸모의 문제이고 틀린 것을 통과시키는 실패는 안전의 문제라고 구분합니다.
- Kgent의 구성 요소별 표가 좋은 ablation study의 본보기입니다. 되먹임을 넣으면 정확도가 30퍼센트에서 60퍼센트로 두 배가 되는데 거짓 양성도 2.5퍼센트에서 7.5퍼센트로 세 배가 됩니다. 좋아지는 지표와 나빠지는 지표를 함께 보여주지 않았다면 묻혔을 사실입니다.
- kernel 설정을 조율하는 연구는 확인 과정에서 세 가지가 드러났습니다. 시스템 이름이 OS-R1에서 TuneAgent로 바뀌었고, 저자 일곱 명 중 한 명이 바뀌었으며, 게재 학회가 저자들의 저장소에만 적혀 있습니다. 이름이 바뀐 것이 특히 위험합니다. 옛 이름으로 검색하면 나오지 않고, 두 연구를 별개로 세는 실수도 가능합니다.
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

### 무엇을 확인했는가

> **확인한 방식.** 제조사가 공개한 개발자 문서를 읽었습니다(2026-09-12 확인). 개념 설명 페이지 하나와 함수 설명 페이지 셋입니다. 아래 인용문은 전부 그 네 페이지에서 나옵니다.
>
> 그리고 **지금 이 문서들은 옛 문서로 분류되어 있습니다.** 개념 페이지의 첫머리에 이렇게 적혀 있습니다.
>
> > "The Game Mode APIs are deprecated in Windows 10, version 1809 and later."
>
> **API가 폐기 예정입니다.** 기능이 없어졌다는 뜻은 아니고, 게임이 이 함수들을 호출해서 상태를 확인하는 방식이 더는 권장되지 않는다는 뜻입니다. 인용할 때 이 사실을 빼면 안 됩니다.

먼저 이 기능이 무엇을 하는지입니다.

> "Game Mode provides customers with the best possible gaming experience by fully utilizing the capacity of their current hardware. It does this by granting a game exclusive or priority access to hardware resources. These resources being dedicated to the game help it hit performance targets more consistently. The performance increase that comes from Game Mode is directly related to the number and impact of other activities running on the device."

**하드웨어 자원에 대한 독점적 또는 우선적 접근**을 준다는 것입니다. 그리고 마지막 문장이 중요합니다. 성능 향상의 크기가 **그 기기에서 돌고 있는 다른 활동의 수와 영향에 정비례한다**고 적혀 있습니다. 다른 것이 아무것도 안 돌면 얻는 것도 없습니다.

### 첫 번째 질문: 게임인지 어떻게 아는가

이것이 이 연구에 가장 중요한 질문이었습니다. 답이 개념 페이지에 있습니다.

> "Game Mode works by default for most Windows games, requiring no action or opt-in by the customer, and no work by the game developer."

**대부분의 Windows 게임에서 기본으로 동작하며, 사용자의 조치도 개발자의 작업도 필요 없습니다.**

그리고 그 옆에 개발자가 명시적으로 선언하는 경로가 따로 있습니다.

> "By using the expandedResources capability, you can explicitly declare that the game will work with Game Mode. As part of launching the game, the process will go into Game Mode with a set of defaults, and you can use the APIs to see what resources are available on the customer's device."

**선언은 할 수 있지만 필수가 아닙니다.** 그리고 그 선언은 아무나 쓸 수 없습니다.

> "This capability is granted on a per-title basis; contact your account manager for more information."

**작품 단위로 허가되고, 담당자에게 문의해야 합니다.**

이제 결론을 확정할 수 있습니다.

**제조사 문서는 판별 방법을 명시하지 않습니다.** 네 페이지 어디에도 목록이라는 말이 없고, 실행 파일 이름을 본다는 말도 없고, 판별을 위해 무엇을 관찰한다는 말도 없습니다. 문서가 말하는 것은 결과뿐입니다. 대부분의 게임에서 저절로 된다는 것입니다.

**그리고 개발자 선언은 판별의 주된 수단이 아닙니다.** 선언 없이도 기본으로 동작한다고 명시되어 있으므로, 선언은 그 위에 얹는 선택지입니다.

> **논문으로.** 이 결론을 어떻게 써야 하는지가 중요합니다. **"게임 모드는 게임 목록을 쓴다"고 쓰면 안 됩니다.** 널리 알려진 이야기이지만 제조사 문서로 뒷받침되지 않습니다.
>
> 쓸 수 있는 것은 이렇습니다. 이 기능은 개발자의 선언 없이 대부분의 게임에서 자동으로 동작하며, **판별 방법은 공개 문서에 기술되어 있지 않습니다.** 닫힌 소프트웨어의 판별 방법을 공개 문서로 확인할 수 없다는 것 자체가 하나의 사실이고, 그 사실이 이 연구가 공개 소프트웨어 쪽을 주된 비교 대상으로 삼는 이유가 됩니다.
>
> 그리고 여기서 인용 규율의 한 갈래를 짚어둡니다. **찾아봤는데 없더라는 것도 확인의 결과입니다.** 아직 확인하지 못했다고 남겨두는 것과, 확인했고 거기에 없다고 확정하는 것은 전혀 다른 진술입니다. 앞엣것은 미완의 숙제이고, 뒤엣것은 **검증 가능한 주장**입니다. 심사자가 그 문서를 열어서 없다는 것을 직접 볼 수 있으니까요.
>
> 그러니 확인 작업의 목표는 모든 칸을 채우는 것이 아닙니다. 각 칸을 **"있고 이렇다" 또는 "찾아봤고 없다"** 중 하나로 만드는 것입니다. 어느 쪽이든 결론이고, 어느 쪽도 아닌 상태만이 미완입니다.

### 두 번째 질문: 배경 작업을 억누르는가

문서가 "억누른다"는 말을 쓰지는 않습니다. 대신 자원 모형을 통해 같은 것을 말합니다.

독점 자원을 포기하는 함수의 설명이 가장 분명합니다.

> "Opts out of CPU exclusivity, giving the app access to all cores, but at the cost of having to share them with other processes."

**독점을 포기하면 모든 core를 쓸 수 있게 되지만 다른 프로세스와 나눠 써야 합니다.** 뒤집어 읽으면, 독점 상태에서는 다른 프로세스가 그 core에 들어오지 못한다는 뜻입니다.

개념 페이지가 그 대가를 더 구체적으로 적습니다.

> "they may opt-out of CPU exclusivity by calling ReleaseExclusiveCpuSets to get access to all cores, but at a higher latency due to other processes and system activities being scheduled on the same cores as the game"

**다른 프로세스와 시스템 활동이 게임과 같은 core에 배치되기 때문에 지연이 높아진다**는 것입니다.

그러니 답은 이렇습니다. **배경 작업을 느리게 만들지는 않지만, 게임에 배정된 core에서 내보냅니다.** 억제가 아니라 격리입니다.

CPU 말고 다른 자원도 언급됩니다.

> "After this function is called, the app will still have access to other Game Mode resources, such as increased GPU prioritization."

**GPU 우선순위 상향**이 따로 있고, 그것은 CPU 독점을 포기해도 유지됩니다.

메모리는 또 다릅니다.

> "While CPU resources may be revoked if the game exits Game Mode, memory resources, once granted, will never be revoked."

**메모리는 한 번 주면 회수하지 않습니다.**

자원마다 규칙이 다르다는 점이 흥미롭습니다. core는 뺏을 수 있고, 메모리는 못 뺏습니다. 앞 권에서 배운 것을 떠올리면 당연합니다. core는 다음 순간에 다른 task를 올리면 그만이지만, 메모리는 안에 든 내용을 어디론가 옮겨야 뺏을 수 있습니다.

### 세 번째 질문: 업데이트나 알림을 미루는가

> **확인 필요.** 이 항목만 확인하지 못했습니다.
>
> 게임 중에 업데이트 설치나 재시작 알림을 미룬다는 서술은 널리 퍼져 있고, 실제로 Windows의 설정 화면에 그런 문구가 있다고 알려져 있습니다. 그러나 **제조사가 발행한 문서 중 이 권에서 읽을 수 있었던 것에는 그 서술이 없습니다.** 위의 네 페이지 어디에도 업데이트, 드라이버 설치, 재시작 알림에 대한 언급이 없습니다.
>
> 그 서술을 담고 있을 법한 제조사의 지원 문서가 하나 있는데, 그 페이지는 내용을 스크립트로 그려내는 방식이라 이 권을 쓰는 환경에서 본문을 읽을 수 없었습니다. 제3자 매체와 커뮤니티 글에는 같은 문장이 여러 곳에 있지만, 이 연구의 인용 규율상 그것으로는 뒷받침되지 않습니다.
>
> 확인해야 할 것은 하나입니다. **제조사가 발행한 문서에 게임 중 업데이트나 알림을 미룬다는 서술이 있는가.** 있으면 그 문서를 인용하고, 없으면 없다고 확정해서 적어야 합니다.

### 그 밖에 확인된 것들

**독점 자원에는 조건이 붙습니다.**

> "The app must be in the foreground and have focus before exclusive resources are granted."

**전면에 있고 초점을 가지고 있어야** 독점 자원을 받습니다. 이 문장은 함수 설명 세 페이지에 모두 반복됩니다.

**상태가 실행 중에 바뀝니다.** 현재 상태를 알려주는 함수의 설명입니다.

> "Gets the current resource state (that is, whether the app is running in Game Mode or shared mode)."

> "This function should be called during each iteration of the game loop to check when the app enters and exits Game Mode so that the appropriate settings can be applied."

**게임 루프를 돌 때마다 확인하라**고 되어 있습니다. 상태가 실행 중에 바뀔 수 있다는 뜻입니다.

개념 페이지가 언제 바뀌는지를 예로 듭니다.

> "When exclusive resources are revoked, such as when the game loses focus, the game will discover this by polling with HasExpandedResources, and can re-scale as appropriate. Some games may reduce the level of detail or use other tactics to maintain performance."

**초점을 잃으면 독점 자원이 회수되고**, 게임은 그것을 감지해서 화면 품질을 낮추는 식으로 대응할 수 있습니다.

**사용자가 끌 수 있습니다.** 받을 수 있는 core 수를 알려주는 함수의 설명입니다.

> "Gets the expected number of exclusive CPU sets that are available to the app when in Game Mode."

> "This function returns 0 if no exclusive CPU sets are available, or if the customer opted out of Game Mode via the Settings in Windows 10."

설정에서 끄면 0을 돌려줍니다.

### 여기서 읽을 수 있는 것

**자원 모델이 구체적입니다.** 막연한 우선순위 상향이 아니라 **독점적인 CPU 집합**입니다. 특정 core를 이 응용에만 배정한다는 뜻입니다. 그리고 자원마다 회수 규칙이 다릅니다. core는 초점을 잃으면 회수되고, 메모리는 한 번 주면 회수하지 않습니다.

**전면과 초점이 조건입니다.** 앞 권에서 Windows가 전면 창을 우대한다고 했는데, 게임 모드에서도 같은 조건이 붙습니다. 시스템이 "사용자가 지금 이걸 보고 있다"는 정보를 알고 있고 그걸 씁니다.

**사용자가 끌 수 있습니다.** 설정에서 끄면 함수가 0을 돌려줍니다.

**그리고 판별 방법은 문서에 없습니다.** 자동으로 된다는 사실만 있습니다.

> **이 연구에서는.** 마지막 항목이 이 연구의 실험 설계에 영향을 줍니다. 이 연구는 이름 목록 기반 인식을 비교 조건으로 두는데, **그 조건을 이 시스템에서 재현할 수 없습니다.** 판별 방법이 공개되어 있지 않으니 충실히 재현했다고 주장할 근거가 없습니다.
>
> 그래서 재현의 대상은 다음 절의 공개 소프트웨어입니다. 그쪽은 규칙 파일이 전부 공개되어 있어서, "이 카탈로그를 이렇게 재현했다"를 검증 가능한 형태로 적을 수 있습니다.

> **논문으로.** 그러니 논문에서 이 시스템을 다룰 때는 **존재와 자원 모델까지만** 쓰고, 판별 방법은 공개 문서에 기술되어 있지 않다고 적는 것이 정확합니다. 그리고 그 사실이 다음 절의 공개 소프트웨어를 baseline으로 택한 이유가 됩니다. 저장소의 related work 초고가 택한 방향도 이쪽입니다.

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

가장 널리 쓰이는 카탈로그 하나를 **2026년 9월 12일에 내려받아** 세어봤습니다. 그 시점의 최신 변경은 나흘 전인 9월 8일이고, 커밋은 `03ef03fb`입니다.

> **세는 방법을 밝혀둡니다.** 규칙 파일은 확장자가 `.rules`인 파일 전부입니다. 항목은 각 파일에서 비어 있지 않고 `#`으로 시작하지 않는 줄 하나를 JSON 객체 하나로 읽어 셌습니다. 파일을 하나로 이어 붙여서 세면 줄 끝이 없는 파일 때문에 항목 둘이 한 줄로 붙어 잘못 세어집니다. 아래 숫자는 파일별로 따로 읽은 결과입니다.
>
> 이 카탈로그는 계속 바뀌므로, 숫자를 쓸 때는 **확인 날짜와 커밋을 함께 적어야** 합니다. 다시 세면 다른 값이 나옵니다.

### 분류 정의

카탈로그의 분류 정의 파일 전체입니다. 주석까지 그대로 옮깁니다.

```text
# Type: Game
# Use more CPU time if possible
# Games do not always need more IO, but in most cases can be hungry for CPU
{ "type": "Game", "nice": -5, "ioclass": "best-effort", "sched": "normal" }

# Type: Player Audio/Video
# Try to add more CPU power to decrease latency/lags
# Try to add real time io for avoiding lags
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

# Type: Indifference
{ "type": "IN_DIFF", "nice": 0, "ioclass": "best-effort", "ionice": 7 }

# Type: Adj OOM Score
{ "type": "OOM_KILL", "oom_score_adj": 1000 }
{ "type": "OOM_NO_KILL", "oom_score_adj": -1000 }
```

**정의는 열다섯 개입니다.**

마지막 세 개가 성격이 다릅니다. `IN_DIFF`는 이름이 "무관심"이고 `nice` 값이 0입니다. **아무것도 하지 않는다는 것을 명시하는 분류**입니다. 그리고 마지막 둘은 CPU가 아니라 메모리가 부족할 때 누구를 먼저 죽일지를 정합니다. 1000은 먼저 죽이라는 뜻이고 -1000은 죽이지 말라는 뜻입니다.

**이 파일이 앞 권에서 말한 "사람이 손으로 적어 넣은 의미"의 순수한 형태입니다.**

주석을 읽어보면 사람의 판단이 그대로 드러납니다. 게임은 입출력보다 CPU가 급하다. 배경 작업은 필요하긴 하지만 최대한 조용해야 한다. 무거운 계산은 충분히 빨라야 하지만 시끄러우면 안 된다.

전부 맞는 판단입니다. 그리고 전부 사람이 앉아서 생각해서 적은 것입니다.

### 규모

카탈로그를 세어보면 이렇습니다.

| 항목 | 수 |
|---|---|
| 규칙 파일 | 361개 |
| 개별 규칙 항목 | 15,813개 |
| 그중 게임으로 분류된 것 | 13,528개 |

**전체의 85.5퍼센트가 게임 하나의 분류입니다.**

분류별로 세어보면 이렇습니다.

| 분류 | 항목 수 | 비율 |
|---|---|---|
| Game | 13,528 | 85.5% |
| BG_CPUIO | 1,615 | 10.2% |
| Service | 194 | 1.2% |
| Doc-View | 160 | 1.0% |
| LowLatency_RT | 109 | 0.7% |
| Chat | 51 | 0.3% |
| Heavy_CPU | 33 | 0.2% |
| Image-View | 32 | 0.2% |
| Player-Audio | 28 | 0.2% |
| Player-Video | 24 | 0.2% |
| Launcher | 24 | 0.2% |
| IN_DIFF | 10 | 0.1% |
| OOM_NO_KILL | 2 | 0.0% |
| TODO | 1 | 0.0% |
| (분류 없음) | 2 | 0.0% |

**이 표가 앞 권에서 말한 열거의 한계를 숫자로 보여줍니다.**

게임 하나를 알아보기 위해 13,528개의 항목이 필요합니다. 그리고 게임은 계속 나옵니다. 이 카탈로그는 나흘 전에도 갱신됐습니다.

그리고 실제로 쓰이는 분류가 열세 가지입니다. 정의된 열다섯 중 둘(`BG_CPU`와 `OOM_KILL`)은 쓰는 항목이 하나도 없습니다. **항목이 만 오천 개가 넘는데 구분되는 상황은 열세 가지입니다.**

### 표 끝의 잔해

세는 과정에서 표가 손으로 관리된다는 흔적이 몇 개 나왔습니다. 작지만 이 갈래의 성격을 보여주는 것들이라 적어둡니다.

**분류가 `TODO`인 항목이 하나 있습니다.** `TODO`는 분류 정의 파일에 정의되어 있지 않습니다. 어떤 프로그램을 어디에 넣을지 정하지 못한 채 자리만 잡아둔 것입니다.

**분류 없이 설정값만 적힌 항목이 둘 있습니다.** 분류를 거치지 않고 `nice` 값을 직접 적었습니다.

**JSON으로 읽히지 않는 줄이 하나 있습니다.** 어떤 게임 항목의 줄 끝에 `+` 문자 하나가 남아 있습니다.

> **이 연구에서는.** 이 잔해들이 앞 권에서 말한 노후화의 한계를 추상적인 말이 아니라 눈에 보이는 형태로 보여줍니다. 만 오천 개의 줄을 사람이 관리하면 정의되지 않은 분류가 섞이고, 형식을 벗어난 줄이 남습니다.
>
> 그리고 이것이 이 연구의 비교 조건을 만들 때 **판단이 필요한 지점**이기도 합니다. 이름 목록 조건을 충실히 재현한다고 할 때, 이런 잔해까지 재현해야 할까요. 재현하면 원본에 충실하지만 비교가 지저분해지고, 정리하면 깨끗하지만 실제보다 나은 목록을 상대로 이기는 셈이 됩니다.
>
> 이 연구는 **정리하는 쪽**을 택합니다. 비교 조건은 이름 목록 방식이 최선일 때 어디까지 할 수 있는지를 보여야 하기 때문입니다. 형식 오류 때문에 이기면 그건 이긴 것이 아닙니다. 그리고 그 선택을 문서에 적어둡니다.

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
- Windows의 게임 모드는 제조사의 개발자 문서 네 페이지에서 확인했습니다. 자원 모델은 독점 CPU 집합과 GPU 우선순위 상향이고, 전면에 있고 초점을 가져야 독점 자원을 받으며, 초점을 잃으면 회수됩니다. 메모리는 한 번 주면 회수하지 않습니다. 사용자가 설정에서 끌 수 있습니다. 이 API들은 Windows 10 버전 1809부터 폐기 예정으로 표시되어 있습니다.
- 게임 판별 방법은 **제조사 문서에 명시되어 있지 않습니다.** 문서가 말하는 것은 "대부분의 Windows 게임에서 사용자의 조치도 개발자의 작업도 없이 기본으로 동작한다"까지입니다. 개발자가 명시적으로 선언하는 경로가 따로 있지만 필수가 아니고 작품 단위로 허가받아야 합니다. 그러므로 "게임 모드는 게임 목록을 쓴다"고 논문에 쓸 수 없습니다. 쓸 수 있는 것은 판별 방법이 공개 문서에 기술되어 있지 않다는 사실이고, 그 사실 자체가 공개 소프트웨어 쪽을 비교 대상으로 택한 이유가 됩니다.
- 배경 작업에 대해서는 억제가 아니라 격리입니다. 독점을 포기하면 "다른 프로세스와 나눠 써야 하고", "다른 프로세스와 시스템 활동이 게임과 같은 core에 배치되기 때문에 지연이 높아진다"고 적혀 있습니다. 뒤집어 읽으면 독점 상태에서는 그 core에 다른 것이 들어오지 못한다는 뜻입니다.
- 게임 중 업데이트나 알림을 미루는지는 확인하지 못했습니다. 읽을 수 있었던 제조사 문서 어디에도 그 서술이 없고, 그 서술을 담고 있을 법한 지원 문서는 본문을 읽을 수 없는 형태였습니다. 제3자 매체에는 같은 문장이 여럿 있지만 이 연구의 인용 규율상 그것으로는 뒷받침되지 않습니다.
- Linux 쪽의 우선순위 조정 데몬은 전부 공개되어 있습니다. 실행 파일 이름으로 프로세스를 찾아 표를 뒤지고 설정을 적용합니다. 이름이 같아도 실행 인자로 구분할 수 있습니다.
- 설정할 수 있는 항목이 넓습니다. CPU 우선순위, scheduling policy 자체, 입출력 우선순위, 메모리 부족 시 죽일 순서, core 고정까지 포함합니다.
- 널리 쓰이는 카탈로그를 2026년 9월 12일 시점의 커밋 `03ef03fb`에서 직접 세어보니 규칙 파일 361개에 항목 15,813개였고, 그중 13,528개가 게임으로 분류되어 있었습니다. 전체의 85.5퍼센트입니다. 분류 정의는 열다섯 개인데 실제로 쓰이는 것은 열세 가지입니다.
- 이 숫자는 계속 바뀌므로 확인 날짜와 커밋을 함께 적어야 하고, 세는 방법도 적어야 합니다. 파일을 이어 붙여서 세면 줄 끝이 없는 파일 때문에 항목 둘이 한 줄로 붙어 잘못 세어집니다.
- 표에는 손으로 관리된 흔적이 남아 있습니다. 정의되지 않은 `TODO` 분류가 붙은 항목, 분류 없이 설정값만 적힌 항목, 줄 끝에 문자 하나가 남아 형식을 벗어난 줄이 있습니다. 이 연구는 비교 조건을 만들 때 이런 잔해를 재현하지 않고 정리하는 쪽을 택하고, 그 선택을 문서에 적어둡니다. 형식 오류 때문에 이기면 이긴 것이 아니기 때문입니다.
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

가장 오래되고 널리 쓰이는 도구가 있습니다.

> **확인한 방식.** 이 도구는 여러 곳에 복제본이 흩어져 있습니다. 아래 인용문은 **상위 프로젝트의 원본 저장소**에서 읽었습니다(2026-09-12 확인, 저장소 HEAD `fd45df83`). 인용문은 도구의 설명서 파일에서, 기본값은 소스 코드에서 가져왔습니다.
>
> 설명서 파일의 날짜는 2020년 9월 19일이고, 소스 코드가 마지막으로 바뀐 것은 2024년 5월입니다. 즉 **아래 내용은 지금도 유효합니다.**

문서의 설명입니다.

> "Hackbench is both a benchmark and a stress test for the Linux kernel scheduler. It's main job is to create a specified number of pairs of schedulable entities (either threads or traditional processes) which communicate via either sockets or pipes and time how long it takes for each pair to send data back and forth."

**서로 통신하는 task 쌍을 잔뜩 만들어놓고 얼마나 걸리는지 재는 것**입니다.

기본값을 문서에서 옮기면 이렇습니다.

> "Running in process mode with 10 groups using 40 file descriptors each (== 400 tasks)"

> "Each sender will pass 100 messages of 100 bytes"

400개의 task가 100바이트짜리 메시지를 100번씩 주고받습니다.

소스 코드에서 그 기본값들을 직접 확인할 수 있습니다. 메시지 크기 100바이트, 반복 100회, 그룹 10개, 그룹당 file descriptor 20개입니다. 마지막 값이 20인데 위의 출력에 40으로 나오는 이유는, 보내는 쪽과 받는 쪽이 각각 그만큼 연다고 설명서가 밝히기 때문입니다.

> "Defines how many file descriptors each child should use. Note that the effective number will be twice the amount you set here, as the sender and receiver children will each open the given amount of file descriptors."

그래서 10 × 20 × 2 = 400개의 task가 됩니다.

**이 도구가 재는 것은 처리량입니다.** 전부 끝나는 데 걸린 시간 하나입니다. 누가 얼마나 기다렸는지, 반응이 빨랐는지는 재지 않습니다.

설명서의 예시 출력에 그 값이 딱 한 줄로 나옵니다. `Time: 0.890`. **숫자가 하나뿐입니다.**

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

### 다른 제조사의 사무용 벤치마크

같은 종류의 도구를 다른 단체가 만든 것이 있습니다. 이 연구의 인용 기록에서 사무용 시나리오 분류의 주 근거로 지정한 문헌입니다.

> **확인한 방식.** 이 제조사의 웹 사이트는 이 권을 쓰는 환경의 요청을 거부했습니다. 그래서 **같은 주소의 문서를 인터넷 아카이브가 보관한 사본**에서 읽었습니다(2026-09-12 확인). 제조사가 자기 주소에 올린 PDF 파일 그대로이고, 보관 시점은 2025년 4월 23일입니다. 파일 이름의 판본은 1.2이고, 표지에는 1.1로 적혀 있는데 개정 이력에는 1.2까지 올라 있습니다.
>
> 제조사의 온라인 상점 페이지는 읽을 수 있었고, 시나리오 이름과 설명이 문서와 일치하는 것을 확인했습니다.
>
> 제출 전에 제조사 사이트에서 같은 문서를 직접 받아 판본과 주소를 확정해야 합니다.

시나리오가 넷입니다. 문서의 서술을 그대로 옮깁니다.

**Office Applications.**

> "The Office Applications scenario models office environment like usage including word processing (mail merge, document comparison, and PDF conversion), spreadsheet data manipulation (data modeling, financial forecasting), presentation editing."

**General Productivity.**

> "The General Productivity scenario models OCR of documents, web browsing, application installation, and archiving and unpacking a mixed file data set."

**Photo Editing.**

> "The Photo Editing scenario models editing digital photos (applying filters and creating HDR photos), cataloging digital photos (organizing catalog, use of facial detection to group people)."

**Advanced Content Creation.**

> "The Advanced Content Creation scenario encodes video with a CPU render and GPU accelerated workload for SUTs configured with a supported accelerated GPU. A multitasking workload switches between photo editing and video editing workloads."

그리고 이 문서도 어떤 프로그램을 쓰는지를 시나리오별로 밝힙니다.

> "The following applications (grouped by scenario) are installed and/or used by SYSmark 30. Some applications appear in multiple scenarios, but only one instance of the application is installed."

| 시나리오 | 쓰는 프로그램 |
|---|---|
| Office Applications | Microsoft Excel 2021, Outlook 2021, PowerPoint 2021, Word 2021 |
| General Productivity | Adobe Acrobat Pro DC, Audacity 2.3.2(설치 과정용), Corel WinZip 26.0, Google Chrome 106 |
| Photo Editing | Adobe Lightroom Classic 11, Adobe Photoshop CC 23 |
| Advanced Content Creation | Adobe Photoshop CC 23, Adobe Premiere CC 22 |

**버전까지 적혀 있습니다.** 앞의 도구와 마찬가지로, 같은 조건에서 여러 기계를 비교하려면 프로그램의 버전이 고정되어야 하기 때문입니다.

두 가지가 눈에 띕니다.

**Audacity가 "설치 과정용"으로 표시되어 있습니다.** 그 프로그램을 쓰는 것이 아니라 **설치하는 행위 자체**를 workload로 삼습니다. General Productivity의 설명에 "application installation"이 있는 것이 그 뜻입니다.

**앞 권에서 본 배경 작업의 한 종류가 여기 시나리오로 들어와 있습니다.** 프로그램 설치는 디스크를 많이 쓰고 짧게 사는 프로세스를 많이 만듭니다. 이 연구의 데이터셋에도 같은 성격의 작업이 있습니다.

**그리고 네 번째 시나리오가 multitasking을 명시합니다.** 사진 편집과 영상 편집 사이를 오가는 부하입니다. 하나의 작업을 재는 것이 아니라 **여러 작업이 섞인 상황**을 재려는 시도입니다.

> **이 연구에서는.** 마지막 항목이 이 연구와 가장 가깝습니다. 그런데 여기서도 한계가 같습니다. 섞인 상황을 만들기는 하는데, **그 상황이 무엇인지를 시스템에게 알려주는 라벨이 없습니다.** 점수만 나옵니다.
>
> 그리고 이 연구가 이 문헌을 쓰는 범위는 앞의 것과 같습니다. **분류 체계의 존재**까지입니다. "이 단체가 데스크톱 사용을 이 네 시나리오로 나눈다"와 "각 시나리오에 이 프로그램들을 쓴다"는 이 문서로 뒷받침됩니다. "사용자들이 실제로 이렇게 쓴다"는 다른 주장입니다.

### 전문가용 벤치마크 모음

한 가지 더 확인했습니다. 앞의 것과 같은 제조사가 내는 다른 모음입니다. 이 연구의 인용 기록에 조건부로 등재되어 있는데, 조건이 **기기에서 직접 도는 인공지능 작업이 데스크톱 시나리오로 존재하는가**입니다.

> **확인한 방식.** 제조사의 제품 개요 페이지를 읽었습니다(2026-09-12 확인). 아래 인용문은 그 페이지에서 나옵니다. 개별 벤치마크의 기술 문서는 읽지 않았습니다.

모음에 들어 있는 것이 아홉 개이고, 그중 셋이 인공지능 작업입니다.

**기기에서 도는 언어 모델.**

> "The AI Text Generation offers an easier and more compact way for standardized AI performance testing in a variety of local AI LLM use cases."

**local**이라는 단어가 있습니다. 서버에 보내는 것이 아니라 그 기기에서 도는 언어 모델입니다.

**이미지 생성.**

> "This benchmark contains two tests built with different versions of the Stable Diffusion models to cover a range of discrete GPU hardware and features our heaviest AI inference workload yet."

**가장 무거운 추론 workload**라고 스스로 적었습니다.

**컴퓨터 시각.**

> "The workload has been designed around a range of machine vision tasks and AI models, carefully selected based on their use case, relevance and daily impact in the modern office."

**현대적인 사무 환경에서의 일상적 영향**을 기준으로 골랐다고 적혀 있습니다.

> **이 연구에서는.** 조건이 충족됐습니다. **기기에서 직접 도는 인공지능 작업이 상용 데스크톱 벤치마크의 시나리오로 실재합니다.** 이 연구의 데이터셋에 그런 작업을 넣는 근거로 이 페이지를 인용할 수 있습니다.
>
> 다만 인용 등급을 지킵니다. 뒷받침되는 것은 **그런 시나리오가 존재한다**까지입니다. 그 작업이 데스크톱에서 얼마나 흔한지, 어떤 scheduling 특성을 갖는지는 이 페이지로 말할 수 없습니다.

나머지 여섯 개도 이름을 적어둡니다. 사무 생산성, 사진 편집, 영상 편집, 배터리 수명, 한 시간 배터리 소모, 그리고 다중 작업과 웹 탐색 중심의 기본 벤치마크입니다.

마지막 것의 설명에 흥미로운 대목이 있습니다.

> "Procyon Essentials is a multitasking and browsing-focused benchmark, covering real-world workloads that professionals use in everyday life. Like PCMark10, the standard run will not require any third-party software, allowing this benchmark to be accessible to all."

**다중 작업 중심**이고, 앞의 도구처럼 제3자 소프트웨어를 요구하지 않습니다.

그리고 사무 생산성과 사진 편집과 영상 편집은 앞의 것들과 같은 프로그램을 씁니다. 사무는 Word, Excel, PowerPoint, Outlook이고, 사진은 Lightroom과 Photoshop이며, 영상은 Premiere Pro입니다.

**세 제조사가 독립적으로 같은 프로그램 목록에 도달했습니다.** 데스크톱의 대표적 작업이 무엇인지에 대해 업계의 합의가 있다는 뜻입니다.

> **논문으로.** 이 합의 자체가 인용 가치가 있습니다. 이 연구가 데이터셋에 어떤 종류의 작업을 넣을지 정할 때, "우리가 보기에 이게 대표적이다"가 아니라 **"서로 경쟁하는 세 제조사가 전부 이 목록에 도달했다"**고 쓸 수 있습니다.
>
> 다만 세 문헌 모두 배포된 제품의 문서이므로 존재 주장까지입니다. 그리고 세 개가 겹친다는 사실을 "그러므로 사용자들이 이렇게 쓴다"로 옮기면 안 됩니다. 겹치는 이유가 실제 사용 조사일 수도 있고, 서로를 참조했기 때문일 수도 있습니다.

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
- kernel을 괴롭히는 도구 중 오래된 것은 서로 통신하는 task를 400개 만들어 전체 완료 시간을 잽니다. 기본값이 그룹 10개에 그룹당 file descriptor 20개인데, 보내는 쪽과 받는 쪽이 각각 그만큼 열어서 400개가 됩니다. 결과가 숫자 하나뿐인 처리량 도구입니다.
- 더 최근 도구는 core를 놀리지 말 것, 강제로 끌어내리지 말 것, 깨운 뒤 빨리 실행할 것을 목표로 삼고, 깨움 지연과 요청 지연과 초당 처리량을 백분위수로 보고합니다. 앞 권에서 배운 개념들이 그대로 도구의 목표에 들어 있습니다.
- 상호작용성 벤치마크는 대화형 작업 자체를 흉내 냅니다. 오디오는 50밀리초마다 5퍼센트, 영상은 초당 60번에 40퍼센트 같은 식으로 수치가 박혀 있습니다. 게임에 대해서는 CPU 사용이 전혀 대화형이 아니라는 점을 스스로 밝힙니다.
- 작업 모델을 JSON 파일로 기술하는 도구가 있습니다. thread의 동작을 국면으로 나누고 실행, 잠들기, 타이머 같은 기본 동작의 나열로 적습니다. 이 연구 데이터셋의 형식적 선례입니다.
- 상용 데스크톱 벤치마크는 실제 응용을 실제로 돌립니다. 시나리오를 네 묶음으로 나누고 각 묶음에 어떤 프로그램을 버전까지 밝혀 적습니다. 다만 하드웨어를 비교하려고 만든 도구입니다.
- 다른 제조사의 사무용 벤치마크도 시나리오가 넷이고, 문서 작업, 일반 생산성, 사진 편집, 고급 콘텐츠 제작입니다. 프로그램 설치 자체를 workload로 삼는 항목과, 사진 편집과 영상 편집 사이를 오가는 다중 작업 항목이 있습니다. 섞인 상황을 만들기는 하지만 그 상황이 무엇인지를 알려주는 라벨은 없고 점수만 나옵니다.
- 전문가용 벤치마크 모음에는 기기에서 직접 도는 언어 모델, 이미지 생성, 컴퓨터 시각 작업이 시나리오로 들어 있습니다. 기기에서 도는 인공지능 작업이 데스크톱 시나리오로 실재한다는 근거가 됩니다.
- 세 제조사가 독립적으로 거의 같은 프로그램 목록에 도달했습니다. 데이터셋에 넣을 작업을 고를 때 "우리가 보기에 이게 대표적이다"가 아니라 그 합의를 근거로 쓸 수 있습니다. 다만 셋 다 배포된 제품의 문서이므로 존재 주장까지이고, 겹친다는 사실을 실제 사용 행태에 대한 주장으로 옮기면 안 됩니다.
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

**한 논문은 시스템 이름이 바뀌었습니다.** 첫 판본과 지금 판본의 제목이 다르고, 저자 일곱 명 중 한 명도 다릅니다. 옛 이름으로 검색하면 지금 판본이 나오지 않고, 반대로 두 판본을 별개의 연구로 세는 실수도 가능합니다.

**한 논문은 길이가 오갔습니다.** 짧은 형태로 올라갔다가 학회 형식의 긴 원고가 됐다가 다시 짧은 형태로 돌아왔습니다. 그래서 "이 논문에 이렇게 적혀 있다"고 말할 때 어느 판본인지가 중요합니다. 실제로 그 논문의 어떤 문장은 최종 판본에서 표현이 고쳐졌고, 어떤 금액은 값 자체가 달라졌습니다.

**한 논문은 게재 정보가 생겼습니다.** 그 사이에 workshop 게재가 확정되어 서지 정보에 반영됐습니다. 다른 논문은 저자들의 저장소에만 게재 학회가 적혀 있고 서지 정보에는 아직 없습니다. 그런 경우에는 **"저자들이 자기 저장소에 그렇게 적어두었다"까지만** 말할 수 있습니다.

**한 논문은 판본이 하나 그대로였습니다.** 그것도 확인의 결과입니다. 심사를 통과한 곳이 아직 없다는 뜻이고, 인용할 때 그 사실을 밝혀야 합니다.

**그러니 제출 직전에 다시 확인하는 절차가 필요합니다.** 이 연구의 인용 기록에는 가장 가까운 선행 연구에 대해 "제출할 때마다 후속 논문이 나왔는지 다시 확인할 것"이라는 메모가 명시되어 있습니다. 이 권의 확인으로 그 메모가 옳다는 것이 다시 확인됐습니다. 그 연구팀의 후속 논문은 없었지만, **다른 연구팀에서 인접 연구가 둘 나와 있었습니다.** 확인하지 않았다면 몰랐을 것입니다.

### 확인은 남을 깎는 일이 아닙니다

한 가지 더 짚어둡니다.

이 권을 쓰면서 초록만 읽고 "이 연구는 이 부분을 말하지 않는다"고 적어둔 지적이 있었습니다. 본문을 열어보니 **그 답이 절 하나로 통째로 있었습니다.**

확인하지 않고 그 지적을 논문에 썼다면, 그 연구를 읽어본 심사자가 해당 절을 가리키며 틀렸다고 했을 것입니다. 그리고 한 번 그런 지적을 받으면 나머지 related work 전체가 의심받습니다.

**인용을 확인하는 일은 남의 연구에서 흠을 찾기 위한 것이 아닙니다. 자기 논문이 틀리지 않게 하기 위한 것입니다.** 확인해보니 내 의심이 틀렸더라는 결과가 나오면, 그것도 성공한 확인입니다.

### 저자 이름은 정확히

같은 연구실에서 나온 두 논문의 저자 표기가 다른 경우가 있습니다. 한 논문에서는 이름을 줄여 쓰고 다른 논문에서는 전체를 쓰는 식입니다.

사소해 보이지만 참고문헌 목록에서는 두 사람으로 보일 수 있습니다.

### 어디서 읽었는지를 구분해서 적기

이 권의 각 절에는 **어느 판본을 언제 어디서 읽었는지**가 적혀 있습니다. 그 표기가 왜 필요한지는 이 권을 쓰면서 실제로 겪은 일들이 보여줍니다.

**논문 원문을 읽은 것과 저자들의 공개 저장소를 읽은 것을 구분했습니다.** 저장소는 신뢰할 만하지만 논문이 아닙니다. 저장소의 설명 문구를 논문의 초록인 것처럼 인용하면 안 됩니다. 확인한 심사자가 지적할 것입니다.

**같은 논문의 다른 판본도 구분했습니다.** 한 논문에서 원고 소스의 문장이 최종 판본에서 고쳐졌고, 다른 곳에서는 금액이 달라졌습니다. 원고 소스만 읽고 옮겼다면 틀린 문장과 틀린 숫자를 인용했을 것입니다.

**초록과 본문도 구분했습니다.** 초록에만 있는 최대치, 본문에만 있는 범위, 초록과 본문이 서로 다른 숫자를 적은 경우가 전부 있었습니다.

**읽지 못한 것에는 무엇을 확인해야 하는지를 함께 적었습니다.** 나중에 접근이 가능해졌을 때 무엇을 열어봐야 하는지 알 수 있게요.

**그리고 원문을 확인하니 의심이 틀렸던 경우도 있었습니다.** 한 연구의 초록을 읽고 "이 부분을 말하지 않는다"고 적어뒀는데, 본문에 절 하나가 통째로 그 답이었습니다. 확인하지 않고 썼다면 심사자가 그 절을 가리키며 틀렸다고 했을 것입니다. **인용 규율은 남의 연구를 깎기 위한 것이 아니라 자기 논문이 틀리지 않게 하기 위한 것입니다.**

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
- 심사 없이 올라간 원고는 제목, 저자, 길이, 게재 여부가 바뀝니다. 이 권을 쓰는 동안에도 시스템 이름이 바뀐 사례, 문장과 금액이 판본 사이에 달라진 사례, 게재 정보가 새로 생긴 사례를 확인했습니다. 제출 직전에 다시 확인하는 절차가 필요합니다.
- 가장 가까운 선행 연구의 후속 논문을 확인한 결과, 그 연구팀의 후속은 없었지만 다른 연구팀에서 인접 연구가 둘 나와 있었습니다. 확인하지 않았다면 심사자가 아는 논문을 저자가 모르는 상황이 됐을 것입니다.
- 논문 원문을 읽은 것, 저자들의 저장소를 읽은 것, 같은 논문의 다른 판본, 초록과 본문을 각각 구분해서 적어야 합니다. 저장소의 설명을 논문의 초록처럼 인용하면 안 되고, 초록의 최대치를 본문의 범위인 것처럼 옮겨도 안 됩니다.
- 확인은 남의 연구를 깎는 일이 아니라 자기 논문이 틀리지 않게 하는 일입니다. 초록만 읽고 적어둔 지적이 본문을 열어보니 틀렸던 경우가 이 권에 실제로 있습니다. 그것도 성공한 확인입니다.
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
| **EEVDF** | 자격을 얻은 요청 중 가상 deadline이 가장 이른 것에 다음 quantum을 주는 fair-share 방식. 지금 Linux의 기본 |
| **virtual time** | 활성 client 가중치 합의 역수를 시간에 대해 쌓은 시계. 경쟁이 심하면 느려지고 줄면 빨라진다 |
| **eligible time** | 어떤 요청이 후보가 되기 시작하는 시각. 이 시각이 현재 virtual time을 넘어서면 아직 고려하지 않는다. EEVDF의 고유 기여 |
| **lag** | 받아야 할 처리 시간과 실제로 받은 처리 시간의 차이. EEVDF가 한계를 증명하는 대상 |
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
| **ASA** | 인식한 뒤 일곱 개의 전문 정책 중 하나를 고르는 연구. 이 연구와 골격이 같고, 읽는 것이 이름이 아니라 수치라는 점이 다르다 |
| **expert policy portfolio** | 하나의 정책을 잘 만드는 대신 목적이 다른 정책을 여럿 두고 상황에 맞는 것을 고르는 구조. ASA와 이 연구의 공통 골격 |
| **SchedCP** | 언어 모델 에이전트가 scheduler를 설정하거나 생성하는 제어 계층. 가장 가까운 선행 연구 |
| **Kgent** | 자연어로 kernel 확장을 작성하게 하는 연구. 만들어낸 코드를 검증기로 확인한다 |
| **semantic gap** | kernel 정책이 응용의 필요를 이해하지 못하는 간극. 이 연구와 SchedCP가 공유하는 문제 인식 |
| **hot path** | 매 결정마다 지나가는 실행 경로. 여기에 느린 것을 두면 시스템이 멈춘다 |
| **control plane** | 결정 경로 바깥에서 느리게 도는 층. 언어 모델이 놓이는 자리 |

## 배포된 이름 표

| 용어 | 뜻 |
|---|---|
| **Game Mode** | 게임에 독점 CPU 집합과 GPU 우선순위를 주는 Windows 기능. 판별 방법은 제조사 문서에 기술되어 있지 않다 |
| **exclusive CPU set** | 특정 core를 한 응용에만 배정하는 것. 포기하면 다른 프로세스와 같은 core를 나눠 쓰게 된다 |
| **ananicy** | 프로세스 이름으로 표를 뒤져 우선순위를 조정하는 Linux 데몬 |
| **rules catalog** | 그 데몬이 참조하는 이름과 분류의 목록. 커뮤니티가 손으로 관리한다 |

## 평가 도구

| 용어 | 뜻 |
|---|---|
| **hackbench** | 서로 통신하는 task를 400개 만들어 전체 완료 시간을 재는 도구 |
| **schbench** | 깨움 지연, 요청 지연, 초당 처리량을 백분위수로 보고하는 도구 |
| **interbench** | 대화형 작업을 흉내 내고 지연과 흔들림과 마감 달성률을 재는 도구 |
| **rt-app** | 작업 모델을 JSON으로 기술해 주기적 부하를 만드는 도구 |
| **PCMark 10 · SYSmark 30 · Procyon** | 실제 응용을 돌려 기계를 비교하는 상용 데스크톱 벤치마크. 시나리오 분류와 프로그램 목록을 문서에 공개한다 |

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

**확인 규율 확인**

- 어떤 인용문에 대해 그것을 어느 판본의 어디에서 읽었는지 말할 수 있다.
- 초록의 숫자와 본문의 숫자가 왜 다를 수 있는지, 어느 쪽을 옮겨야 하는지 말할 수 있다.
- 찾아봤는데 없더라는 결과를 어떻게 적어야 검증 가능한 주장이 되는지 말할 수 있다.

다음 권에서는 이 연구 자체를 봅니다. 무엇을 주장하고, 그 주장이 어떤 고리들로 되어 있고, 각 고리가 어떻게 무너질 수 있는지입니다.
