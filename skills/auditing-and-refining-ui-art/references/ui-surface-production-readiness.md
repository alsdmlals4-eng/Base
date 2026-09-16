# UI·게임 제작 준비와 모듈형 시각 자산

## 0. 역할·적용·권위

`NOT_A_SECOND_CANON` · `OPEN_PR_READ_ONLY`

이 문서는 `auditing-and-refining-ui-art`의 기존 `flow-and-information-architecture`, `pattern-selection`, `design-system-contract`, `godot-ui-contract`, `runtime-ui-audit`를 연결하는 subordinate companion이다. 새로운 Skill, 제작 단계 상태 머신, 게임 정본, 캡처 도구가 아니다.

기존 Feature Spec·화면 인벤토리·Asset Catalog·Traceability에 연결한다. 현재 프로젝트의 같은 질문을 이미 소유하는 원본에 부족한 정보만 추가한다. 새 공용 JSON schema나 모든 프로젝트의 경로 이동을 요구하지 않는다. Base와 프로젝트의 중복 교정·다른 open PR의 흡수는 하지 않는다.

2026-09-01의 직접 사용자 지시는 외부 게임 비교를 먼저 수행하고, 필요한 시스템·메뉴·페이지·탭·대화창 테두리와 구현 참고까지 준비하며, 개별 이미지를 모듈로 제작·조합·재사용하라는 작업 계약이다. 이는 모든 프로젝트의 제품 기능 추가, 미승인 이미지의 정본 승격, 유료 도구, 배포 또는 기존 PR takeover 허가가 아니다.

| 점검 ID | 연결할 기존 책임 |
|---|---|
| UI-REFERENCE-FIRST | 외부 비교 기준을 먼저 수립한 뒤, 실제 적용 전에 프로젝트 정본을 fresh-read한다. |
| UI-INPUTS | 현재 승인 범위, 장르·플레이어 약속, 기존 코드·시안·승인 이미지와 actual/planned consumer를 확인한다. |
| UI-SURFACES | 전체 흐름·화면·페이지·탭·overlay와 실제 입력·도착 상태를 연결한다. |
| UI-MODULES | 개별 원본 → 재사용 컴포넌트 → 화면 조합의 제작 계약을 정한다. |
| UI-ASSETS | 미제작·승인 대기·미연결·미검증을 구분하고 필요한 제작을 실행한다. |
| UI-EVIDENCE | 실제 입력·저장 왕복·인게임 캡처·수정 후 재검증을 연결한다. |

## 1. UI-REFERENCE-FIRST — 외부 사례로 비교 기준부터 만든다

사용자가 benchmark-first를 지시한 작업 순서는 다음과 같다.

`외부 게임 비교 기준 → 프로젝트 정본 fresh-read → 차이 분석 → ADOPT / ADAPT / REJECT → 필요한 제작·구현·검증`

기존 프로젝트에 이미 있다는 이유만으로 좋은 구조로 간주하지 않는다. 반대로 외부 기준은 프로젝트의 승인된 의미·자산·version lock을 덮어쓰지 않는다. 실제 수정 전에 대상 프로젝트 AGENTS, current owner, 실제 코드·데이터·씬·자산·테스트, 동일 목표 PR을 확인한다. 기존 승인 자산의 재사용 적합성도 이때 검사한다. benchmark-first는 구현 전 fresh-read를 생략하라는 뜻이 아니다.

각 참고는 작품/자료, URL, 날짜·버전·commit, 정확한 화면/섹션/timecode, 직접 관찰, 추론, 비교 문제, 채택 원리, 기각할 부분, 프로젝트 적용 방법, 실패 조건, 최소 검증을 기록한다. 이미지·영상에서 확인한 모습, 개발자의 제작 설명, 공개된 코드, 공식 API 예제를 서로 구분한다. 상용 게임의 스크린샷으로 비공개 구현을 확인했다고 주장하지 않는다.

### 외부 비교 기준의 출처

