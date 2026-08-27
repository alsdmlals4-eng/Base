# GPT 이미지 생성·검수 정책

이 문서는 Base를 적용한 프로젝트의 이미지·목업·UI 시각화 생성, 검수, 승인, Notion 전달, 자산 승격과 재사용 경계를 정의한다.

현재 작업면은 `DOMAIN_SPLIT_CANON`을 따른다.

```text
NOTION_HUMAN_FACING_CANON
→ Project Home / Visual Bible / Flow / Asset·Reference / 사람이 이해하는 승인 상태

REPOSITORY_STRUCTURED_CANON
→ Markdown / JSON / game data / ASSET_MANIFEST / Scene / Resource / Test

REPOSITORY_RUNTIME_TRUTH
→ 실제 적용 / build / runtime / device evidence

Google Sheets
→ COMPATIBILITY_ONLY migration source
→ 신규 이미지 기획·승인·동기화의 기본 작업면이 아님
```

프로젝트 정본·최신 사용자 승인·실제 구현이 이 정책보다 우선한다. GPT 생성 이미지는 승인 전까지 정본·최종 자산·구현 완료 증거가 아니다. 생성 성공은 자동 승인이나 다음 이미지 생성 권한을 만들지 않는다.

## 0. Visual Asset Coverage Preflight

프로젝트 전체, 화면군, 캐릭터군, 적군, UI군, 아이템군, 환경군, 마케팅 asset set처럼 **한 장보다 넓은 시각 범위**를 다루거나 현재 이미지 요청이 기존 asset set의 일부일 때는 subordinate `docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`로 화면을 먼저 열거한 뒤 canonical `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`로 교차 검사한다.

```text
current Project canon / stage / consumer
→ SCREEN_SURFACE_INVENTORY_FIRST + screen-to-asset matrix handoff
→ production information인지 먼저 판정
→ actual consumer가 있는 image asset 후보인지 판정
→ existing approved asset / implementation / reuse 조회
→ relevant coverage item applicability 판정
→ coverage_status + STATE_FAMILY_COMPLETENESS 확인
→ 필요한 gap만 Visual Requirement Gate로 전달
```

- coverage checklist는 `COVERAGE_CHECK_ONLY`, `NOT_A_SECOND_ASSET_CANON`이다. 실제 requirement, 승인 asset, Manifest, Notion Asset, repository/runtime state를 복제 소유하지 않는다.
- `coverage_item_id`와 `coverage_status`는 누락 탐지·추적용이며, 실제 자산 상태는 기존 `requirement_id`·Asset owner·runtime evidence에 link한다.
- `GAP_BLOCKING`은 현재 목표의 실제 player-facing flow나 제출 요구를 막는 경우에만 사용한다. 장르·단계·소비처에 필요하지 않으면 이유 있는 `NOT_APPLICABLE`이 정상이다.
- `STATE_FAMILY_COMPLETENESS`는 대표 한 장만 확인하지 않고 버튼 상태, enemy wind-up/active/recovery, interactable state처럼 소비처가 요구하는 상태군이 있는지 확인한다.
- target resolution/aspect, crop/alpha, import/filter/mipmap/compression/atlas/slicing/pivot/localization 같은 engine consumption 조건은 해당 자산에 실제 필요한 항목만 requirement/handoff에 연결한다.
- `PLATFORM_SPEC_RECHECK_REQUIRED`: store/capsule/screenshot/app icon 등 플랫폼 제출용 자산은 release 시점의 현재 공식 규격·콘텐츠 규칙을 다시 조회한다. Base의 오래된 고정 수치를 정답으로 사용하지 않는다.
- **`NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`**: coverage gap은 이미지 생성·batch 확대·다음 variant 자동 생산 권한이 아니다. 아래 Visual Requirement Gate와 Image Conversation Approval Gate를 그대로 적용한다.
- 사용자가 특정 이미지 한 장만 요청한 경우 해당 요청과 직접 관련된 coverage item만 확인하며, 전체 프로젝트 inventory를 자동으로 확장하지 않는다.

Coverage preflight는 **빠뜨린 종류·상태가 있는가**를 묻는다. 아래 Information Artifact / Actual Consumer Gate와 Visual Requirement Gate는 그 후보를 **어떤 형식으로 만들어야 하는가, 실제로 만들 가치가 있는가**로 다시 좁힌다.

### 0A. Information Artifact / Actual Consumer Gate

프로젝트를 이해하고 제작하기 위한 정보는 이미지 생성 제한 때문에 사라지면 안 된다.

```text
PRODUCTION_INFORMATION
INFORMATION_ARTIFACT_NOT_IMAGE_ASSET
TEXT_TABLE_FLOW_DB_FIRST
ACTUAL_CONSUMER_REQUIRED
```

`PRODUCTION_INFORMATION`에는 제작자와 AI가 알아야 할 시스템 설명, 세계관, 캐릭터·세력 관계, 관계도, 제작 체크리스트, 밸런스·경제 구조, Flow, 상태 전이, 구현 계약 등이 포함된다. 이런 정보는 필요하면 생성·갱신한다.

기본 routing:

```text
정보가 필요함
→ 텍스트 / 표 / Notion DB / Mermaid / Flow / JSON 등 editable·searchable 형식으로 충분한가
→ YES: TEXT_TABLE_FLOW_DB_FIRST
→ 필요한 production information을 해당 정본 owner에 생성·갱신
→ image generation은 하지 않음

이미지 자체가 필요함
→ ACTUAL_CONSUMER_REQUIRED
→ 실제 게임/제품 소비처 확인
→ Visual Requirement Gate
→ Image Conversation Approval Gate
→ generate/edit
```

`INFORMATION_ARTIFACT_NOT_IMAGE_ASSET`:

- 시스템 설명, 세계관 설명, 관계도, 제작 체크리스트가 필요하다는 사실만으로 설명용 이미지 시트를 만들지 않는다.
- 제작자·AI가 정보를 알아야 하는 목적이면 구조화 텍스트·표·DB·Mermaid·Flow를 우선한다.
- 문서를 예쁘게 꾸미는 용도, AI에게 보여주기 위한 고해상도 설명판, 체크리스트 장식용 이미지는 project image backlog의 기본 대상이 아니다.
- 정보 산출물에 diagram이 필요하면 Mermaid/Flow/노드처럼 수정 가능한 구조 표현을 먼저 사용한다.

`ACTUAL_CONSUMER_REQUIRED`: project image generation 전에 아래 네 값을 구체적으로 기록한다.

```yaml
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
consumer_surface:
primary_use:
validation:
```

유효 소비처:

- `GAME_RUNTIME`: 실제 gameplay scene, character sprite, environment, HUD, VFX, item icon 등 게임이 직접 소비한다.
- `PLANNED_GAME_SURFACE`: 아직 구현 전이어도 실제 게임에 들어갈 구체적 screen/scene/asset slot을 검증하는 목업이다.
- `PLAYER_FACING_EXPLANATORY`: 튜토리얼, 도감, 인게임 도움말, 세력 관계 UI처럼 플레이어가 게임 안에서 직접 소비하는 설명 visual이다.
- `PRODUCT_DISTRIBUTION`: store capsule, key art, app icon, trailer thumbnail, press kit처럼 판매·배포·홍보 경로가 실제 소비한다.

다음만 존재하면 invalid consumer다.

```text
DOCUMENTATION_DECORATION
AI_EXPLANATION_ONLY
CHECKLIST_DECORATION
UNNAMED_FUTURE_USE
```

invalid consumer뿐이면 `DO_NOT_GENERATE`다. 필요한 정보 자체는 `TEXT_TABLE_FLOW_DB_FIRST`로 계속 만든다.

## 1. Visual Requirement Gate

프로젝트용 이미지·목업을 만들기 전에 `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`에서 필요성·Delete Test·재사용 후보·역할·우선순위·제작 방식을 먼저 **선정**한다.

