# Notion ↔ GPT Visual Layout Contract

## Purpose

This contract defines the minimum reliable workflow for using GPT with the project Notion workspace so that approved visuals are placed in useful human-facing locations without turning the Home page into an AI metadata dump.

It extends `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`; it does not replace repository runtime truth or project-specific visual authority.

## Decision

Use the existing **Notion MCP + Visual Registry metadata + bounded Layout Contract + Human/AI surface separation**.

Do not add a second dashboard, dedicated visual-delivery tool, or paid automation service by default.

### Alternatives considered

1. **Free-form GPT page redesign** — rejected as the default. It maximizes apparent flexibility but causes layout drift, weak repeatability, and accidental exposure of system metadata.
2. **External automation layer (Zapier/Make/custom service)** — defer. It can automate triggers but adds cost, another failure surface, and little value until MCP capability gaps are demonstrated by a real workflow.
3. **Notion MCP + bounded placement contract** — adopted. It reuses the current project workspace, preserves human-readable Notion, keeps repository runtime authority separate, and can be strengthened incrementally when a real limitation is observed.

Reconsider option 2 only when repeated manual placement or unsupported Notion operations create measured workflow cost that the MCP path cannot remove.

## Capability ceiling

`NOTION_TEXT_AND_STRUCTURE_READABLE != NOTION_IMAGE_SEMANTICS_VERIFIED`

`NOTION_BLOCK_WRITABLE != PIXEL_LAYOUT_CONTROLLED`

GPT must distinguish three kinds of evidence:

- **Structured page evidence**: page text, headings, properties, database records, image/file block references and surrounding context that the current Notion connection actually returns.
- **Visual evidence**: the image pixels were supplied to or otherwise directly inspected by a vision-capable path in the current task.
- **UI-layout evidence**: the resulting Notion page or block arrangement was read back through a representation that exposes the relevant columns/blocks, or manually verified by the user when visual geometry is not observable through the tool.

Never claim that GPT understood the visual content of an image merely because an image block, file name, caption or metadata is present.

The legacy/read-only ChatGPT Notion search connector does not index non-document media such as images and videos. Notion MCP can read and write workspace pages, but image semantic inspection still requires direct visual evidence when the decision depends on the pixels.

## Human and AI surfaces

`HUMAN_HOME_IS_NOT_AI_CONTEXT_DUMP`

Human-facing project surfaces prioritize comprehension and decision usefulness:

- Project Home
- Visual Bible
- human-facing Asset/Reference gallery
- approved Visual Map / Flow
- current focus, important decisions and links

AI/system surfaces retain processing metadata that is useful to automation but noisy to people:

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

Before inserting or moving a visual, GPT applies this sequence:

```text
identify project
→ identify record type and approval state
→ determine whether the visual is useful to a human reader
→ determine semantic destination
→ check for an existing canonical instance
→ choose prominence from intended use / placement priority
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

- Prefer semantic proximity over decorative symmetry: a visual belongs next to the explanation it helps a person understand.
- Use two-column arrangements only when the Notion tool representation can create/preserve columns reliably and the pair is genuinely comparative or mutually explanatory.
- Do not create dense mosaics merely to use empty space.
- Do not move unrelated sections to make room for an image.
- Avoid duplicated canonical images. Reuse the same canonical record or link when possible.
- A generated Visual Map is derived presentation. Structured Screen/Flow records remain authoritative when the rendered map disagrees.
- Pixel-level width, crop, mask and exact visual balance are manual/UI-level refinements unless the active tool path exposes and verifies them.

## Image understanding gate

When placement depends only on known metadata and approved intended use, GPT may place the visual without re-inspecting pixels.

When the decision depends on actual visual content — composition, readability, character identity, UI hierarchy, contrast, cropping, visual similarity or whether the image matches a description — require direct visual evidence.

```text
METADATA_ONLY
→ semantic placement allowed when intended use is already approved
→ no claim about pixel content

DIRECT_VISUAL_EVIDENCE
→ semantic + visual-quality judgement allowed within observed scope

NO_DIRECT_VISUAL_EVIDENCE + visual-content-dependent decision
→ BLOCKED_UNVERIFIED for that judgement
```

Do not generate a missing image merely to satisfy this gate. Image generation remains subject to the user's explicit generation instruction and project policy.

## Delivery and readback

Every Notion write that changes durable visual organization follows:

```text
read current destination
→ smallest bounded edit
→ write
→ fetch/read back
→ verify expected block/record and surrounding section
```

A successful write call alone is not completion.

Readback verifies semantic placement and persistence. If the tool output cannot expose exact width, crop, visual balance or on-screen geometry, mark those aspects `UI_GEOMETRY_NOT_VERIFIED` rather than inferring them.

## Project workflow integration

During project planning/review:

```text
read project Home + Visual Bible + approved assets + implementation state
→ build only the visual inventory needed by that project
→ separate missing visual requirements from existing actual visuals
→ for each actual approved visual, record intended use + placement priority
→ update human surface through this contract
→ read back
→ hand runtime-bound assets to repository implementation explicitly
```

During ordinary text-only planning, do not create visual records or placeholder images just to make the page look complete.

## Implementation Reality Gate

Before expanding automation beyond this contract, demonstrate the specific missing capability with a real project example.

Required probe order:

1. read an existing page that contains image/file blocks and surrounding sections;
2. perform one bounded placement/edit using current Notion MCP capabilities;
3. fetch/read back the target;
4. classify what was actually observable: block presence, order, columns, caption, file reference, or only text context;
5. add a helper/tool only for a repeatable capability gap that materially affects the workflow.

Do not build infrastructure for hypothetical layout limitations.

## Failure modes to reject

- treating a text art direction as an actual approved image;
- claiming image semantic understanding from a filename/caption alone;
- putting Prompt/Hash/AI notes on the human Home by default;
- duplicating the same approved visual into competing canonical records;
- redesigning the entire Home during a bounded asset placement task;
- claiming exact visual layout quality when only semantic block readback was available;
- introducing a paid automation layer before current MCP behavior was tested;
- treating Notion placement as proof that Godot/runtime integration occurred.

## Acceptance criteria

The workflow is healthy when:

- human Home remains concise and readable;
- AI/system metadata remains queryable without polluting the human page;
- every displayed project visual is traceable to an actual asset/reference and approval state;
- GPT can select a semantic destination from metadata without repeatedly asking where the asset belongs;
- visual-content-dependent judgements require direct image evidence;
- all Notion writes receive destination readback;
- exact UI geometry is not overstated when the tool cannot verify it;
- repository runtime truth remains separate from Notion presentation state.
