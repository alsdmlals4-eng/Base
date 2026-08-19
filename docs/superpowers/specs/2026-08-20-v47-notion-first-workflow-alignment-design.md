# v4.7 Notion-First Workflow Alignment Design

**Date:** 2026-08-20 KST  
**Status:** USER-APPROVED / REUSED_APPROVAL  
**Baseline:** Base `61862f9a4f7995f1676acca4bb6d5365e46b7630`

## Goal

Base와 프로젝트 작업지시문 v4.7을 같은 방향으로 정렬한다. 최신 사용자 결정은 다음과 같다.

```text
GPT Pro
→ GitHub + exact Project Notion 전체 상태 복원
→ 큰 방향·핵심 재미·세계관/핵심 스토리라인·Core Loop 설계
→ 현행 조사 + 최소 3개 실질 대안 + benchmark/실무/성공·실패 사례
→ Grill Me로 중요한 방향 승인
→ 세부 기획·데이터·BALANCE_BUDGET는 GPT 권장안
→ 필요 시 기획 이미지/시각화 생성 → exact Project Notion 배치/readback
→ 최종 기획·검수
→ 구현이 필요할 때 fresh PowerShell one-block → project Codex/Godot execution
→ release-near Vertical Slice
→ 최소 5회 전체 적대적 개선 루프, 이후 clean까지
→ exact-head PR/merge/postmerge readback
→ 사건·해결·교훈의 project/Base promotion
→ REQUIRED_WORK_REMAINING = 0
```

## Current authority findings

### Already strong and preserved

Current Base already owns:

- `CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY`.
- `MINIMUM_VIABLE_ALTERNATIVES: 3`.
- `BETTER_ALTERNATIVE_SEARCH`.
- `LONG_TERM_PLAN_FIT_REQUIRED`.
- `EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD`.
- `ADVERSARIAL_REVIEW_UNTIL_CLEAN`, minimum 5 full loops.
- `RELEASE_NEAR_VERTICAL_SLICE_FIRST`.
- `BALANCE_BUDGET`.
- `WORLD_STORYLINE_FIT_REQUIRED`.
- `REUSABLE_SYSTEM_EXTRACTION`.
- `NOTION_DEFAULT_PROJECT_WORKSPACE`.
- `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`.
- `EXTERNAL_HTML_WORKSPACE_RETIRED`.
- `LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT`.
- `REQUIRED_WORK_REMAINING: 0`.
- active workstream isolation based on current-owner evidence, not PR-open state alone.
- beginner-safe one-copy/paste PowerShell with location-first and error-stage markers.

These are not reimplemented as new Skills.

### Validated stale/conflicting consumers

1. `START_HERE.md` still advertises Tool Hub and QA Evidence Studio as active/default operational routes even though the retirement policy and long-horizon policy retire local project-management surfaces.
2. `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md` still says Tool Hub runtime should be preferred when registered, contradicting the latest user decision not to use Tool Hub.
3. `docs/OPERATING_MODEL.md` still describes game GDD Google Sheets as `USER_FACING_GDD_WORKSPACE`, contradicting the current Notion-first / Sheet migration-only policy.
4. `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md` retains QA Evidence Studio as an active specialist utility; latest user decision removes it from the active project path.
5. PR #555 merged a reusable module catalog whose `RM-TOOL-004` still routes runtime/UI evidence capture to QA Evidence Studio. That module needs a repository-native replacement contract rather than a dedicated capture app.
6. Current reverse-engineering logic has `NOVELTY_DELTA`, but the latest planning instruction asks to explicitly judge **originality / fun / creativity** and keep searching for best-in-class references until decision time. This should be made visible as a reusable benchmark frontier, not inferred from novelty alone.

## Three materially distinct approaches

### A. New broad `v47-project-production` Skill

Create a new Skill that owns planning, Notion, benchmark, visuals, Codex handoff, PR, retirement, learning and postmerge.

**Pros:** one visible entrypoint.  
**Cons:** duplicates P01/P03/P04/P05/P06/P08/P09 owners, increases routing ambiguity, conflicts with consolidation-first.  
**Verdict:** `REJECT`.

### B. Existing-owner absorption + stale consumer correction — selected

Preserve current owners and change only stale/insufficient consumers:

- entrypoint routing,
- long-horizon clarifications,
- PowerShell Tool Hub priority removal,
- retirement policy,
- operating-model Sheet authority,
- reuse module replacement,
- creative benchmark frontier,
- focused regression.

**Pros:** smallest authority change, low long-term maintenance, current Base updates remain dynamic.  
**Cons:** rules remain distributed by semantic owner, so discoverability must be tested.  
**Verdict:** `ADOPT`.

### C. Instruction-only v4.7, no Base change

Leave Base unchanged and put all latest decisions only in the project instruction file.

**Pros:** lowest immediate repository work.  
**Cons:** Base entrypoints would continue to suggest retired surfaces; future projects could drift from v4.7.  
**Verdict:** `REJECT`.

## Benchmark / professional evidence

