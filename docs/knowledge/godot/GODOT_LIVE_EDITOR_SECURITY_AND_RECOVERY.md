# Godot Live Editor Security and Recovery

## 기본 보안 자세

Godot live-editor bridge는 기본 off, 최소 권한, loopback 전용, typed allowlist 방식으로 운용한다. 프로젝트가 transport·action·identity를 Manifest에 구성하기 전에는 `NOT_CONFIGURED`다. 원격 네트워크 공개, 임의 script 실행, 임의 shell 실행, 전체 파일시스템 접근을 기본 capability로 제공하지 않는다.

## 위협 모델

막아야 할 주요 실패는 다음과 같다.

- 다른 Godot 프로젝트나 재사용된 port에 mutation 전송
- stale catalog 또는 다른 adapter version으로 action 실행
- 승인된 request의 arguments를 바꿔 token 재사용
- timeout 뒤 실제 완료 여부를 모른 채 mutation·test·export 중복 시작
- task 결과를 다른 project·operation에 연결
- 경로 탈출로 프로젝트 밖 파일 수정
- engine input을 physical OS input으로 과장
- contract 파일 존재를 runtime·human PASS로 과장
- log·result에 secret 또는 절대 개인 경로 노출

## 전송과 endpoint

- local HTTP는 `127.0.0.1` 또는 `::1`에만 bind한다.
- named pipe와 stdio bridge는 현재 사용자와 현재 project adapter로 범위를 제한한다.
- endpoint는 프로젝트 identity가 아니다. port·PID·socket path가 바뀌어도 normalized path, `project.godot` hash와 fingerprint가 일치해야 한다.
- browser Origin, 외부 interface, wildcard bind와 인증 없는 remote access는 fail closed한다.
- stdout이 protocol transport이면 진단 문구를 stderr 또는 별도 log로 보낸다.

## Typed action과 경로 제한

Capability Manifest의 `capability_id`와 arguments Schema가 allowlist다. 요청은 Schema 검증 뒤에만 handler로 전달한다.

- repository-relative path 또는 명시된 project root 아래 경로만 허용한다.
- `..`, symlink escape, junction escape와 case-normalization 우회는 canonical path 검사로 거부한다.
- arbitrary GDScript·C#·native code·shell 문자열을 일반 action으로 전달하지 않는다.
- 꼭 필요한 project tool script는 고정된 파일과 고정 entrypoint로 등록하고 hash와 arguments를 검증한다.
- 읽기 action도 Scene tree·Resource·log·environment 전체를 무제한 반환하지 않는다.

## 승인 binding

승인 token은 다음 값에 묶는다.

```text
token_id
+ project fingerprint
+ capability_id
+ normalized arguments
+ request_hash
+ operation_class
+ expiration
```

`APPROVAL_REQUIRED_MUTATION`, `NON_RETRYABLE_MUTATION`과 위험한 `LONG_RUNNING_TASK`는 사전 승인을 요구한다. 승인 후 project·action·argument·hash·등급 중 하나라도 바뀌면 `APPROVAL_TOKEN_MISMATCH`다.

token은 기본 single-use다. batch 승인은 같은 project, 같은 operation class, 명시된 action 목록과 최대 항목 수에만 유효하다. AI는 automatic approval을 수행하지 않는다.

## Idempotency와 retry

`READ_ONLY`만 기본 자동 retry 대상이다. `IDEMPOTENT_MUTATION`은 같은 idempotency key가 operation ledger에서 같은 normalized request와 결과를 가리킬 때만 retry할 수 있다.

다음은 unsafe retry다.

- mutation response가 사라졌는데 ledger가 없음
- project fingerprint 또는 catalog가 바뀜
- approval token이 만료되거나 request가 달라짐
- action이 `NON_RETRYABLE_MUTATION`
- task가 아직 존재할 수 있음
- rollback 가능 여부를 확인하지 못함

이 경우 `UNSAFE_RETRY_BLOCKED`를 반환하고 observe→reconcile 뒤 새 operation 여부를 판정한다.

## Operation ledger

각 mutation과 long task는 최소한 다음을 durable record로 남긴다.

```yaml
operation_id:
project_fingerprint:
capability_id:
request_hash:
idempotency_key:
approval_token_id:
started_at:
last_observed_at:
state:
task_id:
result_hash:
evidence_paths:
```

ledger는 요청보다 먼저 또는 같은 원자 경계에서 생성한다. 완료 record는 result hash와 target identity를 보존한다. 정리 정책은 최근 실패·pending·승인 작업을 조기 삭제하지 않는다.

