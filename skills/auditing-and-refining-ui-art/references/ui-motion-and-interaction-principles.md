# 게임 UI 모션·상호작용 원칙

## 1. 목적과 비목표

UI 모션은 화면을 화려하게 만드는 장식이 아니라 플레이어에게 다음을 설명하는 정보 채널이다.

- 무엇이 바뀌었는가
- 입력이 접수됐는가
- 지금 처리 중인가
- 결과가 어디에 반영됐는가
- 화면·요소 사이의 공간 관계는 무엇인가
- 다음에 무엇을 할 수 있는가

모션은 정보 구조·상태 소유권·도메인 규칙을 대신하지 않는다. 기능·화면 중심 질문·주 입력 경로가 미확정이면 모션으로 가리지 않고 설계 단계로 돌아간다.

## 2. 시작 입력

```yaml
screen_question:
state_change:
state_source:
primary_input:
input_accepted_feedback:
processing_state:
result_state:
first_attention:
feedback_budget:
repeat_frequency:
interruptible:
minimum_and_target_resolution:
accessibility_settings:
performance_budget:
validation_environment:
```

## 3. 모션 목적

각 모션은 하나 이상의 목적을 선언한다.

```text
ORIENT: 화면·패널·요소가 어디에서 왔고 어디로 가는지 설명
CONFIRM: 입력 접수와 선택 상태 확인
PROGRESS: 처리 중·대기·단계 진행 표시
RESULT: 실제 결과와 반영 위치 전달
WARN: 위험·오류·복구 행동 강조
REWARD: 가치 있는 변화와 획득 위치 전달
DECORATE: 정보 기능이 없는 선택적 분위기 표현
```

`DECORATE`는 P0~P2 문제가 해결된 뒤 피드백 예산 안에서만 사용한다.

## 4. Staging과 첫 시선

`staging`은 한 순간에 무엇을 먼저 보게 할지 정한다.

- 화면 중심 질문과 주 행동을 가장 먼저 인식하게 한다.
- 여러 요소가 동시에 최고 강도로 움직이지 않는다.
- 장식 모션이 비용·위험·비활성 이유·오류보다 먼저 시선을 빼앗지 않는다.
- 상태 변화의 원인과 결과를 같은 시간축에서 이해할 수 있게 한다.
- 모션이 끝난 뒤에도 정적 계층만으로 중요도가 남는다.

## 5. Anticipation 판정

`anticipation`은 결과 직전에 짧은 준비 신호를 주는 방식이다. 모든 클릭에 적용하지 않는다.

적합 후보:

- 되돌리기 어렵거나 비용이 큰 행동
- 강한 보상·승급·마일스톤
- 화면 구조가 크게 바뀌는 전환
- 충돌·공격·위험이 곧 발생함을 공정하게 알려야 하는 경우

부적합 후보:

- 반복되는 탭·hover·목록 이동
- 즉시 반응이 중요한 조작
- 입력 지연처럼 느껴지는 준비 동작
- 이미 확인창·텍스트·상태로 충분히 예고된 행동

Anticipation은 결과를 먼저 확정한 것처럼 보이게 해서는 안 된다.

## 6. Timing·Easing

`timing`과 `easing`은 프로젝트·플랫폼·반복 빈도에 따라 정한다. Base에서 고정 millisecond 상수를 강제하지 않는다.

판정 기준:

- 입력 접수 피드백은 즉시 인지 가능해야 한다.
- 처리 중과 실제 결과는 서로 다른 상태다.
- 자주 반복되는 행동일수록 이동 거리·지속 시간·강도를 줄인다.
- 중요한 전환도 플레이어의 다음 행동을 불필요하게 막지 않는다.
- 모션을 건너뛰거나 즉시 완료해도 결과 위치와 원인이 남는다.
- easing은 이동의 출발·도착·무게를 설명하며 단순 취향으로 제각각 사용하지 않는다.

프로젝트는 실제 반복 빈도와 목표 기기에서 값을 검증한다.

## 7. 공간적 연속성과 Follow-through

### 공간적 연속성

- 팝업·상세창·카드 확대가 어떤 원본 요소에서 열렸는지 연결한다.
- 닫을 때 의미 있는 원래 위치와 포커스로 돌아간다.
- 정렬·필터·인벤토리 이동에서 항목이 사라진 이유와 새 위치를 이해할 수 있게 한다.
- 화면 밖으로 이동한 요소의 결과가 로그·수치·목록에 남는다.

### `follow-through`

주 결과 뒤 남는 작은 후행 변화는 결과 위치를 확인시키는 데만 사용한다.

- 획득 수치가 실제 보유량 위치에 반영됨
- 카드가 장착 슬롯으로 이동한 뒤 슬롯 상태가 남음
- 선택 완료 뒤 관련 정보가 안정된 최종 상태로 정착함

후행 연출이 다음 입력을 막거나 결과를 두 번 실행하지 않는다.

## 8. 입력 접수·처리 중·결과 분리

