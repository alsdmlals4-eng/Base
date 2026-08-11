# BCP-2026-022-execution-sandbox-authority-split-recovery — Execution Sandbox Remote-Authority Split Recovery

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/GRIMOIRE-`
- 기준 프로젝트 커밋: `d277a2f5cd4a57947d176e3c49ae7f8f6db97230`
- 관련 프로젝트 PR: `https://github.com/alsdmlals4-eng/GRIMOIRE-/pull/134`
- 관련 Decision: `GM-SPELL-WORKFLOW-UI-V2-01`, `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`
- Learning ID: `LRN-GR-20260812-01`
- 제출일: `2026-08-12`
- 상태: `SUBMITTED`
- 지식 상태: `PATTERN`
- Project Application: `APPLIED` — `GR-SYNC-20260812-21-TASK8-HANDOFF-BCP`와 기존 continuation owner에 remote/local receipt 분리를 실제 반영하고 focused current-state regression을 연결했다.
- Project Verification: 프로젝트 PR #134 exact reviewed head `71d0a814043275b9453c9bdb218eac1be9ae31fa`에서 current-state sync를 포함한 적용 가능한 CI가 통과했고, 일시적 external HTTP 525였던 Star Runtime POC는 동일 exact head 재실행에서 성공했다. PR #134는 `d277a2f5cd4a57947d176e3c49ae7f8f6db97230`으로 병합·new-main readback되었다.
- Existing Solution Verdict: `ABSORB` — 새 broad Skill보다 기존 intake/continuation/local-execution/verification owner에 capability-aware receipt split을 최소 흡수하는 후보이다.
- Base 구현 권한: `NOT_GRANTED_IN_THIS_STAGE`

## 관찰과 증거

GRIMOIRE Task8 PR-prep에서 한 executor가 모든 검증 채널을 동일하게 사용할 수 없다는 failure mode가 재현되었다.

1. exact linked worktree/branch/HEAD와 cached diff는 현재 dedicated Codex sandbox에서 읽을 수 있었다.
2. 같은 Codex sandbox에서 `git fetch origin main`은 linked-worktree administrative path인 `.git/worktrees/task8-spell-use-screen-v2/FETCH_HEAD` 쓰기에서 `Permission denied`로 실패했다.
3. 원격 상태를 쓰지 않는 대안으로 시도한 `git ls-remote origin refs/heads/main`도 같은 sandbox에서 `github.com:443` 연결 실패로 종료되었다.
4. 반면 별도 control-plane GitHub connector는 같은 작업창에서 GRIMOIRE `main`, open PR, Base `main`, open PR을 fresh-read할 수 있었다.
5. 실패한 Codex 시도들은 source edit, staging, commit, push, reset, restore, clean, rebase, amend를 하지 않았고 cached diff도 비어 있었다.
6. 프로젝트 PR #134는 이 차이를 `REMOTE_AUTHORITY_RECEIPT + LOCAL_EXECUTION_RECEIPT`로 분리하고, executor capability failure를 product failure와 분리하는 continuation contract를 실제 적용·검증·병합했다.

### Root Cause

원인은 repository 자체나 제품 상태가 아니라 **실행 채널별 capability boundary가 서로 다를 수 있는데도 remote authority freshness와 local executor readiness를 한 executor의 동일 명령 성공으로 묶은 것**이다.

특히 linked worktree는 main repository와 별도 working directory를 가지면서 repository의 administrative metadata를 공유한다. 공식 Git `git-worktree` 문서는 각 linked worktree가 repository `$GIT_DIR/worktrees/<id>` 아래 private administrative directory를 갖고, `$GIT_COMMON_DIR`을 통해 shared repository state를 참조한다고 설명한다. 따라서 sandbox가 working tree 파일을 읽을 수 있어도 해당 administrative path 또는 outbound network 쓰기/접근 권한까지 자동으로 가진다는 보장은 없다.

공식 근거:

- Git `git-worktree` documentation: https://git-scm.com/docs/git-worktree
- GitHub Required Status Checks troubleshooting: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

