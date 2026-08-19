# Reusable Module Registry

- 상태: Base 공용 재사용 모듈 카탈로그
- 기준일: 2026-08-20 KST
- source method: `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- project scan template: `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`
- human view: `NOTION_HUMAN_VIEW`

## 1. 목적과 권위

이 Registry는 현재 ACTIVE 프로젝트들의 실제 반복 문제를 비교해 **재사용할 가치가 있는 계약 단위**를 찾고, 프로젝트마다 처음부터 다시 설계하거나 구현하는 비용을 줄이기 위한 색인이다.

이 문서가 기록하는 것은 `MODULE_CONTRACT_DEFINED` 상태다. 별도 증거가 없는 모듈은 `IMPLEMENTATION_NOT_BUILT`이며 공용 Godot 코드가 이미 존재한다고 주장하지 않는다. 특정 프로젝트에 유사 구현이 있어도 그것은 `PROJECT_IMPLEMENTATION_EXISTS`일 뿐 Base 공용 구현 증거가 아니다.

```text
module discovery != project adoption
module contract != shared runtime implementation
module discovery != PROJECT_ASSET_APPROVED
module discovery != NEW_SKILL_APPROVED
module contract != player-experience PASS
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

| 상태 | 의미 |
|---|---|
| `MODULE_CONTRACT_DEFINED` | 입력·상태·규칙·출력·경계가 Base 문서로 추상화됨 |
| `IMPLEMENTATION_NOT_BUILT` | 공용 runtime/tool 구현은 아직 만들지 않음 |
| `PROJECT_IMPLEMENTATION_EXISTS` | 하나 이상의 프로젝트에 유사 기능이 실제 존재하지만 공용화하지 않음 |
| `PROJECT_SEED` | 특정 프로젝트에서 강하게 출발한 모듈. 다른 프로젝트 검증 전 보편화 금지 |
| `BASE_PROMOTION_CANDIDATE` | 둘 이상의 프로젝트/벤치마크에서 반복 가치가 보여 공용화 후보 |
| `BASE_ACTIVE_METHOD` | 이미 Base의 실행 방법/Template로 사용 중 |
| `EXISTING_OWNER_REUSE` | 새 도구/Skill을 만들지 않고 기존 Base owner를 재사용 |
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

## 5. Gameplay / content / narrative modules

| ID | Module | 출발 프로젝트 | 1차 판정 | 상태 |
|---|---|---|---|---|
| `RM-SYS-001` | `GRID_PLACEMENT_RULE_ENGINE` | TETRIS / NINJA_SURVIVAL / SWITCHY | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-002` | `PHASED_SESSION_STATE_MACHINE` | URBAN_LEGEND / NINJA_SURVIVAL / SWITCHY / GRIMOIRE / MY_LITTLE_BOAT / OMENWARD | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-SYS-003` | `CANDIDATE_DRAFT_WEIGHT_ENGINE` | NINJA_SURVIVAL / OMENWARD / URBAN_LEGEND | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
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
| `RM-TOOL-001` | `DATA_SCHEMA_CROSSREF_VALIDATOR` | 전체 데이터 중심 프로젝트 | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-TOOL-002` | `DETERMINISTIC_SEED_REPLAY_CAPTURE` | TEN_PACES / OMENWARD / BLACKSMITH / SWITCHY / TETRIS / NINJA_SURVIVAL | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT` |
| `RM-TOOL-003` | `BALANCE_SCENARIO_BATCH_SIMULATOR` | 기존 Balance & Scenario Lab 방향 | `EXISTING_OWNER_REUSE` | `MODULE_CONTRACT_DEFINED · EXISTING_OWNER_REUSE` |
| `RM-TOOL-004` | `QA_EVIDENCE_CAPTURE_ADAPTER` | `tools/qa-evidence-studio` | `EXISTING_OWNER_REUSE` | `EXISTING_OWNER_REUSE · PROJECT_ADAPTER_ONLY` |
| `RM-WORK-001` | `PROJECT_REUSE_OPPORTUNITY_SCAN` | merged Base reverse-engineering method | `EXISTING_OWNER_REUSE` | `BASE_ACTIVE_METHOD` |
| `RM-WORK-002` | `SKILL_WORKFLOW_PATTERN_EVAL` | `docs/AI_SKILL_ADOPTION_GUIDE.md` | `EXISTING_OWNER_REUSE` | `BASE_ACTIVE_METHOD` |

상세 계약: `PRODUCTION_TOOL_WORKFLOW_MODULES.md`.

## 7. Visual / asset-material modules

