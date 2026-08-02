# Base v9.4.1 Skill Evidence Compatibility Release Contract

## 1. 목적

Base v9.4.1은 released v9.4.0 위의 호환·검증 릴리스다. 새 활성 Skill이나 Registry 변경 없이 다음 merged payload를 정식 프로젝트 pin 대상으로 만든다.

```yaml
source_pr: 138
payload_commit: 3f2c4a624d302b704c1b5322eb5c9f34ad55abb9
release_issue: 139
registry_sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
```

## 2. 포함 범위

- 활성 Skill 28개 primary·non-selection 행동평가 coverage
- 외부 모델 결과의 commit·Registry·평가셋 identity 검증
- 독립 reviewer context와 placeholder metadata 차단
- Skill별 구현 증거 Index와 결정적 파생 Matrix
- 외부 AI Worktree 격리 Schema·Template·검사기·회귀 테스트
- focused Skill evidence CI와 고정된 GitHub Action Commit

## 3. 보호 경계

- `base-v9.4.lock.json`과 v9.4.0 payload·evidence를 수정하지 않는다.
- `skills/SKILL_REGISTRY.json` raw bytes를 수정하지 않는다.
- 실제 외부 모델·실제 프로젝트 Worktree·엔진·기기·사람 검증을 실행한 것으로 주장하지 않는다.
- 프로젝트 Adapter는 이 release가 `BASE_RELEASED`가 되기 전까지 v9.4.1을 선택하지 않는다.
- 프로젝트 제품 코드·기획 정본·Google Sheets는 Base release PR에서 변경하지 않는다.

## 4. 릴리스 단계

```text
1. source implementation PR #138 merge
2. trusted evidence PR
3. pin-finalization PR
4. six-project Adapter pin wave
```

### Trusted evidence

- merged payload Commit과 exact Registry SHA-256을 별도 Evidence JSON에 기록한다.
- `base-v9.4.1.lock.json`은 `TRUSTED_EVIDENCE_PENDING`이며 evidence pin은 `null`이다.
- 이 상태는 프로젝트 실행 가능한 released pin이 아니다.

### Pin finalization

- trusted evidence merge Commit을 확인한다.
- payload → evidence → trusted main ancestry를 검사한다.
- lock을 `BASE_RELEASED`로 바꾸고 evidence Commit을 고정한다.
- `tools/project_operating_contract.py`는 v9.4.1 lock을 지원하지만 null evidence pin에서는 fail closed한다.

## 5. 프로젝트 연결

릴리스 확정 뒤 각 프로젝트 Adapter는 다음을 같은 PR에서 갱신한다.

```yaml
base_release.version: 9.4.1
base_release.release_commit: 3f2c4a624d302b704c1b5322eb5c9f34ad55abb9
base_release.release_evidence_commit: <trusted evidence merge commit>
skill_registry.base.sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
external_ai_worktree.base_validator_adoption: ADOPTED_FROM_BASE_V9_4_1
```

각 프로젝트는 Adapter·파생본·전용 CI를 독립적으로 검증하고 main에 병합한다.

## 6. 자동 검증

- lock/evidence JSON Schema
- v9.4.0 predecessor identity 보존
- payload·evidence·trusted history ancestry
- payload와 evidence Commit의 Registry raw SHA-256
- released validator path 존재
- project operating contract의 v9.4.1 release-lock 지원
- 기존 Base v9 전체 계약과 required CI

## 7. 증거 상한

```text
actual external model routing: NOT_RUN
independent external model/code review: NOT_RUN
real project external-AI worktree execution: NOT_RUN
engine runtime / target device / accessibility / human: NOT_RUN or NOT_APPLICABLE
```

## 8. 롤백

- evidence 단계 실패: PR을 닫고 v9.4.0을 계속 사용한다.
- pin-finalization 실패: pending evidence 기록을 보존하고 프로젝트 pin wave를 시작하지 않는다.
- 프로젝트 연결 실패: 해당 프로젝트 PR만 revert하며 Base v9.4.0/v9.4.1 history를 rewrite하지 않는다.
