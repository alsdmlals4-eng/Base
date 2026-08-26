# ChatGPT Work Project Execution Instruction v4.9 — Compatibility Appendix

> 이 appendix는 `CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md`와 함께 하나의 Work 실행 bundle을 구성한다. 본체가 current Base owner로 위임한 r5.4 호환 경계를 명시적으로 보존하며 독립적인 두 번째 정본이 아니다.

## 1. Default Project Entry — No Separate Goal Required

```text
PROJECT_PLUS_INSTRUCTION_IS_DEFAULT_SUFFICIENT_INPUT
SEPARATE_GOAL_NOT_REQUIRED_BY_DEFAULT
PROJECT_PLUS_INSTRUCTION_PLUS_OPTIONAL_GOAL_IS_SUFFICIENT_INPUT
```

일반적인 프로젝트 Work의 **기본 입력은 `프로젝트명 + 공용 작업지시문`만**이다.

사용자가 별도 Goal을 주는 것은 특정 작업을 명시적으로 우선하고 싶을 때의 선택 사항이지, 정상적인 Work 시작 조건이 아니다.

Goal이 별도로 없으면 Work가 current Project canon을 fresh-read해 다음 순서로 이번 작업 계약을 복원한다.

```text
current stage
→ active / approved current work
→ unresolved blockers and dependencies
→ roadmap / accepted frontier
→ next safe playable slice
→ current work contract
```

- Memory나 과거 채팅에서 임의 Goal을 발명하지 않는다.
- 여러 후보가 있어도 current canon이 한 방향을 명확히 가리키면 별도 질문 없이 그 방향으로 진행한다.
- current canon만으로도 서로 다른 제품 의미를 가진 유효 선택지가 남거나 Core/UX/경제/서사/Art Direction/scope 같은 사용자 결정이 필요할 때만 `USER_DECISION_REQUIRED`로 묻는다.
- 단순히 Goal 문장이 없다는 이유만으로 사용자에게 “무엇을 할까요?”를 다시 묻지 않는다.

## 2. Execution Scope Guard

```text
PROJECT_WORK_ONLY_WHEN_CURRENT_USER_REQUEST_AUTHORIZES_EXECUTION
```

이 bundle은 `진행해`, `계속해`, `남은 작업 진행`, 동일 승인 계약 continuation처럼 실제 실행 의도가 있을 때만 승인 범위의 write/correction/PR closeout을 수행한다.

사용자가 `검토만`, `분석만`, `제안만`, `PR만 열어`, `병합하지 마`, `Notion은 건드리지 마`, `GitHub는 읽기만`처럼 범위를 제한하면 최신 지시가 우선하며 그 범위를 넘어 mutation/merge하지 않는다.

필수 source가 material한데 실제로 읽을 수 없으면:

```text
REQUIRED_SOURCE_UNREADABLE
→ BLOCKED_UNVERIFIED
```

로 처리한다. 검색 snippet, 제목, 과거 Memory, 주변 자료, 추론으로 원문을 대체하지 않는다.

## 3. External Process Skill Trigger

current 환경에서 다음 process skill 또는 동등 절차가 trigger와 맞으면 실제로 실행한다.

```text
creative/design/architecture change
→ brainstorming/design exploration

approved multi-step implementation plan
→ writing-plans 또는 current equivalent

code/policy/contract change
→ RED → GREEN TDD

material failure
→ systematic debugging / root-cause isolation

completion claim
→ verification-before-completion / current Base validation owner
```

외부 process skill은 Project/Base canon 또는 사용자 Decision authority가 아니다. 읽은 Skill과 실제 실행한 Skill을 구분한다.

## 4. Toolchain Freshness — Engine Baseline Exception

`STABLE_ENGINE_BASELINE`은 모든 dependency를 영원히 업데이트하지 않는다는 뜻이 아니다.

현재 작업 계약이 실제로 사용하는 engine 외 tool/addon/plugin/SDK/CLI/dependency의 freshness가 material하면:

```text
installed exact identity
→ official upstream source
→ release/changelog/security/compatibility diff
→ current project consumer
→ update need classification
→ rollback
→ bounded canary when risk exists
→ apply only when current Base/project policy permits
→ exact version/readback
→ focused regression
```

을 사용한다.

그러나 **Engine 자체는** 새 release 존재만으로 production baseline을 자동 승격하지 않고 `STABLE_ENGINE_BASELINE + concrete trigger + CANARY_BEFORE_ENGINE_BASELINE_PROMOTION`이 우선한다.

floating `latest`, unreviewed update, 신규 비용·권한·breaking migration은 자동 채택하지 않는다.

## 5. Local Godot / Fresh Shell Compatibility

사용자 로컬 Windows/Godot 실행·검증이 acceptance에 실제 필요할 때만 current Base의 Fresh Shell/P06/HiGodot owner를 progressive-load한다.

```text
LOCATION: exact repository/worktree/project
→ git dirty/diverged/preflight
→ fetch / safe reconciliation when applicable
→ required exact tool/version identity
→ exact Editor/project/session identity
→ authoring/runtime/validation action
→ VERIFY
→ RESULT
```