- 프로젝트 자산 후보는 가능한 한 `requirement_id`를 가진다.
- `GENERATE_EXPLORATION` 또는 승인된 `CREATE_CUSTOM` 판정을 이미지 생성 입력으로 사용한다.
- `GENERATE_EXPLORATION`도 `ACTUAL_CONSUMER_REQUIRED`를 우회하지 않는다. 실제 planned game surface/asset slot을 검증하는 exploration은 허용하지만 독립 설명용 시트 생성은 기본적으로 허용하지 않는다.
- `DEFER / CUT / REUSE_SYSTEM / REUSE_PROJECT / ADAPT_EXISTING / SOURCE_EXISTING`을 이미지 생성으로 임의 변환하지 않는다.
- 프로젝트 전체·화면군·캐릭터군을 다룰 때도 “있으면 좋을 것”이라는 이유만으로 선정되지 않은 자산을 자동 추가하지 않는다.
- `REFERENCE_ONLY`는 외부/기존 reference 활용을 포함할 수 있으나 새 생성 이미지가 자동으로 필요한 상태가 아니다.
- 사용자가 현재 대화에서 특정 프로젝트 이미지 한 장을 요청한 사실은 현재 requirement의 입력이 될 수 있지만, 프로젝트 자산으로 만들 때는 실제 consumer를 기록한다. 지속 자산 목록·`ASSET_MANIFEST.yml`·승인 상태를 자동 생성하지 않는다.

이 Gate는 **무엇을 만들 가치가 있는가**를 결정한다. 실제 생성 시점은 아래 Conversation Gate가 별도로 소유한다.

## 2. Image Conversation Approval Gate

프로젝트 이미지 생성·편집은 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`를 적용한다. 사용자가 current turn에서 실제 이미지 출력을 명시했는지, AI가 검토 중 Visual Need를 먼저 제안했는지를 구분한다.

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ PROJECT_REVIEW_COMPLETE
→ ACTUAL_CONSUMER_REQUIRED
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ current approved visual anchor resolution
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

사용자가 `이미지 만들어줘`, `그려줘`, `이 Brief대로 생성해`, `이 이미지를 편집해줘`처럼 current output을 명시한 경우 별도 장문 이미지 작업지시문이나 다음 turn의 중복 승인을 요구하지 않는다. `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`가 다음을 판정한다.

- usable current approved visual anchor가 있으면 실제 preview/source readback 뒤 사용자에게 surface하고 해당 방향으로 요청 deliverable 1건을 만든다.
- usable anchor가 없으면 final production을 추측하지 않고 사용자가 1안을 고를 concept comparison deliverable 1건을 만든다.
- comparison board는 `GENERATED_EXPLORATION`이며 production/runtime asset이 아니다.
- 사용자 선택 뒤 selected direction은 clean standalone anchor로 제작·승인·readback한 뒤 후속 production에 사용한다.

사용자가 current turn에서 이미지 출력을 명시하지 않았고 AI가 필요성을 먼저 발견한 경우 기존 two-turn barrier를 유지한다.

```text
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
→ PROJECT_REVIEW_COMPLETE
→ Visual Need / current Project canon / actual consumer
→ text brief
→ TEXT_BRIEF_STOP_REQUIRED

[다음 사용자 메시지]

→ NEXT_USER_EXPLICIT_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

`NO_AUTOMATIC_IMAGE_CHAIN`을 두 경로 모두에 적용한다.

- 한 authority 뒤 기본 생성은 이미지·편집·comparison deliverable 1건이다.
- 생성 직후 다음 포즈·캐릭터·화면·분해 에셋·재합성을 자동 연속 실행하지 않는다.
- 기존 승인 이미지를 Notion에 배치·링크·readback하는 작업은 새 이미지 생성이 아니므로 generation checkpoint를 만들지 않는다.
- 생성 성공은 `APPROVED_CANDIDATE`, `PROJECT_ASSET_APPROVED`, runtime 적용을 뜻하지 않는다.
- host/system 정책이 더 엄격하거나 다른 호출 순서를 강제하면 `HOST_PLATFORM_PRECEDENCE`를 따른다.

## 3. 프로젝트 Visual continuity

Project-scoped visual work는 `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`를 적용한다.

```text
latest user decision
→ exact Project relation
→ current project canon / Decision
→ APPROVED_VISUAL_REFERENCE
→ Screen / Flow / System when relevant
→ Keep / Avoid / Do Not Drift
→ image conversation gate
```

프로젝트가 불명확하거나 승인 방향이 없으면 다른 프로젝트의 자산을 빌려 추정하지 않고 `BLOCKED_UNVERIFIED` 또는 `MISSING_CANON`으로 둔다.

