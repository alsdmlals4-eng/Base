# Project Visual Flow Workspace Design

## Goal

AI와 기획한 게임 화면을 Figma 같은 시각 작업면에 모아 화면 흐름·프로토타입·구현 비교까지 연결하되, 시각 자료가 GitHub 정본이나 실제 런타임 증거를 대체하지 않도록 Base 공용 계약을 보강한다.

## Existing Solution First

- 기존 책임 원본: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- 기존 시각 Artifact 색인: `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`
- 기존 이미지 생성·검수 책임: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- 기존 UX/UI flow·prototype·runtime audit 책임: `skills/auditing-and-refining-ui-art/SKILL.md`
- 기존 GDD 시각 작업면: `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`의 `06_시각_작업면`
- 기존 이미지 계획: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

판정: `ABSORB`. 새 `figma-*` Skill이나 제2 시각 정본을 만들지 않고 기존 책임에 흡수한다.

## Player / User Value

1. 텍스트 기획을 대표 게임 화면으로 빠르게 구체화한다.
2. 사용자와 AI의 해석 차이를 시각 자료 옆에서 즉시 확인한다.
3. AI가 임의로 추가한 표현을 확정 기획과 분리해 환각 역수입을 막는다.
4. 화면 전환과 복귀를 Prototype으로 검토해 Godot 구현 전에 UX 결함을 줄인다.
5. 승인 시안과 실제 구현 캡처를 비교해 의도된 변경과 구현 누락을 구분한다.
6. 화면·상태·컴포넌트·자산 수를 보면서 제작 규모를 더 이르게 추정할 수 있다.

## Authority Boundary

```text
GitHub Markdown·JSON + confirmed decisions = canonical rule / approval
Google Sheets = user-facing GDD summary and editable review surface
Figma / visual workspace = Project Visual Flow Workspace
Godot + tests + runtime capture = implementation / validation evidence
```

Visual workspace는 독립 정본이 아니다. 시각 자료가 정본과 충돌하면 `VISUAL_CANONICAL_CONFLICT`로 기록하고 자동 반영·자동 구현을 중지한다.

## Project Visual Flow Workspace

프로젝트별 Figma 파일 또는 동등한 시각 작업면을 다음 목적에 사용한다.

- `FLOW_MAP`: 게임 전체 또는 한 기능의 화면 이동 지도
- `SCREEN_CONCEPT`: AI 생성 또는 수동 제작한 개념 화면
- `SCREEN_WIREFRAME`: 구조·정보 위계 중심의 편집 가능한 화면
- `PROTOTYPE_FLOW`: 클릭·전환·복귀·상태 변화 검토용 흐름
- `RUNTIME_CAPTURE`: 실제 Godot/Web 구현 캡처
- `COMPARE_BOARD`: 승인 시각 참조와 구현 결과의 차이 비교
- `INTERPRETATION_RECORD`: GPT/사람의 화면 해석 기록

권장 Figma page 구조는 프로젝트가 필요할 때만 사용한다.

```text
00 · VISUAL HUB
10 · CONCEPT
20 · UX FLOW
30 · UI SYSTEM
40 · IMPLEMENTATION REVIEW
90 · ARCHIVE
```

페이지 수 자체를 Base가 강제하지 않는다. 작은 프로젝트는 한 페이지의 Section으로 축소할 수 있다.

## GPT Interpretation Record

GPT가 시각 작업면에 쓰기 권한을 가진 경우 화면 옆에 편집 가능한 텍스트/annotation 형태로 해석 기록을 남길 수 있다. Figma connector가 없거나 쓰기 권한이 없으면 동일 내용을 GitHub/Sheet에 기록하고 `SYNC_PENDING` 또는 `UNAVAILABLE`로 둔다.

각 기록은 최소 다음을 가진다.

```yaml
screen_id:
flow_id:
visual_artifact_id:
related_decision_ids: []
source_commit:
reviewed_at:
purpose:
first_attention:
primary_action:
confirmed_alignment: []
discovered_ideas: []
ai_assumptions: []
missing_canon: []
visual_canonical_conflicts: []
rejected_expressions: []
next_gate:
```

해석 항목의 의미:

- `CONFIRMED`: 현재 정본과 일치하는 표현
- `DISCOVERED_IDEA`: AI/시각화가 새로 제안했으며 검토 가치가 있지만 아직 승인되지 않은 표현
- `AI_ASSUMPTION`: 정본 근거 없이 시각화 과정에서 만들어진 가정

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 없이 정본·구현 요구로 승격하지 않는다.

## Lifecycle

```text
DRAFT_VISUAL
→ REVIEW_CANDIDATE
→ APPROVED_VISUAL_REFERENCE
→ IMPLEMENTATION_PINNED
→ VALIDATED
→ SUPERSEDED
```

대표 루프:

```text
canonical planning
→ Screen Brief
→ AI planning visualization
→ Screen Interpretation Review
→ Visual Flow Workspace registration
→ prototype if useful
→ user approval
→ implementation pin
→ Godot/Web implementation
→ runtime capture
→ compare board
→ drift classification
→ validation / follow-up decision
```

## Drift Classification

승인 시각 참조와 실제 구현 비교는 다음 중 하나로 판정한다.

- `MATCHED`: 승인 의도와 구현이 의미상 일치
- `INTENDED_DIFFERENCE`: 승인된 후속 결정 또는 기술 제약으로 의도적으로 변경
- `IMPLEMENTATION_GAP`: 승인 범위가 구현에서 누락·오표현
- `PLANNING_CHANGE_REQUIRED`: 구현 과정에서 기획 자체 재결정이 필요
- `AI_MOCKUP_ERROR`: 초기 AI 시각화의 근거 없는 해석 또는 표현 오류
- `VISUAL_CANONICAL_CONFLICT`: 시각 참조가 현재 정본과 충돌
- `BLOCKED_UNVERIFIED`: 비교 증거가 부족

## Prototype Boundary

Prototype은 사용자 흐름·전환·상태·복귀·피드백 가설을 검토하는 증거다. Godot 런타임, 실제 입력, 성능, 접근성, 저장/경제/보상 도메인 로직 완료 증거가 아니다.

## Figma Handoff / Annotation

Figma의 공식 Prototype 기능은 여러 flow와 starting point를 한 page에서 구성할 수 있으며, Dev Mode annotation은 화면 요소에 추가 문맥과 텍스트 설명을 연결할 수 있다. 프로젝트가 해당 기능과 권한을 사용할 수 있으면 `INTERPRETATION_RECORD`의 표현 수단으로 활용할 수 있다.

공식 참고:
- https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma
- https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode
- https://help.figma.com/hc/en-us/articles/22012921621015-Guide-to-inspecting
- https://www.figma.com/customers/how-king-brings-game-design-together/

## Minimal Project Adoption

1인 개발 프로젝트의 최소 운영은 다음 네 요소면 충분하다.

1. `VISUAL HUB` 또는 동등한 Flow Map
2. 핵심 Screen Concept
3. 화면 옆 `INTERPRETATION_RECORD`
4. 구현 뒤 `RUNTIME_CAPTURE`와 필요한 경우 `COMPARE_BOARD`

Prototype, design system, 상세 Dev Mode handoff는 프로젝트 규모와 구현 단계가 정당화할 때만 추가한다.

## Adversarial Review

### Attack

- Figma가 두 번째 정본이 될 수 있다.
- AI가 만든 재화·랭킹·버튼·기능이 승인 없이 기획으로 역수입될 수 있다.
- 화면을 대량 생성하면 이미지 저장소만 늘고 유지비가 커질 수 있다.
- Prototype이 실제 Godot 구현 완료로 오해될 수 있다.
- live Figma만 참조하면 버전 변경 뒤 당시 구현 기준을 복원하기 어렵다.
- interpretation record가 장문 중복 문서가 될 수 있다.

### Validated decisions

- 새 Skill은 만들지 않고 기존 owner에 흡수한다.
- `Decision ID`, `source_commit`, `snapshot_path`로 정본·시점 연결을 유지한다.
- 해석 기록은 `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION` 분류로 제한한다.
- 최소 프로젝트 운영을 제공해 과도한 Figma 관리 비용을 방지한다.
- Prototype과 runtime proof를 명시적으로 분리한다.
- Sheet에는 전문을 복사하지 않고 Artifact ID와 링크·상태만 기록한다.

## Scope

### In scope

- Visual collaboration policy 강화
- AI image Skill의 Figma 편입 및 interpretation 분류
- UX/UI Skill의 prototype/runtime compare loop
- 이미지 계획 Template과 Visual Artifact Registry 필드 보강
- `06_시각_작업면` 운영 예시 강화
- 회귀 테스트

### Out of scope

- 특정 프로젝트 Figma 파일 생성 또는 강제 마이그레이션
- 새 Figma 전용 Skill
- 모든 프로젝트에 Prototype 강제
- Godot UI 자동 구현
- Figma를 정본 또는 runtime proof로 승격

## Acceptance Criteria

- 기존 Figma/Whimsical 공용 권한 경계를 유지한다.
- `Project Visual Flow Workspace`가 정책과 최소 두 책임 Skill에 연결된다.
- GPT 해석 기록의 `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION` 규칙이 명시된다.
- `PROTOTYPE_FLOW`, `RUNTIME_CAPTURE`, `COMPARE_BOARD`, drift classification이 registry/template에서 추적 가능하다.
- 기존 visual collaboration contract 테스트가 유지되고 새 규칙을 검사한다.
- 새 ACTIVE Skill은 추가되지 않는다.
- 실행하지 않은 실제 Figma/Godot 검증은 `NOT_RUN` 또는 `UNVERIFIED`로 남는다.
