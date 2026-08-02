# 튜토리얼·온보딩 설계 Guide

```yaml
guide_role: tutorial-and-onboarding-design-method
execution_owner: analyzing-and-refining-game-concepts
default_mode: tutorial-and-onboarding-design
research_coverage_owner: governing-game-user-research-coverage
checked_at: 2026-08-02
```

## 1. 목적

튜토리얼을 조작 설명·팝업·강제 클릭의 집합으로 만들지 않는다. 플레이어가 프로젝트의 실제 핵심 규칙을 수행하고, 해결해야 할 필요·결핍을 이해하며, 방법을 발견하고, 성장 전후 차이를 체감한 뒤, 안내 없이 같은 원리를 다시 사용하고 다른 상황으로 전이할 수 있게 설계한다.

```text
프로젝트 정본·실제 구현·진행 상태 감사
→ RULE: 기본 규칙 수행
→ NEED: 필요·결핍 인식
→ DISCOVER: 해결 방법 발견
→ FEEL: 성장 전후 차이 체감
→ PROVE: 안내 없는 독립 수행
→ TRANSFER: 다른 상황에서 재사용
→ 플레이테스트·텔레메트리
→ 적대적 검토
→ KEEP / CHANGE / REMOVE / TEST / HOLD
```

이 Guide는 공용 원리와 검증 계약만 책임진다. 프로젝트 고유 세계관·규칙·수치·성장 내용·Scene·Resource·UI·실제 구현 상태는 대상 프로젝트의 정본과 실제 코드·데이터·자산·테스트가 소유한다.

## 2. 사용 시점과 비사용 시점

### 사용한다

- 첫 세션, 신규 플레이어 온보딩, 튜토리얼, 도움말, 복귀 플레이어 재학습을 설계할 때
- 핵심 규칙·성장 시스템·경제·전투·제작·탐색을 어떤 순서로 가르칠지 결정할 때
- 튜토리얼 이탈, 이해 실패, 힌트 의존, 성장 체감 부족을 분석할 때
- 벤치마킹과 실제 플레이테스트를 튜토리얼 개선 결정으로 바꿀 때

### 사용하지 않는다

- 확정된 단일 문구의 오탈자만 고칠 때
- 프로젝트 정본과 실제 구현을 읽지 않고 장르 관습만으로 튜토리얼을 작성할 때
- 엔진 코드 구현만 필요한데 학습 목표와 설계가 이미 승인됐을 때
- 게임 사용자 연구 11영역의 설치·누락 감사만 필요한 경우. 이때는 `governing-game-user-research-coverage`가 주 책임이다.

## 3. 프로젝트 선감사 Gate

튜토리얼 문구나 화면을 먼저 만들지 않는다. 다음 순서로 현재 상태를 복원한다.

```text
Base START_HERE·AGENTS·운영 모델
→ 대상 프로젝트 AGENTS·START_HERE·Active Context
→ CURRENT_CONFIRMED_DECISIONS·분야 정본
→ 프로젝트 Google Sheets가 구성된 경우 현재 계획·진행도·PROPOSED_SHEET_CHANGE
→ 실제 코드·데이터·Scene·Resource·UI·입력·테스트
→ 동일 Goal의 열린 PR·최근 병합 PR
→ 기존 튜토리얼·도움말·첫 세션 데이터
→ 보류·대체·폐기된 과거 설계
```

최소 확인 항목:

```yaml
target_player_and_play_context:
first_session_promise:
core_action_and_choice:
prerequisite_knowledge:
current_rules_and_systems:
current_growth_or_capability_change:
actual_implementation_paths:
existing_tutorial_and_help_surfaces:
current_progress_and_next_work:
known_failures_and_drop_offs:
benchmark_question:
```

프로젝트 정본·실제 코드·진행 상태를 확인할 수 없으면 `BLOCKED_UNVERIFIED`로 기록한다. 외부 사례나 AI 추론으로 프로젝트 고유 사실을 채우지 않는다.

## 4. 학습 목표를 행동으로 정의하기

나쁜 목표:

> 장비 강화 시스템을 이해한다.

좋은 목표:

> 플레이어가 현재 장벽의 원인을 확인하고, 적합한 강화 대상을 선택해 적용한 뒤, 같은 유형의 장벽을 더 적은 위험과 비용으로 돌파한다.

각 학습 목표는 다음 계약을 가진다.

```yaml
learning_goal:
player_action:
required_information:
system_response:
success_evidence:
failure_evidence:
recovery_path:
independent_performance:
transfer_situation:
```

정적 조작표를 읽거나 팝업을 닫은 것은 학습 성공이 아니다. 핵심 메커니즘을 실제 플레이 환경 또는 본편과 동등한 시뮬레이션 환경에서 수행해야 한다.

