# Base Tool Hub Subscription-Only Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable GPT Pro handoff packet contract and exact tool-specific Figma routing metadata without touching the open Character, Figma Bridge, or Windows child PRs.

**Architecture:** Keep generation outside the local app and represent it as a bounded `SubscriptionHandoffPacket` that is safe to copy to ChatGPT Pro and later import into the same run. Extend the existing Figma registry additively with reviewed `tool_destinations`, preserving the generic `generation_area_node_id` fallback so current consumers remain compatible.

**Tech Stack:** Python 3.12, Pydantic 2, pytest, JSON registry.

## Global Constraints

- `NO_ADDITIONAL_PAYMENT`: production path must not require OpenAI API credits or another paid service.
- Existing paid surfaces allowed: ChatGPT Pro and Figma Pro.
- Do not automate ChatGPT with cookies, DOM scraping, private endpoints, or unsupported subscription APIs.
- Do not modify any file changed by open PR #373, #376, or #386.
- Preserve `PROJECT_FIGMA_TARGET_REGISTRY.json` version 1 and existing public methods.
- Exact tool destination IDs come only from live-inspected Figma nodes.

---

### Task 1: Subscription handoff packet contract

**Files:**
- Create: `tools/base-tool-contracts/tests/test_subscription_handoff.py`
- Create: `tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`

**Interfaces:**
- Produces `SubscriptionHandoffPacket.create(...)` and `public_view()`.
- Fixed values: `generation_surface="CHATGPT_PRO"`, `run_mode="subscription_handoff_import"`, `output_media_type="image/png"`.

- [ ] **Step 1: Write failing tests**

Test that a valid packet preserves exact `project_id/tool_id/run_id`, output count and bounded instructions; rejects invalid IDs, empty instructions, output counts outside `1..8`, strings containing `OPENAI_API_KEY`, `sk-`, absolute Windows/POSIX paths, or caller-supplied Figma node/file targets; and exposes no API credential fields in `public_view()`.

- [ ] **Step 2: Run RED**

Run:

```bash
python -m pytest -q tools/base-tool-contracts/tests/test_subscription_handoff.py
```

Expected: import failure because `base_tool_contracts.subscription_handoff` does not exist.

- [ ] **Step 3: Implement minimal packet**

Use a frozen dataclass with a strict `create()` validator. Keep strings bounded and printable. Do not add network, browser, clipboard, provider SDK, or filesystem behavior.

- [ ] **Step 4: Run GREEN and package regression**

```bash
python -m pytest -q tools/base-tool-contracts/tests/test_subscription_handoff.py tools/base-tool-contracts/tests
```

- [ ] **Step 5: Commit**

Commit message: `feat(tool-contracts): add GPT Pro handoff packet`

---

### Task 2: Tool-specific Figma routing contract

**Files:**
- Modify: `tools/base-tool-contracts/tests/test_figma_routing.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/figma_routing.py`
- Modify: `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`

**Interfaces:**
- Add optional registry entry field `tool_destinations: dict[str, str]`.
- Add `ProjectFigmaTarget.tool_destinations` as an immutable mapping.
- Add `ProjectFigmaTarget.node_for_tool(tool_id: str) -> str`.
- Exact mapping initially only for `expression-studio`; unknown/unmapped tools return `generation_area_node_id`.

- [ ] **Step 1: Write failing routing tests**

Verify all eight projects return the live-inspected Expression Runs ID for `expression-studio`, `sprite-animation-studio` falls back to `generation_area_node_id`, malformed node IDs fail validation, and duplicate/unknown arbitrary runtime destination cannot be supplied through the resolver API.

- [ ] **Step 2: Run RED**

```bash
python -m pytest -q tools/base-tool-contracts/tests/test_figma_routing.py
```

Expected: failure because `node_for_tool` and `tool_destinations` do not exist.

- [ ] **Step 3: Implement additive parser and target method**

Keep `version: 1`. Validate tool IDs with the same lower-kebab pattern as Base tools and destination IDs as canonical `N:N`. Convert the mapping to a read-only `MappingProxyType` in `ProjectFigmaTarget`.

- [ ] **Step 4: Populate eight reviewed Expression node IDs**

Use the exact live-inspected IDs from the design spec. Do not invent Sprite Action/Effect nodes.

- [ ] **Step 5: Run GREEN and compatibility regression**

```bash
python -m pytest -q tools/base-tool-contracts/tests
```

Then run existing consumers that load the registry without modifying them.

- [ ] **Step 6: Commit**

Commit message: `feat(figma): pin tool-specific delivery nodes`

---

### Task 3: Adversarial review and merge gate

**Files:**
- Create: `docs/reviews/2026-08-15-tool-hub-subscription-routing-adversarial-review.md`

- [ ] Attack API-credit leakage, unsupported ChatGPT automation, arbitrary Figma target injection, stale node IDs, fallback regressions, cross-project routing, and accidental overlap with PR #373/#376/#386.
- [ ] Validate critiques against the exact diff and current `main`.
- [ ] Apply only minimal corrections.
- [ ] Re-run base-tool-contracts and Base required checks.
- [ ] Require unresolved review threads `0`, P0/P1 `0`, and exact-head required checks before squash merge.
- [ ] After merge, re-read `main`; do not claim end-to-end generation/delivery because those depend on the still-open implementation PRs.
