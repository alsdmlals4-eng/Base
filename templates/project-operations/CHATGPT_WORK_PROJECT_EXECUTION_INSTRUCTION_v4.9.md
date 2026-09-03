---
contract_name: CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION
contract_version: "4.9"
revision: "2026-08-28-desktop-repository-first"
status: ACTIVE_REPOSITORY_FIRST_SHARED_WORK_EXECUTION_ADAPTER
baseline: PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL
base_repository: https://github.com/alsdmlals4-eng/Base
base_policy: ALWAYS_REFETCH_CURRENT_COMPLETED_MAIN
execution_surface: CHATGPT_WORK
canon_policy: FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER
machine_contract: docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json
human_policy: docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md
---

# GPT Work 프로젝트 총기획·조사·검수·정본화·Codex 인계 통합 작업지시문 v4.9
## DESKTOP GPT · REPOSITORY-FIRST · NOTION-OPTIONAL LEGACY MIGRATION

> 이 파일을 각 ChatGPT Project의 Work 작업에 첨부해서 사용한다.
>
> 기본 입력은 **`프로젝트명 + 이 공용 작업지시문 + 선택적 이번 Goal`**이면 충분하다.
>
> 이 revision부터 프로젝트 repository가 기획·결정·구조화 데이터·승인 runtime asset·코드·Scene·Resource·test·evidence의 단일 active 정본이다. Notion은 고유 자료가 남은 기존 프로젝트의 read-only migration source일 뿐, 신규 기획·승인·Codex handoff의 필수 중간 작업면이 아니다.

---

## 0. 최상위 실행 계약

```text
PROJECT_PLUS_INSTRUCTION_PLUS_OPTIONAL_GOAL_IS_SUFFICIENT_INPUT
WORK_SELF_STARTING_FRESH_READ_BOOTSTRAP
FRESH_READ_PROJECT_BOOTSTRAP
PAST_CONVERSATION_NOT_REQUIRED
DEFAULT_MEMORY_DISCOVERY_ONLY_NOT_CANON
MEMORY_CONFLICT_CURRENT_PROJECT_CANON_WINS

DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
REPOSITORY_PRIMARY_CANON
APPROVED_HUMAN_BLUEPRINT_PDF_CANON
AI_PRODUCTION_SPEC_MARKDOWN
APPROVED_PDF_IS_HUMAN_VISUAL_CANON
CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
NO_NEW_NOTION_WRITE_BY_DEFAULT
NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE

CHAT_QUICK_DISCUSSION_DEFAULT
WORK_LONG_MULTISTEP_NONCODING_DEFAULT
WORK_EXECUTION_SURFACE_NOT_CANON
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA
APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
CODEX_IMAGE_GENERATION_FORBIDDEN

ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE
ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER
STABLE_ENGINE_BASELINE
NO_AUTOMATIC_LATEST_FOLLOW
CANARY_BEFORE_ENGINE_BASELINE_PROMOTION

REUSE_FIRST_PREFLIGHT_REQUIRED
BASE_OWNER_PROGRESSIVE_LOAD
CURRENT_SKILL_REGISTRY_COVERAGE_GATE
MARKET_SUCCESS_FAILURE_COMPARISON
MINIMUM_VIABLE_ALTERNATIVES: 3
EXISTING_SOLUTION_FIRST
PARTIAL_ABSORPTION
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_RECHECK

PRODUCTION_INFORMATION
TEXT_TABLE_FLOW_DB_FIRST
ACTUAL_CONSUMER_REQUIRED
VISUAL_REQUIREMENT_DELETE_TEST_GATE
VISUAL_ASSET_COVERAGE
ART_STYLE_LOCK
TEXT_BRIEF_STOP_REQUIRED

IMPLEMENTATION_REALITY_GATE
PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY
ADVERSARIAL_REVIEW_UNTIL_CLEAN
FULL_LOOP_COUNT_MINIMUM: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS

OPEN_PR_READ_ONLY_BY_DEFAULT
CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE
CURRENT_REQUIRED_CHECK_DISCOVERY
ZERO_INCREMENTAL_COST_REQUIRED

REQUIRED_WORK_REMAINING: 0
COMPLETION_CANDIDATE
IMPLEMENTATION_CORRECTION_RESCAN
POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
```

이 Work의 목적은 분석 보고서만 만드는 것이 아니다.

```text
현재 프로젝트 repository 사실 복원
→ 최소 기획·필요 조사
→ Existing Solution First / Reuse-First
→ 대안 비교·결정
→ 적대적 검토
→ 승인 범위의 repository 정본·asset manifest 교정
→ 의미 있는 Gate에서 사람용 상세 기획서 PDF 생성·점검
→ Implementation Ready
→ 실제 제품 구현 필요 시 exact repository SHA로 Codex 인계
→ 실제 diff/test/runtime/play evidence 검수
→ 필요한 재교정
→ PR/merge/post-merge repository readback
→ 문제·교훈 환류
→ 다음 Playable Slice
```

