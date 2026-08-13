# 서사·세계관·캐릭터 전문 Source Radar 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 승인된 권장안 B에 따라 세계관·캐릭터·장르·현실 고증·표현·현지화·추리 공정성·중국 무협·서브컬처 밈 Source를 기존 Radar 아래에 추가한다.

**Architecture:** `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`와 Evidence Method가 계속 권위를 소유한다. 새 `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`는 `PERIODIC_SPECIALTY_SOURCE_RADAR.md`에 종속된 비실행 Reference이며, 기존 소설·게임기획·서사·아트·문서·검증 owner로 후보를 전달한다. 새 ACTIVE Skill, Work Mode, scheduler, 독립 Ledger, 자동 수집기나 프로젝트 Canon owner를 만들지 않는다.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions, GitHub branch/PR workflow.

## Global Constraints

- 기준 `main`: `23e418ec2e4a801c90aff85611f10a5ab062d53c`.
- 후보 최소·최대 수 제한 없음: `candidate_count_limit: NONE`.
- 유효 후보는 모두 기록할 수 있지만 후보별 relevance·owner·consumer·원출처·반례·검증·rollback을 요구한다.
- 후보가 없으면 억지로 만들지 않는다.
- 프로젝트 고유 인물·세계관·무공·문파·밈·단서·해답·수치는 프로젝트 소유다.
- Community Wiki·Trend·조회수·인기·영화 안무·현대 경기 규칙을 역사·Canon·호감·판매·실전 증거로 과장하지 않는다.
- 특정 작가·작품·팬덤의 식별 가능한 표현을 복제하지 않는다.
- 기존 30 ACTIVE Skill과 `PLAN / BUILD / REVIEW`를 유지한다.
- 열린 PR #312·#322의 소유 경로를 변경하지 않는다.
- 로컬 GitHub DNS 차단으로 실행 불가한 검사는 `BLOCKED_ENVIRONMENT_DNS`로 보고한다.
- 실행 증거는 branch/PR exact-head GitHub Actions와 merge 후 main Actions로 확인한다.

---

### Task 1: RED 계약 고정

**Files:**
- Modify: `tests/test_periodic_external_source_watchlist.py`
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: 기존 Watchlist/Radar authority contract와 기존 Workflow의 unittest 목록.
- Produces: 하위 Radar·Hub route·9개 Domain·후보 수 무제한·claim ceiling·기존 owner routing을 요구하는 실패 계약.

- [ ] **Step 1: Watchlist 계약에 하위 Radar 요구 추가**

`NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md` 경로와 다음 요구를 검사한다.

```text
parent_radar
owner_policy
evidence_owner
scheduler_authority: EXTERNAL_TO_BASE
new_active_skill: false
independent_ledger: false
candidate_count_limit: NONE
capture_all_material_candidates: true
forced_filler_candidates: false
9개 Domain
추리·무협·밈 claim ceiling
```

- [ ] **Step 2: Discovery 계약에 기존 consumer route 요구 추가**

```text
developing-and-revising-serial-fiction
NARRATIVE_AND_RELATIONSHIP_METHOD.md
CHARACTER_AND_NARRATIVE_ART_METHOD.md
analyzing-and-refining-game-concepts
CONTENT_DESIGN_METHOD.md
ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md
reviewing-and-validating-project-changes
running-adversarial-review-and-refinement
```

- [ ] **Step 3: Intentional RED PR 생성**

Branch `docs-source-radar-20260813-b`에서 PR을 열고 Evidence Knowledge Workflow를 확인한다.

Expected:

```text
기존 계약은 통과
새 계약은 하위 Radar·Hub route 부재 때문에 실패
Python syntax error나 기존 회귀 실패가 아님
```

### Task 2: 하위 Radar 구현

**Files:**
- Create: `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`

**Interfaces:**
- Consumes: parent Radar metadata, Watchlist Source roles, Evidence Method dispositions.
- Produces: 9개 Domain과 공통 candidate packet, Source table, claim ceiling, validation flow, cadence, completion states, adversarial questions.

- [ ] **Step 1: 권위·후보 수 정책 작성**

```yaml
candidate_count_limit: NONE
capture_all_material_candidates: true
minimum_candidate_quota: NONE
forced_filler_candidates: false
```

- [ ] **Step 2: 세계관·캐릭터·장르·현실 고증 Domain 작성**

Archive·박물관·도서관·UNESCO·직업·정신건강·대본 Archive·실제 project evidence를 역할별로 분리한다.

- [ ] **Step 3: 표현·언어·현지화 Domain 작성**

Unicode CLDR·W3C와 공식·당사자·전문가 Source를 사용하며 이름·호칭·문자 방향·문화 편향·표현 위험을 구분한다.

