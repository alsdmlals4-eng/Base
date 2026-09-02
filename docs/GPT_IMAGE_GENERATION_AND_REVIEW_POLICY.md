# GPT 이미지 생성·검수 정책

```yaml
status: CURRENT_ACTIVE
workspace: REPOSITORY_FIRST
updated_at: 2026-09-02
```

이 문서는 Base를 적용한 프로젝트의 이미지·목업·UI 시각화 생성, 검수, 사용자 확정, repository 자산 승격, 실제 구현과 runtime evidence 경계를 정의한다.

현재 작업면:

```text
REPOSITORY_HUMAN_FACING_CANON
→ GDD / Flow / Storyboard / Visual direction / 사람이 읽는 승인 상태

REPOSITORY_STRUCTURED_CANON
→ Markdown / JSON / game data / ASSET_MANIFEST / Scene / Resource / Test

REPOSITORY_RUNTIME_TRUTH
→ 실제 적용 / build / runtime / device evidence

legacy Notion / Google Sheets
→ 실제 migration scope에서만 discovery input
→ 신규 이미지 승인·저장·동기화·완료의 기본 작업면이 아님
```

프로젝트 최신 사용자 지시, 프로젝트 `AGENTS.md`, 승인 Decision, 실제 구현이 이 정책보다 우선한다. 생성 결과는 사용자 확정 전까지 정본·최종 자산·구현 완료 증거가 아니다.

## 0. Visual Asset Coverage Preflight

프로젝트 전체, 화면군, 캐릭터군, 적군, UI군, 아이템군, 환경군, 마케팅 asset set처럼 한 장보다 넓은 범위를 다룰 때는 먼저 subordinate `docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`로 실제 화면과 소비처를 열거하고, 그 다음 canonical `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`로 누락을 교차 검사한다.

```text
current project canon / stage / actual or planned consumer
→ SCREEN_SURFACE_INVENTORY_FIRST
→ PRODUCTION_INFORMATION 여부
→ existing approved asset / implementation / reuse 조회
→ coverage_status + STATE_FAMILY_COMPLETENESS
→ 필요한 gap만 Visual Requirement Gate로 전달
```

- `COVERAGE_CHECK_ONLY`, `NOT_A_SECOND_ASSET_CANON`.
- `GAP_BLOCKING`은 현재 player-facing flow나 제출 요구를 실제로 막을 때만 사용한다.
- `STATE_FAMILY_COMPLETENESS`는 대표 한 장이 아니라 실제 소비처가 요구하는 기본·hover·pressed·disabled·selected·warning·피격·사망 등 상태군을 확인한다.
- `PLATFORM_SPEC_RECHECK_REQUIRED`: store capsule, screenshot, app icon 등은 release 시점의 최신 공식 규격을 다시 확인한다.
- `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`: coverage gap 자체는 무제한 batch나 의미 없는 variant 생성 권한이 아니다. 다만 아래 Gate가 필요성과 일관성을 확정하면 사용자 사전 lock 없이 **bounded candidate**를 생성할 수 있다.

### 0A. Information Artifact / Actual Consumer Gate

```text
PRODUCTION_INFORMATION
INFORMATION_ARTIFACT_NOT_IMAGE_ASSET
TEXT_TABLE_FLOW_DB_FIRST
ACTUAL_CONSUMER_REQUIRED
CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
```

`PRODUCTION_INFORMATION`에는 시스템 설명, 세계관, 캐릭터·세력 관계, 관계도, 제작 체크리스트, 밸런스·경제 구조, Flow, 상태 전이, 구현 계약이 포함된다.

- 시스템 설명, 세계관, 관계도, 제작 체크리스트가 필요하다는 이유만으로 장식용 설명 이미지 시트를 만들지 않는다.
- 제작자·AI가 정보를 이해하는 목적이면 Markdown, 표, JSON, Mermaid, Flow 같은 editable·searchable 형식을 우선한다.
- 이미지 자체가 필요하면 실제 게임·제품 또는 승인된 Blueprint planned surface의 소비처를 확인한다.

`ACTUAL_CONSUMER_REQUIRED` 기록:

```yaml
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
consumer_surface:
primary_use:
target_path_or_owner:
validation:
```

유효 소비처:

- `GAME_RUNTIME`: gameplay scene, character sprite, environment, HUD, VFX, item icon.
- `PLANNED_GAME_SURFACE`: 구현 예정인 구체적 screen/scene/asset slot 또는 Blueprint 핵심 화면.
- `PLAYER_FACING_EXPLANATORY`: 튜토리얼, 도감, 인게임 도움말, 관계 UI.
- `PRODUCT_DISTRIBUTION`: store capsule, key art, app icon, trailer thumbnail, press kit.

`DOCUMENTATION_DECORATION`, `AI_EXPLANATION_ONLY`, `CHECKLIST_DECORATION`, `UNNAMED_FUTURE_USE`만 존재하면 `DO_NOT_GENERATE`다. 필요한 정보는 `TEXT_TABLE_FLOW_DB_FIRST`로 계속 만든다.

### 0B. Local candidate vault와 명시적 승격

로컬 GPT/Work가 생성하거나 수집한 candidate의 비정본 보관·동기화·승격은 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`가 소유한다.

```text
.asset-vault/library/
→ assets/_vault_local/
→ REVIEWED / USER LOCK
→ explicit promote
→ project-owned tracked asset path
→ ASSET_MANIFEST / provenance / SHA-256
→ implementation / runtime evidence
```

- `.asset-vault/library/`와 `assets/_vault_local/`은 candidate workspace이며 프로젝트 정본이나 Codex durable input이 아니다.
- 사용자 lock 뒤에도 자동 승격하지 않는다. `promote`와 repository tracked destination readback을 명시적으로 수행해야 한다.
- vault sync·preview·파일 존재는 `PROJECT_ASSET_APPROVED`, `CANON_REGISTERED`, `IMPLEMENTED`, `RUNTIME_VERIFIED`를 증명하지 않는다.
- 프로젝트가 local vault를 채택하지 않았거나 현재 local filesystem을 읽을 수 없으면 `VAULT_LOCAL_STATE_UNVERIFIED`로 남기고 존재를 추정하지 않는다.

## 1. Visual Requirement Gate

프로젝트용 이미지·목업을 만들기 전에 `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`를 적용한다.

```text
need / Delete Test
→ existing approved asset and reference reuse
→ actual or planned consumer
→ role / priority / state family / format
→ REUSE | ADAPT | SOURCE | GENERATE_EXPLORATION | CREATE_CUSTOM | DEFER | CUT
```

- 가능한 한 `requirement_id`를 사용한다.
- `GENERATE_EXPLORATION` 또는 `CREATE_CUSTOM`일 때만 새 candidate 생성을 연다.
- `REUSE_SYSTEM`, `REUSE_PROJECT`, `ADAPT_EXISTING`, `SOURCE_EXISTING`을 불필요한 새 생성으로 바꾸지 않는다.
- 프로젝트 전체 범위를 검토해도 현재 목표에 필요 없는 자산을 자동 추가하지 않는다.
- 실제 이미지 제작은 host 이미지 생성·편집 모델로만 한다. SVG, vector path, HTML/CSS/Canvas, Python drawing, Godot primitive를 이미지 모델 대용으로 사용하지 않는다.

## 2. Image Conversation Approval Gate

실제 생성 시점과 사용자 확정은 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`가 소유한다.

현재 기본 계약:

```text
NEED_DRIVEN_GENERATE_THEN_LOCK
PROJECT_CANON_AND_EXISTING_VISUAL_READBACK_REQUIRED
CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION
USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION
NO_AUTOMATIC_IMAGE_CHAIN
```

### 2.1 사용자가 현재 생성·편집을 명시한 경우

```text
current request
→ exact project / consumer / current canon resolve
→ existing approved visual and source readback
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md
→ bounded candidate generation
→ QA
→ 사용자 LOCK / REVISE / REJECT / REFERENCE_ONLY
```

현재 명시 요청은 별도 장문 승인문을 다시 요구하지 않는다.

### 2.2 검토 중 AI가 필요성을 확인한 경우

사용자가 이미 프로젝트 작업을 승인했고, 아래 조건이 모두 충족되면 routine 사전 승인 없이 후보를 먼저 제작할 수 있다.

- actual consumer 또는 승인된 Blueprint planned surface가 구체적이다.
- 프로젝트 최신 내용·기존 시안·승인 Visual을 실제로 읽었다.
- 역할, 상태, 규격, 보호 요소와 금지 drift가 명확하다.
- 현재 이미지 모델을 사용할 수 있다.
- 후보 생성이 핵심 Art Direction을 임의 확정하거나 새 제품 범위를 만들지 않는다.

```text
VISUAL_NEED_CONFIRMED_DURING_APPROVED_WORK
→ PROJECT_REVIEW_COMPLETE
→ actual/planned consumer + consistency constraints
→ bounded text brief recorded internally or in repository owner
→ GENERATE_EXACTLY_ONE candidate
→ STOP_REQUIRED_AFTER_GENERATION
→ 사용자 결과 검토와 final decision
```

조건이 부족하면 생성하지 않고 `MISSING_CANON`, `MISSING_CONSUMER`, `VISUAL_DIRECTION_CONFLICT`, `BLOCKED_IMAGE_MODEL_UNAVAILABLE` 중 정확한 상태로 둔다.

### 2.3 bounded generation

기본 단위는 candidate deliverable 1건이다. 다만 하나의 실제 consumer가 여러 상태 파일을 동시에 요구하고 개별 생성으로는 검증할 수 없는 경우 `BOUNDED_STATE_FAMILY_ALLOWED_WHEN_CONSUMER_REQUIRES`를 적용할 수 있다.

`NO_AUTOMATIC_IMAGE_CHAIN`은 다음을 금지한다.

- 필요성이 확인되지 않은 다음 캐릭터·포즈·화면·variant 자동 확장
- 생성 성공을 근거로 production batch 전체를 자동 승인
- 사용자가 검토하기 전에 candidate를 정본 또는 runtime에 승격

## 3. 프로젝트 Visual continuity

```text
latest user decision
→ exact project relation
→ current project canon / Decision
→ existing approved image / visual anchor / prior draft
→ relevant Screen / Flow / System / actual implementation
→ Keep / Avoid / Do Not Drift
→ candidate generation
```

- 다른 프로젝트 이미지를 편의상 가져와 정체성을 추정하지 않는다.
- 기존 승인 anchor가 있으면 실제 preview/source readback 뒤 재사용한다.
- anchor가 없고 선택이 필요한 경우 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`의 concept comparison deliverable을 사용한다.
- identity-preserving 편집에서는 얼굴 구조, 헤어, 의상, 장비, 팔레트, 실루엣, 카메라, 광원, UI family 등 요청하지 않은 속성을 보호한다.

## 4. 상태와 증거

```text
NEEDED
→ BRIEF_READY
→ GENERATED_CANDIDATE
→ REVIEWED
→ USER_APPROVED
→ CANON_REGISTERED
→ IMPLEMENTED
→ RUNTIME_VERIFIED
```

다음은 서로 같지 않다.

```text
GENERATED_CANDIDATE
!= USER_APPROVED
!= PROJECT_ASSET_APPROVED
!= CANON_REGISTERED
!= IMPLEMENTED
!= RUNTIME_VERIFIED
```

호환 machine marker:

```text
GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED
```

- `GENERATED_EXPLORATION`: 방향·구성 검토 후보.
- `REVISION_REQUIRED`: 결함이나 drift 수정 필요.
- `PROJECT_ASSET_APPROVED`: 사용자가 해당 결과를 제품 자산 방향으로 lock.
- `CANON_REGISTERED`: repository path, provenance, SHA-256, consumer, state family, rights 상태를 기록.
- `APPLIED_AND_RUNTIME_VERIFIED`: 실제 소비처에 연결하고 실행 evidence로 확인.

정적 mockup, 채팅 preview, PDF 삽입, 자동 테스트 PASS를 runtime proof로 확대하지 않는다.

## 5. Blueprint와 구현 경계

`BLUEPRINT_PASS_1_STRUCTURAL_DRAFT`

`BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`

`REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`

`BLUEPRINT_PASS_2_FINAL`

`VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT`

`ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`

Blueprint 검수에 필요한 이미지·시각자료 candidate는 1차 구조 Blueprint 뒤, 2차 최종 Blueprint 승인 전에 만들 수 있다.

```text
PLAN
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

