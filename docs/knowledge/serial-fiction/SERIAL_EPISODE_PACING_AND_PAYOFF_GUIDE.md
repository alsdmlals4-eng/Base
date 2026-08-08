# 연재소설 회차 Pacing·Payoff Guide

## 1. 핵심 원칙

연재 회차의 품질은 글자 수 하나로 판정하지 않는다.

우선순위:

```text
Episode Value
→ scene / episode completeness
→ rhythm
→ current platform contract
→ project production target character count
```

Base에는 5,000자·5,500자·6,000자 같은 universal 완성 규칙을 두지 않는다. 플랫폼·작품·과금·연재 형식은 변할 수 있으므로 적용 시 현재 공식 기준을 다시 확인한다. 확인하지 못하면 `PLATFORM_REVERIFY_REQUIRED`다.

## 2. Episode Value

회차를 읽기 전과 읽은 뒤를 비교해 최소 하나 이상의 상태가 달라져야 한다.

```yaml
changed_state:
  goal:
  information:
  relationship:
  danger:
  location_or_access:
  ability_or_resource:
  emotion_or_belief:
  reputation_or_faction:
```

변화가 없고 설명·전투·이동만 길어졌다면 `EPISODE_VALUE_MISSING`이다.

## 3. Local Payoff

매 회차가 최종 결말을 줄 필요는 없다. 그러나 독자가 이번 회차에서 받은 보상은 있어야 한다.

가능한 payoff:

- 작은 질문의 답
- 규칙의 이해
- 선택 결과
- 감정적 결산
- 관계 변화
- 임시 성공·명확한 실패
- 새로운 능력·자원의 실제 사용 가치
- 이전 복선의 부분 회수

아무것도 닫히지 않고 다음 회차만 요구하면 `LOCAL_PAYOFF_MISSING`이다.

## 4. Open Loop

다음 화 동력은 다양하게 만든다.

- `QUESTION`: 새 질문
- `COST`: 얻은 것의 대가
- `RELATIONSHIP`: 관계의 불확실성
- `CHANGED_GOAL`: 목표 변경
- `RULE_EXCEPTION`: 알던 규칙의 예외
- `IMMEDIATE_DANGER`: 즉시 위험
- `PROMISED_PAYOFF`: 이미 설치된 보상 직전

`IMMEDIATE_DANGER`만 반복하면 절단 패턴이 보일 수 있다. 작은 사건을 닫고 더 큰 질문을 남기는 방식과 섞는다.

## 5. 회차 경계 재설계

압축 초안의 번호는 최종 연재 번호가 아닐 수 있다.

회차를 합칠 후보:

- 각 회차가 독립 payoff 없이 하나의 사건을 잘게 나눈 경우
- 동일 목표·장소·갈등이 짧게 연속되는 경우
- 감정 변화가 다음 번호에서야 완성되는 경우

회차를 분리할 후보:

- 한 회차에 서로 다른 중심 갈등이 과밀하게 들어간 경우
- 큰 선택 뒤 후폭풍을 별도 체험해야 하는 경우
- POV 전환이 새 질문과 새 목표를 명확히 만드는 경우

번호 보존 자체보다 `Episode Value + Local Payoff + Open Loop`를 우선한다. 다만 프로젝트 정본에서 회차 번호가 의미를 가진다면 먼저 보호 범위를 확인한다.

## 6. Pattern Variation

반복 골격은 장기 연재의 안정감을 준다. 문제는 반복 자체가 아니라 **변화 없는 반복**이다.

```yaml
skeleton: mission | school | work | dungeon | rumor | loop | investigation | battle | other
variation:
  rule_or_exception:
  cost:
  reward:
  solving_character:
  emotion:
  relationship:
  information_release:
  failure_shape:
```

최소 하나가 의미 있게 달라져야 한다. 장식만 바뀌고 해결 순서·감정·보상이 같으면 `PATTERN_REPETITION_UNVARIED`다.

## 7. Consequence Memory

회차 결과는 다음 회차로 넘어간다.

```text
승리 → 새 책임 / 더 큰 적의 관심 / 자원 변화
실패 → 정보 / 상흔 / 관계 손상 / 금기 이해
폭력 → 죄책감 / 신뢰 변화 / 평판 / 작전 조건
능력 → 육체·정신·관계·자원 비용
```

중대한 사건 뒤 바로 초기화되면 연재의 누적감이 약해진다.

## 8. Setup–Payoff Debt

장기 복선과 질문만 추적한다.

상태:

- `SETUP`: 질문·단서 설치
- `RECALL`: 다시 떠올리게 함
- `PARTIAL_PAYOFF`: 일부 의미 공개
- `PAYOFF`: 핵심 질문 회수
- `RETIRED`: 의도적으로 종료·폐기하고 이유 기록
- `DEFERRED`: 장기 아크로 연기하며 다음 점검 시점 기록

권장 기록:

```yaml
setup_id:
question_or_promise:
state:
introduced_at:
last_touched_at:
reader_can_reason_about_it: true | false
next_expected_touch:
retirement_reason:
```

모든 소품·농담·짧은 정보에 ID를 붙이지 않는다. 장기 기대를 만든 항목만 추적한다. 추적 체계가 전혀 없어 미회수 부채가 보이지 않을 때 `SETUP_PAYOFF_DEBT_UNTRACKED`다.

## 9. Pacing은 문장 속도만이 아니다

빠른 문장 = 빠른 전개가 아니다.

전개의 체감 속도는 다음에 좌우된다.

- 목표가 얼마나 빨리 명확해지는가
- 시도와 결과 사이의 거리
- 새 정보가 실제 판단을 바꾸는가
- 같은 결론을 반복하는가
- 장면 전환마다 새 목표가 있는가
- 보상을 얼마나 오래 미루는가

느린 관계 장면도 상태가 바뀌면 전진한다. 반대로 빠른 전투가 반복돼도 결과가 누적되지 않으면 정체다.

## 10. 플랫폼·생산 분량 기록

프로젝트가 실제 연재를 준비할 때만 다음을 기록한다.

```yaml
platform:
observed_at:
count_basis: spaces_included | spaces_excluded | platform_defined
official_minimum_or_contract:
observed_comparable_range:
production_target_range:
scene_completion_override:
exception_reason:
status: VERIFIED_CURRENT | PLATFORM_REVERIFY_REQUIRED
```

`production target`은 작업 계획과 가격·연재 리듬을 돕는 범위다. 장면이 이미 완결됐는데 숫자를 채우기 위해 중복 설명을 추가하거나, 필요한 후폭풍을 숫자 때문에 잘라내지 않는다.

## 11. Framework overfit 방지

회차마다 동일한 촉발 사건·중간 반전·최악의 순간·양자택일을 의무화하지 않는다. 큰 사건 회차에는 유용할 수 있지만 휴식·관계·공포 분위기·후폭풍 회차에는 다른 구조가 더 적합하다.

프레임워크를 채우기 위해 원고를 비틀면 `FRAMEWORK_OVERFIT`이다.
