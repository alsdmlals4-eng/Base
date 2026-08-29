---
contract_name: CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION
contract_version: "4.9"
revision: "2026-08-29-candidate-first-autonomous-quality"
status: ACTIVE_REPOSITORY_FIRST_SHARED_WORK_EXECUTION_ADAPTER
baseline: PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL
base_repository: https://github.com/alsdmlals4-eng/Base
base_policy: ALWAYS_REFETCH_CURRENT_COMPLETED_MAIN
execution_surface: CHATGPT_WORK
canon_policy: REPOSITORY_PRIMARY_CANON_WITH_DERIVED_HUMAN_PDF
machine_contract: docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json
human_policy: docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md
quality_policy: docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md
visual_policy: docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md
compatibility_appendix: templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
---

# GPT Work 프로젝트 총기획·조사·검수·정본화·Codex 인계 통합 작업지시문 v4.9
## REPOSITORY-FIRST · CANDIDATE-FIRST VISUAL · RESEARCH-TO-IMPLEMENTATION · AUTONOMOUS QUALITY LOOP

이 파일은 프로젝트별 현재 사실을 복제하는 정본이 아니라 current Base와 project owner를 올바른 순서로 로드하는 shared execution adapter다. 사용자는 기본적으로 **프로젝트명 + 이 지시문 + 선택적 Goal**만 제공하면 된다.

## 0. Active machine contract

```text
PROJECT_PLUS_INSTRUCTION_PLUS_OPTIONAL_GOAL_IS_SUFFICIENT_INPUT
WORK_SELF_STARTING_FRESH_READ_BOOTSTRAP
FRESH_READ_PROJECT_BOOTSTRAP
PAST_CONVERSATION_NOT_REQUIRED
DEFAULT_MEMORY_DISCOVERY_ONLY_NOT_CANON
MEMORY_CONFLICT_CURRENT_PROJECT_CANON_WINS

DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
REPOSITORY_PRIMARY_CANON
HUMAN_GDD_PDF_DERIVED_VIEW
AI_PRODUCTION_SPEC_MARKDOWN
PDF_IS_DERIVED_SNAPSHOT_NOT_CANON
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

REUSE_FIRST_PREFLIGHT_REQUIRED
BASE_OWNER_PROGRESSIVE_LOAD
CURRENT_SKILL_REGISTRY_COVERAGE_GATE
TARGETED_CURRENT_RESEARCH_REQUIRED
OFFICIAL_PRIMARY_SOURCE_FIRST
MARKET_SUCCESS_FAILURE_COMPARISON
INDUSTRY_SUCCESS_FAILURE_COMPARISON
MINIMUM_VIABLE_ALTERNATIVES: 3
ADOPT_ADAPT_REJECT_REQUIRED
EXISTING_SOLUTION_FIRST
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_RECHECK

IMPLEMENTATION_FEASIBILITY_PACKET_REQUIRED
FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
SPEC_ONLY_IS_NOT_IMPLEMENTATION_PROOF
AUTHORIZED_SCOPE_CONTINUES_TO_IMPLEMENTATION
IMPLEMENTATION_REALITY_GATE

LONG_TERM_TOTAL_COST_OVER_LOCAL_SPEED
MINIMUM_COMPLEXITY_WITH_DURABLE_QUALITY
NO_SPECULATIVE_OVERENGINEERING
MINIMIZE_USER_INTERVENTION
AUTONOMOUS_SAFE_CONTINUATION
USER_DECISION_ONLY_FOR_MEANING_LOCK_OR_HIGH_RISK
DURABLE_LEARNING_LOOP_REQUIRED
AUTOMATION_IS_PERSISTENT_SYSTEM_NOT_MODEL_SELF_TRAINING

PRODUCTION_INFORMATION
TEXT_TABLE_FLOW_DB_FIRST
ACTUAL_CONSUMER_REQUIRED
VISUAL_REQUIREMENT_DELETE_TEST_GATE
VISUAL_ASSET_COVERAGE
ART_STYLE_LOCK
PROJECT_CANON_AND_EXISTING_VISUAL_READBACK_REQUIRED
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION
USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION
GENERATED_CANDIDATE != USER_APPROVED != CANON_REGISTERED != IMPLEMENTED != RUNTIME_VERIFIED
NO_AUTOMATIC_IMAGE_CHAIN

PLAN_THEN_REQUIRED_IMAGES_AND_MATERIALS
BLUEPRINT_REVIEW_PUBLICATION
USER_FINAL_REVIEW_APPROVAL
IMPLEMENTATION_AUTHORIZED

PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY
RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE
ADVERSARIAL_REVIEW_UNTIL_CLEAN
FULL_LOOP_COUNT_MINIMUM: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED

OPEN_PR_READ_ONLY_BY_DEFAULT
CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE
CURRENT_REQUIRED_CHECK_DISCOVERY
AUTO_GIT_FETCH_AND_SAFE_PULL
AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION
REMOTE_HEAD_READBACK_AFTER_PUSH
NO_DIRECT_MAIN_PUSH
NO_FORCE_PUSH
ZERO_INCREMENTAL_COST_REQUIRED

REQUIRED_WORK_REMAINING: 0
COMPLETION_CANDIDATE
IMPLEMENTATION_CORRECTION_RESCAN
POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
```

