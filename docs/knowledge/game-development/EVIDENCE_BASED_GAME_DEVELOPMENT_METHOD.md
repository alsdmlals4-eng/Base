# 근거 기반 게임 개발 Method

## 1. 목적

이 Method는 게임 기획·아트·개발·AI 활용·벤치마킹·검증·출시 판단을 외부 근거와 실제 프로젝트 증거로 개선하는 공용 절차다.

목표는 자료를 많이 수집하는 것이 아니라 다음을 연결하는 것이다.

```text
현재 결정 질문
→ 필요한 근거
→ 적용 조건과 반례
→ 프로젝트 기획·작업 계약
→ 실제 제작·플레이·검증
→ 학습·Base 승격 후보
```

실행 권한은 기존 Skill이 가진다. 이 Method는 `analyzing-and-refining-game-concepts`, `governing-game-user-research-coverage`, `designing-art-prompts-and-technique-cards`, `designing-vertical-slices`, `reviewing-and-validating-project-changes`, `running-adversarial-review-and-refinement`, `evolving-project-discipline-skills`, `managing-base-change-proposals`가 공유하는 근거 구조를 제공한다.

## 2. Coverage 12영역

모든 작업에서 12영역을 전부 조사하지 않는다. 현재 결정에 필요한 영역만 선택한다. 근거가 아직 없으면 `NOT_STARTED`, 적용되지 않으면 이유를 가진 `NOT_APPLICABLE`로 기록한다.

1. 프로젝트 코어·게임 기획
2. 플레이어 경험·게임 필·보상·난이도
3. 아트 디렉션·캐릭터·환경·UI·애니메이션
4. 내러티브·세계관·콘텐츠 설계
5. UX·UI·접근성
6. 사운드·음악·오디오 정보 전달
7. Godot·데이터·저장·성능·플랫폼 기술 기획
8. QA·자동화·런타임·회귀 검증
9. 프로덕션·범위·Vertical Slice·반복 제작성
10. 벤치마킹·Games User Research·텔레메트리
11. AI 협업·Prompt·Evals·보안·권리·독립 검수
12. 출시·스토어·마케팅 약속·출시 후 학습

Coverage는 체크박스 수가 아니라 **책임 원본·현재 상태·근거·다음 결정**을 가진다.

```yaml
coverage_id:
question:
owner_skill:
canonical_source:
status: NOT_STARTED | IN_PROGRESS | EVIDENCED | NOT_APPLICABLE | BLOCKED
current_evidence_ids: []
missing_evidence:
next_decision:
```

## 3. Evidence 층

### `T1_PRIMARY_OFFICIAL`

공식 플랫폼·엔진·표준·원 논문·개발사 원문·실제 프로젝트 실행 로그다. 제품 규칙·기능·요건·버전·정책·측정 방법 확인에 우선한다.

예:

- Godot 공식 문서
- Steamworks·Google Play·Android Developers 공식 문서
- Microsoft Xbox Accessibility Guidelines
- NIST AI RMF
- AAAI·학술지 원 논문
- 프로젝트 실제 코드·데이터·테스트·캡처

### `T2_PROFESSIONAL_PRACTICE`

GDC 발표·개발자 Postmortem·스튜디오 기술 블로그·현업 가이드·전문가 사례다. 적용 배경·조직·제작 규모·도구·실패 조건을 함께 기록한다.

### `T3_PLAYER_BEHAVIOR`

플레이테스트 관찰·텔레메트리·퍼널·입력 로그·완주·이탈·시간·선택 행동이다. 무엇을 했는지는 보여 주지만 감정과 원인을 자동으로 증명하지 않는다.

### `T4_PLAYER_SELF_REPORT`

인터뷰·설문·Steam/Google Play 리뷰·커뮤니티·지원 요청이다. 기대·감정·이유를 이해하는 데 유용하지만 실제 행동과 기억을 정확히 재현한다고 가정하지 않는다.

### `T5_SYNTHESIS`

