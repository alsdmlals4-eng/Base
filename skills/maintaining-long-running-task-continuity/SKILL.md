---
name: maintaining-long-running-task-continuity
description: Use when a large multi-step task may exceed one response, tool session, context window, or execution attempt and must remain resumable through evidence-backed checkpoints, partial deliverables, explicit next actions, and truthful completion states.
---

# Maintaining Long-Running Task Continuity

## Core principle

중단을 숨기거나 비동기 완료를 약속하지 않는다. 큰 작업을 검증 가능한 결과 단위로 나누고, 각 단위가 끝날 때 재개 가능한 checkpoint와 실제 산출물을 남긴다.

이 Skill은 현재 실행 중인 큰 작업의 연속성을 관리한다. 프로젝트의 장기 책임 원본·Active Context·인수인계는 `maintaining-project-context-and-handoff`, 로컬·원격 저장 상태는 `synchronizing-local-and-github-state`가 책임진다.

## Modes

`initialize` → `checkpoint` → `resume` → `partial-delivery` → `close`

## Checkpoint contract

```yaml
objective_and_scope:
completed_outcomes:
changed_or_created_artifacts:
validation_and_evidence:
current_state_and_blockers:
protected_decisions:
next_exact_action:
remaining_acceptance_criteria:
```

## Workflow

1. 작업을 독립 검증 가능한 결과와 선행 조건으로 나눈다.
2. 가장 위험하거나 가치 있는 결과부터 실제로 완성한다.
3. 2~3개 도구 묶음 또는 의미 있는 단계마다 상태·증거·다음 행동을 갱신한다.
4. 실행이 막히면 완료한 결과를 먼저 전달하고 미완료·원인·재개 지점을 분리한다.
5. 재개 시 과거 대화 전체가 아니라 최신 checkpoint와 책임 원본을 읽는다.

## Output contract

```md
## 목표·범위·현재 상태
## 완료한 실제 결과와 산출물
## 실행한 검증과 증거
## 보호한 결정·변경 금지 범위
## 미완료·차단 원인·남은 완료 기준
## 다음 정확한 행동과 재개 입력
```

## Quality gate

진행 중을 완료로 표시하지 않고, 같은 질문을 반복하지 않으며, 시간 예측·백그라운드 작업을 약속하지 않고, checkpoint 없이 긴 조사만 계속하지 않는다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
