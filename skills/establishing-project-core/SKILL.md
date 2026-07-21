---
name: establishing-project-core
description: Use in PLAN work when a new or changing project needs its identity-defining player promise, core actions, core loop, system anchors, invariants, changeable shell, and required technical foundations proposed, stress-tested, explicitly approved, and recorded as the project core contract.
---

# Establishing Project Core

## Purpose and authority

프로젝트 코어 확정은 앞으로 보호할 **최소 정체성 계약**을 정하는 일이다. AI는 후보를 제안하고 반례를 검사할 수 있지만, 사용자 승인 없이 `CORE_CONFIRMED`로 표시하지 않는다.

기존 프로젝트의 사실 판정은 `identifying-project-core`, 컨셉·PoC 탐색은 `analyzing-and-refining-game-concepts`, 승인 계약의 문서화는 `managing-design-documents`가 책임진다.

## Skill Modes and state

`propose → stress-test → confirm → lock`, 새 근거가 생기면 `reopen`한다.

`CORE_SEED → CORE_PROPOSED → CORE_STRESS_TESTED → CORE_CONFIRMED | CORE_REVISE | CORE_REJECTED → CORE_RECORDED`

`confirm`과 `lock`은 명시적 사용자 승인 없이는 실행하지 않는다.

## Required inputs

```yaml
goal_problem_and_target_player:
candidate_concept_and_player_promise:
core_actions_choices_feedback:
candidate_core_loop_and_systems:
world_visual_tone_invariants:
technical_foundations:
constraints_and_capacity:
mvp_poc_playtest_evidence:
alternatives_and_rejected_directions:
approval_authority:
```

## Protection boundary

- `INVARIANT`: 바뀌면 프로젝트 정체성이 달라진다.
- `CHANGEABLE`: 코어를 유지한 채 교체·조정할 수 있다.
- `REQUIRES_REAPPROVAL`: 영향 분석과 사용자 재승인이 필요하다.
- `OUT_OF_SCOPE`: 현재 코어 계약에 포함하지 않는다.

세부 계약 필드·반례·상태 전이·재개 조건은 `references/core-contract-and-state.md`를 필요할 때만 읽는다.

## Workflow

1. 정체성 한 문장, 핵심 행동·선택·피드백, 코어 루프와 중심 시스템을 제안한다.
2. 제거·대체·실패·확장 반례로 최소성과 일관성을 공격한다.
3. 코어 기능과 `MVP_SUPPORT`, 기술 코어와 대체 가능한 구현을 분리한다.
4. 사용자 승인·수정·기각을 기록한다.
5. 승인된 항목만 책임 원본·개발 게이트·검수 기준에 연결한다.

## Output contract

```md
## 상태와 사용자 승인 기록
## 프로젝트 정체성·대상 플레이어·핵심 약속
## 핵심 행동·선택·피드백과 코어 루프
## 중심 시스템·기술 기반
## INVARIANT·CHANGEABLE·REQUIRES_REAPPROVAL·OUT_OF_SCOPE
## 코어 기능과 MVP 지원 기능
## PoC·플레이테스트 근거와 실패 조건
## 제외 후보·미검증·재개 조건
## 책임 원본·게이트·검수 연결
```

## Quality gate

코어를 기능 목록으로 팽창시키지 않고, 불변 조건과 변경 가능한 외피를 구분하며, 반례와 근거를 기록하고, **사용자 승인 없이** `CORE_CONFIRMED` 또는 `CORE_RECORDED`로 전환하지 않는다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
