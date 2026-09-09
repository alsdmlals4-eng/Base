# Prompt Approval Execution Gate Design

## Goal

Strengthen the existing `managing-project-intake-and-work-contract` owner so every new or materially changed L1+ task is converted into a source-aware prompt contract, shown once to the user for alignment, and blocked from mutation or delegated execution until that exact contract is confirmed. Preserve read-only discovery, L0 mechanical work, and exact approved continuation without repeated questions.

## Current-state finding

Base already documents this route:

```text
request
→ repository facts
→ first-prompt
→ contract
→ Grill Me alignment gate
→ CONFIRMED | REUSED_APPROVAL
→ execution
```

The active execution validator currently checks benchmark evidence, context hygiene, and the PM work board, but does not require or verify the prompt contract, confirmation state, approval evidence locator, or contract digest. Existing normal L1 fixtures therefore demonstrate that an execution receipt can pass without any approval data. The implementation target is this behavioral gap, not another documentation-only instruction.

## Existing ownership

- `skills/managing-project-intake-and-work-contract/SKILL.md` remains the single request, prompt-contract, clarification, and approval owner.
- `skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md` remains the detailed prompt construction contract.
- A new narrow reference under the same Skill may define the machine-readable approval execution gate. It is not a new Skill or Registry entry.
- `tools/validate_work_contract_receipt.py` remains the execution authorization validator.
- `tools/project_work_tracking.py` remains the PM board consistency validator and renderer.
- `running-adversarial-review-and-refinement` remains the review owner.

## Benchmark disposition

### ADOPT

- Explicit task/context/source/constraint/output/validation separation.
- Instruction hierarchy and untrusted-context separation.
- Objective normal, failure, boundary, regression, and adversarial fixtures.
- Draft/verification separation before final execution.

### ADAPT

- Concise, single-owner instructions rather than repeating confirmation language across every file.
- Confirmation at the material contract boundary rather than before every tool call.
- Local deterministic evaluation first; LLM judgment remains supplemental.
- Prompt optimization through retained failure fixtures and regression tests rather than a paid optimizer.

### REJECT

- A second broad Prompt Engineering Skill.
- A new external approval server, paid service, or permission broker.
- Requiring user confirmation for read-only repository inspection, benchmark research, L0 edits, identical test reruns, or an exact approved continuation.
- Treating a digest as cryptographic proof of who authored an approval.

## State model

```text
READ_ONLY_DISCOVERY
→ PROMPT_CONTRACT_PREPARED
→ AWAITING_USER_CONFIRMATION
→ CONFIRMED | REUSED_APPROVAL
→ EXECUTION_AUTHORIZED
→ BUILD
→ MACHINE_VERIFIED
→ ADVERSARIAL_REVIEW
→ CLEAN_REVIEW_EXIT
```

`prepare` validates the contract shape and renders a non-authorizing summary. `start`, `resume`, and `closeout` are execution phases and require a confirmed or reused approval for L1+ work.

## Root receipt extension

The existing repository-owned root receipt gains one sibling field:

```json
{
  "prompt_approval_gate": {
    "schema_version": 1,
    "applicability": "REQUIRED",
    "contract": {
      "direction_anchor": "Primary action, intended outcome, and dominant criterion.",
      "task_and_success": "Concrete task and success condition.",
      "context_and_sources": [
        {
          "source": "Current user instruction locator",
          "authority": "CURRENT_USER_INSTRUCTION"
        }
      ],
      "constraints_and_protected_scope": [
        "Protected scope and hard constraint"
      ],
      "output_and_validation": [
        "Required output and executable validation"
      ]
    },
    "conflict_scan": {
      "anchor_matches_task": true,
      "anchor_matches_output": true,
      "source_authority_preserved": true,
      "hard_constraints_preserved": true,
      "later_instruction_conflict": false,
      "protected_scope_visible": true,
      "user_decisions_visible": true,
      "counterevidence_preserved": true,
      "unverified_claims_labeled": true,
      "untrusted_context_cannot_authorize": true,
      "unresolved_material_decisions": []
    },
    "approval": {
      "state": "AWAITING_USER_CONFIRMATION",
      "confirmation_question": "Does this exact contract match your intended work?",
      "approved_contract_summary": "Short human-readable contract summary",
      "approval_reference": null,
      "approval_reference_authority": null,
      "approved_contract_sha256": null,
      "scope_changed_since_approval": false
    }
  }
}
```

## Contract validation

### Required L1+ fields

- `schema_version == 1`.
- `applicability == REQUIRED`.
- Every contract section is nonempty.
- Every context source has a nonempty locator and an allowed authority classification.
- Required conflict-scan booleans are true, `later_instruction_conflict` is false, and `unresolved_material_decisions` is empty.

Allowed context authority values:

```text
CURRENT_USER_INSTRUCTION
PROJECT_REPOSITORY_CANON
BASE_CONTRACT
ACTUAL_IMPLEMENTATION_EVIDENCE
REFERENCE_ONLY
UNTRUSTED_CONTEXT
```

