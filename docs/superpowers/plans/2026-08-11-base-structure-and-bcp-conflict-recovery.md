# Base Structure and BCP Conflict Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the correct BCP collision lineage, restore two evidenced provenance facts lost at distinct BCP-022→023 and BCP-024 rewrite transitions, and publish a durable repository/benchmark audit without adding unnecessary Skills.

**Architecture:** Treat proposal identity as a lineage key rather than a numeric slot. A focused repository test protects the cross-project boundary, the current BCP-024 body carries the restored source evidence, and a separate audit report records broader structure and no-change findings.

**Tech Stack:** Markdown, JSON-backed BCP registry, Python `unittest`, Git history, GitHub PR metadata.

## Global Constraints

- Use current `main` commit `ee8227d1aeae8e159ea2f9c4ba71bb0ff9e4349a` as the audited baseline.
- Do not edit current BCP-023 except if new evidence disproves its byte-identical history.
- Do not add or expand a Skill unless a baseline behavior test fails without the proposed guidance.
- Do not treat skipped environment layers as passing runtime evidence.
- Do not commit, push, create, update, or merge a GitHub PR without explicit authorization for that action.

---

### Task 1: Restore lineage-correct BCP provenance

**Files:**
- Modify: `tests/test_base_change_proposals.py`
- Modify: `[수정제안서]/BCP-2026-024-execution-sandbox-authority-split-recovery/PROPOSAL.md`

**Interfaces:**
- Consumes: proposal entries returned by `check_base_change_proposals.validate_repository(ROOT)`.
- Produces: a regression contract that current BCP-023 is Ten Paces and current BCP-024 retains collision-recovered GRIMOIRE evidence.

- [ ] **Step 1: Write the failing test**

```python
def test_reallocated_bcp_lineage_keeps_distinct_sources_and_recovery_audit(self) -> None:
    registry, errors = CHECKER.validate_repository(ROOT)
    self.assertEqual([], errors)
    entries = {item["proposal_id"]: item for item in registry["proposals"]}
    retained_entry = entries["BCP-2026-023-local-executor-retained-instance-recovery"]
    sandbox_entry = entries["BCP-2026-024-execution-sandbox-authority-split-recovery"]
    retained = (ROOT / retained_entry["path"]).read_text(encoding="utf-8")
    sandbox = (ROOT / sandbox_entry["path"]).read_text(encoding="utf-8")
    self.assertEqual("alsdmlals4-eng/Ten-Paces-Hidden-Moves", retained_entry["source_project"])
    self.assertEqual("alsdmlals4-eng/GRIMOIRE-", sandbox_entry["source_project"])
    self.assertIn("출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`", retained)
    self.assertNotIn("source_project: alsdmlals4-eng/GRIMOIRE-", retained)
    self.assertIn("source_project: alsdmlals4-eng/GRIMOIRE-", sandbox)
    self.assertNotIn("alsdmlals4-eng/Ten-Paces-Hidden-Moves", sandbox)
    self.assertIn("### 충돌 복원 감사", sandbox)
    recovery_audit = sandbox.split("### 충돌 복원 감사", 1)[1].split("## 관찰과 증거", 1)[0]
    self.assertIn("GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01", recovery_audit)
    self.assertIn("HTTP 525", recovery_audit)
    self.assertIn("Star Runtime", recovery_audit)
    for pr_number in (293, 295, 296, 297):
        self.assertIn(f"PR #{pr_number}", recovery_audit)
    self.assertEqual("SUBMITTED", sandbox_entry["status"])
    self.assertIsNone(sandbox_entry["approval_ref"])
    self.assertIn("base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE", sandbox)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run: `.venv/bin/python -m unittest tests.test_base_change_proposals.BaseChangeProposalTests.test_reallocated_bcp_lineage_keeps_distinct_sources_and_recovery_audit -v`

Expected: FAIL because current BCP-024 lacks the explicit `### 충돌 복원 감사` section and recovered evidence markers.

- [ ] **Step 3: Restore the minimum source evidence**

Add the second GRIMOIRE Decision identifier to `## 프로젝트 전용으로 남길 내용`. Extend the Project Verification paragraph with the same-head HTTP 525/Star Runtime recovery, and add a collision-recovery audit that distinguishes the PR #293 BCP-022→PR #295 BCP-023 loss from the PR #296→PR #297 Decision-ID loss.

- [ ] **Step 4: Run focused tests and proposal validation**

Run:

```bash
.venv/bin/python -m unittest tests.test_base_change_proposals -v
.venv/bin/python tools/check_base_change_proposals.py --root . --base-ref ee8227d1aeae8e159ea2f9c4ba71bb0ff9e4349a
```

Expected: PASS and `Validated 25 Base change proposal(s).`

- [ ] **Step 4A: Mutation-check the recovery guard**

Temporarily remove `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` from only the `### 충돌 복원 감사` slice, run the focused test and require failure, restore the exact text, then rerun and require PASS. Do not leave the mutation in the final diff.

- [ ] **Step 5: Commit after explicit authorization**

```bash
git add -- tests/test_base_change_proposals.py '[수정제안서]/BCP-2026-024-execution-sandbox-authority-split-recovery/PROPOSAL.md'
git commit -m "docs: restore BCP collision provenance"
```

### Task 2: Publish the repository and conflict audit

**Files:**
- Create: `docs/audits/2026-08-11-base-structure-and-bcp-conflict-recovery.md`

**Interfaces:**
- Consumes: Base canonical docs, Skill Registry, local validation receipts, PR #291 through #299 history, and current external benchmarks.
- Produces: an evidence table for structure, collision lineage, restored omissions, rejected changes, and verification limits.

- [ ] **Step 1: Write the audit report**

Include exact counts, baseline SHA, validation receipts, tracked link/JSON/duplicate/size inventory, BCP-021 through BCP-025 mapping, BCP-023 hash continuity, distinct GRIMOIRE omission transitions, PR #299 evidence limit, benchmark-to-Base comparison, adversarial no-change decisions, and a measured before/after table.

- [ ] **Step 2: Check report claims against repository evidence**

Run:

```bash
rg -n "ee8227d1|BCP-2026-023|BCP-2026-024|fd9feffc|PR #29" docs/audits/2026-08-11-base-structure-and-bcp-conflict-recovery.md
git diff --check
```

Expected: every critical identity is present and the diff has no whitespace errors.

- [ ] **Step 3: Run full available validation**

Run:

```bash
.venv/bin/python tools/run_local_validation.py --trusted-history-commit ee8227d1aeae8e159ea2f9c4ba71bb0ff9e4349a
git status --short
```

Expected: all available gates pass. Record environment-only skips exactly; do not report them as executed runtime passes.

- [ ] **Step 4: Perform the final PR check**

Fresh-read open/draft PRs, `main` SHA, current branch SHA, required-check status, mergeability, unresolved review threads, and same-goal BCP collisions. Stop if any identity moved.

- [ ] **Step 5: Commit after explicit authorization**

```bash
git add -- docs/audits/2026-08-11-base-structure-and-bcp-conflict-recovery.md docs/superpowers/specs/2026-08-11-base-structure-and-bcp-conflict-recovery-design.md docs/superpowers/plans/2026-08-11-base-structure-and-bcp-conflict-recovery.md
git commit -m "docs: audit Base structure and BCP collision recovery"
```
