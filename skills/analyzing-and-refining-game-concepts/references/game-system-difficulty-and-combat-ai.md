# Game System, Difficulty, and Combat AI Design

## Purpose

`system-design`과 `difficulty-and-combat-ai` Skill Mode에서만 읽는다. 기능·수치를 먼저 늘리지 않고 **플레이어 경험 목표 → Mechanics → Dynamics → Experience → Evidence**를 추적하며, 적의 지능·전투 압박·난이도 조절·검증을 서로 다른 책임으로 설계한다.

이 reference는 공용 절차다. 특정 프로젝트의 체력, 피해량, 반응시간, 적 수, 웨이브 길이와 구현 상태는 프로젝트 책임 원본에 남긴다.

---

## 1. Required inputs

```yaml
player_experience_goal:
target_player_and_play_context:
core_action_choice_and_failure:
current_system_and_combat_rules:
adjacent_systems_and_data_owners:
enemy_roles_and_information_channels:
current_difficulty_modes_and_assists:
platform_input_camera_and_session_constraints:
accessibility_and_performance_constraints:
benchmark_and_player_evidence:
telemetry_playtest_and_failure_evidence:
unknowns_and_decisions:
```

입력이 없으면 값이나 구현 사실을 발명하지 않고 `UNCONFIRMED` 또는 `MEASUREMENT_REQUIRED`로 둔다.

---

# Part A. `system-design`

## 2. 플레이어 경험에서 시스템으로 역추적

```text
플레이어 경험 목표
→ 플레이어가 읽어야 할 정보
→ 고민할 선택과 감수할 위험
→ 입력·행동·자원·상태
→ 시스템 반응과 결과
→ 피드백·학습·다음 행동
→ 필요한 증거
```

각 규칙은 다음 계약을 가진다.

```yaml
rule_or_feature:
player_question:
mechanics:
player_action:
system_response:
dynamics:
expected_experience:
undesired_experience:
feedback_and_legibility:
failure_and_recovery:
evidence_needed:
```

## 3. 시스템 경계

시스템마다 다음을 명시한다.

| 항목 | 질문 |
|---|---|
| 책임 | 이 시스템이 단독으로 결정하는 것은 무엇인가? |
| 입력 | 어떤 상태·데이터·이벤트를 읽는가? |
| 출력 | 어떤 명령·상태·이벤트를 제공하는가? |
| 비책임 | 다른 시스템이 결정해야 하는 것은 무엇인가? |
| 정본 | 기획 규칙·게임 데이터·실제 구현의 책임 파일은 어디인가? |
| 실패 | 입력 누락·충돌·저장 불일치 때 무엇을 하는가? |
| 검증 | 정상·실패·경계 상태를 어떻게 관찰하는가? |

Godot 구현을 계획할 때는 Scene·Node·Resource·Autoload를 기능 목록처럼 배치하지 않는다. 기획 책임과 데이터 수명, 저장·복구, 테스트 경계를 먼저 정하고 Codex 구현 패키지로 넘긴다.

## 4. 시스템 가치 판정

```text
REMOVE
→ REDUCE
→ MERGE
→ CLARIFY
→ FEEDBACK 강화
→ ADD
```

각 시스템을 `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN`으로 분류한다. 인기 기능이나 경쟁작의 표면만으로 `ADD`하지 않는다.

---

# Part B. `difficulty-and-combat-ai`

## 5. 난이도 장벽 프로필

난이도는 적 체력 하나가 아니라 플레이어 능력과 다음 장벽의 관계다.

- 규칙 이해
- 정보 탐색·가독성
- 의사결정 수와 상충 정도
- 기억·주의 분산
- 반응시간·정밀 입력
- 시간 압박
- 자원 부족과 손실 비용
- 반복 길이·복구 거리
- 감각·입력·인지 장벽
- 적 조합·공간·카메라 압박

```yaml
difficulty_barrier:
target_player_segment:
intended_challenge:
required_skill_or_knowledge:
warning_and_information:
recovery_or_alternative:
measurement:
accessibility_risk:
```

## 6. 공정성·가독성·대응 가능성 안전 규칙

높은 난이도에서도 다음을 기본 안전 규칙으로 검토한다.

- 보이지 않는 정보로 즉시 처벌하지 않는다.
- 플레이어 입력을 직접 읽어 완벽하게 카운터하지 않는다.
- 강한 공격은 시각·음향·동작 중 하나 이상으로 예고한다.
- 카메라 밖 즉사, 연속 기절, 기상 직후 재경직, 회피 불가능 조합을 제한한다.
- 실패 원인과 다음에 바꿀 행동을 설명할 수 있어야 한다.
- 접근성 보조를 적의 지능 저하와 동일시하지 않는다.

