# Work 5단계 버티컬 슬라이스 실행 계약

> 승인 근거: `BCP-2026-040-work-five-phase-vertical-slice`. 사용자에게 보이는 5단계 macro interface와 phase transition만 소유한다. Project 사실·상태·Decision과 기존 Base 전문 owner의 세부 절차는 복제하지 않는다.

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

Project의 `PLAN / BUILD / REVIEW`, DoR, Task, Decision, package candidate 등은 rename하지 않는다. exact Project canon·actual implementation을 fresh-read해 `FIVE_PHASE_PROJECT_MAPPING`으로 현재 의미를 phase에 매핑한다.

## 1. Phase 1 — 기획·사용자 공동설계

```text
PHASE_1_PLANNING_CO_DESIGN
CORE_PLANNING_CO_DESIGN_REQUIRED
DECISION_RELEVANT_BENCHMARK_REQUIRED
THREE_MATERIALLY_DISTINCT_ALTERNATIVES_REQUIRED
ADOPT / ADAPT / REJECT
CORE_PLANNING_DECISION_PACKET
PHASE_1_USER_CONFIRMED
DELEGATED_ROUTINE_APPROVAL != CORE_PRODUCT_MEANING_APPROVAL
```

새 핵심 Slice나 material Core 변경에서 아직 승인되지 않은 제품 의미는 Work가 단독 확정하지 않는다. current canon·actual implementation·승인 Decision을 먼저 복원하고, 남은 핵심 Decision만 current Grill Me owner로 사용자와 함께 닫는다.

공동설계 대상은 player promise, core/session/meta loop, representative action, meaningful choice·trade-off, reward·failure learning·feedback, 목표 감정·기억·다음 동기, 차별점/세일즈포인트, protected strength, Slice hypothesis/acceptance다.

```text
current Project / actual implementation
→ approved asset/reference
→ Base reusable evidence
→ directly relevant verified project evidence
→ official·practice·market success/failure/mixed cases
→ 최소 3개 materially distinct 대안
→ ADOPT / ADAPT / REJECT
→ unresolved material Decision만 Grill Me
```

이미 승인된 Decision, 저장소에서 확인되는 사실, Codex 내부 구현 구조, 가역적 기술 세부·초기 시험값은 다시 묻지 않는다.

**Exit:** 핵심 player-value trace, included/non-scope, protected strengths, Slice acceptance와 필요한 사용자 Decision이 Project human/structured canon에 기록·readback되고 `PHASE_1_USER_CONFIRMED`.

## 2. Phase 2 — 구현 전 검수

```text
PHASE_2_PREPRODUCTION_REVIEW
REVIEWED_SLICE_PRODUCTION_CONTRACT
APPROVED_FOR_INGAME_ELEMENT_PRODUCTION
NO_SERIAL_ASSET_PRODUCTION_BEFORE_PHASE_2_PASS
NO_CODEX_IMPLEMENTATION_BEFORE_PHASE_2_PASS
```

Phase 1 내용을 기능 추가로 계속 늘리지 않고 다음을 공격·교정한다.

- action→choice→result→feedback 인과와 실제 고민
- representative scope / explicit non-scope / protected scope
- Existing Solution First와 benchmark applicability
- feasibility / UI·UX / data·state·save·economy 영향
- Visual·Audio·UI·VFX·Data actual consumer와 coverage
- rights/provenance/cost/release risk
- acceptance / deterministic·runtime·build QA / rollback
- GitHub·Notion·actual implementation drift와 재작업 위험

Core 의미가 바뀌는 finding은 Phase 1로 되돌린다. 의미를 바꾸지 않는 누락·모순·coverage·acceptance 결함은 Phase 2 안에서 교정한다.

**Exit:** `REVIEWED_SLICE_PRODUCTION_CONTRACT` + `APPROVED_FOR_INGAME_ELEMENT_PRODUCTION`. 이 전에는 serial production asset 또는 Codex product implementation을 시작하지 않는다.

## 3. Phase 3 — 이미지·사운드·UI·Data·VFX 등 Work 제작

```text
PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
PROJECT_LOCAL_VISUAL_BINARY_FIRST
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

검수된 current Slice에 실제 consumer가 있는 비코딩 제품 입력만 제작·정리한다. Visual·Audio·UI source/copy·runtime Data/content·VFX·localization/accessibility requirement와 provenance/rights/format/import/durable locator를 현재 전문 owner가 소유한다.

설명용 sheet·관계도·비교판은 planning reference일 수 있지만 actual consumer가 없으면 production asset으로 만들지 않는다.

Project/host의 이미지 승인 Gate와 project-local Visual approval/manifest/readback 절차는 current Visual owner가 계속 소유한다. 제품 의미가 바뀌면 Phase 1, requirement/consumer 결함이면 Phase 2를 bounded reopen한다.

**Exit:** actual-consumer input, approval/provenance/locator, UI/Data/QA acceptance가 한 `WORK_PRODUCTION_INPUT_PACKET`으로 닫히고 `READY_FOR_SINGLE_CODEX_WINDOW`.

## 4. Phase 4 — Codex 구현·Machine QA·Work 최종 구현검수

```text
PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
CODEX_SINGLE_IMPLEMENTATION_WINDOW
WORK_FINAL_IMPLEMENTATION_REVIEW_IS_PHASE_4_CLOSEOUT
USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

