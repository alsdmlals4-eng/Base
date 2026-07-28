# 게임 기획·플레이어 경험 Guide

## 1. 목적

이 Guide는 기능 목록이 아니라 **플레이어가 누구이며, 어떤 상황에서, 무엇을 선택하고, 어떤 감정과 기억을 얻어, 왜 다시 행동하는지**를 중심으로 게임을 기획하고 검증하는 방법을 설명한다.

실행 책임은 `analyzing-and-refining-game-concepts`, `identifying-project-core`, `establishing-project-core`, `designing-vertical-slices`, `governing-game-user-research-coverage`가 가진다.

참고 기반:

- MDA는 Mechanics·Dynamics·Aesthetics를 통해 설계·개발·비평·연구의 관점을 연결한다: https://aaai.org/papers/ws04-04-001-mda-a-formal-approach-to-game-design-and-game-research/
- Games User Research는 연구 질문에 맞춰 관찰·인터뷰·분석·설문 등 방법을 선택해야 한다: https://gamesuserresearch.com/choose-the-right-playtest-method/
- 전문 플레이테스트는 무엇을 언제 시험할지, 참가자·방법·수집·분석·보고를 연결한다: https://gamesuserresearch.com/how-to-run-a-games-user-research-playtest/

## 2. 플레이어 약속

먼저 한 문장으로 다음을 고정한다.

> `[대상 플레이어]가 [플레이 상황]에서 [핵심 행동·선택]을 통해 [감정·판타지]를 경험하고, [차별 원리] 때문에 이 게임을 기억한다.`

필수 질문:

- 대상 플레이어는 누구인가?
- 언제·어디서·얼마나 오래 플레이하는가?
- 첫 세션에서 무엇을 이해해야 하는가?
- 핵심 선택은 무엇이며 왜 고민되는가?
- 플레이어가 통제한다고 느끼는 부분은 무엇인가?
- 실패해도 무엇을 배우고 보존하는가?
- 어떤 보상·기억이 다음 행동을 부르는가?
- 비슷한 게임과 구분되는 차별 원리는 무엇인가?

좋은 플레이어 약속은 기능명을 나열하지 않는다.

나쁜 예:

> 카드, 성장, 장비, 보스, 로그라이트가 있는 게임.

좋은 예:

> 상대가 드러낸 단서를 읽고 여러 수를 미리 계획해 숨은 의도를 꺾는 무협 전술 게임.

## 3. 코어 추적 구조

```text
대상 플레이어
→ 플레이 상황
→ 감정·판타지
→ 핵심 선택
→ 반복 행동
→ 규칙·자원·제약
→ 즉시 피드백
→ 결과·보상·기억
→ 다음 선택
→ 장기 약속
```

모든 주요 시스템은 다음 중 하나로 분류한다.

| 분류 | 의미 |
|---|---|
| `AMPLIFY` | 핵심 재미를 직접 강화 |
| `SUPPORT` | 이해·속도·변주·접근성을 지원 |
| `NEUTRAL` | 코어와 약한 관계, 범위 후보 |
| `CONFLICT` | 코어 판단을 대체하거나 흐림 |
| `UNPROVEN` | 가능성은 있으나 증거 없음 |

`CONFLICT`와 `UNPROVEN`을 인기 기능이라는 이유로 추가하지 않는다.

## 4. Mechanics → Dynamics → Experience

MDA를 그대로 용어 암기용으로 쓰지 않고 프로젝트 작업에 맞춰 다음처럼 확장한다.

| 단계 | 질문 |
|---|---|
| `Mechanics` | 규칙·수치·입력·자원·제약은 무엇인가? |
| `Dynamics` | 플레이어와 시스템이 반복해서 어떤 행동·상황을 만드는가? |
| `Experience` | 플레이어는 무엇을 이해·고민·예측·느끼고 기억하는가? |
| `Evidence` | 실제 행동·자기보고·성능·제작 증거는 무엇인가? |

```yaml
feature_or_rule:
mechanics:
player_action:
system_response:
dynamics:
expected_experience:
undesired_experience:
feedback_channel:
evidence_needed:
```

규칙이 원하는 Experience를 만들지 못하면 수치를 조금 올리는 것보다 구조·정보·타이밍을 먼저 점검한다.

## 5. 핵심 루프·세션 루프·메타 루프

### Micro Loop

초 단위의 행동과 피드백이다.

```text
인지 → 선택 → 입력 → 반응 → 결과 이해 → 다음 의도
```

### Session Loop

