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

## 2026-08-11 — 캐릭터 개성·상대 위상 무결성

### 입력과 finding

- 연재소설 각색 과정에서 설정상 강한 조연이 전투 결과·소문으로만 강하다고 설명되고, 원본에 있던 실제 대련·전투 기능이 압축본에서 빠진 사례가 확인됐다.
- 반대로 주인공을 강하게 보이게 하려고 적대자의 판단·훈련·위험성을 낮추면 승자까지 약해 보이는 문제가 반복됐다.
- 동일 작품 안에서도 강자들이 모두 같은 방식으로 강하면 캐릭터 구분과 전투 기억점이 함께 흐려졌다.

### Base 결정

- 새 독립 ACTIVE Skill을 추가하지 않고 기존 `developing-and-revising-serial-fiction`에 `character-and-opponent-integrity` mode와 조건부 reference를 흡수한다.
- 인물 식별은 `관찰 필터 / voice·사고 / 문제 해결 / 화면 안 강함 증명 / 인간적 매력 / 대가를 만드는 결점 / 대표 하이라이트`로 분리한다.
- 중요 상대는 최소 한 번 자기 규칙을 강제하는 `own turn`을 갖고, 승리·생존은 `SKILL / TACTIC / RULE / RELATION` 중 인물 고유 방식과 비용으로 설명한다.
- 원작·로그·구초안 각색은 신규 장면 발명 전 `SOURCE FUNCTION → CURRENT REPRESENTATION → KEEP/RESTORE/REWORK/NEW/REMOVE`를 대조한다.
- 설정상 강한 주요 인물의 위상을 화면 밖 보고만으로 끝내는 것과 주인공 승리를 위한 상대 약체화를 별도 실패 상태로 둔다.

### 경계

- Base는 작품별 캐릭터 이름·전투력·누가 누구를 좋아하는지·고정 전투 횟수를 소유하지 않는다.
- 전투가 없는 인물에게 강제 전투를 붙이지 않는다. **전투 강자라고 정본상 주장하는 중요 인물**의 증명 부채가 있을 때만 화면 안 증명을 요구한다.
- 조연의 위상 증명은 주연의 중앙 선택·결말을 대신하면 실패다.

### 검증 상한

```yaml
base_contract: DOCUMENTED
source_project_evidence: ONE_SERIAL_FICTION_PROJECT
second_project_pilot: NOT_RUN
human_reader_quality: NOT_RUN
model_behavior_eval: NOT_RUN
```

### 다음 검토 트리거

- 다른 연재소설 프로젝트에서 `설정상 강자지만 약해 보임` 또는 `주인공 때문에 적이 바보가 됨` 문제가 반복될 때
- 캐릭터 식별 카드가 모든 인물에게 기계적으로 강제되어 관료화될 때
- own turn 규칙이 모든 단역·잡몹까지 과적용될 때

## 2026-08-11 — 정보·선택·하이라이트·복선 구조 재조사

### 입력과 finding

- Coc-Fiction의 전체 캐릭터 → 주요 사건/하이라이트 → 복선·정보 구조 감사를 시작하기 전에 현행 작법 계약을 최신 편집·작가 실무와 다시 대조했다.
- 미스터리의 답을 숨기는 것과 독자가 현재 행동을 이해할 맥락을 숨기는 것은 다르며, POV가 자연스럽게 아는 사실을 독자만 속이려고 우회하면 false suspense가 된다.
- 캐릭터 설정표의 성장 선언보다 압박 속 선택의 반복·회귀·변형이 실제 아크 증거다.
- 대표 하이라이트는 화려함만이 아니라 캐릭터 고유성·실제 유능함·대가·결정권·후폭풍을 필요한 범위에서 화면 안에 남겨야 한다.
- 장기 복선은 설치 개수보다 recall·recontextualization·payoff 이후 행동 변화가 중요하다.

### Base 결정

- 새 broad Skill을 만들지 않고 기존 `developing-and-revising-serial-fiction`의 조건부 companion guide `SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md`로 흡수한다.
- 정보 공개 감사에 `WITHHOLD_INFORMATION_NOT_CONTEXT`와 `READER_KNOWLEDGE_MATRIX`를 추가한다.
- 캐릭터 아크는 `CHOICE_PROOF`, 후반의 큰 선택은 `SURPRISING_BUT_COHERENT`로 감사한다.
- 대표 캐릭터 하이라이트는 `IDENTITY + COMPETENCE + COST + CHOICE + CONSEQUENCE`를 점수표가 아닌 렌즈로 사용한다.
- 장기 복선·반전은 필요할 때 `SETUP → RECALL → RECONTEXTUALIZE → PARTIAL_PAYOFF → PAYOFF → AFTERMATH`로 추적한다.

### 외부 Evidence와 경계

- working editor/developmental-editing guidance, author/editor craft guidance, 2025–2026 foreshadowing·character-arc 자료, 한국 웹소설 작가·PD 실무 신호를 교차 참고했다.
- 이 자료들은 판매 인과의 실증 연구가 아니며, 특정 플랫폼의 일시적 취향·특정 작품의 반전 위치·클리프행어 빈도·특정 작가의 문체와 장면 배열은 Base universal rule로 승격하지 않는다.
- 체크리스트를 만족시키려고 이미 잘 작동하는 장면을 복잡하게 만들지 않는다.

### TDD evidence

```yaml
red_head: 58b55bf2a3d728521497781671a0d367ff13f26b
workflow: Validate Game Project Operating System
run_id: 31455877107
job: ubuntu-contract
job_id: 93669443479
result: FAILED_AS_EXPECTED
cause: companion guide absent
```

새 contract가 `SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md` 부재만 정확히 잡는 RED를 확인한 뒤 구현했다.

### 검증 상한

```yaml
base_contract: VERIFIABLE
source_project_application: IN_PROGRESS
second_project_pilot: NOT_RUN
human_reader_response: HUMAN_NOT_RUN
commercial_effect: NOT_RUN
platform_specific_fit: PLATFORM_REVERIFY_REQUIRED
```
