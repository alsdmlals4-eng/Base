# Local Bootstrap Capability Discovery Resilience Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record and enforce a Base-wide local-bootstrap rule that discovers environment-dependent tools through multiple trusted routes, validates actual capability semantically, and preserves diagnostics without weakening security/authority gates.

**Architecture:** Reuse the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` and `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` owner in `docs/GPT_CODEX_WORKFLOW_POLICY.md`. Add one focused regression to the already-routed `tests/test_one_shot_local_executor_bootstrap_contract.py`, then update the policy and existing intake Learning Log. No new Skill/Registry/runtime resolver framework is introduced.

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
- Consumes: existing `docs/GPT_CODEX_WORKFLOW_POLICY.md` bootstrap owner.
- Produces: regression method `test_bootstrap_discovers_capability_before_rejecting_one_executable_literal`.

- [ ] **Step 1: Add the failing test**

Add a method requiring the policy to contain:

```python
    def test_bootstrap_discovers_capability_before_rejecting_one_executable_literal(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        learning = (
            ROOT / "skills/managing-project-intake-and-work-contract/LEARNING_LOG.md"
        ).read_text(encoding="utf-8")

        for term in (
            "CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION",
            "DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE",
            "PATHEXT",
            "semantic readiness probe",
            "discovery는 넓게, authority와 acceptance는 좁게",
        ):
            self.assertIn(term, policy)

        self.assertIn("codex.exe", learning)
        self.assertIn("codex login status", learning)
        self.assertIn("diagnostic", learning.lower())
        self.assertIn("trusted", policy.lower())
```

- [ ] **Step 2: Observe RED in required CI**

Create/update the draft PR with only design/plan/test contract and wait for the existing local-bootstrap/Base validation to fail because the new policy tokens are absent.

Expected: existing bootstrap contracts remain green; only the new resilience requirement fails.

- [ ] **Step 3: Record exact RED head/run in PR evidence**

Do not weaken the test to match existing behavior.

---

### Task 2: Implement minimal policy contract

**Files:**
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Test: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Produces: policy identifiers `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION` and `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`.

- [ ] **Step 1: Extend the existing one-shot bootstrap section**

Add a compact rule with this exact semantic structure:

```text
CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION
required capability
→ current command resolution / PATHEXT
→ configured trusted path
→ known trusted standard install location when appropriate
→ semantic readiness probe
→ PASS or bounded BLOCKED
```

State explicitly that `.exe`/`.cmd`/`.bat` packaging differences are discovery details, not capability truth.

- [ ] **Step 2: Add strict-boundary sentence**

Include the literal:

```text
discovery는 넓게, authority와 acceptance는 좁게
```

Clarify that arbitrary disk search, untrusted same-name executables, API-key fallback and unpinned provider/image fallback remain forbidden.

- [ ] **Step 3: Add diagnostic preservation rule**

Define `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`: local bootstrap must keep a user-visible terminal failure state and/or durable bounded log; no credentials/raw private contents.

- [ ] **Step 4: Re-run focused contract**

Expected: focused bootstrap contract PASS.

---

### Task 3: Record the real problem → solution → lesson

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`

**Interfaces:**
- Consumes: approved policy semantics from Task 2.
- Produces: durable `OBSERVATION` entry for 2026-08-15.

- [ ] **Step 1: Add a new top Learning Log entry**

Record:

```text
Trigger: user-PC Loop A2 installer rejected a working Codex session because it required codex.exe; follow-up installer could close before preserving failure evidence.
Finding: packaging literal was stricter than real capability; discovery heuristics and authority/security gates were conflated; diagnostics were ephemeral.
Decision: multi-route trusted discovery → semantic readiness probe → strict acceptance; preserve terminal/log diagnostics.
Evidence: user terminal had already shown `codex login status` = `Logged in using ChatGPT`, while literal `codex.exe` detection failed.
Boundary: no arbitrary disk search, no untrusted executable selection, no API-key/paid fallback, no weakening of exact authority/security gates.
Next trigger: installers repeatedly false-block valid tools, ask for reinstall before probing actual capability, or lose blocker evidence on failure.
```

- [ ] **Step 2: Keep it an observation, not a new Skill**

Do not modify `skills/SKILL_REGISTRY.json`.

---

### Task 4: Adversarial regression, exact-head validation, merge

**Files:**
- Verify all changed files above.

**Interfaces:**
- Produces: merged Base policy/learning contract and closed Issue #415.

- [ ] **Step 1: Adversarial review**

Attack:

```text
- Does flexible discovery broaden to arbitrary untrusted executable search?
- Can path existence become false readiness?
- Are ChatGPT auth / paid API / exact SHA / protected paths weakened?
- Can logs leak credentials/private contents?
- Does this duplicate a Skill or resolver framework unnecessarily?
- Does the diff overlap open PR #414 or any other active PR?
```

Expected: all false after minimal implementation.

- [ ] **Step 2: Run exact-head required checks**

Require focused bootstrap contract plus Base v9/adversarial and Game Project Operating System/`ci-gate` when emitted.

- [ ] **Step 3: Re-read current main and active PRs before merge**

Absorb only completed `main` changes if needed; never modify active PR branches.

- [ ] **Step 4: Squash merge exact reviewed head**

Use expected-head protection where supported.

- [ ] **Step 5: Postmerge readback**

Read merged policy/learning/test and confirm postmerge checks before closing Issue #415 as completed.
