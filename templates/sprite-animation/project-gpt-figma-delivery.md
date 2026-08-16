# Sprite Animation Studio · Tool Hub Figma Bridge Delivery

> `project-gpt-figma-delivery.md`는 이전 파일명 호환을 위해 남아 있습니다. 현재 canonical delivery owner는 **Base Tool Hub + Figma Bridge**이며, `ready_for_project_gpt` packet을 사람이 수동으로 Figma에 배치하는 절차는 더 이상 사용하지 않습니다.

## Required checks

1. Sprite Animation Studio가 Tool Hub가 시작한 인증된 `sprite-animation-studio` child인지 확인합니다.
2. active `project_id`는 Tool Hub의 immutable child identity와 `PROJECT_FIGMA_TARGET_REGISTRY.json`에서만 가져옵니다. 브라우저나 display name으로 target을 정하지 않습니다.
3. 서버에 저장된 `RunRecord.request.mode`에서 route를 결정합니다.
   - `pose_sequence` / `sprite_action` → `sprite_action_runs` → `Sprite Action Runs`
   - `effect_stages` → `effect_runs` → `Effect Runs`
   - `expression_variation` → `DELIVERY_TOOL_ROUTE_UNAVAILABLE`
4. `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`에서 해당 `(project_id, route_id)`가 `READY_FOR_DELIVERY`이며 exact file/parent/destination/marker가 project target과 일치하는지 검증합니다.
5. export manifest와 `record.export_output_sha256["atlas"]`을 다시 확인하고 exact exported atlas PNG bytes의 SHA-256이 일치해야 합니다.
6. 같은 `(tool_id, project_id, run_id, route, atlas SHA-256)` delivery만 idempotent하게 재사용합니다. route 변경은 `DELIVERY_RUN_ROUTE_MISMATCH`, bytes 변경은 `DELIVERY_RUN_CONTENT_MISMATCH`로 차단합니다.

검사 실패 시 다른 project, generic `Generated Assets`, Character용 `Expression Runs`로 fallback하지 않습니다.

## Canonical Figma placement

1. Studio는 검증된 atlas PNG bytes만 child-only localhost credential로 부모 Tool Hub에 전달합니다. 브라우저는 Figma file key, node ID, route를 전달 권한으로 제출하지 않습니다.
2. Tool Hub는 exact reviewed route를 resolve하고 첫 authoritative `JOB.json` 쓰기부터 route identity와 content SHA를 함께 고정합니다.
3. Figma Bridge plugin은 paired project의 job만 claim하고 exact `Sprite Action Runs` 또는 `Effect Runs` target에 같은 bytes를 배치합니다.
4. receipt의 target node, content SHA, bridge version, created node identity, image hash가 모두 일치해야 `DELIVERED_VERIFIED`가 됩니다.
5. 기존 승인 결과, Expression Runs, 다른 run section, 원본 asset을 이동·교체하지 않습니다.

## Never do

- `ready_for_project_gpt` packet, same project GPT workspace, 수동 Figma node 선택을 canonical delivery로 사용하지 않습니다.
- `generation_area_node_id` 자체를 Sprite/Effect destination으로 사용하지 않습니다.
- Sprite child가 `character_expression_runs`를 요청하도록 허용하지 않습니다.
- local queue 생성, Figma 창 열림, pairing 완료만으로 실제 Figma placement를 `VERIFIED`라고 주장하지 않습니다.
- Figma placement를 licensing, Godot import, animation runtime, player acceptance 검증으로 확대 해석하지 않습니다.
