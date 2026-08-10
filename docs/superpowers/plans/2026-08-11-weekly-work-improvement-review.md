# Weekly Work Improvement Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable weekly work-improvement review contract that synthesizes current Base owners into the requested A/B/C/D report without creating a duplicate broad Skill.

**Architecture:** Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as discovery/evidence routing authority and introduce one non-authoritative research Template for weekly synthesis. Protect it with a focused test in the existing Evidence Knowledge workflow. Use the Watchlist as the single one-hop discovery route; do not add a second Documentation Map owner entry for an output Template.

**Tech Stack:** Markdown contracts/templates, Python `unittest`, GitHub Actions.

## Global Constraints

- Initial Base main baseline: `ba4ad067684952d987790f0ebda1a96d9554bc09`.
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
- Consumes: current Watchlist, Skill Registry, and expected Template path.
- Produces: executable contract for the weekly review shape, owner boundaries, one-hop routing, and CI inclusion.

- [x] **Step 1: Write the initial failing test**

Required contract:
- `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`;
- A/B/C/D sections and requested repeated review dimensions;
- previous-report delta and repeat-benchmark suppression;
- direct/adjacent/outside-genre benchmark decisions plus failure/mixed evidence;
- `ORIGINAL_SOURCE_BACKTRACE`, freshness/scope/sample/method/commercial-interest fields;
- Base/project routing and concrete project/consumer destinations;
- research question/method/evidence type/success criterion for experiments;
- GitHub Issue/Codex Goal/test-checklist wording;
- human/player evidence claim ceiling;
- adversarial review + PR check + no forced churn;
- no new weekly-improvement ACTIVE Skill;
- Watchlist one-hop link;
- workflow execution of the focused test.

- [x] **Step 2: Prove RED on the Draft PR**

The focused Evidence Knowledge job failed because the Template and routing were absent while existing tests remained green.

### Task 2: Minimal Template and Routing Absorption

**Files:**
- Create: `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`

**Interfaces:**
- Consumes: source scan candidate/evidence fields, BCP-020 player-experience evidence layers, game/fiction/AI/Skill existing owners.
- Produces: reusable weekly review synthesis with project/Base routing decisions.

- [x] **Step 1: Add the minimal Template**

Implemented A/B/C/D without copying domain owners. Non-material fields may use `N/A — reason` instead of filler.

- [x] **Step 2: Link from Watchlist completion reporting**

The Watchlist remains source/evidence authority and links to the weekly synthesis Template.

- [x] **Step 3: Avoid high-level map bloat**

Adversarial review rejected a separate `docs/DOCUMENTATION_MAP.md` entry because this is an output Template, not a new responsibility owner. Discoverability remains one-hop through the Watchlist.

### Task 3: Cross-Domain AI/Prompt Signal Regression

**Files:**
- Modify: `tests/test_weekly_work_improvement_review.py`
- Modify: `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`

- [x] **Step 1: Add a second failing contract**

Require explicit mapping for `PROMPT_AND_AGENT_WORKFLOW`, `SKILL_AUTHORING_AND_EVOLUTION`, material AI issues, and connected GitHub/Drive context into A/B/C/D impact rather than a news dump.

- [x] **Step 2: Prove RED**

Evidence Knowledge failed only the new cross-domain contract, confirming the omission.

- [x] **Step 3: Add minimal cross-domain mapping**

Add `connected_project_context_checked` and `cross_domain_signal` fields with `source_domain_to_report_impact: A | B | C | D`.

### Task 4: CI Execution and GREEN

**Files:**
- Modify: `.github/workflows/validate-evidence-knowledge.yml`
- Test: `tests/test_weekly_work_improvement_review.py`

- [x] **Step 1: Add focused test to workflow paths, compile, unittest, and artifact list**

Workflow permissions and existing action pins remain unchanged.

- [ ] **Step 2: Verify GREEN on final current PR head**

Confirm the Evidence Knowledge workflow and every repository check that actually runs on the final head. Do not infer skipped/unrun checks.

### Task 5: Adversarial Review and Merge Gate

- [ ] **Step 1: Attack full PR diff**

Check BCP-020 duplication, new-Skill creep, report bloat, benchmark quota gaming, project-canon leakage, causal overclaiming, human-evidence overclaiming, stale links, forced churn, AI-news dumping, connected-context staleness, and workflow consumers.

- [ ] **Step 2: Validate critique**

Reject taste-only or duplicate criticisms; keep only demonstrated gaps with an affected consumer/test.

- [ ] **Step 3: Rerun exact-head validation after the final remediation commit**

Any new commit invalidates previous exact-head evidence.

- [ ] **Step 4: Mark ready and merge only if current-head checks pass and no actionable review thread remains**

After merge, read back current `main` and confirm the Template, Watchlist route, focused test, and workflow consumer are present.