- `BLUEPRINT_PASS_1_STRUCTURAL_DRAFT`는 같은 두 산출물의 working revision에서 Flow, Screen Inventory, 대표 wireframe, entry/exit/cancel/re-entry, target viewport/input, state family, actual/planned consumer를 먼저 고정한다. `BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`가 없는 자산 후보를 이미지 제작 목록으로 만들지 않는다.
- `REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`: 1차 Blueprint가 현재 Slice의 P0/P1 및 필요한 일부 P2로 식별한 image/UI/animation/audio/VFX-source material만 재사용·준비한다. 미래 전체 프로젝트 자산이나 P3 장식을 일괄 생성하지 않는다.
- `VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT`: 이미지·시각 작업은 VFX 목적, trigger, timing, layer, storyboard, texture/mask/sprite source, reduced-motion 동등 경로, 성능 budget과 fallback을 준비할 수 있다.
- `ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`: Particle, Shader, `AnimationPlayer`, Tween, Signal/event wiring, 중단·재진입, 실제 성능 측정과 runtime tuning은 최종 Blueprint 사용자 승인 뒤 Godot 제품 구현에서 수행한다.
- `BLUEPRINT_REVIEW_PUBLICATION`은 image/material candidate review를 통합하는 `BLUEPRINT_PASS_2_FINAL`이다. 1차와 2차는 별도 추가 artifact가 아니라 기존 PDF+AI Markdown의 revision이다.

`NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK`은 이미지 candidate 준비 권한이다. 신규 구현 package의 제품 구현은 여전히 Blueprint 최종 승인 전 시작하지 않는다.

과거 문서의 `NO_AUTOMATIC_IMAGE_GENERATION`은 현재 정책에서 **무제한·무소비처·무검수 자동 생성 금지**로만 해석한다. 이미지 필요성·consumer·일관성이 확인된 bounded candidate 선제작을 막는 근거로 사용하지 않는다.

## 6. Reference·권리·독립 제작

외부 reference 기반 작업은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`를 적용한다.

필수 기록:

```yaml
reference_brief:
transferable_principles:
forbidden_expression:
independent_creation_method:
reference_similarity_status:
rights_and_distribution_status:
```

trade dress, 로고, 캐릭터 고유 실루엣, exact UI, 워터마크, 저작권 표현을 표면 복사하지 않는다. 독립 제작·권리·출처가 확인되지 않으면 `RELEASE_BLOCKED_UNVERIFIED`다.

## 7. 사용자 결과 검토

후보를 제시할 때 최소 다음을 함께 보고한다.

```yaml
requirement_id:
consumer:
purpose:
continuity_sources:
protected_elements:
candidate_status: GENERATED_CANDIDATE
qa_findings:
recommended_decision: LOCK | REVISE | REJECT | REFERENCE_ONLY
promotion_not_yet_done:
```

사용자 `LOCK` 뒤에만 final direction 또는 제품 자산 승격을 진행한다. 수정 요청은 같은 bounded deliverable의 correction으로 처리하고, 범위 밖 독립 이미지는 별도 need/consumer 판정을 거친다.

## 8. Host precedence와 legacy marker

`HOST_PLATFORM_PRECEDENCE`: 상위 system/developer/host 도구 정책이 이미지 호출 시점·도구·응답 형식을 더 엄격하게 제한하면 상위 정책을 따른다. 정적 문서만으로 host runtime enforcement를 주장하지 않는다.

아래 문자열은 과거 test·문서 탐색 호환을 위해 남기는 **비활성 legacy marker**이며 현재 Gate가 아니다.

```text
LEGACY_SUPERSEDED_ONLY:
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
```

현재 동작은 `NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK`과 `GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION`이 소유한다.
