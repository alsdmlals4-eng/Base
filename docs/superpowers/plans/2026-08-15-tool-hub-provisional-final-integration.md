# Tool Hub Provisional Final Integration Implementation Plan

> **Execution note:** use test-driven development, systematic debugging, adversarial review, and verification-before-completion. Owner PR branches remain read-only throughout.

**Goal:** Reconcile the strongest verified parts of Character Studio (#373), Windows child ownership (#386), and local-to-Figma delivery (#376) onto current subscription-only `main`, so the final Tool Hub golden path can be validated before those stale owner PRs finish.

**Architecture:** Work only on this isolated latest-main branch under the merged `PROVISIONAL_INTEGRATION` contract. Treat #373/#376/#386 as read-only upstream owner snapshots. Absorb behavior contract-by-contract, preserving current main security/cost/platform truth. Re-read owner heads and main at every checkpoint; if either moves, semantically reconcile immediately and rerun exact-head tests. This PR must remain unmerged while any owner overlap is unresolved unless that owner is merged+absorbed, explicitly handed off/superseded, or explicitly replaced by user authorization.

**Canonical constraints:** `NO_ADDITIONAL_PAYMENT`, ChatGPT Pro subscription handoff, `subscription_handoff_import`, `CHATGPT_INCLUDED`, `provider_call_made=false`, `requires_additional_payment=false`, Windows no-PowerShell normal flow, portable trusted-file/Asset Vault boundaries, project isolation, exact Figma routing/fail-closed missing routes, no Local Executor changes from #420.

## PROVISIONAL_INTEGRATION checkpoint

```yaml
current_task_or_pr_identity: Issue #427 / provisional integration PR
source_main_sha: 8df92b0832955a64e406d0386135ff1d28f9f91a
current_main_sha: 8df92b0832955a64e406d0386135ff1d28f9f91a
write_parent_sha: 8df92b0832955a64e406d0386135ff1d28f9f91a
expected_head_sha: PENDING_FIRST_WRITE
provisional_integration_authorized: true
owner_pr_head_shas:
  "373": 9b872c9de03e31e514c53b86abdbe1100c83545b
  "376": d476f3756b45820562495d31f9f975b212b25724
  "386": f8e94b63354908364bafa0a1f68a5eb27598ed86
provisional_semantic_resources:
  - character-expression-request-and-identity-edit
  - tool-hub-reviewed-launch-and-windows-process-tree
  - asset-vault-to-figma-delivery-and-receipt
coordination_action: owner branches read-only; integrate only here; reconcile on owner/main movement
```

---

### Task 1: Character / Outfit / Scene on subscription-only main

**Owner snapshot:** PR #373 @ `9b872c9de03e31e514c53b86abdbe1100c83545b`

**Target behavior:**
- Keep internal `expression-studio` compatibility identity, but expose Character Studio display/capabilities.
- Add `edit_mode = expression | outfit | scene` and bounded `edit_prompt` validation.
- Expression mode retains existing controls; outfit/scene require prompt and prohibit expression-control mixing.
- Generate identity-preserving outfit/scene instructions from the approved anchor.
- Preserve current `subscription_handoff_import` / `CHATGPT_INCLUDED` import path; do not make OpenAI API generation canonical.
- Preserve current portable Expression anchor reader and Asset Vault implementation from merged #417/#410.

**TDD:**
1. Port only #373 Character contract tests needed to express the above behavior onto current main.
2. Run focused tests and record RED against expression-only current main.
3. Implement minimal model/catalog/engine/web/registry changes.
4. Re-run Character tests plus existing subscription provenance and Visual Studio portability tests on Ubuntu/Windows.
5. Adversarially verify no paid-provider canonical route, no identity-scope leakage, and no regression to expression import/curation/export.

### Task 2: Windows Tool Hub child ownership on portable current main

**Owner snapshot:** PR #386 @ `f8e94b63354908364bafa0a1f68a5eb27598ed86`

**Target behavior:**
- Reuse #386 suspended-process Job Object design with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`.
- Preserve current main reviewed source/runtime trust and adapt Tool Hub launch path verification for Windows without weakening POSIX descriptor-backed guarantees.
- Remove stale `BLOCKED_PLATFORM` expectation only where actual Windows process-tree ownership is verified.
- Start a real reviewed Studio child + descendant on Windows and prove both terminate on supervisor stop.
- Verify two project-scoped child launches do not cross-wire startup/runtime identity.

**TDD:**
1. Port #386 process-owner tests and current-main portability expectations first; observe RED.
2. Reconcile `environment.py`, `registry.py`, `runtime_trust.py`, `supervisor.py`, and `windows_process_owner.py` with current main.
3. Add/adjust portable reviewed-path helpers rather than duplicating security logic.
4. Run Windows-focused child/process-tree tests and Linux supervisor regressions.
5. Run Tool Hub multi-studio smoke and current subscription/import gates.

### Task 3: Asset Vault → exact Figma delivery boundary

**Owner snapshot:** PR #376 @ `d476f3756b45820562495d31f9f975b212b25724`

**Target behavior:**
- Reuse #376 delivery core, hardening, concurrency, HTTP authority, and plugin contract where compatible.
- Source only accepted/exported Asset Vault bytes and SHA-256 evidence.
- Resolve project/tool target through canonical registries; do not accept arbitrary Figma node IDs from normal UI/API.
- Character/Expression routes may use the eight reviewed exact routes already in main.
- Sprite Action / Effect dedicated route remains fail-closed if absent; do not invent node IDs.
- Delivery receipt/readback must bind project, tool, run, route, byte SHA, and provider-free truth.

**TDD:**
1. Port delivery-core/hardening/concurrency/plugin tests onto current main and observe RED for missing integration.
2. Reconcile `tool_hub.figma_delivery`, Tool Hub API/web surface, and plugin bundle.
3. Bind delivery requests to current Asset Vault/export and canonical Figma route registry.
4. Run Linux/Windows static/HTTP tests.
5. Perform live Figma mutation/readback only if the current Figma connector exposes and permits the exact operation; otherwise record `NOT_RUN` and do not overclaim.

### Task 4: Golden-path integration contract

Validate the actual composed path without adding a second orchestration framework:

```text
Tool Hub project/tool selection
→ approved anchor
→ bounded ChatGPT Pro handoff prompt
→ user-generated PNG import (`CHATGPT_INCLUDED`)
→ candidate validation/curation/export
→ project Asset Vault exact bytes/SHA
→ canonical project/tool Figma route
→ delivery receipt/readback when available
→ downstream game/Godot consumption when actually executed
```

Required assertions:
- no OpenAI API key/provider call in canonical path;
- no shell/PowerShell requirement in normal Windows flow;
- no arbitrary local path or Figma node authority in user-facing request;
- project/run identity cannot cross-wire between simultaneous projects;
- missing target route fails closed;
- exact-head evidence distinguishes fixture PNG transport from real AI visual quality.

### Task 5: Reconciliation checkpoints

Before every persistent write cluster, PR-ready transition, and final review:
1. Re-read current `main`.
2. Re-read #373/#376/#386 state + exact head.
3. If an owner/main moved, classify affected paths/semantic resources.
4. Merge/rebase current main into this integration branch without force-pushing owner branches.
5. Compare owner implementation vs provisional implementation semantically.
6. Keep the stronger/current canonical behavior; delete weaker duplicate code/tests/workflows.
7. Rerun affected focused tests and then exact-head repository gates.

### Task 6: Merge boundary

Even if all implementation and CI gates are green, this PR remains **DO_NOT_MERGE_PROVISIONAL** while #373/#376/#386 are unresolved. Merge becomes eligible only when every overlapping owner is one of:
- merged and absorbed into latest main,
- explicitly handed off/superseded,
- explicitly approved by the user for replacement by this integration PR.

At merge eligibility, re-read latest main/owners, reconcile one final time, remove redundant temporary workflows, run exact-head Base v9 + Game Project OS + relevant Ubuntu/Windows Tool Hub gates, verify unresolved review threads = 0, then squash merge and perform post-merge readback.
