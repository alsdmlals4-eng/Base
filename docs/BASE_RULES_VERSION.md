# Base Rules Version

## Canonical status

| Field | Value |
| --- | --- |
| Base rules line | `v9.0.0-rc.1` |
| Status | `RC_IN_PROGRESS` |
| Baseline reviewed | `f87502a1bb97bdd02a1551cdd41b1d95cad457dd` |
| Active Skill count | Generated from `skills/SKILL_REGISTRY.json`; not a design constraint |
| Final release | `v9.0.0` is `WAVE_2_HOLD` until project adoption and verification are complete |

This document is the canonical source for Base's own version and release state. It
does not claim a project version, project implementation state, or Google Sheets
state.

## Compatibility rule

The Registry and each active Skill's frontmatter are the machine-readable source
of truth for active Skills. Human-facing lists, plugin metadata, and project
snapshots are generated views. A generated view must not silently become a second
authority.

Skill additions, consolidations, and retirements are permitted when their
responsibility boundary is explicit and their migration path is recorded. The
number of active Skills is an observed Registry value, not a release target.

## Release boundary

`v9.0.0-rc.1` may be proposed only after Base contracts, deterministic generated
artifacts, integrity checks, and CI evidence agree. `v9.0.0` must not be released
while the common project adoption wave remains on hold.

The five named project repositories and their Sheets are outside this change. They
remain `[보류]`; Base must not write to those repositories or Sheets in this
release candidate.

## Related canonical documents

- [Base v9 system map](operations/BASE_V9_SYSTEM_MAP.md)
- [Base v9 maturity model](operations/BASE_V9_MATURITY_MODEL.md)
- [Base v9 migration map](operations/BASE_V9_MIGRATION_MAP.md)
- [Base v9 release contract](operations/BASE_V9_RELEASE_CONTRACT.md)
- [Project GDD Google Sheets policy](PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [Base shared Skill adapter contract](BASE_SHARED_SKILL_ADAPTER_CONTRACT.md)
