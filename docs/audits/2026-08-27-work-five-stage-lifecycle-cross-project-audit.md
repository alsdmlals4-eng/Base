# Work 5단계 버티컬 슬라이스 Lifecycle — Base·Project·Notion 교차 감사

```text
AUDIT_ONLY_NOT_PROJECT_CANON
ACTUAL_SOURCE_READ_REQUIRED
FIVE_STAGE_GAP_VERIFIED
PROJECT_SPECIFIC_GATE_PRESERVED
```

## 1. 감사 목적

다음을 추측이 아니라 current source readback으로 확인했다.

1. Work가 `기획 → 검수 → 이미지·요소 생성 → Codex 구현 → 사용자 검증`으로 실제 분리돼 있는가.
2. 각 단계의 입구·출구·재진입·증거가 분명한가.
3. `AUTOMATED_VERTICAL_SLICE_READY`와 최종 `VERTICAL_SLICE_COMPLETE`의 경계가 명확한가.
4. 핵심 기획이 unresolved일 때 Grill Me·벤치마킹·사용자 공동결정으로 닫히는가.
5. 공용 교정이 각 프로젝트의 강한 정본·Human/device Gate·비게임 예외를 덮어쓰지 않는가.

기준 Base completed main:

```text
9b45125d087521fa98696cbd1e857bf2ffbf816a
```

## 2. Base current owner 감사

### 2.1 확인한 owner

