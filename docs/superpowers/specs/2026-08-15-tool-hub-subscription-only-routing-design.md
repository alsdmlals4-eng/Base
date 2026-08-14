# Base Tool Hub Subscription-Only and Tool-Node Routing Design

Issue: #393

## Goal

Base Tool Hub의 실제 사용자 경로를 추가 결제 없는 `ChatGPT Pro + Figma Pro + local runtime + GitHub/Godot` 조합으로 고정하고, Figma 이미지 결과를 프로젝트별 일반 Generated Assets뿐 아니라 검증된 도구별 하위 노드로 정확히 라우팅할 수 있게 한다.

## Hard constraints

- OpenAI API/pay-as-you-go/prepaid 호출은 사용자 production Golden Path에서 금지한다.
- ChatGPT Pro를 비공개 API, 쿠키, DOM scraping, 브라우저 자동 로그인으로 우회 호출하지 않는다.
- 기존 `subscription_handoff_import`를 production handoff boundary로 재사용한다.
- 진행 중 PR #373, #376, #386의 파일은 수정하지 않는다.
- Figma 목적지는 사용자 입력이나 런타임 layer-name 검색으로 결정하지 않는다.
- 실제 존재가 확인된 node만 Base registry에 pin한다.

## Architecture

### 1. Subscription handoff contract

공용 계약 계층에 `SubscriptionHandoffPacket`을 둔다. 이 객체는 생성 자체를 수행하지 않는다. 다음만 고정한다.

- `project_id`, `tool_id`, `run_id`
- `generation_surface = CHATGPT_PRO`
- `run_mode = subscription_handoff_import`
- 승인 anchor/reference 설명
- 요청 작업 설명
- 기대 출력 개수와 PNG 요구
- review checklist
- 금지 항목: API key, provider secret, arbitrary local path, Figma target override

Tool Hub/Studio는 이후 이 계약을 UI용 packet으로 직렬화하고 ChatGPT Pro에서 생성된 실제 결과를 같은 run으로 import한다.

### 2. Tool-specific Figma destinations

기존 `ProjectFigmaTarget.generation_area_node_id`는 fallback/root destination으로 유지한다. 각 registry entry에 선택적 `tool_destinations` map을 추가한다.

초기 canonical route:

- `expression-studio` -> live-inspected `Expression Runs` node

`sprite-animation-studio`는 전용 action/effect node가 아직 검증되지 않았으므로 기존 `generation_area_node_id`를 사용한다.

`ProjectFigmaTarget.node_for_tool(tool_id)`는 exact reviewed mapping이 있으면 그 node를 반환하고, 없으면 generation area fallback을 반환한다. 브라우저나 Figma plugin이 arbitrary node ID를 주입할 수 없다.

## Live Figma evidence — 2026-08-15

Expression Runs node IDs:

- coc-fiction: `15:2`
- ten-paces-hidden-moves: `28:2`
- ninja-survival: `15:2`
- switchy-express-cargo-puzzle: `14:2`
- urban-legend: `14:2`
- grimoire-how-to-rewrite-the-world: `11:2`
- blacksmith: `18:2`
- omenward: `13:2`

All eight were inspected under `Sprite Animation Studio -> Generated Assets -> Expression Runs` and each file contains a hidden `Base Tool Hub Route · <project_id>` marker.

## Compatibility

- Registry remains `version: 1` with an additive optional field; existing entries without `tool_destinations` remain valid.
- `resolve_ready_target(project_id)` remains source-compatible.
- PR #376 can continue using `generation_area_node_id` until a merged follow-up switches enqueue/finalize to `node_for_tool(tool_id)`.
- No tool source, Windows supervisor, Figma Bridge implementation, or Character Studio implementation changes in this slice.

## IRG

This slice may prove only:

- subscription handoff packet is deterministic, project/run scoped and secret-free;
- paid API route is not required by this contract;
- all eight Expression destination IDs are loadable from the canonical registry;
- unknown tools fall back to the reviewed generation area.

It does not prove ChatGPT Pro UI generation, Figma plugin delivery, Windows Studio runtime, character identity quality, sprite generation, or real project consumption.

## Rollback

Revert the contract PR. Existing generic generation-area routing remains intact and no Figma/project data migration is required.
