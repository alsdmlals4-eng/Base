# Integrated Vertical Slice Prompt v7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the split v6 reference/short-prompt workflow with one attachment-ready, interview-driven v7 integrated execution prompt while extending the existing adversarial review system to audit repository-wide omissions, stale active contracts, and untouched consumers.

**Architecture:** Preserve the detailed v6 source material in a single canonical prompt template, but subordinate it to current Base/project canon and replace stale `CORE_POC` product-stage behavior with `DEMO_FIRST_VERTICAL_SLICE` plus optional in-slice `TECHNICAL_SPIKE`. Do not create a duplicate broad Skill; add a `repository-wide-audit` mode and focused protocol to the existing adversarial review Skill, then register and regression-test the propagation path.

**Tech Stack:** Markdown canonical contracts and templates, JSON Skill Registry, Python `unittest`, GitHub Actions contract/reference/publication validation.

## Global Constraints

- Base repository Google Sheets state is `BASE_EXCLUDED`; only configured project Sheets are synchronized.
- No numeric line, character, page, or size ceiling may remove required content.
- Every L1+ task starts with duplicate, omission, conflict, stale-reference, and missing-consumer audit.
- Important design decisions use benchmark, player-response, and professional/official evidence.
- The default product path is `CONCEPT_APPROVAL → DEMO_FIRST_VERTICAL_SLICE → DEMO_VALIDATION → PRODUCTION_APPROVAL`.
- `CORE_POC` is not a standalone required Gate; only a bounded `TECHNICAL_SPIKE` inside the demo program is allowed when a technical uncertainty blocks the demo.
- Historical PRs, changelogs, migration notes, and compatibility explanations may retain old terms when explicitly classified as history or compatibility.
- One integrated prompt file replaces the v6 master-plus-short-prompt attachment workflow.
- No new broad Skill is added unless the existing adversarial-review, reference-freshness, legacy-governance, and operating-system Skills cannot own the responsibility.

---

### Task 1: Freeze the Baseline and Add Failing v7 Contract Tests

**Files:**
- Create: `tests/test_integrated_vertical_slice_prompt_v7.py`
- Create: `docs/superpowers/plans/2026-07-28-integrated-vertical-slice-prompt-v7.md`

**Interfaces:**
- Consumes: current `main` at `b3dd5cbdf9e6c54a6a75af59cec3e5f0aa65c9af`, attached v6 master and short prompt.
- Produces: executable assertions for the v7 integrated prompt, repository-wide adversarial mode, registry routing, and active stale-token handling.

- [ ] **Step 1: Record the baseline and duplicate-work audit in the plan.**
- [ ] **Step 2: Write tests that require `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`.**
- [ ] **Step 3: Assert the prompt contains interview routing, Base/project precedence, `BASE_EXCLUDED`, the eight-step work loop, Evidence Pack, Approval Bundle, Demo-First Gate, repository-wide audit, GPT→Codex handoff, and final coverage reports.**
- [ ] **Step 4: Assert the prompt does not make `PROTOTYPE_AND_VERTICAL_SLICE`, `CORE_POC`, `SLICE_VALIDATION`, or a separate short prompt current authority.**
- [ ] **Step 5: Assert `running-adversarial-review-and-refinement` exposes `repository-wide-audit` and links its focused reference.**
- [ ] **Step 6: Open a draft PR and run CI to observe the tests fail because the new prompt and mode do not yet exist.**

### Task 2: Create the Single Integrated v7 Prompt

**Files:**
- Create: `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`
- Modify: `templates/project-operations/README.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `START_HERE.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: attached `VERTICAL_SLICE_MASTER_REFERENCE_v6(2).md`, attached short prompt, current `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`, current Vertical Slice Gate/Skill contracts.
- Produces: one attachment-ready prompt that conducts its own repository-first interview and routes to current Base/project canon.