## 5. `RULE` — 기본 규칙 수행

플레이어가 지금 필요한 목표·행동·결과를 실제로 수행한다.

- 한 구간에서 하나의 핵심 학습 목표를 우선한다.
- 입력과 시스템 반응의 인과를 즉시 읽을 수 있게 한다.
- 첫 의미 있는 행동과 피드백을 계정·상점·알림·평가 요청보다 먼저 제공한다.
- 설명은 행동 직전이나 막힘이 발생한 순간에 짧게 제공한다.
- 본편과 다른 임시 규칙·무적·가짜 수치가 필요하면 차이를 명시하고 제거 시점을 기록한다.

검증 질문:

- 플레이어가 직접 행동했는가
- 무엇이 성공·실패를 만들었는지 설명할 수 있는가
- 본편에서 같은 입력·규칙·피드백이 유지되는가
- 한 단계에 여러 새 개념이 섞이지 않았는가

## 6. `NEED` — 필요·결핍 인식

새 성장·도구·규칙을 소개하기 전에 플레이어가 왜 필요한지 이해하게 한다.

```text
현재 능력으로 기본 행동 성공
→ 새로운 장벽·비효율·위험 발생
→ 원인과 손실을 읽음
→ 무엇이 부족한지 설명
```

좋은 결핍:

- 핵심 규칙에서 자연스럽게 발생한다.
- 문제 전 예고와 대응 기회가 있다.
- 실패 원인과 다음 행동을 연결할 수 있다.
- 재시도·복구 비용이 학습을 방해하지 않는다.

금지:

- 상점이나 과금을 소개하기 위한 강제 패배
- 보이지 않는 규칙·입력 읽기·임의 수치 조작으로 만든 가짜 결핍
- 선택과 무관하게 실패하도록 결과를 고정
- 실패 후 긴 구간을 반복시키거나 회복 불가능 손실을 부과

## 7. `DISCOVER` — 해결 방법 발견

플레이어가 문제를 인식한 뒤 해결 방법을 발견하고 직접 적용한다.

- 필요한 성장 시스템·도구·정보를 문제와 인과적으로 연결한다.
- 획득·선택·장착·배치·사용 중 실제 핵심 행동을 수행하게 한다.
- `무엇을 누르는가`와 함께 `왜 지금 필요한가`, `언제 다시 쓰는가`를 가르친다.
- 해결 방법이 여러 개면 첫 학습에서는 대표 방법 하나를 제공하고 이후 선택 공간을 확장한다.
- 정답 하나를 영구 강제하지 않고, 프로젝트가 의도한 판단·표현·빌드 다양성을 보존한다.

## 8. `FEEL` — 성장 전후 차이 체감

성장 체감은 큰 숫자·이펙트·팝업만으로 증명하지 않는다.

```text
성장 전 기준 행동
↔ 성장 후 동일하거나 비교 가능한 행동
```

최소 하나 이상의 실제 행동 변화가 있어야 한다.

- 해결 시간 감소
- 자원·위험·손실 감소
- 새로운 선택·경로·조합 발생
- 이전 장벽 돌파
- 더 정교한 판단·표현 가능
- 핵심 재미를 더 자주 또는 선명하게 경험

`가짜 성장`의 징후:

- 숫자와 연출만 커지고 선택·행동·결과가 동일하다.
- 성장 직후 적 수치가 자동 보정되어 성취가 사라진다.
- 플레이어가 무엇이 개선됐는지 설명할 수 없다.
- 핵심 재미가 아니라 메뉴 조작과 보상 수령만 늘어난다.

성장 전후 비교 기록:

```yaml
baseline_task:
before_time_cost_risk:
change_applied:
after_time_cost_risk:
new_choice_or_capability:
player_explanation:
core_fun_effect:
```

## 9. `PROVE` — 안내 없는 독립 수행

안내 없는 독립 수행이 없으면 튜토리얼 완료로 판정하지 않는다.

- 하이라이트·강제 입력·정답 고정을 단계적으로 줄인다.
- 앞서 배운 원리를 유사하지만 동일하지 않은 문제에 적용하게 한다.
- 성공과 실패 원인을 확인할 수 있게 한다.
- 한 번의 우연한 성공만으로 숙련을 확정하지 않는다.
- 막히면 전체 정답 대신 단계적 힌트와 복습 경로를 제공한다.

안내 감소 사다리:

```text
시범·명확한 안내
→ 제한된 선택 안에서 수행
→ 힌트가 있는 유사 문제
→ 안내 없는 독립 수행
→ 다른 상황으로 전이
```

## 10. `TRANSFER` — 다른 상황에서 재사용

플레이어가 배운 원리를 다른 적·상황·조합·레벨·세션에서 재사용한다.

