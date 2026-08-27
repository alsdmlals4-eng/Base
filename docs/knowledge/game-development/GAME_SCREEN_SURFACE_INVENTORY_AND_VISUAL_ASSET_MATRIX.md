# 게임 화면 Surface 인벤토리와 Visual Asset Matrix

## 0. 목적과 권위 경계

이 문서는 게임 제작의 필수 이미지·시각 표현을 **자산 종류 목록이 아니라 플레이어가 실제로 거치는 화면 전체**에서 역산하기 위한 공용 companion contract다.

```text
SUBORDINATE_TO_GAME_VISUAL_ASSET_COVERAGE_OWNER
SCREEN_SURFACE_INVENTORY_FIRST
SCREEN_LEVEL_COMPOSITION_REQUIRED
SCREEN_INVENTORY_HANDOFF_ONLY
COVERAGE_CHECK_ONLY
NOT_A_SECOND_ASSET_CANON
ACTUAL_CONSUMER_REQUIRED
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

이 문서는 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`를 대체하지 않는 subordinate preflight contract다. 최종 visual coverage 상태와 완료 판정의 단일 canonical owner는 기존 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`다.

- 이 문서: 목표 흐름의 모든 화면·오버레이·전환을 먼저 찾고 화면별 시각 소비처를 분해한다.
- `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`: 캐릭터, 환경, UI, VFX, 상태군, 기술 조건 등 자산 종류별 누락을 교차 검사한다.
- `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`: 실제로 만들 가치, 우선순위, 재사용과 제작 방식을 결정한다.
- `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`: 생성·편집·검수·명시적 승인 경계를 소유한다.
- 프로젝트 Notion: 사람이 읽고 비교·승인하는 화면·Flow·Visual·Asset 정본을 소유한다.
- 프로젝트 GitHub: Markdown·JSON·게임 데이터·씬·리소스·테스트와 runtime 사실을 소유한다.
- Godot 실행 증거: 실제 배치, 입력, 해상도, 상태 전환, 가독성 사실을 소유한다.

따라서 이 문서의 row는 기존 프로젝트 정본, requirement, asset record, scene, evidence를 링크한다. 독립적인 두 번째 GDD·Asset Manifest를 만들지 않는다.

## 1. 핵심 교정: 화면부터 찾는다

기존처럼 `캐릭터 / 배경 / 아이콘 / UI / VFX`부터 세면 개별 자산은 많이 있어도 메인 화면, 전투 준비, 결과·보상, 설정 같은 **완결 화면**이 통째로 빠질 수 있다.

모든 project-wide 또는 vertical-slice visual audit는 아래 순서를 사용한다.

```text
current Project canon / target build / target player flow
→ SCREEN_SURFACE_INVENTORY_FIRST
→ 모든 적용 가능한 screen / overlay / transition / error surface 열거
→ 각 화면의 player goal / player question / entry / exit 확인
→ screen-level composition과 identity requirement 확인
→ 화면별 component / state / variant / feedback / technical need 분해
→ existing approved asset / current implementation / reuse 조사
→ SCREEN_TO_ASSET_COVERAGE_MATRIX 작성
→ 자산 종류별 GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md 교차 검사
→ gap을 existing / requirement / decision / defer에 연결
→ 필요한 경우에만 기존 Visual Requirement Gate와 이미지 승인 Gate 적용
→ implementation / runtime / readback 검증
```

규칙:

1. 목표 범위에 포함되는 화면은 row로 기록한다.
2. 적용되지 않는 화면도 조용히 삭제하지 않고 `NOT_APPLICABLE`과 이유를 기록한다.
3. 메인·타이틀, 실제 gameplay, 결과·보상, 일시정지·설정은 존재 여부를 반드시 명시한다.
4. 화면이 여러 상태를 공유해도 진입 목적, 정보 위계, 조작, 결과가 다르면 별도 screen surface 또는 state row로 분리한다.
5. 팝업·작성 overlay·컷인처럼 기존 scene 위에 표시돼도 플레이어 판단과 입력을 바꾸면 독립 surface로 기록한다.
6. loading, empty, error, offline, permission, save conflict처럼 정상 흐름 밖 화면도 실제 발생 가능하면 누락하지 않는다.

## 2. 화면 자체도 필수 시각 산출물이다

`SCREEN_LEVEL_COMPOSITION_REQUIRED`:

실제 또는 계획된 player-facing surface가 있으면 해당 화면은 최소한 다음 중 하나의 검증 가능한 전체 화면 표현을 가져야 한다.

- 승인된 `SCREEN_DESIGN_REFERENCE`
- 목표 해상도의 wireframe 또는 high-fidelity mockup
- 실제 Godot scene capture
- 실행 가능한 prototype capture
- 이미 검증된 기존 화면을 재사용한다는 evidence

이 산출물은 다음을 함께 판단할 수 있어야 한다.

- 무엇을 가장 먼저 봐야 하는가
- 어떤 결정을 내려야 하는가
- 어디를 조작하는가
- 현재 상태와 결과를 어떻게 이해하는가
- 배경, 캐릭터, UI, 텍스트, VFX가 서로 가리지 않는가
- 목표 종횡비와 입력 방식에서 읽히는가

캐릭터·버튼·아이콘 파일이 모두 존재하더라도 이를 조합한 화면의 정보 위계와 감정적 첫인상을 검증하지 못하면 screen coverage는 완료가 아니다.

### 2.1 화면 설계 이미지와 런타임 자산을 분리한다

```text
SCREEN_DESIGN_REFERENCE
→ 화면 전체의 구도, 정보 위계, 시선 흐름, 감정, 레이아웃을 승인하기 위한 visual reference

