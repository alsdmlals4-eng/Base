# Godot live-editor adapter

프로젝트가 Godot live Editor 자동화를 실제로 구성한 경우에만 다음 파일을 사용한다.

- Capability source: `GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json`
- Project adapter: `.agents/skills/godot-live-editor-operations/SKILL.md`
- Common contract: `docs/knowledge/godot/GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md`
- Security and recovery: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`

작업 시작:

```text
doctor → status → catalog --compact
→ normalized project path
→ project.godot SHA-256
→ project fingerprint
→ adapter/contract/catalog freshness
```

Manifest가 없거나 `NOT_CONFIGURED`, stale, Schema-invalid, identity-mismatched이면 engine action을 중단한다. port만으로 프로젝트를 선택하지 않는다.

등록된 typed capability만 사용한다. automatic approval과 unsafe retry는 금지한다. mutation timeout 뒤에는 재전송하지 말고 `operation_id`·`task_id`·ledger와 변경 target을 reconcile한다.

보고:

```text
Connected: <project> · godot=<version> · state=<state> · capabilities=<count>
operation=<id> · task=<id|none> · code=<stable-code> · evidence=<paths>
```
