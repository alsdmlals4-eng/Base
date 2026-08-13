# Project GPT · Sprite Animation Figma Delivery

Use this action only after a visual result has been generated or curated in the **same project GPT workspace**. The Base browser can prepare a `ready_for_project_gpt` packet; it does not upload assets to Figma itself.

## Required inputs

- Active `project_id`, approved animation mode, and the selected output files from the current workspace.
- Approved anchor Figma node URL and selected frame order.
- `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json` from the adopted Base revision.
- A Figma connector with edit permission for the exact resolved file.

## Guarded delivery procedure

1. Resolve only the active `project_id` in the registry. Do not infer a target from a project name or use a fallback project.
2. Stop if the entry is missing, the file key conflicts, image bytes are unavailable, the anchor is not approved, or selected outputs are incomplete.
3. Stop without calling the Figma tool when `delivery_status` is `REGISTERED_NO_MUTATION`, `ARCHIVED`, or any value other than `READY_FOR_DELIVERY`.
4. With a ready target, use the Figma 도구 in that exact file. Resolve or create `Sprite Animation Studio` and its `Generated Assets` area according to the registry defaults.
5. Add a **새 실행 섹션** named with the run ID, mode, action, frame count, FPS, approved-anchor URL, and generation time. Do not overwrite or delete a prior approved section.
6. Upload/place only the visual deliverables selected for this run. Keep manifest/Godot data as text metadata when helpful; do not claim it was imported or runtime-tested.
7. Return the exact new Figma section URL, the files placed, metadata-only items, and any unavailable validation. If Figma placement fails, report the failure and preserve the local run for retry.

## Never do

- Do not use ZIP download/upload as a normal handoff.
- Do not store Figma API tokens, cookies, or image bytes in Base or Git.
- Do not mutate a `REGISTERED_NO_MUTATION` project, route to another project, or silently replace an existing generation section.
- Do not claim Figma placement proves licensing, Godot import, animation runtime, or user acceptance.
