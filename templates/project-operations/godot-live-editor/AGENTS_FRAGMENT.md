# Godot live-editor adapter

프로젝트가 Godot live Editor 자동화를 실제 구성한 경우에만 사용한다.

- Project capability source: `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Project adapter: `.agents/skills/godot-live-editor-operations/SKILL.md`
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

mutation은 expected/observed revision·hash·dirty state·Scene path를 비교한다. 불일치는 `TARGET_STATE_CONFLICT`다. output이 Schema에 맞지 않으면 `OUTPUT_SCHEMA_MISMATCH`이며 성공 evidence를 만들지 않는다.

보고:

```text
Connected: <project> · godot=<version> · state=<state> · capabilities=<count>
base=<commit> · operation=<id> · task=<id|none> · code=<stable-code> · evidence=<paths>
```
