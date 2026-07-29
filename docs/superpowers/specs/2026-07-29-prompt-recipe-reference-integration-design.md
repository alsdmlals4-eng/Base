# PromptRecipe 이미지·프롬프트 레퍼런스 통합 설계

## 1. 목적

PromptRecipe(`https://promptrecipe.pages.dev/`)를 Base의 AI 이미지 기획·프롬프트 작성 작업에서 사용하는 **외부 참고 레퍼런스**로 연결한다.

이 통합의 목적은 사이트의 프롬프트를 그대로 복사하는 것이 아니다. 유사한 이미지와 유사한 프롬프트 사례를 조사해 다음 질문에 답할 수 있는 공용 절차를 만드는 것이다.

> 생성 전에 어떤 결과가 나올 가능성이 높은지 예측하고, 원하는 결과에 더 가까워지도록 어떤 시각 요소와 프롬프트 문장을 왜 선택해야 하는가?

최종적으로 Base는 다음을 지원해야 한다.

- 유사 이미지 사례를 시각 목표·차이·위험을 판단하는 참고 자료로 사용한다.
- 유사 프롬프트 사례를 문장 구조·제어 방식·수정 방법의 참고 자료로 사용한다.
- 생성 전에 예상 결과와 실패 가능성을 가설로 작성한다.
- 원하는 결과에서 역으로 필요한 프롬프트 구성 요소를 추론하고 근거를 남긴다.
- 생성 결과를 예측과 비교해 성공·실패·수정 사례를 학습 자료로 축적한다.
- 특정 이미지·캐릭터·작가 스타일·문장을 그대로 복제하지 않는다.

## 2. 확인된 외부 레퍼런스 범위

PromptRecipe 홈페이지는 다음 성격을 명시한다.

```text
실제 생성 결과
+ 프롬프트 원문
+ 구성 요소 분석
+ 수정 방향
```

현재 홈페이지에서 확인 가능한 주요 예시는 다음과 같다.

- 2D 게임 캐릭터 스프라이트 이미지 프롬프트
- 비 오는 서울 골목 시네마틱 이미지 프롬프트
- 웹소설 표지 이미지 프롬프트
- AI 이미지 프롬프트 작성법
- 장면·피사체·스타일·구도·조명·제약 조건으로 나누는 기본 구조

개별 프롬프트·가이드·Terms·Disclaimer 페이지는 조사 시점에 도구 캐시 오류로 본문을 확인하지 못했다. 따라서 다음 항목은 `UNVERIFIED`로 유지한다.

- 원문 프롬프트 재배포·번역·수정본 공개 허용 범위
- 예시 이미지의 생성 주체와 권리
- 개별 모델명·버전·설정의 정확성
- 동일 입력에서의 재현성
- 사이트 내부 사례 전체의 품질과 일관성

이 제한 때문에 Base에는 사이트 원문 전체를 복제하지 않고 URL·확인일·관찰·적용 판정·재검증 조건만 기록한다.

## 3. Base 현행 구조와 책임 경계

### 3.1 기존 책임

Base에는 이미 다음 구조가 존재한다.

- `designing-art-prompts-and-technique-cards`
  - 이미지 생성·편집 프롬프트
  - 기술 카드
  - 기획 시각화
  - 최종 후보 생성
  - 시각 QA와 승인