| ID | Module | 주요 적용 프로젝트 | 판정 | 상태 |
|---|---|---|---|---|
| `RM-VIS-001` | `SEMANTIC_UI_SKIN_KIT` | 모든 Godot 게임 | `PATTERN_EXTRACT` + 필요 시 `DIRECT_LICENSED_REUSE` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-002` | `GAMEPLAY_SYMBOL_ATLAS` | 전 프로젝트 중 UI/상태 아이콘 소비자 | `PATTERN_EXTRACT` + 필요 시 `DIRECT_LICENSED_REUSE` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-003` | `MODULAR_BACKGROUND_LAYER_KIT` | URBAN_LEGEND / GRIMOIRE / MY_LITTLE_BOAT / COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-004` | `COMBAT_TELEGRAPH_VFX_KIT` | NINJA_SURVIVAL / OMENWARD / GRIMOIRE / TEN_PACES | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |
| `RM-VIS-005` | `PORTRAIT_STATE_VARIANT_KIT` | URBAN_LEGEND / GRIMOIRE / COC_FICTION | `PATTERN_EXTRACT` | `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE` |

상세 계약: `VISUAL_ASSET_MATERIAL_MODULES.md`.

## 8. 프로젝트별 module fit map

`◎` 직접 핵심, `○` 높은 재사용 가치, `△` 선택 적용.

| Project | 핵심 module fit |
|---|---|
| `COC_FICTION` | ◎ RM-NAR-001/002/003/004 · ○ RM-SYS-005/006 · ○ RM-VIS-003/005 · ○ RM-WORK-001/002 |
| `GRIMOIRE` | ◎ RM-SYS-017 · ○ RM-SYS-002/005/007/009/011 · ○ RM-NAR-001/002/003 · ○ RM-VIS-001/002/003/004/005 |
| `SWITCHY` | ◎ RM-SYS-001/016 · ○ RM-SYS-002/004 · ○ RM-TOOL-002 · ○ RM-VIS-001/002 |
| `TETRIS` | ◎ RM-SYS-013/014 · ○ RM-SYS-001/002/011 · ○ RM-TOOL-002/003 · ○ RM-VIS-001/002 |
| `URBAN_LEGEND` | ◎ RM-SYS-005/006/008/009 · ○ RM-SYS-002/003/004/010 · ○ RM-NAR-001/002/003 · ○ RM-VIS-003/005 |
| `NINJA_SURVIVAL` | ◎ RM-SYS-001/012 · ○ RM-SYS-002/003/004/007/011 · ○ RM-TOOL-002/003 · ○ RM-VIS-001/002/004 |
| `MY_LITTLE_BOAT` | ◎ RM-SYS-020 · ○ RM-SYS-002/005/009/010 · △ RM-NAR-001 · ○ RM-VIS-001/002/003 |
| `BLACKSMITH` | ◎ RM-SYS-019 · ○ RM-SYS-004/006/010 · ○ RM-TOOL-002/003 · ○ RM-VIS-001/002 |
| `TEN_PACES` | ◎ RM-SYS-015 · ○ RM-SYS-004 · ○ RM-TOOL-002 · ○ RM-VIS-001/002/004 |
| `OMENWARD` | ◎ RM-SYS-018 · ○ RM-SYS-002/003/004/007 · ○ RM-TOOL-002/003 · ○ RM-VIS-001/002/004 |

## 9. 벤치마크 및 Existing Solution disposition

| Source | 추출 원리 | 판정 |
|---|---|---|
| Godot 4.7 Scenes / Resources | 데이터와 재사용 가능한 scene/script를 분리해 작은 인터페이스로 조립 | `ADOPT` |
| ink | story state와 branching choice를 content/presentation에서 분리 | `ADAPT` |
| Yarn Spinner | dialogue runner / option presentation / variable storage 경계 | `ADAPT` |
| Seoul 2033 | 선택·상태·아이템·부상/스트레스가 이후 사건에 영향을 주는 텍스트 선택 구조 | `ADAPT` |
| Slay the Spire | 카드/효과를 조합 가능한 build 단위로 보고 데이터·밸런스를 반복 조정 | `ADAPT` |
| Vampire Survivors | 실시간 압박 속 자동행동 + 성장 선택 + run/meta 분리 | `ADAPT` |
| Backpack Battles 계열 | inventory arrangement 자체를 전투 전 전략 입력으로 사용 | `ADAPT` |
| Kenney CC0 packs | prototype/placeholder와 일부 최종 UI 재료의 직접 라이선스 재사용 가능성 | `DIRECT_LICENSED_REUSE_CANDIDATE` |
| Tetris | 공간 배치와 line completion이라는 추상 원리만 분석 | `PATTERN_EXTRACT · RIGHTS_REVIEW_REQUIRED` |

외부 사례의 성공은 현재 프로젝트의 재미·시장성 PASS가 아니다. 각 module은 실제 프로젝트 Pilot에서 별도 검증한다.

## 10. 권리 및 복제 방지

### `TETRIS_TRADE_DRESS_BOUNDARY`

`RM-SYS-013`은 낙하/배치/line completion 같은 **추상적인 상호작용 계약**을 프로젝트 요구에 맞게 독립 설계하기 위한 seed다. Tetris 로고, 테마곡, Tetrimino 명칭/표현, 공식 색·UI·trade dress 또는 특정 작품의 시그니처 표현을 이 Registry가 재사용 승인하지 않는다. 현재 Tetris 공식 사이트가 관련 상표와 trade dress 소유를 명시하므로 제품화 전 `RIGHTS_REVIEW_REQUIRED`를 유지한다.

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

## 11. 다음 검증

1. P0 module 중 한 개씩 **서로 다른 2개 프로젝트**에 적용 가능한 adapter contract를 작성한다.
2. 실제로 중복 코드/기획 시간이 줄었는지 비교한다.
3. 플레이 경험을 바꾸는 gameplay module은 release-near Vertical Slice에서 검증한다.
4. Visual module은 Asset Vault / Reusable Visual Harvest를 통해 실제 화면 품질을 검수한다.
5. 공용 구현이 오히려 프로젝트별 예외 분기만 늘리면 `PROJECT_SEED`로 되돌린다.
6. Notion에는 `NOTION_HUMAN_VIEW`로 module ID·프로젝트 fit·상태를 보여 주되, 구현 상태는 이 Registry와 실제 프로젝트 저장소에서 판정한다.
