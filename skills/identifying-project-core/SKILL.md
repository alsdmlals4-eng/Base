---
name: identifying-project-core
description: Use when an existing game or software project needs an evidence-based determination of which experiences, loops, systems, rules, directions, or technical foundations are identity-defining project core rather than replaceable content, MVP support, or implementation detail.
---

# Identifying Project Core

## Core principle

프로젝트 코어는 프로젝트의 핵심 목적·경험·시스템·기술 기반 중에서 다른 요소들이 의존하는 중심부다. 제거하거나 본질적으로 변경했을 때 같은 프로젝트라고 보기 어려운 요소만 코어로 판정한다.

중요해 보이거나 개발 비용이 컸거나 현재 구현되어 있다는 이유만으로 코어가 되지는 않는다. 현행 책임 원본, 사용자 승인 결정, 실제 코드·데이터·자산·테스트와 의존 관계를 근거로 판정한다.

## Responsibility boundary

| 작업 | 책임 |
|---|---|
| 기존 프로젝트의 코어 후보 식별·분류 | 이 Skill |
| 새 프로젝트의 코어 제안·승인·확정 | `establishing-project-core` |
| 핵심 컨셉·뾰족한 재미·PoC 탐색 | `analyzing-and-refining-game-concepts` |
| 승인된 코어의 기획서 기록·발행 | `managing-design-documents` |
| 실제 변경의 정적·런타임·회귀 검증 | `reviewing-and-validating-project-changes` |
| 적대적 공격·비평 검증·개선 반복 | `running-adversarial-review-and-refinement` |

## Work Mode and Skill Modes

기본 Work Mode는 `PLAN` 또는 `REVIEW`이며 읽기 전용이다. 사용자 승인 없이 코어를 새로 확정하거나 책임 원본을 수정하지 않는다.

- `inventory`: 현행 기획·결정·구현·의존 관계를 수집한다.
- `extract-candidates`: 코어 후보와 근거를 추출한다.
- `dependency-map`: 다른 요소가 무엇에 의존하는지 연결한다.
- `removal-and-change-test`: 제거·대체·축소 시 정체성과 핵심 경험의 변화를 검사한다.
- `classify`: 후보를 코어·지원·MVP·콘텐츠·외피·미확정으로 분류한다.
- `core-report`: 근거·충돌·미검증과 함께 판정 결과를 보고한다.

## Required inputs

```yaml
project_identity_and_goal:
current_design_sources:
approved_user_decisions:
actual_code_data_assets_tests:
core_loop_and_major_systems:
player_actions_choices_and_feedback:
world_visual_and_tone_direction:
technical_dependencies:
mvp_scope:
known_conflicts_and_unknowns:
```

입력이 없으면 추정으로 확정하지 않고 `UNVERIFIED` 또는 `PARTIAL`로 표시한다.

## Core layers

### 기획 코어

플레이어에게 제공해야 하는 핵심 경험과 프로젝트의 기본 방향이다.

- 반복되는 핵심 행동과 판단
- 핵심 재미와 플레이어 약속
- 중요한 위험·보상·감정
- 세계관·시각·톤의 불변 방향
- 프로젝트가 하지 않아야 할 금지 방향

### 시스템 코어

다른 콘텐츠와 기능이 연결되는 중심 시스템과 순환 구조다.

```text
입력·자원 획득
→ 핵심 행동
→ 상태·가치 변화
→ 활용·보상
→ 다음 핵심 행동
```

게임에서는 이 반복 순환을 코어 루프로 본다. 단순한 화면 순서나 콘텐츠 목록은 코어 루프가 아니다.

### 코드 코어

여러 기능의 기반이 되는 핵심 코드·데이터 영역이다.

- 게임·세션 상태 관리
- 저장·불러오기와 호환성
- 아이템·엔티티 생성
- 전투·경제·규칙 판정
- 이벤트·메시지 처리
- 공통 데이터·ID·Schema

코드 코어는 기술 의존성의 중심일 수 있지만 그 자체가 반드시 제품 정체성은 아니다. 기획·시스템 코어와 기술 코어를 분리해 기록한다.

## Core versus MVP

- `CORE`: 프로젝트 정체성과 핵심 경험에 반드시 필요하다.
- `MVP_SUPPORT`: 정체성 자체는 아니지만 핵심 가설을 실행·관찰하는 최소 제품에 필요하다.
- `BOTH`: 코어이면서 MVP에서도 반드시 구현해야 한다.
- `LATER`: 코어가 아니며 현재 MVP 검증에도 필요하지 않다.

강화 게임의 무기 강화는 `CORE`이자 `BOTH`일 수 있다. 저장 기능은 정체성의 코어가 아니어도 장기 진행 검증을 위한 `MVP_SUPPORT`일 수 있다.

## Identification process

### 1. Evidence inventory