- Google Engineering Practices recommends small, self-contained changes with related tests because they are easier to review, reason about, merge and roll back: `https://google.github.io/eng-practices/review/developer/small-cls.html`.
- Volition's GDC *The Vertical Slice Challenge* treats the slice as a gate proving both what the team is making and whether it knows how to make it: `https://www.gdcvault.com/play/1022329/Inside-Unity-5-Engine-Architecture`.
- Firaxis' *Play Early, Play Often* describes rapid playable prototyping while also noting missing interface widgets and art delayed by prototype as lessons: `https://gdcvault.com/play/1013284/Play-Early-Play-Often-Prototyping`.
- Bit Reactor's GDC 2024 art-direction session emphasizes clear pre-production evaluation points and art documentation before production: `https://gdcvault.com/play/1034593/Art-Direction-Summit-Pre-Production`.
- Giant Sparrow's *Weaving 13 Prototypes into 1 Game* is a useful creativity benchmark: radically different mechanics were prototyped, discarded and blended into one coherent experience instead of copying one successful template: `https://gdcvault.com/play/1025016/Weaving-13-Prototypes-into-1`.
- Subset Games' FTL postmortem starts from a target player feeling and lets mechanics/genre change around that goal, supporting player-experience-first rather than feature-first design: `https://www.gdcvault.com/play/1019036/Designing-Without-a-Pitch-FTL`.
- Godot's current multiple-resolution guidance supports design-size + `expand` + anchors/containers for multi-aspect UI rather than pixel-identical layouts: `https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html`.
- Notion databases support project-filtered views and pages with images/files, which fits the existing human-facing project workspace model without introducing another visual management app: `https://www.notion.com/help/intro-to-databases`.

## Creative Benchmark Frontier

Important game-design decisions use a multi-source creative frontier rather than a single genre benchmark.

```text
DIRECT_GENRE_BEST_IN_CLASS
+ ADJACENT_GENRE_BEST_IN_CLASS
+ DISTINCTIVE_OR_INNOVATIVE_WORK
+ FAILURE_OR_MIXED_CASE
+ PROJECT_INTERNAL_STRENGTH
→ transferable principles
→ recombination candidates
→ originality/fun/creativity attack
→ project-specific synthesis
```

Evaluation fields:

```yaml
creative_frontier:
  player_promise:
  best_in_class_sources: []
  adjacent_sources: []
  innovative_sources: []
  failure_or_mixed_sources: []
  strengths_to_absorb: []
  expressions_not_to_copy: []
  originality_delta:
  fun_hypothesis:
  creativity_recombination:
  core_loop_fit:
  world_story_fit:
  production_cost:
  long_term_fit:
  revisit_conditions: []
```

`fun_hypothesis` is a design hypothesis until real player evidence exists. Popularity or awards do not prove project fit.

## Tool and workspace authority after alignment

```text
ACTIVE DEFAULT
GPT Pro                     planning/research/review
Notion                      human-facing Project Home/visual/assets/flows/tables
GitHub repository           structured data/code/assets/tests/runtime evidence
PowerShell + Codex          implementation executor when repository/runtime mutation is needed
Godot + HiGodot/GUT/Hera    current project-adopted authoring/test/live-QA boundaries
Loop Engineering            bounded execution/control plane when relevant and current evidence says fit

RETIRED FROM ACTIVE PROJECT FLOW
Figma
external HTML workspace/catalog/dashboard
Google Sheets after one-time migration
project-management Tool Hub
QA Evidence Studio
Expression/Sprite localhost management surfaces
```

Retired code/history is not automatically deleted in this patch. It becomes non-default historical/rollback material, with unique reusable concepts absorbed first. Physical removal is a separate bounded retirement task if active consumers reach zero and deletion is safe.

## Workstream isolation

A branch/path explicitly identified by the user as being worked on in another chat is `ACTIVE_OTHER_WORKER` even if GitHub metadata later changes. It is read-only until explicit handoff/takeover. Open PR state alone is not sufficient owner evidence.

## Project planning and visuals

After understanding a project, create a `PROJECT_VISUALIZATION_NEED_MAP` before implementation:

```yaml
visualization_need:
  project:
  planning_question:
  needed_artifact:
  why_visual_needed:
  target_notion_surface:
  source_decisions:
  implementation_consumer:
  approval_state:
```

Generate only visuals that improve planning, UX/UI understanding, world/story consistency, implementation handoff or demo quality. Attach to the exact Project in Notion and read back. Images remain planning/asset evidence, not runtime proof.

## Data and balance

For core-loop systems, detailed numeric data defaults to a reversible `BALANCE_BUDGET` rather than hard-coded final truth.

```text
core-loop system inventory
→ parameter budget / relative weights / caps
→ dummy-but-coherent test values
→ build/runtime technical validation
→ release-near slice
→ player evidence
→ tuning
```

Project-specific budget examples such as martial-arts budgets remain project-owned; Base owns only the budgeting pattern.

## Story and world

Each game project identifies a world/story backbone that makes the core loop meaningful. It need not be a linear campaign, but must define enough world premise, player role, conflict/question and consequence structure to stop mechanics, visuals and content from becoming thematically disconnected.

## Completion report for user learning

Every material Base/project completion report teaches the system, not just status.

```text
part / responsibility
→ why it exists
→ core rules
→ core Skills and when they trigger
→ core modules: input → processing → output
→ what was merged/absorbed/removed/intentionally kept separate
→ BEFORE → AFTER
→ expected long-term effect
→ trade-offs / evidence ceiling
→ remaining risks and revisit conditions
```

## Acceptance

- no active/default Tool Hub or QA Evidence Studio routing from current entrypoints;
- Google Sheets is migration-only, not current user-facing GDD authority;
- Loop Engineering remains available without depending on Tool Hub or QA Studio;
- creative benchmark frontier and originality/fun/creativity judgment are explicit;
- active-other-chat branch/path is protected by user owner evidence;
- existing 3-alternative, long-term fit, 5-full-loop, balance-budget, world-story, Notion, release-near slice and remaining-work-zero contracts remain intact;
- focused regression is consumed by CI;
- no new broad Skill is created.

## Rollback

Revert the eventual squash merge as one unit. Retired tools are not physically deleted by this alignment patch, so rollback does not require reconstructing tool code.