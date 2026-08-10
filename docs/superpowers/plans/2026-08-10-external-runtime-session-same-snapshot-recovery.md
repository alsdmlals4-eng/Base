# External Runtime Session Same-Snapshot Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add BCP-015's fail-closed same-snapshot external runtime-session recovery classification to existing Godot Live Editor and Handoff responsibilities.

**Architecture:** Keep `GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md` as the sole recovery authority. Extend only its project-facing adapter README and the Handoff stale-identity boundary; focused tests preserve the separation. Do not introduce a Skill, schema, runtime implementation, or external transport.

**Tech Stack:** Markdown, Python 3 standard-library `unittest`, existing Base proposal lifecycle validator.

## Global Constraints

- Generic Base guidance must not contain OMENWARD-specific PID, port, path, session ID, PR/Issue, feature, or metric data.
- All recovery classifications require a bounded same observation window; incomplete evidence is `BLOCKED_UNVERIFIED`.
- Do not alter `skills/SKILL_REGISTRY.json`, release locks, generated release artifacts, schemas, validators, network behavior, or product repositories.
- Keep external-session recovery separate from product/runtime test, human QA, release, and production-readiness evidence.
- Update BCP lifecycle state and implementation link only after the implementation PR has actually merged.

---

### Task 1: Lock canonical recovery classification with a RED test

**Files:**

- Create: `tests/test_external_runtime_session_recovery_contract.py`
- Modify: `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md`

**Interfaces:**

- Consumes: the existing canonical Godot Live Editor recovery source.
- Produces: `ExternalRuntimeSessionRecoveryContractTests.test_canonical_recovery_contract_requires_same_snapshot_evidence_and_fail_closed_classification`.

- [ ] **Step 1: Write the failing test**

```python
def test_canonical_recovery_contract_requires_same_snapshot_evidence_and_fail_closed_classification(self) -> None:
    source = read("docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md")
    for token in (
        "TARGET_PROCESS_IDENTITY",
        "TARGET_TRANSPORT_OWNERSHIP",
        "SERVER_HANDSHAKE_AND_SESSION_LOGS",
        "IMMEDIATE_SESSION_REGISTRY_READ",
        "EXACT_SESSION_RECOVERED",
        "SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER",
        "PROCESS_OR_TRANSPORT_BLOCKER",
        "BLOCKED_UNVERIFIED",
    ):
        self.assertIn(token, source)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_external_runtime_session_recovery_contract.ExternalRuntimeSessionRecoveryContractTests.test_canonical_recovery_contract_requires_same_snapshot_evidence_and_fail_closed_classification -v`

Expected: FAIL because no current canonical source declares the four BCP-015 evidence names and classifications.

- [ ] **Step 3: Write minimal implementation**

Add one `External runtime session same-snapshot recovery` section to the canonical recovery source. Define the four evidence inputs, four classifications, `PROCESS_EXITED_OR_NO_LONGER_RUNNING` with `REASON = UNVERIFIED`, and product-Green separation.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_external_runtime_session_recovery_contract.ExternalRuntimeSessionRecoveryContractTests.test_canonical_recovery_contract_requires_same_snapshot_evidence_and_fail_closed_classification -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_external_runtime_session_recovery_contract.py docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md
git commit -m "feat: classify external runtime recovery"
```

### Task 2: Guard shared server and stale identity consumers with RED tests

**Files:**

- Modify: `tests/test_external_runtime_session_recovery_contract.py`
- Modify: `tests/test_gpt_codex_workflow_contract.py`
- Modify: `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/README.md`
- Modify: `skills/maintaining-project-context-and-handoff/SKILL.md`
- Modify: `skills/maintaining-project-context-and-handoff/LEARNING_LOG.md`

**Interfaces:**

- Consumes: canonical classification from Task 1.
- Produces: project-adapter recovery guidance and a handoff-only stale identity boundary; no external-session implementation capability.

- [ ] **Step 1: Write failing tests**

```python
def test_shared_server_and_stale_identity_rules_prevent_unsafe_resume(self) -> None:
    source = read("docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md")
    for token in (
        "ONE_TARGET_SESSION_MISSING",
        "SHARED_SERVER_SAFE_TO_RESTART",
        "PAST_PID != CURRENT_TARGET",
        "PAST_WS_CONNECTION != CURRENT_TRANSPORT_PROOF",
        "PAST_SESSION_ID != CURRENT_REGISTRY_PROOF",
        "SESSION_RECOVERY_GREEN",
        "project tests/runtime validation remain separate",
    ):
        self.assertIn(token, source)

