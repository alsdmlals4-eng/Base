# Base v9.4.3 First-Prompt Intake Compatibility Release Contract

## 1. 목적

Base v9.4.3은 released v9.4.2 위의 호환 운영 릴리스다. 새 활성 Skill이나 Registry 변경 없이 PR #143의 `first-prompt → contract → Grill Me` 지시문 작성 계약을 정식 프로젝트 pin 대상으로 만든다.

```yaml
source_pr: 143
payload_commit: 7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8
source_exact_head: b2cd0f99827e8e2b34c42204de54a2bf5b447225
release_issue: 148
registry_sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
```

## 2. 포함 범위

- `managing-project-intake-and-work-contract`의 `first-prompt` Mode
- L1 이상 지시문의 `route → first-prompt → contract → clarify`
- 핵심 행동·결과·지배 기준을 첫 1~2문장에 배치하는 direction anchor
- 앞 배치가 권위를 높이지 않는 authority boundary
- Task·Context·Source·Constraints·Output·Validation 누락 검사
- Instruction과 Context 분리
- 설계·전략 작업의 조건부 `정석안 / 파격안 / 통합안`
- 실행 전 `Grill Me alignment gate`
- exact approval reference 재사용과 중복 질문 방지
- L0 오탈자·명백한 형식·동일 검사 재실행 예외

## 3. 보호 경계

- `base-v9.4.2.lock.json`과 v9.4.2 payload·evidence를 수정하지 않는다.
- `skills/SKILL_REGISTRY.json` raw bytes를 수정하지 않는다.
- 앞 문장의 위치를 사용자 최신 지시·정본·증거·`HARD_CONSTRAINT`보다 높은 권위로 취급하지 않는다.
- 모델별 성능·사람 이해도·재작업 감소·실제 프로젝트 채택을 검증한 것으로 주장하지 않는다.
- 프로젝트 Adapter는 이 release가 `BASE_RELEASED`가 되기 전까지 v9.4.3을 선택하지 않는다.
- Base release PR에서 프로젝트 제품 코드·기획 정본·Google Sheets를 변경하지 않는다.

## 4. 릴리스 단계

```text
1. source implementation PR #143 merge
2. trusted evidence PR
3. pin-finalization PR
4. six-project Adapter pin wave
```

### Trusted evidence

- merged payload Commit과 exact Registry SHA-256을 Evidence JSON에 기록한다.
- `base-v9.4.3.lock.json`은 `TRUSTED_EVIDENCE_PENDING`이며 evidence pin은 `null`이다.
- pending 상태는 프로젝트 실행 가능한 released pin이 아니다.

### Pin finalization

- trusted evidence PR의 squash merge Commit을 확인한다.
- payload → evidence → trusted main ancestry를 검사한다.
- lock을 `BASE_RELEASED`로 바꾸고 evidence Commit을 고정한다.
- project operating CLIs는 v9.4.3 lock을 지원하지만 null evidence pin에서는 project adoption을 금지한다.

## 5. 프로젝트 연결

릴리스 확정 뒤 각 프로젝트 Adapter는 다음을 같은 PR에서 갱신한다.

```yaml
base_release.version: 9.4.3
base_release.release_commit: 7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8
base_release.release_evidence_commit: <trusted evidence merge commit>
skill_registry.base.sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
first_prompt.base_contract_source: skills/managing-project-intake-and-work-contract/SKILL.md
first_prompt.direction_anchor_reference: skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md
first_prompt.instruction_flow: [route, first-prompt, contract, clarify]
first_prompt.unconfirmed_state: AWAITING_USER_CONFIRMATION
first_prompt.approval_reuse: REUSE_EXACT_APPROVAL_REFERENCE
first_prompt.actual_project_execution: NOT_RUN
```

각 프로젝트는 Base Skill 본문을 복제하지 않고 Adapter·파생본·전용 CI를 독립 검증한다.

## 6. 자동 검증

- lock/evidence JSON Schema
- v9.4.2 predecessor identity 보존
- payload·evidence·trusted history ancestry
- payload와 evidence Commit의 Registry raw SHA-256
- first-prompt reference·focused tests 존재
- project operating contract의 v9.4.3 release-lock 지원
- 기존 Base v9 전체 계약과 Required CI

## 7. 증거 상한

```text
cross-model behavior: NOT_RUN
prompt rework reduction: NOT_RUN
human comprehension and interview fatigue: NOT_RUN
real project Adapter execution: NOT_RUN
runtime / device / accessibility: NOT_APPLICABLE
```

## 8. 롤백

- evidence 단계 실패: PR을 닫고 v9.4.2를 계속 사용한다.
- pin-finalization 실패: pending evidence 기록을 보존하고 프로젝트 pin wave를 시작하지 않는다.
- 프로젝트 연결 실패: 해당 프로젝트 PR만 revert하며 Base v9.4.2/v9.4.3 history를 rewrite하지 않는다.
