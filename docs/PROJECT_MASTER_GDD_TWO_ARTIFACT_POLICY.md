# Project Master GDD — Desktop GPT 2파일 발행 정책

## 0. 상태와 목적

- Profile ID: `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`
- 상태: `ACTIVE_WHEN_EXPLICITLY_SELECTED`
- 적용 기준: 사용자가 프로젝트 정본을 **사용자용 상세 기획서 PDF + AI용 repository Markdown**의 정확히 두 산출물로 정리하라고 명시한 경우
- 목적: Desktop GPT에서 사람이 읽을 완성도 높은 제작 기획서와 AI/Codex가 실행할 정밀 구현 계약을 중복 surface 없이 유지한다.
- 비목적: 모든 프로젝트의 기본 workspace를 일괄 변경하거나 기존 Notion 자료를 삭제·폐기하는 것

이 profile은 기존 `DOMAIN_SPLIT_CANON` 위에 선택적으로 적용하는 bounded publication profile이다. `GLOBAL_NOTION_DEPRECATION_FORBIDDEN`: 이 문서를 근거로 모든 프로젝트에서 Notion을 폐기하거나 기존 사람용 정본을 자동 삭제하지 않는다.

### 0.1 Base revision fresh-read와 bounded execution

`LATEST_BASE_DISCOVERY_REQUIRED`

`PIN_IS_EVIDENCE_NOT_FRESHNESS_BYPASS`

`PROJECT_ADOPTED_BASE_CONTRACT_PRESERVED`

`BASE_DRIFT_CLASSIFICATION_REQUIRED`

`BASE_EXECUTION_SHA_PINNED_PER_BOUNDED_WORK`

`NO_PERMANENT_STALE_PIN`

`NO_FLOATING_EXECUTION`

`BOUNDARY_FRESH_READ_REQUIRED`

이 profile의 L1+ 작업은 과거에 저장된 Base SHA만 읽고 시작하지 않으며, 작업 도중 이동하는 Base `main`을 매 단계 자동 추종하지도 않는다. 시작 시 최신 completed Base `main`을 fresh-read하고 프로젝트가 채택한 Base 계약·project adapter·프로젝트 정본·실제 구현과 비교해 drift를 분류한 뒤 이번 bounded 작업 또는 플레이 의미 Slice가 실제로 사용할 execution revision을 선택한다.

```yaml
base_observed_head_sha:
base_adopted_contract_sha:
base_execution_sha:
base_drift_classification: NO_RELEVANT_DRIFT | COMPATIBLE_ADOPTION | MIGRATION_REQUIRED | PROJECT_OVERRIDE | BLOCKED_UNVERIFIED
```

- `base_observed_head_sha`: 작업 시작 시 관찰한 최신 completed Base `main`.
- `base_adopted_contract_sha`: 대상 프로젝트가 현재 명시적으로 채택한 Base 계약 revision.
- `base_execution_sha`: drift 분류와 reconcile 뒤 이번 bounded 작업에 실제 적용하는 revision.
- 최신 Base가 더 새롭다는 이유만으로 프로젝트 코어·승인 Decision·실제 구현·채택 계약을 조용히 교체하지 않는다.
- `base_execution_sha`는 한 bounded 작업/Slice 동안 고정한다. 중간에 Base가 바뀌면 관련성·호환성·재검증 범위를 먼저 분류한다.
- 구현 인계, pre-merge, post-merge, closeout에서는 Base 최신 상태를 다시 읽고 drift를 재분류한다. 무관한 변경이면 기존 execution pin을 유지하고, 관련 변경이면 reconcile 후 영향받은 계약·test·consumer를 재검증한다.

## 1. 산출물 계약

`EXACTLY_TWO_DELIVERABLES`

| 구분 | 고정 역할 | 기본 경로 | 사용자 다운로드 |
|---|---|---|---|
| `HUMAN_MASTER_GDD_PDF` | 사람이 프로젝트 전체·핵심 시스템·핵심 콘텐츠·구현 원리를 시각적으로 이해하는 상세 제작 기획서 snapshot | `exports/[PROJECT]_MASTER_PRODUCTION_GDD_[YYYYMMDD].pdf` | 제공 |
| `AI_PRODUCTION_SPEC_MARKDOWN` | GPT/Codex가 후속 기획·구현·테스트·검수를 이어가는 구조화 기획·구현 명세 | `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` | 제공하지 않고 repository 위치만 보고 |

산출물 제한:

- `NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX`
- `NO_SEPARATE_IMAGE_BUNDLE`
- 별도 benchmark 보고서, traceability 표, asset matrix, QA 부록은 만들지 않고 두 산출물 내부에 통합한다.
- 외부 제출처가 다른 형식을 명시한 경우에만 별도 profile 또는 사용자 승인으로 예외를 둔다.

### 1.1 두 산출물 내부의 사람용 Game Blueprint 계층 profile

`HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE`

`NO_SEPARATE_BLUEPRINT_ARTIFACT`

이 profile의 Blueprint는 세 번째 파일·Notion page/view·보드·부록이 아니라, `HUMAN_MASTER_GDD_PDF`와 `AI_PRODUCTION_SPEC_MARKDOWN` 안에 같은 ID로 합성하는 읽기 구조다. `EXACTLY_TWO_DELIVERABLES`가 항상 상위 경계이며 Blueprint, flow card, system card, legend, traceability를 별도 산출물로 발행하지 않는다.

