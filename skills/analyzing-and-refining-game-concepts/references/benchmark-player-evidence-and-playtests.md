# 벤치마크·플레이어 반응·플레이테스트 근거 모델

이 문서는 `analyzing-and-refining-game-concepts`의 `benchmark-and-player-research`, `playtest-and-experiment` mode가 사용하는 상세 근거 모델이다. 외부 사례를 복사하는 절차가 아니라 **현재 기획 가설을 반증하고 개선 결정을 만드는 절차**다.

## 1. 조사 질문을 먼저 고정한다

```yaml
decision_to_make:
current_hypothesis:
what_would_change_the_decision:
target_player_segment:
platform_region_language:
release_or_patch_window:
comparable_dimension:
excluded_questions:
```

“비슷한 게임을 조사한다”로 시작하지 않는다. 다음처럼 현재 결정을 바꿀 수 있는 질문으로 좁힌다.

- 같은 핵심 행동이 다른 게임에서 어떤 기대와 불만을 만드는가?
- 첫 의미 있는 보상·튜토리얼·세션 길이에서 이탈이 발생하는가?
- 플레이어가 상점 설명·영상으로 기대한 경험과 실제 플레이가 일치하는가?
- 경쟁작의 강점이 우리 핵심 컨셉에 필요한가, 장르 관습일 뿐인가?
- 특정 개선안이 행동 데이터와 자기보고 반응에서 모두 지지되는가?

## 2. 근거 층위

| 층위 | 예시 | 사용 방식 |
|---|---|---|
| 제품 사실 | 공식 상점 페이지, 패치 노트, 개발 문서, 실제 플레이·영상 | 기능·규칙·버전·플랫폼 상태 확인 |
| 플레이어 반응 | Steam 리뷰, 커뮤니티, 포럼, 설문, 플레이테스트 기록 | 기대 충족·불만·반복 패턴 탐색 |
| 행동 근거 | 이벤트, 퍼널, 세션 기록, 성공·실패·이탈 | 실제 행동과 자기보고를 분리해 검증 |
| 통제 실험 | A/B 테스트, 동일 과제의 변형 빌드 | 한 가설의 인과 비교 |
| 해석·제안 | 기사, 영상 해설, 모델 추론 | 후보 가설로만 사용하고 상위 근거로 검증 |

한 출처가 다른 층위의 권한을 대신하지 않는다. 리뷰는 구현 사실의 정본이 아니고, 이벤트 수치는 플레이어가 왜 그렇게 행동했는지 단독으로 설명하지 못한다.

## 3. 비교 대상 선정

비교 게임은 장르 이름보다 **비교 차원**으로 고른다.

- 같은 핵심 행동·판단
- 같은 세션 길이·입력 환경
- 같은 성장·보상 구조
- 같은 가격·운영 방식
- 같은 대상 플레이어·난이도 약속
- 같은 제작 제약이나 플랫폼
- 성공 사례뿐 아니라 실패·혼합 반응 사례

최소 구성:

```text
직접 경쟁작 2~3
+ 핵심 행동이 유사한 인접 장르 1~2
+ 실패·혼합 반응 사례 1
+ 게임 밖 상호작용 참고 1 (필요한 경우)
```

## 4. 플레이어 반응 표본

- 긍정·부정·혼합 반응을 모두 본다.
- 최신 반응과 누적 반응을 구분한다.
- 초보·장기 플레이어, 짧은·긴 플레이타임, 플랫폼·언어·지역을 구분한다.
- 특정 패치 전후를 섞지 않는다.
- 반복되는 구체 상황과 영향도를 우선하고, 강한 표현의 수를 중요도로 착각하지 않는다.
- 리뷰 폭탄·오프토픽·밈·복사 리뷰는 별도 표시한다.
- 플레이어가 요구한 해결책보다 **겪은 문제·기대·맥락**을 먼저 추출한다.

Steamworks는 리뷰를 기대가 올바르게 설정되고 충족되는지 이해하는 피드백 채널로 설명하지만, 리뷰 하나가 제품 개선 전체를 지배하게 하지 말라고 안내한다.

## 5. 반응 코딩

