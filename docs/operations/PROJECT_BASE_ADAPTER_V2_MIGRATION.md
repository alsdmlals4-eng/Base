# PROJECT_BASE_ADAPTER v2 Migration

`PROJECT_BASE_ADAPTER` v2 adds one project-owned canonical identity: `project.project_id`. It is required for Tool Hub and multi-project Studio launches. The ID must use lowercase kebab-case and must exactly match the project Figma routing registry entry; neither a path, repository name, nor Hub registration may infer it. Migration must not overwrite the v1 adapter.

## Status boundary

- v1 remains valid for the released v9.1 audit/build/check workflow.
- v1 is `IDENTITY_MIGRATION_REQUIRED` for Tool Hub production use.
- v2 is a separate schema and template. Base does not mutate the v1 schema in place.
- Project adapter `validators` remain compatibility metadata. Tool Hub and `base-tool-contracts` never shell-parse or execute those strings.

## Explicit migration

From the Base checkout, write a new candidate without overwriting the project adapter:

```bash
python tools/migrate_project_base_adapter_v2.py \
  --project-root ../PROJECT \
  --project-id ten-paces-hidden-moves
```

Review `skills/MIGRATED_PROJECT_BASE_ADAPTER_V2.json`, validate it against `schemas/project-base-adapter-v2.schema.json`, cross-check the exact `project_id` in `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`, then promote it through that project's approved operating-contract change process. To verify a previously generated candidate, repeat the command with `--check`.

## Rollback

Do not overwrite or delete the v1 adapter during rollout. If a v2 adopter fails validation, stop Hub launch, retain `IDENTITY_MIGRATION_REQUIRED`, and continue using the unchanged v1 adapter for its existing audit-compatible workflow. Rollback never infers a replacement ID.