네 reading/composition layer는 다음과 같다.

| Layer token | 사람이 먼저 답할 질문 | 두 산출물 안의 구성 |
|---|---|---|
| `PROJECT_PLAYER_LAYER` | 어떤 게임이며 플레이어가 무엇을 느끼고 배우고 선택하는가? | One-Page Vision, promise/pillar, loop, `FIRST_5_15_30` 경험 |
| `SYSTEM_LAYER` | 핵심 flow와 system은 어떤 선택·규칙·상태·피드백으로 작동하는가? | 핵심 flow/system card, 상태·처리 흐름, 시스템 관계 |
| `CONTENT_UX_PRESENTATION_LAYER` | 어떤 콘텐츠·화면·입력·시청각 표현이 시스템을 전달하는가? | content card, UX flow, UI state, visual/audio consumer |
| `PRODUCTION_EVIDENCE_LAYER` | 누가 어떻게 구현하고 무엇으로 완료를 증명하는가? | scene/node/script/data owner, 구현 순서, test/runtime/UX evidence |

PDF의 목차·요약·cross-reference와 AI Markdown의 registry·상세 section은 다음 읽기 순서를 명시적으로 지원한다.

```text
3-MINUTE PROJECT / PLAYER READ
→ 10-MINUTE SYSTEM + CONTENT / UX / PRESENTATION READ
→ DETAIL READ
→ IMPLEMENTATION READ
→ VERIFICATION READ
```

- `REUSABLE_FLOW_AND_SYSTEM_CARDS`: 중요한 flow와 system은 같은 card schema와 공통 ID를 사용한다. Card에는 player purpose, trigger/input, choice/condition, state/data change, output/feedback, 연결 콘텐츠·UX, implementation owner, acceptance/evidence를 포함하며 PDF와 AI Markdown에서 재사용한다.
- `LAYERED_TRACEABILITY_REQUIRED`: project/player promise → flow/system card → content/UX/presentation consumer → scene/node/script/data → test/runtime/UX evidence를 양방향으로 추적한다.
- `STATE_AND_EVIDENCE_LEGEND`: 상태 token의 의미, 필요한 evidence, 아직 주장할 수 없는 상위 상태를 한 legend로 설명하고 모든 layer에서 같은 상태를 사용한다.
- `CONDITIONAL_MODULE_NA_WITH_REASON`: 프로젝트에 적용되지 않는 장·card field·시각 모듈은 억지로 채우거나 빈 placeholder를 만들지 않고 `N/A — 이유`를 남긴다.
- `REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION`: current authority에 유효한 Blueprint·flow·system representation이 있으면 먼저 재사용하고, 현재 profile과 touched scope에 필요한 부분만 adapt한다.
- `NO_MASS_BLUEPRINT_BACKFILL`: 이 profile을 선택해도 untouched project/system을 일괄 변환하지 않는다. 현재 GDD 범위의 material flow/system만 두 산출물 안에 필요한 최소 깊이로 구성한다.

`PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH`: 전체 프로젝트에는 material system의 지도·책임·경계·의존성·향후 검증 위치를 빠짐없이 연결하되, 구현 가능한 세부 깊이는 현재 다음 `PLAY_MEANINGFUL_WORK_SLICE`에 집중한다. 모든 후반 콘텐츠·수치·화면·자산을 한 번에 확정하는 대형 waterfall로 해석하지 않는다.

#### 1.1.1 Blueprint wireframe 결정 surface

`BLUEPRINT_WIREFRAME_DECISION_SURFACE`

`WIREFRAME_WITHIN_EXISTING_TWO_ARTIFACTS`

