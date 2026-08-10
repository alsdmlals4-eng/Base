# Periodic External Source Watchlist Design

## Goal

Base에 Hada GeekNews를 포함한 게임 제작 관련 외부 정보원을 **주기적으로 발견·교차검증·선별**하는 공용 Source Watchlist 계약을 추가한다. 이 계약은 외부 글을 Base 정본으로 직접 승격하지 않고, 기존 Evidence tier·Existing Solution First·적대적 검토·Base 변경 승인 경계를 재사용한다.

이번 승인 범위에는 초기 bootstrap으로 **2026-02-10 ~ 2026-08-10 최근 6개월**의 관련 글·업데이트를 가능한 범위에서 역추적해 반복되는 공용 개선 요소를 추출하는 작업도 포함한다. 조사 중 더 가치 있는 사이트가 발견되면 같은 평가 기준을 통과하는 경우 Watchlist에 추가할 수 있다.

## Existing Solution First

판정: `ABSORB`.

- 새 ACTIVE Skill: `0`
- 새 Work Mode: `0`
- 새 독립 BCP: `0` — 사용자가 이번 Base 변경을 직접 승인했으므로 현행 Base 계약상 별도 제안서 없이 작업 계약으로 처리한다.
- 소유 경계:
  - 외부 근거 판정: `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`
  - 출처 메타데이터·용도·재검증 조건: `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
  - 허브 발견성: `docs/knowledge/game-development/README.md`
  - 공용 기획 Evidence 흐름: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
  - 실패 가정·과잉 일반화 공격: `running-adversarial-review-and-refinement`
  - 실제 Base 정책/Skill 승격 필요 시: `managing-base-change-proposals`

## Why a separate watchlist reference

`REFERENCE_SOURCE_CATALOG.md`는 실제 Evidence에 사용할 수 있는 개별 출처 레코드의 권위 있는 인덱스다. 반면 주기 수집에는 "무엇을 자주 훑을지", "발견용 출처와 권위 출처를 어떻게 구분할지", "기사에서 원출처로 어떻게 역추적할지"가 필요하다. 이 책임은 기존 Catalog와 겹치지 않도록 별도 Reference로 두되, 실행 권한은 기존 Method와 Skill이 유지한다.

초기 6개월 조사는 일회성 보고서로 끝내지 않고 `최근 기간을 표본으로 Watchlist가 실제 Base 개선을 찾는지 검증하는 bootstrap evidence`로 취급한다.

## Source roles

Watchlist의 `source_role`은 Evidence tier와 다르다. 역할은 **수집 단계의 취급 방식**을 정하고, Evidence tier는 실제 채택 후보의 근거 강도를 정한다.

### AUTHORITY_TARGET

공식 플랫폼·엔진·표준에서 직접 변경 사실과 제약을 확인한다.

- Godot official documentation / blog
- Valve Steamworks documentation
- Android Developers Games
- Google Play developer policy / quality documentation
- Xbox Accessibility Guidelines

### PROFESSIONAL_PRACTICE

현업 발표·개발자 회고·전문 실무 가이드에서 적용 조건과 실패 사례를 찾는다.

- GDC Vault
- Game Developer
- Games User Research
- 80 Level
- The Level Design Book
- Game Accessibility Guidelines

### DISCOVERY_FEED

좋은 후보를 빠르게 찾는 탐색면이다. 이 출처 자체를 T1/T2 권위로 취급하지 않는다.

- Hada GeekNews
- GameDiscoverCo newsletter

### OBSERVATIONAL_DATA_OR_VENDOR_GUIDE

관찰 데이터나 도구/벤더 가이드를 가설과 측정 설계에 사용한다. 플랫폼 공식 사실·보편 규칙으로 과장하지 않는다.

- GameAnalytics
- SteamDB

## Adding new sites

조사 중 새 사이트가 발견되면 다음을 모두 확인한 뒤 Watchlist에 추가할 수 있다.

1. 현재 Source Pool과 **정보 역할이 중복되지 않거나**, 중복하더라도 원출처 접근성·현업 깊이·실패 사례·지역/플랫폼 Coverage를 실질적으로 보완한다.
2. 최근 6개월 안에 현재 게임 작업과 연결되는 유효한 자료가 확인된다.
3. 출처 역할과 예상 Evidence tier가 분리돼 기록된다.
4. 광고·SEO·제휴·벤더 이해관계가 있으면 한계에 명시한다.
5. 단일 인기 글만으로 영구 Watchlist에 넣지 않는다. 반복 가치 또는 독립적인 권위가 있어야 한다.

## Processing pipeline

```text
SCHEDULED_DISCOVERY
→ CANDIDATE_CAPTURE
→ DUPLICATE_AND_CURRENT_BASE_CHECK
→ ORIGINAL_SOURCE_BACKTRACE
→ SOURCE_ROLE_AND_EVIDENCE_TIER
→ FRESHNESS_AND_SCOPE_CHECK
→ DECISION_RELEVANCE_FILTER
→ EVIDENCE_PACK
→ ADVERSARIAL_ATTACK
→ CRITIQUE_VALIDATION
→ ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
→ NO_CHANGE | EVIDENCE_ONLY_UPDATE | LOW_RISK_BOUNDED_UPDATE | BCP_OR_USER_DECISION
→ REGRESSION_RECHECK
```

## Recent-six-month bootstrap

초기 bootstrap 기간은 `2026-02-10T00:00:00+09:00`부터 `2026-08-10T23:59:59+09:00`까지다.

목표는 글 개수 집계가 아니라 최근 자료에서 **반복되고 서로 독립적으로 확인되는 개선 패턴**을 찾는 것이다.

```text
각 Source의 archive/blog/changelog/recent listing 확인
→ 기간 내 관련 항목 inventory
→ 제목·날짜·원 URL·주제·핵심 주장 최소 기록
→ 중복 주장을 topic cluster로 묶음
→ 발견 출처에서 원출처로 역추적
→ Base 현행 규칙과 compare
→ 이미 충분히 covered면 NO_CHANGE
→ 부족한 Reference/Evidence만 최소 보강
→ 정책 의미 변화는 BCP_OR_USER_DECISION
```

사이트 특성상 전체 archive를 기계적으로 열람할 수 없거나 paywall·검색 색인 한계가 있으면 `PARTIAL_INDEX_REVIEW`로 표시하고 "6개월치 전부 읽음"이라고 주장하지 않는다. 반대로 공식 changelog/archive가 기간 전체를 노출하면 그 범위를 `FULL_INDEX_REVIEW`로 기록할 수 있다.

## Scheduler boundary

Base는 scheduler·webhook·백그라운드 실행기가 아니다. 이 문서는 "주기적으로 실행될 때 무엇을 해야 하는지"만 정의한다.

- 실제 cadence는 ChatGPT Automation, GitHub Actions 또는 사용자가 선택한 외부 scheduler가 소유한다.
- 권장 기본값은 **주 1회**지만 Base의 불변 규칙이 아니다.
- 실행되지 않은 scan을 완료로 보고하지 않는다.
- scheduler가 없어도 수동 scan에 같은 계약을 적용할 수 있다.
- 주기 실행은 마지막 성공 scan 이후 새 항목을 우선하되, source policy/changelog가 크게 바뀌면 재검토 기간을 확장한다.

## Candidate capture

후보마다 최소 다음을 기록한다.

```yaml
candidate_id:
discovered_from:
original_url:
title:
published_or_updated_at:
checked_at:
source_role:
provisional_evidence_tier:
topics: []
base_owner_candidate:
current_base_overlap:
why_it_might_change_a_decision:
original_source_backtrace:
license_or_copying_notes:
```

본문 전체를 저장소에 복제하지 않는다. 제목·URL·날짜·요약·판정·필요한 짧은 사실 메타데이터만 보존한다.

## Original-source backtrace rule

Hada, 뉴스레터, 기사, 벤더 블로그, 커뮤니티에서 발견한 주장에는 가능한 한 다음 우선순위를 적용한다.

```text
발견 글
→ 링크된 원문/공식 문서/원 발표/원 데이터
→ 현재 버전·게시일·지역·플랫폼 조건 확인
→ Base의 기존 Reference Catalog와 중복·충돌 확인
```

원출처를 확인하지 못하면 확정 정책으로 승격하지 않고 `REFERENCE_ONLY`, `TEST`, 또는 `BLOCKED_UNVERIFIED`로 남긴다.

## Change authority

### 자동 반영 가능한 후보

현재 승인 범위 또는 현행 저위험 자동승인 계약 안에서 다음 조건을 **모두** 만족하는 경우에만 최소 반영할 수 있다.

- 가역적이고 작은 변경
- 기존 책임 경계·Skill ID·Schema·보안·권한·라이선스 의미를 바꾸지 않음
- 정본을 새로 만들지 않고 기존 owner의 Reference/Evidence를 보강함
- 원출처와 현재 Base를 대조해 중복·충돌이 없음
- 관련 검증과 적대적 재검토를 실행할 수 있음

### 자동 확정 금지

다음은 사용자 결정 또는 현행 BCP lifecycle을 유지한다.

- 제품/게임 방향과 핵심 플레이 경험
- Base 공용 정책 의미 변경
- ACTIVE Skill 추가·제거·ID·owner 변경
- Workflow 실행 권한·write permission·보안·인증 변경
- 라이선스·법적 판단
- 대규모 구조 변경 또는 migration
- 미검증 외부 주장을 Hard Rule로 승격

## Adversarial lenses

각 후보는 최소 다음 공격을 통과해야 한다.

- 인기 글 또는 높은 추천 수를 품질·진실의 증거로 오인했는가?
- 기사 요약이 원출처의 조건·반례·버전을 왜곡했는가?
- AAA·F2P·모바일·특정 장르 사례를 1인/소규모 PC 게임에 과잉 일반화했는가?
- SteamDB 같은 제3자 관찰값을 Valve 공식 사실로 표현했는가?
- GameAnalytics 벤치마크를 모든 장르의 목표값으로 고정했는가?
- 80 Level의 개별 제작 사례를 보편 파이프라인으로 강제했는가?
- 접근성 가이드를 실제 사용자 검증이나 플랫폼 인증으로 과장했는가?
- 외부 자료 때문에 새 Skill/Template가 불필요하게 늘어났는가?
- 기존 Base에 이미 같은 원칙이 있는데 이름만 바꿔 중복했는가?
- 최근 6개월이라는 기간 때문에 장기적으로 검증된 원칙을 무시하거나 반대로 최신 유행을 과대평가했는가?

## Validation

Repository contract는 다음을 검증한다.

- Watchlist Reference가 허브와 Evidence Method에서 한 단계로 발견된다.
- Hada와 게임 제작 핵심 Source Pool이 명시돼 있다.
- 조사 중 새 Source를 추가할 수 있는 조건이 명시돼 있다.
- `DISCOVERY_FEED`는 직접 권위가 아님이 명시돼 있다.
- 원출처 역추적·freshness·중복 검사·적대적 검토·disposition이 모두 존재한다.
- 2026-02-10 ~ 2026-08-10 bootstrap 범위와 FULL/PARTIAL index review 구분이 존재한다.
- Base가 scheduler 자체라고 주장하지 않는다.
- 새 ACTIVE Skill을 추가하지 않는다.
- 전용 테스트가 `validate-evidence-knowledge.yml`에서 실제 실행된다.

## Protected boundaries

- `[수정제안서]/PROPOSAL_REGISTRY.json` 변경 없음
- `skills/SKILL_REGISTRY.json` 변경 없음
- release lock / frozen snapshot 변경 없음
- GitHub workflow 권한은 `contents: read` 유지
- 외부 원문 전체 복제 금지
- 실제 scan·적용·검증을 실행하지 않았는데 완료로 보고하지 않음
