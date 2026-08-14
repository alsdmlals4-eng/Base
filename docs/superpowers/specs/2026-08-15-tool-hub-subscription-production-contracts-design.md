# Tool Hub Subscription-Only Production Contracts Design

## Goal

Make the shared Tool Hub contracts enforce a production path that requires no new paid API or per-call service: ChatGPT Pro handoff/import for generation, local validation/storage, and exact project/tool Figma routing.

## Hard constraints

- `NO_ADDITIONAL_PAYMENT`: the normal production route must not require OpenAI API billing, prepaid credits, or another paid SaaS.
- Allowed paid surfaces are the user's existing ChatGPT Pro and Figma Pro subscriptions.
- Do not scrape ChatGPT credentials, browser DOM, private endpoints, or unsupported subscription APIs.
- Keep the current localhost HTML/JS + Python backend; Tauri remains an optional packaging shell after the workflow is proven.
- Do not modify or duplicate open PR #373, #376, or #386. This slice owns only new shared contracts, a new tool-route registry, tests, focused CI, and documentation.
- Figma is a visual workspace/delivery surface, not narrative canon. PR #387 remains the narrative/Godot authority.

## Existing-solution-first decision

### REUSE — `subscription_handoff_import`
Expression Studio and Sprite Animation Studio already default to subscription handoff/import, and Tool Hub already pins that run mode. Promote this boundary into the supported production contract rather than building a paid provider integration.

### REUSE — Base project Figma registry
`PROJECT_FIGMA_TARGET_REGISTRY.json` remains the project/file/parent routing authority. Do not mutate it in this slice because open PR #376 consumes it.

### BUILD_NEW — additive tool-route registry
Add a separate canonical `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json` for tool-specific descendant destinations. This avoids changing the v1 project routing schema under an open Figma Bridge PR and gives future tools an additive route surface.

### BUILD_NEW — shared GPT Pro handoff contract
Add a small `base_tool_contracts.subscription_handoff` module that validates a bounded, deterministic handoff packet. It has no network/client automation and no API credentials.

## GPT Pro handoff packet

A packet is a user-visible bridge between the local Tool Hub and the normal ChatGPT Pro UI. Required fixed truth fields:

- `schema_version = 1`
- `state = GPT_PRO_HANDOFF_READY`
- `generation_surface = CHATGPT_PRO_SUBSCRIPTION`
- `output_media_type = image/png`
- `provider_call_made = false`
- `requires_additional_payment = false`

Required caller-bound fields:

- exact `project_id`, `tool_id`, `run_id`
- `workflow` in `character_edit | sprite_pose_sequence | sprite_effect_stages`
- source declaration with immutable SHA-256 and local display filename only
- bounded generation instruction
- expected PNG count and allowed dimension range
- review checklist

The builder does not accept a caller-selected generation surface or output type. The packet must not contain API keys, tokens, absolute private paths, arbitrary Figma URLs/node IDs, or a claim that generation occurred.

## Import boundary

Imported results are not trusted because a packet exists. A later Studio integration must inspect actual PNG bytes and record source/run identity before a result can become delivery eligible. Fixture/simulated files remain non-production evidence.

## Tool-specific Figma routes

Canonical file: `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`.

Each entry binds:

- `project_id`
- `tool_route_id`
- `figma_file_key`
- `parent_node_id` + fixed expected type `FRAME`
- `destination_node_id` + fixed expected type `FRAME`
- `destination_name`
- exact `project_marker_node_id` + fixed expected type `FRAME`
- exact `project_marker_name`
- `delivery_status`

Initial route:

- `character_expression_runs` -> `Expression Runs`

Live inspection on 2026-08-15 confirmed this destination under the registered `Generated Assets` parent for all eight projects. Sprite action/effect routes are intentionally absent until reviewed dedicated nodes exist; missing routes fail closed instead of inventing node IDs.

## Route validation

`ProjectFigmaToolRouteRegistry`:

1. rejects duplicate `(project_id, tool_route_id)` pairs;
2. rejects malformed IDs/file keys and non-FRAME observed node types;
3. cross-checks the route file key and parent node against `ProjectFigmaRegistry.resolve_ready_target(project_id)`;
4. requires parent, destination, and project-marker node IDs to be distinct inside the file;
5. requires marker name `Base Tool Hub Route · <project_id>`;
6. returns a typed route only for `READY_FOR_DELIVERY` entries;
7. proves the canonical registry matches its committed Base blob before production use;
8. exposes no mutation client or credential.

