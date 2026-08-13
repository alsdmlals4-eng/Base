# Project GPT · Expression Studio Figma Delivery

Use this procedure only after the **matching project GPT workspace** has received an Expression Studio `ready_for_project_gpt` packet and has the selected PNG at the listed local project-relative path.

## Required checks

1. Read the current `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json` from the adopted Base revision.
2. Verify the packet `project_id` equals the active project's canonical ID. Never infer a target by display name.
3. Verify `delivery_status` is exactly `READY_FOR_DELIVERY`.
4. Verify the packet's `figma_file_key` equals the Figma URL `/design/<file-key>/` segment.
5. Verify `delivery_page_node_id` and `generation_area_node_id` exist in that exact Figma file.
6. Verify `selected_expression`, `contact_sheet`, `lineage`, and `manifest` files are available under the current project workspace.

Stop and report the failed check if any check fails. Do not use another project's destination as a fallback.

## Safe Figma placement

1. Open only the packet's exact Figma file and resolve the verified `Sprite Animation Studio` page and `Generated Assets` area by node ID.
2. Resolve the `Expression Runs` section inside that area. If it is absent, create only that section; do not move or replace existing generation sections.
3. Add a new run subsection named with the packet `run_id`. It must contain the selected expression PNG, an optional contact sheet, and text metadata: approved-anchor URL, requested/resolved controls (including A–E intensity and character-anatomical left/right for `AU46`), preset, source SHA-256, and local manifest path.
4. Keep Figma content editable and preserve earlier run sections; **do not replace** an existing result, original asset, or another run section.
5. Return the exact Figma subsection URL, the visual files placed, text-only metadata, and any unverified condition.

## Never do

- Do not mutate a target whose state is not `READY_FOR_DELIVERY`.
- Do not route to a different project, use a ZIP as handoff, store credentials, or claim that a local packet uploaded anything.
- Do not claim Figma placement validates model fidelity, licensing, Godot import, animation, or player acceptance.
