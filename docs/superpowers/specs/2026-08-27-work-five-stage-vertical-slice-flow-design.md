# Work 5단계 버티컬 슬라이스 실행 흐름 설계

## 목표

게임 프로젝트를 ChatGPT Work에서 진행할 때 공용 macro workflow를 다음 5단계로 명확히 고정한다.

```text
1. 기획
2. 검수
3. 이미지·요소 생성
4. 구현(Codex)
5. 사용자 검증
```

이 설계는 Work↔Codex 왕복을 늘리기 위한 것이 아니다. Work 안에서 구현 전 작업을 세 개의 명확한 Gate로 분리하고, 실제 Godot 제품 구현은 한 번의 Codex window로 묶으며, 사용자 검증 전 상태를 버티컬 슬라이스 완료로 오해하지 않게 하는 것이 목적이다.

## 실검증에서 확인한 현재 상태

2026-08-27 Base latest completed main `9b45125d087521fa98696cbd1e857bf2ffbf816a`와 대표 프로젝트 current canon/Notion을 대조했다.

- `WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`는 Work 준비 → Codex → Work final review → 사용자 검증 준비의 큰 흐름을 갖고 있다.
- `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`는 구현 전의 기획·검수·Visual/Audio/VFX 준비를 하나의 `Stage A — Work preparation`에 합친 **three-stage minimum-transition flow**를 사용한다.
- `GPT_CODEX_WORKFLOW_POLICY.md`도 GPT 구현 전 패키지 안에서 기획·벤치마킹·적대적 검토·Visual/Audio requirement를 연속 처리한다.
- `PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`와 Grill Me 프로토콜은 중요한 기획 충돌·코어 결정에 Grill Me를 제공하지만, 새 버티컬 슬라이스의 핵심 player-value 요소를 처음 만들 때 반드시 사용자와 공동 설계하는 macro Gate로는 노출되지 않는다.
- `designing-vertical-slices/SKILL.md`의 Definition of Done은 실제 사람 플레이 evidence까지 요구한다. 반면 최소전환 프로필과 일부 Project/Notion은 사람 검증 전 상태를 `AUTOMATED_VERTICAL_SLICE_READY`라고 표현한다. 내부적으로 evidence ceiling은 분리되어 있지만, ‘완성’ 용어가 혼동될 여지가 있다.
- 일부 프로젝트 AGENTS는 `PLAN / BUILD / REVIEW` 또는 자체 작업순서를 current macro flow처럼 노출하고 있어 5단계 공용 흐름과 명칭이 일치하지 않는다.
- `Coc-Fiction`은 게임 런타임 프로젝트가 아니므로 이 5단계 Godot/Codex 버티컬 슬라이스 계약은 적용 대상이 아니다.

## 설계 원칙

```text
FIVE_STAGE_VERTICAL_SLICE_FLOW_REQUIRED
MACRO_STAGE_IS_NOT_WORK_MODE
MINIMIZE_WORK_CODEX_TRANSITIONS_PRESERVED
CURRENT_PROJECT_CANON_FIRST
CURRENT_BASE_OWNER_WINS_FOR_SHARED_METHOD
GAME_PROJECT_ONLY
NON_GAME_PROJECT_NOT_APPLICABLE
AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE
NEXT_SLICE_REQUIRES_STAGE5_DECISION
```

`PLAN / BUILD / REVIEW` 같은 Work Mode는 한 단계 안에서 사용할 작업 방식이다. 5단계 macro stage를 대체하지 않는다.

## 1단계 — 기획

```text
STAGE_1_PLANNING
USER_COLLABORATIVE_CORE_PLANNING_REQUIRED
GRILL_ME_FOR_MATERIAL_CORE_DECISIONS
DECISION_RELEVANT_BENCHMARK_REQUIRED
EXISTING_SOLUTION_FIRST
```

새 Slice 또는 material한 재설계에서 아직 승인되지 않은 핵심 요소는 GPT가 단독 확정하지 않는다. 현재 Project canon·실제 구현·기존 승인 자산·Base reusable evidence를 먼저 읽고, 실제 사용자 결정이 필요한 항목만 Grill Me로 사용자와 함께 닫는다.

핵심 공동 설계 대상:

- player promise / 핵심 판타지
- 대표 player action
- meaningful choice와 trade-off
- 결과·보상·실패 학습
- 목표 감정·기억·다음 동기
- 첫 세션에서 보여줄 대표 경험
- 핵심 세일즈포인트·차별점
- Slice research question / observable signal / acceptance
- included scope / explicit non-scope / protected scope

