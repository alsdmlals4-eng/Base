# GPT–Codex 역할 분리 · Codex Consumer Migration Packet

## 실행 상태

```yaml
mode: CODEX_IMPLEMENTATION_HANDOFF
pr: 674
branch: workflow/gpt-codex-role-split-20260825
latest_main_reconciled: 6f8ca83efbb34862bd8cdceb38321090734a57ba
latest_observed_head_before_packet: c322deab6a8598cb2f691f5aa843fb7519bf5627
work_instruction_revision: DEFERRED_NOT_CURRENT_CANON
planning_review_owner: GPT_PLANNING_REVIEW_VISUAL_OWNER
implementation_owner: CODEX_IMPLEMENTATION_EXECUTOR
image_generation_by_codex: FORBIDDEN
other_open_prs: READ_ONLY
clean_review_exit: false
```

이 packet은 새 기획을 만들기 위한 문서가 아니다. GPT가 확정·검수한 역할 계약을 **tests / Registry / generated derivatives / machine consumers / secondary active consumers**에 기계적으로 migration하고 실제 검증하는 Codex BUILD 작업이다.

## 먼저 읽기

1. `AGENTS.md`
2. `START_HERE.md`
3. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
4. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
5. `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
6. `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
7. `skills/maintaining-project-context-and-handoff/SKILL.md`
8. `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
9. `templates/custom-instructions.codex.md`
10. `docs/handoffs/2026-08-25-gpt-codex-role-split-resume-checkpoint.md`
11. PR #674 current diff + current GitHub Actions
12. relevant Notion current canon: Base Home / P01 / P03 / P05 / P06 / P07 / P08

`CODEX_REHYDRATE_GITHUB_AND_NOTION`을 통과한 뒤에만 persistent mutation한다.

## 현재 승인된 역할 계약

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
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
CODEX_PREFLIGHT_OPTIONAL
CONTINUOUS_WORK_EXECUTOR_HANDOFF
DEFERRED_EXTERNAL_EXECUTOR
```

해석:

- planning/research/adversarial review/Visual/spec/final review = GPT
- actual code/data/Scene/Resource/config/test/build/runtime implementation = Codex
- planning-only에는 Codex를 강제하지 않음
- implementation이 존재하면 Codex BUILD를 생략하지 않음
- Codex는 GitHub + relevant Notion을 구현 전에 fresh-read
- Codex는 이미지 생성/생성형 편집 금지
- current-use 승인 + Notion attach/readback Visual만 소비
- missing visual = `GPT_VISUAL_REQUEST`

## CI baseline · GPT-owned correction 뒤 측정

### `c59fa9b182e4f096ad935da65c827958043adb76`

PASS:

- Validate Skill Routing Precision
- Validate Evidence-Based Game Development Knowledge
- Validate Base Partition Contract
- whitespace validation
- required-check topology
- generated-artifact/integrity-topology step

FAIL:

- Validate One-Shot Local Executor Bootstrap
- Validate Base v9 Operating Contracts
- Validate Game Project Operating System

Lightweight diagnostics:

```text
Ran 137 tests
FAILED: 5
```

Whole core diagnostics:

```text
Ran 2151 tests
FAILED: 13
SKIPPED: 37
```

### `c322deab6a8598cb2f691f5aa843fb7519bf5627`

GPT가 발견한 실제 파일 오염 `templates/custom-instructions.codex.md = P08 Context Pack`을 stable Codex bootstrap template으로 복원한 exact head다.

현재 관측:

- Base Partition: PASS
- Skill Routing: PASS
- Evidence-Based Game Development Knowledge: PASS
- One-Shot Local Executor: FAIL
- Base v9 / Game Project OS: running or follow-up evidence required at packet 작성 시점

최종 작업에서는 이 값들을 재사용하지 말고 current head에서 다시 실행/조회한다.

## 13개 core failure 분류

### A. 실제 MUST_PRESERVE / MUST_FIX — test를 삭제하면 안 됨

#### A1. Codex custom-instructions stable bootstrap

발견:

`templates/custom-instructions.codex.md`가 P08 Context Pack 내용으로 잘못 덮여 있었다.

GPT가 이미 교정:

- `stable bootstrap`
- `DOMAIN_SPLIT_CANON`
- `AGENTS.md`
- `START_HERE.md`
- `Active Context`
- `NOTION_HUMAN_FACING_CANON`
- `REPOSITORY_STRUCTURED_CANON`
- `REPOSITORY_RUNTIME_TRUTH`
- current session / actual evidence
- GitHub + Notion rehydration
- Codex image generation 금지
- execution environment freshness

Codex는 이 템플릿을 P08 Context Pack으로 다시 바꾸지 않는다.