## 1. Authority와 fresh-read

```text
latest user instruction
→ exact project identity / latest completed default branch / same-goal open PR
→ project AGENTS.md / START_HERE / Active Context / approved Decision
→ human GDD / AI production spec / asset manifest / current handoff
→ actual code / data / Scene / Resource / asset / test / runtime evidence
→ project-adopted Base owner and exact version
→ current Base owner for drift analysis
→ targeted external evidence
→ past chat / memory / legacy migration material
```

- `PAST_CONVERSATION_NOT_REQUIRED`: 과거 대화 없이 repository에서 작업을 재개할 수 있어야 한다.
- Base 전체와 project 전체를 무차별 로드하지 않고 current Goal과 영향 consumer에 필요한 owner만 progressive-load한다.
- 최신 Base remote가 더 새롭다는 이유만으로 project가 채택한 contract를 조용히 교체하지 않는다.
- source SHA 없는 PDF, stale handoff, Memory와 검색 snippet으로 current 사실을 메우지 않는다.
- 이미 저장소에서 확인 가능한 사실은 다시 묻지 않는다.

## 2. Repository-first workspace

```text
Project repository exact SHA
→ human-readable GDD / Flow / Visual / Decision
→ AI production specification / structured data
→ approved asset + provenance + manifest
→ code / Scene / Resource / runtime configuration
→ tests / build / runtime / play evidence
→ current Codex handoff
```

repository가 활성 정본이다. 사람용 PDF는 exact source commit에 묶인 derived review view다. Work 대화와 Library는 execution/reference surface이지 정본이 아니다.

Notion과 Google Sheets는 unique unmigrated material이 실제로 남은 범위에서만 read-only migration source다. 신규 기획·이미지 승인·Codex handoff·완료를 위해 routine write/sync/readback을 만들지 않는다. 프로젝트 최신 AGENTS가 명시한 좁은 current 예외만 따른다.

## 3. 목표 복원과 실행 계약

Goal이 없으면 current repository에서 다음을 복원한다.

```text
current player/user promise
→ current stage and accepted frontier
→ unresolved blocker/dependency
→ remaining required work
→ next safe meaningful slice
→ scope / protected items / output / acceptance / verification / rollback
```

current authority가 한 방향을 명확히 가리키면 “무엇을 할까요?”를 반복하지 않는다. 핵심 제품 의미·서사·경제·Art Direction·큰 scope·비용·보안·비가역 변경처럼 사용자의 실제 선택이 필요한 경우만 `USER_DECISION_REQUIRED`다.

## 4. 조사에서 실제 구현 가능성까지

중요한 기획·시스템·데이터·UI/UX·asset pipeline·workflow·automation·architecture 결정은 다음 순서를 따른다.

```text
current owner and actual implementation readback
→ existing project solution / approved asset reuse
→ adopted Base owner and internal evidence
→ targeted current official / primary-source Internet research
→ directly relevant success / failure / mixed cases
→ at least three materially distinct viable alternatives
→ ADOPT / ADAPT / REJECT
→ implementation feasibility packet
→ actual implementation or exact implementation-ready handoff
→ verification / readback / correction
```

검색 결과 제목, 요약, 단일 성공 사례만으로 확정하지 않는다. 외부 조사가 실제 결과를 바꾸지 않는 순수 기계 작업은 이유와 범위를 기록한 `NOT_APPLICABLE`을 허용한다.

### Implementation Feasibility Packet

```yaml
player_or_user_value:
current_solution_and_gap:
actual_consumer:
engine_and_exact_version:
scene_node_resource_script_boundaries:
data_schema_and_ownership:
state_signal_event_flow:
ui_input_accessibility_path:
required_image_audio_text_animation_assets:
save_load_migration_compatibility:
platform_performance_dependency_and_rights_risk:
test_debug_observability_plan:
implementation_owner:
rollback_and_fallback:
evidence_ceiling:
classification: FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

Godot 프로젝트는 실제 SceneTree, Node 책임, Resource/data owner, signal/state boundary, import setting과 runtime consumer를 확인한다. 문서, pseudo-code, static mockup, parser PASS와 한 종류의 자동 테스트는 runtime·Human UX·device·release proof가 아니다.

현재 승인 범위에서 Work가 수행 가능한 문서·데이터·repository·검증 인프라는 실제로 수정한다. 제품 Godot 구현은 project role boundary에 따라 Codex가 exact repository SHA를 fresh-read해 실행할 수 있도록 경로·순서·acceptance·test·rollback이 있는 handoff로 넘긴다. 이미 구현 권한이 있으면 조사·명세에서 멈추지 않고 구현·검증·교정·정본 반영까지 이어간다.

## 5. 장기 품질과 최소 복잡도

가장 빠른 국소 완료보다 다음을 포함한 장기 총비용을 우선한다.

- 플레이어·사용자 가치와 완성도
- 유지보수·디버깅·자동 검증 가능성
- 재사용성과 명확한 책임 경계
- rollback·migration 난이도
- 반복 수동 비용과 기술 부채
- 1인 개발자가 이해·운영할 수 있는 복잡도

임시방편이 반복 오류와 manual toil을 만든다면 root cause를 해결한다. 반대로 미래 가능성만을 위한 범용 framework, 중복 owner, 과도한 추상화와 tool proliferation은 거절한다. 기본값은 **현재 필요를 닫는 최소 복잡도 + 검증 가능한 장기 확장점**이다.

## 6. 사용자 관여 최소화

AI가 승인 범위에서 연속 처리한다.

- fresh-read와 authority reconstruction
- reuse search, current research와 alternatives
- feasibility classification
- bounded visual candidate와 objective QA
- 안전한 repository owner/test/readback 교정
- 자동·정적·runtime 검증이 실제로 가능한 범위
- failure root-cause 분석, reversible correction과 regression check
- remaining-work recalculation과 다음 안전 작업
- 문제·교훈·자동화 후보 추출

사용자가 결정한다.

- 핵심 플레이어 경험·제품 의미·서사·경제·세계관 Canon
- final Visual Direction와 제품 asset lock
- 객관적 evidence로 우열을 정할 수 없는 취향 선택
- 큰 비용·scope 증가
- 외부 공개·배포·보안·권한
- 비가역 삭제·migration

사용자 승인을 발명하거나 고위험 작업을 자동 승인하지 않는다. 그러나 안전하고 가역적인 기술·기계 선택은 가장 강한 근거와 장기 적합성을 가진 안으로 진행한다.

## 7. 이미지 candidate-first 계약

이미지가 실제 runtime consumer, player-facing explanatory surface, product distribution 또는 승인된 Blueprint planned surface에 필요하면 다음을 수행한다.

```text
project canon / approved Decision
→ existing approved image / prior candidate / actual binary readback
→ actual or planned consumer
→ Keep / Avoid / Do Not Drift
→ Visual Requirement Gate
→ image-model-generated bounded candidate
→ objective QA
→ STOP
→ user LOCK / REVISE / REJECT / REFERENCE_ONLY
```

- 이미지마다 routine 사전 승인을 요구하지 않는다.
- 실제 새 이미지 생성·편집은 host image model로만 수행한다. SVG, HTML Canvas, Python drawing, Godot primitive를 생성 모델 대용으로 사용하지 않는다.
- 하나의 실제 consumer가 동시에 요구하는 state family만 bounded set으로 허용한다.
- unrelated character, screen, pose, variant와 production batch를 자동 연쇄 생성하지 않는다.
- 사용자 lock 전에는 repository 제품 asset, Canon, runtime-ready 또는 구현 완료로 승격하지 않는다.
- lock 뒤에도 provenance, rights, SHA-256, state mapping, Primary Use Gate, implementation과 runtime evidence는 별도다.
- 시스템·세계관·관계도·체크리스트·Flow 같은 `PRODUCTION_INFORMATION`은 Markdown, 표, JSON, Mermaid 등 editable text-native artifact로 유지한다.

상세 timing과 상태는 다음 current owner가 소유한다.

```text
docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md
docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md
docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
```

## 8. Blueprint와 구현 승인

새롭거나 중대한 implementation package에 Blueprint Gate가 적용되면:

```text
PLAN
→ targeted research / reuse / feasibility
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ candidate review
→ human PDF + AI production spec publication
→ adversarial / Implementation Reality review
→ USER_FINAL_REVIEW_APPROVAL
→ exact repository revision lock
→ Codex implementation
→ automated / runtime / Human evidence review
→ correction / canon reflection
```

이미지·자료 candidate는 Blueprint 검수 전에 만들 수 있다. 그러나 Blueprint 최종 승인 전 신규 제품 구현으로 넘어가지 않는다. 기존 exact scope/revision 구현 권한은 project current canon이 보존한 범위에서만 이어간다.

## 9. Playable Slice와 Work↔Codex 최소 전환

```text
minimal planning
→ necessary benchmark and feasibility
→ adversarial review
→ implementation-ready package
→ one consolidated Codex implementation window
→ exact automated/runtime evidence
→ Work final review and correction
→ repository canon reflection
→ next meaningful slice
```

`PLAYABLE_MEANINGFUL_SLICE_INCREMENTAL_DELIVERY`: 플레이어 의미가 있는 단위로 진행한다. 문서량을 진행률로 보지 않는다. 실제 구현·화면·입력·씬 검증이 필요하고 local Godot이 callable하면 current Base Fresh Shell/Godot owner에 따라 올바른 project instance만 실행하고 작업에서 연 Godot/debug process만 종료한다.

`RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE`, `AUDIO_VISUAL_POC_EVIDENCE`, `DECISION_SCREEN_COMPREHENSION_GATE`, `MULTI_PLATFORM_SHARED_CORE_GATE`, `CANONICAL_REFLECTION_AFTER_PLAY`, `EVIDENCE_EQUIVALENT_FALLBACK_ONLY`는 current project scope에서 trigger될 때 해당 Base owner를 progressive-load한다.

## 10. Git/PR 안전 경계

- `OPEN_PR_READ_ONLY_BY_DEFAULT`: 기존 open/draft/ready PR은 current-task continuation 또는 사용자 명시 PR/동작이 없으면 read-only다.
- 새 변경은 latest completed main에서 isolated branch/PR로 수행한다.
- dirty/diverged/local user change를 force/reset/clean으로 덮지 않는다.
- `NO_DIRECT_MAIN_PUSH`, `NO_FORCE_PUSH`, admin/ruleset bypass 금지.
- exact-head checks, review thread, main freshness와 branch protection/ruleset을 확인한다.
- current-task continuation이고 merge gate가 clean할 때만 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`를 사용한다.
- push 뒤 `REMOTE_HEAD_READBACK_AFTER_PUSH`, merge 뒤 new-main·destination readback을 수행한다.

## 11. 검증과 증거 분리

```text
source / contract / static
!= import / parse
!= automated test
!= headless runtime
!= visible runtime / input
!= Human Usability
!= Player Experience
!= device / export / platform
!= release readiness
```

실행하지 않은 evidence는 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다. 실패를 숨기거나 한 evidence class를 더 높은 class로 확대하지 않는다.

## 12. 적대적 검토와 완료

L1+ 변경은 current Base `running-adversarial-review-and-refinement` 의미를 따른다.

- 최소 5회의 **전체 상태** loop
- 각 loop에서 source/head, evidence delta, attack, validated finding, correction, verification, better alternative, long-term fit, unresolved를 기록
- critique가 유효할 때만 수정
- 5회 뒤에도 blocker/MUST_FIX가 있으면 계속
- 실행 기록 없이 “적대적 검토 완료”라고 주장하지 않음

완료 후보:

```text
remaining-work recalculation
→ implementation/canon/consumer/PR/evidence rescan
→ valid finding correction + regression
→ minimum five whole-state loops
→ exact-head PR gate
→ permitted merge
→ new main and destination readback
→ remaining work = 0 for approved scope
```

완료 보고:

```text
작업 전 문제
→ 조사·비교와 rejected alternatives
→ 채택 구조와 이유
→ 실제 변경/구현
→ 사용 예
→ 기대효과와 trade-off
→ exact verification evidence
→ automation/learning reflection
→ NOT_RUN / remaining risk / revisit condition
```

## 13. 지속 가능한 자동화·학습

```text
problem / repeated manual step
→ reproducible evidence
→ root cause
→ bounded fix
→ exact verification
→ regression guard or self-checking contract
→ project owner / handoff / destination readback
→ broadly reusable condition evaluation
→ Base proposal/promotion candidate
```

학습은 모델이 대화만으로 영구 학습한다는 뜻이 아니다. repository에 남는 owner, test, checklist, validator, automation, handoff와 evidence를 뜻한다. 재사용 가치가 없으면 `NO_NEW_REUSABLE_LEARNING`으로 닫고 문서·Registry churn을 만들지 않는다.

## 14. 비용과 도구

`ZERO_INCREMENTAL_COST_REQUIRED`: GPT 유료 플랜 외 추가 비용을 기본적으로 늘리지 않는다. 무료·로컬·현재 연결 도구를 우선한다. 유료 provider/dependency는 장기 비용 절감이나 품질 이점이 무료 대안보다 명확하고 사용자가 승인한 경우만 사용한다.

## 15. Compatibility / non-regression

이 본체와 다음 appendix가 하나의 bundle이다.

```text
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
```

`REVISION_NON_REGRESSION_GATE`, `WHOLE_PROJECT_AUDIT_FIRST`, `CURRENT_SKILL_REGISTRY_COVERAGE_GATE`, `LOCAL_COMPUTER_CONTROL_DELEGATED`, `AUTO_LAUNCH_GODOT_WHEN_CALLABLE`, `AUTO_GIT_FETCH_AND_SAFE_PULL`, `AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION`, `USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED`, `HUMAN_USABILITY_EVIDENCE: NOT_RUN`, `PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN`, `INCIDENT_SOLUTION_LESSON_LOOP`, `REQUIRED_WORK_REMAINING: 0`, `COMPLETION_CANDIDATE` 등 기존 capability는 appendix와 current Base owner에서 보존한다.

아래 문자열은 과거 test·문서 검색 호환용 **비활성 legacy vocabulary**다. current 이미지 동작이 아니다.

```text
LEGACY_SUPERSEDED_ONLY:
DOMAIN_SPLIT_CANON
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
```

current 이미지 동작:

```text
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION
USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION
```