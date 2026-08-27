# GPT Work — 게임 전체 화면·필수 이미지 전수조사·교정 실행 지시문

@Superpowers @GitHub @Notion

현재 이 채팅이 연결된 프로젝트를 대상으로, **목표 빌드에서 플레이어가 실제로 보게 되는 모든 화면과 그 화면을 구성하는 필수 시각 요소**를 전수조사하고 누락·충돌·중복을 실제 정본에 교정해.

이 작업은 단순 이미지 종류 목록 작성이나 제안서 작성이 아니다.

```text
목표 플레이 흐름의 전체 화면을 먼저 확정
→ 화면별 구성요소·상태·변형·피드백·기술 소비처 분해
→ 기존 승인 자산·구현·재사용 가능 요소 조사
→ 누락과 잘못된 분류를 Notion/GitHub 정본에 실제 교정
→ 이미지 제작 queue와 Codex 구현 handoff를 분리
→ readback과 남은 blocking gap 재검사
```

## 0. 최상위 기준

다음 두 Base 문서를 latest completed `main`에서 fresh-read하고 적용해.

- `docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`
- `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`

핵심 규칙은 다음이야.

```text
SCREEN_SURFACE_INVENTORY_FIRST
SCREEN_LEVEL_COMPOSITION_REQUIRED
ACTUAL_CONSUMER_REQUIRED
STATE_FAMILY_COMPLETENESS
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

필수 이미지를 `캐릭터 / 배경 / 아이콘 / UI / VFX` 같은 자산 category부터 세지 마.

먼저 **메인/타이틀 화면부터 핵심 gameplay, 결과·보상, 설정, 실패·엔딩까지 실제 화면 전체**를 찾고, 그다음 각 화면을 구성하는 자산과 상태를 역산해.

## 1. Fresh-read와 현재 상태 재구성

과거 채팅이나 memory를 current truth로 가정하지 마.

먼저 가능한 연결 도구를 직접 사용해 다음을 확인해.

1. Base latest completed `main`
2. 현재 프로젝트 GitHub latest completed `main`
3. 현재 프로젝트의 모든 open/draft PR과 같은 Goal의 최근 merged PR
4. active `AGENTS.md`
5. `ACTIVE_CONTEXT`, `CURRENT_CONFIRMED_DECISIONS`, 승인된 Decision과 handoff
6. 프로젝트 Notion Home, Direction/GDD, Screen/Flow, Visual Bible, Asset Library, Production/Handoff
7. 실제 Godot scene/resource/data와 현재 runtime consumer
8. legacy Google Sheets가 있으면 미이관 고유 정보만 migration compatibility 자료로 확인

저장소·Notion에서 직접 확인 가능한 사실을 사용자에게 다시 질문하지 마.

충돌 시 권위는 다음 순서를 따른다.

```text
최신 사용자 결정
→ 프로젝트 AGENTS / Active Context / 승인 Decision
→ 프로젝트 Notion의 사람용 기획·시각 정본
→ 프로젝트 GitHub의 구조·데이터·코드·씬·리소스·테스트·runtime 사실
→ Base 공용 계약
→ 과거 채팅·memory·초안·외부 reference
```

다른 open PR은 read-only로 유지하고, current 작업은 latest completed `main`에서 별도 안전 변경으로 진행해.

## 2. 목표 빌드와 플레이 흐름 고정

현재 프로젝트의 전체 출시 범위를 무조건 완성하려 하지 말고, 먼저 다음을 구분해.

- 현재 목표 build
- 현재 vertical slice 또는 다음 playable milestone
- first-time player가 처음 실행해서 핵심 loop를 완료하고 결과를 받기까지의 must-play flow
- 반복 플레이에 필요한 support flow
- 후속 production/release flow

각 화면은 `P0 / P1 / P2`로 분류해.

```text
P0: 현재 목표 build와 must-play flow를 막는 화면
P1: 반복 플레이·이해·설정·성장을 지탱하는 화면
P2: 후속 content·mode·release 확장 화면
```

## 3. SCREEN_SURFACE_INVENTORY_FIRST

아래 화면 family를 전부 검사해. 프로젝트에 적용되면 row로 만들고, 적용되지 않으면 `NOT_APPLICABLE + 이유`를 남겨. 이유 없이 생략하지 마.

### A. 시작과 시스템 진입

- 부팅·splash·초기 loading
- 메인/타이틀 화면
- 새 게임·이어하기·불러오기
- 프로필·save slot·난이도·mode 선택

### B. 시작 구성과 선택

- 캐릭터·직업·무공·덱·파티·장비·시작 보너스 선택
- 선택 확인·잠금·조건 미충족·비교 화면

### C. 허브·지도·행로

- 홈·기지·허브
- 월드맵·노드맵·챕터·스테이지·행로 선택
- 현재 위치·도달 가능·잠김·완료·위험·보상 상태

### D. 핵심 gameplay

- 탐색·이동·조사·관리·건설·퍼즐 등 장르 핵심 화면
- HUD와 목표·자원·상호작용·경고
- 대화·인터뷰·이벤트·선택지·기록 열람

### E. 준비와 전투

- 임무·전투·구조 브리핑
- 파티·장비·스킬·적 정보·출발 확인
- 실제 전투장 또는 필드 전투
- 행동 선택, 순서, 사거리, 타기팅, 위험 예고
- 마법 작성·조준·퍼즐 입력·QTE·필살기·합·절초·보스 phase 같은 별도 overlay/컷인

### F. 결과와 반복 성장

- 전투·임무 검토
- 승리·패배·결과·보상 화면
- 경험치·재화·아이템·평가·기록
- 다음 단계·재도전·원래 장면 복귀
- 성장·강화·스킬트리·상점·제작·수리·휴식·정비

### G. 기록과 도움

- 도감·기록 보관소·매뉴얼
- 튜토리얼·도움말·조작 안내
- 검색·분류·잠금·미발견·empty state

### H. 일시정지와 설정

- pause
- 오디오·그래픽·입력·접근성·언어
- save·복귀·종료·변경 적용·되돌리기

### I. 실패·종료·예외

- game over·실패 사유·재시도·checkpoint
- ending·chapter complete·credits
- scene transition·loading·offline·reconnect
- permission·update required·save conflict·error·empty state

팝업이나 overlay라도 플레이어의 판단·입력·정보 위계가 달라지면 별도 screen surface로 기록해.

## 4. 화면 인벤토리 필수 필드

각 화면은 기존 프로젝트 DB·표·Markdown·JSON owner에 아래 정보를 매핑해. 기존 owner가 없을 때만 최소 새 owner를 만들어.

```yaml
screen_id:
screen_family:
screen_name:
project_stage:
priority: P0 | P1 | P2
flow_entry:
flow_exit:
player_goal:
player_question:
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY
consumer_surface:
screen_design_reference:
runtime_consumer:
existing_evidence:
coverage_status:
notion_destination:
repository_destination:
blockers: []
```

특히 각 화면에서 다음 질문에 답해야 해.

- 플레이어는 왜 이 화면에 들어오는가?
- 무엇을 가장 먼저 봐야 하는가?
- 어떤 결정을 내려야 하는가?
- 어떤 입력을 하는가?
- 성공·실패·선택 결과를 어떻게 이해하는가?
- 어디로 나가는가?

## 5. 화면 자체의 필수 visual 확인

적용 가능한 player-facing screen은 자산 조각만 있는 것으로 완료 처리하지 마.

다음 중 하나의 전체 화면 evidence가 필요해.

- 승인된 `SCREEN_DESIGN_REFERENCE`
- 목표 해상도의 wireframe 또는 high-fidelity mockup
- 실제 Godot scene capture
- 실행 가능한 prototype capture
- 검증된 기존 화면 재사용 evidence

전체 화면 evidence로 다음을 검토해.

- composition과 시선 흐름
- 정보 우선순위
- 감정과 첫인상
- 조작 위치와 focus
- 배경·캐릭터·UI·텍스트·VFX의 겹침
- 실제 목표 해상도·종횡비·입력 방식에서 가독성

**화면 목업 한 장과 runtime component는 같은 것이 아니다.**

```text
SCREEN_DESIGN_REFERENCE
→ 화면 전체 방향과 hierarchy 승인

