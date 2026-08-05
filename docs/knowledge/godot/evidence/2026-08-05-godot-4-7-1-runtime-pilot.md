# Godot 4.7.1 Runtime Pilot Evidence

## 판정

업로드된 Godot Linux editor binary와 격리 Pilot에서 CLI_HEADLESS 및 EditorPlugin 생명주기를 실제 실행했다. 원본 네 프로젝트는 `project.godot`만 제공됐으므로 recovery mode 설정 파싱만 확인했고 게임 runtime은 모두 `NOT_RUN`이다.

이번 재검토에서는 closed request Schema, catalog 변조 차단, 승인 만료·single-use, mutation 전 ledger 기록, task preflight `NOT_STARTED`까지 runtime으로 검증했다. 실제 Scene 편집 bridge·network MCP·Undo/Redo·runtime debugger는 구현하지 않았으므로 production adapter 상태는 `NOT_READY`다.

## 실행 입력

- Captured at: `2026-08-05T09:16:36+09:00`
- Engine: `4.7.1.stable.official.a13da4feb`
- Archive SHA-256: `c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba`
- Executable SHA-256: `32f8d7596c4b41185512b1c49d69f2da3be018fd784a53e349fa92a98a97bcde`
- Root warning suppression used only for clean logs: `GODOT_SILENCE_ROOT_WARNING=1`
- Pilot fingerprint: `fadbb98bd91210be3b1c0eacb173558732f49a8c75aa9f935c74d5d5a6d57221`
- Runtime-verified catalog SHA-256: `f364c08e811c77c311bb977695cde7f8a5a56f0316e559c5f4d09b0da074ed31`
- Shared evidence commands use `$GODOT_BIN`, `$PILOT`, `$CONFIG_SAMPLE` placeholders and contain no machine absolute path.

## 실제 검증한 Pilot 경로

```text
doctor → OK
status → OK
catalog.compact → OK
scene.inspect → OK
tampered catalog → CATALOG_STALE
state.write_marker without approval → APPROVAL_REQUIRED
state.write_marker approved → OK
state.write_marker replay → IDEMPOTENT_REPLAY
expired approval → APPROVAL_EXPIRED
first use of single-use token → OK
second operation with same token → APPROVAL_TOKEN_REUSED
extra request field → REQUEST_SCHEMA_INVALID
task.start without request → REQUEST_INVALID + NOT_STARTED
task.start without approval → APPROVAL_REQUIRED + NOT_STARTED
task.start approved → TASK_PENDING
task.start duplicate → same task_id
task.resume wrong task_id → TASK_RESULT_STALE
task.resume matching task_id → COMPLETED
headless editor → base_live_editor_pilot loaded
```

Captured result codes in order:

```text
OK, OK, OK, OK, CATALOG_STALE, APPROVAL_REQUIRED,
OK, IDEMPOTENT_REPLAY, APPROVAL_EXPIRED, OK,
APPROVAL_TOKEN_REUSED, REQUEST_SCHEMA_INVALID,
REQUEST_INVALID, APPROVAL_REQUIRED, TASK_PENDING,
TASK_PENDING, TASK_RESULT_STALE, OK
```

모든 write는 `examples/godot-live-editor-pilot/artifacts/` 아래로 제한했다. EditorPlugin marker는 `network_listener_enabled=false`를 기록한다. mutation은 durable `STARTED` ledger와 approval token consumption을 먼저 기록하고, state write 결과를 `COMPLETED` 또는 `FAILED`로 닫는다. task가 생성되기 전 실패는 가짜 task ID 대신 `NOT_STARTED`를 사용한다.

## 현업·벤치마크 비교

대표적인 Godot MCP 구현은 대체로 외부 MCP stdio server와 Godot EditorPlugin의 loopback TCP/WebSocket을 연결하고, screenshot·runtime input을 위해 별도 Autoload를 추가한다. 이 방식은 실제 Scene 조작 범위가 넓지만 project 안에 listener와 runtime bridge를 설치하므로 인증·메인 스레드·Undo/Redo·cleanup 경계가 중요하다.

