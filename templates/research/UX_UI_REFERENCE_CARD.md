# UX/UI Reference Card

```yaml
reference_id:
title:
publisher:
url:
source_type: official-guideline | official-engine-doc | professional-research | product-case | player-evidence
license:
commercial_use: allowed | restricted | prohibited | unknown
attribution: required | optional | not-required | unknown
modification_and_redistribution: allowed | restricted | prohibited | unknown
godot_compatibility:
maintenance: active | limited | unmaintained | unknown
dependency_removal:
template_or_demo_origin:
published_or_updated_at:
checked_at:
platform_and_version:
problem_being_researched:
project_context:
relevant_principles:
non_applicable_parts:
adoption_decision: ADOPT | ADAPT | AVOID | TEST | IGNORE
transformation_axes:
  player_experience:
  information_architecture:
  interaction:
  visual_language:
  input:
  accessibility:
  godot_implementation:
polishing_evidence:
  affected_priority: P0_BLOCKER | P1_CLARITY | P2_CONSISTENCY | P3_DELIGHT | NOT_APPLICABLE
  feedback_tier: routine | confirming | warning | reward | critical | NOT_APPLICABLE
  expected_repetition_frequency:
  motion_audio_haptic_dependency:
  reduced_motion_mute_haptic_off_path:
  before_after_validation:
visual_generation_integrity:
  visual_question:
  target_screen:
  target_state:
  excluded_scope:
  requested_deliverable_count:
  delivered_independent_count:
  collage_explicitly_requested_or_approved: false
  decision_critical_information:
  semantic_cue_channels:
  scope_fidelity: NOT_RUN | PASS | FAIL | BLOCKED
  human_comprehension: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
external_ui_procurement:
  registry_source:
  source_repository:
  exact_version_or_commit:
  registry_item:
  content_hash:
  license_source_and_hash:
  dependencies:
  scripts_and_postinstall:
  secrets_and_network_access:
  files_added_or_replaced:
  disposable_fixture_result: NOT_RUN | PASS | FAIL | BLOCKED
  target_project_installation: NOT_RUN | PASS | FAIL | BLOCKED
  runtime_build: NOT_RUN | PASS | FAIL | BLOCKED
  actual_render_review: NOT_RUN | PASS | FAIL | BLOCKED
  accessibility_review: NOT_RUN | PARTIAL | PASS | FAIL | BLOCKED
  rollback:
  admission_decision: ADOPT | ADAPT | TEST | REJECT | BLOCKED_UNVERIFIED
motion_interaction_evidence:
  motion_purpose: ORIENT | CONFIRM | PROGRESS | RESULT | WARN | REWARD | DECORATE | NOT_APPLICABLE
  staging_and_first_attention:
  input_accepted_processing_result:
  interruption_and_instant_complete:
  rapid_repeat_and_reentry:
  reduced_motion_mute_haptic_off:
  domain_state_authority:
  target_platform_performance:
copying_prohibited:
transformation_and_validation:
risks_and_biases:
validation_required:
canonical_project_destination:
review_status: DRAFT | REVIEWED | APPLIED | REJECTED | SUPERSEDED
```

## 작성 규칙

1. 현재 플레이어 문제와 연결되지 않은 인기 사례를 수집하지 않는다.
2. 공식 사실, 전문가 해석, 플레이어 자기보고, 행동 증거를 구분한다.
3. 화면·브랜드·고유 문구·자산을 복제하지 않고 원리와 변환 축만 기록한다.
4. 외부 자료를 프로젝트 정본이나 구현 사실보다 높은 권한으로 사용하지 않는다.
5. 수치·크기·시간·효과 강도·반복 횟수는 플랫폼과 실제 플레이 검증 전 `TEST`로 둔다.
6. 링크·최종 확인일·대상 버전이 없으면 현행 근거로 사용하지 않는다.
7. 채택하지 않은 자료도 `AVOID / IGNORE / REJECTED` 이유를 남겨 반복 조사를 막는다.
8. 모션·음향·햅틱을 끈 경로와 같은 조건의 전후 비교가 없으면 폴리싱 효과를 확정하지 않는다.
9. Open-source template or demo references require license, commercial use,
   attribution, modification and redistribution, Godot compatibility,
   maintenance, and dependency removal to be recorded before `ADOPT` or `ADAPT`.
10. A template is evidence and a starting point, never a surface-level copying
    instruction. Record the project transformation and validation result.

## 적용 요약

### 해결하려는 문제

-

### 가져올 원리

-

### 프로젝트에 맞게 바꿀 점

-

### 가져오지 않을 요소

-

### 검증할 행동

-

11. UI 모션 자료는 staging·입력 접수/처리 중/결과·중단·즉시 완료·빠른 반복·재진입·Reduced Motion·mute·haptic-off·도메인 상태 권위를 함께 검토한다.
12. AnimationPlayer·Tween 표현이 구매·보상·저장·진행의 실제 결과를 소유하는 사례는 `AVOID`한다.
13. MCP 연결·Registry 조회·소스 획득·설치·빌드·실제 렌더·접근성·프로젝트 채택을 서로 다른 증거로 기록한다.
14. 공식 브랜드 문서가 아닌 커뮤니티 분석은 `independent_analysis: true`, `official_brand_source: false`로 표시하고 고유 자산·표현을 복제하지 않는다.
15. bounded 생성형 visual은 `visual_question / target_screen / target_state / excluded_scope`를 생성 전에 기록하고, 요청된 N개 결과는 collage가 명시된 경우를 제외하면 독립 deliverable 수량으로 검증한다.
16. decision-critical visual은 색·방향·형태·텍스트/아이콘·밝기/두께·모션 같은 cue 중 프로젝트에 맞는 독립 신호를 비교한다. 이 기록만으로 `human_comprehension`이나 runtime/device PASS를 주장하지 않는다.
