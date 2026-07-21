---
name: analyzing-and-refining-game-concepts
description: Use when defining or reworking a game's core concept, pointed fun, constraints, design coherence, PoC hypothesis, or production direction through structured analysis such as SWOT, MDA/DDE, loop, audience, differentiation, and feasibility review.
---

# Analyzing and Refining Game Concepts

## Core principle

기획 요소를 많이 만드는 것이 목적이 아니다. 플레이어가 계속 플레이하게 만드는 원동력인 **뾰족한 재미**를 찾고, 모든 게임 요소를 핵심 컨셉에 정렬한 뒤, 가장 위험한 가설을 PoC로 빠르게 검증해 다음 방향을 결정한다.

## Distinguish

| 작업 | 이 Skill | 다른 Skill |
|---|---|---|
| 핵심 컨셉·뾰족한 재미·방향성 진단 | 책임짐 | - |
| GDD·레벨·캐릭터·세계관 문서 작성 | 구조와 개선 방향만 제안 | `managing-design-documents` |
| 최소 가설 PoC 계약 | 책임짐 | 실제 구현은 프로젝트 작업 계약 |
| 대표 품질·제작 파이프라인 증명 | 선행 방향만 제공 | `designing-vertical-slices` |
| 구현 결과의 코드·데이터 회귀 검증 | 판단 기준만 제공 | `reviewing-and-validating-project-changes` |

## Modes

- `frame`: 한 문장 핵심 컨셉과 플레이어 약속을 정한다.
- `constrain`: 플랫폼·인력·시간·기술·콘텐츠·시장 제약을 확인한다.
- `sharpen`: 반복 플레이의 원동력인 뾰족한 재미와 핵심 선택을 찾는다.
- `structure`: 모든 기획 요소를 핵심 컨셉에 맞춰 구체화·정돈한다.
- `analyze`: SWOT, MDA/DDE, 3C, 루프, 동기, 차별화, 제작성을 교차 분석한다.
- `poc-contract`: 가장 위험한 기획 가설과 최소 검증물을 정의한다.
- `recalibrate`: PoC 결과에 따라 유지·수정·삭제·보류를 결정한다.
- `production-gate`: 다음 Prototype·Vertical Slice·Production 진입 여부를 판정한다.

## State model

```text
1. CONCEPT_SEED
→ 2. CONSTRAINTS_CHECKED
→ 3. POINTED_FUN_HYPOTHESIS
→ 4. CONCEPT_STRUCTURED
→ 5. POC_BUILD_AND_TEST
→ 6. CONCEPT_RECALIBRATION
→ 7. PRODUCTION_READY | REPEAT_POC | HOLD | STOP
```

사용자가 말한 `BIG BLIND`는 이 Skill에서 4단계 `CONCEPT_STRUCTURED`의 프로젝트 용어로 취급한다. 의미는 **레벨 디자인, 등장인물, 캐릭터 스타일, 스테이지, 세계관 등 모든 요소를 핵심 컨셉과 뾰족한 재미에 맞춰 정돈하는 단계**다. 외부 표준 용어로 가정하지 않는다.

## Required inputs

```yaml
current_idea_or_gdd:
target_player_and_play_context:
reference_games_and_non_game_references:
known_constraints:
core_loop_and_meta_loop:
current_game_elements:
current_risks_and_unknowns:
existing_prototype_or_poc_results:
team_and_production_capacity:
framework_profile:
```

`framework_profile`에서 약어의 의미를 명시한다. `DDD`는 게임 기획에서 단일 표준 의미가 아니므로 프로젝트가 `Data-Driven Design`, `Domain-Driven Design`, 사용자 정의 분석축 등 어떤 의미로 쓰는지 확인하기 전에는 임의 해석하지 않는다. 게임 경험 분석이 목적이면 `MDA` 또는 `DDE(Design–Dynamics–Experience)`를 우선 후보로 제시할 수 있다.

## Phase 1 — Core concept

다음 문장으로 시작한다.

```text
[대상 플레이어]는 [핵심 행동과 선택]을 반복하며
[고유한 감정·판타지·성취]를 경험한다.
이 게임은 [비교 대상]과 달리 [차별화된 원리] 때문에 계속 플레이된다.
```