RUNTIME_COMPONENT_ASSET
→ 게임이 직접 소비하는 배경·초상·sprite·icon·frame·texture·mask

GODOT_UI / TEXT_LAYER / SHADER / PROCEDURAL_DRAW
→ Godot가 실제로 조립·렌더하는 UI와 동적 표현
```

전체 화면 목업을 통째로 UI bitmap으로 넣지 말고, 실제 구현을 위해 분리해야 할 component와 engine-rendered layer를 구분해.

## 6. 화면별 구성요소 분해

각 화면을 최소 다음 층으로 분해해.

### 6.1 Composition / Identity

- 화면 배경·공간·프레이밍
- 로고·대표 실루엣·장면의 감정
- 시선 유도·negative space·information hierarchy

### 6.2 World / Character / Object

- 플레이어·적·NPC·초상
- 환경·타일·배경·전경
- 아이템·장비·건물·시설·상호작용 물체

### 6.3 UI / Icon / Typography

- panel·window·button·tab·slot
- HUD·gauge·cursor·focus·selection
- icon·marker·key prompt
- 수정·번역 가능한 실제 text layer

### 6.4 State / Variant

- normal·hover·pressed·focus·selected
- disabled·locked·warning·new·completed
- 방향·등급·진영·장비·phase·피해 상태
- keyboard·gamepad·touch·language 변형

### 6.5 Feedback / Telegraph / VFX

- 위험·사거리·경로·선택·타기팅
- 공격 예고·hit·회복·상태이상
- 성공·실패·보상·해금·전환

### 6.6 Technical Consumption

- resolution·aspect ratio·crop·safe area
- alpha·mask·9-patch·slicing·pivot
- filter·mipmap·compression·atlas
- shader input·animation frame·localization 분리

그다음 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`로 자산 category와 `STATE_FAMILY_COMPLETENESS`를 교차 검사해.

