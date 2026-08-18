# Visual Collaboration Tool Policy

Figma와 Whimsical은 기획·UX/UI·인계·검토를 돕는 `VISUAL_WORKSPACE`다. 어느 도구도 GitHub의 승인 결정·상세 규칙·구현 계약·실제 Godot 상태를 대체하지 않는다.

## Context and authority

새 프로젝트와 새 시각 작업의 기본 협업면은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`다. 밸런스·경제·Schema·runtime config 같은 구조화 데이터는 `REPO_NATIVE_STRUCTURED_DATA`가 소유하며, 기존 프로젝트 Google Sheets는 `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE` / `MIGRATION_COMPATIBILITY_SURFACE`로만 보존한다.

각 Artifact는 `GDD`, `EXTERNAL_COLLABORATION`, `BOTH` 중 하나의 `usage_context`를 가진다. GDD 안에서는 사람이 흐름과 화면을 빠르게 확인하는 시각 구성요소이고, GDD 밖에서는 설계 탐색·협업·리뷰·인계의 독립 작업면이다. 둘 중 어느 쪽도 도구 사용을 강제하거나 활용 범위를 제한하지 않는다.

```text
GitHub Markdown·JSON + confirmed decisions → canonical rule and approval
Figma → FIGMA_DEFAULT_VISUAL_WORKSPACE for screen, component, state, prototype, design-system and pinned handoff view
repo-native structured source → REPO_NATIVE_STRUCTURED_DATA for balance, economy, schema and runtime configuration
existing Google Sheets → GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE / MIGRATION_COMPATIBILITY_SURFACE for preserved summary, proposal and migration readback
Whimsical → optional loop, relation, branch, journey, system or work-flow visualization
Godot + tests → actual implementation and validation evidence
```

시각 자료와 정본이 충돌하면 자동 덮어쓰지 않고 `VISUAL_CANONICAL_CONFLICT`로 기록하며 구현을 멈춘다.

## Tool choice

| Need | Prefer | Do not treat as |
| --- | --- | --- |
| core/session/meta loop, dependencies, narrative branches, AI/work process | Whimsical (or Mermaid for small static diagrams) | pixel-accurate UI or rule canon |
| screen hierarchy, component states, focus/input flow, responsive layout, prototype | Figma | game-rule canon or Godot completion evidence |
| balance, economy, schema, runtime configuration | repo-native structured source | a visual-workspace-only value |
| preserved legacy status, link, user proposal and migration readback | configured Google Sheets | a new-project default workspace or a copy of every visual artifact |
| durable rule, decision, handoff contract | GitHub | a live design-file-only decision |

Do not create a `figma-*` or `whimsical-*` Skill merely because a connector exists. Extend the responsible planning, UX/UI, documentation, or handoff Skill. Use either tool independently when it solves the current problem; use both only when a confirmed structure must become a screen contract.

## Artifact lifecycle

`DRAFT_VISUAL → REVIEW_CANDIDATE → APPROVED_VISUAL_REFERENCE → IMPLEMENTATION_PINNED → VALIDATED → SUPERSEDED`

Auxiliary states are `AUTH_REQUIRED`, `ACCESS_DENIED`, `READ_ONLY`, `LINK_UNVERIFIED`, `SNAPSHOT_MISSING`, `SYNC_PENDING`, `VISUAL_CANONICAL_CONFLICT`, and `ARCHIVED`.

At `APPROVED_VISUAL_REFERENCE` or later, record a responsible document, Decision ID, scope/exclusion, last verification, replacement relation, and snapshot path or explicit reason. At `IMPLEMENTATION_PINNED`, also record page/board/frame/node, checked time, source commit, target platform/resolution/input, Godot handoff, and validation predicate.

## Project Figma Visual Bible

프로젝트가 Figma를 사용하는 경우 Figma 파일은 **게임 규칙의 두 번째 정본이나 제품 자산 파일 저장소가 아니라, 승인된 시각 방향·화면·컴포넌트·레퍼런스를 지속적으로 비교하는 Visual Bible**로 운영할 수 있다. 프로젝트별 상세 구조는 `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`를 복제·최적화한다.

권장 최소 페이지:

```text
00_DIRECTION
01_APPROVED_REFERENCE
02_WIP
03_REJECTED
04_FINAL
```

이 페이지 이름은 Figma 안에서 사람과 AI가 탐색하기 위한 **조직 규칙**이며 Artifact lifecycle을 새로 만들지 않는다.

| Figma page | 의미 | Artifact/asset 경계 |
| --- | --- | --- |
| `00_DIRECTION` | mood, palette, shape language, camera, UI direction, `Do Not Drift` | 방향 참고면이며 단독 Decision canon 아님 |
| `01_APPROVED_REFERENCE` | 이후 시각 작업에서 우선 비교할 승인 레퍼런스 | 연결 Artifact는 최소 `APPROVED_VISUAL_REFERENCE`여야 함 |
| `02_WIP` | 탐색·수정·검토 중 후보 | `DRAFT_VISUAL` 또는 `REVIEW_CANDIDATE`; 다음 작업의 승인 기준으로 자동 사용 금지 |
| `03_REJECTED` | 불채택 시안과 제외 이유 | 승인 레퍼런스로 재사용 금지; 재도입은 새 검토 필요 |
| `04_FINAL` | 시각적으로 사용 확정된 표현을 모으는 페이지 | `PROJECT_ASSET_APPROVED`, tracked asset, Godot runtime proof를 자동 의미하지 않음 |

이미지·시각 자료 작업에서는 접근 가능한 최신 프로젝트 정본과 Decision을 먼저 확인한 뒤, Visual Artifact Registry에서 연결된 Figma와 `APPROVED_VISUAL_REFERENCE`를 찾고 실제 frame/node를 읽을 수 있을 때만 그 내용을 기준으로 사용한다. 승인 레퍼런스에서 `Keep / Avoid / Do Not Drift`를 추출해 새 생성·편집 계약에 고정하고, 새 결과는 기본적으로 WIP/review 후보로 두며 기존 승인본과 스타일·비율·색·형태·카메라·UI 계층을 비교한다.

프로젝트 Figma가 `CONFIGURED`이고 쓰기 권한이 있으면 새 이미지·UI·시각 자료는 생성·편집 직후 실제 Figma `02_WIP`에 업로드하거나 배치하고 Visual Artifact Registry의 file/page/frame/node와 `DRAFT_VISUAL` 또는 `REVIEW_CANDIDATE` 상태를 연결한다. 쓰기 권한이 없거나 연결에 실패하면 결과물을 잃지 않도록 현재 작업 위치에 보존하고 `READ_ONLY`, `AUTH_REQUIRED`, `ACCESS_DENIED`, `LINK_UNVERIFIED` 또는 `SYNC_PENDING`을 기록한다. 이 경우 Figma에 동기화됐다고 보고하지 않는다.

사용자 승인 뒤에만 Figma의 Approved/Final 위치와 Registry 상태를 갱신한다. 실제 이미지 bytes의 후보·제품 승격 권위는 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`와 tracked asset 계약이 계속 소유하며, `PROJECT_ASSET_APPROVED → promote`를 우회하지 않는다.