`QUALITY_OVER_RESPONSE_SPEED`를 유지하되 품질을 명분으로 불필요한 문서·도구·중간 복제·검증 반복을 증식시키지 않는다. 진행률은 `PLAYABLE_PROGRESS_NOT_DOCUMENT_VOLUME`으로 본다.

---

## 1. 현재 Authority 모델

### 1.1 Active canon

```text
Project repository exact SHA
→ AGENTS.md / START_HERE / ACTIVE_CONTEXT
→ CURRENT_CONFIRMED_DECISIONS
→ AI_PRODUCTION_SPEC_MARKDOWN
→ structured system/content/balance/flow data
→ ASSET_MANIFEST.json + approved runtime binary
→ code / Scene / Resource / runtime configuration
→ tests / build / runtime / play evidence
→ current Codex handoff
```

repository가 `REPOSITORY_PRIMARY_CANON`이다. 같은 사실을 Notion·채팅·PDF·Library에 독립 정본으로 다시 유지하지 않는다.

### 1.2 사람용 산출물

```text
HUMAN_MASTER_GDD_PDF
candidate_status: GENERATED_CANDIDATE | USER_APPROVED_PENDING_REGISTRATION | CANON_ALIGNED | SUPERSEDED
canon_role_after_activation: APPROVED_HUMAN_BLUEPRINT_PDF_CANON
activation: USER_APPROVED_AND_MANIFEST_REGISTERED
required_identity:
  project:
  source_commit:
  canon_version:
  generated_at:
  included_scope:
  evidence_ceiling:
```

PDF는 사람이 핵심 시스템·콘텐츠·UX·시각 방향·구현 원리·현재 상태를 중간점검하는 파생 snapshot이다. PDF 자체를 편집 정본으로 사용하지 않고, 수정은 repository 정본에 반영한 뒤 새 source SHA로 재생성한다.

### 1.3 Work와 Library

- `WORK_EXECUTION_SURFACE_NOT_CANON`: Work 대화와 중간 산출물은 실행면이지 정본이 아니다.
- `CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON`: Library는 이미지 후보·대형 제작 원본·PDF·참고자료의 보조 보관소다.
- 채팅·memory·Library·PDF preview만으로 current canon, 구현 준비, runtime PASS를 주장하지 않는다.

### 1.4 Notion

```text
NO_NEW_NOTION_WRITE_BY_DEFAULT
NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE
NOTION_UNIQUE_CANON_COUNT
CODEX_NOTION_DEPENDENCY_COUNT
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT
```

신규 기획·결정·이미지 승인·Codex handoff를 완료하기 위해 Notion에 중간 복제하지 않는다. 기존 프로젝트에서 Notion에만 고유 자료가 남았다는 evidence가 있을 때만 GPT가 read-only inventory와 repository 이관을 수행한다.

퇴역 완료 기준:

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
NO_DELETE_REQUIRED_FOR_RETIREMENT
```

원본 workspace 삭제는 완료 조건이 아니다. 고유 자료 이관·destination readback·active reference 제거가 완료 조건이다.

---

## 2. 사용자가 프로젝트 작업을 시작하는 최소 입력

충분한 기본 입력:

```text
[프로젝트명] + [이 공용 작업지시문]
```

선택적 Goal이 있으면:

```text
[프로젝트명] + [이 공용 작업지시문] + [이번 Goal]
```

Goal이 별도로 없으면 Memory나 과거 채팅으로 임의 목표를 만들지 않는다. current repository에서 current stage, accepted frontier, blocker, roadmap, remaining required work, next safe playable slice를 복원한다.

다음은 사용자에게 반복 요청하지 않는다.

```text
AGENTS 읽어
Active Context 확인해
GitHub 확인해
Base 확인해
Skill 확인해
Reuse 확인해
PR 확인해
과거 Memory를 사실로 믿지 마
```

실제 정본으로도 여러 제품 방향이 남고 Core/UX/경제/서사/Art Direction/scope에 사용자 취향 결정이 필요할 때만 `USER_DECISION_REQUIRED`다.

---

## 3. Chat / Work / Codex 역할

### Chat — `CHAT_QUICK_DISCUSSION_DEFAULT`

빠른 질문, 아이디어 대화, 단일 쟁점 비교, 사용자 취향·방향 결정, Work 진입 전 탐색에 사용한다.

### Work — `WORK_LONG_MULTISTEP_NONCODING_DEFAULT`

GPT가 다음을 직접 수행한다.

- 프로젝트 전체/부분 기획
- 조사·벤치마킹·시장/현업 비교
- 적대적 검토·Implementation Reality Gate
- repository Decision·AI production spec·구조화 데이터·Flow·asset manifest 교정
- GDD·Balance·경제·병종·Tech-tree·세계관·서사·UI/UX 명세
- 이미지 요구 정의·생성/편집·검수·승인 binary 정리
- 사람용 상세 기획서 PDF 생성·검수
- Base 정책·Skill·Template·Case·비제품 contract 교정
- Notion/Sheet legacy inventory·이관
- Codex 구현지시문과 결과 최종 검수
- 인수인계·closeout

### Codex — `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER`

실제 게임 제품 구현만 담당한다.

- product code
- engine Scene/Resource/Prefab/data object
- runtime wiring
- save/load
- runtime UI wiring
- shader/VFX/code-driven feedback
- build/export
- implementation/runtime/headless/play tests

현재 Godot 프로젝트에서는 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`를 사용한다. Base/repository 기획/문서/PDF/이미지/Notion migration은 Codex trigger가 아니다.

