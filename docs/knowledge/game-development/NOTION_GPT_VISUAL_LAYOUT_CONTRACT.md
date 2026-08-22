# Notion ↔ GPT Visual Layout Contract

## Purpose

This contract defines the minimum reliable workflow for using GPT with the project Notion workspace so that approved visuals are placed in useful human-facing locations without turning the Home page into an AI metadata dump.

It extends `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`; it does not replace repository runtime truth or project-specific visual authority.

## Current decision

Use the existing **Notion MCP + Visual Registry metadata + bounded Layout Contract + Human/AI surface separation**.

```text
NOTION_DEFAULT_PROJECT_WORKSPACE
DIRECT_NOTION_ATTACHMENT_OR_BLOCKED
NO_LOCAL_BRIDGE_DEFAULT
NO_SHEETS_AS_NEW_IMAGE_TRANSPORT
```

Do not add a second dashboard, local binary bridge, Google Sheet relay, dedicated visual-delivery tool, or paid automation service by default.

### Alternatives considered

1. **Free-form GPT page redesign** — rejected as the default. It maximizes apparent flexibility but causes layout drift, weak repeatability, and accidental exposure of system metadata.
2. **External/local automation layer** — rejected as the default. It adds another failure surface, environment burden and duplicate routing authority.
3. **Notion MCP + bounded placement contract + direct attachment when callable** — adopted. It reuses the current project workspace, preserves human-readable Notion, keeps repository runtime authority separate, and fails closed when binary delivery is not currently supported.

Reconsider a new transport helper only when repeated real project evidence proves a direct attachment gap, Existing Solution First finds no supported route, and the user explicitly approves a new active tool boundary.

## Capability ceiling

`NOTION_TEXT_AND_STRUCTURE_READABLE != NOTION_IMAGE_SEMANTICS_VERIFIED`

`NOTION_BLOCK_WRITABLE != PIXEL_LAYOUT_CONTROLLED`

`MCP_DISCOVERED_AVAILABLE != CURRENT_CLIENT_EXECUTABLE`

`CURRENT_CLIENT_EXECUTABLE != EFFECT_VERIFIED`

`SERVER_READBACK_PASS != HUMAN_VISIBLE_DEVICE_PASS`

GPT distinguishes three kinds of evidence:

- **Structured page evidence**: page text, headings, properties, database records, image/file block references and surrounding context that the current Notion connection actually returns.
- **Visual evidence**: image pixels were supplied to or directly inspected by a vision-capable path in the current task.
- **UI-layout evidence**: the resulting Notion page/block arrangement was read back through a representation exposing the relevant structure, or manually verified by the user when visual geometry is not observable through the tool.

Never claim GPT understood image content merely because an image block, filename, caption or metadata exists.

### MCP Reality Gate

Workspace/self capability discovery is a routing hint, not completion evidence. A value such as `self.current_tool_access=available` does not prove the current client exposes the required callable function or schema.

```text
capability discovery
→ callable function + usable schema
→ minimum real invocation
→ durable destination readback
→ consumer / Android/iOS/browser observation when rendering matters
```

States remain distinct:

```text
DISCOVERED_ONLY / BLOCKED_TOOL_SURFACE
INVOCATION_PASS
READBACK_PASS
HUMAN_VISIBLE_PASS
```

A successful API/write call is at most `INVOCATION_PASS`. Do not treat a successful write invocation as durable effect without destination readback. Android/browser rendering becomes `HUMAN_VISIBLE_PASS` only after that client is actually observed.

## Binary media delivery routing

The current binary contract is:

```text
DIRECT_NOTION_ATTACHMENT_OR_BLOCKED
```

Notion MCP remains the owner for text, structure, databases, semantic placement and ordinary readback.

For an approved human-facing image:

```text
approved image / visual
→ current-client attachment capability check
→ trusted direct HTTPS source or connector-native attachment source available?
  → YES
     → invoke current Notion attachment function with its actual supported schema
     → require upload completion
     → consume returned attachment representation as-is
     → attach to exact Project destination
     → destination fetch/readback
     → client-visible observation when required
  → NO
     → BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT
```

