# Base v9.0.0-rc.1 Implementation Plan

## RC work

1. Establish version, release, maturity, migration, and system-map canon.
2. Generate the plugin manifest, Base lock, Skill snapshot, and audit-control artifacts from the Base Registry.
3. Remove fixed active-Skill counts from current operational entrypoints and use the generated active-Skill view instead.
4. Add UI reference and Godot UX/UI verification contracts.
5. Audit links, Registry paths, template consumers, aliases, provenance, cycles, orphans, and duplicate responsibility boundaries.
6. Run focused checks, full regression, generator idempotence, and applicable Windows/CI checks; record unavailable evidence as `NOT_RUN` or `UNVERIFIED`.

## Release boundary

The result may become `v9.0.0-rc.1` only after Base evidence is consistent.
`v9.0.0` remains `WAVE_2_HOLD`: project repositories, GDD Sheets, project
adapters, and project runtime validation are out of scope for this change.

## Non-goals

- No project repository modification.
- No Google Sheets read, write, or creation.
- No direct merge of proposed Skill pull requests.
- No final-release claim while WAVE_2_HOLD remains active.
