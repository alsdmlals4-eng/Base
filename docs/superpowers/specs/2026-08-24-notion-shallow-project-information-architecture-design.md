# Shallow Notion Project Information Architecture Design

**Date:** 2026-08-24 KST  
**Status:** USER-APPROVED DESIGN / SPEC REVIEW PENDING  
**Baseline:** Base `3f02864b5cd04537e1c6d14d0f3bc6a65fc898a6`

## Goal

프로젝트 Notion의 탐색 깊이와 한 단계의 선택지를 줄이되, 사람용 Project Home의 정보량·학습성·교정 가능성은 줄이지 않는다.

핵심 목표는 다음이다.

```text
L0 PROJECT HUB
→ L1 HUMAN PROJECT HOME
→ L2 DOMAIN WORKSPACE
→ L3 DETAIL OR RECORD
```

일반적인 사람/AI navigation은 L3에서 끝낸다. L4+ 일반 페이지 중첩을 기본 구조로 만들지 않는다. 더 깊은 분해가 필요하면 먼저 Notion Database Record, Relation, linked/filter View, toggle, 같은 L3 문서 내부 section으로 해결할 수 있는지 검토한다.

이 구조 변경의 목적은 `페이지 수를 무조건 줄이는 것`이 아니다. 사람과 AI가 매번 거쳐야 하는 **navigation depth와 첫 선택 수를 줄이고**, 각 정보의 owner를 더 명확하게 만드는 것이다.

## Non-negotiable Human Home requirement

사용자 승인 조건을 hard requirement로 둔다.

`FULL_GAME_FLOW_VISIBLE_ON_HOME`

`CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME`

`PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME`

`HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING`

Project Home만 읽어도 사용자가 다음을 직접 볼 수 있어야 한다.

1. **전체 게임/작품 흐름**
   - 단순 Core Loop 한 줄만이 아니라, 프로젝트에 해당하는 전체 session/run/story 흐름을 보여준다.
   - 게임에 `meta/progression loop`와 `encounter/core loop`가 모두 있으면 두 흐름의 관계를 Home에서 설명한다.
   - 서사 프로젝트는 Part/장면/사건/독자 경험의 상위 흐름을 같은 역할로 사용한다.
2. **핵심 시스템과 설정**
   - 주요 시스템이 무엇인지, 서로 어떻게 연결되는지, 플레이어가 무엇을 판단하는지 Home에서 직접 설명한다.
   - 세계/설정이 핵심 시스템의 의미를 결정하면 플레이어 역할·세계 전제·핵심 갈등/목표도 Home에서 직접 볼 수 있어야 한다.
3. **프로젝트 고유 핵심 데이터 표**
   - 프로젝트마다 실제 중요한 데이터가 다르므로 범용 몬스터/경제/캐릭터 필드를 강제하지 않는다.
   - 예: Tetris의 Shared Turn Time/Line/Chain/Skill 구조, TEN_PACES의 10칸·3/3/4·상대·Route·무공 예산, Blacksmith의 강화/내구/수리/경제, OMENWARD의 Forecast/징조륜/병종/건물/20 Stage, COC-Fiction의 인물/세력/관계/사건/Part 상태.
   - Home에는 사람이 비교·학습·수정하는 대표 값과 관계를 직접 보여준다.
   - 전체 raw dataset은 L3/Database/GitHub owner를 유지한다.
4. **현재 Visual/UX 방향과 승인된 주요 Visual anchor**
5. **AI가 이해한 핵심**과 사용자가 이를 고치는 방법
6. **현재 구현·검증 상태와 evidence ceiling**
7. **현재 blocker/다음 작업/중요한 위험**

Home에서 핵심 정보를 `자세한 내용은 하위 페이지 참조`로 대체하는 것은 실패다. 하위 페이지는 **더 자세히 보기**이지 **처음 이해하기 위해 반드시 열어야 하는 페이지**가 아니다.

## Current-state findings

### Already correct and preserved

현재 Base의 `HUMAN_HOME_SELF_CONTAINED_POLICY.md`는 이미 다음을 소유한다.

- `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`
- `PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED`
- `PROJECT_SPECIFIC_CORE_DATA`
- `AI_INTERPRETATION_FOR_USER_CORRECTION`
- `HUMAN_EDIT_GUIDE_REQUIRED`
- `HOME_PROJECTION_IS_NOT_DUPLICATE_CANON`
- Human Home / AI-System metadata 물리 분리

따라서 이번 개편은 Home을 다시 얇게 만들거나 새 Human Home schema를 만드는 작업이 아니다.

### Navigation problem

현재 `00 · 프로젝트 허브`는 각 프로젝트의 dedicated Human Home으로 바로 진입한다. 이 L0→L1 구조는 유지한다.

문제는 L1 이후다. 예를 들어 Tetris Home에는 작업계획·Visual Bible·UI/전투 Flow·Asset·Reference·Production·세계관·핵심 시스템·대표 전투·Audio·First Run·Production Lock·Final Audit·이미지 패키지 등 많은 상세 페이지가 같은 계층의 첫 선택지로 노출된다.

이는 `깊이`만의 문제가 아니라 **한 레벨의 선택 폭이 너무 커지고, owner 관계가 이름/번호에 의존하는 문제**다.

### Downstream contract problem

`NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md`는 현재 `08 · 핵심 시스템 · 상세`을 GAME Project Home의 직접 상세면으로 명시한다. 이 detail view 자체는 유지 가치가 있지만, 특정 번호/직접-child 위치를 공용 계약으로 고정하면 새 Domain Workspace 구조와 충돌한다.

공용 계약은 `Core System detail/linked view가 존재하고 exact Project로 필터된다`를 요구해야 하며, 해당 detail이 Home 직속 `08`이어야 한다고 강제하지 않는다.

### Implementation capability

현재 연결된 Notion 도구는 page/database의 **physical move/reparent**를 지원한다. 따라서 링크만 새로 만든 가상 폴더가 아니라 실제 page tree를 L2 Domain 아래로 재구성할 수 있다.

다만 migration 전에는 page ID/mention/linked view/child block/Project relation을 읽고, 이동 후 destination readback으로 실제 결과를 검증한다. connector readback만으로 pixel width/crop/mobile geometry까지 검증됐다고 주장하지 않는다.

## Benchmark and professional evidence

### Notion

Notion은 동일 Database를 여러 View로 보여주고 각 View마다 filter/sort/group/property visibility를 다르게 설정할 수 있다. 따라서 같은 데이터를 여러 하위 페이지에 복제하기보다 Human Home/L2에서 **linked project-filtered projection**으로 보여주는 구조가 적합하다.

- `https://www.notion.com/help/views-filters-and-sorts`

Notion 자체는 무한 page nesting을 허용하지만, 가능 여부와 권장 IA는 다르다. 이번 계약은 기술적 한계를 흉내내는 것이 아니라 현재 프로젝트 규모에서 탐색 비용을 줄이기 위한 운영 제한이다.

- `https://www.notion.com/help/intro-to-workspaces`

### Atlassian / Confluence

Confluence의 knowledge organization guidance는 related content를 parent 아래 그룹화하되 **hierarchy를 shallow하게 유지해 complex navigation을 피하는 것**을 best practice로 제시한다.

- `https://community.atlassian.com/learning/lesson/organize-confluence-space-content`

### GitLab Handbook

GitLab Handbook은 Information Architecture에서 repetition을 줄이고 **Single Source of Truth**를 유지하며, 관점을 달리 보여줄 때 content를 복제하기보다 cross-link하라고 권장한다. Duplicate content는 여러 위치를 갱신하고 stale copy를 기억해야 하는 비용을 만든다.

- `https://handbook.gitlab.com/handbook/about/handbook-usage/`

### Game design documentation

Stone Librande의 One-Page Design 사례는 긴 GDD/Wiki가 핵심 관계를 분산시키는 문제를 해결하기 위해 전체 핵심 관계를 한눈에 이해할 수 있는 diagram/flow/matrix를 사용한다. 동시에 모든 내용을 한 페이지에 억지로 cram하는 것도 실패라고 지적한다.

- `https://www.gamedeveloper.com/design/video-one-page-designs`

SimCity production 사례에서는 one-page communication이 production 전반에서 유용했지만 복잡한 시스템은 spreadsheet/상세 자료가 추가로 필요했다. 즉 **강한 overview + 상세 owner**의 2층 전략이 실제 복잡한 게임 제작과 맞는다.

- `https://www.gamedeveloper.com/design/pushing-the-limits-in-simulating-a-city-one-page-at-a-time`

## Approaches considered

### A. Fixed universal 5-folder taxonomy

모든 프로젝트를 아래 5개 L2로 강제한다.

```text
Planning
Design
Visual
Production
Reference
```

**장점:** 매우 단순하고 교육하기 쉽다.  
**단점:** Narrative, management, strategy, exploration 프로젝트의 핵심 문법이 사라지고 분류를 맞추기 위한 억지 이동이 생긴다.  
**Verdict:** `REJECT_AS_STRICT_SCHEMA`.

### B. Common 4-layer architecture + project-specific L2 domains — selected

L0/L1/L2/L3의 역할은 공통으로 고정하되, L2 Domain 이름과 조합은 프로젝트 특성에 맞춘다.

공통 starting skeleton은 다음이다.

```text
Direction · Planning
Design · Canon · Data
Visual · UX · Assets
Production · Validation
Reference · Benchmark
Optional: Content · World
```

프로젝트당 **4~6개 L2 Domain**을 권장하고, 필요하지 않은 Domain은 만들지 않는다. 같은 책임이 자연스럽게 합쳐지면 4개까지 줄이고, 의미가 실제로 분리되는 경우에만 6개까지 허용한다.

**장점:** 탐색 일관성과 프로젝트 특수성을 동시에 보존한다.  
**단점:** 초기 migration inventory와 per-project mapping이 필요하다.  
**Verdict:** `ADOPT`.

### C. Fully flat DB-first workspace

Home 아래 일반 detail page를 거의 없애고 모든 자료를 Master DB Record/View로 만든다.

**장점:** nesting과 duplicate page가 최소다.  
**단점:** 초보 사용자에게는 DB schema가 먼저 보이고, Visual Bible/Flow/대표 Encounter 같은 문서형 정보를 억지로 record화할 수 있다.  
**Verdict:** `REJECT_AS_DEFAULT`; L3 내부 구현 패턴으로만 사용한다.

## Target architecture

### L0 — PROJECT HUB

역할은 **프로젝트 선택** 하나다.

```text
00 PROJECT HUB
→ Project A Home
→ Project B Home
→ ...
→ Base Home
```

- 상세 AI metadata를 노출하지 않는다.
- 프로젝트 상태를 장황하게 복제하지 않는다.
- 프로젝트의 Human Home을 first-click destination으로 유지한다.

### L1 — HUMAN PROJECT HOME

사람이 프로젝트 전체를 이해·판단·교정하는 메인 설계서다.

Home은 아래 정보를 직접 보유한다.

```text
Project promise / one-line definition
→ Player experience / value
→ Full game/session/story flow
→ Core encounter/interaction loop
→ Core systems + system relationships
→ Setting / player role / core conflict when relevant
→ Project-specific core data tables / linked filtered views
→ UX/UI/Visual direction + approved anchors
→ AI interpretation for user correction
→ Human edit guide
→ Implementation / validation state
→ Blockers / next work
→ Important decisions / risks / revisit conditions
→ 4~6 L2 Domain drilldowns
```

**Home richness is protected.** IA simplification may not move the items above out of Home merely to make the page shorter.

### L2 — DOMAIN WORKSPACE

AI가 주로 작업하지만 사람이 열어도 이해 가능한 **책임 단위**다.

L2는 empty folder page가 아니다. 각 Domain page는 최소한 다음을 가진다.

- Domain 목적/범위
- 이 Domain이 소유하는 current authority와 Human Home projection 관계
- 현재 주요 상태/결정/위험
- 주요 L3 detail 또는 project-filtered linked view
- 관련 GitHub/Notion owner locator

Domain은 프로젝트에 맞춰 이름을 바꾼다.

예: Tetris

```text
01 Direction · Planning
02 Combat Design · Data
03 Visual · UX · Assets
04 Production · Validation
05 Reference · Benchmark
```

예: TEN_PACES

```text
01 Direction · Planning
02 Combat · Martial Arts · Route
03 Visual · UX · Assets
04 Opponents · World · Content
05 Production · Validation
06 Reference · Benchmark
```

예: Blacksmith

```text
01 Direction · Planning
02 Enhancement · Durability · Economy
03 Item Life · Customer · Content
04 Visual · UX · Assets
05 Production · Validation
06 Reference · Benchmark
```

예: COC-Fiction

