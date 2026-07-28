# Human Validation Artifact Governance

## 1. 목적

이 Reference는 저충실도 카드, 종이 Prototype, 클릭 순서, 기존 PoC 위 연구 보조물, simulated recognition, scripted outcome처럼 **제품 시스템과 동일하지 않은 사람 검증 Artifact**를 안전하게 계획·판정하기 위한 공용 계약이다.

목표는 작은 표본으로 제품 재미나 성능을 증명하는 것이 아니라 다음을 찾는 것이다.

```text
결정 질문
→ 관찰 가능한 행동
→ 반복되는 오해·막힘·반례
→ 주장 가능한 범위
→ 다음 수정 또는 더 높은 fidelity 검증
```

사람 세션을 실행하지 않은 상태는 `NOT_RUN`으로 유지한다.

## 2. 적용 조건

다음 중 하나라도 해당하면 이 Reference를 사용한다.

- 참가자 12명 미만의 방향성 Pilot.
- 카드·종이·Markdown·Wizard-of-Oz 방식의 저충실도 검증.
- 진행자가 결과·후보·확률·전투 결과를 공개하는 scripted session.
- 실제 알고리즘 대신 미리 정한 후보를 보여주는 simulated component.
- 기존 PoC 위에 최종 UI가 아닌 연구용 카피·신호·시트를 겹쳐 쓰는 경우.
- 사람 행동과 사후 자기보고를 함께 수집하는 경우.

## 3. Artifact fidelity와 claim ceiling

모든 세션 패킷은 시작 전에 다음을 기록한다.

```yaml
artifact_fidelity: PAPER | CARD | CLICKABLE_MOCK | EXISTING_POC_OVERLAY | PRODUCT_BUILD
simulated_components: []
scripted_components: []
fixed_outcomes: []
claim_ceiling:
  can_claim: []
  cannot_claim: []
```

### PAPER / CARD

주장 가능:

- 용어·관계·정보 위계 이해 가능성.
- 반복되는 오해·누락·과부하.
- 선택 이유와 반례.
- 진행 순서와 설명 책임의 후보.

주장 불가:

- 실제 조작감·프레임·지연·터치 정확도.
- 실제 RNG 체감의 분포.
- 실제 알고리즘 정확도.
- 최종 UI 접근성 통과.

### CLICKABLE_MOCK

추가 주장 가능:

- 탐색 순서·발견 가능성·뒤로가기·오조작 후보.
- 화면 간 정보 지속성.

여전히 주장 불가:

- 실제 게임 규칙·성능·저장·네트워크·엔진 동작.

### EXISTING_POC_OVERLAY

추가 주장 가능:

- 현재 PoC 규칙 위에서 연구용 정보가 의사결정에 미치는 방향.
- 기존 실행 흐름과 연구 보조물의 충돌.

주의:

- overlay가 제품 UI가 아니다.
- 실제 코드·데이터와 카드 설명이 다르면 즉시 `STOP`한다.
- fixture 또는 재현 가능한 seed 없이 특정 전투 인과를 증명하지 않는다.

### PRODUCT_BUILD

실제 Build에서도 실행한 플랫폼·버전·기기·입력·콘텐츠 범위만 주장한다. 한 Build의 통과를 전체 제품·장기 경제·전체 접근성·전체 재미로 확장하지 않는다.

## 4. simulated·scripted component 계약

모든 simulated 결과 카드에는 다음 상태를 표시한다.

```yaml
component_status: SIMULATED_COMPONENT | SCRIPTED_OUTCOME | FIXED_STIMULUS
measures: UX_RESPONSIBILITY | COMPREHENSION | ATTRIBUTION | RECOVERY_DISCOVERY
not_measured: ALGORITHM_ACCURACY | TRUE_PROBABILITY | LATENCY | BALANCE | PRODUCT_PERFORMANCE
```

- simulated recognition은 후보 확인·수정 흐름을 검증할 수 있지만 실제 인식률을 측정하지 않는다.
- fixed RNG 결과는 인과 설명을 검증할 수 있지만 실제 RNG 체감 분포를 측정하지 않는다.
- scripted 실패 결과는 손실 이해·회상·후회 귀인을 검증할 수 있지만 실제 실패 발생률을 측정하지 않는다.
- 진행자가 제공한 결과를 참가자가 맞혔다고 해서 시스템 성능 성공으로 기록하지 않는다.

## 5. 작은 표본 판정

작은 표본은 방향성·결함 탐색용이다. `0.67`, `0.75`, `0.80` 같은 비율을 통계적 확증이나 자동 합격선으로 사용하지 않는다.

### 반드시 함께 기록할 것

- 분자와 분모의 실제 개수.
- 경험군별 행동 차이.
- 두 명 이상에게 반복된 동일 결함.
- 심각도 높은 단일 반례.
- 예상과 반대인 행동.
- 진행자 개입이 결과에 미친 영향.
- Artifact fidelity와 claim ceiling.

### 판정 언어

| 판정 | 의미 |
|---|---|
| `PROMISING_DIRECTION` | 작은 표본에서 방향을 지지하는 행동이 보였지만 실제 제품 검증 전 확정하지 않음 |
| `ADAPT` | 핵심 방향은 유지하되 반복 오해·과부하·복구 문제를 수정해야 함 |
| `REWORK` | 현재 정보·흐름·자극물이 핵심 질문을 검증하지 못하거나 큰 구조 수정이 필요함 |
| `REJECT` | 방향이 코어와 충돌하거나 참가자 행동이 기대와 지속적으로 반대임 |
| `STOP` | 정본 불일치, 진행자 누출, 자극물 결함, 안전·개인정보 문제로 결과를 해석할 수 없음 |

