# 프로젝트 코어 계약

## 메타데이터

```yaml
project:
core_status: CONFIRMED/PROVISIONAL/CONFLICTED/MISSING
baseline_ref:
owner:
confirmed_by:
confirmed_at:
next_review_trigger:
```

## 코어 요약

> 이 프로젝트는 `[대상]`이 `[핵심 문제·욕구]`를 해결하도록 `[핵심 경험]`을 제공하며, `[핵심 루프]`를 통해 `[핵심 가치]`를 반복적으로 만든다. `[불변조건]`이 훼손되면 프로젝트 정체성이 바뀐다.

## Project Core Contract

```yaml
project_core:
  status:
  purpose:
  target_users_or_players:
  core_problem_or_need:
  core_value:
  core_experience:
  core_loop_or_workflow:
  differentiators: []
  invariants: []
  replaceable_elements: []
  explicit_non_goals: []
  success_signals: []
  failure_signals: []
  evidence:
    user_approval_refs: []
    canonical_source_refs: []
    product_or_test_refs: []
  unresolved_conflicts: []
  change_authority:
  review_triggers: []
```

## 근거 지도

| 코어 주장 | 책임 원본 | 실제 제품·테스트 | 사용자 승인 | 상태 |
|---|---|---|---|---|
|  |  |  |  | CONFIRMED/ASSUMED/UNVERIFIED/CONFLICTED |

## 충돌·미확정 장부

| ID | 주장 A | 주장 B·실제 상태 | 영향 | 해결 권한 | 상태 |
|---|---|---|---|---|---|
| CORE-C01 |  |  |  | 사용자/책임자/증거 | OPEN/RESOLVED |

## 코어 검증

### Removal test

- 제거할 요소:
- 제거 후 핵심 가치 유지 여부:
- 판정:

### Replacement test

- 교체할 요소:
- 교체 후 핵심 경험 유지 여부:
- 판정:

### Identity test

- 변경 시 같은 프로젝트로 인식되는가:
- 근거:

### Dependency test

- 정체성 의존성:
- 단순 기술 결합:

### Evidence test

- 승인 문서:
- 실제 동작:
- 사용자·플레이어 반응:

### Decision test

대표 변경안을 판정한다.

| 변경안 | 판정 | 근거 |
|---|---|---|
|  | CORE_PRESERVING/CORE_SUPPORTING/CORE_RISK/CORE_CHANGING/CORE_CONFLICT |  |

## 책임 원본 연결

- Core canonical source:
- Design Document Registry:
- Documentation Map:
- Active Context·Handoff:
- 관련 테스트·검증:

## 최종 상태

- Core status:
- 사용자 결정 필요:
- 남은 위험:
- 다음 검토 트리거:
