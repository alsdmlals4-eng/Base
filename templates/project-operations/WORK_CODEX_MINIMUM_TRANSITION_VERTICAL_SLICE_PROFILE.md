# Work↔Codex 최소 전환 버티컬 슬라이스 실행 프로필

> 이 파일은 명시적 사용자 위임이 있을 때 Work v4.9에 결합하는 선택형 실행 adapter다. 세부 전문 절차를 복제 소유하지 않고 current Base owner를 조합한다.

## 0. Authority and owner composition

```text
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_SLICE_ONLY
COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON
CURRENT_OWNER_DETAILS_WIN_ON_DRIFT
WORK_NONPRODUCT_OWNER_PRESERVED
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED
HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION
NO_AUTOMATIC_SCOPE_EXPANSION
```

Current detailed owners:

- Work continuation/recovery: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Work↔Codex role and handoff: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Planning/Grill Me policy: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Grill Me interview protocol: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- Visual production/approval: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Default image conversation gate: `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- Shipping-intent Slice evidence: `skills/designing-vertical-slices/SKILL.md`
- HiGodot/GUT/Hera authority: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

이 프로필은 위 owner의 두 번째 정본이 아니다. 세부 owner가 바뀌면 current Base owner가 이 adapter의 오래된 문구보다 우선한다. 프로젝트별 Core, 현재 Slice, Decision, Art Direction, 실제 구현·테스트·자산 상태는 exact Project canon과 actual implementation이 계속 소유한다.

활성화에는 현재 사용자의 명시적 위임 evidence가 필요하다. routine 권장안 승인, 중간 정지 최소화, Work에서 actual game input 일괄 준비, Codex 단일 구현 window, machine QA 우선, Human QA 후속 보류 같은 위임이 없거나 사용자가 더 좁은 제한을 주면 default Work v4.9와 default image approval이 유지된다.

상위 system·developer·host·tool이 confirmation을 강제하면 `HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE`를 따른다. 이 profile은 host Gate, repository ruleset, account/security confirmation을 우회하지 않는다.

```text
FIVE_STAGE_VERTICAL_SLICE_FLOW_REQUIRED
MACRO_STAGE_IS_NOT_WORK_MODE
GAME_PROJECT_ONLY
NON_GAME_PROJECT_NOT_APPLICABLE
PROJECT_WORK_MACRO_FLOW = CURRENT_BASE_FIVE_STAGE_VERTICAL_SLICE_FLOW
PROJECT_SPECIFIC_STAGE_STATE = RESOLVE_FROM_CURRENT_PROJECT_CANON
```

`PLAN / BUILD / REVIEW` 같은 Project Work Mode는 아래 macro stage 안의 수행 방식이다. 명시적인 사용자 승인 current Project Decision이 별도 macro flow를 소유하지 않는 한 5단계를 대체하지 않는다. 비게임 프로젝트에는 이 Godot/Codex 실행 flow를 강제하지 않는다.

## 1. Five-stage macro flow with minimum Work↔Codex transitions

`minimum-transition`은 macro stage 수를 줄인다는 뜻이 아니다. **1~3단계를 Work에서 연속으로 닫고 4단계 product implementation을 Codex 한 window로 묶어 Work↔Codex 왕복을 최소화한다.**

Compatibility vocabulary는 유지한다.

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
WORK_PRODUCTION_INPUT_BATCH
MINIMIZE_WORK_CODEX_TRANSITIONS
CONSOLIDATED_RETURN_PACKET
```

### 1단계 — 기획

```text
STAGE_1_PLANNING
USER_COLLABORATIVE_CORE_PLANNING_REQUIRED
GRILL_ME_FOR_MATERIAL_CORE_DECISIONS
DECISION_RELEVANT_BENCHMARK_REQUIRED
THREE_MATERIALLY_DISTINCT_APPROACHES
EXISTING_SOLUTION_FIRST
ADOPT / ADAPT / REJECT
SLICE_PLANNING_LOCKED
```

새 Slice 또는 material 재설계는 먼저 Project GitHub·Notion·actual implementation을 fresh-read하고 기존 승인 Decision·자산·구현·Base reusable evidence를 복원한다.

아직 승인되지 않았고 제품 의미를 바꾸는 핵심 요소는 GPT가 단독 확정하지 않는다. 다음처럼 플레이어 경험과 제품 정체성을 좌우하는 항목은 current Grill Me owner를 사용해 사용자와 함께 닫는다.

- player promise / 핵심 판타지
- 대표 player action
- meaningful choice와 trade-off
- 결과·보상·실패 학습
- 목표 감정·기억·다음 동기
- 첫 세션에서 보여줄 대표 경험
- 핵심 세일즈포인트·차별점
- Slice research question / observable signal / acceptance
- included scope / explicit non-scope / protected scope

결정에 실질적 대안이 있으면 최소 3개의 materially distinct approach를 비교한다. 조사 순서는 `현재 프로젝트 구현·정본 → 승인 asset/reference → Base reusable evidence → 직접 관련된 검증 사례 → 공식·현업·시장 성공/실패 사례`를 기본으로 하고, 각 후보를 `ADOPT / ADAPT / REJECT`로 판정한다.

이미 승인된 Decision, 저장소에서 확인 가능한 사실, 구현자가 정할 Node/Scene/함수 구조, 가역적 기술 세부, 초기 시험값은 Grill Me로 다시 묻지 않는다.

Exit:

```text
SLICE_PLANNING_LOCKED
```

핵심 player-value trace, 사용자 Decision, scope와 acceptance가 current Project canon에 기록·readback되어야 한다.

### 2단계 — 검수

```text
STAGE_2_PRE_PRODUCTION_REVIEW
PRE_PRODUCTION_REVIEW_CLEAN
PRODUCTION_REQUIREMENTS_LOCKED
NO_ASSET_PRODUCTION_BEFORE_REVIEW_CLEAN
NO_CODEX_PRODUCT_MUTATION_BEFORE_REVIEW_CLEAN
```

1단계에서 새 기능을 계속 늘리지 않고, 고정된 Slice 계약을 적대적으로 검수·축소·교정한다.

필수 검수:

- Project GitHub/Notion/actual implementation drift
- Existing Solution First 누락
- benchmark applicability와 surface-copy 위험
- player choice가 실제 고민인지
- UI/UX 정보 전달과 edge case
- actual consumer / data/state/save/schema 영향
- Visual/Audio/VFX requirement와 실제 소비처
- rights/provenance/release 위험
- implementation acceptance / deterministic QA / runtime QA / evidence ceiling
- protected scope와 rollback

제품 의미를 바꾸는 finding은 1단계로 되돌려 사용자 Decision을 갱신한다. 단순 누락·오류·검증 강화는 2단계 안에서 교정한다.

`PRE_PRODUCTION_REVIEW_CLEAN` 전에는 production asset 제작과 Codex product mutation을 시작하지 않는다.

### 3단계 — 이미지·요소 생성

```text
STAGE_3_ASSET_AND_ELEMENT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
PRODUCTION_INPUTS_BEFORE_CODEX
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

2단계를 통과한 current Slice에 실제 필요한 player-facing/non-code 입력만 제작·정리한다.

포함 후보:

- production Visual/image/animation source asset
- Audio/SFX/music source 또는 승인 procedural spec
- UI source element / icon / font usage record
- VFX presentation requirement/source
- runtime-consumed data/content authored outside Codex product implementation
- provenance/rights/import/format/manifest/durable locator

설명용 시트나 actual consumer 없는 이미지를 production asset으로 만들지 않는다. 현재 대화·Project가 이미지 생성에 별도 명시 승인 Gate를 요구하면 그 Gate가 우선하며, 이 profile은 host/tool confirmation을 우회하지 않는다.

에셋 제작 중 제품 의미가 바뀌면 1단계, requirement/consumer 결함이면 2단계로 되돌린다.

Exit:

```text
WORK_PRODUCTION_INPUT_PACKET_READY
READY_FOR_SINGLE_CODEX_WINDOW
```

### 4단계 — 구현(Codex) + machine closure

```text
STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSURE
CODEX_SINGLE_IMPLEMENTATION_WINDOW
```

Codex는 current Project GitHub·Notion을 fresh-read하고 approved packet을 소비해 actual code·Scene·Resource·runtime wiring·test·build를 구현한다. routine technical choice, reversible refactor, local bug fix, fixture와 QA scenario는 승인 범위 안에서 연속 처리한다.

Codex 반환 뒤 Work가 수행하는 구현 일치·runtime evidence·Visual/Audio consumer·machine QA·canon sync·PR/merge/readback 검수는 별도 macro 6단계가 아니라 Stage 4 closeout이다.

```text
WORK_FINAL_EVIDENCE_REVIEW_IS_STAGE4_CLOSEOUT
WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION
→ actual diff·test·runtime evidence review
→ valid finding correction
→ impact-bounded revalidation
→ GitHub·Notion canon/readback
→ exact-head PR gate·safe merge·new-main readback
→ scope-bounded remaining-work rescan
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

Stage 4 exit:

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

이 상태는 current Slice의 machine-executable required work가 닫힌 **사용자 검증 준비 상태**이며 Vertical Slice 최종 완료가 아니다.

### 5단계 — 사용자 검증

```text
STAGE_5_USER_VALIDATION
ACTUAL_USER_PLAY_REQUIRED
AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE
VERTICAL_SLICE_VALIDATED_COMPLETE_REQUIRES_STAGE5
NEXT_SLICE_REQUIRES_STAGE5_DECISION
```

사용자가 Stage 4 exact build/scene을 실제 플레이한다. 최소한 다음을 분리해 관찰한다.

- 진입·조작 이해
- meaningful choice 인지와 고민
- 피드백·보상·실패 학습 이해
- UI/텍스트/Visual/Audio 가독·지각
- 감정·기억·첫인상
- 핵심 세일즈포인트 전달
- 불편·이탈·혼란·재시도 이유

current vertical-slice Skill의 Decision Gate를 사용한다.

```text
EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP
```

필요하면 `REWORK` 원인을 `FIX / TUNE / REDESIGN`으로 세분한다. `REDESIGN`은 1단계로, requirement/asset/implementation 문제는 영향 범위에 따라 2~4단계로 되돌린다.

`VERTICAL_SLICE_VALIDATED_COMPLETE`는 actual user play evidence와 Decision Gate가 Project canon에 기록·readback된 뒤에만 사용한다. 사용자 검증 전 다음 Slice로 자동 진입하지 않는다.

## 2. Work production-input completion

Codex 전환 기준은 문서량이 아니라 current Slice의 실제 구현 입력 readiness다.

```yaml
WORK_PRODUCTION_INPUT_PACKET:
  project_identity:
  repository:
  slice_id:
  exact_project_baseline:
  player_promise:
  player_action_or_choice:
  meaningful_tradeoff:
  expected_result:
  failure_learning_reward_feedback:
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  planning_and_rules:
  ui_ux_flow:
  data_and_state_contract:
  visual_requirements: []
  approved_visual_assets: []
  audio_requirements: []
  approved_audio_assets_or_procedural_specs: []
  vfx_and_feedback_requirements: []
  localization_and_accessibility_requirements: []
  provenance_and_rights_records: []
  implementation_acceptance: []
  deterministic_test_requirements: []
  runtime_qa_scenarios: []
  build_or_export_checks: []
  required_canon_updates: []
  rollback:
  unresolved_nonblocking: []
  blocking_missing_inputs: []
  evidence_ceiling:
  readiness: READY_FOR_SINGLE_CODEX_WINDOW | BLOCKED_UNVERIFIED
```

Rules:

- current player action→choice→result→feedback에 실제 필요한 input만 준비한다.
- 여러 Slice·장기 roadmap·미래 content를 전환 절감 명목으로 합치지 않는다.
- 승인된 player outcome과 보호 의미를 고정하되 Codex의 Node·함수·Scene 내부 기술 구조를 불필요하게 선행 고정하지 않는다.
- blocking input 하나가 있어도 독립 Work 준비는 계속하고 마지막에 blocking batch를 판정한다.

## 3. Actual in-game Visual, Audio, UI, Data, and VFX

```text
PRODUCTION_INFORMATION != ACTUAL_GAME_INPUT
ACTUAL_CONSUMER_REQUIRED
```

제작자·AI용 설명은 text/table/DB/Flow owner에 둔다. Codex packet의 asset/spec은 concrete game/product consumer가 있어야 한다.

### 3.1 Delegated Visual production

```text
DELEGATED_VISUAL_PRODUCTION_ACTIVE
BOUNDED_VISUAL_PRODUCTION_PACKET_REQUIRED
CURRENT_SLICE_USE_ONLY
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
```

```yaml
VISUAL_PRODUCTION_PACKET:
  requirement_id:
  actual_consumer:
  consumer_surface_and_slot:
  current_art_direction:
  approved_reference_or_style_anchor:
  required_count:
  independent_briefs: []
  format_dimensions_alpha_crop_import:
  protected_identity_and_canon: []
  excluded_scope: []
  objective_acceptance: []
  provenance_and_rights:
  notion_destination:
  repository_or_runtime_destination:
  runtime_validation:
```

명시적 delegation과 완전한 packet이 있으면 current Slice의 생성·선정·revision·허용된 delivery를 per-result 질문 없이 진행할 수 있다. 생성 성공은 project asset approval, runtime consumption, Human/Player PASS가 아니다. upload/attach/readback, import, actual consumer, runtime QA가 별도 필요하다.

Art Direction master, 대표 캐릭터 identity master, 장기 store key art, 권리 불명확 자산, 승인 수량·consumer·Slice를 넘는 batch는 자동 위임 범위가 아니다.

### 3.2 Delegated Audio production

```text
DELEGATED_AUDIO_PRODUCTION_ACTIVE
BOUNDED_AUDIO_PRODUCTION_PACKET_REQUIRED
```

```yaml
AUDIO_PRODUCTION_PACKET:
  cue_id:
  actual_consumer:
  trigger_and_stop_condition:
  information_or_emotion_role:
  existing_approved_asset_or_reuse:
  file_or_approved_procedural_spec:
  format_loop_tail_loudness_priority:
  protected_audio_direction:
  excluded_scope: []
  provenance_and_rights:
  notion_destination:
  repository_or_runtime_destination:
  runtime_validation:
```

Work에 audio binary 제작 capability가 없으면 제작 완료를 추측하지 않는다.

```text
approved project audio
→ reusable rights-verified source
→ zero-incremental-cost rights-verified source
→ approved procedural audio spec legitimately implemented by product code
→ BLOCKED_UNVERIFIED
```

핵심 feedback을 무음·dummy·권리 미확인 자산으로 가린 상태는 shipping-intent readiness가 아니다.

### 3.3 UI·Data·VFX

각 input은 `owner → actual consumer → approved meaning → input/output/state → implementation acceptance → machine QA → evidence ceiling`을 가진다. 목업 존재만으로 runtime UI wiring이나 input semantics를 PASS하지 않는다.

