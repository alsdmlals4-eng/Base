# bcp-GRIMOIRE — GRIMOIRE 프로젝트 공용 교훈 기록

## 출처와 상태

- Proposal ID: `bcp-GRIMOIRE`
- 출처 프로젝트: `alsdmlals4-eng/GRIMOIRE-`
- 출처 프로젝트 기준 main: `fcb5dbe1cbbb23ef195633b1f6680f45d46c5a3f`
- 관련 프로젝트 작업: `Task 8 — Spell Use Screen, Target Selection, and Expected Result`
- 관련 프로젝트 Issue: `alsdmlals4-eng/GRIMOIRE-#111`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- Existing Solution Verdict: `REUSE`
- 신규 ACTIVE Skill: `0`
- 활성 Base 구현 권한: `NOT_GRANTED_IN_THIS_STAGE`

이 기록은 사용자의 최신 명명 규칙인 **`bcp - 프로젝트 이름`**을 적용한 GRIMOIRE 프로젝트 단위 Base 수정제안서다.

이번 proposal은 새 공용 규칙을 중복 생성하지 않는다. GRIMOIRE에서 관찰된 중단·인수인계·재개 문제를 기존 Base 책임에 연결하고, Task 8 완료 후 추가로 발견되는 교훈을 같은 프로젝트 기록에서 재평가할 수 있도록 보존한다.

## 관찰 사실

GRIMOIRE의 승인된 `GM-SPELL-WORKFLOW-UI-V2-01` 구현 중 Task 8이 Codex 사용량 제한으로 중단됐다.

중단 당시 중요한 특성은 다음과 같다.

1. 제품 변경은 원격 브랜치/PR이 아니라 로컬 `task8/spell-use-screen` worktree에 남아 있었다.
2. persistent `.gd` 저작 권위는 HiGodot-only이므로 GitHub API나 일반 텍스트 쓰기로 로컬 작업을 재구성해서는 안 됐다.
3. 마지막 Editor 검증은 `90 assertions / 0 failures`였지만, 전체 headless `43 suites / 1639 assertions / 0 failures` 증거는 마지막 로컬 수정 이전 결과라 최종 PASS로 재사용할 수 없었다.
4. 작업을 처음부터 다시 만들거나 destructive reset/clean을 하면 승인된 로컬 작업과 저작 증거를 잃을 수 있었다.
5. 따라서 프로젝트 Issue #111에 branch, worktree, authority, 마지막 증거, stale evidence, 다음 정확한 실행 단계와 Base 후속 단계를 포함한 SESSION HANDOFF를 저장했다.

## Existing Solution First

### Verdict

`REUSE`

현 시점에서 GRIMOIRE 사례는 새 broad Skill 또는 새로운 독립 Base 규칙을 요구하지 않는다.

이미 다음 Base 책임이 문제를 대부분 소유한다.

- `BCP-2026-010-continuous-work-execution-trigger`
  - 연속작업 실행과 blocker 이후 다음 executable 작업으로 복구하는 책임.
- `maintaining-project-context-and-handoff`
  - current state, resume locator, next work, blocker, runtime truth를 연결하는 책임.
- `BCP-2026-013-post-merge-continuation-state-reconciliation`
  - integration 이후 live continuation state를 실제 repository truth와 다시 맞추는 책임.
- `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`
  - handoff/active context 갱신 시 machine-consumed compatibility surface를 보존하거나 consumer를 migration하는 책임.

따라서 이번 GRIMOIRE 제안서는 위 책임을 복제하지 않고 **프로젝트 증거를 재사용 관계로 등록**한다.

## 공용화 후보와 현재 판정

### 후보 A — 사용량 제한 후 로컬 dirty worktree 복구

```text
executor usage limit / interruption
→ persist resume locator
→ preserve local dirty worktree
→ reconnect authorized authoring tool
→ fresh-read current local state
→ rerun stale verification
→ continue exact approved task
```

현재 판정: `REUSE_EXISTING_BASE_OWNERS`

새로운 Base 규칙으로 승격하지 않는다. Task 8 post-merge 학습에서 기존 owner가 이 상황을 실제로 표현하지 못하는 별도 gap이 확인될 때만 재평가한다.

### 후보 B — stale PASS 재사용 금지

중단 전에 PASS였더라도 이후 로컬 수정이 있었다면 그 증거는 현재 head/worktree의 완료 증거가 아니다.

