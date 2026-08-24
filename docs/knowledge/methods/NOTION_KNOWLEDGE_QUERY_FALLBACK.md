# Notion Knowledge Query Fallback · 조회 제한 시 정본 감사 대체 경로

- 상태: 공용 companion method
- 소유 관계: `NARRATIVE_WORLD_KNOWLEDGE_MODEL.md`의 Notion 조회·감사 실행 보조
- 목적: Notion SQL/Data Source query가 플랜·쿼터·일시 제한으로 실행되지 않을 때 작업을 멈추거나 정본을 추측하지 않고, 기존 View/Search/Fetch 기반으로 안전하게 감사를 계속한다.
- 비목표: Search 결과를 SQL 전수조회와 동등하다고 주장하거나, 검색 hit만으로 Canon을 자동 승격하는 것

`NOTION_QUERY_FALLBACK`

## 1. 발동 조건

다음 중 하나면 fallback을 사용한다.

- SQL/Data Source query usage limit 또는 plan gate
- 특정 query mode만 일시적으로 unavailable
- SQL 전체 조회 비용이 현재 bounded 작업에 비해 과도함

권한 부족, 페이지 미접근, 데이터 자체 부재를 쿼터 제한으로 오인하지 않는다. 원인을 구분하지 못하면 `QUERY_CAUSE_UNVERIFIED`로 남긴다.

## 2. 기본 순서

```text
SQL / direct data-source query unavailable
→ existing filtered View 실행 시도
→ Data Source scoped Search
→ 후보 Page Fetch
→ project source exact-check
→ targeted update only
→ readback
→ anti-stale sweep
```

핵심 토큰:

- `VIEW_MODE_FIRST`
- `DATA_SOURCE_SCOPED_SEARCH`
- `PAGE_FETCH_READBACK`
- `SOURCE_EXACT_CHECK`
- `TARGETED_UPDATE_ONLY`

## 3. `VIEW_MODE_FIRST`

이미 사람용 Gallery/Table/View가 현재 필터 계약을 보유하면 먼저 그 View를 실행한다.

장점:
- 기존 Project / Type / Approval filter를 재사용한다.
- 실제 사용자가 보는 카드 집합을 직접 검증할 수 있다.
- SQL quota와 별개의 view-mode 경로가 제공되는 환경에서는 비용을 줄일 수 있다.

View가 실행되지 않으면 자동으로 빈 결과라고 해석하지 않는다. 다음 단계인 Data Source scoped Search로 전환한다.

## 4. `DATA_SOURCE_SCOPED_SEARCH`

Data Source 자체를 scope로 제한해 stale token, 인물명, 관계명, frontier 표현을 검색한다.

예시 검색 축:

```text
old production frontier
old candidate range
legacy spelling
known conflict name
missing character name
relationship name
source authority phrase
```

검색 결과는 **후보 집합**이다.

`SEARCH_NOT_EXHAUSTIVE`

Search는 ranking·index 상태에 영향을 받을 수 있으므로 다음을 금지한다.

- 검색 0건 = 존재하지 않음으로 단정
- 검색 hit = 현재 Canon으로 자동 승격
- 검색 결과만으로 삭제
- 검색 순위를 중요도 순위로 간주

## 5. `PAGE_FETCH_READBACK`

검색 hit는 반드시 개별 Page Fetch로 속성·본문·현재 상태를 읽는다.

확인 항목:

- Project relation
- Type
- Canon Status
- Text Approval
- Scope
- Current State
- Summary
- 필요한 Relation / Event linkage

사람용 Home·Gallery에 실제 노출되는지 확인해야 하면 linked database View도 별도로 readback한다.

## 6. `SOURCE_EXACT_CHECK`

Notion 문구가 stale 또는 누락처럼 보이면 바로 고치지 않는다.

먼저 현재 프로젝트의 Source Authority에서 exact evidence를 확인한다.

```text
latest user decision
→ project-declared source authority
→ current GitHub/production canon
→ approved Notion decision/evidence
→ candidate/legacy
```

특히 다음은 exact-check 우선 대상이다.