RUNTIME_COMPONENT_ASSET
→ 게임이 직접 불러오는 배경, 캐릭터, 아이콘, 프레임, 텍스처, sprite sheet, mask 등

PROCEDURAL_OR_ENGINE_RENDERED
→ Godot Control, Theme, StyleBox, Label, Line2D, Polygon2D, shader, particle, primitive drawing 등으로 구성

NO_NEW_IMAGE_FILE_REQUIRED
→ 필요한 시각 표현은 있으나 기존 자산·텍스트·SVG·Godot UI·shader·procedural drawing으로 충족되어 새 bitmap 생성이 불필요함
```

전체 화면 목업 한 장을 그대로 runtime UI로 사용하는 것은 명시적으로 의도된 경우를 제외하면 기본값이 아니다.

```text
SCREEN_DESIGN_REFERENCE
→ runtime layer decomposition
→ reusable component / text / data / control / effect 분리
→ actual consumer 연결
→ runtime capture와 reference 비교
```

이미지 안에 버튼 글자·수치·번역 문자열을 굳히지 않는다. 수정·localization·상태 변화가 필요한 정보는 가능한 한 실제 text/data/UI layer로 유지한다.

## 3. PLAYER_VISIBLE_SCREEN_FAMILIES

아래 family는 공용 후보군이다. 장르와 목표 build에 따라 적용 여부를 판정하되, 해당 family를 검토하지 않은 채 누락으로 남기지 않는다.

### `BOOT_SPLASH_LOADING`

- 앱 시작, publisher/engine splash가 실제로 필요한 경우
- 초기 loading, save/profile load, shader/content preparation
- loading progress 또는 응답 없음 방지 feedback

### `MAIN_TITLE_MENU`

- 메인/타이틀 화면
- 새 게임, 이어하기, 불러오기, 프로필 선택
- 설정, 접근성, 언어, 크레딧, 종료
- 버전, save 상태, 최근 기록처럼 실제로 필요한 정보
- 타이틀 로고, 배경, 메뉴 focus/selected/disabled 상태

### `NEW_GAME_PROFILE_SAVE_LOAD`

- 새 진행 생성
- 난이도·모드·슬롯·프로필 선택
- save/load 목록, overwrite, delete, conflict, corrupt/empty state

### `CHARACTER_BUILD_LOADOUT_SELECT`

- 캐릭터, 직업, 무공, 덱, 장비, 파티, 시작 보너스 선택
- 선택/비선택/잠금/조건 미충족/확정 상태
- 비교 정보와 최종 선택 결과

### `HUB_HOME_MAP_ROUTE`

- 허브·기지·홈
- 월드맵, 노드맵, 행로, 챕터, 스테이지 선택
- 현재 위치, 도달 가능, 잠김, 완료, 위험, 보상, 경로 연결

### `EXPLORATION_GAMEPLAY_CORE`

- 자유 이동, 탐색, 관리, 건설, 퍼즐, 조사 등 핵심 gameplay
- HUD, 목표, 상호작용, 위험, 선택, 진행도
- 정상/경고/실패/회복 상태

### `DIALOGUE_EVENT_STORY`

- 대화, 인터뷰, 사건 기록, 이벤트 선택
- 초상·표정·speaker·선택지·로그·skip/auto
- 컷신, chapter visual, player-facing 문서·증거

### `PREPARATION_BRIEFING_PARTY_EQUIPMENT`

- 전투·임무·구조 전 브리핑
- 목표, 적/위험 정보, 파티, 장비, 스킬, 자원, 출발 확인
- 준비 완료/미완료/경고/잠금 상태

### `BATTLE_COMBAT`

- 별도 전투장 또는 필드 전투
- 캐릭터·적·전장·HUD·행동 선택·순서·사거리·위험 예고
- 타기팅, 선택, cooldown, 피해, 회복, 사망, 승패 직전 상태

### `SPECIAL_ACTION_OVERLAY`

- 마법 작성, 조준, 퍼즐 입력, QTE, 합·절초·필살기·보스 phase 컷인
- 기존 화면 위 overlay라도 입력과 판단이 달라지면 별도 surface로 기록
- cancel/confirm/resource cost/invalid state 포함

### `RESULT_REWARD`

- 승리, 패배, 임무 결과, 전투 검토
- 획득 경험치·재화·아이템·평가·기록
- 보상 선택, 다음 단계, 재도전, 원래 장면 복귀
- zero reward, inventory full, reward pending 같은 예외 상태

### `PROGRESSION_UPGRADE_SHOP_CRAFT_REST`

- 성장, 강화, 스킬트리, 상점, 제작, 수리, 휴식, 정비
- 비용, 보유량, preview, before/after, 잠금, 실패/성공 feedback

### `CODEX_ARCHIVE_MANUAL_TUTORIAL_HELP`

- 도감, 기록 보관소, 괴이/무공/아이템 매뉴얼
- 튜토리얼, 도움말, 조작 안내, 용어 설명
- 검색, 분류, unread/new, locked/unknown, empty state

### `PAUSE_SETTINGS`

- 일시정지
- 오디오, 그래픽, 입력, 접근성, 언어, 저장/복귀/종료
- keyboard/gamepad/touch navigation focus
- 변경 적용, 되돌리기, 확인 dialog

### `FAILURE_RETRY_ENDING_CREDITS`

- game over, 실패 사유, 재시도, checkpoint 복귀
- ending, chapter complete, credits, post-game unlock

### `LOADING_TRANSITION_ERROR`

- scene transition, chapter transition, fade/cut/wipe
- loading, reconnect, offline, permission, update required
- empty, missing data, save conflict, unsupported input/device
- recoverable action과 안전한 exit

### `DEBUG_DEVELOPMENT_ONLY`

- collision, spawn, path, camera bounds, AI state, performance overlay
- player-facing production surface와 분리하며 release coverage로 승격하지 않는다.

## 4. SCREEN_TO_ASSET_COVERAGE_MATRIX

화면을 열거한 뒤 각 화면을 아래 구조로 분해한다. 프로젝트에 이미 동일한 DB·JSON·Markdown owner가 있으면 새 파일을 만들지 말고 기존 owner에 필드를 매핑한다.

```yaml
screen_id:
screen_family:
screen_name:
project_stage: CONCEPT | POC | VERTICAL_SLICE | PRODUCTION | RELEASE
priority: P0 | P1 | P2
flow_entry:
flow_exit:
player_goal:
player_question:
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY
consumer_surface:
screen_design_reference:
runtime_consumer:
  scene:
  nodes_or_components: []
