# Pixel Art Style System

> 역할: Base 공용 픽셀 아트 **분류·비교·선택 Reference**
> 실행 책임: 기존 `designing-art-prompts-and-technique-cards`, 프로젝트 Art/UX 책임자
> 시각 예시: `PIXEL_ART_VISUAL_REFERENCE_GALLERY.md`
> 사용자 선호 Reference: `PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md` — 픽셀/비픽셀 혼합 선호군과 AI-look·일관성·세계/시스템 적합성 평가 렌즈
> 프로젝트 정본: 각 프로젝트의 승인된 Art Bible·Visual Bible·Decision

## 1. 목적과 권위 경계

이 문서는 픽셀 아트를 `Anime`, `Chibi`, `HD`, `Clean` 같은 한 줄 장르명으로 고르는 대신, 실제 제작에서 독립적으로 바뀌는 축을 분리해 조합하도록 돕는다.

```text
Base
→ 가능한 시각 어휘·제작 문법·비용·실패 조건·예시를 제공

Project
→ 플레이어 경험·화면 거리·플랫폼·생산 능력·기존 Art Bible을 대조
→ 후보를 비교하고 실제 프로젝트 스타일을 승인
```

고정 경계:

```text
PROJECT_ART_CANON_REMAINS_PROJECT_OWNED
NO_AUTOMATIC_PROJECT_STYLE_PROMOTION
```

- Base Preset은 **선택 재료**이며 프로젝트 정본이 아니다.
- Base Preset 이름을 프로젝트 문서에 복사했다는 사실만으로 스타일이 승인되지 않는다.
- 이미 잠긴 프로젝트 Art Bible과 충돌하면 현행 프로젝트 정본을 우선한다.
- 외부 예시는 `REFERENCE_ONLY`이며 제품 자산·라이선스 승인·Project Visual 승인·`PROJECT_ASSET_APPROVED`를 뜻하지 않는다.

## 2. 선택 Gate

픽셀 아트가 프로젝트의 주 스타일 또는 중요한 하위 스타일 후보가 되면 별도 병렬 규칙을 만들지 않고 Base `AGENTS.md`의 현행 의사결정 계약을 그대로 적용한다.

```text
MINIMUM_VIABLE_ALTERNATIVES: 3
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS
```

### 최소 3개 실질 대안

`MINIMUM_VIABLE_ALTERNATIVES: 3`을 픽셀 아트 결정에 적용한다.

- 현행 유지도 실제로 유효하면 하나의 대안이 될 수 있다.
- 최소 3개 후보는 이름만 다른 허수 후보가 아니라, 플레이어에게 보이는 결과 또는 제작 파이프라인이 materially distinct 해야 한다.
- 권장 기준은 최소 두 축 이상이 다르거나, 같은 시각 결과라도 생산 방식·비용·애니메이션 파이프라인이 실질적으로 달라야 한다.
- 세 후보를 만들기 어렵다면 `픽셀 아트 내부 변형`만 보지 말고 `비픽셀 현행 유지`, `하이브리드`, `화면별 혼합`까지 탐색한다.
- 조사 뒤에도 세 실질 후보를 만들 수 없으면 임의로 기준을 낮추지 않고 Base의 fail-closed 경계를 따른다.

### 결정 직전까지 더 나은 대안 탐색

`BETTER_ALTERNATIVE_SEARCH`를 픽셀 아트 선택 전체에 적용한다. 최초 3개를 적은 뒤 조사 종료로 취급하지 않는다. 레퍼런스, 기술 제약, 승인된 Project Visual Reference / Notion Asset surface, 실제 표시 크기, 애니메이션 비용, 프로토타입 결과에서 새 증거가 나오면 더 나은 후보를 계속 추가·교체한다.

프로젝트 승인 직전에는 마지막으로 다음을 다시 확인한다.

1. 최초 선호안보다 더 명확하거나 더 낮은 수명주기 비용의 후보가 생겼는가.
2. 새 후보가 핵심 플레이어 경험·프로젝트 정체성을 바꾼다면 사용자 결정이 필요한가.
3. 선택 이유가 최신 증거를 반영하고 있는가.