전문 서적·리뷰 논문·체계적 문헌 검토·여러 현업 사례를 종합한 자료다. 원자료와 해석 범위를 구분한다.

### `T6_AI_INFERENCE`

AI 요약·비교·아이디어·분류·가설이다. 탐색과 초안에는 유용하지만 독립 권한이 없으며 원출처·실제 파일·검증 없이 `VERIFIED_SOURCE`가 될 수 없다.

## 4. Evidence 상태

| 상태 | 의미 |
|---|---|
| `VERIFIED_SOURCE` | 원출처·날짜·버전·맥락을 확인함 |
| `PARTIALLY_VERIFIED` | 일부 필드나 원문만 확인함 |
| `CONTEXT_LIMITED` | 다른 장르·규모·플랫폼·표본이라 적용 범위가 제한됨 |
| `STALE_RECHECK_REQUIRED` | 정책·도구·가격·버전·시장 상태가 바뀔 수 있어 적용 전 재검증 필요 |
| `CONFLICTING_EVIDENCE` | 신뢰 가능한 근거끼리 다른 결론을 보임 |
| `UNVERIFIED` | 출처·실행·표본·맥락을 확인하지 못함 |

문서·영상·리뷰의 존재는 Evidence 상태를 자동으로 올리지 않는다.

## 5. 개선 판정

| 판정 | 의미 |
|---|---|
| `ADOPT` | 현재 프로젝트 조건과 일치하며 거의 그대로 채택 |
| `ADAPT` | 원리만 가져와 프로젝트 코어·제작성에 맞게 변형 |
| `TEST` | 가능성은 있지만 PoC·Vertical Slice·플레이테스트·Eval 필요 |
| `AVOID` | 코어 충돌·실패 사례·장벽·비용·권리 위험 때문에 피함 |
| `IGNORE` | 현재 결정과 관련성이 낮음 |
| `REFERENCE_ONLY` | 실행하지 않고 사례·반례·역사 자료로만 보존 |

판정은 다음 항목을 함께 본다.

```yaml
player_value:
core_alignment:
production_capacity:
technical_risk:
accessibility_barrier:
performance_cost:
security_privacy_license:
evidence_strength:
validation_plan:
```

## 6. 전체 실행 흐름

```text
BASELINE_RECOVERY
→ DECISION_QUESTION
→ COVERAGE_SELECTION
→ SOURCE_PLAN
→ EVIDENCE_COLLECTION
→ SOURCE_VALIDATION
→ SYNTHESIS
→ ADOPT/ADAPT/TEST/AVOID/IGNORE/REFERENCE_ONLY
→ PROJECT_CANON_UPDATE
→ TECHNICAL/ART/CONTENT FEASIBILITY
→ ADVERSARIAL_REVIEW
→ PLAYTEST/EVAL/VALIDATION
→ LEARNING_LOG
→ 필요 시 BCP
```

### 6.1 `BASELINE_RECOVERY`

먼저 다음을 비교한다.

```text
최신 사용자 지시
→ 프로젝트 AGENTS·START_HERE·Active Context
→ CURRENT_CONFIRMED_DECISIONS
→ 질문별 책임 원본
→ 같은 Goal의 열린·최근 병합 PR
→ 실제 코드·데이터·Scene·자산·테스트
→ 프로젝트 Sheet가 구성된 경우 해당 tab
```

기존 결정·근거·구현이 있으면 되묻거나 중복 조사하지 않는다.

### 6.2 `DECISION_QUESTION`

조사 질문은 “좋은 게임 기획 사례를 찾아라”가 아니다.

좋은 형식:

> `[대상 플레이어]가 [상황]에서 [핵심 행동·판단]을 이해하고 반복하게 만들기 위해, [현재 결정 A/B] 중 무엇을 유지·변경·시험해야 하는가?`

필수 필드:

- 현재 결정과 가설
- 바뀔 수 있는 결정
- 바꾸지 않을 코어·보호 대상
- 대상 플레이어와 플레이 상황
- 비교 차원
- 필요한 근거와 중단 조건

