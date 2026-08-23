# Running Adversarial Review and Refinement — Learning Log

## 2026-08-24 — Completion is a candidate until remaining work is recalculated

- **Trigger:** Base와 프로젝트에서 계획된 남은 작업을 모두 처리한 뒤에도 실제 구현·정본·Test·consumer·PR·readback을 다시 확인해 교정할 사항이 없는지 적대적으로 검토하고 나서 완료를 판정하라는 사용자 결정.
- **Finding 1:** 계획 목록의 소진은 실제 상태의 누락이 0이라는 증거가 아니다. 계획 밖에서 드러난 구현·교정 누락을 완료 뒤 발견하면 조기 완료 보고가 된다.
- **Decision 1:** `REMAINING_WORK_RECALCULATION_REQUIRED → IMPLEMENTATION_CORRECTION_RESCAN`을 완료 후보 Gate로 둔다. 유효한 새 finding은 `NEW_FINDING_REOPENS_REMAINING_WORK`로 현재 승인 범위의 작업을 다시 열고 기존 owner에서 최소 교정·회귀·readback 후 재계산한다.
- **Finding 2:** 완료 후보용 적대 검토와 기존 `POST_CHANGE_MONITOR_LOOP`를 별도 5회 루프로 해석하면 같은 최종 상태를 5+5회 중복 검토하는 운영비가 생긴다.
- **Decision 2:** `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 새 framework나 두 번째 5회 cycle이 아니라 **최종 completion candidate를 입력으로 하는 기존 `POST_CHANGE_MONITOR_LOOP` 자체**다. 같은 final-state lineage가 기존 minimum-five full loop와 `CLEAN_REVIEW_EXIT`를 충족한다.
- **Finding 3 / RED evidence:** Skill owner 본문과 전용 회귀만 추가한 후보는 canonical reference freshness에서 실패했다. `local-skill-contract-learning-test-sync`와 `local-skill-contract-learning-sync`가 recognized lifecycle test와 Learning Log companion 누락을 실제로 차단했다.
- **Correction:** 기존 `tests/test_reference_freshness.py`를 recognized companion으로 갱신하고 이 Learning Log를 동기화했다. 전용 `tests/test_completion_correction_adversarial_gate.py`는 Base/프로젝트 owner 간 완료 계약을 직접 검사한다.
- **Boundary:** `NO_MATERIAL_FOLLOWUP`이면 최소 회차를 채우기 위해 가짜 finding이나 불필요한 변경을 만들지 않는다. `FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK`는 현재 승인 범위에만 적용하며, 범위 밖 future improvement는 별도 후보로 보존한다. 승인 범위 안의 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, 미해결 `DEFER`는 `전체 완료`로 숨기지 않는다.
- **Evidence ceiling:** 이 변경의 정적 계약·회귀·CI 성공은 운영 규칙의 구현 증거다. 개별 게임의 runtime·사람 플레이·제품 품질이 자동으로 검증됐다는 뜻은 아니다.
- **Next trigger:** 완료 Gate가 작은 L0 작업까지 과도하게 확장되거나, 동일 최종 상태의 중복 review가 재발하거나, 새 finding이 남은 작업으로 편입되지 않은 채 완료 보고되는 사례가 발견되면 경계를 재검토한다.

## 2026-08-19 — minimum five full loops plus verified clean exit is the active contract

- **Trigger:** 사용자가 최신 규칙으로 적대적 검토 루프를 **최소 5회 수행하고, 5회 이후에도 유효 오류가 남으면 오류 0이 될 때까지 계속**하도록 명시했다.
- **Finding:** 직전 `ADVERSARIAL_REVIEW_UNTIL_CLEAN`은 숫자 quota가 종료조건을 왜곡하는 문제를 해결했지만 최소 검토 깊이가 사라져 한두 번의 우연한 clean 결과로 충분히 깊게 공격하지 못할 수 있었다. 반대로 과거 fixed-five 계약은 5회를 최대 종료점처럼 오해할 여지가 있었다.
- **Decision:** 기존 Skill owner를 유지하고 `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`, `CLEAN_REVIEW_EXIT`를 함께 사용한다. 1~5회는 전체 승인 범위를 다시 공격하는 의무 loop이며 5회 전에는 종료하지 않는다. 5회 이후에는 새 유효 `MUST_FIX`/P0/P1/정본 충돌/acceptance failure/회귀가 하나라도 있으면 6..N회로 계속하고, post-minimum 전체 재공격에서 유효 blocking finding 0일 때만 종료한다.
- **Evidence:** PR #532에서 먼저 Long-Horizon regression을 바꿔 current production이 `FULL_LOOP_COUNT_MINIMUM: 5` 부재로 RED가 되는 것을 확인했다. production owner와 companion regression을 동기화한 뒤 focused/required CI로 GREEN을 요구한다.
- **Boundary:** 최소 5회는 가짜 finding이나 불필요한 변경을 만들라는 뜻이 아니다. full-scope attack·검증·대안·장기 적합성 재검사를 실제 수행하면 finding/changes가 0인 clean loop도 의무 회차로 인정한다. 5회는 최대치가 아니며 5회 이후 오류가 남으면 계속한다.
- **Next trigger:** 5회 미만 clean exit, 5회에서 강제 종료, loop를 lens/checklist 개수로 대체, 가짜 finding 생성, evidence ceiling 무시가 나타나면 즉시 재검토한다.

## 2026-08-19 — fixed loop counts are weaker than a verified clean-exit condition (SUPERSEDED LATER SAME DAY)

- **Trigger:** 사용자가 적대적 검토를 5회 같은 고정 횟수로 제한하지 말고, 검토 결과에서 유효한 오류·충돌·누락·blocking finding이 더 이상 나오지 않을 때까지 반복하라고 상위 규칙을 변경했다.
- **Finding:** `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`와 `FULL_LOOP_COUNT_MINIMUM: 5`는 이전의 “5개 lens가 아니라 전체 개선 사이클을 반복한다”는 문제는 해결했지만, 여전히 숫자 quota가 종료 조건처럼 보일 수 있었다. 횟수를 채우는 데 초점을 두면 5회보다 빨리 깨끗해진 상태에서 불필요한 churn을 만들거나, 5회 이후 새 오류가 계속 나오는 상황을 숫자와 혼동할 수 있다.
- **Decision:** 기존 Skill owner를 유지하고 `ADVERSARIAL_REVIEW_UNTIL_CLEAN`과 `CLEAN_REVIEW_EXIT`로 전환한다. 각 회차는 전체 승인 범위를 다시 공격하고, 새 유효 `MUST_FIX`/P0/P1/acceptance blocker/정본·참조 충돌/회귀/evidence ceiling 위반이 나오면 수정·검증 후 다음 전체 회차로 간다. 종료는 새 유효 오류·충돌·누락·blocking finding 0, 회귀 0, acceptance 충족, 정본·참조 신선도와 증거 ceiling 충족으로 판정한다.
- **Evidence:** PR #531의 첫 one-shot migration run `32208848514`에서 정책 변환은 성공했지만 기존 회귀 테스트가 `FULL_LOOP_COUNT_MINIMUM: 5`를 요구해 RED가 발생했다. 후속 run `32208916516`에서 fixed-loop regression을 clean-exit regression으로 교체한 뒤 focused Long-Horizon/GPT-Codex contracts가 Green이었다. 이후 전체 CI의 canonical-reference freshness가 이 Learning Log 동반 갱신 필요성을 다시 검출했다.
- **Boundary:** “오류가 안 나올 때까지”를 무한히 새로운 취향 finding을 발명하라는 의미로 사용하지 않는다. 동일 finding을 표현만 바꿔 계수하지 않고, `NO_MATERIAL_FOLLOWUP`이면 churn을 만들지 않는다. 실행할 수 없는 runtime/human test는 `NOT_RUN`/`BLOCKED_UNVERIFIED`로 남기며 clean 상태를 꾸미지 않는다.
- **Next trigger:** clean-exit가 단순 “한 번 문제 없음”으로 축소되거나, evidence ceiling/consumer/reference drift가 무시되거나, 고정 숫자 quota가 active contract로 재도입되면 즉시 재검토한다.

## 2026-08-18 — segmented five-round review was the wrong abstraction

- **Trigger:** 사용자가 “5회 적대적 검토”는 5개 공격면 분할이 아니라 `전체 적대적 검토 → 충돌·누락·문제 발견 → 개선·보완 → 검증 → 개선된 전체 상태 재검토`를 5회 반복하는 것이라고 재확정했다. 중요 결정은 최소 3개의 실질 대안을 비교하고 더 나은 방안과 장기계획 적합성도 계속 확인해야 한다.
- **Finding:** Base가 `FIVE_DISTINCT_ADVERSARIAL_ROUNDS`를 승격해 하나의 전체 검토를 다섯 lens로 분할했다. 이는 의식적 반복을 줄이려는 이전 해석이었지만 사용자 의도인 반복 개선 control loop를 바꿔 버렸다.
- **Decision:** 새 광역 Skill 없이 기존 owner를 유지하고 당시 `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`, `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_VIABLE_ALTERNATIVES: 3`, `BETTER_ALTERNATIVE_SEARCH`, `LONG_TERM_PLAN_FIT_REQUIRED`를 상위 정책·장기정책·이 Skill에 연결했다. 이 수치형 종료 계약은 2026-08-19의 더 최신 `ADVERSARIAL_REVIEW_UNTIL_CLEAN` 결정으로 대체되었다.
- **Evidence:** PR #519의 test-only head `b04c57bb9fd008c0043dbd488e8f8311c589e946`에서 Long-Horizon contract가 의도대로 RED였다. 초기 production head `26a07487ac60b943fe8510e1c25828f89346b5e8`에서는 새 full-loop 계약 대부분이 GREEN으로 전환됐지만, reference-freshness가 Skill Learning Log 동반 갱신 누락을 잡아 이 기록을 추가하게 됐다.
- **Boundary:** 당시 핵심 교훈인 “lens 분할이 아니라 수정·검증을 포함한 전체 재공격”은 유지한다. 단, 현재 종료 조건은 5회 quota가 아니라 `CLEAN_REVIEW_EXIT`다. 최소 3개 대안은 이름만 다른 허수 후보로 채우지 않는다.
- **Next trigger:** 역사 기록을 현재 active contract로 오인하거나 `FIVE_DISTINCT_ADVERSARIAL_ROUNDS`가 active consumer에 재등장하면 재검토한다.

## 2026-08-15 — Socratic questioning works best as a selective review lens

- **Trigger:** 적대적 검토 루프에 Socratic questioning의 명료화·가정·근거·관점·파급·질문 자체 성찰을 추가하라는 사용자 결정.
- **Finding:** 새 광역 Skill이나 의무 질문 체크리스트를 만들면 기존 `running-adversarial-review-and-refinement`, cross-discipline Lens, intake/Grill Me 질문 Gate와 책임이 겹치고 질문 폭주·가짜 Finding을 만들 위험이 있다.
- **Decision:** 새 Skill ID 없이 `Socratic Review Lens` reference로 흡수한다. 현재 Requirement·주장·Finding·위험과 관련된 Lens만 선택하고, 저장소·정본·실제 구현·도구로 답할 수 있는 사실은 먼저 직접 조사한다. `Meta-question`에서 "답이 달라지면 실제 결정도 달라지는가"를 재검증해 critique-for-critique를 제거한다.
- **Evidence:** Foundation for Critical Thinking의 Richard Paul·Linda Elder 계열 자료에서 clarification, assumptions, reasons/evidence, viewpoints, implications/consequences, questions about the question의 질문군과 disciplined questioning 원칙을 확인했다. 저장소에서는 기존 적대적 Skill이 사용자안/AI안 대칭 검토, 반대를 위한 반대 금지, 선택형 cross-discipline Lens, 기존 Finding decisions를 이미 소유하므로 흡수 구조가 중복을 최소화한다. 집중 계약 RED는 새 reference 부재로 의도대로 실패했다.
- **Boundary:** Socratic Lens는 사용자 인터뷰·승인 Gate가 아니며 모든 여섯 Lens를 강제하지 않는다. `BLOCKED_UNVERIFIED`와 `USER_DECISION_REQUIRED` 의미를 재정의하지 않고, 실제 모델 행동 평가는 실행 전 `MODEL_RUN_STATUS: NOT_RUN`으로 유지한다.
- **Next trigger:** 질문량 증가, repository-first 조사 회피, cross-discipline Lens와 중복 Finding, Meta-question이 유효 비판을 과도하게 기각하는 회귀가 관찰되면 재검토한다.

## 2026-08-11 — Post-change monitoring is a completion invariant

- **Trigger:** 변경 반영 뒤에도 적대적 검토와 PR 체크를 통해 누락·충돌·보완 사항을 항상 감시하라는 사용자 결정.
- **Finding:** 기존 Skill에는 `post-merge-review`, same-goal PR 확인, untouched-consumer 공격, regression recheck가 이미 있었지만 이를 모든 유지 변경의 단일 완료 조건으로 묶은 명시적 invariant가 없었다. 또한 focused adversarial lifecycle test가 Required Base v9 workflow의 명시적 unittest 목록에서 빠져 있어 새 회귀가 추가돼도 거짓 GREEN이 가능했다.
- **Decision:** 새 감시 Skill을 만들지 않고 `running-adversarial-review-and-refinement`에 `POST_CHANGE_MONITOR_LOOP`를 흡수한다. 후속 원인을 `OMISSION / CONFLICT / COMPLEMENT_GAP / DUPLICATE_WORK / NO_MATERIAL_FOLLOWUP`으로 분류하고, 기존 심각도·승인 Gate와 조합한다. focused lifecycle regression을 기존 Required Base v9 workflow에 직접 연결한다.
- **Evidence:** Required Base v9 workflow head `884ad449f1ccbecdbd0b3f63a4888871a9d849f6`에서 318 tests 중 기존 계약은 통과하고 새 monitor-loop test만 `POST_CHANGE_MONITOR_LOOP` 부재로 실패했다. Godot runtime test 1개는 `GODOT_BIN` 미설정으로 skipped였으며 PASS로 계산하지 않는다.
- **Boundary:** `NO_MATERIAL_FOLLOWUP`이면 억지 변경을 만들지 않는다. 이 Skill 계약 자체는 scheduler·webhook·background worker가 아니며, 보호된 정책·권한·보안·제품 방향 변경은 기존 사용자/BCP Gate를 유지한다. 실행하지 않은 CI·runtime·human validation을 PASS로 승격하지 않는다.
- **Next trigger:** post-merge review가 실제 consumer 또는 후속 PR을 놓치거나, same-goal PR race가 발생하거나, complementary finding이 의미 없는 churn으로 변하거나, Required CI에서 focused monitor regression이 다시 빠질 때 재검토한다.

## 2026-08-19 · full loop is not a review lens

- 관찰: 정본은 이미 full-scope review를 요구했지만 실제 완료보고가 `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 lens별 회차로 축약될 수 있었다.
- 교훈: 최소 5회는 서로 다른 관점 5개가 아니라 **동일한 전체 lifecycle을 개선된 상태에 대해 최소 5번 반복**한다는 뜻이어야 한다.
- 반영: `FULL_LOOP_IS_NOT_A_REVIEW_LENS`와 full-scope coverage evidence를 추가하고 lens-only 회차를 계수하지 않는다.
- reuse_scope: BASE_PROMOTION_CANDIDATE
