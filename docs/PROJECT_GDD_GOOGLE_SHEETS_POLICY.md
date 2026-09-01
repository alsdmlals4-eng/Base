# Project GDD Google Sheets Compatibility Policy

## Status

`MIGRATION_ONLY_UNTIL_REMOVAL`

The default project operating surface is `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE` / `REPOSITORY_PRIMARY_CANON` from `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`. `V4_NOTION_EXCEPTION_ONLY` / `NO_NEW_NOTION_WRITE_BY_DEFAULT`: Google Sheets and Notion are not the default workspace for new projects, new visual planning, asset cataloging, or project status management.

This policy exists only for projects that already contain unique material in an older configured Sheet and have not yet completed migration/readback.

## Authority

```text
latest user decision
→ repository-owned planning / asset catalog / visual map and exact-SHA derived human view
→ repository-native code, data, scenes, resources, implementation assets and tests for runtime truth
→ V4 Notion exception only when explicitly approved and scoped
→ legacy Google Sheet only when unique unmigrated material remains
→ external references
```

A legacy Sheet never overrides current user decisions, current Project relation, `REPOSITORY_PRIMARY_CANON`, repository runtime truth, or an approved V4 exception record merely because it has a newer edit timestamp.

## Compatibility states

- `COMPATIBILITY_ONLY`: legacy Sheet remains readable because unique material may still exist.
- `PROPOSED_SHEET_CHANGE`: a user edit exists only in the legacy Sheet and must be reconciled before promotion.
- `MIGRATION_PENDING`: unique material still needs migration.
- `MIGRATED_READBACK_VERIFIED`: intended material has been moved to the active repository authority and exact-SHA derived view, with V4 exception destination only when applicable, and read back successfully.
- `BLOCKED_UNVERIFIED`: access, provenance or migration evidence is insufficient.

## Migration rule

```text
legacy Sheet material
→ classify unique / duplicate / obsolete
→ map unique material to the correct Project
→ migrate to repository planning/asset owner or repository runtime source; V4 exception only when applicable
→ preserve source provenance where material
→ read back the destination
→ mark the old Sheet compatibility-only or archive it
```

Do not bulk-copy the old workbook into Notion or another surface. Preserve meaning, decision history and unique evidence while removing duplicated presentation structure.

## Project separation

`PROJECT_RELATION_REQUIRED` applies during migration. A row cannot be migrated as project canon until its destination Project is known. If project identity is ambiguous, keep the row unpromoted and report the ambiguity instead of guessing.

## Visual and asset migration

Visual previews, references and asset candidates migrate to the repository asset manifest/catalog with the correct Project, Record Type, approval state and source metadata. Human-facing derived views may hide IDs, prompts, hashes and system notes without deleting them.

Rendered flow diagrams are migrated as `VISUAL_MAP_DERIVED`; the underlying semantic Screen or relationship records own the current meaning.

## Runtime boundary

A Sheet row, Notion record, screenshot, or visual map is not runtime proof. Code, scenes, resources, config, builds and QA evidence remain repository/runtime evidence.

## Removal after migration

Google Sheets는 신규 계획·수정·승인 데이터를 받지 않는 `MIGRATION_ONLY_UNTIL_REMOVAL` source다. 각 legacy Sheet는 한 번만 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다. `UNIQUE`만 올바른 Project의 repository structured/runtime owner와 exact-SHA derived view로 이관하고 destination readback을 검증한다. `DUPLICATE / OBSOLETE`는 활성 자료로 재검토하지 않는다.

모든 unique material이 `MIGRATED_READBACK_VERIFIED`이고 active consumer/reference가 0이면 해당 Sheet와 Sheet 전용 템플릿·라우팅·기본 검색 참조는 제거한다. 법적/감사/rollback에 꼭 필요한 최소 provenance만 archive manifest에 남길 수 있으며 기본 탐색에서 제외한다.

## Completion

Do not claim a Sheet migration complete until:

1. unique material has a destination;
2. Project identity is explicit;
3. current decisions are not duplicated as conflicting authorities;
4. destination readback succeeds;
5. any still-unmigrated material is explicitly listed.
