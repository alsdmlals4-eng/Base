# Tool Hub Subscription-Only Production Contracts Design

## Goal

Make the shared Tool Hub contracts enforce a production path that requires no new paid API or per-call service: ChatGPT Pro handoff/import for generation, local validation/storage, and exact project/tool Figma routing.

## Hard constraints

- `NO_ADDITIONAL_PAYMENT`: the normal production route must not require OpenAI API billing, prepaid credits, or another paid SaaS.
- Allowed paid surfaces are the user's existing ChatGPT Pro and Figma Pro subscriptions.
- Do not scrape ChatGPT credentials, browser DOM, private endpoints, or unsupported subscription APIs.
- Keep the current localhost HTML/JS + Python backend; Tauri remains an optional packaging shell after the workflow is proven.
- Do not modify or duplicate open PR #373, #376, or #386. This slice owns only new shared contracts, a new tool-route registry, tests, and documentation.
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

A packet is a user-visible bridge between the local Tool Hub and the normal ChatGPT Pro UI. Required fields:

- `schema_version = 1`
- exact `project_id`, `tool_id`, `run_id`
- `workflow` in `character_edit | sprite_pose_sequence | sprite_effect_stages`
- source declaration with immutable SHA-256 and local display filename only
- bounded generation instruction
- expected PNG count and allowed dimension range
- review checklist
- explicit state `GPT_PRO_HANDOFF_READY`
- explicit `provider_call_made = false`
- explicit `requires_additional_payment = false`

The packet must not contain API keys, tokens, absolute private paths, arbitrary Figma URLs/node IDs, or a claim that generation occurred.

## Import boundary

Imported results are not trusted because a packet exists. A later Studio integration must inspect actual PNG bytes and record source/run identity before a result can become delivery eligible. Fixture/simulated files remain non-production evidence.

## Tool-specific Figma routes

Canonical file: `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`.

Each entry binds:

- `project_id`
- `tool_route_id`
- `figma_file_key`
- `parent_node_id`
- `destination_node_id`
- `destination_name`
- `project_marker_name`
- `status`

Initial route:

- `character_expression_runs` -> `Expression Runs`

Live inspection on 2026-08-15 confirmed this destination under the registered `Generated Assets` parent for all eight projects. Sprite action/effect routes are intentionally absent until reviewed dedicated nodes exist; missing routes fail closed instead of inventing node IDs.

## Route validation

`ProjectFigmaToolRouteRegistry` must:

1. reject duplicate `(project_id, tool_route_id)` pairs;
2. reject malformed IDs/file keys;
3. cross-check the route's file key and parent node against `ProjectFigmaRegistry.resolve_ready_target(project_id)`;
4. require destination and parent nodes to differ;
5. return a typed route only for `READY_FOR_DELIVERY` entries;
6. prove the canonical registry matches its committed Base blob before production use;
7. expose no mutation client or credential.

A later #376 follow-up will additionally verify live Figma node name/type/project marker before mutation and submit a readback receipt.

## Initial observed routes

| project_id | parent | Expression Runs |
|---|---:|---:|
| coc-fiction | `12:3` | `15:2` |
| ten-paces-hidden-moves | `22:3` | `28:2` |
| ninja-survival | `12:3` | `15:2` |
| switchy-express-cargo-puzzle | `11:3` | `14:2` |
| urban-legend | `11:3` | `14:2` |
| grimoire-how-to-rewrite-the-world | `8:3` | `11:2` |
| blacksmith | `13:3` | `18:2` |
| omenward | `10:3` | `13:2` |

The corresponding hidden marker name is `Base Tool Hub Route · <project_id>`.

## UX integration boundary

This PR does not touch the currently-owned Studio/Hub UI files. After #373/#376/#386 merge, a follow-up must provide the user-facing sequence:

`project -> tool -> configure -> GPT Pro로 생성 -> import -> choose -> 확정 및 전달`.

No normal UI API-key field, arbitrary Figma target input, or Git path field is allowed.

## IRG

This slice can prove only:

- subscription handoff packet contract: implemented/tested;
- no-extra-payment metadata and secret/path exclusion: implemented/tested;
- eight-project Expression Runs route registry: implemented/tested against Base project routing;
- canonical file proof: implemented/tested.

It cannot prove:

- real ChatGPT Pro image generation;
- Windows Studio child launch;
- live Figma Bridge mutation/readback;
- character visual identity quality;
- real sprite pose/effect quality;
- real game-project asset consumption.

Those remain `NOT_RUN` or owned by the open prerequisite PRs/follow-up integration.

## Rollback

Revert the eventual merge. The new contract module and additive tool-route registry have no data migration and do not delete project assets or Figma nodes.