# Reusable Module Registry

- 상태: Base 공용 재사용 모듈 카탈로그
- 기준일: 2026-08-22 KST
- source method: `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- context synthesis method: `docs/knowledge/research/CONTEXT_DRIVEN_REUSE_SYNTHESIS.md`
- project scan template: `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`
- human view: `NOTION_HUMAN_VIEW`

## 1. 목적과 권위

이 Registry는 현재 ACTIVE 프로젝트들의 실제 반복 문제와 승인된 구조/roadmap을 비교해 **재사용할 가치가 있는 계약 단위**를 찾고, 프로젝트마다 처음부터 다시 설계하거나 구현하는 비용을 줄이기 위한 색인이다.

후보는 실제 evidence에서 추출할 수도 있고 project context에서 새로 합성할 수도 있다. Context-Synthesis는 contract hypothesis를 허용하지만 검증을 대신하지 않는다. 별도 evidence가 없는 구현은 `IMPLEMENTATION_NOT_BUILT`이며, completed-main 직접 증거가 있는 bounded Base 구현만 `REFERENCE_IMPLEMENTATION_EXISTS`로 기록한다. 특정 프로젝트의 유사 구현은 별도 adoption/evidence owner가 판정한다.

```text
module discovery != project adoption
module contract != shared runtime implementation
module discovery != PROJECT_ASSET_APPROVED
module discovery != NEW_SKILL_APPROVED
module contract != player-experience PASS
CONTEXT_SYNTHESIS_IS_NOT_VALIDATION
REFERENCE_IMPLEMENTATION_EXISTS != project adoption/runtime proof
NOTION_HUMAN_VIEW != repository structured/runtime authority
```

## 2. 현재 프로젝트 입력

Notion `PROJECT REGISTRY · Master`에서 2026-08-20 현재 `ACTIVE`로 분류된 10개 프로젝트를 1차 입력으로 사용했다.

| Project key | Repository | 이번 스캔에서 본 반복 문제 |
|---|---|---|
| `COC_FICTION` | `alsdmlals4-eng/Coc-Fiction` | Canon·출처·연속성·외부 원고 reconciliation·묶음 퇴고 |
| `GRIMOIRE` | `alsdmlals4-eng/GRIMOIRE-` | 글자→회로→주문 사용, 상태/효과, 단계 UI, 결과 품질 |
| `SWITCHY` | `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle` | 배치·경로·도달 가능성·LIFO·스위치·BUILD/RUN |
| `TETRIS` | `alsdmlals4-eng/Tetris` | Line/Chain 퍼즐, 진행/정지, Energy·Skill Tier, Combat Clock |
| `URBAN_LEGEND` | `alsdmlals4-eng/urban-legend` | 일정·사건·동료·연구·장비·지연 결과·원인 설명 |
| `NINJA_SURVIVAL` | `alsdmlals4-eng/ninja-survival-godot` | auto combat·보상 선택·백팩 배치·조합·REST 작업대 |
| `MY_LITTLE_BOAT` | `alsdmlals4-eng/MylittleBoat` | 짧은 평온 세션·사진·병편지·수집·동료 반응 |
| `BLACKSMITH` | `alsdmlals4-eng/Blacksmith` | 강화 push/stop·품질·아이템 생애·의뢰·지연 귀결 |
| `TEN_PACES` | `alsdmlals4-eng/Ten-Paces-Hidden-Moves` | 숨은 계획·동시 해결·공개정보 AI·설명 가능한 replay |
| `OMENWARD` | `alsdmlals4-eng/omenward` | 확률/룰렛 설계·wave·배치 commit·auto battle·결과 해설 |

## 3. 상태 어휘

### 3A. Three-axis candidate state

새 후보 또는 의미 있게 갱신하는 후보는 가능한 경우 다음 세 축을 분리해서 기록한다.

| Axis | 값 | 의미 |
|---|---|---|
| `candidate_origin` | `EVIDENCE_DERIVED` | 실제 구현·실패·benchmark·반복 기록에서 추출 |
| `candidate_origin` | `CONTEXT_SYNTHESIZED` | 현재 canon·roadmap·예상 반복비용에서 새 계약을 가설로 설계 |
| `candidate_origin` | `HYBRID` | evidence와 context synthesis를 함께 사용 |
| `maturity` | `HYPOTHESIS` | 구조 가설만 존재 |
| `maturity` | `MODULE_CONTRACT_DEFINED` | bounded interface/경계가 문서화됨 |
| `maturity` | `REFERENCE_IMPLEMENTATION_EXISTS` | Base reference 구현이 직접 존재 |
| `maturity` | `PROJECT_ADAPTER_VERIFIED` | 실제 project adapter/consumer 검증 증거 존재 |
| `maturity` | `PROJECT_MERGED` | 해당 project main 반영 증거 존재 |
| `validation_state` | `VALIDATION_NOT_RUN` | 아직 직접 검증 없음 |
| `validation_state` | `FOCUSED_VERIFIED` | bounded test/Pilot 검증 |
| `validation_state` | `MULTI_CONTEXT_VERIFIED` | 서로 다른 consumer/context 검증 |
| `validation_state` | `PLAYER_OR_USER_VERIFIED` | 필요한 human/player evidence까지 존재 |

```text
SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS
EVIDENCE_REQUIRED_FOR_PROMOTION
```

기존 Registry의 복합 status 문자열은 현재 소비자 호환성을 위해 유지하되, 그것을 origin/maturity/validation의 동일 축으로 해석하지 않는다.

### 3B. Existing status vocabulary

| 상태 | 의미 |
|---|---|
| `MODULE_CONTRACT_DEFINED` | 입력·상태·규칙·출력·경계가 Base 문서로 추상화됨 |
| `IMPLEMENTATION_NOT_BUILT` | 공용 runtime/tool 구현은 아직 만들지 않음 |
| `REFERENCE_IMPLEMENTATION_EXISTS` | Base에 bounded reference script/tool은 있으나 project adoption·live/runtime proof는 별도 |
| `PROJECT_IMPLEMENTATION_EXISTS` | 하나 이상의 프로젝트에 유사 기능이 실제 존재하지만 공용화하지 않음 |
| `PROJECT_SEED` | 특정 프로젝트에서 강하게 출발한 모듈. 다른 프로젝트 검증 전 보편화 금지 |
| `BASE_PROMOTION_CANDIDATE` | 둘 이상의 프로젝트/벤치마크에서 반복 가치가 보여 공용화 후보 |
| `BASE_ACTIVE_METHOD` | 이미 Base의 실행 방법/Template로 사용 중 |
| `EXISTING_OWNER_REUSE` | 새 도구/Skill을 만들지 않고 기존 Base owner를 재사용 |
| `NO_DEDICATED_CAPTURE_APP` | 별도 검증 GUI/app 대신 repository/runtime/CI 증거를 조합 |
| `DIRECT_LICENSED_REUSE_CANDIDATE` | 라이선스·버전·보안·소비 경로 검토 후 직접 자산/패키지 재사용 가능 후보 |
| `RIGHTS_REVIEW_REQUIRED` | 표현·상표·trade dress·라이선스 등 별도 권리 검토가 필요 |
| `NOTION_HUMAN_VIEW` | Notion은 사람이 보는 요약/현황. 구조화·runtime 권위는 저장소/프로젝트 owner |

## 4. 우선 구현 후보

첫 공용 구현 Pilot은 **프로젝트 수가 많고, 인터페이스가 좁으며, 프로젝트 고유 정체성을 덜 훼손하는 것**부터 한다.

### P0 · 먼저 공용화 검증

1. `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE`
2. `RM-SYS-002 PHASED_SESSION_STATE_MACHINE`
3. `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`
4. `RM-SYS-004 EXPLAINABLE_RESULT_PACKET`
5. `RM-SYS-005 EVENT_CONDITION_CHOICE_OUTCOME_ENGINE`
6. `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR`
7. `RM-VIS-001 SEMANTIC_UI_SKIN_KIT`
8. `RM-VIS-002 GAMEPLAY_SYMBOL_ATLAS`

이 목록은 공용 코드 구현 승인이나 모든 프로젝트 일괄 적용을 뜻하지 않는다. 각 프로젝트에서 adapter 비용과 실제 소비자를 확인한 뒤 최소 Pilot부터 적용한다.

`RM-TOOL-005`, `RM-VIS-006`, `RM-WORK-003`은 2026-08-22에 추가된 **조건부 연구/제작/workflow candidate**다. 기존 P0 gameplay/runtime 우선순위를 밀어내지 않으며 실제 소비 장면에서만 Pilot한다.

## 5. Gameplay / content / narrative modules

| ID | Module | 출발 프로젝트 | 1차 판정 | 상태 |
|---|---|---|---|---|
| `RM-SYS-001` | `GRID_PLACEMENT_RULE_ENGINE` | TETRIS / NINJA_SURVIVAL / SWITCHY | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_EXISTS` |
| `RM-SYS-002` | `PHASED_SESSION_STATE_MACHINE` | URBAN_LEGEND / NINJA_SURVIVAL / SWITCHY / GRIMOIRE / MY_LITTLE_BOAT / OMENWARD | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-003` | `CANDIDATE_DRAFT_WEIGHT_ENGINE` | NINJA_SURVIVAL / OMENWARD / URBAN_LEGEND | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_EXISTS` |
| `RM-SYS-004` | `EXPLAINABLE_RESULT_PACKET` | URBAN_LEGEND / TEN_PACES / OMENWARD / BLACKSMITH / NINJA_SURVIVAL / SWITCHY | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-005` | `EVENT_CONDITION_CHOICE_OUTCOME_ENGINE` | URBAN_LEGEND / GRIMOIRE / MY_LITTLE_BOAT / COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-006` | `DELAYED_CONSEQUENCE_REENTRY_ENGINE` | URBAN_LEGEND / BLACKSMITH / COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-007` | `STAGE_WAVE_ENCOUNTER_DIRECTOR` | NINJA_SURVIVAL / OMENWARD / GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-008` | `RESEARCH_RESOURCE_QUEUE` | URBAN_LEGEND / GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-009` | `COMPANION_SUPPORT_TRIGGER_ENGINE` | URBAN_LEGEND / MY_LITTLE_BOAT / GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-010` | `COLLECTION_HISTORY_REGISTRY` | BLACKSMITH / MY_LITTLE_BOAT / GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-011` | `CARD_ACTION_EFFECT_ENGINE` | GRIMOIRE / TETRIS / NINJA_SURVIVAL | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-012` | `SURVIVOR_AUTO_COMBAT_PROGRESSION_CORE` | NINJA_SURVIVAL | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-013` | `FALLING_BLOCK_LINE_CLEAR_CORE` | TETRIS | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · IMPLEMENTATION_NOT_BUILT · RIGHTS_REVIEW_REQUIRED` |
| `RM-SYS-014` | `CHAIN_MATCH_COMBO_CORE` | TETRIS | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-015` | `HIDDEN_PLAN_RESOLUTION_ENGINE` | TEN_PACES | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-SYS-016` | `ROUTE_STACK_LOGISTICS_ENGINE` | SWITCHY | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-SYS-017` | `SPELL_COMPOSE_VALIDATE_COMMIT_ENGINE` | GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-SYS-018` | `ROULETTE_TOKEN_SOURCE_ENGINE` | OMENWARD | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-SYS-019` | `PUSH_YOUR_LUCK_ENHANCEMENT_ENGINE` | BLACKSMITH | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-SYS-020` | `CALM_DISCOVERY_SESSION_CORE` | MY_LITTLE_BOAT | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · IMPLEMENTATION_NOT_BUILT` |
| `RM-NAR-001` | `NARRATIVE_NODE_CHOICE_STATE_ENGINE` | COC_FICTION / URBAN_LEGEND / GRIMOIRE / MY_LITTLE_BOAT | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-NAR-002` | `CANON_SOURCE_PROVENANCE_REGISTRY` | COC_FICTION / URBAN_LEGEND / GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-NAR-003` | `CONTINUITY_REVISION_REGRESSION` | COC_FICTION / URBAN_LEGEND / GRIMOIRE | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · PROJECT_IMPLEMENTATION_EXISTS` |
| `RM-NAR-004` | `EXTERNAL_ARTIFACT_RECONCILIATION_WORKFLOW` | COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · PROJECT_SEED · PROJECT_IMPLEMENTATION_EXISTS` |

상세 계약: `GAMEPLAY_AND_CONTENT_MODULES.md`.

## 6. Production / tool / workflow modules

| ID | Module | 출발 프로젝트/기존 owner | 판정 | 상태 |
|---|---|---|---|---|
| `RM-TOOL-001` | `DATA_SCHEMA_CROSSREF_VALIDATOR` | 전체 데이터 중심 프로젝트 | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_EXISTS` |
| `RM-TOOL-002` | `DETERMINISTIC_SEED_REPLAY_CAPTURE` | TEN_PACES / OMENWARD / BLACKSMITH / SWITCHY / TETRIS / NINJA_SURVIVAL | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-TOOL-003` | `BALANCE_SCENARIO_BATCH_SIMULATOR` | deterministic runner + project snapshot candidate | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · REFERENCE_IMPLEMENTATION_EXISTS · MULTI_PROJECT_READ_ONLY_CONTRACT_EVIDENCE` |
| `RM-TOOL-004` | `REPOSITORY_NATIVE_EVIDENCE_CAPTURE` | current project tests/runtime/CI + Notion human link | `EXISTING_OWNER_REUSE` | `BASE_ACTIVE_METHOD · NO_DEDICATED_CAPTURE_APP` |
| `RM-TOOL-005` | `PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER` | public talk/tutorial/developer interview evidence | `PATTERN_EXTRACT` + thin `yt-dlp` adapter | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_EXISTS` |
| `RM-WORK-001` | `PROJECT_REUSE_OPPORTUNITY_SCAN` | merged Base reverse-engineering method | `EXISTING_OWNER_REUSE` | `BASE_ACTIVE_METHOD` |
| `RM-WORK-002` | `SKILL_WORKFLOW_PATTERN_EVAL` | `docs/AI_SKILL_ADOPTION_GUIDE.md` | `EXISTING_OWNER_REUSE` | `BASE_ACTIVE_METHOD · HUMAN_EDIT_DELTA` |
| `RM-WORK-003` | `HUMAN_FACING_ARTIFACT_SYNTHESIS` | Base human-publication context + official presentation-AI patterns | `HYBRID · PROVIDER_NEUTRAL` | `MODULE_CONTRACT_DEFINED · VALIDATION_NOT_RUN` |

`RM-TOOL-005` reference implementation: `tools/public_video_research_ingest.py`. Network-free unit test evidence와 실제 live YouTube compatibility는 구분한다.

`RM-WORK-003` contract: `HUMAN_FACING_ARTIFACT_SYNTHESIS.md`. 특정 Gamma/Canva/Beautiful.ai/Pitch/SlidesAI provider를 Base 기본값으로 채택하지 않는다.

상세 tool/workflow 계약: `PRODUCTION_TOOL_WORKFLOW_MODULES.md`.

## 7. Visual / asset-material modules

| ID | Module | 주요 적용 프로젝트 | 판정 | 상태 |
|---|---|---|---|---|
| `RM-VIS-001` | `SEMANTIC_UI_SKIN_KIT` | 모든 Godot 게임 | `PATTERN_EXTRACT` + 필요 시 `DIRECT_LICENSED_REUSE` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_EXISTS` |
| `RM-VIS-002` | `GAMEPLAY_SYMBOL_ATLAS` | 전 프로젝트 중 UI/상태 아이콘 소비자 | `PATTERN_EXTRACT` + 필요 시 `DIRECT_LICENSED_REUSE` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · REFERENCE_IMPLEMENTATION_EXISTS` |
| `RM-VIS-003` | `MODULAR_BACKGROUND_LAYER_KIT` | URBAN_LEGEND / GRIMOIRE / MY_LITTLE_BOAT / COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-004` | `COMBAT_TELEGRAPH_VFX_KIT` | NINJA_SURVIVAL / OMENWARD / GRIMOIRE / TEN_PACES | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-005` | `PORTRAIT_STATE_VARIANT_KIT` | URBAN_LEGEND / GRIMOIRE / COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-006` | `VISUAL_CREATIVE_PROVIDER_ADAPTER` | 시각 제작 provider가 필요한 모든 프로젝트의 조건부 production path | `PATTERN_EXTRACT · PROVIDER_NEUTRAL` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |

`RM-VIS-006`은 runtime visual module이나 새 art owner가 아니다. 기존 project Visual Canon/brief 아래에서 AI service·local model·manual·approved outsource를 교체 가능한 제작 backend로 비교하고 `HUMAN_EDIT_DELTA`를 남긴다.

상세 계약: `VISUAL_ASSET_MATERIAL_MODULES.md`.

## 8. 프로젝트별 module fit map

`◎` 직접 핵심, `○` 높은 재사용 가치, `△` 선택 적용.

| Project | 핵심 module fit |
|---|---|
| `COC_FICTION` | ◎ RM-NAR-001/002/003/004 · ○ RM-SYS-005/006 · ○ RM-VIS-003/005 · ○ RM-WORK-001/002 |
| `GRIMOIRE` | ◎ RM-SYS-017 · ○ RM-SYS-002/005/007/009/011 · ○ RM-NAR-001/002/003 · ○ RM-VIS-001/002/003/004/005 |
| `SWITCHY` | ◎ RM-SYS-001/016 · ○ RM-SYS-002/004 · ○ RM-TOOL-002/004 · ○ RM-VIS-001/002 |
| `TETRIS` | ◎ RM-SYS-013/014 · ○ RM-SYS-001/002/011 · ○ RM-TOOL-002/003/004 · ○ RM-VIS-001/002 |
| `URBAN_LEGEND` | ◎ RM-SYS-005/006/008/009 · ○ RM-SYS-002/003/004/010 · ○ RM-NAR-001/002/003 · ○ RM-TOOL-004 · ○ RM-VIS-003/005 |
| `NINJA_SURVIVAL` | ◎ RM-SYS-001/012 · ○ RM-SYS-002/003/004/007/011 · ○ RM-TOOL-002/003/004 · ○ RM-VIS-001/002/004 |
| `MY_LITTLE_BOAT` | ◎ RM-SYS-020 · ○ RM-SYS-002/005/009/010 · △ RM-NAR-001 · ○ RM-TOOL-004 · ○ RM-VIS-001/002/003 |
| `BLACKSMITH` | ◎ RM-SYS-019 · ○ RM-SYS-004/006/010 · ○ RM-TOOL-002/003/004 · ○ RM-VIS-001/002 |
| `TEN_PACES` | ◎ RM-SYS-015 · ○ RM-SYS-004 · ○ RM-TOOL-002/004 · ○ RM-VIS-001/002/004 |
| `OMENWARD` | ◎ RM-SYS-018 · ○ RM-SYS-002/003/004/007 · ○ RM-TOOL-002/003/004 · ○ RM-VIS-001/002/004 |

`RM-TOOL-005`는 project runtime fit이 아니라 **공개 영상 본문 evidence가 필요한 조사 작업의 조건부 입력 adapter**라서 위 project runtime fit 행에 일괄 추가하지 않는다. `RM-VIS-006`도 모든 프로젝트에 강제하지 않고 실제 시각 제작이 승인된 단계에서 기존 RM-VIS/project-specific target에 붙인다. `RM-WORK-003`도 human-facing artifact가 실제 필요한 작업에서만 조건부로 소비한다.

## 9. 벤치마크 및 Existing Solution disposition

| Source | 추출 원리 | 판정 |
|---|---|---|
| Godot 4.7 Scenes / Resources | 데이터와 재사용 가능한 scene/script를 분리해 작은 인터페이스로 조립 | `ADOPT` |
| ink | story state와 branching choice를 content/presentation에서 분리 | `ADAPT` |
| Yarn Spinner | dialogue runner / option presentation / variable storage 경계 | `ADAPT` |
| Seoul 2033 | 선택·판단과 이후 귀결이 이어지는 텍스트 선택 구조의 공개적으로 확인 가능한 원리만 사용 | `ADAPT` |
| Slay the Spire | 카드/효과를 조합 가능한 build 단위로 보고 데이터·밸런스를 반복 조정 | `ADAPT` |
| Vampire Survivors | 실시간 압박 속 자동행동 + 성장 선택 + run/meta 분리 | `ADAPT` |
| Backpack Battles 계열 | inventory arrangement 자체를 전투 전 전략 입력으로 사용 | `ADAPT` |
| Kenney CC0 packs | prototype/일부 UI 재료의 직접 라이선스 재사용 가능성 | `DIRECT_LICENSED_REUSE_CANDIDATE` |
| Tetris | 공간 배치와 line completion이라는 추상 원리만 분석 | `PATTERN_EXTRACT · RIGHTS_REVIEW_REQUIRED` |
| yt-dlp | public video metadata/caption track discovery를 좁은 CLI contract로 사용 | `ADAPT_LICENSED · THIN_ADAPTER` |
| ytscribe | subtitles-first + optional local ASR + provenance pattern | `REFERENCE_ONLY · POSSIBLE_BOUNDED_PILOT` |
| youtube-transcript-api | 간단한 transcript access pattern, cloud/provider IP blocking·proxy 운영 위험 | `TEST_ONLY · NOT_DEFAULT` |
| TodayFreeAI presentation page | 현재 환경에서 exact body fetch 실패; 제품 discovery trigger로만 사용 | `DISCOVERY_ONLY` |
| Gamma / Canva / Beautiful.ai / Pitch / SlidesAI official sources | outline/structure, editable artifact, brand constraints, post-generation review의 provider-neutral workflow pattern | `PATTERN_EXTRACT · HYBRID_INPUT` |

외부 사례의 성공은 현재 프로젝트의 재미·시장성·생산성 PASS가 아니다. 각 module/workflow는 실제 프로젝트 Pilot에서 별도 검증한다.

## 10. 권리 및 복제 방지

### `TETRIS_TRADE_DRESS_BOUNDARY`

`RM-SYS-013`은 낙하/배치/line completion 같은 **추상적인 상호작용 계약**을 프로젝트 요구에 맞게 독립 설계하기 위한 seed다. Tetris 로고, 테마곡, Tetrimino 명칭/표현, 공식 색·UI·trade dress 또는 특정 작품의 시그니처 표현을 이 Registry가 재사용 승인하지 않는다. 제품화 전 `RIGHTS_REVIEW_REQUIRED`를 유지한다.

### Licensed asset boundary

CC0·MIT 등 재사용 가능한 자료도 아래가 끝나기 전에는 프로젝트 자산/의존성이 아니다.

```text
license/source/version check
→ security/dependency check when executable
→ project visual/core fit
→ actual consumer
→ local provenance
→ runtime/visual validation
→ project owner promotion
```

### Public transcript / generated visual / provider boundary

- 제3자 공개 영상 transcript는 연구 입력이지 재배포 가능한 Base 콘텐츠라는 뜻이 아니다. 전체 transcript는 기본 local-only이며 repository에는 derived note·timestamp·필요한 짧은 근거만 남긴다.
- auto caption/local ASR은 human-authored transcript로 승격하지 않는다.
- AI provider를 바꾸거나 generated visual을 후처리해도 입력 reference의 권리·최종 similarity·provider terms 검토를 우회하지 않는다.
- `VISUAL_CREATIVE_PROVIDER_ADAPTER`는 `PROJECT_ASSET_APPROVED` 권한을 갖지 않는다.
- Presentation provider의 generated deck/import/export는 project canon 또는 human-quality PASS를 자동 획득하지 않는다.

## 11. 다음 검증

1. P0 module 중 한 개씩 **서로 다른 2개 프로젝트**에 적용 가능한 adapter contract를 작성한다.
2. 실제로 중복 코드/기획 시간이 줄었는지 비교한다.
3. 플레이 경험을 바꾸는 gameplay module은 release-near Vertical Slice에서 검증한다.
4. Visual module은 Notion Asset/Visual workflow와 repository implementation evidence를 통해 실제 화면 품질을 검수한다.
5. `RM-TOOL-004`는 별도 capture app 설치 없이 project-native test/runtime/CI evidence로 실제 유용성을 검증한다.
6. `RM-TOOL-005`는 `yt-dlp`가 준비된 실제 로컬 환경에서 manual caption, auto caption, no-caption 대표 영상 각각을 검증하고 site compatibility·failure recovery evidence를 남긴다.
7. `RM-VIS-006`은 실제 승인된 시각 제작 작업에서 기존 방식과 provider 후보를 `HUMAN_EDIT_DELTA`로 비교하고 quality/consistency/rights가 함께 개선되는지 확인한다.
8. `RM-WORK-003`은 기존 승인 자료 하나를 source로 smallest Pilot을 수행하고 outline-first/claim-gap review가 total human edit + QA cost를 줄이는지 확인한다.
9. 공용 구현이 오히려 프로젝트별 예외 분기만 늘리면 `PROJECT_SEED` 또는 reference-only로 되돌린다.
10. Notion에는 `NOTION_HUMAN_VIEW`로 module ID·프로젝트 fit·상태를 보여 주되, 구현 상태는 이 Registry와 실제 프로젝트 저장소에서 판정한다.
