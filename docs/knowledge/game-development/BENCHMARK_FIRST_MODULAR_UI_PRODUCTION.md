# 외부 벤치마크 우선 · 모듈형 화면/이미지 제작 계약

Status: `USER_APPROVED_METHOD` (2026-09-01 current direct instruction).
Owner: existing `auditing-and-refining-ui-art` design, Godot-contract and runtime-audit modes.
This reference extends those modes; it is not a new Skill, game framework, asset catalog or project canon.

## 1. 조사 순서와 적용 권위는 다르다

`EXTERNAL_THEN_PROJECT_FIT` · `MODULAR_PARTS_FIRST`

새 시스템·화면·시각 제작의 구조는 **다른 게임의 기능·흐름·제작 방식을 먼저** 관찰해 세운다. 우리 현재 구현의 부족한 범위를 외부 조사 대상의 상한으로 삼지 않는다.

```text
외부 게임/공개 구현/공식 제작 자료
→ 무엇이 있고 어떤 행동·상태·부품으로 작동하는가
→ 대안 비교와 독립적인 구조 후보
→ 프로젝트 최신 AGENTS·승인 결정·실제 코드/데이터/자산 대조
→ 고유 규칙·장르·플랫폼에 맞게 ADOPT / ADAPT / REJECT
→ 기존 구현/승인 자산 재사용 또는 최소 신규 준비
→ 기획·검수·개별 부품 제작·조합 검수·Blueprint 승인
→ exact-revision Codex 구현
→ 실제 입력·저장 왕복·인게임 캡처·교정
```

이는 **설계 조사 순서의 domain-specific 예외**다. 쓰기 전에 현재 저장소·보호 경로·다른 작업·승인 범위를 읽는 안전 의무는 그대로다. 외부 사례는 프로젝트 정본보다 높은 권위가 아니며 다른 게임의 모든 기능, 그림체, 자산, 수치, 비공개 코드를 가져오지 않는다. 기계적 수정에는 새 benchmark packet을 강제하지 않는다. 같은 범위와 source가 유효하면 기존 조사 증거를 재사용한다.

## 2. 실제 외부 근거와 흡수 범위

확인일: 2026-09-01. 아래는 공개 소스/공식 설명 관찰이며 상용 비공개 코드나 사용자 플레이 검증이 아니다.

| 사례 | 확인한 구성/구현 | 채택 | 기각·주의 |
|---|---|---|---|
| Mindustry | `MenuFragment`의 Play 하위 경로와 Database/Settings, `DatabaseDialog`의 탭·검색·해금 표시, `BaseDialog`의 닫기/일시정지, `Styles`의 공용 이미지 상태 | ADAPT: 공용 화면 틀 + 실제 데이터 + 경로/상태별 행동 | Java/Arc 이식, Mods/Editor/온라인 기능의 자동 추가, 단일 pause bool을 중첩 modal 전체에 복제하지 않음 |
| The Battle for Wesnoth | title WML의 배경·로고·메뉴 panel·tip 페이지 분리, 공통 버튼 정의/ID와 실제 메뉴 목적 | ADAPT: artwork와 live 메뉴/페이지의 분리 | 현재 프로젝트를 C++/WML이나 같은 캠페인 구조로 바꾸지 않음 |
| Wildermyth | PNG layer의 depth, 몸/머리/장비 grouping, rig/표정 조건·결합점으로 외형 조립 | ADAPT: 부품별 원본 + 결합 규격 + 호환 조건 | 모든 캐릭터를 paper-doll로 강제, 원작의 17표정·rig 수·해상도를 우리 수량으로 복사하지 않음 |
| Dialogic 2 | Base layout + textbox/choices/glossary 등 Layer scene + style resource | ADAPT: 대화 UI 부품과 배치/기능 조합을 분리 | 신규 addon 자동 설치, vendor 하위 공유 resource 직접 편집, 기존 대화 상태 owner 교체 금지 |
| Dialogue Manager example balloon | 타이핑 완료·대기·선택지·진행을 분리하고 같은 입력의 typing-skip 후 return | ADAPT: 한 입력으로 문장 완성과 다음 선택을 동시에 실행하지 않음 | 예제 경고 버튼, 자동 진행 정책, Polygon2D 화살표를 production art로 복제하지 않음 |
| Ren'Py GUI / Layered Images | frame/namebox/button-state 분리, 공용 game menu+내용, attribute 기반 layered image | ADAPT: 메뉴 shell 재사용과 조건부 부품 조합 | 엔진 교체, 모든 VN 편의 기능 강제, 경쟁작 UI/이미지 복제 금지 |

