# 자율 품질·최적화·학습 정책

이 문서는 Base와 이를 채택한 프로젝트에서 사용자의 반복 관여를 줄이면서 장기 품질과 실제 구현 가능성을 높이는 공용 실행 계약이다.

```text
AUTONOMOUS_QUALITY_OPTIMIZATION_AND_LEARNING
CURRENT_RESEARCH_AND_IMPLEMENTATION_FEASIBILITY_REQUIRED
MINIMUM_MATERIALLY_DISTINCT_ALTERNATIVES: 3
ACTUAL_PROJECT_BOUNDARY_MAPPING_REQUIRED
LONG_TERM_EFFICIENCY_AND_COMPLETENESS_FIRST
QUALITY_OVER_RESPONSE_SPEED
TOTAL_LIFECYCLE_COST
NO_UNSUPPORTED_OVERENGINEERING
MINIMUM_NECESSARY_COMPLEXITY
LOW_INTERVENTION_AUTOMATION_AND_LEARNING_LOOP
CLAIM_ONLY_ADVERSARIAL_REVIEW_INVALID
EVIDENCE_RECEIPT_REQUIRED_PER_FULL_LOOP
EXACT_HEAD_OR_STATE_REQUIRED
ACTUAL_READS_AND_CHECK_RESULTS_REQUIRED
VALIDATED_FINDING_REQUIRES_CORRECTION_OR_EXPLICIT_BLOCKER
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
```

## 1. 적용 범위와 권위

이 정책은 다음 L1 이상 작업에 적용한다.

- 게임·서사·서비스 기획과 구조 결정
- Godot Scene·Node·Resource·script·data·save/load 구조
- UI/UX·입력·접근성·플랫폼 구조
- 이미지·오디오·텍스트·animation production pipeline
- Base/프로젝트 문서·정본·검증기·CI·자동화
- 구현 검수, PR, 병합, post-merge 교정

권위 순서는 최신 사용자 지시, 프로젝트 `AGENTS.md`와 current canon, 실제 구현·증거, 프로젝트가 채택한 Base 계약, 최신 Base, 외부 자료 순이다. 외부 자료나 이 공용 정책은 프로젝트 고유 제품 의미를 자동 변경하지 않는다.

## 2. 실제 조사와 구현 가능성

### `CURRENT_RESEARCH_AND_IMPLEMENTATION_FEASIBILITY_REQUIRED`

중요 구조를 확정하기 전에 다음을 실제로 수행한다.

```text
fresh current authority and actual implementation read
→ existing project solution search
→ adopted Base solution search
→ current official / primary-source Internet research
→ directly relevant professional practice and failure cases
→ at least 3 materially distinct viable alternatives
→ ADOPT / ADAPT / TEST / REJECT
→ ACTUAL_PROJECT_BOUNDARY_MAPPING_REQUIRED
→ FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

`MINIMUM_MATERIALLY_DISTINCT_ALTERNATIVES: 3`은 표현만 다른 세 문장을 뜻하지 않는다. 현행 유지·최소 수정·기존 해법 재사용·구조 개선·검증된 외부 해법·신규 구축 중 현재 결정에 실제로 다른 trade-off를 주는 후보를 비교한다.

비교 기준에는 최소 다음을 포함한다.

- 플레이어·사용자 가치
- 현재 Godot/언어/플랫폼/API compatibility
- Scene·Node·Resource·script 책임과 consumer
- data schema, save/load, migration, rollback
- UI state, input, focus, accessibility
- asset/audio/text/animation dependency와 rights
- performance, memory, security, failure recovery
- test seam, debug signal, observability
- 구현 비용과 `TOTAL_LIFECYCLE_COST`
- 1인 개발 유지 가능성
- paid dependency와 runner/service 비용

### `ACTUAL_PROJECT_BOUNDARY_MAPPING_REQUIRED`

결론은 실제 repository 경계에 연결한다.

```yaml
actual_consumers: []
scene_node_resource_boundaries: []
script_and_data_owners: []
input_and_ui_states: []
asset_dependencies: []
save_load_or_migration: []
performance_platform_risks: []
test_and_runtime_evidence_plan: []
rollback_boundary: []
codex_implementation_package: []
feasibility: FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

`RESEARCH_SUMMARY_IS_NOT_IMPLEMENTATION_PROOF`: 검색 결과, 링크 목록, 문서 예시, 정적 mockup, AI 추론 또는 자동 test 하나만으로 실제 runtime·UX·출시 가능성을 증명하지 않는다.

외부 정보가 현재 판단을 바꿀 수 없는 순수 오탈자·형식 정리·기계적 rename에는 `RESEARCH_NOT_MATERIAL`과 이유를 기록할 수 있다. 이 예외를 제품 의미·UX·runtime·dependency·platform·rights·security 결정에 사용하지 않는다.

## 3. 장기 품질 선택 규칙

### `LONG_TERM_EFFICIENCY_AND_COMPLETENESS_FIRST`

작업 속도나 응답 길이보다 다음을 우선한다.

1. 사용자·플레이어 가치와 완성도
2. 정본·owner·상태 전이의 명확성
3. 실제 구현·검증·rollback 가능성
4. 유지보수성·확장성·재사용성
5. 반복 수작업과 사용자 개입 감소
6. 기술 부채·오류·드리프트의 재발 방지
7. 출시 수준으로 확장 가능한 품질
8. 현재 필요를 충족하는 `MINIMUM_NECESSARY_COMPLEXITY`

```text
QUALITY_OVER_RESPONSE_SPEED
TOTAL_LIFECYCLE_COST
LONG_TERM_FIT_RECHECK
```

빠른 임시방편이 반복 비용이나 정본 충돌을 만든다면 원인을 해결하는 구조를 채택한다. 단, 오래 걸린다는 사실 자체는 품질 증거가 아니다.

### `NO_UNSUPPORTED_OVERENGINEERING`

다음은 장기 최적화가 아니다.

- 현재 consumer와 acceptance가 없는 범용 framework
- 미래 가능성만을 위한 schema·service·abstraction
- 유지 owner와 test가 없는 자동화
- 무료·기존 해법으로 충분한데 추가하는 paid dependency
- 실제 반복비용보다 구현·유지비가 큰 자동화
- 초보 개발자가 이해·복구할 수 없는 불투명한 구조

자동화·추상화는 측정 가능한 반복비용, 품질 또는 위험 감소가 개발·운영비보다 크고 안전한 rollback이 있을 때만 채택한다.

## 4. 사용자 관여 최소화

### `LOW_INTERVENTION_AUTOMATION_AND_LEARNING_LOOP`

```text
READ CURRENT AUTHORITY
→ RESEARCH / COMPARE
→ SELECT PROVISIONAL BEST OPTION
→ PREPARE CANDIDATE / SPEC / IMPLEMENTATION PACKAGE
→ EXECUTE SAFE REVERSIBLE WORK
→ TEST / READBACK
→ ADVERSARIAL REVIEW
→ CORRECT VALIDATED FINDINGS
→ REGRESSION / POST-CHANGE READBACK
→ INCIDENT / SOLUTION / LESSON
→ PROJECT AUTOMATION OR BASE PROMOTION
→ REMAINING WORK RECALCULATION
```

```text
SAFE_REVERSIBLE_WORK_CONTINUES_WITHOUT_ROUTINE_REAPPROVAL
USER_DECISION_ONLY_FOR_PRODUCT_MEANING_FINAL_VISUAL_LOCK_OR_HIGH_RISK
FAIL_CLOSED_TO_HUMAN_ON_UNSAFE_OR_CANON_CONFLICT
```

사용자의 반복 승인을 기다리지 않고 진행할 수 있는 범위:

- current authority·open PR·actual consumer fresh-read
- 공식/1차 자료 조사와 대안 비교
- 후보 brief·spec·test·검증 계획 작성
- 필요성이 입증된 이미지 후보 1건 제작
- 승인 범위의 문서·검증기·가역적 교정
- test, CI, readback, diff, consumer/reference 검사
- validated finding의 동일 의미 내 최소 수정
- 문제·교훈·자동화 후보 기록
- 남은 작업 재계산과 다음 안전 작업

사용자 결정이 필요한 범위:

- 핵심 게임 경험·서사·캐릭터·세계관 의미 변경
- 최종 visual `LOCK`
- 큰 범위·일정·비용 증가
- paid dependency·외부 공개·배포·계정/권한·보안 변경
- 파괴적 migration·삭제·복구 불가능한 변경
- current canon과 직접 충돌하는 선택
- 객관적 증거로 우열을 닫을 수 없는 핵심 취향 결정

