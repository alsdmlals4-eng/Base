# 주기 Source Scan Queue 설계

```yaml
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-14 사용자 요청 — 주기적으로 Source 사이트를 확장하고 새 글을 검토·흡수
baseline_main_sha: 3e3f59b1b835f9675f0b8dbc4543a6c69a526c36
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
operational_state_owner: docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
narrative_radar: docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
scheduler_runtime: GITHUB_ACTIONS
new_active_skill: false
new_work_mode: false
independent_ledger: false
auto_article_ingestion: false
auto_canon_write: false
auto_content_pr: false
```

## 1. 목표

Base의 기존 Watchlist·Specialty Radar·Evidence Method를 실제 반복 운용할 수 있도록 다음을 설치한다.

1. 현재 Ledger에서 검토 시점이 도래한 Source를 주간 Issue Queue로 만든다.
2. 매 주기마다 기존 Source의 새 글·변경 글을 확인한다.
3. 매 주기마다 신규 Source 사이트 후보를 추가로 탐색한다.
4. 발견 후보를 원출처·현재 owner·프로젝트 consumer·반례·검증·rollback 기준으로 판정한다.
5. 검증된 최소 개선만 기존 Guide·Method·Reference에 흡수한다.
6. 글·사이트 수 자체가 아니라 실제 결정 개선과 재검증 가능성을 성과로 본다.

## 2. 채택 구조

```text
GitHub Actions schedule / workflow_dispatch
→ PERIODIC_SOURCE_OPERATIONS_LEDGER.json 읽기
→ due Source와 신규 Source 확장 질문을 결정론적으로 렌더링
→ 고정 Issue 하나를 생성 또는 갱신
→ 사람이 원출처·본문·날짜·권리·표본·반례 검토
→ Evidence Method disposition
→ 기존 owner 문서·프로젝트 consumer에 최소 흡수
→ 계약 테스트·적대적 검토·PR·rollback
```

GitHub Actions는 **알림·작업 큐 생성기**다. Evidence 판정자, Canon 편집자, 자동 수집기, 자동 PR 작성자가 아니다.

## 3. 실행 주기

```yaml
schedule:
  cron: "17 10 * * 1"
  timezone: Asia/Seoul
manual_trigger: workflow_dispatch
issue_title: "[Periodic Source Scan Queue]"
issue_marker: "<!-- periodic-source-scan-queue -->"
```

월요일 10:17 KST를 사용한다. 정각 혼잡 가능성을 피하고, 저장소 기본 브랜치의 최신 계약을 사용한다.

### Queue 판정

| cadence | 기본 due 간격 |
|---|---:|
| `daily-or-weekly` | 7일 |
| `weekly` | 7일 |
| `monthly-or-on-demand` | 30일 |
| `quarterly-or-when-relevant` | 90일 |

- `last_successful_scan_at`가 `null`이면 due다.
- `ACTIVE`가 아닌 Source는 자동 Queue에서 제외한다.
- 날짜가 미래이거나 형식이 잘못되면 fail closed한다.
- due Source가 없어도 **신규 Source 확장**과 **새 글 확인 절차 감사**는 유지한다.
- Queue 생성은 Ledger의 scan timestamp·후보 수·기여 수를 변경하지 않는다.

## 4. Issue Queue 계약

Issue 본문은 최소 다음을 포함한다.

```text
고정 marker와 생성 기준일
UNVERIFIED_DISCOVERY 경고
cadence별 due Source
기존 Source의 새 글·수정 글 확인
신규 Source 사이트 탐색
원출처 역추적
published/updated/checked date
Source role과 Evidence tier 분리
current Base owner와 project consumer
claim ceiling·반례·권리·표현 위험
validation artifact와 rollback/discard 조건
ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | IGNORE | BLOCKED_UNVERIFIED | PROMOTION_CANDIDATE
```

Queue 안의 링크·제목·요약은 검증 전까지 `UNVERIFIED_DISCOVERY`다. Issue 완료 표시만으로 Ledger·Reference Catalog·Guide·프로젝트 정본이 갱신되었다고 간주하지 않는다.

## 5. 보안·권한

```yaml
permissions:
  contents: read
  issues: write
```

