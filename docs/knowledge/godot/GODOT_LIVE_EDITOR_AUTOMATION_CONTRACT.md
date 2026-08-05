# Godot Live Editor Automation Contract

## 목적과 권한

이 문서는 AI 작업자가 Godot 프로젝트의 CLI, 실행 중 Editor, Scene, Resource, ProjectSettings, 테스트, export와 runtime 상태를 안전하게 관찰·변경·검증하기 위한 공용 계약이다. 실제 명령과 EditorPlugin 구현은 각 프로젝트가 소유하며, Base는 실행 안전·증거·라우팅 경계만 제공한다.

프로젝트가 `templates/project-operations/GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`을 설치하고 실제 값으로 구성하지 않았다면 상태는 `NOT_CONFIGURED`다. 파일 존재만으로 Editor 연결, 명령 지원, 테스트 러너, export, screenshot 또는 runtime 준비를 주장하지 않는다.

## 실행 경로

### CLI_HEADLESS

Godot 실행 파일을 직접 사용해 import, headless 검사, 특정 Scene 실행, 등록된 프로젝트 도구, build와 export를 수행한다. 명령, 엔진 범위, 입력 파일, side effect, timeout과 증거 출력은 Capability Manifest에 명시한다.

### EDITOR_PLUGIN

Scene·Node·Resource·Inspector·ProjectSettings 변경은 프로젝트가 등록한 typed action만 실행한다. 실행 흐름은 다음과 같다.

```text
typed request
→ identity와 catalog freshness 확인
→ operation class와 approval 확인
→ 직렬화된 Editor main-thread 실행
→ 가능한 경우 EditorUndoRedoManager transaction
→ save·import·refresh 경계
→ compact operation envelope
```

전송 방식은 local HTTP, named pipe, stdio bridge 또는 프로젝트가 승인한 loopback 방식일 수 있다. 전송 구현은 공통 identity·approval·retry·evidence 규칙을 약화할 수 없다.

### RUNTIME_DEBUGGER

Runtime 관찰은 EditorDebuggerPlugin, EditorDebuggerSession, EngineDebugger 메시지, 프로젝트 debug API 또는 bounded log를 사용한다. 관찰 명령은 기본 `READ_ONLY`다. Runtime mutation은 Capability Manifest에 별도 action과 승인 등급이 선언된 경우만 허용한다.

## 부트스트랩

모든 엔진 작업은 다음 순서를 사용한다.

```text
doctor → status → catalog --compact
→ normalized project path 확인
→ project.godot SHA-256과 project fingerprint 확인
→ adapter·contract version과 catalog freshness 확인
→ capability와 operation class 확인
```

한 줄 결과 형식:

```text
Connected: <project> · godot=<version> · state=<state> · capabilities=<count> · fingerprint=<short>
```

`doctor`는 실행 파일·프로젝트 파일·Manifest·Schema·adapter를 검사한다. `status`는 선택된 프로젝트, process, Editor/runtime 상태와 transient endpoint를 보여준다. `catalog --compact`는 현재 프로젝트가 실제 등록한 action만 작은 payload로 반환한다.

## 프로젝트 정체성

정체성의 권위는 다음 조합이다.

```text
normalized project path
+ project.godot SHA-256
+ project fingerprint
```

port, PID, window title, 폴더 이름 substring은 임시 힌트다. 여러 selector가 주어지면 모두 같은 프로젝트를 가리켜야 한다. 불일치·모호성·재사용된 endpoint는 mutation 전에 `PROJECT_IDENTITY_MISMATCH`로 실패한다.

## Capability Manifest

각 capability는 다음을 선언한다.

- `capability_id`와 짧은 설명
- `CLI_HEADLESS / EDITOR_PLUGIN / RUNTIME_DEBUGGER`
- `READ_ONLY / IDEMPOTENT_MUTATION / APPROVAL_REQUIRED_MUTATION / NON_RETRYABLE_MUTATION / LONG_RUNNING_TASK`
- arguments JSON Schema
- idempotency key와 approval 필요 여부
- timeout 뒤 상태 판정
- 자동 retry 허용 여부와 operation ledger 필요 여부
- evidence output과 unsupported engine state

Manifest에 없는 action은 `CAPABILITY_NOT_DECLARED`다. catalog가 오래됐거나 source hash가 다르면 `CATALOG_STALE`, adapter와 contract version이 맞지 않으면 `ADAPTER_VERSION_MISMATCH`다.

## 작업 등급

| 등급 | 기본 규칙 |
|---|---|
| `READ_ONLY` | side effect가 없어야 하며 bounded output만 반환한다. |
| `IDEMPOTENT_MUTATION` | 동일 idempotency key가 같은 결과를 가리킴이 입증돼야 한다. |
| `APPROVAL_REQUIRED_MUTATION` | exact normalized request에 묶인 사용자 승인이 필요하다. |
| `NON_RETRYABLE_MUTATION` | 자동 retry 금지. unknown outcome은 현재 상태를 재조회해 reconcile한다. |
| `LONG_RUNNING_TASK` | durable `task_id`와 operation ledger를 사용해 start-once·resume한다. |

