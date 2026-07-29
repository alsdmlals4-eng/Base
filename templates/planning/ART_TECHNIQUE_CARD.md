# 아트·UI 디자인 기술 카드

## 1. 식별

- 기술명:
- 분류: UI / UX / 캐릭터 / 표정 / 포즈 / 레이아웃 / 생성 / 편집 / 후처리
- 상태: 관찰 / 가설 / 패턴 / 검증 / 제외 / 폐기
- 확인 모델·서비스·버전:
- 확인일:

## 2. 목적

- 해결하는 문제:
- 사용자·플레이어 가치:
- 예상 사용 화면:
- 가장 먼저 전달할 정보·감정:

## 3. 사용 조건

### 사용한다

- 

### 사용하지 않는다

- 

## 4. 입력

- 원본 이미지·디자인 카드:
- 화면비·해상도·실제 크롭:
- 필요한 문구·아이콘·로고:
- 참고할 기존 자산:
- 유사 이미지 레퍼런스와 출처·확인일·권리 상태:
- 유사 프롬프트 레퍼런스와 모델·버전 상태:
- 원하는 결과를 관찰 가능한 문장으로 표현한 목표:
- 권리·출처:

## 5. 유지·변경 계약

### 유지할 요소

- 얼굴·체형:
- 헤어·의상·소품:
- 화풍·선·채색:
- 배경·카메라:

### 변경할 요소

- 표정·시선·머리:
- 포즈:
- 색·재질·광원:
- 구도·정보 슬롯:

## 6. 레퍼런스 기반 생성 전 예측·프롬프트 추론

PromptRecipe와 유사 외부 사례를 사용할 때는 다음 자료를 먼저 사용한다.

- Source Audit: `docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md`
- 상세 기록: `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`

유사 이미지와 유사 프롬프트는 별도 증거로 분석한다. 특정 이미지·캐릭터·작가 스타일·프롬프트 전문을 복제하지 않는다.

```yaml
reference_assisted_forecast:
  similar_image_observations: []
  similar_prompt_observations: []
  decision: ADOPT | ADAPT | TEST | AVOID | REFERENCE_ONLY
  expected_result:
  likely_failures: []
  prediction_confidence: LOW | MEDIUM | HIGH
  confidence_basis: []
  unverified_assumptions: []
```

각 핵심 표현은 다음 표로 프롬프트 추론 근거를 기록한다.

| 원하는 관찰 결과 | 프롬프트 표현 | 추론 근거 | 예상 모델 반응 | 위험·보정 |
|---|---|---|---|---|
|  |  |  |  |  |

생성 뒤에는 예측과 실제 결과를 비교하고, 일치·불일치·예측하지 못한 실패와 수정할 최소 프롬프트 모듈을 기록한다. 실제 생성 없이 `VERIFIED`로 승격하지 않는다.

## 7. 프롬프트 패턴

```text
# Goal

# Asset Context

# Preserve

# Change

# Composition

# Style and Material

# Information Layout

# Output

# Avoid

# QA
```

## 8. 제어 어휘

- 표정·FACS:
- 포즈·카메라:
- 형태·재질:
- 색·광원:
- 레이아웃:
- 금지·보호:

## 9. 프롬프트 사례

### 기본 생성

```text

```

### 원본 이미지 편집

```text

```

### 실패 수정

```text

```

## 10. UI·UX 데이터

- primary_action:
- information_priority:
- layout_pattern:
- interaction_pattern:
- state_variants:
- motion_policy:
- accessibility:
- localization_risk:
- implementation_notes:

## 11. 출력·후처리

- 출력 비율·해상도:
- 알파·배경:
- 텍스트 없는 마스터:
- 편집 레이어:
- 크롭 변형:
- manifest·파일명:

## 12. 실패·위험

| 실패 | 원인 | 수정 방법 | 자동 탈락 여부 |
|---|---|---|---|
|  |  |  |  |

## 13. QA

- [ ] 원본 정체성이 유지된다.
- [ ] 변경 요청한 축만 바뀐다.
- [ ] 얼굴·손·소품·관절 오류가 없다.
- [ ] 실제 사용 크롭에서 핵심 정보가 읽힌다.
- [ ] UI·텍스트·VFX와 결합해도 가독성이 유지된다.
- [ ] 이미지 내 문자와 실제 의미 텍스트가 분리된다.
- [ ] 현지화와 접근성에서 의미가 유지된다.
- [ ] 모델·입력·프롬프트·결과를 재현 가능하게 기록했다.
- [ ] 유사 이미지와 유사 프롬프트를 복제 대상이 아닌 비교 근거로 사용했다.
- [ ] 생성 전에 예상 결과·실패 가능성·확신도·미검증 가정을 기록했다.
- [ ] 핵심 프롬프트 표현마다 원하는 관찰 결과와 추론 근거가 연결된다.
- [ ] 생성 뒤 예측과 실제 결과의 차이와 수정할 최소 모듈을 기록했다.

## 14. 공용·전용 분리

### Base에 남길 원리

- 

### 프로젝트에 남길 실제 값

- 

## 15. 관련 자료

- 관련 method: `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- 관련 Source Audit: `docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md`
- 관련 Recipe Card: `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`
- 관련 skill: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- 관련 case:
- 관련 자산·문서:
