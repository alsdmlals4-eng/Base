# 적대적 비평–검증–개선 보고서

## 메타데이터

```yaml
review_target:
review_target_type:
baseline_ref:
review_mode: lightweight/standard/gate
risk_level: low/medium/high/critical
critic:
judge:
refiner:
verifier:
started_at:
completed_at:
```

## 검토 기준선

- 목적:
- 사용자·플레이어 가치:
- 완료 기준:
- 책임 원본:
- 실제 증거:
- 보호 대상:
- 제외 범위:
- 프로젝트 코어 참조:
- 적용한 검토 관점:
- 검증 방법:

## 증거 지도

| 주장·요구 | 근거 | 실제 상태 | 검증 방법 | 상태 |
|---|---|---|---|---|
|  |  |  |  | CONFIRMED/ASSUMED/PROPOSED/UNVERIFIED/CONFLICTED |

## 1. 적대적 비평 Findings

### ADV-001

```yaml
finding_id: ADV-001
lens:
claim:
evidence:
failure_scenario:
affected_requirement_or_value:
impact:
likelihood: high/medium/low/unknown
severity: critical/high/medium/low
confidence: high/medium/low
reproduction_or_observation:
proposed_direction:
```

## 2. 지적 검증

| Finding | 판정 | 판정 근거 | 검증된 증거 | 승인 필요 | 수정 범위 | 회귀 위험 |
|---|---|---|---|---|---|---|
| ADV-001 | MUST_FIX/SHOULD_FIX/DEFER/REJECT/NEEDS_DECISION |  |  |  |  |  |

## 3. 개선 계획

| Finding | 최소 변경 | 변경하지 않을 것 | 담당 | 검증 | 상태 |
|---|---|---|---|---|---|
|  |  |  |  |  | PLANNED/IN_PROGRESS/DONE/BLOCKED |

## 4. 실제 변경

| Finding | 변경 파일·산출물 | 변경 전 | 변경 후 | Diff·렌더·실행 근거 |
|---|---|---|---|---|
|  |  |  |  |  |

## 5. 독립 재검증

### 원래 실패 시나리오

- 재현 절차:
- 수정 전 결과:
- 수정 후 결과:
- 판정:

### 정상 경로

- 검증:
- 결과:

### 경계·오류 경로

- 검증:
- 결과:

### 회귀

- 보호 동작:
- 검증:
- 결과:

### 코어·프로젝트 고유 결정

- 관련 불변조건:
- 유지 여부:
- 근거:

### 새 결함

- 발견 여부:
- 영향:
- 후속 처리:

## 6. 반복 기록

| Cycle | 새 근거 | 해결된 MUST_FIX | 남은 MUST_FIX | 새 회귀 | 계속/종료 근거 |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |

## 7. 잔여 위험·보류·사용자 결정

### DEFER

### NEEDS_DECISION

### 미검증

### 잔여 위험

## 최종 판정

```yaml
final_decision: APPROVE/APPROVE_WITH_RISK/CHANGES_REQUIRED/BLOCKED/UNVERIFIED
all_must_fix_verified: true/false
acceptance_criteria_met: true/false/unknown
protected_properties_preserved: true/false/unknown
remaining_risks: []
next_action:
```