공정성은 쉬움을 뜻하지 않는다. **정보가 주어지고, 인과가 일관되며, 대응 기회가 존재하는 어려움**을 뜻한다.

## 7. 전투 AI 3계층

### 7.1 개별 적 판단

`FSM / Behavior Tree / Utility Scoring` 중 프로젝트 복잡도에 맞는 최소 구조를 사용한다.

책임:

- 감지와 기억
- 현재 목표와 행동 후보
- 공격·이동·엄폐·후퇴·지원 판단
- 행동 쿨다운과 반복 억제
- 애니메이션·이펙트에 전달할 의도

개별 적은 전체 전투 압박량을 독자적으로 결정하지 않는다.

### 7.2 전투 조율자

여러 적이 함께 있을 때 다음을 조율한다.

- 공격 위치·역할 슬롯
- 공격 예산
- 위협 예산
- 강공격·잡기·기절 중복 제한
- 대기 중 적의 선회·엄폐·장전·경고·재배치 행동
- 카메라·공간·탈출로 안전 규칙

예산 예시의 실제 값은 프로젝트가 정한다.

```yaml
action_id:
threat_cost:
concurrency_group:
requires_line_of_sight:
requires_telegraph:
blocked_during_player_disable:
release_condition:
```

### 7.3 난이도·페이싱 디렉터

전투 전체의 강약을 조절한다.

- 웨이브·증원·특수 적
- 공격·위협 예산 상한
- 회복·탐색·정산 시간
- 자원 공급 후보
- 현재 긴장도 상태
- 다음 전투에 적용할 난이도 변경

디렉터가 개별 공격 애니메이션 도중 적 체력·피해·판정을 임의로 바꾸는 것을 기본값으로 삼지 않는다.

## 8. 반응시간과 의도적 빗나감

적이 감지 즉시 완벽히 반응하면 영리함보다 부정행위처럼 보일 수 있다.

```yaml
awareness_state:
perception_delay:
decision_delay:
aim_or_commit_delay:
telegraph_time:
recovery_time:
```

원거리 공격의 의도적 빗나감은 허공 난사가 아니라 다음과 같은 압박 정보가 되도록 설계한다.

- 플레이어 발밑·엄폐물·이동 예상 경로
- 탄착 파편·궤적·위치성 사운드
- 실제 명중 권한을 가진 적과 견제 역할의 분리

근접 전투에서는 짧은 사거리, 직전 위치 공격, 명확한 후딜레이, 강공격 중 잡기 보류 등으로 변환할 수 있다.

## 9. 긴장도 페이싱

기본 상태:

```text
Build Up
→ Sustain Peak
→ Peak Fade
→ Relax
→ 다음 Build Up
```

| 상태 | 목적 | 허용 조절 |
|---|---|---|
| Build Up | 위협을 읽고 준비 | 적 조합·공간 압박 점진 증가 |
| Sustain Peak | 핵심 시험 | 예산 상한 유지, 불공정 중복 금지 |
| Peak Fade | 승부 정리 | 증원 감소, 남은 위협 명료화 |
| Relax | 복구·정산·다음 의도 | 회복·보상·장비·경로 선택 시간 |

계속 최고 압박을 유지하지 않는다. 압박 뒤의 회복이 있어야 다음 압박이 의미를 가진다.

## 10. 고정 난이도 설계

먼저 난이도별 **경험 의도**를 적고 조절 변수를 선택한다.

권장 조절 순서:

1. 공격 예고·반응시간·동시 공격·연속 공격 간격
2. 측면·엄폐·정보 공유·역할 교대 등 전술 빈도
3. 웨이브·특수 적·회복 구간·자원 공급
4. 적 체력·피해·이동속도 등 순수 수치

```yaml
difficulty_tier:
experience_intent:
information_and_telegraph:
reaction_and_recovery:
attack_and_threat_budget:
tactical_frequency:
encounter_pacing:
resource_support:
numeric_scaling:
unchanged_fairness_rules:
```

체력 스펀지와 갑작스러운 피해 폭증이 핵심 선택을 대체하지 않는지 확인한다.

## 11. 적응형 난이도

### 11.1 입력 분리

장기 실력과 단기 스트레스를 분리한다.

```yaml
long_term_skill:
  dodge_or_avoidance:
  kill_or_objective_speed:
  resource_efficiency:
  decision_consistency:
  mastery_signals:
short_term_stress:
  recent_damage:
  active_threats:
  disable_or_control_time:
  low_health_and_resources:
  escape_route_pressure:
```

