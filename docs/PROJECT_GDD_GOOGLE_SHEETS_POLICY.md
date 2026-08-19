# Project GDD Google Sheets Compatibility Policy

## Status

`MIGRATION_ONLY_UNTIL_REMOVAL`

The default project operating surface is `NOTION_DEFAULT_PROJECT_WORKSPACE`. Google Sheets is not the default workspace for new projects, new visual planning, asset cataloging, or project status management.

This policy exists only for projects that already contain unique material in an older configured Sheet and have not yet completed migration/readback.

## Authority

```text
latest user decision
→ project Notion workspace for project planning / asset catalog / visual map
→ repository-native code, data, scenes, resources, implementation assets and tests for runtime truth
→ legacy Google Sheet only when unique unmigrated material remains
→ external references
```

A legacy Sheet never overrides current user decisions, current Project relation, repository runtime truth, or an approved Notion project record merely because it has a newer edit timestamp.

## Compatibility states

- `COMPATIBILITY_ONLY`: legacy Sheet remains readable because unique material may still exist.
- `PROPOSED_SHEET_CHANGE`: a user edit exists only in the legacy Sheet and must be reconciled before promotion.
- `MIGRATION_PENDING`: unique material still needs migration.
- `MIGRATED_READBACK_VERIFIED`: intended material has been moved to the active Notion/repository authority and read back successfully.
- `BLOCKED_UNVERIFIED`: access, provenance or migration evidence is insufficient.

## Migration rule

```text
legacy Sheet material
→ classify unique / duplicate / obsolete
→ map unique material to the correct Project
→ migrate to Notion Work Master, Asset & Knowledge Master, or repository runtime source
→ preserve source provenance where material
→ read back the destination
→ mark the old Sheet compatibility-only or archive it
```

Do not bulk-copy the old workbook into Notion. Preserve meaning, decision history and unique evidence while removing duplicated presentation structure.

## Project separation

`PROJECT_RELATION_REQUIRED` applies during migration. A row cannot be migrated as project canon until its destination Project is known. If project identity is ambiguous, keep the row unpromoted and report the ambiguity instead of guessing.

## Visual and asset migration

Visual previews, references and asset candidates migrate to `ASSET_KNOWLEDGE_MASTER` with the correct Project, Record Type, approval state and source metadata. Human-facing views may hide IDs, prompts, hashes and system notes without deleting them.

Rendered flow diagrams are migrated as `VISUAL_MAP_DERIVED`; the underlying semantic Screen or relationship records own the current meaning.

## Runtime boundary

A Sheet row, Notion record, screenshot, or visual map is not runtime proof. Code, scenes, resources, config, builds and QA evidence remain repository/runtime evidence.

## Removal after migration

Google Sheets는 신규 계획·수정·승인 데이터를 받지 않는 `MIGRATION_ONLY_UNTIL_REMOVAL` source다. 각 legacy Sheet는 한 번만 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다. `UNIQUE`만 올바른 Project의 Notion 사람용 owner 또는 repository structured/runtime owner로 이관하고 destination readback을 검증한다. `DUPLICATE / OBSOLETE`는 활성 자료로 재검토하지 않는다.

모든 unique material이 `MIGRATED_READBACK_VERIFIED`이고 active consumer/reference가 0이면 해당 Sheet와 Sheet 전용 템플릿·라우팅·기본 검색 참조는 제거한다. 법적/감사/rollback에 꼭 필요한 최소 provenance만 archive manifest에 남길 수 있으며 기본 탐색에서 제외한다.

## Completion

Do not claim a Sheet migration complete until:

1. unique material has a destination;
2. Project identity is explicit;
3. current decisions are not duplicated as conflicting authorities;
4. destination readback succeeds;
5. any still-unmigrated material is explicitly listed.
