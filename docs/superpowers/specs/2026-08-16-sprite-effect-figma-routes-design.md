# Dedicated Sprite Action / Effect Figma Routes Design

## Status

Approved design direction from the user on 2026-08-16. This document defines the implementation boundary before code/Figma mutation work begins.

## Goal

Extend the existing exact-node Figma routing contract so each of the eight registered projects has three peer delivery destinations under its existing `Generated Assets` frame:

1. `Expression Runs` — existing Character/Expression route, unchanged.
2. `Sprite Action Runs` — new dedicated Sprite action destination.
3. `Effect Runs` — new dedicated Sprite effect destination.

The change removes the current Sprite/Effect `DELIVERY_TOOL_ROUTE_UNAVAILABLE` blocker without weakening project isolation, node identity validation, cost boundaries, approval boundaries, or same-SHA receipt requirements.

## Non-goals

- Do not reuse `Expression Runs` for Sprite or Effect output.
- Do not deliver Sprite/Effect output to generic `Generated Assets`.
- Do not add a second project marker or a second routing authority.
- Do not grant `PROJECT_ASSET_APPROVED` or change any project asset manifest.
- Do not add an OpenAI API key, paid image API, metered provider, or other incremental-cost production dependency.
- Do not claim user-PC Tool Hub, real ChatGPT Pro pixel quality, localhost Figma Bridge receipt, or Godot consumption from cloud-node/CI evidence alone.
- Do not modify unrelated open PR branches. When an approved overlap exists, use the merged Base copy-integration standing authorization: reconcile onto a separate latest-main integration branch and keep owner branches read-only.

## Existing authority and invariants

The canonical Base registry is:

`docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`

The runtime loader is:

`tools/base-tool-contracts/src/base_tool_contracts/figma_tool_routing.py`

Existing invariants remain unchanged:

- each route is keyed by `(project_id, tool_route_id)`;
- `figma_file_key` must match the registered project target;
- `parent_node_id` must equal the project's registered generation-area node;
- parent, destination, and marker node types remain `FRAME`;
- `project_marker_name` must equal `Base Tool Hub Route · <project_id>`;
- the marker must remain distinct from parent and destination;
- only `READY_FOR_DELIVERY` routes may be resolved for mutation;
- the canonical registry must match committed Base bytes at delivery time;
- route/name/type/project/hash drift fails closed;
- caller/browser input is never mutation authority.

## Figma structure

For every registered project, keep the existing `Generated Assets` frame and existing hidden project marker. Add two peer frames next to the existing `Expression Runs` frame:

```text
Generated Assets
├─ Expression Runs
├─ Sprite Action Runs
├─ Effect Runs
└─ Base Tool Hub Route · <project_id>  [hidden, existing]
```

### Layout

All eight current `Generated Assets` frames are `1440×960`, and the existing `Expression Runs` frame is `1360×148` at `x=40, y=240`.

The new frames use the same width/height and horizontal alignment:

- `Sprite Action Runs`: `x=40, y=408, width=1360, height=148`
- `Effect Runs`: `x=40, y=576, width=1360, height=148`

No resize of `Generated Assets` is required.

Each new frame follows the existing `Expression Runs` internal presentation pattern: one title text node near the top and one concise note describing that the frame is a Base Tool Hub exact delivery destination. The route frame itself, not the text child, is the canonical destination node.

## Project inventory

The existing parent/marker authority is reused exactly as follows. New destination IDs are intentionally absent here; implementation must create the actual Figma frames and then read back their real node IDs before any Base route is marked `READY_FOR_DELIVERY`.

| project_id | figma_file_key | Generated Assets parent | existing Expression Runs | existing project marker |
|---|---|---:|---:|---:|
| `coc-fiction` | `PEa5zDbPHll3eHiNKX0e1k` | `12:3` | `15:2` | `23:2` |
| `ten-paces-hidden-moves` | `pVQ2e6aK45iL8BLBJWDSw4` | `22:3` | `28:2` | `38:2` |
| `ninja-survival` | `xNm1xbYPftEaAE2jOENlvt` | `12:3` | `15:2` | `20:2` |
| `switchy-express-cargo-puzzle` | `QMbylbdAi96PGSdHIT3AGa` | `11:3` | `14:2` | `19:2` |
| `urban-legend` | `Z7J3eLeavEytKN20H4HfoP` | `11:3` | `14:2` | `19:2` |
| `grimoire-how-to-rewrite-the-world` | `AdOGNMp61AZSMMvBVxsVBd` | `8:3` | `11:2` | `16:2` |
| `blacksmith` | `xy6W4ga6ldkF3TvP0eRmtN` | `13:3` | `18:2` | `24:2` |
| `omenward` | `IhxUJaS6ik6MpBzdxt6o8D` | `10:3` | `13:2` | `19:2` |

## Canonical route IDs

The final registry contains exactly three active route IDs for each of the eight registered projects:

- `character_expression_runs`
- `sprite_action_runs`
- `effect_runs`

That produces 24 active project/tool route pairs in the current eight-project registry.

Canonical destination names are exact:

- `character_expression_runs` → `Expression Runs`
- `sprite_action_runs` → `Sprite Action Runs`
- `effect_runs` → `Effect Runs`

