---
name: running-adversarial-review-and-refinement
description: Use when a design, plan, document, code proposal, data change, UX flow, or other work product should be attacked as if it failed, its criticisms independently validated, technically decidable findings organized into a review proposal, only genuine design conflicts escalated to the user one at a time, and the revised result regression-checked without changing project core or adding unnecessary scope.
---

# Running Adversarial Review and Refinement

## Purpose and separation

적대적 검토는 승인 거부 증거를 찾는 공격 단계다. 그러나 **비판도 오류·취향·과잉 요구**일 수 있으므로 공격과 검증을 분리하고, 검증된 문제만 최소 수정한다.

`REVIEW` Work Mode에서는 이 Skill을 단일 변경점 확인이 아니라 **전체 영향 범위에서 수정·개선 후보를 찾는 기본 탐색 루프**로 사용한다. 실제 diff·정적·런타임·접근성·성능 증거는 `reviewing-and-validating-project-changes`, 프로젝트 코어 판정·확정은 관련 코어 Skill이 책임진다.

## Default REVIEW route

```text
review-scope-map
→ attack
→ validate-critique
→ route-findings
→ technical-review-proposal
→ USER_DECISION_REQUIRED가 있으면 한 번에 하나씩 확정
→ 승인된 MUST_FIX·SHOULD_FIX만 refine-approved-findings
→ regression-recheck
→ decision-report
```

- `review-scope-map`은 요청된 파일만 보지 않고 변경 파일, 같은 책임의 정본, 활성 소비자, 인접 시스템, 변경됐어야 하지만 untouched인 파일, 테스트·템플릿·파생본을 연결한다.
- 전체 저장소를 무조건 정독하지 않는다. Registry·Documentation Map·참조 관계·실제 diff로 영향 범위를 확장하되, 발견된 연결 누락 때문에 범위가 바뀌면 지도를 갱신한다.
- 사용자가 검수만 요청한 경우 기본 권한은 읽기 전용이다. 기술적으로 자동 판단 가능해도 파일을 즉시 수정하지 않고 먼저 검수안으로 정리한다.
- 사용자가 수정까지 요청했거나 승인된 변경 계약이 있으면 기술 검수안의 범위 내 항목만 `BUILD`로 전환해 반영하고 다시 `REVIEW`로 돌아온다.

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

코어가 확정되지 않았다면 핵심 충돌은 `UNVERIFIED` 또는 `USER_DECISION_REQUIRED`로 둔다.

## Finding decisions

- `MUST_FIX`: 완료·안전·정합성을 막는 검증된 결함.
- `SHOULD_FIX`: 범위 안에서 가치가 크고 회귀 위험이 통제된다.
- `DEFER`: 유효하지만 현재 범위·근거·비용상 보류한다.
- `REJECT`: 취향, 중복, 잘못된 전제, 범위 밖 요구다.
- `UNVERIFIED`: 증거가 부족하다.

## Finding routing

검증된 finding은 수정 여부와 별도로 다음 경로로 분류한다.

- `TECHNICAL_REVIEW_PROPOSAL`: 정본·계약·테스트·표준·관찰 증거로 정답 또는 최소 안전안이 결정된다. 사용자가 검수만 요청한 경우 한 묶음의 검수안으로 정리한다.
- `USER_DECISION_REQUIRED`: 둘 이상의 유효한 선택지가 프로젝트 코어, 플레이어 경험, 주요 UX, 콘텐츠 의미, 범위, 비용 우선순위 또는 승인된 방향을 다르게 만든다.
- `BLOCKED_UNVERIFIED`: 필요한 정본·환경·실행 증거가 없어 판단할 수 없다. 필요한 입력과 재검증 조건을 적는다.
- `NO_CHANGE`: 지적이 기각됐거나 기존 장점·보호 대상을 유지하는 편이 낫다.

기술 항목을 사용자 질문으로 전가하지 않는다. 저장소·테스트·표준에서 답할 수 있는 사실은 AI가 판단해 검수안에 포함한다.

`USER_DECISION_REQUIRED`는 한 번에 하나만 제시한다. 각 질문은 다음을 포함한다.

```yaml
conflict:
why_user_decision_is_required:
options:
tradeoffs:
recommended_option:
impact_of_confirmation:
```

사용자 답변을 받으면 결정 원장과 책임 원본에 반영하고 다음 충돌로 이동한다. 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 충돌을 권장안으로 확정하되, 프로젝트 코어를 바꾸는 새로운 유형의 충돌은 별도로 제시한다.

상세 공격 렌즈·판정표·회귀 프로토콜은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.

## Rules

1. `review-scope-map`은 전체 영향 범위와 보호 대상을 먼저 고정한다.
2. `attack`은 실패·모순·악용·누락·경계 조건과 수정·개선 후보를 최대한 찾는다.
3. `validate-critique`는 사실성, 발생 가능성, 영향, 범위, 수정 비용을 재판정한다.
4. `route-findings`는 기술적으로 결정 가능한 항목과 사용자 기획 결정을 요구하는 충돌을 분리한다.
5. `technical-review-proposal`은 기술 항목을 우선순위, 근거, 수정 방향, 영향 파일, 검증 방법과 함께 한 번에 정리한다.
6. `USER_DECISION_REQUIRED`는 동시에 여러 개 묻지 않고 가장 차단적인 충돌부터 하나씩 확정한다.
7. `refine-approved-findings`는 `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
8. `regression-recheck`는 기존 장점·정상 경로·코어·범위와 새 결함을 다시 공격한다.
9. `decision-report`는 반영·보류·기각·미검증, 사용자 확정 결정과 남은 위험을 모두 기록한다.

## Output contract

```md
## 검수 범위 지도와 보호 대상
## 공격 관점과 실패 가정
## finding·근거·심각도
## MUST_FIX / SHOULD_FIX / DEFER / REJECT / UNVERIFIED
## 기술적으로 자동 판단 가능한 검수안
## 사용자 기획 결정 필요 충돌 큐
## 이번에 확정한 사용자 결정
## 실제 반영한 최소 변경
## 보호한 코어·장점·범위
## regression-recheck 결과
## 남은 위험·미검증·다음 조건
```

## Quality gate

- 요청 파일만 보고 인접 정본·소비자·untouched 영향 파일을 누락하지 않는다.
- 기술적으로 판단 가능한 항목을 불필요한 사용자 질문으로 전가하지 않는다.
- 기획 충돌을 여러 개 한꺼번에 제시하지 않는다.
- `MUST_FIX`·승인된 `SHOULD_FIX` 외 항목을 몰래 반영하지 않는다.
- 프로젝트 코어를 바꾸거나 기능을 팽창시키지 않는다.
- 수정 뒤 `regression-recheck`를 수행한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