identity-preserving 편집에서는 얼굴 구조, 헤어, 의상, 장비, 팔레트, 실루엣, 카메라, 광원, UI family 등 요청하지 않은 속성을 hard constraint로 보존한다.

## 4. 생성 목적과 상태

### 4.1 기획 중 시각화

기획 중 생성 이미지는 **실제 planned game surface 또는 실제 제품 visual slot을 검증할 때만** 사용한다. 제작자·AI용 기본 정보 설명은 이 mode로 보내지 않는다.

대표 산출물:

- 실제 gameplay 화면에 들어갈 UI·카드·상점·전투·대화 screen mockup
- 실제 게임 캐릭터·환경·오브젝트의 visual identity candidate
- `PLAYER_FACING_EXPLANATORY`인 튜토리얼·도감·인게임 관계 UI mockup
- Vertical Slice에 들어갈 대표 scene/composition 가설
- 실제 store/product consumer가 예정된 key visual의 방향 가설

다음은 기본적으로 이미지 생성하지 않는다.

- 시스템 설명만을 위한 이미지 시트
- 세계관·세력 관계를 제작자/AI에게 설명하기 위한 포스터
- 제작 체크리스트를 그림으로 옮긴 시트
- 구조화 문서로 충분한 캐릭터 설정 설명판

이 정보들은 `PRODUCTION_INFORMATION`으로 유지하고 `TEXT_TABLE_FLOW_DB_FIRST`를 적용한다. 생성된 실제 surface mockup의 상태는 `GENERATED_EXPLORATION`이며 제품 자산으로 자동 승격하지 않는다.

### 4.2 기획 종료 후 실사용 후보

기획 승인 뒤 Demo-First Vertical Slice·게임 runtime·소개·상점·마케팅의 **명시된 actual consumer**에 사용할 수 있는 후보를 만든다.

대표 산출물:

- 키아트·캡슐·배너·썸네일 후보 — `PRODUCT_DISTRIBUTION`
- 캐릭터 gameplay representation, portrait, 표정·포즈·상태 세트 — 실제 screen/scene consumer가 있을 때
- UI 고도화 목업과 실제 화면 합성 — `PLANNED_GAME_SURFACE` 또는 `GAME_RUNTIME`
- 카드·장비·스킬 icon/visual — 실제 게임 UI consumer가 있을 때
- 튜토리얼·도감·인게임 도움말 visual — `PLAYER_FACING_EXPLANATORY`
- 상점·트레일러·프레스킷 시각 후보 — 실제 배포 경로가 있을 때

이 단계도 `APPROVED_CANDIDATE`일 수 있으며 권리·실제 화면·규격·구현·후처리 검증 전에는 `PROJECT_ASSET_APPROVED`가 아니다.

### 4.3 상태 흐름

```text
PLANNED
→ GENERATED_EXPLORATION
→ IN_REVIEW
├─ REVISION_REQUIRED → 다시 brief/승인 checkpoint → 재생성·편집
├─ REJECTED
└─ APPROVED_CANDIDATE
   → 실제 화면·규격·권리·후처리·구현 검수
   → PROJECT_ASSET_APPROVED
   → APPLIED_AND_RUNTIME_VERIFIED
```

## 5. Notion 전달과 Human / AI 분리

실제 이미지·목업·다이어그램이 프로젝트용으로 승인되면 `APPROVED_VISUAL_NOTION_DELIVERY_REQUIRED`를 적용한다.

```text
actual visual exists
→ user/project approval
→ exact Project Visual Bible 또는 project-scoped Asset record에 durable attach
→ Approved + intended use + Project 기록
→ destination readback
→ 필요하면 Human Home의 HERO / PRIMARY visual anchor로 노출
```

Human-facing surface는 사람이 판단하는 데 필요한 것을 보여준다.

- 실제 이미지/Preview
- Name
- Usage
- Style / visual meaning
- Approved state
- Reuse meaning

AI/System surface는 다음을 보존한다.

- Asset ID
- Version
- Prompt
- AI Note
- Source / provenance
- Rights / License
- Hash
- Implementation Path
- raw placement/readback evidence

Prompt·Hash·AI Note가 필요하다는 이유로 Human Home을 AI context dump로 만들지 않는다. 반대로 시스템·세계관·관계·체크리스트 같은 `PRODUCTION_INFORMATION`을 이미지 파일 안에 가둬 검색·수정 불가능하게 만들지도 않는다.

