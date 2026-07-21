---
name: running-adversarial-review-and-refinement
description: Use when a design, plan, document, code proposal, data change, UX flow, or other work product should be attacked as if it failed, its criticisms independently validated, only justified findings refined, and the revised result regression-checked without changing project core or adding unnecessary scope.
---

# Running Adversarial Review and Refinement

## Core principle

적대적 검토는 작업물을 승인하려는 평가가 아니라 승인 거부 증거를 찾는 독립 공격 단계다. 그러나 레드팀의 비판도 오류·취향·과잉 요구일 수 있으므로 그대로 반영하지 않는다.

```text
레드팀은 최대한 공격한다.
검증자는 그 비판마저 의심한다.
개선자는 검증된 문제만 수정한다.
회귀 검토자는 수정으로 생긴 새 문제를 찾는다.
```

목적은 작업물을 무조건 부정적으로 바꾸는 것이 아니라, 프로젝트 코어와 기존 장점을 보호하면서 실제 실패 가능성이 있는 결함만 제거하는 것이다.

## Distinguish

| 작업 | 이 Skill | 다른 Skill |
|---|---|---|
| 초안·기획·계획·제안의 실패 조건 공격 | 책임짐 | - |
| 비판의 유효성·우선순위 재판정 | 책임짐 | - |
| 승인된 finding만 최소 개선 | 승인 범위에서 책임짐 | 실제 파일 변경 권한은 작업 계약 |
| 수정 후 새 위험·기존 장점 회귀 검사 | 책임짐 | 실행 증거가 필요하면 변경 검증 |
| 실제 diff·정적·런타임·접근성·성능 통합 검증 | finding과 회귀 질문 제공 | `reviewing-and-validating-project-changes` |
| 프로젝트 코어 판정·확정 | 보호 기준으로 소비 | `identifying-project-core`, `establishing-project-core` |
| 전문 UI 시각 감사 | 일반 UX 실패만 탐색 | `auditing-and-refining-ui-art` |

## Work Mode and Skill Modes

기본 흐름은 `REVIEW → 필요한 경우 BUILD → REVIEW`다.

- `attack`: 실패를 가정하고 결함·허점·반례를 최대한 찾는다.
- `validate-critique`: 각 지적의 근거·발생 가능성·효과·비용을 다시 판정한다.
- `refine-approved-findings`: `MUST_FIX`와 `SHOULD_FIX`만 최소 수정한다.
- `regression-recheck`: 수정 전후 차이와 새 위험을 다시 공격한다.
- `decision-report`: 반영·보류·기각·미검증과 남은 위험을 보고한다.

`attack`과 `validate-critique`는 관점을 분리한다. 같은 모델이나 사람이 수행해도 단계별 입력과 출력은 섞지 않는다.

## Required inputs

```yaml
work_product:
approved_requirements_and_scope:
project_core:
current_canonical_sources:
actual_implementation_or_diff:
known_constraints:
acceptance_criteria:
protected_strengths_and_assets:
validation_tools_and_environment:
change_authority:
```

프로젝트 코어가 확정되지 않았다면 핵심 충돌 판정은 `UNVERIFIED`로 두거나 먼저 관련 Skill을 호출한다.

## Roles

### 작성자·블루팀

- 초안·구현물을 만든다.
- 요구사항·의도·제약·보호 대상을 제시한다.
- 지적에 대한 근거를 제공한다.
- 승인된 개선을 반영한다.

### 레드팀

- 작업물이 실패했다고 가정한다.
- 승인 거부에 필요한 결함·모순·악용법·실패 조건을 찾는다.
- 칭찬이나 해결책보다 문제 발견에 집중한다.

### 검증자

- 레드팀 지적의 사실성과 중요도를 다시 검사한다.
- 실제 문제와 취향 차이·범위 밖 요구·중복을 분리한다.
- 수정 여부와 우선순위를 판정한다.

### 개선자

- 검증된 문제만 수정한다.
- 프로젝트 코어와 정상 동작·기존 장점을 보호한다.
- 수정 전후와 영향 범위를 기록한다.

### 회귀 검토자

- 수정 때문에 기존 기능·경험·데이터·호환성이 손상됐는지 검사한다.
- 새 예외·복잡성·미검증을 찾는다.

## Phase 1 — Attack

검토자는 다음 선언으로 시작한다.

> 이 작업물을 승인하는 조력자가 아니라 승인 거부 증거를 찾는 독립 레드팀 검토자다. 작업물이 실패했다고 가정하고 결함과 실패 조건을 찾는다.