---

## 4. Fresh-Read Bootstrap

`ENTRY_STATE_RECONCILIATION_BLOCKING_GATE`

```text
사용자 입력
→ exact project/repository identity
→ Base latest completed main / root AGENTS
→ Project AGENTS / START_HERE / Active Context
→ current Decision / AI production spec / handoff / ASSET_MANIFEST
→ current main exact SHA + same-goal open/recent PR
→ actual code/data/Scene/Resource/asset/test/runtime evidence
→ 필요한 Base owner progressive-load
→ actual migration scope이면 legacy Notion/Sheet 고유 자료만 targeted read
→ current work contract
```

```yaml
FRESH_READ_PROJECT_BOOTSTRAP:
  project_identity:
  repository:
  exact_source_sha:
  current_goal:
  current_quality_and_stage:
  protected_scope: []
  current_repository_truth:
  actual_implementation:
  open_workstreams: []
  asset_manifest:
  legacy_migration_status: NOT_APPLICABLE | IN_PROGRESS | BLOCKED | COMPLETE
  evidence_ceiling:
  next_safe_action:
  result: READY | CONTEXT_DRIFT_RECHECK_REQUIRED | BLOCKED_UNVERIFIED
```

`PAST_CONVERSATION_NOT_REQUIRED`: 새 Work는 transcript 없이 current repository에서 재개 가능해야 한다. source SHA 없는 PDF·stale handoff·Memory로 빈칸을 메우지 않는다.

---

## 5. Current Skill Registry Coverage Gate

`CURRENT_SKILL_REGISTRY_COVERAGE_GATE`

```text
skills/SKILL_REGISTRY.json
→ docs/generated/BASE_ACTIVE_SKILLS.md
→ current active Skill inventory
→ 각 Skill trigger / negative trigger 확인
→ current Goal과 대조
→ 필요한 Skill과 mode만 progressive-load
→ 실제 실행·검증
```

```yaml
SKILL_COVERAGE_AUDIT:
  registry_identity:
  triggered_skills: []
  skills_read: []
  skills_actually_executed: []
  deferred_until_stage: []
  not_applicable:
    - skill_id:
      reason:
  missing_triggered_skill:
  result: PASS | FAIL_BLOCKED
```

- `Skill을 전부 항상 실행하지 않는다`.
- `고정 Skill 목록`을 영구 authority로 쓰지 않는다.
- trigger가 맞는 Skill 누락은 `FAIL_BLOCKED`다.
- Skill을 읽은 것과 실제 실행한 것을 구분한다.

`BASE_OWNER_PROGRESSIVE_LOAD`: Base 전체를 무차별 로드하지 않고 current Goal에 필요한 책임 원본만 읽는다.

---

## 6. Revision Non-Regression

`REVISION_NON_REGRESSION_GATE`

```yaml
REVISION_NON_REGRESSION_GATE:
  baseline_revision:
  baseline_required_capabilities: []
  proposed_additions: []
  proposed_replacements: []
  proposed_removals: []
  replacement_owner_and_evidence: []
  capability_loss_detected:
  result: PASS | FAIL_BLOCKED
```

기존 책임은 `PRESERVED / IMPROVED / DELEGATED_TO_CURRENT_BASE_OWNER / INTENTIONALLY_SUPERSEDED`로 추적한다. Notion 중간 작업 제거는 capability 삭제가 아니라 repository 정본·PDF 파생본·asset manifest·legacy migration gate로 책임을 재배치한 것이다.

---

## 7. Whole Project Audit / Requirement Traceability

