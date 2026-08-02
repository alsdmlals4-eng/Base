# Skill Behavior and Evidence Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make active-Skill behavior coverage, external model-run reproducibility, and per-Skill repository evidence machine-auditable without adding a new broad Skill or changing released Registry bytes.

**Architecture:** Extend the existing behavior-evaluation checker with coverage and result-artifact validation, add one strict result schema/template, and build one deterministic generated evidence matrix from Registry and repository facts. Focused tests fail on missing coverage, stale result metadata, and generated evidence drift; existing routing and release contracts remain authoritative.

**Tech Stack:** Python 3, JSON Schema Draft 2020-12, `unittest`/`pytest`, Markdown, GitHub Actions through existing repository test discovery.

## Global Constraints

- Keep `skills/SKILL_REGISTRY.json` byte-identical to released Base v9.4.
- Keep `base-v9.4.lock.json` and frozen/generated release artifacts unchanged.
- Do not invoke an external paid model from CI.
- Keep `MODEL_RUN_STATUS: NOT_RUN` when no real result file is supplied.
- Do not modify open PR #134, #136, or #137 branches or their prompt/tutorial files.
- Do not add a new broad Skill; extend `evolving-project-discipline-skills: behavior-eval`.
- Every generated artifact must be deterministic and checked against source inputs.

---

### Task 1: Define failing behavior-coverage tests

**Files:**
- Create: `tests/test_skill_behavior_evidence_hardening.py`
- Modify later: `tools/check_skill_behavior_evals.py`
- Modify later: `skills/SKILL_BEHAVIOR_EVALS.json`

**Interfaces:**
- Consumes: `validate_contract(root: Path) -> list[str]` from `tools/check_skill_behavior_evals.py`.
- Produces: tests for active primary coverage and forbidden/non-selection coverage.

- [ ] **Step 1: Write temporary-repository tests**

Create fixtures with two active Skills and behavior cases that intentionally omit one Skill as primary or forbidden. Assert errors contain `missing primary behavior coverage` and `missing non-selection behavior coverage`.

- [ ] **Step 2: Run the focused tests**

Run:

```bash
python -m pytest tests/test_skill_behavior_evidence_hardening.py -q
```

Expected: FAIL because the existing checker does not enforce coverage.

- [ ] **Step 3: Commit the RED tests**

```bash
git add tests/test_skill_behavior_evidence_hardening.py
git commit -m "test: define skill behavior coverage gates"
```

### Task 2: Implement coverage validation and complete fixtures

**Files:**
- Modify: `tools/check_skill_behavior_evals.py`
- Modify: `skills/SKILL_BEHAVIOR_EVALS.json`
- Test: `tests/test_skill_behavior_evidence_hardening.py`

**Interfaces:**
- Produces: `behavior_coverage(registry, evals) -> dict[str, dict[str, int]]` and coverage errors from `validate_contract`.
- Every active Skill must have `primary_case_count >= 1` and `forbidden_case_count >= 1`.

- [ ] **Step 1: Add minimal coverage calculation**

Build active Skill counts from `expected_primary_skill`, `expected_supporting_skills`, and `forbidden_skills`. Supporting coverage is reported but does not satisfy primary coverage.

- [ ] **Step 2: Add fail-closed errors and summary output**

Return errors for each active Skill missing primary or forbidden coverage. Print aggregate coverage totals after contract validation.

- [ ] **Step 3: Expand behavior fixtures**

Add focused cases for every active Skill missing primary coverage. Use concrete user prompts, expected Work Mode, primary/supporting Skills, discoverable Skill Modes, forbidden Skills, evidence tokens, decision state, and rationale. Add forbidden appearances until every active Skill has a non-selection boundary.

- [ ] **Step 4: Run focused and existing behavior tests**

```bash
python -m pytest tests/test_skill_behavior_evidence_hardening.py tests/test_neutral_adversarial_feature_lifecycle.py -q
python tools/check_skill_behavior_evals.py
```

Expected: PASS with `CONTRACT_STATUS: PASS`, full primary coverage, full non-selection coverage, and `MODEL_RUN_STATUS: NOT_RUN`.

- [ ] **Step 5: Commit**

```bash
git add tools/check_skill_behavior_evals.py skills/SKILL_BEHAVIOR_EVALS.json tests/test_skill_behavior_evidence_hardening.py
git commit -m "feat: require complete active-skill behavior coverage"
```

### Task 3: Add reproducible external result schema and scoring gates

**Files:**
- Create: `schemas/skill-behavior-results-v1.schema.json`
- Create: `skills/SKILL_BEHAVIOR_RESULTS.template.json`
- Modify: `tools/check_skill_behavior_evals.py`
- Modify: `tests/test_skill_behavior_evidence_hardening.py`

**Interfaces:**
- Result schema requires `repository`, `commit_sha`, Registry/evaluation paths and SHA-256 values, model metadata, independent-review metadata, and one result per case.
- `score_results(root: Path, results_path: Path) -> list[str]` validates schema and exact source identity before semantic scoring.

- [ ] **Step 1: Write failing schema and stale-identity tests**

Test malformed commit SHA, missing reviewer metadata, incomplete results, stale Registry hash, and stale evaluation hash.

- [ ] **Step 2: Run focused tests**

Expected: FAIL because no result schema or identity checks exist.

- [ ] **Step 3: Add the JSON Schema and template**

Use Draft 2020-12. Constrain Work Mode, user decision states, SHA-256 patterns, commit SHA, date-time, array uniqueness, and required result fields.

- [ ] **Step 4: Extend result scoring**

