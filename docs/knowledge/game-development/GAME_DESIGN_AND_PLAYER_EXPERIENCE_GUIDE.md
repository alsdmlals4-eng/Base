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

### PLAYER_EXPERIENCE_EVIDENCE_GATE

검증 이름을 하나로 뭉뚱그리지 않는다. 아래 네 증거는 서로 다른 질문에 답하며, 앞 단계의 `PASS`가 뒤 단계의 `PASS`를 뜻하지 않는다.

| evidence layer | 증명하는 것 | 증명하지 않는 것 |
|---|---|---|
| `TECH_EVIDENCE` | 코드·데이터·Schema·엔진 실행의 기술적 상태 | 사람이 이해·재미·기억을 얻는지 |
| `UI_EVIDENCE` | 렌더·입력·포커스·해상도·시각 상태 | 첫 사용자가 다음 행동을 찾는지 |
| `HUMAN_USABILITY_EVIDENCE` | 처음 보는 사람이 조작·정보 구조·다음 행동을 이해하는지 | 의도한 감정·고민·기억이 생기는지 |
| `PLAYER_EXPERIENCE_EVIDENCE` | 의도한 고민·감정·선택·보상·기억이 실제 플레이에 생기는지 | 장기 유지율·판매 성과 |

사람 관찰을 실행하지 않았으면 `HUMAN_USABILITY_EVIDENCE=NOT_RUN`, `PLAYER_EXPERIENCE_EVIDENCE=NOT_RUN`을 유지한다. 작은 내부 테스트도 테스터의 사전 노출, 과제·질문, 실제 행동·답변, 표본 한계를 함께 기록한다. 자동 테스트·UI 렌더·텍스트 체크만으로 사람 경험의 상태를 올리지 않는다.

`EVIDENCE_LAYER_IS_NOT_A_UNIVERSAL_RELEASE_GATE`: evidence layers define what a result can prove; they do not create a universal participant count or force every project to run a player-experience study. A project may declare `PROJECT_DECLARED_VALIDATION_POLICY: MACHINE_PRIMARY_FINAL_USER_REVIEW`, making deterministic/runtime/export/package/CI evidence its primary acceptance route and reserving `FINAL_USER_REVIEW` for a separately requested final inspection. `FIVE_PERSON_COMPREHENSION_NOT_BASE_DEFAULT` and `PLAYER_EXPERIENCE_STUDY_NOT_BASE_DEFAULT` do not weaken an explicitly approved project study, a platform/device requirement, or release/legal/accessibility owner. Machine evidence never becomes human evidence.

### P04_PLAYER_VALUE_TO_EVIDENCE_TRACE

P04의 핵심 기획·연구·Vertical Slice 판단은 기능 목록이 아니라 다음 한 줄 추적으로 연결한다.

```yaml
player_promise:
meaningful_choice:
expected_experience:
research_question:
observable_signal:
evidence_ceiling:
slice_acceptance:
```

- `player_promise`와 `meaningful_choice`는 코어가 플레이어에게 약속하는 가치와 실제 고민을 고정한다.
- `research_question`은 방법을 고르기 전에 **어떤 결정을 바꾸기 위해 무엇을 배울지**를 명시한다.
- `observable_signal`은 행동·자기보고·이벤트·퍼널·관찰 중 어떤 증거로 기대 경험을 확인할지 정한다.
- `evidence_ceiling`은 현재 증거로 주장 가능한 최대 수준이다. 기술·정적·UI 증거만으로 사람의 이해·감정·기억을 PASS하지 않는다.
- `slice_acceptance`는 신호가 지지·반박·미검증일 때 `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP` 등 다음 결정을 연결한다.

`analyzing-and-refining-game-concepts`는 현재 결정을 위한 `DECISION_SPECIFIC_RESEARCH`를 수행하고, `governing-game-user-research-coverage`는 연구 질문에 필요한 coverage와 evidence gap을 감사한다. `designing-vertical-slices`는 이 trace를 대표 구간 acceptance로 소비한다. 프로젝트 코어의 기존 사실 판정과 새/변경 코어 확정 권한은 각각 `identifying-project-core`, `establishing-project-core`에 남긴다.

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

## 8.1 게임 시스템 설계

게임 시스템 설계는 기능 목록이나 Godot Node 목록이 아니다.

```text
플레이어 경험 목표
→ 플레이어가 읽을 정보
→ 고민할 선택과 위험
→ 입력·행동·자원·상태·규칙
→ 시스템 반응·결과·피드백
→ 실패 후 학습·복구
→ 다음 행동과 검증 Evidence
```

각 시스템은 책임·입력·출력·비책임·정본·실패·검증을 가진다. 인접 시스템과 같은 상태를 중복 소유하지 않으며, 새로운 기능을 추가하기 전에 `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK 강화 → ADD` 순서로 검토한다.

상세 실행은 `analyzing-and-refining-game-concepts: system-design`과 `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`가 책임진다.

## 8.2 난이도 장벽 프로필

난이도는 적 체력 하나가 아니라 규칙 이해, 정보 탐색, 의사결정, 기억·주의, 반응·정밀 입력, 시간 압박, 자원·손실, 반복·복구 거리, 감각·입력 장벽, 적 조합·공간·카메라 압박의 조합이다.

대상 플레이어별로 `의도한 도전 / 요구 능력·지식 / 예고·정보 / 복구·대안 / 측정 / 접근성 위험`을 기록한다. 난이도와 접근성 보조를 같은 축으로 합치지 않는다.

## 8.3 공정성 안전 규칙

높은 난이도에서도 다음을 유지한다.