`NO_LOCAL_BRIDGE_DEFAULT` means a binary capability gap does not automatically authorize a new local helper, PowerShell relay, local HTTP server, or desktop utility.

Google Sheets is `MIGRATION_ONLY_UNTIL_REMOVAL` and cannot be used as a new image relay. A temporary Sheet, even if deleted later, is still a new active transport and is forbidden by the current workspace boundary.

If no direct source is callable, block only the binary-delivery-dependent step. Continue independent planning, visual review, Notion text/structure, repository implementation and other safe work.

The detailed current transport/evidence ceiling is owned by `NOTION_CONNECTOR_IMAGE_DELIVERY_CORRECTION_2026-08-22.md`.

## Human and AI surfaces

`HUMAN_HOME_IS_NOT_AI_CONTEXT_DUMP`

Human-facing project surfaces prioritize comprehension and decision usefulness:

- Project Home
- Visual Bible
- human-facing Asset/Reference gallery
- approved Visual Map / Flow
- current focus, important decisions and links

AI/system surfaces retain processing metadata useful to automation but noisy to people:

- Asset ID
- Project
- Version
- Status
- Prompt
- AI Note
- Source
- Rights / License
- Hash
- Implementation Path
- Decision evidence
- placement/readback evidence

System metadata may be linked from the human page but must not be copied into Home as the default presentation.

## Visual Registry placement metadata

For any durable visual that may be reused or surfaced automatically, maintain enough structured metadata to place it without reinterpreting the asset from scratch.

Recommended minimum fields:

```text
Asset ID
Project
Status
Record Type
Subject
Purpose
Intended Use
Placement Priority
Preferred Surface
Source / Provenance
Version
Rights / License when external material is involved
```

Optional placement fields when useful:

```text
Placement:
  - Home / Hero
  - Visual Bible / Character
  - System page / Enhancement
Do Not Use:
  - AI operations page
  - unrelated project Home
Visual Evidence:
  DIRECT_INSPECTION | METADATA_ONLY | USER_DESCRIPTION
Layout Readback:
  VERIFIED | PARTIAL | NOT_RUN
```

`Status=APPROVED` is required before an asset can be treated as a project-approved visual. A prompt, art direction, graybox description, rejected candidate or `READY_TO_GENERATE` record is not an approved image.

## Placement decision sequence

Before inserting or moving a visual, GPT applies:

```text
identify project
→ identify record type and approval state
→ determine whether the visual is useful to a human reader
→ determine semantic destination
→ check for an existing canonical instance
→ choose prominence from intended use / placement priority
→ verify direct attachment availability when bytes must be delivered
→ place or link once
→ keep system metadata off the human surface
→ fetch/read back destination
→ verify expected block/record presence
→ report visual-geometry limits separately
```

### Placement priority

- `HERO`: one approved visual that best communicates the project or current core experience; Home top region only when it materially helps first comprehension.
- `PRIMARY`: important system/character/world/UI visual; place beside or immediately after the relevant human explanation.
- `SUPPORTING`: useful detail/reference; keep in the relevant Visual Bible or asset gallery rather than crowding Home.
- `ARCHIVE`: provenance/history only; not shown on normal human surfaces.

Do not promote every approved image to Home. Home is a summary surface, not the asset archive.

## Layout grammar

Notion supports image blocks, media alignment and columns. Use these features conservatively through the current Notion representation.

Default human layout:

```text
Project title
Hero visual when a true HERO exists
one-line project promise / current focus

Core experience
Primary visual(s) adjacent to the matching explanation

Core systems / world / UX
Supporting approved visuals near their owning section

Current state / decisions / important links
```

Rules:

- Prefer semantic proximity over decorative symmetry.
- Use two-column arrangements only when the current representation can create/preserve them reliably and the pair is genuinely comparative.
- Do not create dense mosaics merely to fill space.
- Do not move unrelated sections to make room for an image.
- Avoid duplicated canonical images. Reuse the same canonical record or link when possible.
- A generated Visual Map is derived presentation. Structured Screen/Flow records remain authoritative when the map disagrees.
- Pixel-level width, crop, mask and exact visual balance are manual/UI-level refinements unless the active tool path exposes and verifies them.