한 번 플레이에서 의미 있는 목표와 정산까지 연결한다.

```text
진입 → 준비 → 핵심 행동 반복 → 변곡점 → 결과 → 정산 → 복귀
```

### Meta Loop

여러 세션이 정체성·숙련·관계·수집·세계 변화로 쌓이는 구조다.

메타 성장이 핵심 판단을 대신하면 코어가 약해질 수 있다. 강한 수치만으로 문제를 건너뛰게 하지 않고 더 다양한 선택·정보·표현을 제공하는지 본다.

## 6. 게임 필

게임 필은 “타격감이 좋다” 같은 추상 표현이 아니다. 다음 지연과 정보 채널을 관찰한다.

- 입력 인식
- 행동 시작
- 핵심 접촉·판정
- 시각·음향·진동 피드백
- 수치·상태 변화
- 결과 원인 이해
- 다음 입력 가능 시점

```yaml
input_to_motion_ms:
action_to_contact_ms:
contact_to_result_ms:
result_legibility:
recovery_or_cancel:
visual_audio_haptic_channels:
accessibility_alternative:
```

빠르기만이 목표가 아니다. 전략 게임은 충분한 예고와 결과 설명이, 액션 게임은 반응성과 판정 일치가 중요할 수 있다.

## 7. DDD와 보상 사다리

Base에서 DDD는 `Digital Dopamine Design`이며 의학적 도파민 측정이나 중독 진단이 아니다.

관찰 축:

- 첫 의미 있는 보상까지 걸리는 시간
- 행동-피드백 지연
- 보상 명료성
- 보상 밀도와 반복 피로
- Micro→Session→Meta 보상 사다리
- 다음 행동 의도
- 보상 인플레이션
- 실패·중단 후 복귀 가능성

보상 사다리 예:

```text
Micro: 입력 직후 명확한 변화
→ Encounter: 선택의 결과와 학습
→ Session: 빌드·관계·기록 정산
→ Meta: 새로운 가능성·정체성·세계 변화
```

자극을 늘리는 대신 “왜 이 결과가 나왔으며 무엇을 다음에 다르게 할지”가 보이게 한다.

## 8. 난이도와 실패 후 학습·복구

난이도는 하나의 숫자가 아니라 다음 장벽의 조합이다.

- 규칙 이해
- 정보 탐색
- 의사결정 수
- 기억 부담
- 반응·정밀 입력
- 시간 제한
- 손실·복구 비용
- 반복 길이
- 감각 장벽

Microsoft XAG는 난이도가 게임 자체의 고정 속성이라기보다 플레이어 능력과 게임 장벽의 관계에서 생긴다고 설명한다: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/108

실패 설계 질문:

- 실패 원인을 플레이어가 설명할 수 있는가?
- 거짓 정보나 보이지 않는 규칙이 원인인가?
- 실패 전에 예고와 선택 기회가 있었는가?
- 다시 시도할 때 새로운 전략이 가능한가?
- 잃는 것과 보존되는 것이 명확한가?
- 같은 긴 구간을 불필요하게 반복하는가?
- 도움·난이도·시간·입력 대안이 코어를 훼손하지 않고 제공되는가?

## 9. 온보딩과 점진적 공개

온보딩은 설명문을 많이 보여주는 일이 아니다.

```text
플레이어의 현재 질문
→ 필요한 정보 하나
→ 즉시 행동
→ 관찰 가능한 결과
→ 짧은 복기
→ 다음 개념
```

검수 항목:

- 첫 30초·3분·10분의 목표가 보이는가?
- 설명 전 필요한 맥락이 있는가?
- 용어와 UI가 같은 의미를 쓰는가?
- 한 번에 몇 개의 새 규칙을 요구하는가?
- 튜토리얼 전용 규칙과 본편 규칙이 다른가?
- 스킵·재열람·실습·실패 복구가 가능한가?
- 숙련 플레이어의 재시작을 방해하지 않는가?

튜토리얼 이해도는 자기보고만으로 통과시키지 않는다. 실제로 목표를 찾고, 입력하고, 규칙을 설명하고, 다음 행동을 선택하는지 관찰한다.

## 10. 벤치마킹

벤치마킹 전에 비교 차원과 결정 질문을 고정한다.

비교 대상:

- 직접 경쟁작
- 인접 장르
- 같은 문제를 다른 방식으로 푼 게임
- 실패·혼합 반응 사례
- 비게임 인터랙션 참고

분리할 근거:

- 공식 제품 사실
- 개발자 의도·Postmortem
- 플레이어 행동 증거
- 플레이어 자기보고
- 모델 해석