이번 Base 구조는 다음을 더 엄격하게 둔다.

- transport 기본 off와 loopback-only 정책
- capability별 closed arguments Schema
- project fingerprint·catalog hash 확인
- exact request에 묶인 만료·single-use approval
- idempotency·task ledger와 재전송 금지
- engine input·physical input·human evidence 분리

반대로 이번 Pilot은 다음 현업 기능을 아직 증명하지 않았다.

- Editor main-thread request queue
- `EditorUndoRedoManager` transaction
- save·dirty Scene 상태와 import refresh
- bounded TCP/WebSocket framing과 session authentication
- `EditorDebuggerPlugin`·`EngineDebugger` runtime bridge
- screenshot·runtime input·실제 게임 project test

따라서 현재 산출물은 production MCP server가 아니라, production adapter가 지켜야 할 계약과 실행 가능한 안전 fixture다.

## 업로드된 설정 파일 호환성

| 프로젝트 | SHA-256 | 설정 파싱 | 의존성 | 관찰된 누락 참조 | 게임 runtime |
|---|---|---|---|---|---|
| Blacksmith | `d60e5f98299f75a32455124a6665cc6905fe2bc52c1a96a86ed937aa19f1fcc4` | EXECUTION_PASS | NO_MISSING_DEPENDENCY_REPORTED | none reported during recovery-mode configuration startup | NOT_RUN |
| urban-legend | `efb0b9f595d142cca20d92a0555ecb793a1e440decd72dd24dbdb77c23319322` | EXECUTION_PASS | NOT_PROVIDED | `res://scripts/core/urban_legend_state.gd`, `res://scripts/core/game_state.gd` | NOT_RUN |
| 새 게임 프로젝트 | `e93eb65107aa63bf1a8602459a79fec74dbf381c6e02d7d7dcdd558cb8c513fa` | EXECUTION_PASS | NO_MISSING_DEPENDENCY_REPORTED | none reported during recovery-mode configuration startup | NOT_RUN |
| 십보강호: 전투 POC | `f1061e65d87e24dc679fae5da538537086852b155ea7d6a114088e385de21801` | EXECUTION_PASS | NOT_PROVIDED | `res://addons/godot_ai/runtime/game_helper.gd`, `res://addons/godot_ai/plugin.cfg` | NOT_RUN |

`urban-legend`와 `십보강호: 전투 POC`는 recovery mode 설정 시작 자체는 exit code 0이었지만, 제공되지 않은 autoload·addon을 명시적으로 보고했다. `Blacksmith`와 `새 게임 프로젝트`는 이 단계에서 누락 오류를 출력하지 않았으나 main Scene과 전체 프로젝트 파일이 없으므로 runtime 성공으로 해석하지 않는다.

## 증거 경계

```yaml
uploaded_engine_binary: EXECUTION_PASS
isolated_cli_headless_fixture: RUNTIME_PASS
isolated_editor_plugin_load: RUNTIME_PASS
runtime_catalog_freshness_gate: RUNTIME_PASS
closed_request_schema: RUNTIME_PASS
approval_expiration_and_single_use: RUNTIME_PASS
atomic_operation_ledger: RUNTIME_PASS
long_task_preflight_boundary: RUNTIME_PASS
original_project_configs_parse: EXECUTION_PASS
original_project_scenes_and_scripts: NOT_PROVIDED
original_projects_runtime: NOT_RUN
network_mcp_transport: NOT_IMPLEMENTED
editor_main_thread_mutation: NOT_IMPLEMENTED
editor_undo_redo_transaction: NOT_IMPLEMENTED
runtime_debugger_bridge: NOT_IMPLEMENTED
project_test_framework: NOT_CONFIGURED
physical_input_validation: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

전체 captured envelope와 exact placeholder command는 `examples/godot-live-editor-pilot/RUNTIME_EVIDENCE.json`에 저장한다. GitHub CI는 업로드 바이너리를 재실행하지 않고 캡처된 envelope·Manifest·fixture 구조를 현재 Base Schema로 검증한다.