- `WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md`
- `WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
- `WORK_PROJECT_START_CANON_CHECKLIST.md`
- `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
- `WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`
- `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- `skills/designing-vertical-slices/SKILL.md`

### 2.2 실제 finding

현재 Base에는 필요한 capability가 대부분 존재했다.

- Startup Checklist: 핵심 재미·핵심 시스템·SWOT·current stage·남은 작업·작업순서·정본 선교정
- Grill Me: Core Loop·뾰족한 재미·주요 시스템/UX/경제/서사/Art Direction/MVP 범위 같은 제품 의미 결정
- minimum-transition profile: Work 입력 완료 → Codex 단일 구현 → Work final review → user handoff
- Vertical Slice Skill: release-near/shipping-intent, P0/P1 actual consumer, Visual/Audio/VFX·UI·data·content 연결, no player-facing placeholder
- IRG/evidence identity: file/test/build/runtime/Human/Player evidence 분리

그러나 공개 lifecycle은 `Work preparation → Codex → Work final review/user handoff`의 3단계 집계였다. Work preparation 안에 기획·검수·Visual/Audio/Data 입력 준비가 함께 들어 있어 다음 Gate가 독립적으로 기계 판독되지 않았다.

```text
PLANNING_APPROVED
PREPRODUCTION_REVIEW_APPROVED
GAME_INPUT_PRODUCTION_READY
```

또한 Grill Me가 존재해도 현재 Starter/Profile의 planning exit와 직접 연결되지 않아 standing routine approval이 unresolved core planning까지 자동 승인하는 것으로 오인될 수 있었다.

판정:

```text
CAPABILITY_PRESENT_BUT_STAGE_BOUNDARY_NOT_EXPLICIT
FIVE_STAGE_GAP_VERIFIED
```

## 3. 프로젝트 GitHub current authority 감사

### GRIMOIRE

- root `AGENTS.md`에서 `product_stage: DEMO_FIRST_VERTICAL_SLICE`.
- Task9는 `MERGED_MAIN_AUTOMATED_VERTICAL_SLICE_READY`.
- 다음 Gate는 `TASK9_USER_VERTICAL_SLICE_VALIDATION_PENDING`.
- Human/full vertical slice evidence는 `NOT_RUN`.

의미: 자동 구현 완료와 사용자 검증 완료를 이미 분리하는 강한 프로젝트 사례다.

### MylittleBoat

- core promise/loop와 Visual/Audio 중심 cozy voyage 방향은 명확하다.
- 코드 변경에는 Godot check를 요구하나 공용 5단계 stage vocabulary는 없다.

의미: 공용 lifecycle이 핵심 방향을 덮지 않고 stage routing만 제공해야 한다.

### Switchy Express

- fresh authority → benchmark → RED-first → exact evidence → 5-pass → merge/Notion readback을 요구한다.
- current next gate는 post-change exact package candidate와 physical/device/human gates다.

의미: Stage 4 machine closeout과 Stage 5 physical/human validation을 분리해야 한다.

### Omenward

- current Decision/Active Context가 planning·implementation·Visual route를 소유한다.
- actual runtime/Human evidence를 실행 전 PASS로 올리지 않는다.

의미: already-approved Decision을 Stage 1에서 재질문하지 않아야 한다.

### Tetris

- production canon, exact runtime image consumer, implementation isolation, Human evidence contract가 강하다.
- automated tests가 fun/readability/onboarding/choice quality를 증명하지 않는다고 명시한다.

의미: Stage 3 actual-consumer asset Gate와 Stage 5 user evidence가 필수다.

### Ninja Survival

- current phase rule은 `PLAN/canon/product decision → DoR → BUILD/TDD → exact verification → adversarial review → merge/readback`.
- release-near Cheonsul slice를 네 유파 full production 전에 요구한다.

의미: Stage 1·2·4가 이미 의미상 존재하지만 공용 명칭은 다르다.

### Ten Paces Hidden Moves

- Work Mode를 `PLAN / BUILD / REVIEW`로 명시한다.
- root canon은 1대1 10칸 전장과 3/3/4 planning을 보호한다.

의미: 기존 Work Mode를 폐기하지 않고 5단계의 내부 owner mapping으로 유지해야 한다.

### Blacksmith

- current 상태는 PLAN이고 implementation은 planning completion 선언 전 차단된다.
- benchmark/research → brainstorming/adversarial review → RED/GREEN/REFACTOR → verification/readback 순서를 갖는다.
- 신규 이미지는 actual game consumer가 필요하다.

의미: Stage 1/2/3 분리와 current Project planning Gate 우선이 필요하다.

### urban-legend

- Work Mode는 PLAN/BUILD/REVIEW.
- current Gate는 Planning Complete이지만 runtime implementation은 별도 authorization이며 Human QA는 `NOT_RUN`.
- M04는 release-near player-experience Vertical Slice다.

의미: planning completion과 product implementation/user experience completion이 다르다.

### Coc-Fiction

- 게임 runtime 프로젝트가 아니며 Godot rules가 `NOT_APPLICABLE`.
- 원고/scene-pass/packaging lifecycle을 사용한다.

의미: 게임 product 5단계를 모든 Base 소비자에게 universal hardcode하면 회귀다.

판정:

```text
GAME_PRODUCT_FIVE_STAGE_LIFECYCLE_ONLY
PROJECT_SPECIFIC_GATE_PRESERVED
NON_GAME_PROJECT_REQUIRES_PROJECT_SPECIFIC_ADAPTER
```

## 4. Project Notion current surface 감사

### 십보강호 · `13 · 기획 완료 · Visual/구현 Handoff`

실제 페이지는 다음을 분리한다.

```text
PLANNING COMPLETE
!= product implementation
!= Human PASS
!= Android PASS

