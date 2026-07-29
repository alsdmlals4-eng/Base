# PromptRecipe 이미지·프롬프트 레퍼런스 Source Audit

```yaml
source_id: AI-PROMPT-RECIPE-001
source_url: https://promptrecipe.pages.dev/
source_status: PARTIALLY_VERIFIED
source_decision: REFERENCE_ONLY
checked_at: 2026-07-29
owner_skill: skills/designing-art-prompts-and-technique-cards/SKILL.md
project_authority: NONE
implementation_authority: NONE
```

## 1. 목적

PromptRecipe를 Base의 이미지 생성·편집 프롬프트 작업에서 사용하는 **외부 참고 레퍼런스**로 감사한다.

이 자료의 역할은 완성 프롬프트를 복사해 주는 것이 아니다. 유사 이미지와 유사 프롬프트의 관찰 가능한 구조를 비교해 다음을 지원하는 것이다.

- 이미지 생성 전 결과 예측과 실패 가능성 가설 작성
- 원하는 결과에서 프롬프트 구성 요소를 역추론
- 각 핵심 표현을 선택한 프롬프트 추론 근거 기록
- 생성 뒤 예측과 실제 결과 비교
- 성공·실패·수정 사례의 학습 자료화

외부 사례는 프로젝트 정본, 승인 이미지, 실제 구현 상태보다 높은 권한을 갖지 않는다.

## 2. 확인된 범위

2026-07-29 홈페이지에서 다음 구조와 항목을 확인했다.

```text
실제 생성 결과
+ 사용한 프롬프트
+ 프롬프트 구성 요소 분석
+ 수정 방향
```

홈 화면에서 확인한 예시 범위:

- 2D 게임 캐릭터 스프라이트 이미지 프롬프트
- 비 오는 서울 골목의 시네마틱 이미지 프롬프트
- 웹소설 표지 이미지 프롬프트
- AI 이미지 프롬프트 작성법
- 장면·피사체·스타일·구도·조명·제약 조건 중심의 기본 구조

이 관찰은 사이트의 **사례 제시 방식**을 확인한 것이며, 개별 프롬프트의 품질·권리·재현성을 검증한 결과가 아니다.

## 3. 미검증 범위

다음은 현재 `UNVERIFIED`다.

- 개별 프롬프트·가이드·Terms·Disclaimer 전체 본문
- 원문 프롬프트의 재배포·번역·수정본 공개 허용 범위
- 예시 이미지의 생성 주체·원본·라이선스
- 개별 모델명·버전·시드·설정의 정확성
- 동일 입력에서의 재현성
- 사례별 성공률과 실패 표본
- 사이트 전체 콘텐츠의 최신성·일관성

따라서 Base에는 사이트의 프롬프트 원문 전문을 복제하지 않는다. URL, 확인일, 관찰 내용, 사용 한계, 적용 판정, 재검증 조건만 기록한다.

## 4. 유사 이미지 참고 원칙

유사 이미지는 결과물을 복제하기 위한 목표 이미지가 아니라, 원하는 시각 결과를 관찰 가능한 변수로 바꾸는 참고 자료다.

### 4.1 관찰 항목

```yaml
similar_image_reference:
  source_url:
  original_author_or_source:
  checked_at:
  rights_status: VERIFIED | PARTIAL | UNVERIFIED
  observable_features:
    first_impression:
    silhouette:
    proportions:
    composition:
    camera_distance_and_angle:
    color_and_value:
    material:
    lighting:
    detail_density:
    background_relationship:
    target_size_readability:
    production_repeatability:
  decision:
    adopt: []
    adapt: []
    test: []
    avoid: []
  copying_risk:
```

### 4.2 사용 방식

- 가능하면 서로 다른 출처의 여러 이미지를 비교한다.
- 특정 캐릭터·의상·소품·구도를 복제하지 않고 공통 설계 원리를 추출한다.
- 실루엣, 비율, 명도, 재질, 광원, 여백처럼 중립적이고 관찰 가능한 시각 언어로 변환한다.
- 작은 게임 화면, HUD·VFX 중첩, 크롭, 현지화와 반복 제작 가능성을 함께 검토한다.
- 원작자·원출처·권리 상태를 확인하지 못하면 `UNVERIFIED`로 유지한다.

### 4.3 금지

- 식별 가능한 상업 캐릭터 디자인 재현
- 독특한 의상·문양·장식 조합 복제
- 로고·서명·워터마크 사용
- 특정 작품의 대표 구도 그대로 재현
- 특정 작가 이름만으로 스타일을 지시

예시 변환:

```text
특정 작가처럼 그린다
→ 큰 색면, 낮은 선 밀도, 제한된 명암 단계와 부드러운 가장자리로 읽히게 한다.
```

## 5. 유사 프롬프트 참고 원칙

유사 프롬프트는 동일 결과를 보장하는 주문이 아니라, 정보를 어떤 순서와 구체성으로 배치하는지 분석하는 참고 자료다.

### 5.1 관찰 항목

```yaml
similar_prompt_reference:
  source_url:
  checked_at:
  model_as_reported:
  model_version_status: VERIFIED | PARTIAL | UNVERIFIED
  purpose:
  observed_modules:
    subject_and_role:
    scene_context:
    preserve:
    change_or_action:
    composition_and_camera:
    shape_color_material:
    lighting_and_atmosphere:
    output_spec:
    avoid_and_protection:
  useful_pattern:
  ambiguous_pattern:
  model_specific_risk:
  adaptation_decision: ADOPT | ADAPT | TEST | AVOID | REFERENCE_ONLY
```