`TWO_ARTIFACT_PROFILE_CONDITIONALLY_APPLIES`: 이 규칙은 사용자가 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD` profile을 명시적으로 선택한 경우에만 `HUMAN_MASTER_GDD_PDF`와 `AI_PRODUCTION_SPEC_MARKDOWN` 안에 적용한다. 다른 publication profile은 해당 프로젝트의 현행 design-document owner를 따르며, 이 규칙을 근거로 두 산출물을 강제하거나 중복 Blueprint 원본을 만들지 않는다.

Blueprint wireframe는 세 번째 설계 파일·이미지 묶음·별도 보드가 아니라, 위 profile 안에서는 `HUMAN_MASTER_GDD_PDF`와 `AI_PRODUCTION_SPEC_MARKDOWN`에 같은 `screen_id`로 연결하는 text-native 구조 검토 surface다. 이 surface는 화면의 구도와 동선 결정을 검토하는 자료이며, 실제 UI asset·Godot scene·runtime capture의 대체본이 아니다.

`WIRE_FRAME_ONLY_FOR_MATERIAL_PLAYER_FACING_SURFACE`: player-facing 화면·overlay·전환 중 레이아웃, 입력, 상태 또는 화면 사이 동선이 현재 Blueprint 결정에 material한 것에만 wireframe를 둔다. 비시각 system, 이미 검증되어 그대로 재사용하는 surface 또는 현 scope에 없는 surface는 `NOT_APPLICABLE_WITH_REASON`으로 남기며 빈 frame이나 장식용 화면을 만들지 않는다.

각 적용 wireframe는 최소한 다음을 PDF와 AI Markdown에서 공통 ID로 추적한다.

- `screen_id`, `priority`, target viewport / aspect, input mode
- entry / exit / cancel / re-entry
- player goal·player question과 visual hierarchy
- primary / secondary action
- normal state와 disabled / error / unavailable state 한 가지 이상
- planned or actual consumer, 구현 owner와 `SCREEN_LEVEL_COMPOSITION_REQUIRED` row/reference
- wireframe status, evidence reference와 아직 실행하지 않은 runtime/UX 상태 (`NOT_RUN` 포함)

`SMALLEST_REPRESENTATIVE_WIREFRAME_SET`: 한 Goal·Playable Slice에서 실제 결정·구현 순서·검수에 필요한 가장 작은 대표 화면 집합만 선택한다. 같은 navigation/state contract를 재사용하는 화면은 one-to-many reference로 연결하고, 모든 화면의 backfill을 요구하지 않는다.

`WIREFRAME_NOT_RUNTIME_OR_USER_APPROVAL_EVIDENCE`: wireframe는 구조·navigation·상태 설계의 `DOCUMENTED` evidence일 뿐이다. 실제 capture가 없으면 runtime 상태는 `NOT_RUN`으로 유지하고, capture가 있어도 user/device/UX/release approval을 대신하지 않는다. 구현 후에는 프로젝트의 `GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`와 runtime evidence owner를 통해 screen reference, actual consumer, capture를 별도로 readback한다.

### 1.2 Prospective Blueprint 사전 구현 승인 Gate

`BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE`

`BLUEPRINT_PASS_1_STRUCTURAL_DRAFT`

`STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT`

`BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`

`REQUIRED_IMAGE_AND_MATERIAL_PREPARATION`

`REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`

`BLUEPRINT_PASS_2_FINAL`

`VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT`

`ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`

`USER_FINAL_REVIEW_APPROVAL_REQUIRED`

`NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL`

이 profile을 선택한 이후 새 implementation package는 다음 lifecycle을 순서대로 통과해야 한다.

```text
PLAN
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

1. **PLAN** — Game Design Loop의 `FRAME → RESEARCH → DESIGN → SPECIFY`로 player promise, 현재 근거, 전체 system coverage, 다음 Slice의 규칙·flow·상태, 콘텐츠·UX, acceptance, non-goal과 미결정을 구현 전 명세한다.
2. **BLUEPRINT_PASS_1_STRUCTURAL_DRAFT** — 이미지 제작보다 먼저 같은 두 산출물의 working revision에 전체 Game Flow, system 관계, state/data 처리 흐름, Screen Inventory, 최소 대표 low-fidelity wireframe, entry/exit/cancel/re-entry, target viewport/input, player question, planned/actual consumer와 필요한 상태군을 기록한다. `STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT`: 이 1차 Blueprint는 별도 세 번째 파일·정본·보드가 아니라 최종 Blueprint로 승격될 동일 ID·동일 owner의 구조 초안이다.
3. **REQUIRED_IMAGE_AND_MATERIAL_PREPARATION** — 1차 Blueprint의 `BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`를 입력으로 기존 승인 image/build capture/reference/data/audio/material을 재사용하고, 현재 Slice의 P0/P1과 반복 일관성에 필요한 일부 P2 gap만 준비한다. `REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`: 모든 미래 화면·캐릭터·콘텐츠·장식 자산을 일괄 완성하지 않는다. 새 image deliverable은 `IMAGE_CONVERSATION_APPROVAL_GATE.md`와 `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`를 통과해야 하며 이 Gate 자체가 무제한 생성 authority가 아니다. `STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE`: Mermaid / Flow / table은 정확한 구조 정보를 위한 text-native artifact로 유지한다.
4. **VFX preparation boundary** — `VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT`로 VFX의 player-feedback 목적, trigger, 시작/peak/종료 timing, layer, 화면 점유, storyboard/frame intent, 필요한 texture/mask/sprite source, reduced-motion 동등 경로, 성능 budget과 fallback을 확정한다. `ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`: Particle, Shader, `AnimationPlayer`, Tween, Signal/event wiring, 빠른 입력·중단·재진입, 실제 성능 측정과 runtime tuning은 최종 승인 뒤 Godot 제품 구현이 소유한다.
5. **BLUEPRINT_REVIEW_PUBLICATION (`BLUEPRINT_PASS_2_FINAL`)** — 검수·재사용·candidate review 결과를 같은 ID와 두 산출물에 통합하고 Section 1.1의 layer를 합성한다. `CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH` pass 뒤 사용자가 검토할 PDF와 exact AI Markdown final revision을 발행한다.
6. **USER_FINAL_REVIEW_APPROVAL** — `USER_FINAL_APPROVAL_DECISION_ID`로 `DEC-` ID를 부여하고, AI Markdown의 Confirmed Decisions에 사용자가 검토한 artifact의 branch/SHA, scope, known risk·N/A·미결정을 기록한다. 프로젝트에 별도 repository Decision owner가 있으면 같은 ID로 동기화하되 세 번째 artifact를 만들지 않는다. `DRAFT | INTERNAL_REVIEW | GENERATED_IMAGE | AUTOMATED_TEST | ASSISTANT_INFERENCE`는 `USER_FINAL_REVIEW_APPROVAL`을 대체하지 않는다.
7. **IMPLEMENTATION_AUTHORIZED** — 위 `BLUEPRINT_PASS_2_FINAL` exact revision에 대한 명시적 사용자 최종 승인이 기록된 뒤에만 새 구현 실행·Codex implementation package를 시작한다. `TASK_BREAKDOWN_READY_IMPLEMENTATION_EXECUTION_BLOCKED`: 구현 task breakdown, dependency, acceptance 순서는 승인 전에 준비할 수 있지만 실행 상태는 승인 전까지 blocked다.

`PROSPECTIVE_ONLY_EXISTING_IMPLEMENTATION_EVIDENCE_PRESERVED`: 이 Gate는 앞으로 시작하는 구현에만 적용한다. 이미 merge된 code/data/scene/test와 기존 runtime·UX evidence의 역사적 상태를 무효화하거나 하향 재분류하지 않으며, 이 profile 채택을 이유로 mass backfill하지 않는다.

`PROSPECTIVE_ONLY_PREEXISTING_EXACT_USER_APPROVED_IMPLEMENTATION_AUTHORITY_PRESERVED`: Gate 채택 전에 package ID, exact scope와 artifact revision/branch/SHA에 연결된 명시적 사용자 구현 승인이 기록되어 있었다면 `PRE_ADOPTION_USER_APPROVED_BUT_IMPLEMENTATION_NOT_STARTED`여도 그 package의 authority는 유지한다. `EXACT_APPROVED_SCOPE_AND_REVISION_ONLY`: grandfathering은 승인 기록과 동일한 package·scope·revision의 실행만 허용한다. `SCOPE_EXPANSION | SUCCESSOR_PACKAGE | INFERRED_BLANKET_APPROVAL`에는 이 authority를 재사용할 수 없으며 새 범위는 Section 1.2 lifecycle과 별도 사용자 최종 승인을 거쳐야 한다.

## 2. 사용자용 상세 PDF 계약

`CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED`

사용자용 PDF는 홍보용 개요나 짧은 요약본이 아니다. 이 파일 하나만 읽어도 다음을 이해할 수 있는 시각 중심 통합 제작 기획서여야 한다.

### 2.1 프로젝트와 플레이어 경험

- 한 줄 소개, 장르, 플랫폼, 대상 플레이어, 현재 단계
- 플레이어 역할·판타지·핵심 약속
- 플레이어 감정, 선택, 고민, 보상, 기억, 첫인상
- 디자인 필러, 차별점, 판매 포인트, 범위 안/밖
- `FIRST_5_15_30`: 첫 5분·15분·30분 경험과 학습 순서
- Core Loop, Session Loop, Meta Loop, 실패·복구 Loop

### 2.2 핵심 시스템

각 핵심 시스템과 필요한 서브 시스템은 공통 ID로 식별하고 다음 5단 구조로 설명한다.

1. **왜 존재하는가**: 플레이어 가치, 목표 감정, 핵심 선택, 보상, 차별점
2. **어떻게 플레이하는가**: 진입·종료 조건, 입력, 규칙, 처리 순서, 성공·실패, 예외·복구
3. **어떤 콘텐츠가 필요한가**: 스테이지, 유닛, 적, 아이템, 능력, 사건, UI, 이미지, 애니메이션, VFX, SFX, 데이터
4. **어떻게 구현하는가**: Godot 씬, 노드, 스크립트 책임, 데이터 소유권, 상태 전이, 신호·이벤트, 입력, UI 연결, 저장·로드, 의존성, 성능 위험, 구현 순서
5. **어떻게 완료를 판정하는가**: Acceptance Criteria, 자동 테스트, 통합 테스트, runtime 검증, UX 검증, 남은 범위

### 2.3 핵심 콘텐츠

각 핵심 콘텐츠는 단순 목록이 아니라 다음을 포함한다.

- 콘텐츠 ID, 목적, 목표 경험, 등장·해금 조건
- 소비하는 시스템과 영향을 받는 시스템
- 규칙, 상태, 변주, 난이도, 보상, 실패·복구
- 요구 UI·runtime asset·animation·VFX·SFX·audio
- Godot scene/resource/data/script 구성과 재사용 구조
- 구현·튜닝·검증 순서 및 Acceptance Criteria

### 2.4 구현 설명의 최소 깊이

- 권장 scene tree와 각 노드 책임
- controller/model/view/resolver/persistence 책임 분리
- script 간 입력·출력과 공개 API
- Resource/JSON/Dictionary 등 실제 data owner와 field/type/default/range
- 상태 전이와 비정상·중복 입력 처리
- 신호의 emitter/receiver/payload/timing
- UI 기본·hover·pressed·disabled·locked·warning/error 상태
- 저장·로드 시 복원 범위와 migration 고려
- 플랫폼·해상도·입력·성능 제약
- 기존 module/asset/reference 재사용 여부
- 구현 순서와 각 단계의 확인 방법

### 2.5 필수 시각자료

프로젝트에 해당하는 범위에서 다음을 PDF 내부에 포함한다.

- 승인 대표 이미지 또는 실제 플레이 화면
- One-Page Project Vision
- Core/Session/Meta Loop
- 전체 Game Flow와 시스템 관계도
- 상태 전이도와 시스템 처리 순서도
- UX Screen Flow, 주요 화면 wireframe, 첫 10~30분 storyboard
- 진행·해금 구조, 자원 Source–Sink, 콘텐츠 관계도
- 세계·세력·인물 관계도
- Visual Bible과 asset family
- Runtime Asset/Audio Consumer 연결도
- 실제 구현 증거 화면 또는 실제 build capture

모든 도식·이미지에는 목적, 관련 ID, source, 승인 상태, consumer, 구현 상태, runtime 검증 상태를 표시한다. 정확한 구조를 전달하는 도식은 Section 7의 text-native 경계를 따른다.

## 3. AI용 상세 기획·구현 명세 계약

`AI_PRODUCTION_SPEC_MARKDOWN`은 사람이 읽는 PDF의 원문 복제본이 아니라 machine-searchable active specification이다. 최소 구조는 다음과 같다.

1. `CANON SNAPSHOT`
2. `SOURCE REGISTRY`
3. Current Project State
4. Confirmed Decisions
5. Design Pillars / Player Experience Contract
6. Core / Session / Meta Loop
7. `SYSTEM REGISTRY`
8. System Specifications
9. `CONTENT REGISTRY`
10. Content Specifications
11. UI/UX and Input Contract
12. Visual Asset Consumer Matrix
13. Audio Consumer Matrix
14. Technical Architecture
15. `DATA CONTRACTS`
16. `SCENE MAP`
17. `SCRIPT RESPONSIBILITY MAP`
18. `SIGNAL AND EVENT FLOW`
19. `STATE MACHINES`
20. `SAVE/LOAD CONTRACT`
21. `IMPLEMENTATION TRACEABILITY`
22. `TEST AND QA CONTRACT`
23. Vertical Slice Definition
24. Risks and Blockers
25. User Decision Required
26. `IMPLEMENTATION QUEUE`
27. Change Log

각 시스템·콘텐츠 명세는 ID, player contract, rules, entry/exit, states, transitions, data contract, scene/node/script owner, signals/events, UI/asset/audio consumers, save/load, dependencies, implementation order, Acceptance Criteria, automated/integration/runtime/UX verification, remaining work를 포함한다.

`RUNTIME_TRUTH_SEPARATE`: AI 명세는 기획·구현 계약의 active owner가 될 수 있지만 실제 `.gd`, `.tscn`, `.tres`, `.json`, import 설정, test, build, runtime evidence를 대체하지 않는다.

## 4. Notion 입력 전용 경계

`NOTION_INPUT_ONLY_NO_OUTPUT`

이 profile에서는:

- 기존 Notion에 repository로 이관되지 않은 **고유 미이관 자료**가 있는지 먼저 확인한다.
- 해당 자료가 있으면 기존 Notion을 입력 자료로만 fresh-read하고 Source Registry와 migration gap에 출처를 남긴다.
- master GDD를 위해 새 Notion page/database/view를 만들지 않는다.
- Notion은 신규 출력·갱신·동기화·readback 대상이 아니다.
- 기존 승인 정보와 시각자료를 이관한 뒤 원본 폐기 여부는 별도 migration 결정으로 다룬다.
- 사용자가 일반 프로젝트 운영에서 Notion 정본을 유지하라고 명시하면 기존 `DOMAIN_SPLIT_CANON`과 `NOTION_OPERATION_GATE`를 계속 적용한다.

## 5. 공통 ID·동일 시점 계약

`SHARED_ID_AND_SOURCE_SHA_REQUIRED`

PDF와 AI Markdown은 같은 항목에 같은 ID를 사용한다.

- 시스템: `SYS-`
- 콘텐츠: `CNT-`
- UI: `UI-`
- UX Flow: `UX-`
- 시각 에셋: `AST-`
- 오디오: `AUD-`
- 데이터 계약: `DAT-`
- QA: `QA-`
- 결정: `DEC-`

두 파일에는 동일한 source branch, 기준 commit SHA, 생성일을 기록한다. PDF 생성 직전 AI 명세와 실제 repository를 다시 읽어 ID·규칙·상태·SHA 불일치를 검사한다.

구현 현실 상태는 다음을 합치지 않는다.

```text
DOCUMENTED
→ CONFIRMED
→ IMPLEMENTED
→ AUTOMATED_TEST_PASS
→ RUNTIME_VERIFIED
→ UX_VERIFIED
→ RELEASE_READY
```

하위 evidence가 없으면 상위 상태를 주장하지 않는다.

## 6. 벤치마킹·현업 조사 계약

Master GDD를 새로 만들거나 대규모 갱신할 때는 현재 장르·플랫폼에 맞는 근거를 조사한다.

- 직접 경쟁작 5~8개
- 인접 장르 참고작 2~3개
- 핵심 시스템, UI/UX, 접근성, 시각 가독성, 사운드 피드백, 콘텐츠 생산, 실패 사례

결과는 `ADOPT / ADAPT / REJECT`로 판정하며 관찰, 적용 범위, 적용 금지점, 플레이어 영향, 구현·콘텐츠 비용, 위험, 검증 방법, 출처, 조사일을 남긴다. 레퍼런스 게임 이름만 적고 구현을 위임하지 않는다.

## 7. 이미지·시각자료 경계