Load and validate the result schema. Compute current file hashes and reject mismatches before routing comparison. Keep no-results behavior unchanged.

- [ ] **Step 5: Run focused checker tests**

```bash
python -m pytest tests/test_skill_behavior_evidence_hardening.py -q
python tools/check_skill_behavior_evals.py
```

Expected: PASS; no result file still prints `MODEL_RUN_STATUS: NOT_RUN`.

- [ ] **Step 6: Commit**

```bash
git add schemas/skill-behavior-results-v1.schema.json skills/SKILL_BEHAVIOR_RESULTS.template.json tools/check_skill_behavior_evals.py tests/test_skill_behavior_evidence_hardening.py
git commit -m "feat: validate reproducible skill behavior results"
```

### Task 4: Generate the active-Skill implementation evidence matrix

**Files:**
- Create: `tools/build_skill_implementation_evidence.py`
- Create: `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md`
- Modify: `tests/test_skill_behavior_evidence_hardening.py`

**Interfaces:**
- Produces: `build_evidence_markdown(root: Path) -> str`.
- CLI supports `--root`, `--output`, and `--check`.
- Evidence classification: `EXECUTABLE_EVIDENCE`, `CONTRACT_EVIDENCE`, `MISSING_EVIDENCE`.

- [ ] **Step 1: Write failing deterministic-generation tests**

Assert every active Skill appears once, generated bytes match the checked-in file, counts are stable, and missing packages produce `MISSING_EVIDENCE`.

- [ ] **Step 2: Run focused tests**

Expected: FAIL because the builder and generated file do not exist.

- [ ] **Step 3: Implement repository evidence discovery**

Count package `references/**`, package `scripts/**`, exact Skill-ID mentions under `tests/**/*.py` and `.github/workflows/*`, and primary/supporting/forbidden behavior cases. Do not claim execution success.

- [ ] **Step 4: Generate the Markdown derivative**

```bash
python tools/build_skill_implementation_evidence.py
python tools/build_skill_implementation_evidence.py --check
```

Expected: deterministic output and successful check.

- [ ] **Step 5: Run focused tests**

```bash
python -m pytest tests/test_skill_behavior_evidence_hardening.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/build_skill_implementation_evidence.py docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md tests/test_skill_behavior_evidence_hardening.py
git commit -m "feat: generate active skill implementation evidence"
```

### Task 5: Connect the strengthened contract to Skill governance

**Files:**
- Modify: `skills/evolving-project-discipline-skills/SKILL.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `.github/reference-freshness.json`
- Modify: `tests/test_skill_behavior_evidence_hardening.py`

**Interfaces:**
- `behavior-eval` requires coverage audit, exact source identity, independent-review metadata, and evidence-matrix review.
- Coupled-change rules require focused tests and generated evidence when evaluation contracts change.

- [ ] **Step 1: Write failing contract-coupling tests**

Assert the Skill body names the new contracts and reference freshness requires the focused test and generated evidence artifact.

- [ ] **Step 2: Update Skill and Learning Log**

Record the audit finding, implementation, remaining external-model `NOT_RUN`, and future review triggers.

- [ ] **Step 3: Update coupled-change configuration**

Require `tests/test_skill_behavior_evidence_hardening.py` and `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md` when the behavior checker, evaluation set, result schema, or evidence builder changes.

- [ ] **Step 4: Run focused governance tests**

```bash
python -m pytest tests/test_skill_behavior_evidence_hardening.py tests/test_reference_freshness.py tests/test_skill_system_coverage.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/evolving-project-discipline-skills/SKILL.md skills/SKILL_LEARNING_LOG.md .github/reference-freshness.json tests/test_skill_behavior_evidence_hardening.py docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md
git commit -m "docs: connect skill evidence governance"
```

### Task 6: Full verification and Draft PR

**Files:**
- Verify all changed files.
- Create Draft PR from `agent/skill-behavior-evidence-hardening` to `main`.

**Interfaces:**
- Required evidence: exact branch HEAD, changed-file inventory, focused tests, full repository tests when available, reference freshness, Registry hash, release-lock preservation, and unresolved-thread status.

- [ ] **Step 1: Run focused validation**

```bash
python tools/check_skill_behavior_evals.py
python tools/build_skill_implementation_evidence.py --check
python -m pytest tests/test_skill_behavior_evidence_hardening.py tests/test_neutral_adversarial_feature_lifecycle.py tests/test_reference_freshness.py tests/test_skill_system_coverage.py tests/test_consolidated_skill_references.py -q
```

- [ ] **Step 2: Run full validation**

```bash
python -m pytest -q
git diff --check main...HEAD
```

If the environment cannot run the full checkout, record `BLOCKED_ENVIRONMENT` and use exact-head GitHub Actions without claiming local PASS.

- [ ] **Step 3: Verify protected identities**

Confirm Registry SHA-256 remains `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`, release locks are unchanged, and open PR #134/#136/#137 files are untouched.

- [ ] **Step 4: Run adversarial review**

Attack false coverage, fixture padding, stale result acceptance, evidence overclaim, generated-file drift, and new broad-Skill duplication. Validate each criticism and fix only confirmed findings.

- [ ] **Step 5: Create Draft PR**

The PR body must separate contract evidence, actual model-run status, local/Actions results, evidence limits, changed-file scope, rollback, and remaining work.

- [ ] **Step 6: Record exact-head verification**

Fetch exact-head Actions and review threads. Leave the PR Draft if external model behavior remains `NOT_RUN` or any required check is incomplete.
