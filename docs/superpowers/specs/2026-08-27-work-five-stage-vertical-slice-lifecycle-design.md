# Work 5단계 버티컬 슬라이스 Lifecycle 설계

## 1. 목표

게임 프로젝트의 Work 실행을 다음 다섯 단계로 명시적으로 분리한다.

```text
1. 기획
2. 검수
3. 이미지·요소 생성
4. 구현(Codex)
5. 사용자 검증
```

기존 Base의 Authority Recovery, Startup Canon Checklist, Grill Me, Reuse First, Benchmark, Adversarial Review, Visual/Audio owner, Work↔Codex 최소 전환, IRG, Machine QA, Git/PR/merge/readback, Human/Player evidence 경계를 제거하거나 복제하지 않는다. 새 owner는 이 책임들을 5단계의 입구·출구 Gate로 조합한다.

## 2. 실제 감사 결과

### 2.1 Base current 상태

현재 `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`는 외부적으로 `Work preparation → Codex implementation → Work final review/user handoff`의 3단계를 사용한다. `Stage A — Work preparation` 안에 기획, 규칙·UI/UX·Data/Flow 검수, Visual·Audio·VFX 준비, 적대적 검토와 IRG가 함께 들어 있어 사용자가 요청한 기획·검수·요소 제작 경계가 독립 상태로 드러나지 않는다.

`WORK_PROJECT_START_CANON_CHECKLIST.md`는 핵심 재미·핵심 시스템·SWOT·현재 단계·남은 작업·작업순서·정본 선교정을 강하게 요구하지만, 이것은 작업 시작 preflight이며 새로운 Slice의 핵심 기획을 사용자와 공동 확정하는 Stage 1 자체는 아니다.

`PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`와 `grill-me-protocol.md`는 Core Loop, 뾰족한 재미, 중요 시스템·UX·경제·서사·Art Direction·범위 같은 제품 의미 결정에 Grill Me를 요구한다. 그러나 현재 최종 Starter와 minimum-transition profile의 Stage A 출구에 이 사용자 공동결정 Gate가 직접 연결되어 있지 않다.

### 2.2 Project canon 상태

확인한 active project root authority:

- GRIMOIRE
- MylittleBoat
- Switchy Express
- Omenward
- Tetris
- Ninja Survival
- Ten Paces Hidden Moves
- Blacksmith
- urban-legend
- Coc-Fiction

프로젝트들은 `PLAN→BUILD→REVIEW`, `기획 완료→Visual/UX Review→구현`, `current decision→Codex handoff→Human Gate` 등 서로 다른 표현을 사용한다. 십보강호는 기획 완료와 Visual/UX 검수를 잘 분리하고, GRIMOIRE와 Switchy는 Automated Vertical Slice Ready와 사용자/물리 검증을 분리한다. 반면 공통 5단계 상태명과 단계별 Definition of Ready/Done은 Project마다 일관되게 존재하지 않는다.

Coc-Fiction은 게임 runtime 프로젝트가 아니므로 게임 버티컬 슬라이스 5단계를 강제하지 않는다. 이 owner는 게임 product implementation과 user-play validation이 존재하는 프로젝트에 적용한다. 비게임 프로젝트는 project-specific lifecycle owner를 유지한다.

### 2.3 Notion 상태

Project Home은 핵심 Flow·시스템·Visual·현재 상태를 사람에게 보여 주는 구조를 이미 갖는다. 일부 Project Production 페이지는 `Planning Complete`, `Visual/UX Requirement Complete`, 구현 Gate, Human NOT_RUN을 분리하지만, Portfolio 전체에서 공통 5단계 상태 vocabulary와 동일한 Gate를 사용하지는 않는다.

Notion을 새 중앙 실행 정본으로 만들지 않는다. 5단계 상태는 repository structured receipt가 단일 실행 identity를 소유하고, Notion은 사람이 이해하는 현재 단계·핵심 결정·검증 상태를 요약한다.

## 3. 대안 비교

### A. 기존 3단계 이름만 5단계로 바꾸기

- 장점: 변경량이 작다.
- 실패: Stage A 내부의 기획·검수·자산 준비가 실제로 분리되지 않는다. Gate와 rollback 경로가 불명확하다.
- 판정: REJECT.

### B. 새 얇은 5단계 lifecycle owner를 추가하고 기존 owner를 조합하기

- 장점: 사용자에게 보이는 단계와 실제 입출력 Gate를 고정하면서 기존 전문 owner·회귀 증거를 재사용한다. Work↔Codex 전환은 1회로 유지할 수 있다.
- 비용: Router/Profile/Starter에 owner link와 compatibility mapping이 필요하다.
- 판정: ADOPT.