- Schedule과 수동 실행만 허용한다. 외부 PR 코드나 fork를 privileged token으로 실행하지 않는다.
- GitHub 공식 Action은 전체 commit SHA로 고정한다.
- Article HTML·PDF·첨부 파일을 자동 다운로드하거나 실행하지 않는다.
- 외부 URL·제목·본문을 shell 명령으로 해석하지 않는다.
- Queue script는 Python 표준 라이브러리만 사용한다.
- Issue 생성·갱신 외의 repository write를 하지 않는다.
- 자동 Canon, 자동 Guide 흡수, 자동 PR, 자동 merge를 하지 않는다.

## 6. Script 인터페이스

파일: `tools/periodic_source_scan_queue.py`

```python
CADENCE_DAYS: dict[str, int]
ISSUE_MARKER: str
ISSUE_TITLE: str

def load_ledger(path: Path) -> dict[str, object]: ...
def parse_iso_date(value: object) -> date | None: ...
def source_is_due(source: dict[str, object], today: date) -> bool: ...
def select_due_sources(payload: dict[str, object], today: date) -> list[dict[str, object]]: ...
def render_issue_body(payload: dict[str, object], today: date) -> str: ...
def main(argv: Sequence[str] | None = None) -> int: ...
```

CLI:

```text
python tools/periodic_source_scan_queue.py \
  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \
  --date 2026-08-14 \
  --output periodic-source-scan-queue.md
```

출력은 동일 입력에 대해 결정론적이어야 하며 UTC/로컬 실행 환경에 따라 바뀌지 않는다.

## 7. 첫 증분 조사 — 신규 Source 사이트

### `DiGRA Digital Library`

```yaml
role: PROFESSIONAL_PRACTICE
cadence: monthly-or-on-demand
coverage:
  - game research
  - onboarding
  - player expertise
  - narrative systems
  - mystery and environmental inference
claim_ceiling: conference paper 하나를 보편 설계 법칙이나 프로젝트 검증 결과로 만들지 않음
```

### `Game Studies`

```yaml
role: PROFESSIONAL_PRACTICE
cadence: quarterly-or-when-relevant
coverage:
  - game aesthetics
  - culture
  - communication
  - narrative and player interpretation
claim_ceiling: 이론·비평을 실제 플레이어 행동·시장 성과·구현 검증으로 과장하지 않음
```

### `MCLC Resource Center`

```yaml
role: PROFESSIONAL_PRACTICE + DISCOVERY_FEED
cadence: monthly-or-on-demand
coverage:
  - modern and contemporary Chinese literature
  - film and media
  - visual arts
  - popular culture
  - bibliography and expert lectures
claim_ceiling: 중국 전체·모든 시대·무협 장르의 단일 Canon으로 사용하지 않음
```

### `Library of Congress Web Cultures Web Archive`

```yaml
role: AUTHORITY_TARGET + DISCOVERY_FEED
cadence: quarterly-or-when-relevant
coverage:
  - web folklore
  - meme and vernacular culture preservation
  - archived source and dataset discovery
claim_ceiling: archive capture != 현재 의미·현재 호감·현재 유행 강도; 접근 제한·capture lag 기록
```

### `Data & Society`

```yaml
role: PROFESSIONAL_PRACTICE
cadence: monthly-or-on-demand
coverage:
  - platform incentives
  - media manipulation
  - disinformation
  - sociotechnical harm
  - community and power
claim_ceiling: 미국·정책·정치 맥락의 연구를 모든 팬덤·밈·지역의 의미로 일반화하지 않음
```

이 Source들은 첫 Scan Checkpoint에 기록하고 `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`의 기존 owner 경로로 연결한다. 영구 Ledger 승격은 Source 추가 Gate와 운영 상태 갱신을 별도 증거로 수행한다.

## 8. 첫 증분 조사 — 새 글 흡수 판정

### `ADAPT / TEST`

1. **게임 숙련도와 퍼즐 온보딩**
   - 일반 게임 숙련도를 participant covariate·segment로 기록한다.
   - 초보자와 숙련자의 탐색·완료·즐거움 차이를 같은 평균으로 지우지 않는다.
   - 한 상용 퍼즐 게임·자기보고 표본을 보편 인과 법칙으로 만들지 않는다.

2. **Holarchic narrative**
   - 선택적 조각마다 자체 이해 가능성, 전체 storyworld 기여, 추론 부담, 누락 복구를 기록한다.
   - 파편화 자체를 깊이·미스터리·환경 서사의 증거로 취급하지 않는다.

