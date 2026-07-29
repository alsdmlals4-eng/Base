# Base v9 Migration Map

## Rule

Open pull requests are evidence and proposals, not merge instructions. Their
unique requirements are re-evaluated against the v9 Registry, contracts, tests,
and migration evidence. This work does not directly merge PR #5, #18, #28, #29,
or #30.

열린 PR은 직접 병합하지 않는다. v9 계약과 현재 소비자, 검증 증거를 기준으로
필요한 책임만 흡수하거나 보류한다.

| Source | v9 disposition | Preserved value | Compatibility and migration requirement |
| --- | --- | --- | --- |
| PR #5 | `REASSESS` | Historic discipline-coverage analysis | Compare its findings to current coverage output; retain only evidence still supported by current paths |
| PR #18 | `CONSOLIDATE_REVIEW` | Earlier Skill consolidation rationale | Do not restore retired IDs solely for compatibility; map any still-needed consumer to a current route or an explicit alias |
| PR #28 | `ADOPT_AS_CONTRACT` | Handoff, provenance, and decision-surface requirements | Express as current contract fields and generated provenance rather than a blind file-level merge |
| PR #29 | `REASSESS_BOUNDARY` | Game-design specialization proposal | Add, split, absorb, or reject only after responsibility-overlap and lifecycle checks; record the final Registry decision |
| PR #30 | `ADOPT_AS_GATE` | PLAN→BUILD→REVIEW gate expectation | Enforce through the system map, release checks, and evidence paths rather than importing obsolete wording |

## Legacy disposition

Integrity findings and legacy materials use one of these dispositions before any
destructive action: `KEEP`, `CONSOLIDATE`, `ARCHIVE`, `RETIRE`, or `BLOCKED`.
Each record identifies consumers, replacement path, provenance, and rollback
instruction. A missing consumer audit or rollback path leaves the item `BLOCKED`.

## ROLLBACK

For a migration change, retain the prior identifier or document as an explicit
legacy alias until all known consumers have been migrated and the new generated
artifacts verify. To roll back, restore the prior mapping, regenerate outputs,
and rerun Registry, link, and consumer validation. Do not delete historical
evidence merely because an alias is retired.
