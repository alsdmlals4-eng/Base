# Controlled Vocabulary Wave 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing Base controlled vocabulary with project-management, release, testing, maintenance, and Git/versioning terms while preserving standard-vs-industry-vs-Base-local authority boundaries.

**Architecture:** Reuse `docs/CONTROLLED_VOCABULARY.md` as the sole `BASE_SHARED` terminology canon and extend its existing semantic regression instead of adding a new Skill or framework. The regression is already consumed by the existing Game Project OS `ubuntu-contract`, so Wave 2 changes only the vocabulary, its test, design/plan receipts, and changelog.

**Tech Stack:** Markdown, Python 3.12 `unittest`, GitHub Actions, Git/GitHub PR workflow.

## Global Constraints

- Starting main: `6256a6bd88fad4b380f5b7dac06013b51a20b1e2`.
- Existing Solution First disposition: `ABSORB`.
- No new ACTIVE Skill, Work Mode, Skill Mode, Schema, route, workflow, or terminology framework.
- Preserve `AGENTS.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, `skills/**`, `skills/SKILL_REGISTRY.json`, `schemas/**`, `.github/workflows/**`, release locks, generated release artifacts, and project product files.
- `Epic` and `User Story` must not be presented as Scrum Guide-required Artifacts.
- `Early Access` must not collapse into Beta or Pre-Purchase.
- Smoke/Sanity are organization-variable terms; do not present one universal absolute boundary.
- Refactor preserves externally observable behavior/contract; Rewrite is a separate replacement lineage.
- Semantic Versioning meaning requires a declared public API rather than merely an `X.Y.Z` string.
- Exact-head CI, independent review, current-main freshness, unresolved-thread zero, and post-merge readback are mandatory.

---

### Task 1: Establish the Wave 2 semantic RED

**Files:**
- Modify: `tests/test_controlled_vocabulary_contract.py`

**Interfaces:**
- Consumes: existing `docs/CONTROLLED_VOCABULARY.md` and Wave 1 vocabulary regression.
- Produces: five failing Wave 2 semantic test methods covering all approved terminology groups.

- [x] **Step 1: Write the failing semantic tests**

Add tests for project management, release stages, testing taxonomy, maintenance terms, and Git/versioning boundaries. Require exact safety phrases such as `Sprint ≠ Milestone`, `Early Access ≠ Beta`, `Regression Testing ≠ Regression Recheck`, `Rewrite ≠ 큰 Refactor`, and `Rebase ≠ Merge`.

- [x] **Step 2: Run the existing CI consumer and verify intentional RED**

Run through draft PR #347 / Game Project OS `ubuntu-contract`.

Expected result:

```text
syntax: PASS
Base proposal validation: PASS
canonical reference freshness: PASS
Wave 1 vocabulary regression: PASS
Wave 2 vocabulary regression: 5 FAIL
overall ubuntu-contract: FAILURE
```

Actual receipt:

```text
RED commit: 9c4a4385032138f53fe66735362a9da98b41a4a2
run: 31762443963
420 tests
5 failures
15 skipped
first missing terms: Milestone / Alpha / Component / Unit Test / Code Smell / Branch
```

- [x] **Step 3: Confirm failures are requirements failures rather than test harness defects**

Read the job log and confirm only the five new Wave 2 tests fail while Wave 1 vocabulary and neighboring Base regressions remain green.

---

### Task 2: Implement the minimal controlled-vocabulary expansion

**Files:**
- Modify: `docs/CONTROLLED_VOCABULARY.md`
- Test: `tests/test_controlled_vocabulary_contract.py`

**Interfaces:**
- Consumes: Wave 2 RED phrases and source-class contract.
- Produces: human-readable definitions and anti-confusion boundaries that make all Wave 2 semantic tests pass.

- [x] **Step 1: Add project-management terms**

Add `Milestone`, `Sprint`, `Product Backlog`, generic `Backlog`, `Epic`, and `User Story`. Mark Scrum-defined terms separately from broader industry terms.

Required boundary block:

```text
Sprint ≠ Milestone
Product Backlog ≠ 모든 Backlog
User Story ≠ 전체 명세
Epic과 User Story는 Scrum Guide의 필수 Artifact가 아니다.
```

- [x] **Step 2: Add release-state terms**

Add `Alpha`, `Beta`, platform-specific `Early Access`, existing `Release Candidate`, and `Gold / Gold Master`; require project-specific Alpha/Beta Entry/Exit Criteria.

Required boundary block:

```text
Early Access ≠ Beta
Early Access ≠ Pre-Purchase
Gold / Gold Master ≠ Release Candidate
```

- [x] **Step 3: Add test-level and test-purpose terms**

Add `Component / Unit Test`, `Integration Test`, `E2E`, `Smoke`, `Sanity`, `UAT`, `Regression Testing`, and distinguish the existing Base-local `Regression Recheck`.

Required boundary block:

```text
Smoke/Sanity의 경계는 조직별 편차가 크다.
UAT ≠ 일반 QA
Regression Testing ≠ Regression Recheck
```

- [x] **Step 4: Add maintenance terms**

Add `Code Smell`, `Technical Debt`, `Refactor`, and `Rewrite`.

Required boundary block:

```text
Refactor = 외부 관찰 가능한 동작·계약을 보존
Rewrite ≠ 큰 Refactor
Code Smell ≠ 버그·Technical Debt 확정 증거
```

- [x] **Step 5: Add Git/versioning terms**

Add `Branch`, `Merge`, `Rebase`, `Cherry-pick`, `Hotfix`, and `Semantic Versioning / SemVer`.

Required boundary block:

```text
Rebase ≠ Merge
Cherry-pick ≠ Branch Merge
Hotfix ≠ Git 명령
SemVer는 public API를 선언한 소프트웨어에 의미 규칙을 적용한다.
```

- [ ] **Step 6: Run exact-head semantic regression and full selected CI**

Expected: the five Wave 2 tests and all existing selected regressions PASS on the same final PR head.

---

### Task 3: Record authority, evidence, and change history

**Files:**
- Create: `docs/superpowers/specs/2026-08-14-controlled-vocabulary-wave2-design.md`
- Create: `docs/superpowers/plans/2026-08-14-controlled-vocabulary-wave2.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: approved scope, official/reference-source boundaries, RED/GREEN evidence.
- Produces: auditable design/implementation/history receipts without creating a second terminology canon.

- [x] **Step 1: Record the design contract**

Document the five term groups, source classes, ADOPT/ADAPT/AVOID decisions, protected paths, TDD RED receipt, adversarial MUST_FIX list, completion criteria, and rollback.

- [x] **Step 2: Record this implementation plan**

Keep status checkboxes tied to actual execution. Do not mark CI/review/merge steps complete before their evidence exists.

- [ ] **Step 3: Add one concise Unreleased changelog entry**

The entry must state that the existing controlled vocabulary was expanded and that no new Skill/Registry/Schema/framework was created.

---

### Task 4: Exact-head review, integration, and post-merge verification

**Files:**
- Review: all PR #347 changed paths
- No new production files unless a validated review finding requires the minimum fix.

**Interfaces:**
- Consumes: final PR head, all exact-head checks, open-PR overlap inventory, current main.
- Produces: reviewed squash merge and merged-main readback.

- [ ] **Step 1: Verify final changed-path scope**

Expected paths:

```text
docs/CONTROLLED_VOCABULARY.md
docs/CHANGELOG.md
docs/superpowers/specs/2026-08-14-controlled-vocabulary-wave2-design.md
docs/superpowers/plans/2026-08-14-controlled-vocabulary-wave2.md
tests/test_controlled_vocabulary_contract.py
```

No Skill, Registry, Schema, route, workflow, or project file may appear.

- [ ] **Step 2: Run the adversarial review loop**

Attack at minimum:

```text
Scrum artifact overclaim
Sprint/Milestone collapse
Alpha/Beta fixed-percentage overclaim
Early Access/Beta/Pre-Purchase collapse
Gold/RC collapse
Smoke/Sanity universal overdefinition
UAT/all-QA collapse
Regression Testing/Base Regression Recheck collapse
Code Smell/Bug/Debt collapse
Refactor/behavior-change hiding
Rewrite/evidence auto-inheritance
Rebase/Merge collapse
Cherry-pick/Branch merge collapse
Hotfix/Git primitive collapse
X.Y.Z/SemVer-without-public-API overclaim
```

Validated critique → minimum fix → regression recheck for any real finding.

- [ ] **Step 3: Verify merge gate at the reviewed exact HEAD**

Require:

```text
all required checks: success
P0: 0
P1: 0
unresolved review threads: 0
PR: non-Draft and mergeable
main freshness: current
same-goal competing PR: none
path/hunk conflicts: none or explicitly reconciled
```

- [ ] **Step 4: Squash merge with expected head SHA**

Use GitHub merge with the reviewed exact head as `expected_head_sha`; reject a moved head.

- [ ] **Step 5: Read back merged main and post-merge checks**

Confirm:

```text
main contains merge SHA
CONTROLLED_VOCABULARY contains all five groups
semantic regression remains present
post-merge ubuntu-contract / ci-gate execute and pass as selected
no completion claim is made above actual evidence
```

## Rollback

Revert the single squash merge. No runtime, Registry, Schema, workflow, or project-data migration is introduced by this Wave 2 change.
