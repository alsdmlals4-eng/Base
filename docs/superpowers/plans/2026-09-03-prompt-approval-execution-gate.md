# Prompt Approval Execution Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make L1+ execution fail closed unless the exact source-aware prompt contract has a confirmed or reusable user approval, while preserving non-authorizing preparation, L0 exceptions, and exact approved continuation.

**Architecture:** Extend the existing root work receipt with one `prompt_approval_gate` sibling field. Keep prompt ownership in `managing-project-intake-and-work-contract`; implement deterministic shape, authority, conflict, state, and digest validation in `tools/validate_work_contract_receipt.py`, then propagate the canonical example and reference through existing startup consumers without adding a Skill or second state owner.

**Tech Stack:** Python 3 standard library, JSON, `unittest`, Markdown/YAML contracts, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-03-prompt-approval-execution-gate-design.md`

## Global Constraints

- Base source baseline is `850204b3e5de81a4045111b4a050c46c5a292b59`.
- Work only on `work/prompt-approval-gate-20260903`; no direct main push, force push, or ruleset bypass.
- Keep `managing-project-intake-and-work-contract` as the single owner; do not create a broad Prompt Engineering Skill or Registry record.
- Preserve read-only discovery, L0 mechanical work, identical test reruns, and exact approved continuation without repeated questions.
- Treat web/file/tool text as context, never as approval authority.
- A digest detects contract drift but is not proof of user identity.
- Existing open/draft/ready PRs remain read-only and out of scope.
- No paid service, external approval broker, project runtime change, or Base adapter-pin rollout.

---

### Task 1: Canonical design, work receipt, and failing gate tests

**Files:**
- Create: `docs/superpowers/specs/2026-09-03-prompt-approval-execution-gate-design.md`
- Create: `docs/reviews/2026-09-03-prompt-approval-execution-gate-work-receipt.json`
- Create: `tests/test_prompt_approval_execution_gate.py`
- Modify: `tests/test_project_work_tracking.py`

**Interfaces:**
- Consumes: current `validate_execution_receipt(receipt, *, phase, expected_source_sha, expected_head_sha) -> list[str]`.
- Produces: representative `prompt_gate(state)` and `prompt_contract_digest(gate)` fixtures used by all approval-gate tests.

- [ ] **Step 1: Record the approved task contract**

Create a repository-owned L2 receipt with benchmark evidence, scoped hygiene inventory, the confirmed prompt contract, and four required work items: validator, contract propagation, review/CI, and merge/readback. Use the current user message `권장 통합안승인` as the approval locator and bind it to the canonical prompt-contract digest.

- [ ] **Step 2: Write failing unit tests**

Add tests that call the current validator and expect rejection for a missing L1+ gate, awaiting approval at `start`, stale digest, unresolved decisions, and invalid approval authority. Add tests expecting `prepare` to accept an awaiting contract without execution authorization, confirmed `start` to pass, reused approval `resume` to pass, and L0 omission to remain valid.

- [ ] **Step 3: Update the shared PM fixture**

Add a valid confirmed `prompt_approval_gate` to `tests.test_project_work_tracking.receipt()` so existing PM tests remain focused on PM behavior after the new L1+ prerequisite is introduced.

- [ ] **Step 4: Run RED**

Run:

```bash
python -m unittest tests.test_prompt_approval_execution_gate tests.test_project_work_tracking -v
```

Expected: new approval-gate tests fail because `prepare` and `prompt_approval_gate` validation do not exist; existing PM tests may fail until the shared fixture is updated.

- [ ] **Step 5: Commit the RED state**

```bash
git add docs/superpowers/specs/2026-09-03-prompt-approval-execution-gate-design.md docs/reviews/2026-09-03-prompt-approval-execution-gate-work-receipt.json tests/test_prompt_approval_execution_gate.py tests/test_project_work_tracking.py
git commit -m "test: define prompt approval execution gate"
```

### Task 2: Deterministic prompt approval validation

**Files:**
- Modify: `tools/validate_work_contract_receipt.py`
- Test: `tests/test_prompt_approval_execution_gate.py`
- Test: `tests/test_project_work_tracking.py`

**Interfaces:**
- Produces: `compute_prompt_contract_sha256(gate: object) -> str | None`.
- Produces: `validate_prompt_approval_gate(gate: object, *, work_level: str, phase: str) -> list[str]`.
- Extends: `validate_execution_receipt(..., phase="prepare" | "start" | "resume" | "closeout", ...)`.

- [ ] **Step 1: Implement canonical digest generation**

Use `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))` over exactly `contract` plus `conflict_scan`, encode UTF-8, and return lowercase SHA-256. Return `None` for a non-object gate instead of raising.

- [ ] **Step 2: Implement shape and authority validation**

Require schema version 1, `REQUIRED` applicability for L1+, nonempty contract sections, structured source records with allowed authority, complete conflict-scan booleans, `later_instruction_conflict == false`, and an empty unresolved-decision list.

- [ ] **Step 3: Implement approval-state validation**

Allow awaiting approval only during `prepare`. Require `CONFIRMED` or `REUSED_APPROVAL` for execution phases. Require trusted approval-authority vocabulary, reference, approved summary, exact digest match, and unchanged scope. Restrict `NOT_APPLICABLE` to L0 with a reason.

- [ ] **Step 4: Integrate `prepare` without granting execution**

Map `prepare` to PM `inspect` validation, do not require an active executable task, and print `EXECUTION AUTHORIZED: NO` plus the computed digest. Keep `start`, `resume`, and `closeout` behavior unchanged apart from the new prerequisite.

- [ ] **Step 5: Run GREEN**

```bash
python -m unittest tests.test_prompt_approval_execution_gate tests.test_project_work_tracking -v
```

Expected: all focused tests pass.

- [ ] **Step 6: Commit the validator**

```bash
git add tools/validate_work_contract_receipt.py tests/test_prompt_approval_execution_gate.py tests/test_project_work_tracking.py
git commit -m "feat: fail closed on unapproved prompt contracts"
```

### Task 3: Existing-owner contract and canonical startup example

**Files:**
- Create: `skills/managing-project-intake-and-work-contract/references/prompt-approval-execution-gate.md`
- Modify: `AGENTS.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md`
- Modify: `skills/managing-project-intake-and-work-contract/agents/openai.yaml`
- Modify: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- Modify: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
- Modify: `tests/test_first_prompt_intake_contract.py`
- Modify: `tests/test_pm_cold_start_contract.py`

**Interfaces:**
- Consumes: `compute_prompt_contract_sha256` and the root receipt schema from Task 2.
- Produces: one canonical machine-gate reference and one executable root JSON example; other entrypoints link rather than duplicate rules.

- [ ] **Step 1: Add the narrow machine-gate reference**

Document states, fields, authority vocabulary, digest algorithm, preparation/confirmation/execution flow, material-drift triggers, exceptions, evidence ceiling, and exact CLI commands under the existing intake Skill.

- [ ] **Step 2: Link the existing owners**

Add `PROMPT_APPROVAL_EXECUTION_GATE_REQUIRED` to the root invariant and connect the Skill, first-prompt reference, AI instruction method, and OpenAI metadata to the narrow reference. Do not create a Registry entry.

- [ ] **Step 3: Update the canonical startup JSON**

Insert a valid awaiting `prompt_approval_gate` before the existing benchmark, hygiene, and PM sibling fields. Document the `prepare` command, the confirmation update, digest writeback, then the `start` command.

- [ ] **Step 4: Update contract tests**

Make the cold-start fixture assert that the unfilled/awaiting template is invalid for `start` but valid for `prepare`; after filling and computing the digest, set confirmed approval and assert `start` is valid. Expand first-prompt tests to require the new reference and machine-gate marker.

- [ ] **Step 5: Run contract tests**

```bash
python -m unittest tests.test_first_prompt_intake_contract tests.test_pm_cold_start_contract tests.test_prompt_approval_execution_gate -v
```

Expected: PASS.

- [ ] **Step 6: Commit the owner propagation**

```bash
git add AGENTS.md skills/managing-project-intake-and-work-contract docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md tests/test_first_prompt_intake_contract.py tests/test_pm_cold_start_contract.py
git commit -m "docs: route prompt confirmation through the execution gate"
```

### Task 4: Active consumer and regression propagation

**Files:**
- Modify only the active startup/adapter files identified by fresh search that invoke `validate_work_contract_receipt.py` or describe L1+ execution authorization.
- Test: `tests/test_pm_cold_start_contract.py`
- Test: `tests/test_prompt_approval_execution_gate.py`
- Modify: existing reference-freshness or consolidated contract test only when required by current owner rules.

**Interfaces:**
- Consumes: canonical reference path and CLI phases from Tasks 2–3.
- Produces: all active consumers route preparation through `--phase prepare` and mutation through confirmed `--phase start` or `resume`.

- [ ] **Step 1: Inventory active consumers**

Run:

```bash
git grep -n "validate_work_contract_receipt.py --receipt\|AWAITING_USER_CONFIRMATION\|first-prompt.*contract.*clarify" -- AGENTS.md docs skills templates tests
```

Classify each result as `ACTIVE_OWNER`, `ACTIVE_CONSUMER`, `COMPATIBILITY`, `ARCHIVE`, or `UNKNOWN_UNVERIFIED` and change only active paths.

- [ ] **Step 2: Propagate the minimal marker and route**

Update active project-start, Codex starter, AI workflow, adapter/router, planning, and work-item consumers so they cannot describe `start` as available before confirmation. Link to the canonical reference instead of copying the whole schema.

- [ ] **Step 3: Add omission and stale-route tests**

Assert every active consumer names `PROMPT_APPROVAL_EXECUTION_GATE_REQUIRED`, points to the canonical reference or startup receipt, and preserves `--expected-source-sha`. Add negative mutations that remove the marker, change `prepare` to `start` before confirmation, or make an untrusted context source an approval authority; each mutation must fail.

- [ ] **Step 4: Run the propagated suite**

```bash
python -m unittest tests.test_prompt_approval_execution_gate tests.test_pm_cold_start_contract tests.test_first_prompt_intake_contract tests.test_project_work_tracking -v
```

Then run the directly affected existing suites discovered by `git grep`.

- [ ] **Step 5: Commit active-consumer propagation**

```bash
git add AGENTS.md docs skills templates tests
git commit -m "test: enforce prompt approval across active consumers"
```

### Task 5: Five full-scope adversarial loops and exact-head verification

**Files:**
- Create: `docs/reviews/2026-09-03-prompt-approval-execution-gate-adversarial-review.yml`
- Modify: task files only for validated findings.
- Modify: `docs/reviews/2026-09-03-prompt-approval-execution-gate-work-receipt.json`

**Interfaces:**
- Consumes: final candidate branch and `templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml`.
- Produces: five or more complete loop records, corrected candidate, and closeout-ready receipt.

- [ ] **Step 1: Run focused and repository validation**

```bash
python -m unittest tests.test_prompt_approval_execution_gate tests.test_project_work_tracking tests.test_pm_cold_start_contract tests.test_first_prompt_intake_contract -v
python tools/run_local_validation.py --trusted-history-commit 850204b3e5de81a4045111b4a050c46c5a292b59
```

Record exact commands, head, and results. Do not label an unavailable check as PASS.

- [ ] **Step 2: Execute adversarial loops 1–5**

For every loop, reread the entire diff and cover user intent, authority, actual consumer propagation, malformed input, approval spoofing, contract drift, backward compatibility, question fatigue, rollback, lifecycle cost, and evidence limits. Validate each criticism, apply only valid findings, rerun affected tests, search for a better in-scope alternative, and re-attack the resulting state.

- [ ] **Step 3: Continue beyond five when required**

Any new valid `MUST_FIX`, acceptance blocker, canon/consumer drift, evidence-ceiling violation, or better in-scope alternative reopens implementation and requires another full loop.

- [ ] **Step 4: Run negative mutations**

Mutate one field at a time in temporary copies: remove gate, set awaiting at start, alter contract after approval, alter digest, use invalid authority, add unresolved decision, set later conflict true, omit source authority, and mark scope changed. Each must fail for the expected reason. Restore normal files and rerun GREEN.

- [ ] **Step 5: Update work receipt for exact candidate HEAD**

Mark required checks PASS only with evidence, set remaining counters to zero only after readback, and use the independently read candidate HEAD as `verified_head_sha`.

- [ ] **Step 6: Commit review evidence**

```bash
git add docs/reviews tests tools skills templates AGENTS.md docs/knowledge
git commit -m "test: adversarially verify prompt approval gate"
```

### Task 6: PR review, normal integration, and post-merge correction scan

**Files:**
- Pull request metadata and review conversation.
- Repository files only for validated exact-head findings.

**Interfaces:**
- Consumes: verified branch head and current completed `main`.
- Produces: reviewed normal squash merge and post-merge main readback, or an exact blocker report.

- [ ] **Step 1: Reconcile current main and same-goal work**

Fetch the latest completed `main`, confirm this branch remains a descendant or normally update it without force, and recheck same-goal open/recent PRs. Do not absorb unrelated open work.

- [ ] **Step 2: Open the PR**

Create a non-draft PR describing the approval reference, baseline, exact head, changed scope, benchmark disposition, RED→GREEN evidence, five-loop review, evidence ceiling, rollback, and required merge gates.

- [ ] **Step 3: Verify exact-head CI and independent review**

Require all current repository checks, current-head independent review, and zero unresolved valid review threads. Correct findings through the same owner, rerun tests, and obtain new exact-head evidence after every change.

- [ ] **Step 4: Finish the branch**

Before claiming completion, run the repository's final verification, confirm squash-only policy and no bypass, then merge with expected head. Never merge while required current-head review or CI is pending or failing.

- [ ] **Step 5: Post-merge readback**

Read the new `main` commit, owner files, validator, canonical startup example, tests, PR state, and workflow results. Recalculate remaining work and run the final correction/omission/conflict scan.

- [ ] **Step 6: Report evidence ceilings separately**

Report document, static, automated test, CI, post-merge readback, runtime, human UX, and user approval states separately. Prompt-quality and question-fatigue outcomes remain `NOT_RUN` until observed in real tasks.