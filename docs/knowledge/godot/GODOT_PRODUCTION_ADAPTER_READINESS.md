# Godot Production Adapter Readiness

## Purpose

이 문서는 정적 v2 계약, 격리 Pilot, project-local Editor transaction adapter, authenticated transport, runtime debugger와 실제 프로젝트 채택을 분리한다. Schema·validator PASS나 단일 Pilot만으로 `PRODUCTION_ADAPTER_READY`를 주장하지 않는다.

## Reference architecture

```text
project CLI or optional MCP profile
→ authenticated local process/loopback boundary
→ bounded request queue
→ EDITOR_MAIN_THREAD typed executor
→ EditorUndoRedoManager transaction
→ explicit save/import/refresh
→ atomic ledger
→ output validation and bounded evidence
```

transport handler는 `SceneTree`, `Resource`, `EditorInterface` 또는 `ProjectSettings`를 직접 변경하지 않는다. closed request를 검증해 queue에 넣고 Editor main thread가 등록 capability를 실행한다.

PR B의 in-process adapter는 external transport 이전 단계다. v2 Schema에서 `CONFIGURED` Manifest는 `DISABLED` transport를 허용하지 않으므로, listener 없는 exact local profile을 사용한다.

```yaml
transport:
  kind: PROJECT_DEFINED
  enabled: true
  bind_host: null
  endpoint_identity: in-process-editor-plugin
  access_control:
    authentication_mode: NOT_APPLICABLE
    origin_policy: NOT_APPLICABLE
    session_binding: NOT_APPLICABLE
    os_access_control: CURRENT_USER_ONLY
network_listener_enabled: false
```

`enabled: true`는 declared in-process endpoint가 활성 상태라는 뜻이며 socket·HTTP·WebSocket listener를 의미하지 않는다. `NOT_CONFIGURED` installation source는 계속 `DISABLED + enabled: false`다.

## Current PR B evidence

정적 v2 계약과 project-local adapter는 다음 상태다.

```yaml
v2_schema_validation: PASS
v2_semantic_validation: PASS
v1_mutation_authority: REJECTED
bounded_editor_request_queue: STATIC_PASS
closed_scene_inspect_and_node_rename: STATIC_PASS
editor_main_thread_precondition_recheck: STATIC_PASS
atomic_started_terminal_ledger: STATIC_PASS
physical_artifact_hashing: STATIC_PASS
ci_runtime_with_godot_bin: SKIPPED_NOT_CONFIGURED
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
real_project_pilots: NOT_RUN
physical_input_validation: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

2026-08-05 격리 Godot 4.7.1 Editor 실행에서는 다음을 실제로 확인했다.

```yaml
godot_4_7_1_editor_pilot: RUNTIME_PASS_ISOLATED_PILOT
scene_inspect: RUNTIME_PASS
node_rename_keep_dirty: RUNTIME_PASS
editor_undo: RUNTIME_PASS
node_rename_save_current_scene: RUNTIME_PASS
started_completed_ledger: RUNTIME_PASS
saved_scene_byte_sha256: RUNTIME_PASS
network_listener_disabled: RUNTIME_PASS
```

상세 실행 근거는 `docs/knowledge/godot/evidence/2026-08-05-godot-4-7-editor-transaction-pilot.md`에 기록한다. 이 결과는 격리 Pilot이며 실제 게임 프로젝트 두 곳, Windows production operation, authenticated transport, runtime debugger, physical input 또는 human usability 증거가 아니다.

## Production runtime gates

```yaml
exact_project_service_editor_identity: RUNTIME_PASS
contract_snapshot_binding: RUNTIME_PASS
typed_input_validation_before_engine_action: RUNTIME_PASS
output_schema_validation_before_success: RUNTIME_PASS
stale_state_preconditions: RUNTIME_PASS
editor_main_thread_queue: RUNTIME_PASS
editor_undo_redo_transaction: RUNTIME_PASS
save_import_refresh_boundary: RUNTIME_PASS
approval_expiration_single_use: RUNTIME_PASS
atomic_operation_ledger: RUNTIME_PASS
loopback_auth_bounded_framing: RUNTIME_PASS_OR_NOT_APPLICABLE
plugin_load_unload_cleanup: RUNTIME_PASS
runtime_debugger_bridge: RUNTIME_PASS_OR_NOT_APPLICABLE
project_behavior_tests: RUNTIME_PASS
physical_input_validation: NOT_RUN_OR_SEPARATE_EVIDENCE
human_editor_usability: HUMAN_PASS
production_adapter_ready: READY_ONLY_AFTER_ALL_APPLICABLE_PASS
```

`input_schema`와 `output_schema`는 closed object Schema이며 각각 `additionalProperties: false`를 요구한다. runtime handler는 Manifest label을 신뢰하지 않고 실행 전후에 다시 검증한다.

## Mutation ordering

1. project, service, Editor/runtime identity와 `contract_snapshot`을 검증한다.
2. expected/observed preconditions를 비교하고 `TARGET_STATE_CONFLICT`를 차단한다.
3. approval과 operation conflict를 확인한다.
4. `STARTED`, request hash와 token consumption을 원자적으로 저장한다.
5. Editor main thread에서 bounded action을 실행한다.
6. output Schema, result hash와 evidence를 검증한다.
7. `COMPLETED` 또는 `FAILED`를 원자적으로 저장한다.

`NOT_STARTED`에는 fabricated task ID가 없다. timeout은 blind replay 근거가 아니다.

## Editor transaction boundary

undoable mutation은 `EditorPlugin.get_undo_redo()` / `EditorUndoRedoManager`로 do/undo methods를 등록하고 한 번 commit한다. dirty state와 save는 별도 정책과 증거다. undo 불가능한 mutation은 `rollback_policy`, approval과 recovery path를 명시한다.

PR B는 `.tscn` 저장 후 `EditorFileSystem.update_file()`과 physical byte SHA-256을 확인한다. asset import/reimport가 필요한 형식은 아직 증명하지 않았으므로 포괄적인 import boundary PASS로 확대 해석하지 않는다.

## Transport and debugger

STDIO stdout은 protocol-only이며 diagnostics는 stderr다. local HTTP/WebSocket은 loopback, session token 또는 OAuth 2.1 인증, Origin allowlist, frame·depth·batch·connection·idle 제한이 필요하다. remote endpoint는 Base 기본 계약에서 지원하지 않는다.

runtime debugger는 opt-in `EditorDebuggerPlugin` / `EditorDebuggerSession` / `EngineDebugger` capability이며 automatic Autoload가 아니다.

## Pilot boundaries

`examples/godot-live-editor-pilot/`는 Godot 4.7.1에서 v1 typed CLI, identity, catalog, approval expiry와 single-use, idempotent replay, durable task resume, bounded writes와 no-network plugin lifecycle을 증명한다.

`examples/godot-live-editor-v2-editor-pilot/`는 materialized temporary project에서 v2 in-process Editor transaction boundary를 증명한다. checked-in source Manifest는 `NOT_CONFIGURED`이며 원본 fixture나 사용자 프로젝트를 변경하지 않는다.

다음은 아직 증명하지 않는다.

- authenticated external transport 또는 MCP mapping
- runtime debugger control
- 구조가 다른 실제 프로젝트 두 곳의 behavior tests
- Windows production operation
- physical input
- human usability

따라서 현재 production 상태는 `NOT_READY`다.
