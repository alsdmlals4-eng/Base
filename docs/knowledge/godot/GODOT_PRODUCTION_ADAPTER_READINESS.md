# Godot Production Adapter Readiness

## Purpose

이 문서는 정적 v2 계약, 격리 Pilot, production Editor adapter와 실제 프로젝트 채택을 분리한다. Schema·validator PASS나 EditorPlugin load marker만으로 `PRODUCTION_ADAPTER_READY`를 주장하지 않는다.

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

## Static v2 prerequisite

production 구현 전 정적 게이트는 다음 상태여야 한다.

```yaml
v2_schema_validation: PASS
v2_semantic_validation: PASS
v1_mutation_authority: REJECTED
editor_main_thread_queue: NOT_IMPLEMENTED
editor_undo_redo_transaction: NOT_IMPLEMENTED
production_adapter_ready: NOT_READY
```

v1 증거는 `V1_AUDIT_ONLY`로 읽을 수 있지만 v2 mutation 권한이 아니다. `MIGRATION_REQUIRED_V1`을 우회하지 않는다.

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

## Transport and debugger

STDIO stdout은 protocol-only이며 diagnostics는 stderr다. local HTTP/WebSocket은 loopback, session token 또는 OAuth 2.1 인증, Origin allowlist, frame·depth·batch·connection·idle 제한이 필요하다. remote endpoint는 Base 기본 계약에서 지원하지 않는다.

runtime debugger는 opt-in `EditorDebuggerPlugin` / `EditorDebuggerSession` / `EngineDebugger` capability이며 automatic Autoload가 아니다.

## Pilot boundary

`examples/godot-live-editor-pilot/`는 Godot 4.7.1에서 typed CLI, identity, catalog, approval expiry와 single-use, idempotent replay, durable task resume, bounded writes와 no-network plugin lifecycle만 증명한다.

다음은 아직 증명하지 않는다.

- production Editor main-thread mutation
- EditorUndoRedoManager transaction
- authenticated transport
- runtime debugger control
- 실제 프로젝트 behavior tests
- Windows production operation
- physical input
- human usability

따라서 현재 production 상태는 `NOT_READY`다.