`NO_AUTOMATIC_IMAGE_GENERATION`

`TEXT_NATIVE_EXACT_DIAGRAMS`

`CURRENT_IMAGE_CREATION_POLICY_REQUIRED`

`STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE`

- 기존 승인 이미지와 실제 build capture를 우선 사용한다.
- 승인 visual이 없으면 `현재 승인 Visual 없음`과 필요한 consumer·상태·규격을 기록한다.
- flow/state/sequence/system 관계/data처럼 의미가 정확해야 하는 문서 도식은 `Mermaid / Flow / table`의 text-native source로 작성하고 두 산출물 안에 렌더링한다.
- 새로운 concept/runtime/store image나 별도 image deliverable의 생성·편집은 별도의 사용자 명시적 요청 또는 현행 승인 작업 안에서 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 허용한 bounded candidate 경로를 따라야 한다. 무소비처·무검수 자동 생성을 하거나 이 profile의 세 번째 산출물로 추가하지 않는다.
- 이미지 존재를 runtime consumer 연결 또는 UX 검증 완료로 간주하지 않는다.

## 8. 생성·검증 순서

```text
latest completed Base fresh-read
→ project-adopted Base + project canon comparison
→ Base drift classification
→ base execution SHA selection and bounded pin
→ conflict/gap reconciliation
→ benchmark and field research
→ project-wide system coverage + next-Slice depth
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ required image/material/VFX-source preparation and candidate review
→ shared ID registry + AI production spec update
→ implementation/runtime traceability readback
→ BLUEPRINT_REVIEW_PUBLICATION (`BLUEPRINT_PASS_2_FINAL`)
→ same branch/SHA check
→ PDF render and page inspection
→ focused regression + repository checks
→ USER_FINAL_REVIEW_APPROVAL
→ implementation handoff boundary fresh-read
```

위 `BLUEPRINT_REVIEW_PUBLICATION`은 사용자의 최종 검토 입력인 2차 최종 Blueprint를 제공한다. 그 delivery, 내부 review, render inspection 또는 test 통과만으로 `IMPLEMENTATION_AUTHORIZED`가 되지 않으며 Section 1.2의 별도 `USER_FINAL_REVIEW_APPROVAL` decision이 필요하다.

PDF 검증에는 파일 열기, 페이지 수, 목차·페이지 번호, 한글 font, 표·도식 잘림, 이미지 해상도, caption, 내부 link, 빈 페이지, 기준 SHA, 실제 page render inspection을 포함한다.

## 9. 최종 제공 계약

`PDF_ONLY_USER_DOWNLOAD`

최종 사용자 응답에는 사용자용 상세 PDF 하나만 다운로드 링크로 제공한다.

`AI_SPEC_REPOSITORY_PATH_REPORT_ONLY`

AI 명세는 별도 다운로드 링크를 제공하지 않고 다음 정보만 보고한다.

- repository path
- branch
- commit SHA
- PR
- validation result

작업지시문 템플릿 자체를 사용자가 별도로 요청한 경우에는 그 템플릿 파일을 배포할 수 있다. 이것은 프로젝트 master GDD의 2개 결과물에 포함되지 않는 Base 운영 도구다.

## 10. 완료 조건

- 정확히 두 프로젝트 산출물만 생성됨
- `base_observed_head_sha`, `base_adopted_contract_sha`, `base_execution_sha`와 drift classification 누락 0
- 영구 stale pin 또는 bounded 작업 중 floating Base latest 사용 0
- 구현 인계·pre-merge·post-merge·closeout 경계 fresh-read 누락 0
- `PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH` 누락 0
- `BLUEPRINT_PASS_1_STRUCTURAL_DRAFT → REQUIRED_IMAGE_AND_MATERIAL_PREPARATION → BLUEPRINT_PASS_2_FINAL` 의미·순서 누락 0
- Blueprint 두 pass를 별도 세 번째 artifact·parallel canon으로 만든 사례 0
- 1차 Blueprint의 actual/planned consumer·state family·대표 wireframe 누락 0
- current Slice를 넘어 모든 미래 project asset을 일괄 제작한 사례 0
- VFX brief/source 준비와 Godot engine-native VFX 구현 경계 혼합 0
- exact final Blueprint revision에 대한 명시적 사용자 최종 승인 전 신규 구현 실행 0
- draft·내부 review·생성 이미지·자동 test·assistant inference를 최종 승인으로 대체한 사례 0
- 기존 구현·runtime evidence의 소급 무효화·하향 재분류 0
- 최신 정본 누락·미표시 충돌 0
- 핵심 시스템·핵심 콘텐츠 누락 0
- 시스템·콘텐츠별 Godot 구현 설명 누락 0
- 시스템↔콘텐츠↔UI↔asset/audio↔scene/script/data↔test 추적 누락 0
- PDF와 AI 문서 ID·source SHA 불일치 0
- 근거 없는 구현·runtime·UX·release 완료 주장 0
- 목적 없는 시각자료와 자동 이미지 생성 0
- Notion 신규 출력·동기화 0
- PDF 렌더 오류 0
- 검증 가능한 문서 생성 작업의 남은 작업 0

## 11. Blueprint 작업 현황 투영과 증분 수정 무손실 Gate

### 11.1 사람용 Blueprint 안의 작업 현황