- `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
  - 목적·정체성·변경 축·구도·규격·실패 기준 중심의 프롬프트 모듈
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
  - 외부 출처·용도·한계·재검증 조건
- `reviewing-and-validating-project-changes`
  - 외부 자료·AI 결과·문서 변경 검증
- `evolving-project-discipline-skills`
  - 새 Skill보다 기존 Skill mode·reference 통합 우선

따라서 이번 변경에서는 새 광역 Skill을 만들지 않는다.

### 3.2 책임 배치

```text
PromptRecipe 및 유사 외부 사례
→ Source Audit
→ 유사 이미지·유사 프롬프트 비교
→ 생성 전 결과 예측
→ 원하는 결과에서 프롬프트 역추론
→ Prompt Recipe Card
→ 프로젝트 전용 프롬프트·생성
→ 결과 비교·수정·QA
→ Case·Learning Log
```

실행 책임은 기존 `designing-art-prompts-and-technique-cards`가 유지한다. 새 문서는 해당 Skill이 조건부로 읽는 Reference·Template·Case가 된다.

## 4. 핵심 설계 원칙

1. **유사 사례는 정답이 아니라 증거다.** 유사한 이미지나 프롬프트를 그대로 복사하지 않고 관찰 가능한 설계 요소를 추출한다.
2. **생성 전 예측은 보장이 아니라 가설이다.** 모델·버전·입력 이미지·비율·언어에 따라 결과가 달라질 수 있으므로 예상과 확신도를 분리한다.
3. **프롬프트 문장에는 추론 근거가 있어야 한다.** 형용사 나열이 아니라 원하는 관찰 결과와 연결된 이유를 기록한다.
4. **이미지 레퍼런스와 프롬프트 레퍼런스를 분리한다.** 비슷한 이미지가 좋은 프롬프트의 증거는 아니며, 비슷한 프롬프트가 동일한 결과를 보장하지 않는다.
5. **프로젝트 정체성을 먼저 고정한다.** 캐릭터·세계관·UI·게임플레이 정본이 외부 사례보다 우선한다.
6. **채택·변형·회피를 명시한다.** 모든 참고 요소를 `ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY`로 판정한다.
7. **예측과 실제 결과를 비교한다.** 생성 전 예상이 틀린 이유도 공용 학습 자료가 된다.
8. **권리와 유사성을 별도 검수한다.** 특정 상업 IP·작가·캐릭터·로고·고유 구도를 재현하지 않는다.
9. **한 번 성공한 프롬프트는 공용 검증 규칙이 아니다.** 최초 상태는 `OBSERVATION` 또는 `HYPOTHESIS`다.
10. **프로젝트별 실제 값은 Base에 넣지 않는다.** 승인 캐릭터·색상·세계관·실제 프롬프트·생성 이미지는 프로젝트에 남긴다.

## 5. 유사 이미지 참고 절차

### 5.1 목적

유사 이미지는 다음을 예측하고 구체화하기 위한 시각 증거로 사용한다.

- 첫인상과 감정
- 실루엣과 비율
- 카메라 거리와 구도
- 시선 흐름과 정보 위계
- 색상·명도·재질·광원
- 디테일 밀도
- 게임 화면 크기에서의 가독성
- 제작 가능성과 반복 생산성
- 생성 모델이 실패하기 쉬운 부위

### 5.2 비교 단위

가능하면 하나의 이미지가 아니라 서로 다른 출처의 여러 사례를 비교한다.

```yaml
reference_image:
  source_url:
  original_author_or_source:
  checked_at:
  observed_role:
  observable_features:
    silhouette:
    proportions:
    composition:
    camera:
    color_and_value:
    material:
    lighting:
    detail_density:
    readability:
  adopt:
  adapt:
  test:
  avoid:
  copying_risk:
  rights_status:
```

### 5.3 복제 방지

다음은 참고 대상이 아니다.

- 식별 가능한 캐릭터 디자인
- 독특한 의상·문양·소품 조합
- 로고·서명·워터마크
- 특정 작품의 대표 구도
- 특정 작가의 이름만으로 지시하는 스타일 문구

다음처럼 중립적인 시각 언어로 변환한다.

```text
특정 작품 캐릭터처럼
→ 작은 머리 대비 큰 손 장비로 작업 동작을 강조한다.

특정 작가 스타일처럼
→ 선 밀도를 낮추고, 큰 색면과 부드러운 명암 단계로 읽히게 한다.
```

## 6. 유사 프롬프트 참고 절차

### 6.1 목적

유사 프롬프트는 다음을 파악하는 자료로 사용한다.

- 어떤 정보를 앞부분에 배치하는가
- 피사체와 배경을 어떻게 분리하는가
- 구도·카메라·광원을 어떤 어휘로 제어하는가
- 출력 규격과 금지 요소를 어떻게 명시하는가
- 실패한 결과를 어떤 수정 문장으로 교정하는가
- 모델별로 어떤 표현이 실제로 확인됐는가

### 6.2 문장 단위 분석

원문을 장문으로 복제하지 않고 역할 단위로 요약한다.

```yaml
reference_prompt:
  source_url:
  model_as_reported:
  checked_at:
  purpose:
  prompt_modules:
    subject_role:
    scene_context:
    identity_and_preserve:
    action_or_change:
    composition_and_camera:
    form_color_material:
    lighting_and_atmosphere:
    output_spec:
    negative_constraints:
  useful_pattern:
  weak_or_ambiguous_pattern:
  model_specific_risk:
  adaptation_decision:
```

### 6.3 참고와 복사의 경계

참고 가능한 것:

- 섹션 순서
- 정보의 구체성 수준
- 관찰 가능한 제어 축
- 수정 전·후의 논리
- 모델 호환성 기록 방식

복사하지 않는 것:

- 사이트의 프롬프트 전문
- 고유한 캐릭터·설정·카피
- 출처 표시 없는 문장 묶음
- 검증하지 않은 모델별 확정 표현

## 7. 생성 전 결과 예측 계약

### 7.1 목적

이미지를 생성하기 전에 결과를 미리 가설화해 불필요한 반복 생성과 무근거 수정 요청을 줄인다.

예측은 다음 세 층으로 작성한다.

```text
프로젝트가 원하는 관찰 결과
+ 유사 이미지·유사 프롬프트에서 확인한 패턴
+ 현재 모델이 보일 가능성이 높은 반응과 한계
= 생성 전 예상 결과 가설
```

### 7.2 필수 예측 항목

```yaml
pre_generation_forecast:
  target_experience:
  expected_first_impression:
  expected_subject_and_silhouette:
  expected_composition_and_camera:
  expected_color_value_and_lighting:
  expected_material_and_detail_density:
  expected_background_relationship:
  expected_readability_at_target_size:
  likely_successes:
  likely_failures:
  likely_unwanted_variations:
  identity_drift_risk:
  text_logo_anatomy_perspective_risks:
  production_feasibility_risk:
  prediction_confidence: LOW/MEDIUM/HIGH
  confidence_basis:
  unverified_assumptions:
```

### 7.3 예측 언어

사용:

- “다음 결과가 나올 가능성이 높다.”
- “이 문장이 구도를 중앙 대칭으로 유도할 것으로 예상한다.”
- “모델 버전이 확인되지 않아 재질 표현은 낮은 확신도다.”
- “손·무기·문자 영역은 오류 가능성이 높다.”

금지:

- “반드시 이렇게 생성된다.”
- “이 프롬프트면 완벽하게 동일하게 나온다.”
- “모델이 이 태그를 공식 명령으로 이해한다.”
- 실제 생성 없이 `VERIFIED` 또는 `재현 가능`으로 판정한다.

## 8. 원하는 결과에서 프롬프트를 역추론하는 계약

### 8.1 기본 흐름

```text
원하는 플레이어 인상·사용 목적
→ 화면에서 관찰돼야 하는 결과
→ 결과를 만드는 시각 변수
→ 모델에 전달할 프롬프트 모듈
→ 예상되는 모델 반응
→ 실패 가능성·보호 문장
→ 출력 규격과 QA
```

### 8.2 추론 근거 기록

각 핵심 프롬프트 문장은 `원하는 결과 / 선택한 표현 / 선택 이유 / 예상 반응 / 위험`을 가진다.

| 원하는 결과 | 프롬프트 표현 | 추론 근거 | 예상 모델 반응 | 위험·보정 |
|---|---|---|---|---|
| 작은 화면에서도 캐릭터 역할을 즉시 인식 | `clear readable silhouette, one dominant tool shape` | 복잡한 내부 디테일보다 외곽 형태가 축소 시 먼저 남음 | 도구와 몸의 큰 형태가 분리될 가능성 | 장비가 과대화될 수 있어 비율 제한 추가 |
| 차분하지만 외로운 서울 밤 | `wet narrow alley, restrained neon reflections, large dark quiet areas` | 네온 개수보다 어두운 여백과 젖은 반사가 고요한 분위기를 만듦 | 반사광과 어두운 면 대비 증가 | 과도한 사이버펑크화를 피하도록 간판 수 제한 |
| 게임용 반복 제작 가능한 2D 캐릭터 | `front-facing neutral pose, clean separated limbs, simple material groups` | 복잡한 포즈·겹침은 후속 변형과 애니메이션 기준으로 쓰기 어려움 | 신체 부위와 재질 그룹이 분리될 가능성 | 정적인 설정화가 될 수 있어 사용 화면별 동작 변형 필요 |

이 표의 문장은 예시이며 프로젝트 고유 프롬프트 정본이 아니다.

### 8.3 프롬프트 모듈

```text
# Goal and Player/User Value
# Target Asset and Screen
# Project Identity and Canonical Constraints
# Similar Image Observations
# Similar Prompt Observations
# Expected Result Forecast
# Subject and Scene
# Preserve
# Change or Action
# Composition and Camera
# Shape, Color, Material, Lighting
# Output Specification
# Avoid and Protection
# QA and Regeneration Conditions
```

## 9. Prompt Recipe Card

새 Template는 다음 필드를 가진다.

```yaml
recipe_id:
title:
status: OBSERVATION/HYPOTHESIS/PATTERN/VERIFIED

