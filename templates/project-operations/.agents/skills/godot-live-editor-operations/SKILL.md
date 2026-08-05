---
name: godot-live-editor-operations
description: Use in an installed Godot project when registered CLI, EditorPlugin, or runtime-debugger capabilities must be bootstrapped, observed, mutated, validated, resumed, or recovered.
---

# Godot Live Editor Operations

## 책임과 정본 해석

이 파일은 프로젝트에 설치되는 얇은 adapter다. 먼저 `skills/PROJECT_BASE_ADAPTER.json`과 generated snapshot을 검증하고, validated Base adapter가 고정한 repository·commit에서 다음 **Base canonical contract**를 읽는다.

- `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- `tools/validate_godot_live_editor_contract_v2.py`

공용 계약과 Schema를 프로젝트에 복제하지 않는다. 프로젝트가 소유하는 것은 `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`, 이 adapter, 실제 CLI/EditorPlugin/runtime bridge와 프로젝트 증거다. Base adapter 검증 또는 pin 해석이 실패하면 engine action 전에 중단한다.

Base active Skill을 대체하거나 새 광역 책임을 만들지 않는다.

## Modes

`bootstrap` → `observe` → `mutate` → `validate` → `resume` → `recover`

## v2 gate

다음 순서를 고정한다.

```text
validate Base adapter pin and snapshot
→ classify manifest version
→ v1 authorization이면 MIGRATION_REQUIRED_V1
→ validate manifest v2 Schema
→ validate manifest semantics
→ select one declared capability
→ validate operation v2 Schema
→ validate exact identity, contract_snapshot and request
→ execute one typed capability
→ validate output and bind evidence
```

v1 Schema와 Pilot 증거는 `V1_AUDIT_ONLY`로만 읽는다. 과거 class 값을 현재 권한으로 추론하지 않는다.

다음 중 하나면 engine action 전에 중단한다.

- Base adapter 또는 snapshot 검증 실패
- Manifest 없음·JSON/Schema 오류
- `configuration_state: NOT_CONFIGURED`
- normalized path, `project.godot` SHA-256 또는 fingerprint 불일치
- service·Editor·runtime identity 불일치
- adapter·contract·catalog·Schema hash 불일치
- 요청 capability 미등록
- unsupported engine state
- v1 Manifest로 mutation 요청

부트스트랩은 `doctor → status → catalog --compact` 순서다. port 또는 PID만으로 target을 선택하지 않는다.

## PR B Editor transaction adapter

프로젝트가 listener-free Editor transaction adapter를 채택하면 다음 canonical addon을 복사한다.

`godot-live-editor/addons/base_live_editor_adapter/`

configured v2 Manifest는 v2 Schema에 맞는 정확한 in-process profile을 사용한다.

```yaml
transport:
  kind: PROJECT_DEFINED
  enabled: true
  bind_host: null
  endpoint_identity: in-process-editor-plugin
  protocol_profile: GENERIC
  protocol_version: in-process-1.0
  access_control:
    authentication_mode: NOT_APPLICABLE
    origin_policy: NOT_APPLICABLE
    session_binding: NOT_APPLICABLE
    os_access_control: CURRENT_USER_ONLY
