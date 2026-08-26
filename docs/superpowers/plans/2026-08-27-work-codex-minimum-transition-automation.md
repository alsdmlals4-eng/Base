# Work-Codex Minimum-Transition Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicit opt-in Work v4.9 execution profile that completes current-Slice production inputs in Work, performs one consolidated Codex implementation window, prioritizes adopted GUT/Hera machine QA, reaches scope-bounded machine-executable remaining work zero, and hands the resulting vertical slice to the user for actual validation.

**Architecture:** Preserve the existing Work v4.9 main instruction and current domain owners. Add one project-operation profile under `templates/project-operations/`, route it from the existing Compatibility Appendix only when explicit user delegation exists, and protect the behavior with a focused Python contract. Default per-image approval, high-risk confirmation, Human/Player evidence ceilings, Work/Codex ownership, HiGodot/GUT/Hera boundaries, and exact-head merge gates remain unchanged outside the opt-in profile.

**Tech Stack:** Markdown execution contracts, Python `unittest`, GitHub Actions Base regression, GitHub ruleset `ci-gate`.

**Spec:** Proposal PR #729, path `[수정제안서]/BCP-2026-038-work-codex-minimum-transition-automation/PROPOSAL.md`, approval reference `2026-08-27 current ChatGPT Work conversation`.

## Global Constraints

- Baseline completed `main`: `43b3ffb2c5b026e3d4a38dab2338585894d36f61`.
- `OPEN_PR_READ_ONLY_BY_DEFAULT`: all pre-existing open/draft/ready PRs remain read-only.
- No new Skill, provider, paid dependency, executor, second project canon, Registry entry, or engine migration.
- Default image conversation approval remains unchanged unless explicit `DELEGATED_RECOMMENDED_DEFAULT_APPROVAL` evidence exists.
- Work remains planning/research/review/visual/non-product owner; Codex remains actual game-product implementation owner.
- HiGodot remains sole persistent authoring authority; GUT is deterministic GDScript testing when adopted; Hera is live QA/observability only.
- Machine evidence never becomes Human/Player PASS.
- `remaining work 0` means the current approved Slice and automation phase, not the whole roadmap.
- Irreversible data loss, account/security expansion, new paid cost, legal/rights uncertainty, public release, project-core replacement, broad engine/save migration, force/direct-main/admin bypass remain deferred.
- Merge requires current main reconciliation, exact reviewed head, current required checks, unresolved threads 0, squash merge, and post-merge readback.

---

### Task 1: Prove the missing behavior with a focused RED contract

**Files:**
- Create: `tests/test_work_codex_minimum_transition_automation_contract.py`

**Interfaces:**
- Consumes: Work v4.9 Compatibility Appendix.
- Produces: six deterministic assertions covering profile discovery, three-stage order, delegated routine approval, high-risk deferral, stall fallback, scope-bounded zero, GUT/Hera machine QA, and Human/Player separation.

- [x] **Step 1: Write the test before production implementation**

The test uses these exact paths:

```python
ROOT = Path(__file__).resolve().parents[1]
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
```

It requires these machine literals:

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
WORK_PRODUCTION_INPUT_BATCH
MINIMIZE_WORK_CODEX_TRANSITIONS
CODEX_SINGLE_IMPLEMENTATION_WINDOW
CONSOLIDATED_RETURN_PACKET
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
NO_AUTOMATIC_SCOPE_EXPANSION
STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY
DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO
COMPLETION_CANDIDATE_RESCAN
MACHINE_QA_FIRST
GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED
HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED
HERA_PERSISTENT_AUTHORING_FORBIDDEN
HERA_PHASE_SOURCE_DELTA_NONE
HUMAN_QA_DEFERRED_BY_CURRENT_USER
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
AUTOMATED_VERTICAL_SLICE_READY
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION
WORK_NONPRODUCT_OWNER_PRESERVED
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED
CURRENT_SLICE_ONLY
HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED
```

- [x] **Step 2: Verify RED on the test-only head**

Run:

```bash
python -m unittest tests.test_work_codex_minimum_transition_automation_contract -v
```

Verified exact corrected RED head:

```text
25195a44c420b73f4ef886a15d93008675224e63
```

Observed result:

```text
Ran 6 tests
FAILED (failures=6, errors=0)
Reason: opt-in minimum-transition profile did not exist
```

The first test revision produced `FileNotFoundError`; it was corrected before production implementation so the missing contract reports assertion failures rather than test errors.

---

### Task 2: Add the opt-in minimum-transition execution profile

**Files:**
- Create: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`