```text
최신 사용자 승인
→ 등록된 기획 책임 원본
→ 결정 기록·현재 상태
→ 실제 코드·데이터·자산·테스트
→ 과거 문서·외부 설명
```

현재 구현만 있고 승인 근거가 없거나 문서만 있고 구현·검증이 없으면 상태를 분리한다.

### 2. Candidate extraction

```yaml
candidate:
layer: design/system/code
claimed_role:
evidence:
dependents:
current_status:
```

### 3. Dependency mapping

- 어떤 시스템·콘텐츠·UI·데이터가 후보에 의존하는가?
- 후보가 다른 코어를 지탱하는가, 단지 편의를 제공하는가?
- 대체 구현으로 같은 경험을 유지할 수 있는가?
- 코드 의존성과 제품 정체성 의존성이 같은가?

### 4. Removal and change test

1. 제거하면 핵심 행동이 성립하는가?
2. 다른 방식으로 대체해도 같은 플레이 경험인가?
3. 축소하면 뾰족한 재미와 플레이 동기가 유지되는가?
4. 변경하면 장르·판타지·사용자 약속이 달라지는가?
5. 다른 주요 시스템이 끊기거나 의미를 잃는가?
6. UI·대사·스킨·콘텐츠 수량처럼 교체 가능한 외피인가?
7. 구현 방식만 바뀌고 제품 의미는 유지되는가?

### 5. Classification

| 판정 | 의미 |
|---|---|
| `PROJECT_CORE` | 제거·본질 변경 시 같은 프로젝트로 보기 어렵다. |
| `CORE_SUPPORT` | 코어를 이해·운영·확장하도록 돕지만 대체 가능하다. |
| `MVP_SUPPORT` | 최소 검증 제품에는 필요하지만 정체성 코어는 아니다. |
| `CONTENT_VARIANT` | 코어 규칙을 표현하는 교체 가능한 콘텐츠다. |
| `PRESENTATION_SHELL` | UI 배치·대사·스킨·연출처럼 교체 가능한 외피다. |
| `TECHNICAL_FOUNDATION` | 여러 기능이 의존하는 기술 기반이며 제품 코어와 별도 관리한다. |
| `CONFLICTED` | 문서·승인·구현이 서로 다르다. |
| `UNVERIFIED` | 근거가 부족하다. |

모든 중요한 요소를 `PROJECT_CORE`로 판정하지 않는다. 코어가 많아질수록 변경 비용과 정체성 설명이 불명확해진다.

## Decision status

- `IDENTIFIED`: 근거와 경계가 명확하다.
- `PARTIAL`: 일부 층만 확인됐다.
- `CONFLICTED`: 승인 원본과 실제 구현 또는 문서끼리 충돌한다.
- `UNVERIFIED`: 필요한 근거가 없다.

## Output contract

```md
# 프로젝트 코어 판정
## 판정 상태
## 프로젝트 정체성 한 문장
## 기획 코어
## 시스템 코어와 코어 루프
## 코드·데이터 기술 코어
## 코어가 아닌 변경 가능 요소
## 코어 기능과 MVP 지원 기능 구분
## 후보별 제거·대체·변경 테스트
## 의존 관계
## 근거 경로와 승인 상태
## 충돌·미검증·확인 필요
## 코어 변경 시 예상 영향
## 다음 단계
```

## Definition of Done

- 기획·시스템·코드 코어를 분리했다.
- 각 후보에 근거와 제거·대체 테스트가 있다.
- 코어·지원·MVP·콘텐츠·외피·미확정을 구분했다.
- 코어가 아닌 요소도 명시해 과도한 보호 범위를 막았다.
- 문서·승인·구현 충돌과 미검증을 숨기지 않았다.
- 사용자 확정이 필요한 항목을 `establishing-project-core`의 입력으로 넘겼다.

## Failure conditions

- 중요하거나 제작 비용이 크다는 이유만으로 코어로 판정한다.
- 현재 구현을 사용자 승인 또는 제품 정체성과 동일시한다.
- 장르명·기능 목록·홍보 문구만으로 코어를 설명한다.
- UI·스킨·대사·콘텐츠 수량을 불변 코어로 고정한다.
- 기술 기반과 플레이어 경험의 코어를 혼동한다.
- 모든 후보를 코어로 분류해 우선순위를 없앤다.
- 코어 기능과 MVP 지원 기능을 혼동한다.
- 근거가 없는데 `IDENTIFIED` 또는 확정으로 보고한다.
- 읽기 전용 판정 중 책임 원본을 임의 수정한다.

## Learning

- Learning Log: `skills/SKILL_LEARNING_LOG.md`
- 현재 지식 상태: `OBSERVATION`
- 검토 트리거: 코어 과대 판정, 코어와 MVP 혼동, 문서·구현 충돌, 변경 영향 누락
