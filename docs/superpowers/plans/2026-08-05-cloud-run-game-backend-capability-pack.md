# Cloud Run Game Backend Capability Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task. Use `superpowers:systematic-debugging` for unexpected failures and `superpowers:verification-before-completion` before completion claims. Execute this plan in an isolated branch/worktree from the then-current `main`.

**Goal:** Add a reusable Base Guide and project Contract that make Cloud Run a conditional default candidate whenever a game needs server functionality, while rejecting unsuitable realtime, state, cost, security, and lifecycle assumptions.

**Architecture:** Keep all execution authority in existing Base Skills. Add one knowledge Guide, one project-owned Template, dedicated contract tests, and minimal route/discovery updates. Do not add an active Skill, Skill Registry entry, shared project route, Cloud resource, service account, database, secret, or project-specific API.

**Tech Stack:** Markdown contracts and templates, JSON documentation governance/reference-freshness configuration, Python `unittest`, Base proposal/reference validators, GitHub Actions.

**Approved source:** `BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity`

**Approval reference:** `https://github.com/alsdmlals4-eng/Base/pull/170#issuecomment-5192884554`

**Sequencing:** This is implementation PR A. Merge and post-merge verify it before starting the entitlement/integrity implementation plan because both modify shared entrypoints, Learning Log, evidence pack, test imports, and reference-freshness configuration.

## Global Constraints

- Preserve `skills/SKILL_REGISTRY.json` bytes and active Skill count.
- Do not modify `skills/BASE_SHARED_SKILL_ROUTES.json`.
- Do not create Google Cloud resources, credentials, secrets, billing configuration, or provider-specific application code.
- Do not claim deployment, runtime, load, failure, cost, security, or production readiness from static repository tests.
- Preserve project ownership of identity provider, database, API Schema, traffic assumptions, region, retention, cost budget, and platform IDs.
- Cloud Run is `CLOUD_RUN_DEFAULT_CANDIDATE`, never `CLOUD_RUN_REQUIRED`.
- High-frequency authoritative realtime, UDP, indefinite workers, and instance-local authoritative state remain outside the default candidate boundary.
- Every task must preserve a RED → GREEN → refactor → commit sequence.

---

## Task 1: Freeze current authority and implementation baseline

**Files:**

- Read: `[수정제안서]/BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity/PROPOSAL.md`
- Read: `[수정제안서]/BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity/DESIGN.md`
- Read: `[수정제안서]/PROPOSAL_REGISTRY.json`
- Read: `skills/managing-base-change-proposals/SKILL.md`
- Read: `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`

**Interfaces:**

- Consumes: approved BCP, current main, existing technical/operating/validation owners.
- Produces: fixed implementation branch, baseline evidence, protected-file hashes.

- [ ] Confirm current `main` contains BCP-2026-007 as `APPROVED_FOR_IMPLEMENTATION` with the exact approval reference.
- [ ] Search all open/recent PRs for the same Cloud Run Guide, Template, or test paths.
- [ ] Create `agent/implement-cloud-run-game-backend-capability` from exact current main.
- [ ] Record baseline SHA and Git blob IDs for `skills/SKILL_REGISTRY.json`, `skills/BASE_SHARED_SKILL_ROUTES.json`, released locks, and frozen derivatives.
- [ ] Run baseline proposal validation, reference freshness, focused technical/release tests, local aggregate imports, and Base integrity checks.
- [ ] Stop and classify any pre-existing failure before writing tests.
- [ ] Commit no files in this task; record evidence in the PR body or implementation log.

---

## Task 2: Write the dedicated failing contract tests

**Files:**

- Create: `tests/test_cloud_run_game_backend_capability.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**

- Consumes: approved Design tokens and expected file paths.
- Produces: executable RED contract for the missing Guide, Template, routes, and protected boundaries.

- [ ] Create tests requiring these new artifacts:
  - `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
  - `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`
- [ ] Require lifecycle tokens:
  - `SERVER_FEATURE_DETECTED`
  - `CLOUD_RUN_DEFAULT_CANDIDATE`
  - `FIT_AND_RISK_ASSESSMENT`
  - `PROJECT_OWNED_SERVICE_CONTRACT`
  - `CLOUD_RUN_RECOMMENDED`
  - `CLOUD_RUN_CONDITIONAL`
  - `ALTERNATIVE_ARCHITECTURE_REQUIRED`
  - `SERVER_NOT_REQUIRED`
  - `BLOCKED_UNVERIFIED`
