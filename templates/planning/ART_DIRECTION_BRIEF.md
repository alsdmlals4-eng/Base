# 아트디자인 기획서 템플릿

> 작성 방법: `docs/knowledge/methods/ART_DIRECTION_METHOD.md`  
> 생성·편집 기술: `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
> 공용 선정 기준: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`
> 픽셀 아트 후보 분류: `docs/knowledge/game-development/PIXEL_ART_STYLE_SYSTEM.md`
> 픽셀 시각 예시: `docs/knowledge/game-development/PIXEL_ART_VISUAL_REFERENCE_GALLERY.md`

## 1. 한 줄 시각 약속

> ___한 세계·대상을 ___한 형태·색·재료로 표현해, 사용자가 ___을 가장 먼저 느끼고 ___을 쉽게 구분하게 한다.

## 2. 사용자 경험과 아트 역할

- 첫 1초 감정:
- 가장 먼저 읽혀야 할 대상:
- 즉시 구분해야 할 상태·종류:
- 반복 사용 시 피로를 줄일 방법:
- 아트가 플레이·UI 판단을 돕는 방식:

## 3. 스타일 혼합

| 스타일 요소 | 역할 | 사용 범위 | 비율·강도 | 과잉 시 문제 |
|---|---|---|---|---|
| 기본 스타일 |  |  |  |  |
| 질감 스타일 |  |  |  |  |
| 강조 스타일 |  |  |  |  |
| 특수 스타일 |  |  |  |  |

### 3.1 Pixel art candidate — 조건부

픽셀 아트가 실제 후보일 때만 작성한다. Base Preset을 프로젝트 정본으로 복제하지 않고, Base `AGENTS.md`의 `MINIMUM_VIABLE_ALTERNATIVES: 3`, `BETTER_ALTERNATIVE_SEARCH`, `LONG_TERM_PLAN_FIT_REQUIRED`, `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`를 프로젝트 픽셀 아트 결정에 적용한다. 아래 값은 새 전역 규칙이 아니라 그 적용 결과를 기록하는 프로젝트용 필드다.

```yaml
pixel_art_candidate: YES | NO
minimum_viable_alternatives: 3
pixel_grammar:
character_shape:
view:
mood_palette:
detail_motion:
production_cost: LOW | MEDIUM | HIGH
better_alternative_search_status:
long_term_plan_fit:
pre_decision_rereview:
visual_reference_ids:
runtime_validation:
```

- `minimum_viable_alternatives: 3`은 이름만 다른 후보 3개를 뜻하지 않는다. 시각 결과 또는 생산 파이프라인이 실질적으로 달라야 하며, 유효하면 현행 비픽셀 유지도 후보에 포함한다.
- `better_alternative_search_status`는 Base `BETTER_ALTERNATIVE_SEARCH`의 적용 기록이다. 결정 직전까지 새 근거·시각 예시·기술 제약에서 더 나은 후보가 발견됐는지 기록한다.
- `long_term_plan_fit`은 Base `LONG_TERM_PLAN_FIT_REQUIRED`의 적용 기록이다. 두 번째·열 번째 같은 유형 자산, 애니메이션, 플랫폼 확장, 재사용, 유지비와 롤백까지 본다.
- `pre_decision_rereview`는 최종 선택 직전 현행 유지와 다른 후보를 다시 공격 검토한 결과이며 별도 전역 Gate ID가 아니다.
- `visual_reference_ids`는 관찰용 Reference를 가리키며 제품 자산 승인이나 스타일 승인을 자동 부여하지 않는다.

## 4. 시각 축

### 형태

- 인체·오브젝트 비율:
- 선화:
- 실루엣:
- UI 형태 언어:

### 색

- 기본 중성색:
- 브랜드 강조색:
- 상태 색:
- 색상 독립 신호:

### 명암·광원

- 셰이딩 단계:
- 대비:
- 광원 원칙:

### 재료·질감

- 주요 재료:
- 질감 강도:
- 특수 상태 표현:

## 5. 캐릭터·대상 디자인 카드

- 역할과 첫인상:
- 실루엣 키워드:
- 대표 자세:
- 식별 요소:
- 강조색:
- 핵심 소품:
- 필수 표정·상태:
- 다른 대상과 겹치면 안 되는 요소:

## 6. Visual Requirement Gate — 자산·컴포넌트 선정

후보를 바로 제작 목록으로 올리지 않는다. 먼저 `필요성 → Delete Test → 재사용 → 역할 → P0~P3 → disposition → 검증`을 기록한다. 공용 규칙은 Art Guide가 소유하고 이 프로젝트 문서에는 실제 판정만 남긴다.

### 6.1 Requirement record

