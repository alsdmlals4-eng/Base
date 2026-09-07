# Full Adversarial Review Loop Policy

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

Base는 동일 승인 작업의 최종 후보 계보에서 **정확히 2회** 전체 적대적 검토를 수행한다. 이는 2026-09-08 사용자 결정이며, 2회가 최적 품질을 보장한다는 실측 주장이 아니다. 과거 최소 5회/무제한 반복 기록은 당시 증거로 보존하고 현재 실행 지시로 사용하지 않는다.

`TWO_FULL_ADVERSARIAL_REVIEW_ROUNDS`
`FULL_LOOP_COUNT_MINIMUM: 2`
`MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 2`
`FULL_LOOP_COUNT_MAXIMUM: 2`
`NO_AUTOMATIC_THIRD_FULL_REVIEW`

기존 minimum 키는 호환용 하한이다. 상한도 2이며, 단계·Part·세션·병합 전후마다 2회를 새로 시작하지 않는다. 일반 작업 확인과 테스트는 전체 적대 검토 회차가 아니다. 같은 승인 작업의 사전 설계 검토가 이미 전체 회차로 기록됐다면 예산에 포함한다. 변경된 실제 구현을 확인하는 회차는 반드시 남긴다.

각 회차는 다음 전체 lifecycle을 다룬다.

```text
CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK
→ MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK
→ FULL-SCOPE ATTACK
→ VALIDATE CRITIQUE
→ FIX / REFINE VERIFIED FINDINGS
→ EXECUTION / REGRESSION / REFERENCE VERIFICATION
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK THE WHOLE RESULTING STATE
```

`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 관점 하나를 loop 하나로 계수하지 않는다. 각 회차는 전체 승인 범위의 의도·정본·실제 구현·consumer·보안·비용·회귀·증거를 확인한다. 특히 **불필요한 작업, 과설계, 충돌, 누락**을 함께 검토한다. 전체 결과 재확인은 해당 회차 내부의 교정 확인이며 새 독립 검토를 숨겨 추가하지 않는다.

- 1회차: 최종 후보 전체를 공격하고 유효 finding만 최소 교정·검증한다.
- 2회차: 교정된 전체 후보와 untouched consumer를 다시 확인한다.
- **2회 이후에는** 발견된 결함별 수정·영향 범위 회귀검증·정본/consumer readback만 수행한다. 3..N 전체 재공격이나 이름만 바꾼 전체 감사는 자동 실행하지 않는다. 해결하지 못한 blocker는 `BLOCKED_UNVERIFIED` 등 실제 상태로 남기고 완료·병합하지 않는다. 범위 확대 또는 추가 전체 검토가 정말 필요하면 사용자 결정으로 올린다.
- CI, 보안/권한, 독립 승인, exact-head 검사, 병합 후 main readback은 별도 Gate로 유지하되 전체 검토를 다시 시작하지 않는다. 새 커밋/SHA나 테스트 재시도만으로 회차를 초기화하지 않는다.
- 같은 source·범위·consumer가 유지된 대안 비교와 비용·장기 적합성 근거는 freshness를 확인해 재사용한다. 회차마다 새 대안·새 문서·가짜 finding을 만들지 않는다.
- 개선은 기존 owner/Skill/reference에 최소 반영한다. 의미 없는 분할·새 프레임워크·중복 정본은 추가하지 않는다. 폐기 후보는 참조·고유 자료·승계·복구 가능성을 확인하며, 출처 불명 파일은 보존한다.

입력/출력 revision, 전체 coverage, finding 판정, 교정, 실제 검사 또는 재사용 근거, 미해결 항목은 기존 `templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml` 또는 PR에 기록한다. 단순 횟수 기입은 수행 증거가 아니다.

`CLEAN_REVIEW_EXIT`는 2회 수행만으로 얻지 못한다. 유효 MUST_FIX·acceptance blocker·회귀·정본/consumer 충돌이 0이고 필요한 검증과 evidence ceiling이 충족돼야 한다. `NOT_RUN`, `CANCELLED`, 미해결 차단은 PASS가 아니다.