읽은 exact source:
- Mindustry `da3b3358cd03e47ef32a87ee5b40231e656d1c76`: https://github.com/Anuken/Mindustry/blob/da3b3358cd03e47ef32a87ee5b40231e656d1c76/core/src/mindustry/ui/fragments/MenuFragment.java ; 같은 commit의 `core/src/mindustry/ui/dialogs/DatabaseDialog.java`, `BaseDialog.java`, `core/src/mindustry/ui/Styles.java`.
- Wesnoth `69fb4534988c731f627246b1f0c3a98f239b69f7`: https://github.com/wesnoth/wesnoth/blob/69fb4534988c731f627246b1f0c3a98f239b69f7/data/gui/themes/default/dialogs/title_screen.cfg . 이전 `data/gui/window` 경로는 현재 없었으므로 directory discovery로 복구했다.
- Wildermyth 공식 도메인 modding wiki: https://wildermyth.com/wiki/Image_layers . 공개 게임 파일의 layer 계약 설명이지 비공개 엔진 코드 확인은 아니다.
- Dialogic: https://docs.dialogic.pro/styles-and-layouts.html . 구조 참고만 하며 설치·버전 채택은 별도 프로젝트 gate다.
- Dialogue Manager `8a49e8001a9021e1982b6e31a10066b41eac2fd2`: https://github.com/nathanhoad/godot_dialogue_manager/blob/8a49e8001a9021e1982b6e31a10066b41eac2fd2/addons/dialogue_manager/example_balloon/example_balloon.gd . 실행한 테스트로 오인하지 않는다.
- Ren'Py: https://www.renpy.org/doc/html/gui.html ; https://www.renpy.org/doc/html/layeredimage.html . 구조만 추출한다.

원본 코드·게임 이미지·폰트는 Base에 재배포하지 않는다. 실제 코드/자산을 채택할 때는 해당 라이선스·NOTICE·배포 권리와 프로젝트 호환성을 별도 확인한다.

## 3. 구조 대안과 선택

| 대안 | 적합한 경우 | 한계 | 판정 |
|---|---|---|---|
| 화면 전체를 한 장으로 제작 | 단일 고정 event illustration, title key art처럼 정적인 원화 | 버튼/텍스트/상태 변경과 재사용에 약함 | 제한적 예외; 기본안 REJECT |
| 모든 위젯·상태마다 전용 그림 | 독립 시각 변형 자체가 의미인 드문 상호작용 | 수량·일관성·유지비 증가 | 필요한 상태만 ADAPT |
| 개별 부품 + 공용 UI 동작 + 조합 규칙 | 대화·도감·메뉴·설정·보상·카드 등 반복 표면 | anchor/가림/호환성 검증 필요 | 기본 ADOPT |

최종 목표는 부품 수가 아니라 **다른 문맥에서 다시 쓰면서도 기능·가독성·고유 미술을 보존하는 것**이다.

## 4. 기능 흐름과 화면 종류를 함께 설계

`APPROVED_SCOPE_IS_DENOMINATOR`

기본 검토 후보: 시작/메인메뉴, 새 게임/프로필/이어하기, 선택·준비, 허브/지도, 핵심 플레이/HUD, 대화/선택지, 가방/장비/성장, 도감/기록/도움말, 결과/보상/재시작, 일시정지/설정, 확인/오류/로딩/빈 상태/끝맺음.

모든 프로젝트에 전부 추가하지 않는다. 후보마다 승인 범위, 가치, 기존 구현, `REQUIRED / DEFERRED / NOT_APPLICABLE` 근거를 대조한다. 직접 게임으로 들어가는 승인 흐름에 불필요한 title을 강제하지 않는다.

각 surface에는 ID, 중심 질문, entry, 실제 행동, exit/back, 상태·저장 owner, 오류 복구, 입력 장치, actual/planned consumer, acceptance를 연결한다. **메뉴 항목, 페이지, 탭, modal, overlay, 대화창은 구분**하지만 각각 독립 `.tscn`을 만들도록 강제하지 않는다.

Flow map은 Mermaid/표 같은 text-native 정보로 유지한다. 지도·그림은 수정 가능한 논리를 대체하지 않는다. `새 게임 → 첫 플레이 → 결과 → 기록/보상 → 복귀 → 저장 → 재실행/이어하기` 왕복의 목적지와 상태를 명시한다. 이미 구현된 씬만 세서 미구현 required 항목을 분모에서 지우지 않는다.

## 5. 개별 제작할 모듈과 조합 단위

`AUTHORING_PARTS_NOT_RUNTIME_ATLAS` · `NO_SECOND_ASSET_CANON`

