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

## Project Visual Flow Workspace

프로젝트가 Figma 또는 동등한 시각 작업면을 사용하는 경우 이를 `Project Visual Flow Workspace`로 취급할 수 있다. 목적은 이미지를 모으는 데 있지 않고 **기획 화면 → 해석 기록 → 화면 흐름/Prototype → 승인 → 실제 구현 캡처 → 비교 검증**을 한 작업면에서 연결하는 데 있다.

권장 Artifact 유형은 다음과 같다.

- `FLOW_MAP`: 게임 전체 또는 한 기능의 화면 이동 지도.
- `SCREEN_CONCEPT`: AI 생성 또는 수동 제작한 개념 화면.
- `SCREEN_WIREFRAME`: 구조·정보 위계를 편집 가능한 레이어로 정리한 화면.
- `PROTOTYPE_FLOW`: 클릭·전환·복귀·상태 변화 검토용 흐름.
- `RUNTIME_CAPTURE`: 실제 Godot/Web 구현 캡처.
- `COMPARE_BOARD`: 승인 시각 참조와 구현 결과의 차이 비교.
- `INTERPRETATION_RECORD`: GPT/사람이 시각 자료를 어떻게 해석했는지 남기는 편집 가능한 기록.

큰 프로젝트는 `00 · VISUAL HUB / 10 · CONCEPT / 20 · UX FLOW / 30 · UI SYSTEM / 40 · IMPLEMENTATION REVIEW / 90 · ARCHIVE`처럼 Page를 나눌 수 있다. 작은 1인 프로젝트는 같은 구조를 한 Page의 Section으로 축소한다. Base는 Figma 채택이나 Page 수를 강제하지 않는다.

### GPT interpretation record

GPT가 시각 작업면에 쓰기 권한을 가진 경우, 화면 옆 텍스트 패널·annotation·동등한 편집 가능한 객체로 `INTERPRETATION_RECORD`를 남길 수 있다. 최소 기록은 `screen_id`, `flow_id`, `visual_artifact_id`, 관련 Decision ID, `source_commit`, 검토 시각, 화면 목적·첫 시선·주요 행동, 다음 Gate다.

시각화에서 관찰한 항목은 다음처럼 분리한다.

- `CONFIRMED`: 현재 정본과 일치하는 표현.
- `DISCOVERED_IDEA`: AI/시각화가 새로 제안했고 검토 가치가 있지만 아직 승인되지 않은 표현.
- `AI_ASSUMPTION`: 정본 근거 없이 생성 과정에서 만들어진 가정.
- `MISSING_CANON`: 판정에 필요한 정본이 없거나 불충분한 항목.
- `VISUAL_CANONICAL_CONFLICT`: 시각 자료가 현재 정본과 충돌하는 항목.

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 보기 좋거나 구현 가능하다는 이유만으로 기획 요구로 승격하지 않는다. 사용자 Decision이 있어야 정본과 구현 계약에 반영한다. Figma 쓰기가 불가능하면 같은 기록을 책임 GitHub 문서나 프로젝트 Sheet에 남기고 `SYNC_PENDING`, `UNAVAILABLE`, `READ_ONLY` 중 실제 상태를 기록한다.

### Prototype and runtime compare

대표 흐름은 다음과 같다.

```text
canonical planning
→ Screen Brief
→ AI planning visualization
→ Screen Interpretation Review
→ Project Visual Flow Workspace registration
→ PROTOTYPE_FLOW when useful
→ user approval
→ IMPLEMENTATION_PINNED
→ Godot/Web implementation
→ RUNTIME_CAPTURE
→ COMPARE_BOARD
→ drift classification
→ VALIDATED or follow-up Decision
```

Prototype은 화면 전환·복귀·상태·정보 위계·피드백 가설을 검토하는 증거다. 실제 Godot 런타임, 저장·경제·보상 도메인 규칙, 성능, 물리 입력, 접근성, 디바이스 동작 완료 증거가 아니다.