**Interfaces:**
- Consumes: current Work v4.9, continuous-work, GPT–Codex, Visual, Vertical Slice, and HiGodot/GUT/Hera owners.
- Produces: a project-operation composition profile; it does not become a new Skill or second canon.

- [x] **Step 1: Define activation and owner preservation**

The header must contain:

```text
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_SLICE_ONLY
WORK_NONPRODUCT_OWNER_PRESERVED
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED
HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION
NO_AUTOMATIC_SCOPE_EXPANSION
```

- [x] **Step 2: Define the three-stage flow in this exact order**

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
→ CODEX_SINGLE_IMPLEMENTATION_WINDOW
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

- [x] **Step 3: Define `WORK_PRODUCTION_INPUT_PACKET`**

The packet must contain exact Project/Slice identity, player promise and choice, scope/non-scope/protected scope, planning/rules, UI/UX Flow, data/state, actual-consumer Visual and Audio records, VFX, localization/accessibility, provenance/rights, acceptance, deterministic tests, runtime QA, build/export checks, canon updates, rollback, blockers, evidence ceiling, and readiness.

- [x] **Step 4: Define delegated Visual and Audio production**

Visual production requires an actual consumer, bounded count and independent briefs, approved direction/reference, technical format/import requirements, protected identity, excluded scope, objective acceptance, provenance/rights, durable destination, and runtime validation.

Audio production requires an actual cue consumer, trigger/stop semantics, information/emotion role, existing reuse decision, actual file or approved procedural specification, technical format/loop/loudness, provenance/rights, durable destination, and runtime validation.

- [x] **Step 5: Define routine approval and high-risk deferral**

Routine decisions inside the current approved Slice use:

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
```

High-risk actions use:

```text
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
IRREVERSIBLE_DATA_LOSS
ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION
NEW_PAID_COST
LEGAL_OR_RIGHTS_UNCERTAINTY
PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION
FORCE_DIRECT_MAIN_ADMIN_BYPASS
PROJECT_CORE_IDENTITY_REPLACEMENT
BROAD_ENGINE_OR_SAVE_BREAKING_MIGRATION
```

Blocked high-risk work is deferred locally; independent ready work continues; the remaining decisions are bundled for one later user decision.

- [x] **Step 6: Define stall signals and evidence-equivalent fallback**

Required flow:

```text
current-state readback
→ root-cause classification
→ bounded safe retry
→ authorized fallback A
→ authorized fallback B
→ evidence-equivalent local/manual route
→ blocked task local defer
→ independent ready work continue
→ deferred re-evaluation
→ global stop last
```

No elapsed-time constant, infinite retry, source substitution by memory/snippet, security downgrade, or evidence downgrade is allowed.

- [x] **Step 7: Define `CONSOLIDATED_RETURN_PACKET`**

The packet contains exact baseline/head, completed implementation, changed files/reasons, deterministic tests, runtime QA, build/export checks, Visual/Audio consumption, missing inputs, change proposals, high-risk items, independent remaining work, failed/not-run tests, evidence locations, evidence ceiling, and one bounded Work re-entry classification.

- [x] **Step 8: Define GUT/Hera machine QA and evidence ceiling**

```text
MACHINE_QA_FIRST
GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED
HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED
HERA_PERSISTENT_AUTHORING_FORBIDDEN
HERA_PHASE_SOURCE_DELTA_NONE
HUMAN_QA_DEFERRED_BY_CURRENT_USER
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

- [x] **Step 9: Define scope-bounded remaining-work zero**

Machine-executable work for the current approved Slice must reach zero, then `COMPLETION_CANDIDATE_RESCAN` re-checks implementation, canon, asset consumers, tests, QA, PR/merge/readback, high-risk blockers, and evidence ceiling before final adversarial review.

---

### Task 3: Route the profile from the Work v4.9 Compatibility Appendix

**Files:**
- Modify: `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`

**Interfaces:**
- Consumes: the Task 2 profile.
- Produces: explicit opt-in discovery without altering default Work behavior.

- [x] **Step 1: Append `Explicit Delegated Minimum-Transition Profile`**

