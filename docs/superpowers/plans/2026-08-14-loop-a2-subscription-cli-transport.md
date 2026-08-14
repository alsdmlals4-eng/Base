# Loop A2 Subscription-Native Codex CLI Transport Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the paid OpenAI API decision gate with a fail-closed ChatGPT-authenticated Codex CLI transport for Loop A2 Builder/Critic automation.

**Architecture:** Keep `provider_mode=REAL`, but route the active real provider through isolated `codex exec --ephemeral` processes authenticated by the user's ChatGPT plan. The CLI process only returns structured JSON; existing deterministic Base code validates and applies Builder writes and independently attests Critic review material. Direct API-key transport remains present but permanently policy-closed.

**Tech Stack:** Python 3 standard library, existing Loop A2 protocol/worktree modules, official Codex CLI, unittest, GitHub Actions.

## Global Constraints

- Separately billed OpenAI API calls are forbidden.
- No `OPENAI_API_KEY` fallback.
- ChatGPT-authenticated Codex CLI is the primary real provider.
- Builder and Critic use separate ephemeral process/context boundaries.
- Codex receives no direct authority over the project worktree.
- Existing scope, worktree ownership, deterministic test, denied-network, A3-disabled, Scheduler-not-configured, and automatic-product-scope-forbidden constraints remain unchanged.
- No real subscription smoke may be claimed without actual local ChatGPT-authenticated Codex execution evidence.

---

### Task 1: Policy and subscription provider gate

**Files:**
- Modify: `tools/loop_a2_runtime/provider_gate.py`
- Modify: `tests/test_loop_a2_adversarial.py`
- Test: `tests/test_loop_a2_subscription_gate.py`

**Interfaces:**
- Produces: `paid_openai_api_gate() -> dict[str, Any]`
- Produces: `subscription_codex_cli_gate(*, run_command: Callable[..., CompletedProcess[str]] | None = None) -> dict[str, Any]`
- Compatibility: `real_provider_gate()` remains as the direct paid-provider gate alias and must fail closed under current policy.

- [ ] **Step 1: Write failing gate tests**

Test cases:

```python
self.assertEqual(real_provider_gate()["code"], "PAID_OPENAI_API_FORBIDDEN")
self.assertEqual(subscription_codex_cli_gate(fake_chatgpt)["status"], "READY")
self.assertEqual(subscription_codex_cli_gate(fake_api_key)["code"], "CODEX_CHATGPT_AUTH_REQUIRED")
self.assertEqual(subscription_codex_cli_gate(fake_missing)["code"], "CODEX_CLI_UNAVAILABLE")
```

- [ ] **Step 2: Run the focused tests and confirm RED**

Run:

```bash
python -m unittest tests.test_loop_a2_subscription_gate tests.test_loop_a2_adversarial -v
```

Expected: FAIL because the subscription gate and forbidden paid-policy code do not exist yet.

- [ ] **Step 3: Implement the minimal gates**

Implementation rules:

```python
PAID_POLICY_CODE = "PAID_OPENAI_API_FORBIDDEN"
CHATGPT_READY_LINE = "Logged in using ChatGPT"
```

`subscription_codex_cli_gate` must call `codex login status` without shell expansion, bound the timeout, accept only the exact ChatGPT state, and never inspect or require `OPENAI_API_KEY`.

- [ ] **Step 4: Re-run focused tests and confirm GREEN**