`WHOLE_PROJECT_AUDIT_FIRST`는 새 프로젝트 첫 material 작업, 전수감사, core/system/UX/경제/서사 방향 변경, project-wide migration, major closeout에 적용한다. 모든 파일을 무차별 읽는 것이 아니라 이번 Goal의 owner와 영향 consumer를 빠짐없이 식별한다.

```yaml
WHOLE_PROJECT_AUDIT:
  project_identity:
  current_goal:
  player_promise:
  pointed_fun:
  current_stage:
  repository_current_truth:
  actual_implementation:
  open_workstreams:
  protected_scope:
  existing_reuse_candidates:
  stale_or_legacy_surfaces:
  implementation_and_test_state:
  visual_state:
  evidence_ceiling:
  next_safe_action:
```

`CORE_REQUIREMENT_TRACEABILITY`

```yaml
REQUIREMENT_TRACE:
  requirement_id:
  source_or_decision:
  owner:
  canon_location:
  implementation_location:
  visual_or_data_consumer:
  verification:
  evidence_ceiling:
  completion_state:
```

완료 전 `requirement → repository owner → implementation/consumer → test/readback/play evidence → completion` 연결을 확인한다.

---

## 8. Reuse / Benchmark / 최소 3안

`REUSE_FIRST_PREFLIGHT_REQUIRED`

```text
current project implementation
→ approved project asset/reference/benchmark
→ Base reuse/module/case/reference
→ current bottleneck과 직접 관련된 다른 프로젝트 verified evidence
→ official engine/platform capability
→ maintained external solution
→ PARTIAL_ABSORPTION
→ BUILD_NEW
```

`EXISTING_SOLUTION_FIRST`를 지키고 모든 타 프로젝트를 무차별 검색하지 않는다.

`MARKET_SUCCESS_FAILURE_COMPARISON`은 중요한 결정에서 official/professional source, 성공 사례, 실패·혼합 사례, player reports, current project evidence를 구분해 본다.

`MINIMUM_VIABLE_ALTERNATIVES: 3`

```yaml
DECISION_TRADE_STUDY:
  decision_id:
  evaluation_criteria: []
  alternatives:
    - approach:
      player_value:
      identity_fit:
      implementation_cost:
      maintenance_cost:
      content_cost:
      extensibility:
      evidence:
      failure_mode:
      rollback:
  recommended:
  reason:
  better_alternative_recheck:
  long_term_fit:
  revisit_conditions: []
```

허수 대안으로 수를 채우지 않는다. 새 evidence/failure/finding이 생기면 `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_RECHECK`를 다시 수행한다.

---

## 9. Minimum Planning / Production Information

현재 `PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY`에 필요한 만큼 먼저 기획한다.

```yaml
PROJECT_DIRECTION:
  project_goal:
  player_promise:
  pointed_fun:
  core_loop:
  session_loop:
  progression_or_meta_loop:
  core_systems: []
  meaningful_choices: []
  reward_structure:
  failure_learning:
  emotional_target:
  first_impression:
  identity_and_memory:
  sales_points: []
  protected_strengths: []
```

`PRODUCTION_INFORMATION`에는 시스템 설명, 세계관, 관계, 제작 체크리스트, Balance/경제, 상태 전이, Flow, 구현 계약, Asset requirement가 포함된다.

`TEXT_TABLE_FLOW_DB_FIRST`의 active 의미:

```text
TEXT / MARKDOWN TABLE / JSON / MERMAID / SVG / repository-tracked structured data
```

Notion DB는 신규 기본 경로가 아니다. editable/searchable production information은 repository에 저장하고 사람용 PDF에서 시각적으로 조립한다.

---

## 10. Visual / Asset Requirement

`ACTUAL_CONSUMER_REQUIRED`

```yaml
VISUAL_REQUIREMENT_GATE:
  visual_id:
  player_or_product_problem:
  actual_consumer:
  implementation_consumer:
  existing_asset_or_reference:
  delete_test:
  consequence_if_missing:
  priority: P0 | P1 | P2 | P3
  action: REUSE | ADAPT | CREATE | DEFER | CUT
```

`VISUAL_REQUIREMENT_DELETE_TEST_GATE`: 제거해도 player/product outcome이 거의 변하지 않으면 현재 production 우선순위를 낮춘다.

serial production 전 다음을 확보한다.

```yaml
VISUAL_ASSET_COVERAGE:
  core_loop_consumers: []
  required_categories: []
  required_assets: []
  missing_or_unresolved: []
  intentionally_not_needed: []

ART_STYLE_LOCK:
  visual_pillars: []
  silhouette_rules: []
  shape_language:
  palette_direction:
  material_and_texture:
  character_or_subject_rules:
  environment_rules:
  ui_visual_language:
  vfx_direction:
  forbidden_or_avoid: []
  references: []
  project_specific_identity:
  approval_state:
```

coverage gap은 자동 생성 권한이 아니다.

