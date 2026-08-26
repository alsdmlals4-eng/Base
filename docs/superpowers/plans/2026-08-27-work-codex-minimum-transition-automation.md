# Work-Codex Minimum-Transition Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicit opt-in Work v4.9 execution profile that completes current-Slice production inputs in Work, performs one consolidated Codex implementation window, prioritizes adopted GUT/Hera machine QA, reaches scope-bounded machine-executable remaining work zero, and hands the resulting vertical slice to the user for actual validation.

**Architecture:** Keep the existing Work v4.9 main instruction and all domain owners intact. Add one focused project-operation profile that composes current continuous-work, GPT–Codex, Visual, Vertical Slice, and HiGodot/GUT/Hera contracts; route it from the existing compatibility appendix only when the current user has explicitly delegated routine approvals. Protect the behavior with a focused repository contract test and preserve default per-image approval, high-risk confirmation, Human/Player evidence ceilings, and current-task exact-head merge gates.

**Tech Stack:** Markdown execution contracts, Python `unittest`, GitHub Actions Base regression, GitHub ruleset `ci-gate`.

**Spec:** `[수정제안서]/BCP-2026-038-work-codex-minimum-transition-automation/PROPOSAL.md` in proposal PR #729, approval reference `2026-08-27 current ChatGPT Work conversation`.

## Global Constraints

- `OPEN_PR_READ_ONLY_BY_DEFAULT`: all pre-existing open/draft/ready PRs remain read-only.
- No new Skill, provider, paid dependency, executor, second project canon, Registry entry, or engine migration.
- Default image conversation approval remains unchanged unless explicit `DELEGATED_RECOMMENDED_DEFAULT_APPROVAL` activation exists.
- Work remains planning/research/review/visual/non-product owner; Codex remains actual game-product implementation owner.
- HiGodot remains sole persistent authoring authority; GUT is deterministic GDScript testing when adopted; Hera is live QA/observability only.
- Machine evidence must not be promoted to Human/Player PASS.
- `remaining work 0` means current approved Slice and automation phase, not the entire project roadmap.
- High-risk destructive, data-loss, security, account, payment, legal/rights, public-release, force/direct-main/admin-bypass actions remain deferred.
- Repository merge must use exact reviewed head, current required checks, squash merge, and post-merge main readback.

---

### Task 1: Add the RED contract for the opt-in automation profile

**Files:**
- Create: `tests/test_work_codex_minimum_transition_automation_contract.py`

**Interfaces:**
- Consumes: existing Work bundle paths `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md` and `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`.
- Produces: a focused failing contract that requires the new profile path, explicit opt-in routing, three-stage flow, delegated routine approval with high-risk deferral, stall fallback, scope-bounded zero, GUT/Hera machine QA, and separate user validation.

- [ ] **Step 1: Create the focused test with exact required literals**