## 6. 프로젝트 로컬 보존소와 자산 승격

프로젝트별 로컬 이미지 보존·Godot 연결의 공용 책임 원본은 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`다.

보존소가 구성된 프로젝트에서는 다음 경계를 사용한다.

```text
GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE
→ .asset-vault/library/
→ sync
→ assets/_vault_local/
→ PROJECT_ASSET_APPROVED
→ promote
→ assets/<approved-path>/
→ ASSET_MANIFEST.yml·권리/출처·정본 갱신
→ tracked Scene/Resource 연결
→ APPLIED_AND_RUNTIME_VERIFIED
```

- 승인 전 이미지는 local candidate로 보존할 수 있지만 tracked 제품 자산으로 자동 승격하지 않는다.
- `PROJECT_ASSET_APPROVED`만 promote한다.
- tracked Scene/Resource는 `res://assets/_vault_local/...`을 장기 참조하지 않는다.
- 사용자가 후보를 삭제하면 stale context나 download가 자동 부활시키지 않는다.
- 로컬 vault를 확인하지 못한 원격 작업자는 `VAULT_LOCAL_STATE_UNVERIFIED`를 유지한다.

## 7. Primary Use Gate → Reusable Visual Harvest Gate

이미지 작업의 기본 순서는 **`proposal → user approval → production → primary use → harvest review`**다.

```text
기존 승인 자산 / current Project Visual Bible
→ ACTUAL_CONSUMER_REQUIRED
→ image conversation gate
→ 이미지 제작
→ Primary Use Gate
→ primary-use success
→ Reusable Visual Harvest Gate
→ 필요한 요소만 구조화·레이어화·semantic rebuild
→ 다음 작업에서 재사용·변형
```

재사용성을 이유로 `title-specific identity`, 감정, 정보 위계, 구도를 약화시키지 않는다. `primary-use success`와 `reuse promotion`은 별도 판정이다.

Harvest 후보:

- `REUSE_AS_IS`
- `VARIANT_SEED`
- `STRUCTURE_PATTERN`
- `STYLE_DNA`
- `REBUILD_FOR_REUSE`
- `ONE_OFF_KEEP`
- `REJECT_REUSE`

분리·재구축 방법:

```text
SOURCE_LAYER
→ MASK_CUTOUT
→ MANUAL_OR_SEMANTIC_REBUILD
→ DERIVED_GENERATIVE_RECOVERY
```

`SOURCE_LAYER`는 원래 독립 source를 사용하고, `MASK_CUTOUT`은 관측된 픽셀만 분리한다. `MANUAL_OR_SEMANTIC_REBUILD`는 UX/UI처럼 상태·확장·현지화·접근성이 필요한 요소에 우선한다. `DERIVED_GENERATIVE_RECOVERY`는 원본에서 보이지 않은 영역을 새로 만든 derived generated pixels이므로 관측 사실과 분리한다.

Harvest는 `PROJECT_ASSET_APPROVED`, tracked asset, rights 또는 Godot runtime proof를 자동 생성하지 않는다.

## 8. 이미지 검수 계약

모든 이미지·목업은 다음을 검사한다.

1. 기획·세계관·캐릭터·시스템 정본 일치성
2. `ACTUAL_CONSUMER_REQUIRED`의 consumer kind/surface/primary use/validation이 실제인지
3. 핵심 경험·세일즈포인트 전달력
4. 실제 화면 크기·HUD·VFX·배경 위 가독성
5. 구현 가능성·제작 비용·기술 규격
6. 다른 자산과의 형태·색·재질·광원 일관성
7. 재사용성·편집 가능성·현지화 가능성
8. 손·관절·무기·문자·로고·원근·광원 오류
9. 특정 상업 IP·식별 가능한 표현·작가 스타일과의 과도한 유사성
10. 원본·레퍼런스·모델·서비스·버전·프롬프트·생성일 provenance
11. 승인자·사용처·Notion Asset/Visual과 repository tracked path 연결
12. 프로젝트 자산 후보라면 `requirement_id`와 선정 근거
13. 생성 전/후 conversation gate 준수
14. 관련 `coverage_item_id / coverage_status`와 실제 source 또는 `requirement_id` 연결
15. `state_family_status`가 consumer가 요구하는 상태를 빠뜨리지 않았는지
16. 실제 target resolution/aspect에서 crop·UI·VFX와 함께 판독 가능한지
17. engine consumption 조건(import/filter/mipmap/compression/atlas/slicing/pivot 등)이 필요한 자산에서 정의됐는지
18. 중요한 상태가 색 하나에만 의존하지 않고 필요한 semantic redundancy를 갖는지
19. `PLATFORM_REQUIRED`이면 release 시점의 current official spec/rule을 재조회했는지
20. `PRODUCTION_INFORMATION`을 이미지 하나로 대체해 정보 정본이 손실되지 않았는지
21. explicit current-turn request이면 current approved visual anchor를 실제 readback·surface했는지, 없으면 concept comparison으로 방향을 먼저 선택했는지
22. 후속 production이 `STYLE_CONTINUITY_REVIEW_REQUIRED`와 `FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED`를 통과했는지