### 5.2 참고 가능한 것

- 프롬프트 모듈의 순서
- 정보의 구체성 수준
- 구도·카메라·광원·재질의 관찰 가능한 제어 축
- 유지 요소와 변경 요소를 분리하는 방식
- 실패 결과를 수정하는 전후 논리
- 모델·버전·확인일을 기록하는 방식

### 5.3 복제하지 않는 것

- 사이트의 프롬프트 원문 전문
- 고유 캐릭터·세계관·카피·문장 묶음
- 출처 표시가 없는 프롬프트
- 확인되지 않은 모델별 제어 문구를 공용 공식으로 확정하는 표현

## 6. 생성 전 결과 예측의 증거 한계

생성 전 결과 예측은 다음 세 근거를 결합한 **가설**이다.

```text
프로젝트가 원하는 관찰 결과
+ 유사 이미지·유사 프롬프트에서 확인한 패턴
+ 현재 모델·입력·비율·언어에서 예상되는 반응과 한계
= 생성 전 예상 결과 가설
```

필수 예측:

- 첫인상과 감정
- 주 피사체·실루엣·비율
- 구도·카메라·시선 흐름
- 색·명도·재질·광원
- 배경과 피사체 관계
- 목표 화면 크기에서의 가독성
- 성공 가능성이 높은 요소
- 손·관절·무기·문자·로고·원근·광원 오류 가능성
- 정체성 drift와 제작 가능성 위험
- `LOW / MEDIUM / HIGH` 예측 확신도
- 확신도 근거와 미검증 가정

예측은 결과 보장이 아니다. 모델·버전·원본 이미지·비율·언어·서비스 설정이 달라지면 다시 검증한다.

## 7. 원하는 결과에서 프롬프트를 역추론하는 방법

```text
플레이어·사용자에게 줄 인상과 사용 목적
→ 화면에서 관찰돼야 하는 결과
→ 그 결과를 만드는 시각 변수
→ 모델에 전달할 프롬프트 표현
→ 표현을 선택한 reasoning basis
→ expected model response
→ risk and correction
→ 출력 규격과 QA
```

각 핵심 문장은 다음 연결을 가진다.

| 필드 | 질문 |
|---|---|
| `desired_observation` | 결과 이미지에서 실제로 무엇을 볼 수 있어야 하는가? |
| `prompt_expression` | 모델에 어떤 자연어 표현을 전달할 것인가? |
| `reasoning_basis` | 유사 사례·시각 원리·프로젝트 제약 중 무엇이 근거인가? |
| `expected_model_response` | 해당 표현이 어떤 변화 가능성을 높일 것으로 예상하는가? |
| `risk_and_correction` | 과장·누락·drift가 생기면 어떤 최소 문장을 수정할 것인가? |

형용사를 많이 나열하는 것만으로 추론 근거가 되지 않는다.

## 8. 권리·복제·유사성 경계

- 원문 전문을 복제하지 않는다.
- 예시 이미지 자체를 Base 자산으로 가져오지 않는다.
- 특정 작가, 특정 상업 IP, 식별 가능한 캐릭터, 로고, 서명, 고유 구도를 재현하지 않는다.
- 여러 출처에서 공통 원리를 추출하고 프로젝트 정체성에 맞게 `ADAPT`한다.
- 권리 상태가 불명확하면 상업 자산 채택이 아니라 `REFERENCE_ONLY`로 유지한다.
- 외부 자료의 이미지와 문장은 프로젝트 승인 자산을 교체할 권한이 없다.

## 9. Base와 프로젝트 책임 경계

### Base 공용

- Source Audit와 권리·복제 경계
- 유사 이미지·유사 프롬프트 분석 필드
- 생성 전 결과 예측·확신도·미검증 가정
- 원하는 결과에서 프롬프트를 역추론하는 구조
- 예측과 실제 결과 비교 상태
- 실패·수정·재검증 기준

### 프로젝트 전용

- 실제 캐릭터·세계관·색·문구·수치·화면
- 사용 모델·버전·계정·비용·시드·서비스 설정
- 실제 생성 프롬프트와 원본 이미지
- 생성 결과·수정 결과·승인·기각 기록
- 인게임 캡처·구현 가능성·런타임 검증
- Asset ID·GitHub 경로·Sheet 승인 원장

## 10. 지식 상태와 완료 주장

- `OBSERVATION`: 외부 사례에서 구조를 관찰했으나 직접 생성하지 않음
- `HYPOTHESIS`: 프로젝트에서 시험할 가치가 있는 예측·프롬프트 구조
- `PATTERN`: 같은 조건에서 반복 결과를 확인함
- `VERIFIED`: 여러 자산·조건에서 QA와 실제 화면 검증을 통과함

실제 생성 없이 `VERIFIED`, 재현 가능, 최종 자산, 실제 화면 통과로 판정하지 않는다. 한 번의 성공은 먼저 관찰 또는 가설로 기록한다.

## 11. 재검증 조건

다음이 바뀌면 원문과 실제 결과를 다시 확인한다.

- PromptRecipe 사이트 구조·이용 조건·권리 고지
- 개별 프롬프트 페이지 접근 가능 여부
- 이미지 모델·서비스·버전·안전 정책
- 입력 이미지·화면비·해상도·언어
- 프로젝트 아트 정본·승인 이미지·사용 화면
- 상업 사용·배포·현지화 범위
- 동일 패턴에서 예측과 실제 결과가 반복적으로 불일치함

## 12. 적용 Template

- `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`
- `templates/planning/ART_TECHNIQUE_CARD.md`
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`