- [ ] Require explicit exclusion of high-frequency authoritative realtime, UDP, indefinite workers, instance-local durable authority, and universal Cloud Run adoption.
- [ ] Require API fields for identity, authorization, request Schema/version, precondition, idempotency, rate limit, timeout, errors, retry, audit, and sensitive-log redaction.
- [ ] Require separation of service identity, end-user identity, and domain authorization.
- [ ] Require Secret Manager/server-side secret handling and forbid secrets in client, export, repository, and logs.
- [ ] Require WebSocket timeout, reconnect, external state, duplicate/out-of-order, best-effort affinity, failure degradation, and connection-cost evidence.
- [ ] Require capacity/cost fields for min/max instances, concurrency, database connections, quota, budget alert, load result, and cost per active user/match.
- [ ] Require bounded AI proxy rules and forbid LLM-only payment, reward, ban, or permanent-save authority.
- [ ] Require official Cloud Run source domains and explicit `NOT_RUN` evidence ceilings.
- [ ] Require project Template sections for player value, fit decision, authority/state, API lifecycle, identity, migration, idempotency/replay, realtime, tasks, AI proxy, secrets, privacy, cost, failure, rollback, and evidence.
- [ ] Assert no new active Skill or shared route is added.
- [ ] Import the dedicated test in both aggregate test modules.
- [ ] Run the focused test set and observe failures only for missing approved artifacts/routes.
- [ ] Commit the RED tests as `test: define Cloud Run game backend capability contract`.

---

## Task 3: Implement the minimal Cloud Run Guide and project Contract

**Files:**

- Create: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
- Create: `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`

**Interfaces:**

- Consumes: RED tests and approved Design.
- Produces: reusable decision Guide and project-owned evidence Contract.

- [ ] Write the Guide with a server-need gate before provider selection.
- [ ] Define suitable, conditional, unsuitable, and server-not-required examples.
- [ ] Define modular-monolith-first guidance for small projects and split seams only when deployment, permission, scaling, or failure boundaries differ.
- [ ] Define durable state ownership outside container memory/filesystem.
- [ ] Define authenticated mutation order: authenticate → authorize → validate → bind version/identity → idempotency/replay → transaction → durable result.
- [ ] Define IAM/service account, user identity, domain authorization, private/public endpoint, and administrator-route separation.
- [ ] Define secrets, environment separation, rotation, redaction, and minimum privilege.
- [ ] Define Cloud Tasks, Pub/Sub, Scheduler, and Cloud Run Job as conditional candidates rather than automatic dependencies.
- [ ] Define WebSocket and soft-realtime evidence requirements without implying authoritative realtime readiness.
- [ ] Define capacity, quota, egress, logging, database connection, AI-call, load, cost, alert, and provider-exit fields.
- [ ] Define AI proxy limits, output validation, privacy, provider failure, safety-filter, and budget fallback.
- [ ] Write the project Contract with fillable fields and evidence states from `NOT_REQUIRED` through project-specific runtime/load/failure verification.
- [ ] Run the dedicated tests; only route/discovery assertions may remain RED.
- [ ] Refactor duplicate prose while preserving every token and evidence boundary.
- [ ] Commit as `feat: add Cloud Run game backend capability pack`.

---

## Task 4: Connect existing owners and discovery surfaces

**Files:**

- Modify: `docs/knowledge/game-development/README.md`
- Modify: `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `START_HERE.md`
- Modify: `skills/analyzing-and-refining-game-concepts/SKILL.md`
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/designing-vertical-slices/SKILL.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Modify: `skills/optimizing-ai-model-and-prompt-costs/SKILL.md`
- Modify: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`
- Modify: `templates/project-operations/github/documentation-governance.json`

**Interfaces:**

- Consumes: Guide and Contract.
- Produces: one-step discovery and owner-preserving execution routes.

