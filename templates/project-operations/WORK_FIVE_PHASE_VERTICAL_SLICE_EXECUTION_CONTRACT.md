# Work 5단계 버티컬 슬라이스 실행 계약

> 이 문서는 사용자가 이해하고 조정하기 쉬운 **5단계 실행 인터페이스**를 소유한다. 기존 Base·Project의 상세 기획, Grill Me, Visual, Codex, QA, Git, IRG, Vertical Slice owner를 복제하거나 대체하지 않는다.

```text
FIVE_PHASE_VERTICAL_SLICE_EXECUTION
FIVE_PHASE_TRANSITION_GATE_REQUIRED
THIN_PHASE_INTERFACE_NOT_SECOND_CANON
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
CURRENT_OWNER_DETAILS_WIN_ON_DRIFT
CURRENT_APPROVED_SLICE_ONLY
NO_AUTOMATIC_SCOPE_EXPANSION
```

## 0. 현재 상세 owner 조합

다음 owner를 current Base latest completed main과 exact Project canon에서 fresh-read한다.

- 시작 정본 확인·선교정: `WORK_PROJECT_START_CANON_CHECKLIST.md`
- 기획 우선·Grill Me: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Grill Me 인터뷰: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- Work↔Codex 최소 전환·packet·QA·merge: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- 프로젝트 로컬 Visual binary: `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
- 실행 evidence identity: `WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`
- 버티컬 슬라이스 품질·play evidence: `skills/designing-vertical-slices/SKILL.md`

관련 프로젝트 감사 사례:

`docs/knowledge/cases/WORK_FIVE_PHASE_VERTICAL_SLICE_PROJECT_CANON_CASE.md`

```text
PHASE_1_PLANNING_CO_DESIGN
→ PHASE_2_PREPRODUCTION_REVIEW
→ PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
→ PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ PHASE_5_USER_VERTICAL_SLICE_VALIDATION
```

한 단계의 문서가 있다는 사실은 다음 단계 진입 증거가 아니다. 각 phase output과 transition Gate를 실제 readback한다.

---

# 1. PHASE_1_PLANNING_CO_DESIGN — 기획·사용자 공동설계

```text
CORE_PLANNING_CO_DESIGN_REQUIRED
GRILL_ME_FOR_UNRESOLVED_CORE_PRODUCT_MEANING
DELEGATED_ROUTINE_APPROVAL_IS_NOT_CORE_PRODUCT_MEANING_APPROVAL
EXISTING_CONFIRMED_DECISION_REUSE_NO_REASK
```

## 1.1 언제 사용자와 함께 기획하는가

다음이 새로 정해지거나 current canon끼리 충돌하면 Phase 1 사용자 결정 범위다.

- 프로젝트 goal·player fantasy·player promise
- pointed fun·Core Loop·핵심 시스템
- meaningful choice·tension·trade-off
- 주요 UX·경제·보상·실패 의미
- 핵심 서사·세계관·Art Direction
- MVP·Playable Slice 범위·명시적 non-scope
- 차별점·sales point
- Vertical Slice가 검증할 가장 위험한 fun·production·technical hypothesis

이미 current owner에 승인된 Decision이 있고 전제가 유지되면 다시 묻지 않는다. 저장소·Notion·실제 구현으로 답할 수 있는 사실, 가역 기술값, 내부 Node/함수 구조는 Grill Me 질문이 아니다.

```text
DELEGATED_ROUTINE_APPROVAL
!= CORE_PRODUCT_MEANING_APPROVAL
```

routine 권장안 자동 승인은 기존 승인된 제품 의미 안의 세부 실행권이다. 새 핵심 재미·Core Loop·핵심 시스템·주요 UX·경제·서사·Art Direction을 자동 확정하는 권한이 아니다.

## 1.2 질문 전 실제 조사

```text
Project GitHub·Notion·actual implementation fresh-read
→ 기존 confirmed Decision·same-goal PR·runtime evidence
→ REUSE_FIRST_PREFLIGHT_REQUIRED
→ decision-relevant benchmark
→ Grill Me 필요성 판정
```

중요 결정에는 다음을 수행한다.

```text
MARKET_SUCCESS_FAILURE_COMPARISON
MINIMUM_VIABLE_ALTERNATIVES: 3
ADOPT / ADAPT / REJECT
```

- current project existing solution과 승인 Asset/Reference를 먼저 본다.
- 성공·실패·혼합 사례와 공식·현업 근거를 함께 본다.
- 인기 지표를 성공 원인의 단독 증거로 사용하지 않는다.
- `facts / player reports / inference`를 구분한다.
- 허수 대안으로 3개를 채우지 않는다.
- 새 evidence가 생기면 better-alternative와 long-term fit을 다시 검토한다.

## 1.3 Grill Me 방식

실질 사용자 결정이 남으면 한 메시지에 하나의 결정만 묻는다.

```text
current canon과 기존 Decision
→ 새 사실·충돌
→ 최소 3개 유효 대안
→ player value·제작비·장기 유지비·rollback
→ GPT 권장안
→ 선택 시 확정되는 owner·범위·후속 영향
```

사용자가 답하면 같은 승인 단위에서 Decision·GitHub structured canon·Notion human canon을 동기화하고 readback한 뒤 다음 질문 필요성을 재평가한다.

## 1.4 Phase 1 출력

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
  evidence_ceiling:
  result: PHASE_1_USER_CONFIRMED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```

Phase 1 통과:

```text
PHASE_1_USER_CONFIRMED
+ unresolved_core_decisions = 0
+ current canon readback
```

---

# 2. PHASE_2_PREPRODUCTION_REVIEW — 구현 전 검수

> 이 단계의 `검수`는 **Codex 구현 전에 기획·범위·제작 입력을 검증하는 것**이다. Codex 결과의 실제 diff·runtime 검수는 Phase 4 closeout에 속한다.

```text
PHASE_2_PREPRODUCTION_REVIEW
NO_SERIAL_ELEMENT_PRODUCTION_BEFORE_PHASE_2_PASS
NO_CODEX_IMPLEMENTATION_BEFORE_PHASE_3_READY
CORE_MEANING_FINDING_REOPENS_PHASE_1
```

## 2.1 전체 검수 축

Phase 1 packet을 다음 관점으로 전체 재공격한다.

```yaml
PREPRODUCTION_REVIEW:
  core_fun_choice_reward_alignment:
  slice_representativeness_and_scope:
  existing_solution_and_reuse:
  implementation_feasibility:
  ui_ux_information_and_decision_comprehension:
  data_state_save_schema_economy_balance:
  actual_consumer_and_asset_coverage:
  visual_audio_vfx_feedback_quality_bar:
  localization_accessibility:
  provenance_rights_cost_security:
  acceptance_test_runtime_and_rollback:
  work_codex_transition_cost:
  untouched_consumers_and_canon_drift:
  adversarial_findings: []
  result: PASS | REOPEN_PHASE_1 | BLOCKED_UNVERIFIED
```

검수 질문:

- 플레이어 약속→행동→의미 있는 선택→결과→보상/실패 학습이 연결되는가?
- 이 Slice가 핵심 재미와 대표 세일즈포인트를 실제로 보여주는가?
- 더 작은 범위로 같은 검증 목적을 달성할 수 있는가?
- 이미 구현·승인된 해법을 재사용할 수 있는가?
- UI·Data·Visual·Audio·VFX가 실제 consumer와 연결되는가?
- 권리·비용·save/schema·platform 위험이 숨겨졌는가?
- Acceptance와 runtime evidence가 관찰 가능하게 정의됐는가?
- Codex가 Work로 반복 왕복하게 만들 blocking input이 남았는가?

## 2.2 finding 처리

```text
core meaning / promise / core system finding
→ CORE_MEANING_FINDING_REOPENS_PHASE_1

implementation feasibility / flow / asset requirement finding
→ Phase 2에서 최소 안전 교정
→ review rerun
```

Phase 2 전에는 serial 이미지·사운드·UI asset production을 시작하지 않는다. 탐색용 draft는 product input으로 승격하지 않는다.

## 2.3 Phase 2 출력

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

Phase 2 통과:

```text
APPROVED_FOR_INGAME_ELEMENT_PRODUCTION
+ blocking finding = 0
```

---

# 3. PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION — 이미지·요소 생성

```text
PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
WORK_PREP_COMPLETION_BEFORE_CODEX
ACTUAL_CONSUMER_REQUIRED
PRODUCTION_INFORMATION != ACTUAL_GAME_INPUT
```

Work가 current Slice에서 담당 가능한 구현 입력을 Codex 전환 전에 한 번에 닫는다.

## 3.1 제작 범위

- `Visual`: character/environment/sprite/HUD/icon/VFX texture 등 actual consumer가 있는 결과
- `Audio`: music/SFX/UI cue 또는 권리 검증된 source·구현 가능한 procedural spec
- `UI/UX`: screen flow, state family, copy, focus/input, empty/error/loading
- `Data`: schema, state, input/output, tunable default/range
- `VFX`: trigger, semantic role, timing, priority, accessibility alternative
- `localization_accessibility`: string/font/layout/input/readability readiness
- `provenance_and_rights`: source·rights·version·approval·product consumption identity
- deterministic/runtime/build/Hera scenario와 expected evidence

제작자·AI가 이해하는 설명은 text/table/DB/Flow를 우선한다. 실제 game input은 concrete consumer·format·path·acceptance가 있어야 한다.

## 3.2 로컬 Visual route

explicit local Visual profile에서는 상세 owner인 `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`를 따른다.

```text
Notion Visual 구조·Art Direction fresh-read
→ exact project-local candidate
→ format/dimensions/SHA-256/provenance/rights readback
→ PROJECT_ASSET_APPROVED
→ project-owned tracked asset
→ ASSET_MANIFEST
→ feature-branch commit/push
→ remote HEAD readback
→ Codex project-relative locator
```

Notion binary upload는 explicit project policy가 요구하지 않으면 필수가 아니다. Notion human-facing text·상태를 실제로 변경했으면 해당 destination readback은 유지한다.

```text
LOCAL_VISUAL_CANDIDATE
!= PROJECT_ASSET_APPROVED
!= RUNTIME_PROMOTED
```

## 3.3 Phase 3 출력

기존 상세 packet owner를 재사용한다.

```text
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

최소 포함:

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

Phase 3 통과 전 Codex를 시작하지 않는다. 단, 실제 executor 부재와 무관하게 Work-owned 독립 입력은 끝까지 준비한다.

---

# 4. PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT — 구현·자동 검증

```text
PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
CODEX_SINGLE_IMPLEMENTATION_WINDOW
MINIMIZE_WORK_CODEX_TRANSITIONS
WORK_FINAL_IMPLEMENTATION_EVIDENCE_REVIEW
```

## 4.1 Codex 실행

Codex는 exact Project GitHub·Notion·Phase 3 packet을 fresh-read한다.

```text
actual code / Scene / Resource / runtime wiring
→ approved-scope bug fix / reversible refactor
→ deterministic / import / parse / runtime / build QA
→ GUT / Hera / evidence-equivalent machine QA
→ CONSOLIDATED_RETURN_PACKET
```

작은 기술 선택과 국소 finding을 한 건씩 Work로 돌려보내지 않는다. Core meaning·고위험 action·대체 불가능한 blocking input만 즉시 re-entry한다.

## 4.2 Work 최종 구현검수

Codex가 구현했다고 주장한 내용이 아니라 실제 diff·test·runtime·build evidence를 검수한다.

```text
CONSOLIDATED_RETURN_PACKET
→ actual changed paths / consumers
→ acceptance trace
→ failed / not-run evidence
→ valid finding correction
→ impact-bounded revalidation
→ exact-head CI
→ safe merge
→ post-merge readback
→ scope-bounded remaining machine work rescan
```

Hera를 채택한 프로젝트에서 Hera는 live QA·관찰·입력·화면 증거만 담당하고 persistent source writer가 아니다.

## 4.3 사용자 실행 산출물

```text
USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED
NO_CRITICAL_PLAYER_FACING_PLACEHOLDER
```

Phase 4 완료에는 current Slice가 약속한 대표 흐름을 실제로 실행할 수 있는 exact build/scene이 필요하다.

- exact commit/build identity
- executable + required data/package
- clean extract/launch smoke when build artifact exists
- representative flow entry
- current Slice에 필요한 shipping-intent UI/Visual/Audio/VFX/feedback
- player-facing 핵심 placeholder·dummy·무음으로 acceptance를 꾸미지 않음
- SHA-256 또는 동등 artifact identity
- launch route와 validation packet

## 4.4 Phase 4 상태

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

Phase 4 완료는 최종 Vertical Slice 완료가 아니다. 사용자 실제 플레이가 남아 있다.

---

# 5. PHASE_5_USER_VERTICAL_SLICE_VALIDATION — 사용자 실제 검증

```text
PHASE_5_USER_VERTICAL_SLICE_VALIDATION
USER_ACTUALLY_PLAYS_EXACT_BUILD
HUMAN_PLAYER_EVIDENCE_CANNOT_BE_AUTOMATED
```

사용자는 Phase 4에서 전달된 exact build를 실제로 실행한다.

```yaml
USER_VERTICAL_SLICE_VALIDATION_PACKET:
  project:
  slice_id:
  exact_commit_or_build_identity:
  download_or_launch_route:
  prerequisites:
  representative_play_window:
  representative action → choice → result → feedback:
  expected_visual_audio_ui_feedback:
  success_markers: []
  observation_questions:
    goal_and_next_action:
    core_action_and_choice:
    result_reward_failure_learning:
    readability_and_feedback:
    controls_and_fatigue:
    emotion_memory_and_differentiation:
  evidence_capture:
  known_not_run: []