## 7. 제작 방식 판정

각 component에 아래 방식 중 하나 이상을 지정해.

```text
EXISTING_APPROVED
REUSE_PROJECT
REUSE_BASE_REFERENCE
GODOT_UI
TEXT_LAYER
SVG_VECTOR
RASTER_IMAGE
SPRITE_SHEET
SHADER
PROCEDURAL_DRAW
SCREEN_DESIGN_REFERENCE
NO_NEW_IMAGE_FILE_REQUIRED
DO_NOT_GENERATE
```

중요:

- 화면은 필수여도 모든 요소가 별도 PNG일 필요는 없어.
- button, panel, gauge, focus, dynamic text는 Godot Theme/Control/StyleBox가 더 적합할 수 있어.
- 지도 선·노드·범위·경로는 procedural drawing이 더 적합할 수 있어.
- localization이나 수치 변화가 있으면 이미지 안에 text를 굳히지 마.
- `NO_NEW_IMAGE_FILE_REQUIRED`는 화면 누락이 아니라, 필요한 표현을 기존 자산·Godot UI·SVG·text·shader로 충족한다는 뜻이야.

## 8. Existing Solution First

신규 이미지나 component 제작 전에 다음 순서로 확인해.

1. 현재 프로젝트의 실제 구현과 승인 자산
2. 프로젝트 Notion Asset/Reference/Visual Bible
3. 같은 프로젝트에서 재사용 가능한 화면·UI·icon·background
4. Base의 공용 pattern·case·reference
5. 직접 관련된 다른 프로젝트의 검증된 구조적 교훈
6. 필요한 경우에만 외부 benchmark
7. 마지막 수단으로 신규 제작

벤치마크는 `ADOPT / ADAPT / REJECT`로 판정하고 프로젝트 고유 정체성을 우선해.

## 9. 실제 교정 작업

분석·제안만 남기지 말고 승인 범위 안에서 현재 프로젝트 정본을 실제 교정해.

### Notion

기존 프로젝트 구조를 유지하면서 필요한 위치에 반영해.

- Home 상단: 핵심 화면, 전체/UX Flow, 대표 visual, 현재 목표 build
- Screen/Flow: 전체 screen inventory와 진입·이탈·플레이어 목표
- Visual Bible: 화면 family, composition, hierarchy, Keep/Avoid
- Asset Library: asset family, consumer, source, 상태, screen relation
- Production/Handoff: 다음 screen reference·runtime asset·Codex queue

사람이 Project Home에서 핵심 화면과 결과물을 찾을 수 있게 하고, 세부 AI 검증 로그는 AI/Production 영역에 둬.

### GitHub

프로젝트의 기존 owner·schema·경로를 우선해 다음을 반영해.

- screen inventory Markdown/JSON
- screen-to-asset coverage matrix
- runtime scene/resource/data consumer link
- requirement/asset manifest relation
- Codex가 사용할 exact path와 acceptance
- test/runtime evidence와 handoff

중복 정본을 만들지 말고 기존 owner가 있으면 그 문서를 교정해.

### Godot

실제 consumer가 이미 존재하거나 화면 검증이 가능한 경우에만 Godot를 사용해.

- scene/node/resource 연결 여부 확인
- 목표 해상도·종횡비·입력 방식에서 화면 확인
- focus, selected, disabled, loading, result 같은 상태 확인
- 캡처·로그·테스트 evidence 기록
- 사용이 끝나면 이번 작업에서 연 Godot process를 종료

새 구현·코딩은 현재 Work 범위를 넘으면 Codex용 작업지시문으로 분리하고, 구현 완료처럼 주장하지 마.

## 10. 이미지 생성 금지 경계