approval이 필요한데 승인 token이 없으면 `APPROVAL_REQUIRED`, token의 프로젝트·action·arguments·request hash·등급이 다르면 `APPROVAL_TOKEN_MISMATCH`다. timeout 뒤 안전이 증명되지 않은 재전송은 `UNSAFE_RETRY_BLOCKED`다.

## 요청과 결과

모든 호출은 `schemas/godot-live-editor-operation-envelope-v1.schema.json`을 따른다. AI는 바뀔 수 있는 message 문자열이 아니라 stable `code`로 분기한다.

```yaml
operation_id:
project_fingerprint:
capability_id:
operation_class:
request_hash:
approval:
task:
result:
  success:
  code:
  message:
  data:
  evidence:
```

관련 read 또는 mutation은 한 action으로 batch할 수 있지만, 다른 approval 등급이나 rollback 경계를 한 batch로 숨기지 않는다. Scene tree·Resource·log·screenshot 응답은 필요한 field와 line 수만 반환한다.

## 장기 작업

import, build, export, project test 또는 capture가 요청 수명보다 길 수 있으면 시작 직후 durable `task_id`를 만든다.

```text
start once
→ operation_id·task_id·project fingerprint 저장
→ RUNNING 또는 TASK_PENDING 반환
→ status/resume가 같은 record를 조회
→ 원 작업이 존재할 수 있으면 새 작업 금지
→ final result를 project·capability·operation·task에 bind
```

`TASK_PENDING`은 실패나 Editor 정지를 의미하지 않는다. stale result, 다른 프로젝트 결과 또는 다른 operation 결과는 `TASK_RESULT_STALE`다.

## 검증 루프

기본 Light loop:

1. 목표와 변경 범위를 한 문장으로 고정한다.
2. compact read로 필요한 현재 상태만 관찰한다.
3. 등록된 action 한 개 또는 같은 rollback 경계의 batch를 실행한다.
4. import·compile·engine state 또는 task 결과를 확인한다.
5. error log를 bounded read로 확인한다.
6. 변경한 Scene·Node·Resource·setting만 다시 읽는다.
7. 실패 원인을 수정하고 같은 증거 경계를 재검증한다.
8. operation ID, exact action, 결과 code와 evidence path를 보고한다.

중요 변경은 이 루프 뒤 적대적 검토와 인접 regression을 추가한다.

## 테스트 경계

Godot 엔진 자체 테스트 옵션과 게임 프로젝트 테스트는 동일하지 않다. 프로젝트의 test framework와 runner capability가 Manifest에 등록되지 않았다면 `PROJECT_TEST_FRAMEWORK_NOT_CONFIGURED`다. 테스트 파일이나 명령 이름만으로 project test PASS를 주장하지 않는다.

## 입력·화면·사람 증거

증거 상태를 분리한다.

- `CONTRACT_PASS`: Schema와 정적 계약이 유효함
- `EXECUTION_PASS`: 명시한 환경에서 선언된 action이 종료 성공함
- `RUNTIME_PASS`: 대상 runtime 동작을 관찰함
- `ENGINE_INPUT_PASS`: Godot 내부 input dispatch를 관찰함
- `PHYSICAL_INPUT_PASS`: 실제 OS/window 입력을 별도 관찰함
- `HUMAN_PASS`: 이름 있는 사람 검수를 수행함

Godot 내부 input만 확인했으면 물리 입력 기준은 `PHYSICAL_INPUT_EVIDENCE_BLOCKED` 또는 `NOT_RUN`이다. screenshot은 지정 viewport·frame·platform의 렌더만 증명하며 접근성·성능·물리 click·사람 이해도를 증명하지 않는다. `BLOCKED_ENVIRONMENT`와 `HUMAN_NOT_RUN`을 PASS로 승격하지 않는다.

## 기존 Base 책임 연결

- 설치·Manifest·구형 adapter 감사: `managing-game-project-operating-system`
- 재현·Scene/Node/Signal·runtime 원인 격리: `diagnosing-game-engine-runtime-failures`
- static·runtime·regression 증거: `reviewing-and-validating-project-changes`
- UI·screenshot·입력 증거: `auditing-and-refining-ui-art`
- task checkpoint·resume: `maintaining-long-running-task-continuity`
- contract·catalog·Schema drift: `auditing-canonical-reference-freshness`
- 반복된 프로젝트 교훈의 Skill 경계 판정: `evolving-project-discipline-skills`

프로젝트 adapter `godot-live-editor-operations`는 이 책임을 호출하는 설치 Template이며 Base active Skill Registry에 추가하지 않는다.

## 실패 보고

```yaml
status: PASS | FAIL | NOT_CONFIGURED | BLOCKED_ENVIRONMENT
project_identity:
capability:
operation_id:
task_id:
stable_code:
observed_state:
changed_targets:
evidence:
rollback_or_recovery:
unverified:
```