- 표면만 다른 동일 문제와 실제 전이 문제를 구분한다.
- 다른 자원·위험·공간·시간 압력에서도 원리가 유지되는지 본다.
- 장기 미접속 후 목표·규칙·진행을 다시 확인할 수 있게 한다.
- 복귀 플레이어에게 전체 강제 튜토리얼 대신 필요한 개념만 재학습하게 한다.

전이 실패는 튜토리얼 문구 부족만이 아니라 규칙 일관성, 피드백, 난이도 급상승, 정보 구조, 기억 부담 문제일 수 있다.

## 11. 점진 공개와 인지 부담

새 개념은 이전 개념 위에 쌓고, 다음 단계로 넘어가기 전에 최소 숙련 증거를 확인한다.

```yaml
concept:
prerequisites:
introduced_at:
guidance_level:
competency_check:
fade_condition:
revisit_trigger:
```

피해야 할 것:

- 여러 시스템을 한 화면에서 동시에 소개
- 설명을 읽는 동안 게임이 진행되거나 위험이 발생
- 앞서 배우지 않은 용어로 새 개념 설명
- 필수 정보와 장식·홍보·메타 알림 경쟁
- 첫 세션에 장기 메타·과금·커뮤니티 기능을 모두 노출

## 12. Skip·복습·복귀·접근성

### Skip

- 숙련자와 재플레이어가 도입부를 건너뛸 수 있게 한다.
- Skip 후 핵심 도움말·목표·조작을 다시 확인할 수 있어야 한다.
- Skip이 영구적인 학습 자료 접근 상실을 만들지 않는다.

### 복습

- 튜토리얼·도움말·목표를 필요할 때 다시 열 수 있다.
- 텍스트 조작표만이 아니라 짧은 시연·연습·맥락 예시를 제공한다.
- 실패 원인에 맞는 관련 항목으로 연결한다.

### 복귀

- 마지막 목표·최근 변화·핵심 조작·빌드 상태를 요약한다.
- 장기 미접속을 초보자로 단정하지 않고 필요한 부분만 재학습한다.

### 접근성 대체 채널

- 음성 정보에 자막·텍스트·시각 신호를 제공한다.
- 색 하나에만 성공·실패·목표 정보를 의존하지 않는다.
- 비핵심 UI 안내는 플레이어가 읽고 해석하고 수행할 충분한 시간을 제공한다.
- 시간 제한·반복 입력·정밀 입력이 학습 목표가 아니라면 조절·대체·일시정지 수단을 검토한다.
- 입력 방식과 UI Focus가 실제 선택 대상을 명확히 보여야 한다.

접근성 옵션 존재만으로 검증 완료를 주장하지 않는다. 실제 장벽과 대체 경로를 대상 플레이어·입력·플랫폼에서 확인한다.

## 13. 벤치마킹

벤치마크는 인기 게임의 화면·대사·보상 순서를 복사하는 절차가 아니다. 현재 결정을 바꿀 질문과 비교 차원을 먼저 고정한다.

```yaml
decision_question:
comparison_titles_or_sources:
platform_and_version:
observed_product_fact:
player_behavior_or_self_report:
working_principle:
failure_condition:
project_fit:
decision: ADOPT/ADAPT/AVOID/TEST/IGNORE
```

### 주요 공식 근거

#### Apple — Onboarding for Games

- URL: `https://developer.apple.com/app-store/onboarding-for-games/`
- 확인일: `2026-08-02`
- 층: `T1_PRIMARY_OFFICIAL`
- 활용: 핵심 루프를 실제 행동으로 가르치기, 기본에서 고급으로 점진 확장, 한 단계씩 짧게 안내, 필요한 순간 여러 짧은 튜토리얼, 안내 없는 플레이, Skip.
- 한계: App Store 맥락의 플랫폼 가이드이며 프로젝트 장르·플랫폼·사업 모델에 맞춰 검증해야 한다.

#### Microsoft — Xbox Accessibility Guideline 109: Objective clarity

- URL: `https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/109`
- 확인일: `2026-08-02`
- 층: `T1_PRIMARY_OFFICIAL`
- 활용: 정적 조작 화면을 튜토리얼로 충분하다고 보지 않기, 핵심 메커니즘을 실제 수행·시연하기, 튜토리얼을 필요할 때 다시 접근하게 하기.
- 한계: 법적 인증이 아니며 실제 프로젝트 플레이테스트를 대신하지 않는다.

#### Microsoft — Xbox Accessibility Guideline 116: Time limits

- URL: `https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/116`
- 확인일: `2026-08-02`
- 층: `T1_PRIMARY_OFFICIAL`
- 활용: 비핵심 UI 튜토리얼·알림에서 읽기·해석·수행 시간을 보장하고 시간 제한을 조절·대체하기.
- 한계: 핵심 게임플레이 시간 압박과 비핵심 UI 시간 제한을 구분한다.

## 14. 플레이테스트와 텔레메트리

튜토리얼 완료율만으로 이해·숙련·성장 체감을 판정하지 않는다.

최소 이벤트 예:

```yaml
session_started:
learning_step_entered:
first_meaningful_action:
action_failed:
hint_requested:
help_reopened:
step_retried:
step_completed:
tutorial_skipped:
independent_task_started:
independent_task_succeeded:
transfer_task_started:
transfer_task_succeeded:
session_abandoned:
```

관찰·자기보고·행동 근거를 분리한다.

| 질문 | 행동 근거 | 자기보고 보조 |
|---|---|---|
| 규칙을 이해했는가 | 안내 없이 올바른 행동·원인 수정 | 규칙을 자신의 말로 설명 |
| 성장 필요를 이해했는가 | 장벽 원인에 맞는 방법 선택 | 왜 필요한지 설명 |
| 성장을 체감했는가 | 시간·자원·위험·선택 변화 | 무엇이 달라졌는지 설명 |
| 전이가 가능한가 | 다른 상황에서 원리 재사용 | 비슷한 상황 예측 |

사전 선언:

```yaml
build_and_version:
target_group_and_prior_exposure:
player_task:
primary_metric:
guardrails:
success_criteria:
stop_criteria:
observation_and_interview_plan:
```

실제 빌드·대상 집단·과제·관찰 없이 재미·이해·쾌감·접근성을 검증했다고 주장하지 않는다.

## 15. 적대적 검토

```text
attack
→ validate-critique
→ decision-report
→ approved refinement
→ regression-recheck
```

필수 공격 질문:

- 튜토리얼 전용 규칙이 본편과 다른가
- 정적 조작표를 실제 학습으로 오인했는가
- 플레이어가 문제를 이해하기 전에 해결책을 광고하는가
- 강제 패배·가짜 결핍·회복 불가능 손실로 성장을 강요하는가
- 가짜 성장으로 숫자와 연출만 바뀌는가
- 핵심 재미보다 상점·과금·알림을 먼저 노출하는가
- 여러 개념을 동시에 가르쳐 실패 원인을 숨기는가
- 완료율이나 한 번의 성공만으로 숙련을 확정하는가
- 안내 없는 독립 수행이 없는가
- 다른 상황에서 재사용하는 전이 검사가 없는가
- Skip·복습·복귀·접근성 대체 채널이 없는가
- 외부 벤치마크를 프로젝트 정본처럼 복제하는가

Finding:

```text
MUST_FIX
SHOULD_FIX
USER_DECISION_REQUIRED
DEFER
REJECTED_CRITIQUE
BLOCKED_UNVERIFIED
```

비판을 모두 수용하지 않는다. 프로젝트 코어·사용자 승인·실제 근거와 비교해 검증된 Finding만 반영한다.

## 16. 출력 계약

```md
## 프로젝트·첫 세션 현황 감사
## 대상 플레이어·플레이 상황·선수 지식
## 핵심 학습 목표와 본편 규칙 연결
## RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER 단계표
## 안내 감소·힌트·실패·복구·재시도
## 성장 전후 비교와 핵심 재미 강화 근거
## Skip·복습·복귀·접근성 대체 채널
## 벤치마크 질문·근거·판정
## 플레이테스트·관찰·인터뷰·텔레메트리
## 적대적 Finding과 판정
## KEEP / CHANGE / REMOVE / TEST / HOLD
## 미검증·롤백·다음 Gate
```

프로젝트 산출물은 `templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md`를 사용한다.

## 17. 완료 Gate

다음이 모두 충족되어야 설계 단계 완료로 판정한다.

- 프로젝트 정본·실제 구현·진행 상태를 먼저 감사했다.
- 핵심 규칙과 첫 세션 학습 목표가 행동 단위로 연결됐다.
- `RULE → NEED → DISCOVER → FEEL → PROVE → TRANSFER`가 실제 플레이 흐름으로 설계됐다.
- 강제 패배·가짜 결핍·가짜 성장·정적 조작표 오판을 방지한다.
- 안내 감소와 안내 없는 독립 수행이 있다.
- 다른 상황에서 재사용하는 전이 검사가 있다.
- Skip·복습·복귀·접근성 대체 채널을 다룬다.
- 벤치마크는 출처·버전·한계·판정을 기록한다.
- 플레이테스트·텔레메트리 성공·중단 기준을 결과 전에 선언한다.
- 적대적 검토 Finding과 미검증을 분리했다.

설계 완료는 실제 구현·사람 플레이테스트·엔진 런타임 검증 완료를 의미하지 않는다.