Run the same unittest command. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/loop_a2_runtime/provider_gate.py tests/test_loop_a2_subscription_gate.py tests/test_loop_a2_adversarial.py
git commit -m "feat: gate Loop A2 on ChatGPT Codex auth"
```

### Task 2: Isolated Codex CLI structured transport

**Files:**
- Create: `tools/loop_a2_runtime/codex_cli_transport.py`
- Create: `tests/test_loop_a2_codex_cli_transport.py`
- Modify: `tools/loop_a2_runtime/__init__.py`

**Interfaces:**
- Produces: `CodexCliProcess` bounded subprocess adapter.
- Produces: `CodexCliWorkspaceBuilder` implementing the existing WorkspaceWorker signature.
- Produces: `CodexCliWorktreeCritic` implementing `CriticProvider`.
- Produces: `build_subscription_provider_components(repo_root, runtime_root, ...)`.
- Reuses: `_BUILDER_SCHEMA`, `_CRITIC_SCHEMA`, `RepairMailbox`, `GitReviewMaterialSource`, existing write-plan/path validation concepts from `openai_transport.py` without making a paid SDK call.

- [ ] **Step 1: Write failing process-boundary tests**

Assert the generated argv contains:

```text
codex exec
--ephemeral
--ignore-user-config
--skip-git-repo-check
--sandbox read-only
--output-schema <temp-schema>
--output-last-message <temp-output>
-
```

Also assert:

```python
self.assertNotIn("OPENAI_API_KEY", child_env)
self.assertFalse(any("sk-" in value for value in child_env.values()))
```

- [ ] **Step 2: Write failing Builder/Critic protocol tests**

Use a fake process runner that writes schema-valid JSON to the final-message file. Verify Builder produces a bounded write plan and Critic runs through a second independent invocation. Add malformed JSON, non-zero exit, timeout, oversized output, unsafe path, and API-key echo cases.

- [ ] **Step 3: Run focused transport tests and confirm RED**

```bash
python -m unittest tests.test_loop_a2_codex_cli_transport -v
```

Expected: FAIL because the module does not exist.

- [ ] **Step 4: Implement `CodexCliProcess`**

Use `subprocess.run([...], shell=False)` semantics, an empty temporary working directory, text stdin, bounded timeout, and a safe inherited environment. Strip all keys matching `OPENAI_API_KEY`, `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID`, and `OPENAI_BASE_URL`. Do not copy project files into the temporary model directory.

- [ ] **Step 5: Implement structured Builder/Critic adapters**

Builder flow:

```text
collect bounded approved context
→ codex exec in isolated read-only temp cwd
→ parse schema-valid write plan
→ deterministic validate_changed_paths/authority checks
→ host applies writes to owned worktree
→ attest actual Git changed paths
```

Critic flow:

```text
collect owned actual diff
→ codex exec in separate isolated read-only temp cwd
→ parse ReviewResult fields
→ existing A2Runtime validates requirement/path expansion
```

- [ ] **Step 6: Run focused tests and confirm GREEN**

Run the same unittest command. Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add tools/loop_a2_runtime/codex_cli_transport.py tools/loop_a2_runtime/__init__.py tests/test_loop_a2_codex_cli_transport.py
git commit -m "feat: add subscription-native Codex CLI transport"
```

### Task 3: Wire the REAL CLI entry point

**Files:**
- Modify: `tools/loop_a2.py`
- Create: `tests/test_loop_a2_subscription_cli_entrypoint.py`

**Interfaces:**
- Consumes: `subscription_codex_cli_gate` and `build_subscription_provider_components`.
- Produces: `loop_a2.py run --provider real --runtime-root <path>` real subscription execution path.

- [ ] **Step 1: Write failing CLI tests**

Verify:

```text
--provider real + API-key-only auth -> CONTRACT/PROVIDER gate failure
--provider real + ChatGPT auth fake -> constructs subscription components
```

The test must patch the subprocess boundary; CI must not contact OpenAI.

- [ ] **Step 2: Run and confirm RED**

```bash
python -m unittest tests.test_loop_a2_subscription_cli_entrypoint -v
```

- [ ] **Step 3: Implement entrypoint wiring**

Add explicit `--runtime-root` for real runs. Build `A2Runtime(builder=..., critic=..., provider_mode="REAL")`, execute against the observed SHA, print canonical evidence, and preserve non-zero exit for non-integration-eligible outcomes.

- [ ] **Step 4: Run and confirm GREEN**

Run the focused CLI test plus existing A2 runtime tests.

- [ ] **Step 5: Commit**

