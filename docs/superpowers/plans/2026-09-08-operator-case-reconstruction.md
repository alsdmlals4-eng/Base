# External Operator Case Reconstruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Require a complete, bounded reconstruction only when an external operator case is recorded as a benchmark decision influence.

**Architecture:** Extend the existing `benchmark_preflight_receipt.entries` shape instead of creating a second case store. The Python validator enforces six narrative fields only when `operator_case_reconstruction` is present; the benchmark and intake owners state the policy trigger and link the reconstruction to existing execution-strategy and case-study owners.

**Tech Stack:** Python standard library, `unittest`, Markdown, JSON work-contract receipt.

**Spec:** `docs/superpowers/specs/2026-09-08-operator-case-reconstruction-design.md`

## Global Constraints

- Preserve existing receipt entries that do not reference an external operator case.
- Do not add dependencies, a new common taxonomy, an external case database, an agent framework, or a paid tool.
- Treat public cards, vendor case studies, and self-reported outcomes as evidence with an explicit ceiling, not project/runtime proof.
- Direct user approval covers this exact Base change; work only on `codex/operator-case-reconstruction-20260908`, never `main`.
- Run exactly two full-scope adversarial review rounds after the change and run the repository's local validation from the dependency-complete temporary environment.

---

### Task 1: Enforce selective reconstruction completeness

**Files:**

- Modify: `tests/test_work_contract_receipt_validator.py`
- Modify: `tools/validate_work_contract_receipt.py`

**Interfaces:**

- Consumes: `validate_receipt(receipt: object) -> list[str]` and the existing benchmark receipt entry schema.
- Produces: optional `operator_case_reconstruction: dict` validation with six required nonempty string fields.

- [x] **Step 1: Write the failing tests**

```python
def test_operator_case_reconstruction_requires_every_evidence_boundary(self) -> None:
    receipt = valid_receipt()
    receipt["benchmark_preflight_receipt"]["entries"][0]["operator_case_reconstruction"] = {
        "input_anchor_and_source": "operator supplied a greybox prototype request",
        "staged_execution_and_handoffs": "prototype, human test, then themed iteration",
        "human_decision_and_approval_boundary": "human selects the next prototype",
        "observable_outcome_and_evidence_ceiling": "reported outcome; no independent reproduction",
        "nontransferable_or_unobserved": "internal tooling was not available",
    }
    self.assertIn(
        "benchmark_preflight_receipt.entries[0].operator_case_reconstruction.project_trial_and_acceptance_gate is required",
        validate_receipt(receipt),
    )

def test_complete_operator_case_reconstruction_is_accepted(self) -> None:
    receipt = valid_receipt()
    receipt["benchmark_preflight_receipt"]["entries"][0]["operator_case_reconstruction"] = {
        "input_anchor_and_source": "operator supplied a greybox prototype request",
        "staged_execution_and_handoffs": "prototype, human test, then themed iteration",
        "human_decision_and_approval_boundary": "human selects the next prototype",
        "observable_outcome_and_evidence_ceiling": "reported outcome; no independent reproduction",
        "nontransferable_or_unobserved": "internal tooling was not available",
        "project_trial_and_acceptance_gate": "run one small project trial before adoption",
    }
    self.assertEqual([], validate_receipt(receipt))
```

- [x] **Step 2: Run the focused test to verify it fails because the new check is absent**

Run: `python -m unittest tests.test_work_contract_receipt_validator.WorkContractReceiptValidatorTests.test_operator_case_reconstruction_requires_every_evidence_boundary -v`

Expected: FAIL because `validate_receipt` returns no required-field error.

- [x] **Step 3: Add the minimal validator branch**

```python
reconstruction = entry.get("operator_case_reconstruction")
if reconstruction is not None:
    if not isinstance(reconstruction, dict):
        errors.append(f"{prefix}.operator_case_reconstruction must be an object")
    else:
        for field in OPERATOR_CASE_RECONSTRUCTION_FIELDS:
            if not _nonempty_string(reconstruction.get(field)):
                errors.append(f"{prefix}.operator_case_reconstruction.{field} is required")
```

- [x] **Step 4: Run the focused validator test module**

Run: `python -m unittest tests.test_work_contract_receipt_validator -v`

Expected: PASS, including absence, incomplete-object, malformed-object, and complete-object coverage.

- [x] **Step 5: Commit the focused validator and test change**

```bash
git add tools/validate_work_contract_receipt.py tests/test_work_contract_receipt_validator.py
git commit -m "feat: validate operator case reconstruction receipts"
```

### Task 2: Connect the selective policy to existing owners

**Files:**

- Modify: `docs/BENCHMARKING_REFERENCE_GUIDE.md`
- Modify: `templates/KNOWLEDGE_CASE_STUDY.md`
- Modify: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
- Modify: `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`

