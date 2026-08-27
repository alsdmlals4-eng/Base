# Work 5단계 버티컬 슬라이스 실행 계약 — 구현 계획

> 승인 근거: 사용자가 Work 프로젝트 실행을 `1) 기획 → 2) 검수 → 3) 이미지·요소 생성 → 4) Codex 구현 → 5) 사용자 검증`으로 명확히 분리하고, 기획의 핵심 요소는 Grill Me·벤치마킹을 통해 사용자와 함께 확정하며, Base와 프로젝트 정본을 실제 확인해 최적화·교정하라고 지시함.

## 목표

현행 `Work preparation → Codex implementation → Work final review` 3단계 묶음을 폐기하지 않고, 그 세부 기능을 **5단계 상위 상태 머신** 아래로 재배치한다.

```text
1. PLANNING_CO_DESIGN
2. PREPRODUCTION_REVIEW
3. GAME_INPUT_PRODUCTION
4. CODEX_IMPLEMENTATION_AND_MACHINE_VERIFICATION
5. USER_VERTICAL_SLICE_VALIDATION
```

각 단계는 entry evidence, 허용 mutation, exit gate, blocker, 다음 단계가 있어야 하며 앞 단계의 exit gate 없이 다음 단계로 넘어가지 않는다.

## 현행 실검증 결과

Base latest completed main과 등록 프로젝트 정본을 프로그램으로 대조한 결과:

- Codex 단일 구현 window와 Human/Player `NOT_RUN` 경계는 명시되어 있음.
- 기획·검수·Visual/Audio/Data 제작은 기존 `Stage A — Work preparation` 안에 합쳐져 있어 독립 transition gate가 없음.
- Grill Me 정책은 존재하지만 current Starter/Profile에서 Stage 1 핵심 기획 공동 결정 Gate로 강제되지 않음.
- `AUTOMATED_VERTICAL_SLICE_READY`는 존재하지만 사용자 실제 플레이 뒤의 `USER_VALIDATED_VERTICAL_SLICE_COMPLETE`가 독립 완료 상태로 고정되지 않음.
- 프로젝트 정본 다수도 명시적 5단계 토큰보다 기존 Work/Codex 또는 개별 handoff 표현을 사용함.

## 설계 원칙

### 상위 상태 머신, 하위 owner 재사용

새 계약은 세부 Visual·Audio·Git·Godot·CI 절차를 복제하지 않는다.

- 시작 정본 확인: `WORK_PROJECT_START_CANON_CHECKLIST.md`
- Work 최소 전환: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- 로컬 Visual: `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
- evidence identity: `WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`
- Grill Me: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- detailed current Base/Project owners

### Stage 1 사용자 공동 기획

핵심 재미·player promise·meaningful choice·core system role·감정 목표·첫 세션 기억·판매 포인트·Slice 경계는 기존 승인 정본이 없고 material ambiguity가 남을 때 routine auto-approval하지 않는다.

```text
current canon / reuse / benchmark
→ 최소 3개 실질 대안
→ benchmark-informed batched Grill Me
→ 사용자 선택·수정·승인
→ STAGE_1_PLANNING_USER_ALIGNED
```

이미 승인된 Decision은 재질문하지 않고 readback·충돌 검사만 한다.

### Stage 2 독립 검수

기획과 production을 분리한다. Requirement Traceability, 적대적 검토, IRG, 범위·구현 가능성·UI 이해·asset coverage·권리·비용·acceptance·testability를 확인하여 blocking finding 0에서만 통과한다.

### Stage 3 Work 제작

실제 consumer가 있는 Visual·Audio·UI·Data·VFX·localization/accessibility input을 Work에서 생성·검수·정본화한다. 제품 code/Scene/runtime wiring은 금지하며, Codex가 소비 가능한 tracked locator와 Work packet까지 닫는다.

### Stage 4 Codex 구현과 Machine QA

Codex가 actual code·Scene·Resource·runtime wiring을 구현하고 deterministic/runtime/screen/build/CI를 실제 실행한다. Work final evidence review·valid finding 교정·safe merge·post-merge readback까지 포함해 `AUTOMATED_VERTICAL_SLICE_READY`로 닫는다.

### Stage 5 사용자 검증

다운로드 가능한 build를 사용자가 실제로 실행·플레이한다. Human usability와 Player Experience는 이 단계 전까지 `NOT_RUN`이다. P0/P1 feedback을 교정·재검증하고 canon에 반영한 뒤에만 `USER_VALIDATED_VERTICAL_SLICE_COMPLETE`다.

## 버티컬 슬라이스 완료 정의

### Automated-ready

다음을 실제 증거로 충족한다.

```text
start/context
→ readable goal
→ player action + meaningful choice
→ system consequence
→ Visual/Audio/UI feedback
→ reward or failure learning
→ retry/exit/next action
```

그리고 actual-consumer assets, required tests/runtime/build, downloadable artifact, exact-head CI, merge/readback, machine-executable remaining work 0, blocking finding 0이 필요하다.

### User-validated complete

사용자가 build를 실행해 대표 loop를 완료하고 이해·조작·핵심 약속·피드백·첫인상을 검증한다. P0/P1은 수정·재검증하거나 사용자가 명시적으로 수용/보류해야 한다. 그 뒤 canon과 다음 action을 갱신한다.

전체 게임 완료 또는 출시 완료와 동일하지 않다.

## 구현 경로

1. RED contract test 추가.
2. 새 얇은 5단계 owner 추가.
3. Router·Starter·Profile·Startup Checklist·Grill Me policy에 current owner routing 추가.
4. exact-head focused/core regression.
5. 최소 5회 full-scope adversarial review.
6. safe squash merge와 post-merge readback.
7. 최종 단일 Work 작업지시문 산출물 갱신.

## 보호 범위

- 프로젝트 전용 이름·PR·SHA·경로·화풍·수치·다음 우선순위를 Base에 고정하지 않음.
- 다른 open PR은 read-only.
- direct main, force, reset/clean, ruleset bypass 금지.
- 새 도구·provider·비용·engine baseline·CI workflow 변경 없음.
- Human/Player evidence 과장 금지.

## Rollback

새 owner routing과 관련 contract commit을 revert한다. 기존 Startup Checklist, minimum-transition, local Visual, evidence identity owner와 프로젝트 runtime은 독립적으로 유지한다.
