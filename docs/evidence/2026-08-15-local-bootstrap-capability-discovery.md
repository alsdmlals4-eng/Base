# Local Bootstrap Capability Discovery Resilience Evidence

## Identity

- Date: `2026-08-15`
- Tracking issue: `#415`
- PR: `#416`
- Scope: local bootstrap discovery/diagnostic policy + Learning Log + focused regression/workflow coupling.
- Product/runtime authority: unchanged. This change does not execute a REAL A2 burn-in and does not select product scope.

## User-PC incident

The Windows machine had already produced direct capability evidence:

```text
gh auth status --hostname github.com
→ Logged in to github.com account alsdmlals4-eng

codex login status
→ Logged in using ChatGPT

docker version
→ Docker client and Docker Desktop server both available
```

The reviewed Docker test image was also pulled successfully at the exact pinned digest:

```text
python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65
```

Despite that evidence, installer v1 blocked on:

```text
[BLOCKED] codex.exe was not found in PATH.
```

A later installer attempt also exposed a diagnostic-preservation problem: an intermediate batch failure could close the window before a stable blocker remained visible.

## Root cause

### 1. Packaging literal was stronger than the real capability contract

The real requirement is `ChatGPT-authenticated Codex CLI is runnable`, not `a file named codex.exe exists`.

On Windows, a command may be exposed through PATHEXT or a package-manager shim such as `.cmd` or `.bat`. Treating one suffix as authority can therefore reject a working environment.

### 2. Discovery heuristic and security authority were conflated

Environment discovery has legitimate variance; authority and security should not.

Strict invariants remain:

- repository/project identity;
- exact SHA / immutable evidence;
- trusted author/authority;
- ChatGPT authentication;
- reviewed Docker image/boundary;
- protected paths and destructive-operation prohibitions;
- paid OpenAI API and API-key fallback prohibition.

### 3. Local bootstrap diagnostics were ephemeral

A bootstrap that fails before its own `pause`/error handler can remove the best root-cause evidence. Local setup therefore needs a failure state or bounded log that survives the immediate parser/process error.

## Adopted Base rules

### `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`

```text
required capability
→ current command resolution / PATHEXT
→ explicitly configured trusted executable path when present
→ known trusted standard install location when appropriate
→ semantic readiness probe
→ READY | bounded BLOCKED
```

The final truth is the semantic probe when one exists. Path presence is not readiness.

### `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`

Local bootstrap must preserve at least one of:

- a terminal failure state that remains visible until the user closes it;
- a durable bounded diagnostic log / stable blocker code.

Prefer both. Credentials, tokens and raw private file contents remain excluded.

The governing summary is:

> **discovery는 넓게, authority와 acceptance는 좁게**

## TDD chronology

### RED 1 — missing capability-discovery principle

```yaml
head: a8ee9bcefb11baf03a5ec30393a6affc05b09267
workflow: Validate One-Shot Local Executor Bootstrap
run: 31833180090
job: 94873467584
result: EXPECTED_RED
existing_bootstrap_contracts: 3_PASS
new_capability_contract: 1_FAIL
failure: CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION absent
```

This proved the new requirement was genuinely absent while existing bootstrap behavior stayed green.

### Implementation

The new rule was placed in the narrow concrete owner `docs/LOOP_A2_LOCAL_EXECUTOR.md`, not by broadening unrelated GPT–Codex policy. The existing intake Learning Log records the real incident as an `OBSERVATION`.

### RED 2 — CI consumer coupling gap

After the rule itself became green, a second test attacked whether future owner-only changes would still invoke the focused workflow.

```yaml
head: 7655dbb8fd7f8f904233b6e1e3cb8def11a9fc6b
workflow: Validate One-Shot Local Executor Bootstrap
run: 31833487469
job: 94874445902
result: EXPECTED_RED
capability_discovery_contract: PASS
workflow_coupling_contract: FAIL
failure: docs/LOOP_A2_LOCAL_EXECUTOR.md not tracked by workflow
```

The workflow was then coupled to:

```text
docs/LOOP_A2_LOCAL_EXECUTOR.md
skills/managing-project-intake-and-work-contract/LEARNING_LOG.md
docs/superpowers/specs/*local-bootstrap-capability-discovery*.md
docs/superpowers/plans/*local-bootstrap-capability-discovery*.md
```

### Focused GREEN before latest-main reconciliation

```yaml
head: be7c191e01fed74109a8465ce2187153e28cc6ad
workflow: Validate One-Shot Local Executor Bootstrap
run: 31833705680
result: PASS
```

The final synchronized PR head is revalidated again before integration. Final exact-head run IDs remain GitHub/PR evidence rather than being recursively written into this file and changing the head again.

## Completed-main reconciliation

The branch started before multiple unrelated completed changes reached `main`.

1. Merged PR #410 advanced `main` to `06c71144c449123132adbeff99238740c99f518b`. Its Sprite/staging paths had zero overlap with PR #416 and were incorporated without force.
2. A later completed task-recovery change advanced `main` to `c0d5042e86bc74506ad21dc47e6d410914be41d4`. Its only overlapping path was `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`.
3. That Learning Log overlap was reconciled semantically: the completed task-recovery observation and this bootstrap-capability observation are both preserved. No completed-main learning was overwritten.
4. PR #414 was left read-only while in progress. After it merged, completed `main@658f7282e4de071f5225ba9d797bd15b642969ea` was incorporated without force; its story-origin paths have zero overlap with PR #416.

Open PR #417 remains read-only. Its changed paths do not overlap PR #416, and its branch was not modified.

## Adversarial review

### Attack — does flexible discovery become arbitrary executable search?

No. Discovery is limited to trusted current command resolution/PATHEXT, approved configured paths, and known trusted standard install locations. Whole-disk scanning and arbitrary same-name binaries are forbidden.

### Attack — can path existence become false readiness?

No. A semantic readiness probe is required when available. For Codex the target evidence is the authenticated CLI status rather than the executable suffix.

### Attack — does this weaken authentication/payment boundaries?

No. ChatGPT-authenticated Codex remains required. API-key fallback and separately billed OpenAI API usage remain forbidden.

### Attack — can diagnostic logs leak secrets?

The contract permits bounded blocker/status evidence only and explicitly excludes credentials, tokens, and raw private content.

### Attack — does this add a duplicate resolver framework or Skill?

No. It adds policy semantics, an observation, and regression/workflow coupling only. No new Skill ID, Registry entry, runtime resolver framework, Work Mode, A3 or Scheduler authority is added.

### Attack — does this modify in-progress work?

No. Active PR #417 is read-only and has zero changed-path overlap with PR #416. PR #414 was only incorporated after it became a completed `main` change.

## Implementation Reality Gate

Proved by this slice:

```yaml
problem_to_root_cause_record: IMPLEMENTED
capability_discovery_policy: IMPLEMENTED
semantic_readiness_rule: IMPLEMENTED
diagnostic_preservation_rule: IMPLEMENTED
learning_observation: IMPLEMENTED
tdd_red_1: OBSERVED
tdd_red_2: OBSERVED
workflow_coupling: IMPLEMENTED
focused_green_pre_reconciliation: PASS
```

Not proved by this slice:

```yaml
local_executor_installation: NOT_CONFIRMED_COMPLETE
windows_startup_registration: NOT_CONFIRMED_COMPLETE
real_local_chatgpt_codex_call: NOT_RUN_HERE
blacksmith_real_a2_burnin_runs: 0
```

The earlier user-PC evidence does prove GitHub auth, ChatGPT Codex auth, Docker engine availability and reviewed image preload at that moment; it does not by itself prove the Local Executor daemon installation/startup registration finished.

## Preserved limits

```yaml
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
automatic_product_scope_selection: FORBIDDEN
arbitrary_executable_search: FORBIDDEN
untrusted_binary_fallback: FORBIDDEN
```

## Rollback

Revert PR #416. This removes only the discovery/diagnostic policy, observation, focused CI coupling and evidence. It does not mutate project product data, user worktrees, A3, Scheduler, provider billing policy or the Loop A2 runtime implementation.
