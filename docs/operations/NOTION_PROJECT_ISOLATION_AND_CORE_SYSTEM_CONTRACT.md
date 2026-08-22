# Notion Project Isolation and Core System Contract

## Project Home human-facing contract

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

`PROJECT_REGISTRY_IS_SYSTEM_MASTER_NOT_HUMAN_HOME`

`HUMAN_HOME_PHYSICALLY_SEPARATE_FROM_REGISTRY_ROW`

각 Project Home은 프로젝트 한 줄 정의·플레이어/사용자 가치·확정 방향·Core Loop/Flow·핵심 시스템 목적/상호작용·UX/UI/Visual·현재 구현상태·검증 evidence ceiling·blocker/다음 작업·중요 결정·위험/revisit condition을 본문에서 직접 설명한다. 하위 `08 · 핵심 시스템 · 상세` 같은 페이지는 상세 evidence와 긴 표를 위한 drilldown이며 Home의 핵심 이해를 대신하지 않는다.

`PROJECT REGISTRY · Master`는 Project Key·Repository·동기화·실행환경 연결을 보존하는 AI/System Master다. `Codex Home`, `Project Local Path`, `Godot Port`, `Repo Main SHA`, `Record Key`, `Revision` 같은 machine metadata를 가진 Registry row를 사람용 Project Home으로 재사용하지 않는다. Human Home은 Registry row와 **별도 일반 페이지로 물리 분리**하고, 단순히 database view의 column을 숨기는 것으로 대체하지 않는다. 사람용 기본 화면에는 `Prompt`, `AI Note`, `Hash`, `Implementation Path` 같은 AI/asset processing metadata도 노출하지 않는다.

## 목적

여러 프로젝트가 같은 Notion workspace를 동시에 사용하더라도 서로의 작업·자산·핵심 시스템 데이터를 덮어쓰거나 섞지 않도록 한다. `PROJECT_NAMESPACE_ISOLATION`이 프로젝트 간 병렬 작업의 기본 쓰기 모델이다.

Notion은 사람용 전체 그림과 시각/비교/핵심 시스템 표현의 정본이고, repository는 Markdown·JSON·game data·code·scene·resource·test·runtime evidence의 정본이다. Notion 변경이 구조화 또는 runtime 의미를 바꾸면 `SYNC_BEFORE_IMPLEMENTATION`을 적용한다.

## 1. Project namespace

모든 project-scoped record는 **정확히 하나의 Project relation**을 가져야 한다.

```text
Project Registry row
→ Project Key
→ Work / Asset / Core System record의 Project relation
→ Project-filtered linked view
```

AI/자동화는 unfiltered Master DB 전체에서 임의 대상을 고르지 않는다. 작업 시작 시 정확한 Project Registry row와 `Project Key`를 resolve한 뒤 해당 namespace 안에서만 읽고 쓴다.

다른 Project relation의 record는 같은 이름·유사한 내용이라도 수정하지 않는다.

## 2. CORE SYSTEM · Master

사람이 프로젝트의 핵심 시스템을 한 곳에서 자세히 탐색·비교·수정할 수 있도록 `CORE SYSTEM · Master`를 공용 System Master로 사용한다.

각 GAME Project Home에는 `08 · 핵심 시스템 · 상세` 페이지를 두고, 이 페이지는 해당 Project relation으로 필터된 linked view만 노출한다.

공용 metadata는 다음을 기본으로 한다.

```text
Name
Project
Record Key
Record Type
Status
Category
Summary
Player Meaning
Rule / Effect
Values
Dependencies
Source Path
Source SHA
Sync State
Revision
Last Synced
Record ID
Last Edited
Parent / Children
```

추천 Record Type:

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

공통 type은 검색·필터용 metadata다. OMENWARD의 건물/병종과 TEN_PACES의 무공서/기술/노드처럼 프로젝트 고유 문법을 하나의 범용 규칙으로 축소하지 않는다.

## 3. deterministic Record Key

핵심 시스템 record identity는 다음 형식을 사용한다.

```text
<ProjectKey>::<RecordType>::<LocalId>
```

예:

```text
OMENWARD::BUILDING::VAULT
TEN_PACES::MARTIAL_MANUAL::HUASHAN_PLUM_BLOSSOM
TEN_PACES::STAT::EXTERNAL_POWER
MY_LITTLE_BOAT::SYSTEM::VOYAGE_LOOP
```