## 4. Delegated routine approval and high-risk deferral

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
BLOCKING_HIGH_RISK_PREVENTS_PHASE_ADVANCE
NO_AUTOMATIC_SCOPE_EXPANSION
```

Auto-approved only inside the current approved Slice:

- existing project identity·Art/Audio Direction 안의 권장 세부안
- tunable default와 safe test range
- bounded actual-consumer Visual/Audio candidate
- 기술 구현 선택·국소 bug fix·reversible refactor
- 누락 test·consumer·reference·small canon sync
- actual evidence가 결정하는 최소 안전 correction
- evidence-equivalent fallback
- current-task branch·PR·exact-head safe merge

다음은 자동 실행하지 않는다.

```text
IRREVERSIBLE_DATA_LOSS
ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION
NEW_PAID_COST
LEGAL_OR_RIGHTS_UNCERTAINTY
PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION
FORCE_DIRECT_MAIN_ADMIN_BYPASS
PROJECT_CORE_IDENTITY_REPLACEMENT
BROAD_ENGINE_OR_SAVE_BREAKING_MIGRATION
```

```text
high-risk finding
→ affected task만 HIGH_RISK_DEFERRED
→ destructive action 금지
→ evidence·rollback·권장안 기록
→ independent ready work 계속
→ 같은 Slice의 high-risk 결정을 한 packet으로 묶음
→ 독립 작업 소진 뒤 사용자에게 한 번만 요청
```

high-risk item이 current Slice acceptance를 차단하면 automated readiness를 주장하지 않는다.

## 5. Stall signal and fallback ladder

```text
STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY
DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK
```

Stall signal은 같은 root-cause 반복, bounded retry/readback 뒤 새 evidence 없음, 진전 identity 없는 외부 대기, output transport 반복 실패, executor 부재, 구조적으로 불가능한 route, stale project/session/head를 포함한다.

```text
current-state readback
→ root-cause classification
→ bounded safe retry
→ authorized fallback A/B
→ evidence-equivalent local/manual route
→ blocked task local defer
→ independent ready tasks continue
→ deferred re-evaluation on new evidence
→ global stop last
```

No infinite retry, source substitution by snippet/memory, permission bypass, new cost, or evidence downgrade. Product executor absence는 product work만 defer하며 Work-owned independent tasks는 계속한다.

## 6. Codex single implementation window

```text
CODEX_SINGLE_IMPLEMENTATION_WINDOW
MINIMIZE_WORK_CODEX_TRANSITIONS
```

Codex는 current Project GitHub·Notion을 fresh-read하고 approved Slice를 연속 실행한다. Routine technical choices, reversible refactors, local bug fixes, fixtures, QA scenarios, canon-resolvable small ambiguity를 하나씩 Work로 되돌리지 않는다.

```yaml
CONSOLIDATED_RETURN_PACKET:
  project:
  slice_id:
  exact_baseline:
  exact_head:
  implementation_completed: []
  files_and_reasons: []
  deterministic_tests_completed: []
  runtime_qa_completed: []
  build_or_export_checks: []
  approved_visuals_consumed: []
  approved_audio_consumed: []
  missing_input_batch: []
  change_proposal_batch: []
  high_risk_deferred_batch: []
  independent_work_remaining: []
  tests_failed: []
  tests_not_run: []
  evidence_locations: []
  evidence_ceiling:
  work_reentry: NONE | FINAL_REVIEW | BLOCKING_INPUT_BATCH | HIGH_RISK_DECISION_BATCH
```

Immediate Work re-entry는 approved alternative가 없는 blocking input batch, project/core meaning replacement, high-risk action, 또는 final evidence review로 제한한다. Missing Visual/Audio는 batch로 모으되 독립 구현·test를 계속하며, player-facing placeholder로 acceptance를 위장하지 않는다.

## 7. Machine QA first; Human QA deferred

```text
MACHINE_QA_FIRST
HUMAN_QA_DEFERRED_BY_CURRENT_USER
GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED
HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED
HERA_PERSISTENT_AUTHORING_FORBIDDEN
HERA_PHASE_SOURCE_DELTA_NONE
EVIDENCE_EQUIVALENT_MACHINE_QA_REQUIRED_WHEN_NOT_ADOPTED
```

Project가 채택한 current authority를 사용한다.

- deterministic domain/state/save/data/UI logic: adopted GUT 또는 current equivalent
- import/parse/headless/runtime/build/export checks as required
- adopted Hera: normal gameplay run/input, runtime state/UI inspection, diagnostics, screenshot와 bounded visual diff
- Hera pre/post tracked source delta: `NONE`

GUT/Hera를 이 profile 존재만으로 자동 설치하지 않는다. 채택되지 않았다면 evidence-equivalent deterministic/runtime route를 사용하며, required equivalent가 없으면 `NOT_RUN`으로 남고 automated readiness를 막는다.

Hera는 Scene/Node/Script/Resource/files를 persistent authoring하지 않고 diagnostic state cheating을 normal-path acceptance로 쓰거나 screenshot diff를 design/readability/fun 승인으로 바꾸지 않는다.

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

사용자가 실제 플레이하기 전까지 유지한다.

```text
GUT PASS != runtime PASS != screen semantics PASS != Human comprehension PASS != Player Experience PASS
```

## 8. Scope-bounded required work zero

```text
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO
COMPLETION_CANDIDATE_RESCAN
```

```yaml
ready_tasks: []
deferred_tasks: []
high_risk_deferred: []
completed_tasks: []
```

```text
ready task execute→verify→correct
→ stall recovery/fallback
→ unresolved task local defer
→ independent work continue
→ deferred re-evaluate
→ remaining machine-executable work recalculate
```

remaining work가 0이 아니면 계속한다. 0이면 actual implementation, planning/canon, Visual/Audio/Data consumers, deterministic tests, runtime/Hera/build evidence, PR/merge/readback, evidence ceiling, high-risk blocker를 다시 스캔한다. valid finding은 remaining work를 다시 연다.

Automated readiness는 missing product implementation, required input/consumer 누락, mandatory machine QA `NOT_RUN`, required merge/readback 누락, high-risk acceptance blocker, unresolved P0/P1 또는 evidence overclaim이 있으면 차단된다.

교정 후 최소 5회 full-scope adversarial loop를 수행하고 `CLEAN_REVIEW_EXIT`까지 계속한다.

모든 machine-executable current-Slice work가 0이고 사용자 play validation만 남으면:

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_QA: DEFERRED_BY_USER
AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE
```

