# Shallow Notion Project Information Architecture Design

**Date:** 2026-08-24 KST  
**Status:** USER-APPROVED / IMPLEMENTATION AUTHORIZED  
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
→ Core System detail
→ Representative Encounter
→ Balance table
```

또는:

```text
Visual · UX · Assets
→ Visual Bible
→ UI Flow
→ Asset Library
→ Character/Enemy DB Record
```

L3에서 더 세분화가 필요할 때 새 일반 child page를 만드는 대신 다음을 우선한다.

1. database record
2. relation / linked view
3. toggle / section
4. 기존 L3 owner 안의 structured table
5. 위 방식으로 책임 분리가 불가능할 때만 `L4_EXCEPTION_REVIEW_REQUIRED`

### L4+ exception

`L4_EXCEPTION_REVIEW_REQUIRED`

다음 조건을 모두 만족할 때만 예외다.

- 별도 owner가 실제로 필요함
- DB Record/Relation/View/section으로 표현하면 책임이 더 모호해짐
- 해당 깊이가 사람 기본 navigation에는 노출되지 않음
- rollback/migration 비용보다 명확성 이득이 큼

즉 L4+를 기술적으로 금지하는 것이 아니라 **일반 navigation 기본값에서 제외**한다.

## Migration design

### 1. Inventory first

각 프로젝트마다 먼저 현재 child page/DB/view inventory를 만든다.

```text
CURRENT PAGE
→ responsibility
→ UNIQUE / DUPLICATE / STALE / HISTORICAL
→ target L2 Domain
→ target L3 owner
→ Home projection needed?
→ move / merge / keep / archive
```

### 2. No destructive bulk rewrite

- page를 삭제하지 않고 이동/재분류를 먼저 한다.
- 기존 child page/DB를 전부 `replace_content`해서 재작성하지 않는다.
- 물리 move 전 target Domain과 rollback parent를 기록한다.
- move 후 Home/Domain/Detail을 fetch하여 ancestor path와 content를 readback한다.

### 3. SSoT cleanup during move

Migration에서 발견한 중복은 다음처럼 처리한다.

```text
current owner 확정
→ Home에는 human summary/projection
→ L2에는 domain summary/current status
→ L3/DB에는 detail/raw owner
→ old duplicate current text는 historical label 또는 제거
```

현재 mutable 값(SHA/PR/current test count)을 여러 페이지에 복제하지 않는다.

### 4. Home acceptance gate before and after move

각 프로젝트마다 migration 전후 다음 표를 비교한다.

```text
Full Game/Story Flow on Home           YES/NO
Core Systems on Home                   YES/NO
Setting/Player Role/Core Conflict      YES/NO or NOT_APPLICABLE_WITH_REASON
Project-specific Core Data Table       YES/NO
Approved Visual Anchors                PRESENT/WAITING/NOT_APPLICABLE
AI Interpretation                      YES/NO
Human Edit Guide                       YES/NO
Implementation/Validation Ceiling      YES/NO
L2 Domain Count                         4..6 preferred
Normal Navigation Depth                 <= L3
```

하나라도 Home core requirement가 퇴행하면 migration을 완료로 판정하지 않는다.

## Tetris pilot

Tetris를 첫 migration으로 사용한다. 현재 detail page가 많고 Visual/Flow/Core/Data/Production이 모두 있어 정보 architecture를 검증하기에 적합하다.

초기 target:

```text
Tetris Home
├ 01 · Direction · Planning
│  ├ 프로젝트 전체 작업계획
│  ├ Production Content Lock
│  └ Final Planning Audit
├ 02 · Combat Design · Data
│  ├ 핵심 시스템
│  ├ 대표 전투
│  ├ First Run Flow
│  └ 세계관/전투 설정
├ 03 · Visual · UX · Assets
│  ├ Visual Bible
│  ├ UI · Combat Flow
│  ├ Asset Library
│  ├ Audio Bible
│  └ 이미지 제작 패키지
├ 04 · Production · Validation
│  └ Production / Handoff
└ 05 · Reference · Benchmark
```

Pilot acceptance:

- Home의 direct drilldown choice가 4~6개 Domain으로 줄어듦
- Home 전체 Flow/시스템/설정/핵심 데이터는 유지 또는 개선
- 기존 child page는 손실 없이 L3로 이동
- existing mention/link와 project-filtered view가 정상 resolve
- L4+ normal nesting 없음
- duplicate/stale current text를 새 구조로 그대로 운반하지 않음

Pilot이 실패하면 fleet migration을 중단하고 rollback/mapping을 교정한다.

## Fleet rollout

Tetris pilot clean 이후 나머지 프로젝트를 **각 프로젝트 current inventory에 맞춰 순차 이동**한다.

예상 순서:

```text
Tetris pilot
→ TEN_PACES
→ Blacksmith
→ Omenward
→ GRIMOIRE
→ Switchy Express
→ 괴이기록국
→ 닌자 서바이벌
→ 마이 리틀 보트
→ COC-Fiction
```

순서는 current open PR/active owner에 따라 바꿀 수 있다. 구조 migration 중에도 진행 중 project PR은 기본 read-only다. Branch-only content를 새 current Home/L2/L3 정본처럼 승격하지 않는다.

## Base contract changes

새 broad Skill을 만들지 않는다. 기존 owner만 정렬한다.

Expected Base consumers:

- `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
  - full flow/system/setting/core-data Home requirements 강화
  - Home richness 보호