`ADOPT`는 다음을 모두 만족할 때만 후속 결정 문서에서 사용할 수 있다.

- 실제 제품 또는 목표 fidelity Build에서 재검증.
- 반복 세션 또는 독립 표본에서 같은 방향 확인.
- 행동·자기보고·로그가 모순되지 않거나 모순 원인이 설명됨.
- 프로젝트 책임 원본과 사용자 승인 게이트 통과.

## 6. 데이터 분리

한 행 또는 한 사건에서 다음을 분리한다.

```yaml
first_attempt:
post_feedback_attempt:
behavior_observation:
player_self_report:
facilitator_intervention:
system_or_artifact_log:
observer_interpretation:
```

- `first_attempt`는 힌트·교정·정답 피드백 전에 기록한다.
- `post_feedback_attempt`는 어떤 피드백을 받은 뒤 무엇을 수정했는지 기록한다.
- 행동 관찰은 실제 클릭·말·시간·되돌리기다.
- 자기보고는 감정·이유·기억·선호다.
- 진행자 개입은 안내·재질문·오류 교정·결과 공개다.
- 관찰자 해석은 원자료와 별도 열에 둔다.

## 7. 진행자 개입 통제

- 시작 문구와 질문 순서를 고정한다.
- 정답·추천·가치 판단을 제공하지 않는다.
- 이해하지 못한 용어를 설명한 경우 정확한 문구와 시점을 기록한다.
- 잘못된 입력을 교정할 때 최초 시도를 보존한다.
- 진행자 키와 참가자 자극물을 물리적·화면상으로 분리한다.
- 동일 세션 중 자극물 문구를 수정하지 않는다.

## 8. 결과 교차 배정

고정 결과가 통제감이나 성공감을 과장할 수 있으면 같은 구조에 최소 두 결과를 준비한다.

```text
같은 플레이어 구조
→ 유리한 결과
→ 불리하거나 혼합된 결과
```

참가자에게 교차 배정하고 다음을 본다.

- 좋은 결과에서만 자신의 설계 덕분이라고 말하는가.
- 나쁜 결과에서도 통제한 요소와 잔여 무작위성을 구분하는가.
- 결과가 달라도 다음 수정안이 구조·정보와 연결되는가.

## 9. 성공 기준 작성법

비율은 참고 신호로 기록할 수 있지만 판정은 다음 순서로 한다.

1. `STOP` 조건 확인.
2. 핵심 질문을 실제로 측정했는지 확인.
3. 심각도 높은 반례 확인.
4. 반복 결함과 경험군 차이 확인.
5. 행동·자기보고·진행자 개입 비교.
6. 수치 요약과 원자료 사례를 함께 검토.
7. claim ceiling 안에서만 판정.

좋은 형식:

```yaml
PROMISING_DIRECTION:
  required_patterns:
    - "서로 다른 참가자 2명 이상이 핵심 관계를 자기 말로 설명"
    - "심각도 높은 정답 누출·자동 오시전·비관측 규칙 없음"
  supporting_counts:
    - "분자/분모와 경험군별 수를 함께 기록"
  claim: "다음 fidelity Prototype로 진행할 방향을 지지"
```

나쁜 형식:

```yaml
ADOPT:
  success_rate: ">= 0.67"
```

## 10. 보고서 계약

사람 세션을 실제 실행한 뒤에만 보고서를 생성한다.

필수 항목:

- 실행한 repository·branch·commit·Build/Artifact 버전.
- artifact fidelity와 claim ceiling.
- simulated·scripted·fixed 요소.
- 참가자 수·세그먼트·모집 한계.
- first attempt와 post-feedback attempt 원자료.
- 행동·자기보고·진행자 개입·로그 분리.
- 반복 결함·반례·예상 밖 행동.
- 분자/분모가 있는 수치 요약.
- `PROMISING_DIRECTION / ADAPT / REWORK / REJECT / STOP` 판정.
- 미실행 검증과 다음 fidelity 게이트.
- 제품 코드·정본 변경 권한 상태.

## 11. 개인정보·원자료

- 이름·연락처·계정·음성 경로를 기본 원자료에 저장하지 않는다.
- 참가자 ID는 익명 코드로 사용한다.
- 음성·영상 기록이 필요하면 별도 동의·보존·삭제 계약을 둔다.
- 자유 응답의 개인정보는 보고서에 그대로 복사하지 않는다.

## 12. 실패 조건

다음이면 Governance 위반이다.

- 작은 표본 비율만으로 제품 방향을 `ADOPT`함.
- simulated 결과를 실제 알고리즘 정확도·지연·확률로 보고함.
- fixed 결과 하나로 RNG 통제감이나 밸런스를 증명함.
- 피드백 전 최초 시도를 보존하지 않음.
- 행동과 자기보고를 같은 필드로 합침.
- 진행자 힌트·교정을 기록하지 않음.
- 저충실도 Artifact 통과를 제품 UI·접근성·성능 통과로 확대함.
- 사람 세션을 실행하지 않고 `VALIDATED` 또는 `HUMAN_QA_PASS`를 선언함.
