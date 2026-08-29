# Candidate-First Visual · Autonomous Quality Loop Design

## 상태

```yaml
date: 2026-08-29
proposal: BCP-2026-049-candidate-first-visual-and-autonomous-quality-loop
approval_ref: 2026-08-29 current user instruction
base_main: f80ae737619d300cedf906b544961066ed373312
implementation_state: RED_CONTRACT_FIRST
incremental_paid_cost: 0
```

## 목표

이 설계는 이미지 후보 제작 전의 반복 승인 정지를 줄이면서도 최종 시각 확정과 제품 구현의 사람 통제를 유지한다. 동시에 material 시스템·구조를 인터넷 일반론이 아니라 current official/primary evidence와 실제 프로젝트 consumer에서 검증하고, 작업 후 적대적 검토·교정·학습 환류를 실행 가능한 계약으로 만든다.

## 상위 불변식

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
IMPLEMENTATION_FEASIBILITY_BEFORE_COMMITMENT
LONG_TERM_QUALITY_OVER_LOCAL_SPEED
MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL
ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
INCIDENT_SOLUTION_LESSON_AUTOMATION_LOOP
```

### 후보 선제작 경계

```text
VISUAL_NEED_CONFIRMED
→ CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
→ ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
→ EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
→ BOUNDED_BRIEF_READY
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ OBJECTIVE_QA_AND_BOUNDED_CORRECTION
→ PRESENT_FOR_USER_FINAL_LOCK
```

후보 제작은 current project identity, current approved visual direction, 실제 또는 명시적으로 계획된 consumer, 규격과 bounded scope가 확인된 경우에만 preauthorized다. 방향 충돌·원본 미열람·consumer 부재는 자동 상상으로 채우지 않는다.

```text
GENERATED_CANDIDATE
!= USER_FINAL_LOCKED
!= PROJECT_ASSET_APPROVED
!= CANON_REGISTERED
!= IMPLEMENTED
!= RUNTIME_VERIFIED
```

`NO_AUTOMATIC_SCOPE_EXPANSION`을 적용한다. 한 후보와 객관적 결함의 bounded correction을 넘는 다른 캐릭터·화면·variant·batch는 별도 requirement로 계산한다. final lock, repository asset promotion, runtime implementation은 프로젝트의 current Decision·manifest·Blueprint gate를 따른다.

### Blueprint와 구현 경계

```text
CANDIDATE_PRODUCTION_MAY_PRECEDE_BLUEPRINT_FINAL_REVIEW
CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY
NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL
```

Blueprint 검토에 필요한 이미지는 후보로 먼저 만들 수 있다. 그러나 생성 성공이나 final visual lock만으로 새 implementation package가 승인되지 않는다. exact Blueprint revision에 대한 사용자 최종 승인과 프로젝트별 implementation authority는 그대로 유지한다.

## 구현 가능성 Gate

material 기획·시스템·데이터·UI/UX·asset pipeline·automation 구조는 다음 receipt 없이 확정하지 않는다.

```yaml
IMPLEMENTATION_FEASIBILITY_RECEIPT:
  current_owner_and_actual_implementation:
  current_official_primary_sources: []
  directly_relevant_success_failure_or_mixed_cases: []
  materially_distinct_alternatives: []
  project_fit_and_player_value:
  actual_consumer_and_integration_boundary:
  scene_node_resource_script_data_state_signal_save_structure:
  test_debug_runtime_performance_platform_constraints:
  rights_cost_security_constraints:
  rollback_migration_and_evidence_ceiling:
  classification: FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

`MECHANICAL_NO_EXTERNAL_DEPENDENCY`는 외부 사실이 결과를 바꿀 수 없는 순수 기계 변경에서만 이유와 범위를 기록하고 사용할 수 있다. 새 gameplay, player-facing UX, runtime asset, dependency, platform, security, rights, implementation direction에는 적용하지 않는다.

## 장기 품질 기준

```text
LONG_TERM_QUALITY_OVER_LOCAL_SPEED
ROOT_CAUSE_AND_REUSE_BEFORE_REPEATED_MANUAL_PATCH
MINIMUM_SUFFICIENT_COMPLEXITY
SPECULATIVE_OVERENGINEERING_REJECTED
PLAYABLE_OR_OPERATIONAL_VALUE_OVER_DOCUMENT_VOLUME
```

선택 기준:

1. player/user value와 제품 완성도.
2. 정본 명확성·consumer ownership·rollback.
3. 재작업·수동 개입·오류율 감소.
4. 테스트·디버깅·runtime evidence 확보 가능성.
5. 유지보수·확장·다른 프로젝트 재사용 가치.
6. 현재 범위에 필요한 최소 충분 복잡도.

빠른 임시 수정이 반복 비용을 만든다면 root cause를 고친다. 반대로 미래 가능성만을 위한 범용 framework, 새 owner·dashboard·tool 증식은 거절한다.

## 사용자 관여 최소화와 안전 제어

```text
MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL
```

AI가 기본적으로 연속 수행한다.

- fresh authority·actual implementation·open PR 복원.
- reuse-first와 current research.
- 대안 비교와 feasibility classification.
- bounded visual candidate와 objective QA.
- 허용 범위의 문서·test·정본 교정과 readback.
- 남은 작업 재계산과 회귀 검증.
- 문제·원인·해결·재발 방지·Base 승격 후보 환류.

사용자에게 남긴다.

- 핵심 재미·경제·서사·Art Direction과 제품 의미 변경.
- 객관적 우열이 없는 취향 선택과 visual final lock.
- 비용·외부 공개·배포·보안·권한·비가역 삭제.
- 기존 승인 범위를 넘는 scope expansion.

## 실제 적대적 검토 계약

```text
ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
FULL_LOOP_COUNT_MINIMUM: 5
EXECUTION_EVIDENCE_REQUIRED
CORRECT_VALIDATED_FINDINGS
CLEAN_REVIEW_EXIT
```

각 full loop는 같은 final-state lineage를 전체 범위로 다시 공격한다.

```text
FULL_SCOPE_REVIEW
→ FIND
→ VALIDATE_CRITIQUE
→ CORRECT_VALIDATED_FINDINGS
→ VERIFY_AND_REGRESSION_RECHECK
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE_ATTACK
```

각 회차에는 input head, evidence delta, findings, validated findings, correction, verification, better alternative, long-term fit, unresolved, output head를 기록한다. 검토 문구만 있고 실행·diff·test/readback evidence가 없으면 완료가 아니다.

## 학습·자동화 환류

```text
INCIDENT_SOLUTION_LESSON_AUTOMATION_LOOP
```

```text
problem
→ reproducible evidence
→ root cause
→ minimal correction
→ regression prevention
→ project owner and readback
→ reusable lesson candidate
→ Base BCP after cross-project validation
```

대화 기억을 학습 정본으로 사용하지 않는다. 반복 가능한 교훈은 owner 문서, test, validator, template, checklist 또는 BCP로 남긴다.

## 영향 파일

```yaml
base_owners:
  - docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md
  - docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md
  - docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
active_templates:
  - templates/custom-instructions.gpt.md
  - templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
regression_contract:
  - tests/test_candidate_first_autonomous_quality_contract.py
review_evidence:
  - docs/reviews/2026-08-29-candidate-first-autonomous-quality-adversarial-review.md
```

## 호환성

- `TEXT_BRIEF_STOP_REQUIRED`와 `ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE`는 active behavior가 아니라 `RETIRED_COMPATIBILITY_ALIAS`로만 남길 수 있다.
- host/system/tool이 현재 대화에서 명시 이미지 요청을 요구하면 `HOST_PLATFORM_PRECEDENCE`로 fail closed한다.
- image-model-only, actual consumer, rights/provenance, one bounded candidate, final lock, manifest와 runtime evidence 경계는 유지한다.
- 기존 historical proposal·PR·case의 과거 문구는 history로 보존한다.

## 롤백

구현은 하나의 squash commit으로 되돌릴 수 있게 한다. rollback 시 후보를 자동 승격하지 않으며, 현재 사용자 승인 목표와의 차이·다음 안전 경계를 별도 decision으로 남긴다.
