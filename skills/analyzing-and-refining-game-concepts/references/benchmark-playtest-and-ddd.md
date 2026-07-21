# 벤치마크·플레이테스트·DDD 상세 계약

이 문서는 `analyzing-and-refining-game-concepts`의 조건부 상세 계약이다. 벤치마크·사용자 반응·플레이테스트의 전체 기록 Schema와 공식 근거는 `references/benchmark-player-evidence-and-playtests.md`가 책임진다.

## 벤치마크와 사용자 근거

공식 제품 사실, 플레이어 자기보고, 행동 이벤트·퍼널, 통제 실험, 해석을 분리한다. 플랫폼·언어·버전·플레이타임·표본 편향을 기록하고 기능 복사가 아니라 작동 원리와 실패 조건을 추출한다.

## 플레이테스트·실험

빌드·버전, 대상 집단과 기존 노출, 과제·시간, 관찰 행동, 인터뷰·설문, `feedback_channel`, `telemetry_events`, `funnel_steps`, `control_and_variants`, 1차 지표와 가드레일, 성공·중단 기준을 사전 선언한다.

## Digital Dopamine Design

Base에서 DDD는 **Digital Dopamine Design**이다. 실제 도파민 분비량이나 의학적 중독을 진단하는 표현이 아니라, 의미 있는 행동의 결과를 빠르고 이해 가능하게 전달하는 체감 보상 설계축이다.

- First meaningful reward: 첫 의미 있는 보상까지의 시간.
- Action-feedback latency: 입력·행동에서 피드백까지의 지연.
- Reward legibility: 무엇을 왜 얻었는지 즉시 이해되는가.
- Reward density: 짧은 구간의 보상 빈도와 밀도.
- Reward ladder: Micro → Session → Meta 보상 사다리와 다음 목표 연결.
- Fatigue and inflation: 같은 자극의 반복 피로와 보상 인플레이션.

DDD는 **뾰족한 재미를 빠르게 전달**해야 한다. 의미 있는 선택 없이 빠른 보상만 반복하거나, 이펙트·팝업·숫자의 양으로 핵심 재미를 대체하지 않는다. 외부 자료에서 정의되지 않은 DDD를 임의의 분석 틀로 확정하지 않는다.

## Failure boundaries

- 제품 사실, 플레이어 반응, 행동 근거와 해석을 같은 권한으로 취급한다.
- 결과를 본 뒤 성공 기준을 바꾸거나 여러 변수를 동시에 바꾼 실험을 인과 근거로 사용한다.
- 실제 도파민 분비량·중독 여부를 관찰 없이 단정한다.
- DDD 보상이 뾰족한 재미를 가리는데도 빠르다는 이유만으로 통과시킨다.
