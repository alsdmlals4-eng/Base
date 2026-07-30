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

Base v9.2 is the next compatible candidate operating layer. It activates the v9
Vertical Slice reconciliation contract while retaining v6~v8 as non-authoritative
compatibility inputs. Its release identity is recorded separately in
`../base-v9.2.lock.json`; it must not rewrite the immutable v9.0 table above.
Until its separate evidence and pin-finalization PRs are merged, its candidate
pins are null and projects must continue to use their existing verified Base pin.

Base v9.3 is the compatible correction line for the active v9 contract. It keeps
the v9.2 release commits intact while restoring the v8 single-attachment journey:
repository-first interview, planning, Codex handoff/implementation, validation,
and merged-main synchronization when the request and project gates authorize it.
Its release identity is recorded in `../base-v9.3.lock.json`; reconciliation is
now a conditional safety profile, not the universal default.

## Compatibility rule

The Registry and each active Skill's frontmatter are the machine-readable source
of truth for active Skills. Human-facing lists, plugin metadata, and project
snapshots are generated views. A generated view must not silently become a second
authority.

Skill additions, consolidations, and retirements are permitted when their
responsibility boundary is explicit and their migration path is recorded. The
number of active Skills is an observed Registry value, not a release target.

## Merge execution authority

The default merge policy is `AUTO_MERGE_AFTER_REQUIRED_CHECKS` with
`AGENT_MERGE_REQUIRED`. Once a repository-owned PR is non-Draft, its reviewed
HEAD still matches, all required checks and independent review gates pass, no
unresolved review thread or P0/P1 finding remains, and no
`USER_REVIEW_REQUIRED` or `CHANGE_PROPOSAL` decision is open, the responsible
agent must merge it with the repository's allowed method. A separate user merge
click is not required. When GitHub auto-merge is unavailable, execute the
allowed direct PR merge after the same evidence is verified; do not treat an
available merge as an approval-wait state.

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
- [Vertical Slice v8 → v9 migration traceability](knowledge/VERTICAL_SLICE_V8_TO_V9_MIGRATION.md)
- [Base v9.2 release contract](operations/BASE_V9_2_RELEASE_CONTRACT.md)
- [Base v9.3 release contract](operations/BASE_V9_3_RELEASE_CONTRACT.md)
