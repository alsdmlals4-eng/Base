# Adversarial Review — ChatGPT Pro Handoff Prompt Renderer

Date: 2026-08-15
Issue: #411
PR: #412

## Attack → validate critique → minimal refinement → regression recheck

### Attack 1 — Was the RED test actually executed?

**Risk:** A new test file can exist while the permanent workflow still executes only the older test list, creating false GREEN evidence.

**Validation:** The first PR run passed even though `render_chatgpt_pro_prompt` did not exist. Inspection showed `Validate Tool Hub Subscription Contracts` did not include `test_subscription_prompt_renderer.py`.

**Refinement:** Add the renderer test file to the existing permanent subscription-contract workflow. The corrected run `31830496327` failed during collection because the renderer export did not exist, proving the intended RED boundary.

### Attack 2 — Can a caller bypass the builder by constructing the public dataclass directly?

**Risk:** `SubscriptionHandoffPacket` is public. A caller can instantiate it without `build_subscription_handoff_packet`, potentially injecting a Figma URL, credential-like text, or private path into the renderer.

**Validation:** Initial renderer accepted any `isinstance(packet, SubscriptionHandoffPacket)` object.

**Refinement:** Rebuild the packet through the canonical builder before rendering and require equality with the supplied packet. Directly constructed invalid packets and modified fixed truth fields must fail closed.

### Attack 3 — Can the renderer create a paid/provider authority surface?

**Validation:** Renderer inputs are only the revalidated packet. Static output explicitly says no API/provider call is requested and retains `provider_call_made=false`, `requires_additional_payment=false`, `subscription_handoff_import`, and `CHATGPT_INCLUDED`. No provider SDK, network, browser, clipboard, shell, or Figma client is imported.

**Verdict:** no new paid/provider execution authority.

### Attack 4 — Can Figma/private routing leak into the prompt?

**Validation:** Builder rejects credential-like text, absolute local paths, Figma URLs, and node IDs in the only user-controlled text fields. Renderer revalidates before interpolation and itself generates no Figma target or local path.

**Verdict:** fail closed after the dataclass-bypass refinement.

### Attack 5 — Can output become unbounded?

**Validation:** Packet instruction is bounded to 4,000 characters, checklist to 12 × 240 characters, source filename and identities are bounded, and renderer adds a final 12 KiB UTF-8 ceiling. A maximum-valid-packet regression is included.

**Verdict:** bounded.

### Attack 6 — Does this collide with protected open implementation PRs?

**Validation:** #373/#376/#386 do not own `subscription_handoff.py`, its renderer test, or this review. The permanent subscription workflow is shared but no runtime owner or child-process source is changed.

**Verdict:** no product-source overlap with protected in-progress work.

## TDD evidence

- False-GREEN discovery: initial renderer test was not connected to the workflow; not accepted as evidence.
- Corrected RED: `Validate Tool Hub Subscription Contracts` run `31830496327`, Ubuntu failed at import because `render_chatgpt_pro_prompt` was absent.
- GREEN after implementation: exact final-head run must be checked after the last tamper-regression commit; this document alone is not PASS evidence.

## Findings

- P0: 0
- P1: 0 after packet revalidation refinement
- P2: 0 pending final exact-head regression

## IRG ceiling

This PR can prove deterministic, bounded, subscription-only prompt rendering from a revalidated handoff packet. It does not prove ChatGPT Pro browser interaction, generated pixels, download/import UX, visual quality, Figma mutation/readback, or game-project consumption.
