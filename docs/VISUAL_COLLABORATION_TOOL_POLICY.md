# Visual Collaboration Tool Policy

## Current authority

The default project operating surface is `NOTION_DEFAULT_PROJECT_WORKSPACE`.

Authority is split by domain instead of forcing one tool to own every representation.

```text
Notion project workspace
→ NOTION_HUMAN_FACING_CANON
→ project overview / visual direction / visual asset catalog
→ budget tables / tier tables / human-editable Flow Map / Storyboard
→ the primary surface a person reads, compares, and edits

repository-native Markdown / JSON / game data / code / scenes / resources / tests
→ REPOSITORY_STRUCTURED_CANON
→ REPOSITORY_RUNTIME_TRUTH for implemented/runtime facts

legacy Google Sheets
→ COMPATIBILITY_ONLY when an existing migration source still contains unique material
```

`DOMAIN_SPLIT_CANON` means neither side is a disposable copy. Notion has priority for the human-facing visual/table/overview domains above; the repository has priority for structured specifications, data and implementation/runtime domains. When a Notion edit implies a Markdown/data/code/scene/resource/test change, synchronize that structured change to the repository before implementation or runtime claims (`SYNC_BEFORE_IMPLEMENTATION`).

No visual collaboration tool becomes a second runtime or implementation canon.

## Supported collaboration contexts

The same project-boundary rules apply whether the immediate work context is `GDD`, `EXTERNAL_COLLABORATION`, or `BOTH`. These labels describe where a visual decision is being consumed; they do not create another authority.

## Project boundary

`PROJECT_RELATION_REQUIRED` is mandatory for project-scoped Work, Asset, Component, Screen, Reference and Benchmark records.

One workspace may contain many projects, but a normal project page exposes only Project-filtered views. Unfiltered Master views belong under the system-master area and are not the default human work surface.

Cross-project reuse keeps one source record and records reuse intent; do not clone records into multiple projects as separate current authorities.

## Standard project surface

```text
PROJECT HOME
→ current direction / core fun / core loop / blockers / quick links

01 · PROJECT CONTROL
→ WORK_MASTER filtered to the selected Project

02 · VISUAL BIBLE
→ approved visual direction / human-readable north star

03 · FLOW MAP / STORYBOARD
→ human-editable visual relationship surface
→ VISUAL_MAP_DERIVED from structured records when appropriate

04 · ASSET LIBRARY
→ ASSET_KNOWLEDGE_MASTER filtered to the selected Project

05 · REFERENCE / BENCHMARK
→ evidence and adoption decisions

06 · PRODUCTION / HANDOFF
→ approved planning → repository implementation → runtime validation

07+ · PROJECT-SPECIFIC CONFIRMED TABLES
→ budget / tier / roster / economy / progression / other human-learning tables when useful
```

Project-specific confirmed tables are encouraged when they materially improve human understanding. They summarize approved facts with source Decision IDs/paths and must visibly separate confirmed, provisional, deferred and rejected values.

## Intermediate visual checkpoint

`Intermediate visual checkpoint` is a project-scoped decision gate, not a tool/page-specific location.

- `MISSING_CANON`: there is not enough approved visual direction to judge continuity safely.
- `DRAFT_VISUAL`: the artifact is an exploratory checkpoint and is not an approved project asset.
- `PROJECT_ASSET_APPROVED`: the project authority accepted the asset for a stated role.
- `APPLIED_AND_RUNTIME_VERIFIED`: repository/runtime integration has separate evidence.

A checkpoint may use a screenshot, generated image, component preview, semantic flow or Visual Map. It must retain the correct Project relation and must not imply runtime success merely because the draft looks correct.

## Asset and knowledge model

The shared Asset/Knowledge Master uses `Record Type` values such as:

```text
ASSET
COMPONENT
SCREEN
REFERENCE
BENCHMARK
```

Human-facing Gallery/Table views should emphasize Preview, Name, Usage, Style, Approved and Reuse.

The `AI / System` view may retain Asset ID, Project, version, Status, Category, Prompt, AI Note, source provenance, Rights / License, Hash, Implementation Path and Decision without forcing those fields into the normal human view.

Benchmark decisions use:

```text
ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE
```

External references are evidence and inspiration, not project canon. Record why a source matters and what is transferable; do not copy identifiable expression merely because the source is cataloged.

## Confirmed planning tables

Budget, tier, roster, economy and progression tables that are primarily for human comparison belong in Notion as `NOTION_HUMAN_FACING_CANON`.

Each confirmed table must preserve enough traceability to cross-check the repository:

```text
Project
→ table purpose
→ Decision ID or canonical repository path
→ confirmed / provisional / deferred / rejected state
→ repository main SHA or equivalent freshness locator when practical
→ last Notion sync date
```

Do not turn a human table into an undocumented second data model. Machine-consumed JSON/game data stays in the repository. Conversely, do not force the user to inspect raw Markdown/JSON when a visual table is the clearer primary human representation.

## Image and visual candidate lifecycle

```text
need / brief
→ generate or edit candidate
→ bounded visual review
→ attach candidate to the correct Project record
→ readback
→ explicit approval or rejection
→ version / replacement relationship
→ implementation task when needed
→ runtime evidence separately
```

For identity-preserving edits, unchanged identity attributes are hard constraints. Change only the requested expression, pose, gaze, effect stage, UI state or other scoped property.

A successful generation is not approval. A successful upload is not delivery until readback confirms the expected file/preview/version at the intended Project target.

## Reuse promotion