- dirty/diverged 상태를 force/reset/clean으로 덮지 않는다.
- 다른 프로젝트 Editor/session을 process 존재만 보고 재사용하지 않는다.
- 프로젝트가 HiGodot/GUT/Hera를 채택했다면 current adoption authority를 따른다.
- shared exact engine/tool pin 또는 session isolation 상세는 current P06/HiGodot owner가 소유한다.
- 프로젝트마다 Godot binary/port를 이유 없이 증식시키지 않는다.
- Fresh PowerShell은 local Codex launcher가 아니다.
- 로컬 접근이 없으면 `NOT_RUN / BLOCKED_NO_LOCAL_ACCESS`를 유지한다.

## 6. Retired / Migration-only Surfaces

current Project/Base가 다시 채택하지 않는 한 다음을 새 기본 authority로 되살리지 않는다.

```text
Google Sheets → COMPATIBILITY_ONLY migration source
Figma project workspace → retired/non-authoritative unless explicitly re-adopted
external HTML project dashboard/workspace → retired/non-authoritative unless explicitly re-adopted
legacy Tool Hub / QA Evidence Studio default project-management route → not default unless current Base explicitly reactivates it
local Codex launcher → retired
```

UNIQUE 정보가 남은 legacy surface만 current owner로 이관하고 destination readback 후 active reference 0을 확인한다.

## 7. Work Prompt Efficiency

```text
WORK_PROMPT_EFFICIENCY_WITHOUT_CAPABILITY_LOSS
```

이 bundle은 안전·품질 capability를 보존하기 위한 shared stable prefix다. 매 응답마다 전체 문서를 다시 출력하거나 모든 Gate를 무조건 반복하지 않는다.

```text
stable shared instruction
→ current work contract
→ current Project fresh facts
→ triggered Skill/owner only
→ current Stage
→ evidence/checkpoint
```

- 같은 evidence를 새 근거 없이 반복 검증하지 않는다.
- 이미 닫힌 Stage를 매번 처음부터 다시 수행하지 않는다.
- scope/authority/new evidence가 바뀌면 필요한 Gate만 재진입한다.
- prompt 길이를 줄이기 위해 safety/authority/evidence boundary를 삭제하지 않는다.

## 8. Bundle completion

다음 두 파일이 함께 discoverable해야 v4.9 Work bundle이 완전하다.

```text
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
```

사용자에게 전달하는 다운로드용 단일 파일은 본체 뒤에 이 appendix 내용을 합쳐 제공할 수 있다.

## 9. Explicit Delegated Minimum-Transition Profile

```text
EXPLICIT_USER_DELEGATION_REQUIRED
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
```

현재 사용자가 routine 권장안 자동 승인, 중간 승인·중단 최소화, Work에서 실제 인게임 production input 일괄 준비, Codex 단일 구현 구간, machine QA 우선, Human QA 후속 보류를 명시한 경우 다음 opt-in profile을 함께 사용한다.

```text
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
```

이 profile은 다음 3단계를 current Slice 범위에서 연결한다.

```text
Work planning/review/visual/audio/data preparation
→ one consolidated Codex product implementation and machine-QA window
→ Work final evidence/canon/merge review
→ user vertical-slice validation
```

활성화 증거가 없으면 기본 v4.9 execution, 기존 image conversation approval, current Project user-decision Gate를 그대로 유지한다. 사용자가 더 좁은 제한을 주면 최신 제한이 profile보다 우선한다.

이 profile은 current owner를 복제하지 않고 Work v4.9, continuous-work, GPT–Codex workflow, Visual, Vertical Slice, HiGodot/GUT/Hera 계약을 조합한다. Project canon·Base latest owner·상위 host/system/tool confirmation이 충돌 시 우선하며, direct main·force·admin/ruleset bypass 또는 Human/Player evidence 과장을 허용하지 않는다.

## 10. Explicit Automatic Git·Godot·Local-Control Addendum

현재 사용자가 작업 중 Git fetch·안전한 pull, 정확한 프로젝트의 Godot 자동 실행, 현재 Slice에 필요한 프로젝트 한정 컴퓨터 조작을 명시적으로 위임한 경우 다음 addendum을 minimum-transition profile과 함께 사용한다.

```text
templates/project-operations/WORK_CODEX_AUTOMATIC_GIT_GODOT_LOCAL_EXECUTION_ADDENDUM.md
```

```text
AUTOMATIC_GIT_FETCH_AUTHORIZED
AUTOMATIC_SAFE_PULL_AUTHORIZED
AUTOMATIC_GODOT_LAUNCH_AUTHORIZED
PROJECT_SCOPED_COMPUTER_CONTROL_AUTHORIZED
```

이 위임은 무조건적인 desktop 권한이나 blind Git integration이 아니다.

- fetch는 exact repository·remote 확인 뒤 자동 수행한다.
- pull은 clean tracking branch·correct upstream·fast-forward-only 조건에서만 자동 수행한다.
- dirty·ahead·diverged·detached·wrong-worktree 상태는 stash/reset/clean/rebase/force로 덮지 않는다.
- local worktree가 없으면 GitHub connector로 remote facts를 fresh-read하고 local pull을 수행했다고 주장하지 않는다.
- Godot과 컴퓨터 조작은 exact current Project·current Slice·callable tool에 한정한다.
- semantic CLI/API/MCP/element control을 좌표 클릭보다 우선한다.
- unrelated app/file/process/session, credential, account, OS/security setting, purchase, public release는 보호한다.
- 상위 host/tool confirmation과 current Git/Godot owner가 항상 우선한다.
