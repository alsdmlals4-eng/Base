# 주기 Source Scan Queue 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 Watchlist·Ledger·Evidence Method를 유지하면서 매주 Source 재검토 Issue를 생성·갱신하고, 첫 증분 조사에서 확인한 신규 사이트와 새 글의 검증된 최소 개선을 기존 owner에 흡수한다.

**Architecture:** Python 표준 라이브러리 Queue renderer가 Ledger의 due Source를 결정론적으로 계산한다. 최소 권한 GitHub Actions가 매주 월요일 10:17 KST와 수동 실행에서 고정 Issue 하나만 생성·갱신한다. 실제 원출처 검토·Evidence 판정·Guide/프로젝트 반영은 기존 owner와 PR 검증이 계속 담당한다.

**Tech Stack:** Python 3.12 standard library, `unittest`, Markdown/JSON contracts, GitHub Actions, GitHub CLI.

## Global Constraints

- 기준 `main`: `3e3f59b1b835f9675f0b8dbc4543a6c69a526c36`.
- 작업 Branch: `feat/periodic-source-scan-queue-20260814`.
- 새 ACTIVE Skill·Work Mode·Evidence owner·독립 Ledger를 만들지 않는다.
- Schedule은 Queue Issue만 쓰며 Article·PDF 자동 수집, Ledger 자동 갱신, Canon 자동 반영, 자동 PR·merge를 하지 않는다.
- Workflow 권한은 `contents: read`, `issues: write`로 제한한다.
- 공식 GitHub Action은 전체 commit SHA로 고정한다.
- 매 주기 기존 Source의 새 글·수정 글 확인과 신규 Source 사이트 탐색을 모두 요구한다.
- Source·Article 수 자체를 개선 성과로 사용하지 않는다.
- 로컬 네트워크가 막히면 `BLOCKED_ENVIRONMENT_DNS`로 분리하고 exact-head GitHub Actions를 실행 증거로 사용한다.
- 병합 전 최신 `main`과 open PR changed-path를 재확인한다.

---

### Task 1: RED 계약 고정

**Files:**
- Create: `tests/test_periodic_source_scan_queue.py`
- Modify: `tests/test_periodic_external_source_watchlist.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`

**Interfaces:**
- Consumes: `PERIODIC_SOURCE_OPERATIONS_LEDGER.json`, Watchlist, Narrative Radar, Tutorial Guide.
- Produces: Queue script·scheduled workflow·첫 scan checkpoint·신규 Source·흡수 field를 요구하는 실패 계약.

- [ ] **Step 1: Queue renderer 단위 계약 작성**

다음 실제 API를 import하도록 작성한다.

```python
from tools.periodic_source_scan_queue import (
    ISSUE_MARKER,
    ISSUE_TITLE,
    load_ledger,
    parse_iso_date,
    render_issue_body,
    select_due_sources,
    source_is_due,
)
```

검사 항목:

```text
weekly/daily-or-weekly = 7일
monthly-or-on-demand = 30일
quarterly-or-when-relevant = 90일
null last scan = due
inactive = 제외
invalid/future date = ValueError
동일 입력 = 동일 Markdown
Issue marker/title
UNVERIFIED_DISCOVERY
새 글·수정 글 확인
신규 Source 사이트 탐색
original source backtrace
owner/consumer/claim ceiling/validation/rollback/disposition
CLI output
```

- [ ] **Step 2: Watchlist/Radar/Guide/Workflow 계약 추가**

다음을 요구한다.

```text
.github/workflows/periodic-source-scan-queue.yml
cron: "17 10 * * 1"
timezone: "Asia/Seoul"
contents: read
issues: write
workflow_dispatch
DiGRA Digital Library
Game Studies
MCLC Resource Center
Library of Congress Web Cultures Web Archive
Data & Society
prior_game_expertise
story_holon_local_coherence
wuxia_xianxia_cultivation_boundary
platform_commercialization_and_governance_stage
SOURCE_SCAN_CHECKPOINT_2026-08-14.md
```

금지 계약:

```text
pull_request_target
contents: write
auto article body ingestion
auto Canon write
auto content PR
```

- [ ] **Step 3: Evidence Workflow가 새 계약을 실행하도록 수정**

`py_compile`, `unittest`, artifact path에 다음을 넣는다.

```text
tools/periodic_source_scan_queue.py
tests/test_periodic_source_scan_queue.py
.github/workflows/periodic-source-scan-queue.yml
docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md
docs/knowledge/game-development/SOURCE_SCAN_CHECKPOINT_2026-08-14.md
```

- [ ] **Step 4: Intentional RED PR 생성·확인**

Expected:

```text
기존 계약은 통과
새 Queue script/workflow/checkpoint/fields 부재 계약만 실패
Python syntax failure나 기존 회귀가 아님
```

