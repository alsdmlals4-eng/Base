# Godot live-editor adapter

프로젝트가 Godot live Editor 자동화를 실제 구성한 경우에만 사용한다.

- Project capability source: `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Project adapter: `.agents/skills/godot-live-editor-operations/SKILL.md`
- Network-disabled addon: `addons/base_live_editor_adapter/`
- Base pin authority: `skills/PROJECT_BASE_ADAPTER.json`
- Base v2 capability Schema: `schemas/godot-live-editor-capability-manifest-v2.schema.json`
- Base v2 operation Schema: `schemas/godot-live-editor-operation-envelope-v2.schema.json`
- Base semantic validator: `tools/validate_godot_live_editor_contract_v2.py`

공용 계약·Schema·validator를 프로젝트 상대경로로 추정하거나 복제하지 않는다. validated Base adapter가 고정한 repository·commit에서 읽는다.

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

Base adapter 실패, Manifest 없음, `NOT_CONFIGURED`, stale, identity/snapshot mismatch, undeclared capability이면 engine action을 중단한다. automatic approval과 unsafe retry는 금지한다.

PR B addon은 configured v2 Manifest의 exact project-owned in-process profile에서만 활성화된다.

```yaml
transport:
  kind: PROJECT_DEFINED
  enabled: true
  bind_host: null
  endpoint_identity: in-process-editor-plugin
```

`enabled: true`는 in-process 실행 채널을 뜻하며 네트워크 listener를 켜지 않는다. 이미 검증된 envelope를 in-process로만 받고 `scene.inspect`, `node.rename`(`KEEP_DIRTY | SAVE_CURRENT_SCENE`) 외 capability는 거부한다. 서버, MCP, socket, remote endpoint, background thread 또는 Autoload는 포함하지 않는다.

mutation은 full approval binding·expiry와 expected/observed revision·hash·dirty state·Scene path를 같은 Editor frame에서 다시 비교한다. 불일치는 `TARGET_STATE_CONFLICT` 또는 승인 오류다. STARTED ledger 전에 engine mutation을 하지 않고, `EditorUndoRedoManager` transaction·save/filesystem update·physical byte hash·typed output/evidence·terminal ledger가 끝나기 전에는 성공을 보고하지 않는다.

request queue와 completed-result 보관은 각각 64개, 실행은 Editor frame당 하나, 파일 hash는 64 KiB streaming으로 제한한다. Scene hash 비용은 파일 크기에 선형이므로 실제 프로젝트 Pilot 없이 효율성을 PASS로 보고하지 않는다.

addon 시작 문제가 있으면 Godot `--recovery-mode`로 비활성화하거나 제거하고 새 Editor instance ID와 필요한 승인을 발급한다. 이 addon만으로 `PRODUCTION_ADAPTER_READY`를 주장하지 않는다.

보고:

```text
Connected: <project> · godot=<version> · state=<state> · capabilities=<count>
base=<commit> · operation=<id> · task=<id|none> · code=<stable-code> · evidence=<paths>
```