def test_adapter_and_handoff_keep_distinct_recovery_responsibilities(self) -> None:
    adapter = read("templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/README.md")
    handoff = read("skills/maintaining-project-context-and-handoff/SKILL.md")
    self.assertIn("same-snapshot", adapter)
    self.assertIn("external transport", adapter)
    self.assertIn("stale PID/session", handoff)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m unittest tests.test_external_runtime_session_recovery_contract.ExternalRuntimeSessionRecoveryContractTests.test_shared_server_and_stale_identity_rules_prevent_unsafe_resume tests.test_external_runtime_session_recovery_contract.ExternalRuntimeSessionRecoveryContractTests.test_adapter_and_handoff_keep_distinct_recovery_responsibilities -v`

Expected: FAIL because the exact BCP-015 shared-session/stale-identity rules and focused consumer links are absent.

- [ ] **Step 3: Write minimal implementation**

Add the exact shared-server and stale-identity formulas plus safety prohibitions to the canonical recovery document. Add one adapter README note that a network-disabled in-process addon cannot diagnose external sessions and must use the canonical same-snapshot procedure when an external server exists. Add one Handoff sentence that historical PID/session values are evidence only and require fresh reads before current authority or mutation selection. Record this scope-bounded reusable lesson in the Handoff Skill Learning Log.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m unittest tests.test_external_runtime_session_recovery_contract tests.test_gpt_codex_workflow_contract -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/test_external_runtime_session_recovery_contract.py templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/README.md skills/maintaining-project-context-and-handoff/SKILL.md skills/maintaining-project-context-and-handoff/LEARNING_LOG.md
git commit -m "docs: guard runtime session recovery"
```

### Task 3: Validate scope, regressions, and lifecycle readiness

**Files:**

- Modify: `docs/superpowers/specs/2026-08-10-external-runtime-session-same-snapshot-recovery-design.md`
- Modify: `docs/superpowers/plans/2026-08-10-external-runtime-session-same-snapshot-recovery.md`

**Interfaces:**

- Consumes: Tasks 1–2 and fetched `origin/main` SHA.
- Produces: a verified implementation commit ready for a separate implementation PR; Proposal Registry remains `APPROVED_FOR_IMPLEMENTATION` until merge.

- [ ] **Step 1: Run focused contract and lifecycle tests**

Run: `python -m unittest tests.test_external_runtime_session_recovery_contract tests.test_base_change_proposals tests.test_godot_live_editor_contract_v2 tests.test_godot_live_editor_contract_v2_adversarial tests.test_godot_live_editor_runtime_contract_hardening -v`

Expected: PASS using the repository's Python environment with `jsonschema` installed.

- [ ] **Step 2: Run canonical-reference freshness**

Run: `python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base 0d1cebdec0e1f3b660688ec194dcc27054dcfc2d --head HEAD`

Expected: PASS with no active stale reference from the recovery source, template, or handoff consumer.

- [ ] **Step 3: Run adversarial mutation**

Temporarily remove `TARGET_TRANSPORT_OWNERSHIP` from the canonical document, run the Task 1 focused test and observe its expected failure, then restore the exact file bytes and re-run the focused test.

- [ ] **Step 4: Inspect scope and record test evidence**

Run: `git diff --check origin/main...HEAD && git diff --name-only origin/main...HEAD && git status --short`

Expected: no whitespace error; only the plan/spec, focused test, canonical recovery source, adapter README, and Handoff source changed; clean worktree after commit.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/2026-08-10-external-runtime-session-same-snapshot-recovery-design.md docs/superpowers/plans/2026-08-10-external-runtime-session-same-snapshot-recovery.md
git commit -m "docs: record runtime recovery implementation plan"
```

### Task 4: Publish and close lifecycle after remote validation

**Files:**

- Modify after PR merge only: `[수정제안서]/PROPOSAL_REGISTRY.json`
- Modify after PR merge only: `[수정제안서]/BCP-2026-015-external-runtime-session-same-snapshot-recovery/PROPOSAL.md`

**Interfaces:**

- Consumes: a merged implementation PR URL and exact merge commit.
- Produces: `IMPLEMENTED` lifecycle records referencing the actual PR.

- [ ] **Step 1: Create a draft implementation PR from the verified single-purpose commit**

Expected: the original BCP submission and active Base implementation remain separated.

- [ ] **Step 2: Confirm exact head, required CI, review, unresolved threads, and mergeability**

Expected: all required checks pass; no unresolved review thread or blocking finding.

- [ ] **Step 3: Squash-merge under inherited approval authority**

Expected: the user-approved BCP scope is merged without a direct `main` push.

- [ ] **Step 4: Create the lifecycle closeout only with the actual implementation PR link**

Expected: Registry and BCP status move from `APPROVED_FOR_IMPLEMENTATION` to `IMPLEMENTED` without invented PR data.