핵심 컨셉은 다음을 포함한다.

- 플레이어 역할과 판타지.
- 반복하는 핵심 행동.
- 가장 중요한 선택과 긴장.
- 즉시 느끼는 피드백과 보상.
- 다음 플레이를 부르는 미완료 욕구.
- 다른 요소를 추가·삭제할 때 사용할 방향 판단 기준.

## Phase 2 — Constraint check

| 제약 | 확인 내용 |
|---|---|
| 플레이 환경 | 세션 길이, 입력 방식, 온라인·오프라인, 접근성 |
| 제작 | 인력, 기술, 일정, 자산 생산 속도, 반복 비용 |
| 콘텐츠 | 필요한 변형 수, 재사용성, 소모 속도 |
| 시스템 | 저장, 경제, 난이도, AI, 멀티플레이 의존성 |
| 표현 | 아트 스타일, 연출, 가독성, 플랫폼 성능 |
| 사업·시장 | 대상층, 가격·운영 방식, 경쟁작, 포지셔닝 |

제약은 아이디어를 약화시키는 목록이 아니라 **뾰족한 재미를 더 선명하게 만드는 설계 경계**로 사용한다.

## Phase 3 — Pointed fun

뾰족한 재미 후보마다 다음을 확인한다.

1. 플레이어가 직접 하는 행동인가?
2. 반복할수록 판단·숙련·표현이 깊어지는가?
3. 성공과 실패의 피드백이 명확한가?
4. 한 문장과 짧은 플레이로 설명 가능한가?
5. 다른 게임 요소가 이 재미를 강화하는가?
6. 콘텐츠를 늘리지 않아도 변주가 생기는가?
7. 다음 판·다음 단계·다음 빌드를 시도할 이유가 생기는가?

후보를 `핵심`, `보조`, `장식`, `충돌`, `미검증`으로 분류한다.

## Phase 4 — Concept structuring / BIG BLIND

다음 요소를 핵심 컨셉과 뾰족한 재미에 대조한다.

- My Game GDD와 핵심 규칙.
- 레벨 디자인과 공간·난이도 흐름.
- 등장인물의 역할과 플레이 기능.
- 캐릭터 스타일과 조작·전투 정체성.
- 스테이지 구조와 반복 변주.
- 세계관과 시스템 규칙의 연결.
- UI·아트·사운드가 강조해야 하는 판단과 감정.
- 성장·수집·경제·보상이 다음 플레이를 만드는 방식.

각 요소는 다음 중 하나로 판정한다.

```text
AMPLIFY  핵심 재미를 직접 강화
SUPPORT  이해·리듬·동기를 보조
NEUTRAL  존재하지만 핵심에 기여하지 않음
CONFLICT 핵심 컨셉과 충돌
UNPROVEN PoC가 필요한 가설
```

`NEUTRAL`과 `CONFLICT`는 관성적으로 유지하지 않고 삭제·축소·재설계 후보로 만든다.

## Phase 5 — Analysis lenses

### SWOT to action

단순 목록으로 끝내지 않고 전략으로 변환한다.

- `SO`: 강점으로 기회를 확대한다.
- `WO`: 기회를 잡기 위해 약점을 보완한다.
- `ST`: 강점으로 위협을 방어한다.
- `WT`: 약점과 위협이 겹치는 범위를 제거·회피한다.

내부 요인과 외부 요인을 섞지 않으며, 각 항목에 근거와 대응 행동을 연결한다.

### MDA or DDE

- Mechanics / Design: 플레이어가 실제로 다루는 규칙·입력·자원·상태.
- Dynamics: 반복 플레이에서 규칙들이 만들어내는 전략·긴장·변주.
- Aesthetics / Experience: 플레이어가 실제로 느껴야 하는 감정·판타지·성취.

설계자가 의도한 경험에서 역으로 Dynamics와 규칙을 대조한다.

### Additional lenses

