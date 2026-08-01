# Base P2 Entrypoint Ownership and Compaction Implementation Plan

> **For agentic workers:** Use `superpowers:test-driven-development`, `superpowers:executing-plans`, `superpowers:verification-before-completion`, and an adversarial review pass. Do not use a numerical line or character target.

**Goal:** Make `AGENTS.md` the small always-on invariant layer and `START_HERE.md` the one-step cold-start router without losing safety, authority, routing, or verification contracts.

**Architecture:** Preserve detailed behavior in its existing canonical owner. Add semantic ownership tests first, replace the two duplicated entrypoints with role-specific documents, then verify all existing consumers and untouched protected surfaces.

**Baseline:** `main@dfcca68f3b0c654b5b75e6772b014e8fc8ef63af` on `codex/base-p2-entrypoint-compaction`.

## Global constraints

- Preserve `skills/SKILL_REGISTRY.json` bytes, released locks, generated/frozen Base artifacts, compatibility materials, project repositories, Google Sheets, Godot files, code, data, and assets.
- Preserve one-step discovery for active request owners and existing explicit entrypoint tests.
- Do not add a new Skill or duplicate an existing Skill procedure.
- Do not use line count, character count, compression ratio, or a maximum-size test as a quality gate.
- Use repository facts and official primary guidance as benchmark evidence; external guidance does not override Base authority.
- Treat missing or stale pointers, lost safety rules, and hidden conditional procedures as failures.

## Task 1: Freeze semantic ownership in RED tests

**Files:**

- Create: `tests/test_entrypoint_ownership.py`

- [x] Assert the distinct declared roles of `AGENTS.md` and `START_HERE.md`.
- [x] Assert canonical pointers and required one-step request routes.
- [x] Assert always-on safety and proposal boundaries remain in `AGENTS.md`.
- [x] Assert detailed status/publication/review procedures are delegated out of both entrypoints.
- [x] Run the focused test and record failure against the current mixed-responsibility files.

## Task 2: Compact `AGENTS.md` to always-on invariants

**Files:**

- Modify: `AGENTS.md`

- [x] Preserve source priority, environment/permission, truthful evidence, user-change, release, legacy, proposal, asset, and project/Sheet guardrails.
- [x] Keep selective routing and completion evidence requirements.
- [x] Replace detailed procedures and conditional domain guidance with direct canonical links.
- [x] Run the ownership test and existing tests that inspect `AGENTS.md`.

## Task 3: Compact `START_HERE.md` to one-step routing

**Files:**

- Modify: `START_HERE.md`

- [x] Preserve the minimum invocation and Base cold-start distinction.
- [x] Replace long procedure sections with a request/owner/next-file route table.
- [x] Preserve project reading order, v9 integrated prompt, system/difficulty route, UI polishing route, and legacy aliases.
- [x] Run the ownership test and existing tests that inspect `START_HERE.md`.

## Task 4: Documentation and learning synchronization

**Files:**

- Modify: `docs/CHANGELOG.md`
- Modify: `docs/DOCUMENTATION_MAP.md` only if its role description is stale.
- Modify: `skills/SKILL_LEARNING_LOG.md`

- [x] Record the role split, benchmark basis, and no-size-gate boundary.
- [x] Record that compaction is structural evidence, not model-behavior or project-runtime proof.

## Task 5: Adversarial verification and publication

- [x] Run focused entrypoint, routing, UI, difficulty/AI, Vertical Slice, Google Sheets, and operating-system tests.
- [x] Run the canonical local validation entrypoint from P1.
- [x] Run reference freshness, whitespace, Git object, Registry/release protection, and generated-artifact checks.
- [x] Attack missing route, stale ID, duplicated policy, lost approval boundary, false Base status, and untouched consumer cases.
- [ ] Review the final diff, publish a Draft PR, verify exact-head Actions and review threads, then exact-head squash merge if every gate passes.