## Image understanding gate

When placement depends only on approved metadata/intended use, GPT may place an already available visual without re-inspecting pixels.

When a decision depends on composition, readability, character identity, UI hierarchy, contrast, cropping or similarity, require direct visual evidence.

```text
METADATA_ONLY
→ semantic placement allowed when intended use is already approved
→ no claim about pixel content

DIRECT_VISUAL_EVIDENCE
→ semantic + visual-quality judgement allowed within observed scope

NO_DIRECT_VISUAL_EVIDENCE + visual-content-dependent decision
→ BLOCKED_UNVERIFIED for that judgement
```

Do not generate a missing image merely to satisfy this gate. Image generation still follows the user's approval sequence and project policy.

## Delivery and readback

Every durable Notion visual organization change follows:

```text
read current destination
→ smallest bounded edit
→ write/attach through currently supported direct route
→ fetch/read back
→ verify expected block/record and surrounding section
```

A successful write call alone is not completion.

Readback verifies semantic placement and persistence. If the tool output cannot expose exact width, crop, visual balance or on-screen geometry, mark those aspects `UI_GEOMETRY_NOT_VERIFIED` rather than inferring them.

For Android/iOS/browser-visible image delivery, add a final client observation step. Server image readback proves persistence, not device rendering.

## Project workflow integration

During planning/review:

```text
read Project Home + Visual Bible + approved assets + implementation state
→ build only the visual inventory needed by that project
→ separate missing visual requirements from existing actual visuals
→ for each actual approved visual, record intended use + placement priority
→ if bytes require delivery, run DIRECT_NOTION_ATTACHMENT_OR_BLOCKED
→ update human surface when supported
→ read back
→ hand runtime-bound assets to repository implementation explicitly
```

During ordinary text-only planning, do not create visual records or placeholder images just to make the page look complete.

## Implementation Reality Gate

Before expanding automation beyond this contract:

1. read an existing page containing the target media/structure;
2. inspect current MCP/client tool exposure, not only workspace capability discovery;
3. require a callable function with usable schema for the intended operation;
4. perform one bounded real invocation;
5. fetch/read back the target;
6. classify exactly what was observable;
7. when client rendering matters, observe Android/iOS/browser separately;
8. if the required direct binary route is unavailable, use `BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT` rather than inventing a relay;
9. propose a new helper/tool only after repeated project evidence, Existing Solution First, long-term cost review and explicit user approval.

Do not build infrastructure for hypothetical layout limitations.

## Failure modes to reject

- treating text art direction as an actual approved image;
- claiming image semantic understanding from filename/caption alone;
- putting Prompt/Hash/AI notes on human Home by default;
- duplicating one approved visual into competing canonical records;
- redesigning the entire Home during bounded placement;
- claiming exact visual layout quality when only semantic block readback exists;
- treating `self.current_tool_access=available` as proof the current client can invoke the capability;
- treating a successful write invocation as durable effect without destination readback;
- treating server image readback as Android/browser render PASS;
- using Google Sheets as a temporary binary relay;
- introducing a new local binary helper because the direct connector path is unavailable;
- changing external hosts/CDNs repeatedly after a target client has reproduced a media failure without proving the actual failure boundary;
- introducing paid automation before current MCP behavior is tested;
- treating Notion placement as proof of Godot/runtime integration.

## Acceptance criteria

The workflow is healthy when:

- human Home remains concise and readable;
- AI/system metadata remains queryable without polluting human pages;
- every displayed project visual is traceable to an actual asset/reference and approval state;
- GPT can select a semantic destination from metadata without repeatedly asking where the asset belongs;
- visual-content-dependent judgements require direct image evidence;
- capability-dependent claims distinguish discovery, callable schema, invocation, readback and human-visible evidence;
- binary media uses a supported direct Notion-owned attachment path or explicitly blocks with `BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT`;
- no Google Sheet relay, local binary bridge or paid automation is silently introduced;
- all Notion writes receive destination readback;
- exact UI geometry is not overstated when the tool cannot verify it;
- repository runtime truth remains separate from Notion presentation state.