```python
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"


class WorkCodexMinimumTransitionAutomationContractTests(unittest.TestCase):
    def test_profile_is_discoverable_from_the_work_bundle(self) -> None:
        appendix = APPENDIX.read_text(encoding="utf-8")
        self.assertTrue(PROFILE.exists(), "opt-in minimum-transition profile must exist")
        self.assertIn("WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md", appendix)
        self.assertIn("EXPLICIT_USER_DELEGATION_REQUIRED", appendix)

    def test_profile_defines_three_stage_minimum_transition_flow(self) -> None:
        text = PROFILE.read_text(encoding="utf-8")
        for token in (
            "WORK_PREP_COMPLETION_BEFORE_CODEX",
            "WORK_PRODUCTION_INPUT_BATCH",
            "MINIMIZE_WORK_CODEX_TRANSITIONS",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "CONSOLIDATED_RETURN_PACKET",
            "READY_FOR_USER_VERTICAL_SLICE_VALIDATION",
        ):
            self.assertIn(token, text)
        self.assertLess(text.index("WORK_PREP_COMPLETION_BEFORE_CODEX"), text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"))
        self.assertLess(text.index("CODEX_SINGLE_IMPLEMENTATION_WINDOW"), text.index("READY_FOR_USER_VERTICAL_SLICE_VALIDATION"))

    def test_routine_approval_is_delegated_but_high_risk_remains_deferred(self) -> None:
        text = PROFILE.read_text(encoding="utf-8")
        for token in (
            "DELEGATED_RECOMMENDED_DEFAULT_APPROVAL",
            "NO_ROUTINE_APPROVAL_STOPS",
            "HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE",
            "HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE",
            "NO_AUTOMATIC_SCOPE_EXPANSION",
        ):
            self.assertIn(token, text)
        for risk in (
            "IRREVERSIBLE_DATA_LOSS",
            "ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION",
            "NEW_PAID_COST",
            "LEGAL_OR_RIGHTS_UNCERTAINTY",
            "PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION",
            "FORCE_DIRECT_MAIN_ADMIN_BYPASS",
        ):
            self.assertIn(risk, text)

    def test_stall_recovery_and_scope_bounded_zero_are_explicit(self) -> None:
        text = PROFILE.read_text(encoding="utf-8")
        for token in (
            "STALL_SIGNAL_ROUTE_SWITCH",
            "BOUNDED_RETRY_THEN_FALLBACK",
            "EVIDENCE_EQUIVALENT_FALLBACK_ONLY",
            "DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK",
            "SCOPE_BOUNDED_REQUIRED_WORK_ZERO",
            "AUTOMATION_PHASE_REMAINING_WORK_ZERO",
            "COMPLETION_CANDIDATE_RESCAN",
        ):
            self.assertIn(token, text)

    def test_machine_qa_is_required_without_claiming_human_or_player_pass(self) -> None:
        text = PROFILE.read_text(encoding="utf-8")
        for token in (
            "MACHINE_QA_FIRST",
            "GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED",
            "HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED",
            "HERA_PERSISTENT_AUTHORING_FORBIDDEN",
            "HERA_PHASE_SOURCE_DELTA_NONE",
            "HUMAN_QA_DEFERRED_BY_CURRENT_USER",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
            "AUTOMATED_VERTICAL_SLICE_READY",
        ):
            self.assertIn(token, text)

    def test_default_approval_and_owner_boundaries_are_preserved(self) -> None:
        text = PROFILE.read_text(encoding="utf-8")
        for token in (
            "OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT",
            "DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION",
            "WORK_NONPRODUCT_OWNER_PRESERVED",
            "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED",
            "CURRENT_SLICE_ONLY",
            "HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Open a draft PR and run the focused test on the test-only head**

Run through repository CI or an equivalent exact-head environment:

```bash
python -m unittest tests.test_work_codex_minimum_transition_automation_contract -v
```

Expected: FAIL because `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md` does not exist and the compatibility appendix does not route to it.

- [ ] **Step 3: Record the exact RED head and failure reason in the PR body**

Expected record:

```text
RED head: <exact SHA>
Expected failure: missing opt-in profile and Work-bundle route
Existing Work v4.9 non-regression remains unchanged
```

---

### Task 2: Implement the minimum-transition project-operation profile

**Files:**
- Create: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`

**Interfaces:**
- Consumes: current Work v4.9 bundle, `continuous-work-execution.md`, `docs/GPT_CODEX_WORKFLOW_POLICY.md`, `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`, `IMAGE_CONVERSATION_APPROVAL_GATE.md`, `designing-vertical-slices`, and `HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`.
- Produces: an opt-in profile with the exact machine literals asserted by Task 1 and a bounded `WORK_PRODUCTION_INPUT_PACKET` plus `CONSOLIDATED_RETURN_PACKET`.

- [ ] **Step 1: Write the profile header and authority boundaries**

The file must start with:

```markdown
# Work↔Codex 최소 전환 버티컬 슬라이스 실행 프로필

```text
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_SLICE_ONLY
WORK_NONPRODUCT_OWNER_PRESERVED
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED
HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
```
```

- [ ] **Step 2: Add the three-stage flow and Work production-input packet**

Include the exact order:

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
→ CODEX_SINGLE_IMPLEMENTATION_WINDOW
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

Include a packet containing planning/rules, UI/UX Flow, data/state, actual-consumer visual assets, audio assets or approved procedural specs, VFX feedback, provenance/rights, acceptance, deterministic tests, runtime QA scenarios, build/export checks, rollback, and blockers.

- [ ] **Step 3: Add delegated approval with high-risk batch deferral**

