# Serial-Fiction Canon Migration and Frontier Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimal, reusable Canon-migration and reconciliation-frontier contract to the existing serial-fiction and reference-freshness owners.

**Architecture:** `developing-and-revising-serial-fiction: canon-and-continuity` defines the lifecycle and output distinctions; the serial-fiction knowledge guide explains the reusable decision flow; `auditing-canonical-reference-freshness` checks declared consumer inventories and propagation evidence without owning project schemas. A focused Python contract suite protects the four enforcement classes, bounded debt, candidate-versus-verified frontier, and the no-new-Skill boundary.

**Tech Stack:** Markdown Skill/knowledge contracts, Python `unittest`, Base reference-freshness checker, GitHub Actions.

## Global Constraints

- Reuse the existing `developing-and-revising-serial-fiction` and `auditing-canonical-reference-freshness` owners; create no ACTIVE Skill, Registry entry, project schema, or workflow.
- Keep fictional work names, Canon IDs, chapter counts, bundle paths, character data, source-file labels, and project validation commands out of Base.
- Keep `STRICT_NOW`, `FORBIDDEN_IN_NEW_OR_REVISED`, `BOUNDED_LEGACY_RECONCILIATION_DEBT`, and `SCOPED_STRICT` semantically distinct.
- A declared debt set may block expansion but is not `CANON_MIGRATION_COMPLETE`; archive/reference-only artifacts are excluded from active debt.
- A frontier may advance only after its declared validation gate passes; candidate data is never evidence of a verified prefix or whole-manuscript reconciliation.
- Derived consumers must not infer normal continuity across an unresolved migration boundary; duplicate current authority remains fail-closed.
- Do not change `skills/SKILL_REGISTRY.json`, frozen Base v9.0 release artifacts, generated Skill Map, templates, or project repositories.

---

### Task 1: Define failing lifecycle and frontier contracts

**Files:**
- Modify: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: existing serial-fiction Skill and writing/revision guide.
- Produces: `test_canon_migration_contract_distinguishes_enforcement_and_completion` and `test_reconciliation_frontier_contract_blocks_false_continuity_and_false_promotion`.

- [ ] **Step 1: Add the two contract tests.**

The first test must require each enforcement class, an exact declared-versus-actual debt invariant, `PASS_WITH_KNOWN_DEBT`, `CANON_MIGRATION_COMPLETE`, and the rule that active/archive consumers are separated. It must name the break: a change that treats bounded legacy debt as completion or allows debt expansion.

The second test must require `VERIFIED_PREFIX`, `DECLARED_MIGRATION_BOUNDARY`, `LEGACY_TAIL`, `FRONTIER_VERIFICATION_STATUS`, candidate-versus-verified distinction, derived-consumer blocking, and duplicate-current-authority failure. It must name the break: a change that promotes an unvalidated candidate frontier or invents cross-boundary continuity.

- [ ] **Step 2: Run the focused test file to verify RED.**

Run: `python -m unittest tests.test_serial_fiction_discipline -v`

Expected: the two new tests fail because the current contracts lack the lifecycle/frontier guarantees.

### Task 2: Implement the minimal owner contracts

**Files:**
- Modify: `skills/developing-and-revising-serial-fiction/SKILL.md`
- Modify: `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
- Modify: `skills/auditing-canonical-reference-freshness/SKILL.md`
- Modify: `skills/developing-and-revising-serial-fiction/LEARNING_LOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: the two contract-test requirements from Task 1.
- Produces: a project-schema-neutral lifecycle, frontier boundary, output fields, and freshness-audit consumer inventory responsibility.

- [ ] **Step 1: Extend `canon-and-continuity` inputs, procedure, failure markers, and output.**

Require a latest Canon/Decision, active-versus-archive consumer inventory, enforcement class, declared debt set, reconciliation unit, frontier status, validation evidence, and duplicate-authority result only when staged migration applies. Add failure markers `CANON_MIGRATION_DEBT_EXPANDED`, `CANON_MIGRATION_COMPLETION_OVERCLAIM`, `UNVERIFIED_MIGRATION_BOUNDARY_CONTINUITY`, `FRONTIER_PROMOTION_WITHOUT_VALIDATION`, and `DUPLICATE_CURRENT_AUTHORITY`.

