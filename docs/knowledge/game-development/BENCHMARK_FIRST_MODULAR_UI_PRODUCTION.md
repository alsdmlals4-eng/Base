# 외부 벤치마크 우선 · 모듈형 화면/이미지 제작 계약

Status: `USER_APPROVED_METHOD` (2026-09-01).
Owner: existing `auditing-and-refining-ui-art` design, Godot-contract and runtime-audit modes.
Evidence ceiling: `STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL`.

이 파일은 공용 진입점이다. 실제 작업에서는 다음 두 문서를 순서대로 읽는다.

1. [제작 방법 본문](BENCHMARK_FIRST_MODULAR_UI_PRODUCTION_METHOD.md)
2. [파생 packet·검사 계약](BENCHMARK_FIRST_MODULAR_UI_PRODUCTION_PACKET_CONTRACT.md)

본문은 외부 사례·전체 플레이 흐름·이미지 제작·Godot 적용·캡처를 설명하고, packet 계약은 구조 검사 입력과 fail-closed 관계를 소유한다. 두 문서가 충돌하면 packet의 기계 필드는 packet 계약, 게임 의미·미술 방향·승인·runtime은 프로젝트 고유 규칙과 실제 owner가 우선한다.

## 핵심 실행 순서

`EXTERNAL_THEN_PROJECT_FIT` · `MODULAR_PARTS_FIRST`

```text
외부 게임·공개 구현 비교
→ 독립적인 구조 후보
→ 프로젝트 정본·실제 consumer·승인 자산 적합성
→ APPROVED_SCOPE_IS_DENOMINATOR
→ PLANNED_CONSUMER_CONTRACTED
→ 개별 이미지 부품과 named assembly 준비
→ 부품·조합·Blueprint 승인 분리
→ exact-revision 구현
→ 실제 입력·저장 왕복·인게임 캡처
```

외부 조사는 권위가 아니라 설계 입력이다. 프로젝트 **고유 규칙**과 **이미 채택한** Base/engine pin, 승인 자산, 실제 코드·데이터·Scene·Resource·Test가 적용 권위를 가진다. 이 검사는 **선언된 분모 자체의 완전성은 증명하지 않는다**.

## 비교 근거와 적용 방식

공개 소스·공식 제작자료에서 Mindustry, Wildermyth, Wesnoth, Dialogic, Dialogue Manager, Ren'Py를 비교했다. Mindustry source 기준은 `da3b3358cd03e47ef32a87ee5b40231e656d1c76`, Wesnoth는 `69fb4534988c731f627246b1f0c3a98f239b69f7`이다. 결과는 기능·흐름·부품 경계를 `ADOPT / ADAPT / REJECT`로 변환하며 원본 코드·게임 이미지·폰트를 복제하지 않는다.

- Mindustry: 메뉴·Database·Settings·공용 상태 style을 ADAPT.
- Wesnoth: 배경·로고·live 메뉴·tip 페이지 분리를 ADAPT.
- Wildermyth: layer depth, 결합점, 호환 조건을 ADAPT.
- Dialogic / Dialogue Manager: 대화 layout layer와 typing/choice/input 상태 분리를 ADAPT.
- Ren'Py: 공용 game-menu shell과 layered image 원리를 ADAPT하되 엔진 교체는 REJECT.

## 화면·기능 범위

후보에는 `새 게임`, `이어하기`, `도감`, `설정`, `종료`, 허브·지도·HUD·결과·보상·실패·오류·로딩이 포함된다. 모든 프로젝트에 강제하지 않고 승인 범위에서 REQUIRED / DEFERRED / NOT_APPLICABLE을 판정한다.

`대화창`, 메뉴, 페이지, `탭`, modal, `OVERLAY`는 구분하되 각각 별도 Scene을 강제하지 않는다. signal 존재나 버튼 이미지가 아니라 **실제 입력 → command owner → 결과 → 복귀/저장**을 acceptance로 쓴다. 대화 입력은 타이핑 완성과 다음 문장 진행을 동시에 누출하지 않는다.

## 모듈형 이미지·UI

`AUTHORING_PARTS_NOT_RUNTIME_ATLAS` · `NO_SECOND_ASSET_CANON` · `NO_CARTESIAN_ASSET_EXPLOSION`

기본 부품은 FRAME/FILL/NAMEPLATE/ICON/PORTRAIT/BACKGROUND/PROP/SHADOW/OVERLAY/VFX/MASK다. 같은 frame·fill·nameplate를 대화·도감·보상에 재사용하고 기능 텍스트와 hit target은 live UI가 소유한다. 기술 atlas는 승인 원본의 packing 파생물이다.

`MODULE_APPROVAL_IS_NOT_ASSEMBLY_APPROVAL`: 부품 승인, 조합 승인, Blueprint 승인, runtime binding, 인게임 검증을 분리한다. 새 authored art에는 `IMAGE_MODEL_REQUIRED_FOR_AUTHORED_ART`를 적용한다.

Godot에서는 `StyleBoxTexture`, `NinePatchRect`, `TabContainer`, `AtlasTexture`, `Control`, `Container`, `Theme`를 프로젝트 버전에서 재확인한다. `texture_margin`은 이미지 분할, `content_margin`은 본문 여백이며 혼동하지 않는다. 엔진 자동 업그레이드를 하지 않는다.

## 시각 증거

`VISUAL_CHANGE_REQUIRES_INGAME_CAPTURE` · `MODULE_SHEET_IS_NOT_INGAME_CAPTURE`

시안·contact sheet·부품 hash는 실제 적용 증거가 아니다. 디자인 변경 완료에는 exact revision/build, scene/state/consumer, viewport/renderer, capture path·dimensions·`SHA-256`, diagnostics와 입력 경로를 연결한다. Human·device·접근성 검증을 하지 않았다면 `HUMAN_NOT_RUN` 등으로 유지한다.

## 파생 packet 필수 경계

- 최상위 `repository`는 URL이나 경로가 아닌 canonical `owner/repo`다. `.`·`..` segment와 `./.`는 무효다.
- `NATIVE_UI` family는 raster `module_ids`를 생략하거나 `null`로 둔다.
- raster module은 non-native family가 소유하고, 실제 조합되는 각 target surface도 그 family `surfaces`에 있어야 한다. 누락 진단은 `RASTER_MODULE_TARGET_UNOWNED`다.
- missing `--packet`이나 잘못된 gate 같은 parser-level argument error는 structured `INPUT_ERROR` JSON이다. 정상 `--help`는 exit 0이다.
- 정상 구조 검사는 `tools/validate_player_surface_plan.py`를 사용한다.

## 비용·동시성·상한

추가 유료 API, 새 addon, 새 dashboard, 새 capture service를 기본안으로 두지 않는다. 기존 열린 PR은 read-only이며 동일 owner를 침범하지 않는다. 구조 검사 통과는 버튼 작동, 이미지 품질, 승인 authenticity, Godot runtime, Human/device/release PASS가 아니다.
