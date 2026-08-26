# 아트 디렉션·에셋 기획 Guide

## 1. 목적

이 Guide는 “예쁜 그림을 만든다”가 아니라 **플레이어 경험·정보 전달·게임 정체성·제작성·시장 첫인상을 하나의 시각 체계로 연결하는 방법**을 설명한다.

실행 책임은 `designing-art-prompts-and-technique-cards`, `auditing-and-refining-ui-art`, `designing-vertical-slices`, `reviewing-and-validating-project-changes`, 프로젝트 아트·UX Skill이 가진다.

현업 참고:

- Art Direction은 key art만이 아니라 예술·창작·기술·마케팅 조건을 연결한 visual identity framework가 필요하다: https://gdcvault.com/free/gdc-23/play/1028731/Art-Direction-Summit-Building-a
- Graphic design은 typography·iconography·logo·colour·UI·key art·motion을 잇는 visual signature를 만든다: https://www.gdcvault.com/play/1023276/Art-Direction-Graphic-Design-is
- Pre-production은 Art Bible·평가 지점·생산 진입 조건을 명확히 해야 한다: https://gdcvault.com/play/1034593/Art-Direction-Summit-Pre-Production
- 대규모 외주 자산 생산은 상세 brief와 품질 보호 파이프라인이 필요하다: https://www.gdcvault.com/play/1023575/Art-Direction-Bootcamp-Guerrilla-Games

## 2. 아트 문제 정의

이미지를 만들기 전에 다음을 고정한다.

```yaml
player_experience:
information_role:
fantasy_and_emotion:
market_first_impression:
mascot_or_symbol:
target_platform_and_viewing_distance:
production_capacity:
asset_reuse_and_variation:
technical_constraints:
approval_decision:
```

질문:

- 플레이어가 첫 3초에 무엇을 알아야 하는가?
- 플레이 중 무엇을 구분·예측·선택해야 하는가?
- 어떤 감정·판타지·세계관을 즉시 느껴야 하는가?
- 상점 썸네일·캡슐·영상에서 무엇이 기억점인가?
- 마스코트·상징은 플레이·서사·UI·홍보에서 어떤 역할을 하는가?
- 실제 인게임 크기와 거리는 얼마인가?
- 같은 유형의 자산을 몇 개 반복 제작해야 하는가?
- 혼자·AI·외주·에셋스토어 중 무엇이 적합한가?

키워드만 있는 “귀엽고 아름다운 판타지”는 Art Direction 계약이 아니다.

### 2.0.1 Pixel Art 후보 Reference

픽셀 아트가 프로젝트의 주 스타일·부분 스타일 후보라면 이 Guide의 플레이어 경험·Visual Pillar·실루엣·Color·Value·Composition 판단을 그대로 유지한 채 `PIXEL_ART_STYLE_SYSTEM.md`와 `PIXEL_ART_VISUAL_REFERENCE_GALLERY.md`를 **조건부 Reference**로 읽는다.

```text
ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md
→ PIXEL_ART_STYLE_SYSTEM.md
→ PIXEL_ART_VISUAL_REFERENCE_GALLERY.md
→ 프로젝트별 최소 3개 실질 후보 비교
→ 프로젝트 Art Bible/Decision 승인
```

Base의 Pixel Art Preset과 외부 예시는 프로젝트 정본이 아니며, 기존 승인 Art Bible을 자동 교체하거나 `PROJECT_ASSET_APPROVED`를 부여하지 않는다. 프로젝트 선택 시에는 현행 유지·비픽셀·하이브리드도 유효 대안이면 함께 비교하고, 결정 직전 더 나은 대안을 재탐색하며 장기 제작비·반복 생산성·롤백을 재검토한다.

## 2.1 Visual Requirement Gate

프로젝트에서 이미지·아이콘·일러스트·UI 컴포넌트·VFX·마케팅 시각물을 후보로 떠올렸다는 이유만으로 바로 제작하지 않는다. 먼저 **무엇을 왜 만들어야 하는지**를 같은 기준으로 판정한다.

이 Gate에 들어오기 전에 **제작 정보가 필요한 것인지, 이미지/시각 자산 자체가 필요한 것인지**를 분리한다.

