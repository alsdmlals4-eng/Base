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

## Authority layers

| Field | Authority |
| --- | --- |
| Immutable rules baseline | `v9.0.0` and `base.lock.json` at its trusted release history |
| Latest released compatible line | `v9.4.4` and `base-v9.4.4.lock.json` |
| Current routing authority | `skills/SKILL_REGISTRY.json` plus each active Skill's frontmatter |
| Frozen v9.0 release derivatives | `.codex-plugin/plugin.json`, `base.lock.json`, `skills/BASE_V9_SKILL_SNAPSHOT.json` |

The frozen v9.0 release derivatives prove the v9.0 release payload. They are not a current projection of later compatible Skill descriptions or routing changes. The current human-readable active list is `docs/generated/BASE_ACTIVE_SKILLS.md`, bound to the current Registry bytes.

This document is the canonical source for Base's own version and release state. It
does not claim a project version, project implementation state, or Google Sheets
state.

Base v9.1 is a released compatible operating layer over this immutable v9.0.0
release boundary. Its project adapters separate `release_commit` from
`release_evidence_commit`; `../base-v9.1.lock.json` records that released identity
without rewriting the table above.

Base v9.2 is a released compatible operating layer. It activates the v9
Vertical Slice reconciliation contract while retaining v6~v8 as non-authoritative
compatibility inputs. Its release identity is recorded separately in
`../base-v9.2.lock.json`; it must not rewrite the immutable v9.0 table above.
Its evidence and pin-finalization history remains in its own lock and release record.

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

The named project repositories and their Sheets are outside Base release payloads.
Base must not write to those repositories or Sheets as part of a Base candidate,
evidence, or pin-finalization PR.

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
- [Base v9.4 release contract](operations/BASE_V9_4_RELEASE_CONTRACT.md)
- [Base v9.4.1 compatibility release contract](operations/BASE_V9_4_1_RELEASE_CONTRACT.md)
- [Base v9.4.2 compatibility release contract](operations/BASE_V9_4_2_RELEASE_CONTRACT.md)
- [Base v9.4.3 compatibility release contract](operations/BASE_V9_4_3_RELEASE_CONTRACT.md)
- [Base v9.4.4 compatibility release contract](operations/BASE_V9_4_4_RELEASE_CONTRACT.md)

## Base v9.4 released compatible line

Base v9.4 is the released AI-operations line over v9.3. It adds model/effort/cost routing and judgment-centered instruction, context, artifact, and game UI motion contracts while preserving their independent responsibility boundaries.

Its machine identity is recorded in `../base-v9.4.lock.json`:

- payload commit: `a728712cb776ec98f4875914a580fcf7d0156593`
- trusted evidence commit: `ef1fba11167e4da0b298123b0c85ebd268191a42`
- Registry SHA-256: `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`

The immutable v9.0 table and released v9.1-v9.3 identities are not rewritten.

## Base v9.4.1 released compatible line

Base v9.4.1 is the released Skill-evidence and external-AI worktree compatibility line over v9.4.0. It preserves the v9.4.0 Registry bytes while adding complete active-Skill behavior coverage, reproducible result identity, explicit implementation evidence, and executable worktree isolation validation.

Its machine identity is recorded in `../base-v9.4.1.lock.json`:

- payload commit: `3f2c4a624d302b704c1b5322eb5c9f34ad55abb9`
- trusted evidence commit: `ff117d24d5bdb121314e109a6aa9b4f552e0fdc1`
- Registry SHA-256: `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`

Project adoption is a separate post-release wave and must pin this exact payload/evidence pair before claiming v9.4.1 validator adoption. Actual external model routing and real project external-AI worktree execution remain `NOT_RUN` until separately executed.

## Base v9.4.2 released compatible line

Base v9.4.2 is the released planning-first and Grill Me decision-batch compatibility line over v9.4.1. It preserves the v9.4.1 Registry bytes while adding the L1 planning-first Gate, GPT-recommended reversible numeric defaults, user-approved planning conflicts, maximum-ten Decision batches with early checkpoints, exact-head adversarial merge gates, and merged-main/Sheet readback states.

Its machine identity is recorded in `../base-v9.4.2.lock.json`:

- payload commit: `dd705d7f48a7919187bc0507610ba5fc5b43a658`
- trusted evidence commit: `0c6cdd128bf1f5782e96b3a6240c9585f8d1ef6d`
- Registry SHA-256: `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`

Project adoption is a separate post-release wave and must pin this exact payload/evidence pair before claiming v9.4.2 planning-first governance adoption. Real project Grill Me batch execution, external model behavior, and human process usability remain `NOT_RUN` until separately piloted.

## Base v9.4.3 released compatible line

Base v9.4.3 is the released first-prompt intake compatibility line over v9.4.2. It preserves the v9.4.2 Registry bytes while adding a direction anchor at the start of generated instructions, Task·Context·Source·Constraints·Output·Validation completeness, conditional response diversification, and the mandatory `first-prompt → contract → Grill Me` execution gate for L1+ work.

Its machine identity is recorded in `../base-v9.4.3.lock.json`:

- payload commit: `7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8`
- trusted evidence commit: `da33a350d61b8adc52df97fccc7001708a933370`
- Registry SHA-256: `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`

Project adoption is a separate post-release wave and must pin this exact payload/evidence pair before claiming v9.4.3 first-prompt governance adoption. Cross-model behavior improvement, prompt rework reduction, human comprehension, and real project Adapter execution remain `NOT_RUN` until separately piloted.

## Base v9.4.4 released compatible line

Base v9.4.4 is the released reuse-first intake compatibility line over v9.4.3. It preserves the v9.4.3 history while adding a fail-closed preflight that checks current project implementation/assets/tests, approved Project Asset/Reference/Benchmark material, Base reuse and accumulated knowledge/case/reference, targeted cross-project evidence, and only then decision-relevant external research before new design or creation. It also requires the existing project-to-Base reuse learning handoff at completion.

Its machine identity is recorded in `../base-v9.4.4.lock.json`:

- payload commit: `210ec78292fa12ed7563ba743b322dd36103ae4a`
- trusted evidence commit: `bb61e68dc3028421b60c11b87ba2abd297ee6f78`
- Registry SHA-256: `08f882d0c77339e8f7ff187c35b79501e0a2958ab1ff1c7aaa1c0ef8dbee45d6`

Project adoption is a separate post-release wave. Before a project can claim v9.4.4 adoption, the immutable v9.4.4 finalization commit must be indexed by `tools/base_release_index.py`, and the project Adapter must pin the exact payload/evidence/finalization identity. Future agent adherence, human workflow usability, real project Adapter execution, and cross-project reuse quality remain `NOT_RUN` until separately exercised.
