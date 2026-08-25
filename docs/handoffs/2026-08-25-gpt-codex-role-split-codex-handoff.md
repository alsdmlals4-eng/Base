# 2026-08-25 GPT–Codex 역할 분리 · Codex 구현 인계

## 상태

```yaml
handoff_mode: CODEX_IMPLEMENTATION_HANDOFF
branch: workflow/gpt-codex-role-split-20260825
base_main_observed: 31e13c7142695f57a5b7b29102307d1d2c02efac
planning_owner: GPT_PLANNING_REVIEW_VISUAL_OWNER
implementation_owner: CODEX_IMPLEMENTATION_EXECUTOR
other_open_prs: READ_ONLY
protected_open_pr: 660
```

이 Branch에서 GPT 책임 범위인 공용 정책·라우팅·Notion/작업지시문 설계를 교정했다. **코드·테스트·machine registry/generated consumer 교정은 새 역할 계약에 따라 Codex가 이어받는다.**

## 먼저 읽기

1. `AGENTS.md`
2. `START_HERE.md`
3. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
4. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
5. `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
6. `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`
7. `templates/custom-instructions.codex.md`
8. `skills/maintaining-project-context-and-handoff/SKILL.md`
9. `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
10. current main / this branch diff / open PR inventory

## 승인된 새 계약

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
CODEX_PREFLIGHT_OPTIONAL
```

핵심 의미:

- GPT는 기획·조사·벤치마킹·적대적 검수·구현 명세·이미지 생성/편집·최종 검수를 맡는다.
- 실제 code/data/Scene/Resource/config/test/build/runtime 구현은 Codex가 맡는다.
- Codex 전환에 별도 사용자 요청은 필요하지 않다. `IMPLEMENTATION_READY + 구현 존재`가 handoff trigger다.
- Codex는 구현 전에 current GitHub + relevant Notion을 fresh-read한다.
- Codex는 이미지 생성·생성형 편집을 하지 않는다.
- Codex는 current-use 승인 + Notion upload/attach/readback가 확인된 Visual만 사용한다.
- 이미지가 없으면 `GPT_VISUAL_REQUEST`; 임의 AI placeholder 생성 금지.
- GPT→PowerShell→local Codex는 기본 workflow에서 폐기한다. shell/CLI/MCP/Godot freshness는 Codex execution environment가 책임진다.

## Codex 구현 범위

### 1. Active consumer inventory

다음 literal/semantic consumer를 repository 전체에서 fresh-search한다.

```text
OPTIONAL_CODEX_EXECUTOR
GPT_GODOT_PREPRODUCTION_ALLOWED
ON_DEMAND_CODEX_HANDOFF
USER_REQUESTED_CODEX_HANDOFF
기획·구현·POC 누적
Godot 구현 보조·POC
ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
PowerShell/Codex/local executor
```

각 occurrence를 다음으로 분류한다.

```yaml
consumer_state:
  - ACTIVE_CONFLICT
  - CURRENT_COMPATIBILITY_ALIAS
  - HISTORICAL_SNAPSHOT
  - TEST_EXPECTATION_TO_MIGRATE
  - GENERATED_DERIVATIVE
```

History는 current instruction처럼 보이지 않는 한 보존한다. Active conflict와 stale test/generated consumer만 교정한다.

### 2. 우선 확인 대상

기존 main search에서 최소 다음 stale consumer 후보가 관측됐다.

- `tests/test_gpt_codex_workflow_contract.py`
- `tests/test_p08_ai_operations_contract.py`
- `tests/test_base_long_horizon_work_contract.py`
- `tests/test_pr530_selective_integration_contract.py`
- `skills/SKILL_REGISTRY.json`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- `docs/operations/BASE_PARTITION_MANIFEST.json`
- `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `skills/orchestrating-deepseek-worktrees/SKILL.md`
- `templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md`

목록은 정본이 아니다. 반드시 fresh search로 complete consumer inventory를 다시 만든다.

### 3. Test/registry migration

현재 tests에는 과거 계약을 PASS 조건으로 요구하는 assertion이 있다. 예:

- `GPT_GODOT_PREPRODUCTION_ALLOWED` 존재 요구
- `기획·구현·POC 누적` 존재 요구
- `USER_REQUESTED_CODEX_HANDOFF`를 정상 기본 전환으로 가정
- `OPTIONAL_CODEX_EXECUTOR`를 active machine contract로 요구

이를 새 계약에 맞는 regression tests로 교체한다.