visual_layers:
  composition_identity: []
  world_character_object: []
  ui_component_icon: []
  feedback_telegraph_vfx: []
  technical_texture_mask: []
state_families: []
variants: []
implementation_modes: []
existing_evidence: []
coverage_status: NOT_REVIEWED | NOT_APPLICABLE | COVERED_EXISTING | REQUIREMENT_LINKED | GAP_BLOCKING | GAP_NONBLOCKING | DEFERRED_BY_DECISION
requirement_links: []
validation:
  reference_readback:
  target_resolution:
  input_modes: []
  runtime_evidence:
notion_destination:
repository_destination:
blockers: []
note:
```

### 4.1 화면별 구성요소 분해

모든 화면은 필요한 범위에서 아래 층을 검사한다.

1. **Composition / Identity**
   - 화면 전체 배경·공간·프레이밍·visual hierarchy
   - 게임 로고·장면의 감정·대표 실루엣·첫인상
2. **World / Character / Object**
   - 캐릭터, 적, NPC, 환경, 장비, 아이템, 건물, 상호작용 물체
3. **UI Component / Icon / Typography**
   - panel, button, tab, slot, cursor, gauge, icon, text layer
4. **State / Variant**
   - normal, hover, pressed, focus, selected, disabled, locked, warning, complete
   - 방향, 등급, 진영, 장비, 피해, phase, language/input 변형
5. **Feedback / Telegraph / VFX**
   - 위험, 선택, 사거리, 공격 예고, 성공, 실패, 보상, 전환
6. **Technical Consumption**
   - resolution, aspect, crop, alpha, 9-patch, slicing, pivot, filter, mipmap, compression, atlas, mask, shader input

이 분해 뒤 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`의 자산 category와 `STATE_FAMILY_COMPLETENESS`를 교차 검사한다.