## 9. Safe merge and user validation

current-task PR은 다음을 만족한 뒤에만 routine merge 질문 없이 진행할 수 있다.

```text
latest-main reconciliation
→ exact reviewed HEAD
→ current required checks
→ unresolved thread 0
→ review blocker 0
→ conflict 0
→ protected-scope drift 0
→ high-risk blocker 0
→ repository-supported squash merge
→ new-main readback
→ required GitHub·Notion readback
→ post-merge adversarial review
```

`FORCE_DIRECT_MAIN_ADMIN_BYPASS`는 금지한다. 다른 open/draft/ready PR은 read-only이며 다른 SHA의 PASS를 재사용하지 않는다.

```yaml
USER_VERTICAL_SLICE_VALIDATION_PACKET:
  project:
  slice_id:
  build_or_scene:
  exact_commit_or_build_identity:
  launch_route:
  prerequisites:
  representative_play_window:
  expected_action_choice_result:
  expected_visual_audio_feedback:
  success_markers: []
  known_not_run: []
  evidence_capture:
  feedback_questions: []
  next_decisions: [EXPAND, REWORK, REPEAT_SLICE, HOLD, STOP]
  rework_classification: FIX | TUNE | REDESIGN | NONE
```

```text
ACTUAL_USER_PLAY_REQUIRED
NEXT_SLICE_REQUIRES_STAGE5_DECISION
```

사용자 실제 플레이 전 user validation을 주장하지 않는다. Stage 5 evidence와 Decision Gate를 Project canon에 기록·readback한 뒤에만 `VERTICAL_SLICE_VALIDATED_COMPLETE`를 선언할 수 있다.

## 10. Clean-exit contract

Stage 4 automated readiness clean exit:

```text
explicit delegation evidence exists
current Slice bounded
Work production inputs actual-consumer complete
routine approvals did not expand scope
high-risk actions not executed
Codex one-window implementation completed
all independent work completed before return
stall routes exhausted or locally deferred with evidence
machine-executable required work = 0
GUT/current deterministic tests complete when required
Hera/current live QA complete when required
Hera persistent mutation absent
Hera source delta NONE
runtime/build/readback evidence complete
Human/Player evidence remains NOT_RUN
current-task PR safely merged and read back when applicable
minimum five full adversarial loops complete
blocking finding = 0
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

Final validated Slice completion is a separate Stage 5 receipt:

```text
ACTUAL_USER_PLAY_REQUIRED
user validation evidence recorded and read back
Decision Gate recorded: EXPAND | REWORK | REPEAT_SLICE | HOLD | STOP
NEXT_SLICE_REQUIRES_STAGE5_DECISION
VERTICAL_SLICE_VALIDATED_COMPLETE
```
