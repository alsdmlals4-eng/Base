# Loop A2 Authority Snapshot and Pre-Critic Test Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the ChatGPT-authenticated REAL A2 path executable against an M2 post-baseline authority bundle while requiring deterministic project-test PASS before every Critic turn.

**Architecture:** Capture the validated M2 authority bundle into an immutable in-memory snapshot separate from the detached implementation-baseline worktree. Reuse the existing `ProjectTestExecutor` through a value-based Runtime Adapter entry point, run it after every Builder scope PASS, bind its canonical PASS receipt to the same run identity, and expose that bounded receipt to the independent Critic through review material.

**Tech Stack:** Python 3.12 standard library, existing Loop M2 contracts, Loop A2 runtime/worktree ownership, ProjectTestExecutor, Docker denied-network boundary injection, Codex CLI transport, unittest, GitHub Actions.

## Global Constraints

- Separately billed OpenAI API calls remain forbidden.
- `source_main_sha` / `expected_main_sha` remain the approved implementation baseline; do not redefine them as an authority-file commit.
- Authority files are never copied into the detached product worktree.
- REAL Critic execution is forbidden until deterministic project tests PASS.
- FAKE runtime behavior remains backward compatible.
- A3 auto-merge remains `DISABLED`; Scheduler remains `NOT_CONFIGURED`; automatic product-package selection remains forbidden.
- CI must not make a live ChatGPT/Codex model call.
- Do not modify open/draft PR #369 or any unrelated open PR.

---

### Task 1: Capture immutable authority independently from implementation baseline

**Files:**
- Create: `tools/loop_a2_runtime/authority_snapshot.py`
- Create: `tests/test_loop_a2_authority_snapshot.py`
- Modify: `tools/loop_a2_runtime/__init__.py`

**Interfaces:**
- Produces: `AuthorityFile(path: str, content: str)`.
- Produces: `AuthoritySnapshot(project_id, package_id, source_main_sha, capsule_path, runtime_adapter_path, files, snapshot_sha256)`.
- Produces: `capture_authority_snapshot(*, project_root: Path, capsule_relative: str, request: RunRequest) -> AuthoritySnapshot`.
- Produces: `AuthoritySnapshot.text(relative: str) -> str` and `AuthoritySnapshot.parsed_object(relative: str) -> dict[str, object]`.

- [ ] **Step 1: Write the post-baseline authority RED fixture**

Create a temporary Git repository with a baseline commit containing `scripts/feature/a.gd` and tests. Record the baseline SHA. In the working tree after that commit, create a complete valid M2 Capsule bundle whose source fields point to the baseline SHA. Build the `RunRequest` from those current authority files.

Assert:

```python
snapshot = capture_authority_snapshot(
    project_root=repo,
    capsule_relative="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
    request=request,
)
self.assertEqual(snapshot.source_main_sha, baseline_sha)
self.assertIn(request.capsule_path, snapshot.paths)
self.assertEqual(snapshot.package_id, request.package_id)
```

Also assert capture rejects request/package/SHA mismatch, symlink authority, NUL/binary content, unsafe paths, and a bundle that changes between request and capture.

- [ ] **Step 2: Run the authority test and confirm RED**

Run:

```bash
python -m unittest tests.test_loop_a2_authority_snapshot -v
```

Expected: FAIL because `authority_snapshot` does not exist.

- [ ] **Step 3: Implement the minimum immutable snapshot**

Implementation requirements:

```python
@dataclass(frozen=True)
class AuthorityFile:
    path: str
    content: str

@dataclass(frozen=True)
class AuthoritySnapshot:
    project_id: str
    package_id: str
    source_main_sha: str
    capsule_path: str
    runtime_adapter_path: str
    files: tuple[AuthorityFile, ...]
    snapshot_sha256: str
```

Use `validate_bundle()` first, normalize all paths with the existing A2 path contract, reject symlinks, decode UTF-8 only, and compute SHA-256 over canonical JSON containing normalized paths plus exact text. Verify the snapshot's Package fields exactly equal the supplied `RunRequest` authority fields.

- [ ] **Step 4: Re-run the authority test and confirm GREEN**

