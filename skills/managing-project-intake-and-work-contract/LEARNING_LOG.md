# Managing Project Intake and Work Contracts — Learning Log

## 2026-08-15 — Separate blind retry from state-aware resume after execution interruption

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 ChatGPT의 `메시지 전송 시간이 초과되었습니다. 다시 시도해 주세요`와 `연결이 끊어졌습니다. 전체 답변을 기다리는 중입니다` 때문에 승인된 연속작업이 중단되는 문제를 자동 감지·복구하도록 요청했다.
- **Finding:** 기존 continuous-work blocker recovery는 blocker를 어떻게 복구할지 소유했지만, **실행 자체가 끊긴 직후 같은 요청을 다시 보내도 되는지**를 별도로 분류하지 않았다. 특히 파일 수정·commit·PR·merge·메일·외부 write처럼 일부 부작용이 이미 일어났을 수 있는 작업에서 마지막 프롬프트를 그대로 재전송하면 중복 실행 위험이 있다. 또한 `연결이 끊어졌습니다. 전체 답변을 기다리는 중입니다`는 서버가 이미 요청을 처리 중일 수 있어 일반 timeout과 동일한 blind retry로 취급하면 안 된다.
- **Decision:** 새 Skill/Mode를 만들지 않고 intake owner에 `TASK_RECOVERY_PROTOCOL` reference를 흡수했다. 안전한 일시 오류는 `RETRY`, 실행 여부가 불명확하거나 부작용 가능성이 있으면 `RESUME`으로 분리한다. 기본 웹 retry는 3초→10초→30초 최대 3회이며, `stalled`와 안전한 retry control이 없는 연결 단절은 자동 프롬프트 재전송을 금지한다. Resume은 authoritative readback·checkpoint·idempotency를 사용해 완료된 단계를 건너뛰고 pending 단계만 계속한다. Git worktree 재연결은 새 구현을 만들지 않고 기존 Loop A2 durable-resume의 exact identity/ownership receipt 계약을 재사용한다.
- **Evidence:** dedicated `Validate Loop A2 Durable Resume`에 `tests/test_task_recovery_protocol.py`를 연결해 독립 테스트 false-GREEN을 제거했다. RED run `31827735602`에서 기존 durable-resume 계약은 통과하고 새 task-recovery 계약만 reference 부재로 실패했다. 이후 Skill package integrity가 새 reference의 owner 연결 누락을 잡았고, canonical reference freshness가 Skill 본문 변경에 대해 companion regression과 Learning Log 동기화를 다시 요구해 이 기록과 `tests/test_neutral_adversarial_feature_lifecycle.py`를 추가했다.
- **Boundary:** Watchdog·트레이·브라우저 확장은 관찰 신호를 제공할 뿐 새로운 repository write·승인·결제·계정·보안 권위를 만들지 않는다. `USER_DECISION_REQUIRED`, `HIGH_RISK_CONFIRMATION_REQUIRED`, 권위 우회, 범위 확대는 자동 승인하지 않는다. 결과가 불명확한 POST/외부 write는 상태를 확인하기 전 재전송하지 않는다.
- **다음 검토 트리거:** 동일 오류가 UI 변경으로 감지되지 않거나, retry/reload가 중복 실행을 만들거나, checkpoint가 완료 상태를 잘못 복원하거나, `RECOVERY_REQUIRED`가 무한 반복되거나, 실제 프로젝트에서 interruption 후 이미 완료된 단계가 다시 실행되는 사례가 발생할 때.

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