```text
PRODUCTION_INFORMATION
→ 시스템 설명 / 세계관 / 캐릭터·세력 관계 / 관계도 / 제작 체크리스트 / 밸런스·경제 / Flow / 구현 계약
→ TEXT_TABLE_FLOW_DB_FIRST
→ Markdown / Notion text·table·DB / Mermaid / Flow / JSON 등 해당 정보 owner에 생성·갱신
→ image requirement로 만들지 않음

IMAGE_ASSET_OR_SURFACE
→ ACTUAL_CONSUMER_REQUIRED
→ GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
→ Visual Requirement Gate 계속
```

`PRODUCTION_INFORMATION`은 이미지 생성 제한 때문에 생략하는 대상이 아니다. 필요한 정보는 계속 만들되, 제작자·AI 이해만을 위해 고해상도 설명용 시트·포스터·관계 이미지를 신규 생성하는 것을 기본값으로 삼지 않는다.

표준 순서는 다음과 같다.

```text
정보 목적 분류: PRODUCTION_INFORMATION | IMAGE_ASSET_OR_SURFACE
→ image 후보이면 ACTUAL_CONSUMER_REQUIRED
→ 플레이어·사용자의 판단/행동
→ 필요한 정보·감정·피드백
→ 기존 텍스트·표준 컴포넌트로 충분한가
→ 기존 프로젝트·디자인 시스템 자산으로 재사용 가능한가
→ Delete Test
→ 역할 분류
→ P0~P3 우선순위
→ 제작·조달 disposition
→ 실제 소비처·검증 조건
```

`ACTUAL_CONSUMER_REQUIRED`는 이미지 requirement에 최소한 다음을 요구한다.

```yaml
consumer_kind: GAME_RUNTIME | PLANNED_GAME_SURFACE | PLAYER_FACING_EXPLANATORY | PRODUCT_DISTRIBUTION
consumer_surface:
primary_use:
validation:
```

- `GAME_RUNTIME`: 실제 scene/HUD/character/environment/VFX/item 등 게임이 소비한다.
- `PLANNED_GAME_SURFACE`: 아직 구현 전이어도 실제 게임에 들어갈 구체적인 screen/scene/asset slot을 검증한다.
- `PLAYER_FACING_EXPLANATORY`: 튜토리얼·도감·인게임 도움말·세력 관계 UI처럼 플레이어가 게임 안에서 소비한다.
- `PRODUCT_DISTRIBUTION`: store capsule·key art·app icon·trailer thumbnail·press kit처럼 판매·배포·홍보 경로가 소비한다.

`DOCUMENTATION_DECORATION / AI_EXPLANATION_ONLY / CHECKLIST_DECORATION / UNNAMED_FUTURE_USE`만 존재하면 이미지 requirement로 선정하지 않는다. 필요한 정보 자체는 `TEXT_TABLE_FLOW_DB_FIRST`로 보존한다.

### Delete Test

후보를 완전히 제거했을 때 **핵심 흐름, 정보 이해, 플레이어 감정·정체성, 접근성, 플랫폼 제출, 마케팅 전달 중 무엇이 실제로 실패하거나 유의미하게 약해지는지** 설명한다.

- 제거해도 관찰 가능한 손실이 없으면 기본값은 `DEFER` 또는 `CUT`이다.
- 장식이라는 이유만으로 자동 삭제하지 않는다. 프로젝트 코어 감정·브랜드 기억점·세계관 전달에 관찰 가능한 가치가 있으면 근거에 따라 우선순위를 올릴 수 있다.
- 이미 존재하는 표준 컴포넌트·Theme·프로젝트 자산으로 같은 역할을 충족하면 신규 제작보다 재사용을 우선한다.
- 플랫폼이 현재 공식 규격으로 요구하는 자산은 `PLATFORM_REQUIRED`로 분류하되 규격·수량·날짜는 제출 시점의 공식 문서를 다시 확인한다.

### 역할 분류

