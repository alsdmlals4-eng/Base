# Preferred Visual Style Reference Library

> 역할: 사용자가 반복적으로 선호한 시각 특성을 Base 공용 Reference로 구조화한다.
> 권위: `REFERENCE_ONLY · NOT_PROJECT_CANON · NOT_PROJECT_ASSET_APPROVED`
> 연결: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` → `PIXEL_ART_STYLE_SYSTEM.md` → 이 Library → 프로젝트 Art Bible / Visual Bible Decision
> Figma workspace: https://www.figma.com/design/AEYEulNSiobxpCZckun27I
> Figma image status: `BLOCKED_TRANSPORT` — 스타일군 페이지/평가 구조는 생성됐지만, 현재 연결의 raster upload 전송은 완료되지 않았다.

## 1. 목적과 권위 경계

이 Library는 “좋아 보였던 이미지 모음”을 프로젝트 기본 그림체로 자동 승격하지 않는다. 사용자가 선호한 결과에서 **재사용 가능한 시각 원리**를 추출하고, 프로젝트 작업 때 기존 Art Bible·Figma 승인 Reference·핵심 시스템과 비교할 수 있는 탐색 렌즈를 제공한다.

```text
USER_PREFERENCE_REFERENCE
→ reusable visual principles
→ project problem + current canon
→ at least 3 viable alternatives
→ benchmark / reference comparison
→ project-specific approval
```

고정 경계:

```text
REFERENCE_ONLY
PROJECT_ART_CANON_REMAINS_PROJECT_OWNED
NO_AUTOMATIC_PROJECT_STYLE_PROMOTION
```

- 이 문서의 `preferred`는 **사용자 선호 근거가 있음**을 뜻하며 품질 PASS·제품 채택·모든 프로젝트 기본값을 뜻하지 않는다.
- 한 프로젝트의 생성 시안을 다른 프로젝트의 승인 자산으로 복사하지 않는다.
- 특정 상용 작품·작가·스튜디오의 식별 가능한 스타일을 복제하는 지시로 사용하지 않는다.
- 프로젝트에 이미 잠긴 Art Bible이 있으면 그 정본이 우선하며, 이 Library는 재검토 재료일 뿐이다.

## 2. 최상위 평가축 3개

### 2.1 `AI_GENERATED_LOOK_REDUCTION`

이 항목은 **이미지의 AI 생성 여부를 판별하는 탐지기나 출처 판정이 아니다.** 생성·수작업 여부와 무관하게, 반복 제작 시 “규칙 없이 매번 다른 고밀도 이미지”처럼 보이게 만드는 관찰 가능한 위험을 줄이는 품질 Gate다.

강한 방향:

- Shape language, silhouette, edge/outline, palette role, material, lighting, ornament budget가 반복 가능한 규칙으로 설명된다.
- 캐릭터·배경·UI·VFX가 동일 세계의 재료·빛·형태 언어를 공유하되 역할 구분은 유지한다.
- 작은 장식보다 큰 형태·기능·시선 흐름이 먼저 결정된다.
- 이미지 안에 생성된 의미 텍스트를 굽지 않고 실제 UI/타이포그래피와 분리한다.
- 대표 이미지 1장이 아니라 두 번째·열 번째 같은 유형 자산에서 같은 규칙을 재현할 수 있다.

경고 신호:

- 이유 없는 micro-detail, 임의 장식, 과도한 입자·발광·표면 질감.
- 프레임마다 바뀌는 얼굴 비율·손·장비 구조·광원·재질.
- 캐릭터는 단순한데 배경만 과도하게 사진적이거나, UI만 다른 게임의 재질처럼 보이는 불일치.
- 기능과 무관한 문양·문자·소품이 빈 공간을 자동으로 채운다.
- 한 장의 키아트는 훌륭하지만 같은 스타일의 상태 변형·애니메이션·UI 확장이 불가능하다.

검수 질문:

```text
Can the rule be named?
Can the rule be repeated?
Can the rule survive asset #2 and #10?
Can the rule survive gameplay scale?
Can the rule survive text/UI/VFX integration?
```

### 2.2 `STYLE_CONSISTENCY_AND_READABILITY`

시각적 일관성은 모든 것을 같은 모양으로 만드는 것이 아니다. **공통 문법을 유지하면서 필요한 상태·역할·진영·행동 차이를 더 빨리 읽게 만드는 것**이 목표다.

필수 확인:

- 최종 표시 크기 silhouette test.
- grayscale/value hierarchy test.
- 색을 제거해도 핵심 상태가 구분되는지 확인.
- 캐릭터·배경·UI·VFX가 같은 시선을 경쟁하지 않는지 확인.
- 작은 모바일 화면, 16:9 PC, 카메라 확대/축소에서 정보 우선순위 유지.
- UI 상태·아이콘·텍스트가 장식과 재질 효과에 묻히지 않음.
- 반복 캐릭터/유닛에서 같은 픽셀 크기·edge rule·light direction·palette role 유지.
- 모션·VFX가 충돌 판정·다음 입력·위험 경고를 가리지 않음.

### 2.3 `WORLD_CORE_SYSTEM_FIT`

스타일은 세계관 mood board와 핵심 시스템을 동시에 지원해야 한다. “분위기와 잘 맞음”만으로는 부족하다.

```yaml
world_promise:
core_system_question:
visual_information_needed:
style_supports_world:
style_supports_decision:
style_hides_or_distorts:
production_fit:
```

- 무협의 절제·여백이 강점이어도 전술 판단 UI를 흐리게 만들면 UI 계층에는 그대로 적용하지 않는다.
- 오컬트 기록물 분위기가 좋아도 사건 단서·선택·위험 상태가 문서 질감에 묻히면 실패다.
- 다크 판타지 장식이 좋아도 다수 유닛의 역할 판독을 늦추면 전장에서는 축소하거나 제거한다.
- 핵심 시스템이 정보 완전성·예측을 요구하면 세부 묘사보다 telegraph·silhouette·state hierarchy를 우선한다.

## 3. Base 의사결정 계약 적용

이 Library 전용으로 별도 정책 ID를 만들지 않는다. 현행 Base `AGENTS.md`의 다음 계약을 그대로 적용한다.

```text
MINIMUM_VIABLE_ALTERNATIVES: 3
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS
```

프로젝트에서 스타일을 고를 때:

1. 현행 유지·비픽셀·픽셀·하이브리드·화면별 혼합 중 실제로 가능한 **최소 3개 materially distinct 후보**를 확보한다.
2. 최초 3개를 채웠다는 이유로 탐색을 닫지 않고, 승인 직전까지 더 나은 Reference·제작 파이프라인·표현법이 발견되는지 `BETTER_ALTERNATIVE_SEARCH`를 계속한다.
3. `LONG_TERM_PLAN_FIT_REQUIRED`에서 두 번째·열 번째 자산, 애니메이션, 모바일/PC, Figma 재사용, localization, accessibility, runtime cost, rollback까지 본다.
4. 중요한 L1+ 결정은 `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`로 전체 범위를 반복 재공격한다.
5. Base 후보 이름을 그대로 프로젝트 정본에 복사하지 않고, 프로젝트가 실제로 채택한 Visual Pillar·5축·금지 규칙·검증 결과만 기록한다.

## 4. Base 구조 대안 Trade Study

| 대안 | 내용 | 장점 | 약점 | 장기 적합성 | 판정 |
|---|---|---|---|---|---|
| A. Pixel-only preference catalog | 선호 이미지를 모두 도트/픽셀 계열로 묶음 | 단순하고 빠름 | 수묵·Noir UI·Dark Gold UI를 억지로 픽셀로 오분류 | LOW | REJECT |
| B. Flat mood-board labels | `무협`, `다크`, `예쁨`, `고급` 같은 분위기명만 저장 | 사람이 보기 쉬움 | 가독성·생산 파이프라인·시스템 적합성 재현이 약함 | MEDIUM-LOW | REJECT |
| C. Preferred family + existing Base axes | 선호 5군을 Reference Lens로 두고 기존 Pixel 5축·Art Guide와 결합 | 취향 보존, 프로젝트 독립성, 생산 규칙, 비교 가능성 | 기록 구조가 A/B보다 조금 복잡 | HIGH | **ADOPT** |
| D. Machine registry first | 선호를 JSON/YAML Registry로 먼저 고정 | 자동 검색·도구화에 유리 | 현재는 데이터보다 사람 시각 비교가 먼저이며 premature schema 위험 | MEDIUM | DEFER |

결정 직전 재탐색에서도 C보다 현재 요구에 강한 대안은 확인되지 않았다. C는 기존 Base Art/Pixels owner를 재사용하고, 새 broad Skill이나 두 번째 Art Bible을 만들지 않으며, 프로젝트가 각자 다른 결과를 선택할 수 있어 장기 확장성이 가장 높다.

## 5. 선호 스타일군 5종

### 5.1 Pixel Illustration Hybrid

```yaml
family_id: PIXEL_ILLUSTRATION_HYBRID
reference_status: REFERENCE_ONLY
pixel_strength: PIXEL_HYBRID_HIGH
production_cost: MEDIUM_TO_HIGH
consistency_difficulty: MEDIUM
readability_risk: MEDIUM
user_reference_sheet: FIGMA_PAGE_01_PIXEL_ILLUSTRATION_HYBRID
image_transport_status: BLOCKED_TRANSPORT
```

정의: 픽셀/도트의 형태 정리와 작은 캐릭터 판독성을 유지하면서, 배경·광원·공간 깊이·일러스트 밀도를 현대적으로 확장한다.

Visual DNA:

- 큰 cluster/silhouette가 작은 화면에서 먼저 읽힘.
- 디테일은 캐릭터 역할·재질·등급을 설명할 때만 추가.
- 배경은 더 풍부할 수 있지만 gameplay actor와 value/edge separation을 유지.
- UI는 sprite detail보다 정돈된 vector/text hierarchy를 우선할 수 있음.
- pixel scale과 anti-aliasing 규칙을 같은 자산군에서 임의 혼합하지 않음.

`AI_GENERATED_LOOK_REDUCTION`: 팔레트·광원 방향·재질 단계·픽셀/edge 규칙을 고정하면 강하다. 배경마다 무작위 세부를 채우거나 캐릭터마다 다른 해상도 감각을 쓰면 급격히 약해진다.

잘 맞는 문제: 전술 유닛, RPG field sprite, 수집/성장 캐릭터, pixel actor + 고밀도 배경, 현대적 조명과 픽셀 주체의 혼합.

피해야 할 사용: 모든 자산을 HD화해 animation cost를 폭증시키기, pixel 주체를 bloom/lighting이 가리기, 콘셉트 한 장의 고밀도를 실제 전장 sprite에 그대로 축소.

benchmark_disposition: `Dead Cells — ADAPT` 반복 애니메이션 retake 비용이 병목일 때 3D/렌더 보조 생산 원리를 검토하되, setup 비용과 프로젝트 룩을 별도 검증한다.
benchmark_disposition: `OCTOPATH TRAVELER II — ADAPT` pixel subject + depth/light/3D 공간 결합 원리는 참고하되 특정 상용작의 branded visual signature를 복제하지 않는다.

### 5.2 Chibi Epic Dark Fantasy

```yaml
family_id: CHIBI_EPIC_DARK_FANTASY
reference_status: REFERENCE_ONLY
pixel_strength: PIXEL_OR_ILLUSTRATION_OPTIONAL
production_cost: MEDIUM_TO_HIGH
consistency_difficulty: MEDIUM_HIGH
readability_risk: LOW_TO_MEDIUM
user_reference_sheet: FIGMA_PAGE_02_CHIBI_EPIC_DARK_FANTASY
image_transport_status: BLOCKED_TRANSPORT
```

정의: compact/chibi 비율의 즉시 판독성과 다크 판타지의 큰 위협·보스·에너지 대비를 결합한다.

Visual DNA:

- 머리·몸통·무기·대표 소품을 큰 덩어리로 고정.
- 캐릭터 귀여움보다 행동 방향과 직업 silhouette가 먼저 읽힘.
- 적·보스는 크기·형태·value로 위협을 분리하고, 무작위 뿔·사슬·불꽃을 계속 추가하지 않음.
- 유파/속성/VFX는 palette 역할과 shape motif를 공유하되 색만으로 구분하지 않음.

`AI_GENERATED_LOOK_REDUCTION`: 의상 파츠·무기 비율·장식 위치·얼굴 비율을 character sheet로 고정하고, 반복 포즈에서도 같은 anatomy shortcut을 유지한다.

잘 맞는 문제: 액션 로그라이트, 수집/성장, 직업/유파 차별화, 보스 중심 키아트와 gameplay sprite의 연결.

피해야 할 사용: key art 복잡도를 모든 gameplay frame에 강제, 배경/보스/VFX를 모두 최대 contrast로 만들어 플레이어를 묻기, 귀여움 때문에 세계관의 위험과 대가를 지우기.

benchmark_disposition: `Shovel Knight — ADOPT` 역할·실루엣·제한 팔레트·idle pose처럼 기능에서 형태를 시작하는 원리를 채택한다. 정확한 retro hardware 제한은 프로젝트 목적에 맞게 ADAPT한다.

### 5.3 Ink Wash Wuxia

```yaml
family_id: INK_WASH_WUXIA
reference_status: REFERENCE_ONLY
pixel_strength: NON_PIXEL_PREFERENCE_REFERENCE
production_cost: MEDIUM
consistency_difficulty: MEDIUM
readability_risk: MEDIUM
user_reference_sheet: FIGMA_PAGE_03_INK_WASH_WUXIA
image_transport_status: BLOCKED_TRANSPORT
```

정의: 수묵·종이·먹선·여백·산수·절제된 accent를 사용해 무협의 고요함, 긴장, 비장미와 시간성을 전달한다.

Visual DNA:

- neutral paper/ink field + 제한된 accent.
- negative space를 장식 부족이 아니라 시선/호흡 구조로 사용.
- silhouette와 calligraphic gesture를 작은 장식보다 우선.
- UI는 전통 소재를 쓰더라도 text/action hierarchy와 focus state를 명확히 유지.

`AI_GENERATED_LOOK_REDUCTION`: 붓질 방향·종이 texture 강도·산수의 depth/value 단계·장식 seal 규칙을 제한하면 일관성이 강해진다. 의미 없는 한자/문양 자동 생성은 금지한다.

잘 맞는 문제: 무협, 동양 판타지, 명상/대치, 서사 메뉴, 세계관 첫인상, 기록/도감의 특수 표면.

피해야 할 사용: 모든 UI를 붓글씨로 만들어 가독성 저하, gameplay object와 배경을 같은 먹 농도로 합치기, 장식 한자를 정보 텍스트로 사용.

benchmark_disposition: `Shovel Knight — ADAPT` 역사적 제약을 그대로 복제하지 않고, 제한된 시각 규칙이 cohesive identity를 만드는 원리만 차용한다.

### 5.4 Dark Gold UI

```yaml
family_id: DARK_GOLD_UI
reference_status: REFERENCE_ONLY
pixel_strength: CROSS_RENDER_UI_REFERENCE
production_cost: MEDIUM
consistency_difficulty: LOW_TO_MEDIUM
readability_risk: MEDIUM
user_reference_sheet: FIGMA_PAGE_04_DARK_GOLD_UI
image_transport_status: BLOCKED_TRANSPORT
```

정의: 어두운 value field에 제한된 금색/황동 accent, 프레임·아이콘·재질감을 사용해 고급감과 세계관 물성을 만드는 UI 언어다.

Visual DNA:

- 금색은 모든 장식이 아니라 **선택·제목·핵심 테두리·고급 상태**처럼 역할을 가진다.
- black-on-black을 피하고 panel/background/text의 value 단계가 분리된다.
- ornament density는 기능 위계보다 한 단계 아래.
- disabled/locked/selected/focus를 hue 하나로만 구분하지 않는다.
- 실제 typography와 icon set을 생성 이미지에서 분리한다.

`AI_GENERATED_LOOK_REDUCTION`: frame corner, stroke weight, metal roughness, bevel depth, glow strength, icon family를 토큰처럼 고정하고 임의 장식 생성을 막는다.

잘 맞는 문제: 다크 판타지, 대장간/금속, 마법 문서, 전술/전략의 premium shell, 기록/도감 UI.

피해야 할 사용: 모든 선을 금색으로 만들어 hierarchy 소실, 금박 texture가 작은 한글/숫자를 침범, hover/selected마다 다른 장식 motif를 새로 생성.

benchmark_disposition: `Hades — ADOPT` UI/HUD가 gameplay requirement와 함께 설계되고, 대량 icon family가 stylistically consistent해야 하며, 패치 과정에서 VFX/UI clarity·text readability를 지속 수정하는 원리를 채택한다. Hades의 고유 미술 표현 자체는 복제하지 않는다.

### 5.5 Noir Archive / Investigation Interface

```yaml
family_id: NOIR_ARCHIVE_INVESTIGATION_INTERFACE
reference_status: REFERENCE_ONLY
pixel_strength: NON_PIXEL_OR_PIXEL_NOIR_OPTIONAL
production_cost: MEDIUM
consistency_difficulty: MEDIUM
readability_risk: MEDIUM_HIGH
user_reference_sheet: FIGMA_PAGE_05_NOIR_ARCHIVE_INVESTIGATION
image_transport_status: BLOCKED_TRANSPORT
```

정의: 기관 기록, 사건 파일, 조사 보드, 오래된 문서/기기, 제한된 경고색을 정보 architecture와 결합하는 interface family다.

Visual DNA:

- 문서·기록·기관 소재가 실제 navigation/information role과 연결됨.
- 사건 번호, 상태, 위험, 단서, 연결 관계가 decoration보다 우선.
- dark field에서 text/panel/value separation을 강하게 유지.
- danger accent는 제한적으로 사용하고 항상 shape/text/icon redundancy를 제공.
- archive texture는 content legibility를 침범하지 않는 강도로 제한.

`AI_GENERATED_LOOK_REDUCTION`: generated pseudo-text를 제거하고 실제 structured text layer로 교체하며, stamp/document/device material을 제한된 set으로 반복한다.

잘 맞는 문제: 조사, 추리, 오컬트, 정부/기관, case management, evidence linking, rule deduction.

피해야 할 사용: 모든 화면을 낡고 어둡게 만들어 검색/입력/선택 속도 저하, fake text를 분위기 장식으로 과다 사용, 사건 정보보다 frame ornament가 먼저 보임.

benchmark_disposition: `Into the Breach — ADOPT` 핵심 판단이 예측·정보 판독에 의존할 때 적 행동과 결과 정보를 명확히 telegraph하는 원리를 채택한다. 장르/미술 외형이 아니라 정보 설계 원리를 참조한다.

## 6. 현업·성공작 Benchmark

외부 사례는 Base 요구사항 정본이 아니다. 각 사례에서 **재현 가능한 생산/가독성 원리만** `ADOPT / ADAPT / REJECT`로 판정한다.

| 작품/팀 | 확인한 원리 | 현재 Library 적용 | 판정 |
|---|---|---|---|
| Shovel Knight / Yacht Club Games | gameplay function에서 silhouette·pose·palette를 시작하고, 제한을 통해 cohesion/readability 확보 | 역할 우선, 제한된 palette/shape rule, animation 전 asset list | ADOPT/ADAPT |
| Dead Cells / Motion Twin art pipeline | 작은 팀에서 반복 animation·retake 비용을 줄이기 위해 3D 기반 pose/animation을 low-res pixel result로 변환 | hybrid pipeline이 수명주기 비용을 실제로 줄일 때만 사용 | ADAPT |
| OCTOPATH TRAVELER II / Square Enix | retro pixel art와 3DCG를 결합한 HD-2D 표현 | pixel actor + depth/light hybrid를 선택적 후보로 유지 | ADAPT |
| Hades / Supergiant Games | 수많은 icon/UI asset의 stylistic consistency, gameplay clarity, performance/accessibility와 UI art의 결합 | Dark Gold UI를 장식 모음이 아니라 system UI family로 운영 | ADOPT |
| Into the Breach / Subset Games | 적 공격이 telegraphed되고 turn decision이 정보 가독성에 의존 | 전술/조사 UI에서 prediction/decision 정보가 분위기보다 우선 | ADOPT |

원출처:

- Yacht Club Games, *Creating a Shovel Knight Character Sprite*: https://www.yachtclubgames.com/blog/creating-a-shovel-knight-character-sprite
- Yacht Club Games, *Breaking the NES*: https://www.yachtclubgames.com/blog/breaking-the-nes
- Game Developer, Thomas Vasseur, *Art Design Deep Dive: Using a 3D pipeline for 2D animation in Dead Cells*: https://www.gamedeveloper.com/art/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-
- Square Enix, *OCTOPATH TRAVELER II*: https://www.square-enix-games.com/games/octopath-traveler-ii
- Supergiant Games, UI illustrator role: https://www.supergiantgames.com/blog/ui-illustrator/
- Supergiant Games, Hades II patch notes: https://www.supergiantgames.com/blog/hades2-patch-notes/
- Subset Games, *Into the Breach*: https://subsetgames.com/itb.html

## 7. 사용자 제공 Reference Provenance

아래 입력은 사용자가 현재 대화에서 제공한 생성 시안이다. Base는 원본의 고유 캐릭터·로고·문구를 다른 작품에 복제하지 않고, **shape/value/material/UI hierarchy/production principle**만 추출한다.

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

Figma에는 `00_START_HERE`와 5개 스타일군 페이지 구조를 생성했다. 현재 연결 환경에서 `mcp.figma.com` raster POST가 DNS 단계에서 실패했고 Plugin API raster 생성도 지원되지 않아 이미지 bytes 배치는 `BLOCKED_TRANSPORT`로 남긴다. 이 제한은 GitHub의 스타일 원리·출처 hash 기록을 무효화하지 않지만, **Figma에서 실제 이미지를 볼 수 있다고 주장하면 안 된다.** 전송 경로가 복구되면 위 SHA-256을 기준으로 원본/파생 sheet를 대조한 뒤 이미지만 채운다.

## 8. 프로젝트 사용 순서

```text
project current Art Bible / Figma approved reference
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
→ selected project rules only into Art Bible / Visual Bible
```

이 Library의 5개 family를 후보 5개로 자동 제출하지 않는다. 프로젝트 문제에 실질적으로 다른 결과를 만드는 후보만 대안으로 센다.

## 9. `REVIEW_TRIGGERS`

다음 중 하나가 발생하면 선택 스타일을 재검토한다.

```text
REVIEW_TRIGGERS
```

- 두 번째·열 번째 같은 유형 자산에서 얼굴·실루엣·edge·palette·재질·광원이 흔들림.
- 반복 생성 결과에서 임의 장식·pseudo-text·해부/구조 왜곡·과도한 micro-detail이 증가함.
- 실제 gameplay scale, mobile, camera zoom에서 핵심 역할·상태가 읽히지 않음.
- UI/VFX/배경이 핵심 입력·위험·선택 정보와 경쟁함.
- localization 또는 긴 한국어/영어가 decorative UI에 수용되지 않음.
- animation/VFX 변형 제작비 또는 retake 비용이 계획보다 커짐.
- 프로젝트 core loop, world tone, camera, platform, art production capacity가 변경됨.
- 더 낮은 수명주기 비용으로 같은 또는 더 높은 품질을 내는 실질 대안이 발견됨.
- 신규 현업 사례·도구·기법이 기존 선택의 장기 적합성을 약화시키는 증거를 제공함.
- 기존 승인 Art Bible/Figma Reference가 갱신됨.

재검토는 “새 스타일이 더 예뻐 보인다”만으로 자동 교체하지 않는다. 동일한 3개 최상위 평가축, 최소 3개 실질 대안, 장기 비용, rollback, 실제 화면 검증을 다시 적용한다.

## 10. 완료·증거 한계

- 이 문서 추가는 프로젝트별 그림체 확정이 아니다.
- 현업 사례 조사와 Reference 분석은 실제 게임 runtime, 인간 가독성, 접근성, 성능 검증을 대신하지 않는다.
- Figma page structure creation은 실제 raster Reference 업로드 증거가 아니다. 현재 상태는 `BLOCKED_TRANSPORT`다.
- 프로젝트 채택 시에는 실제 대표 장면과 두 번째 같은 유형 자산을 만들어 검증해야 한다.
- “AI 티 감소”는 visual-system consistency 목표이지 AI provenance detector가 아니다.
