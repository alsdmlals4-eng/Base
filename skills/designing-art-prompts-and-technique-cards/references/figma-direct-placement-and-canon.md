# Figma Direct Placement and Canon Module

Use this reference when a visual task is already routed through `designing-art-prompts-and-technique-cards` and the project has a configured Figma Visual Bible.

## Contract name

`FIGMA_DIRECT_VISUAL_ORGANIZATION`

The normal image-work path is:

```text
project canon / Decisions
→ actual Figma approved references
→ generate or edit
→ review candidate
→ place in Figma WIP when possible
→ user review
→ approved visual organization only after explicit user approval
→ separate product-asset/runtime lifecycle when needed
```

## Before generation

1. Resolve the project Figma file from project-owned configuration or Visual Artifact Registry.
2. Read the relevant `01_APPROVED_REFERENCE` node(s) if accessible.
3. Extract `Keep / Avoid / Do Not Drift` rather than copying the reference surface.
4. Check reusable references first:
   - `01.10_REUSABLE_COMPONENTS`
   - `01.11_STRUCTURE_PATTERNS`
   - `01.12_VISUAL_DNA`
5. Do not treat `02_WIP`, `03_REJECTED`, or old screenshots as approved canon.

## Placement branch

### `FIGMA_WRITE_AVAILABLE`

When GPT has an authenticated Figma write capability for the exact project file:

```text
new visual candidate
→ AUTO_PLACE_WIP
→ 02_WIP / most relevant existing section
→ stable artifact/frame name
→ optional WIP/review annotation
→ Figma readback
→ report placement only after readback
```

`AUTO_PLACE_WIP` is an execution convenience, not approval.

Recommended initial status:

```yaml
visual_status: DRAFT_VISUAL | REVIEW_CANDIDATE
product_asset_status: NOT_APPROVED
```

After **explicit user approval**:

- move/reorganize or copy the approved visual into the appropriate `01_APPROVED_REFERENCE` section;
- use `04_FINAL` when it is a visually final-use expression;
- preserve stable IDs/node links where practical;
- read back the destination before claiming success.

### `FIGMA_WRITE_UNAVAILABLE`

Do not give vague advice such as “put it in Figma later.” Return `EXACT_PLACEMENT_GUIDANCE`:

```yaml
project_figma_file:
page: 02_WIP
section:
artifact_name:
visual_status: DRAFT_VISUAL | REVIEW_CANDIDATE
comparison_reference_ids: []
placement_reason:
next_gate: USER_REVIEW
promotion_after_approval:
  approved_reference_section:
  final_section_if_applicable: 04_FINAL
```

If the exact project file/page/section cannot be verified, mark that field `UNVERIFIED` instead of inventing it.

## Naming

Reuse the project's stable prefixes from `FIGMA_VISUAL_BIBLE_PROFILE.md`, such as `CHAR_`, `ENV_`, `UI_`, `ICON_`, `VFX_`, and `MKT_`.

Candidate suffixes may use `_A`, `_B`, `_v01`, etc. Approval should preserve the stable base identity and record supersession rather than silently replacing history.

## Approval boundary

Figma states remain separate from product states.

```text
DRAFT_VISUAL / REVIEW_CANDIDATE
→ explicit user approval
→ APPROVED_VISUAL_REFERENCE and/or 04_FINAL organization
```

This does **not** automatically grant:

- `PROJECT_ASSET_APPROVED`;
- tracked product asset status;
- rights/license approval;
- Asset Vault `promote`;
- Godot implementation;
- runtime/human validation.

## Readback rule

A successful Figma write call is not sufficient evidence by itself. Re-read the created/moved node or destination metadata and verify the expected project, page/section, name, and state before reporting placement success.