```bash
git add tools/loop_a2.py tests/test_loop_a2_subscription_cli_entrypoint.py
git commit -m "feat: route Loop A2 real mode through Codex CLI"
```

### Task 4: Evidence and checkpoint policy migration

**Files:**
- Modify: `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`
- Create: `docs/evidence/2026-08-14-loop-a2-subscription-cli-transport.md`
- Create: `tests/test_universal_loop_subscription_cli_closure.py`
- Modify: `tests/test_ci_required_gate_evaluator.py`

**Interfaces:**
- Produces machine-readable policy state that paid API is forbidden and no longer a user-decision gate.

- [ ] **Step 1: Write closure test first**

The test must require:

```python
checkpoint["provider_policy"]["paid_openai_api"] == "FORBIDDEN"
checkpoint["remaining_external_gate"]["real_openai_api"] == "NOT_APPLICABLE_POLICY_FORBIDDEN"
checkpoint["remaining_external_gate"]["paid_smoke_issue"] is None
checkpoint["remaining_external_gate"]["real_a2_burnin_runs"] == 0
checkpoint["preserved_limits"]["a3_auto_merge"] == "DISABLED"
checkpoint["preserved_limits"]["scheduler"] == "NOT_CONFIGURED"
```

- [ ] **Step 2: Run the required docs gate and confirm RED**

```bash
python -m unittest tests.test_ci_required_gate_evaluator -v
```

Expected: FAIL only on the newly required subscription-policy fields.

- [ ] **Step 3: Update checkpoint and evidence**

Set the top-level status to a subscription-transport-ready state only after exact-head tests pass. Record that real subscription smoke is `NOT_RUN_LOCAL_AUTH_REQUIRED`; do not mark a real model call PASS.

- [ ] **Step 4: Run docs gate and confirm GREEN**

Run required docs tests and JSON parse validation.

- [ ] **Step 5: Commit**

```bash
git add docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json docs/evidence/2026-08-14-loop-a2-subscription-cli-transport.md tests/test_universal_loop_subscription_cli_closure.py tests/test_ci_required_gate_evaluator.py
git commit -m "docs: close paid API gate for Loop A2"
```

### Task 5: Exact-head adversarial verification and merge

**Files:**
- No new product files unless a validated critique requires a minimal in-scope fix.

- [ ] **Step 1: Run focused regression suite**

```bash
python -m unittest \
  tests.test_loop_a2_subscription_gate \
  tests.test_loop_a2_codex_cli_transport \
  tests.test_loop_a2_subscription_cli_entrypoint \
  tests.test_loop_a2_adversarial \
  tests.test_loop_a2_openai_transport \
  tests.test_loop_a2_openai_transport_adversarial \
  tests.test_loop_a2_runtime_worktree \
  tests.test_loop_a2_project_test_executor \
  tests.test_ci_required_gate_evaluator -v
```

- [ ] **Step 2: Run repository-required exact-head GitHub gates**

Require Base-v9/adversarial and Game Project Operating System success on the exact PR head. Any unrelated transient failure may be rerun only on the same SHA and must be reported.

- [ ] **Step 3: Adversarial review**

Attack:

```text
API-key fallback leakage
child env secret leakage
user/project config authority injection
shell injection
worktree mutation by model process
Critic shared-state leakage
scope/authority bypass
false real-smoke claim
A3/Scheduler accidental activation
```

Apply only validated in-scope fixes, then re-run regressions.

- [ ] **Step 4: Merge with exact-head protection**

Squash merge only after unresolved review threads are zero and required exact-head checks pass.

- [ ] **Step 5: Postmerge readback**

Read `main`, confirm the checkpoint/policy/transport files are retained, and require postmerge Base-v9 and Game Project OS success before final completion claim.

- [ ] **Step 6: Close policy issues**

Close the former paid-smoke decision issue as `not_planned` with the user-approved no-paid-API policy recorded. Close the new implementation issue as completed after postmerge evidence is durable.