```

`enabled: true`는 선언된 in-process endpoint가 활성 상태라는 뜻이며 network listener를 만들지 않는다. addon은 이미 Base v2 Schema·semantic validator를 통과한 envelope를 in-process `submit_validated_operation()`으로만 받는다. 서버, MCP, socket, HTTP/WebSocket, background thread 또는 Autoload를 제공하지 않는다.

허용 capability는 다음 두 개뿐이다.

- `scene.inspect`
- `node.rename` + `KEEP_DIRTY | SAVE_CURRENT_SCENE`

한 Editor frame에서 fresh precondition을 다시 확인하고, mutation은 STARTED ledger 뒤 한 번의 `EditorUndoRedoManager` transaction으로 실행한다. save·filesystem update·physical byte SHA-256·output/evidence·terminal ledger가 완료되기 전에는 성공을 보고하지 않는다.

Manifest가 없거나 malformed, v1, `NOT_CONFIGURED`, endpoint identity 불일치, bind 설정 존재, identity 불완전 또는 capability 없음이면 addon은 `ADAPTER_NOT_CONFIGURED`로 닫힌다. 시작 실패 시 Godot `--recovery-mode`로 addon을 비활성화하거나 제거하고 새 Editor instance ID와 승인을 발급한다.

## Policy axes

각 capability는 다음을 독립 선언한다.

```yaml
effect_kind:
idempotency:
approval_policy:
execution_mode:
rollback_policy:
```

`effect_kind: READ_ONLY`는 side effect가 없어야 한다. mutation은 ledger, retry, precondition, rollback과 evidence를 명시한다. `approval_policy: REQUIRED`는 exact identity, `contract_snapshot`, request hash와 preconditions에 묶인 승인이 필요하다. `execution_mode: LONG_RUNNING_TASK`는 receiver-generated durable task ID로 start-once·resume한다.

automatic approval은 금지한다. unsafe retry는 `UNSAFE_RETRY_BLOCKED`로 끝내고 `recover`에서 현재 상태를 reconcile한다.

## Existing owner routing

- 설치·Manifest·legacy adapter: `managing-game-project-operating-system`
- runtime 재현·원인 격리: `diagnosing-game-engine-runtime-failures`
- static·runtime·regression 검증: `reviewing-and-validating-project-changes`
- UI·screenshot·engine/physical input 구분: `auditing-and-refining-ui-art`
- pending task·checkpoint·resume: `maintaining-long-running-task-continuity`
- contract·Schema·catalog freshness: `auditing-canonical-reference-freshness`
- 반복 증거 기반 Skill 승격 판정: `evolving-project-discipline-skills`

현재 주 책임 owner가 engine action 범위를 정하고, 이 adapter는 capability 실행 증거만 제공한다.

## Mode rules

### `bootstrap`

Base pin, Manifest version, v2 Schema, semantic validator, project/instance identity, engine version, transport와 catalog를 검증한다.

### `observe`

필요한 Scene·Node·Resource·setting·log·runtime 상태만 bounded output으로 읽는다. mutation을 위한 관찰은 revision/hash/dirty state/Scene path를 기록한다.

### `mutate`

expected/observed 값이 다르면 `TARGET_STATE_CONFLICT`다. 승인된 typed action만 실행하고 undoable action은 `EditorUndoRedoManager` transaction과 save/import/refresh 경계를 기록한다.

### `validate`

입력은 action 전에, output은 성공 승격 전에 검사한다. 불일치는 `OUTPUT_SCHEMA_MISMATCH`다. `CONTRACT_PASS`, `EXECUTION_PASS`, `RUNTIME_PASS`, `ENGINE_INPUT_PASS`, `PHYSICAL_INPUT_PASS`, `HUMAN_PASS`를 분리한다.

### `resume`

기존 `operation_id`와 `task_id`를 조회하고 initiating action을 다시 보내지 않는다.

### `recover`

identity, catalog, ledger와 target state를 재관찰한다. Editor 시작 실패는 project 절차에 따라 Godot `--recovery-mode`로 adapter를 비활성화하고 새 instance ID와 승인을 요구한다.

## Output

```yaml
mode:
base_adapter_commit:
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
verification:
unverified:
```

## Failure conditions

- validated Base adapter 없이 정본 경로 추정
- 공용 계약 복제
- port-only target selection
- arbitrary script 또는 shell 기본 허용
- automatic approval
- unsafe retry
- stale target 위 mutation
- task pending 중 duplicate start
- output Schema 실패를 성공으로 승격
- engine input을 physical input으로 보고
- test framework 미등록 상태를 PASS로 보고
- contract 파일 존재를 runtime·human PASS로 보고