- [ ] **Step 1: Replace the v6 split-file usage model with one integrated-file usage contract.**
- [ ] **Step 2: Preserve detailed v6 design, system, UX, asset, release, review, handoff, and coverage sections.**
- [ ] **Step 3: Replace stale product-stage behavior with `DEMO_FIRST_VERTICAL_SLICE`, `DEMO_VALIDATION`, and bounded `TECHNICAL_SPIKE`.**
- [ ] **Step 4: Add current preflight order: latest main, decisions, canon, related PRs, actual files, configured project Sheet, duplicate/omission/conflict result.**
- [ ] **Step 5: Add interview rules that ask only unresolved user-owned decisions and do not repeat repository-resolvable questions.**
- [ ] **Step 6: Add the approved planning sequence and project Sheet tab order.**
- [ ] **Step 7: Add prompt-drift handling: current Base/project canon overrides the attached prompt and stale clauses are reported as `STALE_PROMPT_CONTRACT`.**
- [ ] **Step 8: Register the prompt in entrypoints and template documentation.**

### Task 3: Extend Existing Adversarial Review Instead of Adding a Duplicate Skill

**Files:**
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Create: `skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: `auditing-canonical-reference-freshness`, `governing-legacy-retention-and-archives`, `reviewing-and-validating-project-changes`.
- Produces: `repository-wide-audit` orchestration that maps authority, inventories active/history/derivative files, attacks stale and untouched consumers, validates criticism, routes legacy handling, applies approved minimal fixes, and rechecks regressions.

- [ ] **Step 1: Add `repository-wide-audit` as an explicit mode and trigger.**
- [ ] **Step 2: Define authority classes: current canon, active consumer, template, derivative, compatibility, history, archive, test fixture, placeholder, unresolved.**
- [ ] **Step 3: Define search and attack lenses for stale active policy, duplicate authority, orphan references, untouched consumers, derivative drift, and superseded Decision revival.**
- [ ] **Step 4: Route file lifecycle decisions to legacy governance and reference changes to reference freshness rather than duplicating those procedures.**
- [ ] **Step 5: Add output and closure criteria including `ALLOWED_LEGACY` and `BLOCKED_UNVERIFIED`.**
- [ ] **Step 6: Update Registry and Learning Log companion records.**

### Task 4: Reconcile Active v6-Era Contracts and Validate Propagation

**Files:**
- Modify: `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md`
- Modify: `docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md`
- Modify: `tests/test_vertical_slice_v6_contract.py`
- Modify: `tests/test_integrated_vertical_slice_prompt_v7.py`

**Interfaces:**
- Consumes: repository-wide search results for `CORE_POC`, `PROTOTYPE_AND_VERTICAL_SLICE`, `SLICE_VALIDATION`, and old prompt filenames.
- Produces: active documents that use Demo-First terminology while preserving explicitly labeled historical/compatibility evidence.

- [ ] **Step 1: Classify every search hit as active stale, current compatibility explanation, plan/history, or test fixture.**
- [ ] **Step 2: Replace active stale execution flow in Skill orchestration with Demo-First flow and optional internal Spike.**
- [ ] **Step 3: Convert v6 coverage from a current v6 authority claim into a migration/traceability record pointing to the v7 integrated prompt and current Base canon.**
- [ ] **Step 4: Keep compatibility assertions only where they explicitly prove old terms are non-authoritative.**
- [ ] **Step 5: Re-run code search and require no old term to act as an unlabeled current Gate.**
- [ ] **Step 6: Run contract, reference-freshness, documentation, and publication/generation validation.**

### Task 5: PR Review, Merge, Post-Merge Adversarial Loop, and User Artifact

**Files:**
- Update as required by validated findings only.
- Generate: `/mnt/data/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`

**Interfaces:**
- Consumes: PR diff, CI evidence, new `main`, current Decision/canon, open/recent PRs.
- Produces: merged Base contract and a downloadable Markdown file identical to the repository template.

- [ ] **Step 1: Run pre-merge adversarial review on requirements, active authority, untouched consumers, stale prompt terms, and duplicate Skills.**
- [ ] **Step 2: Apply only validated `MUST_FIX` and approved in-scope `SHOULD_FIX` findings.**
- [ ] **Step 3: Require all applicable CI jobs and `ci-gate` to pass.**
- [ ] **Step 4: Squash merge and verify the new `main` HEAD.**
- [ ] **Step 5: Run post-merge repository-wide adversarial review and search for duplicate PRs and residual work branches.**
- [ ] **Step 6: Materialize the exact merged prompt into `/mnt/data` and verify its hash/content markers before linking it to the user.**
