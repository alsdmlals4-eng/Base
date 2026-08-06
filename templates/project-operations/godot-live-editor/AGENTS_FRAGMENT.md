# Historical Base live-editor adapter Pilot

```yaml
status: HISTORICAL_BASE_ADAPTER_PILOT_ONLY
active_project_authority: false
current_provider: hi-godot/godot-ai
```

이 Fragment는 2026-08-05 Base live-editor Adapter와 Pilot의 과거 계약·실행 증거를 재현할 때만 읽는다. 현재 프로젝트에 복사하거나 `AGENTS.md`에 합치거나 `addons/base_live_editor_adapter/`를 설치하는 지침이 아니다.

현재 Godot 실행 정본:

- `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- Project adapter: `.agents/skills/godot-live-editor-operations/SKILL.md`
- Project adoption state: `HIGODOT_ADOPTION_RECORD.json`

HiGodot 외 Base custom MCP, Base network Bridge, Hera 또는 다른 mutation addon을 활성 권위로 추가하지 않는다.

## 보존된 과거 Pilot 계약

아래 항목은 감사와 재현 전용이며 일반 프로젝트 채택에 사용하지 않는다.

- Historical capability source: `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Historical addon: `addons/base_live_editor_adapter/`
- Base pin authority: `skills/PROJECT_BASE_ADAPTER.json`
- Base v2 capability Schema: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Base v2 operation Schema: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Base semantic validator: `tools/validate_godot_live_editor_contract_v2.py`

```text
validate PROJECT_BASE_ADAPTER.json and snapshot
→ doctor → status → catalog --compact
→ classify manifest version
→ v1 authorization: MIGRATION_REQUIRED_V1
→ v2 Schema and semantic validation
→ exact project/service/Editor/runtime identity
→ contract_snapshot and catalog freshness
→ typed capability only
```

validated Base adapter가 고정한 repository·commit에서 과거 공용 계약·Schema·validator를 읽는다. 이 경로는 현재 HiGodot 작업을 우회하는 fallback이 아니다. 과거 Pilot에서도 automatic approval과 unsafe retry는 금지됐다.

과거 PR B addon은 configured v2 Manifest의 exact project-owned in-process Pilot profile에서만 사용됐다.

```yaml
transport:
  kind: PROJECT_DEFINED
  enabled: true
  bind_host: null
  endpoint_identity: in-process-editor-plugin
```

`enabled: true`는 과거 in-process 실행 채널을 뜻하며 네트워크 listener가 아니다. 과거 Pilot은 `scene.inspect`, `node.rename`(`KEEP_DIRTY | SAVE_CURRENT_SCENE`)만 허용했다. 서버, MCP, socket, remote endpoint, background thread 또는 Autoload는 포함하지 않았다.

과거 mutation은 full approval binding·expiry와 expected/observed revision·hash·dirty state·Scene path를 같은 Editor frame에서 다시 비교했다. STARTED ledger, `EditorUndoRedoManager`, save/filesystem update, physical byte hash, typed output/evidence와 terminal ledger가 완료되기 전에는 성공을 보고하지 않았다.

## Fail-closed boundary

- `tools/godot_editor_adapter_materialization.py`는 보존된 historical Pilot materializer 호출에서만 작동한다.
- 일반 코드나 프로젝트 채택 경로의 호출은 `BASE_ADAPTER_ACTIVE_ADOPTION_FORBIDDEN`으로 실패해야 한다.
- Pilot 결과는 현재 HiGodot 설치·연결·runtime·regression·production readiness를 증명하지 않는다.
- addon 시작 문제가 있어도 두 번째 addon을 활성화하지 않는다. 현재 HiGodot 복구·rollback 절차를 사용한다.

보고:

```text
Historical pilot only · provider authority=false · current provider=hi-godot/godot-ai
base=<commit> · operation=<id> · code=<stable-code> · evidence=<paths> · current-runtime=NOT_RUN
```