| role | 판정 질문 | 예 |
|---|---|---|
| `FUNCTIONAL` | 행동을 시작·완료·취소하는 데 필요한가 | 버튼, 슬롯, 선택 카드 |
| `INFORMATIONAL` | 판단에 필요한 상태·차이·위험을 더 빠르고 정확하게 전달하는가 | 상태 아이콘, 지도 기호 |
| `FEEDBACK` | 입력 접수·처리·성공·실패를 전달하는가 | 피격, 선택됨, 잠김 |
| `EXPLANATORY` | **플레이어가 실제 제품 surface에서** 구조·규칙·공간 관계를 이해해야 하는가 | 인게임 튜토리얼 그림, 도감·세력 관계 UI |
| `IDENTITY` | 캐릭터·진영·세계·제품의 식별성과 기억점을 소유하는가 | 캐릭터, 문장, 핵심 환경 |
| `EMOTIONAL` | 감정·판타지·분위기 자체가 제품 가치인가 | 대표 장면, 이벤트 일러스트 |
| `DECORATIVE` | 기능·정보보다 장식·마감이 주 역할인가 | 테두리, 배경 장식 |
| `PLATFORM_REQUIRED` | 현재 플랫폼 제출·배포에 필수인가 | store capsule, app icon |
| `REFERENCE_ONLY` | 비교·방향 탐색용이며 제품 자산이 아닌가 | mood board, concept reference |

제작자·AI가 알아야 하는 **시스템 다이어그램, 세계관 구조, 관계도**는 `EXPLANATORY` 이미지 role로 자동 승격하지 않는다. 기본값은 `PRODUCTION_INFORMATION`이며 Mermaid·Flow·표·DB 등 수정 가능한 형식으로 만든다. 동일 내용이 실제 게임의 튜토리얼·도감·관계 화면에 들어가는 경우에만 별도 `PLAYER_FACING_EXPLANATORY` image requirement를 만들 수 있다.

### 우선순위

기존 UX/UI와 같은 네 단계 언어를 사용해 가짜 정밀 점수제를 만들지 않는다.

| priority | 기준 |
|---|---|
| `P0 BLOCKER` | 없으면 핵심 흐름·접근성·기술 계약·플랫폼 제출이 실패한다 |
| `P1 CLARITY` | 없으면 핵심 경험·규칙·판단·세일즈포인트 이해가 크게 약해진다 |
| `P2 CONSISTENCY` | 재사용성·일관성·학습 비용·반복 제작 효율을 유의미하게 개선한다 |
| `P3 DELIGHT` | 감정·연출·브랜드·폴리싱을 강화하지만 P0~P2를 대체하지 않는다 |

P0~P2가 미해결이면 P3 대량 제작을 기본적으로 보류한다.

### 제작·조달 disposition

```text
REUSE_SYSTEM         Godot·OS·플랫폼·디자인 시스템의 기존 요소 사용
REUSE_PROJECT        현재 프로젝트의 기존 컴포넌트·자산 재사용
ADAPT_EXISTING       현행 요소를 bounded 변형해 사용
SOURCE_EXISTING      Asset Store·오픈소스·상용 패키지 등 기존 대안 조사
GENERATE_EXPLORATION 실제 planned game/product surface의 방향·정보 위계를 생성 도구로 탐색, 제품 자산 아님
CREATE_CUSTOM        actual consumer가 있는 프로젝트 고유 요구를 신규 제작
DEFER                가치는 있으나 현재 단계에서 만들지 않음
CUT                  가치보다 비용·복잡도·혼란이 커 범위에서 제거
```

`SOURCE_EXISTING`은 `evaluating-godot-assets-and-plugins-before-creation`의 기존 대안 평가로 넘긴다. `GENERATE_EXPLORATION`과 승인된 `CREATE_CUSTOM` 이미지 제작은 `ACTUAL_CONSUMER_REQUIRED`를 충족한 경우에만 `designing-art-prompts-and-technique-cards`가 이어받는다. actual consumer가 없는 제작 정보는 이미지 Skill로 넘기지 않고 해당 structured owner로 보낸다. UI 컴포넌트의 상태·입력·정보 구조는 `auditing-and-refining-ui-art`가 상세화하고, Vertical Slice는 해당 구간을 증명하는 최소 requirement 집합만 소비한다.

### 프로젝트 기록

프로젝트에는 공용 판단 규칙을 복제하지 않고, 실제 요구사항과 판정만 기록한다.

```yaml
requirement_id:
surface_or_flow:
player_question:
element_type:
role:
why_needed:
delete_test:
consumer_kind:
consumer:
primary_use:
priority: P0_BLOCKER | P1_CLARITY | P2_CONSISTENCY | P3_DELIGHT
reuse_candidate:
disposition:
required_states:
accessibility_equivalent:
platform_and_input:
localization:
production_cost: LOW | MEDIUM | HIGH
performance_risk:
rights_or_provenance:
validation:
handoff:
```