Figma 링크나 frame/node를 읽을 수 없으면 과거 대화·파일명·스크린샷 추정으로 내용을 확인했다고 보고하지 않는다. `LINK_UNVERIFIED`, `AUTH_REQUIRED`, `ACCESS_DENIED`, `READ_ONLY` 또는 `UNVERIFIED`를 기록하고 Markdown·text wireframe·로컬 승인 자산 등 현재 접근 가능한 근거로 fallback한다. Figma 접근 실패만으로 Google Sheets를 새 기본 시각 workspace로 되살리지 않는다.

Figma의 Pages/Sections는 단계·milestone·협업 구역을 나누는 데 사용하고, 반복되는 UI 요소가 충분히 안정화된 프로젝트는 Components/Styles를 사용해 일관성을 높일 수 있다. 팀 Library 발행은 요금제·권한과 실제 재사용 필요가 확인된 경우에만 선택적으로 사용하며 Base가 강제하지 않는다. 큰 변경 전에는 Figma version history 또는 사용 가능한 branch/checkpoint를 활용해 복구 가능성을 확보한다.

### Reusable visual references and reuse promotion

Primary Use Gate를 통과한 시각 결과에서 반복 가치가 검증된 요소는 Figma Visual Bible의 reusable reference/component/pattern으로 **reuse promotion**할 수 있다. 이 승격은 시각 비교·재사용 편의를 위한 것이며 제품 자산 승격과 분리한다.