- [ ] **Step 4: 추리·단서 공정성 Domain 작성**

Truth model, clue inventory, discoverability, alternative hypotheses, red herring causality, hint ladder, recovery, uniqueness와 unknown-player test를 요구한다.

- [ ] **Step 5: 무술·무림·중국 무협 Domain 작성**

Martial Arts Studies, IWUF, UNESCO Taijiquan, Chinese Text Project, CBDB, CHGIS, Hong Kong Film Archive를 역사·현대 경기·living heritage·원문·사회관계·지리·영화 문법으로 분리한다.

- [ ] **Step 6: 서브컬처·밈·팬덤 Domain 작성**

Fanlore/TWC, Know Your Meme, Google Trends, platform/community discovery를 기원·확산·현재 의미·아이러니·혐오 신호·권리·표본 한계로 분리한다.

- [ ] **Step 7: 검증·상태·적대적 질문 작성**

```text
NO_CHANGE
EVIDENCE_ONLY_UPDATE
ABSORB_EXISTING_OWNER
PROJECT_ONLY
TEST
REFERENCE_ONLY
AVOID
PROMOTION_CANDIDATE
BLOCKED_UNVERIFIED
```

### Task 3: One-hop routing

**Files:**
- Modify: `docs/knowledge/game-development/README.md`
- Modify: `docs/knowledge/serial-fiction/README.md`

**Interfaces:**
- Consumes: 하위 Radar path와 기존 owner matrix.
- Produces: 게임 개발 지식 허브와 Serial Fiction Hub에서 한 단계 접근.

- [ ] **Step 1: Game Development Hub 문서 지도 추가**

하위 Radar가 두 번째 Watchlist·Skill·scheduler가 아니며 기존 owner 조합으로 실행된다고 명시한다.

- [ ] **Step 2: Serial Fiction Hub 외부 조사 route 추가**

세계관·캐릭터·장르·고증·표현·현지화·추리·무협·밈 조사 시 하위 Radar를 읽고 작품별 Canon은 프로젝트에 둔다고 명시한다.

### Task 4: GREEN과 회귀 검증

- [ ] PR exact head에서 `Validate Evidence-Based Game Development Knowledge` 성공 확인.
- [ ] PR exact head에서 `Validate Base v9 Operating Contracts` 성공 확인.
- [ ] PR exact head에서 `Validate Game Project Operating System` 최종 `ci-gate` 성공 확인.
- [ ] Active Skill map 30과 `PLAN / BUILD / REVIEW` readback.
- [ ] 변경 파일과 PR #312·#322 exact path intersection 0 확인.
- [ ] 로컬 테스트는 `BLOCKED_ENVIRONMENT_DNS`로 별도 보고.

### Task 5: 적대적 검토

- [ ] 두 번째 Watchlist·Skill·Ledger·scheduler 생성 여부.
- [ ] 링크 dump와 현재 consumer 없는 후보.
- [ ] 성격 유형·진단·문화 고정관념.
- [ ] 작가 self-test만으로 추리 공정성 주장.
- [ ] clue logic와 discoverability 혼동.
- [ ] 현대 경기·역사 실전·영화 안무·무협 관습 혼동.
- [ ] 중국 시대·지역·계층의 단일화.
- [ ] 밈의 기원·현재 의미·아이러니·혐오·권리 혼동.
- [ ] Community Wiki·Trend를 Canon·호감·판매 인과로 과장.
- [ ] 프로젝트 고유 Canon의 Base 승격.

검증 가능한 affected consumer와 failure mode가 없는 취향 finding은 blocker로 유지하지 않는다.

### Task 6: PR·병합·post-merge

- [ ] final exact head와 current main 재확인.
- [ ] unresolved review thread 0과 P0/P1 0 확인.
- [ ] repository 정책이 허용하면 squash merge.
- [ ] merge SHA와 새 `main`에서 하위 Radar·Hub·tests readback.
- [ ] post-merge main Actions의 Evidence Knowledge, Base v9, Game Project OS/`ci-gate` 성공 확인.

## Expected Files

```text
docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
docs/knowledge/game-development/README.md
docs/knowledge/serial-fiction/README.md
docs/superpowers/specs/2026-08-13-narrative-world-character-source-radar-design.md
docs/superpowers/plans/2026-08-13-narrative-world-character-source-radar.md
tests/test_periodic_external_source_watchlist.py
tests/test_periodic_external_source_discovery_seeds.py
```

## Rollback

Eventual squash merge commit을 revert한다. 하위 Radar, Hub route, tests, spec, plan이 함께 되돌아가며 Runtime·Save/Data Schema·Skill Registry·프로젝트 Canon·외부 dependency migration은 없다.