| 원출처 | 확인한 범위 | 흡수·제한 |
|---|---|---|
| Factorio FFF-246 | GUI 개선안의 정보 그룹·작업 영역·간격을 설명하는 개발자 문서. 당시 mockup도 포함한다. | 페이지별 정보 위계와 행동 우선순위를 비교한다. mockup을 출시 빌드 캡처로 표시하지 않는다. |
| Factorio FFF-348 | GUI 개편, 일관된 아이콘과 상호작용 피드백을 설명하는 개발자 문서. | 화면 하나보다 반복되는 조작·아이콘·상태 언어를 함께 검수한다. |
| Wesnoth GUIWidgetDefinitionWML | panel의 background/foreground, border 공간, 상태별 widget 정의, multi_page/tab 구조. | 장식 layer·내용·상태를 분리하는 공개 구현 계약을 참고한다. WML 자체를 Godot에 복사하지 않는다. |
| Mindustry Styles.java | 공통 drawable, 버튼의 up/down/over/disabled 및 TextButton 스타일 정의를 공개 코드로 확인. | 스타일과 화면 조립을 분리하는 방법을 참고한다. Java/Arc 코드나 원본 아트를 프로젝트 자산으로 복제하지 않는다. |

- https://www.factorio.com/blog/post/fff-246
- https://www.factorio.com/blog/post/fff-348
- https://wiki.wesnoth.org/GUIWidgetDefinitionWML
- https://github.com/Anuken/Mindustry/blob/da3b3358cd03e47ef32a87ee5b40231e656d1c76/core/src/mindustry/ui/Styles.java

이 자료는 외부 구조 비교 근거다. 해당 게임을 이번 작업에서 직접 플레이했거나, 특정 출시 버전 전체를 검증했다는 주장은 하지 않는다. 실제로 읽은 자료·이미지와 접근 실패를 작업 receipt에 구분한다.

## 2. 완결 경험과 전체 제작 영역

승인한 플레이 범위의 시작 → 준비 → 핵심 플레이 → 결과 → 기록/성장 → 복귀 → 저장·재개를 닫는다. 콘텐츠 수량을 줄일 수는 있지만, 포함한 행동을 가짜 버튼이나 막다른 화면으로 남기지 않는다.

적용 여부를 살필 영역은 핵심 재미·선택·보상, 조작·카메라, 전투·적·레벨, 대화·서사, 성장·경제, 메뉴·UI, 이미지·애니메이션, 오디오·VFX, 저장·복구, 접근성·현지화, 성능·플랫폼, 패키징·권리·출시다. 온라인·수익화·업적 등은 실제 필요가 있을 때만 포함한다. 외부 게임의 모든 기능이나 콘텐츠 수량을 복제하지 않는다.

각 영역은 현재 package의 `REQUIRED`, 근거 있는 `DEFERRED`, 이유 있는 `NOT_APPLICABLE`로 분류한다. 미확인을 0으로 계산하지 않는다. 승인한 requirement를 분모로 삼고, 현재 코드에 없다는 이유로 화면이나 필요한 자산을 제외하지 않는다.

작은 기술 probe는 호환성·알고리즘 같은 불확실성만 검증한다. 전체 게임을 먼저 구현한 뒤 Blueprint를 승인하는 순환을 만들지 않는다.

## 3. UI-SURFACES — 화면·메뉴·페이지·탭·대화창

기존 화면 원본에 다음을 연결한다.

`player question → entry → visible information → input → domain owner/result → feedback → exit/back → re-entry/save → test/capture`

Tab은 같은 맥락의 페이지 전환인지, route는 장면/작업 전환인지, modal은 일시적 입력 소유인지 먼저 구분한다. 닫힌 page가 게임 입력·Timer·보상 처리·오디오를 계속 소비하지 않게 한다. modal을 닫으면 이를 연 요소 또는 유효한 의미 위치로 focus를 돌린다. 빈 목록, 잠김, loading, 오류, 변경 적용 전/후, 취소, 긴 한국어를 포함한다.

