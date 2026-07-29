# AI Image Prompt Recipe Card

```yaml
recipe_id:
title:
status: OBSERVATION | HYPOTHESIS | PATTERN | VERIFIED
owner_project:
owner_document:
created_at:
updated_at:
```

## 1. Source Audit

```yaml
source_audit:
  source_urls: []
  checked_at:
  source_status: VERIFIED | PARTIAL | UNVERIFIED
  terms_and_rights_status: VERIFIED | PARTIAL | UNVERIFIED
  source_limits:
  reproduction_boundary:
  source_decision: ADOPT | ADAPT | TEST | AVOID | REFERENCE_ONLY
```

- [ ] 원문 전문을 복제하지 않았다.
- [ ] 예시 이미지·로고·서명·워터마크를 Base 또는 프로젝트 자산으로 가져오지 않았다.
- [ ] 특정 작가·상업 IP·식별 가능한 캐릭터·고유 구도를 재현하지 않았다.
- [ ] 권리 상태가 불명확하면 `REFERENCE_ONLY`로 유지했다.

## 2. Purpose and Target Experience

```yaml
purpose:
  target_asset:
  target_screen:
  target_platform:
  player_or_user_value:
  desired_first_impression:
  desired_emotion:
  primary_information:
  production_use:
```

### Observable target

> 결과 이미지에서 실제로 관찰할 수 있어야 하는 내용을 한 문장으로 쓴다.

- 원하는 관찰 결과:
- 허용 가능한 변형:
- 허용하지 않는 변형:
- 프로젝트 정체성·Decision·정본 경로:

## 3. Similar Image References

```yaml
similar_image_references:
  - source_url:
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

### Cross-reference synthesis

- 여러 출처에서 반복된 공통 원리:
- 서로 충돌하는 특징:
- 프로젝트에 채택할 요소:
- 프로젝트에 맞게 변형할 요소:
- 시험이 필요한 요소:
- 복제 방지를 위해 회피할 요소:

## 4. Similar Prompt References

```yaml
similar_prompt_references:
  - source_url:
    checked_at:
    model_as_reported:
    model_version_status: VERIFIED | PARTIAL | UNVERIFIED
    purpose:
    observed_modules:
      subject_and_role:
      scene_context:
      identity_and_preserve:
      change_or_action:
      composition_and_camera:
      shape_color_material:
      lighting_and_atmosphere:
      output_spec:
      avoid_and_protection:
    useful_patterns: []
    ambiguous_or_model_specific_patterns: []
    adaptation_decision: ADOPT | ADAPT | TEST | AVOID | REFERENCE_ONLY
```

### Prompt-pattern synthesis

- 앞부분에 고정할 안정적인 규칙:
- 뒤쪽에 둘 프로젝트 가변값:
- 모델별로 재검증할 표현:
- 사용하지 않을 모호한 표현:
- 실패 결과를 수정한 전후 논리:

## 5. Pre-generation Forecast

생성 전 결과 예측은 결과 보장이 아니라 가설이다.

```yaml
pre_generation_forecast:
  target_experience:
  expected_first_impression:
  expected_subject_and_silhouette:
  expected_proportions:
  expected_composition_and_camera:
  expected_color_value_and_lighting:
  expected_material_and_detail_density:
  expected_background_relationship:
  expected_readability_at_target_size:
  likely_successes: []
  likely_failures: []
  likely_unwanted_variations: []
  identity_drift_risk:
  anatomy_weapon_text_logo_perspective_risks: []
  production_feasibility_risk:
  prediction_confidence: LOW | MEDIUM | HIGH
  confidence_basis: []
  unverified_assumptions: []
```

### Forecast statement

- 가능성이 높은 결과:
- 낮은 확신도의 요소:
- 가장 먼저 확인할 실패:
- 재생성 전에 유지할 요소:

## 6. Prompt Derivation

각 핵심 표현은 원하는 관찰 결과와 연결한다.

```yaml
prompt_derivation:
  desired_observation_to_prompt:
    - desired_observation:
      prompt_expression:
      reasoning_basis:
      expected_model_response:
      risk_and_correction:
  protected_project_identity: []
  model_specific_assumptions: []