각 근거를 다음 구조로 기록한다.

```yaml
source:
date_and_version:
player_context:
observed_fact:
reported_experience:
trigger_or_situation:
impact:
frequency_signal:
confidence:
possible_explanations:
```

반응 클러스터 예:

- 기대 불일치
- 이해·가독성·온보딩
- 조작·피드백 지연
- 난이도·공정성
- 반복·콘텐츠 피로
- 보상·경제·진행
- 성능·안정성
- 접근성·입력 장벽
- 가격·운영·신뢰
- 핵심 재미 강화·차별화

## 6. 개선 변환

근거마다 다음 중 하나로 판정한다.

- `ADOPT`: 핵심 컨셉과 제약에 맞고 직접 채택한다.
- `ADAPT`: 원리는 유효하지만 우리 핵심 행동에 맞게 변형한다.
- `AVOID`: 반복 실패·기대 불일치·제작 위험이 크다.
- `TEST`: 근거가 상충하거나 프로젝트 적용성이 미확정이다.
- `IGNORE`: 비교 차원·대상 플레이어·버전이 달라 현재 결정과 무관하다.

```yaml
finding:
evidence:
core_concept_alignment:
player_value:
production_cost:
risk:
decision: ADOPT/ADAPT/AVOID/TEST/IGNORE
change_candidate:
validation_needed:
```

유행·평점·판매량만으로 핵심 컨셉을 변경하지 않는다. 사례의 기능을 복사하지 말고 문제를 해결한 원리와 실패 조건을 추출한다.

## 7. 플레이테스트·실험 계약

Steam Playtest는 메인 게임과 분리된 저위험 테스트 앱으로 외부 플레이 데이터를 모을 수 있고, 개발자가 원하는 피드백 채널을 게임 안에 명확히 안내하도록 권장한다. 기존 지식이 결과를 오염시키면 새 테스터 집단으로 다시 확인한다.

```yaml
hypothesis:
build_and_version:
tester_segment:
cohort_size_and_recruitment:
prior_exposure:
tasks_or_play_window:
observation_points:
feedback_questions:
feedback_channel:
telemetry_events:
funnel_steps:
control_and_variants:
primary_metric:
guardrail_metrics:
success_failure_stop:
```

- 관찰된 행동, 이벤트·퍼널, 인터뷰·설문 자기보고를 분리한다.
- 질문은 해결책을 유도하지 않고 경험·혼란·기대·결정 이유를 묻는다.
- A/B 테스트는 한 번에 하나의 주요 가설을 비교하고, 통제군·변형·주 지표·가드레일을 미리 선언한다.
- 이벤트는 플레이어 행동과 당시 맥락을 함께 기록하고, 퍼널은 순서가 있는 단계와 이탈·소요 시간을 확인한다.
- 결과를 본 뒤 성공 기준을 바꾸지 않는다.

## 8. 실패 조건

- 인기 게임 기능 목록을 그대로 모방한다.
- 리뷰 수나 평점만으로 원인을 단정한다.
- 긍정 또는 부정 반응만 골라 현재 기획을 정당화한다.
- 버전·패치·플레이타임·플랫폼 차이를 무시한다.
- 플레이어가 제안한 해결책을 문제 분석 없이 그대로 구현한다.
- 자기보고만으로 실제 행동을 단정하거나, 행동 수치만으로 감정·이유를 단정한다.
- 여러 변수를 동시에 바꾼 실험을 인과 근거로 사용한다.
- 출처·날짜·표본·불확실성을 기록하지 않는다.

## 공식 참고 자료

- Steamworks — User Reviews: https://partner.steamgames.com/doc/store/reviews
- Steamworks — Steam Playtest: https://partner.steamgames.com/doc/features/playtest
- Steamworks — Testing On Steam: https://partner.steamgames.com/doc/store/testing
- Unity Analytics — Events: https://docs.unity.com/en-us/analytics/events/events
- Unity Analytics — Funnels: https://docs.unity.com/en-us/analytics/funnels/funnels
- Unity Game Overrides — A/B testing: https://docs.unity.com/en-us/game-overrides/ab-testing
