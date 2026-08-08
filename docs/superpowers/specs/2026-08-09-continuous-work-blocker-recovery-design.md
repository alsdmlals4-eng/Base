# Continuous Work Blocker Recovery Design

## 승인 근거

2026-08-09 사용자 요청: `[연속작업]`이 중간에 멈추는 4개 실제 사례를 제시하고 `해결해줘`라고 명시적으로 요청했다. 이 요청은 기존 BCP-2026-010의 연속작업 계약을 보수하는 직접 승인 작업 계약이다.

## 문제

현행 `continuous-work-execution.md`는 `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 필수 도구 부재를 만나면 연속 루프를 즉시 종료한다. 이 때문에 실제로는 자동 복구 가능한 상태도 전체 작업 중지로 승격된다.

관찰된 실패 패턴은 네 가지다.

1. **실행 방법을 새 범위로 오판**: 이미 승인된 robustness 목표를 증명하기 위한 dedicated 10,000-seed execution package를 별도 사용자 승인으로 올림.
2. **증거 전송 실패를 검증 실패로 오판**: exact-head Actions 결과가 tool-output truncation으로 안 보인다는 이유만으로 Task 7을 미확정 상태로 종료.
3. **현재 세션 도구 부재를 전체 실행 경로 부재로 오판**: HiGodot가 현재 ChatGPT 세션에 노출되지 않았다는 이유로 다른 실행 환경·위임·독립 작업을 탐색하기 전에 전체 루프 종료.
4. **승인 상속을 무시**: 승인된 범위의 PR도 `별도 병합 승인`이 필요하다고 보고하여 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`와 충돌.

## 설계 대안

### A. 현재처럼 첫 blocker에서 종료

- 장점: 가장 보수적이다.
- 단점: 일시적 API 문제, 증거 조회 지연, 국소 도구 부재가 전체 작업을 자주 끊는다.
- 판정: REJECT.

### B. 연속작업에서는 모든 blocker와 사용자 결정을 자동 승인

- 장점: 거의 멈추지 않는다.
- 단점: 프로젝트 방향 변경, 비용·보안·권한·비가역 외부 행위까지 자동화하여 권한 경계를 파괴한다.
- 판정: REJECT.

### C. Blocker Recovery Ladder + Global Progress Queue

- 장점: 복구 가능한 문제는 자동 복구하고, 한 작업만 막혀도 독립 작업을 계속하며, 실제 사용자 결정과 고위험 행위만 보존한다.
- 단점: 상태 분류가 조금 더 복잡하다.
- 판정: ADOPT.

## 핵심 원칙

`CONTINUOUS_WORK_ACTIVE`에서는 **blocker를 발견했다고 즉시 종료하지 않는다.** 먼저 blocker를 분류하고 복구 사다리를 모두 시도한다.

```text
blocker/finding
→ scope check
→ recoverability classification
→ retry/requery
→ alternate evidence/source
→ authorized alternate executor/tool
→ defer only the blocked task
→ continue independent ready tasks
→ re-attempt deferred tasks after dependencies change
→ only then terminal stop if no actionable work remains
```

## Blocker taxonomy

### `RECOVERABLE_VERIFICATION_BLOCKER`

예: tool-output truncation, polling 지연, 일시적 API 오류, workflow 결과가 아직 queued/in_progress.

처리:

1. 동일 exact HEAD를 보존한다.
2. 더 좁은 endpoint/status/job/log query로 재조회한다.
3. 필요 시 동일 SHA workflow/job을 재실행한다.
4. 대체 authoritative evidence surface를 조회한다.
5. 결과가 확정되면 원래 작업을 계속한다.
6. 일정 횟수 반복이 아니라 **새 증거가 생길 수 있는 유한한 대체 경로 목록**을 소진한 뒤에만 미검증으로 남긴다.

### `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`

예: 현재 ChatGPT 세션에 HiGodot MCP가 노출되지 않음.

처리:

1. 현재 세션에서 승인·권위에 맞는 다른 연결 도구가 있는지 확인한다.
2. 동일 권위 도구를 사용할 수 있는 연결된/호출 가능한 executor가 있는지 확인한다.
3. `[연속작업]` 자체를 해당 승인 범위의 **executor handoff 요청으로 간주할 수 있다**. 별도 `Codex로 넘길까요?` 질문을 만들지 않는다.
4. 실제 executor 호출이 가능하면 handoff package를 만들고 즉시 위임한다.
5. 실제 executor 호출이 불가능하면 handoff/checkpoint를 자동 작성해 blocked task를 `DEFERRED_EXTERNAL_EXECUTOR`로 두고 독립 작업을 계속한다.
6. 권위 계약을 우회해 금지된 직접 파일 편집을 하지 않는다.

`현재 harness에 도구가 없음`과 `승인된 전체 시스템 어디에도 실행 경로가 없음`을 구분한다.

### `LOCAL_TASK_BLOCKER`

한 task/패키지만 막혔고 다른 ready task가 있는 상태.

처리:

- 해당 task만 deferred queue로 이동한다.
- 의존성 없는 다음 task를 계속한다.
- 이후 새 증거/도구/선행 결과가 생기면 deferred task를 재시도한다.

### `USER_DECISION_REQUIRED`

다음에만 사용한다.

- 승인된 목표의 **결과 자체**가 달라지는 복수의 유효한 선택지
- 프로젝트 코어, 주요 UX, 콘텐츠 의미, 비용/범위 우선순위의 새 변경
- 기존 approval reference로 복원할 수 없는 새 사용자 의사결정

다음은 `USER_DECISION_REQUIRED`가 아니다.

- 같은 승인 목표를 검증하기 위한 테스트 규모 확대
- dedicated execution/test package 작성
- 실패한 검증의 재조회·재실행
- 동일 동작을 보존하는 기술적 최소 수정
- 승인 범위의 PR 생성·병합
- 현재 세션 도구 부재 때문에 승인된 다른 executor로 넘기는 것

### `HIGH_RISK_CONFIRMATION_REQUIRED`

결제, 계정 삭제, 권한 확대, 보안 설정 변경, 사용자 자격 확인, 승인 예산을 넘는 외부 비용 등 실제 사용자 확인이 필요한 행위.

이 항목이 있어도 독립 작업이 남아 있으면 전체 루프를 즉시 끝내지 않고 해당 task만 보류한다.

### `GLOBAL_TERMINAL_BLOCKER`

다음 조건을 모두 만족할 때만 사용한다.

- 필수 완료 기준이 남아 있다.
- recovery ladder의 허용된 경로를 모두 소진했다.
- blocked task 외에 실행 가능한 독립 task가 없다.
- 자동 승인·승인 상속·대체 executor로 해결할 수 없다.

## 기존 승인 범위와 실행 방법의 구분

`WHAT/OUTCOME`이 이미 승인되어 있고 새 package/test/run이 그 결과를 구현·검증하는 `HOW`라면 기본적으로 동일 승인 범위다.

예: `robustness를 10k seed로 실제 증명`이 기존 acceptance criterion을 더 강하게 검증하는 행위라면 dedicated 10k package 작성과 실행은 기술 실행 방법이며 자동 승인 가능하다.

단, 외부 유료 자원·시간/금액 예산을 새로 초과하거나 제품 의미를 바꾸면 별도 결정이다.

## exact-head evidence recovery

GitHub/CI 결과 조회 실패는 다음과 같이 처리한다.

```text
expected_head_sha 고정
→ workflow run list 조회
→ exact head run 식별
→ run status/conclusion 재조회
→ job status/conclusion 재조회
→ 필요 시 좁은 job/log query
→ 실패가 일시적/transport면 동일 SHA rerun 가능 여부 확인
→ authoritative PASS/FAIL 확보
```

output truncation은 `FAIL`이 아니다. 단지 `EVIDENCE_TRANSPORT_INCOMPLETE`다.

## 승인 상속과 병합