이 마지막 확인은 `BETTER_ALTERNATIVE_SEARCH`의 픽셀 아트 적용 기록이며 새 전역 Gate ID를 만들지 않는다.

### 장기계획 적합성

`LONG_TERM_PLAN_FIT_REQUIRED`는 다음을 본다.

- 첫인상과 프로젝트 고유 기억점
- 실제 플레이 거리에서의 실루엣·정보 가독성
- 캐릭터·배경·UI·VFX 간 일관성
- 두 번째·열 번째 자산을 만들 때의 반복 제작 비용
- 애니메이션 프레임 수와 변형 비용
- PC/모바일 해상도·화면비·카메라 확대 축소
- 1인 개발자가 Production까지 유지할 수 있는가
- Project Visual/Art Bible과 Notion human-facing 자산 구조로 연결하기 쉬운가
- 향후 콘텐츠 확장·현지화·접근성에서 깨지지 않는가
- 실패했을 때 다른 후보로 되돌리기 쉬운가

### 최종 재검토

프로젝트 Decision 직전에는 위 Base 계약의 적용 결과를 한 번 더 읽는다.

1. 프로젝트 코어 경험을 아트 취향이 가리고 있지 않은가.
2. 선택안보다 더 싸고 명확한 후보가 조사 중 발견됐는데 관성으로 무시하지 않았는가.
3. 대표 캐릭터 한 장이 아니라 배경·UI·반복 자산까지 같은 규칙으로 만들 수 있는가.
4. 작은 화면·축소 화면에서도 핵심 상태가 읽히는가.
5. 승인된 기존 Art Bible을 불필요하게 갈아엎고 있지 않은가.

L1 이상에서는 `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`를 별도 축 체크리스트가 아니라 전체 승인 범위에 대한 완전한 개선 루프로 수행한다. blocking finding이 남으면 5회차 뒤에도 종료하지 않는다.

## 3. 다축 모델

스타일은 다음 튜플로 기록한다.

```yaml
PIXEL_GRAMMAR:
CHARACTER_SHAPE:
VIEW:
MOOD_PALETTE:
DETAIL_MOTION:
```

예:

```yaml
PIXEL_GRAMMAR: CLEAN_CLUSTER
CHARACTER_SHAPE: ANIME_COMPACT
VIEW: THREE_QUARTER
MOOD_PALETTE: MUTED_OCCULT_TEAL_RED
DETAIL_MOTION: MID_32_48_FLUID_KEY_ACTIONS
```

이 방식에서는 `Anime Pixel Art`와 `Clean Cluster Pixel`이 경쟁 장르가 아니다. 같은 프로젝트가 둘을 동시에 사용할 수 있다.

### 3.1 `PIXEL_GRAMMAR`

| 값 | 핵심 원리 | 주 위험 |
|---|---|---|
| `ONE_BIT` | 두 값 또는 극소수 값으로 형태를 자른다 | 정보량 부족 |
| `LIMITED_INDEXED` | 제한 팔레트와 명확한 색 역할 | 팔레트가 상태색과 충돌 |
| `CLEAN_CLUSTER` | 고립 픽셀보다 읽히는 픽셀 덩어리·면을 우선 | 지나친 정리로 재질감 상실 |
| `DITHERED` | 패턴으로 중간 명도·거친 재질을 표현 | 축소 시 노이즈·모아레 |
| `SOFT_NO_OUTLINE` | 경계색·명암으로 형태 분리 | 배경과 합쳐짐 |
| `HARD_OUTLINE` | 외곽선으로 실루엣을 강하게 분리 | 화면이 무겁고 답답해짐 |
| `PAINTERLY_PIXEL` | 픽셀 단위 제어를 유지하며 회화적 면·광원 사용 | 생산비 증가 |
| `HD_PIXEL` | 큰 캔버스에서 픽셀 구조와 세부 묘사를 유지 | 애니메이션 비용 폭증 |
| `HYBRID_RENDERED` | 3D/벡터/렌더 기반 결과를 팔레트·픽셀 규칙으로 변환 | 프레임 간 픽셀 일관성 붕괴 |
| `PIXEL_DEPTH_LIT_HYBRID` | 픽셀 주체와 깊이·광원·고해상도 공간 표현을 결합 | 조명/카메라가 픽셀 주체를 압도 |