### C. 기존 minimum-transition profile 전체를 5단계 문서로 다시 작성하기

- 장점: 한 파일에서 모든 절차를 볼 수 있다.
- 실패: second canon, 긴 context, 기존 owner drift, 높은 회귀 위험.
- 판정: REJECT.

## 4. 최상위 상태 머신

Authority Recovery와 Startup Canon Checklist는 5단계 앞의 공통 `STAGE_0_PREFLIGHT`이며 사용자-facing production 단계 수에 포함하지 않는다.

```text
STAGE_0_PREFLIGHT
→ STAGE_1_PLANNING_WITH_USER
→ STAGE_2_PREPRODUCTION_REVIEW
→ STAGE_3_GAME_INPUT_PRODUCTION
→ STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ STAGE_5_USER_VERTICAL_SLICE_VALIDATION
```

정상 경로에서 Work→Codex 전환은 Stage 3 종료 뒤 정확히 한 번 수행한다. Stage 4의 Codex 결과는 Work final evidence review를 거쳐 Stage 5로 전달된다.

## 5. Stage 0 — Preflight

Owner: `WORK_PROJECT_START_CANON_CHECKLIST.md`.

확인:

- exact Base/Project/Notion/actual implementation identity
- 핵심 재미·핵심 시스템·SWOT current truth
- current stage·active Slice·accepted frontier
- 남은 작업·dependency/player-value work order
- stale/conflict/missing canon 선교정
- open PR·protected workstream

출구: `READY_AFTER_CORRECTION`.

Stage 0은 새 핵심 기획을 확정하지 않는다. current canon이 없는/불완전한 Slice는 Stage 1에서 사용자와 설계한다.

## 6. Stage 1 — 기획 · 사용자 공동설계

```text
STAGE_1_PLANNING_WITH_USER
CORE_PRODUCT_DECISIONS_REQUIRE_GRILL_ME_WHEN_UNRESOLVED
ROUTINE_APPROVAL_DOES_NOT_AUTO_APPROVE_CORE_PLANNING
BENCHMARK_BEFORE_MATERIAL_GRILL_ME
```

### 6.1 목적

현재 Slice의 핵심 플레이어 가치와 제품 의미를 사용자와 확정한다.

필수 범위:

- player promise와 pointed fun
- 대표 문제·행동·의미 있는 선택·trade-off
- 결과·보상·실패 학습·다음 동기
- core loop/session loop/meta 연결
- Slice에 닿는 핵심·지원 시스템
- 첫인상·감정·기억·차별점·판매 포인트
- 포함/제외/보호 범위
- 연구 질문·observable signal·evidence ceiling
- 주요 UX·경제·서사·Art Direction이 관련될 때 그 의미

### 6.2 Grill Me 경계

다음이 current canon에서 이미 승인되고 전제가 유지되면 재질문하지 않는다.

새로 없거나 서로 충돌하거나 materially 바뀌면 `grill-me-protocol.md`를 실행한다.

- 프로젝트 코어·판타지·Core Loop
- 뾰족한 재미의 우선순위
- 핵심 시스템·의미 있는 선택·실패/보상 의미
- 주요 UX·경제·세션·성장·서사·Art Direction
- MVP/Slice 범위와 가장 위험한 가설
- 경쟁작 대비 차별점과 판매 포인트

질문 전에 Project current source와 실제 구현을 확인하고, decision-relevant benchmark·성공/실패 사례·최소 3개 materially distinct 대안을 준비한다. 질문은 한 번에 하나의 사용자 결정만 다룬다.

사용자의 standing routine approval은 기술 기본값·가역 수치·승인 기획 구현 세부에만 적용하며 위 핵심 제품 결정을 자동 승인하지 않는다.

### 6.3 출력

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

출구 조건:

```text
unresolved_core_decisions = 0
AND current decisions synced/read back
AND STAGE_1_PLANNING_APPROVED
```

## 7. Stage 2 — 검수 · Preproduction Review

```text
STAGE_2_PREPRODUCTION_REVIEW
REVIEW_IS_NOT_ASSET_PRODUCTION
REVIEW_IS_NOT_CODEX_IMPLEMENTATION
```

### 7.1 목적

Stage 1 결과가 실제 제작·구현으로 넘어가도 되는지 독립적으로 공격한다.

검수 범위:

- current canon/actual implementation 정합성
- Requirement Traceability
- 핵심 재미·플레이어 가치 보존
- 범위와 Slice 크기
- Reuse First·벤치마크·대안 비교 품질
- 시스템/데이터/UI/Flow 구현 가능성
- Visual/Audio/VFX actual consumer와 coverage
- rights/provenance·localization·accessibility·platform·performance 위험
- acceptance·test/runtime/build·rollback 계획
- Codex가 결정할 기술 자유와 보호 의미
- untouched consumer·정본 drift·중복·과잉 설계