```text
primary-use accepted visual
→ Reusable Visual Harvest Gate
→ REUSE_AS_IS / VARIANT_SEED / STRUCTURE_PATTERN / STYLE_DNA / REBUILD_FOR_REUSE / ONE_OFF_KEEP / REJECT_REUSE
→ Figma reusable reference/component/pattern when applicable
```

- `REUSE_AS_IS`와 `VARIANT_SEED`는 반복해서 실제로 쓸 가치가 있는 visual primitive/variant 기준에 사용한다.
- `STRUCTURE_PATTERN`은 layout·hierarchy·interaction 구조를 기록하지만 게임 규칙의 새 정본이 되지 않는다.
- `STYLE_DNA`는 palette·shape·material·lighting·camera·spacing의 `Keep / Avoid / Do Not Drift`를 보존한다.
- `REBUILD_FOR_REUSE`는 생성 화면의 raster crop을 장기 UI 자산으로 착각하지 않고 Figma Component/Variant 또는 이후 Godot Theme/Scene/Resource로 의미 기반 재구축할 때 사용한다.
- `ONE_OFF_KEEP`는 hero/narrative/title-specific 화면을 공용 library에 억지로 넣지 않는 정상 판정이다.
- `DERIVED_GENERATIVE_RECOVERY`가 포함되면 원본 관측 사실이 아닌 generated/derived pixel임을 Visual Artifact Registry와 Asset Vault provenance에 연결한다.

Figma에서의 reuse promotion은 `PROJECT_ASSET_APPROVED`가 아니다. 실제 후보 bytes는 **Asset Vault**가 소유하고, tracked 제품 자산은 `ASSET_MANIFEST.yml + promote` 경계를 통과해야 하며, 재사용 가능한 **Godot** Scene/Resource/Theme 또는 실제 runtime 사용은 별도 구현·검증 증거가 필요하다. Figma component 등록·Library 발행·`04_FINAL`만으로 이 경계를 건너뛰지 않는다.

### Project Visual Flow Workspace

Visual Bible 안에서 화면 흐름을 관리할 때는 단순 이미지 저장이 아니라 `Project Visual Flow Workspace`로 운영한다. 대표 화면을 `screen_id`, 흐름을 `flow_id`로 묶고 화살표·Prototype 연결을 사용해 진입·전환·취소·복귀·실패 복구를 한눈에 확인한다.

권장 Artifact 유형:

- `FLOW_MAP`: 여러 화면의 이동 관계를 한 보드에서 보여주는 지도.
- `SCREEN_CONCEPT`: AI 생성 또는 수동 제작한 화면 개념 시안.
- `PROTOTYPE_FLOW`: 클릭·전환·복귀·상태 변화 검토용 Prototype.
- `INTERPRETATION_RECORD`: GPT/사람이 화면을 어떻게 해석했는지 남기는 편집 가능한 기록.
- `RUNTIME_CAPTURE`: 실제 Godot/Web 구현 캡처.
- `COMPARE_BOARD`: 승인 시각 참조와 실제 구현의 차이 비교.

대표 흐름:

```text
canonical planning
→ Screen Brief
→ AI planning visualization
→ Screen Interpretation Review
→ FLOW_MAP / Project Visual Flow Workspace
→ PROTOTYPE_FLOW when useful
→ user approval
→ IMPLEMENTATION_PINNED
→ Godot/Web implementation
→ RUNTIME_CAPTURE
→ COMPARE_BOARD
→ drift classification
→ VALIDATED or follow-up Decision
```

Prototype은 화면 흐름·정보 위계·피드백 가설을 검토하는 증거다. 실제 Godot 런타임, 저장·경제·보상 규칙, 성능, 물리 입력, 접근성 완료 증거가 아니다.

### GPT interpretation record

GPT가 Figma 쓰기 권한을 가진 경우 화면 옆 **편집 가능한 텍스트 패널·annotation 또는 동등한 Figma 객체**로 `INTERPRETATION_RECORD`를 남길 수 있다. 최소 기록은 `screen_id`, `flow_id`, `visual_artifact_id`, 관련 Decision ID, `source_commit`, 검토 시각, 화면 목적·첫 시선·주요 행동, 다음 Gate다.

