# Base v9 Adversarial Review Report

## Scope

Base v9.0.0 files only. Project repositories and Google Sheets were not opened,
modified, or used as release evidence.

## Attacks and decisions

| Attack | Evidence | Decision |
| --- | --- | --- |
| A second authority quietly replaces the Registry | Active entrypoint tables were replaced by Registry-derived view links; lock/plugin/snapshot hashes derive from the Registry | `MUST_FIX` found and fixed |
| Generated artifacts change on a second run | Focused deterministic-generator test and `--check` | `ACCEPT` |
| An active package is orphaned or a dependency cycle is hidden | Registry/path/frontmatter and declared dependency-graph validation | `ACCEPT` for current declared graph |
| A fixed active-Skill count becomes a policy constraint | Current operational documents no longer declare a fixed count; generated summary reports the observed count | `ACCEPT` |
| A project or Sheet is accidentally modified during Base work | Sheet control contract, release contract, and held work order | `ACCEPT` |
| Project adoption is confused with Base release evidence | `POST_RELEASE_PROJECT_ADOPTION_WAVE` is separate and does not block the Base v9.0.0 release | `ACCEPT` |
| CI or platform evidence is implied without execution | Local tests are recorded; GitHub Actions and Windows publication checks remain unexecuted | `UNVERIFIED` follow-up |

## Regression recheck

The static active-Skill tables were the validated finding. After consolidation to the generated view, package-integrity, GDD contract, v9 contract, generator, and integrity tests were rerun successfully. The full local test suite is required again after any later change to this report, workflow, Registry, or generator.

## Decision

`ACCEPT_WITH_FOLLOWUP`: the Base v9.0.0 release design is internally consistent
under local evidence. Required GitHub Actions evidence remains a merge gate;
project adoption is deferred to `POST_RELEASE_PROJECT_ADOPTION_WAVE`.