GitHub 문서는 required check가 현재 검증 대상 commit identity에서 성공해야 하며 head와 test-merge identity를 구분해야 한다고 설명한다. 본 제안의 receipt split은 Git/GitHub가 직접 규정한 이름이나 구현 방식이 아니라, **exact identity/freshness를 유지하면서 서로 다른 trusted capability channel을 결합해야 했던 프로젝트 증거에서 도출한 inference**다.

### Existing Base Coverage

현재 Base는 이미 다음 주변 책임을 가진다.

- `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` / `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`: exact project/worktree/environment identity와 fail-closed local startup을 요구한다.
- `BCP-2026-015-external-runtime-session-same-snapshot-recovery`: process/transport/session/registry가 같은 관측창에서 일치하지 않을 때 stale runtime locator를 버리고 bounded recovery를 수행한다.
- continuation/handoff 및 verification owner: stale state와 old-head evidence를 current truth로 승격하지 않고 fresh readback을 요구한다.
- PR validation identity: review head와 actual CI validation target을 분리해 current required checks를 검증한다.

그러나 현재 Base main에서 **remote repository authority receipt와 local executor receipt를 명시적으로 분리하고, 특정 sandbox의 network/shared-Git-metadata capability failure를 별도 blocker class로 보존하면서 다른 trusted remote channel을 freshness source로 사용할 수 있는 공용 fallback contract**는 확인되지 않았다.

따라서 BCP-015를 확장해 runtime session recovery와 repository-authority channel split을 한 책임으로 묶기보다, 기존 intake/continuation/local-execution/verification owner에 흡수할 material complement로 제안한다.

## 일반화 후보

### Proposed General Principle

작업이 remote repository truth와 local executor truth를 모두 요구할 때, 두 receipt의 생산자가 반드시 같을 필요는 없다. 대신 authority/freshness/capability를 각각 명시하고 결합해야 한다.

```text
REMOTE_AUTHORITY_RECEIPT
  source/tool
  repository + ref
  exact remote SHA
  same-goal/open-PR snapshot when relevant
  observed-at/freshness boundary

+

LOCAL_EXECUTION_RECEIPT
  exact local repository/worktree
  branch + HEAD
  cached/staged state
  required local tool/session readiness
  current local tests/QA where required

+

EXECUTOR_CAPABILITY_BLOCKER
  blocked operation
  denied capability: network | shared-git-metadata | credential | other
  original failure payload without secrets
  retry/disposition

→ CURRENT_TASK_RESUME_DECISION
```

공용 후보 규칙:

1. **Capability failure와 project failure를 분리한다.** local executor가 remote query를 수행하지 못했다는 사실만으로 remote repository가 invalid하다고 판정하지 않는다.
2. **대체 remote receipt는 승인된 trusted authority channel이어야 한다.** repository/ref/exact SHA와 readback 시점을 식별할 수 없는 검색 결과·과거 로그·대화 기억으로 대체하지 않는다.
3. **Local receipt를 remote receipt로 대체하지 않는다.** 외부 connector가 최신 `main`을 증명해도 exact local worktree/branch/HEAD/staged state/tool readiness는 local executor가 별도로 증명해야 한다.
4. **Remote receipt를 local mutation 권한으로 확대하지 않는다.** connector가 fresh remote state를 읽었다고 해서 sandbox가 실패했던 stage/commit/push/shared-metadata mutation까지 수행 가능한 것으로 간주하지 않는다.
5. **같은 실패를 의례적으로 재현하지 않는다.** capability가 이미 같은 work unit에서 정확히 분류되었고 trusted alternate channel이 freshness를 제공한다면 blocked remote read를 반복해 independent local verification을 계속 막지 않는다.
6. **Remote write 직전에는 remote authority를 다시 읽는다.** PR 생성/업데이트/merge, shared Registry write 같은 concurrency-sensitive mutation 전에는 실제 write-capable authority channel에서 latest main/open PR/race state를 fresh-read한다.
7. **Receipt freshness invalidation을 정의한다.** relevant main/ref/PR/head가 이동했거나 work unit이 바뀌었으면 이전 remote receipt를 current truth로 재사용하지 않는다.
8. **대체 trusted channel이 없으면 `BLOCKED_UNVERIFIED`를 유지한다.** receipt split은 추측을 허용하는 escape hatch가 아니다.

