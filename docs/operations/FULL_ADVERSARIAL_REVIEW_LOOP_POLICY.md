# Full Adversarial Review Loop Policy

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

Base의 `FULL_LOOP_COUNT_MINIMUM: 5`는 서로 다른 관점 다섯 개를 한 번씩 보는 뜻이 아니다. **한 counted loop가 아래 전체 lifecycle을 모두 수행**하고, 개선된 결과에 대해 이 lifecycle을 최소 5번 반복한다.

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

`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`, `Loop 4=long-term`, `Loop 5=review`처럼 **관점 하나를 loop 하나로 계수하지 않는다**. Scope, UX, CI, security, cost, consumer, rollback 등은 각 full loop 내부의 attack coverage다.

회차 보고에 대표 finding을 적는 것은 허용하지만, 대표 finding이 회차의 전체 범위를 뜻하지 않는다. 최소 5회 후에도 유효 오류·충돌·누락·blocking finding·회귀·acceptance failure가 있으면 6..N회를 계속한다.