같은 `(Project, Record Key)`가 둘 이상이면 `CONFLICT_DUPLICATE_KEY`다. 자동으로 병합하거나 임의 하나를 최신이라고 추정하지 않는다.

## 4. 동일 레코드 동시 수정

Notion API는 일반 SQL DB의 atomic compare-and-swap/row lock을 제공하지 않으므로 절대적인 same-record 직렬화를 주장하지 않는다. AI/자동화는 `OPTIMISTIC_CONFLICT_DETECTION`으로 fail-closed 한다.

```text
resolve exact Project
→ query exact Record Key inside Project
→ read Revision + Last Edited + current target fields
→ build bounded field-level update
→ immediately re-read Revision + Last Edited
→ unchanged: write only intended fields
→ changed: CONFLICT_STALE_READ and abort
→ increment Revision
→ destination readback
→ verify Project + Record Key + Revision + changed fields
```

사람이 Notion UI에서 최신 변경을 넣었다면 AI는 그 변경을 덮어쓰지 않는다. stale snapshot은 재사용하지 않는다.

## 5. BOUNDED_RECORD_WRITE

기본 쓰기는 `BOUNDED_RECORD_WRITE`다.

허용:

- 특정 Project row property update.
- exact Record Key를 가진 Core System row의 필요한 field만 update.
- 기존 Project Home에 새 child page/link/view를 추가하는 작은 insert.
- 새 record 생성 전 exact key 중복 검사.

금지:

- 다른 Project relation을 가진 record 수정.
- Project relation이 없는 record를 project canon으로 승격.
- 동일 Record Key 중복 생성.
- stale read 뒤 overwrite.
- 여러 프로젝트가 들어 있는 공용 페이지의 전체 `replace_content`를 기본 업데이트 방식으로 사용.
- linked view filter 없이 공용 Master를 project user surface에 노출.
- AI/System metadata를 보유한 Project Registry row를 Human Project Home으로 사용.

## 5A. ZERO_INCREMENTAL_COST Free-plan fallback

기본 운영은 `ZERO_INCREMENTAL_COST`를 유지한다. Notion의 SQL형 `query_data_sources`는 `QUERY_DATA_SOURCES_OPTIONAL`이며 기본 작업 완료 조건이 아니다.

`query_data_sources`가 플랜 제한으로 비활성·upgrade-required 상태여도 표준 프로젝트 작업은 중단하지 않는다.

```text
exact Project Registry row resolve
→ Project-filtered linked view 확인
→ search/fetch로 exact Project·Record Key 확인
→ Revision + Last Edited pre-read
→ bounded field-level update
→ destination readback
```

- Project-filtered linked view, `search/fetch`, page/data-source fetch, bounded update, destination readback을 기본 fallback으로 사용한다.
- Business 전용 SQL 집계 기능은 대량 교차 프로젝트 분석의 선택적 최적화일 뿐이다.
- 표준 프로젝트 생성·수정·교차검증만을 위해 유료 Notion 업그레이드를 요구하지 않는다.
- 여러 프로젝트 집계가 필요하지만 SQL query가 없으면 프로젝트별 filtered view/readback으로 분할 검증하고, 실행하지 않은 전역 집계를 완료로 주장하지 않는다.
- 무료 fallback도 동일한 Project namespace, Record Key, Revision/Last Edited, conflict fail-closed 규칙을 유지한다.

## 6. Conflict states

```text
CONFLICT_STALE_READ
= pre-read 뒤 Revision 또는 Last Edited가 바뀜.

CONFLICT_DUPLICATE_KEY
= 같은 Project 안에서 exact Record Key가 둘 이상 존재.

CONFLICT_MISSING_PROJECT
= project-scoped record에 Project relation이 없거나 정확히 하나로 resolve되지 않음.
```

Conflict는 실패를 숨기지 않는다. 사용자 변경을 덮어쓰기보다 `REVIEW_REQUIRED`/`CONFLICT`로 남기는 것이 우선이다.

## 7. Sync states

Core System 사람용 record의 기본 동기화 상태:

```text
SYNCED
PROPOSED_NOTION_CHANGE
REPO_UPDATE_REQUIRED
REVIEW_REQUIRED
CONFLICT
```

