# Game Visual Asset Coverage — adversarial review receipt

## Scope and evidence ceiling

```yaml
review_date: 2026-08-26
repository: alsdmlals4-eng/Base
baseline_main_head: 713756c34c52caf8a00c86bf1d7a240f6e6a7092
work_branch: docs/visual-asset-coverage-checklist-20260826
proposal: BCP-2026-036
scope: STATIC_BASE_VISUAL_ASSET_COVERAGE_CONTRACT
image_generation_run: NOT_RUN
project_asset_generation: NOT_RUN
notion_delivery: NOT_RUN
project_runtime_or_player_validation: NOT_RUN
```

이 검토는 게임 개발 시 필요한 이미지·시각 자산 종류를 빠뜨리지 않도록 하는 **coverage preflight**와 기존 image requirement/generation/review owner의 연결을 검토한다. 실제 프로젝트 이미지가 생성·승인·Godot 적용·플레이 검증됐다고 주장하지 않는다.

## Current-state sources inspected

### Base current owners

- `AGENTS.md` — `REUSE_FIRST_PREFLIGHT_REQUIRED`, 최소 3대안, 5회 이상 전체 적대적 검토, open PR read-only.
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` — Visual Requirement Gate, Delete Test, role, P0~P3, disposition.
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` — explicit image approval, candidate lifecycle, Notion readback, promotion, runtime evidence.
- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` — Notion human-facing canon, repository structured/runtime truth, visual lifecycle.
- `skills/designing-art-prompts-and-technique-cards/SKILL.md` — selected requirement → prompt/generation/review contract.
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md` — image backlog, QA, approval/readback/runtime compare.

### External official/practical benchmark sources

1. Godot — Multiple resolutions: `https://docs.godotengine.org/en/latest/tutorials/rendering/multiple_resolutions.html`
   - design/base size와 실제 window/viewport의 다양한 resolution/aspect scaling을 별도로 다룸.
2. Godot — Import process: `https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/import_process.html`
   - imported asset은 Godot import preset과 reimport parameter를 가지며 source asset과 runtime-consumed imported resource를 구분함.
3. Godot — GPU optimization / texture compression: `https://docs.godotengine.org/en/latest/tutorials/performance/gpu_optimization.html`
   - texture compression은 2D/3D/pixel-art 사용처에 따라 trade-off가 다르므로 단일 고정 preset이 부적절함.
4. Steamworks — Graphical Assets Overview: `https://partner.steamgames.com/doc/store/assets`
   - store/library/event asset의 역할·규격이 별도이며 2024년에도 다수 규격이 변경된 기록이 있어 current official recheck가 필요함.
5. Steamworks — Store Graphical Assets / Rules: `https://partner.steamgames.com/doc/store/assets/standard`, `https://partner.steamgames.com/doc/store/assets/rules`
   - capsule과 screenshot은 역할 및 콘텐츠 제한이 다르며 screenshots는 실제 gameplay를 보여줘야 함.
6. W3C WCAG 2.1 — Use of Color: `https://www.w3.org/WAI/WCAG21/Understanding/use-of-color`
   - 중요한 정보·상태·행동을 color만으로 전달하지 말고 shape/text/pattern 같은 추가 visual cue를 제공함.

외부 자료는 Base의 프로젝트 정본이 아니며 `ADOPT / ADAPT / REJECT` 원리 추출에만 사용한다.

## Three materially distinct alternatives

### A — 독립 마스터 자산 목록을 새 정본으로 추가

- 장점: 사람이 한 파일에서 모든 자산을 볼 수 있다.
- 실패: Visual Requirement, Notion Asset, Asset Manifest, Vault, runtime state와 중복돼 second canon/drift가 생긴다.
- 결정: `REJECT`.

### B — 기존 GPT Image Plan에만 긴 checklist를 추가

- 장점: 새 guide가 적다.
- 실패: image generation task를 열기 전에는 coverage가 발견되지 않고, Art planning/Vertical Slice/Release readiness에서 재사용하기 어렵다.
- 결정: `ADAPT_ONLY`, 단독 해법으로는 부족.

### C — subordinate Coverage Guide + 기존 owner/Skill/template 연결

- 장점: 누락 탐지 책임과 실제 requirement/asset/runtime 책임을 분리한다. 프로젝트별 `NOT_APPLICABLE`을 허용하며 기존 explicit approval gate를 그대로 유지한다.
- 비용: 한 번의 preflight step이 추가된다.
- 결정: `ADOPT`, 이번 구현안.

## Whole-state adversarial loops

