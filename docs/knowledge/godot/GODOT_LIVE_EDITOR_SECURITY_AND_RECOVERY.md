# Godot Live Editor Security and Recovery

## 기본 보안 자세

Godot live-editor 자동화는 기본 off, 최소 권한, typed allowlist와 fail-closed 방식으로 운용한다. 프로젝트가 identity, capability, transport와 복구 절차를 v2 Manifest에 구성하기 전에는 `NOT_CONFIGURED`다. 임의 GDScript·C#·native code·shell, 전체 파일시스템 접근, remote 또는 wildcard bind를 기본 제공하지 않는다.

## 위협 모델

차단 대상은 다음과 같다.

- 다른 프로젝트·service·Editor·runtime session으로 mutation 전송
- 오래된 catalog 또는 input/output Schema로 승인 재사용
- 승인 뒤 arguments·policy·preconditions 변경
- stale Scene 관찰값으로 사용자 변경 덮어쓰기
- timeout 뒤 mutation·test·export duplicate start
- task/result/evidence를 다른 operation에 연결
- `..`, symlink, junction 또는 case 우회로 project root 탈출
- protocol stdout에 진단·secret 출력
- engine input을 physical input으로 과장
- contract 파일 존재를 runtime·human PASS로 과장

## transport profile

- `CLI`: listener가 없고 현재 사용자 프로세스 경계만 사용한다.
- `LOCAL_HTTP`: `127.0.0.1` 또는 `::1`만 허용하며 Origin explicit allowlist, session authentication, project-client session binding, frame·depth·batch·connection·idle 제한이 필요하다.
- `NAMED_PIPE`: current-user 또는 OS peer credential을 검증한다.
- `STDIO_BRIDGE`: 현재 process가 소유하며 stdout은 protocol-only, diagnostics는 stderr다.
- `PROJECT_DEFINED`: identity, approval, path, output, audit와 evidence 규칙을 약화할 수 없다.

endpoint, port, PID와 socket path는 identity가 아니다. normalized path, `project.godot` SHA-256, project fingerprint, `automation_service_instance_id`, 필요한 `editor_instance_id` 또는 active `runtime_session_id`가 일치해야 한다.

## typed action과 경로

`capability_id`, `input_schema`와 confined path roots가 allowlist다. 입력 Schema와 semantic validation을 통과하기 전 handler를 호출하지 않는다. 읽기 action도 Scene tree, Resource, environment와 log를 무제한 반환하지 않는다.

## contract snapshot binding

`contract_snapshot`은 다음을 포함한다.

```yaml
contract_version:
adapter_version:
catalog_sha256:
capability_input_schema_sha256:
capability_output_schema_sha256:
protocol_profile:
protocol_version:
```

승인, ledger, task와 terminal result는 현재 snapshot과 exact equality를 가져야 한다. 하나라도 다르면 `APPROVAL_TOKEN_MISMATCH` 또는 `CONTRACT_SNAPSHOT_MISMATCH`다.

## 승인 binding과 single use

승인 token은 다음 값에 묶는다.

```text
token_id
+ operation_id
+ capability_id
+ project_identity
+ instance_identity
+ contract_snapshot
+ effect_kind / idempotency / approval_policy / execution_mode / rollback_policy
+ request_hash
+ preconditions
+ expiration
```

`approval_policy: REQUIRED`인데 승인되지 않았으면 `APPROVAL_REQUIRED`다. token은 기본 single-use이며 다른 operation ID에서 재사용하면 `APPROVAL_TOKEN_REUSED`다. completed idempotent operation의 exact replay만 같은 result를 반환할 수 있다. automatic approval은 금지한다.

## stale-state와 retry

mutation 전에 expected와 observed revision, content SHA-256, dirty state와 Scene path를 비교한다. 불일치는 `TARGET_STATE_CONFLICT`다. 사용자 미저장 변경을 자동 저장·폐기하지 않는다.

`NON_IDEMPOTENT`와 `IRREVERSIBLE`은 automatic retry를 금지한다. idempotent mutation도 durable ledger가 같은 request와 결과를 증명할 때만 replay할 수 있다. 결과를 모르는 timeout은 실패 확정이 아니며 근거 없는 재전송은 `UNSAFE_RETRY_BLOCKED`다.

## operation ledger와 task

mutation 또는 `LONG_RUNNING_TASK`는 action 전에 durable identity를 기록한다.

```yaml
operation_id:
project_identity:
instance_identity:
contract_snapshot:
capability_id:
request_hash:
idempotency_key:
approval_token_id:
started_at:
state:
task_id:
result_hash:
evidence:
```

`NOT_STARTED`는 task ID가 없다. `QUEUED`, `RUNNING`, `INPUT_REQUIRED`, `PENDING`은 duplicate start를 금지한다. terminal binding이 다르면 `TASK_RESULT_STALE`; result hash가 다르면 `TASK_RESULT_HASH_MISMATCH`다. 진행 중 상태는 `TASK_PENDING`으로 보고한다.

## output과 evidence

handler 결과는 `output_schema`를 통과한 뒤에만 성공으로 승격하며 불일치는 `OUTPUT_SCHEMA_MISMATCH`다. result hash는 canonical result data에서 계산한다.

file-backed PASS evidence는 `artifacts/` 아래 path, SHA-256, timestamp와 producer를 요구한다. kind/state가 맞지 않으면 `EVIDENCE_KIND_STATE_INVALID`, path 탈출은 `EVIDENCE_PATH_OUTSIDE_ARTIFACT_ROOT`다.

## Editor mutation과 rollback

undoable Scene·Resource·setting mutation은 하나의 `EditorUndoRedoManager` transaction으로 묶는다. save, import와 refresh는 명시적이며 각각 증거를 남긴다. 외부 side effect, runtime mutation, 부분 rollback과 사용자 dirty Scene은 별도 위험으로 보고한다.

## 복구 절차

EditorPlugin 또는 tool script로 정상 시작이 실패하면 다음 순서를 사용한다.

```text
mutation stop
→ Godot --recovery-mode
→ project-local adapter disable/remove
→ state BLOCKED_RECOVERY
→ declared snapshot or manual recovery
→ normal Editor startup verification
→ new service and Editor instance IDs
→ renewed approval
```

`--recovery-mode` 시작 자체는 production runtime PASS가 아니다. 복구 뒤 예전 service·Editor approval은 무효다.

## 입력·테스트·사람 경계

Godot 내부 dispatch는 `ENGINE_INPUT_PASS`일 수 있지만 OS mouse·keyboard·window focus를 증명하지 않는다. 별도 경로가 없으면 `PHYSICAL_INPUT_EVIDENCE_BLOCKED`다. test runner가 미등록이면 `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`; 사람 검증이 없으면 `HUMAN_NOT_RUN`이다.

## 안정 코드

- `PROJECT_IDENTITY_MISMATCH`
- `CAPABILITY_NOT_DECLARED`
- `CATALOG_STALE`
- `ADAPTER_VERSION_MISMATCH`
- `CONTRACT_SNAPSHOT_MISMATCH`
- `APPROVAL_REQUIRED`
- `APPROVAL_TOKEN_MISMATCH`
- `APPROVAL_TOKEN_REUSED`
- `TARGET_STATE_CONFLICT`
- `OUTPUT_SCHEMA_MISMATCH`
- `UNSAFE_RETRY_BLOCKED`
- `TASK_PENDING`
- `TASK_RESULT_STALE`
- `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`
- `PHYSICAL_INPUT_EVIDENCE_BLOCKED`
- `MIGRATION_REQUIRED_V1`