## 9. 참조 기반 독립 제작

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다.

```yaml
reference_sources:
reference_brief:
forbidden_expression:
final_asset_record:
reference_similarity_status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

- `reference_brief`에는 프로젝트 목적·정보 구조·일반 형태·재질·광원·가독성 원리만 남긴다.
- `forbidden_expression`에는 식별 가능한 캐릭터, 실루엣·의상·소품 조합, 구도, 로고, UI skin, icon set, 특정 작가 스타일 모사를 기록한다.
- 참조 원본은 제품 build·store·trailer·marketing package에 포함하지 않는다.
- 최종 생성물은 별도 `final_asset_record`와 provenance를 가진다.
- `reference_similarity_status`가 `PASS`가 아니거나 입력 권리·약관이 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`다.

AI 재생성, image-to-image, 부분 편집 또는 overpaint는 원출처·입력 권리·유사성 검토를 면제하지 않는다.

## 10. 승인·정본·동기화

승인된 이미지 Decision은 같은 승인 단위에서 필요한 owner만 갱신한다.

```text
CURRENT_CONFIRMED_DECISIONS
→ 아트·UI·세계관·캐릭터·시스템 structured owner
→ GitHub tracking/main when repository meaning changes
→ exact Project Notion Home / Visual Bible / Asset
→ Asset License / provenance / rights records when applicable
→ repository tracked asset / ASSET_MANIFEST.yml when promoted
→ runtime implementation and validation when required
→ destination readback
```

Google Sheets는 `COMPATIBILITY_ONLY` migration source다. Sheet-only unique material이 실제 migration scope에 있을 때만 읽고, 신규 승인 결과를 Sheet에 동기화하는 것을 정상 완료 조건으로 만들지 않는다.

Notion approval, asset upload, tracked file, runtime application은 서로 다른 상태다. `PRODUCTION_INFORMATION`은 해당 프로젝트의 문서·DB·structured canon에 유지하고 이미지 승인 lifecycle과 혼합하지 않는다.

## 11. 적대적 검토

이미지 작업 전체를 다음 실패 가정으로 다시 공격한다.

