# Base P3 Repository Governance Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:test-driven-development` for implementation, `superpowers:requesting-code-review` before publication, and `superpowers:verification-before-completion` before any success claim.

**Goal:** Add a truthful, low-noise repository governance baseline for reuse rights, security reporting, code ownership, and dependency maintenance.

**Architecture:** Four small GitHub-standard files form the human/platform surface. A mutable Base governance profile owns current repository identity while released locks remain frozen history. A standard-library semantic regression rejects duplicates, owner drift, unsupported scope claims, and ecosystem/manifest mismatch. Unconditional docs validation and conditional contract CI both run that regression.

**Baseline:** `main@4f49f1ed30d7f849417fb936fb1d5ab70ea8217f` on `codex/base-p3-repository-governance`.

## Constraints

- Preserve Registry bytes, released locks, generated Base artifacts, plugin metadata, project repositories, Sheets, game code, and assets.
- Do not claim private reporting, Dependabot execution, CODEOWNERS review requests, or Ruleset enforcement before GitHub evidence exists.
- Do not add a fake security email or organization team.
- Do not auto-merge dependency updates.
- Keep license choice and third-party notices distinct.

## Task 1: Freeze the missing baseline as RED

**Files:**

- Create: `tests/test_repository_governance_baseline.py`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Create: `docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`
- Modify: `templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`

- [x] Assert unique supported locations for LICENSE, SECURITY, CODEOWNERS, and Dependabot config.
- [x] Assert MIT identity/terms, security scope/reporting boundary, repository-owner CODEOWNERS, supported Dependabot ecosystems, and the explicit pnpm 11 deferral.
- [x] Add the regression to canonical compile and contract test lists.
- [x] Add the regression to unconditional docs validation and prove docs-only governance paths cannot bypass it.
- [x] Source current CODEOWNERS identity from the mutable repository profile rather than a frozen release lock.
- [x] Add the current owner field to the reusable project governance profile contract.
- [x] Run focused RED and confirm failures are missing surfaces, not test syntax.

## Task 2: Implement the four platform surfaces

**Files:**

- Create: `LICENSE`
- Create: `SECURITY.md`
- Create: `.github/CODEOWNERS`
- Create: `.github/dependabot.yml`

- [x] Add the canonical MIT text for `2026 alsdmlals4-eng`.
- [x] Add supported-version, private-reporting, response-expectation, scope, and setting-evidence boundaries.
- [x] Add default and self-owning `.github/` ownership for `@alsdmlals4-eng`.
- [x] Add weekly staggered pip/GitHub Actions updates, minor/patch grouping, bounded open PRs, and a fail-closed pnpm 11 deferral.
- [x] Run focused GREEN.

## Task 3: Connect documentation without duplicating authority

**Files:**

- Modify: `README.md`
- Modify: `docs/GITHUB_PRO_OPERATING_POLICY.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

- [x] Link License and Security from README.
- [x] Record the four surfaces and settings-versus-file evidence boundary in the repository policy and Documentation Map.
- [x] Record the completed structural change and its unrun platform behaviors.
- [x] Run focused documentation and governance regressions.

## Task 4: Adversarial verification and publication

- [ ] Attack duplicate precedence files, fake owners/teams, missing manifests, extra ecosystems, grouped major updates, public vulnerability disclosure, and false setting claims.
- [ ] Obtain independent Critical/Important review and close every accepted finding.
- [ ] Run canonical local validation with the exact trusted baseline SHA.
- [ ] Run reference freshness, whitespace, Git object, protected-path, Registry/release, and generated-artifact checks.
- [ ] Publish an exact-tree Draft PR, verify GitHub consumes `dependabot.yml`, exact-head Actions, review threads, and `ci-gate`, then exact-head squash merge only if every gate passes.
