# Game Entitlement, Integrity, and DRM Capability Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task. Use `superpowers:systematic-debugging` for unexpected failures and `superpowers:verification-before-completion` before completion claims. Execute only after the Cloud Run Capability Pack implementation is merged and current main is re-read.

**Goal:** Add a reusable Base Guide and project Record for platform entitlement, app/build/request integrity, server-authoritative value, optional local tamper resistance, offline/outage handling, false-positive remediation, and service-sunset continuity without claiming perfect anti-piracy.

**Architecture:** Keep platform and project implementation under existing owners. Add one Guide, one project Record, dedicated tests, and release/evidence routes. Preserve platform-specific meanings rather than collapsing Steam, Google Play, STOVE, and other systems into a false universal verdict.

**Tech Stack:** Markdown contracts/templates, JSON documentation governance/reference-freshness configuration, Python `unittest`, existing release-compliance/evidence packs, GitHub Actions.

**Approved source:** `BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity`

**Approval reference:** `https://github.com/alsdmlals4-eng/Base/pull/170#issuecomment-5192884554`

**Sequencing:** This is implementation PR B. Start from latest main after PR A is merged and post-merge verified. Do not stack both implementations because they share technical/release Guides, operating Skill, Validation Skill, Evidence Pack, documentation governance, test imports, Learning Log, Changelog, and reference-freshness configuration.

## Global Constraints

- Preserve `skills/SKILL_REGISTRY.json` bytes and active Skill count.
- Do not modify `skills/BASE_SHARED_SKILL_ROUTES.json`.
- `PLATFORM_NATIVE_FIRST` and `NO_CUSTOM_DRM_DEFAULT` are mandatory.
- Do not claim perfect piracy prevention, legal clearance, platform approval, zero false positives, or production readiness.
- Do not create platform accounts, SDK credentials, signing keys, license servers, secrets, or project code.
- One unavailable or negative integrity signal may not directly cause permanent ban, purchase denial, or save deletion.
- Preserve offline/outage, reauthentication, support/appeal, account recovery, save access, and service-sunset decisions.
- Keep raw platform/device/integrity data minimized and retention-purpose bound.
- Every task must preserve RED → GREEN → refactor → commit.

---

## Task 1: Re-synchronize authority after Cloud Run implementation

**Files:**

- Read: current merged Cloud Run Guide, Template, tests, routes, and Learning Log.
- Read: approved BCP Proposal and Design.
- Read: `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- Read: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`

**Interfaces:**

- Consumes: latest main and completed PR A.
- Produces: conflict-free PR B baseline and protected-file hashes.

- [ ] Confirm PR A is merged and post-merge reference/adversarial review has no P0/P1 finding.
- [ ] Search open/recent PRs for the entitlement Guide, Record, or same-goal platform-integrity work.
- [ ] Create `agent/implement-game-entitlement-integrity-drm-capability` from exact latest main.
- [ ] Record hashes for Skill Registry, shared routes, released locks, frozen derivatives, Cloud Run artifacts, and shared entrypoints.
- [ ] Run baseline proposal, release-compliance, technical Guide, aggregate import, reference-freshness, and Base integrity tests.
- [ ] Stop and separate any pre-existing failure.

---

## Task 2: Write the dedicated failing entitlement/integrity tests

**Files:**

- Create: `tests/test_game_entitlement_integrity_drm_capability.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`

**Interfaces:**

- Consumes: approved Design and platform evidence boundaries.
- Produces: RED contract for Guide, Record, routes, and non-harm safeguards.

- [ ] Require new artifacts:
  - `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`
  - `templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md`
- [ ] Require core tokens:
  - `PLATFORM_NATIVE_FIRST`
  - `NO_CUSTOM_DRM_DEFAULT`
  - `SERVER_AUTHORITY_FOR_HIGH_VALUE_STATE`
  - `REQUEST_BINDING_AND_REPLAY_CONTROL`
  - `TIERED_REMEDIATION`
  - `OFFLINE_AND_OUTAGE_POLICY`
  - `PLAYER_HARM_REVIEW`
  - `PLATFORM_CAPABILITY_UNVERIFIED`