### 6.3 `COVERAGE_SELECTION`

결정 질문에 영향을 주는 Coverage만 선택한다. 예를 들어 카드 전투 UI 가독성은 게임 기획, UX·접근성, 아트, 플랫폼 기술, 플레이테스트가 연결될 수 있지만 사운드·출시를 자동 포함하지 않는다.

### 6.4 `SOURCE_PLAN`

자료 수집 전 다음을 정한다.

| 항목 | 질문 |
|---|---|
| 사실 | 실제 규칙·기능·정책·버전은 무엇인가? |
| 현업 | 어떤 제작 조건과 실패를 경험했는가? |
| 행동 | 플레이어가 실제로 무엇을 했는가? |
| 자기보고 | 무엇을 기대·이해·불편해했는가? |
| 반례 | 성공하지 못했거나 혼합된 사례는 무엇인가? |
| 적용 | 우리 프로젝트와 같은 점·다른 점은 무엇인가? |
| 검증 | 무엇을 직접 시험해야 하는가? |

최신 외부 후보가 필요한 L1 이상 조사에서는 `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`를 **발견용 Reference**로 사용할 수 있다. Watchlist는 Evidence 권위가 아니라 Source Pool·freshness·`ORIGINAL_SOURCE_BACKTRACE`만 책임진다. 발견 글은 현재 결정과 관련성이 있을 때만 수집하고, 가능한 경우 공식 문서·원 발표·원 데이터로 되돌아간 뒤 이 Method의 Evidence tier를 부여한다.

주기 scan의 결과가 `NO_CHANGE`여도 정상이다. 새 글이 있다는 이유만으로 기존 Base·프로젝트 결정을 바꾸지 않는다.

### 6.5 `EVIDENCE_COLLECTION`

`templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`에 다음을 기록한다.

- Evidence ID
- 제목·기관·저자
- URL·게시일·확인일·버전
- 근거 층과 상태
- 핵심 내용과 직접 관찰 사실
- 해석과 한계
- 현재 프로젝트와 같은 점·다른 점
- 관련 Case Card

원문 전체를 복제하거나 긴 인용문을 저장하지 않는다.

`playtest`를 Evidence로 기록할 때는 이름만으로 증거 강도를 추정하지 않는다. 최소한 다음을 함께 기록해 QA·동료 피드백·구조화된 사용자 연구·행동 관찰·자기보고를 구분한다.

```yaml
playtest_purpose:
participant_source:
build_or_task_scope:
observed_behavior:
self_report:
facilitation_or_test_context:
```

관찰과 자기보고가 모두 있으면 각각의 Evidence 성격을 분리하고, 친구·팀 내부 세션을 타깃 플레이어 대표 표본으로 자동 일반화하지 않는다.

### 6.6 `SOURCE_VALIDATION`

다음을 검토한다.

- 원출처인가, 재인용인가?
- 게시일과 현재 버전이 일치하는가?
- 제품 사실과 작성자 의견이 분리됐는가?
- 플레이어 리뷰의 플랫폼·언어·플레이타임·패치 맥락이 있는가?
- 행동과 자기보고가 혼동되지 않았는가?
- 성공 사례만 선택하지 않았는가?
- 이해관계·홍보·샘플 편향이 있는가?
- AI가 만든 출처·숫자·인용이 실제 존재하는가?

### 6.7 `SYNTHESIS`

각 발견을 다음 구조로 묶는다.

```text
관찰 사실
→ 적용 조건
→ 현재 프로젝트와 차이
→ 원인 가설
→ 반례
→ 개선 후보
→ 검증 방법
```

관련 없는 인기 기능을 추가하지 않는다.

### 6.8 `PROJECT_CANON_UPDATE`

사용자 승인 또는 기술적으로 확정 가능한 개선만 프로젝트 책임 원본·Issue·Plan·Sheet에 반영한다.