- 등장 여부
- 이름·별칭
- 생존/사망/소실
- 성별·변장·외형
- 세력 소속
- Part / Arc / production frontier
- 관계 변화
- 능력 공개·비용

근거가 없으면 `UNKNOWN` 또는 `REVIEW_REQUIRED`로 유지한다.

## 7. `TARGETED_UPDATE_ONLY`

Fallback 감사 중에는 전체 페이지/DB를 재작성하지 않는다.

허용:
- stale Current State 교정
- 잘못된 fixed range 표현을 frontier-independent 표현으로 교정
- 누락된 Lite Character Card 추가
- 실제 Event participant relation 보완
- 오염 가능 Entity를 `UNKNOWN / REVIEW_REQUIRED`로 강등

금지:
- 검색 결과만으로 record 삭제
- Candidate를 APPROVED로 자동 승격
- 미승격 원고를 production으로 선반영
- unrelated Home/System 구조 개편

## 8. 승인·정본 안전장치

`NO_AUTO_PROMOTION_FROM_SEARCH`

Search/Fetch가 사실을 발견하더라도 프로젝트의 기존 promotion/approval 계약을 우회하지 않는다.

예:

```text
source file에서 Ch31 내용 발견
≠ Ch31 production canon

현재 production frontier = Ch30
→ Ch31은 candidate evidence로만 사용
→ bounded promotion 통과 뒤 current state 갱신
```

사용자 직접 확정이 기존 Source보다 높은 권위인 프로젝트에서는 해당 Decision을 우선한다.

## 9. 전수성 보완 · Anti-stale sweep

SQL 전수 조회가 아니므로 감사 종료 전 서로 다른 검색축을 최소 3회 교차한다.

권장:

1. **range/frontier sweep** — 과거 `001–020`, `026–040 재검증` 같은 고정 문구
2. **entity sweep** — 현재 source의 이름 있는 반복 등장 인물과 Knowledge Master 비교
3. **state sweep** — alive/dead/candidate/approved/source authority 같은 고위험 상태
4. **relation/event sweep** — Event Participants와 주요 Relation 누락 비교

0건 결과는 삭제 근거가 아니라 `NO_HIT_IN_SEARCH` 증거일 뿐이다.

## 10. 완료 조건

Fallback 감사 완료를 주장하려면 최소 다음이 필요하다.

```text
applicable View or scoped Search executed
+ relevant pages fetched
+ source exact-check completed for every mutation
+ targeted updates only
+ final page/view readback
+ unresolved conflict explicitly retained
```

그리고 보고에는 다음을 구분한다.

- `VERIFIED_BY_VIEW_OR_FETCH`
- `SOURCE_EXACT_CHECKED`
- `SEARCH_NO_HIT_ONLY`
- `SQL_FULL_AUDIT_NOT_RUN`

SQL 전수 감사가 실행되지 않았으면 이를 숨기지 않는다. 다만 bounded 목표를 View/Search/Fetch/Source-check로 충분히 검증했다면 작업 자체를 중단할 필요는 없다.

## 11. COC-Fiction 검증 사례 · 2026-08-24

Notion SQL형 Data Source query 사용량 제한 상황에서 다음 fallback을 실제 적용했다.

```text
Character Gallery view-mode readback
→ Knowledge Master scoped Search
→ 밀리/하템/탈론/가론/온돌로프/케인/페스타 Page Fetch
→ 사용자 지정 021–040 DOCX exact-name / event 확인
→ stale Current State·Candidate 표현 교정
→ 누락 Character Card 노아/라자크/쿠바라 추가
→ Ch027/029/030 Event Participants 보완
→ final Gallery view readback
```

검증 결과:
- SQL 제한 때문에 작업을 중단하지 않았다.
- Search 0건을 삭제 근거로 쓰지 않았다.
- current production 밖의 Ch031+ 정보는 APPROVED로 선반영하지 않았다.
- 사람용 Gallery에서 새 APPROVED 카드 노출을 최종 확인했다.

이 사례는 fallback의 실무 재현 증거이며, Search가 SQL과 완전히 동등하다는 증거는 아니다.
