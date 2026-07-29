# Base v9 Release Contract

## Release states

| Version | State | Entry condition | Exit condition |
| --- | --- | --- | --- |
| `v9.0.0` | `BASE_RELEASE_PENDING_CI` | Base-only design, machine contracts, generated artifacts, and local validation are consistent | Required GitHub Actions gates pass and the release is merged |
| Project adoption | `POST_RELEASE_PROJECT_ADOPTION_WAVE` | Base v9.0.0 is released and a named project is explicitly resumed | The project records repository, Sheet-access, user-approval, and verification evidence |

`v9.0.0` is a Base-only release. It must not imply that a project has adopted v9
or that a Sheet has been created, read, or written.

## Required Base release evidence

- Plugin manifest and Base lock validate against the Registry-derived view.
- Registry/frontmatter, generated documentation, project snapshot, and hashes are
  deterministic across two consecutive generator runs.
- Dependency cycle, orphan, duplicate-responsibility, legacy-alias, template
  consumer, provenance, and documentation-link checks pass or retain an explicit
  non-passing status.
- The Sheet control contract confirms `BASE_EXCLUDED`; no external Sheet write is
  part of this Base release.
- `ci-gate` and `adversarial-gate` appear for documentation-only, code, and
  workflow pull-request paths, with actual CI evidence recorded where runnable.
- Windows/local and GitHub Actions results distinguish `PASSED`, `FAILED`,
  `NOT_RUN`, and `UNVERIFIED`.

## POST_RELEASE_PROJECT_ADOPTION_WAVE

The following projects are `[보류]` after the Base-only v9.0.0 release:

- Ten Paces: Hidden Moves
- Blacksmith
- OMENWARD
- urban-legend
- GRIMOIRE: 세계를 다시 쓰는 법

Before a held project can resume, all of the following are required: Base v9.0.0 lock,
actual repository audit, confirmed Sheet access, explicit user approval, and a
working project verification environment. Project implementation, project Skill
snapshots, and Google Sheets writes are not authorized by this Base change.

## Base release rule

`v9.0.0` is released after Base-only contracts, deterministic generation,
integrity checks, and required GitHub Actions evidence agree. The project adoption
wave must not block the Base v9.0.0 release. It is a separately authorized phase
with per-project evidence and compatibility review.

최종 릴리스는 공통 프로젝트 적용과 검증을 대신하는 선언이 아니다.
