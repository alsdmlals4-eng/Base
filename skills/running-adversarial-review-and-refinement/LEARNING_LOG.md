# Running Adversarial Review and Refinement — Learning Log

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