- `docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md`
  - L0/L1/L2/L3 navigation contract
  - `08 · 핵심 시스템 · 상세` direct-child 고정 제거
  - move/reparent/readback/rollback rule
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
  - machine-readable navigation layers/depth/domain policy
- `docs/DOCUMENTATION_MAP.md`
  - project Notion standard를 direct 01~07+ sibling list에서 Domain grouping으로 갱신
- `tests/test_human_home_self_contained_contract.py`
- `tests/test_notion_human_system_surface_separation.py`

`managing-design-documents`는 이미 Human Home owner policy와 workspace authority를 소비한다. 실제 테스트에서 consumer gap이 재발하지 않는 한 추가 Skill 변경을 기본값으로 만들지 않는다.

## Verification

### Base static contract

Required assertions:

```text
FULL_GAME_FLOW_VISIBLE_ON_HOME
CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME
PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME
HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING
SHALLOW_BY_DEFAULT
PROJECT_HUB
HUMAN_PROJECT_HOME
DOMAIN_WORKSPACE
DETAIL_OR_RECORD
L4_EXCEPTION_REVIEW_REQUIRED
```

Machine contract verifies:

```json
{
  "notion_navigation_layers": [
    "PROJECT_HUB",
    "HUMAN_PROJECT_HOME",
    "DOMAIN_WORKSPACE",
    "DETAIL_OR_RECORD"
  ],
  "default_navigation_depth_max": "L3",
  "l4_normal_page_nesting": "AVOID",
  "domain_workspace_recommended_count": {"min": 4, "max": 6}
}
```

기존 Human/System separation, Project relation, approved visual delivery/readback, zero-incremental-cost tests를 약화하지 않는다.

### Live Notion verification

각 migrated project는:

- Hub → Home ancestor/path 확인
- Home → L2 Domain 4~6개 권장 범위 확인
- L2 → L3 owner 정상 이동 확인
- moved page가 기존 content/DB를 보존했는지 확인
- Home acceptance gate 전 항목 확인
- 다른 Project relation/data 혼입 없음 확인

### Evidence ceiling

Notion semantic fetch/readback으로 다음을 주장할 수 있다.

- page parent/child 구조
- visible text/table/mention 존재
- database/view relation metadata
- content 이동 보존

다음은 별도 rendered evidence 전에는 주장하지 않는다.

- pixel-perfect hierarchy
- actual sidebar visual balance
- mobile crop/scroll quality
- user comprehension speed

## Adversarial review

Pre-migration design과 post-migration 결과 모두 minimum 5 whole reviews를 적용한다.

한 loop는 전체 current candidate를 다음 범위까지 다시 본다.

- user intent
- Home richness
- navigation depth/breadth
- SSoT/duplicate risk
- project-specific semantics
- AI/System isolation
- linked view/database integrity
- open PR/concurrent work
- rollback
- zero-cost constraint
- IRG/evidence ceiling

5회 전에 finding이 발생하면 수정한다. material design 또는 migration mapping이 바뀌면 clean count를 0/5로 reset한다. 5회 이후에도 새 valid blocker가 나오면 clean까지 추가 full review를 계속한다.

## Rollback

- Base: eventual squash merge를 revert하면 정책/테스트를 되돌릴 수 있다.
- Notion: migration map에 기존 parent ID와 target parent ID를 모두 기록한다.
- page move 실패/회귀 시 해당 page를 recorded old parent로 되돌린다.
- child page/DB 삭제를 rollback 수단으로 사용하지 않는다.
- content cleanup은 surviving owner destination readback 후에만 수행한다.

## Acceptance

1. Project Hub는 각 dedicated Human Project Home의 first-click launcher다.
2. 모든 Project Home은 full game/story flow를 직접 보여준다.
3. 모든 Project Home은 core systems와 프로젝트에 필요한 setting/player role/core conflict를 직접 보여준다.
4. 모든 Project Home은 project-specific core data의 대표 표/관계를 직접 보여준다.
5. Home drilldown link는 core understanding을 대체하지 않는다.
6. 프로젝트별 L2 Domain은 4~6개를 권장하되 project semantics에 따라 구성한다.
7. 일반 navigation은 L3에서 끝나고 L4+는 review-required exception이다.
8. L2는 empty folder가 아니라 domain responsibility surface다.
9. L3는 detail/record owner이며 더 깊은 구조는 DB/Relation/View/section을 우선한다.
10. current owner가 하나이며 duplicate current canon을 만들지 않는다.
11. AI/System metadata는 Human Home 기본 화면에서 제외된다.
12. Notion move는 read-before-write + destination readback + rollback parent 기록을 가진다.
13. 진행 중 project PR은 read-only이며 branch-only content를 current truth로 승격하지 않는다.
14. 유료 Notion 기능이나 새 broad Skill은 필요하지 않다.
15. Tetris pilot이 acceptance를 통과한 뒤에만 fleet rollout을 계속한다.