Concept 단계는 방향을 가르는 소수 requirement만 기록하고, PoC는 핵심 가설을 증명하는 최소 요소에 집중한다. Vertical Slice에서는 대표 경험과 반복 제작성을 증명하는 P0/P1 및 필요한 P2를 목표 품질에 가깝게 검증한다. Production에서 반복 세트·상태 변형·현지화·성능·권리를 확장하고, Release에서는 현재 공식 플랫폼 규격을 다시 조회해 `PLATFORM_REQUIRED`를 갱신한다.

### 권위 경계

`Visual Requirement Gate`는 **필요성·역할·우선순위·제작 방식 판단**을 소유한다. 실제 생성된 파일이나 승인된 제품 자산의 존재를 새로 소유하지 않는다.

```text
Visual Requirement Gate
→ 무엇이 왜 필요한가

ASSET_MANIFEST.yml
→ 실제 승인 자산의 의미·사용처·승인·권리 연결

docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md
→ 승인 전 로컬 후보와 실제 파일 보존·동기화·promotion 경계
```

따라서 requirement row, `ASSET_MANIFEST.yml`, 로컬 Asset Vault를 하나의 중복 원장으로 합치지 않는다. 승인 전 후보는 requirement와 로컬 작업면에서 관리하고, `PROJECT_ASSET_APPROVED` 뒤에만 기존 Manifest·promotion 흐름으로 승격한다.

## 2.2 Primary Use Gate → Reusable Visual Harvest Gate

시각 자산의 재사용성은 **좋은 이미지의 목적 달성 뒤에 수확한다.** 재사용을 쉽게 만들기 위해 최초 화면의 플레이어 경험·정보 위계·감정·구도나 프로젝트의 `title-specific identity`를 희생하지 않는다. `primary-use success`와 `reuse promotion`은 서로 다른 판정이다.

```text
existing approved asset / Visual Bible lookup
→ visual proposal
→ user approval
→ image production
→ Primary Use Gate
→ Reusable Visual Harvest Gate
→ selective structure / layer / semantic rebuild
→ reusable asset / pattern / Visual DNA
→ next-task reuse or variant
```

### Primary Use Gate

완성 이미지는 먼저 본래 사용처에서 다음을 만족해야 한다.

- 화면·배경·장면·키아트가 원래 목적과 플레이어/사용자 경험을 달성한다.
- 정보 위계·가독성·감정·아트 방향이 승인 기준과 맞는다.
- 재사용을 위해 장면의 고유 composition이나 identity를 평준화하지 않는다.
- 제작 과정에서 `textless master`, `clean plate`, 투명 source처럼 저비용 separation hint를 자연스럽게 남길 수는 있지만 사전 자산화가 본 제작을 지배하지 않는다.

### Reusable Visual Harvest Gate

Primary Use Gate를 통과한 결과만 다음 질문으로 재사용 후보를 판정한다.

1. 다른 화면·장면에서 같은 역할로 다시 쓸 가능성이 높은가?
2. 기존 reusable asset·pattern과 중복되지 않는가?
3. 독립적으로 편집·배치해도 원래 장면과 프로젝트의 `title-specific identity`를 훼손하지 않는가?
4. 분리·재구축 비용보다 다음 사용에서 절감할 제작 비용이 큰가?
5. 선택한 분리·재구축 방식이 source/provenance truth를 보존하는가?

`잘라낼 수 있음`만으로 reusable asset이 되지 않는다. 후보는 다음 중 하나로 분류한다.

| classification | 의미 | 예 |
| --- | --- | --- |
| `REUSE_AS_IS` | 동일 bytes/구조를 독립적으로 다시 사용 | 아이콘, 독립 prop, 장식 texture |
| `VARIANT_SEED` | 승인 기준 자산에서 상태·색·테마 변형 | normal/hover/pressed, day/night |
| `STRUCTURE_PATTERN` | 픽셀이 아니라 배치·정보 위계·interaction 구조 재사용 | HUD, 보상 화면 layout |
| `STYLE_DNA` | palette·shape·material·lighting·camera·spacing 규칙 재사용 | 프로젝트 시각 문법 |
| `REBUILD_FOR_REUSE` | crop보다 semantic component/scene/theme 재구축이 안전 | 버튼, scalable panel, UI skin |
| `ONE_OFF_KEEP` | 현재 결과에는 중요하지만 공용화 가치가 낮아 그대로 보존 | 이벤트·영웅 장면, 서사 composition |
| `REJECT_REUSE` | 오류·중복·권리·저품질·정체성 위험 때문에 재사용하지 않음 | 잘못 분리된 손·그림자 |

