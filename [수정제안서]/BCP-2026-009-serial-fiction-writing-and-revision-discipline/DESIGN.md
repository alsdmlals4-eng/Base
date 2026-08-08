# 연재소설 집필·퇴고 Discipline 설계

## 1. 설계 목표

Base의 기존 PLAN / BUILD / REVIEW와 적대적 검토 구조를 유지하면서, 소설 작업에만 필요한 입력·산출물·품질 기준을 하나의 specialist Skill로 소유한다.

목표는 ‘인기 웹소설처럼 쓰기’가 아니다. 목표는 다음 실패를 반복 가능하게 예방하는 것이다.

- 회차가 길거나 짧다는 이유만으로 완성도를 판정함
- 장면이 사건 요약으로 지나가고 독자 체험이 부족함
- POV가 바뀌어도 문장과 판단이 동일함
- 정보가 많아질수록 누가 무엇을 원하는지 추적 불가
- 루프·학원·괴담·업무 구조가 원패턴화됨
- 복선이 쌓이기만 하고 회수가 늦거나 사라짐
- 댓글 한두 개를 작품 방향으로 즉시 승격함
- 인기작의 문장·플롯·개그를 그대로 모사함

## 2. 왜 기존 게임 기획 Skill에 흡수하지 않는가

`analyzing-and-refining-game-concepts`와 공유하는 활동은 벤치마크·사용자/독자 반응 분석이다. 하지만 책임 경계는 다르다.

| 차원 | 게임 기획 | 연재소설 |
|---|---|---|
| 주 입력 | 게임 코어·시스템·플레이 행동·PoC | 정본·로그라인·아크·회차·원고·POV·독자 반응 |
| 주 산출물 | 시스템 방향·PoC·플레이테스트·재조정 | 회차 설계·장면 원고·퇴고본·복선/회수·피드백 수정안 |
| Quality Bar | 플레이어 행동·공정성·피드백·성능 등 | 인과·가독성·voice·장면 변화·회차 보상·continuity |
| 대표 실패 | 재미 가설 미검증·밸런스·불공정 | 요약문체·POV 평준화·원패턴·미회수·설명 과잉 |
| 검증 단위 | 플레이·빌드·telemetry | 장면·회차·아크·원고 diff·독자 반응 표본 |

따라서 기존 owner의 단순 mode 확장보다 독립 specialist가 적합하다.

## 3. Skill 인터페이스

Skill ID: `developing-and-revising-serial-fiction`

### 입력

```yaml
project_canon_and_priority:
source_material_and_adaptation_boundary:
work_identity_and_reader_promise:
arc_episode_or_scene_scope:
current_draft:
pov_and_character_voice_state:
setup_payoff_ledger:
continuity_and_information_state:
reader_feedback_evidence:
platform_and_release_constraints:
protected_strengths:
requested_output:
```

입력이 모두 필요하다는 뜻은 아니다. 현재 작업에 필요한 최소 입력만 읽고, 모르는 항목은 확정 사실로 추측하지 않는다.

### Mode

1. `canon-and-continuity`
   - 원작·로그·사용자 결정·기존 정본의 우선순위를 복원한다.
   - 사건 결과와 각색 가능 영역을 분리한다.
2. `arc-and-episode-design`
   - 독자 약속, 상태 변화, 회차 가치, 반복 변주, 장기 목표 연결을 설계한다.
3. `pov-and-character-voice`
   - 정보 접근권·편견·욕망·어휘·관찰 대상을 기준으로 POV를 분리한다.
4. `draft-and-prose`
   - 사건 요약을 감각·행동·대사·판단의 장면으로 극화하고 불필요한 해설을 줄인다.
5. `serial-pacing-and-payoff`
   - 회차 경계, local payoff, open loop, 후폭풍, setup/payoff 부채를 점검한다.
6. `reader-feedback-and-revision`
   - 댓글·리뷰를 증상별로 묶고 프로젝트 코어와 원고 증거에 대조해 수정 가설을 만든다.

한 요청에서 필요한 Mode만 선택한다. 모든 Mode를 매번 강제하지 않는다.

## 4. 공용 Gate

### Reader Promise Gate

독자는 현재 아크/회차에서 어떤 경험을 기대해야 하는가? 제목·소개·초반 약속과 현재 전개가 다른 장르를 무단으로 약속하지 않는가?

### Episode Value Gate

회차 종료 시 다음 중 하나 이상이 실제로 변해야 한다.

- 목표
- 정보
- 관계
- 위험
- 위치/접근권
- 능력/자원
- 감정/신념
- 평판/세력 상태

길이만 늘고 상태가 그대로면 실패 후보다.

### Local Payoff Gate

모든 회차가 ‘절정’일 필요는 없지만, 독자가 이번 회차를 읽은 대가로 얻는 것은 있어야 한다. 작은 질문의 답, 감정 결산, 관계 변화, 규칙 이해, 성공/실패 결과 중 하나를 명시한다.

### Open Loop Gate

다음 회차 질문을 남기되 매번 문장 중간 절단이나 즉시 위험만 사용하지 않는다. 미해결 질문, 새로운 비용, 관계의 불확실성, 바뀐 목표도 훅이 될 수 있다.

### Information Legibility Gate

정답·괴이의 원리·배후는 숨길 수 있다. 그러나 장면 단위로 다음은 추적 가능해야 한다.

- 현재 POV가 누구인가
- 누가 무엇을 원하는가
- 즉시 장애가 무엇인가
- 선택/행동 결과 무엇이 바뀌었는가