### Task 2: Queue renderer 구현

**Files:**
- Create: `tools/periodic_source_scan_queue.py`

**Interfaces:**
- Consumes: Ledger schema version 1.
- Produces: deterministic Markdown Issue body and CLI file.

- [ ] **Step 1: 상수와 strict date parser 구현**

```python
CADENCE_DAYS = {
    "daily-or-weekly": 7,
    "weekly": 7,
    "monthly-or-on-demand": 30,
    "quarterly-or-when-relevant": 90,
}
ISSUE_TITLE = "[Periodic Source Scan Queue]"
ISSUE_MARKER = "<!-- periodic-source-scan-queue -->"
```

- [ ] **Step 2: Ledger validation 구현**

```text
root object
schema_version == 1
sources list
unique non-empty source_id
known cadence
ACTIVE status
last_successful_scan_at null 또는 YYYY-MM-DD
future date fail closed
```

- [ ] **Step 3: due source selection 구현**

정렬 키:

```text
recommended_cadence
source_id
```

- [ ] **Step 4: Markdown renderer 구현**

본문에 다음 고정 section을 생성한다.

```text
경고와 authority boundary
Due Source 표
기존 Source 새 글·수정 글 확인
신규 Source 사이트 확장
Candidate Packet
흡수·검증·rollback Gate
완료 체크
```

- [ ] **Step 5: CLI 구현**

Arguments:

```text
--ledger PATH
--date YYYY-MM-DD
--output PATH
```

출력 파일은 UTF-8, LF, 마지막 newline을 사용한다.

- [ ] **Step 6: 단위 계약 GREEN 확인**

Run:

```bash
python -m unittest tests/test_periodic_source_scan_queue.py -v
```

### Task 3: Scheduled Queue Workflow 구현

**Files:**
- Create: `.github/workflows/periodic-source-scan-queue.yml`

**Interfaces:**
- Consumes: Queue script and Ledger.
- Produces: one idempotent GitHub Issue plus Markdown artifact.

- [ ] **Step 1: Trigger·permissions·concurrency 작성**

```yaml
on:
  schedule:
    - cron: "17 10 * * 1"
      timezone: "Asia/Seoul"
  workflow_dispatch:
permissions:
  contents: read
  issues: write
```

- [ ] **Step 2: 공식 Action SHA pinning**

```text
actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97
actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a
```

- [ ] **Step 3: Script 계약과 Queue 렌더 실행**

```bash
python -m py_compile tools/periodic_source_scan_queue.py tests/test_periodic_source_scan_queue.py
python -m unittest tests/test_periodic_source_scan_queue.py -v
python tools/periodic_source_scan_queue.py \
  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
  --date "$(date -u +%F)" \
  --output periodic-source-scan-queue.md
```

- [ ] **Step 4: Issue upsert 구현**

고정 제목으로 열린 Issue를 검색한다.

```bash
issue_number="$(gh issue list --state open --search 'in:title "[Periodic Source Scan Queue]"' --json number,title --jq '.[] | select(.title == "[Periodic Source Scan Queue]") | .number' | head -n 1)"
```

있으면 `gh issue edit`, 없으면 `gh issue create`한다. 본문 파일을 그대로 사용하며 외부 Source 문자열을 shell code로 평가하지 않는다.

- [ ] **Step 5: Queue artifact 업로드**

### Task 4: 첫 Source Scan Checkpoint 작성

**Files:**
- Create: `docs/knowledge/game-development/SOURCE_SCAN_CHECKPOINT_2026-08-14.md`

**Interfaces:**
- Consumes: 현재 Source 사이트와 2025-08~2026-06 신규 글.
- Produces: Source 후보·Article 후보·disposition·owner·validation·rollback 증거.

- [ ] **Step 1: 신규 Source 사이트 5개 판정**

```text
DiGRA Digital Library — ADOPT_DURABLE_SOURCE
Game Studies — ADOPT_DURABLE_SOURCE
MCLC Resource Center — ADOPT_DURABLE_SOURCE
Library of Congress Web Cultures Web Archive — ADOPT_DURABLE_SOURCE
Data & Society — ADOPT_DURABLE_SOURCE_CONDITIONAL
```

각 항목에 role, cadence, scan surfaces, claim ceiling, current owner를 기록한다.

- [ ] **Step 2: 새 글 Candidate Packet 작성**

```text
DiGRA onboarding/game expertise — ADAPT + TEST
DiGRA holarchic narrative — ADAPT + TEST
Cultivation games/cosmotechnics — ADAPT
Bilibili graphicon/platform stages — ADAPT
War trauma/agency — REFERENCE_ONLY
Neighborhood cultural preservation — REFERENCE_ONLY
Black Myth fan journalism — REFERENCE_ONLY
```

- [ ] **Step 3: 미채택·한계 기록**