Include:

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
NO_AUTOMATIC_SCOPE_EXPANSION
```

List the exact high-risk literals asserted by Task 1 and require local deferral plus independent continuation before a bundled user decision.

- [ ] **Step 4: Add stall signals and fallback ladder**

Include bounded retry, current-state readback, fallback A/B, evidence-equivalent manual/local route, local defer, independent continuation, and global stop last. Do not hardcode an elapsed-time threshold.

- [ ] **Step 5: Add the consolidated Codex return packet**

The packet must include completed implementation, machine QA, missing inputs, change proposals, high-risk deferred items, independent remaining work, evidence identity, and whether one Work re-entry is required.

- [ ] **Step 6: Add machine QA and user-validation evidence ceiling**

Require adopted GUT for deterministic tests and adopted Hera for live run/input/state/UI/screenshot/diagnostics with persistent authoring forbidden and source delta `NONE`. Keep Human Usability and Player Experience `NOT_RUN` until the user actually plays.

- [ ] **Step 7: Add scope-bounded remaining-work zero and completion rescan**

Machine-executable required work for the current Slice must reach zero, then re-scan implementation, canon, asset consumers, tests, QA, PR, merge, and readback. Explicit user validation is the next milestone rather than a hidden machine task.

---

### Task 3: Route the profile from the Work v4.9 compatibility appendix

**Files:**
- Modify: `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`

**Interfaces:**
- Consumes: the profile created in Task 2.
- Produces: explicit opt-in discovery without replacing the default Work bundle.

- [ ] **Step 1: Append a section titled `Explicit Delegated Minimum-Transition Profile`**

Include:

```text
EXPLICIT_USER_DELEGATION_REQUIRED
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
```

and the exact path:

```text
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
```

- [ ] **Step 2: State activation and non-activation conditions**

Activation requires the current user to explicitly delegate routine approvals and request Work↔Codex transition minimization. Without that evidence, default Work v4.9 and default image conversation approval remain active.

- [ ] **Step 3: State priority and conflict handling**

The profile composes current owners; current Project canon and more specific user restrictions still win. Host/system/tool confirmations cannot be bypassed.

---

### Task 4: Verify GREEN, non-regression, and plan coverage

**Files:**
- Test: `tests/test_work_codex_minimum_transition_automation_contract.py`
- Test: `tests/test_chatgpt_work_project_instruction_contract.py`
- Verify: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- Verify: `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: exact-head focused and whole-repository evidence.

- [ ] **Step 1: Run the focused GREEN test**

```bash
python -m unittest tests.test_work_codex_minimum_transition_automation_contract -v
```

Expected: PASS, 6 tests, 0 failures.

- [ ] **Step 2: Run existing Work v4.9 non-regression**

```bash
python -m unittest tests.test_chatgpt_work_project_instruction_contract -v
```

Expected: PASS, existing tests unchanged.

- [ ] **Step 3: Run full Base discovery and Skill coverage**

```bash
python -m unittest discover -s tests -v
python tools/check_skill_system_coverage.py
```

Expected: exit 0. If the environment cannot run the full suite, use the repository required CI exact-head result and record local execution as `NOT_RUN`, not PASS.

- [ ] **Step 4: Run canonical reference and whitespace checks**

```bash
python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base <current-main-sha> --head <exact-head-sha>
git diff --check <current-main-sha>...<exact-head-sha>
```

Expected: exit 0.

- [ ] **Step 5: Self-review the plan against BCP-2026-038**

Verify every proposal requirement maps to one of Tasks 1–3, no placeholder remains, and no new Skill/provider/Registry owner was introduced.

---

### Task 5: Adversarial review, PR closeout, merge, and post-merge readback

**Files:**
- Review: all files changed by this implementation PR.
- Readback: new `main` versions of the profile, appendix, test, and plan.

**Interfaces:**
- Consumes: verified exact implementation head.
- Produces: merged Base behavior and a post-merge completion receipt.

- [ ] **Step 1: Perform at least five full-scope adversarial loops**

Each loop must re-check the complete approved scope: user intent, opt-in boundary, approval safety, Work/Codex ownership, image/audio production, stall fallback, remaining-work zero, GUT/Hera evidence ceiling, open-PR concurrency, CI/ruleset, rollback, and long-term context cost.

- [ ] **Step 2: Reconcile with latest completed main and same-goal PRs**

Confirm pre-existing PRs remain read-only and no material path/semantic collision invalidates the head.

- [ ] **Step 3: Verify exact-head required checks and review state**

Require current `ci-gate` PASS, unresolved threads 0, review blockers 0, merge conflict 0, and exact reviewed head identity.

- [ ] **Step 4: Squash merge with expected head SHA**

Use repository-supported squash merge only. Do not use direct main, force, admin, or bypass.

- [ ] **Step 5: Read back new main**

Confirm the merge SHA is current `main`, fetch all changed files from new main, and re-run the focused contract or consume the exact post-merge CI evidence.

- [ ] **Step 6: Report before→after→expected effect and remaining work**

Report machine evidence, `NOT_RUN` boundaries, proposal PR lifecycle state, implementation merge SHA, and whether current approved Base scope has required work remaining.