Review finding이 제품 의미를 바꾸면 Stage 1로 돌아간다. 구현 입력·asset requirement만 부족하면 Stage 3 backlog로 보낸다.

### 7.2 출력

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

출구 조건:

```text
p0_blockers = 0
AND p1_blockers = 0
AND reopen_stage_1 = 0
AND STAGE_2_REVIEW_APPROVED
```

## 8. Stage 3 — 이미지·요소 생성

```text
STAGE_3_GAME_INPUT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
NO_PLAYER_FACING_PLACEHOLDER_FOR_SLICE_ACCEPTANCE
```

### 8.1 목적

Codex 구현 전에 Work가 소유하는 모든 실제 게임 입력을 한 번에 준비한다.

- 이미지·UI visual·animation/transition brief·VFX input
- 음악·효과음·UI cue 또는 구현 가능한 procedural audio spec
- UI/UX state·copy·Flow
- data/state/config/schema contract
- localization/accessibility input
- rights/provenance·manifest·hash·project-relative locator
- deterministic/runtime/build QA scenario

새로 만들기 전에 existing project/Base/rights-cleared asset을 `ADOPT / ADAPT / REJECT`한다. 새 Visual/Audio에는 exact consumer가 필요하다.

Explicit project-local Visual profile에서는 Notion은 구조·Art Direction reference이고 binary는 project-local candidate→tracked asset+manifest→remote readback으로 전달한다.

### 8.2 출력

기존 `WORK_PRODUCTION_INPUT_PACKET`을 Stage 3의 단일 구현 입력 packet으로 사용한다.

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

출구 조건:

```text
blocking_missing_inputs = 0
AND all current-Slice P0/P1 input consumers are ready
AND WORK_PRODUCTION_INPUT_PACKET = READY_FOR_SINGLE_CODEX_WINDOW
```

## 9. Stage 4 — 구현(Codex) · Machine Closeout

```text
STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
CODEX_SINGLE_IMPLEMENTATION_WINDOW
WORK_FINAL_EVIDENCE_REVIEW_INSIDE_STAGE_4
```

### 9.1 Codex 구현

Codex가 exact Project GitHub·Notion과 Stage 3 packet을 fresh-read하고 실제 code·Scene·Resource·runtime wiring·tests·build를 구현한다.

Routine technical decisions·reversible refactor·bug fix는 한 window에서 처리한다. 제품 의미 변경은 Stage 1, input gap은 Stage 3, preproduction contract 결함은 Stage 2로 반환한다.

### 9.2 Machine QA와 Work final review

- deterministic test/GUT 또는 equivalent
- import/parse/headless
- representative runtime flow
- Hera 또는 equivalent screen/runtime observation
- build/export/package smoke
- actual asset consumer 검증
- exact-head CI
- Work가 actual diff·test·runtime/build evidence 검수
- valid finding correction과 impact revalidation
- GitHub/Notion canon sync·safe merge·new-main readback
- downloadable build·exact commit/build identity·SHA-256·clean launch smoke
- current-Slice machine-executable remaining work 0

### 9.3 출력과 상태

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

`AUTOMATED_VERTICAL_SLICE_READY`는 사용자가 검증할 수 있는 빌드 준비 상태이며 `VERTICAL_SLICE_COMPLETE`가 아니다.

## 10. Stage 5 — 사용자 검증

```text
STAGE_5_USER_VERTICAL_SLICE_VALIDATION
VERTICAL_SLICE_COMPLETE_REQUIRES_USER_VALIDATION
NO_NEXT_SLICE_BEFORE_USER_DECISION_GATE
```

### 10.1 사용자 실행 계약

사용자가 과도한 setup 없이 exact build를 실행할 수 있어야 한다.

검증 범위:

- 정상 launch와 representative flow 완주
- `나는 누구고 무엇을 해야 하는가` 이해
- 행동·선택지·비용/위험·결과·다음 행동 이해
- 핵심 feedback의 Visual·Audio·VFX 전달
- 조작·가독성·실패 이유·보상·다음 동기
- 의도한 감정·고민·기억·차별점·첫인상
- 프로젝트별 target platform/input/accessibility gate

한 사용자의 검증은 전체 시장·다수 플레이어·장기 retention 증거가 아니다. Project가 더 높은 표본·기기 Gate를 소유하면 그 계약이 우선한다.

### 10.2 결과

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

완료 조건:

```text
exact downloadable build actually played
AND representative flow completed or failure evidence captured
AND user findings recorded
AND blocking findings corrected/revalidated or explicitly accepted
AND canonical reflection/readback complete
AND user decision permits completion
AND status = USER_VALIDATED_VERTICAL_SLICE
→ VERTICAL_SLICE_COMPLETE
```

사용자 검증 전에는 다음 Slice로 자동 진입하지 않는다.

## 11. Vertical Slice 품질 범위

Stage 4가 Stage 5에 넘기는 build는 시스템-only PoC가 아니다.

필수:

- 대표 진입→행동→선택→결과→기록/복귀 flow
- 핵심 player promise와 meaningful choice
- current Slice의 P0/P1와 필요한 P2 systems/content/UI/data
- 실제 게임 후보 Visual·Audio·VFX·feedback
- player-facing dummy/placeholder 없음
- 권리·provenance·project-owned consumption identity
- 필요한 save/resume/error recovery
- 목표 platform의 현재 machine evidence
- one-click 또는 one-block 실행 경로

전체 게임 콘텐츠, 장기 경제 전체, 모든 캐릭터·맵·플랫폼·언어·스토어 배포는 current Slice scope가 요구하지 않으면 포함하지 않는다.

## 12. 되돌림과 재진입

```text
Stage 2 core/product finding → Stage 1
Stage 3 consumer/coverage conflict that changes product meaning → Stage 1
Stage 3 missing requirement/acceptance → Stage 2
Stage 4 product meaning change → Stage 1
Stage 4 planning contract gap → Stage 2
Stage 4 asset/input gap → Stage 3
Stage 5 fun/core/choice failure → Stage 1
Stage 5 comprehension/spec failure → Stage 2
Stage 5 Visual/Audio/input failure → Stage 3
Stage 5 implementation defect → Stage 4
```

전체를 처음부터 재시작하지 않고 영향 Stage와 downstream만 다시 연다.

## 13. Notion·GitHub 표시

Repository structured receipt가 exact stage identity를 소유한다.

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

Notion Home/Production에는 사람이 이해할 수 있게 현재 단계, 핵심 결정, 준비/미검증, 다음 사용자 행동을 요약한다. raw SHA·CI·tool metadata는 repository/System surface에 둔다.

## 14. Compatibility mapping

기존 3-stage minimum-transition profile:

```text
Stage A Work preparation = new Stage 1 + 2 + 3
Stage B Codex implementation = new Stage 4 Codex execution
Stage C Work final review/user handoff = new Stage 4 machine closeout + Stage 5 entry
```

기존 Work Mode:

```text
PLAN = Stage 1
REVIEW = Stage 2 + Stage 4 Work final review
NONCODING_BUILD = Stage 3 and canon corrections
GODOT_PRODUCT_BUILD = Stage 4 Codex
USER validation = Stage 5, not an AI Work Mode
```

## 15. 비게임 프로젝트

```text
GAME_PRODUCT_FIVE_STAGE_LIFECYCLE_ONLY
NON_GAME_PROJECT_REQUIRES_PROJECT_SPECIFIC_ADAPTER
```

Coc-Fiction 같은 비게임 프로젝트에는 Godot/Codex 버티컬 슬라이스 상태를 자동 강제하지 않는다. 필요하면 `기획→원고 검수→콘텐츠 제작→패키징/발행→독자 검증` 같은 별도 project Decision으로 명시 채택한다.

## 16. 회귀 방지 요구

자동 테스트는 최소 다음을 검사한다.

- 5개 stage 이름과 순서가 current owner에 존재
- Stage 1 core decisions에 Grill Me + benchmark + user collaboration required
- standing routine approval이 core planning을 자동 승인하지 않음
- Stage 2가 asset creation/implementation과 분리
- Stage 3가 Work-owned input production이며 Codex 전환 전 완료
- Stage 4가 actual Codex implementation + machine QA + Work final review + build/merge를 포함
- `AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_COMPLETE`
- Stage 5 user play/readback 없이는 complete/next Slice 금지
- rework가 적절한 Stage로 돌아감
- Router/Profile/Starter가 current owner를 직접 route
- non-game project exception
- Human/Player evidence ceiling 유지
- 기존 local Visual·safe Git·fallback·IRG·required-work-zero capability 비퇴행

## 17. Evidence ceiling

이 Base 계약의 존재와 test PASS는 특정 프로젝트에서 5단계를 실제 수행했다는 뜻이 아니다.

```text
contract present
!= stage packet created
!= asset produced
!= Codex implemented
!= build exported
!= user played
!= Vertical Slice complete
```