Run the Step 2 command. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/loop_a2_runtime/authority_snapshot.py tools/loop_a2_runtime/__init__.py tests/test_loop_a2_authority_snapshot.py
git commit -m "feat: snapshot A2 authority outside baseline worktree"
```

### Task 2: Make Builder consume authority snapshot and baseline implementation context separately

**Files:**
- Modify: `tools/loop_a2_runtime/openai_transport.py`
- Modify: `tools/loop_a2_runtime/codex_cli_transport.py`
- Create: `tests/test_loop_a2_authority_context.py`
- Modify: `tests/test_loop_a2_codex_cli_transport.py`
- Modify: `tests/test_loop_a2_openai_transport.py`

**Interfaces:**
- Consumes: `AuthoritySnapshot` from Task 1.
- `OpenAIWorkspaceBuilder(..., authority_snapshot: AuthoritySnapshot | None = None)`.
- `build_subscription_provider_components(..., authority_snapshot: AuthoritySnapshot, ...)` requires the snapshot on the active subscription path.

- [ ] **Step 1: Write the detached-baseline RED**

Using the Task 1 Git fixture, create a detached worktree at the baseline SHA and prove the Capsule is absent there. Construct `OpenAIWorkspaceBuilder` with an `AuthoritySnapshot` and a fake structured client. Assert the Builder can collect authority and propose an allowed implementation write without copying any `docs/operations/loop/**` file into the detached worktree.

Also assert a proposed write to a snapshot authority path returns `BUILDER_AUTHORITY_WRITE_FORBIDDEN` even when that path is absent from the baseline worktree.

- [ ] **Step 2: Run focused context tests and confirm RED**

```bash
python -m unittest tests.test_loop_a2_authority_context tests.test_loop_a2_codex_cli_transport tests.test_loop_a2_openai_transport -v
```

Expected: new authority-context tests FAIL because Builder still reads authority from `worktree_path`.

- [ ] **Step 3: Split trusted authority context from implementation context**

Change the context collector so snapshot authority text is loaded from `AuthoritySnapshot`, while tracked allowed implementation context remains loaded from the detached worktree. Use snapshot authority paths for the immutable-write denylist. Keep snapshot-less behavior only for existing historical direct-transport test compatibility.

- [ ] **Step 4: Require snapshot in subscription provider factory**

Update `build_subscription_provider_components` to require `authority_snapshot` and pass it to `OpenAIWorkspaceBuilder`. Do not alter the Codex process sandbox/tool restrictions.

- [ ] **Step 5: Re-run focused context tests and confirm GREEN**

Run Step 2 command. Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tools/loop_a2_runtime/openai_transport.py tools/loop_a2_runtime/codex_cli_transport.py tests/test_loop_a2_authority_context.py tests/test_loop_a2_codex_cli_transport.py tests/test_loop_a2_openai_transport.py
git commit -m "fix: separate A2 authority from execution worktree"
```

### Task 3: Add value-based ProjectTestExecutor entry point and candidate verifier

**Files:**
- Modify: `tools/loop_a2_runtime/test_executor.py`
- Create: `tools/loop_a2_runtime/candidate_verification.py`
- Modify: `tools/loop_a2_runtime/__init__.py`
- Modify: `tests/test_loop_a2_project_test_executor.py`
- Create: `tests/test_loop_a2_candidate_verification.py`

**Interfaces:**
- Produces: `ProjectTestExecutor.run_all_from_value(*, adapter_value: Mapping[str, object], worktree_path: Path, expected_project_id: str, expected_main_sha: str) -> TestSuiteResult`.
- Produces: `VerificationEvidenceMailbox.publish(...)`, `.require_pass(...)`.
- Produces: `ProjectTestCandidateVerifier.verify(request: RunRequest, worker_result: WorkerResult) -> TestSuiteResult`.

- [ ] **Step 1: Write value-entry RED**

Require `run_all_from_value()` to produce the same canonical result as file-based `run_all()` for an identical adapter object. Existing `run_all()` must remain a compatibility wrapper.

- [ ] **Step 2: Write candidate-verifier RED**

Create an owned external worktree fixture. Put the Runtime Adapter only in `AuthoritySnapshot`, not the baseline worktree. Assert:

```python
result = verifier.verify(request, worker_result)
self.assertEqual(result.status, "PASS")
self.assertEqual(mailbox.require_pass(request)["status"], "PASS")
```

Require ownership mismatch, adapter identity mismatch, test FAIL/BLOCKED, and stale run identity to fail closed without publishing a PASS receipt.

- [ ] **Step 3: Run focused verification tests and confirm RED**

```bash
python -m unittest tests.test_loop_a2_project_test_executor tests.test_loop_a2_candidate_verification -v
```

Expected: FAIL because the value entry point/verifier do not exist.

- [ ] **Step 4: Refactor ProjectTestExecutor without changing semantics**

Move adapter-object validation/execution into `run_all_from_value()`. Keep `run_all()` responsible only for safe JSON file loading before delegating. Preserve disposable verification worktree, mutation detection, digest-only output, timeout, and NetworkBoundary behavior exactly.

- [ ] **Step 5: Implement ownership-bound verifier and mailbox**

The verifier must verify `WorkspaceOwnershipRegistry` for project/run/SHA before tests, parse Runtime Adapter text from the immutable snapshot, execute the existing ProjectTestExecutor, and publish only canonical PASS evidence under `(project_id, run_id, package_id, expected_main_sha)`.

- [ ] **Step 6: Re-run focused verification tests and confirm GREEN**

Run Step 3 command. Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/loop_a2_runtime/test_executor.py tools/loop_a2_runtime/candidate_verification.py tools/loop_a2_runtime/__init__.py tests/test_loop_a2_project_test_executor.py tests/test_loop_a2_candidate_verification.py
git commit -m "feat: verify A2 candidates before Critic"
```

### Task 4: Enforce REAL pre-Critic verification and bind PASS evidence into Critic material

**Files:**
- Modify: `tools/loop_a2_runtime/runner.py`
- Modify: `tools/loop_a2_runtime/providers.py`
- Modify: `tools/loop_a2_runtime/openai_transport.py`
- Modify: `tools/loop_a2_runtime/codex_cli_transport.py`
- Create: `tests/test_loop_a2_real_verification_gate.py`
- Modify: `tests/test_loop_a2_adversarial.py`
- Modify: `tests/test_loop_a2_codex_cli_transport.py`

**Interfaces:**
- `A2Runtime(..., candidate_verifier: CandidateVerifier | None = None, provider_mode: str = "FAKE")`.
- `ReviewMaterial(..., test_evidence: dict[str, object] | None = None)`.
- `GitReviewMaterialSource(..., verification_mailbox: VerificationEvidenceMailbox | None = None)`.

- [ ] **Step 1: Write REAL gate RED**

Require:

```python
runtime = A2Runtime(builder=builder, critic=critic, provider_mode="REAL")
outcome = runtime.run(request, observed_main_sha=request.expected_main_sha)
self.assertEqual(outcome.state, "BLOCKED_UNVERIFIED")
self.assertIn("PROJECT_TEST_GATE_REQUIRED", outcome.finding_codes)
self.assertEqual(builder.calls, 0)
self.assertEqual(critic.calls, 0)
```

The missing verifier must block before Builder to avoid consuming subscription usage when deterministic verification cannot later run.

With a verifier present, require Builder PASS → scope PASS → verifier PASS → Critic. Test FAIL/BLOCKED must produce zero Critic calls. A repair Builder must trigger a fresh verifier call before the next Critic call.

- [ ] **Step 2: Write Critic-evidence RED**

Require `GitReviewMaterialSource` to attach only the matching mailbox PASS receipt. Cross-run/stale entries must raise a bounded transport error. Assert raw stdout/stderr keys are absent from the Critic payload and only digest/byte-count canonical test evidence is present.

- [ ] **Step 3: Run REAL gate tests and confirm RED**

```bash
python -m unittest tests.test_loop_a2_real_verification_gate tests.test_loop_a2_codex_cli_transport tests.test_loop_a2_adversarial -v
```

Expected: new tests FAIL because REAL runtime has no verifier gate/test evidence binding.

- [ ] **Step 4: Implement pre-Builder REAL verifier requirement and per-candidate verification**

At the beginning of REAL `run()`, block if `candidate_verifier is None`. After each Builder deterministic scope PASS, call verifier. Map test `FAIL`/`BLOCKED` to `BLOCKED_UNVERIFIED` with bounded evidence and never invoke Critic. Keep FAKE paths unchanged.

- [ ] **Step 5: Bind mailbox evidence into Critic review material**

Add optional `test_evidence` to `ReviewMaterial`. On the subscription path, `GitReviewMaterialSource` requires the matching PASS receipt before material collection succeeds. `OpenAIWorktreeCritic` includes that receipt in the JSON payload.

- [ ] **Step 6: Re-run REAL gate tests and confirm GREEN**

Run Step 3 command. Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/loop_a2_runtime/runner.py tools/loop_a2_runtime/providers.py tools/loop_a2_runtime/openai_transport.py tools/loop_a2_runtime/codex_cli_transport.py tests/test_loop_a2_real_verification_gate.py tests/test_loop_a2_adversarial.py tests/test_loop_a2_codex_cli_transport.py
git commit -m "fix: require project tests before REAL A2 Critic"
```

### Task 5: Wire authority capture and verifier through the REAL CLI

**Files:**
- Modify: `tools/loop_a2.py`
- Modify: `tests/test_loop_a2_subscription_cli_entrypoint.py`
- Create: `docs/evidence/2026-08-15-loop-a2-authority-test-gate.md`

**Interfaces:**
- Consumes: `capture_authority_snapshot`, subscription provider components containing `candidate_verifier`.
- REAL CLI order: build request → capture snapshot → provider auth → components → REAL runtime.

- [ ] **Step 1: Write CLI wiring RED**

Patch deterministic boundaries and assert the subscription factory receives the exact captured snapshot and the REAL runtime receives `candidate_verifier=components.candidate_verifier`. Require authority capture failure to stop before Codex auth/factory execution.

- [ ] **Step 2: Run CLI test and confirm RED**

```bash
python -m unittest tests.test_loop_a2_subscription_cli_entrypoint -v
```

Expected: FAIL because current CLI has no snapshot/verifier wiring.

- [ ] **Step 3: Implement minimal REAL CLI wiring**

Capture the snapshot immediately after the validated request. Pass it to `build_subscription_provider_components`. Construct REAL `A2Runtime` with the component verifier. Do not add paid API fallback, package selection, A3, or Scheduler behavior.

The subscription factory's network boundary remains explicitly injectable. If no enforceable project-test boundary is configured, the REAL path must fail closed before Critic and may not claim smoke PASS.

- [ ] **Step 4: Re-run CLI and full focused regressions**

```bash
python -m unittest \
  tests.test_loop_a2_authority_snapshot \
  tests.test_loop_a2_authority_context \
  tests.test_loop_a2_candidate_verification \
  tests.test_loop_a2_real_verification_gate \
  tests.test_loop_a2_subscription_cli_entrypoint \
  tests.test_loop_a2_codex_cli_transport \
  tests.test_loop_a2_openai_transport \
  tests.test_loop_a2_openai_transport_adversarial \
  tests.test_loop_a2_runtime_worktree \
  tests.test_loop_a2_project_test_executor \
  tests.test_loop_a2_adversarial -v
```

Expected: PASS with no live model call.

- [ ] **Step 5: Write exact evidence**

Record root cause, TDD RED heads/run IDs, GREEN heads/run IDs, changed files, claim ceiling, and the fact that local ChatGPT subscription smoke remains `NOT_RUN`.

- [ ] **Step 6: Commit**

```bash
git add tools/loop_a2.py tests/test_loop_a2_subscription_cli_entrypoint.py docs/evidence/2026-08-15-loop-a2-authority-test-gate.md
git commit -m "fix: wire executable REAL A2 verification path"
```

### Task 6: Exact-head adversarial verification, merge, and postmerge closure

**Files:**
- No product files.
- Modify evidence only if exact observed run IDs/head SHA require finalization.

- [ ] **Step 1: Adversarial attack**

Attack authority/request mismatch, symlink/path escape, snapshot mutation, authority-path writes absent from baseline, missing/stale/cross-run PASS receipt, test FAIL/BLOCKED bypass, repair-cycle bypass, Critic-before-test ordering, secret leakage, paid fallback, A3/Scheduler activation, and open-PR overlap.

- [ ] **Step 2: Run repository-required exact-head gates**

Require on one exact PR head:

- Validate Loop A2 Runtime Foundation PASS;
- Validate Loop A2 OpenAI Transport PASS;
- Validate Base v9 Operating Contracts + adversarial gate PASS;
- Validate Game Project Operating System final `ci-gate` PASS;
- Dependency Review PASS when triggered;
- unresolved review threads `0`.

- [ ] **Step 3: Merge with expected-head protection**

Squash merge only the M4.10 branch after all exact-head evidence is green. Do not modify or merge #369 or any unrelated open PR.

- [ ] **Step 4: Postmerge readback**

Read Base `main` for authority snapshot, verifier, REAL runner gate, CLI wiring, and evidence. Require postmerge Base-v9/adversarial and Game Project OS success before completion claim.

- [ ] **Step 5: Close #390**

Close issue #390 as completed with exact head, merge SHA, postmerge run IDs, and claim ceiling. The next independent task is Blacksmith test-only burn-in packaging / local executor portability, not product-package selection.