```text
입력 접수
→ 처리 중
→ 성공 또는 실패 결과
→ 다음 행동 가능 상태
```

각 단계는 시각적으로 구분한다.

- `입력 접수`: 눌림·선택·짧은 소리·텍스트 등 즉시 신호
- `처리 중`: loading·pending·잠금 이유·취소 가능 여부
- `결과`: 실제 상태 원본에서 온 성공·실패·수치·위치

애니메이션이 재생됐다는 이유로 구매·보상·저장·진행을 성공 처리하지 않는다.

## 9. Godot 상태 권위

- `AnimationPlayer`와 `Tween`은 표현을 담당한다.
- 도메인 상태는 게임 로직·데이터·서비스·승인된 상태 소유자가 결정한다.
- 애니메이션 완료 signal을 구매·저장·보상·진행 결과의 유일한 권위 시점으로 사용하지 않는다.
- 모션이 중단되거나 즉시 완료돼도 도메인 결과는 한 번만 발생한다.
- UI는 표시 데이터를 받고 사용자 의도를 `Signal` 또는 명시적 이벤트로 반환한다.

## 10. 중단·즉시 완료·반복·재진입

필수 Fixture:

```yaml
interruption:
instant_complete:
rapid_repeat:
duplicate_input:
modal_reentry:
input_device_switch:
close_and_reopen:
long_session_repetition:
```

### 중단

- 다른 화면 전환·뒤로가기·상태 갱신이 모션을 중단해도 잘못된 중간 상태가 남지 않는다.
- 취소 가능한 처리와 취소 불가능한 처리의 피드백을 구분한다.
- 중단 뒤 scale·alpha·position이 누적되지 않는다.

### 즉시 완료

- Reduced Motion 또는 skip에서 최종 상태로 안전하게 이동한다.
- 결과 위치·원인·다음 행동이 사라지지 않는다.
- 입력 가능 시점과 실제 상태가 일치한다.

### 빠른 반복

- 연타로 구매·보상·저장·Scene 전환이 중복되지 않는다.
- 같은 모션을 재시작해 transform drift가 누적되지 않는다.
- 반복되는 routine 피드백은 피로와 조작 지연을 만들지 않는다.

### 재진입

- 팝업을 닫고 다시 열면 현재 정본 상태를 렌더한다.
- 이전 모션의 임시 상태를 두 번째 정본처럼 유지하지 않는다.
- 포커스가 유효한 의미 위치로 복귀한다.

## 11. Reduced Motion·mute·haptic-off

### `Reduced Motion`

동등 경로:

- 큰 이동 → 짧은 fade 또는 즉시 최종 상태
- 반복 흔들림 → 정적 warning·문구·아이콘
- 화면 확대 → 명확한 선택·focus 변화
- 보상 이동 → 획득 위치·수치의 즉시 강조

모션 감소가 게임 결과·입력 가능성·정보량을 바꾸지 않는다.

### `mute`

음향을 꺼도 입력 접수·오류·경고·보상·완료를 텍스트·형태·아이콘·로그로 이해할 수 있어야 한다.

### `haptic-off`

햅틱을 꺼도 동일한 원인·결과가 시각·텍스트·음향의 허용된 채널로 남는다. 햅틱을 유일한 정보 채널로 사용하지 않는다.

## 12. 성능·해상도·현지화

- 목표 플랫폼에서 UI 전환 frame time·allocation·draw call·memory spike 후보를 본다.
- blur·shader·대형 Texture·동적 그림자·다량 particle은 실제 기기에서 측정한다.
- 긴 한국어·최대 수치·다른 화면 비율에서 이동 시작점과 최종 상태가 잘리지 않는지 확인한다.
- 최소 해상도와 safe area에서 모션 밖에 중요한 정보를 두지 않는다.
- 성능 환경이 없으면 `NOT_RUN` 또는 `UNVERIFIED`다.

## 13. 전후 증거

```yaml
build_or_commit:
screen_and_state:
resolution:
input_device:
locale:
accessibility_settings:
motion_purpose:
before_artifact:
after_artifact:
interruption_result:
repeat_result:
performance_result:
human_evidence: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
```

정지 이미지 한 장은 motion timing·입력 완결성·반복 피로·성능을 증명하지 못한다.

## 14. 실패 조건

- 모든 요소에 확대·흔들림·점멸을 추가함
- P0~P2보다 장식 모션을 먼저 적용함
- 입력 접수와 실제 결과를 같은 상태로 표현함
- AnimationPlayer·Tween 완료를 도메인 성공의 권위로 사용함
- 중단·즉시 완료·빠른 반복에서 결과가 중복됨
- Reduced Motion에서 핵심 정보가 사라짐
- mute·haptic-off에서 의미를 잃음
- 모션이 결과보다 오래 다음 입력을 막음
- 프로젝트 반복 빈도·플랫폼 없이 timing 상수를 공용 규칙으로 고정함
- 웹/SaaS 패턴이나 애니메이션 원칙을 게임 코어·입력·플랫폼 검토 없이 복제함
