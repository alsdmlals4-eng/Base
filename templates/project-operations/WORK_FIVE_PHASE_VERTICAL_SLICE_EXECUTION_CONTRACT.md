# Work 5단계 버티컬 슬라이스 실행 계약

> 승인 근거: `BCP-2026-040-work-five-phase-vertical-slice`. 이 문서는 사용자에게 보이는 5단계 macro interface와 phase transition만 소유한다. Project 고유 사실·상태·Decision과 기존 Base 전문 owner의 세부 절차를 복제하지 않는다.

```text
FIVE_PHASE_INTERFACE_OWNER
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
CURRENT_BASE_SPECIALIST_OWNER_WINS_ON_DETAIL_DRIFT
PROJECT_NATIVE_STATE_NAMES_PRESERVED
NO_PROJECT_WIDE_STATE_RENAME
DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE
```

## 0. 공용 흐름

```text
PHASE_1_PLANNING_CO_DESIGN
→ PHASE_2_PREPRODUCTION_REVIEW
→ PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
→ PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ PHASE_5_USER_VERTICAL_SLICE_VALIDATION
```

이 5단계는 `PLAN / BUILD / REVIEW`, Task, Decision, package candidate 같은 Project-native state를 대체하지 않는다. 시작할 때 exact Project canon과 actual implementation을 fresh-read해 `FIVE_PHASE_PROJECT_MAPPING` receipt로 현재 phase를 매핑한다.

## 1. Phase 1 — 기획·사용자 공동설계

```text
PHASE_1_PLANNING_CO_DESIGN
CORE_PLANNING_CO_DESIGN_REQUIRED
DECISION_RELEVANT_BENCHMARK_REQUIRED
THREE_MATERIALLY_DISTINCT_ALTERNATIVES_REQUIRED
ADOPT / ADAPT / REJECT
CORE_PLANNING_DECISION_PACKET
PHASE_1_USER_CONFIRMED
```

새 프로젝트·새 핵심 Slice·Core 의미 변경에서는 아직 승인되지 않은 핵심 제품 의미를 Work가 단독 확정하지 않는다. current canon과 실제 구현을 먼저 읽고, 저장소·승인 Decision으로 닫히지 않는 material 항목만 current Grill Me owner를 사용해 사용자와 함께 결정한다.

핵심 공동설계 범위:

- project goal / player promise / pointed fun
- core / session / meta loop
- core systems / supporting systems
- representative player action
- meaningful choice / tension / trade-off
- result / reward / failure learning / feedback
- emotional target / first-session memory / next motivation
- project differentiation / sales point
- protected strengths / included scope / explicit non-scope
- Vertical Slice fun·production·technical hypothesis와 observable acceptance

결정 순서:

```text
현재 Project canon·actual implementation
→ approved asset/reference
→ Base reusable evidence
→ 직접 관련된 검증 Project 사례
→ 공식·현업·시장 성공/실패·혼합 사례
→ 최소 3개 materially distinct 대안 비교
→ ADOPT / ADAPT / REJECT
→ 필요한 핵심 Decision만 Grill Me
```

이미 승인된 핵심 Decision, 저장소로 확인 가능한 사실, Codex가 정할 Node/Scene/함수 내부 구조, 가역적 기술 세부, 초기 시험값은 다시 묻지 않는다.

```text
DELEGATED_ROUTINE_APPROVAL != CORE_PRODUCT_MEANING_APPROVAL
```

Phase 1 exit은 핵심 player-value trace, scope/non-scope, protected strengths, Slice hypothesis/acceptance가 Project human/structured canon에 기록·readback되고 필요한 material Decision이 `PHASE_1_USER_CONFIRMED`인 상태다.

## 2. Phase 2 — 구현 전 검수

```text
PHASE_2_PREPRODUCTION_REVIEW
REVIEWED_SLICE_PRODUCTION_CONTRACT
APPROVED_FOR_INGAME_ELEMENT_PRODUCTION
NO_SERIAL_ASSET_PRODUCTION_BEFORE_PHASE_2_PASS
NO_CODEX_IMPLEMENTATION_BEFORE_PHASE_2_PASS
```

Phase 1의 기획을 계속 확장하지 않고 다음 관점에서 재공격·축소·교정한다.