### 3.2 `CHARACTER_SHAPE`

`CHIBI`, `ANIME_COMPACT`, `NATURAL_PROPORTION`, `MASCOT`, `SILHOUETTE_FIRST`, `HORROR_DISTORTED`, `OBJECT_FIRST` 중 필요한 것을 고른다. 캐릭터가 없는 퍼즐·풍경 프로젝트에는 `OBJECT_FIRST`가 더 적절할 수 있다.

### 3.3 `VIEW`

`SIDE`, `TOP_DOWN`, `THREE_QUARTER`, `ISOMETRIC`, `TACTICAL`, `FIRST_PERSON_SCENIC`, `PORTRAIT_UI_FIRST`처럼 실제 플레이 카메라와 소비 화면을 기록한다. 시점은 미술 취향이 아니라 실루엣·애니메이션·타일 제작량을 결정한다.

### 3.4 `MOOD_PALETTE`

`MONO`, `HANDHELD_4_TONE`, `EARTHY`, `COZY_PASTEL`, `NOIR`, `GOTHIC`, `NEON`, `HEROIC_RICH`, `MUTED_OCCULT`, `PROJECT_CUSTOM` 등을 출발점으로 쓴다. 상태색·접근성 신호는 분위기 팔레트보다 우선한다.

### 3.5 `DETAIL_MOTION`

| 범위 | 권장 용도 |
|---|---|
| `MICRO_8_16` | 많은 타일·아이콘·대량 유닛, 매우 낮은 제작비 |
| `CLASSIC_16_32` | 전통적인 게임플레이 자산, 빠른 반복 |
| `MID_32_64` | 얼굴·장비·행동 가독성과 제작비의 절충 |
| `HD_64_PLUS` | 대표 캐릭터·풍경·저빈도 고품질 자산 |
| `LIMITED_MOTION` | 키 포즈·짧은 루프 중심 |
| `FLUID_MOTION` | 전투·캐릭터 액션의 프레임 품질 우선 |
| `RENDER_ASSISTED_MOTION` | 3D/렌더 기반 포즈 일관성을 픽셀 결과로 변환 |

## 4. Base 실전 Preset 20종

Preset은 시작점을 빠르게 찾기 위한 **조합 예시**다. 프로젝트에서는 그대로 채택하지 말고 5축 값을 조정한다. 시각 예시는 `PIXEL_ART_VISUAL_REFERENCE_GALLERY.md`에서 같은 이름으로 찾는다.

`제작비`는 프로젝트 Template과 같은 `LOW | MEDIUM | HIGH` 3단계만 사용한다. 세부 사유는 프로젝트 기록에 적는다. 예를 들어 3D-to-Pixel은 초기 setup이 HIGH이고 반복 프레임 비용이 낮아질 수 있지만, 후보 비교에서는 총 파이프라인 비용을 `HIGH`로 둔다.