No aliases or runtime layer-name search are allowed as mutation authority.

## Creation and registration sequence

1. Re-read latest completed Base `main` and the eight Figma parents/markers before mutation.
2. For each project, verify the existing parent, `Expression Runs`, and marker IDs/names/types still match the current Base registry.
3. If either new route frame already exists, do not create a duplicate. Read it back and accept it only when its parent, exact name, type, geometry, and project context match this spec.
4. Otherwise create `Sprite Action Runs` and `Effect Runs` under the exact registered `Generated Assets` parent.
5. Read back all 16 new route frames through the Figma connector and record their real node IDs.
6. Add the resulting 16 route entries to `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`; retain the eight existing Character/Expression entries unchanged.
7. Only after readback evidence exists may the new entries use `delivery_status: READY_FOR_DELIVERY`.
8. Run exact-head tests and CI before merge.
9. After merge, read the registry from new `main` and re-read all 24 Figma destinations to detect route drift.

## Fail-closed behavior

The following cases must remain blocked:

- a Sprite action delivery resolves to `character_expression_runs` instead of `sprite_action_runs`;
- an Effect delivery resolves to `character_expression_runs` instead of `effect_runs`;
- Sprite/Effect delivery falls back to generic `Generated Assets`;
- destination node is missing, renamed, reparented, wrong type, or belongs to the wrong Figma file;
- project marker is missing, renamed, wrong type, or no longer distinct from route nodes;
- a browser/request supplies a project, Figma URL, node ID, or route different from the server/canonical registry;
- the registry changes after loading or differs from committed Base bytes;
- the delivered file SHA differs from the accepted run SHA;
- an unregistered project or unregistered tool route is requested.

The expected public result for missing/unavailable Sprite/Effect routes remains a blocked state such as `DELIVERY_TOOL_ROUTE_UNAVAILABLE`; implementation must not silently degrade to a generic destination.

## Testing requirements

### Registry contract

Tests must prove:

- all 8 projects retain `character_expression_runs`;
- all 8 projects gain `sprite_action_runs` and `effect_runs`;
- total active route pairs = 24;
- destination names match the exact canonical names;
- parent/file/marker authority remains the same per project;
- no duplicate `(project_id, tool_route_id)` pair exists;
- all new destinations are distinct from parent, marker, and the project's other destinations.

### Delivery routing

Focused tests must prove:

- Sprite action delivery selects only `sprite_action_runs`;
- effect delivery selects only `effect_runs`;
- Character/Expression behavior is unchanged;
- generic-parent and Character-route fallback for Sprite/Effect are rejected;
- wrong project/file/node/name/type/hash fails closed;
- idempotent same-run/same-SHA behavior remains unchanged.

### Figma cloud preflight

After creation, the connector must read back each new destination and confirm:

- exact file key;
- exact parent relation;
- exact frame name;
- node type `FRAME`;
- expected geometry;
- existing project marker still present;
- no duplicate sibling route with the same canonical name.

Cloud preflight is evidence of node identity/layout only. It is not a localhost Bridge receipt.

### CI and post-merge

The implementation PR must run the existing Base operating/tool-route/Tool Hub/Figma integration tests that cover the changed registry and delivery path. Any new test must be executed by CI rather than merely committed.

After merge, repeat:

- new `main` readback;
- registry readback;
- 24-route count;
- Figma cloud node readback;
- relevant post-merge workflow status.

## Error recovery and idempotency

Figma creation must be retry-safe. A retry first searches only the exact registered parent for exact canonical sibling names and validates them before deciding whether creation is needed. It must never create `Sprite Action Runs 2`, `Effect Runs Copy`, or similar duplicates.

If Figma creation succeeds for only some projects, the Base registry remains unchanged. Do not publish any of the 16 new routes until all 16 route frames have been created or safely reused and read back successfully. This keeps the current eight Character/Expression routes as the only active authority until the new route set is complete.

If Base registry update or CI later fails, the created empty Figma frames may remain as non-authoritative workspace structure; they become mutation authority only after a committed `READY_FOR_DELIVERY` registry entry passes canonical validation.

## Rollback

Rollback of the Base code/registry is additive and must not delete project assets.

- Revert the Base registry/test/runtime change as one unit.
- If a new Figma route frame is still empty, it may be removed during an explicit rollback.
- If a route frame contains delivered evidence/assets, do not delete it; retain it and mark/remove its Base route authority through the registry so the runtime no longer resolves it.
- Existing `Expression Runs`, project markers, project files, asset manifests, and receipts are never deleted by this rollback.

## Implementation Reality Gate boundary

Successful implementation and CI will establish:

- reviewed dedicated Sprite/Effect cloud destination nodes for all eight projects;
- exact Base registry authority for those nodes;
- fail-closed software routing to the correct destination class.

It will **not** by itself establish:

- actual user-PC `Base Tool Hub.lnk` execution;
- real ChatGPT Pro-generated `pose_sequence` quality;
- real ChatGPT Pro-generated `effect_stages` quality;
- localhost Figma Bridge same-SHA delivery/readback receipt;
- real project/Godot consumption.

Those remain separate live IRG steps after this routing prerequisite is merged.