---
name: identifying-project-core
description: Use when an existing project needs an evidence-based, read-only determination of which experiences, loops, systems, rules, directions, or technical foundations are identity-defining project core rather than replaceable content, MVP support, or implementation detail.
---

# Identifying Project Core

## Purpose and boundary

프로젝트 코어는 제거하거나 본질적으로 바꾸면 같은 프로젝트라고 보기 어려운 최소 정체성·경험·시스템 중심부다. 현재 구현, 높은 제작비, 중요해 보인다는 인상만으로 코어를 확정하지 않는다.

기본 Work Mode는 `PLAN` 또는 `REVIEW`이며 **읽기 전용**이다. 새 코어의 제안·사용자 승인은 `establishing-project-core`, 실제 변경 검증은 `reviewing-and-validating-project-changes`가 책임진다.

## Skill Modes

`inventory → extract-candidates → dependency-map → removal-and-change-test → classify → core-report`

## Required inputs

```yaml
project_identity_and_goal:
approved_design_and_decisions:
actual_code_data_assets_tests:
player_actions_choices_feedback:
core_loop_and_major_systems:
technical_dependencies:
mvp_scope:
conflicts_and_unknowns:
```

근거가 없으면 `UNVERIFIED`, 일부만 확인되면 `PARTIAL`, 문서·승인·구현이 충돌하면 `CONFLICTED`다.

## Classification

- `PROJECT_CORE`: 제거·본질 변경 시 프로젝트 정체성이 달라진다.
- `CORE_SUPPORT`: 코어를 운영·이해·확장하지만 대체 가능하다.
- `MVP_SUPPORT`: 핵심 가설 검증에는 필요하지만 정체성 코어는 아니다.
- `CONTENT_VARIANT`: 코어 규칙을 표현하는 교체 가능한 콘텐츠다.
- `PRESENTATION_SHELL`: UI·대사·스킨·연출 등 교체 가능한 외피다.
- `TECHNICAL_FOUNDATION`: 여러 기능이 의존하는 기술 기반이며 제품 코어와 분리한다.
- `CONFLICTED` / `UNVERIFIED`: 충돌 또는 근거 부족이다.

세부 층·증거 우선순위·제거·대체·변경 질문은 `references/classification-and-tests.md`를 필요할 때만 읽는다.

## Output contract

```md
## 판정 상태
## 프로젝트 정체성 한 문장
## 기획·시스템·기술 코어
## 코어가 아닌 변경 가능 요소
## 코어 기능과 MVP 지원 기능
## 후보별 제거·대체·변경 테스트
## 의존 관계와 근거
## 충돌·미검증·변경 영향
## 다음 단계
```

## Quality gate

- 기획·시스템·기술 코어를 구분한다.
- 모든 후보에 실제 근거와 `removal-and-change-test`가 있다.
- 코어가 아닌 요소도 명시해 보호 범위 팽창을 막는다.
- 사용자 승인 없이 책임 원본을 수정하거나 확정하지 않는다.
- 결과는 `IDENTIFIED / PARTIAL / CONFLICTED / UNVERIFIED` 중 하나다.

## Failure conditions

기능 목록 전체를 코어로 만들거나, 기술 의존성을 제품 정체성과 혼동하거나, UI·분량·임시 구현을 불변 코어로 고정하거나, 코어와 `MVP_SUPPORT`를 혼동하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
