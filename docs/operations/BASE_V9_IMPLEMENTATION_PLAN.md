# Base v9.0.0 Implementation Plan

## RC work

1. Establish version, release, maturity, migration, and system-map canon.
2. Generate the plugin manifest, Base lock, Skill snapshot, and audit-control artifacts from the Base Registry.
3. Remove fixed active-Skill counts from current operational entrypoints and use the generated active-Skill view instead.
4. Add UI reference and Godot UX/UI verification contracts.
5. Audit links, Registry paths, template consumers, aliases, provenance, cycles, orphans, and duplicate responsibility boundaries.
6. Run focused checks, full regression, generator idempotence, and applicable Windows/CI checks; record unavailable evidence as `NOT_RUN` or `UNVERIFIED`.

## Release boundary

The result may become `v9.0.0` after Base-only evidence is consistent and the
required GitHub Actions gates pass. Project repositories, GDD Sheets, project
adapters, and project runtime validation are a separate
`POST_RELEASE_PROJECT_ADOPTION_WAVE`.

## Non-goals

- No project repository modification.
- No Google Sheets read, write, or creation.
- No direct merge of proposed Skill pull requests.
- Do not perform project adoption inside the Base release; it is resumed only in
  `POST_RELEASE_PROJECT_ADOPTION_WAVE`.