- [ ] Require trust Tiers 0–5 from client claim through multi-signal/human review.
- [ ] Require platform adapter fields for account, product/package, entitlement, app/device integrity, request binding, issued/expiry, replay, raw-signal retention, normalized decision, and remediation.
- [ ] Require Steam DRM Wrapper limitations and forbid perfect anti-piracy claims.
- [ ] Require Google Play backend verification, `requestHash` or current official binding, replay protection, quota/error/remediation, and no one-verdict permanent punishment.
- [ ] Require STOVE and unsupported platforms to remain explicitly unverified until official SDK/account evidence is checked.
- [ ] Require server authority for purchase-linked entitlement, currency/trade, competitive score/rank, reward achievements, asynchronous battle result, online inventory, and limited claims.
- [ ] Require offline, cached entitlement, grace period, outage, recovery, device change, refund/revocation, save export, sunset, support, and appeal fields.
- [ ] Require privacy minimization and purpose/retention controls for raw integrity/device signals.
- [ ] Require project Record sections for threat model, protected value, signal sources, server authority, local protection, offline/outage, false positives, privacy, sunset, evidence, and remaining gates.
- [ ] Assert no new active Skill, no shared route, no universal platform verdict, and no legal/platform-approval claim.
- [ ] Import the dedicated test in both aggregate test modules.
- [ ] Run focused tests and observe RED only for missing approved artifacts/routes.
- [ ] Commit as `test: define game entitlement and integrity capability contract`.

---

## Task 3: Implement the minimal entitlement/integrity Guide and Record

**Files:**

- Create: `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`
- Create: `templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md`

**Interfaces:**

- Consumes: RED tests and approved platform boundaries.
- Produces: layered protection Guide and project-owned evidence Record.

- [ ] Define entitlement, integrity, DRM, tamper resistance, server authority, and evidence state separately.
- [ ] Define trust Tiers 0–5 and when high-value actions require higher tiers.
- [ ] Define platform-specific adapters that preserve unsupported/unknown fields instead of fabricating parity.
- [ ] Define Steam ownership/launch integration and Wrapper limitations.
- [ ] Define Google Play App Signing/Integrity evaluation, backend verification, request binding, replay handling, quota/errors, and remediation.
- [ ] Define STOVE/other platforms as official-evidence-required and allow `PLATFORM_CAPABILITY_UNVERIFIED`.
- [ ] Define server recomputation, ranges, resource version, transactions, double-spend, idempotency, replay, audit, rollback, and support for high-value state.
- [ ] Define optional local protection—signing, package encryption, obfuscation, checksum/signature, debugger/tamper detection—as cost-raising support rather than authority.
- [ ] Define client secrets as extractable and avoid excessive protection where local single-player modification does not harm others/economy/competition.
- [ ] Define offline, first-launch, cached entitlement, TTL, clock tamper, grace, platform/backend outage, recovery, device change, refund, save export, sunset, and appeal decisions.
- [ ] Define tiered remediation from retry/degraded mode through temporary restriction and evidence-backed severe action.
- [ ] Write the project Record with explicit `UNKNOWN`, `UNVERIFIED`, `NOT_APPLICABLE`, and evidence-state fields.
- [ ] Run dedicated tests; only route/discovery assertions may remain RED.
- [ ] Refactor duplicated prose without weakening platform-specific or player-harm boundaries.
- [ ] Commit as `feat: add game entitlement and integrity capability pack`.

---

## Task 4: Connect release, technical, operating, and validation owners

**Files:**

- Modify: `docs/knowledge/game-development/README.md`
- Modify: `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`
- Modify: `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `START_HERE.md`
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/designing-vertical-slices/SKILL.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Modify: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- Modify: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`
- Modify: `templates/project-operations/github/documentation-governance.json`

**Interfaces:**

- Consumes: Guide and Record.
- Produces: one-step discovery and evidence-linked release/production routes.

- [ ] Add knowledge-hub and Documentation Map entries without duplicating the Guide.
- [ ] Add a compact START_HERE route for entitlement, platform integrity, DRM, anti-tamper, offline license, or server-authoritative value questions.
- [ ] Route Record installation and project ownership through project operating-system management.
- [ ] Route SDK/platform/native feature evaluation through existing asset/plugin evaluation rather than a new Skill.
- [ ] Route representative entitlement/offline/outage/player recovery flow through Vertical Slice.
- [ ] Route signal verification, server authority, replay, privacy, failure, false-positive, and regression evidence through integrated validation.
- [ ] Link entitlement/integrity status from the release Compliance Pack without merging it with asset-rights provenance.
- [ ] Link the project Record from the general Evidence Pack and documentation governance roles.
- [ ] Preserve current Cloud Run routes and avoid conflicting ownership.
- [ ] Run dedicated, release-compliance, route, governance, and aggregate tests until GREEN.
- [ ] Commit as `docs: route entitlement and integrity capability through existing owners`.