자동화가 불안전한 입력, 정본 충돌, 확인 불가능한 권한 또는 고위험 상태를 만나면 `BLOCKED_UNVERIFIED`로 닫고 사람에게 되돌린다. 자동화 목표는 사용자 통제를 없애는 것이 아니라 반복적인 저가치 개입을 줄이는 것이다.

## 5. 이미지 후보 선제작

이미지 authority는 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`와 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 소유한다.

```text
NEED_DRIVEN_GENERATE_THEN_LOCK
CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED
CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED
GENERATE_ONE_CANDIDATE_BEFORE_LOCK
USER_LOCK_REVISE_REJECT_AFTER_GENERATION
```

구체적 필요와 프로젝트 시각 정본을 확인하면 별도의 사전 생성 승인 질문 없이 후보 1건을 만들 수 있다. 그러나 다음 상태는 분리한다.

```text
GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED
```

이미지 후보는 Blueprint 판단 자료가 될 수 있지만 신규 구현 authority가 아니다.

## 6. Blueprint와 구현 권한

```text
BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE
PLAN
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

`GENERATED_CANDIDATE_IS_NOT_IMPLEMENTATION_AUTHORITY`.

이미지·자료·구현 task breakdown은 사용자 최종 Blueprint 검토 전에 준비할 수 있다. 신규 implementation package 실행은 exact artifact revision에 대한 `USER_FINAL_REVIEW_APPROVAL` 뒤에만 시작한다. Gate 채택 전 exact package·scope·revision에 이미 승인된 구현은 프로젝트 current authority가 보존하는 범위에서만 이어간다.

## 7. 증거 기반 적대적 검토

### `CLAIM_ONLY_ADVERSARIAL_REVIEW_INVALID`

`검토했다`, `5회 확인했다`, `문제 없음`이라는 문장만으로 적대적 검토를 완료 처리하지 않는다.

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

각 loop는 `templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml`의 필드를 실제 값으로 남긴다. 서로 다른 관점 이름만 붙인 한 번의 검토를 여러 loop로 세지 않는다.

다음은 무효다.

- actual file/diff/state를 읽지 않은 checklist 체크
- exact head 또는 input state가 없는 검토
- 실행하지 않은 test/runtime/readback의 PASS 주장
- 비판을 검증하지 않고 바로 수정하거나 폐기
- validated finding을 수정·회귀검사·blocker 없이 종료
- 같은 finding을 표현만 바꿔 반복 계수
- 최소 횟수를 채우기 위한 가짜 finding이나 무의미한 변경

5회 이후에도 새 `MUST_FIX`, acceptance blocker, canon/consumer drift, evidence ceiling 위반 또는 더 강한 in-scope 대안이 발견되면 수정 후 다음 full loop를 계속한다.

## 8. 학습과 재발 방지

### `INCIDENT_SOLUTION_LESSON_TO_AUTOMATION_OR_BASE_PROMOTION`

```text
INCIDENT
→ ROOT CAUSE
→ SOLUTION
→ VERIFICATION
→ REGRESSION PREVENTION
→ PROJECT OWNER UPDATE
→ REUSABILITY CLASSIFICATION
   ├─ PROJECT_SPECIFIC
   └─ CROSS_PROJECT_BASE_PROMOTION_CANDIDATE
→ SUPERSESSION / STALE REFERENCE CLEANUP
```

교훈은 대화 요약만으로 완료되지 않는다. 최소 하나의 durable output이 있어야 한다.

- current owner 교정
- regression test/checker
- template/checklist/schema
- routing·freshness rule
- automation script/workflow
- explicit `NO_BASE_PROMOTION` 근거

공용 승격은 실제 두 개 이상의 프로젝트에 같은 재발 위험이 있거나 Base active contract 자체가 원인일 때 우선한다. 프로젝트 고유 의미를 공용 규칙으로 과잉 일반화하지 않는다.

## 9. 완료 보고

완료 보고는 다음을 분리한다.

```text
작업 전 문제
→ 조사·대안 비교
→ 실제 변경
→ 실제 사용 예
→ 기대효과
→ exact verification / readback evidence
→ adversarial loop receipts and corrections
→ automation / lesson promotion
→ NOT_RUN / BLOCKED / remaining risk
```

문서 PASS, static PASS, automated test PASS, runtime PASS, UX/Human PASS, user visual lock, release PASS는 서로 대체하지 않는다.
