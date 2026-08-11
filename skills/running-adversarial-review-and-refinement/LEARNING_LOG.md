# Running Adversarial Review and Refinement — Learning Log

## 2026-08-11 — Post-change monitoring is a completion invariant

- **Trigger:** 변경 반영 뒤에도 적대적 검토와 PR 체크를 통해 누락·충돌·보완 사항을 항상 감시하라는 사용자 결정.
- **Finding:** 기존 Skill에는 `post-merge-review`, same-goal PR 확인, untouched-consumer 공격, regression recheck가 이미 있었지만 이를 모든 유지 변경의 단일 완료 조건으로 묶은 명시적 invariant가 없었다. 또한 focused adversarial lifecycle test가 Required Base v9 workflow의 명시적 unittest 목록에서 빠져 있어 새 회귀가 추가돼도 거짓 GREEN이 가능했다.
- **Decision:** 새 감시 Skill을 만들지 않고 `running-adversarial-review-and-refinement`에 `POST_CHANGE_MONITOR_LOOP`를 흡수한다. 후속 원인을 `OMISSION / CONFLICT / COMPLEMENT_GAP / DUPLICATE_WORK / NO_MATERIAL_FOLLOWUP`으로 분류하고, 기존 심각도·승인 Gate와 조합한다. focused lifecycle regression을 기존 Required Base v9 workflow에 직접 연결한다.
- **Evidence:** Required Base v9 workflow head `884ad449f1ccbecdbd0b3f63a4888871a9d849f6`에서 318 tests 중 기존 계약은 통과하고 새 monitor-loop test만 `POST_CHANGE_MONITOR_LOOP` 부재로 실패했다. Godot runtime test 1개는 `GODOT_BIN` 미설정으로 skipped였으며 PASS로 계산하지 않는다.
- **Boundary:** `NO_MATERIAL_FOLLOWUP`이면 억지 변경을 만들지 않는다. 이 Skill 계약 자체는 scheduler·webhook·background worker가 아니며, 보호된 정책·권한·보안·제품 방향 변경은 기존 사용자/BCP Gate를 유지한다. 실행하지 않은 CI·runtime·human validation을 PASS로 승격하지 않는다.
- **Next trigger:** post-merge review가 실제 consumer 또는 후속 PR을 놓치거나, same-goal PR race가 발생하거나, complementary finding이 의미 없는 churn으로 변하거나, Required CI에서 focused monitor regression이 다시 빠질 때 재검토한다.
