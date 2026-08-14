# Tool Hub Subscription-Only Production Contracts Implementation Plan

> **Execution mode:** superpowers writing-plans + executing-plans + TDD. GitHub feature branch is the isolation boundary because a local worktree is unavailable in this tool environment.

**Goal:** Add shared, testable contracts for a no-additional-payment ChatGPT Pro handoff path and exact tool-specific Figma destinations without touching open Tool Hub product PRs.

**Architecture:** Keep `PROJECT_FIGMA_TARGET_REGISTRY.json` as the project/file/parent authority, add an additive tool-route registry for reviewed descendant nodes, and add a network-free `subscription_handoff` contract for GPT Pro handoff packets. Keep a narrow focused workflow for regression because this contract spans shared contracts plus three existing visual-tool boundaries and does not belong in the already-large central workflow.

**Tech Stack:** Python 3.12, Pydantic 2, Base trusted-file helpers, JSON registries, unittest/pytest-compatible tests, GitHub Actions Ubuntu/Windows matrix.

## Global Constraints

- `NO_ADDITIONAL_PAYMENT`: no OpenAI API billing or new paid SaaS in the production contract.
- Existing paid surfaces allowed: ChatGPT Pro and Figma Pro.
- Do not automate ChatGPT via credential scraping, DOM automation, or unsupported private endpoints.
- Do not modify open PR #373, #376, or #386 files.
- Do not change `PROJECT_FIGMA_TARGET_REGISTRY.json` schema in this slice.
- Missing tool-specific Figma routes fail closed.
- TDD RED must be observed before production implementation.

---

## Task 1 — Subscription handoff packet contract — COMPLETE

**Files:**
- `tools/base-tool-contracts/tests/test_subscription_handoff.py`
- `tools/base-tool-contracts/src/base_tool_contracts/subscription_handoff.py`
- `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`

- [x] Write failing tests.
- [x] Observe RED in focused workflow run `31818432974`: missing `base_tool_contracts.subscription_handoff`.
- [x] Implement network-free packet builder.
- [x] Fix truth fields: `GPT_PRO_HANDOFF_READY`, `CHATGPT_PRO_SUBSCRIPTION`, `image/png`, `provider_call_made=false`, `requires_additional_payment=false`.
- [x] Make all fixed truth fields non-overridable constructor fields with `init=False`.
- [x] Reject invalid project/tool/run identities, Windows-special/path-shaped source filenames, invalid SHA-256, secret/token-like instruction content, non-integer/unbounded count/dimensions, malformed checklist values, and workflow/tool cross-wiring.
- [x] Prove initial GREEN in run `31818614093` on Ubuntu and Windows.
- [x] Adversarial RED in run `31819013278` for missing subscription-surface/output fields.
- [x] Prove refined GREEN in run `31819211022` on Ubuntu and Windows.
- [x] Truth/type hardening RED in run `31819588625`: `11 failed, 21 passed`, with failures limited to intended hardening gaps.
- [x] Truth/type hardening GREEN in run `31819831239` on Ubuntu and Windows.

## Task 2 — Canonical tool-specific Figma route registry — COMPLETE

**Files:**
- `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`
- `tools/base-tool-contracts/src/base_tool_contracts/figma_tool_routing.py`
- `tools/base-tool-contracts/tests/test_figma_tool_routing.py`
- `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`

- [x] Write failing tests.
- [x] Observe RED in run `31818432974`: missing `base_tool_contracts.figma_tool_routing`.
- [x] Add eight reviewed `character_expression_runs` routes from live Figma inspection.
- [x] Cross-check each route against the project registry's file key and generation-area parent.
- [x] Add canonical committed-byte and unchanged-after-load proof.
- [x] Keep sprite/effect destination routes absent until reviewed nodes exist.
- [x] Pin exact project-marker node IDs and expected `FRAME` type for parent/destination/marker.
- [x] Reject duplicate pairs, same parent/destination, reused marker node, malformed IDs, non-FRAME types, project/file/parent cross-wiring.
- [x] Prove refined GREEN in run `31819211022` on Ubuntu and Windows.
- [x] Reconfirm route contracts as part of final hardening GREEN `31819831239` on Ubuntu and Windows.