Codex는 exact Project GitHub·Notion과 packet을 fresh-read해 actual code·Scene·Resource·runtime wiring·test·build를 구현한다. routine technical choice·reversible refactor·local bug fix·fixture·QA는 approved Slice 안에서 연속 처리한다.

Codex 뒤 Work의 actual diff/evidence 검수, valid correction, impact-bounded revalidation, canon sync/readback, exact-head CI, safe merge, post-merge readback은 별도 6단계가 아니라 **Phase 4 closeout**이다. 세부 packet/approval/fallback/GUT·Hera/merge 계약은 minimum-transition profile과 current evidence owner가 소유한다.

**Exit:** current Slice의 machine-executable required work = 0, representative build/launch route와 다운로드 가능한 internal artifact가 준비되고 다음 상태를 만족한다.

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

사용자가 Phase 4 exact build/scene을 실제 실행해 representative action→choice→result→feedback을 플레이한다. 시작/조작 이해, meaningful choice, feedback/reward/failure learning, UI·Visual·Audio 지각, 감정·기억·첫인상·차별점, 이탈·재시도·계속 플레이 이유를 확인한다.

판정:

```text
USER_VALIDATED_VERTICAL_SLICE_PASS
USER_VALIDATED_WITH_FOLLOWUP
REWORK_REQUIRED
BLOCKED_USER_VALIDATION
```

Core 의미 변경은 Phase 1, 설계·가독성·acceptance는 Phase 2, asset 문제는 Phase 3, bug/runtime/build는 Phase 4를 bounded reopen한다.

**Exit:** actual user play evidence, finding/feedback, next decision, Canonical Reflection After Play가 Project canon에 기록·readback된 뒤 `USER_VALIDATED_VERTICAL_SLICE`.

## 6. Vertical Slice 완료 범위

```text
REPRESENTATIVE_EXPERIENCE_REQUIRED
SHIPPING_INTENT_SLICE_QUALITY_REQUIRED
CRITICAL_PLAYER_FACING_PLACEHOLDER_FORBIDDEN
WHOLE_GAME_COMPLETION_NOT_REQUIRED
FINAL_ALL_PLATFORM_PASS_NOT_REQUIRED
FINAL_STORE_RELEASE_PASS_NOT_REQUIRED
```

Phase 4에는 current Slice가 약속한 representative flow가 actual build에서 처음부터 끝까지 실행되고 core systems와 실제 consumer가 연결되며, 필요한 범위의 shipping-intent UI/Visual/Audio/VFX/feedback, machine evidence, exact identity, launch route가 있어야 한다. critical player-facing placeholder로 목표 품질을 위장할 수 없다.

Phase 5에는 여기에 actual user play, blocking usability 처리/판정, 핵심 재미·감정·기억·차별점 evidence와 next decision이 추가된다.

전체 게임 콘텐츠, 최종 전체 밸런스, 모든 플랫폼, 최종 localization, store/legal 공개 출시 PASS는 current Vertical Slice 완료 조건이 아니다.

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
DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE
GODOT_EVIDENCE_NOT_APPLICABLE_FOR_NON_GAME
```

비게임/서사 프로젝트는 업무 분리 원칙을 해당 domain production에 adapt하고 Godot/GUT/Hera/game-runtime evidence만 `NOT_APPLICABLE`로 둔다. 비게임 산출물에 game Vertical Slice 완료를 허위 주장하지 않는다.

## 8. 상세 owner routing

```text
startup canon → WORK_PROJECT_START_CANON_CHECKLIST.md
planning/Grill Me → current planning decision owner + Grill Me protocol
packet/approval/fallback/QA/merge → WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
Work↔Codex role → docs/GPT_CODEX_WORKFLOW_POLICY.md
Visual generation/delivery → current image + project-local Visual owners
shipping-intent Slice evidence → skills/designing-vertical-slices/SKILL.md
evidence identity → WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
```

세부 owner와 이 interface가 충돌하면 Project truth를 먼저 확인하고 해당 분야 current specialist owner의 세부 계약을 따른다. 단 사용자 승인 5단계 순서와 Phase 4/5 evidence ceiling을 3단계 macro flow로 다시 압축하지 않는다.
