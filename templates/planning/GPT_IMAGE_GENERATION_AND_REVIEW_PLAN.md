# GPT Image Generation and Review Plan

## 1. Context

```yaml
project:
project_key:
project_relation:
project_stage:
approval_bundle:
coverage_item_id:
coverage_status: NOT_REVIEWED | NOT_APPLICABLE | COVERED_EXISTING | REQUIREMENT_LINKED | GAP_BLOCKING | GAP_NONBLOCKING | DEFERRED_BY_DECISION
state_family_status: NOT_REVIEWED | COMPLETE | PARTIAL | NOT_APPLICABLE
platform_spec_status: NOT_APPLICABLE | CURRENT_OFFICIAL_VERIFIED | RECHECK_REQUIRED | BLOCKED_UNVERIFIED
requirement_id:
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
consumer_surface:
primary_use:
consumer_validation:
information_artifact_route: NOT_APPLICABLE | TEXT | TABLE | NOTION_DB | MERMAID | FLOW | JSON | OTHER_STRUCTURED
image_phase: PLANNING_VISUALIZATION | INTERMEDIATE_VISUAL_CHECKPOINT | FINAL_VISUAL_CANDIDATE
related_decisions: []
canonical_sources: []
player_experience:
target_screen_or_use:
screen_id:
flow_id:
platform_resolution_camera:
existing_approved_assets: []
approved_visual_reference_ids: []
visual_map_status: CURRENT | UPDATE_REQUIRED | NOT_APPLICABLE | UNVERIFIED
interpretation_record_id:
interpretation_status: CONFIRMED | DISCOVERED_IDEA | AI_ASSUMPTION | MIXED | UNVERIFIED
readback_status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
runtime_compare_required: YES | NO
runtime_capture_path:
drift_status: NOT_RUN | MATCHED | INTENDED_DIFFERENCE | IMPLEMENTATION_GAP | PLANNING_CHANGE_REQUIRED | AI_MOCKUP_ERROR | VISUAL_CANONICAL_CONFLICT | BLOCKED_UNVERIFIED
asset_vault_status: ENABLED | NOT_CONFIGURED | VAULT_LOCAL_STATE_UNVERIFIED
vault_source_key:
workspace_path:
promotion_target:
promoted_path:
primary_use_status: NOT_RUN | IN_REVIEW | ACCEPTED | REVISION_REQUIRED
harvest_status: NOT_REVIEWED | NO_REUSE_VALUE | CANDIDATES_FOUND | STRUCTURED | SECOND_USE_VALIDATED
reuse_classification: UNASSESSED | REUSE_AS_IS | VARIANT_SEED | STRUCTURE_PATTERN | STYLE_DNA | REBUILD_FOR_REUSE | ONE_OFF_KEEP | REJECT_REUSE
decomposition_method: NONE | SOURCE_LAYER | MASK_CUTOUT | MANUAL_OR_SEMANTIC_REBUILD | DERIVED_GENERATIVE_RECOVERY
asset_vault_harvest_record_id:
second_use_validation: NOT_RUN | PASS | FAIL | NOT_APPLICABLE
reference_similarity_status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

`PROJECT_RELATION_REQUIRED`: 프로젝트용 계획에는 정확한 `project_relation`이 있어야 한다. 다른 프로젝트의 approved reference, asset, screen, benchmark를 project-local canon처럼 복사하지 않는다.

`coverage_item_id / coverage_status / state_family_status`는 `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`의 누락 탐지 결과를 연결한다. 이 값들은 `requirement_id`, Asset status, Manifest, runtime evidence를 대체하지 않는다. `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`를 적용해 `GAP_BLOCKING / GAP_NONBLOCKING` 자체를 이미지 생성 승인으로 해석하지 않는다.

`PRODUCTION_INFORMATION / INFORMATION_ARTIFACT_NOT_IMAGE_ASSET / TEXT_TABLE_FLOW_DB_FIRST`: 시스템 설명, 세계관, 관계도, 제작 체크리스트 등 제작자·AI가 알아야 할 기본 정보는 필요하면 해당 문서·표·DB·Mermaid·Flow owner에 생성·갱신한다. 이 계획의 Image backlog에 넣기 위해 설명용 이미지를 만들지 않는다. 비이미지 route를 확인한 경우 `information_artifact_route`에 기록하고 image row를 만들지 않는다.

`ACTUAL_CONSUMER_REQUIRED`: Image backlog에 들어가는 모든 project image는 `consumer_kind / consumer_surface / primary_use / consumer_validation`이 있어야 한다. 유효 값은 실제 runtime, 구체적인 planned game surface, `PLAYER_FACING_EXPLANATORY`, 실제 store/marketing distribution surface다. `DOCUMENTATION_DECORATION / AI_EXPLANATION_ONLY / CHECKLIST_DECORATION / UNNAMED_FUTURE_USE`만 있으면 `DO_NOT_GENERATE`이며 backlog에 넣지 않는다.

`approved_visual_reference_ids`가 있으면 `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`에서 `Keep / Avoid / Do Not Drift`를 작업 계약에 반영한다. 현재 승인 기준을 읽을 수 없으면 `BLOCKED_UNVERIFIED`; 승인 기준 자체가 부족하면 `MISSING_CANON`; 최신 Decision과 충돌하면 `VISUAL_CANONICAL_CONFLICT`다.

보존소가 `ENABLED`이면 `GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE`는 기본적으로 local-only 후보로 유지한다. `PROJECT_ASSET_APPROVED` 뒤에만 `promotion_target`을 확정하고 `promote`하여 `promoted_path`를 만든다.

`primary_use_status`는 이미지가 원래 actual consumer에서 목적을 달성했는지 기록한다. `harvest_status`와 `reuse_classification`은 그 뒤 재사용 가치를 별도 판정한다. `asset_vault_harvest_record_id`는 local-only Harvest metadata를 연결할 뿐 제품 자산 승인이나 tracked promotion을 뜻하지 않는다.

## 2. Image backlog

`ACTUAL_CONSUMER_REQUIRED`를 통과한 결과만 이 표에 넣는다.

| Image ID | Project | Consumer Kind | Consumer Surface | Screen/Flow ID | Record Type | Primary Use | 관련 canon | 핵심 전달 | 비율·해상도 | 유지 요소 | 변경 축 | Approved Reference | 해석 상태 | Runtime 비교 | Reference | vault_source_key | promotion_target | promoted_path | 우선순위 | 구현 난이도 | 재사용성 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- Project relation이 불명확한 row는 project canon으로 promotion하지 않는다.
- `Consumer Kind`: `GAME_RUNTIME / PLANNED_GAME_SURFACE / PLAYER_FACING_EXPLANATORY / PRODUCT_DISTRIBUTION`만 사용한다.
- `Record Type`: `ASSET / COMPONENT / SCREEN / REFERENCE / BENCHMARK` 중 해당 type. `REFERENCE / BENCHMARK`는 생성 제품 자산이 아니며 actual consumer 없이 production image로 승격하지 않는다.
- 우선순위: `S / A / B`.
- 상태: `PLANNED / GENERATED_EXPLORATION / IN_REVIEW / REVISION_REQUIRED / REJECTED / APPROVED_CANDIDATE / PROJECT_ASSET_APPROVED / APPLIED_AND_RUNTIME_VERIFIED`.
- Approved Reference는 실제 current Project에서 확인한 `APPROVED_VISUAL_REFERENCE` ID만 기록한다.
- `vault_source_key`는 local candidate를 가리키며 repository runtime canon이 아니다.
- `promoted_path`는 `PROJECT_ASSET_APPROVED` 후 tracked asset이 실제 생성된 경우에만 채운다.

### 2.1 Production-information route-out

다음 정보가 필요하면 Image backlog가 아니라 해당 project documentation/structured owner를 갱신한다.

| Information | Preferred editable form | Destination owner | Status / Readback |
|---|---|---|---|
| 시스템 설명·상태 전이 | text / table / Mermaid / Flow | System/GDD/Notion owner | |
| 세계관·세력 | text / DB / table | World/Notion owner | |
| 캐릭터·세력 관계/관계도 | relation DB / table / Mermaid | Character/Relation owner | |
| 제작 체크리스트 | Markdown checklist / DB | Project/Base process owner | |
| 밸런스·경제 | table / JSON / chart when useful | Balance/data owner | |

이 표는 별도 정본이 아니라 route 확인 예시다. 실제 정보는 해당 owner에 기록한다.

## 2A. Visual asset coverage

이 표는 `COVERAGE_CHECK_ONLY`이며 실제 Asset/Manifest/Notion/runtime 원장이 아니다.

| Coverage Item | Category | Surface/Flow | Stage | Applicable | Coverage Status | State Family | State Family Status | Requirement / Existing Asset | Consumer Kind | Consumer | Validation | Gap Action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

`Coverage Status`:

- `NOT_REVIEWED`: 아직 검사하지 않음.
- `NOT_APPLICABLE`: current project/stage/consumer에 불필요하며 이유를 기록함.
- `COVERED_EXISTING`: 기존 승인 asset/system/implementation으로 충족.
- `REQUIREMENT_LINKED`: 필요한 항목이 `requirement_id`에 연결됨.
- `GAP_BLOCKING`: 현재 목표 player-facing flow, accessibility 또는 platform submission을 실제로 막는 누락.
- `GAP_NONBLOCKING`: 필요한 누락이지만 current target 완료를 막지 않음.
- `DEFERRED_BY_DECISION`: 명시적 Decision으로 현재 단계에서 보류.

`GAP_BLOCKING`이 남아 있으면 해당 target을 visual-ready/final로 주장하지 않는다. 그러나 gap 발견만으로 이미지를 생성하거나 batch를 확대하지 않는다. `NOT_APPLICABLE`은 정상 판정이며 장르·camera·input·stage와 맞지 않는 asset을 억지로 만들지 않는다. `PRODUCTION_INFORMATION` 누락은 이 coverage gap으로 해결하지 않고 적합한 text/table/Flow/DB owner로 보낸다.

### State family completeness

대표 이미지 한 장이 있다고 component가 완성된 것은 아니다. current consumer에 필요한 상태만 기록한다.

| Family | Required States | Existing | Missing | Status | Linked Coverage / Requirement | Validation |
|---|---|---|---|---|---|---|

예: UI control의 Normal/Hover/Pressed/Disabled/Focus, enemy attack의 Wind-up/Telegraph/Active/Recovery, interactable의 Default/Targeted/Usable-or-Unavailable/Triggered, map node의 Current/Reachable/Selected/Locked/Completed. `COMPLETE`는 예시의 모든 상태가 아니라 **현재 consumer가 요구하는 상태가 모두 있음**을 뜻한다.

### Technical consumption

실제 게임 자산이면 필요한 항목만 기록한다.

```yaml
source_master:
export_format:
resolution_or_design_size:
aspect_ratio:
crop_and_safe_area:
alpha_or_mask:
filter_mode:
mipmap:
compression:
atlas_or_sprite_sheet:
slicing:
pivot_or_anchor:
nine_patch_or_scaling_region:
animation_fps_loop:
naming_and_variant:
engine_import_profile:
localization_text_separation:
performance_budget:
rights_or_provenance:
```

실제 target resolution/aspect에서 확인하고 pixel art, 9-patch, mipmap, atlas, slicing 등은 필요한 asset에만 적용한다. `PLATFORM_REQUIRED` 항목은 release 시 current official specification을 다시 확인한다.

## 3. Prompt contract

```text
ACTUAL_CONSUMER_REQUIRED
→ consumer_kind · consumer_surface · primary_use · consumer_validation
→ coverage_item_id · coverage_status · state_family_status
→ requirement_id · project_relation · 목적과 사용자 경험
→ 프로젝트 canon / Decision 고정
→ approved_visual_reference_ids · Keep/Avoid/Do Not Drift
→ 화면 구성과 정보 위계
→ 캐릭터·환경·오브젝트·UI 요구
→ 형태·색·재질·광원
→ 실제 화면비·크롭·해상도
→ 필요한 engine consumption constraints
→ 유지 요소와 변경 축
→ 금지·보호 요소
→ 텍스트 없는 master / 편집 가능한 후처리 계획
→ QA · readback · 재생성 기준
```

## 4. Review

| Review ID | Image ID | Consumer / Primary Use | Coverage/State Family | 기획 일치 | Approved Reference 일관성 | 핵심 경험 전달 | 실제 화면 가독성 | 구현 가능성 | 일관성 | 재사용·편집 | 권리·유사성 | 오류 | 판정 | 수정 요청 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Consumer / Primary Use는 생성 결과가 실제 게임/제품 surface의 목적을 충족하는지 확인한다. 설명용 문서 장식이 실제 consumer처럼 둔갑했으면 `REVISION_REQUIRED` 또는 `REJECTED`다.

Coverage/State Family은 관련 `coverage_item_id`의 어떤 상태를 실제로 충족하는지와 consumer에 필요한 상태 누락이 남는지를 확인한다. 생성 성공만으로 `COVERED_EXISTING`, `PROJECT_ASSET_APPROVED` 또는 runtime PASS를 만들지 않는다.

Approved Reference 일관성은 비율·silhouette·palette·line/texture/material·lighting·camera/composition·UI hierarchy·icon/VFX grammar를 필요한 범위에서 비교한다. Project canon과 visual reference가 충돌하면 `VISUAL_CANONICAL_CONFLICT`; 승인 source/readback을 확인할 수 없으면 `BLOCKED_UNVERIFIED`다.

### 4A. Reusable Visual Harvest Review

Primary Use Gate에서 원래 목적이 `ACCEPTED`된 결과만 Harvest 대상으로 본다. 이 표는 working review surface이며 `ASSET_MANIFEST.yml`, `PROJECT_ASSET_APPROVED`, `promote`를 대체하지 않는다.

| Harvest ID | Image ID | Primary Use | Candidate | Classification | Existing Reuse Conflict | Method | Derived Pixels | Target Reuse | Second Use | Decision |
|---|---|---|---|---|---|---|---|---|---|---|

- `Classification`: `REUSE_AS_IS / VARIANT_SEED / STRUCTURE_PATTERN / STYLE_DNA / REBUILD_FOR_REUSE / ONE_OFF_KEEP / REJECT_REUSE`.
- `Method`: `SOURCE_LAYER / MASK_CUTOUT / MANUAL_OR_SEMANTIC_REBUILD / DERIVED_GENERATIVE_RECOVERY`.
- `DERIVED_GENERATIVE_RECOVERY`는 source에서 관측한 사실이 아닌 generated/derived pixel이므로 별도 provenance와 review가 필요하다.
- `ONE_OFF_KEEP`는 재사용 실패가 아니라 title-specific composition을 보호하는 정상 판정이다.
- reuse promotion은 primary-use success, rights, `PROJECT_ASSET_APPROVED`, title-specific identity를 우회하지 않는다.

### 4B. Screen Interpretation Review

중요한 AI 생성 화면은 이미지와 별개로 interpretation record를 남긴다. Notion Asset/Knowledge Master의 Project-filtered record 또는 repository 책임 기록에 `screen_id / flow_id / interpretation_record_id`를 연결한다.

| Review ID | Screen ID | Flow ID | Interpretation Record ID | 관련 Decision | `CONFIRMED` | `DISCOVERED_IDEA` | `AI_ASSUMPTION` | `MISSING_CANON` | `VISUAL_CANONICAL_CONFLICT` | 버린 표현 | 다음 Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 없이 canon·implementation requirement로 승격하지 않는다.

### 4C. Flow registration

여러 Screen이 연결되면 semantic Screen/flow record에 `screen_id / flow_id`, entry point, primary path, cancel/return, failure recovery를 연결한다. 사람용 `VISUAL_MAP_DERIVED`는 이 record와 approved preview에서 재생성 가능한 표현이다.

Visual Map이나 clickable prototype은 runtime proof가 아니다. 제작자/AI용 관계도·시스템 Flow는 실제 game image backlog가 아니라 structured information artifact로 유지할 수 있다.

### 4D. Runtime compare

`runtime_compare_required: YES`인 화면은 approved project visual과 실제 implementation capture를 비교한다.

| Compare ID | Screen ID | Approved Artifact | runtime_capture_path | source commit | drift_status | 관찰 차이 | 후속 Decision/Finding |
|---|---|---|---|---|---|---|---|

`drift_status`: `MATCHED / INTENDED_DIFFERENCE / IMPLEMENTATION_GAP / PLANNING_CHANGE_REQUIRED / AI_MOCKUP_ERROR / VISUAL_CANONICAL_CONFLICT / BLOCKED_UNVERIFIED`.

실제 runtime capture가 없으면 planning preview나 Visual Map만으로 `MATCHED`를 주장하지 않는다.

### 4E. Reference / Benchmark review

외부 reference와 benchmark는 `REFERENCE` 또는 `BENCHMARK` record로 분리한다.

```yaml
reference_sources: []
reference_brief:
forbidden_expression:
source_provenance:
rights_license:
decision: ADOPT | ADAPT | TEST | REFERENCE_ONLY | AVOID | IGNORE
reference_similarity_status:
```

Reference/Benchmark가 유용하다는 이유만으로 Project Asset로 자동 promotion하지 않는다.

## 5. Notion attach / replace / readback

이미지나 파일을 Notion에 넣는 경우:

```text
generate / edit
→ 현재 workspace file boundary 확인
→ correct Project record/page target
→ upload / attach
→ target fetch readback
→ expected file / preview / version / Project 확인
→ readback_status = PASS
```

replace 작업이면 old version이 human current view에 남아 있지 않은지도 확인한다. readback 실패는 delivery success가 아니다.

`PRODUCTION_INFORMATION`을 Notion에 기록할 때는 이미지 attachment가 없다는 이유로 미완료로 보지 않는다. text/table/DB/Mermaid/Flow readback이 해당 owner에서 확인되면 정보 산출물 자체는 완료될 수 있다.

## 6. Approval sync

- [ ] `project_relation`과 Project Key 확인
- [ ] 먼저 production information인지 image asset인지 분리하고, 정보면 `TEXT_TABLE_FLOW_DB_FIRST`로 적합한 owner에 반영
- [ ] Image backlog row라면 `ACTUAL_CONSUMER_REQUIRED`의 consumer kind/surface/primary use/validation 확인
- [ ] 관련 coverage item의 applicability, `coverage_status`, `state_family_status` 확인
- [ ] coverage gap을 자동 image queue로 바꾸지 않았는지 확인
- [ ] `CURRENT_CONFIRMED_DECISIONS` 또는 해당 project decision owner 반영
- [ ] 관련 세계관·인물·시스템·아트·UI canon 반영
- [ ] GitHub Issue·PR·main 반영이 필요한 implementation task 연결
- [ ] Asset/Knowledge Master에 correct `Record Type`·Project·Status·Approved·Reuse·Decision 기록
- [ ] human Gallery에는 판단에 필요한 최소 속성만 노출
- [ ] AI/System metadata에는 Asset ID·Version·Status·Category·Prompt·AI Note·Source·Rights / License·Hash·Implementation Path 보존
- [ ] 신규 결과를 먼저 WIP/review candidate로 두고 사용자 승인 전 approved reference 또는 final project asset로 자동 승격 금지
- [ ] 중요 AI 화면은 필요 시 `interpretation_record_id`와 `screen_id / flow_id` 연결
- [ ] 연결된 Screen은 semantic flow를 갱신하고 `VISUAL_MAP_DERIVED`가 stale하면 재생성
- [ ] upload/replace 후 `readback_status` 확인
- [ ] 보존소 사용 시 `vault_source_key` 현재 상태 확인 또는 `VAULT_LOCAL_STATE_UNVERIFIED` 기록
- [ ] Primary Use Gate 뒤 `harvest_status`와 `reuse_classification` 별도 review
- [ ] structured candidate가 생긴 경우 local-only `asset_vault_harvest_record_id` 연결; 이 ID를 제품 asset approval로 해석하지 않음
- [ ] `APPROVED_CANDIDATE`까지 local-only 유지; tracked product asset 자동 생성 금지
- [ ] `PROJECT_ASSET_APPROVED` 후 `promotion_target` 확정·`promote` 실행·`promoted_path` 기록
- [ ] tracked Scene/Resource가 `assets/_vault_local/`을 참조하지 않는지 `project_asset_vault.py check` 실행
- [ ] 실제 적용·runtime 검증 상태 기록
- [ ] 실제 source/requirement/runtime evidence에 따라 coverage row readback
- [ ] `repository-wide-audit` 재실행