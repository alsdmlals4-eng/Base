# Base v9.4.4 Reuse-First Intake Compatibility Release Contract

## 1. 목적

Base v9.4.4는 released v9.4.3 위의 호환 운영 릴리스다. 새 활성 Skill을 만들지 않고 PR #669의 `REUSE_FIRST_PREFLIGHT_REQUIRED`와 `REUSE_LEARNING_HANDOFF_REQUIRED`를 기존 프로젝트 Base Adapter가 pin할 수 있는 정식 release identity로 만든다.

```yaml
source_pr: 669
payload_commit: 210ec78292fa12ed7563ba743b322dd36103ae4a
source_exact_head: e9a081b0aa9d046bfdec819ef2b88b7d1f115ec8
release_issue: 670
registry_sha256: <derived from payload raw bytes>
```

## 2. 포함 범위

- 신규/의미 있는 개정 작업의 `REUSE_FIRST_PREFLIGHT_REQUIRED`
- current project implementation/assets/tests 우선 확인
- 승인·수집된 Project Asset/Reference/Benchmark 확인
- Base reuse handoff/profile/matrix/Registry 확인
- 현재 결정과 관련된 Base accumulated knowledge/case/reference 확인
- Registry/profile/current bottleneck이 직접 가리키는 targeted cross-project evidence만 확인
- 현재 결정을 바꾸는 데 필요한 external benchmark/professional practice/success-failure cases
- owner별 reuse/adapt/reference/no-reuse disposition 뒤 unresolved gap만 신규 제작
- 적용 대상 `NOT_RUN`의 신규 제작/`BUILD_NEW` 차단
- 동일 승인 범위·같은 consumer·freshness가 유지된 `REUSED_EVIDENCE`
- 순수 기계적 no-new-design 작업의 reasoned `NOT_APPLICABLE`
- 종료 시 `REUSE_LEARNING_HANDOFF_REQUIRED`
- 새 reuse lesson이 없을 때 `NO_NEW_REUSE_LEARNING`으로 Registry churn 없이 종료

## 3. 보호 경계

- `base-v9.4.3.lock.json`과 v9.4.3 payload/evidence/finalization history를 수정하지 않는다.
- Base reference가 프로젝트 canon·identity·approved decision보다 높은 권위를 갖지 않는다.
- 모든 프로젝트를 전수 검색하지 않는다.
- candidate discovery를 project adoption, Asset 승인, runtime proof, player/human evidence로 승격하지 않는다.
- external benchmark는 프로젝트/Base 축적 자료를 건너뛰기 위한 기본 경로가 아니다.
- 프로젝트 Adapter는 이 release가 `BASE_RELEASED`이고 finalization identity가 release index에 고정되기 전까지 v9.4.4를 선택하지 않는다.
- Base release PR에서는 게임 코드·프로젝트 canon·게임 데이터·Asset·Google Sheets를 변경하지 않는다.

## 4. 릴리스 단계

```text
1. source implementation PR #669 merge
2. trusted evidence PR
3. pin-finalization PR
4. finalization identity index PR
5. six-project Adapter pin wave
```

### Trusted evidence

- merged payload Commit과 payload Registry raw SHA-256을 Evidence JSON에 기록한다.
- `base-v9.4.4.lock.json`은 `TRUSTED_EVIDENCE_PENDING`이며 evidence pin은 `null`이다.
- pending 상태는 프로젝트 실행 가능한 released pin이 아니다.

### Pin finalization

- trusted evidence PR의 squash merge Commit을 확인한다.
- payload → evidence → trusted main ancestry를 검사한다.
- lock을 `BASE_RELEASED`로 바꾸고 evidence Commit을 고정한다.
- `docs/BASE_RULES_VERSION.md`의 latest compatible line을 v9.4.4로 승격한다.

### Finalization identity index

- finalization PR의 squash merge Commit을 확인한 뒤 `tools/base_release_index.py`에 immutable `finalization_commit` identity를 고정한다.
- strict project adapter validation은 이 index commit이 main에 존재하기 전 v9.4.4 adapter pin을 허용하지 않는다.

## 5. 프로젝트 연결

릴리스 및 finalization index 확정 뒤 기존 formal Adapter fleet의 각 프로젝트는 Base Skill 본문을 복사하지 않고 canonical `skills/PROJECT_BASE_ADAPTER.json`의 pin과 reuse-first adoption metadata만 갱신한다.

```yaml
base_release.version: 9.4.4
base_release.release_commit: 210ec78292fa12ed7563ba743b322dd36103ae4a
base_release.release_evidence_commit: <trusted evidence merge commit>
base_release.finalization_commit: <v9.4.4 finalization merge commit>
skill_registry.base.sha256: <payload Registry raw SHA-256>
reuse_first.base_contract_source: skills/managing-project-intake-and-work-contract/SKILL.md
reuse_first.handoff_source: docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json
reuse_first.required_gates:
  - REUSE_FIRST_PREFLIGHT_REQUIRED
  - REUSE_LEARNING_HANDOFF_REQUIRED
reuse_first.actual_project_execution: NOT_RUN
```

Adapter migration PR은 game code/canon/data/asset을 수정하지 않고 project-specific validator/CI로 exact pin을 검증한다.

## 6. 자동 검증

- lock/evidence JSON Schema
- released v9.4.3 predecessor identity 보존
- payload/source exact-head/issue/source-PR identity
- payload와 evidence의 Registry raw SHA-256
- payload·evidence·trusted-history ancestry
- reuse-first contract/handoff/focused regression paths 존재
- project operating contract의 v9.4.4 release-lock 지원
- 기존 Base v9 전체 Required CI

## 7. 증거 상한

```text
future agent execution adherence: NOT_RUN
human workflow usability: NOT_RUN
real project Adapter execution: NOT_RUN until each adapter PR is executed
cross-project reuse quality: NOT_RUN
runtime / device / accessibility: NOT_APPLICABLE
```

정적 release와 adapter pin은 앞으로의 모든 AI 세션이 규칙을 완벽하게 준수한다는 증거가 아니다. 대신 해당 프로젝트가 읽는 shared Base contract를 최신 고정 identity로 연결하고, 누락이 검증 단계에서 보이도록 만든다.

## 8. 롤백

- evidence 단계 실패: PR을 닫고 v9.4.3을 계속 사용한다.
- pin-finalization 실패: pending evidence를 보존하고 project rollout을 시작하지 않는다.
- finalization index 실패: v9.4.4 project pin을 시작하지 않는다.
- 프로젝트 연결 실패: 해당 프로젝트 Adapter PR만 revert하며 Base v9.4.3/v9.4.4 release history를 rewrite하지 않는다.