| 부품 family | 개별 원본/결합 정보 | 조합 소비 예 |
|---|---|---|
| Panel / Frame / Fill | 외곽 테두리, 내부 재질, nine-slice margin, content padding | 대화창·설정·도감·보상·확인창 |
| Nameplate / Header / Divider | 이름표, 제목 장식, 구분선; 글자는 별도 | 대화·상세·퀘스트·이벤트 |
| Button / Tab / Slot | 몸체/테두리와 필요한 상태 표현; label/icon 분리 | 메뉴·선택지·페이지·카드 슬롯 |
| Icon / Badge / Overlay | 기능 아이콘, 잠금·새 항목·선택 등 상태 | 도감·가방·지도·HUD |
| Portrait / Object / Prop | 공통 canvas/anchor, pose/scale, 가림/빛 조건 | 대화·정보 카드·결과·플레이 장면 |
| Background / Foreground / Shadow / VFX | 배경/소품/그림자/효과를 필요에 따라 독립 | 같은 장면의 상태 변형·여러 배치 |

기본 저작 단위는 **각각 저장·교체·승인 가능한 원본 부품**이다. 기술적 atlas는 승인 부품으로부터 만든 packing 파생물일 뿐이며, 생성 모델에게 관련 없는 모든 부품을 콜라주 한 장으로 그리게 하는 것과 다르다. 프레임 한 장을 nine-slice로 쓰면 충분할 때 모서리 4개·변 4개를 무조건 따로 생성하지 않는다.

`IMAGE_MODEL_REQUIRED_FOR_AUTHORED_ART`: 새 장식 테두리·캐릭터·아이콘·배경 등 아트 생성·편집은 이미지 모델로 한다. SVG·HTML Canvas·Python drawing·Godot primitive를 직접 그려 이미지 모델의 대체물로 쓰지 않는다. 네이티브 Control/Theme는 레이아웃·실제 텍스트·입력·상태를 소유하며, 이것은 아트 이미지를 대신 그리는 행위와 다르다.

부품 기록은 프로젝트의 **이미 채택한** Asset Catalog/manifest owner를 쓴다. ID, 버전, source path/hash, 승인/provenance, style family, canvas/alpha/anchor, 필요 상태, consumer, scaling/nine-slice 규격을 연결한다. 여기서 똑같은 자산 정본을 하나 더 만들지 않는다.

조합 정의는 기존 Scene/Resource 또는 명시한 단일 layout owner가 소유한다. 필요한 slot, 부품 ID, draw order, anchor/scale, content safe area, 입력 소유와 style compatibility를 적는다. 같은 부분을 장면마다 다시 굽거나 부품 수정 때 새 화면 이미지를 모두 재생성하지 않는다.

예시(새 프로젝트 내용 확정이 아닌 구성 원리):
```text
대화창 = 공용 frame + paper fill + nameplate + portrait + live text + choice controls
아이템 상세 = 같은 frame + paper fill + item icon + live stats + action controls
보상창 = 같은 frame + emblem + reward icon slots + live result + return controls
```

## 6. 과분할·조합 폭발 방지

`NO_CARTESIAN_ASSET_EXPLOSION`

독립 변경/재사용/상태 전환에 가치가 있는 경계에서 나눈다. 한 번만 등장하는 완성 삽화, 특수 원근·포즈, 몸과 빛이 강하게 결합된 원화는 합리적 예외를 기록한다. 이를 핑계로 UI·label·버튼을 통째로 baked screenshot으로 만들지 않는다.

재사용은 프로젝트 미술군 안에서 먼저 성립해야 한다. 다른 게임의 수채화·픽셀·실사 조각을 호환 검수 없이 섞지 않는다. 이미지 수를 늘리기 위한 전역 모든 조합 생성은 금지한다. 사용되는 조합, 가장 작은/큰 layout, 긴 한글, 가림 위험과 의미가 달라지는 상태를 검증한다. 공통 테두리의 복수 소비 사례를 검증하되 모든 일회용 삽화에 두 번째 소비처를 억지로 만들지 않는다.

## 7. 대화창을 테두리부터 기능까지 한 묶음으로

테두리/내부 재질/이름표/초상/본문/선택지/넘김 표시/로그 접근을 구분한다. 타입 출력, 즉시 완성, 다음 문장, 선택지 대기, 확인, 중단·재개, 로그 열기·닫기, 긴 이름·본문·선택지를 계약한다. Auto/Skip/Log는 프로젝트에서 채택한 것만 제공한다.

