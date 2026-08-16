# Expression Studio · Tool Hub Figma Bridge Delivery

> `project-gpt-figma-delivery.md`는 이전 파일명 호환을 위해 남아 있습니다. 현재 canonical delivery owner는 **Base Tool Hub + Figma Bridge**이며, `ready_for_project_gpt` packet을 사람이 수동으로 Figma에 배치하는 절차는 더 이상 사용하지 않습니다.

## Required checks

1. Expression Studio가 Tool Hub가 시작한 인증된 `expression-studio` child인지 확인합니다.
2. 현재 project ID는 Tool Hub의 immutable child identity와 `PROJECT_FIGMA_TARGET_REGISTRY.json`의 project binding에서만 가져옵니다. 브라우저 입력이나 display name으로 추론하지 않습니다.
3. `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`에서 `(project_id, character_expression_runs)`가 `READY_FOR_DELIVERY`인지 확인합니다.
4. route의 `figma_file_key`, parent `Generated Assets`, exact destination `Expression Runs`, hidden project marker가 현재 project target과 일치하는지 재검증합니다.
5. `확정 및 전달` 직전 selected PNG를 다시 읽어 export에 기록된 SHA-256과 동일한지 검증합니다.
6. 같은 `(tool_id, project_id, run_id, route, SHA-256)` delivery는 idempotent하게 재사용합니다. route가 달라지거나 bytes가 바뀌면 fail-closed합니다.

어느 검사든 실패하면 전달을 중단합니다. 다른 project, generic `Generated Assets`, Sprite/Effect destination을 fallback으로 사용하지 않습니다.

## Canonical Figma placement

1. Studio는 selected PNG bytes만 child-only localhost credential로 부모 Tool Hub에 전달합니다. 브라우저는 Figma file key, node ID, route를 전달 권한으로 제출하지 않습니다.
2. Tool Hub가 exact `character_expression_runs` route를 resolve한 뒤 queue job의 첫 authoritative `JOB.json` 쓰기부터 route identity와 content SHA를 함께 고정합니다.
3. Figma Bridge plugin은 paired project의 job만 claim하고 exact `Expression Runs` target에 같은 bytes를 배치합니다.
4. receipt의 target node, content SHA, bridge version, created node identity, image hash가 모두 일치해야 `DELIVERED_VERIFIED`가 됩니다.
5. 기존 Expression 결과, 승인 원본, Sprite Action Runs, Effect Runs 또는 다른 run을 이동·교체하지 않습니다.

## Never do

- `ready_for_project_gpt` packet, matching project GPT workspace, 수동 Figma node 선택을 canonical delivery로 사용하지 않습니다.
- `generation_area_node_id` 자체를 Expression destination으로 사용하지 않습니다.
- Expression child가 `sprite_action_runs`나 `effect_runs`를 요청하도록 허용하지 않습니다.
- local queue 생성, Figma 창 열림, pairing 완료만으로 실제 Figma placement를 `VERIFIED`라고 주장하지 않습니다.
- Figma placement를 model fidelity, licensing, Godot import, animation, player acceptance 검증으로 확대 해석하지 않습니다.
