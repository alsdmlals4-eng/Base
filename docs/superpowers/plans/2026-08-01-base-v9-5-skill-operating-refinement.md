# Base v9.5 Skill Operating Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an unreleased v9.5 maintenance candidate that clarifies release authority, reduces Skill discovery metadata, adds behavior-evaluation infrastructure, and integrates Issue #74 into existing workflows.

**Architecture:** Preserve every released lock and the current Registry bytes. Add a deterministic evaluation fixture and scorer, then make minimal documentation and Skill-body changes whose behavior is protected by focused and full regression tests.

**Tech Stack:** Python 3, unittest, JSON Schema Draft 2020-12, Markdown, Git.

## Global Constraints

- Base v9.4 remains the latest released compatible line.
- Do not modify `skills/SKILL_REGISTRY.json`, released lock/evidence identity, project repositories, Google Sheets, product code, or v7/v8 compatibility prompts.
- Do not claim model behavior passed without scored external result files.
- Use `apply_patch` for authored file changes and preserve unrelated untracked `.venv` and temporary directories.

---

### Task 1: Add the failing v9.5 contract test

**Files:**
- Create: `tests/test_base_v9_5_skill_operating_refinement.py`

**Interfaces:**
- Consumes: active Registry, Skill frontmatter, release/version docs, future eval fixture and checker.
- Produces: executable acceptance contract for Tasks 2-5.

- [x] **Step 1: Write tests for the approved behaviors**

Cover discovery metadata `<= 8000`, unchanged Registry hash, authority wording, v9.4 adoption status, Changelog hierarchy, Issue #74 contract terms, eval fixture schema, and scorer rejection paths.

- [x] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_base_v9_5_skill_operating_refinement -v`

Expected: failures for missing eval files, over-budget descriptions, and missing contract wording.

### Task 2: Implement deterministic behavior-eval infrastructure

**Files:**
- Create: `schemas/skill-behavior-eval-v1.schema.json`
- Create: `skills/SKILL_BEHAVIOR_EVALS.json`
- Create: `tools/check_skill_behavior_evals.py`

**Interfaces:**
- Consumes: `skills/SKILL_REGISTRY.json`, active Skill package paths, optional result JSON.
- Produces: `validate_contract(root) -> list[str]` and `score_results(root, results_path) -> list[str]`.

- [x] **Step 1: Define the schema and realistic cases**

Include at least eight Korean prompts without literal Skill IDs. Each case declares expected Work Mode, primary/supporting Skill IDs, modes, forbidden Skill IDs, required evidence, and user-decision state.

- [x] **Step 2: Implement contract validation**

Validate JSON Schema, unique case IDs/prompts, Registry membership, real package paths, single primary Skill, non-leaking prompts, and positive/negative/boundary/cross-skill coverage.

- [x] **Step 3: Implement optional result scoring**

Reject missing/extra/forbidden Skills, wrong Work Mode or primary Skill, missing modes/evidence, and wrong decision state. Print `MODEL_RUN_STATUS: NOT_RUN` when no result file is supplied.

- [x] **Step 4: Run the focused test**

Run: `python -m unittest tests.test_base_v9_5_skill_operating_refinement -v`

Expected: eval tool tests pass; documentation and budget tests may still fail.

### Task 3: Compress Skill discovery descriptions

**Files:**
- Modify: all active `skills/*/SKILL.md` frontmatter descriptions
- Modify: `skills/evolving-project-discipline-skills/SKILL.md`

**Interfaces:**
- Consumes: current Registry triggers and existing Skill bodies.
- Produces: trigger-only `Use when...` descriptions and `behavior-eval` mode.

- [x] **Step 1: Shorten descriptions without changing names or bodies**

Retain distinctive trigger terms and move no safety contract out of the body.

- [x] **Step 2: Add the behavior-eval mode**

Define inputs, baseline/result scoring, false-claim boundary, output, and learning handoff in the existing Skill evolution package.

- [x] **Step 3: Verify the budget and package integrity**

Run: `python -m unittest tests.test_base_v9_5_skill_operating_refinement tests.test_skill_package_integrity -v`

Expected: all tests pass and discovery metadata is at most 8,000 characters.

### Task 4: Integrate Issue #74 and repair authority documentation

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Modify: `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- Modify: `templates/project-operations/SKILL_EXECUTION_REPORT.md`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `docs/operations/BASE_V9_4_RELEASE_CONTRACT.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/SKILL_COVERAGE_MAP.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Issue #74, released v9.4 evidence, current merge policy, v9.0 frozen artifacts.
- Produces: testable hypothesis/decomposition/review/report contracts and unambiguous authority text.

- [x] **Step 1: Add Build-Measure-Learn and element decomposition**

Add hypothesis, minimal test unit, observation, thresholds, evidence decision, element purpose, interface, integration, and learning output fields.

- [x] **Step 2: Add review lenses and E2E paths**

Require applicable/omitted decisions for Simplify, Style Guide, Domain Review, Security/Safety/Trust Boundary, plus Golden Path, Edge, and Regression evidence.

- [x] **Step 3: Correct release and merge-policy wording**

Separate v9.0 baseline, released v9.4, current Registry, and frozen v9.0 derivatives; move project adoption outside completed v9.4 stages; promote v9.4 Changelog headings; mark old user-merge wording as superseded.

- [x] **Step 4: Run focused and documentation tests**

Run: `python -m unittest tests.test_base_v9_5_skill_operating_refinement tests.test_documentation_governance tests.test_v9_governance_documents -v`

Expected: all tests pass.

### Task 5: Verify references, regression, and learning state

**Files:**
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: final diff and fresh verification output.
- Produces: evidence-backed observation with model evaluation explicitly `NOT_RUN`.

- [x] **Step 1: Run behavior and reference checks**

Run: `python tools/check_skill_behavior_evals.py`

Run: `python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base HEAD --head WORKTREE`

If the freshness checker does not accept a worktree pseudo-ref, use the repository's supported worktree comparison mode or report that exact check as blocked and supplement it with repository searches.

- [x] **Step 2: Run focused and full regression**

Run: `python -m unittest discover -s tests -v`

Run: `python tools/check_base_v9_integrity.py`

Run: `git diff --check`

- [x] **Step 3: Record verified learning status**

Record actual contract/test results as `OBSERVATION`; keep live model behavior `NOT_RUN` until external result files are scored.

- [x] **Step 4: Perform adversarial regression review**

Check untouched consumers, Registry bytes, released locks, historical prompts, false completion claims, scope expansion, and rollback.

- [x] **Step 5: Report without publishing**

Summarize changed files, tests, non-run checks, preserved history, Base-wide changes, project-specific changes (none), and the next authorized Git action. Do not stage, commit, push, or open a PR without separate authorization.