## Timeout과 복구

timeout은 결과 미수신이지 실패 확정이 아니다.

1. normalized project path와 project fingerprint를 다시 확인한다.
2. process 소유권과 endpoint reachability를 별도로 확인한다.
3. adapter catalog version과 ledger를 다시 읽는다.
4. `operation_id` 또는 `task_id` 상태를 조회한다.
5. 완료·실패·pending·stale을 분리한다.
6. idempotency 또는 resume 근거가 있을 때만 계속한다.

다른 process가 같은 endpoint를 사용하거나 project hash가 달라졌으면 `PROJECT_IDENTITY_MISMATCH`다. catalog hash가 달라졌으면 `CATALOG_STALE`이며 재-bootstrap 전 실행하지 않는다.

## 장기 task

`LONG_RUNNING_TASK`는 start-once다. `task_id`가 만들어진 뒤 `status`와 `resume`은 같은 ledger/result store를 읽고 initiating action을 다시 전송하지 않는다.

- `QUEUED`, `RUNNING`, `PENDING`은 새 run 시작 금지
- `COMPLETED`, `FAILED`, `CANCELLED`, `STALE` 결과는 project·capability·operation·task binding 필수
- 다른 fingerprint 또는 오래된 adapter 결과는 `TASK_RESULT_STALE`
- stale heartbeat만으로 task 실패 판정 금지
- cancel은 capability가 안전한 cancel boundary를 선언한 경우만 실행

## Editor mutation과 rollback

가능한 Scene·Resource·setting mutation은 EditorUndoRedoManager로 undo/redo transaction을 만든다. 다음은 별도 보고한다.

- external process 또는 import side effect로 undo 불가
- 파일 저장 뒤 부분 rollback만 가능
- export·package·network side effect
- runtime state mutation
- 이미 존재한 사용자 미저장 변경과 충돌

rollback이 불완전하면 mutation 전 snapshot 또는 Git 복구 경로를 요구한다. 사용자 미저장 변경을 자동 폐기하지 않는다.

## 입력·테스트·화면 검증

Godot 내부 action dispatch는 `ENGINE_INPUT_PASS`일 수 있지만 물리 mouse·keyboard·window focus를 증명하지 않는다. OS 수준 관찰 도구가 없으면 `PHYSICAL_INPUT_EVIDENCE_BLOCKED`다.

project test framework가 등록되지 않으면 `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`다. engine self-test, script parse, Scene load와 game behavior test를 한 상태로 합치지 않는다.

screenshot과 viewport capture는 지정한 frame의 시각 출력만 증명한다. 사람이 이해하기 쉽거나 접근 가능하다는 결론은 `HUMAN_PASS` 증거가 필요하다.

## Secret과 진단 데이터

- token, API key, credential, home directory와 개인 절대 경로를 response에 넣지 않는다.
- log는 필요한 line과 error category만 반환하고 secret pattern을 redact한다.
- shared 문서·fixture에는 repository-relative path와 placeholder를 사용한다.
- diagnostic artifact의 보존 위치·수명·접근 권한을 project contract에 기록한다.

## 복구 판정 코드

| code | 의미 |
|---|---|
| `PROJECT_IDENTITY_MISMATCH` | target identity가 일치하지 않음 |
| `CAPABILITY_NOT_DECLARED` | allowlist에 action이 없음 |
| `CATALOG_STALE` | capability catalog가 현재 adapter와 맞지 않음 |
| `ADAPTER_VERSION_MISMATCH` | contract와 adapter version이 호환되지 않음 |
| `APPROVAL_REQUIRED` | 승인 없이 mutation을 시작할 수 없음 |
| `APPROVAL_TOKEN_MISMATCH` | 승인 binding이 현재 request와 다름 |
| `UNSAFE_RETRY_BLOCKED` | 중복 side effect 위험 때문에 재전송 금지 |
| `TASK_PENDING` | 기존 task가 아직 진행 또는 결과 대기 중 |
| `TASK_RESULT_STALE` | task 결과 identity 또는 freshness가 불일치 |
| `ENGINE_STATE_UNSUPPORTED` | 현재 import·play·debug 상태에서 action 금지 |
| `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED` | 프로젝트 테스트 runner 미등록 |
| `PHYSICAL_INPUT_EVIDENCE_BLOCKED` | OS 입력 증거 경로가 없음 |
