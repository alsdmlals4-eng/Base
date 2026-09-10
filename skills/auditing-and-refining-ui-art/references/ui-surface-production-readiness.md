# Benchmark-first 화면·메뉴·스킨 제작 준비

`UI_SURFACE_PRODUCTION_READINESS`는 기존 `auditing-and-refining-ui-art`의
`flow-and-information-architecture / design-system-contract / godot-ui-contract / runtime-ui-audit`
에서 사용하는 조건부 reference다. 새 Skill이나 범용 UI 엔진이 아니다.
기존 화면 인벤토리·UI 명세·Asset Catalog·검증 owner를 연결하는 절차이며 not a second canon이다.
No mandatory new schema. No new paid service. 상세 화면 후보군은 기존
`GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`, coverage 판정은
`GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`, 생성·승격은 현행 이미지 정책을 따른다.

## 불변 경계

- APPROVED_SCOPE_IS_THE_DENOMINATOR: required planned surfaces remain gaps even when no scene exists.
- PLANNED_CONSUMER_IS_NOT_RUNTIME: a specified future consumer permits preparation, not an implementation claim.
- PIXEL_READ_REQUIRED: filenames, manifests and hashes alone do not prove that image contents were inspected.
- NO_NEW_IMAGE_IS_NOT_NO_DESIGN: a reused/native skin still needs composition, states and readability review.
- GENERATED_CANDIDATE_IS_NOT_USER_APPROVED: final asset and Blueprint approval remain separate user decisions.
- CAPTURE_IS_NOT_ACTION_PROOF: screenshots do not prove clicks, persistence, timing, audio or recovery.
- VISUAL_RUNTIME_CLAIM_REQUIRES_CAPTURE: a visual runtime completion claim needs a retained in-game capture.
- PINNED_CONTRACT_PRESERVED: newer Base content is adopted explicitly, never by silently replacing a project lock.
- OPEN_OTHER_PR_IS_READ_ONLY: no takeover, rebase, absorption, closure or merge of another workstream.
- PROJECT_CANON_WINS: reference-game features never authorize new project scope or overwrite approved identity.
- FLOW_MAP_IS_TEXT_NATIVE: navigation maps stay editable text, tables or Mermaid, not generated artwork.
- IMAGE_ART_USES_IMAGE_MODEL: native controls do not replace required authored border, illustration or icon art.
- REVIEW_SELF_IS_NOT_INDEPENDENT: five author rechecks are not a separate independent review.
- ADOPTION_IS_NOT_RUNTIME: routing/document tests never become Godot, device, Human or release PASS.

## UI-REFERENCE — 외부 게임으로 후보 구조부터 세운다

2026-09-01 사용자 지시: 기존 프로젝트를 먼저 보며 부족한 것만 채우지 말고, 외부 게임의
플로우·메뉴·페이지·탭·대화·시스템 표현과 공개 구현을 먼저 비교한다.
최소 read-only identity/권한 bootstrap은 허용하지만 이를 제품 분석으로 확대하지 않는다.

BENCHMARK_FIRST_EXECUTION_ORDER
```text
EXTERNAL_BENCHMARK
→ CANDIDATE_STRUCTURE
→ PROJECT_RECONCILIATION
→ MODULE_PREPARATION
→ SCREEN_COMPOSITION_REVIEW
→ BLUEPRINT_AND_ASSET_APPROVAL
→ IMPLEMENTATION
→ RUNTIME_CAPTURE_AND_INPUT_VERIFICATION
```

- BENCHMARK_FIRST: establish the external interaction and implementation pattern before auditing project gaps.
- RECONCILE_BEFORE_MUTATION: external findings are candidates until current project authority, approved assets and consumers have been read.

직접 유사 장르, 같은 상호작용의 인접 장르, 공개 구현 또는 공식 샘플을 조합해 비교한다.
주요 판단은 실제로 유효한 3개 대안을 비교한다. 성공 화면뿐 아니라 긴 본문·빈 목록·실패·복귀·
해상도 변화도 확인한다. 같은 범위의 유효한 조사는 재사용하고 관련 drift만 재확인한다.
기존 Reuse First는 제작 전 재사용 대조로 유지하되 외부 연구를 기존 gap 목록 뒤로 미루지 않는다.

각 기록은 existing owner에 다음을 연결한다.

```text
source + source_version/date + 정확한 파일/페이지/장면
→ OBSERVED_BEHAVIOR (실제로 본 행동/화면)
→ SOURCE_VERIFIED (공개 코드/공식 구현) 또는 IMPLEMENTATION_HYPOTHESIS
→ ADOPT / ADAPT / REJECT + 차이·이유
→ reference_method (어느 상태·데이터·기법을 어떻게 적용할지)
→ 프로젝트 consumer·예제/실패 입력·검증·rollback
```

