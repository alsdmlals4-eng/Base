# Godot live-editor adapter

프로젝트가 Godot live Editor 자동화를 실제로 구성한 경우에만 다음 경로를 사용한다.

- Project capability source: `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Project adapter: `.agents/skills/godot-live-editor-operations/SKILL.md`
- Base pin and route authority: `skills/PROJECT_BASE_ADAPTER.json`
- Base canonical contract: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Base security and recovery contract: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`

공용 계약과 Schema는 프로젝트 상대경로로 추정하거나 복제하지 않는다. `skills/PROJECT_BASE_ADAPTER.json`과 generated snapshot을 먼저 검증하고, **validated Base adapter**가 고정한 Base repository·commit에서 **Base canonical contract**를 읽는다.

작업 시작:

```text
validate PROJECT_BASE_ADAPTER.json and snapshot
→ doctor → status → catalog --compact
→ normalized project path
→ project.godot SHA-256
→ project fingerprint
→ adapter/contract/catalog freshness
```

Base adapter 검증 실패, Manifest 없음, `NOT_CONFIGURED`, stale, Schema-invalid, identity-mismatched이면 engine action을 중단한다. port만으로 프로젝트를 선택하지 않는다.

등록된 typed capability만 사용한다. automatic approval과 unsafe retry는 금지한다. mutation timeout 뒤에는 재전송하지 말고 `operation_id`·`task_id`·ledger와 변경 target을 reconcile한다.

보고:

```text
Connected: <project> · godot=<version> · state=<state> · capabilities=<count>
base=<commit> · operation=<id> · task=<id|none> · code=<stable-code> · evidence=<paths>
```