Reusable visual harvest and reuse promotion happen in `ASSET_KNOWLEDGE_MASTER`, not in a tool-specific profile. A source candidate may be classified as `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, or `REJECT_REUSE` before any project approval. Reuse classification does not itself grant approval or rights.

## Visual Map

`VISUAL_MAP_DERIVED` means the map may be generated from current Screen/relationship records and approved previews; it does **not** mean the human must treat the map as disposable. Once approved in Notion, that Notion view is the primary human-facing representation for visual planning and review.

Game projects may visualize screen IDs, thumbnails, entry points, primary/secondary/conditional routes and key systems. Narrative projects may visualize canon, character, faction, clue, scene and continuity relationships.

If a visual edit changes structured semantics, reconcile the semantic records/repository before implementation. If repository runtime facts change, refresh the Notion map so the person-facing view does not drift.

## Human and AI views

The same records support two display layers:

- `human` view: sparse visual information for scanning, learning, comparison and direct planning edits.
- `AI / System` view: provenance, IDs, version, status, hash, prompt, rights and implementation metadata.

Hiding system metadata is a presentation decision, not deletion. Automation may still read it when needed.

## Release-near Vertical Slice visual readiness

`RELEASE_NEAR_VERTICAL_SLICE_FIRST`를 게임 플레이 검증의 기본으로 한다. 기획·검수를 닫은 뒤 재미·몰입·가독성·첫인상·판매 포인트·감정 곡선을 판단하는 플레이 테스트는 `shipping-intent` 짧은 Vertical Slice에서 수행한다. `SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED`에 따라 실제 게임 사용 후보인 UI/UX, 이미지·아트, 애니메이션/연출, 음악·효과음, VFX/피드백, 핵심 시스템·데이터·콘텐츠를 서로 연결한 상태여야 한다. 플레이어가 실제로 보는·듣는·조작하는 Slice 경로에는 임시 `player-facing placeholder`나 dummy presentation을 남기지 않는다.

```text
planning + UX/UI/audio/VFX flow
→ PROJECT_VISUALIZATION_NEED_MAP
→ visual/audio/effect requirements
→ generate/select/reuse candidate assets
→ Notion Project placement + readback
→ approval/rejection
→ repository implementation package
→ shipping-intent UI + image/art + audio + VFX + system/content integration
→ complete short Vertical Slice
→ runtime UX/UI/play test
```

`SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`: 회색 상자, dummy UI, 무음/무연출, 시스템-only PoC는 기술 Spike로만 사용할 수 있으며 재미·몰입·전체 UX·플레이어 기억의 최종 판단 근거가 아니다. 좁은 기술 질문은 `TECHNICAL_SPIKE_INTERNAL_ONLY`로 먼저 풀 수 있지만, 그 결과는 완성형 Vertical Slice에 흡수한 뒤 플레이 테스트한다. 생성 성공·업로드 성공·정적 mockup만으로 player-experience PASS를 선언하지 않는다.

## Repository handoff and runtime evidence

Notion approval means the project accepted the human-facing planning, table, visual direction or asset candidate for its stated use. It does not prove runtime implementation.

```text
Notion approved human-facing record
→ synchronize any required Markdown / JSON / game data contract
→ repository implementation task
→ code / asset / scene / resource / config
→ build or runtime
→ REPOSITORY_NATIVE_EVIDENCE_CAPTURE
→ Notion readback/status refresh
```

`REPOSITORY_NATIVE_EVIDENCE_CAPTURE`는 별도 QA GUI/app을 요구하지 않는다. 현재 프로젝트가 이미 쓰는 tests, GUT, Godot/Hera runtime, logs, screenshots/video, CI artifacts를 exact project/build identity에 묶고 `PASS / FAIL / BLOCKED / NOT_RUN`과 evidence ceiling을 기록한다. Notion preview는 사람이 보는 연결면이며 runtime truth를 대체하지 않는다.

## Legacy and deprecated visual execution paths

Dedicated Figma routing, Figma Bridge, localhost Expression/Sprite Studios, visual-delivery/project-management Tool Hub, QA Evidence Studio, and external HTML workspace/catalog/dashboard are not active authorities or required project surfaces. 재사용 가능한 아이디어—project identity, provenance, bounded edits, approval, versioning, reuse classification, readback, evidence ceiling, explicit handoff—만 current Notion/repository/PowerShell/Loop owner에 흡수한다.

Do not restore a deprecated execution surface merely because historical docs, Git history or archived evidence mention it. Reintroduction requires a new Existing Solution First comparison, lifecycle-cost justification and user approval.

## Cost boundary

The default path must satisfy `ZERO_INCREMENTAL_COST_REQUIRED`. Notion Free may be used within its current feature/file-size limits; paid Notion AI, separately metered storage, paid automation, or external provider calls are not part of the default workflow. Current paid AI plan is `GPT_PRO` only.

## Adversarial rejection criteria

Reject or revise a change if it:

- exposes unfiltered cross-project records on a normal project page;
- treats Notion human-facing tables/visuals as runtime proof;
- creates a competing structured data model in a visual table instead of synchronizing machine data to the repository;
- duplicates one approved asset into multiple independent project authorities;
- hides provenance by deleting metadata instead of hiding it from the human view;
- reports upload success without readback;
- promotes a Reference/Benchmark to approved asset without a project decision;
- leaves an approved Notion visual/table materially inconsistent with the repository domain it is meant to summarize;
- reintroduces Figma, Tool Hub, QA Studio, external HTML or another deprecated visual/management surface without current evidence and new approval;
- reports repository-native static/test evidence as human fun/usability proof.
