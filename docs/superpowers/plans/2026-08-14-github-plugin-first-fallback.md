# GitHub Plugin-First Fallback Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent Base-guided work from stopping solely because GitHub CLI or its local authentication is missing when a connected GitHub plugin can perform the required operation.

**Architecture:** Keep `synchronizing-local-and-github-state` as the single operational owner. Add one contract test that binds the Skill, Base-wide invariant, Registry routing, and learning evidence; then make the smallest policy edits that satisfy it without weakening existing concurrent-change or exact-SHA gates.

**Tech Stack:** Markdown Skill contracts, JSON Skill Registry, Python `unittest`, GitHub connector and Git object APIs.

## Global Constraints

- Do not create a second GitHub publication Skill.
- Do not copy or persist user GitHub credentials in a cloud container.
- Do not weaken no-force-push, concurrent-change, PR review, CI, or exact-SHA verification.
- Missing `gh` alone is not a blocker when connector coverage exists.

---

### Task 1: Bind the connector fallback contract

**Files:**
- Create: `tests/test_github_connector_fallback_policy.py`
- Modify: `skills/synchronizing-local-and-github-state/SKILL.md`
- Modify: `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: existing `synchronizing-local-and-github-state` routing and concurrent-write preflight.
- Produces: a discoverable `GITHUB_CAPABILITY_FALLBACK` contract and routing triggers for missing CLI/authentication.

- [ ] **Step 1: Write the failing policy test**

Require the Skill to contain `GITHUB_CAPABILITY_FALLBACK`, `github_connector`, `local_git`, `gh_cli`, `MISSING_OPTIONAL_CLI`, `BLOCKED_UNVERIFIED`, non-force Git-object publication, and a prohibition on repeated user re-authentication when connector coverage exists. Require matching Base-wide, Registry-trigger, and learning-log evidence.

- [ ] **Step 2: Run the test and verify RED**

Run: `python -m unittest tests.test_github_connector_fallback_policy -v`

Expected: FAIL because the current Skill has no plugin-first capability contract.

- [ ] **Step 3: Implement the minimal policy**

Add the capability decision order and exact blocking boundary to the existing Skill. Add only one summary invariant to `AGENTS.md`, three routing triggers and related review triggers to the Registry entry, and one incident entry to the Skill learning log.

- [ ] **Step 4: Run focused and neighboring tests**

Run:

```bash
python -m unittest \
  tests.test_github_connector_fallback_policy \
  tests.test_concurrent_git_sync_preflight_contract \
  tests.test_skill_routing_governance \
  tests.test_skill_package_integrity -v
```

Expected: PASS.

- [ ] **Step 5: Run Base validation and inspect generated drift**

Run `python tools/run_local_validation.py` when available in the environment, followed by `git diff --check` and `git status --short`. If a generated Registry consumer is stale, regenerate it only with the repository-owned generator and include the resulting focused diff.

- [ ] **Step 6: Commit, publish through the GitHub connector, and validate PR CI**

Commit the verified files. If authenticated `git push` is unavailable, create the remote branch and verified commit through connector Git-object writes, open a draft PR, wait for required checks, then merge only at the reviewed exact head SHA.