| Preset | 대표 조합 | 잘 맞는 경우 | 제작비 | 주요 위험 |
|---|---|---|---|---|
| **1-Bit Graphic Pixel** | ONE_BIT + SILHOUETTE_FIRST + MONO | 공포 기록, 퍼즐, 아이콘, 특수 구간 | LOW | 긴 플레이에서 단조로움 |
| **4-Tone Handheld Pixel** | LIMITED_INDEXED + HANDHELD_4_TONE | 회상, 휴대기기 감성, 규칙이 단순한 화면 | LOW | 상태 구분 색 부족 |
| **8-Bit Limited Palette** | LIMITED_INDEXED + MICRO_8_16 | 대량 타일, 고전 액션·RPG | LOW | 개성·재질 표현 부족 |
| **16-Bit Rich Pixel** | CLEAN_CLUSTER + HEROIC_RICH + CLASSIC_16_32 | RPG, 제작·탐험, 캐릭터 중심 2D | MEDIUM | 색 과다·클러터 |
| **Clean Cluster Pixel** | CLEAN_CLUSTER + PROJECT_CUSTOM | 대부분의 읽기 우선 픽셀 게임 | MEDIUM | 지나친 균질화 |
| **Dithered Texture Pixel** | DITHERED + LIMITED_INDEXED | 사막, 안개, 낡음, 거친 재질 | MEDIUM | 축소 노이즈 |
| **Soft No-Outline Pixel** | SOFT_NO_OUTLINE + COZY_PASTEL | 힐링, 자연, 부드러운 환경 | MEDIUM | 배경과 실루엣 합쳐짐 |
| **Hard-Outline Comic Pixel** | HARD_OUTLINE + SILHOUETTE_FIRST | 전투, 캐릭터 액션, 작은 화면 | MEDIUM | 화면이 무거워짐 |
| **Chibi Pixel** | CHIBI + MID_32_64 | 육성, 수집, 경쾌한 RPG | MEDIUM | 진지한 감정의 무게 감소 |
| **Anime / JRPG Pixel** | ANIME_COMPACT + CLEAN_CLUSTER | 캐릭터 정체성·파티·무협/판타지 | HIGH | 표정·의상 변형 비용 |
| **HD Pixel** | HD_PIXEL + HD_64_PLUS | 대표 캐릭터·장비·풍경의 세부 묘사 | HIGH | 프레임 애니메이션 비용 |
| **Painterly Pixel** | PAINTERLY_PIXEL + HD_64_PLUS | 분위기·광원·풍경이 핵심 경험 | HIGH | 반복 자산 일관성 |
| **Pixel Noir** | CLEAN_CLUSTER/DITHERED + NOIR | 미스터리, 도시, 오컬트, 탐정 | MEDIUM | 암부 가독성 |
| **Gothic Pixel** | HARD_OUTLINE/DITHERED + GOTHIC | 다크 판타지, 묘지, 저주, 공포 | HIGH | 장식 과잉 |
| **Cozy Pastel Pixel** | SOFT_NO_OUTLINE + COZY_PASTEL | 힐링, 생활, 수집 | MEDIUM | 상태 신호 약화 |
| **Neon Pixel** | CLEAN_CLUSTER + NEON | 사이버, 야간 도시, 위험 신호 | MEDIUM | 눈부심·색 접근성 |
| **Isometric Pixel** | CLEAN_CLUSTER + ISOMETRIC | 건설, 경영, 공간 퍼즐 | HIGH | 타일·방향 자산량 증가 |
| **Tactical Top-down Pixel** | SILHOUETTE_FIRST + TACTICAL + CLASSIC_16_32 | 전략, 오토배틀, 다수 유닛 | MEDIUM | 캐릭터 감정 표현 약함 |
| **3D-to-Pixel Hybrid** | HYBRID_RENDERED + RENDER_ASSISTED_MOTION | 회전·다방향·액션 프레임 생산을 안정화 | HIGH | setup·후처리·픽셀 문법 일치 비용 |
| **HD-2D Hybrid** | PIXEL_DEPTH_LIT_HYBRID + DEPTH_LIGHTING | 픽셀 주체와 깊이·광원·공간감을 동시에 강조 | HIGH | 렌더/조명 복잡도·정체성 분산 |

`HD-2D Hybrid`는 탐색 편의를 위한 발견용 이름이다. Base의 canonical 조합명은 `PIXEL_DEPTH_LIT_HYBRID`이며, 특정 회사·제품의 브랜드 표현이나 서명적 화면을 복제하는 지시로 사용하지 않는다. 생성 모델의 공식 style 명령어로도 취급하지 않는다.

## 4.1 사용자 선호 Reference Lens

사용자가 반복적으로 선호한 픽셀 하이브리드·치비 다크 판타지·수묵 무협·Dark Gold UI·Noir Archive 계열은 `PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md`에서 별도 `REFERENCE_ONLY` 렌즈로 관리한다.

이 렌즈는 기존 20 Preset을 대체하지 않는다. 프로젝트 후보를 만들 때 다음 세 질문을 추가한다.

```text
AI_GENERATED_LOOK_REDUCTION
STYLE_CONSISTENCY_AND_READABILITY
WORLD_CORE_SYSTEM_FIT
```