관찰 내용은 다음처럼 분리한다.

- `CONFIRMED`: 현재 정본과 일치하는 표현.
- `DISCOVERED_IDEA`: 시각화 과정에서 새로 발견한 제안으로, 검토 가치는 있지만 아직 승인되지 않음.
- `AI_ASSUMPTION`: 정본 근거 없이 AI가 추가한 기능·재화·상태·구성.
- `MISSING_CANON`: 판정에 필요한 정본이 불충분함.
- `VISUAL_CANONICAL_CONFLICT`: 시각 자료가 현재 정본과 충돌함.

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 보기 좋거나 구현 가능하다는 이유만으로 기획 요구로 승격하지 않는다. 사용자 Decision 뒤에만 정본·구현 계약에 반영한다. Figma 쓰기가 불가능하면 같은 기록을 책임 GitHub 문서에 남기고, 이미 구성된 legacy Sheet가 migration 범위에 있을 때만 해당 Sheet에도 연결할 수 있다. 실제 상태는 `SYNC_PENDING`, `READ_ONLY`, `AUTH_REQUIRED`, `ACCESS_DENIED` 또는 `UNVERIFIED`로 기록한다.

승인 시각 참조와 실제 구현 비교는 `MATCHED / INTENDED_DIFFERENCE / IMPLEMENTATION_GAP / PLANNING_CHANGE_REQUIRED / AI_MOCKUP_ERROR / VISUAL_CANONICAL_CONFLICT / BLOCKED_UNVERIFIED` 중 하나로 판정한다. 실제 `RUNTIME_CAPTURE`가 없으면 Prototype만으로 `MATCHED`를 주장하지 않는다.

## Access, safety and fallback

Never publish a private board, change ownership, or place secrets, credentials, private data, or internal keys in a visual workspace. Record public/private access and ownership separately. A link that cannot be read is not evidence of its contents.

If access is unavailable, use Markdown, Mermaid, a table, or a text wireframe; mark it as a fallback rather than an external artifact. `AVAILABLE`, `READ_ONLY`, `AUTH_REQUIRED`, `ACCESS_DENIED`, `UNAVAILABLE`, and `UNVERIFIED` describe capability—not completion.

## GDD and implementation handoff

Configured legacy Sheets may hold a short Artifact ID, purpose, context, Decision ID, responsible source, status, link, snapshot, and next check during migration. They do not copy full boards or frames and are not required for new projects. An implementation handoff uses a pinned Figma frame or a Whimsical structural reference plus a GitHub implementation contract; actual Godot render, input, accessibility, device, and human evidence remain independent and remain `NOT_RUN` until evidence exists.

## Intermediate visual checkpoint

When a user asks for a mid-review, an expected game screen, or a UI-included game screen—or when a planning interpretation gap is `P1`—use the current canonical sources to produce one `DRAFT_VISUAL` screen flow. Require a Screen Brief with purpose, first glance, primary action, platform/resolution/aspect/input, state/risk/cost/reward/success/failure/recovery, Korean and accessibility constraints, Decision IDs, confirmed facts, and `MISSING_CANON` items.

Use image generation only when it is available and authorized. Otherwise use the same brief as a text wireframe, Mermaid, or Figma fallback. Immediately record a Screen Interpretation Review: confirmed alignment, `MISSING_CANON`, `VISUAL_CANONICAL_CONFLICT`, `TECHNICAL_REVIEW_PROPOSAL`, and rejected expressions. A checkpoint never changes canon or becomes a final asset, license approval, Figma handoff, Godot completion, runtime proof, or human-validation proof without a later user Decision and the normal Artifact lifecycle.

## Adversarial review

Reject a change if it makes a visual tool a second canon, forces both tools, duplicates full content across tools, pins a live file without a snapshot, treats a prototype as runtime proof, silently bypasses access failure, auto-promotes `DISCOVERED_IDEA` or `AI_ASSUMPTION`, treats Figma reuse promotion as `PROJECT_ASSET_APPROVED`, restores Google Sheets as a new-project default workspace, or mixes project URL/token/design decisions into Base.
