# Godot Live Editor Contract v2 — Current Main Amendment

## Status

- Date: `2026-08-05`
- Authority: `CURRENT_MAIN_RECONCILIATION`
- Current main baseline: `45f470853285477df79c915df9b711c77bd8b8a2`
- BCP: `BCP-2026-005-godot-live-editor-contract-v2`
- BCP state: `APPROVED_FOR_IMPLEMENTATION`
- Submission PR: `#156`
- Approval transition PR: `#159`
- Source design and plan: PR `#157` document blobs

## Precedence

This amendment governs any conflict between the approved design/plan and repository state at merge time.

1. Do not implement on `agent/godot-live-editor-contract-v2-reconciliation` or any design-and-plan branch.
2. Start implementation only after a new explicit implementation authorization.
3. At implementation time, re-fetch `main` and create a fresh isolated branch or worktree from the exact current main commit.
4. Keep the test-only RED commit separate from the documentation merge. A deliberately failing RED branch is evidence, not merge-ready code.
5. Preserve `skills/SKILL_REGISTRY.json`, Base v9.4.3 and predecessor release locks, frozen derivatives, v1 Schemas, and existing Godot 4.7.1 Pilot evidence unless a later approved task explicitly changes them.
6. Static v2 reconciliation cannot claim Godot runtime, physical-input, project-behavior, or human-usability success.
7. Any later implementation PR must pass its exact current-main merge ref, resolve all MUST_FIX findings, and have zero unresolved review threads before merge consideration.

## Current evidence boundary

```yaml
written_spec: APPROVED
implementation_plan: APPROVED_FOR_EXECUTION_AFTER_SEPARATE_AUTHORIZATION
bcp: APPROVED_FOR_IMPLEMENTATION
documentation_merge: AUTHORIZED
implementation: NOT_AUTHORIZED_BY_THIS_AMENDMENT
test_only_red: PRESERVED_OUTSIDE_DOCUMENTATION_MERGE
v2_schema: NOT_IMPLEMENTED
semantic_validator: NOT_IMPLEMENTED
godot_v2_runtime: NOT_RUN
production_adapter_ready: false
```
