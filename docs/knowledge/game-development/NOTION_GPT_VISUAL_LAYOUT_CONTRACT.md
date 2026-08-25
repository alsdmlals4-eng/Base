# Notion ↔ GPT Visual Layout Contract

## Purpose

This contract defines the minimum reliable workflow for using GPT with the project Notion workspace so that approved visuals are placed in useful human-facing locations without turning the Home page into an AI metadata dump.

It extends `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`; it does not replace repository runtime truth or project-specific visual authority. Human Home content density follows `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`: the Home may be information-rich when Flow, systems, project-specific core data, visuals, or edit guidance materially improve human understanding.

For current Notion page/database/view/data-source/layout/media/permission/Agent semantics, also apply `docs/knowledge/methods/NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md`. That reference supplies product-behavior boundaries; this file remains the visual placement/evidence workflow owner.

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

`MCP_DISCOVERED_AVAILABLE != CURRENT_CLIENT_EXECUTABLE`

`CURRENT_CLIENT_EXECUTABLE != EFFECT_VERIFIED`

`SERVER_READBACK_PASS != HUMAN_VISIBLE_DEVICE_PASS`

GPT must distinguish three kinds of evidence:

- **Structured page evidence**: page text, headings, properties, database records, image/file block references and surrounding context that the current Notion connection actually returns.
- **Visual evidence**: the image pixels were supplied to or otherwise directly inspected by a vision-capable path in the current task.
- **UI-layout evidence**: the resulting Notion page or block arrangement was read back through a representation that exposes the relevant columns/blocks, or manually verified by the user when visual geometry is not observable through the tool.

Never claim that GPT understood the visual content of an image merely because an image block, file name, caption or metadata is present.

The legacy/read-only ChatGPT Notion search connector does not index non-document media such as images and videos. Notion MCP can read and write workspace pages, but image semantic inspection still requires direct visual evidence when the decision depends on the pixels.

### MCP capability evidence

Notion workspace/self capability discovery is a routing hint, not completion evidence. If a capability is reported as `available` but the current ChatGPT client does not expose a callable function with the required input schema, classify it as `DISCOVERED_ONLY / BLOCKED_TOOL_SURFACE` rather than executable.

For capability-dependent work, apply the shared `claim-and-intent-verification` Reality Gate:

```text
capability discovery
→ callable function + usable schema
→ minimum real invocation
→ durable destination readback when applicable
→ human/device-visible observation when the claim depends on rendering
```

A successful API/write call is at most `INVOCATION_PASS`; a durable page change requires `READBACK_PASS`. Android/browser rendering becomes `HUMAN_VISIBLE_PASS` only after that client is actually observed. Server-side image block readback never substitutes for the device-visible rendering claim.

### Binary media delivery routing

Notion MCP remains the default owner for text, page structure, databases, semantic placement and ordinary readback. A separate local path is allowed only for a **proven binary-media capability gap** where the target operation requires the official typed `file_upload` representation and the current client cannot preserve it.

Current routing:

```text
Notion text / structure / database / semantic layout
→ Notion MCP

binary media
→ current MCP exposes usable typed `file_upload` attach + real invocation/readback succeeds
  → use MCP
→ otherwise
  → Notion Native File Bridge
  → official `ntn files create`
  → typed `file_upload` attach through `ntn api`
  → destination readback

client-visible claim
→ actual Android / iOS / browser observation
→ only then HUMAN_VISIBLE_PASS
```

The local **Notion Native File Bridge** is not a second Notion workspace or automation authority. It is a narrow transport adapter around Notion's official `ntn` CLI for local binary upload and typed attachment only. OAuth/keychain handling remains owned by the official CLI; no Notion token is committed to Base or project repositories.

If a target client has already reproduced `422` or broken-image behavior for external media, changing from one external host/CDN to another is not an acceptable substitute for typed `file_upload`. A GitHub raw URL, jsDelivr URL, temporary signed URL, status text, filename, empty Gallery card or server-only image readback cannot be promoted to Android-visible success.

When the ChatGPT Notion connector later exposes and verifies typed `file_upload` attachment directly, prefer the connector-native path and retire the local bridge rather than maintaining duplicate infrastructure.

### Official file-limit conflict guard

`NOTION_FILE_LIMIT_CLAIM_CONFLICT_GUARD`

As checked on 2026-08-25, Notion's official `Images, files & media` help page simultaneously presents a conservative paid-plan note (`PDF <20MB`, `PNG/JPG <5MB`) and an FAQ statement that paid plans allow files up to `5GB`. Do not collapse those different statements into one universal render/upload ceiling.

