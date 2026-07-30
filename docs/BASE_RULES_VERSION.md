# Base Rules Version

## Canonical status

| Field | Value |
| --- | --- |
| Base rules line | `v9.0.0` |
| Status | `BASE_RELEASED` |
| Release commit | `585a53a25be1b04c543196f5901551deb49c7691` (`release: finalize Base v9 operating system (#69)`) |
| Baseline reviewed | `f87502a1bb97bdd02a1551cdd41b1d95cad457dd` |
| Active Skill count | Generated from `skills/SKILL_REGISTRY.json`; not a design constraint |
| Project adoption | `POST_RELEASE_PROJECT_ADOPTION_WAVE`; it does not block the Base v9.0.0 release |

This document is the canonical source for Base's own version and release state. It
does not claim a project version, project implementation state, or Google Sheets
state.

Base v9.1 is a compatible candidate operating layer over this immutable v9.0.0
release boundary. Its project adapters separate `release_commit` from
`release_evidence_commit`; `../base-v9.1.lock.json` records the machine-readable
`RELEASE_CANDIDATE` identity without rewriting the table above.

## Compatibility rule

The Registry and each active Skill's frontmatter are the machine-readable source
of truth for active Skills. Human-facing lists, plugin metadata, and project
snapshots are generated views. A generated view must not silently become a second
authority.

Skill additions, consolidations, and retirements are permitted when their
responsibility boundary is explicit and their migration path is recorded. The
number of active Skills is an observed Registry value, not a release target.

## Release boundary

`v9.0.0` is a released Base-only line. Its release commit is
`585a53a25be1b04c543196f5901551deb49c7691`; the required Base contracts,
deterministic generated artifacts, integrity checks, and GitHub Actions evidence
were accepted for that merge. Project adoption is a separate post-release wave and
does not block the Base v9.0.0 release.

The five named project repositories and their Sheets are outside this change. They
remain `[보류]`; Base must not write to those repositories or Sheets as part of
this Base release.

## Related canonical documents

- [Base v9 system map](operations/BASE_V9_SYSTEM_MAP.md)
- [Base v9 maturity model](operations/BASE_V9_MATURITY_MODEL.md)
- [Base v9 migration map](operations/BASE_V9_MIGRATION_MAP.md)
- [Base v9 release contract](operations/BASE_V9_RELEASE_CONTRACT.md)
- [Project GDD Google Sheets policy](PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [Base shared Skill adapter contract](BASE_SHARED_SKILL_ADAPTER_CONTRACT.md)
- [Base v9.1 release contract](operations/BASE_V9_1_RELEASE_CONTRACT.md)
- [Base v9.1 system map](operations/BASE_V9_1_SYSTEM_MAP.md)
- [Base v9.1 dual-axis maturity model](operations/BASE_V9_1_MATURITY_MODEL.md)
