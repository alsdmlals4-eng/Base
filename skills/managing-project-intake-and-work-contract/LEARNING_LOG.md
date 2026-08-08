# Managing Project Intake and Work Contracts — Learning Log

## 2026-08-09 — Recover local and transient blockers before global stop

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 `[연속작업]`이 중간에 멈춘 실제 4사례를 제시했다. (1) 승인된 robustness 목표의 dedicated 10,000-seed package를 새 사용자 승인으로 올림, (2) exact-head Actions 결과의 tool-output truncation에서 전체 작업을 중지함, (3) 현재 ChatGPT 세션에 HiGodot가 없다는 이유로 다른 executor/독립 작업을 탐색하지 않고 중지함, (4) 승인 범위 PR에도 별도 병합 승인이 필요하다고 보고함.
- **Finding:** BCP-2026-010의 첫 구현은 `USER_DECISION_REQUIRED`와 `BLOCKED_UNVERIFIED`를 너무 넓게 전역 종료 조건으로 사용했다. 이 때문에 결과 자체를 바꾸는 진짜 사용자 결정과, 동일 승인 결과를 수행·검증하는 HOW, 일시적인 evidence transport failure, current-session capability absence, 한 task만 막힌 local blocker를 구분하지 못했다. 또한 새 standalone 회귀 테스트를 추가했을 때 일부 명시적 CI 목록이 그 파일을 소비하지 않아 처음에는 거짓 GREEN이 재현됐다.
- **Decision:** `CONTINUOUS_WORK_ACTIVE`에 `recover first → defer locally → continue independent work → stop globally last` 원칙을 추가했다. `RECOVERABLE_VERIFICATION_BLOCKER`, `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`, `LOCAL_TASK_BLOCKER`, `USER_DECISION_REQUIRED`, `HIGH_RISK_CONFIRMATION_REQUIRED`, `GLOBAL_TERMINAL_BLOCKER`를 분리하고 `ready_tasks / deferred_tasks / completed_tasks` Global Progress Queue를 사용한다. `EVIDENCE_TRANSPORT_INCOMPLETE`는 FAIL이 아니며 exact-head workflow/run/job/log를 재조회한다. 현재 세션에 권위 도구가 없으면 전체 실행 경로 부재로 간주하지 않고 callable authorized executor를 탐색하며, `[연속작업] 진행해`는 동일 승인 범위의 `CONTINUOUS_WORK_EXECUTOR_HANDOFF` 요청으로 재사용할 수 있다. 실제 executor가 없으면 거짓 실행 대신 해당 task만 `DEFERRED_EXTERNAL_EXECUTOR`로 두고 handoff/checkpoint를 남긴다. HiGodot 단일 persistent-authoring 권위는 우회하지 않는다. 승인된 동일 범위의 PR은 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 소비해 merge gate 통과 뒤 별도 승인 없이 병합한다.
- **Evidence:** CI가 소비하지 않는 standalone test 문제를 확인한 뒤 `tests/test_deep_interview_contract.py`에 recovery 계약을 연결했다. exact HEAD `6b7144ce471514d133c0a12ff7c942ada57be578`, Actions run `31279523253`, job `93158494112`에서 381개 계약 중 새 `RECOVERABLE_VERIFICATION_BLOCKER` 요구만 1 failure로 재현되고 나머지는 통과해 RED가 정확히 확인됐다. 이후 canonical reference, AGENTS, routing, GPT–Codex handoff policy, intake Skill을 같은 recovery semantics로 정렬했다.
- **Boundary:** 연속작업은 새 제품 목표·범위·예산·권한을 자동 승인하지 않는다. 결제·계정 삭제·보안/권한 확대·사용자 자격 확인과 같은 true high-risk 행위, 프로젝트 결과 자체를 바꾸는 진짜 사용자 결정은 유지한다. 무한 retry를 허용하지 않으며 유한한 evidence/executor recovery path를 소진한 뒤 실행 가능한 독립 task도 없을 때만 `GLOBAL_TERMINAL_BLOCKER`다. 다른 채팅 자동 메시지·scheduler·webhook·브라우저 종료 뒤 백그라운드 실행을 의미하지 않는다.
- **다음 검토 트리거:** recoverable blocker가 무한 반복되거나, executor handoff가 비용/권한을 암묵 확대하거나, 독립 task 판정이 dependency를 무시하거나, 승인 상속이 새 `CHANGE_PROPOSAL`/P0/P1을 덮거나, 실제 프로젝트에서 여전히 `[연속작업]`이 복구 가능한 상황에 중단될 때.

## 2026-08-08 — Explicit bounded continuous-work execution

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 현재 채팅에서 `[연속작업] 진행해`라고 명시하면 `작업 → 적대적 검토 → 권장안 결정 → 자동 승인 처리 → 다음 작업 → … → 최종 보고`를 중간 승인 대기 없이 수행하라는 요청.
- **Finding:** Base에는 이미 승인된 계약, `PLAN / BUILD / REVIEW`, 적대 검토, 기술 finding 반영, 회귀 재검증, 승인 범위의 병합 권한 상속이 있었지만 이를 하나의 명시적 opt-in 연속 실행 상태로 묶는 계약은 없었다. 또한 새 standalone 테스트 파일만 추가하면 일부 명시적 CI 목록에서 소비되지 않아 거짓 GREEN이 될 수 있음을 RED 단계에서 다시 확인했다.
- **Decision:** 새 Skill이나 Work Mode를 만들지 않고 Existing Solution First를 `ABSORB`로 판정했다. intake에 `CONTINUOUS_WORK_ACTIVE / CONTINUOUS_WORK_INACTIVE` 실행 flag와 `references/continuous-work-execution.md`를 추가하고, `[연속작업] 진행해`가 있을 때만 현재 승인된 작업 계약의 남은 범위에서 다음 미완료 작업을 자동 선택한다. 기술적 단일 최소 안전 권장안은 적대 검토 뒤 자동 승인으로 간주할 수 있지만 `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 범위 확대, 고위험 외부 행위, 사용자 중지는 자동 승인하지 않는다.
- **Evidence:** PR #228의 TDD RED에서 GitHub Actions `Validate Game Project Operating System` run `31256943151`, job `93101653170`가 새 reference 부재를 정확히 실패시켰고 나머지 기존 계약 테스트는 통과했다. 구현 뒤에는 기존 CI의 reference-freshness가 변경된 intake Skill에 대해 인정된 회귀 테스트와 Learning Log 동반 변경을 요구해 추가 소비자 누락도 탐지했다.
- **Boundary:** 연속작업은 현재 응답·에이전트 실행 세션 안의 orchestration이다. scheduler, webhook, 브라우저가 닫힌 뒤의 백그라운드 처리, 다른 ChatGPT 채팅 자동 메시지 전송을 의미하지 않는다. 트리거가 없는 일반 요청의 승인·Grill Me 흐름은 바꾸지 않는다.
- **다음 검토 트리거:** 실제 프로젝트에서 연속작업이 승인 범위를 넘어 새 Goal을 생성하거나, 사용자 전용 결정을 자동 확정하거나, 고위험 외부 행위를 우회하거나, 지나친 중간 보고/무한 반복으로 작업 연속성을 해칠 때 이 계약을 재검토한다.