다음 축을 우선 공격한다.

1. 프로젝트 코어와 충돌하는 부분
2. 승인된 요구·기획·범위와 다른 부분
3. 필요한 단계·조건·산출물의 누락
4. 최신화되지 않은 구형 파일·경로·내용
5. 논리적 모순·모호한 용어·판정 불가능한 조건
6. 구현 불가능하거나 비용이 과도한 요구
7. 사용자 경험·가독성·입력·피드백이 깨지는 지점
8. 빈 값·최대값·중복·취소·복귀·실패 등 예외에서 무너지는 구조
9. 악용·우회·경제 붕괴·데이터 손상 가능성
10. 과도한 복잡성·중복·불필요한 기능
11. 미검증된 가정과 근거 없는 확정
12. 수정·확장 시 인접 시스템을 손상시키는 의존성
13. 접근성·성능·플랫폼 장벽
14. 롤백·복구·호환성 부재

이 단계에서는 장점·칭찬·균형 잡힌 평가를 작성하지 않는다.

### Finding format

```yaml
finding_id:
problem:
violated_requirement_or_core:
why_it_matters:
failure_scenario:
evidence:
severity: CRITICAL/HIGH/MEDIUM/LOW
suggested_direction:
confidence:
```

근거가 없는 의심도 기록할 수 있지만 `evidence`와 `confidence`를 비워 두지 않고 가설임을 표시한다.

## Phase 2 — Validate critique

앞 단계의 지적을 그대로 수용하지 않고 다음을 확인한다.

- 실제 요구사항·프로젝트 코어·관찰 가능한 증거에 근거하는가?
- 단순한 취향 차이인가?
- 발생 가능성과 영향이 충분한가?
- 이미 다른 구조에서 대응하는 중복 지적인가?
- 현재 작업 범위 안에서 처리해야 하는가?
- 수정 비용보다 개선 효과가 큰가?
- 수정이 다른 코어 기능·장점·호환성을 손상시키지 않는가?
- 검증 가능한가?
- 해결책이 아니라 문제 정의 자체가 타당한가?

### Critique decisions

| 판정 | 의미 |
|---|---|
| `MUST_FIX` | 코어·요구·데이터·보안·핵심 UX·구현 가능성을 직접 손상한다. |
| `SHOULD_FIX` | 비차단 문제지만 개선 효과가 크고 현재 범위에서 합리적이다. |
| `DEFER` | 문제 가능성은 있으나 근거·우선순위·비용·선행 조건이 부족하다. |
| `REJECT` | 취향·잘못된 전제·중복·범위 밖·지나치게 낮은 가능성이다. |
| `UNVERIFIED` | 필요한 파일·환경·실행 증거가 없어 판정할 수 없다. |

검증 기록:

```yaml
finding_id:
decision:
decision_basis:
evidence_quality:
probability_and_impact:
cost_benefit:
core_and_regression_risk:
scope_fit:
```

레드팀의 높은 심각도가 자동으로 `MUST_FIX`가 되지는 않는다.

## Phase 3 — Refine approved findings

`MUST_FIX`와 `SHOULD_FIX`만 반영한다.

조건:

- 프로젝트 코어를 변경하지 않는다.
- 기존 장점·정상 동작·승인 자산을 훼손하지 않는다.
- 필요 이상의 기능을 추가하지 않는다.
- 현재 작업 계약 밖으로 범위를 확장하지 않는다.
- 가장 작은 수정으로 원인을 해결한다.
- 수정 전후 차이와 영향 범위를 명확히 기록한다.
- `DEFER`, `REJECT`, `UNVERIFIED`를 몰래 반영하지 않는다.
- 파일 수정 권한이 없으면 개선안만 제시한다.

수정 기록:

```yaml
finding_id:
decision:
before:
after:
reason:
changed_scope:
preserved_strengths:
new_risks:
validation_plan:
```

## Phase 4 — Regression recheck

수정된 결과를 다시 적대적으로 검토한다.

1. 프로젝트 코어가 유지되는가?
2. 승인 요구와 완료 기준을 충족하는가?
3. 기존 핵심 기능·장점·자산이 손상되지 않았는가?
4. 데이터·저장·ID·Schema·호환성이 유지되는가?
5. 새 예외·악용·복잡성이 생기지 않았는가?
6. 한 문제를 해결하면서 다른 문제를 만들지 않았는가?
7. 수정 전 실패 사례가 실제로 차단됐는가?
8. 미검증 내용을 완료로 표시하지 않았는가?
9. 접근성·성능·플랫폼 비용이 악화되지 않았는가?
10. 롤백 경로가 유지되는가?