- Visual Asset Coverage Preflight를 생략해 버튼 상태, enemy telegraph, feedback, input prompt, platform asset 같은 인접 필수 범위가 누락됐는가
- 시스템 설명·세계관·관계도·제작 체크리스트 같은 기본 `PRODUCTION_INFORMATION`이 이미지 제한 때문에 생성되지 않았는가
- 반대로 `PRODUCTION_INFORMATION`을 검색·수정 가능한 text/table/flow/db 대신 설명용 생성 이미지로 대체했는가
- `ACTUAL_CONSUMER_REQUIRED`가 비어 있는데도 설명용 시트·포스터·관계 이미지를 생성했는가
- `PLAYER_FACING_EXPLANATORY`와 제작자/AI용 설명 자료를 혼동했는가
- `PRODUCT_DISTRIBUTION` 소비처가 없는 marketing-style visual을 관성적으로 만들었는가
- Visual Asset Coverage Preflight를 second asset canon이나 자동 production queue로 만들었는가
- `NOT_APPLICABLE`을 허용하지 않아 장르·단계와 무관한 asset scope가 폭증했는가
- `STATE_FAMILY_COMPLETENESS` 없이 대표 이미지 한 장만으로 component 완성을 주장했는가
- `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`를 어기고 gap 발견 뒤 사용자 승인 없는 image chain/batch를 만들었는가
- Visual Requirement Gate에서 선정되지 않은 자산을 관성적으로 대량 생성했는가
- `CURRENT_TURN_EXPLICIT_IMAGE_REQUEST`인데 current approved anchor resolution·actual preview readback·found/reuse 또는 concept comparison 분기를 생략하고 blind final production으로 갔는가
- `ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE`인데 `TEXT_BRIEF_STOP_REQUIRED`와 다음-turn 승인을 생략했는가
- 승인 하나로 여러 이미지·포즈·컴포넌트를 자동 연쇄 생성했는가
- concept comparison board나 panel을 final master·runtime asset으로 사용했는가
- 선택된 방향을 standalone anchor로 잠그지 않고 panel crop·기억만으로 후속 자산을 만들었는가
- 후속 이미지가 current Flow/Screen에 없는 버튼·상태·시스템을 새 요구사항처럼 발명했는가
- 모든 layer를 같은 렌더링 밀도로 강제해 UI·VFX·marketing의 역할이 손상됐거나, 반대로 project global grammar가 사라졌는가
- 승인 전 이미지가 final/production asset처럼 사용됐는가
- 승인 전 vault 후보가 tracked Repo 자산으로 자동 승격됐는가
- tracked Scene/Resource가 local-only vault를 참조하는가
- 사용자가 제거한 후보를 stale 문맥이 다시 살렸는가
- 기획 변경 뒤 이미지·목업이 stale 상태인가
- 이미지 Decision이 GitHub/Notion/Asset owner 일부에만 남았는가
- Google Sheets·Figma·HTML·retired visual tool을 active authority로 되살렸는가
- 원출처·라이선스·유사성 검토가 빠졌는가
- 실제 화면 검수 없이 예쁜 원화만 승인했는가
- target resolution/aspect 또는 Godot import 소비 조건을 확인하지 않아 실제 적용에서 재작업이 발생하는가
- color-only cue 때문에 중요한 상태·위험·선택을 구별하기 어려운가
- store/platform asset이 오래된 규격·콘텐츠 규칙을 따르는가
- concept art/reference를 gameplay screenshot/runtime proof로 오인했는가
- Primary Use 전에 재사용 편의를 위해 본 화면 품질·정체성을 희생했는가
- `ONE_OFF_KEEP`가 정상인데도 모든 이미지를 강제 component/layer library로 승격했는가
- `DERIVED_GENERATIVE_RECOVERY` 픽셀을 원본의 관측 사실로 기록했는가
- Harvest를 `PROJECT_ASSET_APPROVED` 또는 runtime proof로 오해했는가

차단 Finding은 `MUST_FIX`, 권리·출처·약관·유사성 판정 불가는 `RELEASE_BLOCKED_UNVERIFIED`로 기록한다.

## 12. Implementation Reality Gate

이 정책은 정적 계약이다. 실제 이미지 생성 도구/모델이 이 대화 Gate를 따랐다는 증거는 **실제 작업 기록**이 있어야 한다.

```text
STATIC_POLICY_PRESENT
!= MODEL_BEHAVIOR_VERIFIED
!= IMAGE_QUALITY_PASS
!= NOTION_DELIVERY_PASS
!= RUNTIME_VISUAL_PASS
```

실행 플랫폼의 더 높은 시스템·안전·제품 정책과 충돌하는 경우 Base 계약이 그 상위 정책을 override한다고 주장하지 않는다. 가능한 범위에서는 current-turn explicit request와 assistant-initiated Visual Need를 먼저 분류하고, 전자는 visual anchor pipeline의 one-output route로, 후자는 text brief two-turn route로 실행한다. 실제 tool call은 적용 가능한 상위 정책과 현재 사용자 승인 범위 안에서 수행한다. 상위 정책 때문에 해당 route를 그대로 적용할 수 없으면 `HOST_POLICY_OVERRIDE`, `BLOCKED_POLICY_CONFLICT` 또는 해당 실행 환경의 evidence ceiling을 기록하며 정적 테스트 통과를 실제 모델 행동 PASS로 승격하지 않는다.