`CONTINUOUS_WORK_ACTIVE`는 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 반드시 소비한다.

승인 범위의 PR은 별도 `병합할까요?`를 묻지 않는다. exact HEAD, required checks, independent review, unresolved thread 0, P0/P1/CHANGE_PROPOSAL/USER_REVIEW_REQUIRED 없음이 확인되면 저장소가 허용하는 방식으로 즉시 병합한다.

## Global Progress Queue

연속작업은 단일 현재 task만 보지 않고 다음 세 집합을 유지한다.

```yaml
ready_tasks: []
deferred_tasks: []
completed_tasks: []
```

각 blocker 발생 시:

1. 현재 task의 dependency와 blocker 종류를 기록한다.
2. 회복 가능하면 recovery ladder를 실행한다.
3. 당장 못 풀리면 `deferred_tasks`로 이동한다.
4. `ready_tasks`가 있으면 계속 수행한다.
5. 상태 변화 후 deferred task를 다시 평가한다.
6. `ready_tasks == []`이고 남은 필수 task가 모두 terminal-blocked일 때만 전체 중지한다.

## 사례별 기대 동작

### 사례 1 — 10k robustness package

- `STOPPED_USER_DECISION` 금지.
- 기존 robustness 승인 범위라면 package 작성 → TDD → 실제 10k 실행까지 계속.
- 외부 비용/예산 경계를 새로 넘을 때만 사용자 결정.

### 사례 2 — Actions tool-output truncation

- `EVIDENCE_TRANSPORT_INCOMPLETE`로 분류.
- exact head workflow/run/job을 자동 재조회.
- 필요 시 동일 SHA rerun.
- Task 7이 PASS면 상태 동기화 후 Task 8로 계속.
- Task 7이 아직 미확정이면 Task 8 의존성을 지키되 다른 독립 작업은 계속.
- PR은 기존 승인 상속 조건이 충족되면 별도 병합 승인 없이 병합.

### 사례 3/4 — HiGodot unavailable in current session

- 현재 세션 부재만으로 `GLOBAL_TERMINAL_BLOCKER` 금지.
- authorized alternate executor/tool을 자동 탐색.
- 호출 가능한 Codex/agent/환경이 있으면 handoff를 자동 수행.
- 호출할 수 없으면 executor-ready handoff/checkpoint를 자동 생성하고 해당 authoring task만 defer.
- 문서/테스트 설계/CI/정본 동기화 등 독립 작업은 계속.
- persistent Godot authoring 권위 자체는 우회하지 않는다.

## 변경 범위

주 정본:

- `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- `skills/managing-project-intake-and-work-contract/SKILL.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/OPERATING_MODEL.md`
- `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- `skills/maintaining-long-running-task-continuity/SKILL.md`

검증/학습:

- `tests/test_continuous_work_execution_contract.py`
- reference-freshness가 실제 소비하는 기존 회귀 테스트 1개 이상
- `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`
- `skills/SKILL_LEARNING_LOG.md` 또는 관련 package learning log
- `docs/CHANGELOG.md`

## 비목표

- 금지된 HiGodot 권위 우회
- 임의 결제·계정·보안·권한 변경 자동 승인
- 다른 ChatGPT 채팅에 자동 메시지 주입
- 실제로 호출할 수 없는 Codex/agent를 호출했다고 주장
- 무한 retry

## 완료 기준

- 네 사례가 회귀 계약으로 표현된다.
- recoverable blocker는 즉시 전체 stop을 만들지 않는다.
- 독립 ready task가 남아 있으면 계속 수행한다.
- 기존 approval 범위의 실행 package와 merge가 별도 승인 질문을 만들지 않는다.
- current-session tool absence와 global execution-route absence가 구분된다.
- 실제 executor가 없으면 거짓 실행 대신 defer + handoff + 다른 task 진행으로 처리한다.
- 기존 사용자 결정·고위험·권위 Gate는 보존된다.
- exact-head CI와 canonical reference freshness가 통과한다.