이번 지시문의 기본 작업은 **전수조사·교정·제작 준비**야.

```text
NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS
```

현재 사용자 메시지가 실제 이미지 생성·편집을 명시적으로 요청하지 않았다면 이미지 도구를 호출하지 마.

- gap 발견은 이미지 생성 승인 아님
- 한 화면 누락은 다음 화면·상태·variant 자동 생성 권한 아님
- screen reference와 runtime component는 각각 독립 deliverable
- 이미지가 실제로 필요한 항목만 exact consumer, 규격, brief, validation을 갖춘 queue로 올려
- 설명용 sheet·관계도·체크리스트 장식은 기본 image queue에서 제외하고 editable text/table/Flow/DB로 보완해

## 11. 필수 산출물

현재 프로젝트 정본에 맞는 형식으로 다음을 완성해.

### A. Target Screen Inventory

모든 적용 가능한 screen/overlay/transition과 `P0/P1/P2`, 상태, evidence를 기록.

### B. Screen → Asset Coverage Matrix

화면별 구성요소, 상태·변형, actual consumer, 제작 방식, existing/reuse/requirement를 연결.

### C. Screen Design Reference Queue

전체 화면 composition·hierarchy 검증이 필요한 화면만 정리.

각 row:

```yaml
screen_id:
consumer_surface:
player_goal:
reference_needed:
existing_anchor:
required_fidelity:
validation:
priority:
```

### D. Runtime Asset Family Queue

실제 Godot consumer가 있는 component만 정리.

각 row:

```yaml
asset_family_id:
screen_ids: []
runtime_consumer:
role:
states: []
variants: []
production_mode:
format_and_spec:
existing_or_reuse_source:
requirement_id:
validation:
status:
```

### E. 교정 로그

각 finding을 다음 순서로 기록해.

```text
현행
→ 문제
→ 교정
→ 실제 사용 예
→ 기대효과
→ 검증 evidence
```

### F. Codex 구현 Handoff

Work에서 확정·승인된 자료만 사용하도록 다음을 명시해.

- exact Notion page/database
- exact GitHub path/commit
- screen별 runtime consumer
- 구현 방식과 non-goal
- acceptance test
- Godot 실행·화면 검증 방법
- 사용 가능한 승인 image locator
- 아직 생성·승인되지 않은 asset은 placeholder 또는 blocker로 명시

### G. 남은 작업

```text
남은 blocking gap
남은 nonblocking gap
사용자 결정 필요
Codex 구현 필요
이미지 brief 승인 필요
runtime/player validation 필요
```

## 12. 적대적 검토와 완료 Gate

전체 결과를 최소 5회 다른 관점으로 다시 읽고 교정해.

1. **화면 완전성:** 목표 flow의 화면·overlay·transition이 빠지지 않았는가
2. **플레이 판단:** 각 화면이 감정·선택·고민·보상·결과를 명확히 전달하는가
3. **자산 완전성:** component의 필요한 상태·변형·feedback이 빠지지 않았는가
4. **과잉 제작 방지:** Godot UI·text·SVG·shader·reuse로 충분한 것을 불필요한 이미지로 만들지 않았는가
5. **정본·구현 현실성:** Notion/GitHub/Godot consumer, path, evidence가 서로 일치하는가

다음 조건 전에는 완료라고 하지 마.

```text
목표 build의 relevant screen 전부 기록 또는 NOT_APPLICABLE + 이유
→ 메인/타이틀 화면, 핵심 gameplay, 결과·보상, pause/settings 존재 여부 명시
→ 각 화면의 player goal/question/entry/exit 확인
→ 전체 화면 reference와 runtime component 분리
→ 화면별 구성요소·상태·변형·제작 방식 연결
→ P0 남은 blocking gap 0 또는 명시적 Decision/Blocker
→ Notion readback
→ GitHub exact path/readback
→ 가능한 범위의 Godot runtime evidence
→ 새로운 유효 P0/P1 finding 0
```

## 13. 최종 보고 형식

중간 진행 보고는 꼭 필요한 blocker만 짧게 하고, 작업 종료 시 아래 순서로 보고해.

```text
1. 작업 전 상태
2. 개선된 기능과 교정 내용
3. 실제 프로젝트에서 어떻게 사용되는지
4. 검증 결과와 evidence
5. 기대효과
6. 아직 개선되지 않은 범위
7. 남은 blocking gap / nonblocking gap / 다음 단일 milestone
```

‘이미지 목록을 만들었다’가 아니라, **목표 빌드의 모든 실제 화면과 시각 소비처가 추적되고 누락이 교정됐는지**를 기준으로 종료해.