## Task 3 — Repository production-boundary regression — COMPLETE

**Files:**
- `tests/test_tool_hub_subscription_production_contract.py`
- `.github/workflows/validate-tool-hub-subscription-contracts.yml`

- [x] Assert current Tool Hub adapter pins `subscription_handoff_import` for visual Studios.
- [x] Assert Expression/Sprite parser defaults remain subscription handoff/import.
- [x] Assert Tool Hub adapter does not introduce `OPENAI_API_KEY`.
- [x] Assert shared subscription contract imports no OpenAI/network/browser-automation client.
- [x] Assert fixed truth fields use `init=False`.
- [x] Assert all eight registered projects have exactly one reviewed Character/Expression route.
- [x] Assert no unreviewed sprite/effect node ID is invented.
- [x] Keep the focused workflow as a permanent narrow regression surface with Ubuntu and Windows matrix.
- [x] Prove repository-boundary GREEN in run `31818787891` on Ubuntu and Windows.
- [x] Prove refined package + repository GREEN in run `31819211022` on Ubuntu and Windows.
- [x] Prove final hardening package + repository GREEN in run `31819831239` on Ubuntu and Windows.

## Task 4 — Adversarial review, exact-head CI, PR and merge — PRE-MERGE IN PROGRESS

**PR:** #394, Issue #393 independent slice.

- [x] Open draft PR without touching #373/#376/#386.
- [x] Attack paid-provider ambiguity; refinement added fixed ChatGPT Pro surface and PNG output.
- [x] Attack constructor truth-field spoofing and weak runtime typing; hardening made truth fields `init=False` and rejects invalid runtime types consistently.
- [x] Attack Figma cross-file/stale-name ambiguity; refinement added exact marker IDs and expected FRAME types.
- [x] Attack route invention; sprite/effect routes remain absent and fail closed.
- [x] Attack canonical drift; committed-byte proof and repository regression cover the route file.
- [x] Attack secret/private-path leakage; packet input constraints and static no-client test cover the current surface.
- [x] Fetch PR changed files and verify zero changed-file overlap with open PR #373/#376/#386.
- [ ] Confirm final document-head focused workflow, Base v9, Game Project Operating System, and Dependency Review are successful.
- [ ] Confirm unresolved review threads = 0 and final P0/P1 = 0.
- [ ] Update PR body from TDD-RED wording to final verified slice and mark ready.
- [ ] Squash merge exact reviewed head.
- [ ] Re-read merged `main` files and inspect post-merge workflow runs.

## Deliberately deferred product integration

This independent slice must not be confused with the complete product loop. The following cannot be implemented here without editing files currently owned by open prerequisite PRs:

- Character/Outfit/Scene UI integration — #373
- localhost-to-Figma Bridge transport/readback — #376
- Windows Studio child execution — #386

After those are merged into `main`, Issue #393 continues with a follow-up integration slice for:

`project -> tool -> configure -> GPT Pro로 생성 -> import -> choose -> 확정 및 전달`

and real evidence for:

- two simultaneous projects;
- real ChatGPT Pro-generated Character/Expression import;
- real pose sequence and effect stages import;
- project Asset Vault persistence;
- same accepted SHA-256 delivered to Figma;
- live node ID/name/type/marker revalidation;
- readback receipt;
- actual project asset consumption.

Until then those states remain `NOT_RUN`/`NOT_PROVED_HERE` rather than being inferred from contract tests.

## Self-review

- No placeholder requirements remain in this slice.
- Spec and implementation use the same packet/route field names.
- Focused CI ownership matches the actual workflow instead of claiming central-CI integration.
- Open PR-owned UI/supervisor/Figma Bridge files are read-only dependencies and are not modified by this branch.