```

| 원하는 관찰 결과 | 프롬프트 표현 | reasoning_basis | expected_model_response | risk_and_correction |
|---|---|---|---|---|
|  |  |  |  |  |

### Reasoning checks

- [ ] 핵심 형용사·구도·광원 표현마다 관찰 가능한 이유가 있다.
- [ ] 유사 이미지의 표면을 복사하지 않고 시각 원리를 변환했다.
- [ ] 유사 프롬프트의 문장 전문을 복사하지 않고 모듈 구조만 참고했다.
- [ ] 프로젝트 정체성·승인 이미지·사용 화면을 외부 사례보다 우선했다.
- [ ] 모델별 가정을 공식 명령이나 보장으로 표현하지 않았다.

## 7. Prompt Modules

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
# Information Layout
# Output Specification
# Avoid and Protection
# QA and Regeneration Conditions
```

### Draft prompt

```text

```

### Protected elements

- 얼굴·헤어·의상·소품:
- 프로젝트 색·형태·재질 언어:
- 화면·HUD·크롭 조건:
- 변경 금지 문자·로고·상징:

### Avoid and protection

- 손·관절·무기:
- 문자·로고·서명:
- 원근·광원:
- 과도한 IP·작가 유사성:
- 배경과 피사체 혼합:
- 목표 화면 크기에서의 정보 과밀:

## 8. Generation Record

```yaml
generation_record:
  generation_status: NOT_RUN | RUN
  model_and_version:
  tool_or_surface:
  input_images: []
  aspect_ratio:
  resolution:
  seed_or_settings:
  prompt_version:
  generated_at:
  output_asset_ids: []
```

실제 생성 없이 `VERIFIED`, 재현 가능, 최종 자산, 실제 화면 통과로 판정하지 않는다.

## 9. Actual Result Review

```yaml
actual_result_review:
  generation_status: NOT_RUN | RUN
  prediction_status: PREDICTION_NOT_TESTED | PREDICTION_PARTIALLY_MATCHED | PREDICTION_MATCHED | PREDICTION_FAILED | MODEL_OR_CONTEXT_CHANGED_RETEST_REQUIRED
  matched_predictions: []
  missed_predictions: []
  unexpected_results: []
  identity_drift:
  target_size_readability:
  anatomy_text_logo_perspective_findings: []
  production_feasibility:
  rights_and_similarity_review:
  correction_prompt:
  changed_prompt_module:
  project_decision: ADOPT | ADAPT | TEST | AVOID | REJECT | HOLD
  evidence_status: NOT_RUN | PARTIAL | PASSED | FAILED
```

### Prediction comparison

- 예상과 일치한 요소:
- 예상과 다르게 나온 요소:
- 예측하지 못한 실패:
- 영향을 준 것으로 추정되는 프롬프트 문장:
- 다음 반복에서 변경할 최소 모듈:
- 다음 반복에서 유지할 모듈:

## 10. QA Gates

### Project alignment

- [ ] 플레이어·사용자 가치와 사용 화면이 명확하다.
- [ ] 프로젝트 정본·Decision·승인 이미지와 충돌하지 않는다.
- [ ] 외부 사례가 프로젝트 정체성을 교체하지 않는다.

### Visual result

- [ ] 목표 화면 크기와 실제 크롭에서 핵심 실루엣·정보가 읽힌다.
- [ ] 색·명도·재질·광원이 다른 승인 자산과 일관된다.
- [ ] 배경·HUD·VFX 위에서 피사체가 구분된다.
- [ ] 손·관절·무기·문자·로고·원근·광원 오류를 검수했다.

### Production feasibility

- [ ] 후속 표정·포즈·애니메이션·UI 변형에 재사용 가능하다.
- [ ] 알파·크롭·해상도·현지화·후처리 계획이 있다.
- [ ] 반복 제작 비용과 모델 의존성을 기록했다.

### Rights and evidence

- [ ] 원출처·확인일·권리 상태를 기록했다.
- [ ] 특정 작가·IP·캐릭터·고유 구도를 복제하지 않았다.
- [ ] 생성 전 가설과 실제 생성 결과를 분리했다.
- [ ] 사람이 확인하지 않은 결과를 사람 검수 완료로 표시하지 않았다.

## 11. Knowledge State Decision

```yaml
knowledge_state_decision:
  current_status: OBSERVATION | HYPOTHESIS | PATTERN | VERIFIED | EXCLUDED
  evidence:
  limitations:
  reuse_conditions:
  do_not_use_when:
  next_validation:
  base_promotion_candidate: YES | NO
```

한 번의 성공은 먼저 `OBSERVATION` 또는 `HYPOTHESIS`로 기록한다. 여러 자산·모델·프로젝트에서 반복 검증되기 전에는 Base 강제 규칙으로 승격하지 않는다.