| 기능 | 실동작 기준 |
|---|---|
| 새 게임 | 승인된 초기 상태를 한 번 생성하고 플레이에 도달. 기존 저장 덮어쓰기 확인·취소와 연타 처리. |
| 이어하기 | 정상/없음/손상/구버전 저장을 구분. 프로그램 재시작 뒤 실제 진행·자원·해금·위치를 복원. |
| 도감 | 실제 데이터와 관측/해금 상태, 목록·상세·분류·필요한 검색·뒤로가기. 숨겨야 할 정답을 노출하지 않음. |
| 설정 | 실제 음량·화면·입력·접근성 consumer에 적용, 저장·취소·초기화·화면 복구·재실행 유지. |
| 종료 | 해당 플랫폼의 정상 종료와 승인된 저장 정책. 저장 실패를 성공으로 숨기지 않음. |
| 결과 뒤 | 비용·보상·기록을 한 번 반영한 뒤 다음 플레이·허브·메뉴·재시작 중 승인된 목적지로 이동. |

`PUBLIC_INPUT → 도메인 결과 → 도착 화면 → 저장·재진입`을 시험한다. 버튼·signal·파일 존재만으로 실동작 완료라 하지 않는다. 테스트용 private method 호출은 public navigation 증거가 아니다. 직접 보트 진입처럼 승인된 예외에는 시작 메뉴를 억지로 추가하지 않는다.

플로우맵은 editable text/Mermaid/data가 우선이다. 사람이 보는 참고 화면은 실제 scene/control/state와 매핑하며, 이미지 속 화살표나 버튼을 동작 구현으로 세지 않는다.

## 4. UI-MODULES — 독립 이미지와 재사용 컴포넌트

`MODULE_ART → COMPONENT_SCENE → SCREEN_ASSEMBLY`

비교한 대안:
- 화면마다 한 장의 완성 이미지를 만든다: 빠른 구도 시안에는 적합하지만 텍스트·해상도·상태 변경과 재사용에 불리하다.
- 모든 모서리·장식을 최대한 잘게 나눈다: 정렬·색·광원·seam·조합 수와 관리 비용이 늘어난다.
- **의미 있는 독립 부품을 만들고 컴포넌트와 화면에서 조합한다**: 기본값. 자연스러운 일체형 그림이 필요한 경우는 하나의 부품으로 유지한다.

개별 원본과 안정된 asset_id를 보존한다. 실제로 다른 화면·상태·내용에서 바꿔 쓰는 경계로 나눈다. 완성 화면 한 장을 잘라 부품이 있다고 간주하지 않는다. 시안 sheet와 collage는 참고일 뿐 개별 production 원본의 대체물이 아니다.

`ATLAS_IS_PACKAGING_NOT_AUTHORING`: 개별 원본을 검수한 뒤 엔진 소비·성능을 위해 atlas로 묶을 수 있다. 원본 ID·SHA-256·region mapping·padding을 보존하고 packing 후 bleed/import를 검증한다. atlas 파일 하나라는 이유로 재생성·승인·consumer 상태를 한꺼번에 올리지 않는다.

| 자산군 | 분리·조합 예 |
|---|---|
| 환경 | 배경 / 전경 / 독립 소품 / 캐릭터 / 날씨·빛·효과. 서로 가릴 순서와 허용 변형을 지정. |
| SYSTEM_PANEL | 재사용 프레임 / 제목 장식 / 구분선 / 버튼 skin / 상태 icon. 현재 사용처가 없는 장식은 생성하지 않음. |
| DIALOGUE_FRAME | 본문 프레임 / 이름표 / 초상·필요 표정 / 선택지 skin / 진행 표시. history·auto·skip은 승인된 기능일 때만. |
| TAB_FRAME·도감 | 탭 skin / 목록 행·선택 표시 / 내용 frame / item·portrait / 잠금·새 항목 상태. |
| 카드·장비 | frame / 내용 illustration / 분류·상태 icon / 실제 비용·설명 text. |
| 지도·flow | 배경 / node·장소 icon / 상태 표시. 실제 경로·도달 가능성·입력은 데이터·엔진이 소유. |