상용작 화면만으로 비공개 코드·데이터 구조를 단정하지 않는다. 작품 이름·링크 목록으로 끝내지 않는다.
원작의 소스·그림·문구를 복사하지 않고 원리만 변환하며 재사용 권리는 기존 rights owner에서 검토한다.

### 직접 확인한 외부 구현 — 2026-09-01

| 대상 | 확인한 구현 | 적용 원리와 기각 범위 |
|---|---|---|
| Shattered Pixel Dungeon | `Chrome.java`의 창/버튼/탭 NinePatch; `WndTabbed.java`의 선택 스킨·listener 해제; `chrome.png` 실제 픽셀 | 작은 스킨의 재사용과 탭 상태 분리를 ADAPT. 픽셀 그림체·수치·GPL 코드/이미지 복제는 하지 않음. |
| Mindustry | `MenuFragment.java`의 icon/text/callback·desktop/mobile 배열; `Styles.java`의 up/down/over/disabled/checked | 외형·문구·동작·플랫폼 배치를 분리. 모드·멀티플레이 같은 원작 기능은 자동 추가하지 않음. |
| The Battle for Wesnoth | GUI2 문서와 `window_default.cfg`의 스타일·내용 grid·tile 배경·닫기 버튼 | 스타일/레이아웃/제어를 분리. 자체 GUI 엔진과 원작 아트를 들여오지 않음. |
| Ren'Py 공식 샘플/GUI | textbox/namebox/choice·menu overlay·save slot·9-slice Frame | 대화 부품과 저장 슬롯의 조합을 ADAPT. 상용 게임 사례와 구분; 엔진 전환·auto/skip/rollback을 자동 추가하지 않음. |

정확한 구현 출처:
- Shattered Pixel Dungeon `7b8b845a76fe76c6b7c031ae9e570852411f56db`:
  `core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/Chrome.java`,
  `core/src/main/java/com/shatteredpixel/shatteredpixeldungeon/windows/WndTabbed.java`.
  https://github.com/00-Evan/shattered-pixel-dungeon/tree/7b8b845a76fe76c6b7c031ae9e570852411f56db
  확인한 `core/src/main/assets/interfaces/chrome.png`: 128x64, Git blob
  `2b567b38b19a578d147c1094f69c6babfdb3ffb0`. 외부 사례이지 프로젝트 자산이 아니다.
- Mindustry `da3b3358cd03e47ef32a87ee5b40231e656d1c76`:
  `core/src/mindustry/ui/fragments/MenuFragment.java`, `core/src/mindustry/ui/Styles.java`.
  https://github.com/Anuken/Mindustry/tree/da3b3358cd03e47ef32a87ee5b40231e656d1c76
- Wesnoth: https://wiki.wesnoth.org/Guitoolkit ;
  `data/gui/themes/default/widgets/window_default.cfg`, inspected blob
  `e0ff3d35a38432ef7b8169900d36ade3737b340f`.

이는 게임 전체 실행 QA가 아니다. 일부 Ren'Py 예제 이미지 원본은 회수하지 못했으므로
그 픽셀 검수를 완료했다고 주장하지 않는다. 공개 구현/문서와 화면 관찰의 증거 상한은 다르다.

## UI-FLOW — 후보 구조를 프로젝트의 실제 범위에 대조한다

외부 후보 구조를 세운 뒤 최신 AGENTS/read order → 채택 계약 → 승인 Decision·UI/기획 owner
→ 실제 코드·데이터·Scene·이미지·테스트·open PR을 읽는다. 이 정합화 전에는 제품을 수정하지 않는다.
범용 후보 목록에서 현재 Slice 필수 / 지원 / 후속 / NOT_APPLICABLE+이유를 판정한다.
승인된 직접 진입 게임에 타이틀·슬롯·도감·상점을 강제로 넣지 않는다. unknown은 완료나 미구현이 아니다.