### Pattern Variation Gate

같은 골격이 반복될 경우 직전 유사 에피소드와 비교해 최소 하나를 바꾼다.

- 규칙/예외
- 비용
- 보상
- 해결 주체
- 감정
- 관계
- 정보 공개 방식
- 실패 형태

### Consequence Memory Gate

중대한 실패·폭력·능력·선택 뒤에는 다음 회차 이후에 남는 흔적이 있는지 확인한다.

### Setup–Payoff Debt Gate

복선은 ID 또는 식별 가능한 질문 단위로 `SETUP / RECALL / PARTIAL_PAYOFF / PAYOFF / RETIRED / DEFERRED` 상태를 가진다. 모든 떡밥을 빠르게 회수할 필요는 없지만 장기 미회수 부채를 관찰할 수 있어야 한다.

### Reader Feedback Evidence Gate

반응을 다음 세 층으로 나눈다.

```text
RAW_REACTION
→ SYMPTOM_CLUSTER
→ REVISION_HYPOTHESIS
```

`“전개가 답답하다”`는 raw reaction이다. 바로 ‘전투를 추가한다’로 가지 않고, 주인공 주도권·상태 변화·정보 보상·반복 설명 중 무엇이 증상을 만드는지 원고에서 확인한다.

## 5. Hard Rule이 아닌 진단 Lens

다음은 선택적 Lens다. 전 장면에 강제하지 않는다.

- Story Grid 5 Commandments
- Save the Cat beat
- Story Circle
- Hero’s Journey
- 대사/행동/묘사 비율
- 장면당 기능 개수
- 양자택일 위기
- 특정 문장 길이
- 특정 회차 글자 수

Lens가 작품의 목적보다 우선하면 `FRAMEWORK_OVERFIT`으로 판정한다.

## 6. 분량 정책

Base는 `5,000자`, `5,500자`, `6,000자`를 보편 Hard Rule로 두지 않는다.

프로젝트는 목표 플랫폼의 현재 계약·상업 표본을 확인해 다음을 기록한다.

```yaml
count_basis: spaces_included | spaces_excluded | platform_defined
platform_minimum_or_contract:
production_target_range:
observed_comparable_range:
scene_completion_override:
exception_reason:
```

완성도 판정 순서는 `회차 가치 → 장면/회차 완결성 → 리듬 → 플랫폼 제약 → 생산 목표 글자 수`다.

## 7. 벤치마크 학습 계약

작품별로 아래 네 층을 분리한다.

```text
PRODUCT_FACT
READER_RESPONSE
CRAFT_HYPOTHESIS
TRANSFER_DECISION
```

예: 플랫폼 조회수는 PRODUCT_FACT지만 `그 문체 때문에 성공했다`는 인과 증거가 아니다. 리뷰의 반복 불만은 READER_RESPONSE이며, 실제 텍스트/구조와 대조한 뒤에만 CRAFT_HYPOTHESIS가 된다.

Transfer decision:

- `ADOPT_INVARIANT`
- `ADAPT_AS_LENS`
- `PROJECT_ONLY`
- `REJECT_COPY`
- `INSUFFICIENT_EVIDENCE`

## 8. 저작권·독창성 경계

- 인기작의 장문 원문·대표 문장·대사·비유를 학습 자료로 Base에 복사하지 않는다.
- 특정 현역 작가의 문체를 그대로 모사하는 지시를 Skill default로 만들지 않는다.
- 구조적 기능, 독자 경험, 장면 리듬, 정보 배치 같은 높은 수준의 원리로 추상화한다.
- 프로젝트 최종 문장은 프로젝트 고유 POV·정본·인물 관계에서 새로 작성한다.

## 9. Knowledge 구조

초기 버전은 4개 파일만 둔다.

- `README.md`: 라우팅과 권한
- `SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`: 전체 작법·장면·POV·퇴고
- `SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md`: 회차 경계·hook·payoff·분량·복선 부채
- `READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md`: 외부 작품·댓글·리뷰의 근거 처리

POV 전용 Guide와 복선 전용 Guide는 실제 사용에서 크기·독립 소비자가 생길 때만 분리한다.

## 10. Behavior eval 경계

Primary examples:

- “이 5천자 웹소설 1화를 2차 퇴고해줘. POV와 다음 화 흡입력도 봐줘.”
- “원본 TRPG 로그의 결과는 보존하면서 이 장면을 소설 장면으로 각색해줘.”
- “독자 댓글에서 답답하다는 반응이 반복되는데 실제 원고 문제를 진단해줘.”

Non-selection examples:

- “이 전투 시스템의 DPS와 적 AI 난이도를 설계해줘.” → 게임 기획 Skill
- “이 문단 맞춤법만 교정해줘.” → 일반 문서/쓰기 경로, broad fiction Skill 불필요
- “게임 개발 유튜브 대본을 써줘.” → YouTube Skill

## 11. 검증 상한

Base 구현이 증명할 수 있는 것:

- 라우팅 존재
- 책임 경계
- Gate와 비사용 조건
- behavior fixture coverage
- 정본·Registry·문서 참조 일관성

Base 구현만으로 증명할 수 없는 것:

- 특정 작품의 판매 증가
- 독자 만족도 향상
- 현업 편집자의 품질 승인
- 모든 장르에서의 보편적 최적 회차 길이
- 특정 플랫폼 정책의 영구 불변성

이 항목은 `NOT_RUN / HUMAN_NOT_RUN / PLATFORM_REVERIFY_REQUIRED` 상태를 유지한다.
