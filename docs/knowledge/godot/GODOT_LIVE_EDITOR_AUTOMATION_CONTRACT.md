# Godot Live Editor Automation Contract

## 목적과 권한

이 문서는 AI 작업자가 Godot 프로젝트의 CLI, 실행 중 Editor, Scene, Resource, ProjectSettings, 테스트, export와 runtime 상태를 안전하게 관찰·변경·검증하기 위한 Base 공용 계약이다. Base는 typed capability, 실행 안전, 복구와 증거 경계만 소유한다. 실제 명령, EditorPlugin, runtime debugger와 프로젝트 증거는 각 프로젝트가 소유한다.

프로젝트 설치 Template은 `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`이며 기본 상태는 `NOT_CONFIGURED`다. 파일 존재만으로 Editor 연결, 명령 지원, 테스트 runner, runtime 또는 사람 검증을 주장하지 않는다.

## 활성 v2 권위

활성 계약 파일은 다음과 같다.

- `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- `tools/validate_godot_live_editor_contract_v2.py`

실행 순서는 고정한다.

```text
manifest v2 Schema validation
→ manifest semantic validation
→ operation v2 Schema validation
→ exact identity and contract_snapshot validation
→ input_schema validation
→ typed project capability execution
→ output_schema validation
→ result/evidence hash binding
```

JSON Schema는 구조를 검사하고 semantic validator는 equality, hash, approval reuse, stale state와 cross-field 규칙을 검사한다. 둘 중 하나라도 실패하면 engine action 전에 중단한다.

## v1 감사 경계

v1 Schema와 `examples/godot-live-editor-pilot/` 증거는 회귀와 감사용으로 보존하며 상태는 `V1_AUDIT_ONLY`다. v1 Manifest 또는 과거 `operation_class` 값을 v2 mutation 권한으로 추론하지 않는다. 프로젝트가 v1로 구성되어 mutation을 요청하면 `MIGRATION_REQUIRED_V1` 또는 validator의 `V1_MUTATION_AUTHORITY_REJECTED`로 중단한다.

## 실행 경로

### `CLI_HEADLESS`

Godot 실행 파일을 직접 사용하되 Manifest에 등록된 command, arguments, path, timeout과 evidence만 허용한다.

### `EDITOR_PLUGIN`

Scene·Node·Resource·Inspector·ProjectSettings 변경은 등록된 typed action만 사용한다.

```text
bounded request
→ exact Editor instance 확인
→ expected/observed precondition 비교
→ 직렬화된 Editor main-thread queue
→ EditorUndoRedoManager transaction
→ explicit save/import/refresh
→ output validation and evidence
```

### `RUNTIME_DEBUGGER`

Runtime 관찰은 `EditorDebuggerPlugin`, `EditorDebuggerSession`, `EngineDebugger` 또는 project debug API를 사용한다. active `runtime_session_id`가 없는 runtime action은 실패한다.

## 부트스트랩

모든 engine 작업은 다음 순서를 사용한다.

```text
doctor → status → catalog --compact
→ normalized project path
→ project.godot SHA-256
→ project fingerprint
→ automation_service_instance_id
→ editor_instance_id or runtime_session_id
→ contract_snapshot and catalog freshness
```

port, PID, window title와 폴더 substring은 힌트일 뿐이다. 불일치하면 `PROJECT_IDENTITY_MISMATCH`, 미등록 capability는 `CAPABILITY_NOT_DECLARED`, 오래된 catalog는 `CATALOG_STALE`다.

## Capability Manifest v2

각 capability는 다음 독립 축을 모두 선언한다.

```yaml
effect_kind: READ_ONLY | MUTATION
idempotency: NOT_APPLICABLE | IDEMPOTENT | NON_IDEMPOTENT
approval_policy: NOT_REQUIRED | REQUIRED
execution_mode: SYNCHRONOUS | LONG_RUNNING_TASK
rollback_policy: NOT_APPLICABLE | EDITOR_UNDO_REDO | SNAPSHOT | MANUAL | IRREVERSIBLE
```

또한 `input_schema`, `output_schema`, `capability_input_schema_sha256`, `capability_output_schema_sha256`, path roots, precondition, retry, timeout, evidence와 unsupported state를 선언한다. 읽기·mutation·승인·수명·rollback 의미를 한 enum으로 합치지 않는다.

## Operation Envelope v2

```yaml
operation_id:
capability_id:
project_identity:
instance_identity:
contract_snapshot:
policy:
request:
  arguments:
request_hash:
idempotency_key:
preconditions:
approval:
task:
result:
  success:
  code:
  data:
  result_hash:
  evidence:
```

`contract_snapshot`은 contract·adapter version, catalog SHA-256, input/output Schema SHA-256, protocol profile과 version을 포함한다. request hash는 capability, identity, snapshot, policy, preconditions와 arguments를 canonical JSON으로 묶는다.

## stale-state 차단

Scene·Resource·Inspector·ProjectSettings처럼 사람이 바꿀 수 있는 mutation은 예상값과 실행 직전 관찰값을 함께 기록한다.

```yaml
expected_target_revision:
observed_target_revision:
expected_target_content_sha256:
observed_target_content_sha256:
expected_dirty_state:
observed_dirty_state:
expected_scene_path:
observed_scene_path:
conflict_policy: FAIL_CLOSED
```

한 값이라도 다르면 `TARGET_STATE_CONFLICT`다. dirty Scene을 자동 저장·폐기하거나 새 관찰 없이 재승인하지 않는다.

## 승인·retry·task

승인은 exact operation, capability, project/service/Editor/runtime identity, `contract_snapshot`, 다섯 policy 축, request hash, preconditions와 expiry에 묶는다. 값이 다르면 `APPROVAL_TOKEN_MISMATCH`; 승인이 없으면 `APPROVAL_REQUIRED`다. automatic approval은 금지한다.

idempotent mutation도 ledger와 exact replay 증거가 없으면 재전송하지 않는다. unknown outcome을 맹목적으로 다시 실행하면 `UNSAFE_RETRY_BLOCKED`다.

장기 작업은 receiver-generated durable `task_id`를 한 번 만들고 `TASK_PENDING` 동안 duplicate start를 금지한다. terminal result가 다른 operation/service/task에 묶이면 `TASK_RESULT_STALE`다.

## 입력·출력·증거

입력은 action 전에 `input_schema`로, 결과 data는 성공 승격 전에 `output_schema`로 검사한다. 출력 불일치는 `OUTPUT_SCHEMA_MISMATCH`다. file-backed PASS evidence는 `artifacts/` 아래 confined path, SHA-256, timestamp와 producer 선언을 요구한다.

정적 validator는 evidence의 kind/state/path/hash **형식과 binding**만 검사한다. `artifact_sha256`이 실제 파일 bytes와 일치하는지는 승인된 artifact root를 읽을 수 있는 project/runtime validator가 별도로 검증해야 하며, 정적 JSON 검사만으로 physical artifact proof를 주장하지 않는다.

증거 상태를 합치지 않는다.

- `CONTRACT_PASS`
- `EXECUTION_PASS`
- `RUNTIME_PASS`
- `ENGINE_INPUT_PASS`
- `PHYSICAL_INPUT_PASS`
- `HUMAN_PASS`

project test runner가 없으면 `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`, OS 입력 경로가 없으면 `PHYSICAL_INPUT_EVIDENCE_BLOCKED`다. `BLOCKED_ENVIRONMENT`, `NOT_RUN`, `HUMAN_NOT_RUN`은 PASS가 아니다.

## 기존 Base 책임 연결

- 설치·Manifest·legacy adapter: `managing-game-project-operating-system`
- runtime 재현·원인 격리: `diagnosing-game-engine-runtime-failures`
- static·runtime·regression: `reviewing-and-validating-project-changes`
- UI·screenshot·입력 증거: `auditing-and-refining-ui-art`
- task checkpoint·resume: `maintaining-long-running-task-continuity`
- contract·Schema·catalog freshness: `auditing-canonical-reference-freshness`
- 반복 교훈의 Skill 경계: `evolving-project-discipline-skills`

프로젝트 adapter `godot-live-editor-operations`는 설치 Template이며 Base active Skill Registry에 추가하지 않는다.

## 실패 보고

```yaml
status: PASS | FAIL | NOT_CONFIGURED | BLOCKED_ENVIRONMENT
project_identity:
instance_identity:
contract_snapshot:
capability_id:
policy:
operation_id:
task_id:
stable_code:
changed_targets:
evidence:
rollback_or_recovery:
unverified:
```