한 번 누르면 타이핑 완성인지 다음 문장인지 명확히 하고 같은 입력이 두 행동으로 누출되지 않게 한다. 숨은 정답이나 비공개 선택을 UI가 자동 공개하지 않는다. 대화 종료 뒤 원래 화면·포커스·pause state를 복구한다. nested modal에서는 각 화면이 제멋대로 simulation을 resume하지 않고 기존 navigation/pause owner를 사용한다.

## 8. 메뉴·페이지·탭·도감의 실제 동작

| 항목 | 준비/검증할 계약 |
|---|---|
| 새 게임 | 초기화, 기존 저장 보호, 확인·취소, 첫 씬 진입, 연타 중복 차단 |
| 이어하기 | 저장 없음/손상/버전 불일치, 복원 성공, 종료→재실행 왕복 |
| 도감 | 실제 데이터/해금, 검색·필터·목록·상세, 빈 상태, 숨은 정보 보호, 복귀 |
| 설정 | 오디오/화면/입력 등 실제 consumer 적용, 취소·초기화, 저장 후 유지 |
| 종료 | 플랫폼 정책, 저장 중/실패, OS close, 해당 game process 종료 |
| 페이지/탭 | stable ID, active/hover/focus/disabled 구분, scroll/filter 보존 정책, 숨은 페이지 입력 차단 |
| modal | focus 진입·trap·복귀, 배경 click-through 차단, 중첩/취소·연타 |
| 결과/보상 | 한 번만 정산, 다음 선택, 재시작·허브·메뉴 복귀; 막다른 화면 금지 |

signal 존재나 예쁜 버튼 이미지가 아니라 **실제 입력 → command owner → 결과 상태 → 복귀/저장**을 acceptance로 쓴다. 탭 인덱스를 저장 데이터의 영구 ID로 사용하지 않는다.

## 9. Godot 구현 참고와 호환성

- `Control`/`Container`/공용 Scene와 기존 `Theme` variation을 먼저 활용한다. domain state·save·reward의 owner는 UI 밖에 둔다.
- 테두리는 `StyleBoxTexture`/`NinePatchRect`로 변·중앙 scaling/tiling과 모서리 보존을 지정한다. `texture_margin`(그림 분할)과 `content_margin`(본문 여백)을 혼동하지 않는다.
- 장식 layer는 입력을 가로채지 않게 설정하고, 부모 Container layout과 픽셀 anchor의 책임을 구분한다.
- `TabContainer`/`TabBar`는 실제 탭 의미에 맞춰 선택한다. 전환은 hide/show 또는 Scene 교체 중 현재 navigation owner와 맞는 방식 하나를 쓴다. 새 범용 router를 무조건 추가하지 않는다.
- atlas 사용 시 region/filter clipping·seam·pixel density를 검수한다. packing 전 개별 승인 원본과 버전/provenance는 보존한다.
- 공식 stable 문서는 검색 진입점이다. 실제 작업은 프로젝트의 고정 엔진 버전에서 API·import·render를 재확인하며 엔진 자동 업그레이드를 하지 않는다.

공식 참고: https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html ; https://docs.godotengine.org/en/stable/classes/class_ninepatchrect.html ; https://docs.godotengine.org/en/stable/classes/class_tabcontainer.html ; https://docs.godotengine.org/en/stable/classes/class_atlastexture.html ; https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html .

## 10. 제작 readiness와 최종 승인

`PLANNED_CONSUMER_CONTRACTED`는 아직 없는 scene을 있다고 주장하는 상태가 아니다. 기능/화면/slot/규격/상태/owner/acceptance를 계약하면 구현 전에도 부품 후보를 준비할 수 있다.

```text
NEEDED → BRIEF_READY → GENERATED_CANDIDATE → REVIEWED
→ USER_APPROVED → CANON_REGISTERED → IMPLEMENTED → RUNTIME_VERIFIED
```

`MODULE_APPROVAL_IS_NOT_ASSEMBLY_APPROVAL`: 부품 승인과 조합 layout 승인, Blueprint 승인, runtime binding, 실행 검증은 각각 기록한다. 후보 생성은 현재 사용자·프로젝트 승인 범위에서 진행하고 실제 최종 art lock은 사용자 결정으로 유지한다. Work가 필요한 부품·sound·data·참고 적용법·QA 입력을 준비하고 Codex는 exact revision을 재수화해 연결된 기능을 구현한다.

## 11. 디자인·시각 변경은 실제 인게임 캡처를 보존

`VISUAL_CHANGE_REQUIRES_INGAME_CAPTURE` · `MODULE_SHEET_IS_NOT_INGAME_CAPTURE`