- 핵심 재미·행동·선택·결과·보상의 인과 연결
- representative scope와 explicit non-scope
- Existing Solution First / 재사용 / 실제 기술 가능성
- decision-relevant benchmark applicability와 surface-copy 위험
- UI/UX 정보 이해·상태·edge case
- data/state/save/schema/economy/balance 영향
- Visual/Audio/UI/VFX/data actual consumer와 coverage
- rights/provenance/incremental cost/release 위험
- implementation acceptance / deterministic test / runtime / build / rollback
- Codex 재작업 위험과 Work↔Codex 불필요 왕복
- Project GitHub/Notion/actual implementation drift와 untouched consumer

finding이 Core 의미를 바꾸면 Phase 1로 되돌린다. 의미를 바꾸지 않는 누락·모순·coverage·acceptance 결함은 Phase 2 안에서 교정한다. `APPROVED_FOR_INGAME_ELEMENT_PRODUCTION` 전에는 serial production asset 제작이나 Codex product implementation을 시작하지 않는다.

## 3. Phase 3 — 이미지·사운드·UI·Data·VFX 등 Work 제작

```text
PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
PROJECT_LOCAL_VISUAL_BINARY_FIRST
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

검수된 current Slice에 실제 consumer가 있는 비코딩 제품 입력을 Work에서 최대한 한 번에 닫는다.

- production Visual / sprite / texture / animation source
- Audio / music / SFX source 또는 승인 procedural spec
- UI/UX states / copy / flow / icon / font usage
- runtime-consumed Data/content와 tunable range
- VFX / feedback requirement 또는 source
- localization/accessibility requirement
- provenance / rights / format / import / durable locator
- deterministic/runtime/Hera/build QA scenario와 acceptance

설명용 sheet·관계도·비교판은 planning reference일 수 있지만 actual consumer가 없으면 production asset으로 만들지 않는다.

Visual binary는 current local Visual owner에 따라:

```text
project-local candidate
→ objective review
→ PROJECT_ASSET_APPROVED
→ tracked project asset + ASSET_MANIFEST
→ commit/push/remote readback
→ Codex project-relative locator
→ runtime consumer evidence
```

Project/host가 별도 이미지 승인 Gate를 요구하면 그 Gate가 우선한다. Phase 3 중 제품 의미가 바뀌면 Phase 1, requirement/consumer 문제가 발견되면 Phase 2를 bounded reopen한다.

## 4. Phase 4 — Codex 구현·Machine QA·Work 최종 구현검수

```text
PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
CODEX_SINGLE_IMPLEMENTATION_WINDOW
WORK_FINAL_IMPLEMENTATION_REVIEW_IS_PHASE_4_CLOSEOUT
USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

Codex는 exact Project GitHub·Notion과 `WORK_PRODUCTION_INPUT_PACKET`을 fresh-read하고 실제 product code·Scene·Resource·runtime wiring·test·build를 구현한다. routine technical choice·reversible refactor·local bug fix·fixture·QA scenario는 approved Slice 안에서 연속 처리하고 작은 finding마다 Work로 되돌아오지 않는다.

Phase 4 closeout:

```text
Codex actual implementation
→ deterministic/import/parse/runtime/build QA
→ adopted GUT/Hera 또는 evidence-equivalent machine QA
→ Work actual diff/evidence final implementation review
→ valid implementation correction
→ impact-bounded revalidation
→ GitHub·Notion canon sync/readback
→ exact-head CI / safe squash merge / post-merge readback
→ machine-executable required work = 0
→ downloadable internal build + validation packet
```