- `SYNCED`: Notion 의미와 현재 repository owner가 일치하고 destination readback 완료.
- `PROPOSED_NOTION_CHANGE`: 사용자가 Notion에서 사람용 의미를 바꿨지만 repository 반영 여부를 아직 판단하지 않음.
- `REPO_UPDATE_REQUIRED`: 변경이 structured/runtime 의미에 영향을 주므로 repository 동기화 필요.
- `REVIEW_REQUIRED`: source status/권위/중복 등 사람이 판단해야 함.
- `CONFLICT`: stale read, duplicate key, missing project 등으로 자동 쓰기 중단.

## 8. Source/status laundering 금지

GitHub source가 `APPROVED_DRAFT_PLANNING`, `POC_HYPOTHESIS`, `DEFERRED`, `NOT_RUN`이면 Notion에서 이유 없이 `CONFIRMED`나 구현 완료로 승격하지 않는다.

Notion `Status`는 사람용 의미의 확정 정도를 나타내고, runtime 구현·테스트 상태를 대신하지 않는다.

```text
CONFIRMED
PROVISIONAL
DEFERRED
REJECTED
```

Source Path와 Source SHA를 남겨 교차검증한다.

## 9. 프로젝트별 사용자 surface

`08 · 핵심 시스템 · 상세`은 다음 질문에 답해야 한다.

- 이 프로젝트의 핵심 시스템은 무엇인가?
- 플레이어에게 어떤 의미가 있는가?
- 어떤 규칙·효과·수치·상태를 가지는가?
- 무엇과 연결되는가?
- 무엇이 확정이고 무엇이 미정인가?
- 구조화 정본과 runtime 근거는 어디에 있는가?

예:

### OMENWARD

- MapRun/Stage/Pressure.
- 자원·3릴·배치 commit.
- 7종 건물과 Tier/분기.
- 병종 역할·T3 역할.
- Mana Tower·전술 연구.
- Merchant·Onboarding·Hero/Meta.

### TEN_PACES

- 10칸 전장·3/3/4 계획.
- 전투 자원·합·방어·회피·중단.
- 외공·근골·신법·내공·심안.
- 주요 비무·중간 노드 구조.
- 무공서 성장.
- 무공서별 기술1·5성 효과·기술2·9성 효과·10성 절초.
- 기술/절초 예산.

### MY_LITTLE_BOAT

- 마음 선택.
- 5분 항해 루프.
- 사진·감상모드·속도 조절.
- 병 속 편지·풍경·동반자 호감도·앨범.
- 모바일 세로/PC 입력.
- 전투·실패·경쟁·결제·광고·온라인 편지 공유 금지.

## 10. 병렬 작업 예시

OMENWARD와 TEN_PACES가 동시에 수정될 때:

```text
Worker A
Project = OMENWARD
Record Key prefix = OMENWARD::

Worker B
Project = TEN_PACES
Record Key prefix = TEN_PACES::
```

서로 다른 Project relation이므로 병렬 실행 가능하다.

같은 OMENWARD 건물 record를 두 worker가 동시에 수정하려 하면 둘 다 최신 Revision/Last Edited를 다시 확인하고, 먼저 반영된 쓰기 뒤 두 번째 worker는 `CONFLICT_STALE_READ`로 중단해야 한다.

## 11. 완료 검증

Notion write는 저장 호출 성공만으로 완료가 아니다.

```text
write
→ destination readback
→ Project 확인
→ Record Key 확인
→ Revision 확인
→ intended field 확인
→ source/status 확인
→ SYNCED 또는 명시적 비동기 상태 판정
```

Project Registry에서 Project Key 중복, Core System Master에서 `(Project, Record Key)` 중복, Project relation 누락을 검사한다.

기존 Project Home·child page·Work/Asset record를 삭제하거나 이동하지 않는다. 단, Human Home/AI-System 물리 분리 교정처럼 **명시적으로 승인된 구조 교정**은 기존 System Master를 보존한 채 링크/부모만 이동하고 destination readback과 rollback path를 남긴다.

## Human Home 상세 정책

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`의 Base/Project Home 필수 내용과 AI/System 제외 규칙은 `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`가 소유한다. 하위 페이지는 drilldown/evidence이며 core understanding을 대신하지 않는다.