| 대상 | 기존 owner에 연결할 항목 | 주요 반례 |
|---|---|---|
| 화면·메뉴 | surface_id, 목적, entry, exit, state_owner | 구현 inventory에 없다고 계획 요구 누락 |
| 페이지 | page_id, parent_surface, 데이터, 앞/뒤 | 빈/마지막/삭제된 페이지, 긴 본문 |
| 탭 | tab_id, parent_surface, 선택, focus_restore, scroll_restore | selected와 focused 혼동, 숨김·잠금·비활성 |
| 팝업·대화 | 호출 원인, 입력 소유자, return_target, cancel | 뒤 화면 클릭, 중첩 modal, 복귀 focus 유실 |
| Flow map | from/input/조건/to/실패·복귀/검증을 가진 edge | 화살표만 있고 호출·상태·검증 연결 없음 |
| 전체 흐름 | cold_start, 플레이, 결과, save_reload, 재진입 | 가짜 버튼, 결과 뒤 막다른 화면 |

같은 Scene의 페이지·탭도 판단/입력이 다르면 하위 surface/state로 추적한다.
문서용 Flow map과 게임 안의 지도는 별개다. 구조 정보는 text-native로 유지한다.

## UI-SKIN — 시스템 창과 대화창을 함께 명세한다

적용 가능한 `system_panel / dialogue_frame / nameplate / choice_row / continue_indicator /
history_panel / confirmation_modal / tab_header / tooltip / scrollbar / button / save_slot`을 확인한다.
아래 질문의 답은 기존 UI/Art 정본에 연결하며 새 스타일 정본을 중복 생성하지 않는다.

| 책임 | 확정할 내용 |
|---|---|
| 외형 | 승인 Art Direction, 재질, 테두리·모서리, 장식 밀도, 음영, 대비, opacity |
| 읽기 | text_safe_area, padding, 글꼴·줄간격, 긴 한국어, 이름·초상·본문·선택지 간격 |
| 대화 상태 | 등장/타이핑/완료/선택대기/로그/재개; 첫 입력은 본문 완성인지 다음 진행인지 |
| 입력 | 선택·이전/다음·닫기·취소·modal 차단, double 입력, focus/스크롤 복원 |
| 시각 상태 | normal/hover/focused/pressed/selected/disabled/locked/loading/warning/error 중 필요한 것 |

새 그림이 필요 없더라도 구성·상태·가독성 결정은 생략하지 않는다.
필요한 authored 테두리·아이콘·삽화는 이미지 모델로 제작한다. SVG/Canvas/Python drawing/Godot primitive로
새 그림을 대신 만들지 않는다. 기존 승인 이미지의 crop/export는 원본·변환 이력을 보존하는 기술 처리다.

## UI-MODULE — 개별 이미지 원본을 조합하는 것이 기본이다

- SEPARATE_MODULE_MASTERS: author each reusable image module as an independent source file; compose screens from module references.
- ATLAS_IS_DERIVED_PACKAGING: an atlas is a build/import derivative, not the only editable master or an image-model collage deliverable.
- COMPOSITION_IS_NOT_NEW_ART: reuse compatible module versions instead of regenerating a complete screen for each combination.
- TEXT_AND_ACTIONS_STAY_LIVE: localized text, numbers, hit targets and callbacks remain runtime controls, not baked image content.
- REUSE_WITHIN_APPROVED_FAMILY: share technical structure across projects, not unapproved palettes, motifs or character identities.
- COMPOSITION_COVERAGE_IS_BOUNDED: test declared consumers and distinct risky combinations, not an unbounded Cartesian product.
- NO_PROMOTION_BY_ASSEMBLY: assembling candidate modules does not approve their pixels, replace locked assets or prove runtime behavior.

| module kind | 독립 원본과 재사용 조건 |
|---|---|
| fill | 종이/천/금속 읽기면; 균일 조명, tile·색 변조·opacity 허용 범위 |
| frame_9slice | 글자/로고 없는 테두리; 모서리 고정, 변/중앙 stretch 또는 tile, minimum_size |
| nameplate | 인물/섹션 제목판; 실제 이름은 live text; 본문 프레임과 독립 비율 |
| button_plate / tab_plate | 문구·아이콘 없는 바탕; 상태는 별도 모듈 또는 검증된 overlay |
| state_overlay | focus/selected/disabled/locked/warning; 색 외 형태·설명 신호 유지 |
| icon / portrait | 테두리를 굽지 않은 아이콘·초상; 목록/정보창에서 재사용 |
| illustration / world prop | 배경·인물·오브젝트·효과 별도 레이어; 원근·빛·접점 정합성 |

분리 기준은 독립 교체 가치와 실제/계약된 재사용이다. 9-slice 프레임 한 개를 무조건 아홉 파일로
쪼개지 않는다. 늘어나면 깨지는 이름표·문양·로고는 분리한다. 단일 소비처 전용 이미지는 이유를
남겨 유지할 수 있다. 쓸 곳 없는 미래 부품이나 의미 없는 상태별 PNG를 양산하지 않는다.
완성 화면 mockup은 조합 검토용 파생물이며 개별 runtime 부품을 대체하지 않는다.

