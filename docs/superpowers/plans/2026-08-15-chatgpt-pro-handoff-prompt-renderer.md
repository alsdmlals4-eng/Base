# ChatGPT Pro Handoff Prompt Renderer Implementation Plan

**Goal:** Add a pure renderer from the existing subscription handoff packet to a safe copy-ready ChatGPT Pro prompt.

### Task 1 — RED

Modify `tools/base-tool-contracts/tests/test_subscription_handoff.py` to require `render_chatgpt_pro_prompt` with deterministic identity/source/generation/review/import sections, no Figma/API/shell/private path content, and a bounded result.

Run the existing `Validate Tool Hub Subscription Contracts` workflow. Expected RED: renderer import/function absent.

### Task 2 — GREEN

Modify only:
- `tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py`
- `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`

Implement pure rendering from an already-validated packet. No network, clipboard, browser, filesystem, provider SDK, or Figma code.

### Task 3 — Review and merge

Run Ubuntu/Windows subscription contracts plus Base required gates. Adversarially check prompt injection surfaces, accidental local/Figma/API leakage, non-determinism, and scope overlap. Require P0/P1=0, unresolved threads=0, exact-head checks before squash merge.
