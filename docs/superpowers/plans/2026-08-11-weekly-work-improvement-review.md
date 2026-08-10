# Weekly Work Improvement Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable weekly work-improvement review contract that synthesizes current Base owners into the requested A/B/C/D report without creating a duplicate broad Skill.

**Architecture:** Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as discovery/evidence routing authority and introduce one non-authoritative research template for weekly synthesis. Protect the contract with a focused test and run that test through the existing evidence-knowledge workflow; add one-hop discoverability through the Watchlist and Documentation Map.

**Tech Stack:** Markdown contracts/templates, Python `unittest`, GitHub Actions.

## Global Constraints

- Current Base main baseline: `ba4ad067684952d987790f0ebda1a96d9554bc09`.
- Existing Solution First and consolidation-first: no new ACTIVE Skill unless an independent responsibility/authority/validation boundary is proven.
- Preserve BCP-2026-020 owners and do not duplicate its player-experience rules.
- DISCOVERY_FEED/news/vendor benchmarks require original-source backtrace where possible and do not become canon by popularity.
- Project-specific canon, numeric values, UI layouts, story/channel direction remain project-owned.
- Actual Base changes use branch → PR → adversarial review → exact-head validation → merge gate.
- Unrun validation is reported as `NOT_RUN`, never PASS.

---

### Task 1: Contract Test — Weekly Review Shape and Boundaries

**Files:**
- Create: `tests/test_weekly_work_improvement_review.py`

**Interfaces:**
- Consumes: current Watchlist, Documentation Map, Skill Registry, and expected template path.
- Produces: executable contract for the weekly review template, routing links, no-new-Skill boundary, and CI inclusion.

- [ ] **Step 1: Write the failing test**

Create tests that require:
- `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`;
- A/B/C/D sections;
- previous-report delta and repeat-benchmark suppression;
- direct/adjacent/outside-genre benchmark decisions plus failure/mixed evidence;
- `ORIGINAL_SOURCE_BACKTRACE`, freshness/scope/sample/method/commercial-interest fields;
- `BASE_PROMOTION_CANDIDATE`, `PROJECT_ONLY`, concrete project/consumer destinations;
- research question/method/evidence type/success criterion for experiments;
- GitHub Issue/Codex Goal/test-checklist wording;
- `HUMAN_USABILITY_EVIDENCE` / `PLAYER_EXPERIENCE_EVIDENCE` claim ceiling;
- adversarial review + PR check + no forced churn;
- no new `weekly-work-improvement` ACTIVE Skill;
- Watchlist and Documentation Map one-hop links;
- workflow execution of the focused test.

- [ ] **Step 2: Run RED on the draft PR head**

Open a draft PR containing only design/plan + the failing test, then use GitHub Actions evidence to verify the test fails because the template/linkage is absent.

Expected: Evidence Knowledge workflow fails on `test_weekly_work_improvement_review.py` for missing template or required linkage.

### Task 2: Minimal Template and Routing Absorption

**Files:**
- Create: `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: source scan candidate/evidence fields, BCP-020 player-experience evidence layers, game/fiction/AI/Skill existing owners.
- Produces: reusable weekly review synthesis with project/Base routing decisions.

- [ ] **Step 1: Add the minimal template**

Implement the requested A/B/C/D structure without copying domain owners. Make non-material fields explicitly skippable with `N/A — reason` rather than forcing filler.

- [ ] **Step 2: Link from Watchlist completion reporting**

Add a one-hop instruction that weekly or cross-project synthesis may use the template after the normal scan/adversarial decision flow; the Watchlist remains source/evidence authority.

- [ ] **Step 3: Register discoverability in Documentation Map**

Add the template as a reusable report/output surface, explicitly non-canonical.

### Task 3: CI Execution and GREEN

**Files:**
- Modify: `.github/workflows/validate-evidence-knowledge.yml`
- Test: `tests/test_weekly_work_improvement_review.py`

**Interfaces:**
- Consumes: focused contract test.
- Produces: PR-triggered evidence that future edits cannot silently drop the weekly review contract.

- [ ] **Step 1: Add focused test to workflow paths, compile, unittest, and artifact list**

Do not change workflow permissions or action pins.

- [ ] **Step 2: Verify GREEN on current PR head**

Wait for the exact-head workflows to complete. Confirm the Evidence Knowledge workflow and any repository-required checks that actually ran are successful; do not infer skipped/unrun checks.

### Task 4: Adversarial Review and Merge Gate

**Files:**
- Review entire PR diff plus same-owner untouched consumers.

**Interfaces:**
- Consumes: PR diff, current main, BCP-020, Watchlist, active Skill map, workflow/check evidence.
- Produces: attack/critique validation, minimal remediation if needed, exact-head merge decision.

- [ ] **Step 1: Attack**

Check for BCP-020 duplication, new-Skill creep, report bloat, benchmark quota gaming, project-canon leakage, causal overclaiming, human-evidence overclaiming, stale links, forced weekly churn, and missing workflow consumer.

- [ ] **Step 2: Validate critique**

Reject taste-only or duplicate criticisms; keep only demonstrated gaps with an affected consumer/test.

- [ ] **Step 3: Apply approved minimal fixes and rerun exact-head validation**

Any new commit invalidates previous exact-head evidence.

- [ ] **Step 4: Mark ready and merge only if current-head checks pass and no actionable review thread remains**

After merge, read back current `main` and confirm the template, Watchlist link, Documentation Map route, and test are present.
