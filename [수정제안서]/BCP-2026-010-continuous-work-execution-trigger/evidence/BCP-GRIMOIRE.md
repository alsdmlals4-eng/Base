# BCP - GRIMOIRE

## 역할

이 파일은 새 Base Change Proposal을 만들지 않는다.

GRIMOIRE에서 관찰된 Codex 사용량 제한 중단과 로컬-only worktree 복구 문제의 핵심은 현재 Base main의 `BCP-2026-010-continuous-work-execution-trigger` 및 기존 `maintaining-project-context-and-handoff` 책임이 이미 소유한다.

따라서 사용자의 최신 **`BCP - 프로젝트 이름`** 명명 규칙에 따라 GRIMOIRE 프로젝트 증거를 기존 canonical BCP 아래에 보강하고, 새 Registry 항목이나 중복 공용 규칙은 만들지 않는다.

```yaml
project_evidence_name: BCP - GRIMOIRE
source_project: alsdmlals4-eng/GRIMOIRE-
source_project_main_at_interruption: fcb5dbe1cbbb23ef195633b1f6680f45d46c5a3f
related_project_task: Task 8 — Spell Use Screen, Target Selection, and Expected Result
related_project_issue: 111
existing_solution_verdict: REUSE_BCP_2026_010
new_base_proposal: false
new_registry_entry: false
new_active_base_behavior: false
```

## 프로젝트 관찰 — 사용량 제한과 local-only authoritative work

승인된 `GM-SPELL-WORKFLOW-UI-V2-01` 구현 중 Task 8은 Codex 사용량 제한으로 세션이 종료되었다.

중단 시점에는 다음 상태가 존재했다.

- local branch: `task8/spell-use-screen`
- local worktree: `C:/Users/user/Documents/GitHub/Ninza/GRIMOIRE-/.worktrees/task8-spell-use-screen/`
- remote Task 8 branch: 없음
- active Task 8 PR: 없음
- persistent GDScript authoring authority: `HIGODOT_ONLY`
- Hera authority: `LIVE_QA_AND_OBSERVABILITY_ONLY`
- last Editor evidence: `90 assertions / 0 failures`
- earlier full headless evidence: `43 suites / 1639 assertions / 0 failures`
- full headless freshness: 마지막 local edit보다 오래되어 최종 완료 증거로 재사용 불가

이 상황에서 원격 GitHub 상태만 보고 Task 8을 처음부터 다시 만들면 실제 최신 작업을 잃을 수 있다.

또한 `.gd`를 GitHub API나 일반 텍스트 도구로 재구성하면 HiGodot-only persistent authoring authority를 위반한다.

따라서 프로젝트 Issue #111에 SESSION HANDOFF를 영속화하고, 다음 세션은 기존 dirty worktree를 보존한 채 fresh HiGodot session과 fresh regression evidence부터 복구하도록 했다.

## 실제 인수인계 계약

Issue #111에 저장된 다음 재개 순서가 현재 프로젝트 복구 계약이다.

```text
fresh origin/main + Issue + local worktree readback
→ preserve dirty worktree
→ reconnect fresh HiGodot session
→ fresh-read authored .gd/.tscn
→ compile/import scan
→ Task 8 Editor regression
→ workflow/state/atomic-use regression
→ full headless fresh regression
→ adversarial review
→ P0/P1 = 0
→ protected delta + HERA_SOURCE_DELTA: NONE
→ fresh HiGodot receipt/readback
→ commit/push/PR
→ exact-head CI + review threads 0
→ merge inside approved scope
→ post-merge main fresh verification
→ Project Learning extraction
```

핵심 원칙은 **중단 이전 PASS를 현재 완료 증거로 자동 승격하지 않는 것**이다.

마지막 검증 이후 파일이 변했다면 이전 PASS는 historical evidence일 뿐이며 현재 작업 상태에서 다시 검증해야 한다.

## Existing Solution First

### Primary owner — BCP-2026-010

`BCP-2026-010-continuous-work-execution-trigger`는 연속작업 실행 루프와 blocker 이후의 계속 실행을 이미 소유한다.

GRIMOIRE 사례는 이 규칙의 구체적인 현실 사례다.

