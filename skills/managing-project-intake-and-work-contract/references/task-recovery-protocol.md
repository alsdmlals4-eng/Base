# Task Recovery Protocol

## 목적과 책임 경계

`TASK_RECOVERY_PROTOCOL`은 메시지 `timeout`, `network` 오류, 응답 생성 실패, 실행 프로세스 종료, `stalled` 상태처럼 **승인된 작업 계약이 예기치 않게 중단된 뒤 안전하게 계속하기 위한 상위 복구 계약**이다.

이 프로토콜은 새로운 Skill이나 Work Mode가 아니다. 기존 `continuous-work-execution.md`의 blocker recovery와 Global Progress Queue를 재사용하며, Git worktree 기반 실행을 재연결해야 할 때는 기존 Loop A2 durable-resume owner의 exact identity/ownership receipt 검증을 재사용한다. 외부 Watchdog나 트레이 프로그램은 `WATCHDOG_SIGNAL`을 전달할 뿐 **실행 권한을 새로 부여하지 않는다**.

핵심 원칙은 다음과 같다.

```text
INTERRUPTION
→ CLASSIFY
→ RETRY 또는 RESUME 결정
→ CHECKPOINT + 현재 상태 재확인
→ 완료된 작업 보호
→ 미완료 작업만 계속
→ VERIFY
```

## `RETRY`와 `RESUME`을 분리한다

### `RETRY`

동일 동작을 다시 수행해도 중복 실행이나 외부 부작용이 생기지 않는 일시적 실패에서만 사용한다.

대표 대상:

- 명시적인 메시지 `timeout`
- 일시적 `network` 오류
- 응답 생성 단계의 명시적 transient error
- 아직 외부 부작용이 시작되지 않았음이 확인된 bounded request

기본 웹 복구 backoff는 **3초 → 10초 → 30초, 최대 3회**다. 이 경로를 소진하면 같은 요청을 계속 누르지 않고 `RECOVERY_REQUIRED`로 승격한다. 무한 retry는 금지한다.

`stalled`는 단순히 출력 변화가 일정 시간 없다는 관찰 신호다. 서버가 실제로 요청을 처리 중일 가능성을 배제할 수 없으므로 **자동 재전송 금지**다. 먼저 `RESUME` 경로로 전환해 현재 상태를 읽는다.

### 연결 단절 + 전체 답변 대기

ChatGPT 웹에서 다음과 같은 명시적 상태가 보이면 독립적인 복구 신호로 취급한다.

```text
연결이 끊어졌습니다. 전체 답변을 기다리는 중입니다
```

이 상태는 프롬프트가 서버에 이미 전달되고 응답이 계속 처리 중일 수 있으므로, 마지막 프롬프트를 blind resend하지 않는다.

```text
명시적 연결 단절 신호
→ 같은 오류 surface 안의 안전한 retry control 확인
   ├─ 존재: bounded RETRY
   └─ 없음: RECOVERY_REQUIRED
→ 동일 대화/작업 identity의 현재 상태 readback
→ 완료 응답이 이미 존재하면 재전송 없이 RECOVERED
→ 미완료이면 안전한 reconnect/resume 경로만 사용
```

`다시 시도`, `Retry`, `Try again`, `Regenerate`처럼 오류와 같은 국소 surface에 속한 **안전한 retry control**만 자동 클릭 후보가 된다. 다른 영역의 버튼, 승인/확인 버튼, 일반 `Continue`는 retry control로 간주하지 않는다.

### `RESUME`

이미 일부 단계가 실행됐을 가능성이 있거나 부작용이 있는 작업에서 사용한다. 재개 전에 반드시 `CHECKPOINT`와 현재 정본을 비교한다.

```text
trusted CHECKPOINT 식별
→ 현재 상태 재확인
→ repository / external system readback
→ 완료된 작업과 pending 작업 분리
→ 이미 완료된 단계는 다시 실행하지 않는다
→ pending 단계만 계속
→ postcondition 검증
```

체크포인트가 없거나 신뢰할 수 없으면 마지막 프롬프트를 그대로 재전송하지 않는다. 권위 있는 현재 상태에서 재구성할 수 있는 범위만 복구하고, 나머지는 `RECOVERY_REQUIRED` 또는 `BLOCKED_UNVERIFIED`로 둔다.

## 체크포인트 우선순위

복구 시 사실의 우선순위는 다음과 같다.

1. 현재 저장소/서비스의 authoritative readback
2. exact identity에 묶인 durable receipt/checkpoint
3. 현재 승인된 작업 계약과 기록된 completed/pending 상태
4. 최근 실행 로그
5. 추정

Git worktree 기반 Loop A2 실행이라면 기존 durable-resume 계약을 사용한다. `project_id`, `run_id`, `expected_main_sha`, source repository, workspace ownership이 검증된 경우에만 기존 작업공간을 재연결한다. receipt가 stale/corrupt/missing이면 새 권위를 추정하거나 임의 adopt하지 않는다.