- 3C: Character, Camera, Control.
- Core loop / session loop / meta loop.
- 선택의 의미, 숙련 깊이, 실패 학습, 피드백 지연.
- 플레이 동기: 숙련, 발견, 수집, 표현, 관계, 서사, 경쟁, 창조.
- 차별화: 보이는 차이와 실제 플레이 원리의 차이.
- 제작성: 콘텐츠 한 단위의 비용, 재사용률, 자동화 가능성.
- 확장성: 새 요소가 핵심 재미를 강화하는가, 복잡성만 늘리는가.

## Phase 6 — PoC contract

PoC는 게임 전체를 만드는 단계가 아니다. 가장 위험한 기획 가설을 최소 비용으로 틀릴 수 있게 만드는 단계다.

```yaml
hypothesis:
player_action:
expected_experience:
minimum_rules_and_content:
excluded_scope:
observation_method:
success_signal:
failure_signal:
stop_condition:
next_decision_if_passed:
next_decision_if_failed:
```

가능하면 행동·선택·반복·감정의 관찰 증거를 사용한다. “재미있다” 한 문장만으로 통과시키지 않는다.

## Phase 7 — Recalibration and production gate

PoC 결과를 다음으로 분류한다.

- `KEEP`: 가설과 요소를 유지한다.
- `AMPLIFY`: 핵심으로 승격하고 다른 요소를 정렬한다.
- `CHANGE`: 원인 가설과 수정안을 명시한다.
- `REMOVE`: 핵심에 기여하지 않거나 비용 대비 가치가 낮다.
- `DEFER`: 현재 PoC로 판단할 수 없다.
- `RETEST`: 다른 조건에서 다시 검증한다.

Production 진입 조건:

- 핵심 컨셉과 뾰족한 재미를 한 문장으로 설명할 수 있다.
- 핵심 행동과 반복 동기가 PoC에서 관찰됐다.
- 주요 기획 요소가 핵심 컨셉에 정렬됐다.
- 가장 큰 제약과 위험의 대응 방향이 있다.
- 다음 제작 범위와 제외 범위가 명확하다.
- 실패 시 되돌아갈 재조정 지점이 있다.

목표 품질과 제작 파이프라인까지 증명해야 하면 `designing-vertical-slices`로 넘긴다.

## Output contract

```md
# 게임 핵심 컨셉·방향성 분석

## 한 문장 핵심 컨셉
## 대상 플레이어와 플레이 약속
## 제약 조건
## 뾰족한 재미 후보와 최종 가설
## 핵심·보조·장식·충돌 요소
## GDD·레벨·캐릭터·스테이지·세계관 정렬
## SWOT와 SO·WO·ST·WT 전략
## MDA/DDE·3C·루프·동기 분석
## 차별화·제작성·확장성
## PoC 계약
## PoC 결과와 유지·수정·삭제·보류
## 개선 우선순위
## Production·Vertical Slice 진입 판정
## 미검증·위험·다음 질문
```

## Definition of Done

- 핵심 컨셉과 뾰족한 재미가 분리되지 않고 연결됐다.
- 제약을 반영한 선택과 제외 범위가 있다.
- 게임 요소별 핵심 기여도를 판정했다.
- 분석 프레임워크 결과를 실제 개선 행동으로 변환했다.
- 가장 위험한 가설을 검증하는 PoC 계약이 있다.
- PoC 결과에 따른 재조정과 다음 게이트가 정의됐다.
- `DDD` 등 모호한 약어를 임의로 해석하지 않았다.

## Failure conditions

- 장르·기능 목록을 핵심 컨셉으로 대체한다.
- 뾰족한 재미가 플레이어 행동이 아니라 홍보 문구뿐이다.
- 모든 요소를 핵심이라 부르며 우선순위를 만들지 않는다.
- SWOT을 일반적인 장단점 목록으로 끝낸다.
- PoC가 전체 게임·Vertical Slice 규모로 팽창한다.
- PoC 결과와 무관하게 기존 기획을 유지한다.
- 시장 유행만으로 핵심 경험을 바꾼다.
- 정의되지 않은 DDD 약어를 임의의 분석 틀로 확정한다.

Template: `templates/planning/GAME_CONCEPT_DIRECTION_REVIEW.md`
