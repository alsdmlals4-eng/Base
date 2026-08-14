# Adversarial Review — GPT Pro Handoff Import Provenance

Date: 2026-08-15
Issue: #404
PR: #406

## Attack → validate critique → minimal refinement → regression recheck

### Attack 1 — Can a caller relabel GPT Pro output as another source?

**Risk:** If `declared_source` remains a free handoff value, a UI or caller could choose `OTHER_USER_SUPPLIED` or another provenance after generation.

**Validation:** Merged Expression and Sprite import modules both already define `CHATGPT_INCLUDED` as the reviewed source for images created in the subscribed ChatGPT surface. The shared #394 packet did not pin the corresponding consumer value.

**Refinement:** Add frozen `init=False` truth `import_declared_source="CHATGPT_INCLUDED"` and expose it in the packet `import` object. Tests reject constructor/builder override attempts.

### Attack 2 — Can the packet drift to a paid/local engine run mode?

**Risk:** `generation_surface=CHATGPT_PRO_SUBSCRIPTION` could coexist with a later import into `openai` or another run mode.

**Validation:** Current Tool Hub and both Studio apps use `subscription_handoff_import` as the reviewed no-additional-payment path.

**Refinement:** Add frozen `import_run_mode="subscription_handoff_import"`; repository contract binds the shared truth to both Studio app defaults.

### Attack 3 — Does this accidentally authorize provider execution or extra payment?

**Validation:** The patch does not add any network/browser/provider import and leaves `provider_call_made=false` and `requires_additional_payment=false` untouched. It only adds literal import metadata.

**Verdict:** no new provider authority.

### Attack 4 — Does this weaken project/Figma isolation?

**Validation:** No project path, Figma file/node, credential, route, or mutation field is added. Existing #394 private-routing rejection remains unchanged.

**Verdict:** no routing authority expansion.

### Attack 5 — Does this collide with open PR #373/#376/#386?

**Validation:** Changed product file is only `tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py`; remaining changes are its tests/spec/plan/review. None of the three open PRs change that shared handoff module or these test/docs paths.

**Verdict:** zero source-file overlap with protected in-progress work.

## TDD evidence

- RED workflow: `Validate Tool Hub Subscription Contracts` run `31828646146`.
- Ubuntu RED: 2 intended failures, 33 existing focused tests passed.
- Root cause: missing `import` public view and missing `import_run_mode` attribute.
- GREEN run: pending final cross-platform exact-head result at time this review record was created; do not treat this document alone as PASS evidence.

## Findings

- P0: 0
- P1: 0
- P2: 0 after minimal refinement

## IRG ceiling

This change proves only the handoff/import provenance contract. Real ChatGPT Pro image generation, browser import UX, visual quality, live Figma delivery, Windows Studio child runtime and project asset consumption remain separate gates.