## 5. 제작 방식 판정

각 component는 아래 중 하나 이상으로 기록한다.

| 방식 | 의미 |
|---|---|
| `EXISTING_APPROVED` | 현재 프로젝트의 승인 자산·화면으로 충족 |
| `REUSE_PROJECT` | 같은 프로젝트의 기존 component를 재사용·변형 |
| `REUSE_BASE_REFERENCE` | Base의 공용 pattern/reference를 프로젝트 정체성에 맞게 ADAPT |
| `GODOT_UI` | Control, Theme, StyleBox, container, Label 등으로 구현 |
| `TEXT_LAYER` | 번역·데이터 변경 가능한 실제 text layer |
| `SVG_VECTOR` | 해상도 독립 icon/shape/vector |
| `RASTER_IMAGE` | 배경, 초상, texture 등 bitmap이 실제로 필요 |
| `SPRITE_SHEET` | animation/state frame 소비처가 명확함 |
| `SHADER` | glow, outline, mask, distortion, palette, transition 등 |
| `PROCEDURAL_DRAW` | Line2D, Polygon2D, primitive, graph/map/path 등 |
| `SCREEN_DESIGN_REFERENCE` | 전체 화면 설계·승인용 reference |
| `DO_NOT_GENERATE` | 실제 소비처가 없거나 기존 방식으로 충분함 |
| `NO_NEW_IMAGE_FILE_REQUIRED` | 시각 표현은 필수지만 새 image file은 불필요함 |

`NO_NEW_IMAGE_FILE_REQUIRED`는 “화면이 필요 없다”는 뜻이 아니다. 화면 설계와 구현 검증은 그대로 필요하지만 불필요한 bitmap 생산만 막는다.

## 6. 우선순위

### P0 — Must-play flow

첫 실행부터 핵심 loop와 결과까지 플레이를 막는 화면.

```text
boot/title
→ new/continue/select
→ hub/map/preparation
→ core gameplay/battle
→ result/reward
→ next action 또는 safe exit
```

Vertical Slice에서는 P0 화면의 player-facing placeholder, 누락 상태, 깨진 전환을 허용하지 않는다.

### P1 — 반복과 유지

성장·상점·장비·도감·튜토리얼·설정·save/load처럼 반복 플레이와 이해를 지탱하는 화면.

### P2 — 확장과 출시

후반 content, 추가 mode, ending variation, marketing/platform surface. 현재 목표에 필요하지 않으면 명시적으로 defer한다.

## 7. Notion과 GitHub 반영

### Notion — 사람이 읽는 정본

프로젝트의 기존 구조를 우선하며, 필요한 경우 다음을 연결한다.

- Home 상단: 핵심 화면·Flow·대표 visual과 현재 목표 build
- Screen/Flow: 전체 화면 인벤토리, 진입·이탈·플레이어 목표
- Visual Bible: 화면 family, composition, hierarchy, Keep/Avoid
- Asset Library: 승인 asset, source, 상태, consumer, 화면 relation
- Production/Handoff: 다음 화면·asset queue와 승인 경계

### GitHub — 구조·구현 정본

프로젝트의 기존 경로·schema를 우선한다.

- Markdown/JSON screen inventory
- scene/resource/runtime consumer
- requirement/asset manifest link
- test와 runtime capture/evidence
- Codex가 구현할 exact path와 acceptance

Notion의 시각 방향과 GitHub의 runtime 사실이 충돌하면 완료가 아니다. 양쪽 readback을 남기고 current authority에 따라 교정한다.

## 8. 이미지 생성 경계

화면 인벤토리와 gap 발견은 이미지 생성 권한이 아니다.

```text
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

- 이 audit는 화면과 requirement를 정리한다.
- 사용자 current turn이 실제 이미지 생성·편집을 명시하지 않았다면 이미지 도구를 호출하지 않는다.
- 한 화면 누락을 발견해도 다른 화면·상태·variant를 자동 연속 생성하지 않는다.
- 실제 이미지가 필요한 row만 `ACTUAL_CONSUMER_REQUIRED`와 기존 approval gate로 보낸다.
- 전체 화면 reference 생성과 runtime component 생성은 각각 독립 deliverable·brief·approval이다.

## 9. 적대적 검토

다음 중 하나라도 발생하면 교정한다.

1. 자산 category는 많지만 목표 flow의 화면 목록이 없다.
2. 메인/타이틀 화면, 준비, 결과·보상, pause/settings 중 하나가 이유 없이 빠졌다.
3. 전체 화면 목업을 runtime asset 한 장으로 오인했다.
4. 화면 설계가 필요하다는 사실을 모든 component의 신규 bitmap 생성으로 확대했다.
5. 실제 consumer가 없는 설명용 sheet를 runtime backlog에 넣었다.
6. 화면 row가 player goal·player question·entry·exit를 설명하지 못한다.
7. normal 화면만 있고 loading, empty, error, disabled, locked, failure 상태가 없다.
8. 캐릭터·UI·VFX가 개별로 승인됐지만 한 화면에서 겹치고 읽히지 않는다.
9. Notion visual과 GitHub/Godot runtime가 서로 다른 화면을 가리킨다.
10. screen coverage가 두 번째 GDD·Asset Manifest가 됐다.
11. 이미지 생성 승인 없이 gap을 자동 생산 queue로 실행했다.
12. target resolution, aspect, input, localization에서 화면 검증을 하지 않았다.

## 10. 완료 조건

`SCREEN_INVENTORY_HANDOFF_READY`는 다음을 모두 만족할 때만 사용한다.

```text
목표 build의 모든 relevant screen / overlay / transition이 row로 존재
→ 적용되지 않는 family는 NOT_APPLICABLE + reason
→ 각 screen에 player goal / question / entry / exit가 있음
→ SCREEN_LEVEL_COMPOSITION_REQUIRED 충족
→ screen design reference와 runtime component가 구분됨
→ component / state / variant / feedback / technical need가 분해됨
→ implementation mode와 actual consumer가 연결됨
→ asset category/state-family 교차 검사 완료
→ P0 blocking gap 0 또는 명시적 Decision/Blocker
→ Notion human-facing canon readback
→ GitHub structured/runtime evidence readback
```

이 완료는 모든 이미지가 생성됐다는 뜻이 아니다. 실제 이미지가 필요한 항목은 별도의 생성·승인·promotion·Godot runtime 검증을 통과해야 한다.

`SCREEN_INVENTORY_HANDOFF_READY`는 화면 row와 화면별 matrix가 canonical coverage owner에 전달될 준비가 됐다는 뜻이다. 최종 coverage status, Visual Requirement Gate 전달, 이미지 승인, runtime QA와 READBACK은 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`와 기존 owner가 판정한다.
