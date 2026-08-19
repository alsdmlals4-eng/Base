# Notion Project Isolation + Core System Design

## Goal

여러 프로젝트가 같은 Notion workspace와 공용 Master DB를 동시에 사용해도 프로젝트 간 쓰기 충돌과 데이터 혼입을 구조적으로 줄이고, 사람이 프로젝트별 핵심 시스템을 상세하게 읽고 수정할 수 있는 `CORE SYSTEM · Master`를 추가한다. `My Little Boat`를 Project Registry와 같은 운영 구조에 등록한다.

## Approved direction

사용자 요구와 기존 `DOMAIN_SPLIT_CANON`을 유지한다.

- Notion = 사람이 보는 프로젝트 전체 그림, 핵심 재미·루프, 시각 자료, 예산/Tier/핵심 시스템 표의 우선 정본.
- Repository = Markdown/JSON/game data/code/scene/resource/test/runtime evidence의 구조화·구현 정본.
- Notion 수정이 구조화/런타임 의미를 바꾸면 `SYNC_BEFORE_IMPLEMENTATION`으로 repository에 동기화한다.

## Alternatives reviewed

### A. 프로젝트마다 독립 DB 세트

- 장점: 물리적 격리 강함.
- 단점: Project/Work/Asset/System schema와 view를 프로젝트 수만큼 복제해 drift와 유지보수 비용이 커짐.
- 판정: 기각.

### B. 공용 Master + Project 필터만 사용

- 장점: 단순하고 현재 구조와 유사함.
- 단점: 같은 레코드에 대한 동시 AI 수정, 중복 Record 생성, 전체 페이지 replace에 취약함.
- 판정: 불충분.

### C. 공용 Master + Project namespace + deterministic Record Key + optimistic conflict detection

- 장점: 프로젝트 간 병렬 작업을 허용하면서 공용 schema를 하나만 유지하고, 같은 레코드의 경쟁 쓰기만 탐지할 수 있음.
- 단점: Notion API가 원자적 compare-and-swap을 제공하지 않으므로 동일 레코드 동시 쓰기를 100% 직렬화하지는 못함.
- 판정: 채택.

## Project isolation contract

### Project namespace

모든 project-scoped record는 정확히 하나의 `Project` relation을 가져야 한다. `Project Key`는 project namespace다.

예시:

```text
OMENWARD
TEN_PACES
MY_LITTLE_BOAT
```

AI/자동화는 unfiltered Master DB에서 임의로 수정 대상을 고르지 않는다. 먼저 Project Registry row를 resolve한 뒤 해당 Project relation으로 범위를 제한한다.

### Record identity

핵심 시스템 record는 다음 deterministic key를 사용한다.

```text
<ProjectKey>::<RecordType>::<LocalId>
```

예시:

```text
OMENWARD::BUILDING::VAULT
TEN_PACES::MARTIAL_MANUAL::HUASHAN_PLUM_BLOSSOM
TEN_PACES::STAT::EXTERNAL_POWER
MY_LITTLE_BOAT::SYSTEM::VOYAGE_LOOP
```

`Record Key`는 사람이 임의로 재사용하지 않는다. 같은 key가 둘 이상 발견되면 자동 수정하지 않고 `CONFLICT_DUPLICATE_KEY`로 처리한다.

## Optimistic concurrency contract

Notion API에는 일반 SQL DB의 atomic compare-and-swap/row lock과 같은 보장이 없으므로 과장하지 않는다. 대신 AI/자동화 쓰기는 fail-closed optimistic protocol을 따른다.

```text
resolve Project
→ query exact Record Key inside Project
→ read Revision + Last Edited + current content
→ compute bounded field-level change
→ immediately re-read Revision + Last Edited
→ unchanged: update only target record/field
→ changed: abort as CONFLICT_STALE_READ
→ increment Revision
→ destination readback
→ verify Project + Record Key + Revision + intended fields
```

금지:

- 다른 Project relation을 가진 record 수정.
- Project relation이 없는 record를 project canon으로 승격.
- 공용 Master 또는 Project Home 전체 `replace_content`로 다른 작업의 블록을 재전송.
- stale snapshot으로 동일 record를 덮어쓰기.
- 같은 Record Key 중복 생성.

사람이 Notion UI에서 수정한 경우 AI는 최신 `Last Edited`/Revision을 다시 읽고 그 변경을 보존한다. 충돌 시 사람 변경을 덮어쓰지 않는다.

## Shared Master responsibilities

### Existing masters

- `PROJECT REGISTRY · Master`: 프로젝트 identity와 repository 연결.
- `작업계획 · Master`: Project relation이 있는 작업.
- `ASSET LIBRARY · Master`: Project relation이 있는 asset/reference/benchmark.

### New master

`CORE SYSTEM · Master`를 `90 · SYSTEM MASTERS` 아래에 둔다.

Required properties:

- `Name` TITLE
- `Project` RELATION(Project Registry)
- `Record Key` RICH_TEXT
- `Record Type` SELECT
- `Status` SELECT: `CONFIRMED / PROVISIONAL / DEFERRED / REJECTED`
- `Category` RICH_TEXT
- `Summary` RICH_TEXT
- `Player Meaning` RICH_TEXT
- `Rule / Effect` RICH_TEXT
- `Values` RICH_TEXT
- `Dependencies` RICH_TEXT
- `Source Path` RICH_TEXT
- `Source SHA` RICH_TEXT
- `Sync State` SELECT: `SYNCED / PROPOSED_NOTION_CHANGE / REPO_UPDATE_REQUIRED / REVIEW_REQUIRED / CONFLICT`
- `Revision` NUMBER
- `Last Synced` DATE
- `Record ID` UNIQUE_ID prefix `SYS`
- `Last Edited` LAST_EDITED_TIME
- self relation `Parent / Children`

Initial `Record Type` set:

```text
SYSTEM
LOOP
RULE
RESOURCE
STAT
NODE
BUILDING
UNIT
MARTIAL_MANUAL
SKILL
EFFECT
ITEM
EVENT
COLLECTION
STATE
```

Project-specific semantics stay in `Category`, `Summary`, `Rule / Effect`, and project pages; the shared type list is metadata, not a forced universal game ontology.

## Project human surface

각 GAME Project Home에는 `08 · 핵심 시스템 · 상세` child page를 둔다.

이 페이지는:

1. 해당 프로젝트의 핵심 재미/루프를 짧게 설명한다.
2. `CORE SYSTEM · Master`의 **Project-filtered linked view**만 표시한다.
3. 필요하면 프로젝트별 상세 표/설명을 함께 둔다.
4. 다른 프로젝트 record를 노출하거나 수정 대상으로 사용하지 않는다.

기존 `07+` 프로젝트 고유 확정표는 유지한다. `08`은 기계적 목록 복제가 아니라 사람이 시스템 전체를 이해하는 탐색/학습 surface다.

## Initial detailed population

### OMENWARD

최소 다음 record family를 current GitHub `main`에서 읽어 배치한다.

- core loop / MapRun / Stage cadence / pressures.
- resources / three reels / deployment commitment.
- 7 building families and Tier grammar.
- general barracks, special barracks, defense tower branches.
- 10 troop roles/T3 role structure where current approved source supports it.
- mana tower research/tactical skill rules.
- merchant/onboarding/hero/meta rules as top-level system records.

과거 superseded no-TokenSource rule은 current record로 복원하지 않는다.

### TEN_PACES

최소 다음 record family를 current GitHub `main`에서 읽어 배치한다.

- 10-space battlefield and 3/3/4 planning loop.
- combat resources and resolution rules.
- stats: 외공/근골/신법/내공/심안 and derived maxima.
- route nodes and major duel/node cadence.
- starting martial manual growth skeleton.
- current 10 martial manuals.
- each manual’s 3/5/7/9/10-star skill/effect summary.
- skill budget and ultimate budget relationship.

`APPROVED_DRAFT_PLANNING`, `POC_HYPOTHESIS`, `DEFERRED` 같은 source status는 Notion에서 `CONFIRMED`로 세탁하지 않는다.

### MY LITTLE BOAT

Repository `alsdmlals4-eng/MylittleBoat`를 `MY_LITTLE_BOAT`로 등록한다.

Initial human-facing canon:

- first-person healing drifting boat game.
- player body invisible.
- mood selection → sea → 5-minute drift → voyage record → idle appreciation.
- controls: photo / appreciation mode / speed.
- mood 4종: 평온, 지침, 외로움, 설렘.
- bottle letter, scenery collection, companion affection Lv1~3, album.
- mobile portrait first + PC mouse support.
- combat/failure/competition/payment/ads/online letter sharing forbidden.

## Validation

- Project Registry에는 `Project Key` 중복이 없어야 한다.
- Work/Asset/Core System project canon record는 Project relation이 비어 있으면 안 된다.
- Project Home linked view는 해당 Project relation filter를 가져야 한다.
- `CORE SYSTEM · Master`에서 같은 `(Project, Record Key)` 중복이 없어야 한다.
- AI write 후 readback에서 Project/Record Key/Revision/필드 값이 일치해야 한다.
- 기존 8개 프로젝트의 Project relation과 child pages를 삭제/이동하지 않는다.
- `My Little Boat` 생성 후 repository URL과 Project Key를 readback한다.

## Rollback

- 새 Core System Master와 project-specific `08` pages는 기존 Work/Asset masters와 독립이므로 문제 시 새 surface만 비활성화/Archive 가능하다.
- 기존 Project Registry/Work/Asset rows를 삭제하지 않는다.
- Base contract 변경은 단일 PR로 되돌릴 수 있다.
- My Little Boat row는 잘못된 identity가 확인된 경우에만 Archive하고 올바른 key로 새 row를 만든다; 기존 다른 프로젝트 row는 수정하지 않는다.
