# Work 프로젝트 실행 Current Router

```text
WORK_PROJECT_EXECUTION_CURRENT_ROUTER
THIN_ROUTER_NOT_SECOND_CANON
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
CURRENT_BASE_OWNER_WINS_ON_DRIFT
FIVE_STAGE_VERTICAL_SLICE_FLOW_REQUIRED
MACRO_STAGE_IS_NOT_WORK_MODE
GAME_PROJECT_ONLY
NON_GAME_PROJECT_NOT_APPLICABLE
```

> 프로젝트 사실·세부 절차를 복제하지 않고 현재 owner를 연결하는 얇은 진입점이다. 게임 프로젝트의 공용 macro flow는 아래 5단계이며, Project의 `PLAN / BUILD / REVIEW` 같은 Work Mode는 각 단계 안에서 쓰는 작업 방식이지 이 5단계를 대체하지 않는다. 비게임 프로젝트는 `NON_GAME_PROJECT_NOT_APPLICABLE`이다.

## 1. 권위와 로드 순서

```text
사용자의 최신 명시 지시
→ Project AGENTS / Active Context / 승인 Decision
→ Project GitHub·Notion 분야별 current canon
→ 실제 code/data/Scene/Resource/asset/test/runtime evidence
→ Project가 채택한 current Base owner
→ Base latest completed main
→ 과거 채팅·Memory·handoff
```

```text
1. exact Project identity / GitHub / Notion / actual implementation
2. Base latest main / root AGENTS / current Skill Registry inventory
3. WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md
4. WORK_PROJECT_START_CANON_CHECKLIST.md
5. WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
6. WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
7. trigger되는 current Base·Project 전문 owner
```

과거 대화와 Memory는 discovery 후보일 뿐이다. 충돌하면 `CONTEXT_DRIFT_RECHECK_REQUIRED`로 되돌린다.

## 2. 시작 전 정본 교정

새 기획·production·Codex mutation 전에 `WORK_PROJECT_START_CANON_CHECKLIST.md`로 확인한다.

```text
핵심 재미 / player promise
핵심 시스템 / actual consumer
evidence-based SWOT
current stage / active Slice / accepted frontier
구현·test·Visual·Audio 상태
남은 required work
dependency·player value·risk 기반 작업순서
stale·duplicate·conflict·missing canon
GitHub structured / Notion human canon readback
```

승인 범위의 작은 정본 결함은 먼저 교정한다. Core·주요 UX·경제·서사·Art Direction처럼 제품 의미가 바뀌는 결정만 사용자 결정으로 남긴다.

## 3. 게임 프로젝트 Work 5단계 macro flow

`WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`가 상세 Gate를 소유한다. `MINIMIZE_WORK_CODEX_TRANSITIONS`는 단계를 합친다는 뜻이 아니라 **1~3단계를 Work에서 닫고 4단계 Codex를 한 번의 구현 window로 묶는다**는 뜻이다.

### 1단계 — 기획

```text
STAGE_1_PLANNING
USER_COLLABORATIVE_CORE_PLANNING_REQUIRED
GRILL_ME_FOR_MATERIAL_CORE_DECISIONS
DECISION_RELEVANT_BENCHMARK_REQUIRED
THREE_MATERIALLY_DISTINCT_APPROACHES
ADOPT / ADAPT / REJECT
```

Project canon·실제 구현·기존 승인 자산·Base reusable evidence를 먼저 읽는다. 아직 승인되지 않은 핵심 player promise·대표 행동·meaningful choice·trade-off·보상/실패 학습·목표 감정/기억·첫인상·세일즈포인트·Slice 가설/acceptance처럼 제품 의미를 바꾸는 항목은 Grill Me와 결정 관련 벤치마킹으로 사용자와 함께 닫는다. 저장소에서 이미 확인되는 사실, 구현 세부, 가역적 초기값은 다시 묻지 않는다.

### 2단계 — 검수

```text
STAGE_2_PRE_PRODUCTION_REVIEW
PRE_PRODUCTION_REVIEW_CLEAN
NO_ASSET_PRODUCTION_BEFORE_REVIEW_CLEAN
NO_CODEX_PRODUCT_MUTATION_BEFORE_REVIEW_CLEAN
```

1단계 계약을 Project/Notion/actual implementation, Existing Solution First, benchmark applicability, player choice, UI/UX, data/state/save, actual consumer, rights/provenance, acceptance, QA/evidence ceiling 관점에서 적대적으로 검수·교정한다. 제품 의미가 바뀌는 finding은 1단계 사용자 결정으로 되돌리고, `PRE_PRODUCTION_REVIEW_CLEAN` 전에는 production asset 제작이나 Codex 제품 mutation을 시작하지 않는다.

### 3단계 — 이미지·요소 생성

