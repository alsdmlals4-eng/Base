# 자율 조사·구현 현실성·장기 최적화·학습 정책

```yaml
status: CURRENT_ACTIVE
scope: Base 및 이를 채택한 프로젝트의 L1 이상 실질 작업
owner_role: docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md의 실행 세분화
updated_at: 2026-08-29
```

이 문서는 사용자의 반복 개입을 줄이면서도 조사·설계·실제 구현·검증·학습의 품질을 낮추지 않는 공용 실행 계약이다. 가장 빠른 국소 완료보다 **장기 총비용이 낮고 유지·검증·재사용이 쉬운 완성도 높은 결과**를 우선한다.

프로젝트의 최신 사용자 지시, 프로젝트 `AGENTS.md`, 승인 Decision, 실제 코드·데이터·Scene·Resource·asset·test·runtime evidence가 이 문서보다 우선한다. 이 정책은 새 제품 범위나 위험한 외부 변경을 임의 승인하지 않는다.

## 1. Machine contract

```text
TARGETED_CURRENT_RESEARCH_REQUIRED
OFFICIAL_PRIMARY_SOURCE_FIRST
INDUSTRY_SUCCESS_FAILURE_COMPARISON
ADOPT_ADAPT_REJECT_REQUIRED
CURRENT_IMPLEMENTATION_READBACK_REQUIRED
IMPLEMENTATION_FEASIBILITY_PACKET_REQUIRED
FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
SPEC_ONLY_IS_NOT_IMPLEMENTATION_PROOF
AUTHORIZED_SCOPE_CONTINUES_TO_IMPLEMENTATION
LONG_TERM_TOTAL_COST_OVER_LOCAL_SPEED
MINIMUM_COMPLEXITY_WITH_DURABLE_QUALITY
NO_SPECULATIVE_OVERENGINEERING
MINIMIZE_USER_INTERVENTION
AUTONOMOUS_SAFE_CONTINUATION
USER_DECISION_ONLY_FOR_MEANING_LOCK_OR_HIGH_RISK
DURABLE_LEARNING_LOOP_REQUIRED
AUTOMATION_IS_PERSISTENT_SYSTEM_NOT_MODEL_SELF_TRAINING
PROBLEM_TO_ROOT_CAUSE_TO_FIX_TO_REGRESSION_GUARD
PROJECT_LESSON_BEFORE_BASE_PROMOTION
NO_NEW_LEARNING_CHURN_WITHOUT_REUSABLE_EVIDENCE
CLAIM_ONLY_ADVERSARIAL_REVIEW_INVALID
EVIDENCE_RECEIPT_REQUIRED_PER_FULL_LOOP
EXACT_HEAD_OR_STATE_REQUIRED
ACTUAL_READS_AND_CHECK_RESULTS_REQUIRED
VALIDATED_FINDING_REQUIRES_CORRECTION_OR_EXPLICIT_BLOCKER
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
```

## 2. 조사에서 실제 구현 가능성까지

중요한 시스템·데이터·UI/UX·시각·asset·workflow·자동화·아키텍처를 새로 만들거나 의미 있게 바꾸기 전에는 다음 순서를 실제 evidence로 수행한다.

```text
latest user instruction
→ current project authority / actual implementation / open PR readback
→ existing project solution and approved asset reuse
→ adopted Base owner and directly relevant internal evidence
→ targeted current official / primary-source Internet research
→ directly relevant industry success / failure / mixed cases
→ materially distinct alternatives
→ ADOPT / ADAPT / REJECT
→ actual project feasibility packet
→ implementation or implementation-ready handoff
→ verification / readback / correction
```

### 2.1 조사 기준

- `TARGETED_CURRENT_RESEARCH_REQUIRED`: 현재 결정을 바꿀 수 있는 외부 사실은 최신 공식 문서·표준·엔진 문서·플랫폼 정책·원저자 자료를 우선 확인한다.
- 검색 결과 요약, 제목, 과거 기억, 단일 성공 사례를 근거로 확정하지 않는다.
- 중요한 결정은 현행 유지, 기존 해법 재사용·수정, 대체 구조 등 최소 3개의 실질 대안을 같은 기준으로 비교한다.
- 벤치마크는 표면을 복제하지 않고 `ADOPT / ADAPT / REJECT`로 흡수한다.
- 외부 조사가 결과에 영향을 주지 않는 순수 기계 작업이면 범위와 이유를 기록한 `NOT_APPLICABLE`을 허용한다.

### 2.2 Implementation Feasibility Packet

문서상 타당성을 실제 구현 가능성으로 과장하지 않는다. 구현 방향을 확정하기 전에 다음을 현재 프로젝트의 실제 경로와 버전으로 확인한다.

