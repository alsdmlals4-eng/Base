# Godot Production Adapter Readiness

> 상태: `HISTORICAL_BASE_ADAPTER_REFERENCE_ONLY`
>
> 이 문서는 Base custom live-editor adapter의 2026-08-05 readiness와 Pilot 증거를 보존하는 역사적 reference다. **현재 Godot persistent authoring 실행 경로가 아니다.** 현재 writer/authoring 권위와 HiGodot·GUT·Hera 역할은 `HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다. 아래 `NOT_READY`, Pilot 수치와 production gate는 당시 Base adapter의 증거 ceiling을 기록하며 현재 도구의 readiness로 승격하지 않는다.

## Purpose

이 문서는 당시 정적 v2 계약, 격리 Pilot, project-local Editor transaction adapter, authenticated transport, runtime debugger와 실제 프로젝트 채택을 분리한 기록이다. Schema·validator PASS나 단일 Pilot만으로 `PRODUCTION_ADAPTER_READY`를 주장하지 않는다는 교훈을 보존한다.

## Historical reference architecture

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

historical transport handler는 `SceneTree`, `Resource`, `EditorInterface` 또는 `ProjectSettings`를 직접 변경하지 않는다. closed request를 검증해 queue에 넣고 Editor main thread가 등록 capability를 실행하도록 설계했다.

PR B의 in-process adapter는 external transport 이전 단계였다. v2 Schema에서 `CONFIGURED` Manifest는 `DISABLED` transport를 허용하지 않았으므로, listener 없는 exact local profile을 사용했다.

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

`enabled: true`는 declared in-process endpoint가 활성 상태라는 뜻이며 socket·HTTP·WebSocket listener를 의미하지 않았다. `NOT_CONFIGURED` installation source는 `DISABLED + enabled: false`였다.

## Historical PR B evidence

정적 v2 계약과 project-local adapter에 기록된 상태는 다음과 같다.

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

## Historical post-merge adversarial hardening

PR #166은 PR B 병합 뒤 실제 실행 경계를 다시 공격했다. 정적 CI만 통과한 첫 hardening Runtime은 Pilot script의 동적 타입 추론 오류로 Plugin을 로드하지 못했고, 이를 명시적 타입과 Runtime 회귀 테스트로 수정했다.

강화된 격리 Godot 4.7.1 실행에서는 다음을 추가로 확인했다.

```yaml
canonical_request_hash_recompute: RUNTIME_PASS
full_approval_binding_and_expiry: STATIC_AND_RUNTIME_PATH_PASS
canonical_result_hash: RUNTIME_PASS
stale_request_rejected_without_mutation: RUNTIME_PASS
stale_request_ledger_absent: RUNTIME_PASS
output_type_and_save_policy_validation: RUNTIME_PASS
queue_capacity_64: RUNTIME_PASS
request_65_queue_full: RUNTIME_PASS
batch_64_completed: 64
batch_64_elapsed_usec_median: 444301
batch_64_throughput_ops_per_second_median: 144.0
network_listener_disabled: RUNTIME_PASS
```

이 성능 수치는 minimal Scene, Linux x86_64, headless Editor, frame당 한 요청, evidence 생성을 포함한 격리 수치다. `.tscn` hash 비용은 파일 크기에 선형이므로 실제 대형 프로젝트 성능으로 일반화하지 않는다. 반복 process soak 중 Editor 초기화 전 stall도 관찰되어 process-start soak 안정성은 `BLOCKED_ENVIRONMENT`다.

상세 근거와 한계는 `docs/knowledge/godot/evidence/2026-08-05-godot-editor-transaction-hardening-pilot.md`에 기록한다.

## Historical Base C0 multi-project Pilot runner

Base C0는 실제 프로젝트 source checkout을 직접 변경하지 않고 disposable workspace에서만 legacy authority disable, main Scene read-only inspect, runner-owned scratch Scene rename·Undo·save와 physical byte hash 검증을 수행하는 재사용 runner를 제공했다.

```yaml
multi_project_pilot_runner: STATIC_PASS
base_c0_descriptor_schema: STATIC_PASS
base_c0_source_inventory: STATIC_PASS
base_c0_disposable_workspace: STATIC_PASS
base_c0_legacy_copy_transform: STATIC_PASS
base_c0_scratch_only_editor_wrapper: STATIC_PASS
base_c0_physical_evidence_verifier: STATIC_PASS
base_c0_reusable_workflow: STATIC_PASS
real_project_pilots: NOT_RUN
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
windows_production_operation: NOT_RUN
physical_input_validation: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