```text
STAGE_3_ASSET_AND_ELEMENT_PRODUCTION
ACTUAL_CONSUMER_REQUIRED
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

검수된 current Slice의 실제 consumer가 있는 Visual·Audio·UI source·VFX·runtime-consumed data/content만 제작·정리한다. 설명용 시트나 consumer 없는 이미지를 production asset으로 만들지 않는다. Project/host의 별도 이미지 승인 Gate가 있으면 그대로 우선한다. durable locator·provenance·rights·format/import·acceptance까지 닫아 Codex 입력 패킷으로 만든다.

### 4단계 — 구현(Codex) + machine closure

```text
STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSURE
CODEX_SINGLE_IMPLEMENTATION_WINDOW
WORK_FINAL_EVIDENCE_REVIEW_IS_STAGE4_CLOSEOUT
WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION
```

Codex가 actual code·Scene·Resource·runtime wiring·test·build를 한 구현 window에서 처리한다. 반환 뒤 Work의 diff/runtime/evidence 검수, valid correction, canon sync, exact-head CI, safe merge, post-merge readback은 별도 6단계가 아니라 **4단계 closeout**이다.

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

이 시점은 machine-executable current-Slice required work가 0이고 사용자에게 줄 exact build/launch route가 준비된 상태이지, 버티컬 슬라이스 최종 완료가 아니다.

### 5단계 — 사용자 검증

```text
STAGE_5_USER_VALIDATION
ACTUAL_USER_PLAY_REQUIRED
AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE
NEXT_SLICE_REQUIRES_STAGE5_DECISION
```

사용자가 4단계의 exact build/scene을 실제 플레이하고 조작 이해, meaningful choice, 피드백·보상·실패 학습, UI/Visual/Audio 지각, 감정·기억·첫인상·핵심 세일즈포인트를 검증한다. 실제 플레이 evidence와 `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP` 계열 Decision Gate가 기록·readback된 뒤에만 `VERTICAL_SLICE_VALIDATED_COMPLETE`를 사용할 수 있다. 사용자 검증 전에는 다음 Slice로 자동 진입하지 않는다.

## 4. Project-local Visual opt-in

사용자가 이미지 binary를 각 프로젝트가 소유하도록 명시하면 함께 적용한다.

```text
WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md
PROJECT_LOCAL_VISUAL_BINARY_FIRST
NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY
NO_NOTION_BINARY_UPLOAD_REQUIRED
```

```text
Notion 구조·Art Direction fresh-read
→ project-local candidate
→ format/dimensions/SHA-256/provenance/rights readback
→ PROJECT_ASSET_APPROVED
→ tracked project asset + ASSET_MANIFEST
→ commit/push/remote readback
→ Codex project-relative locator
→ Godot import/runtime consumer evidence
```

Notion text/status를 수정했으면 readback한다. binary를 올리지 않았으면 업로드했다고 주장하지 않는다. Project별 binary owner가 있으면 그 결정이 우선한다.

## 5. Evidence identity

`WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md`로 분리한다.

```text
product baseline SHA != documentation/router sync SHA
current validation HEAD != build/runtime candidate HEAD
TEST_LOGIC_PASS != CI_GATE_PASS
Godot import cache != product source
LOCAL_VISUAL_CANDIDATE != PROJECT_ASSET_APPROVED != RUNTIME_PROMOTED
local commit != remote synchronized
machine QA != Human usability != Player Experience
```

player-facing bytes 또는 package 설정이 바뀌면 영향 후보를 supersede하고 필요한 Gate를 다시 수행한다.

## 6. 안전 자동화와 완료

```text
remote/upstream/default branch 발견
→ fetch
→ clean·tracking·non-diverged일 때만 pull --ff-only
→ current-task branch commit/push/remote readback
→ PR / exact-head required checks / squash merge
→ post-merge main readback

exact project/worktree/Godot/session
→ Editor/game/GUT/Hera 또는 adopted equivalent
→ runtime/screen/build evidence
```

금지: direct main / force push / blind stash·reset·clean·rebase / 다른 open PR takeover / 무관한 앱·파일·credential·OS 보안 조작 / 새 유료 비용 / 공개 Release·스토어 게시.

```text
bounded retry
→ evidence-equivalent fallback
→ 막힌 task만 defer
→ 독립 ready work 계속
→ current Slice machine-executable required work = 0
→ completion rescan
→ 최소 5회 full-scope adversarial review
→ blocking finding 0
```

다운로드 가능한 internal build와 사용자 검증 패킷을 제공한다. `AUTOMATED_VERTICAL_SLICE_READY`는 Stage 5 입장 조건이며 `VERTICAL_SLICE_VALIDATED_COMPLETE`가 아니다.

## 7. Project-specific 값

프로젝트명·캐릭터·세계관·특정 PR/Issue/Task/Decision·SHA·경로·해상도·HUD·palette·Art Style·완료 목록·우선순위·현재 `macro_stage`는 exact Project canon에서 fresh-read한다.

```text
PROJECT_WORK_MACRO_FLOW = CURRENT_BASE_FIVE_STAGE_VERTICAL_SLICE_FLOW
PROJECT_SPECIFIC_STAGE_STATE = RESOLVE_FROM_CURRENT_PROJECT_CANON
```