Use this operational distinction:

```text
INLINE_IMAGE_DISPLAY_SAFE_TARGET
→ human-visible PNG/JPG preview: conservatively target <=5MB

SOURCE_MASTER_OR_LARGE_FILE
→ use the currently supported file/API route
→ upload status
→ typed attach
→ destination readback
→ actual client observation when rendering is claimed
```

A large file being accepted by storage/API is not proof that the same bytes will render reliably as an inline image on every client.

### Preview/master separation

`NOTION_PREVIEW_MASTER_SEPARATION`

When an approved image must remain high resolution, preserve the source master rather than overwriting it merely to satisfy a human-facing preview limit.

```text
DISPLAY_PREVIEW
→ optimized for Home/Gallery/inline viewing
→ can be resized/compressed for reliable display

SOURCE_MASTER
→ approved high-resolution source
→ retained as file/Files & media/verified typed upload as appropriate
→ version/provenance retained
```

Preview delivery is not source-master verification and is not runtime integration evidence.

## Human and AI surfaces

`HUMAN_HOME_IS_NOT_AI_CONTEXT_DUMP`

Human-facing project surfaces prioritize comprehension and decision usefulness:

- Project Home
- Visual Bible
- human-facing Asset/Reference gallery
- approved Visual Map / Flow
- project-specific human-readable core data
- AI interpretation of design intent for user correction
- user edit guidance
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

### Gallery preview source

`NOTION_GALLERY_EXPLICIT_MEDIA_PREVIEW`

For a Visual Bible or Asset catalog where image identity is important, prefer an explicit approved `Files & media` property as the Gallery card preview source when the active schema supports it.

Notion also supports `Page cover` and `Page content` previews. Use them intentionally:

- `Page cover`: valid when the cover itself is the canonical presentation for that record.
- `Page content`: acceptable for lightweight notes, but the preview can drift when the first page block changes.
- `Files & media`: preferred for a stable approved asset/reference card whose preview identity should not depend on page-body order.

Use `Fit image` when the full composition must remain visible; allow crop/reposition only when the intended thumbnail/hero use benefits from cropping. A cropped card preview never replaces the full approved asset.

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

Do not promote every approved image to Home. Home is an information-rich learning surface, not the asset archive.

## Layout grammar

Notion supports image blocks, media alignment and columns. Use these features conservatively through the current Notion representation.

Default human layout:

```text
Project title
Hero visual when a true HERO exists
one-line project promise / current focus

Core experience / Flow
Primary visual(s) adjacent to the matching explanation

Core systems / project-specific core data / world / UX
Supporting approved visuals near their owning section

AI-understood design intent / how to edit
Current state / decisions / important links
```

Rules:

- Prefer semantic proximity over decorative symmetry: a visual belongs next to the explanation it helps a person understand.
- Use two-column arrangements only when the Notion tool representation can create/preserve columns reliably and the pair is genuinely comparative or mutually explanatory.
- `NOTION_MOBILE_STACK_SEMANTIC_ORDER_REQUIRED`: phone clients do not preserve desktop multi-column geometry; right-column content stacks below left-column content. Design the source order so the page remains understandable as one vertical stream. Do not hide a required premise, warning or conclusion only in a right-hand column.
- `NOTION_DATABASE_GLOBAL_LAYOUT_IMPACT_GATE`: database page layout applies across the database, not to one record/view. Do not use `Customize layout` for a bounded single-record polish request; use local page body/record-property edits unless a database-wide redesign is explicitly intended and its affected record family has been checked.
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

## Image generation conversation gate

When the task actually asks to generate or edit a project image, apply `IMAGE_CONVERSATION_APPROVAL_GATE.md` at `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`.

The minimum conversation contract is:

```text
project/visual canon review
→ text brief
→ TEXT_BRIEF_STOP_REQUIRED

next user message
→ explicit image approval
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

Do not call image generation in the same assistant turn that first presents the text brief. Do not automatically chain the next image, pose, asset, UI variant, or decomposition step after generation.

This conversation gate does not replace `Visual Requirement Gate`, candidate review, project approval, Notion delivery/readback, or runtime integration evidence.

## Delivery and readback

Every Notion write that changes durable visual organization follows:

```text
read current destination
→ classify page/view/source/layout/file impact
→ smallest bounded edit
→ write
→ fetch/read back
→ verify expected block/record and surrounding section
```

A successful write call alone is not completion.

Readback verifies semantic placement and persistence. If the tool output cannot expose exact width, crop, visual balance or on-screen geometry, mark those aspects `UI_GEOMETRY_NOT_VERIFIED` rather than inferring them.

For file/image delivery, preserve `upload → status=uploaded → typed attach → destination readback` as separate evidence when the active route exposes those stages. Upload success alone is not attachment success.

For Android/iOS/browser-visible image delivery, add a final client observation step. A Notion server image block, signed file URL, or successful page fetch can prove persistence but cannot prove that a specific client actually rendered the bytes.

## Project workflow integration

During project planning/review:

```text
read project Home + Visual Bible + approved assets + implementation state
→ build only the visual inventory needed by that project
→ separate missing visual requirements from existing actual visuals
→ for each actual approved visual, record intended use + placement priority
→ choose explicit Gallery preview source when stable asset identity matters
→ preserve source master when a smaller display preview is needed
→ update human surface through this contract
→ read back
→ hand runtime-bound assets to repository implementation explicitly
```

During ordinary text-only planning, do not create visual records or placeholder images just to make the page look complete.

## Implementation Reality Gate

Before expanding automation beyond this contract, demonstrate the specific missing capability with a real project example.

Required probe order:

1. read an existing page that contains image/file blocks and surrounding sections;
2. inspect current MCP/client tool exposure, not only workspace capability discovery;
3. require a callable function with usable schema for the intended operation;
4. perform one bounded real invocation using current Notion MCP capabilities;
5. fetch/read back the target;
6. classify what was actually observable: block presence, order, columns, caption, file reference, or only text context;
7. when client rendering matters, observe that Android/iOS/browser surface separately;
8. add a helper/tool only for a repeatable capability gap that materially affects the workflow.

Do not build infrastructure for hypothetical layout limitations.

## Failure modes to reject

- treating a text art direction as an actual approved image;
- generating an image in the same assistant turn that first defines the project image brief;
- chaining multiple project images without the required user checkpoint;
- claiming image semantic understanding from a filename/caption alone;
- putting Prompt/Hash/AI notes on the human Home by default;
- duplicating the same approved visual into competing canonical records;
- redesigning the entire Home during a bounded asset placement task;
- editing a linked data source record/property while reporting only a local view-presentation change;
- changing a database-global page layout to polish one record;
- designing a critical Home comparison that becomes semantically broken when mobile stacks the right column below the left;
- relying on `Page content` as a stable Visual Bible card identity without accepting first-block preview drift;
- treating one of Notion's currently conflicting `5MB`/`5GB` official statements as a universal upload-and-render cap for every file path;
- overwriting a high-resolution approved master only to meet a smaller display-preview target;
- claiming exact visual layout quality when only semantic block readback was available;
- treating `self.current_tool_access=available` as proof that the current client can invoke the capability;
- treating a successful write invocation as durable effect without destination readback;
- treating a file-upload object as delivered before typed attachment and target readback;
- treating server image readback as Android/browser render PASS;
- using a different external CDN as a hidden workaround after the target client has reproduced media 422;
- treating Notion Native File Bridge readback as `HUMAN_VISIBLE_PASS` without actual client observation;
- introducing a paid automation layer before current MCP behavior was tested;
- treating Notion placement as proof that Godot/runtime integration occurred.

## Acceptance criteria

The workflow is healthy when:

- human Home is information-rich where needed while remaining readable and responsibility-separated;
- AI/system metadata remains queryable without polluting the human page;
- every displayed project visual is traceable to an actual asset/reference and approval state;
- GPT can select a semantic destination from metadata without repeatedly asking where the asset belongs;
- database/view/source/global-layout impact is classified before non-trivial Notion writes;
- desktop column use preserves a coherent mobile one-column reading order;
- stable Visual Bible/Asset cards use an intentional preview source rather than accidental first-block drift;
- high-resolution source masters are preserved separately when a smaller human-visible preview is needed;
- image generation/editing obeys `TEXT_BRIEF_STOP_REQUIRED` and `GENERATE_EXACTLY_ONE` through the image conversation gate;
- visual-content-dependent judgements require direct image evidence;
- capability-dependent claims distinguish discovery, callable schema, invocation, readback and human-visible evidence;
- binary media uses a verified typed `file_upload` path instead of known-broken external delivery when client rendering matters;
- official file-size conflicts are treated as a freshness/capability probe problem rather than one universal hard cap;
- all Notion writes receive destination readback;
- exact UI geometry is not overstated when the tool cannot verify it;
- repository runtime truth remains separate from Notion presentation state.