### Existing Solution Verdict

`ABSORB`

별도 broad Skill을 만드는 것보다 기존 project intake/continuation/local executor/verification owner의 recovery reference와 tests에 최소 규칙을 흡수하는 편이 책임 중복을 줄인다. 실제 Base active 구현은 이 제안 저장 단계에서 수행하지 않는다.

## 프로젝트 전용으로 남길 내용

다음은 GRIMOIRE 전용이므로 Base 공용 규칙으로 승격하지 않는다.

- `C:\Users\user\Documents\GitHub\Ninza\GRIMOIRE-\.worktrees\task8-spell-use-screen-v2` 경로
- `feat/task8-spell-use-screen-v2` / `8c611f...` Task8 local identity
- HiGodot `8001/9501`, Hera `8770-8785`, project-scoped `CODEX_HOME`, Hera profile/token wrapper
- Godot 4.7.1 / HiGodot 3.1.4 / Hera 1.0.0 / GUT 9.7.1 exact project tool policy
- Task8 9-path commit allowlist, GUT counts, Hera acceptance semantics
- `CURRENT_DEDICATED_CODEX_REUSE_ALLOWED_FOR_CODEX_ONLY_CONTINUATION`라는 사용자의 GRIMOIRE workflow preference
- `GM-SPELL-WORKFLOW-UI-V2-01` 및 GRIMOIRE Stage3/gameplay authority

또한 모든 프로젝트가 connector와 local executor를 동시에 갖는다고 가정하지 않는다.

## 적용 조건과 비사용 조건

### Use When

다음이 모두 또는 실질적으로 성립할 때 사용한다.

- current task가 remote authority freshness와 local execution evidence를 모두 요구한다.
- local executor가 worktree/local tests를 읽고 수행할 수 있으나 remote network 또는 shared repository metadata operation 중 일부가 capability boundary로 막힌다.
- blocked operation과 원 실패 payload가 민감정보 없이 보존되어 있다.
- 별도의 승인된 trusted remote authority channel이 exact repository/ref/SHA를 fresh-read할 수 있다.
- local mutation/validation은 여전히 local receipt로 독립 검증한다.
- remote write 직전 다시 race/freshness check할 수 있다.

### Do Not Use When

- local HEAD/worktree/branch 자체가 기대 identity와 다르다.
- source/product tests가 실제로 실패했다.
- remote repository state 자체가 여러 trusted sources에서 불일치한다.
- 사용할 수 있는 remote source가 과거 handoff, 오래된 로그, 추론뿐이다.
- remote write가 필요한데 현재 어느 approved channel도 그 write와 final race check를 수행할 수 없다.
- connector가 반환한 SHA의 repository/ref identity 또는 freshness를 증명할 수 없다.
- capability error를 고치거나 사용자에게 노출해야 할 보안/운영 incident인데 receipt split으로 숨기려 한다.

## 반례와 위험

### Counterexamples

1. **Local HEAD mismatch:** external connector가 remote `main`을 정확히 읽어도 local branch가 잘못된 HEAD라면 local gate는 실패다.
2. **Real source failure:** local GUT/compile/parser failure는 remote connector receipt로 우회할 수 없다.
3. **Stale connector receipt:** connector read 이후 main이나 same-goal PR이 이동했다면 write/merge 전에 새 read가 필요하다.
4. **Write capability missing:** commit/push/shared Registry mutation 자체가 sandbox에서 불가능하면 read receipt를 대체하는 것이 아니라 capable executor 또는 connector write path로 경계를 넘겨야 한다.
5. **Untrusted secondary source:** 웹 검색 snippet이나 기억된 SHA를 authoritative remote receipt로 사용하면 안 된다.
6. **Same-goal concurrency:** proposal ID/Registry처럼 공유 namespace가 동시에 바뀌는 경우 branch creation 때의 remote receipt만으로 merge할 수 없고 final race check가 필요하다.

### Risks