Planning Complete
→ Visual/UX Requirement & Reference Review
→ 별도 implementation authorization
→ implementation
```

Visual/UX review에서 core conflict가 나오면 planning을 해당 범위만 reopen한다.

### 괴이기록국 · `09 · Vertical Slice · 플레이 검증 계약`

실제 페이지는 release-near Vertical Slice를 기술 PoC가 아니라 재미·첫인상·가독성·추리 인과·관계·기록의 실제 플레이 경험 검증으로 정의한다.

완료에는 다음이 필요하다고 명시한다.

```text
runtime implementation
+ Audio/VFX
+ concrete art
+ Human QA
```

planning closure·자동 테스트·문서 completion을 player-experience PASS로 사용하지 않는다.

### Project Home 공통 구조

검색·fetch한 Project Home은 핵심 Flow·시스템·Visual·현재 상태를 사람에게 보여 주는 구조를 이미 갖는다. 그러나 전체 portfolio가 동일한 5단계 status vocabulary와 Definition of Ready/Done을 사용하지는 않는다.

판정:

- repository structured receipt가 exact stage identity를 소유한다.
- Notion은 사람이 이해하는 current stage·핵심 결정·미검증·다음 사용자 행동을 요약한다.
- 모든 Project Notion을 일괄 재구축하지 않는다.
- 각 프로젝트 다음 material Work에서 current stage를 5단계에 mapping하고 필요한 text/status만 bounded correction한다.

## 5. 외부 공식·현업 벤치마크

### Unity Learn · Vertical Slice 정의

- https://learn.unity.com/tutorial/66f53a14edbc2a0e75d4fe90
- functioning part of a larger game이며 final game이 어떻게 보이고 플레이될지 시험하는 용도라고 설명한다.

적용:

```text
system-only PoC → REJECT as completed vertical slice
representative functioning player flow → ADOPT
```

### Game Developer · Milestone 정의

- https://www.gamedeveloper.com/production/do-you-have-a-firm-definition-of-your-milestones-
- documentation, end of pre-dev, prototype, vertical slice의 납품 품질·시간·예산을 사전 합의해야 한다고 설명한다.
- vertical slice가 art/audio를 포함한 final-polish 수준인지 명시하지 않으면 demo hell과 production delay가 발생할 수 있다고 경고한다.

적용:

```text
Stage별 Definition of Ready/Done → ADOPT
무제한 final-polish 확대 → REJECT
current Slice의 P0/P1 + 필요한 P2 quality bar → ADAPT
```

### Godot 공식 Export 문서

- https://docs.godotengine.org/en/4.6/tutorials/export/exporting_projects.html
- `Export Project`는 executable + project data의 playable build를 만든다.
- `Export PCK/ZIP`은 project data만 내보내며 playable build가 아니다.

적용:

```text
PCK/ZIP only != user-runnable vertical slice
Stage 4 downloadable build = executable + required project data + launch smoke
```

### Usability testing

- https://www.nngroup.com/courses/usability-testing/
- usability testing은 실제 사용자의 문제·기회를 관찰하는 별도 검증 활동이다.

적용:

```text
Machine QA != Human usability
Stage 5 actual user play required for final completion
```

## 6. 비교안과 결정

| 안 | 장점 | 실패 | 판정 |
|---|---|---|---|
| 기존 3단계의 이름만 5개로 변경 | 변경량 최소 | planning/review/input Gate가 실제로 분리되지 않음 | REJECT |
| 얇은 5단계 owner + 기존 전문 owner 조합 | 명확한 public stages, 최소 전환, 비퇴행 | routing/test 추가 필요 | ADOPT |
| minimum-transition profile 전체 재작성 | 한 파일 집중 | second canon·context·회귀·유지비 | REJECT |

## 7. 교정 목표

```text
STAGE_0_PREFLIGHT
→ STAGE_1_PLANNING_WITH_USER
→ STAGE_2_PREPRODUCTION_REVIEW
→ STAGE_3_GAME_INPUT_PRODUCTION
→ STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ STAGE_5_USER_VERTICAL_SLICE_VALIDATION
```

핵심 완료 경계:

```text
AUTOMATED_VERTICAL_SLICE_READY
!= VERTICAL_SLICE_COMPLETE

USER_VALIDATED_VERTICAL_SLICE
+ canonical reflection/readback
+ accepted/corrected blocking findings
→ VERTICAL_SLICE_COMPLETE
```

## 8. Evidence ceiling

이 감사와 Base 계약의 PASS는 특정 프로젝트의 실제 5단계 완료를 뜻하지 않는다.

```text
source read
!= project stage packet written
!= asset produced
!= Codex implementation
!= runtime/build
!= user played
!= Vertical Slice complete
```

각 프로젝트는 다음 material Work에서 current exact evidence로 stage를 복원한다.