```yaml
player_or_user_value:
current_solution_and_gap:
actual_consumer:
engine_and_version:
scene_node_resource_script_boundaries:
data_schema_and_ownership:
state_signal_event_flow:
ui_input_accessibility_path:
required_image_audio_text_animation_assets:
save_load_migration_compatibility:
platform_performance_and_dependency_risk:
test_and_observability_plan:
implementation_owner:
rollback_and_fallback:
evidence_ceiling:
feasibility: FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

Godot 프로젝트에서는 실제 SceneTree, Node 책임, Resource·data owner, signal/state boundary, import 설정과 runtime 소비처를 확인한다. Godot 공식 Best Practices가 제시하는 느슨한 결합·단일 책임·scene 자립성은 출발점이지 프로젝트 정본을 덮는 절대 규칙이 아니다.

`SPEC_ONLY_IS_NOT_IMPLEMENTATION_PROOF`: 기획서, 코드 예시, 정적 mockup, parser PASS, 자동 테스트 하나만으로 runtime·Human UX·기기·출시 가능성을 증명하지 않는다.

### 2.3 실제 구현으로 이어지는 기준

조사의 목표는 권장안 작성이 아니라 **현재 프로젝트에서 안전하게 구현 가능한 최적 구조를 확정하는 것**이다.

- 현재 승인 범위 안에서 GPT가 직접 수행할 수 있는 문서·데이터·검증 인프라·repository 작업은 실제로 수행한다.
- 실제 Godot 제품 구현은 프로젝트 역할 경계에 따라 Codex가 exact repository revision을 fresh-read해 수행할 수 있도록 파일·경로·작업 순서·acceptance·test·rollback이 있는 handoff를 만든다.
- 구현 권한이 이미 존재하면 조사나 명세에서 멈추지 않고 구현·검증·교정·정본 반영까지 이어간다.
- 새 핵심 제품 의미, Blueprint 최종 승인 전 제품 구현, 위험한 migration, 비용·권한 증가는 자동 승인하지 않는다.

## 3. 장기 효율과 과설계 방지

`LONG_TERM_TOTAL_COST_OVER_LOCAL_SPEED`는 단순히 작업을 크게 만드는 규칙이 아니다. 다음을 함께 비교한다.

- 플레이어·사용자 가치
- 정확성·완성도
- 유지보수성과 디버깅 가능성
- 자동 검증 가능성
- 재사용성과 모듈성
- 정본·책임 경계의 명확성
- rollback과 migration 난이도
- 장기 반복 비용과 기술 부채
- 1인 개발자가 이해·운영할 수 있는 복잡도

빠른 임시방편이 반복 오류와 수동 작업을 만든다면 원인을 해결하는 구조를 선택한다. 반대로 미래 가능성만을 위한 추상화·범용 framework·중복 owner·도구 증식은 `NO_SPECULATIVE_OVERENGINEERING`으로 거절한다. 기본값은 **현재 필요를 충족하는 최소 복잡도 + 검증 가능한 장기 확장점**이다.

## 4. 사용자 관여 최소화

`MINIMIZE_USER_INTERVENTION`은 승인 생략이 아니라 **판단 주체를 올바르게 분리하는 것**이다.

AI가 승인 범위에서 연속 처리하는 항목:

- fresh-read와 정본 충돌 탐지
- 기존 구현·자산·Base 재사용 조사
- 인터넷·실무 벤치마킹
- 대안 비교와 권장안 선택
- image candidate와 자료 준비
- 구현 가능성 판정과 handoff
- 자동 테스트·정적 검사·readback
- 실패 원인 분석·가역적 수정·회귀검사
- 문서·상태·evidence 반영
- 남은 작업 재계산
- 문제·교훈·자동화 후보 추출

사용자 결정으로 올리는 항목:

- 핵심 플레이어 경험·게임 의미·판매 포인트 변경
- 주요 서사·캐릭터·세계관 정본 변경
- 최종 Visual Direction 또는 제품 자산 lock
- 큰 범위·비용 증가
- 보안·권한·외부 공개·배포
- 되돌리기 어려운 삭제·migration
- 정본 충돌에서 객관적 증거로 우열을 정할 수 없는 취향 선택

안전하고 되돌릴 수 있는 기술적·기계적 선택은 가장 강한 근거와 장기 적합성을 가진 안으로 진행한다. 불확실성을 숨기거나 사용자 승인을 발명하지 않는다.

## 5. 지속 가능한 자동화·학습

이 문서에서 `학습`은 모델이 대화만으로 영구 학습한다는 뜻이 아니다. 반복 가능한 지식과 검증을 repository에 남기는 **지속 가능한 운영 시스템**을 뜻한다.

```text
problem / failure / repeated manual step
→ root cause
→ bounded fix
→ exact verification
→ regression guard or automated check
→ project canon / handoff / evidence update
→ reusable condition evaluation
→ Base promotion candidate when broadly reusable
```

- 프로젝트 고유 교훈과 공용 교훈을 구분한다.
- 재사용 조건·금지 조건·evidence ceiling·rollback을 함께 남긴다.
- 새 재사용 가치가 없으면 `NO_NEW_REUSABLE_LEARNING`으로 닫고 문서·Registry churn을 만들지 않는다.
- 자동화는 scope가 명확하고 rollback 가능한 경우부터 적용한다. 잘못된 판단을 빠르게 반복하는 자동화는 금지한다.
- 장기적으로는 사람이 반복 버튼을 누르는 절차보다 self-checking contract, deterministic test, readback, generated freshness check처럼 결과가 스스로 검증되는 구조를 우선한다.

## 6. 이미지 후보 선제작과 최종 lock

이미지 세부 실행 owner는 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`와 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`다.

```text
PROJECT_CANON_AND_EXISTING_VISUAL_READBACK_REQUIRED
NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK
GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION
USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION
GENERATED_CANDIDATE != USER_APPROVED != CANON_REGISTERED != IMPLEMENTED != RUNTIME_VERIFIED
```

실제 consumer 또는 승인된 Blueprint 준비에 필요한 구체적 planned surface가 있고 기존 프로젝트 내용·시안·승인 Visual로 일관성을 판단할 수 있으면 후보를 먼저 제작할 수 있다. 사용자에게는 생성 전 routine approval이 아니라 결과의 `LOCK / REVISE / REJECT / REFERENCE_ONLY` 결정을 요청한다.

후보 제작은 이미지 모델로만 수행한다. 사용자 lock 전에는 repository 정본 asset, runtime asset, production batch, 구현 완료 증거로 승격하지 않는다.

## 7. 증거 기반 적대적 검토와 교정

### `CLAIM_ONLY_ADVERSARIAL_REVIEW_INVALID`

`검토했다`, `5회 확인했다`, `문제 없음`이라는 문장만으로 적대적 검토를 완료 처리하지 않는다. retained L1 이상 변경은 작업 뒤 최소 5회의 **실제 full-scope loop**를 수행하고, 각 회차의 입력 상태·실제 읽기·실행 검사·finding·교정·재검증을 durable evidence로 남긴다.

```text
EVIDENCE_RECEIPT_REQUIRED_PER_FULL_LOOP
EXACT_HEAD_OR_STATE_REQUIRED
ACTUAL_READS_AND_CHECK_RESULTS_REQUIRED
VALIDATED_FINDING_REQUIRES_CORRECTION_OR_EXPLICIT_BLOCKER
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
```

각 full loop는 전체 승인 범위를 다시 읽고 다음 lifecycle을 수행한다.

```text
FULL_SCOPE_READ
→ ATTACK
→ VALIDATE CRITIQUE
→ APPLY CORRECTION OR RECORD EXPLICIT BLOCKER
→ VERIFY / REGRESSION / READBACK
→ BETTER ALTERNATIVE SEARCH
→ LONG_TERM FIT RECHECK
→ RE-ATTACK RESULTING STATE
```

각 loop는 `templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml`의 필드를 실제 값으로 남긴다. 관점 이름만 바꾼 한 번의 검토, 실제 파일·diff·상태를 읽지 않은 checklist, exact head가 없는 검토, 실행하지 않은 PASS, 검증하지 않은 비판, correction·blocker·회귀검사 없이 닫은 finding은 무효다.

5회 이후에도 새 `MUST_FIX`, acceptance blocker, canon/consumer drift, evidence ceiling 위반 또는 더 강한 in-scope 대안이 발견되면 수정 후 다음 full loop를 계속한다. 최소 횟수를 채우기 위한 가짜 finding이나 무의미한 변경을 만들지 않는다.

## 8. 완료 기준

완료 보고는 최소 다음을 분리한다.

```text
research evidence
→ selected structure and rejected alternatives
→ feasibility classification
→ actual implementation or exact handoff
→ automated/static verification
→ runtime/device/Human evidence
→ destination readback
→ adversarial loop receipts and corrections
→ learning/automation result
→ remaining work and revisit conditions
```

필수 조사·구현·검증·적대적 검토가 `NOT_RUN`이면 완료가 아니다. 단, 현재 승인 범위 밖의 실제 사용자 Decision만 남은 경우에는 수행 완료 범위와 blocker를 분리해 보고한다.