```text
01 Direction · Planning
02 Story · Canon · Events
03 Characters · Factions · World
04 Visual · Storyboard · Assets
05 Production · Continuity · Validation
06 Reference · Benchmark
```

이 예시는 taxonomy owner가 아니라 migration starting map이다. 실제 inventory 결과에 따라 의미가 겹치면 합친다.

### L3 — DETAIL OR RECORD

한 시스템·한 문서·한 dataset/view·한 atomic record를 책임지는 terminal navigation layer다.

예:

```text
Combat Design · Data
→ Turn System
→ Line System
→ Chain System
→ Skill System
→ Gatebreaker Encounter
→ Balance Budget
```

또는:

```text
Visual · UX · Assets
→ Visual Bible
→ UI / Combat Flow
→ Asset Library
→ Audio Bible
→ Image Production Package
```

Database를 사용하는 경우 L3 page/record가 terminal navigation node다. Relation으로 다른 L3 record를 연결할 수 있지만 이를 L4 page-tree navigation으로 다시 확장하지 않는다.

### L4+ — AVOID NORMAL PAGE NESTING

`L4+ NORMAL_PAGE_NESTING = AVOID_BY_DEFAULT`

예외는 다음과 같다.

- Notion Database Record 내부 block/section
- relation으로 연결된 다른 terminal record
- import/archive provenance를 보존하기 위한 비활성 historical container
- 외부 도구가 기술적으로 생성하지만 사람이 정상 탐색 경로로 사용하지 않는 implementation detail

예외를 current human/AI navigation으로 승격하려면 `왜 L3로 표현할 수 없는가`가 설명돼야 한다.

## Global AI/System surfaces

`90 · SYSTEM MASTERS`, Project Registry, cross-project Master DB는 프로젝트 Human navigation tree와 별도 infrastructure로 유지한다.

이들은 L4+를 허용하는 loophole이 아니다. Project L2/L3에서는 exact `Project` relation으로 filter한 view/record를 연결한다.

```text
Human navigation
PROJECT HUB → HOME → DOMAIN → DETAIL

AI/System infrastructure
SYSTEM MASTERS / Registry / shared DB
       ↑ project-filtered relation/view
DOMAIN / DETAIL
```

GitHub repository는 계속 structured data/code/scene/resource/test/runtime truth를 소유한다.

## Home projection and SSoT

Home의 rich information은 별도 canon 복제가 아니다.

### Preferred

- linked project-filtered View
- summary table derived from current owner
- approved Visual anchor
- current semantic summary + canonical locator

### Avoid

- raw dataset 전체 복사
- exact SHA/PR/CI 값을 current Home prose에 장기 고정
- 동일 rule table을 Home/L2/L3 세 곳에 독립 편집 가능한 형태로 복제
- detail link만 남기고 Home 설명 제거

Home 변경이 structured/runtime 의미를 바꾸면 기존 `SYNC_BEFORE_IMPLEMENTATION`을 그대로 따른다.

## Migration algorithm

각 프로젝트를 다음 순서로 처리한다.

### Phase 0 — Inventory only

Home 아래 현재 page tree와 linked DB/view를 recursive read한다. 모든 item을 다음 중 하나로 분류한다.

```text
KEEP_INLINE_ON_HOME
L2_DOMAIN
L3_DETAIL
DB_RECORD_OR_VIEW
AI_SYSTEM_INFRASTRUCTURE
HISTORICAL_RETAIN
DUPLICATE_CONSOLIDATE
OBSOLETE_REVIEW
```

분류 전에는 page를 이동/삭제하지 않는다.

### Phase 1 — Target mapping

프로젝트별 `current → target` mapping을 만든다.

각 기존 page에는:

- current parent
- current role
- target L2 Domain
- target L3 role
- source/canon owner
- duplicate/stale status
- move risk
- linked view/relation dependencies

를 기록한다.

### Phase 2 — Domain creation

실제 content가 있는 Domain만 L2에 만든다. 빈 folder page를 만들지 않는다.

L2 page 자체에는 Domain summary + current state + L3 index/view가 있어야 한다.

### Phase 3 — Physical move/reparent

`notion-move-pages`를 사용해 existing page ID를 가능한 한 유지한 채 target Domain 아래로 물리 이동한다.