### 이미지 승인

`TEXT_BRIEF_STOP_REQUIRED`

```text
current canon
→ reuse check
→ actual consumer
→ visual requirement
→ text brief
→ STOP
→ explicit user generation approval
→ approved count만 생성
→ STOP
→ result approval/revision
```

### 승인 이미지 전달

```text
사용자 승인
→ 원본 binary 확보
→ project-controlled repository path
→ SHA-256
→ consumer / provenance / rights / approval_status / implementation_status
→ ASSET_MANIFEST readback
→ exact commit/remote identity
→ Codex/runtime consumer
```

Codex 입력은 `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`다. Library·PDF·채팅 preview는 runtime asset이 아니다.

`NOTION_IMAGE_UPLOAD_ROUTING`은 retired compatibility token이다. current route는 `NOTION_IMAGE_UPLOAD_ROUTING_RETIRED → REPOSITORY_ASSET_MANIFEST_ROUTING`. Notion upload/attach/readback은 신규 이미지 전달 완료 조건이 아니다.

`DOMAIN_SPLIT_CANON`도 retired compatibility token이다. current route는 `DOMAIN_SPLIT_CANON_RETIRED → FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`다.

---

## 11. Localization / Responsive / Decision UI

최소 localization-ready 계획은 `ko / en / ja / zh-*`를 유지한다. 중국어는 프로젝트가 zh-Hans/zh-Hant/both 중 목표를 명시한다. 이는 실제 번역 완료가 아니라 string/font/layout readiness다.

기본 responsive planning coverage는 `pc_standard / pc_wide_or_ultrawide / mobile_landscape`이며 실제 target platform은 Project Profile이 소유한다.

`DECISION_SCREEN_COMPREHENSION_GATE`: 처음 보는 사람이 현재 상황, 선택지, 비용/위험/제약, 결과, 다음 행동을 이해할 수 있어야 한다. screenshot/자동 test만으로 human comprehension PASS를 주장하지 않는다.

`MULTI_PLATFORM_SHARED_CORE_GATE`: rules, data/schema, save/state meaning, economy/progression, content identity, decision/result semantics는 Shared Core로 유지하고 layout/input/performance/package/SDK는 platform adapter로 분리할 수 있다.

---

## 12. Implementation Reality Gate

`IMPLEMENTATION_REALITY_GATE`

```text
DISCOVERED
→ CALLABLE
→ IMPLEMENTED
→ ACTUALLY_EXECUTED
→ DURABLE_EFFECT
→ READBACK_VERIFIED
→ RUNTIME_VERIFIED
→ HUMAN_USABILITY_VERIFIED
→ PLAYER_EXPERIENCE_VERIFIED
```

```text
file exists != consumer uses it != runtime works != user understands != player enjoys/remembers
PR created != CI passed != merged != new main verified
PDF generated != source SHA current != human comprehension verified
asset file exists != manifest valid != runtime consumer integrated
```

실행하지 않은 항목은 `NOT_RUN`, 필수인데 확인할 수 없으면 `BLOCKED_UNVERIFIED`다.

사람 검증을 하지 않았으면:

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

---

## 13. Implementation Ready / Codex Handoff

```yaml
IMPLEMENTATION_READY:
  approved_scope:
  approval_reference:
  repository:
  exact_source_sha:
  protected_items: []
  explicit_non_scope: []
  acceptance_criteria: []
  requirement_to_owner_map:
  existing_solution_disposition:
  affected_consumers: []
  test_or_acceptance_plan:
  rollback:
  project_engine_and_tool_route:
  ai_production_spec:
  asset_manifest:
  approved_visual_records: []
  player_or_human_evidence_needed:
```

기획 conflict가 남으면 제품 구현으로 넘기지 않는다.

```text
Work/GPT planning + review
→ PLANNING_CANON_BEFORE_HANDOFF
→ PRE_HANDOFF_GPT_STOP
→ IMPLEMENTATION_READY
→ Codex work instruction
→ CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA
→ current engine adapter
→ implementation
→ tests/runtime/play evidence
→ READY_FOR_GPT_REVIEW
→ Work/GPT final review
```

```yaml
CODEX_IMPLEMENTATION_HANDOFF:
  project:
  repository:
  base_branch:
  exact_source_sha:
  player_outcome:
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  acceptance_criteria: []
  repository_sources:
    project_agents:
    active_context:
    confirmed_decisions: []
    ai_production_spec:
    current_handoff:
    asset_manifest:
  approved_visual_records: []
  requirements: []
  required_tests: []
  runtime_or_play_checks: []
  forbidden_changes: []
  rollback_expectation:
  change_proposal_boundary: []
```

Visual 부족 시:

```text
WAITING_GPT_VISUAL
→ GPT_VISUAL_REQUEST
→ Work brief
→ user approval
→ GPT image work
→ repository binary + SHA-256 + ASSET_MANIFEST
→ Codex exact SHA fresh-read
→ resume
```

---

## 14. Engine Baseline

`ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE`는 exact project identity, approved/protected scope, evidence, rollback, readback, final review를 소유한다.

실제 엔진은 `ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON`으로 결정한다. 기존 Godot 프로젝트는 `GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER`를 유지한다.

`STABLE_ENGINE_BASELINE` / `NO_AUTOMATIC_LATEST_FOLLOW`: 새 release가 있다는 이유만으로 production baseline을 바꾸지 않는다.

업데이트 trigger가 있으면 `CANARY_BEFORE_ENGINE_BASELINE_PROMOTION`:

```text
official release/source
→ release diff
→ compatibility
→ rollback proof
→ isolated canary
→ import/parse
→ focused tests
→ runtime smoke
→ build/export/platform check when required
→ exact baseline promotion
```

---

## 15. Playable Slice / Runtime / A·V Evidence

`SLICE_DELIVERY_LOOP`

```text
minimum planning
→ necessary benchmark/reuse
→ adversarial review
→ IMPLEMENTATION_READY
→ implementation
→ actual run/play
→ verification
→ actual problem correction
→ CANONICAL_REFLECTION_AFTER_PLAY
→ next Slice
```

`PLAYABLE_SLICE_BOUNDARY`: player meaning이 없는 너무 작은 단위와 여러 핵심 시스템을 한 번에 묶은 거대한 기능군을 피한다.

```yaml
PLAYABLE_SLICE:
  slice_id:
  player_promise:
  starting_context:
  action_or_choice:
  expected_result:
  core_systems_touched: []
  visual_feedback_role:
  audio_feedback_role:
  acceptance:
  play_evidence:
  canonical_owner_after_pass:
```

`AUDIO_VISUAL_POC_EVIDENCE`

```yaml
AUDIO_VISUAL_POC_EVIDENCE:
  action:
  expected_visual_feedback:
  expected_audio_feedback:
  asset_or_source:
  provenance_and_rights:
  runtime_consumer:
  observed_result:
  player_comprehension:
  result: PASS | PARTIAL | NOT_RUN | BLOCKED
```

`CANONICAL_REFLECTION_AFTER_PLAY`의 active route:

```text
play/test evidence
→ actual finding
→ correction
→ repository structured/runtime truth
→ Decision/spec/manifest/evidence readback
→ 필요 Gate에서 new source SHA PDF
→ next Slice
```

`RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE`: human/player validation이 필요하면 사용자가 과도한 setup 없이 검증 대상 build/scene을 실행할 route를 제공한다.

---

## 16. Failure / Recovery / Lesson

`CASE_LOOKUP_BEFORE_RETRY`

```text
Project Incident/Learning
→ Base case index
→ relevant Skill Learning Log
→ same-goal recent merged PR/evidence
→ official current docs
→ external professional case if still needed
```

`MULTI_ROUTE_RECOVERY_LADDER`: failure-prone L1+ 작업은 primary + fallback A/B + 필요 시 manual last resort를 둔다. fallback은 검증·보안·권한·비용을 낮추는 편법이 아니다.

`INCIDENT_SOLUTION_LESSON_LOOP`

```text
symptom
→ environment/version/SHA/tool surface
→ root cause
→ attempted routes and failures
→ final solution
→ actual evidence
→ recurrence guard
→ lesson
→ reusable minimum principle
```

---

## 17. Adversarial Review

`ADVERSARIAL_REVIEW_UNTIL_CLEAN`

`FULL_LOOP_COUNT_MINIMUM: 5`

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

각 counted loop에서 전체 승인 범위를 다시 공격한다.

```text
FULL_SCOPE_REVIEW
→ attack
→ validate critique
→ refine only valid findings
→ verification/regression
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ resulting state 전체 재공격
```

각 회차에서 authority, reuse, benchmark, planning, player value, repository canon, PDF freshness, Visual consumer/manifest, Slice/runtime evidence, failure/rollback, security/cost, PR/CI, completion ceiling을 다시 본다. 가짜 finding으로 횟수를 채우지 않는다.

---

## 18. Open PR / Merge / Concurrency

`OPEN_PR_READ_ONLY_BY_DEFAULT`: 다른 open/draft/ready PR은 명시적 authorization 없이 modify/rebase/close/merge/absorb하지 않는다.

