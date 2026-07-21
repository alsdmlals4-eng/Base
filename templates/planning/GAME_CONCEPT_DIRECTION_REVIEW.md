# 게임 핵심 컨셉·방향성 분석

## 1. 현재 단계

- 상태: `CONCEPT_SEED / CONSTRAINTS_CHECKED / POINTED_FUN_HYPOTHESIS / CONCEPT_STRUCTURED / POC_BUILD_AND_TEST / CONCEPT_RECALIBRATION / PRODUCTION_READY / REPEAT_POC / HOLD / STOP`
- 분석 기준 커밋·기획서:
- 분석 목적:

## 2. 한 문장 핵심 컨셉

> [대상 플레이어]는 [핵심 행동과 선택]을 반복하며 [고유한 감정·판타지·성취]를 경험한다. 이 게임은 [비교 대상]과 달리 [차별화된 원리] 때문에 계속 플레이된다.

## 3. 대상 플레이어와 플레이 약속

- 대상 플레이어:
- 플레이 상황·세션 길이:
- 플레이어 역할·판타지:
- 처음 느껴야 하는 감정:
- 반복할수록 깊어지는 요소:
- 다음 플레이를 부르는 미완료 욕구:

## 4. 제약 조건

| 영역 | 확인된 제약 | 설계 영향 | 대응·활용 |
|---|---|---|---|
| 플레이 환경 | | | |
| 제작 인력·기술·일정 | | | |
| 콘텐츠 생산 | | | |
| 시스템·저장·성능 | | | |
| 아트·UI·사운드 | | | |
| 시장·운영 | | | |

## 5. 뾰족한 재미

| 후보 | 플레이어 행동 | 핵심 선택·긴장 | 숙련·변주 | 반복 원동력 | DDD가 드러내는 방식 | 판정 |
|---|---|---|---|---|---|---|
| | | | | | | `핵심/보조/장식/충돌/미검증` |

최종 가설:

> [플레이어가 계속 플레이하게 만드는 행동·선택·피드백·다음 동기]

## 6. 게임 요소 정렬 / BIG BLIND

| 요소 | 현재 역할 | 핵심 컨셉 기여 | 판정 | 개선 방향 |
|---|---|---|---|---|
| GDD 핵심 규칙 | | | `AMPLIFY/SUPPORT/NEUTRAL/CONFLICT/UNPROVEN` | |
| 레벨 디자인 | | | | |
| 등장인물 | | | | |
| 캐릭터 스타일 | | | | |
| 스테이지 | | | | |
| 세계관 | | | | |
| UI·아트·사운드 | | | | |
| 성장·수집·경제 | | | | |
| 첫 보상·행동 피드백·보상 사다리 | | | | |

## 7. SWOT와 실행 전략

### SWOT

| 내부·외부 | 긍정 | 부정 |
|---|---|---|
| 내부 | Strengths | Weaknesses |
| 외부 | Opportunities | Threats |

### 전략 변환

| 전략 | 활용 요소 | 실행 방향 | 우선순위 |
|---|---|---|---|
| SO | | | |
| WO | | | |
| ST | | | |
| WT | | | |

## 8. 분석 프레임워크

- framework_profile:
- 외부 자료에서 사용하는 추가 약어 정의:

### MDA 또는 DDE

| 층 | 현재 설계 | 의도한 결과 | 불일치·개선 |
|---|---|---|---|
| Mechanics / Design | | | |
| Dynamics | | | |
| Aesthetics / Experience | | | |

### DDD — Digital Dopamine Design

> 프로젝트 정의: 플레이 시작 또는 행동 직후 짧은 시간 안에 사용자가 의미 있는 보상, 변화, 성취와 다음 기대를 체감하도록 설계하는 빠른 보상 요소.

| 분석축 | 현재 값·구조 | 목표 | 문제·개선 |
|---|---|---|---|
| 첫 의미 있는 보상까지의 시간 | | | |
| 행동 → 피드백 지연 | | | |
| 보상 원인·결과의 명료성 | | | |
| 짧은 구간의 의미 있는 보상 밀도 | | | |
| 기대 → 행동 → 공개·획득 리듬 | | | |
| Micro → Session → Meta 보상 사다리 | | | |
| 다음 행동·선택 유도 | | | |
| 반복 피로·무감각·보상 인플레이션 | | | |

DDD 핵심 판정:

- DDD가 뾰족한 재미를 더 빨리 이해시키는가:
- 단순 이펙트·팝업·숫자로 핵심 재미를 가리는가:
- 줄여야 할 무의미한 자극:
- 앞당겨야 할 첫 의미 있는 보상:
- 다음 선택과 연결할 작은 보상:

DDD 위험 점검:

- [ ] 보상 가치·확률·비용을 과장하거나 숨기지 않는다.
- [ ] 불필요한 불편을 만든 뒤 결제로 해소하지 않는다.
- [ ] 손실 압박과 놓치면 손해라는 감정만으로 복귀를 유도하지 않는다.
- [ ] 플레이어가 멈추거나 쉬기 어렵게 연속 알림·보상을 배치하지 않는다.
- [ ] 실제 도파민 분비나 의학적 중독을 관찰 없이 단정하지 않는다.

### 3C·루프·동기

- Character:
- Camera:
- Control:
- Core loop:
- Session loop:
- Meta loop:
- 핵심 동기:
- 피드백·실패 학습:

## 9. 차별화·제작성·확장성

- 보이는 차이:
- 실제 플레이 원리의 차이:
- 콘텐츠 한 단위 제작 비용:
- 반복 생산 가능성:
- 재사용·자동화 가능성:
- 확장 시 핵심 재미 강화 여부:

## 10. PoC 계약

```yaml
hypothesis:
player_action:
expected_experience:
minimum_rules_and_content:
excluded_scope:
observation_method:
success_signal:
failure_signal:
stop_condition:
next_decision_if_passed:
next_decision_if_failed:
ddd_observation:
  time_to_first_meaningful_reward:
  action_to_feedback_latency:
  reward_cause_understanding:
  next_action_intent:
  fatigue_or_overstimulation:
```

## 11. PoC 결과와 기획 재조정

| 요소·가설 | 증거 | 판정 | 변경 | 영향 문서·시스템 |
|---|---|---|---|---|
| | | `KEEP/AMPLIFY/CHANGE/REMOVE/DEFER/RETEST` | | |

## 12. 개선 우선순위

1.
2.
3.

## 13. 다음 게이트

- 판정: `PRODUCTION_READY / REPEAT_POC / HOLD / STOP`
- 다음 제작 범위:
- 제외 범위:
- Vertical Slice 선행 조건:
- DDD 선행 검증:
- 미검증·위험:
- 다음 질문:
