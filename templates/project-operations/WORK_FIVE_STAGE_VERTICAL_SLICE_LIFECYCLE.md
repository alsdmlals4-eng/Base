# Work 게임 프로젝트 5단계 버티컬 슬라이스 Lifecycle

> 게임 제품의 Work 실행을 사용자가 이해하고 AI가 기계적으로 판정할 수 있는 다섯 단계로 고정하는 얇은 lifecycle owner다. 세부 절차는 기존 Startup Checklist, Grill Me, minimum-transition, Visual/Audio, Codex, IRG, Git·CI·QA owner가 계속 소유한다.

```text
GAME_PRODUCT_FIVE_STAGE_LIFECYCLE_ONLY
NON_GAME_PROJECT_REQUIRES_PROJECT_SPECIFIC_ADAPTER
FIVE_STAGE_LIFECYCLE_IS_PUBLIC_WORK_SEQUENCE
EXISTING_WORK_MODES_AND_PROFILES_ARE_INTERNAL_OWNER_MAPPING
THIN_LIFECYCLE_NOT_SECOND_CANON
CURRENT_PROJECT_AND_BASE_OWNER_WIN_ON_DRIFT
```

## 0. 적용과 권위

적용 대상:

- 실제 게임 product implementation이 존재하거나 예정된 프로젝트
- Playable Vertical Slice를 Work→Codex→사용자 검증으로 닫는 작업

비게임 프로젝트에는 자동 적용하지 않는다. 소설·문서·도구 프로젝트는 current Project lifecycle을 유지하거나 별도 adapter를 명시적으로 채택한다.

권위:

```text
사용자의 최신 명시 지시
→ Project AGENTS / Active Context / 승인 Decision
→ Project GitHub·Notion current canon
→ actual code/data/Scene/Resource/asset/test/runtime
→ current Base owner
→ 이 lifecycle의 오래된 표현
```

## 1. 공통 Preflight · 5단계에 포함하지 않음

```text
STAGE_0_PREFLIGHT
→ WORK_PROJECT_START_CANON_CHECKLIST.md
→ READY_AFTER_CORRECTION
```

Preflight는 다음을 fresh-read하고 현재 승인 범위의 stale·conflict·missing canon을 먼저 교정한다.

- exact Base/Project/Notion/actual implementation identity
- 핵심 재미·핵심 시스템·SWOT current truth
- current stage·active Slice·accepted frontier
- remaining work와 dependency/player-value work order
- open PR·protected workstream·evidence ceiling

Preflight가 기존 사실을 복원하는 단계라면, 아래 Stage 1은 **새 Slice의 제품 의미를 사용자와 확정하는 단계**다.

## 2. 공개 5단계 순서

```text
STAGE_1_PLANNING_WITH_USER
→ STAGE_2_PREPRODUCTION_REVIEW
→ STAGE_3_GAME_INPUT_PRODUCTION
→ STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ STAGE_5_USER_VERTICAL_SLICE_VALIDATION
```

정상 경로의 Work→Codex 전환은 Stage 3 종료 뒤 한 번이다. Stage 4 Codex 결과는 같은 Stage 안에서 Work final evidence review와 machine closeout을 거쳐 Stage 5로 전달된다.

---

# Stage 1 — 기획 · 사용자 공동설계

```text
STAGE_1_PLANNING_WITH_USER
CORE_PRODUCT_DECISIONS_REQUIRE_GRILL_ME_WHEN_UNRESOLVED
ROUTINE_APPROVAL_DOES_NOT_AUTO_APPROVE_CORE_PLANNING
BENCHMARK_BEFORE_MATERIAL_GRILL_ME
MINIMUM_VIABLE_ALTERNATIVES: 3
```

## 1.1 목적

현재 Slice에서 플레이어가 무엇을 느끼고, 무엇을 선택하고, 어떤 결과와 기억을 얻는지 사용자와 확정한다.

필수 기획 범위:

```text
project goal / player_promise / pointed_fun
→ representative problem and action
→ meaningful choice_and_tradeoff
→ observable result
→ reward / failure learning
→ next motivation
→ emotional target / first memory
→ differentiation_and_sales_points
→ core/session/meta loop connection
→ core and supporting systems
→ scope / non-scope / protected scope
→ research question / observable signal / evidence ceiling
```

## 1.2 Grill Me와 벤치마킹

다음이 current canon에 이미 승인되어 있고 전제가 유지되면 재질문하지 않는다.

없거나 충돌하거나 materially 바뀌면 `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`와 `grill-me-protocol.md`를 실행한다.

- 프로젝트 코어·플레이어 판타지·Core Loop
- 뾰족한 재미의 우선순위
- 핵심 시스템·의미 있는 선택·보상·실패 학습
- 주요 UX·경제·세션·성장·서사·Art Direction
- MVP/Slice 범위와 가장 위험한 가설
- 차별점·판매 포인트·첫인상·기억

질문 전:

```text
current Project canon + actual implementation
→ Existing Solution First
→ fresh official/professional benchmark
→ success + failure/mixed cases
→ materially distinct alternatives >= 3
→ ADOPT / ADAPT / TEST / REJECT
→ Grill Me one decision at a time
```

standing routine approval은 기술 기본값·가역 수치·승인 기획의 구현 세부에만 적용한다. unresolved core product decision은 자동 승인하지 않는다.

## 1.3 출력과 출구

```yaml
STAGE_1_PLANNING_DECISION_PACKET:
  slice_id:
  player_promise:
  pointed_fun:
  representative_flow:
  meaningful_choice_and_tradeoff:
  result_reward_failure_learning:
  emotional_target_and_first_memory:
  differentiation_and_sales_points: []
  core_and_supporting_systems: []
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  benchmark_and_trade_studies: []
  confirmed_decision_ids: []
  unresolved_core_decisions: []
  research_question:
  observable_signal:
  evidence_ceiling:
  acceptance_hypothesis:
  readiness: STAGE_1_PLANNING_APPROVED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```

```text
unresolved_core_decisions = 0
AND approved Decisions are durably synced/read back
AND readiness = STAGE_1_PLANNING_APPROVED
→ Stage 2
```

---

# Stage 2 — 검수 · Preproduction Review

```text
STAGE_2_PREPRODUCTION_REVIEW
REVIEW_IS_NOT_ASSET_PRODUCTION
REVIEW_IS_NOT_CODEX_IMPLEMENTATION
```

## 2.1 목적

Stage 1 기획이 실제 제작·구현으로 넘어가도 되는지 독립적으로 공격하고, 구현 준비 결함과 제품 의미 충돌을 분리한다.

검수 범위:

- current canon ↔ actual implementation 정합성
- Requirement Traceability
- 핵심 재미·플레이어 가치·first-session promise 보존
- Slice 크기·scope/non-scope·protected scope
- Reuse First·benchmark·trade study 품질
- system/data/UI/Flow 구현 가능성
- Visual/Audio/VFX actual consumer·coverage·quality bar
- rights/provenance·localization·accessibility·platform·performance 위험
- acceptance·test/runtime/build·rollback 계획
- Codex 기술 자유와 제품 의미 보호 경계
- untouched consumer·stale canon·중복·과잉 설계

제품 의미 finding은 Stage 1을 다시 연다. Work-owned input requirement가 부족하면 Stage 3 requirement로 보낸다.

## 2.2 출력과 출구

```yaml
STAGE_2_PREPRODUCTION_REVIEW_PACKET:
  reviewed_stage_1_identity:
  requirement_traceability:
  reuse_and_benchmark_review:
  feasibility_and_scope_review:
  player_value_and_core_fun_review:
  system_data_ui_flow_review:
  visual_audio_vfx_coverage_review:
  rights_accessibility_platform_performance_review:
  acceptance_test_runtime_build_review:
  findings: []
  p0_blockers: []
  p1_blockers: []
  reopen_stage_1: []
  stage_3_requirements: []
  readiness: STAGE_2_REVIEW_APPROVED | REOPEN_STAGE_1 | BLOCKED_UNVERIFIED
```

```text
p0_blockers = 0
AND p1_blockers = 0
AND reopen_stage_1 = 0
AND readiness = STAGE_2_REVIEW_APPROVED
→ Stage 3
```

---

# Stage 3 — 이미지·요소 생성 · Game Input Production

```text
STAGE_3_GAME_INPUT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
NO_PLAYER_FACING_PLACEHOLDER_FOR_SLICE_ACCEPTANCE
WORK_PREP_COMPLETION_BEFORE_CODEX
```

## 3.1 목적

Codex로 전환하기 전에 Work가 소유하는 실제 게임 입력을 모두 준비한다.

- 이미지·UI visual·animation/transition brief·VFX input
- 음악·효과음·UI cue 또는 구현 가능한 procedural audio spec
- UI/UX state·copy·Flow
- data/state/config/schema contract
- localization/accessibility input
- rights/provenance·manifest·hash·project-relative locator
- deterministic/runtime/build QA scenario

새로 만들기 전에 current project implementation/asset → approved reference → Base reuse → rights-cleared external source 순으로 `ADOPT / ADAPT / REJECT`한다.

Visual/Audio에는 exact actual consumer가 필요하다. 설명용 정보는 text/table/DB/Flow를 우선하며 runtime asset으로 가장하지 않는다.

explicit project-local Visual profile에서는:

```text
Notion structure / Art Direction reference
→ project-local candidate
→ PROJECT_ASSET_APPROVED
→ tracked project asset + ASSET_MANIFEST
→ commit/push/remote readback
→ Codex project-relative locator
```

## 3.2 출력과 출구

기존 `WORK_PRODUCTION_INPUT_PACKET`이 단일 Codex handoff input을 소유한다.

```yaml
STAGE_3_GAME_INPUT_PRODUCTION_RECEIPT:
  stage_1_packet_identity:
  stage_2_packet_identity:
  reused_inputs: []
  created_visuals: []
  created_audio_or_specs: []
  ui_data_vfx_localization_inputs: []
  actual_consumers: []
  provenance_rights_manifest: []
  exact_project_relative_locators: []
  remote_readback:
  asset_and_input_qa:
  blocking_missing_inputs: []
  readiness: READY_FOR_SINGLE_CODEX_WINDOW | BLOCKED_UNVERIFIED
```

```text
blocking_missing_inputs = 0
AND all current-Slice P0/P1 consumers are ready
AND WORK_PRODUCTION_INPUT_PACKET = READY_FOR_SINGLE_CODEX_WINDOW
→ Stage 4
```

---

# Stage 4 — 구현(Codex) · Machine Closeout

```text
STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
CODEX_SINGLE_IMPLEMENTATION_WINDOW
WORK_FINAL_EVIDENCE_REVIEW_INSIDE_STAGE_4
MACHINE_QA_FIRST
```

## 4.1 Codex 구현

Codex가 exact Project GitHub·Notion과 Stage 3 packet을 fresh-read하고 actual code·Scene·Resource·runtime wiring·tests·build를 구현한다.

- routine technical choice·reversible refactor·bug fix는 한 window에서 처리
- 제품 의미 변경 → Stage 1
- planning/acceptance contract 결함 → Stage 2
- asset/input gap → Stage 3

## 4.2 Machine QA와 Work final review

다음을 실제로 수행하고 층별 증거를 남긴다.

- deterministic test/GUT 또는 equivalent
- import/parse/headless
- representative runtime flow
- Hera 또는 equivalent screen/runtime observation
- build/export/package smoke
- actual asset consumer verification
- exact-head CI
- Work actual diff·test·runtime/build evidence review
- valid finding correction과 영향 재검증
- GitHub/Notion canon sync·safe merge·new-main readback
- downloadable build·exact build identity·SHA-256·clean launch smoke
- current-Slice machine-executable remaining work 0

## 4.3 출력과 Stage 4 완료

```yaml
STAGE_4_AUTOMATED_SLICE_BUILD:
  exact_product_baseline:
  exact_implementation_head:
  implemented_requirements: []
  consumed_visual_audio_inputs: []
  deterministic_tests:
  runtime_and_screen_evidence:
  build_export_package_evidence:
  exact_ci_and_merge:
  new_main_and_canon_readback:
  downloadable_build_locator:
  build_sha256:
  machine_remaining_work:
  human_usability: NOT_RUN
  player_experience: NOT_RUN
  readiness: AUTOMATED_VERTICAL_SLICE_READY | REOPEN_STAGE_1 | REOPEN_STAGE_2 | REOPEN_STAGE_3 | BLOCKED_UNVERIFIED
```

```text
AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_COMPLETE
```

`AUTOMATED_VERTICAL_SLICE_READY`는 사용자가 검증할 exact build가 준비됐다는 뜻이다. 재미·가독성·첫인상·감정·기억의 최종 PASS가 아니다.

---

# Stage 5 — 사용자 검증

```text
STAGE_5_USER_VERTICAL_SLICE_VALIDATION
VERTICAL_SLICE_COMPLETE_REQUIRES_USER_VALIDATION
NO_NEXT_SLICE_BEFORE_USER_DECISION_GATE
```

## 5.1 사용자 실행·검증 범위

사용자가 과도한 setup 없이 exact downloadable build를 실행할 수 있어야 한다.

확인:

- launch와 representative flow 완주
- `나는 누구고 무엇을 해야 하는가` 이해
- 행동·선택지·비용/위험·결과·다음 행동 이해
- Visual·Audio·VFX feedback 전달
- 조작·가독성·실패 이유·보상·다음 동기
- 의도한 감정·고민·기억·차별점·첫인상
- Project가 요구하는 platform/input/accessibility gate

한 사용자의 검증은 전체 시장·다수 플레이어·장기 retention 증거가 아니다. Project가 더 높은 표본·기기 Gate를 소유하면 그 계약을 추가 적용한다.

## 5.2 출력과 최종 완료

```yaml
STAGE_5_USER_VALIDATION_RESULT:
  exact_build_identity:
  tester_and_prior_exposure:
  launch_result:
  representative_flow_completed:
  comprehension_findings: []
  controls_and_readability_findings: []
  visual_audio_feedback_findings: []
  fun_emotion_choice_reward_memory_findings: []
  defects_and_blockers: []
  user_decision: EXPAND | REWORK | REPEAT_SLICE | HOLD | STOP
  canonical_reflection:
  routed_rework_stage: NONE | STAGE_1 | STAGE_2 | STAGE_3 | STAGE_4
  status: USER_VALIDATED_VERTICAL_SLICE | VALIDATION_FAILED_OR_REWORK_REQUIRED | BLOCKED_UNVERIFIED
```

```text
exact build actually played
AND representative flow completed or failure evidence captured
AND user findings recorded
AND blocking findings corrected/revalidated or explicitly accepted
AND canonical reflection/readback complete
AND user decision permits completion
AND status = USER_VALIDATED_VERTICAL_SLICE
→ VERTICAL_SLICE_COMPLETE
```

## 5.3 finding 재라우팅

```text
fun/core/choice failure → Stage 1
comprehension/spec failure → Stage 2
Visual/Audio/input failure → Stage 3
implementation defect → Stage 4
```

전체 작업을 처음부터 재시작하지 않고 영향 Stage와 downstream만 다시 연다.

---

# 6. Vertical Slice의 완료 범위

Stage 4가 Stage 5에 넘기는 build는 system-only PoC가 아니다.

필수:

- 대표 진입→행동→선택→결과→기록/복귀 flow
- core player promise와 meaningful choice
- current Slice의 P0/P1와 필요한 P2 system/content/UI/data
- 실제 게임 후보 Visual·Audio·VFX·feedback
- player-facing dummy/placeholder 없음
- rights/provenance·project-owned consumption identity
- 필요한 save/resume/error recovery
- current target의 machine evidence
- one-click 또는 one-block launch route

current Slice가 요구하지 않으면 전체 게임 콘텐츠, 장기 경제 전체, 모든 캐릭터·맵·플랫폼·언어·스토어 배포를 포함하지 않는다.

# 7. Structured stage receipt

Repository structured owner가 exact stage identity를 소유한다.

```yaml
FIVE_STAGE_LIFECYCLE_STATE:
  current_stage: PREFLIGHT | PLANNING | REVIEW | INPUT_PRODUCTION | CODEX_IMPLEMENTATION | USER_VALIDATION | COMPLETE
  stage_1_decision_packet:
  stage_2_review_packet:
  stage_3_input_packet:
  stage_4_build_identity:
  stage_5_validation_identity:
  reopen_reason:
  next_action:
```

Notion Home/Production에는 사람이 이해할 현재 단계·핵심 결정·준비/미검증·다음 사용자 행동을 요약한다. raw SHA·CI·tool metadata는 repository/System surface에 둔다.

# 8. 기존 owner compatibility

기존 minimum-transition profile:

```text
legacy Stage A Work preparation = public Stage 1 + Stage 2 + Stage 3
legacy Stage B Codex implementation = public Stage 4 Codex execution
legacy Stage C Work final review/user handoff = public Stage 4 machine closeout + Stage 5 entry
```

기존 Work Mode:

```text
PLAN = Stage 1
REVIEW = Stage 2 + Stage 4 Work final review
NONCODING_BUILD = Stage 3 and canon correction
GODOT_PRODUCT_BUILD = Stage 4 Codex
USER validation = Stage 5, not an AI Work Mode
```

# 9. Evidence ceiling

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

```text
contract present
!= stage packet created
!= asset produced
!= Codex implemented
!= build exported
!= user played
!= Vertical Slice complete
```

실제 사용자 검증 전에는 Stage 5 PASS, `VERTICAL_SLICE_COMPLETE`, 다음 Slice 자동 진입을 주장하지 않는다.
