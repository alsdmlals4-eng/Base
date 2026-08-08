# 연재소설 회차·장면 Quality Gates

이 reference는 `developing-and-revising-serial-fiction`의 회차 설계·집필·퇴고에서 필요한 Gate만 빠르게 확인하는 실행 카드다. 작품 정본과 세부 장르 규칙은 프로젝트가 소유한다.

## 1. Reader Promise

```yaml
promise:
current_arc_fulfillment:
scene_or_episode_relation:
status: PASS | READER_PROMISE_MISSING
```

Reader Promise는 특정 사건을 매번 반복하라는 뜻이 아니라 독자가 계속 받을 경험의 종류다.

## 2. Episode Value

회차 종료 전후를 비교한다.

```yaml
before:
after:
changed_axes:
  - goal
  - information
  - relationship
  - danger
  - location_or_access
  - ability_or_resource
  - emotion_or_belief
  - reputation_or_faction
status: PASS | EPISODE_VALUE_MISSING
```

상태가 바뀌지 않은 채 설명·전투·이동만 늘면 실패 후보다.

## 3. Local Payoff + Open Loop

```yaml
local_payoff:
open_loop:
hook_type: QUESTION | COST | RELATIONSHIP | CHANGED_GOAL | RULE_EXCEPTION | IMMEDIATE_DANGER | NONE
status: PASS | LOCAL_PAYOFF_MISSING
```

모든 회차를 즉시 위험 직전에서 자르지 않는다.

## 4. Information Legibility

미스터리 정답은 숨겨도 다음은 추적 가능해야 한다.

```yaml
pov:
immediate_goal:
obstacle_or_risk:
changed_state:
status: PASS | INFORMATION_LEGIBILITY_FAILURE
```

## 5. Pattern Variation

직전 유사 에피소드와 비교한다.

```yaml
repeated_skeleton:
changed_dimensions:
  - rule_or_exception
  - cost
  - reward
  - solving_character
  - emotion
  - relationship
  - information_release
  - failure_shape
status: PASS | PATTERN_REPETITION_UNVARIED
```

## 6. Consequence Memory

중대한 실패·폭력·능력·선택의 흔적:

```yaml
trigger:
persistent_effect:
  information:
  injury_or_limit:
  relationship:
  reputation:
  taboo:
  debt:
status: PASS | CONSEQUENCE_MEMORY_MISSING
```

## 7. Setup–Payoff Debt

장기 질문만 추적한다.

```yaml
setup_id:
question:
state: SETUP | RECALL | PARTIAL_PAYOFF | PAYOFF | RETIRED | DEFERRED
last_touched_episode:
next_expected_touch:
```

모든 작은 정보를 ID화하지 않는다. 장기 복선의 미회수 상태를 확인할 방법이 없을 때만 `SETUP_PAYOFF_DEBT_UNTRACKED`다.

## 8. Slow vs Stagnant

느린 장면은 허용한다.

`SLOW_BUT_MOVING` 예:
- 관계가 가까워지거나 멀어진다.
- 새로운 의심이 생긴다.
- 결정 비용이 커진다.
- 인물이 이전 사건을 다르게 해석한다.
- 일상 루틴이 다음 위기의 기준점을 만든다.

`STAGNANT` 후보:
- 같은 정보와 감정을 새 변화 없이 반복한다.
- 이미 확정된 결론을 다른 표현으로 재설명한다.
- 전투·이동이 길지만 위치·위험·관계·자원이 그대로다.

## 9. Framework Lens

Story Grid, Save the Cat, Story Circle, Hero's Journey, 고정 대사 비율, 양자택일 위기, 문장 길이는 진단 Lens다. 장면 목적과 맞지 않는데도 형식을 채우면 `FRAMEWORK_OVERFIT`이다.