`STATIC_PASS`는 Base C0 구현과 단위·계약 검증 상태이며 실제 게임 저장소 Runtime PASS가 아니다. 프로젝트별 증거는 Switchy Express clean Pilot 이후 독립 Draft PR과 post-merge push artifact에서 수집하고 Base C1에서 물리적으로 재검증하도록 설계됐다.

## Historical Base adapter runtime gates

아래 gate는 historical adapter가 production-ready를 주장하려면 필요했던 기준이다. 현재 HiGodot/GUT/Hera의 실제 지원 또는 PASS 상태를 나타내지 않는다.

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

`input_schema`와 `output_schema`는 closed object Schema이며 각각 `additionalProperties: false`를 요구한다. historical runtime handler는 Manifest label을 신뢰하지 않고 실행 전후에 다시 검증하도록 설계됐다.

## Mutation ordering

historical adapter는 다음 순서를 요구했다.

1. project, service, Editor/runtime identity와 `contract_snapshot`을 검증한다.
2. expected/observed preconditions를 비교하고 `TARGET_STATE_CONFLICT`를 차단한다.
3. approval과 operation conflict를 확인한다.
4. `STARTED`, request hash와 token consumption을 원자적으로 저장한다.
5. Editor main thread에서 bounded action을 실행한다.
6. output Schema, result hash와 evidence를 검증한다.
7. `COMPLETED` 또는 `FAILED`를 원자적으로 저장한다.

`NOT_STARTED`에는 fabricated task ID가 없다. timeout은 blind replay 근거가 아니다.

## Editor transaction boundary

undoable mutation은 `EditorPlugin.get_undo_redo()` / `EditorUndoRedoManager`로 do/undo methods를 등록하고 한 번 commit하도록 설계했다. dirty state와 save는 별도 정책과 증거였다. undo 불가능한 mutation은 `rollback_policy`, approval과 recovery path를 명시했다.

PR B는 `.tscn` 저장 후 `EditorFileSystem.update_file()`과 physical byte SHA-256을 확인했다. asset import/reimport가 필요한 형식은 증명하지 않았으므로 포괄적인 import boundary PASS로 확대 해석하지 않는다.

## Transport and debugger

historical STDIO stdout은 protocol-only이며 diagnostics는 stderr였다. local HTTP/WebSocket은 loopback, session token 또는 OAuth 2.1 인증, Origin allowlist, frame·depth·batch·connection·idle 제한을 요구했다. remote endpoint는 당시 Base 기본 계약에서 지원하지 않았다.

runtime debugger는 opt-in `EditorDebuggerPlugin` / `EditorDebuggerSession` / `EngineDebugger` capability이며 automatic Autoload가 아니었다.

## Pilot boundaries

`examples/godot-live-editor-pilot/`는 Godot 4.7.1에서 v1 typed CLI, identity, catalog, approval expiry와 single-use, idempotent replay, durable task resume, bounded writes와 no-network plugin lifecycle을 증명했다.

`examples/godot-live-editor-v2-editor-pilot/`는 materialized temporary project에서 v2 in-process Editor transaction boundary를 증명했다. checked-in source Manifest는 `NOT_CONFIGURED`이며 원본 fixture나 사용자 프로젝트를 변경하지 않았다.

다음은 historical Base adapter에서 증명하지 못했다.

- authenticated external transport 또는 MCP mapping
- runtime debugger control
- 구조가 다른 실제 프로젝트 두 곳의 behavior tests
- Windows production operation
- process-start soak stability
- physical input
- human usability

따라서 historical Base adapter의 마지막 기록 상태는 `NOT_READY`다. 이 상태를 현재 Godot authoring/toolchain 상태로 해석하거나, 이 문서를 근거로 legacy adapter를 재활성화하지 않는다.
