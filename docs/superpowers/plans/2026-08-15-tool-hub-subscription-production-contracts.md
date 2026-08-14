# Tool Hub Subscription-Only Production Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add shared, testable contracts for a no-additional-payment ChatGPT Pro handoff path and exact tool-specific Figma destinations without touching open Tool Hub product PRs.

**Architecture:** Keep `PROJECT_FIGMA_TARGET_REGISTRY.json` as the project/file/parent authority, add a separate tool-route registry for reviewed descendant nodes, and add a network-free `subscription_handoff` contract for GPT Pro handoff packets. Both loaders live in `base_tool_contracts`, fail closed, and prove canonical committed bytes before production use.

**Tech Stack:** Python 3.12, Pydantic 2, Base trusted-file helpers, JSON registries, unittest/pytest-compatible tests, GitHub Actions existing Game Project Operating System workflow.

## Global Constraints

- `NO_ADDITIONAL_PAYMENT`: no OpenAI API billing or new paid SaaS in the production contract.
- Existing paid surfaces allowed: ChatGPT Pro and Figma Pro.
- Do not automate ChatGPT via credential scraping, DOM automation, or unsupported private endpoints.
- Do not modify open PR #373, #376, or #386 files.
- Do not change `PROJECT_FIGMA_TARGET_REGISTRY.json` schema in this slice.
- Missing tool-specific Figma routes fail closed.
- TDD RED must be observed before production code is added.

---

### Task 1: Subscription handoff packet contract

**Files:**
- Create: `tools/base-tool-contracts/tests/test_subscription_handoff.py`
- Create: `tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`

**Interfaces:**
- Produces: `SubscriptionHandoffPacket`, `SubscriptionHandoffError`, `build_subscription_handoff_packet(...)`.
- Packet public view contains exact project/tool/run/workflow identity, source SHA-256, bounded instruction/count/dimension/review contract, `GPT_PRO_HANDOFF_READY`, `provider_call_made=False`, `requires_additional_payment=False`.

- [ ] **Step 1: Write failing tests**

Test that a valid packet is deterministic and that invalid project/tool/run IDs, non-SHA256 source hashes, excessive instructions/counts/dimensions, absolute paths, API-key-like fields, arbitrary Figma destinations, and unsupported workflows are rejected.

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest -q tools/base-tool-contracts/tests/test_subscription_handoff.py
```

Expected: collection/import failure because `base_tool_contracts.subscription_handoff` does not exist.

- [ ] **Step 3: Implement minimal contract**

Use frozen dataclasses/Pydantic only where useful. Do not add network access, clipboard access, browser automation, or provider clients.

- [ ] **Step 4: Run GREEN**

Run the focused test plus existing base-tool-contract tests.

- [ ] **Step 5: Commit**

Commit message: `feat(tool-contracts): add GPT Pro subscription handoff contract`.

### Task 2: Canonical tool-specific Figma route registry

**Files:**
- Create: `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`
- Create: `tools/base-tool-contracts/src/base_tool_contracts/figma_tool_routing.py`
- Create: `tools/base-tool-contracts/tests/test_figma_tool_routing.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`

**Interfaces:**
- Consumes: `ProjectFigmaRegistry.resolve_ready_target(project_id)`.
- Produces: `ProjectFigmaToolRouteRegistry`, `ProjectFigmaToolRoute`, and `resolve_ready_route(project_id, tool_route_id, project_registry)`.

- [ ] **Step 1: Write failing tests**

Require eight `character_expression_runs` routes, exact observed node IDs, matching project file key and parent node, unique project/route pairs, canonical numeric node IDs, different parent/destination IDs, and fail-closed missing/blocked routes.

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest -q tools/base-tool-contracts/tests/test_figma_tool_routing.py
```

Expected: import/file failure before implementation.

- [ ] **Step 3: Add registry and minimal loader**

The registry contains only reviewed IDs observed live on 2026-08-15. Do not invent sprite/effect route IDs.

- [ ] **Step 4: Add committed-byte canonical proof**

Reuse the same trusted-file and Git proof pattern as `figma_routing.py`.

- [ ] **Step 5: Run GREEN**

Run focused route tests plus existing Figma routing tests.

- [ ] **Step 6: Commit**

Commit message: `feat(tool-contracts): add Figma tool-node routing registry`.

### Task 3: CI and policy integration

**Files:**
- Create: `tests/test_tool_hub_subscription_production_contract.py`
- Modify only if needed and non-conflicting: `.github/workflows/validate-game-project-operating-system.yml`
- Update: `docs/superpowers/specs/2026-08-15-tool-hub-subscription-production-contracts-design.md` only for evidence corrections.

**Interfaces:**
- Ensures existing Tool Hub adapter still pins `subscription_handoff_import` for Expression/Sprite.
- Ensures normal production contract does not require or expose `OPENAI_API_KEY`.
- Ensures all eight project IDs have a ready Expression route.

- [ ] **Step 1: Add repository-level contract test**

The test reads current `tools/tool-hub/src/tool_hub/adapters.py`, Expression/Sprite parser defaults, and both Figma registries. It must fail if the subscription mode stops being canonical or a route disappears.

- [ ] **Step 2: Run focused repository contract**

```bash
python -m unittest tests/test_tool_hub_subscription_production_contract.py -v
```

- [ ] **Step 3: Ensure existing CI executes it**

Prefer adding the test to an already-required explicit contract list rather than creating another workflow. Only edit the workflow if the test is otherwise unreachable.

- [ ] **Step 4: Run contract regressions**

Run the same unittest command group used by `ubuntu-contract` where feasible, plus focused base-tool-contract tests.

- [ ] **Step 5: Commit**

Commit message: `test(tool-hub): enforce subscription-only production contracts`.

### Task 4: Adversarial review, exact-head CI, PR and merge

**Files:**
- No product file changes unless a validated P0/P1 finding requires a minimal fix.

- [ ] **Step 1: Attack**

Check secret/path leakage, route cross-wiring, duplicate IDs, malformed SHA/count/dimensions, paid-provider ambiguity, Figma-as-canon drift, stale observed node IDs, and overlap with #373/#376/#386.

- [ ] **Step 2: Validate critique**

Discard hypothetical findings not supported by code/contracts. Record remaining P0/P1/P2.

- [ ] **Step 3: Minimal refinement and regression recheck**

P0/P1 must be zero before merge.

- [ ] **Step 4: Open PR for Issue #393 partial independent slice**

PR body must state that UI integration/live GPT Pro/Figma mutation remain follow-up gates after open prerequisites merge.

- [ ] **Step 5: Verify exact-head Actions and review threads**

Required checks must pass, unresolved threads must be zero, and the reviewed head SHA must match the merge request.

- [ ] **Step 6: Squash merge**

Merge only if repository protection permits. Then re-read merged files from `main` and inspect post-merge Actions.

## Self-review

- Spec coverage: no-extra-payment boundary, GPT Pro handoff, exact Figma tool routes, canonical proof, and IRG are each mapped to tasks.
- No placeholders remain.
- Interfaces use consistent names across tasks.
- Open PR-owned UI/supervisor/Figma Bridge files are excluded except read-only repository contract assertions.