---

## Task 5: Add platform, abuse, false-positive, and sunset adversarial fixtures

**Files:**

- Modify: `tests/test_game_entitlement_integrity_drm_capability.py`
- Modify: `.github/reference-freshness.json`
- Modify: `skills/managing-game-project-operating-system/LEARNING_LOG.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**

- Consumes: complete Guide/Record/routes.
- Produces: regression coverage for false platform parity and legitimate-player harm.

- [ ] Fixture: Steam single-player entitlement with graceful offline behavior.
- [ ] Fixture: Google Play competitive score submit with request-bound backend verification.
- [ ] Fixture: client-only currency/inventory mutation → blocked.
- [ ] Fixture: one unavailable or negative integrity signal → permanent ban prohibited.
- [ ] Fixture: repeated multi-signal abuse → temporary restriction/review, not automatic irreversible deletion.
- [ ] Fixture: platform outage → retry/degraded/read-only/grace path required.
- [ ] Fixture: service sunset → offline fallback or save/data export decision required.
- [ ] Fixture: raw device/integrity signal retained without purpose/TTL → blocked.
- [ ] Fixture: STOVE capability copied from Steam/Google without official evidence → `PLATFORM_CAPABILITY_UNVERIFIED`.
- [ ] Fixture: Wrapper/obfuscation described as perfect anti-piracy → blocked.
- [ ] Fixture: local single-player modding with no external harm → excessive DRM must be challenged.
- [ ] Register exact coupled-change paths in reference freshness without wildcard exemptions.
- [ ] Record why the Capability Pack is not a legal clearance, platform approval, or piracy-proof claim.
- [ ] Record human false-positive/recovery and real platform sandbox evidence as `HUMAN_NOT_RUN`/`NOT_RUN` until executed.
- [ ] Run dedicated, aggregate, release-compliance, reference-freshness, and protected-boundary checks.
- [ ] Commit as `test: harden entitlement and integrity player safeguards`.

---

## Task 6: Exact-head verification and implementation PR

**Files:**

- Verify all changed files.
- Do not mark the BCP `IMPLEMENTED` until both Capability Packs are merged and lifecycle evidence is linked.

**Interfaces:**

- Consumes: complete implementation diff and merged PR A.
- Produces: review-ready PR B with truthful platform and human evidence limits.

- [ ] Re-read latest main and integrate any concurrent disjoint changes without replacing shared files.
- [ ] Run focused tests, all affected release/technical/operating tests, proposal validation, publication/generation, reference freshness, Base integrity, whitespace, and protected-file hashes.
- [ ] Run `attack → validate-critique → regression-recheck → decision-report` against perfect-DRM claims, false platform parity, client authority, replay/double spend, irreversible one-signal punishment, outage lockout, excessive data retention, and no-sunset design.
- [ ] Confirm Skill Registry, shared routes, released locks, frozen derivatives, Cloud resources, project files, and Google Sheets remain unchanged.
- [ ] Open a separate implementation PR with exact head, RED/GREEN evidence, official-source check date, changed-file inventory, rollback, and explicit runtime/platform/human `NOT_RUN` states.
- [ ] Merge only after Required `ci-gate`, unresolved threads `0`, P0/P1 `0`, and exact-head evidence.
- [ ] Run post-merge adversarial/reference-freshness review.
- [ ] Only then create a small lifecycle PR that links both implementation PRs and decides whether BCP-2026-007 can become `IMPLEMENTED`.

## Definition of Done

- Guide and project Record exist and are discoverable in one step.
- Platform-specific meanings and unknown states are preserved.
- High-value state has explicit server-authority, transaction, idempotency, replay, audit, and rollback rules.
- Offline/outage, false-positive remediation, recovery, privacy, support/appeal, save access, and sunset are mandatory decisions.
- Perfect anti-piracy, legal clearance, platform approval, zero false positives, and production readiness are not claimed.
- Existing Skills retain authority; no active Skill or shared route is added.
- All required exact-head gates pass and protected boundaries are unchanged.
