# GPT Pro Handoff → Studio Import Provenance Implementation Plan

**Goal:** Bind merged #394 handoff truth to the exact existing Studio import provenance without touching open implementation PRs.

### Task 1 — RED contract tests

Files:
- Modify `tools/base-tool-contracts/tests/test_subscription_handoff.py`
- Modify `tests/test_tool_hub_subscription_production_contract.py`

Require fixed non-constructor fields `import_run_mode` and `import_declared_source`, expose them in `public_view()`, and verify current Expression/Sprite import modules retain `CHATGPT_INCLUDED` while their apps retain `subscription_handoff_import`.

Run existing permanent workflow `Validate Tool Hub Subscription Contracts`; expected RED because the two handoff fields are absent.

### Task 2 — Minimal implementation

File:
- Modify `tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py`

Add only two frozen `init=False` truth fields and the public `import` object. No network, clipboard, browser or Studio source changes.

### Task 3 — GREEN and adversarial gate

Run the existing focused Ubuntu/Windows workflow plus Base required checks. Attack user override, source drift, cost-truth regression, and open-PR overlap. Require exact head, P0/P1=0, unresolved threads=0, then squash merge and re-read main.