```

## 5.1 판정

```text
USER_VALIDATED_VERTICAL_SLICE_PASS
USER_VALIDATED_WITH_FOLLOWUP
REWORK_REQUIRED
BLOCKED_USER_VALIDATION
```

- `USER_VALIDATED_VERTICAL_SLICE_PASS`: current Slice의 대표 경험과 품질 방향을 사용자가 승인하고 blocking finding이 없다.
- `USER_VALIDATED_WITH_FOLLOWUP`: 대표 경험은 승인하지만 비차단 polish/tuning follow-up이 있다.
- `REWORK_REQUIRED`: blocking usability, 핵심 경험, asset, runtime 문제가 있어 이전 phase를 다시 연다.
- `BLOCKED_USER_VALIDATION`: build/access/environment 문제로 실제 검증하지 못했다.

## 5.2 최종 상태

```text
USER_VALIDATED_VERTICAL_SLICE
CANONICAL_REFLECTION_AFTER_PLAY
```

`USER_VALIDATED_VERTICAL_SLICE`는 다음을 요구한다.

- exact build 실제 사용자 실행
- representative action→choice→result→feedback 완료
- blocking usability finding 0 또는 명시적 rework 판정 후 재검증
- 핵심 재미·감정·기억·차별점의 방향성에 대한 사용자 판단
- 관찰·feedback·decision 기록
- 실제 finding에 따른 정본·구현 교정
- repository structured truth와 Notion human truth의 필요한 Canonical Reflection After Play·readback

전체 게임 콘텐츠·모든 플랫폼·최종 밸런스·모든 언어·store/legal/release PASS는 이 상태의 자동 포함 조건이 아니다.

---

# 6. 사용자 evidence 기반 bounded reopen

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

Phase 5 finding을 문서 전체 재작성으로 처리하지 않는다. 가장 이른 영향 phase만 열고 downstream evidence를 영향 범위만큼 재검증한다.

---

# 7. 프로젝트 고유 상태 매핑·정본 교정

```text
FIVE_PHASE_PROJECT_MAPPING
PROJECT_PHASE_DRIFT_CORRECTION_REQUIRED
PROJECT_NATIVE_STATE_PRESERVED
NO_PROJECT_STATE_MASS_RENAME_OR_NOTION_REMIGRATION
```

프로젝트는 `PLAN / BUILD / REVIEW`, Task, Decision, DoR, package candidate, Human gate 같은 고유 상태를 계속 소유할 수 있다. Base 5단계 interface는 이를 교체하지 않고 현재 의미를 매핑한다.

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

작업 시작 시:

```text
Project AGENTS / Active Context / current Decision / Notion / actual implementation
→ native state 의미 복원
→ five-phase mapping
→ 같은 상태가 서로 다른 phase를 주장하는가?
→ stale next gate·완료 상태·evidence ceiling 교정
→ exact destination readback
→ current work 진입
```

고유 역사 receipt와 Decision ID를 일괄 rename하지 않는다. 검증된 Notion IA도 5단계 표기 통일만을 위해 remigration하지 않는다. 사람용 current state에서 오해가 실제 발생할 때만 bounded correction한다.

---

# 8. Domain adaptation

```text
DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE
NON_GAME_PROJECT_GODOT_EVIDENCE_NOT_APPLICABLE
```

게임 프로젝트는 Phase 3의 product inputs와 Phase 4의 engine/runtime/build를 사용한다.

소설·문서·TRPG 등 non-game 프로젝트는 같은 의도를 domain production에 맞게 적용한다.

```text
기획 공동설계
→ production 전 검수
→ 원고·데이터·표지·편집요소 준비
→ domain production / 검사 / 발행 후보 closeout
→ 사용자 독해·사용 검증
```

Godot·Scene·runtime/build 필드가 해당되지 않으면 `NOT_APPLICABLE`로 둔다. 비게임 프로젝트에 엔진 설치·Godot 증거를 강제하지 않는다.

---

# 9. 자동 승인·중단 경계

Phase 1 핵심 제품 의미를 제외한 current approved Slice의 routine 기술·가역 세부는 standing delegation으로 진행할 수 있다.

자동 계속:

- 정본과 실제 구현이 결정하는 안전한 기술 세부
- tunable default와 test range
- Phase 2에서 승인된 actual-consumer input 제작
- 국소 bug fix·reversible refactor·test 보완
- current-task Git closeout
- evidence-equivalent fallback

사용자 결정:

- 새 core identity·core fun·Core Loop·핵심 시스템 의미
- 주요 UX·경제·보상·서사·Art Direction
- Slice 범위 확대
- 파괴적 migration·삭제
- 새 비용·권한·권리 불확실성·공개 배포

이미 승인된 Phase 1 Decision은 다시 묻지 않는다.

---

# 10. 최적화·전환 최소화

```text
Phase 1의 핵심 결정 batch를 확정·readback
→ Phase 2에서 한 번의 substantive review package
→ Phase 3에서 Work input batch 완료
→ Phase 4에서 one Codex implementation window
→ Phase 5에서 one user validation packet
```

- 각 phase의 blocking finding만 upstream으로 돌린다.
- 같은 evidence를 Base/GitHub/Notion에서 반복해 검증 횟수로 세지 않는다.
- 완료된 phase는 source·scope·new evidence가 바뀌지 않으면 재실행하지 않는다.
- Work transcript를 phase 정본으로 사용하지 않는다.
- durable checkpoint와 project owner가 새 Work를 재수화한다.

---

# 11. 완료 증거

```yaml
FIVE_PHASE_COMPLETION_EVIDENCE:
  project:
  slice_id:
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
Phase 1 PASS
+ Phase 2 PASS
+ Phase 3 PASS
+ Phase 4 AUTOMATED_VERTICAL_SLICE_READY
+ Phase 5 USER_VALIDATED_VERTICAL_SLICE_PASS or USER_VALIDATED_WITH_FOLLOWUP
→ USER_VALIDATED_VERTICAL_SLICE
```

`remaining work = 0`은 completion candidate다. actual-state rescan과 최소 5회 full-scope adversarial review 뒤 blocking finding 0에서만 해당 phase를 닫는다.

---

# 12. Evidence ceiling

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

Phase 4까지:

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

Phase 5에서 실제 관찰한 범위만 PASS로 올린다. 한 명의 사용자 검증은 현재 Slice의 사용자 방향 판정이며 시장 적합성·장기 유지율·전체 목표 플레이어 표본을 증명하지 않는다.

---

# 13. Rollback

이 interface가 잘못된 경우:

```text
implementation squash commit revert
→ Router/Starter의 five-phase owner link 제거
→ focused/core regression
→ 기존 minimum-transition profile과 project-native states readback
```

기존 Project Decision·Task·Notion IA·Visual asset·제품 구현은 이 interface rollback 때문에 자동 변경하지 않는다.