```yaml
requirement_id:
surface_or_flow:
player_question:
element_type:
role:
why_needed:
delete_test:
consumer:
priority: P0_BLOCKER | P1_CLARITY | P2_CONSISTENCY | P3_DELIGHT
reuse_candidate:
disposition: REUSE_SYSTEM | REUSE_PROJECT | ADAPT_EXISTING | SOURCE_EXISTING | GENERATE_EXPLORATION | CREATE_CUSTOM | DEFER | CUT
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

| requirement_id | surface_or_flow | player_question | element_type | role | why_needed | delete_test | consumer | priority | reuse_candidate | disposition | validation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |

- `delete_test`가 관찰 가능한 손실을 설명하지 못하면 기본값은 `DEFER` 또는 `CUT`이다.
- `reuse_candidate`가 있으면 신규 제작 전에 재사용·bounded 변형을 먼저 검토한다.
- `DECORATIVE`는 자동 삭제가 아니라 기본 P3다. 코어 감정·브랜드 기억점에 증명 가능한 기여가 있으면 승격 근거를 기록한다.
- 플랫폼 요구 자산은 `PLATFORM_REQUIRED`로 분류하고 제출 시점의 공식 규격을 다시 확인한다.

### 6.2 기존 자산 티어

선정 Gate를 통과한 항목에만 프로젝트 기존 티어를 적용한다. 티어는 필요성 판정을 대체하지 않는다.

| 티어 | 자산 | 용도 | 제작 방식 | 폴백 |
|---|---|---|---|---|
| T0 |  |  |  |  |
| T1 |  |  |  |  |
| T2 |  |  |  |  |
| T3 |  |  |  |  |

## 7. 레퍼런스

| 레퍼런스 | 관찰할 요소 | 적용할 원리 | 복제하지 않을 요소 |
|---|---|---|---|
|  |  |  |  |

## 8. 제작·기술 제약

- 화면비·해상도:
- 실제 표시 크기:
- 알파·파일 포맷:
- 엔진·도구 제약:
- 제작 일정·예산:
- 라이선스·출처:

## 9. 디자인 기술 라이브러리

이 프로젝트에서 추천·재사용할 수 있는 시각 기술을 기록한다. 상세 카드는 `templates/planning/ART_TECHNIQUE_CARD.md`를 사용한다.

| 기술명 | 해결 문제 | 사용 조건 | 모델·도구 | 상태 | 상세 카드 |
|---|---|---|---|---|---|
|  |  |  |  | 관찰/가설/패턴/검증 |  |

필수 기록:

- 기술이 사용자 경험에 주는 가치.
- 유지할 요소와 변경할 요소.
- 사용하지 않을 조건.
- 모델·버전·확인일.
- 실패 사례와 QA.
- Base 공용 원리와 프로젝트 전용 값.

## 10. 프롬프트 설계

### 공통 구조

```text
목적과 자산 역할
→ 원본·정체성 고정
→ 변경할 표정·포즈·상태
→ 구도와 정보 위계
→ 형태·색·재질·광원
→ 텍스트·레이아웃 슬롯
→ 출력 규격
→ 금지·보호 요소
→ QA와 재생성 기준
```

### 기본 생성 프롬프트

```text

```

### 원본 이미지 편집 프롬프트

```text

```

### 실패 수정 프롬프트

```text

```

### 제어 어휘

- 표정·FACS:
- 시선·머리 방향:
- 포즈·카메라:
- 색·재질·광원:
- 레이아웃·인셋:
- 보호·금지:

> FACS AU와 기타 코드는 자연어를 보조하는 어휘다. 모델의 공식 명령 체계로 가정하지 않는다.

## 11. 생성형 이미지 운영

- 연결 `requirement_id`:
- 사용 모델·서비스·버전:
- 원본 이미지 역할:
- 프롬프트 핵심:
- 텍스트 없는 마스터 여부:
- 편집 가능한 타이포그래피·로고 레이어:
- 후처리:
- manifest 항목:
- 실패·재생성 기준:
- 외부 전송 금지 자료:

이미지 안의 이름·설명·로고는 최종 의미 텍스트로 사용하지 않는 것을 기본값으로 한다. 생성 단계의 문자는 레이아웃 시안으로 보고 실제 제품에서는 편집 가능한 UI·벡터 레이어로 교체한다.

## 12. 변형·응용 계획

- 표정 파생:
- 포즈 파생:
- 키 컬러 변형:
- 캐릭터 포스터·상세 페이지:
- 이벤트·배너 크롭:
- 누락 자산 폴백:

관련 템플릿:

- `templates/planning/EXPRESSION_CONTROL_CARD.md`
- `templates/planning/CHARACTER_PROMO_POSTER_BRIEF.md`

## 13. 금지 요소

-
-
-

## 14. QA

### 기술

- [ ] 크기·비율·알파가 명세와 일치한다.
- [ ] 파일명·ID·manifest가 일치한다.
- [ ] 엔진에서 로드된다.
- [ ] 불필요한 텍스트·워터마크가 없다.

### 시각

- [ ] 축소 화면에서 실루엣과 얼굴이 읽힌다.
- [ ] 다른 자산과 같은 작품으로 보인다.
- [ ] 상태 색과 캐릭터 색이 충돌하지 않는다.
- [ ] 배경과 정보 모듈이 핵심 대상과 UI를 압도하지 않는다.
- [ ] 원본 편집에서 요청한 축 외 요소가 유지된다.

### 경험·운영

- [ ] 사용자가 자산 역할을 즉시 이해한다.
- [ ] 자산 누락 시 폴백으로 기능이 유지된다.
- [ ] 접근성 옵션에서 의미가 보존된다.
- [ ] 이미지와 의미 텍스트가 분리돼 수정·현지화 가능하다.
- [ ] 기술 카드에 모델·버전·검증 상태가 기록된다.
- [ ] 실패 프롬프트와 수정 경로가 남아 있다.
- [ ] 신규 자산·컴포넌트가 연결 `requirement_id`와 Delete Test를 가진다.

## GPT 이미지 생성·검수 연결

- 이미지 단계: `PLANNING_VISUALIZATION / FINAL_VISUAL_CANDIDATE`
- 기록 Template: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`
- 승인 전 생성 결과는 최종 자산이 아니다.