결정에 실질적 대안이 있으면 최소 3개의 materially distinct approach를 비교한다. 조사 순서는 현재 프로젝트 → 승인 자산/reference → Base reusable evidence → 직접 관련된 검증 프로젝트 사례 → 공식·현업·시장 성공/실패 사례이며, 최종 disposition은 `ADOPT / ADAPT / REJECT`를 기본으로 한다.

저장소에서 이미 확정된 사실, 가역적 기술 세부, 초기 시험값은 Grill Me 질문으로 전가하지 않는다.

### 1단계 Exit

```text
SLICE_PLANNING_LOCKED
```

- 핵심 player-value trace가 승인됨.
- 필요한 Decision이 current Project structured/human canon에 기록되고 readback됨.
- 구현 방법의 Node/Scene/함수 구조는 Codex 자율 영역으로 남음.
- 미해결 core/UX/economy/narrative/Art Direction 결정이 현재 Slice acceptance를 바꾸지 않음.

## 2단계 — 검수

```text
STAGE_2_PRE_PRODUCTION_REVIEW
NO_ASSET_PRODUCTION_BEFORE_REVIEW_CLEAN
NO_CODEX_PRODUCT_MUTATION_BEFORE_REVIEW_CLEAN
```

1단계 기획을 새로 늘리는 단계가 아니라, 이미 잡힌 Slice 계약을 공격·검증·축소·교정하는 단계다.

필수 검수:

- Project GitHub/Notion/actual implementation drift
- Existing Solution First 누락
- benchmark applicability와 surface-copy 위험
- player choice가 실제 고민인지
- UI/UX 정보 전달과 edge case
- actual consumer / data/state / save/schema 영향
- Visual/Audio/VFX requirement와 실제 소비처
- 권리/provenance/release 위험
- acceptance / deterministic QA / runtime QA / evidence ceiling
- 최소 5회 full-scope adversarial review는 final clean exit에서 충족

기획 의미를 바꾸는 finding이면 1단계로 되돌아가 사용자 Decision을 갱신한다. 단순 누락·오류·검증 강화는 2단계 안에서 교정한다.

### 2단계 Exit

```text
PRE_PRODUCTION_REVIEW_CLEAN
PRODUCTION_REQUIREMENTS_LOCKED
```

P0/P1 또는 material planning conflict가 0이고, 어떤 실제 게임 입력을 왜 만들어야 하는지 consumer와 acceptance가 고정돼야 한다.

## 3단계 — 이미지·요소 생성

```text
STAGE_3_ASSET_AND_ELEMENT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
PRODUCTION_INPUTS_BEFORE_CODEX
```

2단계를 통과한 current Slice에 실제 필요한 player-facing/non-code 입력만 제작·정리한다.

포함 대상:

- production Visual/image/animation source asset
- Audio/SFX/music source 또는 승인 procedural spec
- UI source elements / icon / font usage record
- VFX presentation requirement/source
- runtime-consumed data/content authored outside Codex implementation
- provenance/rights/import/format/manifest/locator

설명용 시트나 실제 consumer 없는 이미지를 production asset으로 만들지 않는다. 현재 대화·Project가 이미지 생성에 별도 명시 승인 Gate를 요구하면 그 Gate가 우선한다. 이 공용 단계는 host/tool confirmation을 우회하지 않는다.

에셋 생성 중 제품 의미가 바뀌면 1단계, requirement/consumer 결함이면 2단계로 되돌린다.

### 3단계 Exit

```text
WORK_PRODUCTION_INPUT_PACKET_READY
READY_FOR_SINGLE_CODEX_WINDOW
```

승인 자산·data·UI/UX·acceptance·QA 입력의 durable locator와 exact consumer가 닫혀 있어야 한다.

## 4단계 — 구현(Codex)

```text
STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSURE
CODEX_SINGLE_IMPLEMENTATION_WINDOW
WORK_FINAL_EVIDENCE_REVIEW_IS_STAGE4_CLOSEOUT
```

Codex는 Project GitHub + Notion을 fresh-read하고 actual Godot code/Scene/Resource/runtime wiring/test/build를 구현한다. Routine technical choice, reversible refactor, bug fix와 test는 Codex가 승인 범위 안에서 연속 처리한다.

Codex 반환 뒤 Work가 수행하는 구현 일치·runtime evidence·Visual/Audio consumer·machine QA·canon sync·PR/merge/readback 검수는 **별도 macro 6단계가 아니라 4단계 closeout**이다.

### 4단계 Exit

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

필수:

- current Slice machine-executable required work = 0
- actual code/Scene/Resource/runtime wiring present
- required deterministic/runtime/screen/build QA complete or legitimate explicit environment gate
- player-facing required Visual/Audio/UI/VFX/data actually consumed
- no placeholder that invalidates shipping-intent quality claim
- exact-head checks / current-task merge / new-main readback complete when applicable
- canon/evidence readback complete
- blocking high-risk item 0
- 최소 5회 full-scope adversarial clean exit
- downloadable/launchable user validation artifact or exact launch route available

이 상태는 **Vertical Slice 완료가 아니다.** 사용자 경험 evidence가 아직 없다.

## 5단계 — 사용자 검증

```text
STAGE_5_USER_VALIDATION
ACTUAL_USER_PLAY_REQUIRED
VERTICAL_SLICE_VALIDATED_COMPLETE_REQUIRES_STAGE5
```

사용자가 4단계 exact build/scene을 실제 플레이한다. 최소한 다음을 구분해 수집한다.

- 진입·조작 이해
- meaningful choice 인지와 고민
- 피드백·보상·실패 학습 이해
- UI/텍스트/Visual/Audio 가독·지각
- 감정·기억·첫인상
- 핵심 세일즈포인트 전달
- 불편·이탈·혼란·재시도 이유

판정:

```text
EXPAND | FIX | TUNE | REDESIGN | REPEAT_SLICE | HOLD | STOP
```

- `FIX/TUNE`은 영향 범위에 맞춰 2/3/4단계로 되돌린다.
- `REDESIGN`은 1단계로 되돌린다.
- `REPEAT_SLICE`는 표본/구간/가설을 다시 고정한다.
- `EXPAND`만 자동으로 다음 Slice를 허용한다는 뜻은 아니며, current project roadmap/decision을 다시 읽고 다음 Stage 1 후보를 잡는다.

### 최종 완료 명칭

```text
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
!=
VERTICAL_SLICE_VALIDATED_COMPLETE
```

`VERTICAL_SLICE_VALIDATED_COMPLETE`는 5단계 실제 사용자 플레이 evidence와 Decision Gate가 기록·readback된 뒤에만 사용한다.

## Project 적용 방식

게임 Project AGENTS/adapter는 이 문서 내용을 복제하지 않는다. 명시적으로 다른 macro workflow를 current로 고정한 프로젝트만 얇게 정렬한다.

```text
PROJECT_WORK_MACRO_FLOW = CURRENT_BASE_FIVE_STAGE_VERTICAL_SLICE_FLOW
PROJECT_SPECIFIC_STAGE_STATE = RESOLVE_FROM_CURRENT_PROJECT_CANON
```

프로젝트별 Core, Slice 범위, Decision, 현재 Stage, 이미지 승인 방식, Human evidence requirement는 Project canon이 계속 소유한다.

비게임 프로젝트는 `NON_GAME_PROJECT_NOT_APPLICABLE`을 사용한다.

## 호환성

기존 consumer가 읽는 다음 token은 유지한다.

- `WORK_PREP_COMPLETION_BEFORE_CODEX`
- `WORK_PRODUCTION_INPUT_BATCH`
- `CODEX_SINGLE_IMPLEMENTATION_WINDOW`
- `WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION`
- `AUTOMATED_VERTICAL_SLICE_READY`
- `READY_FOR_USER_VERTICAL_SLICE_VALIDATION`

단, 이 token들이 macro stage 수를 3개로 정의한다는 해석은 폐기한다.

## 검증 계약

새 regression contract는 최소 다음을 검사한다.

1. current Router와 minimum-transition profile에 5단계 token이 순서대로 존재한다.
2. Stage 1에 Grill Me material-core collaboration과 benchmark/3 alternatives가 연결된다.
3. Stage 2 clean 전 Stage 3/4 진입을 금지한다.
4. Stage 3는 actual consumer를 요구한다.
5. Work final evidence review는 Stage 4 closeout이며 Stage 5보다 앞선다.
6. `AUTOMATED_VERTICAL_SLICE_READY`와 `VERTICAL_SLICE_VALIDATED_COMPLETE`를 구분한다.
7. Stage 5 actual user play와 Decision Gate 없이는 완료/next-slice를 주장하지 않는다.
8. 비게임 프로젝트는 적용 대상이 아니다.
9. 기존 minimum-transition/visual/evidence identity token은 회귀하지 않는다.

## 범위 밖

- 프로젝트별 게임 코어 변경
- Godot 제품 구현
- 이미지 실제 생성
- 새 유료 도구/서비스
- open PR takeover
- Base PR #660의 `grill-me-protocol.md` 등 기존 changed path 수정