## 부작용이 있는 작업의 복구

다음 작업은 blind `RETRY`가 아니라 기본적으로 `RESUME + readback + idempotency`를 사용한다.

| 작업 | 재개 전 확인 |
|---|---|
| 파일 수정 | 실제 파일/diff와 정본을 readback해 변경 적용 여부 확인 |
| `commit` | Git HEAD/log/status에서 동일 변경의 commit 존재 여부 확인 |
| `PR` 생성/수정 | 동일 Goal/branch의 PR 존재 여부와 current head 확인 |
| `merge` | PR merged 상태와 새 main readback 확인 |
| 메일 | Sent/Draft 또는 provider receipt를 확인한 뒤 재전송 여부 판정 |
| 외부 전송/API write | provider 상태, request/result identity, postcondition 확인 |

가능하면 작업 자체에 `idempotency` key 또는 stable operation identity를 사용한다. 그렇지 못하면 상태 확인으로 중복 실행 위험을 줄인다. **이미 완료된 단계는 다시 실행하지 않는다.**

## 상태와 Watchdog 신호

외부 Watchdog/트레이/브라우저 확장은 복구 상태를 다음처럼 전달할 수 있다.

```text
WATCHDOG_SIGNAL
├─ RETRYING
├─ RECOVERY_REQUIRED
├─ RECOVERED
└─ FAILED_TERMINAL
```

- `RETRYING`: 명시적 transient failure에 대해 bounded `RETRY`가 진행 중이다.
- `RECOVERY_REQUIRED`: retry ceiling, `stalled`, unsafe/missing retry control, 연결 단절, 불확실한 side effect처럼 상태 재확인이 필요하다.
- `RECOVERED`: 같은 작업 identity에서 retry 또는 resume 뒤 실행이 정상적으로 다시 진행되거나 terminal success를 확인했다.
- `FAILED_TERMINAL`: bounded recovery path를 소진했거나 인증/권한/계약 위반처럼 자동 복구하면 안 되는 실패다.

신호는 관찰 결과일 뿐 approval, repository write, 결제, 계정, 보안 또는 다른 실행 권위를 자동으로 생성하지 않는다.

## 승인·권위 보존

복구는 언제나 **승인된 작업 계약** 안에서만 수행한다.

다음은 자동 승인하지 않는다.

- `USER_DECISION_REQUIRED`
- `HIGH_RISK_CONFIRMATION_REQUIRED`
- 기존 승인 범위를 넘는 범위 확대
- 프로젝트가 정한 단일 authoring/runtime 권위의 우회
- 새로운 자격 증명·보안·결제·계정 권한 부여

복구를 위해 alternate executor를 사용하더라도 기존 권위와 파일 쓰기/보안 계약을 그대로 지킨다. 현재 세션에서 호출할 수 없는 executor를 호출했다고 주장하지 않는다.

## 연속작업과 결합

`CONTINUOUS_WORK_ACTIVE`에서 interruption이 발생하면 `TASK_RECOVERY_PROTOCOL`을 실행한 뒤 기존 Global Progress Queue로 돌아간다.

```text
interrupted task
→ RETRY/RESUME recovery
→ 성공: 원래 task 계속
→ 국소 미복구: deferred_tasks
→ ready_tasks가 있으면 독립 작업 계속
→ dependencies 변화 후 deferred task 재평가
→ GLOBAL_TERMINAL_BLOCKER는 기존 조건을 모두 만족할 때만 사용
```

즉 이 프로토콜은 `continuous-work-execution.md`의 recovery ladder를 대체하지 않고, **실행 자체가 끊긴 상황에서 recovery ladder로 안전하게 돌아오기 위한 입구**다.

## 완료·검증

복구 완료를 선언하려면 최소 다음을 확인한다.

- 같은 작업/대화/실행 identity인지 확인
- 완료된 단계가 중복 실행되지 않았는지 확인
- pending 단계가 실제로 재개되었는지 확인
- 저장소 작업이면 diff/HEAD/PR/main readback
- 테스트/CI 작업이면 exact-head 결과
- 외부 write면 provider postcondition 또는 receipt

관찰할 수 없는 상태는 성공으로 추정하지 않는다.

## 비목표와 롤백

이 프로토콜은 scheduler, webhook, 브라우저가 닫힌 뒤의 임의 백그라운드 실행, 다른 ChatGPT 채팅으로의 자동 메시지 주입을 새로 허용하지 않는다. 실제 외부 Watchdog/Runner 구현은 별도 실행 도구가 담당하며 이 문서는 그 도구에 새로운 authority를 부여하지 않는다.

문서 계약 자체의 롤백은 이 참조와 `continuous-work-execution.md` 연결을 revert하면 된다. Loop A2 durable-resume, 기존 blocker taxonomy, 승인 상속, 사용자 결정/고위험 Gate는 독립 owner로 그대로 보존한다.