`BLUEPRINT_GOAL_SYSTEM_CASE_PROGRESS_PROJECTION`

`PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION`

`NO_SEPARATE_PM_PDF_OR_HTML`

사람용 `HUMAN_MASTER_GDD_PDF`는 게임 Blueprint와 프로젝트 PM 현황을 한 파일에서 읽게 하되, 별도 PM PDF·HTML dashboard·세 번째 artifact 또는 병행 상태 정본을 만들지 않는다. 작업 현황은 프로젝트의 승인 Goal/Playable Slice, Active Context, `project_work_kanban`, AI production specification, 실제 implementation·test·runtime·UX·approval evidence에서 읽어 만든 read-only snapshot이다.

필수 View:

| View token | 필수 내용 |
|---|---|
| `PROJECT_GOAL_STATUS_SUMMARY` | 현재 프로젝트 목표와 Slice, 적용 목표 완료 수, 시스템·케이스 상태, 진행 중, 검증 대기, blocker, 사용자 결정, 다음 안전 작업 |
| `GOAL_LEVEL_CHECKLIST` | 목표 ID, player value, Acceptance Criteria, 관련 system/work item, 상태와 evidence, blocker, 다음 행동 |
| `SYSTEM_LEVEL_CHECKLIST` | 시스템 ID, 목적·player value, 입력·출력·owner·actual consumer·dependency, 기획·데이터·자산·구현·검증 체크리스트 |
| `CASE_LEVEL_STATUS_MATRIX` | 정상·경계·실패·충돌·중단·복구·저장·UI·접근성·성능 중 실제 위험과 consumer에 필요한 case의 상태 |
| `BLOCKERS_DECISIONS_AND_NEXT_SAFE_ACTION` | 해결되지 않은 blocker, 사용자 결정 packet, resume condition, 현재 작업과 다음 단일 안전 작업 |

`PASS_ONLY_COUNTS_COMPLETE`: 적용 대상의 완료 수에는 해당 Acceptance와 요구 evidence가 실제 `PASS` 또는 work item `DONE`인 항목만 포함한다. `NOT_APPLICABLE`은 이유와 함께 분모에서 제외한다. 다음 차원은 하나의 초록색 완료나 평균 퍼센트로 합치지 않는다.

```text
DOCUMENTED
IMPLEMENTED
AUTOMATED_TEST_PASS
RUNTIME_VERIFIED
UX_VERIFIED
USER_APPROVED
```

PDF에는 `work_status_snapshot_at`과 source branch/SHA를 기록한다. PDF 안의 체크 상태를 수동 변경해 정본 상태를 바꾸지 않고, 차이가 발견되면 repository owner·receipt·evidence를 먼저 교정한 뒤 PDF를 다시 발행한다.

### 11.2 기존 Blueprint를 predecessor로 사용하는 증분 수정

`EXISTING_BLUEPRINT_INCREMENTAL_REVISION_REQUIRED`

`NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS`

`PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY`

유효한 기존 Blueprint가 있으면 새 Blueprint를 빈 문서에서 재작성하지 않는다. latest valid `HUMAN_MASTER_GDD_PDF`, 그 PDF를 만든 source commit과 source document, `AI_PRODUCTION_SPEC_MARKDOWN`, 승인 Decision, 실제 repository owner를 predecessor set으로 고정한 뒤 현재 변경 범위만 증분 수정한다.

작업 시작 전에 최소 다음을 inventory한다.

- predecessor Blueprint ref, source branch/SHA, 생성일, approval/evidence ceiling
- project/goal/system/content/UI/UX/asset/audio/data/QA/decision ID
- 목차와 section anchors, flow/system/content card와 cross-reference
- 확정 규칙·수치·예외·용어와 미해결 결정
- text-native diagram source, 승인 이미지·caption·provenance·actual consumer
- 구현 owner, code/data/scene/resource path, test/runtime/UX evidence
- 현재 blocker, next action, N/A 이유와 known risk

`STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION`: successor는 touched scope 밖의 유효 ID·설명·규칙·section·도식·승인 시각자료·consumer·evidence를 기본 carry-forward한다. 레이아웃 개선이나 요약을 이유로 의미 있는 내용을 삭제하지 않는다. ID를 rename·split·merge할 때는 predecessor ID와 successor ID의 mapping을 남긴다.

### 11.3 semantic delta와 손실 비교

`SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED`

`UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN`

successor 발행 전 predecessor inventory와 successor inventory를 비교하고 다음을 기록한다.

```yaml
predecessor_blueprint_ref:
predecessor_source_commit:
revision_mode: INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS
predecessor_inventory:
successor_inventory:
semantic_delta_summary:
removal_or_downgrade_justifications:
work_status_snapshot_at:
```

- 새 항목: 추가 이유, owner, ID, source와 consumer.
- 변경 항목: 이전 값, 새 값, 변경 근거, 영향받는 system/case/evidence.
- 삭제·대체 항목: 삭제 사유, supersession/replacement ID, consumer·migration·rollback 영향.
- 상태 하향 항목: 반증 또는 stale evidence, 영향 범위, 재검증 계획.
- 그대로 유지한 항목: `CARRIED_FORWARD_UNCHANGED`로 요약할 수 있으나 source locator를 보존한다.