디자인·시각 변경의 적용/완료를 주장할 때, 실제 실행 화면의 이미지를 기존 evidence owner에 남긴다. 최소한 source revision/build, 실행 entry/scene/state, viewport/renderer, consumer, capture path·dimensions·SHA-256, diagnostics, 입력 경로, 검증 상한을 연결한다. 가독성·동작·시간 연출은 해당 검사와 짧은 영상/연속 프레임을 보완한다.

기획 시안만 있으면 `PLANNING_REFERENCE_ONLY`, 구현/실행 환경이 없으면 해당 runtime는 `NOT_RUN`이다. 시안·부품 contact sheet·정적 mockup·해시 일치만으로 runtime/UX가 되지 않는다. 실제 입력 경로가 아닌 state injection을 썼다면 선언하고 full-flow 입력 증거와 분리한다. 유효하고 제품 바이트가 동일한 증거는 identity 근거를 남겨 재사용한다. 변경된 화면과 영향 경로만 재캡처해 낭비를 줄인다.

기존 `RM-TOOL-004`와 `FRESH_RUNTIME_ARTIFACT_GATE`, 프로젝트 capture tool을 재사용한다. 새 capture app이나 두 번째 전역 증거 schema를 강제하지 않는다. `HUMAN_NOT_RUN`, device·accessibility·release·rights·user lock은 machine screenshot으로 승격하지 않는다. 보존이 privacy/rights에 막히면 제한을 기록하고 동등한 안전 보관 경로를 선택한다.

## 12. 실행 가능한 구조 검사

기존 project validator가 같은 계약을 검사하면 그것을 우선한다. 공통 보완이 필요하면 같은 정본을 **파생 packet**으로 투영해 실행한다:

```text
python <Base>/tools/validate_player_surface_plan.py --packet <derived-packet.json> --gate plan
python <Base>/tools/validate_player_surface_plan.py --packet <derived-packet.json> --gate handoff
```

packet shape는 실행 테스트 `tests/test_player_surface_plan.py`의 `packet()`과 `add_modular_parts()`를 최소 fixture로 읽는다. fixture 값은 실제 승인·게임 데이터가 아니다. `schema_version=1`, `artifact_role=DERIVED_REVIEW_PACKET`, exact `source_revision`, repository/scope/approval locator, `benchmark_order=EXTERNAL_THEN_PROJECT_FIT`, `asset_strategy=MODULAR_PARTS_FIRST`가 필요하다.

required surface/action IDs는 승인된 범위를 독립 대조해 투영한다. 각 surface/action/family는 현재 owner에 연결한다. `modules`는 asset manifest 참조와 버전/style/canvas/anchor/alpha/상태만 투영하고, `compositions`는 assembly owner·target surface·required slots·parts(module_id/slot/z)를 투영한다. 실제 namespace와 state는 기존 owner로 매핑한다. 같은 raster family가 여러 화면을 대상에 포함하면 그 family의 부품들이 각 화면 조합에 연결되어야 한다. 다른 부품을 쓰는 variants는 같은 owner 아래 다른 family/assembly record로 표현한다.

plan은 미구현 계약과 후보를 허용한다. handoff는 선언한 부품과 조합의 승인 locator를 요구한다. 실행 결과는 `STRUCTURE_VALID / STRUCTURE_INVALID / INPUT_ERROR`와 **`STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL`**다. 이 검사는 파일 생성·네트워크·프로젝트 수정·이미지 승인·캡처·Godot 실행을 하지 않으며 **선언된 분모 자체의 완전성은 증명하지 않는다**. 승인 authenticity, source freshness, 실제 texture/hash/consumer 존재는 native owner readback·runtime 검사로 따로 증명한다.

## 13. 프로젝트 흡수·종료

Base의 root route에서 이 reference를 읽고, 기존 프로젝트 UX owner/Skill adapter에 최소 연결을 둔다. Base의 공용 계약을 통째로 복사하거나 프로젝트 engine/contract pin을 조용히 올리지 않는다. 별도의 additive workflow approval과 사용한 Base exact commit을 남긴다. 기존 열린 PR은 read-only이며 같은 경로를 소유하면 그 경로의 변경을 보류하거나 충돌 없는 기존 router에서 연결한다.

추가 유료 API·새 addon·새 dashboard는 기본안이 아니다. 기존 테스트/캡처/문서 owner를 재사용하고 비교로 검증된 빈 기능만 보완한다.

완료 보고는 문서, 구조 검사, 실제 구현, 인게임 capture, Human, 사용자 승인, 출시를 분리한다. 자동 검사 통과는 기획 전체 완성이나 플레이어 가치의 증거가 아니다. 교훈은 재현한 반례와 테스트로 남기고 프로젝트 고유 미술·설정·수치는 그 프로젝트에 유지한다.