`IMAGE_MODEL_REQUIRED`: 필요한 원화·프레임·아이콘·캐릭터 등 새 이미지 생성·그림 내용 편집은 이미지 모델을 사용한다. 직접 그린 SVG/Canvas/Python drawing/Godot primitive로 필요한 아트를 대체하지 않는다. 기존 승인 이미지의 기술적 atlas packing·규격 변환은 별도 파생 처리로 기록한다.

텍스트·수치·입력은 실제 Control 및 도메인 데이터로 유지한다. 작동 가능한 UI를 한 장의 이미지로 굳히지 않는다. 동일 이미지 스타일을 모든 프로젝트에 강제하지 않는다. 공용화 대상은 호환성·구성·검증 방법이지 세계관·그림체·캐릭터·palette 자체가 아니다.

## 5. 테두리·호환성·조합 레시피

9-slice 프레임 한 장을 아홉 번 따로 생성하지 않는다. authored source 한 장과 slice margin으로 모서리·변·중앙의 확대 규칙을 정한다. visual border와 text content padding을 구분하고, 이름표·초상·선택지는 실제로 교체·재사용할 필요가 있는 경우 분리한다.

기존 owner 필드에 다음 의미를 매핑한다. 새 저장 schema 의무가 아니다.

| 정보 | 확인할 내용 |
|---|---|
| style_family / compatible_slots | 같은 조합에서 허용되는 재질·화풍·semantic slot |
| pivot_or_anchor / alpha_mode | 기준점, 실제 alpha, crop-safe 영역, 배경 제거 상태 |
| slice_margins / text_safe_area | 9-slice 규칙, 최소 크기, 내용 여백·긴 텍스트 |
| filtering / allowed_transforms | 보간·mipmap·pixel density, 허용 scale/crop/flip/tint와 금지 |
| assembly_recipe | 기존 asset ID/version, slot, layer order, layout constraints, 필요한 상태 |
| consumer / approval / evidence | 실제·계획 소비처, 승인 범위, 구현·캡처와 보관 경로 |

Godot 구현은 현재 Theme/type variation, PanelContainer + StyleBoxTexture 또는 NinePatchRect, MarginContainer 등 기존 Container와 live text/Control을 재사용한다. 장식 layer는 pointer를 가로채지 않는다. TabContainer의 표시 전환만으로 게임의 pause·cancel·도메인 안전성이 구현됐다고 보지 않는다.

공식 구현 참고:
- https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html
- https://docs.godotengine.org/en/stable/classes/class_tabcontainer.html
- https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html

적용 시 프로젝트가 고정한 Godot 버전의 API·import·최소 크기를 확인한다. 최신 문서 조회가 engine upgrade 승인이 아니다.

아래는 설명용 조합 데이터이며 파일·자산·Scene이 구현됐다는 증거가 아니다.

```json
{
  "example_kind": "ILLUSTRATIVE_MODULE_COMPOSITION",
  "evidence_status": "DESIGN_EXAMPLE_NOT_RUNTIME",
  "modules": [
    {"asset_id": "FRAME_SHARED", "role": "resizable_panel_frame"},
    {"asset_id": "TAB_SHARED", "role": "tab_skin"},
    {"asset_id": "BUTTON_SHARED", "role": "button_skin"},
    {"asset_id": "NAMEPLATE", "role": "speaker_name_frame"},
    {"asset_id": "PORTRAIT", "role": "character_portrait"}
  ],
  "assemblies": [
    {"id": "dialogue", "module_ids": ["FRAME_SHARED", "BUTTON_SHARED", "NAMEPLATE", "PORTRAIT"], "live_text": true, "flattened_runtime_ui": false},
    {"id": "codex", "module_ids": ["FRAME_SHARED", "TAB_SHARED", "BUTTON_SHARED", "PORTRAIT"], "live_text": true, "flattened_runtime_ui": false},
    {"id": "settings", "module_ids": ["FRAME_SHARED", "TAB_SHARED", "BUTTON_SHARED"], "live_text": true, "flattened_runtime_ui": false}
  ]
}
```