최소 새 assertion:

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
CODEX_PREFLIGHT_OPTIONAL
```

negative assertions에는 다음 active behavior 재등장을 막는 항목을 포함한다.

```text
GPT_GODOT_PREPRODUCTION_ALLOWED
GPT가 제품 코드/POC를 기본 구현
구현 handoff가 USER_REQUESTED_CODEX_HANDOFF에만 의존
Codex가 이미지 생성/생성형 편집
승인되지 않은 Visual을 임의 사용
GPT가 PowerShell local Codex launcher를 기본 프로젝트 경로로 소유
```

Skill Registry에서 handoff trigger/mode를 `IMPLEMENTATION_READY` / `CODEX_IMPLEMENTATION_HANDOFF` 중심으로 migration하고 `USER_REQUESTED_CODEX_HANDOFF`는 필요하다면 compatibility alias로만 유지한다. generated skill index는 source registry에서 재생성한다.

### 4. Secondary active docs

`OPTIONAL_CODEX_EXECUTOR`의 과거 의미가 active current instruction으로 남은 secondary docs는 canonical policy로 맞춘다.

중요 의미:

- planning-only: Codex optional/not required
- implementation exists: Codex implementation executor required
- optional인 것은 별도 `CODEX_PREFLIGHT_OPTIONAL` technical Plan이지 Build ownership이 아님

Long-horizon/failure recovery에서 “현재 세션 tool로 실행할 수 있으면 GPT가 직접 구현한다”는 옛 의미가 남아 있으면 새 역할 경계와 충돌하지 않게 재작성한다. GPT의 connected read/write는 기획·Notion·정본·검수 작업에는 사용할 수 있지만 제품 code/runtime BUILD owner는 Codex다.

### 5. Image policy regression

기존 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`의 사용자 승인·한 결과·Notion delivery/readback·rights/provenance Gate는 약화하지 않는다.

새 역할과 연결되는 regression을 추가한다.

```text
Codex image generation/editing forbidden
→ current-use approved Notion visual required
→ missing visual = GPT_VISUAL_REQUEST
→ GPT conversation approval gate
→ GPT image production/review
→ Notion approved upload/attach/readback
→ Codex fresh-read/resume
```

### 6. Open PR protection

Open PR #660 및 다른 독립 open/draft/ready PR의 branch/file changes를 수정·흡수·종료·병합하지 않는다. 현재 Branch와 semantic conflict가 있으면 `CROSS_WORKSTREAM_CONFLICT`로 보고하고 현재 Branch 안에서 안전하게 해결 가능한 부분만 진행한다.

## 필수 적대적 체크포인트

최소 5회 whole-state loop를 새 current state에 대해 수행한다.

1. **Role ownership loop** — GPT가 구현 owner로 돌아가는 경로 / Codex Build가 optional로 빠지는 경로 공격.
2. **Canon rehydration loop** — GitHub만 읽고 Notion을 놓치거나 stale handoff를 current truth로 쓰는 경로 공격.
3. **Visual loop** — Codex 이미지 생성, 임의 placeholder, Notion 미승인 Visual, missing visual deadlock 공격.
4. **Non-regression loop** — 기존 벤치마킹·IRG·TDD·runtime/play evidence·open PR 보호·rollback·merge gate 약화 공격.
5. **Consumer/test loop** — active docs/registry/generated/test에 옛 literal/semantic contract가 남는지 전체 검색.

finding이 생기면 수정 후 Loop 1부터 current state를 다시 공격한다. 최소 5회 이전에는 clean exit 금지.

## Verification

Codex가 실제 사용 가능한 repository test command를 current Base에서 discovery한 뒤 실행한다. 특정 과거 check 이름을 가정하지 않는다.

최소 evidence:

```yaml
verification:
  stale_consumer_search:
  focused_role_contract_tests:
  registry_generated_sync:
  json_parse:
  markdown_or_doc_contract_checks:
  full_or_maximal_available_suite:
  tests_not_run: []
  branch_diff_vs_current_main:
  open_pr_overlap_check:
```

`NOT_RUN`을 PASS라고 보고하지 않는다.

## 완료 보고

```yaml
codex_result:
  branch:
  baseline_main:
  final_head:
  changed_files_and_reasons: []
  active_conflicts_removed: []
  compatibility_or_history_kept: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  adversarial_loops:
  open_pr_protection:
  remaining_risks: []
  merge_readiness:
```

코드/test/registry consumer migration과 fresh verification까지 닫히기 전에는 이 역할 분리 PR을 `COMPLETE` 또는 merge-ready라고 주장하지 않는다.