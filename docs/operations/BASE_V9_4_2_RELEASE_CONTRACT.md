# Base v9.4.2 Planning-First Grill Me Compatibility Release Contract

## 1. 목적

Base v9.4.2는 released v9.4.1 위의 호환 운영 릴리스다. 새 활성 Skill이나 Registry 변경 없이 PR #142의 기획 우선·Grill Me 결정 배치 계약을 정식 프로젝트 pin 대상으로 만든다.

```yaml
source_pr: 142
payload_commit: dd705d7f48a7919187bc0507610ba5fc5b43a658
release_issue: 144
registry_sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
```

## 2. 포함 범위

- `L1` 이상 `PLAN → 승인된 실행 계약 → BUILD → REVIEW`
- 가역적 상세 수치의 `DETAILED_NUMERIC_DEFAULT / RECOMMENDED_DEFAULT`
- 기획 충돌의 `PLANNING_CONFLICT / USER_DECISION_REQUIRED / GRILL_ME_REQUIRED`
- `MAX_APPROVED_DECISIONS_PER_BATCH: 10`과 조기 체크포인트
- 활성 배치 Branch의 Decision별 논리 Commit과 `APPROVED_PENDING_MERGE`
- latest exact-head 필수 검사와 `attack → validate-critique → regression-recheck → decision-report`
- 병합 후 merged main·Sheet 재조회와 `SYNCED_TO_MAIN`
- 작업 구조 벤치마킹·적대적 검토 감사 기록

## 3. 보호 경계

- `base-v9.4.1.lock.json`과 v9.4.1 payload·evidence를 수정하지 않는다.
- `skills/SKILL_REGISTRY.json` raw bytes를 수정하지 않는다.
- 실제 프로젝트 Grill Me 배치·외부 모델·사람 사용성 검증을 실행한 것으로 주장하지 않는다.
- 프로젝트 Adapter는 이 release가 `BASE_RELEASED`가 되기 전까지 v9.4.2를 선택하지 않는다.
- 프로젝트 제품 코드·기획 정본·Google Sheets는 Base release PR에서 변경하지 않는다.

## 4. 릴리스 단계

```text
1. source implementation PR #142 merge
2. trusted evidence PR
3. pin-finalization PR
4. six-project Adapter pin wave
```

### Trusted evidence

- merged payload Commit과 exact Registry SHA-256을 Evidence JSON에 기록한다.
- `base-v9.4.2.lock.json`은 `TRUSTED_EVIDENCE_PENDING`이며 evidence pin은 `null`이다.
- pending 상태는 프로젝트 실행 가능한 released pin이 아니다.

### Pin finalization

- trusted evidence PR의 squash merge Commit을 확인한다.
- payload → evidence → trusted main ancestry를 검사한다.
- lock을 `BASE_RELEASED`로 바꾸고 evidence Commit을 고정한다.
- project operating CLIs는 v9.4.2 lock을 지원하지만 null evidence pin에서는 fail closed한다.

## 5. 프로젝트 연결

릴리스 확정 뒤 각 프로젝트 Adapter는 다음을 같은 PR에서 갱신한다.

```yaml
base_release.version: 9.4.2
base_release.release_commit: dd705d7f48a7919187bc0507610ba5fc5b43a658
base_release.release_evidence_commit: <trusted evidence merge commit>
skill_registry.base.sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
planning_first_grill_me.policy_path: docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md
planning_first_grill_me.checkpoint_template: templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md
planning_first_grill_me.max_approved_decisions_per_batch: 10
planning_first_grill_me.actual_project_batch_execution: NOT_RUN
```

각 프로젝트는 Adapter·파생본·전용 CI를 독립적으로 검증하고 main에 병합한다.

## 6. 자동 검증

- lock/evidence JSON Schema
- v9.4.1 predecessor identity 보존
- payload·evidence·trusted history ancestry
- payload와 evidence Commit의 Registry raw SHA-256
- released policy·Template·test path 존재
- project operating contract의 v9.4.2 release-lock 지원
- 기존 Base v9 전체 계약과 Required CI

## 7. 증거 상한

```text
real project Grill Me batch execution: NOT_RUN
actual external model behavior: NOT_RUN
independent human/external review: NOT_RUN
runtime / device / accessibility: NOT_APPLICABLE
```

## 8. 롤백

- evidence 단계 실패: PR을 닫고 v9.4.1을 계속 사용한다.
- pin-finalization 실패: pending evidence 기록을 보존하고 프로젝트 pin wave를 시작하지 않는다.
- 프로젝트 연결 실패: 해당 프로젝트 PR만 revert하며 Base v9.4.1/v9.4.2 history를 rewrite하지 않는다.