### 모듈 계약과 Godot 연결

기존 Asset Catalog에 다음을 매핑한다.

```text
module_id + module_version + compatible_family
+ 독립 source path / sha256 / approval / provenance
+ role / alpha / dimensions / filter / color space
+ slice_ltrb(texture_margin) / content_margin / minimum_size
+ stretch 또는 tile / anchor / pivot / text_safe_area
+ 지원 상태 / overlay 허용·금지 조합 / consumers / fallback
```

기존 `Theme / Control / Container / Signal`을 재사용한다. `PanelContainer + StyleBoxTexture`는
프레임과 내용 배치, `NinePatchRect`는 장식층, `TabContainer` 또는 기존 controller는 탭 전환에
사용할 수 있다. 프로젝트 pin에서 실제 지원을 확인하며 새로운 공용 UI 엔진을 만들지 않는다.
`region_rect`는 atlas 영역, `texture_margin`은 절단 경계, `content_margin`은 내용 여백으로 서로 다르다.
장식층의 `mouse_filter`가 입력을 가로채지 않아야 한다. palette/해상도/절단값은 프로젝트별로 확정한다.

### 화면 조합 recipe

기존 Scene/Resource 또는 UI 정본이 recipe를 소유한다. 각 slot은 `module_id@module_version`,
layer_order, anchor, 크기 규칙, 실제 데이터/입력 consumer를 참조한다. 같은 부품을 여러 slot에서
사용할 수 있고, 배치를 바꿔도 원본 이미지를 재생성하지 않는다.

| 조합 | 같은 패밀리의 부품 재사용 | runtime 책임 |
|---|---|---|
| 메인메뉴 조합 | background + fill + frame_9slice + button_plate + icon + state_overlay | 새 게임/이어하기/설정/종료와 실제 저장 가용 상태 |
| 대화창 조합 | background + portrait + fill + frame_9slice + nameplate + choice button_plate | speaker/body, 타이핑/다음, 선택 확정, 로그/복귀 |
| 도감·기록 조합 | fill + frame_9slice + tab_plate + icon/portrait + scrollbar | 해금 데이터, tab/page/검색/스크롤, 상세·뒤로 |

이미지 단독 QA와 조합 화면 QA를 구분한다. 대표 소비처, 최소/최대 크기, 긴 한국어,
selected+focus, disabled+설명, 복잡한 배경, 긴 목록·모달 복귀 등 실패 위험이 다른 조합을 선정한다.
무한 조합 대신 선택 근거를 기록한다. 모서리 왜곡, alpha 가장자리, atlas bleed, 이중 그림자·테두리,
클릭 가로채기, 패밀리 혼용은 교정한다. 재사용률이나 파일 수를 시각 품질 PASS로 쓰지 않는다.

## UI-ACTION — 표시가 아니라 실제 도착 상태를 검증한다

각 행동은 `from → input → domain owner → state/result → destination → failure/recovery`로 연결한다.
signal/handler 존재나 메뉴 그림은 완료 증거가 아니다.

| action | 성공과 필수 반례 |
|---|---|
| new_game | 초기 상태·도입·플레이; 덮어쓰기 확인/취소, double 입력과 기존 저장 보호 |
| continue | 위치·진행·해금·자원 복원; no-save/corrupt/구버전/읽기 실패 |
| archive | 실제 목록·선택·상세·페이지/탭·복귀; 잠금·빈 목록·긴 본문·invalid ID |
| settings | 지원 옵션 적용·저장·재실행 유지; 취소/되돌리기·기본값·지원하지 않는 옵션 |
| exit / result_return | 저장 정책·실패 처리·정상 종료 또는 다음 흐름; 중복 보상·막다른 결과창 |
| dialogue_advance / tab_change | 본문 완성/다음/선택의 구분, 표시·scroll/focus 복원; 이중 처리·입력 누출 |

저장이 범위에 있으면 새 게임 → 상태 변경 → 저장 → 프로세스 종료 → 재실행 → continue를 검사한다.
UI는 도메인 피해·보상·저장 규칙을 재계산하지 않는다. 미지원 기능의 숨김/비활성은 승인된 표현을 사용한다.

## UI-IMAGE — 실제 원본 확인에서 제작·승인까지