선호 Reference가 프로젝트 core나 현행 Art Bible보다 우선하지 않으며, `NO_AUTOMATIC_PROJECT_STYLE_PROMOTION`을 그대로 유지한다.

## 5. 프로젝트에서 사용하는 순서

```text
프로젝트 Art/Visual canon + 승인된 Project Visual Reference / Notion Asset surface 확인
→ 아트가 해결해야 할 플레이어 질문 정의
→ MINIMUM_VIABLE_ALTERNATIVES: 3에 따라 비픽셀 현행 유지 포함 실질 후보 확보
→ 5축으로 후보를 기록
→ Visual Gallery에서 관찰 포인트 확인
→ 실제 표시 크기와 대표 화면에서 저비용 탐색
→ BETTER_ALTERNATIVE_SEARCH로 결정 직전까지 더 나은 후보 재탐색
→ LONG_TERM_PLAN_FIT_REQUIRED로 비용·반복 제작·확장·롤백 비교
→ 최종 재검토
→ 프로젝트 사용자 승인
→ 프로젝트 Art Bible/Decision에 선택 결과만 기록
```

Base 문서를 프로젝트에 통째로 복제하지 않는다. 프로젝트는 선택한 5축, 왜 선택했는지, 버린 후보, 재검토 조건, 검증 결과만 가진다.

## 6. 제작·엔진 주의

### 팔레트와 Dithering

Aseprite 공식 문서에서 Indexed mode는 각 픽셀이 팔레트 색의 인덱스를 참조하는 방식이다. CLI에는 RGB→Indexed 변환과 ordered dithering/matrix 지정 경로가 있다.

- https://www.aseprite.org/docs/color-mode/
- https://www.aseprite.org/docs/cli/

따라서 `Limited Palette`는 단순히 색이 적어 보이는 이미지가 아니라 팔레트 역할과 변환 규칙까지 기록하는 편이 재현성이 높다. Dithering은 분위기용 노이즈가 아니라 의도한 명도·재질 패턴이어야 한다.

### Godot 표시

Godot의 pixel art는 원본 PNG만으로 결정되지 않는다. 실제 프로젝트에서 texture filtering, viewport/base resolution, integer scaling, Camera2D 확대·축소, UI와 3D 혼합 여부를 함께 검증한다.

- https://docs.godotengine.org/en/stable/classes/class_canvasitem.html
- https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html

`nearest`나 integer scaling을 사용했다는 사실만으로 아트 품질 PASS를 주장하지 않는다. 실제 목표 해상도 캡처와 사람 눈 QA가 필요하다.

## 7. 생성형 이미지와 Reference 사용

- Preset 이름은 생성 모델의 공식 스타일 명령어가 아니다.
- 생성 시에는 Preset 이름보다 5축의 형태·팔레트·시점·픽셀 문법·디테일/모션을 자연어 제작 계약으로 풀어 쓴다.
- 특정 현존 작가의 식별 가능한 스타일 모사를 목표로 삼지 않는다.
- Gallery의 외부 이미지는 원리 관찰용이다. 그대로 제품에 넣으려면 프로젝트 자산 권리 Gate를 다시 통과한다.
- 탐색 이미지가 좋아 보여도 프로젝트 Art Bible 승인과 Runtime 검증을 자동으로 획득하지 않는다.

## 8. 유지·재검토 조건

다음이 바뀌면 프로젝트 스타일 후보를 다시 비교한다.

- 카메라·화면비·주 플랫폼 변경
- 캐릭터 수·유닛 수·반복 배경 수가 크게 증가
- 애니메이션 요구량이 예상보다 커짐
- 승인된 Project Visual Reference / Notion Asset surface 또는 프로젝트 Art Bible 변경
- 작은 화면 가독성·접근성 실패
- 대표 자산은 좋지만 두 번째 같은 유형 자산에서 품질/비용이 유지되지 않음
- 더 나은 생산 방식이나 장기적으로 싼 실질 후보가 발견됨

Base의 이 문서가 갱신돼도 프로젝트 확정 스타일은 자동 교체되지 않는다. 프로젝트가 재검토 Gate를 열고 새 Decision으로 승인해야 한다.