#### A2. 경량 중립성 Gate 의미 보존

`tests/test_neutral_adversarial_feature_lifecycle.py`가 다음 실제 capability 퇴행을 검출했다.

반드시 `docs/WORK_MODE_AND_SKILL_ROUTING.md`에 현재 역할 구조와 양립하는 형태로 복원한다.

```text
동의 편향
반대를 위한 반대
```

의미:
- 중립 Gate는 무비판 동의를 막지만 반대를 위한 반대를 요구하지 않는다.

#### A3. 균형 평가 do-not-use 경계 보존

복원할 의미/contract:

```text
결정·권장안이 없는 설명형 칭찬·균형 요약
PLAN 사전판정
`refine-approved-findings`에서 분야 Skill BUILD로 한 번만 구현·수정
regression-recheck → decision-report
```

새 역할 적용:
- PLAN/REVIEW finding owner = GPT
- finding이 제품 implementation을 요구하면 분야 Skill BUILD 실행자는 Codex
- 이미 구현된 finding을 다시 중복 수정하지 않음

#### A4. 연속작업의 단일 최소 안전 finding 처리

복원할 의미:

```text
기술적 단일 최소 안전 finding이면 자동 승인
```

단 새 역할에서 “자동 승인”은 **사용자 새 기획 결정이 필요 없는 승인 범위 내 기술 finding을 구현 queue에 넣을 수 있다**는 뜻이다.

```text
GPT REVIEW finding validation
→ approved scope의 기술적 단일 최소 안전 finding
→ Codex BUILD minimal fix
→ regression-recheck
→ GPT whole-state review
```

GPT가 제품 코드를 직접 수정한다는 의미로 복원하지 않는다.

### B. SAFE CAPABILITY MIGRATION — old ownership literal은 교체, 안전성은 강화 보존

#### B1. One-Shot Local Executor

현재 old test는 다음을 GPT workflow policy에 직접 요구한다.

```text
ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY
one copy/paste
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
ASSUME_PREVIOUS_POWERSHELL_CLOSED
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
```

새 역할에서 **GPT가 PowerShell/local Codex launcher를 직접 제공하는 default path는 폐기**한다.

그러나 다음 안전 capability는 삭제 금지:

- exact project/worktree identity
- fresh shell/session assumptions
- wrong-target/profile/process collision 방지
- stale PID/editor/MCP session 금지
- project/session/version/readiness fresh probe
- capability discovery before literal rejection
- diagnostic preservation
- destructive reset/restore/clean 금지
- unrelated process/worktree 보호
- adopted persistent authoring authority 준수

migration target:

```text
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
+ Godot live-editor/runtime owner의 current safety contract
+ focused regression test
```

old “GPT one copy/paste launcher 제공”을 새 current requirement로 되살리지 않는다.

### C. STALE TEST / CONSUMER EXPECTATION — 새 contract로 교체

다음 assertion은 current ownership과 충돌하므로 새 regression으로 migration한다.

#### C1. `OPTIONAL_CODEX_EXECUTOR`

현재 implementation BUILD ownership에서는 폐기.

대체:

```text
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_IMPLEMENTATION_EXECUTOR
CODEX_PREFLIGHT_OPTIONAL
```

optional인 것은 **planning-only에서 Codex 실행** 및 별도 technical Plan이지, implementation owner가 아니다.

#### C2. `GPT_GODOT_PREPRODUCTION_ALLOWED` / `기획·구현·POC 누적`

current active behavior에서 폐기.

negative regression:
- GPT가 제품 code/Godot POC를 기본 BUILD owner로 누적하지 않음.

#### C3. `godot_runtime_files_only`

과거 Codex package 제한을 current universal rule로 유지하지 않는다.

Codex는 승인 package에 필요한:

```text
code/data/Scene/Resource/config/test/build/runtime
+ 구현에 필요한 structured implementation docs
```

를 수정할 수 있다.

기획 의미 변경은 `CHANGE_PROPOSAL`로 반환한다.

#### C4. literal compatibility 문구

현재 실패 예:

```text
현재 ChatGPT 세션
명시적 승인이 완료된 항목
실제 저장소·프로젝트·Godot 상태
```

문구 자체보다 semantic assertion으로 바꾼다.

대체 의미:

- current execution surface에 executor가 없으면 실행했다고 주장하지 않음
- explicit user approval scope는 추가 재승인 없이 merge authority를 상속
- Codex는 actual GitHub + Notion + actual project/runtime state를 fresh-read

#### C5. Workspace planning_owner old value

old:

```text
planning_owner = GPT_FIRST_PLANNING_AND_REVIEW
codex_role = OPTIONAL_CODEX_EXECUTOR
```

current:

```text
planning_owner = GPT_PLANNING_REVIEW_VISUAL_OWNER
codex_role = CODEX_IMPLEMENTATION_EXECUTOR
```

`schema_version: 3`, `cross_domain_sync: SYNC_BEFORE_IMPLEMENTATION`는 compatibility 때문에 유지한다.

#### C6. old machine token

```text
REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF
```

이 token이 “GPT가 tool이 있으면 제품 BUILD도 직접 한다”는 old semantics를 요구하면 current contract로 migration한다.

대체 의미:

```text
GPT_TOOL_EVIDENCE_DOES_NOT_TRANSFER_BUILD_OWNERSHIP
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
```

## 현재 active secondary consumer inventory

fresh search에서 old `OPTIONAL_CODEX_EXECUTOR`가 current-main에 남아 있는 후보:

### active/migration candidate

- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- `skills/orchestrating-deepseek-worktrees/SKILL.md`
- `templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md`
- machine Manifest / Registry consumers

### already GPT-corrected on #674

- `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md` — 단, A2~A4 의미 복원 필요
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`
- `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- Handoff Skill/reference
- `templates/custom-instructions.codex.md`

### historical evidence — current instruction으로 오인되지 않으면 보존

예:
- `docs/evidence/2026-08-19-gpt-first-clean-review-workflow.md`
- 날짜/SHA/당시 PR 상태를 설명하는 historical snapshot

## Codex 수정 대상

최소:

```text
tests/test_gpt_codex_workflow_contract.py
tests/test_one_shot_local_executor_bootstrap_contract.py
tests/test_neutral_adversarial_feature_lifecycle.py  # test 의미 보존, routing doc을 맞춤
tests/test_ai_bootstrap_drift_contract.py            # stable bootstrap 재검증
tests/test_base_long_horizon_work_contract.py
tests/test_deliberate_work_routing_recovery.py
tests/test_pr530_selective_integration_contract.py
tests/test_p08_ai_operations_contract.py
skills/SKILL_REGISTRY.json
docs/generated/BASE_ACTIVE_SKILLS.md
docs/operations/BASE_PARTITION_MANIFEST.json
relevant generated/checker consumers
```

그리고 fresh search 결과에서 current active conflict로 판정된 문서/Skill/prompt만 최소 교정한다.

## TDD / verification 요구

1. 현재 exact head에서 failing tests를 재현한다.
2. stale test는 삭제하는 대신 새 역할 contract assertion으로 먼저 교체해 RED를 확인한다.
3. A2~A4와 B1처럼 보존해야 할 capability는 source 문서를 current 역할에 맞게 수정해 GREEN으로 만든다.
4. Registry를 source-of-truth로 수정하고 generated derivative를 정식 생성 경로로 재생성한다.
5. canonical-reference freshness를 실행한다.
6. focused role tests → Base v9 → Game Project OS → maximal available core regression 순으로 실행한다.
7. actual failing/not-run/skipped를 숨기지 않는다.

## 최소 새 regression

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
APPROVED_ITEM_INHERITS_MERGE_AUTHORITY
CONTINUOUS_WORK_EXECUTOR_HANDOFF
DEFERRED_EXTERNAL_EXECUTOR
```

negative regression:

```text
GPT product-code BUILD ownership must not return
Codex implementation must not be optional when implementation exists
Codex image generation/editing must not appear
unapproved visual substitution must not appear
GPT default PowerShell/local-Codex orchestration must not return
```

## Open PR / concurrency

- PR #674 = current authorized workstream
- 다른 independent open/draft/ready PR = read-only
- 특히 #660은 명시적 허가 없이는 수정/흡수/종료/병합 금지
- current main의 merged change는 reconciliation 가능
- force push / history rewrite / ruleset bypass 금지

## Visual policy

이 consumer migration은 이미지 제작이 필요 없다.

Codex가 어떤 이유로 새 이미지가 필요하다고 판단하면 직접 생성하지 말고 `GPT_VISUAL_REQUEST`를 반환한다.

## 완료 기준

```yaml
required:
  current_main_reconciled: true
  active_old_role_conflicts: 0
  actual_non_regression_findings_fixed: true
  stable_codex_bootstrap: true
  registry_generated_sync: PASS
  canonical_reference_freshness: PASS
  focused_role_tests: PASS
  base_v9: PASS
  game_project_os: PASS
  maximal_core_regression: PASS_OR_EXPLAINED_UNRELATED_NOT_RUN
  adversarial_full_loops_minimum: 5
  clean_review_exit: true
  other_open_prs_untouched: true
```

완료 뒤 exact head, changed files, tests, remaining risks를 GPT 검수로 반환한다. PR을 Ready/merge로 올리는 판단은 그 fresh evidence 뒤에만 한다.