```text
CONTINUOUS_WORK
→ external executor limit
→ persist continuation state
→ resume same approved work
→ fresh verification
→ continue gates
```

따라서 새 broad Skill이나 별도 continuous-work BCP는 필요하지 않다.

### Supporting owner — maintaining-project-context-and-handoff

다음 세션이 다시 조사하지 않고 이어갈 수 있게 하기 위해 필요한 상태는 기존 handoff owner의 책임과 일치한다.

- current work
- authoritative source/worktree
- blockers
- stale verification evidence
- protected decisions
- next exact executable step
- runtime/repository truth 우선순위

### Supporting lifecycle — BCP-2026-013

`BCP-2026-013-post-merge-continuation-state-reconciliation`은 Task 8이 실제 병합된 뒤 적용되는 후속 lifecycle이다.

merge 전 handoff의 main SHA, PR state, CI state는 integration 후 stale해질 수 있으므로, post-merge runtime truth를 다시 관측해 live continuation state를 맞춰야 한다.

### Supporting lifecycle — BCP-2026-014

`BCP-2026-014-handoff-machine-consumer-compatibility-closeout`은 Handoff/Active Context 갱신 중 machine-consumed compatibility surface를 보존하거나 consumer를 migration하는 closeout 책임을 다룬다.

현재 GRIMOIRE 사례에서는 이와 별개의 새로운 machine-consumer failure는 확인되지 않았다.

## 현재 공용 판정

```yaml
finding_1:
  name: executor_usage_limit_with_local_only_authoritative_work
  verdict: REUSE_BCP_2026_010
finding_2:
  name: stale_pass_after_later_local_edits
  verdict: REUSE_EXISTING_VERIFICATION_DISCIPLINE
finding_3:
  name: authoring_authority_preserved_in_handoff
  verdict: REUSE_EXISTING_HANDOFF_AND_TOOL_AUTHORITY
new_base_gap_confirmed: false
```

즉 이 파일은 새로운 공용 규칙을 제안하기보다 **GRIMOIRE가 기존 Base 규칙을 실제로 재사용한 증거**를 추가한다.

## 프로젝트 전용으로 남길 값

Base 공용 규칙으로 승격하지 않는다.

- `GM-SPELL-WORKFLOW-UI-V2-01`
- Spell Use Screen의 UI/도메인 세부 규칙
- Stage 2 / Stage 3 주문 처리 구현 자체
- `task8/spell-use-screen`이라는 구체 branch 이름
- 특정 assertion/suite 수치
- 특정 HiGodot session id
- GRIMOIRE Issue/PR 번호 자체

## Task 8 완료 후 재평가

현재 Task 8은 완료·병합 상태가 아니다.

Task 8 post-merge verification 뒤에는 프로젝트 교훈을 다시 추출한다.

```text
TASK8_POST_MERGE_VERIFY
→ PROJECT_LEARNING_EXTRACT
→ PROJECT_ONLY / BASE_CANDIDATE / SPLIT / NO_PROMOTION
→ EXISTING_SOLUTION_FIRST
→ REUSE / ABSORB / REFACTOR / BUILD_NEW
```

새로운 재사용 가능한 gap이 없다면 본 `BCP - GRIMOIRE` 증거는 `REUSE_BCP_2026_010` 근거로 종료한다.

새로운 gap이 실제로 확인될 경우에도 먼저 기존 Base BCP/owner와 같은 Goal인지 재검사하며, 중복 proposal을 만들지 않는다.

## 검증 ceiling

```yaml
usage_limit_interruption: OBSERVED
local_only_task8_state: OBSERVED_AND_PERSISTED_IN_PROJECT_HANDOFF
fresh_final_task8_regression: NOT_RUN_YET
task8_merge: NOT_DONE
existing_solution_alignment: CONFIRMED_BY_CURRENT_BASE_REVIEW
base_active_implementation: NOT_CHANGED
```

이 증거 파일의 병합은 GRIMOIRE 프로젝트 학습 기록을 기존 BCP-010에 연결하는 것만 의미한다. 활성 Base Skill·Method·Template·Tool·Test·Workflow 동작을 변경하거나 구현 승인하지 않는다.