대표 조합 하나 → 두 번째 실제 consumer의 재사용 → 기존·신규 부품의 혼합 조합을 검수한다. 조합 수를 전부 곱해 이미지 생성량으로 계산하지 않는다. 상태별 표현은 필요하지만 모든 hover·focus에 별도 PNG가 필요한 것은 아니다. 필요한 고유 형태 변화는 별도 이미지로 만들고, 이미 승인된 skin 위의 native focus/opacity 등 표현과 구분한다.

## 6. UI-ASSETS — 확인에서 실제 제작까지

`PLANNED_CONSUMER`: 구현된 노드가 없어도 승인된 화면·상태·예정 scene/node/slot·규격·사용 방법·test가 구체적이면 필요한 후보를 준비할 수 있다. 이를 IMPLEMENTED로 기록하지 않는다. “이미지가 없어 구현 못함 / 구현 안 돼 이미지 못 만듦” 순환을 만들지 않는다.

기존 이미지 원본을 직접 열어 alpha·규격·크롭·내용·필요 상태·시각 방향을 확인한다. filename/manifest만으로 이미지 검수 완료라 하지 않는다. 접근 불가는 미확인으로 남긴다.

누락은 `미제작 / 생성 후보 / 승인 대기 / 원본 회수 불가 / 미연결 / 조합 불일치 / 런타임 미검증`으로 나눈다. 이미 생성된 후보를 다시 미제작으로 세지 않는다. `NO_NEW_IMAGE_REQUIRED`도 실제 reuse/native 표현 근거가 있어야 한다.

필요성이 확정되면 브리프·호환 규격·실제 개별 후보 생성·객관 검수까지 진행한다. 최종 사용자 승인 전 `USER_APPROVED` 또는 canon/runtime asset으로 승격하지 않는다. 승인된 모듈을 허용된 기존 조합에 재사용할 때 routine 재승인을 반복하지 않지만, 새로운 핵심 시각 의미·허용 밖 변형·다른 자산 교체를 자동 승인하지 않는다.

## 7. UI-EVIDENCE — Blueprint·구현·캡처·교정

Work는 참조 적용 방법·상태·schema·실제 example data·이미지/오디오/VFX·tests·실패/rollback까지 준비하고, 검수된 exact Blueprint와 자산 범위를 승인받는다. Codex는 해당 repository revision과 실제 파일을 fresh-read하여 구현한다. 핵심 미결정을 구현자가 즉석에서 정하게 넘기지 않는다.

`IN_GAME_CAPTURE_REQUIRED`: 시각·디자인 변경은 관련 화면의 실제 인게임 캡처를 보존한다. 필요한 전후 비교·선택/비활성/오류·motion 핵심 frame을 포함한다. exact source commit/build, project/scene/state, viewport·renderer·input, 실제 consumer, 파일 path/hash, diagnostics와 검사 결과를 연결한다. 기존 repository/CI artifact 보관 owner를 재사용하며, 저장 정책·권리·개인정보·용량 경계를 지킨다.

생성 시안은 인게임 캡처를 대체하지 않는다. 캡처만으로 클릭·저장·음량·자연스러운 전체 플레이를 증명하지 않는다. 주입한 fixture는 fixture라고 표시하고 public-entry playthrough와 구분한다. runtime을 실행하지 못하면 해당 상태를 NOT_RUN으로 유지하며 다른 준비 작업을 계속한다.

`DOC_CONTRACT_PASS ≠ RUNTIME_PASS ≠ HUMAN_PASS`

단일 부품 검수와 조립된 화면 검수는 다르다. 필수 조합의 잘림·가림·focus·긴 한국어·해상도·상태 판독을 확인하고 교정한다. 변경되지 않은 source/consumer의 유효 증거는 근거를 기록해 재사용할 수 있지만, 오래된 capture를 바뀐 제품 head의 PASS로 사용하지 않는다.

종료 시 기존 owner·test·이미지 상태·handoff를 readback하고 새 유효 blocker, 미검증, 승인 대기, 다음 안전 작업을 분리한다. 공용 절차·테스트 교훈은 Base에, 고유 작품·게임 규칙·모듈 원화·실제 조합·runtime 결과는 프로젝트에 남긴다.
