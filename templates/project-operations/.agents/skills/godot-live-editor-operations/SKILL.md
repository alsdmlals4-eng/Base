---
name: godot-live-editor-operations
description: Use in an installed Godot project when registered CLI, EditorPlugin, or runtime-debugger capabilities must be bootstrapped, observed, mutated, validated, resumed, or recovered.
---

# Godot Live Editor Operations

## 책임

이 파일은 프로젝트에 설치되는 얇은 adapter다. 재사용 계약은 `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`, 보안·복구는 `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`, 실제 capability는 `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`이 책임진다.

Base active Skill을 대체하거나 새 광역 책임을 만들지 않는다.

## Modes

`bootstrap` → `observe` → `mutate` → `validate` → `resume` → `recover`

## Manifest gate

다음 중 하나면 engine action 전에 중단한다.

- Manifest 없음·JSON/Schema 오류
- `configuration_state: NOT_CONFIGURED`
- normalized project path, `project.godot` SHA-256 또는 project fingerprint 불일치
- adapter·contract version 불일치
- catalog `STALE / MISMATCH`
- 요청 capability 미등록
- 현재 engine state가 `unsupported_states`에 포함됨

부트스트랩은 `doctor → status → catalog --compact` 순서다. port 또는 PID만으로 target을 선택하지 않는다.

## Operation contract

1. 한 개의 등록 capability와 arguments Schema를 선택한다.
2. operation class를 확인한다.
3. exact normalized request와 request hash를 만든다.
4. approval·idempotency·ledger·timeout 조건을 확인한다.
5. action을 한 번 시작한다.
6. compact operation envelope와 evidence path를 기록한다.
7. 변경 target만 재조회하고 error·regression을 확인한다.

| class | 실행 |
|---|---|
| `READ_ONLY` | bounded read. side effect 금지 |
| `IDEMPOTENT_MUTATION` | idempotency key와 같은 ledger record 필요 |
| `APPROVAL_REQUIRED_MUTATION` | exact request에 묶인 사용자 승인 필요 |
| `NON_RETRYABLE_MUTATION` | unknown outcome 뒤 재전송 금지 |
| `LONG_RUNNING_TASK` | durable `task_id`로 status/resume |

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

Manifest·Schema·project identity·engine version·transport·catalog를 검증한다. 하나라도 불일치하면 mutation으로 진행하지 않는다.

### `observe`

필요한 Scene·Node·Resource·setting·log·runtime 상태만 bounded output으로 읽는다.

### `mutate`

승인과 operation class를 충족한 typed action만 실행한다. 가능한 경우 EditorUndoRedoManager transaction과 복구 경로를 기록한다.

### `validate`

import·parse·build·Scene run·project test·export 중 Manifest에 등록된 capability만 실행한다. `CONTRACT_PASS`, `EXECUTION_PASS`, `RUNTIME_PASS`, `ENGINE_INPUT_PASS`, `PHYSICAL_INPUT_PASS`, `HUMAN_PASS`를 분리한다.

### `resume`

기존 `operation_id`와 `task_id`를 조회한다. initiating action을 다시 보내지 않는다.

### `recover`

identity, process, endpoint, catalog, ledger와 target state를 다시 관찰한 뒤 완료·실패·pending·stale·rollback 가능성을 분리한다.

## Output

```yaml
mode:
project_fingerprint:
capability_id:
operation_class:
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

- port-only target selection
- arbitrary script 또는 shell execution 기본 허용
- automatic approval
- unsafe retry
- task pending 중 duplicate start
- engine input을 physical input으로 보고
- test framework 미등록 상태를 PASS로 보고
- contract 파일 존재를 runtime·human PASS로 보고