- [ ] **Step 2: Add the reusable guide section.**

Describe Decision authority versus legacy-artifact completion, the four enforcement classes, exact bounded-debt behavior, verified-prefix/boundary/tail topology, candidate-versus-verified promotion, normal-continuity prohibition across unresolved boundaries, and the greenfield/archive/safe-rename exclusions.

- [ ] **Step 3: Add the supporting freshness boundary.**

Limit the freshness owner to inventory, canonical-owner, derived-consumer, declared-validation, and untouched-consumer audit evidence; state that it does not prescribe fiction data fields or decide narrative continuity.

- [ ] **Step 4: Record both learning entries.**

Record that the pattern comes from one project plus counterexample, that the Base contract is schema-neutral, and that second-project/human usability validation remains not run.

- [ ] **Step 5: Run the focused test file to verify GREEN.**

Run: `python -m unittest tests.test_serial_fiction_discipline -v`

Expected: all serial-fiction discipline tests pass.

### Task 3: Verify propagation, scope, and adversarial failures

**Files:**
- Verify only: Task 1–2 files and their diff.

**Interfaces:**
- Consumes: the implementation diff against `381b66bc3619caf7994b0073108fdcba23b30e96`.
- Produces: exact-head freshness, protected-surface, and adversarial dispositions.

- [ ] **Step 1: Run canonical reference freshness for the exact base and head.**

Run: `python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base 381b66bc3619caf7994b0073108fdcba23b30e96 --head HEAD`

Expected: pass with the changed Skill, learning-log, and focused-test companions.

- [ ] **Step 2: Run adversarial checks.**

Confirm with `git diff --name-only`, `git diff --check`, Registry comparison, and targeted searches that no new Skill/schema/project identifier/frozen artifact was introduced; then temporarily inject and restore a guide marker to prove the focused contract fails when a lifecycle guarantee is absent.

- [ ] **Step 3: Run the relevant broader validation.**

Run the focused serial suite, reference-freshness suite, skill-system coverage check, generated-artifact check, and `tools/run_local_validation.py --trusted-history-commit 381b66bc3619caf7994b0073108fdcba23b30e96` when its documented environment is available. Separate environment failures from regression failures.

### Task 4: Publish verified implementation

**Files:**
- Commit: only the plan, Task 1–2 contract files, and any generated/learning companion required by validation.

**Interfaces:**
- Consumes: clean working tree, exact validation evidence, and the user’s existing continuous-work approval.
- Produces: one Base implementation PR for BCP-012 and BCP-017.

- [ ] **Step 1: Inspect staged paths and commit only confirmed files.**

Run: `git status --short && git diff --check && git diff --name-only 381b66bc3619caf7994b0073108fdcba23b30e96...HEAD`

- [ ] **Step 2: Create a draft PR from `agent/bcp-012-017-serial-fiction` to `main`.**

Include the exact base/head, BCP-012/017 relationship, no-new-Skill boundary, test evidence, unresolved second-project/human validation, rollback (revert only this PR), and protected surfaces.

- [ ] **Step 3: Merge only after exact-head required CI, review, and unresolved-thread checks pass.**

After merge, re-fetch `main`, compare its tree to the verified head tree, and run post-merge checks available in the verified environment.

## Plan self-review

- Coverage: lifecycle, frontier, derived consumers, freshness support, learning, regression, adversarial review, publish, and post-merge verification each have an explicit task.
- Scope: no project data/schema, new Skill, Registry, frozen artifact, workflow, or template is included.
- Ambiguity resolved: documentation contracts are the implementation surface; tests protect semantic contracts in the repository’s established `unittest` style.
- Deferred evidence: second project, human usability, and project runtime verification are explicitly not completion criteria for this Base contract.