- 보이지 않는 정보나 플레이어 입력 직접 읽기로 즉시 처벌하지 않는다.
- 강한 공격은 시각·음향·동작 중 하나 이상으로 예고한다.
- 카메라 밖 즉사, 연속 기절, 기상 직후 재경직, 회피 불가능 조합을 제한한다.
- 실패 원인과 다음에 바꿀 행동을 설명할 수 있어야 한다.
- 정보 채널을 색 하나에만 의존하지 않는다.

공정성은 쉬움이 아니라 정보·인과·대응 가능성이 유지되는 어려움이다.

## 8.4 적 전투 AI와 공격·위협 예산

영리함과 압박량을 분리한다.

```text
개별 적 판단
→ 감지·기억·행동 후보·Utility·쿨다운

전투 조율자
→ 역할·위치 슬롯·공격 예산·위협 예산·동시 강공격 제한

난이도·페이싱 디렉터
→ 웨이브·증원·예산 상한·회복 구간·긴장도·다음 전투 조절
```

공격 권한을 받지 못한 적은 멈추지 않고 선회·엄폐·장전·경고·재배치를 수행한다. 쉬움 난이도에서 적을 멍청하게 만들기보다 반응시간, 동시 공격, 전술 빈도, 회복 폭과 자원 지원을 조절한다.

## 8.5 긴장도 곡선

```text
Build Up
→ Sustain Peak
→ Peak Fade
→ Relax
→ 다음 Build Up
```

계속 최고 압박을 유지하면 아슬아슬함이 아니라 피로가 된다. Peak 뒤에는 결과 이해, 회복, 보상, 장비·경로 선택 시간이 필요하다.

## 8.6 고정·적응형 난이도

고정 난이도는 먼저 경험 의도를 정한 뒤 다음 순서로 조절한다.

1. 정보·예고·반응·회복·동시 공격
2. 측면·엄폐·정보 공유·역할 교대 등 전술 빈도
3. 웨이브·특수 적·회복 구간·자원
4. 체력·피해·속도 등 수치

적응형 난이도는 장기 실력과 단기 스트레스를 분리한다. 히스테리시스, 최소 상태 유지시간, 변경 쿨다운, 한 번에 한 단계, 안전한 적용 시점을 둔다. 현재 플레이어가 보고 있는 적의 체력·피해를 갑자기 바꾸는 것을 기본값으로 삼지 않는다.

**성공을 벌주지 않는다.** 좋은 장비·숙련 직후 적 수치를 같은 비율로 올려 성장 체감을 무효화하지 않고, 이후 구간에서 더 다양한 조합·선택·전술을 제공한다.

텔레메트리는 전투 시간, 최저 체력, 피해 폭증, 동시 공격자, 예산 사용량, 무력화 시간, 카메라 밖 피해, 자원 소비, 사망 직전 상태와 난이도 변경 이유를 기록할 수 있다. 감정과 원인은 플레이 영상·관찰·인터뷰를 결합해 판정한다.

## 8.7 MINIGAME_NARRATIVE_FUNCTION_GATE

별도 미니게임은 "조작 하나를 더한다"는 이유로 채택하지 않는다. 아래 질문에 답할 수 있을 때만 독립 시스템으로 검토한다.

```yaml
main_game_information_used:
player_decision_tested:
narrative_or_system_result_changed:
failure_learning:
rule_learning_time:
reusability:
content_cost:
flow_interrupt_cost:
```

- 본편 또는 직전 장면에서 얻은 정보·규칙을 실제 판단에 사용한다.
- 성공·실패가 사건·자원·기록·다음 선택 등 의미 있는 결과를 바꾼다.
- 실패가 오답 이유·새 정보·위험 사례처럼 다음 시도의 학습을 남긴다.
- 공통 프레임·데이터 변형으로 재사용할 수 있는지, 더 짧은 선택지·공통 인터랙션이 같은 경험을 낼 수 없는지를 먼저 비교한다.

퍼즐·전투·제작 조작 자체가 프로젝트 코어라면 이를 미니게임으로 낮춰 평가하지 않는다. 이 경우 `MINIGAME_NARRATIVE_FUNCTION_GATE` 대신 프로젝트 코어 계약과 `CORE_INTERACTION_EVIDENCE`로 대표 행동·선택·결과를 검증한다.

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

### FIRST_10_MINUTES_CONTRACT

첫 10분은 고정된 시간 제한이 아니라 대표 경험의 압축판이라는 기본값이다. 장르·세션 길이·의도한 불확실성에 맞춰 시간을 조정하되, 행동 목적까지 흐려지지 않게 아래 흐름을 최소 한 번 확인한다.

```text
대표 문제
→ 대표 행동
→ 첫 선택
→ 첫 결과
→ 다음 질문
```

- 전체 세계관·규칙·기능을 한 번에 설명하는 것을 목표로 하지 않는다.
- 공포·미스터리의 정보 비공개는 허용하지만, 플레이어가 지금 무엇을 시도할 수 있는지는 읽을 수 있어야 한다.
- 첫 세션의 실제 사람 검증에서는 문제·행동·선택 이유·결과 원인·다음 시도 의도를 각각 관찰한다.

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
## P04 player-value-to-evidence trace·evidence ceiling·slice acceptance
## Micro·Session·Meta Loop
## 게임 필·보상 사다리·난이도·실패 복구
## 온보딩·점진적 공개
## 벤치마크·행동 증거·플레이어 자기보고
## 플레이테스트 계약
## Vertical Slice 대표 흐름
## 유지·강화·수정·제거·보류
## 미검증·다음 결정
```