현재 HP 하나로 실력을 단정하지 않는다.

### 11.2 적용 규칙

- 현재 전투 응급 조절과 다음 전투 장기 조절을 분리한다.
- 히스테리시스로 상태 경계를 분리한다.
- 같은 상태가 일정 기간 유지될 때만 변경한다.
- 변경 쿨다운과 한 번에 한 단계 제한을 둔다.
- 플레이어가 보고 있는 적의 체력·피해를 갑자기 바꾸지 않는다.
- 보스·랭킹·기록 경쟁에서는 허용 범위와 표시 정책을 별도로 정한다.
- 적응형 난이도 끄기·고정 난이도 선택·보조 옵션을 검토한다.

### 11.3 성공을 벌주지 않는다

```text
좋은 플레이
→ 성장과 숙련의 체감 보존
→ 다음 구간에서 더 다양한 선택·조합·전술 제공
```

```text
좋은 플레이
→ 즉시 적 체력·피해가 같은 비율로 증가
→ 성장 무효화
```

두 번째 구조를 기본값으로 사용하지 않는다.

## 12. 텔레메트리

최소 후보:

- 전투 시작·종료·소요 시간
- 플레이어 최저·종료 체력
- 최근 짧은 구간 최대 피해량
- 동시 공격자와 예산 사용량
- 경직·기절 연속 시간
- 카메라 밖·예고 미인지 피해
- 적 역할별 피해·처치·무력화 비중
- 회복·소모품·탈출 사용
- 사망 직전 상태·행동·원인 후보
- 난이도 상태·변경 이유·적용 시점

텔레메트리는 감정이나 원인을 자동 확정하지 않는다. 플레이 영상·관찰·인터뷰와 결합한다.

## 13. 플레이테스트

```yaml
hypothesis:
build_and_version:
tester_segment_and_prior_exposure:
difficulty_configuration:
combat_scenario:
observation_points:
telemetry_events:
player_self_report_questions:
primary_metric:
guardrail_metrics:
success_failure_stop:
rollback_trigger:
```

필수 반례:

- 가만히 있을 때
- 계속 도망갈 때
- 좁은 공간·카메라 경계
- 여러 강공격·기절 조합
- 낮은 체력·자원 고갈
- 숙련자가 빠르게 압도할 때
- 낮은 숙련자가 규칙을 이해하지 못할 때
- 동일 seed·동일 입력 재현

## 14. 접근성·성능

- 난이도, 접근성, 보조 기능을 한 축으로 합치지 않는다.
- 정보 채널은 색 하나에만 의존하지 않는다.
- 시간·입력·인지 장벽에 대체 경로를 검토한다.
- 다수 적의 감지·경로·회피·Utility 계산 비용을 목표 플랫폼에서 측정한다.
- 모든 적이 매 프레임 전체 행동 후보를 평가하도록 기본 설계하지 않는다.

실제 접근성·성능 검증은 `reviewing-and-validating-project-changes`의 해당 mode로 넘긴다.

## 15. Output contract

```md
## 플레이어 경험 목표
## 시스템 경계와 책임 원본
## 행동·선택·결과 계약
## 난이도 장벽 프로필
## 공정성·가독성·대응 가능성 안전 규칙
## 개별 적 판단·전투 조율자·난이도/페이싱 디렉터
## 공격·위협 예산
## 반응시간·예고·회복·의도적 빗나감
## Build Up·Sustain Peak·Peak Fade·Relax
## 고정 난이도별 경험과 조절 변수
## 장기 실력·단기 스트레스·적응형 난이도
## 히스테리시스·변경 쿨다운·적용 시점
## 텔레메트리·플레이테스트·접근성·성능
## 유지·수정·삭제·보류·재검증
## Base 승격 후보
## 프로젝트 전용 유지
## 미검증·롤백·다음 게이트
```

## 16. 공용화 경계

### Base 승격 후보

- 장르를 넘어 반복 검증된 공정성 원칙
- 재사용 가능한 입력·출력·검증 절차
- 여러 프로젝트에서 같은 실패를 줄인 예산·페이싱 패턴
- 프로젝트 고유 수치를 제거해도 유효한 텔레메트리·테스트 계약

### 프로젝트 전용 유지

- 적 이름·역할·패턴·수치
- 난이도별 실제 배율과 시간
- 보스·스테이지·카메라·맵 고유 규칙
- 프로젝트 데이터 경로·Scene·Resource·구현 상태
- 한 번의 플레이테스트 결과

한 번의 성공을 공용 강제 규칙으로 승격하지 않는다. 프로젝트 Pilot과 반복 증거를 거쳐 `managing-base-change-proposals`로 환류한다.