```text
제목·snippet만으로 세부 기법 확정 금지
한 연구·한 플랫폼·한 지역의 보편화 금지
프로젝트 consumer 없는 후보는 REFERENCE_ONLY
actual player evidence 부재는 TEST 또는 BLOCKED_UNVERIFIED
```

### Task 5: 기존 owner에 최소 흡수

**Files:**
- Modify: `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
- Modify: `docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md`
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`

**Interfaces:**
- Consumes: first scan dispositions.
- Produces: reusable Guide fields and recurring operating contract.

- [ ] **Step 1: Narrative Radar Source rows 추가**

```text
DiGRA Digital Library
Game Studies
MCLC Resource Center
Library of Congress Web Cultures Web Archive
Data & Society
```

- [ ] **Step 2: Holarchic fragment field 추가**

```yaml
story_holon_local_coherence:
shared_storyworld_contribution:
fragment_inference_burden:
optional_fragment_redundancy_and_recovery:
```

- [ ] **Step 3: Wuxia/Cultivation boundary 추가**

```yaml
wuxia_xianxia_cultivation_boundary: WUXIA | XIANXIA | CULTIVATION | MARTIAL_ARTS_FANTASY | MIXED
cosmology_and_technical_practice:
translation_and_cross_cultural_boundary:
```

- [ ] **Step 4: Meme platform-stage field 추가**

```yaml
platform_commercialization_and_governance_stage:
native_symbol_system_and_recontextualization:
```

- [ ] **Step 5: Tutorial expertise covariate 추가**

```yaml
prior_game_expertise:
expertise_measure:
novice_expert_segment:
expertise_by_onboarding_interaction:
```

한 연구를 보편 규칙으로 만들지 않고 실제 프로젝트에서 novice/expert를 분리 검증한다.

- [ ] **Step 6: Watchlist에 Scheduled Queue 경계 추가**

```text
Queue != scan completion
Issue update != Ledger timestamp update
매 주기 새 글 + 신규 Source 확장
원출처 확인 전 UNVERIFIED_DISCOVERY
흡수는 기존 owner와 PR 검증
```

### Task 6: GREEN·회귀·적대적 검토

- [ ] Evidence Knowledge exact-head GREEN.
- [ ] Base v9 exact-head GREEN; adversarial gate GREEN.
- [ ] Game Project OS exact-head GREEN; final `ci-gate` GREEN.
- [ ] Queue script sample output readback.
- [ ] Workflow permission·trigger·SHA pinning readback.
- [ ] ACTIVE Skill 수와 `PLAN / BUILD / REVIEW` 불변 확인.
- [ ] open PR exact changed-path intersection 확인.
- [ ] P0/P1 0, unresolved review thread 0.
- [ ] 로컬 DNS 차단을 원격 Actions 성공으로 위장하지 않음.

### Task 7: 최신 main 동기화·병합

- [ ] 최신 `main` SHA 재확인.
- [ ] Branch behind 여부 확인.
- [ ] 뒤처졌으면 비파괴 merge commit으로 동기화하고 exact-head Checks 재실행.
- [ ] squash merge.
- [ ] feature merge SHA와 새 `main` readback.
- [ ] post-merge Base v9·Game Project OS 성공 확인.

### Task 8: 실제 Scheduled Queue 가동

- [ ] 기본 브랜치에서 `periodic-source-scan-queue.yml` 수동 실행.
- [ ] Workflow success 확인.
- [ ] `[Periodic Source Scan Queue]` Issue 생성 확인.
- [ ] marker·due Source·새 글·신규 Source·Evidence/rollback section readback.
- [ ] 다시 수동 실행.
- [ ] 열린 Queue Issue가 하나만 유지되고 같은 Issue가 갱신되는지 확인.
- [ ] 운영 증거를 implementation plan closeout에 기록하고 필요 시 문서 전용 PR로 병합.

## Expected Files

```text
.github/workflows/periodic-source-scan-queue.yml
.github/workflows/validate-evidence-knowledge.yml
docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
docs/knowledge/game-development/SOURCE_SCAN_CHECKPOINT_2026-08-14.md
docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md
docs/superpowers/plans/2026-08-14-periodic-source-scan-queue.md
docs/superpowers/specs/2026-08-14-periodic-source-scan-queue-design.md
tests/test_periodic_external_source_watchlist.py
tests/test_periodic_source_scan_queue.py
tools/periodic_source_scan_queue.py
```

## Rollback

Feature squash merge commit을 revert한다. Scheduled workflow를 제거하면 이후 자동 Queue 갱신이 중단된다. 기존 Queue Issue는 닫고 `DISABLED_BY_ROLLBACK`을 기록한다. Runtime·Save/Data Schema·Skill Registry·프로젝트 Canon·외부 dependency migration은 없다.
