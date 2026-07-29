# Base v9 Release Contract

## Release states

| Version | State | Entry condition | Exit condition |
| --- | --- | --- | --- |
| `v9.0.0-rc.1` | `RC_IN_PROGRESS` | Base-only design, machine contracts, generated artifacts, and focused tests are implemented | All required Base validation evidence agrees and release review accepts the candidate |
| `v9.0.0` | `WAVE_2_HOLD` | RC is accepted and common project adoption work is explicitly authorized | Each adopted project has actual repository, Sheet-access, user-approval, and verification evidence |

`v9.0.0-rc.1` is a Base release candidate. It must not imply that a project has
adopted v9 or that a Sheet has been created, read, or written.

## Required Base RC evidence

- Plugin manifest and Base lock validate against the Registry-derived view.
- Registry/frontmatter, generated documentation, project snapshot, and hashes are
  deterministic across two consecutive generator runs.
- Dependency cycle, orphan, duplicate-responsibility, legacy-alias, template
  consumer, provenance, and documentation-link checks pass or retain an explicit
  non-passing status.
- The Sheet control contract confirms `BASE_EXCLUDED`; no external Sheet write is
  part of this candidate.
- `ci-gate` and `adversarial-gate` appear for documentation-only, code, and
  workflow pull-request paths, with actual CI evidence recorded where runnable.
- Windows/local and GitHub Actions results distinguish `PASSED`, `FAILED`,
  `NOT_RUN`, and `UNVERIFIED`.

## WAVE_2_HOLD: common project adoption

The following projects are `[보류]` in this Base-only release candidate:

- Ten Paces: Hidden Moves
- Blacksmith
- OMENWARD
- urban-legend
- GRIMOIRE: 세계를 다시 쓰는 법

Before a held project can resume, all of the following are required: Base RC lock,
actual repository audit, confirmed Sheet access, explicit user approval, and a
working project verification environment. Project implementation, project Skill
snapshots, and Google Sheets writes are not authorized by this Base change.

## Final release rule

`v9.0.0` is not a documentation milestone. It is released only after WAVE_2_HOLD
is cleared with per-project evidence and a final compatibility review. Until then,
the final release remains blocked by `WAVE_2_HOLD`.

최종 릴리스는 공통 프로젝트 적용과 검증을 대신하는 선언이 아니다.
