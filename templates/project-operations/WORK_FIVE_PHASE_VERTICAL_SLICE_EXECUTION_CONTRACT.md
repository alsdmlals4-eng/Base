# Work 5단계 버티컬 슬라이스 실행 계약
> 이 문서는 사용자에게 보이는 5단계 lifecycle의 **순서·입력·출력·진입/종료·재진입·완료·프로젝트 매핑**만 소유한다. 세부 기획, Grill Me, Visual, Codex, QA, Git, IRG, Vertical Slice 알고리즘은 현재 owner에 위임한다.
```text
FIVE_PHASE_VERTICAL_SLICE_EXECUTION
FIVE_PHASE_TRANSITION_GATE_REQUIRED
THIN_PHASE_INTERFACE_NOT_SECOND_CANON
DETAILED_ALGORITHMS_DELEGATED_TO_CURRENT_OWNERS
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
CURRENT_OWNER_DETAILS_WIN_ON_DRIFT
CURRENT_APPROVED_SLICE_ONLY
NO_AUTOMATIC_SCOPE_EXPANSION
NO_AUTOMATIC_NEXT_SLICE_BEFORE_USER_DECISION
```

## 0. 현재 owner 조합
- 시작 정본·핵심 재미·시스템·SWOT·작업순서: `WORK_PROJECT_START_CANON_CHECKLIST.md`
- 기획 우선·Grill Me: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Grill Me 질문: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- packet·승인·Codex·QA·Git closeout: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- 로컬 Visual: `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
- evidence identity: `WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`
- Vertical Slice 품질·play evidence: `skills/designing-vertical-slices/SKILL.md`
- 실제 프로젝트 대조 사례: `docs/knowledge/cases/WORK_FIVE_PHASE_VERTICAL_SLICE_PROJECT_CANON_CASE.md`
```text
PHASE_1_PLANNING_CO_DESIGN
→ PHASE_2_PREPRODUCTION_REVIEW
→ PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
→ PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ PHASE_5_USER_VERTICAL_SLICE_VALIDATION
```
각 phase는 산출물과 exit Gate를 실제 readback해야 한다.

## 1. PHASE_1_PLANNING_CO_DESIGN — 기획·사용자 공동설계
```text
CORE_PLANNING_CO_DESIGN_REQUIRED
GRILL_ME_FOR_UNRESOLVED_CORE_PRODUCT_MEANING
DELEGATED_ROUTINE_APPROVAL_IS_NOT_CORE_PRODUCT_MEANING_APPROVAL
EXISTING_CONFIRMED_DECISION_REUSE_NO_REASK
REUSE_FIRST_PREFLIGHT_REQUIRED
MARKET_SUCCESS_FAILURE_COMPARISON
MINIMUM_VIABLE_ALTERNATIVES: 3
ADOPT / ADAPT / REJECT
```
새 core identity·핵심 재미·Core Loop·핵심 시스템·주요 UX/경제/서사/Art Direction·차별점·Slice 가설은 current Project canon과 actual implementation을 먼저 확인한 뒤 사용자와 결정한다. 유효한 approval_ref와 confirmed Decision은 다시 묻지 않는다.
중요 결정은 current project/승인 자료/Base reuse/공식·현업·성공·실패 사례를 조사하고 `facts / player reports / inference`를 구분한다. materially distinct한 최소 3개 대안과 권장안·비용·위험·rollback을 준비한 뒤, 저장소로 답할 수 없는 결정만 Grill Me로 한 번에 하나씩 묻는다.
```text
DELEGATED_ROUTINE_APPROVAL
!= CORE_PRODUCT_MEANING_APPROVAL
```
```yaml
CORE_PLANNING_DECISION_PACKET:
  project_goal:
  player_promise:
  pointed_fun:
  core_loop:
  session_loop:
  progression_or_meta_loop:
  core_systems: []
  supporting_systems: []
  meaningful_choices: []
  reward_and_failure_learning:
  emotional_target:
  first_session_memory:
  differentiation_and_sales_points: []
  protected_strengths: []
  approved_scope: []
  explicit_non_scope: []
  vertical_slice_hypotheses:
    fun:
    production:
    technical:
  benchmark_and_trade_study:
  confirmed_decisions: []
  unresolved_core_decisions: []
  result: PHASE_1_USER_CONFIRMED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```
Exit:
```text
PHASE_1_USER_CONFIRMED
+ unresolved_core_decisions = 0
+ current canon readback
```

## 2. PHASE_2_PREPRODUCTION_REVIEW — 구현 전 검수
> Phase 2는 구현 전 검수다. Codex 결과의 actual diff/runtime 검수는 Phase 4에 속한다.
```text
NO_SERIAL_ELEMENT_PRODUCTION_BEFORE_PHASE_2_PASS
NO_CODEX_IMPLEMENTATION_BEFORE_PHASE_3_READY
CORE_MEANING_FINDING_REOPENS_PHASE_1
```
Phase 1 packet을 핵심 재미·선택·보상, 대표성·scope, reuse, `implementation_feasibility`, UI/UX, data/save/economy, `actual_consumer_and_asset_coverage`, 권리·비용, `acceptance_test_runtime_and_rollback`, `work_codex_transition_cost`, untouched consumer·canon drift 관점으로 전체 검수한다. 최소 5회 full-scope 적대검토와 IRG를 통과한다.
```yaml
REVIEWED_SLICE_PRODUCTION_CONTRACT:
  phase_1_packet_identity:
  approved_player_outcome:
  reviewed_scope: []
  explicit_non_scope: []
  protected_scope: []
  system_and_data_contract:
  ui_ux_flow:
  actual_consumers: []
  required_visual_audio_ui_data_vfx: []
  acceptance_criteria: []
  machine_qa_plan: []
  human_or_player_questions: []
  rollback:
  remaining_findings: []
  result: APPROVED_FOR_INGAME_ELEMENT_PRODUCTION | REOPEN_PHASE_1 | BLOCKED_UNVERIFIED
```
Exit:
```text
APPROVED_FOR_INGAME_ELEMENT_PRODUCTION
+ blocking finding = 0
```
Core meaning finding은 `CORE_MEANING_FINDING_REOPENS_PHASE_1`; 그 밖의 유효 finding은 최소 교정 후 Phase 2를 다시 검수한다.

## 3. PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION — 이미지·요소 생성
```text
WORK_PREP_COMPLETION_BEFORE_CODEX
ACTUAL_CONSUMER_REQUIRED
PRODUCTION_INFORMATION != ACTUAL_GAME_INPUT
```
Work가 Codex 전환 전에 실제 consumer가 있는 `Visual`, `Audio`, `UI/UX`, `Data`, `VFX`, `localization_accessibility`, `provenance_and_rights`, Acceptance와 QA 입력을 한 번에 닫는다.
로컬 Visual 세부는 `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`를 따른다.
```text
project-local candidate
→ PROJECT_ASSET_APPROVED
→ project-owned tracked asset
→ ASSET_MANIFEST
→ commit/push
→ remote HEAD readback
→ Codex project-relative locator
```
```text
LOCAL_VISUAL_CANDIDATE
!= PROJECT_ASSET_APPROVED
!= RUNTIME_PROMOTED
```
```yaml
PHASE_3_INPUT_COMPLETION:
  reviewed_slice_contract:
  planning_and_rules:
  ui_ux_flow:
  data_and_state_contract:
  approved_visual_assets: []
  approved_audio_assets_or_procedural_specs: []
  vfx_and_feedback_requirements: []
  localization_accessibility:
  provenance_and_rights_records: []
  deterministic_test_requirements: []
  runtime_qa_scenarios: []
  build_or_export_checks: []
  codex_readable_project_relative_locators: []
  exact_commit_or_artifact:
  blocking_missing_inputs: []
  result: READY_FOR_SINGLE_CODEX_WINDOW | BLOCKED_UNVERIFIED
```
Output/Exit:
```text
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

## 4. PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT — 구현·자동 검증
```text
CODEX_SINGLE_IMPLEMENTATION_WINDOW
MINIMIZE_WORK_CODEX_TRANSITIONS
WORK_FINAL_IMPLEMENTATION_EVIDENCE_REVIEW
```
Codex는 Phase 3 packet을 fresh-read하고 `actual code / Scene / Resource / runtime wiring`을 구현한다. 승인 범위의 국소 기술 finding은 한 window에서 처리하고 통합 반환한다.
```text
deterministic / import / parse / runtime / build QA
→ GUT / Hera / evidence-equivalent machine QA
→ Work actual diff/evidence review
→ valid finding correction
→ exact-head CI
→ safe merge
→ post-merge readback
```
Phase 4 완료에는 `USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED`, exact build identity, representative flow smoke, release-near/shipping-intent UI·Visual·Audio·VFX·feedback, `NO_CRITICAL_PLAYER_FACING_PLACEHOLDER`, machine-executable work 0이 필요하다.
```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
AUTOMATED_VERTICAL_SLICE_READY_IS_PHASE_4_ONLY
AUTOMATED_VERTICAL_SLICE_READY != USER_VALIDATED_VERTICAL_SLICE
```
```yaml
PHASE_4_COMPLETION:
  actual_implementation:
  machine_qa:
  work_final_review:
  exact_head_ci:
  merge_and_readback:
  downloadable_build:
  representative_flow_smoke:
  remaining_machine_executable_work: 0
  HUMAN_USABILITY_EVIDENCE: NOT_RUN
  PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
  WHOLE_GAME_COMPLETE: false
  RELEASE_READY: false
  result: AUTOMATED_VERTICAL_SLICE_READY | BLOCKED_UNVERIFIED
```

## 5. PHASE_5_USER_VERTICAL_SLICE_VALIDATION — 사용자 실제 검증
```text
USER_ACTUALLY_PLAYS_EXACT_BUILD
HUMAN_PLAYER_EVIDENCE_CANNOT_BE_AUTOMATED
NO_AUTOMATIC_NEXT_SLICE_BEFORE_USER_DECISION
```
사용자가 Phase 4 exact build를 실제 실행하고 `representative action → choice → result → feedback`, 목표·다음 행동, 조작·가독성, 보상·실패 학습, 감정·기억·차별점을 검증한다.
```yaml
USER_VERTICAL_SLICE_VALIDATION_PACKET:
  project:
  slice_id:
  exact_commit_or_build_identity:
  download_or_launch_route:
  representative_play_window:
  representative action → choice → result → feedback:
  expected_visual_audio_ui_feedback:
  success_markers: []
  observation_questions:
  evidence_capture:
  known_not_run: []
```
판정:
```text
USER_VALIDATED_VERTICAL_SLICE_PASS
USER_VALIDATED_WITH_FOLLOWUP
REWORK_REQUIRED
BLOCKED_USER_VALIDATION
```
최종 상태:
```text
USER_VALIDATED_VERTICAL_SLICE
CANONICAL_REFLECTION_AFTER_PLAY
```
`USER_VALIDATED_VERTICAL_SLICE`는 actual user play, representative flow, blocking usability 처리, 핵심 경험 방향 판단, feedback 기록과 필요한 canon readback을 요구한다. 이는 전체 콘텐츠·모든 플랫폼·최종 밸런스·모든 언어·store/legal/release 완료가 아니다.

## 6. 사용자 evidence 기반 bounded reopen
```text
BOUNDED_PHASE_REOPEN_FROM_USER_EVIDENCE
EARLIEST_AFFECTED_PHASE_REOPENS
NO_FULL_PROJECT_RESTART_FOR_LOCAL_FINDING
```
```text
core meaning / promise / core system → PHASE_1_PLANNING_CO_DESIGN
design / readability / flow / balance intent → PHASE_2_PREPRODUCTION_REVIEW
missing or unsuitable Visual / Audio / UI copy / data input → PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
bug / wiring / runtime / build / performance → PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
```
가장 이른 영향 phase만 열고 downstream evidence를 영향 범위만큼 재검증한다.

## 7. 프로젝트 native state 매핑
```text
FIVE_PHASE_PROJECT_MAPPING
PROJECT_PHASE_DRIFT_CORRECTION_REQUIRED
PROJECT_NATIVE_STATE_PRESERVED
NO_PROJECT_STATE_MASS_RENAME_OR_NOTION_REMIGRATION
```
```yaml
FIVE_PHASE_PROJECT_MAPPING:
  project_native_state:
  phase_1_planning:
  phase_2_review:
  phase_3_element_production:
  phase_4_implementation:
  phase_5_user_validation:
  current_phase:
  mapping_evidence:
  ambiguity_or_drift:
  current_owner_to_correct:
  result: MAPPED | CORRECTION_REQUIRED | BLOCKED_UNVERIFIED
```
Project의 PLAN/BUILD/REVIEW, Task, Decision, candidate, Human gate를 rename하지 않는다. current meaning을 매핑하고 stale current stage·next gate·evidence ceiling만 실제 owner에서 bounded correction/readback한다.

## 8. Domain adaptation·승인·완료
```text
DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE
NON_GAME_PROJECT_GODOT_EVIDENCE_NOT_APPLICABLE
```
비게임 프로젝트는 Phase 3·4를 `domain production`에 맞게 적용하고 Godot/runtime 필드는 `NOT_APPLICABLE`로 둔다.
Routine 자동 승인은 기존 approved Slice의 가역 세부·요소 제작·bug fix·Git closeout에만 적용한다. 새 core meaning, scope 확대, 파괴적 변경, 비용·권한·권리 불확실성·공개 배포는 사용자 결정이다.
```yaml
FIVE_PHASE_COMPLETION_EVIDENCE:
  phase_1_packet:
  phase_1_user_confirmation:
  phase_2_review_contract:
  phase_3_work_input_packet:
  phase_4_implementation_and_machine_evidence:
  phase_4_exact_build:
  phase_4_merge_readback:
  phase_5_user_validation_packet:
  phase_5_actual_user_evidence:
  final_state:
  reopened_phase_history: []
  remaining_machine_executable_work:
  remaining_user_validation_work:
  HUMAN_USABILITY_EVIDENCE:
  PLAYER_EXPERIENCE_EVIDENCE:
  blockers: []
```
```text
planning text exists
!= user-confirmed core design
!= preproduction review PASS
!= product input ready
!= Codex implementation
!= machine runtime/build PASS
!= user actually played
!= USER_VALIDATED_VERTICAL_SLICE
```
`remaining work = 0`은 completion candidate다. current phase의 actual-state rescan과 최소 5회 full-scope 적대검토 후 blocking finding 0에서만 닫는다. Phase 5 판정 뒤에도 다음 Slice는 사용자 결정 전 자동 시작하지 않는다.
