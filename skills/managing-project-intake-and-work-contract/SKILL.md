---
name: managing-project-intake-and-work-contract
description: Use when routing a project request, closing material ambiguity, defining a work contract, or sequencing approved dependent work.
---

# Managing Project Intake and Work Contracts

## Core principle

요청 접수는 `의도 파악 → Work Mode 자동 선택 → Skill 자동 선택 → 사실 조사 → GitHub+Notion baseline 복원 → first-prompt 방향 고정 → 실행 계약 → Grill Me 정합성 확인 → 필요 시 작업 분해·순서화 → 실행 보고`인 하나의 상태 흐름이다.

사용자는 Skill 이름이나 mode를 선언할 필요가 없다. Registry trigger와 현재 작업 단계로 필요한 최소 Skill·Skill Mode를 자동 선택하고, 실제 사용 이유와 결과를 최종 보고에 남긴다.

L1 이상 지시문은 `first-prompt → contract → clarify` 순서를 기본으로 하며 `Grill Me alignment gate`로 의도·기획·범위를 닫는다. `exact contract already approved`이고 유효한 `approval reference`가 있으면 같은 결정을 다시 묻지 않는다.

프로젝트 기본 권위는 다음과 같이 읽는다.

```text
latest user decision
→ project AGENTS / security / engine / data rules
→ current_confirmed_decisions
→ GitHub latest main / actual code-data-scene-resource-test
→ exact project_notion_home and filtered human-facing surfaces
→ current approved work contract
→ adopted Base contracts
```

Google Sheets는 normal intake input이 아니다. legacy Sheet가 현재 승인된 migration scope의 고유 미이관 자료라는 증거가 있을 때만 `legacy_migration_source`로 읽고 `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`를 적용한다.

## GPT-first responsibility

`GPT_PRIMARY_PLANNING_REVIEW`가 기본이다. 이 Skill은 GPT가 기획·조사·대안 비교·UI/UX·아트 방향·시각 후보·최종 검수를 수행할 수 있게 작업 계약을 만든다.

`CODEX_OPTIONAL_SUB_EXECUTOR`는 실제 repository/engine mutation, 다수 파일 구현, build/runtime reproduction이 필요할 때만 handoff한다. “작업이면 무조건 Codex”로 라우팅하지 않는다.

시각이 material하면 `NOTION_VISUAL_CHECKPOINT_BEFORE_POC → UX_UI_REPRESENTATIVE_STATE_REQUIRED → APPROVED_VISUALS_FEED_POC`를 계약에 포함한다.

## Continuous work and workstream isolation

사용자가 `[연속작업] 진행해`라고 명시하면 `references/continuous-work-execution.md`를 적용한다.

```text
CONTINUOUS_WORK_ACTIVE
→ ready task
→ BUILD
→ REVIEW
→ verified minimal fix
→ regression
→ blocker recovery
→ next independent ready task
```

이는 `PLAN / BUILD / REVIEW`를 대체하지 않는다. `USER_DECISION_REQUIRED`, 결제, 계정·보안 권한 확대, 파괴적 migration은 자동 승인하지 않는다.

다른 채팅/독립 workstream은 기본 `DO NOT TOUCH`다. `same-goal` PR이 보여도 read-only overlap evidence로만 확인하고 owner branch를 modify/rebase/update/close/merge하지 않는다. 명시적 현재-workstream 흡수 승인이 없으면 별도 branch/PR을 유지한다.

`USER_DIRECTED_PARALLEL_PR`, `SAME_GOAL / PATH_OVERLAP / SEMANTIC_OVERLAP`, `PROVISIONAL_INTEGRATION`, `absorbed_owner_deltas`, `residual_owner_deltas`, `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`은 기존 concurrent protocol의 compatibility terms다.

## Existing Solution First

새 MCP·addon·CLI·framework·Skill·Mode·공용 실행 계층 요청은 일반 설계보다 먼저 current environment와 기존 대안을 조사한다.

```text
inventory-current-environment
→ existing_solution_disposition
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
```

`existing_solution_disposition`, 비교 증거, 사용자 승인 없이 `BUILD_NEW`를 계약으로 만들지 않는다.

## Terminology