`ONE_OFF_KEEP`는 실패가 아니다. 강한 narrative composition·hero image·타이틀 고유 표현은 공용화하지 않는 것이 일관성 보호에 더 적합할 수 있다.

### 분리·재구축 방법

가장 낮은 위험 방식부터 선택한다.

```text
SOURCE_LAYER
→ MASK_CUTOUT
→ MANUAL_OR_SEMANTIC_REBUILD
→ DERIVED_GENERATIVE_RECOVERY
```

- `SOURCE_LAYER`: 제작 단계에서 이미 독립 layer/file로 존재한 source를 사용한다.
- `MASK_CUTOUT`: 현재 관측되는 픽셀만 mask/matting으로 분리한다.
- `MANUAL_OR_SEMANTIC_REBUILD`: 특히 UI처럼 상태·크기·현지화·접근성이 필요한 요소를 Figma Component/Variant, Godot Theme/Scene/Resource 등 의미 구조로 다시 만든다.
- `DERIVED_GENERATIVE_RECOVERY`: 가려진 영역이 독립 재사용에 반드시 필요한 경우에만 생성 복원한다. 이는 원본에서 관측된 사실이 아니라 **생성된 derived pixel**이며 별도 provenance와 검토를 요구한다.

Harvest 후보·분리 결과는 승인 전 `.asset-vault`/Figma WIP에서 검토하며, Harvest 판정만으로 `PROJECT_ASSET_APPROVED`, tracked asset, `promote`, Figma Final 또는 Godot runtime proof가 되지 않는다.

## 3. Visual Pillar

Visual Pillar는 3~5개로 제한하고 서로 다른 책임을 가진다.

예시 구조:

```yaml
pillar_id:
player_promise:
visual_rule:
observable_examples:
anti_examples:
implementation_scope:
validation_capture:
```

좋은 Visual Pillar:

- 플레이어 경험과 연결된다.
- 실제 캐릭터·배경·UI·이펙트에서 관찰 가능하다.
- 포함 예시와 금지 예시가 있다.
- 제작 비용과 기술 제약을 고려한다.
- 다른 Pillar와 중복되지 않는다.

나쁜 Visual Pillar:

- `고퀄리티`
- `예쁨`
- `독창적`
- `AAA 느낌`

## 4. Visual Identity 구조

```text
플레이어 약속
→ Visual Pillar
→ Shape Language·실루엣
→ Color·Value·Composition
→ Typography·Iconography·Logo
→ 캐릭터·환경·UI·VFX·Animation
→ Store·Trailer·Marketing
→ 실제 인게임 캡처
```

### Shape Language

`Shape Language`는 진영·문화·성격·기능을 공통 형태로 표현한다.

현업 사례에서 shape language는 추상 형태를 차량·의상·건축·환경으로 확장해 세계관을 일관되게 만드는 방법으로 사용된다: https://www.gdcvault.com/play/1025897/Art-Direction-Bootcamp-Building-Worlds

검수:

- 원·삼각·사각·곡선·각진 형태가 어떤 의미를 갖는가?
- 캐릭터·장비·건물·UI가 같은 형태 문법을 공유하는가?
- 모든 대상이 같은 모양이라 구분성이 사라지지 않는가?
- 세계관의 문화·재료·기능과 연결되는가?

### 실루엣

실루엣은 디테일을 제거한 상태에서도 역할·진영·위험·방향을 구분하게 한다.

```text
전체 크기
→ 머리·몸통·부속 비율
→ 대표 도구·장식
→ 포즈·무게 중심
→ 이동·공격 시 외곽 변화
```

썸네일과 실제 플레이 거리 양쪽에서 검사한다.

### Color

`Color`는 분위기뿐 아니라 진영·상태·상호작용을 전달한다.

- 핵심 상태를 색 하나에만 의존하지 않는다.
- 배경과 플레이 요소의 분리 기준을 둔다.
- 일반·위험·보상·선택·비활성 상태의 색 역할을 정의한다.
- 플랫폼·디스플레이·밝기·색각 조건을 고려한다.

### Value

`Value`는 명도 구조다.

