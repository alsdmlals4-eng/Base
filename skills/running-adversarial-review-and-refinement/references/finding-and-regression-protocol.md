# 적대적 finding·회귀 상세 프로토콜

## 역할 분리

- 작성자·블루팀: 요구·의도·제약·보호 대상을 제시하고 승인된 개선만 반영한다.
- 레드팀: 작업물이 실패했다고 가정하고 승인 거부에 필요한 결함·모순·악용법·실패 조건을 찾는다.
- 검증자: 레드팀의 사실성·중요도·범위·비용을 다시 검사하고 취향·중복·잘못된 전제를 분리한다.
- 개선자: 검증된 문제만 최소 수정하고 수정 전후·영향 범위·보호 대상을 기록한다.
- 회귀 검토자: 기존 기능·경험·데이터·호환성과 새 예외·복잡성·미검증을 독립적으로 재검사한다.

## 공격 렌즈

1. 프로젝트 코어, 승인 요구와 범위 충돌.
2. 필요한 단계·조건·산출물 누락.
3. 오래된 책임 원본·파일·경로·내용.
4. 논리적 모순, 모호한 용어, 판정 불가능한 기준.
5. 구현 불가능하거나 비용이 과도한 요구.
6. 사용자 경로, 가독성, 입력, 피드백 실패.
7. 빈 값·최대값·중복·취소·복귀·재시도·실패 경계.
8. 악용·우회·경제 붕괴·데이터 손상·보안 위험.
9. 중복·과도한 복잡성·불필요한 기능과 유지보수 비용.
10. 미검증 가정, 근거 없는 확정, 인접 시스템 의존성.
11. 접근성·성능·플랫폼 장벽.
12. 저장·ID·Schema·호환성·롤백·복구 부재.

`attack`에서는 장점·칭찬·해결책으로 공격 강도를 희석하지 않는다. 장점 보호와 수정 여부는 뒤 단계에서 판단한다.

## Finding record

```yaml
finding_id:
problem:
violated_requirement_or_core:
why_it_matters:
failure_scenario:
evidence:
severity: CRITICAL/HIGH/MEDIUM/LOW
confidence:
suggested_direction:
```

근거가 없는 의심은 가설로 기록할 수 있지만 `evidence`와 `confidence`를 비워 두지 않는다.

## finding 검증

각 지적에 다음을 확인한다.

- 실제 요구·프로젝트 코어·책임 원본·관찰 증거에 근거하는가?
- 단순 취향, 중복, 범위 밖 요구, 해결책 선호인가?
- 발생 가능성과 실제 영향이 충분한가?
- 수정 비용보다 개선 효과가 큰가?
- 수정이 코어·기존 장점·호환성을 손상시키지 않는가?
- 현재 환경에서 검증 가능한가?

```yaml
finding_id:
decision: MUST_FIX/SHOULD_FIX/DEFER/REJECT/UNVERIFIED
decision_basis:
evidence_quality:
probability_and_impact:
cost_benefit:
core_and_regression_risk:
scope_fit:
```

레드팀의 높은 심각도가 자동으로 `MUST_FIX`가 되지는 않는다.

## 승인된 개선 기록

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

`DEFER`, `REJECT`, `UNVERIFIED`는 몰래 반영하지 않는다. 실제 파일 변경 권한이 없으면 개선안만 제시한다.

## 회귀 재검토

1. 원래 finding과 실패 사례가 실제로 사라졌는가?
2. 승인 요구·완료 기준·프로젝트 코어가 유지되는가?
3. 정상 경로와 기존 장점·자산이 손상되지 않았는가?
4. 데이터·저장·ID·Schema·호환성이 유지되는가?
5. 새 예외·악용·복잡성·접근성·성능·플랫폼 비용이 생기지 않았는가?
6. 롤백·복구 경로가 유지되는가?
7. 실행하지 못한 검사를 `UNVERIFIED`로 남겼는가?

회귀 결정은 `PASS / PASS_WITH_FOLLOWUP / REVISE_AGAIN / REJECT_CHANGE / UNVERIFIED` 중 하나다. 실제 코드·데이터·자산 변경은 `reviewing-and-validating-project-changes`의 정적·런타임 증거로 연결한다.

## 심각도

- `CRITICAL`: 코어 붕괴, 데이터 손실, 보안·결제·출시 차단, 복구 불가.
- `HIGH`: 핵심 기능 실패, 주요 UX 차단, 경제·진행 붕괴, 광범위 회귀.
- `MEDIUM`: 제한 조건 실패, 반복 피로, 유지보수·명료성 저하.
- `LOW`: 영향이 작고 우회 가능하며 현재 목표를 직접 막지 않는다.