| Loop | Whole-state attack | Finding | Correction | Regression / re-attack | Result |
|---|---|---|---|---|---|
| 1 | Coverage table이 새로운 asset canon이 되는가 | 최초 단순 목록은 상태/승인까지 붙이면 Manifest/Notion/Vault와 경쟁할 위험이 있음 | `COVERAGE_CHECK_ONLY`, `NOT_A_SECOND_ASSET_CANON`; existing asset/requirement/evidence link만 허용 | policy/Skill/template에서 coverage lifecycle과 asset lifecycle을 분리했는지 재검토 | PASS |
| 2 | 목록 때문에 모든 프로젝트가 수백 자산을 만들어야 하는가 | 8-direction, portrait, PBR map, marketing set 등은 장르/단계마다 불필요할 수 있음 | `NOT_APPLICABLE`, stage별 scope, Delete Test, current consumer 기반 applicability 추가 | 2D/3D, PoC/Vertical Slice/Release를 대입해 불필요 asset 강제 여부 재공격 | PASS |
| 3 | 대표 이미지 존재가 실제 상호작용 상태 완결성을 가리는가 | button, enemy attack, interactable, map node는 state 누락이 실제 UX 오류로 이어질 수 있음 | `STATE_FAMILY_COMPLETENESS`와 UI/Enemy/Interactable/Item/Map/Building/Status family 추가 | Normal 한 장, enemy attack frame 한 장만 있는 반례를 대입; PARTIAL로 남는지 확인 | PASS |
| 4 | 실무 소비 조건·접근성·플랫폼 변경이 checklist에서 빠지는가 | 해상도만 적으면 aspect/stretch/import/filter/mipmap/atlas/pivot/localization 재작업이 남고, color-only cue와 stale store spec 위험이 있음 | Technical Consumption Contract, semantic redundancy, `PLATFORM_SPEC_RECHECK_REQUIRED` 추가 | Godot 2D/pixel-art와 Steam store screenshot/capsule, color-only danger state 반례로 재공격 | PASS |
| 5 | Coverage gap이 AI 이미지 자동 생산을 촉발하거나 open PR/claim boundary를 침범하는가 | “빠진 것 발견→전부 생성”으로 해석하면 기존 explicit approval와 사용자 통제권을 무너뜨림. open PR #713/#660/#678 경로도 보호 필요 | `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`; current image와 직접 관련된 범위만 확인; #713/#660/#678 소유 경로는 read-only 유지 | gap 발견→Visual Requirement→Conversation Approval 순서를 policy/Skill/template에서 재읽고 changed path를 open PR과 재비교 | PASS |

최소 5회 whole-state loop 후 새 blocking design finding은 0이다.

## Implementation Reality Gate

현재 증명 가능한 것:

- 공용 coverage guide와 연결 contract가 repository branch에 존재한다.
- coverage는 actual asset canon이 아니며 기존 requirement/approval/runtime owners와 분리된다.
- future image-generation path에서 coverage item과 state family를 확인하도록 static policy/Skill/template가 연결된다.

현재 증명 불가능한 것:

- 실제 모든 프로젝트에서 누락이 0이라는 주장.
- 이미지 생성 모델이 항상 이 checklist를 행동 수준에서 준수한다는 주장.
- 생성 이미지 품질, Notion delivery, Godot import/runtime, player readability의 PASS.
- Steam/기타 플랫폼의 미래 규격이 현재와 같다는 주장.

따라서 evidence ceiling은 `STATIC_CONTRACT_AND_FOCUSED_REGRESSION_ONLY`다.

## Concurrency review

현재 open PR 중 직접 관련된 시각 workstream을 읽기 전용으로 비교했다.

- #713: UI/visual scope & batch integrity 구현. 이번 변경은 해당 PR의 파일을 수정하지 않는다.
- #660: active surface reconciliation. 이번 변경은 `docs/DOCUMENTATION_MAP.md`를 수정하지 않는다.
- #678: proposal registry를 소유. BCP-036은 `PROPOSAL_REGISTRY.json`을 수정하지 않고 registry reconciliation을 defer한다.
- 기타 open PR도 checkout/rebase/merge/close/흡수하지 않는다.

## Final determination

`CLEAN_REVIEW_EXIT`는 **static visual asset coverage design**에만 적용한다.

다음 조건을 유지한다.

- coverage gap != image-generation approval
- coverage status != asset lifecycle
- concept/reference != gameplay/runtime evidence
- `NOT_APPLICABLE`은 정상 상태
- release platform asset은 current official spec 재조회
- 실제 프로젝트 완료 판단은 project-specific requirement/asset/runtime evidence가 필요