- 흑백으로 보아도 핵심 요소가 분리되는가?
- 가장 밝거나 어두운 영역이 의도한 시선을 받는가?
- UI·텍스트·이펙트가 배경과 충돌하지 않는가?
- 공포를 “전부 어둡게” 만드는 방식으로 해결하지 않는가?

### Composition

`Composition`은 플레이어의 시선과 정보 순서를 설계한다.

- 첫 시선
- 두 번째 판단 정보
- 행동 대상
- 위험·보상
- 다음 이동 방향
- 서사·감정 강조

카메라·UI·캐릭터·이펙트가 서로 같은 위치를 경쟁하지 않게 한다.

## 5. 시각적 위계

```text
1차: 지금 반드시 알아야 하는 정보
2차: 다음 선택에 필요한 정보
3차: 숙련·최적화 정보
4차: 분위기·세계관·장식
```

장식이 1차·2차 정보를 가리면 Art Quality가 아니라 UX 결함이다.

검수 방법:

- 3초 테스트
- 흑백 테스트
- 축소 썸네일 테스트
- 모션 중 정지 화면 테스트
- 색 제거 테스트
- 텍스트·아이콘 제거 후 형태 테스트
- 실제 인게임 캡처 비교

## 6. 마스코트·상징

마스코트·상징은 귀여운 부속물이 아니라 다음 역할을 가질 수 있다.

- 첫인상과 기억점
- 플레이어 안내
- 세계관·기관·진영 표현
- 감정 완충
- 진행·성장·관계 피드백
- UI 상태 전달
- 상점·캡슐·트레일러 대표 이미지

```yaml
symbol_role:
player_relationship:
core_loop_touchpoints:
narrative_role:
ui_role:
marketing_role:
non_negotiable_traits:
changeable_traits:
production_scope:
```

마스코트가 핵심 판단을 대신하거나 기능 설명을 독점하지 않게 한다.

## 7. Concept Exploration

`Concept Exploration`은 정답 이미지 한 장을 빨리 만드는 단계가 아니다.

```text
문제 정의
→ reference axis
→ 서로 다른 방향 3개 안팎
→ 동일 구도·조건 비교
→ 채택·비채택 요소 분리
→ 선택 이유 기록
```

비교 차원 예:

- 현실성↔도식성
- 귀여움↔위엄
- 따뜻함↔불안
- 장식 밀도
- 형태 복잡도
- 색 채도
- 실제 제작 난이도
- UI·이펙트와 결합성

후보마다 다음을 기록한다.

- 강화하는 플레이어 경험
- 약화하는 정보
- 세일즈포인트
- 제작 비용
- 반복 생산 위험
- 기술·플랫폼 위험
- 채택 요소
- 비채택 요소

## 8. Concept → Art Bible → Asset Specification

### Concept Exploration

- 방향 후보와 핵심 질문을 검증한다.
- 최종 자산으로 사용하지 않는다.
- 임시 텍스트·수치·UI를 공식 기획값으로 해석하지 않는다.

### Art Bible

`Art Bible`은 프로젝트의 시각 결정과 판단 규칙을 가진다.

필수 내용:

- 플레이어 약속과 Visual Pillar
- Shape Language·실루엣
- Color·Value·Composition
- 캐릭터·환경·UI·VFX·Animation 원칙
- 재료·광원·카메라·렌더 규칙
- Typography·Iconography·Logo
- 포함·금지 예시
- 접근성·가독성
- 승인 상태와 대체 관계

### Asset Specification

`Asset Specification`은 개별 제작물이 실제 엔진과 파이프라인에서 작동하기 위한 계약이다.

```yaml
asset_id:
role:
canonical_path:
source_and_license:
dimensions_and_aspect:
viewing_distance:
pivot_and_alignment:
frames_and_states:
export_format:
import_settings:
performance_budget:
size_quality_class:
platform_import_profile:
quality_validation:
accessibility_role:
approval_status:
validation_scene_and_capture:
```

`size_quality_class`, `platform_import_profile`, `quality_validation`은 용량 최적화가 해당 자산에 적용될 때만 구체화한다. byte·압축·전달·패치 trade-off의 공용 방법은 `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`가 책임지고, 이 문서는 시각 의도·가독성·실제 인게임 품질을 계속 소유한다.

Art Bible이 “어떤 방향인가”를, Asset Specification이 “정확히 무엇을 어떻게 납품하는가”를 책임진다.

