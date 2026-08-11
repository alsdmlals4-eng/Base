# GitHub + Solo Game-Dev Source Seeds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add GitHub repository discovery and solo game-development YouTube seeds, starting with `@zang_gamedev`, to the active periodic research intake with Shorts/long-form evidence boundaries.

**Architecture:** Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as the durable source-policy owner. Add one bounded active-discovery addendum for user-nominated or platform-wide seeds that should be scanned now but are not yet justified as permanent Operations Ledger source families. Wire a focused regression into the existing Evidence Knowledge workflow.

**Tech Stack:** Markdown source contracts, Python `unittest`, GitHub Actions.

## Global Constraints

- Existing Solution First; no new ACTIVE Skill.
- GitHub hosting/popularity is not evidence authority.
- `@zang_gamedev` is a user-nominated active seed; current channel corpus details remain `BLOCKED_UNVERIFIED` until actually scanned.
- Shorts and long-form remain separate evidence contexts.
- Additional solo-dev channels require the existing new-site gate before durable Watchlist/Ledger promotion.
- No workflow permission, trigger topology, Ruleset, Required Check name, or scheduler cadence change.

---

### Task 1: RED contract for source seeds

**Files:**
- Create: `tests/test_periodic_external_source_discovery_seeds.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`

**Interfaces:**
- Consumes: existing Watchlist source-role/new-site-gate semantics.
- Produces: a focused CI contract requiring the active seed addendum and its authority boundaries.

- [ ] **Step 1: Write failing regression**

Require the addendum to contain GitHub repository discovery, `@zang_gamedev`, `ACTIVE_DISCOVERY_SEED`, explicit Shorts/long-form handling, no popularity authority, `BLOCKED_UNVERIFIED`, and promotion through the existing Watchlist/Ledger gate.

- [ ] **Step 2: Wire the test into Evidence Knowledge CI**

Add the test file to workflow path filters, `py_compile`, `unittest`, and diagnostic artifacts without changing permissions, triggers, jobs, or Required Check topology.

- [ ] **Step 3: Run through PR CI**

Expected RED: the focused test fails because `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md` does not yet exist.

---

### Task 2: Add the active discovery seeds

**Files:**
- Create: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

**Interfaces:**
- Consumes: Watchlist roles, Evidence tiers, `ORIGINAL_SOURCE_BACKTRACE`, new-site gate, Existing Solution First.
- Produces: active scan inputs for GitHub and solo-development YouTube.

- [ ] **Step 1: Add GitHub discovery contract**

Define repository search/releases/tags/issues/PRs/discussions/examples as discovery surfaces. State that stars/forks/trending do not raise authority and that official upstream identity/version/release must be verified before primary-source use.

- [ ] **Step 2: Add `@zang_gamedev` seed**

Record the exact channel URL as user-nominated and active. Do not invent channel statistics or project facts that were not fetched.

- [ ] **Step 3: Separate Shorts and long-form**

Use Shorts for rapid discovery/visual progress signals and long-form for deeper rationale/process context; require format-aware comparison and follow-up to primary sources when claims matter.

- [ ] **Step 4: Define expansion gate**

Allow additional solo/small-team creator channels only through repeat-value/overlap/commercial-interest/source-access/owner-consumer checks. No creator quota or popularity-based authority.

---

### Task 3: Adversarial PR validation

**Files:**
- Review all PR-changed files.

**Interfaces:**
- Consumes: current PR diff, same-goal PR search, current main, CI and review-thread state.
- Produces: `OMISSION / CONFLICT / COMPLEMENT_GAP / DUPLICATE_WORK / NO_MATERIAL_FOLLOWUP` decision.

- [ ] **Step 1: Attack overlap**

Confirm generic GitHub discovery does not duplicate `github-platform-engineering` or `github-copilot` authority owners.

- [ ] **Step 2: Attack creator overgeneralization**

Reject subscriber/view-count authority, single-creator universal rules, Shorts-vs-long metric laundering, and unverified channel claims.

- [ ] **Step 3: Verify exact head**

Require Evidence Knowledge, Base v9, Game Project OS/final `ci-gate`, zero unresolved review threads, latest-main compatibility and same-goal PR recheck.

- [ ] **Step 4: Merge and post-merge recheck**

Use expected-head squash merge only if all gates remain valid; then re-read the new main seed file and recheck same-goal PRs/canon.