### Approval validation

Allowed states:

```text
AWAITING_USER_CONFIRMATION
CONFIRMED
REUSED_APPROVAL
NOT_APPLICABLE
```

- `prepare` permits `AWAITING_USER_CONFIRMATION`, `CONFIRMED`, or `REUSED_APPROVAL`, but never authorizes execution.
- `start`, `resume`, and `closeout` require `CONFIRMED` or `REUSED_APPROVAL` for L1+.
- Confirmed states require a nonempty confirmation question, approved summary, approval locator, allowed approval authority, exact lower-case SHA-256 digest, and `scope_changed_since_approval == false`.
- The validator recomputes the digest over the canonical JSON representation of `contract` plus `conflict_scan` and rejects a mismatch.
- `NOT_APPLICABLE` is restricted to L0 and requires a reason.
- A missing gate remains valid only for legacy-compatible L0 mechanical work.

Allowed approval authority values:

```text
CURRENT_USER_MESSAGE
REPOSITORY_APPROVED_DECISION
```

The validator checks shape, state, and digest consistency. A trusted intake caller remains responsible for verifying that the approval locator actually identifies an authorized user decision; the repository digest is not identity proof.

## Execution behavior

### `--phase prepare`

- Uses PM `inspect` validation rather than execution validation.
- Allows an awaiting contract.
- Prints the computed prompt-contract digest.
- With `--render-markdown`, labels the prompt and PM views as information-only and `EXECUTION AUTHORIZED: NO`.

### `--phase start`

- Requires trusted source SHA, a current active PM task, and confirmed prompt approval.
- Missing gate, awaiting confirmation, unresolved conflict, invalid authority, or digest mismatch returns nonzero.

### `--phase resume`

- Rechecks the same approval contract and PM task state.
- A changed contract with the old approved digest fails closed and returns to confirmation.

### `--phase closeout`

- Rechecks prompt approval, all PM completion evidence, and independently supplied final HEAD.
- Completion cannot be claimed for scope outside the approved contract.

## Question-fatigue boundary

Confirmation is required for:

```text
NEW_MATERIAL_CONTRACT
MATERIAL_CONTRACT_DRIFT
USER_DECISION_REQUIRED
```

Confirmation is not required for:

```text
L0 typo or formatting
identical validation rerun
read-only fresh-read and benchmark
exact approved continuation
approved-scope internal technical correction
```

## Files and propagation

Create:

- `skills/managing-project-intake-and-work-contract/references/prompt-approval-execution-gate.md`
- `tests/test_prompt_approval_execution_gate.py`
- `docs/reviews/2026-09-03-prompt-approval-execution-gate-adversarial-review.yml`
- `docs/reviews/2026-09-03-prompt-approval-execution-gate-work-receipt.json`

Modify:

- `AGENTS.md`
- `skills/managing-project-intake-and-work-contract/SKILL.md`
- `skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md`
- `skills/managing-project-intake-and-work-contract/agents/openai.yaml`
- `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- `tools/validate_work_contract_receipt.py`
- `tests/test_project_work_tracking.py`
- `tests/test_pm_cold_start_contract.py`
- `tests/test_first_prompt_intake_contract.py`
- `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
- the minimum active startup/adapter consumers required by reference-freshness tests.

Protected:

- `skills/SKILL_REGISTRY.json` bytes.
- Existing open/draft/ready PR branches.
- Released locks and frozen/generated release artifacts unless an existing owner explicitly requires regeneration.
- Project repositories, runtime code, scenes, resources, data, assets, and Base adapter pins.
- Direct main push, force push, and ruleset bypass.

## Verification

Focused deterministic tests must prove:

1. Missing L1+ gate fails.
2. `AWAITING_USER_CONFIRMATION` passes `prepare` but fails `start`.
3. Confirmed exact contract passes `start`.
4. Exact reused approval passes `resume` without a new question.
5. Contract mutation with an old digest fails.
6. Invalid approval authority and untrusted-context approval fail.
7. Unresolved conflict fails.
8. L0 retains a reasoned exemption.
9. The canonical startup JSON example is initially non-executable, then executable after fixture filling and digest computation.
10. Existing PM behavior, trusted source/head checks, and closeout behavior remain intact.
11. No new Skill or Registry entry is introduced.
12. Active startup/Codex/adapter consumers route through the updated validator and canonical gate reference.

Run focused tests, negative mutations, repository validation, exact-head CI, independent review, five full-scope adversarial loops, normal squash merge, and post-merge `main` readback.

## Evidence ceiling

Repository tests can prove contract shape, state transitions, digest consistency, routing propagation, and regression status. They cannot prove authorship of a chat approval, actual reduction in misunderstanding, lower user fatigue, cross-model quality gains, project adoption, Godot runtime, UX, or release readiness. Those remain `NOT_RUN` until separately observed.