---
name: running-adversarial-review-and-refinement
description: Use when a design, plan, document, code proposal, data change, UX flow, or other work product should be attacked as if it failed, its criticisms independently validated, only justified findings refined, and the revised result regression-checked without changing project core or adding unnecessary scope.
---

# Running Adversarial Review and Refinement

## Purpose and separation

적대적 검토는 승인 거부 증거를 찾는 공격 단계다. 그러나 **비판도 오류·취향·과잉 요구**일 수 있으므로 공격과 검증을 분리하고, 검증된 문제만 최소 수정한다.

실제 diff·정적·런타임·접근성·성능 증거는 `reviewing-and-validating-project-changes`, 프로젝트 코어 판정·확정은 관련 코어 Skill이 책임진다.

## Workflow

`attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`

기본 Work Mode는 `REVIEW → 필요한 경우 BUILD → REVIEW`다. 같은 수행자가 맡아도 단계별 입력과 출력을 섞지 않는다.

## Required inputs

```yaml
work_product:
approved_requirements_and_scope:
project_core:
canonical_sources_and_actual_diff:
acceptance_criteria:
protected_strengths_and_assets:
constraints_and_validation_environment:
change_authority:
```

코어가 확정되지 않았다면 핵심 충돌은 `UNVERIFIED`로 둔다.

## Finding decisions

- `MUST_FIX`: 완료·안전·정합성을 막는 검증된 결함.
- `SHOULD_FIX`: 범위 안에서 가치가 크고 회귀 위험이 통제된다.
- `DEFER`: 유효하지만 현재 범위·근거·비용상 보류한다.
- `REJECT`: 취향, 중복, 잘못된 전제, 범위 밖 요구다.
- `UNVERIFIED`: 증거가 부족하다.

상세 공격 렌즈·판정표·회귀 프로토콜은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.

## Rules

1. `attack`은 실패·모순·악용·누락·경계 조건을 최대한 찾는다.
2. `validate-critique`는 사실성, 발생 가능성, 영향, 범위, 수정 비용을 재판정한다.
3. `refine-approved-findings`는 `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
4. `regression-recheck`는 기존 장점·정상 경로·코어·범위와 새 결함을 다시 공격한다.
5. `decision-report`는 반영·보류·기각·미검증과 남은 위험을 모두 기록한다.

## Output contract

```md
## 공격 관점과 실패 가정
## finding·근거·심각도
## MUST_FIX / SHOULD_FIX / DEFER / REJECT / UNVERIFIED
## 실제 반영한 최소 변경
## 보호한 코어·장점·범위
## regression-recheck 결과
## 남은 위험·미검증·다음 조건
```

## Quality gate

`MUST_FIX`·`SHOULD_FIX` 외 항목을 몰래 반영하지 않고, 프로젝트 코어를 바꾸거나 기능을 팽창시키지 않으며, 수정 뒤 `regression-recheck`를 수행한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