외부 후보 구조의 프로젝트 정합화 단계에서 이미지 정본·승인 시안·candidate·Asset Catalog·기존 캡처를 읽고
실제 파일을 열어 픽셀을 확인한다. 이름·hash·치수만으로 봤다고 하지 않는다. 읽지 못하면 PIXEL_REVIEW_NOT_RUN이며
NO_NEW_IMAGE_FILE_REQUIRED로 바꾸지 않는다.

미제작 / 생성됨 / 승인 대기 / 승인됨 / 미연결 / 연결됨 / 실행 미검증을 분리하고 기존 승인 부품을 우선 재사용한다.
필요한 개별 모듈마다 consumer(현재 또는 명시적 계획), 역할·상태·규격·패밀리·slice·조합·검사 방법을 brief로 만든다.
노드가 없어도 계약이 충분하면 BRIEF_READY가 가능하지만 ASSET_READY/IMPLEMENTED는 아니다.
허용된 범위에서 이미지 모델로 후보를 만들고 검수·보존한다. user lock 후에만 기존 asset owner에
provenance, sha256, repository path, consumer와 상태군을 등록한다. 최종 자산 승인과 Blueprint final approval은 별개다.

## UI-EVIDENCE — 실제 화면 보관과 정확한 완료 상한

계획 시안은 목표 구성의 증거이지 runtime 증거가 아니다. 시각 변경을 구현했다면 실제 프로젝트의 인게임 캡처를
항상 보관한다. 필요한 대표 상태와 영향 있는 조합을 선정하고, 시간감이 수용 기준이면 영상/연속 프레임을 추가한다.
기존 `FRESH_RUNTIME_ARTIFACT_GATE`와 `RM-TOOL-004`를 재사용하며 새 캡처 앱·필수 JSON schema·고정 보관 용량을 강제하지 않는다.

```text
source_commit + build_or_run_id + project/worktree
+ scene/state + viewport/renderer/input + asset revision
+ capture_path + dimensions + sha256 + actual image readback
+ diagnostics + 재현 경로 + evidence_ceiling
```

repository 또는 관리되는 artifact 저장소에서 다시 회수·열람한다. artwork와 QA capture는 분리하며
검증에 필요한 유일한 캡처를 임시파일 정리로 삭제하지 않는다. 실제 입력/저장 시험, 캡처 픽셀 검토,
기계 테스트, Human/기기/출시 판정은 각각 기록한다. debug fixture는 일반 플레이 도달성의 증거가 아니다.
변경되지 않은 consumer의 과거 증거는 freshness와 적용 범위를 확인한 경우에만 재사용한다.

### Work → Blueprint → Codex → 검수

Work의 외부 벤치마크 → 후보 구조 → 프로젝트 fresh-read/정합화 → UI-FLOW/SKIN/MODULE/ACTION 명세
→ UI-IMAGE 개별 후보 제작·검수 → 정확한 Blueprint와 final approval → Codex exact-revision fresh-read
→ 승인 자산/데이터 구현 → 테스트·실제 입력·인게임 캡처 → 교정 → current owner/readback → post-merge 검사.

SPECIFIED / ASSET_READY / IMPLEMENTED / MACHINE_VERIFIED / RUNTIME_VERIFIED / USER_APPROVED를 분리한다.
승인 범위 안의 안전한 준비·검사·교정은 계속하고 핵심 의미·고위험 변경·최종 확정만 사용자에게 올린다.
5회 full-scope 적대적 검토는 각 회 실제 읽기·finding·교정 또는 blocker·회귀증거를 남긴다.
다섯 번의 작성자 검토를 독립 review로 보고하지 않는다.

### 채택과 cold-start

Base 본문을 프로젝트에 복사하지 않는다. 기존 entrypoint/owner에 채택한 source commit과 이 reference,
프로젝트의 UI/화면/자산/capture owner·범위·보호 결정·다음 작업을 연결한다. 기존 Base pin과 generated adapter는 보존한다.
새 채팅에서 entrypoint → 채택 reference → 실제 owner를 따라 cold-start readback한다.
로컬 준비, 미병합 PR, main 반영을 구분하며 미병합 adoption PR을 적용 완료로 보고하지 않는다.

## 공식 엔진 참고

- https://www.renpy.org/doc/html/gui.html — 대화/선택/저장 슬롯/Frame의 분리된 공식 샘플.
- https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html — 9-slice와 영역·margin·tile.
- https://docs.godotengine.org/en/stable/classes/class_tabcontainer.html — 탭 선택과 child Control 표시.
- https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html — 입력·focus 경로.

공식 문서의 stable 경로는 변한다. 구현 전 프로젝트 엔진 pin의 같은 API를 확인한다. 문서 조회는 runtime PASS가 아니다.