다음과 같은 표면 복사는 금지한다.

> 성공한 게임에 일일 퀘스트가 있으므로 추가한다.

대신 질문한다.

> 그 게임에서 일일 구조가 어떤 플레이 상황과 메타 루프를 해결했으며, 우리 프로젝트의 세션 길이·콘텐츠 생산량·피로와 같은 조건인가?

판정은 `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 남긴다.

## 11. Games User Research

연구 질문에 맞는 방법을 선택한다.

| 알고 싶은 것 | 우선 방법 | 주의 |
|---|---|---|
| 어디서 막히는가? | 관찰·게임플레이 영상 | 원인은 추가 질문 필요 |
| 왜 그렇게 선택했는가? | 즉시 인터뷰·회상 질문 | 사후 합리화 가능 |
| 얼마나 자주 일어나는가? | 텔레메트리·퍼널 | 감정·이유를 단정하지 않음 |
| 만족·기대·선호는 무엇인가? | 설문·인터뷰 | 실제 행동과 분리 |
| 두 설계 중 어느 쪽이 낫나? | 통제된 비교·A/B | 주요 변수 하나 |
| 첫인상·약속이 전달되나? | Concept Test·Store/Trailer Test | 구매 의도와 실제 구매는 다름 |

Games User Research의 일반적인 방법을 질문에 맞춰 조합하는 것이 중요하다: https://academic.oup.com/book/26677/chapter/195455798

### 플레이어 행동과 플레이어 자기보고

- 행동 증거: 무엇을 했는가
- 플레이어 자기보고: 무엇을 느끼고 기억하고 기대한다고 말하는가
- 연구자 해석: 왜 그런 결과가 생겼다고 추론하는가

세 층을 같은 문장으로 합치지 않는다.

## 12. 플레이테스트 계약

```yaml
hypothesis:
decision_if_supported:
decision_if_refuted:
build_and_version:
tester_segment:
prior_exposure:
recruitment_and_access:
tasks_or_play_window:
observation_points:
interview_questions:
survey_items:
telemetry_events:
funnel_steps:
primary_metric:
guardrail_metrics:
success_failure_stop:
bias_and_validity_risks:
```

- 친구·개발자·기존 팬과 목표 신규 플레이어를 분리한다.
- 첫 경험이 중요하면 기존 기획을 모르는 테스터를 사용한다.
- 관찰·인터뷰·설문·분석을 목적에 맞게 조합한다.
- 성공 기준을 결과를 본 뒤 바꾸지 않는다.
- 재미와 사용성, 난이도와 접근성, 콘텐츠 양과 반복 제작성을 분리한다.

## 13. Vertical Slice 연결

Vertical Slice는 기능 목록이 아니라 대표 경험의 처음부터 끝까지다.

```text
진입
→ 핵심 정보 인지
→ 선택·행동
→ 시스템 반응
→ 위험·변곡점
→ 결과 이해
→ 보상·기록·복귀
```

다음을 함께 검증한다.

- 핵심 세일즈포인트
- 일반 반복 플레이
- 조작·정보·아트·UI·사운드 품질
- 접근성·성능
- 저장·복구
- 콘텐츠 제작 파이프라인
- 두 번째 같은 유형의 콘텐츠 반복 가능성
- 외부 플레이어 행동·자기보고

## 14. 제거·축소 우선순위

기능을 추가하기 전에 다음 순서로 검토한다.

```text
REMOVE
→ REDUCE
→ MERGE
→ CLARIFY
→ FEEDBACK 강화
→ ADD
```

제거 질문:

- 이 기능이 없어지면 핵심 재미가 사라지는가?
- 다른 기능이 같은 역할을 하는가?
- 플레이어가 이해하거나 기억해야 할 비용이 가치보다 큰가?
- 콘텐츠·아트·QA·저장·밸런스 비용이 반복 가능한가?
- 세일즈포인트와 관련이 있는가?

## 15. Output Contract

```md
## 플레이어 약속·대상 플레이어·플레이 상황
## 감정·판타지·핵심 선택·반복 행동
## Mechanics / Dynamics / Experience / Evidence
## Micro·Session·Meta Loop
## 게임 필·보상 사다리·난이도·실패 복구
## 온보딩·점진적 공개
## 벤치마크·행동 증거·플레이어 자기보고
## 플레이테스트 계약
## Vertical Slice 대표 흐름
## 유지·강화·수정·제거·보류
## 미검증·다음 결정
```