근거 없는 누락, 설명 없는 상태 하향, 승인된 이미지·도식·규칙·evidence의 유실은 편집으로 인정하지 않는다.

`BLUEPRINT_LOSS_REGRESSION_GATE`: 다음을 successor 발행 전 검사한다.

1. predecessor stable ID가 successor에 존재하거나 explicit mapping·removal justification이 있다.
2. 이전 section·card·diagram·asset·consumer·evidence가 유지되거나 exact replacement가 있다.
3. 목표→시스템→케이스→work item→evidence traceability가 끊기지 않았다.
4. PDF와 AI Markdown의 source SHA·ID·semantic delta가 일치한다.
5. 기존 구현·runtime·UX·user approval 상태를 새 policy 채택만으로 하향하지 않았다.
6. page render와 text extraction 비교에서 잘림·누락·빈 페이지·깨진 glyph가 없다.

Gate 실패 시 기존 predecessor를 보존하고 successor를 최종본으로 승격하지 않는다.

### 11.4 predecessor를 읽지 못하는 경우와 최초 생성

`PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED`

기존 Blueprint 존재가 확인됐지만 파일·source revision·embedded visual·AI spec을 신뢰성 있게 읽을 수 없으면 memory·과거 채팅·추정으로 대체 재작성하지 않는다. 읽지 못한 locator, 영향받는 ID/section, 복구 경로를 기록하고 `BLOCKED_UNVERIFIED`로 둔다. 접근 가능한 repository owner와 predecessor 일부만으로 안전하게 수정할 수 있으면 touched scope를 명시적으로 제한한다.

정말 유효한 predecessor가 없는 최초 Blueprint만 `INITIAL_CREATION_NO_VALID_PREDECESSOR`로 생성할 수 있다. 이 판정에는 기존 PDF·repository design docs·Library/legacy migration source 검색 결과를 남기며, 최초 생성 뒤부터는 같은 두 artifact와 stable ID를 predecessor로 사용한다.

이 Gate는 `EXACTLY_TWO_DELIVERABLES`, `NO_SEPARATE_BLUEPRINT_ARTIFACT`, `NO_MASS_BLUEPRINT_BACKFILL`, `RUNTIME_TRUTH_SEPARATE`, 이미지 승인·consumer 경계를 변경하지 않는다.


<!-- FEDERATED_DUAL_CANON_PUBLICATION_CONTRACT -->

## 12. GitHub·승인 PDF 연합 정본 Gate

```text
FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER
REPOSITORY_EXECUTION_DATA_CANON
APPROVED_HUMAN_BLUEPRINT_PDF_CANON
ONE_EDITABLE_OWNER_PER_ATOMIC_FACT
```

`HUMAN_MASTER_GDD_PDF`는 생성만으로 정본이 되지 않는다. `CANDIDATE_PDF_NOT_CANON`이며 다음을 모두 만족한 version만 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`으로 승격한다.

```yaml
source_commit:
pdf_sha256:
approval_ref:
approved_at:
canonical_status: CANON_ALIGNED
supersedes_pdf_ref:
pdf_canon_manifest_ref:
included_scope:
implementation_evidence_ceiling:
```

승격 token은 `USER_APPROVED_AND_MANIFEST_REGISTERED`다. 승인본은 `APPROVED_PDF_IMMUTABLE_NEW_VERSION_REQUIRED`; 수정은 새 version·hash를 만들고 `NEW_VERSION_NEW_HASH_KEEP_HISTORY`로 predecessor를 보존한다.

### 12.1 단일 편집 owner

- repository owner: 코드·데이터·ID·규칙·수치·상태·Decision source·작업현황·실제 implementation/test/runtime evidence.
- 승인 PDF: 사용자가 승인한 읽기 구조, 프로젝트/플레이어 경험 지도, Flow·화면·정보 hierarchy, 시스템 카드 시각 표현, milestone 범위와 사람용 검수 baseline.
- `PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION`.
- `PDF_ANNOTATION_IS_CHANGE_REQUEST_NOT_CANON_MUTATION`.
- `PROJECT_WORK_KANBAN_IS_PROGRESS_SOURCE`.
- `PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION`.
- `NO_PARALLEL_BLUEPRINT_STATUS_CANON`.

### 12.2 충돌 처리

- repository 구조화 값과 PDF 표시값이 다르면 repository 값을 유지하고 PDF를 `REPOSITORY_ADVANCED_PDF_REVIEW_REQUIRED`로 내려 새 candidate를 만든다.
- 승인 PDF의 material visual flow/hierarchy와 구현이 다르면 구현을 교정하거나 새 candidate delta를 사용자에게 보여 다시 승인한다.
- 반영되지 않은 PDF feedback은 `PDF_FEEDBACK_PENDING_REPOSITORY_REFLECTION`이다.
- 해결되지 않은 동시 차이는 `CANON_CONFLICT`.
- `CANON_CONFLICT_BLOCKS_COMPLETION_AND_RELEASE`.

predecessor inventory, stable-ID carry-forward, semantic delta와 `BLUEPRINT_LOSS_REGRESSION_GATE`는 새 candidate를 승인 정본으로 승격하기 전 필수다. 기존 승인 PDF는 successor가 `USER_APPROVED_AND_MANIFEST_REGISTERED`가 되기 전까지 사람용 검수 baseline으로 유지한다.
