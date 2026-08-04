---
name: godot-live-editor-operations
description: Use in an installed Godot project when registered CLI, EditorPlugin, or runtime-debugger capabilities must be bootstrapped, observed, mutated, validated, resumed, or recovered.
---

# Godot Live Editor Operations

## 책임과 정본 해석

이 파일은 프로젝트에 설치되는 얇은 adapter다. 먼저 `skills/PROJECT_BASE_ADAPTER.json`과 생성 snapshot을 프로젝트의 기존 validator로 검사한다. 검사를 통과한 **validated Base adapter**가 고정한 Base repository·commit에서 다음 **Base canonical contract**를 읽는다.

- `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`
- `schemas/godot-live-editor-capability-manifest-v1.schema.json`
- `schemas/godot-live-editor-operation-envelope-v1.schema.json`
- `tools/validate_godot_live_editor_contract.py`

공용 본문·Schema·semantic validator를 프로젝트 내부에 복제하지 않는다. 프로젝트가 소유하는 것은 `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`, 이 adapter, 실제 command/EditorPlugin/runtime bridge와 프로젝트 증거다. Base adapter 검증 또는 pin 해석이 실패하면 engine action 전에 중단한다.

Base active Skill을 대체하거나 새 광역 책임을 만들지 않는다.

## Modes

`bootstrap` → `observe` → `mutate` → `validate` → `resume` → `recover`

## Manifest gate

다음 중 하나면 engine action 전에 중단한다.

- `skills/PROJECT_BASE_ADAPTER.json` 또는 generated snapshot 검증 실패
- Manifest 없음·JSON/Schema 오류
- semantic validator 오류
- `configuration_state: NOT_CONFIGURED`
- normalized project path, `project.godot` SHA-256 또는 project fingerprint 불일치
- detected Godot version·지원 범위 누락 또는 불일치
- tool source·version pin·telemetry·external data·uninstall·rollback 정책 누락
- adapter·contract version 불일치
- catalog `STALE / MISMATCH`
- 중복 `capability_id`
- 요청 capability 미등록
- configured project test runner가 catalog와 불일치
- 현재 engine state가 `unsupported_states`에 포함됨

부트스트랩은 `doctor → status → catalog --compact` 순서다. port 또는 PID만으로 target을 선택하지 않는다.

## Operation contract

1. validated Base adapter에서 공용 계약·Schema·semantic validator를 해석한다.
2. 한 개의 등록 capability와 arguments Schema를 선택한다.
3. `effect_class`와 `execution_mode`를 각각 확인한다.
4. exact normalized request와 request hash를 만든다.
5. approval·idempotency·ledger·timeout 조건을 확인한다.
6. action을 한 번 시작한다.
7. compact operation envelope와 evidence path를 기록한다.
8. approval·task·result binding을 semantic validator로 재검사한다.
9. 변경 target만 재조회하고 error·regression을 확인한다.

### Effect class

| `effect_class` | 실행 |
|---|---|
| `READ_ONLY` | bounded read. side effect 금지 |
| `IDEMPOTENT_MUTATION` | idempotency key와 같은 ledger record 필요 |
| `APPROVAL_REQUIRED_MUTATION` | exact request에 묶인 사용자 승인 필요 |
| `NON_RETRYABLE_MUTATION` | unknown outcome 뒤 재전송 금지 |

### Execution mode

| `execution_mode` | 실행 |
|---|---|
| `SYNCHRONOUS` | 요청 수명 안에 종료하고 task는 `NOT_APPLICABLE` |
| `LONG_RUNNING_TASK` | durable `task_id`로 start-once·status·resume |

두 축은 직교한다. `APPROVAL_REQUIRED_MUTATION + LONG_RUNNING_TASK`와 `NON_RETRYABLE_MUTATION + LONG_RUNNING_TASK`는 승인·retry 규칙을 유지한다. automatic approval은 금지한다. unsafe retry는 `UNSAFE_RETRY_BLOCKED`로 끝내고 `recover`에서 현재 상태를 reconcile한다.

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

Base adapter pin, Manifest·Schema·semantic validator, project identity, engine version, tool adoption, transport와 catalog를 검증한다. 하나라도 불일치하면 mutation으로 진행하지 않는다.

### `observe`

필요한 Scene·Node·Resource·setting·log·runtime 상태만 bounded output으로 읽는다.

### `mutate`

승인과 `effect_class`를 충족한 typed action만 실행한다. `execution_mode`가 장기 작업이면 initiating action을 한 번만 보내고 durable task를 사용한다. 가능한 경우 EditorUndoRedoManager transaction과 복구 경로를 기록한다.

### `validate`

import·parse·build·Scene run·project test·export 중 Manifest에 등록된 capability만 실행한다. project test runner는 catalog에 정확히 하나 존재하고 `TEST_RESULT` evidence를 선언해야 한다. Evidence `kind`와 `state`를 Schema 허용 조합으로 제한하고 `CONTRACT_PASS`, `EXECUTION_PASS`, `RUNTIME_PASS`, `ENGINE_INPUT_PASS`, `PHYSICAL_INPUT_PASS`, `HUMAN_PASS`를 분리한다.

### `resume`

기존 `operation_id`와 `task_id`를 조회한다. initiating action을 다시 보내지 않는다. terminal result의 project·capability·operation·task·result hash binding을 검사한다.

### `recover`

identity, process, endpoint, catalog, ledger와 target state를 다시 관찰한 뒤 완료·실패·pending·stale·rollback 가능성을 분리한다.

## Output

```yaml
mode:
base_adapter_commit:
project_fingerprint:
capability_id:
effect_class:
execution_mode:
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

- Base adapter 검증 없이 공용 계약·Schema를 프로젝트 상대경로로 추정
- 공용 계약 본문 또는 semantic validator를 프로젝트 adapter에 복제
- port-only target selection
- tool source·version·telemetry·external data·제거 정책 미검증
- duplicate capability ID 또는 잘못된 project test runner
- arbitrary script 또는 shell execution 기본 허용
- automatic approval
- approval binding 불일치
- unsafe retry
- task pending 중 duplicate start
- task/result hash binding 불일치
- evidence kind/state 왜곡
- engine input을 physical input으로 보고
- test framework 미등록 상태를 PASS로 보고
- contract 파일 존재를 runtime·human PASS로 보고