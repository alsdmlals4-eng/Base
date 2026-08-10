# developing-and-revising-serial-fiction Learning Log

## 2026-08-08 — BCP-2026-009 최초 구현

### 입력

- 《폭풍의 눈》 `작법서`와 225화 압축 초안의 작성·퇴고 문제
- 사용자 지정 한국 웹소설 인기작 표본 14종
- 한국콘텐츠진흥원 현업 웹소설 교육 자료와 공개 작법 자료
- Base의 기존 PLAN / BUILD / REVIEW, 적대적 검토, BCP, Registry·behavior eval 구조

### 학습

성공작의 공통 **문체**를 찾는 방식은 실패했다. 담백하고 낮은 피로도의 작품, 강한 1인칭 음성 작품, 고정보량 군상 미스터리, 반복 루틴 코미디, 고난도 루프물이 모두 성공할 수 있어 문장 길이·대사 비율·설명량의 단일 최적값을 공용화할 수 없다.

재사용 가능한 것은 표현보다 다음 독자 경험 계약이었다.

- Reader Promise
- Episode Value / State Change
- Local Payoff + Open Loop
- Information Legibility
- Pattern Variation
- Voice as Filter
- Consequence Memory
- Setup–Payoff Debt
- Reader Feedback as Evidence
- Platform Range, not Universal Count

### 적대적 검토에서 기각

- 인기작의 공통 문체를 Base 표준으로 만들기
- 5,000 / 5,500 / 6,000자 또는 프로젝트의 `공백 제외 2,000자`를 universal 완성 기준으로 만들기
- 모든 장면에 Story Grid·Save the Cat·Story Circle 등의 동일 공식을 강제하기
- 느린 장면 자체를 삭제 후보로 보기
- 모든 회차를 즉시 위험 직전에서 자르기
- 댓글 한두 개의 해결책을 그대로 요구사항으로 승격하기
- 현역 작가의 식별 가능한 voice·대사·비유를 모사하기

### TDD RED

```yaml
red_head: 6f615b7f4a617a2825cacf3433058f0415286740
workflow: Validate Game Project Operating System
run_id: 31254750559
job: ubuntu-contract
job_id: 93096401328
result: FAILED_AS_EXPECTED
suite_summary: 380 tests / 4 failures / 2 errors / 15 skipped
```

새 `tests/test_serial_fiction_discipline.py`가 기존 `tests/test_local_validation.py`에 집계되어 mandatory contract path에서 실제 실행됐다.

예상대로 실패한 항목:

- Skill/Knowledge Hub 미존재
- cold-start route 미존재
- Registry entry 미존재
- primary/non-selection behavior fixture 미존재

frozen v9.0 snapshot 보호 테스트는 RED 단계에서도 PASS했다.

### 구현 경계

새 ACTIVE Skill은 `developing-and-revising-serial-fiction` 하나만 추가한다. 게임 기획·적대 검토·정본 발행·Skill 진화 책임은 기존 owner를 유지한다. 프로젝트별 인물·세계관·고정 POV 수·장르 비율·플랫폼 생산 목표는 Base로 승격하지 않는다.

### 아직 미검증

```yaml
project_pilot: PROJECT_PILOT_NOT_RUN
human_reader_quality: HUMAN_NOT_RUN
commercial_outcome: NOT_RUN
platform_rules_future_stability: PLATFORM_REVERIFY_REQUIRED
```

## 2026-08-10 — BCP-2026-012·017 Canon migration debt와 reconciliation frontier

### 입력과 finding

- 한 프로젝트의 승인된 Canon 변경 뒤 기존 활성 DRAFT가 남아, 새 Decision의 즉시
  권위와 실제 원고 이관 완료를 한 상태로 처리하면 blind rewrite 또는 legacy 확산이
  생겼다.
- 이어진 reconciliation에서 candidate prefix 데이터가 저장돼도 declared validation
  gate가 실패하면 verified prefix로 승격할 수 없고, 미검증 경계를 derived consumer가
  normal continuity로 연결하면 사건 상태를 되감길 수 있었다.

### Base 결정

- 새 Skill·project schema·fixed work-unit을 만들지 않고 `canon-and-continuity`에
  `STRICT_NOW`, `FORBIDDEN_IN_NEW_OR_REVISED`,
  `BOUNDED_LEGACY_RECONCILIATION_DEBT`, `SCOPED_STRICT` lifecycle을 흡수한다.
- `actual_legacy_debt_consumers == declared_debt_consumers`를 bounded debt의
  fail-closed invariant로 두며, `PASS_WITH_KNOWN_DEBT`와
  `CANON_MIGRATION_COMPLETE`를 분리한다.
- `VERIFIED_PREFIX`, `DECLARED_MIGRATION_BOUNDARY`, `LEGACY_TAIL`,
  `FRONTIER_VERIFICATION_STATUS`를 schema-neutral topology로 두고, declared
  validation gate Green 전 candidate frontier를 verified로 부르지 않는다.
- derived consumer의 경계 추론과 duplicate current authority는 실패 상태로 드러내되,
  narrative event truth와 실제 field 이름은 프로젝트 정본이 소유한다.

### 검증 상한

```yaml
base_contract: VERIFIABLE
project_evidence: ONE_PROJECT_PATTERN_AND_COUNTEREXAMPLE
second_project_pilot: NOT_RUN
human_usability: HUMAN_NOT_RUN
project_runtime_validation: PROJECT_LOCAL
```

### 다음 검토 트리거

- 다른 연재소설 프로젝트에서 bounded debt 또는 frontier가 실제로 쓰일 때
- declared debt set을 wildcard로 느슨하게 만들려는 요구가 나올 때
- candidate frontier를 Green 전에 completion으로 보고하려는 경우
- derived consumer의 adjacency가 duplicate authority 또는 거짓 continuity를 만드는 경우
