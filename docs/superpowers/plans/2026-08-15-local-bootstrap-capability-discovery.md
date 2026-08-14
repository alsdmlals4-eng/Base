# Local Bootstrap Capability Discovery Resilience Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record and enforce a Base local-bootstrap rule that discovers environment-dependent tools through multiple trusted routes, validates actual capability semantically, and preserves diagnostics without weakening security/authority gates.

**Architecture:** Keep the broad `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` policy unchanged and put the new environment-discovery rule in its concrete Loop A2 consumer/owner, `docs/LOOP_A2_LOCAL_EXECUTOR.md`. Extend the already-existing one-shot regression and workflow so the owner plus the existing intake Learning Log stay coupled. No new Skill/Registry/runtime resolver framework is introduced.

**Tech Stack:** Markdown policy/learning contracts, Python `unittest`, GitHub Actions existing Base validation.

## Global Constraints

- Open/draft/in-progress PRs remain untouched.
- Security, authority, exact identity/SHA, ChatGPT-auth, protected-path, paid-API, A3 and Scheduler gates remain strict.
- Environment discovery may be multi-route only through trusted command resolution/configured paths/known trusted install locations.
- Semantic readiness, not path existence alone, decides capability readiness when a probe exists.
- Failure diagnostics must remain visible and/or durably logged without secrets.
- No new Skill ID or Registry entry.

---

### Task 1: Add RED bootstrap resilience contract

**Files:**
- Modify: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Consumes: existing local bootstrap contract and `docs/LOOP_A2_LOCAL_EXECUTOR.md` owner.
- Produces: regression `test_bootstrap_discovers_capability_before_rejecting_one_executable_literal`.

- [x] **Step 1: Add the failing test** requiring `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`, `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`, `PATHEXT`, semantic readiness and the strict-boundary sentence.
- [x] **Step 2: Observe RED in required CI.**

Evidence:

```yaml
head: a8ee9bcefb11baf03a5ec30393a6affc05b09267
workflow: Validate One-Shot Local Executor Bootstrap
run: 31833180090
job: 94873467584
result: EXPECTED_RED
existing_contracts: 3_PASS
new_contract: 1_FAIL
cause: CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION absent
```

- [x] **Step 3: Preserve the RED evidence rather than weakening the test.**

---

### Task 2: Implement minimal owner contract and learning record

**Files:**
- Modify: `docs/LOOP_A2_LOCAL_EXECUTOR.md`
- Modify: `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`
- Test: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Produces: `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION` and `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`.

- [x] **Step 1: Add trusted multi-route discovery.**

```text
required capability
→ current command resolution / PATHEXT
→ configured trusted path
→ known trusted standard install location when appropriate
→ semantic readiness probe
→ READY or bounded BLOCKED
```

- [x] **Step 2: Add the strict boundary:** `discovery는 넓게, authority와 acceptance는 좁게`.
- [x] **Step 3: Keep arbitrary disk search, untrusted same-name executable selection, API-key/paid fallback and unpinned Docker fallback forbidden.**
- [x] **Step 4: Add diagnostic preservation:** user-visible terminal failure state and/or durable bounded diagnostic log, without secrets.
- [x] **Step 5: Record the real 2026-08-15 problem → root cause → solution → boundary in the existing intake Learning Log.**

---

### Task 3: TDD workflow coupling

**Files:**
- Modify: `tests/test_one_shot_local_executor_bootstrap_contract.py`
- Modify: `.github/workflows/validate-one-shot-local-executor-bootstrap.yml`

**Interfaces:**
- Produces: permanent CI coupling from owner/Learning Log/design/plan to the focused bootstrap contract.

- [x] **Step 1: Add a failing workflow-coupling test** requiring:

```text
docs/LOOP_A2_LOCAL_EXECUTOR.md
skills/managing-project-intake-and-work-contract/LEARNING_LOG.md
```

- [x] **Step 2: Observe RED.**

```yaml
head: 7655dbb8fd7f8f904233b6e1e3cb8def11a9fc6b
workflow: Validate One-Shot Local Executor Bootstrap
run: 31833487469
job: 94874445902
capability_contract: PASS
workflow_coupling_contract: FAIL
cause: docs/LOOP_A2_LOCAL_EXECUTOR.md not tracked by workflow
```

- [x] **Step 3: Extend workflow paths** to the owner, Learning Log, and capability-discovery spec/plan.
- [ ] **Step 4: Require exact-final-head GREEN.**

---

### Task 4: Durable evidence and adversarial review

**Files:**
- Create: `docs/evidence/2026-08-15-local-bootstrap-capability-discovery.md`
- Verify all files above.

**Interfaces:**
- Produces: one durable problem/solution/evidence record for Issue #415 / PR #416.

- [ ] **Step 1: Record actual local evidence**: GitHub auth, `codex login status`, Docker client/server and pinned image were working while literal `codex.exe` detection falsely blocked.
- [ ] **Step 2: Record both RED cycles and final GREEN IDs.**
- [ ] **Step 3: Adversarially attack:** arbitrary executable search, path-is-readiness, auth/payment weakening, credential logging, duplicate framework, open-PR overlap.
- [ ] **Step 4: Require no validated P0/P1 finding before merge.**

---

### Task 5: Exact-head validation, current-main reconciliation, merge

**Files:**
- Verify exact final PR diff and current Base `main`.

**Interfaces:**
- Produces: merged Base policy/learning contract and completed Issue #415.

- [ ] **Step 1: Re-read current `main` and active PRs.** Absorb only completed `main` changes when required; never modify active PR branches.
- [ ] **Step 2: Confirm no changed-file overlap with active PR #414 or other active work.**
- [ ] **Step 3: Require exact-head checks:** focused bootstrap, Loop A2 Local Executor when emitted, Base v9/adversarial, Game Project Operating System/`ci-gate`, and Dependency Review when emitted.
- [ ] **Step 4: Confirm unresolved review threads = 0 and mergeability/ruleset conditions.**
- [ ] **Step 5: Update PR #416 body, mark ready, and squash merge the exact reviewed head.**
- [ ] **Step 6: Read merged `main`, verify postmerge checks, then close Issue #415 with durable evidence.**