- [ ] Add one compact knowledge-hub row and one Documentation Map owner entry.
- [ ] Add a technical Guide route for server need, online service, Cloud Run suitability, state, realtime, and cost questions.
- [ ] Add a compact START_HERE route without duplicating the Guide.
- [ ] Route player-value/server-necessity questions through game-concept analysis.
- [ ] Route installation and project-owned Contract through project operating-system management.
- [ ] Route deployed representative flow, reconnect, persistence, failure, and target-environment evidence through Vertical Slice.
- [ ] Route static/runtime/load/failure/cost/security verification through integrated validation.
- [ ] Route AI proxy model, Prompt, quota, caching, and provider cost through the existing AI-cost Skill.
- [ ] Link the project Contract from the general Evidence Pack and documentation governance roles.
- [ ] Do not add a Registry entry, new Skill body, or shared project route.
- [ ] Run dedicated and affected route/governance tests until GREEN.
- [ ] Commit as `docs: route Cloud Run backend capability through existing owners`.

---

## Task 5: Add adversarial fixtures, learning, and propagation guards

**Files:**

- Modify: `tests/test_cloud_run_game_backend_capability.py`
- Modify: `.github/reference-freshness.json`
- Modify: `skills/managing-game-project-operating-system/LEARNING_LOG.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**

- Consumes: complete Guide/Template/routes.
- Produces: regression coverage for false suitability, duplicate mutation, cost, and readiness claims.

- [ ] Add fixture: asynchronous leaderboard API → `CLOUD_RUN_RECOMMENDED`.
- [ ] Add fixture: turn-based asynchronous battle → `CLOUD_RUN_RECOMMENDED`.
- [ ] Add fixture: WebSocket lobby/presence → `CLOUD_RUN_CONDITIONAL`.
- [ ] Add fixture: 60 Hz authoritative action battle/UDP → `ALTERNATIVE_ARCHITECTURE_REQUIRED`.
- [ ] Add fixture: offline-only feature with no shared state → `SERVER_NOT_REQUIRED`.
- [ ] Add fixture: retrying reward mutation without idempotency → blocked.
- [ ] Add fixture: provider key in client or repository → blocked.
- [ ] Add fixture: unlimited LLM proxy without quota/cost → blocked.
- [ ] Add fixture: instance-local durable save → blocked.
- [ ] Add fixture: static docs presented as runtime/load/cost proof → blocked.
- [ ] Register exact coupled-change paths in reference freshness without wildcard exemptions.
- [ ] Record why no active Skill/shared route was added and what evidence would justify future reconsideration.
- [ ] Record static versus real deployment/readiness limits in Changelog.
- [ ] Run the dedicated, aggregate, reference-freshness, documentation-governance, and protected-boundary checks.
- [ ] Commit as `test: harden Cloud Run backend capability boundaries`.

---

## Task 6: Exact-head verification and implementation PR

**Files:**

- Verify all changed files.
- Do not update BCP to `IMPLEMENTED` in this PR.

**Interfaces:**

- Consumes: complete implementation diff.
- Produces: review-ready implementation PR with truthful evidence ceilings.

- [ ] Compare exact current main and rebase/reconcile only through a non-destructive current-main integration if needed.
- [ ] Run focused tests, full required Base contract tests, proposal validation, generated/publication checks, reference freshness, Base integrity, whitespace, and protected-file hash comparison.
- [ ] Run `attack → validate-critique → regression-recheck → decision-report` against Cloud Run forcing, realtime overclaim, state loss, duplicate mutation, secret leakage, cost explosion, and AI authority.
- [ ] Confirm `skills/SKILL_REGISTRY.json`, `skills/BASE_SHARED_SKILL_ROUTES.json`, released locks, and frozen derivatives are unchanged.
- [ ] Open a separate implementation PR with exact head, RED/GREEN evidence, changed-file inventory, rollback, and explicit `NOT_RUN` states.
- [ ] Do not merge until Required `ci-gate`, unresolved threads `0`, P0/P1 `0`, and exact-head evidence are confirmed.
- [ ] After merge, run a post-merge adversarial/reference-freshness review.
- [ ] Start the entitlement/integrity implementation only from the resulting latest main.

## Definition of Done

- Guide and project Contract exist and are discoverable in one step.
- Existing Skills retain authority; no new active Skill or shared route exists.
- Cloud Run is a conditional candidate with explicit rejection paths.
- State, identity, idempotency, realtime, secrets, AI, capacity, cost, failure, rollback, and evidence ceilings are executable contract tests.
- Static CI is not reported as deployment, load, security, cost, or production evidence.
- All required exact-head gates pass and protected boundaries are unchanged.