**Interfaces:**

- Consumes: the six fields validated in Task 1.
- Produces: one policy trigger and one receipt-template route that distinguish documented evidence from outcome/adoption proof.

- [x] **Step 1: Add the policy trigger to the benchmark guide**

Add a short subsection immediately after pattern extraction: when an external operator case materially changes a workflow/tool/Skill/evaluation/QA/content-pipeline decision, record a complete reconstruction in the existing receipt entry; otherwise do not require it. State direct-source preference and the evidence ceiling.

- [x] **Step 2: Extend the reusable case-study template**

Add an optional reconstruction section after observational evidence. Include the six field labels, the human gate, non-transferability, and the smallest project trial. Preserve the template's current decision, results, non-copy, and validation sections.

- [x] **Step 3: Add the receipt-template field without duplicating a new schema**

In the Project Start checklist and Execution Sequence plan, document `operator_case_reconstruction` as an optional nested object on a benchmark entry and list its six required fields when present. In the intake Skill/reference, link it to the existing execution-strategy owner for observed runtime behavior and failure routing.

- [x] **Step 4: Read changed consumers and run the focused test module**

Run: `python -m unittest tests.test_work_contract_receipt_validator -v`

Expected: PASS. Read all six edited human-facing owners to confirm they consistently say “only when an external operator case changes the decision” and do not claim independent proof.

- [x] **Step 5: Commit the owner and template documentation**

```bash
git add docs/BENCHMARKING_REFERENCE_GUIDE.md templates/KNOWLEDGE_CASE_STUDY.md templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md templates/planning/EXECUTION_SEQUENCE_PLAN.md skills/managing-project-intake-and-work-contract/SKILL.md skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md
git commit -m "docs: record bounded external operator case evidence"
```

### Task 3: Record, verify, and publish the approved Base change

**Files:**

- Create: `docs/operations/work-receipts/2026-09-08-operator-case-reconstruction.json`
- Create: `docs/superpowers/specs/2026-09-08-operator-case-reconstruction-design.md`
- Create: `docs/superpowers/plans/2026-09-08-operator-case-reconstruction.md`

**Interfaces:**

- Consumes: source SHA `68792fc38340a19945ba6b15eedef39f55d50705`, the completed validator, and local validation runner.
- Produces: an auditable L1 receipt, test evidence, two adversarial review results, one committed branch, and a PR.

- [x] **Step 1: Validate the start receipt**

Run: `python tools/validate_work_contract_receipt.py --receipt docs/operations/work-receipts/2026-09-08-operator-case-reconstruction.json --phase start --expected-source-sha 68792fc38340a19945ba6b15eedef39f55d50705 --render-markdown`

Expected: PASS with the implementation item `IN_PROGRESS`.

- [x] **Step 2: Run targeted and whole-repository validation**

Run: `python -m unittest tests.test_work_contract_receipt_validator -v` and `python tools/run_local_validation.py --trusted-history-commit 86ebb1f13f3c48e45392ece4b3167216445dca4f` using the dependency-complete temporary virtual environment.

Expected: both exit 0. Record only the actual static/test ceiling; do not claim runtime/project productivity proof.

- [x] **Step 3: Run exactly two full-scope adversarial rounds**

Round 1 checks semantic trigger, validator bypasses, all direct templates/consumers, duplicate-owner risk, and evidence claims. Correct only validated findings, then rerun affected tests.

Round 2 re-reads the complete changed surface and test/validation evidence after round-1 corrections. Confirm no actionable omission, conflict, duplicate work, or complement gap remains; do not invent a third round.

- [ ] **Step 4: Update the receipt to its actual final state and verify closeout**

Set the task `DONE` only after every acceptance/check/required evidence is PASS at the final commit SHA. Run the receipt closeout command with independently read final HEAD.

- [ ] **Step 5: Commit, push the named branch, and create a focused PR**

```bash
git add docs/operations/work-receipts/2026-09-08-operator-case-reconstruction.json docs/superpowers/specs/2026-09-08-operator-case-reconstruction-design.md docs/superpowers/plans/2026-09-08-operator-case-reconstruction.md
git commit -m "docs: record operator case reconstruction change"
git push -u origin codex/operator-case-reconstruction-20260908
```

Expected: no push to `main`, no force push, and the PR describes evidence limits, tests, and rollback.

## Plan self-review

- Spec coverage: Task 1 covers the conditional machine check; Task 2 assigns the trigger and owner routes; Task 3 records source/limits, validates, runs two full-scope reviews, and publishes a reversible branch.
- Placeholder scan: the plan uses concrete paths, field names, commands, expected results, source SHA, and commit messages; no implementation placeholders remain.
- Interface consistency: every documentation owner uses the same six `operator_case_reconstruction` field names validated by `validate_receipt`.
