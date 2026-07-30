# Visual Collaboration Tool Policy

Figma와 Whimsical은 기획·UX/UI·인계·검토를 돕는 `VISUAL_WORKSPACE`다. 어느 도구도 GitHub의 승인 결정·상세 규칙·구현 계약·실제 Godot 상태를 대체하지 않는다.

## Context and authority

각 Artifact는 `GDD`, `EXTERNAL_COLLABORATION`, `BOTH` 중 하나의 `usage_context`를 가진다. GDD 안에서는 사람이 흐름과 화면을 빠르게 확인하는 시각 구성요소이고, GDD 밖에서는 설계 탐색·협업·리뷰·인계의 독립 작업면이다. 둘 중 어느 쪽도 도구 사용을 강제하거나 활용 범위를 제한하지 않는다.

```text
GitHub Markdown·JSON + confirmed decisions → canonical rule and approval
Google Sheets → USER_FACING_GDD_WORKSPACE summary and editable review surface
Whimsical → loop, relation, branch, journey, system or work-flow visualization
Figma → screen, component, state, prototype, design-system and pinned handoff view
Godot + tests → actual implementation and validation evidence
```

시각 자료와 정본이 충돌하면 자동 덮어쓰지 않고 `VISUAL_CANONICAL_CONFLICT`로 기록하며 구현을 멈춘다.

## Tool choice

| Need | Prefer | Do not treat as |
| --- | --- | --- |
| core/session/meta loop, dependencies, narrative branches, AI/work process | Whimsical (or Mermaid for small static diagrams) | pixel-accurate UI or rule canon |
| screen hierarchy, component states, focus/input flow, responsive layout, prototype | Figma | game-rule canon or Godot completion evidence |
| compact status, link and user review | Google Sheets | a copy of every visual artifact |
| durable rule, decision, handoff contract | GitHub | a live design-file-only decision |

Do not create a `figma-*` or `whimsical-*` Skill merely because a connector exists. Extend the responsible planning, UX/UI, documentation, or handoff Skill. Use either tool independently when it solves the current problem; use both only when a confirmed structure must become a screen contract.

## Artifact lifecycle

`DRAFT_VISUAL → REVIEW_CANDIDATE → APPROVED_VISUAL_REFERENCE → IMPLEMENTATION_PINNED → VALIDATED → SUPERSEDED`

Auxiliary states are `AUTH_REQUIRED`, `ACCESS_DENIED`, `READ_ONLY`, `LINK_UNVERIFIED`, `SNAPSHOT_MISSING`, `SYNC_PENDING`, `VISUAL_CANONICAL_CONFLICT`, and `ARCHIVED`.

At `APPROVED_VISUAL_REFERENCE` or later, record a responsible document, Decision ID, scope/exclusion, last verification, replacement relation, and snapshot path or explicit reason. At `IMPLEMENTATION_PINNED`, also record page/board/frame/node, checked time, source commit, target platform/resolution/input, Godot handoff, and validation predicate.

## Access, safety and fallback

Never publish a private board, change ownership, or place secrets, credentials, private data, or internal keys in a visual workspace. Record public/private access and ownership separately. A link that cannot be read is not evidence of its contents.

If access is unavailable, use Markdown, Mermaid, a table, or a text wireframe; mark it as a fallback rather than an external artifact. `AVAILABLE`, `READ_ONLY`, `AUTH_REQUIRED`, `ACCESS_DENIED`, `UNAVAILABLE`, and `UNVERIFIED` describe capability—not completion.

## GDD and implementation handoff

Sheets hold a short Artifact ID, purpose, context, Decision ID, responsible source, status, link, snapshot, and next check. They do not copy full boards or frames. An implementation handoff uses a pinned Figma frame or a Whimsical structural reference plus a GitHub implementation contract; actual Godot render, input, accessibility, device, and human evidence remain independent and remain `NOT_RUN` until evidence exists.

## Adversarial review

Reject a change if it makes a visual tool a second canon, forces both tools, duplicates full content across tools, pins a live file without a snapshot, treats a prototype as runtime proof, silently bypasses access failure, or mixes project URL/token/design decisions into Base.