현재 판정: `REUSE_EXISTING_VERIFICATION_DISCIPLINE`

### 후보 C — authoring authority를 handoff에 보존

HiGodot-only 같은 저작 권위는 다음 세션이 편의상 우회하지 못하도록 handoff에 포함돼야 한다.

현재 판정: `REUSE_EXISTING_PROJECT_HANDOFF_AND_TOOL_AUTHORITY`

## 프로젝트 전용으로 남길 내용

다음 값은 Base 공용 규칙으로 승격하지 않는다.

- `GM-SPELL-WORKFLOW-UI-V2-01`
- Task 8 화면/주문 도메인 규칙
- `task8/spell-use-screen` branch/worktree 이름
- 특정 assertion/suite 수치
- 특정 HiGodot session id
- GRIMOIRE의 Stage 2/Stage 3 주문 처리 세부 구현
- 특정 Issue/PR 번호

## 적용 조건

이 프로젝트 기록을 참고하는 경우:

- GRIMOIRE에서 작업이 외부 executor limit, 세션 종료, 도구 disconnect 등으로 중단됐을 때
- 로컬-only dirty state가 원격 GitHub보다 최신일 때
- persistent authoring authority가 별도 도구에 묶여 있을 때
- 이전 검증 증거가 마지막 변경보다 오래돼 stale일 때
- 다음 작업자가 현재 작업을 처음부터 재구현할 위험이 있을 때

## 비사용 조건

- 모든 변경이 이미 원격 PR에 commit/push되어 있고 local-only state가 없을 때
- 작업이 실제 완료·병합돼 fresh post-merge verification까지 끝났을 때
- 기존 handoff가 현재 repository/runtime truth와 모순될 때: 이 경우 handoff snapshot보다 fresh readback을 우선한다.

## Task 8 완료 후 재평가

Task 8이 실제 병합된 뒤에는 다음을 수행한다.

```text
TASK8_POST_MERGE_VERIFY
→ PROJECT_LEARNING_EXTRACT
→ PROJECT_ONLY / BASE_CANDIDATE / SPLIT / NO_PROMOTION
→ EXISTING_SOLUTION_FIRST
→ REUSE / ABSORB / REFACTOR / BUILD_NEW
```

새롭고 재사용 가능한 gap이 남지 않으면 `bcp-GRIMOIRE`는 `REUSE / NO_PROMOTION` 프로젝트 기록으로 유지한다.

새 gap이 확인되면 **새 숫자형 BCP를 자동 생성하지 않고**, 우선 이 `bcp-GRIMOIRE` 프로젝트 기록에 증거를 추가한 뒤 독립 공용 규칙이 실제 필요한지 별도 판단한다.

## 검증 시나리오

1. **Local-only interruption**
   - Given: 승인 작업이 로컬 dirty worktree에 있고 executor가 중단됨.
   - Expected: destructive reset 없이 branch/worktree/authority를 복구하고 fresh 검증부터 이어감.
2. **Stale verification evidence**
   - Given: 마지막 full regression 이후 로컬 파일이 수정됨.
   - Expected: 이전 PASS를 현재 PASS로 승격하지 않고 다시 실행함.
3. **Existing solution reuse**
   - Given: 기존 Base owner/BCP가 동일 문제를 이미 소유함.
   - Expected: 새 broad Skill/중복 BCP를 만들지 않음.
4. **Post-merge learning**
   - Given: Task 8이 병합됨.
   - Expected: 실제 최종 증거에서 새 공용 gap을 다시 추출하고 없으면 `NO_PROMOTION`으로 종료함.

## 범위와 보호

이번 proposal-only 단계의 허용 쓰기 범위:

```text
[수정제안서]/bcp-GRIMOIRE/**
[수정제안서]/PROPOSAL_REGISTRY.json
```

금지 범위:

```text
skills/**
docs/**
templates/**
tests/**
tools/**
.github/workflows/**
활성 Registry / generated consumer
```

## 승인과 구현

```yaml
proposal_status: SUBMITTED
existing_solution_verdict: REUSE
active_base_behavior_changed: false
approval_ref: null
implementation_pr: null
```

이 proposal의 Base main 병합은 **GRIMOIRE 프로젝트 교훈 기록을 저장하는 것**만 의미한다. 활성 Base 동작 변경이나 새 Skill 구현을 승인하지 않는다.
