# Preferred Visual Style Reference Library

> 역할: 사용자가 반복적으로 선호한 시각 특성과 검증된 현업 원리를 Base 공용 Reference로 구조화한다.
> 권위: `REFERENCE_ONLY · NOT_PROJECT_CANON · NOT_PROJECT_ASSET_APPROVED`
> 연결: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` → `PIXEL_ART_STYLE_SYSTEM.md` → 이 Library → 프로젝트 Visual Decision
> 지속 탐색: `VISUAL_STYLE_SOURCE_RADAR.md` — 기존 `PERIODIC_SPECIALTY_SOURCE_RADAR.md`의 bounded child reference
> 프로젝트 작업면: `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`의 repository asset manifest/catalog와 exact-SHA human projection. V4 Notion exception은 명시적으로 승인·범위가 정해진 경우에만 사용한다.

## 1. 목적과 권위 경계

이 Library는 “좋아 보였던 이미지 모음”을 모든 프로젝트의 기본 그림체로 자동 승격하지 않는다. 사용자 선호 결과와 외부 성공 사례에서 **재사용 가능한 시각 원리**를 추출하고, 프로젝트 작업 때 현재 Project canon·승인 Reference·핵심 시스템과 비교할 수 있는 탐색 렌즈를 제공한다.

```text
USER_PREFERENCE_REFERENCE | PROFESSIONAL_REFERENCE
→ reusable visual principles
→ project problem + current canon
→ MINIMUM_VIABLE_ALTERNATIVES: 3
→ benchmark + counterexample + production comparison
→ project-specific approval
```

고정 경계:

```text
REFERENCE_ONLY
PROJECT_ART_CANON_REMAINS_PROJECT_OWNED
NO_AUTOMATIC_PROJECT_STYLE_PROMOTION
PROJECT_RELATION_REQUIRED
```

- `preferred`는 사용자 선호 근거가 있다는 뜻이며 품질 PASS·제품 채택·모든 프로젝트 기본값을 뜻하지 않는다.
- 한 프로젝트의 생성 시안을 다른 프로젝트의 승인 자산으로 복사하지 않는다.
- 특정 상용 작품·작가·스튜디오의 식별 가능한 스타일을 복제하는 지시로 사용하지 않는다.
- 이미 잠긴 프로젝트 Visual/Art canon이 있으면 그 정본이 우선한다.
- 외부 성공작은 전체 외형 복제 대상이 아니라 `ADOPT / ADAPT / REJECT`할 제작·가독성 원리를 찾는 근거다.

## 2. 사용자 선호 Reference overview

![Preferred visual style overview](reference-images/preferred-visual/preferred-visual-style-overview.jpg)

```yaml
overview_status: REFERENCE_ONLY
derivative_type: DERIVED_CONTACT_SHEET
canonical_path: docs/knowledge/game-development/reference-images/preferred-visual/preferred-visual-style-overview.jpg
source_scope: CURRENT_USER_PROVIDED_GENERATED_REFERENCES_U01_TO_U13
source_assets_promoted: false
project_asset_approval: false
notion_sync_role: REFERENCE_LIBRARY_SEED
```

이 overview는 원본 13장을 저용량 비교용으로 재배치한 파생 Reference다. 원본의 제품 사용권이나 프로젝트 승인 상태를 새로 만들지 않는다. 원본 식별은 아래 SHA-256 표를 사용한다.

## 3. 최상위 평가축 3개

### 3.1 `AI_GENERATED_LOOK_REDUCTION`

이 항목은 AI 생성 여부를 판별하는 탐지기가 아니다. 생성·수작업 여부와 무관하게, **규칙 없이 매번 다른 고밀도 이미지처럼 보이는 관찰 가능한 결함**을 줄이는 품질 Gate다.

강한 방향:

- Shape language, silhouette, edge/outline, palette role, material, lighting, ornament budget가 반복 가능한 규칙으로 설명된다.
- 작은 장식보다 큰 형태·기능·시선 흐름을 먼저 결정한다.
- 의미 텍스트는 이미지에 굽지 않고 실제 UI/타이포그래피로 분리한다.
- 얼굴 비율·손·장비 구조·광원·재질이 같은 자산군 안에서 이유 없이 흔들리지 않는다.
- 대표 이미지 1장이 아니라 두 번째·열 번째 같은 유형 자산에서도 같은 규칙을 재현할 수 있다.

경고 신호:

- 목적 없는 micro-detail, 임의 장식, 과도한 입자·발광·표면 질감.
- 캐릭터는 단순한데 배경만 과도하게 사진적이거나 UI만 다른 게임처럼 보이는 불일치.
- pseudo-text, 무의미한 문양·한자·소품으로 빈 공간을 자동 채움.
- 키아트 한 장은 강하지만 상태 변형·애니메이션·UI 확장이 불가능함.

### 3.2 `STYLE_CONSISTENCY_AND_READABILITY`

일관성은 모든 것을 같은 모양으로 만드는 것이 아니다. **공통 시각 문법을 유지하면서 역할·진영·상태·행동 차이를 더 빨리 읽게 하는 것**이 목표다.

- 실제 표시 크기 silhouette / thumbnail test.
- grayscale/value hierarchy와 색 제거 상태 구분.
- 캐릭터·배경·UI·VFX의 시선 경쟁 방지.
- 모바일/PC/카메라 확대·축소에서 정보 우선순위 유지.
- 반복 캐릭터·유닛의 pixel/edge/light/palette 규칙 일치.
- 모션·VFX가 충돌 판정·다음 입력·위험 경고를 가리지 않음.

### 3.3 `WORLD_CORE_SYSTEM_FIT`

스타일은 세계관 mood와 핵심 시스템을 동시에 지원해야 한다. “분위기가 맞는다”만으로는 부족하다.

```yaml
world_promise:
core_system_question:
visual_information_needed:
style_supports_world:
style_supports_decision:
style_hides_or_distorts:
production_fit:
```

예를 들어 수묵 무협이 아름다워도 전술 판단을 흐리면 전투 UI에 그대로 쓰지 않는다. 오컬트 기록물 질감이 단서 판독을 늦추면 질감을 줄인다. 다크 판타지 장식이 다수 유닛 역할 판독을 늦추면 전장에서는 제거한다.

## 4. Base 의사결정 계약

```text
MINIMUM_VIABLE_ALTERNATIVES: 3
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS
REVIEW_TRIGGERS
```

프로젝트에서 실제 그림체를 결정할 때는 현행 유지·비픽셀·픽셀·하이브리드·화면별 혼합 중 가능한 최소 3개 **materially distinct** 후보를 확보한다. 최초 후보를 지키는 것이 아니라 결정 직전까지 더 나은 Reference·제작 파이프라인·표현법을 탐색한다.

`LONG_TERM_PLAN_FIT_REQUIRED`에서는 첫 대표 이미지가 아니라 반복 자산, 애니메이션, PC/mobile, Notion 재사용, localization, accessibility, runtime cost, source/rights, rollback까지 본다.

## 5. Library 구조 Trade Study

| 대안 | 내용 | 장점 | 약점 | 장기 적합성 | 판정 |
|---|---|---|---|---|---|
| A. Pixel-only preference catalog | 선호 이미지를 모두 도트/픽셀로 묶음 | 단순 | 수묵·Noir·Dark Gold를 오분류 | LOW | REJECT |
| B. Flat mood-board labels | 무협·다크·고급 같은 분위기명만 저장 | 보기 쉬움 | 가독성·생산 규칙·시스템 적합성 약함 | MEDIUM-LOW | REJECT |
| C. Preferred family + existing Base axes | 선호 family를 Lens로 두고 Art Guide·Pixel 5축과 결합 | 취향·생산 규칙·프로젝트 독립성 동시 보존 | 약간 더 구조적 | HIGH | **ADOPT** |
| D. Machine registry first | JSON/YAML Registry부터 고정 | 자동화에 유리 | premature schema 위험 | MEDIUM | DEFER |

## 6. 선호 스타일군

### 6.1 Pixel Illustration Hybrid

```yaml
family_id: PIXEL_ILLUSTRATION_HYBRID
reference_status: REFERENCE_ONLY
pixel_strength: PIXEL_HYBRID_HIGH
production_cost: MEDIUM_TO_HIGH
consistency_difficulty: MEDIUM
readability_risk: MEDIUM
user_reference_sheet: BASE_OVERVIEW_AND_NOTION_REFERENCE_LIBRARY
```

픽셀의 형태 정리와 작은 캐릭터 판독성을 유지하면서 배경·광원·공간 깊이·일러스트 밀도를 현대적으로 확장한다. 큰 cluster/silhouette를 먼저 읽히게 하고, pixel scale과 anti-aliasing 규칙을 같은 자산군에서 임의 혼합하지 않는다.

benchmark_disposition: `Dead Cells — ADAPT` 반복 animation/retake 비용이 병목일 때 3D/렌더 보조 생산 원리를 검토한다.
benchmark_disposition: `OCTOPATH TRAVELER II — ADAPT` pixel subject + depth/light/3D 공간 결합 원리만 참고한다.

### 6.2 Chibi Epic Dark Fantasy

```yaml
family_id: CHIBI_EPIC_DARK_FANTASY
reference_status: REFERENCE_ONLY
pixel_strength: PIXEL_OR_ILLUSTRATION_OPTIONAL
production_cost: MEDIUM_TO_HIGH
consistency_difficulty: MEDIUM_HIGH
readability_risk: LOW_TO_MEDIUM
user_reference_sheet: BASE_OVERVIEW_AND_NOTION_REFERENCE_LIBRARY
```

compact/chibi 비율의 즉시 판독성과 다크 판타지의 위협·보스·에너지 대비를 결합한다. 머리·몸통·무기·대표 소품의 큰 덩어리를 고정하고, 적·보스의 무작위 뿔·사슬·불꽃 증식을 금지한다.

benchmark_disposition: `Shovel Knight — ADOPT/ADAPT` gameplay intent에서 silhouette·pose·palette를 시작하고 제한으로 cohesion을 만드는 원리를 채택한다.

### 6.3 Ink Wash Wuxia

```yaml
family_id: INK_WASH_WUXIA
reference_status: REFERENCE_ONLY
pixel_strength: NON_PIXEL_PREFERENCE_REFERENCE
production_cost: MEDIUM
consistency_difficulty: MEDIUM
readability_risk: MEDIUM
user_reference_sheet: BASE_OVERVIEW_AND_NOTION_REFERENCE_LIBRARY
```

수묵·종이·먹선·여백·산수·제한 accent로 무협의 고요함과 비장미를 전달한다. 붓질 방향·종이 texture 강도·산수 depth/value·seal 사용 규칙을 제한하고 의미 없는 한자 자동 생성을 금지한다.

benchmark_disposition: `Shovel Knight — ADAPT` 제한된 시각 규칙이 cohesive identity를 만든다는 일반 원리만 가져온다.

### 6.4 Dark Gold UI

```yaml
family_id: DARK_GOLD_UI
reference_status: REFERENCE_ONLY
pixel_strength: CROSS_RENDER_UI_REFERENCE
production_cost: MEDIUM
consistency_difficulty: LOW_TO_MEDIUM
readability_risk: MEDIUM
user_reference_sheet: BASE_OVERVIEW_AND_NOTION_REFERENCE_LIBRARY
```

어두운 value field와 제한된 금색/황동 accent로 고급감과 세계관 물성을 만든다. 금색은 선택·제목·핵심 테두리·고급 상태처럼 역할을 가져야 하며 모든 선을 금색으로 만들지 않는다.

benchmark_disposition: `Hades — ADOPT` UI art를 gameplay requirement·icon family consistency·clarity와 함께 관리하는 생산 원리를 채택하고 고유 미술 표현은 복제하지 않는다.

### 6.5 Noir Archive / Investigation Interface

```yaml
family_id: NOIR_ARCHIVE_INVESTIGATION_INTERFACE
reference_status: REFERENCE_ONLY
pixel_strength: NON_PIXEL_OR_PIXEL_NOIR_OPTIONAL
production_cost: MEDIUM
consistency_difficulty: MEDIUM
readability_risk: MEDIUM_HIGH
user_reference_sheet: BASE_OVERVIEW_AND_NOTION_REFERENCE_LIBRARY
```

기관 기록·사건 파일·조사 보드·오래된 문서/기기·제한 경고색을 information architecture와 결합한다. generated pseudo-text를 실제 structured text layer로 교체하고 archive texture가 content legibility를 침범하지 않게 한다.

benchmark_disposition: `Into the Breach — ADOPT` 핵심 판단이 예측에 의존할 때 telegraph와 결과 정보가 분위기보다 우선한다는 원리를 채택한다.

## 7. 현업·성공작 Benchmark

| 작품/팀 | 관찰 원리 | Library 적용 | 판정 |
|---|---|---|---|
| Shovel Knight / Yacht Club Games | gameplay intent → concept → pixel model, limited colors, silhouette와 idle pose 정리 | 역할 우선·제한된 visual grammar | ADOPT/ADAPT |
| Dead Cells / Motion Twin | 반복 animation/retake를 감당하기 위한 3D-assisted 2D production | lifecycle cost가 실제 감소할 때만 hybrid 사용 | ADAPT |
| OCTOPATH TRAVELER II / Square Enix | pixel art와 3D/depth/light 결합 | depth-lit hybrid 후보 | ADAPT |
| Hades / Supergiant Games | UI/icon family를 gameplay clarity와 함께 생산 | Dark Gold UI를 system family로 관리 | ADOPT |
| Into the Breach / Subset Games | 예측 가능한 적 행동과 전술 정보의 명확성 | prediction/decision readability 우선 | ADOPT |

원출처·현업 자료는 `VISUAL_STYLE_SOURCE_RADAR.md`의 최신성·원출처 역추적 규칙으로 재검증한다. 특정 작품의 외형 전체를 스타일 프롬프트로 사용하지 않는다.

## 8. 사용자 제공 Reference provenance

공통 상태:

```text
USER_PROVIDED_GENERATED_REFERENCE
REFERENCE_ONLY
NOT_PROJECT_CANON
NOT_PROJECT_ASSET_APPROVED
```

| ID | 원본 파일명 | SHA-256 | 주요 관찰군 |
|---|---|---|---|
| U01 | `ChatGPT Image 2026년 8월 11일 오후 09_10_09.png` | `1a6945d2e70791bb5017eeb63e21fe573a5af628fcd277ec00a82d70859af268` | Ink Wash Wuxia |
| U02 | `ChatGPT Image 2026년 8월 11일 오후 09_20_47.png` | `d3c52dfd2b337a71ded7b757f66f56c76088002a291d0afe88f8603de1e4870b` | Chibi Epic Dark Fantasy |
| U03 | `ChatGPT Image 2026년 8월 11일 오후 04_33_39.png` | `9ab7a291cf71163cdf40242a64c5f4763ecbed4c0a5080de80e3f9eaba180139` | Chibi Epic Dark Fantasy |
| U04 | `ChatGPT Image 2026년 8월 11일 오후 05_06_17.png` | `ce72126fcdd6dbb2f045d6db4a69e883f8bc8f2f44585b2f0c28d98eed91dd20` | Chibi Epic Dark Fantasy |
| U05 | `ChatGPT Image 2026년 8월 1일 오전 04_34_53.png` | `1a9fcb46c255ff0b7141acc69b3c08371dfea4582d7b911980d36151ab206b4c` | Dark Gold UI |
| U06 | `ChatGPT Image 2026년 8월 11일 오후 04_36_42.png` | `4d2feaa9bfb4ba05e12d72784083ad3df8d0e9916f0bb3f4cb624920532401df` | Noir Archive / Investigation Interface |
| U07 | `ChatGPT Image 2026년 8월 11일 오후 05_42_02.png` | `a3a222cdfad0410b7dd5384644702138163a8ed83dcb8c99417e314c25aa4c48` | Noir Archive / Investigation Interface |
| U08 | `ChatGPT Image 2026년 8월 9일 오후 07_55_00.png` | `868ded6653d3153f94f2ce60c0595bb2800fec3df050a34c7c3e30b03ead1f67` | Noir Archive / Investigation Interface |
| U09 | `f1b9a324-4e5e-467d-982c-a6fc6a5e8cc2(1).png` | `68398bd3ca5b103a4197b09609480af1da4a040d3c0a0625a948201ef499ff0a` | Pixel Illustration Hybrid, Dark Gold UI |
| U10 | `ChatGPT Image 2026년 8월 1일 오전 05_25_54(1).png` | `bd43f951a17a34cbf4c967541314f0eda84a7c77209fae3d3c94f50d6d9e88bf` | Pixel Illustration Hybrid, Dark Gold UI |
| U11 | `2aad1d9f-2b89-473a-aea0-486402989eb2.png` | `4e82032535a4eac9d1e09012ef468355613a6dff79de15c6b2ffb616864135cf` | Pixel Illustration Hybrid |
| U12 | `생성된 이미지 1 (1)(3).png` | `da07d76e2037fd438ab70e9dc0abf65bdfbcf073ff6d4eb272ae923d4e9fdb6e` | Pixel Illustration Hybrid |
| U13 | `92fa25e2-c1a9-41d2-9b16-a4eaa40c1fc2.png` | `c13422f47c0ba6a7cd70517bd281c81742b652aa917ef4048d342641bdc6ae1a` | Pixel Illustration Hybrid, Dark Gold UI |

## 9. `CONTINUOUS_STYLE_DISCOVERY`

이 Library는 5개 family에서 닫히지 않는다. 새 스타일·새 제작법·새 성공 사례는 기존 Base Source discovery 경로를 재사용한다.

```text
CONTINUOUS_STYLE_DISCOVERY
→ UNCAPPED_CANDIDATE_INTAKE
→ ORIGINAL_SOURCE_BACKTRACE
→ evidence / rights / freshness classification
→ STYLE_FAMILY_MATCH | NEW_FAMILY_CANDIDATE
→ AI_GENERATED_LOOK_REDUCTION
→ STYLE_CONSISTENCY_AND_READABILITY
→ WORLD_CORE_SYSTEM_FIT
→ benchmark + counterexample
→ ADOPT | ADAPT | TEST | REFERENCE_ONLY | AVOID | IGNORE
→ approved Base reference delta
```

운영 원칙:

- 후보 수에 임의 상한을 두지 않는다. 후보 수가 곧 채택 수는 아니다.
- Pinterest·검색 썸네일·리포스트는 discovery surface일 수 있지만 `ORIGINAL_SOURCE_BACKTRACE` 뒤 원작자·개발사·GDC·공식 문서·원 게시물로 되돌린다.
- 기존 family로 충분히 설명되면 `STYLE_FAMILY_MATCH`로 흡수하고 이름만 다른 family를 늘리지 않는다.
- 기존 family에 넣으면 핵심 제작 문법·가독성 위험·세계관/시스템 역할이 왜곡되는 경우에만 `NEW_FAMILY_CANDIDATE`를 연다.
- 실제 스캔·근거 등급·PR 생명주기는 `VISUAL_STYLE_SOURCE_RADAR.md`와 상위 `PERIODIC_SPECIALTY_SOURCE_RADAR.md`를 따른다.

## 10. Notion Reference sync contract

Base Reference의 repository 원본을 자동으로 모든 프로젝트 Asset Master에 복제하지 않는다. 프로젝트에서 실제로 채택 검토할 때만 올바른 `Project` relation과 `Record Type: REFERENCE`로 연결한다.

```text
repository REFERENCE_ONLY source
→ Project selection
→ correct Project relation
→ Asset & Knowledge Master / REFERENCE
→ source provenance + rights boundary
→ attach preview when useful
→ NOTION_READBACK_REQUIRED
→ fetch target and verify Project / Preview / Status
→ REFERENCE_SYNC_READBACK_VERIFIED
```

Notion 파일 업로드·교체는 성공 응답만으로 완료가 아니다. target fetch/readback으로 예상 file/preview/version을 확인한다. 프로젝트에 채택하지 않은 Base Reference는 repository Library에 그대로 두며 Project canon으로 승격하지 않는다.

## 11. 프로젝트 사용 순서

```text
project current canon + APPROVED_VISUAL_REFERENCE
→ player emotion + core-system visual question
→ Base Art Guide
→ Pixel Style System (if relevant)
→ Preferred Visual Style Reference Library
→ MINIMUM_VIABLE_ALTERNATIVES: 3
→ benchmark / user-reference principle extraction
→ AI_GENERATED_LOOK_REDUCTION
→ STYLE_CONSISTENCY_AND_READABILITY
→ WORLD_CORE_SYSTEM_FIT
→ BETTER_ALTERNATIVE_SEARCH until decision
→ LONG_TERM_PLAN_FIT_REQUIRED
→ full adversarial re-review
→ user project approval
→ selected project rules only into Project records
```

이 Library의 family 수를 후보 수로 자동 계산하지 않는다. 프로젝트 문제에 실질적으로 다른 결과를 만드는 후보만 대안으로 센다.

## 12. `REVIEW_TRIGGERS`

다음 중 하나가 발생하면 선택 스타일을 재검토한다.

- 두 번째·열 번째 같은 유형 자산에서 얼굴·실루엣·edge·palette·재질·광원이 흔들림.
- 임의 장식·pseudo-text·해부/구조 왜곡·과도한 micro-detail이 증가함.
- gameplay scale/mobile/camera zoom에서 핵심 역할·상태가 읽히지 않음.
- UI/VFX/배경이 입력·위험·선택 정보와 경쟁함.
- localization이 decorative UI에 수용되지 않음.
- animation/VFX retake 비용이 계획보다 커짐.
- core loop, world tone, camera, platform, production capacity가 변경됨.
- 더 낮은 수명주기 비용으로 같거나 더 높은 품질을 내는 대안이 발견됨.
- 신규 현업 사례·도구·기법이 기존 선택의 장기 적합성을 약화시키는 증거를 제공함.
- 기존 Project canon 또는 승인 Reference가 갱신됨.

재검토는 “새 스타일이 더 예뻐 보인다”만으로 자동 교체하지 않는다. 동일한 세 평가축, 최소 3개 실질 대안, 장기 비용, rollback, 실제 화면 검증을 다시 적용한다.

## 13. 증거 한계

- 이 Library 추가는 프로젝트별 그림체 확정이 아니다.
- 현업 사례 조사와 Reference 분석은 실제 runtime·사람 가독성·접근성·성능 검증을 대신하지 않는다.
- Notion page/image upload 성공은 Project runtime sync 성공과 다르며 `NOTION_READBACK_REQUIRED`를 거쳐야 한다.
- 프로젝트 채택 시 대표 장면뿐 아니라 두 번째 같은 유형 자산을 만들어 반복 생산성을 검증한다.
- `AI_GENERATED_LOOK_REDUCTION`은 visual-system consistency 목표이지 AI provenance detector가 아니다.
