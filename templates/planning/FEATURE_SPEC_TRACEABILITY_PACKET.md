# Feature Spec Traceability Packet

> 적용: `L2 이상` 승인 작업 중 Requirement가 여러 Task·파일·검증으로 분산될 때
> 권한: 이 Packet은 **별도 책임 원본이 아니다**. 승인 Decision·분야 정본·실제 구현·테스트를 ID와 경로로 연결한다.
> 비사용: L0·L1 단일 수정, 아직 승인되지 않은 아이디어, 상세 정본을 새로 작성해야 하는 경우

## 1. Packet identity

```yaml
packet_id:
work_level: L2 | L3 | L4
approval_reference:
source_commit:
created_at:
updated_at:
coverage_status: GAP | BLOCKED_UNVERIFIED | CONVERGED
```

## 2. Canonical authority

```yaml
canonical_sources:
  - source_id:
    path:
    section_or_record:
    authority:
protected_scope: []
excluded_scope: []
```

## 3. Traceability matrix

| decision_id | requirement_id | requirement summary | acceptance_criteria_ids | task_ids | implementation_paths | verification_ids | status |
|---|---|---|---|---|---|---|---|
| | | | | | | | PROPOSED / APPROVED / IMPLEMENTED / VERIFIED / BLOCKED |

## 4. Verification evidence

| verification_id | requirement_ids | method | exact command·environment | artifact·result | status |
|---|---|---|---|---|---|
| | | | | | NOT_RUN / PASSED / FAILED / BLOCKED_UNVERIFIED |

## 5. Coverage gaps

```yaml
unmapped_items:
  - item_type: decision | requirement | acceptance | task | implementation | verification
    item_id:
    reason:
    owner_skill:
    next_action:
unknowns: []
```

## 6. Convergence rules

- `CONVERGED`: 승인된 모든 `requirement_id`가 Acceptance·Task·실제 구현 경로·실행된 검증 증거에 연결되고 `unmapped_items`가 없다.
- `GAP`: 하나 이상의 연결이 없거나 정본과 실제 diff가 다르다.
- `BLOCKED_UNVERIFIED`: 필요한 정본·환경·권한·실행 결과가 없어 판정할 수 없다.
- 파일 존재, 체크 표시, 테스트 정의만으로 `CONVERGED`를 선언하지 않는다.
- Packet이 상세 책임 원본과 충돌하면 상세 정본을 수정 없이 우선하고 Packet을 낮은 상태로 재판정한다.

## 7. Phase ownership

```text
managing-project-intake-and-work-contract
→ Decision·Requirement·Acceptance ID와 범위 연결

managing-design-documents
→ canonical_source·Section·Decision 동기화

reviewing-and-validating-project-changes
→ 실제 diff·runtime·test evidence 대조와 coverage_status 재계산
```