source_audit:
  source_urls: []
  checked_at:
  terms_and_rights_status:
  source_limits:

purpose:
  target_asset:
  target_screen:
  player_or_user_value:
  desired_first_impression:

similar_image_references:
  observations: []
  adopt: []
  adapt: []
  test: []
  avoid: []

similar_prompt_references:
  observed_modules: []
  useful_patterns: []
  ambiguous_or_model_specific_patterns: []

pre_generation_forecast:
  expected_result:
  likely_failures:
  confidence:
  reasoning_basis:

prompt_derivation:
  desired_observation_to_prompt_rows: []
  protected_project_identity: []
  model_specific_assumptions: []

prompt_modules:
  goal_and_value:
  asset_context:
  preserve:
  change:
  composition_and_camera:
  form_color_material_lighting:
  output_spec:
  avoid_and_protection:
  qa:

actual_result_review:
  generation_status: NOT_RUN/RUN
  matched_predictions: []
  missed_predictions: []
  unexpected_results: []
  correction_prompt:
  project_decision:
  evidence_status:
```

## 10. 상태와 증거

### 10.1 지식 상태

- `OBSERVATION`: 외부 사례에서 패턴을 관찰했지만 직접 실행하지 않음
- `HYPOTHESIS`: 프로젝트에서 시험할 가치가 있는 예측·프롬프트 구조
- `PATTERN`: 같은 조건에서 반복 결과를 확인함
- `VERIFIED`: 여러 자산·조건에서 QA와 실제 화면 검증을 통과함

### 10.2 예측 검증 상태

- `PREDICTION_NOT_TESTED`
- `PREDICTION_PARTIALLY_MATCHED`
- `PREDICTION_MATCHED`
- `PREDICTION_FAILED`
- `MODEL_OR_CONTEXT_CHANGED_RETEST_REQUIRED`

### 10.3 결과 비교

생성 후에는 다음을 기록한다.

```text
예상과 일치한 요소
→ 예상과 다르게 나온 요소
→ 예측하지 못한 실패
→ 프롬프트 문장별 영향 추정
→ 수정할 최소 모듈
→ 재생성 결과
```

한 번에 여러 축을 모두 바꾸지 않고, 원인 판별이 필요하면 핵심 변수 하나 또는 관련 모듈 하나씩 수정한다.

## 11. 정보 구조 변경안

### 11.1 신규 파일

- `docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md`
  - PromptRecipe의 확인 범위·권리·한계·재검증 조건
- `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`
  - 유사 이미지·유사 프롬프트·생성 전 예측·역추론·결과 비교 Template
- `tests/test_prompt_recipe_reference_contract.py`
  - Source Audit·Template·Skill·Documentation Map·Workflow 연결 검증

개별 PromptRecipe 페이지의 본문과 권리 조건을 확인할 수 있을 때만 Pilot Case를 추가한다.

- `docs/knowledge/cases/PROMPT_RECIPE_2D_GAME_SPRITE_ADAPTATION_CASE.md`
  - 초기 상태 `OBSERVATION` 또는 `HYPOTHESIS`
  - 사이트 원문 프롬프트 전문은 저장하지 않음

### 11.2 갱신 파일

- `docs/knowledge/README.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
- `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- `skills/SKILL_REGISTRY.json`
- `skills/SKILL_LEARNING_LOG.md`
- `docs/CHANGELOG.md`
- `.github/workflows/validate-evidence-knowledge.yml`

### 11.3 변경하지 않는 범위

- 새 광역 Skill
- `AGENTS.md`
- `START_HERE.md`
- `docs/OPERATING_MODEL.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- Godot 코드·Scene·Resource
- 개별 프로젝트의 실제 이미지·프롬프트·승인 자산
- 프로젝트 Google Sheets 실제 수정

구현 중 상위 진입점이 없으면 발견성이 확보되지 않는다는 증거가 생긴 경우에만 `START_HERE.md` 등의 변경을 별도 finding으로 제안한다.

## 12. 프로젝트 적용 흐름

```text
프로젝트 정본·사용 화면·플레이어 경험 확인
→ 원하는 결과를 관찰 가능한 문장으로 정의
→ 유사 이미지와 유사 프롬프트 사례 수집
→ 채택·변형·시험·회피 분리
→ 생성 전 결과 예측
→ 원하는 결과에서 프롬프트 모듈 역추론
→ 사용자가 이미지 생성을 요청한 경우 생성
→ 예상과 실제 결과 비교
→ 최소 수정 프롬프트 작성
→ 실제 화면·권리·제작성 QA
→ 프로젝트 승인 원장 반영
→ 반복 검증 가치가 있으면 Base Case 또는 BCP 후보
```

유사 사례 조사는 사용자가 이미 승인한 이미지나 프로젝트 정체성을 교체하는 권한이 없다.

## 13. 완료 기준

1. `프롬프트 레시피`, `유사 이미지 참고`, `유사 프롬프트 참고`, `생성 전 결과 예측`, `프롬프트 추론 근거` 요청이 기존 아트 프롬프트 Skill로 라우팅된다.
2. 새 광역 Skill이 추가되지 않는다.
3. 외부 사이트 원문 전문을 복제하지 않는다.
4. Source Audit에 URL·확인일·권리 상태·미검증·재검증 조건이 존재한다.
5. Template가 유사 이미지와 유사 프롬프트를 별도 필드로 관리한다.
6. Template가 생성 전 예상 결과·실패 가능성·확신도·추론 근거를 요구한다.
7. 핵심 프롬프트 문장이 원하는 관찰 결과와 연결된다.
8. 생성 결과를 예측과 비교하는 상태와 필드가 존재한다.
9. 실제 생성하지 않은 항목은 `VERIFIED`로 표시할 수 없다.
10. Base 공용 원리와 프로젝트 전용 값이 분리된다.
11. Documentation Map·Knowledge README·Skill·Registry·Template·Test·Workflow가 연결된다.
12. 기존 Evidence Knowledge와 아트 프롬프트 계약이 회귀하지 않는다.

## 14. 검증 설계

```text
신규 계약 테스트 작성
→ 구현 전 RED 확인
→ Source Audit·Template·Method·Skill·Registry·라우팅 구현
→ 신규 계약 GREEN
→ 기존 Evidence Knowledge 회귀
→ canonical reference freshness
→ JSON·Markdown·Workflow 정적 검사
→ 변경 파일 범위 대조
→ PR Required Checks
→ 병합 후 main 재검사
```

전용 테스트는 최소한 다음을 확인한다.

- 신규 Source Audit와 Template 존재
- Template의 `similar image`, `similar prompt`, `pre-generation forecast`, `reasoning basis`, `actual result review` 계약
- 복제 금지·권리 미검증·예측 비보장 문구
- 기존 `designing-art-prompts-and-technique-cards` Skill 연결
- Registry trigger 연결
- Documentation Map·Knowledge README 발견성
- Evidence Knowledge Workflow에서 테스트 실행
- 신규 광역 Skill 부재
- 실제 생성 전 `VERIFIED` 금지

## 15. 위험과 대응

| 위험 | 대응 |
|---|---|
| 외부 프롬프트 원문 무단 복제 | URL·구조·관찰·판정만 기록하고 전문 저장 금지 |
| 비슷한 이미지를 그대로 모방 | 여러 출처 비교, 중립적 시각 언어 변환, AVOID 항목 기록 |
| 예측을 보장처럼 표현 | 확신도·미검증 가정·모델 조건 필수화 |
| 프롬프트 추론을 사후 합리화 | 생성 전에 예측과 근거를 먼저 고정하고 결과와 대조 |
| 모델별 표현을 공통 공식으로 오인 | 모델·버전·확인일·재검증 조건 기록 |
| 참고 자료가 프로젝트 정본을 대체 | 프로젝트 정본과 승인 자산 우선순위 명시 |
| Template 과대화 | Skill 본문에는 핵심 흐름만 두고 상세 필드는 조건부 Template로 분리 |
| 한 번의 성공을 공용 규칙으로 승격 | OBSERVATION/HYPOTHESIS부터 시작하고 반복 검증 요구 |

## 16. 사용자 승인 사항

2026-07-29 사용자 요청으로 다음 방향을 승인된 설계 입력으로 사용한다.

- PromptRecipe를 Base의 참조 레퍼런스로 사용한다.
- 유사한 이미지와 유사한 프롬프트를 참고하는 예시 자료로 사용한다.
- 이미지 생성 전 예상 결과를 제시한다.
- 원하는 결과에 가까운 프롬프트를 추론한 근거를 설명한다.
- Base 현행 Skill·작업 구조를 먼저 이해하고 기존 구조에 통합한다.

## 17. 구현 전 사용자 검토 게이트

이 문서가 사용자 검토를 통과한 뒤 `writing-plans`로 상세 구현 계획을 작성한다. 구현 계획 승인 전에는 위 신규·갱신 파일을 실제로 변경하지 않는다.
