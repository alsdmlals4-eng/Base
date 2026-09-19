# Feature Spec Traceability Packet

> 적용: `L2 이상` 승인 작업 중 Requirement가 여러 Task·파일·검증으로 분산될 때
> 권한: 이 Packet은 **별도 책임 원본이 아니다**. 승인 Decision·분야 정본·실제 구현·테스트를 ID와 경로로 연결한다.
> 비사용: L0·L1 단일 수정, 아직 승인되지 않은 아이디어, 상세 정본을 새로 작성해야 하는 경우

## 1. Packet identity

```yaml
packet_id:
work_level: L2 | L3 | L4
design_spec_id:
canonical_design_spec_path:
approval_reference:
source_commit:
created_at:
updated_at:
coverage_status: GAP | BLOCKED_UNVERIFIED | CONVERGED
```

`design_spec_id`와 `canonical_design_spec_path`는 승인된 L2 상세 설계 정본을 가리킨다. Packet은 해당 Spec의 Player Flow·규칙·상태·수치·edge case·전문 분야 내용을 복사하지 않는다.

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

`GAME_FEATURE_DESIGN_SPEC.md`가 사용된 기능이면 그 문서와 더 정밀한 전문 분야 정본을 `canonical_sources`에 연결한다. Packet은 구현·검증 추적용 파생층이며 상세 설계를 다시 소유하지 않는다.

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
- 상세 설계가 바뀌면 먼저 `canonical_design_spec_path`의 정본과 승인 Decision을 갱신한 뒤 Packet 연결을 재대조한다.

## 7. Phase ownership

```text
managing-project-intake-and-work-contract
→ Decision·Requirement·Acceptance ID와 범위 연결

managing-design-documents
→ canonical_source·Section·Decision 동기화
→ 필요한 L2 기능의 GAME_FEATURE_DESIGN_SPEC 정본 유지

reviewing-and-validating-project-changes
→ 실제 diff·runtime·test evidence 대조와 coverage_status 재계산
```

## 8. Player-experience verification linkage

L2 이상 플레이어-facing 기능은 [Base 재미 검증 생명주기](../../skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md#fun-verification-lifecycle)의 경험 가설을 기존 행에 연결한다. L0·L1에 이 Packet을 새로 요구하지 않는다.

- §2 `canonical_sources`에 승인된 프로젝트 핵심 경험과 기능 Spec의 Experience Intent/Planned evidence 위치를 참조한다. 목표나 성공 기준의 전문을 이 Packet에 복제하지 않는다.
- §3의 같은 `requirement_id`를 실제 `implementation_paths`와 경험 가설의 Acceptance에 연결한다. 아직 없는 Scene·데이터·자산 경로는 계획/누락이지 IMPLEMENTED가 아니다.
- §4의 `verification_id`를 MACHINE·RUNTIME·HUMAN 질문별로 분리하고 같은 Requirement에 연결한다. 결과 owner의 exact 빌드·환경·구간·대상·행동 관찰·자기보고·필요한 로그·반증을 참조한다. 사람 검증이 없으면 HUMAN은 `NOT_RUN`이며 기계 검사 결과를 복사하지 않는다.
- 재미 관련 근거가 반박되거나 불충분하면 기존 Decision에 최소 수정 또는 재검증을 연결하고 §5에 owner·다음 행동을 남긴다. 로그·AI 점수만으로 `FUN_PASS`를 만들지 않는다.
- `CONVERGED`는 §6의 승인된 현재 scope에 대한 연결·검증 수렴이다. 필요한 HUMAN 검증이 남으면 `GAP / BLOCKED_UNVERIFIED`를 유지한다. HUMAN 검증이 scope 밖인 기술 구현 Packet이 수렴하더라도 재미·사용자 승인·출시 PASS를 뜻하지 않는다.
- 프로젝트에 설치할 때 Base 내부 상대 링크를 채택된 project-local owner 또는 exact Base commit permalink로 바꾸고 링크를 다시 확인한다.