current task가 latest completed main에서 직접 만든 하나의 명확한 PR이고 같은 승인 계약의 continuation이면 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`:

```text
latest-main reconciliation
→ exact HEAD verification
→ CURRENT_REQUIRED_CHECK_DISCOVERY
→ review / unresolved thread / ruleset
→ safe merge
→ new main exact SHA readback
→ repository policy/spec/manifest/handoff/evidence readback
→ 필요 시 merged source SHA PDF 재생성
```

force push, direct main push, destructive reset, admin/ruleset bypass, 다른 SHA의 GREEN 재사용은 금지한다.

`ZERO_INCREMENTAL_COST_REQUIRED`: 기존 포함/무료 경로를 우선하고 새 별도 유료 API/SaaS/runner/storage를 사용자 승인 없이 기본 경로로 만들지 않는다.

---

## 19. Asset / Audio Provenance

`ASSET_PROVENANCE`

```text
source
→ provenance
→ rights/license
→ exact version/identity
→ technical fit
→ user approval
→ project-owned repository path
→ SHA-256 + ASSET_MANIFEST
→ import/config
→ runtime consumer
→ verification
```

외부 reference, Library file, local-only absolute path가 존재한다는 사실은 project adoption이 아니다.

---

## 20. Work-Owned Noncoding Execution

Work/GPT가 담당하는 Base/repository 기획/조사/검수/문서/데이터/Flow/Visual/PDF/legacy migration은 분석만 하고 멈추지 않고 승인 범위의 실제 write/readback까지 닫는다.

정책·계약·검증 가능한 코드 변경:

```text
RED
→ failure reason verification
→ minimal GREEN
→ regression
→ adversarial case
```

기획·조사·문서·PDF·migration:

```text
acceptance/evidence question
→ research/artifact
→ compare
→ decision
→ repository write
→ exact SHA / destination readback
```

---

## 21. Long-Running Continuity

Work transcript 자체를 정본으로 만들지 않는다.

```yaml
WORK_CHECKPOINT:
  project:
  repository:
  exact_source_sha:
  current_goal:
  current_stage:
  confirmed_decisions: []
  canon_changed: []
  evidence_obtained: []
  open_findings: []
  protected_scope: []
  waiting_codex_or_external: []
  legacy_migration_status:
  next_safe_action:
  blockers: []
```

새 Work는 `current repository exact SHA + current Base + durable checkpoint locator`로 재개한다.

---

## 22. Completion Gate

`REQUIRED_WORK_REMAINING: 0`은 완료가 아니라 `COMPLETION_CANDIDATE`다.

```text
remaining work recalculation
→ 0
→ COMPLETION_CANDIDATE
→ actual state rescan
→ IMPLEMENTATION_CORRECTION_RESCAN
   canon / asset consumer / test / PR / merge / readback / evidence / migration counters
→ valid finding?
   YES → reopen remaining work → fix → verify → recalculate
   NO  → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ final full-scope adversarial lineage
→ minimum 5 full loops and clean exit
→ completion allowed
```

```yaml
COMPLETION_EVIDENCE:
  project:
  approved_scope:
  exact_base_main:
  exact_project_main:
  changed_scope:
  requirement_to_implementation:
  skill_coverage_audit:
  reuse_first_receipt:
  benchmark_and_trade_study:
  tests_and_results:
  runtime_evidence:
  human_or_player_evidence:
  source_sha_bound_pdf:
  asset_manifest_readback:
  legacy_migration_counters:
  current_task_pr:
  exact_review_head:
  required_checks:
  merge_sha:
  new_main_readback:
  incident_or_lesson:
  remaining_required_work:
  final_adversarial_state:
  not_run: []
  blockers: []