3. **Wuxia / Xianxia / Cultivation 분리**
   - 무협·선협·수선/수련·중국 판타지의 장르 논리와 문화·종교·우주론을 구분한다.
   - cosmology가 장식인지 실제 시스템 규칙인지 기록한다.

4. **플랫폼 고유 기호의 역사**
   - 밈·이모티콘·스티커를 플랫폼 상업화·거버넌스 단계와 함께 기록한다.
   - 표면상 같은 기호라도 플랫폼 고유 재맥락화와 공동체 권력 관계를 분리한다.

### `REFERENCE_ONLY`

- 전쟁 트라우마와 agency/inevitability의 형식적 분석
- 게임을 통한 지역·문화·기억 보존
- Black Myth: Wukong의 fan video·cloud-gaming·transnational discourse 분석

이들은 표현·팬덤·서사 검토의 반례와 질문을 제공하지만 프로젝트에 자동 적용하지 않는다.

## 9. 기존 owner 흡수

```text
퍼즐 온보딩·게임 숙련도
→ TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md
→ analyzing-and-refining-game-concepts
→ 실제 novice/expert playtest

파편화·환경 단서·storyworld inference
→ NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
→ NARRATIVE_AND_RELATIONSHIP_METHOD.md
→ mystery clue packet·unknown-player evidence

무협·선협·수련물
→ NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
→ 프로젝트 세계관·무공·문파·시스템 정본

밈·플랫폼 기호·팬덤
→ NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
→ 프로젝트 Tone·대사·UI·홍보 consumer
```

새 광역 Skill이나 별도 Evidence 권위를 만들지 않는다.

## 10. 검증

### 계약 테스트

- `tests/test_periodic_source_scan_queue.py`
  - cadence due 판정
  - null scan date
  - inactive source 제외
  - invalid/future date fail closed
  - 결정론적 Issue body
  - 신규 Source 확장·새 글·원출처·owner·검증·rollback 계약
  - CLI 출력
- `tests/test_periodic_external_source_watchlist.py`
  - Scheduled Queue의 권위 경계
  - 신규 Source 사이트와 새 packet field
  - 자동 본문 수집·Canon·PR 금지
- Evidence Knowledge Workflow가 두 테스트와 script compile을 실행한다.
- Base v9와 Game Project OS 회귀를 그대로 통과해야 한다.

### 운영 검증

병합 후 기본 브랜치에서 Workflow를 수동 실행한다.

```text
Workflow success
→ [Periodic Source Scan Queue] Issue 생성 또는 갱신
→ marker·기준일·due Source·신규 Source 확장·새 글 검토 계약 readback
→ 두 번째 실행에서 중복 Issue를 만들지 않고 같은 Issue 갱신
```

## 11. 적대적 검토

- Queue가 링크 dump 또는 뉴스 요약으로 변했는가?
- 신규 Source 수를 성과로 착각했는가?
- 제목·snippet만 읽고 owner 문서에 흡수했는가?
- 자동화가 Ledger timestamp를 거짓 갱신했는가?
- Schedule token으로 PR code·외부 script를 실행했는가?
- Article 본문·PDF·첨부를 자동 다운로드·실행했는가?
- Community Wiki·archive·trend·조회수를 Canon·현재 의미·호감·판매로 과장했는가?
- 연구 한 편을 보편 인과 법칙으로 승격했는가?
- 특정 문화·플랫폼·팬덤 표본을 다른 지역에 일반화했는가?
- 현재 owner·consumer·validation·rollback 없는 후보를 흡수했는가?
- 같은 open Issue를 갱신하지 않고 주간 Issue를 무한 생성했는가?

## 12. 완료와 Rollback

완료는 다음을 모두 요구한다.

```text
Intentional RED
→ exact-head GREEN
→ source/checkpoint readback
→ P0/P1 0
→ latest main 동기화
→ squash merge
→ post-merge CI
→ manual scheduled workflow success
→ 실제 Queue Issue 생성·중복 방지 확인
```

Rollback은 eventual feature squash merge commit을 revert한다. Queue Issue는 닫거나 본문에 `DISABLED_BY_ROLLBACK`을 기록한다. Runtime·Save/Data Schema·Skill Registry·프로젝트 Canon·외부 dependency migration은 없다.