### Regression decisions

- `PASS`
- `PASS_WITH_FOLLOWUP`
- `REVISE_AGAIN`
- `REJECT_CHANGE`
- `UNVERIFIED`

실제 코드·데이터·자산 변경이면 `reviewing-and-validating-project-changes`로 정적·런타임·회귀 증거를 확인한다.

## Severity guidance

- `CRITICAL`: 프로젝트 코어 붕괴, 데이터 손실, 보안·결제·출시 차단, 복구 불가.
- `HIGH`: 핵심 기능 실패, 주요 UX 차단, 경제·진행 붕괴, 광범위 회귀.
- `MEDIUM`: 제한된 조건의 실패, 반복 피로, 유지보수·명료성 저하.
- `LOW`: 영향이 작고 우회 가능하며 현재 목표를 직접 막지 않음.

심각도는 문제의 영향이고, 수정 판정은 근거·범위·비용까지 포함한 별도 결정이다.

## Example — Game design review

```text
기획자
→ 게임 시스템 초안 작성

레드팀
→ 재미가 사라지는 구간·반복 피로·악용 전략·경제 붕괴·모순·구현 난도를 공격

검증자
→ 실제 요구와 프로젝트 코어에 대조
→ 문제·취향·범위 밖 요구를 분리
→ MUST_FIX / SHOULD_FIX / DEFER / REJECT / UNVERIFIED 판정

개선자
→ 프로젝트 코어를 유지하며 승인된 finding만 최소 수정

회귀 검토자
→ 기존 시스템·경제·진행·UX·데이터가 손상되지 않았는지 재검사
```

## Output contract

```md
# 적대적 검토·개선 결과
## 검토 대상·요구·프로젝트 코어
## 레드팀 finding과 심각도
## finding별 근거·실패 사례
## 비판 검증 판정
## MUST_FIX·SHOULD_FIX
## DEFER·REJECT·UNVERIFIED와 이유
## 실제 반영한 수정
## 수정 전후 차이와 보호한 장점
## 새 위험·영향 범위
## 회귀 재검토 결과
## 실행한 검증·실행하지 못한 검증
## 남은 위험·롤백·다음 승인 조건
```

## Definition of Ready

- 검토 대상과 버전·범위가 고정됐다.
- 승인 요구·완료 기준·보호 대상이 있다.
- 프로젝트 코어 또는 코어 미확정 상태가 명시됐다.
- 현행 책임 원본과 실제 구현·diff를 찾을 수 있다.
- 개선 권한과 검증 환경이 구분됐다.

## Definition of Done

- 공격 단계가 칭찬이나 방어와 분리됐다.
- 모든 finding에 근거·실패 사례·심각도·신뢰도가 있다.
- 비판 자체를 다시 검증하고 다섯 판정으로 분류했다.
- 승인된 finding만 최소 수정했다.
- 프로젝트 코어와 기존 장점·정상 동작을 보호했다.
- 수정 전후와 새 위험을 기록했다.
- 회귀 재검토와 미실행 검증을 분리했다.

## Failure conditions

- 레드팀 지적을 검증 없이 전부 반영한다.
- 단순 취향을 치명적 결함으로 판정한다.
- 칭찬과 균형 평가 때문에 공격 강도를 낮춘다.
- 프로젝트 코어를 개선 명목으로 암묵적으로 변경한다.
- 필요 이상의 기능·추상화·리팩터링을 추가한다.
- `DEFER`, `REJECT`, `UNVERIFIED` finding을 몰래 수정한다.
- 실제 파일·diff·실행 증거 없이 완료로 판정한다.
- 수정 후 회귀 재검토를 생략한다.
- 접근성·성능·저장·호환성 위험을 적용 대상인데도 무시한다.

## Related skills and learning

- 코어 판정: `identifying-project-core`
- 코어 확정: `establishing-project-core`
- 핵심 컨셉·PoC: `analyzing-and-refining-game-concepts`
- 실제 변경 검증: `reviewing-and-validating-project-changes`
- 정본 변경 전파: `auditing-canonical-reference-freshness`
- 전문 UI 감사: `auditing-and-refining-ui-art`
- Learning Log: `skills/SKILL_LEARNING_LOG.md`
- 현재 지식 상태: `HYPOTHESIS`
- 검토 트리거: 비판 과수용, 취향의 결함화, 코어 훼손, 기능 팽창, 회귀 누락