## 9. 캐릭터·환경·UI·VFX·Animation 연결

### 캐릭터

- 실루엣·비율·대표 소품
- 성격·직업·진영
- 실제 인게임 크기
- 표정·포즈·애니메이션 범위
- 다른 캐릭터와 구분성
- 마스코트·세일즈 역할

### 환경

- 이동·전투·조사의 길 찾기
- 위험·상호작용·보상 affordance
- 장소의 이야기
- 캐릭터와 명도·채도 분리
- 반복 모듈과 대표 landmark

### UI

- visual identity와 인게임 가독성의 균형
- Typography·Iconography·Focus·State
- 입력 장치별 일관성
- 화면 비율·안전 영역
- 색 외 정보 채널

GDC의 UI Art Direction 사례는 인지 과정·이론·엔진 지식을 결합해 concept부터 release까지 일관된 표현을 만드는 접근을 다룬다: https://www.gdcvault.com/play/1025498/Art-Direction-for-AAA

### VFX

- 판정·방향·범위·속성·위험·보상 전달
- VFX가 게임 디자인 언어로 작동하는가?
- 이펙트가 캐릭터·UI·배경을 가리지 않는가?
- 모션 감소·번쩍임·반복 피로 대안이 있는가?

VFX가 넓은 게임 디자인 개념을 시각 언어로 전달할 수 있다는 현업 관점을 참고한다: https://www.gdcvault.com/play/1027899/Visual-Effects-Summit-VFX-as

### Animation

- key pose와 silhouette 변화
- anticipation·contact·follow-through·recovery
- 입력·판정·피드백 타이밍
- 무기·장비·의상 continuity
- 루프·1회성·전환 상태
- 프레임 수보다 의미 있는 동작 차이

## 10. 실제 인게임 검수

아트는 분리된 일러스트가 아니라 실제 게임 화면에서 검수한다.

필수 증거:

- 실제 해상도
- 대표·최악 장면
- 실제 UI와 텍스트
- 이동·전투·이펙트 중 화면
- 밝은·어두운 배경
- 목표 플랫폼 화면 크기
- 접근성 옵션 적용 전후
- 성능 capture
- 용량 최적화 전후 동일 장면 비교(해당 시)
- texture compression·resolution·font fallback 변경의 artifact/가독성 확인(해당 시)

상태 예:

```text
CONCEPT_EXPLORATION
→ VISUAL_REFERENCE_CANDIDATE
→ USER_APPROVED_VISUAL_REFERENCE
→ ART_BIBLE_APPROVED
→ ASSET_SPEC_APPROVED
→ IMPLEMENTED_IN_ENGINE
→ RUNTIME_ASSET_APPROVED
```

`Runtime Asset Approval`은 실제 인게임 캡처·성능·가독성 검수 뒤에만 사용한다. 용량 최적화가 적용된 자산은 byte 절감만으로 승인하지 않고 변경 후 동일 quality bar를 다시 확인한다.

## 11. 생산 파이프라인

```text
Brief
→ Concept
→ Review
→ Specification
→ Production
→ Export
→ Import
→ Integration
→ Runtime QA
→ Revision
→ Approval Ledger
```

각 단계에 입력·출력·담당·도구·검증·재작업 원인을 기록한다.

### 두 번째 같은 유형의 자산

첫 자산 하나를 멋지게 만든 것으로 Production 준비를 판단하지 않는다.

두 번째 같은 유형의 자산을 만들며 다음을 확인한다.

- Brief가 재사용 가능한가?
- 명명·경로·Export·Import가 반복 가능한가?
- 품질 판단이 개인 감각에만 의존하는가?
- 수정 왕복 횟수와 병목은 무엇인가?
- AI·외주·에셋 사용 시 provenance가 추적되는가?
- 실제 엔진 통합 시간이 예측 가능한가?

## 12. AI 생성·외주·기존 에셋

### 공통 원칙

- 원출처를 기록한다.
- 라이선스와 상업 사용 조건을 확인한다.
- 기존 IP·작가·브랜드와의 유사성을 검수한다.
- 생성·편집·외주·구매·직접 제작 관계를 기록한다.
- 채택·비채택 요소와 사용자 승인 상태를 남긴다.

### 생성 이미지

**생성 이미지는 자동 최종 자산이 아니다.**

기획 시각화, 후보 비교, mood·composition 탐색과 최종 후보 제작을 구분한다. 실제 자산은 Asset Specification과 Runtime 검수를 통과해야 한다. 프로젝트용 생성 이미지는 `ACTUAL_CONSUMER_REQUIRED`를 충족해야 하며, 제작자·AI용 `PRODUCTION_INFORMATION`은 생성 이미지 대신 `TEXT_TABLE_FLOW_DB_FIRST`를 적용한다.

### Pinterest·커뮤니티 이미지

- 탐색과 mood reference로 사용할 수 있다.
- Pinterest Pin 자체를 원출처로 간주하지 않는다.
- 가능하면 작가·스튜디오·공식 프로젝트 원문으로 추적한다.
- 무단 복제·스타일 사칭·로고·상표·인물 위험을 검수한다.

### 외주

현업 대규모 외주 사례처럼 상세 Brief와 품질 보호 파이프라인이 중요하다. 1인 개발에서는 규모를 복사하지 않고 다음 원리를 ADAPT한다.

- 납품 규격
- 포함·금지 예시
- 리뷰 단계
- 수정 횟수와 책임
- 원본 파일·파생물·권리
- 엔진 통합 검증

## 13. 접근성·성능

- 핵심 정보는 Color 하나에만 의존하지 않는다.
- 텍스트·아이콘·형태·음향·진동 중 가능한 대체 채널을 둔다.
- motion·camera shake·flashing을 조절할 수 있게 한다.
- 실제 frame time·GPU·메모리·로딩 예산을 아트 목표와 연결한다.
- 모바일은 발열·배터리·해상도·텍스처 메모리를 고려한다.
- 접근성 옵션이 visual identity를 파괴하지 않도록 초기부터 설계한다.
- 용량 최적화는 `size_quality_class`와 실제 screen coverage를 사용하며 모든 자산에 동일 resolution·compression을 강제하지 않는다.
- 폰트·texture·animation 압축으로 용량을 줄였으면 실제 장면에서 visual identity·가독성·silhouette·contact timing을 다시 검증한다.

## 14. 실패 조건

- Art Direction을 이미지 검색 결과 모음으로 대체함
- 키워드만 있고 관찰 가능한 Visual Pillar가 없음
- Concept 이미지를 Art Bible·Asset Specification 없이 대량 제작함
- 큰 일러스트만 보고 실제 인게임 가독성을 검증하지 않음
- 배경·캐릭터·UI·VFX가 같은 위치·명도·채도를 경쟁함
- 생성 이미지의 원출처·권리·유사성·승인 상태가 없음
- 첫 자산 하나만 만들고 반복 제작 가능성을 통과 처리함
- 성능·접근성·플랫폼 제약을 구현 후반으로 미룸
- 승인 이미지가 있는데 별도 지시 없이 교체함
- 용량 절감을 이유로 HERO/GAMEPLAY_CRITICAL 품질 저하를 증거 없이 승인함
- PC와 Android에 동일 texture import profile을 무조건 강제함
- Delete Test 없이 “있으면 좋아 보인다”는 이유만으로 P3 시각물을 대량 제작함
- 기존 컴포넌트·프로젝트 자산을 조사하지 않고 동일 역할을 신규 제작함
- 제작자·AI가 알아야 할 시스템·세계관·관계 정보를 이미지 생성 제한 때문에 생략함
- 반대로 제작자·AI용 설명 정보를 actual consumer가 없는 고해상도 생성 이미지 시트로 대체함
- `PLAYER_FACING_EXPLANATORY`와 제작자용 구조 문서를 같은 image requirement로 취급함

## 15. Output Contract

```md
## 플레이어 경험·정보 역할·시장 첫인상
## Production Information route · Actual Consumer
## Visual Requirement Gate·Delete Test·role·priority·disposition
## Visual Pillar·포함·금지 예시
## Shape Language·실루엣·Color·Value·Composition
## 시각적 위계·마스코트·상징
## Concept Exploration 후보 비교
## Art Bible 결정
## Asset Specification·경로·규격·Import·size quality profile
## 캐릭터·환경·UI·VFX·Animation 연결
## 실제 인게임 캡처·최적화 전후 품질·Runtime Asset Approval
## 원출처·라이선스·유사성·승인 원장
## 반복 생산성·두 번째 같은 유형의 자산
## 접근성·성능·미검증·다음 결정
```