- `Work Mode`: `PLAN / BUILD / REVIEW` 중 현재 주 자세·권한·증거 기준.
- `Skill`: 특정 책임을 수행하는 재사용 가능한 작업 계약.
- `Skill Mode`: 한 Skill의 조건부 절차.
- `Prompt`: 사용자의 현재 목표·제약·산출물.
- `Direction anchor`: 지시문 앞에서 핵심 행동·결과·지배 기준을 고정하는 짧은 방향 문장.
- `Continuous Work`: 명시적 trigger가 있을 때만 활성화되는 orchestration flag.
- `Project Notion`: `NOTION_HUMAN_FACING_CANON`을 가진 exact Project workspace surface.

상세 Work Mode 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

승인 결정 복원·중복 질문 방지·GitHub/Notion 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

프로젝트 기본 생명주기: `docs/GPT_FIRST_PROJECT_WORKFLOW.md`

폐기 surface migration: `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`

## Skill Modes

- `route`: 요청 의도·단계·위험을 파악하고 Work Mode, 작업 수준, 주 책임 분야와 최소 Skill 집합을 자동 판정한다.
- `first-prompt`: 핵심 방향 문장을 앞에 두고 Task·Context·Source·Constraints·Output·Validation을 구조화한다.
- `contract`: 목표·배경·사용자/플레이어 경험·범위·제외·보호·산출물·완료·검증·rollback이 있는 실행 계약으로 변환한다.
- `clarify`: GitHub/Notion/정본에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성만 한 번에 하나씩 닫는다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·gate·rollback 순서를 정한다.
- `execution-report`: 실제 사용한 Work Mode·Skill·Mode, 변경, 증거, 미검증, 사용자 학습 정보를 보고한다.

L1 이상 기본 순서는 `route → first-prompt → contract → clarify`다. 승인 후에만 `decompose-and-sequence`를 실행한다.

## First-prompt completeness

`first-prompt`는 다음 토큰을 책임진다.

```text
DIRECTION_ANCHOR
TASK_AND_SUCCESS
CONTEXT_AND_SOURCES
CONSTRAINTS_AND_PROTECTED_SCOPE
OUTPUT_AND_VALIDATION
```

Direction anchor는 상위 권한을 만들지 않는다. 최신 사용자 결정·정본·`HARD_CONSTRAINT`와 충돌하면 후자가 우선한다.

## Grill Me alignment gate

- 중요한 결정을 한 번에 하나씩 질문한다: **한 번에 하나**.
- 이미 승인된 결정을 표현만 바꿔 재질문하지 않는다.
- 사용자가 “모두 권장안대로” 승인하면 승인된 bundle 범위의 권장안을 기록하되 새 범위를 자동 추가하지 않는다.
- 기술 세부·가역적 초기값은 `RECOMMENDED_DEFAULT`.
- core/player experience/major UX/story/cost/scope conflict는 `USER_DECISION_REQUIRED`.

Reference: `references/grill-me-protocol.md`

## Work Mode selection

### PLAN
- 요구·근거·설계·정본·작업 순서를 확정한다.
- 읽기·조사·제안이 기본이다.

### BUILD
- 승인된 계약 범위의 코드·데이터·문서·자산을 구현한다.
- 단계별 검증과 rollback을 유지한다.

### REVIEW
- 결과를 적대적으로 검토하고 반례·회귀·증거를 찾는다.
- 수정 finding이 승인 범위 안이면 BUILD로 전환해 최소 수정 후 REVIEW로 재검증한다.

## Automatic selection policy

- Registry trigger와 `do_not_use_when`으로 최소 Skill만 선택한다.
- 주 책임 분야 Skill은 하나를 우선한다.
- 사용자에게 Skill 선택을 전가하지 않는다.
- 새 실패·정본 변경·범위 변경이 생기면 라우팅을 다시 계산한다.
- Skill 파일을 읽은 것과 실제 Skill 절차 실행을 구분한다.
- GPT/Codex/외부 AI용 작업 지시문도 `first-prompt → contract → clarify`를 거친다.
- Codex는 필요할 때만 선택한다.

## Required inputs

```yaml
request:
project_agents:
project_start_here:
active_context:
current_confirmed_decisions:
project_notion_home:
project_notion_surfaces: []
related_open_and_recent_prs:
documentation_map:
design_document_registry:
skill_registry:
current_stage_and_gate:
current_issue_or_approved_request:
actual_code_data_assets_tests:
approved_visual_inputs: []
legacy_migration_sources: []
delivery_constraints:
known_dependencies_and_blockers:
available_people_tools_permissions:
validation_environment:
rollback_constraints:
approval_reference:
continuous_work_trigger:
continuous_work_state: CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE
existing_solution_inventory:
existing_solution_disposition:
existing_solution_evidence:
existing_solution_user_approval:
```

## Read first

1. 최신 사용자 지시.
2. project `AGENTS.md`, START_HERE, Active Context, Documentation Map.
3. `CURRENT_CONFIRMED_DECISIONS.md`, related_open_and_recent_prs.
4. GitHub latest main과 actual code/data/Scene/Resource/assets/tests.
5. exact `project_notion_home`과 current task에 필요한 filtered surfaces.
6. `docs/GPT_FIRST_PROJECT_WORKFLOW.md`와 `docs/WORK_MODE_AND_SKILL_ROUTING.md`.
7. `SKILL_REGISTRY.json`과 current primary Skill.
8. migration scope일 때만 legacy Sheet/local/HTML source.
9. L1 prompt면 `references/first-prompt-direction-anchoring.md`.
10. 필요 시 `references/grill-me-protocol.md`, `references/continuous-work-execution.md`, `references/work-decomposition-and-sequencing.md`.

## Work decomposition

승인된 일을 결과 단위로 나누고 관계를 다음으로 표시한다.

```text
BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES
```

같은 semantic resource를 쓰는 작업은 독립 파일이어도 무분별하게 병렬화하지 않는다.

```yaml
work_item:
  goal:
  output:
  dependencies: []
  shared_resources: []
  acceptance_criteria: []
  validation: []
  rollback:
```

## Visual / PoC contract

이미지·UI·UX가 플레이 판단에 영향을 주면:

```text
representative states
→ GPT visual + UX review
→ exact Project Notion attach
→ destination readback
→ user approval
→ approved visual/provenance
→ PoC/demo implementation
→ runtime evidence
```

Notion preview는 runtime proof가 아니다.

## Optional Codex handoff

Codex가 필요하면 `ONE_SHOT_CODEX_HANDOFF_WHEN_NEEDED`로 fresh PowerShell용 한 번 붙여넣기 block과 complete contract를 만든다.

Codex contract에는 최소:

```yaml
project_identity:
github_repository:
project_notion_home:
approved_goal:
player_or_user_experience:
important_rules: []
important_skills: []
module_map: []
approved_visual_inputs: []
repository_paths_to_read: []
notion_records_to_read: []
protected_behavior_and_data_contracts: []
implementation_scope: []
acceptance_criteria: []
required_tests: []
runtime_checks: []
forbidden_changes: []
rollback: []
```

Codex 결과는 GPT final review로 돌아온다.

## Completion contract

L1 이상 결과는 `USER_LEARNING_COMPLETION_REPORT`를 포함한다.

- 작업/파트의 역할.
- 핵심 규칙과 canonical owner.
- 핵심 Skill·Mode와 경계.
- 핵심 모듈: 역할·입력·출력·연결.
- 변경 전 / 변경 후.
- 유지 / 개선 / 흡수 / 제거 / 의도적 미추가.
- 사용자/플레이어 효과와 장기 효과.
- trade-off와 revisit conditions.
- actual tests/runtime/Notion readback/PR/main SHA.
- unverified / risks / blockers / rollback.

## Failure states

```text
AWAITING_USER_CONFIRMATION
DUPLICATE_WORK
DUPLICATE_QUESTION
CANON_CONFLICT
IMPLEMENTATION_CONFLICT
MISSING_SYNC
MIGRATION_PENDING
BLOCKED_UNVERIFIED
USER_DECISION_REQUIRED
COST_GATE_BLOCKED
```

retired local/HTML/Sheet surface가 current authority로 필요하다고 결론 내리기 전에 `DEPRECATED_SURFACE_ABSORB_THEN_DELETE`와 Existing Solution First를 다시 적용한다.