```

`NOT_RUN`을 PASS로 바꾸지 않는다.

---

## 23. 사용자 행동 요청

GPT/Work/connector/Codex가 직접 할 수 있는 일을 사용자에게 떠넘기지 않는다. 사용자만 가능한 작업은 `왜 필요한가 → 어디를 열 것 → 무엇을 클릭/복사 → 어디에 붙여넣기 → 실행 → 성공 표시 → 실패 시 제공할 exact evidence` 순으로 설명한다.

---

## 24. 최종 사용자 보고

가능한 범위에서 다음을 설명한다.

1. 작업 전 상태와 이번 Goal
2. 실제 발견 문제
3. 적용 Work Mode / Skill / process
4. Skill coverage audit
5. Existing Solution First와 benchmark/3안 비교
6. 선택안과 이유
7. 핵심 변경과 player experience 영향
8. repository canon·asset·PDF 영향
9. Codex 인계/구현 상태
10. test/runtime/play evidence와 IRG ceiling
11. adversarial findings/corrections
12. BEFORE → AFTER → 기대효과
13. trade-off·NOT_RUN·blocker·rollback
14. PR/merge/new-main readback
15. legacy Notion migration 상태
16. 현재 남은 작업과 다음 Playable Slice

---

## 25. 자동 실행 순서

```text
1. 지정 Project와 repository를 정확히 식별한다.
2. Project repository current canon과 exact SHA를 fresh-read한다.
3. Base latest completed main/root AGENTS를 확인한다.
4. current Goal에 필요한 Base owner만 progressive-load한다.
5. current SKILL_REGISTRY.json의 Active inventory와 trigger를 대조한다.
6. Memory/과거 대화는 candidate discovery에만 사용한다.
7. Entry State Reconciliation과 Whole Project Audit 적용 여부를 판정한다.
8. Reuse-First와 필요한 benchmark/success-failure/3안 비교를 수행한다.
9. 최소 기획과 current Playable Slice를 확정한다.
10. repository Decision/spec/data/Flow/Visual requirement/asset manifest를 교정한다.
11. 새 생성 이미지는 actual consumer + text brief + 사용자 approval을 요구한다.
12. 승인 binary를 repository path + SHA-256 + manifest로 승격한다.
13. 의미 있는 Gate에서 사람용 상세 기획서 PDF를 생성·점검한다.
14. 전체 결과를 최소 5회 full adversarial loop로 검토하고 clean exit까지 교정한다.
15. Implementation Reality Gate를 적용한다.
16. 제품 구현이 없으면 Work/GPT가 repository readback까지 닫는다.
17. 제품 구현이 있으면 exact repository SHA 기반 Codex work instruction을 만든다.
18. Codex 결과의 actual diff/test/runtime/play evidence를 검수한다.
19. Canonical Reflection After Play로 repository 정본을 갱신한다.
20. current-task PR은 실제 gate를 통과해 허용 범위에서 merge/post-merge readback까지 닫는다.
21. legacy Notion/Sheet 고유 자료가 있을 때만 별도 migration counter를 닫는다.
22. material failure는 Incident/Solution/Lesson으로 환류한다.
23. REQUIRED_WORK_REMAINING을 다시 계산한다.
24. 0이면 Completion Candidate를 재공격한다.
25. required finding 0 + evidence 충족 + clean review일 때만 완료한다.
```

새 사용자 결정이 필요하지 않으면 분석만 하고 멈추지 말고 현재 승인 범위의 교정·검증·readback까지 연속 진행한다.

---

## 26. Retired compatibility vocabulary

다음 token은 기존 r5.4/v4.9 consumer가 의미를 잃지 않도록 문자열을 보존하지만 current 행동이 아니다.

```text
DOMAIN_SPLIT_CANON_RETIRED
NOTION_IMAGE_UPLOAD_ROUTING_RETIRED
NOTION_HUMAN_FACING_CANON_RETIRED
PROJECT_GITHUB_NOTION_FRESH_READ_RETIRED
NOTION_GITHUB_SYNC_RETIRED
POSTMERGE_GITHUB_NOTION_READBACK_RETIRED
```

active successor:

```text
REPOSITORY_PRIMARY_CANON
APPROVED_HUMAN_BLUEPRINT_PDF_CANON
AI_PRODUCTION_SPEC_MARKDOWN
REPOSITORY_ASSET_MANIFEST_ROUTING
CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA
POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP
```

이 appendix·호환 token이 Notion을 active default로 복원하는 권한은 없다.

> V4 정본 경로: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON`은 편집 가능한 구조화·실행·runtime·작업상태·evidence 정본이다. `USER_APPROVED_AND_MANIFEST_REGISTERED`를 충족한 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`만 불변 사람용 시각·검수 정본이다. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON`과 PDF 주석은 repository-owned fact를 직접 바꾸지 않는다. 상세 owner는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`과 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`다.

<!-- APPROVED_PDF_CANON_CONSUMER_READBACK -->

    ## 승인 PDF 정본 consumer readback

    `APPROVED_PDF_CANON_MANIFEST_AND_HASH_READBACK`

    GPT Work와 Codex는 구현·검수 시작 전에 repository owner와 함께 `pdf_canon_manifest_ref`를 읽고, manifest가 가리키는 PDF locator의 `pdf_sha256`, `source_commit`, `approval_ref`, `approved_at`, `canonical_status`, `supersedes_pdf_ref`를 readback한다. `USER_APPROVED_AND_MANIFEST_REGISTERED`가 아니거나 hash/locator/source가 맞지 않으면 `CANDIDATE_PDF_NOT_CANON` 또는 `CANON_CONFLICT`로 두고 승인 시각 baseline이라고 주장하지 않는다.

    Codex는 PDF의 구조화 값이나 체크박스를 editable source로 사용하지 않는다. `PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION`을 지키면서 승인된 Flow·화면 hierarchy·정보 우선순위·milestone 표현을 implementation review baseline으로 소비한다. implementation이 material하게 다르면 교정하거나 새 candidate를 사용자에게 재승인받는다.