- receipt별 timestamp/identity를 기록하지 않으면 split-brain state가 생길 수 있다.
- capability failure를 너무 넓게 분류하면 실제 Git/network/config 결함을 영구 우회할 수 있다.
- remote connector가 local mutation까지 승인한 것으로 오해될 수 있다.
- local executor의 stale HiGodot/runtime session을 과거 acceptance evidence로 잘못 재사용할 수 있다.
- 같은 Goal owner가 분산되면 새로운 broad Skill/문서 중복이 생길 수 있다.

Mitigation은 exact identity, freshness invalidation, explicit capability blocker, existing-owner `ABSORB`, remote-write final race check, fail-closed fallback 부재 상태다.

## 영향 범위와 검증

### Potential Affected Consumers — future implementation candidate only

실제 구현 승인이 별도로 주어질 경우 다음 기존 owner chain을 먼저 평가한다.

- project intake / continuous-work recovery reference
- maintaining project context and handoff
- project-dedicated local executor bootstrap/continuation reference
- reviewing/validating project changes
- canonical/reference freshness and exact validation identity tests
- project adapter / generated consumer는 기존 owner 변경이 실제 routing에 영향을 줄 때만 동기화한다.

새 broad Skill 생성은 기본값이 아니다.

### Validation Plan

별도 구현 단계가 승인된다면 최소 다음 behavior를 검증한다.

1. remote/local receipt source가 동일하고 모든 capability가 있는 정상 경로 — 기존 route 유지.
2. local executor remote-read capability만 막히고 trusted remote connector가 fresh exact SHA를 제공 — independent local checks는 계속 가능.
3. local executor의 shared-Git-metadata write가 막힘 — remote receipt가 stage/commit/push 권한으로 확대되지 않음.
4. alternate remote source가 stale/ambiguous — `BLOCKED_UNVERIFIED`.
5. local HEAD mismatch 또는 local test failure — remote receipt가 failure를 덮지 않음.
6. remote main/open PR이 write 직전에 변경 — stale receipt 폐기 + final race recheck.
7. same-goal BCP/Registry collision — 다른 project entry를 덮지 않고 own delta만 재할당/재구성.
8. non-selection case — 단일 executor가 모든 required capability를 정상 보유하면 추가 split ceremony를 강제하지 않음.

### Regression Plan

- existing dedicated-local-environment fail-closed checks 유지
- BCP-015 runtime-session recovery semantics 유지
- continuous-work blocker taxonomy와 충돌하지 않음
- required CI validation identity freshness 유지
- proposal-only lifecycle/approval boundary 유지

### Rollback

이번 단계는 proposal-only 문서/Registry entry만 추가한다. 문제가 있으면 proposal-only merge를 revert하거나 proposal lifecycle에서 reject/supersede할 수 있으며 Base active runtime/Skill behavior에는 즉시 변경이 없다.

## 필요한 도구·파일·권한

이번 proposal storage 단계에 필요한 것은 다음뿐이다.

- Base current `main` read access
- `[수정제안서]/README.md`
- `[수정제안서]/PROPOSAL_REGISTRY.json`
- `templates/BASE_CHANGE_PROPOSAL.md`
- `tools/check_base_change_proposals.py` 및 현재 proposal validation CI
- open proposal PR / same-goal PR read access
- source project PR #134/new-main readback
- `[수정제안서]/**` proposal-only write/PR/merge 권한

필요하지 않으며 이 단계에서 금지되는 것:

- Base active `skills/**`, `docs/**`, `templates/**`, `tools/**`, `tests/**`, workflow 수정
- source project product 파일 변경
- Hera/HiGodot product authoring
- 다른 프로젝트 proposal branch/Registry entry 수정

## 승인과 구현

```yaml
proposal_status: SUBMITTED
proposal_storage_merge_authority: GRANTED_BY_CURRENT_HANDOFF_INSTRUCTION
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
implementation_status: NOT_STARTED_IN_THIS_STAGE
approval_ref: null
implementation_pr: null
implementation_boundary: SEPARATE_FOLLOWUP_STAGE
```

이 proposal-only PR의 저장·병합은 Base 활성 구현 승인이 아니다. 본 제안이 추후 `APPROVED_FOR_IMPLEMENTATION`으로 승격되더라도 실제 Base Skill/reference/template/test/tool/workflow 구현은 별도 사용자 승인·별도 구현 단계에서만 수행한다.