The section must contain:

```text
EXPLICIT_USER_DELEGATION_REQUIRED
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
```

- [x] **Step 2: Preserve non-activation behavior**

Without explicit delegation, default v4.9, default image-conversation approval, and current Project user-decision gates remain active. More specific user restrictions and host/system/tool confirmations always win.

- [x] **Step 3: Prove the previous appendix was preserved byte-for-byte as a prefix**

The original appendix blob is:

```text
1cf2cc79db3fed8ccea00e975a0070d69419b05a
```

The pre-section prefix of the changed appendix hashes to the same Git blob, proving the change is append-only rather than a silent rewrite.

---

### Task 4: Verify exact changed files and repository gates

**Files:**
- Test: `tests/test_work_codex_minimum_transition_automation_contract.py`
- Verify: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- Verify: `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`
- Verify: `tests/test_chatgpt_work_project_instruction_contract.py`

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: focused exact-file evidence plus repository exact-head CI evidence.

- [x] **Step 1: Verify local reconstruction matches remote Git blobs**

Run:

```bash
git hash-object templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
git hash-object templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
git hash-object tests/test_work_codex_minimum_transition_automation_contract.py
```

Expected exact blobs:

```text
e6af8207af3c81bf878e5f217eab2ca4a6c79052
55ac4a7cd5993ce65fe048adae9345b2b0f1e9c5
658b9d8e326567f12470f51a1735536715ff7795
```

- [x] **Step 2: Run the focused GREEN contract**

```bash
python -m unittest tests.test_work_codex_minimum_transition_automation_contract -v
```

Expected and observed on the exact changed blobs:

```text
Ran 6 tests
OK
```

- [ ] **Step 3: Run existing Work v4.9 non-regression**

```bash
python -m unittest tests.test_chatgpt_work_project_instruction_contract -v
```

The main instruction and P08 files are unchanged; the existing appendix is preserved as an exact prefix. Fresh exact-head repository execution is still required before merge.

- [ ] **Step 4: Run full Base regression and Skill coverage**

```bash
python -m unittest discover -s tests -v
python tools/check_skill_system_coverage.py
```

- [ ] **Step 5: Run canonical freshness and whitespace checks**

```bash
BASE_SHA=$(git rev-parse origin/main)
HEAD_SHA=$(git rev-parse HEAD)
python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base "$BASE_SHA" --head "$HEAD_SHA"
git diff --check "$BASE_SHA...$HEAD_SHA"
```

If local repository execution is unavailable, the exact-head repository-required CI result supplies these gates; local execution remains `NOT_RUN` rather than being inferred.

---

### Task 5: Adversarial closeout, merge, and post-merge readback

**Files:**
- Review: all four implementation PR files.
- Readback: merged `main` versions of profile, appendix, focused test, and plan.

**Interfaces:**
- Consumes: verified exact implementation head.
- Produces: safely merged Base behavior and a final completion receipt.

- [ ] **Step 1: Perform at least five full-scope adversarial loops**

Every loop re-checks user intent, opt-in boundary, approval safety, Work/Codex ownership, Visual/Audio production, stall fallback, remaining-work zero, GUT/Hera evidence ceiling, open-PR concurrency, CI/ruleset, rollback, and long-term context cost.

- [ ] **Step 2: Reconcile latest completed main and same-goal PRs**

Use GitHub compare/PR APIs. Pre-existing PR branches remain read-only; only already merged `main` changes may become the new baseline.

- [ ] **Step 3: Verify exact-head merge gates**

Read the PR API immediately before merge and record its current head SHA. Require current `ci-gate` PASS, unresolved threads 0, review blockers 0, conflict 0, and no high-risk deferred blocker.

- [ ] **Step 4: Squash merge using the immediately read PR head as `expected_head_sha`**

No direct main, force, rebase rewrite, admin, or ruleset bypass.

- [ ] **Step 5: Read back new main**

Fetch the default branch, confirm the merge SHA is current, fetch all changed files from new main, and consume post-merge CI/readback evidence.

- [ ] **Step 6: Report before→after→expected effect and remaining work**

Report exact Base baseline, RED and GREEN evidence, changed paths, benchmark disposition, adversarial findings, required checks, merge SHA, post-merge readback, `NOT_RUN` boundaries, proposal lifecycle state, and remaining required work for the approved Base scope.