A later #376 follow-up must query the live Figma file and verify the pinned node IDs still have these reviewed names/types/marker identity before mutation, then submit a readback receipt.

## Initial observed routes

| project_id | parent | Expression Runs | project marker |
|---|---:|---:|---:|
| coc-fiction | `12:3` | `15:2` | `23:2` |
| ten-paces-hidden-moves | `22:3` | `28:2` | `38:2` |
| ninja-survival | `12:3` | `15:2` | `20:2` |
| switchy-express-cargo-puzzle | `11:3` | `14:2` | `19:2` |
| urban-legend | `11:3` | `14:2` | `19:2` |
| grimoire-how-to-rewrite-the-world | `8:3` | `11:2` | `16:2` |
| blacksmith | `13:3` | `18:2` | `24:2` |
| omenward | `10:3` | `13:2` | `19:2` |

All three reviewed node roles were observed as Figma `FRAME` nodes. The hidden marker name is `Base Tool Hub Route · <project_id>`.

## CI ownership

Keep `.github/workflows/validate-tool-hub-subscription-contracts.yml` as a narrow feature-owned regression workflow rather than editing the already-large central Game Project Operating System workflow. It triggers only when the handoff contract, visual-Studio subscription boundary, project/tool Figma registries, or its own tests change and runs the same focused contract suite on Ubuntu and Windows.

## UX integration boundary

This PR does not touch the currently-owned Studio/Hub UI files. After #373/#376/#386 merge, a follow-up must provide the user-facing sequence:

`project -> tool -> configure -> GPT Pro로 생성 -> import -> choose -> 확정 및 전달`.

No normal UI API-key field, arbitrary Figma target input, or Git path field is allowed.

## Executed evidence

### Initial RED

Focused workflow run `31818432974` failed as intended because both production modules were absent:

- `base_tool_contracts.subscription_handoff`: `ModuleNotFoundError`
- `base_tool_contracts.figma_tool_routing`: `ModuleNotFoundError`

### Initial GREEN

Focused workflow run `31818614093` passed on both Ubuntu and Windows after the minimal packet and route-registry implementation.

### Repository-boundary GREEN

Focused workflow run `31818787891` passed on both Ubuntu and Windows after adding the repository-level regression contract.

### Adversarial refinement RED

Focused workflow run `31819013278` failed on the intended missing fixed fields only: ChatGPT Pro generation surface/output media type and exact live Figma node-type/marker identity. Twenty existing focused tests remained passing.

### Adversarial refinement GREEN

Focused workflow run `31819211022` passed on both Ubuntu and Windows with package-level and repository-level contracts after adding those fixed fields.

## IRG

Verified in this slice:

- subscription handoff packet contract: `IMPLEMENTED_TESTED`
- generation surface fixed to ChatGPT Pro subscription: `IMPLEMENTED_TESTED`
- PNG output contract: `IMPLEMENTED_TESTED`
- provider-call/additional-payment truth fields: `IMPLEMENTED_TESTED`
- secret/private-path exclusion: `IMPLEMENTED_TESTED`
- eight-project Expression Runs route registry: `IMPLEMENTED_TESTED`
- exact parent/destination/project-marker IDs and FRAME types: `IMPLEMENTED_TESTED`
- canonical committed-byte proof: `IMPLEMENTED_TESTED`
- Ubuntu/Windows focused regression: `PASS`

Not proved by this slice:

- real ChatGPT Pro image generation: `NOT_RUN`
- Windows Studio child launch: owned by open PR #386 / `NOT_PROVED_HERE`
- live Figma Bridge mutation/readback: owned by open PR #376 / `NOT_RUN_HERE`
- character visual identity quality: `NOT_RUN`
- real sprite pose/effect quality: `NOT_RUN`
- real game-project asset consumption: `NOT_RUN`

No result above may be promoted to production-loop completion until those gates have their own evidence.

## Rollback

Revert the eventual merge. The new contract module, focused workflow, and additive tool-route registry have no data migration and do not delete project assets or Figma nodes.