Phase 4 exit은 다음이며 최종 Vertical Slice 완료가 아니다.

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
AUTOMATED_VERTICAL_SLICE_READY != USER_VALIDATED_VERTICAL_SLICE
```

## 5. Phase 5 — 사용자 실제 플레이 검증

```text
PHASE_5_USER_VERTICAL_SLICE_VALIDATION
ACTUAL_USER_PLAY_REQUIRED
CANONICAL_REFLECTION_AFTER_PLAY_REQUIRED
```

사용자가 Phase 4의 exact build/scene을 실제 실행하고 representative action→choice→result→feedback flow를 플레이한다.

최소 관찰:

- 시작·목표·다음 행동 이해
- 핵심 행동과 meaningful choice·trade-off 인지
- 결과·피드백·보상·실패 학습 이해
- Visual/Audio/UI 가독성·지각
- 조작·입력·피로·막힘
- 핵심 감정·기억·첫인상·차별점/세일즈포인트 전달
- 이탈·재시도·계속 플레이 이유

판정:

```text
USER_VALIDATED_VERTICAL_SLICE_PASS
USER_VALIDATED_WITH_FOLLOWUP
REWORK_REQUIRED
BLOCKED_USER_VALIDATION
```

feedback이 Core 의미를 바꾸면 Phase 1, 설계·가독성·acceptance 문제면 Phase 2, 누락/부적절 asset이면 Phase 3, bug/runtime/build 문제면 Phase 4를 bounded reopen한다.

`USER_VALIDATED_VERTICAL_SLICE`는 actual user play evidence, feedback/finding, next decision, Canonical Reflection After Play가 Project canon에 기록·readback된 뒤에만 사용할 수 있다.

## 6. Vertical Slice 완료 범위

```text
REPRESENTATIVE_EXPERIENCE_REQUIRED
SHIPPING_INTENT_SLICE_QUALITY_REQUIRED
CRITICAL_PLAYER_FACING_PLACEHOLDER_FORBIDDEN
WHOLE_GAME_COMPLETION_NOT_REQUIRED
FINAL_ALL_PLATFORM_PASS_NOT_REQUIRED
FINAL_STORE_RELEASE_PASS_NOT_REQUIRED
```

Phase 4 `AUTOMATED_VERTICAL_SLICE_READY`에는 current Slice가 약속한 representative flow가 actual build에서 처음부터 끝까지 실행되고, core systems와 실제 consumer가 연결되며, 필요한 범위의 shipping-intent UI/Visual/Audio/VFX/feedback, deterministic/runtime/build evidence, exact build identity, launch route가 있어야 한다. critical player-facing placeholder로 목표 품질을 위장할 수 없다.

Phase 5 `USER_VALIDATED_VERTICAL_SLICE`에는 위 조건에 더해 actual user play, blocking usability의 처리/판정, 핵심 재미·감정·기억·차별점에 대한 사용자 evidence와 next decision이 필요하다.

전체 게임 콘텐츠, 최종 전체 밸런스, 모든 플랫폼, 최종 localization, 스토어·법적 공개 출시 PASS는 current Vertical Slice 완료 조건이 아니다.

## 7. Project 상태 매핑과 비게임 도메인

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
```

```text
PROJECT_NATIVE_STATE_NAMES_PRESERVED
NO_PROJECT_WIDE_STATE_RENAME
```

예를 들어 `PLAN / BUILD / REVIEW`, `DoR`, Task, Decision, package candidate, `AUTOMATED_VERTICAL_SLICE_READY`는 실제 의미에 따라 매핑하며 historical state를 rename하지 않는다.

비게임/서사 프로젝트도 업무 분리 원칙은 domain에 맞게 adapt할 수 있다.

```text
DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE
GODOT_EVIDENCE_NOT_APPLICABLE_FOR_NON_GAME
```

비게임 프로젝트에서 Phase 3/4는 해당 domain의 실제 production/implementation으로 해석하고 Godot/GUT/Hera/game-runtime evidence만 `NOT_APPLICABLE`로 둔다. 비게임 산출물에 게임 Vertical Slice 완료를 허위 주장하지 않는다.

## 8. 상세 owner routing

이 계약은 다음 current owner를 조합한다.

- startup canon: `WORK_PROJECT_START_CANON_CHECKLIST.md`
- planning decision/Grill Me: `PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md` + current Grill Me protocol
- minimum-transition packets/approval/fallback/QA/merge: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- Work↔Codex role: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Visual generation/approval and project-local delivery: current image + local Visual owners
- shipping-intent Vertical Slice evidence/DoD: `skills/designing-vertical-slices/SKILL.md`
- evidence identity: `WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`

세부 owner와 이 macro interface가 충돌하면 Project truth를 먼저 확인하고 해당 분야 current specialist owner의 세부 계약을 따른다. 단, 사용자 승인 5단계 순서와 Phase 4/5 evidence ceiling을 3단계 표현으로 다시 압축하지 않는다.