- 이동 전 source fetch
- 이동
- destination fetch/readback
- parent/path 확인
- mention/link/view/Project relation 확인

검증 실패 시 다음 move를 진행하지 않고 해당 프로젝트를 `MIGRATION_REVIEW_REQUIRED`로 둔다.

### Phase 4 — Home rewire

Home의 `작업면`은 4~6개 L2 Domain을 기본 drilldown으로 보여준다.

동시에 Home의 전체 게임 흐름·핵심 시스템/설정·핵심 데이터 표·Visual·AI 이해·수정 방법·현재 상태는 그대로 유지하거나 더 명확하게 만든다.

### Phase 5 — Duplicate/stale cleanup

- current duplicate는 one owner + projection/link로 통합한다.
- historical information은 current처럼 보이지 않게 상태를 명시한다.
- obsolete content는 unique information이 없는지 확인하기 전 삭제하지 않는다.
- physical deletion/trash가 필요한 경우 기존 deletion gate를 따른다.

### Phase 6 — Readback and regression

각 프로젝트에서:

```text
Hub → Home
Home full flow visible
Home core systems/settings visible
Home core data tables visible
Home → 4~6 Domain
Domain → L3 detail/record
normal L4+ navigation absent
Project relation/filter preserved
AI/System metadata excluded from Home
runtime/Human evidence ceiling preserved
```

를 readback한다.

## Rollout strategy

### 1. Base contract first

새 broad Skill을 만들지 않는다. 기존 owner를 확장한다.

Expected owner set:

- `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- `docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md`
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- `skills/managing-design-documents/SKILL.md`
- 필요 시 `skills/building-project-visual-dashboards/SKILL.md`
- focused regression tests

정확한 파일 목록은 implementation plan에서 current main을 다시 읽고 최소화한다.

### 2. Tetris pilot

현재 breadth가 큰 Tetris를 pilot로 사용한다.

목적은 game-specific content를 바꾸는 것이 아니라:

- 14개 수준의 first-choice detail을 4~6 Domain으로 줄이는지
- Home richness가 유지되는지
- physical move 이후 existing links/views가 유지되는지
- `08` 등 numbered direct-child assumption을 제거해도 consumer가 정상인지

를 검증하는 것이다.

Pilot이 clean이면 별도 승인 없이 같은 승인 범위로 보호되지 않은 프로젝트에 연속 rollout한다.

### 3. Fleet rollout

모든 프로젝트에 동일 taxonomy를 복사하지 않고 project-specific mapping을 적용한다.

현재 다른 작업선이 active인 프로젝트는 read-only다. 예를 들어 migration 시점에 COC-Fiction 또는 GRIMOIRE의 active PR/Notion 작업이 계속 존재하면 해당 프로젝트는 `DEFERRED_ACTIVE_WORKSTREAM`으로 남기고, 그 작업이 main에 완료된 뒤 fresh inventory에서 이어간다. 사용자가 특정 active PR에 별도 takeover/exception authority를 주지 않는 한 진행 중 작업을 재배치하지 않는다.

### 4. Final fleet audit

10개 active project 모두:

- dedicated Human Home
- Home self-contained acceptance
- 4~6 Domain 또는 정당화된 더 작은 수
- terminal L3 detail/record
- no normal L4+ navigation
- current Project relation/filter
- post-move readback

을 충족해야 fleet migration 완료로 판정한다.

## Testing and verification

### Repository regression

최소 다음을 machine-readable/static contract로 검증한다.

```text
SHALLOW_BY_DEFAULT
L0_PROJECT_HUB
L1_HUMAN_PROJECT_HOME
L2_DOMAIN_WORKSPACE
L3_DETAIL_OR_RECORD
L4_PLUS_NORMAL_PAGE_NESTING_AVOID_BY_DEFAULT
FULL_GAME_FLOW_VISIBLE_ON_HOME
CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME
PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME
HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING
NO_DUPLICATED_CANON
NO_FIXED_UNIVERSAL_GAME_TAXONOMY
```

기존 Human/System separation, Project relation, approved visual delivery/readback, zero-incremental-cost tests를 약화하지 않는다.

### Live Notion verification

CI만으로 live Notion tree를 PASS 처리하지 않는다. 실제 connector readback으로 parent path, child/domain mapping, Home content, linked view/filter, Project relation을 확인한다.

### Evidence ceilings

이번 IA migration으로 증명되지 않는 것:

- 게임 runtime correctness
- Windows/Android/device validation
- Human 재미/가독성/usability
- Notion desktop/mobile pixel geometry
- visual asset quality

해당 상태는 기존 evidence를 그대로 유지한다.

## Adversarial review requirements

구현 전/후 각각 동일 전체안을 최소 5회 다시 검토한다.

각 loop는 특정 관점 하나가 아니라 다음 전체를 다시 본다.

- user intent / Home richness
- navigation simplicity
- project-specific fit
- SSoT / duplicate drift
- Human vs AI/System boundary
- Project isolation/relation
- current GitHub/Notion owner
- active PR/workstream collision
- Visual/asset implications
- implementation feasibility
- migration rollback/readback
- cost
- evidence ceiling

문제가 발견되면 수정한 뒤 다음 loop에서 수정된 전체안을 처음부터 다시 검토한다. 최소 5회 이후에도 unresolved issue가 있으면 clean할 때까지 계속한다.

## Rollback and safety

- migration 동안 content를 먼저 삭제하지 않는다.
- move 전 source path/page IDs를 inventory에 기록한다.
- move 후 destination readback 실패 시 해당 프로젝트의 다음 move를 중지한다.
- L2 Domain 자체가 잘못된 경우 page ID를 유지한 채 원래 Home 또는 corrected Domain으로 reparent한다.
- GitHub Base 변경은 별도 PR 하나로 묶고 exact-head validation 후 merge한다.
- 진행 중 project PR/branch는 사용자 명시 예외 없이 수정하지 않는다.

## Acceptance criteria

완료 조건은 `페이지가 적어 보임`이 아니라 다음이다.

1. Project Hub에서 project 선택 시 dedicated Human Home으로 바로 진입한다.
2. **Home에서 전체 게임/작품 흐름을 직접 볼 수 있다.**
3. **Home에서 핵심 시스템과 핵심 설정/플레이어 역할을 직접 볼 수 있다.**
4. **Home에서 프로젝트 고유 핵심 데이터 표 또는 linked filtered projection을 직접 볼 수 있다.**
5. Home에는 AI/System raw metadata가 기본 노출되지 않는다.
6. Home의 핵심 이해를 detail link로 대체하지 않는다.
7. 각 Project Home의 첫 drilldown 선택은 원칙적으로 4~6개 L2 Domain이다.
8. L2 Domain은 empty folder가 아니라 책임·상태·L3 index/view를 가진다.
9. 정상 navigation은 L3 Detail/Record에서 끝난다.
10. L4+ 일반 page nesting은 없거나 명시적 예외 사유가 있다.
11. 동일 canon/data의 독립 복제를 만들지 않는다.
12. shared Master/Registry는 AI/System infrastructure로 유지하고 project-filtered relation/view로 연결한다.
13. project-specific data/terminology를 universal template 때문에 잃지 않는다.
14. active concurrent workstream은 보호된다.
15. Notion write/move마다 destination readback이 있다.
16. Base regression + live Notion verification + 전체 적대적 검토 최소 5회 clean exit가 있다.
17. 모든 미검증 runtime/device/Human/UI geometry 상태는 과장 없이 `NOT_RUN`/appropriate ceiling을 유지한다.

## Expected effect

### Before

```text
Hub
→ rich Home
→ 많은 번호형 detail이 같은 레벨에 병렬 노출
→ detail 안에서 다시 detail/history/view로 이동
```

사용자와 AI가 `어느 페이지가 어떤 책임을 갖는지`를 페이지 번호와 기억에 의존한다.

### After

```text
Hub
→ rich Home
→ 4~6 project-specific Domain
→ terminal Detail/Record
```

Home에서 전체 프로젝트를 이해하고, 더 자세한 작업은 의미가 분명한 Domain을 통해 들어간다. 데이터 원본은 하나를 유지하며 Home/Domain에서는 적절한 projection/view를 사용한다.

장기 기대효과는 다음이다.

- navigation depth 감소
- first-choice overload 감소
- 새 page 폭증 억제
- stale duplicate 감소
- AI routing/owner 판정 단순화
- 사용자 학습·교정 속도 향상
- 프로젝트별 고유 시스템/데이터 표현 보존
- Notion 구조가 커져도 Home의 전체 게임 이해 기능 유지