승인 시각 참조와 실제 구현 비교는 다음 중 하나로 판정한다.

- `MATCHED`: 승인 의도와 구현이 의미상 일치.
- `INTENDED_DIFFERENCE`: 승인된 후속 Decision 또는 기술 제약으로 의도적으로 변경.
- `IMPLEMENTATION_GAP`: 승인 범위가 구현에서 누락·오표현.
- `PLANNING_CHANGE_REQUIRED`: 구현 과정에서 기획 자체 재결정이 필요.
- `AI_MOCKUP_ERROR`: 초기 AI 시각화의 근거 없는 해석 또는 표현 오류.
- `VISUAL_CANONICAL_CONFLICT`: 시각 참조와 현재 정본이 충돌.
- `BLOCKED_UNVERIFIED`: 비교 증거 부족.

## Artifact lifecycle

`DRAFT_VISUAL → REVIEW_CANDIDATE → APPROVED_VISUAL_REFERENCE → IMPLEMENTATION_PINNED → VALIDATED → SUPERSEDED`

Auxiliary states are `AUTH_REQUIRED`, `ACCESS_DENIED`, `READ_ONLY`, `LINK_UNVERIFIED`, `SNAPSHOT_MISSING`, `SYNC_PENDING`, `VISUAL_CANONICAL_CONFLICT`, and `ARCHIVED`.

At `APPROVED_VISUAL_REFERENCE` or later, record a responsible document, Decision ID, scope/exclusion, last verification, replacement relation, and snapshot path or explicit reason. At `IMPLEMENTATION_PINNED`, also record page/board/frame/node, checked time, source commit, target platform/resolution/input, Godot handoff, and validation predicate.

## Access, safety and fallback

Never publish a private board, change ownership, or place secrets, credentials, private data, or internal keys in a visual workspace. Record public/private access and ownership separately. A link that cannot be read is not evidence of its contents.

If access is unavailable, use Markdown, Mermaid, a table, or a text wireframe; mark it as a fallback rather than an external artifact. `AVAILABLE`, `READ_ONLY`, `AUTH_REQUIRED`, `ACCESS_DENIED`, `UNAVAILABLE`, and `UNVERIFIED` describe capability—not completion.

## GDD and implementation handoff

Sheets hold a short Artifact ID, purpose, context, Decision ID, responsible source, status, link, snapshot, and next check. They do not copy full boards or frames. An implementation handoff uses a pinned Figma frame or a Whimsical structural reference plus a GitHub implementation contract; actual Godot render, input, accessibility, device, and human evidence remain independent and remain `NOT_RUN` until evidence exists.

## Intermediate visual checkpoint

When a user asks for a mid-review, an expected game screen, or a UI-included game screen—or when a planning interpretation gap is `P1`—use the current canonical sources to produce one `DRAFT_VISUAL` screen flow. Require a Screen Brief with purpose, first glance, primary action, platform/resolution/aspect/input, state/risk/cost/reward/success/failure/recovery, Korean and accessibility constraints, Decision IDs, confirmed facts, and `MISSING_CANON` items.

Use image generation only when it is available and authorized. Otherwise use the same brief as a text wireframe, Mermaid, or Figma fallback. Immediately record a Screen Interpretation Review: confirmed alignment, `MISSING_CANON`, `VISUAL_CANONICAL_CONFLICT`, `TECHNICAL_REVIEW_PROPOSAL`, and rejected expressions. A checkpoint never changes canon or becomes a final asset, license approval, Figma handoff, Godot completion, runtime proof, or human-validation proof without a later user Decision and the normal Artifact lifecycle.

## Adversarial review

Reject a change if it makes a visual tool a second canon, forces both tools, duplicates full content across tools, pins a live file without a snapshot, treats a prototype as runtime proof, silently bypasses access failure, auto-promotes `DISCOVERED_IDEA` or `AI_ASSUMPTION`, or mixes project URL/token/design decisions into Base.
